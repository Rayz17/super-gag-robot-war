#!/usr/bin/env python3
"""Read-only validator for C01E02 A8 B1.1 narrow visual rework."""

from __future__ import annotations

import csv
import hashlib
from collections import deque
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in (HERE, *HERE.parents) if (parent / ".git").exists())
PACKAGE_ID = "C01CDV1_A8_PHASE_B1_1_V1"
VEHICLE = HERE.parent / "phase-b0-b1" / "assets" / "vehicles" / "R05_VEHICLE_EAST_STATIC_128x128.png"
VEHICLE_SHA = "09db0e7b97fcd2f522209cb68aefdcd88afcc40d468e28eb27233fb4b84180c3"

EXPECTED_IMAGES = {
    "assets/atlases/R05_COMMS_OLD_GUARDIAN_V10X_B1_1_3072x768.png": ((3072, 768), "RGBA", 1024, 3),
    "assets/atlases/R05_GUARDIAN_Z_SOUTH_ACTION_B1_1_1280x256.png": ((1280, 256), "RGBA", 256, 5),
    "assets/atlases/R05_BREAKER_NORTH_ACTION_B1_1_960x320.png": ((960, 320), "RGBA", 320, 3),
    "assets/props/R05_SHIELD_WALL_HUNG_B1_1_256x256.png": ((256, 256), "RGBA", 256, 1),
    "review/A8_B1_1_A4_INITIAL_ACTUAL_SCALE_2400x1350.png": ((2400, 1350), "RGB", 2400, 1),
    "review/A8_B1_1_T3_CONTACT_UI_CROP_1280x720.png": ((1280, 720), "RGB", 1280, 1),
    "review/A8_B1_1_BEFORE_AFTER_2800x2200.png": ((2800, 2200), "RGB", 2800, 1),
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


def component_count(alpha: Image.Image) -> int:
    mask = alpha.point(lambda value: 255 if value >= 64 else 0)
    pixels = mask.load()
    width, height = mask.size
    seen = bytearray(width * height)
    count = 0
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if seen[index] or not pixels[x, y]:
                continue
            count += 1
            queue = deque([(x, y)])
            seen[index] = 1
            while queue:
                px, py = queue.popleft()
                for nx in range(max(0, px - 1), min(width, px + 2)):
                    for ny in range(max(0, py - 1), min(height, py + 2)):
                        nindex = ny * width + nx
                        if not seen[nindex] and pixels[nx, ny]:
                            seen[nindex] = 1
                            queue.append((nx, ny))
    return count


def validate_images(errors: list[str]) -> None:
    for relative, (size, mode, frame_width, frame_count) in EXPECTED_IMAGES.items():
        path = HERE / relative
        require(path.is_file(), f"missing image: {relative}", errors)
        if not path.is_file():
            continue
        with Image.open(path) as image:
            require(image.size == size, f"wrong size {relative}: {image.size}", errors)
            require(image.mode == mode, f"wrong mode {relative}: {image.mode}", errors)
            if mode == "RGBA":
                alpha = image.getchannel("A")
                require(alpha.getbbox() is not None, f"empty alpha: {relative}", errors)
                for index in range(frame_count):
                    require(alpha.crop((index * frame_width, 0, (index + 1) * frame_width, size[1])).getbbox() is not None, f"empty frame {index}: {relative}", errors)


def validate_sources(errors: list[str]) -> None:
    for row in rows(HERE / "source-validation-receipt.tsv"):
        path = ROOT / row["path"]
        require(row["result"] == "match", f"source receipt drift: {row['source_id']}", errors)
        require(row["runtime_allowed"] == "false", f"source runtime flag drift: {row['source_id']}", errors)
        require(path.is_file(), f"source missing: {row['path']}", errors)
        if path.is_file():
            require(sha256(path) == row["expected_sha256"] == row["actual_sha256"], f"source hash mismatch: {row['source_id']}", errors)


def validate_visual_audits(errors: list[str]) -> None:
    stability = rows(HERE / "old-guardian-identity-stability-audit.tsv")
    require(len(stability) == 3, "old guardian stability row count", errors)
    for row in stability:
        require(row["result"] == "pass" and float(row["center_error_px"]) <= 2, f"old guardian center drift: {row['state']}", errors)

    safety = {row["state"]: row for row in rows(HERE / "breaker-contact-safety-audit.tsv")}
    contact = safety.get("contact", {})
    require(contact.get("result") == "pass", "BREAKER contact safety failed", errors)
    for key in ("left_margin", "top_margin", "right_margin"):
        require(int(contact.get(key, "-1")) >= 8, f"BREAKER contact {key} <8", errors)

    t3 = rows(HERE / "t3-readability-audit.tsv")
    require(len(t3) == 1 and t3[0]["result"] == "pass", "T3 overlap audit failed", errors)
    if t3:
        require(float(t3[0]["bbox_overlap_ratio"]) <= 0.5, "T3 bbox overlap >0.5", errors)

    scar_mask = Image.open(HERE / "source-layers" / "shield" / "shield-old-burn-scar-mask-256x256.png").convert("RGBA")
    require(component_count(scar_mask.getchannel("A")) == 3, "shield scar mask must contain exactly three components", errors)

    alpha = rows(HERE / "alpha-pivot-audit.tsv")
    require(len(alpha) == 12, f"unexpected alpha audit rows: {len(alpha)}", errors)
    for row in alpha:
        if row["asset_id"].startswith("R05_COMMS"):
            require(row["result"] == "review", "portrait pivot should remain review-only", errors)
        else:
            require(row["result"] == "pass", f"pivot baseline failed: {row['asset_id']}[{row['frame_index']}]", errors)


def validate_vehicle(errors: list[str]) -> None:
    require(VEHICLE.is_file(), "reused vehicle missing", errors)
    if VEHICLE.is_file():
        require(sha256(VEHICLE) == VEHICLE_SHA, "reused vehicle byte drift", errors)
    require(not (HERE / "assets" / "vehicles").exists(), "B1.1 must not create a local vehicle copy", errors)
    ledger = rows(HERE / "vehicle-byte-preservation.tsv")
    require(len(ledger) == 1 and ledger[0]["actual_sha256"] == VEHICLE_SHA, "vehicle preservation ledger mismatch", errors)


def validate_manifest(errors: list[str]) -> None:
    manifest = rows(HERE / "asset-manifest.tsv")
    require(manifest, "empty manifest", errors)
    ids = {row["asset_id"] for row in manifest}
    require("vehicle_east_static_reused" in ids, "vehicle reuse missing from manifest", errors)
    for row in manifest:
        require(row["package_id"] == PACKAGE_ID, f"wrong package: {row['asset_id']}", errors)
        require(row["lifecycle"] == "Candidate", f"non-Candidate: {row['asset_id']}", errors)
        require(row["runtime_allowed"] == "false", f"runtime enabled: {row['asset_id']}", errors)
        require(row["runtime_handoff"] == "none", f"runtime handoff set: {row['asset_id']}", errors)
        require(row["exact_handoff"] == "false", f"exact handoff set: {row['asset_id']}", errors)
        require(row["canon_promotion"] == "none", f"Canon promotion set: {row['asset_id']}", errors)
        path = (HERE / row["path"]).resolve()
        require(path.is_file(), f"manifest path missing: {row['path']}", errors)
        if path.is_file():
            require(sha256(path) == row["sha256"], f"manifest hash mismatch: {row['asset_id']}", errors)


def validate_core_hashes(errors: list[str]) -> None:
    for line in (HERE / "core-delivery-hashes.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        require(path.is_file(), f"core hash target missing: {relative}", errors)
        if path.is_file():
            require(sha256(path) == expected, f"core hash mismatch: {relative}", errors)


def main() -> None:
    errors: list[str] = []
    validate_images(errors)
    validate_sources(errors)
    validate_visual_audits(errors)
    validate_vehicle(errors)
    validate_manifest(errors)
    validate_core_hashes(errors)
    if errors:
        print(f"FAIL {PACKAGE_ID}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"PASS {PACKAGE_ID}")
    print("images=7 old_guardian_center<=2 breaker_contact_ltr>=8 shield_scars=3")
    print(f"vehicle_sha256={VEHICLE_SHA} local_copy=false")
    print("lifecycle=Candidate runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
