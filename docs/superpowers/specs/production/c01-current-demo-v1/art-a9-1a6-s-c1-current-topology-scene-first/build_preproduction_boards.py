#!/usr/bin/env python3
"""Build Task90 pre-generation evidence boards only.

This script performs byte-copy, crop, layout, labels, and transparent UI-template
composition. It does not draw a target map, actor, mecha, building, route, ghost,
or other visible scene content. A4 pixels remain explicitly labelled legacy mood
donors; current topology must come from a later producer-signed Task89 actual frame.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/rayz/Documents/超gag机器人大战")
OUT = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c1-current-topology-scene-first"
A4 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer"
SAFE_SOURCE = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-scene-target-lookdev/source-guides/IDENTITY_STYLE_REFERENCE_MOSAIC_SAFE_2400x1800.png"
SAFE_EXPECTED_SHA = "dc473235883669165e0eef58ce8c9d390e719e946e133648893b7d0ca83f3276"

SOURCES = {
    "ground": A4 / "A4_MAP_B_BASE_2400x1350.png",
    "buildings": A4 / "A4_MAP_B_BUILDINGS_2400x1350.png",
    "roofs": A4 / "A4_MAP_B_ROOFS_2400x1350.png",
    "foreground": A4 / "A4_MAP_B_FOREGROUND_2400x1350.png",
    "occlusion": A4 / "A4_MAP_B_OCCLUSION_MASK_2400x1350.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    choices = (
        [Path("/System/Library/Fonts/STHeiti Medium.ttc")] if bold else [Path("/System/Library/Fonts/STHeiti Light.ttc")]
    ) + [
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/System/Library/Fonts/Helvetica.ttc"),
    ]
    for choice in choices:
        if choice.exists():
            return ImageFont.truetype(str(choice), size=size, index=0)
    return ImageFont.load_default()


def fit_crop(source: Image.Image, crop_box: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    crop = source.crop(crop_box).convert("RGBA")
    target_ratio = size[0] / size[1]
    source_ratio = crop.width / crop.height
    if source_ratio > target_ratio:
        new_width = int(round(crop.height * target_ratio))
        left = (crop.width - new_width) // 2
        crop = crop.crop((left, 0, left + new_width, crop.height))
    elif source_ratio < target_ratio:
        new_height = int(round(crop.width / target_ratio))
        top = (crop.height - new_height) // 2
        crop = crop.crop((0, top, crop.width, top + new_height))
    return crop.resize(size, Image.Resampling.LANCZOS)


def add_panel(
    board: Image.Image,
    source: Image.Image,
    crop_box: tuple[int, int, int, int],
    rect: tuple[int, int, int, int],
    title: str,
    subtitle: str,
) -> None:
    x, y, w, h = rect
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=(10, 27, 35, 255), outline=(75, 116, 125, 255), width=2)
    label_height = 54
    draw.rounded_rectangle((x + 2, y + 2, x + w - 2, y + label_height), radius=15, fill=(13, 39, 49, 245))
    draw.rectangle((x + 2, y + 30, x + w - 2, y + label_height), fill=(13, 39, 49, 245))
    draw.text((x + 18, y + 10), title, font=font(22, True), fill=(225, 240, 241, 255))
    draw.text((x + w - 18, y + 14), subtitle, font=font(16), fill=(121, 184, 189, 255), anchor="ra")

    inner = (x + 12, y + label_height + 10, w - 24, h - label_height - 22)
    pixels = fit_crop(source, crop_box, (inner[2], inner[3]))
    backing = Image.new("RGBA", (inner[2], inner[3]), (4, 11, 15, 255))
    backing.alpha_composite(pixels)
    board.alpha_composite(backing, (inner[0], inner[1]))


def build_map_language_board() -> None:
    sources = {name: Image.open(path).convert("RGBA") for name, path in SOURCES.items()}
    board = Image.new("RGBA", (1920, 1080), (5, 14, 20, 255))
    draw = ImageDraw.Draw(board)

    draw.text((40, 28), "CURRENT-TOPOLOGY MAP LANGUAGE — PRE-GENERATION DONOR BOARD", font=font(34, True), fill=(235, 245, 243, 255))
    draw.text((40, 78), "A4 legacy pixels: material / value / layer / occlusion method only", font=font(22), fill=(112, 187, 192, 255))
    draw.rounded_rectangle((1420, 25, 1880, 108), radius=16, fill=(71, 24, 28, 255), outline=(222, 85, 83, 255), width=2)
    draw.text((1650, 49), "NOT CURRENT WORLD GEOMETRY", font=font(21, True), fill=(255, 224, 217, 255), anchor="ma")
    draw.text((1650, 80), "CALL02_ALLOWED = FALSE", font=font(18), fill=(255, 160, 148, 255), anchor="ma")

    add_panel(board, sources["ground"], (250, 220, 1150, 840), (40, 145, 920, 555), "GROUND VALUE + TILE RHYTHM", "legacy crop / donor only")
    add_panel(board, sources["buildings"], (90, 250, 760, 820), (990, 145, 890, 265), "BUILDING PLANE SEPARATION", "generic west-side crop")
    add_panel(board, sources["roofs"], (70, 250, 760, 650), (990, 435, 890, 265), "ROOF PLANE + EDGE LIGHT", "no object semantics")
    add_panel(board, sources["occlusion"], (110, 250, 760, 800), (40, 730, 510, 220), "LOCAL OCCLUSION MASK", "method evidence")
    add_panel(board, sources["foreground"], (180, 480, 720, 700), (580, 730, 510, 220), "LOW LIGHT-POST LAYER", "foreground method")

    draw.rounded_rectangle((1120, 730, 760 + 1120, 220 + 730), radius=18, fill=(10, 27, 35, 255), outline=(75, 116, 125, 255), width=2)
    rules = [
        "DO USE: ground value hierarchy, cool concrete, dark road,",
        "building face separation, roof-edge accents, local masks.",
        "DO NOT USE: old shield / exit / facility / rescue-line semantics.",
        "CURRENT TOPOLOGY: only producer-signed Task89 actual pixels.",
        "RAIN / WET FINISH: method target; not proven by these donor pixels.",
    ]
    for index, line in enumerate(rules):
        color = (244, 198, 115, 255) if index >= 2 else (212, 231, 231, 255)
        draw.text((1146, 756 + index * 33), line, font=font(19, index == 2), fill=color)

    draw.line((40, 992, 1880, 992), fill=(75, 116, 125, 255), width=2)
    footer = "BOARD ROLE: vocabulary extraction only — no target map, no current actor, no topology claim, no ImageGen input release"
    draw.text((960, 1033), footer, font=font(20, True), fill=(151, 201, 201, 255), anchor="mm")
    board.convert("RGB").save(OUT / "map-language-board.png", optimize=True)


def build_overlay_template() -> None:
    image = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    teal = (95, 216, 215, 232)
    amber = (244, 190, 89, 235)
    pale = (229, 240, 238, 244)
    quiet = (146, 176, 179, 225)
    panel = (5, 16, 23, 220)
    panel2 = (10, 29, 38, 214)

    # Screen-space UI bands only. The map viewport remains transparent.
    draw.rectangle((0, 0, 1280, 57), fill=panel)
    draw.line((0, 57, 1280, 57), fill=teal, width=2)
    draw.rectangle((0, 642, 1280, 719), fill=panel)
    draw.line((0, 642, 1280, 642), fill=teal, width=2)

    draw.text((22, 10), "目标｜让应急车通过，挡开扑向东门的小体，并站到冲线前。", font=font(19, True), fill=pale)
    draw.text((22, 37), "威胁｜应急车先穿过落脚区 · 小体第二时点扑向东门 · BREAKER直线冲入街区", font=font(15), fill=quiet)
    draw.rounded_rectangle((1004, 7, 1264, 50), radius=10, fill=panel2, outline=(75, 116, 125, 220), width=1)
    draw.text((1018, 15), "ROUTE FAMILY", font=font(12, True), fill=quiet)
    draw.text((1018, 31), "A 7步 / 余量1   B 6步 / 余量0", font=font(14, True), fill=amber)

    # PLAN-only comm box; CONTACT delivery removes this layer.
    draw.rounded_rectangle((18, 510, 320, 630), radius=14, fill=(6, 20, 28, 225), outline=(80, 139, 148, 225), width=2)
    draw.rectangle((30, 523, 84, 581), fill=(19, 48, 58, 220), outline=teal, width=1)
    draw.line((37, 571, 78, 530), fill=(61, 116, 124, 180), width=2)
    draw.text((99, 525), "纪存 / PLAN COMM", font=font(13, True), fill=teal)
    draw.text((99, 550), "人都在后面。", font=font(20, True), fill=pale)
    draw.text((99, 580), "把它引到南边去。", font=font(20, True), fill=pale)
    draw.text((30, 606), "CONTACT: REMOVE LARGE COMM LAYER", font=font(11), fill=quiet)

    labels = ["应急车", "小体", "巨体接触", "城市炮", "赤红蓄能"]
    centers = [420, 580, 740, 900, 1060]
    draw.line((370, 675, 1110, 675), fill=(77, 112, 119, 220), width=3)
    for idx, (label, x) in enumerate(zip(labels, centers)):
        color = teal if idx < 3 else amber
        draw.ellipse((x - 7, 668, x + 7, 682), fill=color, outline=(237, 247, 246, 230), width=1)
        draw.text((x, 650), f"T{idx + 1}", font=font(12, True), fill=color, anchor="mm")
        draw.text((x, 700), label, font=font(14), fill=pale, anchor="mm")
    draw.text((20, 669), "五时点", font=font(16, True), fill=pale)
    draw.text((1160, 662), "T4/T5", font=font(13, True), fill=amber)
    draw.text((1160, 685), "HUD FORECAST ONLY", font=font(12), fill=quiet)

    # Review-only viewport corner ticks. They are deterministic screen-space guides.
    for x, y, sx, sy in [(0, 58, 1, 1), (1279, 58, -1, 1), (0, 641, 1, -1), (1279, 641, -1, -1)]:
        draw.line((x, y, x + sx * 22, y), fill=(95, 216, 215, 150), width=2)
        draw.line((x, y, x, y + sy * 22), fill=(95, 216, 215, 150), width=2)

    image.save(OUT / "deterministic-overlay-ui-template-1280x720.png", optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if sha256(SAFE_SOURCE) != SAFE_EXPECTED_SHA:
        raise SystemExit("safe identity/style board SHA mismatch; no output permitted")
    for path in SOURCES.values():
        if not path.is_file():
            raise SystemExit(f"missing donor: {path}")

    shutil.copyfile(SAFE_SOURCE, OUT / "identity-style-safe-board.png")
    if sha256(OUT / "identity-style-safe-board.png") != SAFE_EXPECTED_SHA:
        raise SystemExit("byte-copy verification failed")

    build_map_language_board()
    build_overlay_template()


if __name__ == "__main__":
    main()
