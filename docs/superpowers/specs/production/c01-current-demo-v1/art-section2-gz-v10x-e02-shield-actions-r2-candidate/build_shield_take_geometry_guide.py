#!/usr/bin/env python3
"""Build the identity-free shield_take/south geometry gate.

This is deliberately not character art. It only freezes the action silhouette,
occlusion order, Camera V2 south vector, and the rear-handle contact logic before
the single allowed ImageGen call.
"""

from __future__ import annotations

from pathlib import Path
from math import cos, radians, sin

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
GUIDE = ROOT / "guide"
QA = ROOT / "qa"
SCALE = 2
W = H = 1024


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def p(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(x * SCALE, y * SCALE) for x, y in points]


def ellipse(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], **kwargs: object) -> None:
    draw.ellipse(tuple(v * SCALE for v in box), **kwargs)


def line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], width: int, **kwargs: object) -> None:
    draw.line(p(points), width=width * SCALE, joint="curve", **kwargs)


def shield_space(points: list[tuple[int, int]], centre: tuple[int, int] = (350, 650), degrees: float = -22.0) -> list[tuple[int, int]]:
    """Rotate shield-local points into the deliberately low take position."""
    c = cos(radians(degrees))
    s = sin(radians(degrees))
    cx, cy = centre
    return [(round(cx + x * c - y * s), round(cy + x * s + y * c)) for x, y in points]


def pose_guide() -> Image.Image:
    canvas = Image.new("RGBA", (W * SCALE, H * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)

    # Soft footprint plane. It is a guide-only registration cue, not a prop.
    d.polygon(p([(390, 858), (650, 702), (814, 800), (555, 956)]), fill=(55, 75, 92, 34), outline=(83, 111, 132, 100))

    # Rear leg first: asymmetric step makes this a lift/turn transition, not a
    # square planted block.
    d.polygon(p([(585, 541), (665, 560), (696, 720), (630, 758), (571, 690)]), fill=(108, 118, 126, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(628, 742), (708, 732), (760, 782), (716, 824), (622, 814)]), fill=(90, 100, 108, 255), outline=(39, 47, 54, 255))

    # Lead leg is lower and loaded under the shield.
    d.polygon(p([(505, 536), (575, 552), (566, 733), (489, 779), (449, 689)]), fill=(129, 138, 145, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(478, 758), (563, 737), (602, 792), (547, 842), (449, 835)]), fill=(105, 115, 123, 255), outline=(39, 47, 54, 255))

    # Pelvis and torso lean down-left over the object being lifted.
    d.polygon(p([(493, 474), (599, 456), (646, 527), (576, 577), (486, 548)]), fill=(88, 98, 106, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(468, 279), (588, 252), (664, 336), (614, 483), (500, 501), (431, 398)]), fill=(120, 130, 138, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(460, 303), (542, 280), (611, 337), (580, 430), (494, 451), (449, 391)]), fill=(147, 154, 160, 255), outline=(62, 70, 77, 255))

    # Anonymous head block: orientation only, no GZ identity features.
    d.polygon(p([(478, 218), (535, 190), (584, 224), (570, 289), (510, 304), (467, 265)]), fill=(98, 108, 116, 255), outline=(39, 47, 54, 255))
    line(d, [(508, 251), (466, 276)], width=10, fill=(236, 177, 58, 255))

    # Both arm chains are drawn before the shield: their hands terminate behind
    # the rear/interior plane and must be fully occluded by the exterior face.
    ellipse(d, (405, 293, 490, 378), fill=(92, 102, 110, 255), outline=(39, 47, 54, 255))
    ellipse(d, (596, 290, 682, 377), fill=(92, 102, 110, 255), outline=(39, 47, 54, 255))
    line(d, [(445, 347), (383, 455), (330, 566)], width=48, fill=(105, 115, 123, 255))
    line(d, [(641, 348), (579, 467), (464, 643)], width=48, fill=(105, 115, 123, 255))
    # Rear handle contact points. These circles are hidden by the shield face.
    ellipse(d, (308, 544, 352, 588), fill=(236, 177, 58, 255), outline=(39, 47, 54, 255))
    ellipse(d, (442, 621, 486, 665), fill=(236, 177, 58, 255), outline=(39, 47, 54, 255))

    # Shield exterior: low, off-centre, slightly rolled and still rising. The
    # top remains below the head/shoulder line; bottom is just off the foot plane.
    shield = shield_space([(-100, -220), (70, -220), (150, -130), (145, 120), (50, 230), (-70, 210), (-150, 80), (-145, -130)])
    d.polygon(p(shield), fill=(31, 79, 124, 255), outline=(18, 31, 45, 255))
    d.line(p(shield + [shield[0]]), fill=(193, 203, 211, 255), width=18 * SCALE, joint="curve")
    shield_inner = shield_space([(-78, -187), (55, -187), (117, -110), (112, 92), (38, 188), (-52, 171), (-116, 62), (-111, -103)])
    d.polygon(p(shield_inner), fill=(53, 101, 145, 255), outline=(16, 43, 67, 255))
    line(d, shield_space([(0, -170), (0, 170)]), width=26, fill=(34, 52, 68, 255))
    # Exactly three cold, broad, shallow scars. No red/hot fourth mark.
    for pts in (
        [(-105, -92), (105, -92)],
        [(-113, 8), (112, 8)],
        [(-92, 108), (92, 108)],
    ):
        line(d, shield_space(pts), width=12, fill=(188, 201, 209, 235))

    # A little of each arm remains visible outside the edge; no hand or handle
    # is visible on the exterior face.
    line(d, [(441, 344), (394, 410)], width=34, fill=(113, 123, 131, 255))
    line(d, [(632, 350), (576, 444)], width=34, fill=(113, 123, 131, 255))

    return canvas.resize((W, H), Image.Resampling.LANCZOS)


def qa_board(pose: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1536, 1024), (18, 26, 35, 255))
    d = ImageDraw.Draw(board)
    d.text((40, 28), "SHIELD_TAKE / SOUTH · IDENTITY-FREE GEOMETRY GATE", font=font(30, True), fill=(246, 248, 250, 255))
    d.text((40, 68), "low + off-centre + rising; both contacts behind; cold shield = exactly 3 scars", font=font(19), fill=(190, 204, 215, 255))

    full = pose.resize((768, 768), Image.Resampling.LANCZOS)
    board.alpha_composite(full, (24, 146))
    d.text((40, 920), "100% geometry", font=font(20, True), fill=(242, 193, 66, 255))

    small = pose.resize((512, 512), Image.Resampling.LANCZOS)
    for idx, bg in enumerate(((238, 236, 230, 255), (8, 15, 24, 255))):
        x = 864
        y = 142 + idx * 416
        d.rounded_rectangle((x, y, x + 600, y + 374), radius=16, fill=bg)
        thumb = small.resize((374, 374), Image.Resampling.LANCZOS)
        board.alpha_composite(thumb, (x + 112, y))
    d.text((880, 930), "50% light/dark first-read", font=font(20, True), fill=(242, 193, 66, 255))

    # Direction vector is QA-only and is not present in the clean ImageGen guide.
    origin = (725, 820)
    end = (645, 868)
    d.line((origin, end), fill=(255, 194, 62, 255), width=6)
    d.polygon((end, (670, 863), (657, 842)), fill=(255, 194, 62, 255))
    d.text((608, 876), "SOUTH [-40,+24]", font=font(16, True), fill=(255, 214, 111, 255))
    return board


def main() -> None:
    GUIDE.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    pose = pose_guide()
    pose.save(GUIDE / "GZ_V10X_SHIELD_TAKE_SOUTH_IDENTITY_FREE_GEOMETRY_GUIDE_1024.png")
    pose.resize((512, 512), Image.Resampling.LANCZOS).save(GUIDE / "GZ_V10X_SHIELD_TAKE_SOUTH_IDENTITY_FREE_GEOMETRY_GUIDE_50PCT.png")
    qa_board(pose).save(QA / "GZ_V10X_SHIELD_TAKE_SOUTH_GEOMETRY_GATE_50_100_QA.png")


if __name__ == "__main__":
    main()
