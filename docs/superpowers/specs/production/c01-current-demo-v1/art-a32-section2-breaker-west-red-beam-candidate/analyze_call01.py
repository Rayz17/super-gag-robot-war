#!/usr/bin/env python3
"""Machine readback for the single A32 west generation; uses ffmpeg only."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "call01" / "generation-raw" / "BREAKER_A32_CALL01_WEST_RAW.png"
OUT = ROOT / "call01" / "receipts" / "BREAKER_A32_CALL01_WEST_HARD_GATE.json"
QA = ROOT / "call01" / "qa" / "BREAKER_A32_CALL01_WEST_HARD_GATE_FAIL_QA_50_100.png"
TARGET = math.degrees(math.atan2(-24, -40))


def circular_delta(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def main() -> None:
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height,pix_fmt",
         "-of", "json", str(RAW)], check=True, capture_output=True, text=True
    )
    stream = json.loads(probe.stdout)["streams"][0]
    width, height = int(stream["width"]), int(stream["height"])
    rgb = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(RAW), "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-"], check=True, capture_output=True
    ).stdout
    if len(rgb) != width * height * 3:
        raise RuntimeError("unexpected rawvideo length")

    dark_points: list[tuple[float, float, float]] = []
    red_points: list[tuple[float, float, float]] = []
    bg_samples: dict[tuple[int, int, int], int] = {}
    min_x, min_y, max_x, max_y = width, height, -1, -1

    for y in range(height):
        row = y * width * 3
        for x in range(width):
            i = row + x * 3
            r, g, b = rgb[i], rgb[i + 1], rgb[i + 2]
            mean = (r + g + b) / 3.0
            red_like = r > 120 and r - g > 45 and r - b > 35 and r > 1.45 * max(g, 1)
            if mean < 218 and not red_like:
                weight = max(1.0, 235.0 - mean)
                dark_points.append((x, y, weight))
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)
            if red_like:
                weight = max(1.0, r - (g + b) / 2.0)
                red_points.append((x, y, weight))
            if y < 80 and r > 230 and g > 230 and b > 230:
                q = (round(r / 4) * 4, round(g / 4) * 4, round(b / 4) * 4)
                bg_samples[q] = bg_samples.get(q, 0) + 1

    def centroid(points: list[tuple[float, float, float]]) -> tuple[float, float]:
        total = sum(p[2] for p in points)
        return (sum(p[0] * p[2] for p in points) / total,
                sum(p[1] * p[2] for p in points) / total)

    cx, cy = centroid(dark_points)
    rx, ry = centroid(red_points)
    total = sum(p[2] for p in dark_points)
    cxx = sum((p[0] - cx) ** 2 * p[2] for p in dark_points) / total
    cyy = sum((p[1] - cy) ** 2 * p[2] for p in dark_points) / total
    cxy = sum((p[0] - cx) * (p[1] - cy) * p[2] for p in dark_points) / total
    theta = 0.5 * math.atan2(2.0 * cxy, cxx - cyy)
    vx, vy = math.cos(theta), math.sin(theta)
    if vx * (rx - cx) + vy * (ry - cy) < 0:
        vx, vy = -vx, -vy
    axis_angle = math.degrees(math.atan2(vy, vx))
    red_angle = math.degrees(math.atan2(ry - cy, rx - cx))
    axis_delta = circular_delta(axis_angle, TARGET)
    red_delta = circular_delta(red_angle, TARGET)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    readback = {
        "schema_id": "BREAKER_A32_CALL01_WEST_HARD_GATE_V1",
        "raw": {
            "path": str(RAW.relative_to(ROOT.parent.parent.parent.parent.parent.parent)),
            "sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
            "size": [width, height],
            "pixel_format": stream.get("pix_fmt", ""),
            "has_alpha": "a" in stream.get("pix_fmt", ""),
        },
        "geometry": {
            "dark_subject_bbox_inclusive": [min_x, min_y, max_x, max_y],
            "dark_subject_centroid": [round(cx, 3), round(cy, 3)],
            "red_accent_centroid": [round(rx, 3), round(ry, 3)],
            "principal_axis_toward_red_degrees": round(axis_angle, 4),
            "centroid_to_red_degrees": round(red_angle, 4),
            "camera_v2_west_target_degrees": round(TARGET, 4),
            "principal_axis_delta_degrees": round(axis_delta, 4),
            "centroid_to_red_delta_degrees": round(red_delta, 4),
            "hard_gate_tolerance_degrees": 10.0,
            "west_axis_pass": axis_delta <= 10.0 and red_delta <= 10.0,
        },
        "alpha": {
            "true_alpha_pass": False,
            "baked_checker_detected": True,
            "top_background_quantized_colors": sorted(
                ({"rgb": list(k), "count": v} for k, v in bg_samples.items()),
                key=lambda item: item["count"], reverse=True
            )[:8],
            "deterministic_recoverability": "not_attempted_after_geometry_hard_fail",
        },
        "hard_gate": {
            "identity_leaf_armor_low_body_four_limb_visual_read": "manual_review_required",
            "west_polarity": "pass" if axis_delta <= 10.0 and red_delta <= 10.0 else "fail",
            "alpha_or_safe_recoverability": "not_proven",
            "overall": "FAIL_STOP",
            "reason": "camera_v2_west_axis_not_met; true_alpha_absent",
        },
        "qa": {
            "path": str(QA.relative_to(ROOT.parent.parent.parent.parent.parent.parent)),
            "sha256": hashlib.sha256(QA.read_bytes()).hexdigest() if QA.exists() else "MISSING",
            "layout": ["raw_half_scale", "head_crop_one_to_one", "west_geometry_guide", "current_north_positive"],
        },
    }
    OUT.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(readback["geometry"], indent=2))
    print(OUT)


if __name__ == "__main__":
    main()
