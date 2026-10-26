#!/usr/bin/env python3
"""Seal the producer-reviewed ENV-A8 QA package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "asset-manifest.tsv"
HASHES = ROOT / "delivery-hashes.sha256"
STATUS = "producer_pass_exact_qa_only_not_final_plan"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_class(relative: str) -> str:
    if relative.startswith("qa/"):
        return "producer_visual_qa"
    if relative.startswith("receipts/"):
        return "machine_evidence"
    if relative.endswith("objective.md"):
        return "objective_contract"
    if relative == "completion-report.md":
        return "producer_completion_receipt"
    if relative.endswith(".py"):
        return "reproducible_build_tool"
    return "package_evidence"


def main() -> None:
    files = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path not in (MANIFEST, HASHES)
    )
    with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(("relative_path", "artifact_class", "status", "width", "height", "mode", "bytes", "sha256"))
        for path in files:
            relative = str(path.relative_to(ROOT))
            width = height = mode = ""
            if path.suffix.lower() == ".png":
                with Image.open(path) as image:
                    width, height = image.size
                    mode = image.mode
            writer.writerow((relative, artifact_class(relative), STATUS, width, height, mode, path.stat().st_size, sha256(path)))

    hash_files = sorted(path for path in ROOT.rglob("*") if path.is_file() and path != HASHES)
    lines = [f"{sha256(path)}  {path.relative_to(ROOT)}" for path in hash_files]
    HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"sealed {len(files)} manifest items and {len(hash_files)} hash items")


if __name__ == "__main__":
    main()
