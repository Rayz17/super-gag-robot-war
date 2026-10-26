#!/usr/bin/env python3
"""Build the ENV-A8 exact Camera V2 recomposition QA.

There are two explicit producer-gated modes.  Neither exposes manual placement
or scale arguments: structure positions, actor footpoints and crops are derived
from the frozen Task111 and golden-slice contracts.
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

OBJECTIVE = ROOT / "A8-camera-v2-structure-plan-recomposition-objective.md"
TASK125 = C01 / "125-c01e02-env-a6-a7-producer-asset-acceptance-and-a8-plan-recomposition-release.md"
GROUND = C01 / "art-a9-1a6-env-a2-simple-recomposition/delivery/GROUND_BAKE_CURRENT_V2_2400x1350.png"
A7 = C01 / "art-a9-1a6-env-a7-camera-v2-six-structure-asset-pack"
A7_STRUCTURES = A7 / "delivery/structures"
A7_HASHES = A7 / "delivery-hashes.sha256"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
SPRITE_CONTRACT = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-sprite-slot-and-socket-contract.json"
GOLDEN_PROFILE = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json"

QA = ROOT / "qa/gate1-a-plan"
ALL_CLEANPLATES = ROOT / "qa/four-profile-actor-free-cleanplates"
PROXY_QA = ROOT / "qa/occlusion-proxy"
RECEIPTS = ROOT / "receipts"

FRAME_SIZE = (1280, 720)
MAP_DRAW_ORIGIN = (0, 58)
EXPECTED = {
    GROUND: "893e0df76d0cbcacba93fc22ef307f15e1dd04748cc4b016ed4bf8cc2537d27a",
    CAMERA: "756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a",
    REGISTRATION: "0133cf5c5af7a6dba659221249b9e0bb45c51bebc8cb9b81c50cf9d920d25b7b",
    SPRITE_CONTRACT: "a6874f033554c71af2e3c1d634cd2671d4a3efd1494ba0bccb491579c0117cce",
    GOLDEN_PROFILE: "61b49e5328e702cd654d28ff39c5c380ba0ae3e78753330635036d33f689523c",
    TASK125: "d6cb1fe4614f440f5da51a480e221797f5afffa25f4ce0ec66ab6852f7f30280",
}
BUILDING_IDS = (
    "NW_BLOCK",
    "NM_BLOCK",
    "NE_BLOCK",
    "SW_BLOCK",
    "SE_BLOCK",
    "BROKEN_SKYWALK",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_csv_ints(value: str, count: int) -> tuple[int, ...]:
    parts = tuple(int(part) for part in value.split(","))
    if len(parts) != count:
        raise ValueError(f"expected {count} comma-separated ints, got {value!r}")
    return parts


def project_raw(x: float, y: float) -> tuple[int, int]:
    return int(round((x - y) * 40)), int(round((x + y) * 24))


def raw_to_source(point: tuple[int, int], origin_raw: tuple[int, int]) -> tuple[int, int]:
    return point[0] - origin_raw[0], point[1] - origin_raw[1]


def footpoint_raw(anchor: list[int] | tuple[int, int], footprint: list[int] | tuple[int, int]) -> tuple[int, int]:
    anchor_x, anchor_y = anchor
    width, height = footprint
    return (
        int(round(40 * (anchor_x - anchor_y + (width - height) / 2))),
        int(round(24 * (anchor_x + anchor_y + width + height - 1))),
    )


def footprint_polygon_source(
    anchor: list[int] | tuple[int, int],
    footprint: list[int] | tuple[int, int],
    origin_raw: tuple[int, int],
) -> list[tuple[int, int]]:
    x, y = anchor
    width, height = footprint
    corners = (
        (x - 0.5, y - 0.5),
        (x + width - 0.5, y - 0.5),
        (x + width - 0.5, y + height - 0.5),
        (x - 0.5, y + height - 0.5),
    )
    return [raw_to_source(project_raw(px, py), origin_raw) for px, py in corners]


def qa_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Helvetica.ttc"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def alpha_scaled(image: Image.Image, factor: float) -> Image.Image:
    out = image.copy()
    out.putalpha(out.getchannel("A").point(lambda value: int(round(value * factor))))
    return out


def count_mask_intersection(left: Image.Image, right: Image.Image) -> int:
    overlap = ImageChops.multiply(left, right)
    return sum(overlap.histogram()[1:])


def load_structure_rows() -> dict[str, dict]:
    with REGISTRATION.open(newline="", encoding="utf-8") as handle:
        rows = {
            row["object_id"]: row
            for row in csv.DictReader(handle, delimiter="\t")
            if row["record_type"] == "STRUCTURE"
        }
    if set(rows) != set(BUILDING_IDS):
        raise AssertionError(f"unexpected structure ids: {sorted(rows)}")

    parsed: dict[str, dict] = {}
    for object_id in BUILDING_IDS:
        row = rows[object_id]
        parsed[object_id] = {
            "grid_rect": parse_csv_ints(row["grid_rect"], 4),
            "visual_bounds_raw": parse_csv_ints(row["visual_bounds_raw"], 4),
            "front_edge_raw": parse_csv_ints(row["front_edge_raw"], 2),
            "world_height_px": int(row["world_height_px"]),
            "registration_point": row["registration_point"],
        }
    return parsed


def load_a7_locked_hashes() -> dict[str, str]:
    locked: dict[str, str] = {}
    for line in A7_HASHES.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(maxsplit=1)
        relative = relative.lstrip("* ")
        if relative.startswith("delivery/structures/"):
            locked[relative] = digest
    if len(locked) != 12:
        raise AssertionError(f"A7 lock must contain 12 structure images, found {len(locked)}")
    return locked


def validate_inputs(camera: dict, structures: dict[str, dict]) -> dict:
    input_hashes: dict[str, str] = {}
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(f"frozen input drift: {path}: {actual} != {expected}")
        input_hashes[str(path.relative_to(PROJECT))] = actual

    locked_a7 = load_a7_locked_hashes()
    for relative, expected in sorted(locked_a7.items()):
        path = A7 / relative
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(f"A7 structure drift: {relative}: {actual} != {expected}")
        input_hashes[str(path.relative_to(PROJECT))] = actual

    projection = camera["projection"]
    if projection["camera_contract_id"] != "CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE":
        raise AssertionError("wrong camera contract")
    if projection["tile_half_px"] != [40, 24] or projection["matrix"] != [[40, -40], [24, 24]]:
        raise AssertionError("Camera V2 projection drift")
    world = projection["world_canvas"]
    if world["size_px"] != [2400, 1350] or world["world_canvas_origin_raw_px"] != [-920, -99]:
        raise AssertionError("Camera V2 world canvas drift")
    expected_crops = {
        "A_PLAN": [680, 515, 1280, 584],
        "B_PLAN": [680, 515, 1280, 584],
        "A_CONTACT": [680, 551, 1280, 584],
        "B_CONTACT": [660, 539, 1280, 584],
    }
    actual_crops = {
        profile_id: profile["source_canvas_crop_px"]
        for profile_id, profile in projection["camera_profiles"].items()
    }
    if actual_crops != expected_crops:
        raise AssertionError(f"Camera V2 profile crop drift: {actual_crops}")

    for object_id, row in structures.items():
        if row["registration_point"] != "structure_front_edge":
            raise AssertionError(f"{object_id}: wrong registration point")

    golden = json.loads(GOLDEN_PROFILE.read_text(encoding="utf-8"))
    staging = golden["contact_staging"]
    if staging["guardian_footprint"] != [2, 2] or staging["breaker_footprint"] != [3, 3]:
        raise AssertionError("gameplay footprint drift")
    if staging["breaker_public_route"] != [[20, 13], [20, 12], [20, 11]]:
        raise AssertionError("BREAKER public route drift")
    if staging["strategies"]["A_BODY_INTERCEPT"]["planning_route"] != [
        [15, 11], [16, 11], [17, 11], [18, 11], [18, 10], [19, 10], [19, 9], [20, 9]
    ]:
        raise AssertionError("A planning route drift")

    sprite = json.loads(SPRITE_CONTRACT.read_text(encoding="utf-8"))
    if sprite["slots"]["V353U001"]["footprint"] != [2, 2]:
        raise AssertionError("GZ slot footprint drift")
    if sprite["slots"]["ENEMY_C01_BREAKER"]["footprint"] != [3, 3]:
        raise AssertionError("BREAKER slot footprint drift")
    input_hashes[str(OBJECTIVE.relative_to(PROJECT))] = sha256(OBJECTIVE)
    return input_hashes


def load_layer(object_id: str, layer: str, expected_size: tuple[int, int]) -> Image.Image:
    path = A7_STRUCTURES / f"{object_id}_{layer}_CAMERA_V2_RGBA.png"
    image = Image.open(path).convert("RGBA")
    if image.size != expected_size:
        raise AssertionError(f"{object_id} {layer}: {image.size} != {expected_size}")
    return image


def compose_world(structures: dict[str, dict], origin_raw: tuple[int, int]) -> tuple[Image.Image, list[dict], list[str]]:
    world = Image.open(GROUND).convert("RGBA")
    if world.size != (2400, 1350):
        raise AssertionError(f"GroundBake size drift: {world.size}")

    placements: list[dict] = []
    loaded: dict[str, dict[str, Image.Image]] = {}
    for object_id, row in structures.items():
        raw_x, raw_y, width, height = row["visual_bounds_raw"]
        source_pos = (raw_x - origin_raw[0], raw_y - origin_raw[1])
        expected_size = (width, height)
        loaded[object_id] = {
            "foundation": load_layer(object_id, "FOUNDATION", expected_size),
            "occluder": load_layer(object_id, "OCCLUDER", expected_size),
        }
        placements.append({
            "object_id": object_id,
            "grid_rect": list(row["grid_rect"]),
            "visual_bounds_raw": list(row["visual_bounds_raw"]),
            "source_canvas_position_px": list(source_pos),
            "local_canvas_px": list(expected_size),
            "front_edge_raw": list(row["front_edge_raw"]),
            "manual_offset_px": [0, 0],
            "display_scale": [1, 1],
            "independent_toggle_layers": ["foundation", "occluder"],
        })

    # Foundations are ground-bound modules.  Occluders are then resolved only by
    # the frozen Task111 front-edge key; no category or hand-authored screen key.
    for placement in placements:
        object_id = placement["object_id"]
        world.alpha_composite(loaded[object_id]["foundation"], tuple(placement["source_canvas_position_px"]))

    occluder_order = sorted(
        BUILDING_IDS,
        key=lambda object_id: (
            structures[object_id]["front_edge_raw"][1],
            structures[object_id]["front_edge_raw"][0],
            object_id,
        ),
    )
    by_id = {placement["object_id"]: placement for placement in placements}
    for object_id in occluder_order:
        world.alpha_composite(loaded[object_id]["occluder"], tuple(by_id[object_id]["source_canvas_position_px"]))
    return world, placements, list(occluder_order)


def crop_frame(world: Image.Image, profile: dict) -> Image.Image:
    x, y, width, height = (int(value) for value in profile["source_canvas_crop_px"])
    if (width, height) != (1280, 584):
        raise AssertionError(f"unexpected Camera V2 map crop: {(width, height)}")
    crop = world.crop((x, y, x + width, y + height))
    frame = Image.new("RGBA", FRAME_SIZE, (5, 13, 19, 255))
    frame.alpha_composite(crop, MAP_DRAW_ORIGIN)
    return frame


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)


def build_a_plan_gate() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    camera = json.loads(CAMERA.read_text(encoding="utf-8"))
    structures = load_structure_rows()
    input_hashes = validate_inputs(camera, structures)

    projection = camera["projection"]
    origin_raw = tuple(projection["world_canvas"]["world_canvas_origin_raw_px"])
    world, placements, occluder_order = compose_world(structures, origin_raw)
    profile = projection["camera_profiles"]["A_PLAN"]
    frame_100 = crop_frame(world, profile)
    frame_50 = frame_100.resize((640, 360), Image.Resampling.LANCZOS)

    path_100 = QA / "A8_A_PLAN_ACTOR_FREE_CLEANPLATE_1280x720.png"
    path_50 = QA / "A8_A_PLAN_ACTOR_FREE_CLEANPLATE_50_PERCENT_640x360.png"
    save_png(frame_100, path_100)
    save_png(frame_50, path_50)

    readback = {
        "task": "ENV_A8_CAMERA_V2_STRUCTURE_PLAN_RECOMPOSITION",
        "status": "A_PLAN_GATE_PRODUCER_REVIEWED_AND_RELEASED_TO_GATE2",
        "authority": "Task125",
        "zero_imagegen": True,
        "qa_only": True,
        "not_plan_asset": True,
        "runtime_bindable": False,
        "actor_free": True,
        "stateful_objects_included": False,
        "real_actor_pixels_included": False,
        "manual_structure_offsets": False,
        "world_canvas_px": projection["world_canvas"]["size_px"],
        "world_canvas_origin_raw_px": list(origin_raw),
        "raw_to_source_canvas_translation_px": projection["world_canvas"]["raw_to_source_canvas_translation_px"],
        "profile": "A_PLAN",
        "camera_raw_px": profile["camera_raw_px"],
        "source_canvas_crop_px": profile["source_canvas_crop_px"],
        "map_draw_origin_in_frame_px": list(MAP_DRAW_ORIGIN),
        "frame_px": list(FRAME_SIZE),
        "foundation_draw_order": list(BUILDING_IDS),
        "occluder_draw_order_by_front_edge": occluder_order,
        "structure_placements": placements,
        "independent_toggle_count": 6,
        "four_profile_built": False,
        "occlusion_proxy_qa_built": False,
        "producer_visual_review": "PASS_GAMEPLAY_STAGING_AND_LOW_OCCLUSION / FAIL_FINAL_ENVIRONMENT_RICHNESS",
        "stop_gate": "RELEASED_TO_GATE2_BY_PRODUCER",
        "inputs_sha256": input_hashes,
        "outputs": {
            str(path_100.relative_to(ROOT)): {"sha256": sha256(path_100), "size_px": [1280, 720]},
            str(path_50.relative_to(ROOT)): {"sha256": sha256(path_50), "size_px": [640, 360]},
        },
    }
    readback_path = RECEIPTS / "A8-A-PLAN-gate-readback.json"
    readback_path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": readback["status"],
        "frame_100": str(path_100),
        "frame_50": str(path_50),
        "readback": str(readback_path),
        "four_profile_built": False,
    }, ensure_ascii=False, indent=2))


def make_actor_proxy(subject_id: str, slot: dict) -> Image.Image:
    width, height = slot["native_canvas"]
    pivot_x, pivot_y = slot["pivot_px"]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")

    if subject_id == "V353U001":
        fill = (38, 202, 224, 205)
        edge = (164, 246, 255, 245)
        dark = (10, 68, 84, 220)
        draw.ellipse((pivot_x - 67, pivot_y - 13, pivot_x + 67, pivot_y + 9), fill=(12, 67, 76, 110))
        draw.polygon([(87, 104), (106, 78), (150, 78), (173, 104), (165, 165), (91, 165)], fill=fill, outline=edge)
        draw.polygon([(55, 112), (87, 96), (91, 142), (63, 151)], fill=dark, outline=edge)
        draw.polygon([(201, 112), (169, 96), (165, 142), (193, 151)], fill=dark, outline=edge)
        draw.polygon([(104, 165), (125, 165), (119, pivot_y), (91, pivot_y)], fill=fill, outline=edge)
        draw.polygon([(131, 165), (152, 165), (165, pivot_y), (137, pivot_y)], fill=fill, outline=edge)
        draw.polygon([(110, 57), (128, 45), (146, 57), (143, 82), (113, 82)], fill=(195, 239, 235, 230), outline=edge)
        draw.line((128, 88, 128, 156), fill=(221, 255, 255, 220), width=4)
        label = "GZ 2x2"
        label_fill = (3, 24, 31, 240)
        label_y = 119
    elif subject_id == "ENEMY_C01_BREAKER":
        fill = (218, 77, 63, 205)
        edge = (255, 188, 128, 245)
        dark = (72, 24, 27, 225)
        draw.ellipse((pivot_x - 145, pivot_y - 20, pivot_x + 145, pivot_y + 12), fill=(80, 22, 24, 105))
        draw.polygon([(58, 174), (91, 105), (157, 72), (228, 78), (300, 127), (326, 207), (290, 272), (237, 292), (117, 285), (66, 246)], fill=fill, outline=edge)
        draw.polygon([(34, 190), (85, 157), (116, 203), (92, 306), (49, pivot_y), (27, 278)], fill=dark, outline=edge)
        draw.polygon([(350, 190), (299, 157), (268, 203), (292, 306), (335, pivot_y), (357, 278)], fill=dark, outline=edge)
        draw.polygon([(128, 285), (183, 264), (175, pivot_y), (99, pivot_y)], fill=fill, outline=edge)
        draw.polygon([(201, 264), (256, 285), (285, pivot_y), (209, pivot_y)], fill=fill, outline=edge)
        draw.polygon([(150, 108), (191, 83), (238, 112), (219, 154), (163, 154)], fill=(112, 31, 33, 235), outline=edge)
        draw.line((169, 127, 219, 127), fill=(255, 87, 66, 255), width=7)
        label = "BREAKER 3x3"
        label_fill = (35, 7, 8, 245)
        label_y = 190
    else:
        raise ValueError(subject_id)

    font = qa_font(17 if subject_id == "V353U001" else 20)
    box = draw.textbbox((0, 0), label, font=font)
    text_width = box[2] - box[0]
    draw.rounded_rectangle(
        (pivot_x - text_width // 2 - 8, label_y - 3, pivot_x + text_width // 2 + 8, label_y + box[3] - box[1] + 5),
        radius=5,
        fill=label_fill,
        outline=edge,
        width=2,
    )
    draw.text((pivot_x - text_width // 2, label_y), label, font=font, fill=(236, 250, 250, 255))
    return image


def build_route_overlay(
    origin_raw: tuple[int, int],
    golden: dict,
) -> tuple[Image.Image, Image.Image, dict]:
    overlay = Image.new("RGBA", (2400, 1350), (0, 0, 0, 0))
    coverage = Image.new("L", (2400, 1350), 0)
    draw = ImageDraw.Draw(overlay, "RGBA")
    mask_draw = ImageDraw.Draw(coverage)
    staging = golden["contact_staging"]

    routes = {
        "GZ_A_ROUTE_2X2": {
            "anchors": staging["strategies"]["A_BODY_INTERCEPT"]["planning_route"],
            "footprint": staging["guardian_footprint"],
            "fill": (34, 207, 226, 44),
            "edge": (80, 235, 245, 195),
            "line": (94, 243, 250, 220),
        },
        "BREAKER_PUBLIC_ROUTE_3X3": {
            "anchors": staging["breaker_public_route"],
            "footprint": staging["breaker_footprint"],
            "fill": (232, 73, 62, 38),
            "edge": (255, 119, 92, 190),
            "line": (255, 137, 96, 225),
        },
    }

    readback: dict[str, dict] = {}
    for route_id, route in routes.items():
        footpoints = [raw_to_source(footpoint_raw(anchor, route["footprint"]), origin_raw) for anchor in route["anchors"]]
        if len(footpoints) > 1:
            draw.line(footpoints, fill=route["line"], width=8, joint="curve")
        for index, anchor in enumerate(route["anchors"]):
            polygon = footprint_polygon_source(anchor, route["footprint"], origin_raw)
            draw.polygon(polygon, fill=route["fill"])
            draw.line(polygon + [polygon[0]], fill=route["edge"], width=3 if index in (0, len(route["anchors"]) - 1) else 1)
            mask_draw.polygon(polygon, fill=255)
        readback[route_id] = {
            "anchors": route["anchors"],
            "footprint": route["footprint"],
            "footpoints_source_canvas_px": [list(point) for point in footpoints],
            "coverage_kind": "union_of_exact_projected_footprint_polygons",
        }
    return overlay, coverage, readback


def load_proxy_actors(
    camera: dict,
    sprite_contract: dict,
    origin_raw: tuple[int, int],
) -> tuple[dict[str, dict], dict]:
    expectations = {
        item["subject_id"]: item
        for item in camera["actor_footpoint_expectations"]["PLAN_SHARED"]
        if item["subject_id"] in ("V353U001", "ENEMY_C01_BREAKER")
    }
    actors: dict[str, dict] = {}
    actor_readback: dict[str, dict] = {}
    profile = camera["projection"]["camera_profiles"]["A_PLAN"]
    camera_raw = profile["camera_raw_px"]
    for subject_id in ("V353U001", "ENEMY_C01_BREAKER"):
        expected = expectations[subject_id]
        slot = sprite_contract["slots"][subject_id]
        if expected["footprint"] != slot["footprint"]:
            raise AssertionError(f"{subject_id}: expectation/slot footprint mismatch")
        raw = footpoint_raw(expected["anchor"], expected["footprint"])
        screen = [640 + raw[0] - camera_raw[0], 350 + raw[1] - camera_raw[1]]
        if screen != expected["screen"]:
            raise AssertionError(f"{subject_id}: footpoint screen mismatch {screen} != {expected['screen']}")
        source = raw_to_source(raw, origin_raw)
        pivot = tuple(slot["pivot_px"])
        top_left = (source[0] - pivot[0], source[1] - pivot[1])
        proxy = make_actor_proxy(subject_id, slot)
        mask = Image.new("L", (2400, 1350), 0)
        mask.paste(proxy.getchannel("A"), top_left)
        actors[subject_id] = {
            "image": proxy,
            "mask": mask,
            "top_left": top_left,
            "footpoint_raw": raw,
            "footpoint_source": source,
            "depth_key_raw": raw[1] + int(slot["z_bias"]),
            "slot": slot,
            "expected": expected,
        }
        actor_readback[subject_id] = {
            "anchor": expected["anchor"],
            "footprint": expected["footprint"],
            "facing": expected["facing"],
            "native_canvas_px": slot["native_canvas"],
            "pivot_px": slot["pivot_px"],
            "z_bias": slot["z_bias"],
            "footpoint_raw_px": list(raw),
            "footpoint_source_canvas_px": list(source),
            "footpoint_A_PLAN_screen_px": screen,
            "expected_A_PLAN_screen_px": expected["screen"],
            "top_left_source_canvas_px": list(top_left),
            "real_actor_pixels": False,
            "proxy_only": True,
        }
    return actors, actor_readback


def load_structure_layers(
    structures: dict[str, dict],
    origin_raw: tuple[int, int],
) -> tuple[dict[str, dict], list[dict]]:
    loaded: dict[str, dict] = {}
    placements: list[dict] = []
    for object_id in BUILDING_IDS:
        row = structures[object_id]
        raw_x, raw_y, width, height = row["visual_bounds_raw"]
        position = raw_to_source((raw_x, raw_y), origin_raw)
        foundation = load_layer(object_id, "FOUNDATION", (width, height))
        occluder = load_layer(object_id, "OCCLUDER", (width, height))
        mask = Image.new("L", (2400, 1350), 0)
        mask.paste(occluder.getchannel("A"), position)
        loaded[object_id] = {
            "foundation": foundation,
            "occluder": occluder,
            "mask": mask,
            "position": position,
            "depth_key_raw": row["front_edge_raw"][1],
        }
        placements.append({
            "object_id": object_id,
            "grid_rect": list(row["grid_rect"]),
            "visual_bounds_raw": list(row["visual_bounds_raw"]),
            "source_canvas_position_px": list(position),
            "front_edge_raw": list(row["front_edge_raw"]),
            "depth_key_raw": row["front_edge_raw"][1],
            "normal_occluder_alpha": 1.0,
            "reveal_occluder_alpha_when_intersecting": 0.34,
            "foundation_alpha_all_states": 1.0,
            "independent_toggle": True,
        })
    return loaded, placements


def find_occlusion_intersections(
    structures: dict[str, dict],
    loaded: dict[str, dict],
    ground_coverage: Image.Image,
    actors: dict[str, dict],
) -> tuple[list[str], dict]:
    audit: dict[str, dict] = {}
    intersecting: list[str] = []
    for object_id in BUILDING_IDS:
        structure = loaded[object_id]
        route_pixels = count_mask_intersection(structure["mask"], ground_coverage)
        body_pixels: dict[str, int] = {}
        body_pixels_all_depths: dict[str, int] = {}
        for subject_id, actor in actors.items():
            raw_pixels = count_mask_intersection(structure["mask"], actor["mask"])
            body_pixels_all_depths[subject_id] = raw_pixels
            is_in_front = structure["depth_key_raw"] > actor["depth_key_raw"]
            body_pixels[subject_id] = raw_pixels if is_in_front else 0
        trigger = route_pixels > 0 or any(value > 0 for value in body_pixels.values())
        if trigger:
            intersecting.append(object_id)
        audit[object_id] = {
            "front_edge_raw_y": structures[object_id]["front_edge_raw"][1],
            "route_or_footprint_intersection_px": route_pixels,
            "actor_body_intersection_px_in_front_only": body_pixels,
            "actor_body_raw_intersection_px_all_depths": body_pixels_all_depths,
            "reveal_triggered": trigger,
            "normal_alpha": 1.0,
            "reveal_alpha": 0.34 if trigger else 1.0,
        }
    return intersecting, audit


def compose_proxy_world(
    loaded: dict[str, dict],
    route_overlay: Image.Image,
    actors: dict[str, dict],
    intersecting: list[str],
    reveal: bool,
) -> Image.Image:
    world = Image.open(GROUND).convert("RGBA")
    for object_id in BUILDING_IDS:
        structure = loaded[object_id]
        world.alpha_composite(structure["foundation"], structure["position"])
    world.alpha_composite(route_overlay)

    events: list[tuple[int, int, str, str]] = []
    for object_id in BUILDING_IDS:
        events.append((loaded[object_id]["depth_key_raw"], 0, "structure", object_id))
    for subject_id, actor in actors.items():
        events.append((actor["depth_key_raw"], 1, "actor", subject_id))

    for _, _, kind, item_id in sorted(events):
        if kind == "structure":
            structure = loaded[item_id]
            image = structure["occluder"]
            if reveal and item_id in intersecting:
                image = alpha_scaled(image, 0.34)
            world.alpha_composite(image, structure["position"])
        else:
            actor = actors[item_id]
            world.alpha_composite(actor["image"], actor["top_left"])
    return world


def annotate_proxy_frame(frame: Image.Image, title: str, subtitle: str, accent: tuple[int, int, int]) -> Image.Image:
    out = frame.copy()
    draw = ImageDraw.Draw(out, "RGBA")
    draw.rectangle((0, 0, 1280, 58), fill=(4, 12, 18, 255))
    draw.text((22, 12), title, font=qa_font(22), fill=(*accent, 255))
    draw.text((22, 38), subtitle, font=qa_font(13), fill=(171, 191, 197, 255))
    draw.rectangle((0, 642, 1280, 720), fill=(4, 12, 18, 255))
    draw.text((22, 659), "QA proxy only / exact 2x2 + 3x3 footprints / frozen routes / no real actor pixels", font=qa_font(15), fill=(171, 191, 197, 255))
    draw.text((22, 682), "Buildings remain independent foundation + occluder modules; composite is NOT a PLAN asset.", font=qa_font(15), fill=(120, 158, 166, 255))
    return out


def make_proxy_comparison(normal: Image.Image, reveal: Image.Image, intersecting: list[str]) -> Image.Image:
    board = Image.new("RGBA", (1280, 420), (4, 12, 18, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.text((22, 12), "A8 OCCLUSION QA / NORMAL vs INTERSECT-ONLY 0.34", font=qa_font(22), fill=(219, 232, 232, 255))
    trigger_text = ", ".join(intersecting) if intersecting else "NONE (normal and reveal are expected to match)"
    draw.text((22, 39), f"0.34 trigger set: {trigger_text}", font=qa_font(14), fill=(244, 174, 101, 255))
    board.alpha_composite(normal.resize((640, 360), Image.Resampling.LANCZOS), (0, 60))
    board.alpha_composite(reveal.resize((640, 360), Image.Resampling.LANCZOS), (640, 60))
    draw.text((18, 72), "NORMAL 1.00", font=qa_font(16), fill=(212, 237, 239, 255))
    draw.text((658, 72), "ONLY INTERSECTING OCCLUDER 0.34", font=qa_font(16), fill=(255, 194, 123, 255))
    return board


def write_toggle_matrix(placements: list[dict], intersecting: list[str]) -> Path:
    path = RECEIPTS / "A8-structure-toggle-and-reveal-matrix.tsv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow((
            "object_id", "independent_foundation", "independent_occluder", "normal_occluder_alpha",
            "proxy_reveal_occluder_alpha", "foundation_alpha", "manual_offset", "composite_role",
        ))
        for placement in placements:
            object_id = placement["object_id"]
            writer.writerow((
                object_id, "true", "true", "1.00", "0.34" if object_id in intersecting else "1.00",
                "1.00", "false", "QA_ONLY_NOT_PLAN_ASSET",
            ))
    return path


def build_all_after_producer_gate() -> None:
    ALL_CLEANPLATES.mkdir(parents=True, exist_ok=True)
    PROXY_QA.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    camera = json.loads(CAMERA.read_text(encoding="utf-8"))
    sprite_contract = json.loads(SPRITE_CONTRACT.read_text(encoding="utf-8"))
    golden = json.loads(GOLDEN_PROFILE.read_text(encoding="utf-8"))
    structures = load_structure_rows()
    input_hashes = validate_inputs(camera, structures)
    projection = camera["projection"]
    origin_raw = tuple(projection["world_canvas"]["world_canvas_origin_raw_px"])

    actor_free_world, _, occluder_order = compose_world(structures, origin_raw)
    output_paths: list[Path] = []
    profile_readback: dict[str, dict] = {}
    profile_frames: dict[str, Image.Image] = {}
    for profile_id in ("A_PLAN", "B_PLAN", "A_CONTACT", "B_CONTACT"):
        profile = projection["camera_profiles"][profile_id]
        frame = crop_frame(actor_free_world, profile)
        profile_frames[profile_id] = frame
        path_100 = ALL_CLEANPLATES / f"A8_{profile_id}_ACTOR_FREE_CLEANPLATE_1280x720.png"
        path_50 = ALL_CLEANPLATES / f"A8_{profile_id}_ACTOR_FREE_CLEANPLATE_50_PERCENT_640x360.png"
        save_png(frame, path_100)
        save_png(frame.resize((640, 360), Image.Resampling.LANCZOS), path_50)
        output_paths.extend((path_100, path_50))
        profile_readback[profile_id] = {
            "branch": profile["branch"],
            "phase": profile["phase"],
            "camera_raw_px": profile["camera_raw_px"],
            "source_canvas_crop_px": profile["source_canvas_crop_px"],
            "frame_100": str(path_100.relative_to(ROOT)),
            "frame_50": str(path_50.relative_to(ROOT)),
        }

    board = Image.new("RGBA", (1280, 780), (4, 12, 18, 255))
    board_draw = ImageDraw.Draw(board, "RGBA")
    board_draw.text((22, 14), "A8 FOUR CAMERA V2 PROFILES / ACTOR-FREE / QA ONLY", font=qa_font(22), fill=(213, 232, 232, 255))
    board_draw.text((22, 41), "Exact registered structures; no manual offsets; composites are not PLAN/CONTACT assets.", font=qa_font(14), fill=(135, 170, 178, 255))
    board_slots = {
        "A_PLAN": (0, 60),
        "B_PLAN": (640, 60),
        "A_CONTACT": (0, 420),
        "B_CONTACT": (640, 420),
    }
    for profile_id, position in board_slots.items():
        board.alpha_composite(profile_frames[profile_id].resize((640, 360), Image.Resampling.LANCZOS), position)
        label_x, label_y = position[0] + 14, position[1] + 10
        board_draw.rounded_rectangle((label_x - 6, label_y - 4, label_x + 118, label_y + 24), radius=5, fill=(3, 12, 18, 220))
        board_draw.text((label_x, label_y), profile_id, font=qa_font(16), fill=(224, 238, 238, 255))
    profile_board_path = ALL_CLEANPLATES / "A8_FOUR_PROFILE_ACTOR_FREE_BOARD_1280x780.png"
    save_png(board, profile_board_path)
    output_paths.append(profile_board_path)

    loaded, placements = load_structure_layers(structures, origin_raw)
    route_overlay, ground_coverage, route_readback = build_route_overlay(origin_raw, golden)
    actors, actor_readback = load_proxy_actors(camera, sprite_contract, origin_raw)
    intersecting, intersection_audit = find_occlusion_intersections(
        structures, loaded, ground_coverage, actors
    )
    normal_world = compose_proxy_world(loaded, route_overlay, actors, intersecting, reveal=False)
    reveal_world = compose_proxy_world(loaded, route_overlay, actors, intersecting, reveal=True)
    diff_rgba = ImageChops.difference(normal_world, reveal_world)
    diff_bands = diff_rgba.split()
    diff_mask = diff_bands[0]
    for band in diff_bands[1:]:
        diff_mask = ImageChops.lighter(diff_mask, band)
    diff_mask = diff_mask.point(lambda value: 255 if value > 0 else 0)
    allowed_diff_mask = Image.new("L", (2400, 1350), 0)
    for object_id in intersecting:
        allowed_diff_mask = ImageChops.lighter(allowed_diff_mask, loaded[object_id]["mask"])
    allowed_diff_mask = allowed_diff_mask.point(lambda value: 255 if value > 0 else 0)
    outside_allowed = ImageChops.multiply(diff_mask, ImageChops.invert(allowed_diff_mask))
    outside_allowed_pixels = sum(outside_allowed.histogram()[1:])
    if outside_allowed_pixels != 0:
        raise AssertionError(f"reveal changed pixels outside triggered occluders: {outside_allowed_pixels}")
    reveal_diff_audit = {
        "changed_pixel_count": sum(diff_mask.histogram()[1:]),
        "changed_bbox_source_canvas_px": list(diff_mask.getbbox()) if diff_mask.getbbox() else None,
        "allowed_occluder_ids": intersecting,
        "changed_pixels_outside_allowed_occluders": outside_allowed_pixels,
        "only_intersecting_occluders_changed": outside_allowed_pixels == 0,
    }
    profile = projection["camera_profiles"]["A_PLAN"]
    normal_frame = annotate_proxy_frame(
        crop_frame(normal_world, profile),
        "A PLAN / EXACT GAMEPLAY PROXY / NORMAL 1.00",
        "GZ east 2x2 + BREAKER north 3x3 + A route + public north-charge route",
        (90, 224, 231),
    )
    reveal_frame = annotate_proxy_frame(
        crop_frame(reveal_world, profile),
        "A PLAN / INTERSECT-ONLY REVEAL 0.34",
        "Triggered occluders: " + (", ".join(intersecting) if intersecting else "none"),
        (244, 174, 101),
    )
    normal_path = PROXY_QA / "A8_A_PLAN_EXACT_FOOTPRINT_ROUTE_PROXY_NORMAL_1280x720.png"
    reveal_path = PROXY_QA / "A8_A_PLAN_EXACT_FOOTPRINT_ROUTE_PROXY_INTERSECT_ONLY_REVEAL_034_1280x720.png"
    comparison_path = PROXY_QA / "A8_A_PLAN_OCCLUSION_NORMAL_VS_INTERSECT_ONLY_034_COMPARISON_1280x420.png"
    save_png(normal_frame, normal_path)
    save_png(reveal_frame, reveal_path)
    save_png(make_proxy_comparison(normal_frame, reveal_frame, intersecting), comparison_path)
    output_paths.extend((normal_path, reveal_path, comparison_path))

    toggle_path = write_toggle_matrix(placements, intersecting)
    output_paths.append(toggle_path)
    readback = {
        "task": "ENV_A8_CAMERA_V2_STRUCTURE_PLAN_RECOMPOSITION",
        "status": "PRODUCER_PASS_EXACT_STRUCTURE_RECOMPOSITION_AND_INTERSECT_ONLY_REVEAL_NOT_FINAL_PLAN",
        "gate1_producer_decision": "PASS_GAMEPLAY_STAGING_AND_LOW_OCCLUSION / FAIL_FINAL_ENVIRONMENT_RICHNESS",
        "zero_imagegen": True,
        "qa_only": True,
        "not_plan_asset": True,
        "runtime_bindable": False,
        "manual_structure_offsets": False,
        "camera_modified": False,
        "topology_modified": False,
        "real_actor_pixels_included": False,
        "four_profile_built": True,
        "four_profile_actor_free": True,
        "profile_readback": profile_readback,
        "foundation_draw_order": list(BUILDING_IDS),
        "occluder_draw_order_by_front_edge": occluder_order,
        "structure_placements": placements,
        "independent_toggle_count": 6,
        "proxy_profile": "A_PLAN",
        "proxy_actor_readback": actor_readback,
        "route_readback": route_readback,
        "intersection_method": "exact placed occluder alpha vs union of projected route/footprint coverage; actor-body overlap only when structure depth key is in front",
        "intersecting_occluder_ids": intersecting,
        "intersecting_occluder_count": len(intersecting),
        "non_intersecting_occluder_count": 6 - len(intersecting),
        "whole_map_fade": False,
        "foundation_alpha_all_states": 1.0,
        "intersection_audit": intersection_audit,
        "normal_vs_reveal_pixel_diff_audit": reveal_diff_audit,
        "producer_visual_review": "PASS_EXACT_STRUCTURE_RECOMPOSITION_AND_INTERSECT_ONLY_REVEAL / FAIL_FINAL_ENVIRONMENT_RICHNESS / NOT_FINAL_PLAN",
        "known_environment_gap": "seven independent gameplay-object and road-result layers",
        "next_gap_exact_slots": [
            "PROP_C01CDV1_RETIRED_SHIELD",
            "PROP_C01CDV1_RETIRED_SHIELD_SUPPORT_PLINTH",
            "TARGET_C01_EAST_EXIT",
            "TARGET_C01_SECURITY_GATE_ACTIVE",
            "TARGET_C01_SECURITY_GATE_DAMAGED",
            "ROAD_DAMAGE_A_42_OVERLAY",
            "ROAD_DAMAGE_B_24_OVERLAY",
        ],
        "not_the_gap": ["building rebake", "camera change", "building position change", "topology change", "arbitrary decoration"],
        "closed": [
            "STATEFUL_OBJECT_ART", "REAL_ACTOR_PIXELS", "FINAL_PLAN", "FINAL_CONTACT",
            "RUNTIME", "DEFAULT", "SAVE", "CANON", "HUMAN_PLAYTEST",
        ],
        "inputs_sha256": input_hashes,
        "outputs": {},
    }
    for path in output_paths:
        if path.suffix.lower() == ".png":
            with Image.open(path) as image:
                metadata = {"sha256": sha256(path), "size_px": list(image.size), "mode": image.mode}
        else:
            metadata = {"sha256": sha256(path), "bytes": path.stat().st_size}
        readback["outputs"][str(path.relative_to(ROOT))] = metadata

    readback_path = RECEIPTS / "A8-full-recomposition-and-occlusion-readback.json"
    readback_path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": readback["status"],
        "cleanplates": 4,
        "intersecting_occluder_ids": intersecting,
        "normal_proxy": str(normal_path),
        "reveal_proxy": str(reveal_path),
        "comparison": str(comparison_path),
        "readback": str(readback_path),
    }, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument(
        "--a-plan-gate",
        action="store_true",
        help="Build only the actor-free A_PLAN 100%/50% producer gate.",
    )
    modes.add_argument(
        "--build-all",
        action="store_true",
        help="After Gate 1 producer PASS, build four cleanplates and exact proxy QA.",
    )
    args = parser.parse_args()
    if args.a_plan_gate:
        build_a_plan_gate()
    else:
        build_all_after_producer_gate()


if __name__ == "__main__":
    main()
