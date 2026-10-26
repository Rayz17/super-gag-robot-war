from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "user-confirmation-call01/generation-raw/WANJI_A16_C_STYLE_MUSEUM_MEGASTRUCTURE_CALL01_RAW.png"
OUT = ROOT / "user-confirmation-call01/WANJI_A16_C_STYLE_MUSEUM_MEGASTRUCTURE_USER_CONFIRMATION_BOARD_2400x1800.png"
OUT_HALF = ROOT / "user-confirmation-call01/qa/WANJI_A16_C_STYLE_MUSEUM_MEGASTRUCTURE_USER_CONFIRMATION_BOARD_1200x900.png"

FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, light: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_LIGHT if light else FONT_MEDIUM, size=size)


def fit_image(im: Image.Image, box: tuple[int, int]) -> Image.Image:
    copy = im.copy()
    copy.thumbnail(box, Image.Resampling.LANCZOS)
    return copy


def draw_lines(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    lines: list[str],
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    gap: int,
) -> int:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


canvas = Image.new("RGB", (2400, 1800), "#EEECE6")
draw = ImageDraw.Draw(canvas)

# Header
draw.rectangle((0, 0, 2400, 132), fill="#222A2D")
draw.text((62, 24), "A16｜万机馆：C 轮廓语言 × A15 博物馆母体", font=font(50), fill="#F7F2E7")
draw.text((1870, 48), "一次生成 · 0 reroll", font=font(24, True), fill="#D7CDBE")

# Full, uncropped generation
raw = Image.open(RAW).convert("RGB")
raw_fit = fit_image(raw, (1650, 1100))
img_x, img_y = 60, 170
draw.rectangle((img_x - 5, img_y - 5, img_x + raw_fit.width + 5, img_y + raw_fit.height + 5), fill="#343A39")
canvas.paste(raw_fit, (img_x, img_y))
draw.rounded_rectangle((img_x + 18, img_y + 18, img_x + 350, img_y + 66), radius=10, fill="#222A2DE6")
draw.text((img_x + 34, img_y + 26), "完整原图｜未裁切、未重绘", font=font(21), fill="#FFFFFF")

# Right-side audit panel
px, py, pw, ph = 1750, 170, 590, 1100
draw.rounded_rectangle((px, py, px + pw, py + ph), radius=22, fill="#FAF8F2", outline="#C8C2B7", width=3)
draw.text((px + 34, py + 30), "50% 首读门", font=font(36), fill="#252B2B")
draw.rounded_rectangle((px + 30, py + 88, px + pw - 30, py + 190), radius=16, fill="#DDEBDD")
draw.text((px + 54, py + 110), "PASS FOR USER REVIEW", font=font(27), fill="#24452D")
draw.text((px + 54, py + 151), "结构基础保留，造型语言已换轨", font=font(22, True), fill="#355B3E")

evidence_y = py + 224
evidence = [
    ("01  现代轮廓", ["三段层叠屋面 + 连续转折面", "低矮横向，不再是方盒堆叠"]),
    ("02  博物馆首读", ["公共大厅、展廊、实机窗与人可读", "舰体不是游艇上层或普通舰桥"]),
    ("03  巨构重量", ["B1 / B2 剖面明显大于地上馆体", "城市、消防车与馆守Z形成尺度带"]),
    ("04  深度人形", ["馆体进入胸肩，地下体进入腿足", "头部重构，不是外骨骼包覆"]),
]
for heading, body in evidence:
    draw.text((px + 38, evidence_y), heading, font=font(27), fill="#9D3F31")
    evidence_y += 40
    evidence_y = draw_lines(draw, (px + 44, evidence_y), body, font(22, True), "#424846", 9)
    evidence_y += 18

draw.line((px + 34, py + 840, px + pw - 34, py + 840), fill="#C8C2B7", width=2)
draw.text((px + 38, py + 870), "真实开放项", font=font(29), fill="#252B2B")
draw_lines(
    draw,
    (px + 44, py + 920),
    [
        "· 巡展态是否仍有一点大型载具首读",
        "· 人形头肩是否已有万机馆专属识别",
        "· 精确低矮比例仍需正投影验证",
    ],
    font(21, True),
    "#555B58",
    12,
)

# Decision strip
by = 1310
draw.text((60, by), "用户视觉裁决｜本轮只判断造型深化，不接程序", font=font(34), fill="#252B2B")

cards = [
    ("1  C 风格回收", ["是否比 A15 更现代、流动、帅，", "且没有退回游艇／快艇或方盒感？"]),
    ("2  博物馆巨构", ["公共展馆与巨大 B1 / B2 是否仍成立，", "整体是否真正读成 130–160m 巨物？"]),
    ("3  未来人形", ["是否完成深度重组与头部变化，", "并已有足够的万机馆专属识别？"]),
]
for i, (heading, body) in enumerate(cards):
    x = 60 + i * 770
    draw.rounded_rectangle((x, by + 60, x + 735, by + 300), radius=18, fill="#FAF8F2", outline="#C8C2B7", width=2)
    draw.text((x + 28, by + 87), heading, font=font(28), fill="#9D3F31")
    draw_lines(draw, (x + 28, by + 137), body, font(23, True), "#3F4543", 12)

draw.rectangle((0, 1660, 2400, 1800), fill="#2C3231")
draw.text((60, 1684), "边界：Candidate · user=false · runtime=false · Canon 未迁移 · 未接 Godot", font=font(25), fill="#F4EEE3")
draw.text((60, 1728), "输入职责：A15 只供结构／内容；原 ABC 的 C 只供现代轮廓／构面语法。", font=font(23, True), fill="#D7CFC1")
draw.text((60, 1765), "C01 只使用固定馆、离地转换、低空巡展态；右侧完整人形只作后续方向预演。", font=font(21, True), fill="#BFC8C2")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT_HALF.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, quality=96)
canvas.resize((1200, 900), Image.Resampling.LANCZOS).save(OUT_HALF, quality=94)
print(OUT)
print(OUT_HALF)
