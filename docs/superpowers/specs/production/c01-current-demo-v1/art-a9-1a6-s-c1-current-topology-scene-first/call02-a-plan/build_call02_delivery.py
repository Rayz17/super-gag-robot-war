#!/usr/bin/env python3
"""Build Task95 Call02 deterministic diagnostic delivery.

This script never draws or edits a physical actor, map object, or environment.
It performs the permitted one-time crop/resize of the single Call02 raw image,
then adds separable screen UI, route, ghost, edge-cue, and review overlays.
"""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/rayz/Documents/超gag机器人大战")
BASE = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c1-current-topology-scene-first/call02-a-plan"
RAW = BASE / "generation-raw/CALL02_A_PLAN_RAW.png"
DELIVERY = BASE / "delivery"
LAYERS = BASE / "layers"
RECEIPTS = BASE / "receipts"
REVIEW = BASE / "review"

EXPECTED_RAW_SHA = "98f30a9797591204f702ad1b36aaad1042c2cece1fd35a088b44d828f9e156d5"
RAW_CROP = (4, 2, 1668, 938)  # exact 1664x936 = 16:9
CANVAS = (1280, 720)
MAP_CENTER = (640.0, 350.0)
RAW_ORIGIN = (-880.0, -170.0)
CAMERA = (-480.0, 420.0)
TILE_HALF = (40.0, 20.0)

INPUTS = [
    {
        "role": "exact_current_topology_plan_raster_guide",
        "path": ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c1/captures/02_EDITABLE_DRAFT_A.png",
        "sha256": "2bd9fa53a575ddafcc0c63a7557924d1fc5bb509a2b42966ae08bc0da5708fe1",
    },
    {
        "role": "safe_identity_style_board",
        "path": ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c1-current-topology-scene-first/identity-style-safe-board.png",
        "sha256": "dc473235883669165e0eef58ce8c9d390e719e946e133648893b7d0ca83f3276",
    },
    {
        "role": "map_language_donor_only",
        "path": ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c1-current-topology-scene-first/map-language-board.png",
        "sha256": "4776660f7ab282f1434286e6670f080256b56a3208f2f5a0d13b754b78797819",
    },
    {
        "role": "a5_swarm_camera_identity",
        "path": ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png",
        "sha256": "1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b",
    },
]

PROMPT = """Use case: stylized-concept
Asset type: NON-SEPARABLE CANDIDATE game whole-screen PLAN physical cleanplate, 16:9 landscape
Primary request: Transform Image 1's exact current-topology proxy composition into one polished KINETIC_CEL tactical-map physical cleanplate. This is the shared current physical PLAN state before any contact. Preserve Image 1's camera, crop, 2:1 orthographic dimetric projection, every ground anchor, footprint, actor count, object placement, depth order, road/block geometry, and open selection pocket. Remove every UI or planning overlay from Image 1.

Input image roles, strict priority:
Image 1: ABSOLUTE geometry guide only. Copy camera, crop, approximately 45-degree azimuth and 30-degree elevation, parallel 2:1 dimetric projection with no perspective convergence, roads, blocks, current object positions, actor footpoints, footprints, depth and occlusion. IGNORE its proxy anatomy, colors, text, UI, route, ghosts, labels, footprint boxes, arrows, protection-zone overlay and debug marks.
Image 2: identity and style reference only. Guardian Z uses only the upper-left V10X identity. BREAKER uses only the upper-right B body plus lower-left X surface relation. Lower-right CML128 cells are STYLE ONLY: ignore any depicted anatomy. Absolutely no wings and no backpack.
Image 3: legacy A4 MATERIAL LANGUAGE DONOR ONLY: cool dark values, rainy wet ground, building-plane separation, roof-edge light, and local occlusion method. Do not copy any old topology, old shield, old exit, old facility, old rescue-line semantics, labels or board layout.
Image 4: the sole Rift Swarm camera/identity reference. Exactly three small swarm bodies in the positions and facings from Image 1; do not add more.

Scene/backdrop: current 32x18 urban tactical space at blue-gray rainy night. Wet concrete and road surfaces, controlled reflections, layered industrial buildings and selective roof cutouts. East gate at the far right is the main landmark with restrained cyan safe reflection. West broken wall and wall-mounted retired shield are secondary landmarks. Security facility stays at right-center. City artillery source remains offscreen and has no cue. The central selection pocket and five-cell load-bearing avenue between Guardian Z and BREAKER stay visually open and unobstructed.

Subjects and exact current-state relationships:
- Guardian Z at the left-of-center current footpoint exactly as Image 1, 2x2 footprint, facing east/lower-right, standing ready but not moving or colliding. 18 m, about four heads tall, old super-robot weight; two arms; no wings; no backpack. Preserve V10X: layered gold crown with central red crown and blue forehead helmet, dignified silver grille face, red X chest armor with round gold core, broad square shoulder rings, equal-weight cylindrical forearms, blue/red/white/gold masses.
- BREAKER at the lower-middle current footpoint exactly as Image 1, 3x3 footprint, facing north/upper-right, charge-ready but still in PLAN and not contacting Guardian Z. Nearly 30 m black intrusion shell. Preserve B body plus X surface: huge high back shell pressing over the torso, very low embedded head with one narrow red slit, load-bearing semi-upright front limbs, short rear stabilizer feet, asymmetric alien bio-armor plates and flexible seams forming one continuous stress path, closed chest seam, sealed upper-back core outlet. First read must NOT be ape, ordinary quadruped, turtle, armored car or sled.
- One emergency vehicle at Image 1's exact current point, facing east/lower-right.
- Exactly three small Rift Swarm units at Image 1's three exact points: Swarm 01 west/upper-left facing, Swarm 02 north/upper-right facing, Swarm 03 south/lower-left facing. They act independently, not in formation.
- Keep the retired shield wall-mounted and not acquired; keep east gate, security facility and current protection-zone physical architecture at their exact places. Do not turn the transparent protection overlay from Image 1 into a physical wall or glowing polygon.

Style/medium: finished Japanese KINETIC_CEL game lookdev, clean pressure-sensitive deep ink-blue linework, 4-7 large color masses per major subject, no more than two levels of hard cel shadow, readable material facets, restrained local wear, controlled rain streaks and wet reflections. Strong tactical readability at 50%, credible limb construction and armor at 100%. Not photorealistic, not flat low-poly, not generic 3D, not painterly fog that hides geometry.

Composition/framing: exact Image 1 spatial registration and camera. Full-bleed 16:9 cleanplate with safe top and bottom areas for later deterministic UI. Keep all current actors physically separated at their guide footpoints. Roofs may locally fade or cut away only where needed; never globally fade buildings. Preserve shared ground shadows and footpoint-y depth sorting.

Lighting/mood: cool medium-low-value rainy night. Cyan east-gate safety direction and BREAKER's narrow red threat slit are distinct. Guardian Z's chest core and primary color blocks read clearly against the wet ground.

Constraints: NO text, NO pseudo-text, NO letters, NO numbers, NO UI, NO communication portrait, NO route line, NO route nodes, NO ghost, NO footprint outline, NO facing fan, NO arrows, NO labels, NO debug grid, NO edge cue, NO forecast graphics. No T3 impact, crack, debris, splash or recoil. No T4 artillery beam/projectile/source. No T5 red charge or complete road buckle. No future/post state. No redesign, no extra actor, no extra swarm, no duplicate mecha, no identity mixing, no winged red mecha, no wings, no backpack, no watermark."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=False, compress_level=9)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("/System/Library/Fonts/STHeiti Medium.ttc") if bold else Path("/System/Library/Fonts/STHeiti Light.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size, index=0)
    return ImageFont.load_default()


def grid_center(grid: tuple[float, float]) -> tuple[float, float]:
    x, y = grid
    raw_x = RAW_ORIGIN[0] + (x - y) * TILE_HALF[0]
    raw_y = RAW_ORIGIN[1] + (x + y) * TILE_HALF[1]
    return (MAP_CENTER[0] + raw_x - CAMERA[0], MAP_CENTER[1] + raw_y - CAMERA[1])


def footprint_bottom_center(anchor: tuple[float, float], footprint: tuple[int, int]) -> tuple[float, float]:
    ax, ay = anchor
    w, h = footprint
    points = [grid_center((ax + dx, ay + dy)) for dx in range(w) for dy in range(h)]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return ((min(xs) + max(xs)) / 2.0, max(ys) + TILE_HALF[1])


def footprint_polygon(anchor: tuple[int, int], footprint: tuple[int, int]) -> list[tuple[float, float]]:
    ax, ay = anchor
    w, h = footprint
    top = grid_center((ax, ay))
    east = grid_center((ax + w - 1, ay))
    bottom = grid_center((ax + w - 1, ay + h - 1))
    south = grid_center((ax, ay + h - 1))
    return [
        (top[0], top[1] - TILE_HALF[1]),
        (east[0] + TILE_HALF[0], east[1]),
        (bottom[0], bottom[1] + TILE_HALF[1]),
        (south[0] - TILE_HALF[0], south[1]),
    ]


def dashed_line(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: tuple[int, int, int, int], width: int = 3, dash: float = 11.0, gap: float = 7.0) -> None:
    for start, end in zip(points, points[1:]):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)
        if not length:
            continue
        position = 0.0
        while position < length:
            stop = min(position + dash, length)
            p0 = (start[0] + dx * position / length, start[1] + dy * position / length)
            p1 = (start[0] + dx * stop / length, start[1] + dy * stop / length)
            draw.line((p0, p1), fill=fill, width=width)
            position += dash + gap


def arrow_head(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], fill: tuple[int, int, int, int], size: float = 11.0) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy) or 1.0
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    back_x, back_y = end[0] - ux * size, end[1] - uy * size
    draw.polygon(
        [end, (back_x + px * size * 0.55, back_y + py * size * 0.55), (back_x - px * size * 0.55, back_y - py * size * 0.55)],
        fill=fill,
    )


def pill(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color: tuple[int, int, int, int]) -> None:
    x, y = xy
    f = font(13, True)
    box = draw.textbbox((0, 0), text, font=f)
    w = box[2] - box[0] + 20
    draw.rounded_rectangle((x, y, x + w, y + 25), radius=8, fill=(4, 18, 26, 220), outline=color, width=1)
    draw.text((x + 10, y + 5), text, font=f, fill=color)


def build_cleanplate() -> Image.Image:
    if not RAW.is_file() or sha256(RAW) != EXPECTED_RAW_SHA:
        raise SystemExit("Call02 raw missing or SHA mismatch")
    raw = Image.open(RAW)
    if raw.size != (1672, 941):
        raise SystemExit(f"unexpected raw dimensions: {raw.size}")
    clean = raw.convert("RGB").crop(RAW_CROP)
    if clean.size != (1664, 936):
        raise SystemExit("deterministic 16:9 crop failed")
    clean = clean.resize(CANVAS, Image.Resampling.LANCZOS)
    save_png(clean, DELIVERY / "PLAN_SHARED_CURRENT_PHYSICAL_CLEANPLATE_1280x720.png")
    return clean


def build_route_layer() -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    cyan = (76, 233, 230, 230)
    amber = (255, 177, 69, 224)
    orange = (255, 119, 66, 224)
    red = (255, 66, 93, 225)

    zone = footprint_polygon((20, 5), (12, 7))
    draw.polygon(zone, fill=(34, 187, 194, 22))
    draw.line(zone + [zone[0]], fill=(66, 206, 208, 80), width=2)

    a_route = [(15, 11), (15, 10), (15, 9), (16, 9), (17, 9), (18, 9), (19, 9), (20, 9)]
    a_points = [footprint_bottom_center(point, (2, 2)) for point in a_route]
    draw.line(a_points, fill=(1, 8, 12, 220), width=10, joint="curve")
    draw.line(a_points, fill=cyan, width=5, joint="curve")
    for index, point in enumerate(a_points):
        radius = 7 if index in (0, len(a_points) - 1) else 5
        draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), fill=(8, 27, 35, 245), outline=cyan, width=2)
    arrow_head(draw, a_points[-2], a_points[-1], cyan, 14)
    pill(draw, (430, 235), "当前草稿·方案甲", cyan)

    trajectories = [
        ([(17, 10), (18, 10), (21, 10), (24, 9)], (1, 1), amber, "应急车"),
        ([(22, 7), (21, 8), (20, 9), (20, 10)], (1, 1), orange, "小体"),
        ([(20, 13), (20, 12), (20, 11)], (3, 3), red, "破城者"),
    ]
    label_offsets = [(12, -24), (10, -20), (-78, 12)]
    for (route, footprint, color, label), offset in zip(trajectories, label_offsets):
        points = [footprint_bottom_center(point, footprint) for point in route]
        dashed_line(draw, points, color, width=3)
        arrow_head(draw, points[-2], points[-1], color, 10)
        end = points[-1]
        draw.text((end[0] + offset[0], end[1] + offset[1]), label, font=font(13, True), fill=color)

    save_png(image, LAYERS / "ROUTE_ONLY_1280x720.png")
    return image


def build_ghost_layer() -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    cyan = (78, 239, 233, 235)
    red = (255, 73, 102, 225)

    gz_poly = footprint_polygon((20, 9), (2, 2))
    draw.polygon(gz_poly, fill=(58, 226, 220, 48))
    draw.line(gz_poly + [gz_poly[0]], fill=cyan, width=3)
    gz_foot = footprint_bottom_center((20, 9), (2, 2))
    south = (gz_foot[0] - 32, gz_foot[1] + 16)
    draw.line((gz_foot, south), fill=cyan, width=4)
    arrow_head(draw, gz_foot, south, cyan, 12)
    draw.rounded_rectangle((gz_foot[0] - 60, gz_foot[1] - 56, gz_foot[0] + 55, gz_foot[1] - 30), radius=7, fill=(4, 20, 28, 220), outline=cyan, width=1)
    draw.text((gz_foot[0] - 50, gz_foot[1] - 51), "馆守Z终点", font=font(13, True), fill=cyan)

    bx_poly = footprint_polygon((20, 11), (3, 3))
    draw.polygon(bx_poly, fill=(255, 58, 82, 24))
    dashed_line(draw, bx_poly + [bx_poly[0]], red, width=2, dash=9, gap=6)
    bx_foot = footprint_bottom_center((20, 11), (3, 3))
    draw.rounded_rectangle((bx_foot[0] + 18, bx_foot[1] - 34, bx_foot[0] + 129, bx_foot[1] - 8), radius=7, fill=(28, 8, 16, 220), outline=red, width=1)
    draw.text((bx_foot[0] + 28, bx_foot[1] - 29), "破城者冲线", font=font(13, True), fill=red)

    save_png(image, LAYERS / "GHOST_ONLY_1280x720.png")
    return image


def build_edge_layer() -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    cyan = (96, 225, 224, 210)
    orange = (255, 135, 72, 220)
    amber = (248, 194, 86, 220)

    cues = [
        (454, "小体三", orange),
        (535, "东门", cyan),
        (392, "第四时点炮源", amber),
    ]
    for y, label, color in cues:
        draw.line((1215, y, 1268, y), fill=color, width=2)
        arrow_head(draw, (1248, y), (1272, y), color, 10)
        box = draw.textbbox((0, 0), label, font=font(12, True))
        width = box[2] - box[0] + 16
        draw.rounded_rectangle((1204 - width, y - 12, 1204, y + 12), radius=7, fill=(4, 17, 24, 205), outline=(color[0], color[1], color[2], 130), width=1)
        draw.text((1212 - width, y - 8), label, font=font(12, True), fill=color)

    save_png(image, LAYERS / "EDGE_CUE_ONLY_1280x720.png")
    return image


def build_ui_layer() -> Image.Image:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    panel = (3, 14, 22, 232)
    panel_soft = (4, 20, 29, 218)
    pale = (235, 244, 242, 248)
    quiet = (151, 183, 187, 238)
    cyan = (80, 230, 226, 240)
    amber = (247, 187, 78, 240)

    draw.rectangle((0, 0, 1279, 57), fill=panel)
    draw.line((0, 57, 1279, 57), fill=cyan, width=2)
    draw.text((18, 7), "目标｜让应急车通过，挡开扑向东门的小体，并站到冲线前。", font=font(18, True), fill=pale)
    draw.text((18, 35), "威胁｜应急车先穿过落脚区 · 小体将在第二时点扑向东门 · 破城者沿直线冲入街区", font=font(13), fill=quiet)
    draw.rounded_rectangle((1175, 9, 1262, 47), radius=10, fill=(8, 35, 42, 238), outline=cyan, width=2)
    draw.text((1218, 28), "方案甲", font=font(16, True), fill=cyan, anchor="mm")

    # Strategy comparison remains screen-space and does not alter the world.
    cards = [
        ((848, 72, 1262, 135), cyan, "方案甲｜正面卡位｜本轮热量24｜第二轮热量68、余量1", "警戒设施受损｜道路损伤42"),
        ((848, 143, 1262, 206), amber, "方案乙｜先护撤离线、接触前转身｜本轮热量46", "警戒设施保全｜道路损伤24｜第二轮热量88、余量0"),
    ]
    for index, (rect, color, line1, line2) in enumerate(cards):
        x0, y0, x1, y1 = rect
        draw.rounded_rectangle(rect, radius=10, fill=(5, 19, 27, 220 if index == 0 else 202), outline=color, width=2 if index == 0 else 1)
        draw.text((x0 + 12, y0 + 9), line1, font=font(12, True), fill=pale if index == 0 else quiet)
        draw.text((x0 + 12, y0 + 35), line2, font=font(12), fill=color)

    # PLAN communication, capped below 320 px.
    draw.rounded_rectangle((14, 508, 316, 632), radius=13, fill=panel_soft, outline=(82, 154, 160, 225), width=2)
    draw.rounded_rectangle((27, 522, 82, 580), radius=8, fill=(15, 48, 57, 225), outline=cyan, width=1)
    draw.line((35, 570, 74, 532), fill=(87, 175, 178, 160), width=3)
    draw.text((96, 520), "纪存｜战术通讯", font=font(13, True), fill=cyan)
    draw.text((96, 548), "人都在后面。", font=font(18, True), fill=pale)
    draw.text((96, 577), "把它引到南边去。", font=font(18, True), fill=pale)
    draw.text((27, 607), "当前轮只做路线预示，未发生接触。", font=font(11), fill=quiet)

    draw.rectangle((0, 642, 1279, 719), fill=panel)
    draw.line((0, 642, 1279, 642), fill=cyan, width=2)
    draw.text((18, 670), "五时点", font=font(16, True), fill=pale)
    labels = ["应急车", "小体", "巨体接触", "城市炮", "赤红蓄能"]
    numbers = ["一", "二", "三", "四", "五"]
    centers = [330, 520, 710, 900, 1090]
    draw.line((280, 675, 1140, 675), fill=(78, 116, 123, 220), width=3)
    for index, (label, number, x) in enumerate(zip(labels, numbers, centers)):
        color = cyan if index < 3 else amber
        draw.ellipse((x - 7, 668, x + 7, 682), fill=color, outline=(239, 247, 246, 230), width=1)
        draw.text((x, 653), f"时点{number}", font=font(11, True), fill=color, anchor="mm")
        draw.text((x, 702), label, font=font(14), fill=pale, anchor="mm")
        if index >= 3:
            draw.text((x + 52, 653), "预示", font=font(10, True), fill=amber, anchor="mm")

    product_text = "\n".join([
        "目标 威胁 方案甲 方案乙 纪存 战术通讯",
        "人都在后面 把它引到南边去",
        "应急车 小体 巨体接触 城市炮 赤红蓄能 预示",
    ])
    for banned in ["ROUTE FAMILY", "east", "south", "damaged", "active", "R2", "HUD FORECAST ONLY"]:
        if banned in product_text:
            raise SystemExit(f"banned product term present: {banned}")

    save_png(image, LAYERS / "UI_ONLY_1280x720.png")
    return image


def build_registration_review(clean: Image.Image) -> None:
    image = clean.convert("RGBA")
    debug = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(debug)
    draw.rectangle((0, 0, 1279, 56), fill=(3, 12, 20, 232))
    draw.text((18, 9), "注册诊断｜亮色十字为 1.6.2 预期脚点，不代表生成像素已对齐", font=font(17, True), fill=(235, 242, 241, 255))
    expected = [
        ("馆守Z", (15, 11), (2, 2), (82, 236, 231, 245)),
        ("破城者", (20, 13), (3, 3), (255, 72, 100, 245)),
        ("应急车", (17, 10), (1, 1), (250, 186, 75, 245)),
        ("小体一", (22, 7), (1, 1), (255, 127, 70, 245)),
        ("小体二", (26, 12), (1, 1), (255, 127, 70, 245)),
        ("小体三", (29, 5), (1, 1), (255, 127, 70, 245)),
    ]
    rows = []
    for label, anchor, footprint, color in expected:
        x, y = footprint_bottom_center(anchor, footprint)
        draw.line((x - 10, y, x + 10, y), fill=color, width=3)
        draw.line((x, y - 10, x, y + 10), fill=color, width=3)
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(3, 13, 18, 245), outline=color, width=2)
        draw.text((x + 12, y - 18), label, font=font(12, True), fill=color)
        rows.append((label, anchor, footprint, (x, y)))
    image.alpha_composite(debug)
    save_png(image.convert("RGB"), REVIEW / "EXACT_GUIDE_REGISTRATION_QA_1280x720.png")

    lines = ["entity\tanchor\tfootprint\texpected_footpoint_screen_px\tgenerated_pixel_measurement\tresult"]
    for label, anchor, footprint, point in rows:
        lines.append(f"{label}\t{anchor[0]},{anchor[1]}\t{footprint[0]}x{footprint[1]}\t{point[0]:.0f},{point[1]:.0f}\tnot_machine_segmented\tNOT_PROVEN")
    (BASE / "registration-diagnostic.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_identity_review(clean: Image.Image) -> None:
    board = Image.new("RGB", CANVAS, (4, 12, 18))
    draw = ImageDraw.Draw(board)
    draw.text((34, 25), "Call02 身份原寸诊断｜下图为 cleanplate 100% 像素裁切，未修图", font=font(22, True), fill=(232, 241, 240))

    gz_box = (210, 105, 500, 430)
    bx_box = (350, 250, 730, 600)
    gz = clean.crop(gz_box)
    bx = clean.crop(bx_box)
    board.paste(gz, (38, 105))
    board.paste(bx, (370, 105))
    draw.rectangle((38, 105, 38 + gz.width, 105 + gz.height), outline=(82, 228, 226), width=2)
    draw.rectangle((370, 105, 370 + bx.width, 105 + bx.height), outline=(255, 77, 103), width=2)
    draw.text((38, 446), "馆守Z：通用高比例机战主角读法", font=font(16, True), fill=(82, 228, 226))
    draw.text((38, 474), "V10X、约4头身、旧超级系重量不足。", font=font(15), fill=(188, 211, 212))
    draw.text((370, 474), "破城者：高壳龟状普通四足读法", font=font(16, True), fill=(255, 92, 116))
    draw.text((370, 502), "B前肢承重半直立与X异质生体甲第一读法失效。", font=font(15), fill=(218, 194, 197))

    draw.rounded_rectangle((790, 104, 1244, 590), radius=16, fill=(7, 25, 33), outline=(75, 115, 123), width=2)
    notes = [
        ("制作人结论", (239, 244, 242), True),
        ("CALL02_VISUAL_FAIL_IDENTITY", (255, 94, 116), True),
        ("环境／雨湿／轴测城市完成度强，", (190, 213, 214), False),
        ("只登记为环境与材质画法供体。", (190, 213, 214), False),
        ("不是可修的整屏候选。", (250, 188, 80), True),
        ("不是 Call03 基础。", (250, 188, 80), True),
        ("不得局部修图冒充身份恢复。", (250, 188, 80), True),
    ]
    y = 132
    for text, color, bold in notes:
        draw.text((816, y), text, font=font(16 if bold else 15, bold), fill=color)
        y += 45 if bold else 34
    save_png(board, REVIEW / "CALL02_IDENTITY_100_PERCENT_DIAGNOSTIC_1280x720.png")


def build_documents(cleanplate_path: Path, integrated_path: Path, layer_paths: dict[str, Path]) -> None:
    input_rows = []
    for index, item in enumerate(INPUTS, 1):
        input_rows.append(f"{index}. `{item['path']}`  ")
        input_rows.append(f"   role=`{item['role']}`; sha256=`{item['sha256']}`")

    log = f"""# Task95 Call02 A PLAN generation log

Status: `CALL02_VISUAL_FAIL_IDENTITY / ENVIRONMENT_LOOK_DONOR_ONLY / CALL03=false / CALL04=false`

## Invocation

- tool: built-in `image_gen`
- invocation ordinal: `Call02`
- call started: `2026-08-20T09:46:31.170Z`
- calls made by Task95: `1`
- automatic reroll: `false`
- raw tool output preserved at: `/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-e64bdc9c-d6b8-4885-ac56-5032ec08eac0.png`
- immutable workspace copy: `{RAW}`
- raw dimensions: `1672x941 RGB`
- raw sha256: `{sha256(RAW)}`

## Exact four referenced images

{chr(10).join(input_rows)}

No fifth reference was supplied. Call01, unsafe identity boards, legacy A9/A3, SVG, and Blender assets were not referenced.

## Submitted prompt (verbatim)

```text
{PROMPT}
```

## Deterministic post-process

- one exact center crop: source box `{RAW_CROP}` -> `1664x936` (exact 16:9)
- one LANCZOS resize: `1664x936 -> 1280x720`
- no actor move, patch, redraw, inpaint, local identity repair, or resampling beyond that single scale
- UI, route, ghost, and edge cue are independent transparent layers

## Producer actual-pixel verdict

- environment, rain-wet material, and dimetric city finish: usable only as `ENVIRONMENT_LOOK_DONOR_ONLY`
- Guardian Z: generic tall-proportion hero-mecha read; V10X and approximately four-head old-super-robot identity insufficient
- BREAKER: high-shell turtle-like ordinary quadruped; B load-bearing semi-upright forelimbs and B+X first read failed
- integrated frame is a failure diagnostic, not a PASS and not a Call03 foundation
- `CALL03=false`; `CALL04=false`; no further ImageGen call was made
"""
    (BASE / "generation-log.md").write_text(log, encoding="utf-8")

    budget = {
        "task": "A9_1A6_S_C1_CURRENT_TOPOLOGY_SCENE_LOOKDEV_CALL02",
        "status": "CALL02_VISUAL_FAIL_IDENTITY",
        "Call01_history_used": 1,
        "Call02_this_task_used": 1,
        "total_budget_used": 2,
        "remaining_budget_unspent": 2,
        "Call03": False,
        "Call04": False,
        "automatic_reroll": False,
        "disposition": "ENVIRONMENT_LOOK_DONOR_ONLY",
        "real_art_loaded": 0,
    }
    (BASE / "call-budget-receipt.json").write_text(json.dumps(budget, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    tool_receipt = {
        "tool": "builtin_image_gen",
        "call_ordinal": "Call02",
        "call_started_utc": "2026-08-20T09:46:31.170Z",
        "invocation_count_task95": 1,
        "source_output_path": "/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-e64bdc9c-d6b8-4885-ac56-5032ec08eac0.png",
        "source_output_preserved": True,
        "workspace_raw_path": str(RAW),
        "workspace_raw_sha256": sha256(RAW),
        "workspace_raw_dimensions": [1672, 941],
        "referenced_images": [{"role": item["role"], "path": str(item["path"]), "sha256": item["sha256"]} for item in INPUTS],
        "no_reroll": True,
        "Call03": False,
        "Call04": False,
    }
    (RECEIPTS / "CALL02_A_PLAN_TOOL_RECEIPT.json").write_text(json.dumps(tool_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    recomposition = {
        "status": "DETERMINISTIC_DIAGNOSTIC_ONLY",
        "cleanplate": {"path": str(cleanplate_path), "sha256": sha256(cleanplate_path)},
        "layers": {key: {"path": str(path), "sha256": sha256(path)} for key, path in layer_paths.items()},
        "composition_order": ["cleanplate", "route", "ghost", "edge_cue", "screen_ui"],
        "integrated": {"path": str(integrated_path), "sha256": sha256(integrated_path)},
        "projection": {
            "type": "orthographic_dimetric_2_to_1",
            "runtime_raw_origin_px": [-880, -170],
            "effective_camera_raw_px": [-480, 420],
            "map_rect_center_px": [640, 350],
            "tile_half_px": [40, 20],
            "registration": "footprint_bottom_center",
        },
        "physical_actor_pixels_modified": False,
        "identity_repair_attempted": False,
        "integrated_frame_disposition": "FAILURE_DIAGNOSTIC_NOT_PASS",
    }
    (RECEIPTS / "deterministic-recomposition-receipt.json").write_text(json.dumps(recomposition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = f"""# Task95 Call02 completion report

## Final state

- `CALL02_VISUAL_FAIL_IDENTITY`
- `ENVIRONMENT_LOOK_DONOR_ONLY`
- `CALL03=false`
- `CALL04=false`
- `NON_SEPARABLE_CANDIDATE_LOOK_TARGET / NOT_SPRITE / NOT_ATLAS / NOT_RUNTIME / real_art_loaded=0`

## Delivered

- raw: `{RAW}`
- cleanplate: `{cleanplate_path}`
- integrated failure-diagnostic frame: `{integrated_path}`
- separable UI, route, ghost, and edge-cue layers: `{LAYERS}`
- 50% full-screen and 100% identity review: `{REVIEW}`

## Machine evidence

- all four frozen input paths and SHA-256 values matched before Call02
- Call02 raw is `1672x941`, SHA-256 `{sha256(RAW)}`
- deterministic physical-frame operation is only crop `{RAW_CROP}` plus one LANCZOS resize to `1280x720`
- cleanplate contains no deterministic UI, route, ghost, or edge-cue layer
- integrated layers can be disabled independently; recomposition receipt records every layer SHA
- Call02 invocation count is one; remaining two calls were not consumed

## Producer visual gate

Environment/material finish is strong enough to retain only as a rainy dimetric-city look donor. Whole-screen identity gate failed:

1. Guardian Z reads as a generic tall-proportion hero mecha; V10X, approximately four-head stature, and old-super-robot weight are insufficient.
2. BREAKER reads as a high-shell turtle-like ordinary quadruped; B semi-upright load-bearing forelimbs and X alien bio-armor first read are absent.
3. Exact-guide actor registration remains `NOT_PROVEN`; the diagnostic overlay intentionally does not move or patch actors to hide drift.

Therefore neither cleanplate nor integrated frame is a repairable whole-screen candidate or Call03 foundation. No local image edit or identity-restoration claim was attempted. Machine completion does not upgrade the producer visual verdict.
"""
    (BASE / "completion-report.md").write_text(report, encoding="utf-8")


def write_hashes() -> None:
    manifest = BASE / "delivery-hashes.sha256"
    files = sorted(path for path in BASE.rglob("*") if path.is_file() and path != manifest)
    rows = [f"{sha256(path)}  {path.relative_to(BASE)}" for path in files]
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> None:
    for directory in (DELIVERY, LAYERS, RECEIPTS, REVIEW):
        directory.mkdir(parents=True, exist_ok=True)
    for item in INPUTS:
        if not item["path"].is_file() or sha256(item["path"]) != item["sha256"]:
            raise SystemExit(f"frozen input SHA mismatch: {item['path']}")

    clean = build_cleanplate()
    route = build_route_layer()
    ghost = build_ghost_layer()
    edge = build_edge_layer()
    ui = build_ui_layer()

    clean_rgba = clean.convert("RGBA")
    no_ui = clean_rgba.copy()
    for layer in (route, ghost, edge):
        no_ui.alpha_composite(layer)
    save_png(no_ui.convert("RGB"), LAYERS / "NO_SCREEN_UI_WITH_WORLD_INTENT_1280x720.png")

    integrated = clean_rgba.copy()
    for layer in (route, ghost, edge, ui):
        integrated.alpha_composite(layer)
    integrated_path = DELIVERY / "GF_PLAN_A_INTEGRATED_LOOK_TARGET_1280x720.png"
    save_png(integrated.convert("RGB"), integrated_path)

    fifty = integrated.convert("RGB").resize((640, 360), Image.Resampling.LANCZOS)
    save_png(fifty, REVIEW / "GF_PLAN_A_INTEGRATED_50_PERCENT_640x360.png")
    shutil.copyfile(integrated_path, REVIEW / "GF_PLAN_A_INTEGRATED_100_PERCENT_1280x720.png")
    build_registration_review(clean)
    build_identity_review(clean)

    cleanplate_path = DELIVERY / "PLAN_SHARED_CURRENT_PHYSICAL_CLEANPLATE_1280x720.png"
    layer_paths = {
        "ui_only": LAYERS / "UI_ONLY_1280x720.png",
        "route_only": LAYERS / "ROUTE_ONLY_1280x720.png",
        "ghost_only": LAYERS / "GHOST_ONLY_1280x720.png",
        "edge_cue_only": LAYERS / "EDGE_CUE_ONLY_1280x720.png",
        "no_screen_ui_with_world_intent": LAYERS / "NO_SCREEN_UI_WITH_WORLD_INTENT_1280x720.png",
    }
    build_documents(cleanplate_path, integrated_path, layer_paths)
    write_hashes()


if __name__ == "__main__":
    main()
