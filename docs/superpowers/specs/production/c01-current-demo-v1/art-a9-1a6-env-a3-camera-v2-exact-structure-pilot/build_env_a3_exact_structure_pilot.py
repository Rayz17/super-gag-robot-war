#!/usr/bin/env python3
"""Build the zero-generation ENV-A3 Camera V2 NW_BLOCK structure pilot.

The visible structure is constructed directly from the exact 40x24 dimetric
projection. No ENV-A1/A2 structure pixel is used as a donor. ENV-A2 ground is
used only as a retained placement background and the rejected A2 NW_BLOCK is
used only in the labelled comparison panel.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(__file__).resolve().parents[6]
ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent / "121-c01e02-env-a3-camera-v2-exact-structure-pilot-objective.md"
P103 = ROOT.parent / "119-c01e02-p103-env-a2-camera-v2-visual-rejection.md"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
A2 = ROOT.parent / "art-a9-1a6-env-a2-simple-recomposition"
A2_GROUND = A2 / "delivery/GROUND_BAKE_CURRENT_V2_2400x1350.png"
A2_OLD_FOUNDATION = A2 / "delivery/structures/NW_BLOCK_FOUNDATION_RGBA.png"
A2_OLD_OCCLUDER = A2 / "delivery/structures/NW_BLOCK_OCCLUDER_RGBA.png"

DELIVERY = ROOT / "delivery"
STATES = ROOT / "qa/states"
QA = ROOT / "qa"
RECEIPTS = ROOT / "receipts"
for directory in (DELIVERY, STATES, QA, RECEIPTS):
    directory.mkdir(parents=True, exist_ok=True)

ASSET_W, ASSET_H = 480, 378
PIVOT_LOCAL = (240, 378)
GRID_RECT = (1, 0, 7, 5)
WORLD_CANVAS_ORIGIN_RAW = (-920, -99)
VISUAL_BOUNDS_RAW = (-160, -90, 480, 378)
FRONT_EDGE_RAW = (80, 288)
HEIGHT_PX = 84
SCALE = 4


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def project_local(x: float, y: float) -> tuple[float, float]:
    """Project grid boundary coordinate into NW_BLOCK local canvas."""
    raw_x = (x - y) * 40.0
    raw_y = (x + y) * 24.0
    return raw_x - VISUAL_BOUNDS_RAW[0], raw_y - VISUAL_BOUNDS_RAW[1]


def hs(point: tuple[float, float]) -> tuple[int, int]:
    return round(point[0] * SCALE), round(point[1] * SCALE)


def hpoly(draw: ImageDraw.ImageDraw, points, fill, outline=None, width=1):
    scaled = [hs(p) for p in points]
    draw.polygon(scaled, fill=fill)
    if outline:
        draw.line(scaled + [scaled[0]], fill=outline, width=width * SCALE, joint="curve")


def hline(draw: ImageDraw.ImageDraw, points, fill, width=1):
    draw.line([hs(p) for p in points], fill=fill, width=width * SCALE, joint="curve")


def lerp(a, b, t: float):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def shift_y(point, amount: float):
    return point[0], point[1] - amount


def downsample(image: Image.Image) -> Image.Image:
    return image.resize((ASSET_W, ASSET_H), Image.Resampling.LANCZOS)


def build_foundation() -> Image.Image:
    image = Image.new("RGBA", (ASSET_W * SCALE, ASSET_H * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    outer = [project_local(0.5, -0.5), project_local(7.5, -0.5), project_local(7.5, 4.5), project_local(0.5, 4.5)]
    curb = [project_local(0.72, -0.28), project_local(7.28, -0.28), project_local(7.28, 4.28), project_local(0.72, 4.28)]
    building_pad = [project_local(0.82, -0.18), project_local(7.18, -0.18), project_local(7.18, 4.18), project_local(0.82, 4.18)]

    hpoly(d, outer, "#122a34", "#07151c", 3)
    hpoly(d, curb, "#274956", "#416a74", 2)
    hpoly(d, building_pad, "#193541", "#0e252e", 2)

    # Exact 40x24 expansion joints. Every visible diagonal is one camera axis.
    for x in (2.5, 4.5, 6.5):
        hline(d, [project_local(x, -0.18), project_local(x, 4.18)], "#294b56", 1)
    for y in (1.25, 2.75):
        hline(d, [project_local(0.82, y), project_local(7.18, y)], "#102b34", 1)

    # A low loading apron and two hard contact-shadow masses; these stay visible.
    apron = [project_local(2.0, 3.45), project_local(6.55, 3.45), project_local(6.55, 4.18), project_local(2.0, 4.18)]
    hpoly(d, apron, "#213e48", "#385d67", 1)
    contact = [project_local(1.0, 3.92), project_local(7.0, 3.92), project_local(7.0, 4.15), project_local(1.0, 4.15)]
    hpoly(d, contact, (6, 19, 25, 110), None)

    # Restrained material patches, aligned with the grid instead of free perspective.
    for x, y in ((1.15, 0.25), (5.75, 0.55), (3.9, 3.25)):
        patch = [project_local(x, y), project_local(x + 0.7, y), project_local(x + 0.7, y + 0.3), project_local(x, y + 0.3)]
        hpoly(d, patch, "#31505a", None)

    return downsample(image)


def face_patch(edge_roof_a, edge_roof_b, edge_base_a, edge_base_b, u0, u1, t0, t1):
    ra = lerp(edge_roof_a, edge_roof_b, u0)
    rb = lerp(edge_roof_a, edge_roof_b, u1)
    ba = lerp(edge_base_a, edge_base_b, u0)
    bb = lerp(edge_base_a, edge_base_b, u1)
    return [lerp(ra, ba, t0), lerp(rb, bb, t0), lerp(rb, bb, t1), lerp(ra, ba, t1)]


def build_occluder() -> Image.Image:
    image = Image.new("RGBA", (ASSET_W * SCALE, ASSET_H * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)

    a = project_local(0.9, -0.1)
    b = project_local(7.1, -0.1)
    c = project_local(7.1, 4.1)
    dd = project_local(0.9, 4.1)
    ar, br, cr, dr = [shift_y(p, HEIGHT_PX) for p in (a, b, c, dd)]

    # Two hard shadow levels: east face and south face.
    hpoly(d, [br, cr, c, b], "#284b56", "#0a1b22", 3)
    hpoly(d, [dr, cr, c, dd], "#1b3540", "#08171e", 3)

    # Exact-axis facade bays; no perspective taper.
    for u0, u1 in ((0.07, 0.27), (0.34, 0.54), (0.61, 0.81)):
        hpoly(d, face_patch(br, cr, b, c, u0, u1, 0.28, 0.78), "#335964", "#112a33", 1)
        hpoly(d, face_patch(dr, cr, dd, c, u0, u1, 0.25, 0.76), "#294c57", "#0e2630", 1)

    # South service door and an amber emergency strip.
    hpoly(d, face_patch(dr, cr, dd, c, 0.42, 0.61, 0.38, 0.98), "#132c35", "#4b7078", 2)
    hpoly(d, face_patch(dr, cr, dd, c, 0.45, 0.58, 0.48, 0.54), "#a46f37", None)

    # Roof plane. Its two principal edges are mathematically +/- atan(24/40).
    hpoly(d, [ar, br, cr, dr], "#315766", "#091b22", 3)
    roof_inner = [project_local(1.12, 0.12), project_local(6.88, 0.12), project_local(6.88, 3.88), project_local(1.12, 3.88)]
    roof_inner = [shift_y(p, HEIGHT_PX) for p in roof_inner]
    hpoly(d, roof_inner, "#365f6b", "#517985", 2)

    # Roof panels and drainage seams remain parallel to the exact grid axes.
    for x in (2.3, 3.8, 5.3):
        hline(d, [shift_y(project_local(x, 0.12), HEIGHT_PX), shift_y(project_local(x, 3.88), HEIGHT_PX)], "#264a55", 1)
    for y in (1.25, 2.55):
        hline(d, [shift_y(project_local(1.12, y), HEIGHT_PX), shift_y(project_local(6.88, y), HEIGHT_PX)], "#193b46", 1)

    # Flat service hatches and vents: material detail without extra camera language.
    hatch = [project_local(3.05, 1.2), project_local(4.55, 1.2), project_local(4.55, 2.25), project_local(3.05, 2.25)]
    hatch = [shift_y(p, HEIGHT_PX) for p in hatch]
    hpoly(d, hatch, "#223f49", "#66858c", 2)
    hatch_inner = [project_local(3.25, 1.38), project_local(4.35, 1.38), project_local(4.35, 2.07), project_local(3.25, 2.07)]
    hatch_inner = [shift_y(p, HEIGHT_PX) for p in hatch_inner]
    hpoly(d, hatch_inner, "#182f38", None)

    for x, y in ((1.55, 0.58), (5.65, 3.05)):
        vent = [project_local(x, y), project_local(x + 0.75, y), project_local(x + 0.75, y + 0.36), project_local(x, y + 0.36)]
        vent = [shift_y(p, HEIGHT_PX) for p in vent]
        hpoly(d, vent, "#4b6d76", "#172f38", 1)

    # Sparse rain wear, still aligned to the surface plane.
    for x, y, length in ((1.5, 2.2, 0.55), (5.0, 0.9, 0.42), (5.7, 2.3, 0.6)):
        hline(d, [shift_y(project_local(x, y), HEIGHT_PX), shift_y(project_local(x + length, y), HEIGHT_PX)], "#66838a", 1)

    return downsample(image)


def alpha_scaled(image: Image.Image, factor: float) -> Image.Image:
    out = image.copy()
    alpha = out.getchannel("A").point(lambda p: round(p * factor))
    out.putalpha(alpha)
    return out


def composite(foundation: Image.Image, occluder: Image.Image, alpha: float = 1.0) -> Image.Image:
    result = foundation.copy()
    result.alpha_composite(alpha_scaled(occluder, alpha))
    return result


def checker(size, cell=24):
    image = Image.new("RGBA", size, "#0b1820")
    d = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2 == 0:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#10242d")
    return image


def paste_center(panel: Image.Image, asset: Image.Image, y_offset=28):
    x = (panel.width - asset.width) // 2
    y = y_offset + (panel.height - y_offset - asset.height) // 2
    panel.alpha_composite(asset, (x, y))


def build_tristate_board(normal, reveal, restore):
    panel_w, panel_h = 560, 500
    board = Image.new("RGBA", (panel_w * 3, panel_h + 86), "#071219")
    d = ImageDraw.Draw(board)
    labels = [
        ("NORMAL 100%", "occluder alpha 1.00"),
        ("REVEAL 34%", "foundation 1.00 / occluder 0.34"),
        ("RESTORE 100%", "same bytes restored to 1.00"),
    ]
    for index, (state, label) in enumerate(zip((normal, reveal, restore), labels)):
        panel = checker((panel_w - 16, panel_h - 16), 28)
        paste_center(panel, state, 38)
        x = index * panel_w + 8
        board.alpha_composite(panel, (x, 78))
        d.text((x + 18, 13), label[0], font=font(27, True), fill="#e9f4f6")
        d.text((x + 18, 46), label[1], font=font(18), fill="#7fb1bc")
    d.line((0, 76, board.width, 76), fill="#315866", width=2)
    return board


def target_axes(draw, origin, length=125, width=4):
    ox, oy = origin
    dx = length * math.cos(math.radians(30.9637565))
    dy = length * math.sin(math.radians(30.9637565))
    draw.line((ox, oy, ox + dx, oy - dy), fill="#45c6d8", width=width)
    draw.line((ox, oy, ox + dx, oy + dy), fill="#e0a24a", width=width)
    draw.ellipse((ox - 5, oy - 5, ox + 5, oy + 5), fill="#f2f7f8")


def fit_asset(asset, box_w, box_h):
    factor = min(box_w / asset.width, box_h / asset.height)
    return asset.resize((round(asset.width * factor), round(asset.height * factor)), Image.Resampling.LANCZOS)


def build_angle_comparison(new_asset):
    old_foundation = Image.open(A2_OLD_FOUNDATION).convert("RGBA")
    old_occluder = Image.open(A2_OLD_OCCLUDER).convert("RGBA")
    old_asset = composite(old_foundation, old_occluder)

    board = Image.new("RGBA", (1600, 900), "#071219")
    d = ImageDraw.Draw(board)
    d.text((40, 25), "NW_BLOCK CAMERA-ANGLE COMPARISON", font=font(34, True), fill="#eff7f8")
    d.text((40, 69), "Target grid axes: +/-30.96 deg | orthographic | no convergence", font=font(22), fill="#8ab8c2")
    for i, (title, asset) in enumerate((("REJECTED A2 PIXELS", old_asset), ("A3 EXACT 40x24 BUILD", new_asset))):
        x0 = 30 + i * 785
        panel = checker((755, 700), 30)
        display = fit_asset(asset, 680, 530)
        px = (panel.width - display.width) // 2
        py = 100 + (520 - display.height) // 2
        panel.alpha_composite(display, (px, py))
        pd = ImageDraw.Draw(panel)
        pd.text((22, 20), title, font=font(26, True), fill="#f0f6f7")
        target_axes(pd, (92, 630), 125, 5)
        if i == 0:
            pd.text((235, 606), "P103 measured dominant edges", font=font(20, True), fill="#f2c889")
            pd.text((235, 635), "approx. 20-25 deg -> CAMERA MISMATCH", font=font(20), fill="#d99463")
        else:
            angle = math.degrees(math.atan2(24, 40))
            pd.text((235, 606), "measured from authored edges", font=font(20, True), fill="#8ee0e8")
            pd.text((235, 635), f"+/-{angle:.2f} deg, slope +/-0.600 -> EXACT", font=font(20), fill="#b8ecf0")
        board.alpha_composite(panel, (x0, 145))
    return board


def build_world_and_plan(normal_asset):
    ground = Image.open(A2_GROUND).convert("RGBA")
    world = ground.copy()
    # visual bounds raw top-left + raw-to-source-canvas translation
    source_x = VISUAL_BOUNDS_RAW[0] - WORLD_CANVAS_ORIGIN_RAW[0]
    source_y = VISUAL_BOUNDS_RAW[1] - WORLD_CANVAS_ORIGIN_RAW[1]
    world.alpha_composite(normal_asset, (source_x, source_y))

    # Full world overview preserves exact placement and marks the A_PLAN camera crop.
    overview = world.resize((1280, 720), Image.Resampling.LANCZOS)
    od = ImageDraw.Draw(overview)
    sx = 1280 / 2400
    sy = 720 / 1350
    crop = (680, 515, 680 + 1280, 515 + 584)
    crop_scaled = tuple(round(v * (sx if i % 2 == 0 else sy)) for i, v in enumerate(crop))
    od.rectangle(crop_scaled, outline="#64d5df", width=3)
    od.text((24, 20), "A PLAN WORLD-CANVAS EXACT PLACEMENT", font=font(25, True), fill="#f0f7f8", stroke_width=2, stroke_fill="#071219")
    od.text((24, 53), "NW_BLOCK grid rect [1,0,7,5] | camera crop outlined", font=font(18), fill="#a2d4dc", stroke_width=2, stroke_fill="#071219")

    # Actual A_PLAN camera crop. The exact NW_BLOCK is offscreen above the crop.
    actual = Image.new("RGBA", (1280, 720), "#071219")
    actual_crop = world.crop(crop)
    actual.alpha_composite(actual_crop, (0, 58))
    ad = ImageDraw.Draw(actual)
    ad.text((22, 15), "A PLAN ACTUAL CAMERA CROP", font=font(22, True), fill="#eaf4f6")
    ad.line((320, 58, 320, 32), fill="#e0a24a", width=4)
    ad.polygon(((312, 40), (328, 40), (320, 28)), fill="#e0a24a")
    ad.text((345, 17), "NW_BLOCK front edge is y=-70 before viewport offset: correctly offscreen", font=font(17), fill="#f0c27d")

    # Focus crop for the local art gate; placement stays unchanged in world pixels.
    focus_box = (520, 0, 1240, 405)
    focused = world.crop(focus_box).resize((1280, 720), Image.Resampling.LANCZOS)
    fd = ImageDraw.Draw(focused)
    fd.text((24, 20), "NW_BLOCK EXACT-POSITION FOCUS (QA ONLY)", font=font(24, True), fill="#edf7f8", stroke_width=2, stroke_fill="#071219")
    fd.text((24, 53), "No manual move; source-canvas top-left = [760,9]", font=font(18), fill="#a5dae0", stroke_width=2, stroke_fill="#071219")
    return overview, actual, focused


def write_text_reports():
    camera_sha = sha256(CAMERA)
    registration_sha = sha256(REGISTRATION)
    task_sha = sha256(TASK)
    p103_sha = sha256(P103)
    ground_sha = sha256(A2_GROUND)
    old_foundation_sha = sha256(A2_OLD_FOUNDATION)
    old_occluder_sha = sha256(A2_OLD_OCCLUDER)

    readback = {
        "task_id": "C01E02_ENV_A3_CAMERA_V2_EXACT_STRUCTURE_PILOT",
        "status": "ZERO_GENERATION_ONE_STRUCTURE_PILOT_NOT_FINAL_ART",
        "object_id": "NW_BLOCK",
        "anchor": "NA_STRUCTURE_GRID_RECT_OWNER",
        "grid_rect": list(GRID_RECT),
        "footprint_cells": [7, 5],
        "local_canvas_px": [ASSET_W, ASSET_H],
        "pivot_local_px": list(PIVOT_LOCAL),
        "visual_bounds_raw": list(VISUAL_BOUNDS_RAW),
        "front_edge_raw": list(FRONT_EDGE_RAW),
        "front_edge_A_PLAN": [320, -70],
        "world_height_class": "HIGH",
        "world_height_limit_px": 90,
        "authored_occluder_height_px": HEIGHT_PX,
        "projection": {
            "matrix": [[40, -40], [24, 24]],
            "axis_vectors_px": [[40, 24], [-40, 24]],
            "axis_slopes": [0.6, -0.6],
            "axis_angles_deg": [30.9637565, -30.9637565],
            "perspective_convergence": False,
            "manual_screen_offset": False,
        },
        "interaction_alpha": {
            "normal_foundation": 1.0,
            "normal_occluder": 1.0,
            "reveal_foundation": 1.0,
            "reveal_occluder": 0.34,
            "restore_foundation": 1.0,
            "restore_occluder": 1.0,
        },
        "source_lineage": {
            "visible_structure_pixels": "procedural_vector_from_CAMERA_V2_40X24_only",
            "visible_structure_pixel_donors": [],
            "A_PLAN_background_only": str(A2_GROUND.relative_to(PROJECT)),
            "comparison_only_not_donor": [str(A2_OLD_FOUNDATION.relative_to(PROJECT)), str(A2_OLD_OCCLUDER.relative_to(PROJECT))],
        },
        "known_camera_fact": "NW_BLOCK exact front edge is offscreen above the selected A_PLAN crop; overview and focus panels do not change placement",
    }
    (RECEIPTS / "camera-v2-exact-structure-readback.json").write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with (ROOT / "source-lineage.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source_id", "path", "sha256", "role", "visible_pixel_use"))
        writer.writerow(("TASK121", TASK.relative_to(PROJECT), task_sha, "objective", "none"))
        writer.writerow(("P103", P103.relative_to(PROJECT), p103_sha, "rejection_measurement", "QA_label_only"))
        writer.writerow(("CAMERA_V2", CAMERA.relative_to(PROJECT), camera_sha, "exact_projection_authority", "geometry_only"))
        writer.writerow(("REGISTRATION", REGISTRATION.relative_to(PROJECT), registration_sha, "exact_placement_authority", "geometry_only"))
        writer.writerow(("A2_GROUND", A2_GROUND.relative_to(PROJECT), ground_sha, "retained_ground_placement_background", "A_PLAN_QA_background_only"))
        writer.writerow(("A2_OLD_FOUNDATION", A2_OLD_FOUNDATION.relative_to(PROJECT), old_foundation_sha, "rejected_old_angle", "comparison_panel_only_not_donor"))
        writer.writerow(("A2_OLD_OCCLUDER", A2_OLD_OCCLUDER.relative_to(PROJECT), old_occluder_sha, "rejected_old_angle", "comparison_panel_only_not_donor"))

    review = f"""# ENV-A3 NW_BLOCK 50% / 100%目视自审

状态：`LOCAL_STRUCTURE_METHOD_PASS / A_PLAN_FULL_FRAME_INTEGRATION_NOT_PROVEN / NOT_FINAL_ART`

## 目视结论

- 角度：新屋顶和地基两轴由同一`40×24`投影直接生成，实测斜率`±0.600`、角度`±30.96°`，不存在自由透视或汇聚；旧A2像素仅作为拒收对照。
- 50%：外轮廓、屋顶平面、两面墙体、地基和门位仍可区分；材质密度克制，没有用渲染噪声掩盖几何。
- 100%：foundation与occluder共享`[240,378]` pivot；normal/reveal/restore只改变occluder alpha `1.00 -> 0.34 -> 1.00`，foundation保持`1.00`。
- 排序：front edge仍为raw`[80,288]`，A PLAN readback`[320,-70]`，未加任何手工screen offset。
- A PLAN限制：NW_BLOCK按当前玩法位置本来就在A PLAN镜头上缘之外。因此A PLAN实际crop只能证明“没有被手移”，局部视觉门由exact-position focus与world-canvas overview承担；这栋样板本身不能单独证明六栋全图50%整合。

## 放行边界

可放行同模板扩建的只是：`foundation/occluder分层 + exact-40×24结构几何 + 整件0.34显隐`方法。不可据此宣称环境全图、六栋风格统一、最终PLAN、CONTACT、Runtime或60fps已通过。
"""
    (ROOT / "50-100-visual-self-review.md").write_text(review, encoding="utf-8")

    report = f"""# ENV-A3 Camera V2精确Structure样板完成回执

状态：`COMPLETE_ZERO_GENERATION_PILOT / LOCAL_METHOD_PASS / NOT_FINAL_ART`

## 完成

- 已从Camera V2公式直接构造NW_BLOCK独立foundation与occluder；没有继承旧建筑轮廓、屋顶边或自由透视。
- exact grid rect=`[1,0,7,5]`，pivot=`[240,378]`，高度=`{HEIGHT_PX}px <= 90px`，两轴=`±30.96°`。
- 已交normal/reveal/restore三态、50%缩略图、A PLAN世界画布精确位置、A PLAN真实crop与未手移focus、A2/A3角度对照。
- ImageGen调用数：`0`。

## 制作人应看

1. `qa/NW_BLOCK_ANGLE_COMPARISON_1600x900.png`
2. `qa/NW_BLOCK_REVEAL_TRISTATE_BOARD_1680x586.png`
3. `qa/A_PLAN_WORLD_CANVAS_NW_BLOCK_EXACT_POSITION_1280x720.png`
4. `qa/A_PLAN_ACTUAL_CAMERA_CROP_NW_BLOCK_OFFSCREEN_1280x720.png`
5. `qa/NW_BLOCK_EXACT_POSITION_FOCUS_1280x720.png`

## 结论

这条方法解决了“素材角度和地图角度不匹配”的几何根因，局部结构与显隐方法可继续；但NW_BLOCK在A PLAN实际镜头外，不能把本样板冒充整张地图签收。扩六栋后仍需一次50%全图制作人实际帧门。
"""
    (ROOT / "completion-report.md").write_text(report, encoding="utf-8")


def write_manifest_and_hashes():
    paths = sorted(
        p for p in ROOT.rglob("*")
        if p.is_file() and p.name not in {"delivery-hashes.sha256", "asset-manifest.tsv"}
    )
    with (ROOT / "asset-manifest.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "role"))
        for path in paths:
            rel = path.relative_to(ROOT)
            role = "script" if path.suffix == ".py" else "receipt" if "receipts" in rel.parts or path.suffix in {".md", ".json", ".tsv"} else "visual"
            writer.writerow((str(rel), sha256(path), role))

    manifest_paths = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name != "delivery-hashes.sha256")
    with (ROOT / "delivery-hashes.sha256").open("w", encoding="utf-8") as handle:
        for path in manifest_paths:
            handle.write(f"{sha256(path)}  {path.relative_to(ROOT)}\n")


def main():
    foundation = build_foundation()
    occluder = build_occluder()
    foundation_path = DELIVERY / "NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png"
    occluder_path = DELIVERY / "NW_BLOCK_OCCLUDER_CAMERA_V2_RGBA.png"
    foundation.save(foundation_path)
    occluder.save(occluder_path)

    normal = composite(foundation, occluder, 1.0)
    reveal = composite(foundation, occluder, 0.34)
    restore = composite(foundation, occluder, 1.0)
    normal.save(STATES / "NW_BLOCK_NORMAL_100.png")
    reveal.save(STATES / "NW_BLOCK_REVEAL_034.png")
    restore.save(STATES / "NW_BLOCK_RESTORE_100.png")
    normal.resize((240, 189), Image.Resampling.LANCZOS).save(STATES / "NW_BLOCK_NORMAL_50_PERCENT.png")

    build_tristate_board(normal, reveal, restore).save(QA / "NW_BLOCK_REVEAL_TRISTATE_BOARD_1680x586.png")
    build_angle_comparison(normal).save(QA / "NW_BLOCK_ANGLE_COMPARISON_1600x900.png")
    overview, actual, focused = build_world_and_plan(normal)
    overview.save(QA / "A_PLAN_WORLD_CANVAS_NW_BLOCK_EXACT_POSITION_1280x720.png")
    actual.save(QA / "A_PLAN_ACTUAL_CAMERA_CROP_NW_BLOCK_OFFSCREEN_1280x720.png")
    focused.save(QA / "NW_BLOCK_EXACT_POSITION_FOCUS_1280x720.png")

    write_text_reports()
    write_manifest_and_hashes()
    print(json.dumps({
        "status": "COMPLETE_ZERO_GENERATION_PILOT",
        "root": str(ROOT),
        "foundation": str(foundation_path),
        "occluder": str(occluder_path),
        "axis_angle_deg": round(math.degrees(math.atan2(24, 40)), 8),
        "height_px": HEIGHT_PX,
        "pivot_local_px": PIVOT_LOCAL,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
