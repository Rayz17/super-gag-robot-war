from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source-lock" / "BRAVE_FIST_A33_ONLY_POSITIVE_MASTER.png"
STATE00 = ROOT / "delivery" / "BRAVE_FIST_A34_STATE00_NEUTRAL_MECHANISM_USER_REVIEW_CANDIDATE.png"
STATE01 = ROOT / "delivery" / "BRAVE_FIST_A34_STATE01_ABSORB_IMPACT_USER_REVIEW_CANDIDATE.png"
STATE02 = ROOT / "delivery" / "BRAVE_FIST_A34_STATE02_R1_PHYSICAL_COMPRESSION_LOCKED_USER_REVIEW_CANDIDATE.png"
OUT = ROOT / "qa" / "BRAVE_FIST_A34_STATE00_NEUTRAL_50PCT_GATE_BOARD.png"
PARTIAL_OUT = ROOT / "qa" / "BRAVE_FIST_A34_00_01_02_R1_PARTIAL_RETURN_GATE_BOARD.png"


def contain(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    result = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
    return result


def panel(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int], label: str) -> None:
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=(20, 23, 27), outline=(104, 116, 125), width=2)
    font = ImageFont.load_default(size=20)
    draw.text((x0 + 18, y0 + 14), label, fill=(230, 235, 239), font=font)
    fitted = contain(image, (x1 - x0 - 30, y1 - y0 - 70))
    px = x0 + (x1 - x0 - fitted.width) // 2
    py = y0 + 55 + (y1 - y0 - 65 - fitted.height) // 2
    canvas.paste(fitted, (px, py))


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    state = Image.open(STATE00).convert("RGB")
    gray = ImageOps.grayscale(state).convert("RGB")

    # Focus crop covers both upper arms, forearms, fist faces, head, and chest.
    focus = state.crop((0, 190, state.width, 1210))

    canvas = Image.new("RGB", (1800, 1200), (8, 10, 12))
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.load_default(size=28)
    draw.text(
        (32, 22),
        "A34 STATE00 HARD GATE | A33 identity / 50% silhouette / grayscale / arm-mechanism focus",
        fill=(245, 191, 66),
        font=title_font,
    )

    panel(canvas, source, (30, 75, 435, 1170), "A33 POSITIVE IDENTITY ANCHOR")
    panel(canvas, state, (455, 75, 860, 1170), "A34 STATE00 COLOR 50% READ")
    panel(canvas, gray, (880, 75, 1285, 1170), "A34 STATE00 GRAYSCALE 50% READ")
    panel(canvas, focus, (1305, 75, 1770, 1170), "A34 TWIN-FIST / TWIN-RAIL FOCUS")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT, optimize=True)

    states = [Image.open(path).convert("RGB") for path in (STATE00, STATE01, STATE02)]
    labels = (
        "00 NEUTRAL | IMPACT FACE + SLEEVES + RETURN RAILS",
        "01 ABSORB | FACE RECOIL + INWARD ENERGY",
        "02 R1 FULL LOAD | SHORT SLEEVES + LOCKS + WINDOWS",
    )
    overview = Image.new("RGB", (1980, 1800), (8, 10, 12))
    odraw = ImageDraw.Draw(overview)
    title_font = ImageFont.load_default(size=31)
    body_font = ImageFont.load_default(size=20)
    odraw.text(
        (38, 24),
        "BRAVE FIST A34 RETURN GATE | 00 + 01 RETAINED / 02 R1 PASS / 03 STILL MISSING",
        fill=(245, 191, 66),
        font=title_font,
    )
    for index, (state, label) in enumerate(zip(states, labels)):
        x0 = 30 + index * 640
        x1 = x0 + 610
        odraw.rounded_rectangle((x0, 82, x1, 1765), radius=18, fill=(20, 23, 27), outline=(104, 116, 125), width=2)
        odraw.text((x0 + 16, 98), label, fill=(230, 235, 239), font=body_font)
        full = contain(state, (570, 1140))
        overview.paste(full, (x0 + (610 - full.width) // 2, 145))
        # Keep identical normalized upper-body crop across all four states.
        crop_bottom = round(state.height * 0.68)
        focus = state.crop((0, round(state.height * 0.1), state.width, crop_bottom))
        focus_fit = contain(focus, (570, 430))
        overview.paste(focus_fit, (x0 + (610 - focus_fit.width) // 2, 1305))
    overview.save(PARTIAL_OUT, optimize=True)


if __name__ == "__main__":
    main()
