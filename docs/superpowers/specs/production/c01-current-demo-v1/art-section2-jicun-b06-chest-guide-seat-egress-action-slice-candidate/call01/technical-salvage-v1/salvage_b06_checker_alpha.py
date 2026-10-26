#!/usr/bin/env python3
"""Deterministic checker-background alpha salvage for the single B06 raw.

The script is deliberately source-locked. It removes only a bright, nearly
neutral checker field that is connected to the canvas border, plus enclosed
components that independently retain the same two-phase checker statistics.
Opaque subject RGB is never rewritten. Only transparent pixels are zeroed and
partially transparent trimap-edge pixels are colour-decontaminated.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


LOCKED_SOURCE_SHA256 = "4ae747191473e7f2a84601f15cc5d061a4c1bd3d807bfbf6029c22358163c493"
BASE_LUMA = 235
BASE_CHROMA = 8
TRIMAP_RADIUS = 10
FOREGROUND_SEED_MAX_LUMA = 175
FOREGROUND_SEED_MIN_CHROMA = 18
FOREGROUND_DONOR_INSET = 4
ENCLOSED_MIN_AREA = 16
ENCLOSED_MAX_MEAN_CHROMA = 2.5
ENCLOSED_MIN_CHECKER_LUMA_FRACTION = 0.5
STABILITY_LUMA = (230, 235, 238)


@dataclass
class Component:
    component_id: int
    indices: np.ndarray
    area: int
    bbox: tuple[int, int, int, int]
    mean_luma: float
    std_luma: float
    mean_chroma: float
    checker_luma_fraction: float
    low_chroma_fraction: float
    accepted_as_enclosed_background: bool


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def flood_from_border(mask: np.ndarray) -> np.ndarray:
    height, width = mask.shape
    flat_mask = mask.ravel()
    visited = np.zeros(mask.size, dtype=bool)
    queue: deque[int] = deque()

    def push(index: int) -> None:
        if flat_mask[index] and not visited[index]:
            visited[index] = True
            queue.append(index)

    for x in range(width):
        push(x)
        push((height - 1) * width + x)
    for y in range(height):
        push(y * width)
        push(y * width + width - 1)

    while queue:
        index = queue.popleft()
        y, x = divmod(index, width)
        if x > 0:
            push(index - 1)
        if x + 1 < width:
            push(index + 1)
        if y > 0:
            push(index - width)
        if y + 1 < height:
            push(index + width)
    return visited.reshape(mask.shape)


def connected_components(
    mask: np.ndarray,
    luma: np.ndarray,
    chroma: np.ndarray,
) -> list[Component]:
    height, width = mask.shape
    flat_mask = mask.ravel()
    visited = np.zeros(mask.size, dtype=bool)
    components: list[Component] = []
    component_id = 0

    for seed in np.flatnonzero(flat_mask):
        seed = int(seed)
        if visited[seed]:
            continue
        component_id += 1
        queue: deque[int] = deque([seed])
        visited[seed] = True
        indices: list[int] = []
        while queue:
            index = queue.popleft()
            indices.append(index)
            y, x = divmod(index, width)
            for neighbour in (
                index - 1 if x > 0 else -1,
                index + 1 if x + 1 < width else -1,
                index - width if y > 0 else -1,
                index + width if y + 1 < height else -1,
            ):
                if neighbour >= 0 and flat_mask[neighbour] and not visited[neighbour]:
                    visited[neighbour] = True
                    queue.append(neighbour)

        index_array = np.asarray(indices, dtype=np.int32)
        ys = index_array // width
        xs = index_array % width
        component_luma = luma[ys, xs]
        component_chroma = chroma[ys, xs]
        checker_fraction = float(
            np.mean(
                ((component_luma >= 242.0) & (component_luma <= 248.0))
                | (component_luma >= 251.0)
            )
        )
        mean_chroma = float(np.mean(component_chroma))
        accepted = (
            len(indices) >= ENCLOSED_MIN_AREA
            and mean_chroma <= ENCLOSED_MAX_MEAN_CHROMA
            and checker_fraction >= ENCLOSED_MIN_CHECKER_LUMA_FRACTION
        )
        components.append(
            Component(
                component_id=component_id,
                indices=index_array,
                area=len(indices),
                bbox=(int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())),
                mean_luma=float(np.mean(component_luma)),
                std_luma=float(np.std(component_luma)),
                mean_chroma=mean_chroma,
                checker_luma_fraction=checker_fraction,
                low_chroma_fraction=float(np.mean(component_chroma <= 3)),
                accepted_as_enclosed_background=accepted,
            )
        )
    return components


def dilate8(mask: np.ndarray, radius: int) -> np.ndarray:
    current = mask.copy()
    for _ in range(radius):
        previous = current
        expanded = previous.copy()
        expanded[1:, :] |= previous[:-1, :]
        expanded[:-1, :] |= previous[1:, :]
        expanded[:, 1:] |= previous[:, :-1]
        expanded[:, :-1] |= previous[:, 1:]
        expanded[1:, 1:] |= previous[:-1, :-1]
        expanded[1:, :-1] |= previous[:-1, 1:]
        expanded[:-1, 1:] |= previous[1:, :-1]
        expanded[:-1, :-1] |= previous[1:, 1:]
        current = expanded
    return current


def offset_groups(max_radius: int) -> list[list[tuple[int, int]]]:
    groups: dict[int, list[tuple[int, int]]] = {}
    for dy in range(-max_radius, max_radius + 1):
        for dx in range(-max_radius, max_radius + 1):
            distance_squared = dx * dx + dy * dy
            if distance_squared == 0 or distance_squared > max_radius * max_radius:
                continue
            groups.setdefault(distance_squared, []).append((dy, dx))
    return [groups[key] for key in sorted(groups)]


def nearest_mean_rgb(
    rgb: np.ndarray,
    source_mask: np.ndarray,
    y: int,
    x: int,
    groups: list[list[tuple[int, int]]],
) -> np.ndarray | None:
    height, width = source_mask.shape
    for group in groups:
        values: list[np.ndarray] = []
        for dy, dx in group:
            yy = y + dy
            xx = x + dx
            if 0 <= yy < height and 0 <= xx < width and source_mask[yy, xx]:
                values.append(rgb[yy, xx].astype(np.float64))
        if values:
            return np.mean(np.stack(values, axis=0), axis=0)
    return None


def bbox_for_alpha(alpha: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.where(alpha > 0)
    if len(xs) == 0:
        return (0, 0, -1, -1)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def recover(
    rgb_u8: np.ndarray,
    luma_floor: int,
    chroma_limit: int,
) -> tuple[np.ndarray, dict, list[Component], np.ndarray]:
    rgb = rgb_u8.astype(np.float64)
    luma = np.mean(rgb, axis=2)
    chroma = np.max(rgb, axis=2) - np.min(rgb, axis=2)
    checker_candidate = (luma >= luma_floor) & (chroma <= chroma_limit)
    border_background = flood_from_border(checker_candidate)
    enclosed_candidate = checker_candidate & ~border_background
    components = connected_components(enclosed_candidate, luma, chroma)

    definite_background = border_background.copy()
    flat_background = definite_background.ravel()
    accepted_components = 0
    accepted_component_pixels = 0
    for component in components:
        if component.accepted_as_enclosed_background:
            flat_background[component.indices] = True
            accepted_components += 1
            accepted_component_pixels += component.area

    expanded_background = dilate8(definite_background, TRIMAP_RADIUS)
    # High-confidence subject donors deliberately exclude pale, nearly neutral
    # pixels.  Donors also sit several pixels inside the recovered silhouette,
    # so dark anti-aliased outline pixels are solved rather than frozen opaque.
    confident_foreground = (
        ~dilate8(definite_background, FOREGROUND_DONOR_INSET)
    ) & (
        (luma <= FOREGROUND_SEED_MAX_LUMA)
        | (chroma >= FOREGROUND_SEED_MIN_CHROMA)
    )
    unknown = expanded_background & ~definite_background
    alpha = np.full(luma.shape, 255, dtype=np.uint8)
    alpha[definite_background] = 0
    output_rgb = rgb_u8.copy()
    output_rgb[definite_background] = 0

    groups = offset_groups(TRIMAP_RADIUS * 4)
    partial_count = 0
    projection_residuals: list[float] = []
    missing_neighbour_count = 0
    for y, x in zip(*np.where(unknown)):
        background = nearest_mean_rgb(rgb_u8, definite_background, int(y), int(x), groups)
        foreground = nearest_mean_rgb(
            rgb_u8, confident_foreground, int(y), int(x), groups
        )
        if background is None or foreground is None:
            missing_neighbour_count += 1
            continue
        observed = rgb[y, x]
        direction = foreground - background
        denominator = float(np.dot(direction, direction))
        if denominator < 64.0:
            continue
        alpha_float = float(np.dot(observed - background, direction) / denominator)
        alpha_float = min(1.0, max(0.0, alpha_float))
        reconstructed = background + alpha_float * direction
        projection_residuals.append(float(np.linalg.norm(observed - reconstructed)))
        if alpha_float <= 0.02:
            alpha[y, x] = 0
            output_rgb[y, x] = 0
            continue
        if alpha_float >= 0.98:
            continue
        alpha_value = int(round(alpha_float * 255.0))
        alpha[y, x] = np.uint8(max(1, min(254, alpha_value)))
        partial_count += 1
        if alpha_float < 0.12:
            decontaminated = foreground
        else:
            decontaminated = (observed - (1.0 - alpha_float) * background) / alpha_float
            decontaminated = 0.75 * np.clip(decontaminated, 0.0, 255.0) + 0.25 * foreground
        output_rgb[y, x] = np.rint(np.clip(decontaminated, 0.0, 255.0)).astype(np.uint8)

    rgba = np.dstack([output_rgb, alpha])
    opaque = alpha == 255
    transparent = alpha == 0
    partial = (alpha > 0) & (alpha < 255)
    rgb_changed = np.any(output_rgb != rgb_u8, axis=2)
    metrics = {
        "luma_floor": luma_floor,
        "chroma_limit": chroma_limit,
        "canvas": [int(rgb_u8.shape[1]), int(rgb_u8.shape[0])],
        "checker_candidate_pixels": int(np.count_nonzero(checker_candidate)),
        "border_connected_background_pixels": int(np.count_nonzero(border_background)),
        "enclosed_candidate_component_count": len(components),
        "accepted_enclosed_component_count": accepted_components,
        "accepted_enclosed_component_pixels": accepted_component_pixels,
        "definite_background_pixels": int(np.count_nonzero(definite_background)),
        "transparent_pixels": int(np.count_nonzero(transparent)),
        "partial_alpha_pixels": int(np.count_nonzero(partial)),
        "opaque_pixels": int(np.count_nonzero(opaque)),
        "alpha_bbox": list(bbox_for_alpha(alpha)),
        "rgb_changed_pixels_total": int(np.count_nonzero(rgb_changed)),
        "rgb_changed_transparent_pixels": int(np.count_nonzero(rgb_changed & transparent)),
        "rgb_changed_partial_pixels": int(np.count_nonzero(rgb_changed & partial)),
        "rgb_changed_opaque_pixels": int(np.count_nonzero(rgb_changed & opaque)),
        "trimap_unknown_pixels": int(np.count_nonzero(unknown)),
        "confident_foreground_seed_pixels": int(
            np.count_nonzero(confident_foreground)
        ),
        "trimap_partial_solved_pixels": partial_count,
        "trimap_missing_neighbour_count": missing_neighbour_count,
        "projection_residual_mean": float(np.mean(projection_residuals)) if projection_residuals else 0.0,
        "projection_residual_p95": float(np.quantile(projection_residuals, 0.95)) if projection_residuals else 0.0,
        "projection_residual_max": float(np.max(projection_residuals)) if projection_residuals else 0.0,
    }
    return rgba, metrics, components, definite_background


def composite(rgba: Image.Image, colour: tuple[int, int, int]) -> Image.Image:
    background = Image.new("RGBA", rgba.size, colour + (255,))
    return Image.alpha_composite(background, rgba).convert("RGB")


def protected_roi_metrics(
    source_rgb: np.ndarray,
    final_rgba: np.ndarray,
    variants: dict[int, np.ndarray],
) -> list[dict]:
    rois = {
        "face_hair": (340, 25, 610, 325),
        "brace_hand": (90, 315, 305, 585),
        "terminal_and_other_hand": (440, 255, 835, 630),
        "white_shirt": (330, 215, 625, 650),
        "seat_frame": (80, 285, 390, 1320),
    }
    luma = np.mean(source_rgb.astype(np.float64), axis=2)
    chroma = np.max(source_rgb, axis=2).astype(np.int16) - np.min(source_rgb, axis=2).astype(np.int16)
    strong_foreground = (luma < 225.0) | (chroma > 12)
    base_alpha = final_rgba[:, :, 3]
    base_rgb = final_rgba[:, :, :3]
    rows: list[dict] = []
    for name, (x0, y0, x1, y1) in rois.items():
        slices = np.s_[y0:y1, x0:x1]
        strong = strong_foreground[slices]
        alpha = base_alpha[slices]
        rgb_same = np.all(base_rgb[slices] == source_rgb[slices], axis=2)
        row = {
            "roi": name,
            "bbox": [x0, y0, x1 - 1, y1 - 1],
            "strong_foreground_pixels": int(np.count_nonzero(strong)),
            "strong_foreground_alpha_zero": int(np.count_nonzero(strong & (alpha == 0))),
            "strong_foreground_alpha_partial": int(np.count_nonzero(strong & (alpha > 0) & (alpha < 255))),
            "strong_foreground_rgb_changed": int(np.count_nonzero(strong & ~rgb_same)),
            "all_partial_alpha_pixels": int(np.count_nonzero((alpha > 0) & (alpha < 255))),
        }
        for threshold, variant_rgba in variants.items():
            variant_alpha = variant_rgba[:, :, 3][slices]
            row[f"alpha_diff_pixels_vs_L{threshold}"] = int(np.count_nonzero(alpha != variant_alpha))
            row[f"strong_foreground_alpha_diff_vs_L{threshold}"] = int(
                np.count_nonzero(strong & (alpha != variant_alpha))
            )
        rows.append(row)
    return rows


def write_tsv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    source = args.source.resolve()
    output_dir = args.output_dir.resolve()
    if sha256(source) != LOCKED_SOURCE_SHA256:
        raise SystemExit("source SHA-256 does not match the locked B06 Call01 raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    source_image = Image.open(source).convert("RGB")
    source_rgb = np.asarray(source_image, dtype=np.uint8)
    variants: dict[int, np.ndarray] = {}
    variant_metrics: dict[int, dict] = {}
    base_components: list[Component] = []
    for threshold in STABILITY_LUMA:
        rgba, metrics, components, _ = recover(source_rgb, threshold, BASE_CHROMA)
        variants[threshold] = rgba
        variant_metrics[threshold] = metrics
        if threshold == BASE_LUMA:
            base_components = components

    final_rgba = variants[BASE_LUMA]
    final_metrics = variant_metrics[BASE_LUMA]
    final_image = Image.fromarray(final_rgba, mode="RGBA")
    master_path = output_dir / "JICUN_B06_CHEST_GUIDE_SEAT_EGRESS_RGBA_MASTER_DETERMINISTIC_V1.png"
    final_image.save(master_path, optimize=False)

    final_image.resize((512, 768), Image.Resampling.LANCZOS).save(
        output_dir / "JICUN_B06_RGBA_MASTER_50PCT_QA.png"
    )
    alpha_image = Image.fromarray(final_rgba[:, :, 3], mode="L")
    alpha_image.save(output_dir / "JICUN_B06_ALPHA_MASK_100PCT_QA.png")
    alpha_image.resize((512, 768), Image.Resampling.LANCZOS).save(
        output_dir / "JICUN_B06_ALPHA_MASK_50PCT_QA.png"
    )

    qa_colours = {
        "DARK": (7, 15, 26),
        "LIGHT": (238, 236, 228),
        "SATURATED_MAGENTA": (255, 0, 160),
    }
    for label, colour in qa_colours.items():
        full = composite(final_image, colour)
        full.save(output_dir / f"JICUN_B06_{label}_BG_100PCT_QA.png")
        full.resize((512, 768), Image.Resampling.LANCZOS).save(
            output_dir / f"JICUN_B06_{label}_BG_50PCT_QA.png"
        )

    stability_rows: list[dict] = []
    base_alpha = final_rgba[:, :, 3].astype(np.int16)
    for threshold in STABILITY_LUMA:
        variant = variants[threshold]
        variant_alpha = variant[:, :, 3].astype(np.int16)
        difference = np.abs(base_alpha - variant_alpha)
        row = dict(variant_metrics[threshold])
        row.update(
            {
                f"alpha_diff_pixels_vs_L{BASE_LUMA}": int(np.count_nonzero(difference)),
                f"alpha_abs_diff_mean_vs_L{BASE_LUMA}": float(np.mean(difference)),
                f"alpha_abs_diff_p95_nonzero_vs_L{BASE_LUMA}": float(
                    np.quantile(difference[difference > 0], 0.95)
                )
                if np.any(difference > 0)
                else 0.0,
                f"alpha_abs_diff_max_vs_L{BASE_LUMA}": int(np.max(difference)),
            }
        )
        stability_rows.append(row)
    write_tsv(output_dir / "threshold-stability.tsv", stability_rows)

    component_rows: list[dict] = []
    for component in sorted(base_components, key=lambda item: item.area, reverse=True):
        component_rows.append(
            {
                "component_id": component.component_id,
                "area": component.area,
                "bbox": ",".join(str(value) for value in component.bbox),
                "mean_luma": component.mean_luma,
                "std_luma": component.std_luma,
                "mean_chroma": component.mean_chroma,
                "checker_luma_fraction": component.checker_luma_fraction,
                "low_chroma_fraction": component.low_chroma_fraction,
                "accepted_as_enclosed_background": str(
                    component.accepted_as_enclosed_background
                ).lower(),
            }
        )
    write_tsv(output_dir / "enclosed-components.tsv", component_rows)

    roi_rows = protected_roi_metrics(source_rgb, final_rgba, variants)
    write_tsv(output_dir / "protected-roi-metrics.tsv", roi_rows)

    hard_gate_failures: list[str] = []
    if final_metrics["rgb_changed_opaque_pixels"] != 0:
        hard_gate_failures.append("opaque subject RGB changed")
    for row in roi_rows:
        if row["strong_foreground_alpha_zero"] != 0:
            hard_gate_failures.append(f"{row['roi']} strong foreground was erased")
        if row["strong_foreground_rgb_changed"] != row["strong_foreground_alpha_partial"]:
            hard_gate_failures.append(
                f"{row['roi']} strong foreground RGB changed outside the partial edge band"
            )
    alpha_bboxes = {
        tuple(metrics["alpha_bbox"]) for metrics in variant_metrics.values()
    }
    if len(alpha_bboxes) != 1:
        hard_gate_failures.append("alpha bounds change across stability thresholds")
    for threshold, variant in variants.items():
        difference = np.abs(
            final_rgba[:, :, 3].astype(np.int16)
            - variant[:, :, 3].astype(np.int16)
        )
        if float(np.mean(difference)) > 0.10:
            hard_gate_failures.append(
                f"threshold L{threshold} mean alpha drift exceeds 0.10/255"
            )

    report = {
        "schema_id": "C01_B06_JICUN_DETERMINISTIC_CHECKER_ALPHA_SALVAGE_V1",
        "source": {
            "path": str(source),
            "sha256": sha256(source),
            "mode": "RGB",
            "size": list(source_image.size),
        },
        "method": {
            "imagegen_calls": 0,
            "global_white_key": False,
            "base_luma_floor": BASE_LUMA,
            "base_chroma_limit": BASE_CHROMA,
            "border_connectivity": 4,
            "trimap_radius": TRIMAP_RADIUS,
            "foreground_seed_max_luma": FOREGROUND_SEED_MAX_LUMA,
            "foreground_seed_min_chroma": FOREGROUND_SEED_MIN_CHROMA,
            "foreground_donor_inset": FOREGROUND_DONOR_INSET,
            "enclosed_component_rule": {
                "min_area": ENCLOSED_MIN_AREA,
                "max_mean_chroma": ENCLOSED_MAX_MEAN_CHROMA,
                "min_checker_luma_fraction": ENCLOSED_MIN_CHECKER_LUMA_FRACTION,
            },
            "stability_luma_thresholds": list(STABILITY_LUMA),
        },
        "final_metrics": final_metrics,
        "threshold_metrics": variant_metrics,
        "protected_roi_metrics": roi_rows,
        "hard_gate_failures": hard_gate_failures,
        "machine_gate": "PASS_FOR_VISUAL_QA" if not hard_gate_failures else "FAIL_STOP",
        "candidate_only": True,
        "user_visual_acceptance": False,
        "runtime_allowed": False,
        "canon_modified": False,
        "godot_binding_modified": False,
        "master": {
            "path": str(master_path),
            "sha256": sha256(master_path),
            "mode": "RGBA",
            "size": list(final_image.size),
        },
    }
    (output_dir / "salvage-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not hard_gate_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
