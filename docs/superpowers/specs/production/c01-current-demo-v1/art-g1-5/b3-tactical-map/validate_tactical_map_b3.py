#!/usr/bin/env python3
"""Read-only validator for the C01E02 G1.5-B3 tactical-map package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image, ImageChops

import generate_tactical_map_b3 as gen


OUT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def alpha_extrema_in_box(image: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int]:
    return image.getchannel("A").crop(box).getextrema()


def validate_sources() -> None:
    gen.validate_sources()
    receipt = rows(OUT / "source-validation-receipt.tsv")
    require(len(receipt) == len(gen.SOURCE_LOCKS) == 34, "source receipt must contain 34 frozen sources")
    expected = {(path, ref): (blob, sha, role) for path, ref, blob, sha, role in gen.SOURCE_LOCKS}
    for row in receipt:
        key = (row["source_path"], row["frozen_ref"])
        require(key in expected, f"unexpected source receipt row: {key}")
        blob, digest, role = expected[key]
        require(row["git_blob"] == blob, f"source blob mismatch: {key}")
        require(row["sha256"] == digest, f"source sha mismatch: {key}")
        require(row["role"] == role, f"source role mismatch: {key}")
        require(row["validation"] == "PASS_exact_blob_and_sha256", f"source not PASS: {key}")
        require(row["runtime_source"] == "false", f"source incorrectly marked Runtime: {key}")

    note_by_role = {row["role"]: row["use_boundary"] for row in receipt}
    require("no Sprite Master or Runtime handoff" in note_by_role["GZ_C_scale_evidence"], "A1 boundary missing")
    require("does not yet contain approved X" in note_by_role["BREAKER_B_scale_evidence"], "B1 X boundary missing")
    require("does not yet contain approved F(D70/P30)" in note_by_role["shield_A_wall_evidence"], "B2 F boundary missing")


def validate_images() -> None:
    shared = {
        "TACTICAL_MAP_B3_direction_board_2400x1600.png": ((2400, 1600), "RGB"),
        "TACTICAL_MAP_B3_layer_contact_sheet_2200x1400.png": ((2200, 1400), "RGB"),
        "TACTICAL_MAP_B3_geometry_alignment_overlay_1280x720.png": ((1280, 720), "RGBA"),
    }
    for filename, (size, mode) in shared.items():
        with Image.open(OUT / filename) as image:
            require(image.size == size, f"wrong size: {filename}")
            require(image.mode == mode, f"wrong mode: {filename}")

    for candidate in gen.CANDIDATES:
        expected = {
            "base": "RGB",
            "foreground": "RGBA",
            "fade": "L",
            "shield_wall": "RGBA",
            "shield_empty": "RGBA",
            "weather": "RGBA",
            "readability": "RGB",
        }
        opened: dict[str, Image.Image] = {}
        try:
            for key, mode in expected.items():
                image = Image.open(OUT / gen.layer_file(candidate, key))
                image.load()
                opened[key] = image
                require(image.size == (gen.WIDTH, gen.HEIGHT), f"wrong canvas: MAP-{candidate.code} {key}")
                require(image.mode == mode, f"wrong mode: MAP-{candidate.code} {key}")

            fg = opened["foreground"]
            fade = opened["fade"]
            require(fg.getchannel("A").getextrema()[1] > 0, f"empty foreground: MAP-{candidate.code}")
            require(fade.getextrema()[1] > 0, f"empty fade mask: MAP-{candidate.code}")

            # Foreground art cannot cover program-owned chrome or its protected gap.
            clear_boxes = {
                "top_hud": (0, 0, gen.WIDTH, 55),
                "bottom_hud": (0, 648, gen.WIDTH, gen.HEIGHT),
                "ui_gap": (852, 54, 885, 648),
                "intent_panel": (885, 78, 1241, 197),
                "command_panel": (885, 210, 1241, 625),
            }
            for label, box in clear_boxes.items():
                require(alpha_extrema_in_box(fg, box)[1] == 0, f"MAP-{candidate.code} foreground invades {label}")

            effective = gen.apply_occlusion_fade(fg, fade)
            board_overlap = ImageChops.multiply(fg.getchannel("A"), gen.board_mask()).getextrema()[1]
            effective_overlap = ImageChops.multiply(effective.getchannel("A"), gen.board_mask()).getextrema()[1]
            require(board_overlap > 0, f"MAP-{candidate.code} must demonstrate in-board soft fade")
            require(effective_overlap < board_overlap, f"MAP-{candidate.code} in-board foreground was not faded")

            # Locked interaction and unit evidence must remain unobscured.
            critical = {
                "hotspot": (gen.HOTSPOT_CENTER[0] - 18, gen.HOTSPOT_CENTER[1] - 18,
                            gen.HOTSPOT_CENTER[0] + 19, gen.HOTSPOT_CENTER[1] + 19),
                "guardian_z": (gen.GZ_BBOX[0], gen.GZ_BBOX[1], gen.GZ_BBOX[2] + 1, gen.GZ_BBOX[3] + 1),
                "breaker": (gen.BREAKER_BBOX[0], gen.BREAKER_BBOX[1], gen.BREAKER_BBOX[2] + 1, gen.BREAKER_BBOX[3] + 1),
                "impact": (gen.IMPACT_BBOX[0], gen.IMPACT_BBOX[1], gen.IMPACT_BBOX[2] + 1, gen.IMPACT_BBOX[3] + 1),
            }
            for label, box in critical.items():
                require(alpha_extrema_in_box(effective, box)[1] <= 72, f"MAP-{candidate.code} obscures {label}")

            wall_alpha = opened["shield_wall"].getchannel("A")
            empty_alpha = opened["shield_empty"].getchannel("A")
            hx, hy = gen.HOTSPOT_CENTER
            require(wall_alpha.getpixel((hx, hy)) > 0, f"MAP-{candidate.code} wall shield missing at hotspot")
            require(empty_alpha.getpixel((hx, hy)) == 0, f"MAP-{candidate.code} empty mount still contains shield body")
            require(ImageChops.difference(wall_alpha, empty_alpha).getbbox() is not None,
                    f"MAP-{candidate.code} shield states are identical")
        finally:
            for image in opened.values():
                image.close()


def validate_geometry_and_tables() -> None:
    candidate_rows = rows(OUT / "candidate-spec.tsv")
    require(len(candidate_rows) == 3, "candidate-spec must contain MAP-A/B/C")
    signatures = {row["geometry_signature"] for row in candidate_rows}
    require(signatures == {gen.GEOMETRY_SIGNATURE}, "candidate geometry signatures differ")
    require({row["candidate_code"] for row in candidate_rows} == {"MAP-A", "MAP-B", "MAP-C"}, "candidate set mismatch")
    for row in candidate_rows:
        require(row["stable_state"] == gen.STABLE_STATE, "stable state mismatch")
        require(row["profile_id"] == gen.PROFILE_ID, "profile mismatch")
        require(row["blocked_cell_topology"] == "none", "blocked topology was introduced")
        require(row["lifecycle"] == "Candidate", "candidate lifecycle mismatch")
        require(row["runtime_allowed"] == "false", "candidate runtime gate opened")
        require(row["runtime_handoff"] == "none", "candidate runtime handoff opened")

    cell_rows = rows(OUT / "cell-visual-audit.tsv")
    require(len(cell_rows) == 108, "cell audit must contain exactly 108 rows")
    seen: set[tuple[int, int]] = set()
    for row in cell_rows:
        x, y = int(row["x"]), int(row["y"])
        require(0 <= x < 12 and 0 <= y < 9, f"cell out of range: {(x, y)}")
        require((x, y) not in seen, f"duplicate cell: {(x, y)}")
        seen.add((x, y))
        require((int(row["center_x"]), int(row["center_y"])) == gen.cell_center(x, y), f"cell center mismatch: {(x, y)}")
        expected_polygon = ";".join(f"{px},{py}" for px, py in gen.cell_polygon(x, y))
        require(row["polygon"] == expected_polygon, f"cell polygon mismatch: {(x, y)}")
        require(row["blocked"] == "false", f"blocked cell introduced: {(x, y)}")
        require(row["movement_semantic"] == "uniform_ground", f"terrain semantic changed: {(x, y)}")
        require(row["collision_semantic"] == "none", f"collision introduced: {(x, y)}")
        require(row["shield_hotspot"] == str((x, y) == gen.HOTSPOT).lower(), f"hotspot mismatch: {(x, y)}")
        require(row["impact_affected"] == str(5 <= x <= 7 and 0 <= y <= 5).lower(), f"impact mismatch: {(x, y)}")
    require(seen == {(x, y) for y in range(9) for x in range(12)}, "cell audit coverage incomplete")

    layer_rows = rows(OUT / "map-layer-spec.tsv")
    require(len(layer_rows) == 21, "map-layer-spec must contain 7 layers x 3 candidates")
    for row in layer_rows:
        require(row["runtime_allowed"] == "false", f"layer runtime gate opened: {row['layer_id']}")
        require(row["runtime_handoff"] == "none", f"layer handoff opened: {row['layer_id']}")
        require(row["geometry_signature"] == gen.GEOMETRY_SIGNATURE, f"layer geometry mismatch: {row['layer_id']}")
        require(row["collision_semantic"] == "none", f"layer collision introduced: {row['layer_id']}")
        require("grid" in row["program_owned_not_baked"] and "menu" in row["program_owned_not_baked"],
                f"program ownership boundary missing: {row['layer_id']}")
    for candidate in gen.CANDIDATES:
        shield_rows = [
            row for row in layer_rows
            if row["candidate_id"] == candidate.stable_id and row["layer_kind"] in ("shield_wall", "shield_empty")
        ]
        require(len(shield_rows) == 2, f"shield state pair missing: MAP-{candidate.code}")
        require({row["mutual_exclusion_group"] for row in shield_rows} == {"shield_state"},
                f"shield mutual exclusion missing: MAP-{candidate.code}")

    # Geometry-only overlay carries exact program lock evidence without report text.
    with Image.open(OUT / "TACTICAL_MAP_B3_geometry_alignment_overlay_1280x720.png") as overlay:
        require(overlay.mode == "RGBA", "geometry overlay must be RGBA")
        alpha = overlay.getchannel("A")
        for y in range(9):
            for x in range(12):
                require(alpha.getpixel(gen.cell_center(x, y)) > 0, f"geometry overlay misses center {(x, y)}")
        require(alpha.getpixel(gen.HOTSPOT_CENTER) > 0, "geometry overlay misses hotspot center")
        require(alpha.crop((852, 54, 885, 648)).getextrema()[1] > 0, "geometry overlay misses UI gap")


def validate_manifest_and_hashes() -> None:
    manifest = rows(OUT / "asset-manifest.tsv")
    require(manifest, "empty asset manifest")
    listed = set()
    for row in manifest:
        path = OUT / row["relative_path"]
        require(path.is_file(), f"manifest file missing: {path.name}")
        require(row["relative_path"] not in listed, f"duplicate manifest file: {path.name}")
        listed.add(row["relative_path"])
        require(row["lifecycle"] == "Candidate", f"manifest lifecycle mismatch: {path.name}")
        require(row["runtime_allowed"] == "false", f"manifest runtime gate opened: {path.name}")
        require(row["runtime_handoff"] == "none", f"manifest handoff opened: {path.name}")
        require(row["scope"] == "C01E02_G1.5_B3_only", f"manifest scope mismatch: {path.name}")
        require(row["sha256"] == sha256(path), f"manifest sha mismatch: {path.name}")

    required_manifest_entries = {
        "generate_tactical_map_b3.py", "validate_tactical_map_b3.py",
        "candidate-spec.tsv", "map-layer-spec.tsv", "cell-visual-audit.tsv",
        "source-validation-receipt.tsv", "user-decision-card.md", "completion-report.md",
    }
    require(required_manifest_entries <= listed, "manifest omits required delivery files")

    hash_lines = (OUT / "delivery-hashes.sha256").read_text(encoding="utf-8").splitlines()
    hashed = set()
    for line in hash_lines:
        digest, filename = line.split("  ", 1)
        path = OUT / filename
        require(path.is_file(), f"hash file entry missing: {filename}")
        require(digest == sha256(path), f"delivery hash mismatch: {filename}")
        hashed.add(filename)
    expected = {
        path.name for path in OUT.iterdir()
        if path.is_file() and path.name not in {"delivery-hashes.sha256", "BLOCKED.md", ".DS_Store"}
        and path.suffix != ".pyc"
    }
    require(hashed == expected, "delivery hash coverage mismatch")

    forbidden_suffixes = (".mp4", ".mov", ".webm", ".godot", ".tscn", ".tres")
    for path in OUT.iterdir():
        require(not path.name.startswith("B4"), f"forbidden B4 output: {path.name}")
        require(path.suffix.lower() not in forbidden_suffixes, f"forbidden output type: {path.name}")
    require(not (OUT / "BLOCKED.md").exists(), "B3 was marked blocked")


def main() -> None:
    validate_sources()
    validate_images()
    validate_geometry_and_tables()
    validate_manifest_and_hashes()
    print("PASS: C01E02 G1.5-B3 tactical-map Candidate package")
    print(f"geometry_signature={gen.GEOMETRY_SIGNATURE}")
    print("runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
