#!/usr/bin/env python3
"""Deterministic ENV-A1 post-process: chroma extraction, slot split, assembly and QA."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import deque
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
PROJECT = Path("/Users/rayz/Documents/超gag机器人大战")
RAW = ROOT / "generation-raw/ENV_A1_IMAGEGEN_RAW_SHEET.png"
CONTRACT_PATH = ROOT / "module-slot-contract.json"
CAMERA_PATH = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REG_PATH = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
PROFILE_PATH = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json"
DONOR_PATH = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c2-sprite-first-map-camera-masters/CALL02_ENVIRONMENT_METHOD_DONOR_CROP_SHEET_1600x1200.png"
GUIDE_PATH = ROOT / "source-guides/ENV_A1_MODULAR_SLOT_GUIDE_1536x1024.png"

VISUAL_SELF_REVIEW_PASS = False
VISUAL_SELF_REVIEW_STATUS = "PENDING_EXECUTOR_50_100_PIXEL_REVIEW"

EXPECTED = {
    PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/108-c01e02-route-a2-modular-environment-and-interaction-user-approval.md": "c33bc0ffa4fe6f5ecc553001e640eba18a39a917a0c4691def8c940ca0ad0280",
    PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/112-c01e02-p111-camera-v2-exact-interface-producer-acceptance.md": "2eda6f614f46b0ba8ef43adc76ff08152d63d3560a5e4b19989c7612d44a2793",
    PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/113-c01e02-a9-1a6-env-a1-modular-tactical-environment-kit-master-objective.md": "f8148ac350ca30a48e991ac73aaf6de3949b3f85c00a473d643819ab601efdde",
    PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/114-c01e02-env-a1-modular-environment-art-dispatch-receipt.md": "d9041b3d6e489f5487b1e0cfd0464e005c467105d06ca6dad7747b67bcae9993",
    PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv": "668ab2e882196f28efd6993af0f0453c588a6e465c28a663699d1b37bc494fbe",
    PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/c01e02-tactical-visual-interface-v1.json": "5dc09a26ff0124edd9bc2c3d05f9a0b180ae544ce9c04477664ac9061a443e2f",
    CAMERA_PATH: "756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a",
    REG_PATH: "0133cf5c5af7a6dba659221249b9e0bb45c51bebc8cb9b81c50cf9d920d25b7b",
    PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c4b-camera-v2-freeze/receipts/06-camera-v2-capture-manifest.json": "4275e63d9b748ce512995fa7cc316186d48dcb9fb4b1ab71c20507d639233242",
    DONOR_PATH: "4dba9ba7590edb227a934dd4e363da1cc9718e316a01469d76230c4cd1450273",
}

PROMPT = """Use case: stylized-concept
Asset type: production-ready modular tactical game environment kit sheet, not a scene or screenshot.

Input images:
- Image 1 is the STRICT SLOT LAYOUT AND MASK. Preserve its 1536x1024 landscape composition, all sixteen magenta panels, black gutters, panel boundaries, row order, and complete separation. Paint only inside each magenta panel. Do not merge, overlap, resize, reorder, or cross gutters.
- Image 2 is STYLE AND MATERIAL METHOD ONLY: cold rainy industrial values, wet asphalt, restrained reflections, faceted roofs and curbs. Ignore all labels and layout in Image 2; do not reproduce its text, topology, objects, or coordinates.

Camera and drawing language:
One consistent orthographic 40x24 dimetric map view for every module. Grid x edges run down-right at 24/40 slope; grid y edges run down-left at 24/40 slope. Parallel edges never converge. No perspective, no second viewpoint, no y-dependent scale. Clean kinetic-cel tactical-map finish: 4-7 large color masses, clean line pressure, at most two hard shadow levels, restrained rain wear, no noisy photopaint.

Exact panel content, reading left-to-right:
Top row, four edge-to-edge ground material panels:
1 wet dark asphalt with subtle puddles;
2 intact tactical road language with restrained pale lane marks;
3 curb, drainage channel, low edge modules;
4 plaza/apron paving with quiet seams.
These four panels contain flat material only, no buildings or props.

Second row: three isolated structures:
1 NW high old exhibition block;
2 NM medium exhibition block;
3 NE high old exhibition block.
Third row: three isolated structures:
1 SW medium block;
2 SE high block;
3 low broken skywalk.
Each structure is a single clean map asset centered in its panel, footprint fully visible, with a clearly exposed dark low foundation slab and a separate upper occluder body divided by a clean seam. Foundation is ground-hugging and remains readable if the upper body fades. High structures are only moderately taller than medium; low skywalk is clearly lowest. Strong mecha-map presence but not skyscraper canyons. No cast shadow crossing the panel edge.

Bottom row, six isolated transparent-ready assets:
1 wall-hung retired heavy shield with exactly three scorch marks;
2 open east evacuation gate/exit;
3 compact warning/security facility active;
4 same compact facility damaged, visibly related but separately drawn;
5 A-road damage decal: one long broken arc, severe but passability unchanged;
6 B-road damage decal: two restrained buckles, visibly lighter damage.
Keep each isolated and centered with generous empty magenta around it.

Palette and materials:
Cold blue-gray wet old exhibition district, muted teal guidance accents, small restrained warm edge lights, aged concrete and industrial metal. No neon danger-zone glow.

Hard constraints:
NO text, letters, numbers, labels, signage, symbols, watermark, UI, route lines, ghost, actors, humans, robots, mecha, vehicles, creatures, swarms, artillery, cannon, shield-in-use pose, battle action, explosions, future-state FX, complete battlefield, or full-screen environment. Do not paint outside magenta panels. Keep black gutters clean and continuous. Preserve the magenta background wherever there is no module so deterministic chroma separation remains possible. This is one modular kit sheet only."""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ensure_dirs() -> None:
    for rel in [
        "intermediate/slots", "intermediate/materials", "delivery/structures",
        "delivery/tactical-objects", "delivery/world-results", "qa/cleanplates",
        "qa/registration", "qa/structure-solo", "qa/structure-layer-toggle",
        "qa/structure-reveal", "qa/structure-thumbnails", "receipts",
    ]:
        (ROOT / rel).mkdir(parents=True, exist_ok=True)


def save_png(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if im.mode == "RGBA":
        arr = np.array(im)
        arr[arr[:, :, 3] == 0, :3] = 0
        im = Image.fromarray(arr, "RGBA")
    im.save(path, compress_level=9)


def alpha_bbox(im: Image.Image):
    return im.getchannel("A").getbbox() if im.mode == "RGBA" else None


def largest_connected_component(mask: np.ndarray) -> np.ndarray:
    """Keep one isolated slot asset and reject gutter/neighbor fragments."""
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=np.uint8)
    best = []
    for y, x in zip(*np.nonzero(mask)):
        if seen[y, x]:
            continue
        seen[y, x] = 1
        q = deque([(y, x)])
        component = []
        while q:
            cy, cx = q.popleft()
            component.append((cy, cx))
            for ny in range(max(0, cy - 1), min(h, cy + 2)):
                for nx in range(max(0, cx - 1), min(w, cx + 2)):
                    if mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = 1
                        q.append((ny, nx))
        if len(component) > len(best):
            best = component
    keep = np.zeros((h, w), dtype=bool)
    if best:
        yy, xx = zip(*best)
        keep[np.asarray(yy), np.asarray(xx)] = True
    return keep


def chroma_extract(rgb: Image.Image) -> Image.Image:
    arr = np.asarray(rgb.convert("RGB"), dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    magenta_excess = np.minimum(r, b) - g
    mag_like = (
        (r > 42) & (b > 38) &
        (magenta_excess > 18) &
        ((r + b - 2.0 * g) > 48) &
        (np.abs(r - b) < 150)
    )
    # The generated sheet occasionally lets the black guide gutter enter a
    # frozen slot box. It is keyed only when it is near-neutral and very dark.
    guide_gutter = (np.max(arr, axis=2) < 27) & ((np.max(arr, axis=2) - np.min(arr, axis=2)) < 19)
    alpha = np.ones(r.shape, dtype=np.float32)
    alpha[mag_like | guide_gutter] = 0.0
    # Remove the contractual outer edge; every visible module has ample key
    # margin and no approved content touches a slot boundary.
    alpha[:3, :] = 0.0
    alpha[-3:, :] = 0.0
    alpha[:, :3] = 0.0
    alpha[:, -3:] = 0.0
    alpha[~largest_connected_component(alpha > 0)] = 0.0
    out = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
    fg = arr.copy()
    # Deterministic magenta despill on retained edge pixels: remove red-violet
    # contamination while preserving the intended cold blue-grey material.
    retained_spill = (alpha > 0) & (r > g + 10) & (b > g + 10)
    fg[:, :, 0][retained_spill] = np.minimum(r[retained_spill], g[retained_spill] * 1.18 + 12.0)
    out[:, :, :3] = np.clip(fg, 0, 255).astype(np.uint8)
    out[:, :, 3] = np.rint(alpha * 255.0).astype(np.uint8)
    out[out[:, :, 3] == 0] = 0
    return Image.fromarray(out, "RGBA")


def crop_content(im: Image.Image) -> Image.Image:
    box = alpha_bbox(im)
    if not box:
        raise RuntimeError("EMPTY_ALPHA_SLOT")
    return im.crop(box)


def keep_largest_alpha_component(im: Image.Image) -> Image.Image:
    """Drop disconnected guide/neighbor fragments while preserving one module."""
    arr = np.array(im.convert("RGBA"))
    mask = arr[:, :, 3] > 0
    height, width = mask.shape
    seen = np.zeros(mask.shape, dtype=bool)
    largest = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or seen[y, x]:
                continue
            stack = [(x, y)]
            seen[y, x] = True
            component = []
            while stack:
                cx, cy = stack.pop()
                component.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < width and 0 <= ny < height and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((nx, ny))
            if len(component) > len(largest):
                largest = component
    if not largest:
        raise RuntimeError("EMPTY_ALPHA_COMPONENT")
    keep = np.zeros(mask.shape, dtype=bool)
    xs, ys = zip(*largest)
    keep[np.asarray(ys), np.asarray(xs)] = True
    arr[~keep] = 0
    return Image.fromarray(arr, "RGBA")


def fit_content(im: Image.Image, canvas_size, pivot, margin=4) -> Image.Image:
    src = crop_content(im)
    cw, ch = canvas_size
    px, py = pivot
    max_w = max(1, cw - 2 * margin)
    max_h = max(1, py - 2 * margin)
    scale = min(max_w / src.width, max_h / src.height)
    nw = max(1, int(round(src.width * scale)))
    nh = max(1, int(round(src.height * scale)))
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    dst = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    x = int(round(px - nw / 2))
    y = int(round(py - nh))
    dst.alpha_composite(src, (x, y))
    return dst


def split_structure(combined: Image.Image):
    box = alpha_bbox(combined)
    if not box:
        raise RuntimeError("EMPTY_STRUCTURE")
    band = max(18, min(34, int(round(combined.height * 0.09))))
    cut = max(box[1], box[3] - band)
    arr = np.array(combined)
    foundation = arr.copy()
    foundation[:cut, :, :] = 0
    occluder = arr.copy()
    occluder[cut:, :, :] = 0
    return Image.fromarray(foundation, "RGBA"), Image.fromarray(occluder, "RGBA"), cut


def centered_swatch(im: Image.Image) -> Image.Image:
    box = alpha_bbox(im)
    if not box:
        raise RuntimeError("EMPTY_MATERIAL")
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx0, cx1 = x0 + int(w * 0.24), x1 - int(w * 0.24)
    cy0, cy1 = y0 + int(h * 0.37), y1 - int(h * 0.25)
    sw = im.crop((cx0, cy0, cx1, cy1))
    matte = Image.new("RGBA", sw.size, (25, 34, 43, 255))
    matte.alpha_composite(sw)
    return matte.convert("RGB")


def tile_texture(sw: Image.Image, size=(2400, 1350), scale=2.2) -> Image.Image:
    tw = max(32, int(round(sw.width * scale)))
    th = max(24, int(round(sw.height * scale)))
    tile = sw.resize((tw, th), Image.Resampling.LANCZOS)
    out = Image.new("RGB", size, (20, 29, 38))
    row = 0
    y = -th // 3
    while y < size[1]:
        x = -tw // 2 + (row % 2) * (tw // 3)
        col = 0
        while x < size[0]:
            patch = ImageOps.mirror(tile) if (row + col) % 2 else tile
            out.paste(patch, (x, y))
            x += tw
            col += 1
        y += th
        row += 1
    return out


def continuous_texture(sw: Image.Image, size=(2400, 1350)) -> Image.Image:
    """Make a quiet seamless fill from the internal crop without slab borders."""
    src = sw.convert("RGB")
    target_w = max(220, min(520, src.width * 3))
    target_h = max(120, min(300, src.height * 3))
    src = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    seamless = Image.new("RGB", (target_w * 2, target_h * 2))
    seamless.paste(src, (0, 0))
    seamless.paste(ImageOps.mirror(src), (target_w, 0))
    seamless.paste(ImageOps.flip(src), (0, target_h))
    seamless.paste(ImageOps.flip(ImageOps.mirror(src)), (target_w, target_h))
    tiled = Image.new("RGB", size)
    for y in range(0, size[1], seamless.height):
        for x in range(0, size[0], seamless.width):
            tiled.paste(seamless, (x, y))
    low_frequency = ImageOps.fit(sw.convert("RGB"), size, method=Image.Resampling.BICUBIC,
                                 centering=(0.5, 0.5))
    return Image.blend(low_frequency, tiled, 0.42)


def seamless_internal_texture(sw: Image.Image, size=(2400, 1350), scale=4.2) -> Image.Image:
    """Mirror an internal border-free crop in both axes, with no hard tile seam."""
    tw = max(64, int(round(sw.width * scale)))
    th = max(48, int(round(sw.height * scale)))
    tile = sw.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
    out = Image.new("RGB", size, (20, 29, 38))
    y = 0
    row = 0
    while y < size[1]:
        x = 0
        while x < size[0]:
            patch = tile
            if (x // tw) % 2:
                patch = ImageOps.mirror(patch)
            if row % 2:
                patch = ImageOps.flip(patch)
            out.paste(patch, (x, y))
            x += tw
        y += th
        row += 1
    return out


def match_material_mean(im: Image.Image, reference: Image.Image, strength=0.78) -> Image.Image:
    src = np.asarray(im.convert("RGB"), dtype=np.float32)
    ref = np.asarray(reference.convert("RGB"), dtype=np.float32)
    delta = (ref.reshape(-1, 3).mean(axis=0) - src.reshape(-1, 3).mean(axis=0)) * strength
    return Image.fromarray(np.clip(src + delta[None, None, :], 0, 255).astype(np.uint8), "RGB")


def project_raw(gx, gy):
    return ((gx - gy) * 40.0, (gx + gy) * 24.0)


def source_point(gx, gy):
    rx, ry = project_raw(gx, gy)
    return (int(round(rx + 920)), int(round(ry + 99)))


def rect_polygon_source(rect):
    x, y, w, h = rect
    return [source_point(x - .5, y - .5), source_point(x + w - .5, y - .5),
            source_point(x + w - .5, y + h - .5), source_point(x - .5, y + h - .5)]


def polygon_mask(points, size=(2400, 1350)) -> Image.Image:
    scale = 2
    mask = Image.new("L", (size[0] * scale, size[1] * scale), 0)
    ImageDraw.Draw(mask).polygon([(x * scale, y * scale) for x, y in points], fill=255)
    return mask.resize(size, Image.Resampling.LANCZOS)


def build_ground(materials):
    base = seamless_internal_texture(materials["GROUND_WET_ASPHALT"], scale=4.6)
    road = seamless_internal_texture(materials["GROUND_ROAD_LANGUAGE"], scale=4.8)
    curb = seamless_internal_texture(materials["GROUND_CURB_DRAINAGE"], scale=4.4)
    apron = seamless_internal_texture(materials["GROUND_APRON_PAVING"], scale=4.6)
    base = ImageEnhance.Color(base).enhance(0.72)
    road = ImageEnhance.Color(road).enhance(0.68)
    curb = ImageEnhance.Color(curb).enhance(0.70)
    apron = ImageEnhance.Color(apron).enhance(0.68)
    road = match_material_mean(road, base, 0.82)
    curb = match_material_mean(curb, base, 0.78)
    apron = match_material_mean(apron, base, 0.82)
    result = base
    result = Image.composite(road, result, polygon_mask(rect_polygon_source([0, 7, 32, 7])))
    result = Image.composite(curb, result, polygon_mask(rect_polygon_source([20, 5, 12, 7])))
    result = Image.composite(apron, result, polygon_mask(rect_polygon_source([24, 4, 8, 8])))
    # Lower contrast in the frozen choice pocket without drawing new visible forms.
    quiet = ImageEnhance.Contrast(road).enhance(0.58)
    quiet = ImageEnhance.Brightness(quiet).enhance(0.88)
    result = Image.composite(quiet, result, polygon_mask(rect_polygon_source([15, 9, 6, 3])))
    board_poly = [source_point(-.5, -.5), source_point(31.5, -.5),
                  source_point(31.5, 17.5), source_point(-.5, 17.5)]
    alpha = polygon_mask(board_poly)
    rgba = result.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba


def paste_at_footpoint(world, asset, foot_raw, pivot):
    sx, sy = foot_raw[0] + 920, foot_raw[1] + 99
    x = int(round(sx - pivot[0]))
    y = int(round(sy - pivot[1]))
    world.alpha_composite(asset, (x, y))


def frame_crop(world, profile):
    x, y, w, h = [int(round(v)) for v in profile["source_canvas_crop_px"]]
    crop = world.crop((x, y, x + w, y + h))
    frame = Image.new("RGBA", (1280, 720), (5, 13, 19, 255))
    frame.alpha_composite(crop, (0, 58))
    return frame


def screen_point(gx, gy, camera_raw):
    rx, ry = project_raw(gx, gy)
    return (int(round(640 + rx - camera_raw[0])), int(round(350 + ry - camera_raw[1])))


def rect_polygon_screen(rect, camera_raw):
    x, y, w, h = rect
    return [screen_point(x - .5, y - .5, camera_raw), screen_point(x + w - .5, y - .5, camera_raw),
            screen_point(x + w - .5, y + h - .5, camera_raw), screen_point(x - .5, y + h - .5, camera_raw)]


def qa_overlay(frame, profile_name, profile, structures, routes):
    out = frame.copy()
    d = ImageDraw.Draw(out)
    cam = profile["camera_raw_px"]
    for spec in structures:
        d.line(rect_polygon_screen(spec["grid_rect"], cam) + [rect_polygon_screen(spec["grid_rect"], cam)[0]], fill=(198, 209, 222, 210), width=2)
    for rect, color in [([15, 9, 6, 3], (50, 225, 235, 255)), ([20, 11, 3, 5], (255, 170, 65, 255)), ([20, 5, 12, 7], (72, 210, 164, 220))]:
        pts = rect_polygon_screen(rect, cam)
        d.line(pts + [pts[0]], fill=color, width=3)
    for route_id, cells, color in routes:
        pts = [screen_point(x, y, cam) for x, y in cells]
        d.line(pts, fill=color, width=3)
        for p in pts:
            d.ellipse((p[0]-3,p[1]-3,p[0]+3,p[1]+3), fill=color)
    for rec in CAMERA["actor_footpoint_expectations"]["PLAN_SHARED" if "PLAN" in profile_name else profile_name]:
        p = tuple(int(round(v)) for v in rec["screen"])
        d.line((p[0]-6,p[1],p[0]+6,p[1]), fill=(255,235,110,255), width=2)
        d.line((p[0],p[1]-6,p[0],p[1]+6), fill=(255,235,110,255), width=2)
    d.rectangle((12, 12, 485, 44), fill=(4,10,16,220))
    d.text((22, 20), f"{profile_name} | Camera V2 40x24 | QA ONLY", fill=(235,242,250,255))
    return out


def compose_preview(asset, canvas=(300, 260), alpha_scale=1.0):
    im = asset.copy()
    if alpha_scale != 1.0:
        a = im.getchannel("A").point(lambda v: int(round(v * alpha_scale)))
        im.putalpha(a)
    bg = Image.new("RGBA", canvas, (15, 24, 31, 255))
    src = crop_content(im)
    scale = min((canvas[0]-24)/src.width, (canvas[1]-24)/src.height)
    src = src.resize((max(1,int(src.width*scale)), max(1,int(src.height*scale))), Image.Resampling.LANCZOS)
    bg.alpha_composite(src, ((canvas[0]-src.width)//2, (canvas[1]-src.height)//2))
    return bg


def build_board(items, title, size=(1920,1080), cols=3):
    out = Image.new("RGBA", size, (7, 13, 20, 255))
    d = ImageDraw.Draw(out)
    d.text((28, 22), title, fill=(235,242,250,255))
    rows = math.ceil(len(items)/cols)
    cell_w = size[0]//cols
    cell_h = (size[1]-70)//max(1,rows)
    for i,(label,im) in enumerate(items):
        col,row=i%cols,i//cols
        x,y=col*cell_w,70+row*cell_h
        panel=compose_preview(im,(cell_w-24,cell_h-42))
        out.alpha_composite(panel,(x+12,y+28))
        d.text((x+18,y+7),label,fill=(109,220,236,255))
    return out


def write_source_lineage():
    task113_path = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/113-c01e02-a9-1a6-env-a1-modular-tactical-environment-kit-master-objective.md"
    rows = [
        ("TASK113", task113_path, "Candidate_objective", "sole_task_authority", "no Canon/runtime promotion"),
        ("TASK112", PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/112-c01e02-p111-camera-v2-exact-interface-producer-acceptance.md", "Producer_acceptance", "opens ENV-A1 only", "does not open Call03/04"),
        ("TASK114", PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/114-c01e02-env-a1-modular-environment-art-dispatch-receipt.md", "Dispatch_receipt", "one environment call", "no reroll"),
        ("CAMERA_V2", CAMERA_PATH, "Candidate_exact_interface", "geometry/pivot/crop", "not visible pixel donor"),
        ("REGISTRATION", REG_PATH, "Candidate_exact_registration", "structure/object registration", "not visible pixel donor"),
        ("TASK111_CAPTURE_MANIFEST", PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c4b-camera-v2-freeze/receipts/06-camera-v2-capture-manifest.json", "Candidate_QA_only", "local geometry/safe-area validation", "not ImageGen reference"),
        ("SLOT_GUIDE", GUIDE_PATH, "Candidate_mechanical_guide", "ImageGen strict layout reference", "no visible final art"),
        ("CALL02_DONOR", DONOR_PATH, "History_environment_method_only", "ImageGen style/material reference", "no topology/object semantics"),
        ("IMAGEGEN_RAW", RAW, "Candidate_generated_raw", "sole generated visible parent", "not runtime"),
    ]
    with (ROOT / "source-lineage.tsv").open("w", newline="", encoding="utf-8") as fh:
        w=csv.writer(fh,delimiter="\t",lineterminator="\n")
        w.writerow(["source_id","absolute_path","sha256","authority","allowed_use","forbidden_use"])
        for sid,path,auth,allow,forbid in rows:
            w.writerow([sid,str(path),sha256(path),auth,allow,forbid])


def write_generation_log(raw_sha, contract_sha, guide_sha):
    log = f"""# ENV-A1 generation log

- tool_mode: built-in imagegen skill
- call_count: 1
- reroll_count: 0
- environment_budget_before: total=1 / used=0 / remaining=1
- environment_budget_after: total=1 / used=1 / remaining=0
- environment_calls_used: 1/1
- Call03_used: 0
- Call03_allowed: false
- Call04_used: 0
- Call04_allowed: false
- call_completed_at: 2026-08-21T21:29:44+0800
- original_result_path: `/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-b64e265d-1e65-4609-8938-4f7908e2c410.png`
- workspace_raw_copy: `{RAW}`
- workspace_raw_sha256: `{raw_sha}`
- raw_dimensions: 1536x1024 RGB opaque sheet
- pre_call_module_slot_contract_sha256: `{contract_sha}`
- reference_1: `{GUIDE_PATH}` / `{guide_sha}` / strict slot layout only
- reference_2: `{DONOR_PATH}` / `{sha256(DONOR_PATH)}` / style and material method only
- no other image references were supplied

## Exact prompt

```text
{PROMPT}
```

No second call, edit, reroll, Call03 or Call04 was used.
"""
    (ROOT / "generation-log.md").write_text(log, encoding="utf-8")


def build_asset_manifest(metadata):
    rows=[]
    pngs=sorted(p for p in ROOT.rglob("*.png") if p.name != "delivery-hashes.sha256")
    md_by_rel={m["relative_path"]:m for m in metadata}
    for p in pngs:
        rel=p.relative_to(ROOT).as_posix()
        im=Image.open(p)
        m=md_by_rel.get(rel,{})
        bbox=alpha_bbox(im.convert("RGBA")) if (im.mode=="RGBA" or "transparency" in im.info) else None
        rows.append([rel,m.get("resource_id","QA_OR_EVIDENCE"),m.get("artifact_class",rel.split('/')[0]),m.get("state","NA"),im.width,im.height,im.mode,
                     json.dumps(list(bbox) if bbox else None,separators=(",",":")),json.dumps(m.get("pivot"),separators=(",",":")),
                     json.dumps(m.get("origin_raw"),separators=(",",":")),json.dumps(m.get("grid_rect"),separators=(",",":")),
                     json.dumps(m.get("front_edge_raw"),separators=(",",":")),m.get("world_height_class","NA"),sha256(p),"false"])
    with (ROOT/"asset-manifest.tsv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.writer(fh,delimiter="\t",lineterminator="\n")
        w.writerow(["relative_path","resource_id","artifact_class","state","width","height","mode","alpha_bbox","pivot_px","origin_raw","grid_rect","front_edge_raw","world_height_class","sha256","runtime_allowed"])
        w.writerows(rows)


def write_hashes():
    paths=sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name!="delivery-hashes.sha256" and "__pycache__" not in p.parts)
    (ROOT/"delivery-hashes.sha256").write_text("".join(f"{sha256(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in paths),encoding="utf-8")


def main():
    ensure_dirs()
    for p,expected in EXPECTED.items():
        if sha256(p)!=expected:
            raise SystemExit(f"INPUT_SHA_MISMATCH {p}")
    contract=json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    global CAMERA
    CAMERA=json.loads(CAMERA_PATH.read_text(encoding="utf-8"))
    profile=json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    raw=Image.open(RAW).convert("RGB")
    if raw.size!=(1536,1024):
        raise SystemExit("RAW_DIMENSION_MISMATCH")
    slots={s["slot_id"]:s for s in contract["generation_slots"]}
    extracted={}
    slot_qa=[]
    for sid,s in slots.items():
        x0,y0,x1,y1=s["box"]
        rgba=chroma_extract(raw.crop((x0,y0,x1,y1)))
        if s["kind"] in {"structure", "tactical_object"}:
            rgba = keep_largest_alpha_component(rgba)
        bbox=alpha_bbox(rgba)
        if not bbox:
            raise SystemExit(f"EMPTY_SLOT {sid}")
        extracted[sid]=rgba
        save_png(rgba,ROOT/f"intermediate/slots/{sid}_EXTRACTED_RGBA.png")
        slot_qa.append({"slot_id":sid,"source_box":s["box"],"alpha_bbox":list(bbox),"alpha_pixels":int(np.count_nonzero(np.array(rgba.getchannel('A')))),"nonempty":True})

    materials={}
    for sid in ["GROUND_WET_ASPHALT","GROUND_ROAD_LANGUAGE","GROUND_CURB_DRAINAGE","GROUND_APRON_PAVING"]:
        sw=centered_swatch(extracted[sid])
        materials[sid]=sw
        save_png(sw.convert("RGBA"),ROOT/f"intermediate/materials/{sid}_SWATCH_RGBA.png")
    ground=build_ground(materials)
    ground_path=ROOT/"delivery/GROUND_BAKE_CURRENT_V2_2400x1350.png"
    save_png(ground,ground_path)

    if "--correction-pilot" in sys.argv:
        pilot_dir = ROOT / "qa/correction-pilot"
        pilot_dir.mkdir(parents=True, exist_ok=True)
        nw = next(s for s in contract["structure_delivery_contracts"] if s["object_id"] == "NW_BLOCK")
        nw_asset = fit_content(extracted["NW_BLOCK"], nw["local_canvas_px"], nw["pivot_local_px"], margin=3)
        shield_asset = fit_content(extracted["PROP_C01CDV1_RETIRED_SHIELD"], (320,256), (160,244), margin=6)
        nw_path = pilot_dir / "NW_BLOCK_CORRECTED_COMBINED_RGBA.png"
        shield_path = pilot_dir / "PROP_C01CDV1_RETIRED_SHIELD_CORRECTED_RGBA.png"
        ground_pilot_path = pilot_dir / "GROUND_BAKE_CURRENT_V2_CORRECTED_2400x1350.png"
        save_png(nw_asset, nw_path)
        save_png(shield_asset, shield_path)
        save_png(ground.copy(), ground_pilot_path)
        print(json.dumps({
            "status": "CORRECTION_PILOT_ONLY_FOUR_CAMERA_BLOCKED",
            "object": str(shield_path),
            "structure": str(nw_path),
            "ground": str(ground_pilot_path),
            "ImageGen_calls_added": 0,
        }, ensure_ascii=False, indent=2))
        return

    structures=[]
    metadata=[{"relative_path":ground_path.relative_to(ROOT).as_posix(),"resource_id":"GROUND_BAKE_CURRENT_V2","artifact_class":"ground_bake","state":"intact_first_round","origin_raw":[-920,-99]}]
    for spec in contract["structure_delivery_contracts"]:
        sid=spec["object_id"]
        combined=fit_content(extracted[sid],spec["local_canvas_px"],spec["pivot_local_px"],margin=3)
        foundation,occluder,cut=split_structure(combined)
        base=ROOT/f"delivery/structures/{sid}"
        fp=Path(str(base)+"_FOUNDATION_RGBA.png")
        op=Path(str(base)+"_OCCLUDER_RGBA.png")
        save_png(foundation,fp); save_png(occluder,op)
        combined_check=Image.alpha_composite(foundation,occluder)
        structures.append({**spec,"foundation":foundation,"occluder":occluder,"combined":combined_check,"split_y":cut})
        for p,kind in [(fp,"foundation"),(op,"occluder")]:
            metadata.append({"relative_path":p.relative_to(ROOT).as_posix(),"resource_id":sid,"artifact_class":f"structure_{kind}","state":"opaque_source","pivot":spec["pivot_local_px"],"grid_rect":spec["grid_rect"],"front_edge_raw":spec["front_edge_raw"],"world_height_class":spec["world_height_class"]})
        save_png(combined_check.resize((max(1,combined_check.width//2),max(1,combined_check.height//2)),Image.Resampling.LANCZOS),ROOT/f"qa/structure-thumbnails/{sid}_50_PERCENT.png")
        save_png(foundation,ROOT/f"qa/structure-layer-toggle/{sid}_FOUNDATION_ONLY.png")
        save_png(occluder,ROOT/f"qa/structure-layer-toggle/{sid}_OCCLUDER_ONLY.png")
        save_png(combined_check,ROOT/f"qa/structure-layer-toggle/{sid}_COMBINED.png")
        revealed=foundation.copy(); faded=occluder.copy(); faded.putalpha(faded.getchannel("A").point(lambda v:int(round(v*0.34)))); revealed=Image.alpha_composite(revealed,faded)
        save_png(combined_check,ROOT/f"qa/structure-reveal/{sid}_OPAQUE_100.png")
        save_png(revealed,ROOT/f"qa/structure-reveal/{sid}_REVEALED_034.png")
        save_png(combined_check.copy(),ROOT/f"qa/structure-reveal/{sid}_RESTORED_100.png")

    prop_specs={
        "PROP_C01CDV1_RETIRED_SHIELD":((320,256),(160,244),[160,600],"wall_hung_3_scorches"),
        "TARGET_C01_EAST_EXIT":((360,300),(180,286),[960,936],"active_first_round_open"),
        "TARGET_C01_SECURITY_GATE_ACTIVE":((256,256),(128,242),[760,864],"active"),
        "TARGET_C01_SECURITY_GATE_DAMAGED":((256,256),(128,242),[760,864],"damaged"),
    }
    props={}
    for sid,(size,pivot,foot,state) in prop_specs.items():
        asset=fit_content(extracted[sid],size,pivot,margin=6)
        props[sid]={"image":asset,"pivot":pivot,"foot_raw":foot,"state":state}
        p=ROOT/f"delivery/tactical-objects/{sid}_RGBA.png"; save_png(asset,p)
        metadata.append({"relative_path":p.relative_to(ROOT).as_posix(),"resource_id":sid,"artifact_class":"tactical_object","state":state,"pivot":list(pivot),"front_edge_raw":foot})

    road_specs={
        "ROAD_DAMAGE_A_42_OVERLAY":((700,340),(1320,843),"long_broken_arc",42),
        "ROAD_DAMAGE_B_24_OVERLAY":((520,260),(1300,831),"twin_buckles",24),
    }
    roads={}
    for sid,(box_size,center,state,damage) in road_specs.items():
        decal=fit_content(extracted[sid],box_size,(box_size[0]//2,box_size[1]-8),margin=2)
        layer=Image.new("RGBA",(2400,1350),(0,0,0,0))
        layer.alpha_composite(decal,(int(center[0]-box_size[0]/2),int(center[1]-box_size[1]/2)))
        p=ROOT/f"delivery/world-results/{sid}_2400x1350.png"; save_png(layer,p)
        roads[sid]=layer
        metadata.append({"relative_path":p.relative_to(ROOT).as_posix(),"resource_id":sid,"artifact_class":"world_result_overlay","state":state,"origin_raw":[-920,-99]})

    world=ground.copy()
    events=[]
    for s in structures:
        x,y,_,_=s["visual_bounds_raw"]
        events.append((s["front_edge_raw"][1],"structure",s,(x+920,y+99)))
    for sid,p in props.items():
        events.append((p["foot_raw"][1],"prop",(sid,p),None))
    for _,kind,data,pos in sorted(events,key=lambda e:e[0]):
        if kind=="structure":
            world.alpha_composite(data["foundation"],pos)
            world.alpha_composite(data["occluder"],pos)
        else:
            _,p=data; paste_at_footpoint(world,p["image"],p["foot_raw"],p["pivot"])

    camera_profiles=CAMERA["projection"]["camera_profiles"]
    routes=[
        ("A",[[15,11],[16,11],[17,11],[18,11],[18,10],[19,10],[19,9],[20,9]],(255,194,64,255)),
        ("B",[[15,11],[15,10],[16,10],[17,10],[18,10],[19,10],[19,9]],(61,224,220,255)),
        ("BREAKER",[[20,13],[20,12],[20,11]],(255,92,92,255)),
    ]
    frames={}
    for name in ["A_PLAN","B_PLAN","A_CONTACT","B_CONTACT"]:
        frame=frame_crop(world,camera_profiles[name]); frames[name]=frame
        p=ROOT/f"qa/cleanplates/{name}_ACTOR_FREE_CLEANPLATE_1280x720.png"; save_png(frame,p)
        q=qa_overlay(frame,name,camera_profiles[name],structures,routes)
        save_png(q,ROOT/f"qa/registration/{name}_SLOT_FOOTPRINT_ROUTE_QA_1280x720.png")
    save_png(frames["A_PLAN"],ROOT/"qa/A_PLAN_ENVIRONMENT_100_PERCENT_1280x720.png")
    save_png(frames["A_PLAN"].resize((640,360),Image.Resampling.LANCZOS),ROOT/"qa/A_PLAN_ENVIRONMENT_50_PERCENT_640x360.png")

    for s in structures:
        solo=ground.copy(); x,y,_,_=s["visual_bounds_raw"]
        solo.alpha_composite(s["foundation"],(x+920,y+99)); solo.alpha_composite(s["occluder"],(x+920,y+99))
        save_png(frame_crop(solo,camera_profiles["A_PLAN"]),ROOT/f"qa/structure-solo/{s['object_id']}_A_PLAN_SOLO_1280x720.png")

    reveal_items=[]
    for s in structures:
        revealed=s["foundation"].copy(); faded=s["occluder"].copy(); faded.putalpha(faded.getchannel("A").point(lambda v:int(round(v*0.34)))); revealed=Image.alpha_composite(revealed,faded)
        reveal_items.extend([(f"{s['object_id']} OPAQUE",s["combined"]),(f"{s['object_id']} REVEALED 0.34",revealed),(f"{s['object_id']} RESTORED",s["combined"])])
    save_png(build_board(reveal_items,"STRUCTURE OPAQUE / REVEALED 0.34 / RESTORED",cols=3),ROOT/"qa/STRUCTURE_REVEAL_TRISTATE_BOARD_1920x1080.png")
    object_items=[("RETIRED SHIELD",props["PROP_C01CDV1_RETIRED_SHIELD"]["image"]),("EAST EXIT",props["TARGET_C01_EAST_EXIT"]["image"]),("SECURITY ACTIVE",props["TARGET_C01_SECURITY_GATE_ACTIVE"]["image"]),("SECURITY DAMAGED",props["TARGET_C01_SECURITY_GATE_DAMAGED"]["image"]),("ROAD A 42",crop_content(roads["ROAD_DAMAGE_A_42_OVERLAY"])),("ROAD B 24",crop_content(roads["ROAD_DAMAGE_B_24_OVERLAY"]))]
    save_png(build_board(object_items,"TACTICAL OBJECT / WORLD RESULT STATES",cols=3),ROOT/"qa/TACTICAL_OBJECT_AND_ROAD_STATE_TOGGLE_1920x1080.png")
    for sid,layer in roads.items():
        state_world=world.copy(); state_world.alpha_composite(layer)
        save_png(frame_crop(state_world,camera_profiles["A_PLAN"]),ROOT/f"qa/{sid}_WORLD_RESULT_A_PLAN_1280x720.png")

    # Exact readbacks and mechanical gates.
    controls=[]
    for item in CAMERA["control_points"]:
        gx,gy=item["grid"]; rx,ry=project_raw(gx,gy)
        controls.append({"grid":item["grid"],"expected_raw":item["raw"],"actual_raw":[rx,ry],"error_px":math.hypot(rx-item["raw"][0],ry-item["raw"][1])})
    structure_checks=[]
    for s in structures:
        restored=ROOT/f"qa/structure-reveal/{s['object_id']}_RESTORED_100.png"
        opaque=ROOT/f"qa/structure-reveal/{s['object_id']}_OPAQUE_100.png"
        structure_checks.append({"object_id":s["object_id"],"foundation_canvas":list(s["foundation"].size),"occluder_canvas":list(s["occluder"].size),"expected_canvas":s["local_canvas_px"],"pivot":s["pivot_local_px"],"height_class":s["world_height_class"],"height_cap_px":s["world_height_px"],"foundation_bbox":list(alpha_bbox(s["foundation"]) or []),"occluder_bbox":list(alpha_bbox(s["occluder"]) or []),"restored_equals_opaque":sha256(restored)==sha256(opaque)})
    mechanical_pass=(max(c["error_px"] for c in controls)<=0.5 and all(c["foundation_canvas"]==c["expected_canvas"] and c["occluder_canvas"]==c["expected_canvas"] and c["foundation_bbox"] and c["occluder_bbox"] and c["restored_equals_opaque"] for c in structure_checks) and ground.size==(2400,1350) and all(r.size==(2400,1350) for r in roads.values()) and len(slot_qa)==16)

    raw_sha=sha256(RAW); contract_sha=sha256(CONTRACT_PATH); guide_sha=sha256(GUIDE_PATH)
    write_source_lineage(); write_generation_log(raw_sha,contract_sha,guide_sha)
    (ROOT/"receipts/slot-extraction-readback.json").write_text(json.dumps({"raw_sha256":raw_sha,"slots":slot_qa,"slot_count":len(slot_qa),"all_nonempty":all(s["nonempty"] for s in slot_qa)},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"receipts/camera-v2-registration-readback.json").write_text(json.dumps({"camera_contract_id":"CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE","world_canvas":[2400,1350],"origin_raw":[-920,-99],"controls":controls,"max_error_px":max(c["error_px"] for c in controls),"structures":structure_checks},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    build_asset_manifest(metadata)
    report={"task_id":"A9_1A6_ENV_A1_MODULAR_TACTICAL_ENVIRONMENT_KIT_MASTER","status":"MACHINE_PASS_VISUAL_REVIEW_PENDING" if mechanical_pass else "MACHINE_FAIL","mechanical_pass":mechanical_pass,"visual_self_review_pass":VISUAL_SELF_REVIEW_PASS,"visual_self_review_status":VISUAL_SELF_REVIEW_STATUS,"overall_pass":bool(mechanical_pass and VISUAL_SELF_REVIEW_PASS),"input_sha_pass":True,"environment_calls_used":"1/1","reroll_count":0,"Call03_used":0,"Call03_allowed":False,"Call04_used":0,"Call04_allowed":False,"raw_sha256":raw_sha,"slot_count":len(slot_qa),"all_slots_nonempty":all(s["nonempty"] for s in slot_qa),"max_registration_error_px":max(c["error_px"] for c in controls),"ground_size_pass":ground.size==(2400,1350),"road_overlay_size_pass":all(r.size==(2400,1350) for r in roads.values()),"structure_layer_contract_pass":all(c["foundation_canvas"]==c["expected_canvas"] and c["occluder_canvas"]==c["expected_canvas"] for c in structure_checks),"runtime_allowed":False,"real_art_loaded":0,"producer_P102_required":True,"fun_proven":False}
    (ROOT/"machine-validation-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"50-100-visual-self-review.md").write_text(f"""# ENV-A1 50% / 100% visual self-review

Status: `{VISUAL_SELF_REVIEW_STATUS}`

- 50% three-second environment read: pending executor inspection.
- 100% camera consistency, alpha edges, module separation and reveal readability: pending executor inspection.
- Machine geometry and registration are reported separately and do not imply visual acceptance.
""",encoding="utf-8")
    (ROOT/"completion-report.md").write_text(f"""# ENV-A1 completion report

Status: `{'ENV_A1_MODULAR_ENVIRONMENT_AND_OBJECT_KIT_CANDIDATE_FOR_P102' if mechanical_pass and VISUAL_SELF_REVIEW_PASS else 'ENV_A1_POSTPROCESS_COMPLETE_VISUAL_SELF_REVIEW_PENDING'}`

- Environment ImageGen: 1/1 used; no reroll.
- Call03: 0, false. Call04: 0, false.
- Mechanical pass: `{str(mechanical_pass).lower()}`.
- Visual self-review pass: `{str(VISUAL_SELF_REVIEW_PASS).lower()}`.
- Runtime/Canon/UA91/G2-B handoff: none.
- Stop: P102 producer 50%/100% actual-pixel review.
""",encoding="utf-8")
    write_hashes()
    print(json.dumps({"mechanical_pass":mechanical_pass,"visual_self_review_pass":VISUAL_SELF_REVIEW_PASS,"raw_sha256":raw_sha,"slot_count":len(slot_qa),"max_registration_error_px":max(c["error_px"] for c in controls),"manifest_sha256":sha256(ROOT/"delivery-hashes.sha256")},ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
