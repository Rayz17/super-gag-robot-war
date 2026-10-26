#!/usr/bin/env python3
"""Validate the bounded C01E02 A2 rolling-district Candidate package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]

PACKAGE_ID = "C01CDV1_A2_ROLLING_DISTRICT_V1"
PROFILE_ID = "c01cdv1_e02_scroll_m2_r2"
PROFILE_PATH = ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/graybox_profiles.json"
CONTRACT_PATH = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/19-current-demo-inplace-rebase-producer-contract.md"
CONTRACT_SHA256 = "6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94"
TOPOLOGY_SIGNATURE = "baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8"

SOURCE_HASHES = {
    "docs/superpowers/specs/production/c01-current-demo-v1/19-current-demo-inplace-rebase-producer-contract.md": CONTRACT_SHA256,
    "docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C01-闭馆以后万机出击.md": "c9a9aa490badea3d2de937e0003b80547974fed27103b31ec9181cd3583cfc8b",
    "docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C01/C01-用户创作验收回执.md": "3d11387d92120cfdeeb0069a2a7cdfbe677ed0ea2ac5ae6649038de7b0cd532b",
    "docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-剧情游玩拓扑与状态桥接.tsv": "5d640ed3e70854a178194ceeeffe7d444a928547a414af3407674b9d4f4be5aa",
    "docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/gameflow/C01-游戏流程解构-v1.md": "68ac0efa2d8316f33eb41ca745568684dd180021931355e8ff1d0798196b5296",
    "docs/superpowers/specs/2026-08-08-chao-gag-story-play-operation-topology-contract-v1.md": "550da9196bb9029aa0ceb7d75cd1bfdb73c852dd806fb4b609f1765c652eee76",
    "game-godot/content/candidate_runtime_demo/c01/e02/graybox_profiles.json": "07f611fabb1a41c713da5019ce433820f95229cbf83b633fe67fa43d836278da",
    "game-godot/content/candidate_runtime_demo/c01/e02/named_geometry_fallbacks.json": "cfcabcdf5dca0efebdc982ce59012cb8c7c89dc55a7ad71672b90140f2758c01",
    "game-godot/content/candidate_runtime_demo/c01/e02/generated/build_identity.json": "3ceadfee30defad3ed606759165da2f88df9c402c5d130585e07147f7b97bdb8",
    "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv": "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee",
    "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv": "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920",
    "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b2-user-approval-receipt.tsv": "792d9061b804ec3d87d79c777171f5aa4bd44979416c40d45d8968a2004d0c51",
    "docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md": "ec061505dc395c96136e9415985706ecf6c99c564e68c0c5686968581f40b653",
}

SCOPED_CANON_PATHS = {
    "docs/superpowers/specs/data/canon/authority_manifest.tsv",
    "docs/superpowers/specs/data/canon/entities.tsv",
    "docs/superpowers/specs/data/canon/scenes.tsv",
    "docs/superpowers/specs/data/canon/wanji_exhibition_zones.tsv",
}

SUPERSEDED_HASHES = {
    "docs/superpowers/specs/production/c01-current-demo-v1/18-g1-5-b3-tactical-map-art-objective.md": "d9f1c67ce7beddaf376cbcfee707e145f0c36f21c246fad7e9fcb977de587bcc",
    "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b3-tactical-map/asset-manifest.tsv": "424bc211fbeb79d6fbdb6b614729cc3f8aa8932e2d47374230074f82ece4cbff",
    "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b3-tactical-map/delivery-hashes.sha256": "e61700d0fbc5cb7696fd3aec9fffb0aee80ae4787364aaa852d378db3faf5b69",
}

CANDIDATE_IDS = {
    "CAND_C01CDV1_A2_DISTRICT_A_EXPO_SPINE_V1",
    "CAND_C01CDV1_A2_DISTRICT_B_RESCUE_RING_V1",
    "CAND_C01CDV1_A2_DISTRICT_C_LAYERED_RAIN_V1",
}

IMAGE_SPECS = {
    "A2_DIRECTION_BOARD_ABC_3000x1800.png": (3000, 1800),
    "A2_OCCLUSION_SAFEZONE_BOARD_2400x1350.png": (2400, 1350),
    "A2_SWARM_DENSITY_LMH_BOARD_2400x1000.png": (2400, 1000),
    "A2_PURE_READ_triptych_no_text_2400x900.png": (2400, 900),
}
for code in "ABC":
    IMAGE_SPECS.update({
        f"A2_MAP_{code}_full_domain_review_2400x1350.png": (2400, 1350),
        f"A2_MAP_{code}_pure_read_full_domain_2400x1350.png": (2400, 1350),
        f"A2_MAP_{code}_three_viewport_continuity_3840x820.png": (3840, 820),
        f"A2_MAP_{code}_viewport_west_1280x720.png": (1280, 720),
        f"A2_MAP_{code}_viewport_central_1280x720.png": (1280, 720),
        f"A2_MAP_{code}_viewport_east_1280x720.png": (1280, 720),
    })


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    path = OUT / name
    require(path.is_file(), f"missing {name}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_source_tsv(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_scoped_canon() -> None:
    authority = {
        (row["record_type"], row["record_id"]): row
        for row in read_source_tsv("docs/superpowers/specs/data/canon/authority_manifest.tsv")
    }
    for key in (
        ("entity", "V353U001"),
        ("entity", "ENEMY_C01_BREAKER"),
        ("entity", "ENEMY_C01_RIFT_SWARM"),
        ("scene", "V355-C01E02"),
    ):
        row = authority.get(key)
        require(bool(row), f"scoped Canon authority missing: {key}")
        require(row["canon_level"] == "working" and row["lifecycle_status"] == "active", f"scoped Canon authority drift: {key}")

    entities = {
        row["entity_id"]: row
        for row in read_source_tsv("docs/superpowers/specs/data/canon/entities.tsv")
    }
    guardian = entities.get("V353U001", {})
    breaker = entities.get("ENEMY_C01_BREAKER", {})
    swarm = entities.get("ENEMY_C01_RIFT_SWARM", {})
    require(guardian.get("status") == "working_current" and "18米" in guardian.get("role", ""), "Guardian Z scoped Canon drift")
    require(breaker.get("status") == "working_current" and "近30米" in breaker.get("implementation_policy", ""), "BREAKER scoped Canon drift")
    require(swarm.get("status") == "working_current" and "E02少量" in swarm.get("implementation_policy", ""), "swarm scoped Canon quantity drift")
    require("各自扑击" in swarm.get("implementation_policy", "") and "不锁造型" in swarm.get("notes", ""), "swarm scoped Canon behavior/design drift")

    scenes = {
        row["scene_id"]: row
        for row in read_source_tsv("docs/superpowers/specs/data/canon/scenes.tsv")
    }
    scene = scenes.get("V355-C01E02", {})
    required = set(scene.get("required_entities", "").split(";"))
    require({"V353U001", "ENEMY_C01_BREAKER", "ENEMY_C01_RIFT_SWARM"}.issubset(required), "C01E02 scoped required-entity drift")
    scene_text = scene.get("location", "") + scene.get("notes", "")
    for token in ("旧会展广场与相连街区", "最后应急车辆", "退役重盾", "各自扑击"):
        require(token in scene_text, f"C01E02 scoped scene token missing: {token}")

    zones = {
        row["zone_id"]: row
        for row in read_source_tsv("docs/superpowers/specs/data/canon/wanji_exhibition_zones.tsv")
    }
    external = zones.get("WEZ_EXT_01_DOCKYARD_LOCKS", {})
    require(external.get("map_code") == "EXT-D01" and "旧会展广场" in external.get("canonical_name", ""), "external old-expo scoped Canon drift")


def topology_signature(tactical: dict) -> str:
    payload = {
        "profile_id": tactical["profile_id"],
        "grid": tactical["grid"],
        "projection": tactical["projection"],
        "swarm_organization_state": tactical["swarm_organization_state"],
        "minimum_phase_survivors": tactical["minimum_phase_survivors"],
        "shield_hotspot": tactical["shield_hotspot"],
        "guard_zone": tactical["guard_zone"],
        "units": tactical["units"],
        "terrain_zones": tactical["terrain_zones"],
        "destructibles": tactical["destructibles"],
        "phase_checkpoint": tactical["phase_checkpoint"],
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_sources() -> dict:
    require(sha256(CONTRACT_PATH) == CONTRACT_SHA256, "producer contract hash drift")
    for relative, expected in SOURCE_HASHES.items():
        path = ROOT / relative
        require(path.is_file(), f"active source missing: {relative}")
        require(sha256(path) == expected, f"active source hash drift: {relative}")
    for relative in SCOPED_CANON_PATHS:
        require((ROOT / relative).is_file(), f"scoped Canon source missing: {relative}")
    for relative, expected in SUPERSEDED_HASHES.items():
        path = ROOT / relative
        require(path.is_file(), f"superseded audit source missing: {relative}")
        require(sha256(path) == expected, f"superseded audit source changed: {relative}")

    validate_scoped_canon()
    profile_doc = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    tactical = profile_doc["tactical_profile"]
    require(tactical["profile_id"] == PROFILE_ID, "wrong tactical profile")
    require(tactical["grid"] == [32, 18], "rolling grid is not 32x18")
    require(tactical["projection"]["tile_half"] == [40, 20], "projection drift")
    require(tactical["swarm_organization_state"] == "scattered", "swarm is not scattered")
    require(topology_signature(tactical) == TOPOLOGY_SIGNATURE, "topology signature drift")
    return tactical


def validate_receipts(tactical: dict) -> None:
    sources = read_tsv("source-receipt.tsv")
    expected_source_paths = set(SOURCE_HASHES) | SCOPED_CANON_PATHS
    require(len(sources) == len(expected_source_paths), "source receipt row count drift")
    require({row["source_path"] for row in sources} == expected_source_paths, "source receipt paths drift")
    for row in sources:
        if row["source_path"] in SOURCE_HASHES:
            require(row["sha256"] == SOURCE_HASHES[row["source_path"]], f"source receipt hash mismatch: {row['source_path']}")
            require(row["validation"] == "PASS_exact_sha256", f"exact source validation label drift: {row['source_path']}")
        else:
            require(len(row["sha256"]) == 64 and all(char in "0123456789abcdef" for char in row["sha256"]), f"invalid observed Canon hash: {row['source_path']}")
            require(row["validation"] == "PASS_scoped_semantics_observed_sha256", f"scoped Canon validation label drift: {row['source_path']}")
        require(row["active_source"] == "true", f"source not active: {row['source_path']}")
        require(row["runtime_source"] == "false", f"runtime source leak: {row['source_path']}")
        require("b3-tactical-map" not in row["source_path"] and "18-g1-5-b3" not in row["source_path"], "old B3 entered active source receipt")

    history = read_tsv("superseded-history-ledger.tsv")
    require(len(history) == 5, "superseded ledger must contain five audit-only rows")
    for row in history:
        require(row["classification"] == "superseded_history_only", "history classification drift")
        require(row["active_source"] == "false", "superseded source became active")
        require(row["allowed_use"] == "audit_trace_only", "superseded use boundary drift")
        require(row["modified_by_A2"] == "false", "A2 modified old B3 evidence")

    candidates = read_tsv("candidate-spec.tsv")
    require(len(candidates) == 3, "candidate count must be three")
    require({row["candidate_id"] for row in candidates} == CANDIDATE_IDS, "candidate IDs drift")
    for row in candidates:
        require(row["tactical_profile_id"] == PROFILE_ID, "candidate profile drift")
        require(row["topology_signature"] == TOPOLOGY_SIGNATURE, "candidate topology drift")
        require(row["grid"] == "32x18", "candidate grid drift")
        require(row["viewport"] == "900x594 inside 1280x720", "candidate viewport drift")
        require(row["swarm_organization_state"] == "scattered", "candidate swarm drift")
        require(row["lifecycle"] == "Candidate" and row["runtime_allowed"] == "false" and row["runtime_handoff"] == "none", "candidate runtime gate opened")

    cameras = read_tsv("camera-continuity.tsv")
    require(len(cameras) == 3, "camera continuity must contain three views")
    expected_camera = [
        ("1", "WEST", "-160,320", "n/a"),
        ("2", "CENTRAL", "240,480", "500"),
        ("3", "EAST", "830,620", "310"),
    ]
    for row, expected in zip(cameras, expected_camera):
        require((row["order"], row["camera_code"], row["review_center_world"], row["previous_overlap_world_x"]) == expected, "camera continuity drift")
        require(row["screen_rect"] == "0,54,900,594", "camera content rect drift")
        require(row["review_camera_is_runtime_lock"] == "false", "review camera became runtime lock")
        require(row["runtime_allowed"] == "false" and row["runtime_handoff"] == "none", "camera runtime gate opened")

    topology = read_tsv("topology-receipt.tsv")
    require(len(topology) == len(tactical["terrain_zones"]) + len(tactical["units"]) + len(tactical["destructibles"]), "topology receipt row count drift")
    expected_ids = {zone["zone_id"] for zone in tactical["terrain_zones"]}
    expected_ids |= {unit["unit_id"] for unit in tactical["units"]}
    expected_ids |= {item["object_id"] for item in tactical["destructibles"]}
    require({row["stable_id"] for row in topology} == expected_ids, "topology receipt identity drift")
    require(all(row["source_profile"] == PROFILE_ID and row["topology_signature"] == TOPOLOGY_SIGNATURE for row in topology), "topology receipt source drift")

    densities = read_tsv("swarm-density-spec.tsv")
    require([(row["density_option"], row["token_count"]) for row in densities] == [("LOW", "4"), ("MID", "6"), ("HIGH", "9")], "density options drift")
    for row in densities:
        anchors = row["anchors"].split(";")
        require(len(anchors) == len(set(anchors)) == int(row["token_count"]), "density anchors are not unique")
        require(row["organization_state"] == "scattered", "density formation drift")
        require(row["queue_or_arrow_formation"] == "false" and row["boss_synchronization"] == "false", "forbidden swarm formation")
        require(row["design_approval"] == "layout_density_only_not_mecha_design", "small-body design scope leak")
        require(row["runtime_allowed"] == "false" and row["runtime_handoff"] == "none", "density runtime gate opened")

    occlusion = read_tsv("occlusion-rule.tsv")
    require([row["candidate_mode"] for row in occlusion] == ["pure_fade", "fade_plus_outline", "hard_rule"], "occlusion choices drift")
    require(occlusion[0]["building_alpha"] == "0.25_candidate" and occlusion[1]["building_alpha"] == "0.18_candidate", "occlusion alpha drift")
    require(occlusion[2]["safe_area"] == "top_0..54;bottom_648..720;right_900..1280", "HUD safe area drift")
    require(all(row["collision_semantic"] == "unchanged_profile_owned" for row in occlusion), "occlusion changed collision semantics")


def validate_images() -> None:
    actual = {path.name for path in OUT.glob("*.png")}
    require(actual == set(IMAGE_SPECS), "image set drift")
    for name, size in IMAGE_SPECS.items():
        path = OUT / name
        with Image.open(path) as image:
            require(image.size == size, f"wrong dimensions: {name}")
            require(image.mode == "RGB", f"wrong image mode: {name}")
            reference = Image.new("RGB", image.size, image.getpixel((0, 0)))
            require(ImageChops.difference(image, reference).getbbox() is not None, f"blank image: {name}")


def validate_manifest_and_hashes() -> None:
    manifest = read_tsv("asset-manifest.tsv")
    expected_paths = {
        path.name for path in OUT.iterdir()
        if path.is_file()
        and path.name not in {"asset-manifest.tsv", "delivery-hashes.sha256", "BLOCKED.md", ".DS_Store"}
        and path.suffix != ".pyc"
    }
    require({row["relative_path"] for row in manifest} == expected_paths, "manifest coverage drift")
    for row in manifest:
        path = OUT / row["relative_path"]
        require(row["package_id"] == PACKAGE_ID, f"package ID drift: {path.name}")
        require(row["source_profile"] == PROFILE_ID and row["topology_signature"] == TOPOLOGY_SIGNATURE, f"manifest source drift: {path.name}")
        require(row["lifecycle"] == "Candidate", f"lifecycle drift: {path.name}")
        require(row["runtime_allowed"] == "false" and row["runtime_handoff"] == "none", f"runtime gate opened: {path.name}")
        require(row["uses_old_B3_asset"] == "false" and row["uses_final_sprite_master"] == "false", f"forbidden asset source: {path.name}")
        require(row["sha256"] == sha256(path), f"manifest hash mismatch: {path.name}")
        lower = path.name.lower()
        if path.suffix == ".png" and ("pure_read" in lower or "viewport_" in lower):
            require(row["contains_report_text"] == "false", f"pure/readability image text flag drift: {path.name}")

    hash_rows = {}
    for line in (OUT / "delivery-hashes.sha256").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        require(name not in hash_rows, f"duplicate hash entry: {name}")
        hash_rows[name] = digest
    expected_hashed = {
        path.name for path in OUT.iterdir()
        if path.is_file() and path.name not in {"delivery-hashes.sha256", "BLOCKED.md", ".DS_Store"} and path.suffix != ".pyc"
    }
    require(set(hash_rows) == expected_hashed, "delivery hash coverage drift")
    for name, digest in hash_rows.items():
        require(sha256(OUT / name) == digest, f"delivery hash mismatch: {name}")

    forbidden_suffixes = {".mp4", ".mov", ".webm", ".godot", ".tscn", ".tres", ".wav", ".ogg"}
    require(not any(path.suffix.lower() in forbidden_suffixes for path in OUT.rglob("*")), "forbidden runtime/video/audio output present")
    require(not (OUT / "BLOCKED.md").exists(), "package is marked BLOCKED")


def main() -> None:
    tactical = validate_sources()
    validate_receipts(tactical)
    validate_images()
    validate_manifest_and_hashes()
    print("PASS C01E02 A2 rolling-district Candidate package")
    print(f"package={PACKAGE_ID}")
    print(f"profile={PROFILE_ID} grid=32x18 topology={TOPOLOGY_SIGNATURE}")
    print("candidates=3 images=22 cameras=3 density=4/6/9 scattered")
    print("old_B3=history_only runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
