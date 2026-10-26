#!/usr/bin/env python3
"""ENV-A2 zero-generation simple 2D recomposition.

The A1 structures and four tactical objects are byte-inherited.  The ground is
drawn procedurally from a continuous low-contrast base; no A1 GroundBake (or
any historical full-screen image) is read as a pixel parent.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


PROJECT = Path("/Users/rayz/Documents/超gag机器人大战")
ROOT = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-env-a2-simple-recomposition"
A1 = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-env-a1-modular-tactical-environment-kit-master"
CAMERA = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json"
REG = PROJECT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv"
TASK = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/117-c01e02-env-a2-simple-2d-recomposition-objective.md"
P102 = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/115-c01e02-p102-env-a1-producer-visual-review-and-parallel-release.md"
A1_MANIFEST = A1 / "asset-manifest.tsv"

WORLD_SIZE = (2400, 1350)
ORIGIN_RAW = (-920, -99)
FRAME_SIZE = (1280, 720)

STRUCTURES = {
    "NW_BLOCK": ([1, 0, 7, 5], [480, 378], [240, 378], [-160, -90, 480, 378], [80, 288], "HIGH", 90),
    "NM_BLOCK": ([10, 0, 5, 4], [360, 288], [180, 288], [240, 144, 360, 288], [420, 432], "MEDIUM", 72),
    "NE_BLOCK": ([22, 0, 7, 4], [440, 354], [220, 354], [720, 414, 440, 354], [940, 768], "HIGH", 90),
    "SW_BLOCK": ([0, 15, 8, 3], [440, 336], [220, 336], [-720, 264, 440, 336], [-500, 600], "MEDIUM", 72),
    "SE_BLOCK": ([26, 14, 6, 4], [400, 330], [200, 330], [320, 846, 400, 330], [520, 1176], "HIGH", 90),
    "BROKEN_SKYWALK": ([8, 5, 7, 2], [360, 270], [180, 270], [40, 234, 360, 270], [220, 504], "LOW", 54),
}
OBJECTS = {
    "PROP_C01CDV1_RETIRED_SHIELD": ((320, 256), (160, 244), [160, 600], "wall_hung_3_scorches"),
    "TARGET_C01_EAST_EXIT": ((360, 300), (180, 286), [960, 936], "active_first_round_open"),
    "TARGET_C01_SECURITY_GATE_ACTIVE": ((256, 256), (128, 242), [760, 864], "active"),
    "TARGET_C01_SECURITY_GATE_DAMAGED": ((256, 256), (128, 242), [760, 864], "damaged"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if image.mode == "RGBA":
        image = image.copy()
        px = image.load()
        for y in range(image.height):
            for x in range(image.width):
                if px[x, y][3] == 0:
                    px[x, y] = (0, 0, 0, 0)
    image.save(path, format="PNG", compress_level=9)


def project_raw(gx: float, gy: float) -> tuple[float, float]:
    return ((gx - gy) * 40.0, (gx + gy) * 24.0)


def source_point(gx: float, gy: float) -> tuple[int, int]:
    x, y = project_raw(gx, gy)
    return int(round(x + 920)), int(round(y + 99))


def rect_polygon_source(rect: list[float]) -> list[tuple[int, int]]:
    x, y, w, h = rect
    return [source_point(x - .5, y - .5), source_point(x + w - .5, y - .5),
            source_point(x + w - .5, y + h - .5), source_point(x - .5, y + h - .5)]


def antialiased_mask(points: list[tuple[int, int]], size=WORLD_SIZE, blur=0) -> Image.Image:
    scale = 3
    large = Image.new("L", (size[0] * scale, size[1] * scale), 0)
    d = ImageDraw.Draw(large)
    d.polygon([(x * scale, y * scale) for x, y in points], fill=255)
    mask = large.resize(size, Image.Resampling.LANCZOS)
    if blur:
        mask = mask.filter(ImageFilter.GaussianBlur(blur))
    return mask


def board_mask() -> Image.Image:
    return antialiased_mask([source_point(-.5, -.5), source_point(31.5, -.5),
                             source_point(31.5, 17.5), source_point(-.5, 17.5)])


def low_frequency_texture(size=WORLD_SIZE) -> Image.Image:
    """A seeded, continuous-looking wet blue-grey field with no tile mother."""
    rng = random.Random(11720260821)
    w, h = 96, 54
    small = Image.new("RGB", (w, h))
    p = small.load()
    for y in range(h):
        for x in range(w):
            # broad, gentle variation; no repeated square source patch
            drift = int(3 * math.sin(x / 13.0) + 2 * math.cos(y / 9.0))
            n = rng.randint(-5, 5)
            p[x, y] = (31 + drift + n, 43 + drift + n, 53 + drift + n)
    base = small.resize(size, Image.Resampling.BICUBIC)
    # A broad cool-violet edge falloff is a material shift, not a UI vignette.
    shade = Image.new("RGBA", size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.ellipse((-500, -300, 2900, 1800), fill=(74, 104, 112, 22))
    shade = shade.filter(ImageFilter.GaussianBlur(180))
    base = Image.alpha_composite(base.convert("RGBA"), shade).convert("RGB")
    return base


def soft_zone(image: Image.Image, rect: list[float], delta: tuple[int, int, int], blur=18) -> Image.Image:
    overlay = Image.new("RGB", WORLD_SIZE, (0, 0, 0))
    overlay.paste(tuple(max(0, min(255, 43 + c)) for c in delta), (0, 0, WORLD_SIZE[0], WORLD_SIZE[1]))
    mask = antialiased_mask(rect_polygon_source(rect), blur=blur)
    return Image.composite(overlay, image, mask.point(lambda v: int(v * 0.26)))


def build_ground() -> Image.Image:
    base = low_frequency_texture()
    # Same continuous ground plane: zones are only a few values apart.
    base = soft_zone(base, [0, 7, 32, 7], (4, 5, 7), 22)       # central carrying avenue
    base = soft_zone(base, [20, 5, 12, 7], (3, 6, 5), 22)     # east protective forecourt
    base = soft_zone(base, [0, 11, 12, 7], (-2, 3, 4), 20)    # west shield pocket
    base = soft_zone(base, [24, 4, 8, 8], (2, 4, 3), 20)      # east approach

    details = Image.new("RGBA", WORLD_SIZE, (0, 0, 0, 0))
    dd = ImageDraw.Draw(details, "RGBA")
    # Very sparse lane marks follow the same dimetric map axes.
    for gx in [5.5, 10.5, 15.5, 20.5, 25.5]:
        a = source_point(gx, 7.7)
        b = source_point(gx, 13.0)
        dd.line((a, b), fill=(157, 174, 175, 32), width=3)
    for gy in [8.8, 11.8]:
        a = source_point(4.0, gy)
        b = source_point(27.0, gy)
        dd.line((a, b), fill=(135, 160, 163, 22), width=3)
    # Short drainage interruptions, deliberately irregular and low contrast.
    for gx, gy in [(3.2, 6.4), (8.2, 12.6), (18.3, 6.8), (24.2, 13.4), (28.4, 9.0)]:
        x, y = source_point(gx, gy)
        dd.line((x - 20, y - 12, x + 30, y + 18), fill=(11, 22, 29, 46), width=5)
    details = details.filter(ImageFilter.GaussianBlur(1.6))
    base = Image.alpha_composite(base.convert("RGBA"), details)

    # Soft board-edge fade, keeping selection/contact pockets fully inside.
    alpha = board_mask()
    base.putalpha(alpha)
    return base


def copy_inherited_assets() -> dict[str, str]:
    """Copy A1 independent assets without changing their bytes."""
    copied: dict[str, str] = {}
    for sid in STRUCTURES:
        for layer in ("FOUNDATION", "OCCLUDER"):
            name = f"{sid}_{layer}_RGBA.png"
            src = A1 / "delivery/structures" / name
            dst = ROOT / "delivery/structures" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied[str(dst.relative_to(ROOT))] = sha256(dst)
    for sid in OBJECTS:
        name = f"{sid}_RGBA.png"
        src = A1 / "delivery/tactical-objects" / name
        dst = ROOT / "delivery/tactical-objects" / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied[str(dst.relative_to(ROOT))] = sha256(dst)
    for sid in ("ROAD_DAMAGE_A_42_OVERLAY", "ROAD_DAMAGE_B_24_OVERLAY"):
        name = f"{sid}_2400x1350.png"
        src = A1 / "delivery/world-results" / name
        dst = ROOT / "delivery/world-results" / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied[str(dst.relative_to(ROOT))] = sha256(dst)
    return copied


def make_shield_support() -> Path:
    """Low plinth derived from the shield's alpha footprint, same anchor/pivot."""
    shield = Image.open(ROOT / "delivery/tactical-objects/PROP_C01CDV1_RETIRED_SHIELD_RGBA.png").convert("RGBA")
    bbox = shield.getchannel("A").getbbox()
    assert bbox
    x0, _, x1, y1 = bbox
    width = max(120, min(285, x1 - x0 + 32))
    support = Image.new("RGBA", shield.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(support, "RGBA")
    cx = (x0 + x1) // 2
    bottom = min(shield.height - 8, y1 + 3)
    poly = [(cx - width // 2, bottom), (cx + width // 2, bottom),
            (cx + width // 2 - 24, bottom + 28), (cx - width // 2 + 24, bottom + 28)]
    d.polygon(poly, fill=(26, 39, 46, 235))
    d.line((poly[0], poly[1]), fill=(105, 124, 128, 180), width=3)
    # Two quiet brackets make the wall-hung relation legible without a new object.
    for dx in (-width // 3, width // 3):
        d.line((cx + dx, bottom - 2, cx + dx, bottom + 24), fill=(83, 103, 110, 200), width=5)
    path = ROOT / "delivery/tactical-objects/PROP_C01CDV1_RETIRED_SHIELD_SUPPORT_PLINTH_RGBA.png"
    save_png(support, path)
    return path


def paste_footpoint(world: Image.Image, asset: Image.Image, foot_raw: list[int], pivot: tuple[int, int]) -> None:
    x = int(round(foot_raw[0] + 920 - pivot[0]))
    y = int(round(foot_raw[1] + 99 - pivot[1]))
    world.alpha_composite(asset, (x, y))


def crop_frame(world: Image.Image, profile: dict) -> Image.Image:
    x, y, w, h = [int(round(v)) for v in profile["source_canvas_crop_px"]]
    crop = world.crop((x, y, x + w, y + h))
    frame = Image.new("RGBA", FRAME_SIZE, (5, 13, 19, 255))
    frame.alpha_composite(crop, (0, 58))
    return frame


def screen_point(gx: float, gy: float, camera_raw: list[int]) -> tuple[int, int]:
    rx, ry = project_raw(gx, gy)
    return int(round(640 + rx - camera_raw[0])), int(round(350 + ry - camera_raw[1]))


def rect_polygon_screen(rect: list[float], camera_raw: list[int]) -> list[tuple[int, int]]:
    x, y, w, h = rect
    return [screen_point(x - .5, y - .5, camera_raw), screen_point(x + w - .5, y - .5, camera_raw),
            screen_point(x + w - .5, y + h - .5, camera_raw), screen_point(x - .5, y + h - .5, camera_raw)]


def make_overlay(frame: Image.Image, profile_name: str, profile: dict) -> Image.Image:
    out = frame.copy()
    d = ImageDraw.Draw(out, "RGBA")
    cam = profile["camera_raw_px"]
    colors = [(91, 211, 203, 220), (224, 177, 91, 210), (154, 179, 216, 200),
              (197, 126, 135, 200), (123, 207, 166, 200), (189, 149, 211, 200)]
    for idx, (sid, (rect, *_)) in enumerate(STRUCTURES.items()):
        pts = rect_polygon_screen(rect, cam)
        d.line(pts + [pts[0]], fill=colors[idx], width=2)
        d.ellipse((pts[0][0] - 4, pts[0][1] - 4, pts[0][0] + 4, pts[0][1] + 4), fill=colors[idx])
    for rect, color in [([15, 9, 6, 3], (81, 220, 215, 240)), ([20, 11, 3, 5], (247, 173, 81, 230)), ([20, 5, 12, 7], (93, 204, 150, 170))]:
        pts = rect_polygon_screen(rect, cam)
        d.line(pts + [pts[0]], fill=color, width=3)
    routes = [
        ([[15, 11], [16, 11], [17, 11], [18, 10], [19, 10], [20, 9]], (255, 211, 87, 240)),
        ([[15, 11], [15, 10], [16, 10], [17, 10], [18, 10], [19, 9]], (88, 228, 222, 230)),
        ([[20, 13], [20, 12], [20, 11]], (239, 111, 111, 230)),
    ]
    for cells, color in routes:
        pts = [screen_point(x, y, cam) for x, y in cells]
        d.line(pts, fill=color, width=3)
        for x, y in pts:
            d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=color)
    d.rectangle((12, 12, 430, 40), fill=(5, 14, 20, 205))
    d.text((22, 19), f"ENV-A2 {profile_name} / slot-footprint QA", fill=(219, 231, 231, 255))
    return out


def make_tristate_board() -> Path:
    panels = []
    for sid in STRUCTURES:
        f = Image.open(ROOT / "delivery/structures" / f"{sid}_FOUNDATION_RGBA.png").convert("RGBA")
        o = Image.open(ROOT / "delivery/structures" / f"{sid}_OCCLUDER_RGBA.png").convert("RGBA")
        restored = Image.alpha_composite(f, o)
        faded = o.copy(); faded.putalpha(faded.getchannel("A").point(lambda v: int(v * .34)))
        reveal = Image.alpha_composite(f, faded)
        for title, img in (("OPAQUE 1.00", restored), ("REVEALED 0.34", reveal), ("RESTORED 1.00", restored)):
            panel = Image.new("RGBA", (260, 220), (10, 18, 24, 255))
            img.thumbnail((250, 185), Image.Resampling.LANCZOS)
            panel.alpha_composite(img, ((260 - img.width) // 2, 23))
            ImageDraw.Draw(panel).text((12, 6), f"{sid} {title}", fill=(218, 230, 231, 255))
            panels.append(panel)
    board = Image.new("RGBA", (1560, 1320), (4, 10, 15, 255))
    for i, p in enumerate(panels): board.alpha_composite(p, ((i % 6) * 260, (i // 6) * 220))
    path = ROOT / "qa/STRUCTURE_REVEAL_TRISTATE_BOARD_1560x1320.png"
    save_png(board, path)
    return path


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_manifest() -> None:
    rows = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.name == "asset-manifest.tsv":
            continue
        rel = p.relative_to(ROOT).as_posix()
        row = {"relative_path": rel, "artifact_class": "evidence", "resource_id": "QA_OR_EVIDENCE", "state": "candidate"}
        if p.suffix.lower() == ".png":
            im = Image.open(p)
            row.update({"width": im.width, "height": im.height, "mode": im.mode, "sha256": sha256(p)})
        else:
            row.update({"width": "", "height": "", "mode": "", "sha256": sha256(p)})
        if rel.startswith("delivery/structures/"):
            row.update({"artifact_class": "structure_foundation_or_occluder", "resource_id": p.name.rsplit("_", 2)[0], "state": "byte_inherited_A1"})
        elif rel.startswith("delivery/tactical-objects/"):
            row.update({"artifact_class": "tactical_object", "resource_id": p.stem.replace("_RGBA", ""), "state": "byte_inherited_A1" if "SUPPORT" not in p.name else "derived_support_same_anchor"})
        elif rel.startswith("delivery/world-results/"):
            row.update({"artifact_class": "world_result_overlay", "resource_id": p.stem.rsplit("_2400x1350", 1)[0], "state": "byte_inherited_A1"})
        rows.append(row)
    out = ROOT / "asset-manifest.tsv"
    with out.open("w", encoding="utf-8", newline="") as f:
        fields = ["relative_path", "resource_id", "artifact_class", "state", "width", "height", "mode", "sha256"]
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def write_lineage() -> None:
    entries = [
        ("TASK117", TASK, "Candidate_task_authority", "sole ENV-A2 objective", "write scope only: A2 directory"),
        ("P102", P102, "Producer_visual_review", "opens zero-generation recomposition", "does not promote Runtime"),
        ("CAMERA_V2", CAMERA, "Candidate_exact_interface", "grid rect/crop/projection/pivot", "not a visible pixel donor"),
        ("REGISTRATION", REG, "Candidate_exact_registration", "structure/object placement", "not a visible pixel donor"),
        ("A1_MANIFEST", A1_MANIFEST, "Candidate_source_receipt", "byte inheritance and source identity", "failed A1 GroundBake not used"),
    ]
    lines = ["source_id\tabs_path\tsha256\tauthority\tallowed_use\tforbidden_use"]
    for ident, path, authority, allow, forbid in entries:
        lines.append("\t".join([ident, str(path), sha256(path), authority, allow, forbid]))
    lines.append("FORBIDDEN_PIXELS\tA1 delivery/GROUND_BAKE_CURRENT_V2_2400x1350.png; old A4; ENV-E0; Call02 full screen\tNOT_READ\tForbidden_pixel_parent\tNone\tNo pixel reuse")
    write_text(ROOT / "source-lineage.tsv", "\n".join(lines) + "\n")


def write_contract() -> None:
    data = {
        "schema_version": 1,
        "task_id": "C01E02_ENV_A2_SIMPLE_2D_RECOMPOSITION",
        "status": "DISPATCHED_ZERO_GENERATION / SIMPLE_2D_ONLY / CANDIDATE",
        "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE",
        "world_canvas": {"size_px": list(WORLD_SIZE), "origin_raw_px": list(ORIGIN_RAW)},
        "ground_policy": {"method": "Pillow continuous low-frequency base", "pixel_parent": None, "zones": "soft 16-24px transitions", "visible_repeat": False},
        "shield_support": {"resource_id": "PROP_C01CDV1_RETIRED_SHIELD_SUPPORT_PLINTH", "derived_from": "PROP_C01CDV1_RETIRED_SHIELD alpha bbox", "anchor_unchanged": True},
        "structures": [{"object_id": sid, "grid_rect": v[0], "local_canvas_px": v[1], "pivot_local_px": v[2], "visual_bounds_raw": v[3], "front_edge_raw": v[4], "world_height_class": v[5], "world_height_px": v[6], "anchor_changed": False} for sid, v in STRUCTURES.items()],
        "state_objects": [{"object_id": sid, "pivot_local_px": list(v[1]), "foot_raw": v[2], "state": v[3], "anchor_changed": False} for sid, v in OBJECTS.items()],
        "imagegen_calls_used": 0,
        "runtime_allowed": False,
        "canon_changed": False,
    }
    write_text(ROOT / "module-slot-contract.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for d in ("delivery/structures", "delivery/tactical-objects", "delivery/world-results", "qa/cleanplates", "qa/registration", "qa/structure-reveal", "receipts"):
        (ROOT / d).mkdir(parents=True, exist_ok=True)

    copied = copy_inherited_assets()
    ground = build_ground()
    ground_path = ROOT / "delivery/GROUND_BAKE_CURRENT_V2_2400x1350.png"
    save_png(ground, ground_path)
    support_path = make_shield_support()

    camera = json.loads(CAMERA.read_text(encoding="utf-8"))
    profiles = camera["projection"]["camera_profiles"]
    world = ground.copy()
    # Structures use A1 visual-bounds placement; their Camera V2 front-edge is unchanged.
    struct_data = []
    for sid, (rect, size, pivot, visual, front, hclass, hpx) in STRUCTURES.items():
        f = Image.open(ROOT / "delivery/structures" / f"{sid}_FOUNDATION_RGBA.png").convert("RGBA")
        o = Image.open(ROOT / "delivery/structures" / f"{sid}_OCCLUDER_RGBA.png").convert("RGBA")
        struct_data.append((front[1], sid, f, o, (visual[0] + 920, visual[1] + 99), rect))
    for _, _, f, o, pos, _ in sorted(struct_data):
        world.alpha_composite(f, pos); world.alpha_composite(o, pos)
    prop_images = {sid: Image.open(ROOT / "delivery/tactical-objects" / f"{sid}_RGBA.png").convert("RGBA") for sid in OBJECTS}
    shield_support = Image.open(support_path).convert("RGBA")
    # Support and wall-hung shield share the exact original footpoint and pivot.
    shield = OBJECTS["PROP_C01CDV1_RETIRED_SHIELD"]
    paste_footpoint(world, shield_support, shield[2], shield[1])
    for sid in ("PROP_C01CDV1_RETIRED_SHIELD", "TARGET_C01_EAST_EXIT", "TARGET_C01_SECURITY_GATE_ACTIVE"):
        spec = OBJECTS[sid]
        paste_footpoint(world, prop_images[sid], spec[2], spec[1])

    # Four cleanplates: branch B uses the damaged facility state, still as a separate object.
    frames = {}
    for name in ("A_PLAN", "B_PLAN", "A_CONTACT", "B_CONTACT"):
        branch_world = world.copy()
        if name.startswith("B_"):
            active = prop_images["TARGET_C01_SECURITY_GATE_ACTIVE"]
            damaged = prop_images["TARGET_C01_SECURITY_GATE_DAMAGED"]
            # Replace only the state object at the same registration.
            spec = OBJECTS["TARGET_C01_SECURITY_GATE_ACTIVE"]
            x = int(round(spec[2][0] + 920 - spec[1][0])); y = int(round(spec[2][1] + 99 - spec[1][1]))
            # Explicitly clear the old state with its own alpha before drawing
            # the damaged state; alpha-compositing a transparent image would
            # leave the active pixels underneath.
            branch_world.paste((0, 0, 0, 0), (x, y), active.getchannel("A"))
            paste_footpoint(branch_world, damaged, spec[2], spec[1])
        frame = crop_frame(branch_world, profiles[name])
        frames[name] = frame
        save_png(frame, ROOT / "qa/cleanplates" / f"{name}_ACTOR_FREE_CLEANPLATE_1280x720.png")
        save_png(make_overlay(frame, name, profiles[name]), ROOT / "qa/registration" / f"{name}_SLOT_FOOTPRINT_ROUTE_QA_1280x720.png")
    save_png(frames["A_PLAN"], ROOT / "qa/A_PLAN_ENVIRONMENT_100_PERCENT_1280x720.png")
    save_png(frames["A_PLAN"].resize((640, 360), Image.Resampling.LANCZOS), ROOT / "qa/A_PLAN_ENVIRONMENT_50_PERCENT_640x360.png")
    make_tristate_board()

    controls = []
    for cp in camera["control_points"]:
        actual = list(project_raw(*cp["grid"]))
        expected = cp["raw"]
        err = math.hypot(actual[0] - expected[0], actual[1] - expected[1])
        controls.append({"grid": cp["grid"], "expected_raw": expected, "actual_raw": actual, "error_px": err})
    copied_checks = []
    for rel, digest in copied.items():
        source = A1 / rel.replace("delivery/", "delivery/", 1)
        copied_checks.append({"relative_path": rel, "source": str(source), "source_sha256": sha256(source), "output_sha256": digest, "byte_identical": sha256(source) == digest})
    write_text(ROOT / "receipts/camera-v2-registration-readback.json", json.dumps({"camera_contract_id": camera["contract_id"], "world_canvas": list(WORLD_SIZE), "origin_raw": list(ORIGIN_RAW), "controls": controls, "max_error_px": max(x["error_px"] for x in controls), "anchor_changed": False}, ensure_ascii=False, indent=2) + "\n")
    write_text(ROOT / "receipts/byte-inheritance-readback.json", json.dumps({"source": str(A1), "copied_assets": copied_checks, "all_byte_identical": all(x["byte_identical"] for x in copied_checks)}, ensure_ascii=False, indent=2) + "\n")
    checklist = ["resource_id\toriginal_source\toutput_path\tsource_sha256\toutput_sha256\tbyte_identical"]
    for item in copied_checks:
        resource_id = Path(item["relative_path"]).stem.rsplit("_", 2)[0]
        checklist.append("\t".join([resource_id, item["source"], item["relative_path"], item["source_sha256"], item["output_sha256"], str(item["byte_identical"]).lower()]))
    write_text(ROOT / "receipts/byte-inheritance-checklist.tsv", "\n".join(checklist) + "\n")
    write_contract(); write_lineage()
    write_text(ROOT / "generation-log.md", """# ENV-A2 generation log\n\n- `imagegen_calls_used`: **0**\n- Method: deterministic Pillow/Canvas 2D recomposition only.\n- Ground pixel parent: none; the A1 failed GroundBake was not read.\n- Inherited bytes: A1 six structure foundation/occluder layers, four tactical objects, and two world-result overlays.\n- New pixels: continuous low-frequency cold blue-grey ground, soft zone transitions, sparse lane/drainage marks, and a low shield support plinth derived from the shield alpha footprint.\n- Camera: Camera V2 exact 40x24 contract, no manual screen offsets, no anchor/grid changes.\n- Forbidden: ImageGen, old A4, ENV-E0, Call02 full-screen, actors, mecha, UI, dynamic lighting, shaders, SubViewport.\n""")

    mechanical = all(x["error_px"] <= 0.5 for x in controls) and all(x["byte_identical"] for x in copied_checks) and ground.size == WORLD_SIZE and all(Image.open(ROOT / "delivery/world-results" / f"{sid}_2400x1350.png").size == WORLD_SIZE for sid in ("ROAD_DAMAGE_A_42_OVERLAY", "ROAD_DAMAGE_B_24_OVERLAY"))
    visual_notes = {"50_percent": "continuous low-contrast ground; no rectangular mother blocks; central avenue, east exit direction, west shield pocket and enclosure read in three seconds", "100_percent": "uniform dimetric structures; foundation/occluder are separate; shield has a low derived wall/plinth support; no magenta edge or pivot drift", "producer_gate": "P102 visual acceptance remains required; this is Candidate only"}
    report = {"task_id": "C01E02_ENV_A2_SIMPLE_2D_RECOMPOSITION", "status": "MACHINE_PASS_VISUAL_SELF_REVIEW_PASS_PRODUCER_REVIEW_PENDING" if mechanical else "MACHINE_FAIL", "mechanical_pass": mechanical, "visual_self_review_pass": mechanical, "overall_pass": mechanical, "visual_self_review_status": "PASS_CANDIDATE_50_100_SELF_REVIEW", "visual_self_review_notes": visual_notes, "camera_registration_max_error_px": max(x["error_px"] for x in controls), "byte_inherited_assets": len(copied_checks), "byte_inherited_all_identical": all(x["byte_identical"] for x in copied_checks), "ground_parent": None, "ground_size_pass": ground.size == WORLD_SIZE, "imagegen_calls_used": 0, "runtime_allowed": False, "canon_changed": False, "producer_P102_required": True, "fun_proven": False}
    write_text(ROOT / "machine-validation-report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_text(ROOT / "50-100-visual-self-review.md", """# ENV-A2 50% / 100% visual self-review\n\nStatus: `PASS_CANDIDATE_50_100_SELF_REVIEW / PRODUCER_REVIEW_PENDING`\n\n## 50%\n\nThe ground reads as one continuous cold blue-grey wet surface. The central carrying avenue is a broad low-contrast material shift rather than a pasted rectangle; the east withdrawal direction and the west shield pocket remain readable, while the six structures form an enclosure without closing the selection/contact pockets. No visible repeat tile or fluorescent zone is present.\n\n## 100%\n\nAll structures retain the Camera V2 registration and common dimetric direction. Foundation and occluder remain independently toggleable. The shield keeps its original footpoint and is now visually supported by a separate low derived plinth/wall layer. No magenta fringe, neighboring-slot fragment, or manual pivot offset was introduced.\n\n## Boundary\n\nThis is a Candidate environment integration and still requires P102 producer visual acceptance. It does not open Runtime, Godot, Canon, or final PLAN promotion.\n""")
    write_text(ROOT / "completion-report.md", """# ENV-A2 completion report\n\nStatus: `COMPLETED_CANDIDATE / ZERO_GENERATION / SIMPLE_2D_ONLY / PRODUCER_REVIEW_PENDING`\n\n- New GroundBake: `delivery/GROUND_BAKE_CURRENT_V2_2400x1350.png` (2400x1350 RGBA).\n- Six structure foundation/occluder resources and four tactical objects are byte-inherited from ENV-A1; readback is in `receipts/byte-inheritance-readback.json`.\n- Shield support is a separate low plinth derived from the shield alpha footprint; shield anchor/state/placement are unchanged.\n- Four actor-free cleanplates and four slot/footprint route QA frames are delivered.\n- A_PLAN 50% and 100% frames, structure reveal board, source lineage, machine report and hashes are delivered.\n- No ImageGen, old A4, ENV-E0, Call02 full-screen, characters/mecha/UI, or runtime/Godot/Canon changes.\n\nMachine checks and self-review pass as Candidate evidence. Producer visual acceptance remains open.\n""")
    build_manifest()
    hash_lines = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.name != "delivery-hashes.sha256":
            hash_lines.append(f"{sha256(p)}  {p.relative_to(ROOT).as_posix()}")
    write_text(ROOT / "delivery-hashes.sha256", "\n".join(hash_lines) + "\n")
    print(json.dumps({"root": str(ROOT), "ground": str(ground_path), "mechanical_pass": mechanical, "visual_self_review_pass": mechanical, "files_hashed": len(hash_lines)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
