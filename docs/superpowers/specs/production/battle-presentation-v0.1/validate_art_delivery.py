#!/usr/bin/env python3
"""Validate the C01 Guardian Z art-delivery manifest and raster contracts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[5]
MANIFEST = Path(__file__).resolve().parent / "art-delivery-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []
    asset_ids = {asset["stable_id"] for asset in data["assets"]}

    for asset in data["assets"]:
        asset_id = asset["stable_id"]
        path = ROOT / asset["delivery_path"]
        if not path.exists():
            errors.append(f"{asset_id}: missing {path}")
            continue
        if sha256(path) != asset["sha256"]:
            errors.append(f"{asset_id}: sha256 mismatch")

        with Image.open(path) as image:
            if image.size != (asset["width"], asset["height"]):
                errors.append(f"{asset_id}: size {image.size} != {(asset['width'], asset['height'])}")

            alpha_kind = asset["alpha"]
            if alpha_kind.startswith("straight"):
                if "A" not in image.getbands():
                    errors.append(f"{asset_id}: missing alpha channel")
                    continue
                alpha = image.getchannel("A")
                corners = [alpha.getpixel((0, 0)), alpha.getpixel((image.width - 1, 0)), alpha.getpixel((0, image.height - 1)), alpha.getpixel((image.width - 1, image.height - 1))]
                if any(corners):
                    errors.append(f"{asset_id}: non-transparent corner {corners}")

                bbox = alpha.getbbox()
                safe = asset.get("safe_area")
                if bbox and safe:
                    left, top, right, bottom = bbox
                    if left < safe["left"] or top < safe["top"]:
                        errors.append(f"{asset_id}: visible bbox {bbox} enters left/top safe area {safe}")
                    if right > image.width - safe["right"] or bottom > image.height - safe["bottom"]:
                        errors.append(f"{asset_id}: visible bbox {bbox} enters right/bottom safe area {safe}")

                rgba = image.convert("RGBA")
                magenta = 0
                for red, green, blue, alpha_value in rgba.get_flattened_data():
                    if alpha_value > 16 and red > 205 and blue > 205 and green < 110:
                        magenta += 1
                if magenta > 8:
                    warnings.append(f"{asset_id}: {magenta} visible magenta-like pixels require visual review")

        if asset["runtime_allowed"] and asset["approval_status"] != "approved_for_runtime":
            errors.append(f"{asset_id}: runtime_allowed without approved_for_runtime")
        if "chroma" in asset["delivery_path"] and asset["runtime_allowed"]:
            errors.append(f"{asset_id}: chroma source cannot be runtime_allowed")

    for sequence in data.get("animation_sequences", []):
        for frame in sequence["frames"]:
            if frame["asset_id"] not in asset_ids:
                errors.append(f"{sequence['stable_id']}: unknown frame asset {frame['asset_id']}")

    for artifact in data.get("review_artifacts", []):
        path = ROOT / artifact["path"]
        if not path.exists():
            errors.append(f"review artifact missing: {path}")
        elif sha256(path) != artifact["sha256"]:
            errors.append(f"review artifact sha256 mismatch: {path}")

    print(f"assets_checked={len(data['assets'])}")
    print(f"warnings={len(warnings)}")
    for warning in warnings:
        print(f"WARN {warning}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
