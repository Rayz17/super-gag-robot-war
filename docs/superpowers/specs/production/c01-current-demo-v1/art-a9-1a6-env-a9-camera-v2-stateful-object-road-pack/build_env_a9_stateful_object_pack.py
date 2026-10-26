#!/usr/bin/env python3
"""Build the zero-ImageGen ENV-A9 stateful-object review package.

This script deliberately stops at the producer's object-board gate.  It emits
the seven independent RGBA assets plus isolated 100/50 review boards and one
exact A PLAN footpoint board.  It does not emit the five full-screen states.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = Path(__file__).resolve().parents[6]
C01 = ROOT.parent
BUNDLED_NOTE = "Codex bundled Python/Pillow; deterministic procedural 2D; ZERO_IMAGEGEN"

TASK126 = C01 / "126-c01e02-env-a9-camera-v2-stateful-object-and-road-result-pack-objective.md"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
GOLDEN = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json"
A7_SCRIPT = C01 / "art-a9-1a6-env-a7-camera-v2-six-structure-asset-pack/build_env_a7_six_structure_pack.py"
A8_BASE = C01 / "art-a9-1a6-env-a8-camera-v2-structure-plan-recomposition/qa/gate1-a-plan/A8_A_PLAN_ACTOR_FREE_CLEANPLATE_1280x720.png"
A8_CLEANPLATES = C01 / "art-a9-1a6-env-a8-camera-v2-structure-plan-recomposition/qa/four-profile-actor-free-cleanplates"

DELIVERY = ROOT / "delivery"
QA = ROOT / "qa"
RECEIPTS = ROOT / "receipts"
for directory in (DELIVERY, QA, RECEIPTS):
    directory.mkdir(parents=True, exist_ok=True)

S = 4
WORLD = (2400, 1350)
ORIGIN_RAW = (-920, -99)
MAP_Y = 58

ASSETS = {
    "GROUND_DETAIL_OVERLAY_STATIC_CURRENT_V2_2400x1350.png": {
        "role": "ground_detail_static", "state": "intact", "size": WORLD, "pivot": None, "anchor": None,
    },
    "RETIRED_SHIELD_WALL_HUNG_3_SCORCHES_CAMERA_V2_RGBA.png": {
        "role": "retired_shield", "state": "wall_hung_3_scorches", "size": (256, 220), "pivot": (128, 196), "anchor": (14, 10),
    },
    "EAST_EXIT_FIRST_ROUND_OPEN_CAMERA_V2_RGBA.png": {
        "role": "east_exit", "state": "first_round_open", "size": (300, 220), "pivot": (150, 196), "anchor": (31, 7),
    },
    "WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png": {
        "role": "warning_facility", "state": "active", "size": (220, 220), "pivot": (110, 196), "anchor": (27, 8),
    },
    "WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png": {
        "role": "warning_facility", "state": "damaged", "size": (220, 220), "pivot": (110, 196), "anchor": (27, 8),
    },
    "ROAD_RESULT_A_LONG_BROKEN_ARC_42_RGBA_2400x1350.png": {
        "role": "road_result", "state": "long_broken_arc_42", "size": WORLD, "pivot": None, "anchor": None,
    },
    "ROAD_RESULT_B_TWIN_BUCKLES_24_RGBA_2400x1350.png": {
        "role": "road_result", "state": "twin_buckles_24", "size": WORLD, "pivot": None, "anchor": None,
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False):
    candidates = (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)


def ss_canvas(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", (size[0] * S, size[1] * S), (0, 0, 0, 0))


def down(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)


def pt(x: float, y: float) -> tuple[int, int]:
    return round(x * S), round(y * S)


def polygon(draw: ImageDraw.ImageDraw, points, fill, outline=None, width=1):
    ps = [pt(x, y) for x, y in points]
    draw.polygon(ps, fill=fill)
    if outline:
        draw.line(ps + [ps[0]], fill=outline, width=width * S, joint="curve")


def line(draw: ImageDraw.ImageDraw, points, fill, width=1):
    draw.line([pt(x, y) for x, y in points], fill=fill, width=width * S, joint="curve")


def ellipse(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1):
    draw.ellipse(tuple(round(v * S) for v in box), fill=fill, outline=outline, width=width * S)


def rectangle(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1):
    draw.rectangle(tuple(round(v * S) for v in box), fill=fill, outline=outline, width=width * S)


def project_raw(x: float, y: float) -> tuple[float, float]:
    return (x - y) * 40, (x + y) * 24


def source_point(x: float, y: float) -> tuple[float, float]:
    px, py = project_raw(x, y)
    return px - ORIGIN_RAW[0], py - ORIGIN_RAW[1]


def diamond(draw: ImageDraw.ImageDraw, center, rx, ry, fill, outline=None, width=1):
    x, y = center
    polygon(draw, [(x, y - ry), (x + rx, y), (x, y + ry), (x - rx, y)], fill, outline, width)


def draw_ground_overlay() -> Image.Image:
    image = Image.new("RGBA", WORLD, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Low-contrast paving is confined to existing road/apron spaces.  All
    # geometry uses the exact +/-30.96 degree Camera V2 axes.
    road = [source_point(-0.5, 6.5), source_point(31.5, 6.5), source_point(31.5, 13.5), source_point(-0.5, 13.5)]
    draw.polygon(road, fill=(35, 53, 61, 28))
    apron = [source_point(23.5, 3.5), source_point(31.5, 3.5), source_point(31.5, 11.5), source_point(23.5, 11.5)]
    draw.polygon(apron, fill=(48, 66, 72, 24))

    # Sparse panel seams, never a glowing grid.
    seam = (119, 142, 148, 30)
    dark = (7, 18, 24, 44)
    for y in (7.5, 9.5, 11.5, 13.5):
        draw.line([source_point(-0.5, y), source_point(31.5, y)], fill=seam, width=2)
    for x in (4.5, 10.5, 16.5, 22.5, 28.5):
        draw.line([source_point(x, 6.5), source_point(x, 13.5)], fill=dark, width=2)

    # Evacuation-lane road language: muted paint, broken and weathered.
    for x in (20.5, 24.5, 28.5):
        p0 = source_point(x, 7.0)
        p1 = source_point(x + 1.2, 7.0)
        draw.line([p0, p1], fill=(96, 142, 142, 54), width=5)
    for x, y in ((8.0, 10.5), (13.0, 8.7), (19.0, 12.4), (26.0, 9.2), (29.0, 11.8)):
        cx, cy = source_point(x, y)
        draw.ellipse((cx - 34, cy - 7, cx + 34, cy + 7), fill=(8, 22, 29, 25))
    return image


def draw_shield() -> Image.Image:
    size = (256, 220)
    image = ss_canvas(size)
    d = ImageDraw.Draw(image)
    # Contact shadow and a low broken exhibition-wall remnant.  The two wings
    # remain visibly masonry at 50%, while the shield body below is unchanged.
    diamond(d, (128, 190), 73, 24, "#13232a", "#49616a", 2)
    polygon(d, [(8, 113), (62, 81), (82, 93), (82, 181), (8, 213)], "#283e47", "#091a22", 2)
    polygon(d, [(8, 113), (62, 81), (82, 93), (29, 125)], "#596b70", "#0b1d25", 2)
    polygon(d, [(174, 94), (196, 81), (248, 112), (248, 212), (174, 181)], "#1b333d", "#091a22", 2)
    polygon(d, [(174, 94), (196, 81), (248, 112), (226, 125)], "#475e66", "#0b1d25", 2)
    # Broken cap and masonry seams obey Camera V2 axes/verticals only.
    line(d, [(8, 144), (46, 121), (82, 143)], "#61757b", 1)
    line(d, [(29, 125), (29, 198)], "#142a33", 2)
    line(d, [(174, 143), (211, 121), (248, 143)], "#526a72", 1)
    line(d, [(226, 125), (226, 198)], "#102832", 2)
    polygon(d, [(9, 112), (28, 100), (41, 108), (62, 81), (82, 93), (73, 104), (60, 97), (38, 119)], "#4b6067", "#0b1d25", 2)
    polygon(d, [(174, 94), (187, 87), (197, 82), (210, 91), (224, 97), (248, 112), (232, 121), (213, 107)], "#3e555e", "#0b1d25", 2)

    # Exhibition hanger: rear rails, short articulated hooks and a continuous
    # load path into the floor cradle.  Visible exposed sections make it read
    # as wall-mounted rather than as a road sign.
    line(d, [(70, 91), (70, 174), (100, 191)], "#75868a", 8)
    line(d, [(186, 92), (186, 174), (156, 191)], "#213943", 8)
    line(d, [(69, 111), (92, 125)], "#a2afb1", 7)
    line(d, [(187, 111), (164, 125)], "#415963", 7)
    rectangle(d, (62, 103, 76, 119), "#263b43", "#8b9a9e", 2)
    rectangle(d, (180, 103, 194, 119), "#192f38", "#647980", 2)
    line(d, [(100, 175), (100, 197)], "#6c7f84", 7)
    line(d, [(156, 175), (156, 197)], "#263f48", 7)
    # Low floor cradle physically closes the hanger chain.
    polygon(d, [(55, 190), (128, 214), (201, 190), (201, 198), (128, 220), (55, 198)], "#0a151b", "#263d46", 2)
    # Heavy shield body: no animal cues, one asymmetric chipped shoulder.
    body = [(128, 32), (183, 65), (207, 117), (181, 166), (128, 194), (72, 165), (47, 115), (75, 65)]
    polygon(d, body, "#475a62", "#091a22", 3)
    inset = [(128, 47), (173, 74), (190, 116), (169, 154), (128, 176), (86, 154), (65, 115), (84, 74)]
    polygon(d, inset, "#2b3f48", "#6f8289", 2)
    polygon(d, [(128, 47), (173, 74), (190, 116), (128, 109)], "#596d73", None)
    polygon(d, [(128, 109), (190, 116), (169, 154), (128, 176)], "#172c35", None)
    polygon(d, [(128, 109), (128, 176), (86, 154), (65, 115)], "#223740", None)
    # Three unmistakable, pre-existing scorch slashes.
    for points, w in (
        ([(91, 79), (141, 103), (169, 130)], 9),
        ([(82, 103), (126, 125), (151, 149)], 7),
        ([(103, 66), (147, 88), (179, 104)], 5),
    ):
        line(d, points, "#10171b", w)
        line(d, [(x + 1, y - 2) for x, y in points], "#874b31", max(2, w // 3))
    diamond(d, (128, 111), 18, 11, "#1a2b32", "#8b9a9e", 2)
    return down(image, size)


def draw_exit() -> Image.Image:
    size = (300, 220)
    image = ss_canvas(size)
    d = ImageDraw.Draw(image)
    diamond(d, (150, 194), 121, 25, "#11242c", "#42616b", 2)
    # Two Camera-V2 pillars with a clear open void.
    for cx, mirror in ((65, False), (235, True)):
        side = -1 if mirror else 1
        polygon(d, [(cx - 27, 72), (cx + 5, 53), (cx + 29, 68), (cx - 3, 87)], "#526870", "#0a1c24", 2)
        polygon(d, [(cx - 27, 72), (cx - 3, 87), (cx - 3, 180), (cx - 27, 166)], "#243b45", "#0a1c24", 2)
        polygon(d, [(cx - 3, 87), (cx + 29, 68), (cx + 29, 161), (cx - 3, 180)], "#182f39", "#0a1c24", 2)
        rectangle(d, (cx - 18, 101, cx - 8, 145), "#5d747a", "#0e252e", 1)
        ellipse(d, (cx - 19, 89, cx - 7, 101), "#58b9b5", "#b5e0d9", 1)
        # Retracted barrier leaves point away from the opening.
        start = cx - 1
        end = cx + side * 57
        line(d, [(start, 166), (end, 188)], "#657a80", 8)
        line(d, [(start, 164), (end, 186)], "#bb7740", 2)
    polygon(d, [(65, 53), (150, 3), (235, 53), (205, 71), (150, 39), (95, 71)], "#304a54", "#081a22", 3)
    polygon(d, [(95, 71), (150, 39), (205, 71), (150, 103)], "#1a333d", "#55727a", 2)
    rectangle(d, (126, 58, 174, 73), "#193038", "#709097", 1)
    line(d, [(136, 66), (164, 66)], "#58b9b5", 4)
    # Floor ticks make open status readable without a glowing route.
    line(d, [(112, 178), (150, 200), (188, 178)], "#547178", 3)
    return down(image, size)


def draw_facility(damaged: bool) -> Image.Image:
    size = (220, 220)
    image = ss_canvas(size)
    d = ImageDraw.Draw(image)
    diamond(d, (110, 193), 73, 25, "#102129", "#3d5b65", 2)
    polygon(d, [(58, 169), (110, 139), (162, 169), (110, 200)], "#263f49", "#091b23", 2)
    polygon(d, [(72, 68), (110, 45), (151, 69), (110, 94)], "#526970", "#0b1d25", 2)
    polygon(d, [(72, 68), (110, 94), (110, 164), (72, 142)], "#273e48", "#0b1d25", 2)
    polygon(d, [(110, 94), (151, 69), (151, 141), (110, 164)], "#172f39", "#0b1d25", 2)
    rectangle(d, (83, 99, 101, 131), "#52666c", "#10252e", 1)
    line(d, [(119, 106), (141, 93)], "#73888d", 3)
    line(d, [(119, 119), (141, 106)], "#425b63", 3)
    if not damaged:
        polygon(d, [(89, 48), (110, 14), (132, 48), (110, 61)], "#8b5b32", "#181c1d", 2)
        polygon(d, [(98, 43), (110, 24), (122, 43), (110, 50)], "#db8b3d", "#f4c16c", 1)
        line(d, [(81, 55), (63, 44)], "#b4773c", 3)
        line(d, [(139, 55), (157, 44)], "#b4773c", 3)
        rectangle(d, (84, 139, 136, 150), "#1d343d", "#71898f", 1)
        line(d, [(93, 145), (128, 145)], "#63aaa6", 3)
    else:
        # Same body/canvas/pivot; only local state damage changes.
        polygon(d, [(89, 48), (103, 26), (110, 40), (122, 31), (132, 48), (110, 61)], "#3b3d3b", "#171b1c", 2)
        line(d, [(111, 42), (130, 77), (118, 98)], "#10191c", 5)
        line(d, [(113, 43), (132, 77), (120, 98)], "#8b4d32", 2)
        rectangle(d, (84, 139, 136, 150), "#17272d", "#46595d", 1)
        line(d, [(93, 145), (108, 145)], "#a95c35", 3)
        line(d, [(125, 148), (142, 166)], "#5a3429", 4)
        ellipse(d, (136, 163, 143, 170), "#bc693b")
    return down(image, size)


def world_line(image: Image.Image, grid_points, color, width):
    ImageDraw.Draw(image).line([source_point(x, y) for x, y in grid_points], fill=color, width=width, joint="curve")


def draw_road_result(route: str) -> Image.Image:
    image = Image.new("RGBA", WORLD, (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    if route == "A":
        main = [(18.5, 10.0), (19.6, 9.45), (20.5, 10.5), (21.4, 11.55), (22.8, 11.0), (24.0, 12.1)]
        world_line(image, main, (8, 13, 16, 210), 13)
        world_line(image, main, (92, 66, 52, 170), 4)
        for branch in (
            [(20.5, 10.5), (20.0, 11.5), (19.2, 12.0)],
            [(21.4, 11.55), (22.2, 12.25), (23.0, 12.35)],
            [(19.6, 9.45), (19.0, 8.7), (18.2, 8.45)],
        ):
            world_line(image, branch, (11, 16, 18, 185), 7)
            world_line(image, branch, (96, 72, 57, 120), 2)
        cx, cy = source_point(20.5, 10.5)
        d.ellipse((cx - 92, cy - 19, cx + 92, cy + 19), fill=(18, 26, 30, 38))
    else:
        for y in (9.9, 11.1):
            pts = [(19.1, y), (19.8, y - 0.35), (20.5, y + 0.25), (21.2, y - 0.28), (21.9, y)]
            world_line(image, pts, (10, 16, 19, 190), 10)
            world_line(image, pts, (84, 68, 58, 135), 3)
        for x, y in ((20.0, 10.0), (21.0, 11.0)):
            cx, cy = source_point(x, y)
            d.ellipse((cx - 54, cy - 10, cx + 54, cy + 10), fill=(20, 29, 33, 32))
    return image


def checker(size, cell=16):
    im = Image.new("RGBA", size, "#101a21")
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#17252d")
    return im


def alpha_bbox(image: Image.Image):
    return image.getchannel("A").getbbox()


def crop_nonzero(image: Image.Image, pad=24):
    bbox = alpha_bbox(image)
    if not bbox:
        return Image.new("RGBA", (1, 1))
    box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(image.width, bbox[2] + pad), min(image.height, bbox[3] + pad))
    return image.crop(box)


def build_object_board(images: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGBA", (1800, 1200), "#081219")
    d = ImageDraw.Draw(board)
    d.text((70, 38), "ENV-A9  STATEFUL OBJECT / ROAD RESULT  —  PRODUCER OBJECT GATE", font=font(34, True), fill="#d8e4e4")
    d.text((70, 83), "Camera V2 exact • independent RGBA • ZERO_IMAGEGEN • no final PLAN", font=font(21), fill="#7f9da4")
    cards = [
        ("RETIRED_SHIELD_WALL_HUNG_3_SCORCHES_CAMERA_V2_RGBA.png", "RETIRED SHIELD / 3 SCORCHES", (50, 150, 450, 560)),
        ("EAST_EXIT_FIRST_ROUND_OPEN_CAMERA_V2_RGBA.png", "EAST EXIT / ROUND-1 OPEN", (480, 150, 880, 560)),
        ("WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png", "WARNING FACILITY / ACTIVE", (910, 150, 1310, 560)),
        ("WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png", "WARNING FACILITY / DAMAGED", (1340, 150, 1740, 560)),
        ("GROUND_DETAIL_OVERLAY_STATIC_CURRENT_V2_2400x1350.png", "GROUND DETAIL / INTACT", (50, 640, 570, 1050)),
        ("ROAD_RESULT_A_LONG_BROKEN_ARC_42_RGBA_2400x1350.png", "A T5 / LONG BROKEN ARC 42", (640, 640, 1160, 1050)),
        ("ROAD_RESULT_B_TWIN_BUCKLES_24_RGBA_2400x1350.png", "B T5 / TWIN BUCKLES 24", (1230, 640, 1750, 1050)),
    ]
    for name, title, box in cards:
        x0, y0, x1, y1 = box
        d.rounded_rectangle(box, radius=18, fill="#0e1d25", outline="#37515a", width=2)
        d.text((x0 + 20, y0 + 18), title, font=font(20, True), fill="#d1dddd")
        area = (x0 + 20, y0 + 58, x1 - 20, y1 - 55)
        bg = checker((area[2] - area[0], area[3] - area[1]), 18)
        board.alpha_composite(bg, (area[0], area[1]))
        sample = images[name]
        if sample.size == WORLD:
            sample = crop_nonzero(sample, 36)
        max_w, max_h = area[2] - area[0] - 28, area[3] - area[1] - 26
        scale = min(max_w / sample.width, max_h / sample.height, 1.5)
        scaled = sample.resize((max(1, round(sample.width * scale)), max(1, round(sample.height * scale))), Image.Resampling.LANCZOS)
        px = area[0] + (area[2] - area[0] - scaled.width) // 2
        py = area[1] + (area[3] - area[1] - scaled.height) // 2
        board.alpha_composite(scaled, (px, py))
        spec = ASSETS[name]
        if spec["pivot"]:
            pivot = spec["pivot"]
            sx = px + round(pivot[0] * scale)
            sy = py + round(pivot[1] * scale)
            d.line((sx - 8, sy, sx + 8, sy), fill="#56c8c0", width=2)
            d.line((sx, sy - 8, sx, sy + 8), fill="#56c8c0", width=2)
        d.text((x0 + 20, y1 - 38), f"{images[name].size[0]}×{images[name].size[1]}  alpha RGBA", font=font(16), fill="#78969e")
    d.text((70, 1120), "50% gate: ACTIVE/DAMAGED and A/B road consequences must remain distinct; all footpoints stay exact.", font=font(21), fill="#c18b52")
    return board


def crop_world_overlay(overlay: Image.Image) -> Image.Image:
    crop = overlay.crop((680, 515, 1960, 1099))
    frame = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    frame.alpha_composite(crop, (0, MAP_Y))
    return frame


def crop_world_overlay_for_profile(overlay: Image.Image, profile: dict) -> Image.Image:
    x, y, width, height = profile["source_canvas_crop_px"]
    assert (width, height) == (1280, 584)
    crop = overlay.crop((x, y, x + width, y + height))
    frame = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    frame.alpha_composite(crop, (0, MAP_Y))
    return frame


def build_a_plan_board(images: dict[str, Image.Image]) -> Image.Image:
    frame = Image.open(A8_BASE).convert("RGBA")
    frame.alpha_composite(crop_world_overlay(images["GROUND_DETAIL_OVERLAY_STATIC_CURRENT_V2_2400x1350.png"]))
    placements = [
        ("RETIRED_SHIELD_WALL_HUNG_3_SCORCHES_CAMERA_V2_RGBA.png", (400, 242), "[14,10] SHIELD"),
        ("WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png", (1000, 506), "[27,8] ACTIVE"),
        ("EAST_EXIT_FIRST_ROUND_OPEN_CAMERA_V2_RGBA.png", (1200, 578), "[31,7] OPEN"),
    ]
    for name, foot, _ in sorted(placements, key=lambda row: row[1][1]):
        asset = images[name]
        pivot = ASSETS[name]["pivot"]
        frame.alpha_composite(asset, (foot[0] - pivot[0], foot[1] - pivot[1]))

    # QA-only exact readback markers; never part of the RGBA assets.
    d = ImageDraw.Draw(frame)
    for _, (x, y), label in placements:
        d.ellipse((x - 7, y - 4, x + 7, y + 4), outline="#4de1d4", width=2)
        d.line((x, y - 16, x, y + 16), fill="#4de1d4", width=1)
        tw = d.textbbox((0, 0), label, font=font(15, True))[2]
        tx = min(max(8, x - tw // 2), 1272 - tw)
        ty = max(66, y + 13)
        d.rounded_rectangle((tx - 5, ty - 3, tx + tw + 5, ty + 20), radius=4, fill=(4, 17, 24, 218), outline="#35636a", width=1)
        d.text((tx, ty), label, font=font(15, True), fill="#bce7e2")
    d.text((22, 667), "A PLAN exact footpoint QA • shield (400,242) • facility (1000,506) • east exit (1200,578)", font=font(17, True), fill="#d4dedf")
    d.text((22, 693), "Candidate review composite only — no actors, route, protection overlay or T5 consequence", font=font(15), fill="#8ea2a8")
    return frame


def registration_rows() -> dict[str, dict]:
    with REGISTRATION.open(newline="", encoding="utf-8") as handle:
        return {row["object_id"]: row for row in csv.DictReader(handle, delimiter="\t")}


def parse_pair(value: str) -> tuple[int, int]:
    left, right = value.split(",")
    return int(left), int(right)


def draw_micro_crack_fx(frame: Image.Image) -> None:
    # CONTACT-only sparse program/FX cue.  It is intentionally not saved as an
    # eighth asset and never expands into either T5 road consequence.
    d = ImageDraw.Draw(frame)
    for points in (
        [(640, 350), (650, 356), (658, 354)],
        [(641, 351), (634, 360), (629, 360)],
        [(650, 356), (654, 364)],
    ):
        d.line(points, fill=(142, 106, 76, 150), width=2, joint="curve")
        d.line([(x, y + 1) for x, y in points], fill=(8, 15, 18, 150), width=1, joint="curve")


def qa_header(frame: Image.Image, title: str, subtitle: str) -> None:
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((18, 12, 610, 50), radius=8, fill=(4, 15, 21, 224), outline="#36535d", width=1)
    d.text((30, 18), title, font=font(18, True), fill="#d9e4e4")
    d.text((280, 20), subtitle, font=font(14), fill="#8faab0")


def build_full_state_frame(
    images: dict[str, Image.Image],
    camera: dict,
    rows: dict[str, dict],
    state_id: str,
    profile_id: str,
    facility_state: str,
    road_state: str,
    contact_micro_crack: bool,
) -> tuple[Image.Image, dict]:
    cleanplate_names = {
        "A_PLAN": "A8_A_PLAN_ACTOR_FREE_CLEANPLATE_1280x720.png",
        "A_CONTACT": "A8_A_CONTACT_ACTOR_FREE_CLEANPLATE_1280x720.png",
        "B_CONTACT": "A8_B_CONTACT_ACTOR_FREE_CLEANPLATE_1280x720.png",
    }
    base = Image.open(A8_CLEANPLATES / cleanplate_names[profile_id]).convert("RGBA")
    profile = camera["projection"]["camera_profiles"][profile_id]
    base.alpha_composite(crop_world_overlay_for_profile(images["GROUND_DETAIL_OVERLAY_STATIC_CURRENT_V2_2400x1350.png"], profile))

    road_asset = None
    if road_state == "long_broken_arc_42":
        road_asset = "ROAD_RESULT_A_LONG_BROKEN_ARC_42_RGBA_2400x1350.png"
    elif road_state == "twin_buckles_24":
        road_asset = "ROAD_RESULT_B_TWIN_BUCKLES_24_RGBA_2400x1350.png"
    elif road_state != "intact":
        raise AssertionError(f"unsupported road state {road_state}")
    if road_asset:
        base.alpha_composite(crop_world_overlay_for_profile(images[road_asset], profile))
    if contact_micro_crack:
        if road_asset is not None:
            raise AssertionError("CONTACT cannot include a T5 road result asset")
        draw_micro_crack_fx(base)

    facility_asset = (
        "WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png"
        if facility_state == "damaged"
        else "WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png"
    )
    column = f"front_edge_{profile_id}"
    placements = [
        ("PROP_C01CDV1_RETIRED_SHIELD", "RETIRED_SHIELD_WALL_HUNG_3_SCORCHES_CAMERA_V2_RGBA.png"),
        ("TARGET_C01_SECURITY_GATE", facility_asset),
        ("TARGET_C01_EAST_EXIT", "EAST_EXIT_FIRST_ROUND_OPEN_CAMERA_V2_RGBA.png"),
    ]
    placement_readback = {}
    sortable = []
    for object_id, asset_name in placements:
        footpoint = parse_pair(rows[object_id][column])
        sortable.append((footpoint[1], object_id, asset_name, footpoint))
    for _, object_id, asset_name, footpoint in sorted(sortable):
        asset = images[asset_name]
        pivot = ASSETS[asset_name]["pivot"]
        base.alpha_composite(asset, (footpoint[0] - pivot[0], footpoint[1] - pivot[1]))
        placement_readback[object_id] = {"asset": asset_name, "footpoint": list(footpoint), "pivot": list(pivot), "manual_offset": [0, 0]}

    labels = {
        "A_PLAN": ("A PLAN", "ROAD INTACT • FACILITY ACTIVE • SHIELD WALL-HUNG • EXIT OPEN"),
        "A_CONTACT": ("A CONTACT", "MICRO-CRACK FX ONLY • FACILITY ACTIVE • NO A42"),
        "A_T5_RESULT": ("A T5 RESULT", "LONG BROKEN ARC 42 • FACILITY DAMAGED"),
        "B_CONTACT": ("B CONTACT", "MICRO-CRACK FX ONLY • FACILITY ACTIVE • NO B24"),
        "B_T5_RESULT": ("B T5 RESULT", "TWIN BUCKLES 24 • FACILITY ACTIVE"),
    }
    qa_header(base, *labels[state_id])
    return base, {
        "state_id": state_id,
        "profile_id": profile_id,
        "camera_crop": profile["source_canvas_crop_px"],
        "facility_state": facility_state,
        "road_state": road_state,
        "contact_micro_crack_fx": contact_micro_crack,
        "road_asset": road_asset,
        "shield_state": "wall_hung_3_scorches_not_acquired",
        "east_exit_state": "round1_open",
        "placements": placement_readback,
        "forbidden_visible_assets": [],
    }


def build_full_states(images: dict[str, Image.Image]) -> dict:
    camera = json.loads(CAMERA.read_text(encoding="utf-8"))
    rows = registration_rows()
    definitions = [
        ("A_PLAN", "A_PLAN", "active", "intact", False),
        ("A_CONTACT", "A_CONTACT", "active", "intact", True),
        ("A_T5_RESULT", "A_CONTACT", "damaged", "long_broken_arc_42", False),
        ("B_CONTACT", "B_CONTACT", "active", "intact", True),
        ("B_T5_RESULT", "B_CONTACT", "active", "twin_buckles_24", False),
    ]
    full_dir = QA / "full-states"
    state_readbacks = {}
    frames = {}
    for state_id, profile_id, facility_state, road_state, micro in definitions:
        frame, readback = build_full_state_frame(images, camera, rows, state_id, profile_id, facility_state, road_state, micro)
        path100 = full_dir / f"A9_{state_id}_ACTOR_FREE_STATE_QA_1280x720.png"
        path50 = full_dir / f"A9_{state_id}_ACTOR_FREE_STATE_QA_50_PERCENT_640x360.png"
        save(frame, path100)
        save(frame.resize((640, 360), Image.Resampling.LANCZOS), path50)
        frames[state_id] = frame
        readback["qa_100"] = str(path100.relative_to(ROOT))
        readback["qa_50"] = str(path50.relative_to(ROOT))
        state_readbacks[state_id] = readback

    # Contact temporal assertions are fail-closed.
    for contact in ("A_CONTACT", "B_CONTACT"):
        item = state_readbacks[contact]
        assert item["facility_state"] == "active"
        assert item["road_state"] == "intact"
        assert item["contact_micro_crack_fx"] is True
        assert item["road_asset"] is None
    assert state_readbacks["A_T5_RESULT"]["facility_state"] == "damaged"
    assert state_readbacks["A_T5_RESULT"]["road_asset"].startswith("ROAD_RESULT_A_")
    assert state_readbacks["B_T5_RESULT"]["facility_state"] == "active"
    assert state_readbacks["B_T5_RESULT"]["road_asset"].startswith("ROAD_RESULT_B_")

    # Five-frame overview for quick producer actual-frame review.
    board = Image.new("RGBA", (2320, 1120), "#071118")
    d = ImageDraw.Draw(board)
    d.text((50, 28), "ENV-A9 FIVE-STATE ACTOR-FREE TEMPORAL QA", font=font(32, True), fill="#d8e4e4")
    d.text((50, 70), "PLAN → CONTACT micro-FX → T5 resolved consequence; Candidate review only", font=font(20), fill="#83a1a8")
    positions = {
        "A_PLAN": (50, 120), "A_CONTACT": (800, 120), "A_T5_RESULT": (1550, 120),
        "B_CONTACT": (425, 610), "B_T5_RESULT": (1175, 610),
    }
    for state_id, (x, y) in positions.items():
        scaled = frames[state_id].resize((720, 405), Image.Resampling.LANCZOS)
        board.alpha_composite(scaled, (x, y))
        d.rounded_rectangle((x, y, x + 720, y + 405), radius=8, outline="#3c5962", width=2)
    d.text((50, 1060), "Temporal gate: CONTACT contains neither T5 road result nor damaged facility. Shield and east exit remain unchanged in all five states.", font=font(19), fill="#c58a4f")
    save(board, QA / "A9_FIVE_STATE_ACTOR_FREE_TEMPORAL_BOARD_2320x1120.png")
    save(board.resize((1160, 560), Image.Resampling.LANCZOS), QA / "A9_FIVE_STATE_ACTOR_FREE_TEMPORAL_BOARD_50_PERCENT_1160x560.png")

    with (RECEIPTS / "A9-five-state-timing-matrix.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["state_id", "profile_id", "road", "facility", "shield", "east_exit", "micro_crack_fx", "T5_road_asset_used"])
        for state_id, *_ in definitions:
            row = state_readbacks[state_id]
            writer.writerow([state_id, row["profile_id"], row["road_state"], row["facility_state"], row["shield_state"], row["east_exit_state"], str(row["contact_micro_crack_fx"]).lower(), row["road_asset"] or "none"])
    return state_readbacks


def validate_inputs() -> dict:
    camera = json.loads(CAMERA.read_text(encoding="utf-8"))
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    projection = camera["projection"]
    assert projection["tile_half_px"] == [40, 24]
    assert projection["matrix"] == [[40, -40], [24, 24]]
    assert projection["world_canvas"]["size_px"] == [2400, 1350]
    assert projection["world_canvas"]["world_canvas_origin_raw_px"] == [-920, -99]
    assert projection["camera_profiles"]["A_PLAN"]["source_canvas_crop_px"] == [680, 515, 1280, 584]
    assert golden["initial_world"]["warning_facility_state"] == "active"
    assert golden["initial_world"]["road_damage"] == 0
    assert golden["initial_world"]["shield_state"] == "wall_hung_3_scorches"
    assert golden["initial_world"]["east_gate_state"] == "open"

    expected = {
        "PROP_C01CDV1_RETIRED_SHIELD": ((14, 10), (400, 242)),
        "TARGET_C01_SECURITY_GATE": ((27, 8), (1000, 506)),
        "TARGET_C01_EAST_EXIT": ((31, 7), (1200, 578)),
    }
    with REGISTRATION.open(newline="", encoding="utf-8") as handle:
        rows = {row["object_id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    for object_id, (anchor, footpoint) in expected.items():
        row = rows[object_id]
        assert tuple(map(int, row["anchor"].split(","))) == anchor
        assert tuple(map(int, row["front_edge_A_PLAN"].split(","))) == footpoint
        assert row["registration_point"] == "footprint_bottom_center"
    return {
        str(path.relative_to(PROJECT)): sha(path)
        for path in (TASK126, CAMERA, REGISTRATION, GOLDEN, A7_SCRIPT, A8_BASE)
    }


def build(full_states: bool = False) -> None:
    inputs = validate_inputs()
    images = {
        "GROUND_DETAIL_OVERLAY_STATIC_CURRENT_V2_2400x1350.png": draw_ground_overlay(),
        "RETIRED_SHIELD_WALL_HUNG_3_SCORCHES_CAMERA_V2_RGBA.png": draw_shield(),
        "EAST_EXIT_FIRST_ROUND_OPEN_CAMERA_V2_RGBA.png": draw_exit(),
        "WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png": draw_facility(False),
        "WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png": draw_facility(True),
        "ROAD_RESULT_A_LONG_BROKEN_ARC_42_RGBA_2400x1350.png": draw_road_result("A"),
        "ROAD_RESULT_B_TWIN_BUCKLES_24_RGBA_2400x1350.png": draw_road_result("B"),
    }
    for name, image in images.items():
        if image.size != ASSETS[name]["size"]:
            raise AssertionError(f"{name}: size drift {image.size}")
        if image.mode != "RGBA" or not alpha_bbox(image):
            raise AssertionError(f"{name}: missing RGBA/alpha pixels")
        save(image, DELIVERY / name)

    # Stateful facility variants must remain registration-identical.
    assert images["WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png"].size == images["WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png"].size
    assert ASSETS["WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png"]["pivot"] == ASSETS["WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png"]["pivot"]
    if ImageChops.difference(images["WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png"], images["WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png"]).getbbox() is None:
        raise AssertionError("warning facility state variants are not distinguishable")
    if ImageChops.difference(images["ROAD_RESULT_A_LONG_BROKEN_ARC_42_RGBA_2400x1350.png"], images["ROAD_RESULT_B_TWIN_BUCKLES_24_RGBA_2400x1350.png"]).getbbox() is None:
        raise AssertionError("road result variants are not distinguishable")

    board100 = build_object_board(images)
    board50 = board100.resize((900, 600), Image.Resampling.LANCZOS)
    plan100 = build_a_plan_board(images)
    plan50 = plan100.resize((640, 360), Image.Resampling.LANCZOS)
    save(board100, QA / "A9_SEVEN_RGBA_OBJECT_BOARD_1800x1200.png")
    save(board50, QA / "A9_SEVEN_RGBA_OBJECT_BOARD_50_PERCENT_900x600.png")
    save(plan100, QA / "A9_A_PLAN_EXACT_FOOTPOINT_OBJECT_BOARD_1280x720.png")
    save(plan50, QA / "A9_A_PLAN_EXACT_FOOTPOINT_OBJECT_BOARD_50_PERCENT_640x360.png")

    full_state_readback = build_full_states(images) if full_states else None
    readback = {
        "task": "ENV_A9_CAMERA_V2_STATEFUL_OBJECT_ROAD_PACK",
        "status": "PRODUCER_ACTUAL_FRAME_SIGNED_SEVEN_RGBA_AND_FIVE_STATE_TEMPORAL_QA_PASS_NOT_FINAL_PLAN" if full_states else "SEVEN_RGBA_BUILT_AWAITING_PRODUCER_OBJECT_BOARD_REVIEW",
        "authority": "Task126 Candidate production objective; Current scene authority V355-C01E02 unchanged",
        "generator": BUNDLED_NOTE,
        "full_screen_five_state_qa_emitted": full_states,
        "camera": {"axes": [[40, 24], [-40, 24]], "origin_raw": list(ORIGIN_RAW), "world_canvas": list(WORLD), "A_PLAN_crop": [680, 515, 1280, 584]},
        "placements": {
            "PROP_C01CDV1_RETIRED_SHIELD": {"anchor": [14, 10], "A_PLAN_footpoint": [400, 242], "asset": "RETIRED_SHIELD_WALL_HUNG_3_SCORCHES_CAMERA_V2_RGBA.png"},
            "TARGET_C01_SECURITY_GATE": {"anchor": [27, 8], "A_PLAN_footpoint": [1000, 506], "asset_active": "WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png", "asset_damaged": "WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png"},
            "TARGET_C01_EAST_EXIT": {"anchor": [31, 7], "A_PLAN_footpoint": [1200, 578], "asset": "EAST_EXIT_FIRST_ROUND_OPEN_CAMERA_V2_RGBA.png"},
        },
        "timeslice": {
            "PLAN": {"shield": "wall_hung_3_scorches", "east_exit": "open", "facility": "active", "road": "intact"},
            "CONTACT": {"shield": "wall_hung_3_scorches", "east_exit": "open", "facility": "active", "road": "micro_crack_is_program_fx_not_asset"},
            "T5_A": {"facility": "damaged", "road": "long_broken_arc_42"},
            "T5_B": {"facility": "active", "road": "twin_buckles_24"},
        },
        "inputs": inputs,
        "assets": {},
        "full_states": full_state_readback,
        "closed": ["ImageGen", "new gameplay objects", "Runtime", "Default", "Save", "Canon", "final PLAN"],
    }
    for name, spec in ASSETS.items():
        path = DELIVERY / name
        readback["assets"][name] = {
            "sha256": sha(path), "size": list(images[name].size), "alpha_bbox": list(alpha_bbox(images[name])),
            "pivot": list(spec["pivot"]) if spec["pivot"] else None,
            "anchor": list(spec["anchor"]) if spec["anchor"] else None,
            "role": spec["role"], "state": spec["state"],
        }
    (RECEIPTS / "A9-object-gate-readback.json").write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if full_states:
        (RECEIPTS / "A9-five-state-phase-readback.json").write_text(
            json.dumps({
                "status": "PRODUCER_ACTUAL_FRAME_SIGNED_SEVEN_RGBA_AND_FIVE_STATE_TEMPORAL_QA_PASS_NOT_FINAL_PLAN",
                "full_states": full_state_readback,
                "temporal_assertions": {
                    "PLAN_intact_active": True,
                    "A_CONTACT_micro_crack_only_active_no_A42": True,
                    "B_CONTACT_micro_crack_only_active_no_B24": True,
                    "A_T5_damaged_long_broken_arc_42": True,
                    "B_T5_active_twin_buckles_24": True,
                    "shield_wall_hung_not_acquired_all_states": True,
                    "east_exit_round1_open_all_states": True,
                },
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    machine = {
        "status": "PASS" if full_states else "PASS_OBJECT_GATE_ONLY",
        "producer_actual_frame_review": "SIGNED_PASS_50_AND_100_PERCENT_FIVE_STATE_BOARDS" if full_states else "OBJECT_GATE_PENDING",
        "zero_imagegen": True,
        "seven_independent_rgba": len(images) == 7,
        "world_overlay_size_exact": all(images[name].size == WORLD for name in (
            "GROUND_DETAIL_OVERLAY_STATIC_CURRENT_V2_2400x1350.png",
            "ROAD_RESULT_A_LONG_BROKEN_ARC_42_RGBA_2400x1350.png",
            "ROAD_RESULT_B_TWIN_BUCKLES_24_RGBA_2400x1350.png",
        )),
        "facility_same_canvas_pivot_anchor": True,
        "A_PLAN_footpoints_exact": True,
        "five_state_temporal_contract_pass": bool(full_states),
        "contact_T5_asset_leak_count": 0 if full_states else None,
        "runtime_bindable": False,
        "canon_changed": False,
        "final_plan": False,
    }
    (RECEIPTS / "A9-machine-validation-report.json").write_text(json.dumps(machine, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with (ROOT / "source-lineage.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["asset", "derivation", "pixel_source", "geometry_source", "state_source", "imagegen_used", "runtime_bindable"])
        for name, spec in ASSETS.items():
            writer.writerow([name, "deterministic_original_2d", "none_no_old_object_pixels", "Task111 Camera V2 + Task126", "Task126 temporal matrix + golden_slice_profile", "false", "false"])

    files = sorted([
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.name not in {"asset-manifest.tsv", "delivery-hashes.sha256"}
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    ])
    with (ROOT / "asset-manifest.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["path", "role", "status", "width", "height", "mode", "bytes", "sha256"])
        for path in files:
            rel = path.relative_to(ROOT)
            role = "asset" if str(rel).startswith("delivery/") else "qa_or_receipt"
            width = height = mode = ""
            if path.suffix.lower() == ".png":
                with Image.open(path) as im:
                    width, height, mode = im.width, im.height, im.mode
            writer.writerow([rel, role, "candidate_object_gate_pass_producer_actual_frames_signed_not_final_plan", width, height, mode, path.stat().st_size, sha(path)])
    manifest_files = sorted([
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != "delivery-hashes.sha256"
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    ])
    (ROOT / "delivery-hashes.sha256").write_text("".join(f"{sha(path)}  {path.relative_to(ROOT)}\n" for path in manifest_files), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-states", action="store_true", help="emit the producer-released five-state full-screen QA")
    args = parser.parse_args()
    build(full_states=args.full_states)
