#!/usr/bin/env python3
"""Deterministically derive GZ V10X E02 Wave-B action sprites and QA.

ImageGen owns pose pixels. This script removes the border-connected neutral
checkerboard plus only the audited enclosed negative-space components, scales
the intact cutout uniformly, registers its bottom center at the locked Camera
V2 pivot, and emits multi-background QA. It never globally keys white, repaints,
mirrors, rotates, or combines a previous rejected pose.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
import json
from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[5]
CALL = ROOT / "call01"
PIVOT = (128, 224)
CANVAS = (256, 256)
SCREEN_VECTORS = {"east": (40, 24), "south": (-40, 24)}
INTERNAL_VISUAL_PASSES = {"brace_east", "brace_south"}

INTERNAL_BACKGROUND_COMPONENTS = {
    "brace_east": (
        {
            "label": "brace_east_right_arm_to_torso_negative_space",
            "strict_bbox": (761, 457, 833, 534),
            "strict_pixels": 2840,
            "expanded_bbox": (761, 457, 834, 535),
            "expanded_pixels": 2952,
        },
    ),
    "brace_south": (
        {
            "label": "brace_south_left_arm_to_torso_negative_space",
            "strict_bbox": (448, 430, 512, 575),
            "strict_pixels": 3617,
            "expanded_bbox": (448, 429, 512, 576),
            "expanded_pixels": 3751,
        },
        {
            "label": "brace_south_right_arm_to_torso_negative_space",
            "strict_bbox": (714, 427, 841, 614),
            "strict_pixels": 6841,
            "expanded_bbox": (714, 427, 842, 615),
            "expanded_pixels": 7071,
        },
    ),
}

WHITE_SILVER_ARMOUR_SENTINELS = {
    "brace_east": {
        "chest_keel": (600, 420),
        "left_thigh_armour": (485, 600),
        "right_thigh_armour": (710, 665),
        "left_toe_armour": (280, 950),
        "right_toe_armour": (875, 1080),
    },
    "brace_south": {
        "chest_keel": (667, 405),
        "left_thigh_armour": (495, 620),
        "right_thigh_armour": (735, 590),
        "left_toe_armour": (340, 1035),
        "right_toe_armour": (955, 920),
    },
}

PRE_ALPHA_HISTORY = CALL / "_history" / "pre-internal-alpha-hole-fix-20260824"
PRE_ALPHA_CANDIDATE_SHAS = {
    "brace_east": "fc316e3169934086d9925e6eda65a8b36c7b4f0b7adaf4a265b70af77c733a8f",
    "brace_south": "acfb7180481bf9546128807568b2389bc97886d65f6d2a0cb6e0d35d89e6ccce",
}

SOURCE_IDLE_EAST = PROJECT_ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_EAST_CANDIDATE_256.png"
SOURCE_IDLE_SOUTH = PROJECT_ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png"
SOURCE_SHIELD = PROJECT_ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png"

EXPECTED = {
    SOURCE_IDLE_EAST: "1f6907776a382dd9daacdb8854725392c8f8d662b402654250327eb66bb9bdb7",
    SOURCE_IDLE_SOUTH: "d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796",
    SOURCE_SHIELD: "169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305",
}

# Per-action target height preserves the approved idle scale while allowing the
# crouched brace/block silhouettes to become visibly shorter.
ACTIONS = {
    "brace_east": {
        "raw": "GUARDIAN_Z_V10X_CAMERA_V2_BRACE_EAST_CALL01_RAW.png",
        "candidate": "GUARDIAN_Z_V10X_CAMERA_V2_BRACE_EAST_CANDIDATE_256.png",
        "target_height": 196,
        "direction": "east",
        "shield": False,
    },
    "brace_south": {
        "raw": "GUARDIAN_Z_V10X_CAMERA_V2_BRACE_SOUTH_CALL01_RAW.png",
        "candidate": "GUARDIAN_Z_V10X_CAMERA_V2_BRACE_SOUTH_CANDIDATE_256.png",
        "target_height": 196,
        "direction": "south",
        "shield": False,
    },
    "shield_take_south": {
        "raw": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_TAKE_SOUTH_CALL01_RAW.png",
        "candidate": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_TAKE_SOUTH_CANDIDATE_256.png",
        "target_height": 204,
        "direction": "south",
        "shield": True,
    },
    "shield_hold_south": {
        "raw": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_HOLD_SOUTH_CALL01_RAW.png",
        "candidate": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_HOLD_SOUTH_CANDIDATE_256.png",
        "target_height": 204,
        "direction": "south",
        "shield": True,
    },
    "shield_block_south": {
        "raw": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_BLOCK_SOUTH_CALL01_RAW.png",
        "candidate": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_BLOCK_SOUTH_CANDIDATE_256.png",
        "target_height": 196,
        "direction": "south",
        "shield": True,
    },
    "shield_bash_south": {
        "raw": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_BASH_SOUTH_CALL01_RAW.png",
        "candidate": "GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_BASH_SOUTH_CANDIDATE_256.png",
        "target_height": 202,
        "direction": "south",
        "shield": True,
    },
}


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    names = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _component_bbox(points: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def checker_alpha_with_internal_holes(rgb: Image.Image, action_key: str) -> tuple[Image.Image, dict[str, object]]:
    """Remove border checker and only action-keyed enclosed negative space."""
    rgb = rgb.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    strict_mask = bytearray(width * height)
    border_mask = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def strict_checker(x: int, y: int) -> bool:
        r, g, b = pixels[x, y]
        return min(r, g, b) >= 224 and max(r, g, b) - min(r, g, b) <= 14

    def expanded_checker(x: int, y: int) -> bool:
        r, g, b = pixels[x, y]
        return min(r, g, b) >= 180 and max(r, g, b) - min(r, g, b) <= 30

    for y in range(height):
        row = y * width
        for x in range(width):
            if strict_checker(x, y):
                strict_mask[row + x] = 1

    def enqueue_border(x: int, y: int) -> None:
        idx = y * width + x
        if strict_mask[idx] and not border_mask[idx]:
            border_mask[idx] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue_border(x, 0)
        enqueue_border(x, height - 1)
    for y in range(height):
        enqueue_border(0, y)
        enqueue_border(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x > 0:
            enqueue_border(x - 1, y)
        if x + 1 < width:
            enqueue_border(x + 1, y)
        if y > 0:
            enqueue_border(x, y - 1)
        if y + 1 < height:
            enqueue_border(x, y + 1)

    seen = bytearray(border_mask)
    strict_components: dict[tuple[int, int, int, int], list[tuple[int, int]]] = {}
    for y in range(height):
        row = y * width
        for x in range(width):
            idx = row + x
            if not strict_mask[idx] or seen[idx]:
                continue
            component: list[tuple[int, int]] = []
            seen[idx] = 1
            queue.append((x, y))
            while queue:
                cx, cy = queue.popleft()
                component.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue
                    nidx = ny * width + nx
                    if strict_mask[nidx] and not seen[nidx]:
                        seen[nidx] = 1
                        queue.append((nx, ny))
            strict_components[_component_bbox(component)] = component

    internal_mask = bytearray(width * height)
    component_receipts: list[dict[str, object]] = []
    for contract in INTERNAL_BACKGROUND_COMPONENTS.get(action_key, ()):
        strict_bbox = tuple(contract["strict_bbox"])
        component = strict_components.get(strict_bbox)
        assert component is not None, f"internal checker component missing: {contract['label']} {strict_bbox}"
        assert len(component) == contract["strict_pixels"], f"internal checker component size drift: {contract['label']}"
        expanded_seen = set(component)
        queue.extend(component)
        while queue:
            cx, cy = queue.popleft()
            for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                if not (0 <= nx < width and 0 <= ny < height) or (nx, ny) in expanded_seen:
                    continue
                if expanded_checker(nx, ny):
                    expanded_seen.add((nx, ny))
                    queue.append((nx, ny))
        expanded_points = sorted(expanded_seen)
        expanded_bbox = _component_bbox(expanded_points)
        assert expanded_bbox == tuple(contract["expanded_bbox"]), f"internal checker fringe bbox drift: {contract['label']}"
        assert len(expanded_points) == contract["expanded_pixels"], f"internal checker fringe size drift: {contract['label']}"
        for px, py in expanded_points:
            pidx = py * width + px
            assert not border_mask[pidx], f"internal checker unexpectedly touches border background: {contract['label']}"
            assert not internal_mask[pidx], f"internal checker contracts overlap: {contract['label']}"
            internal_mask[pidx] = 1
        component_receipts.append({
            "label": contract["label"],
            "strict_bbox": list(strict_bbox),
            "strict_pixels": len(component),
            "removed_bbox": list(expanded_bbox),
            "removed_pixels": len(expanded_points),
            "selection": "exact_strict_component_then_neutral_fringe_growth",
        })

    alpha = Image.new("L", rgb.size, 255)
    ap = alpha.load()
    border_removed = 0
    internal_removed = 0
    for y in range(height):
        row = y * width
        for x in range(width):
            idx = row + x
            if border_mask[idx] or internal_mask[idx]:
                ap[x, y] = 0
                border_removed += int(bool(border_mask[idx]))
                internal_removed += int(bool(internal_mask[idx]))

    for label, point in WHITE_SILVER_ARMOUR_SENTINELS.get(action_key, {}).items():
        assert ap[point[0], point[1]] == 255, f"real white/silver armour removed: {action_key}/{label}"

    rgba = rgb.convert("RGBA")
    rgba.putalpha(alpha)
    transparent = border_removed + internal_removed
    return rgba, {
        "method": "border_connected_strict_checker_plus_exact_internal_component_fringe_removal",
        "strict_classifier": {"minimum_channel": 224, "maximum_chroma": 14},
        "internal_fringe_classifier": {"minimum_channel": 180, "maximum_chroma": 30},
        "canvas_pixels": width * height,
        "border_connected_transparent_pixels": border_removed,
        "internal_background_transparent_pixels": internal_removed,
        "transparent_pixels": transparent,
        "opaque_pixels": width * height - transparent,
        "partial_alpha_pixels": 0,
        "removed_internal_background_components": component_receipts,
        "white_silver_armour_sentinels_preserved": {
            label: list(point) for label, point in WHITE_SILVER_ARMOUR_SENTINELS.get(action_key, {}).items()
        },
    }


def archive_pre_alpha_history(candidate_dir: Path, master_dir: Path, qa_dir: Path, receipt_dir: Path) -> None:
    manifest_path = PRE_ALPHA_HISTORY / "REJECTED_ALPHA_HISTORY_MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest.get("candidate_sha256") == PRE_ALPHA_CANDIDATE_SHAS, "brace pre-alpha History manifest drift"
        return
    current_candidates = {
        key: candidate_dir / str(ACTIONS[key]["candidate"])
        for key in PRE_ALPHA_CANDIDATE_SHAS
    }
    for key, path in current_candidates.items():
        assert path.is_file() and digest(path) == PRE_ALPHA_CANDIDATE_SHAS[key], f"brace pre-alpha Candidate SHA drift: {key}"
    PRE_ALPHA_HISTORY.mkdir(parents=True, exist_ok=True)
    archive_sources: list[Path] = [*current_candidates.values()]
    for key in PRE_ALPHA_CANDIDATE_SHAS:
        raw_name = str(ACTIONS[key]["raw"])
        archive_sources.extend([
            master_dir / raw_name.replace("_RAW.png", "_RGBA_MASTER.png"),
            qa_dir / str(ACTIONS[key]["candidate"]).replace("_CANDIDATE_256.png", "_DARK_LIGHT_50_100_QA.png"),
            qa_dir / str(ACTIONS[key]["candidate"]).replace("_CANDIDATE_256.png", "_SOCKET_READBACK.png"),
            receipt_dir / str(ACTIONS[key]["candidate"]).replace("_CANDIDATE_256.png", "_METADATA.json"),
        ])
    archive_sources.extend([
        receipt_dir / "CALL01_GZ_V10X_E02_WAVE_B_ACTIONS_METADATA.json",
        receipt_dir / "CALL01_SECTION2_DELIVERY_RECEIPT.md",
    ])
    archived: list[dict[str, str]] = []
    for source in archive_sources:
        if not source.is_file():
            continue
        destination = PRE_ALPHA_HISTORY / source.name
        shutil.copy2(source, destination)
        archived.append({
            "source_path": str(source.relative_to(PROJECT_ROOT)),
            "history_path": str(destination.relative_to(PROJECT_ROOT)),
            "sha256": digest(destination),
        })
    manifest = {
        "schema_id": "GZ_V10X_BRACE_PRE_INTERNAL_ALPHA_FIX_HISTORY_V1",
        "status": "REJECTED_ALPHA_HISTORY",
        "reason": "border-only alpha cleanup left opaque checkerboard inside closed pose negative space",
        "user_report": "抠图还有很多白色区域没有镂空",
        "candidate_sha256": PRE_ALPHA_CANDIDATE_SHAS,
        "runtime_allowed": False,
        "default_allowed": False,
        "canon_allowed": False,
        "archived_files": archived,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def qa_board(candidate: Image.Image, label: str) -> Image.Image:
    board = Image.new("RGBA", (768, 640), (18, 25, 34, 255))
    draw = ImageDraw.Draw(board)
    draw.text((24, 18), label.upper(), font=font(28, True), fill=(246, 247, 249, 255))
    draw.text((24, 54), "100% dark/light + 50% readability; red cross = pivot [128,224]", font=font(17), fill=(185, 199, 211, 255))
    for idx, bg in enumerate(((239, 237, 231, 255), (12, 20, 29, 255))):
        x = 24 + idx * 304
        y = 100
        draw.rectangle((x, y, x + 287, y + 287), fill=bg)
        board.alpha_composite(candidate, (x + 16, y + 16))
        px, py = x + 16 + PIVOT[0], y + 16 + PIVOT[1]
        draw.line((px - 7, py, px + 7, py), fill=(255, 70, 84, 255), width=2)
        draw.line((px, py - 7, px, py + 7), fill=(255, 70, 84, 255), width=2)
    small = candidate.resize((128, 128), Image.Resampling.LANCZOS)
    draw.rectangle((632, 100, 759, 227), fill=(239, 237, 231, 255))
    board.alpha_composite(small, (632, 100))
    draw.rectangle((632, 244, 759, 371), fill=(12, 20, 29, 255))
    board.alpha_composite(small, (632, 244))
    draw.text((24, 420), "Alpha-repaired Candidate · user=false · runtime=false · canon=false", font=font(17, True), fill=(255, 194, 67, 255))
    return board


def multibackground_alpha_qa(candidates: dict[str, Image.Image]) -> Image.Image:
    backgrounds = (
        ("PURE BLACK", (0, 0, 0, 255)),
        ("DEEP GRAY", (18, 26, 34, 255)),
        ("SATURATED MAGENTA", (216, 0, 104, 255)),
        ("SATURATED GREEN", (0, 184, 76, 255)),
    )
    keys = ("brace_east", "brace_south")
    cell_w = 320
    row_h = 286
    header_h = 58
    board = Image.new("RGBA", (cell_w * 2, header_h + row_h * len(backgrounds) * 2), (15, 20, 28, 255))
    draw = ImageDraw.Draw(board)
    for column, key in enumerate(keys):
        draw.text((column * cell_w + 14, 14), key.upper(), font=font(20, True), fill=(248, 249, 251, 255))
    for scale_index, scale_label in enumerate(("100%", "50%")):
        for bg_index, (bg_label, bg) in enumerate(backgrounds):
            row = scale_index * len(backgrounds) + bg_index
            y0 = header_h + row * row_h
            for column, key in enumerate(keys):
                x0 = column * cell_w
                draw.rectangle((x0, y0, x0 + cell_w - 1, y0 + row_h - 1), fill=bg)
                sprite = candidates[key]
                if scale_label == "100%":
                    board.alpha_composite(sprite, (x0 + 32, y0 + 22))
                else:
                    small = sprite.resize((128, 128), Image.Resampling.LANCZOS)
                    board.alpha_composite(small, (x0 + 96, y0 + 76))
                draw.text((x0 + 10, y0 + 8), f"{bg_label} · {scale_label}", font=font(13, True), fill=(255, 225, 78, 255) if bg_label == "PURE BLACK" else (248, 249, 251, 255))
    return board


def alpha_component_stats(image: Image.Image) -> dict[str, object]:
    alpha = image.getchannel("A")
    width, height = alpha.size
    pixels = alpha.load()
    seen = bytearray(width * height)
    components: list[list[tuple[int, int]]] = []
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            if pixels[x, y] < 128 or seen[idx]:
                continue
            component: list[tuple[int, int]] = []
            queue: deque[tuple[int, int]] = deque([(x, y)])
            seen[idx] = 1
            while queue:
                cx, cy = queue.popleft()
                component.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue
                    nidx = ny * width + nx
                    if pixels[nx, ny] >= 128 and not seen[nidx]:
                        seen[nidx] = 1
                        queue.append((nx, ny))
            components.append(component)
    components.sort(key=len, reverse=True)
    largest = components[0]
    return {
        "alpha_128_component_count": len(components),
        "largest_alpha_128_component_pixels": len(largest),
        "largest_alpha_128_component_bbox": list(_component_bbox(largest)),
        "corner_alpha": [alpha.getpixel((0, 0)), alpha.getpixel((255, 0)), alpha.getpixel((0, 255)), alpha.getpixel((255, 255))],
    }


def socket_readback(candidate: Image.Image, label: str, direction: str) -> Image.Image:
    board = Image.new("RGBA", (512, 416), (15, 23, 32, 255))
    draw = ImageDraw.Draw(board)
    draw.text((20, 16), f"{label.upper()} · CAMERA V2 SOCKET READBACK", font=font(22, True), fill=(246, 247, 249, 255))
    draw.text((20, 48), "256 RGBA · pivot [128,224] · footprint 2x2 · scale 1x1", font=font(15), fill=(184, 199, 211, 255))
    sprite_x, sprite_y = 128, 82
    pivot_x, pivot_y = sprite_x + PIVOT[0], sprite_y + PIVOT[1]
    diamond = [
        (pivot_x, pivot_y),
        (pivot_x + 80, pivot_y - 48),
        (pivot_x, pivot_y - 96),
        (pivot_x - 80, pivot_y - 48),
        (pivot_x, pivot_y),
    ]
    draw.line(diamond, fill=(92, 127, 151, 220), width=2)
    board.alpha_composite(candidate, (sprite_x, sprite_y))
    draw.ellipse((pivot_x - 5, pivot_y - 5, pivot_x + 5, pivot_y + 5), fill=(255, 70, 84, 255))
    vx, vy = SCREEN_VECTORS[direction]
    end = (pivot_x + vx, pivot_y + vy)
    draw.line((pivot_x, pivot_y, end[0], end[1]), fill=(255, 195, 58, 255), width=4)
    draw.polygon((end, (end[0] - 11, end[1] - 2), (end[0] - 3, end[1] - 11)), fill=(255, 195, 58, 255))
    draw.text((20, 380), f"Facing {direction.upper()} · bottom-center registration · Candidate only", font=font(15, True), fill=(255, 194, 67, 255))
    return board


def build() -> None:
    for path, expected in EXPECTED.items():
        assert digest(path) == expected, f"positive source SHA drift: {path}"

    raw_dir = CALL / "generation-raw"
    master_dir = CALL / "masters"
    candidate_dir = CALL / "map-candidates"
    qa_dir = CALL / "qa"
    receipt_dir = CALL / "receipts"
    for directory in (raw_dir, master_dir, candidate_dir, qa_dir, receipt_dir):
        directory.mkdir(parents=True, exist_ok=True)

    archive_pre_alpha_history(candidate_dir, master_dir, qa_dir, receipt_dir)

    metadata: dict[str, object] = {
        "schema_version": "1.1.0",
        "task": "Section2_GZ_V10X_E02_WaveB_actions_Call01",
        "status": "ALPHA_REPAIRED_CANDIDATE_PENDING_USER_VISUAL_REVIEW",
        "generation": {"mode": "built_in_imagegen", "random_reroll_count": 0},
        "camera": {
            "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE",
            "view_space": "map_dimetric_40x24",
        },
        "map_contract": {
            "canvas_px": list(CANVAS),
            "pivot_px": list(PIVOT),
            "footprint": [2, 2],
            "display_scale": [1, 1],
            "anchor": "footprint_bottom_center",
        },
        "source_lock": {
            "approved_v10x_idle_east": {"path": str(SOURCE_IDLE_EAST.relative_to(PROJECT_ROOT)), "sha256": EXPECTED[SOURCE_IDLE_EAST]},
            "approved_v10x_idle_south": {"path": str(SOURCE_IDLE_SOUTH.relative_to(PROJECT_ROOT)), "sha256": EXPECTED[SOURCE_IDLE_SOUTH]},
            "accepted_a17_shield_design": {"path": str(SOURCE_SHIELD.relative_to(PROJECT_ROOT)), "sha256": EXPECTED[SOURCE_SHIELD]},
            "old_guardian_and_old_shield_positive_input_count": 0,
        },
        "actions": {},
        "lifecycle": {
            "user_accepted": False,
            "alpha_repair_pending_user_visual_review": True,
            "runtime": False,
            "default": False,
            "canon": False,
            "godot_bound": False,
        },
    }

    candidate_frames: dict[str, Image.Image] = {}
    generated_paths: list[Path] = []
    for key, spec in ACTIONS.items():
        raw_path = raw_dir / str(spec["raw"])
        if not raw_path.exists():
            continue
        raw = Image.open(raw_path).convert("RGB")
        rgba, alpha_stats = checker_alpha_with_internal_holes(raw, key)
        master_path = master_dir / str(spec["raw"]).replace("_RAW.png", "_RGBA_MASTER.png")
        rgba.save(master_path)
        generated_paths.append(master_path)
        assert raw.tobytes() == rgba.convert("RGB").tobytes(), "alpha cleanup changed ImageGen RGB"
        bbox = rgba.getchannel("A").getbbox()
        assert bbox is not None, f"empty subject: {key}"
        cutout = rgba.crop(bbox)
        target_h = int(spec["target_height"])
        scale = target_h / cutout.height
        width = max(1, round(cutout.width * scale))
        height = max(1, round(cutout.height * scale))
        assert width <= 236, f"{key} too wide for safe 256 canvas: {width}"
        resized = cutout.resize((width, height), Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        x = PIVOT[0] - width // 2
        y = PIVOT[1] - height
        frame.alpha_composite(resized, (x, y))
        candidate_path = candidate_dir / str(spec["candidate"])
        frame.save(candidate_path)
        candidate_frames[key] = frame
        generated_paths.append(candidate_path)
        visible = frame.getchannel("A").getbbox()
        assert visible is not None
        assert visible[3] == PIVOT[1], f"pivot miss: {key}"
        topology = alpha_component_stats(frame)
        assert topology["corner_alpha"] == [0, 0, 0, 0], f"nontransparent map corner: {key}"
        qa_path = qa_dir / str(spec["candidate"]).replace("_CANDIDATE_256.png", "_DARK_LIGHT_50_100_QA.png")
        qa_board(frame, key).save(qa_path)
        generated_paths.append(qa_path)
        socket_path = qa_dir / str(spec["candidate"]).replace("_CANDIDATE_256.png", "_SOCKET_READBACK.png")
        socket_readback(frame, key, str(spec["direction"])).save(socket_path)
        generated_paths.append(socket_path)
        action_metadata = {
            "direction": spec["direction"],
            "shield": spec["shield"],
            "raw_path": str(raw_path.relative_to(PROJECT_ROOT)),
            "raw_sha256": digest(raw_path),
            "raw_mode": Image.open(raw_path).mode,
            "raw_size": list(raw.size),
            "alpha_cleanup": alpha_stats,
            "master_path": str(master_path.relative_to(PROJECT_ROOT)),
            "master_sha256": digest(master_path),
            "candidate_path": str(candidate_path.relative_to(PROJECT_ROOT)),
            "candidate_sha256": digest(candidate_path),
            "candidate_mode": frame.mode,
            "candidate_size": list(frame.size),
            "candidate_visible_bbox": list(visible),
            "candidate_visible_size": [visible[2] - visible[0], visible[3] - visible[1]],
            "pivot_error_px": PIVOT[1] - visible[3],
            **topology,
            "qa_path": str(qa_path.relative_to(PROJECT_ROOT)),
            "qa_sha256": digest(qa_path),
            "socket_readback_path": str(socket_path.relative_to(PROJECT_ROOT)),
            "socket_readback_sha256": digest(socket_path),
            "internal_visual_gate": "PASS_DETERMINISTIC_ALPHA_PIVOT_PENDING_USER_VISUAL_REVIEW" if key in INTERNAL_VISUAL_PASSES else "PENDING_MANUAL_REVIEW",
            "user_accepted": False,
            "runtime": False,
            "canon": False,
        }
        metadata["actions"][key] = action_metadata
        per_action_path = receipt_dir / str(spec["candidate"]).replace("_CANDIDATE_256.png", "_METADATA.json")
        per_action_path.write_text(json.dumps(action_metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated_paths.append(per_action_path)

    qa_multibackground = qa_dir / "GUARDIAN_Z_V10X_CAMERA_V2_BRACE_MULTIBACKGROUND_ALPHA_QA_100_50.png"
    assert set(candidate_frames) == INTERNAL_VISUAL_PASSES, "multi-background QA requires both brace candidates"
    multibackground_alpha_qa(candidate_frames).save(qa_multibackground)
    generated_paths.append(qa_multibackground)
    metadata["qa"] = {
        "multibackground_alpha_100_50": {
            "path": str(qa_multibackground.relative_to(PROJECT_ROOT)),
            "sha256": digest(qa_multibackground),
        }
    }
    metadata["alpha_repair"] = {
        "rejected_pre_fix_candidate_sha256": PRE_ALPHA_CANDIDATE_SHAS,
        "rejected_history_manifest_path": str((PRE_ALPHA_HISTORY / "REJECTED_ALPHA_HISTORY_MANIFEST.json").relative_to(PROJECT_ROOT)),
        "high_alpha_subject_rgb_policy": "raw RGB bytes unchanged; alpha-only cleanup plus normal derivative resize",
    }

    blocked_raw = CALL / "stage-a-block/generation-raw/GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_TAKE_SOUTH_CALL01_BLOCK_RAW.png"
    blocked_count = 1 if blocked_raw.exists() else 0
    metadata["generation"]["call_count"] = len(metadata["actions"]) + blocked_count
    metadata["generation"]["successful_candidate_count"] = len(metadata["actions"])
    metadata["generation"]["blocked_call_count"] = blocked_count
    metadata["generation"]["not_called_after_stop_count"] = 3 if blocked_count else 0
    if blocked_count:
        metadata["first_failure"] = {
            "action": "shield_take_south",
            "raw_path": str(blocked_raw.relative_to(PROJECT_ROOT)),
            "raw_sha256": digest(blocked_raw),
            "failed_gate": "exactly_three_old_scrapes_and_distinct_take_transition",
            "downstream_calls_stopped": ["shield_hold_south", "shield_block_south", "shield_bash_south"],
        }
    out = receipt_dir / "CALL01_GZ_V10X_E02_WAVE_B_ACTIONS_METADATA.json"
    out.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    generated_paths.append(out)
    hash_path = receipt_dir / "CALL01_ALPHA_REPAIRED_DELIVERY_HASHES.sha256"
    hash_path.write_text(
        "".join(f"{digest(path)}  {path.relative_to(PROJECT_ROOT)}\n" for path in generated_paths),
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
