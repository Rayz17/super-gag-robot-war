#!/usr/bin/env python3
"""Deterministic Alpha, scale, pivot, and QA for Brave Fist south Call01.

No visible mecha geometry is drawn or reconstructed here.  The script consumes
the single ImageGen raw, removes only its border-connected checker background,
despills the anti-aliased edge, scales the intact subject, and builds QA boards.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


RAW_SHA = "09395f3d1bb628fae21ae37c9ec3c7793413823b4b72a562d1d93bcba56c6afd"
SOURCE_SHA = "9bda4674457b71968c8923bcd231a77b3bf64cb5214e22186756a58707a15217"
PIVOT = (128, 224)
FOOTPRINT = (2, 2)
TARGET_VISIBLE_HEIGHT = 208
CORE_DISTANCE = 4.0

SCRIPT = Path(__file__).resolve()
CALL_DIR = SCRIPT.parents[1]
PROJECT = SCRIPT.parents[8]
RAW = CALL_DIR / "generation-raw" / "BRAVE_FIST_E03_IDLE_SOUTH_CALL01_RAW_RGB_1254.png"
SOURCE = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a33-section2-brave-fist-heavy-twin-fist-mane-crown-rework-candidate/delivery/BRAVE_FIST_A33_HEAVY_TWIN_FIST_MANE_CROWN_MASTER_USER_REVIEW_CANDIDATE.png"
MASTER = CALL_DIR / "masters" / "BRAVE_FIST_E03_IDLE_SOUTH_CALL01_RGBA_MASTER_1254.png"
SPRITE = CALL_DIR / "map-candidate" / "BRAVE_FIST_E03_IDLE_SOUTH_CAMERA_V2_CANDIDATE_RGBA_256.png"
QA = CALL_DIR / "qa"
QA_100 = QA / "100pct"
AUDIT = CALL_DIR / "receipts" / "CALL01_ALPHA_SCALE_MACHINE_AUDIT.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bbox(mask: np.ndarray) -> list[int] | None:
    y, x = np.nonzero(mask)
    if not len(x):
        return None
    return [int(x.min()), int(y.min()), int(x.max() + 1), int(y.max() + 1)]


def checker_model(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    source = rgb.astype(np.float32)
    gray = source.mean(axis=2)
    column = np.median(gray[5:20, :], axis=0)
    row = np.median(gray[:, 5:20], axis=1)
    refs = np.concatenate((column, row))
    dark = float(np.percentile(refs, 5))
    bright = float(np.percentile(refs, 95))
    mid = (dark + bright) / 2.0
    amp = (bright - dark) / 2.0
    if amp < 1.0:
        raise RuntimeError("checker amplitude is not separable")
    sx = np.clip((column - mid) / amp, -1.0, 1.0)
    sy = np.clip((row - mid) / amp, -1.0, 1.0)

    border = np.zeros(gray.shape, dtype=bool)
    border[:32] = True
    border[-32:] = True
    border[:, :32] = True
    border[:, -32:] = True
    choices = []
    for sign in (-1.0, 1.0):
        modeled_gray = mid + sign * amp * sy[:, None] * sx[None, :]
        modeled = np.repeat(modeled_gray[:, :, None], 3, axis=2)
        residual = np.max(np.abs(source - modeled), axis=2)
        score = float(np.percentile(residual[border], 99))
        choices.append((score, sign, modeled, residual))
    choices.sort(key=lambda item: item[0])
    score, sign, modeled, residual = choices[0]
    threshold = float(np.clip(score + 1.0, 3.0, 6.0))
    return modeled, residual, {
        "dark": dark,
        "bright": bright,
        "midpoint": mid,
        "amplitude": amp,
        "separable_sign": sign,
        "border_residual_p99": score,
        "background_threshold": threshold,
    }


def largest(mask: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if count < 2:
        raise RuntimeError("no foreground component")
    selected = int(np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1)
    keep = labels == selected
    return keep, {
        "foreground_component_count_before_keep_largest": int(count - 1),
        "kept_foreground_pixels": int(keep.sum()),
        "discarded_isolated_pixels": int(mask.sum() - keep.sum()),
    }


def extract_alpha(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, object]]:
    source = rgb.astype(np.float32)
    background, residual, model = checker_model(rgb)
    threshold = float(model["background_threshold"])
    candidate_background = residual <= threshold
    candidate_count, labels, candidate_stats, _ = cv2.connectedComponentsWithStats(
        candidate_background.astype(np.uint8), 8
    )
    border_labels = np.unique(np.concatenate((labels[0], labels[-1], labels[:, 0], labels[:, -1])))
    border_labels = border_labels[border_labels > 0]
    outer = np.isin(labels, border_labels)
    border_label_set = {int(v) for v in border_labels}

    # Real checker negative spaces can be fully enclosed by the two arms and
    # torso.  Remove only components that reproduce both checker parities and
    # remain nearly neutral; single-parity white/silver mecha highlights are
    # deliberately protected.
    enclosed_checker = np.zeros(candidate_background.shape, dtype=bool)
    enclosed_checker_records = []
    source_gray = source.mean(axis=2)
    source_chroma = source.max(axis=2) - source.min(axis=2)
    background_gray = background[:, :, 0]
    for label in range(1, candidate_count):
        if label in border_label_set:
            continue
        area = int(candidate_stats[label, cv2.CC_STAT_AREA])
        width = int(candidate_stats[label, cv2.CC_STAT_WIDTH])
        height = int(candidate_stats[label, cv2.CC_STAT_HEIGHT])
        if area < 40 or width < 6 or height < 6:
            continue
        component = labels == label
        dark_parity = component & (background_gray < model["midpoint"])
        bright_parity = component & (background_gray >= model["midpoint"])
        if int(dark_parity.sum()) < 10 or int(bright_parity.sum()) < 10:
            continue
        bright_minus_dark = float(source_gray[bright_parity].mean() - source_gray[dark_parity].mean())
        mean_chroma = float(source_chroma[component].mean())
        if bright_minus_dark >= 4.5 and mean_chroma <= 2.0:
            enclosed_checker |= component
            enclosed_checker_records.append(
                {
                    "area": area,
                    "bbox": [
                        int(candidate_stats[label, cv2.CC_STAT_LEFT]),
                        int(candidate_stats[label, cv2.CC_STAT_TOP]),
                        width,
                        height,
                    ],
                    "bright_minus_dark": bright_minus_dark,
                    "mean_chroma": mean_chroma,
                }
            )

    foreground, component_stats = largest(~(outer | enclosed_checker))

    distance = cv2.distanceTransform(foreground.astype(np.uint8), cv2.DIST_L2, 5)
    core = foreground & (distance >= CORE_DISTANCE)
    edge = foreground & ~core
    core_weight = core.astype(np.float32)
    blurred_weight = cv2.GaussianBlur(core_weight, (0, 0), 3.5)
    estimate = np.empty_like(source)
    for c in range(3):
        weighted = cv2.GaussianBlur(source[:, :, c] * core_weight, (0, 0), 3.5)
        estimate[:, :, c] = np.where(
            blurred_weight > 1e-5,
            weighted / np.maximum(blurred_weight, 1e-5),
            source[:, :, c],
        )

    cb = source - background
    fb = estimate - background
    fnorm = np.sum(fb * fb, axis=2)
    cnorm = np.sum(cb * cb, axis=2)
    dot = np.sum(cb * fb, axis=2)
    alpha_ls = dot / np.maximum(fnorm, 1e-6)
    cosine = dot / np.maximum(np.sqrt(fnorm * cnorm), 1e-6)
    reliable = (fnorm >= 900.0) & (cosine >= 0.80)
    # The binary foreground can include several pixels of resampled checker
    # fringe around a closed negative space.  Do not force those pixels opaque
    # merely because they are geometrically inside the provisional mask; use
    # their measured departure from the known checker instead.
    color_alpha = np.clip((residual - threshold) / max(24.0 - threshold, 1.0), 0.0, 1.0)
    alpha = np.where(reliable, np.clip(alpha_ls, 0.0, 1.0), color_alpha)
    alpha = np.maximum(alpha, color_alpha)
    alpha[core] = 1.0
    alpha[~foreground] = 0.0
    alpha[alpha < 0.02] = 0.0
    alpha[alpha > 0.98] = 1.0
    a8 = np.clip(np.rint(alpha * 255.0), 0, 255).astype(np.uint8)

    # Color-based matting can classify isolated near-white panel highlights as
    # one-pixel holes.  Restore every enclosed zero-Alpha component that does
    # not overlap one of the three independently checker-verified negative
    # spaces.  This preserves face/eye/crown/fist detail without filling the
    # actual arm/torso background openings.
    provisional_zero = a8 == 0
    pcount, plabels, _, _ = cv2.connectedComponentsWithStats(provisional_zero.astype(np.uint8), 8)
    pborder = {
        int(v)
        for v in np.unique(np.concatenate((plabels[0], plabels[-1], plabels[:, 0], plabels[:, -1])))
        if int(v)
    }
    restored_false_holes = np.zeros(a8.shape, dtype=bool)
    restored_false_hole_count = 0
    for label in range(1, pcount):
        if label in pborder:
            continue
        component = plabels == label
        if np.any(component & enclosed_checker):
            continue
        restored_false_holes |= component
        restored_false_hole_count += 1
    alpha[restored_false_holes] = 1.0
    a8[restored_false_holes] = 255

    out_rgb = rgb.copy()
    partial = (a8 > 0) & (a8 < 255)
    safe_a = np.maximum(alpha[:, :, None], 1e-4)
    unblend = (source - (1.0 - alpha[:, :, None]) * background) / safe_a
    unblend = np.minimum(np.maximum(unblend, estimate - 32.0), estimate + 32.0)
    unblend = np.clip(np.rint(unblend), 0, 255).astype(np.uint8)
    out_rgb[partial] = unblend[partial]
    out_rgb[a8 == 0] = 0
    rgba = np.dstack((out_rgb, a8))

    rgb_changed = np.any(out_rgb != rgb, axis=2) & (a8 > 0)
    core_changed = int(np.any(out_rgb[core] != rgb[core], axis=1).sum())
    opaque_changed = int(np.any(out_rgb[a8 == 255] != rgb[a8 == 255], axis=1).sum())

    transparent = a8 == 0
    nt, tl, _, _ = cv2.connectedComponentsWithStats(transparent.astype(np.uint8), 8)
    touching = set(int(v) for v in np.unique(np.concatenate((tl[0], tl[-1], tl[:, 0], tl[:, -1]))) if int(v))
    enclosed = [label for label in range(1, nt) if label not in touching]

    checker_match = (a8 >= 250) & (residual <= threshold)
    nc, cl, st, _ = cv2.connectedComponentsWithStats(checker_match.astype(np.uint8), 8)
    bad_checker = []
    bggray = background[:, :, 0]
    sgray = source.mean(axis=2)
    chroma = source.max(axis=2) - source.min(axis=2)
    for label in range(1, nc):
        area = int(st[label, cv2.CC_STAT_AREA])
        width = int(st[label, cv2.CC_STAT_WIDTH])
        height = int(st[label, cv2.CC_STAT_HEIGHT])
        if area < 64 or width < 16 or height < 16:
            continue
        m = cl == label
        lo = m & (bggray < model["midpoint"])
        hi = m & (bggray >= model["midpoint"])
        if lo.sum() < 20 or hi.sum() < 20:
            continue
        if float(sgray[hi].mean() - sgray[lo].mean()) >= 6.0 and float(chroma[m].mean()) <= 4.0:
            bad_checker.append({"area": area, "bbox": [int(st[label, 0]), int(st[label, 1]), width, height]})

    neutral_core = core & (source.min(axis=2) >= 235) & ((source.max(axis=2) - source.min(axis=2)) <= 8)
    audit = {
        "checker_model": model,
        "outer_background_label_count": int(len(border_labels)),
        "enclosed_checker_background_component_count_removed": int(len(enclosed_checker_records)),
        "enclosed_checker_background_components_removed": enclosed_checker_records,
        "restored_nonchecker_enclosed_highlight_component_count": int(restored_false_hole_count),
        "restored_nonchecker_enclosed_highlight_pixel_count": int(restored_false_holes.sum()),
        **component_stats,
        "foreground_bbox_exclusive": bbox(foreground),
        "alpha_bbox_exclusive": bbox(a8 > 0),
        "transparent_pixel_count": int((a8 == 0).sum()),
        "partial_alpha_pixel_count": int(((a8 > 0) & (a8 < 255)).sum()),
        "opaque_pixel_count": int((a8 == 255).sum()),
        "outside_foreground_nontransparent_pixels": int(np.count_nonzero(a8[~foreground])),
        "transparent_component_count_8_connected": int(nt - 1),
        "enclosed_transparent_component_count": int(len(enclosed)),
        "internal_core_rgb_changed_pixels": core_changed,
        "opaque_rgb_changed_pixels": opaque_changed,
        "edge_rgb_changed_pixels": int(rgb_changed.sum()),
        "edge_rgb_changed_bbox_exclusive": bbox(rgb_changed),
        "edge_band_pixels": int(edge.sum()),
        "neutral_white_core_preserved_pixels": int(neutral_core.sum()),
        "opaque_checker_component_count": int(len(bad_checker)),
        "opaque_checker_components": bad_checker,
        "transparent_rgb_nonzero_pixels": int(np.any(out_rgb[a8 == 0] != 0, axis=1).sum()),
    }
    return rgba, foreground, core, audit


def premul_resize(rgba: np.ndarray, size: tuple[int, int], alpha_zero: int = 5) -> np.ndarray:
    a = rgba[:, :, 3].astype(np.float32) / 255.0
    rgb = rgba[:, :, :3].astype(np.float32) / 255.0
    pre = rgb * a[:, :, None]
    resample = Image.Resampling.LANCZOS
    ra = np.array(Image.fromarray(a, "F").resize(size, resample), dtype=np.float32)
    rp = np.stack(
        [np.array(Image.fromarray(pre[:, :, c], "F").resize(size, resample), dtype=np.float32) for c in range(3)],
        axis=2,
    )
    ra = np.clip(ra, 0.0, 1.0)
    rr = np.zeros_like(rp)
    valid = ra > 1e-6
    rr[valid] = rp[valid] / ra[valid, None]
    out = np.dstack((np.clip(np.rint(rr * 255), 0, 255).astype(np.uint8), np.clip(np.rint(ra * 255), 0, 255).astype(np.uint8)))
    out[out[:, :, 3] <= alpha_zero] = 0
    return out


def register(master: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    mb = bbox(master[:, :, 3] > 0)
    nominal = int(round(master.shape[0] * TARGET_VISIBLE_HEIGHT / (mb[3] - mb[1])))
    options = []
    for side in range(nominal - 14, nominal + 15):
        resized = premul_resize(master, (side, side))
        rb = bbox(resized[:, :, 3] > 0)
        if rb:
            options.append((abs((rb[3] - rb[1]) - TARGET_VISIBLE_HEIGHT), abs(side - nominal), side, resized, rb))
    options.sort(key=lambda v: (v[0], v[1], v[2]))
    error, _, side, resized, rb = options[0]
    if error:
        raise RuntimeError(f"could not reach target visible height: side={side} bbox={rb}")
    ox = int(round(PIVOT[0] - (rb[0] + rb[2]) / 2.0))
    oy = int(PIVOT[1] - rb[3])
    if ox < 0 or oy < 0 or ox + side > 256 or oy + side > 256:
        raise RuntimeError(f"registered canvas clips subject: side={side} offset={ox,oy}")
    canvas = np.zeros((256, 256, 4), dtype=np.uint8)
    canvas[oy : oy + side, ox : ox + side] = resized
    cb = bbox(canvas[:, :, 3] > 0)
    return canvas, {
        "full_canvas_resized_side": int(side),
        "scale_from_master": float(side / master.shape[0]),
        "placement_offset": [ox, oy],
        "alpha_bbox_exclusive": cb,
        "visible_size": [cb[2] - cb[0], cb[3] - cb[1]],
        "pivot": list(PIVOT),
        "footprint": list(FOOTPRINT),
        "scale": [1, 1],
        "clipped_alpha_pixels": 0,
    }


def composite(rgba: np.ndarray, color: tuple[int, int, int]) -> np.ndarray:
    a = rgba[:, :, 3:4].astype(np.float32) / 255.0
    bg = np.full(rgba[:, :, :3].shape, color, dtype=np.float32)
    return np.clip(np.rint(rgba[:, :, :3] * a + bg * (1 - a)), 0, 255).astype(np.uint8)


def label(image: np.ndarray, text: str) -> np.ndarray:
    im = Image.fromarray(image, "RGB")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, im.width, 19), fill=(7, 9, 15))
    d.text((6, 5), text, fill=(255, 255, 255), font=ImageFont.load_default())
    return np.array(im)


def make_qa(sprite: np.ndarray, master: np.ndarray) -> dict[str, str]:
    QA_100.mkdir(parents=True, exist_ok=True)
    colors = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "MAGENTA": (255, 0, 255), "GREEN": (0, 210, 55)}
    panels = []
    paths = {}
    for name, color in colors.items():
        view = composite(sprite, color)
        p = QA_100 / f"BRAVE_FIST_E03_IDLE_SOUTH_100PCT_{name}_ALPHA_QA.png"
        Image.fromarray(view, "RGB").save(p, optimize=False)
        paths[f"100pct_{name.lower()}"] = str(p)
        panels.append(label(view, f"100% {name}"))
    board = np.concatenate(panels, axis=1)
    pboard = QA / "BRAVE_FIST_E03_IDLE_SOUTH_100PCT_4BACKGROUND_ALPHA_QA.png"
    Image.fromarray(board, "RGB").save(pboard, optimize=False)
    paths["100pct_4background_board"] = str(pboard)

    mask_path = QA / "BRAVE_FIST_E03_IDLE_SOUTH_ALPHA_INTERNAL_SPACE_MASK_1254.png"
    Image.fromarray(master[:, :, 3], "L").save(mask_path, optimize=False)
    paths["alpha_internal_space_mask"] = str(mask_path)

    # A 50% display-scale QA.  Only the grid, arrow, and compositing are drawn;
    # the mecha pixels are a premultiplied resize of the delivered sprite.
    qa = Image.new("RGB", (640, 360), (20, 25, 34))
    d = ImageDraw.Draw(qa)
    pivot = (320, 286)
    ex = (20, 12)
    ny = (20, -12)
    for u in range(-2, 3):
        a = (pivot[0] + u * ex[0] - 2 * ny[0], pivot[1] + u * ex[1] - 2 * ny[1])
        b = (pivot[0] + u * ex[0] + 2 * ny[0], pivot[1] + u * ex[1] + 2 * ny[1])
        d.line((a, b), fill=(72, 92, 116), width=1)
    for v in range(-2, 3):
        a = (pivot[0] - 2 * ex[0] + v * ny[0], pivot[1] - 2 * ex[1] + v * ny[1])
        b = (pivot[0] + 2 * ex[0] + v * ny[0], pivot[1] + 2 * ex[1] + v * ny[1])
        d.line((a, b), fill=(72, 92, 116), width=1)
    small = premul_resize(sprite, (128, 128), alpha_zero=2)
    small_im = Image.fromarray(small, "RGBA")
    qa.paste(small_im, (pivot[0] - 64, pivot[1] - 112), small_im)
    d = ImageDraw.Draw(qa)
    d.ellipse((pivot[0] - 3, pivot[1] - 3, pivot[0] + 3, pivot[1] + 3), fill=(255, 220, 80))
    d.line((pivot[0], pivot[1], pivot[0] - 40, pivot[1] + 24), fill=(255, 105, 75), width=3)
    d.text((16, 16), "50% CAMERA V2 / SOUTH [-40,24] / 2x2 / PIVOT [128,224]", fill=(245, 245, 245), font=ImageFont.load_default())
    scale_path = QA / "BRAVE_FIST_E03_IDLE_SOUTH_50PCT_CAMERA_V2_SCALE_QA.png"
    qa.save(scale_path, optimize=False)
    paths["50pct_camera_v2_scale"] = str(scale_path)
    return paths


def main() -> None:
    if digest(RAW) != RAW_SHA:
        raise SystemExit("raw SHA mismatch")
    if digest(SOURCE) != SOURCE_SHA:
        raise SystemExit("A33 source SHA mismatch")
    raw_image = Image.open(RAW)
    if raw_image.mode != "RGB" or raw_image.size != (1254, 1254):
        raise SystemExit(f"unexpected raw: {raw_image.mode} {raw_image.size}")
    rgb = np.array(raw_image, dtype=np.uint8)
    master, _, _, alpha_audit = extract_alpha(rgb)
    sprite, register_audit = register(master)

    MASTER.parent.mkdir(parents=True, exist_ok=True)
    SPRITE.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(master, "RGBA").save(MASTER, optimize=False)
    Image.fromarray(sprite, "RGBA").save(SPRITE, optimize=False)
    qa = make_qa(sprite, master)

    technical_pass = (
        alpha_audit["internal_core_rgb_changed_pixels"] == 0
        and alpha_audit["opaque_rgb_changed_pixels"] == 0
        and alpha_audit["opaque_checker_component_count"] == 0
        and alpha_audit["outside_foreground_nontransparent_pixels"] == 0
        and alpha_audit["transparent_rgb_nonzero_pixels"] == 0
        and register_audit["clipped_alpha_pixels"] == 0
        and register_audit["alpha_bbox_exclusive"][3] == PIVOT[1]
    )
    report = {
        "status": "MACHINE_ALPHA_SCALE_PASS_VISUAL_USER_REVIEW_PENDING" if technical_pass else "FAIL_STOP_MACHINE_ALPHA_SCALE",
        "technical_pass": bool(technical_pass),
        "imagegen_calls": 1,
        "rerolls": 0,
        "input": {"path": str(RAW), "sha256": RAW_SHA, "size": [1254, 1254], "mode": "RGB"},
        "identity_source": {"path": str(SOURCE), "source_id": "BF_A33_USER_ACCEPTED_IDENTITY", "sha256": SOURCE_SHA},
        "master": {"path": str(MASTER), "sha256": digest(MASTER), "size": [1254, 1254], "mode": "RGBA", **alpha_audit},
        "sprite": {"path": str(SPRITE), "sha256": digest(SPRITE), "size": [256, 256], "mode": "RGBA", **register_audit},
        "qa": qa,
        "lifecycle": {"authority": "Candidate", "user": False, "runtime": False, "default": False, "canon": False, "godot_binding": False},
    }
    AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not technical_pass:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
