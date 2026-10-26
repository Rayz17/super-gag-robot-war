from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "generation-raw" / "WANJI_C_DERIVED_MOBILE_FORTRESS_IMAGEGEN_CALL01_RAW.png"
OUT = ROOT / "delivery" / "WANJI_C_DERIVED_MOBILE_FORTRESS_USER_CONFIRMATION_BOARD_2400x1800.png"
OUT_HALF = ROOT / "delivery" / "WANJI_C_DERIVED_MOBILE_FORTRESS_USER_CONFIRMATION_BOARD_1200x900.png"

W, H = 2400, 1800
BG = "#F2EFE8"
PAPER = "#FBFAF6"
INK = "#202B32"
MUTED = "#657078"
LINE = "#C8CECF"
TEAL = "#356F70"
BLUE = "#315D78"
INDIGO = "#56669A"
AMBER = "#B8752D"
RED = "#A64A42"
GREEN = "#4D7D65"
PALE_TEAL = "#D6E5E2"
PALE_BLUE = "#D7E3E9"
PALE_AMBER = "#EADDC4"
PALE_RED = "#EBD8D4"
STEEL = "#4B6572"
STEEL_DARK = "#2E4653"
CREAM = "#E7D7B6"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font(size):
    return ImageFont.truetype(FONT_PATH, size=size)


F_TITLE = font(52)
F_SUB = font(25)
F_PANEL = font(31)
F_HEAD = font(27)
F_BODY = font(22)
F_SMALL = font(18)
F_TINY = font(15)


def txt(draw, xy, s, f=F_BODY, fill=INK, anchor=None, stroke=0):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor,
              stroke_width=stroke, stroke_fill=fill)


def wrapped(draw, box, s, f=F_BODY, fill=INK, spacing=8):
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
    txt(draw, (x0 + 22, y0 + 28), title, F_PANEL, "white", anchor="lm", stroke=1)


def badge(draw, box, label, fill):
    draw.rounded_rectangle(box, radius=16, fill=fill)
    txt(draw, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2),
        label, F_SMALL, "white", anchor="mm", stroke=1)


def paste_crop(canvas, source, crop, box, fill="#F8F5EE"):
    x0, y0, x1, y1 = box
    canvas.paste(fill, (x0, y0, x1, y1))
    frag = source.crop(crop)
    fitted = ImageOps.contain(frag, (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    px = x0 + (x1 - x0 - fitted.width) // 2
    py = y0 + (y1 - y0 - fitted.height) // 2
    canvas.paste(fitted, (px, py))


def arrow(draw, start, end, color=TEAL, width=4, head=12):
    x0, y0 = start
    x1, y1 = end
    draw.line((x0, y0, x1, y1), fill=color, width=width)
    if abs(x1 - x0) > abs(y1 - y0):
        sign = 1 if x1 > x0 else -1
        pts = [(x1, y1), (x1 - sign * head, y1 - head * .62),
               (x1 - sign * head, y1 + head * .62)]
    else:
        sign = 1 if y1 > y0 else -1
        pts = [(x1, y1), (x1 - head * .62, y1 - sign * head),
               (x1 + head * .62, y1 - sign * head)]
    draw.polygon(pts, fill=color)


def structure_icon(draw, x, y, w, h):
    # Same four masses as the generated proposal, simplified for producer reading.
    draw.rounded_rectangle((x + w * .20, y, x + w * .80, y + h * .22),
                           14, fill=CREAM, outline=AMBER, width=3)
    draw.polygon([(x + w * .44, y + h * .20), (x + w * .56, y + h * .20),
                  (x + w * .62, y + h), (x + w * .38, y + h)],
                 fill=STEEL_DARK, outline=BLUE)
    draw.rounded_rectangle((x, y + h * .24, x + w * .34, y + h * .89),
                           18, fill=STEEL, outline=BLUE, width=3)
    draw.rounded_rectangle((x + w * .66, y + h * .24, x + w, y + h * .89),
                           18, fill=STEEL, outline=BLUE, width=3)
    draw.ellipse((x + w * .80, y + h * .03, x + w * 1.03, y + h * .25),
                 fill="#6F5B4B", outline=AMBER, width=3)


def guardian(draw, x, base_y, height, color=TEAL):
    head = max(8, int(height * .16))
    body_top = base_y - height + head
    draw.ellipse((x - head / 2, base_y - height, x + head / 2,
                  base_y - height + head), fill=color)
    draw.polygon([(x - head * .7, body_top), (x + head * .7, body_top),
                  (x + head * .55, base_y - height * .40),
                  (x - head * .55, base_y - height * .40)], fill=color)
    draw.line((x - head * .3, base_y - height * .42, x - head * .65, base_y),
              fill=color, width=max(5, int(height * .08)))
    draw.line((x + head * .3, base_y - height * .42, x + head * .65, base_y),
              fill=color, width=max(5, int(height * .08)))
    draw.line((x - head * .62, body_top + height * .13, x - head * 1.05,
               base_y - height * .35), fill=color, width=max(5, int(height * .07)))
    draw.line((x + head * .62, body_top + height * .13, x + head * 1.05,
               base_y - height * .35), fill=color, width=max(5, int(height * .07)))


def ship_profile(draw, x, y, length, height, accent):
    # A deliberately low orthographic interpretation of the same proposal.
    crown_h = height * .29
    belly_h = height * .71
    draw.polygon([(x, y + crown_h * .83), (x + length * .14, y + crown_h * .16),
                  (x + length * .63, y), (x + length * .82, y + crown_h * .25),
                  (x + length, y + crown_h * .74), (x + length * .94, y + crown_h),
                  (x + length * .06, y + crown_h)], fill=CREAM, outline=AMBER)
    draw.polygon([(x + length * .04, y + crown_h),
                  (x + length * .94, y + crown_h),
                  (x + length * .84, y + crown_h + belly_h * .80),
                  (x + length * .60, y + height),
                  (x + length * .19, y + height * .95),
                  (x, y + height * .70)], fill=STEEL, outline=accent)
    draw.polygon([(x + length * .39, y + crown_h),
                  (x + length * .57, y + crown_h),
                  (x + length * .62, y + height),
                  (x + length * .43, y + height)], fill=STEEL_DARK)
    draw.ellipse((x + length * .85, y + crown_h * .78,
                  x + length * .99, y + crown_h + height * .16),
                 fill="#6E5C4B", outline=AMBER, width=2)


def checkrow(draw, x, y, text, color=GREEN):
    draw.rounded_rectangle((x, y, x + 23, y + 23), radius=5, outline=color, width=3)
    draw.line((x + 5, y + 12, x + 10, y + 18, x + 20, y + 5), fill=color, width=3)
    txt(draw, (x + 36, y + 11), text, F_SMALL, INK, anchor="lm")


canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)
raw = Image.open(RAW).convert("RGB")

# Header
txt(draw, (52, 38), "万机馆｜C 路线深化：移动堡垒 / 可变结构确认板", F_TITLE, INK)
txt(draw, (55, 106),
    "一套构型・三个读法｜地表公共馆仅占约 1/3，地下旧巡展身体约 2/3+｜本轮只裁决构型与尺度",
    F_SUB, MUTED)
badge(draw, (1995, 34, 2345, 86), "SECTION 2  ・  CALL 01", BLUE)
txt(draw, (2170, 112), "1 次 ImageGen ・ 0 reroll", F_SMALL, RED, anchor="mm")

# Top art readings
panel(draw, (50, 150, 770, 1050), "01  固定馆剖面：地下才是真身体", TEAL)
paste_crop(canvas, raw, (0, 35, 515, 1024), (68, 220, 752, 900))
badge(draw, (86, 910, 286, 952), "地上约 1/3", AMBER)
badge(draw, (298, 910, 514, 952), "地下约 2/3+", BLUE)
wrapped(draw, (86, 966, 740, 1036),
        "公共前厅、展窗、屋盖还在城市尺度；中央深龙骨、左右机库/收藏承力舱与航行炉完整埋于地下。",
        F_SMALL, MUTED, 5)

panel(draw, (790, 150, 1830, 1050), "02  巡展舰态：展馆冠部 + 完整移动堡垒", BLUE)
paste_crop(canvas, raw, (490, 38, 1135, 1024), (810, 220, 1810, 914))
badge(draw, (824, 920, 1050, 962), "3–5 个主体量", TEAL)
badge(draw, (1063, 920, 1328, 962), "双侧巨型舱体", BLUE)
badge(draw, (1342, 920, 1595, 962), "中央承力龙骨", INDIGO)
badge(draw, (1608, 920, 1792, 962), "旧推进环", AMBER)
wrapped(draw, (824, 978, 1798, 1035),
        "规则化大结构代替“展馆粘薄底盘”；前场是外部泊位/前甲板，不是现代航母跑道。",
        F_SMALL, MUTED, 4)

panel(draw, (1850, 150, 2350, 1050), "03  可变潜力：只显示结构语法", AMBER)
paste_crop(canvas, raw, (1190, 10, 1536, 1024), (1870, 220, 2330, 882))
wrapped(draw, (1880, 910, 2322, 1032),
        "大分缝、侧舱转轴、中央脊与锁止环，可预示“航行 / 展开作业堡垒 / 未来完整形态”。不画人形，不宣布未定变形。",
        F_SMALL, MUTED, 5)

# Bottom left: structural interpretation
panel(draw, (50, 1080, 790, 1742), "构型首读｜这一轮实际解决了什么", TEAL)
structure_icon(draw, 82, 1170, 275, 285)
txt(draw, (390, 1172), "A  公共博物馆冠部", F_HEAD, AMBER)
wrapped(draw, (390, 1210, 756, 1270), "层叠屋盖、暖色窗带、公共入口与前场。", F_SMALL, MUTED, 4)
txt(draw, (390, 1280), "B  中央深龙骨 / 航行炉", F_HEAD, BLUE)
wrapped(draw, (390, 1318, 756, 1378), "它承担自动航行、承力与上下层连续。", F_SMALL, MUTED, 4)
txt(draw, (390, 1388), "C  左右巨型舱体", F_HEAD, INDIGO)
wrapped(draw, (390, 1426, 756, 1486), "收藏承力舱、B1 机库脊柱与有限重修位。", F_SMALL, MUTED, 4)
draw.line((75, 1515, 765, 1515), fill=LINE, width=2)
checkrow(draw, 82, 1542, "不再是“展馆从地下拔起 + 薄底盘”")
checkrow(draw, 82, 1586, "大块面转轴可追踪，不靠密集小零件")
checkrow(draw, 82, 1630, "公共博物馆读感没有被军舰外壳吞掉")
txt(draw, (82, 1694), "注：生成透视用来判断体量关系，不是最终侧视尺寸图。", F_TINY, RED)

# Bottom middle: scale decision band
panel(draw, (810, 1080, 1625, 1742), "尺度决策带｜同一构型，不同整舰容量", BLUE)
txt(draw, (842, 1160), "S  保留现行约 160m 上限", F_HEAD, TEAL)
ship_profile(draw, 850, 1205, 490, 142, TEAL)
guardian(draw, 1390, 1347, 55, TEAL)
draw.line((850, 1362, 1340, 1362), fill=INK, width=2)
txt(draw, (1095, 1370), "约160m", F_TINY, MUTED, anchor="ma")
txt(draw, (1390, 1370), "馆守Z 18m", F_TINY, MUTED, anchor="ma")
wrapped(draw, (850, 1407, 1592, 1465),
        "好处：不迁移现行尺度。代价：深舰腹必须收敛，机库/生活/收藏容量更紧。",
        F_SMALL, MUTED, 4)
draw.line((840, 1482, 1595, 1482), fill=LINE, width=2)
txt(draw, (842, 1514), "L  约 230m 移动堡垒（非 Canon 候选）", F_HEAD, INDIGO)
ship_profile(draw, 850, 1555, 690, 142, INDIGO)
guardian(draw, 1570, 1697, 55, TEAL)
draw.line((850, 1710, 1540, 1710), fill=INK, width=2)
txt(draw, (1195, 1717), "约230m｜高度与泊位需后续迁移", F_TINY, MUTED, anchor="ms")
txt(draw, (1570, 1717), "18m", F_TINY, MUTED, anchor="ms")

# Bottom right: user gate
panel(draw, (1645, 1080, 2350, 1742), "用户视觉门｜本轮只需裁决 3 件事", RED)
badge(draw, (1680, 1162, 2315, 1220), "C 路线新主体是否成立？", RED)
for num, yy, head, body in [
    ("1", 1260, "构型", "层叠公共馆 + 中央深龙骨 + 左右巨型舱体，是否像“移动机器人文化堡垒”？"),
    ("2", 1395, "尺度", "选 S：保留约160m并收敛舰腹；或选 L：将约230m作为尺度迁移候选？"),
    ("3", 1530, "可变语法", "保留侧舱转轴/中央脊/锁止环的潜力提示，还是返回轮廓层？"),
]:
    draw.ellipse((1680, yy, 1726, yy + 46), fill=BLUE if num != "3" else AMBER)
    txt(draw, (1703, yy + 23), num, F_HEAD, "white", anchor="mm", stroke=1)
    txt(draw, (1744, yy + 4), head, F_HEAD, INK)
    wrapped(draw, (1744, yy + 43, 2315, yy + 122), body, F_SMALL, MUTED, 5)

draw.rounded_rectangle((1680, 1668, 2315, 1718), radius=14, fill=PALE_RED)
txt(draw, (1997, 1693),
    "Candidate ・ user=false ・ runtime=false ・ Canon 未迁移 ・ 未接 Godot",
    F_SMALL, RED, anchor="mm", stroke=1)

txt(draw, (55, 1770),
    "禁止误读：薄飞行平板 / 现代航母跑道 / 战列舰炮塔 / 履带底盘 / 展馆直接粘上舰 / 提前画出人形变形",
    F_TINY, MUTED)
txt(draw, (2345, 1770), "Art Asset Section 2 ・ single built-in ImageGen call ・ 0 reroll", F_TINY, MUTED, anchor="ra")

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, optimize=True)
canvas.resize((W // 2, H // 2), Image.Resampling.LANCZOS).save(OUT_HALF, optimize=True)
