#!/usr/bin/env python3
"""Deterministic E07 enclosed-checker Alpha repair.

This is intentionally a zero-ImageGen technical pass.  It preserves every RGB
byte from the raw Candidate and changes Alpha only for enclosed components that
independently pass all of these gates:

1. the pixels remained opaque after the V1 edge-connected extraction;
2. the component contains enough neutral pixels matching the fitted 21 px
   checker phase from confirmed exterior background;
3. the component does not touch any protected anatomy/costume/terminal ROI;
4. the component is not an ambiguous antialias or highlight fragment.

Run ``--preflight-only`` first to emit the component/ROI evidence without
writing a repaired delivery.  Run without that flag only after inspecting the
preflight report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw/JICUN_E07_POSTBATTLE_CALL_CALL01_RAW.png"
V1 = ROOT / "delivery/JICUN_E07_POSTBATTLE_CALL_CANDIDATE_RGBA.png"
V2 = ROOT / "delivery/JICUN_E07_POSTBATTLE_CALL_CANDIDATE_RGBA_ALPHA_FIX_V2.png"
PREFLIGHT_JSON = ROOT / "receipts/CALL01_ALPHA_FIX_V2_COMPONENT_PREFLIGHT.json"
PREFLIGHT_PNG = ROOT / "qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V2_COMPONENT_PREFLIGHT.png"
QA = ROOT / "qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V2_50_100_QA.png"
PROOF = ROOT / "qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V2_COMPONENT_PROOF.png"
RECEIPT = ROOT / "receipts/CALL01_JICUN_E07_ALPHA_FIX_V2_RECEIPT.md"
HASHES = ROOT / "receipts/CALL01_ALPHA_FIX_V2_HASHES.sha256"

EXPECTED_RAW_SHA256 = "4a1266ecce221edabed6e46c644d66f39fd17b0d35a7ec4f1ee75ee499de88de"
EXPECTED_V1_SHA256 = "2cd8d55529e94bfd9c49afc4080218036b698f3f8e8ee8d16a191d1ded08a35e"
EXPECTED_SIZE = (1022, 1538)


@dataclass(frozen=True)
class Roi:
    roi_id: str
    label: str
    bbox: tuple[int, int, int, int]


PROTECTED_ROIS = (
    Roi("P01", "face / eyes / skin", (330, 175, 570, 445)),
    Roi("P02", "white shirt / shirt highlights", (350, 285, 620, 955)),
    Roi("P03", "museum badge", (315, 470, 415, 600)),
    Roi("P04", "right hand / arm terminal / hologram", (340, 640, 820, 930)),
    Roi("P05", "left hand / white cuff", (135, 1135, 315, 1405)),
)

# The automatic gates below must resolve to exactly these three components.
# Half-open coordinates are used throughout: [x0,y0,x1,y1).
EXPECTED_DELETE_COMPONENTS = {
    (244, 762, 269, 947): 2113,
    (532, 51, 562, 70): 153,
    (464, 32, 492, 39): 110,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def connected_components(mask: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    components: list[tuple[np.ndarray, np.ndarray]] = []
    for seed_y, seed_x in zip(*np.nonzero(mask)):
        if seen[seed_y, seed_x]:
            continue
        queue: deque[tuple[int, int]] = deque([(int(seed_y), int(seed_x))])
        seen[seed_y, seed_x] = True
        ys: list[int] = []
        xs: list[int] = []
        while queue:
            y, x = queue.popleft()
            ys.append(y)
            xs.append(x)
            for next_y, next_x in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if (
                    0 <= next_y < height
                    and 0 <= next_x < width
                    and mask[next_y, next_x]
                    and not seen[next_y, next_x]
                ):
                    seen[next_y, next_x] = True
                    queue.append((next_y, next_x))
        components.append((np.asarray(ys, dtype=np.int32), np.asarray(xs, dtype=np.int32)))
    components.sort(key=lambda item: len(item[0]), reverse=True)
    return components


def fit_checker_phase(
    rgb: np.ndarray,
    old_alpha: np.ndarray,
    minimum: np.ndarray,
    chroma: np.ndarray,
) -> dict[str, object]:
    # Only already-transparent, near-neutral exterior pixels may train the raw
    # checker model.  The deterministic modulo sample keeps this inexpensive.
    fit_y, fit_x = np.nonzero((old_alpha == 0) & (minimum >= 235) & (chroma <= 5))
    sample = ((fit_x + 2 * fit_y) % 17) == 0
    fit_x = fit_x[sample]
    fit_y = fit_y[sample]
    luminance = rgb[fit_y, fit_x].mean(axis=1)
    assert len(luminance) >= 40000, "insufficient confirmed exterior checker pixels"

    results: list[tuple[float, int, int, int, bool]] = []
    for cell in range(19, 24):
        for offset_x in range(cell):
            x_cells = (fit_x + offset_x) // cell
            for offset_y in range(cell):
                parity = ((x_cells + (fit_y + offset_y) // cell) & 1).astype(bool)
                par_dark_error = float(np.mean(np.abs(luminance - np.where(parity, 246.0, 254.0))))
                par_light_error = float(np.mean(np.abs(luminance - np.where(parity, 254.0, 246.0))))
                if par_dark_error <= par_light_error:
                    results.append((par_dark_error, cell, offset_x, offset_y, True))
                else:
                    results.append((par_light_error, cell, offset_x, offset_y, False))
    results.sort()
    best = results[0]
    assert best[1:5] == (21, 14, 16, True), f"unexpected raw checker phase: {best}"
    return {
        "cell_px": best[1],
        "offset_x": best[2],
        "offset_y": best[3],
        "parity_true_is_dark": best[4],
        "mean_absolute_luminance_error": round(best[0], 6),
        "runner_up_error": round(results[1][0], 6),
        "fit_pixels": int(len(luminance)),
        "light_level": 254,
        "dark_level": 246,
    }


def bbox_for(ys: np.ndarray, xs: np.ndarray) -> tuple[int, int, int, int]:
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def roi_hits(ys: np.ndarray, xs: np.ndarray) -> list[str]:
    hits: list[str] = []
    for roi in PROTECTED_ROIS:
        x0, y0, x1, y1 = roi.bbox
        if bool(np.any((xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1))):
            hits.append(roi.roi_id)
    return hits


def analyze_components(
    rgb: np.ndarray,
    old_alpha: np.ndarray,
    phase: dict[str, object],
) -> tuple[list[dict[str, object]], list[tuple[np.ndarray, np.ndarray]]]:
    rgb16 = rgb.astype(np.int16)
    minimum = rgb16.min(axis=2)
    maximum = rgb16.max(axis=2)
    chroma = maximum - minimum
    luminance = rgb.mean(axis=2)

    # Reuse the V1 neutral/background candidate family, but only inside pixels
    # that V1 left opaque.  No global white key is performed.
    background_candidate = (
        ((minimum >= 55) & (chroma <= 20))
        | ((minimum >= 180) & (chroma <= 55))
    ) & (old_alpha == 255)

    y_grid, x_grid = np.indices(old_alpha.shape)
    parity = (
        ((x_grid + int(phase["offset_x"])) // int(phase["cell_px"]))
        + ((y_grid + int(phase["offset_y"])) // int(phase["cell_px"]))
    ) & 1
    expected_luminance = np.where(parity.astype(bool), 246.0, 254.0)
    phase_support = (
        (minimum >= 225)
        & (chroma <= 8)
        & (np.abs(luminance - expected_luminance) <= 20.0)
    )

    components = connected_components(background_candidate)
    records: list[dict[str, object]] = []
    selected: list[tuple[np.ndarray, np.ndarray]] = []
    for component_index, (ys, xs) in enumerate(components):
        area = int(len(ys))
        bbox = bbox_for(ys, xs)
        support_pixels = int(phase_support[ys, xs].sum())
        support_fraction = support_pixels / area
        mean_chroma = float(chroma[ys, xs].mean())
        hits = roi_hits(ys, xs)
        delete = (
            area >= 20
            and support_pixels >= 5
            and support_fraction >= 0.15
            and mean_chroma <= 3.0
            and not hits
        )
        if delete:
            decision = "DELETE_PHASE_CONFIRMED_ENCLOSED_BACKGROUND"
            selected.append((ys, xs))
        elif hits:
            decision = "PROTECT_ROI"
        elif support_pixels > 0:
            decision = "HOLD_INSUFFICIENT_PHASE_OR_COMPONENT_EVIDENCE"
        else:
            decision = "KEEP_FOREGROUND"
        records.append(
            {
                "component_index": component_index,
                "bbox_half_open": list(bbox),
                "area_pixels": area,
                "mean_rgb": [round(float(value), 3) for value in rgb[ys, xs].mean(axis=0)],
                "mean_chroma": round(mean_chroma, 6),
                "phase_support_pixels": support_pixels,
                "phase_support_fraction": round(support_fraction, 6),
                "protected_roi_hits": hits,
                "decision": decision,
            }
        )

    actual = {bbox_for(ys, xs): int(len(ys)) for ys, xs in selected}
    assert actual == EXPECTED_DELETE_COMPONENTS, f"selection drifted; refusing Alpha write: {actual}"
    return records, selected


def draw_preflight(raw: Image.Image, records: list[dict[str, object]]) -> None:
    canvas = Image.new("RGB", (1450, 1600), (24, 29, 38))
    canvas.paste(raw, (20, 42))
    draw = ImageDraw.Draw(canvas)
    title = font(28)
    label = font(17)
    draw.text((20, 8), "E07 ALPHA V2 PREFLIGHT — COMPONENTS BEFORE WRITE", font=title, fill=(240, 243, 248))

    for roi in PROTECTED_ROIS:
        x0, y0, x1, y1 = roi.bbox
        box = (x0 + 20, y0 + 42, x1 + 20, y1 + 42)
        draw.rectangle(box, outline=(30, 210, 235), width=2)
        draw.text((box[0] + 2, box[1] + 2), roi.roi_id, font=label, fill=(10, 130, 155))

    bright_records = [record for record in records if int(record["phase_support_pixels"]) > 0]
    for record in bright_records:
        x0, y0, x1, y1 = [int(value) for value in record["bbox_half_open"]]
        decision = str(record["decision"])
        if decision.startswith("DELETE"):
            color = (30, 225, 95)
        elif decision.startswith("PROTECT"):
            color = (30, 210, 235)
        else:
            color = (255, 170, 35)
        box = (x0 + 20, y0 + 42, x1 + 20, y1 + 42)
        draw.rectangle(box, outline=color, width=3)

    x_text = 1070
    draw.text((x_text, 54), "Protection ROIs", font=title, fill=(30, 210, 235))
    y_text = 94
    for roi in PROTECTED_ROIS:
        draw.text((x_text, y_text), f"{roi.roi_id} {roi.bbox}", font=label, fill=(225, 232, 240))
        y_text += 34
    y_text += 20
    draw.text((x_text, y_text), "DELETE", font=title, fill=(30, 225, 95))
    y_text += 42
    for record in records:
        if str(record["decision"]).startswith("DELETE"):
            draw.text(
                (x_text, y_text),
                f"{record['bbox_half_open']}\narea={record['area_pixels']} phase={record['phase_support_pixels']}",
                font=label,
                fill=(225, 232, 240),
                spacing=3,
            )
            y_text += 72
    y_text += 12
    draw.text((x_text, y_text), "Orange = held", font=label, fill=(255, 170, 35))
    y_text += 30
    draw.text((x_text, y_text), "Cyan = protected", font=label, fill=(30, 210, 235))
    y_text += 55
    draw.text((x_text, y_text), "No global white key", font=label, fill=(245, 195, 90))
    y_text += 30
    draw.text((x_text, y_text), "RGB will remain byte-identical", font=label, fill=(245, 195, 90))
    PREFLIGHT_PNG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(PREFLIGHT_PNG, optimize=True)


def composite_on(image: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    base = Image.new("RGBA", image.size, color + (255,))
    base.alpha_composite(image)
    return base.convert("RGB")


def build_qa(v2: Image.Image, removed: np.ndarray) -> None:
    backgrounds = (
        ("BLACK", (8, 10, 14), (255, 255, 255)),
        ("LIGHT", (240, 242, 245), (18, 24, 32)),
        ("MAGENTA", (180, 0, 140), (255, 255, 255)),
        ("SATURATED GREEN", (0, 210, 90), (5, 25, 20)),
    )
    crop_box = (200, 0, 720, 1538)
    panel_width = 520
    gap = 20
    top = 80
    label_height = 34
    full_height = 1538
    half_height = 769
    half_top = top + label_height + full_height + 55
    board_width = gap + 4 * (panel_width + gap)
    board_height = half_top + label_height + half_height + 115
    board = Image.new("RGB", (board_width, board_height), (24, 29, 38))
    draw = ImageDraw.Draw(board)
    title_font = font(28)
    label_font = font(19)
    draw.text((gap, 18), "JICUN E07 ALPHA FIX V2 — BLACK / LIGHT / MAGENTA / SATURATED — 100% + 50%", font=title_font, fill=(240, 243, 248))

    half = v2.resize((511, 769), Image.Resampling.LANCZOS)
    for index, (name, color, _text_color) in enumerate(backgrounds):
        x0 = gap + index * (panel_width + gap)
        full = composite_on(v2, color).crop(crop_box)
        board.paste(full, (x0, top + label_height))
        draw.text((x0 + 8, top + 4), f"100% {name}", font=label_font, fill=(240, 243, 248))

        half_panel = Image.new("RGBA", (panel_width, half_height), color + (255,))
        half_panel.alpha_composite(half, ((panel_width - half.width) // 2, 0))
        board.paste(half_panel.convert("RGB"), (x0, half_top + label_height))
        draw.text((x0 + 8, half_top + 4), f"50% {name}", font=label_font, fill=(240, 243, 248))

    draw.text((gap, board_height - 75), f"Alpha-only removal: {int(removed.sum()):,} px | RGB changes: 0 | Candidate / user=false / runtime=false / canon=false", font=label_font, fill=(245, 195, 90))
    QA.parent.mkdir(parents=True, exist_ok=True)
    board.save(QA, optimize=True)


def build_proof(raw: Image.Image, old: Image.Image, v2: Image.Image, records: list[dict[str, object]], removed: np.ndarray) -> None:
    canvas = Image.new("RGB", (2100, 1700), (24, 29, 38))
    draw = ImageDraw.Draw(canvas)
    title_font = font(30)
    label_font = font(20)
    draw.text((30, 20), "E07 ALPHA FIX V2 — COMPONENT / BEFORE-AFTER PROOF", font=title_font, fill=(240, 243, 248))

    old_half = old.resize((511, 769), Image.Resampling.LANCZOS)
    v2_half = v2.resize((511, 769), Image.Resampling.LANCZOS)
    old_panel = Image.new("RGBA", old_half.size, (0, 210, 90, 255))
    new_panel = old_panel.copy()
    old_panel.alpha_composite(old_half)
    new_panel.alpha_composite(v2_half)
    canvas.paste(old_panel.convert("RGB"), (30, 90))
    canvas.paste(new_panel.convert("RGB"), (571, 90))
    draw.text((40, 100), "V1 BEFORE", font=label_font, fill=(5, 25, 20))
    draw.text((581, 100), "V2 AFTER", font=label_font, fill=(5, 25, 20))

    overlay = raw.convert("RGBA")
    overlay_pixels = np.asarray(overlay).copy()
    overlay_pixels[removed, 0] = 255
    overlay_pixels[removed, 1] = 30
    overlay_pixels[removed, 2] = 30
    overlay_pixels[removed, 3] = 255
    overlay = Image.fromarray(overlay_pixels, mode="RGBA").resize((511, 769), Image.Resampling.NEAREST)
    canvas.paste(overlay.convert("RGB"), (1112, 90))
    draw.text((1122, 100), "REMOVED PIXELS = RED", font=label_font, fill=(255, 255, 255))

    alpha = np.asarray(v2.getchannel("A"))
    alpha_rgb = np.repeat(alpha[:, :, None], 3, axis=2)
    alpha_half = Image.fromarray(alpha_rgb, mode="RGB").resize((511, 769), Image.Resampling.NEAREST)
    canvas.paste(alpha_half, (1653, 90))
    draw.text((1663, 100), "V2 ALPHA", font=label_font, fill=(255, 210, 60))

    y = 900
    draw.text((30, y), "Confirmed enclosed components", font=title_font, fill=(30, 225, 95))
    y += 52
    for record in records:
        if str(record["decision"]).startswith("DELETE"):
            draw.text(
                (30, y),
                f"bbox={record['bbox_half_open']}  area={record['area_pixels']}  phase={record['phase_support_pixels']}/{record['area_pixels']}",
                font=label_font,
                fill=(225, 232, 240),
            )
            y += 38
    y += 20
    draw.text((30, y), "Protected: face/eyes/skin, white shirt, badge, both hands, arm terminal and hologram.", font=label_font, fill=(30, 210, 235))
    y += 42
    draw.text((30, y), "Held: bbox [590,103,599,114) is an exterior-connected hair-edge AA/highlight fragment, not a confirmed enclosed hole.", font=label_font, fill=(255, 170, 35))
    y += 42
    draw.text((30, y), "All RGB bytes are identical before/after; only Alpha changed on 2,376 confirmed background pixels.", font=label_font, fill=(245, 195, 90))
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(PROOF, optimize=True)


def alpha_receipt(alpha: np.ndarray) -> dict[str, object]:
    values, counts = np.unique(alpha, return_counts=True)
    count_map = {int(value): int(count) for value, count in zip(values, counts)}
    nonzero_y, nonzero_x = np.nonzero(alpha > 0)
    transparent_components = connected_components(alpha == 0)
    return {
        "alpha_values": sorted(count_map),
        "alpha_0_pixels": count_map.get(0, 0),
        "alpha_255_pixels": count_map.get(255, 0),
        "partial_alpha_pixels": int(alpha.size - count_map.get(0, 0) - count_map.get(255, 0)),
        "nonzero_alpha_bbox_half_open": [
            int(nonzero_x.min()),
            int(nonzero_y.min()),
            int(nonzero_x.max()) + 1,
            int(nonzero_y.max()) + 1,
        ],
        "transparent_components_4_connected": len(transparent_components),
        "transparent_component_areas_desc": [int(len(item[0])) for item in transparent_components[:8]],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()

    assert sha256(RAW) == EXPECTED_RAW_SHA256, "raw source hash drifted"
    assert sha256(V1) == EXPECTED_V1_SHA256, "V1 delivery hash drifted"
    raw = Image.open(RAW).convert("RGB")
    old = Image.open(V1).convert("RGBA")
    assert raw.size == EXPECTED_SIZE and old.size == EXPECTED_SIZE
    rgb = np.asarray(raw, dtype=np.uint8)
    old_rgba = np.asarray(old, dtype=np.uint8)
    assert np.array_equal(rgb, old_rgba[:, :, :3]), "V1 changed generated RGB"
    old_alpha = old_rgba[:, :, 3]
    assert set(np.unique(old_alpha).tolist()) == {0, 255}

    rgb16 = rgb.astype(np.int16)
    minimum = rgb16.min(axis=2)
    chroma = rgb16.max(axis=2) - minimum
    phase = fit_checker_phase(rgb, old_alpha, minimum, chroma)
    records, selected = analyze_components(rgb, old_alpha, phase)

    # Keep the persisted report reviewable: every phase-supported component is
    # present, plus only substantial protected components.  One-pixel protected
    # anatomy fragments are still enforced by the mask but do not flood the
    # evidence document.
    bright_records = [
        record
        for record in records
        if int(record["phase_support_pixels"]) > 0
        or (
            str(record["decision"]).startswith("PROTECT")
            and int(record["area_pixels"]) >= 100
        )
    ]
    report = {
        "schema_id": "C01_JICUN_E07_ALPHA_FIX_V2_PREFLIGHT_V1",
        "scope": {
            "zero_imagegen": True,
            "alpha_only": True,
            "global_white_key": False,
            "production_binding": False,
            "test_only_capture_after_delivery": True,
        },
        "source": {
            "raw_path": str(RAW),
            "raw_sha256": sha256(RAW),
            "v1_path": str(V1),
            "v1_sha256": sha256(V1),
            "size": list(EXPECTED_SIZE),
        },
        "checker_phase": phase,
        "protection_rois": [
            {"roi_id": roi.roi_id, "label": roi.label, "bbox_half_open": list(roi.bbox)}
            for roi in PROTECTED_ROIS
        ],
        "component_counts": {
            "all_enclosed_candidate_components": len(records),
            "reported_relevant_components": len(bright_records),
            "delete_components": len(selected),
            "delete_pixels": int(sum(len(ys) for ys, _ in selected)),
        },
        "relevant_components": bright_records,
        "automatic_selection_exact_expected_match": True,
    }
    PREFLIGHT_JSON.parent.mkdir(parents=True, exist_ok=True)
    PREFLIGHT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    draw_preflight(raw, records)
    if args.preflight_only:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    removed = np.zeros_like(old_alpha, dtype=bool)
    for ys, xs in selected:
        removed[ys, xs] = True
    assert int(removed.sum()) == 2376
    assert not bool(np.any(removed & (old_alpha == 0)))

    new_rgba = old_rgba.copy()
    new_rgba[removed, 3] = 0
    assert np.array_equal(new_rgba[:, :, :3], old_rgba[:, :, :3])
    assert np.array_equal(new_rgba[:, :, :3], rgb)
    assert int(np.count_nonzero(new_rgba[:, :, 3] != old_alpha)) == 2376
    assert bool(np.all(new_rgba[:, :, 3][~removed] == old_alpha[~removed]))
    v2 = Image.fromarray(new_rgba, mode="RGBA")
    V2.parent.mkdir(parents=True, exist_ok=True)
    v2.save(V2, optimize=True)

    before_alpha = alpha_receipt(old_alpha)
    after_alpha = alpha_receipt(new_rgba[:, :, 3])
    build_qa(v2, removed)
    build_proof(raw, old, v2, records, removed)

    v2_sha = sha256(V2)
    qa_sha = sha256(QA)
    proof_sha = sha256(PROOF)
    preflight_sha = sha256(PREFLIGHT_JSON)
    receipt_text = f"""# JICUN E07 Alpha Fix V2 receipt

## Result

`PASS_INTERNAL_ALPHA_GATE / CANDIDATE / USER_REVIEW_REQUIRED / NOT_BOUND`

This was a deterministic, zero-ImageGen Alpha-only repair.  It does not alter story data, production HUD bindings, Runtime, Canon or Default.

## Exact scope

- beat: `E07_NEXT_TIME_I_BOOK`
- line: `下次我来订。`
- slot: `JICUN_POST_BATTLE_CALL`
- source V1 SHA-256: `{EXPECTED_V1_SHA256}`
- repaired V2 SHA-256: `{v2_sha}`
- ImageGen calls in this repair: `0`

## Checker evidence and component decision

- fitted raw checker: cell=`{phase['cell_px']} px`, offsets=`({phase['offset_x']},{phase['offset_y']})`, parity-true=`dark`
- exterior fit pixels: `{phase['fit_pixels']:,}`
- fit MAE: `{phase['mean_absolute_luminance_error']}`
- no global white key was used

Removed only these confirmed enclosed-background components (half-open bbox):

| bbox | area | decision |
| --- | ---: | --- |
| `[244,762,269,947)` | 2,113 | left-arm/torso enclosed checker gap |
| `[532,51,562,70)` | 153 | enclosed hair-loop checker gap |
| `[464,32,492,39)` | 110 | enclosed top hair-loop checker gap |

Held `[590,103,599,114)` because its true white core is already exterior-connected and the remaining opaque fragment is ambiguous hair-edge antialias/highlight, not a reliable enclosed hole.

## Protection ROIs

| ROI | bbox | protected content |
| --- | --- | --- |
| P01 | `[330,175,570,445)` | face, eyes, skin |
| P02 | `[350,285,620,955)` | white shirt and highlights |
| P03 | `[315,470,415,600)` | museum badge |
| P04 | `[340,640,820,930)` | right hand, arm terminal, hologram |
| P05 | `[135,1135,315,1405)` | left hand and white cuff |

## Preservation metrics

| Metric | Before | After |
| --- | ---: | ---: |
| alpha=0 | {before_alpha['alpha_0_pixels']:,} | {after_alpha['alpha_0_pixels']:,} |
| alpha=255 | {before_alpha['alpha_255_pixels']:,} | {after_alpha['alpha_255_pixels']:,} |
| partial Alpha | {before_alpha['partial_alpha_pixels']:,} | {after_alpha['partial_alpha_pixels']:,} |
| transparent components | {before_alpha['transparent_components_4_connected']} | {after_alpha['transparent_components_4_connected']} |
| RGB pixels changed | 0 | 0 |
| Alpha pixels changed | 0 | 2,376 |

The remaining opaque-subject RGB and all transparent RGB are byte-identical to the original raw Candidate.

## Files

- repaired Candidate: `{V2}`
- preflight report: `{PREFLIGHT_JSON}`
- component preflight: `{PREFLIGHT_PNG}`
- black/light/magenta/saturated 50/100 QA: `{QA}`
- component proof: `{PROOF}`

## Lifecycle

- `status=Candidate`
- `user_approved=false`
- `runtime_allowed=false`
- `canon=false`
- `godot_bound=false`
"""
    RECEIPT.write_text(receipt_text, encoding="utf-8")
    hashes = (
        f"{sha256(RAW)}  {RAW}\n"
        f"{sha256(V1)}  {V1}\n"
        f"{v2_sha}  {V2}\n"
        f"{preflight_sha}  {PREFLIGHT_JSON}\n"
        f"{sha256(PREFLIGHT_PNG)}  {PREFLIGHT_PNG}\n"
        f"{qa_sha}  {QA}\n"
        f"{proof_sha}  {PROOF}\n"
        f"{sha256(RECEIPT)}  {RECEIPT}\n"
    )
    HASHES.write_text(hashes, encoding="utf-8")

    result = {
        "success": True,
        "v1_sha256": EXPECTED_V1_SHA256,
        "v2_sha256": v2_sha,
        "rgb_pixels_changed": 0,
        "alpha_pixels_changed": int(removed.sum()),
        "before_alpha": before_alpha,
        "after_alpha": after_alpha,
        "delivery": str(V2),
        "qa": str(QA),
        "proof": str(PROOF),
        "receipt": str(RECEIPT),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
