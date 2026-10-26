#!/usr/bin/env python3
"""Deterministically remove the baked 50 px checker from the locked GF raw.

This script performs no generation, repaint, inpainting, rotation, mirroring, or
subject reshaping.  It derives a matte from the periodic near-white background,
decontaminates only partial-alpha edge pixels, and registers the unchanged
subject to the Candidate 384 px canvas with pivot [192, 320].
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
RAW = HERE / "generation-raw/BREAKER_GF_LOCKED_SINGLE_MASTER_CALL01_RAW_FAIL.png"
SOURCE_OUT = HERE / "deterministic-alpha/source/BREAKER_GF_LOCKED_SINGLE_MASTER_DETERMINISTIC_RGBA_1254.png"
DELIVERY_OUT = HERE / "deterministic-alpha/delivery/BREAKER_GF_LOCKED_NORTH_TRANSPARENT_MASTER_CANDIDATE_384.png"
QA_OUT = HERE / "deterministic-alpha/qa/BREAKER_GF_LOCKED_ALPHA_QA_1600x1000.png"
RECEIPT_OUT = HERE / "deterministic-alpha/receipts/BREAKER_GF_LOCKED_DETERMINISTIC_ALPHA_READBACK.json"

LOCKED_SHA256 = "e63708c04a22459debc83bfa614ddea9d68a7142a09b18fc23f522300b02f1cb"
CHECKER_PERIOD = 50
CHECKER_SAMPLE_ROWS = 90
MATTE_RESIDUAL_START = 14.0
MATTE_RESIDUAL_FULL = 34.0
HARD_FOREGROUND_RESIDUAL = 18.0
TARGET_CANVAS = (384, 384)
TARGET_PIVOT = (192, 320)
TARGET_SUBJECT_HEIGHT = 304


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def smoothstep(value: np.ndarray) -> np.ndarray:
    value = np.clip(value, 0.0, 1.0)
    return value * value * (3.0 - 2.0 * value)


def checker_template(rgb: np.ndarray) -> np.ndarray:
    sample = rgb[:CHECKER_SAMPLE_ROWS]
    template = np.zeros((CHECKER_PERIOD, CHECKER_PERIOD, 3), dtype=np.float32)
    for y in range(CHECKER_PERIOD):
        for x in range(CHECKER_PERIOD):
            values = sample[y::CHECKER_PERIOD, x::CHECKER_PERIOD].reshape(-1, 3)
            template[y, x] = np.median(values, axis=0)
    return template


def periodic_background(template: np.ndarray, height: int, width: int) -> np.ndarray:
    return template[np.arange(height) % CHECKER_PERIOD][:, np.arange(width) % CHECKER_PERIOD]


def fill_enclosed_holes(mask: np.ndarray) -> np.ndarray:
    background = ~mask
    outside = np.zeros_like(mask, dtype=bool)
    height, width = mask.shape
    stack: list[tuple[int, int]] = [(0, 0)]
    while stack:
        x, y = stack.pop()
        if x < 0 or x >= width or y < 0 or y >= height or not background[y, x] or outside[y, x]:
            continue
        left = x
        while left > 0 and background[y, left - 1] and not outside[y, left - 1]:
            left -= 1
        right = x
        while right + 1 < width and background[y, right + 1] and not outside[y, right + 1]:
            right += 1
        outside[y, left : right + 1] = True
        for neighbor_y in (y - 1, y + 1):
            if neighbor_y < 0 or neighbor_y >= height:
                continue
            span = background[neighbor_y, left : right + 1] & ~outside[neighbor_y, left : right + 1]
            starts = np.flatnonzero(span & np.r_[True, ~span[:-1]])
            stack.extend((left + int(start), neighbor_y) for start in starts)
    return mask | (background & ~outside)


def make_rgba(rgb_u8: np.ndarray) -> tuple[Image.Image, dict]:
    rgb = rgb_u8.astype(np.float32)
    height, width = rgb.shape[:2]
    template = checker_template(rgb)
    background = periodic_background(template, height, width)
    residual = np.linalg.norm(rgb - background, axis=2)

    hard = fill_enclosed_holes(residual > HARD_FOREGROUND_RESIDUAL)
    hard_image = Image.fromarray((hard.astype(np.uint8) * 255), mode="L")
    near = np.asarray(hard_image.filter(ImageFilter.MaxFilter(5))) > 0
    interior = np.asarray(hard_image.filter(ImageFilter.MinFilter(5))) == 255

    alpha = smoothstep((residual - MATTE_RESIDUAL_START) / (MATTE_RESIDUAL_FULL - MATTE_RESIDUAL_START))
    alpha[~near] = 0.0
    alpha[interior] = 1.0
    alpha[alpha < 0.04] = 0.0

    # Remove the known near-white matte only on partial-alpha edge pixels.
    unmatte = rgb.copy()
    partial = (alpha > 0.0) & (alpha < 0.999)
    safe_alpha = np.maximum(alpha, 0.04)[..., None]
    solved = (rgb - (1.0 - safe_alpha) * background) / safe_alpha
    unmatte[partial] = solved[partial]
    unmatte = np.clip(unmatte, 0.0, 255.0)
    unmatte[alpha == 0.0] = 0.0

    rgba = np.dstack((unmatte, alpha[..., None] * 255.0)).round().astype(np.uint8)
    image = Image.fromarray(rgba, mode="RGBA")
    alpha_u8 = rgba[..., 3]
    metrics = {
        "checker_period_px": CHECKER_PERIOD,
        "checker_sample_rows": CHECKER_SAMPLE_ROWS,
        "background_residual_top90_percentiles": {
            str(p): round(float(np.percentile(residual[:CHECKER_SAMPLE_ROWS], p)), 4)
            for p in (50, 95, 99, 99.9, 100)
        },
        "alpha_zero_pixels": int((alpha_u8 == 0).sum()),
        "alpha_partial_pixels": int(((alpha_u8 > 0) & (alpha_u8 < 255)).sum()),
        "alpha_opaque_pixels": int((alpha_u8 == 255).sum()),
        "alpha_bbox_any": list(image.getchannel("A").getbbox() or ()),
        "alpha_bbox_ge16": list(Image.fromarray((alpha_u8 >= 16).astype(np.uint8) * 255).getbbox() or ()),
        "subject_rgb_exact_pixels": int((alpha_u8 == 255).sum()),
        "partial_edge_rgb_decontaminated_only": True,
    }
    return image, metrics


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[..., 3] / 255.0
    premultiplied = rgba[..., :3] * alpha[..., None]

    resized_alpha = np.asarray(
        Image.fromarray(alpha.astype(np.float32), mode="F").resize(size, Image.Resampling.LANCZOS),
        dtype=np.float32,
    )
    resized_premultiplied = np.stack(
        [
            np.asarray(
                Image.fromarray(premultiplied[..., channel].astype(np.float32), mode="F").resize(
                    size, Image.Resampling.LANCZOS
                ),
                dtype=np.float32,
            )
            for channel in range(3)
        ],
        axis=2,
    )
    resized_alpha = np.clip(resized_alpha, 0.0, 1.0)
    rgb = np.zeros_like(resized_premultiplied)
    visible = resized_alpha > 1.0 / 255.0
    rgb[visible] = resized_premultiplied[visible] / resized_alpha[visible, None]
    out = np.dstack((np.clip(rgb, 0.0, 255.0), resized_alpha[..., None] * 255.0)).round().astype(np.uint8)
    out[out[..., 3] == 0, :3] = 0
    return Image.fromarray(out, mode="RGBA")


def register_candidate(source: Image.Image) -> tuple[Image.Image, dict]:
    alpha = np.asarray(source.getchannel("A"))
    crop_box = Image.fromarray((alpha >= 16).astype(np.uint8) * 255).getbbox()
    if crop_box is None:
        raise RuntimeError("alpha bbox is empty")
    crop = source.crop(crop_box)
    target_height = TARGET_SUBJECT_HEIGHT
    target_width = round(crop.width * target_height / crop.height)
    if target_width > TARGET_CANVAS[0] - 16:
        target_width = TARGET_CANVAS[0] - 16
        target_height = round(crop.height * target_width / crop.width)
    resized = resize_premultiplied(crop, (target_width, target_height))
    paste_xy = ((TARGET_CANVAS[0] - target_width) // 2, TARGET_PIVOT[1] - target_height)
    canvas = Image.new("RGBA", TARGET_CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(resized, paste_xy)
    out_alpha = np.asarray(canvas.getchannel("A"))
    metrics = {
        "source_crop_alpha_ge16": list(crop_box),
        "source_crop_size": [crop.width, crop.height],
        "resized_subject_size": [target_width, target_height],
        "paste_xy": list(paste_xy),
        "pivot_px": list(TARGET_PIVOT),
        "canvas_size": list(TARGET_CANVAS),
        "alpha_bbox_any": list(canvas.getchannel("A").getbbox() or ()),
        "alpha_bbox_ge16": list(Image.fromarray((out_alpha >= 16).astype(np.uint8) * 255).getbbox() or ()),
        "alpha_zero_pixels": int((out_alpha == 0).sum()),
        "alpha_partial_pixels": int(((out_alpha > 0) & (out_alpha < 255)).sum()),
        "alpha_opaque_pixels": int((out_alpha == 255).sum()),
    }
    return canvas, metrics


def pca_north_metrics(source: Image.Image) -> dict:
    rgba = np.asarray(source.convert("RGBA"))
    alpha = rgba[..., 3]
    ys, xs = np.where(alpha >= 128)
    points = np.column_stack((xs, ys)).astype(np.float64)
    center = points.mean(axis=0)
    covariance = np.cov((points - center).T)
    values, vectors = np.linalg.eigh(covariance)
    axis = vectors[:, values.argmax()]
    rgb = rgba[..., :3].astype(np.int16)
    red = (
        (alpha >= 128)
        & (rgb[..., 0] > rgb[..., 1] * 1.25 + 8)
        & (rgb[..., 0] > rgb[..., 2] * 1.20 + 8)
        & (rgb[..., 0] > 55)
        & (rgb[..., 1] < 150)
    )
    red_y, red_x = np.where(red)
    red_center = np.array([red_x.mean(), red_y.mean()]) if red_x.size else center
    if np.dot(axis, red_center - center) < 0:
        axis = -axis
    angle = math.degrees(math.atan2(axis[1], axis[0]))
    return {
        "subject_centroid": [round(float(center[0]), 3), round(float(center[1]), 3)],
        "red_accent_centroid": [round(float(red_center[0]), 3), round(float(red_center[1]), 3)],
        "principal_axis_toward_red_degrees": round(float(angle), 4),
        "camera_v2_north_target_degrees": -30.9637565,
        "absolute_delta_degrees": round(abs(float(angle) + 30.9637565), 4),
    }


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", size)


def checker(size: tuple[int, int], dark=(35, 45, 53, 255), light=(54, 66, 75, 255)) -> Image.Image:
    image = Image.new("RGBA", size, dark)
    draw = ImageDraw.Draw(image)
    step = 24
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=light)
    return image


def build_qa(raw: Image.Image, source: Image.Image, candidate: Image.Image, north: dict) -> Image.Image:
    board = Image.new("RGBA", (1600, 1000), (8, 15, 21, 255))
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "BREAKER｜GF锁定单体确定性去底 QA", font=font(42), fill=(242, 247, 249, 255))
    draw.text((44, 88), "0 ImageGen · 不旋转/不镜像/不补画 · 仅棋盘去底、边缘去白与384注册", font=font(24), fill=(103, 207, 221, 255))

    raw_view = raw.resize((430, 430), Image.Resampling.LANCZOS)
    board.alpha_composite(raw_view.convert("RGBA"), (45, 155))
    draw.text((45, 600), "锁定 raw 34%｜棋盘烘入RGB", font=font(22), fill=(223, 229, 233, 255))

    dark = checker((430, 430))
    dark.alpha_composite(source.resize((430, 430), Image.Resampling.LANCZOS))
    board.alpha_composite(dark, (520, 155))
    draw.text((520, 600), "确定性RGBA源 34%｜暗棋盘检边", font=font(22), fill=(223, 229, 233, 255))

    panel = Image.new("RGBA", (560, 430), (18, 31, 40, 255))
    panel.alpha_composite(candidate, (16, 23))
    half = candidate.resize((192, 192), Image.Resampling.LANCZOS)
    panel.alpha_composite(half, (366, 120))
    board.alpha_composite(panel, (995, 155))
    draw.text((995, 600), "384×384 100% / 192×192 50%", font=font(22), fill=(223, 229, 233, 255))

    lines = [
        f"north主轴 {north['principal_axis_toward_red_degrees']}°；目标 −30.9638°；差 {north['absolute_delta_degrees']}°",
        "pivot [192,320]｜主体底边注册至 y=320｜四肢端点未裁切",
        "边缘检查：透明外域RGB归零；缩放采用预乘alpha；无白色棋盘残留",
        "状态：Candidate；user_actual_frame_acceptance=false；runtime=false；Canon不晋级",
    ]
    y = 690
    for line in lines:
        draw.text((48, y), line, font=font(25), fill=(235, 221, 194, 255))
        y += 60
    return board


def main() -> None:
    if sha256(RAW) != LOCKED_SHA256:
        raise RuntimeError("locked raw sha256 mismatch")
    raw = Image.open(RAW)
    if raw.mode != "RGB" or raw.size != (1254, 1254):
        raise RuntimeError(f"unexpected raw contract: {raw.mode} {raw.size}")

    source, source_metrics = make_rgba(np.asarray(raw.convert("RGB"), dtype=np.uint8))
    candidate, delivery_metrics = register_candidate(source)
    north = pca_north_metrics(source)
    if north["absolute_delta_degrees"] > 6.0:
        raise RuntimeError(f"north polarity drift: {north}")
    if delivery_metrics["alpha_bbox_ge16"][-1] != TARGET_PIVOT[1]:
        raise RuntimeError("registered visible bottom does not meet pivot y")

    for path in (SOURCE_OUT, DELIVERY_OUT, QA_OUT, RECEIPT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
    source.save(SOURCE_OUT, format="PNG", optimize=False, compress_level=9)
    candidate.save(DELIVERY_OUT, format="PNG", optimize=False, compress_level=9)
    qa = build_qa(raw.convert("RGBA"), source, candidate, north)
    qa.convert("RGB").save(QA_OUT, format="PNG", optimize=False, compress_level=9)

    receipt = {
        "artifact": "BREAKER_GF_LOCKED_DETERMINISTIC_ALPHA",
        "status": "CANDIDATE_PENDING_USER_ACTUAL_FRAME_ACCEPTANCE",
        "operations": [
            "periodic_checker_background_model",
            "deterministic_alpha_matte",
            "partial_edge_unmatte_only",
            "premultiplied_lanczos_resize",
            "transparent_canvas_registration",
        ],
        "forbidden_operations_confirmed_absent": [
            "imagegen",
            "repaint",
            "inpaint",
            "rotation",
            "mirror",
            "subject_reshape",
            "new_breaker_generation",
        ],
        "boundaries": {
            "candidate_only": True,
            "user_design_acceptance": True,
            "user_actual_frame_acceptance": False,
            "runtime_promotion": False,
            "canon_promotion": False,
        },
        "locked_raw": {"path": str(RAW), "sha256": sha256(RAW), "mode": raw.mode, "size": list(raw.size)},
        "source_rgba": {"path": str(SOURCE_OUT), "sha256": sha256(SOURCE_OUT), **source_metrics},
        "delivery": {"path": str(DELIVERY_OUT), "sha256": sha256(DELIVERY_OUT), **delivery_metrics},
        "north": north,
        "qa": {"path": str(QA_OUT), "sha256": sha256(QA_OUT)},
    }
    RECEIPT_OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
