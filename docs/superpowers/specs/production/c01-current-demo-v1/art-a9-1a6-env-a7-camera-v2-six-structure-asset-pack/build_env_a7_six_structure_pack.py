#!/usr/bin/env python3
"""Build six differentiated Camera V2 structure assets for ENV-A7."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
import shutil
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = Path(__file__).resolve().parents[6]
C01 = ROOT.parent
TASK121 = C01 / "art-a9-1a6-env-a3-camera-v2-exact-structure-pilot/six-structure"
A6 = C01 / "art-a9-1a6-env-a6-camera-v2-one-structure-material-pilot"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
OBJECTIVE = ROOT / "A7-six-structure-asset-pack-objective.md"

DELIVERY = ROOT / "delivery/structures"
STATES = ROOT / "qa/states"
QA = ROOT / "qa"
RECEIPTS = ROOT / "receipts"
for directory in (DELIVERY, STATES, QA, RECEIPTS):
    directory.mkdir(parents=True, exist_ok=True)

SCALE = 4


BUILDINGS = {
    "NW_BLOCK": {
        "role": "exhibition_maintenance_hall",
        "role_cn": "展馆维修厅",
        "grid_rect": [1, 0, 7, 5], "bounds": [-160, -90, 480, 378], "pivot": [240, 378], "front": [80, 288], "height": 90,
        "inherit_a6": True,
        "signature": "stepped_low_hall_offset_equipment_room_short_south_eave",
    },
    "NM_BLOCK": {
        "role": "office_security_annex", "role_cn": "中型办公／安保附楼",
        "grid_rect": [10, 0, 5, 4], "bounds": [240, 144, 360, 288], "pivot": [180, 288], "front": [420, 432], "height": 72,
        "volumes": [
            ((9.90, -0.10, 13.25, 2.40), 0, 36, "main"),
            ((12.75, 0.15, 14.12, 1.50), 0, 72, "tower"),
            ((10.00, 2.15, 11.55, 3.32), 0, 24, "eave"),
        ],
        "palette": {
            "main": ((67, 79, 84), (42, 53, 59), (34, 43, 49)),
            "tower": ((82, 96, 100), (48, 62, 68), (39, 51, 57)),
            "eave": ((103, 114, 116), (61, 72, 76), (49, 59, 63)),
        },
        "signature": "low_office_bar_front_doorhouse_and_full_72px_corner_watch_tower",
    },
    "NE_BLOCK": {
        "role": "warehouse_transport_hall", "role_cn": "仓储／交通厅",
        "grid_rect": [22, 0, 7, 4], "bounds": [720, 414, 440, 354], "pivot": [220, 354], "front": [940, 768], "height": 90,
        "volumes": [
            ((21.90, -0.10, 28.10, 3.08), 0, 44, "hall"),
            ((22.50, 0.08, 27.40, 0.82), 44, 62, "spine"),
            ((22.90, 2.80, 27.45, 3.35), 24, 30, "loading_eave"),
        ],
        "palette": {
            "hall": ((43, 79, 78), (27, 59, 59), (22, 48, 49)),
            "spine": ((65, 102, 98), (38, 72, 70), (31, 60, 59)),
            "loading_eave": ((83, 113, 108), (48, 78, 76), (38, 65, 64)),
        },
        "signature": "long_low_hall_continuous_roof_spine_wide_loading_face",
    },
    "SW_BLOCK": {
        "role": "segmented_service_corridor", "role_cn": "服务廊",
        "grid_rect": [0, 15, 8, 3], "bounds": [-720, 264, 440, 336], "pivot": [220, 336], "front": [-500, 600], "height": 72,
        "volumes": [
            ((-0.10, 14.90, 3.05, 17.10), 0, 38, "west"),
            ((4.65, 14.80, 7.10, 17.05), 0, 46, "east"),
            ((2.80, 15.25, 4.95, 16.70), 22, 34, "connector"),
            ((0.20, 16.78, 6.85, 17.30), 22, 28, "walkway"),
        ],
        "palette": {
            "west": ((82, 74, 69), (55, 48, 45), (44, 39, 37)),
            "east": ((92, 82, 75), (62, 53, 49), (50, 44, 41)),
            "connector": ((112, 99, 90), (72, 62, 57), (58, 51, 47)),
            "walkway": ((103, 92, 85), (65, 57, 53), (52, 47, 44)),
        },
        "signature": "very_long_two_end_service_bars_recessed_connector_side_walkway",
    },
    "SE_BLOCK": {
        "role": "equipment_energy_station", "role_cn": "设备／能源站",
        "grid_rect": [26, 14, 6, 4], "bounds": [320, 846, 400, 330], "pivot": [200, 330], "front": [520, 1176], "height": 90,
        "volumes": [
            ((25.90, 14.15, 30.90, 16.80), 0, 18, "deck"),
            ((26.00, 13.95, 27.55, 15.75), 18, 88, "energy"),
            ((28.75, 14.05, 30.45, 15.55), 18, 68, "plant"),
            ((27.25, 15.75, 30.90, 17.10), 0, 24, "transformer"),
        ],
        "palette": {
            "deck": ((63, 82, 90), (40, 57, 65), (32, 47, 54)),
            "plant": ((76, 99, 106), (45, 68, 76), (36, 56, 64)),
            "energy": ((91, 113, 120), (55, 78, 86), (45, 65, 72)),
            "transformer": ((70, 91, 99), (43, 63, 71), (34, 52, 59)),
        },
        "signature": "low_base_separated_88px_energy_peak_68px_plant_peak_front_heat_exchange_row",
    },
    "BROKEN_SKYWALK": {
        "role": "broken_low_skywalk", "role_cn": "低矮断连廊",
        "grid_rect": [8, 5, 7, 2], "bounds": [40, 234, 360, 270], "pivot": [180, 270], "front": [220, 504], "height": 54,
        "volumes": [
            ((7.90, 4.80, 10.05, 6.20), 0, 38, "left_head"),
            ((12.05, 4.80, 14.10, 6.20), 0, 44, "right_head"),
            ((9.65, 5.02, 10.80, 5.98), 27, 33, "left_tongue"),
            ((11.45, 5.02, 12.30, 5.98), 29, 35, "right_tongue"),
        ],
        "palette": {
            "left_head": ((92, 82, 98), (61, 53, 67), (49, 43, 55)),
            "right_head": ((103, 91, 108), (68, 58, 73), (55, 48, 61)),
            "left_tongue": ((115, 103, 120), (73, 64, 78), (59, 53, 65)),
            "right_tongue": ((123, 110, 128), (78, 68, 83), (63, 56, 69)),
        },
        "signature": "two_bridgeheads_two_broken_tongues_clear_center_gap",
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def project(spec, x, y, z=0.0):
    bounds = spec["bounds"]
    return (x - y) * 40 - bounds[0], (x + y) * 24 - bounds[1] - z


def corners(spec, rect, z):
    x0, y0, x1, y1 = rect
    return [project(spec, x0, y0, z), project(spec, x1, y0, z), project(spec, x1, y1, z), project(spec, x0, y1, z)]


def mask_polygon(spec, points):
    width, height = spec["bounds"][2:]
    image = Image.new("L", (width * SCALE, height * SCALE), 0)
    ImageDraw.Draw(image).polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=255)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def volume_masks(spec, rect, z0, z1):
    a, b, c, d = corners(spec, rect, z0)
    at, bt, ct, dt = corners(spec, rect, z1)
    return {
        "roof": mask_polygon(spec, [at, bt, ct, dt]),
        "east": mask_polygon(spec, [bt, ct, c, b]),
        "south": mask_polygon(spec, [dt, ct, c, d]),
    }


def value_field(size, color, seed, amplitude=6, coarse=58):
    rng = random.Random(seed)
    width = max(3, math.ceil(size[0] / coarse) + 2)
    height = max(3, math.ceil(size[1] / coarse) + 2)
    grid = Image.new("L", (width, height))
    grid.putdata([128 + rng.randint(-amplitude, amplitude) for _ in range(width * height)])
    field = grid.resize(size, Image.Resampling.BICUBIC)
    return ImageChops.add(Image.new("RGB", size, color), Image.merge("RGB", (field, field, field)), scale=1.0, offset=-128)


def paint(canvas, mask, color, seed, amplitude=6):
    canvas.paste(value_field(canvas.size, color, seed, amplitude), (0, 0), mask)


def hs(point):
    return round(point[0] * SCALE), round(point[1] * SCALE)


def poly(draw, points, fill, outline=None, width=1):
    scaled = [hs(point) for point in points]
    draw.polygon(scaled, fill=fill)
    if outline:
        draw.line(scaled + [scaled[0]], fill=outline, width=width * SCALE, joint="curve")


def line(draw, points, fill, width=1):
    draw.line([hs(point) for point in points], fill=fill, width=width * SCALE, joint="curve")


def face_south(spec, x0, x1, y, z0, z1):
    return [project(spec, x0, y, z1), project(spec, x1, y, z1), project(spec, x1, y, z0), project(spec, x0, y, z0)]


def face_east(spec, x, y0, y1, z0, z1):
    return [project(spec, x, y0, z1), project(spec, x, y1, z1), project(spec, x, y1, z0), project(spec, x, y0, z0)]


def draw_volume_edges(draw, spec):
    for rect, z0, z1, _ in spec["volumes"]:
        base = corners(spec, rect, z0)
        top = corners(spec, rect, z1)
        line(draw, top + [top[0]], "#0b2028", 2)
        _, b, c, d = base
        _, bt, ct, dt = top
        line(draw, [bt, b, c, ct], "#0b2028", 2)
        line(draw, [dt, d, c, ct], "#0b2028", 2)


def exact_roof_inset(draw, spec, rect, z, amount=0.15):
    x0, y0, x1, y1 = rect
    inset = min(amount, (x1 - x0) * 0.08, (y1 - y0) * 0.08)
    pts = corners(spec, (x0 + inset, y0 + inset, x1 - inset, y1 - inset), z)
    line(draw, pts + [pts[0]], "#6d858b", 1)


def draw_role_details(object_id, spec, alpha):
    width, height = spec["bounds"][2:]
    overlay = Image.new("RGBA", (width * SCALE, height * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_volume_edges(draw, spec)

    if object_id == "NM_BLOCK":
        exact_roof_inset(draw, spec, spec["volumes"][0][0], 36)
        band = face_south(spec, 10.12, 12.96, 2.402, 10, 27)
        poly(draw, band, "#172b33", "#526970", 1)
        for x0, x1 in ((10.22, 10.92), (11.02, 11.72), (11.82, 12.52)):
            poly(draw, face_south(spec, x0, x1, 2.404, 13, 25), "#344e57", "#6b7d81", 1)
        poly(draw, face_south(spec, 10.20, 11.38, 3.322, 2, 21), "#1b272d", "#9b6b3b", 1)
        # High corner watch glazing is the role-defining block.
        poly(draw, face_east(spec, 14.122, 0.28, 1.38, 27, 62), "#19343e", "#789097", 1)
        line(draw, [project(spec, 14.124, 0.82, 27), project(spec, 14.124, 0.82, 62)], "#74898e", 1)
        for x, y in ((10.12, 3.325), (14.00, 1.40)):
            line(draw, [project(spec, x, y, 6), project(spec, x, y, 13)], "#cf883f", 2)

    elif object_id == "NE_BLOCK":
        exact_roof_inset(draw, spec, spec["volumes"][0][0], 44)
        # Long roof drain and clerestory band.
        poly(draw, corners(spec, (22.25, 2.66, 27.75, 2.86), 44.2), "#15383a", "#63817f", 1)
        poly(draw, face_south(spec, 22.72, 27.18, 0.822, 49, 58), "#183b3b", "#73908c", 1)
        for x in (23.55, 24.45, 25.35, 26.25):
            line(draw, [project(spec, x, 0.824, 49), project(spec, x, 0.824, 58)], "#7b928e", 1)
        # Two broad loading portals.
        for x0, x1 in ((23.15, 25.05), (25.25, 27.15)):
            poly(draw, face_south(spec, x0, x1, 3.084, 2, 27), "#122d31", "#5f7978", 1)
            line(draw, [project(spec, x0 + 0.15, 3.086, 10), project(spec, x1 - 0.15, 3.086, 10)], "#486765", 1)
        for x in (23.02, 27.28):
            line(draw, [project(spec, x, 3.091, 7), project(spec, x, 3.091, 14)], "#d18a3f", 2)

    elif object_id == "SW_BLOCK":
        exact_roof_inset(draw, spec, spec["volumes"][0][0], 38)
        exact_roof_inset(draw, spec, spec["volumes"][1][0], 46)
        # Long service-window rhythm split by the central recessed connector.
        for x0, x1, y in ((0.12, 2.82, 17.102), (4.86, 6.92, 17.052)):
            poly(draw, face_south(spec, x0, x1, y, 11, 25), "#282f31", "#756d68", 1)
        for x in (0.72, 1.40, 2.08, 5.42, 6.10):
            line(draw, [project(spec, x, 17.106 if x < 3 else 17.056, 11), project(spec, x, 17.106 if x < 3 else 17.056, 25)], "#8d8179", 1)
        poly(draw, face_south(spec, 3.02, 4.74, 16.702, 24, 32), "#34383a", "#8b817c", 1)
        for x in (0.30, 6.72):
            line(draw, [project(spec, x, 17.31, 5), project(spec, x, 17.31, 12)], "#c98546", 2)

    elif object_id == "SE_BLOCK":
        exact_roof_inset(draw, spec, spec["volumes"][0][0], 18)
        # Separated high energy peak, medium plant peak and front heat-exchange row.
        poly(draw, face_south(spec, 26.12, 27.42, 15.752, 31, 76), "#18313a", "#6d848b", 1)
        for z in (39, 49, 59, 69):
            line(draw, [project(spec, 26.22, 15.754, z), project(spec, 27.32, 15.754, z)], "#788d92", 1)
        poly(draw, face_east(spec, 30.452, 14.22, 15.40, 30, 60), "#172f38", "#789097", 1)
        for y in (14.48, 14.78, 15.08):
            line(draw, [project(spec, 30.454, y, 33), project(spec, 30.454, y, 57)], "#6e858b", 1)
        poly(draw, face_south(spec, 27.45, 30.65, 17.102, 3, 20), "#1b333b", "#647b82", 1)
        for x, y, z0, z1 in ((26.08, 15.76, 24, 34), (28.82, 15.56, 24, 34), (30.68, 17.11, 5, 13)):
            line(draw, [project(spec, x, y, z0), project(spec, x, y, z1)], "#d18a3f", 2)

    elif object_id == "BROKEN_SKYWALK":
        # Large side truss panels, not dense linework; dark cut faces identify the break.
        for x0, x1 in ((8.08, 9.86), (12.22, 13.92)):
            poly(draw, face_south(spec, x0, x1, 6.202, 9, 29), "#322d38", "#8a7c8e", 1)
            mid = (x0 + x1) / 2
            line(draw, [project(spec, x0 + 0.12, 6.204, 10), project(spec, mid, 6.204, 28), project(spec, x1 - 0.12, 6.204, 10)], "#8f8194", 1)
        poly(draw, face_east(spec, 10.802, 5.08, 5.92, 27, 33), "#19141e", "#a06a54", 1)
        poly(draw, face_east(spec, 11.448, 5.08, 5.92, 29, 35), "#19141e", "#a06a54", 1)
        for x, y in ((8.12, 6.21), (13.88, 6.21)):
            line(draw, [project(spec, x, y, 6), project(spec, x, y, 13)], "#c98546", 2)

    overlay = overlay.resize((width, height), Image.Resampling.LANCZOS)
    overlay.putalpha(ImageChops.multiply(overlay.getchannel("A"), alpha))
    return overlay


def build_authored_structure(object_id, spec):
    width, height = spec["bounds"][2:]
    masks_by_volume = []
    alpha = Image.new("L", (width, height), 0)
    for rect, z0, z1, key in spec["volumes"]:
        masks = volume_masks(spec, rect, z0, z1)
        masks_by_volume.append((key, masks))
        for mask in masks.values():
            alpha = ImageChops.lighter(alpha, mask)

    canvas = Image.new("RGB", (width, height), "#132630")
    for index, (key, masks) in enumerate(masks_by_volume):
        roof, east, south = spec["palette"][key]
        paint(canvas, masks["east"], east, 7100 + index * 101, 5)
        paint(canvas, masks["south"], south, 7117 + index * 101, 5)
        paint(canvas, masks["roof"], roof, 7134 + index * 101, 7)

    result = canvas.convert("RGBA")
    result.putalpha(alpha)
    result.alpha_composite(draw_role_details(object_id, spec, alpha))
    result.putalpha(alpha)
    pixels = result.load()
    for y in range(height):
        for x in range(width):
            if pixels[x, y][3] == 0:
                pixels[x, y] = (0, 0, 0, 0)
    return result


def source_foundation_path(object_id):
    if object_id == "NW_BLOCK":
        return A6 / "delivery/NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png"
    return TASK121 / f"delivery/structures/{object_id}_FOUNDATION_CAMERA_V2_RGBA.png"


def output_paths(object_id):
    return (
        DELIVERY / f"{object_id}_FOUNDATION_CAMERA_V2_RGBA.png",
        DELIVERY / f"{object_id}_OCCLUDER_CAMERA_V2_RGBA.png",
    )


def alpha_scaled(image, factor):
    out = image.copy()
    out.putalpha(out.getchannel("A").point(lambda value: round(value * factor)))
    return out


def combined(foundation, occluder, factor=1.0):
    out = foundation.copy()
    out.alpha_composite(alpha_scaled(occluder, factor))
    return out


def fit(asset, max_w, max_h):
    factor = min(max_w / asset.width, max_h / asset.height)
    return asset.resize((round(asset.width * factor), round(asset.height * factor)), Image.Resampling.LANCZOS)


def group_board(assets):
    board = Image.new("RGBA", (1800, 1120), "#071219")
    draw = ImageDraw.Draw(board)
    draw.text((32, 22), "A7 SIX CAMERA V2 INDEPENDENT STRUCTURES", font=font(34, True), fill="#eff7f8")
    draw.text((32, 66), "role-distinct silhouettes / exact 40x24 / independent foundation + occluder / NOT PLAN", font=font(21), fill="#91c2ca")
    panel_w, panel_h = 580, 480
    for index, object_id in enumerate(BUILDINGS):
        col, row = index % 3, index // 3
        x0, y0 = 20 + col * 590, 120 + row * 490
        draw.rectangle((x0, y0, x0 + panel_w - 10, y0 + panel_h - 10), fill="#0d222b", outline="#315661", width=2)
        shown = fit(assets[object_id]["combined"], 500, 330)
        board.alpha_composite(shown, (x0 + (570 - shown.width) // 2, y0 + 82 + (330 - shown.height) // 2))
        spec = BUILDINGS[object_id]
        draw.text((x0 + 18, y0 + 14), object_id, font=font(24, True), fill="#eef7f8")
        draw.text((x0 + 18, y0 + 45), spec["role_cn"], font=font(17), fill="#8ed0d8")
        draw.text((x0 + 18, y0 + 435), f"height <= {spec['height']}px | alpha 1.00 / 0.34 / 1.00", font=font(15), fill="#b3d8dd")
    path100 = QA / "A7_SIX_STRUCTURE_GROUP_BOARD_1800x1120.png"
    path50 = QA / "A7_SIX_STRUCTURE_GROUP_BOARD_50_PERCENT_900x560.png"
    board.save(path100)
    board.resize((900, 560), Image.Resampling.LANCZOS).save(path50)
    return path100, path50


def reveal_board(assets):
    board = Image.new("RGBA", (1800, 1120), "#071219")
    draw = ImageDraw.Draw(board)
    draw.text((32, 22), "A7 SIX STRUCTURES | NORMAL / REVEAL 0.34", font=font(34, True), fill="#eff7f8")
    draw.text((32, 66), "foundation remains 1.00; only whole occluder changes alpha", font=font(21), fill="#91c2ca")
    for index, object_id in enumerate(BUILDINGS):
        col, row = index % 3, index // 3
        x0, y0 = 20 + col * 590, 120 + row * 490
        draw.rectangle((x0, y0, x0 + 570, y0 + 470), fill="#0d222b", outline="#315661", width=2)
        normal = fit(assets[object_id]["normal"], 255, 310)
        reveal = fit(assets[object_id]["reveal"], 255, 310)
        board.alpha_composite(normal, (x0 + 18 + (255 - normal.width) // 2, y0 + 90 + (300 - normal.height) // 2))
        board.alpha_composite(reveal, (x0 + 297 + (255 - reveal.width) // 2, y0 + 90 + (300 - reveal.height) // 2))
        draw.text((x0 + 18, y0 + 15), f"{object_id} | {BUILDINGS[object_id]['role_cn']}", font=font(20, True), fill="#eef7f8")
        draw.text((x0 + 80, y0 + 55), "1.00", font=font(17), fill="#b8dce0")
        draw.text((x0 + 370, y0 + 55), "0.34", font=font(17), fill="#8ed0d8")
    path = QA / "A7_SIX_STRUCTURE_NORMAL_REVEAL_GROUP_1800x1120.png"
    board.save(path)
    return path


def hidden_silhouette_board(assets):
    # Deliberately shuffled and anonymized: names, roles, colors, material and
    # foundations cannot rescue a repeated silhouette.
    order = ["SE_BLOCK", "NM_BLOCK", "BROKEN_SKYWALK", "NW_BLOCK", "SW_BLOCK", "NE_BLOCK"]
    board = Image.new("RGBA", (1800, 1120), "#071219")
    draw = ImageDraw.Draw(board)
    draw.text((32, 22), "A7 SIX STRUCTURES | HIDDEN-NAME UNIFORM-GREY SILHOUETTE GATE", font=font(31, True), fill="#eff7f8")
    draw.text((32, 66), "50% first-read audit / no foundation / no material / no role labels", font=font(21), fill="#91c2ca")
    mapping = {}
    for index, object_id in enumerate(order):
        col, row = index % 3, index // 3
        x0, y0 = 20 + col * 590, 120 + row * 490
        draw.rectangle((x0, y0, x0 + 570, y0 + 470), fill="#0d222b", outline="#315661", width=2)
        alpha = assets[object_id]["occluder"].getchannel("A")
        silhouette = Image.new("RGBA", assets[object_id]["occluder"].size, (0, 0, 0, 0))
        silhouette.paste((113, 143, 151, 255), (0, 0, silhouette.width, silhouette.height), alpha)
        shown = fit(silhouette, 500, 350)
        board.alpha_composite(shown, (x0 + (570 - shown.width) // 2, y0 + 72 + (350 - shown.height) // 2))
        slot = f"SLOT_{index + 1}"
        mapping[slot] = object_id
        draw.text((x0 + 20, y0 + 18), f"SILHOUETTE {index + 1}", font=font(23, True), fill="#e4eff1")
    path100 = QA / "A7_REV2_HIDDEN_NAME_UNIFORM_GREY_SILHOUETTE_GATE_1800x1120.png"
    path50 = QA / "A7_REV2_HIDDEN_NAME_UNIFORM_GREY_SILHOUETTE_GATE_50_PERCENT_900x560.png"
    board.save(path100)
    board.resize((900, 560), Image.Resampling.LANCZOS).save(path50)
    mapping_path = RECEIPTS / "A7-REV2-hidden-silhouette-slot-mapping.json"
    mapping_path.write_text(json.dumps({"visible_board_has_names": False, "foundation_included": False, "material_included": False, "mapping": mapping}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path100, path50, mapping_path


def normalized_mask(alpha, size=(192, 160)):
    binary = alpha.point(lambda value: 255 if value >= 32 else 0)
    bbox = binary.getbbox()
    if not bbox:
        return Image.new("1", size, 0)
    crop = binary.crop(bbox)
    factor = min((size[0] - 16) / crop.width, (size[1] - 16) / crop.height)
    resized = crop.resize((max(1, round(crop.width * factor)), max(1, round(crop.height * factor))), Image.Resampling.NEAREST)
    out = Image.new("L", size, 0)
    out.paste(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
    return out


def iou(a, b):
    intersection = ImageChops.multiply(a, b)
    union = ImageChops.lighter(a, b)
    inter_count = sum(1 for value in intersection.getdata() if value)
    union_count = sum(1 for value in union.getdata() if value)
    return inter_count / union_count if union_count else 0.0


def component_count(alpha):
    small = normalized_mask(alpha, (128, 112))
    data = [1 if value else 0 for value in small.getdata()]
    width, height = small.size
    visited = bytearray(width * height)
    components = 0
    for index, value in enumerate(data):
        if not value or visited[index]:
            continue
        queue = deque([index])
        visited[index] = 1
        count = 0
        while queue:
            current = queue.popleft()
            count += 1
            x, y = current % width, current // width
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < width and 0 <= ny < height:
                    ni = ny * width + nx
                    if data[ni] and not visited[ni]:
                        visited[ni] = 1
                        queue.append(ni)
        if count >= 16:
            components += 1
    return components


def repetition_audit(assets):
    masks = {object_id: normalized_mask(asset["occluder"].getchannel("A")) for object_id, asset in assets.items()}
    pairs = []
    adjacency = {object_id: set() for object_id in BUILDINGS}
    threshold = 0.82
    for first, second in itertools.combinations(BUILDINGS, 2):
        similarity = iou(masks[first], masks[second])
        high = similarity >= threshold
        pairs.append({"a": first, "b": second, "normalized_alpha_iou": round(similarity, 5), "high_similarity": high})
        if high:
            adjacency[first].add(second)
            adjacency[second].add(first)
    max_clique = 1
    ids = list(BUILDINGS)
    for size in range(2, len(ids) + 1):
        for group in itertools.combinations(ids, size):
            if all(second in adjacency[first] for first, second in itertools.combinations(group, 2)):
                max_clique = max(max_clique, size)
    signatures = {}
    for object_id, asset in assets.items():
        alpha = asset["occluder"].getchannel("A")
        bbox = alpha.getbbox()
        signatures[object_id] = {
            "role": BUILDINGS[object_id]["role"],
            "silhouette_signature": BUILDINGS[object_id]["signature"],
            "alpha_bbox": list(bbox),
            "bbox_aspect": round((bbox[2] - bbox[0]) / (bbox[3] - bbox[1]), 5),
            "component_count": component_count(alpha),
        }
    result = {
        "threshold": threshold,
        "pairwise": pairs,
        "signatures": signatures,
        "max_high_similarity_clique_size": max_clique,
        "three_or_more_near_duplicate_cluster": max_clique >= 3,
        "machine_pass": max_clique < 3,
        "boundary": "normalized alpha audit supports but does not replace producer 50-percent first-read review",
    }
    path = RECEIPTS / "A7-silhouette-repetition-audit.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result, path


def write_audits(assets):
    camera_path = RECEIPTS / "camera-pivot-angle-audit.tsv"
    with camera_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("object_id", "grid_rect", "local_canvas_px", "pivot_local_px", "front_edge_raw", "visual_bounds_raw", "height_limit_px", "authored_height_px", "axis_slopes", "axis_angles_deg", "foundation_byte_identical", "manual_offset", "alpha_bbox"))
        for object_id, spec in BUILDINGS.items():
            foundation_source = source_foundation_path(object_id)
            foundation_out, _ = output_paths(object_id)
            authored_height = 82 if object_id == "NW_BLOCK" else max(volume[2] for volume in spec["volumes"])
            writer.writerow((
                object_id, ",".join(map(str, spec["grid_rect"])), f"{spec['bounds'][2]},{spec['bounds'][3]}", ",".join(map(str, spec["pivot"])),
                ",".join(map(str, spec["front"])), ",".join(map(str, spec["bounds"])), spec["height"], authored_height,
                "+0.600;-0.600", "+30.9637565;-30.9637565", sha(foundation_source) == sha(foundation_out), "false", ",".join(map(str, assets[object_id]["occluder"].getchannel("A").getbbox())),
            ))
    role_path = RECEIPTS / "role-distinction.tsv"
    with role_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("object_id", "role", "role_cn", "silhouette_signature", "fifty_percent_identity", "clone_source"))
        for object_id, spec in BUILDINGS.items():
            writer.writerow((object_id, spec["role"], spec["role_cn"], spec["signature"], spec["signature"], "A6_exact_inheritance" if object_id == "NW_BLOCK" else "independent_recipe"))
    return camera_path, role_path


def write_lineage():
    path = ROOT / "source-lineage.tsv"
    sources = [
        ("A7_OBJECTIVE", OBJECTIVE, "task_scope", "none"),
        ("CAMERA_V2", CAMERA, "exact_projection_authority", "geometry_only"),
        ("REGISTRATION", REGISTRATION, "grid_pivot_front_edge_envelope_authority", "geometry_only"),
        ("A6_NW_FOUNDATION", A6 / "delivery/NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png", "NW_exact_foundation", "copied_byte_for_byte"),
        ("A6_NW_OCCLUDER", A6 / "delivery/NW_BLOCK_OCCLUDER_CAMERA_V2_MATERIAL_RGBA.png", "NW_producer_passed_asset_method_candidate", "copied_byte_for_byte"),
        ("TASK121_FOUNDATIONS", TASK121 / "delivery/structures", "other_five_foundation_authority", "each_foundation_copied_byte_for_byte"),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source_id", "path", "sha256", "role", "visible_pixel_use"))
        for source_id, source, role, use in sources:
            source_hash = sha(source) if source.is_file() else "DIRECTORY_MULTIPLE_SOURCES_SEE_MACHINE_REPORT"
            writer.writerow((source_id, str(source.relative_to(PROJECT)), source_hash, role, use))
    return path


def build():
    assets = {}
    for object_id, spec in BUILDINGS.items():
        foundation_source = source_foundation_path(object_id)
        foundation_path, occluder_path = output_paths(object_id)
        shutil.copyfile(foundation_source, foundation_path)
        foundation = Image.open(foundation_path).convert("RGBA")
        if spec.get("inherit_a6"):
            shutil.copyfile(A6 / "delivery/NW_BLOCK_OCCLUDER_CAMERA_V2_MATERIAL_RGBA.png", occluder_path)
            occluder = Image.open(occluder_path).convert("RGBA")
        else:
            occluder = build_authored_structure(object_id, spec)
            occluder.save(occluder_path)
        assert foundation.size == (spec["bounds"][2], spec["bounds"][3])
        assert occluder.size == foundation.size
        normal = combined(foundation, occluder, 1.0)
        reveal = combined(foundation, occluder, 0.34)
        restore = combined(foundation, occluder, 1.0)
        state_paths = {}
        for name, image in (("NORMAL_100", normal), ("REVEAL_034", reveal), ("RESTORE_100", restore)):
            path = STATES / f"{object_id}_{name}.png"
            image.save(path)
            state_paths[name] = path
        assert state_paths["NORMAL_100"].read_bytes() == state_paths["RESTORE_100"].read_bytes()
        assets[object_id] = {"foundation": foundation, "occluder": occluder, "combined": normal, "normal": normal, "reveal": reveal, "restore": restore, "state_paths": state_paths}

    group100, group50 = group_board(assets)
    reveal_group = reveal_board(assets)
    repetition, repetition_path = repetition_audit(assets)
    camera_audit, role_audit = write_audits(assets)
    lineage = write_lineage()

    report = {
        "task_id": "A9_1A6_ENV_A7_CAMERA_V2_SIX_STRUCTURE_ASSET_PACK",
        "status": "MACHINE_PASS_PRODUCER_SIX_STRUCTURE_50_PERCENT_REVIEW_PENDING" if repetition["machine_pass"] else "FAIL_REPETITION_STOPPED",
        "camera_axes": [[40, 24], [-40, 24]],
        "axis_angles_deg": [30.9637565, -30.9637565],
        "imagegen_calls": 0,
        "old_donor_pixels_used": False,
        "structure_count": 6,
        "foundation_byte_identical_count": sum(1 for object_id in BUILDINGS if sha(source_foundation_path(object_id)) == sha(output_paths(object_id)[0])),
        "normal_restore_identical_count": sum(1 for asset in assets.values() if asset["state_paths"]["NORMAL_100"].read_bytes() == asset["state_paths"]["RESTORE_100"].read_bytes()),
        "repetition_audit": repetition,
        "three_or_more_first_read_near_duplicate": repetition["three_or_more_near_duplicate_cluster"],
        "machine_pass": bool(repetition["machine_pass"]),
        "producer_visual_review": "PENDING",
        "plan_released": False,
        "runtime_released": False,
    }
    report_path = RECEIPTS / "A7-machine-validation-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ENV_A7_SIX_STRUCTURE_BUILD_COMPLETE")
    print(f"group_50={group50}")
    print(f"repetition_max_clique={repetition['max_high_similarity_clique_size']}")
    print(f"machine_pass={report['machine_pass']}")
    print("producer_visual_review=PENDING")


def build_silhouette_gate():
    assets = {}
    for object_id, spec in BUILDINGS.items():
        if spec.get("inherit_a6"):
            occluder = Image.open(A6 / "delivery/NW_BLOCK_OCCLUDER_CAMERA_V2_MATERIAL_RGBA.png").convert("RGBA")
        else:
            occluder = build_authored_structure(object_id, spec)
        assets[object_id] = {"occluder": occluder}
    board100, board50, mapping_path = hidden_silhouette_board(assets)
    repetition, repetition_path = repetition_audit(assets)
    gate = {
        "task_id": "A9_1A6_ENV_A7_CAMERA_V2_SIX_STRUCTURE_ASSET_PACK",
        "phase": "HIDDEN_NAME_UNIFORM_GREY_50_PERCENT_SILHOUETTE_GATE",
        "status": "AWAITING_PRODUCER_REPETITION_REVIEW" if repetition["machine_pass"] else "FAIL_REPETITION_STOPPED",
        "board_100": str(board100.relative_to(ROOT)),
        "board_50": str(board50.relative_to(ROOT)),
        "mapping_receipt": str(mapping_path.relative_to(ROOT)),
        "repetition_receipt": str(repetition_path.relative_to(ROOT)),
        "max_high_similarity_clique_size": repetition["max_high_similarity_clique_size"],
        "three_or_more_near_duplicate_cluster": repetition["three_or_more_near_duplicate_cluster"],
        "rgb_delivery_built": False,
        "plan_released": False,
    }
    path = RECEIPTS / "A7-REV2-silhouette-gate-readback.json"
    path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ENV_A7_HIDDEN_SILHOUETTE_GATE_BUILT")
    print(f"board_50={board50}")
    print(f"max_high_similarity_clique_size={repetition['max_high_similarity_clique_size']}")
    print("rgb_delivery_built=false")


def seal(verdict):
    report_path = RECEIPTS / "A7-machine-validation-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if verdict == "candidate" and not report.get("machine_pass"):
        raise SystemExit("cannot candidate-seal repetition failure")
    candidate = verdict == "candidate"
    report["status"] = "PASS_CANDIDATE_FOR_PRODUCER_SIX_STRUCTURE_REVIEW" if candidate else "FAIL_REPETITION_OR_VISUAL_QUALITY_STOPPED"
    report["visual_self_review"] = verdict.upper()
    report["task_stopped"] = not candidate
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review = ROOT / "50-100-visual-self-review.md"
    if candidate:
        review.write_text("""# ENV-A7六栋Structure 50% / 100%目视自审\n\n状态：`PASS_CANDIDATE_FOR_PRODUCER_SIX_STRUCTURE_REVIEW / NOT_PLAN`\n\n- 50%：六栋分别读作维修厅、安保办公附楼、长仓储交通厅、分段服务廊、紧凑能源设备站和断连廊；未出现三栋以上同一盒体换色。\n- 100%：六套foundation独立且逐字继承；所有主边来自40x24 exact轴或竖直；用途细节共享语言但不共享排布。\n- 交互：六栋均完成1.00/0.34/1.00且normal与restore逐字一致。\n- 边界：本结论只提交制作人查看六栋资产板，不进入PLAN。\n""", encoding="utf-8")
    else:
        review.write_text("""# ENV-A7六栋Structure 50% / 100%目视自审\n\n状态：`FAIL_REPETITION_OR_VISUAL_QUALITY / STOPPED`\n\n六栋中出现三栋以上第一读近似，或50%用途区分失败；按任务书停止，不进入PLAN。\n""", encoding="utf-8")
    completion = ROOT / "completion-report.md"
    completion.write_text(f"""# ENV-A7六栋独立Structure资产包回执\n\n状态：`{'PASS_CANDIDATE_FOR_PRODUCER_SIX_STRUCTURE_REVIEW' if candidate else 'FAIL_REPETITION_OR_VISUAL_QUALITY_STOPPED'} / ZERO_IMAGEGEN / NOT_PLAN`\n\n- NW逐字继承A6；其余五栋按各自角色、grid、pivot、front edge、envelope和高度上限独立制作。\n- 六栋foundation/occluder及三态、50% group board、重复度与Camera V2机器审计已交。\n- 制作人六栋资产实际帧审查仍为PENDING；不开放PLAN、Runtime、UA91、G2-B或Canon。\n""", encoding="utf-8")

    paths = [path for path in ROOT.rglob("*") if path.is_file() and path.name not in {"asset-manifest.tsv", "delivery-hashes.sha256"}]
    paths.sort(key=lambda item: str(item.relative_to(ROOT)))
    manifest = ROOT / "asset-manifest.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in paths:
            writer.writerow((str(path.relative_to(ROOT)), sha(path), path.stat().st_size))
    hashes = ROOT / "delivery-hashes.sha256"
    hashes.write_text("".join(f"{sha(path)}  {path.relative_to(ROOT)}\n" for path in [*paths, manifest]), encoding="utf-8")
    print(f"ENV_A7_SEALED_{verdict.upper()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--silhouette-gate", action="store_true")
    parser.add_argument("--seal", choices=("candidate", "fail"))
    args = parser.parse_args()
    if sum((bool(args.build), bool(args.silhouette_gate), bool(args.seal))) != 1:
        raise SystemExit("choose exactly one action")
    if args.build:
        build()
    elif args.silhouette_gate:
        build_silhouette_gate()
    else:
        seal(args.seal)


if __name__ == "__main__":
    main()
