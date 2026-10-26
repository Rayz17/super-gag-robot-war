#!/usr/bin/env python3
"""Read-only validator for the C01E02 A5 four-facing idle atlas package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image, ImageChops

import generate_art_a5_rift_swarm_four_facing_atlas as gen


OUT = Path(__file__).resolve().parent
EXPECTED_IMAGES = {
    gen.ATLAS_FILES[96]: ((384, 96), "RGBA"),
    gen.ATLAS_FILES[128]: ((512, 128), "RGBA"),
    "A5_atlas_overview_review_3000x1200.png": ((3000, 1200), "RGB"),
    "A5_four_facing_baseline_edge_review_3000x1800.png": ((3000, 1800), "RGB"),
    "A5_MAP_B_WEST_96_128_scale_compare_2560x820.png": ((2560, 820), "RGB"),
    "A5_MAP_B_CENTRAL_96_128_scale_compare_2560x820.png": ((2560, 820), "RGB"),
    "A5_MAP_B_EAST_96_128_scale_compare_2560x820.png": ((2560, 820), "RGB"),
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


def require_image(name: str, size: tuple[int, int], mode: str) -> Image.Image:
    path = OUT / name
    if not path.is_file():
        fail(f"missing image: {name}")
    image = Image.open(path)
    image.load()
    if image.size != size or image.mode != mode:
        fail(f"image contract mismatch: {name}: {image.size}/{image.mode}")
    return image


def assert_pixel_equal(left: Image.Image, right: Image.Image, label: str) -> None:
    if left.mode != right.mode:
        right = right.convert(left.mode)
    if left.size != right.size or ImageChops.difference(left, right).getbbox() is not None:
        fail(f"pixel mismatch: {label}")


def validate_atlases() -> None:
    for size in gen.SIZES:
        atlas = require_image(gen.ATLAS_FILES[size], (size * 4, size), "RGBA")
        for index, facing in enumerate(gen.ORDER):
            frame = atlas.crop((index * size, 0, (index + 1) * size, size))
            source = gen.frame_image(facing, size)
            assert_pixel_equal(frame, source, f"{size}px idle/{facing} direct paste")
            alpha = frame.getchannel("A")
            bbox = alpha.getbbox()
            if bbox is None or bbox[3] != size:
                fail(f"bottom baseline missing: {size}px idle/{facing}")
            bottom_contact_bbox = alpha.crop((0, size - 1, size, size)).getbbox()
            if (
                bottom_contact_bbox is None
                or not (bottom_contact_bbox[0] <= size // 2 < bottom_contact_bbox[2])
            ):
                fail(f"bottom-center contact missing: {size}px idle/{facing}")
            if alpha.crop((0, 0, 1, size)).getbbox() or alpha.crop((size - 1, 0, size, size)).getbbox():
                fail(f"cross-frame side pixel risk: {size}px idle/{facing}")
            if alpha.crop((0, 0, size, 1)).getbbox():
                fail(f"top frame edge is not transparent: {size}px idle/{facing}")
            gen.red_seam_bbox(frame)

    pngs = {path.name for path in OUT.glob("*.png")}
    configured_atlases = set(gen.ATLAS_FILES.values())
    missing_atlases = configured_atlases - pngs
    if missing_atlases:
        fail(f"A5 configured atlas candidates missing: {sorted(missing_atlases)}")
    unexpected_atlases = {
        name
        for name in pngs
        if "ATLAS" in name.upper()
        and "OVERVIEW" not in name.upper()
        and name not in configured_atlases
    }
    if unexpected_atlases:
        fail(f"A5 contains unregistered atlas candidates: {sorted(unexpected_atlases)}")


def validate_atlas_spec() -> None:
    rows = load_tsv("atlas-spec.tsv")
    if len(rows) != 8:
        fail(f"atlas-spec expected 8 rows, got {len(rows)}")
    for size in gen.SIZES:
        size_rows = [row for row in rows if row["frame_size"] == f"{size}x{size}"]
        if len(size_rows) != 4:
            fail(f"atlas-spec {size}px row count mismatch")
        size_rows.sort(key=lambda row: int(row["frame_index"]))
        atlas_sha = sha256_file(OUT / gen.ATLAS_FILES[size])
        for index, (row, facing) in enumerate(zip(size_rows, gen.ORDER, strict=True)):
            expected = {
                "package_id": gen.PACKAGE_ID,
                "subject_id": gen.SUBJECT_ID,
                "candidate_id": gen.CANDIDATE_ID,
                "runtime_slot_id": gen.SLOT_ID,
                "relative_path": gen.ATLAS_FILES[size],
                "sheet_dimensions": f"{size * 4}x{size}",
                "frame_index": str(index),
                "frame_id": f"idle/{facing}",
                "frame_rect": f"{index * size},0,{size},{size}",
                "source_path": gen.sample_path(facing, size),
                "source_sha256": gen.SAMPLE_HASHES[(facing, size)],
                "packing_operation": "mechanical_direct_paste_no_scale_no_repaint",
                "binding_kind": "sprite_sheet",
                "pivot": gen.PIVOT,
                "footprint": gen.FOOTPRINT,
                "actions": "idle",
                "facings": ";".join(gen.ORDER),
                "edge_gap_px": "0",
                "baseline_y": str(size - 1),
                "bottom_center_contact": "true",
                "atlas_sha256": atlas_sha,
                "lifecycle": "Candidate",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
                "user_decision_required": "true",
            }
            for field, value in expected.items():
                if row.get(field) != value:
                    fail(f"atlas-spec mismatch: {size}px {facing} {field}")


def validate_instance_defer() -> None:
    rows = load_tsv("instance-variation-defer.tsv")
    expected_ids = {f"ENEMY_C01_RIFT_SWARM_{index:02d}" for index in range(1, 7)}
    if len(rows) != 6 or {row["instance_stable_id"] for row in rows} != expected_ids:
        fail("instance defer set mismatch")
    for row in rows:
        if row["master_slot_id"] != gen.SLOT_ID or row["approved_master_candidate"] != gen.CANDIDATE_ID:
            fail(f"instance defer master mismatch: {row['instance_stable_id']}")
        if row["binding_state"] != "runtime_deferred_not_bound" or row["atlas_output"] != "none_one_shared_master_only":
            fail(f"instance defer state mismatch: {row['instance_stable_id']}")
        if row["runtime_allowed"] != "false" or row["runtime_handoff"] != "none":
            fail(f"instance defer runtime mismatch: {row['instance_stable_id']}")


def validate_source_receipt() -> None:
    rows = load_tsv("source-validation-receipt.tsv")
    expected = {relative: digest for relative, digest, _ in gen.STATIC_SOURCES}
    if len(rows) != len(expected) or {row["source_path"] for row in rows} != set(expected):
        fail("source receipt set mismatch")
    for row in rows:
        path = gen.ROOT / row["source_path"]
        actual = sha256_file(path)
        if row["expected_sha256"] != expected[row["source_path"]] or row["actual_sha256"] != actual:
            fail(f"source receipt hash mismatch: {row['source_path']}")
        if row["validation"] != "PASS_exact_sha256" or row["active_source"] != "true" or row["mutation"] != "none":
            fail(f"source receipt boundary mismatch: {row['source_path']}")
        lowered = row["source_path"].lower()
        if "story_first" in lowered or "/history" in lowered or "art-g1-5/b3-tactical-map" in lowered:
            fail(f"denied source entered A5: {row['source_path']}")


def validate_manifest() -> None:
    rows = load_tsv("asset-manifest.tsv")
    if not rows:
        fail("asset manifest is empty")
    atlas_rows = [row for row in rows if row["asset_role"].startswith("atlas_candidate_")]
    if len(atlas_rows) != 2 or {row["relative_path"] for row in atlas_rows} != set(gen.ATLAS_FILES.values()):
        fail("manifest atlas candidate set mismatch")
    map_rows = [row for row in rows if row["asset_role"] == "external_map_scale_review"]
    if len(map_rows) != 3 or any(row["contains_external_map_overlay"] != "true" for row in map_rows):
        fail("manifest map overlay evidence mismatch")
    for row in rows:
        if row["package_id"] != gen.PACKAGE_ID or row["subject_id"] != gen.SUBJECT_ID:
            fail(f"manifest identity mismatch: {row['relative_path']}")
        if row["runtime_slot_id"] != gen.SLOT_ID or row["candidate_id"] != gen.CANDIDATE_ID:
            fail(f"manifest slot/candidate mismatch: {row['relative_path']}")
        if row["lifecycle"] != "Candidate" or row["runtime_allowed"] != "false" or row["runtime_handoff"] != "none":
            fail(f"manifest runtime boundary mismatch: {row['relative_path']}")
        if row["user_decision_required"] != "true":
            fail(f"manifest user gate mismatch: {row['relative_path']}")
        path = OUT / row["relative_path"]
        if not path.is_file() or sha256_file(path) != row["sha256"]:
            fail(f"manifest file/hash mismatch: {row['relative_path']}")
        lowered = row["relative_path"].lower()
        if any(token in lowered for token in ("move", "impact", "death", "libtv", "godot")):
            fail(f"forbidden A5 output entered manifest: {row['relative_path']}")
    for row in atlas_rows:
        if row["actions"] != "idle" or row["facings"] != ";".join(gen.ORDER):
            fail(f"atlas manifest action/facing mismatch: {row['relative_path']}")
        if row["pivot"] != gen.PIVOT or row["footprint"] != gen.FOOTPRINT:
            fail(f"atlas manifest pivot/footprint mismatch: {row['relative_path']}")


def validate_review_images() -> None:
    for name, (size, mode) in EXPECTED_IMAGES.items():
        require_image(name, size, mode)


def validate_decision_card() -> None:
    path = OUT / "user-decision-card.md"
    if not path.is_file():
        fail("missing user-decision-card.md")
    text = path.read_text(encoding="utf-8")
    for size in gen.SIZES:
        filename = gen.ATLAS_FILES[size]
        digest = sha256_file(OUT / filename)
        if filename not in text or digest not in text:
            fail(f"decision card concrete file/hash missing: {size}")
    for token in ("四朝向", "接地点", "96px", "128px", "六实例", "exact handoff"):
        if token not in text:
            fail(f"decision card token missing: {token}")


def validate_hashes() -> None:
    path = OUT / "core-delivery-hashes.sha256"
    if not path.is_file():
        fail("missing core-delivery-hashes.sha256")
    listed: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        listed.add(relative)
        target = gen.ROOT / relative
        if not target.is_file() or sha256_file(target) != digest:
            fail(f"core delivery hash mismatch: {relative}")
    required_paths = [gen.ROOT / relative for relative, _, _ in gen.STATIC_SOURCES]
    required_paths.extend(
        OUT / name for name in (
            gen.ATLAS_FILES[96],
            gen.ATLAS_FILES[128],
            "atlas-spec.tsv",
            "instance-variation-defer.tsv",
            "source-validation-receipt.tsv",
            "asset-manifest.tsv",
            "user-decision-card.md",
            "completion-report.md",
            "generate_art_a5_rift_swarm_four_facing_atlas.py",
            "validate_art_a5_rift_swarm_four_facing_atlas.py",
        )
    )
    required = {item.relative_to(gen.ROOT).as_posix() for item in required_paths}
    missing = required - listed
    if missing:
        fail(f"core hash coverage missing: {sorted(missing)}")


def main() -> None:
    gen.validate_sources()
    validate_atlases()
    validate_atlas_spec()
    validate_instance_defer()
    validate_source_receipt()
    validate_manifest()
    validate_review_images()
    validate_decision_card()
    validate_hashes()
    print("PASS C01E02 A5 four-facing idle atlas Candidate package")
    print(f"package={gen.PACKAGE_ID}")
    print(f"atlas_96_sha256={sha256_file(OUT / gen.ATLAS_FILES[96])}")
    print(f"atlas_128_sha256={sha256_file(OUT / gen.ATLAS_FILES[128])}")
    print("actions=idle facings=north,east,south,west shared_master=true")
    print("runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
