#!/usr/bin/env python3
"""Resolve the single E07 V2 negative-space hold by manual inspection.

The source V2 is immutable.  The 41-pixel component is inspected at 10x on
dark, light, saturated-magenta and saturated-green backgrounds.  Because it
follows the hair specular/edge instead of a checker-scale background opening,
the conservative result is zero pixel changes.  A deterministic PNG audit
metadata chunk gives the reviewed Candidate its own SHA without pretending
that an uncertain white region was safely removable.
"""

from __future__ import annotations

import hashlib
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "delivery/JICUN_E07_POSTBATTLE_CALL_CANDIDATE_RGBA_ALPHA_FIX_V2.png"
OUTPUT = ROOT / "delivery/JICUN_E07_POSTBATTLE_CALL_CANDIDATE_RGBA_ALPHA_FIX_V3.png"
QA = ROOT / "qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V3_BG_QA_100_50.png"
PROOF = ROOT / "qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V3_LOCAL_COMPONENT_PROOF.png"
RECEIPT = ROOT / "receipts/CALL01_JICUN_E07_ALPHA_FIX_V3_RECEIPT.md"
HASHES = ROOT / "receipts/CALL01_ALPHA_FIX_V3_HASHES.sha256"
MANIFEST = ROOT / "asset-manifest.tsv"

EXPECTED_SOURCE_SHA256 = "de06a6775c65e56370e71aa52f85c080df659b7e0bab6abbae09c46e8cc53298"
EXPECTED_SIZE = (1022, 1538)
CHANGE_BBOX = (590, 103, 599, 114)  # half-open
EXPECTED_CHANGE_PIXELS = 41
SAFE_CROP_RECT = (93, 8, 820, 1538)  # >=16 px around the full alpha bbox


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


def exact_component(rgba: np.ndarray) -> np.ndarray:
    rgb = rgba[:, :, :3].astype(np.int16)
    alpha = rgba[:, :, 3]
    minimum = rgb.min(axis=2)
    chroma = rgb.max(axis=2) - minimum
    x0, y0, x1, y1 = CHANGE_BBOX
    roi = np.zeros(alpha.shape, dtype=bool)
    roi[y0:y1, x0:x1] = True
    candidate = (
        (
            ((minimum >= 55) & (chroma <= 20))
            | ((minimum >= 180) & (chroma <= 55))
        )
        & (alpha == 255)
        & roi
    )

    seed = (103, 591)  # y, x; locked inside the reviewed component
    assert candidate[seed], "reviewed seed no longer belongs to the neutral component"
    seen = np.zeros_like(candidate)
    queue: deque[tuple[int, int]] = deque([seed])
    seen[seed] = True
    while queue:
        y, x = queue.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < alpha.shape[0] and 0 <= nx < alpha.shape[1] and candidate[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                queue.append((ny, nx))

    ys, xs = np.nonzero(seen)
    actual_bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    assert actual_bbox == CHANGE_BBOX, f"component bbox drifted: {actual_bbox}"
    assert len(ys) == EXPECTED_CHANGE_PIXELS, f"component area drifted: {len(ys)}"
    return seen


def composite(image: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    base = Image.new("RGBA", image.size, color + (255,))
    base.alpha_composite(image)
    return base.convert("RGB")


def build_background_qa(v3: Image.Image) -> None:
    backgrounds = (
        ("DARK", (8, 10, 14)),
        ("LIGHT", (240, 242, 245)),
        ("SATURATED MAGENTA", (255, 0, 190)),
        ("SATURATED GREEN", (0, 255, 80)),
    )
    x0, y0, x1, y1 = SAFE_CROP_RECT
    panel_w, panel_h = x1 - x0, y1 - y0
    half_w, half_h = panel_w // 2, panel_h // 2
    gap = 18
    margin = 24
    label_h = 38
    full_top = 82
    half_top = full_top + label_h + panel_h + 48
    board_w = margin * 2 + panel_w * 4 + gap * 3
    board_h = half_top + label_h + half_h + 105
    board = Image.new("RGB", (board_w, board_h), (24, 29, 38))
    draw = ImageDraw.Draw(board)
    title = font(30)
    label = font(18)
    draw.text((margin, 20), "JICUN E07 ALPHA FIX V3 — FULL FIGURE 100% + 50% BACKGROUND QA", font=title, fill=(240, 243, 248))

    full_crop = v3.crop(SAFE_CROP_RECT)
    half = full_crop.resize((half_w, half_h), Image.Resampling.LANCZOS)
    for index, (name, color) in enumerate(backgrounds):
        px = margin + index * (panel_w + gap)
        full_bg = Image.new("RGBA", full_crop.size, color + (255,))
        full_bg.alpha_composite(full_crop)
        board.paste(full_bg.convert("RGB"), (px, full_top + label_h))
        draw.text((px, full_top + 7), f"100% {name}", font=label, fill=(240, 243, 248))

        half_bg = Image.new("RGBA", half.size, color + (255,))
        half_bg.alpha_composite(half)
        board.paste(half_bg.convert("RGB"), (px, half_top + label_h))
        draw.text((px, half_top + 7), f"50% {name}", font=label, fill=(240, 243, 248))

    draw.text(
        (margin, board_h - 68),
        "Manual Alpha audit: changed=0 px | RGB changed=0 | safe_crop_rect=[93,8,820,1538)",
        font=label,
        fill=(245, 195, 90),
    )
    QA.parent.mkdir(parents=True, exist_ok=True)
    board.save(QA, optimize=True)


def build_local_proof(v2: Image.Image, v3: Image.Image, held: np.ndarray) -> None:
    crop_box = (570, 82, 625, 145)
    scale = 10
    panel_size = ((crop_box[2] - crop_box[0]) * scale, (crop_box[3] - crop_box[1]) * scale)
    panels: list[tuple[str, Image.Image]] = []
    for name, image in (("V2", v2), ("V3", v3)):
        crop = image.crop(crop_box).resize(panel_size, Image.Resampling.NEAREST)
        for bg_name, color in (("MAGENTA", (255, 0, 190)), ("GREEN", (0, 255, 80)), ("DARK", (8, 10, 14))):
            base = Image.new("RGBA", panel_size, color + (255,))
            base.alpha_composite(crop)
            panels.append((f"{name} {bg_name}", base.convert("RGB")))

    held_overlay = np.zeros((*v2.size[::-1], 4), dtype=np.uint8)
    held_overlay[held] = (255, 180, 20, 255)
    held_crop = Image.fromarray(held_overlay, mode="RGBA").crop(crop_box).resize(panel_size, Image.Resampling.NEAREST)
    held_bg = Image.new("RGBA", panel_size, (240, 242, 245, 255))
    held_bg.alpha_composite(held_crop)
    panels.append(("REVIEWED/KEPT = AMBER", held_bg.convert("RGB")))

    gap = 12
    margin = 18
    label_h = 34
    board_w = margin * 2 + len(panels) * panel_size[0] + gap * (len(panels) - 1)
    board_h = 74 + label_h + panel_size[1] + 86
    board = Image.new("RGB", (board_w, board_h), (24, 29, 38))
    draw = ImageDraw.Draw(board)
    title = font(28)
    label = font(17)
    draw.text((margin, 18), "V3 MANUAL HAIR-GAP RESOLUTION — 10x NEAREST", font=title, fill=(240, 243, 248))
    x = margin
    for name, panel in panels:
        draw.text((x, 78), name, font=label, fill=(240, 243, 248))
        board.paste(panel, (x, 78 + label_h))
        x += panel_size[0] + gap
    draw.text(
        (margin, board_h - 58),
        "Manual verdict: KEEP HAIR HIGHLIGHT/EDGE. It lacks checker-scale alternation; no subject or Alpha pixel was changed.",
        font=label,
        fill=(245, 195, 90),
    )
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    board.save(PROOF, optimize=True)


def main() -> None:
    assert sha256(SOURCE) == EXPECTED_SOURCE_SHA256, "V2 source SHA drifted"
    v2 = Image.open(SOURCE).convert("RGBA")
    assert v2.size == EXPECTED_SIZE and v2.mode == "RGBA"
    before = np.asarray(v2, dtype=np.uint8)
    assert set(np.unique(before[:, :, 3]).tolist()) == {0, 255}
    assert Image.fromarray(before[:, :, 3]).getbbox() == (109, 24, 804, 1521)

    held = exact_component(before)
    changed = np.zeros(before.shape[:2], dtype=bool)
    after = before.copy()
    assert np.array_equal(before[:, :, :3], after[:, :, :3])
    assert int(np.count_nonzero(before[:, :, :3] != after[:, :, :3])) == 0
    assert int(np.count_nonzero(before[:, :, 3] != after[:, :, 3])) == 0
    assert bool(np.all(before[:, :, 3][~changed] == after[:, :, 3][~changed]))
    assert Image.fromarray(after[:, :, 3]).getbbox() == (109, 24, 804, 1521)

    v3 = Image.fromarray(after, mode="RGBA")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("AlphaAudit", "V3 manual negative-space review; no confirmed Alpha deletion")
    pnginfo.add_text("SourceSHA256", EXPECTED_SOURCE_SHA256)
    pnginfo.add_text("Lifecycle", "Candidate; user=false; runtime=false; canon=false")
    v3.save(OUTPUT, optimize=True, pnginfo=pnginfo)
    assert np.array_equal(np.asarray(Image.open(OUTPUT).convert("RGBA")), before)
    build_background_qa(v3)
    build_local_proof(v2, v3, held)

    before_zero = int(np.count_nonzero(before[:, :, 3] == 0))
    after_zero = int(np.count_nonzero(after[:, :, 3] == 0))
    before_opaque = int(np.count_nonzero(before[:, :, 3] == 255))
    after_opaque = int(np.count_nonzero(after[:, :, 3] == 255))
    output_sha = sha256(OUTPUT)
    receipt = f"""# JICUN E07 Alpha Fix V3 receipt

## Result

`ALPHA_ONLY_LOCAL_FIX_COMPLETE / CANDIDATE / USER_REVIEW_REQUIRED / NOT_BOUND`

- source V2 SHA-256: `{EXPECTED_SOURCE_SHA256}`
- repaired V3 SHA-256: `{output_sha}`
- size/mode: `1022x1538 RGBA8`
- ImageGen: `0`; Blender: `0`; global white key: `false`

## Manual negative-space decision

At 10x on dark, light, saturated-magenta and saturated-green backgrounds, the previous held component `[590,103,599,114)` follows a narrow hair specular/edge stroke. Only `6/41` pixels support the fitted checker phase (`14.6%`), with no checker-scale alternation. Independent visual/topology review agrees that it is not a confirmed background hole. It is therefore reclassified as `KEEP_CONFIRMED_HAIR_HIGHLIGHT_OR_EDGE`; no Alpha pixel was changed.

| audited zone | decision |
| --- | --- |
| hair strands | existing loops remain transparent; the 41-pixel hold was reviewed and kept as hair highlight/edge |
| left arm / torso | the V2 enclosed gap remains transparent; no new opaque background found |
| crossed hand / terminal | visible inter-finger spaces fall over shirt, sleeve or terminal pixels, not scene background; kept |
| hanging hand / fingers | visible gaps fall over the coat/trouser body behind the hand, not scene background; kept |
| coat hem / legs | leg and tail negative spaces were already transparent; kept unchanged |
| shirt / skin / badge / highlights | confirmed subject; untouched |

## Byte evidence

| metric | V2 | V3 |
| --- | ---: | ---: |
| alpha=0 | {before_zero:,} | {after_zero:,} |
| alpha=255 | {before_opaque:,} | {after_opaque:,} |
| partial Alpha | 0 | 0 |
| RGB pixels changed | 0 | 0 |
| Alpha pixels changed | 0 | 0 |

- Alpha change bbox list: `[]`
- Alpha changed pixels: `0`
- manually reviewed/kept bbox: `[590,103,599,114)`; `41` subject pixels
- full-person alpha bbox: `[109,24,804,1521)`
- `safe_crop_rect` with at least 16-pixel subject padding: `[93,8,820,1538)`

## Lifecycle

- `status=Candidate`
- `user_approved=false`
- `runtime_allowed=false`
- `canon=false`
- `godot_bound=false`
- local `asset-manifest.tsv`: V2 retained as `Candidate_Superseded_By_Manual_Alpha_Audit`; V3 registered as the unapproved Candidate
"""
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(receipt, encoding="utf-8")

    hashes = (
        f"{sha256(SOURCE)}  {SOURCE}\n"
        f"{output_sha}  {OUTPUT}\n"
        f"{sha256(QA)}  {QA}\n"
        f"{sha256(PROOF)}  {PROOF}\n"
        f"{sha256(RECEIPT)}  {RECEIPT}\n"
        f"{sha256(MANIFEST)}  {MANIFEST}\n"
        f"{sha256(Path(__file__))}  {Path(__file__)}\n"
    )
    HASHES.parent.mkdir(parents=True, exist_ok=True)
    HASHES.write_text(hashes, encoding="utf-8")

    print(f"source_sha256={sha256(SOURCE)}")
    print(f"output_sha256={output_sha}")
    print(f"alpha_changed_pixels=0")
    print(f"manually_reviewed_kept_pixels={EXPECTED_CHANGE_PIXELS}")
    print(f"rgb_changed_pixels=0")
    print(f"safe_crop_rect={SAFE_CROP_RECT}")
    print(f"output={OUTPUT}")
    print(f"qa={QA}")
    print(f"proof={PROOF}")
    print(f"receipt={RECEIPT}")


if __name__ == "__main__":
    main()
