from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "user-confirmation-call01/generation-raw/wanji_a15_call01_raw.png"
OUT = ROOT / "user-confirmation-call01/wanji_a15_user_confirmation_board_2400x1800.png"
OUT_HALF = ROOT / "user-confirmation-call01/qa/wanji_a15_user_confirmation_board_1200x900.png"

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


canvas = Image.new("RGB", (2400, 1800), "#EEECE6")
draw = ImageDraw.Draw(canvas)

# Header
draw.rectangle((0, 0, 2400, 132), fill="#242A2A")
draw.text((62, 24), "A15｜万机馆：机器人博物馆巨构 → 未来人形方向预演", font=font(54), fill="#F7F2E7")
draw.text((1850, 48), "一次生成 · 0 reroll", font=font(24, True), fill="#D7CDBE")

# Full, uncropped generation
raw = Image.open(RAW).convert("RGB")
raw_fit = fit_image(raw, (1650, 1100))
img_x, img_y = 60, 170
draw.rectangle((img_x - 5, img_y - 5, img_x + raw_fit.width + 5, img_y + raw_fit.height + 5), fill="#343A39")
canvas.paste(raw_fit, (img_x, img_y))
draw.rounded_rectangle((img_x + 18, img_y + 18, img_x + 313, img_y + 65), radius=10, fill="#242A2ADE")
draw.text((img_x + 34, img_y + 26), "完整原图｜未裁切", font=font(22), fill="#FFFFFF")

# Right-side audit panel
px, py, pw, ph = 1750, 170, 590, 1100
draw.rounded_rectangle((px, py, px + pw, py + ph), radius=22, fill="#FAF8F2", outline="#C8C2B7", width=3)
draw.text((px + 34, py + 30), "50% 首读门", font=font(36), fill="#252B2B")
draw.rounded_rectangle((px + 30, py + 88, px + pw - 30, py + 190), radius=16, fill="#DDEBDD")
draw.text((px + 54, py + 110), "PASS（未获用户确认）", font=font(29), fill="#24452D")
draw.text((px + 54, py + 151), "首读是博物馆巨构，不是船艇", font=font(22, True), fill="#355B3E")

evidence_y = py + 230
evidence = [
    ("01  公共馆体", ["大跨度主展厅成为主轮廓", "多层展廊、入口、实机窗可读"]),
    ("02  地下巨构", ["B1 / B2 体量不再是薄底盘", "承力柱、深舱与城市断管成立"]),
    ("03  前向语言", ["宽直巨机门 + 外泊前场", "无尖鼻、曲面驾驶舱、游艇船舷"]),
    ("04  同源人形", ["展厅 / 展廊进入胸肩背", "地下躯体进入骨盆、腿与地基足"]),
]
for heading, body in evidence:
    draw.text((px + 38, evidence_y), heading, font=font(28), fill="#9D3F31")
    evidence_y += 43
    evidence_y = draw_lines(draw, (px + 44, evidence_y), body, font(23, True), "#424846", 10)
    evidence_y += 24

draw.line((px + 34, py + 850, px + pw - 34, py + 850), fill="#C8C2B7", width=2)
draw.text((px + 38, py + 880), "仍需你裁决", font=font(29), fill="#252B2B")
draw_lines(
    draw,
    (px + 44, py + 930),
    ["· 130–160m / 35–45m 是否够低矮", "· 南侧巨机门是否清楚承担前向", "· 人形是否有万机馆专属识别"],
    font(22, True),
    "#555B58",
    12,
)

# Decision strip
by = 1310
draw.text((60, by), "用户视觉裁决｜请按 1–3 逐项判断", font=font(34), fill="#252B2B")

cards = [
    ("1  博物馆巨构", ["第一眼是否已是可进入的高科技", "机器人文化博物馆，而不是舰船？"]),
    ("2  C01 巡展态", ["馆体 / B1 / B2 的重量与低矮比例", "是否成立？南侧巨机门前向是否清楚？"]),
    ("3  未来人形", ["展厅→胸肩背、地下巨构→骨盆腿足", "是否同源且具有万机馆专属特点？"]),
]
for i, (heading, body) in enumerate(cards):
    x = 60 + i * 770
    draw.rounded_rectangle((x, by + 60, x + 735, by + 300), radius=18, fill="#FAF8F2", outline="#C8C2B7", width=2)
    draw.text((x + 28, by + 87), heading, font=font(28), fill="#9D3F31")
    draw_lines(draw, (x + 28, by + 137), body, font(23, True), "#3F4543", 12)

draw.rectangle((0, 1660, 2400, 1800), fill="#2C3231")
draw.text((60, 1684), "边界：Candidate · user=false · runtime=false · Canon 未迁移 · 未接 Godot", font=font(25), fill="#F4EEE3")
draw.text((60, 1728), "C01 只展示固定馆 / 离地转换 / 低空巡展态；右侧人形仅作未来方向预演。", font=font(23, True), fill="#D7CFC1")
draw.text((60, 1765), "A13 / A14 像素未输入本次生成。", font=font(21, True), fill="#BFC8C2")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT_HALF.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, quality=96)
canvas.resize((1200, 900), Image.Resampling.LANCZOS).save(OUT_HALF, quality=94)
print(OUT)
print(OUT_HALF)
