#!/usr/bin/env python3
"""Generate the C01E02 G1 art previs from the seven frozen visual inputs only."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


OUT = Path(__file__).resolve().parent
CONTRACT_DIR = OUT.parent
ROOT = OUT.parents[5]
CONTRACT_PATH = CONTRACT_DIR / "13-demo-build-contract.json"
VISUAL_MANIFEST_PATH = CONTRACT_DIR / "09b-frozen-visual-snapshot.tsv"
EXPECTED_FINGERPRINT = "944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94"

W, H = 1280, 720
WORLD_W, WORLD_H = 1920, 900
FPS = 24
S01_JOINT_STATE = "C01CDV1_JOINT_S01_CAMB_V1"
S06_JOINT_STATE = "C01CDV1_JOINT_S06_T2_STAGE1_V1"
S06_BUTTON_RECTS = (
    (905, 390, 145, 38),
    (1070, 390, 145, 38),
    (905, 442, 145, 38),
    (1070, 442, 145, 38),
    (905, 494, 145, 38),
    (1070, 494, 145, 38),
)

PRESERVED_G11_HASHES = {
    "PV01_S01_EVAC_WORLD_clean_plate_1920x900.png": "b0075a5596ed836e97e82fcc7d9f0212ffabf676e0cf94fa9a1dc69ec6b6d223",
    "PV01_S01_EVAC_WORLD_camera_A_1280x720.png": "e118b46ac8ec8297955ae98cc6a1c4cef05961eee11d7b462afde7ed5b3560aa",
    "PV01_S01_EVAC_WORLD_camera_B_1280x720.png": "64739cbf8ba80153de519f7137ab8afc7e06665a97905a548a6f6eaa08d78cd3",
    "PV01_S01_EVAC_WORLD_camera_C_1280x720.png": "c2177f6f0de75f5e56410046d477aa21106cfbbde9a5453ae59cc48fd2133554",
    "PV02_S03_SAME_BODY_1280x720.png": "c3a3ed7ebc98afe159a0b00e2d857d870ad9a74b3b178ef9630d22664caed8c6",
    "PV03_S04_QIHAI_SCREEN_1280x720.png": "3be51dc02033f23bfdae061c795819f1743860224528781132cbaafedf27c2bb",
    "PV04_S05_GUARDIAN_STAND_1280x720.png": "70f173b62f06028228981023d530751451ff756e93c93e2232205fdb1500a0df",
    "PV06_S07_SHIELD_IMPACT_1280x720.png": "95b55efccd7d0ca9c14f2570036f71ac7df6f24468d46cdb0cf9db1a2d13ffce",
    "SPACE_CONTACT_SHEET_1280x720.png": "c26095b5dc386c8baa346e000cf188d7738b68ce304b73726e418861de23aac5",
    "GZ_IDENTITY_COMPARISON_1280x720.png": "5bbf3d5866a0c18395241da439f451b36e4b0706c140994aa35444a052469f8c",
    "C01E02_G1_ANIMATIC_placeholder_audio.wav": "a4344fc35712e5f3e2a01e01918a1bdcd81cba2f5091f3768d78f367db598b58",
    "C01E02_G1_ANIMATIC_1280x720_36s.mp4": "a3d08005bb5fdeeb0b5bd270e2dac87ee76b2c4e692149df9cb5fb103d493da9",
    "animatic-shot-list.tsv": "4809579059e15f5688346927a6e638d82102df1d1bf2a98c1e20f21d61cc6e5c",
    "PV01_S01_EVAC_WORLD_coordinate-lock.tsv": "84a35381cc2a24499b3f023b110d0ee1a7de436c0a7683b91524901136ae2305",
    "PV05_S06_TACTICAL_READ_1280x720.png": "492744c1654760732856711d8c922962342777088e5d6a540b0d791ee5bcb5e9",
    "PV05_S06_TACTICAL_READ_overlay_source_t2s1_1280x720.png": "0cf806996e9d0894aa7fb17fa83c43be70f9aac6ea044f777940c00b4b94f59e",
    "g1-user-question-self-check.tsv": "dc28adefe177ee69b899a3a98c6cd9f4bb9aa6dca84203c87126dae2b663ecdb",
    "source-validation-receipt.tsv": "7acd72ef39bed1c82acedf08620e38fe4063ccde095faf6c996cfcf995b7794b",
}

INK = "#18232f"
INK_2 = "#344454"
PAPER = "#eef1f2"
PAPER_2 = "#dce2e5"
WHITE = "#fbfbf8"
NAVY = "#19324a"
NAVY_2 = "#315673"
RED = "#cf3f37"
RED_2 = "#8f2d2b"
GOLD = "#d7a33c"
TEAL = "#4f9295"
GREEN = "#547d67"
AMBER = "#e0a542"
SMOKE = "#66727a"
MUTED = "#75828c"
BLACK = "#0c1117"

FONT_REGULAR_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_REGULAR_PATH, size)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_visual_manifest() -> dict[str, dict[str, str]]:
    with VISUAL_MANIFEST_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 7:
        raise RuntimeError(f"Expected 7 frozen visual inputs, got {len(rows)}")
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise RuntimeError(f"Frozen visual missing: {row['path']}")
        actual = sha256(path)
        if actual != row["sha256"]:
            raise RuntimeError(f"Frozen visual hash mismatch: {row['visual_id']}")
        if row["runtime_allowed"].lower() != "false":
            raise RuntimeError(f"Frozen visual unexpectedly runtime-enabled: {row['visual_id']}")
        row["resolved_path"] = str(path)
        result[row["visual_id"]] = row
    return result


def validate_contract() -> tuple[dict, dict[str, dict[str, str]]]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if contract["content_fingerprint"] != EXPECTED_FINGERPRINT:
        raise RuntimeError("Content fingerprint mismatch")
    if contract["visual_manifest"]["entry_count"] != 7:
        raise RuntimeError("Visual manifest count mismatch")
    if contract["d0"] != {
        "outcome": "gameplay_finisher",
        "required_input": "confirm_shield_bash",
        "trigger_state": "finisher_triggered=true",
        "knockdown_state": "confirmed_gameplay_finisher",
        "breaker_destroyed": False,
    }:
        raise RuntimeError("D0-B contract mismatch")
    return contract, read_visual_manifest()


CONTRACT, VISUALS = validate_contract()
IMAGE_CACHE: dict[str, Image.Image] = {}


def load_visual(visual_id: str) -> Image.Image:
    if visual_id not in IMAGE_CACHE:
        IMAGE_CACHE[visual_id] = Image.open(VISUALS[visual_id]["resolved_path"]).convert("RGBA")
    return IMAGE_CACHE[visual_id].copy()


def connected_white_to_alpha(image: Image.Image, threshold: int = 28) -> Image.Image:
    """Remove only edge-connected pale background, preserving enclosed white armor/clothes."""
    rgba = image.convert("RGBA")
    for point in ((0, 0), (rgba.width - 1, 0), (0, rgba.height - 1), (rgba.width - 1, rgba.height - 1)):
        ImageDraw.floodfill(rgba, point, (255, 255, 255, 0), thresh=threshold)
    alpha = rgba.getchannel("A")
    bbox = alpha.getbbox()
    return rgba.crop(bbox) if bbox else rgba


def fit_image(
    canvas: Image.Image,
    image: Image.Image,
    box: tuple[int, int, int, int],
    *,
    opacity: int = 255,
    align: str = "center",
) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    max_w, max_h = max(1, x1 - x0), max(1, y1 - y0)
    scale = min(max_w / image.width, max_h / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    placed = image.resize(size, Image.Resampling.LANCZOS)
    if opacity != 255:
        placed.putalpha(ImageChops.multiply(placed.getchannel("A"), Image.new("L", placed.size, opacity)))
    if align == "bottom":
        px, py = x0 + (max_w - size[0]) // 2, y1 - size[1]
    elif align == "left":
        px, py = x0, y0 + (max_h - size[1]) // 2
    elif align == "right":
        px, py = x1 - size[0], y0 + (max_h - size[1]) // 2
    else:
        px, py = x0 + (max_w - size[0]) // 2, y0 + (max_h - size[1]) // 2
    canvas.alpha_composite(placed, (px, py))
    return px, py, px + size[0], py + size[1]


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, fill=INK, *, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def wrapped_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    value: str,
    size: int,
    fill=INK,
    *,
    bold=False,
    spacing=5,
) -> int:
    x0, y0, x1, _ = box
    fnt = font(size, bold)
    lines: list[str] = []
    for paragraph in value.split("\n"):
        current = ""
        for char in paragraph:
            trial = current + char
            if current and draw.textbbox((0, 0), trial, font=fnt)[2] > x1 - x0:
                lines.append(current)
                current = char
            else:
                current = trial
        lines.append(current)
    y = y0
    line_h = size + spacing
    for line in lines:
        draw.text((x0, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def rounded_panel(draw: ImageDraw.ImageDraw, box, fill, outline=INK_2, width=2, radius=6):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill=RED, width=5, head=13):
    draw.line((start, end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    p1 = (end[0] - head * math.cos(angle - 0.55), end[1] - head * math.sin(angle - 0.55))
    p2 = (end[0] - head * math.cos(angle + 0.55), end[1] - head * math.sin(angle + 0.55))
    draw.polygon((end, p1, p2), fill=fill)


def focus_marker(draw: ImageDraw.ImageDraw, xy, label: str, color=GOLD):
    x, y = xy
    draw.ellipse((x - 12, y - 12, x + 12, y + 12), outline=color, width=3)
    draw.line((x - 18, y, x + 18, y), fill=color, width=2)
    draw.line((x, y - 18, x, y + 18), fill=color, width=2)
    rounded_panel(draw, (x + 18, y - 15, x + 18 + max(92, len(label) * 14), y + 17), "#fff9e8", color, 2, 4)
    text(draw, (x + 26, y - 10), label, 15, INK, bold=True)


def header(canvas: Image.Image, stable_id: str, title: str, subtitle: str = ""):
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, canvas.width, 62), fill=INK)
    draw.rectangle((0, 62, canvas.width, 66), fill=RED)
    id_font = font(14, True)
    draw.text((24, 18), stable_id, font=id_font, fill=WHITE)
    id_width = draw.textbbox((24, 18), stable_id, font=id_font)[2] - 24
    title_x = max(260, min(390, 24 + id_width + 30))
    text(draw, (title_x, 14), title, 23, WHITE, bold=True)
    if subtitle:
        text(draw, (canvas.width - 24, 18), subtitle, 14, "#cfd8de", anchor="ra")


def footer(canvas: Image.Image, note: str, *, runtime=False):
    if runtime:
        raise RuntimeError("G1 art cannot be runtime-enabled")
    draw = ImageDraw.Draw(canvas, "RGBA")
    y0 = canvas.height - 54
    draw.rectangle((0, y0, canvas.width, canvas.height), fill=(24, 35, 47, 238))
    text(draw, (20, y0 + 9), note, 15, WHITE)
    text(draw, (canvas.width - 20, y0 + 9), "candidate_previs | runtime_allowed=false", 14, "#f0c86e", anchor="ra")
    text(draw, (canvas.width - 20, y0 + 30), f"fp {EXPECTED_FINGERPRINT[:12]}", 12, "#b8c4cc", anchor="ra")


def safe_area(draw: ImageDraw.ImageDraw, w=W, h=H, label="1280x720 SAFE AREA"):
    draw.rectangle((32, 56, w - 32, h - 72), outline=(24, 35, 47, 120), width=2)
    text(draw, (40, 68), label, 12, MUTED)


def proxy_person(
    draw: ImageDraw.ImageDraw,
    foot: tuple[int, int],
    height: int,
    color: str,
    label: str,
    *,
    child=False,
    show_label=True,
):
    x, y = foot
    head_r = max(7, int(height * (0.09 if not child else 0.12)))
    body_top = y - height + head_r * 2
    draw.ellipse((x - head_r, y - height, x + head_r, y - height + head_r * 2), fill=color, outline=INK, width=2)
    shoulder = int(height * 0.16)
    hip = int(height * 0.09)
    draw.polygon(((x - shoulder, body_top + 8), (x + shoulder, body_top + 8), (x + hip, y - int(height * 0.38)), (x - hip, y - int(height * 0.38))), fill=color, outline=INK)
    draw.line((x - hip, y - int(height * 0.38), x - int(height * 0.08), y), fill=INK, width=max(3, height // 30))
    draw.line((x + hip, y - int(height * 0.38), x + int(height * 0.08), y), fill=INK, width=max(3, height // 30))
    if show_label:
        rounded_panel(draw, (x - 52, y + 7, x + 52, y + 31), WHITE, color, 2, 4)
        text(draw, (x, y + 12), label, 13, INK, bold=True, anchor="ma")


def proxy_terminal(draw: ImageDraw.ImageDraw, center: tuple[int, int], *, damaged=False, label=True):
    x, y = center
    body = ((x - 38, y - 35), (x + 38, y + 18))
    rounded_panel(draw, (*body[0], *body[1]), "#50606a" if not damaged else "#3a4146", INK, 3, 6)
    draw.rectangle((x - 25, y - 23, x + 25, y + 4), fill="#d9e7e9", outline=TEAL, width=2)
    draw.ellipse((x - 34, y + 5, x - 10, y + 29), fill=INK_2, outline=INK, width=2)
    draw.ellipse((x + 10, y + 5, x + 34, y + 29), fill=INK_2, outline=INK, width=2)
    if damaged:
        draw.line((x - 28, y - 18, x + 24, y + 6), fill=RED, width=4)
        draw.line((x + 5, y - 26, x - 16, y + 8), fill=RED, width=3)
    if label:
        text(draw, (x, y + 38), "旧守护者终端 / PREVIS PROXY", 12, INK, bold=True, anchor="ma")


def proxy_dog(draw: ImageDraw.ImageDraw, center: tuple[int, int], *, show_label=True):
    x, y = center
    draw.rounded_rectangle((x - 34, y - 22, x + 28, y + 14), radius=8, fill="#cfd8d9", outline=INK, width=3)
    draw.ellipse((x + 18, y - 34, x + 48, y - 5), fill="#cfd8d9", outline=INK, width=3)
    for dx in (-22, 17):
        draw.line((x + dx, y + 12, x + dx - 5, y + 32), fill=INK, width=5)
    draw.ellipse((x + 40, y - 25, x + 47, y - 18), fill=TEAL)
    draw.line((x - 34, y - 8, x - 54, y - 22), fill=TEAL, width=5)
    if show_label:
        text(draw, (x, y + 42), "机器犬 / PREVIS PROXY", 12, INK, bold=True, anchor="ma")


def proxy_bridge(draw: ImageDraw.ImageDraw, center: tuple[int, int], *, show_label=True):
    x, y = center
    draw.rounded_rectangle((x - 92, y - 40, x + 92, y + 16), radius=8, fill="#e7a647", outline=INK, width=4)
    draw.rectangle((x - 76, y - 58, x + 76, y - 39), fill="#f4c56c", outline=INK, width=3)
    for dx in (-62, -20, 20, 62):
        draw.line((x + dx, y + 15, x + dx - 12, y + 58), fill=INK_2, width=7)
    if show_label:
        text(draw, (x, y + 68), "消防架桥机 / PREVIS PROXY", 12, INK, bold=True, anchor="ma")


def proxy_breaker(draw: ImageDraw.ImageDraw, box, *, knocked=False, label=True):
    x0, y0, x1, y1 = box
    if knocked:
        draw.rounded_rectangle((x0, y0 + (y1 - y0) * 0.42, x1, y1), radius=18, fill=BLACK, outline=RED_2, width=4)
        draw.polygon(((x0 + 20, y0 + 70), (x1 - 20, y0 + 45), (x1 - 55, y1 - 15), (x0 + 35, y1 - 5)), fill="#1d252e", outline=INK, width=3)
        draw.line((x0 + 45, y0 + 88, x1 - 45, y0 + 66), fill=RED, width=6)
    else:
        mid = (x0 + x1) / 2
        draw.polygon(((mid, y0), (x1, y0 + 55), (x1 - 22, y1), (x0 + 22, y1), (x0, y0 + 55)), fill=BLACK, outline=INK_2, width=4)
        draw.polygon(((mid, y0 + 20), (x1 - 25, y0 + 65), (x1 - 40, y1 - 35), (x0 + 40, y1 - 35), (x0 + 25, y0 + 65)), fill="#222d36", outline="#4a5660", width=3)
        draw.line((x0 + 48, y0 + 72, x1 - 48, y0 + 72), fill=RED, width=7)
    if label:
        text(draw, ((x0 + x1) // 2, y1 + 8), "BREAKER / DESIGN PREVIS", 12, INK, bold=True, anchor="ma")


def proxy_shield(draw: ImageDraw.ImageDraw, center: tuple[int, int], height: int, *, scorch=3, hot=False, damaged=False):
    x, y = center
    half_w = int(height * 0.29)
    top = y - height // 2
    bottom = y + height // 2
    fill = "#9f493f" if hot else "#53616a"
    points = ((x - half_w, top + 20), (x, top), (x + half_w, top + 20), (x + half_w - 8, bottom - 24), (x, bottom), (x - half_w + 8, bottom - 24))
    draw.polygon(points, fill=fill, outline=INK, width=4)
    draw.line((x, top + 12, x, bottom - 12), fill=GOLD, width=4)
    for i in range(scorch):
        yy = top + 50 + i * max(18, height // 8)
        draw.line((x - half_w + 15, yy, x + half_w - 20, yy + 8), fill="#282e32", width=4)
    if damaged:
        draw.line((x - 20, top + 35, x + 18, bottom - 28), fill=RED_2, width=5)


def guardian_cutout() -> Image.Image:
    return connected_white_to_alpha(load_visual("VIS_GUARDIAN_Z_V10X"), threshold=30)


def jicun_q_cutout() -> Image.Image:
    return connected_white_to_alpha(load_visual("VIS_JICUN_Q_RUNTIME_V1"), threshold=26)


def jicun_standard_cutout() -> Image.Image:
    return connected_white_to_alpha(load_visual("VIS_JICUN_STANDARD_V1"), threshold=26)


def qihai_cutout() -> Image.Image:
    sheet = load_visual("VIS_CML002_003_004_CURRENT_BASE")
    crop = sheet.crop((1125, 10, sheet.width - 8, sheet.height - 8))
    return connected_white_to_alpha(crop, threshold=25)


def draw_museum_clean_plate() -> Image.Image:
    image = Image.new("RGBA", (WORLD_W, WORLD_H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((0, 0, WORLD_W, 505), fill="#e8ecee")
    draw.rectangle((0, 505, WORLD_W, WORLD_H), fill="#cfd7db")
    for y in (560, 650, 760, 860):
        draw.line((0, y, WORLD_W, y), fill=(104, 120, 130, 80), width=2)
    for x in range(-200, 2200, 240):
        draw.line((960, 505, x, WORLD_H), fill=(105, 120, 130, 65), width=2)
    for x in (120, 520, 920, 1320, 1720):
        draw.rectangle((x, 92, x + 36, 650), fill="#aab6bd", outline=INK_2, width=2)
        draw.rectangle((x + 36, 92, x + 62, 650), fill="#f7f7f4", outline="#8d9ba3", width=2)
    draw.rectangle((0, 80, WORLD_W, 112), fill=NAVY)
    text(draw, (40, 86), "MILLION MECH MUSEUM  /  EAST EVACUATION ROUTE", 17, WHITE, bold=True)
    draw.polygon(((80, 700), (1680, 570), (1880, 760), (260, 875)), fill=(245, 247, 246, 205), outline=TEAL)
    draw.line((260, 840, 1780, 650), fill=TEAL, width=7)
    draw.line((260, 790, 1780, 605), fill=(79, 146, 149, 90), width=3)
    draw.rectangle((1700, 290, 1885, 650), fill="#dce9e7", outline=TEAL, width=5)
    draw.polygon(((1725, 485), (1840, 485), (1885, 650), (1680, 650)), fill="#c3d4d4", outline=TEAL)
    text(draw, (1792, 315), "东侧出口", 24, NAVY, bold=True, anchor="ma")
    draw.rectangle((170, 480, 350, 675), fill="#313c45", outline=RED, width=5)
    draw.rectangle((195, 510, 325, 635), fill="#11181e", outline=RED_2, width=3)
    text(draw, (260, 445), "地下封闭区", 22, RED_2, bold=True, anchor="ma")
    draw.rectangle((1240, 420, 1510, 660), fill="#d9e0e2", outline=NAVY_2, width=4)
    text(draw, (1375, 445), "模型病院", 22, NAVY, bold=True, anchor="ma")
    draw.polygon(((625, 245), (1040, 180), (1260, 505), (500, 505)), fill=(29, 50, 72, 30), outline=(25, 50, 74, 110))
    draw.ellipse((755, 230, 1060, 520), fill=(25, 50, 74, 45), outline=(25, 50, 74, 100), width=4)
    text(draw, (910, 350), "馆守Z远景尺度 / PREVIS VOLUME", 18, NAVY, bold=True, anchor="ma")
    return image


def add_world_actors(image: Image.Image) -> Image.Image:
    scene = image.copy()
    draw = ImageDraw.Draw(scene, "RGBA")
    for i in range(5):
        draw.ellipse((20 + i * 55, 230 - i * 18, 240 + i * 70, 720), fill=(76, 86, 92, 26))
    draw.rectangle((390, 275, 425, 700), fill=(207, 63, 55, 90), outline=RED, width=3)
    draw.rectangle((430, 275, 465, 700), fill=(207, 63, 55, 55), outline=RED_2, width=2)
    text(draw, (428, 248), "动态火帘层", 16, RED_2, bold=True, anchor="ma")
    proxy_person(draw, (560, 742), 182, "#b43d35", "唐胶 / PROXY")
    proxy_person(draw, (1240, 650), 175, TEAL, "兜灯 / PROXY")
    proxy_person(draw, (1492, 676), 142, "#e0a65a", "小满 / PROXY", child=True)
    proxy_person(draw, (980, 676), 155, "#8b7a6e", "老余 / PROXY")
    draw.ellipse((930, 617, 1028, 690), outline=INK, width=5)
    draw.line((960, 620, 980, 675), fill=INK, width=5)
    proxy_dog(draw, (850, 655))
    proxy_bridge(draw, (1170, 515))
    proxy_terminal(draw, (720, 680), label=True)
    draw.rounded_rectangle((435, 620, 510, 680), radius=28, fill="#d8dde0", outline=INK, width=3)
    draw.line((475, 620, 475, 565), fill=INK, width=7)
    text(draw, (474, 697), "跌跌 / PROXY", 12, INK, bold=True, anchor="ma")
    q = jicun_q_cutout()
    fit_image(scene, q, (765, 505, 925, 716), align="bottom")
    text(draw, (845, 726), "纪存 / CAND Q", 13, NAVY, bold=True, anchor="ma")
    arrow(draw, (690, 790), (1760, 690), TEAL, 8, 20)
    text(draw, (1180, 775), "浅 X/Y 主行走带", 20, NAVY, bold=True, anchor="ma")
    arrow(draw, (620, 760), (620, 690), NAVY_2, 5, 14)
    text(draw, (600, 782), "Y 深度", 14, NAVY_2, bold=True, anchor="ra")
    return scene


def generate_pv01() -> list[Path]:
    paths: list[Path] = []
    plate = draw_museum_clean_plate()
    plate_path = OUT / "PV01_S01_EVAC_WORLD_clean_plate_1920x900.png"
    plate.convert("RGB").save(plate_path, quality=95)
    paths.append(plate_path)
    world = add_world_actors(plate)
    crop_specs = {
        "A": (0, 90, 1280, 810, "地下危险入口 + 跌跌", (270, 520)),
        "B": (320, 90, 1600, 810, "纪存 + 机器犬 + 老余", (650, 540)),
        "C": (640, 90, 1920, 810, "架桥机 + 小满 + 东侧出口", (1040, 515)),
    }
    for name, (x0, y0, x1, y1, label, focus) in crop_specs.items():
        crop = world.crop((x0, y0, x1, y1))
        draw = ImageDraw.Draw(crop, "RGBA")
        safe_area(draw)
        focus_marker(draw, focus, label)
        arrow(draw, (120, 600), (1060, 550), TEAL, 4, 12)
        header(crop, f"PV01-CAM-{name}", f"S01 东侧撤离 / 相机{name}", "D1 探索呈现证据")
        footer(crop, "World Space | 三区相机 | 浅X/Y | 动态对象独立于clean plate")
        path = OUT / f"PV01_S01_EVAC_WORLD_camera_{name}_1280x720.png"
        crop.convert("RGB").save(path, quality=95)
        paths.append(path)
    return paths


def write_pv01_coordinate_lock() -> Path:
    path = OUT / "PV01_S01_EVAC_WORLD_coordinate-lock.tsv"
    rows = [
        ("meta", "episode_checkpoint", "S01 / CP0", "", "spatial_completed=[] / no_failure"),
        ("meta", "world_viewport", "1920x900", "1280x720", "screen = world - camera_center + (640,360)"),
        ("camera", "camera_B", "center=(960,450)", "crop=Rect(320,90,1280,720)", "direct lock; no lerp intermediate"),
        ("actor", "jicun_foot", "(845,716)", "(525,626)", "CAND_JICUN_Q_RUNTIME_V1"),
        ("anchor", "diedie_fire_door", "(475,680)", "(155,590)", "shared interaction point"),
        ("anchor", "machine_dog", "(850,655)", "(530,565)", "shared named geometry"),
        ("anchor", "laoyu_wheelchair", "(980,676)", "(660,586)", "shared named geometry"),
        ("anchor", "fire_bridge_foot", "(1170,573)", "(850,483)", "shared named geometry"),
        ("anchor", "xiaoman", "(1492,676)", "(1172,586)", "shared named geometry"),
        ("anchor", "east_exit", "(1792,650)", "(1472,560)", "outside camera B"),
        ("anchor", "underground_danger", "(260,675)", "(-60,585)", "outside camera B"),
        ("anchor", "foreground_occluder_center", "(1080,640)", "(760,550)", "overlay source foreground layer"),
        ("geometry", "main_walk_plane", "(80,700) (1680,570) (1880,760) (260,875)", "", "unchanged PV01 clean plate"),
        ("geometry", "underground_rect", "Rect(170,480,180,195)", "", "unchanged PV01 clean plate"),
        ("geometry", "east_exit_rect", "Rect(1700,290,185,360)", "", "unchanged PV01 clean plate"),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("stable_state", "scope", "item", "world_lock", "screen_lock", "notes", "runtime_allowed"))
        for scope, item, world_lock, screen_lock, notes in rows:
            writer.writerow((S01_JOINT_STATE, scope, item, world_lock, screen_lock, notes, "false"))
    return path


def generate_pv01_overlay_source_cam_b() -> Path:
    world = draw_museum_clean_plate()
    draw = ImageDraw.Draw(world, "RGBA")
    for i in range(5):
        draw.ellipse((20 + i * 55, 230 - i * 18, 240 + i * 70, 720), fill=(76, 86, 92, 26))
    draw.rectangle((390, 275, 425, 700), fill=(207, 63, 55, 90), outline=RED, width=3)
    draw.rectangle((430, 275, 465, 700), fill=(207, 63, 55, 55), outline=RED_2, width=2)
    proxy_person(draw, (560, 742), 182, "#b43d35", "Tangjiao", show_label=False)
    proxy_person(draw, (1240, 650), 175, TEAL, "Doudeng", show_label=False)
    proxy_person(draw, (1492, 676), 142, "#e0a65a", "Xiaoman", child=True, show_label=False)
    proxy_person(draw, (980, 676), 155, "#8b7a6e", "Laoyu", show_label=False)
    draw.ellipse((930, 617, 1028, 690), outline=INK, width=5)
    draw.line((960, 620, 980, 675), fill=INK, width=5)
    proxy_dog(draw, (850, 655), show_label=False)
    proxy_bridge(draw, (1170, 515), show_label=False)
    proxy_terminal(draw, (720, 680), label=False)
    draw.rounded_rectangle((435, 620, 510, 680), radius=28, fill="#d8dde0", outline=INK, width=3)
    draw.line((475, 620, 475, 565), fill=INK, width=7)
    fit_image(world, jicun_q_cutout(), (765, 505, 925, 716), align="bottom")
    # Program lock: anchor world=(1080,640), world Rect(1025,400,110,270).
    occluder_rect = (1025, 400, 1135, 670)
    screen_rect = (occluder_rect[0] - 320, occluder_rect[1] - 90, occluder_rect[2] - 320, occluder_rect[3] - 90)
    if screen_rect != (705, 310, 815, 580):
        raise RuntimeError("S01 foreground occluder screen rect drifted")
    draw.rounded_rectangle(occluder_rect, radius=5, fill=(37, 53, 64, 205), outline=INK, width=3)
    for y in range(430, 655, 38):
        draw.line((1029, y, 1131, y - 18), fill="#61717b", width=4)
    crop = world.crop((320, 90, 1600, 810))
    if crop.size != (1280, 720):
        raise RuntimeError("S01 Camera B overlay source crop drifted")
    overlay_draw = ImageDraw.Draw(crop, "RGBA")
    overlay_draw.rectangle((0, 0, W, 54), fill=INK)
    overlay_draw.rectangle((0, 648, W, H), fill=INK)
    path = OUT / "PV01_S01_EVAC_WORLD_overlay_source_cam_B_1280x720.png"
    crop.convert("RGB").save(path, quality=95)
    return path


def generate_pv02() -> Path:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((0, 66, 632, H - 54), fill="#e4e8e9")
    draw.rectangle((648, 66, W, H - 54), fill="#1c2c3d")
    draw.line((640, 72, 640, H - 58), fill=GOLD, width=5)
    jicun = jicun_standard_cutout()
    fit_image(image, jicun, (42, 115, 390, 640), opacity=235, align="bottom")
    proxy_terminal(draw, (475, 485), damaged=True)
    draw.polygon(((390, 330), (590, 285), (610, 345), (410, 390)), fill="#53616a", outline=INK, width=3)
    text(draw, (435, 210), "A / 常态", 17, NAVY, bold=True)
    rounded_panel(draw, (330, 125, 600, 198), WHITE, NAVY_2, 2, 5)
    wrapped_text(draw, (348, 140, 582, 190), "“下一项工作是……”", 20, INK, bold=True)
    gz = guardian_cutout()
    chest = gz.crop((int(gz.width * 0.10), 0, int(gz.width * 0.90), int(gz.height * 0.57)))
    fit_image(image, chest, (705, 112, 1185, 622), align="bottom")
    draw.ellipse((895, 300, 1010, 415), outline=(215, 163, 60, 110), width=11)
    draw.ellipse((903, 308, 1002, 407), outline=(207, 63, 55, 120), width=4)
    text(draw, (690, 88), "B / 仅声源转移边缘", 17, "#f0c86e", bold=True)
    rounded_panel(draw, (695, 475, 1200, 567), "#f7f5ee", GOLD, 3, 5)
    wrapped_text(draw, (716, 490, 1180, 555), "“阻止敌体进入居民区。”\n“旧守护者？”  “我在。”", 20, INK, bold=True)
    points = []
    for x in range(395, 895, 8):
        amp = 15 + 12 * math.sin(x * 0.08)
        points.append((x, 395 + amp * math.sin(x * 0.22)))
    draw.line(points, fill=GOLD, width=4)
    arrow(draw, (580, 395), (720, 395), GOLD, 5, 14)
    text(draw, (640, 420), "同一句话 / 声轨不断", 15, GOLD, bold=True, anchor="ma")
    focus_marker(draw, (958, 360), "胸灯回应", GOLD)
    safe_area(draw)
    header(image, "PV02_S03_SAME_BODY", "S03 同体揭示 / 两帧声源续接", "A常态 + B局部峰值")
    footer(image, "Shot Space | 终端是远端外壳 | 纪存只报路，不驾驶四肢")
    path = OUT / "PV02_S03_SAME_BODY_1280x720.png"
    image.convert("RGB").save(path, quality=95)
    return path


def generate_pv03() -> Path:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((20, 82, 525, 640), fill="#dfe6e7", outline=NAVY_2, width=3)
    draw.rectangle((545, 82, 1260, 640), fill="#192735", outline=NAVY_2, width=3)
    text(draw, (42, 96), "万机馆 / STATIC", 15, NAVY, bold=True)
    text(draw, (570, 96), "代哥东区封存中心 / REMOTE", 15, "#cfd9df", bold=True)
    jicun = jicun_standard_cutout()
    fit_image(image, jicun, (40, 150, 270, 620), opacity=220, align="bottom")
    gz = guardian_cutout()
    chest = gz.crop((int(gz.width * 0.16), 0, int(gz.width * 0.84), int(gz.height * 0.50)))
    fit_image(image, chest, (250, 160, 505, 585), opacity=225, align="bottom")
    qihai = qihai_cutout()
    fit_image(image, qihai, (705, 115, 1068, 628), align="bottom")
    draw.rectangle((570, 128, 690, 610), fill=(41, 57, 70, 210), outline="#617486", width=2)
    for y in (170, 270, 370):
        draw.rectangle((588, y, 670, y + 58), fill="#425565", outline="#71828e")
    text(draw, (630, 515), "同僚\n轮廓", 15, "#b7c3ca", anchor="mm")
    rounded_panel(draw, (1040, 145, 1228, 285), "#f5f4ef", RED, 3, 5)
    text(draw, (1134, 165), "停机令", 17, RED_2, bold=True, anchor="ma")
    draw.ellipse((1092, 200, 1176, 284), outline=RED, width=7)
    draw.line((1108, 216, 1160, 268), fill=RED, width=7)
    draw.line((1160, 216, 1108, 268), fill=RED, width=7)
    draw.rectangle((1040, 304, 1228, 354), fill="#2f4e45", outline=GREEN, width=3)
    text(draw, (1134, 317), "本人命令：已撤回", 16, "#dceadf", bold=True, anchor="ma")
    rounded_panel(draw, (785, 440, 1225, 585), "#f7f6f1", GOLD, 2, 5)
    wrapped_text(draw, (805, 455, 1205, 565), "“观众呢？”\n“兜灯呢？”\n“这道命令是我签的。我自己撤。”", 19, INK, bold=True)
    arrow(draw, (955, 385), (1128, 327), GOLD, 4, 13)
    focus_marker(draw, (1128, 330), "红标熄灭", GOLD)
    safe_area(draw)
    header(image, "PV03_S04_QIHAI_SCREEN", "S04 七海撤令 / 双地ADV", "七海仅远程出现")
    footer(image, "Screen Space | CML004成年身份锚 | 不加载馆内Sprite或旧头像")
    path = OUT / "PV03_S04_QIHAI_SCREEN_1280x720.png"
    image.convert("RGB").save(path, quality=95)
    return path


def panel(draw: ImageDraw.ImageDraw, box, index: int, title_value: str):
    rounded_panel(draw, box, "#f7f7f3", "#8a969e", 2, 5)
    x0, y0, x1, _ = box
    draw.rectangle((x0, y0, x1, y0 + 38), fill=NAVY)
    text(draw, (x0 + 12, y0 + 8), f"{index:02d}", 15, GOLD, bold=True)
    text(draw, (x0 + 47, y0 + 7), title_value, 16, WHITE, bold=True)


def generate_pv04() -> Path:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    gz = guardian_cutout()
    boxes = [(20 + i * 250, 92, 258 + i * 250, 608) for i in range(5)]
    titles = ["左手按台", "膝扣崩开", "缓慢直身", "肩撞裂墙", "第二步站稳"]
    for i, (box, title_value) in enumerate(zip(boxes, titles), start=1):
        panel(draw, box, i, title_value)
        x0, y0, x1, y1 = box
        if i == 1:
            fit_image(image, gz, (x0 + 42, y0 + 65, x1 - 20, y1 - 64), align="bottom")
            draw.rectangle((x0 + 10, y1 - 130, x1 - 10, y1 - 90), fill="#6e7880", outline=INK, width=2)
            arrow(draw, (x0 + 80, y1 - 190), (x0 + 60, y1 - 125), RED, 4, 12)
        elif i == 2:
            lower = gz.crop((0, int(gz.height * 0.45), gz.width, gz.height))
            fit_image(image, lower, (x0 + 24, y0 + 95, x1 - 24, y1 - 68), align="bottom")
            for px, py in ((x0 + 58, y1 - 240), (x1 - 65, y1 - 220), (x0 + 110, y1 - 170)):
                draw.line((px - 12, py - 12, px + 14, py + 14), fill=RED, width=4)
                draw.line((px + 12, py - 12, px - 10, py + 14), fill=GOLD, width=3)
        elif i == 3:
            fit_image(image, gz, (x0 + 30, y0 + 55, x1 - 30, y1 - 52), align="bottom")
            arrow(draw, (x1 - 35, y1 - 120), (x1 - 35, y0 + 90), GOLD, 4, 12)
            text(draw, (x0 + 20, y1 - 60), "18m / 双前臂完整", 13, NAVY, bold=True)
        elif i == 4:
            fit_image(image, gz, (x0 + 15, y0 + 75, x1 - 42, y1 - 52), align="bottom")
            draw.rectangle((x1 - 58, y0 + 50, x1 - 12, y1 - 45), fill="#aeb8bd", outline=INK, width=3)
            for yy in range(y0 + 130, y1 - 80, 70):
                draw.line((x1 - 58, yy, x1 - 20, yy + 32), fill=RED_2, width=3)
            arrow(draw, (x1 - 115, y0 + 240), (x1 - 48, y0 + 240), RED, 5, 14)
        else:
            fit_image(image, gz, (x0 + 34, y0 + 65, x1 - 24, y1 - 52), align="bottom")
            draw.ellipse((x0 + 25, y1 - 72, x1 - 18, y1 - 44), fill=(70, 82, 90, 35), outline="#7d8a92")
            draw.line((x0 + 65, y1 - 78, x0 + 105, y1 - 58), fill=TEAL, width=5)
            draw.line((x0 + 128, y1 - 64, x0 + 178, y1 - 64), fill=TEAL, width=5)
        text(draw, ((x0 + x1) // 2, y1 - 34), "V10X / demo_visual_candidate", 11, MUTED, anchor="ma")
    safe_area(draw)
    header(image, "PV04_S05_GUARDIAN_STAND", "S05 馆守Z起身 / 五拍缩略镜头板", "D2视觉母版证据")
    footer(image, "Shot Space | V10X实际Previs + CML008身份复核 | 右肩旧伤、双前臂完整")
    path = OUT / "PV04_S05_GUARDIAN_STAND_1280x720.png"
    image.convert("RGB").save(path, quality=95)
    return path


def iso_center(x: int, y: int) -> tuple[int, int]:
    return 420 + (x - y) * 35, 150 + (x + y) * 18


def iso_vertices(x: int, y: int) -> tuple[tuple[int, int], ...]:
    cx, cy = iso_center(x, y)
    return ((cx, cy - 18), (cx + 35, cy), (cx, cy + 18), (cx - 35, cy))


def cells_bbox(cells: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    points = [point for x, y in cells for point in iso_vertices(x, y)]
    return min(x for x, _ in points), min(y for _, y in points), max(x for x, _ in points), max(y for _, y in points)


def draw_s06_joint_state(*, report_chrome: bool, annotations: bool) -> Image.Image:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((0, 0, W, 54), fill=INK)
    draw.rectangle((0, 54, W, 648), fill="#e9edef")
    draw.rectangle((0, 648, W, H), fill=INK)

    affected = {(x, y) for x in range(5, 8) for y in range(0, 6)}
    guardian_cells = {(x, y) for x in range(5, 7) for y in range(3, 5)}
    breaker_cells = {(x, y) for x in range(5, 8) for y in range(6, 9)}
    cell_count = 0
    for layer in range(20):
        for y in range(9):
            for x in range(12):
                if x + y != layer:
                    continue
                cell_count += 1
                fill = "#d9e1e4"
                if y <= 1:
                    fill = "#ead1ce"
                elif y >= 7:
                    fill = "#d8e5dc"
                draw.polygon(iso_vertices(x, y), fill=fill, outline="#89969e")
                if (x, y) in affected:
                    draw.polygon(iso_vertices(x, y), fill=(207, 63, 55, 75), outline=RED_2)
                if (x, y) in guardian_cells:
                    draw.polygon(iso_vertices(x, y), fill=(49, 86, 115, 130), outline=NAVY)
                if (x, y) in breaker_cells:
                    draw.polygon(iso_vertices(x, y), fill=(12, 17, 23, 165), outline=BLACK)
    if cell_count != 108:
        raise RuntimeError(f"S06 grid must contain 108 cells, got {cell_count}")

    all_cells = [(x, y) for x in range(12) for y in range(9)]
    if cells_bbox(all_cells) != (105, 132, 840, 510):
        raise RuntimeError("S06 board bbox drifted")
    if cells_bbox(sorted(affected)) != (385, 222, 700, 384):
        raise RuntimeError("S06 intent band bbox drifted")
    if cells_bbox(sorted(guardian_cells)) != (420, 276, 560, 348):
        raise RuntimeError("S06 Guardian Z footprint drifted")
    if cells_bbox(sorted(breaker_cells)) != (280, 330, 490, 438):
        raise RuntimeError("S06 BREAKER footprint drifted")
    if iso_center(1, 2) != (385, 204) or iso_center(5, 3) != (490, 294) or iso_center(5, 6) != (385, 348):
        raise RuntimeError("S06 anchor center drifted")

    if annotations:
        draw.line((105, 216, 805, 216), fill=RED, width=3)
        text(draw, (118, 186), "北侧城市安全线", 15, RED_2, bold=True)
        text(draw, (735, 500), "南侧承冲区", 14, GREEN, bold=True, anchor="ra")
    proxy_shield(draw, (385, 204), 44, scorch=3)
    fit_image(image, guardian_cutout(), (458, 260, 522, 344), align="bottom")
    proxy_breaker(draw, (300, 338, 470, 426), label=False)
    if annotations:
        draw.polygon(((484, 342), (496, 342), (490, 352)), fill=TEAL)
        draw.polygon(((379, 330), (391, 330), (385, 320)), fill=RED)
        arrow(draw, (385, 348), (595, 240), RED, 7, 18)

    # Exact program-alignment UI locks.
    draw.rectangle((885, 78, 1240, 196), fill="#fff3f0", outline=RED, width=2)
    draw.rectangle((885, 210, 1240, 624), fill="#f7f7f3", outline=NAVY_2, width=2)
    if annotations:
        text(draw, (903, 91), "敌方意图", 18, INK, bold=True)
        wrapped_text(draw, (903, 119, 1222, 186), "BREAKER / 冲撞\n目标：北侧城市安全线\n受影响格：x=5..7, y=0..5", 15, INK, bold=True, spacing=3)
        text(draw, (903, 224), "T2 / STAGE 1", 17, NAVY, bold=True)
        text(draw, (903, 251), "north_safety_line_held = true", 13, GREEN, bold=True)
        text(draw, (903, 274), "redirected / shield / block = false", 13, MUTED)
        text(draw, (903, 297), "finisher_ready / triggered = false", 13, MUTED)
    commands = [
        ("移动", NAVY_2, True),
        ("推击", RED_2, True),
        ("防御 / 支撑", TEAL, True),
        ("调取重盾", GOLD, True),
        ("结束行动", INK_2, True),
        ("强化盾拍", MUTED, False),
    ]
    if len(commands) != len(S06_BUTTON_RECTS):
        raise RuntimeError("S06 command/button count drifted")
    for (label, color, enabled), (x0, y0, width, height) in zip(commands, S06_BUTTON_RECTS):
        draw.rectangle((x0, y0, x0 + width, y0 + height), fill=WHITE if enabled else "#d9dde0", outline=color, width=2)
        if annotations:
            text(draw, (x0 + width // 2, y0 + 8), label, 15, color, bold=True, anchor="ma")
    if annotations:
        rounded_panel(draw, (903, 548, 1222, 607), "#303b44", INK, 2, 4)
        text(draw, (921, 558), "面向：馆守Z 南 / BREAKER 北", 14, WHITE, bold=True)
        text(draw, (921, 582), "profile c01cdv1_s06_g1_v1", 13, "#c9d3d9")

    if report_chrome:
        text(draw, (20, 16), "PV05_S06_TACTICAL_READ", 14, WHITE, bold=True)
        text(draw, (285, 13), "S06 等距战棋 / T2-S1 联合对齐态", 22, WHITE, bold=True)
        text(draw, (W - 20, 17), "D3 evidence / 108 cells", 13, "#cfd8de", anchor="ra")
        text(draw, (20, 664), S06_JOINT_STATE, 14, WHITE, bold=True)
        text(draw, (W - 20, 664), "candidate_previs | runtime_allowed=false", 14, "#f0c86e", anchor="ra")
        text(draw, (W - 20, 688), f"fp {EXPECTED_FINGERPRINT[:12]}", 12, "#b8c4cc", anchor="ra")
    return image


def generate_pv05() -> Path:
    path = OUT / "PV05_S06_TACTICAL_READ_1280x720.png"
    draw_s06_joint_state(report_chrome=True, annotations=True).convert("RGB").save(path, quality=95)
    return path


def generate_pv05_overlay_source() -> Path:
    path = OUT / "PV05_S06_TACTICAL_READ_overlay_source_t2s1_1280x720.png"
    draw_s06_joint_state(report_chrome=False, annotations=False).convert("RGB").save(path, quality=95)
    return path


def paste_guardian_with_shield(image: Image.Image, box, *, hot=False, scorch=3, angle=0):
    gz = guardian_cutout()
    if angle:
        gz = gz.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    placed = fit_image(image, gz, box, align="bottom")
    draw = ImageDraw.Draw(image, "RGBA")
    x0, y0, x1, y1 = placed
    proxy_shield(draw, (x0 + int((x1 - x0) * 0.24), y0 + int((y1 - y0) * 0.57)), int((y1 - y0) * 0.62), scorch=scorch, hot=hot)


def generate_pv06() -> Path:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    boxes = [(20, 92, 418, 610), (441, 92, 839, 610), (862, 92, 1260, 610)]
    titles = ["01 挡下赤红冲击", "02 第四焦痕 / 南向推进", "03 强化盾拍 / 首次倒地"]
    for box, title_value in zip(boxes, titles):
        rounded_panel(draw, box, "#e8ecee", "#86939b", 2, 5)
        x0, y0, x1, y1 = box
        draw.rectangle((x0, y0, x1, y0 + 38), fill=NAVY)
        text(draw, (x0 + 14, y0 + 8), title_value, 16, WHITE, bold=True)
    paste_guardian_with_shield(image, (55, 155, 285, 585), hot=True, scorch=3)
    proxy_breaker(draw, (285, 190, 400, 475), label=False)
    arrow(draw, (395, 310), (235, 310), RED, 12, 22)
    draw.line((225, 305, 140, 245), fill=RED, width=7)
    draw.line((225, 315, 140, 375), fill=RED, width=7)
    text(draw, (220, 565), "双前臂完整", 14, NAVY, bold=True, anchor="ma")
    paste_guardian_with_shield(image, (470, 150, 720, 585), hot=False, scorch=4, angle=-2)
    proxy_breaker(draw, (690, 205, 815, 486), label=False)
    arrow(draw, (725, 505), (780, 555), TEAL, 9, 18)
    text(draw, (638, 530), "向南", 20, TEAL, bold=True)
    focus_marker(draw, (525, 325), "第四焦痕", GOLD)
    paste_guardian_with_shield(image, (895, 145, 1120, 585), hot=False, scorch=4, angle=3)
    proxy_breaker(draw, (1055, 360, 1240, 540), knocked=True, label=False)
    arrow(draw, (1015, 310), (1132, 418), RED, 12, 24)
    draw.arc((1030, 265, 1185, 430), 190, 300, fill=GOLD, width=7)
    rounded_panel(draw, (910, 535, 1234, 594), "#f8f6ed", GOLD, 2, 5)
    text(draw, (1072, 547), "第一次倒地 / 未毁 / 未破甲", 15, INK, bold=True, anchor="ma")
    safe_area(draw)
    header(image, "PV06_S07_SHIELD_IMPACT", "S07 盾拍首胜 / 三帧高光", "D0-B 已冻结")
    footer(image, "Shot Space | 玩家确认后演出 | BREAKER_FIRST_KNOCKDOWN=true / DESTROYED=false")
    path = OUT / "PV06_S07_SHIELD_IMPACT_1280x720.png"
    image.convert("RGB").save(path, quality=95)
    return path


def generate_space_contact_sheet() -> Path:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    cols = [(18, 385), (435, 802), (852, 1262)]
    titles = ["WORLD SPACE", "SCREEN SPACE", "SHOT SPACE"]
    for (x0, x1), title_value in zip(cols, titles):
        draw.rectangle((x0, 84, x1, 628), fill="#f7f7f3", outline="#8c989f", width=2)
        draw.rectangle((x0, 84, x1, 120), fill=NAVY)
        text(draw, ((x0 + x1) // 2, 93), title_value, 16, WHITE, bold=True, anchor="ma")
    q = jicun_q_cutout()
    standard = jicun_standard_cutout()
    gz = guardian_cutout()
    fit_image(image, q, (48, 135, 190, 365), align="bottom")
    fit_image(image, gz, (215, 165, 360, 365), align="bottom")
    text(draw, (202, 376), "Q比例：同一深蓝外套/终端/头发", 13, NAVY, bold=True, anchor="ma")
    fit_image(image, standard, (465, 135, 650, 390), align="bottom")
    fit_image(image, gz, (655, 145, 785, 390), align="bottom")
    text(draw, (620, 400), "半身焦点：不长期挂旧头像框", 13, NAVY, bold=True, anchor="ma")
    head_j = standard.crop((int(standard.width * 0.13), 0, int(standard.width * 0.88), int(standard.height * 0.43)))
    head_g = gz.crop((int(gz.width * 0.10), 0, int(gz.width * 0.90), int(gz.height * 0.48)))
    fit_image(image, head_j, (885, 145, 1050, 360), align="bottom")
    fit_image(image, head_g, (1055, 145, 1230, 360), align="bottom")
    text(draw, (1056, 375), "正比例关键帧：身份锚不变", 13, NAVY, bold=True, anchor="ma")
    y = 445
    labels = [
        ("纪存", "黑发蓝眼 / 成年比例 / 长外套 / 左臂终端", NAVY_2),
        ("馆守Z", "金色冠 / 红色胸肩连续面 / 圆柱前臂 / 双臂完整", RED_2),
        ("A/B", "A保持主体；B只贴声源、胸灯和冲击边缘", GOLD),
    ]
    for label, value, color in labels:
        rounded_panel(draw, (42, y, 1235, y + 46), WHITE, color, 2, 5)
        text(draw, (60, y + 10), label, 16, color, bold=True)
        text(draw, (155, y + 10), value, 16, INK)
        y += 55
    safe_area(draw)
    header(image, "SPACE_CONTACT_SHEET", "World / Screen / Shot 身份联系表", "同一角色与机体跨载体")
    footer(image, "Identity continuity | 纪存使用最新Standard/Q方向 | 馆守Z使用V10X Previs")
    path = OUT / "SPACE_CONTACT_SHEET_1280x720.png"
    image.convert("RGB").save(path, quality=95)
    return path


def generate_gz_identity_comparison() -> Path:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    rounded_panel(draw, (20, 88, 590, 625), "#f7f7f3", NAVY_2, 3, 5)
    rounded_panel(draw, (610, 88, 1260, 625), "#f7f7f3", RED_2, 3, 5)
    text(draw, (305, 104), "CML008 / Current身份锚", 18, NAVY, bold=True, anchor="ma")
    text(draw, (935, 104), "V10X / 实际E02 Previs候选", 18, RED_2, bold=True, anchor="ma")
    base = load_visual("VIS_CML008_CURRENT_BASE")
    fit_image(image, base, (42, 138, 568, 545))
    gz = guardian_cutout()
    fit_image(image, gz, (685, 135, 985, 575), align="bottom")
    rounded_panel(draw, (1000, 150, 1238, 520), "#e9edef", GOLD, 2, 5)
    wrapped_text(
        draw,
        (1020, 172, 1218, 500),
        "复核锚点\n\n18米重体量\n金色主冠\n脸谱与眼灯\n红胸/肩连续面\n圆柱双前臂\nE02双臂完整\n右肩旧伤\n\n状态\napproved=false\ndemo_visual_candidate",
        16,
        INK,
        bold=True,
        spacing=6,
    )
    draw.line((590, 355, 610, 355), fill=GOLD, width=6)
    safe_area(draw)
    header(image, "GZ_IDENTITY_COMPARISON", "馆守Z 冻结身份锚 / V10X并排校对", "D2等待用户确认")
    footer(image, "Comparison only | 不升母版、不派生Runtime、不引入飞翼或后期臂态")
    path = OUT / "GZ_IDENTITY_COMPARISON_1280x720.png"
    image.convert("RGB").save(path, quality=95)
    return path


def generate_placeholder_audio(duration: float = 36.0) -> Path:
    path = OUT / "C01E02_G1_ANIMATIC_placeholder_audio.wav"
    sample_rate = 44100
    cue_times = [0.0, 4.0, 8.0, 12.0, 17.0, 21.0, 27.0, 32.0]
    total = int(duration * sample_rate)
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        frames = bytearray()
        for index in range(total):
            t = index / sample_rate
            value = 0.018 * math.sin(2 * math.pi * 52 * t)
            for cue in cue_times:
                dt = t - cue
                if 0 <= dt < 0.16:
                    value += 0.13 * (1 - dt / 0.16) * math.sin(2 * math.pi * 740 * t)
            if 12.0 <= t < 13.2:
                value *= 0.18
            if 31.2 <= t < 31.45:
                value += 0.18 * math.sin(2 * math.pi * 92 * t) * (1 - (t - 31.2) / 0.25)
            frames.extend(struct.pack("<h", max(-32767, min(32767, int(value * 32767)))))
        output.writeframes(frames)
    return path


def generate_animatic(
    slides: list[tuple[Path, float, str]],
    *,
    preserve_audio: bool = False,
    preserve_shot_list: bool = False,
) -> tuple[Path, Path, Path]:
    audio = OUT / "C01E02_G1_ANIMATIC_placeholder_audio.wav"
    if preserve_audio:
        if not audio.is_file():
            raise RuntimeError(f"Preserved animatic audio missing: {audio.name}")
    else:
        audio = generate_placeholder_audio(sum(duration for _, duration, _ in slides))
    shot_list = OUT / "animatic-shot-list.tsv"
    if preserve_shot_list:
        if not shot_list.is_file():
            raise RuntimeError(f"Preserved animatic shot list missing: {shot_list.name}")
    else:
        lines = ["shot_id\tstart_seconds\tduration_seconds\tsource\tcarrier\truntime_allowed"]
        cursor = 0.0
        for index, (path, duration, carrier) in enumerate(slides, start=1):
            lines.append(f"ANIM_{index:02d}\t{cursor:.1f}\t{duration:.1f}\t{path.name}\t{carrier}\tfalse")
            cursor += duration
        shot_list.write_text("\n".join(lines) + "\n", encoding="utf-8")
    video = OUT / "C01E02_G1_ANIMATIC_1280x720_36s.mp4"
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for the G1 animatic")
    command = [ffmpeg, "-y"]
    for path, _, _ in slides:
        command.extend(["-i", str(path)])
    command.extend(["-i", str(audio)])
    filters = []
    labels = []
    for index, (_, duration, _) in enumerate(slides):
        frames = round(duration * FPS)
        fade_out = max(0.0, duration - 0.28)
        filters.append(
            f"[{index}:v]scale={W}:{H},zoompan=z='min(zoom+0.00035,1.025)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
            f"fade=t=in:st=0:d=0.24,fade=t=out:st={fade_out:.2f}:d=0.24,setsar=1[v{index}]"
        )
        labels.append(f"[v{index}]")
    filters.append("".join(labels) + f"concat=n={len(slides)}:v=1:a=0[vout]")
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[vout]",
            "-map",
            f"{len(slides)}:a",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-shortest",
            "-map_metadata",
            "-1",
            "-metadata",
            "creation_time=1970-01-01T00:00:00Z",
            str(video),
        ]
    )
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return video, audio, shot_list


def write_source_receipt() -> Path:
    path = OUT / "source-validation-receipt.tsv"
    fields = [
        "visual_id",
        "freeze_kind",
        "snapshot_ref_or_contract_version",
        "path",
        "expected_sha256",
        "actual_sha256",
        "validation",
        "runtime_allowed",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for visual_id, row in VISUALS.items():
            writer.writerow(
                {
                    "visual_id": visual_id,
                    "freeze_kind": row["freeze_kind"],
                    "snapshot_ref_or_contract_version": row["snapshot_ref_or_contract_version"],
                    "path": row["path"],
                    "expected_sha256": row["sha256"],
                    "actual_sha256": sha256(Path(row["resolved_path"])),
                    "validation": "match",
                    "runtime_allowed": "false",
                }
            )
    return path


def write_self_check() -> Path:
    path = OUT / "g1-user-question-self-check.tsv"
    rows = [
        ("JOINT_S01_ALIGNMENT", "S01 Camera B是否与制作人程序坐标逐点同位", f"PV01_S01_EVAC_WORLD_coordinate-lock.tsv;PV01 Camera B overlay source;{S01_JOINT_STATE}", "aligned_for_producer_overlay"),
        ("JOINT_S06_ALIGNMENT", "S06是否为程序同一等距投影与同一T2/S1状态", f"PV05 report source;PV05 overlay source;{S06_JOINT_STATE}", "aligned_for_producer_overlay"),
        ("D1_EXPLORE", "S01/S03是否像轻RPG探索而非横版或俯视小人", "保留PV01三相机;新增Camera B overlay source;PV02声源镜头", "ready_for_user_decision"),
        ("IDENTITY_CROSS_SPACE", "World/Shot是否仍读成同一人物与机体", "SPACE_CONTACT_SHEET;GZ_IDENTITY_COMPARISON", "ready_for_user_decision"),
        ("D2_GZ_MASTER", "V10X是否可作为Demo继续派生基准", "PV04;PV05;PV06;GZ_IDENTITY_COMPARISON", "ready_for_user_decision"),
        ("D3_TACTICAL_READ", "是否一眼读懂守北线/改向/取盾", f"PV05;{S06_JOINT_STATE}", "ready_for_user_decision"),
        ("MOTION_VALUE", "关键帧与程序运动是否足以决定后续投入", "36秒Animatic;PV04;PV06", "ready_for_user_decision"),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("question_id", "question", "evidence", "internal_status"))
        writer.writerows(rows)
    return path


def artifact_dimensions(path: Path) -> str:
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            return f"{image.width}x{image.height}"
    if path.suffix.lower() == ".mp4":
        return "1280x720"
    if path.suffix.lower() == ".wav":
        return "mono/44100Hz"
    return "n/a"


def write_asset_manifest(artifacts: list[dict[str, str]]) -> Path:
    path = OUT / "asset-manifest.tsv"
    fields = [
        "asset_id",
        "path",
        "type",
        "dimensions_or_format",
        "duration_seconds",
        "source_visual_ids",
        "source_snapshot_or_contract",
        "parent_slot",
        "lifecycle",
        "status",
        "sha256",
        "runtime_allowed",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for item in artifacts:
            artifact = OUT / item["path"]
            row = dict(item)
            row["dimensions_or_format"] = artifact_dimensions(artifact)
            row["sha256"] = sha256(artifact)
            row["runtime_allowed"] = "false"
            writer.writerow(row)
    return path


def write_completion_report(manifest: Path, artifacts: list[dict[str, str]]) -> Path:
    path = OUT / "completion-report.md"
    report = f"""# C01E02 G1.1 Joint Art Alignment Completion Report

> Status: `candidate_previs_g1_1_s01_occluder_corrected / producer_overlay_recheck_pending / D1-D3_pending`
>
> Contract: `{CONTRACT['contract_id']} / {CONTRACT['contract_version']}`
>
> Snapshot: `{CONTRACT['snapshot_ref']}`
>
> Content fingerprint: `{EXPECTED_FINGERPRINT}`
>
> Runtime permission: `false` for every deliverable

## Scope completed

- Preserved the original PV01 clean plate and Camera A/B/C review images byte-for-byte.
- Preserved `PV01_S01_EVAC_WORLD_coordinate-lock.tsv`; the Camera B overlay source now masks y=0..54 and y=648..720 as text-free HUD safe bands while keeping the middle world anchors unchanged.
- Final point correction: the foreground occluder now matches the producer exactly at world `Rect(1025,400,110,270)` / Camera B screen `Rect(705,310,110,270)`.
- Rebuilt only PV05 to the producer program's isometric projection and `{S06_JOINT_STATE}` gameplay state, with the six exact program button rectangles.
- The PV05 overlay source contains geometry only: board, affected cells, both silhouettes, shield, panel boundaries, and button rectangles; all art-side annotations are absent.
- The previously corrected PV05, PV05 overlay source, 36-second Animatic, self-check, shot list, and audio were hash-protected and not regenerated in this final S01-only pass.
- PV02/PV03/PV04/PV06, identity/contact sheets, source receipt, and placeholder audio were not regenerated.

## Delivery inventory

- Artifact rows: `{len(artifacts)}` in `{manifest.name}`.
- New S01 overlay source and both PV05 outputs: `1280x720`.
- Coordinate lock: tab-separated world/screen/shot alignment evidence.
- Animatic: `1280x720`, 24 fps, 36 seconds, procedural placeholder audio.

## Boundaries preserved

- No Godot, Canon, producer contract, source manifest, or runtime files were modified.
- No external generation service or video-generation service was used.
- No design promotion, identity lock, Runtime promotion, or batch derivative was created.
- All seven frozen visual inputs are still covered by the unchanged `source-validation-receipt.tsv`.
- Every protected G1/G1.1 file, including both S06 outputs and the Animatic, was hash-checked before and after the S01-only correction.
- All outputs remain `runtime_allowed=false` and are for composition/overlay review only.

## User decisions still open

- D1: approve or reject the oblique shallow-X/Y exploration presentation.
- D2: approve or reject V10X as the Demo derivation base.
- D3: approve or reject the tactical pose puzzle read.

Internal technical completion is not user visual acceptance. Stop after the G1.1 S01 occluder correction and wait for the producer pixel-overlay recheck plus D1-D3 decisions.
"""
    path.write_text(report, encoding="utf-8")
    return path


def write_delivery_hashes(exclude: set[str] | None = None) -> Path:
    path = OUT / "delivery-hashes.sha256"
    excluded = {path.name}
    if exclude:
        excluded.update(exclude)
    lines = []
    for item in sorted(OUT.iterdir(), key=lambda p: p.name):
        if not item.is_file() or item.name in excluded or item.name.startswith("."):
            continue
        lines.append(f"{sha256(item)}  {item.name}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def verify_preserved_g11_assets() -> None:
    for name, expected in PRESERVED_G11_HASHES.items():
        path = OUT / name
        if not path.is_file():
            raise RuntimeError(f"Protected G1 file missing: {name}")
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"Protected G1 hash mismatch: {name}: {actual}")


def read_existing_asset_manifest() -> list[dict[str, str]]:
    path = OUT / "asset-manifest.tsv"
    if not path.is_file():
        raise RuntimeError("Existing G1 asset manifest is required for incremental G1.1 generation")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if any(row.get("runtime_allowed", "").lower() != "false" for row in rows):
        raise RuntimeError("Existing G1 manifest contains a runtime-enabled asset")
    g11_asset_ids = {
        "PV01_S01_EVAC_WORLD_COORDINATE_LOCK",
        "PV01_S01_EVAC_WORLD_CAM_B_OVERLAY_SOURCE",
        "PV05_S06_TACTICAL_OVERLAY_SOURCE",
    }
    base_rows = [row for row in rows if row["asset_id"] not in g11_asset_ids]
    if len(base_rows) != 17:
        raise RuntimeError(f"Expected 17 base G1 manifest rows, got {len(base_rows)}")
    return base_rows


def main() -> None:
    verify_preserved_g11_assets()
    artifact_rows = read_existing_asset_manifest()

    coordinate_lock = OUT / "PV01_S01_EVAC_WORLD_coordinate-lock.tsv"
    s01_overlay = generate_pv01_overlay_source_cam_b()
    pv05 = OUT / "PV05_S06_TACTICAL_READ_1280x720.png"
    s06_overlay = OUT / "PV05_S06_TACTICAL_READ_overlay_source_t2s1_1280x720.png"
    video = OUT / "C01E02_G1_ANIMATIC_1280x720_36s.mp4"
    audio = OUT / "C01E02_G1_ANIMATIC_placeholder_audio.wav"
    shot_list = OUT / "animatic-shot-list.tsv"
    self_check = OUT / "g1-user-question-self-check.tsv"

    by_id = {row["asset_id"]: row for row in artifact_rows}
    by_id["PV05_S06_TACTICAL_READ"].update(
        source_snapshot_or_contract=f"{CONTRACT['snapshot_ref']};{S06_JOINT_STATE}",
        status="aligned_for_producer_overlay",
        notes="program isometric projection; exact T2/S1 state and exact six program button rectangles",
    )
    by_id["C01E02_G1_ANIMATIC"]["path"] = video.name
    by_id["C01E02_G1_PLACEHOLDER_AUDIO"]["path"] = audio.name
    by_id["ANIMATIC_SHOT_LIST"]["path"] = shot_list.name
    by_id["G1_USER_QUESTION_SELF_CHECK"]["path"] = self_check.name
    by_id["GENERATOR_SOURCE"].update(
        status="g1_1_s01_occluder_correction_complete",
        notes="protected-hash incremental generator; S01 foreground occluder correction only",
    )
    artifact_rows.extend(
        [
            {"asset_id": "PV01_S01_EVAC_WORLD_COORDINATE_LOCK", "path": coordinate_lock.name, "type": "tsv", "duration_seconds": "", "source_visual_ids": "VIS_JICUN_Q_RUNTIME_V1", "source_snapshot_or_contract": S01_JOINT_STATE, "parent_slot": "BG_C01CDV1_EAST_ROUTE;SPR_C01CDV1_JICUN_WORLD", "lifecycle": "candidate_previs_evidence", "status": "aligned_for_producer_overlay", "notes": "exact world/screen Camera B lock; runtime false"},
            {"asset_id": "PV01_S01_EVAC_WORLD_CAM_B_OVERLAY_SOURCE", "path": s01_overlay.name, "type": "png", "duration_seconds": "", "source_visual_ids": "VIS_JICUN_Q_RUNTIME_V1", "source_snapshot_or_contract": S01_JOINT_STATE, "parent_slot": "BG_C01CDV1_EAST_ROUTE;SPR_C01CDV1_JICUN_WORLD", "lifecycle": "candidate_previs", "status": "aligned_for_producer_overlay", "notes": "Camera B exact crop; text-free HUD bands; occluder world Rect(1025,400,110,270), screen Rect(705,310,110,270)"},
            {"asset_id": "PV05_S06_TACTICAL_OVERLAY_SOURCE", "path": s06_overlay.name, "type": "png", "duration_seconds": "", "source_visual_ids": "VIS_GUARDIAN_Z_V10X", "source_snapshot_or_contract": S06_JOINT_STATE, "parent_slot": "BG_C01CDV1_PLAZA_TACTICAL;UI_C01CDV1_TACTICAL_INTENT", "lifecycle": "candidate_previs", "status": "aligned_for_producer_overlay", "notes": "geometry-only joint source; no title, footer, board, unit, panel or button text"},
        ]
    )
    manifest = write_asset_manifest(artifact_rows)
    report = write_completion_report(manifest, artifact_rows)
    write_delivery_hashes()
    verify_preserved_g11_assets()
    print(f"Generated G1.1 S01 occluder correction with {len(artifact_rows)} manifest artifacts in {OUT}")
    print(f"Content fingerprint: {EXPECTED_FINGERPRINT}")
    print(f"Completion report: {report.name}")


if __name__ == "__main__":
    main()
