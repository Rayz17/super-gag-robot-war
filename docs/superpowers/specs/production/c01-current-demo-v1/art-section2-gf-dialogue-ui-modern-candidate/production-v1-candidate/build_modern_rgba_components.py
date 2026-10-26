#!/usr/bin/env python3
"""Deterministically derive production RGBA UI components from the user-approved modern direction board.

The board is the only positive pixel source.  The rejected ornate Call01 is never read.
This script reconstructs the smooth presentation backdrop, separates the authored
materials/highlights, opens the dialogue perimeter, exports explicit component assets,
and creates technical/visual QA.  It does not touch Godot or Canon.
"""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "call01" / "raw" / "GF_DIALOGUE_UI_MODERN_DIRECTION_BOARD_CALL01.png"
DELIVERY = HERE / "delivery"
QA = HERE / "qa"
RECEIPTS = HERE / "receipts"

SOURCE_SHA = "54c2fd074699dccc363e4eeca2ea0a2021823b96b2c765f3d32859848c0fa446"
LIFECYCLE = "production_quality_candidate_user_accepted_direction"


@dataclass(frozen=True)
class Asset:
    asset_id: str
    filename: str
    image: Image.Image
    filter_mode: str
    repeat_mode: str
    margins: tuple[int, int, int, int]
    safe_rect: str
    atlas_layout: str
    state_ids: str
    notes: str


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def aa_mask(size: tuple[int, int], layers: list[tuple[list[tuple[int, int]], int]], scale: int = 4) -> np.ndarray:
    canvas = Image.new("L", (size[0] * scale, size[1] * scale), 0)
    draw = ImageDraw.Draw(canvas)
    for polygon, value in layers:
        points = [(x * scale, y * scale) for x, y in polygon]
        draw.polygon(points, fill=value)
    canvas = canvas.resize(size, Image.Resampling.LANCZOS)
    return np.asarray(canvas, dtype=np.float32)


def rect_mask(size: tuple[int, int], rects: list[tuple[int, int, int, int]], value: int = 255) -> np.ndarray:
    canvas = Image.new("L", size, 0)
    draw = ImageDraw.Draw(canvas)
    for rect in rects:
        draw.rectangle(rect, fill=value)
    return np.asarray(canvas, dtype=np.float32)


def poly_features(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            np.ones_like(x), x, y,
            x * x, x * y, y * y,
            x**3, x * x * y, x * y * y, y**3,
            x**4, x**3 * y, x * x * y * y, x * y**3, y**4,
        ]
    )


def fit_background(rgb: np.ndarray) -> tuple[np.ndarray, dict]:
    """Fit the smooth graphite presentation backdrop from known empty zones."""
    h, w, _ = rgb.shape
    yy, xx = np.mgrid[0:h:4, 0:w:4]
    keep = np.ones(xx.shape, dtype=bool)
    excluded = [
        (55, 55, 1265, 525),
        (1260, 270, 1635, 440),
        (35, 515, 480, 905),
        (625, 535, 1630, 690),
        (500, 700, 1165, 885),
        (1160, 700, 1640, 885),
    ]
    for x1, y1, x2, y2 in excluded:
        keep &= ~((xx >= x1) & (xx < x2) & (yy >= y1) & (yy < y2))

    xn = (xx[keep].astype(np.float64) / (w - 1)) * 2.0 - 1.0
    yn = (yy[keep].astype(np.float64) / (h - 1)) * 2.0 - 1.0
    design = poly_features(xn, yn)
    samples = rgb[yy[keep], xx[keep]].astype(np.float64)
    coeffs = np.linalg.lstsq(design, samples, rcond=None)[0]

    full_y, full_x = np.mgrid[0:h, 0:w]
    fx = (full_x.astype(np.float64) / (w - 1)) * 2.0 - 1.0
    fy = (full_y.astype(np.float64) / (h - 1)) * 2.0 - 1.0
    bg = (poly_features(fx.ravel(), fy.ravel()) @ coeffs).reshape(h, w, 3)
    bg = np.clip(bg, 0, 255).astype(np.float32)

    predicted = (design @ coeffs)
    residual = samples - predicted
    metrics = {
        "model": "degree4_bivariate_polynomial_from_clean_4px_samples",
        "sample_count": int(samples.shape[0]),
        "channel_mae": [float(v) for v in np.mean(np.abs(residual), axis=0)],
        "channel_rmse": [float(v) for v in np.sqrt(np.mean(residual * residual, axis=0))],
        "excluded_component_rects": excluded,
    }
    return bg, metrics


def dilate(mask: np.ndarray, pixels: int) -> np.ndarray:
    if pixels <= 0:
        return mask
    size = pixels * 2 + 1
    if size % 2 == 0:
        size += 1
    image = Image.fromarray(np.clip(mask, 0, 255).astype(np.uint8), "L")
    return np.asarray(image.filter(ImageFilter.MaxFilter(size)), dtype=np.float32)


def extract_component(
    source: np.ndarray,
    background: np.ndarray,
    box: tuple[int, int, int, int],
    base_mask: np.ndarray,
    detail_extent: np.ndarray,
    *,
    detail_floor: float = 1.0,
    detail_span: float = 22.0,
    suppress_detail: np.ndarray | None = None,
    cut_alpha: np.ndarray | None = None,
) -> Image.Image:
    x1, y1, x2, y2 = box
    observed = source[y1:y2, x1:x2].astype(np.float32)
    backdrop = background[y1:y2, x1:x2].astype(np.float32)
    if observed.shape[:2] != base_mask.shape:
        raise ValueError(f"mask mismatch for {box}: {observed.shape[:2]} vs {base_mask.shape}")

    delta = observed - backdrop
    magnitude = np.sqrt(np.sum(delta * delta, axis=2))
    chroma_signal = np.maximum.reduce(
        [np.abs(delta[:, :, 0] - delta[:, :, 1]), np.abs(delta[:, :, 1] - delta[:, :, 2])]
    )
    effective = np.maximum(magnitude, chroma_signal * 1.7)
    detail_alpha = np.clip((effective - detail_floor) / detail_span * 255.0, 0.0, 255.0)
    detail_alpha *= detail_extent / 255.0
    if suppress_detail is not None:
        detail_alpha *= 1.0 - np.clip(suppress_detail / 255.0, 0.0, 1.0)

    # A tiny blur retains antialiasing while the manual component support prevents a rectangular matte.
    detail_image = Image.fromarray(detail_alpha.astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.35))
    detail_alpha = np.asarray(detail_image, dtype=np.float32)
    # Smooth-board residuals below this level are not authored glow.  Pruning them
    # outside the solid support prevents color-noise halos on white/magenta QA beds.
    detail_alpha[(base_mask < 1.0) & (detail_alpha < 52.0)] = 0.0
    alpha = np.maximum(base_mask, detail_alpha)
    if cut_alpha is not None:
        alpha *= 1.0 - np.clip(cut_alpha / 255.0, 0.0, 1.0)
    alpha = np.clip(alpha, 0, 255)

    a = alpha[:, :, None] / 255.0
    safe_a = np.maximum(a, 1.0 / 255.0)
    foreground = (observed - (1.0 - a) * backdrop) / safe_a
    foreground = np.clip(foreground, 0, 255)
    foreground[alpha < 0.5] = 0
    rgba = np.dstack([foreground.astype(np.uint8), alpha.astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA")


def cool_neutral_grade(image: Image.Image) -> Image.Image:
    """Turn warm-neutral bevel light into cool white without touching safety orange."""
    arr = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgb = arr[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    chroma = np.maximum.reduce([r, g, b]) - np.minimum.reduce([r, g, b])
    warm_neutral = (
        (arr[:, :, 3] > 0)
        & (r > g + 1)
        & (g >= b)
        & (chroma <= 42)
        & (r >= 72)
    )
    luminance = np.clip(np.rint(r * 0.30 + g * 0.59 + b * 0.11), 0, 255).astype(np.uint8)
    arr[warm_neutral, 0] = np.clip(luminance[warm_neutral].astype(np.int16) - 2, 0, 255).astype(np.uint8)
    arr[warm_neutral, 1] = luminance[warm_neutral]
    arr[warm_neutral, 2] = np.clip(luminance[warm_neutral].astype(np.int16) + 5, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def inset_with_padding(image: Image.Image, size: tuple[int, int], padding: int) -> Image.Image:
    inner = resize_premultiplied(image, (size[0] - padding * 2, size[1] - padding * 2))
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.alpha_composite(inner, (padding, padding))
    return out


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    premult = rgba[:, :, :3] * alpha
    premult_img = Image.fromarray(np.clip(premult, 0, 255).astype(np.uint8), "RGB")
    alpha_img = Image.fromarray(rgba[:, :, 3].astype(np.uint8), "L")
    premult_resized = np.asarray(premult_img.resize(size, Image.Resampling.LANCZOS), dtype=np.float32)
    alpha_resized = np.asarray(alpha_img.resize(size, Image.Resampling.LANCZOS), dtype=np.float32)
    out_alpha = alpha_resized[:, :, None] / 255.0
    rgb = np.zeros_like(premult_resized)
    valid = out_alpha[:, :, 0] > 0.0
    rgb[valid] = premult_resized[valid] / out_alpha[valid]
    rgb = np.clip(rgb, 0, 255)
    out = np.dstack([rgb.astype(np.uint8), alpha_resized.astype(np.uint8)])
    out[out[:, :, 3] == 0, :3] = 0
    return Image.fromarray(out, "RGBA")


def place_in_cell(image: Image.Image, cell: tuple[int, int], pad: int = 4) -> Image.Image:
    max_w = cell[0] - pad * 2
    max_h = cell[1] - pad * 2
    scale = min(max_w / image.width, max_h / image.height)
    resized = resize_premultiplied(image, (max(1, round(image.width * scale)), max(1, round(image.height * scale))))
    canvas = Image.new("RGBA", cell, (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((cell[0] - resized.width) // 2, (cell[1] - resized.height) // 2))
    return canvas


def clean_zero_rgb(image: Image.Image) -> Image.Image:
    arr = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    arr[arr[:, :, 3] == 0, :3] = 0
    return Image.fromarray(arr, "RGBA")


def build_assets(source: np.ndarray, background: np.ndarray) -> list[Asset]:
    assets: list[Asset] = []

    # 1) Dialogue panel.  Preserve the authored left avionics rail and clipped terminals,
    # but suppress the long top/right/bottom contour so the production structure is decisively open.
    box = (78, 78, 1245, 500)
    size = (box[2] - box[0], box[3] - box[1])
    panel_layers = [
        ([(92, 26), (1120, 26), (1150, 44), (1150, 274), (1056, 394), (120, 394), (94, 367), (94, 49)], 188),
        ([(18, 17), (102, 17), (130, 43), (94, 85), (94, 354), (121, 394), (86, 409), (18, 409)], 234),
        ([(243, 11), (377, 11), (382, 29), (236, 29)], 218),
    ]
    base = aa_mask(size, panel_layers)
    extent = dilate(np.where(base > 0, 255.0, 0.0), 18)
    open_cuts = rect_mask(size, [(500, 8, 1070, 35), (1137, 82, 1166, 251), (355, 382, 880, 421)])
    panel = extract_component(
        source,
        background,
        box,
        base,
        extent,
        detail_floor=0.8,
        detail_span=20.0,
        suppress_detail=open_cuts,
        cut_alpha=open_cuts,
    )
    panel = cool_neutral_grade(panel)
    panel = inset_with_padding(panel, (768, 192), 3)
    assets.append(
        Asset(
            "C01_GF_DIALOGUE_PANEL_9SLICE",
            "gf_modern_dialogue_panel_9slice_rgba.png",
            panel,
            "linear",
            "disabled",
            (104, 48, 92, 48),
            "126,34,700,162",
            "n/a",
            "n/a",
            "combined smoked panel plus open asymmetric left rail; production perimeter opened from approved board",
        )
    )

    # 2) Speaker/data tab.
    box = (1288, 292, 1615, 412)
    size = (327, 120)
    base = aa_mask(
        size,
        [
            ([(38, 18), (120, 18), (131, 23), (246, 23), (257, 33), (300, 33), (300, 90), (288, 101), (57, 101), (18, 69), (18, 38)], 208),
        ],
    )
    extent = dilate(np.where(base > 0, 255.0, 0.0), 12)
    speaker = extract_component(source, background, box, base, extent, detail_floor=0.8, detail_span=18.0)
    speaker = cool_neutral_grade(speaker)
    speaker = inset_with_padding(speaker, (320, 72), 2)
    assets.append(
        Asset(
            "C01_GF_SPEAKER_TAB_9SLICE",
            "gf_modern_speaker_tab_9slice_rgba.png",
            speaker,
            "linear",
            "disabled",
            (48, 20, 48, 20),
            "64,18,256,54",
            "n/a",
            "n/a",
            "live text only; no baked speaker identity",
        )
    )

    # 3) Local-scene status rail: an open L rail; its interior must stay transparent.
    box = (60, 530, 460, 885)
    size = (400, 355)
    rail_layers = [
        ([(20, 25), (100, 25), (113, 35), (190, 35), (198, 47), (235, 47), (235, 73), (102, 73), (75, 60), (20, 60)], 206),
        ([(20, 25), (75, 60), (75, 284), (96, 307), (20, 307)], 216),
        ([(20, 307), (96, 307), (218, 307), (248, 280), (367, 280), (367, 317), (20, 317)], 206),
    ]
    base = aa_mask(size, rail_layers)
    extent = dilate(np.where(base > 0, 255.0, 0.0), 12)
    local_rail = extract_component(source, background, box, base, extent, detail_floor=0.7, detail_span=17.0)
    local_rail = cool_neutral_grade(local_rail)
    local_rail = inset_with_padding(local_rail, (360, 320), 2)
    assets.append(
        Asset(
            "C01_GF_LOCAL_SCENE_STATUS_RAIL_9SLICE",
            "gf_modern_local_scene_status_rail_9slice_rgba.png",
            local_rail,
            "linear",
            "disabled",
            (64, 72, 64, 72),
            "70,68,326,286",
            "n/a",
            "n/a",
            "open action-insert anchor; center remains true transparent and does not crop local-scene pixels",
        )
    )

    # 4) Beat progress state cells sampled from the approved rail.
    state_centers = [(842, 610), (1183, 610), (1328, 610), (1441, 610)]
    state_names = ["completed", "current", "idle", "locked"]
    state_images: dict[str, Image.Image] = {}
    for (cx, cy), state in zip(state_centers, state_names):
        box = (cx - 34, cy - 34, cx + 34, cy + 34)
        size = (68, 68)
        base = aa_mask(size, [([(4, 29), (64, 29), (64, 39), (4, 39)], 82), ([(24, 18), (44, 18), (44, 50), (24, 50)], 150)])
        extent = dilate(np.where(base > 0, 255.0, 0.0), 8)
        state_img = extract_component(source, background, box, base, extent, detail_floor=0.65, detail_span=13.0)
        state_images[state] = place_in_cell(cool_neutral_grade(state_img), (48, 48), pad=1)

    # Locked keeps the approved dark marker but loses the top-right terminal, a shape cue rather than brightness only.
    locked_arr = np.asarray(state_images["locked"], dtype=np.uint8).copy()
    lock_cut = aa_mask((48, 48), [([(31, 4), (47, 4), (47, 20)], 255)])
    locked_arr[:, :, 3] = np.clip(locked_arr[:, :, 3].astype(np.float32) * (1.0 - lock_cut / 255.0), 0, 255).astype(np.uint8)
    locked_arr[locked_arr[:, :, 3] == 0, :3] = 0
    state_images["locked"] = Image.fromarray(locked_arr, "RGBA")

    atlas = Image.new("RGBA", (192, 48), (0, 0, 0, 0))
    ordered = ["idle", "completed", "current", "locked"]
    for index, state in enumerate(ordered):
        atlas.alpha_composite(state_images[state], (index * 48, 0))
    assets.append(
        Asset(
            "C01_GF_DIALOGUE_PROGRESS_ATLAS",
            "gf_modern_dialogue_progress_atlas_rgba.png",
            atlas,
            "linear",
            "disabled",
            (0, 0, 0, 0),
            "0,0,192,48",
            "4x1;cell=48x48",
            "idle,completed,current,locked",
            "dynamic beat count remains runtime-owned",
        )
    )

    # 5) Three low-profile prompt shell states, repeated for keyboard/mouse/gamepad rows.
    prompt_boxes = [(545, 735, 740, 840), (746, 735, 935, 840), (944, 735, 1134, 840)]
    prompt_states: list[Image.Image] = []
    for box in prompt_boxes:
        size = (box[2] - box[0], box[3] - box[1])
        w, h = size
        base = aa_mask(size, [([(22, 20), (w - 49, 20), (w - 20, 43), (w - 20, h - 34), (w - 49, h - 13), (22, h - 13), (8, h - 31), (8, 38)], 198)])
        extent = dilate(np.where(base > 0, 255.0, 0.0), 10)
        prompt = extract_component(source, background, box, base, extent, detail_floor=0.7, detail_span=15.0)
        prompt_states.append(place_in_cell(cool_neutral_grade(prompt), (96, 48), pad=2))

    prompt_atlas = Image.new("RGBA", (288, 144), (0, 0, 0, 0))
    for row in range(3):
        for col, state in enumerate(prompt_states):
            prompt_atlas.alpha_composite(state, (col * 96, row * 48))
    assets.append(
        Asset(
            "C01_GF_DIALOGUE_NEXT_PROMPT_ATLAS",
            "gf_modern_dialogue_next_prompt_atlas_rgba.png",
            prompt_atlas,
            "linear",
            "disabled",
            (0, 0, 0, 0),
            "0,0,288,144",
            "3x3;cell=96x48;rows=input;cols=state",
            "keyboard_idle,keyboard_focus,keyboard_pressed,mouse_idle,mouse_focus,mouse_pressed,gamepad_idle,gamepad_focus,gamepad_pressed",
            "shells only; live device glyph and localized instruction remain runtime-owned",
        )
    )

    # 6) Two comms/status rail states from the approved cyan and safety-orange lines.
    comms_cells: list[Image.Image] = []
    for box, y_band in [((1190, 730, 1615, 790), (17, 46)), ((1190, 785, 1615, 845), (18, 50))]:
        size = (425, 60)
        base = rect_mask(size, [(24, 27, 397, 33)], value=70)
        extent = rect_mask(size, [(8, y_band[0], 417, y_band[1])], value=255)
        rail = extract_component(source, background, box, base, extent, detail_floor=0.55, detail_span=10.0)
        rail = cool_neutral_grade(rail)
        comms_cells.append(place_in_cell(rail, (384, 48), pad=2))
    comms_atlas = Image.new("RGBA", (768, 48), (0, 0, 0, 0))
    comms_atlas.alpha_composite(comms_cells[0], (0, 0))
    comms_atlas.alpha_composite(comms_cells[1], (384, 0))
    assets.append(
        Asset(
            "C01_GF_COMMS_STATUS_RAIL_ATLAS",
            "gf_modern_comms_status_rail_atlas_rgba.png",
            comms_atlas,
            "linear",
            "disabled",
            (0, 0, 0, 0),
            "0,0,768,48",
            "2x1;cell=384x48",
            "linked_cyan,decision_orange",
            "short functional comms/status rail; no text or identity baked",
        )
    )

    return assets


def nine_slice_resize(image: Image.Image, size: tuple[int, int], margins: tuple[int, int, int, int]) -> Image.Image:
    left, top, right, bottom = margins
    sw, sh = image.size
    tw, th = size
    if tw < left + right or th < top + bottom:
        raise ValueError(f"target {size} smaller than margins {margins}")
    xs = [0, left, sw - right, sw]
    ys = [0, top, sh - bottom, sh]
    txs = [0, left, tw - right, tw]
    tys = [0, top, th - bottom, th]
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    for row in range(3):
        for col in range(3):
            crop = image.crop((xs[col], ys[row], xs[col + 1], ys[row + 1]))
            target = (txs[col + 1] - txs[col], tys[row + 1] - tys[row])
            if crop.size != target:
                crop = resize_premultiplied(crop, target)
            out.alpha_composite(crop, (txs[col], tys[row]))
    return clean_zero_rgb(out)


def composite_on(image: Image.Image, color: tuple[int, int, int, int]) -> Image.Image:
    bg = Image.new("RGBA", image.size, color)
    bg.alpha_composite(image)
    return bg.convert("RGB")


def font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def make_alpha_qa(assets: list[Asset]) -> None:
    backgrounds = [
        (5, 13, 25, 255),
        (127, 127, 127, 255),
        (245, 245, 245, 255),
        (255, 0, 255, 255),
    ]
    card_w, card_h = 360, 210
    sheet = Image.new("RGB", (card_w * 4, card_h * len(assets)), (8, 13, 22))
    draw = ImageDraw.Draw(sheet)
    label_font = font(17)
    for row, asset in enumerate(assets):
        for col, color in enumerate(backgrounds):
            card = Image.new("RGBA", (card_w, card_h), color)
            scale = min((card_w - 24) / asset.image.width, (card_h - 42) / asset.image.height, 1.0)
            preview = resize_premultiplied(asset.image, (max(1, round(asset.image.width * scale)), max(1, round(asset.image.height * scale))))
            card.alpha_composite(preview, ((card_w - preview.width) // 2, 30 + (card_h - 34 - preview.height) // 2))
            sheet.paste(card.convert("RGB"), (col * card_w, row * card_h))
            draw.text((col * card_w + 8, row * card_h + 6), asset.asset_id, fill=(210, 224, 236), font=label_font)
    sheet.save(QA / "GF_MODERN_COMPONENTS_ALPHA_BACKGROUNDS_100PCT.png")
    sheet.resize((sheet.width // 2, sheet.height // 2), Image.Resampling.LANCZOS).save(QA / "GF_MODERN_COMPONENTS_ALPHA_BACKGROUNDS_50PCT.png")


def make_nineslice_qa(assets: list[Asset]) -> None:
    by_id = {a.asset_id: a for a in assets}
    panel = by_id["C01_GF_DIALOGUE_PANEL_9SLICE"]
    speaker = by_id["C01_GF_SPEAKER_TAB_9SLICE"]
    local = by_id["C01_GF_LOCAL_SCENE_STATUS_RAIL_9SLICE"]
    canvas = Image.new("RGBA", (1280, 1000), (6, 15, 28, 255))
    draw = ImageDraw.Draw(canvas)
    f = font(18)
    tests = [
        (panel, (679, 163), (24, 42), "dialogue 679x163"),
        (panel, (1144, 163), (24, 245), "dialogue 1144x163"),
        (speaker, (210, 64), (24, 455), "speaker 210x64"),
        (speaker, (330, 64), (260, 455), "speaker 330x64"),
        (local, (342, 512), (900, 450), "local rail 342x512"),
    ]
    for asset, target, pos, label in tests:
        rendered = nine_slice_resize(asset.image, target, asset.margins)
        canvas.alpha_composite(rendered, pos)
        draw.text((pos[0], max(4, pos[1] - 24)), label, fill=(205, 222, 236, 255), font=f)
    canvas.convert("RGB").save(QA / "GF_MODERN_NINESLICE_STRETCH_QA.png")


def make_actual_hud_qa(assets: list[Asset]) -> None:
    by_id = {a.asset_id: a for a in assets}
    canvas = Image.new("RGBA", (1280, 720), (4, 12, 24, 255))
    draw = ImageDraw.Draw(canvas)
    # Subtle battlefield grid only for scale/readability, not a consumer mockup.
    for x in range(0, 1280, 64):
        draw.line((x, 0, x, 720), fill=(18, 39, 57, 90), width=1)
    for y in range(0, 720, 64):
        draw.line((0, y, 1280, y), fill=(18, 39, 57, 90), width=1)

    local = nine_slice_resize(by_id["C01_GF_LOCAL_SCENE_STATUS_RAIL_9SLICE"].image, (342, 512), by_id["C01_GF_LOCAL_SCENE_STATUS_RAIL_9SLICE"].margins)
    panel = nine_slice_resize(by_id["C01_GF_DIALOGUE_PANEL_9SLICE"].image, (679, 163), by_id["C01_GF_DIALOGUE_PANEL_9SLICE"].margins)
    speaker = nine_slice_resize(by_id["C01_GF_SPEAKER_TAB_9SLICE"].image, (250, 64), by_id["C01_GF_SPEAKER_TAB_9SLICE"].margins)
    canvas.alpha_composite(local, (18, 76))
    canvas.alpha_composite(panel, (338, 410))
    canvas.alpha_composite(speaker, (360, 382))
    progress = by_id["C01_GF_DIALOGUE_PROGRESS_ATLAS"].image.crop((0, 0, 192, 48))
    canvas.alpha_composite(progress, (745, 392))
    prompt = by_id["C01_GF_DIALOGUE_NEXT_PROMPT_ATLAS"].image.crop((192, 48, 288, 96))
    canvas.alpha_composite(prompt, (905, 515))
    comms = by_id["C01_GF_COMMS_STATUS_RAIL_ATLAS"].image.crop((0, 0, 384, 48))
    canvas.alpha_composite(comms, (680, 28))

    title_font = font(16)
    body_font = font(25)
    small_font = font(14)
    draw.text((376, 399), "纪存  /  现场导览席", fill=(218, 232, 242, 255), font=title_font)
    draw.text((392, 456), "这里是实际对话的中文安全区。", fill=(231, 238, 244, 255), font=body_font)
    draw.text((392, 497), "开放框缘不得压住左侧动作关系或战场主体。", fill=(189, 207, 220, 255), font=small_font)
    draw.text((932, 533), "推进", fill=(209, 229, 240, 255), font=small_font)
    canvas.convert("RGB").save(QA / "GF_MODERN_HUD_ACTUAL_1280x720_NAVY_GATE.png")
    canvas.resize((640, 360), Image.Resampling.LANCZOS).convert("RGB").save(QA / "GF_MODERN_HUD_ACTUAL_50PCT_NAVY_GATE.png")


def make_edge_qa(assets: list[Asset]) -> None:
    colors = [(3, 9, 18, 255), (245, 245, 245, 255), (255, 0, 255, 255)]
    tile_w, tile_h = 720, 260
    sheet = Image.new("RGB", (tile_w * 3, tile_h * len(assets)), (0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    f = font(17)
    for row, asset in enumerate(assets):
        enlarged = resize_premultiplied(asset.image, (asset.image.width * 2, asset.image.height * 2))
        for col, color in enumerate(colors):
            tile = Image.new("RGBA", (tile_w, tile_h), color)
            scale = min((tile_w - 20) / enlarged.width, (tile_h - 38) / enlarged.height, 1.0)
            preview = resize_premultiplied(enlarged, (max(1, round(enlarged.width * scale)), max(1, round(enlarged.height * scale))))
            tile.alpha_composite(preview, ((tile_w - preview.width) // 2, 28 + (tile_h - 32 - preview.height) // 2))
            sheet.paste(tile.convert("RGB"), (col * tile_w, row * tile_h))
            draw.text((col * tile_w + 8, row * tile_h + 5), f"{asset.asset_id} / edge gate", fill=(210, 224, 236), font=f)
    sheet.save(QA / "GF_MODERN_COMPONENTS_EDGE_GATE_DARK_WHITE_MAGENTA.png")


def image_metrics(asset: Asset) -> dict:
    arr = np.asarray(asset.image.convert("RGBA"), dtype=np.uint8)
    alpha = arr[:, :, 3]
    boundary = np.concatenate([alpha[0, :], alpha[-1, :], alpha[:, 0], alpha[:, -1]])
    zero_rgb_nonzero = int(np.count_nonzero(np.any(arr[alpha == 0, :3] != 0, axis=1))) if np.any(alpha == 0) else 0
    return {
        "asset_id": asset.asset_id,
        "width": asset.image.width,
        "height": asset.image.height,
        "mode": asset.image.mode,
        "alpha0_pixels": int(np.count_nonzero(alpha == 0)),
        "partial_alpha_pixels": int(np.count_nonzero((alpha > 0) & (alpha < 255))),
        "alpha255_pixels": int(np.count_nonzero(alpha == 255)),
        "boundary_alpha_nonzero_pixels": int(np.count_nonzero(boundary)),
        "transparent_pixels_with_nonzero_rgb": zero_rgb_nonzero,
        "alpha_bbox": list(Image.fromarray(alpha, "L").getbbox() or (0, 0, 0, 0)),
    }


def write_delivery(assets: list[Asset], background_metrics: dict) -> None:
    for path in [DELIVERY, QA, RECEIPTS]:
        path.mkdir(parents=True, exist_ok=True)

    rows = []
    metrics = []
    for asset in assets:
        image = clean_zero_rgb(asset.image)
        path = DELIVERY / asset.filename
        image.save(path)
        normalized = Asset(asset.asset_id, asset.filename, image, asset.filter_mode, asset.repeat_mode, asset.margins, asset.safe_rect, asset.atlas_layout, asset.state_ids, asset.notes)
        metric = image_metrics(normalized)
        if metric["mode"] != "RGBA":
            raise RuntimeError(f"{asset.asset_id}: not RGBA")
        if metric["alpha0_pixels"] == 0 or metric["partial_alpha_pixels"] == 0:
            raise RuntimeError(f"{asset.asset_id}: missing true transparent/partial alpha")
        if metric["transparent_pixels_with_nonzero_rgb"] != 0:
            raise RuntimeError(f"{asset.asset_id}: RGB data remains under alpha0")
        metrics.append(metric)
        rows.append(
            {
                "asset_id": asset.asset_id,
                "path": f"delivery/{asset.filename}",
                "media": "image/png",
                "width": image.width,
                "height": image.height,
                "alpha": "RGBA8_true_alpha",
                "color_space": "sRGB",
                "filter_mode": asset.filter_mode,
                "repeat_mode": asset.repeat_mode,
                "nine_slice_left": asset.margins[0],
                "nine_slice_top": asset.margins[1],
                "nine_slice_right": asset.margins[2],
                "nine_slice_bottom": asset.margins[3],
                "safe_rect": asset.safe_rect,
                "atlas_layout": asset.atlas_layout,
                "state_ids": asset.state_ids,
                "lifecycle": LIFECYCLE,
                "user_accepted_direction": "true",
                "internal_visual_gate": "pass_for_isolated_test_only",
                "component_visual_acceptance": "false",
                "test_only_consumption_allowed": "true",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
                "canon_allowed": "false",
                "source_rights_receipt": "receipts/SOURCE_RIGHTS_RECEIPT.md",
                "notes": asset.notes,
                "sha256": sha256(path),
            }
        )

    fields = list(rows[0].keys())
    with (HERE / "asset-manifest.tsv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    make_alpha_qa(assets)
    make_nineslice_qa(assets)
    make_actual_hud_qa(assets)
    make_edge_qa(assets)

    receipt = {
        "status": "PASS_MACHINE_AND_INTERNAL_VISUAL_GATE_TEST_ONLY",
        "source_board": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": sha256(SOURCE),
            "expected_sha256": SOURCE_SHA,
            "only_positive_pixel_source": True,
            "rejected_call01_pixels_read": False,
        },
        "background_reconstruction": background_metrics,
        "assets": rows,
        "alpha_metrics": metrics,
        "gates": {
            "user_accepted_direction": True,
            "internal_visual_gate": "pass_for_isolated_test_only",
            "component_visual_acceptance": False,
            "test_only_consumption_allowed": True,
            "godot_modified": False,
            "runtime_allowed": False,
            "runtime_handoff": "none",
            "canon_modified": False,
        },
    }
    (RECEIPTS / "machine-metrics.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    paths = [HERE / "asset-manifest.tsv"] + [DELIVERY / a.filename for a in assets] + sorted(QA.glob("*.png"))
    hash_lines = [f"{sha256(path)}  {path.relative_to(HERE)}" for path in paths]
    (RECEIPTS / "delivery-hashes.sha256").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"missing approved source: {SOURCE}")
    if sha256(SOURCE) != SOURCE_SHA:
        raise SystemExit("approved source SHA mismatch")
    raw = Image.open(SOURCE).convert("RGB")
    source = np.asarray(raw, dtype=np.float32)
    background, background_metrics = fit_background(source)
    assets = build_assets(source, background)
    write_delivery(assets, background_metrics)
    print(
        json.dumps(
            {
                "status": "PASS_MACHINE_AND_INTERNAL_VISUAL_GATE_TEST_ONLY",
                "source_sha256": sha256(SOURCE),
                "assets": [
                    {"asset_id": a.asset_id, "path": f"delivery/{a.filename}", "sha256": sha256(DELIVERY / a.filename)}
                    for a in assets
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
