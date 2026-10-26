#!/usr/bin/env python3
"""Deterministically reconstruct the pre-impact (cold) A17 shield front.

This utility is deliberately limited to the user-accepted A17 front master.  It
does not call ImageGen and does not read any later shield/action candidate.  A
small, reproducible scar mask is built from a manually locked trajectory plus
red-heat evidence.  Clean pixels are cloned from unscarred areas of the same
panel family with fixed affine offsets.  Pixels outside the saved mask and the
complete source alpha channel are preserved byte-for-byte.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = (
    ROOT
    / "derived-front-rear-sprites-v1"
    / "masters"
    / "A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png"
)
EXPECTED_SOURCE_SHA256 = (
    "8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47"
)

OUT = ROOT / "failed-cold-front-deterministic-experiments-do-not-use"
MASTER_DIR = OUT / "masters"
MAP_DIR = OUT / "map-candidates"
MASK_DIR = OUT / "masks"
QA_DIR = OUT / "qa"

MASTER_NAME = "FAILED_DO_NOT_USE_A17_SHIELD_COLD_FRONT_EXPERIMENT_768x1152.png"
MAP_NAME = "FAILED_DO_NOT_USE_A17_SHIELD_COLD_FRONT_EXPERIMENT_256x256.png"
MASK_NAME = "A17_SHIELD_FOURTH_HOT_SCAR_AND_HALO_MASK_768x1152.png"
KEEP_NAME = "A17_SHIELD_THREE_OLD_WHITE_SCARS_PRESERVE_MASK_768x1152.png"

MAP_CANVAS = (256, 256)
MAP_LONG_AXIS_PX = 208
MAP_GROUND_TIP_Y = 224


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    """Circular-ish deterministic dilation through Pillow's square max filter."""
    if radius <= 0:
        return mask.copy()
    image = Image.fromarray(mask.astype(np.uint8) * 255, mode="L")
    return np.asarray(image.filter(ImageFilter.MaxFilter(radius * 2 + 1))) > 0


def erode(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask.copy()
    image = Image.fromarray(mask.astype(np.uint8) * 255, mode="L")
    return np.asarray(image.filter(ImageFilter.MinFilter(radius * 2 + 1))) > 0


def polygon_mask(size: tuple[int, int], points: list[tuple[int, int]]) -> np.ndarray:
    image = Image.new("L", size, 0)
    ImageDraw.Draw(image).polygon(points, fill=255)
    return np.asarray(image) > 0


def polyline_capsule(
    size: tuple[int, int], points: list[tuple[int, int]], radius: float
) -> np.ndarray:
    width, height = size
    yy, xx = np.mgrid[:height, :width]
    minimum = np.full((height, width), np.inf, dtype=np.float32)
    for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
        vx = float(x1 - x0)
        vy = float(y1 - y0)
        denom = vx * vx + vy * vy
        t = np.clip(((xx - x0) * vx + (yy - y0) * vy) / denom, 0.0, 1.0)
        px = x0 + t * vx
        py = y0 + t * vy
        minimum = np.minimum(minimum, (xx - px) ** 2 + (yy - py) ** 2)
    return minimum <= radius * radius


def components_touching(mask: np.ndarray, seed: np.ndarray) -> np.ndarray:
    """Return 8-connected mask components intersecting seed."""
    height, width = mask.shape
    visited = np.zeros_like(mask)
    stack = [(int(y), int(x)) for y, x in zip(*np.where(mask & seed))]
    for y, x in stack:
        visited[y, x] = True
    cursor = 0
    while cursor < len(stack):
        y, x = stack[cursor]
        cursor += 1
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                ny, nx = y + dy, x + dx
                if (
                    0 <= ny < height
                    and 0 <= nx < width
                    and mask[ny, nx]
                    and not visited[ny, nx]
                ):
                    visited[ny, nx] = True
                    stack.append((ny, nx))
    return visited


def resize_rgba_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    array = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = array[:, :, 3:4] / 255.0
    premultiplied = np.concatenate((array[:, :, :3] * alpha, array[:, :, 3:4]), axis=2)
    premultiplied_u8 = np.clip(np.rint(premultiplied), 0, 255).astype(np.uint8)
    resized = np.asarray(
        Image.fromarray(premultiplied_u8, mode="RGBA").resize(size, Image.Resampling.LANCZOS),
        dtype=np.float32,
    )
    out_alpha = resized[:, :, 3:4]
    safe_alpha = np.where(out_alpha > 0, out_alpha / 255.0, 1.0)
    rgb = np.where(out_alpha > 0, resized[:, :, :3] / safe_alpha, 0.0)
    return Image.fromarray(
        np.clip(np.rint(np.concatenate((rgb, out_alpha), axis=2)), 0, 255).astype(np.uint8),
        mode="RGBA",
    )


def build_old_scar_keep(source: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    """Segment only visible neutral/white pixels inside the three old-scar corridors."""
    height, width = source.shape[:2]
    yy, xx = np.mgrid[:height, :width]
    rgb = source[:, :, :3].astype(np.int16)
    high = rgb.max(axis=2)
    low = rgb.min(axis=2)
    neutral_bright = (high >= 78) & ((high - low) <= 62)

    upper = (xx >= 80) & (xx <= 600) & (np.abs(yy - (198.337 + 0.33833 * xx)) <= 18)
    middle = (xx >= 65) & (xx <= 410) & (np.abs(yy - (519.145 - 0.02563 * xx)) <= 16)
    lower = (xx >= 100) & (xx <= 610) & (np.abs(yy - (839.250 - 0.29569 * xx)) <= 20)
    keep = dilate(neutral_bright & (upper | middle | lower), 2)
    keep &= source[:, :, 3] > 0
    return keep, {
        "segmentation": "neutral-bright pixels in three locked linear corridors, dilated 2 px",
        "neutral_bright_rule": "max(rgb)>=78 and chroma<=62",
        "upper_corridor": "x=80..600; abs(y-(198.337+0.33833*x))<=18",
        "middle_corridor": "x=65..410; abs(y-(519.145-0.02563*x))<=16",
        "lower_corridor": "x=100..610; abs(y-(839.250-0.29569*x))<=20",
        "pixels": int(keep.sum()),
    }


def build_hot_scar_mask(
    source: np.ndarray, old_scar_keep: np.ndarray
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    """Build inner correction evidence and final changed-pixel mask."""
    height, width = source.shape[:2]
    yy, xx = np.mgrid[:height, :width]
    rgb = source[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    envelope_points = [
        (205, 702), (220, 654), (246, 621), (284, 596), (326, 556),
        (372, 526), (416, 493), (458, 452), (506, 414), (552, 391),
        (598, 394), (628, 414), (638, 446), (628, 477), (600, 503),
        (564, 532), (520, 554), (470, 576), (424, 600), (380, 621),
        (334, 644), (288, 663), (248, 685), (220, 708),
    ]
    envelope = polygon_mask((width, height), envelope_points)
    axis_points = [
        (216, 680), (248, 643), (289, 614), (336, 587), (382, 566),
        (431, 540), (482, 512), (532, 484), (577, 464), (611, 443),
    ]
    emit = polyline_capsule((width, height), axis_points, 18.0)
    emit &= envelope

    red_light = (red >= 105) & ((red - green) >= 35) & ((red - blue) >= 25)
    luminance = (red * 54 + green * 183 + blue * 19) // 256
    warm_soot = (
        (luminance <= 85)
        & (red >= 22)
        & (red <= 120)
        & ((red - green) >= 4)
        & ((red - blue) >= 3)
    )
    evidence = (red_light | warm_soot) & envelope & (source[:, :, 3] > 0)
    connected = components_touching(evidence | emit, emit)
    soot = connected & evidence
    soot = dilate(erode(dilate(soot, 3), 3), 2)

    inner = (emit | soot) & envelope & (source[:, :, 3] > 0)
    inner &= ~old_scar_keep
    outer = dilate(inner, 5) & dilate(envelope, 3) & (source[:, :, 3] > 0)
    outer &= ~old_scar_keep
    return inner, outer, {
        "trajectory": "polyline through ten locked high-heat-axis points; least-squares reference y=-0.50920*x+759.520",
        "emit_capsule_radius_px": 18,
        "red_light_rule": "r>=105; r-g>=35; r-b>=25",
        "warm_soot_rule": "luma<=85; 22<=r<=120; r-g>=4; r-b>=3",
        "soot_topology": "only evidence 8-connected to emit; fixed 3 px close then 2 px dilate",
        "outer_seam_margin_px": 5,
        "inner_pixels": int(inner.sum()),
        "outer_changed_pixel_cap": int(outer.sum()),
        "old_scar_keep_intersection_pixels": int((outer & old_scar_keep).sum()),
    }


def clone_sample(source: np.ndarray, sx: np.ndarray, sy: np.ndarray) -> np.ndarray:
    height, width = source.shape[:2]
    ix = np.clip(np.rint(sx), 0, width - 1).astype(np.int32)
    iy = np.clip(np.rint(sy), 0, height - 1).astype(np.int32)
    return source[iy, ix, :3].astype(np.float32)


def reconstruct(
    source: np.ndarray,
    inner: np.ndarray,
    outer: np.ndarray,
    old_scar_keep: np.ndarray,
) -> np.ndarray:
    """Clone fixed donors from the same structural panel family."""
    height, width = source.shape[:2]
    yy, xx = np.mgrid[:height, :width]
    # These labels follow the five surfaces crossed by the scar.  Small overlaps
    # are resolved left-to-right so a donor never crosses the central spine or
    # the outer off-white/rim seams.
    right_ivory_left = 585.0 - 0.10 * (yy - 400.0)
    rim_left = 643.0 - 0.08 * (yy - 400.0)
    labels = np.zeros((height, width), dtype=np.uint8)
    labels[xx < 245] = 1                       # left ivory/blue flank
    labels[(xx >= 245) & (xx < 345)] = 2      # central steel spine
    labels[(xx >= 345) & (xx < 414)] = 3      # central-right ivory rib
    labels[(xx >= 414) & (xx < right_ivory_left)] = 4  # right navy field
    labels[(xx >= right_ivory_left) & (xx < rim_left)] = 5  # outer ivory rib
    labels[xx >= rim_left] = 6                 # thick perimeter frame

    def donor_offsets(prefer_down: bool) -> list[tuple[int, int]]:
        preferred_sign = 1 if prefer_down else -1
        offsets: list[tuple[int, int]] = []
        # First choices retain a coherent vertical/normal translation.
        for distance in range(72, 241, 16):
            for dx in (0, -8, 8, -16, 16, -24, 24, -32, 32):
                offsets.append((dx, preferred_sign * distance))
        # Opposite side and tangent-assisted fallbacks remain same-panel and
        # deterministic; they are used only when old scars occupy the preferred
        # donor strip.
        for distance in range(72, 241, 16):
            for dx in (0, -8, 8, -16, 16, -24, 24, -40, 40, -72, 72):
                offsets.append((dx, -preferred_sign * distance))
        return offsets

    candidates: dict[int, list[tuple[int, int]]] = {
        1: donor_offsets(False),
        2: donor_offsets(False),
        3: donor_offsets(False),
        4: donor_offsets(True),
        5: donor_offsets(True),
        6: donor_offsets(True),
    }

    patch = source[:, :, :3].astype(np.float32).copy()
    target_y, target_x = np.where(outer)
    assigned = np.zeros(target_y.shape, dtype=np.bool_)

    # A donor may not come from any old-scar corridor, even if the local white
    # pixels did not meet the visible-scar threshold.
    upper_corridor = (xx >= 80) & (xx <= 600) & (np.abs(yy - (198.337 + 0.33833 * xx)) <= 25)
    middle_corridor = (xx >= 65) & (xx <= 410) & (np.abs(yy - (519.145 - 0.02563 * xx)) <= 23)
    lower_corridor = (xx >= 100) & (xx <= 610) & (np.abs(yy - (839.250 - 0.29569 * xx)) <= 28)
    donor_forbidden = outer | upper_corridor | middle_corridor | lower_corridor | (source[:, :, 3] == 0)

    for label in range(1, 7):
        label_targets = np.where(labels[target_y, target_x] == label)[0]
        for dx, dy in candidates[label]:
            pending = label_targets[~assigned[label_targets]]
            if pending.size == 0:
                break
            sy = np.clip(target_y[pending] + dy, 0, height - 1)
            sx = np.clip(target_x[pending] + dx, 0, width - 1)
            valid = (~donor_forbidden[sy, sx]) & (labels[sy, sx] == label)
            chosen = pending[valid]
            if chosen.size:
                cy = np.clip(target_y[chosen] + dy, 0, height - 1)
                cx = np.clip(target_x[chosen] + dx, 0, width - 1)
                patch[target_y[chosen], target_x[chosen]] = source[cy, cx, :3]
                assigned[chosen] = True

    if not assigned.all():
        # Fail closed instead of allowing a cross-panel or scar donor.
        missing = int((~assigned).sum())
        raise SystemExit(f"FAIL_STOP: {missing} masked pixels have no same-panel clean donor")

    # Full replacement for evidenced heat; 14 px internal feather only at the
    # already-clean outer margin.  Clipping by outer guarantees byte identity
    # everywhere else.
    inner_image = Image.fromarray(inner.astype(np.uint8) * 255, mode="L")
    feather = np.asarray(inner_image.filter(ImageFilter.GaussianBlur(8.0)), dtype=np.float32) / 255.0
    weight = np.where(inner, 1.0, feather)
    weight = np.where(outer, weight, 0.0)
    weight = np.clip(weight, 0.0, 1.0)[:, :, None]

    out = source.copy()
    blended = np.rint(source[:, :, :3].astype(np.float32) * (1.0 - weight) + patch * weight)
    out[:, :, :3] = np.clip(blended, 0, 255).astype(np.uint8)
    out[:, :, 3] = source[:, :, 3]
    return out


def normalized_map_candidate(master: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    rgba = np.asarray(master.convert("RGBA"))
    ys, xs = np.where(rgba[:, :, 3] > 0)
    bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    crop = master.crop(tuple(bbox))
    scale = MAP_LONG_AXIS_PX / float(crop.height)
    resized_size = (max(1, round(crop.width * scale)), MAP_LONG_AXIS_PX)
    resized = resize_rgba_premultiplied(crop, resized_size)
    canvas = Image.new("RGBA", MAP_CANVAS, (0, 0, 0, 0))
    offset = ((MAP_CANVAS[0] - resized.width) // 2, MAP_GROUND_TIP_Y - resized.height)
    canvas.alpha_composite(resized, offset)
    out_alpha = np.asarray(canvas)[:, :, 3]
    out_y, out_x = np.where(out_alpha > 0)
    return canvas, {
        "canvas_size": list(MAP_CANVAS),
        "source_alpha_bbox_xyxy": bbox,
        "normalized_subject_size_px": list(resized.size),
        "copy_offset_px": list(offset),
        "alpha_bbox_xyxy": [
            int(out_x.min()), int(out_y.min()), int(out_x.max()) + 1, int(out_y.max()) + 1
        ],
        "ground_tip_pivot_px": [128, MAP_GROUND_TIP_Y],
        "nominal_sprite_scale": [1.0, 1.0],
        "resample": "premultiplied_alpha_lanczos",
    }


def checker(size: tuple[int, int], cell: int, dark: bool) -> Image.Image:
    a, b = ((26, 30, 38), (48, 54, 64)) if dark else ((238, 239, 241), (207, 211, 217))
    image = Image.new("RGB", size, a)
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if ((x // cell) + (y // cell)) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=b)
    return image


def alpha_composite_rgb(background: Image.Image, foreground: Image.Image) -> Image.Image:
    out = background.convert("RGBA")
    out.alpha_composite(foreground.convert("RGBA"))
    return out.convert("RGB")


def make_qa(master: Image.Image, mask: np.ndarray, keep: np.ndarray) -> dict[str, Path]:
    outputs: dict[str, Path] = {}
    dark = alpha_composite_rgb(checker(master.size, 32, True), master)
    light = alpha_composite_rgb(checker(master.size, 32, False), master)
    qa100 = Image.new("RGB", (master.width * 2, master.height), (16, 18, 22))
    qa100.paste(dark, (0, 0))
    qa100.paste(light, (master.width, 0))
    qa100_path = QA_DIR / "A17_SHIELD_COLD_FRONT_DARK_LIGHT_QA_100PCT.png"
    qa100.save(qa100_path)
    outputs["dark_light_100pct"] = qa100_path

    half = resize_rgba_premultiplied(master, (master.width // 2, master.height // 2))
    dark_half = alpha_composite_rgb(checker(half.size, 16, True), half)
    light_half = alpha_composite_rgb(checker(half.size, 16, False), half)
    qa50 = Image.new("RGB", (half.width * 2, half.height + 72), (22, 24, 29))
    qa50.paste(dark_half, (0, 72))
    qa50.paste(light_half, (half.width, 72))
    draw = ImageDraw.Draw(qa50)
    draw.text((18, 15), "A17 COLD FRONT / 50% / three old white scars only", font=font(24, True), fill=(242, 244, 248))
    draw.text((18, 43), "Candidate review only - no Godot, Runtime or Canon binding", font=font(16), fill=(178, 185, 196))
    qa50_path = QA_DIR / "A17_SHIELD_COLD_FRONT_DARK_LIGHT_QA_50PCT.png"
    qa50.save(qa50_path)
    outputs["dark_light_50pct"] = qa50_path

    overlay = np.asarray(master.convert("RGBA")).copy()
    # Magenta = changed-pixel cap; cyan = protected old scars.
    tint = overlay[:, :, :3].astype(np.float32)
    tint[mask] = tint[mask] * 0.25 + np.array([255.0, 0.0, 210.0]) * 0.75
    tint[keep] = tint[keep] * 0.25 + np.array([0.0, 245.0, 255.0]) * 0.75
    overlay[:, :, :3] = np.clip(np.rint(tint), 0, 255).astype(np.uint8)
    overlay_image = Image.fromarray(overlay, mode="RGBA")
    overlay_path = QA_DIR / "A17_SHIELD_COLD_FRONT_MASK_AND_OLD_SCAR_PRESERVE_OVERLAY.png"
    overlay_image.save(overlay_path)
    outputs["mask_overlay"] = overlay_path
    return outputs


def main() -> None:
    if sha256(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise SystemExit("FAIL_STOP: A17 accepted source SHA mismatch")

    for directory in (MASTER_DIR, MAP_DIR, MASK_DIR, QA_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    source_image = Image.open(SOURCE).convert("RGBA")
    if source_image.size != (768, 1152):
        raise SystemExit(f"FAIL_STOP: expected 768x1152, got {source_image.size}")
    source = np.asarray(source_image).copy()

    old_keep, old_keep_meta = build_old_scar_keep(source)
    inner, outer, mask_meta = build_hot_scar_mask(source, old_keep)
    output = reconstruct(source, inner, outer, old_keep)

    outside_equal = bool(np.array_equal(output[~outer], source[~outer]))
    alpha_equal = bool(np.array_equal(output[:, :, 3], source[:, :, 3]))
    changed = np.any(output != source, axis=2)
    changed_outside = int((changed & ~outer).sum())
    old_scar_changed = int((changed & old_keep).sum())
    if not outside_equal or not alpha_equal or changed_outside or old_scar_changed:
        raise SystemExit(
            "FAIL_STOP: deterministic isolation gate failed "
            f"outside_equal={outside_equal} alpha_equal={alpha_equal} "
            f"changed_outside={changed_outside} old_scar_changed={old_scar_changed}"
        )

    master = Image.fromarray(output, mode="RGBA")
    master_path = MASTER_DIR / MASTER_NAME
    master.save(master_path)
    Image.fromarray(outer.astype(np.uint8) * 255, mode="L").save(MASK_DIR / MASK_NAME)
    Image.fromarray(old_keep.astype(np.uint8) * 255, mode="L").save(MASK_DIR / KEEP_NAME)

    map_candidate, map_meta = normalized_map_candidate(master)
    map_path = MAP_DIR / MAP_NAME
    map_candidate.save(map_path)
    qa_paths = make_qa(master, outer, old_keep)

    # Vivid red/heat signature audit in the locked fourth-scar ROI.  Ordinary
    # ochre paint chips are excluded by the high-red/high-dominance rule.
    yy, xx = np.mgrid[:source.shape[0], :source.shape[1]]
    center_y = 818.0 - 0.56 * xx
    scar_roi = (xx >= 165) & (xx <= 670) & (yy >= center_y - 105) & (yy <= center_y + 85)
    out_rgb = output[:, :, :3].astype(np.int16)
    vivid_red = (
        scar_roi
        & (out_rgb[:, :, 0] >= 175)
        & (out_rgb[:, :, 0] >= out_rgb[:, :, 1] * 1.55 + 15)
        & (out_rgb[:, :, 0] >= out_rgb[:, :, 2] * 1.35 + 15)
    )

    alpha = output[:, :, 3]
    ys, xs = np.where(alpha > 0)
    metadata = {
        "schema": "a17-cold-front-deterministic-v1",
        "status": "FAIL_STOP_VISUAL_GATE_DO_NOT_USE",
        "user_accepted": False,
        "runtime": False,
        "canon": False,
        "godot_bound": False,
        "imagegen_calls": 0,
        "positive_source_policy": "accepted front master plus its derivation receipt/metadata only",
        "forbidden_inputs": [
            "all R2/R3 failed cold outputs",
            "all ImageGen cold edits",
            "all Guardian Z action composites",
        ],
        "source": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": sha256(SOURCE),
            "size": list(source_image.size),
            "mode": source_image.mode,
        },
        "method": {
            "name": "locked scar trajectory + red-heat evidence + same-panel deterministic clone",
            "mask": mask_meta,
            "old_scar_preservation": old_keep_meta,
            "clone_regions": [
                {"x": "<414", "clean_side": "above", "mapping": "reflect across per-column mask top"},
                {"x": ">=414", "clean_side": "below", "mapping": "reflect across per-column mask bottom"},
            ],
            "source_rejection": "walk outward by 4 px if lookup hits correction mask, alpha zero, or old-scar preserve mask",
            "taper_follow": "x'=322+(x-322)*clip(1-0.00038*(y'-y),0.88,1.12)",
            "feather": "inner=1.0; 8 px Gaussian only inside the saved outer mask",
        },
        "hard_gates": {
            "source_alpha_byte_identical": alpha_equal,
            "outside_saved_mask_rgba_byte_identical": outside_equal,
            "changed_pixels_outside_saved_mask": changed_outside,
            "changed_pixels_intersecting_three_old_scar_keep_mask": old_scar_changed,
            "saved_mask_intersecting_three_old_scar_keep_mask": int((outer & old_keep).sum()),
            "source_and_output_alpha_bbox_equal": [
                int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
            ],
            "output_size": list(master.size),
            "output_mode": master.mode,
            "vivid_red_heat_pixels_in_locked_scar_roi": int(vivid_red.sum()),
            "manual_visual_gate": "FAIL: repeated donor striping, central-spine/panel discontinuity, residual red heat",
        },
        "outputs": {
            "master": {"path": str(master_path.relative_to(ROOT)), "sha256": sha256(master_path)},
            "map_candidate": {
                "path": str(map_path.relative_to(ROOT)),
                "sha256": sha256(map_path),
                **map_meta,
            },
            "hot_scar_mask": {
                "path": str((MASK_DIR / MASK_NAME).relative_to(ROOT)),
                "sha256": sha256(MASK_DIR / MASK_NAME),
                "pixels": int(outer.sum()),
            },
            "old_scar_preserve_mask": {
                "path": str((MASK_DIR / KEEP_NAME).relative_to(ROOT)),
                "sha256": sha256(MASK_DIR / KEEP_NAME),
                "pixels": int(old_keep.sum()),
            },
            "qa": {
                key: {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
                for key, path in qa_paths.items()
            },
        },
    }
    metadata_path = OUT / "A17_SHIELD_COLD_FRONT_DERIVATION_METADATA.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata["hard_gates"], ensure_ascii=False, indent=2))
    raise SystemExit(
        "FAIL_STOP: deterministic reconstruction did not pass the visual gate; "
        "outputs are quarantined and must not be used as Candidate inputs"
    )


if __name__ == "__main__":
    main()
