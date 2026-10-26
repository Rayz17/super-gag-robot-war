#!/usr/bin/env python3.13
"""Render the A7 Guardian C + BREAKER B/X identity lock review board.

The renderer validates every approved evidence file and every quarantined
exploration before drawing. Rejected explorations are never opened as images.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


W, H = 2400, 1600

BG = "#101820"
PANEL = "#17242d"
PANEL_ALT = "#1d2d36"
INK = "#ecf3f1"
MUTED = "#9fb2b5"
RULE = "#3f5960"
CYAN = "#5cd6cb"
RED = "#e7473c"
RED_DARK = "#7e2528"
GOLD = "#e8b83f"
GOLD_DARK = "#8e6d1e"
NAVY = "#294b66"
NAVY_DARK = "#162d42"
SILVER = "#c7d1d0"
STEEL = "#70848a"
BLACK = "#0a0d10"
BIO = "#294b4c"
BIO_DARK = "#162d31"
BIO_LIGHT = "#4e7771"
BIO_SEAM = "#72a79b"
WARNING = "#f0c66a"


def repo_root() -> Path:
    here = Path(__file__).resolve()
    marker = Path("docs/superpowers/specs/production/c01-current-demo-v1")
    for parent in here.parents:
        if (parent / marker).is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = repo_root()
TARGET = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a7-round-presentation"
OUTPUT = TARGET / "A7_IDENTITY_LOCK_GUARDIAN_C_BREAKER_BX_2400x1600.png"

APPROVED = {
    "Guardian C": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png",
        "4d8e7975649b2b85458a838afd9bc2fe8e3a90fd8cbcfe8a7929b8ae9ae6c225",
    ),
    "BREAKER B": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png",
        "7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868",
    ),
    "BREAKER X": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png",
        "cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85",
    ),
}

REJECTED = {
    "R05_CUTIN_SWARM_INTERCEPT_imagegen_source.png": "14da360aafc93e55507659a015afb87f1f24a8b23472ad9c01c2040ed0e5879c",
    "R05_CUTIN_GIANT_CONTACT_imagegen_source.png": "a01e55edf1d14ed3601dd2dac6b8c9c98f72f37eafe54a930978b4e5f9976bf1",
    "R05_CUTIN_ARTILLERY_SIDE_HIT_imagegen_source.png": "be01ab84be1ba19bf55975040a1b29254e759c9cfa53695e737660861b31b0d5",
    "R05_CUTIN_RED_CHARGE_imagegen_source.png": "8a1093377704ca6f9ba7345900cb6a0f65ecb2bca62d97a95363daaed63edcbd",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_inputs() -> None:
    for label, (path, expected) in APPROVED.items():
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"approved source hash mismatch: {label}: {actual}")
    quarantine = TARGET / "rejected-exploration/source"
    for name, expected in REJECTED.items():
        path = quarantine / name
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"rejected source byte drift: {name}: {actual}")


FONT_PATH = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")
FONT_BOLD_PATH = Path("/System/Library/Fonts/STHeiti Medium.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD_PATH if bold else FONT_PATH), size)


F12 = font(12)
F14 = font(14)
F16 = font(16)
F18 = font(18)
F20 = font(20)
F22 = font(22, True)
F26 = font(26, True)
F31 = font(31, True)
F42 = font(42, True)


def rr(draw: ImageDraw.ImageDraw, box, radius=10, fill=PANEL, outline=RULE, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw: ImageDraw.ImageDraw, xy, value, f=F16, fill=INK, anchor=None):
    draw.text(xy, value, font=f, fill=fill, anchor=anchor)


def centered(draw: ImageDraw.ImageDraw, box, value, f=F16, fill=INK):
    x1, y1, x2, y2 = box
    draw.text(((x1 + x2) / 2, (y1 + y2) / 2), value, font=f, fill=fill, anchor="mm")


def pill(draw: ImageDraw.ImageDraw, x, y, label, fill, fg=INK):
    bbox = draw.textbbox((0, 0), label, font=F14)
    width = bbox[2] - bbox[0] + 24
    draw.rounded_rectangle((x, y, x + width, y + 28), radius=6, fill=fill)
    text(draw, (x + 12, y + 14), label, F14, fg, "lm")
    return x + width + 8


def section_title(draw: ImageDraw.ImageDraw, x, y, code, title_value, accent):
    draw.rectangle((x, y, x + 8, y + 44), fill=accent)
    text(draw, (x + 22, y + 1), code, F16, accent)
    text(draw, (x + 22, y + 20), title_value, F26, INK)


def local_transform(cx, ground, scale, points, squash=1.0, shift=0.0):
    return [
        (int(cx + (x * squash + shift) * scale), int(ground - y * scale))
        for x, y in points
    ]


def guardian(draw: ImageDraw.ImageDraw, cx, ground, scale=1.0, view="front", pose="idle"):
    """Render the approved C silhouette: 4.2 heads, broad shoulders, compact limbs."""
    lean = -5 if pose in {"brace", "contact"} else 0

    def tp(points):
        return local_transform(cx, ground, scale, points, 1.0, lean)

    def poly(points, fill, outline=BLACK, width=2):
        pts = tp(points)
        draw.polygon(pts, fill=fill)
        draw.line(pts + [pts[0]], fill=outline, width=max(1, int(width * scale)), joint="curve")

    def ellipse(box, fill, outline=BLACK, width=2):
        x1, y1, x2, y2 = box
        a = tp([(x1, y2)])[0]
        b = tp([(x2, y1)])[0]
        draw.ellipse((a[0], a[1], b[0], b[1]), fill=fill, outline=outline, width=max(1, int(width * scale)))

    def line(points, fill, width=2):
        draw.line(tp(points), fill=fill, width=max(1, int(width * scale)), joint="curve")

    def grille(x1, x2, y1, y2):
        poly([(x1, y1), (x2, y1), (x2 - 3, y2), (x1 + 3, y2)], SILVER)
        for gx in range(int(x1 + 8), int(x2 - 2), 10):
            line([(gx, y1 + 4), (gx - 1, y2 - 4)], "#41545d", 2)

    stance = 18 if pose in {"brace", "contact"} else 0
    hand_raise = 28 if pose == "brace" else 16 if pose == "contact" else 0
    draw.ellipse((cx - 126 * scale, ground - 9 * scale, cx + 126 * scale, ground + 8 * scale), fill="#081013")

    if view == "front":
        # Short block legs: each foot and shin read as one compact SD mass.
        poly([(-68 - stance, 5), (-22 - stance, 5), (-20, 33), (-63, 36)], NAVY_DARK)
        poly([(22 + stance, 5), (68 + stance, 5), (63, 36), (20, 33)], NAVY_DARK)
        poly([(-62, 34), (-20, 34), (-16, 82), (-54, 82)], NAVY)
        poly([(20, 34), (62, 34), (54, 82), (16, 82)], NAVY)
        poly([(-53, 78), (-17, 78), (-11, 119), (-48, 119)], SILVER)
        poly([(17, 78), (53, 78), (48, 119), (11, 119)], SILVER)
        ellipse((-51, 94, -13, 127), GOLD_DARK)
        ellipse((13, 94, 51, 127), GOLD_DARK)

        # Square shoulder blocks and both complete dark-blue cylindrical forearms.
        poly([(-124, 181), (-124, 235), (-112, 249), (-75, 249), (-63, 237), (-63, 185)], NAVY_DARK)
        poly([(63, 185), (63, 237), (75, 249), (112, 249), (124, 235), (124, 181)], NAVY_DARK)
        poly([(-116, 168), (-69, 168), (-66, 196), (-113, 199)], RED)
        poly([(69, 168), (116, 168), (113, 199), (66, 196)], RED_DARK)
        poly([(-110, 80 + hand_raise), (-72, 80 + hand_raise), (-70, 168), (-112, 168)], NAVY)
        poly([(72, 80 + hand_raise), (110, 80 + hand_raise), (112, 168), (70, 168)], NAVY)
        poly([(-101, 88 + hand_raise), (-88, 88 + hand_raise), (-88, 160), (-101, 160)], "#355f7b", None, 0)
        poly([(87, 88 + hand_raise), (100, 88 + hand_raise), (100, 160), (87, 160)], "#355f7b", None, 0)
        poly([(-113, 72 + hand_raise), (-68, 72 + hand_raise), (-68, 91 + hand_raise), (-113, 91 + hand_raise)], SILVER)
        poly([(68, 72 + hand_raise), (113, 72 + hand_raise), (113, 91 + hand_raise), (68, 91 + hand_raise)], SILVER)
        poly([(-111, 48 + hand_raise), (-70, 48 + hand_raise), (-66, 72 + hand_raise), (-114, 72 + hand_raise)], NAVY_DARK)
        poly([(70, 48 + hand_raise), (111, 48 + hand_raise), (114, 72 + hand_raise), (66, 72 + hand_raise)], NAVY_DARK)
        for fx in (-102, -92, -82, 82, 92, 102):
            line([(fx, 53 + hand_raise), (fx, 69 + hand_raise)], SILVER, 2)

        # Thick red chest armor on a wide navy abdomen.
        poly([(-72, 215), (-13, 226), (0, 207), (0, 136), (-57, 145), (-79, 171)], RED)
        poly([(72, 215), (13, 226), (0, 207), (0, 136), (57, 145), (79, 171)], RED_DARK)
        poly([(-57, 145), (0, 136), (57, 145), (48, 113), (-48, 113)], NAVY_DARK)
        poly([(-13, 222), (13, 222), (13, 142), (-13, 142)], SILVER)
        ellipse((-18, 168, 18, 204), GOLD, GOLD_DARK, 3)
        ellipse((-9, 177, 9, 195), "#fff0a0", GOLD_DARK, 2)
        poly([(-8, 105), (8, 105), (8, 137), (-8, 137)], GOLD, GOLD_DARK, 2)

        # Wide head and silver grille keep the approved C face read.
        poly([(-36, 226), (36, 226), (36, 278), (21, 299), (-21, 299), (-36, 278)], NAVY_DARK)
        grille(-27, 27, 236, 270)
        poly([(-11, 270), (11, 270), (14, 307), (0, 319), (-14, 307)], RED)
        line([(-63, 290), (-28, 280), (0, 294), (29, 280), (63, 290)], GOLD, 8)
        ellipse((-35, 273, -25, 283), GOLD)
        ellipse((25, 273, 35, 283), GOLD)

        # Robot-right shoulder is viewer-left: old wound only, not arm loss.
        line([(-106, 227), (-91, 211), (-101, 198)], "#e4a084", 4)
        return

    if view == "three_quarter":
        # Far side is smaller, near side stays square and heavy.
        poly([(-53 - stance, 5), (-13 - stance, 5), (-10, 34), (-49, 36)], NAVY_DARK)
        poly([(21 + stance, 5), (70 + stance, 5), (65, 37), (20, 34)], NAVY_DARK)
        poly([(-48, 34), (-10, 34), (-6, 82), (-43, 82)], NAVY)
        poly([(20, 34), (64, 34), (55, 84), (14, 82)], NAVY)
        poly([(-43, 78), (-8, 78), (-3, 117), (-39, 117)], SILVER)
        poly([(16, 78), (55, 78), (50, 120), (11, 117)], SILVER)
        ellipse((-41, 94, -6, 126), GOLD_DARK)
        ellipse((13, 95, 52, 129), GOLD_DARK)

        poly([(-109, 187), (-109, 232), (-98, 245), (-68, 245), (-58, 233), (-58, 189)], NAVY_DARK)
        poly([(59, 183), (59, 238), (73, 253), (116, 253), (129, 237), (128, 178)], NAVY_DARK)
        poly([(-102, 169), (-62, 169), (-59, 196), (-100, 199)], RED)
        poly([(68, 165), (120, 165), (119, 201), (64, 195)], RED_DARK)
        poly([(-98, 82 + hand_raise), (-64, 82 + hand_raise), (-62, 169), (-101, 169)], NAVY)
        poly([(71, 80 + hand_raise), (113, 80 + hand_raise), (120, 165), (68, 165)], NAVY)
        poly([(-101, 51 + hand_raise), (-61, 51 + hand_raise), (-59, 80 + hand_raise), (-103, 80 + hand_raise)], NAVY_DARK)
        poly([(68, 49 + hand_raise), (115, 49 + hand_raise), (117, 80 + hand_raise), (66, 80 + hand_raise)], NAVY_DARK)
        for fx in (-91, -81, -71, 79, 90, 102):
            line([(fx, 55 + hand_raise), (fx, 75 + hand_raise)], SILVER, 2)

        poly([(-64, 215), (-5, 228), (12, 207), (9, 137), (-48, 145), (-72, 171)], RED)
        poly([(75, 217), (14, 228), (12, 207), (9, 137), (64, 147), (87, 174)], RED_DARK)
        poly([(-48, 145), (9, 137), (64, 147), (54, 113), (-42, 113)], NAVY_DARK)
        poly([(-5, 223), (22, 223), (21, 142), (-5, 142)], SILVER)
        ellipse((-10, 169, 27, 206), GOLD, GOLD_DARK, 3)
        ellipse((-1, 178, 18, 197), "#fff0a0", GOLD_DARK, 2)
        poly([(0, 105), (16, 105), (16, 138), (0, 138)], GOLD, GOLD_DARK, 2)

        poly([(-29, 227), (43, 227), (43, 279), (27, 300), (-14, 300), (-29, 279)], NAVY_DARK)
        grille(-20, 34, 237, 271)
        poly([(-3, 271), (18, 271), (20, 308), (7, 320), (-7, 307)], RED)
        line([(-55, 291), (-20, 281), (7, 295), (35, 282), (64, 291)], GOLD, 8)
        line([(-91, 226), (-78, 210), (-87, 198)], "#e4a084", 4)
        return

    # Side view retains the same short limbs, thick chest and both intact forearms.
    poly([(-34, 5), (12, 5), (15, 36), (-28, 37)], NAVY_DARK)
    poly([(-28, 34), (10, 34), (14, 81), (-24, 82)], NAVY)
    poly([(-22, 78), (12, 78), (18, 118), (-17, 118)], SILVER)
    ellipse((-20, 95, 17, 128), GOLD_DARK)
    poly([(16, 12), (58, 12), (54, 41), (15, 39)], NAVY_DARK)
    poly([(17, 38), (54, 38), (48, 84), (13, 82)], NAVY)

    # Far complete arm behind the torso.
    poly([(35, 182), (70, 181), (73, 232), (58, 246), (30, 239)], NAVY_DARK)
    poly([(45, 80 + hand_raise), (76, 80 + hand_raise), (72, 181), (39, 181)], NAVY)
    poly([(41, 50 + hand_raise), (78, 50 + hand_raise), (79, 80 + hand_raise), (39, 80 + hand_raise)], NAVY_DARK)

    poly([(-48, 215), (26, 221), (54, 194), (47, 141), (-17, 132), (-54, 158)], RED)
    poly([(-17, 132), (47, 141), (41, 112), (-33, 112)], NAVY_DARK)
    ellipse((4, 165, 39, 200), GOLD, GOLD_DARK, 3)
    ellipse((13, 174, 30, 191), "#fff0a0", GOLD_DARK, 2)

    poly([(-39, 228), (32, 228), (40, 277), (21, 300), (-18, 299), (-38, 278)], NAVY_DARK)
    grille(-28, 26, 238, 271)
    poly([(-8, 271), (12, 271), (16, 309), (3, 320), (-10, 307)], RED)
    line([(-55, 290), (-22, 282), (3, 295), (29, 283), (54, 290)], GOLD, 8)

    poly([(-78, 183), (-42, 183), (-40, 238), (-52, 251), (-82, 241)], NAVY_DARK)
    poly([(-73, 80 + hand_raise), (-42, 80 + hand_raise), (-42, 183), (-76, 183)], NAVY)
    poly([(-76, 50 + hand_raise), (-39, 50 + hand_raise), (-39, 80 + hand_raise), (-78, 80 + hand_raise)], NAVY_DARK)
    for fx in (-67, -58, -49):
        line([(fx, 55 + hand_raise), (fx, 75 + hand_raise)], SILVER, 2)
    line([(-69, 226), (-55, 210), (-64, 198)], "#e4a084", 4)


def breaker(draw: ImageDraw.ImageDraw, cx, ground, scale=1.0, view="front", state="idle"):
    """Render B structure with X curved shell language and an independent low head."""
    glow = state == "red_charge_only"
    drop = -5 if state in {"brace", "contact"} else 0

    def tp(points):
        return local_transform(cx, ground, scale, points, 1.0, 0)

    def poly(points, fill, outline=BLACK, width=2):
        pts = tp(points)
        draw.polygon(pts, fill=fill)
        if outline:
            draw.line(pts + [pts[0]], fill=outline, width=max(1, int(width * scale)), joint="curve")

    def ellipse(box, fill, outline=BLACK, width=2):
        x1, y1, x2, y2 = box
        a = tp([(x1, y2)])[0]
        b = tp([(x2, y1)])[0]
        draw.ellipse((a[0], a[1], b[0], b[1]), fill=fill, outline=outline, width=max(1, int(width * scale)))

    def line(points, fill, width=2):
        draw.line(tp(points), fill=fill, width=max(1, int(width * scale)), joint="curve")

    def head_block(points, seam_points):
        # The complete outlined block separates the head seam from the chest seam.
        poly(points, "#14262c", "#071014", 5)
        if glow:
            for width, color in ((16, "#5e191d"), (10, "#a9282c"), (5, "#ff6158")):
                line(seam_points, color, width)
        else:
            line(seam_points, "#ff5047", 6)

    draw.ellipse((cx - 170 * scale, ground - 10 * scale, cx + 170 * scale, ground + 8 * scale), fill="#081013")

    if view == "front":
        # Inner rear legs are columns under the shell, distinct from outer forelimbs.
        poly([(-75, 108), (-36, 108), (-34, 24), (-72, 24)], "#244247")
        poly([(36, 108), (75, 108), (72, 24), (34, 24)], "#244247")
        poly([(-78, 4), (-32, 4), (-32, 27), (-80, 27)], "#102126")
        poly([(32, 4), (78, 4), (80, 27), (32, 27)], "#102126")
        poly([(-57, 7), (-48, 7), (-48, 25), (-57, 25)], STEEL, None)
        poly([(48, 7), (57, 7), (57, 25), (48, 25)], STEEL, None)

        # High-back B mass with curved X outer contour and asymmetric plate joins.
        shell = [(-150, 151), (-154, 184), (-143, 222), (-124, 260), (-92, 289), (-42, 307), (10, 315), (64, 302), (109, 278), (139, 242), (154, 196), (151, 158), (108, 136), (-108, 136)]
        poly(shell, BIO_DARK, "#071014", 5)
        poly([(-133, 164), (-129, 213), (-100, 255), (-48, 282), (8, 292), (13, 143), (-95, 143)], BIO)
        poly([(13, 143), (8, 292), (60, 280), (105, 250), (136, 205), (133, 164), (96, 143)], BIO_LIGHT)
        line([(-112, 183), (-57, 216), (7, 211), (57, 231), (116, 197)], BIO_SEAM, 3)

        # Closed chest panel is separate and lower than the head block.
        poly([(-67, 151), (67, 151), (55, 90), (0, 70), (-55, 90)], "#1b3036", "#071014", 4)
        line([(0, 137), (0, 84)], "#597076", 3)
        line([(-4, 132), (-4, 88)], "#0a1418", 2)

        # Shoulder-shell underhang frames a genuinely independent low head block.
        poly([(-83, 205), (-61, 226), (61, 226), (83, 205), (67, 183), (-67, 183)], "#0d1b20", None)
        head_block([(-69, 183), (-60, 217), (-45, 229), (45, 229), (60, 217), (69, 183), (57, 162), (-57, 162)], [(-42, 191), (42, 191)])

        # Outer forelimbs reach the floor and carry the high shell.
        poly([(-145, 184), (-101, 187), (-95, 92), (-118, 23 + drop), (-154, 31 + drop), (-148, 112)], BIO)
        poly([(145, 184), (101, 187), (95, 92), (118, 23 + drop), (154, 31 + drop), (148, 112)], BIO_LIGHT)
        poly([(-158, 14 + drop), (-116, 14 + drop), (-111, 33 + drop), (-154, 34 + drop)], "#102126")
        poly([(116, 14 + drop), (158, 14 + drop), (154, 34 + drop), (111, 33 + drop)], "#102126")
        line([(-137, 102), (-128, 53)], BIO_SEAM, 3)
        line([(137, 102), (128, 53)], BIO_SEAM, 3)
        return

    if view == "three_quarter":
        # Rear columns remain vertical while the forelimbs sit outside the body mass.
        poly([(20, 112), (58, 108), (56, 25), (18, 25)], BIO_DARK)
        poly([(78, 116), (112, 103), (118, 25), (82, 22)], BIO_DARK)
        poly([(15, 5), (59, 5), (60, 28), (14, 28)], "#102126")
        poly([(80, 4), (123, 4), (122, 27), (78, 27)], "#102126")
        poly([(34, 7), (43, 7), (43, 26), (34, 26)], STEEL, None)
        poly([(95, 6), (104, 6), (104, 25), (95, 25)], STEEL, None)

        shell = [(-113, 144), (-125, 176), (-116, 225), (-91, 269), (-50, 303), (5, 315), (68, 307), (123, 282), (158, 246), (166, 198), (154, 158), (105, 132), (-72, 128)]
        poly(shell, BIO_DARK, "#071014", 5)
        poly([(-99, 158), (-101, 207), (-70, 259), (-20, 289), (37, 296), (48, 137), (-67, 137)], BIO)
        poly([(48, 137), (37, 296), (91, 282), (136, 249), (153, 205), (140, 163), (104, 141)], BIO_LIGHT)
        line([(-84, 184), (-28, 219), (38, 211), (92, 235), (142, 201)], BIO_SEAM, 3)

        poly([(-23, 154), (92, 151), (83, 94), (32, 76), (-21, 96)], "#1b3036", "#071014", 4)
        line([(31, 137), (32, 88)], "#597076", 3)

        # Head projects forward from under the near shoulder; red seam lives here.
        poly([(-139, 209), (-113, 230), (-47, 222), (-29, 191), (-49, 172), (-122, 175)], "#0d1b20", None)
        head_block([(-157, 178), (-153, 211), (-137, 224), (-68, 224), (-50, 211), (-53, 179), (-70, 165), (-139, 165)], [(-137, 190), (-75, 190)])

        poly([(-112, 183), (-73, 179), (-67, 91), (-92, 22 + drop), (-128, 30 + drop), (-121, 111)], BIO_LIGHT)
        poly([(124, 183), (94, 173), (97, 89), (118, 24 + drop), (151, 30 + drop), (142, 108)], BIO)
        poly([(-133, 13 + drop), (-91, 13 + drop), (-86, 32 + drop), (-128, 34 + drop)], "#102126")
        poly([(115, 14 + drop), (155, 14 + drop), (151, 33 + drop), (111, 33 + drop)], "#102126")
        line([(-102, 101), (-94, 52)], BIO_SEAM, 3)
        return

    # Strict side profile from B: high back, forward head block, one forelimb,
    # two rear columns. X changes the shell surface, not these relationships.
    poly([(31, 119), (68, 112), (68, 26), (31, 26)], BIO_DARK)
    poly([(94, 121), (126, 106), (132, 25), (99, 22)], BIO_DARK)
    poly([(28, 5), (72, 5), (72, 28), (27, 28)], "#102126")
    poly([(96, 4), (139, 4), (138, 27), (94, 27)], "#102126")
    poly([(46, 7), (55, 7), (55, 26), (46, 26)], STEEL, None)
    poly([(111, 6), (120, 6), (120, 25), (111, 25)], STEEL, None)

    shell = [(-106, 139), (-124, 174), (-119, 223), (-92, 269), (-45, 304), (18, 315), (79, 306), (132, 277), (161, 236), (166, 190), (151, 150), (106, 128), (-70, 126)]
    poly(shell, BIO_DARK, "#071014", 5)
    poly([(-91, 151), (-98, 205), (-64, 259), (-9, 291), (45, 296), (53, 135), (-63, 135)], BIO)
    poly([(53, 135), (45, 296), (96, 281), (137, 248), (152, 204), (139, 161), (104, 139)], BIO_LIGHT)
    line([(-77, 181), (-20, 218), (45, 210), (98, 234), (141, 199)], BIO_SEAM, 3)

    poly([(-21, 153), (91, 150), (84, 96), (35, 78), (-18, 97)], "#1b3036", "#071014", 4)
    line([(34, 136), (35, 89)], "#597076", 3)

    poly([(-151, 208), (-128, 228), (-58, 221), (-39, 192), (-59, 174), (-133, 176)], "#0d1b20", None)
    head_block([(-177, 177), (-173, 210), (-157, 222), (-88, 222), (-69, 209), (-73, 178), (-90, 164), (-159, 164)], [(-157, 189), (-95, 189)])

    poly([(-105, 182), (-67, 178), (-61, 91), (-87, 21 + drop), (-123, 30 + drop), (-115, 111)], BIO_LIGHT)
    poly([(-128, 12 + drop), (-86, 12 + drop), (-81, 32 + drop), (-123, 34 + drop)], "#102126")
    line([(-96, 100), (-88, 51)], BIO_SEAM, 3)


def palette_row(draw, x, y, colors):
    for name, color in colors:
        draw.rectangle((x, y, x + 25, y + 25), fill=color, outline=RULE, width=1)
        text(draw, (x + 33, y + 13), name, F12, MUTED, "lm")
        x += 112


def draw_view_panel(draw, x1, y1, x2, y2, label, actor):
    rr(draw, (x1, y1, x2, y2), 8, "#132028", "#30464d", 1)
    text(draw, ((x1 + x2) / 2, y1 + 24), label, F16, MUTED, "mm")
    if actor == "guardian":
        guardian(draw, (x1 + x2) / 2, y2 - 24, 1.08, label)
    else:
        breaker(draw, (x1 + x2) / 2, y2 - 22, 0.92, label)


def iso_point(origin, i, j, tile_w=40, tile_h=20):
    ox, oy = origin
    return ox + (i - j) * tile_w / 2, oy + (i + j) * tile_h / 2


def draw_iso_grid(draw, origin, cols=11, rows=9):
    for i in range(cols + 1):
        draw.line([iso_point(origin, i, 0), iso_point(origin, i, rows)], fill="#385158", width=1)
    for j in range(rows + 1):
        draw.line([iso_point(origin, 0, j), iso_point(origin, cols, j)], fill="#385158", width=1)


def iso_tile_block(draw, origin, i0, j0, size, fill, outline):
    pts = [
        iso_point(origin, i0, j0),
        iso_point(origin, i0 + size, j0),
        iso_point(origin, i0 + size, j0 + size),
        iso_point(origin, i0, j0 + size),
    ]
    draw.polygon(pts, fill=fill, outline=outline)


def evidence_strip(canvas, draw, x, y, label, path, digest, accent):
    rr(draw, (x, y, x + 748, y + 150), 7, "#111d24", "#344950", 1)
    with Image.open(path) as src:
        thumb = ImageOps.contain(src.convert("RGBA"), (235, 120), Image.Resampling.LANCZOS)
    thumb_x = x + 12 + (235 - thumb.width) // 2
    thumb_y = y + 15 + (120 - thumb.height) // 2
    canvas.alpha_composite(thumb, (thumb_x, thumb_y))
    draw.rectangle((x + 12, y + 15, x + 247, y + 135), outline=RULE, width=1)
    text(draw, (x + 265, y + 20), label, F18, accent)
    text(draw, (x + 265, y + 49), "READ-ONLY APPROVED EVIDENCE", F12, MUTED)
    text(draw, (x + 265, y + 77), "SHA256", F12, MUTED)
    text(draw, (x + 265, y + 95), digest[:32], F12, INK)
    text(draw, (x + 265, y + 113), digest[32:], F12, INK)


def draw_board() -> Image.Image:
    canvas = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # Header and explicit claim boundary.
    draw.rectangle((0, 0, W, 96), fill="#0a1218")
    draw.rectangle((0, 92, W, 96), fill=CYAN)
    text(draw, (40, 19), "A7 JOINT IDENTITY LOCK", F42, INK)
    text(draw, (650, 29), "GUARDIAN C  ×  BREAKER B+X", F31, CYAN)
    x = 1724
    x = pill(draw, x, 19, "CANDIDATE", "#315867")
    x = pill(draw, x, 19, "PARENT REVIEW", "#765b22", WARNING)
    text(draw, (2360, 68), "review_revision=R2  ·  runtime_allowed=false  ·  runtime_handoff=none  ·  NOT U1 READY", F14, WARNING, "ra")

    # Guardian identity panel.
    rr(draw, (40, 120, 1180, 850), 10, PANEL, RULE, 2)
    section_title(draw, 66, 142, "GZ / C", "馆守 Z · C 动作骨架", GOLD)
    text(draw, (1148, 152), "18m  ·  2×2", F18, GOLD, "ra")
    for box, label in zip(((66, 202, 414, 630), (426, 202, 774, 630), (786, 202, 1134, 630)), ("front", "three_quarter", "side")):
        draw_view_panel(draw, *box, label, "guardian")
    text(draw, (68, 656), "IDENTITY LOCKS", F14, GOLD)
    text(draw, (68, 681), "金色横冠  ·  红色中脊  ·  银色栅格脸  ·  红胸甲  ·  圆形金胸核", F16, INK)
    text(draw, (68, 708), "约 4.2 头身  ·  宽方肩厚红胸  ·  双深蓝圆筒前臂/拳完整  ·  右肩旧伤", F16, INK)
    text(draw, (68, 739), "R0.5 STOP: 右前臂尚未最终报废", F18, WARNING)
    text(draw, (68, 771), "FORBID: 现代尖锐英雄机甲 / 提前断臂 / 身份随镜头改型", F14, MUTED)
    palette_row(draw, 68, 804, (("NAVY", NAVY), ("RED", RED), ("GOLD", GOLD), ("SILVER", SILVER)))

    # BREAKER identity panel.
    rr(draw, (1220, 120, 2360, 850), 10, PANEL_ALT, RULE, 2)
    section_title(draw, 1246, 142, "BREAKER / B+X", "前肢承重 × 异质生体甲", CYAN)
    text(draw, (2328, 152), "近 30m  ·  3×3", F18, CYAN, "ra")
    for box, label in zip(((1246, 202, 1594, 630), (1606, 202, 1954, 630), (1966, 202, 2314, 630)), ("front", "three_quarter", "side")):
        draw_view_panel(draw, *box, label, "breaker")
    text(draw, (1248, 656), "IDENTITY LOCKS", F14, CYAN)
    text(draw, (1248, 681), "B: 前肢承重  ·  半直立  ·  低位钻压轮廓  ·  巨型上壳", F16, INK)
    text(draw, (1248, 708), "X: 非对称弧形叠甲  ·  稀疏柔性接缝  ·  异质生体曲面", F16, INK)
    text(draw, (1248, 739), "无眼单红缝  ·  胸缝闭合  ·  红光只在壳内蓄能", F18, WARNING)
    text(draw, (1248, 771), "FORBID: 人形黑机 / 普通四足兽 / 光滑蜘蛛 / 眼罩机器人", F14, MUTED)
    palette_row(draw, 1248, 804, (("BIO", BIO), ("DARK", BIO_DARK), ("SEAM", BIO_SEAM), ("RED", RED)))

    # Shared scale lock on a 40x20 isometric grid.
    rr(draw, (40, 878, 826, 1314), 10, PANEL, RULE, 2)
    section_title(draw, 66, 898, "SCALE", "同屏比例锁", WARNING)
    text(draw, (794, 907), "40×20 ISO TILE", F14, MUTED, "ra")
    origin = (370, 986)
    draw_iso_grid(draw, origin)
    iso_tile_block(draw, origin, 1, 5, 2, "#4f4122", GOLD)
    iso_tile_block(draw, origin, 6, 1, 3, "#214c49", CYAN)
    guardian(draw, 268, 1257, 0.42, "three_quarter", "brace")
    breaker(draw, 604, 1258, 0.68, "three_quarter", "idle")
    text(draw, (165, 1278), "馆守 Z", F18, GOLD, "mm")
    text(draw, (165, 1298), "18m · 2×2", F14, MUTED, "mm")
    text(draw, (630, 1278), "BREAKER", F18, CYAN, "mm")
    text(draw, (630, 1298), "近 30m · 3×3", F14, MUTED, "mm")

    # Four continuity thumbnails.
    rr(draw, (846, 878, 1800, 1314), 10, PANEL_ALT, RULE, 2)
    section_title(draw, 872, 898, "CONTINUITY", "同身份动作缩略", CYAN)
    thumb_labels = ("idle", "brace", "contact", "red_charge_only")
    for idx, label in enumerate(thumb_labels):
        x1 = 872 + idx * 228
        x2 = x1 + 212
        rr(draw, (x1, 958, x2, 1284), 7, "#111d24", "#344950", 1)
        text(draw, ((x1 + x2) / 2, 981), label, F14, WARNING if label == "red_charge_only" else MUTED, "mm")
        if label == "idle":
            guardian(draw, x1 + 55, 1257, 0.38, "three_quarter", "idle")
            breaker(draw, x1 + 154, 1258, 0.32, "three_quarter", "idle")
        elif label == "brace":
            guardian(draw, x1 + 57, 1257, 0.38, "three_quarter", "brace")
            breaker(draw, x1 + 155, 1258, 0.32, "three_quarter", "brace")
        elif label == "contact":
            guardian(draw, x1 + 73, 1257, 0.38, "three_quarter", "contact")
            breaker(draw, x1 + 148, 1258, 0.31, "side", "contact")
        else:
            guardian(draw, x1 + 55, 1257, 0.37, "three_quarter", "brace")
            breaker(draw, x1 + 155, 1258, 0.32, "three_quarter", "red_charge_only")
            text(draw, ((x1 + x2) / 2, 1270), "NO BEAM / NO RELEASE", F12, WARNING, "mm")

    # Stop-state checks: contained red charge and shield still mounted with 3 marks.
    rr(draw, (1820, 878, 2360, 1314), 10, PANEL, RULE, 2)
    section_title(draw, 1846, 898, "STOP STATE", "红光与墙挂盾", RED)
    rr(draw, (1846, 958, 2088, 1284), 7, "#111d24", "#344950", 1)
    breaker(draw, 1967, 1197, 0.43, "front", "red_charge_only")
    text(draw, (1967, 1225), "CHARGE ONLY", F16, RED, "mm")
    text(draw, (1967, 1251), "无束流 · 无释放", F14, MUTED, "mm")

    rr(draw, (2104, 958, 2334, 1284), 7, "#111d24", "#344950", 1)
    draw.rectangle((2124, 995, 2314, 1234), fill="#263139", outline="#596970", width=3)
    draw.line((2146, 1008, 2146, 1216), fill="#53646b", width=5)
    draw.line((2292, 1008, 2292, 1216), fill="#53646b", width=5)
    draw.line((2172, 1024, 2172, 1060), fill=STEEL, width=7)
    draw.line((2266, 1024, 2266, 1060), fill=STEEL, width=7)
    shield = [(2156, 1050), (2282, 1050), (2272, 1164), (2219, 1214), (2166, 1164)]
    draw.polygon(shield, fill="#5d6b70", outline=SILVER)
    draw.line(shield + [shield[0]], fill="#bac5c4", width=3)
    draw.ellipse((2201, 1100, 2237, 1136), fill="#2e383c", outline="#1a2124", width=2)
    # Exactly three old scorch marks, numbered for auditability.
    scorch_marks = ((2181, 1085, 1), (2251, 1124, 2), (2203, 1171, 3))
    for sx, sy, number in scorch_marks:
        draw.ellipse((sx - 13, sy - 9, sx + 13, sy + 9), fill="#2b2320", outline="#8a5b3b", width=2)
        text(draw, (sx, sy), str(number), F12, "#d8b08b", "mm")
    text(draw, (2219, 1251), "WALL-HUNG · 3 OLD SCORCHES", F12, WARNING, "mm")
    text(draw, (1848, 1295), "STOP: no shield pickup · no crimson impact · no shield strike · no P1", F12, MUTED)

    # Approved evidence strip. Rejected explorations are deliberately absent.
    rr(draw, (40, 1332, 2360, 1572), 10, "#0e171d", RULE, 2)
    text(draw, (66, 1350), "APPROVED READ-ONLY EVIDENCE  ·  rejected exploration excluded from render inputs", F16, MUTED)
    for index, (label, (path, digest)) in enumerate(APPROVED.items()):
        accent = GOLD if index == 0 else CYAN
        evidence_strip(canvas, draw, 66 + index * 764, 1388, label, path, digest, accent)

    text(draw, (40, 1586), "A7 identity gate only · parent_producer_identity_review_pending · derivative_authority=none", F12, MUTED)
    text(draw, (2360, 1586), "2400×1600 RGBA", F12, MUTED, "ra")
    return canvas


def main() -> None:
    validate_inputs()
    board = draw_board()
    if board.size != (W, H) or board.mode != "RGBA":
        raise RuntimeError(f"unexpected board properties: {board.size} {board.mode}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    board.save(OUTPUT, format="PNG", optimize=True)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
