#!/usr/bin/env python3
"""Deterministic guides, UI, review boards, and QA for A9.1-A6-S.

This helper never draws production-visible mecha or buildings.  Its drawing
operations are limited to debug geometry, tactical overlays, UI, labels, and
review-board layout around ImageGen whole-scene cleanplates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[6]
PROD = REPO / "docs/superpowers/specs/production/c01-current-demo-v1"

VIEWPORT = (0, 58, 1280, 584)
CROP = (480, 428, 1280, 584)
RAW_ORIGIN = (-880.0, -170.0)
CANVAS_ORIGIN = (-1680.0, -350.0)
TILE_HALF = (40.0, 20.0)

SOURCES = {
    "base": PROD / "art-a4-map-b-six-layer/A4_MAP_B_BASE_2400x1350.png",
    "buildings": PROD / "art-a4-map-b-six-layer/A4_MAP_B_BUILDINGS_2400x1350.png",
    "roofs": PROD / "art-a4-map-b-six-layer/A4_MAP_B_ROOFS_2400x1350.png",
    "foreground": PROD / "art-a4-map-b-six-layer/A4_MAP_B_FOREGROUND_2400x1350.png",
    "jicun": REPO / ".superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_jicun_stand.png",
    "guardian_q": PROD / "art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_imagegen_v2.png",
    "breaker_b": PROD / "art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png",
    "breaker_x": PROD / "art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png",
    "kinetic_cel": REPO / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png",
    "kinetic_compliance": PROD / "art-a9-1a-identity-style-scale-masters/review/KINETIC_CEL_STYLE_COMPLIANCE_2400x1350.png",
}

COLORS = {
    "guardian": (255, 199, 70, 235),
    "breaker": (255, 82, 98, 235),
    "vehicle": (232, 247, 255, 235),
    "swarm": (173, 99, 255, 235),
    "object": (76, 238, 190, 235),
    "route": (66, 225, 255, 230),
    "danger": (255, 82, 98, 210),
    "ghost": (72, 232, 255, 118),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/System/Library/Fonts/SFNS.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                return ImageFont.truetype(str(candidate), size=size, index=1 if bold else 0)
            except OSError:
                continue
    return ImageFont.load_default()


def alpha_over(base: Image.Image, overlay: Image.Image) -> Image.Image:
    return Image.alpha_composite(base.convert("RGBA"), overlay.convert("RGBA"))


def registered_a4() -> Image.Image:
    base = Image.open(SOURCES["base"]).convert("RGBA")
    for key in ("buildings", "roofs", "foreground"):
        base = alpha_over(base, Image.open(SOURCES[key]))
    x, y, w, h = CROP
    crop = base.crop((x, y, x + w, y + h))
    screen = Image.new("RGBA", (1280, 720), (5, 16, 25, 255))
    screen.alpha_composite(crop, (VIEWPORT[0], VIEWPORT[1]))
    return screen


def project_grid(point: tuple[float, float]) -> tuple[float, float]:
    gx, gy = point
    raw_x = RAW_ORIGIN[0] + (gx - gy) * TILE_HALF[0]
    raw_y = RAW_ORIGIN[1] + (gx + gy) * TILE_HALF[1]
    sx = raw_x - CANVAS_ORIGIN[0] - CROP[0] + VIEWPORT[0]
    sy = raw_y - CANVAS_ORIGIN[1] - CROP[1] + VIEWPORT[1]
    return sx, sy


def cell_center(cell: tuple[float, float]) -> tuple[float, float]:
    return project_grid((cell[0] + 0.5, cell[1] + 0.5))


def footprint_polygon(anchor: tuple[float, float], footprint: tuple[int, int]) -> list[tuple[float, float]]:
    x, y = anchor
    w, h = footprint
    return [project_grid((x, y)), project_grid((x + w, y)), project_grid((x + w, y + h)), project_grid((x, y + h))]


def footprint_bottom_center(anchor: tuple[float, float], footprint: tuple[int, int]) -> tuple[float, float]:
    x, y = anchor
    w, h = footprint
    points = [cell_center((x + ix, y + iy)) for ix in range(w) for iy in range(h)]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (min(xs) + max(xs)) / 2.0, max(ys) + TILE_HALF[1]


def draw_footprint(draw: ImageDraw.ImageDraw, anchor, footprint, color, label, dashed=False):
    poly = footprint_polygon(anchor, footprint)
    fill = color[:3] + ((54 if dashed else 86),)
    draw.polygon(poly, fill=fill)
    draw.line(poly + [poly[0]], fill=color, width=4)
    foot = footprint_bottom_center(anchor, footprint)
    draw.ellipse((foot[0] - 6, foot[1] - 6, foot[0] + 6, foot[1] + 6), fill=color, outline=(4, 12, 20, 255), width=2)
    cx = sum(p[0] for p in poly) / 4
    cy = sum(p[1] for p in poly) / 4
    draw.rounded_rectangle((cx - 27, cy - 14, cx + 27, cy + 14), radius=6, fill=(5, 16, 25, 220), outline=color, width=2)
    draw.text((cx, cy), label, font=font(16, True), fill=(255, 255, 255, 255), anchor="mm")


def draw_route(draw: ImageDraw.ImageDraw, cells, color, width=5):
    points = [cell_center(tuple(c)) for c in cells]
    draw.line(points, fill=color, width=width, joint="curve")
    for p in points:
        draw.ellipse((p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5), fill=color, outline=(5, 16, 25, 255), width=2)


def build_guides() -> None:
    source_dir = OUT / "source-guides"
    source_dir.mkdir(parents=True, exist_ok=True)
    registered = registered_a4()
    registered.save(source_dir / "A4_REGISTERED_CLEAN_1280x720.png")

    # Mechanical contact sheet only: no visible design is redrawn or altered.
    mosaic = Image.new("RGB", (2400, 1800), (8, 20, 30))
    tiles = [
        ("GUARDIAN Z V10X", SOURCES["guardian_q"], (0, 0, 1200, 900)),
        ("BREAKER B BODY", SOURCES["breaker_b"], (1200, 0, 2400, 900)),
        ("BREAKER X SURFACE", SOURCES["breaker_x"], (0, 900, 1200, 1800)),
    ]
    md = ImageDraw.Draw(mosaic)
    for label, path, box in tiles:
        x0, y0, x1, y1 = box
        panel = Image.open(path).convert("RGB")
        panel = ImageOps.contain(panel, (x1 - x0 - 24, y1 - y0 - 64), Image.Resampling.LANCZOS)
        px = x0 + (x1 - x0 - panel.width) // 2
        py = y0 + 52 + (y1 - y0 - 52 - panel.height) // 2
        mosaic.paste(panel, (px, py))
        md.rectangle((x0, y0, x1 - 1, y0 + 48), fill=(5, 16, 25), outline=(92, 124, 145), width=2)
        md.text((x0 + 18, y0 + 24), label, font=font(24, True), fill=(235, 246, 255), anchor="lm")
        md.rectangle((x0, y0, x1 - 1, y1 - 1), outline=(92, 124, 145), width=2)
    # CML128 evidence is deliberately anatomy-free.  The previous whole-frame
    # style reference contained an unrelated wing/backpack silhouette and could
    # contaminate Guardian Z identity.  These are mechanical crops of empty
    # industrial environment plus the CML128 line/color/material rule table;
    # no depicted body, wing, backpack, or alternate mecha remains.
    x0, y0, x1, y1 = (1200, 900, 2400, 1800)
    md.rectangle((x0, y0, x1 - 1, y1 - 1), fill=(8, 20, 30), outline=(92, 124, 145), width=2)
    md.rectangle((x0, y0, x1 - 1, y0 + 72), fill=(5, 16, 25), outline=(92, 124, 145), width=2)
    md.text((x0 + 18, y0 + 22), "CML128 STYLE ONLY — IGNORE DEPICTED ANATOMY", font=font(22, True), fill=(235, 246, 255))
    md.text((x1 - 18, y0 + 22), "NO WINGS / NO BACKPACK", font=font(20, True), fill=(255, 183, 76), anchor="ra")

    story = Image.open(SOURCES["kinetic_cel"]).convert("RGB")
    # Verified empty-environment areas of the CML128 storyframe.
    env_crops = [
        story.crop((0, 0, 285, 175)),
        story.crop((665, 0, 940, 165)),
        story.crop((1450, 655, 1672, 941)),
    ]
    env_boxes = [
        (1212, 984, 1588, 1268),
        (1600, 984, 1988, 1268),
        (2000, 984, 2388, 1268),
    ]
    for crop, box in zip(env_crops, env_boxes):
        bx0, by0, bx1, by1 = box
        crop = ImageOps.fit(crop, (bx1 - bx0, by1 - by0), Image.Resampling.LANCZOS)
        mosaic.paste(crop, (bx0, by0))
        md.rectangle((bx0, by0, bx1 - 1, by1 - 1), outline=(92, 124, 145), width=2)

    compliance = Image.open(SOURCES["kinetic_compliance"]).convert("RGB")
    rule_crop = compliance.crop((36, 878, 2364, 1305))
    rule_crop = ImageOps.fit(rule_crop, (1176, 478), Image.Resampling.LANCZOS)
    mosaic.paste(rule_crop, (1212, 1298))
    md.rectangle((1212, 1298, 2387, 1775), outline=(92, 124, 145), width=2)
    mosaic.save(source_dir / "IDENTITY_STYLE_REFERENCE_MOSAIC_SAFE_2400x1800.png")

    plan = ImageEnhance.Brightness(registered).enhance(0.68)
    plan_overlay = Image.new("RGBA", plan.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(plan_overlay, "RGBA")
    # Central safe zone and east protection area.
    d.rectangle((256, 117, 1024, 583), outline=(255, 255, 255, 86), width=2)
    d.polygon(footprint_polygon((20, 5), (12, 7)), fill=(76, 238, 190, 28), outline=(76, 238, 190, 150))
    # Public trajectories.
    draw_route(d, [(15, 11), (16, 11), (17, 11), (18, 11), (18, 10), (19, 10), (19, 9), (20, 9)], COLORS["route"], 6)
    draw_route(d, [(17, 10), (18, 10), (21, 10), (24, 9)], COLORS["vehicle"], 4)
    draw_route(d, [(22, 7), (21, 8), (20, 9), (20, 10)], COLORS["swarm"], 4)
    draw_route(d, [(20, 13), (20, 12), (20, 11)], COLORS["danger"], 7)
    # Current actors and predictive-only endpoints.
    draw_footprint(d, (15, 11), (2, 2), COLORS["guardian"], "GZ")
    draw_footprint(d, (20, 13), (3, 3), COLORS["breaker"], "BR")
    draw_footprint(d, (17, 10), (1, 1), COLORS["vehicle"], "EV")
    draw_footprint(d, (22, 7), (1, 1), COLORS["swarm"], "S1")
    draw_footprint(d, (26, 12), (1, 1), COLORS["swarm"], "S2")
    draw_footprint(d, (29, 5), (1, 1), COLORS["swarm"], "S3")
    draw_footprint(d, (20, 9), (2, 2), COLORS["ghost"], "GHOST", True)
    draw_footprint(d, (20, 11), (3, 3), COLORS["ghost"], "INTENT", True)
    # Static objects.
    draw_footprint(d, (14, 10), (1, 1), COLORS["object"], "SH")
    draw_footprint(d, (27, 8), (1, 1), COLORS["object"], "SG")
    draw_footprint(d, (31, 7), (1, 1), COLORS["object"], "EXIT")
    focus = cell_center((19, 10))
    d.ellipse((focus[0] - 12, focus[1] - 12, focus[0] + 12, focus[1] + 12), outline=(255, 255, 255, 230), width=3)
    plan = alpha_over(plan, plan_overlay)
    plan.save(source_dir / "GF_PLAN_GEOMETRY_GUIDE_1280x720.png")

    contact = ImageEnhance.Brightness(registered).enhance(0.68)
    contact_overlay = Image.new("RGBA", contact.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(contact_overlay, "RGBA")
    d.rectangle((256, 117, 1024, 583), outline=(255, 255, 255, 86), width=2)
    d.polygon(footprint_polygon((20, 5), (12, 7)), fill=(76, 238, 190, 24), outline=(76, 238, 190, 120))
    draw_footprint(d, (20, 9), (2, 2), COLORS["guardian"], "GZ")
    draw_footprint(d, (20, 11), (3, 3), COLORS["breaker"], "BR")
    draw_footprint(d, (24, 9), (1, 1), COLORS["vehicle"], "EV")
    draw_footprint(d, (22, 9), (1, 1), COLORS["swarm"], "S1")
    draw_footprint(d, (27, 12), (1, 1), COLORS["swarm"], "S2")
    draw_footprint(d, (29, 5), (1, 1), COLORS["swarm"], "S3")
    draw_footprint(d, (14, 10), (1, 1), COLORS["object"], "SH")
    draw_footprint(d, (27, 8), (1, 1), COLORS["object"], "SG")
    draw_footprint(d, (31, 7), (1, 1), COLORS["object"], "EXIT")
    socket = project_grid((20.5, 10.5))
    d.ellipse((socket[0] - 14, socket[1] - 14, socket[0] + 14, socket[1] + 14), fill=(255, 244, 170, 190), outline=(255, 255, 255, 255), width=3)
    end = project_grid((20.5, 11.5))
    d.line((socket, end), fill=(255, 82, 98, 240), width=6)
    contact = alpha_over(contact, contact_overlay)
    contact.save(source_dir / "GF_CONTACT_GEOMETRY_GUIDE_1280x720.png")

    readback = {
        "camera_contract_id": "A4_MAP_SPRITE_CAMERA_V1",
        "viewport_px": [1280, 720],
        "map_viewport_rect": list(VIEWPORT),
        "a4_crop_rect_px": list(CROP),
        "projection_origin_raw_px": list(RAW_ORIGIN),
        "canvas_origin_raw_px": list(CANVAS_ORIGIN),
        "guide_only": True,
        "visible_mecha_drawn_by_script": False,
        "screen_points": {
            "plan_guardian_footpoint": list(footprint_bottom_center((15, 11), (2, 2))),
            "plan_breaker_footpoint": list(footprint_bottom_center((20, 13), (3, 3))),
            "contact_guardian_footpoint": list(footprint_bottom_center((20, 9), (2, 2))),
            "contact_breaker_footpoint": list(footprint_bottom_center((20, 11), (3, 3))),
            "contact_socket": list(project_grid((20.5, 10.5))),
            "contact_swarm01_footpoint": list(footprint_bottom_center((22, 9), (1, 1))),
        },
    }
    (source_dir / "guide-readback.json").write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("guides",))
    args = parser.parse_args()
    if args.mode == "guides":
        build_guides()
        for path in sorted((OUT / "source-guides").glob("*")):
            print(f"{sha256(path)}  {path.relative_to(OUT)}")


if __name__ == "__main__":
    main()
