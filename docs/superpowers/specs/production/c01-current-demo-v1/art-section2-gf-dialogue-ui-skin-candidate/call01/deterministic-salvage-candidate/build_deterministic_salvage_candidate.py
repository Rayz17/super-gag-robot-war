#!/usr/bin/env python3
"""Deterministic checker-background recovery for the rejected GF UI atlas.

This does not alter the original FAIL receipt.  It uses the single retained RGB
raw, a fitted periodic checker model, and hysteresis-connected masks.  It makes
no network or ImageGen calls and touches no Godot consumer.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
CALL01 = HERE.parent
RAW = CALL01 / "raw" / "GF_DIALOGUE_UI_SKIN_ATLAS_CALL01_RAW.png"
DELIVERY = HERE / "delivery"
QA = HERE / "qa"
RECEIPTS = HERE / "receipts"

for folder in (DELIVERY, QA, RECEIPTS):
    folder.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class Region:
    name: str
    box: tuple[int, int, int, int]  # x0, y0, x1, y1
    min_area: int
    expected_components: int
    fill_holes_up_to: int = 64


REGIONS = (
    Region("dialogue_frame", (30, 15, 1642, 310), 1000, 1, 96),
    Region("speaker_tab", (520, 305, 1357, 416), 1000, 1, 64),
    Region("action_holder", (40, 320, 440, 670), 1000, 1, 96),
    Region("progress", (510, 430, 1363, 550), 1000, 4, 48),
    Region("control_shells", (480, 565, 1385, 680), 1000, 3, 48),
    Region("fill_sample", (38, 685, 340, 934), 1000, 1, 96),
    Region("accent_divider", (385, 715, 1595, 790), 1000, 1, 48),
    Region("white_sweep", (380, 820, 1600, 900), 1000, 1, 256),
)

STRONG_THRESHOLDS = (9.0, 9.25, 9.5)
WEAK_THRESHOLD = 7.0
CANONICAL_STRONG_THRESHOLD = 9.25


def image_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def fit_background(rgb: np.ndarray) -> tuple[np.ndarray, dict]:
    h, w, _ = rgb.shape
    yy, xx = np.indices((h, w))
    f = rgb.astype(np.float32)
    luma = f.mean(axis=2)
    chroma = f.max(axis=2) - f.min(axis=2)

    safe = np.zeros((h, w), dtype=bool)
    safe[:20, :] = True
    safe[-10:, :] = True
    safe[:, :35] = True
    safe[:, -30:] = True
    safe[85:250, 105:1565] = True
    safe[380:610, 110:355] = True
    safe[300:310, :] = True
    safe &= (chroma <= 4) & (luma >= 240)

    tile = 12
    best = None
    for oy in range(tile):
        for ox in range(tile):
            parity = (((xx + ox) // tile + (yy + oy) // tile) & 1).astype(bool)
            v0 = luma[safe & ~parity]
            v1 = luma[safe & parity]
            m0 = float(v0.mean())
            m1 = float(v1.mean())
            row = (abs(m0 - m1), ox, oy, m0, m1)
            if best is None or row > best:
                best = row

    # Two-cell repeat is 24 px.  A per-phase median absorbs the baked checker's
    # gentle edge ramp without learning any foreground geometry.
    neutral_pool = (chroma <= 4) & (luma >= 240)
    phase = np.zeros((24, 24, 3), dtype=np.float32)
    phase_counts = np.zeros((24, 24), dtype=np.int32)
    for py in range(24):
        for px in range(24):
            take = neutral_pool & (yy % 24 == py) & (xx % 24 == px)
            values = f[take]
            if len(values) == 0:
                phase[py, px] = 251.0
            else:
                phase[py, px] = np.median(values, axis=0)
                phase_counts[py, px] = len(values)
    background = phase[yy % 24, xx % 24]

    flat = rgb.reshape(-1, 3)
    colors, counts = np.unique(flat, axis=0, return_counts=True)
    neutral_exact = [
        (int(n), [int(v) for v in c])
        for c, n in zip(colors, counts)
        if int(c.max()) - int(c.min()) <= 1 and int(c.min()) >= 240
    ]
    neutral_exact.sort(reverse=True)

    metrics = {
        "checker_tile_px": tile,
        "checker_two_cell_period_px": 24,
        "best_phase_offset_xy": [int(best[1]), int(best[2])],
        "best_phase_parity_luma_means": [best[3], best[4]],
        "best_phase_mean_separation": best[0],
        "dominant_neutral_rgb_modes": [
            {"rgb": c, "count": n} for n, c in neutral_exact[:8]
        ],
        "phase_rgb_min": phase.min(axis=(0, 1)).tolist(),
        "phase_rgb_max": phase.max(axis=(0, 1)).tolist(),
        "phase_rgb_mean": phase.mean(axis=(0, 1)).tolist(),
        "phase_model_sha256": sha256(np.rint(phase).astype(np.uint8).tobytes()).hexdigest(),
        "phase_sample_count_min": int(phase_counts.min()),
        "phase_sample_count_max": int(phase_counts.max()),
    }
    return background, metrics


def components(mask: np.ndarray, connectivity: int = 8) -> list[dict]:
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    result: list[dict] = []
    offsets = (
        ((-1, 0), (1, 0), (0, -1), (0, 1))
        if connectivity == 4
        else tuple((dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx)
    )
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            q = [(y, x)]
            seen[y, x] = True
            pts: list[tuple[int, int]] = []
            min_x = max_x = x
            min_y = max_y = y
            touches_edge = False
            while q:
                cy, cx = q.pop()
                pts.append((cy, cx))
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)
                touches_edge |= cy == 0 or cx == 0 or cy == h - 1 or cx == w - 1
                for dy, dx in offsets:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            result.append(
                {
                    "area": len(pts),
                    "bbox": [min_x, min_y, max_x + 1, max_y + 1],
                    "touches_edge": touches_edge,
                    "points": pts,
                }
            )
    return result


def hysteresis_region(
    residual: np.ndarray,
    region: Region,
    strong_threshold: float,
) -> tuple[np.ndarray, list[dict], list[dict]]:
    x0, y0, x1, y1 = region.box
    r = residual[y0:y1, x0:x1]
    weak = r > WEAK_THRESHOLD
    strong = r > strong_threshold
    output = np.zeros_like(weak, dtype=bool)
    kept: list[dict] = []
    rejected: list[dict] = []
    for comp in components(weak, 8):
        pts = comp["points"]
        intersects_strong = any(strong[py, px] for py, px in pts)
        comp["intersects_strong"] = intersects_strong
        if comp["area"] >= region.min_area and intersects_strong:
            for py, px in pts:
                output[py, px] = True
            kept.append(comp)
        elif comp["area"] >= 20:
            rejected.append(comp)

    # Preserve only tiny enclosed negative-space interruptions caused by pixels
    # numerically identical to the checker.  Large authored windows stay clear.
    inverse = ~output
    filled_holes: list[dict] = []
    for hole in components(inverse, 4):
        if not hole["touches_edge"] and hole["area"] <= region.fill_holes_up_to:
            for py, px in hole["points"]:
                output[py, px] = True
            filled_holes.append(hole)

    for item in kept + rejected + filled_holes:
        item.pop("points", None)
    return output, kept, filled_holes


def prune_checker_matte(
    support: np.ndarray,
    rgb: np.ndarray,
    region_names: tuple[str, ...] = ("dialogue_frame", "speaker_tab", "action_holder", "control_shells"),
) -> dict[str, int]:
    """Remove only bright neutral boundary pixels left by the baked checker.

    Gold and cyan authored highlights are protected by chroma; navy/graphite
    material is protected by luminance.  Removal is restricted to the exposed
    one-pixel boundary and repeated three times so no white matte shelf remains.
    """
    f = rgb.astype(np.float32)
    luma = f.mean(axis=2)
    chroma = f.max(axis=2) - f.min(axis=2)
    removed: dict[str, int] = {}
    selected = {r.name: r for r in REGIONS if r.name in region_names}
    for name, region in selected.items():
        x0, y0, x1, y1 = region.box
        local = support[y0:y1, x0:x1]
        local_luma = luma[y0:y1, x0:x1]
        local_chroma = chroma[y0:y1, x0:x1]
        count = 0
        for _ in range(3):
            padded = np.pad(local, 1, constant_values=False)
            interior = local.copy()
            h, w = local.shape
            for dy in range(3):
                for dx in range(3):
                    interior &= padded[dy : dy + h, dx : dx + w]
            boundary = local & ~interior
            matte = boundary & (local_luma >= 120.0) & (local_chroma <= 12.0)
            n = int(matte.sum())
            if n == 0:
                break
            local[matte] = False
            count += n
        support[y0:y1, x0:x1] = local
        removed[name] = count
    return removed


def build_support_masks(residual: np.ndarray, rgb: np.ndarray) -> tuple[dict[float, np.ndarray], dict]:
    h, w = residual.shape
    variants: dict[float, np.ndarray] = {}
    all_stats: dict[str, dict] = {}
    for threshold in STRONG_THRESHOLDS:
        full = np.zeros((h, w), dtype=bool)
        threshold_stats: dict[str, dict] = {}
        for region in REGIONS:
            local, kept, holes = hysteresis_region(residual, region, threshold)
            if len(kept) != region.expected_components:
                raise RuntimeError(
                    f"{region.name}: expected {region.expected_components} components, got {len(kept)} at {threshold}"
                )
            x0, y0, x1, y1 = region.box
            if np.any(full[y0:y1, x0:x1] & local):
                raise RuntimeError(f"overlapping region masks at {region.name}")
            full[y0:y1, x0:x1] |= local
            threshold_stats[region.name] = {
                "support_pixels": int(local.sum()),
                "kept_components": kept,
                "small_holes_filled": holes,
            }
        # These two authored windows are visibly empty in the retained raw.
        # Clearing their conservative interior rectangles prevents weak-checker
        # noise from being retained through accidental edge connectivity.
        full[85:250, 105:1565] = False
        full[380:610, 110:355] = False
        threshold_stats["checker_matte_prune"] = prune_checker_matte(full, rgb)
        variants[threshold] = full
        all_stats[str(threshold)] = threshold_stats
    return variants, all_stats


def iou(a: np.ndarray, b: np.ndarray) -> float:
    union = np.logical_or(a, b).sum()
    return 1.0 if union == 0 else float(np.logical_and(a, b).sum() / union)


def recover_rgba(
    rgb_u8: np.ndarray,
    background: np.ndarray,
    residual: np.ndarray,
    support: np.ndarray,
) -> tuple[np.ndarray, dict]:
    f = rgb_u8.astype(np.float32)
    h, w, _ = f.shape
    out = np.zeros((h, w, 4), dtype=np.uint8)
    yy, xx = np.indices((h, w))
    luma = f.mean(axis=2)

    sweep_region = next(r for r in REGIONS if r.name == "white_sweep")
    sx0, sy0, sx1, sy1 = sweep_region.box
    sweep = np.zeros((h, w), dtype=bool)
    sweep[sy0:sy1, sx0:sx1] = support[sy0:sy1, sx0:sx1]

    # A checker-composited antialiased fringe may still be much darker than the
    # checker and must not be mistaken for an opaque gray outline.  Only deep
    # source contrast or a fully surrounded interior pixel is unambiguously
    # opaque.  This preserves authored interior RGB while decontaminating the
    # boundary against the fitted checker.
    padded = np.pad(support, 1, constant_values=False)
    interior = support.copy()
    for dy in range(3):
        for dx in range(3):
            interior &= padded[dy : dy + h, dx : dx + w]

    core_non_sweep = support & ~sweep & ((residual >= 80.0) | interior)
    core_sweep = sweep & (residual >= 32.0)
    core = core_non_sweep | core_sweep
    partial = support & ~core
    alpha = np.zeros((h, w), dtype=np.float32)
    alpha[core] = 1.0

    below = np.maximum(background - f, 0.0) / np.maximum(background, 1.0)
    above = np.maximum(f - background, 0.0) / np.maximum(255.0 - background, 1.0)
    min_alpha = np.max(np.maximum(below, above), axis=2)
    alpha[partial] = np.maximum(min_alpha[partial], 12.0 / 255.0)
    alpha = np.clip(alpha, 0.0, 1.0)

    out_rgb = f.copy()
    decontam = partial & ~sweep
    a3 = np.maximum(alpha[:, :, None], 1.0 / 255.0)
    recovered = (f - (1.0 - a3) * background) / a3
    recovered = np.clip(recovered, 0.0, 255.0)
    out_rgb[decontam] = recovered[decontam]

    out[:, :, :3] = np.rint(out_rgb).astype(np.uint8)
    out[:, :, 3] = np.rint(alpha * 255.0).astype(np.uint8)
    out[~support, :3] = 0

    opaque = out[:, :, 3] == 255
    opaque_changed = int(np.any(out[:, :, :3][opaque] != rgb_u8[opaque], axis=1).sum())
    partial_mask = (out[:, :, 3] > 0) & (out[:, :, 3] < 255) & ~sweep
    partial_rgb = out[:, :, :3].astype(np.int16)
    partial_chroma = partial_rgb.max(axis=2) - partial_rgb.min(axis=2)
    partial_luma = partial_rgb.mean(axis=2)
    suspicious_bright_neutral = partial_mask & (partial_luma >= 230) & (partial_chroma <= 5)
    bright_neutral_components = components(suspicious_bright_neutral, 8)
    bright_neutral_areas = sorted((c["area"] for c in bright_neutral_components), reverse=True)

    sweep_support = sweep
    sweep_high_luma_source = sweep_support & (luma >= 235)
    metrics = {
        "alpha0_pixels": int((out[:, :, 3] == 0).sum()),
        "alpha_partial_pixels": int(((out[:, :, 3] > 0) & (out[:, :, 3] < 255)).sum()),
        "alpha255_pixels": int((out[:, :, 3] == 255).sum()),
        "opaque_rgb_changed_pixels": opaque_changed,
        "partial_non_sweep_bright_neutral_pixels": int(suspicious_bright_neutral.sum()),
        "partial_non_sweep_bright_neutral_connected_components": len(bright_neutral_areas),
        "partial_non_sweep_bright_neutral_max_connected_area": max(bright_neutral_areas, default=0),
        "white_sweep_support_pixels": int(sweep_support.sum()),
        "white_sweep_high_luma_source_pixels": int(sweep_high_luma_source.sum()),
        "white_sweep_high_luma_preserved_pixels": int(
            (sweep_high_luma_source & (out[:, :, 3] > 0)).sum()
        ),
        "white_sweep_high_luma_preservation_ratio": float(
            (sweep_high_luma_source & (out[:, :, 3] > 0)).sum()
            / max(1, sweep_high_luma_source.sum())
        ),
    }
    return out, metrics


def crop_rgba(full: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    return full.crop(box)


def component_boxes(mask: np.ndarray, region: Region) -> list[tuple[int, int, int, int]]:
    x0, y0, x1, y1 = region.box
    local = mask[y0:y1, x0:x1]
    found = [c for c in components(local, 8) if c["area"] >= region.min_area]
    found.sort(key=lambda c: c["bbox"][0])
    return [
        (x0 + b[0], y0 + b[1], x0 + b[2], y0 + b[3])
        for b in (c["bbox"] for c in found)
    ]


def pack_cells(
    full: Image.Image,
    boxes: list[tuple[int, int, int, int]],
    cell_size: tuple[int, int],
) -> Image.Image:
    cw, ch = cell_size
    atlas = Image.new("RGBA", (cw * len(boxes), ch), (0, 0, 0, 0))
    for index, box in enumerate(boxes):
        piece = full.crop(box)
        if piece.width > cw or piece.height > ch:
            raise RuntimeError(f"piece {box} does not fit cell {cell_size}")
        x = index * cw + (cw - piece.width) // 2
        y = (ch - piece.height) // 2
        atlas.alpha_composite(piece, (x, y))
    return atlas


def mirror_tile(full: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int]]:
    # Sample is deliberately inside the dark material, outside its ornamental frame.
    source_box = (126, 776, 190, 840)
    patch = full.crop(source_box)
    tile = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tile.alpha_composite(patch, (0, 0))
    tile.alpha_composite(patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (64, 0))
    tile.alpha_composite(patch.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, 64))
    tile.alpha_composite(
        patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM),
        (64, 64),
    )
    return tile, source_box


def save_assets(full_rgba: np.ndarray, support: np.ndarray) -> tuple[list[dict], dict]:
    full = Image.fromarray(full_rgba, "RGBA")
    atlas_path = DELIVERY / "gf_dialogue_ui_skin_atlas_rgba_salvage_candidate.png"
    full.save(atlas_path)

    frame = crop_rgba(full, (30, 15, 1642, 310))
    speaker = crop_rgba(full, (520, 305, 1357, 416))
    holder = crop_rgba(full, (40, 320, 440, 670))
    divider = crop_rgba(full, (385, 715, 1595, 790))
    sweep = crop_rgba(full, (380, 820, 1600, 900))
    fill, fill_source_box = mirror_tile(full)
    fill_pixels = np.array(fill, dtype=np.uint8)
    fill_left_right_equal = bool(np.array_equal(fill_pixels[:, 0], fill_pixels[:, -1]))
    fill_top_bottom_equal = bool(np.array_equal(fill_pixels[0], fill_pixels[-1]))

    progress_region = next(r for r in REGIONS if r.name == "progress")
    progress_boxes = component_boxes(support, progress_region)
    progress = pack_cells(full, progress_boxes, (192, 112))

    controls_region = next(r for r in REGIONS if r.name == "control_shells")
    control_boxes = component_boxes(support, controls_region)
    control_row = pack_cells(full, control_boxes, (288, 112))
    controls = Image.new("RGBA", (864, 336), (0, 0, 0, 0))
    for row in range(3):
        controls.alpha_composite(control_row, (0, row * 112))

    products = [
        ("C01_GF_DIALOGUE_FRAME_9SLICE", "gf_dialogue_frame_9slice_rgba.png", frame, "linear", "disabled", (96, 64, 96, 64), "n/a", "n/a", "40,70,1572,225"),
        ("C01_GF_DIALOGUE_FILL_TILE", "gf_dialogue_fill_tile_rgba.png", fill, "linear", "enabled", (0, 0, 0, 0), "1x1", "material_fill", "0,0,128,128"),
        ("C01_GF_SPEAKER_TAB_9SLICE", "gf_speaker_tab_9slice_rgba.png", speaker, "linear", "disabled", (52, 20, 52, 20), "n/a", "n/a", "160,38,677,73"),
        ("C01_GF_DIALOGUE_PROGRESS_ATLAS", "gf_dialogue_progress_atlas_rgba.png", progress, "linear", "disabled", (0, 0, 0, 0), "4x1;cell=192x112", "idle,completed,current,locked", "0,0,768,112"),
        ("C01_GF_DIALOGUE_NEXT_PROMPT_ATLAS", "gf_dialogue_next_prompt_atlas_rgba.png", controls, "linear", "disabled", (0, 0, 0, 0), "3x3;cell=288x112", "keyboard_enter_idle,keyboard_enter_focus,keyboard_enter_pressed,mouse_primary_idle,mouse_primary_focus,mouse_primary_pressed,gamepad_south_idle,gamepad_south_focus,gamepad_south_pressed", "0,0,864,336"),
        ("C01_GF_DIALOGUE_ACCENT_MASK", "gf_dialogue_accent_mask_rgba.png", sweep, "linear", "disabled", (0, 0, 0, 0), "1x1", "white_sweep", "0,0,1220,80"),
        ("C01_GF_ACTION_SLICE_HOLDER_EXTRA", "gf_action_slice_holder_rgba.png", holder, "linear", "disabled", (48, 48, 48, 48), "n/a", "n/a", "65,55,320,295"),
        ("C01_GF_GOLD_CYAN_DIVIDER_EXTRA", "gf_gold_cyan_divider_rgba.png", divider, "linear", "disabled", (0, 0, 0, 0), "1x1", "divider", "0,0,1210,75"),
    ]

    manifest_rows: list[dict] = []
    for asset_id, name, image, filter_mode, repeat, margins, layout, states, safe_rect in products:
        path = DELIVERY / name
        image.save(path)
        manifest_rows.append(
            {
                "asset_id": asset_id,
                "path": f"delivery/{name}",
                "media": "image/png",
                "width": image.width,
                "height": image.height,
                "alpha": "RGBA8_true_alpha",
                "color_space": "sRGB",
                "filter_mode": filter_mode,
                "repeat_mode": repeat,
                "nine_slice_left": margins[0],
                "nine_slice_top": margins[1],
                "nine_slice_right": margins[2],
                "nine_slice_bottom": margins[3],
                "safe_rect": safe_rect,
                "atlas_layout": layout,
                "state_ids": states,
                "lifecycle": "USER_REJECTED_HISTORY_ONLY_DO_NOT_USE",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
                "user_visual_acceptance": "false",
                "source_rights_receipt": "../USER_REJECTED_HISTORY_ONLY_DO_NOT_USE.md",
                "sha256": image_sha(path),
            }
        )

    source_map = {
        "full_atlas": [0, 0, full.width, full.height],
        "dialogue_frame": [30, 15, 1642, 310],
        "speaker_tab": [520, 305, 1357, 416],
        "action_holder": [40, 320, 440, 670],
        "accent_divider": [385, 715, 1595, 790],
        "white_sweep": [380, 820, 1600, 900],
        "fill_tile_source_patch": list(fill_source_box),
        "fill_tile_left_right_edges_identical": fill_left_right_equal,
        "fill_tile_top_bottom_edges_identical": fill_top_bottom_equal,
        "progress_component_boxes": [list(v) for v in progress_boxes],
        "control_shell_component_boxes": [list(v) for v in control_boxes],
        "control_shell_note": "three authored state shells repeated across three input rows; live glyphs remain outside this bitmap",
    }
    return manifest_rows, source_map


def write_manifest(rows: list[dict]) -> None:
    fields = [
        "asset_id", "path", "media", "width", "height", "alpha", "color_space",
        "filter_mode", "repeat_mode", "nine_slice_left", "nine_slice_top",
        "nine_slice_right", "nine_slice_bottom", "safe_rect", "atlas_layout",
        "state_ids", "lifecycle", "runtime_allowed", "runtime_handoff",
        "user_visual_acceptance", "source_rights_receipt", "sha256",
    ]
    lines = ["\t".join(fields)]
    for row in rows:
        lines.append("\t".join(str(row[key]) for key in fields))
    (HERE / "asset-manifest.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def composite_on(image: Image.Image, color: tuple[int, int, int, int]) -> Image.Image:
    bg = Image.new("RGBA", image.size, color)
    bg.alpha_composite(image)
    return bg.convert("RGB")


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill=(240, 244, 248)) -> None:
    draw.text(xy, text, font=ImageFont.load_default(), fill=fill)


def make_background_qa(full: Image.Image) -> None:
    thumb = full.resize((full.width // 2, full.height // 2), Image.Resampling.LANCZOS)
    colors = [
        (8, 18, 28, 255),
        (245, 246, 248, 255),
        (128, 128, 128, 255),
        (255, 0, 255, 255),
    ]
    names = ["DARK", "LIGHT", "GRAY50", "MAGENTA"]
    pad = 20
    cell_w, cell_h = thumb.width + pad * 2, thumb.height + 44
    board = Image.new("RGB", (cell_w * 2, cell_h * 2), (24, 28, 34))
    draw = ImageDraw.Draw(board)
    for i, (color, name) in enumerate(zip(colors, names)):
        x = (i % 2) * cell_w + pad
        y = (i // 2) * cell_h + 28
        board.paste(composite_on(thumb, color), (x, y))
        label(draw, (x, y - 18), f"{name} / 50%")
    board.save(QA / "GF_UI_ALPHA_BACKGROUNDS_50PCT.png")


def make_component_qa(rows: list[dict]) -> None:
    assets = [(row, Image.open(HERE / row["path"]).convert("RGBA")) for row in rows]
    width = 1700
    y = 36
    placements = []
    for row, image in assets:
        placements.append((row, image, y))
        y += image.height + 34
    board = Image.new("RGB", (width, y + 20), (8, 18, 28))
    draw = ImageDraw.Draw(board)
    for row, image, py in placements:
        label(draw, (12, py - 18), f"{row['asset_id']} / 100%")
        board.paste(composite_on(image, (8, 18, 28, 255)), (12, py))
    board.save(QA / "GF_UI_COMPONENTS_DARK_100PCT.png")


def make_sweep_qa() -> None:
    sweep = Image.open(DELIVERY / "gf_dialogue_accent_mask_rgba.png").convert("RGBA")
    colors = [(8, 18, 28, 255), (245, 246, 248, 255), (255, 0, 255, 255)]
    names = ["DARK", "LIGHT", "MAGENTA"]
    board = Image.new("RGB", (sweep.width + 40, (sweep.height + 42) * 3), (24, 28, 34))
    draw = ImageDraw.Draw(board)
    for i, (color, name) in enumerate(zip(colors, names)):
        y = i * (sweep.height + 42) + 24
        label(draw, (20, y - 18), f"WHITE SWEEP PRESERVATION / {name} / 100%")
        board.paste(composite_on(sweep, color), (20, y))
    board.save(QA / "GF_UI_WHITE_SWEEP_BACKGROUNDS_100PCT.png")


def make_edge_forensic_qa(raw: Image.Image, full: Image.Image) -> None:
    samples = [
        ("FRAME TOP CENTER", (660, 22, 1010, 92)),
        ("FRAME BOTTOM CENTER", (660, 238, 1010, 308)),
        ("SPEAKER RIGHT EDGE", (1240, 305, 1365, 420)),
        ("ACTION HOLDER TOP RIGHT", (300, 320, 445, 470)),
    ]
    scale = 3
    column_widths = [max((b[2] - b[0]) * scale for _, b in samples)] * 3
    row_heights = [(b[3] - b[1]) * scale + 54 for _, b in samples]
    board = Image.new("RGB", (sum(column_widths) + 80, sum(row_heights) + 20), (24, 28, 34))
    draw = ImageDraw.Draw(board)
    x_positions = [20, 20 + column_widths[0] + 20, 20 + column_widths[0] * 2 + 40]
    y = 20
    for (name, box), row_h in zip(samples, row_heights):
        raw_crop = raw.crop(box).resize(((box[2] - box[0]) * scale, (box[3] - box[1]) * scale), Image.Resampling.NEAREST)
        rgba_crop = full.crop(box).resize(raw_crop.size, Image.Resampling.NEAREST)
        views = [
            ("RAW BAKED CHECKER", raw_crop.convert("RGB")),
            ("RECOVERED / DARK", composite_on(rgba_crop, (8, 18, 28, 255))),
            ("RECOVERED / MAGENTA", composite_on(rgba_crop, (255, 0, 255, 255))),
        ]
        for x, (view_name, view) in zip(x_positions, views):
            label(draw, (x, y), f"{name} / {view_name} / 300%")
            board.paste(view, (x, y + 22))
        y += row_h
    board.save(QA / "GF_UI_EDGE_FORENSIC_RAW_DARK_MAGENTA_300PCT.png")


def nine_slice(image: Image.Image, target: tuple[int, int], margins: tuple[int, int, int, int]) -> Image.Image:
    left, top, right, bottom = margins
    tw, th = target
    sw, sh = image.size
    if tw < left + right or th < top + bottom:
        raise ValueError("nine-slice target smaller than fixed margins")
    out = Image.new("RGBA", target, (0, 0, 0, 0))
    sx = (0, left, sw - right, sw)
    sy = (0, top, sh - bottom, sh)
    dx = (0, left, tw - right, tw)
    dy = (0, top, th - bottom, th)
    for row in range(3):
        for col in range(3):
            src = image.crop((sx[col], sy[row], sx[col + 1], sy[row + 1]))
            size = (dx[col + 1] - dx[col], dy[row + 1] - dy[row])
            if src.size != size:
                src = src.resize(size, Image.Resampling.LANCZOS)
            out.alpha_composite(src, (dx[col], dy[row]))
    return out


def make_nineslice_qa() -> None:
    frame = Image.open(DELIVERY / "gf_dialogue_frame_9slice_rgba.png").convert("RGBA")
    speaker = Image.open(DELIVERY / "gf_speaker_tab_9slice_rgba.png").convert("RGBA")
    samples = [
        ("LEFT ACTION FRAME 679x163", nine_slice(frame, (679, 163), (96, 64, 96, 64))),
        ("WIDE FRAME 1144x163", nine_slice(frame, (1144, 163), (96, 64, 96, 64))),
        ("SPEAKER TAB 210x64", nine_slice(speaker, (210, 64), (52, 20, 52, 20))),
        ("SPEAKER TAB 330x64", nine_slice(speaker, (330, 64), (52, 20, 52, 20))),
    ]
    width = 1220
    height = sum(im.height + 44 for _, im in samples) + 20
    board = Image.new("RGB", (width, height), (8, 18, 28))
    draw = ImageDraw.Draw(board)
    y = 30
    for name, im in samples:
        label(draw, (20, y - 18), name)
        board.paste(composite_on(im, (8, 18, 28, 255)), (20, y))
        y += im.height + 44
    board.save(QA / "GF_UI_NINESLICE_STRETCH_QA.png")


def topology_metrics(support: np.ndarray) -> dict:
    result = {}
    for region in REGIONS:
        x0, y0, x1, y1 = region.box
        local = support[y0:y1, x0:x1]
        fg = [c for c in components(local, 8) if c["area"] >= region.min_area]
        holes = [c for c in components(~local, 4) if not c["touches_edge"]]
        for c in fg + holes:
            c.pop("points", None)
        result[region.name] = {
            "foreground_connected_components": len(fg),
            "foreground": fg,
            "enclosed_transparent_components": len(holes),
            "largest_enclosed_transparent_area": max((h["area"] for h in holes), default=0),
            "enclosed_transparent": sorted(holes, key=lambda c: c["area"], reverse=True)[:12],
        }
    frame_window = support[85:250, 105:1565]
    holder_window = support[380:610, 110:355]
    result["safe_window_checks"] = {
        "dialogue_frame_center_alpha0_ratio": float((~frame_window).mean()),
        "action_holder_window_alpha0_ratio": float((~holder_window).mean()),
    }
    return result


def main() -> None:
    raw_image = Image.open(RAW)
    if raw_image.mode != "RGB":
        raise RuntimeError(f"expected retained RGB raw; got {raw_image.mode}")
    rgb = np.array(raw_image.convert("RGB"), dtype=np.uint8)
    background, checker_metrics = fit_background(rgb)
    residual = np.max(np.abs(rgb.astype(np.float32) - background), axis=2)
    variants, variant_stats = build_support_masks(residual, rgb)

    bg_iou = {}
    for i, a in enumerate(STRONG_THRESHOLDS):
        for b in STRONG_THRESHOLDS[i + 1 :]:
            value = iou(~variants[a], ~variants[b])
            bg_iou[f"{a}_vs_{b}"] = value
            if value < 0.999:
                raise RuntimeError(f"background mask IoU below hard gate: {a} vs {b} = {value}")

    support = variants[CANONICAL_STRONG_THRESHOLD]
    rgba, alpha_metrics = recover_rgba(rgb, background, residual, support)
    if alpha_metrics["opaque_rgb_changed_pixels"] != 0:
        raise RuntimeError("opaque RGB changed")
    if alpha_metrics["white_sweep_high_luma_preservation_ratio"] < 0.999:
        raise RuntimeError("white sweep high-luma preservation failed")
    if alpha_metrics["partial_non_sweep_bright_neutral_max_connected_area"] > 4:
        raise RuntimeError("continuous bright neutral partial-alpha fringe detected")

    rows, source_map = save_assets(rgba, support)
    write_manifest(rows)

    full = Image.fromarray(rgba, "RGBA")
    make_background_qa(full)
    make_component_qa(rows)
    make_sweep_qa()
    make_nineslice_qa()
    make_edge_forensic_qa(raw_image.convert("RGB"), full)

    topology = topology_metrics(support)
    metrics = {
        "status": "USER_REJECTED_HISTORY_ONLY_DIAGNOSTIC_TECHNICAL_RECOVERY",
        "original_call01_failure_receipt_remains_valid": True,
        "imagegen_calls_added": 0,
        "raw": {
            "path": str(Path("..") / "raw" / RAW.name),
            "sha256": image_sha(RAW),
            "mode": raw_image.mode,
            "width": raw_image.width,
            "height": raw_image.height,
        },
        "checker": checker_metrics,
        "mask": {
            "weak_threshold": WEAK_THRESHOLD,
            "strong_thresholds": list(STRONG_THRESHOLDS),
            "canonical_strong_threshold": CANONICAL_STRONG_THRESHOLD,
            "background_mask_iou": bg_iou,
            "all_background_mask_iou_ge_0_999": all(v >= 0.999 for v in bg_iou.values()),
            "variant_stats": variant_stats,
        },
        "alpha": alpha_metrics,
        "topology": topology,
        "source_map": source_map,
        "delivery_rows": rows,
        "gates": {
            "test_only_consumption_allowed": False,
            "runtime_allowed": False,
            "runtime_handoff": "none",
            "user_visual_acceptance": False,
            "godot_modified": False,
            "canon_modified": False,
        },
    }
    (RECEIPTS / "deterministic-salvage-metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    hash_paths = [HERE / "asset-manifest.tsv"] + [HERE / row["path"] for row in rows]
    hash_paths += sorted(QA.glob("*.png"))
    hash_lines = [f"{image_sha(path)}  {path.relative_to(HERE)}" for path in hash_paths]
    (RECEIPTS / "delivery-hashes.sha256").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": metrics["status"],
        "background_mask_iou": bg_iou,
        "alpha": alpha_metrics,
        "safe_window_checks": topology["safe_window_checks"],
        "deliveries": [{"asset_id": r["asset_id"], "path": r["path"], "sha256": r["sha256"]} for r in rows],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
