#!/usr/bin/env python3
"""Build deterministic QA views for the stopped A31 ImageGen call.

This script never derives a Candidate sprite. It only compares the locked
Camera V2 south source against the single failed raw generation and proves
that the raw image has no alpha channel.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[6]
PACKAGE = Path(__file__).resolve().parent
RAW = PACKAGE / "call01/generation-raw/GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_BLOCK_SOUTH_BODY_ONLY_CALL01_RAW.png"
SOUTH = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png"
QA_DIR = PACKAGE / "call01/qa"

EXPECTED = {
    RAW: "77fd478233d4bdd1d0a81b807be4e5e0217d256e79097a4a4c22f8db3d272f7b",
    SOUTH: "d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int) -> ImageFont.ImageFont:
    candidates = (
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Helvetica.ttc"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def checker(size: tuple[int, int], cell: int = 24) -> Image.Image:
    canvas = Image.new("RGBA", size, (248, 248, 248, 255))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(204, 204, 210, 255))
    return canvas


def contain(image: Image.Image, bounds: tuple[int, int]) -> Image.Image:
    scale = min(bounds[0] / image.width, bounds[1] / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def build_direction_board() -> None:
    board = Image.new("RGB", (1600, 1000), (25, 28, 34))
    draw = ImageDraw.Draw(board)
    title = font(34)
    body = font(25)
    small = font(20)
    draw.text((42, 28), "A31 CALL01 FAIL-STOP — Camera V2 SOUTH contract", fill=(245, 245, 248), font=title)

    left_box = (42, 100, 760, 918)
    right_box = (840, 100, 1558, 918)
    draw.rounded_rectangle(left_box, radius=18, fill=(48, 53, 64), outline=(100, 108, 126), width=2)
    draw.rounded_rectangle(right_box, radius=18, fill=(48, 53, 64), outline=(235, 80, 80), width=4)
    draw.text((68, 122), "LOCKED SOURCE — PASSING SOUTH AXIS", fill=(140, 235, 170), font=body)
    draw.text((866, 122), "IMAGEGEN RAW — FAIL", fill=(255, 120, 120), font=body)

    south = Image.open(SOUTH).convert("RGBA")
    left_stage = checker((620, 620), 20)
    shown = contain(south, (560, 560))
    left_stage.alpha_composite(shown, ((620 - shown.width) // 2, (620 - shown.height) // 2))
    board.paste(left_stage.convert("RGB"), (92, 190))

    raw = Image.open(RAW).convert("RGB")
    shown_raw = contain(raw, (620, 620))
    board.paste(shown_raw, (889 + (620 - shown_raw.width) // 2, 190 + (620 - shown_raw.height) // 2))

    # Fixed Camera V2 south vector [-40,+24], scaled by five for legibility.
    start = (386, 420)
    end = (186, 540)
    draw.line((start, end), fill=(75, 220, 255), width=12)
    draw.polygon(((end[0], end[1]), (end[0] + 40, end[1] - 8), (end[0] + 20, end[1] - 40)), fill=(75, 220, 255))
    draw.text((112, 555), "SOUTH  [-40,+24]", fill=(90, 230, 255), font=body)

    draw.text((68, 858), "High-oblique map view; front axis reads lower-left.", fill=(225, 228, 235), font=small)
    draw.text((866, 820), "Front-orthographic hero view; not lower-left SOUTH.", fill=(255, 190, 190), font=small)
    draw.text((866, 852), "Top/side planes do not establish Camera V2 40x24.", fill=(255, 190, 190), font=small)
    draw.text((866, 884), "Hard gate: SOUTH = FAIL; no shield composite built.", fill=(255, 190, 190), font=small)
    board.save(QA_DIR / "CALL01_CAMERA_V2_SOUTH_FAIL_COMPARISON.png", optimize=True)


def build_alpha_board() -> None:
    raw = Image.open(RAW)
    # Deliberately convert the RGB raw to opaque RGBA; this is diagnostic only.
    opaque = raw.convert("RGBA")
    shown = contain(opaque, (330, 470))
    board = Image.new("RGB", (1600, 1000), (22, 24, 28))
    draw = ImageDraw.Draw(board)
    title = font(34)
    body = font(24)
    small = font(20)
    draw.text((42, 28), "A31 CALL01 FAIL-STOP — alpha/background diagnostic", fill=(245, 245, 248), font=title)
    backgrounds = (
        ("BLACK", Image.new("RGBA", (360, 500), (0, 0, 0, 255))),
        ("MAGENTA", Image.new("RGBA", (360, 500), (255, 0, 180, 255))),
        ("GREEN", Image.new("RGBA", (360, 500), (0, 210, 90, 255))),
        ("CHECKER", checker((360, 500), 20)),
    )
    for index, (label, stage) in enumerate(backgrounds):
        x = 42 + index * 389
        y = 140
        stage.alpha_composite(shown, ((stage.width - shown.width) // 2, (stage.height - shown.height) // 2))
        board.paste(stage.convert("RGB"), (x, y))
        draw.text((x, 106), label, fill=(225, 228, 235), font=body)
    draw.text((42, 690), "Observed PNG: 1024x1536, mode RGB, alpha channel absent.", fill=(255, 150, 150), font=body)
    draw.text((42, 734), "The light checker remains identical on every QA background because it is baked into RGB pixels.", fill=(255, 190, 190), font=body)
    draw.text((42, 778), "Hard gate: TRUE ALPHA = FAIL. No matting, threshold cutout, shield composite, or reroll is permitted.", fill=(255, 190, 190), font=body)
    draw.text((42, 858), f"raw sha256: {EXPECTED[RAW]}", fill=(170, 175, 188), font=small)
    board.save(QA_DIR / "CALL01_ALPHA_FAIL_DIAGNOSTIC.png", optimize=True)


def main() -> None:
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"source hash mismatch: {path}\nexpected {expected}\nactual   {actual}")
    QA_DIR.mkdir(parents=True, exist_ok=True)
    build_direction_board()
    build_alpha_board()
    print("PASS deterministic failure QA: 2 PNGs; Candidate outputs: 0")


if __name__ == "__main__":
    main()
