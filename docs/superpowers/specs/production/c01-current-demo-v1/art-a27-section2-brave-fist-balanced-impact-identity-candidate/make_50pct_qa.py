from pathlib import Path

from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "generation-raw/BRAVE_FIST_A27_BALANCED_IMPACT_CALL01_RAW.png"
COLOR_OUT = ROOT / "qa/BRAVE_FIST_A27_BALANCED_IMPACT_RAW_50PCT.png"
GRAY_OUT = ROOT / "qa/BRAVE_FIST_A27_BALANCED_IMPACT_COLOR_HIDDEN_50PCT.png"

raw = Image.open(RAW).convert("RGB")
half = raw.resize((raw.width // 2, raw.height // 2), Image.Resampling.LANCZOS)
half.save(COLOR_OUT, quality=94)

gray = half.convert("L")
gray = ImageEnhance.Contrast(gray).enhance(1.08)
gray.convert("RGB").save(GRAY_OUT, quality=94)

print(COLOR_OUT)
print(GRAY_OUT)
