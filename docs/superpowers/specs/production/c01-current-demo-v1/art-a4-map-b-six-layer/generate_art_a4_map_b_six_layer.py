#!/usr/bin/env python3
"""Generate the bounded C01E02 A4 MAP-B six-layer Candidate review package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]

PACKAGE_ID = "C01CDV1_A4_MAP_B_SIX_LAYER_V1"
SUBJECT_ID = "MAP_C01CDV1_SCROLLING_STREET"
PROFILE_ID = "c01cdv1_e02_scroll_m2_r2"
TOPOLOGY_SHA256 = "baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8"
MAP_CANDIDATE_ID = "CAND_C01CDV1_A2_DISTRICT_B_RESCUE_RING_V1"
CANVAS = (2400, 1350)
ORIGIN = "0,0"
PIVOT = "0.5,0.5"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

PAPER = "#edf1ee"
PANEL = "#f8faf7"
INK_DEEP = "#07151b"
INK = "#182b32"
INK_SOFT = "#52666b"
IVORY = "#dfe4dc"
TEAL = "#59aaa3"
CORAL = "#e65b50"
CORAL_DARK = "#913a38"
GOLD = "#d6aa3d"
BACKGROUND = "#07151a"
ROAD = "#172b34"
ROAD_LIGHT = "#253a42"
PLAZA = "#52696b"
PLAZA_ALT = "#607477"
RESCUE = "#345f59"
SECURITY = "#5b5f45"
REPAIR = "#60746e"
WALL_COLD = "#b8c4c2"
WALL_LIGHT = "#d7dfdc"
WALL_MID = "#60757a"
WALL_DARK = "#2b424a"
ROOF_COLD = "#83979b"
ROOF_DARK = "#475f65"
SERVICE_WALL = "#42575c"

CORE_LAYER_ROWS = (
    ("BASE", "MAP_C01CDV1_R2_BASE", "MAP_C01CDV1_SCROLLING_STREET_R2_BASE", "A4_MAP_B_BASE_2400x1350.png", 0, "RGB", "opaque terrain, roads and large-scale wayfinding"),
    ("BUILDINGS", "MAP_C01CDV1_R2_BUILDINGS", "MAP_C01CDV1_SCROLLING_STREET_R2_BUILDINGS", "A4_MAP_B_BUILDINGS_2400x1350.png", 10, "RGBA", "building bodies, Wanji south wall and fixed facilities without roofs"),
    ("STATE_LAYERS", "MAP_C01CDV1_R2_STATE_LAYERS", "MAP_C01CDV1_SCROLLING_STREET_R2_STATE_LAYERS", "A4_MAP_B_STATE_LAYERS_2400x1350.png", 20, "RGBA", "default active rescue lane plus wall-hung named shield fixture"),
    ("ROOFS", "MAP_C01CDV1_R2_ROOFS", "MAP_C01CDV1_SCROLLING_STREET_R2_ROOFS", "A4_MAP_B_ROOFS_2400x1350.png", 30, "RGBA", "fade-group roofs, awnings and broken overhead corridor"),
    ("FOREGROUND", "MAP_C01CDV1_R2_FOREGROUND", "MAP_C01CDV1_SCROLLING_STREET_R2_FOREGROUND", "A4_MAP_B_FOREGROUND_2400x1350.png", 40, "RGBA", "sparse front-edge world rails and protection fixtures"),
    ("OCCLUSION_MASK", "MAP_C01CDV1_R2_OCCLUSION_MASK", "MAP_C01CDV1_SCROLLING_STREET_R2_OCCLUSION_MASK", "A4_MAP_B_OCCLUSION_MASK_2400x1350.png", -1, "RGBA", "R fade fill, G roof outline, B safety fringe; control-only"),
)

STATIC_SOURCES = (
    ("docs/superpowers/specs/production/c01-current-demo-v1/19-current-demo-inplace-rebase-producer-contract.md", "6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94", "producer_contract_r2"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/20-c01e02-j2-joint-integration-contract.md", "038bfb0d57aea64c1ca3a91cae7e1623a33d7c8aaeb7e7ae2af4541770ca3f0d", "joint_contract"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/24-c01e02-a4-map-b-six-layer-art-objective.md", "b35a88d775e2851c899c4245824eddf73014ebc331115ad99aa1c001f3a37e4e", "a4_objective"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a2/a2-user-approval-receipt.tsv", "5eae8ce88217e1ab7185ef3fbf42dd234574ab8b016c068c441f8424c41a5e76", "a2_approval"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a3/a3-user-approval-receipt.tsv", "4698ab86e24483bbaf0bd95c5f72e9f2d9cf694f935a6176ee7862ed9465bab4", "a3_approval"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a3/a3-selected-source-hashes.sha256", "ff09490e4e0cad1c3f324c98397cd909d936a4d9447e42ff74c5c04783224355", "a3_selected_sources"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/candidate-spec.tsv", "43f0afcc7d576074927029592936daddd56f0491cc74f941400fe4f7d477491c", "a2_candidate_spec"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/topology-receipt.tsv", "e2af0c5542b3a3cb78c8b631aba934c59e980f553e319e346fb62637f72e80c7", "a2_topology"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/camera-continuity.tsv", "a3b717531c70da32239ce253eb0faeada44442a3c30bd676f728a6036ce90bf7", "a2_cameras"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/occlusion-rule.tsv", "ac507102f1eb53de59edc0977f2c54fbe39852554d0c50a1031404dc8a791435", "a2_occlusion"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_full_domain_review_2400x1350.png", "03c48e13c278cf058f223cd18590a7f9ed59e32d48676d05e33bac10ac8250b0", "a2_map_b_full"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_pure_read_full_domain_2400x1350.png", "2b0ff5ca23674b6f0393c91ef3d2468391a05e7053806db6d705cef1d0bbc381", "a2_map_b_pure"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_three_viewport_continuity_3840x820.png", "c4618e0faeefd6aed3ef56a1053c8556d0450e756111b69f3c5353aa7355fad9", "a2_map_b_continuity"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_viewport_west_1280x720.png", "5dc4d77416b2e132aebc51bb078516c055119612c35d2524c47c5a879d79f519", "a2_map_b_west"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_viewport_central_1280x720.png", "841288bf225cd4dc63d11ed20ffea5a859c9333e732eb6d5dbefa8f8c8914dc2", "a2_map_b_central"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_viewport_east_1280x720.png", "d396fe83b01fe06a7f89117fb6d66cf4e8fe46a2e69bd441d62ff83358e64a88", "a2_map_b_east"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/main-m2-2/01-13-slot-test-matrix.tsv", "654c6ab16c4f5c61fd148cde03cee3be9842b2f281db66c28c2fd434cada4350", "m2_2_slot_matrix"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/main-m2-2/05-completion-report.md", "cb2fad6347f87b1e772fd2f793478a70ed94874b29939e31262246c4acf5123b", "m2_2_completion"),
    ("game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/asset_slot_manifest_r2.json", "2cc85fc524b453b255c4d8aa521236e0845664f1a8721829da7a5befa21b93c9", "r2_slot_manifest"),
    ("game-godot/content/candidate_runtime_demo/c01/e02/graybox_profiles.json", "07f611fabb1a41c713da5019ce433820f95229cbf83b633fe67fa43d836278da", "r2_tactical_profile"),
)

A3_OVERLAY = "docs/superpowers/specs/production/c01-current-demo-v1/art-a3-rift-swarm-qsd/samples/A3_A_east_96_review.png"
A3_OVERLAY_SHA256 = "66ab008651b84f799d3c9cf7e1df7c8d9c9a0e21a5b248fca83d3f5fa37dc03a"

REVIEW_CAMERAS = (
    ("WEST", "A2_CAM_WEST_GUARDIAN_SHIELD", (-160, 320), "西侧起步 / 馆守Z与取盾"),
    ("CENTRAL", "A2_CAM_CENTRAL_BOSS_PRESSURE", (240, 480), "中央空场 / 巨体回旋"),
    ("EAST", "A2_CAM_EAST_RESCUE_LANE", (830, 620), "东侧环廊 / 撤离出口"),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def canonical_json_sha(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_sources() -> tuple[dict, list[dict[str, str]]]:
    for relative, expected, _ in STATIC_SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"A4 frozen source missing: {relative}")
        actual = sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"A4 frozen source drift: {relative}: {actual}")
    if sha256_file(ROOT / A3_OVERLAY) != A3_OVERLAY_SHA256:
        raise RuntimeError("A4 selected A3 overlay drift")

    a2 = load_tsv(ROOT / STATIC_SOURCES[3][0])
    if len(a2) != 1 or a2[0].get("selected_candidate_id") != MAP_CANDIDATE_ID:
        raise RuntimeError("A4 MAP-B approval mismatch")
    if a2[0].get("occlusion_selection") != "fade_plus_outline" or a2[0].get("runtime_allowed") != "false":
        raise RuntimeError("A4 A2 occlusion/runtime boundary mismatch")

    a3 = load_tsv(ROOT / STATIC_SOURCES[4][0])
    if len(a3) != 1 or a3[0].get("selected_candidate_code") != "A":
        raise RuntimeError("A4 A3 selected direction mismatch")
    for field, expected in (
        ("movement_grammar", "diagonal_alternating_crawl"),
        ("breaker_ecology_relation", "passed_for_BREAKER_B_plus_X"),
        ("instance_rule", "one_master_plus_six_light_variants"),
        ("occlusion", "fade_plus_outline"),
        ("runtime_allowed", "false"),
        ("runtime_handoff", "none"),
    ):
        if a3[0].get(field) != expected:
            raise RuntimeError(f"A4 A3 receipt mismatch: {field}")

    with (ROOT / STATIC_SOURCES[-1][0]).open(encoding="utf-8") as handle:
        profiles = json.load(handle)
    tactical = profiles.get("tactical_profile")
    if not tactical or tactical.get("profile_id") != PROFILE_ID or tactical.get("grid") != [32, 18]:
        raise RuntimeError("A4 tactical profile mismatch")
    topology_payload = {
        "profile_id": tactical["profile_id"],
        "grid": tactical["grid"],
        "projection": tactical["projection"],
        "swarm_organization_state": tactical["swarm_organization_state"],
        "minimum_phase_survivors": tactical["minimum_phase_survivors"],
        "shield_hotspot": tactical["shield_hotspot"],
        "guard_zone": tactical["guard_zone"],
        "units": tactical["units"],
        "terrain_zones": tactical["terrain_zones"],
        "destructibles": tactical["destructibles"],
        "phase_checkpoint": tactical["phase_checkpoint"],
    }
    if canonical_json_sha(topology_payload) != TOPOLOGY_SHA256:
        raise RuntimeError("A4 topology hash mismatch")

    with (ROOT / STATIC_SOURCES[-2][0]).open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    slots = {row["slot_id"]: row for row in manifest["slots"]}
    for _, slot_id, stable_id, _, _, _, _ in CORE_LAYER_ROWS:
        slot = slots.get(slot_id)
        if not slot or slot.get("expected_stable_id") != stable_id or slot.get("runtime_allowed") is not False:
            raise RuntimeError(f"A4 R2 slot mismatch: {slot_id}")
        if slot.get("approved_asset_binding") is not None:
            raise RuntimeError(f"A4 cannot overwrite approved binding: {slot_id}")

    topology = load_tsv(ROOT / STATIC_SOURCES[7][0])
    if not topology or any(row.get("topology_signature") != TOPOLOGY_SHA256 for row in topology):
        raise RuntimeError("A4 A2 topology receipt mismatch")

    scenes = load_tsv(ROOT / "docs/superpowers/specs/data/canon/scenes.tsv")
    scene = next((row for row in scenes if row.get("scene_id") == "V355-C01E02"), None)
    if not scene or "旧会展广场与相连街区" not in scene.get("location", ""):
        raise RuntimeError("A4 Current Canon scene location mismatch")
    if "rescue_lane" not in scene.get("notes", "") and "撤离线" not in scene.get("notes", ""):
        raise RuntimeError("A4 Current Canon rescue-lane boundary missing")
    return tactical, topology


def rgba(color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = color.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4)) + (alpha,)


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def world_point(x: float, y: float) -> tuple[float, float]:
    return ((x - y) * 40.0, (x + y) * 20.0)


def project(x: float, y: float) -> tuple[int, int]:
    wx, wy = world_point(x, y)
    return (round(880 + wx), round(170 + wy))


def cell_polygon(x: int, y: int) -> list[tuple[int, int]]:
    cx, cy = project(x, y)
    return [(cx, cy - 20), (cx + 40, cy), (cx, cy + 20), (cx - 40, cy)]


def rect_polygon(rect: list[int]) -> list[tuple[int, int]]:
    x, y, width, height = rect
    p0 = project(x, y)
    p1 = project(x + width - 1, y)
    p2 = project(x + width - 1, y + height - 1)
    p3 = project(x, y + height - 1)
    return [(p0[0], p0[1] - 20), (p1[0] + 40, p1[1]), (p2[0], p2[1] + 20), (p3[0] - 40, p3[1])]


def rect_contains(rect: list[int], x: int, y: int) -> bool:
    return rect[0] <= x < rect[0] + rect[2] and rect[1] <= y < rect[1] + rect[3]


def terrain_kind(tactical: dict, x: int, y: int) -> str:
    result = "plaza"
    for zone in tactical["terrain_zones"]:
        if rect_contains(zone["rect"], x, y):
            result = zone["kind"]
    return result


def ground_color(kind: str, x: int, y: int) -> str:
    if kind == "road":
        return ROAD if (x + y) % 3 else ROAD_LIGHT
    if kind == "rescue_lane":
        return RESCUE if (x + y) % 2 else "#3b6962"
    if kind == "security_apron":
        return SECURITY if (x + y) % 2 else "#64664b"
    if kind == "building":
        return "#405457" if (x + y) % 2 else "#495d5e"
    if kind == "broken_corridor":
        return "#344a50"
    return PLAZA if (x + y) % 3 else PLAZA_ALT


def draw_base(tactical: dict) -> Image.Image:
    image = Image.new("RGB", CANVAS, BACKGROUND)
    draw = ImageDraw.Draw(image, "RGBA")
    for y in range(18):
        for x in range(32):
            kind = terrain_kind(tactical, x, y)
            poly = cell_polygon(x, y)
            draw.polygon(poly, fill=ground_color(kind, x, y))
            draw.line(poly + [poly[0]], fill=rgba("#91a09d", 42), width=1)

    # Main-road lane rhythm is a world material, not tactical UI.
    for y_line in (8.45, 10.55):
        draw.line([project(x, y_line) for x in range(32)], fill=rgba(IVORY, 120), width=3, joint="curve")
    for x in range(2, 30, 4):
        draw.line((project(x, 9.5), project(x + 1.4, 9.5)), fill=rgba("#a7b8b4", 76), width=5)

    # East rescue lane: fixed red structure and directional paving; state lights live elsewhere.
    draw.line([project(x, 3.05) for x in range(15, 32)], fill=rgba(CORAL, 215), width=8, joint="curve")
    draw.line([project(x, 5.85) for x in range(15, 32)], fill=rgba(CORAL_DARK, 175), width=5, joint="curve")
    for x in range(17, 31, 2):
        draw.line((project(x, 4.05), project(x + 0.9, 4.05)), fill=rgba(IVORY, 155), width=5)

    # Large repair panels keep the old expo material history legible without micro-noise.
    for rect in ([3, 11, 5, 2], [10, 7, 4, 2], [18, 12, 5, 2], [25, 6, 4, 2]):
        poly = rect_polygon(rect)
        draw.polygon(poly, fill=rgba(REPAIR, 92))
        draw.line(poly + [poly[0]], fill=rgba("#9aa9a1", 95), width=2)

    # Existing old surface wear. New E02 damage belongs only to state overlays.
    for start, end in (((6.5, 12.2), (8.5, 11.7)), ((17.2, 8.2), (18.4, 9.0)), ((28.0, 12.0), (29.2, 11.4))):
        draw.line((project(*start), project(*end)), fill=rgba("#27383c", 128), width=4)
    return image


def building_zones(tactical: dict) -> list[dict]:
    return sorted(
        (zone for zone in tactical["terrain_zones"] if zone["kind"] == "building"),
        key=lambda zone: zone["rect"][0] + zone["rect"][1],
    )


BUILDING_HEIGHTS = (152, 132, 122, 96, 108, 94)


def volume_geometry(rect: list[int], height: int) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]]]:
    foot = rect_polygon(rect)
    roof = [(x, y - height) for x, y in foot]
    face_a = [roof[1], roof[2], foot[2], foot[1]]
    face_b = [roof[2], roof[3], foot[3], foot[2]]
    return foot, roof, face_a, face_b


def lerp_point(a: tuple[int, int], b: tuple[int, int], amount: float) -> tuple[int, int]:
    return (round(a[0] + (b[0] - a[0]) * amount), round(a[1] + (b[1] - a[1]) * amount))


def draw_face_ribs(draw: ImageDraw.ImageDraw, top_a: tuple[int, int], top_b: tuple[int, int], bottom_a: tuple[int, int], bottom_b: tuple[int, int], count: int, color: str) -> None:
    for index in range(1, count + 1):
        amount = index / (count + 1)
        start = lerp_point(top_a, top_b, amount)
        end = lerp_point(bottom_a, bottom_b, amount)
        draw.line((start, end), fill=rgba(color, 115), width=3)


def draw_buildings(tactical: dict) -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    zones = building_zones(tactical)
    for index, zone in enumerate(zones):
        _, roof, face_a, face_b = volume_geometry(zone["rect"], BUILDING_HEIGHTS[index])
        north_group = zone["rect"][1] == 0
        face_a_color = WALL_COLD if north_group else SERVICE_WALL
        face_b_color = WALL_MID if north_group else WALL_DARK
        draw.polygon(face_a, fill=rgba(face_a_color, 255), outline=rgba(INK_DEEP, 235))
        draw.polygon(face_b, fill=rgba(face_b_color, 255), outline=rgba(INK_DEEP, 235))
        draw_face_ribs(draw, roof[1], roof[2], face_a[3], face_a[2], 4 if north_group else 3, WALL_LIGHT)
        draw_face_ribs(draw, roof[2], roof[3], face_b[3], face_b[2], 3, "#91a4a3")

        # Wanji south wall uses three large machine-display apertures, never tiny windows.
        if north_group:
            center = lerp_point(roof[1], roof[2], 0.52)
            lower = lerp_point(face_a[3], face_a[2], 0.52)
            cy = round((center[1] + lower[1]) / 2)
            radius = 22 if index == 0 else 18
            draw.ellipse((center[0] - radius, cy - radius, center[0] + radius, cy + radius), outline=rgba(CORAL, 220), width=6)
            draw.ellipse((center[0] - radius + 8, cy - radius + 8, center[0] + radius - 8, cy + radius - 8), outline=rgba(IVORY, 150), width=3)
        else:
            draw.line((roof[1], roof[2]), fill=rgba(REPAIR, 220), width=8)

    # Broken overhead corridor side bodies and supports remain in BUILDINGS.
    for segment, height in (([8, 5, 4, 2], 72), ([13, 5, 3, 2], 76)):
        foot, roof, face_a, face_b = volume_geometry(segment, height)
        draw.polygon(face_a, fill=rgba("#6f504e", 255), outline=rgba(INK_DEEP, 230))
        draw.polygon(face_b, fill=rgba("#3c4144", 255), outline=rgba(INK_DEEP, 230))
        for point in (foot[1], foot[2]):
            draw.line((point[0], point[1], point[0], point[1] + 48), fill=rgba("#26383e", 255), width=10)

    # East disaster-control gate is fixed world geometry; lights are state overlays.
    for x, side in ((30.65, -1), (31.35, 1)):
        cx, cy = project(x, 4.4)
        draw.polygon([(cx - 18, cy - 76), (cx + 18, cy - 76), (cx + 14, cy), (cx - 14, cy)], fill=rgba(WALL_COLD, 255), outline=rgba(INK_DEEP, 230))
        draw.rectangle((cx - 11, cy - 58, cx + 11, cy - 28), fill=rgba("#25383e", 255))
        draw.line((cx, cy - 76, cx + side * 28, cy - 94), fill=rgba(CORAL, 220), width=6)
    return image


def draw_roofs(tactical: dict) -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    zones = building_zones(tactical)
    for index, zone in enumerate(zones):
        _, roof, _, _ = volume_geometry(zone["rect"], BUILDING_HEIGHTS[index])
        north_group = zone["rect"][1] == 0
        color = ROOF_COLD if north_group else ROOF_DARK
        if not north_group and index % 2:
            color = "#577069"
        draw.polygon(roof, fill=rgba(color, 255), outline=rgba(IVORY, 225))
        draw.line((roof[0], roof[1]), fill=rgba(CORAL, 245), width=9)
        draw.line((roof[3], roof[0]), fill=rgba("#a8b7b3", 140), width=3)
        center = (sum(point[0] for point in roof) // 4, sum(point[1] for point in roof) // 4)
        if north_group:
            radius = 30 if index == 0 else 24
            draw.ellipse((center[0] - radius, center[1] - radius // 2, center[0] + radius, center[1] + radius // 2), outline=rgba(IVORY, 150), width=5)
            draw.line((center[0] - radius, center[1], center[0] + radius, center[1]), fill=rgba(IVORY, 110), width=3)
            draw.line((center[0], center[1] - radius // 2, center[0], center[1] + radius // 2), fill=rgba(IVORY, 110), width=3)
        else:
            repair = [(center[0] - 42, center[1] - 12), (center[0] + 9, center[1] - 24), (center[0] + 50, center[1] + 6), (center[0] - 15, center[1] + 22)]
            draw.polygon(repair, fill=rgba(REPAIR, 175), outline=rgba("#9baaa4", 110))

    # Broken corridor roof groups retain the A2 split and the open collapsed center.
    corridor_roofs = []
    for segment, height in (([8, 5, 4, 2], 72), ([13, 5, 3, 2], 76)):
        _, roof, _, _ = volume_geometry(segment, height)
        corridor_roofs.append(roof)
        draw.polygon(roof, fill=rgba("#765c59", 255), outline=rgba(IVORY, 230))
        draw.line((roof[0], roof[1]), fill=rgba(CORAL, 245), width=8)
    left, right = corridor_roofs
    draw.line((left[1], right[0]), fill=rgba(CORAL, 240), width=10)
    draw.line((left[2], right[3]), fill=rgba(IVORY, 170), width=5)
    return image


def draw_foreground() -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    # Sparse protection rails occupy the front edge of existing non-passable blocks only.
    segments = (((1.2, 17.4), (6.2, 17.4)), ((11.2, 17.4), (15.6, 17.4)), ((26.0, 17.4), (30.7, 17.4)))
    for start, end in segments:
        p0, p1 = project(*start), project(*end)
        draw.line((p0, p1), fill=rgba("#839794", 245), width=7)
        for amount in (0.12, 0.5, 0.88):
            x = round(p0[0] + (p1[0] - p0[0]) * amount)
            y = round(p0[1] + (p1[1] - p0[1]) * amount)
            draw.line((x, y - 24, x, y + 8), fill=rgba("#34494f", 255), width=8)
            draw.ellipse((x - 6, y - 32, x + 6, y - 20), fill=rgba(CORAL, 220))
    # Two front-edge repair barricades, deliberately below tactical markers.
    for x, y in ((18.4, 15.6), (24.7, 16.2)):
        cx, cy = project(x, y)
        draw.polygon([(cx - 34, cy - 12), (cx + 34, cy - 12), (cx + 24, cy + 4), (cx - 24, cy + 4)], fill=rgba("#34484e", 245), outline=rgba(IVORY, 170))
        draw.line((cx - 24, cy - 5, cx + 24, cy - 5), fill=rgba(CORAL, 230), width=5)
    return image


def occlusion_mask(buildings: Image.Image, roofs: Image.Image) -> Image.Image:
    body_alpha = buildings.getchannel("A")
    roof_alpha = roofs.getchannel("A")
    fill = ImageChops.lighter(body_alpha, roof_alpha)
    roof_expanded = roof_alpha.filter(ImageFilter.MaxFilter(9))
    roof_outline = ImageChops.subtract(roof_expanded, roof_alpha)
    safety_expanded = fill.filter(ImageFilter.MaxFilter(17))
    safety_fringe = ImageChops.subtract(safety_expanded, fill)
    alpha = ImageChops.lighter(fill, ImageChops.lighter(roof_outline, safety_fringe))
    return Image.merge("RGBA", (fill, roof_outline, safety_fringe, alpha))


def draw_rescue_state(state: str) -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    if state == "active":
        color = CORAL
        glow = "#f09862"
        for x in range(16, 32):
            cx, cy = project(x, 4.65)
            draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=rgba(glow, 225))
            draw.ellipse((cx - 18, cy - 11, cx + 18, cy + 11), fill=rgba(color, 54))
        for x in (30.65, 31.35):
            cx, cy = project(x, 4.4)
            draw.rectangle((cx - 9, cy - 57, cx + 9, cy - 37), fill=rgba("#ff765e", 245))
    elif state == "cleared":
        color = TEAL
        for x in range(16, 32, 2):
            p0 = project(x, 4.65)
            p1 = project(x + 0.8, 4.65)
            draw.line((p0, p1), fill=rgba(color, 210), width=6)
        for x in (30.65, 31.35):
            cx, cy = project(x, 4.4)
            draw.rectangle((cx - 9, cy - 57, cx + 9, cy - 37), fill=rgba("#78d3c5", 235))
        gate_a, gate_b = project(30.75, 3.85), project(31.25, 4.95)
        draw.line((gate_a, gate_b), fill=rgba(IVORY, 165), width=4)
    else:
        raise ValueError(f"unknown rescue state: {state}")
    return image


def draw_shield_state(state: str) -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    cx, cy = project(11, 10)
    # Named geometry rack fixture only; this is not the B2 shield master.
    draw.line((cx - 34, cy - 62, cx - 28, cy + 7), fill=rgba("#493d33", 255), width=9)
    draw.line((cx + 34, cy - 62, cx + 28, cy + 7), fill=rgba("#493d33", 255), width=9)
    draw.line((cx - 35, cy - 62, cx + 35, cy - 62), fill=rgba(GOLD, 230), width=7)
    if state == "wall_hung":
        shield = [(cx, cy - 58), (cx + 24, cy - 42), (cx + 20, cy + 5), (cx, cy + 22), (cx - 20, cy + 5), (cx - 24, cy - 42)]
        draw.polygon(shield, fill=rgba("#35484e", 255), outline=rgba(GOLD, 230))
        draw.line((cx, cy - 45, cx, cy + 9), fill=rgba("#778b89", 170), width=4)
    elif state == "rack_empty":
        draw.ellipse((cx - 8, cy - 35, cx + 8, cy - 19), outline=rgba(IVORY, 175), width=3)
        draw.line((cx - 18, cy - 9, cx + 18, cy - 9), fill=rgba(CORAL_DARK, 165), width=4)
    else:
        raise ValueError(f"unknown shield state: {state}")
    return image


def draw_damage_state(state: str) -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    if state == "before":
        return image
    if state != "after":
        raise ValueError(f"unknown damage state: {state}")
    draw = ImageDraw.Draw(image, "RGBA")
    # E02-only road and facade damage. It changes no passability and implies no later-phase result.
    cx, cy = project(23.2, 10.1)
    draw.ellipse((cx - 88, cy - 31, cx + 92, cy + 35), fill=rgba("#0d171b", 125))
    draw.arc((cx - 76, cy - 40, cx + 84, cy + 38), 196, 344, fill=rgba(CORAL_DARK, 205), width=6)
    for dx, dy in ((-74, 4), (-29, -9), (25, 1), (73, -5)):
        draw.line((cx + dx, cy + dy, cx + dx * 1.22, cy + dy + 30), fill=rgba("#101d22", 210), width=5)
    wall = project(23.8, 1.6)
    draw.ellipse((wall[0] - 42, wall[1] - 154, wall[0] + 58, wall[1] - 74), fill=rgba("#1a2428", 110))
    draw.line((wall[0] - 30, wall[1] - 104, wall[0] + 44, wall[1] - 128), fill=rgba(CORAL_DARK, 155), width=8)
    return image


def combine_state_layers(rescue: str, shield: str, damage: str) -> Image.Image:
    result = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    result.alpha_composite(draw_rescue_state(rescue))
    result.alpha_composite(draw_shield_state(shield))
    result.alpha_composite(draw_damage_state(damage))
    return result


def compose_map(base: Image.Image, buildings: Image.Image, state: Image.Image, roofs: Image.Image, foreground: Image.Image) -> Image.Image:
    result = base.convert("RGBA")
    for layer in (buildings, state, roofs, foreground):
        result.alpha_composite(layer)
    return result.convert("RGB")


def image_outline(source: Image.Image, color: str = IVORY, width: int = 7) -> Image.Image:
    rgba_source = source.convert("RGBA")
    alpha = rgba_source.getchannel("A")
    expanded = alpha.filter(ImageFilter.MaxFilter(width if width % 2 else width + 1))
    ring = ImageChops.subtract(expanded, alpha)
    outline = Image.new("RGBA", source.size, rgba(color, 0))
    outline.putalpha(ring)
    return outline


def faded_layer(source: Image.Image, alpha_ratio: float = 0.18) -> Image.Image:
    result = source.convert("RGBA")
    original = result.getchannel("A")
    result.putalpha(original.point(lambda value: round(value * alpha_ratio)))
    return result


def paste_bottom_center(canvas: Image.Image, sprite: Image.Image, position: tuple[int, int]) -> tuple[int, int]:
    x = position[0] - sprite.width // 2
    y = position[1] - sprite.height
    canvas.alpha_composite(sprite, (x, y))
    return (x, y)


def guardian_fixture(size: int = 190) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    cx, floor = size // 2, size - 8
    draw.polygon([(cx - 30, floor - 120), (cx + 30, floor - 120), (cx + 43, floor - 63), (cx + 24, floor - 36), (cx - 24, floor - 36), (cx - 43, floor - 63)], fill=rgba("#355d70", 255), outline=rgba(INK_DEEP, 255))
    draw.polygon([(cx - 53, floor - 104), (cx - 30, floor - 96), (cx - 38, floor - 53), (cx - 62, floor - 59)], fill=rgba(CORAL, 255))
    draw.polygon([(cx + 53, floor - 104), (cx + 30, floor - 96), (cx + 38, floor - 53), (cx + 62, floor - 59)], fill=rgba(CORAL, 255))
    draw.rectangle((cx - 31, floor - 36, cx - 7, floor), fill=rgba("#314e5d", 255))
    draw.rectangle((cx + 7, floor - 36, cx + 31, floor), fill=rgba("#314e5d", 255))
    draw.line((cx - 55, floor - 105, cx, floor - 125, cx + 55, floor - 105), fill=rgba(IVORY, 235), width=5)
    return image


def breaker_fixture(size: int = 220) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    cx, floor = size // 2, size - 10
    body = [(cx - 84, floor - 85), (cx - 38, floor - 129), (cx + 50, floor - 110), (cx + 91, floor - 61), (cx + 67, floor - 24), (cx - 69, floor - 24), (cx - 94, floor - 59)]
    draw.polygon(body, fill=rgba("#141f24", 255), outline=rgba(CORAL, 240))
    for dx in (-58, -18, 30, 63):
        draw.ellipse((cx + dx - 18, floor - 45, cx + dx + 18, floor - 4), fill=rgba("#263238", 255), outline=rgba(INK_DEEP, 245))
    draw.line((cx - 35, floor - 85, cx + 27, floor - 82), fill=rgba(CORAL, 255), width=7)
    return image


def make_occlusion_demo(base: Image.Image, buildings: Image.Image, state: Image.Image, roofs: Image.Image, foreground: Image.Image) -> Image.Image:
    scene = base.convert("RGBA")
    scene.alpha_composite(buildings)
    scene.alpha_composite(state)

    overlay_records: list[tuple[Image.Image, tuple[int, int], str]] = []
    swarm = Image.open(ROOT / A3_OVERLAY).convert("RGBA")
    overlay_records.append((swarm, project(13, 6), "A3-A / 1x1"))
    overlay_records.append((guardian_fixture(), project(5.5, 10.5), "馆守Z夹具 / 2x2"))
    overlay_records.append((breaker_fixture(), project(24, 9), "BREAKER夹具 / 3x3"))
    placements: list[tuple[Image.Image, tuple[int, int], tuple[int, int], str]] = []
    for sprite, position, title in overlay_records:
        top_left = paste_bottom_center(scene, sprite, position)
        placements.append((sprite, position, top_left, title))

    scene.alpha_composite(faded_layer(roofs, 0.18))
    scene.alpha_composite(image_outline(roofs, IVORY, 9))
    for sprite, _, top_left, _ in placements:
        scene.alpha_composite(image_outline(sprite, IVORY, 7), top_left)
    scene.alpha_composite(foreground)

    board = Image.new("RGB", (2400, 1350), PAPER)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2400, 128), fill=INK_DEEP)
    draw.text((58, 31), "A4｜淡出＋轮廓与多 footprint 验证", font=font(44, bold=True), fill=IVORY)
    draw.text((1720, 50), "建筑 18%｜路径/意图层仍由程序拥有", font=font(21), fill="#b9c8c5")
    panel_width = 740
    for index, (sprite, position, _, title) in enumerate(placements):
        left = 55 + index * 780
        draw.rounded_rectangle((left, 175, left + panel_width, 1240), radius=8, fill=PANEL, outline=(170, 184, 181), width=2)
        draw.text((left + 28, 198), title, font=font(28, bold=True), fill=(24, 43, 50))
        crop = scene.crop((position[0] - 300, position[1] - 330, position[0] + 300, position[1] + 170)).convert("RGB")
        preview = crop.resize((680, 567), Image.Resampling.LANCZOS)
        board.paste(preview, (left + 30, 258))
        draw.rectangle((left + 30, 258, left + 710, 825), outline=(15, 30, 35), width=2)
        footprint = {"A3-A / 1x1": "1×1", "馆守Z夹具 / 2x2": "2×2", "BREAKER夹具 / 3x3": "3×3"}[title]
        draw.text((left + 31, 858), f"footprint = {footprint}", font=font(22, bold=True), fill=(214, 84, 74))
        draw.text((left + 31, 904), "遮挡组填充降至18%，屋檐与单位外轮廓保留。", font=font(21), fill=(24, 43, 50))
        draw.text((left + 31, 948), "不改锚点、碰撞、通行拓扑或屏幕尺度。", font=font(21), fill=(24, 43, 50))
        draw.text((left + 31, 1005), "评审 overlay；没有烘入六层核心图。", font=font(20), fill=(82, 102, 107))
    draw.text((58, 1291), "A3 小体只读取制作人签收的 A 案透明样张；馆守Z与 BREAKER 均为具名几何夹具。", font=font(21), fill=INK_SOFT)
    return board


def viewport_from_composite(composite: Image.Image, camera: tuple[int, int]) -> Image.Image:
    crop_left = round(430 + camera[0])
    crop_top = round(camera[1] - 127)
    tactical = composite.crop((crop_left, crop_top, crop_left + 900, crop_top + 594))
    canvas = Image.new("RGB", (1280, 720), "#0a171d")
    canvas.paste(tactical, (0, 54))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1280, 53), fill="#09151a")
    draw.rectangle((0, 648, 1280, 719), fill="#09151a")
    draw.rectangle((900, 54, 1279, 647), fill="#102229")
    draw.rectangle((915, 70, 1260, 207), fill="#1b171b", outline=CORAL, width=2)
    draw.rectangle((915, 219, 1260, 634), fill="#0d1c22", outline="#3c7881", width=2)
    for rect in ((934, 406, 1075, 444), (1093, 406, 1234, 444), (934, 456, 1075, 494), (1093, 456, 1234, 494), (934, 506, 1075, 544), (1093, 506, 1234, 544)):
        draw.rectangle(rect, outline=GOLD, width=2)
    return canvas


def make_continuity_strip(viewports: dict[str, Image.Image]) -> Image.Image:
    image = Image.new("RGB", (3840, 820), INK_DEEP)
    draw = ImageDraw.Draw(image)
    colors = {"WEST": TEAL, "CENTRAL": GOLD, "EAST": CORAL}
    labels = {item[0]: item[3] for item in REVIEW_CAMERAS}
    for index, code in enumerate(("WEST", "CENTRAL", "EAST")):
        left = index * 1280
        draw.text((left + 32, 29), f"{code}｜{labels[code]}", font=font(25, bold=True), fill=colors[code])
        draw.text((left + 917, 36), "同画布 / 同状态 / 重叠裁切", font=font(17), fill="#aab9b6")
        image.paste(viewports[code], (left, 100))
        if index < 2:
            draw.rectangle((left + 1270, 0, left + 1279, 819), fill=colors[code])
    return image


def checkerboard(size: tuple[int, int], step: int = 20) -> Image.Image:
    image = Image.new("RGB", size, "#e7ece8")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill="#d4dcd7")
    return image


def fit_image(source: Image.Image, size: tuple[int, int], *, checker: bool = False) -> Image.Image:
    background = checkerboard(size) if checker else Image.new("RGB", size, BACKGROUND)
    image = source.convert("RGBA")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    background_rgba = background.convert("RGBA")
    background_rgba.alpha_composite(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return background_rgba.convert("RGB")


def make_layer_switch_board(layers: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGB", (3000, 1800), PAPER)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 3000, 132), fill=INK_DEEP)
    draw.text((60, 31), "A4｜六层逐层开关与透明通道", font=font(47, bold=True), fill=IVORY)
    draw.text((2130, 50), "2400×1350｜origin 0,0｜pixel registered", font=font(21), fill="#b9c8c5")
    order = ("BASE", "BUILDINGS", "ROOFS", "FOREGROUND", "OCCLUSION_MASK", "STATE_LAYERS")
    descriptions = {
        "BASE": "不透明地表；无单位、屋顶、UI或说明文字",
        "BUILDINGS": "透明建筑体；屋顶不重复",
        "ROOFS": "透明屋顶/雨棚/断连廊；对应mask",
        "FOREGROUND": "稀疏前缘世界物件；不以装饰遮棋盘",
        "OCCLUSION_MASK": "R淡出填充 / G屋檐轮廓 / B安全边缘",
        "STATE_LAYERS": "默认态：撤离线active＋盾墙挂＋无新损伤",
    }
    for index, key in enumerate(order):
        column = index % 3
        row = index // 3
        left = 55 + column * 980
        top = 175 + row * 790
        draw.rounded_rectangle((left, top, left + 930, top + 735), radius=8, fill=PANEL, outline=(168, 183, 180), width=2)
        accent = (TEAL, GOLD, CORAL)[column]
        draw.rectangle((left, top, left + 930, top + 68), fill=accent)
        draw.text((left + 25, top + 16), key, font=font(28, bold=True), fill=INK_DEEP)
        preview = fit_image(layers[key], (870, 490), checker=key != "BASE")
        board.paste(preview, (left + 30, top + 95))
        draw.rectangle((left + 30, top + 95, left + 900, top + 585), outline=INK_DEEP, width=2)
        draw.text((left + 30, top + 614), descriptions[key], font=font(20), fill=INK)
        mode = layers[key].mode
        draw.text((left + 30, top + 662), f"{mode}｜2400×1350｜Candidate｜runtime_allowed=false", font=font(18), fill=INK_SOFT)
    return board


def crop_around(image: Image.Image, center: tuple[int, int], width: int = 650, height: int = 430) -> Image.Image:
    left = max(0, min(image.width - width, center[0] - width // 2))
    top = max(0, min(image.height - height, center[1] - height // 2))
    return image.crop((left, top, left + width, top + height))


def make_state_difference_board(
    base: Image.Image,
    buildings: Image.Image,
    roofs: Image.Image,
    foreground: Image.Image,
    variants: dict[str, Image.Image],
) -> Image.Image:
    comparisons = (
        ("撤离线", "active", "cleared", project(28, 4.5), "朱红连续警示变为冷绿分段通行；拓扑不变"),
        ("墙挂位", "wall_hung", "rack_empty", project(11, 10), "具名盾夹具消失，只留下空架；不是正式重盾母版"),
        ("E02新损伤", "damage_before", "damage_after", project(23, 9.5), "道路焦痕与馆墙擦伤可见；不出现E03贯穿或E04碎裂"),
    )
    board = Image.new("RGB", (3000, 1600), PAPER)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 3000, 130), fill=INK_DEEP)
    draw.text((60, 31), "A4｜状态差分连续性", font=font(48, bold=True), fill=IVORY)
    draw.text((2200, 52), "只改可见状态，不改通行拓扑", font=font(21), fill="#b9c8c5")

    for index, (title, before_key, after_key, center, note) in enumerate(comparisons):
        left = 55 + index * 980
        draw.rounded_rectangle((left, 175, left + 930, 1505), radius=8, fill=PANEL, outline=(168, 183, 180), width=2)
        accent = (TEAL, GOLD, CORAL)[index]
        draw.rectangle((left, 175, left + 930, 245), fill=accent)
        draw.text((left + 25, 191), title, font=font(30, bold=True), fill=INK_DEEP)

        before_state = variants[before_key]
        after_state = variants[after_key]
        before_map = compose_map(base, buildings, before_state, roofs, foreground)
        after_map = compose_map(base, buildings, after_state, roofs, foreground)
        before_crop = crop_around(before_map, center).resize((850, 562), Image.Resampling.LANCZOS)
        after_crop = crop_around(after_map, center).resize((850, 562), Image.Resampling.LANCZOS)
        board.paste(before_crop, (left + 40, 285))
        board.paste(after_crop, (left + 40, 885))
        draw.rectangle((left + 40, 285, left + 890, 847), outline=INK_DEEP, width=2)
        draw.rectangle((left + 40, 885, left + 890, 1447), outline=INK_DEEP, width=2)
        draw.rectangle((left + 55, 300, left + 220, 344), fill=INK_DEEP)
        draw.text((left + 72, 309), "BEFORE", font=font(20, bold=True), fill=accent)
        draw.rectangle((left + 55, 900, left + 220, 944), fill=INK_DEEP)
        draw.text((left + 72, 909), "AFTER", font=font(20, bold=True), fill=accent)
        draw.text((left + 42, 1465), note, font=font(18), fill=INK_SOFT)
    return board


def make_overview_board(composite: Image.Image) -> Image.Image:
    board = Image.new("RGB", (3000, 1800), PAPER)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 3000, 135), fill=INK_DEEP)
    draw.text((60, 31), "A4 MAP-B｜万机馆南侧旧会展区首轮美术", font=font(48, bold=True), fill=IVORY)
    draw.text((2200, 52), "六层合成｜无单位｜Candidate", font=font(21), fill="#b9c8c5")
    preview = composite.resize((2200, 1238), Image.Resampling.LANCZOS)
    board.paste(preview, (45, 185))
    draw.rectangle((45, 185, 2245, 1423), outline=INK_DEEP, width=3)
    draw.rounded_rectangle((2295, 185, 2950, 1640), radius=8, fill=PANEL, outline=(168, 183, 180), width=2)
    y = 225
    notes = (
        ("场景身份", "北侧冷白万机馆旧展墙、中央巨体空场、东侧朱红防灾环廊共同成立。", TEAL),
        ("材料", "墨蓝道路、冷白馆墙、低饱和绿灰修补面；朱红只占应急结构与状态提示。", CORAL),
        ("细节密度", "每体块保留一至三处大符号；不使用碎贴纸、密集窗格或高频污迹。", GOLD),
        ("滚动", "WEST、CENTRAL、EAST 是同一2400×1350画布的重叠裁切，不是三张独立背景。", TEAL),
        ("状态", "撤离线、墙挂位和E02新损伤均在独立透明状态层，关闭后不会残留。", CORAL),
        ("边界", "无单位、坐标、箭头、标签或UI烘入地图；不授权Godot或Runtime。", GOLD),
    )
    for title, body, color in notes:
        draw.text((2330, y), title, font=font(25, bold=True), fill=color)
        y += 43
        for line in wrap_text(draw, body, 560, font(21)):
            draw.text((2330, y), line, font=font(21), fill=INK)
            y += 31
        y += 34
    draw.text((55, 1690), f"{PROFILE_ID}｜topology {TOPOLOGY_SHA256[:18]}｜runtime_allowed=false｜runtime_handoff=none", font=font(20), fill=INK_SOFT)
    return board


def wrap_text(draw: ImageDraw.ImageDraw, text: str, width: int, used_font: ImageFont.FreeTypeFont) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if current and draw.textbbox((0, 0), trial, font=used_font)[2] > width:
            lines.append(current)
            current = char
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def write_tsv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_layer_spec() -> None:
    fields = (
        "package_id", "layer_code", "slot_id", "stable_id", "relative_path", "dimensions", "channels", "alpha",
        "origin", "pivot", "layer_order", "render_semantic", "state_semantic", "pixel_registration",
        "topology_sha256", "lifecycle", "runtime_allowed", "runtime_handoff", "user_decision_required",
    )
    rows: list[dict[str, object]] = []
    for code, slot_id, stable_id, filename, order, channels, purpose in CORE_LAYER_ROWS:
        rows.append({
            "package_id": PACKAGE_ID,
            "layer_code": code,
            "slot_id": slot_id,
            "stable_id": stable_id,
            "relative_path": filename,
            "dimensions": "2400x1350",
            "channels": channels,
            "alpha": "opaque" if code == "BASE" else "straight_rgba_transparent",
            "origin": ORIGIN,
            "pivot": PIVOT,
            "layer_order": order,
            "render_semantic": purpose,
            "state_semantic": "default_active_wall_hung_before_damage" if code == "STATE_LAYERS" else "n/a",
            "pixel_registration": "exact_same_canvas",
            "topology_sha256": TOPOLOGY_SHA256,
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "user_decision_required": "true",
        })
    variant_rows = (
        ("STATE_RESCUE_ACTIVE", "A4_MAP_B_STATE_RESCUE_ACTIVE_2400x1350.png", "rescue_lane=active;shield=wall_hung;damage=before"),
        ("STATE_RESCUE_CLEARED", "A4_MAP_B_STATE_RESCUE_CLEARED_2400x1350.png", "rescue_lane=cleared;shield=wall_hung;damage=before"),
        ("STATE_SHIELD_WALL_HUNG", "A4_MAP_B_STATE_SHIELD_WALL_HUNG_2400x1350.png", "rescue_lane=active;shield=wall_hung;damage=before"),
        ("STATE_SHIELD_RACK_EMPTY", "A4_MAP_B_STATE_SHIELD_RACK_EMPTY_2400x1350.png", "rescue_lane=active;shield=rack_empty;damage=before"),
        ("STATE_DAMAGE_BEFORE", "A4_MAP_B_STATE_DAMAGE_BEFORE_2400x1350.png", "rescue_lane=active;shield=wall_hung;damage=before"),
        ("STATE_DAMAGE_AFTER", "A4_MAP_B_STATE_DAMAGE_AFTER_2400x1350.png", "rescue_lane=active;shield=wall_hung;damage=after_E02_non_topology"),
        ("STATE_P1_AFTER", "A4_MAP_B_STATE_P1_AFTER_2400x1350.png", "rescue_lane=cleared;shield=rack_empty;damage=after_E02_non_topology"),
    )
    for code, filename, semantic in variant_rows:
        rows.append({
            "package_id": PACKAGE_ID,
            "layer_code": code,
            "slot_id": "MAP_C01CDV1_R2_STATE_LAYERS",
            "stable_id": f"MAP_C01CDV1_SCROLLING_STREET_R2_{code}",
            "relative_path": filename,
            "dimensions": "2400x1350",
            "channels": "RGBA",
            "alpha": "straight_rgba_transparent",
            "origin": ORIGIN,
            "pivot": PIVOT,
            "layer_order": 20,
            "render_semantic": "reviewable full-canvas state snapshot candidate",
            "state_semantic": semantic,
            "pixel_registration": "exact_same_canvas",
            "topology_sha256": TOPOLOGY_SHA256,
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "user_decision_required": "true",
        })
    write_tsv(OUT / "layer-spec.tsv", fields, rows)


def write_topology_receipt(source_rows: list[dict[str, str]]) -> None:
    fields = tuple(source_rows[0].keys()) + (
        "a4_source_candidate", "a4_canvas", "a4_anchor_or_rect", "a4_match", "a4_art_change", "runtime_allowed", "runtime_handoff",
    )
    rows = []
    for source in source_rows:
        rows.append({
            **source,
            "a4_source_candidate": MAP_CANDIDATE_ID,
            "a4_canvas": "2400x1350",
            "a4_anchor_or_rect": source["anchor_or_rect"],
            "a4_match": "exact",
            "a4_art_change": "material_height_layer_grouping_only",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
        })
    write_tsv(OUT / "topology-lock-receipt.tsv", fields, rows)


def write_source_receipt() -> None:
    fields = ("source_path", "source_sha256", "authority_role", "validation", "usage_boundary", "active_source", "mutation")
    rows = []
    for relative, digest, role in STATIC_SOURCES:
        rows.append({
            "source_path": relative,
            "source_sha256": digest,
            "authority_role": role,
            "validation": "PASS_exact_sha256",
            "usage_boundary": "read_only_current_or_approved_derivative_source",
            "active_source": "true",
            "mutation": "none",
        })
    rows.append({
        "source_path": A3_OVERLAY,
        "source_sha256": A3_OVERLAY_SHA256,
        "authority_role": "approved_A3_A_external_occlusion_overlay",
        "validation": "PASS_exact_sha256",
        "usage_boundary": "review_overlay_only_not_baked_not_atlas",
        "active_source": "true",
        "mutation": "none",
    })
    canon_path = "docs/superpowers/specs/data/canon/scenes.tsv"
    rows.append({
        "source_path": canon_path,
        "source_sha256": sha256_file(ROOT / canon_path),
        "authority_role": "current_canon_scene_scope",
        "validation": "PASS_scoped_V355_C01E02_semantics_whole_file_hash_observed",
        "usage_boundary": "scene_fact_boundary_only_no_canon_write",
        "active_source": "true",
        "mutation": "none",
    })
    write_tsv(OUT / "source-validation-receipt.tsv", fields, rows)


def write_user_decision_card() -> None:
    text = f"""# C01E02 A4 MAP-B 六层地图用户裁决卡

> Package: `{PACKAGE_ID}`  
> Subject: `{SUBJECT_ID}`  
> Topology: `{TOPOLOGY_SHA256}`  
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

请逐项裁决：

1. **场景身份**：是否仍明确是万机馆南侧旧会展区，而不是泛化城市？
2. **质感与密度**：冷白馆墙、墨蓝铺装、朱红防灾结构、绿灰修补面及细节密度是否通过？
3. **六层与滚动**：BASE / BUILDINGS / ROOFS / FOREGROUND / OCCLUSION_MASK / STATE_LAYERS 的拆分、三段滚动连续性和建筑入格是否通过？
4. **遮挡操作性**：A3-A 小体及 2×2 / 3×3 夹具的淡出＋轮廓是否自然，是否妨碍操作？
5. **状态差分**：撤离线 active→cleared、墙挂→空架、道路/建筑损伤前后是否清楚？
6. **派生授权**：是否批准本包中六张核心层具体文件作为 Demo 派生来源？

建议回复：`身份通过；质感通过；六层与滚动通过；遮挡通过；状态通过；批准六张核心层作为Demo派生来源`。

本裁决不等于 exact handoff、Godot 导入或 Runtime promotion。未获六项明确批准，本任务不继续下一项。
"""
    (OUT / "user-decision-card.md").write_text(text, encoding="utf-8")


def write_completion_report() -> None:
    text = f"""# C01E02 A4 MAP-B 六层地图完成报告

## Result

- Package: `{PACKAGE_ID}`
- Selected source: `MAP-B 馆墙防灾环廊型`
- Canvas: `2400×1350`, shared origin `{ORIGIN}`, pivot `{PIVOT}`
- Core layers: `6`
- Review viewports: `WEST / CENTRAL / EAST`, each `1280×720`
- Occlusion: `fade_plus_outline`, building alpha candidate `0.18`
- State evidence: rescue lane, shield rack, E02 road/facade damage

## Boundary

All files remain `Candidate / runtime_allowed=false / runtime_handoff=none`. No unit is baked into the six core layers. The selected A3-A sample appears only on the occlusion review board; Guardian Z and BREAKER are named geometry fixtures. No final atlas, exact handoff, Godot, Runner, R2 manifest, Canon, gameplay, C04, LibTV, paid generation, staging, or commit is produced here.

## Stop Gate

Stopped for the six individual user decisions in `user-decision-card.md`. Specific files may become Demo derivative sources only after explicit user approval and a later producer receipt.
"""
    (OUT / "completion-report.md").write_text(text, encoding="utf-8")


def package_files(*, include_manifest: bool = False) -> list[Path]:
    excluded = {"core-delivery-hashes.sha256", "BLOCKED.md"}
    if not include_manifest:
        excluded.add("asset-manifest.tsv")
    return sorted(
        path for path in OUT.rglob("*")
        if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )


def media_info(path: Path) -> tuple[str, str, str]:
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            return ("image/png", f"{image.width}x{image.height}", image.mode)
    if path.suffix.lower() == ".tsv":
        return ("text/tab-separated-values", "", "UTF-8")
    if path.suffix.lower() == ".md":
        return ("text/markdown", "", "UTF-8")
    if path.suffix.lower() == ".py":
        return ("text/x-python", "", "UTF-8")
    return ("application/octet-stream", "", "")


def write_manifest() -> None:
    fields = (
        "package_id", "asset_id", "relative_path", "subject_id", "media_type", "dimensions", "channels", "asset_role",
        "pixel_registration", "contains_units_baked_in_core", "contains_external_unit_overlay", "uses_old_asset",
        "uses_final_atlas", "topology_sha256", "lifecycle", "runtime_allowed", "runtime_handoff", "sha256",
    )
    rows = []
    core_names = {row[3] for row in CORE_LAYER_ROWS}
    state_names = {
        "A4_MAP_B_STATE_RESCUE_ACTIVE_2400x1350.png",
        "A4_MAP_B_STATE_RESCUE_CLEARED_2400x1350.png",
        "A4_MAP_B_STATE_SHIELD_WALL_HUNG_2400x1350.png",
        "A4_MAP_B_STATE_SHIELD_RACK_EMPTY_2400x1350.png",
        "A4_MAP_B_STATE_DAMAGE_BEFORE_2400x1350.png",
        "A4_MAP_B_STATE_DAMAGE_AFTER_2400x1350.png",
        "A4_MAP_B_STATE_P1_AFTER_2400x1350.png",
    }
    for path in package_files():
        relative = path.relative_to(OUT).as_posix()
        media_type, dimensions, channels = media_info(path)
        if relative in core_names:
            role = "core_layer"
        elif relative in state_names:
            role = "state_variant"
        elif relative == "A4_occlusion_footprint_review_2400x1350.png":
            role = "external_unit_occlusion_review"
        elif media_type == "image/png":
            role = "review_evidence"
        else:
            role = "machine_evidence"
        rows.append({
            "package_id": PACKAGE_ID,
            "asset_id": f"A4_MAP_B_{relative.upper().replace('/', '_').replace('.', '_').replace('-', '_')}",
            "relative_path": relative,
            "subject_id": SUBJECT_ID,
            "media_type": media_type,
            "dimensions": dimensions,
            "channels": channels,
            "asset_role": role,
            "pixel_registration": "exact_2400_canvas" if dimensions == "2400x1350" else "review_derived",
            "contains_units_baked_in_core": "false",
            "contains_external_unit_overlay": "true" if role == "external_unit_occlusion_review" else "false",
            "uses_old_asset": "false",
            "uses_final_atlas": "false",
            "topology_sha256": TOPOLOGY_SHA256,
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "sha256": sha256_file(path),
        })
    write_tsv(OUT / "asset-manifest.tsv", fields, rows)


def write_core_hashes() -> None:
    external = [ROOT / relative for relative, _, _ in STATIC_SOURCES]
    external.extend((ROOT / A3_OVERLAY, ROOT / "docs/superpowers/specs/data/canon/scenes.tsv"))
    package_names = [row[3] for row in CORE_LAYER_ROWS] + [
        "A4_MAP_B_six_layer_composite_full_2400x1350.png",
        "A4_MAP_B_pure_read_no_ui_2400x1350.png",
        "A4_MAP_B_three_viewport_continuity_3840x820.png",
        "A4_layer_switch_alpha_board_3000x1800.png",
        "A4_occlusion_footprint_review_2400x1350.png",
        "A4_state_difference_board_3000x1600.png",
        "A4_MAP_B_overview_review_3000x1800.png",
        "layer-spec.tsv",
        "topology-lock-receipt.tsv",
        "source-validation-receipt.tsv",
        "asset-manifest.tsv",
        "user-decision-card.md",
        "completion-report.md",
        "generate_art_a4_map_b_six_layer.py",
        "validate_art_a4_map_b_six_layer.py",
    ]
    files = external + [OUT / name for name in package_names]
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        raise RuntimeError(f"A4 core hash files missing: {missing}")
    lines = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256_file(path)}  {relative}")
    (OUT / "core-delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_images(tactical: dict) -> None:
    base = draw_base(tactical)
    buildings = draw_buildings(tactical)
    roofs = draw_roofs(tactical)
    foreground = draw_foreground()
    mask = occlusion_mask(buildings, roofs)

    state_core = combine_state_layers("active", "wall_hung", "before")
    variants = {
        "active": combine_state_layers("active", "wall_hung", "before"),
        "cleared": combine_state_layers("cleared", "wall_hung", "before"),
        "wall_hung": combine_state_layers("active", "wall_hung", "before"),
        "rack_empty": combine_state_layers("active", "rack_empty", "before"),
        "damage_before": combine_state_layers("active", "wall_hung", "before"),
        "damage_after": combine_state_layers("active", "wall_hung", "after"),
        "p1_after": combine_state_layers("cleared", "rack_empty", "after"),
    }

    layers = {
        "BASE": base,
        "BUILDINGS": buildings,
        "STATE_LAYERS": state_core,
        "ROOFS": roofs,
        "FOREGROUND": foreground,
        "OCCLUSION_MASK": mask,
    }
    for code, _, _, filename, _, _, _ in CORE_LAYER_ROWS:
        layers[code].save(OUT / filename, optimize=True)

    variant_files = {
        "active": "A4_MAP_B_STATE_RESCUE_ACTIVE_2400x1350.png",
        "cleared": "A4_MAP_B_STATE_RESCUE_CLEARED_2400x1350.png",
        "wall_hung": "A4_MAP_B_STATE_SHIELD_WALL_HUNG_2400x1350.png",
        "rack_empty": "A4_MAP_B_STATE_SHIELD_RACK_EMPTY_2400x1350.png",
        "damage_before": "A4_MAP_B_STATE_DAMAGE_BEFORE_2400x1350.png",
        "damage_after": "A4_MAP_B_STATE_DAMAGE_AFTER_2400x1350.png",
        "p1_after": "A4_MAP_B_STATE_P1_AFTER_2400x1350.png",
    }
    for key, filename in variant_files.items():
        variants[key].save(OUT / filename, optimize=True)

    composite = compose_map(base, buildings, state_core, roofs, foreground)
    pure_read = compose_map(base, buildings, Image.new("RGBA", CANVAS, (0, 0, 0, 0)), roofs, foreground)
    p1_after = compose_map(base, buildings, variants["p1_after"], roofs, foreground)
    composite.save(OUT / "A4_MAP_B_six_layer_composite_full_2400x1350.png", optimize=True)
    pure_read.save(OUT / "A4_MAP_B_pure_read_no_ui_2400x1350.png", optimize=True)
    p1_after.save(OUT / "A4_MAP_B_P1_AFTER_review_2400x1350.png", optimize=True)

    viewports: dict[str, Image.Image] = {}
    for code, _, camera, _ in REVIEW_CAMERAS:
        viewport = viewport_from_composite(composite, camera)
        viewport.save(OUT / f"A4_MAP_B_viewport_{code.lower()}_1280x720.png", optimize=True)
        viewports[code] = viewport
    make_continuity_strip(viewports).save(OUT / "A4_MAP_B_three_viewport_continuity_3840x820.png", optimize=True)
    make_layer_switch_board(layers).save(OUT / "A4_layer_switch_alpha_board_3000x1800.png", optimize=True)
    make_occlusion_demo(base, buildings, state_core, roofs, foreground).save(OUT / "A4_occlusion_footprint_review_2400x1350.png", optimize=True)
    make_state_difference_board(base, buildings, roofs, foreground, variants).save(OUT / "A4_state_difference_board_3000x1600.png", optimize=True)
    make_overview_board(composite).save(OUT / "A4_MAP_B_overview_review_3000x1800.png", optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tactical, topology_rows = validate_sources()
    generate_images(tactical)
    write_layer_spec()
    write_topology_receipt(topology_rows)
    write_source_receipt()
    write_user_decision_card()
    write_completion_report()
    write_manifest()
    write_core_hashes()
    print(f"Generated {PACKAGE_ID}")
    print(f"topology={TOPOLOGY_SHA256}")
    print("core_layers=6 runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
