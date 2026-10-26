#!/usr/bin/env python3
"""Build the bounded A9.1-A2 visual correction evidence package.

Pillow is used only for deterministic extraction, palette reduction, layout,
measurement overlays and A4 layer compositing. It does not invent mecha art.
"""

from __future__ import annotations

import csv
import hashlib
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[5]
SOURCES = HERE / "sources"
DELIVERY = HERE / "delivery"
REVIEW = HERE / "review"

OBJECTIVE = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/62-c01e02-a9-1a2-master-production-correction-objective.md"
BOARD = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv"
OBJECTIVE_SHA = "b1cab624016e6d351ba3100fd4ebe4cf76dc6f4ad0abd88a35f7c6ec1bca816b"
BOARD_SHA = "02fe3009d8c0cc0710dcb543795decb3d80d91e67a449d1fa3e63d2c8656e801"

GZ_SURFACE_V2 = SOURCES / "guardian_z_v10x_fourview_imagegen_surface_v2.png"
GZ_SURFACE_V1 = SOURCES / "guardian_z_v10x_fourview_imagegen_surface_v1.png"
BREAKER_SURFACE_V3 = SOURCES / "breaker_bx_nonanimal_imagegen_surface_v3.png"
BREAKER_SURFACE_V4 = SOURCES / "breaker_bx_nonanimal_imagegen_surface_v4.png"
BREAKER_SURFACE_V2 = SOURCES / "breaker_bx_nonanimal_imagegen_surface_v2.png"
BREAKER_SURFACE_V1 = SOURCES / "breaker_bx_nonanimal_imagegen_surface_v1.png"

GZ_STRUCTURE = {
    name: SOURCES / f"GUARDIAN_Z_V10X_STRUCTURE_{name.upper()}_1024.png"
    for name in ("front", "left", "back", "right")
}
BREAKER_STRUCTURE = SOURCES / "BREAKER_BX_NONANIMAL_STRUCTURE_PLANNING_1024.png"

A4 = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer"
A4_LAYERS = {
    "base": A4 / "A4_MAP_B_BASE_2400x1350.png",
    "buildings": A4 / "A4_MAP_B_BUILDINGS_2400x1350.png",
    "state": A4 / "A4_MAP_B_STATE_LAYERS_2400x1350.png",
    "roofs": A4 / "A4_MAP_B_ROOFS_2400x1350.png",
    "foreground": A4 / "A4_MAP_B_FOREGROUND_2400x1350.png",
    "mask": A4 / "A4_MAP_B_OCCLUSION_MASK_2400x1350.png",
}
A5_ATLAS = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png"

FONT_REGULAR = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")
FONT_BOLD = Path("/System/Library/Fonts/STHeiti Medium.ttc")

INK = "#06151f"
PAPER = "#edf1ee"
PANEL = "#102630"
PANEL_ALT = "#17333d"
TEXT = "#edf2ef"
MUTED = "#a8bab9"
CYAN = "#58c5ca"
CORAL = "#ef5a50"
GOLD = "#dfb13e"

GZ_PALETTE = (
    "#06151f", "#101920", "#0b2238", "#174b73", "#7f2026", "#e44338",
    "#8e9699", "#e8ecea", "#8f651e", "#e5b33f", "#f3f1e8",
)
BREAKER_PALETTE = (
    "#06151f", "#101820", "#202a32", "#38434a", "#6f787a", "#a2a9aa",
    "#962429", "#ef423c",
)

GZ_METRICS = (
    ("total_height", "8.35u"),
    ("head_height", "1.95u / 4.28 heads"),
    ("shoulder_width", "5.05u"),
    ("chest_width", "3.18u"),
    ("upper_arm_length", "0.92u"),
    ("forearm_length", "1.62u"),
    ("hip_width", "1.92u"),
    ("thigh_length", "1.02u"),
    ("shin_length", "1.58u"),
    ("foot_baseline", "0.11u"),
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(path), size)


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4)) + (alpha,)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_inputs() -> None:
    if sha256_file(OBJECTIVE) != OBJECTIVE_SHA:
        raise RuntimeError("A9.1-A2 objective drift")
    if sha256_file(BOARD) != BOARD_SHA:
        raise RuntimeError("A9.1-A2 production board drift")
    required = [
        GZ_SURFACE_V2, GZ_SURFACE_V1, BREAKER_SURFACE_V4, BREAKER_SURFACE_V3, BREAKER_SURFACE_V2,
        BREAKER_SURFACE_V1, BREAKER_STRUCTURE, A5_ATLAS, *GZ_STRUCTURE.values(),
        *A4_LAYERS.values(),
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Missing A9.1-A2 inputs:\n" + "\n".join(missing))


def connected_white_to_alpha(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def is_background(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        return min(red, green, blue) >= 218 and max(red, green, blue) - min(red, green, blue) <= 28

    def push(x: int, y: int) -> None:
        offset = y * width + x
        if not seen[offset] and is_background(x, y):
            seen[offset] = 1
            queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                push(nx, ny)

    alpha = Image.new("L", image.size, 255)
    alpha_pixels = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if seen[row + x]:
                alpha_pixels[x, y] = 0
    result = image.convert("RGBA")
    result.putalpha(alpha)
    return result


def trim(image: Image.Image, padding: int = 0) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        return image
    left, top, right, bottom = bbox
    return image.crop((
        max(0, left - padding), max(0, top - padding),
        min(image.width, right + padding), min(image.height, bottom + padding),
    ))


def contain(image: Image.Image, width: int, height: int, resample: int = Image.Resampling.LANCZOS) -> Image.Image:
    scale = min(width / image.width, height / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, resample)


def fixed_palette(image: Image.Image, colors: tuple[str, ...]) -> Image.Image:
    alpha = image.getchannel("A")
    palette = Image.new("P", (1, 1))
    raw = []
    for color in colors:
        raw.extend(rgba(color)[:3])
    first = rgba(colors[0])[:3]
    while len(raw) < 768:
        raw.extend(first)
    raw = raw[:768]
    palette.putpalette(raw)
    indexed = image.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
    result = indexed.convert("RGBA")
    result.putalpha(alpha)
    return result


def clean_fixed_palette(image: Image.Image, colors: tuple[str, ...]) -> Image.Image:
    """Collapse soft rendering noise while retaining the source alpha silhouette."""
    alpha = image.getchannel("A")
    quantized = fixed_palette(image, colors)
    cleaned_rgb = quantized.convert("RGB").filter(ImageFilter.ModeFilter(3)).filter(ImageFilter.ModeFilter(3))
    cleaned = cleaned_rgb.convert("RGBA")
    cleaned.putalpha(alpha)
    return fixed_palette(cleaned, colors)


def keep_largest_alpha_component(image: Image.Image) -> Image.Image:
    """Discard accidental fragments from an adjacent turnaround view."""
    alpha = image.getchannel("A")
    width, height = image.size
    pixels = alpha.load()
    seen = bytearray(width * height)
    largest: list[tuple[int, int]] = []
    for start_y in range(height):
        for start_x in range(width):
            offset = start_y * width + start_x
            if seen[offset] or pixels[start_x, start_y] == 0:
                continue
            queue: deque[tuple[int, int]] = deque([(start_x, start_y)])
            seen[offset] = 1
            component: list[tuple[int, int]] = []
            while queue:
                x, y = queue.popleft()
                component.append((x, y))
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < width and 0 <= ny < height:
                        index = ny * width + nx
                        if not seen[index] and pixels[nx, ny] > 0:
                            seen[index] = 1
                            queue.append((nx, ny))
            if len(component) > len(largest):
                largest = component
    keep = Image.new("L", image.size, 0)
    keep_pixels = keep.load()
    for x, y in largest:
        keep_pixels[x, y] = pixels[x, y]
    result = image.copy()
    result.putalpha(keep)
    return trim(result, 4)


def silhouette_outline(image: Image.Image, color: str, strength: int = 230) -> Image.Image:
    alpha = image.getchannel("A")
    edge = ImageChops.subtract(alpha.filter(ImageFilter.MaxFilter(9)), alpha.filter(ImageFilter.MinFilter(7)))
    result = Image.new("RGBA", image.size, rgba(color, 0))
    result.putalpha(edge.point(lambda value: min(strength, value)))
    return result


def paste_bottom_center(canvas: Image.Image, sprite: Image.Image, center_x: int, bottom_y: int) -> tuple[int, int]:
    x = round(center_x - sprite.width / 2)
    y = bottom_y - sprite.height
    canvas.alpha_composite(sprite, (x, y))
    return x, y


def checkerboard(size: tuple[int, int], cell: int = 24) -> Image.Image:
    canvas = Image.new("RGBA", size, rgba("#cad2d0"))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=rgba("#e4e8e5"))
    return canvas


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str) -> None:
    draw.rounded_rectangle(box, radius=8, fill=PANEL, outline="#42616a", width=2)
    draw.text((box[0] + 20, box[1] + 16), title, font=font(25, True), fill=TEXT)


def line_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str, width: int = 3) -> None:
    draw.line((start, end), fill=color, width=width)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) >= abs(ey - sy):
        draw.polygon(((sx, sy), (sx + 11, sy - 6), (sx + 11, sy + 6)), fill=color)
        draw.polygon(((ex, ey), (ex - 11, ey - 6), (ex - 11, ey + 6)), fill=color)
    else:
        draw.polygon(((sx, sy), (sx - 6, sy + 11), (sx + 6, sy + 11)), fill=color)
        draw.polygon(((ex, ey), (ex - 6, ey - 11), (ex + 6, ey - 11)), fill=color)


def build_gz_assets() -> tuple[dict[str, Image.Image], Image.Image, Image.Image]:
    source = connected_white_to_alpha(Image.open(GZ_SURFACE_V2))
    boxes = {
        "front": (18, 42, 458, 940),
        "left": (476, 42, 727, 940),
        "back": (738, 42, 1200, 940),
        "right": (1202, 42, 1436, 940),
    }
    views: dict[str, Image.Image] = {}
    for name, box in boxes.items():
        view = keep_largest_alpha_component(trim(source.crop(box), 4))
        view = clean_fixed_palette(view, GZ_PALETTE)
        views[name] = view
        view.save(SOURCES / f"guardian_z_v10x_{name}_kinetic_rgba.png")

    sheet = Image.new("RGBA", (2560, 960), (0, 0, 0, 0))
    for index, name in enumerate(("front", "left", "back", "right")):
        sprite = contain(views[name], 585, 850)
        paste_bottom_center(sheet, sprite, 320 + index * 640, 910)
    sheet_path = DELIVERY / "GUARDIAN_Z_V10X_KINETIC_FOURVIEW_RGBA_2560x960.png"
    sheet = fixed_palette(sheet, GZ_PALETTE)
    sheet.save(sheet_path)

    master = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    front = contain(views["front"], 860, 900)
    paste_bottom_center(master, front, 512, 970)
    master_path = DELIVERY / "GUARDIAN_Z_V10X_KINETIC_FRONT_RGBA_1024.png"
    master = fixed_palette(master, GZ_PALETTE)
    master.save(master_path)
    return views, sheet, master


def build_breaker_assets() -> tuple[Image.Image, Image.Image, Image.Image]:
    source = clean_fixed_palette(trim(connected_white_to_alpha(Image.open(BREAKER_SURFACE_V4)), 6), BREAKER_PALETTE)
    source.save(SOURCES / "breaker_bx_nonanimal_kinetic_rgba.png")

    master = Image.new("RGBA", (1400, 1400), (0, 0, 0, 0))
    sprite = contain(source, 1280, 1300)
    paste_bottom_center(master, sprite, 700, 1360)
    master = fixed_palette(master, BREAKER_PALETTE)
    master.save(DELIVERY / "BREAKER_BX_NONANIMAL_KINETIC_MASTER_RGBA_1400.png")

    planning = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    plan_sprite = contain(source, 930, 930)
    paste_bottom_center(planning, plan_sprite, 512, 975)
    planning = fixed_palette(planning, BREAKER_PALETTE)
    planning.save(DELIVERY / "BREAKER_BX_NONANIMAL_PLANNING_PROXY_RGBA_1024.png")

    contact = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    contact_sprite = contain(source, 930, 930)
    contact_sprite = contact_sprite.resize(
        (contact_sprite.width, round(contact_sprite.height * 0.94)), Image.Resampling.NEAREST
    ).rotate(-7, expand=True, resample=Image.Resampling.BICUBIC)
    paste_bottom_center(contact, contact_sprite, 548, 985)
    contact = fixed_palette(contact, BREAKER_PALETTE)
    contact.save(DELIVERY / "BREAKER_BX_NONANIMAL_CONTACT_PROXY_RGBA_1024.png")
    return master, planning, contact


def build_gz_structure_board(views: dict[str, Image.Image]) -> Path:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((44, 26), "A9.1-A2｜馆守Z同一立体结构四向", font=font(46, True), fill=TEXT)
    draw.text((2350, 42), "one structure / orthographic rotation", font=font(20), fill=GOLD, anchor="ra")
    labels = (("front", "正面"), ("left", "严格左侧"), ("back", "背面"), ("right", "严格右侧"))
    for index, (name, label) in enumerate(labels):
        left = 30 + index * 592
        panel(draw, (left, 104, left + 562, 1042), label)
        field = checkerboard((522, 780), 24)
        sprite = contain(views[name], 500, 724)
        paste_bottom_center(field, sprite, 261, 748)
        canvas.alpha_composite(field, (left + 20, 166))
        rig = trim(connected_white_to_alpha(Image.open(GZ_STRUCTURE[name])), 2)
        rig = contain(rig, 135, 180)
        inset = Image.new("RGBA", (155, 200), rgba(INK, 220))
        paste_bottom_center(inset, rig, 78, 190)
        canvas.alpha_composite(inset, (left + 385, 820))
        draw.line((left + 34, 922, left + 530, 922), fill=CYAN, width=3)
    draw.rounded_rectangle((30, 1074, 2370, 1314), radius=8, fill=PANEL_ALT, outline="#42616a", width=2)
    checks = (
        "后脑：红冠脊连续 + 分层枕甲 + 环形耳轴",
        "躯干：胸背厚度 + 肩胛甲 + 颈后机械栈",
        "裸机背部：中央凹式挂载座 + 双小喷口，无大型背包",
        "四肢：双臂等长、肩肘膝踝轴位与脚底线闭合",
        "Denylist：平板后脑、平背封板、独立重画四视图、正面贴花式转面",
    )
    for index, item in enumerate(checks):
        x = 62 + (index % 2) * 1150
        y = 1108 + (index // 2) * 62
        draw.ellipse((x, y + 7, x + 13, y + 20), fill=CYAN if index < 4 else CORAL)
        draw.text((x + 26, y), item, font=font(21), fill=TEXT)
    path = REVIEW / "GUARDIAN_Z_SHARED_STRUCTURE_FOURVIEW_2400x1350.png"
    canvas.convert("RGB").save(path)
    return path


def build_gz_measurement_board(views: dict[str, Image.Image]) -> Path:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((44, 26), "A9.1-A2｜馆守Z结构叠合与尺寸闭合", font=font(46, True), fill=TEXT)
    draw.text((2350, 42), "V10X E02 naked body / mirrored arms", font=font(20), fill=GOLD, anchor="ra")

    # Normalized silhouette overlays demonstrate front/back and left/right rotation pairs.
    pairs = (("front", "back", "FRONT ↔ BACK"), ("left", "right", "LEFT ↔ mirrored RIGHT"))
    for index, (first, second, title) in enumerate(pairs):
        left = 34 + index * 790
        panel(draw, (left, 106, left + 752, 1010), title)
        field = checkerboard((708, 760), 24)
        for pair_index, (name, color) in enumerate(((first, CYAN), (second, CORAL))):
            rig = trim(connected_white_to_alpha(Image.open(GZ_STRUCTURE[name])), 2)
            if name == "right":
                rig = ImageOps.mirror(rig)
            rig = contain(rig, 640, 704)
            outline = silhouette_outline(rig, color)
            paste_bottom_center(field, outline, 348 + pair_index * 12, 728)
        canvas.alpha_composite(field, (left + 22, 178))
        draw.line((left + 52, 916, left + 700, 916), fill=GOLD, width=3)
        draw.text((left + 376, 954), "cyan=first / coral=second / display offset ±6px", font=font(15), fill=MUTED, anchor="ma")

    table_left = 1626
    panel(draw, (table_left, 106, 2366, 1010), "共享结构参数")
    y = 176
    for index, (key, value) in enumerate(GZ_METRICS):
        if index % 2 == 0:
            draw.rectangle((table_left + 18, y - 8, 2348, y + 52), fill=PANEL_ALT)
        draw.text((table_left + 34, y), key, font=font(21), fill=MUTED)
        draw.text((2328, y), value, font=font(21, True), fill=TEXT, anchor="ra")
        y += 72
    draw.text((table_left + 34, 918), "asymmetry", font=font(21), fill=MUTED)
    draw.text((2328, 918), "none visible in E02", font=font(21, True), fill=CYAN, anchor="ra")

    draw.rounded_rectangle((34, 1042, 2366, 1314), radius=8, fill=PANEL_ALT, outline="#42616a", width=2)
    summary = (
        "总高与脚底线：四向统一归一化；头高含后脑盔体，不把天线虚高计作躯干",
        "正背：肩宽/胸宽/髋宽左右镜像；红肩前甲为独立锁块，背部不复制红X",
        "左右：头盔、胸、肩环、圆柱前臂、骨盆、脚跟的前后厚度逐项可追踪",
        "背面：挂载座和小喷口属于裸机；V21飞翼与大型背包仍禁止进入E02",
    )
    for index, item in enumerate(summary):
        draw.text((70, 1082 + index * 55), f"{index + 1}. {item}", font=font(22), fill=TEXT)
    path = REVIEW / "GUARDIAN_Z_DIMENSIONAL_OVERLAY_2400x1350.png"
    canvas.convert("RGB").save(path)
    return path


def build_breaker_board(master: Image.Image, planning: Image.Image, contact: Image.Image) -> Path:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((44, 26), "A9.1-A2｜BREAKER B＋X非动物化母版", font=font(46, True), fill=TEXT)
    draw.text((2350, 42), "one master / deterministic contact transform", font=font(20), fill=GOLD, anchor="ra")
    panel(draw, (34, 104, 1010, 1308), "近30m地面攻城壳")
    field = checkerboard((920, 1030), 26)
    sprite = contain(trim(master), 850, 950)
    paste_bottom_center(field, sprite, 460, 982)
    canvas.alpha_composite(field, (62, 170))
    anchors = (
        ((340, 910), "低位单红缝"),
        ((220, 958), "半直立承重前构架"),
        ((510, 700), "三段轴向巨背壳"),
        ((382, 958), "闭合胸缝"),
        ((682, 580), "封闭上背核心出口"),
    )
    for index, (point, _) in enumerate(anchors, start=1):
        draw.ellipse((point[0] - 17, point[1] - 17, point[0] + 17, point[1] + 17), fill=GOLD, outline=INK, width=2)
        draw.text(point, str(index), font=font(17, True), fill=INK, anchor="mm")
    draw.rounded_rectangle((72, 1090, 972, 1284), radius=7, fill=rgba(INK, 232), outline="#42616a", width=2)
    for index, (_, label) in enumerate(anchors, start=1):
        x = 92 + ((index - 1) % 2) * 430
        y = 1110 + ((index - 1) // 2) * 48
        draw.text((x, y), f"{index}. {label}", font=font(17), fill=TEXT)

    panel(draw, (1040, 104, 2366, 710), "同一RGBA母版：规划 → 首撞")
    plan = contain(trim(planning), 570, 500)
    hit = contain(trim(contact), 570, 500)
    paste_bottom_center(canvas, plan, 1370, 650)
    paste_bottom_center(canvas, hit, 2050, 650)
    draw.text((1370, 164), "规划低伏", font=font(26, True), fill=CYAN, anchor="ma")
    draw.text((2050, 164), "首撞承压", font=font(26, True), fill=CORAL, anchor="ma")
    draw.text((1710, 664), "same pixels → y 94% → rotate -7° → x +36", font=font(18), fill=MUTED, anchor="ma")

    panel(draw, (1040, 742, 2366, 1308), "第一读法排除与同源区分")
    swarm = Image.open(A5_ATLAS).convert("RGBA").crop((96, 0, 192, 96))
    swarm = trim(swarm)
    big = contain(trim(master), 420, 340)
    small = contain(swarm, 330, 250, Image.Resampling.NEAREST)
    paste_bottom_center(canvas, big, 1370, 1175)
    paste_bottom_center(canvas, small, 2050, 1150)
    draw.text((1370, 800), "BREAKER：轴向壳＋承重构架", font=font(23, True), fill=TEXT, anchor="ma")
    draw.text((2050, 800), "小体A：低伏钳足爬行", font=font(23, True), fill=TEXT, anchor="ma")
    deny = "无龟甲鳞片／猿肩／哺乳腹腔／掌爪／兽足"
    draw.text((1705, 1262), deny, font=font(22), fill=GOLD, anchor="ma")
    path = REVIEW / "BREAKER_NONANIMAL_SAME_MASTER_DERIVATION_2400x1350.png"
    canvas.convert("RGB").save(path)
    return path


def unique_opaque_colors(image: Image.Image) -> int:
    colors = image.convert("RGBA").getdata()
    return len({pixel[:3] for pixel in colors if pixel[3] > 0})


def swatches(draw: ImageDraw.ImageDraw, colors: tuple[str, ...], left: int, top: int, width: int = 56) -> None:
    for index, color in enumerate(colors):
        x = left + (index % 6) * (width + 10)
        y = top + (index // 6) * (width + 30)
        draw.rectangle((x, y, x + width, y + width), fill=color, outline="#dbe4df", width=1)
        draw.text((x, y + width + 5), color[1:].upper(), font=font(12), fill=MUTED)


def build_style_board(gz_master: Image.Image, breaker_master: Image.Image) -> Path:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((44, 26), "A9.1-A2｜KINETIC_CEL原像素证据", font=font(46, True), fill=TEXT)
    draw.text((2350, 42), "CML128 = Working art-direction lock", font=font(20), fill=GOLD, anchor="ra")
    units = (
        ("馆守Z", gz_master, GZ_PALETTE, 180, "4主色块＋墨线／两级硬阴影"),
        ("BREAKER", breaker_master, BREAKER_PALETTE, 300, "黑灰主块＋单红缝／两级硬阴影"),
    )
    for index, (name, master, palette, map_height, note) in enumerate(units):
        left = 34 + index * 1176
        panel(draw, (left, 104, left + 1140, 1308), name)
        field = checkerboard((520, 660), 24)
        large = contain(trim(master), 490, 610, Image.Resampling.NEAREST)
        paste_bottom_center(field, large, 260, 632)
        canvas.alpha_composite(field, (left + 24, 176))

        crop = trim(master)
        crop = crop.crop((crop.width // 4, crop.height // 5, crop.width * 3 // 4, crop.height * 3 // 5))
        crop = contain(crop, 510, 330, Image.Resampling.NEAREST)
        zoom = checkerboard((540, 360), 18)
        paste_bottom_center(zoom, crop, 270, 340)
        canvas.alpha_composite(zoom, (left + 568, 176))
        draw.text((left + 838, 548), "100% → nearest pixel zoom", font=font(18), fill=MUTED, anchor="ma")

        actual = contain(trim(master), 360, map_height, Image.Resampling.NEAREST)
        baseline = 930
        paste_bottom_center(canvas, actual, left + 272, baseline)
        draw.line((left + 66, baseline, left + 500, baseline), fill=CYAN, width=3)
        draw.text((left + 272, 946), f"实际地图校验高 {map_height}px", font=font(18), fill=CYAN, anchor="ma")

        swatches(draw, palette, left + 568, 730)
        draw.text((left + 568, 938), f"opaque RGB count = {unique_opaque_colors(master)}", font=font(20, True), fill=TEXT)
        draw.text((left + 568, 980), note, font=font(20), fill=MUTED)
        draw.text((left + 568, 1022), "无软渐变／无商品反射／无随机磨损噪声", font=font(20), fill=GOLD)
        draw.text((left + 568, 1064), "透明边缘只用于抗锯齿，不新增色阶", font=font(18), fill=MUTED)
    path = REVIEW / "KINETIC_CEL_PIXEL_EVIDENCE_2400x1350.png"
    canvas.convert("RGB").save(path)
    return path


def project(tile_x: float, tile_y: float) -> tuple[int, int]:
    return round(880 + (tile_x - tile_y) * 40), round(170 + (tile_x + tile_y) * 20)


def cell_polygon(tile_x: int, tile_y: int) -> tuple[tuple[int, int], ...]:
    x, y = project(tile_x, tile_y)
    return ((x, y - 20), (x + 40, y), (x, y + 20), (x - 40, y))


def footprint_center(tile_x: int, tile_y: int, size: int) -> tuple[int, int]:
    return project(tile_x + (size - 1) / 2, tile_y + (size - 1) / 2)


def draw_footprint(layer: Image.Image, tile_x: int, tile_y: int, size: int, color: str) -> tuple[int, int]:
    draw = ImageDraw.Draw(layer, "RGBA")
    for x in range(tile_x, tile_x + size):
        for y in range(tile_y, tile_y + size):
            polygon = cell_polygon(x, y)
            draw.polygon(polygon, fill=rgba(color, 68), outline=rgba(color, 230))
    anchor = footprint_center(tile_x, tile_y, size)
    draw.line((anchor[0] - 12, anchor[1], anchor[0] + 12, anchor[1]), fill=rgba("#ffffff", 255), width=3)
    draw.line((anchor[0], anchor[1] - 12, anchor[0], anchor[1] + 12), fill=rgba("#ffffff", 255), width=3)
    return anchor


def opacity(image: Image.Image, alpha: float) -> Image.Image:
    image = image.convert("RGBA")
    channel = image.getchannel("A").point(lambda value: round(value * alpha))
    image.putalpha(channel)
    return image


def outline_from_alpha(image: Image.Image, color: str) -> Image.Image:
    alpha = image.getchannel("A")
    outer = alpha.filter(ImageFilter.MaxFilter(9))
    inner = alpha.filter(ImageFilter.MinFilter(5))
    edge = ImageChops.subtract(outer, inner)
    result = Image.new("RGBA", image.size, rgba(color, 0))
    result.putalpha(edge.point(lambda value: min(220, value)))
    return result


def central_viewport(full: Image.Image, caption: str) -> Image.Image:
    canvas = Image.new("RGBA", (1280, 720), rgba("#07151a"))
    crop = full.crop((670, 353, 1570, 947))
    canvas.alpha_composite(crop, (0, 54))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1280, 54), fill=rgba("#081820"))
    draw.text((24, 13), caption, font=font(21, True), fill=TEXT)
    draw.rectangle((900, 54, 1279, 647), fill=rgba("#091c24", 244), outline=rgba(CYAN), width=2)
    draw.text((930, 84), "A4 MAP-B / CENTRAL", font=font(20, True), fill=CYAN)
    draw.text((930, 126), "tile_half 40×20", font=font(18), fill=MUTED)
    draw.text((930, 162), "origin -880,-170", font=font(18), fill=MUTED)
    draw.text((930, 218), "2×2 馆守Z", font=font(21), fill=GOLD)
    draw.text((930, 258), "3×3 BREAKER", font=font(21), fill=CORAL)
    draw.text((930, 298), "1×1 小体A", font=font(21), fill=CYAN)
    draw.text((930, 354), "白十字 = bottom_center pivot", font=font(17), fill=TEXT)
    draw.text((930, 392), "色菱形 = real footprint", font=font(17), fill=TEXT)
    draw.text((930, 448), "review overlay only", font=font(17), fill=MUTED)
    return canvas


def build_map_evidence(gz_master: Image.Image, breaker_master: Image.Image) -> tuple[Path, Path, Path]:
    base = Image.open(A4_LAYERS["base"]).convert("RGBA")
    buildings = Image.open(A4_LAYERS["buildings"]).convert("RGBA")
    state = Image.open(A4_LAYERS["state"]).convert("RGBA")
    roofs = Image.open(A4_LAYERS["roofs"]).convert("RGBA")
    foreground = Image.open(A4_LAYERS["foreground"]).convert("RGBA")

    pre = base.copy()
    pre.alpha_composite(buildings)
    pre.alpha_composite(state)
    marks = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gz_anchor = draw_footprint(marks, 11, 11, 2, GOLD)
    breaker_anchor = draw_footprint(marks, 18, 8, 3, CORAL)
    swarm_anchors = [
        draw_footprint(marks, 13, 9, 1, CYAN),
        draw_footprint(marks, 20, 10, 1, CYAN),
        draw_footprint(marks, 23, 8, 1, CYAN),
    ]
    pre.alpha_composite(marks)

    gz = contain(trim(gz_master), 300, 210, Image.Resampling.NEAREST)
    breaker = contain(trim(breaker_master), 520, 350, Image.Resampling.NEAREST)
    swarm_atlas = Image.open(A5_ATLAS).convert("RGBA")
    swarm = trim(swarm_atlas.crop((96, 0, 192, 96)))
    paste_bottom_center(pre, gz, gz_anchor[0], gz_anchor[1] + 6)
    paste_bottom_center(pre, breaker, breaker_anchor[0], breaker_anchor[1] + 12)
    for anchor in swarm_anchors:
        paste_bottom_center(pre, swarm, anchor[0], anchor[1] + 4)
    pivot_marks = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pivot_draw = ImageDraw.Draw(pivot_marks)
    for anchor in (gz_anchor, breaker_anchor, *swarm_anchors):
        pivot_draw.line((anchor[0] - 10, anchor[1], anchor[0] + 10, anchor[1]), fill=rgba("#ffffff"), width=3)
        pivot_draw.line((anchor[0], anchor[1] - 10, anchor[0], anchor[1] + 10), fill=rgba("#ffffff"), width=3)
    pre.alpha_composite(pivot_marks)

    full = pre.copy()
    full.alpha_composite(roofs)
    full.alpha_composite(foreground)
    full_path = REVIEW / "A4_MAP_B_ACTUAL_UNITS_FULL_OCCLUSION_2400x1350.png"
    full.convert("RGB").save(full_path)

    fade = pre.copy()
    fade.alpha_composite(opacity(roofs, 0.5))
    fade.alpha_composite(opacity(foreground, 0.5))
    combined_occ = Image.alpha_composite(roofs, foreground)
    fade.alpha_composite(outline_from_alpha(combined_occ, CYAN))
    fade_path = REVIEW / "A4_MAP_B_ACTUAL_UNITS_50P_OUTLINE_2400x1350.png"
    fade.convert("RGB").save(fade_path)

    full_view = central_viewport(full, "FULL OCCLUSION｜原屋顶／前景")
    fade_view = central_viewport(fade, "50% + OUTLINE｜单位靠近时")
    full_view.save(REVIEW / "A4_CENTRAL_ACTUAL_UNITS_FULL_1280x720.png")
    fade_view.save(REVIEW / "A4_CENTRAL_ACTUAL_UNITS_50P_1280x720.png")

    board = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(board)
    draw.text((44, 26), "A9.1-A2｜A4实际pivot／footprint／遮挡", font=font(46, True), fill=TEXT)
    draw.text((2350, 42), "actual MAP-B layers / no map redraw", font=font(20), fill=GOLD, anchor="ra")
    left = contain(full, 1460, 1030)
    board.alpha_composite(left, (34, 112))
    full_small = contain(full_view, 830, 467)
    fade_small = contain(fade_view, 830, 467)
    board.alpha_composite(full_small, (1530, 112))
    board.alpha_composite(fade_small, (1530, 610))
    draw.rounded_rectangle((1530, 1108, 2360, 1310), radius=8, fill=PANEL, outline="#42616a", width=2)
    lines = (
        "馆守Z 18m：2×2 / 210px",
        "BREAKER near-30m：3×3 / 350px",
        "小体A：1×1 / 96px",
        "pivot：bottom_center；脚点落于白十字",
        "遮挡：原层 vs 50%淡出＋轮廓",
    )
    for index, text_value in enumerate(lines):
        draw.text((1560, 1132 + index * 32), text_value, font=font(18), fill=TEXT if index < 3 else MUTED)
    board_path = REVIEW / "A4_ACTUAL_PIVOT_FOOTPRINT_OCCLUSION_BOARD_2400x1350.png"
    board.convert("RGB").save(board_path)
    return full_path, fade_path, board_path


def build_overview(gz_board: Path, breaker_board: Path, style_board: Path, map_board: Path) -> Path:
    canvas = Image.new("RGBA", (2400, 1800), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    draw.text((52, 34), "C01E02 A9.1-A2｜母版生产性纠偏总览", font=font(48, True), fill="#12232a")
    draw.text((2348, 50), "Candidate / runtime_allowed=false / runtime_handoff=none", font=font(19), fill="#8c3d35", anchor="ra")
    entries = (
        (gz_board, (44, 122, 1178, 886), "馆守Z：同一立体结构四向"),
        (breaker_board, (1222, 122, 2356, 886), "BREAKER：去动物化B＋X"),
        (style_board, (44, 948, 1178, 1712), "KINETIC_CEL：真实像素"),
        (map_board, (1222, 948, 2356, 1712), "A4：真实落点与遮挡"),
    )
    for path, box, label in entries:
        image = Image.open(path).convert("RGB")
        thumb = ImageOps.contain(image, (box[2] - box[0], box[3] - box[1] - 58), method=Image.Resampling.LANCZOS)
        px = box[0] + (box[2] - box[0] - thumb.width) // 2
        py = box[1] + (box[3] - box[1] - 58 - thumb.height) // 2
        canvas.alpha_composite(thumb.convert("RGBA"), (px, py))
        draw.rectangle(box, outline="#28434a", width=3)
        draw.rectangle((box[0], box[3] - 56, box[2], box[3]), fill=rgba("#07151f", 220))
        draw.text((box[0] + 18, box[3] - 45), label, font=font(22, True), fill=TEXT)
    path = REVIEW / "A91A2_MASTER_REVIEW_OVERVIEW_2400x1800.png"
    canvas.convert("RGB").save(path)
    return path


def dimensions(path: Path) -> str:
    with Image.open(path) as image:
        return f"{image.width}x{image.height}"


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, str]]:
    sources = (
        ("A91A2_OBJECTIVE", OBJECTIVE, "Producer authority", "active objective"),
        ("A91A2_BOARD", BOARD, "Producer board", "active work row"),
        ("CML_LOCKS", PROJECT / "docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv", "Canon art locks", "CML001/CML008 Hard identity; CML128 Working art direction"),
        ("V10X_FRONT", PROJECT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png", "Scoped V10X Candidate parent", "front identity only"),
        ("GZ_HEAD_VOLUME", PROJECT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_head_sculpt_dual_aux_antenna_three_view_candidate_v9w.png", "Candidate structure reference", "head depth and antenna continuity"),
        ("GZ_SIDE_REAR", PROJECT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_side_rear_turnaround_candidate_v11y.png", "Candidate structure reference", "side/rear depth only"),
        ("GZ_REAR_VERNIER", PROJECT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_rear_integral_verniers_candidate_v14.png", "Candidate structure reference", "naked-body mount and verniers"),
        ("GZ_SURFACE_V2", GZ_SURFACE_V2, "A9.1-A2 generated correction source", "active surface source"),
        ("GZ_SURFACE_V1", GZ_SURFACE_V1, "A9.1-A2 rejected source", "history only: flat rear"),
        ("BREAKER_B_APPROVAL", PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv", "User approval receipt", "B silhouette + X surface relation"),
        ("BREAKER_B_SHEET", PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png", "Approved derivative direction", "scale and five anchors"),
        ("BREAKER_X_BOARD", PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png", "Approved derivative direction", "X alien bio-armor relation"),
        ("BREAKER_SURFACE_V4", BREAKER_SURFACE_V4, "A9.1-A2 generated correction source", "active axial siege-shell source"),
        ("BREAKER_SURFACE_V3", BREAKER_SURFACE_V3, "A9.1-A2 rejected source", "history only: residual quadruped read"),
        ("BREAKER_SURFACE_V2", BREAKER_SURFACE_V2, "A9.1-A2 intermediate source", "history only: red dorsal cap"),
        ("BREAKER_SURFACE_V1", BREAKER_SURFACE_V1, "A9.1-A2 intermediate source", "history only: extra red marks"),
        ("A4_APPROVAL", PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-a4/a4-user-approval-receipt.tsv", "User approval receipt", "six core MAP-B layers"),
        ("A5_ATLAS", A5_ATLAS, "Approved Demo handoff source", "96px external overlay only"),
        ("A4_BASE", A4_LAYERS["base"], "Approved A4 derivative source", "actual map evidence"),
        ("A4_BUILDINGS", A4_LAYERS["buildings"], "Approved A4 derivative source", "actual map evidence"),
        ("A4_STATE", A4_LAYERS["state"], "Approved A4 derivative source", "actual map evidence"),
        ("A4_ROOFS", A4_LAYERS["roofs"], "Approved A4 derivative source", "actual occlusion evidence"),
        ("A4_FOREGROUND", A4_LAYERS["foreground"], "Approved A4 derivative source", "actual occlusion evidence"),
        ("A4_MASK", A4_LAYERS["mask"], "Approved A4 control source", "occlusion audit"),
    )
    rows = []
    for source_id, path, authority, role in sources:
        if not path.is_file():
            raise RuntimeError(f"Missing receipt source: {path}")
        rows.append({
            "source_id": source_id,
            "path": str(path.relative_to(PROJECT)),
            "sha256": sha256_file(path),
            "authority": authority,
            "role": role,
            "runtime_allowed": "false",
        })
    return rows


def write_metadata(outputs: list[Path]) -> None:
    manifest_rows = []
    for path in outputs:
        manifest_rows.append({
            "stable_id": "CAND_C01E02_A91A2_" + path.stem,
            "path": str(path.relative_to(HERE)),
            "type": path.suffix.lstrip("."),
            "dimensions": dimensions(path) if path.suffix.lower() == ".png" else "n/a",
            "mode": Image.open(path).mode if path.suffix.lower() == ".png" else "text",
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "sha256": sha256_file(path),
            "notes": "A9.1-A2 review evidence; not Runtime or exact handoff",
        })
    write_tsv(
        HERE / "asset-manifest.tsv",
        ["stable_id", "path", "type", "dimensions", "mode", "lifecycle", "runtime_allowed", "runtime_handoff", "sha256", "notes"],
        manifest_rows,
    )
    write_tsv(
        HERE / "source-receipt.tsv",
        ["source_id", "path", "sha256", "authority", "role", "runtime_allowed"],
        source_rows(),
    )
    keypoint_rows = []
    for direction in ("front", "left", "back", "right"):
        for key, value in GZ_METRICS:
            keypoint_rows.append({
                "stable_id": "CAND_C01E02_A91A2_GZ_V10X_STRUCTURE_MASTER_V1",
                "direction": direction,
                "measurement": key,
                "value": value,
                "relation": "same structural rig; normalized common baseline",
                "lifecycle": "Candidate",
            })
    for key, value in (
        ("red_sensor", "one low horizontal slit"),
        ("forelimb", "load-bearing semi-upright siege strut"),
        ("dorsal_shell", "three axial masses; no turtle scutes"),
        ("chest_seam", "closed in E02"),
        ("upper_back_exit", "sealed and cold in E02"),
    ):
        keypoint_rows.append({
            "stable_id": "CAND_C01E02_A91A2_BREAKER_BX_NONANIMAL_MASTER_V1",
            "direction": "north_three_quarter",
            "measurement": key,
            "value": value,
            "relation": "same master for planning/contact",
            "lifecycle": "Candidate",
        })
    write_tsv(
        HERE / "structure-keypoints.tsv",
        ["stable_id", "direction", "measurement", "value", "relation", "lifecycle"],
        keypoint_rows,
    )
    write_tsv(
        HERE / "scale-pivot-contract.tsv",
        ["stable_id", "entity", "world_scale", "footprint", "tile_half", "canvas_world_origin", "review_height", "pivot", "occlusion", "runtime_allowed", "runtime_handoff"],
        [
            {"stable_id": "CAND_C01E02_A91A2_GZ_MAP_EVIDENCE", "entity": "V353U001", "world_scale": "18m", "footprint": "2x2", "tile_half": "40,20", "canvas_world_origin": "-880,-170", "review_height": "210px", "pivot": "bottom_center", "occlusion": "full vs 50%+outline", "runtime_allowed": "false", "runtime_handoff": "none"},
            {"stable_id": "CAND_C01E02_A91A2_BREAKER_MAP_EVIDENCE", "entity": "ENEMY_C01_BREAKER", "world_scale": "near-30m", "footprint": "3x3", "tile_half": "40,20", "canvas_world_origin": "-880,-170", "review_height": "350px", "pivot": "bottom_center", "occlusion": "full vs 50%+outline", "runtime_allowed": "false", "runtime_handoff": "none"},
            {"stable_id": "A5_RIFT_SWARM_A_96_REFERENCE", "entity": "ENEMY_C01_RIFT_SWARM", "world_scale": "small", "footprint": "1x1", "tile_half": "40,20", "canvas_world_origin": "-880,-170", "review_height": "96px", "pivot": "bottom_center", "occlusion": "external approved overlay", "runtime_allowed": "false", "runtime_handoff": "none"},
        ],
    )
    write_tsv(
        HERE / "style-palette-evidence.tsv",
        ["stable_id", "authority", "main_blocks", "palette", "opaque_rgb_count", "shadow_rule", "gradient", "wear", "lifecycle"],
        [
            {"stable_id": "CAND_C01E02_A91A2_GZ_KINETIC", "authority": "CML128 Working art-direction lock", "main_blocks": "navy;red;silver;gold", "palette": ";".join(GZ_PALETTE), "opaque_rgb_count": str(unique_opaque_colors(Image.open(DELIVERY / "GUARDIAN_Z_V10X_KINETIC_FRONT_RGBA_1024.png"))), "shadow_rule": "max two hard values per family", "gradient": "none", "wear": "near-zero", "lifecycle": "Candidate"},
            {"stable_id": "CAND_C01E02_A91A2_BREAKER_KINETIC", "authority": "CML128 Working art-direction lock", "main_blocks": "ink;charcoal;bone-gray;single-red-slit", "palette": ";".join(BREAKER_PALETTE), "opaque_rgb_count": str(unique_opaque_colors(Image.open(DELIVERY / "BREAKER_BX_NONANIMAL_KINETIC_MASTER_RGBA_1400.png"))), "shadow_rule": "max two hard values per family", "gradient": "none", "wear": "none", "lifecycle": "Candidate"},
        ],
    )

    (HERE / "generation-log.md").write_text(
        """# A9.1-A2 Generation Log\n\n"
        "- V10X front identity was retained. The first A9.1-A2 four-view surface source was rejected because its rear was a flat closure and lost head volume.\n"
        "- The active V2 surface source was corrected with V9W head depth, V11Y side/rear depth and V14 naked-body mount/vernier references.\n"
        "- Four directions consume one deterministic Three.js structure rig. The polished sheet is palette-reduced and measured against that rig; it is not four independent generations.\n"
        "- BREAKER V1/V2 are history-only. V3 is the active source and is deterministically palette-reduced; planning/contact share the same RGBA pixels.\n"
        "- CML128 is recorded as a Working project art-direction lock, never as a Hard identity lock. CML001 and CML008 remain the identity locks.\n"
        "- Pillow performs extraction, palette reduction, review layout, measurement and approved A4 layer compositing only.\n"
        "- Multi-view production denylist: flat rear closure, flat occiput, pasted front motifs, independent view redraws, untracked joint relocation, and missing mount/thruster continuity.\n"
        """,
        encoding="utf-8",
    )
    (HERE / "completion-report.md").write_text(
        """# C01E02 A9.1-A2 Completion Report\n\n"
        "## Completed\n\n"
        "1. Guardian Z now has one traceable four-direction structural rig, a corrected volumetric rear, ten shared measurements, mirrored limb declaration and a KINETIC_CEL delivery sheet.\n"
        "2. BREAKER now reads as an alien siege shell rather than a turtle/ape quadruped while retaining the five approved B+X anchors. Planning and contact are deterministic transforms of one RGBA master.\n"
        "3. Both masters use fixed hard palettes with no soft gradient or material-noise expansion; the review board shows native pixels, nearest-neighbour zoom and actual map display heights.\n"
        "4. The approved A4 MAP-B layers demonstrate real 2x2, 3x3 and 1x1 footprints, bottom-center pivots, feet contact and full versus 50%+outline occlusion.\n"
        "5. Source authority now records CML128 as Working art direction. CML001/CML008 identity locks are unchanged.\n\n"
        "## Boundary\n\n"
        "All outputs remain Candidate / runtime_allowed=false / runtime_handoff=none. No Atlas, Gold Frame, Godot, Runtime, LibTV or A9.1-B work was created or authorized. Producer collection is the stop point.\n"
        """,
        encoding="utf-8",
    )

    hash_targets = outputs + [
        HERE / "asset-manifest.tsv", HERE / "source-receipt.tsv",
        HERE / "structure-keypoints.tsv", HERE / "scale-pivot-contract.tsv",
        HERE / "style-palette-evidence.tsv", HERE / "generation-log.md",
        HERE / "completion-report.md", HERE / "generate_a9_1a2_package.py",
        HERE / "validate_a9_1a2_package.py",
    ]
    lines = [f"{sha256_file(path)}  {path.relative_to(PROJECT)}" for path in hash_targets]
    (HERE / "core-delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    DELIVERY.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    validate_inputs()
    views, gz_sheet, gz_master = build_gz_assets()
    breaker_master, breaker_planning, breaker_contact = build_breaker_assets()
    gz_structure = build_gz_structure_board(views)
    gz_measure = build_gz_measurement_board(views)
    breaker_board = build_breaker_board(breaker_master, breaker_planning, breaker_contact)
    style_board = build_style_board(gz_master, breaker_master)
    map_full, map_fade, map_board = build_map_evidence(gz_master, breaker_master)
    overview = build_overview(gz_structure, breaker_board, style_board, map_board)
    outputs = [
        DELIVERY / "GUARDIAN_Z_V10X_KINETIC_FOURVIEW_RGBA_2560x960.png",
        DELIVERY / "GUARDIAN_Z_V10X_KINETIC_FRONT_RGBA_1024.png",
        DELIVERY / "BREAKER_BX_NONANIMAL_KINETIC_MASTER_RGBA_1400.png",
        DELIVERY / "BREAKER_BX_NONANIMAL_PLANNING_PROXY_RGBA_1024.png",
        DELIVERY / "BREAKER_BX_NONANIMAL_CONTACT_PROXY_RGBA_1024.png",
        gz_structure, gz_measure, breaker_board, style_board,
        map_full, map_fade, map_board,
        REVIEW / "A4_CENTRAL_ACTUAL_UNITS_FULL_1280x720.png",
        REVIEW / "A4_CENTRAL_ACTUAL_UNITS_50P_1280x720.png",
        overview,
    ]
    write_metadata(outputs)
    print(f"A9.1-A2 generated: {len(outputs)} assets")


if __name__ == "__main__":
    main()
