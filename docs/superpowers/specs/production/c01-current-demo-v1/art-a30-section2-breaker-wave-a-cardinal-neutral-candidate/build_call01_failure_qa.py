#!/usr/bin/env python3
"""Build a read-only QA board for the stopped A30 EAST generation.

This script does not create a sprite and does not alter either source image.
It composites the current NORTH Candidate and the rejected EAST raw solely for
human inspection, then records the direction/alpha hard-gate result.
"""

from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[5]
NORTH = PROJECT / "game-godot/content/c01_breaker_demo/assets/candidate_ground_mecha/breaker_north_camera_v2_candidate.png"
EAST_RAW = ROOT / "call01/generation-raw/BREAKER_A30_CALL01_EAST_RAW_FAIL.png"
QA = ROOT / "call01/qa/BREAKER_A30_CALL01_EAST_HARD_GATE_FAIL_QA.png"
METADATA = ROOT / "call01/receipts/BREAKER_A30_CALL01_EAST_HARD_GATE_FAIL.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    choices = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for choice in choices:
        try:
            return ImageFont.truetype(choice, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def centroid(points: list[tuple[int, int]]) -> tuple[float, float]:
    return (
        sum(point[0] for point in points) / len(points),
        sum(point[1] for point in points) / len(points),
    )


def read_direction(path: Path) -> dict[str, object]:
    source = Image.open(path).convert("RGBA")
    dark: list[tuple[int, int]] = []
    red: list[tuple[int, int]] = []
    for y in range(source.height):
        for x in range(source.width):
            r, g, b, a = source.getpixel((x, y))
            if a >= 16 and max(r, g, b) < 180:
                dark.append((x, y))
            if a >= 16 and r >= 70 and r > g * 1.3 and r > b * 1.25 and r - g >= 20:
                red.append((x, y))
    subject = centroid(dark)
    accent = centroid(red)
    vector = (accent[0] - subject[0], accent[1] - subject[1])
    return {
        "subject_dark_centroid": [round(subject[0], 3), round(subject[1], 3)],
        "red_accent_centroid": [round(accent[0], 3), round(accent[1], 3)],
        "subject_to_red_vector": [round(vector[0], 3), round(vector[1], 3)],
        "angle_degrees_screen": round(math.degrees(math.atan2(vector[1], vector[0])), 3),
        "dark_sample_pixels": len(dark),
        "red_sample_pixels": len(red),
    }


def checker(size: tuple[int, int], cell: int = 32) -> Image.Image:
    output = Image.new("RGB", size, "#19212a")
    draw = ImageDraw.Draw(output)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#27313d")
    return output


def fit(image: Image.Image, box: tuple[int, int], padding: int) -> Image.Image:
    clone = image.copy()
    clone.thumbnail((box[0] - padding * 2, box[1] - padding * 2), Image.Resampling.LANCZOS)
    return clone


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str, width: int = 10) -> None:
    draw.line((*start, *end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 28
    wing = 0.65
    p1 = (int(end[0] - length * math.cos(angle - wing)), int(end[1] - length * math.sin(angle - wing)))
    p2 = (int(end[0] - length * math.cos(angle + wing)), int(end[1] - length * math.sin(angle + wing)))
    draw.polygon((end, p1, p2), fill=color)


def main() -> None:
    assert digest(NORTH) == "6b20111c80e3dc76adb5a05b55395359b7d1bdc2ec189060859058e53dbffde1"
    north = Image.open(NORTH).convert("RGBA")
    east_original = Image.open(EAST_RAW)
    east = east_original.convert("RGBA")
    north_read = read_direction(NORTH)
    east_read = read_direction(EAST_RAW)

    board = Image.new("RGB", (1800, 1040), "#0d1117")
    draw = ImageDraw.Draw(board)
    title = font(42, True)
    h2 = font(27, True)
    body = font(23, False)
    small = font(19, False)
    draw.text((60, 36), "BREAKER A30 / EAST HARD-GATE STOP", font=title, fill="#f2f5f7")
    draw.text((60, 94), "Current NORTH remains untouched. The generated EAST is rejected and never becomes a sprite.", font=body, fill="#c4ccd5")

    panels = [(60, 155, 840, 835), (960, 155, 1740, 835)]
    for panel in panels:
        draw.rounded_rectangle(panel, radius=18, fill="#151b23", outline="#46515f", width=3)

    north_bg = checker((720, 590))
    north_fit = fit(north, north_bg.size, 45)
    north_bg.paste(north_fit, ((720 - north_fit.width) // 2, (590 - north_fit.height) // 2), north_fit)
    board.paste(north_bg, (90, 205))

    east_bg = Image.new("RGB", (720, 590), "#202731")
    east_fit = fit(east, east_bg.size, 30)
    east_bg.paste(east_fit.convert("RGB"), ((720 - east_fit.width) // 2, (590 - east_fit.height) // 2))
    board.paste(east_bg, (990, 205))

    draw.text((88, 167), "CURRENT NORTH / KEEP", font=h2, fill="#71d995")
    draw.text((988, 167), "CALL01 EAST RAW / REJECT", font=h2, fill="#ff7272")

    # World-facing direction arrows, not inferred pixel transforms.
    arrow(draw, (355, 725), (500, 638), "#59d8ff")
    draw.text((292, 742), "NORTH [40,-24]", font=small, fill="#59d8ff")
    arrow(draw, (1290, 630), (1435, 717), "#59d8ff")
    draw.text((1260, 742), "EXPECTED EAST [40,24]", font=small, fill="#59d8ff")

    # Measured red-accent direction on EAST points toward lower-left.
    arrow(draw, (1320, 590), (1182, 654), "#ffb347")
    draw.text((1010, 682), "MEASURED RED ACCENT: LEFT-DOWN", font=small, fill="#ffb347")

    draw.rounded_rectangle((60, 870, 1740, 1000), radius=16, fill="#251619", outline="#ff7272", width=3)
    draw.text((86, 890), "STOP 1 / Direction polarity: the sole red slit remains left-down while EAST head end must be right-down.", font=body, fill="#ffd2d2")
    draw.text((86, 929), "STOP 2 / Alpha: output mode is RGB with baked checkerboard; no real transparency, including enclosed gaps.", font=body, fill="#ffd2d2")
    draw.text((86, 968), "Per Wave A contract: no SOUTH/WEST calls, no cleanup, no Godot/Runtime/Canon binding.", font=body, fill="#ffd2d2")

    QA.parent.mkdir(parents=True, exist_ok=True)
    board.save(QA)
    result = {
        "schema_id": "BREAKER_A30_WAVE_A_EAST_HARD_GATE_V1",
        "status": "STOPPED_AFTER_EAST_HARD_GATE_FAIL",
        "generation": {
            "mode": "built_in_imagegen",
            "calls_used": {"east": 1, "south": 0, "west": 0},
            "random_reroll_count": 0,
            "raw_path": str(EAST_RAW.relative_to(PROJECT)),
            "raw_sha256": digest(EAST_RAW),
            "raw_mode": east_original.mode,
            "raw_size": list(east_original.size),
        },
        "north_unchanged": {"path": str(NORTH.relative_to(PROJECT)), "sha256": digest(NORTH)},
        "direction_readback": {"north": north_read, "east_raw": east_read},
        "hard_gate_failures": [
            "east_head_red_slit_polarity_points_left_down_instead_of_required_right_down",
            "east_raw_is_rgb_with_baked_checkerboard_and_no_alpha_channel",
        ],
        "derived_candidate_count": 0,
        "south_generation_skipped": True,
        "west_generation_skipped": True,
        "runtime_allowed": False,
        "default_allowed": False,
        "canon_allowed": False,
        "qa_path": str(QA.relative_to(PROJECT)),
    }
    METADATA.parent.mkdir(parents=True, exist_ok=True)
    METADATA.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

