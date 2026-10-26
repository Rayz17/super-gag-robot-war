#!/usr/bin/env python3
"""Build the zero-generation BREAKER Camera V2 hand-paint preproduction pack.

This is deliberately a geometric underdrawing, not final identity art.  It consumes
no historical BREAKER pixels and does not read the failed Call03 raw image.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DELIVERY = ROOT / "delivery"
QA = ROOT / "qa"
RECEIPTS = ROOT / "receipts"

BASE = 384
SCALE = 4
CANVAS = BASE * SCALE
PIVOT_BASE = (192, 320)
PIVOT = (PIVOT_BASE[0] * SCALE, PIVOT_BASE[1] * SCALE)
NORTH_BASE = (40, -24)

INK = (16, 31, 48, 255)
INK_SOFT = (39, 65, 83, 220)
UNDERLAY = (102, 127, 140, 116)
UNDERLAY_DARK = (52, 73, 87, 150)
GUIDE = (64, 220, 232, 220)
GUIDE_SOFT = (64, 220, 232, 82)
LOAD = (255, 184, 72, 235)
X_COLOR = (230, 83, 153, 238)
SEAM = (122, 234, 165, 235)
RED = (235, 56, 67, 255)
PAPER = (230, 238, 242, 255)


def s(value: float) -> int:
    return round(value * SCALE)


def pts(values: Sequence[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(s(x), s(y)) for x, y in values]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Supplemental/Helvetica.ttc"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def line(draw: ImageDraw.ImageDraw, values: Sequence[tuple[float, float]], fill, width: float = 2, joint: str = "curve") -> None:
    draw.line(pts(values), fill=fill, width=s(width), joint=joint)


def polygon(draw: ImageDraw.ImageDraw, values: Sequence[tuple[float, float]], fill, outline=INK, width: float = 2) -> None:
    p = pts(values)
    draw.polygon(p, fill=fill)
    draw.line(p + [p[0]], fill=outline, width=s(width), joint="curve")


def ellipse(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float], fill, outline=INK, width: float = 2) -> None:
    draw.ellipse(tuple(s(v) for v in box), fill=fill, outline=outline, width=s(width))


def breaker_parts() -> dict[str, list[tuple[float, float]]]:
    """B body coordinates in the 384 authoring basis.

    The shell spine is exactly parallel to Camera V2 north: (160, -96) = 4*(40,-24).
    Forelimbs are long load columns; rear contacts are deliberately shorter and
    subordinate.  Coordinates stop above the exact [192,320] registration pivot.
    """

    return {
        # Rear contacts are visibly subordinate wedges, not a second pair of legs.
        # REV4 rear stabilizers are thin tail brackets, deliberately unlike legs.
        "rear_stabilizer_far": [(100, 205), (114, 209), (116, 224), (107, 245), (96, 240), (96, 220)],
        "rear_stabilizer_near": [(125, 208), (139, 211), (141, 228), (132, 250), (121, 245), (121, 223)],
        # REV4 front assemblies use an explicit mechanical hinge and splayed impact
        # wedges.  Their lower silhouettes cannot be read as round animal feet.
        "far_forelimb_upper": [(160, 171), (194, 168), (210, 190), (197, 216), (164, 217), (148, 196)],
        "far_forelimb_lower": [(145, 204), (191, 210), (193, 246), (172, 281), (181, 296), (154, 317), (111, 312), (98, 301), (130, 282), (133, 244)],
        # REV4 outer shell: flat offset ridge, straight plate breaks and a rear
        # diagonal cut.  No shoulder-like round arch is present.
        "shell": [(83, 207), (111, 151), (151, 102), (206, 76), (269, 76), (307, 95), (328, 119), (320, 151), (284, 177), (235, 195), (175, 198), (117, 218)],
        "shell_top": [(116, 183), (143, 135), (180, 106), (216, 93), (268, 94), (298, 108), (306, 132), (276, 156), (229, 177), (170, 181)],
        # Chest hangs clear of the ground and exposes a large negative-space pocket.
        "chest_closure": [(197, 177), (247, 171), (270, 190), (256, 224), (226, 240), (194, 217)],
        # Horizontal recessed sensor slot; fully contained by the shell front plate.
        "head": [(243, 139), (286, 139), (301, 149), (291, 162), (251, 162), (238, 151)],
        "near_forelimb_upper": [(248, 168), (282, 164), (303, 184), (300, 215), (268, 222), (242, 201)],
        "near_forelimb_lower": [(257, 205), (298, 202), (313, 240), (308, 279), (335, 298), (326, 312), (282, 318), (249, 301), (264, 279), (248, 244)],
    }


def draw_body(image: Image.Image, responsibility: str = "neutral") -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    p = breaker_parts()

    if responsibility == "B":
        fills = {
            "rear": (225, 188, 66, 205),
            "far_limb": (241, 142, 64, 220),
            "shell": (46, 181, 196, 220),
            "top": (78, 205, 214, 205),
            "chest": (105, 149, 233, 220),
            "head": (76, 110, 202, 230),
            "near_limb": (247, 123, 62, 235),
        }
    elif responsibility == "X":
        fills = {
            "rear": UNDERLAY_DARK,
            "far_limb": UNDERLAY_DARK,
            "shell": (91, 60, 91, 185),
            "top": (115, 63, 107, 205),
            "chest": (65, 85, 92, 200),
            "head": (78, 61, 83, 220),
            "near_limb": UNDERLAY_DARK,
        }
    else:
        fills = {
            "rear": (89, 111, 120, 132),
            "far_limb": (89, 111, 120, 145),
            "shell": UNDERLAY,
            "top": (136, 156, 165, 106),
            "chest": (78, 99, 111, 155),
            "head": (78, 99, 111, 165),
            "near_limb": (86, 108, 118, 165),
        }

    polygon(draw, p["rear_stabilizer_far"], fills["rear"], INK_SOFT, 2)
    polygon(draw, p["rear_stabilizer_near"], fills["rear"], INK, 2)
    polygon(draw, p["far_forelimb_upper"], fills["far_limb"], INK_SOFT, 2)
    polygon(draw, p["far_forelimb_lower"], fills["far_limb"], INK_SOFT, 2)
    polygon(draw, p["shell"], fills["shell"], INK, 3)
    polygon(draw, p["shell_top"], fills["top"], INK_SOFT, 2)
    polygon(draw, p["chest_closure"], fills["chest"], INK, 2)
    polygon(draw, p["head"], fills["head"], INK, 2.5)
    polygon(draw, p["near_forelimb_upper"], fills["near_limb"], INK, 2.5)
    polygon(draw, p["near_forelimb_lower"], fills["near_limb"], INK, 2.5)

    # Articulation, B load paths and the exact Camera V2 north spine.
    line(draw, [(130, 205), (290, 109)], GUIDE if responsibility != "X" else (78, 93, 103, 160), 1.5)
    line(draw, [(178, 174), (180, 214), (160, 286), (125, 307)], LOAD if responsibility == "B" else INK_SOFT, 2)
    line(draw, [(267, 169), (281, 211), (292, 282), (320, 306)], LOAD if responsibility == "B" else INK_SOFT, 2)

    # X ownership: asymmetric plate rhythm, flexible seams, narrow red slit,
    # closed chest seam and a visibly sealed upper-back outlet.
    xline = X_COLOR if responsibility == "X" else (96, 119, 130, 205)
    seam = SEAM if responsibility == "X" else (74, 97, 108, 190)
    line(draw, [(111, 180), (158, 155), (190, 117), (226, 98)], xline, 2)
    line(draw, [(168, 180), (190, 142), (229, 130), (275, 155)], xline, 2)
    line(draw, [(226, 98), (260, 103), (298, 111)], xline, 2)
    line(draw, [(119, 208), (160, 197), (195, 214)], seam, 2)
    line(draw, [(207, 188), (226, 206), (258, 211)], seam, 2)
    line(draw, [(250, 213), (256, 220), (254, 226)], PAPER if responsibility == "X" else INK_SOFT, 1.5)
    line(draw, [(249, 149), (290, 151)], RED, 3)
    ellipse(draw, (244, 89, 267, 103), (62, 76, 84, 230), X_COLOR if responsibility == "X" else INK_SOFT, 2)
    line(draw, [(246, 91), (265, 101)], PAPER if responsibility == "X" else INK_SOFT, 1.5)
    line(draw, [(265, 91), (247, 101)], PAPER if responsibility == "X" else INK_SOFT, 1.5)


def build_pose_scaffold() -> Path:
    image = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw_body(image, "neutral")
    out = QA / "BREAKER_NORTH_CAMERA_V2_REV4_REJECTED_SCAFFOLD_RGBA_1536.png"
    image.save(out, compress_level=9)
    return out


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], delta: tuple[int, int], color, width: int = 10) -> None:
    end = (start[0] + delta[0], start[1] + delta[1])
    draw.line((*start, *end), fill=color, width=width)
    dx, dy = delta
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    tip = end
    left = (round(end[0] - ux * 34 + px * 18), round(end[1] - uy * 34 + py * 18))
    right = (round(end[0] - ux * 34 - px * 18), round(end[1] - uy * 34 - py * 18))
    draw.polygon([tip, left, right], fill=color)


def build_exact_registration(scaffold: Image.Image) -> Path:
    image = Image.new("RGBA", (CANVAS, CANVAS), (8, 15, 24, 255))
    draw = ImageDraw.Draw(image, "RGBA")

    footprint = pts([(72, 248), (192, 176), (312, 248), (192, 320)])
    draw.polygon(footprint, fill=(230, 68, 153, 54), outline=(244, 119, 187, 230), width=8)
    draw.rounded_rectangle((s(28), s(40), s(356), s(320)), radius=s(12), outline=(194, 208, 223, 220), width=6)
    image.alpha_composite(scaffold)

    # Exact pivot and final-384 sampling lines.
    draw.line((PIVOT[0] - 44, PIVOT[1], PIVOT[0] + 44, PIVOT[1]), fill=(255, 255, 255, 255), width=8)
    draw.line((PIVOT[0], PIVOT[1] - 44, PIVOT[0], PIVOT[1] + 44), fill=(255, 255, 255, 255), width=8)
    draw.ellipse((PIVOT[0] - 18, PIVOT[1] - 18, PIVOT[0] + 18, PIVOT[1] + 18), fill=(255, 255, 255, 255))
    draw_arrow(draw, (s(274), s(116)), (s(NORTH_BASE[0]), s(NORTH_BASE[1])), (255, 220, 75, 255), 14)

    small = font(30)
    medium = font(38, True)
    draw.text((52, 42), "CAMERA V2 EXACT / UNDERDRAW ONLY", font=medium, fill=PAPER)
    draw.text((52, 100), "tile half 40x24 | 3x3 | pivot 768,1280 | N +160,-96 at 4x", font=small, fill=(176, 197, 209, 255))
    draw.text((s(272), s(80)), "NORTH", font=small, fill=(255, 220, 75, 255))
    draw.text((PIVOT[0] + 34, PIVOT[1] + 18), "PIVOT", font=small, fill=PAPER)

    out = QA / "BREAKER_NORTH_CAMERA_V2_EXACT_REGISTRATION_1536.png"
    image.save(out, compress_level=9)
    return out


def paste_centered(board: Image.Image, subject: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    scale = min((x1 - x0) / subject.width, (y1 - y0) / subject.height)
    resized = subject.resize((round(subject.width * scale), round(subject.height * scale)), Image.Resampling.LANCZOS)
    board.alpha_composite(resized, (x0 + (x1 - x0 - resized.width) // 2, y0 + (y1 - y0 - resized.height) // 2))


def build_responsibility_board() -> Path:
    width, height = 1920, 1200
    board = Image.new("RGBA", (width, height), (10, 18, 28, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    title = font(42, True)
    h2 = font(30, True)
    body = font(24)
    tiny = font(20)

    draw.text((64, 42), "BREAKER B/X HAND-PAINT RESPONSIBILITY MAP", font=title, fill=PAPER)
    draw.text((64, 98), "RESPONSIBILITY CONTRACT ONLY | REV4 FIGURE REJECTED | no final art", font=body, fill=(238, 100, 127, 255))
    draw.rounded_rectangle((54, 152, 938, 1140), radius=18, fill=(17, 30, 43, 255), outline=(58, 202, 216, 180), width=3)
    draw.rounded_rectangle((982, 152, 1866, 1140), radius=18, fill=(25, 24, 38, 255), outline=(222, 80, 148, 180), width=3)

    b_img = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    x_img = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw_body(b_img, "B")
    draw_body(x_img, "X")
    paste_centered(board, b_img, (70, 190, 920, 790))
    paste_centered(board, x_img, (998, 190, 1848, 790))

    draw.text((88, 174), "B = BODY / SILHOUETTE OWNER", font=h2, fill=(82, 221, 232, 255))
    draw.text((1016, 174), "X = SURFACE / MATERIAL OWNER", font=h2, fill=(236, 95, 167, 255))

    b_lines = [
        "High shell dominates the mass",
        "Low embedded head; never a necked animal",
        "Long load-bearing forelimb columns",
        "Short rear stabilizers only",
        "Exact north spine +40,-24",
        "B owns every outer-contour change",
    ]
    x_lines = [
        "Asymmetric alien armor plates",
        "Flexible seams follow load, not symmetry",
        "One narrow red slit on the head block",
        "Chest seam remains visibly closed",
        "Upper-back outlet remains sealed",
        "X may not change B joints or silhouette",
    ]
    for i, text_value in enumerate(b_lines):
        draw.ellipse((92, 826 + i * 46, 106, 840 + i * 46), fill=(255, 184, 72, 255))
        draw.text((120, 818 + i * 46), text_value, font=tiny, fill=(214, 226, 232, 255))
    for i, text_value in enumerate(x_lines):
        draw.ellipse((1020, 826 + i * 46, 1034, 840 + i * 46), fill=(122, 234, 165, 255))
        draw.text((1048, 818 + i * 46), text_value, font=tiny, fill=(222, 220, 231, 255))

    out = DELIVERY / "BREAKER_BX_RESPONSIBILITY_BOARD_1920x1200.png"
    board.save(out, compress_level=9)
    return out


def build_50_100_board(scaffold: Image.Image) -> Path:
    """Show the actual final-slot 100% and 50% reads without claiming art quality."""
    board = Image.new("RGBA", (1600, 900), (9, 16, 25, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.text((54, 36), "BREAKER CAMERA V2 SILHOUETTE GATE", font=font(42, True), fill=PAPER)
    draw.text((54, 90), "1536 underdraw sampled to final 384 (100%) and 192 (50%)", font=font(24), fill=(164, 185, 198, 255))

    final_100 = scaffold.resize((384, 384), Image.Resampling.LANCZOS)
    final_50 = scaffold.resize((192, 192), Image.Resampling.LANCZOS)
    boxes = [(80, 180, 720, 820), (880, 180, 1520, 820)]
    for x0, y0, x1, y1 in boxes:
        draw.rounded_rectangle((x0, y0, x1, y1), radius=20, fill=(16, 29, 42, 255), outline=(60, 84, 102, 255), width=3)
    board.alpha_composite(final_100, (208, 294))
    board.alpha_composite(final_50, (1104, 390))
    draw.text((108, 204), "100% / 384 px", font=font(30, True), fill=(78, 218, 230, 255))
    draw.text((908, 204), "50% / 192 px", font=font(30, True), fill=(255, 184, 72, 255))
    draw.text((108, 756), "Judge silhouette, north axis and load hierarchy only.", font=font(21), fill=(197, 212, 220, 255))
    draw.text((908, 756), "If this reads turtle / ape / vehicle: reject before paint.", font=font(21), fill=(236, 137, 153, 255))

    out = QA / "BREAKER_NORTH_CAMERA_V2_50_100_SILHOUETTE_BOARD_1600x900.png"
    board.save(out, compress_level=9)
    return out


def build_black_silhouette(scaffold: Image.Image) -> tuple[Path, Image.Image]:
    # Collapse every occupied underdraw pixel into one opaque union.  Internal
    # line/fill alpha must not help the first-read gate.
    alpha_1536 = scaffold.getchannel("A").point(lambda value: 255 if value else 0)
    black_1536 = Image.new("RGBA", scaffold.size, (4, 7, 10, 255))
    black_1536.putalpha(alpha_1536)
    black_192 = black_1536.resize((192, 192), Image.Resampling.LANCZOS)
    out = QA / "BREAKER_NORTH_CAMERA_V2_REV4_BLACK_SILHOUETTE_192.png"
    black_192.save(out, compress_level=9)
    return out, black_192


def build_black_silhouette_gate(black_192: Image.Image) -> Path:
    board = Image.new("RGBA", (1200, 720), (232, 236, 238, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.text((48, 34), "REV4 192 PX BLACK-SILHOUETTE GATE / FAIL", font=font(38, True), fill=(185, 35, 61, 255))
    draw.text((48, 84), "Still reads as a hunched ape / bear. Script scaffold route stops here.", font=font(22), fill=(117, 48, 61, 255))
    scaled = black_192.resize((384, 384), Image.Resampling.NEAREST)
    board.alpha_composite(scaled, (90, 190))
    draw.line((600, 164, 600, 648), fill=(156, 166, 172, 255), width=3)
    checks = [
        "asymmetric high-back wedge, not a round dome",
        "raised belly produces visible negative space",
        "two front ram-columns dominate the lower silhouette",
        "rear stabilizers remain roughly half forelimb length",
        "head does not project as a snout or neck",
        "reject if turtle / ape / quadruped / vehicle wins",
    ]
    draw.text((648, 184), "FIRST-READ CHECK", font=font(28, True), fill=(21, 54, 70, 255))
    for i, value in enumerate(checks):
        color = (112, 123, 130, 255) if i < 5 else (202, 54, 76, 255)
        draw.ellipse((652, 250 + i * 58, 668, 266 + i * 58), fill=color)
        draw.text((686, 241 + i * 58), value, font=font(21), fill=(34, 45, 53, 255))
    out = QA / "BREAKER_NORTH_CAMERA_V2_REV4_BLACK_SILHOUETTE_GATE_1200x720.png"
    board.save(out, compress_level=9)
    return out


def build_rev4_comparison(rev4: Image.Image) -> Path:
    rev1_path = QA / "BREAKER_NORTH_CAMERA_V2_REV1_REJECTED_384.png"
    rev2_path = QA / "BREAKER_NORTH_CAMERA_V2_REV2_REJECTED_384.png"
    rev3_path = QA / "BREAKER_NORTH_CAMERA_V2_REV3_REJECTED_384.png"
    if not rev1_path.exists() or not rev2_path.exists() or not rev3_path.exists():
        raise FileNotFoundError("REV1/REV2/REV3 rejection baselines are required for the REV4 comparison")
    rev1 = Image.open(rev1_path).convert("RGBA")
    rev2 = Image.open(rev2_path).convert("RGBA")
    rev3 = Image.open(rev3_path).convert("RGBA")
    board = Image.new("RGBA", (2400, 900), (9, 16, 25, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.text((54, 36), "BREAKER PREPRODUCTION REV1 -> REV2 -> REV3 -> REV4", font=font(42, True), fill=PAPER)
    draw.text((54, 90), "Same Camera V2 / 3x3 / pivot. REV1-3 remain History; no final paint.", font=font(24), fill=(164, 185, 198, 255))
    panels = [(30, 174, 570, 824), (630, 174, 1170, 824), (1230, 174, 1770, 824), (1830, 174, 2370, 824)]
    for x0, y0, x1, y1 in panels:
        draw.rounded_rectangle((x0, y0, x1, y1), radius=20, fill=(16, 29, 42, 255), outline=(60, 84, 102, 255), width=3)
    board.alpha_composite(rev1, (108, 276))
    board.alpha_composite(rev2, (708, 276))
    board.alpha_composite(rev3, (1308, 276))
    board.alpha_composite(rev4, (1908, 276))
    draw.text((58, 198), "REV1 / REJECTED", font=font(26, True), fill=(236, 97, 125, 255))
    draw.text((658, 198), "REV2 / REJECTED", font=font(26, True), fill=(236, 97, 125, 255))
    draw.text((1258, 198), "REV3 / REJECTED", font=font(26, True), fill=(236, 97, 125, 255))
    draw.text((1858, 198), "REV4 / REJECTED STOP", font=font(26, True), fill=(236, 97, 125, 255))
    draw.text((58, 748), "Round shell + four-support animal read.", font=font(18), fill=(235, 169, 181, 255))
    draw.text((658, 748), "Ram-columns improved; shell still dome-like.", font=font(18), fill=(235, 169, 181, 255))
    draw.text((1258, 748), "Black union read as hunched ape / bear.", font=font(18), fill=(235, 169, 181, 255))
    draw.text((1858, 748), "Still hunched ape / bear; human concept redraw required.", font=font(18), fill=(235, 169, 181, 255))
    out = QA / "BREAKER_NORTH_CAMERA_V2_REV1_REV2_REV3_REV4_COMPARISON_2400x900.png"
    board.save(out, compress_level=9)
    return out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_delivery_hashes() -> Path:
    manifest = ROOT / "delivery-hashes.sha256"
    paths = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path != manifest
    )
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in paths]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    for directory in (DELIVERY, QA, RECEIPTS):
        directory.mkdir(parents=True, exist_ok=True)

    scaffold_path = build_pose_scaffold()
    scaffold = Image.open(scaffold_path).convert("RGBA")
    registration_path = build_exact_registration(scaffold)
    responsibility_path = build_responsibility_board()
    readability_path = build_50_100_board(scaffold)
    black_silhouette_path, black_192 = build_black_silhouette(scaffold)
    black_gate_path = build_black_silhouette_gate(black_192)

    preview = scaffold.resize((BASE, BASE), Image.Resampling.LANCZOS)
    preview_path = QA / "BREAKER_NORTH_CAMERA_V2_SCAFFOLD_384_PREVIEW.png"
    preview.save(preview_path, compress_level=9)
    rev4_comparison_path = build_rev4_comparison(preview)

    alpha = scaffold.getchannel("A")
    bbox = alpha.getbbox()
    payload = {
        "status": "STOP_SCRIPT_SCAFFOLD_REQUIRES_HUMAN_CONCEPT_REDRAW",
        "final_art": False,
        "scaffold_ready": False,
        "revision": "REV4_REJECTED_FINAL_SCRIPT_TRY",
        "visual_verdict": "HUNCHED_APE_OR_BEAR_FIRST_READ_REMAINS",
        "human_concept_redraw_required": True,
        "imagegen_used": False,
        "historical_breaker_pixels_consumed": False,
        "call03_raw_read_or_consumed": False,
        "canvas_px": [CANVAS, CANVAS],
        "final_basis_px": [BASE, BASE],
        "work_scale": 4,
        "pivot_work_px": list(PIVOT),
        "pivot_final_px": list(PIVOT_BASE),
        "footprint": [3, 3],
        "tile_half_final_px": [40, 24],
        "tile_half_work_px": [160, 96],
        "north_vector_final_px": list(NORTH_BASE),
        "north_vector_work_px": [NORTH_BASE[0] * SCALE, NORTH_BASE[1] * SCALE],
        "shell_spine_work_delta_px": [640, -384],
        "shell_spine_parallel_to_north": True,
        "alpha_bbox_work_px": list(bbox) if bbox else None,
        "alpha_stays_above_pivot": bool(bbox and bbox[3] <= PIVOT[1]),
        "outputs": {
            str(p.relative_to(ROOT)): sha256(p)
            for p in (
                scaffold_path,
                registration_path,
                responsibility_path,
                readability_path,
                black_silhouette_path,
                black_gate_path,
                preview_path,
                rev4_comparison_path,
            )
        },
    }
    receipt = RECEIPTS / "geometry-readback.json"
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_delivery_hashes()
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
