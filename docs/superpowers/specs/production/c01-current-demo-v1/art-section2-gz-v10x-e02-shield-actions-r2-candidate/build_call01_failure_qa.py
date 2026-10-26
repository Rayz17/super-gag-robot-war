#!/usr/bin/env python3
"""Build failure-only QA for the stopped shield_take R2 call.

The raw remains immutable. A border-connected checker removal is used only to
make the front-hand failure readable on dark and light review backgrounds.
Nothing from this script is a master or map candidate.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "call01/stage-a-block/generation-raw/GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_TAKE_SOUTH_R2_CALL01_FRONT_HANDS_FAIL_RAW.png"
QA = ROOT / "call01/stage-a-block/qa"


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for name in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def border_connected_checker_alpha(rgb: Image.Image) -> tuple[Image.Image, dict[str, int]]:
    rgb = rgb.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def is_background(x: int, y: int) -> bool:
        r, g, b = pixels[x, y]
        return min(r, g, b) >= 224 and max(r, g, b) - min(r, g, b) <= 14

    def enqueue(x: int, y: int) -> None:
        index = y * width + x
        if not visited[index] and is_background(x, y):
            visited[index] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                enqueue(nx, ny)

    alpha = Image.new("L", rgb.size, 255)
    ap = alpha.load()
    removed = 0
    for y in range(height):
        row = y * width
        for x in range(width):
            if visited[row + x]:
                ap[x, y] = 0
                removed += 1
    rgba = rgb.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba, {
        "canvas_pixels": width * height,
        "transparent_pixels": removed,
        "opaque_pixels": width * height - removed,
        "partial_alpha_pixels": 0,
    }


def mark_front_hands(image: Image.Image, scale: float = 1.0, offset: tuple[int, int] = (0, 0)) -> Image.Image:
    marked = image.copy()
    d = ImageDraw.Draw(marked)
    # Centres are measured on the immutable 1254 raw. Both lie visibly on the
    # exterior/front plane above the shield crown.
    for cx, cy in ((405, 466), (590, 470)):
        cx -= offset[0]
        cy -= offset[1]
        box = tuple(round(v * scale) for v in (cx - 62, cy - 62, cx + 62, cy + 62))
        d.ellipse(box, outline=(255, 64, 76, 255), width=max(3, round(8 * scale)))
    return marked


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW).convert("RGB")
    rgba, _ = border_connected_checker_alpha(raw)
    review = QA / "GUARDIAN_Z_V10X_SHIELD_TAKE_SOUTH_R2_CALL01_ALPHA_REVIEW_ONLY.png"
    rgba.save(review)

    bbox = rgba.getchannel("A").getbbox()
    assert bbox is not None
    subject = rgba.crop(bbox)
    scale = min(700 / subject.width, 760 / subject.height)
    subject = subject.resize((round(subject.width * scale), round(subject.height * scale)), Image.Resampling.LANCZOS)

    board = Image.new("RGBA", (2000, 1320), (17, 24, 33, 255))
    d = ImageDraw.Draw(board)
    d.text((36, 26), "SHIELD_TAKE / SOUTH R2 · FIRST FAILURE GATE", font=font(34, True), fill=(246, 248, 250, 255))
    d.text((36, 73), "STOP: both hands are painted on the shield front/exterior; required front=0, rear=2", font=font(22, True), fill=(255, 106, 113, 255))

    # 50% action/identity read on light and dark.
    thumb = rgba.resize((627, 627), Image.Resampling.LANCZOS)
    for idx, bg in enumerate(((240, 238, 232, 255), (8, 15, 23, 255))):
        x = 28 + idx * 664
        y = 126
        d.rounded_rectangle((x, y, x + 648, y + 648), radius=14, fill=bg)
        board.alpha_composite(thumb, (x + 10, y + 10))
    d.text((36, 790), "50% light/dark: V10X identity + cold three-scar shield are readable", font=font(19, True), fill=(226, 232, 237, 255))

    # 100% interaction crop with explicit red failure circles.
    crop_box = (230, 310, 790, 670)
    detail = rgba.crop(crop_box)
    detail = detail.resize((840, 540), Image.Resampling.LANCZOS)
    detail = mark_front_hands(detail, scale=840 / (crop_box[2] - crop_box[0]), offset=(crop_box[0], crop_box[1]))
    x, y = 1100, 176
    d.rounded_rectangle((x - 12, y - 12, x + 852, y + 552), radius=14, fill=(237, 235, 229, 255))
    board.alpha_composite(detail, (x, y))
    d.text((1110, 748), "100% hand-side read: two exterior/front contacts = hard FAIL", font=font(19, True), fill=(255, 106, 113, 255))

    d.text((36, 864), "Passed subreads", font=font(23, True), fill=(116, 218, 158, 255))
    d.text((36, 902), "• exactly 3 pale old scars; no red/hot fourth trace", font=font(19), fill=(219, 228, 234, 255))
    d.text((36, 936), "• shield remains low/off-centre and action is closer to TAKE than HOLD/BLOCK", font=font(19), fill=(219, 228, 234, 255))
    d.text((36, 982), "Failed hard subread", font=font(23, True), fill=(255, 106, 113, 255))
    d.text((36, 1020), "• hands and grips must be behind/rear-interior, but the image puts both on the visible exterior", font=font(19), fill=(219, 228, 234, 255))
    d.text((36, 1078), "Downstream calls NOT MADE: shield_hold · shield_block · shield_bash", font=font(22, True), fill=(255, 198, 74, 255))
    d.text((36, 1130), "Failure-only evidence · no map candidate · no socket · user=false · runtime=false · canon=false", font=font(18, True), fill=(190, 204, 215, 255))

    board.save(QA / "GUARDIAN_Z_V10X_SHIELD_TAKE_SOUTH_R2_CALL01_FRONT_HANDS_FAIL_50_100_QA.png")


if __name__ == "__main__":
    main()
