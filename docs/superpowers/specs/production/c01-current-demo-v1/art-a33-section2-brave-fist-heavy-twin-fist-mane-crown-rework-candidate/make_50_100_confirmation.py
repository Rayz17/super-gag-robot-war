from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "generation-raw/BRAVE_FIST_A33_CALL01_RAW.png"
COLOR_50 = ROOT / "qa/BRAVE_FIST_A33_HEAVY_TWIN_FIST_MANE_CROWN_COLOR_50PCT.png"
GRAY_50 = ROOT / "qa/BRAVE_FIST_A33_HEAVY_TWIN_FIST_MANE_CROWN_COLOR_HIDDEN_50PCT.png"
BOARD = ROOT / "delivery/BRAVE_FIST_A33_HEAVY_TWIN_FIST_MANE_CROWN_50_100_QA_BOARD_USER_REVIEW_CANDIDATE.png"


raw = Image.open(RAW).convert("RGB")
half = raw.resize((raw.width // 2, raw.height // 2), Image.Resampling.LANCZOS)
half.save(COLOR_50)

gray = ImageEnhance.Contrast(half.convert("L")).enhance(1.08).convert("RGB")
gray.save(GRAY_50)

margin = 34
header = 58
gap = 28
board_width = margin * 4 + gap * 2 + raw.width + half.width * 2
board_height = margin * 2 + header + raw.height
canvas = Image.new("RGB", (board_width, board_height), (21, 23, 26))
draw = ImageDraw.Draw(canvas)
try:
    label_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
except OSError:
    label_font = ImageFont.load_default()

x100 = margin
x50c = x100 + raw.width + gap
x50g = x50c + half.width + gap
y = margin + header

draw.text((x100, margin), "100% COLOR MASTER", fill=(240, 240, 236), font=label_font)
draw.text((x50c, margin), "50% COLOR", fill=(240, 240, 236), font=label_font)
draw.text((x50g, margin), "50% COLOR HIDDEN", fill=(240, 240, 236), font=label_font)

canvas.paste(raw, (x100, y))
canvas.paste(half, (x50c, y))
canvas.paste(gray, (x50g, y))

for x, w, h in (
    (x100, raw.width, raw.height),
    (x50c, half.width, half.height),
    (x50g, gray.width, gray.height),
):
    draw.rectangle((x - 1, y - 1, x + w, y + h), outline=(118, 123, 130), width=2)

canvas.save(BOARD)
print(COLOR_50)
print(GRAY_50)
print(BOARD)

