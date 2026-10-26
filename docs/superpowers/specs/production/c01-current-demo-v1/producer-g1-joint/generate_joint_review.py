#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
EXPECTED_SIZE = (1280, 720)

PAIRS = (
    {
        "state_id": "C01CDV1_JOINT_S01_CAMB_V1",
        "art": ROOT / "art-g1/PV01_S01_EVAC_WORLD_overlay_source_cam_B_1280x720.png",
        "program": ROOT / "main-g1/BASELINE_S01_CAM_B_X845_Y716_1280x720.png",
        "overlay": OUT / "S01_CAM_B_X845_Y716_overlay50_1280x720.png",
        "side_by_side": OUT / "S01_CAM_B_X845_Y716_side_by_side_2560x720.png",
    },
    {
        "state_id": "C01CDV1_JOINT_S06_T2_STAGE1_V1",
        "art": ROOT / "art-g1/PV05_S06_TACTICAL_READ_overlay_source_t2s1_1280x720.png",
        "program": ROOT / "main-g1/BASELINE_S06_T2_STAGE1_1280x720.png",
        "overlay": OUT / "S06_T2_STAGE1_overlay50_1280x720.png",
        "side_by_side": OUT / "S06_T2_STAGE1_side_by_side_2560x720.png",
    },
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_exact(path: Path) -> Image.Image:
    with Image.open(path) as source:
        source.load()
        if source.size != EXPECTED_SIZE:
            raise RuntimeError(f"{path.name}: expected {EXPECTED_SIZE}, got {source.size}")
        return source.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for pair in PAIRS:
        art = load_exact(pair["art"])
        program = load_exact(pair["program"])

        # The contract requires an exact same-pixel 50/50 blend. No resize,
        # crop, transform, resampling, annotation, or alpha compositing occurs.
        Image.blend(art, program, 0.5).save(pair["overlay"], format="PNG")

        side_by_side = Image.new("RGB", (2560, 720))
        side_by_side.paste(art, (0, 0))
        side_by_side.paste(program, (1280, 0))
        side_by_side.save(pair["side_by_side"], format="PNG")

        print(
            "\t".join(
                (
                    pair["state_id"],
                    f"art={sha256(pair['art'])}",
                    f"program={sha256(pair['program'])}",
                    f"overlay={sha256(pair['overlay'])}",
                    f"side_by_side={sha256(pair['side_by_side'])}",
                )
            )
        )


if __name__ == "__main__":
    main()
