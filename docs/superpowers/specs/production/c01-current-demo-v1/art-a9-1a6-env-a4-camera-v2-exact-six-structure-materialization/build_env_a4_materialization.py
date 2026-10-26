#!/usr/bin/env python3
"""Task122 ENV-A4 locked-geometry materialization.

Pilot mode authors NW_BLOCK only.  It never copies donor contours: ENV-A1
swatches contribute color/roughness statistics to deterministic, directionless
noise fields.  Delivery alpha is copied byte-for-byte from the Task121 source.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parent
PROJECT = Path(__file__).resolve().parents[6]
C01 = ROOT.parent
A3 = C01 / "art-a9-1a6-env-a3-camera-v2-exact-structure-pilot/six-structure"
A1 = C01 / "art-a9-1a6-env-a1-modular-tactical-environment-kit-master"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"

PILOT = ROOT / "pilot"
PILOT_DELIVERY = PILOT / "delivery"
PILOT_QA = PILOT / "qa"
PILOT_RECEIPTS = PILOT / "receipts"

DONORS = {
    "wet_asphalt": A1 / "intermediate/materials/GROUND_WET_ASPHALT_SWATCH_RGBA.png",
    "apron_paving": A1 / "intermediate/materials/GROUND_APRON_PAVING_SWATCH_RGBA.png",
    "curb_drainage": A1 / "intermediate/materials/GROUND_CURB_DRAINAGE_SWATCH_RGBA.png",
    "road_language": A1 / "intermediate/materials/GROUND_ROAD_LANGUAGE_SWATCH_RGBA.png",
}

OBJECTS = {
    "NW_BLOCK": {"grid_rect": [1, 0, 7, 5], "height": 90, "base": "315766", "amber": True},
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def parse_ints(value: str) -> list[int]:
    return [int(item) for item in value.split(",")]


def rgb(hex_value: str) -> tuple[int, int, int]:
    value = hex_value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def mix(a, b, amount):
    return tuple(round(a[index] * (1.0 - amount) + b[index] * amount) for index in range(3))


def scale_color(color, factor):
    return tuple(max(0, min(255, round(channel * factor))) for channel in color)


def font(size: int, bold: bool = False):
    choices = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in choices:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_registration():
    with REGISTRATION.open(encoding="utf-8", newline="") as handle:
        return {
            row["object_id"]: row
            for row in csv.DictReader(handle, delimiter="\t")
            if row["record_type"] == "STRUCTURE"
        }


def project_local(x: float, y: float, bounds: list[int]):
    return (x - y) * 40 - bounds[0], (x + y) * 24 - bounds[1]


def footprint(grid_rect, bounds, inset=0.0):
    x, y, w, h = grid_rect
    x0, y0 = x - 0.5 + inset, y - 0.5 + inset
    x1, y1 = x + w - 0.5 - inset, y + h - 0.5 - inset
    return [
        project_local(x0, y0, bounds),
        project_local(x1, y0, bounds),
        project_local(x1, y1, bounds),
        project_local(x0, y1, bounds),
    ]


def shifted(points, height):
    return [(x, y - height) for x, y in points]


def polygon_mask(size, points):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon([(round(x), round(y)) for x, y in points], fill=255)
    return mask


def clipped_mask(mask, alpha):
    return ImageChops.multiply(mask, alpha)


def donor_statistics():
    stats = {}
    samples = []
    for donor_id, path in DONORS.items():
        image = Image.open(path).convert("RGB")
        stat = ImageStat.Stat(image)
        mean = tuple(round(value, 3) for value in stat.mean)
        std = tuple(round(value, 3) for value in stat.stddev)
        stats[donor_id] = {
            "path": str(path.relative_to(PROJECT)),
            "sha256": sha(path),
            "mean_rgb": mean,
            "stddev_rgb": std,
            "pixel_use": "statistics_only_no_contours_no_lines",
        }
        if donor_id in {"wet_asphalt", "apron_paving"}:
            samples.append(mean)
    neutral = tuple(round(sum(item[channel] for item in samples) / len(samples)) for channel in range(3))
    return stats, neutral


def value_noise(size, seed, coarse, amplitude):
    rng = random.Random(seed)
    grid_w = max(2, math.ceil(size[0] / coarse) + 2)
    grid_h = max(2, math.ceil(size[1] / coarse) + 2)
    grid = Image.new("L", (grid_w, grid_h))
    grid.putdata([max(0, min(255, 128 + rng.randint(-amplitude, amplitude))) for _ in range(grid_w * grid_h)])
    return grid.resize(size, Image.Resampling.BICUBIC)


def micro_noise(size, seed, amplitude):
    rng = random.Random(seed)
    image = Image.new("L", size)
    image.putdata([max(0, min(255, 128 + rng.randint(-amplitude, amplitude))) for _ in range(size[0] * size[1])])
    return image.filter(ImageFilter.GaussianBlur(0.45))


def material_field(size, base_color, seed, donor_neutral, low_amp=10, micro_amp=6):
    # Donor controls the cool industrial bias; spatial donor features are discarded.
    donor_tint = mix(base_color, donor_neutral, 0.10)
    base = Image.new("RGB", size, donor_tint)
    low = value_noise(size, seed, 34, low_amp)
    micro = micro_noise(size, seed + 997, micro_amp)
    # Apply fields as signed luma deltas around 128.  Blending against the
    # neutral field would wash the contract palette toward grey.
    low_rgb = Image.merge("RGB", (low, low, low))
    base = ImageChops.add(base, low_rgb, scale=1.0, offset=-128)
    micro_rgb = Image.merge("RGB", (micro, micro, micro))
    return ImageChops.add(base, micro_rgb, scale=1.0, offset=-128)


def apply_inside(destination, material, mask):
    destination.paste(material, (0, 0), mask)


def preserve_exact_detail(destination, source_rgb, alpha, strength=0.34):
    # Retain only exact Task121 linework/high-frequency structure, not its flat fills.
    grey = source_rgb.convert("L")
    broad = grey.filter(ImageFilter.GaussianBlur(4.0))
    detail = ImageChops.subtract(grey, broad, scale=1.0, offset=128)
    detail = detail.point(lambda value: max(0, min(255, round(128 + (value - 128) * strength))))
    detail_rgb = Image.merge("RGB", (detail, detail, detail))
    detailed = ImageChops.add(destination, detail_rgb, scale=1.0, offset=-128)
    destination.paste(detailed, (0, 0), alpha)


def restore_amber_identity(destination, source_rgb, alpha):
    r, g, b = source_rgb.split()
    # Isolate the already-authored Task121 amber slit; no new accent geometry.
    mask = Image.new("L", source_rgb.size, 0)
    source_pixels = list(source_rgb.getdata())
    mask.putdata([255 if red > 120 and red > green * 1.25 and green > blue * 1.05 else 0 for red, green, blue in source_pixels])
    mask = ImageChops.multiply(mask, alpha)
    amber = Image.new("RGB", source_rgb.size, (178, 109, 43))
    destination.paste(amber, (0, 0), mask)


def add_internal_wear(image, mask, seed, amber=False):
    rng = random.Random(seed)
    wear = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(wear)
    # Short exact-axis wet scuffs; never introduce an alternative camera angle.
    axes = ((5, 3), (-5, 3), (0, 1))
    for index in range(24):
        x = rng.randrange(12, max(13, image.width - 12))
        y = rng.randrange(12, max(13, image.height - 12))
        dx, dy = axes[index % len(axes)]
        length = rng.randrange(1, 4)
        color = (170, 195, 202, rng.randrange(12, 29)) if index % 3 else (5, 16, 21, rng.randrange(18, 34))
        draw.line((x, y, x + dx * length, y + dy * length), fill=color, width=1)
    wear.putalpha(ImageChops.multiply(wear.getchannel("A"), mask))
    image.alpha_composite(wear)

    if amber:
        # Existing identity cue is recolored only; no new silhouette or semantic sign.
        pass


def recolor_foundation(source, base_color, seed, donor_neutral):
    alpha = source.getchannel("A")
    result_rgb = material_field(source.size, scale_color(base_color, 0.72), seed, donor_neutral, 8, 4)
    preserve_exact_detail(result_rgb, source.convert("RGB"), alpha, 0.24)
    result = result_rgb.convert("RGBA")
    result.putalpha(alpha.copy())
    add_internal_wear(result, alpha, seed + 41)
    result.putalpha(alpha.copy())
    return result


def recolor_occluder(source, spec, row, seed, donor_neutral):
    alpha = source.getchannel("A")
    bounds = parse_ints(row["visual_bounds_raw"])
    grid_rect = spec["grid_rect"]
    base = footprint(grid_rect, bounds, inset=0.38 if grid_rect[3] >= 4 else 0.28)
    roof = shifted(base, spec["height"])
    a, b, c, d = base
    ar, br, cr, dr = roof
    roof_mask = clipped_mask(polygon_mask(source.size, [ar, br, cr, dr]), alpha)
    light_wall_mask = clipped_mask(polygon_mask(source.size, [br, cr, c, b]), alpha)
    dark_wall_mask = clipped_mask(polygon_mask(source.size, [dr, cr, c, d]), alpha)

    base_color = rgb(spec["base"])
    result_rgb = Image.new("RGB", source.size, scale_color(base_color, 0.62))
    apply_inside(result_rgb, material_field(source.size, base_color, seed, donor_neutral), roof_mask)
    apply_inside(result_rgb, material_field(source.size, scale_color(base_color, 0.80), seed + 11, donor_neutral), light_wall_mask)
    apply_inside(result_rgb, material_field(source.size, scale_color(base_color, 0.62), seed + 23, donor_neutral), dark_wall_mask)

    # Exact Task121 seams, panels, hatch and outline stay the only structural linework.
    preserve_exact_detail(result_rgb, source.convert("RGB"), alpha, 0.26)
    restore_amber_identity(result_rgb, source.convert("RGB"), alpha)
    result = result_rgb.convert("RGBA")
    result.putalpha(alpha.copy())
    add_internal_wear(result, alpha, seed + 53, spec["amber"])
    result.putalpha(alpha.copy())
    return result, {"roof": roof_mask, "light_wall": light_wall_mask, "dark_wall": dark_wall_mask}


def checker(size):
    image = Image.new("RGBA", size, "#071219")
    draw = ImageDraw.Draw(image)
    cell = 28
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            fill = "#0c222b" if (x // cell + y // cell) % 2 == 0 else "#102d37"
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=fill)
    return image


def combined(foundation, occluder, occluder_alpha=1.0):
    output = foundation.copy()
    layer = occluder.copy()
    layer.putalpha(layer.getchannel("A").point(lambda value: round(value * occluder_alpha)))
    output.alpha_composite(layer)
    return output


def pilot_boards(object_id, source_foundation, source_occluder, foundation, occluder):
    material = combined(foundation, occluder)
    source = combined(source_foundation, source_occluder)

    stage = checker((1120, 620))
    draw = ImageDraw.Draw(stage)
    draw.rectangle((0, 0, 1120, 82), fill="#071219")
    draw.text((24, 17), "NW_BLOCK | CAMERA V2 LOCKED MATERIAL PILOT", font=font(27, True), fill="#f0f7f8")
    draw.text((24, 52), "same alpha / same pivot / +/-30.96 deg / ENV-A1 statistics only", font=font(16), fill="#8fc5ce")

    for index, (label, asset) in enumerate((("TASK121 GEOMETRY", source), ("TASK122 MATERIAL", material))):
        x0 = 35 + index * 545
        draw.text((x0, 96), label, font=font(19, True), fill="#dcebed")
        scale = min(500 / asset.width, 420 / asset.height)
        shown = asset.resize((round(asset.width * scale), round(asset.height * scale)), Image.Resampling.LANCZOS)
        stage.alpha_composite(shown, (x0 + (500 - shown.width) // 2, 140 + (410 - shown.height) // 2))
    path100 = PILOT_QA / "NW_BLOCK_MATERIAL_PILOT_100_PERCENT_1120x620.png"
    stage.save(path100)
    path50 = PILOT_QA / "NW_BLOCK_MATERIAL_PILOT_50_PERCENT_560x310.png"
    stage.resize((560, 310), Image.Resampling.LANCZOS).save(path50)
    return path100, path50


def build_pilot():
    for directory in (PILOT_DELIVERY, PILOT_QA, PILOT_RECEIPTS):
        directory.mkdir(parents=True, exist_ok=True)

    rows = load_registration()
    donor_stats, donor_neutral = donor_statistics()
    object_id = "NW_BLOCK"
    spec = OBJECTS[object_id]
    row = rows[object_id]
    assert parse_ints(row["visual_bounds_raw"])[2:] == [480, 378]
    assert int(row["world_height_px"]) == spec["height"]

    source_foundation_path = A3 / f"delivery/structures/{object_id}_FOUNDATION_CAMERA_V2_RGBA.png"
    source_occluder_path = A3 / f"delivery/structures/{object_id}_OCCLUDER_CAMERA_V2_RGBA.png"
    source_foundation = Image.open(source_foundation_path).convert("RGBA")
    source_occluder = Image.open(source_occluder_path).convert("RGBA")
    seed = int(hashlib.sha256((object_id + "TASK122").encode()).hexdigest()[:8], 16)

    foundation = recolor_foundation(source_foundation, rgb("193541"), seed, donor_neutral)
    occluder, masks = recolor_occluder(source_occluder, spec, row, seed + 101, donor_neutral)

    assert foundation.size == source_foundation.size
    assert occluder.size == source_occluder.size
    assert foundation.getchannel("A").tobytes() == source_foundation.getchannel("A").tobytes()
    assert occluder.getchannel("A").tobytes() == source_occluder.getchannel("A").tobytes()

    foundation_path = PILOT_DELIVERY / f"{object_id}_FOUNDATION_CAMERA_V2_MATERIALIZED_RGBA.png"
    occluder_path = PILOT_DELIVERY / f"{object_id}_OCCLUDER_CAMERA_V2_MATERIALIZED_RGBA.png"
    foundation.save(foundation_path)
    occluder.save(occluder_path)
    path100, path50 = pilot_boards(object_id, source_foundation, source_occluder, foundation, occluder)

    readback = {
        "task_id": "A9_1A6_ENV_A4_CAMERA_V2_EXACT_SIX_STRUCTURE_MATERIALIZATION",
        "phase": "NW_BLOCK_50_PERCENT_PILOT_ONLY",
        "status": "AWAITING_INTERNAL_VISUAL_REVIEW_NO_BATCH_YET",
        "camera_axes": [[40, 24], [-40, 24]],
        "axis_slopes": [0.6, -0.6],
        "axis_angles_deg": [30.9637565, -30.9637565],
        "object_id": object_id,
        "grid_rect": spec["grid_rect"],
        "local_canvas_px": list(source_foundation.size),
        "pivot_local_px": [240, 378],
        "front_edge_raw": parse_ints(row["front_edge_raw"]),
        "height_px": spec["height"],
        "foundation_source_alpha_sha256": alpha_sha(source_foundation),
        "foundation_output_alpha_sha256": alpha_sha(foundation),
        "occluder_source_alpha_sha256": alpha_sha(source_occluder),
        "occluder_output_alpha_sha256": alpha_sha(occluder),
        "alpha_bit_exact": True,
        "manual_offset": False,
        "imagegen_calls": 0,
        "donor_statistics": donor_stats,
        "outputs": {
            "foundation": str(foundation_path.relative_to(ROOT)),
            "occluder": str(occluder_path.relative_to(ROOT)),
            "qa_100": str(path100.relative_to(ROOT)),
            "qa_50": str(path50.relative_to(ROOT)),
        },
        "batch_released": False,
    }
    (PILOT_RECEIPTS / "NW_BLOCK-material-pilot-readback.json").write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("ENV_A4_NW_BLOCK_PILOT_OK")
    print(f"qa_50={path50}")
    print(f"alpha_bit_exact={readback['alpha_bit_exact']}")
    print("batch_released=false")


def main():
    stop_receipt = PILOT_RECEIPTS / "A4_PRODUCER_STOP_FAIL_FINAL_QUALITY.md"
    if stop_receipt.exists():
        raise SystemExit("Task122 stopped by producer: FAIL_FINAL_QUALITY / no pilot rebuild / no six-structure batch")
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true", help="Build NW_BLOCK pilot only")
    args = parser.parse_args()
    if not args.pilot:
        raise SystemExit("Task122 fail-closed: run --pilot before any six-structure batch")
    build_pilot()


if __name__ == "__main__":
    main()
