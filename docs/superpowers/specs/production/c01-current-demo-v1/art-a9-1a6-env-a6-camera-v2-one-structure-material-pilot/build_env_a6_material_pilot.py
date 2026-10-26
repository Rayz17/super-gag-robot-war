#!/usr/bin/env python3
"""Build ENV-A6 NW_BLOCK material pilot over the producer-passed A5 alpha."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = Path(__file__).resolve().parents[6]
C01 = ROOT.parent
A5 = C01 / "art-a9-1a6-env-a5-camera-v2-one-structure-enrichment"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REGISTRATION = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
OBJECTIVE = ROOT / "A6-one-structure-material-pilot-objective.md"

SOURCE_FOUNDATION = A5 / "delivery/NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png"
SOURCE_OCCLUDER = A5 / "delivery/NW_BLOCK_OCCLUDER_CAMERA_V2_ENRICHED_RGBA.png"

DELIVERY = ROOT / "delivery"
QA = ROOT / "qa"
RECEIPTS = ROOT / "receipts"
for directory in (DELIVERY, QA, RECEIPTS):
    directory.mkdir(parents=True, exist_ok=True)

FOUNDATION_OUT = DELIVERY / "NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png"
OCCLUDER_OUT = DELIVERY / "NW_BLOCK_OCCLUDER_CAMERA_V2_MATERIAL_RGBA.png"

GRID_RECT = [1, 0, 7, 5]
BOUNDS_RAW = [-160, -90, 480, 378]
CANVAS = [480, 378]
PIVOT = [240, 378]
FRONT_EDGE = [80, 288]
HEIGHT_LIMIT = 90
AUTHORED_HEIGHT = 82
SCALE = 4

VOLUMES = {
    "main": ((0.90, -0.10, 5.15, 4.05), 0, 52),
    "east_wing": ((4.72, 0.72, 6.92, 3.16), 0, 42),
    "equipment": ((1.55, 0.30, 3.35, 1.75), 52, 82),
    "eave": ((1.78, 3.73, 4.08, 4.34), 29, 35),
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


def project(x, y, z=0.0):
    return (x - y) * 40 - BOUNDS_RAW[0], (x + y) * 24 - BOUNDS_RAW[1] - z


def corners(rect, z):
    x0, y0, x1, y1 = rect
    return [project(x0, y0, z), project(x1, y0, z), project(x1, y1, z), project(x0, y1, z)]


def mask_polygon(points):
    image = Image.new("L", (CANVAS[0] * SCALE, CANVAS[1] * SCALE), 0)
    ImageDraw.Draw(image).polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=255)
    return image.resize(tuple(CANVAS), Image.Resampling.LANCZOS)


def volume_masks(rect, z0, z1, alpha):
    a, b, c, d = corners(rect, z0)
    at, bt, ct, dt = corners(rect, z1)
    return {
        "roof": ImageChops.multiply(mask_polygon([at, bt, ct, dt]), alpha),
        "east": ImageChops.multiply(mask_polygon([bt, ct, c, b]), alpha),
        "south": ImageChops.multiply(mask_polygon([dt, ct, c, d]), alpha),
    }


def value_field(size, color, seed, amplitude=7, coarse=58):
    rng = random.Random(seed)
    width = max(3, math.ceil(size[0] / coarse) + 2)
    height = max(3, math.ceil(size[1] / coarse) + 2)
    grid = Image.new("L", (width, height))
    grid.putdata([128 + rng.randint(-amplitude, amplitude) for _ in range(width * height)])
    noise = grid.resize(size, Image.Resampling.BICUBIC)
    base = Image.new("RGB", size, color)
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return ImageChops.add(base, noise_rgb, scale=1.0, offset=-128)


def paint_field(canvas, mask, color, seed, amplitude=7):
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


def face_south(x0, x1, y, z0, z1):
    return [project(x0, y, z1), project(x1, y, z1), project(x1, y, z0), project(x0, y, z0)]


def face_east(x, y0, y1, z0, z1):
    return [project(x, y0, z1), project(x, y1, z1), project(x, y1, z0), project(x, y0, z0)]


def draw_material_details(alpha):
    overlay = Image.new("RGBA", (CANVAS[0] * SCALE, CANVAS[1] * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    edge = "#0b2028"
    seam = "#688188"

    # Exact volume outlines, subdued rather than black program-linework.
    for rect, z0, z1 in VOLUMES.values():
        base = corners(rect, z0)
        top = corners(rect, z1)
        line(draw, top + [top[0]], edge, 2)
        _, b, c, d = base
        _, bt, ct, dt = top
        line(draw, [bt, b, c, ct], edge, 2)
        line(draw, [dt, d, c, ct], edge, 2)

    # Main waterproof membrane inset and two broad exact-axis seams.
    membrane = corners((1.08, 0.08, 4.96, 3.82), 52)
    poly(draw, membrane, (54, 82, 89, 210), seam, 1)
    line(draw, [project(2.35, 0.08, 52), project(2.35, 3.82, 52)], "#587078", 1)
    line(draw, [project(3.72, 0.08, 52), project(3.72, 3.82, 52)], "#273f48", 1)

    # One exact-axis roof drainage strip and two drain caps.
    drain = corners((1.12, 3.56, 4.76, 3.79), 52)
    poly(draw, drain, "#1b343d", "#577079", 1)
    for x in (1.52, 4.28):
        cap = corners((x, 3.58, x + 0.24, 3.76), 52.2)
        poly(draw, cap, "#0f272f", "#70878c", 1)

    # Main south facade: one large window band, entrance under the short eave.
    band = face_south(1.12, 4.72, 4.052, 15, 31)
    poly(draw, band, "#102832", "#395964", 1)
    for x0, x1 in ((1.22, 2.10), (2.20, 3.08), (3.18, 4.06), (4.16, 4.61)):
        window = face_south(x0, x1, 4.054, 18, 29)
        poly(draw, window, "#284c58", "#54727a", 1)
    entrance = face_south(2.34, 3.08, 4.058, 2, 29)
    poly(draw, entrance, "#11242c", "#6c7f83", 1)
    inner = face_south(2.46, 2.96, 4.060, 3, 24)
    poly(draw, inner, "#25343a", "#9a6534", 1)

    # East wing service panel: broad value block, no dense grid.
    service = face_east(6.922, 1.02, 2.86, 8, 29)
    poly(draw, service, "#132b34", "#47636b", 1)
    line(draw, [project(6.924, 1.94, 29), project(6.924, 1.94, 8)], "#587078", 1)

    # Equipment-room broad louver panel and three exact-axis slats.
    louver = face_south(1.74, 3.15, 1.752, 59, 74)
    poly(draw, louver, "#1b333b", "#60757a", 1)
    for z in (63, 67, 71):
        line(draw, [project(1.82, 1.754, z), project(3.07, 1.754, z)], "#6f858a", 1)

    # Three restrained warm edge lights, all vertical and within existing faces.
    for x, y, z0, z1 in ((1.24, 4.061, 6, 13), (4.48, 4.061, 6, 13), (6.925, 2.72, 7, 14)):
        p0 = project(x, y, z0)
        p1 = project(x, y, z1)
        line(draw, [p0, p1], "#d18a3f", 2)

    # Sparse low-frequency vertical rain streaks on visible walls.
    for x, y, top, bottom in (
        (1.52, 4.063, 44, 32), (3.55, 4.063, 45, 34), (4.85, 4.063, 40, 30),
        (6.928, 1.30, 36, 22), (6.928, 2.48, 34, 20), (3.24, 1.756, 78, 74),
    ):
        line(draw, [project(x, y, top), project(x, y, bottom)], (145, 170, 175, 44), 2)

    overlay = overlay.resize(tuple(CANVAS), Image.Resampling.LANCZOS)
    overlay.putalpha(ImageChops.multiply(overlay.getchannel("A"), alpha))
    return overlay


def materialize(source):
    alpha = source.getchannel("A")
    result_rgb = Image.new("RGB", tuple(CANVAS), "#152b34")
    masks = {name: volume_masks(*spec, alpha) for name, spec in VOLUMES.items()}

    palette = {
        "main": {"roof": (54, 82, 89), "east": (35, 60, 69), "south": (28, 48, 57)},
        "east_wing": {"roof": (48, 74, 82), "east": (29, 52, 61), "south": (24, 43, 51)},
        "equipment": {"roof": (83, 108, 114), "east": (52, 76, 83), "south": (43, 64, 71)},
        "eave": {"roof": (95, 119, 124), "east": (58, 80, 86), "south": (43, 62, 69)},
    }
    order = ("main", "east_wing", "equipment", "eave")
    for index, name in enumerate(order):
        for face_index, face in enumerate(("east", "south", "roof")):
            paint_field(result_rgb, masks[name][face], palette[name][face], 6100 + index * 101 + face_index * 17, amplitude=7 if face == "roof" else 5)

    result = result_rgb.convert("RGBA")
    result.putalpha(alpha.copy())
    result.alpha_composite(draw_material_details(alpha))
    result.putalpha(alpha.copy())
    # Transparent RGB is normalized without changing alpha.
    pixels = result.load()
    for y in range(result.height):
        for x in range(result.width):
            if pixels[x, y][3] == 0:
                pixels[x, y] = (0, 0, 0, 0)
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


def comparison_board(foundation, old_occluder, new_occluder):
    old = combined(foundation, old_occluder)
    new = combined(foundation, new_occluder)
    board = checker((1120, 620))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1120, 82), fill="#071219")
    draw.text((24, 15), "NW_BLOCK | A6 LOCKED-ALPHA MATERIAL PILOT", font=font(27, True), fill="#eff7f8")
    draw.text((24, 50), "A5 silhouette unchanged | 4-7 value blocks | exact-axis architecture | no donor pixels", font=font(16), fill="#8fc7d0")
    for index, (label, asset) in enumerate((("A5 PURE GEOMETRY", old), ("A6 MATERIAL", new))):
        x0 = 35 + index * 545
        draw.text((x0, 95), label, font=font(19, True), fill="#e0edef")
        shown = fit(asset, 500, 420)
        board.alpha_composite(shown, (x0 + (500 - shown.width) // 2, 140 + (410 - shown.height) // 2))
    path100 = QA / "NW_BLOCK_A6_MATERIAL_COMPARISON_100_PERCENT_1120x620.png"
    path50 = QA / "NW_BLOCK_A6_MATERIAL_COMPARISON_50_PERCENT_560x310.png"
    board.save(path100)
    board.resize((560, 310), Image.Resampling.LANCZOS).save(path50)
    return path100, path50


def map_proxy():
    image = Image.new("RGBA", tuple(CANVAS), "#14252c")
    draw = ImageDraw.Draw(image)
    # Exact 40x24 tactical grid proxy.
    for gx in range(-2, 11):
        line_points = [project(gx, -2, 0), project(gx, 8, 0)]
        draw.line(line_points, fill=(45, 78, 87, 130), width=1)
    for gy in range(-2, 9):
        line_points = [project(-2, gy, 0), project(11, gy, 0)]
        draw.line(line_points, fill=(45, 78, 87, 130), width=1)
    return image


def unit_route_proxy():
    image = Image.new("RGBA", tuple(CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Route and generic unit proxy, QA only. It composites above foundation and
    # below occluder, matching the focus-reveal responsibility split.
    route = [(92, 286), (172, 238), (252, 286), (332, 238), (412, 286)]
    draw.line(route, fill=(28, 219, 232, 235), width=5, joint="curve")
    for x, y in route:
        draw.polygon([(x, y - 7), (x + 12, y), (x, y + 7), (x - 12, y)], fill=(25, 222, 235, 235), outline=(201, 251, 255, 255))
    cx, cy = 255, 228
    draw.ellipse((cx - 17, cy - 23, cx + 17, cy + 11), fill=(25, 215, 228, 255), outline=(218, 255, 255, 255), width=2)
    draw.rectangle((cx - 10, cy - 40, cx + 10, cy - 18), fill=(36, 229, 240, 255), outline=(218, 255, 255, 255), width=2)
    draw.line((cx - 10, cy + 7, cx - 20, cy + 28), fill=(218, 255, 255, 255), width=4)
    draw.line((cx + 10, cy + 7, cx + 20, cy + 28), fill=(218, 255, 255, 255), width=4)
    return image


def proxy_board(foundation, occluder):
    background = map_proxy()
    proxy = unit_route_proxy()
    frames = []
    for factor in (1.0, 0.34):
        frame = background.copy()
        frame.alpha_composite(foundation)
        frame.alpha_composite(proxy)
        frame.alpha_composite(alpha_scaled(occluder, factor))
        frames.append(frame)
    board = Image.new("RGBA", (1120, 620), "#071219")
    draw = ImageDraw.Draw(board)
    draw.text((24, 15), "NW_BLOCK A6 | MAP PROXY NORMAL / REVEAL 0.34", font=font(27, True), fill="#eff7f8")
    draw.text((24, 50), "proxy grid, route and unit are QA-only; delivery assets remain isolated", font=font(16), fill="#8fc7d0")
    for index, (label, asset) in enumerate((("NORMAL 1.00", frames[0]), ("REVEAL 0.34", frames[1]))):
        x0 = 35 + index * 545
        draw.text((x0, 95), label, font=font(20, True), fill="#e0edef")
        shown = fit(asset, 500, 420)
        board.alpha_composite(shown, (x0 + (500 - shown.width) // 2, 140 + (410 - shown.height) // 2))
    path = QA / "NW_BLOCK_A6_MAP_PROXY_NORMAL_REVEAL_1120x620.png"
    board.save(path)
    return path


def write_lineage():
    sources = [
        ("A6_OBJECTIVE", OBJECTIVE, "task_scope", "none"),
        ("CAMERA_V2", CAMERA, "exact_projection_authority", "geometry_only"),
        ("REGISTRATION", REGISTRATION, "grid_pivot_front_edge_envelope_authority", "geometry_only"),
        ("A5_FOUNDATION", SOURCE_FOUNDATION, "byte_locked_foundation", "copied_byte_for_byte"),
        ("A5_OCCLUDER", SOURCE_OCCLUDER, "alpha_and_silhouette_authority", "alpha_copied_pixel_for_pixel_rgb_replaced"),
    ]
    path = ROOT / "source-lineage.tsv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source_id", "path", "sha256", "role", "visible_pixel_use"))
        for source_id, source, role, use in sources:
            writer.writerow((source_id, str(source.relative_to(PROJECT)), sha(source), role, use))
    return path


def write_readback(foundation, source_occluder, output_occluder, outputs):
    source_foundation = Image.open(SOURCE_FOUNDATION).convert("RGBA")
    alpha_locked = source_occluder.getchannel("A").tobytes() == output_occluder.getchannel("A").tobytes()
    foundation_locked = source_foundation.tobytes() == foundation.tobytes()
    readback = {
        "task_id": "A9_1A6_ENV_A6_CAMERA_V2_ONE_STRUCTURE_MATERIAL_PILOT",
        "status": "MACHINE_PASS_PRODUCER_VISUAL_REVIEW_PENDING",
        "scope": "NW_BLOCK_ONLY_NO_BATCH",
        "upstream_producer_verdict": "A5_PASS_STRUCTURE_HIERARCHY_NOT_FINAL_ART",
        "registration": {
            "grid_rect": GRID_RECT,
            "local_canvas_px": CANVAS,
            "pivot_local_px": PIVOT,
            "front_edge_raw": FRONT_EDGE,
            "visual_bounds_raw": BOUNDS_RAW,
            "world_height_limit_px": HEIGHT_LIMIT,
            "authored_max_height_px": AUTHORED_HEIGHT,
        },
        "camera": {
            "axis_vectors_px": [[40, 24], [-40, 24]],
            "axis_angles_deg": [30.9637565, -30.9637565],
            "allowed_structural_line_families": ["+30.9637565_deg", "-30.9637565_deg", "vertical"],
            "manual_screen_offset": False,
        },
        "foundation": {
            "source_sha256": sha(SOURCE_FOUNDATION),
            "output_sha256": sha(FOUNDATION_OUT),
            "byte_identical": foundation_locked,
        },
        "occluder": {
            "source_sha256": sha(SOURCE_OCCLUDER),
            "output_sha256": sha(OCCLUDER_OUT),
            "source_alpha_sha256": alpha_sha(source_occluder),
            "output_alpha_sha256": alpha_sha(output_occluder),
            "alpha_pixel_identical": alpha_locked,
            "alpha_bbox_local": list(output_occluder.getchannel("A").getbbox()),
            "normal_alpha": 1.0,
            "reveal_alpha": 0.34,
        },
        "material_blocks": [
            "main_waterproof_roof", "main_window_facade", "east_service_wing", "offset_equipment_room",
            "short_eave_and_entrance", "foundation", "restrained_amber_edges",
        ],
        "material_features": ["roof_drain_strip", "continuous_window_band", "entrance", "equipment_louver", "three_warm_edge_lights", "low_frequency_rain_wear"],
        "old_donor_pixels_used": False,
        "imagegen_calls": 0,
        "dynamic_lighting": False,
        "shader": False,
        "subviewport": False,
        "outputs": [str(path.relative_to(ROOT)) for path in outputs],
        "machine_pass": bool(alpha_locked and foundation_locked and AUTHORED_HEIGHT <= HEIGHT_LIMIT),
        "producer_visual_review": "PENDING",
        "six_structure_batch_released": False,
    }
    path = RECEIPTS / "A6-NW_BLOCK-machine-readback.json"
    path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def build():
    shutil.copyfile(SOURCE_FOUNDATION, FOUNDATION_OUT)
    foundation = Image.open(FOUNDATION_OUT).convert("RGBA")
    source_occluder = Image.open(SOURCE_OCCLUDER).convert("RGBA")
    output_occluder = materialize(source_occluder)
    assert output_occluder.getchannel("A").tobytes() == source_occluder.getchannel("A").tobytes()
    output_occluder.save(OCCLUDER_OUT)
    comparison100, comparison50 = comparison_board(foundation, source_occluder, output_occluder)
    proxy = proxy_board(foundation, output_occluder)
    lineage = write_lineage()
    outputs = [FOUNDATION_OUT, OCCLUDER_OUT, comparison100, comparison50, proxy, lineage]
    readback = write_readback(foundation, source_occluder, output_occluder, outputs)
    print("ENV_A6_NW_BLOCK_MACHINE_BUILD_OK")
    print(f"comparison_50={comparison50}")
    print(f"map_proxy={proxy}")
    print(f"readback={readback}")
    print("producer_visual_review=PENDING")
    print("six_structure_batch_released=false")


def seal(verdict):
    readback_path = RECEIPTS / "A6-NW_BLOCK-machine-readback.json"
    readback = json.loads(readback_path.read_text(encoding="utf-8"))
    if not readback.get("machine_pass"):
        raise SystemExit("cannot seal visual verdict over machine failure")
    candidate = verdict == "candidate"
    readback["status"] = "PASS_CANDIDATE_FOR_PRODUCER_VISUAL_REVIEW" if candidate else "FAIL_FINAL_QUALITY_STOPPED"
    readback["visual_self_review"] = verdict.upper()
    readback["task_stopped"] = not candidate
    readback_path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review = ROOT / "50-100-visual-self-review.md"
    if candidate:
        review.write_text("""# ENV-A6 NW_BLOCK 50% / 100%目视自审\n\n状态：`PASS_CANDIDATE_FOR_PRODUCER_VISUAL_REVIEW / NOT_PRODUCER_ACCEPTED / NO_BATCH`\n\n- 50%：A5四段结构层级仍是第一读法；屋顶、窗带、东翼、设备间、入口与foundation形成7个克制色值块，不靠高频噪声。\n- 100%：防水层、排水带、连续窗带、入口、设备间宽百叶与三处暖色边灯均在A5 Alpha内；线条仅沿Camera V2 exact轴或竖直。\n- 0.34：地图Proxy中的后方单位与路线清楚可读；Proxy未进入交付资产。\n- 边界：只提交NW_BLOCK单栋制作人目视，不开放其余五栋或地图整合。\n""", encoding="utf-8")
    else:
        review.write_text("""# ENV-A6 NW_BLOCK 50% / 100%目视自审\n\n状态：`FAIL_FINAL_QUALITY / STOPPED`\n\n50%仍先读作程序模型或材质压过体块；按任务书停止，不扩六栋。\n""", encoding="utf-8")
    report = ROOT / "completion-report.md"
    report.write_text(f"""# ENV-A6 NW_BLOCK单栋材质试制回执\n\n状态：`{'PASS_CANDIDATE_FOR_PRODUCER_VISUAL_REVIEW' if candidate else 'FAIL_FINAL_QUALITY_STOPPED'} / ZERO_IMAGEGEN / A5_ALPHA_LOCKED / NO_BATCH`\n\n- foundation与A5逐字一致，occluder Alpha逐像素一致；只重做既有面内RGB。\n- 交付100%/50% A5-A6对照、地图Proxy normal/reveal 0.34与机器readback。\n- 制作人视觉审查仍为PENDING；不开放其余五栋、最终PLAN、Runtime、UA91、G2-B或Canon。\n""", encoding="utf-8")

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
    print(f"ENV_A6_SEALED_{verdict.upper()}")


def producer_accept():
    readback_path = RECEIPTS / "A6-NW_BLOCK-machine-readback.json"
    readback = json.loads(readback_path.read_text(encoding="utf-8"))
    if not readback.get("machine_pass"):
        raise SystemExit("cannot producer-accept over machine failure")
    readback["status"] = "PRODUCER_PASS_ASSET_METHOD_CANDIDATE_NOT_FINAL_PLAN"
    readback["producer_visual_review"] = "COMPLETE_PASS_ASSET_METHOD_CANDIDATE"
    readback["producer_verdict"] = "PASS_ASSET_METHOD_CANDIDATE"
    readback["producer_verdict_date"] = "2026-08-22"
    readback["final_plan_pass"] = False
    readback["a7_six_structure_asset_pack_released"] = True
    readback["six_structure_batch_released"] = "A7_ASSET_PACK_ONLY"
    readback_path.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (ROOT / "50-100-visual-self-review.md").write_text("""# ENV-A6 NW_BLOCK 50% / 100%制作人视觉裁决\n\n状态：`PRODUCER_PASS_ASSET_METHOD_CANDIDATE / NOT_FINAL_PLAN / A7_ASSET_PACK_RELEASED`\n\n- 制作人独立确认A6的50%材质、建筑读法与0.34地图Proxy达到可复用单栋资产方法Candidate。\n- A5 Alpha、foundation、grid、pivot、front edge和Camera V2保持锁定。\n- 本PASS只放行A7六栋独立Structure资产包，不等于最终PLAN、整图环境、Runtime或最终美术验收。\n""", encoding="utf-8")
    (ROOT / "completion-report.md").write_text("""# ENV-A6 NW_BLOCK单栋材质试制回执\n\n状态：`PRODUCER_PASS_ASSET_METHOD_CANDIDATE / ZERO_IMAGEGEN / A5_ALPHA_LOCKED / NOT_FINAL_PLAN`\n\n- foundation与A5逐字一致，occluder Alpha逐像素一致；只重做既有面内RGB。\n- 制作人实际查看50%/100%与地图Proxy 0.34并通过资产方法Candidate。\n- 只开放A7六栋独立Structure包；最终PLAN、Runtime、UA91、G2-B和Canon仍禁止。\n""", encoding="utf-8")

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
    print("ENV_A6_PRODUCER_PASS_ASSET_METHOD_CANDIDATE_SEALED")
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
