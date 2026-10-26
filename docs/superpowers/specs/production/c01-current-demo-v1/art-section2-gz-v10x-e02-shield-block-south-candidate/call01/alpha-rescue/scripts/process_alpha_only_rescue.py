#!/usr/bin/env python3
"""Deterministic alpha-only rescue for the locked GZ shield-block Call01 raw.

This script does not draw, repaint, or alter the pose/silhouette.  It models the
four-edge-connected checker background, derives alpha, despills only the
anti-aliased edge band, registers the resulting sprite, and emits QA evidence.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


EXPECTED_RAW_SHA256 = "cebbb904d3504e54d76ac3d00f8328fb8c4d8bb3fda155d2ae3d7e2114d6270f"
RAW_NAME = "GZ_V10X_E02_SHIELD_BLOCK_SOUTH_CALL01_RAW_FAIL_RGB_1254.png"
MASTER_NAME = "GZ_V10X_E02_SHIELD_BLOCK_SOUTH_ALPHA_RESCUE_RGBA_MASTER_1254.png"
SPRITE_NAME = "GZ_V10X_E02_SHIELD_BLOCK_SOUTH_CAMERA_V2_CANDIDATE_RGBA_256.png"
PIVOT = (128, 224)
FOOTPRINT = (2, 2)
CHECKER_RESIDUAL_THRESHOLD = 5.5
CORE_DISTANCE_PX = 4.0
TARGET_VISIBLE_HEIGHT = 208
ALPHA_ZERO_THRESHOLD_256 = 2

SCRIPT_PATH = Path(__file__).resolve()
RESCUE_DIR = SCRIPT_PATH.parents[1]
CALL01_DIR = RESCUE_DIR.parent
RAW_PATH = CALL01_DIR / "generation-raw" / RAW_NAME
MASTER_PATH = RESCUE_DIR / "masters" / MASTER_NAME
SPRITE_PATH = RESCUE_DIR / "map-candidate" / SPRITE_NAME
QA_DIR = RESCUE_DIR / "qa"
QA_100_DIR = QA_DIR / "100pct"
AUDIT_PATH = RESCUE_DIR / "receipts" / "ALPHA_ONLY_RESCUE_AUDIT.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bbox_exclusive(mask: np.ndarray) -> list[int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]


def checker_background_model(rgb: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    """Recover the resampled checker from known-clean top and left margins."""
    gray = rgb.astype(np.float32).mean(axis=2)
    column_reference = np.median(gray[5:20, :], axis=0)
    row_reference = np.median(gray[:, 5:20], axis=1)
    references = np.concatenate((column_reference, row_reference))
    dark = float(np.percentile(references, 5.0))
    bright = float(np.percentile(references, 95.0))
    midpoint = (dark + bright) / 2.0
    amplitude = (bright - dark) / 2.0
    if amplitude < 1.0:
        raise RuntimeError("Checker amplitude is too small to model safely")

    sx = np.clip((column_reference - midpoint) / amplitude, -1.0, 1.0)
    sy = np.clip((row_reference - midpoint) / amplitude, -1.0, 1.0)
    background_gray = midpoint - amplitude * sy[:, None] * sx[None, :]
    background_rgb = np.repeat(background_gray[:, :, None], 3, axis=2).astype(np.float32)
    return background_rgb, {
        "dark_level": dark,
        "bright_level": bright,
        "midpoint": midpoint,
        "amplitude": amplitude,
    }


def largest_component(mask: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if count <= 1:
        raise RuntimeError("No foreground component found")
    areas = stats[1:, cv2.CC_STAT_AREA]
    selected_label = int(np.argmax(areas) + 1)
    selected = labels == selected_label
    removed = int(mask.sum() - selected.sum())
    return selected, {
        "component_count_before_keep_largest": int(count - 1),
        "kept_foreground_pixel_count": int(selected.sum()),
        "discarded_isolated_noise_pixel_count": removed,
    }


def derive_master(rgb: np.ndarray) -> tuple[np.ndarray, dict[str, object], np.ndarray, np.ndarray]:
    background, model = checker_background_model(rgb)
    source = rgb.astype(np.float32)
    residual = np.max(np.abs(source - background), axis=2)
    checker_candidate = residual <= CHECKER_RESIDUAL_THRESHOLD

    component_count, labels = cv2.connectedComponents(checker_candidate.astype(np.uint8), 8)
    edge_labels = np.unique(
        np.concatenate((labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]))
    )
    edge_labels = edge_labels[edge_labels > 0]
    outer_background = np.isin(labels, edge_labels)
    foreground_seed = ~outer_background
    foreground, foreground_stats = largest_component(foreground_seed)

    distance = cv2.distanceTransform(foreground.astype(np.uint8), cv2.DIST_L2, 5)
    core = foreground & (distance >= CORE_DISTANCE_PX)
    edge = foreground & ~core

    core_weight = core.astype(np.float32)
    blurred_weight = cv2.GaussianBlur(core_weight, (0, 0), 2.2)
    foreground_estimate = np.empty_like(source)
    for channel in range(3):
        weighted = cv2.GaussianBlur(source[:, :, channel] * core_weight, (0, 0), 2.2)
        foreground_estimate[:, :, channel] = np.where(
            blurred_weight > 1e-5,
            weighted / np.maximum(blurred_weight, 1e-5),
            source[:, :, channel],
        )

    c_minus_b = source - background
    f_minus_b = foreground_estimate - background
    vnorm_sq = np.sum(f_minus_b * f_minus_b, axis=2)
    cnorm_sq = np.sum(c_minus_b * c_minus_b, axis=2)
    dot = np.sum(c_minus_b * f_minus_b, axis=2)
    alpha_ls = dot / np.maximum(vnorm_sq, 1e-6)
    cosine = dot / np.maximum(np.sqrt(vnorm_sq * cnorm_sq), 1e-6)
    reliable = (vnorm_sq >= 30.0**2) & (cosine >= 0.80)

    geometric_alpha = np.clip((distance - 0.15) / 3.85, 0.0, 1.0)
    conservative_alpha = np.maximum(geometric_alpha, np.clip(residual / 24.0, 0.0, 1.0))
    alpha = np.where(reliable, np.clip(alpha_ls, 0.0, 1.0), conservative_alpha)
    alpha = np.maximum(alpha, geometric_alpha)
    alpha[core] = 1.0
    alpha[~foreground] = 0.0
    alpha[alpha < 0.02] = 0.0
    alpha[alpha > 0.98] = 1.0

    alpha_u8 = np.clip(np.rint(alpha * 255.0), 0, 255).astype(np.uint8)
    output_rgb = rgb.copy()
    partial = (alpha_u8 > 0) & (alpha_u8 < 255)
    safe_alpha = np.maximum(alpha[:, :, None], 1e-4)
    unblended = (source - (1.0 - alpha[:, :, None]) * background) / safe_alpha
    unblended = np.minimum(np.maximum(unblended, foreground_estimate - 32.0), foreground_estimate + 32.0)
    unblended = np.clip(np.rint(unblended), 0, 255).astype(np.uint8)
    output_rgb[partial] = unblended[partial]
    output_rgb[alpha_u8 == 0] = 0
    rgba = np.dstack((output_rgb, alpha_u8))

    rgb_changed = np.any(output_rgb != rgb, axis=2) & (alpha_u8 > 0)
    core_rgb_changed = np.any(output_rgb[core] != rgb[core], axis=1)
    opaque_rgb_changed = np.any(output_rgb[alpha_u8 == 255] != rgb[alpha_u8 == 255], axis=1)

    # Detect only checker-scale opaque components. Neutral subject whites that
    # match one checker parity are deliberately not classified as contamination.
    opaque_checker_match = (alpha_u8 >= 250) & (residual <= CHECKER_RESIDUAL_THRESHOLD)
    nmatch, match_labels, match_stats, _ = cv2.connectedComponentsWithStats(
        opaque_checker_match.astype(np.uint8), 8
    )
    opaque_checker_components: list[dict[str, object]] = []
    background_gray = background[:, :, 0]
    source_gray = source.mean(axis=2)
    source_chroma = source.max(axis=2) - source.min(axis=2)
    midpoint = float(model["midpoint"])
    for label in range(1, nmatch):
        area = int(match_stats[label, cv2.CC_STAT_AREA])
        width = int(match_stats[label, cv2.CC_STAT_WIDTH])
        height = int(match_stats[label, cv2.CC_STAT_HEIGHT])
        if area < 64 or width < 16 or height < 16:
            continue
        component = match_labels == label
        dark_parity = component & (background_gray < midpoint)
        bright_parity = component & (background_gray >= midpoint)
        if int(dark_parity.sum()) < 20 or int(bright_parity.sum()) < 20:
            continue
        dark_mean = float(source_gray[dark_parity].mean())
        bright_mean = float(source_gray[bright_parity].mean())
        chroma_mean = float(source_chroma[component].mean())
        if bright_mean - dark_mean >= 8.0 and chroma_mean <= 4.0:
            opaque_checker_components.append(
                {
                    "label": int(label),
                    "area": area,
                    "bbox": [
                        int(match_stats[label, cv2.CC_STAT_LEFT]),
                        int(match_stats[label, cv2.CC_STAT_TOP]),
                        width,
                        height,
                    ],
                    "bright_minus_dark": bright_mean - dark_mean,
                    "mean_chroma": chroma_mean,
                }
            )

    transparent_mask = alpha_u8 == 0
    transparent_count, transparent_labels, _, _ = cv2.connectedComponentsWithStats(
        transparent_mask.astype(np.uint8), 8
    )
    border_transparent_labels = {
        int(v)
        for v in np.unique(
            np.concatenate(
                (
                    transparent_labels[0, :],
                    transparent_labels[-1, :],
                    transparent_labels[:, 0],
                    transparent_labels[:, -1],
                )
            )
        )
        if int(v) != 0
    }
    enclosed_transparent_components = [
        label for label in range(1, transparent_count) if label not in border_transparent_labels
    ]

    neutral_white_core = (
        core
        & (source.min(axis=2) >= 235.0)
        & ((source.max(axis=2) - source.min(axis=2)) <= 8.0)
    )
    audit = {
        "checker_model": model,
        "checker_residual_threshold": CHECKER_RESIDUAL_THRESHOLD,
        "outer_checker_component_count": int(len(edge_labels)),
        **foreground_stats,
        "foreground_bbox_exclusive": bbox_exclusive(foreground),
        "alpha_bbox_exclusive": bbox_exclusive(alpha_u8 > 0),
        "alpha_zero_pixel_count": int((alpha_u8 == 0).sum()),
        "alpha_partial_pixel_count": int(((alpha_u8 > 0) & (alpha_u8 < 255)).sum()),
        "alpha_opaque_pixel_count": int((alpha_u8 == 255).sum()),
        "transparent_pixel_count": int((alpha_u8 == 0).sum()),
        "outside_foreground_nontransparent_pixel_count": int(np.count_nonzero(alpha_u8[~foreground])),
        "outside_transparent": bool(np.count_nonzero(alpha_u8[~foreground]) == 0),
        "transparent_component_count_8_connected": int(transparent_count - 1),
        "enclosed_transparent_component_count": int(len(enclosed_transparent_components)),
        "internal_core_rgb_changed_pixel_count": int(core_rgb_changed.sum()),
        "opaque_rgb_changed_pixel_count": int(opaque_rgb_changed.sum()),
        "edge_rgb_changed_pixel_count": int(rgb_changed.sum()),
        "edge_rgb_changed_bbox_exclusive": bbox_exclusive(rgb_changed),
        "edge_band_pixel_count": int(edge.sum()),
        "core_distance_px": CORE_DISTANCE_PX,
        "neutral_white_core_preserved_pixel_count": int(neutral_white_core.sum()),
        "opaque_checker_component_count": int(len(opaque_checker_components)),
        "opaque_checker_components": opaque_checker_components,
        "opaque_checker_metric": {
            "residual_max": CHECKER_RESIDUAL_THRESHOLD,
            "alpha_min": 250,
            "minimum_area": 64,
            "minimum_bbox": [16, 16],
            "minimum_pixels_per_checker_parity": 20,
            "minimum_bright_minus_dark": 8.0,
            "maximum_mean_chroma": 4.0,
        },
    }
    return rgba, audit, foreground, core


def premultiplied_resize(rgba: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    alpha = rgba[:, :, 3].astype(np.float32) / 255.0
    rgb = rgba[:, :, :3].astype(np.float32) / 255.0
    premultiplied = rgb * alpha[:, :, None]
    resample = Image.Resampling.LANCZOS
    resized_alpha = np.array(
        Image.fromarray(alpha, mode="F").resize(size, resample=resample), dtype=np.float32
    )
    resized_pre = np.stack(
        [
            np.array(
                Image.fromarray(premultiplied[:, :, channel], mode="F").resize(
                    size, resample=resample
                ),
                dtype=np.float32,
            )
            for channel in range(3)
        ],
        axis=2,
    )
    resized_alpha = np.clip(resized_alpha, 0.0, 1.0)
    resized_rgb = np.zeros_like(resized_pre)
    valid = resized_alpha > 1e-6
    resized_rgb[valid] = resized_pre[valid] / resized_alpha[valid, None]
    resized_rgb = np.clip(resized_rgb, 0.0, 1.0)
    out = np.dstack(
        (
            np.clip(np.rint(resized_rgb * 255.0), 0, 255).astype(np.uint8),
            np.clip(np.rint(resized_alpha * 255.0), 0, 255).astype(np.uint8),
        )
    )
    out[out[:, :, 3] <= ALPHA_ZERO_THRESHOLD_256] = 0
    return out


def register_sprite(master: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    # Search the small deterministic range around the nominal scale so the
    # delivered visible height matches the accepted Camera V2 map scale exactly.
    nominal = TARGET_VISIBLE_HEIGHT / (
        bbox_exclusive(master[:, :, 3] > 0)[3] - bbox_exclusive(master[:, :, 3] > 0)[1]
    )
    nominal_size = int(round(master.shape[0] * nominal))
    choices: list[tuple[int, int, np.ndarray, list[int]]] = []
    for side in range(max(1, nominal_size - 12), nominal_size + 13):
        resized = premultiplied_resize(master, (side, side))
        bbox = bbox_exclusive(resized[:, :, 3] > 0)
        if bbox is None:
            continue
        visible_height = bbox[3] - bbox[1]
        choices.append((abs(visible_height - TARGET_VISIBLE_HEIGHT), side, resized, bbox))
    if not choices:
        raise RuntimeError("Could not resize a non-empty sprite")
    choices.sort(key=lambda item: (item[0], abs(item[1] - nominal_size), item[1]))
    error, side, resized, bbox = choices[0]
    if error != 0:
        raise RuntimeError(
            f"No deterministic resize produced target visible height {TARGET_VISIBLE_HEIGHT}; "
            f"closest side={side}, bbox={bbox}"
        )

    x_center = (bbox[0] + bbox[2]) / 2.0
    offset_x = int(round(PIVOT[0] - x_center))
    offset_y = int(PIVOT[1] - bbox[3])
    if offset_x < 0 or offset_y < 0 or offset_x + side > 256 or offset_y + side > 256:
        raise RuntimeError(
            f"Registered sprite would be clipped: side={side}, offset=({offset_x},{offset_y})"
        )
    canvas = np.zeros((256, 256, 4), dtype=np.uint8)
    canvas[offset_y : offset_y + side, offset_x : offset_x + side] = resized
    final_bbox = bbox_exclusive(canvas[:, :, 3] > 0)
    if final_bbox is None or final_bbox[3] != PIVOT[1]:
        raise RuntimeError(f"Pivot registration failed: final bbox={final_bbox}, pivot={PIVOT}")
    return canvas, {
        "resized_full_canvas_side_px": int(side),
        "full_canvas_scale": float(side / master.shape[0]),
        "resized_alpha_bbox_exclusive": bbox,
        "placement_offset": [offset_x, offset_y],
        "registered_alpha_bbox_exclusive": final_bbox,
        "registered_visible_size": [final_bbox[2] - final_bbox[0], final_bbox[3] - final_bbox[1]],
        "pivot": list(PIVOT),
        "footprint": list(FOOTPRINT),
        "target_visible_height": TARGET_VISIBLE_HEIGHT,
        "clipped_alpha_pixel_count": 0,
    }


def composite(rgba: np.ndarray, background: tuple[int, int, int]) -> np.ndarray:
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    fg = rgba[:, :, :3].astype(np.float32)
    bg = np.full_like(fg, background, dtype=np.float32)
    return np.clip(np.rint(fg * alpha + bg * (1.0 - alpha)), 0, 255).astype(np.uint8)


def qa_checker(size: tuple[int, int], cell: int = 16) -> np.ndarray:
    width, height = size
    yy, xx = np.indices((height, width))
    parity = ((xx // cell) + (yy // cell)) % 2
    dark = np.array([72, 78, 92], dtype=np.uint8)
    light = np.array([158, 166, 184], dtype=np.uint8)
    return np.where(parity[:, :, None] == 0, dark, light)


def alpha_composite_over(rgba: np.ndarray, background: np.ndarray) -> np.ndarray:
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    fg = rgba[:, :, :3].astype(np.float32)
    return np.clip(np.rint(fg * alpha + background.astype(np.float32) * (1.0 - alpha)), 0, 255).astype(
        np.uint8
    )


def label_panel(panel: np.ndarray, label: str) -> np.ndarray:
    image = Image.fromarray(panel, mode="RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.rectangle((0, 0, image.width, 18), fill=(8, 10, 16))
    draw.text((6, 5), label, fill=(255, 255, 255), font=font)
    return np.array(image)


def make_qa(sprite: np.ndarray, master: np.ndarray, foreground: np.ndarray, core: np.ndarray) -> dict[str, str]:
    QA_100_DIR.mkdir(parents=True, exist_ok=True)
    backgrounds = {
        "TRANSPARENT_CHECK": None,
        "BLACK": (0, 0, 0),
        "WHITE": (255, 255, 255),
        "MAGENTA": (255, 0, 255),
        "GREEN": (0, 210, 55),
    }
    panels_100: list[np.ndarray] = []
    panels_50: list[np.ndarray] = []
    paths: dict[str, str] = {}

    for name, color in backgrounds.items():
        if color is None:
            panel = alpha_composite_over(sprite, qa_checker((256, 256)))
        else:
            panel = composite(sprite, color)
        path = QA_100_DIR / f"GZ_SHIELD_BLOCK_SOUTH_100PCT_{name}_QA.png"
        Image.fromarray(panel, mode="RGB").save(path, optimize=False)
        paths[f"100pct_{name.lower()}"] = str(path)
        panels_100.append(label_panel(panel, f"100% {name}"))

        rgba_50 = premultiplied_resize(sprite, (128, 128))
        cell = np.zeros((256, 256, 4), dtype=np.uint8)
        cell[64:192, 64:192] = rgba_50
        if color is None:
            small_panel = alpha_composite_over(cell, qa_checker((256, 256)))
        else:
            small_panel = composite(cell, color)
        panels_50.append(label_panel(small_panel, f"MAP 50% {name}"))

    board_100 = np.concatenate(panels_100, axis=1)
    board_100_path = QA_DIR / "GZ_SHIELD_BLOCK_SOUTH_100PCT_5BACKGROUND_QA.png"
    Image.fromarray(board_100, mode="RGB").save(board_100_path, optimize=False)
    paths["100pct_5background_board"] = str(board_100_path)

    board_50 = np.concatenate(panels_50, axis=1)
    board_50_path = QA_DIR / "GZ_SHIELD_BLOCK_SOUTH_MAP_50PCT_5BACKGROUND_QA.png"
    Image.fromarray(board_50, mode="RGB").save(board_50_path, optimize=False)
    paths["map_50pct_5background_board"] = str(board_50_path)

    alpha_mask_path = QA_DIR / "GZ_SHIELD_BLOCK_SOUTH_ALPHA_INTERNAL_HOLES_MASK_1254.png"
    Image.fromarray(master[:, :, 3], mode="L").save(alpha_mask_path, optimize=False)
    paths["alpha_internal_holes_mask"] = str(alpha_mask_path)

    diagnostic = np.zeros((master.shape[0], master.shape[1], 3), dtype=np.uint8)
    diagnostic[~foreground] = (18, 24, 38)
    diagnostic[foreground & ~core] = (255, 160, 0)
    diagnostic[core] = (238, 238, 238)
    diagnostic_path = QA_DIR / "GZ_SHIELD_BLOCK_SOUTH_ALPHA_CORE_EDGE_DIAGNOSTIC_1254.png"
    Image.fromarray(diagnostic, mode="RGB").save(diagnostic_path, optimize=False)
    paths["alpha_core_edge_diagnostic"] = str(diagnostic_path)
    return paths


def main() -> None:
    actual_sha = sha256(RAW_PATH)
    if actual_sha != EXPECTED_RAW_SHA256:
        raise SystemExit(
            f"INPUT_SHA_MISMATCH expected={EXPECTED_RAW_SHA256} actual={actual_sha} path={RAW_PATH}"
        )

    raw_image = Image.open(RAW_PATH)
    if raw_image.mode != "RGB" or raw_image.size != (1254, 1254):
        raise SystemExit(f"Unexpected raw format: mode={raw_image.mode}, size={raw_image.size}")
    raw = np.array(raw_image, dtype=np.uint8)

    master, master_audit, foreground, core = derive_master(raw)
    sprite, registration_audit = register_sprite(master)

    MASTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPRITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(master, mode="RGBA").save(MASTER_PATH, optimize=False)
    Image.fromarray(sprite, mode="RGBA").save(SPRITE_PATH, optimize=False)
    qa_paths = make_qa(sprite, master, foreground, core)

    alpha = master[:, :, 3]
    technical_pass = all(
        (
            master_audit["internal_core_rgb_changed_pixel_count"] == 0,
            master_audit["opaque_rgb_changed_pixel_count"] == 0,
            master_audit["opaque_checker_component_count"] == 0,
            master_audit["outside_transparent"] is True,
            registration_audit["clipped_alpha_pixel_count"] == 0,
            master.shape == (1254, 1254, 4),
            sprite.shape == (256, 256, 4),
            int(alpha.min()) == 0,
            int(alpha.max()) == 255,
        )
    )
    audit = {
        "status": "ALPHA_ONLY_RESCUE_TECHNICAL_PASS_USER_REVIEW_PENDING"
        if technical_pass
        else "ALPHA_ONLY_RESCUE_FAIL_STOP",
        "technical_pass": bool(technical_pass),
        "scope": "deterministic_alpha_only_rescue",
        "not_additional_generation": True,
        "previous_call01_candidate_created_false_unchanged": True,
        "input": {
            "path": str(RAW_PATH),
            "expected_sha256": EXPECTED_RAW_SHA256,
            "actual_sha256": actual_sha,
            "mode": raw_image.mode,
            "size": list(raw_image.size),
            "mistaken_f72_hash_classification": "receipt_hash_file_self_sha_not_raw_png",
        },
        "master": {
            "path": str(MASTER_PATH),
            "sha256": sha256(MASTER_PATH),
            "mode": "RGBA",
            "size": [1254, 1254],
            "hasAlpha": True,
            **master_audit,
        },
        "map_candidate": {
            "path": str(SPRITE_PATH),
            "sha256": sha256(SPRITE_PATH),
            "mode": "RGBA",
            "size": [256, 256],
            "hasAlpha": True,
            **registration_audit,
        },
        "qa": qa_paths,
        "visual_hard_gate_readback": {
            "front_visible_hand_count": 0,
            "rear_interior_contact": "rear/interior contact visually occluded, user review pending",
            "shield_white_surface_global_key_used": False,
            "drawing_or_redrawing_used": False,
            "imagegen_used": False,
            "blender_used": False,
        },
        "lifecycle": {
            "authority": "Candidate",
            "user_accepted": False,
            "runtime_allowed": False,
            "default_allowed": False,
            "canon_migrated": False,
            "godot_binding_written": False,
        },
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    if not technical_pass:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
