#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "call01/delivery/JICUN_B06_CHEST_GUIDE_SEAT_LOCAL_SCENE_CANDIDATE_V1.png"
QA = ROOT / "call01/qa"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGB")
    if source.size != (1024, 1536):
        raise SystemExit(f"unexpected source size: {source.size}")

    half = source.resize((512, 768), Image.Resampling.LANCZOS)
    half.save(QA / "JICUN_B06_LOCAL_SCENE_50PCT_FULL_QA.png", optimize=True)

    identity_action = source.crop((90, 180, 930, 680))
    identity_action.save(
        QA / "JICUN_B06_LOCAL_SCENE_100PCT_IDENTITY_ACTION_CROP_QA.png",
        optimize=True,
    )

    seat_threshold = source.crop((240, 500, 1024, 1100))
    seat_threshold.save(
        QA / "JICUN_B06_LOCAL_SCENE_100PCT_SEAT_THRESHOLD_CROP_QA.png",
        optimize=True,
    )

    board = Image.new("RGB", (1500, 1360), (18, 23, 31))
    draw = ImageDraw.Draw(board)
    title = font(26)
    label = font(20)
    ink = (236, 240, 246)
    accent = (248, 190, 78)

    draw.text((40, 24), "B06 LOCAL SCENE INSERT — 50% / 100% CROP QA", font=title, fill=ink)
    draw.text((40, 112), "50% FULL: PERSON + GUIDE SEAT + HATCH", font=label, fill=accent)
    board.paste(half, (40, 160))

    draw.text((600, 74), "100% IDENTITY / BRACE / TERMINAL / SEAT", font=label, fill=accent)
    board.paste(identity_action, (600, 112))

    draw.text((600, 632), "100% GUIDE-SEAT / HARNESS / THRESHOLD", font=label, fill=accent)
    board.paste(seat_threshold, (600, 670))

    board.save(QA / "JICUN_B06_LOCAL_SCENE_50_100_CROP_QA_BOARD.png", optimize=True)


if __name__ == "__main__":
    main()
