#!/usr/bin/env python3
"""Read-only validator for the bounded C01E02 A3 Rift Swarm review package."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

import generate_art_a3_rift_swarm_qsd as gen


OUT = Path(__file__).resolve().parent


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    path = OUT / name
    if not path.is_file():
        fail(f"missing TSV: {name}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require_file(relative: str) -> Path:
    path = OUT / relative
    if not path.is_file():
        fail(f"missing output: {relative}")
    return path


def validate_candidates() -> None:
    rows = read_tsv("candidate-spec.tsv")
    if len(rows) != 3:
        fail(f"candidate count must be 3, got {len(rows)}")
    expected = {candidate.stable_id for candidate in gen.CANDIDATES}
    if {row["candidate_id"] for row in rows} != expected:
        fail("candidate stable IDs drifted")
    if {row["candidate_code"] for row in rows} != {"A", "B", "C"}:
        fail("candidate codes must be A/B/C")
    for row in rows:
        if row["footprint"] != "1,1" or row["pivot"] != "bottom_center":
            fail(f"candidate footprint/pivot drift: {row['candidate_id']}")
        if row["facings"].split(";") != list(gen.FACINGS):
            fail(f"candidate facings drift: {row['candidate_id']}")
        if row["native_sizes"] != "96;128":
            fail(f"candidate sizes drift: {row['candidate_id']}")
        if row["instance_rule"] != "one_master_plus_six_light_variants":
            fail(f"candidate instance rule drift: {row['candidate_id']}")
        if (row["lifecycle"], row["runtime_allowed"], row["runtime_handoff"]) != ("Candidate", "false", "none"):
            fail(f"candidate authority drift: {row['candidate_id']}")


def validate_samples() -> None:
    rows = read_tsv("transparent-sample-index.tsv")
    if len(rows) != 24:
        fail(f"transparent sample index must contain 24 rows, got {len(rows)}")
    expected_keys = {
        (candidate.stable_id, facing, size)
        for candidate in gen.CANDIDATES
        for facing in gen.FACINGS
        for size in gen.SAMPLE_SIZES
    }
    actual_keys: set[tuple[str, str, int]] = set()
    indexed_paths: set[str] = set()
    for row in rows:
        width, height = (int(value) for value in row["native_size"].split("x"))
        if width != height:
            fail(f"non-square Q/SD sample: {row['path']}")
        actual_keys.add((row["candidate_id"], row["facing"], width))
        indexed_paths.add(row["path"])
        path = require_file(row["path"])
        with Image.open(path) as opened:
            if opened.size != (width, height) or opened.mode != "RGBA":
                fail(f"sample dimensions/channels mismatch: {row['path']} {opened.size} {opened.mode}")
            alpha = opened.getchannel("A")
            minimum, maximum = alpha.getextrema()
            if minimum != 0 or maximum == 0:
                fail(f"sample must have transparent exterior and nonempty art: {row['path']}")
            corners = (alpha.getpixel((0, 0)), alpha.getpixel((width - 1, 0)), alpha.getpixel((0, height - 1)), alpha.getpixel((width - 1, height - 1)))
            if any(corners):
                fail(f"sample corner transparency failed: {row['path']}")
        if row["channels"] != "RGBA" or row["pivot"] != "bottom_center" or row["footprint"] != "1,1":
            fail(f"sample interface drift: {row['path']}")
        if row["final_atlas"] != "false" or row["lifecycle"] != "Candidate" or row["runtime_allowed"] != "false" or row["runtime_handoff"] != "none":
            fail(f"sample authority drift: {row['path']}")
    if actual_keys != expected_keys:
        fail("sample candidate/facing/size matrix is incomplete")
    actual_paths = {path.relative_to(OUT).as_posix() for path in (OUT / "samples").glob("*.png")}
    if actual_paths != indexed_paths:
        fail("transparent sample folder and index differ")


def validate_variants() -> None:
    rows = read_tsv("instance-light-variation-spec.tsv")
    if len(rows) != 18:
        fail(f"variation spec must contain 18 rows, got {len(rows)}")
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["candidate_id"]].append(row)
        if row["identity_shared"] != "true" or row["proportion_shared"] != "true" or row["action_grammar_shared"] != "true" or row["collision_shared"] != "true":
            fail(f"variant illegally changes master identity: {row['instance_stable_id']}")
        if row["independent_design"] != "false":
            fail(f"variant became independent design: {row['instance_stable_id']}")
        if (row["lifecycle"], row["runtime_allowed"], row["runtime_handoff"]) != ("Candidate", "false", "none"):
            fail(f"variant authority drift: {row['instance_stable_id']}")
    for candidate in gen.CANDIDATES:
        candidate_rows = grouped[candidate.stable_id]
        if {row["instance_stable_id"] for row in candidate_rows} != set(gen.INSTANCE_IDS):
            fail(f"candidate {candidate.code} does not map one master to all six instances")
        if {int(row["variation_index"]) for row in candidate_rows} != set(range(6)):
            fail(f"candidate {candidate.code} variation indices drifted")


def validate_map_placements() -> None:
    rows = read_tsv("map-b-central-overlay-placement.tsv")
    if len(rows) != 18:
        fail(f"map placement must contain 18 rows, got {len(rows)}")
    source_bindings = gen.validate_sources()
    expected = {row["instance_stable_id"]: row for row in source_bindings}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["candidate_id"]].append(row)
        source = expected.get(row["instance_stable_id"])
        if not source:
            fail(f"unknown map instance: {row['instance_stable_id']}")
        for field in ("anchor", "footprint", "facing"):
            if row[field] != source[field]:
                fail(f"map placement changed {field}: {row['instance_stable_id']}")
        if row["profile_id"] != gen.PROFILE_ID or row["topology_sha256"] != gen.TOPOLOGY_SHA256:
            fail(f"map profile/topology drift: {row['instance_stable_id']}")
        if row["organization_state"] != "scattered" or row["relocated"] != "false" or row["map_baked"] != "false":
            fail(f"map organization/bake drift: {row['instance_stable_id']}")
        expected_position = gen.CENTRAL_PLACEMENTS.get(row["instance_stable_id"])
        if (row["central_visible"] == "true") != (expected_position is not None):
            fail(f"CENTRAL visibility drift: {row['instance_stable_id']}")
        if expected_position and (row["central_screen_x"], row["central_screen_y"]) != tuple(str(value) for value in expected_position):
            fail(f"CENTRAL screen coordinate drift: {row['instance_stable_id']}")
        if (row["lifecycle"], row["runtime_allowed"], row["runtime_handoff"]) != ("Candidate", "false", "none"):
            fail(f"map placement authority drift: {row['instance_stable_id']}")
    for candidate in gen.CANDIDATES:
        candidate_rows = grouped[candidate.stable_id]
        if len(candidate_rows) != 6 or sum(row["central_visible"] == "true" for row in candidate_rows) != 4:
            fail(f"candidate {candidate.code} must preserve 6 anchors with 4 visible in CENTRAL")


def validate_images() -> None:
    expected = {
        "A3_direction_board_3000x1800.png": (3000, 1800),
        "A3_four_direction_action_space_3000x1800.png": (3000, 1800),
        "A3_footprint_pivot_occlusion_2400x1350.png": (2400, 1350),
        "A3_one_master_six_variants_2400x1200.png": (2400, 1200),
        "A3_MAP_B_CENTRAL_comparison_3000x1200.png": (3000, 1200),
    }
    for candidate in gen.CANDIDATES:
        expected[f"A3_candidate_{candidate.code.lower()}_identity_sheet_1800x1200.png"] = (1800, 1200)
        expected[f"A3_{candidate.code}_MAP_B_CENTRAL_composite_1280x720.png"] = (1280, 720)
    for relative, dimensions in expected.items():
        path = require_file(relative)
        with Image.open(path) as opened:
            if opened.size != dimensions or opened.mode != "RGB":
                fail(f"review image mismatch: {relative} {opened.size} {opened.mode}")
            extrema = opened.convert("L").getextrema()
            if extrema[0] == extrema[1]:
                fail(f"blank review image: {relative}")


def validate_source_receipt() -> None:
    rows = read_tsv("source-validation-receipt.tsv")
    if len(rows) != len(gen.STATIC_SOURCES) + len(gen.SCOPED_CANON_SOURCES):
        fail("source receipt row count drifted")
    by_path = {row["source_path"]: row for row in rows}
    for relative, expected, _, _ in gen.STATIC_SOURCES:
        row = by_path.get(relative)
        if not row or row["source_sha256"] != expected or row["validation"] != "exact_sha256_pass" or row["mutation"] != "none":
            fail(f"static source receipt drift: {relative}")


def validate_manifest_and_hashes() -> None:
    rows = read_tsv("asset-manifest.tsv")
    manifest_by_path = {row["relative_path"]: row for row in rows}
    expected_files = {
        path.relative_to(OUT).as_posix(): path
        for path in gen.package_files()
    }
    if set(manifest_by_path) != set(expected_files):
        missing = sorted(set(expected_files) - set(manifest_by_path))
        extra = sorted(set(manifest_by_path) - set(expected_files))
        fail(f"manifest coverage mismatch: missing={missing} extra={extra}")
    for relative, path in expected_files.items():
        row = manifest_by_path[relative]
        if row["sha256"] != sha256_file(path):
            fail(f"manifest hash mismatch: {relative}")
        if row["package_id"] != gen.PACKAGE_ID or row["subject_id"] != gen.SUBJECT_ID:
            fail(f"manifest package/subject drift: {relative}")
        if row["uses_old_asset"] != "false" or row["uses_final_atlas"] != "false" or row["map_baked"] != "false":
            fail(f"manifest forbidden-source/atlas/bake flag: {relative}")
        if (row["lifecycle"], row["runtime_allowed"], row["runtime_handoff"]) != ("Candidate", "false", "none"):
            fail(f"manifest authority drift: {relative}")

    hashes_path = require_file("delivery-hashes.sha256")
    recorded: dict[str, str] = {}
    for line in hashes_path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        recorded[relative] = digest
    expected_hash_files = {
        path.relative_to(OUT).as_posix(): path
        for path in gen.package_files(include_manifest=True)
    }
    if set(recorded) != set(expected_hash_files):
        fail("delivery hash coverage mismatch")
    for relative, path in expected_hash_files.items():
        if recorded[relative] != sha256_file(path):
            fail(f"delivery hash mismatch: {relative}")


def validate_forbidden_outputs() -> None:
    forbidden_suffixes = {".tscn", ".tres", ".gd", ".godot", ".mp4", ".mov", ".webm", ".gif", ".wav", ".mp3", ".ogg"}
    for path in OUT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in forbidden_suffixes:
            fail(f"forbidden Runtime/video/audio output: {path.relative_to(OUT)}")
        lowered = path.name.lower()
        if "atlas" in lowered or "libtv" in lowered or "cut-in" in lowered or "cutin" in lowered:
            fail(f"forbidden atlas/LibTV/Cut-in output: {path.relative_to(OUT)}")


def main() -> None:
    gen.validate_sources()
    validate_candidates()
    validate_samples()
    validate_variants()
    validate_map_placements()
    validate_images()
    validate_source_receipt()
    validate_manifest_and_hashes()
    validate_forbidden_outputs()
    counts = Counter(path.suffix.lower() for path in OUT.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    print(f"A3 VALIDATION PASS: package={gen.PACKAGE_ID} files={sum(counts.values())} png={counts['.png']} tsv={counts['.tsv']} md={counts['.md']} py={counts['.py']}")
    print("authority=Candidate runtime_allowed=false runtime_handoff=none final_atlas=false map_baked=false")


if __name__ == "__main__":
    main()
