#!/usr/bin/env python3
"""Expand the passed ENV-A3 exact-40x24 method to six geometry skeletons.

This is a zero-generation geometry/alpha/placement proof, not final art.
Only the retained A2 ground is used as the shared PLAN background; no rejected
A1/A2 structure or tactical-object pixels are consumed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
A3 = ROOT.parent
PROJECT = Path(__file__).resolve().parents[7]
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
A2_GROUND = A3.parent / "art-a9-1a6-env-a2-simple-recomposition/delivery/GROUND_BAKE_CURRENT_V2_2400x1350.png"
TASK121 = A3.parent / "121-c01e02-env-a3-camera-v2-exact-structure-pilot-objective.md"

DELIVERY = ROOT / "delivery/structures"
QA = ROOT / "qa"
RECEIPTS = ROOT / "receipts"
for directory in (DELIVERY, QA, RECEIPTS):
    directory.mkdir(parents=True, exist_ok=True)

SCALE = 4
EXPECTED = {
    "NW_BLOCK": ([1, 0, 7, 5], 90),
    "NM_BLOCK": ([10, 0, 5, 4], 72),
    "NE_BLOCK": ([22, 0, 7, 4], 90),
    "SW_BLOCK": ([0, 15, 8, 3], 72),
    "SE_BLOCK": ([26, 14, 6, 4], 90),
    "BROKEN_SKYWALK": ([8, 5, 7, 2], 54),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_font(size: int, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def parse_csv_ints(value: str):
    return [int(v) for v in value.split(",")]


def load_contracts():
    camera = json.loads(CAMERA.read_text(encoding="utf-8"))
    structures = {row["object_id"]: row for row in camera["structures"]}
    with REGISTRATION.open(encoding="utf-8", newline="") as handle:
        rows = {row["object_id"]: row for row in csv.DictReader(handle, delimiter="\t") if row["record_type"] == "STRUCTURE"}
    for object_id, (grid_rect, height) in EXPECTED.items():
        assert structures[object_id]["grid_rect"] == grid_rect
        assert int(rows[object_id]["world_height_px"]) == height
    return camera, structures, rows


def rgb(hex_value: str):
    value = hex_value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def shade(hex_value: str, factor: float):
    return tuple(max(0, min(255, round(c * factor))) for c in rgb(hex_value)) + (255,)


def project_local(x, y, bounds):
    return (x - y) * 40 - bounds[0], (x + y) * 24 - bounds[1]


def hs(point):
    return round(point[0] * SCALE), round(point[1] * SCALE)


def poly(draw, points, fill, outline=None, width=1):
    points = [hs(p) for p in points]
    draw.polygon(points, fill=fill)
    if outline:
        draw.line(points + [points[0]], fill=outline, width=width * SCALE, joint="curve")


def line(draw, points, fill, width=1):
    draw.line([hs(p) for p in points], fill=fill, width=width * SCALE, joint="curve")


def lerp(a, b, t):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def shift(point, height):
    return point[0], point[1] - height


def downsample(image, size):
    return image.resize(size, Image.Resampling.LANCZOS)


def footprint_points(grid_rect, bounds, inset=0.0):
    x, y, w, h = grid_rect
    x0, y0 = x - 0.5 + inset, y - 0.5 + inset
    x1, y1 = x + w - 0.5 - inset, y + h - 0.5 - inset
    return [
        project_local(x0, y0, bounds),
        project_local(x1, y0, bounds),
        project_local(x1, y1, bounds),
        project_local(x0, y1, bounds),
    ]


def face_panel(roof_a, roof_b, base_a, base_b, u0, u1, t0, t1):
    ra, rb = lerp(roof_a, roof_b, u0), lerp(roof_a, roof_b, u1)
    ba, bb = lerp(base_a, base_b, u0), lerp(base_a, base_b, u1)
    return [lerp(ra, ba, t0), lerp(rb, bb, t0), lerp(rb, bb, t1), lerp(ra, ba, t1)]


def build_foundation(spec, row):
    bounds = parse_csv_ints(row["visual_bounds_raw"])
    size = (bounds[2], bounds[3])
    image = Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    outer = footprint_points(spec["grid_rect"], bounds, 0.0)
    curb = footprint_points(spec["grid_rect"], bounds, 0.18)
    pad = footprint_points(spec["grid_rect"], bounds, 0.32)
    base = "#" + spec["foundation"]["color"]
    poly(d, outer, shade(base, 0.62), "#07161d", 3)
    poly(d, curb, shade(base, 1.35), shade(base, 1.75), 2)
    poly(d, pad, shade(base, 1.0), shade(base, 0.65), 2)

    x, y, w, h = spec["grid_rect"]
    # Sparse exact-axis joints; all slopes are inherited from 40x24 projection.
    for ratio in (0.33, 0.66):
        gx = x - 0.5 + 0.32 + (w - 0.64) * ratio
        line(d, [project_local(gx, y - 0.18, bounds), project_local(gx, y + h - 0.82, bounds)], shade(base, 1.35), 1)
    if h >= 3:
        gy = y - 0.5 + h * 0.62
        line(d, [project_local(x - 0.18, gy, bounds), project_local(x + w - 0.82, gy, bounds)], shade(base, 0.72), 1)
    return downsample(image, size)


def draw_box(draw, grid_rect, bounds, height, color, inset=0.4, bay_count=3, amber=False):
    base = footprint_points(grid_rect, bounds, inset)
    a, b, c, dd = base
    ar, br, cr, dr = [shift(p, height) for p in base]
    edge = shade(color, 0.30)
    poly(draw, [br, cr, c, b], shade(color, 0.78), edge, 3)
    poly(draw, [dr, cr, c, dd], shade(color, 0.58), edge, 3)

    gap = 0.08
    usable = 1.0 - gap * 2
    bay_w = usable / bay_count
    for index in range(bay_count):
        u0 = gap + index * bay_w + 0.035
        u1 = gap + (index + 1) * bay_w - 0.035
        poly(draw, face_panel(br, cr, b, c, u0, u1, 0.32, 0.78), shade(color, 0.96), shade(color, 0.42), 1)
        poly(draw, face_panel(dr, cr, dd, c, u0, u1, 0.30, 0.77), shade(color, 0.86), shade(color, 0.38), 1)

    poly(draw, [ar, br, cr, dr], shade(color, 1.08), edge, 3)
    roof = footprint_points(grid_rect, bounds, inset + 0.22)
    roof = [shift(p, height) for p in roof]
    poly(draw, roof, shade(color, 1.18), shade(color, 1.5), 2)

    x, y, w, h = grid_rect
    # One flat roof hatch and two exact-axis seams: no additional camera language.
    hx0, hy0 = x + w * 0.38, y + h * 0.33
    hatch = [
        project_local(hx0, hy0, bounds),
        project_local(hx0 + max(0.8, w * 0.18), hy0, bounds),
        project_local(hx0 + max(0.8, w * 0.18), hy0 + max(0.45, h * 0.18), bounds),
        project_local(hx0, hy0 + max(0.45, h * 0.18), bounds),
    ]
    hatch = [shift(p, height) for p in hatch]
    poly(draw, hatch, shade(color, 0.62), shade(color, 1.65), 1)
    for ratio in (0.35, 0.68):
        gx = x - 0.5 + inset + (w - 2 * inset) * ratio
        line(draw, [shift(project_local(gx, y - 0.5 + inset + 0.1, bounds), height), shift(project_local(gx, y + h - 0.5 - inset - 0.1, bounds), height)], shade(color, 0.78), 1)

    if amber:
        poly(draw, face_panel(dr, cr, dd, c, 0.42, 0.62, 0.49, 0.57), "#b47834", None)


def build_occluder(object_id, spec, row):
    bounds = parse_csv_ints(row["visual_bounds_raw"])
    size = (bounds[2], bounds[3])
    height = int(row["world_height_px"])
    color = "#" + spec["occluder"]["color"]
    image = Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    x, y, w, h = spec["grid_rect"]

    if object_id == "BROKEN_SKYWALK":
        # Two exact-axis low bridgeheads separated by a readable broken gap.
        left = [x, y, 3, h]
        right = [x + 4, y, 3, h]
        draw_box(d, left, bounds, height, color, inset=0.22, bay_count=2, amber=False)
        draw_box(d, right, bounds, height, color, inset=0.22, bay_count=2, amber=False)
        # Broken deck lips point toward the gap but never change the 7x2 footprint.
        for gx0, gx1 in ((x + 2.45, x + 3.25), (x + 3.75, x + 4.55)):
            deck = [
                project_local(gx0, y + 0.35, bounds),
                project_local(gx1, y + 0.35, bounds),
                project_local(gx1, y + h - 0.35, bounds),
                project_local(gx0, y + h - 0.35, bounds),
            ]
            deck = [shift(p, height * 0.78) for p in deck]
            poly(d, deck, shade(color, 1.15), shade(color, 0.35), 2)
    else:
        bay_count = 4 if w >= 7 else 3
        inset = 0.38 if h >= 4 else 0.28
        draw_box(d, spec["grid_rect"], bounds, height, color, inset=inset, bay_count=bay_count, amber=object_id in {"NW_BLOCK", "NE_BLOCK", "SE_BLOCK"})
    return downsample(image, size)


def alpha_scaled(image, factor):
    out = image.copy()
    out.putalpha(out.getchannel("A").point(lambda p: round(p * factor)))
    return out


def composite(foundation, occluder, alpha=1.0):
    out = foundation.copy()
    out.alpha_composite(alpha_scaled(occluder, alpha))
    return out


def build_catalogue(assets, rows):
    board = Image.new("RGBA", (1800, 1120), "#071219")
    d = ImageDraw.Draw(board)
    d.text((32, 22), "SIX CAMERA V2 EXACT STRUCTURE SKELETONS", font=get_font(34, True), fill="#eff7f8")
    d.text((32, 66), "Every visible diagonal derives from (40,24) / (-40,24); geometry proof, not final art", font=get_font(21), fill="#91c2ca")
    panel_w, panel_h = 580, 480
    for index, object_id in enumerate(EXPECTED):
        column, row_index = index % 3, index // 3
        x0, y0 = 20 + column * 590, 120 + row_index * 490
        d.rectangle((x0, y0, x0 + panel_w - 10, y0 + panel_h - 10), fill="#0d222b", outline="#315661", width=2)
        asset = assets[object_id]
        factor = min(500 / asset.width, 340 / asset.height)
        display = asset.resize((round(asset.width * factor), round(asset.height * factor)), Image.Resampling.LANCZOS)
        board.alpha_composite(display, (x0 + (panel_w - 10 - display.width) // 2, y0 + 76 + (330 - display.height) // 2))
        height = rows[object_id]["world_height_px"]
        d.text((x0 + 18, y0 + 16), object_id, font=get_font(24, True), fill="#eef7f8")
        d.text((x0 + 18, y0 + 47), f"grid {EXPECTED[object_id][0]} | height {height}px | slope +/-0.600", font=get_font(17), fill="#8ed0d8")
        d.text((x0 + 18, y0 + 438), "foundation 1.00 | occluder 1.00 / reveal 0.34", font=get_font(16), fill="#b3d8dd")
    return board


def build_shared_plan(assets, camera, rows):
    ground = Image.open(A2_GROUND).convert("RGBA")
    world = ground.copy()
    origin = camera["projection"]["world_canvas"]["world_canvas_origin_raw_px"]

    # Foundations are always visible and remain below every occluder.
    for object_id in EXPECTED:
        bounds = parse_csv_ints(rows[object_id]["visual_bounds_raw"])
        pos = (bounds[0] - origin[0], bounds[1] - origin[1])
        world.alpha_composite(assets[object_id]["foundation"], pos)

    # Stable front-edge depth order; no manual offsets or category-layer tricks.
    ordered = sorted(EXPECTED, key=lambda object_id: parse_csv_ints(rows[object_id]["front_edge_raw"])[1])
    for object_id in ordered:
        bounds = parse_csv_ints(rows[object_id]["visual_bounds_raw"])
        pos = (bounds[0] - origin[0], bounds[1] - origin[1])
        world.alpha_composite(assets[object_id]["occluder"], pos)

    profile = camera["projection"]["camera_profiles"]["A_PLAN"]
    crop = profile["source_canvas_crop_px"]
    frame = Image.new("RGBA", (1280, 720), "#071219")
    frame.alpha_composite(world.crop((crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3])), (0, 58))
    d = ImageDraw.Draw(frame)
    d.text((22, 15), "SHARED A PLAN | SIX EXACT STRUCTURE SKELETONS", font=get_font(22, True), fill="#eef7f8")
    d.text((710, 17), "40x24 / +/-30.96 deg / no manual move / NOT FINAL ART", font=get_font(16), fill="#91c9d1")
    return frame


def write_readback(structures, rows, paths):
    with (RECEIPTS / "six-structure-camera-v2-readback.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("object_id", "grid_rect", "footprint", "local_canvas_px", "pivot_local_px", "front_edge_raw", "world_height_px", "axis_slopes", "axis_angles_deg", "foundation_alpha", "occluder_normal_alpha", "occluder_reveal_alpha", "manual_offset", "foundation_sha256", "occluder_sha256"))
        for object_id in EXPECTED:
            row = rows[object_id]
            bounds = parse_csv_ints(row["visual_bounds_raw"])
            front = parse_csv_ints(row["front_edge_raw"])
            pivot = [front[0] - bounds[0], front[1] - bounds[1]]
            grid = structures[object_id]["grid_rect"]
            writer.writerow((
                object_id,
                ",".join(map(str, grid)),
                f"{grid[2]},{grid[3]}",
                f"{bounds[2]},{bounds[3]}",
                ",".join(map(str, pivot)),
                row["front_edge_raw"],
                row["world_height_px"],
                "+0.600;-0.600",
                "+30.9637565;-30.9637565",
                "1.00",
                "1.00",
                "0.34",
                "false",
                sha(paths[object_id]["foundation"]),
                sha(paths[object_id]["occluder"]),
            ))

    (ROOT / "source-lineage.tsv").write_text(
        "source_id\tpath\tsha256\trole\tvisible_pixel_use\n"
        f"CAMERA_V2\t{CAMERA.relative_to(PROJECT)}\t{sha(CAMERA)}\texact geometry/placement\tgeometry only\n"
        f"REGISTRATION\t{REGISTRATION.relative_to(PROJECT)}\t{sha(REGISTRATION)}\tpivot/bounds/height\tgeometry only\n"
        f"TASK121\t{TASK121.relative_to(PROJECT)}\t{sha(TASK121)}\tpassed method authority\tnone\n"
        f"A2_GROUND\t{A2_GROUND.relative_to(PROJECT)}\t{sha(A2_GROUND)}\tretained PLAN background\tbackground only\n",
        encoding="utf-8",
    )
    (ROOT / "completion-report.md").write_text(
        "# ENV-A3六Structure Camera V2几何骨架回执\n\n"
        "状态：`COMPLETE_ZERO_GENERATION_GEOMETRY_SKELETON / NOT_FINAL_ART`\n\n"
        "- 六栋沿用原grid_rect、footprint、front edge、pivot及90/72/54px高度；没有玩法坐标变化。\n"
        "- 每栋foundation/occluder独立RGBA，所有主边均由40×24公式直接生成，斜率±0.600、角度±30.96°。\n"
        "- 共享A PLAN只证明相机角度、放置和简单排序；NW/SW等镜头外结构未被手移进画面。\n"
        "- ImageGen=0；未消费旧建筑像素；不是最终美术、Runtime或整图制作人签收。\n",
        encoding="utf-8",
    )


def write_hashes():
    paths = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name not in {"delivery-hashes.sha256", "asset-manifest.tsv"})
    with (ROOT / "asset-manifest.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256"))
        for path in paths:
            writer.writerow((path.relative_to(ROOT), sha(path)))
    paths = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name != "delivery-hashes.sha256")
    (ROOT / "delivery-hashes.sha256").write_text("".join(f"{sha(path)}  {path.relative_to(ROOT)}\n" for path in paths), encoding="utf-8")


def main():
    camera, structures, rows = load_contracts()
    assets = {}
    paths = {}
    for object_id in EXPECTED:
        foundation = build_foundation(structures[object_id], rows[object_id])
        occluder = build_occluder(object_id, structures[object_id], rows[object_id])
        foundation_path = DELIVERY / f"{object_id}_FOUNDATION_CAMERA_V2_RGBA.png"
        occluder_path = DELIVERY / f"{object_id}_OCCLUDER_CAMERA_V2_RGBA.png"
        foundation.save(foundation_path)
        occluder.save(occluder_path)
        assets[object_id] = {
            "foundation": foundation,
            "occluder": occluder,
            "normal": composite(foundation, occluder),
        }
        paths[object_id] = {"foundation": foundation_path, "occluder": occluder_path}

    build_catalogue({key: value["normal"] for key, value in assets.items()}, rows).save(QA / "SIX_STRUCTURE_EXACT_GEOMETRY_BOARD_1800x1120.png")
    build_shared_plan(assets, camera, rows).save(QA / "SHARED_A_PLAN_SIX_STRUCTURE_CAMERA_V2_1280x720.png")
    write_readback(structures, rows, paths)
    write_hashes()
    print(json.dumps({
        "status": "COMPLETE_ZERO_GENERATION_SIX_STRUCTURE_GEOMETRY_SKELETON",
        "structure_count": len(assets),
        "axis_slopes": [0.6, -0.6],
        "axis_angles_deg": [math.degrees(math.atan2(24, 40)), -math.degrees(math.atan2(24, 40))],
        "root": str(ROOT),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
