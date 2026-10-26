#!/usr/bin/env python3
"""Task 75 §5.1: deterministic, zero-redraw Guardian Z V10X Q reuse preflight.

Visible mecha pixels come only from the exact 330346 front master and the exact
3873 four-direction sheet.  Pillow is used only for byte copy, fixed crop,
transparent pad, one deterministic resize, alpha composition, labels, QA and
hashes.  It does not draw, repair, despill, reconstruct or invent mecha pixels.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / ".git").exists())

FONT_REGULAR = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")
FONT_BOLD = Path("/System/Library/Fonts/STHeiti Medium.ttc")

DISPLAY_SIZE = 256
HALF_SIZE = 128
MAP_ANCHOR = (382, 434)
MAP_FOOTPRINT = "2x2"

FRONT_EXACT_NAME = "GUARDIAN_Z_V10X_Q_SOUTH_SOURCE_EXACT_1024.png"
FOUR_CELL_NAMES = {
    "south_sheet": "GUARDIAN_Z_V10X_Q_SOUTH_SHEET_CROP_640x960.png",
    "west": "GUARDIAN_Z_V10X_Q_WEST_SOURCE_CROP_640x960.png",
    "north": "GUARDIAN_Z_V10X_Q_NORTH_SOURCE_CROP_640x960.png",
    "east": "GUARDIAN_Z_V10X_Q_EAST_SOURCE_CROP_640x960.png",
}
DISPLAY_NAMES = {
    "south": "GUARDIAN_Z_V10X_Q_SOUTH_IDLE_256.png",
    "west": "GUARDIAN_Z_V10X_Q_WEST_IDLE_256.png",
    "north": "GUARDIAN_Z_V10X_Q_NORTH_IDLE_256.png",
    "east": "GUARDIAN_Z_V10X_Q_EAST_IDLE_256.png",
}
HALF_NAMES = {
    key: value.replace("_256.png", "_128_REVIEW.png")
    for key, value in DISPLAY_NAMES.items()
}
REVIEW_NAME = "GZ_V10X_Q_50_100_REVIEW_1920x1080.png"
MAP_NAME = "GZ_V10X_Q_ON_A4_MAP_1280x720.png"


@dataclass(frozen=True)
class Source:
    source_id: str
    relative_path: str
    expected_sha256: str
    authority: str
    allowed_use: str
    forbidden_use: str


SOURCES = (
    Source(
        "TASK75",
        "docs/superpowers/specs/production/c01-current-demo-v1/75-c01e02-guardian-z-v10x-q-lineage-recovery-and-asset-governance-correction.md",
        "aa5cded0c1c67c797e6655e268d7d7e4d329c21a39b67b0778ad3d46716906ff",
        "current producer correction",
        "sole scope and zero-redraw gate",
        "redesign;Runtime;Atlas;UA91 promotion",
    ),
    Source(
        "LINEAGE",
        "docs/superpowers/specs/production/c01-current-demo-v1/c01e02-current-production-asset-lineage.tsv",
        "e71ecf6246c4ed95548f3b00bdb44a3476b26b6c9341e2c1fbdc01f176e7f2ad",
        "current asset lineage entry",
        "source routing and authority roles",
        "filename or chat-memory source substitution",
    ),
    Source(
        "BOARD38",
        "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv",
        "31635ae18b515bfb60d32aa3d68779e06b130d5410a493a81b354b6ffec1148e",
        "current production board",
        "Candidate boundary and dispatched preflight",
        "visual PASS;Runtime;downstream advancement",
    ),
    Source(
        "GZ_CML008_HARD",
        ".superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png",
        "a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521",
        "Hard identity calibration anchor",
        "identity cross-check only",
        "map sprite pixels or Candidate overwrite",
    ),
    Source(
        "GZ_V10X_E02_PARENT",
        "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png",
        "e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade",
        "Candidate scoped E02 design parent",
        "lineage verification",
        "Hard promotion;Runtime;pixel replacement",
    ),
    Source(
        "GZ_V10X_Q_SOURCE_V2",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_imagegen_v2.png",
        "c701f3efa72301720117bae08b1479d704315c5a4de62034bf385263ea57f412",
        "Candidate latest same-sheet Q source",
        "lineage verification only in this preflight",
        "new extraction route;redraw;Runtime",
    ),
    Source(
        "GZ_V10X_Q_RGBA_V2",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_rgba.png",
        "2afe2ff0ed254096cf6820cdfbc97e7e3cea5eace85e24187fc58f79168726c4",
        "Candidate transparent intermediate",
        "lineage verification only in this preflight",
        "visible repair;Runtime;Atlas",
    ),
    Source(
        "GZ_V10X_Q_FRONT",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_MASTER_FRONT_RGBA_1024.png",
        "3303465975ccc726dc3ee4088c57e71cf6e1dfa0fd64a1241f57e48ea4d8da24",
        "Candidate current front review master",
        "exact byte copy;display-scale reuse preflight",
        "redraw;despill;Runtime;Atlas;exact handoff",
    ),
    Source(
        "GZ_V10X_Q_FOUR",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png",
        "3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9",
        "Candidate current four-direction review source",
        "fixed 640x960 cells;transparent pad;display-scale reuse preflight",
        "independent direction redraw;repair;Runtime;Atlas;exact handoff",
    ),
    Source(
        "GZ_C128_CONSTRAINT",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png",
        "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e",
        "Candidate approved proportion/action/pivot constraint",
        "2x2 proportion and bottom-center registration cross-check",
        "visible pixel master;exact mask;Runtime",
    ),
    Source(
        "GOLDEN_TURN_SEMANTICS",
        "docs/superpowers/specs/production/c01-current-demo-v1/58-c01e02-g2-golden-slice-ui-gamefeel-objective.md",
        "dfaa9fdf6914abe3dd11eac274921fa0c020c70545d566713bc93fc937ae6643",
        "Candidate production semantics",
        "gap-matrix motion and impact requirements only",
        "Godot implementation;visual approval",
    ),
    Source(
        "A4_VIEWPORT",
        "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_central_1280x720.png",
        "b8ccc9b6eefb802b929a6d674e668611c6d9a88e123e24a2991710ae7e5f4ea9",
        "Candidate map review context",
        "actual display-scale placement board",
        "event staging;map repaint;Runtime",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def validate_sources() -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for source in SOURCES:
        path = ROOT / source.relative_path
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = sha256(path)
        if actual != source.expected_sha256:
            raise RuntimeError(
                f"SOURCE_HASH_MISMATCH {source.source_id}: "
                f"expected={source.expected_sha256} actual={actual}"
            )
        resolved[source.source_id] = path
    return resolved


def fixed_sheet_cells(sheet: Image.Image) -> dict[str, Image.Image]:
    if sheet.mode != "RGBA" or sheet.size != (2560, 960):
        raise RuntimeError(f"Unexpected four-direction source: {sheet.mode} {sheet.size}")
    order = ("south_sheet", "west", "north", "east")
    return {
        name: sheet.crop((index * 640, 0, (index + 1) * 640, 960))
        for index, name in enumerate(order)
    }


def pad_cell_to_square(cell: Image.Image) -> Image.Image:
    if cell.size != (640, 960):
        raise RuntimeError(f"Unexpected fixed cell: {cell.size}")
    padded = Image.new("RGBA", (960, 960), (0, 0, 0, 0))
    padded.alpha_composite(cell, (160, 0))
    return padded


def resize_once(image: Image.Image, size: int) -> Image.Image:
    return image.resize((size, size), Image.Resampling.LANCZOS)


def half_up_scaled(value: int, numerator: int, denominator: int) -> int:
    return (value * numerator + denominator // 2) // denominator


def checker(size: tuple[int, int], cell: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, (21, 32, 40, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle(
                    (x, y, min(size[0] - 1, x + cell - 1), min(size[1] - 1, y + cell - 1)),
                    fill=(30, 43, 52, 255),
                )
    return image


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("Empty alpha image")
    return bbox


def alpha_nonzero(image: Image.Image) -> int:
    return sum(1 for value in image.getchannel("A").getdata() if value)


def binary_alpha_iou(first: Image.Image, second: Image.Image) -> float:
    first_mask = first.getchannel("A").point(lambda value: 255 if value else 0)
    second_mask = second.getchannel("A").point(lambda value: 255 if value else 0)
    intersection = ImageChops.multiply(first_mask, second_mask)
    union = ImageChops.lighter(first_mask, second_mask)
    intersection_count = sum(intersection.histogram()[1:])
    union_count = sum(union.histogram()[1:])
    return round(intersection_count / union_count, 6) if union_count else 1.0


def write_source_lock(paths: dict[str, Path]) -> None:
    with (HERE / "source-lock.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(
            (
                "source_id",
                "project_relative_path",
                "absolute_path",
                "expected_sha256",
                "actual_sha256",
                "hash_check",
                "authority",
                "allowed_use",
                "forbidden_use",
                "runtime_allowed",
            )
        )
        for source in SOURCES:
            path = paths[source.source_id]
            actual = sha256(path)
            writer.writerow(
                (
                    source.source_id,
                    source.relative_path,
                    str(path),
                    source.expected_sha256,
                    actual,
                    "PASS",
                    source.authority,
                    source.allowed_use,
                    source.forbidden_use,
                    "false",
                )
            )


def write_gap_matrix() -> None:
    rows = (
        ("south_idle", "south", "DIRECT_REUSE", "330346 front master", "existing visible pixels", "none", "usable now for south-facing idle/selection/occupy-line read", "Candidate; producer visual review pending"),
        ("west_idle", "west", "DIRECT_REUSE", "3873 fixed cell 1", "existing visible pixels", "none", "usable now for west-facing idle", "strict-side structural consistency remains a visual risk"),
        ("north_idle", "north", "DIRECT_REUSE", "3873 fixed cell 2", "existing visible pixels", "none", "usable now for north-facing idle", "rear detail may merge at 50 percent"),
        ("east_idle", "east", "DIRECT_REUSE", "3873 fixed cell 3", "existing visible pixels", "none", "usable now for east-facing idle", "strict-side structural consistency remains a visual risk"),
        ("cardinal_turn", "N/E/S/W", "TRANSFORM_OR_FRAME_SWITCH", "four existing idle directions", "no new visible frame", "select nearest existing cardinal; short rotation/scale cue", "usable if Golden Turn does not require a visible in-between turn", "no diagonal or turn-in-between artwork"),
        ("route_move", "N/E/S/W", "CONDITIONAL_GAP", "four existing idle directions", "no step frames", "position tween; limited y-bob/lean; dust/footfall FX", "may cover short map travel only; Golden Turn must judge", "long travel or hero framing would require a separately authorized step keyframe"),
        ("contact_anticipation_brace", "contact-facing", "MISSING_KEYFRAME_CANDIDATE", "none", "no dedicated visible pose", "brief scale/lean; hit-stop lead; ground/debris FX", "not proven sufficient", "first giant contact must not degrade to flat translation plus white flash"),
        ("first_giant_contact", "contact-facing", "MISSING_CRITICAL_KEYFRAME", "none", "no contact silhouette", "camera lead; hit-stop; shake; flash; debris and road-damage FX", "Golden Turn still lacks a dedicated contact/weight pose", "Task58 requires body weight and aftermath, not FX-only substitution"),
        ("recoil_aftermath", "contact-facing", "CONDITIONAL_GAP", "none", "no recoil frame", "short reverse offset/tilt; shake decay; dust/road aftermath FX", "may cover a brief map-scale recoil; producer must judge hold length", "high-focus or long hold needs a separately authorized keyframe"),
        ("damage_flash", "any existing direction", "TRANSFORM_FX", "existing idle direction", "no new visible frame", "shader flash/mask; hit-stop; directional shake", "expressible without new sprite pixels", "does not replace contact/recoil body mechanics"),
        ("shield_block_or_bash", "future", "OUT_OF_CURRENT_GOLDEN_TURN", "none in V10X naked idle chain", "missing", "not evaluated here", "deferred beyond current first-round preflight", "requires separate authorized shield state; must not be inferred"),
        ("rocket_punch_or_arm_loss", "future E03", "OUT_OF_SCOPE_FORBIDDEN", "none", "missing", "none", "not part of C01E02 naked-body Golden Turn", "must not be invented from current Q idle source"),
    )
    with (HERE / "direction-status-gap-matrix.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(
            (
                "state_or_action",
                "direction",
                "inheritance_status",
                "existing_pixel_source",
                "visible_pixel_state",
                "allowed_transform_or_fx_expression",
                "golden_turn_finding",
                "risk_or_stop_note",
            )
        )
        writer.writerows(rows)


def build_review_board(display: dict[str, Image.Image], half: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGBA", (1920, 1080), (7, 17, 24, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 1920, 90), fill=(13, 34, 45, 255))
    draw.text((36, 18), "馆守Z V10X Q · ZERO-REDRAW 50% / 100%", font=font(34, True), fill=(243, 247, 242, 255))
    draw.text((1310, 28), "Candidate · visual gate pending", font=font(21, True), fill=(245, 190, 65, 255))

    names = (("south", "SOUTH / front 330346"), ("west", "WEST / fixed cell"), ("north", "NORTH / fixed cell"), ("east", "EAST / fixed cell"))
    x_positions = (44, 386, 728, 1070)
    for (key, title), x in zip(names, x_positions):
        draw.rounded_rectangle((x, 120, x + 310, 512), radius=10, fill=(11, 27, 36, 255), outline=(65, 118, 140, 255), width=2)
        draw.text((x + 18, 138), title, font=font(18, True), fill=(223, 235, 235, 255))
        field = checker((256, 256), 16)
        field.alpha_composite(display[key], (0, 0))
        board.alpha_composite(field, (x + 27, 196))
        draw.text((x + 18, 472), "100% · 256 frame · pivot (128,243)", font=font(15), fill=(148, 193, 208, 255))

        draw.rounded_rectangle((x, 552, x + 310, 850), radius=10, fill=(11, 27, 36, 255), outline=(58, 92, 108, 255), width=2)
        draw.text((x + 18, 570), title, font=font(17, True), fill=(210, 224, 225, 255))
        half_field = checker((128, 128), 8)
        half_field.alpha_composite(half[key], (0, 0))
        board.alpha_composite(half_field, (x + 91, 625))
        draw.text((x + 18, 790), "50% · 128 · direct from native", font=font(13), fill=(145, 176, 187, 255))

    draw.rounded_rectangle((1410, 120, 1884, 850), radius=12, fill=(17, 31, 39, 255), outline=(211, 157, 55, 255), width=2)
    draw.text((1440, 148), "SOURCE / RISK READ", font=font(25, True), fill=(245, 199, 92, 255))
    notes = (
        "• south visible bytes: 330346 exact\n"
        "• W/N/E: 3873 fixed 640×960 cells\n"
        "• transparent pad only; one resize\n"
        "• no paint, repair, despill or redraw\n\n"
        "At 100%\n"
        "identity and red-X/gold-core read strongly.\n\n"
        "At 50%\n"
        "soft gradients and fine panel lines compress;\n"
        "dark blue can merge with A4 roofs/road.\n\n"
        "Structure\n"
        "same-sheet lineage is proven; strict side-to-\n"
        "front mechanical equivalence is not a rig proof.\n\n"
        "Machine PASS ≠ visual PASS."
    )
    draw.multiline_text((1440, 204), notes, font=font(19), fill=(213, 224, 224, 255), spacing=10)

    draw.rounded_rectangle((36, 884, 1884, 1046), radius=10, fill=(12, 25, 33, 255), outline=(63, 94, 109, 255), width=2)
    draw.text((60, 904), "ZERO-REDRAW INHERITANCE FINDING", font=font(21, True), fill=(114, 203, 224, 255))
    draw.multiline_text(
        (60, 942),
        "Four cardinal idle views are directly reusable. Golden Turn still lacks a dedicated first-contact weight pose.\n"
        "Movement, flash and brief recoil may be tested with transform/FX, but Task58 rejects flat translation + white flash as final impact presentation.\n"
        "No new visible pixel is authorized by this preflight.",
        font=font(16),
        fill=(224, 231, 230, 255),
        spacing=5,
    )
    return board


def draw_diamond(draw: ImageDraw.ImageDraw, center: tuple[int, int], cells: int) -> None:
    x, y = center
    half_w, half_h = 40 * cells, 20 * cells
    points = ((x, y - half_h), (x + half_w, y), (x, y + half_h), (x - half_w, y))
    draw.polygon(points, fill=(65, 194, 223, 40))
    draw.line((*points, points[0]), fill=(83, 210, 237, 235), width=3, joint="curve")


def build_map_board(map_path: Path, south: Image.Image) -> Image.Image:
    board = Image.open(map_path).convert("RGBA")
    if board.size != (1280, 720):
        raise RuntimeError(f"Unexpected A4 viewport size: {board.size}")

    annotations = Image.new("RGBA", board.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(annotations, "RGBA")
    draw.rectangle((0, 0, 1280, 66), fill=(4, 14, 20, 235))
    draw.rectangle((0, 648, 1280, 720), fill=(4, 14, 20, 240))
    draw.text((24, 14), "V10X Q · A4 ACTUAL DISPLAY-SCALE PREFLIGHT", font=font(25, True), fill=(242, 246, 240, 255))
    draw.text((812, 20), "256 display · Candidate · not event staging", font=font(17, True), fill=(249, 197, 75, 255))
    draw_diamond(draw, MAP_ANCHOR, 2)
    draw.ellipse((MAP_ANCHOR[0] - 4, MAP_ANCHOR[1] - 4, MAP_ANCHOR[0] + 4, MAP_ANCHOR[1] + 4), fill=(83, 210, 237, 255))
    board = Image.alpha_composite(board, annotations)

    pivot = (128, 243)
    board.alpha_composite(south, (MAP_ANCHOR[0] - pivot[0], MAP_ANCHOR[1] - pivot[1]))

    labels = Image.new("RGBA", board.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(labels, "RGBA")
    draw.rounded_rectangle((914, 238, 1258, 348), radius=8, fill=(4, 12, 18, 224), outline=(83, 210, 237, 255), width=2)
    draw.text((932, 253), "馆守Z V10X Q", font=font(20, True), fill=(234, 247, 248, 255))
    draw.text((932, 287), "SOUTH idle · 2×2 · display 256", font=font(15), fill=(165, 222, 233, 255))
    draw.text((932, 316), "bottom-center (128,243)", font=font(15), fill=(165, 222, 233, 255))
    draw.multiline_text(
        (24, 663),
        "Existing 330346 pixels only · prior review anchor (382,434) · scale/readability proof, not spawn/event position.\n"
        "Open risks: dark-blue/map merge and large tactical occlusion. Machine PASS ≠ visual PASS.",
        font=font(14),
        fill=(224, 232, 231, 255),
        spacing=3,
    )
    return Image.alpha_composite(board, labels)


def write_generation_log() -> None:
    text = """# Task 75 §5.1 generation log

Status: `ZERO_REDRAW_PREFLIGHT_BUILT / Candidate / runtime_allowed=false / visual_pass=pending`

## Fixed source route

`V10X e1d6... -> same-sheet Q c701... -> transparent front 330346... / four-direction 3873...`

- South uses a byte-identical copy of the exact 1024×1024 `330346...` front master.
- The exact 2560×960 `3873...` sheet is divided into four fixed cells, without trim or content-aware detection:
  - front/south: `[0,0,640,960]`
  - left/west: `[640,0,1280,960]`
  - back/north: `[1280,0,1920,960]`
  - right/east: `[1920,0,2560,960]`
- Each 640×960 cell is centered in a transparent 960×960 canvas at `(160,0)`. Padding adds no visible pixels.
- Display assets are resized exactly once from the native square canvas to 256×256 with Pillow `LANCZOS`. The 50% review assets are separately resized once from native to 128×128; they are not scaled from the 256 outputs.
- Registration is bottom-center: 256 pivot `(128,243)` and 128 review pivot `(64,121)`. These preserve the source review baselines (`970/1024` for 330346 and `910/960` for 3873).
- The A4 board uses the prior review anchor `(382,434)` and 2×2 footprint only as scale/readability evidence, not event staging or Runtime coordinates.

## Explicit non-actions

- ImageGen 0; Blender 0; SVG 0; Python/Pillow visible-mecha drawing 0.
- No visible-pixel generation, repair, cleanup, despill, recolor, structure correction, frame interpolation or new action pose.
- No BREAKER consumption; no Atlas, Godot, Runtime, UA91, G2-B, exact handoff or Canon migration.

## Risks intentionally retained

- Soft gradients and fine panel lines compress at 50%; dark-blue armor can merge into A4 roofs and road.
- The four views share one sheet/source chain, but they are not a named rig and do not prove exact strict-side/front structural equivalence.
- Existing pixels provide only four cardinal idle views. A first-contact weight pose is absent; transforms and FX may express short movement/flash/recoil, but cannot automatically satisfy Task58's impact requirement.
- Machine source/crop/alpha checks do not grant visual approval.
"""
    (HERE / "generation-log.md").write_text(text, encoding="utf-8")


def write_completion_report(metrics: dict[str, object]) -> None:
    text = f"""# Task 75 §5.1 zero-redraw reuse preflight completion report

Status: `DELIVERED_FOR_PRODUCER_PIXEL_PREFLIGHT / MACHINE_PASS / VISUAL_PASS_PENDING`

## Result

- The exact current V10X Q lineage was consumed; old `60352...`, A8 program sprites, Blender, SVG and R1 pixels were not consumed.
- Four cardinal idle display assets were inherited without repaint: south from `330346...`; west/north/east from fixed `3873...` cells.
- Display scale is 256×256 with bottom-center `(128,243)`; 50% review is 128×128 with bottom-center `(64,121)`.
- A4 placement is review-only at anchor `{MAP_ANCHOR}`, footprint `{MAP_FOOTPRINT}`; it is not a spawn/event/Runtime claim.

## Machine evidence

- `source_lock_pass_all={str(metrics['source_lock_pass_all']).lower()}`
- `fixed_crop_pixel_equal_all={str(metrics['fixed_crop_pixel_equal_all']).lower()}`
- `south_exact_copy={str(metrics['south_exact_copy']).lower()}`
- `output_alpha_present_all={str(metrics['output_alpha_present_all']).lower()}`
- `display_size_all=256x256`
- `machine_pass={str(metrics['machine_pass']).lower()}`
- `south_master_vs_sheet_front_alpha_iou={metrics['structure_risk_metrics']['south_master_vs_sheet_front_alpha_iou']}`
- `west_vs_mirrored_east_alpha_iou={metrics['structure_risk_metrics']['west_vs_mirrored_east_alpha_iou']}`

## Visual and production stop

- Soft-gradient compression, side/front structural consistency, dark-blue map merge and map occlusion remain open producer risks.
- Four idle directions are directly reusable. Dedicated movement, brace/contact and recoil artwork is not present; the first giant-contact weight pose is the clearest Golden Turn keyframe gap.
- Transform/FX can test translation, short lean/bob, flash, hit-stop, shake, debris and brief recoil. This does not prove the final impact presentation.
- No visual PASS, UA91, Atlas, Godot, Runtime or exact handoff is claimed. Work stops at producer actual-pixel preflight.

See `direction-status-gap-matrix.tsv`, `qa-report.json`, `source-lock.tsv`, `generation-log.md` and `delivery-hashes.sha256`.
"""
    (HERE / "completion-report.md").write_text(text, encoding="utf-8")


def write_hashes() -> None:
    names = (
        FRONT_EXACT_NAME,
        *FOUR_CELL_NAMES.values(),
        *DISPLAY_NAMES.values(),
        *HALF_NAMES.values(),
        REVIEW_NAME,
        MAP_NAME,
        "direction-status-gap-matrix.tsv",
        "source-lock.tsv",
        "generation-log.md",
        "qa-report.json",
        "completion-report.md",
        Path(__file__).name,
    )
    lines = []
    for name in names:
        path = HERE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        lines.append(f"{sha256(path)}  {name}")
    (HERE / "delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    paths = validate_sources()
    write_source_lock(paths)

    front_path = paths["GZ_V10X_Q_FRONT"]
    shutil.copyfile(front_path, HERE / FRONT_EXACT_NAME)
    south_native = Image.open(front_path).convert("RGBA")
    if south_native.size != (1024, 1024):
        raise RuntimeError(f"Unexpected front master size: {south_native.size}")

    sheet = Image.open(paths["GZ_V10X_Q_FOUR"]).convert("RGBA")
    cells = fixed_sheet_cells(sheet)
    crop_equal: dict[str, bool] = {}
    for index, key in enumerate(("south_sheet", "west", "north", "east")):
        output = HERE / FOUR_CELL_NAMES[key]
        cells[key].save(output, optimize=False)
        reopened = Image.open(output).convert("RGBA")
        expected = sheet.crop((index * 640, 0, (index + 1) * 640, 960))
        crop_equal[key] = ImageChops.difference(reopened, expected).getbbox() is None

    native_by_direction = {
        "south": south_native,
        "west": pad_cell_to_square(cells["west"]),
        "north": pad_cell_to_square(cells["north"]),
        "east": pad_cell_to_square(cells["east"]),
    }
    display: dict[str, Image.Image] = {}
    half: dict[str, Image.Image] = {}
    for key, native in native_by_direction.items():
        display[key] = resize_once(native, DISPLAY_SIZE)
        half[key] = resize_once(native, HALF_SIZE)
        display[key].save(HERE / DISPLAY_NAMES[key], optimize=False)
        half[key].save(HERE / HALF_NAMES[key], optimize=False)

    build_review_board(display, half).convert("RGB").save(HERE / REVIEW_NAME, optimize=False)
    build_map_board(paths["A4_VIEWPORT"], display["south"]).convert("RGB").save(HERE / MAP_NAME, optimize=False)
    write_gap_matrix()
    write_generation_log()

    direction_metrics: dict[str, object] = {}
    for key in ("south", "west", "north", "east"):
        image = display[key]
        direction_metrics[key] = {
            "source": "330346 front exact" if key == "south" else f"3873 fixed cell {('west','north','east').index(key) + 1}",
            "size": list(image.size),
            "alpha_bbox": list(alpha_bbox(image)),
            "alpha_nonzero": alpha_nonzero(image),
            "pivot": [128, 243],
            "resize": "one native-to-256 LANCZOS",
        }

    sheet_front_display = resize_once(pad_cell_to_square(cells["south_sheet"]), DISPLAY_SIZE)
    mirrored_east = display["east"].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    structure_risk_metrics = {
        "south_master_vs_sheet_front_alpha_iou": binary_alpha_iou(display["south"], sheet_front_display),
        "west_vs_mirrored_east_alpha_iou": binary_alpha_iou(display["west"], mirrored_east),
        "interpretation": "same-source lineage proven; exact rig-like structural equivalence not proven",
        "pass_fail_role": "risk evidence only; no automatic visual threshold",
    }

    source_lock_pass_all = all(sha256(paths[s.source_id]) == s.expected_sha256 for s in SOURCES)
    fixed_crop_pixel_equal_all = all(crop_equal.values())
    front_expected = next(source.expected_sha256 for source in SOURCES if source.source_id == "GZ_V10X_Q_FRONT")
    south_exact_copy = sha256(HERE / FRONT_EXACT_NAME) == front_expected
    output_alpha_present_all = all(alpha_nonzero(display[key]) > 0 for key in display)
    machine_pass = source_lock_pass_all and fixed_crop_pixel_equal_all and south_exact_copy and output_alpha_present_all
    metrics: dict[str, object] = {
        "task": "75-c01e02-guardian-z-v10x-q-lineage-recovery-and-asset-governance-correction §5.1",
        "authority": "Candidate",
        "runtime_allowed": False,
        "redesign": False,
        "visible_pixel_generation": False,
        "imagegen_calls": 0,
        "blender_calls": 0,
        "svg_calls": 0,
        "pillow_visible_mecha_drawing": False,
        "operations": ["byte_copy", "fixed_crop", "transparent_pad", "single_resize", "layout", "qa", "hash"],
        "source_lock_pass_all": source_lock_pass_all,
        "fixed_crop_pixel_equal": crop_equal,
        "fixed_crop_pixel_equal_all": fixed_crop_pixel_equal_all,
        "south_exact_copy": south_exact_copy,
        "output_alpha_present_all": output_alpha_present_all,
        "display_scale": [256, 256],
        "display_pivot": [128, 243],
        "half_review_scale": [128, 128],
        "half_review_pivot": [64, 121],
        "map_anchor": list(MAP_ANCHOR),
        "map_footprint": MAP_FOOTPRINT,
        "structure_risk_metrics": structure_risk_metrics,
        "directions": direction_metrics,
        "machine_pass": machine_pass,
        "visual_pass": "PENDING_PRODUCER_ACTUAL_PIXEL_PREFLIGHT",
        "ua91": "NOT_OPEN",
        "downstream": "STOPPED",
    }
    (HERE / "qa-report.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_completion_report(metrics)
    write_hashes()

    if not machine_pass:
        raise RuntimeError("Task75 zero-redraw preflight machine gate failed")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
