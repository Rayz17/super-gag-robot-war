#!/usr/bin/env python3
"""Build Task 65 P0 evidence from ImageGen-authored visible sources.

Allowed operations only: connected-background removal, white despill at the
alpha edge, crop, pad, one resize per derivative, approved A4 layer
compositing, review-board layout, and mechanical assertions.  This script
does not draw, recolor, complete, or alter any subject geometry.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path("/Users/rayz/Documents/超gag机器人大战")
OUT = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-sprite-first-master-pilot"
A4 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer"

RAW_GZ = Path("/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-7ece8686-72b5-4e98-b146-5c7ee675e780.png")
RAW_BREAKER = Path("/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-d22713bc-a4f8-4914-aac3-2d8bf9a491c9.png")

CML008 = ROOT / ".superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png"
V10X = ROOT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png"
BREAKER_B = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png"
BREAKER_X = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png"

GZ_OUT = OUT / "P0_GUARDIAN_Z_Q_SOUTH_IDLE_SOURCE_1024.png"
BREAKER_OUT = OUT / "P0_BREAKER_BX_Q_NORTH_CHARGE_READY_SOURCE_1024.png"
SWEEP_OUT = OUT / "P0_NATIVE_SCALE_SWEEP_A4_1280x720.png"
BOARD_OUT = OUT / "P0_IDENTITY_SOURCE_AND_ANCHOR_BOARD_2400x1350.png"

INK = "#07151b"
PANEL = "#10252d"
PANEL_2 = "#0c1d24"
TEXT = "#edf2ef"
MUTED = "#a9b9ba"
GOLD = "#e5b84f"
CORAL = "#f05f55"
CYAN = "#58c5ca"


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size, index=1 if bold and "PingFang" in candidate else 0)
        except OSError:
            continue
    return ImageFont.load_default()


def remove_connected_white_background(path: Path) -> Image.Image:
    """Remove only light neutral pixels connected to the canvas boundary."""
    image = Image.open(path).convert("RGB")
    width, height = image.size
    pixels = image.load()
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def is_bg(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        return min(red, green, blue) >= 218 and max(red, green, blue) - min(red, green, blue) <= 30

    def push(x: int, y: int) -> None:
        offset = y * width + x
        if not seen[offset] and is_bg(x, y):
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
    ap = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if seen[row + x]:
                ap[x, y] = 0

    # Limit edge antialias/despill to the one-pixel foreground band touching
    # the removed white field. Interior white armor remains fully opaque.
    touching_bg = alpha.filter(ImageFilter.MinFilter(3))
    band = ImageChops.subtract(alpha, touching_bg)
    bp = band.load()
    out = image.convert("RGBA")
    op = out.load()
    for y in range(height):
        for x in range(width):
            if ap[x, y] and bp[x, y]:
                red, green, blue = pixels[x, y]
                edge_alpha = max(32, min(255, 255 - min(red, green, blue)))
                if edge_alpha < 245:
                    def unmatte(channel: int) -> int:
                        return max(0, min(255, round((channel * 255 - (255 - edge_alpha) * 255) / edge_alpha)))
                    op[x, y] = (unmatte(red), unmatte(green), unmatte(blue), edge_alpha)
                else:
                    op[x, y] = (red, green, blue, 255)
            elif ap[x, y] == 0:
                op[x, y] = (0, 0, 0, 0)
    return out


def trim(image: Image.Image, padding: int = 0) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError("empty alpha source")
    left, top, right, bottom = bbox
    return image.crop((
        max(0, left - padding),
        max(0, top - padding),
        min(image.width, right + padding),
        min(image.height, bottom + padding),
    ))


def one_resize_to_frame(clean: Image.Image, frame_size: int, padding: int) -> Image.Image:
    """Trim raw clean pixels, resize once, then pad into an exact square."""
    subject = trim(clean, 2)
    inner = frame_size - 2 * padding
    scale = min(inner / subject.width, inner / subject.height)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    resized = subject.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (frame_size, frame_size), (0, 0, 0, 0))
    x = round((frame_size - resized.width) / 2)
    y = frame_size - padding - resized.height
    canvas.alpha_composite(resized, (x, y))
    return canvas


def checkerboard(size: tuple[int, int], cell: int = 20) -> Image.Image:
    canvas = Image.new("RGBA", size, rgba("#d9dfdd"))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=rgba("#eef1ef"))
    return canvas


def contain(image: Image.Image, width: int, height: int, resample: int = Image.Resampling.LANCZOS) -> Image.Image:
    scale = min(width / image.width, height / image.height)
    return image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), resample)


def place_center(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int], bg: str | None = None) -> None:
    left, top, right, bottom = box
    if bg:
        ImageDraw.Draw(canvas).rectangle(box, fill=rgba(bg))
    fitted = contain(image, right - left, bottom - top)
    x = left + (right - left - fitted.width) // 2
    y = top + (bottom - top - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))


def project(tile_x: float, tile_y: float) -> tuple[int, int]:
    return round(880 + (tile_x - tile_y) * 40), round(170 + (tile_x + tile_y) * 20)


def cell_polygon(tile_x: int, tile_y: int) -> tuple[tuple[int, int], ...]:
    x, y = project(tile_x, tile_y)
    return ((x, y - 20), (x + 40, y), (x, y + 20), (x - 40, y))


def draw_footprint(layer: Image.Image, tile_x: int, tile_y: int, size: int, color: str) -> tuple[int, int]:
    draw = ImageDraw.Draw(layer, "RGBA")
    for x in range(tile_x, tile_x + size):
        for y in range(tile_y, tile_y + size):
            draw.polygon(cell_polygon(x, y), fill=rgba(color, 58), outline=rgba(color, 220))
    anchor = project(tile_x + (size - 1) / 2, tile_y + (size - 1) / 2)
    draw.line((anchor[0] - 10, anchor[1], anchor[0] + 10, anchor[1]), fill=rgba("#ffffff"), width=3)
    draw.line((anchor[0], anchor[1] - 10, anchor[0], anchor[1] + 10), fill=rgba("#ffffff"), width=3)
    return anchor


def alpha_opacity(image: Image.Image, factor: float) -> Image.Image:
    out = image.convert("RGBA")
    out.putalpha(out.getchannel("A").point(lambda value: round(value * factor)))
    return out


def alpha_outline(image: Image.Image, color: str) -> Image.Image:
    alpha = image.getchannel("A")
    edge = ImageChops.subtract(alpha.filter(ImageFilter.MaxFilter(7)), alpha.filter(ImageFilter.MinFilter(5)))
    out = Image.new("RGBA", image.size, rgba(color, 0))
    out.putalpha(edge.point(lambda value: min(190, value)))
    return out


def paste_bottom_center(canvas: Image.Image, sprite: Image.Image, x: int, y: int) -> None:
    canvas.alpha_composite(sprite, (round(x - sprite.width / 2), y - sprite.height))


def build_scale_sweep(gz_clean: Image.Image, breaker_clean: Image.Image) -> None:
    base = Image.open(A4 / "A4_MAP_B_BASE_2400x1350.png").convert("RGBA")
    buildings = Image.open(A4 / "A4_MAP_B_BUILDINGS_2400x1350.png").convert("RGBA")
    state = Image.open(A4 / "A4_MAP_B_STATE_LAYERS_2400x1350.png").convert("RGBA")
    roofs = Image.open(A4 / "A4_MAP_B_ROOFS_2400x1350.png").convert("RGBA")
    foreground = Image.open(A4 / "A4_MAP_B_FOREGROUND_2400x1350.png").convert("RGBA")

    full = base.copy()
    full.alpha_composite(buildings)
    full.alpha_composite(state)

    footprint = Image.new("RGBA", full.size, (0, 0, 0, 0))
    specs = (
        ("馆守Z SOUTH / 256 / 2x2", gz_clean, 256, 13, 17, 2, GOLD),
        ("BREAKER NORTH / 320 / 3x3", breaker_clean, 320, 17, 12, 3, CORAL),
        ("BREAKER NORTH / 384 / 3x3", breaker_clean, 384, 21, 9, 3, CORAL),
        ("BREAKER NORTH / 448 / 3x3", breaker_clean, 448, 25, 6, 3, CORAL),
    )
    placed: list[tuple[str, int, int, int]] = []
    for label, clean, frame_size, tile_x, tile_y, footprint_size, color in specs:
        anchor_x, anchor_y = draw_footprint(footprint, tile_x, tile_y, footprint_size, color)
        native = one_resize_to_frame(clean, frame_size, max(12, round(frame_size * 0.045)))
        paste_bottom_center(full, native, anchor_x, anchor_y + 8)
        placed.append((label, anchor_x, anchor_y, frame_size))
    full.alpha_composite(footprint)

    # Units must remain legible for size selection while still proving the
    # approved map's real roofs/foreground and their occlusion boundaries.
    occ = Image.alpha_composite(roofs, foreground)
    full.alpha_composite(alpha_opacity(roofs, 0.42))
    full.alpha_composite(alpha_opacity(foreground, 0.42))
    full.alpha_composite(alpha_outline(occ, CYAN))

    crop_box = (560, 300, 1840, 1020)
    canvas = full.crop(crop_box)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, 1280, 58), fill=rgba("#07151b", 238))
    draw.text((22, 12), "TASK 65 P0｜A4 native scale sweep｜tile_half=(40,20)", font=font(25, True), fill=TEXT)
    draw.text((1258, 17), "Candidate / runtime_allowed=false", font=font(17), fill=GOLD, anchor="ra")
    for index, (label, anchor_x, anchor_y, frame_size) in enumerate(placed):
        x = anchor_x - crop_box[0]
        y = max(66, anchor_y - crop_box[1] - frame_size - 30)
        width = 240 if index else 205
        left = max(6, min(1274 - width, x - width // 2))
        draw.rounded_rectangle((left, y, left + width, y + 27), radius=5, fill=rgba("#091a21", 226), outline=rgba(CYAN, 180), width=1)
        draw.text((left + 8, y + 4), label, font=font(14, True), fill=TEXT)
    draw.rounded_rectangle((20, 664, 1260, 710), radius=6, fill=rgba("#07151b", 226), outline=rgba("#42616a"), width=1)
    draw.text((34, 676), "原生帧格按原始ImageGen透明源各自一次缩放；白十字=bottom_center；色菱形=2x2/3x3；屋顶/前景42%+青色轮廓仅作P0可读性证据", font=font(15), fill=MUTED)
    canvas.convert("RGB").save(SWEEP_OUT)


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, accent: str) -> None:
    draw.rounded_rectangle(box, radius=8, fill=rgba(PANEL), outline=rgba(accent), width=2)
    draw.text((box[0] + 16, box[1] + 12), title, font=font(19, True), fill=TEXT)


def draw_lines(draw: ImageDraw.ImageDraw, x: int, y: int, lines: tuple[str, ...], accent: str) -> None:
    for index, value in enumerate(lines):
        fill = rgba(accent) if value.startswith(("不可漂移", "禁止")) else rgba(TEXT if index < 2 else MUTED)
        draw.text((x, y + index * 35), value, font=font(18, index < 2), fill=fill)


def build_identity_board(gz_master: Image.Image, breaker_master: Image.Image) -> None:
    board = Image.new("RGBA", (2400, 1350), rgba(INK))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.text((38, 24), "TASK 65 P0｜身份源／锚点板", font=font(38, True), fill=TEXT)
    draw.text((2360, 40), "Candidate only / no P1 / runtime_allowed=false", font=font(18), fill=GOLD, anchor="ra")

    rows = (
        (105, 685, GOLD, "馆守Z｜CML008 Hard + V10X E02限域 → Q SOUTH IDLE", CML008, V10X, gz_master, (
            "18m；约4头身；E02完整双臂；无翼、无背包",
            "旧超级系重量；256px仍先读头冠／脸／X胸／圆核",
            "不可漂移：金色层叠头冠／中央红冠／蓝额盔／银栅格脸",
            "不可漂移：红X胸甲／圆形金核／宽方肩环／等重圆柱前臂",
            "KINETIC_CEL：深墨蓝线压；大色块；最多两级硬阴影",
            "禁止：损伤态、单臂、飞翼、背包、幼体玩具、高挑六至八头身",
        )),
        (710, 1295, CORAL, "BREAKER｜Working实体 + 用户已批B主轮廓／X表面语言 → Q NORTH CHARGE-READY", BREAKER_B, BREAKER_X, breaker_master, (
            "近30m；3x3；高背壳压住躯干；低嵌头仅一条窄红缝",
            "两条前肢主承重半直立；短后稳定器不构成第二对动物腿",
            "不可漂移：非对称异质叠片／柔性甲缝／连续受力路径",
            "不可漂移：闭合胸缝／封闭上背核心出口／同源charge-ready",
            "B+X第一读法：壳重→柔性缝→不等前肢→楔形承压垫",
            "禁止：车／雪橇／龟／猿／哺乳兽／普通四足／标准工业对称块",
        )),
    )

    for top, bottom, accent, title, ref_a, ref_b, result, lines in rows:
        panel(draw, (28, top, 405, bottom), "身份源 A", accent)
        panel(draw, (425, top, 802, bottom), "身份源 B / 限域", accent)
        panel(draw, (822, top, 1392, bottom), "ImageGen P0结果（透明预览）", accent)
        panel(draw, (1412, top, 2372, bottom), title, accent)

        place_center(board, Image.open(ref_a).convert("RGBA"), (44, top + 52, 389, bottom - 18), PANEL_2)
        place_center(board, Image.open(ref_b).convert("RGBA"), (441, top + 52, 786, bottom - 18), PANEL_2)
        preview_box = (840, top + 52, 1374, bottom - 18)
        preview = checkerboard((preview_box[2] - preview_box[0], preview_box[3] - preview_box[1]), 18)
        board.alpha_composite(preview, (preview_box[0], preview_box[1]))
        place_center(board, result, preview_box)
        draw_lines(draw, 1440, top + 90, lines, accent)

    draw.text((1200, 1322), "身份源按原字节只读；可见主体仅来自ImageGen生成/局部编辑；本板文字位于图外并由确定性排版添加", font=font(16), fill=MUTED, anchor="ma")
    board.convert("RGB").save(BOARD_OUT)


def assert_outputs() -> None:
    expected = {
        GZ_OUT: ((1024, 1024), "RGBA"),
        BREAKER_OUT: ((1024, 1024), "RGBA"),
        SWEEP_OUT: ((1280, 720), "RGB"),
        BOARD_OUT: ((2400, 1350), "RGB"),
    }
    for path, (size, mode) in expected.items():
        with Image.open(path) as image:
            assert image.size == size, (path, image.size)
            assert image.mode == mode, (path, image.mode)
            if mode == "RGBA":
                extrema = image.getchannel("A").getextrema()
                assert extrema[0] == 0 and extrema[1] == 255, (path, extrema)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gz_clean = remove_connected_white_background(RAW_GZ)
    breaker_clean = remove_connected_white_background(RAW_BREAKER)

    gz_master = one_resize_to_frame(gz_clean, 1024, 48)
    breaker_master = one_resize_to_frame(breaker_clean, 1024, 48)
    gz_master.save(GZ_OUT)
    breaker_master.save(BREAKER_OUT)

    build_scale_sweep(gz_clean, breaker_clean)
    build_identity_board(gz_master, breaker_master)
    assert_outputs()
    for path in (GZ_OUT, BREAKER_OUT, SWEEP_OUT, BOARD_OUT):
        print(path)


if __name__ == "__main__":
    main()
