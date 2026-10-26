#!/usr/bin/env python3
"""Build the A6 Candidate asset manifest from files already in the delivery root."""

from __future__ import annotations

import hashlib
import re
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_DOCS = [
    "portrait-spec.tsv",
    "review-layout-spec.tsv",
    "source-validation-receipt.tsv",
    "source-rights-receipt.md",
    "generation-prompts.md",
    "user-decision-card.md",
    "completion-report.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def png_info(path: Path) -> tuple[str, str]:
    data = path.read_bytes()[:33]
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    if bit_depth != 8:
        raise ValueError(f"expected 8-bit PNG: {path}")
    return f"{width}x{height}", "true" if color_type in (4, 6) else "false"


def asset_id(path: str) -> str:
    known = {
        "assets/atlases/r05-portrait-jicun-states-2304x768.png": "R05_PORTRAIT_JICUN",
        "assets/atlases/r05-portrait-qihai-remote-states-2304x768.png": "R05_PORTRAIT_QIHAI_REMOTE",
        "assets/atlases/r05-comms-old-guardian-states-3072x768.png": "R05_COMMS_OLD_GUARDIAN",
        "simulations/jicun-doudeng-local-1280x720.png": "A6_SIM_JICUN_DOUDENG_LOCAL",
        "simulations/jicun-qihai-remote-presence-1280x720.png": "A6_SIM_JICUN_QIHAI_REMOTE_PRESENCE",
        "simulations/jicun-old-guardian-machine-1280x720.png": "A6_SIM_JICUN_OLD_GUARDIAN_MACHINE",
    }
    if path in known:
        return known[path]
    token = re.sub(r"[^A-Za-z0-9]+", "_", path).strip("_").upper()
    return f"A6_{token}"


def subject(path: str) -> str:
    if "qihai" in path:
        return "CH_QIHAI"
    if "jicun" in path:
        return "CH_JICUN"
    if "old_guardian" in path or "old-guardian" in path:
        return "CH002;V353U001"
    if "doudeng" in path:
        return "CH001"
    return "A6_PACKAGE"


def role(path: str) -> str:
    if "/atlases/" in f"/{path}":
        return "candidate_state_atlas"
    if path.startswith("assets/portraits/") or path.startswith("assets/comms/"):
        return "candidate_state_master_or_review_composite"
    if path.startswith("source-layers/"):
        return "editable_source_layer"
    if path.startswith("sources/chroma/") and "rejected" in path:
        return "rejected_trace_source"
    if path.startswith("sources/chroma/"):
        return "imagegen_keyed_source"
    if path.startswith("sources/references/"):
        return "read_only_identity_reference_copy_or_crop"
    if path.startswith("boards/"):
        return "review_board"
    if path.startswith("simulations/"):
        return "review_simulation"
    if path.startswith("scripts/"):
        return "reproducibility_or_validator"
    return "delivery_evidence"


def source_tool(path: str) -> str:
    if path.startswith("sources/chroma/"):
        return "openai_builtin_imagegen"
    if path.startswith("sources/references/"):
        return "project_frozen_source_copy_or_crop"
    if path.endswith(".png"):
        return "ffmpeg"
    return "codex_apply_patch"


def source_ref(path: str) -> str:
    refs = ["36_A6_OBJECTIVE", "41_PACKING_CORRECTION", "42_MEDIA_PACKING_V2"]
    if "jicun" in path:
        refs.append("VIS_CML001_CURRENT_BASE")
    if "qihai" in path:
        refs.extend(["VIS_CML002_003_004_CURRENT_BASE", "44_QIHAI_REMOTE_INTERFACE"])
    if "old_guardian" in path or "old-guardian" in path:
        refs.extend(["VIS_CML008_CURRENT_BASE", "CANON_CH002"])
    if "doudeng" in path:
        refs.extend(["CUTIN_DOUDENG_C01_OBSERVE_V01", "CUTIN_DOUDENG_C01_TENSE_V01"])
    if path.startswith("simulations/"):
        refs.append("A4_MAP_B_PURE_READ_NO_UI")
    return ";".join(refs)


def rights_note(path: str) -> str:
    if path.startswith("sources/chroma/"):
        return "generated_candidate_from_project_identity_reference;producer_rights_review_pending"
    if path.startswith("sources/references/"):
        return "project_provided_read_only_identity_reference;no_new_title_claim"
    if "doudeng" in path and (path.startswith("boards/") or path.startswith("simulations/")):
        return "review_composite_contains_project_approved_Doudeng_and_A4;not_new_runtime_master"
    if path.startswith("simulations/"):
        return "review_composite_contains_project_approved_A4_and_generated_candidate_characters"
    if path.endswith(".png"):
        return "derived_from_generated_candidate_or_project_review_source;producer_rights_review_pending"
    return "project_delivery_documentation"


def forbidden_states(path: str) -> str:
    values = ["runtime_binding", "auto_handoff", "canon_promotion", "stable_id_reuse_without_u1"]
    if "qihai" in path:
        values.extend(["dialogue_consumer", "interactive_card", "artillery_authority", "open_mouth_command_read"])
    if "doudeng" in path:
        values.extend(["source_crop", "source_overwrite", "new_Doudeng_master", "stable_id_impersonation"])
    if "old_guardian" in path or "old-guardian" in path:
        values.extend(["human_avatar", "independent_ai_body", "copyable_assistant"])
    if "rejected" in path:
        values.append("active_consumer")
    return ";".join(values)


def collect_files() -> list[Path]:
    paths: list[Path] = []
    for folder in ("assets", "source-layers", "sources", "boards", "simulations"):
        paths.extend(path for path in (ROOT / folder).rglob("*.png") if path.is_file())
    paths.extend(path for path in (ROOT / "scripts").glob("*.py") if path.is_file())
    paths.extend(ROOT / name for name in ROOT_DOCS if (ROOT / name).is_file())
    return sorted(set(paths), key=lambda item: item.relative_to(ROOT).as_posix())


def main() -> None:
    header = [
        "package_id",
        "asset_id",
        "path",
        "subject",
        "media_type",
        "dimensions",
        "alpha_channel",
        "role",
        "source_tool",
        "source_ref",
        "rights_note",
        "forbidden_states",
        "lifecycle",
        "runtime_allowed",
        "runtime_handoff",
        "sha256",
    ]
    rows = ["\t".join(header)]
    for file_path in collect_files():
        relative = file_path.relative_to(ROOT).as_posix()
        suffix = file_path.suffix.lower()
        if suffix == ".png":
            media_type = "image/png"
            dimensions, alpha = png_info(file_path)
        elif suffix == ".tsv":
            media_type, dimensions, alpha = "text/tab-separated-values", "n/a", "n/a"
        elif suffix == ".md":
            media_type, dimensions, alpha = "text/markdown", "n/a", "n/a"
        else:
            media_type, dimensions, alpha = "text/x-python", "n/a", "n/a"
        row = [
            "C01CDV1_A6_CHARACTER_COMMS_UI_R05_CANDIDATE",
            asset_id(relative),
            relative,
            subject(relative),
            media_type,
            dimensions,
            alpha,
            role(relative),
            source_tool(relative),
            source_ref(relative),
            rights_note(relative),
            forbidden_states(relative),
            "Candidate",
            "false",
            "none",
            sha256(file_path),
        ]
        rows.append("\t".join(row))
    (ROOT / "asset-manifest.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"A6_MANIFEST_REBUILT rows={len(rows) - 1}")


if __name__ == "__main__":
    main()
