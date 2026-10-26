#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import math
from collections import deque
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in (HERE, *HERE.parents) if (parent / ".git").exists())
PACKAGE_ID = "C01CDV1_A8_PHASE_B0_B1_V1"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"

BG = "#07151c"
PANEL = "#10242c"
PANEL_2 = "#152d35"
LINE = "#426b73"
TEXT = "#e8efec"
MUTED = "#99aaa8"
CYAN = "#68c8c3"
GOLD = "#e4b94b"
CORAL = "#ef6458"
INK = "#07131b"
NAVY = "#102e4b"
NAVY_LIGHT = "#244b6b"
RED = "#d74b42"
RED_DARK = "#842d34"
IVORY = "#e8ebe5"
STEEL = "#84959a"
GRAPHITE = "#26343c"
OLIVE = "#596b61"
AMBER = "#f0b84d"


SOURCES = [
    (
        "SRC_52_DISPATCH",
        "docs/superpowers/specs/production/c01-current-demo-v1/52-c01e02-a8-v10x-scoped-user-decision-and-phase-b-dispatch.md",
        "d65c85e4a9778e84cb4356dcd6ced40269d474ec064c7562e8b0deb414c9ad38",
        "sole_phase_dispatch_and_user_scope",
    ),
    (
        "SRC_GZ_V10X",
        "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png",
        "e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade",
        "guardian_z_e02_naked_candidate_derivation_parent",
    ),
    (
        "SRC_GZ_A1_C_128",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png",
        "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e",
        "guardian_z_approved_action_skeleton",
    ),
    (
        "SRC_GZ_A1_RECEIPT",
        "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv",
        "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee",
        "guardian_z_action_direction_user_receipt",
    ),
    (
        "SRC_BREAKER_B_IDENTITY",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png",
        "7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868",
        "breaker_b_forelimb_bearer_identity",
    ),
    (
        "SRC_BREAKER_X_SURFACE",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png",
        "cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85",
        "breaker_x_bio_armor_and_closed_relation",
    ),
    (
        "SRC_BREAKER_RECEIPT",
        "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv",
        "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920",
        "breaker_b_x_user_receipt",
    ),
    (
        "SRC_SHIELD_A_STATES",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b2-retired-shield/RETIRED_SHIELD_B2_candidate_A_four_state_sheet_1800x1200.png",
        "e3d3cb2f736d3fd6bfd972553d8336773530412d695db6153b2a8d3b45015fc5",
        "shield_a_tower_shape_and_three_old_scars",
    ),
    (
        "SRC_SHIELD_F_SURFACE",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b2-retired-shield/RETIRED_SHIELD_B2_surface_language_board_1800x1050.png",
        "097002a8b4fd7efd2e4713f4263bb47e99b91bc090da21d72238c9add8af8151",
        "shield_f_d70_p30_surface_ratio",
    ),
    (
        "SRC_SHIELD_RECEIPT",
        "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b2-user-approval-receipt.tsv",
        "792d9061b804ec3d87d79c777171f5aa4bd44979416c40d45d8968a2004d0c51",
        "shield_a_f_user_receipt",
    ),
    (
        "SRC_A4_BASE",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_BASE_2400x1350.png",
        "6fd40a256afee225457594558edf274823de5d1e771d1f570d0263c5df217789",
        "a4_static_base_read_only",
    ),
    (
        "SRC_A4_BUILDINGS",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_BUILDINGS_2400x1350.png",
        "db3f83eeb3ed5e583d0a831a203ab0d5446a594f9ed9e34f25f175f290f62237",
        "a4_static_buildings_read_only",
    ),
    (
        "SRC_A4_ROOFS",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_ROOFS_2400x1350.png",
        "7fea3c7918ff85bb1d5df1f4bcc5856afac1d8fa7f174d59b862f985962f11a9",
        "a4_static_roofs_read_only",
    ),
    (
        "SRC_A4_FOREGROUND",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_FOREGROUND_2400x1350.png",
        "454b3cf845ba91d7d7f13e201874bbbe79f871297a36930a24348823df1525a3",
        "a4_static_foreground_read_only",
    ),
    (
        "SRC_A4_OCCLUSION_MASK",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_OCCLUSION_MASK_2400x1350.png",
        "b5f68f4749f6bff2025409622888d8e8faa17d977aca372caa43121eec18e899",
        "a4_static_occlusion_control_read_only",
    ),
    (
        "SRC_A4_RESCUE_ACTIVE",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_STATE_RESCUE_ACTIVE_2400x1350.png",
        "05833205230b087b3024545a1344174fb1a73c7975087fcf06808d62b01d3ff1",
        "a4_state_overlay_active_wall_hung_read_only",
    ),
    (
        "SRC_A4_TOPOLOGY",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/topology-lock-receipt.tsv",
        "1763883a84f5bfccfbb3add981f26044a5fca785fab1c22398355eee885eecb4",
        "a4_initial_entity_anchors",
    ),
    (
        "SRC_A5_SWARM_96",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png",
        "1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b",
        "a5_approved_small_swarm_read_only_overlay",
    ),
    (
        "SRC_T3_JOINT_STATE",
        "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-joint/joint-readonly-review.md",
        "b9df31e85752d6ba9532c4772aa78bbe83e47200019781561af0d278655f9866",
        "t3_joint_calibrated_positions_and_facing",
    ),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def source_path(source_id: str) -> Path:
    row = next(row for row in SOURCES if row[0] == source_id)
    return ROOT / row[1]


def validate_sources() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path_text, expected, role in SOURCES:
        path = ROOT / path_text
        if not path.is_file():
            raise RuntimeError(f"missing source: {path_text}")
        actual = sha256(path)
        result = "match" if actual == expected else "mismatch"
        rows.append(
            {
                "source_id": source_id,
                "path": path_text,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "role": role,
                "result": result,
                "runtime_allowed": "false",
            }
        )
        if result != "match":
            raise RuntimeError(f"source drift: {path_text}: expected={expected} actual={actual}")
    return rows


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def write_tsv(path: Path, rows: Iterable[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def connected_white_to_alpha(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    background = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def candidate(x: int, y: int) -> bool:
        r, g, b = pixels[x, y]
        return min(r, g, b) >= 238 and max(r, g, b) - min(r, g, b) <= 18

    def push(x: int, y: int) -> None:
        index = y * width + x
        if not visited[index] and candidate(x, y):
            visited[index] = 1
            queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        background[y * width + x] = 1
        if x:
            push(x - 1, y)
        if x + 1 < width:
            push(x + 1, y)
        if y:
            push(x, y - 1)
        if y + 1 < height:
            push(x, y + 1)

    mask = Image.new("L", (width, height), 255)
    mask_pixels = mask.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if background[row + x]:
                mask_pixels[x, y] = 0
    mask = mask.filter(ImageFilter.GaussianBlur(0.55))
    result = rgb.convert("RGBA")
    result.putalpha(mask)
    return result


def contain(image: Image.Image, box: tuple[int, int, int, int]) -> tuple[Image.Image, tuple[int, int]]:
    left, top, right, bottom = box
    work = image.copy()
    work.thumbnail((right - left, bottom - top), Image.Resampling.LANCZOS)
    return work, (left + (right - left - work.width) // 2, top + (bottom - top - work.height) // 2)


def glow_circle(size: tuple[int, int], center: tuple[int, int], radius: int, color: tuple[int, int, int]) -> Image.Image:
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for step in range(radius, 0, -2):
        alpha = round(95 * (1 - step / max(radius, 1)) ** 1.4)
        draw.ellipse(
            (center[0] - step, center[1] - step, center[0] + step, center[1] + step),
            fill=(*color, alpha),
        )
    return layer.filter(ImageFilter.GaussianBlur(3))


def make_old_guardian_states(outputs: dict[str, Path]) -> list[Image.Image]:
    source = Image.open(source_path("SRC_GZ_V10X")).convert("RGB")
    cutout = connected_white_to_alpha(source)
    bbox = cutout.getbbox()
    if bbox is None:
        raise RuntimeError("V10X cutout is empty")
    cutout = cutout.crop(bbox)
    bust = cutout.crop((0, 0, cutout.width, round(cutout.height * 0.61)))

    states = [
        ("guide", CYAN, 0, 1.00, 36, 2),
        ("contact", CORAL, -4, 1.035, 58, 4),
        ("shield_gaze", GOLD, 22, 1.01, 48, 3),
    ]
    frames: list[Image.Image] = []
    layer_root = HERE / "source-layers" / "old_guardian_v10x"
    layer_root.mkdir(parents=True, exist_ok=True)

    for state, accent_hex, shift_x, scale, wave_radius, wave_count in states:
        accent = tuple(int(accent_hex[index:index + 2], 16) for index in (1, 3, 5))
        body_layer = Image.new("RGBA", (1024, 768), (0, 0, 0, 0))
        target = bust.resize((round(bust.width * scale), round(bust.height * scale)), Image.Resampling.LANCZOS)
        target, position = contain(target, (80 + shift_x, 36, 944 + shift_x, 710))
        body_layer.alpha_composite(target, position)

        light_layer = glow_circle((1024, 768), (512 + shift_x, 420), 72 if state == "contact" else 54, accent)
        light_draw = ImageDraw.Draw(light_layer)
        light_draw.ellipse((497 + shift_x, 405, 527 + shift_x, 435), fill=(*accent, 238), outline=(250, 238, 188, 255), width=3)
        light_draw.line((420 + shift_x, 230, 448 + shift_x, 234), fill=(*accent, 220), width=8)
        light_draw.line((576 + shift_x, 234, 604 + shift_x, 230), fill=(*accent, 220), width=8)

        waveform_layer = Image.new("RGBA", (1024, 768), (0, 0, 0, 0))
        wave_draw = ImageDraw.Draw(waveform_layer)
        base_y = 650
        center_x = 512 + shift_x
        for index in range(wave_count):
            radius = wave_radius + index * 24
            alpha = 210 - index * 42
            wave_draw.arc(
                (center_x - radius * 2, base_y - radius, center_x + radius * 2, base_y + radius),
                205,
                335,
                fill=(*accent, max(60, alpha)),
                width=max(3, 7 - index),
            )
        if state == "shield_gaze":
            wave_draw.line((center_x - 230, 596, center_x - 96, 628), fill=(*accent, 210), width=6)

        frame = Image.new("RGBA", (1024, 768), (0, 0, 0, 0))
        frame.alpha_composite(body_layer)
        frame.alpha_composite(light_layer)
        frame.alpha_composite(waveform_layer)
        frames.append(frame)

        state_dir = layer_root / state
        state_dir.mkdir(parents=True, exist_ok=True)
        for layer_name, layer in (("head_chest", body_layer), ("chest_light", light_layer), ("speaker_waveform", waveform_layer)):
            path = state_dir / f"{state}-{layer_name}-1024x768.png"
            layer.save(path, optimize=True)
            outputs[f"old_guardian_{state}_{layer_name}_layer"] = path
        state_path = HERE / "assets" / "comms" / "old_guardian_v10x" / f"r05-comms-old-guardian-v10x-{state}-1024x768.png"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(state_path, optimize=True)
        outputs[f"old_guardian_{state}_frame"] = state_path

    atlas = Image.new("RGBA", (3072, 768), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * 1024, 0))
    atlas_path = HERE / "assets" / "atlases" / "R05_COMMS_OLD_GUARDIAN_V10X_3072x768.png"
    atlas_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(atlas_path, optimize=True)
    outputs["old_guardian_v10x_atlas"] = atlas_path
    return frames


class HiDraw:
    def __init__(self, width: int, height: int, scale: int = 4):
        self.scale = scale
        self.image = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.width = width
        self.height = height

    def p(self, points: Iterable[tuple[float, float]]) -> list[tuple[int, int]]:
        return [(round(x * self.scale), round(y * self.scale)) for x, y in points]

    def polygon(self, points: Iterable[tuple[float, float]], fill: str, outline: str = INK, width: int = 3) -> None:
        pts = self.p(points)
        self.draw.polygon(pts, fill=fill)
        self.draw.line(pts + [pts[0]], fill=outline, width=width * self.scale, joint="curve")

    def rounded(self, box: tuple[float, float, float, float], radius: float, fill: str, outline: str = INK, width: int = 3) -> None:
        self.draw.rounded_rectangle(
            tuple(round(value * self.scale) for value in box),
            radius=round(radius * self.scale),
            fill=fill,
            outline=outline,
            width=width * self.scale,
        )

    def ellipse(self, box: tuple[float, float, float, float], fill: str, outline: str = INK, width: int = 3) -> None:
        self.draw.ellipse(
            tuple(round(value * self.scale) for value in box),
            fill=fill,
            outline=outline,
            width=width * self.scale,
        )

    def line(self, points: Iterable[tuple[float, float]], fill: str, width: int = 3) -> None:
        self.draw.line(self.p(points), fill=fill, width=width * self.scale, joint="curve")

    def finish(self) -> Image.Image:
        return self.image.resize((self.width, self.height), Image.Resampling.LANCZOS)


def baseline_align(image: Image.Image, baseline: int) -> Image.Image:
    bbox = image.getbbox()
    if bbox is None:
        raise RuntimeError("empty generated sprite")
    shift_y = baseline - (bbox[3] - 1)
    result = Image.new("RGBA", image.size, (0, 0, 0, 0))
    result.alpha_composite(image, (0, shift_y))
    alpha = result.getchannel("A")
    if baseline + 1 < result.height:
        clear = Image.new("L", result.size, 255)
        ImageDraw.Draw(clear).rectangle((0, baseline + 1, result.width, result.height), fill=0)
        alpha = ImageChops.multiply(alpha, clear)
        result.putalpha(alpha)
    return result


def draw_guardian_frame(action: str) -> Image.Image:
    pose = {
        "idle": (0, 0, -2, 2, 0, 0),
        "step_a": (-2, 0, -10, 5, 7, -5),
        "step_b": (2, 0, -5, 10, -5, 7),
        "brace": (0, 8, -16, 16, 8, 8),
        "recoil": (8, -4, -4, 5, -8, 10),
    }[action]
    cx_shift, y_shift, left_leg, right_leg, left_arm, right_arm = pose
    h = HiDraw(256, 256)

    # Legs and feet retain the long V10X lower-body read even in Q/SD translation.
    h.polygon([(72 + left_leg, 202), (111 + left_leg, 198), (118 + left_leg, 224), (69 + left_leg, 224), (64 + left_leg, 216)], NAVY)
    h.polygon([(145 + right_leg, 198), (184 + right_leg, 202), (192 + right_leg, 216), (187 + right_leg, 224), (138 + right_leg, 224)], NAVY)
    h.polygon([(78 + left_leg, 147), (111 + left_leg, 145), (115 + left_leg, 204), (72 + left_leg, 207)], NAVY_LIGHT)
    h.polygon([(145 + right_leg, 145), (178 + right_leg, 147), (184 + right_leg, 207), (141 + right_leg, 204)], NAVY_LIGHT)
    h.polygon([(89 + left_leg, 128), (115 + left_leg, 130), (111 + left_leg, 159), (82 + left_leg, 160)], IVORY)
    h.polygon([(141 + right_leg, 130), (167 + right_leg, 128), (174 + right_leg, 160), (145 + right_leg, 159)], IVORY)
    h.ellipse((99 + left_leg, 188, 116 + left_leg, 205), GRAPHITE, GOLD, 2)
    h.ellipse((140 + right_leg, 188, 157 + right_leg, 205), GRAPHITE, GOLD, 2)

    torso_x = cx_shift
    torso_y = y_shift
    h.polygon([(98 + torso_x, 122 + torso_y), (158 + torso_x, 122 + torso_y), (169 + torso_x, 145 + torso_y), (145 + torso_x, 154 + torso_y), (111 + torso_x, 154 + torso_y), (87 + torso_x, 145 + torso_y)], NAVY)
    h.polygon([(125 + torso_x, 81 + torso_y), (91 + torso_x, 74 + torso_y), (74 + torso_x, 91 + torso_y), (99 + torso_x, 123 + torso_y), (128 + torso_x, 110 + torso_y)], RED)
    h.polygon([(131 + torso_x, 81 + torso_y), (165 + torso_x, 74 + torso_y), (182 + torso_x, 91 + torso_y), (157 + torso_x, 123 + torso_y), (128 + torso_x, 110 + torso_y)], RED)
    h.polygon([(120 + torso_x, 79 + torso_y), (136 + torso_x, 79 + torso_y), (139 + torso_x, 126 + torso_y), (128 + torso_x, 139 + torso_y), (117 + torso_x, 126 + torso_y)], IVORY)
    h.ellipse((118 + torso_x, 96 + torso_y, 138 + torso_x, 116 + torso_y), AMBER, IVORY, 2)
    h.rounded((120 + torso_x, 124 + torso_y, 136 + torso_x, 145 + torso_y), 3, AMBER, INK, 2)

    # Independent navy shoulder frame, with the red shoulder-front latch visibly nested inside.
    for side in (-1, 1):
        shoulder_x = 84 + torso_x if side < 0 else 172 + torso_x
        h.ellipse((shoulder_x - 31, 63 + torso_y, shoulder_x + 31, 124 + torso_y), NAVY, INK, 4)
        h.ellipse((shoulder_x - 17, 76 + torso_y, shoulder_x + 17, 111 + torso_y), GRAPHITE, INK, 2)
        if side < 0:
            h.polygon([(57 + torso_x, 80 + torso_y), (91 + torso_x, 75 + torso_y), (105 + torso_x, 91 + torso_y), (82 + torso_x, 104 + torso_y), (59 + torso_x, 99 + torso_y)], RED)
        else:
            h.polygon([(199 + torso_x, 80 + torso_y), (165 + torso_x, 75 + torso_y), (151 + torso_x, 91 + torso_y), (174 + torso_x, 104 + torso_y), (197 + torso_x, 99 + torso_y)], RED)

    left_x = 47 + left_arm
    right_x = 174 + right_arm
    h.rounded((left_x, 102 + torso_y, left_x + 35, 174 + torso_y), 10, NAVY_LIGHT, INK, 4)
    h.rounded((right_x, 102 + torso_y, right_x + 35, 174 + torso_y), 10, NAVY_LIGHT, INK, 4)
    h.rounded((left_x - 2, 99 + torso_y, left_x + 37, 115 + torso_y), 6, IVORY, INK, 3)
    h.rounded((right_x - 2, 99 + torso_y, right_x + 37, 115 + torso_y), 6, IVORY, INK, 3)
    h.polygon([(left_x, 124 + torso_y), (left_x + 13, 118 + torso_y), (left_x + 13, 159 + torso_y), (left_x, 165 + torso_y)], RED_DARK)
    h.polygon([(right_x + 35, 124 + torso_y), (right_x + 22, 118 + torso_y), (right_x + 22, 159 + torso_y), (right_x + 35, 165 + torso_y)], RED_DARK)
    h.rounded((left_x + 7, 168 + torso_y, left_x + 30, 185 + torso_y), 6, GRAPHITE, INK, 3)
    h.rounded((right_x + 5, 168 + torso_y, right_x + 28, 185 + torso_y), 6, GRAPHITE, INK, 3)

    head_x = torso_x + (5 if action == "recoil" else 0)
    h.polygon([(106 + head_x, 42 + torso_y), (116 + head_x, 31 + torso_y), (140 + head_x, 31 + torso_y), (150 + head_x, 42 + torso_y), (146 + head_x, 72 + torso_y), (110 + head_x, 72 + torso_y)], NAVY)
    h.polygon([(122 + head_x, 28 + torso_y), (134 + head_x, 28 + torso_y), (139 + head_x, 51 + torso_y), (128 + head_x, 57 + torso_y), (117 + head_x, 51 + torso_y)], RED)
    h.polygon([(105 + head_x, 45 + torso_y), (77 + head_x, 35 + torso_y), (101 + head_x, 59 + torso_y), (123 + head_x, 54 + torso_y)], GOLD)
    h.polygon([(151 + head_x, 45 + torso_y), (179 + head_x, 35 + torso_y), (155 + head_x, 59 + torso_y), (133 + head_x, 54 + torso_y)], GOLD)
    h.line([(111 + head_x, 56 + torso_y), (121 + head_x, 54 + torso_y)], AMBER, 4)
    h.line([(135 + head_x, 54 + torso_y), (145 + head_x, 56 + torso_y)], AMBER, 4)
    h.polygon([(115 + head_x, 59 + torso_y), (141 + head_x, 59 + torso_y), (138 + head_x, 76 + torso_y), (118 + head_x, 76 + torso_y)], IVORY)
    for x in (122, 128, 134):
        h.line([(x + head_x, 62 + torso_y), (x + head_x, 72 + torso_y)], GRAPHITE, 2)

    return baseline_align(h.finish(), 225)


def draw_breaker_frame(action: str) -> Image.Image:
    params = {
        "idle": (0, 0, 0, 0, 4),
        "charge": (0, 15, -10, 10, 9),
        "contact": (0, 22, -22, 22, 13),
    }[action]
    x_shift, y_shift, left_spread, right_spread, seam_width = params
    h = HiDraw(320, 320)

    # Hind support first; the front limbs remain the dominant weight-bearing pair.
    h.polygon([(117, 191 + y_shift), (145, 190 + y_shift), (142, 281), (111, 281), (104, 256)], GRAPHITE)
    h.polygon([(175, 190 + y_shift), (203, 191 + y_shift), (216, 256), (209, 281), (178, 281)], GRAPHITE)
    h.rounded((106, 270, 146, 288), 7, "#17242b", INK, 4)
    h.rounded((174, 270, 214, 288), 7, "#17242b", INK, 4)

    left_x = 48 + left_spread
    right_x = 223 + right_spread
    h.polygon([(78, 145 + y_shift), (110, 159 + y_shift), (88 + left_spread, 244), (56 + left_spread, 275), (36 + left_spread, 258), (52 + left_spread, 199)], "#1c2a31")
    h.polygon([(242, 145 + y_shift), (210, 159 + y_shift), (232 + right_spread, 244), (264 + right_spread, 275), (284 + right_spread, 258), (268 + right_spread, 199)], "#1c2a31")
    h.polygon([(42 + left_spread, 260), (20 + left_spread, 280), (53 + left_spread, 274), (38 + left_spread, 293), (68 + left_spread, 276)], "#a0aaac", INK, 2)
    h.polygon([(278 + right_spread, 260), (300 + right_spread, 280), (267 + right_spread, 274), (282 + right_spread, 293), (252 + right_spread, 276)], "#a0aaac", INK, 2)

    # Giant shell, curved segment seams, and sealed upper-back outlet.
    h.polygon([(52, 139 + y_shift), (74, 90 + y_shift), (118, 55 + y_shift), (205, 48 + y_shift), (264, 82 + y_shift), (283, 140 + y_shift), (256, 202 + y_shift), (196, 226 + y_shift), (111, 218 + y_shift), (66, 184 + y_shift)], "#101b21", INK, 6)
    h.polygon([(68, 137 + y_shift), (90, 99 + y_shift), (127, 73 + y_shift), (170, 64 + y_shift), (154, 150 + y_shift), (102, 174 + y_shift)], "#26363d", "#0a1419", 3)
    h.polygon([(171, 64 + y_shift), (209, 65 + y_shift), (252, 93 + y_shift), (267, 137 + y_shift), (224, 173 + y_shift), (154, 150 + y_shift)], "#33464d", "#0a1419", 3)
    h.polygon([(101, 174 + y_shift), (154, 150 + y_shift), (224, 173 + y_shift), (247, 194 + y_shift), (195, 211 + y_shift), (118, 206 + y_shift)], "#1d2b31", "#0a1419", 3)
    h.line([(92, 111 + y_shift), (139, 90 + y_shift), (154, 150 + y_shift)], "#52676c", 4)
    h.line([(215, 83 + y_shift), (224, 173 + y_shift), (194, 202 + y_shift)], "#4a6065", 4)
    h.rounded((139, 76 + y_shift, 205, 105 + y_shift), 12, "#16252c", INK, 5)
    h.line([(154, 91 + y_shift), (190, 91 + y_shift)], CORAL, seam_width)
    h.line([(142, 118 + y_shift), (179, 111 + y_shift), (208, 124 + y_shift)], "#0b151a", 5)
    h.line([(156, 121 + y_shift), (177, 119 + y_shift), (195, 127 + y_shift)], "#35474d", 3)
    h.rounded((147, 178 + y_shift, 188, 194 + y_shift), 7, "#101a1f", "#35464b", 3)
    h.line([(154, 186 + y_shift), (181, 186 + y_shift)], "#26363c", 4)

    if action in ("charge", "contact"):
        glow = glow_circle(h.image.size, (172 * h.scale, (91 + y_shift) * h.scale), 42 * h.scale, (239, 74, 67))
        h.image = Image.alpha_composite(glow, h.image)
    return baseline_align(h.finish(), 288)


def draw_shield() -> Image.Image:
    h = HiDraw(256, 256)
    h.rounded((48, 17, 208, 34), 4, "#8e7750", INK, 3)
    h.rounded((68, 27, 84, 74), 4, "#6e5f45", INK, 3)
    h.rounded((172, 27, 188, 74), 4, "#6e5f45", INK, 3)
    outer = [(78, 25), (178, 25), (201, 54), (194, 205), (174, 246), (82, 246), (62, 205), (55, 54)]
    inner = [(88, 42), (168, 42), (183, 64), (177, 195), (160, 226), (96, 226), (79, 195), (73, 64)]
    h.polygon(outer, "#17262d", INK, 5)
    h.polygon(inner, "#566970", "#263a42", 3)
    h.polygon([(91, 48), (128, 44), (128, 222), (96, 219), (82, 188), (84, 72)], "#71858a", "#31464c", 2)
    h.polygon([(128, 44), (165, 50), (177, 72), (171, 196), (157, 218), (128, 222)], OLIVE, "#31464c", 2)
    h.line([(128, 48), (128, 221)], "#c2aa69", 4)
    h.line([(89, 77), (120, 111)], "#aeb9b4", 3)
    h.line([(167, 96), (137, 124)], "#aeb9b4", 3)
    for x, y, rx, ry in ((101, 73, 13, 9), (153, 132, 16, 10), (112, 188, 15, 10)):
        h.ellipse((x - rx, y - ry, x + rx, y + ry), "#231a18", "#875347", 3)
        h.ellipse((x - rx // 2, y - ry // 2, x + rx // 2, y + ry // 2), "#090d0f", "#a05b48", 1)
    h.line([(166, 57), (176, 73)], "#d5a45d", 2)
    h.line([(153, 212), (169, 202)], "#d5a45d", 2)
    return baseline_align(h.finish(), 255)


def draw_vehicle() -> Image.Image:
    h = HiDraw(128, 128)
    h.ellipse((22, 84, 45, 107), "#10171b", INK, 3)
    h.ellipse((86, 84, 109, 107), "#10171b", INK, 3)
    h.ellipse((27, 89, 41, 103), STEEL, INK, 2)
    h.ellipse((91, 89, 105, 103), STEEL, INK, 2)
    h.polygon([(15, 62), (37, 47), (88, 47), (112, 64), (111, 91), (18, 91)], "#28444d", INK, 3)
    h.polygon([(69, 49), (90, 51), (105, 64), (72, 64)], "#7b9295", INK, 2)
    h.polygon([(30, 52), (61, 50), (61, 64), (22, 65)], "#48636a", INK, 2)
    h.polygon([(20, 70), (109, 69), (109, 79), (17, 81)], AMBER, INK, 2)
    h.rounded((28, 80, 96, 91), 3, "#1c3037", INK, 2)
    h.polygon([(111, 66), (121, 70), (117, 83), (110, 84)], "#b7d1cd", INK, 2)
    h.line([(41, 47), (41, 31), (63, 31)], "#657b7e", 3)
    h.rounded((61, 26, 72, 36), 3, CORAL, INK, 2)
    return baseline_align(h.finish(), 105)


def make_action_assets(outputs: dict[str, Path]) -> tuple[list[Image.Image], list[Image.Image], Image.Image, Image.Image]:
    asset_root = HERE / "assets"
    guardian_actions = ["idle", "step_a", "step_b", "brace", "recoil"]
    guardian_frames = [draw_guardian_frame(action) for action in guardian_actions]
    guardian_strip = Image.new("RGBA", (1280, 256), (0, 0, 0, 0))
    for index, frame in enumerate(guardian_frames):
        action = guardian_actions[index]
        guardian_strip.alpha_composite(frame, (index * 256, 0))
        frame_path = asset_root / "guardian_z_south" / f"guardian-z-south-{action}-256x256.png"
        frame_path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(frame_path, optimize=True)
        outputs[f"guardian_z_south_{action}"] = frame_path
    guardian_strip_path = asset_root / "atlases" / "R05_GUARDIAN_Z_SOUTH_ACTION_PROOF_1280x256.png"
    guardian_strip_path.parent.mkdir(parents=True, exist_ok=True)
    guardian_strip.save(guardian_strip_path, optimize=True)
    outputs["guardian_z_south_action_strip"] = guardian_strip_path

    breaker_actions = ["idle", "charge", "contact"]
    breaker_frames = [draw_breaker_frame(action) for action in breaker_actions]
    breaker_strip = Image.new("RGBA", (960, 320), (0, 0, 0, 0))
    for index, frame in enumerate(breaker_frames):
        action = breaker_actions[index]
        breaker_strip.alpha_composite(frame, (index * 320, 0))
        frame_path = asset_root / "breaker_north" / f"breaker-north-{action}-320x320.png"
        frame_path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(frame_path, optimize=True)
        outputs[f"breaker_north_{action}"] = frame_path
    breaker_strip_path = asset_root / "atlases" / "R05_BREAKER_NORTH_ACTION_PROOF_960x320.png"
    breaker_strip.save(breaker_strip_path, optimize=True)
    outputs["breaker_north_action_strip"] = breaker_strip_path

    shield = draw_shield()
    shield_path = asset_root / "props" / "R05_SHIELD_WALL_HUNG_256x256.png"
    shield_path.parent.mkdir(parents=True, exist_ok=True)
    shield.save(shield_path, optimize=True)
    outputs["shield_wall_hung"] = shield_path

    vehicle = draw_vehicle()
    vehicle_path = asset_root / "vehicles" / "R05_VEHICLE_EAST_STATIC_128x128.png"
    vehicle_path.parent.mkdir(parents=True, exist_ok=True)
    vehicle.save(vehicle_path, optimize=True)
    outputs["vehicle_east_static"] = vehicle_path
    return guardian_frames, breaker_frames, shield, vehicle


def project(x: float, y: float) -> tuple[int, int]:
    return (round(880 + (x - y) * 40), round(170 + (x + y) * 20))


def cell_polygon(x: float, y: float, width: int = 1, height: int = 1) -> list[tuple[int, int]]:
    p0 = project(x, y)
    p1 = project(x + width - 1, y)
    p2 = project(x + width - 1, y + height - 1)
    p3 = project(x, y + height - 1)
    return [(p0[0], p0[1] - 20), (p1[0] + 40, p1[1]), (p2[0], p2[1] + 20), (p3[0] - 40, p3[1])]


def paste_pivot(scene: Image.Image, sprite: Image.Image, point: tuple[int, int], pivot: tuple[float, float]) -> tuple[int, int]:
    position = (round(point[0] - sprite.width * pivot[0]), round(point[1] - sprite.height * pivot[1]))
    scene.alpha_composite(sprite, position)
    return position


def sprite_outline(sprite: Image.Image, color: tuple[int, int, int, int], radius: int = 5) -> Image.Image:
    alpha = sprite.getchannel("A")
    expanded = alpha.filter(ImageFilter.MaxFilter(radius * 2 + 1))
    ring = ImageChops.subtract(expanded, alpha)
    layer = Image.new("RGBA", sprite.size, color)
    layer.putalpha(ImageChops.multiply(ring, Image.new("L", sprite.size, color[3])))
    return layer


def load_a4_layers() -> dict[str, Image.Image]:
    return {
        "base": Image.open(source_path("SRC_A4_BASE")).convert("RGBA"),
        "buildings": Image.open(source_path("SRC_A4_BUILDINGS")).convert("RGBA"),
        "roofs": Image.open(source_path("SRC_A4_ROOFS")).convert("RGBA"),
        "foreground": Image.open(source_path("SRC_A4_FOREGROUND")).convert("RGBA"),
        "mask": Image.open(source_path("SRC_A4_OCCLUSION_MASK")).convert("RGBA"),
        "state": Image.open(source_path("SRC_A4_RESCUE_ACTIVE")).convert("RGBA"),
    }


def swarm_frames() -> list[Image.Image]:
    atlas = Image.open(source_path("SRC_A5_SWARM_96")).convert("RGBA")
    return [atlas.crop((index * 96, 0, (index + 1) * 96, 96)) for index in range(4)]


def composite_world(
    layers: dict[str, Image.Image],
    placements: list[dict],
    footprints: list[tuple[list[tuple[int, int]], str]],
) -> Image.Image:
    scene = layers["base"].copy()
    scene.alpha_composite(layers["buildings"])
    scene.alpha_composite(layers["state"])
    footprint_layer = Image.new("RGBA", scene.size, (0, 0, 0, 0))
    footprint_draw = ImageDraw.Draw(footprint_layer)
    for polygon, color in footprints:
        rgb = tuple(int(color[index:index + 2], 16) for index in (1, 3, 5))
        footprint_draw.polygon(polygon, fill=(*rgb, 42), outline=(*rgb, 180))
    scene.alpha_composite(footprint_layer)

    local_fade = Image.new("L", scene.size, 0)
    fade_draw = ImageDraw.Draw(local_fade)
    positions: list[tuple[Image.Image, tuple[int, int], tuple[int, int]]] = []
    for item in sorted(placements, key=lambda row: row["point"][1]):
        sprite = item["sprite"]
        point = item["point"]
        pivot = item["pivot"]
        top_left = (round(point[0] - sprite.width * pivot[0]), round(point[1] - sprite.height * pivot[1]))
        outline = sprite_outline(sprite, (236, 239, 225, 205), 4)
        scene.alpha_composite(outline, top_left)
        scene.alpha_composite(sprite, top_left)
        positions.append((sprite, point, top_left))
        fade_draw.ellipse((point[0] - sprite.width * 0.52, point[1] - sprite.height * 0.95, point[0] + sprite.width * 0.52, point[1] + 18), fill=255)

    roof = layers["roofs"].copy()
    roof_alpha = roof.getchannel("A")
    mask_r = layers["mask"].getchannel("R")
    active = ImageChops.multiply(local_fade, mask_r)
    reduced = roof_alpha.point(lambda value: round(value * 0.18))
    roof.putalpha(Image.composite(reduced, roof_alpha, active))
    scene.alpha_composite(roof)

    outline_alpha = ImageChops.multiply(layers["mask"].getchannel("G"), local_fade)
    roof_outline = Image.new("RGBA", scene.size, (232, 235, 216, 0))
    roof_outline.putalpha(outline_alpha.point(lambda value: round(value * 0.75)))
    scene.alpha_composite(roof_outline)
    scene.alpha_composite(layers["foreground"])
    return scene


def make_map_boards(
    outputs: dict[str, Path],
    guardian_frames: list[Image.Image],
    breaker_frames: list[Image.Image],
    shield: Image.Image,
    vehicle: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    layers = load_a4_layers()
    swarms = swarm_frames()
    initial_placements = [
        {"sprite": guardian_frames[0], "point": project(5.5, 10.5), "pivot": (0.5, 0.88)},
        {"sprite": breaker_frames[0], "point": project(24, 9), "pivot": (0.5, 0.9)},
        {"sprite": shield, "point": project(1, 2), "pivot": (0.5, 1.0)},
        {"sprite": vehicle, "point": project(28, 5), "pivot": (0.5, 0.82)},
    ]
    swarm_points = [(13, 6), (18, 5), (27, 6), (15, 12), (29, 11), (21, 14)]
    for index, point in enumerate(swarm_points):
        initial_placements.append({"sprite": swarms[index % 4], "point": project(*point), "pivot": (0.5, 1.0)})
    initial_footprints = [
        (cell_polygon(5, 10, 2, 2), CYAN),
        (cell_polygon(23, 8, 3, 3), CORAL),
        (cell_polygon(28, 5), GOLD),
        (cell_polygon(1, 2), GOLD),
    ]
    initial_scene = composite_world(layers, initial_placements, initial_footprints)
    initial_path = HERE / "review" / "A8_B1_A4_INITIAL_ACTUAL_SCALE_2400x1350.png"
    initial_path.parent.mkdir(parents=True, exist_ok=True)
    initial_scene.convert("RGB").save(initial_path, optimize=True)
    outputs["a4_initial_actual_scale"] = initial_path

    t3_placements = [
        {"sprite": guardian_frames[3], "point": project(5.5, 3.5), "pivot": (0.5, 0.88)},
        {"sprite": breaker_frames[2], "point": project(6, 7), "pivot": (0.5, 0.9)},
        {"sprite": shield, "point": project(1, 2), "pivot": (0.5, 1.0)},
    ]
    t3_footprints = [
        (cell_polygon(5, 3, 2, 2), CYAN),
        (cell_polygon(5, 6, 3, 3), CORAL),
        (cell_polygon(1, 2), GOLD),
    ]
    t3_scene = composite_world(layers, t3_placements, t3_footprints)
    crop = t3_scene.crop((240, 0, 1140, 594)).convert("RGB")
    viewport = Image.new("RGB", (1280, 720), "#09161c")
    viewport.paste(crop, (0, 54))
    draw = ImageDraw.Draw(viewport)
    draw.rectangle((0, 0, 1279, 53), fill="#071319")
    draw.text((24, 13), "T3 / GIANT CONTACT · actual scale review", font=font(23, bold=True), fill=TEXT)
    draw.text((715, 17), "shield wall-hung · rescue lane active · no red release", font=font(16), fill=MUTED)
    draw.rectangle((0, 648, 1279, 719), fill="#071319")
    draw.text((24, 670), "A4 fixed projection 40×20 · GZ 2×2 south · BREAKER 3×3 north", font=font(17), fill=MUTED)
    draw.rectangle((900, 54, 1279, 647), fill="#11242b")
    draw.rectangle((918, 74, 1260, 194), fill="#1c1b20", outline=CORAL, width=2)
    draw.text((938, 90), "CONTACT WINDOW", font=font(20, bold=True), fill=CORAL)
    draw.text((938, 127), "GUARDIAN Z  BRACE", font=font(17), fill=CYAN)
    draw.text((938, 155), "BREAKER    CONTACT", font=font(17), fill=CORAL)
    draw.rectangle((918, 216, 1260, 630), fill="#0d1c22", outline=LINE, width=2)
    for y, label, color in (
        (240, "SHIELD      WALL-HUNG", GOLD),
        (276, "RESCUE LANE ACTIVE", CYAN),
        (312, "RED CHARGE   NOT RELEASED", CORAL),
    ):
        draw.text((938, y), label, font=font(16), fill=color)
    for rect in ((938, 390, 1080, 428), (1098, 390, 1240, 428), (938, 442, 1080, 480), (1098, 442, 1240, 480), (938, 494, 1080, 532), (1098, 494, 1240, 532)):
        draw.rectangle(rect, outline=GOLD, width=2)
    draw.text((938, 572), "review composite · no runtime binding", font=font(15), fill=MUTED)
    t3_path = HERE / "review" / "A8_B1_T3_CONTACT_UI_CROP_1280x720.png"
    viewport.save(t3_path, optimize=True)
    outputs["t3_contact_ui_crop"] = t3_path
    return initial_scene, viewport


def checkerboard(size: tuple[int, int], cell: int = 24) -> Image.Image:
    image = Image.new("RGB", size, "#e9eeeb")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#d8dfdc")
    return image


def place_contain(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    work, position = contain(image, box)
    canvas.alpha_composite(work, position)


def make_review_board(
    outputs: dict[str, Path],
    old_guardian_frames: list[Image.Image],
    guardian_frames: list[Image.Image],
    breaker_frames: list[Image.Image],
    shield: Image.Image,
    vehicle: Image.Image,
) -> None:
    board = Image.new("RGBA", (2600, 1800), BG)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2599, 128), fill="#041117")
    draw.text((54, 30), "C01E02 A8｜Phase B0/B1 综合评审包", font=font(45, bold=True), fill=TEXT)
    draw.text((1870, 50), "Candidate · runtime_allowed=false · no handoff", font=font(20), fill=MUTED)

    panels = [
        (45, 165, 2555, 610, GOLD, "B0｜旧守护者 V10X 三态"),
        (45, 640, 2555, 1045, CYAN, "B1｜馆守 Z south 五动作证明"),
        (45, 1075, 1885, 1605, CORAL, "B1｜BREAKER north 三动作证明"),
        (1915, 1075, 2555, 1605, GOLD, "B1｜墙挂重盾＋应急车 east"),
    ]
    for left, top, right, bottom, accent, title in panels:
        draw.rounded_rectangle((left, top, right, bottom), radius=8, fill=PANEL, outline=LINE, width=2)
        draw.rectangle((left, top, right, top + 7), fill=accent)
        draw.text((left + 24, top + 20), title, font=font(25, bold=True), fill=accent)

    for index, frame in enumerate(old_guardian_frames):
        left = 80 + index * 820
        background = checkerboard((760, 330)).convert("RGBA")
        place_contain(background, frame, (12, 12, 748, 318))
        board.alpha_composite(background, (left, 250))
        draw.text((left, 210), ("guide", "contact", "shield_gaze")[index], font=font(21), fill=TEXT)

    for index, frame in enumerate(guardian_frames):
        left = 85 + index * 495
        background = checkerboard((450, 295)).convert("RGBA")
        place_contain(background, frame, (35, 12, 415, 278))
        board.alpha_composite(background, (left, 720))
        draw.text((left, 682), ("idle", "step_a", "step_b", "brace", "recoil")[index], font=font(20), fill=TEXT)

    for index, frame in enumerate(breaker_frames):
        left = 82 + index * 590
        background = checkerboard((545, 405)).convert("RGBA")
        place_contain(background, frame, (20, 15, 525, 390))
        board.alpha_composite(background, (left, 1160))
        draw.text((left, 1118), ("idle", "charge", "contact")[index], font=font(20), fill=TEXT)

    prop_bg = checkerboard((570, 390)).convert("RGBA")
    place_contain(prop_bg, shield, (20, 12, 315, 375))
    place_contain(prop_bg, vehicle, (315, 85, 555, 305))
    board.alpha_composite(prop_bg, (1950, 1160))
    draw.text((1972, 1545), "三旧焦痕 · D70/P30 · 无医疗十字/文字", font=font(17), fill=MUTED)

    draw.rectangle((45, 1640, 2555, 1755), fill=PANEL_2, outline=LINE, width=1)
    draw.text((70, 1666), "审查重点：V10X同体通讯｜馆守Z/BREAKER体量与动作端点｜重盾三旧痕｜车辆中性身份｜A4遮挡与接地点", font=font(22), fill=TEXT)
    draw.text((70, 1710), "V21禁入；未扩四向Atlas、车辆四帧、GIANT_CONTACT、FX/音频、Godot或Runtime。", font=font(20), fill=MUTED)
    path = HERE / "review" / "A8_B0_B1_COMPREHENSIVE_REVIEW_2600x1800.png"
    board.convert("RGB").save(path, optimize=True)
    outputs["comprehensive_review_board"] = path


def alpha_audit(asset_id: str, path: Path, frame_width: int, pivot_y: float) -> list[dict[str, str]]:
    image = Image.open(path).convert("RGBA")
    rows: list[dict[str, str]] = []
    count = image.width // frame_width
    for index in range(count):
        frame = image.crop((index * frame_width, 0, (index + 1) * frame_width, image.height))
        bbox = frame.getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError(f"empty frame: {asset_id}[{index}]")
        baseline = round(image.height * pivot_y)
        rows.append(
            {
                "asset_id": asset_id,
                "frame_index": str(index),
                "alpha_bbox": ",".join(map(str, bbox)),
                "declared_pivot": f"0.5,{pivot_y}",
                "declared_baseline_y": str(baseline),
                "alpha_bottom_y": str(bbox[3] - 1),
                "baseline_delta_px": str((bbox[3] - 1) - baseline),
                "result": "pass" if abs((bbox[3] - 1) - baseline) <= 1 else "review",
            }
        )
    return rows


def write_specs(outputs: dict[str, Path]) -> None:
    rows = [
        {
            "asset_id": "R05_COMMS_OLD_GUARDIAN_V10X",
            "path": "assets/atlases/R05_COMMS_OLD_GUARDIAN_V10X_3072x768.png",
            "dimensions": "3072x768",
            "mode": "RGBA",
            "frame_order": "guide;contact;shield_gaze",
            "frame_dimensions": "1024x768",
            "pivot": "0.5,0.5",
            "footprint": "n/a",
            "source_identity": "V10X E02 naked body; old A6 state grammar only",
            "forbidden": "legacy 09b body;human avatar;independent AI;copilot;V21 wings",
        },
        {
            "asset_id": "R05_GUARDIAN_Z_SOUTH_ACTION_PROOF",
            "path": "assets/atlases/R05_GUARDIAN_Z_SOUTH_ACTION_PROOF_1280x256.png",
            "dimensions": "1280x256",
            "mode": "RGBA",
            "frame_order": "idle;step_a;step_b;brace;recoil",
            "frame_dimensions": "256x256",
            "pivot": "0.5,0.88",
            "footprint": "2,2",
            "source_identity": "V10X identity + approved A1-C action skeleton",
            "forbidden": "full four-facing atlas;V21 wings;legacy map unit;runtime binding",
        },
        {
            "asset_id": "R05_BREAKER_NORTH_ACTION_PROOF",
            "path": "assets/atlases/R05_BREAKER_NORTH_ACTION_PROOF_960x320.png",
            "dimensions": "960x320",
            "mode": "RGBA",
            "frame_order": "idle;charge;contact",
            "frame_dimensions": "320x320",
            "pivot": "0.5,0.9",
            "footprint": "3,3",
            "source_identity": "B forelimb bearer + X bio armor + closed three-point relation",
            "forbidden": "humanized body;ordinary quadruped;open core;flight core;E03 rupture",
        },
        {
            "asset_id": "R05_SHIELD_WALL_HUNG",
            "path": "assets/props/R05_SHIELD_WALL_HUNG_256x256.png",
            "dimensions": "256x256",
            "mode": "RGBA",
            "frame_order": "wall_hung_cold",
            "frame_dimensions": "256x256",
            "pivot": "0.5,1.0",
            "footprint": "review_anchor_only",
            "source_identity": "A tower shield + F D70/P30 + three old scars",
            "forbidden": "fourth new scorch;E03 penetration;E04 breakage;acquired state",
        },
        {
            "asset_id": "R05_VEHICLE_EAST_STATIC",
            "path": "assets/vehicles/R05_VEHICLE_EAST_STATIC_128x128.png",
            "dimensions": "128x128",
            "mode": "RGBA",
            "frame_order": "east_static",
            "frame_dimensions": "128x128",
            "pivot": "0.5,0.82",
            "footprint": "1,1",
            "source_identity": "neutral urban emergency support vehicle",
            "forbidden": "medical cross;ambulance-only silhouette;last-vehicle text;story number",
        },
        {
            "asset_id": "A8_B1_A4_INITIAL_ACTUAL_SCALE",
            "path": "review/A8_B1_A4_INITIAL_ACTUAL_SCALE_2400x1350.png",
            "dimensions": "2400x1350",
            "mode": "RGB",
            "frame_order": "initial_state_review",
            "frame_dimensions": "2400x1350",
            "pivot": "n/a",
            "footprint": "A4 fixed projection 40x20",
            "source_identity": "A4 original layers + external Candidate units + A5 read-only swarm",
            "forbidden": "baked unit in A4 source;topology change;runtime handoff",
        },
        {
            "asset_id": "A8_B1_T3_CONTACT_UI_CROP",
            "path": "review/A8_B1_T3_CONTACT_UI_CROP_1280x720.png",
            "dimensions": "1280x720",
            "mode": "RGB",
            "frame_order": "T3_contact_review",
            "frame_dimensions": "1280x720",
            "pivot": "n/a",
            "footprint": "GZ 2x2 south;BREAKER 3x3 north;shield 1x1 anchor",
            "source_identity": "joint-calibrated T3 positions and A4 projection",
            "forbidden": "red release;shield acquisition;P1;runtime UI claim",
        },
    ]
    path = HERE / "asset-spec.tsv"
    write_tsv(path, rows, list(rows[0].keys()))
    outputs["asset_spec"] = path


def write_docs(outputs: dict[str, Path]) -> None:
    decision_path = HERE / "producer-comprehensive-review-card.md"
    decision_path.write_text(
        """# C01E02 A8 Phase B0/B1｜制作人综合评审卡

> 本卡回传制作人任务 `019f55ea-799e-7e71-a5f2-f91e74bdae32` 集中展示；本美术任务不单独索取用户回复。

全部文件保持 `Candidate / runtime_allowed=false / runtime_handoff=none`。

## 制作人需集中展示的四项

1. **旧守护者 V10X 三态**：是否已明确读成馆守 Z 同一主体；`guide/contact/shield_gaze` 的胸灯与波形差异是否够用。
2. **双方单向动作身份**：馆守 Z south 五动作是否同时保留 V10X 身份与 A1-C 动作端点；BREAKER north 三动作是否读成 B 前肢承重＋X 生体装甲，并保持胸缝和核心出口闭合。
3. **重盾与车辆**：墙挂盾是否是一眼可读的 A 高窄塔盾、D70/P30 与三旧焦痕；应急车是否中性、朝东且没有医疗／剧情专属标识。
4. **实际比例与遮挡**：A4 初态全图和 T3 1280×720 裁切中，2×2 馆守 Z、3×3 BREAKER、1×1 小体／车辆、墙挂盾的体量、接地点、朝向和淡出＋轮廓是否通过。

## 未开放

完整四向 Atlas、车辆四帧、Phase C、GIANT_CONTACT、FX／音频封包、Godot、Runtime copy、exact handoff、Canon/Current 晋升。
""",
        encoding="utf-8",
    )
    outputs["producer_review_card"] = decision_path

    report_path = HERE / "completion-report.md"
    report_path.write_text(
        """# C01E02 A8 Phase B0/B1｜完成报告

- 已按 52 号限域裁决使用 V10X 作为 C01E02 裸机 Demo Candidate 派生母体；红肩前甲保持独立锁块关系。
- 原 A6 旧守护者 Atlas 未覆盖；新建 V10X `guide/contact/shield_gaze` 三态及头胸／胸灯／波形源层。
- 已交馆守 Z south 五动作、BREAKER north 三动作、墙挂三旧焦痕重盾、应急车 east 静态帧。
- A4 五个静态层、active 状态层和 A5 小体均只读；单位仅作外置透明合成，没有写回地图源。
- 已交 A4 初态全图实际比例合成和 T3 接触／界面裁切。
- 未使用 V21；未扩四向 Atlas、车辆四帧、Phase C、GIANT_CONTACT、FX／音频、Godot、Runtime 或 exact handoff。

停止点：等待制作人集中展示并回收四项综合评审。
""",
        encoding="utf-8",
    )
    outputs["completion_report"] = report_path


def write_manifest(outputs: dict[str, Path]) -> Path:
    rows: list[dict[str, str]] = []
    for asset_id, path in sorted(outputs.items()):
        if path.suffix.lower() == ".png":
            with Image.open(path) as image:
                dimensions = f"{image.width}x{image.height}"
                mode = image.mode
            media_type = "image/png"
        elif path.suffix.lower() == ".tsv":
            dimensions = "n/a"
            mode = "text"
            media_type = "text/tab-separated-values"
        elif path.suffix.lower() == ".py":
            dimensions = "n/a"
            mode = "text"
            media_type = "text/x-python"
        else:
            dimensions = "n/a"
            mode = "text"
            media_type = "text/markdown"
        rows.append(
            {
                "package_id": PACKAGE_ID,
                "asset_id": asset_id,
                "path": path.relative_to(HERE).as_posix(),
                "media_type": media_type,
                "dimensions": dimensions,
                "mode": mode,
                "lifecycle": "Candidate",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
                "exact_handoff": "false",
                "canon_promotion": "none",
                "source_policy": "scoped_derivative_or_review_composite;no_runtime_binding",
                "sha256": sha256(path),
            }
        )
    path = HERE / "asset-manifest.tsv"
    write_tsv(path, rows, list(rows[0].keys()))
    return path


def write_hashes(paths: Iterable[Path]) -> Path:
    path = HERE / "core-delivery-hashes.sha256"
    unique = sorted(set(paths), key=rel)
    path.write_text("\n".join(f"{sha256(item)}  {rel(item)}" for item in unique) + "\n", encoding="utf-8")
    return path


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    source_rows = validate_sources()
    outputs: dict[str, Path] = {}

    receipt = HERE / "source-validation-receipt.tsv"
    write_tsv(
        receipt,
        source_rows,
        ["source_id", "path", "expected_sha256", "actual_sha256", "role", "result", "runtime_allowed"],
    )
    outputs["source_validation_receipt"] = receipt

    old_guardian_frames = make_old_guardian_states(outputs)
    guardian_frames, breaker_frames, shield, vehicle = make_action_assets(outputs)
    make_map_boards(outputs, guardian_frames, breaker_frames, shield, vehicle)
    make_review_board(outputs, old_guardian_frames, guardian_frames, breaker_frames, shield, vehicle)
    write_specs(outputs)

    alpha_rows: list[dict[str, str]] = []
    alpha_rows.extend(alpha_audit("R05_COMMS_OLD_GUARDIAN_V10X", outputs["old_guardian_v10x_atlas"], 1024, 0.5))
    alpha_rows.extend(alpha_audit("R05_GUARDIAN_Z_SOUTH_ACTION_PROOF", outputs["guardian_z_south_action_strip"], 256, 0.88))
    alpha_rows.extend(alpha_audit("R05_BREAKER_NORTH_ACTION_PROOF", outputs["breaker_north_action_strip"], 320, 0.9))
    alpha_rows.extend(alpha_audit("R05_SHIELD_WALL_HUNG", outputs["shield_wall_hung"], 256, 1.0))
    alpha_rows.extend(alpha_audit("R05_VEHICLE_EAST_STATIC", outputs["vehicle_east_static"], 128, 0.82))
    alpha_path = HERE / "alpha-pivot-audit.tsv"
    write_tsv(alpha_path, alpha_rows, list(alpha_rows[0].keys()))
    outputs["alpha_pivot_audit"] = alpha_path

    validator = HERE / "validate_phase_b0_b1.py"
    if validator.exists():
        outputs["validator"] = validator

    write_docs(outputs)
    manifest = write_manifest(outputs)
    hashes = write_hashes(list(outputs.values()) + [manifest, Path(__file__).resolve()] + [ROOT / row[1] for row in SOURCES])
    print(f"PASS {PACKAGE_ID}")
    print(f"outputs={len(outputs)} manifest={rel(manifest)} hashes={rel(hashes)}")
    print("lifecycle=Candidate runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
