#!/usr/bin/env python3
"""Read-only validator for the bounded C01E02 A4 MAP-B Candidate package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image, ImageChops

import generate_art_a4_map_b_six_layer as gen


OUT = Path(__file__).resolve().parent
CORE_CODES = {row[0] for row in gen.CORE_LAYER_ROWS}
CORE_FILENAMES = {row[3] for row in gen.CORE_LAYER_ROWS}
EXPECTED_REVIEW_IMAGES = {
    "A4_MAP_B_six_layer_composite_full_2400x1350.png": (2400, 1350),
    "A4_MAP_B_pure_read_no_ui_2400x1350.png": (2400, 1350),
    "A4_MAP_B_P1_AFTER_review_2400x1350.png": (2400, 1350),
    "A4_MAP_B_viewport_west_1280x720.png": (1280, 720),
    "A4_MAP_B_viewport_central_1280x720.png": (1280, 720),
    "A4_MAP_B_viewport_east_1280x720.png": (1280, 720),
    "A4_MAP_B_three_viewport_continuity_3840x820.png": (3840, 820),
    "A4_layer_switch_alpha_board_3000x1800.png": (3000, 1800),
    "A4_occlusion_footprint_review_2400x1350.png": (2400, 1350),
    "A4_state_difference_board_3000x1600.png": (3000, 1600),
    "A4_MAP_B_overview_review_3000x1800.png": (3000, 1800),
}
STATE_FILES = {
    "active": "A4_MAP_B_STATE_RESCUE_ACTIVE_2400x1350.png",
    "cleared": "A4_MAP_B_STATE_RESCUE_CLEARED_2400x1350.png",
    "wall_hung": "A4_MAP_B_STATE_SHIELD_WALL_HUNG_2400x1350.png",
    "rack_empty": "A4_MAP_B_STATE_SHIELD_RACK_EMPTY_2400x1350.png",
    "damage_before": "A4_MAP_B_STATE_DAMAGE_BEFORE_2400x1350.png",
    "damage_after": "A4_MAP_B_STATE_DAMAGE_AFTER_2400x1350.png",
    "p1_after": "A4_MAP_B_STATE_P1_AFTER_2400x1350.png",
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_tsv(name: str) -> list[dict[str, str]]:
    path = OUT / name
    if not path.is_file():
        fail(f"missing TSV: {name}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require_image(name: str, size: tuple[int, int], mode: str | None = None) -> Image.Image:
    path = OUT / name
    if not path.is_file():
        fail(f"missing image: {name}")
    image = Image.open(path)
    image.load()
    if image.size != size:
        fail(f"image size mismatch: {name}: {image.size}")
    if mode is not None and image.mode != mode:
        fail(f"image mode mismatch: {name}: {image.mode}")
    return image


def assert_same(left: Image.Image, right: Image.Image, label: str) -> None:
    if left.mode != right.mode:
        right = right.convert(left.mode)
    if ImageChops.difference(left, right).getbbox() is not None:
        fail(f"pixel mismatch: {label}")


def assert_different(left: Image.Image, right: Image.Image, label: str) -> None:
    if left.mode != right.mode:
        right = right.convert(left.mode)
    if ImageChops.difference(left, right).getbbox() is None:
        fail(f"expected visible difference missing: {label}")


def validate_layer_spec() -> dict[str, Image.Image]:
    rows = load_tsv("layer-spec.tsv")
    core = [row for row in rows if row["layer_code"] in CORE_CODES]
    if len(core) != 6 or {row["relative_path"] for row in core} != CORE_FILENAMES:
        fail("layer-spec core layer set mismatch")
    if len(rows) != 13:
        fail(f"layer-spec expected 13 rows, got {len(rows)}")

    expected = {row[0]: row for row in gen.CORE_LAYER_ROWS}
    images: dict[str, Image.Image] = {}
    for row in rows:
        for field, value in (
            ("package_id", gen.PACKAGE_ID),
            ("dimensions", "2400x1350"),
            ("origin", gen.ORIGIN),
            ("pivot", gen.PIVOT),
            ("pixel_registration", "exact_same_canvas"),
            ("topology_sha256", gen.TOPOLOGY_SHA256),
            ("lifecycle", "Candidate"),
            ("runtime_allowed", "false"),
            ("runtime_handoff", "none"),
            ("user_decision_required", "true"),
        ):
            if row[field] != value:
                fail(f"layer-spec boundary mismatch: {row['layer_code']} {field}")
        if row["layer_code"] not in CORE_CODES:
            require_image(row["relative_path"], gen.CANVAS, "RGBA")

    for code, (_, slot_id, stable_id, filename, order, channels, _) in expected.items():
        row = next(item for item in core if item["layer_code"] == code)
        if row["slot_id"] != slot_id or row["stable_id"] != stable_id:
            fail(f"R2 slot/stable ID mismatch: {code}")
        if row["layer_order"] != str(order) or row["channels"] != channels:
            fail(f"layer channel/order mismatch: {code}")
        images[code] = require_image(filename, gen.CANVAS, channels)

    if images["BASE"].mode != "RGB":
        fail("BASE must be opaque RGB")
    for code in CORE_CODES - {"BASE"}:
        alpha = images[code].getchannel("A")
        minimum, maximum = alpha.getextrema()
        if minimum != 0 or maximum == 0:
            fail(f"transparent layer alpha range invalid: {code}: {(minimum, maximum)}")

    mask = images["OCCLUSION_MASK"]
    red, green, blue, alpha = mask.split()
    if any(channel.getbbox() is None for channel in (red, green, blue, alpha)):
        fail("occlusion mask requires nonempty R/G/B/A semantics")
    roof_alpha = images["ROOFS"].getchannel("A")
    building_alpha = images["BUILDINGS"].getchannel("A")
    if ImageChops.subtract(roof_alpha, red).getbbox() is not None:
        fail("roof pixels are not covered by mask R fade fill")
    if ImageChops.subtract(building_alpha, red).getbbox() is not None:
        fail("building pixels are not covered by mask R fade fill")
    if ImageChops.subtract(red, alpha).getbbox() is not None:
        fail("mask alpha does not cover fade-fill channel")
    return images


def validate_topology() -> None:
    source = gen.load_tsv(gen.ROOT / gen.STATIC_SOURCES[7][0])
    receipt = load_tsv("topology-lock-receipt.tsv")
    if len(source) != len(receipt):
        fail("topology receipt row count drift")
    for original, derived in zip(source, receipt, strict=True):
        for field, value in original.items():
            if derived.get(field) != value:
                fail(f"topology source field changed: {field}")
        if derived["a4_anchor_or_rect"] != original["anchor_or_rect"] or derived["a4_match"] != "exact":
            fail("A4 anchor/rect is not exact")
        if derived["topology_signature"] != gen.TOPOLOGY_SHA256:
            fail("A4 topology signature mismatch")
        if derived["runtime_allowed"] != "false" or derived["runtime_handoff"] != "none":
            fail("topology receipt runtime boundary mismatch")


def validate_states_and_composites(images: dict[str, Image.Image]) -> None:
    states = {key: require_image(filename, gen.CANVAS, "RGBA") for key, filename in STATE_FILES.items()}
    for key in ("active", "wall_hung", "damage_before"):
        assert_same(images["STATE_LAYERS"], states[key], f"default state vs {key}")
    assert_different(states["active"], states["cleared"], "rescue active to cleared")
    assert_different(states["wall_hung"], states["rack_empty"], "shield wall-hung to empty")
    assert_different(states["damage_before"], states["damage_after"], "E02 damage before to after")
    assert_different(states["active"], states["p1_after"], "default to P1-after")

    composite = require_image("A4_MAP_B_six_layer_composite_full_2400x1350.png", gen.CANVAS, "RGB")
    expected = gen.compose_map(images["BASE"], images["BUILDINGS"], images["STATE_LAYERS"], images["ROOFS"], images["FOREGROUND"])
    assert_same(composite, expected, "six-layer composite")
    empty = Image.new("RGBA", gen.CANVAS, (0, 0, 0, 0))
    pure = require_image("A4_MAP_B_pure_read_no_ui_2400x1350.png", gen.CANVAS, "RGB")
    expected_pure = gen.compose_map(images["BASE"], images["BUILDINGS"], empty, images["ROOFS"], images["FOREGROUND"])
    assert_same(pure, expected_pure, "pure-read map")
    p1 = require_image("A4_MAP_B_P1_AFTER_review_2400x1350.png", gen.CANVAS, "RGB")
    expected_p1 = gen.compose_map(images["BASE"], images["BUILDINGS"], states["p1_after"], images["ROOFS"], images["FOREGROUND"])
    assert_same(p1, expected_p1, "P1-after map")


def validate_receipts_and_manifest() -> None:
    sources = load_tsv("source-validation-receipt.tsv")
    expected_paths = {relative for relative, _, _ in gen.STATIC_SOURCES} | {
        gen.A3_OVERLAY,
        "docs/superpowers/specs/data/canon/scenes.tsv",
    }
    if {row["source_path"] for row in sources} != expected_paths:
        fail("source receipt set mismatch")
    for row in sources:
        source = gen.ROOT / row["source_path"]
        if sha256_file(source) != row["source_sha256"]:
            fail(f"source receipt hash mismatch: {row['source_path']}")
        if row["active_source"] != "true" or row["mutation"] != "none" or not row["validation"].startswith("PASS"):
            fail(f"source receipt boundary mismatch: {row['source_path']}")
        lowered = row["source_path"].lower()
        if "story_first" in lowered or "/history" in lowered or "art-g1-5/b3-tactical-map" in lowered:
            fail(f"superseded or denied source entered A4: {row['source_path']}")
    a3 = next(row for row in sources if row["source_path"] == gen.A3_OVERLAY)
    if a3["usage_boundary"] != "review_overlay_only_not_baked_not_atlas":
        fail("A3 sample is not scoped to external review overlay")

    manifest = load_tsv("asset-manifest.tsv")
    if not manifest:
        fail("asset manifest is empty")
    core_rows = [row for row in manifest if row["asset_role"] == "core_layer"]
    if len(core_rows) != 6 or {row["relative_path"] for row in core_rows} != CORE_FILENAMES:
        fail("manifest core layer set mismatch")
    overlay_rows = [row for row in manifest if row["contains_external_unit_overlay"] == "true"]
    if len(overlay_rows) != 1 or overlay_rows[0]["relative_path"] != "A4_occlusion_footprint_review_2400x1350.png":
        fail("external unit overlay manifest boundary mismatch")
    for row in manifest:
        if row["package_id"] != gen.PACKAGE_ID or row["subject_id"] != gen.SUBJECT_ID:
            fail(f"manifest package identity mismatch: {row['relative_path']}")
        if row["lifecycle"] != "Candidate" or row["runtime_allowed"] != "false" or row["runtime_handoff"] != "none":
            fail(f"manifest lifecycle/runtime mismatch: {row['relative_path']}")
        if row["contains_units_baked_in_core"] != "false" or row["uses_old_asset"] != "false" or row["uses_final_atlas"] != "false":
            fail(f"manifest forbidden asset boundary mismatch: {row['relative_path']}")
        if row["topology_sha256"] != gen.TOPOLOGY_SHA256:
            fail(f"manifest topology mismatch: {row['relative_path']}")
        path = OUT / row["relative_path"]
        if not path.is_file() or sha256_file(path) != row["sha256"]:
            fail(f"manifest file/hash mismatch: {row['relative_path']}")
        lowered = row["relative_path"].lower()
        if "atlas" in lowered or "libtv" in lowered or "godot" in lowered:
            fail(f"forbidden deliverable entered package: {row['relative_path']}")


def validate_review_evidence() -> None:
    for name, size in EXPECTED_REVIEW_IMAGES.items():
        require_image(name, size, "RGB")
    for code in ("WEST", "CENTRAL", "EAST"):
        require_image(f"A4_MAP_B_viewport_{code.lower()}_1280x720.png", (1280, 720), "RGB")


def validate_core_is_unit_free_by_construction() -> None:
    for function in (
        gen.draw_base,
        gen.draw_buildings,
        gen.draw_roofs,
        gen.draw_foreground,
        gen.occlusion_mask,
        gen.combine_state_layers,
    ):
        if "A3_OVERLAY" in function.__code__.co_names or "guardian_fixture" in function.__code__.co_names or "breaker_fixture" in function.__code__.co_names:
            fail(f"unit source referenced by core constructor: {function.__name__}")


def validate_hash_list() -> None:
    path = OUT / "core-delivery-hashes.sha256"
    if not path.is_file():
        fail("missing core-delivery-hashes.sha256")
    listed: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, relative = raw.split("  ", 1)
        listed.add(relative)
        target = gen.ROOT / relative
        if not target.is_file() or sha256_file(target) != digest:
            fail(f"core delivery hash mismatch: {relative}")
    required = {path.relative_to(gen.ROOT).as_posix() for path in (
        [gen.ROOT / relative for relative, _, _ in gen.STATIC_SOURCES]
        + [gen.ROOT / gen.A3_OVERLAY, gen.ROOT / "docs/superpowers/specs/data/canon/scenes.tsv"]
        + [OUT / row[3] for row in gen.CORE_LAYER_ROWS]
        + [OUT / "asset-manifest.tsv", OUT / "generate_art_a4_map_b_six_layer.py", OUT / "validate_art_a4_map_b_six_layer.py"]
    )}
    missing = required - listed
    if missing:
        fail(f"core hash coverage missing: {sorted(missing)}")


def main() -> None:
    gen.validate_sources()
    images = validate_layer_spec()
    validate_topology()
    validate_states_and_composites(images)
    validate_receipts_and_manifest()
    validate_review_evidence()
    validate_core_is_unit_free_by_construction()
    validate_hash_list()
    print("PASS C01E02 A4 MAP-B six-layer Candidate package")
    print(f"package={gen.PACKAGE_ID}")
    print(f"topology={gen.TOPOLOGY_SHA256}")
    print("core_layers=6 pixel_registration=exact_same_canvas")
    print("runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
