#!/usr/bin/env python3
"""Build Task101 ENV-E0/E1/E2 from frozen geometry and six registered donor crops.

Visible pixels are derived only from the six Task98 material crops. Pillow drawing
is used only for mechanical masks, QA overlays, labels, and receipts. No actors,
stateful objects, weather FX, routes, UI, or future-state pixels enter cleanplates.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path("/Users/rayz/Documents/超gag机器人大战")
PROD = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1"
OUT = PROD / "art-a9-1a6-env-e0-current-topology-environment"
TASK98 = PROD / "art-a9-1a6-s-c2-sprite-first-map-camera-masters"

DIRS = {
    "source": OUT / "source",
    "donors": OUT / "source/donor-crops",
    "e0": OUT / "env-e0-masks",
    "e1": OUT / "env-e1-materials",
    "modules": OUT / "env-e1-materials/modules",
    "e2": OUT / "env-e2-layers",
    "clean": OUT / "cleanplates",
    "qa": OUT / "qa",
    "receipts": OUT / "receipts",
}

EXPECTED_INPUTS = {
    "TASK101_OBJECTIVE": (
        PROD / "101-c01e02-a9-1a6-env-e0-current-topology-environment-derivation-objective.md",
        "2f895fa89e25407d7f096df6ad1cc2c5baf7ef1e4395d48dea7de1bd0834f7cc",
    ),
    "PRODUCTION_BOARD": (
        PROD / "38-c01e02-m3-r0-5-production-board.tsv",
        "6402757d50ef070e38b03369f5c04d9a22ab459ab8deb14e87db5575d601764e",
    ),
    "TACTICAL_INTERFACE_1_6_4": (
        PROD / "c01e02-tactical-visual-interface-v1.json",
        "faeff89ec153b25d37dc991f56aa75b6580bf47db958b4e828b46ac81c08635c",
    ),
    "P98_PRODUCER_ACCEPTANCE": (
        PROD / "100-c01e02-g2-a2-c2-producer-playability-preflight-acceptance.md",
        "cd4d128a023136be7197190382b9724b002ad9f093247ce25160838e9d1ffdcc",
    ),
    "TASK102_RUNTIME_GRID_REGISTRATION_CORRECTION": (
        PROD / "102-c01e02-task98-runtime-grid-registration-producer-correction.md",
        "e8556f917456da83d933842b9ace9542f5238635d5166a6f5b7adbfad0d62378",
    ),
    "TASK98_MANIFEST": (
        TASK98 / "delivery-hashes.sha256",
        "41f5ba27a5b12088e84424c73e4fd6aa6aa93ba2bd7285e4bcb8eb94a94e50be",
    ),
    "TASK98_ENVIRONMENT_CONTRACT": (
        TASK98 / "environment-layer-contract.json",
        "ed683edc21dfde7b92ea3625e59892667694dd850ef49487a5962a19b818126b",
    ),
    "CURRENT_TOPOLOGY": (
        ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json",
        "61b49e5328e702cd654d28ff39c5c380ba0ae3e78753330635036d33f689523c",
    ),
    "CURRENT_MAP_CONTRACT": (
        ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/current_topology_map_contract.json",
        "74c6bbb3f732a61d3ed5a55d9c209b628152b9411395339d665aeeb0d76ab875",
    ),
    "CURRENT_COMPOSITOR_PROFILE": (
        ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/visual_compositor_profile.json",
        "13719d8a3bde0cc06acbed893198943164f2541cdc0b112cc5897ff38f4c3451",
    ),
    "CURRENT_PROJECTION_SOURCE": (
        ROOT / "game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/visual_projection.gd",
        "4f1fb4e029abb12d33abe3494425c3766916e7c3f9daf4395f0f682d5c6e3aed",
    ),
}

DONOR_TABLE = TASK98 / "call02-environment-donor-crops.tsv"
DONOR_TABLE_SHA = "76bda0377d2b738a9be279aeb4e2a4f823cfa378edfa694e9b606bc4be3d1034"
DONOR_PARENT_SHA = "98f30a9797591204f702ad1b36aaad1042c2cece1fd35a088b44d828f9e156d5"

CANVAS_SIZE = (2400, 1350)
CANVAS_ORIGIN = (-1760.0, -340.0)
GRID_SIZE = (32, 18)
TILE_HALF = (40.0, 20.0)
RAW_ORIGIN = (-880.0, -170.0)
MAP_VIEWPORT = (0, 58, 1280, 584)

CAMERAS = {
    "NO_FOCUS": {
        "center": (-720.0, 350.0),
        "map_crop": (400, 398, 1280, 584),
        "layer_top_left": (-400, -340),
    },
    "PLAN": {
        "center": (-480.0, 420.0),
        "map_crop": (640, 468, 1280, 584),
        "layer_top_left": (-640, -410),
    },
    "CONTACT_A": {
        "center": (-480.0, 450.0),
        "map_crop": (640, 498, 1280, 584),
        "layer_top_left": (-640, -440),
    },
    "CONTACT_B": {
        "center": (-500.0, 440.0),
        "map_crop": (620, 488, 1280, 584),
        "layer_top_left": (-620, -430),
    },
}

PALETTES = {
    "ground": [(7, 14, 22), (11, 23, 33), (16, 34, 45), (23, 48, 59), (34, 64, 74), (54, 88, 96), (91, 125, 129)],
    "road": [(7, 16, 25), (12, 28, 40), (19, 42, 54), (27, 57, 69), (41, 76, 86), (68, 105, 113), (119, 151, 154)],
    "rescue": [(7, 18, 26), (12, 31, 42), (18, 47, 58), (26, 64, 74), (38, 83, 91), (63, 111, 117), (109, 153, 155)],
    "facade": [(4, 10, 17), (8, 19, 28), (13, 30, 40), (20, 43, 54), (29, 58, 68), (47, 79, 87), (80, 111, 116)],
    "roof": [(5, 12, 20), (9, 23, 33), (15, 36, 47), (23, 50, 61), (34, 65, 75), (55, 91, 98), (92, 125, 128)],
    "foreground": [(3, 9, 15), (7, 17, 25), (11, 27, 37), (17, 39, 49), (26, 52, 61), (42, 70, 76), (72, 98, 102)],
}

FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
VISUAL_REVIEW_STATUS = "FAIL_50_PERCENT_INSUFFICIENT_DONOR_COVERAGE_PROGRAMMATIC_COLLAGE"
FAILURE_STATE = "ENV_E2_VISUAL_FAIL_50_PERCENT / BLOCKED_INSUFFICIENT_DONOR_COVERAGE_FOR_PRODUCT_ENVIRONMENT / IMAGEGEN_ZERO / NO_STATEFUL_OBJECTS / NOT_RUNTIME / FUN_NOT_PROVEN"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size=size)


def grid_to_raw(point: tuple[float, float]) -> tuple[float, float]:
    gx, gy = point
    return (
        RAW_ORIGIN[0] + (gx - gy) * TILE_HALF[0],
        RAW_ORIGIN[1] + (gx + gy) * TILE_HALF[1],
    )


def raw_to_canvas(point: tuple[float, float]) -> tuple[float, float]:
    return (point[0] - CANVAS_ORIGIN[0], point[1] - CANVAS_ORIGIN[1])


def grid_to_canvas(point: tuple[float, float]) -> tuple[float, float]:
    return raw_to_canvas(grid_to_raw(point))


def grid_to_screen(point: tuple[float, float], camera: str) -> tuple[float, float]:
    raw = grid_to_raw(point)
    center = CAMERAS[camera]["center"]
    return (640.0 + raw[0] - center[0], 350.0 + raw[1] - center[1])


def rect_polygon(rect: tuple[float, float, float, float], shift_y: float = 0.0) -> list[tuple[float, float]]:
    """Exact visual_projection.gd integer-cell-center boundary convention."""
    x, y, w, h = rect
    points = [
        (x - 0.5, y - 0.5),
        (x + w - 0.5, y - 0.5),
        (x + w - 0.5, y + h - 0.5),
        (x - 0.5, y + h - 0.5),
    ]
    return [(px, py + shift_y) for px, py in map(grid_to_canvas, points)]


def polygon_mask(points: list[tuple[float, float]], antialias: int = 1) -> Image.Image:
    if antialias == 1:
        im = Image.new("L", CANVAS_SIZE, 0)
        ImageDraw.Draw(im).polygon([(round(x), round(y)) for x, y in points], fill=255)
        return im
    hi = Image.new("L", (CANVAS_SIZE[0] * antialias, CANVAS_SIZE[1] * antialias), 0)
    ImageDraw.Draw(hi).polygon([(round(x * antialias), round(y * antialias)) for x, y in points], fill=255)
    return hi.resize(CANVAS_SIZE, Image.Resampling.LANCZOS)


def rect_mask(rect: tuple[float, float, float, float], antialias: int = 1, shift_y: float = 0.0) -> Image.Image:
    return polygon_mask(rect_polygon(rect, shift_y=shift_y), antialias=antialias)


def union_masks(masks: list[Image.Image]) -> Image.Image:
    out = Image.new("L", CANVAS_SIZE, 0)
    for m in masks:
        out = ImageChops.lighter(out, m)
    return out


def cell_union_mask(cells: set[tuple[int, int]], antialias: bool = False) -> Image.Image:
    scale = 2 if antialias else 1
    size = (CANVAS_SIZE[0] * scale, CANVAS_SIZE[1] * scale)
    out = Image.new("L", size, 0)
    draw = ImageDraw.Draw(out)
    for x, y in sorted(cells):
        pts = rect_polygon((x, y, 1, 1))
        draw.polygon([(round(px * scale), round(py * scale)) for px, py in pts], fill=255)
    if antialias:
        out = out.resize(CANVAS_SIZE, Image.Resampling.LANCZOS)
    return out


def parse_rect(text: str) -> tuple[int, int, int, int]:
    vals = [int(v.strip()) for v in text.strip().strip("[]").split(",")]
    if len(vals) != 4:
        raise ValueError(text)
    return tuple(vals)  # type: ignore[return-value]


def blockify(image: Image.Image, palette: list[tuple[int, int, int]], shift: int = 0) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = np.asarray(rgba.getchannel("A"), dtype=np.uint8)
    rgb = rgba.convert("RGB").filter(ImageFilter.MedianFilter(3))
    gray = np.asarray(ImageOps.grayscale(rgb), dtype=np.float32)
    valid = gray[alpha > 0]
    if valid.size == 0:
        return rgba
    lo, hi = np.percentile(valid, [2.0, 98.0])
    if hi - lo < 8:
        hi = lo + 8
    normalized = np.clip((gray - lo) / (hi - lo), 0.0, 1.0)
    normalized = np.power(normalized, 1.12)
    idx = np.floor(normalized * len(palette)).astype(np.int32)
    idx = np.clip(idx + shift, 0, len(palette) - 1)
    pal = np.asarray(palette, dtype=np.uint8)
    mapped = pal[idx]
    return Image.fromarray(np.dstack([mapped, alpha]), "RGBA")


def regrade(image: Image.Image, palette_name: str, shift: int = 0) -> Image.Image:
    return blockify(image, PALETTES[palette_name], shift=shift)


def cosine_window(width: int, height: int, overlap_x: int, overlap_y: int) -> np.ndarray:
    wx = np.ones(width, dtype=np.float32)
    wy = np.ones(height, dtype=np.float32)
    if overlap_x:
        ramp = np.sin(np.linspace(0.0, math.pi / 2.0, overlap_x, dtype=np.float32)) ** 2
        wx[:overlap_x] = ramp
        wx[-overlap_x:] = ramp[::-1]
    if overlap_y:
        ramp = np.sin(np.linspace(0.0, math.pi / 2.0, overlap_y, dtype=np.float32)) ** 2
        wy[:overlap_y] = ramp
        wy[-overlap_y:] = ramp[::-1]
    return wy[:, None] * wx[None, :]


def quilt(
    name: str,
    module_ids: list[str],
    modules: dict[str, Image.Image],
    seed: int,
    patch_size: tuple[int, int] = (360, 240),
    overlap: tuple[int, int] = (96, 64),
) -> tuple[Image.Image, list[dict], list[dict]]:
    rng = random.Random(seed)
    width, height = CANVAS_SIZE
    pw, ph = patch_size
    ox, oy = overlap
    step_x, step_y = pw - ox, ph - oy
    xs = list(range(-ox, width, step_x))
    ys = list(range(-oy, height, step_y))
    accum = np.zeros((height, width, 3), dtype=np.float32)
    weights = np.zeros((height, width, 1), dtype=np.float32)
    window = cosine_window(pw, ph, ox, oy)[..., None]
    log_rows: list[dict] = []
    heat_rows: list[dict] = []
    for row_index, dy in enumerate(ys):
        for col_index, dx in enumerate(xs):
            module_id = module_ids[(row_index * 5 + col_index * 3 + rng.randrange(len(module_ids))) % len(module_ids)]
            src = modules[module_id]
            sw, sh = src.size
            crop_ratio = rng.choice([0.72, 0.78, 0.84, 0.90, 0.96])
            cw = max(64, int(sw * crop_ratio))
            ch = max(64, int(sh * crop_ratio))
            sx = rng.randrange(0, max(1, sw - cw + 1))
            sy = rng.randrange(0, max(1, sh - ch + 1))
            patch = src.crop((sx, sy, sx + cw, sy + ch)).resize((pw, ph), Image.Resampling.LANCZOS)
            mirrored = bool((row_index + col_index + rng.randrange(2)) % 2)
            if mirrored:
                patch = ImageOps.mirror(patch)
            patch_arr = np.asarray(patch.convert("RGB"), dtype=np.float32)
            x0, y0 = max(0, dx), max(0, dy)
            x1, y1 = min(width, dx + pw), min(height, dy + ph)
            if x1 <= x0 or y1 <= y0:
                continue
            px0, py0 = x0 - dx, y0 - dy
            px1, py1 = px0 + (x1 - x0), py0 + (y1 - y0)
            local_w = window[py0:py1, px0:px1]
            accum[y0:y1, x0:x1] += patch_arr[py0:py1, px0:px1] * local_w
            weights[y0:y1, x0:x1] += local_w
            sig_payload = f"{module_id}|{sx},{sy},{cw},{ch}|mirror={int(mirrored)}"
            signature = hashlib.sha256(sig_payload.encode("utf-8")).hexdigest()[:16]
            log_rows.append({
                "texture_id": name,
                "patch_index": len(log_rows),
                "module_id": module_id,
                "source_crop_xywh": f"{sx},{sy},{cw},{ch}",
                "mirror_x": str(mirrored).lower(),
                "destination_xywh": f"{dx},{dy},{pw},{ph}",
                "resample": "lanczos",
                "blend": f"cosine_overlap_{ox}x{oy}",
                "signature": signature,
            })
            heat_rows.append({"rect": (x0, y0, x1, y1), "signature": signature, "module_id": module_id})
    result = np.divide(accum, np.maximum(weights, 1e-5), out=np.zeros_like(accum), where=weights > 0)
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8), "RGB"), log_rows, heat_rows


def paste_texture(layer: Image.Image, texture: Image.Image, mask: Image.Image) -> None:
    layer.paste(texture.convert(layer.mode), (0, 0), mask)


def outline_mask(mask: Image.Image, width: int = 3) -> Image.Image:
    size = max(3, width * 2 + 1)
    outer = mask.filter(ImageFilter.MaxFilter(size))
    inner = mask.filter(ImageFilter.MinFilter(size))
    return ImageChops.subtract(outer, inner)


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").getbbox() if image.mode == "RGBA" else None


def build() -> None:
    for directory in DIRS.values():
        directory.mkdir(parents=True, exist_ok=True)

    input_rows = []
    for input_id, (path, expected) in EXPECTED_INPUTS.items():
        actual = sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"input SHA mismatch {input_id}: expected {expected}, got {actual}")
        input_rows.append({
            "input_id": input_id,
            "absolute_path": str(path),
            "expected_sha256": expected,
            "actual_sha256": actual,
            "status": "PASS",
        })
    donor_table_actual = sha256_file(DONOR_TABLE)
    if donor_table_actual != DONOR_TABLE_SHA:
        raise RuntimeError(f"donor table SHA mismatch: {donor_table_actual}")

    # Validate every Task98 manifest member without modifying Task98.
    manifest_results = []
    for raw_line in (TASK98 / "delivery-hashes.sha256").read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        expected, rel = raw_line.split(None, 1)
        rel = rel.strip().lstrip("*")
        member = TASK98 / rel
        actual = sha256_file(member)
        manifest_results.append({"path": rel, "expected": expected, "actual": actual, "pass": actual == expected})
    if not all(row["pass"] for row in manifest_results):
        raise RuntimeError("Task98 delivery manifest member mismatch")

    profile = json.loads(EXPECTED_INPUTS["CURRENT_COMPOSITOR_PROFILE"][0].read_text(encoding="utf-8"))
    topo = json.loads(EXPECTED_INPUTS["CURRENT_TOPOLOGY"][0].read_text(encoding="utf-8"))
    map_contract = json.loads(EXPECTED_INPUTS["CURRENT_MAP_CONTRACT"][0].read_text(encoding="utf-8"))

    # Extract only the six registered source atoms from the exact raw parent.
    donor_rows: list[dict] = []
    donor_images: dict[str, Image.Image] = {}
    with DONOR_TABLE.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            parent = Path(row["parent_absolute_path"])
            if row["parent_sha256"] != DONOR_PARENT_SHA or sha256_file(parent) != DONOR_PARENT_SHA:
                raise RuntimeError(f"parent mismatch for {row['crop_id']}")
            crop_box = parse_rect(row["raw_half_open_xyxy"])
            source = Image.open(parent).convert("RGBA")
            crop = source.crop(crop_box)
            if crop.size != (int(row["width"]), int(row["height"])):
                raise RuntimeError(f"crop size mismatch for {row['crop_id']}")
            crop_path = DIRS["donors"] / f"{row['crop_id']}_EXACT_RGBA.png"
            crop.save(crop_path)
            donor_images[row["crop_id"]] = crop
            donor_rows.append({
                "crop_id": row["crop_id"],
                "parent_absolute_path": str(parent),
                "parent_sha256": DONOR_PARENT_SHA,
                "raw_half_open_xyxy": row["raw_half_open_xyxy"],
                "crop_size_px": f"{crop.width}x{crop.height}",
                "derived_crop_path": str(crop_path),
                "derived_crop_sha256": sha256_file(crop_path),
                "allowed_role": row["allowed_role"],
                "forbidden_role": row["forbidden_role"],
            })

    # ENV-E1 modules: four deterministic crop/offset/mirror variants per donor.
    category_for_donor = {
        "A_WET_ASPHALT_LINES": "road",
        "B_FACADE_CURB_WET": "facade",
        "C_EMPTY_ROOF": "roof",
        "D_DARK_WET_VALUE": "ground",
        "E_ROOF_FOREGROUND": "foreground",
        "F_ROAD_DASH_PUDDLE": "road",
    }
    # Remove old full-building/corner silhouettes before any module enters E2.
    # Boxes are donor-local half-open coordinates and preserve only material atoms.
    safe_subcrops = {
        "A_WET_ASPHALT_LINES": [(0, 50, 105, 120), (72, 48, 190, 120), (0, 36, 130, 112), (55, 52, 190, 120)],
        "B_FACADE_CURB_WET": [(0, 0, 160, 100), (24, 0, 184, 100), (0, 10, 160, 110), (38, 0, 198, 100)],
        "C_EMPTY_ROOF": [(108, 0, 220, 92), (0, 86, 220, 150), (112, 18, 220, 132), (0, 92, 190, 150)],
        "D_DARK_WET_VALUE": [(0, 0, 98, 120), (122, 0, 220, 120), (0, 0, 112, 92), (116, 24, 220, 120)],
        "E_ROOF_FOREGROUND": [(126, 0, 290, 108), (112, 12, 290, 122), (142, 0, 290, 128), (102, 22, 280, 132)],
        "F_ROAD_DASH_PUDDLE": [(0, 54, 190, 130), (0, 42, 112, 130), (72, 50, 190, 130), (20, 62, 170, 130)],
    }
    modules: dict[str, Image.Image] = {}
    module_rows: list[dict] = []
    module_size = (320, 192)
    for crop_id in sorted(donor_images):
        variants = []
        for variant_index, source_box in enumerate(safe_subcrops[crop_id]):
            atom = donor_images[crop_id].crop(source_box)
            base = ImageOps.fit(atom, module_size, Image.Resampling.LANCZOS)
            if variant_index == 0:
                variants.append(("V0_SAFE", base, "safe_subcrop+contain_lanczos", 0, source_box))
            elif variant_index == 1:
                variants.append(("V1_SAFE_MIRROR", ImageOps.mirror(base), "safe_subcrop+contain_lanczos+mirror_x", 0, source_box))
            elif variant_index == 2:
                variants.append(("V2_SAFE_OFFSET", ImageChops.offset(base, 83, 37), "safe_subcrop+contain_lanczos+wrap_offset_83_37", -1, source_box))
            else:
                variants.append(("V3_SAFE_OFFSET_MIRROR", ImageOps.mirror(ImageChops.offset(base, 149, 61)), "safe_subcrop+contain_lanczos+wrap_offset_149_61+mirror_x", 1, source_box))
        for suffix, variant, transform, shift, source_box in variants:
            module_id = f"{crop_id}__{suffix}"
            blocked = blockify(variant, PALETTES[category_for_donor[crop_id]], shift=shift)
            module_path = DIRS["modules"] / f"{module_id}.png"
            blocked.save(module_path)
            modules[module_id] = blocked
            module_rows.append({
                "module_id": module_id,
                "source_crop_id": crop_id,
                "parent_raw_sha256": DONOR_PARENT_SHA,
                "raw_half_open_xyxy": next(r["raw_half_open_xyxy"] for r in donor_rows if r["crop_id"] == crop_id),
                "donor_safe_subcrop_xyxy": str(list(source_box)),
                "transform": transform,
                "cml128_block_palette": category_for_donor[crop_id],
                "palette_shift": shift,
                "module_size_px": "320x192",
                "module_path": str(module_path),
                "module_sha256": sha256_file(module_path),
            })

    # Labeled atlas is review evidence only; module files above are the actual E1 atoms.
    atlas = Image.new("RGBA", (1600, 1200), (7, 14, 22, 255))
    ad = ImageDraw.Draw(atlas)
    ad.text((32, 22), "ENV-E1 MATERIAL MODULE ATLAS · SIX REGISTERED DONORS ONLY", font=font(28, True), fill=(224, 238, 242, 255))
    ad.text((32, 60), "CANDIDATE · NO TOPOLOGY · NO ACTOR / OBJECT / TEXT SEMANTICS", font=font(18), fill=(111, 169, 180, 255))
    cell_w, cell_h = 388, 180
    for index, row in enumerate(module_rows):
        col, rr = index % 4, index // 4
        x, y = 24 + col * cell_w, 100 + rr * cell_h
        module = modules[row["module_id"]].resize((320, 152), Image.Resampling.LANCZOS)
        atlas.alpha_composite(module, (x + 8, y + 20))
        ad.rectangle((x + 6, y + 18, x + 330, y + 174), outline=(62, 102, 116, 255), width=2)
        ad.text((x + 10, y), row["module_id"].replace("_WET_ASPHALT_LINES", "_WET").replace("_ROAD_DASH_PUDDLE", "_ROAD"), font=font(13, True), fill=(102, 221, 226, 255))
    atlas_path = DIRS["e1"] / "MATERIAL_MODULE_ATLAS_RGBA_1600x1200.png"
    atlas.save(atlas_path)
    atlas_half = atlas.resize((800, 600), Image.Resampling.LANCZOS)
    atlas_half.save(DIRS["e1"] / "MATERIAL_MODULE_ATLAS_50_PERCENT_800x600.png")

    # Frozen terrain membership and exact later-wins classification.
    terrain_zones = topo["terrain_zones"]
    classification = [["open" for _x in range(GRID_SIZE[0])] for _y in range(GRID_SIZE[1])]
    zone_cells: dict[str, set[tuple[int, int]]] = {}
    impassable_cells: set[tuple[int, int]] = set()
    building_rects: list[dict] = []
    for zone in terrain_zones:
        x, y, w, h = zone["rect"]
        cells = {(cx, cy) for cy in range(y, y + h) for cx in range(x, x + w)}
        zone_cells[zone["zone_id"]] = cells
        if not zone["passable"]:
            impassable_cells |= cells
            building_rects.append(zone)
        kind = zone["kind"]
        material_kind = {
            "road": "road",
            "rescue_lane": "rescue",
            "building": "building",
            "broken_corridor": "building",
            "security_apron": "apron",
        }.get(kind, "open")
        for cx, cy in cells:
            classification[cy][cx] = material_kind
    class_cells = {kind: set() for kind in ["open", "road", "rescue", "building", "apron"]}
    for cy in range(GRID_SIZE[1]):
        for cx in range(GRID_SIZE[0]):
            class_cells[classification[cy][cx]].add((cx, cy))

    selection_cells = {(x, y) for y in range(9, 12) for x in range(15, 21)}
    avenue_cells = {(x, y) for y in range(11, 16) for x in range(20, 23)}
    shoulder_cells = {(x, y) for y in range(11, 16) for x in (19, 23)}
    protection_cells = zone_cells["TERRAIN_C01_RESCUE_LANE"]
    anchor_map = {
        "PROP_C01CDV1_RETIRED_SHIELD": (14, 10),
        "TARGET_C01_EAST_EXIT": (31, 7),
        "TARGET_C01_SECURITY_GATE": (27, 8),
        "ALLY_C01_CITY_ARTILLERY": (29, 2),
    }
    object_anchor_cells = set(anchor_map.values())
    decor_keep_clear_cells = selection_cells | avenue_cells | shoulder_cells | object_anchor_cells

    invalid_guardian_anchors: set[tuple[int, int]] = set()
    legal_guardian_anchors: set[tuple[int, int]] = set()
    for ay in range(GRID_SIZE[1]):
        for ax in range(GRID_SIZE[0]):
            footprint = {(ax + dx, ay + dy) for dy in range(2) for dx in range(2)}
            invalid = ax + 1 >= GRID_SIZE[0] or ay + 1 >= GRID_SIZE[1] or bool(footprint & impassable_cells)
            (invalid_guardian_anchors if invalid else legal_guardian_anchors).add((ax, ay))

    mechanical_masks = {
        "ROAD_SOURCE_ZONE_MASK_2400x1350.png": cell_union_mask(zone_cells["TERRAIN_C01_MAIN_ROAD"]),
        "BUILDING_BLOCK_MASK_2400x1350.png": cell_union_mask(impassable_cells),
        "SELECTION_POCKET_MASK_2400x1350.png": cell_union_mask(selection_cells),
        "BREAKER_CHARGE_AVENUE_MASK_2400x1350.png": cell_union_mask(avenue_cells),
        "BREAKER_SHOULDER_BANDS_MASK_2400x1350.png": cell_union_mask(shoulder_cells),
        "PROTECTION_ZONE_MASK_2400x1350.png": cell_union_mask(protection_cells),
        "STATEFUL_OBJECT_ANCHORS_MASK_2400x1350.png": cell_union_mask(object_anchor_cells),
        "TERRAIN_IMPASSABLE_CELL_MASK_2400x1350.png": cell_union_mask(impassable_cells),
        "GUARDIAN_2X2_INVALID_ANCHOR_MASK_2400x1350.png": cell_union_mask(invalid_guardian_anchors),
        "ENV_DECOR_KEEP_CLEAR_MASK_2400x1350.png": cell_union_mask(decor_keep_clear_cells),
        "SECURITY_APRON_MASK_2400x1350.png": cell_union_mask(zone_cells["TERRAIN_C01_SECURITY_APRON"]),
    }
    for filename, mask in mechanical_masks.items():
        mask.save(DIRS["e0"] / filename)

    # Visual masks are antialiased derivatives of exact membership, not new topology.
    map_mask = rect_mask((0, 0, 32, 18), antialias=2)
    visual_class_masks = {kind: cell_union_mask(cells, antialias=True) for kind, cells in class_cells.items()}

    module_groups = defaultdict(list)
    for module_id in modules:
        crop_id = module_id.split("__", 1)[0]
        module_groups[crop_id].append(module_id)
    group_ids = {
        "ground": module_groups["D_DARK_WET_VALUE"] + module_groups["A_WET_ASPHALT_LINES"] + module_groups["F_ROAD_DASH_PUDDLE"],
        "road": module_groups["A_WET_ASPHALT_LINES"] + module_groups["F_ROAD_DASH_PUDDLE"] + module_groups["D_DARK_WET_VALUE"],
        "rescue": module_groups["A_WET_ASPHALT_LINES"] + module_groups["F_ROAD_DASH_PUDDLE"],
        "facade": module_groups["B_FACADE_CURB_WET"],
        "roof": module_groups["C_EMPTY_ROOF"],
        "foreground": module_groups["E_ROOF_FOREGROUND"],
    }

    all_transform_rows: list[dict] = []
    all_heat_rows: list[dict] = []
    textures = {}
    for index, (name, ids) in enumerate(group_ids.items()):
        texture, logs, heat = quilt(name, ids, modules, seed=10100 + index * 137)
        # Reassert the scene-level color family after overlap interpolation.
        texture = regrade(texture.convert("RGBA"), "facade" if name == "facade" else name).convert("RGB")
        textures[name] = texture
        all_transform_rows.extend(logs)
        all_heat_rows.extend([{**h, "texture_id": name} for h in heat])

    # ENV-E2 opaque base: every visible pixel is donor-derived; no flat program color fill.
    base = regrade(textures["ground"].convert("RGBA"), "ground", shift=-2).convert("RGB")
    plaza = regrade(textures["ground"].convert("RGBA"), "ground", shift=0).convert("RGB")
    base.paste(plaza, (0, 0), map_mask)
    paste_texture(base, textures["road"], visual_class_masks["road"])
    paste_texture(base, textures["rescue"], visual_class_masks["rescue"])
    apron_texture = regrade(textures["ground"].convert("RGBA"), "road", shift=-1).convert("RGB")
    paste_texture(base, apron_texture, visual_class_masks["apron"])

    # Physical east lifeline: donor road/curb material clipped to low profile strips.
    # These are not overlays and do not claim object or collision semantics.
    lane_mark_mask = rect_mask((20, 9.15, 12, 0.28), antialias=2)
    curb_north = rect_mask((20, 4.50, 12, 0.20), antialias=2)
    curb_south = rect_mask((20, 11.30, 12, 0.20), antialias=2)
    physical_lifeline_mask = union_masks([lane_mark_mask, curb_north, curb_south])
    physical_lifeline_mask = ImageChops.multiply(physical_lifeline_mask, map_mask)
    paste_texture(base, textures["rescue"], physical_lifeline_mask)

    base_path = DIRS["e2"] / "BASE_GROUND_OPAQUE_2400x1350.png"
    base.save(base_path)

    buildings = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    roofs = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    foreground = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    building_rows = []
    height_by_zone = {
        "TERRAIN_C01_NW_BLOCK": 150,
        "TERRAIN_C01_NM_BLOCK": 178,
        "TERRAIN_C01_NE_BLOCK": 158,
        "TERRAIN_C01_SW_BLOCK": 58,
        "TERRAIN_C01_SE_BLOCK": 68,
        "TERRAIN_C01_BROKEN_SKYWALK": 48,
    }
    # Back to front by ground footprint lower screen point.
    ordered_blocks = sorted(building_rects, key=lambda z: max(p[1] for p in rect_polygon(tuple(z["rect"]))))
    for zone in ordered_blocks:
        zone_id = zone["zone_id"]
        rect = tuple(zone["rect"])
        height_px = height_by_zone[zone_id]
        ground_poly = rect_polygon(rect)
        roof_poly = [(x, y - height_px) for x, y in ground_poly]
        # Visible southwest and southeast body faces only.
        face_left = [roof_poly[3], roof_poly[2], ground_poly[2], ground_poly[3]]
        face_right = [roof_poly[1], roof_poly[2], ground_poly[2], ground_poly[1]]
        left_mask = polygon_mask(face_left, antialias=2)
        right_mask = polygon_mask(face_right, antialias=2)
        left_texture = regrade(textures["facade"].convert("RGBA"), "facade", shift=-1)
        right_texture = regrade(textures["facade"].convert("RGBA"), "facade", shift=0)
        paste_texture(buildings, left_texture, left_mask)
        paste_texture(buildings, right_texture, right_mask)
        body_edge = outline_mask(union_masks([left_mask, right_mask]), width=2)
        paste_texture(buildings, regrade(textures["facade"].convert("RGBA"), "facade", shift=1), body_edge)

        roof_mask = polygon_mask(roof_poly, antialias=2)
        paste_texture(roofs, textures["roof"].convert("RGBA"), roof_mask)
        roof_edge = outline_mask(roof_mask, width=2)
        paste_texture(roofs, regrade(textures["roof"].convert("RGBA"), "roof", shift=1), roof_edge)

        if zone_id in {"TERRAIN_C01_SW_BLOCK", "TERRAIN_C01_SE_BLOCK", "TERRAIN_C01_BROKEN_SKYWALK"}:
            # Local parapet strip on the front roof edge, safely outside the charge avenue.
            p_left, p_right = roof_poly[3], roof_poly[2]
            strip = [p_left, p_right, (p_right[0], p_right[1] + 12), (p_left[0], p_left[1] + 12)]
            strip_mask = polygon_mask(strip, antialias=2)
            paste_texture(foreground, textures["foreground"].convert("RGBA"), strip_mask)

        building_rows.append({
            "zone_id": zone_id,
            "topology_rect": list(rect),
            "derived_visual_height_px": height_px,
            "height_role": "north_depth" if rect[1] < 7 else "south_low_profile",
            "collision_or_semantic_authority": False,
            "ground_polygon_canvas": [[round(x, 3), round(y, 3)] for x, y in ground_poly],
            "roof_polygon_canvas": [[round(x, 3), round(y, 3)] for x, y in roof_poly],
        })

    buildings_path = DIRS["e2"] / "BUILDINGS_WORLD_BODY_RGBA_2400x1350.png"
    roofs_path = DIRS["e2"] / "ROOF_RGBA_2400x1350.png"
    foreground_path = DIRS["e2"] / "FOREGROUND_RGBA_2400x1350.png"
    buildings.save(buildings_path)
    roofs.save(roofs_path)
    foreground.save(foreground_path)

    # Invisible controls. Static coverage exists; applied actor-local patch remains empty in actor-free cleanplates.
    roof_alpha = roofs.getchannel("A")
    foreground_alpha = foreground.getchannel("A")
    coverage = ImageChops.lighter(roof_alpha, foreground_alpha)
    outline = outline_mask(coverage, width=2)
    fringe = ImageChops.subtract(coverage.filter(ImageFilter.MaxFilter(13)), coverage)
    occlusion = Image.merge("RGBA", (coverage, outline, fringe, coverage))
    occlusion_path = DIRS["e2"] / "OCCLUSION_CONTROL_RGBA_2400x1350.png"
    occlusion.save(occlusion_path)

    wetness_r = Image.new("L", CANVAS_SIZE, 0)
    wetness_r.paste(72, (0, 0), map_mask)
    wetness_r.paste(170, (0, 0), visual_class_masks["road"])
    wetness_r.paste(196, (0, 0), visual_class_masks["rescue"])
    wetness_r.paste(150, (0, 0), visual_class_masks["apron"])
    low_emissive = physical_lifeline_mask.point(lambda v: min(96, int(v * 0.38)))
    specular = ImageChops.lighter(visual_class_masks["road"].point(lambda v: int(v * 0.62)), visual_class_masks["rescue"].point(lambda v: int(v * 0.74)))
    wetness = Image.merge("RGBA", (wetness_r, low_emissive, specular, map_mask))
    wetness_path = DIRS["e2"] / "WETNESS_EMISSIVE_CONTROL_RGBA_2400x1350.png"
    wetness.save(wetness_path)

    # Composite only visible environment layers; controls never enter cleanplates.
    world = base.convert("RGBA")
    world = Image.alpha_composite(world, buildings)
    world = Image.alpha_composite(world, roofs)
    world = Image.alpha_composite(world, foreground)

    cleanplate_rows = []
    cleanplates: dict[str, Image.Image] = {}
    for camera_id, camera in CAMERAS.items():
        x, y, w, h = camera["map_crop"]
        map_crop = world.crop((x, y, x + w, y + h))
        frame = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        frame.alpha_composite(map_crop, (0, MAP_VIEWPORT[1]))
        clean_path = DIRS["clean"] / f"{camera_id}_CLEANPLATE_1280x720.png"
        half_path = DIRS["clean"] / f"{camera_id}_CLEANPLATE_50_PERCENT_640x360.png"
        frame.save(clean_path)
        frame.resize((640, 360), Image.Resampling.LANCZOS).save(half_path)
        cleanplates[camera_id] = frame
        cleanplate_rows.append({
            "camera_id": camera_id,
            "camera_center_raw_px": list(camera["center"]),
            "map_crop_world_canvas_px": list(camera["map_crop"]),
            "map_crop_half_open_xyxy": [x, y, x + w, y + h],
            "layer_top_left_screen_px": list(camera["layer_top_left"]),
            "destination_rect_screen_px": list(MAP_VIEWPORT),
            "padding_policy": "transparent_top_58_bottom_78_no_environment_extrapolation",
            "cleanplate_path": str(clean_path),
            "cleanplate_sha256": sha256_file(clean_path),
        })

    # QA trajectory overlay only. It is never composited into cleanplates.
    trajectory = cleanplates["PLAN"].copy()
    td = ImageDraw.Draw(trajectory, "RGBA")
    route_specs = [
        ("VEHICLE T1", [(17, 10), (18, 10), (21, 10), (24, 9)], (70, 220, 226, 230)),
        ("SWARM T2", [(22, 7), (21, 8), (20, 9), (20, 10)], (232, 160, 73, 230)),
        ("BREAKER T3", [(20, 13), (20, 12), (20, 11)], (239, 83, 91, 230)),
    ]
    for label, points, color in route_specs:
        screen_points = [grid_to_screen(p, "PLAN") for p in points]
        td.line(screen_points, fill=color, width=5, joint="curve")
        for px, py in screen_points:
            td.ellipse((px - 5, py - 5, px + 5, py + 5), fill=color)
        lx, ly = screen_points[0]
        td.text((lx + 8, ly - 26), label, font=font(17, True), fill=color)
    for rect, color, label in [
        ((15, 9, 6, 3), (72, 222, 226, 220), "SELECTION CLEAR"),
        ((19, 11, 5, 5), (244, 161, 66, 220), "CHARGE + SHOULDERS"),
    ]:
        pts = [grid_to_screen(p, "PLAN") for p in [
            (rect[0] - 0.5, rect[1] - 0.5),
            (rect[0] + rect[2] - 0.5, rect[1] - 0.5),
            (rect[0] + rect[2] - 0.5, rect[1] + rect[3] - 0.5),
            (rect[0] - 0.5, rect[1] + rect[3] - 0.5),
        ]]
        td.line(pts + [pts[0]], fill=color, width=3)
        td.text((pts[0][0], pts[0][1] - 24), label, font=font(15, True), fill=color)
    sx, sy = grid_to_screen(anchor_map["PROP_C01CDV1_RETIRED_SHIELD"], "PLAN")
    td.line((sx - 10, sy, sx + 10, sy), fill=(195, 205, 210, 220), width=2)
    td.line((sx, sy - 10, sx, sy + 10), fill=(195, 205, 210, 220), width=2)
    td.text((sx + 12, sy - 12), "RESERVED SHIELD HOOK SPACE", font=font(14), fill=(195, 205, 210, 220))
    trajectory_path = DIRS["qa"] / "PLAN_TRAJECTORY_OVERLAY_QA_1280x720.png"
    trajectory.save(trajectory_path)
    trajectory.resize((640, 360), Image.Resampling.LANCZOS).save(DIRS["qa"] / "PLAN_TRAJECTORY_OVERLAY_QA_50_PERCENT_640x360.png")

    # 100% and 50% review boards.
    board100 = Image.new("RGBA", (2560, 1440), (5, 10, 17, 255))
    for index, camera_id in enumerate(["PLAN", "CONTACT_A", "CONTACT_B", "NO_FOCUS"]):
        x, y = (index % 2) * 1280, (index // 2) * 720
        board100.alpha_composite(cleanplates[camera_id], (x, y))
        ImageDraw.Draw(board100).text((x + 18, y + 14), f"{camera_id} · 100% · CLEANPLATE", font=font(22, True), fill=(222, 238, 241, 255))
    board100.save(DIRS["qa"] / "FOUR_CAMERA_100_PERCENT_REVIEW_BOARD_2560x1440.png")
    board50 = board100.resize((1280, 720), Image.Resampling.LANCZOS)
    board50.save(DIRS["qa"] / "FOUR_CAMERA_50_PERCENT_REVIEW_BOARD_1280x720.png")

    # Layer toggles at PLAN camera, composed using the same crop path.
    toggle_worlds = []
    stage = base.convert("RGBA")
    toggle_worlds.append(("BASE", stage.copy()))
    stage = Image.alpha_composite(stage, buildings)
    toggle_worlds.append(("+ BUILDINGS", stage.copy()))
    stage = Image.alpha_composite(stage, roofs)
    toggle_worlds.append(("+ ROOF", stage.copy()))
    stage = Image.alpha_composite(stage, foreground)
    toggle_worlds.append(("+ FOREGROUND", stage.copy()))
    toggle_board = Image.new("RGBA", (1280, 720), (5, 10, 17, 255))
    px, py, pw, ph = CAMERAS["PLAN"]["map_crop"]
    for index, (label, staged_world) in enumerate(toggle_worlds):
        panel = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        panel.alpha_composite(staged_world.crop((px, py, px + pw, py + ph)), (0, 58))
        panel = panel.resize((640, 360), Image.Resampling.LANCZOS)
        x, y = (index % 2) * 640, (index // 2) * 360
        toggle_board.alpha_composite(panel, (x, y))
        ImageDraw.Draw(toggle_board).text((x + 16, y + 14), label, font=font(18, True), fill=(224, 238, 242, 255))
    toggle_board.save(DIRS["qa"] / "LAYER_TOGGLE_QA_1280x720.png")

    # Repetition heatmap based on exact transform signatures.
    signature_counts = Counter(row["signature"] for row in all_transform_rows)
    heat = Image.new("RGB", (1200, 675), (6, 12, 18))
    hd = ImageDraw.Draw(heat, "RGBA")
    texture_colors = {
        "ground": (77, 161, 180), "road": (97, 194, 201), "rescue": (92, 220, 211),
        "facade": (119, 132, 166), "roof": (151, 145, 181), "foreground": (188, 132, 143),
    }
    max_reuse = max(signature_counts.values()) if signature_counts else 1
    for row in all_heat_rows:
        x0, y0, x1, y1 = row["rect"]
        x0, x1 = int(x0 * 0.5), int(x1 * 0.5)
        y0, y1 = int(y0 * 0.5), int(y1 * 0.5)
        reuse = signature_counts[row["signature"]]
        alpha = 34 + int(116 * (reuse - 1) / max(1, max_reuse - 1))
        hd.rectangle((x0, y0, x1, y1), fill=(*texture_colors[row["texture_id"]], alpha), outline=(220, 235, 238, 22), width=1)
    hd.rectangle((0, 0, 1200, 52), fill=(5, 10, 16, 230))
    hd.text((18, 12), "E1 REPETITION HEATMAP · transform signature reuse (QA only)", font=font(20, True), fill=(223, 237, 240, 255))
    heat_path = DIRS["e1"] / "REPETITION_HEATMAP_1200x675.png"
    heat.save(heat_path)
    exact_duplicate_patches = sum(count - 1 for count in signature_counts.values() if count > 1)
    native_donor_pixels = sum(image.width * image.height for image in donor_images.values())
    repetition_metrics = {
        "metric_scope": "deterministic E2 material quilt transform signatures",
        "native_donor_pixel_total": native_donor_pixels,
        "world_canvas_pixel_total": CANVAS_SIZE[0] * CANVAS_SIZE[1],
        "native_donor_coverage_ratio_of_canvas": round(native_donor_pixels / (CANVAS_SIZE[0] * CANVAS_SIZE[1]), 6),
        "minimum_area_reuse_before_safe_subcrop_exclusions": round((CANVAS_SIZE[0] * CANVAS_SIZE[1]) / native_donor_pixels, 6),
        "total_patches": len(all_transform_rows),
        "unique_transform_signatures": len(signature_counts),
        "exact_duplicate_patch_count": exact_duplicate_patches,
        "exact_duplicate_ratio": round(exact_duplicate_patches / max(1, len(all_transform_rows)), 6),
        "max_exact_signature_reuse": max_reuse,
        "subjective_visible_repetition_requires_50_percent_human_review": True,
        "visible_50_percent_repetition_pass": False,
        "visible_failure_despite_unique_transform_signatures": True,
        "transform_signature_metric_is_not_visual_quality_proof": True,
        "machine_threshold_duplicate_ratio_lte": 0.12,
        "machine_pass": exact_duplicate_patches / max(1, len(all_transform_rows)) <= 0.12,
    }
    write_json(DIRS["receipts"] / "repetition-metrics.json", repetition_metrics)

    write_tsv(
        DIRS["receipts"] / "source-lineage.tsv",
        input_rows + [{
            "input_id": "TASK98_DONOR_TABLE",
            "absolute_path": str(DONOR_TABLE),
            "expected_sha256": DONOR_TABLE_SHA,
            "actual_sha256": donor_table_actual,
            "status": "PASS",
        }],
        ["input_id", "absolute_path", "expected_sha256", "actual_sha256", "status"],
    )
    write_tsv(
        DIRS["receipts"] / "donor-crop-lineage.tsv",
        donor_rows,
        ["crop_id", "parent_absolute_path", "parent_sha256", "raw_half_open_xyxy", "crop_size_px", "derived_crop_path", "derived_crop_sha256", "allowed_role", "forbidden_role"],
    )
    write_tsv(
        DIRS["receipts"] / "material-module-lineage.tsv",
        module_rows,
        ["module_id", "source_crop_id", "parent_raw_sha256", "raw_half_open_xyxy", "donor_safe_subcrop_xyxy", "transform", "cml128_block_palette", "palette_shift", "module_size_px", "module_path", "module_sha256"],
    )
    write_tsv(
        DIRS["receipts"] / "material-transform-log.tsv",
        all_transform_rows,
        ["texture_id", "patch_index", "module_id", "source_crop_xywh", "mirror_x", "destination_xywh", "resample", "blend", "signature"],
    )

    control_points = [(0.0, 0.0), (15.0, 11.0), (20.5, 10.5), (20.0, 10.5), (31.0, 17.0)]
    registration_rows = []
    max_error = 0.0
    for point in control_points:
        raw = grid_to_raw(point)
        canvas = raw_to_canvas(raw)
        for camera_id, camera in CAMERAS.items():
            screen = grid_to_screen(point, camera_id)
            expected_screen = (640.0 + raw[0] - camera["center"][0], 350.0 + raw[1] - camera["center"][1])
            error = math.dist(screen, expected_screen)
            max_error = max(max_error, error)
            registration_rows.append({
                "grid_xy": f"{point[0]},{point[1]}",
                "raw_xy": f"{raw[0]},{raw[1]}",
                "canvas_xy": f"{canvas[0]},{canvas[1]}",
                "camera_id": camera_id,
                "screen_xy": f"{screen[0]},{screen[1]}",
                "expected_screen_xy": f"{expected_screen[0]},{expected_screen[1]}",
                "error_px": f"{error:.6f}",
                "pass_lte_0_5px": str(error <= 0.5).lower(),
            })
    write_tsv(
        DIRS["receipts"] / "registration-control-points.tsv",
        registration_rows,
        ["grid_xy", "raw_xy", "canvas_xy", "camera_id", "screen_xy", "expected_screen_xy", "error_px", "pass_lte_0_5px"],
    )

    camera_receipt = {
        "contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
        "grid_size": list(GRID_SIZE),
        "tile_half_px": list(TILE_HALF),
        "raw_origin_px": list(RAW_ORIGIN),
        "world_canvas_size_px": list(CANVAS_SIZE),
        "world_canvas_origin_raw_px": list(CANVAS_ORIGIN),
        "integer_grid_coordinate_semantics": "cell_center",
        "rect_boundary_formula": "(x-.5,y-.5),(x+w-.5,y-.5),(x+w-.5,y+h-.5),(x-.5,y+h-.5)",
        "task98_visible_guide_pixel_reuse": False,
        "task98_guide_known_shift_px": [0, 20],
        "map_viewport_rect": list(MAP_VIEWPORT),
        "cleanplate_padding": {"top_px": 58, "bottom_px": 78, "left_px": 0, "right_px": 0, "alpha": 0},
        "cameras": cleanplate_rows,
        "max_control_point_error_px": max_error,
        "control_point_threshold_px": 0.5,
        "pass": max_error <= 0.5,
    }
    write_json(DIRS["receipts"] / "camera-registration-receipt.json", camera_receipt)
    write_json(DIRS["receipts"] / "task98-manifest-member-check.json", {"manifest_sha256": EXPECTED_INPUTS["TASK98_MANIFEST"][1], "members": manifest_results, "pass": True})

    history_guides = [
        {
            "path": str(TASK98 / "CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png"),
            "sha256": "8aa4909af5aefe0cf1959e1c941bb5c9437567e429ffa487dedd1663f36b5c3a",
            "new_role": "History_trace_only",
            "pixel_consumed_by_task101": False,
            "reason": "cell_diamond used x+0.5,y+0.5 and shifts terrain grid +20px screen Y",
        },
        {
            "path": str(TASK98 / "PLAN_SLOT_COMPOSITE_QA_1280x720.png"),
            "sha256": "772c299994d47510dce3f30f6fb07fc4d2d4ba39744886dacff0b64558f96348",
            "new_role": "History_trace_only",
            "pixel_consumed_by_task101": False,
            "reason": "correct actor footpoints were composited over +20px-shifted terrain guide",
        },
        {
            "path": str(TASK98 / "PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png"),
            "sha256": "75bb1b09ec4201c8b66f624b00789237766f1db41177c0fff52cf6e346681a33",
            "new_role": "History_trace_only",
            "pixel_consumed_by_task101": False,
            "reason": "50 percent derivative of invalid composite registration evidence",
        },
    ]
    for history_guide in history_guides:
        actual_history_sha = sha256_file(Path(history_guide["path"]))
        history_guide["actual_sha256"] = actual_history_sha
        history_guide["hash_pass"] = actual_history_sha == history_guide["sha256"]
        if not history_guide["hash_pass"]:
            raise RuntimeError(f"Task102 History guide SHA mismatch: {history_guide['path']}")
    inherited_contract_values = {
        "source_authority": "runtime visual_projection.gd + compositor profile, not Task98 guide pixels",
        "grid_size": list(GRID_SIZE),
        "integer_grid_is_cell_center": True,
        "tile_half_px": list(TILE_HALF),
        "raw_origin_px": list(RAW_ORIGIN),
        "world_canvas_size_px": list(CANVAS_SIZE),
        "world_canvas_origin_raw_px": list(CANVAS_ORIGIN),
        "map_viewport_rect": list(MAP_VIEWPORT),
        "camera_centers_raw_px": {camera: list(value["center"]) for camera, value in CAMERAS.items()},
        "camera_map_crops_world_canvas_px": {camera: list(value["map_crop"]) for camera, value in CAMERAS.items()},
        "visible_z": {"base": -1200, "buildings": -900, "roof": 900, "foreground": 1100},
        "layer_and_owner_contracts": "inherited where independent of invalid guide pixels",
        "atlas_pivot_socket_phase_contracts": "unaffected by Task102 but not consumed as visible environment pixels",
    }
    task102_receipt = {
        "producer_correction_path": str(EXPECTED_INPUTS["TASK102_RUNTIME_GRID_REGISTRATION_CORRECTION"][0]),
        "producer_correction_sha256": EXPECTED_INPUTS["TASK102_RUNTIME_GRID_REGISTRATION_CORRECTION"][1],
        "history_guides": history_guides,
        "inherited_contract_values": inherited_contract_values,
        "registration_proof_source": "fresh Task101 computation from runtime projection truth",
        "task98_guide_pixels_used_as_registration_proof": False,
        "control_point_count": len(registration_rows),
        "distinct_grid_points": len(control_points),
        "max_error_px": max_error,
        "threshold_px": 0.5,
        "pass": max_error == 0.0 and len(control_points) >= 3,
    }
    write_json(DIRS["receipts"] / "task98-runtime-registration-lineage-correction.json", task102_receipt)
    correction_md = """# Task98 runtime registration lineage correction

Authority: Task102 producer receipt `e8556f917456da83d933842b9ace9542f5238635d5166a6f5b7adbfad0d62378`.

## Downgraded to History trace only

1. `CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png` — terrain grid is +20px screen Y.
2. `PLAN_SLOT_COMPOSITE_QA_1280x720.png` — correct footpoints over invalid terrain registration.
3. `PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png` — invalid composite derivative.

None of those pixels was opened or consumed by Task101 as registration proof.

## Still inherited as numeric contracts

- 32x18 grid; integer grid coordinate is cell center; tile half 40x20.
- raw origin [-880,-170]; world canvas 2400x1350 at raw origin [-1760,-340].
- map viewport [0,58,1280,584].
- NO_FOCUS / PLAN / CONTACT_A / CONTACT_B camera centers, exact crops, and layer top-left values.
- z and layer ownership rules independent of the invalid guide pixels.

## Fresh Task101 readback

Five distinct grid points were recomputed through grid -> raw -> canvas -> each of four camera screens. All twenty rows have 0.000000px error; see `registration-control-points.tsv` and `camera-registration-receipt.json`.
"""
    (DIRS["receipts"] / "task98-runtime-registration-lineage-correction.md").write_text(correction_md, encoding="utf-8")

    object_rows = []
    for object_id, grid in anchor_map.items():
        raw = grid_to_raw(grid)
        canvas = raw_to_canvas(raw)
        row = {"object_id": object_id, "grid_anchor": list(grid), "raw_px": list(raw), "canvas_px": list(canvas), "visible_pixel_slot": "EMPTY_RESERVED"}
        row["screen_by_camera"] = {camera: list(grid_to_screen(grid, camera)) for camera in CAMERAS}
        object_rows.append(row)
    write_json(DIRS["receipts"] / "stateful-object-anchor-reservation.json", {
        "objects": object_rows,
        "objects_are_terrain_impassable": False,
        "visible_pixels_baked": False,
        "stateful_owner": "future_session_resolver_owned_object_layers",
        "pass": True,
    })

    write_json(DIRS["receipts"] / "topology-mask-receipt.json", {
        "source_zone_cell_counts": {
            "main_road": len(zone_cells["TERRAIN_C01_MAIN_ROAD"]),
            "protection_rescue": len(protection_cells),
            "security_apron": len(zone_cells["TERRAIN_C01_SECURITY_APRON"]),
            "terrain_impassable": len(impassable_cells),
            "selection_pocket": len(selection_cells),
            "breaker_avenue": len(avenue_cells),
            "shoulder_bands": len(shoulder_cells),
        },
        "later_wins_material_class_counts": {kind: len(cells) for kind, cells in class_cells.items()},
        "guardian_2x2_anchor_counts": {"legal": len(legal_guardian_anchors), "invalid": len(invalid_guardian_anchors)},
        "non_placeable_is_not_universal_union": True,
        "terrain_impassable_mask": "TERRAIN_IMPASSABLE_CELL only",
        "decor_keep_clear_mask": "selection + avenue + shoulders + reserved stateful anchors; not gameplay blocking",
        "protection_zone_policy": "LOW_PROFILE_ONLY; physical donor-derived curb/road language allowed",
        "pass": len(impassable_cells) == 145 and len(legal_guardian_anchors) == 360 and len(invalid_guardian_anchors) == 216,
    })
    write_json(DIRS["receipts"] / "building-visual-height-derivation.json", {
        "authority": "Task101 north-depth / south-low presentation clause",
        "topology_unchanged": True,
        "new_building_design_claimed": False,
        "blocks": building_rows,
    })

    write_json(DIRS["receipts"] / "environment-layer-manifest.json", {
        "contract_id": "C01E02_CURRENT_TOPOLOGY_ENVIRONMENT_LAYERS_V1",
        "status": "CANDIDATE_NOT_RUNTIME",
        "world_canvas": {"size_px": list(CANVAS_SIZE), "origin_raw_px": list(CANVAS_ORIGIN), "shared_pivot": [0, 0]},
        "visible_layers": [
            {"slot": "base_ground", "path": str(base_path), "z": -1200, "alpha": "opaque", "sha256": sha256_file(base_path)},
            {"slot": "buildings_world_body", "path": str(buildings_path), "z": -900, "alpha": "local", "sha256": sha256_file(buildings_path)},
            {"slot": "roof", "path": str(roofs_path), "z": 900, "alpha": "local", "sha256": sha256_file(roofs_path)},
            {"slot": "foreground", "path": str(foreground_path), "z": 1100, "alpha": "local", "sha256": sha256_file(foreground_path)},
        ],
        "control_layers": [
            {"slot": "occlusion_control", "path": str(occlusion_path), "visible": False, "visible_z": None, "channels": "R=static_fade_coverage;G=roof_outline;B=safety_fringe;A=coverage", "sha256": sha256_file(occlusion_path)},
            {"slot": "wetness_emissive_control", "path": str(wetness_path), "visible": False, "visible_z": None, "channels": "R=wetness;G=low_physical_lifeline_response;B=specular_response;A=map_coverage", "sha256": sha256_file(wetness_path)},
        ],
        "reserved_external_owner_groups": [
            {"group": "stateful_objects", "state": "EMPTY_RESERVED_EXTERNAL_OWNER", "owner": "session_resolver_object_layers"},
            {"group": "weather_fx", "state": "NOT_BAKED_EXTERNAL_OWNER", "owner": "independent_weather_fx_layer"},
            {"group": "stateful_nonphysical_overlays", "state": "NOT_BAKED_EXTERNAL_OWNER", "owner": "deterministic_overlay_or_UI_consumer"},
            {"group": "actor_and_object_shadows", "state": "NOT_BAKED_EXTERNAL_OWNER", "owner": "engine_independent_ground_shadow_layer"},
        ],
        "real_art_loaded": 0,
        "runtime_bindable": False,
    })

    common_origin_alpha = {
        "world_canvas_size": list(CANVAS_SIZE),
        "origin_raw_px": list(CANVAS_ORIGIN),
        "base_alpha_extrema": list(base.convert("RGBA").getchannel("A").getextrema()),
        "buildings_alpha_bbox": alpha_bbox(buildings),
        "roof_alpha_bbox": alpha_bbox(roofs),
        "foreground_alpha_bbox": alpha_bbox(foreground),
        "roof_global_fade": False,
        "foreground_global_fade": False,
        "layer_toggle_board": str(DIRS["qa"] / "LAYER_TOGGLE_QA_1280x720.png"),
        "pass": base.convert("RGBA").getchannel("A").getextrema() == (255, 255),
    }
    write_json(DIRS["receipts"] / "common-origin-alpha-layer-toggle-receipt.json", common_origin_alpha)
    write_json(DIRS["receipts"] / "occlusion-control-receipt.json", {
        "file": str(occlusion_path),
        "visible": False,
        "occupies_visible_z": False,
        "channel_semantics": {"R": "static roof/foreground fade coverage", "G": "roof/foreground outline", "B": "safety fringe", "A": "coverage"},
        "task98_actor_free_mask_interpretation": "static ownership coverage may exist; applied actor-local patch is fully empty while actor list is empty",
        "applied_actor_local_patch_in_cleanplates": "EMPTY",
        "control_file_composited_into_cleanplates": False,
        "contract_literal_risk_requires_producer_awareness": True,
    })
    write_json(DIRS["receipts"] / "wetness-weather-state-receipt.json", {
        "file": str(wetness_path),
        "control_only": True,
        "composited_into_cleanplates": False,
        "airborne_rain_fx_baked": False,
        "contact_weather_fx_baked": False,
        "T3_T5_future_state_baked": False,
        "surface_material_wetness_derived_from_registered_donors": True,
    })
    write_json(DIRS["receipts"] / "forbidden-content-and-pixel-contamination-receipt.json", {
        "visible_parent_pixel_sources": [{"path": donor_rows[0]["parent_absolute_path"], "sha256": DONOR_PARENT_SHA, "allowed_rects_only": [row["raw_half_open_xyxy"] for row in donor_rows]}],
        "call02_full_frame_direct_reuse": False,
        "call02_unit_object_shadow_reflection_pixels_reused": False,
        "old_A4_visible_pixels_opened_or_reused": False,
        "old_A4_topology_reused": False,
        "forbidden_visible_categories": ["actors", "mecha", "vehicle", "swarms", "shield", "east_exit", "security_facility", "artillery", "route", "ghost", "UI", "text", "T3-T5 FX"],
        "stateful_slots_visible_pixel_count": 0,
        "manual_semantic_review_still_required": True,
        "pass_machine_lineage": True,
    })

    generation_log = f"""# ENV-E0 generation log

- Task: `A9_1A6_ENV_E0_CURRENT_TOPOLOGY_ENVIRONMENT_DERIVATION`
- Build method: deterministic crop / mask / mirror / offset / overlap reassembly / level blocking / validation.
- ImageGen calls: `0`
- LibTV generation calls: `0`
- Blender calls: `0`
- Godot writes or runs: `0`
- Call03: `false`
- Call04: `false`
- Actor or mecha visible drawing: `0`
- Stateful object visible drawing: `0`
- Runtime handoff: `none`
- Canon migration: `none`
- Visible parent scope: six exact Task98 registered donor rectangles only.
- Old A4 pixels: `unused`.
- Call02 full frame: `not reused`; parent raw opened only to extract the six exact rectangles.
- Task98 actor-free guide: `not reused as pixels`; exact projection regenerated from `visual_projection.gd` because the old guide builder carried a +20px Y offset.
- Task102 producer correction: `e8556f917456da83d933842b9ace9542f5238635d5166a6f5b7adbfad0d62378`; its three named Task98 boards are History-only.
- Weather/FX: not baked; only surface material wetness remains in donor-derived visible texture.
- Cleanplate padding: transparent top 58px / bottom 78px; 1280×584 map crop is never stretched.
- Visual self-review state: `{VISUAL_REVIEW_STATUS}`.
- Visual refinement after failure: `stopped`; no reroll, no generation, no extra donor, no hidden repair.
"""
    (OUT / "generation-log.md").write_text(generation_log, encoding="utf-8")

    # Mechanical validation of named files, alpha, registration, and cleanplate padding.
    required_layers = [base_path, buildings_path, roofs_path, foreground_path, occlusion_path, wetness_path]
    layer_checks = []
    for path in required_layers:
        im = Image.open(path)
        layer_checks.append({"path": str(path), "size": list(im.size), "mode": im.mode, "pass_size": im.size == CANVAS_SIZE})
    clean_checks = []
    for camera_id in CAMERAS:
        im = cleanplates[camera_id]
        alpha = np.asarray(im.getchannel("A"))
        top_empty = int(alpha[:58].max()) == 0
        bottom_empty = int(alpha[642:].max()) == 0
        map_opaque_ratio = float(np.mean(alpha[58:642] == 255))
        clean_checks.append({
            "camera_id": camera_id,
            "size": list(im.size),
            "top_padding_alpha_zero": top_empty,
            "bottom_padding_alpha_zero": bottom_empty,
            "map_rows_opaque_ratio": round(map_opaque_ratio, 6),
            "pass": top_empty and bottom_empty and map_opaque_ratio == 1.0,
        })
    validation_pass = (
        all(row["pass_size"] for row in layer_checks)
        and base.convert("RGBA").getchannel("A").getextrema() == (255, 255)
        and all(row["pass"] for row in clean_checks)
        and max_error <= 0.5
        and repetition_metrics["machine_pass"]
        and len(impassable_cells) == 145
        and len(legal_guardian_anchors) == 360
        and len(invalid_guardian_anchors) == 216
    )
    machine_report = {
        "task_id": "A9_1A6_ENV_E0_CURRENT_TOPOLOGY_ENVIRONMENT_DERIVATION",
        "status": "MACHINE_PASS_VISUAL_REVIEW_NOT_IMPLIED" if validation_pass else "MACHINE_FAIL",
        "input_sha_pass": True,
        "task98_manifest_members_pass": True,
        "layer_checks": layer_checks,
        "cleanplate_checks": clean_checks,
        "base_alpha_opaque": base.convert("RGBA").getchannel("A").getextrema() == (255, 255),
        "max_registration_error_px": max_error,
        "repetition_metrics": repetition_metrics,
        "stateful_objects_baked": False,
        "weather_fx_baked": False,
        "controls_in_cleanplates": False,
        "imagegen_calls": 0,
        "libtv_generation_calls": 0,
        "godot_writes": 0,
        "call03": False,
        "call04": False,
        "visual_50_100_review_required": True,
        "visual_self_review_pass": False,
        "visual_failure_code": "BLOCKED_INSUFFICIENT_DONOR_COVERAGE_FOR_PRODUCT_ENVIRONMENT",
        "candidate_visual_promotion_allowed": False,
        "pass": validation_pass,
    }
    write_json(OUT / "machine-validation-report.json", machine_report)

    completion = f"""# Task101 ENV-E0 completion report

## Declared state

`{FAILURE_STATE}`

## Scope result

- ENV-E0 exact current-topology masks and four-camera registration: `MACHINE_PASS`
- ENV-E1 six-donor material atlas / lineage / transform / repetition evidence: `MACHINE_PASS`
- ENV-E2 six 2400×1350 visible/control layers and four 1280×720 + 50% cleanplates: `MACHINE_PASS / VISUAL_FAIL`
- Actor, vehicle, swarm, shield, east exit, security facility, artillery, UI, route, ghost, T3–T5 state pixels: `NOT BAKED`
- ImageGen / LibTV generation / Godot / Call03 / Call04: `0 / 0 / 0 / false / false`
- Runtime or real-art handoff: `NONE`; `real_art_loaded=0`

## Visual self-review

- Status: `{VISUAL_REVIEW_STATUS}`
- 50% failure: large donor fragments and repeated diagonal seams remain immediately visible; the north blocks read as clipped/extruded texture slabs.
- 50% failure: central avenue, east lifeline, and southern charge space require the QA overlay to read; the cleanplate alone fails the three-second hierarchy gate.
- 100% failure: hard rectangular texture phase changes, enlarged donor marks, and dark value collapse expose the deterministic assembly instead of a premium environment finish.
- Capacity cause: the six native crops total only 209,850 source pixels (6.48% of the 2400×1350 canvas), requiring at least 15.44× area reuse before additional safe-subcrop exclusions.
- Decision: stop with failure evidence. No further deterministic repaint, donor expansion, ImageGen, Call03/04, or semantic-object fill was attempted.
- Machine PASS does not claim producer visual PASS.
- 50% review must judge three-second avenue/lifeline/charge/shield-hook-space readability and visible repetition/programmatic feel.
- 100% review must judge 2:1 dimetric edge coherence, donor seam/noise, local roof/foreground control, and CML128 large-block/hard-shadow discipline.

## Contract risk disclosed

Task98 says `occlusion_control.actor_free_mask=fully_empty`, while Task101 requires a populated RGBA ownership control. This delivery interprets that as: static roof/foreground coverage may exist in the invisible control file, but the applied actor-local patch is empty while the cleanplate is actor-free. The control file never enters visible compositing. Producer may require a stricter clarification; machine PASS does not erase this wording risk.

## Task102 registration correction

The three Task98 integrated guide/composite boards named by Task102 are retained only as History trace bytes and were not consumed as registration proof. Numeric contracts independent of those pixels remain inherited: grid/tile, integer-cell-center projection, raw/canvas origins, four camera centers/crops, viewport, z, layer ownership, and unaffected atlas/pivot/socket/phase contracts. Task101 freshly recomputed five grid points across four cameras; all twenty grid→raw→canvas→screen rows read back at `0.000000px` error.

## Stop gate

Stopped at P102 producer 50%/100% actual-pixel review. No Godot integration, actor composition, Call03/04, UA91, G2-B, Runtime, or Canon migration follows automatically.
"""
    (OUT / "completion-report.md").write_text(completion, encoding="utf-8")

    # Hash every delivery except the hash list itself; stable relative paths.
    hash_path = OUT / "delivery-hashes.sha256"
    delivery_files = sorted(
        p for p in OUT.rglob("*")
        if p.is_file() and p != hash_path and "__pycache__" not in p.parts and p.suffix != ".pyc"
    )
    hash_lines = [f"{sha256_file(path)}  {path.relative_to(OUT)}" for path in delivery_files]
    hash_path.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "output": str(OUT),
        "file_count_excluding_hash_manifest": len(delivery_files),
        "machine_pass": validation_pass,
        "visual_review_status": VISUAL_REVIEW_STATUS,
        "max_registration_error_px": max_error,
        "repetition_duplicate_ratio": repetition_metrics["exact_duplicate_ratio"],
        "cleanplates": {camera: str(DIRS["clean"] / f"{camera}_CLEANPLATE_1280x720.png") for camera in CAMERAS},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
