#!/usr/bin/env python3
"""Generate the G1.5-A1 Guardian Z Q/SD direction board from frozen inputs."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]

CONTRACT_COMMIT = "cf49dac4d539d23337999807114676c9d060ec3e"
CONTRACT_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/15-g1-5-representative-art-pilot.md"
CONTRACT_BLOB = "9fa5548a4ce81f935a86ba1f3ea322146a00e750"
CONTRACT_SHA256 = "844e9d15b8be1575f33b0b06992044a0cc7338284d27747802bce88eaae84b6f"
FROZEN_SNAPSHOT = "fe7a0764d11f5ac5f9d11accb7398df664132b0b"
CONTENT_FINGERPRINT = "944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94"
VISUAL_MANIFEST_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/09b-frozen-visual-snapshot.tsv"
BUILD_CONTRACT_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/13-demo-build-contract.json"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

INK = "#182936"
INK_SHADOW = "#0d1822"
NAVY = "#173650"
NAVY_LIGHT = "#285673"
RED = "#c83d36"
RED_SHADOW = "#8f2d2b"
IVORY = "#e9e5db"
SILVER = "#b9c2c7"
GOLD = "#d8a63e"
PAPER = "#eef1f2"
PAPER_LIGHT = "#fafaf7"
TEAL = "#4f9295"
MUTED = "#71808a"


@dataclass(frozen=True)
class Candidate:
    code: str
    stable_id: str
    title: str
    ratio: str
    head_scale: float
    shoulder_span: int
    shoulder_radius: int
    torso_bottom: int
    hip_y: int
    knee_y: int
    foot_y: int
    forearm_top: int
    forearm_bottom: int
    forearm_width: int
    stance: int
    strength: str
    tradeoff: str


CANDIDATES = (
    Candidate(
        "A",
        "CAND_GZ_QSD_A1_HEAVY_ICON_V1",
        "重装图标型",
        "约 3.3 头身",
        1.10,
        148,
        67,
        292,
        318,
        391,
        477,
        224,
        359,
        70,
        70,
        "96 px 识别最强；重量与老派超级系最明确。",
        "短腿与大前臂限制横移、推击等后续动作幅度。",
    ),
    Candidate(
        "B",
        "CAND_GZ_QSD_A1_BALANCED_GUARD_V1",
        "均衡守卫型",
        "约 3.8 头身",
        1.00,
        142,
        62,
        278,
        309,
        397,
        487,
        218,
        365,
        64,
        75,
        "头冠、红胸肩、双圆柱臂在 96/128 px 都清楚。",
        "重量略低于 A，但 2×2 格内的朝向和动作扩展最平衡。",
    ),
    Candidate(
        "C",
        "CAND_GZ_QSD_A1_ACTION_FRAME_V1",
        "动作骨架型",
        "约 4.2 头身",
        0.92,
        136,
        58,
        263,
        297,
        398,
        493,
        211,
        357,
        58,
        81,
        "腿部和关节留出最大动作空间，面向变化最利落。",
        "96 px 下主角机的厚重感与圆柱前臂存在感最弱。",
    ),
)


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{CONTRACT_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def validate_authority() -> tuple[dict[str, dict[str, str]], dict[str, bytes], str]:
    commit = subprocess.run(
        ["git", "rev-parse", f"{CONTRACT_COMMIT}^{{commit}}"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()
    if commit != CONTRACT_COMMIT:
        raise RuntimeError(f"Contract commit drifted: {commit}")

    blob = subprocess.run(
        ["git", "rev-parse", f"{CONTRACT_COMMIT}:{CONTRACT_PATH}"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()
    contract_bytes = git_bytes(CONTRACT_PATH)
    if blob != CONTRACT_BLOB or sha256_bytes(contract_bytes) != CONTRACT_SHA256:
        raise RuntimeError("G1.5 contract identity mismatch")

    build_contract = json.loads(git_bytes(BUILD_CONTRACT_PATH).decode("utf-8"))
    if build_contract["content_fingerprint"] != CONTENT_FINGERPRINT:
        raise RuntimeError("Content fingerprint mismatch")
    if build_contract["visual_manifest"]["entry_count"] != 7:
        raise RuntimeError("Frozen visual input count mismatch")

    manifest_bytes = git_bytes(VISUAL_MANIFEST_PATH)
    rows = list(csv.DictReader(io.StringIO(manifest_bytes.decode("utf-8")), delimiter="\t"))
    by_id = {row["visual_id"]: row for row in rows}
    required = ("VIS_CML008_CURRENT_BASE", "VIS_GUARDIAN_Z_V10X")
    if len(rows) != 7 or any(visual_id not in by_id for visual_id in required):
        raise RuntimeError("Required Guardian Z frozen visuals are missing")

    if by_id["VIS_CML008_CURRENT_BASE"]["lifecycle_or_role"] != "current_identity_anchor":
        raise RuntimeError("CML008 is not the frozen current identity anchor")
    if by_id["VIS_GUARDIAN_Z_V10X"]["lifecycle_or_role"] != "demo_visual_candidate;c01e02_intact_original_both_forearms":
        raise RuntimeError("V10X is not the intact E02 demo candidate")
    if any(by_id[visual_id]["runtime_allowed"].lower() != "false" for visual_id in required):
        raise RuntimeError("A frozen Guardian Z input is unexpectedly runtime-enabled")

    source_bytes: dict[str, bytes] = {}
    for visual_id in required:
        data = git_bytes(by_id[visual_id]["path"])
        if sha256_bytes(data) != by_id[visual_id]["sha256"]:
            raise RuntimeError(f"Frozen visual hash mismatch: {visual_id}")
        source_bytes[visual_id] = data
    return by_id, source_bytes, sha256_bytes(manifest_bytes)


def polygon(draw: ImageDraw.ImageDraw, points, fill, *, width: int = 5) -> None:
    draw.polygon(points, fill=fill, outline=INK)
    draw.line((*points, points[0]), fill=INK, width=width, joint="curve")


def rounded(draw: ImageDraw.ImageDraw, box, radius: int, fill, *, width: int = 5, outline=INK) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_guardian_qsd(candidate: Candidate) -> Image.Image:
    image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    cx = 256
    left_x = cx - candidate.stance
    right_x = cx + candidate.stance
    shoulder_left = cx - candidate.shoulder_span
    shoulder_right = cx + candidate.shoulder_span
    shoulder_y = 176 if candidate.code == "A" else 164 if candidate.code == "B" else 154
    head_w = int(116 * candidate.head_scale)
    head_h = int(108 * candidate.head_scale)
    head_top = 49 if candidate.code == "A" else 43 if candidate.code == "B" else 37
    head_bottom = head_top + head_h

    # Rear C-frame shoulders: one large silhouette anchor, no panel-line noise.
    for sx in (shoulder_left, shoulder_right):
        rounded(
            draw,
            (sx - candidate.shoulder_radius, shoulder_y - candidate.shoulder_radius,
             sx + candidate.shoulder_radius, shoulder_y + candidate.shoulder_radius),
            candidate.shoulder_radius // 2,
            NAVY,
            width=7,
        )
        rounded(
            draw,
            (sx - candidate.shoulder_radius + 19, shoulder_y - candidate.shoulder_radius + 18,
             sx + candidate.shoulder_radius - 18, shoulder_y + candidate.shoulder_radius - 14),
            max(8, candidate.shoulder_radius // 3),
            INK_SHADOW,
            width=4,
            outline=NAVY_LIGHT,
        )

    # Legs and feet.
    for lx, mirror in ((left_x, -1), (right_x, 1)):
        polygon(
            draw,
            ((lx - 37, candidate.hip_y), (lx + 31, candidate.hip_y),
             (lx + 27, candidate.knee_y - 24), (lx - 31, candidate.knee_y - 17)),
            IVORY,
            width=5,
        )
        rounded(draw, (lx - 34, candidate.knee_y - 30, lx + 34, candidate.knee_y + 28), 20, NAVY_LIGHT, width=5)
        draw.ellipse((lx - 12, candidate.knee_y - 8, lx + 12, candidate.knee_y + 16), fill=GOLD, outline=INK, width=4)
        polygon(
            draw,
            ((lx - 40, candidate.knee_y + 10), (lx + 37, candidate.knee_y + 8),
             (lx + 42, candidate.foot_y - 28), (lx - 44, candidate.foot_y - 22)),
            NAVY,
            width=6,
        )
        shadow_x = lx + 6 * mirror
        draw.polygon(
            ((shadow_x, candidate.knee_y + 18), (lx + 36 * mirror, candidate.knee_y + 14),
             (lx + 40 * mirror, candidate.foot_y - 30), (shadow_x, candidate.foot_y - 27)),
            fill=NAVY_LIGHT,
        )
        foot_box = (lx - 49, candidate.foot_y - 30, lx + 49, candidate.foot_y + 5)
        rounded(draw, foot_box, 13, NAVY, width=6)
        toe_x0 = lx - 18 if mirror < 0 else lx - 2
        toe_x1 = lx + 2 if mirror < 0 else lx + 18
        draw.rectangle((toe_x0, candidate.foot_y - 27, toe_x1, candidate.foot_y + 1), fill=IVORY, outline=INK, width=3)

    # Hip block and center identity light.
    polygon(
        draw,
        ((cx - 92, candidate.torso_bottom - 20), (cx + 92, candidate.torso_bottom - 20),
         (cx + 78, candidate.hip_y + 29), (cx - 78, candidate.hip_y + 29)),
        NAVY,
        width=6,
    )
    rounded(draw, (cx - 23, candidate.torso_bottom - 2, cx + 23, candidate.hip_y + 27), 9, INK_SHADOW, width=4)
    draw.rectangle((cx - 8, candidate.torso_bottom + 6, cx + 8, candidate.hip_y + 19), fill=GOLD)

    # Red chest/shoulder-front structure reads as one X-like mass.
    chest_top = max(head_bottom + 7, shoulder_y - 28)
    polygon(
        draw,
        ((cx - 8, chest_top + 16), (cx - 94, chest_top - 8), (cx - 127, shoulder_y + 29),
         (cx - 102, candidate.torso_bottom - 14), (cx - 30, candidate.torso_bottom + 6),
         (cx - 9, candidate.torso_bottom - 36)),
        RED,
        width=7,
    )
    polygon(
        draw,
        ((cx + 8, chest_top + 16), (cx + 94, chest_top - 8), (cx + 127, shoulder_y + 29),
         (cx + 102, candidate.torso_bottom - 14), (cx + 30, candidate.torso_bottom + 6),
         (cx + 9, candidate.torso_bottom - 36)),
        RED,
        width=7,
    )
    draw.polygon(
        ((cx + 10, chest_top + 21), (cx + 91, chest_top), (cx + 116, shoulder_y + 31),
         (cx + 89, candidate.torso_bottom - 24), (cx + 31, candidate.torso_bottom - 4)),
        fill=RED_SHADOW,
    )
    rounded(draw, (cx - 21, chest_top + 5, cx + 21, candidate.torso_bottom - 25), 8, IVORY, width=5)
    draw.ellipse((cx - 17, shoulder_y + 34, cx + 17, shoulder_y + 68), fill=GOLD, outline=INK, width=5)

    # Upper arms and intact original cylindrical forearms.
    for ax, mirror in ((shoulder_left, -1), (shoulder_right, 1)):
        polygon(
            draw,
            ((ax - 34, shoulder_y + 18), (ax + 34, shoulder_y + 18),
             (ax + 28, candidate.forearm_top + 25), (ax - 29, candidate.forearm_top + 25)),
            RED if mirror < 0 else RED_SHADOW,
            width=5,
        )
        fw = candidate.forearm_width
        rounded(
            draw,
            (ax - fw // 2, candidate.forearm_top, ax + fw // 2, candidate.forearm_bottom),
            fw // 3,
            NAVY,
            width=6,
        )
        draw.rectangle((ax - fw // 2 + 4, candidate.forearm_top + 12, ax - 2, candidate.forearm_bottom - 12), fill=NAVY_LIGHT)
        draw.rectangle((ax - fw // 2 - 1, candidate.forearm_top + 7, ax + fw // 2 + 1, candidate.forearm_top + 22), fill=SILVER, outline=INK, width=4)
        draw.rectangle((ax - fw // 2 - 1, candidate.forearm_bottom - 24, ax + fw // 2 + 1, candidate.forearm_bottom - 7), fill=SILVER, outline=INK, width=4)
        rounded(draw, (ax - 29, candidate.forearm_bottom - 5, ax + 29, candidate.forearm_bottom + 42), 18, INK_SHADOW, width=5)
        for offset in (-17, -6, 6, 17):
            draw.line((ax + offset, candidate.forearm_bottom + 5, ax + offset, candidate.forearm_bottom + 28), fill=SILVER, width=3)

    # E02 right-shoulder old injury: visible but no missing armor or replacement arm.
    injury_x = shoulder_left
    draw.line((injury_x - 37, shoulder_y - 26, injury_x + 2, shoulder_y + 4), fill=IVORY, width=8)
    draw.line((injury_x - 22, shoulder_y - 31, injury_x + 15, shoulder_y - 4), fill=INK_SHADOW, width=3)

    # Head and face identity are drawn last to dominate the small-size read.
    hx0, hx1 = cx - head_w // 2, cx + head_w // 2
    polygon(
        draw,
        ((hx0 + 13, head_top + 25), (cx - 24, head_top), (cx + 25, head_top),
         (hx1 - 12, head_top + 25), (hx1, head_bottom - 28),
         (cx + 34, head_bottom + 4), (cx - 34, head_bottom + 4), (hx0, head_bottom - 28)),
        NAVY,
        width=7,
    )
    polygon(
        draw,
        ((cx - 18, head_top + 3), (cx + 18, head_top + 3),
         (cx + 25, head_top + 58), (cx, head_top + 76), (cx - 25, head_top + 58)),
        RED,
        width=4,
    )
    horn_y = head_top + 45
    polygon(draw, ((cx - 16, horn_y), (cx - 78, horn_y - 20), (cx - 36, horn_y + 18)), GOLD, width=4)
    polygon(draw, ((cx + 16, horn_y), (cx + 78, horn_y - 20), (cx + 36, horn_y + 18)), GOLD, width=4)
    draw.polygon(((cx - 38, head_top + 66), (cx - 7, head_top + 60), (cx - 16, head_top + 79), (cx - 42, head_top + 82)), fill=GOLD, outline=INK)
    draw.polygon(((cx + 38, head_top + 66), (cx + 7, head_top + 60), (cx + 16, head_top + 79), (cx + 42, head_top + 82)), fill=GOLD, outline=INK)
    polygon(
        draw,
        ((cx - 33, head_top + 78), (cx + 33, head_top + 78),
         (cx + 28, head_bottom + 2), (cx, head_bottom + 17), (cx - 28, head_bottom + 2)),
        IVORY,
        width=5,
    )
    for x in (cx - 15, cx, cx + 15):
        draw.line((x, head_top + 88, x, head_bottom + 2), fill=INK_SHADOW, width=4)
    draw.ellipse((cx - 61, head_top + 68, cx - 45, head_top + 85), fill=GOLD, outline=INK, width=3)
    draw.ellipse((cx + 45, head_top + 68, cx + 61, head_top + 85), fill=GOLD, outline=INK, width=3)

    return image


def native_sprite(candidate: Candidate, size: int) -> Image.Image:
    return draw_guardian_qsd(candidate).resize((size, size), Image.Resampling.LANCZOS)


def board_text(draw: ImageDraw.ImageDraw, xy, value: str, size: int, color=INK, *, bold=False, anchor=None) -> None:
    draw.text(xy, value, font=font(size, bold=bold), fill=color, anchor=anchor)


def wrap_text(draw: ImageDraw.ImageDraw, box, value: str, size: int, color=INK, *, bold=False, spacing=6) -> None:
    x0, y0, x1, y1 = box
    current = ""
    lines: list[str] = []
    for char in value:
        trial = current + char
        if draw.textbbox((0, 0), trial, font=font(size, bold=bold))[2] > x1 - x0 and current:
            lines.append(current)
            current = char
        else:
            current = trial
    if current:
        lines.append(current)
    draw.multiline_text((x0, y0), "\n".join(lines), font=font(size, bold=bold), fill=color, spacing=spacing)


def rounded_panel(draw: ImageDraw.ImageDraw, box, fill, outline, *, width=2, radius=7) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def fit_crop(image: Image.Image, box, crop) -> Image.Image:
    x0, y0, x1, y1 = box
    source = image.crop(crop)
    return ImageOps.fit(source, (x1 - x0, y1 - y0), method=Image.Resampling.LANCZOS)


def draw_footprint(draw: ImageDraw.ImageDraw, origin: tuple[int, int], sprite: Image.Image) -> None:
    ox, oy = origin
    cells = ((0, 0), (1, 0), (0, 1), (1, 1))
    for x, y in cells:
        cx = ox + (x - y) * 42
        cy = oy + (x + y) * 22
        points = ((cx, cy - 22), (cx + 42, cy), (cx, cy + 22), (cx - 42, cy))
        draw.polygon(points, fill="#dce5e8", outline="#758895")
    px = ox - sprite.width // 2
    py = oy + 47 - sprite.height
    draw._image.alpha_composite(sprite, (px, py))
    draw.ellipse((ox - 5, oy + 41, ox + 5, oy + 51), fill=RED, outline=INK, width=2)


def generate_board(cml_image: Image.Image, v10x_image: Image.Image, sprites: dict[tuple[str, int], Image.Image]) -> Path:
    board = Image.new("RGBA", (1920, 1080), PAPER)
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 1920, 92), fill=INK)
    board_text(draw, (34, 24), "C01E02 G1.5-A1｜馆守 Z Q/SD 战棋地图造型方向判断板", 30, "#ffffff", bold=True)
    board_text(draw, (1886, 30), "Candidate / runtime_allowed=false", 18, "#f2c45f", anchor="ra")

    # Frozen identity sources.
    rounded_panel(draw, (24, 112, 372, 1054), PAPER_LIGHT, NAVY_LIGHT, width=3)
    board_text(draw, (46, 132), "身份锚（只读）", 23, NAVY, bold=True)
    board.alpha_composite(fit_crop(cml_image, (46, 174, 350, 391), (260, 0, 1080, 650)), (46, 174))
    board_text(draw, (54, 401), "CML008 / Hard 当前身份锚", 16, RED_SHADOW, bold=True)
    board.alpha_composite(fit_crop(v10x_image, (46, 438, 350, 671), (105, 0, 920, 820)), (46, 438))
    board_text(draw, (54, 681), "V10X / E02 完整双前臂候选", 16, NAVY, bold=True)
    board_text(draw, (46, 730), "四个不可丢的识别点", 19, INK, bold=True)
    anchor_rows = (
        ("01", "金色横向头冠 + 红色中脊"),
        ("02", "金眼与银白格栅脸谱"),
        ("03", "红胸甲延续到肩前甲"),
        ("04", "双圆柱前臂完整；右肩旧伤"),
    )
    y = 770
    for number, label in anchor_rows:
        draw.ellipse((46, y - 2, 76, y + 28), fill=RED, outline=INK, width=2)
        board_text(draw, (61, y + 12), number, 12, "#ffffff", bold=True, anchor="mm")
        board_text(draw, (88, y), label, 15, INK, bold=True)
        y += 50
    board_text(draw, (46, 979), "禁止：飞翼 / 背包 / 火箭拳 / 缺臂 / 巡展臂", 14, RED_SHADOW, bold=True)
    board_text(draw, (46, 1010), "常态 A / KINETIC_CEL：大色块、两级硬阴影、无碎贴纸", 13, MUTED)

    panel_x = (390, 900, 1410)
    accents = (RED, TEAL, GOLD)
    for candidate, x0, accent in zip(CANDIDATES, panel_x, accents):
        x1 = x0 + 490
        rounded_panel(draw, (x0, 112, x1, 1054), PAPER_LIGHT, accent, width=3)
        board_text(draw, (x0 + 22, 132), f"{candidate.code}｜{candidate.title}", 24, INK, bold=True)
        board_text(draw, (x1 - 20, 137), candidate.ratio, 16, accent, bold=True, anchor="ra")

        main = draw_guardian_qsd(candidate).resize((354, 354), Image.Resampling.LANCZOS)
        board.alpha_composite(main, (x0 + 68, 176))
        draw.line((x0 + 48, 530, x1 - 48, 530), fill="#c5ced3", width=2)

        board_text(draw, (x0 + 24, 548), "识别点复核", 16, NAVY, bold=True)
        chips = (("冠/脸", GOLD), ("红胸肩", RED), ("双圆柱臂", NAVY_LIGHT), ("右肩旧伤", IVORY))
        chip_x = x0 + 24
        for label, color in chips:
            width = 100 if label != "双圆柱臂" else 116
            rounded_panel(draw, (chip_x, 578, chip_x + width, 612), "#ffffff", color, width=2, radius=5)
            board_text(draw, (chip_x + width // 2, 595), label, 13, INK, bold=True, anchor="mm")
            chip_x += width + 8

        board_text(draw, (x0 + 24, 638), "原生显示尺寸（1:1）", 16, NAVY, bold=True)
        rounded_panel(draw, (x0 + 24, 668, x0 + 198, 810), "#e3e8ea", "#abb6bc", width=1)
        rounded_panel(draw, (x0 + 214, 668, x0 + 466, 810), "#e3e8ea", "#abb6bc", width=1)
        board.alpha_composite(sprites[(candidate.code, 96)], (x0 + 63, 701))
        board.alpha_composite(sprites[(candidate.code, 128)], (x0 + 276, 678))
        board_text(draw, (x0 + 111, 789), "96 px", 13, INK, bold=True, anchor="mm")
        board_text(draw, (x0 + 340, 789), "128 px", 13, INK, bold=True, anchor="mm")

        board_text(draw, (x0 + 24, 830), "2×2 footprint / 脚底中心 pivot", 15, NAVY, bold=True)
        draw_footprint(draw, (x0 + 247, 916), sprites[(candidate.code, 96)])
        board_text(draw, (x0 + 24, 966), candidate.strength, 14, INK, bold=True)
        wrap_text(draw, (x0 + 24, 994, x1 - 20, 1040), candidate.tradeoff, 13, MUTED)

    path = OUT / "GZ_QSD_A1_direction_board_1920x1080.png"
    board.convert("RGB").save(path)
    return path


def write_source_receipt(rows: dict[str, dict[str, str]], manifest_sha: str) -> Path:
    path = OUT / "source-validation-receipt.tsv"
    fields = (
        "input_id", "authority_role", "contract_commit_or_snapshot", "source_path",
        "expected_sha256", "actual_sha256", "validation", "runtime_allowed",
    )
    receipt_rows = [
        {
            "input_id": "G15_A1_CONTRACT",
            "authority_role": "unique_authority_contract",
            "contract_commit_or_snapshot": CONTRACT_COMMIT,
            "source_path": CONTRACT_PATH,
            "expected_sha256": CONTRACT_SHA256,
            "actual_sha256": CONTRACT_SHA256,
            "validation": f"match;git_blob={CONTRACT_BLOB}",
            "runtime_allowed": "false",
        },
        {
            "input_id": "G15_A1_FROZEN_VISUAL_MANIFEST",
            "authority_role": "seven_input_frozen_manifest",
            "contract_commit_or_snapshot": FROZEN_SNAPSHOT,
            "source_path": VISUAL_MANIFEST_PATH,
            "expected_sha256": manifest_sha,
            "actual_sha256": manifest_sha,
            "validation": f"match;content_fingerprint={CONTENT_FINGERPRINT}",
            "runtime_allowed": "false",
        },
    ]
    for visual_id in ("VIS_CML008_CURRENT_BASE", "VIS_GUARDIAN_Z_V10X"):
        row = rows[visual_id]
        receipt_rows.append(
            {
                "input_id": visual_id,
                "authority_role": row["lifecycle_or_role"],
                "contract_commit_or_snapshot": row["snapshot_ref_or_contract_version"],
                "source_path": row["path"],
                "expected_sha256": row["sha256"],
                "actual_sha256": row["sha256"],
                "validation": "match_from_contract_commit",
                "runtime_allowed": "false",
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(receipt_rows)
    return path


def write_manifest(board: Path, sprite_paths: dict[tuple[str, int], Path], receipt: Path) -> tuple[Path, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    rows.append(
        {
            "asset_id": "G15_A1_GZ_QSD_DIRECTION_BOARD",
            "path": board.name,
            "type": "png",
            "dimensions_or_format": "1920x1080",
            "source_visual_ids": "VIS_CML008_CURRENT_BASE;VIS_GUARDIAN_Z_V10X",
            "parent_slot": "MECHA_C01CDV1_GUARDIAN_Z",
            "lifecycle": "candidate_direction_board",
            "status": "awaiting_individual_user_decision",
            "runtime_allowed": "false",
            "notes": "A1 only; three controlled proportion candidates; E02 intact original both forearms",
        }
    )
    for candidate in CANDIDATES:
        for size in (96, 128):
            sprite = sprite_paths[(candidate.code, size)]
            rows.append(
                {
                    "asset_id": f"{candidate.stable_id}_{size}",
                    "path": sprite.name,
                    "type": "png_rgba",
                    "dimensions_or_format": f"{size}x{size}",
                    "source_visual_ids": "VIS_CML008_CURRENT_BASE;VIS_GUARDIAN_Z_V10X",
                    "parent_slot": "MECHA_C01CDV1_GUARDIAN_Z",
                    "lifecycle": "candidate_qsd_scale_sample",
                    "status": "direction_sample_not_sprite_master",
                    "runtime_allowed": "false",
                    "notes": f"candidate {candidate.code}; native scale sample; foot-center pivot; no animation",
                }
            )
    rows.extend(
        [
            {
                "asset_id": "G15_A1_SOURCE_VALIDATION_RECEIPT",
                "path": receipt.name,
                "type": "tsv",
                "dimensions_or_format": "n/a",
                "source_visual_ids": "09b_guardian_z_pair;contract_15",
                "parent_slot": "G15_A1_AUTHORITY",
                "lifecycle": "validation_evidence",
                "status": "complete",
                "runtime_allowed": "false",
                "notes": "contract, snapshot, fingerprint and two frozen visual hashes",
            },
            {
                "asset_id": "G15_A1_GENERATOR_SOURCE",
                "path": Path(__file__).name,
                "type": "python",
                "dimensions_or_format": "n/a",
                "source_visual_ids": "09b_guardian_z_pair;contract_15",
                "parent_slot": "G15_A1_REPRODUCIBILITY",
                "lifecycle": "reproducibility_evidence",
                "status": "complete",
                "runtime_allowed": "false",
                "notes": "procedural controlled candidates; no ImageGen or LibTV",
            },
        ]
    )
    fields = (
        "asset_id", "path", "type", "dimensions_or_format", "source_visual_ids", "parent_slot",
        "lifecycle", "status", "sha256", "runtime_allowed", "notes",
    )
    path = OUT / "asset-manifest.tsv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            item = dict(row)
            item["sha256"] = sha256_file(OUT / item["path"])
            writer.writerow(item)
    return path, rows


def write_completion_report(manifest: Path, rows: list[dict[str, str]]) -> Path:
    path = OUT / "completion-report.md"
    report = f"""# C01E02 G1.5-A1 馆守 Z Q/SD 方向板交付

> Status: `candidate_direction_board_complete / awaiting_individual_user_decision`
>
> Runtime: `runtime_allowed=false`

## 权威记录

- 合同提交：`{CONTRACT_COMMIT}`
- 合同 Git blob：`{CONTRACT_BLOB}`
- 合同 SHA-256：`{CONTRACT_SHA256}`
- 冻结截面：`{FROZEN_SNAPSHOT}`
- Content fingerprint：`{CONTENT_FINGERPRINT}`
- 身份关系：`CML008 = Hard/Current identity anchor`；`V10X = E02 intact-both-forearms Candidate Previs`

## A1 交付

- 方向板：`{board_name()}`
- 原生尺寸样张：A/B/C 各 `96×96` 与 `128×128`，均为透明 Candidate 样张，不是 Sprite 母版。
- Manifest：`{manifest.name}`，共 `{len(rows)}` 行；全部 `runtime_allowed=false`。

## 三个候选

- **A 重装图标型**：最像老派重型主角机，96 px 识别最好；动作幅度最受限。
- **B 均衡守卫型**：身份、格上可读和动作扩展最均衡；建议优先细化。
- **C 动作骨架型**：移动与推击扩展最好；小尺寸下厚重感最弱。

三案都保留金色头冠、银白脸谱、红胸肩连续面、双圆柱原装前臂和右肩旧伤；都没有飞翼、背包、火箭拳、缺臂或巡展臂。

## 边界

- 只写 `art-g1-5/**`；未覆盖 `art-g1/**`。
- 未写 Godot、Canon 或 Runtime，未生成动画、BREAKER、重盾或 Cut-in。
- 未调用 ImageGen、LibTV 或任何付费/批量生成。
- 自动检查只证明来源、尺寸和生命周期正确，不代表用户批准。

## 用户门

请逐项给出：`方向通过，可继续细化`、`需要修改`、`仅参考，不进入 Demo`，或 `批准作为 Demo 派生来源，等待制作人交接`。在明确批准前，本任务停止，不继续 B1 或其他资产。
"""
    path.write_text(report, encoding="utf-8")
    return path


def board_name() -> str:
    return "GZ_QSD_A1_direction_board_1920x1080.png"


def write_delivery_hashes() -> Path:
    path = OUT / "delivery-hashes.sha256"
    lines = []
    for item in sorted(OUT.iterdir(), key=lambda value: value.name):
        if item.is_file() and item.name != path.name and not item.name.startswith("."):
            lines.append(f"{sha256_file(item)}  {item.name}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    rows, source_bytes, manifest_sha = validate_authority()
    cml_image = Image.open(io.BytesIO(source_bytes["VIS_CML008_CURRENT_BASE"])).convert("RGBA")
    v10x_image = Image.open(io.BytesIO(source_bytes["VIS_GUARDIAN_Z_V10X"])).convert("RGBA")

    sprites: dict[tuple[str, int], Image.Image] = {}
    sprite_paths: dict[tuple[str, int], Path] = {}
    for candidate in CANDIDATES:
        for size in (96, 128):
            image = native_sprite(candidate, size)
            path = OUT / f"GZ_QSD_A1_candidate_{candidate.code}_{size}.png"
            image.save(path)
            sprites[(candidate.code, size)] = image
            sprite_paths[(candidate.code, size)] = path

    board = generate_board(cml_image, v10x_image, sprites)
    receipt = write_source_receipt(rows, manifest_sha)
    manifest, manifest_rows = write_manifest(board, sprite_paths, receipt)
    report = write_completion_report(manifest, manifest_rows)
    hashes = write_delivery_hashes()

    print(f"Generated {board.name}")
    print(f"Manifest rows: {len(manifest_rows)}")
    print(f"Completion report: {report.name}")
    print(f"Delivery hashes: {hashes.name}")
    print(f"Contract SHA-256: {CONTRACT_SHA256}")
    print(f"Frozen snapshot: {FROZEN_SNAPSHOT}")
    print(f"Content fingerprint: {CONTENT_FINGERPRINT}")


if __name__ == "__main__":
    main()
