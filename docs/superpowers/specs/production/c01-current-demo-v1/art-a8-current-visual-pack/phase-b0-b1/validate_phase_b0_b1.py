#!/usr/bin/env python3
"""Read-only validator for the C01E02 A8 Phase B0/B1 Candidate package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in (HERE, *HERE.parents) if (parent / ".git").exists())
PACKAGE_ID = "C01CDV1_A8_PHASE_B0_B1_V1"

EXPECTED_IMAGES = {
    "assets/atlases/R05_COMMS_OLD_GUARDIAN_V10X_3072x768.png": ((3072, 768), "RGBA", 1024, 3),
    "assets/atlases/R05_GUARDIAN_Z_SOUTH_ACTION_PROOF_1280x256.png": ((1280, 256), "RGBA", 256, 5),
    "assets/atlases/R05_BREAKER_NORTH_ACTION_PROOF_960x320.png": ((960, 320), "RGBA", 320, 3),
    "assets/props/R05_SHIELD_WALL_HUNG_256x256.png": ((256, 256), "RGBA", 256, 1),
    "assets/vehicles/R05_VEHICLE_EAST_STATIC_128x128.png": ((128, 128), "RGBA", 128, 1),
    "review/A8_B1_A4_INITIAL_ACTUAL_SCALE_2400x1350.png": ((2400, 1350), "RGB", 2400, 1),
    "review/A8_B1_T3_CONTACT_UI_CROP_1280x720.png": ((1280, 720), "RGB", 1280, 1),
    "review/A8_B0_B1_COMPREHENSIVE_REVIEW_2600x1800.png": ((2600, 1800), "RGB", 2600, 1),
}

EXPECTED_SPEC = {
    "R05_COMMS_OLD_GUARDIAN_V10X": ("guide;contact;shield_gaze", "0.5,0.5"),
    "R05_GUARDIAN_Z_SOUTH_ACTION_PROOF": ("idle;step_a;step_b;brace;recoil", "0.5,0.88"),
    "R05_BREAKER_NORTH_ACTION_PROOF": ("idle;charge;contact", "0.5,0.9"),
    "R05_SHIELD_WALL_HUNG": ("wall_hung_cold", "0.5,1.0"),
    "R05_VEHICLE_EAST_STATIC": ("east_static", "0.5,0.82"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_images(errors: list[str]) -> None:
    for relative, (size, mode, frame_width, frame_count) in EXPECTED_IMAGES.items():
        path = HERE / relative
        require(path.is_file(), f"missing image: {relative}", errors)
        if not path.is_file():
            continue
        with Image.open(path) as image:
            require(image.size == size, f"wrong size {relative}: {image.size} != {size}", errors)
            require(image.mode == mode, f"wrong mode {relative}: {image.mode} != {mode}", errors)
            if mode == "RGBA":
                alpha = image.getchannel("A")
                require(alpha.getbbox() is not None, f"empty alpha: {relative}", errors)
                for index in range(frame_count):
                    frame = alpha.crop((index * frame_width, 0, (index + 1) * frame_width, size[1]))
                    require(frame.getbbox() is not None, f"empty frame {index}: {relative}", errors)


def validate_old_guardian_layers(errors: list[str]) -> None:
    states = ("guide", "contact", "shield_gaze")
    layers = ("head_chest", "chest_light", "speaker_waveform")
    for state in states:
        for layer in layers:
            relative = f"source-layers/old_guardian_v10x/{state}/{state}-{layer}-1024x768.png"
            path = HERE / relative
            require(path.is_file(), f"missing old guardian layer: {relative}", errors)
            if not path.is_file():
                continue
            with Image.open(path) as image:
                require(image.size == (1024, 768), f"wrong layer size: {relative}", errors)
                require(image.mode == "RGBA", f"wrong layer mode: {relative}", errors)
                require(image.getchannel("A").getbbox() is not None, f"empty layer: {relative}", errors)


def validate_specs(errors: list[str]) -> None:
    data = {row["asset_id"]: row for row in rows(HERE / "asset-spec.tsv")}
    for asset_id, (frame_order, pivot) in EXPECTED_SPEC.items():
        require(asset_id in data, f"missing spec row: {asset_id}", errors)
        if asset_id not in data:
            continue
        require(data[asset_id]["frame_order"] == frame_order, f"wrong frame order: {asset_id}", errors)
        require(data[asset_id]["pivot"] == pivot, f"wrong pivot: {asset_id}", errors)
    require(data.get("R05_GUARDIAN_Z_SOUTH_ACTION_PROOF", {}).get("footprint") == "2,2", "Guardian Z footprint drift", errors)
    require(data.get("R05_BREAKER_NORTH_ACTION_PROOF", {}).get("footprint") == "3,3", "BREAKER footprint drift", errors)


def validate_alpha_pivots(errors: list[str]) -> None:
    data = rows(HERE / "alpha-pivot-audit.tsv")
    require(len(data) == 13, f"unexpected alpha audit row count: {len(data)}", errors)
    for row in data:
        asset_id = row["asset_id"]
        if asset_id == "R05_COMMS_OLD_GUARDIAN_V10X":
            require(row["result"] == "review", "portrait pivot must stay review-only", errors)
        else:
            require(row["result"] == "pass", f"pivot baseline failed: {asset_id} frame {row['frame_index']}", errors)
            require(abs(int(row["baseline_delta_px"])) <= 1, f"pivot delta >1: {asset_id}", errors)


def validate_sources(errors: list[str]) -> None:
    receipt = rows(HERE / "source-validation-receipt.tsv")
    require(receipt, "empty source receipt", errors)
    for row in receipt:
        path = ROOT / row["path"]
        require(row["result"] == "match", f"source receipt not match: {row['source_id']}", errors)
        require(row["runtime_allowed"] == "false", f"source runtime flag drift: {row['source_id']}", errors)
        require(path.is_file(), f"missing frozen source: {row['path']}", errors)
        if path.is_file():
            actual = sha256(path)
            require(actual == row["expected_sha256"] == row["actual_sha256"], f"source hash drift: {row['source_id']}", errors)
    active_source_text = "\n".join(row["path"] for row in receipt).lower()
    require("v21" not in active_source_text, "V21 entered active source receipt", errors)


def validate_manifest(errors: list[str]) -> None:
    manifest = rows(HERE / "asset-manifest.tsv")
    require(manifest, "empty manifest", errors)
    for row in manifest:
        require(row["package_id"] == PACKAGE_ID, f"wrong package id: {row['asset_id']}", errors)
        require(row["lifecycle"] == "Candidate", f"non-Candidate row: {row['asset_id']}", errors)
        require(row["runtime_allowed"] == "false", f"runtime enabled: {row['asset_id']}", errors)
        require(row["runtime_handoff"] == "none", f"runtime handoff set: {row['asset_id']}", errors)
        require(row["exact_handoff"] == "false", f"exact handoff set: {row['asset_id']}", errors)
        require(row["canon_promotion"] == "none", f"Canon promotion set: {row['asset_id']}", errors)
        path = HERE / row["path"]
        require(path.is_file(), f"manifest path missing: {row['path']}", errors)
        if path.is_file():
            require(sha256(path) == row["sha256"], f"manifest hash mismatch: {row['asset_id']}", errors)


def validate_core_hashes(errors: list[str]) -> None:
    path = HERE / "core-delivery-hashes.sha256"
    require(path.is_file(), "missing core-delivery-hashes.sha256", errors)
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        target = ROOT / relative
        require(target.is_file(), f"core hash target missing: {relative}", errors)
        if target.is_file():
            require(sha256(target) == expected, f"core hash mismatch: {relative}", errors)


def main() -> None:
    errors: list[str] = []
    validate_images(errors)
    validate_old_guardian_layers(errors)
    validate_specs(errors)
    validate_alpha_pivots(errors)
    validate_sources(errors)
    validate_manifest(errors)
    validate_core_hashes(errors)
    if errors:
        print("FAIL C01CDV1_A8_PHASE_B0_B1_V1")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS C01CDV1_A8_PHASE_B0_B1_V1")
    print("images=8 old_guardian_layers=9 alpha_pivot_rows=13")
    print("lifecycle=Candidate runtime_allowed=false runtime_handoff=none")
    print("V21_active_source=false Godot_write=false Runtime_write=false")


if __name__ == "__main__":
    main()
