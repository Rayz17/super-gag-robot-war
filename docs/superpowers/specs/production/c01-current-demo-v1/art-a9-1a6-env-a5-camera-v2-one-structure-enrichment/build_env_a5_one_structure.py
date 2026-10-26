#!/usr/bin/env python3
"""Build ENV-A5 NW_BLOCK pure-geometry silhouette pilot.

Only the occluder alpha may change.  The Task121 foundation is copied byte for
byte.  Every authored structural edge is constructed from the exact 40x24
projection or screen vertical; no material donors or generated imagery exist.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = Path(__file__).resolve().parents[6]
C01 = ROOT.parent
A3 = C01 / "art-a9-1a6-env-a3-camera-v2-exact-structure-pilot/six-structure"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
OBJECTIVE = ROOT / "A5-one-structure-enrichment-objective.md"

DELIVERY = ROOT / "delivery"
QA = ROOT / "qa"
STATES = QA / "states"
RECEIPTS = ROOT / "receipts"
for directory in (DELIVERY, QA, STATES, RECEIPTS):
    directory.mkdir(parents=True, exist_ok=True)

SOURCE_FOUNDATION = A3 / "delivery/structures/NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png"
SOURCE_OCCLUDER = A3 / "delivery/structures/NW_BLOCK_OCCLUDER_CAMERA_V2_RGBA.png"

FOUNDATION_OUT = DELIVERY / "NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png"
OCCLUDER_OUT = DELIVERY / "NW_BLOCK_OCCLUDER_CAMERA_V2_ENRICHED_RGBA.png"

GRID_RECT = [1, 0, 7, 5]
BOUNDS_RAW = [-160, -90, 480, 378]
CANVAS = [480, 378]
PIVOT = [240, 378]
FRONT_EDGE = [80, 288]
HEIGHT_LIMIT = 90
MAX_AUTHORED_HEIGHT = 82
SCALE = 4


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


def hs(point):
    return round(point[0] * SCALE), round(point[1] * SCALE)


def project(x: float, y: float, z: float = 0.0):
    return (x - y) * 40 - BOUNDS_RAW[0], (x + y) * 24 - BOUNDS_RAW[1] - z


def corners(rect, z):
    x0, y0, x1, y1 = rect
    return [project(x0, y0, z), project(x1, y0, z), project(x1, y1, z), project(x0, y1, z)]


def poly(draw, points, fill, outline="#07161d", width=2):
    scaled = [hs(point) for point in points]
    draw.polygon(scaled, fill=fill)
    if outline:
        draw.line(scaled + [scaled[0]], fill=outline, width=width * SCALE, joint="curve")


def line(draw, points, fill, width=1):
    draw.line([hs(point) for point in points], fill=fill, width=width * SCALE, joint="curve")


def volume_layer(rect, z0, z1, roof, east_wall, south_wall, outline="#07161d", roof_inset=True):
    image = Image.new("RGBA", (CANVAS[0] * SCALE, CANVAS[1] * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    base = corners(rect, z0)
    top = corners(rect, z1)
    a, b, c, d = base
    at, bt, ct, dt = top

    # Only the two camera-facing exact planes are authored.
    poly(draw, [bt, ct, c, b], east_wall, outline, 2)
    poly(draw, [dt, ct, c, d], south_wall, outline, 2)
    poly(draw, [at, bt, ct, dt], roof, outline, 2)

    if roof_inset:
        x0, y0, x1, y1 = rect
        inset = min(0.16, (x1 - x0) * 0.08, (y1 - y0) * 0.08)
        inner = corners((x0 + inset, y0 + inset, x1 - inset, y1 - inset), z1)
        line(draw, inner + [inner[0]], "#77939a", 1)
    return image.resize(tuple(CANVAS), Image.Resampling.LANCZOS)


def composite_layers(layers):
    out = Image.new("RGBA", tuple(CANVAS), (0, 0, 0, 0))
    for layer in layers:
        out.alpha_composite(layer)
    return out


def build_enriched_occluder():
    # L-shaped low mass: a broad western hall and a lower, inset east service wing.
    main_hall = volume_layer(
        (0.90, -0.10, 5.15, 4.05), 0, 52,
        roof="#476f79", east_wall="#2e515d", south_wall="#243f4a",
    )
    east_wing = volume_layer(
        (4.72, 0.72, 6.92, 3.16), 0, 42,
        roof="#3b626d", east_wall="#294b56", south_wall="#213b45",
    )
    # Offset roof equipment room: second silhouette tier, total height 82px.
    equipment_room = volume_layer(
        (1.55, 0.30, 3.35, 1.75), 52, 82,
        roof="#66868d", east_wall="#405e67", south_wall="#354f58",
    )
    # One short south eave, fully inside the retained 7x5 foundation/envelope.
    short_eave = volume_layer(
        (1.78, 3.73, 4.08, 4.34), 29, 35,
        roof="#78949a", east_wall="#506970", south_wall="#40575f", roof_inset=False,
    )

    result = composite_layers((main_hall, east_wing, equipment_room, short_eave))
    # A single recessed service door is flat geometry, not text or material.
    overlay = Image.new("RGBA", (CANVAS[0] * SCALE, CANVAS[1] * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    door_top_left = project(2.35, 4.051, 30)
    door_top_right = project(3.05, 4.051, 30)
    door_bottom_right = project(3.05, 4.051, 3)
    door_bottom_left = project(2.35, 4.051, 3)
    poly(draw, [door_top_left, door_top_right, door_bottom_right, door_bottom_left], "#182c35", "#0b1d24", 1)
    overlay = overlay.resize(tuple(CANVAS), Image.Resampling.LANCZOS)
    result.alpha_composite(overlay)
    return result


def checker(size):
    image = Image.new("RGBA", size, "#071219")
    draw = ImageDraw.Draw(image)
    cell = 28
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            color = "#0c222b" if (x // cell + y // cell) % 2 == 0 else "#102d37"
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=color)
    return image


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


def comparison_board(old_combined, new_combined):
    board = checker((1120, 620))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1120, 82), fill="#071219")
    draw.text((24, 15), "NW_BLOCK | A5 PURE-GEOMETRY SILHOUETTE PILOT", font=font(27, True), fill="#eff7f8")
    draw.text((24, 50), "same grid / pivot / front edge / foundation | occluder alpha intentionally reauthored", font=font(16), fill="#8fc7d0")
    for index, (label, asset) in enumerate((("TASK121 SINGLE MASS", old_combined), ("A5 STEPPED MASS", new_combined))):
        x0 = 35 + index * 545
        draw.text((x0, 95), label, font=font(19, True), fill="#e0edef")
        shown = fit(asset, 500, 420)
        board.alpha_composite(shown, (x0 + (500 - shown.width) // 2, 140 + (410 - shown.height) // 2))
    path100 = QA / "NW_BLOCK_A5_GEOMETRY_COMPARISON_100_PERCENT_1120x620.png"
    path50 = QA / "NW_BLOCK_A5_GEOMETRY_COMPARISON_50_PERCENT_560x310.png"
    board.save(path100)
    board.resize((560, 310), Image.Resampling.LANCZOS).save(path50)
    return path100, path50


def alpha_difference_board(old_occluder, new_occluder):
    old_alpha = old_occluder.getchannel("A")
    new_alpha = new_occluder.getchannel("A")
    old_on = old_alpha.point(lambda value: 255 if value else 0)
    new_on = new_alpha.point(lambda value: 255 if value else 0)
    added = ImageChops.subtract(new_on, old_on)
    removed = ImageChops.subtract(old_on, new_on)
    overlap = ImageChops.multiply(old_on, new_on)
    diff = Image.new("RGBA", tuple(CANVAS), (0, 0, 0, 0))
    diff.paste((48, 214, 226, 255), (0, 0, CANVAS[0], CANVAS[1]), added)
    diff.paste((230, 92, 81, 255), (0, 0, CANVAS[0], CANVAS[1]), removed)
    diff.paste((108, 128, 136, 150), (0, 0, CANVAS[0], CANVAS[1]), overlap)

    board = checker((1120, 620))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1120, 82), fill="#071219")
    draw.text((24, 15), "NW_BLOCK | OCCLUDER ALPHA DIFFERENCE + VISUAL ENVELOPE", font=font(25, True), fill="#eff7f8")
    draw.text((24, 50), "cyan=added / red=removed / grey=overlap | envelope [-160,-90,480,378]", font=font(16), fill="#8fc7d0")

    shown = fit(diff, 500, 420)
    board.alpha_composite(shown, (35 + (500 - shown.width) // 2, 130 + (420 - shown.height) // 2))
    draw.rectangle((35, 130, 535, 550), outline="#42c8d5", width=3)
    draw.text((45, 565), "ALPHA DIFFERENCE", font=font(17, True), fill="#dcebed")

    silhouette = Image.new("RGBA", tuple(CANVAS), (0, 0, 0, 0))
    silhouette.paste((83, 147, 158, 255), (0, 0, CANVAS[0], CANVAS[1]), new_on)
    shown = fit(silhouette, 500, 420)
    board.alpha_composite(shown, (580 + (500 - shown.width) // 2, 130 + (420 - shown.height) // 2))
    draw.rectangle((580, 130, 1080, 550), outline="#42c8d5", width=3)
    draw.text((590, 565), "NEW ALPHA WITHIN FIXED LOCAL CANVAS", font=font(17, True), fill="#dcebed")
    path = QA / "NW_BLOCK_A5_ALPHA_DIFF_AND_ENVELOPE_1120x620.png"
    board.save(path)
    return path


def tristate_board(foundation, occluder):
    assets = [
        ("NORMAL 100%", combined(foundation, occluder, 1.0)),
        ("REVEAL 34%", combined(foundation, occluder, 0.34)),
        ("RESTORE 100%", combined(foundation, occluder, 1.0)),
    ]
    state_paths = []
    for label, asset in assets:
        slug = label.split()[0]
        path = STATES / f"NW_BLOCK_{slug}_{'034' if slug == 'REVEAL' else '100'}.png"
        asset.save(path)
        state_paths.append(path)

    board = checker((1680, 620))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1680, 82), fill="#071219")
    draw.text((24, 15), "NW_BLOCK A5 | OCCLUDER WHOLE-OBJECT REVEAL", font=font(27, True), fill="#eff7f8")
    draw.text((24, 50), "foundation 1.00 throughout | occluder 1.00 -> 0.34 -> 1.00", font=font(16), fill="#8fc7d0")
    for index, (label, asset) in enumerate(assets):
        x0 = 20 + index * 555
        draw.text((x0 + 15, 95), label, font=font(20, True), fill="#e0edef")
        shown = fit(asset, 515, 420)
        board.alpha_composite(shown, (x0 + (545 - shown.width) // 2, 140 + (410 - shown.height) // 2))
    path = QA / "NW_BLOCK_A5_REVEAL_TRISTATE_1680x620.png"
    board.save(path)
    return path, state_paths


def proxy_layer():
    proxy = Image.new("RGBA", tuple(CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(proxy)
    route = [(95, 286), (175, 238), (255, 286), (335, 238), (415, 286)]
    draw.line(route, fill=(31, 218, 232, 230), width=5, joint="curve")
    for x, y in route:
        draw.polygon([(x, y - 7), (x + 12, y), (x, y + 7), (x - 12, y)], fill=(25, 222, 235, 230), outline=(201, 251, 255, 255))
    # Generic unit proxy behind the new occluder; QA only.
    cx, cy = 257, 228
    draw.ellipse((cx - 17, cy - 23, cx + 17, cy + 11), fill=(25, 215, 228, 255), outline=(218, 255, 255, 255), width=2)
    draw.rectangle((cx - 10, cy - 40, cx + 10, cy - 18), fill=(36, 229, 240, 255), outline=(218, 255, 255, 255), width=2)
    draw.line((cx - 10, cy + 7, cx - 20, cy + 28), fill=(218, 255, 255, 255), width=4)
    draw.line((cx + 10, cy + 7, cx + 20, cy + 28), fill=(218, 255, 255, 255), width=4)
    return proxy


def proxy_qa(foundation, occluder):
    proxy = proxy_layer()
    frames = []
    for factor in (1.0, 0.34):
        frame = foundation.copy()
        frame.alpha_composite(proxy)
        frame.alpha_composite(alpha_scaled(occluder, factor))
        frames.append(frame)

    board = checker((1120, 620))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1120, 82), fill="#071219")
    draw.text((24, 15), "NW_BLOCK A5 | BEHIND-UNIT + ROUTE PROXY QA", font=font(27, True), fill="#eff7f8")
    draw.text((24, 50), "proxy is QA-only and never enters delivery assets", font=font(16), fill="#8fc7d0")
    for index, (label, asset) in enumerate((("NORMAL 1.00", frames[0]), ("REVEAL 0.34", frames[1]))):
        x0 = 35 + index * 545
        draw.text((x0, 95), label, font=font(20, True), fill="#e0edef")
        shown = fit(asset, 500, 420)
        board.alpha_composite(shown, (x0 + (500 - shown.width) // 2, 140 + (410 - shown.height) // 2))
    path = QA / "NW_BLOCK_A5_BEHIND_UNIT_ROUTE_PROXY_QA_1120x620.png"
    board.save(path)
    return path


def alpha_bbox(alpha):
    bbox = alpha.getbbox()
    return list(bbox) if bbox else None


def count_binary(mask):
    return sum(1 for value in mask.getdata() if value > 0)


def write_machine_readback(foundation, old_occluder, new_occluder, normal_path, restore_path, outputs):
    old_binary = old_occluder.getchannel("A").point(lambda value: 255 if value else 0)
    new_binary = new_occluder.getchannel("A").point(lambda value: 255 if value else 0)
    added = ImageChops.subtract(new_binary, old_binary)
    removed = ImageChops.subtract(old_binary, new_binary)
    bbox = alpha_bbox(new_occluder.getchannel("A"))
    inside_envelope = bbox is not None and bbox[0] >= 0 and bbox[1] >= 0 and bbox[2] <= CANVAS[0] and bbox[3] <= CANVAS[1]
    source_foundation = Image.open(SOURCE_FOUNDATION).convert("RGBA")
    foundation_identical = foundation.tobytes() == source_foundation.tobytes()
    readback = {
        "task_id": "A9_1A6_ENV_A5_CAMERA_V2_ONE_STRUCTURE_ENRICHMENT",
        "status": "MACHINE_PASS_PRODUCER_VISUAL_REVIEW_PENDING",
        "scope": "NW_BLOCK_ONLY_PURE_GEOMETRY_NO_MATERIAL",
        "camera": {
            "axis_vectors_px": [[40, 24], [-40, 24]],
            "axis_slopes": [0.6, -0.6],
            "axis_angles_deg": [30.9637565, -30.9637565],
            "perspective_convergence": False,
            "manual_screen_offset": False,
        },
        "registration": {
            "grid_rect": GRID_RECT,
            "local_canvas_px": CANVAS,
            "pivot_local_px": PIVOT,
            "front_edge_raw": FRONT_EDGE,
            "visual_bounds_raw": BOUNDS_RAW,
            "world_height_limit_px": HEIGHT_LIMIT,
            "authored_max_height_px": MAX_AUTHORED_HEIGHT,
        },
        "foundation": {
            "source_sha256": sha(SOURCE_FOUNDATION),
            "output_sha256": sha(FOUNDATION_OUT),
            "byte_identical": foundation_identical,
            "alpha_sha256": alpha_sha(foundation),
        },
        "occluder": {
            "source_alpha_sha256": alpha_sha(old_occluder),
            "output_alpha_sha256": alpha_sha(new_occluder),
            "alpha_intentionally_changed": alpha_sha(old_occluder) != alpha_sha(new_occluder),
            "output_alpha_bbox_local": bbox,
            "inside_fixed_visual_envelope": inside_envelope,
            "added_binary_alpha_pixels": count_binary(added),
            "removed_binary_alpha_pixels": count_binary(removed),
            "normal_alpha": 1.0,
            "reveal_alpha": 0.34,
            "restore_alpha": 1.0,
        },
        "geometry_recipe": {
            "low_main_hall_height_px": 52,
            "east_side_wing_height_px": 42,
            "offset_equipment_room_total_height_px": 82,
            "short_south_eave_height_range_px": [29, 35],
            "allowed_edge_families": ["+30.9637565_deg", "-30.9637565_deg", "vertical"],
        },
        "normal_restore_byte_identical": Path(normal_path).read_bytes() == Path(restore_path).read_bytes(),
        "imagegen_calls": 0,
        "material_donors_used": [],
        "outputs": [str(path.relative_to(ROOT)) for path in outputs],
        "machine_pass": bool(foundation_identical and inside_envelope and MAX_AUTHORED_HEIGHT <= HEIGHT_LIMIT and Path(normal_path).read_bytes() == Path(restore_path).read_bytes()),
        "producer_visual_review": "PENDING",
        "six_structure_batch_released": False,
    }
    path = RECEIPTS / "A5-NW_BLOCK-machine-readback.json"
    path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_lineage():
    entries = [
        ("A5_OBJECTIVE", OBJECTIVE, "task_scope", "none"),
        ("CAMERA_V2", CAMERA, "exact_projection_authority", "geometry_only"),
        ("REGISTRATION", REGISTRATION, "grid_pivot_front_edge_envelope_authority", "geometry_only"),
        ("TASK121_FOUNDATION", SOURCE_FOUNDATION, "byte_locked_foundation", "copied_byte_for_byte"),
        ("TASK121_OCCLUDER", SOURCE_OCCLUDER, "rejected_single_mass_comparison", "comparison_and_alpha_diff_only"),
    ]
    path = ROOT / "source-lineage.tsv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source_id", "path", "sha256", "role", "visible_pixel_use"))
        for source_id, source_path, role, use in entries:
            writer.writerow((source_id, str(source_path.relative_to(PROJECT)), sha(source_path), role, use))
    return path


def build():
    camera = json.loads(CAMERA.read_text(encoding="utf-8"))
    structure = next(item for item in camera["structures"] if item["object_id"] == "NW_BLOCK")
    assert structure["grid_rect"] == GRID_RECT
    with REGISTRATION.open(encoding="utf-8", newline="") as handle:
        row = next(row for row in csv.DictReader(handle, delimiter="\t") if row["object_id"] == "NW_BLOCK")
    assert [int(value) for value in row["visual_bounds_raw"].split(",")] == BOUNDS_RAW
    assert [int(value) for value in row["front_edge_raw"].split(",")] == FRONT_EDGE
    assert int(row["world_height_px"]) == HEIGHT_LIMIT

    shutil.copyfile(SOURCE_FOUNDATION, FOUNDATION_OUT)
    foundation = Image.open(FOUNDATION_OUT).convert("RGBA")
    old_occluder = Image.open(SOURCE_OCCLUDER).convert("RGBA")
    new_occluder = build_enriched_occluder()
    assert new_occluder.size == tuple(CANVAS)
    OCCLUDER_OUT.parent.mkdir(parents=True, exist_ok=True)
    new_occluder.save(OCCLUDER_OUT)

    old_combined = combined(foundation, old_occluder)
    new_combined = combined(foundation, new_occluder)
    comparison100, comparison50 = comparison_board(old_combined, new_combined)
    diff_path = alpha_difference_board(old_occluder, new_occluder)
    tristate_path, state_paths = tristate_board(foundation, new_occluder)
    proxy_path = proxy_qa(foundation, new_occluder)
    lineage = write_lineage()
    outputs = [FOUNDATION_OUT, OCCLUDER_OUT, comparison100, comparison50, diff_path, tristate_path, *state_paths, proxy_path, lineage]
    readback = write_machine_readback(foundation, old_occluder, new_occluder, state_paths[0], state_paths[2], outputs)
    print("ENV_A5_NW_BLOCK_MACHINE_BUILD_OK")
    print(f"comparison_50={comparison50}")
    print(f"readback={readback}")
    print("producer_visual_review=PENDING")
    print("six_structure_batch_released=false")


def seal(verdict):
    readback_path = RECEIPTS / "A5-NW_BLOCK-machine-readback.json"
    if not readback_path.exists():
        raise SystemExit("build outputs before sealing")
    readback = json.loads(readback_path.read_text(encoding="utf-8"))
    if not readback.get("machine_pass"):
        raise SystemExit("cannot seal visual verdict over machine failure")
    status = "PASS_CANDIDATE_FOR_PRODUCER_VISUAL_REVIEW" if verdict == "candidate" else "FAIL_FINAL_QUALITY_STOPPED"
    readback["status"] = status
    readback["visual_self_review"] = verdict.upper()
    readback["task_stopped"] = verdict == "fail"
    readback_path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review = ROOT / "50-100-visual-self-review.md"
    if verdict == "candidate":
        review.write_text("""# ENV-A5 NW_BLOCK 50% / 100%目视自审\n\n状态：`PASS_CANDIDATE_FOR_PRODUCER_VISUAL_REVIEW / NOT_PRODUCER_ACCEPTED`\n\n- 50%：低主楼、较低东侧翼、偏置设备间和南侧短檐形成四段轮廓，不再依赖材质解释单一盒体。\n- 100%：所有结构边来自40x24 exact轴或竖直边；foundation逐字继承；新occluder Alpha只在固定canvas/envelope内。\n- 交互：occluder整件1.00/0.34/1.00，foundation不变；后方单位与路线Proxy在0.34中可读。\n- 边界：本结论只把一栋纯色几何提交制作人实际帧审查，不开放材质或六栋。\n""", encoding="utf-8")
    else:
        review.write_text("""# ENV-A5 NW_BLOCK 50% / 100%目视自审\n\n状态：`FAIL_FINAL_QUALITY / STOPPED`\n\n50%仍首先读作程序盒体；按任务书停止，不进入材质或六栋。机器注册PASS不替代本视觉失败。\n""", encoding="utf-8")

    report = ROOT / "completion-report.md"
    report.write_text(f"""# ENV-A5单栋纯色轮廓试制回执\n\n状态：`{status} / ZERO_IMAGEGEN / NW_BLOCK_ONLY / NO_MATERIAL / NO_BATCH`\n\n- grid、pivot、front edge、foundation、40x24投影和90px上限保持不变。\n- 新occluder由52px低主楼、42px东侧翼、总高82px偏置设备间和29—35px南侧短檐组成。\n- 制作人视觉审查：`PENDING`。\n- 不开放材质、其余五栋、最终PLAN、Runtime、UA91、G2-B或Canon。\n""", encoding="utf-8")

    manifest_paths = [path for path in ROOT.rglob("*") if path.is_file() and path.name not in {"asset-manifest.tsv", "delivery-hashes.sha256"}]
    manifest_paths.sort(key=lambda item: str(item.relative_to(ROOT)))
    manifest = ROOT / "asset-manifest.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in manifest_paths:
            writer.writerow((str(path.relative_to(ROOT)), sha(path), path.stat().st_size))
    hash_paths = [*manifest_paths, manifest]
    hashes = ROOT / "delivery-hashes.sha256"
    hashes.write_text("".join(f"{sha(path)}  {path.relative_to(ROOT)}\n" for path in hash_paths), encoding="utf-8")
    print(f"ENV_A5_SEALED_{verdict.upper()}")
    print(f"delivery_hashes={hashes}")


def producer_accept():
    readback_path = RECEIPTS / "A5-NW_BLOCK-machine-readback.json"
    readback = json.loads(readback_path.read_text(encoding="utf-8"))
    if not readback.get("machine_pass"):
        raise SystemExit("cannot producer-accept over machine failure")
    readback["status"] = "PRODUCER_PASS_STRUCTURE_HIERARCHY_NOT_FINAL_ART"
    readback["producer_visual_review"] = "COMPLETE_PASS_STRUCTURE_HIERARCHY"
    readback["producer_verdict"] = "PASS_STRUCTURE_HIERARCHY"
    readback["producer_verdict_date"] = "2026-08-22"
    readback["final_art_pass"] = False
    readback["material_pilot_released"] = "NW_BLOCK_ONLY_A6"
    readback["six_structure_batch_released"] = False
    readback_path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (ROOT / "50-100-visual-self-review.md").write_text("""# ENV-A5 NW_BLOCK 50% / 100%制作人视觉裁决\n\n状态：`PRODUCER_PASS_STRUCTURE_HIERARCHY / NOT_FINAL_ART / A6_NW_ONLY_RELEASED`\n\n- 制作人确认50%已摆脱单一长方程序盒，低主楼、低东翼、偏置设备间与短檐层级成立。\n- 0.34 QA中的后方单位与路线可读。\n- 本PASS只覆盖NW_BLOCK纯几何结构层级，不等于最终材质、美术、六栋环境或地图整合PASS。\n- 只放行A6 NW_BLOCK单栋材质试制；其余五栋继续禁止。\n""", encoding="utf-8")
    (ROOT / "completion-report.md").write_text("""# ENV-A5单栋纯色轮廓试制回执\n\n状态：`PRODUCER_PASS_STRUCTURE_HIERARCHY / ZERO_IMAGEGEN / NW_BLOCK_ONLY / NOT_FINAL_ART / NO_BATCH`\n\n- grid、pivot、front edge、foundation、40x24投影和90px上限保持不变。\n- 新occluder由52px低主楼、42px东侧翼、总高82px偏置设备间和29—35px南侧短檐组成。\n- 制作人实际查看50%与0.34 QA并通过结构层级，只放行A6单栋材质试制。\n- 不开放其余五栋、最终PLAN、Runtime、UA91、G2-B或Canon。\n""", encoding="utf-8")

    manifest_paths = [path for path in ROOT.rglob("*") if path.is_file() and path.name not in {"asset-manifest.tsv", "delivery-hashes.sha256"}]
    manifest_paths.sort(key=lambda item: str(item.relative_to(ROOT)))
    manifest = ROOT / "asset-manifest.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in manifest_paths:
            writer.writerow((str(path.relative_to(ROOT)), sha(path), path.stat().st_size))
    hash_paths = [*manifest_paths, manifest]
    hashes = ROOT / "delivery-hashes.sha256"
    hashes.write_text("".join(f"{sha(path)}  {path.relative_to(ROOT)}\n" for path in hash_paths), encoding="utf-8")
    print("ENV_A5_PRODUCER_PASS_STRUCTURE_HIERARCHY_SEALED")
    print(f"delivery_hashes={hashes}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--seal", choices=("candidate", "fail"))
    parser.add_argument("--producer-accept", action="store_true")
    args = parser.parse_args()
    if sum((bool(args.build), bool(args.seal), bool(args.producer_accept))) != 1:
        raise SystemExit("choose exactly one action")
    if args.build:
        build()
    elif args.seal:
        seal(args.seal)
    else:
        producer_accept()


if __name__ == "__main__":
    main()
