#!/usr/bin/env python3
"""Build non-art Camera V2 guides and deterministic QA composites.

This script never draws, repairs, or invents subject pixels.  Before generation it
only draws projection guides.  After generation it may crop/pad/scale existing
RGBA subject pixels and assemble review boards.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
GUIDES = ROOT / "source-guides"
RECEIPTS = ROOT / "receipts"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dashed_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color, width=2, dash=8):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, dash * 2):
        draw.line((x, y0, min(x + dash, x1), y0), fill=color, width=width)
        draw.line((x, y1, min(x + dash, x1), y1), fill=color, width=width)
    for y in range(y0, y1, dash * 2):
        draw.line((x0, y, x0, min(y + dash, y1)), fill=color, width=width)
        draw.line((x1, y, x1, min(y + dash, y1)), fill=color, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, color, width):
    draw.line((*start, *end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = width * 4
    for delta in (2.55, -2.55):
        p = (end[0] + math.cos(angle + delta) * size, end[1] + math.sin(angle + delta) * size)
        draw.line((*end, *p), fill=color, width=width)


def guide(size: int, pivot: tuple[int, int], footprint: int, facing: str, path: Path):
    # Opaque neutral reference prevents checkerboard or alpha from being treated as anatomy.
    im = Image.new("RGBA", (size, size), (14, 20, 27, 255))
    d = ImageDraw.Draw(im)
    d.rectangle((1, 1, size - 2, size - 2), outline=(102, 124, 139, 255), width=2)
    margin = max(8, size // 24)
    dashed_rect(d, (margin, margin, size - margin - 1, pivot[1]), (70, 94, 109, 255), width=max(1, size // 192))

    half_w = footprint * 40 // 2
    half_h = footprint * 24 // 2
    cx, bottom = pivot
    cy = bottom - half_h
    diamond = [(cx, bottom - 2 * half_h), (cx + half_w, cy), (cx, bottom), (cx - half_w, cy)]
    d.polygon(diamond, fill=(26, 47, 56, 255), outline=(78, 210, 224, 255))
    d.line(diamond + [diamond[0]], fill=(78, 210, 224, 255), width=max(2, size // 128), joint="curve")
    d.ellipse((cx - 5, bottom - 5, cx + 5, bottom + 5), fill=(255, 92, 171, 255))
    d.line((cx - 12, bottom, cx + 12, bottom), fill=(255, 92, 171, 255), width=2)
    d.line((cx, bottom - 12, cx, bottom + 12), fill=(255, 92, 171, 255), width=2)

    length = int(size * 0.22)
    theta = math.radians(30.9637565 if facing == "east" else -30.9637565)
    start = (cx, cy)
    end = (round(cx + math.cos(theta) * length), round(cy + math.sin(theta) * length))
    arrow(d, start, end, (255, 193, 71, 255), max(3, size // 96))

    # A short vertical cue encodes the elevated/top-visible view without supplying anatomy.
    arrow(d, (margin * 2, pivot[1] - margin), (margin * 2, margin * 2), (130, 162, 255, 255), max(2, size // 128))
    im.save(path, format="PNG", optimize=False, compress_level=9)
    return {
        "path": str(path),
        "sha256": sha256(path),
        "canvas": [size, size],
        "pivot_px": list(pivot),
        "footprint_cells": [footprint, footprint],
        "facing": facing,
        "screen_axis_degrees": 30.9637565 if facing == "east" else -30.9637565,
        "footprint_local_polygon": [list(p) for p in diamond],
        "subject_pixels_present": False,
    }


def build_guides():
    GUIDES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    data = {
        "camera_contract": "CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE",
        "projection": "P(x,y)=((x-y)*40,(x+y)*24)",
        "guides": [
            guide(256, (128, 224), 2, "east", GUIDES / "GZ_EAST_CAMERA_V2_EXACT_GUIDE_256.png"),
            guide(384, (192, 320), 3, "north", GUIDES / "BREAKER_NORTH_CAMERA_V2_EXACT_GUIDE_384.png"),
        ],
    }
    out = RECEIPTS / "camera-guide-readback.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["guides"])
    args = parser.parse_args()
    if args.mode == "guides":
        build_guides()


if __name__ == "__main__":
    main()
