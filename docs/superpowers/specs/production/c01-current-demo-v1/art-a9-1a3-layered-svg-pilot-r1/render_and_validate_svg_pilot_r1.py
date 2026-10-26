#!/usr/bin/env python3
"""Render and QA Task 71 local R1 hand-authored SVG pilots.

This script does not draw either machine. Visible machine geometry lives only in
the two hand-authored SVG masters. The script is limited to approved-alpha mask
preparation, SVG rasterization, review-board layout, measurements, and hashes.
It never draws machine pixels or changes the approved body designs.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path("/Users/rayz/Documents/超gag机器人大战")
OUT = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-layered-svg-pilot-r1"
PARENT = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-layered-svg-pilot"
NODE = Path("/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node")
NODE_MODULES = Path("/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules")

GZ_C128 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png"
GZ_BOARD = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png"
GZ_HARD = ROOT / ".superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png"
GZ_V10X = ROOT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png"
GZ_A2 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a2-master-production-correction/delivery/GUARDIAN_Z_V10X_KINETIC_FRONT_RGBA_1024.png"

BR_B128 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png"
BR_ID = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png"
BR_X = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png"
BR_DONOR = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/BREAKER_BX_GROUND_SHELL_MASTER_RGBA_1400.png"
STYLE_A = ROOT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png"
A4_MAP = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_central_1280x720.png"
PARENT_GZ_PNG = PARENT / "GUARDIAN_Z_C_SOUTH_IDLE_256.png"
PARENT_BR_PNG = PARENT / "BREAKER_BX_NORTH_CHARGE_READY_384.png"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


@dataclass(frozen=True)
class Pilot:
    key: str
    label: str
    frame: int
    scale: int
    source: Path
    svg: Path
    mask: Path
    envelope: Path
    png: Path
    expected_bbox: tuple[int, int, int, int]
    pivot: tuple[int, int]
    required_layers: tuple[str, ...]


PILOTS = (
    Pilot(
        "guardian_z",
        "馆守Z C · south idle · R1",
        256,
        2,
        GZ_C128,
        OUT / "GUARDIAN_Z_C_SOUTH_IDLE_MASTER-R1.svg",
        OUT / "GUARDIAN_Z_C_APPROVED_ALPHA_256-R1.png",
        OUT / "GUARDIAN_Z_C_R1_ALPHA_ENVELOPE_256.png",
        OUT / "GUARDIAN_Z_C_SOUTH_IDLE_256-R1.png",
        (26, 12, 230, 254),
        (128, 254),
        (
            "silhouette_guard", "helmet_crown_face", "shoulder_ring_left", "shoulder_ring_right",
            "chest_left", "chest_right", "center_spine_core", "upper_arm_left", "upper_arm_right",
            "cyl_forearm_left", "cyl_forearm_right", "wrist_hand_left", "wrist_hand_right", "pelvis",
            "thigh_left", "thigh_right", "shin_left", "shin_right", "foot_left", "foot_right",
            "e02_right_shoulder_old_damage", "r1_internal_negative_space_allowance",
            "r1_torso_pelvis_interlock", "hard_shadow_1", "hard_shadow_2", "accent_highlight",
        ),
    ),
    Pilot(
        "breaker",
        "BREAKER B+X · north charge-ready · R1",
        384,
        3,
        BR_B128,
        OUT / "BREAKER_BX_NORTH_CHARGE_READY_MASTER-R1.svg",
        OUT / "BREAKER_B_APPROVED_ALPHA_384-R1.png",
        OUT / "BREAKER_B_R1_ALPHA_ENVELOPE_384.png",
        OUT / "BREAKER_BX_NORTH_CHARGE_READY_384-R1.png",
        (33, 18, 351, 348),
        (192, 348),
        (
            "silhouette_guard", "high_back_shell", "x_bio_plate_01", "x_bio_plate_02", "x_bio_plate_03",
            "x_bio_plate_04", "x_bio_plate_05", "x_bio_plate_06", "x_bio_plate_07",
            "low_head_single_red_slit", "closed_chest_seam", "sealed_upper_back_exit",
            "forelimb_left", "forelimb_right", "wrist_claw_left", "wrist_claw_right",
            "short_rear_stabilizer_left", "short_rear_stabilizer_right", "hard_shadow_1", "hard_shadow_2",
            "r1_x_flexible_seam_network", "r1_forelimb_load_plates", "r1_head_shell_overlap", "accent_red",
        ),
    ),
)


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def alpha_mask_from_source(pilot: Pilot) -> None:
    source = Image.open(pilot.source).convert("RGBA")
    if source.size != (128, 128):
        raise RuntimeError(f"approved source must be 128x128: {pilot.source} = {source.size}")
    alpha = source.getchannel("A").resize((pilot.frame, pilot.frame), Image.Resampling.NEAREST)
    white = Image.new("RGBA", (pilot.frame, pilot.frame), (255, 255, 255, 0))
    white.putalpha(alpha)
    white.save(pilot.mask, optimize=False)


def render_svg_text(pilot: Pilot, svg_text: str, output: Path) -> None:
    mask_data = base64.b64encode(pilot.mask.read_bytes()).decode("ascii")
    data_url = f"data:image/png;base64,{mask_data}"
    svg_text = svg_text.replace(f'href="{pilot.mask.name}"', f'href="{data_url}"')
    node_code = r"""
const sharp = require('sharp');
const chunks = [];
process.stdin.on('data', chunk => chunks.push(chunk));
process.stdin.on('end', async () => {
  try {
    const frame = Number(process.argv[2]);
    await sharp(Buffer.concat(chunks), { density: 96 })
      .resize(frame, frame, { fit: 'fill', kernel: sharp.kernel.nearest })
      .png({ compressionLevel: 9 })
      .toFile(process.argv[1]);
  } catch (error) {
    console.error(error.stack || String(error));
    process.exit(1);
  }
});
"""
    env = dict(os.environ)
    env["NODE_PATH"] = str(NODE_MODULES)
    subprocess.run(
        [str(NODE), "-e", node_code, str(output), str(pilot.frame)],
        input=svg_text.encode("utf-8"),
        check=True,
        env=env,
    )


def render_svg(pilot: Pilot) -> None:
    render_svg_text(pilot, pilot.svg.read_text(encoding="utf-8"), pilot.png)


def render_envelope(pilot: Pilot) -> None:
    # The full-canvas foundation is the first visible path inside silhouette_guard,
    # so the rendered alpha is exactly the effective R1 mask envelope. Exporting
    # that alpha is QA evidence only; no visible machine color or geometry is drawn.
    alpha = Image.open(pilot.png).convert("RGBA").getchannel("A")
    envelope = Image.new("RGBA", (pilot.frame, pilot.frame), (255, 255, 255, 0))
    envelope.putalpha(alpha)
    envelope.save(pilot.envelope, optimize=False)


def binary_alpha(image: Image.Image) -> Image.Image:
    return image.convert("RGBA").getchannel("A").point(lambda value: 255 if value > 0 else 0, mode="1")


def count_bits(image: Image.Image) -> int:
    return sum(1 for value in image.getdata() if value)


def validate_pilot(pilot: Pilot) -> dict[str, object]:
    svg_root = ET.parse(pilot.svg).getroot()
    ids = {element.attrib.get("id") for element in svg_root.iter() if element.attrib.get("id")}
    missing_layers = sorted(set(pilot.required_layers) - ids)
    disallowed = []
    for element in svg_root.iter():
        tag = element.tag.split("}")[-1]
        if tag in {"rect", "circle", "ellipse", "polygon", "polyline", "line", "filter", "linearGradient", "radialGradient"}:
            disallowed.append(tag)

    source_mask = Image.open(pilot.mask).convert("RGBA")
    envelope = Image.open(pilot.envelope).convert("RGBA")
    result = Image.open(pilot.png).convert("RGBA")
    if result.size != (pilot.frame, pilot.frame):
        raise RuntimeError(f"render size mismatch: {pilot.png} = {result.size}")
    source_binary = binary_alpha(source_mask)
    envelope_binary = binary_alpha(envelope)
    result_binary = binary_alpha(result)
    intersection = ImageChops.logical_and(source_binary, result_binary)
    union = ImageChops.logical_or(source_binary, result_binary)
    inter_count = count_bits(intersection)
    union_count = count_bits(union)
    iou = inter_count / union_count if union_count else 0.0
    envelope_intersection = ImageChops.logical_and(envelope_binary, result_binary)
    envelope_union = ImageChops.logical_or(envelope_binary, result_binary)
    envelope_union_count = count_bits(envelope_union)
    envelope_iou = count_bits(envelope_intersection) / envelope_union_count if envelope_union_count else 0.0
    outside = ImageChops.multiply(result.getchannel("A"), ImageOps.invert(envelope_binary.convert("L")))
    added_vs_source = ImageChops.subtract(result_binary.convert("L"), source_binary.convert("L"))
    removed_vs_source = ImageChops.subtract(source_binary.convert("L"), result_binary.convert("L"))
    bbox = result.getchannel("A").getbbox()
    expected_center = ((pilot.expected_bbox[0] + pilot.expected_bbox[2]) / 2, (pilot.expected_bbox[1] + pilot.expected_bbox[3]) / 2)
    actual_center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2) if bbox else (None, None)
    center_drift = max(abs(actual_center[0] - expected_center[0]), abs(actual_center[1] - expected_center[1])) if bbox else None
    return {
        "key": pilot.key,
        "svg": pilot.svg.name,
        "png": pilot.png.name,
        "frame": [pilot.frame, pilot.frame],
        "bbox": list(bbox) if bbox else None,
        "expected_bbox": list(pilot.expected_bbox),
        "bbox_size": [bbox[2] - bbox[0], bbox[3] - bbox[1]] if bbox else None,
        "pivot": list(pilot.pivot),
        "approved_silhouette_iou": round(iou, 6),
        "r1_envelope_iou": round(envelope_iou, 6),
        "added_internal_cleanup_px": sum(1 for value in added_vs_source.getdata() if value),
        "removed_approved_px": sum(1 for value in removed_vs_source.getdata() if value),
        "center_drift_px": center_drift,
        "outside_r1_envelope_alpha_max": outside.getextrema()[1],
        "missing_layers": missing_layers,
        "disallowed_svg_geometry": sorted(set(disallowed)),
        "machine_pass": bool(
            bbox == pilot.expected_bbox
            and iou >= 0.96
            and envelope_iou >= 0.999
            and (center_drift is not None and center_drift <= 1)
            and outside.getextrema()[1] == 0
            and not missing_layers
            and not disallowed
        ),
    }


def contain(path: Path, size: tuple[int, int], *, background=(12, 28, 38, 255), nearest=False) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    resample = Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS
    image.thumbnail(size, resample)
    target = Image.new("RGBA", size, background)
    target.alpha_composite(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return target


def add_card(board: Image.Image, box: tuple[int, int, int, int], title: str, image_path: Path, *, accent: str, nearest=False) -> None:
    draw = ImageDraw.Draw(board)
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=16, fill="#0d202b", outline=accent, width=2)
    draw.text((x0 + 16, y0 + 12), title, font=font(18, bold=True), fill="#f2efe6")
    area = contain(image_path, (x1 - x0 - 24, y1 - y0 - 52), background=(10, 24, 32, 255), nearest=nearest)
    board.alpha_composite(area, (x0 + 12, y0 + 42))


def build_layer_source_board() -> None:
    board = Image.new("RGBA", (1920, 1080), "#07131d")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1920, 88), fill="#0c2431")
    draw.text((34, 22), "A9.1-A3 · LOCAL R1 / LAYER + SOURCE BOARD", font=font(30, bold=True), fill="#f2efe6")
    draw.text((1885, 28), "one local R1 · no redesign · Candidate", anchor="ra", font=font(20), fill="#e8ab35")

    draw.rounded_rectangle((24, 108, 946, 1028), radius=22, fill="#091b25", outline="#3784a8", width=3)
    draw.text((48, 128), "馆守Z C · approved silhouette + Hard identity + E02 form", font=font(24, bold=True), fill="#f2efe6")
    add_card(board, (48, 180, 288, 442), "C128 · silhouette only", GZ_C128, accent="#e5ad37", nearest=True)
    add_card(board, (48, 458, 288, 740), "CML008 · Hard identity", GZ_HARD, accent="#e65848")
    add_card(board, (48, 756, 288, 996), "V10X · E02 detail limit", GZ_V10X, accent="#4d98b9")
    add_card(board, (310, 180, 744, 620), "R1 SVG actual · 256", OUT / "GUARDIAN_Z_C_SOUTH_IDLE_256-R1.png", accent="#42a0bf", nearest=True)
    draw.text((314, 650), "Named path layers", font=font(20, bold=True), fill="#e5ad37")
    gz_lines = [
        "helmet / layered crown / grille face", "L/R shoulder rings + red X chest", "circular gold core + center spine",
        "E02 twin cylindrical forearms", "pelvis / articulated legs / broad feet", "old right-shoulder damage",
        "R1 torso-pelvis interlock + two shadows",
    ]
    for index, value in enumerate(gz_lines):
        draw.text((326, 688 + index * 38), f"{index + 1:02d}  {value}", font=font(17), fill="#c8d7dd")
    add_card(board, (760, 180, 922, 430), "70 parent · frozen", PARENT_GZ_PNG, accent="#455f70", nearest=True)
    draw.multiline_text((766, 466), "R1 delta only:\ninternal negative space\n+ armor interlock", font=font(16), fill="#9fb1ba", spacing=8)

    draw.rounded_rectangle((974, 108, 1896, 1028), radius=22, fill="#091b25", outline="#b24a48", width=3)
    draw.text((998, 128), "BREAKER B+X · approved load topology + approved bio-armor relation", font=font(24, bold=True), fill="#f2efe6")
    add_card(board, (998, 180, 1238, 442), "B128 · silhouette only", BR_B128, accent="#e5ad37", nearest=True)
    add_card(board, (998, 458, 1238, 740), "B identity · topology", BR_ID, accent="#4d98b9")
    add_card(board, (998, 756, 1238, 996), "X relation · surface", BR_X, accent="#e65848")
    add_card(board, (1260, 180, 1694, 620), "R1 SVG actual · 384", OUT / "BREAKER_BX_NORTH_CHARGE_READY_384-R1.png", accent="#b94e4c", nearest=True)
    draw.text((1264, 650), "Named path layers", font=font(20, bold=True), fill="#e5ad37")
    br_lines = [
        "high back shell + seven asym bio plates", "low embedded head / one narrow red slit", "closed chest seam",
        "sealed upper-back exit", "forelimb-bearing semi-upright load", "short rear stabilizers",
        "R1 seam network + asymmetric limb plates",
    ]
    for index, value in enumerate(br_lines):
        draw.text((1276, 688 + index * 38), f"{index + 1:02d}  {value}", font=font(17), fill="#c8d7dd")
    add_card(board, (1710, 180, 1872, 430), "70 parent · frozen", PARENT_BR_PNG, accent="#455f70", nearest=True)
    draw.multiline_text((1716, 466), "R1 delta only:\nX surface rhythm\n+ load line pressure", font=font(16), fill="#9fb1ba", spacing=8)
    board.convert("RGB").save(OUT / "SVG_LAYER_AND_SOURCE_BOARD_1920x1080-R1.png", optimize=True)


def mask_panel(mask: Image.Image, color: tuple[int, int, int, int]) -> Image.Image:
    alpha = mask.convert("RGBA").getchannel("A")
    result = Image.new("RGBA", mask.size, color)
    result.putalpha(alpha)
    return result


def build_silhouette_board(metrics: list[dict[str, object]]) -> None:
    board = Image.new("RGBA", (1920, 1080), "#07131d")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1920, 88), fill="#0c2431")
    draw.text((34, 22), "R1 APPROVED ENVELOPE / SVG ALPHA OVERLAY", font=font(30, bold=True), fill="#f2efe6")
    draw.text((1885, 28), "cyan=allowed internal cleanup · red=removed · white=match", anchor="ra", font=font(18), fill="#b9cbd2")
    for row, (pilot, metric) in enumerate(zip(PILOTS, metrics)):
        y0 = 120 + row * 470
        draw.rounded_rectangle((30, y0, 1890, y0 + 430), radius=22, fill="#091b25", outline="#2f5d70", width=2)
        draw.text((54, y0 + 18), pilot.label, font=font(24, bold=True), fill="#f2efe6")
        approved = Image.open(pilot.mask).convert("RGBA")
        actual = Image.open(pilot.png).convert("RGBA")
        source_bin = binary_alpha(approved).convert("L")
        actual_bin = binary_alpha(actual).convert("L")
        source_only = ImageChops.subtract(source_bin, actual_bin)
        actual_only = ImageChops.subtract(actual_bin, source_bin)
        common = ImageChops.multiply(source_bin, actual_bin)
        overlay = Image.new("RGBA", approved.size, (0, 0, 0, 0))
        common_layer = Image.new("RGBA", approved.size, (238, 239, 231, 255)); common_layer.putalpha(common)
        source_layer = Image.new("RGBA", approved.size, (238, 69, 64, 255)); source_layer.putalpha(source_only)
        actual_layer = Image.new("RGBA", approved.size, (47, 200, 220, 255)); actual_layer.putalpha(actual_only)
        overlay.alpha_composite(common_layer); overlay.alpha_composite(source_layer); overlay.alpha_composite(actual_layer)
        panels = (
            ("approved alpha", mask_panel(approved, (230, 72, 66, 255))),
            ("SVG alpha", mask_panel(actual, (52, 198, 218, 255))),
            ("difference overlay", overlay),
        )
        for column, (label, image) in enumerate(panels):
            x = 54 + column * 390
            draw.rounded_rectangle((x, y0 + 62, x + 360, y0 + 396), radius=14, fill="#06131b", outline="#274957", width=2)
            view = contain_image(image, (320, 290), nearest=True)
            board.alpha_composite(view, (x + 20, y0 + 86))
            draw.text((x + 180, y0 + 370), label, anchor="mm", font=font(17, bold=True), fill="#cbd8dd")
        mx = 1260
        draw.text((mx, y0 + 86), f"approved IoU  {metric['approved_silhouette_iou']:.6f}", font=font(26, bold=True), fill="#e5ad37")
        draw.text((mx, y0 + 140), f"bbox  {metric['bbox']}", font=font(19), fill="#c8d7dd")
        draw.text((mx, y0 + 184), f"target  {metric['expected_bbox']}", font=font(19), fill="#c8d7dd")
        draw.text((mx, y0 + 228), f"pivot  {metric['pivot']}", font=font(19), fill="#c8d7dd")
        draw.text((mx, y0 + 272), f"outside R1 envelope  {metric['outside_r1_envelope_alpha_max']}", font=font(19), fill="#c8d7dd")
        status = "MACHINE PASS" if metric["machine_pass"] else "MACHINE FAIL"
        color = "#60c795" if metric["machine_pass"] else "#ef5a4f"
        draw.rounded_rectangle((mx, y0 + 320, mx + 420, y0 + 378), radius=12, fill="#0b1820", outline=color, width=3)
        draw.text((mx + 210, y0 + 349), status, anchor="mm", font=font(22, bold=True), fill=color)
    board.convert("RGB").save(OUT / "SVG_SILHOUETTE_OVERLAY_1920x1080-R1.png", optimize=True)


def contain_image(image: Image.Image, size: tuple[int, int], *, nearest=False) -> Image.Image:
    image = image.convert("RGBA")
    resample = Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS
    image.thumbnail(size, resample)
    target = Image.new("RGBA", size, (8, 20, 28, 255))
    target.alpha_composite(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return target


def build_a4_board() -> None:
    board = Image.open(A4_MAP).convert("RGBA")
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 1280, 68), fill=(4, 13, 19, 238))
    draw.text((24, 16), "LOCAL R1 ON A4 MAP · DISPLAY 256 / 384", font=font(26, bold=True), fill="#f4f0e6")
    draw.text((1250, 22), "same design + scale · local path cleanup only", anchor="ra", font=font(17), fill="#e5ad37")
    guardian = Image.open(OUT / "GUARDIAN_Z_C_SOUTH_IDLE_256-R1.png").convert("RGBA")
    breaker = Image.open(OUT / "BREAKER_BX_NORTH_CHARGE_READY_384-R1.png").convert("RGBA")
    gz_xy = (232, 356)
    br_xy = (520, 262)
    board.alpha_composite(guardian, gz_xy)
    board.alpha_composite(breaker, br_xy)
    draw.rounded_rectangle((174, 78, 485, 130), radius=12, fill=(5, 18, 26, 225), outline="#45a6c5", width=2)
    draw.text((194, 91), "馆守Z · 256 · 2×2", font=font(19, bold=True), fill="#e8eef0")
    draw.rounded_rectangle((588, 78, 917, 130), radius=12, fill=(5, 18, 26, 225), outline="#d14d47", width=2)
    draw.text((608, 91), "BREAKER · 384 · 3×3", font=font(19, bold=True), fill="#e8eef0")
    for x, y, color in ((360, 610, "#49c5dc"), (712, 610, "#f2554c")):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color, outline="#07131d", width=2)
        draw.line((x - 18, y, x + 18, y), fill=color, width=2)
    draw.rectangle((0, 672, 1280, 720), fill=(4, 13, 19, 225))
    draw.text((22, 687), "R1 keeps C/B design and scale; pivot markers are review evidence, not Runtime anchors or event positions.", font=font(16), fill="#d2dee2")
    board.convert("RGB").save(OUT / "SVG_PILOT_ON_A4_MAP_1280x720-R1.png", optimize=True)


def build_scale_review_board() -> None:
    board = Image.new("RGBA", (1920, 1080), "#07131d")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1920, 88), fill="#0c2431")
    draw.text((34, 22), "LOCAL R1 · 50% / 100% ACTUAL PIXEL REVIEW", font=font(30, bold=True), fill="#f2efe6")
    draw.text((1885, 28), "same design · one local path cleanup · nearest display", anchor="ra", font=font(18), fill="#b9cbd2")

    panels = (
        (PILOTS[0], (30, 116, 940, 1035), "#3d8dad"),
        (PILOTS[1], (980, 116, 1890, 1035), "#b64c49"),
    )
    for pilot, box, accent in panels:
        x0, y0, x1, y1 = box
        draw.rounded_rectangle(box, radius=22, fill="#091b25", outline=accent, width=3)
        draw.text((x0 + 26, y0 + 22), pilot.label, font=font(24, bold=True), fill="#f2efe6")
        source = Image.open(pilot.png).convert("RGBA")
        full_back = Image.new("RGBA", (430, 520), "#e9eceb")
        full_back.alpha_composite(source, ((430 - source.width) // 2, (480 - source.height) // 2 + 20))
        draw.rounded_rectangle((x0 + 24, y0 + 72, x0 + 474, y0 + 612), radius=14, fill="#e9eceb", outline="#879ba4", width=2)
        board.alpha_composite(full_back, (x0 + 34, y0 + 82))
        draw.text((x0 + 249, y0 + 584), f"100% · {pilot.frame}px", anchor="mm", font=font(18, bold=True), fill="#162b36")

        half = source.resize((pilot.frame // 2, pilot.frame // 2), Image.Resampling.NEAREST)
        half_back = Image.new("RGBA", (360, 310), "#e9eceb")
        half_back.alpha_composite(half, ((360 - half.width) // 2, (270 - half.height) // 2 + 8))
        draw.rounded_rectangle((x0 + 505, y0 + 72, x0 + 885, y0 + 402), radius=14, fill="#e9eceb", outline="#879ba4", width=2)
        board.alpha_composite(half_back, (x0 + 515, y0 + 82))
        draw.text((x0 + 695, y0 + 374), f"50% · {pilot.frame // 2}px", anchor="mm", font=font(18, bold=True), fill="#162b36")

        checks = (
            ("馆守Z" in pilot.label and "冠 / 银栅脸 / 红X胸 / 金核" or "高背 / 低头单红缝 / 前肢承重"),
            ("馆守Z" in pilot.label and "双圆柱前臂 / 双臂E02 / 宽脚" or "短后稳定 / X异质叠片 / 三处封闭"),
            "deep-ink / large blocks / two hard shadows",
            "producer pixel verdict pending",
        )
        draw.text((x0 + 514, y0 + 445), "50% identity checklist", font=font(19, bold=True), fill="#e5ad37")
        for index, value in enumerate(checks):
            draw.text((x0 + 526, y0 + 488 + index * 48), f"• {value}", font=font(14), fill="#c8d7dd")
        draw.text((x0 + 34, y0 + 670), "PATH FINISH", font=font(18, bold=True), fill=accent)
        draw.multiline_text(
            (x0 + 34, y0 + 710),
            "Local edits inside parent SVG layers\nApproved outer envelope unchanged\nNo ImageGen / Blender / body reroll",
            font=font(17), fill="#aebfc7", spacing=12,
        )
    board.convert("RGB").save(OUT / "SVG_PILOT_50_100_REVIEW_1920x1080-R1.png", optimize=True)


def validate_source_locks() -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    with (OUT / "source-lock-R1.tsv").open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = ROOT / row["path"]
            actual = sha256(path) if path.exists() else None
            checks.append(
                {
                    "source_id": row["source_id"],
                    "path": row["path"],
                    "expected_sha256": row["sha256"],
                    "actual_sha256": actual,
                    "pass": actual == row["sha256"],
                }
            )
    return checks


def write_qa_report(metrics: list[dict[str, object]], source_checks: list[dict[str, object]]) -> None:
    report = {
        "task": "71-c01e02-a9-1a3-svg-pilot-producer-review-and-local-r1",
        "authority": "Candidate",
        "runtime_allowed": False,
        "imagegen_calls": 0,
        "blender_calls": 0,
        "pillow_machine_drawing": False,
        "revision_round": "R1_ONLY",
        "redesign": False,
        "visible_machine_geometry": "hand-authored SVG path only",
        "source_locks": source_checks,
        "source_lock_pass_all": all(bool(check["pass"]) for check in source_checks),
        "pilots": metrics,
        "machine_pass_all": all(bool(metric["machine_pass"]) for metric in metrics) and all(bool(check["pass"]) for check in source_checks),
        "visual_pass": "PENDING_PRODUCER_PIXEL_REVIEW",
    }
    (OUT / "qa-report-R1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_hashes() -> None:
    names = [
        "GUARDIAN_Z_C_SOUTH_IDLE_MASTER-R1.svg",
        "GUARDIAN_Z_C_SOUTH_IDLE_256-R1.png",
        "BREAKER_BX_NORTH_CHARGE_READY_MASTER-R1.svg",
        "BREAKER_BX_NORTH_CHARGE_READY_384-R1.png",
        "GUARDIAN_Z_C_APPROVED_ALPHA_256-R1.png",
        "BREAKER_B_APPROVED_ALPHA_384-R1.png",
        "GUARDIAN_Z_C_R1_ALPHA_ENVELOPE_256.png",
        "BREAKER_B_R1_ALPHA_ENVELOPE_384.png",
        "SVG_LAYER_AND_SOURCE_BOARD_1920x1080-R1.png",
        "SVG_SILHOUETTE_OVERLAY_1920x1080-R1.png",
        "SVG_PILOT_ON_A4_MAP_1280x720-R1.png",
        "SVG_PILOT_50_100_REVIEW_1920x1080-R1.png",
        "layer-spec-R1.tsv",
        "source-lock-R1.tsv",
        "qa-report-R1.json",
        "r1-delta.md",
        "visual-self-review-R1.md",
        "completion-report-R1.md",
        "render_and_validate_svg_pilot_r1.py",
    ]
    lines = []
    for name in names:
        path = OUT / name
        if path.exists():
            lines.append(f"{sha256(path)}  {name}")
    (OUT / "delivery-hashes-R1.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for pilot in PILOTS:
        alpha_mask_from_source(pilot)
        render_svg(pilot)
        render_envelope(pilot)
    metrics = [validate_pilot(pilot) for pilot in PILOTS]
    source_checks = validate_source_locks()
    write_qa_report(metrics, source_checks)
    build_layer_source_board()
    build_silhouette_board(metrics)
    build_a4_board()
    build_scale_review_board()
    write_hashes()
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
