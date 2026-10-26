#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[5]
SOURCES = ROOT / "sources"
DELIVERY = ROOT / "delivery"
REVIEW = ROOT / "review"

GZ_SOURCE = SOURCES / "guardian_z_v10x_qsd_turnaround_imagegen_v2.png"
BREAKER_SOURCE = SOURCES / "breaker_bx_ground_shell_master_imagegen_v2.png"
JICUN_SOURCE = PROJECT / ".superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_jicun_stand.png"
STYLE_SOURCE = PROJECT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png"
SWARM_ATLAS = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png"

FONT_REGULAR = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")
FONT_BOLD = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")

INK = "#07151d"
PANEL = "#10232d"
PANEL_2 = "#172f3a"
PAPER = "#eef2ef"
TEXT = "#edf2ef"
MUTED = "#a8bab9"
CYAN = "#5bc8cf"
CORAL = "#e5574f"
GOLD = "#d6a43b"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(path), size=size)


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def connected_white_to_alpha(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def background(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        return min(red, green, blue) >= 218 and max(red, green, blue) - min(red, green, blue) <= 24

    def push(x: int, y: int) -> None:
        index = y * width + x
        if not seen[index] and background(x, y):
            seen[index] = 1
            queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x > 0:
            push(x - 1, y)
        if x + 1 < width:
            push(x + 1, y)
        if y > 0:
            push(x, y - 1)
        if y + 1 < height:
            push(x, y + 1)

    alpha = Image.new("L", (width, height), 255)
    alpha_pixels = alpha.load()
    for y in range(height):
        offset = y * width
        for x in range(width):
            if seen[offset + x]:
                alpha_pixels[x, y] = 0

    result = image.convert("RGBA")
    result.putalpha(alpha)
    return result


def trim(image: Image.Image, padding: int = 0) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        return image
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)
    return image.crop((left, top, right, bottom))


def contain(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    scale = min(max_width / image.width, max_height / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def paste_bottom_center(canvas: Image.Image, sprite: Image.Image, center_x: int, bottom_y: int) -> tuple[int, int]:
    x = round(center_x - sprite.width / 2)
    y = bottom_y - sprite.height
    canvas.alpha_composite(sprite, (x, y))
    return x, y


def checkerboard(size: tuple[int, int], cell: int = 24) -> Image.Image:
    canvas = Image.new("RGBA", size, rgba("#cfd7d5"))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=rgba("#e4e8e5"))
    return canvas


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str) -> None:
    draw.rounded_rectangle(box, radius=8, fill=PANEL, outline="#40606b", width=2)
    draw.text((box[0] + 24, box[1] + 18), title, font=font(28, True), fill=TEXT)


def crop_gz_views(gz_rgba: Image.Image) -> dict[str, Image.Image]:
    bounds = {
        "front": (0, 0, 555, gz_rgba.height),
        "left": (575, 0, 845, gz_rgba.height),
        "back": (865, 0, 1350, gz_rgba.height),
        "right": (1390, 0, gz_rgba.width, gz_rgba.height),
    }
    return {name: trim(gz_rgba.crop(box), 4) for name, box in bounds.items()}


def build_gz_assets() -> tuple[dict[str, Image.Image], Image.Image]:
    gz_rgba = connected_white_to_alpha(Image.open(GZ_SOURCE))
    gz_rgba.save(SOURCES / "guardian_z_v10x_qsd_turnaround_rgba.png")
    views = crop_gz_views(gz_rgba)

    transparent_sheet = Image.new("RGBA", (2560, 960), (0, 0, 0, 0))
    for index, name in enumerate(("front", "left", "back", "right")):
        view = contain(views[name], 590, 850)
        paste_bottom_center(transparent_sheet, view, index * 640 + 320, 910)
    transparent_sheet.save(DELIVERY / "GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png")

    master = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    front = contain(views["front"], 850, 900)
    paste_bottom_center(master, front, 512, 970)
    master.save(DELIVERY / "GUARDIAN_Z_V10X_QSD_MASTER_FRONT_RGBA_1024.png")
    return views, master


def build_breaker_assets() -> tuple[Image.Image, Image.Image, Image.Image]:
    raw = connected_white_to_alpha(Image.open(BREAKER_SOURCE))
    raw = trim(raw, 8)
    raw.save(SOURCES / "breaker_bx_ground_shell_master_rgba_trimmed.png")

    master = Image.new("RGBA", (1400, 1400), (0, 0, 0, 0))
    sprite = contain(raw, 1280, 1300)
    paste_bottom_center(master, sprite, 700, 1360)
    master.save(DELIVERY / "BREAKER_BX_GROUND_SHELL_MASTER_RGBA_1400.png")

    planning = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    plan_sprite = contain(raw, 930, 930)
    paste_bottom_center(planning, plan_sprite, 512, 975)
    planning.save(DELIVERY / "BREAKER_BX_PLANNING_PROXY_FROM_MASTER_RGBA_1024.png")

    contact = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    contact_sprite = contain(raw, 930, 930)
    contact_sprite = contact_sprite.resize(
        (contact_sprite.width, round(contact_sprite.height * 0.94)), Image.Resampling.LANCZOS
    ).rotate(-7, expand=True, resample=Image.Resampling.BICUBIC)
    paste_bottom_center(contact, contact_sprite, 548, 985)
    contact.save(DELIVERY / "BREAKER_BX_CONTACT_PROXY_FROM_MASTER_RGBA_1024.png")
    return master, planning, contact


def build_gz_direction_board(views: dict[str, Image.Image]) -> Image.Image:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((46, 28), "A9.1-A｜馆守Z V10X唯一Q/SD母版", font=font(48, True), fill=TEXT)
    draw.text((2350, 46), "Candidate / runtime_allowed=false", font=font(21), fill=GOLD, anchor="ra")
    names = (("front", "正面"), ("left", "严格左侧"), ("back", "背面"), ("right", "严格右侧"))
    metrics = {
        "front": (714, 178, "4.01"),
        "left": (696, 170, "4.09"),
        "back": (692, 168, "4.12"),
        "right": (695, 169, "4.11"),
    }
    for index, (name, label) in enumerate(names):
        left = 36 + index * 590
        box = (left, 116, left + 560, 1055)
        panel(draw, box, label)
        field = checkerboard((520, 780), 26)
        view = contain(views[name], 500, 720)
        paste_bottom_center(field, view, 260, 744)
        canvas.alpha_composite(field, (left + 20, 184))
        body_h, head_h, ratio = metrics[name]
        draw.line((left + 34, 928, left + 526, 928), fill=CYAN, width=3)
        draw.text((left + 28, 976), f"body={body_h}px  head={head_h}px  ≈{ratio}头身", font=font(20), fill=MUTED)
    draw.rounded_rectangle((36, 1090, 2364, 1310), radius=8, fill=PANEL_2, outline="#40606b", width=2)
    statements = [
        "身份锁：金色层叠头冠＋中央红冠＋蓝额＋银栅格脸",
        "上身锁：红X胸甲＋圆形金核＋宽方肩环",
        "肢体锁：双臂等长等重；圆柱前臂；E02无翼、无背包、无损伤",
        "生产锁：同页四向；只保留身份板缝；25%缩放仍靠轮廓与三色块辨认",
    ]
    for index, statement in enumerate(statements):
        x = 76 + (index % 2) * 1120
        y = 1128 + (index // 2) * 74
        draw.ellipse((x, y + 7, x + 14, y + 21), fill=CYAN)
        draw.text((x + 28, y), statement, font=font(24), fill=TEXT)
    out = REVIEW / "GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_EVIDENCE_2400x1350.png"
    canvas.convert("RGB").save(out)
    return canvas


def build_breaker_board(master: Image.Image, planning: Image.Image, contact: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((46, 28), "A9.1-A｜BREAKER B＋X唯一地面壳母版", font=font(48, True), fill=TEXT)
    draw.text((2350, 46), "one source body / no separate contact redraw", font=font(21), fill=GOLD, anchor="ra")
    panel(draw, (36, 116, 940, 1288), "B＋X主母版｜近30m／3×3")
    field = checkerboard((850, 1010), 28)
    main = contain(trim(master), 800, 940)
    paste_bottom_center(field, main, 425, 965)
    canvas.alpha_composite(field, (62, 188))
    draw.text((72, 1216), "高背壳｜低头单红缝｜双长承重前肢｜短后足｜闭合胸缝", font=font(23), fill=TEXT)

    panel(draw, (980, 116, 2364, 600), "同源但非放大小体｜轮廓等高比较")
    small_atlas = Image.open(SWARM_ATLAS).convert("RGBA")
    small = trim(small_atlas.crop((96, 0, 192, 96)))
    breaker_same_height = contain(trim(master), 510, 350)
    small_same_height = contain(small, 510, 350)
    canvas.alpha_composite(breaker_same_height, (1050, 205))
    canvas.alpha_composite(small_same_height, (1780, 232))
    draw.text((1285, 536), "半直立／高背／长前肢", font=font(23), fill=CYAN, anchor="ma")
    draw.text((2050, 536), "低伏／四短足／扁壳", font=font(23), fill=CORAL, anchor="ma")

    panel(draw, (980, 630, 2364, 1288), "同一RGBA母版的确定性姿态代理")
    plan = contain(trim(planning), 560, 490)
    hit = contain(trim(contact), 560, 490)
    paste_bottom_center(canvas, plan, 1320, 1145)
    paste_bottom_center(canvas, hit, 2020, 1145)
    draw.text((1320, 710), "规划待机", font=font(28, True), fill=TEXT, anchor="ma")
    draw.text((2020, 710), "首撞承压代理", font=font(28, True), fill=TEXT, anchor="ma")
    draw.line((1650, 985, 1770, 925), fill=CORAL, width=8)
    draw.polygon(((1770, 925), (1730, 920), (1753, 957)), fill=CORAL)
    draw.text((1670, 1045), "same pixels → y 94% → rotate -7° → x +36", font=font(19), fill=MUTED, anchor="ma")
    draw.text((1670, 1240), "本阶段仅证明同母版派生；不是动作帧、Atlas或Runtime handoff", font=font(22), fill=GOLD, anchor="ma")
    out = REVIEW / "BREAKER_BX_IDENTITY_AND_SAME_MASTER_DERIVATION_2400x1350.png"
    canvas.convert("RGB").save(out)
    return canvas


def iso_point(origin: tuple[int, int], x: float, y: float) -> tuple[int, int]:
    return round(origin[0] + (x - y) * 40), round(origin[1] + (x + y) * 20)


def footprint_polygon(origin: tuple[int, int], x: int, y: int, size: int) -> tuple[tuple[int, int], ...]:
    return (
        iso_point(origin, x, y),
        iso_point(origin, x + size, y),
        iso_point(origin, x + size, y + size),
        iso_point(origin, x, y + size),
    )


def build_scale_board(gz_master: Image.Image, breaker_master: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((46, 28), "A9.1-A｜同一40×20等距量尺", font=font(48, True), fill=TEXT)
    draw.text((2350, 46), "18m / near-30m / 1×1", font=font(22), fill=GOLD, anchor="ra")
    origin = (1020, 225)
    for x in range(13):
        draw.line((iso_point(origin, x, 0), iso_point(origin, x, 8)), fill="#31505b", width=2)
    for y in range(9):
        draw.line((iso_point(origin, 0, y), iso_point(origin, 12, y)), fill="#31505b", width=2)

    footprints = (
        (1, 4, 1, rgba(CYAN, 85)),
        (4, 3, 2, rgba(GOLD, 80)),
        (8, 2, 3, rgba(CORAL, 75)),
    )
    for x, y, size, fill in footprints:
        polygon = footprint_polygon(origin, x, y, size)
        draw.polygon(polygon, fill=fill, outline=fill[:3] + (255,))

    swarm_atlas = Image.open(SWARM_ATLAS).convert("RGBA")
    swarm = trim(swarm_atlas.crop((96, 0, 192, 96)))
    swarm = contain(swarm, 82, 90)
    gz = contain(trim(gz_master), 230, 300)
    breaker = contain(trim(breaker_master), 385, 500)
    anchors = {
        "swarm": iso_point(origin, 1.5, 4.5),
        "gz": iso_point(origin, 5.0, 4.0),
        "breaker": iso_point(origin, 9.5, 3.5),
    }
    paste_bottom_center(canvas, swarm, anchors["swarm"][0], anchors["swarm"][1] + 6)
    paste_bottom_center(canvas, gz, anchors["gz"][0], anchors["gz"][1] + 12)
    paste_bottom_center(canvas, breaker, anchors["breaker"][0], anchors["breaker"][1] + 20)

    cards = (
        (72, 930, 706, 1275, "小体A", "1×1", "弱小低伏体", "90px校验高"),
        (883, 930, 1517, 1275, "馆守Z", "18m／2×2", "约4头身V10X", "300px校验高"),
        (1694, 930, 2328, 1275, "BREAKER", "near-30m／3×3", "B＋X地面壳", "500px校验高"),
    )
    for left, top, right, bottom, name, scale, identity, render in cards:
        draw.rounded_rectangle((left, top, right, bottom), radius=8, fill=PANEL, outline="#40606b", width=2)
        draw.text((left + 28, top + 22), name, font=font(30, True), fill=TEXT)
        draw.text((left + 28, top + 88), scale, font=font(36, True), fill=GOLD)
        draw.text((left + 28, top + 160), identity, font=font(24), fill=MUTED)
        draw.text((left + 28, top + 218), render, font=font(22), fill=CYAN)
    draw.text((1200, 1310), "tile_half=(40,20)｜量尺证据，不是地图重绘或运行时截图", font=font(21), fill=MUTED, anchor="ma")
    out = REVIEW / "SCALE_40X20_18M_30M_1X1_EVIDENCE_2400x1350.png"
    canvas.convert("RGB").save(out)

    no_labels = Image.new("RGBA", (1600, 900), rgba(INK))
    no_draw = ImageDraw.Draw(no_labels)
    no_origin = (660, 160)
    for x in range(13):
        no_draw.line((iso_point(no_origin, x, 0), iso_point(no_origin, x, 8)), fill="#294550", width=2)
    for y in range(9):
        no_draw.line((iso_point(no_origin, 0, y), iso_point(no_origin, 12, y)), fill="#294550", width=2)
    for x, y, size, fill in footprints:
        no_draw.polygon(footprint_polygon(no_origin, x, y, size), fill=fill, outline=fill[:3] + (255,))
    no_anchors = {
        "swarm": iso_point(no_origin, 1.5, 4.5),
        "gz": iso_point(no_origin, 5.0, 4.0),
        "breaker": iso_point(no_origin, 9.5, 3.5),
    }
    paste_bottom_center(no_labels, swarm, no_anchors["swarm"][0], no_anchors["swarm"][1] + 6)
    paste_bottom_center(no_labels, gz, no_anchors["gz"][0], no_anchors["gz"][1] + 12)
    paste_bottom_center(no_labels, breaker, no_anchors["breaker"][0], no_anchors["breaker"][1] + 20)
    no_labels.convert("RGB").save(REVIEW / "SCALE_NO_LABEL_PURE_READ_1600x900.png")
    return canvas


def build_style_board(gz_master: Image.Image, breaker_master: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((46, 28), "A9.1-A｜KINETIC_CEL常态画法合规", font=font(48, True), fill=TEXT)
    draw.text((2350, 46), "CML128 A档 / no Archive Offset", font=font(21), fill=GOLD, anchor="ra")
    columns = ((36, "CML128画法锚"), (828, "馆守Z Q/SD"), (1620, "BREAKER B＋X"))
    style = Image.open(STYLE_SOURCE).convert("RGB")
    style_crop = ImageOps.fit(style, (720, 650), method=Image.Resampling.LANCZOS, centering=(0.68, 0.52)).convert("RGBA")
    gz = contain(trim(gz_master), 680, 650)
    breaker = contain(trim(breaker_master), 680, 650)
    images = (style_crop, gz, breaker)
    for (left, title), image in zip(columns, images):
        panel(draw, (left, 116, left + 744, 850), title)
        field = checkerboard((700, 650), 26)
        paste_bottom_center(field, image, 350, 628)
        canvas.alpha_composite(field, (left + 22, 180))

    rows = (
        ("外轮廓", "深墨蓝压力线", "PASS", "PASS"),
        ("内线密度", "身份板缝优先", "LOW", "LOW"),
        ("色块", "红/蓝/白/金大块", "4主色", "黑/灰＋单红缝"),
        ("阴影", "两级硬边", "2 levels", "2 levels"),
        ("材质高光", "受控、非写实反射", "局部金属", "窄边冷光"),
        ("磨损预算", "常态不画细碎伤痕", "近零", "近零"),
    )
    y = 900
    col_x = (48, 370, 1000, 1760)
    headers = ("项目", "A档规则", "馆守Z", "BREAKER")
    for x, header in zip(col_x, headers):
        draw.text((x, y), header, font=font(25, True), fill=GOLD)
    y += 55
    for index, row in enumerate(rows):
        fill = PANEL if index % 2 == 0 else PANEL_2
        draw.rectangle((36, y - 8, 2364, y + 47), fill=fill)
        for x, value in zip(col_x, row):
            draw.text((x, y), value, font=font(22), fill=TEXT if x < 1000 else CYAN)
        y += 60
    draw.text((1200, 1320), "常态图不叠加B档纸白切口、错版朱红或伪档案文字", font=font(21), fill=MUTED, anchor="ma")
    canvas.convert("RGB").save(REVIEW / "KINETIC_CEL_STYLE_COMPLIANCE_2400x1350.png")
    return canvas


def build_readability_board(gz_master: Image.Image, breaker_master: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (2400, 1200), rgba(INK))
    draw = ImageDraw.Draw(canvas)
    draw.text((46, 28), "A9.1-A｜50%／25%轮廓可读性", font=font(48, True), fill=TEXT)
    swarm_atlas = Image.open(SWARM_ATLAS).convert("RGBA")
    swarm = trim(swarm_atlas.crop((96, 0, 192, 96)))
    units = (("馆守Z", trim(gz_master), 360), ("BREAKER", trim(breaker_master), 600), ("小体A", swarm, 108))
    scales = (("50%", 0.5), ("25%", 0.25))
    for row, (scale_name, scale) in enumerate(scales):
        top = 140 + row * 505
        draw.text((64, top + 190), scale_name, font=font(40, True), fill=GOLD)
        for col, (name, unit, base_h) in enumerate(units):
            left = 240 + col * 710
            box = (left, top, left + 660, top + 440)
            panel(draw, box, name)
            sprite = contain(unit, 600, max(24, round(base_h * scale)))
            paste_bottom_center(canvas, sprite, left + 330, top + 388)
            draw.line((left + 70, top + 390, left + 590, top + 390), fill="#47656d", width=2)
    draw.text((1200, 1160), "判据：头冠／红X／圆前臂；高背壳／单红缝／长前肢；低伏扁壳／短足", font=font(23), fill=MUTED, anchor="ma")
    canvas.convert("RGB").save(REVIEW / "MASTER_50_25_PERCENT_READABILITY_2400x1200.png")
    return canvas


def build_jicun_proxy() -> Image.Image:
    source = Image.open(JICUN_SOURCE).convert("RGBA")
    crop = source.crop((90, 0, 855, 1135))
    crop = trim(crop)
    portrait = contain(crop, 300, 590)
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    panel_width = 307
    draw.rectangle((0, 62, panel_width, 680), fill=rgba(INK, 228), outline=rgba(CYAN, 220), width=3)
    draw.rectangle((0, 62, panel_width, 115), fill=rgba(PANEL_2, 245))
    draw.text((18, 76), "纪存｜路线判断", font=font(23, True), fill=TEXT)
    paste_bottom_center(overlay, portrait, 158, 682)
    draw.line((306, 120, 306, 640), fill=CYAN, width=4)
    overlay.save(DELIVERY / "JICUN_CML001_COMMS_PROXY_24PCT_1280x720.png")

    review = checkerboard((1600, 900), 32)
    review.alpha_composite(overlay.resize((1600, 900), Image.Resampling.LANCZOS))
    rdraw = ImageDraw.Draw(review)
    rdraw.rectangle((0, 0, 1599, 899), outline=rgba(INK), width=8)
    rdraw.text((1560, 42), "panel width = 307 / 1280 = 23.98%", font=font(25, True), fill=INK, anchor="ra")
    rdraw.text((1560, 82), "CML001原脸＋原制服＋左臂终端｜未生成第三张脸", font=font(22), fill=INK, anchor="ra")
    review.convert("RGB").save(REVIEW / "JICUN_CML001_COMMS_USAGE_EVIDENCE_1600x900.png")
    return overlay


def build_overview(boards: list[Image.Image]) -> None:
    canvas = Image.new("RGB", (2400, 1800), INK)
    draw = ImageDraw.Draw(canvas)
    draw.text((46, 28), "C01E02 A9.1-A｜唯一母版评审总览", font=font(48, True), fill=TEXT)
    thumbs = []
    for board in boards[:4]:
        image = contain(board.convert("RGBA"), 1120, 760)
        thumb = Image.new("RGB", (1120, 760), INK)
        thumb.paste(image.convert("RGB"), ((1120 - image.width) // 2, (760 - image.height) // 2))
        thumbs.append(thumb)
    positions = ((48, 110), (1232, 110), (48, 930), (1232, 930))
    for image, position in zip(thumbs, positions):
        canvas.paste(image, position)
    draw.text((1200, 1750), "Candidate｜runtime_allowed=false｜runtime_handoff=none｜等待制作人统一回收", font=font(22), fill=GOLD, anchor="ma")
    canvas.save(REVIEW / "A9_1A_MASTER_REVIEW_OVERVIEW_2400x1800.png")


def main() -> None:
    DELIVERY.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    views, gz_master = build_gz_assets()
    breaker_master, planning, contact = build_breaker_assets()
    gz_board = build_gz_direction_board(views)
    breaker_board = build_breaker_board(breaker_master, planning, contact)
    scale_board = build_scale_board(gz_master, breaker_master)
    style_board = build_style_board(gz_master, breaker_master)
    build_readability_board(gz_master, breaker_master)
    build_jicun_proxy()
    build_overview([gz_board, breaker_board, scale_board, style_board])


if __name__ == "__main__":
    main()
