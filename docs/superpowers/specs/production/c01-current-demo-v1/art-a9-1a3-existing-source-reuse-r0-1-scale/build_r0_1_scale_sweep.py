#!/usr/bin/env python3
"""Task 68 R0.1 deterministic display-scale sweep.

Only the frozen exact 128 px sources are resized, using Pillow NEAREST on the
entire square frame.  All other marks are review labels, footprint annotations,
or alpha-bbox annotations.  No visible mecha pixels are drawn or reconstructed.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = next(parent for parent in OUT.parents if (parent / ".git").exists())
FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

TASK_REL = "docs/superpowers/specs/production/c01-current-demo-v1/68-c01e02-a9-1a3-r0-reuse-producer-review-and-r0-1-scale-sweep.md"
BOARD_REL = "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv"
GZ_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-existing-source-reuse-r0/GUARDIAN_Z_C128_APPROVED_EXACT.png"
BR_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-existing-source-reuse-r0/BREAKER_B128_APPROVED_EXACT.png"
MAP_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_central_1280x720.png"

EXPECTED = {
    TASK_REL: "ac9b42a1ddc187ac9dc1f17251736c1321c517b7936fa50fc89dc2d39c1a5797",
    BOARD_REL: "a289d00095b9a2787f2186c66615e4a4357f78ecd420202d34b4b601b3019619",
    GZ_REL: "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e",
    BR_REL: "e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4",
    MAP_REL: "b8ccc9b6eefb802b929a6d674e668611c6d9a88e123e24a2991710ae7e5f4ea9",
}

SWEEP_NAME = "R0_1_SCALE_SWEEP_A4_3840x720.png"
BOARD_NAME = "R0_1_SCALE_DECISION_BOARD_1920x1080.png"

GZ_ANCHOR = (382, 434)
BR_ANCHOR = (688, 505)
GZ_SOURCE_PIVOT = (64, 127)  # Task67/R0 alpha-bottom inference; not source manifest numeric data.
BR_SOURCE_PIVOT = (64, 116)  # candidate-spec.tsv ground_center_128.


@dataclass(frozen=True)
class Option:
    code: str
    label: str
    breaker_frame: int
    occlusion_level: str
    occlusion_note: str
    first_read_note: str


OPTIONS = (
    Option("A", "320", 320, "LOW", "largest tactical margins; road context remains broad", "size gain is visible; vertical giant-pressure remains restrained"),
    Option("B", "384", 384, "MEDIUM", "balanced lane occupation; road and right-side UI remain readable", "clearer giant-body read without reaching the UI rail"),
    Option("C", "448", 448, "HIGH", "strongest lane occupation; least road/context clearance", "strongest near-30m pressure; highest occlusion cost"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def validate_inputs() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for relative, expected in EXPECTED.items():
        if ".codex/generated_images" in relative or "sprite-first-master-pilot" in relative:
            raise RuntimeError(f"Forbidden source in Task68 route: {relative}")
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"Input hash mismatch: {relative}: {actual}")
        paths[relative] = path
    return paths


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.convert("RGBA").getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("Empty alpha source")
    return bbox


def bbox_size(bbox: tuple[int, int, int, int]) -> tuple[int, int]:
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def resize_nearest(source: Image.Image, target: int) -> Image.Image:
    if source.size != (128, 128):
        raise RuntimeError(f"Expected whole 128x128 source frame, got {source.size}")
    result = source.resize((target, target), Image.Resampling.NEAREST)
    # NEAREST must introduce no RGBA values absent from the exact source.
    source_colors = set(source.convert("RGBA").getdata())
    target_colors = set(result.convert("RGBA").getdata())
    if not target_colors.issubset(source_colors):
        raise RuntimeError(f"Non-nearest color synthesis detected at target {target}")
    return result


def scaled_pivot(source_pivot: tuple[int, int], target: int) -> tuple[int, int]:
    scale = Fraction(target, 128)
    values = (Fraction(source_pivot[0]) * scale, Fraction(source_pivot[1]) * scale)
    if any(value.denominator != 1 for value in values):
        raise RuntimeError(f"Non-integer target pivot for frame {target}: {values}")
    return int(values[0]), int(values[1])


def translate_bbox(bbox: tuple[int, int, int, int], origin: tuple[int, int]) -> tuple[int, int, int, int]:
    return bbox[0] + origin[0], bbox[1] + origin[1], bbox[2] + origin[0], bbox[3] + origin[1]


def draw_diamond(draw: ImageDraw.ImageDraw, center: tuple[int, int], cells: int, color: tuple[int, int, int, int]) -> None:
    x, y = center
    half_width, half_height = 40 * cells, 20 * cells
    points = ((x, y - half_height), (x + half_width, y), (x, y + half_height), (x - half_width, y))
    draw.polygon(points, fill=(color[0], color[1], color[2], 32))
    draw.line((*points, points[0]), fill=color, width=3, joint="curve")
    draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)


def make_lane(
    map_image: Image.Image,
    gz_scaled: Image.Image,
    br_scaled: Image.Image,
    option: Option,
) -> tuple[Image.Image, dict[str, object]]:
    lane = map_image.convert("RGBA").copy()
    overlay = Image.new("RGBA", lane.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    draw.rectangle((0, 0, 1280, 66), fill=(5, 13, 19, 242))
    draw.rectangle((0, 648, 1280, 720), fill=(5, 13, 19, 242))
    draw_diamond(draw, GZ_ANCHOR, 2, (83, 211, 236, 235))
    draw_diamond(draw, BR_ANCHOR, 3, (255, 183, 65, 235))
    lane = Image.alpha_composite(lane, overlay)

    gz_pivot = scaled_pivot(GZ_SOURCE_PIVOT, 256)
    br_pivot = scaled_pivot(BR_SOURCE_PIVOT, option.breaker_frame)
    gz_origin = (GZ_ANCHOR[0] - gz_pivot[0], GZ_ANCHOR[1] - gz_pivot[1])
    br_origin = (BR_ANCHOR[0] - br_pivot[0], BR_ANCHOR[1] - br_pivot[1])
    lane.alpha_composite(gz_scaled, gz_origin)
    lane.alpha_composite(br_scaled, br_origin)

    gz_target_bbox = alpha_bbox(gz_scaled)
    br_target_bbox = alpha_bbox(br_scaled)
    gz_screen_bbox = translate_bbox(gz_target_bbox, gz_origin)
    br_screen_bbox = translate_bbox(br_target_bbox, br_origin)
    right_ui_clearance = 900 - br_screen_bbox[2]
    topbar_clearance = br_screen_bbox[1] - 66

    labels = Image.new("RGBA", lane.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(labels, "RGBA")
    draw.text((24, 14), f"OPTION {option.code} · BREAKER FRAME {option.breaker_frame}", font=font(27, True), fill=(250, 246, 228, 255))
    draw.text((730, 20), f"GZ 256 · B {option.breaker_frame} · NEAREST · whole-frame / no crop", font=font(18, True), fill=(255, 197, 87, 255))
    draw.rounded_rectangle((914, 76, 1258, 205), radius=8, fill=(7, 14, 21, 238), outline=(238, 93, 84, 255), width=2)
    br_w, br_h = bbox_size(br_target_bbox)
    gz_w, gz_h = bbox_size(gz_target_bbox)
    draw.text((934, 90), f"B ALPHA BBOX {br_w}×{br_h}", font=font(19, True), fill=(255, 221, 214, 255))
    draw.text((934, 119), f"vs GZ {gz_w}×{gz_h}", font=font(17), fill=(228, 236, 238, 255))
    draw.text((934, 145), f"UI clear {right_ui_clearance}px · top clear {topbar_clearance}px", font=font(16), fill=(228, 236, 238, 255))
    draw.text((934, 170), f"lane occlusion: {option.occlusion_level}", font=font(17, True), fill=(255, 188, 87, 255))
    draw.text((24, 662), "source scale proof / not event staging / not final art", font=font(19, True), fill=(255, 202, 92, 255))
    draw.text((610, 662), "same anchors · GZ 2×2 · BREAKER 3×3 · bottom-center registered", font=font(17), fill=(220, 232, 234, 255))
    draw.text((24, 690), "Only exact C128/B128 pixels enlarged by deterministic nearest-neighbor; no paint-over, outline, sharpening, or color change.", font=font(15), fill=(188, 207, 216, 255))
    lane = Image.alpha_composite(lane, labels)

    metrics: dict[str, object] = {
        "option": option.code,
        "breaker_frame": option.breaker_frame,
        "gz_target_bbox": gz_target_bbox,
        "br_target_bbox": br_target_bbox,
        "gz_screen_bbox": gz_screen_bbox,
        "br_screen_bbox": br_screen_bbox,
        "gz_pivot": gz_pivot,
        "br_pivot": br_pivot,
        "gz_origin": gz_origin,
        "br_origin": br_origin,
        "right_ui_clearance": right_ui_clearance,
        "topbar_clearance": topbar_clearance,
        "occlusion_level": option.occlusion_level,
        "occlusion_note": option.occlusion_note,
        "first_read_note": option.first_read_note,
    }
    return lane.convert("RGB"), metrics


def make_sweep(map_image: Image.Image, gz_source: Image.Image, br_source: Image.Image) -> tuple[list[Image.Image], list[dict[str, object]]]:
    gz_scaled = resize_nearest(gz_source, 256)
    lanes: list[Image.Image] = []
    metrics: list[dict[str, object]] = []
    for option in OPTIONS:
        br_scaled = resize_nearest(br_source, option.breaker_frame)
        lane, lane_metrics = make_lane(map_image, gz_scaled, br_scaled, option)
        lanes.append(lane)
        metrics.append(lane_metrics)
    sweep = Image.new("RGB", (3840, 720), (0, 0, 0))
    for index, lane in enumerate(lanes):
        sweep.paste(lane, (index * 1280, 0))
    sweep.save(OUT / SWEEP_NAME, optimize=False)
    return lanes, metrics


def draw_bbox_annotation(
    image: Image.Image,
    screen_bbox: tuple[int, int, int, int],
    crop_origin: tuple[int, int],
    color: tuple[int, int, int, int],
    label: str,
) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    box = (
        screen_bbox[0] - crop_origin[0],
        screen_bbox[1] - crop_origin[1],
        screen_bbox[2] - crop_origin[0] - 1,
        screen_bbox[3] - crop_origin[1] - 1,
    )
    draw.rectangle(box, outline=color, width=2)
    label_box = (box[0], max(0, box[1] - 23), box[0] + 170, max(22, box[1]))
    draw.rectangle(label_box, fill=(4, 10, 15, 220))
    draw.text((label_box[0] + 5, label_box[1] + 3), label, font=font(14, True), fill=color)


def make_decision_board(lanes: list[Image.Image], metrics: list[dict[str, object]]) -> None:
    board = Image.new("RGBA", (1920, 1080), (9, 16, 24, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 1920, 102), fill=(18, 30, 42, 255))
    draw.text((34, 17), "R0.1 DISPLAY-SCALE DECISION BOARD · SAME APPROVED PIXELS", font=font(31, True), fill=(247, 245, 232, 255))
    draw.text((34, 59), "Guardian Z fixed 256 · BREAKER 320 / 384 / 448 · whole 128 frame nearest-neighbor · producer selects display size only", font=font(18), fill=(164, 194, 210, 255))

    x_positions = (30, 655, 1280)
    crop_box = (270, 80, 880, 600)  # 610x520, no resampling.
    for index, (option, lane, data, x0) in enumerate(zip(OPTIONS, lanes, metrics, x_positions)):
        panel = (x0, 118, x0 + 610, 1050)
        draw.rounded_rectangle(panel, radius=10, fill=(25, 40, 52, 255), outline=(75, 104, 120, 255), width=2)
        draw.text((x0 + 18, 132), f"OPTION {option.code} · BREAKER {option.breaker_frame}", font=font(23, True), fill=(255, 190, 85, 255))
        draw.text((x0 + 18, 161), f"scale {Fraction(option.breaker_frame, 128)}× · nearest · frame intact", font=font(16), fill=(205, 221, 225, 255))

        crop = lane.crop(crop_box).convert("RGBA")
        gz_w, gz_h = bbox_size(data["gz_target_bbox"])
        br_w, br_h = bbox_size(data["br_target_bbox"])
        draw_bbox_annotation(crop, data["gz_screen_bbox"], (crop_box[0], crop_box[1]), (83, 211, 236, 255), f"GZ bbox {gz_w}×{gz_h}")
        draw_bbox_annotation(crop, data["br_screen_bbox"], (crop_box[0], crop_box[1]), (255, 183, 65, 255), f"B bbox {br_w}×{br_h}")
        board.alpha_composite(crop, (x0, 194))

        width_ratio = br_w / gz_w
        height_ratio = br_h / gz_h
        info_y = 728
        draw.text((x0 + 18, info_y), f"alpha bbox: B {br_w}×{br_h} / GZ {gz_w}×{gz_h}", font=font(17, True), fill=(238, 241, 236, 255))
        draw.text((x0 + 18, info_y + 29), f"bbox ratio: width {width_ratio:.2f}× · height {height_ratio:.2f}×", font=font(16), fill=(193, 216, 225, 255))
        draw.text((x0 + 18, info_y + 57), f"B pivot {data['br_pivot']} → anchor {BR_ANCHOR}", font=font(16), fill=(193, 216, 225, 255))
        draw.text((x0 + 18, info_y + 85), "footprint: GZ 2×2 / BREAKER 3×3", font=font(16), fill=(193, 216, 225, 255))
        draw.text((x0 + 18, info_y + 113), f"clearance: UI {data['right_ui_clearance']}px / topbar {data['topbar_clearance']}px", font=font(16), fill=(193, 216, 225, 255))
        draw.text((x0 + 18, info_y + 144), f"lane occlusion: {data['occlusion_level']}", font=font(17, True), fill=(255, 145, 133, 255))
        draw.multiline_text((x0 + 18, info_y + 174), f"{data['occlusion_note']}\n{data['first_read_note']}", font=font(15), fill=(229, 234, 232, 255), spacing=5)
        draw.text((x0 + 18, 1018), "Candidate comparison · not final sprite/Atlas/Runtime", font=font(14, True), fill=(149, 177, 191, 255))

    board.convert("RGB").save(OUT / BOARD_NAME, optimize=False)


def fmt_bbox(value: tuple[int, int, int, int]) -> str:
    return ",".join(str(item) for item in value)


def fmt_point(value: tuple[int, int]) -> str:
    return f"{value[0]},{value[1]}"


def write_tsv(gz_source: Image.Image, br_source: Image.Image, metrics: list[dict[str, object]]) -> None:
    gz_source_bbox = alpha_bbox(gz_source)
    br_source_bbox = alpha_bbox(br_source)
    columns = (
        "option", "subject", "source_path", "source_sha256", "source_canvas", "source_alpha_bbox", "source_pivot", "pivot_authority",
        "target_frame", "actual_scale", "resampling", "target_alpha_bbox", "target_alpha_bbox_size", "target_pivot", "map_anchor", "screen_alpha_bbox",
        "footprint", "right_ui_clearance_px", "topbar_clearance_px", "lane_occlusion_level", "lane_occlusion_notes", "first_read_notes",
        "alpha_crop", "aspect_changed", "visible_pixel_edit", "runtime_allowed",
    )
    with (OUT / "scale-sweep.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        fixed = metrics[0]
        gz_w, gz_h = bbox_size(fixed["gz_target_bbox"])
        writer.writerow({
            "option": "FIXED", "subject": "GUARDIAN_Z_C", "source_path": GZ_REL, "source_sha256": EXPECTED[GZ_REL], "source_canvas": "128x128",
            "source_alpha_bbox": fmt_bbox(gz_source_bbox), "source_pivot": fmt_point(GZ_SOURCE_PIVOT), "pivot_authority": "Task67_R0_alpha_bbox_bottom_inference_labeled_not_source_numeric",
            "target_frame": "256x256", "actual_scale": "2.0", "resampling": "nearest", "target_alpha_bbox": fmt_bbox(fixed["gz_target_bbox"]), "target_alpha_bbox_size": f"{gz_w}x{gz_h}",
            "target_pivot": fmt_point(fixed["gz_pivot"]), "map_anchor": fmt_point(GZ_ANCHOR), "screen_alpha_bbox": fmt_bbox(fixed["gz_screen_bbox"]), "footprint": "2x2",
            "right_ui_clearance_px": 900 - fixed["gz_screen_bbox"][2], "topbar_clearance_px": fixed["gz_screen_bbox"][1] - 66,
            "lane_occlusion_level": "FIXED_COMPARATOR", "lane_occlusion_notes": "same 256 frame and anchor in all three lanes", "first_read_notes": "approved C silhouette fixed comparator",
            "alpha_crop": "false", "aspect_changed": "false", "visible_pixel_edit": "false", "runtime_allowed": "false",
        })
        for option, data in zip(OPTIONS, metrics):
            br_w, br_h = bbox_size(data["br_target_bbox"])
            writer.writerow({
                "option": option.code, "subject": "BREAKER_B", "source_path": BR_REL, "source_sha256": EXPECTED[BR_REL], "source_canvas": "128x128",
                "source_alpha_bbox": fmt_bbox(br_source_bbox), "source_pivot": fmt_point(BR_SOURCE_PIVOT), "pivot_authority": "candidate-spec.tsv_ground_center_128",
                "target_frame": f"{option.breaker_frame}x{option.breaker_frame}", "actual_scale": str(float(Fraction(option.breaker_frame, 128))), "resampling": "nearest",
                "target_alpha_bbox": fmt_bbox(data["br_target_bbox"]), "target_alpha_bbox_size": f"{br_w}x{br_h}", "target_pivot": fmt_point(data["br_pivot"]),
                "map_anchor": fmt_point(BR_ANCHOR), "screen_alpha_bbox": fmt_bbox(data["br_screen_bbox"]), "footprint": "3x3",
                "right_ui_clearance_px": data["right_ui_clearance"], "topbar_clearance_px": data["topbar_clearance"], "lane_occlusion_level": data["occlusion_level"],
                "lane_occlusion_notes": data["occlusion_note"], "first_read_notes": data["first_read_note"], "alpha_crop": "false", "aspect_changed": "false",
                "visible_pixel_edit": "false", "runtime_allowed": "false",
            })


def write_report(metrics: list[dict[str, object]]) -> None:
    rows = []
    for option, data in zip(OPTIONS, metrics):
        br_w, br_h = bbox_size(data["br_target_bbox"])
        gz_w, gz_h = bbox_size(data["gz_target_bbox"])
        rows.append(f"| {option.code} | {option.breaker_frame} | {float(Fraction(option.breaker_frame, 128)):.1f}× | {br_w}×{br_h} | {br_w/gz_w:.2f}× / {br_h/gz_h:.2f}× | {data['right_ui_clearance']} / {data['topbar_clearance']} px | {option.occlusion_level} |")
    report = f"""# Task 68 R0.1 completion report

Status: `deterministic display-scale sweep delivered / Candidate only / producer selection pending / runtime_allowed=false`

## Fixed inputs

- Task 68 SHA-256: `{EXPECTED[TASK_REL]}`
- Current production board SHA-256: `{EXPECTED[BOARD_REL]}`
- Guardian Z exact C128 SHA-256: `{EXPECTED[GZ_REL]}`
- BREAKER exact B128 SHA-256: `{EXPECTED[BR_REL]}`
- A4 central viewport SHA-256: `{EXPECTED[MAP_REL]}`

## Mechanical method

- Guardian Z: full 128×128 frame → 256×256 at exactly 2.0×, Pillow `NEAREST`.
- BREAKER: full 128×128 frame → 320/384/448 at exactly 2.5×/3.0×/3.5×, Pillow `NEAREST`.
- No alpha-bbox crop; no aspect-ratio change; no independent movement of head, shell, limbs, or center of gravity.
- All lanes use the same map, Guardian Z anchor `{GZ_ANCHOR}`, BREAKER anchor `{BR_ANCHOR}`, fixed 2×2/3×3 annotations, and scaled bottom-center pivots.
- The script asserts that every resized RGBA value already exists in the corresponding exact source, preventing interpolated colors.

## Comparison metrics

Guardian Z fixed target alpha bbox: `{bbox_size(metrics[0]['gz_target_bbox'])[0]}×{bbox_size(metrics[0]['gz_target_bbox'])[1]}`.

| option | BREAKER frame | scale | target alpha bbox | B/GZ width / height | right-UI / topbar clearance | lane occlusion |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
{chr(10).join(rows)}

These are display-scale and screen-occupancy measurements, not world-position, event-staging, final Sprite, Atlas, or Runtime claims.

## Delivered files

- `{SWEEP_NAME}` — three independent 1280×720 A4 lanes concatenated without resampling.
- `{BOARD_NAME}` — three native crops with alpha-bbox, footprint, clearance, occlusion, and first-read annotations.
- `scale-sweep.tsv` — source/target frame, bboxes, pivots, anchors, footprints, and lane notes.
- `delivery-hashes.sha256` — hashes for every R0.1 deliverable except itself.

## Zero-operation attestation

- ImageGen: `0`
- Blender: `0`
- redraw / cleanup / paint-over / detail completion / outline: `0`
- sharpening / denoise / color change: `0`
- reads from temporary generated_images: `0`
- Atlas / Godot / Runtime / LibTV / Canon migration: `0`
- git add / commit: `0`

`producer_scale_selection=PENDING_320_384_448`

Machine checks do not select an option or approve final art. Work stops at the producer review gate.
"""
    (OUT / "completion-report.md").write_text(report, encoding="utf-8")


def write_hashes() -> None:
    names = (
        BOARD_NAME,
        SWEEP_NAME,
        "build_r0_1_scale_sweep.py",
        "completion-report.md",
        "scale-sweep.tsv",
    )
    lines = [f"{sha256(OUT / name)}  {name}" for name in sorted(names)]
    (OUT / "delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    paths = validate_inputs()
    gz_source = Image.open(paths[GZ_REL]).convert("RGBA")
    br_source = Image.open(paths[BR_REL]).convert("RGBA")
    map_image = Image.open(paths[MAP_REL]).convert("RGB")
    if map_image.size != (1280, 720):
        raise RuntimeError(f"Unexpected A4 viewport size: {map_image.size}")
    lanes, metrics = make_sweep(map_image, gz_source, br_source)
    make_decision_board(lanes, metrics)
    write_tsv(gz_source, br_source, metrics)
    write_report(metrics)
    write_hashes()
    print(f"R0.1 outputs: {OUT}")
    for option, data in zip(OPTIONS, metrics):
        print(f"{option.code}: frame={option.breaker_frame} bbox={bbox_size(data['br_target_bbox'])} UI_clear={data['right_ui_clearance']} top_clear={data['topbar_clearance']}")
    print("producer_scale_selection=PENDING_320_384_448")


if __name__ == "__main__":
    main()
