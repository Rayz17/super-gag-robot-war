#!/usr/bin/env python3
"""Read-only validator for A6 PNG packing, alpha bounds, and source layers."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKING_PATH = ROOT.parent / "42-c01e02-m3-r0-5-media-packing-v2.json"
FFMPEG = shutil.which("ffmpeg")
DOUDENG_ROOT = ROOT.parents[1] / "battle-presentation-v0.1/art-delivery/approved"


@dataclass(frozen=True)
class Image:
    path: Path
    width: int
    height: int
    pixels: bytes


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def png_header(path: Path) -> tuple[int, int, int]:
    data = path.read_bytes()[:33]
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        fail(f"not a PNG: {path}")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    if bit_depth != 8:
        fail(f"expected 8-bit PNG: {path}")
    return width, height, color_type


def load_rgba(path: Path) -> Image:
    if not path.is_file():
        fail(f"missing file: {path}")
    width, height, color_type = png_header(path)
    if color_type not in (4, 6):
        fail(f"PNG has no alpha channel: {path}")
    if not FFMPEG:
        fail("ffmpeg is required")
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgba", "pipe:1"],
        check=True,
        capture_output=True,
    )
    expected = width * height * 4
    if len(result.stdout) != expected:
        fail(f"unexpected decoded byte count: {path}")
    return Image(path, width, height, result.stdout)


def alpha_bbox(image: Image, x0: int = 0, y0: int = 0, width: int | None = None, height: int | None = None):
    width = image.width - x0 if width is None else width
    height = image.height - y0 if height is None else height
    xs: list[int] = []
    ys: list[int] = []
    for y in range(height):
        row = ((y0 + y) * image.width + x0) * 4
        for x in range(width):
            if image.pixels[row + x * 4 + 3] > 0:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def edge_alpha_max(image: Image, x0: int, y0: int, width: int, height: int) -> int:
    values: list[int] = []
    for x in range(width):
        values.append(image.pixels[((y0 * image.width + x0 + x) * 4) + 3])
        values.append(image.pixels[((((y0 + height - 1) * image.width) + x0 + x) * 4) + 3])
    for y in range(height):
        values.append(image.pixels[((((y0 + y) * image.width) + x0) * 4) + 3])
        values.append(image.pixels[((((y0 + y) * image.width) + x0 + width - 1) * 4) + 3])
    return max(values, default=0)


def green_fringe_ratio(image: Image, x0: int, y0: int, width: int, height: int) -> float:
    edge_pixels = 0
    green_pixels = 0
    for y in range(height):
        row = ((y0 + y) * image.width + x0) * 4
        for x in range(width):
            r, g, b, a = image.pixels[row + x * 4 : row + x * 4 + 4]
            if 0 < a < 250:
                edge_pixels += 1
                if g > 100 and g > r + 35 and g > b + 35:
                    green_pixels += 1
    return green_pixels / edge_pixels if edge_pixels else 0.0


def extract_cell(image: Image, x0: int, y0: int, width: int, height: int) -> bytes:
    rows = []
    for y in range(height):
        start = (((y0 + y) * image.width) + x0) * 4
        rows.append(image.pixels[start : start + width * 4])
    return b"".join(rows)


def validate_atlas(slot: dict, atlas_path: Path, state_paths: list[Path]) -> list[str]:
    atlas = load_rgba(atlas_path)
    total_width, total_height = slot["total_size"]
    frame_width, frame_height = slot["frame_size"]
    columns, rows = slot["grid"]
    safe_x, safe_y, safe_width, safe_height = slot["safe_rect"]
    if (atlas.width, atlas.height) != (total_width, total_height):
        fail(f"wrong atlas size for {slot['slot_id']}: {(atlas.width, atlas.height)}")
    if len(state_paths) != slot["frame_count"] or columns * rows != slot["frame_count"]:
        fail(f"frame count mismatch for {slot['slot_id']}")

    reports = []
    for index, state_path in enumerate(state_paths):
        column = index % columns
        row = index // columns
        x0 = column * frame_width
        y0 = row * frame_height
        state = load_rgba(state_path)
        if (state.width, state.height) != (frame_width, frame_height):
            fail(f"wrong state size: {state_path}")
        cell = extract_cell(atlas, x0, y0, frame_width, frame_height)
        if cell != state.pixels:
            fail(f"atlas cell does not match state order at index {index}: {atlas_path}")
        bbox = alpha_bbox(atlas, x0, y0, frame_width, frame_height)
        if bbox is None:
            fail(f"empty atlas cell at index {index}: {atlas_path}")
        x1, y1, x2, y2 = bbox
        if x1 < safe_x or y1 < safe_y or x2 >= safe_x + safe_width or y2 >= safe_y + safe_height:
            fail(f"alpha bbox outside safe rect at index {index}: {bbox} vs {slot['safe_rect']}")
        if edge_alpha_max(atlas, x0, y0, frame_width, frame_height) != 0:
            fail(f"nontransparent frame edge at index {index}: {atlas_path}")
        fringe = green_fringe_ratio(atlas, x0, y0, frame_width, frame_height)
        if fringe > 0.005:
            fail(f"green fringe ratio {fringe:.4f} at index {index}: {atlas_path}")
        reports.append(f"{slot['frame_order'][index]} bbox={bbox} fringe={fringe:.4f}")
    return reports


def require_layer(path: Path, size: tuple[int, int]) -> None:
    image = load_rgba(path)
    if (image.width, image.height) != size:
        fail(f"wrong layer size: {path}")
    if alpha_bbox(image) is None:
        fail(f"empty required layer: {path}")
    if edge_alpha_max(image, 0, 0, image.width, image.height) != 0:
        fail(f"required layer touches outer edge: {path}")


def validate_external_doudeng() -> None:
    expected = {
        "cutin_doudeng_c01_observe_v01.png": "b8530e98b9d76edb9275680488558167ad368697fe6f55a3af00ac5492196d3a",
        "cutin_doudeng_c01_tense_v01.png": "c846e48b04b7d8671fd4853330487d0f39d1df98a70550d1f03d49770a26f159",
    }
    for name, expected_hash in expected.items():
        path = DOUDENG_ROOT / name
        image = load_rgba(path)
        if (image.width, image.height) != (1920, 640):
            fail(f"Doudeng approved source size drift: {path}")
        if sha256(path) != expected_hash:
            fail(f"Doudeng approved source hash drift: {path}")


def validate_review_assets() -> None:
    required = [
        "boards/jicun-state-board-1280x720.png",
        "boards/qihai-state-board-1280x720.png",
        "boards/old-guardian-state-board-1280x720.png",
        "boards/doudeng-approved-layout-board-1280x720.png",
        "boards/layout-safe-area-review-board-1280x720.png",
        "boards/alpha-edge-review-board-1280x720.png",
        "simulations/jicun-doudeng-local-1280x720.png",
        "simulations/jicun-qihai-remote-presence-1280x720.png",
        "simulations/jicun-old-guardian-machine-1280x720.png",
    ]
    for relative in required:
        image = load_rgba(ROOT / relative)
        if (image.width, image.height) != (1280, 720):
            fail(f"review asset is not 1280x720: {relative}")


def validate_qihai_correction_and_mask(slot: dict) -> list[str]:
    active = ROOT / "sources/chroma/qihai-decision-keyed-source.png"
    rejected = ROOT / "sources/chroma/qihai-decision-speaking-drift-rejected-source.png"
    if not active.is_file() or not rejected.is_file():
        fail("Qihai decision correction trace is incomplete")
    if sha256(active) == sha256(rejected):
        fail("Qihai active decision still equals rejected speaking drift")
    mask = load_rgba(ROOT / "source-layers/qihai/remote-noise-mask-768.png")
    alpha = mask.pixels[3::4]
    nonzero = sum(value > 0 for value in alpha)
    if nonzero < 1000 or max(alpha, default=0) == 0:
        fail("Qihai remote noise mask has no usable signal")
    if max(alpha) > 96:
        fail("Qihai remote noise mask is too opaque for a restrained presence card")
    safe_x, safe_y, safe_width, safe_height = slot["safe_rect"]
    reports = []
    for state in ("controlled", "decision", "concerned"):
        path = ROOT / f"assets/portraits/qihai/r05-portrait-qihai-remote-{state}-768.png"
        image = load_rgba(path)
        if (image.width, image.height) != tuple(slot["frame_size"]):
            fail(f"wrong Qihai character layer size: {path}")
        bbox = alpha_bbox(image)
        if bbox is None:
            fail(f"empty Qihai character layer: {path}")
        x1, y1, x2, y2 = bbox
        if x1 < safe_x or y1 < safe_y or x2 >= safe_x + safe_width or y2 >= safe_y + safe_height:
            fail(f"Qihai character bbox outside safe rect: {state} {bbox}")
        if edge_alpha_max(image, 0, 0, image.width, image.height) != 0:
            fail(f"Qihai character layer touches outer edge: {state}")
        fringe = green_fringe_ratio(image, 0, 0, image.width, image.height)
        if fringe > 0.005:
            fail(f"Qihai character green fringe ratio {fringe:.4f}: {state}")
        reports.append(f"R05_PORTRAIT_QIHAI_REMOTE character_{state} bbox={bbox} fringe={fringe:.4f}")
    return reports


def validate_specs_and_claims() -> None:
    portrait_path = ROOT / "portrait-spec.tsv"
    with portrait_path.open(encoding="utf-8", newline="") as source:
        portrait_rows = list(csv.DictReader(source, delimiter="\t"))
    if len(portrait_rows) != 5:
        fail("portrait-spec.tsv must contain three new slots and two Doudeng references")
    for row in portrait_rows:
        if row["runtime_allowed"] != "false" or row["runtime_handoff"] != "none":
            fail(f"portrait spec lifecycle drift: {row['slot_id']}")
    qihai_rows = [row for row in portrait_rows if row["slot_id"] == "R05_PORTRAIT_QIHAI_REMOTE"]
    if len(qihai_rows) != 1 or "presence_cards" not in qihai_rows[0]["consumer"]:
        fail("Qihai portrait consumer is not presence_cards")
    if "not_character_comms" not in qihai_rows[0]["consumer"]:
        fail("Qihai portrait spec does not exclude dialogue consumption")

    layout_path = ROOT / "review-layout-spec.tsv"
    with layout_path.open(encoding="utf-8", newline="") as source:
        layout_rows = list(csv.DictReader(source, delimiter="\t"))
    qihai_layout = [row for row in layout_rows if row["review_id"] == "A6_SIM_QIHAI_PRESENCE"]
    if len(qihai_layout) != 1:
        fail("missing Qihai presence layout row")
    semantics = qihai_layout[0]["qihai_presence_semantics"]
    required_semantics = (
        "consumer=presence_cards",
        "not_character_comms",
        "line_text_empty",
        "status_text=本人停机令已撤回",
        "interactive=false",
        "command_capability=none",
        "artillery_authority=false",
    )
    for token in required_semantics:
        if token not in semantics:
            fail(f"missing Qihai presence semantic: {token}")
    if qihai_layout[0]["text_baked"] != "false" or qihai_layout[0]["buttons_baked"] != "false":
        fail("Qihai review mockup must not bake text or buttons")

    decision_card = (ROOT / "user-decision-card.md").read_text(encoding="utf-8")
    for token in ("presence_cards", "不是通讯台词", "line_text", "runtime_allowed=false", "runtime_handoff=none"):
        if token not in decision_card:
            fail(f"user decision card missing boundary: {token}")

    completion = (ROOT / "completion-report.md").read_text(encoding="utf-8")
    required_claims = (
        "Claim level: presentation judgeability only",
        "General common-turn causality: NOT PROVEN",
        "Editable route/waypoints: NOT IMPLEMENTED",
        "Commit summary completeness: INCOMPLETE IN FROZEN R0",
        "Derived mutation/settlement evidence: NOT PROVEN",
        "Actual route hash: NOT IMPLEMENTED",
        "R1 readiness: BLOCKED BY PRODUCTION BOARD HARD GATES",
    )
    for claim in required_claims:
        if claim not in completion:
            fail(f"completion report missing claim boundary: {claim}")


def validate_manifest() -> None:
    manifest_path = ROOT / "asset-manifest.tsv"
    with manifest_path.open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    if len(rows) < 40:
        fail("asset manifest is unexpectedly small")
    ids: set[str] = set()
    paths: set[str] = set()
    for row in rows:
        asset_id = row["asset_id"]
        relative = row["path"]
        if asset_id in ids or relative in paths:
            fail(f"duplicate manifest id or path: {asset_id} {relative}")
        ids.add(asset_id)
        paths.add(relative)
        if row["lifecycle"] != "Candidate":
            fail(f"manifest lifecycle drift: {relative}")
        if row["runtime_allowed"] != "false" or row["runtime_handoff"] != "none":
            fail(f"manifest runtime boundary drift: {relative}")
        for field in ("source_tool", "rights_note", "forbidden_states"):
            if not row[field]:
                fail(f"manifest missing {field}: {relative}")
        path = ROOT / relative
        if not path.is_file():
            fail(f"manifest points to missing file: {relative}")
        if sha256(path) != row["sha256"]:
            fail(f"manifest hash mismatch: {relative}")
    required_ids = {"R05_PORTRAIT_JICUN", "R05_PORTRAIT_QIHAI_REMOTE", "R05_COMMS_OLD_GUARDIAN"}
    if not required_ids.issubset(ids):
        fail("manifest is missing one or more packed slot IDs")
    png_paths = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*.png")
        if path.is_file()
    }
    if png_paths != {path for path in paths if path.endswith(".png")}:
        missing = sorted(png_paths - paths)
        stale = sorted({path for path in paths if path.endswith(".png")} - png_paths)
        fail(f"manifest PNG coverage mismatch missing={missing} stale={stale}")
    for path in png_paths:
        if "cutin_doudeng_c01_" in path.lower():
            fail(f"Doudeng approved Stable ID was copied into A6: {path}")


def main() -> int:
    packing = json.loads(PACKING_PATH.read_text(encoding="utf-8"))
    if packing["packing_contract_id"] != "C01E02_R05_MEDIA_PACKING_V2":
        fail("unexpected packing contract")
    slots = {slot["slot_id"]: slot for slot in packing["visual_slots"]}

    atlas_specs = [
        (
            "R05_PORTRAIT_JICUN",
            ROOT / "assets/atlases/r05-portrait-jicun-states-2304x768.png",
            [ROOT / f"assets/portraits/jicun/r05-portrait-jicun-{state}-768.png" for state in ("focused", "alarm", "resolve")],
        ),
        (
            "R05_PORTRAIT_QIHAI_REMOTE",
            ROOT / "assets/atlases/r05-portrait-qihai-remote-states-2304x768.png",
            [
                ROOT / f"assets/portraits/qihai/composite/r05-portrait-qihai-remote-{state}-composite-768.png"
                for state in ("controlled", "decision", "concerned")
            ],
        ),
        (
            "R05_COMMS_OLD_GUARDIAN",
            ROOT / "assets/atlases/r05-comms-old-guardian-states-3072x768.png",
            [
                ROOT / f"assets/comms/old_guardian/states/r05-comms-old-guardian-{state}-1024x768.png"
                for state in ("guide", "contact", "shield_gaze")
            ],
        ),
    ]

    reports = []
    for slot_id, atlas_path, state_paths in atlas_specs:
        reports.extend(f"{slot_id} {line}" for line in validate_atlas(slots[slot_id], atlas_path, state_paths))

    require_layer(ROOT / "source-layers/qihai/remote-noise-mask-768.png", (768, 768))
    for state in ("guide", "contact", "shield_gaze"):
        layer_root = ROOT / f"source-layers/old_guardian/{state}"
        for name in ("head-rgba-1024x768.png", "chest-rgba-1024x768.png", "waveform-rgba-1024x768.png"):
            require_layer(layer_root / name, (1024, 768))

    validate_external_doudeng()
    validate_review_assets()
    character_reports = validate_qihai_correction_and_mask(slots["R05_PORTRAIT_QIHAI_REMOTE"])
    validate_specs_and_claims()
    validate_manifest()

    for path in ROOT.rglob("*"):
        if path.is_symlink():
            fail(f"symlink is not allowed in delivery root: {path}")

    for report in reports:
        print(report)
    for report in character_reports:
        print(report)
    print(
        "A6_MEDIA_PACKING_V2_OK "
        f"validated_frames={len(reports)} character_layers={len(character_reports)} "
        "review_assets=9 manifest=verified "
        "runtime_allowed=false runtime_handoff=none"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"A6_MEDIA_PACKING_V2_FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
