#!/usr/bin/env python3
"""Build A8 Phase A truth evidence without changing any source asset."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = next(path for path in [HERE, *HERE.parents] if (path / ".git").exists())
PACKAGE_ID = "C01CDV1_A8_PHASE_A_CURRENT_TRUTH_V1"

BG = (5, 18, 25, 255)
PANEL = (12, 31, 40, 255)
PANEL_ALT = (17, 39, 48, 255)
LINE = (56, 92, 102, 255)
TEXT = (225, 236, 235, 255)
MUTED = (142, 164, 166, 255)
CYAN = (95, 194, 194, 255)
GOLD = (225, 180, 68, 255)
CORAL = (231, 100, 91, 255)
GREEN = (100, 196, 164, 255)
PURPLE = (184, 137, 207, 255)

FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
]
FONT_PATH = next(path for path in FONT_CANDIDATES if path.exists())


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


SOURCES = {
    "contract_48": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/48-c01e02-m3-j1-current-art-and-gameplay-joint-producer-plan.md",
        "06592d45483496247f915313fd22b6f28a4b392b1a073e2960f271d0af16eb35",
        "producer_plan",
    ),
    "objective_49": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/49-c01e02-a8-current-visual-pack-and-u1-objective.md",
        "4d4f79720fe2eaebbdeafc215810457310d83b3c97f4ae413e62e76d5c0fc651",
        "a8_objective",
    ),
    "snapshot_09b": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/09b-frozen-visual-snapshot.tsv",
        "4eec352ef11b7f6706559c2d7f3285136dba6781e4892066718696795dd89713",
        "frozen_visual_snapshot",
    ),
    "packing_42": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/42-c01e02-m3-r0-5-media-packing-v2.json",
        "fe75667eac656756e35ddbbb784e250d39c0f8b05c2c14f719234d653b944012",
        "media_packing_contract",
    ),
    "a7_review_45": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/45-c01e02-m3-r0-5-a7-identity-lock-producer-review.md",
        "a90314f6357d18874e78c56312412e4253badc1365a8710e6c723471a064ca57",
        "a7_producer_review",
    ),
    "a4_approval": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-a4/a4-user-approval-receipt.tsv",
        "dc402de8ee471953fa1de8b98676aa76a9826a2b219dc6010ba7e762f128781b",
        "user_approval_receipt",
    ),
    "a5_approval": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-a5/a5-user-approval-receipt.tsv",
        "45c1687c3fdbdd87d7f9e872933b48925871f680eeaa0095d360623ad1a34f75",
        "user_approval_receipt",
    ),
    "a1_approval": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv",
        "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee",
        "user_direction_receipt",
    ),
    "b1_approval": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv",
        "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920",
        "user_direction_receipt",
    ),
    "b2_approval": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b2-user-approval-receipt.tsv",
        "792d9061b804ec3d87d79c777171f5aa4bd44979416c40d45d8968a2004d0c51",
        "user_direction_receipt",
    ),
    "a6_manifest": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a6-character-comms-ui/asset-manifest.tsv",
        "34155c16651266251e9e40ddb8624ee3b6a1af92891b966a41c711299b2755fb",
        "a6_candidate_manifest",
    ),
    "a6_core_hashes": (
        ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a6-character-comms-ui/core-delivery-hashes.sha256",
        "6f3d4b05b1ee17aadc2424ec7ac0e922cccde99e378e0da804ab8daa22021bcd",
        "a6_core_hashes",
    ),
}


A6_ROOT = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a6-character-comms-ui"
JICUN_ANCHOR = A6_ROOT / "sources/references/jicun-identity-reference.png"
QIHAI_ANCHOR = A6_ROOT / "sources/references/qihai-identity-reference-crop.png"
GUARDIAN_LEGACY_ANCHOR = A6_ROOT / "sources/references/guardian-z-head-chest-reference-crop.png"
GUARDIAN_E02_MASTER = ROOT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png"
GUARDIAN_WING_CANDIDATE = ROOT / "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_a_a3_shoulder_preserved_hybrid_front_candidate_v21.png"
JICUN_ATLAS = A6_ROOT / "assets/atlases/r05-portrait-jicun-states-2304x768.png"
QIHAI_ATLAS = A6_ROOT / "assets/atlases/r05-portrait-qihai-remote-states-2304x768.png"
GUARDIAN_ATLAS = A6_ROOT / "assets/atlases/r05-comms-old-guardian-states-3072x768.png"
DOUDENG_LAYOUT = A6_ROOT / "boards/doudeng-approved-layout-board-1280x720.png"
DOUDENG_OBSERVE = ROOT / "docs/superpowers/specs/production/battle-presentation-v0.1/art-delivery/approved/cutin_doudeng_c01_observe_v01.png"
DOUDENG_TENSE = ROOT / "docs/superpowers/specs/production/battle-presentation-v0.1/art-delivery/approved/cutin_doudeng_c01_tense_v01.png"

IMAGE_EXPECTED = {
    JICUN_ANCHOR: "3e624ba9b65a712855f71c72c3ce57238719ffb83718bf2e8a495c89384bca6c",
    QIHAI_ANCHOR: "85aba44e446f0b4f8dafff3f3b2ba139edf983003c733e4034f8a87f4ba8038f",
    GUARDIAN_LEGACY_ANCHOR: "7b07792b3adcef17029406c5e84c0e79325c2e4ef71094aa6c65f92064fed596",
    GUARDIAN_E02_MASTER: "e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade",
    GUARDIAN_WING_CANDIDATE: "e0029c0a4f6621349689288a2a2d87c0f7b2c5a33db93cce2564fe2edfb9882c",
    JICUN_ATLAS: "d6ec72d6976f532cfde707902231de3df5633d17aca66116710e4fa72b67622e",
    QIHAI_ATLAS: "477f0873c6bdda04dde1312c49d57aaf53b1f2f6337023269290c5f87edbf67f",
    GUARDIAN_ATLAS: "41dd29862ed0a2be873dbaac580c4269c4ad3161156834021812c5a0b1a7e4be",
    DOUDENG_LAYOUT: "9eb780435ac52d2d2c3f99d57001e757222f1a7403ab5efdaf006c523174a0a6",
    DOUDENG_OBSERVE: "b8530e98b9d76edb9275680488558167ad368697fe6f55a3af00ac5492196d3a",
    DOUDENG_TENSE: "c846e48b04b7d8671fd4853330487d0f39d1df98a70550d1f03d49770a26f159",
}


TRUTH_ROWS = [
    {
        "stable_id": "R05_MAP_BASE+BUILDINGS+ROOFS+FOREGROUND+OCCLUSION_MASK",
        "subject": "A4 MAP-B five static layers",
        "canon_art_level": "Candidate source; producer exact handoff exists for M2",
        "current_identity_anchor": "A4 MAP-B / 40x20 projection / user-approved six-layer package",
        "existing_user_decision": "身份、质感、六层滚动、遮挡、状态通过；核心层可作 Demo 派生源",
        "current_candidate": "art-a4-map-b-six-layer/A4_MAP_B_*_2400x1350.png",
        "alignment_status": "approved_source_consistent",
        "demo_use": "scrolling district world layers",
        "next_action": "producer rebinds original bytes for M3-J1; art does not repaint",
        "lifecycle": "Candidate derivative source approved",
        "runtime_allowed": "false",
        "runtime_handoff": "M2 exact only; M3-J1 none",
        "evidence_paths": "producer-a4/a4-user-approval-receipt.tsv;art-a4-map-b-six-layer/asset-manifest.tsv",
    },
    {
        "stable_id": "R05_RIFT_SWARM_IDLE_4DIR",
        "subject": "A5 small rift swarm 96px atlas",
        "canon_art_level": "Candidate source; producer exact handoff exists for M2",
        "current_identity_anchor": "A / 伏壳钳足型; north-east-south-west; bottom_center",
        "existing_user_decision": "四向、接地点、红缝、扑击端通过；选择96；六实例共用母版",
        "current_candidate": "art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png",
        "alignment_status": "approved_source_consistent",
        "demo_use": "1x1 small enemy idle four-facing",
        "next_action": "producer rebinds original bytes for M3-J1; light variance deferred",
        "lifecycle": "Candidate exact handoff source approved",
        "runtime_allowed": "false",
        "runtime_handoff": "M2 exact only; M3-J1 none",
        "evidence_paths": "producer-a5/a5-user-approval-receipt.tsv",
    },
    {
        "stable_id": "R05_PORTRAIT_JICUN",
        "subject": "纪存 three-state portrait atlas",
        "canon_art_level": "CML001 Hard identity lock; A6 Candidate",
        "current_identity_anchor": "black hair; blue eyes; no glasses; navy museum coat; wrist archive terminal",
        "existing_user_decision": "Current identity locked; A6 not yet U1-approved",
        "current_candidate": "art-a6-character-comms-ui/assets/atlases/r05-portrait-jicun-states-2304x768.png",
        "alignment_status": "identity_consistent; focused/alarm separation subtle; U1 pending",
        "demo_use": "route, people and city judgment portrait",
        "next_action": "user approves or requests a narrow state revision",
        "lifecycle": "Candidate",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "CML001;09b VIS_CML001_CURRENT_BASE;A6 manifest",
    },
    {
        "stable_id": "R05_PORTRAIT_QIHAI_REMOTE",
        "subject": "七海 remote three-state atlas",
        "canon_art_level": "CML004 Hard identity lock; A6 Candidate",
        "current_identity_anchor": "mature Japanese woman; dark straight hair; cold-white legal uniform; restrained authority",
        "existing_user_decision": "Current identity locked; A6 not yet U1-approved",
        "current_candidate": "art-a6-character-comms-ui/assets/atlases/r05-portrait-qihai-remote-states-2304x768.png",
        "alignment_status": "identity_consistent; decision mouth closed; U1 pending",
        "demo_use": "remote presence card only; no battle command authority",
        "next_action": "user confirms presence-card reading and three states",
        "lifecycle": "Candidate",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "CML004;09b VIS_CML002_003_004_CURRENT_BASE;A6 manifest",
    },
    {
        "stable_id": "R05_COMMS_OLD_GUARDIAN",
        "subject": "旧守护者 three-state machine comms atlas",
        "canon_art_level": "CH002 Working identity + legacy CML008 Hard anchor; V10X later E02 production source; A6 Candidate",
        "current_identity_anchor": "V10X/W-X Guardian Z head/chest; chest light; speaker waveform; same subject",
        "existing_user_decision": "old guardian equals Guardian Z; W positive parent; V10X frozen for E02 visual use; CML008 not migrated",
        "current_candidate": "art-a6-character-comms-ui/assets/atlases/r05-comms-old-guardian-states-3072x768.png",
        "alignment_status": "identity_source_drift: A6 derived from legacy 09b body; cannot approve unchanged",
        "demo_use": "guide/contact/shield-gaze machine comms",
        "next_action": "narrow rederive three states from V10X head/chest, then return to U1",
        "lifecycle": "Candidate",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "CH002;CML008;09b legacy anchor;V10X SHA e1d6b00d...;A6 manifest;49 line 24",
    },
    {
        "stable_id": "CUTIN_DOUDENG_C01_OBSERVE_V01 + TENSE_V01",
        "subject": "兜灯 existing two full-width cut-ins",
        "canon_art_level": "CML002 Hard identity; existing approved_for_runtime sources",
        "current_identity_anchor": "Chinese maintenance engineer; headlamp/goggles; tools and machine-condition responsibility",
        "existing_user_decision": "two original 1920x640 sources already approved_for_runtime",
        "current_candidate": "A6 review adaptation only; originals unchanged and uncropped",
        "alignment_status": "source_preserved; layout adaptation U1 pending",
        "demo_use": "local machine-condition observe/tense presentation",
        "next_action": "user confirms fit or opens a separate new-Doudeng task",
        "lifecycle": "original locked current; A6 board Candidate",
        "runtime_allowed": "original true; A6 board false",
        "runtime_handoff": "M3-J1 cross-lane rebind pending producer",
        "evidence_paths": "CML002;battle-presentation art-delivery-manifest.json;A6 layout board",
    },
    {
        "stable_id": "R05_GUARDIAN_MAP_ACTION_4DIR",
        "subject": "馆守Z map action atlas",
        "canon_art_level": "legacy CML008 Hard identity cross-check; V10X latest E02 body source; A1-C action direction approved only",
        "current_identity_anchor": "V10X/W-X body: layered gold crown; red crest; blue brow; silver grille; red X chest; gold core; thick upper body; equal cylinder forearms",
        "existing_user_decision": "W positive parent; V10X E02 source frozen; C action skeleton approved; V21 wing mount remains separate Candidate",
        "current_candidate": "missing true 1280x1024 atlas",
        "alignment_status": "missing_master",
        "demo_use": "player-controlled 5 actions x 4 directions",
        "next_action": "Phase B one-facing keyframe + A4 scale board; stop for user",
        "lifecycle": "Candidate direction only",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "CML008;V10X SHA e1d6b00d...;V21 SHA e0029c0a...;producer-g1-5/a1-user-approval-receipt.tsv",
    },
    {
        "stable_id": "R05_BREAKER_MAP_ACTION_4DIR",
        "subject": "BREAKER map action atlas",
        "canon_art_level": "Working text identity; B silhouette + X surface approved",
        "current_identity_anchor": "forelimb-bearing semi-upright; giant back shell; low head block; single red seam; closed chest seam",
        "existing_user_decision": "B + X + current three-point closed relation approved",
        "current_candidate": "missing true 960x1280 atlas",
        "alignment_status": "missing_master",
        "demo_use": "boss idle/charge/contact x 4 directions",
        "next_action": "Phase B one-facing keyframe + A4 scale board; stop for user",
        "lifecycle": "Candidate direction only",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "producer-g1-5/b1-user-approval-receipt.tsv",
    },
    {
        "stable_id": "R05_SHIELD_WALL_HUNG",
        "subject": "retired wall-hung shield",
        "canon_art_level": "Working scene prop; A silhouette + F-D70/P30 approved",
        "current_identity_anchor": "high narrow tower shield; 70% retired defense heavy armor; 30% port repair; three old scorches",
        "existing_user_decision": "A; F-D70/P30; four-state continuity approved",
        "current_candidate": "final A+F 256x256 wall-hung master missing",
        "alignment_status": "missing_master",
        "demo_use": "wall-hung cold state before acquisition",
        "next_action": "Phase B one-facing keyframe + A4 scale board; stop for user",
        "lifecycle": "Candidate direction only",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "producer-g1-5/b2-user-approval-receipt.tsv",
    },
    {
        "stable_id": "R05_VEHICLE_EAST_MOVE",
        "subject": "neutral emergency vehicle east-only atlas",
        "canon_art_level": "Working scene need; no current art master",
        "current_identity_anchor": "neutral emergency vehicle; no medical cross, ambulance identity or baked text",
        "existing_user_decision": "none; must be shown and confirmed in this art task",
        "current_candidate": "missing 512x128 atlas",
        "alignment_status": "missing_design",
        "demo_use": "last evacuation vehicle movement",
        "next_action": "Phase B one-facing keyframe + A4 scale board; stop for user",
        "lifecycle": "not yet produced",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "48 plan;49 objective;42 packing",
    },
    {
        "stable_id": "R05_CUTIN_GIANT_CONTACT",
        "subject": "representative giant contact cut-in",
        "canon_art_level": "A7 Candidate; producer identity derivation only",
        "current_identity_anchor": "Current Guardian Z crown/face/chest/shoulder/forearm identity + B/X BREAKER",
        "existing_user_decision": "not requested; not granted",
        "current_candidate": "art-a7-round-presentation/cutin/R05_CUTIN_GIANT_CONTACT_1600x900.png",
        "alignment_status": "identity_drift_guardian_z; cannot approve current version",
        "demo_use": "single representative contact cut-in",
        "next_action": "Phase C narrow Guardian Z identity repair; preserve composition; U1 required",
        "lifecycle": "Candidate",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "45 producer review;49 objective;A7 validator",
    },
    {
        "stable_id": "R05_FX_CONTACT_DUST + ARTILLERY_HIT + RED_CHARGE",
        "subject": "A7 limited reusable FX",
        "canon_art_level": "A7 Candidate",
        "current_identity_anchor": "contact dust; artillery hit; red charge only, no release",
        "existing_user_decision": "not requested; not granted",
        "current_candidate": "three 2048x256 RGBA eight-frame atlases exist and probe PASS",
        "alignment_status": "technical_pass; package_incomplete; U1 pending",
        "demo_use": "representative round effects",
        "next_action": "Phase C complete manifest/spec/probe/report/hashes/user card; show user",
        "lifecycle": "Candidate",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "art-a7-round-presentation/fx-spec.tsv;A7 validator",
    },
    {
        "stable_id": "R05_SFX_LIMITED_ORIGINAL_SET",
        "subject": "A7 original audio limited set",
        "canon_art_level": "A7 Candidate",
        "current_identity_anchor": "16 contract-listed WAV slots; 48kHz PCM24; declared channels/durations",
        "existing_user_decision": "not requested; not granted",
        "current_candidate": "16 WAV files and probe exist; validator media checks PASS",
        "alignment_status": "technical_pass; package_incomplete; U1 pending",
        "demo_use": "UI/world tone for representative round",
        "next_action": "Phase C complete package records and user selection",
        "lifecycle": "Candidate",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "evidence_paths": "art-a7-round-presentation/audio-spec.tsv;audio-media-probe.json;A7 validator",
    },
]


def validate_sources() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, (path, expected, role) in SOURCES.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"SOURCE_DRIFT {rel(path)} expected={expected} actual={actual}")
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "role": role,
                "result": "PASS_exact_sha256",
            }
        )
    for path, expected in IMAGE_EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"SOURCE_DRIFT {rel(path)} expected={expected} actual={actual}")
        rows.append(
            {
                "source_id": path.stem,
                "path": rel(path),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "role": "read_only_identity_or_candidate_source",
                "result": "PASS_exact_sha256",
            }
        )
    return rows


def alpha_composite_contain(
    canvas: Image.Image,
    source: Image.Image,
    box: tuple[int, int, int, int],
    *,
    pad: int = 0,
) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    target = (max(1, right - left - pad * 2), max(1, bottom - top - pad * 2))
    fitted = ImageOps.contain(source.convert("RGBA"), target, Image.Resampling.LANCZOS)
    x = left + (right - left - fitted.width) // 2
    y = top + (bottom - top - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    return x, y, x + fitted.width, y + fitted.height


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    text_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    max_width: int,
    *,
    line_gap: int = 6,
    max_lines: int | None = None,
) -> int:
    x, y = xy
    lines: list[str] = []
    current = ""
    for token in text:
        trial = current + token
        if draw.textbbox((0, 0), trial, font=text_font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = token
    if current:
        lines.append(current)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines[-1] and draw.textbbox((0, 0), lines[-1] + "…", font=text_font)[2] > max_width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"
    line_height = draw.textbbox((0, 0), "国Ag", font=text_font)[3]
    for index, line in enumerate(lines):
        draw.text((x, y + index * (line_height + line_gap)), line, font=text_font, fill=fill)
    return y + len(lines) * (line_height + line_gap)


def frame_atlas(path: Path, frame_width: int, count: int) -> list[Image.Image]:
    atlas = Image.open(path).convert("RGBA")
    if atlas.width != frame_width * count:
        raise SystemExit(f"ATLAS_WIDTH_MISMATCH {rel(path)}")
    return [atlas.crop((index * frame_width, 0, (index + 1) * frame_width, atlas.height)) for index in range(count)]


def header(canvas: Image.Image, title: str, subtitle: str) -> None:
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, canvas.width, 132), fill=(3, 14, 20, 255))
    draw.text((48, 28), title, font=font(42), fill=TEXT)
    draw.text((canvas.width - 48, 46), subtitle, font=font(24), fill=MUTED, anchor="ra")
    draw.line((48, 132, canvas.width - 48, 132), fill=LINE, width=2)


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], accent: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=6, fill=PANEL, outline=LINE, width=2)
    draw.rectangle((box[0], box[1], box[2], box[1] + 7), fill=accent)


def make_subject_board(
    output: Path,
    *,
    title: str,
    subtitle: str,
    anchor_path: Path,
    atlas_path: Path,
    frame_width: int,
    state_labels: list[str],
    anchor_label: str,
    notes: list[str],
    accent: tuple[int, int, int, int],
    conclusion: str = "审计结论：身份锚一致性仅通过只读复核；是否作为 Demo 派生来源仍等待用户 U1。",
) -> None:
    canvas = Image.new("RGBA", (2400, 1400), BG)
    draw = ImageDraw.Draw(canvas)
    header(canvas, title, subtitle)

    anchor_box = (48, 176, 622, 1250)
    panel(draw, anchor_box, accent)
    draw.text((72, 202), anchor_label, font=font(27), fill=accent)
    anchor = Image.open(anchor_path).convert("RGBA")
    alpha_composite_contain(canvas, anchor, (74, 258, 596, 1122), pad=12)
    draw_wrapped(draw, notes[0], (74, 1142), font(21), MUTED, 500, max_lines=3)

    frames = frame_atlas(atlas_path, frame_width, 3)
    start_x = 662
    gap = 20
    frame_panel_width = 548
    for index, (state, frame) in enumerate(zip(state_labels, frames, strict=True)):
        left = start_x + index * (frame_panel_width + gap)
        box = (left, 176, left + frame_panel_width, 1250)
        state_accent = [CYAN, CORAL, GOLD][index]
        panel(draw, box, state_accent)
        draw.text((left + 24, 202), f"A6 Candidate · {state}", font=font(25), fill=state_accent)
        alpha_composite_contain(canvas, frame, (left + 22, 262, left + frame_panel_width - 22, 1032), pad=8)
        draw_wrapped(draw, notes[index + 1], (left + 24, 1062), font(20), TEXT, frame_panel_width - 48, max_lines=4)

    draw.rectangle((48, 1280, 2352, 1352), fill=(7, 24, 31, 255), outline=LINE, width=1)
    draw.text((72, 1300), conclusion, font=font(24), fill=TEXT)
    canvas.convert("RGB").save(output, quality=95)


def make_doudeng_board(output: Path) -> None:
    canvas = Image.new("RGBA", (2400, 1400), BG)
    draw = ImageDraw.Draw(canvas)
    header(canvas, "A8 Phase A｜兜灯既有件布局适配", "CML002 · no redraw · no crop · no overwrite")

    observe_box = (48, 176, 1118, 610)
    tense_box = (48, 636, 1118, 1070)
    layout_box = (1150, 176, 2352, 1070)
    for box, accent in [(observe_box, CYAN), (tense_box, CORAL), (layout_box, GOLD)]:
        panel(draw, box, accent)

    draw.text((72, 200), "既有 approved_for_runtime｜OBSERVE｜1920×640", font=font(25), fill=CYAN)
    draw.text((72, 660), "既有 approved_for_runtime｜TENSE｜1920×640", font=font(25), fill=CORAL)
    draw.text((1174, 200), "A6 Candidate 适配板｜1280×720", font=font(25), fill=GOLD)

    alpha_composite_contain(canvas, Image.open(DOUDENG_OBSERVE), (72, 254, 1094, 582), pad=4)
    alpha_composite_contain(canvas, Image.open(DOUDENG_TENSE), (72, 714, 1094, 1042), pad=4)
    alpha_composite_contain(canvas, Image.open(DOUDENG_LAYOUT), (1174, 254, 2328, 1026), pad=4)

    draw.rectangle((48, 1102, 2352, 1352), fill=(7, 24, 31, 255), outline=LINE, width=1)
    draw.text((72, 1130), "本轮只问布局适配，不重审兜灯身份、不生成 A6 新母版。", font=font(28), fill=TEXT)
    draw.text((72, 1182), "OBSERVE / TENSE 原件在适配板中均保持 3:1 整幅等比缩放；没有裁切、拉伸或覆盖源文件。", font=font(23), fill=MUTED)
    draw.text((72, 1232), "若你认为新界面仍不适配，应另开“新作兜灯”任务，而不是在这里静默改图。", font=font(23), fill=GOLD)
    draw.text((72, 1290), "状态：原件 approved_for_runtime；本适配板 Candidate / runtime_allowed=false / handoff=none", font=font(20), fill=MUTED)
    canvas.convert("RGB").save(output, quality=95)


def status_color(status: str) -> tuple[int, int, int, int]:
    if status.startswith("approved") or status.startswith("source_preserved"):
        return GREEN
    if status.startswith("identity_consistent") or status.startswith("technical_pass"):
        return GOLD
    if status.startswith("missing") or status.startswith("identity_drift"):
        return CORAL
    return PURPLE


def make_truth_board(output: Path) -> None:
    width, height = 2400, 1800
    canvas = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    header(canvas, "A8 Phase A｜C01E02 当前视觉资产真值矩阵", "Current / Working / Candidate / History separated")

    columns = [(40, 420), (460, 1080), (1120, 1790), (1830, 2360)]
    headers = ["Stable ID / 对象", "身份权威与既有决定", "当前候选与真实状态", "Demo 用途 / 下一动作"]
    y = 150
    draw.rectangle((40, y, 2360, y + 70), fill=(14, 40, 49, 255), outline=LINE, width=2)
    for (left, right), label in zip(columns, headers, strict=True):
        draw.text((left + 12, y + 18), label, font=font(23), fill=TEXT)
        draw.line((right, y, right, height - 54), fill=LINE, width=1)

    row_height = 116
    y += 70
    for index, row in enumerate(TRUTH_ROWS):
        top = y + index * row_height
        bottom = top + row_height
        fill = PANEL if index % 2 == 0 else PANEL_ALT
        draw.rectangle((40, top, 2360, bottom), fill=fill)
        accent = status_color(row["alignment_status"])
        draw.rectangle((40, top, 48, bottom), fill=accent)
        draw.line((40, bottom, 2360, bottom), fill=LINE, width=1)
        for _, right in columns[:-1]:
            draw.line((right, top, right, bottom), fill=LINE, width=1)

        draw_wrapped(draw, row["stable_id"], (58, top + 10), font(19), accent, 344, max_lines=2)
        draw_wrapped(draw, row["subject"], (58, top + 64), font(18), MUTED, 344, max_lines=2)

        authority_text = f"{row['canon_art_level']}｜{row['existing_user_decision']}"
        draw_wrapped(draw, authority_text, (474, top + 10), font(18), TEXT, 588, max_lines=4)

        candidate_text = f"{row['alignment_status']}｜{row['current_candidate']}"
        draw_wrapped(draw, candidate_text, (1134, top + 10), font(18), TEXT, 638, max_lines=4)

        next_text = f"{row['demo_use']}｜{row['next_action']}"
        draw_wrapped(draw, next_text, (1844, top + 10), font(18), TEXT, 500, max_lines=4)

    footer_y = 150 + 70 + len(TRUTH_ROWS) * row_height + 14
    draw.text((48, footer_y), "绿色＝已有明确用户来源；黄色＝技术/身份复核通过但 U1 未签；红色＝缺失或明确漂移。", font=font(21), fill=MUTED)
    draw.text((2352, footer_y), "全部 A8 Phase A 输出：Candidate / runtime_allowed=false / runtime_handoff=none", font=font(20), fill=MUTED, anchor="ra")
    canvas.convert("RGB").save(output, quality=95)


def write_tsv(path: Path, rows: Iterable[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_docs(outputs: dict[str, Path]) -> None:
    decision = HERE / "phase-a-user-decision-card.md"
    decision.write_text(
        """# C01E02 A8 Phase A｜A6 与既有兜灯资产 U1 裁决卡

> Package: `C01CDV1_A8_PHASE_A_CURRENT_TRUTH_V1`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 请按顺序判断

1. **纪存**：三态是否延续黑发、蓝眼、无眼镜、深蓝馆务外套和腕部终端？`focused / alarm` 差异是否足够，还是需要窄返修其中一态？
2. **七海**：三态是否保持成熟、克制、远程承担撤令后果？闭口 `decision` 是否明确读成 `presence card`，而非正在下达战场命令？
3. **旧守护者**：原 A6 三态误用了 `09b` 老馆守 Z 裁图，现已判定身份源漂移，不再请求按原图批准。下一步只从 `V10X` 新本体窄返修头胸、胸灯与波形，再回到 U1。
4. **兜灯**：既有 `OBSERVE / TENSE` 整幅原件放入新布局后是否适配？不适配时只决定是否另开“新作兜灯”任务，本轮不直接重画。
5. **720p 信息布局**：人物／机体通讯、远程 presence card 和长文安全区是否可读，是否压住战术地图？
6. 请逐项点名允许作为下一阶段 Demo 派生来源的具体 Atlas 与 SHA；兜灯仍引用既有 Stable ID，不批准 A6 适配板冒名成新母版。

## A6 两份待批 Atlas＋一份退回返修

- 纪存：`art-a6-character-comms-ui/assets/atlases/r05-portrait-jicun-states-2304x768.png`  
  SHA-256：`d6ec72d6976f532cfde707902231de3df5633d17aca66116710e4fa72b67622e`
- 七海：`art-a6-character-comms-ui/assets/atlases/r05-portrait-qihai-remote-states-2304x768.png`  
  SHA-256：`477f0873c6bdda04dde1312c49d57aaf53b1f2f6337023269290c5f87edbf67f`
- 旧守护者（退回，不得批准原图）：`art-a6-character-comms-ui/assets/atlases/r05-comms-old-guardian-states-3072x768.png`  
  SHA-256：`41dd29862ed0a2be873dbaac580c4269c4ad3161156834021812c5a0b1a7e4be`

新 E02 本体源：`art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`  
SHA-256：`e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`

## 建议回复格式

```text
纪存：通过 / 修改……；
七海：通过，确认为 presence card / 修改……；
旧守护者：同意按 V10X 窄返修 / 修改返修边界……；
兜灯：适配通过 / 另开新作任务；
720p 布局：通过 / 修改……；
批准派生来源：纪存 <路径>/<SHA>；七海 <路径>/<SHA>。旧守护者原 Atlas 不批准。
```

未获明确回复，不进入馆守 Z、BREAKER、重盾和车辆的完整 Atlas。
""",
        encoding="utf-8",
    )

    completion = HERE / "phase-a-completion-report.md"
    completion.write_text(
        """# C01E02 A8 Phase A｜当前资产真值与 A6 复核完成报告

- 已核验 48/49 合同、09b 冻结视觉快照、A1/B1/B2/A4/A5 用户回执、42 媒体规格与 45 A7 制作人审查。
- A6 原包 validator 与 core hashes 均通过；本任务未改写任何 A6 源图或 Atlas。
- A7 图像／FX／音频技术资产存在，但缺少 `asset-manifest.tsv`、`completion-report.md`、`core-delivery-hashes.sha256` 与 `user-decision-card.md`，状态记录为“有限包尚未封包”。
- 复核发现 A6 旧守护者三态与晚于 09b 的 V10X 馆守 Z 新本体不一致；原 Atlas 已明确退回，不得作为 U1 handoff。
- 已把 CML008 标记为旧 Hard 身份校对锚，把 V10X 标记为 E02 实际生产源；V21 只登记为飞行背包装着 Candidate，不替代裸机。
- 已生成完整真值矩阵、四张身份锚并排板和 U1 用户卡。
- 未制作馆守 Z、BREAKER、重盾、车辆新图；未返修 GIANT_CONTACT；未写 Godot、Runtime、Canon 或 exact handoff。

当前停止点：等待用户确认 V10X 返修边界，以及纪存、七海与兜灯的 A6 U1。
""",
        encoding="utf-8",
    )
    outputs["decision_card"] = decision
    outputs["completion_report"] = completion


def write_manifest(outputs: dict[str, Path]) -> Path:
    path = HERE / "phase-a-asset-manifest.tsv"
    fields = [
        "package_id",
        "asset_id",
        "path",
        "media_type",
        "dimensions",
        "role",
        "source_policy",
        "lifecycle",
        "runtime_allowed",
        "runtime_handoff",
        "sha256",
    ]
    rows = []
    for asset_id, output in sorted(outputs.items()):
        if output.suffix.lower() == ".png":
            with Image.open(output) as image:
                dimensions = f"{image.width}x{image.height}"
            media_type = "image/png"
            role = "review_board"
        elif output.suffix.lower() == ".tsv":
            dimensions = "n/a"
            media_type = "text/tab-separated-values"
            role = "authority_evidence"
        else:
            dimensions = "n/a"
            media_type = "text/markdown"
            role = "decision_or_completion_evidence"
        rows.append(
            {
                "package_id": PACKAGE_ID,
                "asset_id": asset_id,
                "path": output.relative_to(HERE).as_posix(),
                "media_type": media_type,
                "dimensions": dimensions,
                "role": role,
                "source_policy": "read_only_composite_or_evidence;no_source_asset_modified",
                "lifecycle": "Candidate",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
                "sha256": sha256(output),
            }
        )
    write_tsv(path, rows, fields)
    return path


def write_core_hashes(paths: Iterable[Path]) -> None:
    target = HERE / "phase-a-core-delivery-hashes.sha256"
    lines = [f"{sha256(path)}  {rel(path)}" for path in sorted(set(paths), key=lambda item: rel(item))]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    source_rows = validate_sources()

    truth_tsv = HERE / "current-asset-truth-matrix.tsv"
    write_tsv(truth_tsv, TRUTH_ROWS, list(TRUTH_ROWS[0].keys()))

    source_receipt = HERE / "source-validation-receipt.tsv"
    write_tsv(
        source_receipt,
        source_rows,
        ["source_id", "path", "expected_sha256", "actual_sha256", "role", "result"],
    )

    outputs: dict[str, Path] = {
        "truth_matrix_tsv": truth_tsv,
        "source_validation_receipt": source_receipt,
    }

    truth_board = HERE / "A8_PHASE_A_CURRENT_ASSET_TRUTH_BOARD_2400x1800.png"
    make_truth_board(truth_board)
    outputs["truth_board"] = truth_board

    jicun_board = HERE / "A8_PHASE_A_JICUN_CURRENT_VS_A6_2400x1400.png"
    make_subject_board(
        jicun_board,
        title="A8 Phase A｜纪存 Current 身份锚 vs A6 三态",
        subtitle="CML001 Hard lock · R05_PORTRAIT_JICUN Candidate",
        anchor_path=JICUN_ANCHOR,
        atlas_path=JICUN_ATLAS,
        frame_width=768,
        state_labels=["focused", "alarm", "resolve"],
        anchor_label="Current 身份锚｜CML001",
        notes=[
            "黑发蓝眼、无眼镜、青年而不幼；深蓝馆务外套、左腕档案终端、微白机魂光。",
            "读取路线与人员状态；动作由腕部终端承担，不是统帅姿态。",
            "警觉仍然克制；与 focused 的差异目前偏细，请用户判断是否够用。",
            "抬头作出路线判断；不是全知宣告，也不控制馆守 Z 四肢。",
        ],
        accent=CYAN,
    )
    outputs["jicun_review_board"] = jicun_board

    qihai_board = HERE / "A8_PHASE_A_QIHAI_CURRENT_VS_A6_2400x1400.png"
    make_subject_board(
        qihai_board,
        title="A8 Phase A｜七海 Current 身份锚 vs A6 远程三态",
        subtitle="CML004 Hard lock · R05_PORTRAIT_QIHAI_REMOTE Candidate",
        anchor_path=QIHAI_ANCHOR,
        atlas_path=QIHAI_ATLAS,
        frame_width=768,
        state_labels=["controlled", "decision", "concerned"],
        anchor_label="Current 身份锚｜CML004",
        notes=[
            "日本成年女性；深色直发、冷白法务服、成熟克制的秩序与危险吸引力。",
            "远程公务状态；不在现场，不承担玩家可操作命令入口。",
            "闭口、眼神坚定；表达撤回本人停机令后的承担，而非发布战场指令。",
            "担忧不少女化；仍保持流程责任与远程距离。",
        ],
        accent=GOLD,
    )
    outputs["qihai_review_board"] = qihai_board

    guardian_board = HERE / "A8_PHASE_A_OLD_GUARDIAN_CURRENT_VS_A6_2400x1400.png"
    make_subject_board(
        guardian_board,
        title="A8 Phase A｜馆守 Z 新本体 V10X vs A6 旧守护者三态",
        subtitle="CH002 same subject · V10X E02 production source · legacy CML008 cross-check only",
        anchor_path=GUARDIAN_E02_MASTER,
        atlas_path=GUARDIAN_ATLAS,
        frame_width=1024,
        state_labels=["guide", "contact", "shield_gaze"],
        anchor_label="E02 新本体源｜V10X/W-X",
        notes=[
            "原 A6 三态取自 09b 老工程化馆守 Z，晚于 09b 的 V10X/W-X 新本体没有被带入。",
            "旧守护者仍是馆守 Z 同一主体，但头冠、红X胸、圆形金核、宽肩和等长飞拳必须换成 V10X 身份。",
            "现有 guide/contact/shield_gaze 只保留状态语法；原头胸造型不得进入 handoff。",
            "V21 的 A3 双翼只属于飞行背包装着 Candidate，不进入 E02 裸机通讯头像。",
        ],
        accent=GOLD,
        conclusion="审计结论：A6 原三态身份源漂移，原 Atlas 退回；必须按 V10X 新本体窄返修后再进入 U1。",
    )
    outputs["old_guardian_review_board"] = guardian_board

    doudeng_board = HERE / "A8_PHASE_A_DOUDENG_EXISTING_ADAPTATION_2400x1400.png"
    make_doudeng_board(doudeng_board)
    outputs["doudeng_adaptation_board"] = doudeng_board

    write_docs(outputs)
    manifest = write_manifest(outputs)

    core_paths = list(outputs.values()) + [manifest, Path(__file__).resolve()]
    core_paths += [path for path, _, _ in SOURCES.values()]
    core_paths += list(IMAGE_EXPECTED.keys())
    write_core_hashes(core_paths)

    print(f"PASS {PACKAGE_ID}")
    print(f"truth_rows={len(TRUTH_ROWS)} review_boards=5")
    print("lifecycle=Candidate runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
