from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "generation-raw/BRAVE_FIST_A26_SINGLE_IMPACT_RETURN_CALL01_RAW.png"
OUT = ROOT / "delivery/BRAVE_FIST_A26_SINGLE_IMPACT_RETURN_USER_CONFIRMATION_BOARD_2400x1800.png"
OUT_HALF = ROOT / "qa/BRAVE_FIST_A26_SINGLE_IMPACT_RETURN_USER_CONFIRMATION_BOARD_1200x900.png"
RAW_HALF = ROOT / "qa/BRAVE_FIST_A26_SINGLE_IMPACT_RETURN_RAW_50PCT.png"

FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, light: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_LIGHT if light else FONT_MEDIUM, size=size)


def fit(im: Image.Image, box: tuple[int, int]) -> Image.Image:
    result = im.copy()
    result.thumbnail(box, Image.Resampling.LANCZOS)
    return result


def cover_crop(im: Image.Image, crop_box: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    crop = im.crop(crop_box)
    ratio = max(size[0] / crop.width, size[1] / crop.height)
    resized = crop.resize((round(crop.width * ratio), round(crop.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


raw = Image.open(RAW).convert("RGB")
canvas = Image.new("RGB", (2400, 1800), "#EEEAE1")
draw = ImageDraw.Draw(canvas)

draw.rectangle((0, 0, 2400, 132), fill="#202424")
draw.text((62, 24), "A26｜勇拳单一冲量回送拳 · 身份母版", font=font(52), fill="#F7F2E7")
draw.text((1960, 48), "1 call · 0 reroll", font=font(23, True), fill="#D6CBB8")

main_box = (52, 164, 1216, 1660)
draw.rounded_rectangle(main_box, radius=22, fill="#151818", outline="#474D4B", width=4)
main = fit(raw, (1120, 1446))
main_x = main_box[0] + (main_box[2] - main_box[0] - main.width) // 2
main_y = main_box[1] + (main_box[3] - main_box[1] - main.height) // 2
canvas.paste(main, (main_x, main_y))
draw.rounded_rectangle((76, 188, 430, 240), radius=12, fill="#232929")
draw.text((96, 199), "单一全身身份 Candidate", font=font(23), fill="#FFFFFF")

right_x = 1260
draw.text((right_x, 166), "50% 首读", font=font(34), fill="#242929")
draw.rounded_rectangle((right_x, 216, 2350, 474), radius=18, fill="#FAF8F2", outline="#C8C0B2", width=3)
thumb = fit(raw, (180, 230))
canvas.paste(thumb, (right_x + 22, 230))
draw.text((right_x + 230, 242), "PASS_FOR_USER_REVIEW", font=font(28), fill="#8B3F2A")
draw.text((right_x + 230, 294), "首先读到的是一只单侧巨型压缩回送拳，", font=font(23, True), fill="#3E4441")
draw.text((right_x + 230, 334), "而不是对称双大拳的通用勇者机。", font=font(23, True), fill="#3E4441")
draw.text((right_x + 230, 386), "另一臂为可抓持、承力的五指手。", font=font(23, True), fill="#3E4441")

cards = [
    ("独有主剪影", (420, 245, 858, 1450), ["同一只完整大拳", "多段套筒＋双回送导轨"]),
    ("完整机器人能力", (0, 460, 410, 1240), ["非对称另一臂", "五指救援／抓持手"]),
    ("头胸同一语言", (105, 150, 720, 800), ["小型压力冠＋偏置传感器", "胸腹承力轴接入主拳"]),
]

for i, (heading, crop_box, lines) in enumerate(cards):
    y = 520 + i * 326
    draw.rounded_rectangle((right_x, y, 2350, y + 292), radius=18, fill="#FAF8F2", outline="#C8C0B2", width=3)
    crop = cover_crop(raw, crop_box, (365, 246))
    canvas.paste(crop, (right_x + 22, y + 22))
    draw.text((right_x + 420, y + 30), heading, font=font(29), fill="#9B452D")
    draw.text((right_x + 420, y + 91), lines[0], font=font(23, True), fill="#3E4441")
    draw.text((right_x + 420, y + 134), lines[1], font=font(23, True), fill="#3E4441")
    if i == 0:
        draw.text((right_x + 420, y + 190), "接冲击 → 套筒压缩 → 原拳整量回送", font=font(21, True), fill="#6B716D")

draw.rectangle((0, 1690, 2400, 1800), fill="#292F2E")
draw.text((58, 1711), "边界：Candidate · user=false · runtime=false · Canon=false · 未接 Godot · 未制作四向/动作 Sprite", font=font(24), fill="#F2EBDC")
draw.text((58, 1753), "本图仅等待用户判断单一回送拳、完整可用的另一臂、头胸回路识别性。", font=font(22, True), fill="#D4CBBB")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT_HALF.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, quality=96)
canvas.resize((1200, 900), Image.Resampling.LANCZOS).save(OUT_HALF, quality=94)
raw.resize((raw.width // 2, raw.height // 2), Image.Resampling.LANCZOS).save(RAW_HALF, quality=94)

print(OUT)
print(OUT_HALF)
print(RAW_HALF)
