from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png"
OUT = ROOT / "user-confirmation-call01/TRUE_RETIRED_HEAVY_SHIELD_CALL01_USER_CONFIRMATION_BOARD_2400x1800.png"
OUT_HALF = ROOT / "user-confirmation-call01/qa/TRUE_RETIRED_HEAVY_SHIELD_CALL01_USER_CONFIRMATION_BOARD_1200x900.png"
RAW_HALF = ROOT / "user-confirmation-call01/qa/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW_50PCT.png"
WHITE_COMPOSITE = ROOT / "user-confirmation-call01/qa/TRUE_RETIRED_HEAVY_SHIELD_CALL01_ALPHA_WHITE_COMPOSITE.png"

FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, light: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_LIGHT if light else FONT_MEDIUM, size=size)


def fit_image(im: Image.Image, box: tuple[int, int]) -> Image.Image:
    copy = im.copy()
    copy.thumbnail(box, Image.Resampling.LANCZOS)
    return copy


def draw_lines(draw: ImageDraw.ImageDraw, xy: tuple[int, int], lines: list[str],
               fnt: ImageFont.FreeTypeFont, fill: str, gap: int) -> int:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def checkerboard(size: tuple[int, int], cell: int = 40) -> Image.Image:
    bg = Image.new("RGB", size, "#E8E7E3")
    d = ImageDraw.Draw(bg)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#D8D7D2")
    return bg


raw = Image.open(RAW).convert("RGBA")
alpha = raw.getchannel("A")
alpha_min, alpha_max = alpha.getextrema()
if alpha_min != 0 or alpha_max == 0:
    raise RuntimeError(f"alpha gate failed: extrema={(alpha_min, alpha_max)}")

canvas = Image.new("RGB", (2400, 1800), "#EEECE6")
draw = ImageDraw.Draw(canvas)

draw.rectangle((0, 0, 2400, 132), fill="#242A2A")
draw.text((62, 24), "A17｜退役重盾：双手承力与横拍结构确认", font=font(54), fill="#F7F2E7")
draw.text((1900, 48), "1 call · 0 reroll", font=font(24, True), fill="#D7CDBE")

image_box = (60, 170, 1710, 1270)
bx, by, br, bb = image_box
panel_bg = checkerboard((br - bx, bb - by), 38)
raw_fit = fit_image(raw, (br - bx - 28, bb - by - 28))
paste_x = bx + ((br - bx) - raw_fit.width) // 2
paste_y = by + ((bb - by) - raw_fit.height) // 2
panel_bg.paste(raw_fit, (paste_x - bx, paste_y - by), raw_fit)
canvas.paste(panel_bg, (bx, by))
draw.rectangle(image_box, outline="#343A39", width=5)
draw.rounded_rectangle((bx + 18, by + 18, bx + 370, by + 66), radius=10, fill="#242A2ADE")
draw.text((bx + 34, by + 26), "完整原图｜透明通道复核", font=font(22), fill="#FFFFFF")

px, py, pw, ph = 1750, 170, 590, 1100
draw.rounded_rectangle((px, py, px + pw, py + ph), radius=22, fill="#FAF8F2", outline="#C8C2B7", width=3)
draw.text((px + 34, py + 30), "50% 制作人首读", font=font(34), fill="#252B2B")
draw.rounded_rectangle((px + 30, py + 86, px + pw - 30, py + 184), radius=16, fill="#DDEBDD")
draw.text((px + 54, py + 108), "PASS（未获用户确认）", font=font(28), fill="#24452D")
draw.text((px + 54, py + 148), "首读是专用重盾，不是装甲板", font=font(21, True), fill="#355B3E")

evidence_y = py + 222
evidence = [
    ("01  盾牌剪影", ["冠部、收尖底部、弧面与厚边", "即使缩小仍一眼是盾"]),
    ("02  双手承力", ["两套独立巨机握把", "前臂轨、中脊与周边承力框连通"]),
    ("03  挡击 / 横拍", ["正面中脊分流，边缘钝厚", "侧面证明可承冲、插地与横拍"]),
    ("04  四次伤痕", ["三道旧的宽浅碎片雨擦压痕", "一道新的赤红热痕，无穿孔"]),
]
for heading, body in evidence:
    draw.text((px + 38, evidence_y), heading, font=font(27), fill="#9D3F31")
    evidence_y += 41
    evidence_y = draw_lines(draw, (px + 44, evidence_y), body, font(21, True), "#424846", 9)
    evidence_y += 22

draw.line((px + 34, py + 855, px + pw - 34, py + 855), fill="#C8C2B7", width=2)
draw.text((px + 38, py + 882), "用户待裁决", font=font(29), fill="#252B2B")
draw_lines(
    draw,
    (px + 44, py + 930),
    ["· 专用重盾的整体形状是否成立", "· 背面双手握持 / 承力是否可信", "· 蓝白老装甲与四道伤痕是否合适"],
    font(22, True),
    "#555B58",
    13,
)

by = 1310
draw.text((60, by), "Reader 动作对应｜同一面盾，不是多个方案", font=font(34), fill="#252B2B")
cards = [
    ("正面分流", ["立于馆守 Z 身前承受赤红冲击，", "将能量沿弧面和厚边向两侧导开。"]),
    ("顶盾改向", ["中脊、前臂轨和周边框连成承力链，", "支持双手推进与插地封路。"]),
    ("双手横拍", ["额外加厚的钝边是真正受力边，", "不是装饰刀刃或藏枪的板件。"]),
]
for i, (heading, body) in enumerate(cards):
    x = 60 + i * 770
    draw.rounded_rectangle((x, by + 60, x + 735, by + 270), radius=18, fill="#FAF8F2", outline="#C8C2B7", width=2)
    draw.text((x + 28, by + 86), heading, font=font(28), fill="#9D3F31")
    draw_lines(draw, (x + 28, by + 137), body, font(22, True), "#3F4543", 12)

draw.rectangle((0, 1660, 2400, 1800), fill="#2C3231")
draw.text((60, 1685), "边界：Candidate · user=false · runtime=false · Canon=false · 未接 Godot", font=font(25), fill="#F4EEE3")
draw.text((60, 1730), "单次 built-in ImageGen · 0 reroll · 未读取 A2 / A13 / A14 旧盾像素 · 未绘制馆守 Z", font=font(22, True), fill="#D7CFC1")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT_HALF.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, quality=96)
canvas.resize((1200, 900), Image.Resampling.LANCZOS).save(OUT_HALF, quality=94)
raw.resize((768, 512), Image.Resampling.LANCZOS).save(RAW_HALF)

white = Image.new("RGBA", raw.size, "white")
white.alpha_composite(raw)
white.convert("RGB").save(WHITE_COMPOSITE, quality=96)

print(f"alpha_extrema={alpha.getextrema()}")
print(OUT)
print(OUT_HALF)
print(RAW_HALF)
print(WHITE_COMPOSITE)
