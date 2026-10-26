#!/usr/bin/env python3
"""Build the text-free Camera V2 geometry guide for Call03."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "source-guides/BREAKER_NORTH_CAMERA_V2_40X24_GEOMETRY_GUIDE_384.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (384, 384), (8, 15, 24, 255))
    draw = ImageDraw.Draw(image)

    # 3x3 footprint in Camera V2: 3 * tile_half = (120, 72).
    footprint = [(72, 248), (192, 176), (312, 248), (192, 320)]
    draw.polygon(footprint, fill=(233, 76, 155, 220), outline=(255, 153, 208, 255), width=2)

    # Native 384 slot and bottom-center pivot contract.
    draw.rounded_rectangle((28, 40, 356, 320), radius=12, outline=(194, 208, 223, 255), width=2)
    draw.line((192, 308, 192, 332), fill=(255, 255, 255, 255), width=3)
    draw.line((180, 320, 204, 320), fill=(255, 255, 255, 255), width=3)
    draw.ellipse((186, 314, 198, 326), fill=(255, 255, 255, 255))

    # Exact north screen vector (+40, -24), shown without text.
    start = (284, 138)
    end = (324, 114)
    draw.line((*start, *end), fill=(255, 220, 75, 255), width=5)
    draw.polygon([(324, 114), (312, 116), (319, 126)], fill=(255, 220, 75, 255))

    # Quiet body envelope: high shell, low head, load-bearing forelimbs.
    envelope = [(116, 230), (142, 126), (208, 92), (278, 120), (300, 214),
                (270, 250), (260, 300), (228, 300), (220, 238),
                (170, 238), (156, 300), (124, 300)]
    draw.line(envelope + [envelope[0]], fill=(85, 224, 233, 180), width=3)

    image.save(OUT, compress_level=9)
    print(OUT)


if __name__ == "__main__":
    main()
