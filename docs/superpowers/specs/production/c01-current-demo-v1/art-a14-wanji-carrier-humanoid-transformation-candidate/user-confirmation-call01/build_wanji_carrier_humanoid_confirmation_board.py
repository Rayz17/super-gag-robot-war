from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "generation-raw" / "WANJI_CARRIER_TO_HUMANOID_IMAGEGEN_CALL01_RAW.png"
OUT = ROOT / "delivery" / "WANJI_CARRIER_TO_HUMANOID_USER_CONFIRMATION_BOARD_2400x1800.png"
OUT_HALF = ROOT / "delivery" / "WANJI_CARRIER_TO_HUMANOID_USER_CONFIRMATION_BOARD_1200x900.png"

W, H = 2400, 1800
BG = "#F2EFE8"
PAPER = "#FBFAF6"
INK = "#202A31"
MUTED = "#657078"
LINE = "#C9CECE"
TEAL = "#367574"
BLUE = "#315E78"
INDIGO = "#58669B"
AMBER = "#B8772F"
RED = "#AA4C43"
GREEN = "#4A7B62"
PALE_BLUE = "#D8E5E9"
PALE_TEAL = "#D7E6E2"
PALE_AMBER = "#EADCC1"
PALE_RED = "#EBD8D3"
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font(size):
    return ImageFont.truetype(FONT_PATH, size=size)


F_TITLE = font(51)
F_SUB = font(24)
F_PANEL = font(30)
F_HEAD = font(25)
F_BODY = font(21)
F_SMALL = font(18)
F_TINY = font(15)


def txt(draw, xy, s, f=F_BODY, fill=INK, anchor=None, stroke=0):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor,
              stroke_width=stroke, stroke_fill=fill)


def wrapped(draw, box, s, f=F_BODY, fill=INK, spacing=7):
    x0, y0, x1, _ = box
    lines = []
    current = ""
    for ch in s:
        if ch == "\n":
            lines.append(current)
            current = ""
            continue
        candidate = current + ch
        if draw.textbbox((0, 0), candidate, font=f)[2] > x1 - x0 and current:
            lines.append(current)
            current = ch
        else:
            current = candidate
    if current:
        lines.append(current)
    y = y0
    line_h = draw.textbbox((0, 0), "国Ag", font=f)[3] + spacing
    for line in lines:
        draw.text((x0, y), line, font=f, fill=fill)
        y += line_h
    return y


def panel(draw, box, title, accent):
    draw.rounded_rectangle(box, radius=22, fill=PAPER, outline=LINE, width=2)
    x0, y0, x1, _ = box
    draw.rounded_rectangle((x0, y0, x1, y0 + 56), radius=22, fill=accent)
    draw.rectangle((x0, y0 + 28, x1, y0 + 56), fill=accent)
    txt(draw, (x0 + 20, y0 + 28), title, F_PANEL, "white", anchor="lm", stroke=1)


def badge(draw, box, label, fill):
    draw.rounded_rectangle(box, radius=15, fill=fill)
    txt(draw, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2),
        label, F_SMALL, "white", anchor="mm", stroke=1)


def paste_crop(canvas, source, crop, box, fill="#F9F6EF"):
    x0, y0, x1, y1 = box
    canvas.paste(fill, (x0, y0, x1, y1))
    frag = source.crop(crop)
    fitted = ImageOps.contain(frag, (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    px = x0 + (x1 - x0 - fitted.width) // 2
    py = y0 + (y1 - y0 - fitted.height) // 2
    canvas.paste(fitted, (px, py))


def arrow(draw, start, end, color=TEAL, width=5, head=14):
    x0, y0 = start
    x1, y1 = end
    draw.line((x0, y0, x1, y1), fill=color, width=width)
    if abs(x1 - x0) >= abs(y1 - y0):
        sign = 1 if x1 >= x0 else -1
        pts = [(x1, y1), (x1 - sign * head, y1 - head * .62),
               (x1 - sign * head, y1 + head * .62)]
    else:
        sign = 1 if y1 >= y0 else -1
        pts = [(x1, y1), (x1 - head * .62, y1 - sign * head),
               (x1 + head * .62, y1 - sign * head)]
    draw.polygon(pts, fill=color)


def mapping_row(draw, y, source, target, accent, note):
    draw.rounded_rectangle((78, y, 420, y + 46), radius=11, fill=accent)
    txt(draw, (249, y + 23), source, F_SMALL, "white", anchor="mm", stroke=1)
    arrow(draw, (438, y + 23), (520, y + 23), accent, 4, 11)
    draw.rounded_rectangle((536, y, 845, y + 46), radius=11,
                           fill="#EEF1EF", outline=accent, width=2)
    txt(draw, (690, y + 23), target, F_SMALL, INK, anchor="mm")
    txt(draw, (870, y + 23), note, F_TINY, MUTED, anchor="lm")


def number_item(draw, x, y, n, head, body, accent=BLUE):
    draw.ellipse((x, y, x + 46, y + 46), fill=accent)
    txt(draw, (x + 23, y + 23), str(n), F_HEAD, "white", anchor="mm", stroke=1)
    txt(draw, (x + 64, y + 2), head, F_HEAD, INK)
    wrapped(draw, (x + 64, y + 38, x + 530, y + 115), body, F_SMALL, MUTED, 5)


canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)
raw = Image.open(RAW).convert("RGB")

# Header
txt(draw, (52, 38), "万机馆｜巡展舰 → 未来人形巨机 变形关系确认板", F_TITLE, INK)
txt(draw, (54, 105),
    "C01 只使用第一形态｜第二形态仅为后续故事 Candidate｜本板只验证轮廓、部件映射与同体性",
    F_SUB, MUTED)
badge(draw, (1996, 34, 2345, 86), "SECTION 2  ・  CALL 01", BLUE)
txt(draw, (2170, 112), "1 次 ImageGen ・ 0 reroll ・ 无图像输入", F_SMALL, RED, anchor="mm")

# One coherent raw sheet; do not crop its stages into misleading fragments.
panel(draw, (50, 150, 2350, 1300), "同一主体｜第一形态 → 承力骨架重组 → 第二形态", BLUE)
paste_crop(canvas, raw, (0, 0, 1536, 1024), (70, 220, 2330, 1282))

# On-art boundary labels occupy the generated negative space.
badge(draw, (92, 247, 392, 300), "01  C01 第一形态", GREEN)
wrapped(draw, (92, 318, 420, 410),
        "低矮巡展舰 / 移动堡垒\n当前 Reader 只到这里",
        F_SMALL, GREEN, 5)
arrow(draw, (290, 430), (570, 810), GREEN, 5, 14)

badge(draw, (955, 250, 1438, 303), "02  同一承力骨架重组", BLUE)
wrapped(draw, (1010, 320, 1415, 410),
        "前舰体展肩臂\n后舰体下放腿足\n中央龙骨立成躯干",
        F_SMALL, BLUE, 4)

badge(draw, (1960, 247, 2308, 300), "03  未来第二形态", RED)
wrapped(draw, (2010, 318, 2298, 420),
        "完整人形巨机\n只是后续故事 Candidate",
        F_SMALL, RED, 5)
arrow(draw, (2080, 440), (1890, 650), RED, 5, 14)

# Carrier direction and stage boundary receipts.
draw.rounded_rectangle((155, 1178, 782, 1248), radius=15, fill=PAPER, outline=TEAL, width=2)
badge(draw, (174, 1192, 356, 1235), "馆守Z 18m 尺度锚", TEAL)
txt(draw, (506, 1201), "舰首 / 向右航行", F_SMALL, AMBER, anchor="mm")
arrow(draw, (430, 1228), (742, 1228), AMBER, 5, 15)

draw.rounded_rectangle((868, 1180, 1532, 1248), radius=15, fill=PAPER, outline=BLUE, width=2)
txt(draw, (1200, 1214),
    "胸 / 头 / 肩髋轴连续清楚；腿部藏纳仍待正投影拆分",
    F_SMALL, BLUE, anchor="mm")

draw.rounded_rectangle((1660, 1178, 2265, 1248), radius=15, fill=PAPER, outline=RED, width=2)
badge(draw, (1678, 1192, 1880, 1235), "Future Candidate", RED)
txt(draw, (2063, 1214), "解锁章节 / 尺度 / 能力均未定", F_SMALL, MUTED, anchor="mm")

# Compact mapping table.
panel(draw, (50, 1330, 1425, 1743), "部件连续性｜舰态大块在人形中的去向", BLUE)
left_rows = [
    ("\u8230首 / \u524d甲板", "\u80f8甲 / \u80f8骨", AMBER),
    ("\u524d部左右舰体", "\u80a9 / \u81c2 / \u624b", BLUE),
    ("\u540e部左右舰体", "\u9acb / \u817f / \u811a", INDIGO),
    ("\u4e2d央龙骨", "\u810a柱 / \u8179 / \u9aa8盆", TEAL),
]
right_rows = [
    ("\u5bfc航冠部密封舱", "\u5934 / \u9888", AMBER),
    ("\u516c共展馆屋盖 / \u7a97带", "\u4e0a胸 / \u80a9梁 / \u4e0a背", GREEN),
    ("\u8230尾循环 / \u63a8进块", "\u80cc包 / \u59ff态稳定", RED),
]
for i, (source, target, accent) in enumerate(left_rows):
    yy = 1410 + i * 66
    draw.rounded_rectangle((78, yy, 360, yy + 43), radius=10, fill=accent)
    txt(draw, (219, yy + 22), source, F_TINY, "white", anchor="mm", stroke=1)
    arrow(draw, (376, yy + 22), (430, yy + 22), accent, 3, 9)
    draw.rounded_rectangle((444, yy, 650, yy + 43), radius=10, fill="#EEF1EF", outline=accent, width=2)
    txt(draw, (547, yy + 22), target, F_TINY, INK, anchor="mm")
for i, (source, target, accent) in enumerate(right_rows):
    yy = 1410 + i * 66
    draw.rounded_rectangle((720, yy, 1060, yy + 43), radius=10, fill=accent)
    txt(draw, (890, yy + 22), source, F_TINY, "white", anchor="mm", stroke=1)
    arrow(draw, (1074, yy + 22), (1128, yy + 22), accent, 3, 9)
    draw.rounded_rectangle((1142, yy, 1396, yy + 43), radius=10, fill="#EEF1EF", outline=accent, width=2)
    txt(draw, (1269, yy + 22), target, F_TINY, INK, anchor="mm")
draw.rounded_rectangle((720, 1612, 1396, 1709), radius=14, fill=PALE_AMBER)
wrapped(draw, (742, 1627, 1374, 1698),
        "首读结论：不是展馆挂竖筒，也不是侧舱打开就算变形。\n开口：腿部如何在舰底前后段收折，尚未达工程定型。",
        F_SMALL, AMBER, 4)

# Exact user gate.
panel(draw, (1445, 1330, 2350, 1743), "用户视觉门｜三项分开裁决", RED)
number_item(draw, 1478, 1404, 1, "舰态轮廓",
            "舰首/航向、低矮移动堡垒、巨大下层主体是否成立？")
number_item(draw, 1478, 1514, 2, "人形身份",
            "头胸与全身比例是否足够像万机馆独有的第二形态？",
            AMBER)
number_item(draw, 1478, 1624, 3, "同体映射",
            "舰首→胸、前舰体→臂、后舰体→腿、龙骨→躯干是否可信？",
            INDIGO)
draw.rounded_rectangle((2032, 1394, 2318, 1708), radius=16, fill="#F4E9E5", outline=RED, width=2)
txt(draw, (2175, 1427), "建议回复", F_HEAD, RED, anchor="mm")
wrapped(draw, (2060, 1470, 2295, 1678),
        "舰态：\n通过 / 退回\n\n人形：\n通过 / 退回\n\n映射：\n通过 / 需补拆分",
        F_SMALL, RED, 6)

txt(draw, (55, 1770),
    "Candidate ・ user=false ・ runtime=false ・ Canon 未迁移 ・ 未接 Godot ・ A13 RETURN 未作为正向图像输入",
    F_TINY, MUTED)
txt(draw, (2345, 1770), "Art Asset Section 2 ・ single built-in ImageGen call ・ 0 reroll", F_TINY, MUTED, anchor="ra")

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, optimize=True)
canvas.resize((W // 2, H // 2), Image.Resampling.LANCZOS).save(OUT_HALF, optimize=True)
