#!/usr/bin/env python3
"""Recover edge-connected baked checker background and build deterministic QA.

The ImageGen result is preserved verbatim under raw/.  This script does not
redraw the character.  It removes only bright, low-chroma pixels connected to
the canvas edge, so enclosed white shirt/badge highlights remain opaque.
"""

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw/JICUN_E07_POSTBATTLE_CALL_CALL01_RAW.png"
DELIVERY = ROOT / "delivery/JICUN_E07_POSTBATTLE_CALL_CANDIDATE_RGBA.png"
QA = ROOT / "qa/JICUN_E07_POSTBATTLE_CALL_50_100_ALPHA_QA.png"


def edge_connected(mask: np.ndarray) -> np.ndarray:
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=np.uint8)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        if mask[0, x]:
            seen[0, x] = 1
            queue.append((0, x))
        if mask[height - 1, x] and not seen[height - 1, x]:
            seen[height - 1, x] = 1
            queue.append((height - 1, x))
    for y in range(height):
        if mask[y, 0] and not seen[y, 0]:
            seen[y, 0] = 1
            queue.append((y, 0))
        if mask[y, width - 1] and not seen[y, width - 1]:
            seen[y, width - 1] = 1
            queue.append((y, width - 1))

    while queue:
        y, x = queue.popleft()
        for dy, dx in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = 1
                queue.append((ny, nx))
    return seen.astype(bool)


def checker(size: tuple[int, int], cell: int = 24) -> Image.Image:
    width, height = size
    out = Image.new("RGB", size, (218, 218, 218))
    draw = ImageDraw.Draw(out)
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            if ((x // cell) + (y // cell)) % 2:
                draw.rectangle((x, y, min(x + cell - 1, width - 1), min(y + cell - 1, height - 1)), fill=(174, 174, 174))
    return out


def contain(image: Image.Image, box: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(box, Image.Resampling.LANCZOS)
    return copy


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def main() -> None:
    raw = Image.open(RAW).convert("RGB")
    rgb = np.asarray(raw, dtype=np.uint8)
    rgb16 = rgb.astype(np.int16)
    minimum = rgb16.min(axis=2)
    maximum = rgb16.max(axis=2)
    chroma = maximum - minimum

    # The generated background consists of near-white neutral checker cells.
    # A looser connected threshold consumes antialiased checker edges without
    # crossing the dark outline that encloses skin, shirt, badge and terminal.
    background_candidate = ((minimum >= 55) & (chroma <= 20)) | ((minimum >= 180) & (chroma <= 55))
    background = edge_connected(background_candidate)

    rgba = np.dstack((rgb, np.where(background, 0, 255).astype(np.uint8)))
    out = Image.fromarray(rgba, mode="RGBA")
    DELIVERY.parent.mkdir(parents=True, exist_ok=True)
    out.save(DELIVERY, optimize=True)

    # 50/100 QA: full-resolution crops on contrasting backgrounds plus a 50%
    # whole-silhouette read.  This catches white halos and accidental shirt holes.
    board = Image.new("RGB", (2200, 1800), (23, 28, 36))
    draw = ImageDraw.Draw(board)
    title_font = font(34)
    label_font = font(24)
    draw.text((40, 24), "JICUN E07 — 100% EDGE / 50% SILHOUETTE / ALPHA QA", font=title_font, fill=(238, 241, 246))

    crop_box = (150, 0, 880, 900)
    edge_crop = out.crop(crop_box)
    for idx, (label, bg_color) in enumerate((("100% DARK", (15, 20, 28)), ("100% MAGENTA", (104, 18, 82)))):
        x0 = 40 + idx * 760
        panel = Image.new("RGBA", edge_crop.size, bg_color + (255,))
        panel.alpha_composite(edge_crop)
        board.paste(panel.convert("RGB"), (x0, 88))
        draw.text((x0 + 12, 100), label, font=label_font, fill=(255, 255, 255))

    alpha = out.getchannel("A")
    alpha_panel = Image.new("RGB", edge_crop.size, (0, 0, 0))
    alpha_panel.paste(alpha.crop(crop_box).convert("RGB"))
    board.paste(alpha_panel, (1560, 88))
    draw.text((1572, 100), "100% ALPHA", font=label_font, fill=(255, 255, 255))

    half = contain(out, (560, 740))
    for idx, (label, base) in enumerate((("50% CHECKER", checker((680, 760))), ("50% LIGHT", Image.new("RGB", (680, 760), (238, 240, 242))))):
        x0 = 40 + idx * 720
        y0 = 1010
        panel = base.convert("RGBA")
        px = (panel.width - half.width) // 2
        py = panel.height - half.height
        panel.alpha_composite(half, (px, py))
        board.paste(panel.convert("RGB"), (x0, y0))
        draw.text((x0 + 12, y0 + 12), label, font=label_font, fill=(18, 24, 32) if "LIGHT" in label else (255, 255, 255))

    stats = np.unique(rgba[:, :, 3], return_counts=True)
    counts = dict(zip(stats[0].tolist(), stats[1].tolist()))
    draw.text((1480, 1050), f"RAW: RGB 1022×1538", font=label_font, fill=(232, 235, 240))
    draw.text((1480, 1100), f"DELIVERY: RGBA 1022×1538", font=label_font, fill=(232, 235, 240))
    draw.text((1480, 1150), f"alpha=0: {counts.get(0, 0):,}", font=label_font, fill=(232, 235, 240))
    draw.text((1480, 1200), f"alpha=255: {counts.get(255, 0):,}", font=label_font, fill=(232, 235, 240))
    draw.text((1480, 1270), "Candidate only", font=title_font, fill=(255, 196, 92))
    draw.text((1480, 1320), "user=false", font=label_font, fill=(232, 235, 240))
    draw.text((1480, 1360), "runtime=false", font=label_font, fill=(232, 235, 240))
    draw.text((1480, 1400), "canon=false", font=label_font, fill=(232, 235, 240))

    QA.parent.mkdir(parents=True, exist_ok=True)
    board.save(QA, optimize=True)


if __name__ == "__main__":
    main()
