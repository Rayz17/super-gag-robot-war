#!/usr/bin/env python3
"""Build immutable QA for the one allowed A17 cold-front ImageGen edit.

The ImageGen output is copied byte-for-byte into the workspace and is retained
only as failure evidence. It must never be used as a positive pixel source.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[5]
ACCEPTED = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png"
FAILED = ROOT / "call01-shield-edit/preflight-fail/generation-raw/A17_COLD_FRONT_CALL01_FOURTH_WHITE_SCAR_IDENTITY_DRIFT_FAIL_RAW.png"
OUT = ROOT / "call01-shield-edit/preflight-fail/qa/A17_COLD_FRONT_CALL01_FAIL_50_100_QA.png"


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    return copy


def composite_on(image: Image.Image, size: tuple[int, int], background: tuple[int, int, int, int]) -> Image.Image:
    fitted = fit(image.convert("RGBA"), size)
    canvas = Image.new("RGBA", size, background)
    canvas.alpha_composite(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return canvas


def main() -> None:
    accepted = Image.open(ACCEPTED).convert("RGBA")
    failed_rgb = Image.open(FAILED)
    assert failed_rgb.mode == "RGB" and failed_rgb.size == (1024, 1536)

    board = Image.new("RGBA", (2400, 1560), (15, 24, 33, 255))
    d = ImageDraw.Draw(board)
    white = (243, 247, 250, 255)
    muted = (187, 203, 215, 255)
    amber = (255, 190, 71, 255)
    fail = (255, 103, 103, 255)

    d.text((40, 30), "R3 A17 COLD FRONT · CALL01 FAIL AT 50% / 100%", font=font(36, True), fill=white)
    d.text((40, 82), "Shield edit calls: 1 · rerolls: 0 · body calls: 0 · failed raw is isolated and never a positive input", font=font(22), fill=amber)

    # 50% first-read comparison normalized to the same display box.
    left_box = (40, 150, 540, 900)
    right_box = (580, 150, 1080, 900)
    d.rounded_rectangle(left_box, radius=16, fill=(235, 233, 227, 255))
    d.rounded_rectangle(right_box, radius=16, fill=(235, 233, 227, 255))
    board.alpha_composite(composite_on(accepted, (500, 750), (235, 233, 227, 255)), (40, 150))
    board.alpha_composite(fit(failed_rgb.convert("RGBA"), (500, 750)), (580, 150))
    d.text((40, 918), "ACCEPTED A17 · 3 pale scars + 1 future red/hot trace", font=font(20, True), fill=white)
    d.text((580, 918), "CALL01 EDIT · 4 pale scars + baked checker RGB", font=font(20, True), fill=fail)

    # Mark the four pale scars on the normalized failed frame.
    # Failed raw scales uniformly from 1024x1536 to 500x750.
    scar_points = ((560, 480), (450, 715), (710, 690), (540, 1010))
    for index, (sx, sy) in enumerate(scar_points, start=1):
        x = 580 + round(sx * 500 / 1024)
        y = 150 + round(sy * 750 / 1536)
        radius = 22
        d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(175, 23, 36, 235), outline=(255, 232, 232, 255), width=3)
        label = str(index)
        box = d.textbbox((0, 0), label, font=font(24, True))
        d.text((x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2 - 2), label, font=font(24, True), fill=white)

    # 100% pixel crops: accepted hot region and generated replacement region.
    accepted_crop = accepted.crop((168, 345, 728, 845))  # 560x500, no resample
    failed_crop = failed_rgb.crop((224, 460, 784, 960)).convert("RGBA")  # 560x500, no resample
    board.alpha_composite(accepted_crop, (1160, 150))
    board.alpha_composite(failed_crop, (1760, 150))
    d.rectangle((1160, 150, 1720, 650), outline=(214, 224, 230, 255), width=3)
    d.rectangle((1760, 150, 2320, 650), outline=fail, width=3)
    d.text((1160, 668), "100% accepted source crop", font=font(20, True), fill=white)
    d.text((1760, 668), "100% failed edit crop", font=font(20, True), fill=fail)

    d.text((1160, 735), "HARD FAIL 1", font=font(24, True), fill=fail)
    d.text((1160, 775), "The removed red/hot slash became an extra pale diagonal scar.", font=font(21), fill=white)
    d.text((1160, 815), "Required: exactly 3 old pale scars. Observed: 4.", font=font(21, True), fill=fail)
    d.text((1160, 885), "HARD FAIL 2", font=font(24, True), fill=fail)
    d.text((1160, 925), "Required transparent RGBA. Output is 1024×1536 RGB with checker baked in.", font=font(21), fill=white)
    d.text((1160, 995), "HARD FAIL 3", font=font(24, True), fill=fail)
    d.text((1160, 1035), "Outside the narrow repair region, crown, panels, frame and wear were redrawn.", font=font(21), fill=white)

    d.rounded_rectangle((40, 1120, 2320, 1470), radius=18, fill=(30, 41, 52, 255), outline=(89, 111, 128, 255), width=2)
    d.text((72, 1150), "FIRST FAILURE GATE", font=font(28, True), fill=fail)
    d.text((72, 1200), "FAIL_COLD_SHIELD_50_100_IDENTITY_AND_STATE_FIDELITY", font=font(25, True), fill=white)
    d.text((72, 1260), "Stop immediately. No body-only ImageGen call. No deterministic composite, map Candidate, manifest, socket, Godot binding, Runtime or Canon.", font=font(22), fill=amber)
    d.text((72, 1320), "The failed RGB raw and this QA exist only as negative evidence; they are forbidden as future positive inputs.", font=font(22), fill=muted)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    board.convert("RGB").save(OUT)


if __name__ == "__main__":
    main()
