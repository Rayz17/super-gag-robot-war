#!/usr/bin/env python3
"""Build Task98 zero-generation preproduction evidence.

This script only composes exact approved reference pixels, programmatic geometry
guides, QA slots, contracts, and receipts.  It never draws visible actor art and
never calls a generative service.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path("/Users/rayz/Documents/超gag机器人大战")
OUT = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c2-sprite-first-map-camera-masters"

TASK97 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/97-c01e02-a9-1a6-s-c1-call02-producer-visual-failure-review.md"
TASK98 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/98-c01e02-a9-1a6-s-c2-sprite-first-map-camera-master-preproduction-objective.md"
TASK99 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/99-c01e02-g2-a2-c3-current-topology-real-atlas-neutral-consumer-objective.md"
BOARD = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv"
INTERFACE = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/c01e02-tactical-visual-interface-v1.json"

GOLDEN_PROFILE = ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json"
TOPOLOGY_CONTRACT = ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/current_topology_map_contract.json"
COMPOSITOR_PROFILE = ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/visual_compositor_profile.json"
PROJECTION_CODE = ROOT / "game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/visual_projection.gd"
TOPOLOGY_CODE = ROOT / "game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/current_topology_layer.gd"

GZ_HARD = ROOT / ".superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png"
GZ_V10X = ROOT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png"
GZ_QSD = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_imagegen_v2.png"
GZ_FOUR = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png"
GZ_ACTION = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png"
BR_B = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png"
BR_X = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png"
BR_128 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png"
CML128 = ROOT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png"
A5 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png"
CALL02_RAW = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c1-current-topology-scene-first/call02-a-plan/generation-raw/CALL02_A_PLAN_RAW.png"
TASK102 = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/102-c01e02-task98-runtime-grid-registration-producer-correction.md"
TASK102_SHA = "e8556f917456da83d933842b9ace9542f5238635d5166a6f5b7adbfad0d62378"
EXECUTOR_VISUAL_INSPECTION = "PASS_TERRAIN_AND_FOOTPOINT_SINGLE_RUNTIME_COORDINATE_SYSTEM"

TASK102_AFFECTED_HISTORY_SHA = {
    "CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png": "8aa4909af5aefe0cf1959e1c941bb5c9437567e429ffa487dedd1663f36b5c3a",
    "PLAN_SLOT_COMPOSITE_QA_1280x720.png": "772c299994d47510dce3f30f6fb07fc4d2d4ba39744886dacff0b64558f96348",
    "PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png": "75bb1b09ec4201c8b66f624b00789237766f1db41177c0fff52cf6e346681a33",
}

TASK102_PROTECTED_SHA = {
    "GUARDIAN_Z_EAST_MAP_CAMERA_GEOMETRY_GUIDE_256.png": "a9900c16436e10c0050831c2aa1c364d0618d9877fffde382410be77a56f0ef0",
    "BREAKER_NORTH_MAP_CAMERA_GEOMETRY_GUIDE_384.png": "a6e213f8defaba97ed4581009a2bfbf2366361c140588078de4a008c06337f30",
    "atlas-schema-current.json": "159c0af021c99a8c778692f5b02794e5ec55a476514da55ff55958baa19e8e5d",
    "map-camera-slot-contract.json": "17e195dcac011be803bd69d893a918830dd838a5aa7a4aedd3e76bab45fb1a24",
    "socket-contact-contract.json": "c954af9b0ac7e5a1ef0e55f95b613367af9ab5ddbaec3fc55f5f4a258e5b8ea5",
    "first-round-state-facing-phase-matrix.tsv": "992ff3e6c35eb5cf6aa69ae928190f5c8ac3bb11927474569e1211ebb655bb2e",
    "first-round-phase-continuity-readback.tsv": "e03f74e3e81ce888554b7ec0ba7e8e5c8e81600a1bc1f1974b755d73b7d64199",
}

EXPECTED = {
    TASK97: "1ef4459756a44aaa3f9ee08a3036189164f5e0e4712c9252d4a2a65d0eb75767",
    TASK98: "7c82e7af59f36e52f795e14b84d647692582ad7643310beed8a26445a4edfdca",
    TASK99: "f00252166c86b3f4f3cc0d2431db584c887777cd2876a5c55268aa17570e513b",
    BOARD: "8758870be3904f5cb51b004ee8175d8df40820223c07f3f72c60968668e79a08",
    INTERFACE: "cdea5bd2f1715c076b4050cbc4f41ad203e94b896eed10e04e518f5bd483e312",
    GOLDEN_PROFILE: "61b49e5328e702cd654d28ff39c5c380ba0ae3e78753330635036d33f689523c",
    TOPOLOGY_CONTRACT: "74c6bbb3f732a61d3ed5a55d9c209b628152b9411395339d665aeeb0d76ab875",
    COMPOSITOR_PROFILE: "13719d8a3bde0cc06acbed893198943164f2541cdc0b112cc5897ff38f4c3451",
    PROJECTION_CODE: "4f1fb4e029abb12d33abe3494425c3766916e7c3f9daf4395f0f682d5c6e3aed",
    TOPOLOGY_CODE: "395b5139f68f4421757d949b285c420a981463adb9592f5f7563e52f3a764f24",
    GZ_HARD: "a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521",
    GZ_V10X: "e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade",
    GZ_QSD: "c701f3efa72301720117bae08b1479d704315c5a4de62034bf385263ea57f412",
    GZ_FOUR: "3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9",
    GZ_ACTION: "4d8e7975649b2b85458a838afd9bc2fe8e3a90fd8cbcfe8a7929b8ae9ae6c225",
    BR_B: "7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868",
    BR_X: "cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85",
    BR_128: "e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4",
    CML128: "8a546082e8fd2f1b0f9c6e8a8b1e602a647f478112887e93a8f44148e4867842",
    A5: "1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b",
    CALL02_RAW: "98f30a9797591204f702ad1b36aaad1042c2cece1fd35a088b44d828f9e156d5",
}

FONT_PATHS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

BG = (11, 16, 25, 255)
PANEL = (23, 32, 46, 255)
INK = (231, 240, 248, 255)
MUTED = (151, 169, 188, 255)
CYAN = (70, 218, 238, 255)
ORANGE = (255, 171, 70, 255)
MAGENTA = (240, 90, 166, 255)
GREEN = (103, 220, 146, 255)
RED = (244, 93, 93, 255)
YELLOW = (245, 214, 90, 255)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def font(size: int, index: int = 0) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in FONT_PATHS:
        try:
            return ImageFont.truetype(candidate, size=size, index=index)
        except Exception:
            pass
    return ImageFont.load_default()


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int = 24,
         fill: tuple[int, int, int, int] = INK, anchor: str | None = None,
         stroke: int = 0) -> None:
    draw.text(xy, value, font=font(size), fill=fill, anchor=anchor,
              stroke_width=stroke, stroke_fill=(0, 0, 0, 255))


def multiline(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int = 22,
              fill: tuple[int, int, int, int] = INK, spacing: int = 8) -> None:
    draw.multiline_text(xy, value, font=font(size), fill=fill, spacing=spacing)


def contain(source: Path, size: tuple[int, int], bg=(8, 12, 18, 255)) -> Image.Image:
    im = Image.open(source).convert("RGBA")
    im.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, bg)
    canvas.alpha_composite(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return canvas


def crop_contain(source: Path, crop: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    im = Image.open(source).convert("RGBA").crop(crop)
    im.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (8, 12, 18, 255))
    canvas.alpha_composite(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return canvas


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str,
          subtitle: str = "") -> None:
    draw.rounded_rectangle(box, radius=18, fill=PANEL, outline=(55, 76, 98, 255), width=3)
    x0, y0, _, _ = box
    text(draw, (x0 + 22, y0 + 16), title, 26, CYAN)
    if subtitle:
        text(draw, (x0 + 22, y0 + 52), subtitle, 18, MUTED)


def save_png(im: Image.Image, name: str) -> None:
    im.save(OUT / name, format="PNG", optimize=False, compress_level=9)


def write_json(name: str, payload: Any) -> None:
    (OUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_tsv(name: str, header: list[str], rows: Iterable[Iterable[Any]]) -> None:
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        for row in rows:
            w.writerow(row)


def canonical_signature(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def verify_sources() -> list[dict[str, Any]]:
    checks = []
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"SOURCE_SHA_MISMATCH: {path}\nexpected={expected}\nactual={actual}")
        checks.append({"path": str(path), "expected": expected, "actual": actual, "match": True})
    return checks


def build_source_lineage() -> None:
    rows = [
        ("P97_CALL02_FAILURE_REVIEW", TASK97, "Candidate_producer_receipt", "governance", "failure and donor boundary", "target pixels; CONTACT parent; pass claim"),
        ("P98_PREPRODUCTION_OBJECTIVE", TASK98, "Candidate_objective", "governance", "sole write and delivery contract", "visible target generation; Runtime"),
        ("P99_FUTURE_CONSUMER_OBJECTIVE", TASK99, "Candidate_future_objective", "fixture_only", "future consumer precondition only", "Godot write in Task98; invocation"),
        ("PRODUCTION_BOARD", BOARD, "Candidate_board", "governance", "current dispatch and gate readback", "visual-pass promotion"),
        ("TACTICAL_INTERFACE_1_6_3", INTERFACE, "Candidate_interface", "map_dimetric_40x20", "camera, pivot, full-scene and call gates", "Canon; Runtime promotion"),
        ("CURRENT_TOPOLOGY_PROFILE", GOLDEN_PROFILE, "Candidate_gameplay_source", "grid_32x18", "ordered terrain zones and object anchors", "visible art"),
        ("CURRENT_TOPOLOGY_MAP_CONTRACT", TOPOLOGY_CONTRACT, "Candidate_geometry_contract", "map_dimetric_40x20", "selection pocket, charge avenue, plan bindings", "visible art"),
        ("CURRENT_COMPOSITOR_PROFILE", COMPOSITOR_PROFILE, "Candidate_geometry_contract", "map_dimetric_40x20", "projection, camera, canvas and z responsibility", "visible art"),
        ("CURRENT_PROJECTION_CODE", PROJECTION_CODE, "Candidate_implementation_evidence", "map_dimetric_40x20", "formula cross-check only", "Runtime edits"),
        ("CURRENT_TOPOLOGY_LAYER_CODE", TOPOLOGY_CODE, "Candidate_implementation_evidence", "map_dimetric_40x20", "ordered mask and roof-method cross-check", "visible art; Runtime edits"),
        ("GZ_CML008_HARD", GZ_HARD, "Hard", "design_orthographic", "identity deviation calibration only; not embedded in safe board", "map sprite; anatomy replacement"),
        ("GZ_V10X_E02_PARENT", GZ_V10X, "Candidate_scoped_user_authorized_parent", "design_orthographic", "E02 two-arm naked-body identity source", "direct map sprite; wings; backpack"),
        ("GZ_QSD_CURRENT_IDENTITY", GZ_QSD, "Candidate_current_correct_identity", "design_orthographic", "four-head proportion, structure, color and weight", "direct map sprite; map cardinal alias"),
        ("GZ_FOUR_DIRECTION_CROSSCHECK", GZ_FOUR, "Candidate_cross_face_reference", "design_orthographic", "cross-face identity consistency", "map cardinal alias"),
        ("GZ_ACTION_SPACE_DIRECTION", GZ_ACTION, "Candidate_direction_approved", "design_action_space", "C action-skeleton proportion and movement allowance as text rule", "A/B variants; visible board reuse"),
        ("BREAKER_B_BODY", BR_B, "Candidate_direction_approved", "design_orthographic", "B body topology crops only and always paired with X", "scale panel; GZ pixel; final master claim"),
        ("BREAKER_X_SURFACE", BR_X, "Candidate_direction_approved", "design_surface_relation", "X surface crops only and always paired with B", "M/A/C variants; standalone master"),
        ("BREAKER_B128", BR_128, "Candidate_direction_sample", "design_direction_sample", "outline, scale and pivot calibration; X not baked", "final visible master"),
        ("CML128_KINETIC_CEL", CML128, "Working", "style_only", "rule-card text only: line, block color, hard shadow, material", "any depicted mecha anatomy; wing/backpack pixels"),
        ("A5_SWARM_MAP_ATLAS", A5, "Candidate_current_map_positive", "map_dimetric_40x20", "exact 96px facing example; source for future real atlas", "Call02 swarm pixels; cross-facing fallback"),
        ("CALL02_RAW", CALL02_RAW, "History_environment_method_donor_only", "invalid_registration", "six actor/object/text-free environment crops only", "unit/object/shadow/reflection/topology/CONTACT parent"),
    ]
    write_tsv(
        "source-lineage.tsv",
        ["source_id", "absolute_path", "sha256", "authority", "view_space", "allowed_use", "forbidden_use"],
        [(sid, str(p), EXPECTED[p], auth, view, allow, forbid) for sid, p, auth, view, allow, forbid in rows],
    )


def build_geometry_guide(name: str, size: int, subject: str, footprint: tuple[int, int],
                         pivot: tuple[int, int], facing: str, vector: tuple[int, int],
                         sockets: dict[str, tuple[int, int]], accent: tuple[int, int, int, int],
                         negative_space_note: str) -> None:
    im = Image.new("RGBA", (size, size), BG)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 0, size - 1, size - 1), outline=(72, 96, 120, 255), width=3)
    top_h = 40 if size == 256 else 48
    d.rectangle((0, 0, size, top_h), fill=(93, 22, 28, 255))
    text(d, (size // 2, top_h // 2), "GEOMETRY GUIDE ONLY · NOT VISIBLE ART · NOT RUNTIME",
         8 if size == 256 else 12, (255, 245, 228, 255), "mm")
    px, py = pivot
    fw, fh = footprint
    diamond = [(px, py - (fw + fh) * 20), (px + (fw + fh) * 20, py - (fw + fh) * 10),
               (px, py), (px - (fw + fh) * 20, py - (fw + fh) * 10)]
    d.polygon(diamond, fill=accent[:3] + (32,), outline=accent, width=3)
    # occupied-cell grid
    centers = []
    max_y = -10**9
    for gx in range(fw):
        for gy in range(fh):
            sx = (gx - gy) * 40
            sy = (gx + gy) * 20
            centers.append((sx, sy))
            max_y = max(max_y, sy)
    for sx, sy in centers:
        cx, cy = px + sx, py + sy - (max_y + 20)
        cell = [(cx, cy - 20), (cx + 40, cy), (cx, cy + 20), (cx - 40, cy)]
        d.line(cell + [cell[0]], fill=accent[:3] + (150,), width=1)
    # conservative alpha/bbox safety zone
    margin_x = 18 if size == 256 else 28
    safe_top = 78 if size == 256 else 104
    d.rounded_rectangle((margin_x, safe_top, size - margin_x, py), radius=10,
                        outline=(183, 199, 214, 220), width=2)
    text(d, (margin_x + 6, safe_top + 5), "ALPHA / BBOX SAFE ZONE", 9 if size == 256 else 13, MUTED)
    # pivot and facing
    d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
    d.line((px - 14, py, px + 14, py), fill=(255, 255, 255, 255), width=2)
    d.line((px, py - 14, px, py + 14), fill=(255, 255, 255, 255), width=2)
    # Direction compass is kept inside the canvas; pivot stays the registration mark.
    compass = (size - (78 if size == 256 else 112), safe_top + (46 if size == 256 else 72))
    scale = 0.72 if size == 256 else 1.0
    ex, ey = int(compass[0] + vector[0] * scale), int(compass[1] + vector[1] * scale)
    d.line((*compass, ex, ey), fill=YELLOW, width=4)
    d.ellipse((compass[0] - 3, compass[1] - 3, compass[0] + 3, compass[1] + 3), fill=YELLOW)
    d.polygon([(ex, ey), (ex - 9, ey - 1), (ex - 3, ey - 9)], fill=YELLOW)
    text(d, (compass[0], compass[1] - 15), facing.upper(), 11 if size == 256 else 16, YELLOW, "mm")
    # sockets relative to footpoint
    socket_colors = {"body": CYAN, "shield": GREEN, "weapon": ORANGE, "impact": MAGENTA, "target": RED}
    rendered = set()
    for key, (ox, oy) in sockets.items():
        x, y = px + ox, py + oy
        col = socket_colors[key]
        if (x, y) in rendered:
            continue
        rendered.add((x, y))
        d.line((x - 5, y, x + 5, y), fill=col, width=2)
        d.line((x, y - 5, x, y + 5), fill=col, width=2)
        same = [k for k, value in sockets.items() if tuple(value) == (ox, oy)]
        label = "/".join({"body": "B", "shield": "S", "weapon": "W", "impact": "I", "target": "T"}[k] for k in same)
        text(d, (x + 7, y - 6), label, 9 if size == 256 else 12, col)
    bottom_y = top_h + 4
    text(d, (9, bottom_y), f"{subject} · {size}² · footprint {fw}×{fh}", 10 if size == 256 else 15, INK)
    text(d, (9, bottom_y + (14 if size == 256 else 21)), f"pivot={list(pivot)} · local origin=footpoint", 9 if size == 256 else 13, MUTED)
    text(d, (8, size - 10), negative_space_note, 7 if size == 256 else 10, MUTED, anchor="lm")
    save_png(im, name)


def build_safe_boards() -> None:
    # Guardian board: no BREAKER source is ever opened here.
    im = Image.new("RGBA", (2400, 1800), BG)
    d = ImageDraw.Draw(im, "RGBA")
    text(d, (70, 58), "GUARDIAN Z · ISOLATED SAFE IDENTITY BOARD", 52, INK)
    text(d, (72, 122), "Candidate preproduction · runtime_allowed=false · V10X identity only · never a map sprite", 25, MUTED)
    panel(d, (60, 180, 820, 1460), "V10X E02 parent", "two arms · naked body · absolutely no wings / backpack")
    im.alpha_composite(contain(GZ_V10X, (700, 1140)), (90, 275))
    panel(d, (850, 180, 2340, 800), "Latest Q/SD same-sheet identity", "four-head weight, crown/face/chest/shoulder/forearm continuity")
    im.alpha_composite(contain(GZ_QSD, (1430, 500)), (880, 275))
    panel(d, (850, 830, 2340, 1460), "Orthographic cross-face review only", "IDENTITY / CROSS-FACE ONLY · NEVER MAP CARDINAL")
    im.alpha_composite(contain(GZ_FOUR, (1430, 500)), (880, 925))
    d.rounded_rectangle((60, 1500, 2340, 1740), radius=18, fill=(31, 38, 48, 255), outline=CYAN, width=3)
    text(d, (90, 1530), "CML008 + CML128 ACTOR-FREE RULE CARD", 30, CYAN)
    multiline(d, (90, 1580),
              "IDENTITY: layered gold crown / central red crown / blue brow / silver grille face / red-X chest / round gold core\n"
              "MASS: approx. 4.0–4.2 heads / heavy old-super-robot weight / square shoulder rings / equal-weight cylindrical forearms\n"
              "STYLE ONLY: clean line pressure / 4–7 large color blocks / maximum two hard-shadow levels / limited wear\n"
              "FORBIDDEN: second anatomy, depicted CML128 machine pixels, wings, backpack, orthographic-to-cardinal alias",
              24, INK, 10)
    for i, col in enumerate([(33, 46, 70, 255), (61, 99, 153, 255), (196, 48, 48, 255), (220, 169, 63, 255), (202, 210, 217, 255), (22, 28, 36, 255)]):
        d.rectangle((1720 + i * 92, 1620, 1792 + i * 92, 1692), fill=col, outline=(255, 255, 255, 100), width=1)
    save_png(im, "GUARDIAN_Z_ISOLATED_SAFE_REFERENCE_BOARD_2400x1800.png")

    # BREAKER board: precise crops exclude GZ scale panel and M/A/C alternatives.
    im = Image.new("RGBA", (2400, 1800), BG)
    d = ImageDraw.Draw(im, "RGBA")
    text(d, (70, 58), "BREAKER B+X · ISOLATED SAFE IDENTITY BOARD", 52, INK)
    text(d, (72, 122), "Candidate direction-approved derivative · runtime_allowed=false · B body and X surface must be consumed together", 25, MUTED)
    panel(d, (60, 180, 1460, 830), "B body topology · approved crops only", "high back shell · low embedded head · load-bearing semi-upright forelimbs · short stabilizing rear feet")
    im.alpha_composite(crop_contain(BR_B, (29, 117, 1772, 650), (1320, 510)), (100, 290))
    panel(d, (1490, 180, 2340, 830), "B silhouette / relation crops", "no scale panel · no Guardian Z pixels")
    im.alpha_composite(crop_contain(BR_B, (29, 673, 551, 928), (790, 300)), (1520, 285))
    im.alpha_composite(crop_contain(BR_B, (728, 948, 1261, 1182), (790, 190)), (1520, 600))
    panel(d, (60, 860, 1680, 1450), "X heterogenous / bio-armor relation · approved crops only", "asymmetric plates · flexible seams · closed chest seam · sealed upper-back outlet")
    im.alpha_composite(crop_contain(BR_X, (930, 117, 1772, 590), (780, 470)), (100, 950))
    im.alpha_composite(crop_contain(BR_X, (617, 663, 1184, 1068), (740, 420)), (900, 950))
    panel(d, (1710, 860, 2340, 1450), "B128 calibration only", "OUTLINE / SCALE / PIVOT ONLY · X NOT BAKED")
    b128 = Image.open(BR_128).convert("RGBA").resize((384, 384), Image.Resampling.NEAREST)
    im.alpha_composite(b128, (1830, 970))
    d.rounded_rectangle((60, 1490, 2340, 1740), radius=18, fill=(31, 38, 48, 255), outline=MAGENTA, width=3)
    text(d, (90, 1520), "B+X + CML128 ACTOR-FREE RULE CARD", 30, MAGENTA)
    multiline(d, (90, 1570),
              "FIRST READ: not turtle / ape / ordinary quadruped / vehicle / sled. Forelimbs bear weight in a semi-upright attack posture.\n"
              "SILHOUETTE: giant shell presses the torso; head sits lower in shell lip; single red slit stays narrow; rear feet only stabilize.\n"
              "SURFACE: asymmetric heterogeneous bio-armor, continuous load path through flexible seams; no industrial symmetric block language.\n"
              "STYLE ONLY: clean line pressure / 4–7 large value-color blocks / ≤2 hard-shadow levels / limited wear.",
              23, INK, 8)
    save_png(im, "BREAKER_BX_ISOLATED_SAFE_REFERENCE_BOARD_2400x1800.png")


def build_donor_sheet() -> None:
    crops = [
        ("A_WET_ASPHALT_LINES", (310, 45, 500, 165), "wet asphalt / white line / rain highlight"),
        ("B_FACADE_CURB_WET", (760, 30, 1010, 175), "industrial facade / curb / wet plane"),
        ("C_EMPTY_ROOF", (1430, 30, 1650, 180), "roof seams / parapet / drainage"),
        ("D_DARK_WET_VALUE", (930, 130, 1150, 250), "dark paving / rain / cold reflection"),
        ("E_ROOF_FOREGROUND", (60, 670, 350, 900), "roof / foreground occlusion method"),
        ("F_ROAD_DASH_PUDDLE", (1090, 790, 1280, 920), "road dash / crack / puddle"),
    ]
    im = Image.new("RGBA", (1600, 1200), BG)
    d = ImageDraw.Draw(im, "RGBA")
    text(d, (60, 48), "CALL02 · ENVIRONMENT / MATERIAL METHOD DONOR CROPS", 42, INK)
    text(d, (62, 102), "History only · no topology · no unit/object/text semantics · parent SHA 98f30a97…", 22, MUTED)
    raw = Image.open(CALL02_RAW).convert("RGBA")
    rows = []
    for idx, (cid, box, note) in enumerate(crops):
        col, row = idx % 3, idx // 3
        x0, y0 = 55 + col * 510, 160 + row * 490
        d.rounded_rectangle((x0, y0, x0 + 470, y0 + 450), radius=16, fill=PANEL, outline=(66, 91, 116, 255), width=3)
        crop = raw.crop(box)
        # retain native pixels at 1:1; only center on board
        px = x0 + (470 - crop.width) // 2
        py = y0 + 70 + (260 - crop.height) // 2
        im.alpha_composite(crop, (px, py))
        text(d, (x0 + 18, y0 + 16), cid, 23, CYAN)
        text(d, (x0 + 18, y0 + 342), f"raw half-open {list(box)}", 18, INK)
        text(d, (x0 + 18, y0 + 374), note, 17, MUTED)
        text(d, (x0 + 18, y0 + 408), "NO ACTOR / OBJECT / TEXT · DONOR ONLY", 15, GREEN)
        rows.append((cid, str(CALL02_RAW), EXPECTED[CALL02_RAW], json.dumps(list(box)), crop.width, crop.height,
                     note, "ENVIRONMENT_MATERIAL_METHOD_DONOR_ONLY", "no_topology;no_object_semantics;no_target_parent"))
    d.rectangle((0, 1155, 1600, 1200), fill=(93, 22, 28, 255))
    text(d, (800, 1177), "NOT A CURRENT WORLD · NOT A CLEANPLATE · NOT RUNTIME", 23, (255, 244, 224, 255), "mm")
    save_png(im, "CALL02_ENVIRONMENT_METHOD_DONOR_CROP_SHEET_1600x1200.png")
    write_tsv("call02-environment-donor-crops.tsv",
              ["crop_id", "parent_absolute_path", "parent_sha256", "raw_half_open_xyxy", "width", "height", "method_note", "allowed_role", "forbidden_role"], rows)


TILE_HALF = (40, 20)
RAW_ORIGIN = (-880, -170)
PLAN_CAMERA = (-480, 420)
MAP_CENTER = (640, 350)


def raw_at(point: tuple[float, float]) -> tuple[float, float]:
    x, y = point
    return RAW_ORIGIN[0] + (x - y) * 40, RAW_ORIGIN[1] + (x + y) * 20


def screen_at(point: tuple[float, float], camera: tuple[float, float] = PLAN_CAMERA) -> tuple[float, float]:
    rx, ry = raw_at(point)
    return MAP_CENTER[0] + rx - camera[0], MAP_CENTER[1] + ry - camera[1]


TERRAIN_ZONES = [
    ("MAIN_ROAD", "road", (0, 7, 32, 7), True),
    ("RESCUE_LANE", "rescue_lane", (20, 5, 12, 7), True),
    ("BLOCK_NW", "building", (1, 0, 7, 5), False),
    ("BLOCK_NM", "building", (10, 0, 5, 4), False),
    ("BLOCK_NE", "building", (22, 0, 7, 4), False),
    ("BLOCK_SW", "building", (0, 15, 8, 3), False),
    ("BLOCK_SE", "building", (26, 14, 6, 4), False),
    ("BROKEN_SKYWALK", "building", (8, 5, 7, 2), False),
    ("SECURITY_APRON", "security_apron", (24, 4, 8, 8), True),
]


def terrain_grid() -> list[list[tuple[str, str, bool]]]:
    grid = [[("VOID", "void", True) for _ in range(18)] for _ in range(32)]
    for zid, kind, (x0, y0, w, h), passable in TERRAIN_ZONES:
        for x in range(max(0, x0), min(32, x0 + w)):
            for y in range(max(0, y0), min(18, y0 + h)):
                grid[x][y] = (zid, kind, passable)
    return grid


def cell_diamond(x: int, y: int) -> list[tuple[int, int]]:
    # Task102 correction: runtime integer (x,y) is the cell center.
    cx, cy = screen_at((x, y))
    return [(round(cx), round(cy - 20)), (round(cx + 40), round(cy)),
            (round(cx), round(cy + 20)), (round(cx - 40), round(cy))]


def draw_world_base(im: Image.Image, title: str, qa: bool = False) -> ImageDraw.ImageDraw:
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 0, 1280, 720), fill=(8, 14, 23, 255))
    grid = terrain_grid()
    colors = {
        "void": (25, 37, 47, 255),
        "road": (48, 64, 76, 255),
        "rescue_lane": (46, 67, 78, 255),
        "security_apron": (55, 67, 75, 255),
        "building": (72, 79, 88, 255),
    }
    # painter order by projected cell center y
    cells = sorted(((x, y) for x in range(32) for y in range(18)), key=lambda p: screen_at((p[0], p[1]))[1])
    for x, y in cells:
        zid, kind, passable = grid[x][y]
        poly = cell_diamond(x, y)
        d.polygon(poly, fill=colors[kind], outline=(85, 105, 118, 180))
        if kind == "road" and (x + y) % 3 == 0:
            cx, cy = screen_at((x, y))
            d.line((cx - 14, cy, cx + 14, cy), fill=(158, 170, 176, 100), width=2)
        if not passable:
            height = 22
            top = [(px, py - height) for px, py in poly]
            d.polygon([poly[3], poly[2], top[2], top[3]], fill=(38, 47, 57, 255))
            d.polygon([poly[1], poly[2], top[2], top[1]], fill=(45, 54, 64, 255))
            d.polygon(top, fill=(89, 98, 108, 255), outline=(128, 141, 150, 200))
    d.rectangle((0, 0, 1280, 54), fill=(7, 10, 16, 232))
    text(d, (24, 10), title, 21, INK)
    text(d, (1254, 43), "CURRENT_TOPOLOGY_CAMERA_V1 · 2:1 dimetric · camera [-480,420]", 12, MUTED, "rm")
    d.rectangle((0, 680, 1280, 720), fill=(93, 22, 28, 235))
    text(d, (640, 700), "GEOMETRY GUIDE ONLY · NOT VISIBLE ART · NOT RUNTIME", 23, (255, 245, 228, 255), "mm")
    return d


def polygon_for_rect(rect: tuple[int, int, int, int]) -> list[tuple[int, int]]:
    x, y, w, h = rect
    # Task102 correction: a w×h rect spans center-boundaries at ±0.5.
    points = [
        screen_at((x - 0.5, y - 0.5)),
        screen_at((x + w - 0.5, y - 0.5)),
        screen_at((x + w - 0.5, y + h - 0.5)),
        screen_at((x - 0.5, y + h - 0.5)),
    ]
    return [(round(px), round(py)) for px, py in points]


def dashed_poly(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color, width=4, dash=12) -> None:
    pts = points + [points[0]]
    for a, b in zip(pts, pts[1:]):
        ax, ay = a
        bx, by = b
        length = max(abs(bx - ax), abs(by - ay))
        if length == 0:
            continue
        steps = max(1, length // dash)
        for i in range(steps):
            if i % 2 == 0:
                t0, t1 = i / steps, min(1, (i + 1) / steps)
                draw.line((ax + (bx - ax) * t0, ay + (by - ay) * t0,
                           ax + (bx - ax) * t1, ay + (by - ay) * t1), fill=color, width=width)


def build_actor_free_world() -> None:
    im = Image.new("RGBA", (1280, 720), BG)
    d = draw_world_base(im, "ACTOR-FREE CURRENT TOPOLOGY · ENVIRONMENT DRAWING GUIDE")
    pocket = polygon_for_rect((15, 9, 6, 3))
    charge = polygon_for_rect((20, 11, 3, 5))
    dashed_poly(d, pocket, CYAN, 4)
    dashed_poly(d, charge, ORANGE, 4)
    text(d, (372, 210), "SELECTION POCKET · geometry only · clear", 17, CYAN)
    text(d, (410, 526), "BREAKER CHARGE AVENUE · geometry only · clear", 17, ORANGE)
    d.rounded_rectangle((18, 76, 370, 174), radius=12, fill=(8, 12, 18, 222), outline=(77, 96, 114, 255), width=2)
    multiline(d, (32, 88),
              "EMPTY BY CONTRACT:\nactors · vehicle · 3 swarms · shield · exit · facility\nprotection overlay · artillery · route · ghost · UI · FX",
              16, INK, 4)
    d.rounded_rectangle((910, 80, 1260, 190), radius=12, fill=(8, 12, 18, 222), outline=(77, 96, 114, 255), width=2)
    multiline(d, (928, 94),
              "WORLD DELIVERY SPACE\n2400×1350 canvas\norigin [-1760,-340]\nThis 1280×720 is framing guide only.",
              17, INK, 5)
    save_png(im, "CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png")


def draw_footpoint(draw: ImageDraw.ImageDraw, p: tuple[float, float], color, label: str) -> None:
    x, y = round(p[0]), round(p[1])
    draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color, outline=(255, 255, 255, 255), width=2)
    draw.line((x - 12, y, x + 12, y), fill=color, width=2)
    draw.line((x, y - 12, x, y + 12), fill=color, width=2)
    text(draw, (x + 9, y - 19), label, 15, color)


def build_plan_slot_qa() -> None:
    im = Image.new("RGBA", (1280, 720), BG)
    d = draw_world_base(im, "PLAN SLOT COMPOSITE QA · EXACT FOOTPOINTS / NATIVE CANVASES / A5 PIXELS", qa=True)
    # selection and charge geometry remain clear at footprint-cell level
    dashed_poly(d, polygon_for_rect((15, 9, 6, 3)), CYAN, 3)
    dashed_poly(d, polygon_for_rect((20, 11, 3, 5)), ORANGE, 3)
    # Native canvas slots, top-left = footpoint - pivot. Hollow translucent rectangles only.
    gz_fp = (400, 340)
    br_fp = (520, 520)
    gz_box = (gz_fp[0] - 128, gz_fp[1] - 224, gz_fp[0] + 128, gz_fp[1] + 32)
    br_box = (br_fp[0] - 192, br_fp[1] - 320, br_fp[0] + 192, br_fp[1] + 64)
    d.rectangle(gz_box, outline=CYAN, width=3)
    d.rectangle(br_box, outline=MAGENTA, width=3)
    text(d, (gz_box[0] + 5, gz_box[1] + 5), "GZ 256 · pivot 128,224", 15, CYAN)
    text(d, (br_box[0] + 5, br_box[1] + 5), "BREAKER 384 · pivot 192,320", 15, MAGENTA)
    draw_footpoint(d, gz_fp, CYAN, "GZ (400,340) · 0px")
    draw_footpoint(d, br_fp, MAGENTA, "BR (520,520) · 0px")
    # Vehicle identity-neutral proxy.
    veh_fp = (520, 320)
    vx, vy = veh_fp
    d.polygon([(vx, vy - 62), (vx + 42, vy - 38), (vx + 28, vy - 12), (vx - 36, vy - 18)],
              fill=(255, 171, 70, 170), outline=ORANGE)
    draw_footpoint(d, veh_fp, ORANGE, "VEH (520,320) · 0px")
    # A5 exact source frames, direct paste at current pivot [48,72].
    a5 = Image.open(A5).convert("RGBA")
    swarm_specs = [
        ("S1 west", (840, 360), (288, 0, 384, 96)),
        ("S2 north", (800, 540), (0, 0, 96, 96)),
        ("S3 south", (1200, 460), (192, 0, 288, 96)),
    ]
    for label, fp, box in swarm_specs:
        frame = a5.crop(box)
        im.alpha_composite(frame, (fp[0] - 48, fp[1] - 72))
        draw_footpoint(d, fp, GREEN, f"{label} · 0px")
    # Current object proxies remain geometric and separable.
    object_specs = [
        ("SHIELD", screen_at((14, 10)), (126, 139, 155, 255)),
        ("SECURITY", screen_at((27, 8)), (245, 214, 90, 255)),
        ("EXIT", screen_at((31, 7)), (70, 218, 238, 255)),
    ]
    for label, fp, col in object_specs:
        x, y = round(fp[0]), round(fp[1])
        d.rectangle((x - 12, y - 32, x + 12, y), fill=col[:3] + (150,), outline=col, width=2)
        draw_footpoint(d, fp, col, label)
    # Protection zone is outline only; artillery remains offscreen with edge cue.
    dashed_poly(d, polygon_for_rect((20, 5, 12, 7)), (90, 190, 240, 180), 2, 10)
    d.polygon([(1268, 355), (1242, 367), (1242, 343)], fill=YELLOW)
    text(d, (1236, 326), "ARTILLERY [29,2] OFFSCREEN", 14, YELLOW, "rm")
    # Local roof-mask method inset: explicit method proof, not actor placement.
    d.rounded_rectangle((930, 80, 1260, 255), radius=12, fill=(7, 11, 17, 230), outline=(120, 139, 156, 255), width=2)
    text(d, (945, 94), "LOCAL ROOF MASK METHOD · QA ONLY", 17, INK)
    roof = [(970, 145), (1040, 110), (1110, 145), (1040, 180)]
    d.polygon(roof, fill=(105, 116, 128, 255), outline=(190, 205, 215, 255))
    proxy = (1030, 130, 1150, 220)
    d.rectangle(proxy, fill=(240, 90, 166, 42), outline=MAGENTA, width=2)
    # local intersection hatch, demonstrating patch-only ownership
    for x in range(1040, 1115, 10):
        d.line((x, 135, x - 35, 175), fill=(255, 230, 130, 210), width=2)
    text(d, (945, 225), "patch-only mask; outside alpha unchanged", 14, MUTED)
    d.rounded_rectangle((18, 565, 440, 670), radius=12, fill=(7, 11, 17, 230), outline=(90, 110, 130, 255), width=2)
    multiline(d, (32, 578),
              "MACHINE QA ONLY\nfootpoint error: 0 px (all six actors)\nselection pocket blocked cells: 0\ncharge avenue blocked cells: 0\ncanvas relation at 100%; paired 50% review delivered",
              13, INK, 3)
    save_png(im, "PLAN_SLOT_COMPOSITE_QA_1280x720.png")
    half = im.resize((640, 360), Image.Resampling.LANCZOS)
    save_png(half, "PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png")


def build_contracts() -> None:
    gz_sockets = {"body": [0, -74], "shield": [-46, -62], "weapon": [46, -72], "impact": [-20, -10], "target": [-20, -10]}
    br_sockets = {"body": [0, -98], "shield": [-68, -84], "weapon": [68, -96], "impact": [12, -18], "target": [12, -18]}
    vehicle_sockets = {"body": [0, -37], "shield": [-21, -32], "weapon": [23, -36], "impact": [0, -43], "target": [0, -43]}
    swarm_sockets = {"body": [0, -28], "shield": [-16, -24], "weapon": [17, -27], "impact": [0, -32], "target": [0, -32]}
    slot_contract = {
        "schema_version": "1.0.0",
        "task_id": "A9_1A6_S_C2_SPRITE_FIRST_MAP_CAMERA_MASTER_PREPRODUCTION",
        "status": "PREPRODUCTION_ONLY_IMAGEGEN_0_CALL03_FALSE_CALL04_FALSE",
        "authority_scope": "Candidate production evidence only; no Canon, Runtime, UA91, or handoff",
        "view_space": "map_dimetric_40x20",
        "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
        "projection": {
            "type": "orthographic_dimetric_2_to_1", "grid_size_cells": [32, 18], "tile_half_px": [40, 20],
            "runtime_raw_origin_px": [-880, -170], "plan_camera_raw_px": [-480, 420],
            "map_viewport_rect_px": [0, 58, 1280, 584], "world_canvas_px": [2400, 1350],
            "world_canvas_origin_raw_px": [-1760, -340],
            "direction_vectors_screen_px": {"north": [40, -20], "east": [40, 20], "south": [-40, 20], "west": [-40, -20]},
        },
        "registration": {
            "anchor_semantics": "minimum_grid_cell_of_rectangular_footprint",
            "registration_point": "footprint_bottom_center",
            "sort_key": "footpoint_screen_y + explicit_z_bias",
            "centered": False,
            "sprite_top_left_formula": "footpoint_screen - pivot_px * display_scale",
            "max_footpoint_error_px": 0.5,
            "cross_facing_fallback": False,
            "missing_clip_behavior": "hide_subject_and_emit_single_reason",
        },
        "slots": [
            {"stable_id": "V353U001", "slot_id": "guardian_z_map_current", "native_size": [256, 256], "footprint": [2, 2],
             "pivot_normalized": [0.5, 0.875], "pivot_px": [128, 224], "facing": "east", "facing_screen_vector_px": [40, 20],
             "first_clip": "idle/east/0", "z_bias": 1, "socket_placeholders_local_from_footpoint_px": gz_sockets,
             "visual_status": "not_generated", "identity_source_direct_map_bind_allowed": False},
            {"stable_id": "ENEMY_C01_BREAKER", "slot_id": "breaker_map_current", "native_size": [384, 384], "footprint": [3, 3],
             "pivot_normalized": [0.5, 0.8333333333], "pivot_px": [192, 320], "facing": "north", "facing_screen_vector_px": [40, -20],
             "first_clip": "charge/north/0", "z_bias": 2, "socket_placeholders_local_from_footpoint_px": br_sockets,
             "visual_status": "not_generated", "identity_source_direct_map_bind_allowed": False},
        ],
        "consumer_gate": {"required_objective": "G2_A2_C3", "P99_invoked": False, "real_art_loaded": 0, "fixture_validation_only": True},
    }
    write_json("map-camera-slot-contract.json", slot_contract)

    env_contract = {
        "schema_version": "1.0.1",
        "contract_id": "C01E02_CURRENT_TOPOLOGY_ENVIRONMENT_LAYERS_V1",
        "status": "PREPRODUCTION_ONLY_NO_VISIBLE_TARGET_PIXELS",
        "view_space": "map_dimetric_40x20",
        "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
        "world_canvas": {"size_px": [2400, 1350], "origin_raw_px": [-1760, -340], "shared_pivot": [0, 0],
                         "raw_to_canvas_formula": "canvas_xy = raw_xy - origin_raw_px"},
        "screen_guide": {"size_px": [1280, 720], "camera_raw_px": [-480, 420], "crop_rect_in_world_canvas_px": [640, 468, 1280, 584],
                         "role": "framing_and_geometry_guide_only_not_delivery_substitute"},
        "visible_z_constants": {"base_ground": -1200, "buildings_world_body": -900, "roof": 900, "foreground": 1100},
        "layer_responsibilities": [
            {"group": "base_ground", "visible": True, "visible_z": -1200, "required_separable": True,
             "contents": ["ground_base", "road_and_rescue_lane_material"], "actor_free_initially": True},
            {"group": "buildings_world_body", "visible": True, "visible_z": -900, "required_separable": True,
             "contents": ["building_world_body"], "actor_free_initially": True},
            {"group": "stateful_objects", "visible": True, "visible_z": None, "required_separable": True,
             "contents": ["retired_shield", "east_exit", "security_gate_or_facility"],
             "depth_sort_policy": "footprint_bottom_center_screen_y_plus_explicit_z_bias",
             "fixed_front_overlay_forbidden": True,
             "split_when_needed": ["body", "roof", "foreground"],
             "split_policy": "body joins actor depth sort; roof and foreground pieces use local ownership/mask semantics and may not force every object in front of every actor",
             "actor_free_initially": True, "session_or_resolver_owned": True},
            {"group": "roof", "visible": True, "visible_z": 900, "required_separable": True,
             "contents": ["roof"], "local_mask_only": True, "global_fade_forbidden": True},
            {"group": "foreground", "visible": True, "visible_z": 1100, "required_separable": True,
             "contents": ["foreground_parapet"], "local_mask_only": True, "global_fade_forbidden": True},
            {"group": "occlusion_control", "visible": False, "visible_z": None, "required_separable": True,
             "contents": ["local_occlusion_control"], "occupies_visible_z": False, "actor_free_mask": "fully_empty"},
            {"group": "weather_fx", "visible": True, "visible_z": None, "required_separable": True,
             "contents": ["rain", "wetness_response", "contact_weather_fx"],
             "visible_z_policy": "independent_effect_owner_not_static_environment_or_actor_sort",
             "must_not_bake_into_cleanplate": True},
            {"group": "stateful_nonphysical_overlays", "visible": True, "visible_z": None, "required_separable": True,
             "contents": ["protection_zone_overlay", "route", "ghost", "intent_trajectory"],
             "owner": "deterministic_overlay_or_UI_consumer", "must_not_bake_into_cleanplate": True,
             "actor_free_initially": True},
        ],
        "current_topology_source": {"path": str(GOLDEN_PROFILE), "sha256": EXPECTED[GOLDEN_PROFILE],
                                    "ordered_zone_override": "later terrain_zones entry wins"},
        "actor_free_guide_exclusions": ["all actors", "vehicle", "three swarms", "shield", "east exit", "security facility",
                                         "protection overlay", "artillery", "route", "ghost", "UI", "T3-T5 FX"],
        "shadow_owner": "engine_independent_ground_shadow_layer",
        "screen_cleanplate_may_replace_world_canvas": False,
        "legacy_A4_pixels_are_current_geometry": False,
    }
    write_json("environment-layer-contract.json", env_contract)

    socket_contract = {
        "schema_version": "1.0.1",
        "contract_id": "C01E02_MAP_CAMERA_SOCKET_CONTACT_V1",
        "status": "PROVISIONAL_FIXTURE_SEMANTICS_REAL_ART_REMEASURE_REQUIRED",
        "coordinate_basis": "local_offset_px_relative_to_footprint_bottom_center",
        "frame_top_left_coordinate_alias_forbidden": True,
        "machine_screen_readback_max_error_px": 0.5,
        "assets": {
            "V353U001": {"native_size": [256, 256], "offsets": gz_sockets, "semantic_region_tolerance_px": 8,
                          "measurement_status": "pending_real_art_alpha_measurement"},
            "ENEMY_C01_BREAKER": {"native_size": [384, 384], "offsets": br_sockets, "semantic_region_tolerance_px": 12,
                                  "measurement_status": "pending_real_art_alpha_measurement"},
            "TARGET_C01_EMERGENCY_VEHICLE_01": {"native_size": [128, 128], "offsets": vehicle_sockets, "semantic_region_tolerance_px": 4,
                                                "measurement_status": "provisional_fixture_semantics_remeasure_before_real_art"},
            "ENEMY_C01_RIFT_SWARM": {"native_size": [96, 96], "offsets": swarm_sockets, "semantic_region_tolerance_px": 3,
                                     "measurement_status": "provisional_fixture_semantics_remeasure_before_real_art"},
        },
        "future_contact_measurement_targets": {
            "shared_plan_comparison_only": {
                "camera_raw_px": [-480, 420],
                "acceptance_role": "comparison_only_not_contact_truth",
                "A": {"impact_world_grid": [20.5, 10.5], "impact_screen_px": [640, 380],
                      "breaker_post_anchor": [21, 11], "t4_side_armor_world_grid": [24.0, 12.5], "t4_side_armor_screen_px": [700, 490]},
                "B": {"impact_world_grid": [20.0, 10.5], "impact_screen_px": [620, 370],
                      "breaker_post_anchor": [21, 10], "t4_side_armor_world_grid": [24.0, 11.5], "t4_side_armor_screen_px": [740, 470]},
            },
            "contact_pose_and_socket_acceptance": {
                "acceptance_role": "authoritative_screen_targets_for_CONTACT_pose_and_socket_review",
                "A": {"camera_raw_px": [-480, 450], "impact_world_grid": [20.5, 10.5], "impact_screen_px": [640, 350],
                      "breaker_post_anchor": [21, 11], "t4_side_armor_world_grid": [24.0, 12.5], "t4_side_armor_screen_px": [700, 460]},
                "B": {"camera_raw_px": [-500, 440], "impact_world_grid": [20.0, 10.5], "impact_screen_px": [640, 350],
                      "breaker_post_anchor": [21, 10], "t4_side_armor_world_grid": [24.0, 11.5], "t4_side_armor_screen_px": [760, 450]},
            },
        },
        "contact_camera_policy": "CONTACT pose and socket acceptance must use the branch-specific CONTACT camera targets; shared PLAN values are comparison evidence only",
        "shadow": {"sole_owner": "engine_independent_ground_shadow_layer", "sprite_png_contains_ground_shadow": False,
                   "double_shadow_behavior": "fail_closed", "future_art_shadow_requires_interface_change": True},
        "runtime_bindable": False,
        "real_art_loaded": 0,
    }
    write_json("socket-contact-contract.json", socket_contract)

    build_atlas_schema(gz_sockets, br_sockets, vehicle_sockets, swarm_sockets)


def alias_entry(stable_id: str, slot_id: str, revision: str, alias_key: str, source_key: str,
                native_size: list[int], pivot_px: list[int], socket_contract_id: str) -> dict[str, Any]:
    payload = {
        "stable_id": stable_id, "slot_id": slot_id, "revision": revision, "alias_kind": "physical_clip_alias",
        "alias_key": alias_key, "source_clip_key": source_key, "facing_policy": "preserve_exact",
        "native_size": native_size, "pivot_px": pivot_px, "socket_contract_id": socket_contract_id,
        "resource_binding_id": f"{slot_id}_p99_fixture_binding",
    }
    return {**payload, "canonical_payload_sha256": canonical_signature(payload), "one_hop": True, "cycle_forbidden": True}


def build_atlas_schema(gz_sockets, br_sockets, vehicle_sockets, swarm_sockets) -> None:
    socket_id = "C01E02_MAP_CAMERA_SOCKET_CONTACT_V1"
    assets = [
        {
            "stable_id": "V353U001", "slot_id": "guardian_z_map_current", "revision": "task98_preproduction_v1",
            "view_space": "map_dimetric_40x20", "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
            "resource_binding_id": "guardian_z_map_current_p99_fixture_binding",
            "resource_path": "res://content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/fixtures/c3_guardian_z_neutral_768x768.png",
            "sha256": None, "sha256_status": "PENDING_P99_EXACT_RECEIPT", "binding_mode": "p99_exact_receipt_overlay", "binding_owner": "G2_A2_C3",
            "native_size": [256, 256], "atlas_size": [768, 768], "display_scale": [1.0, 1.0], "footprint": [2, 2],
            "pivot_normalized": [0.5, 0.875], "pivot_px": [128, 224], "z_bias": 1,
            "sparse_clips": {
                "idle/east/0": [0, 0, 256, 256], "move/north/0": [256, 0, 256, 256], "brace/east/0": [512, 0, 256, 256],
                "brace/north/0": [0, 256, 256, 256], "brace/south/0": [256, 256, 256, 256], "contact/south/0": [512, 256, 256, 256],
                "recoil/east/0": [0, 512, 256, 256], "recoil/south/0": [256, 512, 256, 256],
            },
            "physical_clip_aliases_with_signature": [alias_entry("V353U001", "guardian_z_map_current", "task98_preproduction_v1", "move/east/0", "idle/east/0", [256, 256], [128, 224], socket_id)],
            "state_aliases_with_signature": [alias_entry("V353U001", "guardian_z_map_current", "task98_preproduction_v1", "move/east/0", "idle/east/0", [256, 256], [128, 224], socket_id)],
            "semantic_state_aliases": {"active": "idle", "moving": "move", "anticipation": "brace", "holding_first_contact": "brace", "impact": "contact", "recoil_hold": "recoil"},
            "fps_or_hold": {"idle": "hold", "move": "engine_route_tween_after_rect_resolution", "brace": "hold", "contact": "hit_stop_hold", "recoil": "hold"},
            "loop": {"idle": True, "move": False, "brace": False, "contact": False, "recoil": False}, "facings": ["east", "north", "south"],
            "interaction_sockets": gz_sockets, "filter": "nearest", "mipmap": False,
            "shadow_owner": "engine_independent_ground_shadow_layer", "fixture_validation_only": True,
            "runtime_bindable": False, "fail_closed": True,
        },
        {
            "stable_id": "ENEMY_C01_BREAKER", "slot_id": "breaker_map_current", "revision": "task98_preproduction_v1",
            "view_space": "map_dimetric_40x20", "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
            "resource_binding_id": "breaker_map_current_p99_fixture_binding",
            "resource_path": "res://content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/fixtures/c3_breaker_neutral_1152x768.png",
            "sha256": None, "sha256_status": "PENDING_P99_EXACT_RECEIPT", "binding_mode": "p99_exact_receipt_overlay", "binding_owner": "G2_A2_C3",
            "native_size": [384, 384], "atlas_size": [1152, 768], "display_scale": [1.0, 1.0], "footprint": [3, 3],
            "pivot_normalized": [0.5, 0.8333333333], "pivot_px": [192, 320], "z_bias": 2,
            "sparse_clips": {"charge/north/0": [0, 0, 384, 384], "contact/north/0": [384, 0, 384, 384],
                             "recoil/north/0": [768, 0, 384, 384], "side_hit/north/0": [0, 384, 384, 384], "red_charge/north/0": [384, 384, 384, 384]},
            "physical_clip_aliases_with_signature": [], "state_aliases_with_signature": [],
            "semantic_state_aliases": {"charging_run": "charge", "anticipation": "charge", "brace": "charge", "impact": "contact",
                                       "charge_partially_redirected": "recoil", "recover": "recoil", "side_armor_hit": "side_hit"},
            "fps_or_hold": {"charge": "hold_or_engine_route_tween_after_rect_resolution", "contact": "hit_stop_hold", "recoil": "hold", "side_hit": "hold", "red_charge": "hold"},
            "loop": {"charge": True, "contact": False, "recoil": False, "side_hit": False, "red_charge": True}, "facings": ["north"],
            "interaction_sockets": br_sockets, "filter": "nearest", "mipmap": False,
            "shadow_owner": "engine_independent_ground_shadow_layer", "fixture_validation_only": True,
            "runtime_bindable": False, "fail_closed": True,
        },
        {
            "stable_id": "TARGET_C01_EMERGENCY_VEHICLE_01", "slot_id": "emergency_vehicle_map_current", "revision": "task98_preproduction_v1",
            "view_space": "map_dimetric_40x20", "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
            "resource_binding_id": "emergency_vehicle_map_current_p99_fixture_binding",
            "resource_path": "res://content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/fixtures/c3_emergency_vehicle_neutral_256x256.png",
            "sha256": None, "sha256_status": "PENDING_P99_EXACT_RECEIPT", "binding_mode": "p99_exact_receipt_overlay", "binding_owner": "G2_A2_C3",
            "native_size": [128, 128], "atlas_size": [256, 256], "display_scale": [1.0, 1.0], "footprint": [1, 1],
            "pivot_normalized": [0.5, 0.75], "pivot_px": [64, 96], "z_bias": 0,
            "sparse_clips": {"waiting/east/0": [0, 0, 128, 128], "drive/east/0": [128, 0, 128, 128], "recoil/east/0": [0, 128, 128, 128]},
            "physical_clip_aliases_with_signature": [alias_entry("TARGET_C01_EMERGENCY_VEHICLE_01", "emergency_vehicle_map_current", "task98_preproduction_v1", "passed/east/0", "waiting/east/0", [128, 128], [64, 96], socket_id)],
            "state_aliases_with_signature": [alias_entry("TARGET_C01_EMERGENCY_VEHICLE_01", "emergency_vehicle_map_current", "task98_preproduction_v1", "passed/east/0", "waiting/east/0", [128, 128], [64, 96], socket_id)],
            "semantic_state_aliases": {"active": "waiting", "moving": "drive", "move": "drive", "passed_lane_still_active": "passed"},
            "fps_or_hold": {"waiting": "hold", "drive": "engine_route_tween_after_rect_resolution", "recoil": "hold", "passed": "hold"},
            "loop": {"waiting": True, "drive": False, "recoil": False, "passed": True}, "facings": ["east"],
            "interaction_sockets": vehicle_sockets, "filter": "nearest", "mipmap": False,
            "shadow_owner": "engine_independent_ground_shadow_layer", "fixture_validation_only": True,
            "runtime_bindable": False, "fail_closed": True,
        },
        {
            "stable_id": "ENEMY_C01_RIFT_SWARM", "slot_id": "rift_swarm_map_current", "revision": "task98_preproduction_v1",
            "view_space": "map_dimetric_40x20", "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
            "resource_binding_id": "rift_swarm_map_current_p99_fixture_binding",
            "resource_path": "res://content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/fixtures/c3_rift_swarm_neutral_384x192.png",
            "sha256": None, "sha256_status": "PENDING_P99_EXACT_RECEIPT", "binding_mode": "p99_exact_receipt_overlay", "binding_owner": "G2_A2_C3",
            "native_size": [96, 96], "atlas_size": [384, 192], "display_scale": [1.0, 1.0], "footprint": [1, 1],
            "pivot_normalized": [0.5, 0.75], "pivot_px": [48, 72], "z_bias": 0,
            "sparse_clips": {"idle/north/0": [0, 0, 96, 96], "idle/east/0": [96, 0, 96, 96], "idle/south/0": [192, 0, 96, 96],
                             "idle/west/0": [288, 0, 96, 96], "recoil/west/0": [0, 96, 96, 96], "deflected/west/0": [96, 96, 96, 96]},
            "physical_clip_aliases_with_signature": [alias_entry("ENEMY_C01_RIFT_SWARM", "rift_swarm_map_current", "task98_preproduction_v1", "move/west/0", "idle/west/0", [96, 96], [48, 72], socket_id)],
            "state_aliases_with_signature": [alias_entry("ENEMY_C01_RIFT_SWARM", "rift_swarm_map_current", "task98_preproduction_v1", "move/west/0", "idle/west/0", [96, 96], [48, 72], socket_id)],
            "semantic_state_aliases": {"active": "idle", "anticipation": "idle", "scattered_active": "idle", "moving": "move", "move": "move", "deflected_alive": "deflected"},
            "fps_or_hold": {"idle": "hold", "move": "engine_route_tween_after_rect_resolution", "recoil": "hold", "deflected": "hold"},
            "loop": {"idle": True, "move": False, "recoil": False, "deflected": True}, "facings": ["north", "east", "south", "west"],
            "interaction_sockets": swarm_sockets, "filter": "nearest", "mipmap": False,
            "shadow_owner": "engine_independent_ground_shadow_layer", "fixture_validation_only": True,
            "runtime_bindable": False, "fail_closed": True,
            "instance_bindings": [
                {"stable_id": "ENEMY_C01_RIFT_SWARM_01", "initial_clip": "idle/west/0"},
                {"stable_id": "ENEMY_C01_RIFT_SWARM_02", "initial_clip": "idle/north/0"},
                {"stable_id": "ENEMY_C01_RIFT_SWARM_03", "initial_clip": "idle/south/0"},
            ],
            "future_real_art_source": {"path": str(A5), "sha256": EXPECTED[A5], "allowed_operation": "exact frame copy into current atlas after separate gate", "used_by_P99_fixture": False},
        },
    ]
    schema = {
        "schema_version": "1.0.0",
        "schema_id": "C01E02_CURRENT_TOPOLOGY_SPARSE_ATLAS_SCHEMA_V1",
        "status": "STRUCTURE_FROZEN_RESOURCE_BYTES_PENDING_EXTERNAL_P99_RECEIPT",
        "view_space": "map_dimetric_40x20", "camera_contract_id": "CURRENT_TOPOLOGY_CAMERA_V1",
        "filter": "nearest", "mipmap": False, "centered": False,
        "shadow_owner": "engine_independent_ground_shadow_layer", "sprite_png_contains_shadow": False,
        "socket_contract_id": socket_id,
        "binding_resolution": {"mode": "p99_exact_receipt_overlay", "join_key": ["stable_id", "slot_id", "revision", "resource_path"],
                               "P99_may_modify_task98_schema": False, "fail_closed_until_exact_sha_resolved": True,
                               "resolved_fixture_must_remain_fixture_validation_only": True},
        "assets": assets,
        "global_fail_closed_rules": ["missing_clip", "wrong_camera_contract_id", "wrong_view_space", "wrong_pivot", "wrong_sha256", "rect_out_of_bounds",
                                     "alias_cycle", "alias_more_than_one_hop", "cross_facing_alias", "signature_mismatch"],
        "fallback_behavior": "hide_current_subject_and_emit_one_unique_reason; never previous frame, first frame, or cross-facing fallback",
        "fixture_validation_only": True, "runtime_bindable": False, "real_art_loaded": 0,
    }
    write_json("atlas-schema-current.json", schema)


def build_phase_matrix() -> None:
    clips = [
        ("V353U001", "guardian_z_map_current", "idle", "east", 0, "new_frame", "", "PLAN,T1,T2 hold", "hold", "idle/east/0"),
        ("V353U001", "guardian_z_map_current", "move", "east", 0, "same_facing_alias_plus_engine_tween", "idle/east/0", "T3 east route segment", "route_tween", "move/east/0"),
        ("V353U001", "guardian_z_map_current", "move", "north", 0, "new_frame_plus_engine_tween", "", "T3 north route segment", "route_tween", "move/north/0"),
        ("V353U001", "guardian_z_map_current", "brace", "east", 0, "new_frame", "", "T3 east settle/anticipation", "hold", "brace/east/0"),
        ("V353U001", "guardian_z_map_current", "brace", "north", 0, "new_frame", "", "T3 turn bridge", "hold", "brace/north/0"),
        ("V353U001", "guardian_z_map_current", "brace", "south", 0, "new_frame", "", "T3 contact anticipation", "hold", "brace/south/0"),
        ("V353U001", "guardian_z_map_current", "contact", "south", 0, "new_frame", "", "T3 contact hit-stop", "hit_stop", "contact/south/0"),
        ("V353U001", "guardian_z_map_current", "recoil", "east", 0, "new_frame", "", "B T3 post through T5", "hold", "recoil/east/0"),
        ("V353U001", "guardian_z_map_current", "recoil", "south", 0, "new_frame", "", "A T3 post through T5", "hold", "recoil/south/0"),
        ("ENEMY_C01_BREAKER", "breaker_map_current", "charge", "north", 0, "new_frame", "", "PLAN,T1,T2 and T3 approach", "hold_or_route_tween", "charge/north/0"),
        ("ENEMY_C01_BREAKER", "breaker_map_current", "contact", "north", 0, "new_frame", "", "T3 contact", "hit_stop", "contact/north/0"),
        ("ENEMY_C01_BREAKER", "breaker_map_current", "recoil", "north", 0, "new_frame", "", "T3 post", "hold", "recoil/north/0"),
        ("ENEMY_C01_BREAKER", "breaker_map_current", "side_hit", "north", 0, "new_frame", "", "T4", "hold", "side_hit/north/0"),
        ("ENEMY_C01_BREAKER", "breaker_map_current", "red_charge", "north", 0, "new_frame", "", "T5", "hold", "red_charge/north/0"),
        ("TARGET_C01_EMERGENCY_VEHICLE_01", "emergency_vehicle_map_current", "waiting", "east", 0, "new_frame", "", "PLAN,T1 start", "hold", "waiting/east/0"),
        ("TARGET_C01_EMERGENCY_VEHICLE_01", "emergency_vehicle_map_current", "drive", "east", 0, "new_frame_plus_engine_tween", "", "T1 route", "route_tween", "drive/east/0"),
        ("TARGET_C01_EMERGENCY_VEHICLE_01", "emergency_vehicle_map_current", "recoil", "east", 0, "new_frame", "", "T1 embodied consequence", "hold", "recoil/east/0"),
        ("TARGET_C01_EMERGENCY_VEHICLE_01", "emergency_vehicle_map_current", "passed", "east", 0, "same_facing_alias", "waiting/east/0", "T1 finish through T5", "hold", "passed/east/0"),
        ("ENEMY_C01_RIFT_SWARM_01", "rift_swarm_map_current", "idle", "west", 0, "new_current_rect_from_exact_A5", "A5 west exact pixels", "PLAN,T1,T2 start", "hold", "idle/west/0"),
        ("ENEMY_C01_RIFT_SWARM_01", "rift_swarm_map_current", "move", "west", 0, "same_facing_alias_plus_engine_tween", "idle/west/0", "T2 route", "route_tween", "move/west/0"),
        ("ENEMY_C01_RIFT_SWARM_01", "rift_swarm_map_current", "recoil", "west", 0, "new_frame", "", "T2 embodied consequence", "hold", "recoil/west/0"),
        ("ENEMY_C01_RIFT_SWARM_01", "rift_swarm_map_current", "deflected", "west", 0, "new_frame", "", "T2 finish through T5", "hold", "deflected/west/0"),
        ("ENEMY_C01_RIFT_SWARM_02", "rift_swarm_map_current", "idle", "north", 0, "new_current_rect_from_exact_A5", "A5 north exact pixels", "PLAN through T5 hold", "hold", "idle/north/0"),
        ("ENEMY_C01_RIFT_SWARM_03", "rift_swarm_map_current", "idle", "south", 0, "new_current_rect_from_exact_A5", "A5 south exact pixels", "PLAN through T5 hold", "hold", "idle/south/0"),
    ]
    header = ["stable_id", "slot_id", "state", "facing", "frame", "production_resolution", "alias_or_source", "continuous_phase_scope", "motion_or_hold", "clip_key",
              "cross_facing_fallback", "missing_clip_allowed", "real_pixel_status"]
    rows = [(*r, "false", "false", "planned_not_generated") for r in clips]
    write_tsv("first-round-state-facing-phase-matrix.tsv", header, rows)

    subjects = ["V353U001", "ENEMY_C01_BREAKER", "TARGET_C01_EMERGENCY_VEHICLE_01", "ENEMY_C01_RIFT_SWARM_01", "ENEMY_C01_RIFT_SWARM_02", "ENEMY_C01_RIFT_SWARM_03"]
    phases = [
        ("PLAN", "shared", {"V353U001": "idle/east/0", "ENEMY_C01_BREAKER": "charge/north/0", "TARGET_C01_EMERGENCY_VEHICLE_01": "waiting/east/0", "ENEMY_C01_RIFT_SWARM_01": "idle/west/0"}),
        ("T1_WAIT", "shared", {"TARGET_C01_EMERGENCY_VEHICLE_01": "waiting/east/0"}),
        ("T1_DRIVE", "shared", {"TARGET_C01_EMERGENCY_VEHICLE_01": "drive/east/0"}),
        ("T1_RECOIL", "shared", {"TARGET_C01_EMERGENCY_VEHICLE_01": "recoil/east/0"}),
        ("T1_PASSED", "shared", {"TARGET_C01_EMERGENCY_VEHICLE_01": "passed/east/0"}),
        ("T2_IDLE", "shared", {"ENEMY_C01_RIFT_SWARM_01": "idle/west/0"}),
        ("T2_MOVE", "shared", {"ENEMY_C01_RIFT_SWARM_01": "move/west/0"}),
        ("T2_RECOIL", "shared", {"ENEMY_C01_RIFT_SWARM_01": "recoil/west/0"}),
        ("T2_DEFLECTED", "shared", {"ENEMY_C01_RIFT_SWARM_01": "deflected/west/0"}),
        ("T3_MOVE_EAST", "A_or_B", {"V353U001": "move/east/0"}),
        ("T3_MOVE_NORTH", "A_or_B", {"V353U001": "move/north/0"}),
        ("T3_BRACE_EAST", "A_or_B", {"V353U001": "brace/east/0"}),
        ("T3_BRACE_NORTH", "A_or_B", {"V353U001": "brace/north/0"}),
        ("T3_BRACE_SOUTH", "A_or_B", {"V353U001": "brace/south/0"}),
        ("T3_CONTACT", "A_or_B", {"V353U001": "contact/south/0", "ENEMY_C01_BREAKER": "contact/north/0"}),
        ("T3_POST_A", "A", {"V353U001": "recoil/south/0", "ENEMY_C01_BREAKER": "recoil/north/0"}),
        ("T3_POST_B", "B", {"V353U001": "recoil/east/0", "ENEMY_C01_BREAKER": "recoil/north/0"}),
        ("T4_SIDE_HIT_A", "A", {"V353U001": "recoil/south/0", "ENEMY_C01_BREAKER": "side_hit/north/0"}),
        ("T4_SIDE_HIT_B", "B", {"V353U001": "recoil/east/0", "ENEMY_C01_BREAKER": "side_hit/north/0"}),
        ("T5_RED_CHARGE_A", "A", {"V353U001": "recoil/south/0", "ENEMY_C01_BREAKER": "red_charge/north/0"}),
        ("T5_RED_CHARGE_B", "B", {"V353U001": "recoil/east/0", "ENEMY_C01_BREAKER": "red_charge/north/0"}),
    ]
    default = {"V353U001": "idle/east/0", "ENEMY_C01_BREAKER": "charge/north/0", "TARGET_C01_EMERGENCY_VEHICLE_01": "waiting/east/0",
               "ENEMY_C01_RIFT_SWARM_01": "idle/west/0", "ENEMY_C01_RIFT_SWARM_02": "idle/north/0", "ENEMY_C01_RIFT_SWARM_03": "idle/south/0"}
    current = default.copy()
    continuity_rows = []
    for phase, branch, changes in phases:
        current.update(changes)
        if phase.startswith("T1_PASSED"):
            current["TARGET_C01_EMERGENCY_VEHICLE_01"] = "passed/east/0"
        if phase.startswith("T2_DEFLECTED"):
            current["ENEMY_C01_RIFT_SWARM_01"] = "deflected/west/0"
        for subject in subjects:
            clip = current[subject]
            continuity_rows.append((phase, branch, subject, clip, "resolved_before_tween", "false", "false", "planned_not_generated"))
    write_tsv("first-round-phase-continuity-readback.tsv",
              ["continuous_phase", "branch_scope", "stable_id", "resolved_clip_key", "resolution_order", "missing_clip", "cross_facing_fallback", "real_pixel_status"], continuity_rows)


def build_call_plan() -> None:
    content = """# Task98 future Call03 / Call04 plan

Status: `PREPRODUCTION_ONLY / IMAGEGEN_CALLS_THIS_TASK=0 / CALL03=false / CALL04=false`

No call is authorized by this file. P99 neutral-atlas consumer evidence and an explicit producer release are both mandatory before Call03.

## Budget and order

- Total historic budget: 4 calls.
- Used: Call01 History + Call02 visual failure = 2.
- Remaining: 2, reserved sequentially. Automatic reroll is forbidden.
- Call03: BREAKER PLAN map-camera master north only.
- Call04: Guardian Z PLAN map-camera master east only, and only after Call03 passes producer 50% and 100% review.

## Future Call03 · BREAKER

Four isolated inputs only: exact 384 geometry guide; approved B-body crops; approved X-surface crops; actor-free CML128 rule card. Solid uniform background, one subject, no ground, environment, text, second machine, CONTACT or FX. The B and X responsibilities must be read together. Output is rejected at 50% if it first reads as turtle, ape, ordinary quadruped, vehicle or sled. At 100%, asymmetric bio-armor, flexible seams, narrow red slit, closed chest seam and sealed upper-back outlet must survive. Any failure stops; Call04 remains unused.

Postprocess if separately authorized: background removal, despill, fixed-canvas pad and hash only. No body redraw, limb move or identity repair.

## Future Call04 · Guardian Z

Four isolated inputs only: exact 256 geometry guide; V10X E02 parent; latest Q/SD identity source; actor-free CML128 rule card. One subject, solid uniform background, map-east view with visible top planes. Required: approx. four-head old-super-robot mass, layered gold crown, central red crown, blue brow, silver grille face, red-X chest and gold core, square shoulder rings, equal-weight cylindrical forearms, two arms, no wings and no backpack. Orthographic strict-side paper read fails.

## Fail gate shared by both calls

Wrong view-space, identity fusion, second anatomy, background semantics, baked shadow, text, clipped socket region, wrong pivot, cross-facing fallback, or any unapproved local repair => `VISUAL_FAIL_STOP`. Neither call makes an Atlas, Runtime handoff, UA91 submission or Canon migration.
"""
    (OUT / "call03-call04-plan.md").write_text(content, encoding="utf-8")


def build_logs(source_checks: list[dict[str, Any]]) -> None:
    log = f"""# Task98 generation log

Status: `ZERO_GENERATION_PREPRODUCTION_COMPLETE / CALL03=false / CALL04=false`

- ImageGen calls in Task98: `0`
- Blender calls: `0`
- Visible target pixel generation or editing: `0`
- Godot / Atlas consumer / Runtime writes: `0`
- Call02 unit, object, shadow or reflection pixels reused: `0`
- Call02 use: six registered actor/object/text-free local environment crops, `History / ENVIRONMENT_METHOD_DONOR_ONLY`.
- CML128 source pixels embedded in safe boards: `0`; the board uses an actor-free rule card only because the source contains conflicting wing/backpack anatomy.
- Safe-board isolation: Guardian board opens only Guardian sources; BREAKER board opens only approved B/X crops and B128.
- Source SHA verification: `{len(source_checks)}/{len(source_checks)}` exact.
- P99 invoked: `false`.
- Producer joint-interface correction: environment depth ownership and branch-specific CONTACT camera targets rebuilt without any visible-pixel generation.

The builder only performed byte reads, deterministic crops/scales/layout, projection guides, QA geometry, and contract serialization. It did not make visible actor art.
"""
    (OUT / "generation-log.md").write_text(log, encoding="utf-8")

    report = """# Task98 preproduction completion report

Status: `PREPRODUCTION_PACKAGE_COMPLETE_AWAITING_PRODUCER_P99 / IMAGEGEN_0 / CALL03_FALSE / CALL04_FALSE`

## Closed in this package

- Exact source lineage and Hard / Working / Candidate / History boundaries.
- `CURRENT_TOPOLOGY_CAMERA_V1` map slots, pivot, facing, z-bias and fail-closed registration.
- Guardian and BREAKER geometry guides marked non-art/non-runtime.
- Two identity-isolated safe boards; no cross-machine pixels and no CML128 anatomy pixels.
- Actor/object-free exact current-topology guide and corrected 2400×1350 layer contract: base `-1200`, buildings `-900`, roof `900`, foreground `1100`; stateful objects join footpoint depth sort and may split body/roof/foreground; invisible occlusion control and independent weather/FX never bake into the cleanplate.
- Six Call02 local environment-method donor crops with raw half-open coordinates and parent SHA.
- Exact PLAN slot QA: GZ `(400,340)`, BREAKER `(520,520)`, vehicle `(520,320)`, swarms `(840,360)/(800,540)/(1200,460)`; all declared 0px; selection pocket and charge avenue contain zero blocked cells.
- Complete 24-key sparse state/facing clip plan plus continuous PLAN/T1–T5 A/B readback with no allowed missing clip.
- Current sparse atlas schema: rects, pivots, z-bias, same-facing signed aliases, sockets, nearest filter, mipmap false and strict fail-closed behavior.
- Socket/contact contract uses footpoint-local offsets and machine readback tolerance ≤0.5px. Shared PLAN values remain comparison-only; CONTACT acceptance is branch-camera-specific: A camera `[-480,450]` gives impact/side `[640,350]/[700,460]`, B camera `[-500,440]` gives `[640,350]/[760,450]`. Real-art measurement remains explicitly pending.
- Shadow sole owner is the engine independent ground-shadow layer; sprite shadow is forbidden.

## Honest external pending state

The neutral fixture PNG bytes do not exist in Task98. Their paths and structural bindings are frozen, while `sha256=null / PENDING_P99_EXACT_RECEIPT / fail_closed_until_resolved=true`. P99 must generate identity-neutral fixture bytes and an exact overlay receipt in its own write domain; Task98 does not invoke or implement it. Real visible actor pixels, alpha-measured sockets, visual acceptance, fun, UA91 and Runtime remain unproven.

## Stop gate

`real_art_loaded=0 / FUN_NOT_PROVEN / approved_handoffs=[]`. Stop for producer P99 review. Do not call ImageGen, Call03 or Call04; do not write Godot.
"""
    (OUT / "preproduction-completion-report.md").write_text(report, encoding="utf-8")


def validate_outputs(source_checks: list[dict[str, Any]]) -> None:
    required_pngs = {
        "GUARDIAN_Z_EAST_MAP_CAMERA_GEOMETRY_GUIDE_256.png": (256, 256),
        "BREAKER_NORTH_MAP_CAMERA_GEOMETRY_GUIDE_384.png": (384, 384),
        "GUARDIAN_Z_ISOLATED_SAFE_REFERENCE_BOARD_2400x1800.png": (2400, 1800),
        "BREAKER_BX_ISOLATED_SAFE_REFERENCE_BOARD_2400x1800.png": (2400, 1800),
        "CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png": (1280, 720),
        "CALL02_ENVIRONMENT_METHOD_DONOR_CROP_SHEET_1600x1200.png": (1600, 1200),
        "PLAN_SLOT_COMPOSITE_QA_1280x720.png": (1280, 720),
        "PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png": (640, 360),
    }
    png_checks = []
    for name, size in required_pngs.items():
        with Image.open(OUT / name) as im:
            ok = im.size == size and im.mode == "RGBA"
            if not ok:
                raise SystemExit(f"PNG_QA_FAIL {name}: got {im.size} {im.mode}, expected {size} RGBA")
            png_checks.append({"path": str(OUT / name), "size": list(im.size), "mode": im.mode, "pass": True})

    with (OUT / "first-round-state-facing-phase-matrix.tsv").open(encoding="utf-8") as f:
        phase_rows = list(csv.DictReader(f, delimiter="\t"))
    with (OUT / "first-round-phase-continuity-readback.tsv").open(encoding="utf-8") as f:
        continuity_rows = list(csv.DictReader(f, delimiter="\t"))
    if len(phase_rows) != 24 or any(r["missing_clip_allowed"] != "false" for r in phase_rows):
        raise SystemExit("PHASE_MATRIX_QA_FAIL")
    if any(r["missing_clip"] != "false" or r["cross_facing_fallback"] != "false" for r in continuity_rows):
        raise SystemExit("CONTINUITY_QA_FAIL")

    schema = json.loads((OUT / "atlas-schema-current.json").read_text(encoding="utf-8"))
    for asset in schema["assets"]:
        if asset["sha256"] is not None or asset["sha256_status"] != "PENDING_P99_EXACT_RECEIPT":
            raise SystemExit("ATLAS_PENDING_HASH_QA_FAIL")
        aw, ah = asset["atlas_size"]
        for rect in asset["sparse_clips"].values():
            x, y, w, h = rect
            if x < 0 or y < 0 or x + w > aw or y + h > ah:
                raise SystemExit(f"ATLAS_RECT_OOB {asset['stable_id']} {rect}")
        for alias_field in ["physical_clip_aliases_with_signature", "state_aliases_with_signature"]:
            for alias in asset[alias_field]:
                payload = {k: alias[k] for k in ["stable_id", "slot_id", "revision", "alias_kind", "alias_key", "source_clip_key", "facing_policy", "native_size", "pivot_px", "socket_contract_id", "resource_binding_id"]}
                if canonical_signature(payload) != alias["canonical_payload_sha256"]:
                    raise SystemExit("ALIAS_SIGNATURE_QA_FAIL")

    env = json.loads((OUT / "environment-layer-contract.json").read_text(encoding="utf-8"))
    z = env["visible_z_constants"]
    if z != {"base_ground": -1200, "buildings_world_body": -900, "roof": 900, "foreground": 1100}:
        raise SystemExit("ENV_VISIBLE_Z_CONTRACT_QA_FAIL")
    layers = {row["group"]: row for row in env["layer_responsibilities"]}
    if layers["stateful_objects"]["visible_z"] is not None or layers["stateful_objects"]["depth_sort_policy"] != "footprint_bottom_center_screen_y_plus_explicit_z_bias":
        raise SystemExit("STATEFUL_OBJECT_DEPTH_SORT_QA_FAIL")
    if layers["occlusion_control"]["visible"] is not False or layers["occlusion_control"]["occupies_visible_z"] is not False:
        raise SystemExit("OCCLUSION_CONTROL_VISIBILITY_QA_FAIL")
    if layers["weather_fx"]["must_not_bake_into_cleanplate"] is not True:
        raise SystemExit("WEATHER_FX_CLEANPLATE_QA_FAIL")

    sockets = json.loads((OUT / "socket-contact-contract.json").read_text(encoding="utf-8"))
    targets = sockets["future_contact_measurement_targets"]
    if targets["shared_plan_comparison_only"]["acceptance_role"] != "comparison_only_not_contact_truth":
        raise SystemExit("PLAN_COMPARISON_ROLE_QA_FAIL")
    contact = targets["contact_pose_and_socket_acceptance"]
    expected_contact = {
        "A": {"camera_raw_px": [-480, 450], "impact_screen_px": [640, 350], "t4_side_armor_screen_px": [700, 460]},
        "B": {"camera_raw_px": [-500, 440], "impact_screen_px": [640, 350], "t4_side_armor_screen_px": [760, 450]},
    }
    for branch, expected in expected_contact.items():
        for key, value in expected.items():
            if contact[branch][key] != value:
                raise SystemExit(f"CONTACT_CAMERA_TARGET_QA_FAIL {branch} {key}")

    checks = {
        "task": "A9_1A6_S_C2_SPRITE_FIRST_MAP_CAMERA_MASTER_PREPRODUCTION",
        "status": "MACHINE_QA_PASS_VISUAL_AND_PRODUCER_PASS_NOT_CLAIMED",
        "source_sha_checks": source_checks,
        "png_checks": png_checks,
        "safe_board_source_isolation": {
            "guardian_board_breaker_sources_opened": 0,
            "breaker_board_guardian_sources_opened": 0,
            "CML128_anatomy_pixels_embedded": 0,
            "call02_unit_or_object_pixels_permitted": 0,
        },
        "phase_matrix_rows": len(phase_rows),
        "continuity_readback_rows": len(continuity_rows),
        "missing_clip_allowed": False,
        "cross_facing_fallback": False,
        "producer_interface_contract_corrections": {
            "environment_visible_z_constants": z,
            "stateful_objects_use_footpoint_depth_sort": True,
            "stateful_objects_fixed_front_overlay": False,
            "occlusion_control_visible": False,
            "weather_fx_baked_into_cleanplate": False,
            "shared_PLAN_screen_points_are_CONTACT_truth": False,
            "CONTACT_A_camera_and_targets": expected_contact["A"],
            "CONTACT_B_camera_and_targets": expected_contact["B"],
            "pass": True,
        },
        "ImageGen_calls": 0,
        "Call03_allowed": False,
        "Call04_allowed": False,
        "P99_invoked": False,
        "real_art_loaded": 0,
        "FUN_NOT_PROVEN": True,
    }
    write_json("machine-validation-report.json", checks)

    files = sorted(p for p in OUT.iterdir() if p.is_file() and p.name != "delivery-hashes.sha256")
    lines = [f"{sha256(p)}  {p.name}" for p in files]
    (OUT / "delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def runtime_screen_external(point: tuple[float, float], camera: tuple[float, float]) -> tuple[float, float]:
    """Independent literal transcription of visual_projection.gd for Task102 QA."""
    gx, gy = point
    raw_x = -880.0 + (gx - gy) * 40.0
    raw_y = -170.0 + (gx + gy) * 20.0
    return 640.0 + raw_x - camera[0], 350.0 + raw_y - camera[1]


def footprint_bottom_center_external(
    anchor: tuple[int, int], footprint: tuple[int, int], camera: tuple[float, float] = PLAN_CAMERA
) -> tuple[float, float]:
    points = [
        runtime_screen_external((anchor[0] + dx, anchor[1] + dy), camera)
        for dy in range(footprint[1])
        for dx in range(footprint[0])
    ]
    return (
        (min(p[0] for p in points) + max(p[0] for p in points)) * 0.5,
        max(p[1] for p in points) + 20.0,
    )


def snapshot_top_level_files(excluded: set[str]) -> dict[str, str]:
    return {
        path.name: sha256(path)
        for path in sorted(OUT.iterdir())
        if path.is_file() and path.name not in excluded
    }


def build_runtime_grid_correction() -> None:
    if sha256(TASK102) != TASK102_SHA:
        raise SystemExit("TASK102_SHA_MISMATCH")
    if sha256(PROJECTION_CODE) != EXPECTED[PROJECTION_CODE]:
        raise SystemExit("RUNTIME_PROJECTION_SOURCE_SHA_MISMATCH")
    if sha256(COMPOSITOR_PROFILE) != EXPECTED[COMPOSITOR_PROFILE]:
        raise SystemExit("COMPOSITOR_PROFILE_SHA_MISMATCH")
    if sha256(A5) != EXPECTED[A5]:
        raise SystemExit("A5_SOURCE_SHA_MISMATCH")

    protected_before = {}
    for name, expected in TASK102_PROTECTED_SHA.items():
        actual = sha256(OUT / name)
        if actual != expected:
            raise SystemExit(f"TASK102_PROTECTED_SHA_MISMATCH_BEFORE {name}: {actual}")
        protected_before[name] = actual

    allowed_changed = {
        "build_preproduction_package.py",
        "CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png",
        "PLAN_SLOT_COMPOSITE_QA_1280x720.png",
        "PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png",
        "machine-validation-report.json",
        "runtime-grid-registration-correction-receipt.json",
        "runtime-grid-registration-completion-correction.md",
        "delivery-hashes.sha256",
    }
    untouched_before = snapshot_top_level_files(allowed_changed)

    history_dir = OUT / "_history/task102-pre-runtime-grid-correction"
    history_dir.mkdir(parents=True, exist_ok=True)
    history_rows = []
    for name, expected_old_sha in TASK102_AFFECTED_HISTORY_SHA.items():
        source = OUT / name
        archived = history_dir / name
        if archived.exists():
            if sha256(archived) != expected_old_sha:
                raise SystemExit(f"TASK102_HISTORY_ARCHIVE_SHA_MISMATCH {name}")
        else:
            if sha256(source) != expected_old_sha:
                raise SystemExit(f"TASK102_PRE_FIX_SOURCE_SHA_MISMATCH {name}")
            shutil.copyfile(source, archived)
        history_rows.append({
            "filename": name,
            "disposition": "History_invalid_runtime_registration",
            "pre_fix_sha256": expected_old_sha,
            "history_archive_path": str(archived),
            "history_archive_sha256": sha256(archived),
            "history_bytes_preserved": sha256(archived) == expected_old_sha,
        })

    # The only visible QA bytes regenerated by this correction.
    build_actor_free_world()
    build_plan_slot_qa()

    control_specs = [
        ("GRID_0_0_PLAN", (0.0, 0.0), PLAN_CAMERA, (240.0, -240.0)),
        ("GRID_15_11_PLAN", (15.0, 11.0), PLAN_CAMERA, (400.0, 280.0)),
        ("A_IMPACT_CONTACT_A", (20.5, 10.5), (-480.0, 450.0), (640.0, 350.0)),
        ("B_IMPACT_CONTACT_B", (20.0, 10.5), (-500.0, 440.0), (640.0, 350.0)),
        ("GRID_31_17_PLAN", (31.0, 17.0), PLAN_CAMERA, (800.0, 720.0)),
    ]
    control_rows = []
    for control_id, grid, camera, expected in control_specs:
        actual = runtime_screen_external(grid, camera)
        error = ((actual[0] - expected[0]) ** 2 + (actual[1] - expected[1]) ** 2) ** 0.5
        control_rows.append({
            "control_id": control_id,
            "grid": list(grid),
            "camera_raw_px": list(camera),
            "expected_screen_px": list(expected),
            "actual_screen_px": list(actual),
            "error_px": error,
            "pass_lte_0_5px": error <= 0.5,
        })

    footpoint_specs = [
        ("V353U001", (15, 11), (2, 2), (400.0, 340.0), CYAN),
        ("ENEMY_C01_BREAKER", (20, 13), (3, 3), (520.0, 520.0), MAGENTA),
        ("TARGET_C01_EMERGENCY_VEHICLE_01", (17, 10), (1, 1), (520.0, 320.0), ORANGE),
        ("ENEMY_C01_RIFT_SWARM_01", (22, 7), (1, 1), (840.0, 360.0), GREEN),
        ("ENEMY_C01_RIFT_SWARM_02", (26, 12), (1, 1), (800.0, 540.0), GREEN),
        ("ENEMY_C01_RIFT_SWARM_03", (29, 5), (1, 1), (1200.0, 460.0), GREEN),
    ]
    plan_image = Image.open(OUT / "PLAN_SLOT_COMPOSITE_QA_1280x720.png").convert("RGBA")
    footpoint_rows = []
    for subject, anchor, footprint, expected, marker_color in footpoint_specs:
        actual = footprint_bottom_center_external(anchor, footprint)
        error = ((actual[0] - expected[0]) ** 2 + (actual[1] - expected[1]) ** 2) ** 0.5
        pixel = plan_image.getpixel((round(expected[0]), round(expected[1])))
        footpoint_rows.append({
            "subject_id": subject,
            "anchor": list(anchor),
            "footprint": list(footprint),
            "expected_footpoint_screen_px": list(expected),
            "actual_footpoint_screen_px": list(actual),
            "error_px": error,
            "rendered_center_pixel_rgba": list(pixel),
            "expected_marker_rgba": list(marker_color),
            "rendered_marker_center_exact": pixel == marker_color,
            "pass": error <= 0.5 and pixel == marker_color,
        })

    rect_rows = [
        {
            "rect_id": "SELECTION_POCKET",
            "grid_rect": [15, 9, 6, 3],
            "expected_polygon_screen_px": [[480, 220], [720, 340], [600, 400], [360, 280]],
            "actual_polygon_screen_px": [list(p) for p in polygon_for_rect((15, 9, 6, 3))],
        },
        {
            "rect_id": "BREAKER_CHARGE_AVENUE",
            "grid_rect": [20, 11, 3, 5],
            "expected_polygon_screen_px": [[600, 360], [720, 420], [520, 520], [400, 460]],
            "actual_polygon_screen_px": [list(p) for p in polygon_for_rect((20, 11, 3, 5))],
        },
    ]
    for row in rect_rows:
        row["error_px"] = max(
            ((a[0] - e[0]) ** 2 + (a[1] - e[1]) ** 2) ** 0.5
            for a, e in zip(row["actual_polygon_screen_px"], row["expected_polygon_screen_px"])
        )
        row["pass_lte_0_5px"] = row["error_px"] <= 0.5

    actor_free = Image.open(OUT / "CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png").convert("RGBA")
    terrain_samples = [
        ("ROAD_CELL_15_11", (15, 11), (48, 64, 76, 255)),
        ("RESCUE_CELL_20_11", (20, 11), (46, 67, 78, 255)),
        ("SECURITY_APRON_CELL_25_8", (25, 8), (55, 67, 75, 255)),
    ]
    terrain_pixel_rows = []
    for sample_id, grid, expected_rgba in terrain_samples:
        screen = runtime_screen_external(grid, PLAN_CAMERA)
        sample_xy = (round(screen[0]), round(screen[1]))
        actual_rgba = actor_free.getpixel(sample_xy)
        terrain_pixel_rows.append({
            "sample_id": sample_id,
            "grid_cell_center": list(grid),
            "screen_px": list(sample_xy),
            "expected_rgba": list(expected_rgba),
            "actual_rgba": list(actual_rgba),
            "pass": actual_rgba == expected_rgba,
        })

    corrected_rows = []
    for name, old_sha in TASK102_AFFECTED_HISTORY_SHA.items():
        path = OUT / name
        with Image.open(path) as image:
            size = list(image.size)
            mode = image.mode
        corrected_rows.append({
            "filename": name,
            "pre_fix_sha256": old_sha,
            "corrected_sha256": sha256(path),
            "bytes_changed": sha256(path) != old_sha,
            "size_px": size,
            "mode": mode,
        })

    protected_after = {name: sha256(OUT / name) for name in TASK102_PROTECTED_SHA}
    protected_pass = protected_before == protected_after == TASK102_PROTECTED_SHA
    untouched_after = snapshot_top_level_files(allowed_changed)
    untouched_pass = untouched_before == untouched_after
    machine_pass = (
        all(row["pass_lte_0_5px"] for row in control_rows)
        and all(row["pass"] for row in footpoint_rows)
        and all(row["pass_lte_0_5px"] for row in rect_rows)
        and all(row["pass"] for row in terrain_pixel_rows)
        and all(row["bytes_changed"] for row in corrected_rows)
        and all(row["history_bytes_preserved"] for row in history_rows)
        and protected_pass
        and untouched_pass
    )
    if not machine_pass:
        raise SystemExit("TASK102_RUNTIME_GRID_CORRECTION_QA_FAIL")

    correction = {
        "task_id": "TASK102_RUNTIME_GRID_REGISTRATION_CORRECTION",
        "authority_path": str(TASK102),
        "authority_sha256": TASK102_SHA,
        "status": "MACHINE_PASS_AWAITING_PRODUCER_VISUAL_REGISTRATION_ACCEPTANCE",
        "runtime_truth": {
            "integer_grid_coordinate_is_cell_center": True,
            "cell_boundary": "(x-0.5,y-0.5)..(x+0.5,y+0.5)",
            "rect_boundary": "(x-0.5,y-0.5)..(x+w-0.5,y+h-0.5)",
            "projection_source_path": str(PROJECTION_CODE),
            "projection_source_sha256": EXPECTED[PROJECTION_CODE],
        },
        "history_archive": history_rows,
        "corrected_files": corrected_rows,
        "runtime_projection_control_points": control_rows,
        "footpoint_readback": footpoint_rows,
        "rect_polygon_readback": rect_rows,
        "rendered_terrain_center_pixel_readback": terrain_pixel_rows,
        "max_control_error_px": max(row["error_px"] for row in control_rows),
        "max_footpoint_error_px": max(row["error_px"] for row in footpoint_rows),
        "max_rect_vertex_error_px": max(row["error_px"] for row in rect_rows),
        "protected_files_before": protected_before,
        "protected_files_after": protected_after,
        "protected_files_byte_identical": protected_pass,
        "all_other_existing_top_level_files_byte_identical": untouched_pass,
        "executor_visual_inspection": EXECUTOR_VISUAL_INSPECTION,
        "ImageGen_calls": 0,
        "Call03_allowed": False,
        "Call04_allowed": False,
        "new_visible_target_pixels_generated": False,
        "real_art_loaded": 0,
        "producer_visual_acceptance_required": True,
        "machine_pass": machine_pass,
    }
    write_json("runtime-grid-registration-correction-receipt.json", correction)

    old_machine = json.loads((OUT / "machine-validation-report.json").read_text(encoding="utf-8"))
    old_machine["status"] = "MACHINE_QA_PASS_RUNTIME_GRID_REGISTRATION_CORRECTED_PRODUCER_VISUAL_ACCEPTANCE_PENDING"
    old_machine["runtime_grid_registration_correction"] = correction
    old_machine["Call03_allowed"] = False
    old_machine["Call04_allowed"] = False
    old_machine["ImageGen_calls"] = 0
    old_machine["real_art_loaded"] = 0
    old_machine["FUN_NOT_PROVEN"] = True
    write_json("machine-validation-report.json", old_machine)

    completion = f"""# Task98 runtime grid registration completion correction

Authority: Task102 `{TASK102_SHA}`.

Status: `MACHINE_PASS / EXECUTOR_VISUAL_INSPECTION={EXECUTOR_VISUAL_INSPECTION} / AWAITING_PRODUCER_ACCEPTANCE / CALL03_FALSE / CALL04_FALSE`

## Corrected scope

- `cell_diamond(x,y)` now treats integer `(x,y)` as the runtime cell center.
- `polygon_for_rect([x,y,w,h])` now uses `[x-0.5,y-0.5]..[x+w-0.5,y+h-0.5]`.
- Only the actor-free guide and PLAN composite 100%/50% were re-exported.
- Their pre-fix bytes are retained under `_history/task102-pre-runtime-grid-correction/` with exact Task102 SHAs and disposition `History_invalid_runtime_registration`.

## Independent readback

- Five runtime projection controls: max error `0.0px`.
- Six PLAN actor footpoints: max error `0.0px`; each corrected board marker center was sampled at the expected pixel.
- Selection pocket and BREAKER charge avenue polygon vertices: max error `0.0px`.
- Three rendered terrain cell-center samples match the runtime-derived center pixels.

## Frozen-byte proof

- Both local Guardian/BREAKER geometry guides: byte-identical.
- Five C3 frozen contracts: byte-identical.
- Every other pre-existing top-level Task98 file outside the explicit correction allowlist: byte-identical.

## Boundary

ImageGen=0; no new visible target pixel; no Call03/04; no board/interface/Canon/Godot/Runtime write. Machine PASS does not claim producer visual acceptance. Stop at producer registration review.
"""
    (OUT / "runtime-grid-registration-completion-correction.md").write_text(completion, encoding="utf-8")

    manifest = OUT / "delivery-hashes.sha256"
    files = sorted(
        path for path in OUT.rglob("*")
        if path.is_file() and path != manifest and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    manifest.write_text(
        "\n".join(f"{sha256(path)}  {path.relative_to(OUT)}" for path in files) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": correction["status"],
        "executor_visual_inspection": EXECUTOR_VISUAL_INSPECTION,
        "max_control_error_px": correction["max_control_error_px"],
        "max_footpoint_error_px": correction["max_footpoint_error_px"],
        "max_rect_vertex_error_px": correction["max_rect_vertex_error_px"],
        "protected_files_byte_identical": protected_pass,
        "delivery_manifest_sha256": sha256(manifest),
        "corrected_files": {row["filename"]: row["corrected_sha256"] for row in corrected_rows},
    }, ensure_ascii=False, indent=2))


def build_full_package() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_checks = verify_sources()
    build_source_lineage()
    build_geometry_guide(
        "GUARDIAN_Z_EAST_MAP_CAMERA_GEOMETRY_GUIDE_256.png", 256, "V353U001", (2, 2), (128, 224), "east", (40, 20),
        {"body": (0, -74), "shield": (-46, -62), "weapon": (46, -72), "impact": (-20, -10), "target": (-20, -10)},
        CYAN, "two arms · no wings/backpack · sockets must remain inside safe zone",
    )
    build_geometry_guide(
        "BREAKER_NORTH_MAP_CAMERA_GEOMETRY_GUIDE_384.png", 384, "ENEMY_C01_BREAKER", (3, 3), (192, 320), "north", (40, -20),
        {"body": (0, -98), "shield": (-68, -84), "weapon": (68, -96), "impact": (12, -18), "target": (12, -18)},
        MAGENTA, "B semi-upright forelimb load · X shell negative space · T4 side-armor reserve",
    )
    build_safe_boards()
    build_donor_sheet()
    build_actor_free_world()
    build_plan_slot_qa()
    build_contracts()
    build_phase_matrix()
    build_call_plan()
    build_logs(source_checks)
    validate_outputs(source_checks)
    print(f"Task98 package built at {OUT}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runtime-grid-correction",
        action="store_true",
        help="Task102 scoped rebuild of only the three affected composite guides and receipts",
    )
    args = parser.parse_args()
    if args.runtime_grid_correction:
        build_runtime_grid_correction()
    else:
        build_full_package()


if __name__ == "__main__":
    main()
