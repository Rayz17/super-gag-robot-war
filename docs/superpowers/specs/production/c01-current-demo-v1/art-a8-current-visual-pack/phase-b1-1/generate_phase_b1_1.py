#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import importlib.util
import math
import os
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFilter


HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in (HERE, *HERE.parents) if (parent / ".git").exists())
BASE_DIR = HERE.parent / "phase-b0-b1"
BASE_GENERATOR = BASE_DIR / "generate_phase_b0_b1.py"
PACKAGE_ID = "C01CDV1_A8_PHASE_B1_1_V1"


def load_base_module():
    spec = importlib.util.spec_from_file_location("a8_phase_b0_b1_base", BASE_GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load base generator: {BASE_GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base_module()

BG = base.BG
PANEL = base.PANEL
PANEL_2 = base.PANEL_2
LINE = base.LINE
TEXT = base.TEXT
MUTED = base.MUTED
CYAN = base.CYAN
GOLD = base.GOLD
CORAL = base.CORAL
INK = base.INK
NAVY = base.NAVY
NAVY_LIGHT = base.NAVY_LIGHT
RED = base.RED
RED_DARK = base.RED_DARK
IVORY = base.IVORY
STEEL = base.STEEL
GRAPHITE = base.GRAPHITE
OLIVE = base.OLIVE
AMBER = base.AMBER

BASE_ASSET = BASE_DIR / "assets"
BASE_REVIEW = BASE_DIR / "review"
VEHICLE_SOURCE = BASE_ASSET / "vehicles" / "R05_VEHICLE_EAST_STATIC_128x128.png"

EXTRA_SOURCES = [
    (
        "SRC_53_OBJECTIVE",
        "docs/superpowers/specs/production/c01-current-demo-v1/53-c01e02-a8-b1-1-narrow-visual-rework-objective.md",
        "396c3d247803252460158243247f92ac7be27ba7e869a258df75a868675fe96a",
        "sole_b1_1_visual_rework_authority",
    ),
    (
        "SRC_B0B1_GENERATOR",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/generate_phase_b0_b1.py",
        "0addfa8db88e815d913a82c79ba4c3bfb40cb58076ef09e3f0d5c314c84a3f7f",
        "read_only_reproducible_base_generator",
    ),
    (
        "SRC_B0B1_MANIFEST",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/asset-manifest.tsv",
        "9d8b32a32352d46be55e9ac19b518034038b15927f942045cafbbb861e57da69",
        "producer_accepted_technical_baseline",
    ),
    (
        "SRC_B0B1_COMPLETION",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/completion-report.md",
        "93af1728f9fb51bb9ab0e2bf70bdc120ca52bc0f78c727bfb415bf019fa49c1d",
        "producer_accepted_technical_completion",
    ),
    (
        "SRC_B0B1_CORE_HASHES",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/core-delivery-hashes.sha256",
        "09cb64f2964382ba7a7eee31850776c8d44cf653056896c478027d33fb666ca8",
        "protected_delivery_hash_baseline",
    ),
    (
        "SRC_BEFORE_OLD_GUARDIAN",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/assets/atlases/R05_COMMS_OLD_GUARDIAN_V10X_3072x768.png",
        "b13bebe3a830a6c3a011ecbfede63219a3fa186dacf744bac178363db8efee8e",
        "before_comparison_only",
    ),
    (
        "SRC_BEFORE_GZ_STRIP",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/assets/atlases/R05_GUARDIAN_Z_SOUTH_ACTION_PROOF_1280x256.png",
        "ad1058c7e4a4b424c8f3b4e14070179a26443d53b958a7efe402f8a21a1acfe7",
        "before_comparison_only",
    ),
    (
        "SRC_BEFORE_BREAKER_STRIP",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/assets/atlases/R05_BREAKER_NORTH_ACTION_PROOF_960x320.png",
        "d36c75544d49a78df4b1f2d679f83e3eb9e648939b19e4c243e1e61d6cf120bf",
        "before_comparison_only",
    ),
    (
        "SRC_BEFORE_SHIELD",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/assets/props/R05_SHIELD_WALL_HUNG_256x256.png",
        "e88e252ae3077b97ba6603cc69353a7ee7e9e586cb1a76006297ba094d5fe6b4",
        "before_comparison_only",
    ),
    (
        "SRC_BEFORE_A4_INITIAL",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/review/A8_B1_A4_INITIAL_ACTUAL_SCALE_2400x1350.png",
        "1d8affce230d30356be9df60e82e8e93734bb7be2bc0dc3eade5207c66114855",
        "before_comparison_only",
    ),
    (
        "SRC_BEFORE_T3",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/review/A8_B1_T3_CONTACT_UI_CROP_1280x720.png",
        "7d1f7c9af69e5d2686093a33bba7b4cd272fa0e39ae70a4644f9b810bb9b996f",
        "before_comparison_only",
    ),
    (
        "SRC_VEHICLE_UNCHANGED",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b0-b1/assets/vehicles/R05_VEHICLE_EAST_STATIC_128x128.png",
        "09db0e7b97fcd2f522209cb68aefdcd88afcc40d468e28eb27233fb4b84180c3",
        "external_reuse_exact_bytes_no_local_rewrite",
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


def write_tsv(path: Path, rows: Iterable[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validate_sources() -> list[dict[str, str]]:
    rows = base.validate_sources()
    for source_id, path_text, expected, role in EXTRA_SOURCES:
        path = ROOT / path_text
        actual = sha256(path) if path.is_file() else "missing"
        result = "match" if actual == expected else "drift"
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


def hex_rgb(value: str) -> tuple[int, int, int]:
    return tuple(int(value[index:index + 2], 16) for index in (1, 3, 5))


def arc(h, box: tuple[float, float, float, float], start: int, end: int, fill: str, width: int) -> None:
    h.draw.arc(
        tuple(round(value * h.scale) for value in box),
        start,
        end,
        fill=fill,
        width=width * h.scale,
    )


def thick_segment(h, p1: tuple[float, float], p2: tuple[float, float], width: float, fill: str, outline: str = INK, outline_width: int = 3) -> None:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = max(math.hypot(dx, dy), 0.001)
    nx = -dy / length * width / 2
    ny = dx / length * width / 2
    h.polygon(
        [
            (p1[0] + nx, p1[1] + ny),
            (p2[0] + nx, p2[1] + ny),
            (p2[0] - nx, p2[1] - ny),
            (p1[0] - nx, p1[1] - ny),
        ],
        fill,
        outline,
        outline_width,
    )


def make_old_guardian_states(outputs: dict[str, Path]) -> list[Image.Image]:
    source = Image.open(base.source_path("SRC_GZ_V10X")).convert("RGB")
    cutout = base.connected_white_to_alpha(source)
    bbox = cutout.getbbox()
    if bbox is None:
        raise RuntimeError("V10X cutout is empty")
    cutout = cutout.crop(bbox)
    bust = cutout.crop((0, 0, cutout.width, round(cutout.height * 0.61)))
    body_master = Image.new("RGBA", (1024, 768), (0, 0, 0, 0))
    target, position = base.contain(bust, (80, 36, 944, 710))
    body_master.alpha_composite(target, position)

    states = [
        ("guide", CYAN, 36, 2, 50),
        ("contact", CORAL, 58, 4, 72),
        ("shield_gaze", GOLD, 48, 3, 56),
    ]
    frames: list[Image.Image] = []
    layer_root = HERE / "source-layers" / "old_guardian_v10x"

    for state, accent_hex, wave_radius, wave_count, glow_radius in states:
        accent = hex_rgb(accent_hex)
        body_layer = body_master.copy()
        light_layer = base.glow_circle((1024, 768), (512, 420), glow_radius, accent)
        light_draw = ImageDraw.Draw(light_layer)
        light_draw.ellipse((497, 405, 527, 435), fill=(*accent, 238), outline=(250, 238, 188, 255), width=3)
        light_draw.line((420, 230, 448, 234), fill=(*accent, 220), width=8)
        light_draw.line((576, 234, 604, 230), fill=(*accent, 220), width=8)
        if state == "shield_gaze":
            light_draw.line((430, 230, 451, 232), fill=(255, 235, 168, 248), width=5)

        waveform_layer = Image.new("RGBA", (1024, 768), (0, 0, 0, 0))
        wave_draw = ImageDraw.Draw(waveform_layer)
        for index in range(wave_count):
            radius = wave_radius + index * 24
            alpha = max(60, 210 - index * 42)
            wave_draw.arc(
                (512 - radius * 2, 650 - radius, 512 + radius * 2, 650 + radius),
                205,
                335,
                fill=(*accent, alpha),
                width=max(3, 7 - index),
            )
        if state == "shield_gaze":
            wave_draw.line((282, 596, 416, 628), fill=(*accent, 210), width=6)

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
        state_path = HERE / "assets" / "comms" / "old_guardian_v10x" / f"r05-comms-old-guardian-v10x-b1-1-{state}-1024x768.png"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(state_path, optimize=True)
        outputs[f"old_guardian_{state}_frame"] = state_path

    atlas = Image.new("RGBA", (3072, 768), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * 1024, 0))
    atlas_path = HERE / "assets" / "atlases" / "R05_COMMS_OLD_GUARDIAN_V10X_B1_1_3072x768.png"
    atlas_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(atlas_path, optimize=True)
    outputs["old_guardian_v10x_atlas"] = atlas_path
    return frames


def draw_guardian_leg(h, hip, knee, ankle, foot_x: float, foot_bottom: float, foot_direction: int) -> None:
    thick_segment(h, hip, knee, 25, IVORY, INK, 3)
    h.ellipse((knee[0] - 11, knee[1] - 11, knee[0] + 11, knee[1] + 11), GRAPHITE, GOLD, 2)
    thick_segment(h, knee, ankle, 31, NAVY_LIGHT, INK, 4)
    if foot_direction < 0:
        points = [(foot_x - 25, foot_bottom - 15), (foot_x + 18, foot_bottom - 19), (foot_x + 25, foot_bottom - 4), (foot_x + 20, foot_bottom), (foot_x - 31, foot_bottom), (foot_x - 36, foot_bottom - 7)]
    else:
        points = [(foot_x - 18, foot_bottom - 19), (foot_x + 25, foot_bottom - 15), (foot_x + 36, foot_bottom - 7), (foot_x + 31, foot_bottom), (foot_x - 20, foot_bottom), (foot_x - 25, foot_bottom - 4)]
    h.polygon(points, NAVY, INK, 4)


def draw_guardian_arm(h, shoulder, elbow, wrist, side: int) -> None:
    thick_segment(h, shoulder, elbow, 21, GRAPHITE, INK, 3)
    h.ellipse((elbow[0] - 13, elbow[1] - 10, elbow[0] + 13, elbow[1] + 10), IVORY, INK, 3)
    thick_segment(h, elbow, wrist, 35, NAVY_LIGHT, INK, 4)
    offset = -9 if side < 0 else 9
    thick_segment(h, (elbow[0] + offset, elbow[1] + 7), (wrist[0] + offset, wrist[1] - 3), 8, RED_DARK, INK, 2)
    h.ellipse((wrist[0] - 12, wrist[1] - 7, wrist[0] + 12, wrist[1] + 12), GRAPHITE, INK, 3)


def draw_guardian_frame(action: str) -> Image.Image:
    poses = {
        "idle": {
            "torso": (128, 105), "pelvis": (128, 149), "head": (128, 53),
            "shoulders": ((84, 91), (172, 91)),
            "arms": (((84, 94), (65, 128), (64, 178)), ((172, 94), (191, 128), (192, 178))),
            "legs": (((104, 147), (96, 178), (91, 207), 86, 225, -1), ((152, 147), (160, 178), (165, 207), 170, 225, 1)),
        },
        "step_a": {
            "torso": (127, 101), "pelvis": (119, 148), "head": (131, 49),
            "shoulders": ((82, 88), (172, 92)),
            "arms": (((82, 91), (60, 128), (54, 175)), ((172, 95), (194, 120), (201, 161))),
            "legs": (((101, 147), (89, 178), (77, 208), 72, 225, -1), ((143, 147), (158, 173), (172, 197), 169, 215, 1)),
        },
        "step_b": {
            "torso": (129, 101), "pelvis": (137, 148), "head": (125, 49),
            "shoulders": ((84, 92), (174, 88)),
            "arms": (((84, 95), (62, 120), (55, 161)), ((174, 91), (196, 128), (202, 175))),
            "legs": (((113, 147), (98, 173), (84, 197), 87, 215, -1), ((155, 147), (167, 178), (179, 208), 184, 225, 1)),
        },
        "brace": {
            "torso": (128, 113), "pelvis": (128, 159), "head": (128, 63),
            "shoulders": ((80, 102), (176, 102)),
            "arms": (((80, 105), (54, 134), (69, 176)), ((176, 105), (202, 134), (187, 176))),
            "legs": (((104, 158), (86, 182), (76, 209), 72, 225, -1), ((152, 158), (170, 182), (180, 209), 184, 225, 1)),
        },
        "recoil": {
            "torso": (140, 98), "pelvis": (124, 151), "head": (151, 42),
            "shoulders": ((94, 93), (186, 80)),
            "arms": (((94, 96), (65, 126), (52, 169)), ((186, 83), (207, 108), (214, 153))),
            "legs": (((106, 150), (91, 180), (78, 209), 73, 225, -1), ((146, 150), (164, 177), (179, 209), 184, 225, 1)),
        },
    }
    pose = poses[action]
    h = base.HiDraw(256, 256)

    for leg in pose["legs"]:
        draw_guardian_leg(h, *leg)
    draw_guardian_arm(h, *pose["arms"][0], -1)
    draw_guardian_arm(h, *pose["arms"][1], 1)

    torso_x, torso_y = pose["torso"]
    pelvis_x, pelvis_y = pose["pelvis"]
    left_shoulder, right_shoulder = pose["shoulders"]
    h.polygon([(pelvis_x - 38, pelvis_y - 20), (pelvis_x + 38, pelvis_y - 20), (pelvis_x + 46, pelvis_y + 4), (pelvis_x + 20, pelvis_y + 16), (pelvis_x - 20, pelvis_y + 16), (pelvis_x - 46, pelvis_y + 4)], NAVY, INK, 4)
    h.polygon([(torso_x - 3, torso_y - 31), (left_shoulder[0] + 8, left_shoulder[1] - 8), (left_shoulder[0] - 10, left_shoulder[1] + 9), (torso_x - 29, torso_y + 24), (torso_x, torso_y + 10)], RED, INK, 4)
    h.polygon([(torso_x + 3, torso_y - 31), (right_shoulder[0] - 8, right_shoulder[1] - 8), (right_shoulder[0] + 10, right_shoulder[1] + 9), (torso_x + 29, torso_y + 24), (torso_x, torso_y + 10)], RED, INK, 4)
    h.polygon([(torso_x - 8, torso_y - 33), (torso_x + 8, torso_y - 33), (torso_x + 11, torso_y + 31), (torso_x, torso_y + 42), (torso_x - 11, torso_y + 31)], IVORY, INK, 3)
    h.ellipse((torso_x - 11, torso_y - 12, torso_x + 11, torso_y + 10), AMBER, IVORY, 2)
    h.rounded((torso_x - 8, torso_y + 24, torso_x + 8, torso_y + 48), 3, AMBER, INK, 2)

    for side, shoulder in ((-1, left_shoulder), (1, right_shoulder)):
        h.ellipse((shoulder[0] - 31, shoulder[1] - 27, shoulder[0] + 31, shoulder[1] + 28), NAVY, INK, 4)
        h.ellipse((shoulder[0] - 17, shoulder[1] - 14, shoulder[0] + 17, shoulder[1] + 17), GRAPHITE, INK, 2)
        if side < 0:
            h.polygon([(shoulder[0] - 27, shoulder[1] - 11), (shoulder[0] + 7, shoulder[1] - 16), (shoulder[0] + 20, shoulder[1]), (shoulder[0] - 4, shoulder[1] + 14), (shoulder[0] - 26, shoulder[1] + 8)], RED, INK, 3)
        else:
            h.polygon([(shoulder[0] + 27, shoulder[1] - 11), (shoulder[0] - 7, shoulder[1] - 16), (shoulder[0] - 20, shoulder[1]), (shoulder[0] + 4, shoulder[1] + 14), (shoulder[0] + 26, shoulder[1] + 8)], RED, INK, 3)

    head_x, head_y = pose["head"]
    h.polygon([(head_x - 22, head_y - 15), (head_x - 12, head_y - 27), (head_x + 12, head_y - 27), (head_x + 22, head_y - 15), (head_x + 18, head_y + 17), (head_x - 18, head_y + 17)], NAVY, INK, 4)
    h.polygon([(head_x - 6, head_y - 31), (head_x + 6, head_y - 31), (head_x + 11, head_y - 8), (head_x, head_y - 2), (head_x - 11, head_y - 8)], RED, INK, 3)
    h.polygon([(head_x - 23, head_y - 12), (head_x - 52, head_y - 21), (head_x - 27, head_y + 3), (head_x - 5, head_y - 2)], GOLD, INK, 3)
    h.polygon([(head_x + 23, head_y - 12), (head_x + 52, head_y - 21), (head_x + 27, head_y + 3), (head_x + 5, head_y - 2)], GOLD, INK, 3)
    h.line([(head_x - 17, head_y + 1), (head_x - 7, head_y - 1)], AMBER, 4)
    h.line([(head_x + 7, head_y - 1), (head_x + 17, head_y + 1)], AMBER, 4)
    h.polygon([(head_x - 14, head_y + 4), (head_x + 14, head_y + 4), (head_x + 11, head_y + 22), (head_x - 11, head_y + 22)], IVORY, INK, 3)
    for offset in (-6, 0, 6):
        h.line([(head_x + offset, head_y + 7), (head_x + offset, head_y + 18)], GRAPHITE, 2)

    return base.baseline_align(h.finish(), 225)


def draw_breaker_claw(h, wrist: tuple[float, float], side: int) -> None:
    x, y = wrist
    if side < 0:
        h.polygon([(x + 10, y - 10), (x - 8, y + 2), (x - 25, y + 16), (x + 2, y + 11), (x - 14, y + 28), (x + 18, y + 12)], "#a5afb0", INK, 2)
    else:
        h.polygon([(x - 10, y - 10), (x + 8, y + 2), (x + 25, y + 16), (x - 2, y + 11), (x + 14, y + 28), (x - 18, y + 12)], "#a5afb0", INK, 2)


def draw_breaker_frame(action: str) -> Image.Image:
    poses = {
        "idle": {
            "shell": (160, 43, 47, 273, 222),
            "front": (((89, 151), (59, 211), (39, 260)), ((231, 151), (261, 211), (281, 260))),
            "hind": ((123, 202, 126), (187, 202, 194)),
            "slit_y": 76,
        },
        "charge": {
            "shell": (164, 58, 42, 280, 232),
            "front": (((94, 169), (59, 225), (36, 260)), ((234, 164), (267, 220), (284, 260))),
            "hind": ((130, 216, 133), (188, 214, 195)),
            "slit_y": 91,
        },
        "contact": {
            "shell": (158, 68, 31, 289, 238),
            "front": (((88, 181), (51, 229), (37, 258)), ((228, 176), (265, 229), (283, 258))),
            "hind": ((132, 224, 137), (180, 222, 187)),
            "slit_y": 103,
        },
    }
    pose = poses[action]
    cx, top, left, right, bottom = pose["shell"]
    h = base.HiDraw(320, 320)

    for hip_x, hip_y, foot_x in pose["hind"]:
        thick_segment(h, (hip_x, hip_y), (foot_x, 274), 27, GRAPHITE, INK, 4)
        h.rounded((foot_x - 18, 270, foot_x + 18, 288), 7, "#17242b", INK, 4)

    for side, chain in ((-1, pose["front"][0]), (1, pose["front"][1])):
        shoulder, elbow, wrist = chain
        thick_segment(h, shoulder, elbow, 31, "#26383d", INK, 4)
        h.ellipse((elbow[0] - 15, elbow[1] - 14, elbow[0] + 15, elbow[1] + 14), "#1d2c32", INK, 3)
        thick_segment(h, elbow, wrist, 35, "#31454a", INK, 4)
        draw_breaker_claw(h, wrist, side)

    outer = [
        (left + 10, top + 74), (left + 28, top + 28), (left + 70, top + 2),
        (cx - 5, top - 6), (right - 57, top + 4), (right - 18, top + 32),
        (right, top + 83), (right - 14, bottom - 18), (right - 58, bottom + 2),
        (cx + 20, bottom + 9), (left + 62, bottom + 2), (left + 17, bottom - 25),
    ]
    h.polygon(outer, "#101b20", INK, 6)

    left_plate = [
        (left + 27, top + 70), (left + 49, top + 31), (left + 87, top + 13),
        (cx - 14, top + 17), (cx - 5, top + 77), (cx - 31, top + 123),
        (left + 58, bottom - 30), (left + 24, bottom - 60),
    ]
    right_plate = [
        (cx - 4, top + 17), (right - 70, top + 15), (right - 29, top + 43),
        (right - 14, top + 82), (right - 30, bottom - 48), (right - 77, bottom - 20),
        (cx - 31, top + 123), (cx - 5, top + 77),
    ]
    belly_plate = [
        (left + 58, bottom - 63), (cx - 31, top + 123), (right - 77, bottom - 53),
        (right - 53, bottom - 18), (cx + 20, bottom + 1), (left + 70, bottom - 7),
    ]
    h.polygon(left_plate, "#2b3f43", "#091419", 3)
    h.polygon(right_plate, "#3a4d50", "#091419", 3)
    h.polygon(belly_plate, "#223237", "#091419", 3)

    # X-surface: asymmetric growth layers and flexible closed seams, deliberately not hard panel grids.
    arc(h, (left + 37, top + 32, cx + 12, bottom - 28), 195, 310, "#60777a", 4)
    arc(h, (cx - 20, top + 20, right - 24, bottom - 39), 220, 345, "#52696c", 4)
    arc(h, (left + 59, top + 64, right - 51, bottom - 5), 18, 161, "#40575a", 3)
    h.line([(cx - 3, top + 76), (cx - 13, top + 104), (cx + 8, top + 128), (cx - 9, bottom - 38)], "#0b1519", 5)
    h.line([(cx + 3, top + 78), (cx + 18, top + 101), (cx + 10, top + 127)], "#4a5e61", 2)

    h.rounded((cx - 34, pose["slit_y"], cx + 34, pose["slit_y"] + 30), 12, "#15242a", INK, 5)
    slit_width = {"idle": 4, "charge": 8, "contact": 12}[action]
    h.line([(cx - 18, pose["slit_y"] + 15), (cx + 20, pose["slit_y"] + 15)], CORAL, slit_width)
    h.rounded((cx - 23, bottom - 47, cx + 20, bottom - 31), 7, "#101a1f", "#3c5053", 3)
    h.line([(cx - 15, bottom - 39), (cx + 12, bottom - 39)], "#26373b", 4)
    h.rounded((cx - 18, top + 2, cx + 20, top + 13), 5, "#0b1519", "#293c40", 2)

    if action == "charge":
        arc(h, (cx - 91, top + 30, cx + 96, bottom - 14), 35, 145, "#6d4b49", 3)
    elif action == "contact":
        arc(h, (cx - 106, top + 45, cx + 110, bottom - 6), 31, 151, "#87504c", 4)
        h.line([(left + 50, bottom - 32), (cx - 34, bottom - 52), (right - 50, bottom - 35)], "#6d4b49", 4)

    return base.baseline_align(h.finish(), 288)


SCAR_SHAPES = [
    (
        [(88, 69), (94, 62), (105, 61), (114, 67), (116, 75), (109, 83), (98, 85), (89, 79)],
        [(95, 68), (103, 65), (111, 71), (107, 78), (98, 80), (92, 75)],
    ),
    (
        [(139, 127), (147, 119), (160, 120), (168, 128), (166, 139), (157, 146), (145, 143), (136, 135)],
        [(146, 127), (156, 124), (163, 131), (158, 140), (148, 139), (141, 133)],
    ),
    (
        [(98, 183), (106, 175), (118, 177), (127, 185), (124, 196), (114, 202), (103, 198), (95, 191)],
        [(105, 183), (115, 180), (122, 188), (117, 197), (107, 196), (101, 189)],
    ),
]


def draw_shield() -> tuple[Image.Image, Image.Image]:
    h = base.HiDraw(256, 256)
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

    scar_mask = Image.new("RGBA", h.image.size, (0, 0, 0, 0))
    mask_draw = ImageDraw.Draw(scar_mask)
    for outer_shape, inner_shape in SCAR_SHAPES:
        h.polygon(outer_shape, "#5b3831", "#8d5749", 2)
        h.polygon(inner_shape, "#171315", "#442421", 1)
        scaled_outer = h.p(outer_shape)
        mask_draw.polygon(scaled_outer, fill=(255, 255, 255, 255))
    h.line([(166, 57), (176, 73)], "#d5a45d", 2)
    h.line([(153, 212), (169, 202)], "#d5a45d", 2)

    shield = base.baseline_align(h.finish(), 255)
    mask = base.baseline_align(scar_mask.resize((256, 256), Image.Resampling.LANCZOS), 255)
    return shield, mask


def make_action_assets(outputs: dict[str, Path]) -> tuple[list[Image.Image], list[Image.Image], Image.Image]:
    guardian_actions = ["idle", "step_a", "step_b", "brace", "recoil"]
    guardian_frames = [draw_guardian_frame(action) for action in guardian_actions]
    guardian_strip = Image.new("RGBA", (1280, 256), (0, 0, 0, 0))
    for index, (action, frame) in enumerate(zip(guardian_actions, guardian_frames)):
        guardian_strip.alpha_composite(frame, (index * 256, 0))
        path = HERE / "assets" / "guardian_z_south" / f"guardian-z-south-b1-1-{action}-256x256.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(path, optimize=True)
        outputs[f"guardian_z_south_{action}"] = path
    guardian_path = HERE / "assets" / "atlases" / "R05_GUARDIAN_Z_SOUTH_ACTION_B1_1_1280x256.png"
    guardian_path.parent.mkdir(parents=True, exist_ok=True)
    guardian_strip.save(guardian_path, optimize=True)
    outputs["guardian_z_south_action_strip"] = guardian_path

    breaker_actions = ["idle", "charge", "contact"]
    breaker_frames = [draw_breaker_frame(action) for action in breaker_actions]
    breaker_strip = Image.new("RGBA", (960, 320), (0, 0, 0, 0))
    for index, (action, frame) in enumerate(zip(breaker_actions, breaker_frames)):
        breaker_strip.alpha_composite(frame, (index * 320, 0))
        path = HERE / "assets" / "breaker_north" / f"breaker-north-b1-1-{action}-320x320.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(path, optimize=True)
        outputs[f"breaker_north_{action}"] = path
    breaker_path = HERE / "assets" / "atlases" / "R05_BREAKER_NORTH_ACTION_B1_1_960x320.png"
    breaker_strip.save(breaker_path, optimize=True)
    outputs["breaker_north_action_strip"] = breaker_path

    shield, scar_mask = draw_shield()
    shield_path = HERE / "assets" / "props" / "R05_SHIELD_WALL_HUNG_B1_1_256x256.png"
    shield_path.parent.mkdir(parents=True, exist_ok=True)
    shield.save(shield_path, optimize=True)
    outputs["shield_wall_hung"] = shield_path
    mask_path = HERE / "source-layers" / "shield" / "shield-old-burn-scar-mask-256x256.png"
    mask_path.parent.mkdir(parents=True, exist_ok=True)
    scar_mask.save(mask_path, optimize=True)
    outputs["shield_old_burn_scar_mask"] = mask_path
    return guardian_frames, breaker_frames, shield


def make_map_boards(outputs: dict[str, Path], guardian_frames: list[Image.Image], breaker_frames: list[Image.Image], shield: Image.Image) -> tuple[Image.Image, Image.Image]:
    layers = base.load_a4_layers()
    swarms = base.swarm_frames()
    vehicle = Image.open(VEHICLE_SOURCE).convert("RGBA")
    initial_placements = [
        {"sprite": guardian_frames[0], "point": base.project(5.5, 10.5), "pivot": (0.5, 0.88)},
        {"sprite": breaker_frames[0], "point": base.project(24, 9), "pivot": (0.5, 0.9)},
        {"sprite": shield, "point": base.project(1, 2), "pivot": (0.5, 1.0)},
        {"sprite": vehicle, "point": base.project(28, 5), "pivot": (0.5, 0.82)},
    ]
    for index, point in enumerate([(13, 6), (18, 5), (27, 6), (15, 12), (29, 11), (21, 14)]):
        initial_placements.append({"sprite": swarms[index % 4], "point": base.project(*point), "pivot": (0.5, 1.0)})
    initial_footprints = [
        (base.cell_polygon(5, 10, 2, 2), CYAN),
        (base.cell_polygon(23, 8, 3, 3), CORAL),
        (base.cell_polygon(28, 5), GOLD),
        (base.cell_polygon(1, 2), GOLD),
    ]
    initial_scene = base.composite_world(layers, initial_placements, initial_footprints)
    initial_path = HERE / "review" / "A8_B1_1_A4_INITIAL_ACTUAL_SCALE_2400x1350.png"
    initial_path.parent.mkdir(parents=True, exist_ok=True)
    initial_scene.convert("RGB").save(initial_path, optimize=True)
    outputs["a4_initial_actual_scale"] = initial_path

    gz_logic_point = base.project(5.5, 3.5)
    breaker_logic_point = base.project(6, 7)
    gz_visual_point = (gz_logic_point[0] + 48, gz_logic_point[1] + 8)
    breaker_visual_point = (breaker_logic_point[0] - 20, breaker_logic_point[1])
    t3_placements = [
        {"sprite": guardian_frames[3], "point": gz_visual_point, "pivot": (0.5, 0.88)},
        {"sprite": breaker_frames[2], "point": breaker_visual_point, "pivot": (0.5, 0.9)},
        {"sprite": shield, "point": base.project(1, 2), "pivot": (0.5, 1.0)},
    ]
    t3_footprints = [
        (base.cell_polygon(5, 3, 2, 2), CYAN),
        (base.cell_polygon(5, 6, 3, 3), CORAL),
        (base.cell_polygon(1, 2), GOLD),
    ]
    t3_scene = base.composite_world(layers, t3_placements, t3_footprints)
    crop = t3_scene.crop((240, 0, 1140, 594)).convert("RGB")
    viewport = Image.new("RGB", (1280, 720), "#09161c")
    viewport.paste(crop, (0, 54))
    draw = ImageDraw.Draw(viewport)
    draw.rectangle((0, 0, 1279, 53), fill="#071319")
    draw.text((24, 13), "T3 / GIANT CONTACT · B1.1 force relation", font=base.font(23, bold=True), fill=TEXT)
    draw.text((715, 17), "shield wall-hung · rescue lane active · no red release", font=base.font(16), fill=MUTED)
    draw.rectangle((0, 648, 1279, 719), fill="#071319")
    draw.text((24, 670), "A4 fixed topology · GZ 2×2 south · BREAKER 3×3 north · pose offsets only", font=base.font(17), fill=MUTED)
    draw.rectangle((900, 54, 1279, 647), fill="#11242b")
    draw.rectangle((918, 74, 1260, 194), fill="#1c1b20", outline=CORAL, width=2)
    draw.text((938, 90), "CONTACT WINDOW", font=base.font(20, bold=True), fill=CORAL)
    draw.text((938, 127), "GUARDIAN Z  BRACE", font=base.font(17), fill=CYAN)
    draw.text((938, 155), "BREAKER    CONTACT", font=base.font(17), fill=CORAL)
    draw.rectangle((918, 216, 1260, 630), fill="#0d1c22", outline=LINE, width=2)
    for y, label, color in ((240, "SHIELD      WALL-HUNG", GOLD), (276, "RESCUE LANE ACTIVE", CYAN), (312, "RED CHARGE   NOT RELEASED", CORAL)):
        draw.text((938, y), label, font=base.font(16), fill=color)
    for rect in ((938, 390, 1080, 428), (1098, 390, 1240, 428), (938, 442, 1080, 480), (1098, 442, 1240, 480), (938, 494, 1080, 532), (1098, 494, 1240, 532)):
        draw.rectangle(rect, outline=GOLD, width=2)
    draw.text((938, 572), "review composite · no runtime binding", font=base.font(15), fill=MUTED)
    t3_path = HERE / "review" / "A8_B1_1_T3_CONTACT_UI_CROP_1280x720.png"
    viewport.save(t3_path, optimize=True)
    outputs["t3_contact_ui_crop"] = t3_path

    gz_bbox = (gz_visual_point[0] - 128, gz_visual_point[1] - round(256 * 0.88), gz_visual_point[0] + 128, gz_visual_point[1] + round(256 * 0.12))
    b_bbox = (breaker_visual_point[0] - 160, breaker_visual_point[1] - round(320 * 0.9), breaker_visual_point[0] + 160, breaker_visual_point[1] + round(320 * 0.1))
    ix0, iy0 = max(gz_bbox[0], b_bbox[0]), max(gz_bbox[1], b_bbox[1])
    ix1, iy1 = min(gz_bbox[2], b_bbox[2]), min(gz_bbox[3], b_bbox[3])
    intersection = max(0, ix1 - ix0) * max(0, iy1 - iy0)
    gz_area = (gz_bbox[2] - gz_bbox[0]) * (gz_bbox[3] - gz_bbox[1])
    b_area = (b_bbox[2] - b_bbox[0]) * (b_bbox[3] - b_bbox[1])
    overlap_ratio = intersection / min(gz_area, b_area)
    t3_rows = [{
        "state": "T3",
        "guardian_logic_anchor": "5,3|2x2|south",
        "breaker_logic_anchor": "5,6|3x3|north",
        "guardian_visual_offset_px": "+48,+8",
        "breaker_visual_offset_px": "-20,0",
        "bbox_overlap_ratio": f"{overlap_ratio:.4f}",
        "limit": "<=0.5",
        "result": "pass" if overlap_ratio <= 0.5 else "fail",
    }]
    t3_audit = HERE / "t3-readability-audit.tsv"
    write_tsv(t3_audit, t3_rows, list(t3_rows[0].keys()))
    outputs["t3_readability_audit"] = t3_audit
    return initial_scene, viewport


def make_before_after(outputs: dict[str, Path], old_guardian_frames: list[Image.Image], guardian_frames: list[Image.Image], breaker_frames: list[Image.Image], shield: Image.Image, t3_view: Image.Image) -> None:
    board = Image.new("RGB", (2800, 2200), BG)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2799, 112), fill="#041117")
    draw.text((52, 26), "C01E02 A8 B1.1｜窄返修前后对比", font=base.font(44, bold=True), fill=TEXT)
    draw.text((2030, 43), "Candidate · no Runtime handoff", font=base.font(20), fill=MUTED)

    def panel(box, title, accent):
        draw.rounded_rectangle(box, radius=8, fill=PANEL, outline=LINE, width=2)
        draw.rectangle((box[0], box[1], box[2], box[1] + 7), fill=accent)
        draw.text((box[0] + 20, box[1] + 17), title, font=base.font(23, bold=True), fill=accent)

    panel((45, 135, 2755, 565), "馆守 Z south：重心、交替步、brace 与 recoil", CYAN)
    panel((45, 590, 2755, 1045), "BREAKER north：X表面、charge/contact 受力与安全边距", CORAL)
    panel((45, 1070, 2755, 1495), "旧守护者三态：主体锚点稳定", GOLD)
    panel((45, 1520, 2755, 2160), "重盾旧烧蚀痕与 T3 接触可读性", GOLD)

    before_gz = Image.open(BASE_ASSET / "atlases" / "R05_GUARDIAN_Z_SOUTH_ACTION_PROOF_1280x256.png").convert("RGBA")
    after_gz = Image.new("RGBA", (1280, 256), (0, 0, 0, 0))
    for index, frame in enumerate(guardian_frames):
        after_gz.alpha_composite(frame, (index * 256, 0))
    for x, label, image in ((75, "BEFORE", before_gz), (1420, "B1.1", after_gz)):
        bg = base.checkerboard((1260, 310)).convert("RGBA")
        base.place_contain(bg, image, (10, 26, 1250, 300))
        board.paste(bg.convert("RGB"), (x, 215))
        draw.text((x, 174), label, font=base.font(20, bold=True), fill=TEXT)

    before_breaker = Image.open(BASE_ASSET / "atlases" / "R05_BREAKER_NORTH_ACTION_PROOF_960x320.png").convert("RGBA")
    after_breaker = Image.new("RGBA", (960, 320), (0, 0, 0, 0))
    for index, frame in enumerate(breaker_frames):
        after_breaker.alpha_composite(frame, (index * 320, 0))
    for x, label, image in ((75, "BEFORE", before_breaker), (1420, "B1.1", after_breaker)):
        bg = base.checkerboard((1260, 330)).convert("RGBA")
        base.place_contain(bg, image, (15, 15, 1245, 320))
        board.paste(bg.convert("RGB"), (x, 675))
        draw.text((x, 634), label, font=base.font(20, bold=True), fill=TEXT)

    before_guardian = Image.open(BASE_ASSET / "atlases" / "R05_COMMS_OLD_GUARDIAN_V10X_3072x768.png").convert("RGBA")
    after_guardian = Image.new("RGBA", (3072, 768), (0, 0, 0, 0))
    for index, frame in enumerate(old_guardian_frames):
        after_guardian.alpha_composite(frame, (index * 1024, 0))
    for x, label, image in ((75, "BEFORE", before_guardian), (1420, "B1.1", after_guardian)):
        bg = base.checkerboard((1260, 305)).convert("RGBA")
        base.place_contain(bg, image, (10, 8, 1250, 297))
        board.paste(bg.convert("RGB"), (x, 1145))
        draw.text((x, 1105), label, font=base.font(20, bold=True), fill=TEXT)

    before_shield = Image.open(BASE_ASSET / "props" / "R05_SHIELD_WALL_HUNG_256x256.png").convert("RGBA")
    for x, label, image in ((80, "BEFORE", before_shield), (390, "B1.1", shield)):
        bg = base.checkerboard((270, 420)).convert("RGBA")
        base.place_contain(bg, image, (7, 25, 263, 390))
        board.paste(bg.convert("RGB"), (x, 1625))
        draw.text((x, 1585), label, font=base.font(20, bold=True), fill=TEXT)

    before_t3 = Image.open(BASE_REVIEW / "A8_B1_T3_CONTACT_UI_CROP_1280x720.png").convert("RGB")
    for x, label, image in ((760, "BEFORE", before_t3), (1775, "B1.1", t3_view)):
        thumb = image.resize((950, 534), Image.Resampling.LANCZOS)
        board.paste(thumb, (x, 1585))
        draw.text((x, 1545), label, font=base.font(20, bold=True), fill=TEXT)

    compare_path = HERE / "review" / "A8_B1_1_BEFORE_AFTER_2800x2200.png"
    board.save(compare_path, optimize=True)
    outputs["before_after_review"] = compare_path


def write_audits(outputs: dict[str, Path]) -> None:
    alpha_rows = []
    alpha_rows.extend(base.alpha_audit("R05_COMMS_OLD_GUARDIAN_V10X_B1_1", outputs["old_guardian_v10x_atlas"], 1024, 0.5))
    alpha_rows.extend(base.alpha_audit("R05_GUARDIAN_Z_SOUTH_ACTION_B1_1", outputs["guardian_z_south_action_strip"], 256, 0.88))
    alpha_rows.extend(base.alpha_audit("R05_BREAKER_NORTH_ACTION_B1_1", outputs["breaker_north_action_strip"], 320, 0.9))
    alpha_rows.extend(base.alpha_audit("R05_SHIELD_WALL_HUNG_B1_1", outputs["shield_wall_hung"], 256, 1.0))
    alpha_path = HERE / "alpha-pivot-audit.tsv"
    write_tsv(alpha_path, alpha_rows, list(alpha_rows[0].keys()))
    outputs["alpha_pivot_audit"] = alpha_path

    stability_rows = []
    centers = []
    for state in ("guide", "contact", "shield_gaze"):
        path = outputs[f"old_guardian_{state}_head_chest_layer"]
        bbox = Image.open(path).convert("RGBA").getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError(f"empty old guardian identity layer: {state}")
        center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
        centers.append(center)
        stability_rows.append({"state": state, "alpha_bbox": ",".join(map(str, bbox)), "center_x": f"{center[0]:.2f}", "center_y": f"{center[1]:.2f}"})
    reference = centers[0]
    for row, center in zip(stability_rows, centers):
        error = math.hypot(center[0] - reference[0], center[1] - reference[1])
        row["center_error_px"] = f"{error:.2f}"
        row["limit"] = "<=2"
        row["result"] = "pass" if error <= 2 else "fail"
    stability_path = HERE / "old-guardian-identity-stability-audit.tsv"
    write_tsv(stability_path, stability_rows, list(stability_rows[0].keys()))
    outputs["old_guardian_identity_stability_audit"] = stability_path

    safety_rows = []
    strip = Image.open(outputs["breaker_north_action_strip"]).convert("RGBA")
    for index, state in enumerate(("idle", "charge", "contact")):
        frame = strip.crop((index * 320, 0, (index + 1) * 320, 320))
        bbox = frame.getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError(f"empty breaker frame: {state}")
        margins = (bbox[0], bbox[1], 320 - bbox[2], 320 - bbox[3])
        edge_min = min(margins[:3]) if state == "contact" else min(margins)
        safety_rows.append({
            "state": state,
            "alpha_bbox": ",".join(map(str, bbox)),
            "left_margin": str(margins[0]),
            "top_margin": str(margins[1]),
            "right_margin": str(margins[2]),
            "bottom_margin": str(margins[3]),
            "contact_ltr_limit": ">=8" if state == "contact" else "review",
            "result": "pass" if state != "contact" or edge_min >= 8 else "fail",
        })
    safety_path = HERE / "breaker-contact-safety-audit.tsv"
    write_tsv(safety_path, safety_rows, list(safety_rows[0].keys()))
    outputs["breaker_contact_safety_audit"] = safety_path

    vehicle_rows = [{
        "asset_id": "R05_VEHICLE_EAST_STATIC_REUSED",
        "source_path": rel(VEHICLE_SOURCE),
        "expected_sha256": "09db0e7b97fcd2f522209cb68aefdcd88afcc40d468e28eb27233fb4b84180c3",
        "actual_sha256": sha256(VEHICLE_SOURCE),
        "local_copy_created": "false",
        "result": "byte_identical_reused",
    }]
    vehicle_path = HERE / "vehicle-byte-preservation.tsv"
    write_tsv(vehicle_path, vehicle_rows, list(vehicle_rows[0].keys()))
    outputs["vehicle_byte_preservation"] = vehicle_path


def write_specs(outputs: dict[str, Path]) -> None:
    rows = [
        {"asset_id": "R05_COMMS_OLD_GUARDIAN_V10X_B1_1", "path": "assets/atlases/R05_COMMS_OLD_GUARDIAN_V10X_B1_1_3072x768.png", "dimensions": "3072x768", "mode": "RGBA", "frame_order": "guide;contact;shield_gaze", "frame_dimensions": "1024x768", "pivot": "0.5,0.5", "footprint": "n/a", "source_identity": "V10X fixed head-chest master; state light/wave only", "forbidden": "body translation;legacy 09b;human avatar;V21 wings"},
        {"asset_id": "R05_GUARDIAN_Z_SOUTH_ACTION_B1_1", "path": "assets/atlases/R05_GUARDIAN_Z_SOUTH_ACTION_B1_1_1280x256.png", "dimensions": "1280x256", "mode": "RGBA", "frame_order": "idle;step_a;step_b;brace;recoil", "frame_dimensions": "256x256", "pivot": "0.5,0.88", "footprint": "2,2", "source_identity": "V10X identity + A1-C skeleton + weight correction only", "forbidden": "new action;shield;V21 wings;weapon;runtime binding"},
        {"asset_id": "R05_BREAKER_NORTH_ACTION_B1_1", "path": "assets/atlases/R05_BREAKER_NORTH_ACTION_B1_1_960x320.png", "dimensions": "960x320", "mode": "RGBA", "frame_order": "idle;charge;contact", "frame_dimensions": "320x320", "pivot": "0.5,0.9", "footprint": "3,3", "source_identity": "B forelimb bearer + visible X bio armor; closed red/chest/back relation", "forbidden": "open core;wing;E03 rupture;ordinary quadruped"},
        {"asset_id": "R05_SHIELD_WALL_HUNG_B1_1", "path": "assets/props/R05_SHIELD_WALL_HUNG_B1_1_256x256.png", "dimensions": "256x256", "mode": "RGBA", "frame_order": "wall_hung_cold", "frame_dimensions": "256x256", "pivot": "0.5,1.0", "footprint": "review_anchor_only", "source_identity": "A tower + F D70/P30 + exactly three irregular old burn scars", "forbidden": "interface rings;fourth scar;penetration;acquired state"},
        {"asset_id": "R05_VEHICLE_EAST_STATIC_REUSED", "path": "../phase-b0-b1/assets/vehicles/R05_VEHICLE_EAST_STATIC_128x128.png", "dimensions": "128x128", "mode": "RGBA", "frame_order": "east_static", "frame_dimensions": "128x128", "pivot": "0.5,0.82", "footprint": "1,1", "source_identity": "B0/B1 original exact bytes", "forbidden": "local rewrite;animation;medical identity;runtime binding"},
        {"asset_id": "A8_B1_1_A4_INITIAL_ACTUAL_SCALE", "path": "review/A8_B1_1_A4_INITIAL_ACTUAL_SCALE_2400x1350.png", "dimensions": "2400x1350", "mode": "RGB", "frame_order": "initial_state_review", "frame_dimensions": "2400x1350", "pivot": "n/a", "footprint": "A4 fixed projection 40x20", "source_identity": "A4/A5 unchanged topology; revised external unit poses", "forbidden": "topology change;baked source;runtime handoff"},
        {"asset_id": "A8_B1_1_T3_CONTACT_UI_CROP", "path": "review/A8_B1_1_T3_CONTACT_UI_CROP_1280x720.png", "dimensions": "1280x720", "mode": "RGB", "frame_order": "T3_contact_review", "frame_dimensions": "1280x720", "pivot": "n/a", "footprint": "GZ 5,3 2x2 south;BREAKER 5,6 3x3 north;shield 1,2 wall-hung", "source_identity": "same logic anchors;pose-only art offsets +48,+8 and -20,0", "forbidden": "red release;shield acquisition;logic coordinate change;runtime claim"},
    ]
    path = HERE / "asset-spec.tsv"
    write_tsv(path, rows, list(rows[0].keys()))
    outputs["asset_spec"] = path


def write_docs(outputs: dict[str, Path]) -> None:
    card = HERE / "producer-review-card.md"
    card.write_text(
        """# C01E02 A8 B1.1｜制作人集中评审卡

全部文件保持 `Candidate / runtime_allowed=false / runtime_handoff=none`。

1. 馆守 Z `step_a/step_b` 是否能看出相反支撑脚、骨盆偏移和对侧肩臂补偿；`brace/recoil` 是否具有重量与支撑解释。
2. BREAKER 是否保留 B 型轮廓，同时在地图尺寸读出 X 生体覆甲；`charge/contact` 是否分别读成蓄势与冲击压缩，contact 不触边。
3. T3 中双方头部、主要躯干和支撑点是否同时可见；BREAKER 是否保持 3×3 压迫感，而非简单放大遮住馆守 Z。
4. 旧守护者主体是否稳定；重盾三痕是否读成旧烧蚀而非接口。车辆只读复用，不在本轮重审。

停止点：等待制作人集中评审；不向本美术任务用户索取裁决。
""",
        encoding="utf-8",
    )
    outputs["producer_review_card"] = card

    report = HERE / "completion-report.md"
    report.write_text(
        """# C01E02 A8 B1.1｜完成报告

- 仅修正 53 号列出的五类视觉执行缺陷；身份、footprint、A4/A5 拓扑与剧情状态未改。
- 馆守 Z south 五动作重建重心、交替支撑、brace 降重心与 recoil 惯性；V10X 头冠、面栅、红肩、圆核及圆柱前臂保留。
- BREAKER 保留 B 前肢承重轮廓，以非对称生长层、柔性闭缝强化 X 表面；charge/contact 分别体现蓄势和冲击压缩，contact 三侧安全边距已审计。
- 旧守护者三态共用同一头胸主体层；仅胸灯、波形与轻微视线高光变化。
- 重盾仍为 A/F-D70/P30 墙挂未取得态，恰好三处旧烧蚀痕；无第四痕、贯穿或碎裂。
- T3 保持原逻辑格与剧情状态，仅使用 pose-space 美术偏移减少关键身份遮挡。
- 应急车辆不生成本地副本，直接登记 B0/B1 原文件和 SHA，字节未改。

未扩四向 Atlas、车辆动画、Phase C、GIANT_CONTACT、FX、音频、Godot、Runtime 或 exact handoff。
""",
        encoding="utf-8",
    )
    outputs["completion_report"] = report


def manifest_metadata(path: Path) -> tuple[str, str, str]:
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            return "image/png", f"{image.width}x{image.height}", image.mode
    if path.suffix.lower() == ".tsv":
        return "text/tab-separated-values", "n/a", "text"
    if path.suffix.lower() == ".py":
        return "text/x-python", "n/a", "text"
    return "text/markdown", "n/a", "text"


def write_manifest(outputs: dict[str, Path]) -> Path:
    rows = []
    for asset_id, path in sorted(outputs.items()):
        media_type, dimensions, mode = manifest_metadata(path)
        rows.append({
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
            "source_policy": "narrow_visual_rework;no_identity_or_runtime_change",
            "sha256": sha256(path),
        })
    rows.append({
        "package_id": PACKAGE_ID,
        "asset_id": "vehicle_east_static_reused",
        "path": os.path.relpath(VEHICLE_SOURCE, HERE),
        "media_type": "image/png",
        "dimensions": "128x128",
        "mode": "RGBA",
        "lifecycle": "Candidate",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "exact_handoff": "false",
        "canon_promotion": "none",
        "source_policy": "reused_external_read_only;byte_identical;no_local_copy",
        "sha256": sha256(VEHICLE_SOURCE),
    })
    rows.sort(key=lambda row: row["asset_id"])
    path = HERE / "asset-manifest.tsv"
    write_tsv(path, rows, list(rows[0].keys()))
    return path


def write_hashes(paths: Iterable[Path]) -> Path:
    path = HERE / "core-delivery-hashes.sha256"
    unique = sorted(set(item.resolve() for item in paths), key=lambda item: rel(item))
    path.write_text("\n".join(f"{sha256(item)}  {rel(item)}" for item in unique) + "\n", encoding="utf-8")
    return path


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}
    source_rows = validate_sources()
    receipt = HERE / "source-validation-receipt.tsv"
    write_tsv(receipt, source_rows, ["source_id", "path", "expected_sha256", "actual_sha256", "role", "result", "runtime_allowed"])
    outputs["source_validation_receipt"] = receipt

    old_guardian_frames = make_old_guardian_states(outputs)
    guardian_frames, breaker_frames, shield = make_action_assets(outputs)
    _, t3_view = make_map_boards(outputs, guardian_frames, breaker_frames, shield)
    make_before_after(outputs, old_guardian_frames, guardian_frames, breaker_frames, shield, t3_view)
    write_audits(outputs)
    write_specs(outputs)
    write_docs(outputs)

    validator = HERE / "validate_phase_b1_1.py"
    if validator.exists():
        outputs["validator"] = validator
    manifest = write_manifest(outputs)
    source_paths = [ROOT / row["path"] for row in source_rows]
    hashes = write_hashes(list(outputs.values()) + [manifest, Path(__file__).resolve(), VEHICLE_SOURCE] + source_paths)
    print(f"PASS {PACKAGE_ID}")
    print(f"outputs={len(outputs)} manifest={rel(manifest)} hashes={rel(hashes)}")
    print("lifecycle=Candidate runtime_allowed=false runtime_handoff=none")
    print(f"vehicle_sha256={sha256(VEHICLE_SOURCE)} local_copy=false")


if __name__ == "__main__":
    main()
