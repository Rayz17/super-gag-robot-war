#!/usr/bin/env python3
"""Promote user-approved C01 art and refresh manifest hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE / "art-delivery"
MANIFEST = HERE / "art-delivery-manifest.json"


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def refresh(asset: dict) -> None:
    path = ROOT / asset["delivery_path"]
    width, height = image_size(path)
    asset["width"] = width
    asset["height"] = height
    asset["sha256"] = digest(path)


def drone_asset(
    stable_id: str,
    filename: str,
    state: str,
    *,
    pivot: list[int] | None = [256, 416],
    safe_area: dict | None = None,
    runtime_allowed: bool = True,
    approval_status: str = "approved_for_runtime",
) -> dict:
    delivery = PACKAGE / "approved" / filename
    if safe_area is None and runtime_allowed:
        inset = 24 if state in {"hit", "disabled"} else 32
        safe_area = {"left": inset, "top": inset, "right": inset, "bottom": inset}
    asset = {
        "stable_id": stable_id,
        "canon_story_source": [
            "CML031",
            "ENEMY_SEAL_DRONE",
            "wanji_c01_mecha_scene_asset_contract_v1.json",
        ],
        "source_path": relative(PACKAGE / "sources" / "seal_drone_b_base_chroma_v01.png"),
        "delivery_path": relative(delivery),
        "runtime_path": (
            f"res://assets/battle_presentation/c01/seal_drone/{filename}"
            if runtime_allowed
            else None
        ),
        "width": 0,
        "height": 0,
        "pivot": pivot,
        "safe_area": safe_area,
        "alpha": "straight_srgb",
        "state": state,
        "approval_status": approval_status,
        "source_model_or_tool": (
            "OpenAI built-in imagegen; remove_chroma_key.py; "
            "Pillow identity-preserving deterministic state derivation"
        ),
        "prompt_version": "SEAL-DRONE-B-CLEAN-MASTER-v1+STATE-DERIVATIVE-v1",
        "prompt": (
            "Selected B hover archive-case identity: off-white shell, navy spine, brass joints, "
            "four folding clamp limbs, horizontal sealing slot, abstract segmented number lamp; "
            "no monster face, conventional weapons, text, or extra limbs."
        ),
        "runtime_allowed": runtime_allowed,
        "sha256": "",
    }
    refresh(asset)
    return asset


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["schema_version"] = "1.2"
    data["package_id"] = "ARTDEL_C01_GUARDIAN_Z_SEAL_DRONE_V02"
    data["generated_at"] = "2026-07-13"
    data["status_policy"].update(
        {
            "approved_as_video_reference": (
                "Composition mother frame approved, but no video output exists and runtime loading is forbidden."
            ),
            "not_selected": "Historical comparison candidate only; never load at runtime.",
        }
    )

    by_id = {asset["stable_id"]: asset for asset in data["assets"]}
    promoted = {
        "POSE_GZ_C01_KNEEL_START_V01": "half_kneel_start",
        "POSE_GZ_C01_KNEEL_CONTACT_V01": "palm_guard_contact",
        "SPR_GZ_C01_KNEEL_IDLE_V01": "half_kneel_idle",
        "SPR_GZ_C01_KNEEL_GUARD_V01": "palm_guard",
        "SPR_GZ_C01_KNEEL_RECOIL_V01": "recoil",
    }
    for stable_id, state in promoted.items():
        asset = by_id[stable_id]
        asset["delivery_path"] = asset["delivery_path"].replace("/staging/", "/approved/")
        asset["state"] = state
        asset["approval_status"] = "approved_for_runtime"
        asset["runtime_allowed"] = True
        refresh(asset)

    for stable_id in [
        "POSE_GZ_C01_KNEEL_PALM_GUARD_V01",
        "SHADOW_GZ_C01_KNEEL_V01",
        "CUTIN_DOUDENG_C01_COMMAND_V01",
        "CUTIN_DOUDENG_C01_OBSERVE_V01",
        "CUTIN_DOUDENG_C01_TENSE_V01",
        "CUTIN_DOUDENG_C01_SAFETY_LOCK_V01",
    ]:
        refresh(by_id[stable_id])

    for stable_id in [
        "VID_GZ_C01_PALM_GUARD_START_FRAME_V01",
        "VID_GZ_C01_PALM_GUARD_END_FRAME_V01",
    ]:
        asset = by_id[stable_id]
        asset["approval_status"] = "approved_as_video_reference"
        asset["runtime_allowed"] = False
        refresh(asset)

    by_id["CAND_SEAL_DRONE_RAIL_V01"]["approval_status"] = "not_selected"
    by_id["CAND_SEAL_DRONE_HOVER_ARCHIVE_V01"]["approval_status"] = "locked_current"
    by_id["CAND_SEAL_DRONE_HOVER_ARCHIVE_V01"]["state"] = "selected_candidate_history"
    by_id["CAND_SEAL_DRONE_RING_V01"]["approval_status"] = "not_selected"
    for stable_id in [
        "CAND_SEAL_DRONE_RAIL_V01",
        "CAND_SEAL_DRONE_HOVER_ARCHIVE_V01",
        "CAND_SEAL_DRONE_RING_V01",
    ]:
        by_id[stable_id]["runtime_allowed"] = False
        refresh(by_id[stable_id])

    design_master = drone_asset(
        "DESIGN_SEAL_DRONE_B_MASTER_V01",
        "design_seal_drone_b_master_v01.png",
        "locked_current",
        pivot=None,
        safe_area=None,
        runtime_allowed=False,
        approval_status="locked_current",
    )
    states = [
        drone_asset("SPR_SEAL_DRONE_C01_IDLE_V01", "sprite_seal_drone_c01_idle_v01.png", "idle"),
        drone_asset("SPR_SEAL_DRONE_C01_SCAN_V01", "sprite_seal_drone_c01_scan_v01.png", "scan"),
        drone_asset("SPR_SEAL_DRONE_C01_LOCK_V01", "sprite_seal_drone_c01_lock_v01.png", "lock"),
        drone_asset("SPR_SEAL_DRONE_C01_HIT_V01", "sprite_seal_drone_c01_hit_v01.png", "hit"),
        drone_asset(
            "SPR_SEAL_DRONE_C01_DISABLED_V01",
            "sprite_seal_drone_c01_disabled_v01.png",
            "disabled",
        ),
        drone_asset(
            "SHADOW_SEAL_DRONE_C01_V01",
            "shadow_seal_drone_c01_v01.png",
            "runtime_support",
        ),
    ]
    preserved_ids = {
        asset["stable_id"]
        for asset in [design_master, *states]
    }
    data["assets"] = [
        asset for asset in data["assets"] if asset["stable_id"] not in preserved_ids
    ] + [design_master, *states]

    data["animation_sequences"] = [
        sequence
        for sequence in data["animation_sequences"]
        if sequence["stable_id"] != "ANIM_SEAL_DRONE_C01_SCAN_LOCK_V01"
    ]
    for sequence in data["animation_sequences"]:
        sequence["approval_status"] = "approved_for_runtime"
    data["animation_sequences"].append(
        {
            "stable_id": "ANIM_SEAL_DRONE_C01_SCAN_LOCK_V01",
            "approval_status": "approved_for_runtime",
            "frames": [
                {"asset_id": "SPR_SEAL_DRONE_C01_IDLE_V01", "duration_ms": 300},
                {"asset_id": "SPR_SEAL_DRONE_C01_SCAN_V01", "duration_ms": 260},
                {"asset_id": "SPR_SEAL_DRONE_C01_LOCK_V01", "duration_ms": 480},
                {"asset_id": "SPR_SEAL_DRONE_C01_IDLE_V01", "duration_ms": 240},
            ],
            "notes": "Hit and disabled are reaction states, not forced into the scan-lock sequence.",
        }
    )

    review_paths = [
        PACKAGE / "review" / "guardian_z_c01_art_delivery_contact_sheet_v01.jpg",
        PACKAGE / "review" / "guardian_z_c01_art_delivery_contact_sheet_v02.jpg",
        PACKAGE / "review" / "seal_drone_candidate_comparison_v01.png",
        PACKAGE / "review" / "seal_drone_b_state_contact_sheet_v01.png",
        PACKAGE / "review" / "map_scale_readability_check_v01.png",
        PACKAGE / "review" / "map_scale_readability_check_v02.png",
        PACKAGE / "review" / "alpha_edge_check_v01.png",
        PACKAGE / "review" / "alpha_edge_check_v02.png",
    ]
    data["review_artifacts"] = [
        {"path": relative(path), "sha256": digest(path)} for path in review_paths
    ]
    data["video_gate"]["status"] = "mother_frames_approved_video_not_started"

    MANIFEST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
