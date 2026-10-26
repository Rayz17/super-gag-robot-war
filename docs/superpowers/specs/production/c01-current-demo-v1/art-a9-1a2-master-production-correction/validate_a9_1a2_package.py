#!/usr/bin/env python3
"""Read-only validator for active A9.1-A2 2D evidence.

Rejected renderer sources live in history quarantine and are intentionally not
required or executed by this active production validator.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[5]
OBJECTIVE = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/62-c01e02-a9-1a2-master-production-correction-objective.md"
BOARD = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv"
OBJECTIVE_SHA = "b1cab624016e6d351ba3100fd4ebe4cf76dc6f4ad0abd88a35f7c6ec1bca816b"
BOARD_SHA = "02fe3009d8c0cc0710dcb543795decb3d80d91e67a449d1fa3e63d2c8656e801"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check_authority() -> None:
    assert sha256_file(OBJECTIVE) == OBJECTIVE_SHA, "objective drift"
    assert sha256_file(BOARD) == BOARD_SHA, "production board drift"


def check_manifest() -> None:
    rows = tsv(HERE / "asset-manifest.tsv")
    assert len(rows) == 15, f"expected 15 manifest rows, got {len(rows)}"
    for row in rows:
        assert row["lifecycle"] == "Candidate"
        assert row["runtime_allowed"] == "false"
        assert row["runtime_handoff"] == "none"
        path = HERE / row["path"]
        assert path.is_file(), f"missing manifest output: {path}"
        assert sha256_file(path) == row["sha256"], f"manifest hash mismatch: {path}"
        with Image.open(path) as image:
            assert f"{image.width}x{image.height}" == row["dimensions"]
            assert image.mode == row["mode"]


def check_sources() -> None:
    rows = tsv(HERE / "source-receipt.tsv")
    assert rows
    authority = {row["source_id"]: row for row in rows}
    assert "Working art direction" in authority["CML_LOCKS"]["role"]
    assert "active surface" in authority["GZ_SURFACE_V2"]["role"]
    assert "history only: flat rear" in authority["GZ_SURFACE_V1"]["role"]
    assert "active axial siege-shell" in authority["BREAKER_SURFACE_V4"]["role"]
    assert "residual quadruped" in authority["BREAKER_SURFACE_V3"]["role"]
    for row in rows:
        path = PROJECT / row["path"]
        assert path.is_file(), f"missing source: {path}"
        assert sha256_file(path) == row["sha256"], f"source drift: {path}"
        assert row["runtime_allowed"] == "false"


def opaque_colors(path: Path) -> set[tuple[int, int, int]]:
    with Image.open(path) as image:
        return {pixel[:3] for pixel in image.convert("RGBA").getdata() if pixel[3] > 0}


def check_palette_and_alpha() -> None:
    gz = HERE / "delivery/GUARDIAN_Z_V10X_KINETIC_FRONT_RGBA_1024.png"
    breaker = HERE / "delivery/BREAKER_BX_NONANIMAL_KINETIC_MASTER_RGBA_1400.png"
    assert len(opaque_colors(gz)) <= 11, "Guardian Z palette expanded"
    assert len(opaque_colors(breaker)) <= 8, "BREAKER palette expanded"
    for path in (gz, breaker):
        with Image.open(path) as image:
            assert image.mode == "RGBA"
            alpha = image.getchannel("A")
            assert alpha.getbbox() is not None
            assert alpha.getextrema()[0] == 0, f"missing transparent background: {path}"


def check_structure_and_scale() -> None:
    rows = tsv(HERE / "structure-keypoints.tsv")
    gz = [row for row in rows if "GZ_V10X" in row["stable_id"]]
    assert len(gz) == 40, f"expected 4x10 GZ measurements, got {len(gz)}"
    assert {row["direction"] for row in gz} == {"front", "left", "back", "right"}
    for direction in {"front", "left", "back", "right"}:
        measurements = {row["measurement"] for row in gz if row["direction"] == direction}
        assert len(measurements) == 10
    breaker = [row for row in rows if "BREAKER" in row["stable_id"]]
    assert len(breaker) == 5
    assert {row["measurement"] for row in breaker} == {
        "red_sensor", "forelimb", "dorsal_shell", "chest_seam", "upper_back_exit"
    }

    scale = {row["entity"]: row for row in tsv(HERE / "scale-pivot-contract.tsv")}
    assert scale["V353U001"]["footprint"] == "2x2"
    assert scale["ENEMY_C01_BREAKER"]["footprint"] == "3x3"
    assert scale["ENEMY_C01_RIFT_SWARM"]["footprint"] == "1x1"
    for row in scale.values():
        assert row["tile_half"] == "40,20"
        assert row["canvas_world_origin"] == "-880,-170"
        assert row["pivot"] == "bottom_center"
        assert row["runtime_allowed"] == "false"
        assert row["runtime_handoff"] == "none"


def check_hashes() -> None:
    for line in (HERE / "core-delivery-hashes.sha256").read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        assert "history-quarantine" not in relative and "/work/renderer/" not in relative, "quarantined renderer entered active hash validation"
        path = PROJECT / relative
        assert path.is_file(), f"missing hash target: {path}"
        assert sha256_file(path) == expected, f"core hash mismatch: {path}"


def main() -> None:
    check_authority()
    check_manifest()
    check_sources()
    check_palette_and_alpha()
    check_structure_and_scale()
    check_hashes()
    print("A9.1-A2 validator: PASS")


if __name__ == "__main__":
    main()
