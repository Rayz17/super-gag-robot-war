from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "generation-raw" / "WANJI_CURRENT_READER_STRUCTURE_IMAGEGEN_CALL01_RAW.png"
OUT = ROOT / "delivery" / "WANJI_CURRENT_READER_STRUCTURE_USER_CONFIRMATION_BOARD_2400x1800.png"
OUT_HALF = ROOT / "delivery" / "WANJI_CURRENT_READER_STRUCTURE_USER_CONFIRMATION_BOARD_1200x900.png"

W, H = 2400, 1800
BG = "#F2F0EA"
PAPER = "#FBFAF6"
INK = "#202A32"
MUTED = "#5D6870"
LINE = "#CBD0D1"
BLUE = "#315F78"
TEAL = "#3C7F7B"
AMBER = "#B67833"
INDIGO = "#626EA0"
RED = "#A84A42"
PALE_BLUE = "#D7E5E9"
PALE_WARM = "#EADDC6"
PALE_PURPLE = "#DDD9E8"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font(size: int, bold: bool = False):
    # The bundled CJK face is legible at the 50% review size; faux-bold via stroke.
    return ImageFont.truetype(FONT_PATH, size=size)


F_TITLE = font(54)
F_SUB = font(25)
F_COL = font(34)
F_HEAD = font(28)
F_BODY = font(23)
F_SMALL = font(19)
F_TINY = font(16)


def txt(draw, xy, s, f=F_BODY, fill=INK, anchor=None, stroke=0):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=fill)


def panel(draw, box, title, accent=BLUE):
    draw.rounded_rectangle(box, radius=22, fill=PAPER, outline=LINE, width=2)
    x0, y0, x1, _ = box
    draw.rounded_rectangle((x0, y0, x1, y0 + 48), radius=22, fill=accent)
    draw.rectangle((x0, y0 + 24, x1, y0 + 48), fill=accent)
    txt(draw, (x0 + 20, y0 + 24), title, F_HEAD, "white", anchor="lm", stroke=1)


def paste_contain(canvas, source, crop, box):
    frag = source.crop(crop)
    x0, y0, x1, y1 = box
    fitted = ImageOps.contain(frag, (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    x = x0 + (x1 - x0 - fitted.width) // 2
    y = y0 + (y1 - y0 - fitted.height) // 2
    canvas.paste(fitted, (x, y))


def arrow(draw, start, end, color=TEAL, width=5, head=14, dashed=False):
    x0, y0 = start
    x1, y1 = end
    if dashed:
        steps = max(1, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 / 18))
        for i in range(0, steps, 2):
            a = i / steps
            b = min((i + 1) / steps, 1)
            draw.line((x0 + (x1 - x0) * a, y0 + (y1 - y0) * a,
                       x0 + (x1 - x0) * b, y0 + (y1 - y0) * b), fill=color, width=width)
    else:
        draw.line((x0, y0, x1, y1), fill=color, width=width)
    if abs(x1 - x0) >= abs(y1 - y0):
        sign = 1 if x1 >= x0 else -1
        pts = [(x1, y1), (x1 - sign * head, y1 - head * 0.62), (x1 - sign * head, y1 + head * 0.62)]
    else:
        sign = 1 if y1 >= y0 else -1
        pts = [(x1, y1), (x1 - head * 0.62, y1 - sign * head), (x1 + head * 0.62, y1 - sign * head)]
    draw.polygon(pts, fill=color)


def pill(draw, box, label, fill="#2E3941"):
    draw.rounded_rectangle(box, radius=13, fill=fill)
    txt(draw, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), label, F_SMALL, "white", anchor="mm", stroke=1)


def building_icon(draw, x, y, w, h, accent=BLUE, airborne=False):
    base = y + h
    draw.rounded_rectangle((x, y + h * 0.38, x + w, base), radius=7, fill=PALE_BLUE, outline=accent, width=3)
    draw.arc((x + w * 0.18, y, x + w * 0.82, y + h * 0.82), 180, 360, fill=accent, width=4)
    draw.rectangle((x + w * 0.18, y + h * 0.38, x + w * 0.82, y + h * 0.64), fill=PALE_WARM, outline=accent, width=2)
    for i in range(4):
        wx = x + w * (0.27 + i * 0.13)
        draw.rectangle((wx, y + h * 0.46, wx + w * 0.07, y + h * 0.59), fill="#D69B51")
    if airborne:
        draw.polygon([(x - w * .12, base), (x + w * 1.08, base), (x + w * .86, base + h * .28),
                      (x + w * .08, base + h * .28)], fill="#496272", outline=accent)
        for j in range(3):
            arrow(draw, (x + w * (.25 + .25 * j), base + h * .25),
                  (x + w * (.25 + .25 * j), base + h * .46), color="#63AFC3", width=3, head=8)


def draw_transition(draw, box):
    x0, y0, _, _ = box
    xs = [x0 + 72, x0 + 248, x0 + 430, x0 + 610]
    yy = y0 + 90
    building_icon(draw, xs[0], yy, 105, 70, BLUE)
    txt(draw, (xs[0] + 52, yy + 102), "固定馆", F_SMALL, anchor="mm")
    # Detached glass lobby and municipal pipe are visibly left behind.
    building_icon(draw, xs[1], yy - 2, 92, 64, BLUE)
    draw.rounded_rectangle((xs[1] - 25, yy + 44, xs[1] - 4, yy + 68), 3, fill="#DCEAF0", outline=MUTED)
    draw.line((xs[1] - 12, yy + 42, xs[1] + 10, yy + 34), fill=RED, width=3)
    txt(draw, (xs[1] + 46, yy + 102), "留地 / 断开", F_SMALL, anchor="mm")
    building_icon(draw, xs[2], yy - 18, 92, 64, BLUE, airborne=True)
    txt(draw, (xs[2] + 46, yy + 102), "离地 / 配平", F_SMALL, anchor="mm")
    building_icon(draw, xs[3], yy - 18, 103, 64, BLUE, airborne=True)
    arrow(draw, (xs[3] + 104, yy + 45), (xs[3] + 142, yy + 45), color=AMBER, width=4, head=11)
    txt(draw, (xs[3] + 51, yy + 102), "舰首转东", F_SMALL, anchor="mm")
    for i in range(3):
        arrow(draw, (xs[i] + 116, yy + 36), (xs[i + 1] - 15, yy + 36), color=TEAL, width=4, head=10)
    txt(draw, (x0 + 24, y0 + 238), "随舰：主展厅 · 两侧展廊 · 南侧泊位/舰首 · B1承力舰体", F_SMALL, BLUE)
    txt(draw, (x0 + 24, y0 + 268), "留地：外围玻璃门厅 · 市政管线 · 后加固定件", F_SMALL, RED)
    txt(draw, (x0 + 24, y0 + 297), "生活证据：入口/窗带/观众尺度仍可读；避难所直播看见“熟悉的馆”升空。", F_TINY, MUTED)


def draw_layers(draw, box):
    x0, y0, _, _ = box
    # Side section.
    sx, sy = x0 + 28, y0 + 78
    draw.rounded_rectangle((sx, sy, sx + 430, sy + 58), 14, fill=PALE_WARM, outline=AMBER, width=3)
    draw.rounded_rectangle((sx + 34, sy + 58, sx + 406, sy + 112), 10, fill=PALE_BLUE, outline=BLUE, width=3)
    draw.rounded_rectangle((sx + 70, sy + 112, sx + 370, sy + 144), 8, fill=PALE_PURPLE, outline=INDIGO, width=3)
    draw.polygon([(sx + 430, sy + 16), (sx + 525, sy + 30), (sx + 525, sy + 74), (sx + 430, sy + 62)], fill="#D9E4E5", outline=TEAL)
    txt(draw, (sx + 12, sy + 29), "L1 展陈 / 观众 / 主展厅", F_SMALL, AMBER, anchor="lm")
    txt(draw, (sx + 45, sy + 85), "B1 机库脊柱：2–12m泊位 / 单机重修", F_TINY, BLUE, anchor="lm")
    txt(draw, (sx + 82, sy + 128), "B2 残响 / 黑匣层", F_TINY, INDIGO, anchor="lm")
    txt(draw, (sx + 448, sy + 53), "舰首前甲板", F_TINY, TEAL, anchor="lm")
    for px in (sx + 125, sx + 245, sx + 345):
        arrow(draw, (px, sy + 144), (px, sy + 173), color="#63AFC3", width=3, head=8)
    txt(draw, (sx + 140, sy + 176), "低空推进 / 承力接口", F_TINY, "#4E8190")
    # Top view.
    tx, ty = x0 + 34, y0 + 245
    draw.rounded_rectangle((tx + 90, ty, tx + 450, ty + 45), 12, fill=PALE_WARM, outline=AMBER, width=2)
    draw.rounded_rectangle((tx + 40, ty + 8, tx + 115, ty + 74), 12, fill=PALE_BLUE, outline=BLUE, width=2)
    draw.rounded_rectangle((tx + 425, ty + 8, tx + 500, ty + 74), 12, fill=PALE_BLUE, outline=BLUE, width=2)
    draw.polygon([(tx + 500, ty + 18), (tx + 620, ty + 29), (tx + 620, ty + 57), (tx + 500, ty + 68)], fill="#D9E4E5", outline=TEAL)
    txt(draw, (tx + 270, ty + 23), "主展厅", F_TINY, AMBER, anchor="mm")
    txt(draw, (tx + 77, ty + 82), "展廊", F_TINY, BLUE, anchor="mm")
    txt(draw, (tx + 462, ty + 82), "展廊", F_TINY, BLUE, anchor="mm")
    txt(draw, (tx + 558, ty + 86), "前甲板", F_TINY, TEAL, anchor="mm")
    for px in (tx + 34, tx + 506):
        draw.line((px, ty + 25, px - 18 if px < tx + 100 else px + 18, ty + 25), fill=INDIGO, width=5)
    draw.ellipse((tx + 145, ty + 54, tx + 153, ty + 62), fill=RED)
    draw.ellipse((tx + 385, ty + 54, tx + 393, ty + 62), fill=RED)
    txt(draw, (x0 + 500, y0 + 275), "有限外泊 / 小口径近防", F_TINY, MUTED, anchor="lm")


def draw_scale(draw, box):
    x0, y0, _, _ = box
    # Carrier profile at a shared 3.4 px per metre scale.
    s = 3.4
    ship_x, ship_y = x0 + 120, y0 + 88
    ship_w, ship_h = int(145 * s), int(40 * s)
    draw.polygon([(ship_x, ship_y + ship_h * .32), (ship_x + ship_w * .76, ship_y + ship_h * .25),
                  (ship_x + ship_w, ship_y + ship_h * .52), (ship_x + ship_w * .88, ship_y + ship_h),
                  (ship_x + ship_w * .12, ship_y + ship_h), (ship_x, ship_y + ship_h * .72)],
                 fill="#8BA3AD", outline=BLUE)
    draw.rounded_rectangle((ship_x + 70, ship_y + 10, ship_x + ship_w * .72, ship_y + ship_h * .48),
                           16, fill=PALE_WARM, outline=AMBER, width=3)
    txt(draw, (ship_x + ship_w / 2, ship_y - 10), "万机馆 145m × 40m（设计范围 130–160 / 35–45）", F_SMALL, BLUE, anchor="ms")
    draw.line((ship_x, ship_y + ship_h + 15, ship_x + ship_w, ship_y + ship_h + 15), fill=INK, width=2)
    txt(draw, (ship_x + ship_w / 2, ship_y + ship_h + 20), "145m", F_TINY, MUTED, anchor="ma")
    # Same-scale reference subjects below, deliberately tiny when appropriate.
    base = y0 + 294
    px = x0 + 40
    # Person 1.7m
    ph = max(6, int(1.7 * s))
    draw.line((px, base - ph, px, base), fill=INK, width=3)
    draw.ellipse((px - 2, base - ph - 4, px + 2, base), fill=INK)
    txt(draw, (px, base + 6), "人 1.7", F_TINY, anchor="ma")
    # Fire truck roughly 8m long / 3m high
    px += 78
    draw.rectangle((px, base - int(3 * s), px + int(8 * s), base), fill="#C66E50", outline=INK)
    draw.ellipse((px + 4, base - 4, px + 11, base + 3), fill=INK)
    draw.ellipse((px + 18, base - 4, px + 25, base + 3), fill=INK)
    txt(draw, (px + 14, base + 6), "消防车", F_TINY, anchor="ma")
    # 9m bridge machine
    px += 92
    bh = int(9 * s)
    draw.rounded_rectangle((px, base - bh, px + 22, base), 5, fill="#D69B51", outline=INK)
    draw.line((px - 12, base - bh + 6, px + 32, base - bh + 6), fill=AMBER, width=5)
    txt(draw, (px + 10, base + 6), "架桥机 9", F_TINY, anchor="ma")
    # GZ 18m simple humanoid
    px += 95
    gh = int(18 * s)
    draw.ellipse((px + 10, base - gh, px + 24, base - gh + 14), fill=TEAL)
    draw.rectangle((px + 8, base - gh + 13, px + 26, base - 22), fill=TEAL)
    draw.line((px + 10, base - 38, px + 2, base), fill=TEAL, width=7)
    draw.line((px + 24, base - 38, px + 33, base), fill=TEAL, width=7)
    draw.line((px + 8, base - gh + 25, px - 7, base - 35), fill=TEAL, width=7)
    draw.line((px + 26, base - gh + 25, px + 39, base - 32), fill=TEAL, width=7)
    txt(draw, (px + 16, base + 6), "馆守Z 18", F_TINY, anchor="ma")
    # BREAKER low shell 29m class
    px += 110
    bw, bh = int(29 * s), int(15 * s)
    draw.polygon([(px, base - 8), (px + bw * .12, base - bh * .72), (px + bw * .52, base - bh),
                  (px + bw, base - bh * .52), (px + bw * .88, base), (px + bw * .15, base)],
                 fill="#37434A", outline=RED)
    txt(draw, (px + bw / 2, base + 6), "BREAKER 29级", F_TINY, anchor="ma")
    px += bw + 48
    # City roof 25m
    ch = int(25 * s)
    draw.rectangle((px, base - ch, px + 48, base), fill="#B9B7AE", outline=MUTED)
    for wy in range(int(base - ch + 12), base - 8, 15):
        draw.line((px + 8, wy, px + 40, wy), fill="#E8E0C9", width=3)
    txt(draw, (px + 24, base + 6), "普通楼顶", F_TINY, anchor="ma")


def draw_e04(draw, box):
    x0, y0, _, _ = box
    gx, gy, gw, gh = x0 + 24, y0 + 72, 665, 185
    draw.rounded_rectangle((gx, gy, gx + gw, gy + gh), 15, fill="#E6EFF1", outline="#A7BBC0", width=2)
    for i in range(1, 8):
        draw.line((gx + i * gw / 8, gy, gx + i * gw / 8, gy + gh), fill="#CFDCDD", width=1)
    for j in range(1, 4):
        draw.line((gx, gy + j * gh / 4, gx + gw, gy + j * gh / 4), fill="#CFDCDD", width=1)
    # Carrier facing east.
    ship = [(gx + 160, gy + 78), (gx + 430, gy + 66), (gx + 510, gy + 92),
            (gx + 430, gy + 122), (gx + 160, gy + 112)]
    draw.polygon(ship, fill="#6F8994", outline=BLUE)
    draw.rounded_rectangle((gx + 215, gy + 70, gx + 405, gy + 108), 10, fill=PALE_WARM, outline=AMBER)
    draw.ellipse((gx + 455, gy + 84, gx + 470, gy + 110), fill=TEAL)
    txt(draw, (gx + 462, gy + 78), "Z", F_TINY, TEAL, anchor="ms")
    # Two public routes east, narrow near-defense lane, and dive threat.
    arrow(draw, (gx + 510, gy + 78), (gx + 642, gy + 38), color=TEAL, width=6, head=14)
    arrow(draw, (gx + 510, gy + 111), (gx + 642, gy + 151), color=INDIGO, width=6, head=14)
    txt(draw, (gx + 598, gy + 18), "东向航路 A", F_TINY, TEAL, anchor="mm")
    txt(draw, (gx + 598, gy + 174), "东向航路 B", F_TINY, INDIGO, anchor="mm")
    draw.arc((gx + 115, gy + 35, gx + 520, gy + 155), 205, 335, fill=AMBER, width=5)
    txt(draw, (gx + 290, gy + 158), "近防窄航道", F_TINY, AMBER, anchor="mm")
    arrow(draw, (gx + 390, gy - 8), (gx + 405, gy + 52), color=RED, width=6, head=14)
    txt(draw, (gx + 390, gy + 4), "前厅俯冲威胁轴", F_TINY, RED, anchor="ms")
    txt(draw, (x0 + 24, y0 + 276), "只验证占地、舰首站位与两条公开路线；不是最终 Sprite。", F_TINY, MUTED)


def draw_c02(draw, box):
    x0, y0, _, _ = box
    # Heavy-duty road and continuous cradle.
    road_y = y0 + 262
    draw.rectangle((x0 + 24, road_y - 22, x0 + 680, road_y + 20), fill="#9B9A94")
    for x in range(x0 + 40, x0 + 660, 68):
        draw.line((x, road_y - 2, x + 28, road_y - 2), fill="#E9DCA9", width=4)
    # Ship side profile.
    sx, sy = x0 + 160, y0 + 92
    draw.polygon([(sx, sy + 30), (sx + 400, sy + 20), (sx + 485, sy + 58),
                  (sx + 425, sy + 120), (sx + 45, sy + 120), (sx, sy + 78)],
                 fill="#78939E", outline=BLUE)
    draw.rounded_rectangle((sx + 52, sy, sx + 360, sy + 64), 15, fill=PALE_WARM, outline=AMBER, width=3)
    # Continuous shipyard cradle and support points.
    draw.rectangle((sx + 32, sy + 120, sx + 438, sy + 150), fill="#4F5F66")
    for cx in (sx + 65, sx + 165, sx + 265, sx + 365):
        draw.polygon([(cx, sy + 150), (cx + 32, sy + 150), (cx + 42, road_y - 22), (cx - 10, road_y - 22)],
                     fill="#687980", outline=INK)
    # Tug convoy.
    for tx in (x0 + 42, x0 + 86):
        draw.rectangle((tx, road_y - 48, tx + 34, road_y - 20), fill="#C9754F", outline=INK)
        draw.ellipse((tx + 3, road_y - 26, tx + 12, road_y - 17), fill=INK)
        draw.ellipse((tx + 22, road_y - 26, tx + 31, road_y - 17), fill=INK)
    arrow(draw, (x0 + 128, road_y - 40), (sx - 5, road_y - 40), color=AMBER, width=5, head=12)
    txt(draw, (x0 + 32, y0 + 65), "连续重载托架 / 船台承重", F_SMALL, BLUE)
    arrow(draw, (x0 + 220, y0 + 72), (sx + 210, sy + 142), color=BLUE, width=3, head=9)
    txt(draw, (x0 + 430, y0 + 188), "宽侧承力面", F_SMALL, TEAL)
    arrow(draw, (x0 + 512, y0 + 182), (sx + 420, sy + 105), color=TEAL, width=3, head=9)
    txt(draw, (x0 + 26, y0 + 292), "地面车队沿承重作业道低速牵引；与 C01 空中形态是同一舰体。", F_TINY, MUTED)


def draw_decision(draw, box):
    x0, y0, x1, _ = box
    txt(draw, (x0 + 28, y0 + 82), "请只回答一个选择：", F_BODY, MUTED)
    txt(draw, ((x0 + x1) // 2, y0 + 132), "A / B / C，或三案全部退回？", font(35), INK, anchor="mm", stroke=1)
    checks = [
        "固定馆 → 巡展舰结构连续性成立",
        "低矮比例、18m 馆守Z与城市尺度成立",
        "“公共博物馆 / 老式巡展机械”的比重合适",
    ]
    for i, label in enumerate(checks):
        cy = y0 + 181 + i * 34
        draw.rounded_rectangle((x0 + 38, cy - 9, x0 + 56, cy + 9), 3, outline=TEAL, width=2)
        txt(draw, (x0 + 70, cy), label, F_SMALL, INK, anchor="lm")
    txt(draw, ((x0 + x1) // 2, y0 + 292),
        "Candidate · user=false · runtime=false · Canon 未晋级 · 未接 Godot",
        F_TINY, RED, anchor="mm", stroke=1)


def main():
    raw = Image.open(RAW).convert("RGB")
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    txt(draw, (54, 58), "万机馆｜Current Reader 结构轮廓用户确认板", F_TITLE, INK, anchor="lm", stroke=1)
    txt(draw, (55, 111), "固定展馆与低空巡展母舰必须是同一座馆｜同视角 · 同比例 · 同信息密度｜130–160m 长 / 35–45m 高", F_SUB, MUTED, anchor="lm")
    pill(draw, (2030, 38, 2346, 83), "SECTION 2 · CALL 01", BLUE)
    txt(draw, (2345, 112), "只比较结构，不以材质精度诱导选择", F_SMALL, RED, anchor="rs")

    columns = [
        (50, 150, 770, 1018, "A  连续拱壳", TEAL,
         (0, 55, 520, 480), (0, 445, 530, 1024),
         "展厅首读最强｜馆/舰整体性最高｜连续大跨屋盖"),
        (840, 150, 1560, 1018, "B  双廊中庭", AMBER,
         (465, 55, 1045, 480), (440, 435, 1055, 1024),
         "公共动线最清楚｜B1 脊柱直观｜模块维护性高"),
        (1630, 150, 2350, 1018, "C  层叠平台", INDIGO,
         (970, 55, 1536, 480), (930, 435, 1536, 1024),
         "城市公共性强｜非对称旧修补感｜前甲板最突出"),
    ]

    for x0, y0, x1, y1, label, accent, fixed_crop, ship_crop, note in columns:
        draw.rounded_rectangle((x0, y0, x1, y1), 24, fill=PAPER, outline=accent, width=3)
        draw.rounded_rectangle((x0, y0, x1, y0 + 62), 24, fill=accent)
        draw.rectangle((x0, y0 + 30, x1, y0 + 62), fill=accent)
        txt(draw, ((x0 + x1) // 2, y0 + 32), label, F_COL, "white", anchor="mm", stroke=1)
        paste_contain(canvas, raw, fixed_crop, (x0 + 18, y0 + 72, x1 - 18, y0 + 420))
        pill(draw, (x0 + 25, y0 + 78, x0 + 137, y0 + 116), "固定馆", accent)
        draw.line((x0 + 24, y0 + 431, x1 - 24, y0 + 431), fill=LINE, width=2)
        paste_contain(canvas, raw, ship_crop, (x0 + 18, y0 + 442, x1 - 18, y0 + 790))
        pill(draw, (x0 + 25, y0 + 449, x0 + 155, y0 + 487), "巡展舰", accent)
        draw.rounded_rectangle((x0 + 22, y0 + 805, x1 - 22, y1 - 18), 14, fill="#F2F4F2")
        txt(draw, ((x0 + x1) // 2, y0 + 842), note, F_SMALL, accent, anchor="mm", stroke=1)
        txt(draw, ((x0 + x1) // 2, y0 + 879), "公共展馆先读；低空承力舰体后读", F_TINY, MUTED, anchor="mm")

    draw.line((55, 1055, 2345, 1055), fill=LINE, width=3)
    txt(draw, (55, 1082), "共同硬约束验证（不随 A/B/C 改变）", F_HEAD, INK, anchor="lm", stroke=1)

    p1 = (50, 1110, 790, 1408)
    p2 = (815, 1110, 1535, 1408)
    p3 = (1560, 1110, 2350, 1408)
    p4 = (50, 1432, 790, 1748)
    p5 = (815, 1432, 1535, 1748)
    p6 = (1560, 1432, 2350, 1748)
    panel(draw, p1, "三态连续性｜固定馆 → 离地 → 巡展舰", TEAL)
    panel(draw, p2, "侧视 + 顶视｜展陈、机库与承力分层", AMBER)
    panel(draw, p3, "统一尺度带｜同一比例，不靠气势偷尺寸", INDIGO)
    panel(draw, p4, "C01E04 盘面投影｜舰首朝东 / 外海", TEAL)
    panel(draw, p5, "C02 船台最小示意｜连续托架 / 地面牵引", AMBER)
    panel(draw, p6, "用户停止门｜选轮廓后才进入材质与实机", RED)
    draw_transition(draw, p1)
    draw_layers(draw, p2)
    draw_scale(draw, p3)
    draw_e04(draw, p4)
    draw_c02(draw, p5)
    draw_decision(draw, p6)

    txt(draw, (55, 1780), "禁止：履带堡垒 / 军事战列舰 / 小宫殿粘底盘 / 人形变形 / 巨炮 / 无限机库门", F_TINY, MUTED, anchor="lm")
    txt(draw, (2345, 1780), "视觉源：Section 2 单次 ImageGen；无旧 History 舰图输入；无 reroll", F_TINY, MUTED, anchor="rm")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT, optimize=True)
    canvas.resize((1200, 900), Image.Resampling.LANCZOS).save(OUT_HALF, optimize=True)
    print(OUT)
    print(OUT_HALF)


if __name__ == "__main__":
    main()
