#!/usr/bin/env python3
"""Validate a Chao GAG Episode Loop run directory.

This catches the failure mode where a run claims to use the single-episode
pipeline but actually ships multi-chapter prose without episode packets,
writer-room reviews, ledgers, or prefix regression reviews.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PACKET_HEADINGS = [
    "## Episode",
    "## 1. Previous Episode Audit",
    "## 2. Next Episode Brief",
    "## 3. Context Pack",
    "## 4. Pipeline Pressure Board",
    "## 5. Episode Card",
    "## 6. Draft Synopsis",
    "## 7. Writer Room Review",
    "## 8. Patch Log",
    "## 9. Gate Result",
    "## 10. State Deltas",
    "## 11. Auto Next Brief",
]

REQUIRED_AGENT_ROLES = [
    "showrunner",
    "mecha_ip",
    "gameplay",
    "relationship",
    "protagonist",
    "canon_asset",
]

CREATIVE_AGENT_ROLES = [
    "quote_scene",
    "spectacle_emotion",
    "wanji_culture",
]

STRICT_WRITER_ROOM_ROLES = [
    "showrunner",
    "50_issue",
    "mecha_ip",
    "gameplay",
    "character_dialogue",
    "relationship",
    "protagonist",
    "jicun_memory",
    "quote_scene",
    "spectacle_emotion",
    "robot_anime_pv",
    "commercial_opening",
    "macro_mystery",
    "player_interest",
    "wanji_culture",
    "thickness",
    "canon_asset",
]

REQUIRED_LEDGER_FILES = [
    "episode_state.tsv",
    "roster_exposure.tsv",
    "quote_scene_usage.tsv",
    "relationship_heat.tsv",
    "protagonist_arc.tsv",
    "protagonist_memory.tsv",
    "enemy_gain.tsv",
    "regression_tickets.tsv",
    "unresolved_issues.tsv",
    "episode_packet_index.tsv",
    "writer_room_reviews.tsv",
    "prefix_reviews.tsv",
    "run_validation.tsv",
]

CREATIVE_LEDGER_FILES = [
    "creative_experience_gates.tsv",
    "mecha_ip_first_appearances.tsv",
]

REQUIRED_LEDGER_COLUMNS = {
    "episode_packet_index.tsv": [
        "episode_id",
        "packet_path",
        "status",
        "reviewer_mode",
        "subagent_review_ids",
        "gate_decision",
        "chapter_id",
    ],
    "writer_room_reviews.tsv": [
        "episode_id",
        "role_id",
        "reviewer_id",
        "result",
        "blocking_findings",
        "patch_actions",
    ],
    "prefix_reviews.tsv": [
        "chapter_id",
        "review_path",
        "chapters_read",
        "overall_result",
        "earliest_root_cause_chapter",
        "regression_ticket_opened",
        "warn_classification",
        "blocking_issue",
        "required_action",
        "ledger_rows_written",
    ],
    "regression_tickets.tsv": [
        "ticket_id",
        "root_cause_id",
        "discovered_after_chapter",
        "root_cause_chapter",
        "replay_range",
        "attempt_no",
        "replay_log_path",
        "status",
    ],
    "unresolved_issues.tsv": [
        "issue_id",
        "root_cause_id",
        "first_seen_after_chapter",
        "chronology",
        "cause_summary",
        "attempts_summary",
        "chosen_version",
        "residual_risk",
        "future_watchpoint",
        "user_review_needed",
    ],
    "run_validation.tsv": [
        "run_id",
        "validator_command",
        "validator_result",
        "fallback_or_downgrade",
    ],
}

CREATIVE_LEDGER_COLUMNS = {
    "creative_experience_gates.tsv": [
        "episode_id",
        "burn_point",
        "tear_point",
        "gag_point",
        "pv_spectacle",
        "ip_scene_projection",
        "protagonist_big_move",
        "qihai_or_core_big_move",
        "wanji_collection_sample_count",
        "gate_result",
    ],
    "mecha_ip_first_appearances.tsv": [
        "episode_id",
        "countable_first_appearance_units",
        "roster_package_class_units",
        "functional_modules",
        "non_count_anchors",
        "gate_result",
    ],
    "quote_scene_usage.tsv": [
        "episode_id",
        "quote_text_or_phrase",
        "quote_family",
        "usage_type",
        "scene_payload",
        "reuse_policy",
    ],
}

FABLE_LEDGER_COLUMNS = {
    "fable_review.tsv": [
        "episode_id",
        "fable_review_status",
        "review_pack_path",
        "output_capture_path",
        "diagnosis_surfaces",
        "accepted_items",
        "rejected_items",
        "local_fallback_review",
        "merge_status",
    ],
}

SOURCE_ABSORPTION_LEDGER_COLUMNS = {
    "source_absorption.tsv": [
        "episode_id",
        "source_class",
        "source_id",
        "selected_or_skipped",
        "bound_scene",
        "player_action",
        "character_action",
        "mecha_or_map_action",
        "enemy_gain_or_misuse",
        "state_delta",
        "reader_visible",
        "production_visible",
        "absorption_status",
        "next_required_read",
    ],
}

V35_SLOT_LEDGER_COLUMNS = {
    "slot_episode_mapping.tsv": [
        "episode_id",
        "chapter_id",
        "slot_id",
        "slot_title",
        "episode_order_within_slot",
        "episodes_in_slot",
        "slot_mode",
        "route_window",
        "mapping_status",
        "split_reason",
    ],
    "route_state.tsv": [
        "episode_id",
        "route_window",
        "selected_slots",
        "skipped_slots",
        "incoming_route_state",
        "active_route_state",
        "convergence_differences",
        "failure_dignity_state",
        "next_required_read",
        "gate_result",
    ],
    "unit_availability.tsv": [
        "episode_id",
        "unit_id",
        "lifecycle_event",
        "availability_before",
        "fleet_before",
        "action_in_episode",
        "availability_after",
        "fleet_after",
        "lifecycle_source",
        "gate_result",
    ],
    "decision_propagation.tsv": [
        "episode_id",
        "thread_id",
        "source_stage",
        "incoming_state",
        "bound_scene",
        "outgoing_state_delta",
        "downstream_read",
        "propagation_status",
    ],
    "skipped_slot_world_state.tsv": [
        "episode_id",
        "chapter_id",
        "route_window",
        "skipped_slot_id",
        "world_continues_as",
        "unit_or_character_state",
        "next_visibility_window",
        "ex_role",
        "status",
    ],
}

V35_SOURCE_SETS = {
    "v35_4": {
        "slots": [Path("docs/superpowers/specs/data/story/v35_4_author_slot_route_architecture_v35_4.tsv")],
        "routes": [Path("docs/superpowers/specs/data/story/v35_4_playthrough_route_combinations_v35_4.tsv")],
        "units": [Path("docs/superpowers/specs/data/story/v35_4_unit_lifecycle_slot_allocation_v35_4.tsv")],
        "decisions": [Path("docs/superpowers/specs/data/story/v35_4_decision_branch_state_propagation_v35_4.tsv")],
    },
    "v35_7": {
        "slots": [Path("docs/superpowers/specs/data/story/v35_7_author_slot_architecture_v35_7.tsv")],
        "routes": [Path("docs/superpowers/specs/data/story/v35_7_playthrough_route_combinations_v35_7.tsv")],
        "units": [
            Path("docs/superpowers/specs/data/story/v35_7_unit_lifecycle_slot_remap_v35_7.tsv"),
            Path("docs/superpowers/specs/data/story/v35_7_starfire_playable_lifecycle_patch_v35_7.tsv"),
        ],
        "decisions": [
            Path("docs/superpowers/specs/data/story/v35_4_decision_branch_state_propagation_v35_4.tsv"),
            Path("docs/superpowers/specs/data/story/v35_7_continuity_thread_backflow_v35_7.tsv"),
            Path("docs/superpowers/specs/data/story/v35_7_mystery_slot_binding_v35_7.tsv"),
            Path("docs/superpowers/specs/data/story/v35_7_foreshadow_slot_binding_v35_7.tsv"),
        ],
        "crosswalk": [Path("docs/superpowers/specs/data/story/v35_7_v29_eighteen_chapter_crosswalk_v35_7.tsv")],
        "manifests": [Path("docs/superpowers/specs/data/story/v35_7_high_density_slot_mecha_manifest_v35_7.tsv")],
        "loadouts": [Path("docs/superpowers/specs/data/story/v35_8_slot_mecha_ip_play_contract_v35_8.tsv")],
        "unit_manifests": [Path("docs/superpowers/specs/data/story/v35_8_slot_unit_manifest_v35_8.tsv")],
        "source_absorption": [Path("docs/superpowers/specs/data/story/v35_8_slot_source_absorption_v35_8.tsv")],
        "gameplay_contracts": [Path("docs/superpowers/specs/data/story/v35_8_slot_gameplay_contract_v35_8.tsv")],
        "asset_manifests": [Path("docs/superpowers/specs/data/story/v35_8_slot_asset_manifest_v35_8.tsv")],
        "gate_reconciliation": [Path("docs/superpowers/specs/data/story/v35_8_gate_lifecycle_reconciliation_v35_8.tsv")],
        "dynamic_selectors": [Path("docs/superpowers/specs/data/story/v35_8_dynamic_unit_selectors_v35_8.tsv")],
        "unit_source_crosswalk": [Path("docs/superpowers/specs/data/story/v35_8_unit_source_crosswalk_v35_8.tsv")],
        "package_source_crosswalk": [Path("docs/superpowers/specs/data/story/v35_8_package_source_crosswalk_v35_8.tsv")],
    },
}

VALID_STATUS = {"pass", "accepted", "warn"}
VALID_GATE_DECISION = {"pass", "accepted"}
VALID_REVIEW_RESULT = {"pass", "warn", "fail"}
VALID_FABLE_STATUS = {
    "fable_review_done",
    "fable_failed_technical",
    "fable_rejected_overdrift",
    "fable_skipped_user_approved",
}
VALID_FABLE_MERGE_STATUS = {
    "merged",
    "rejected",
    "deferred",
    "local_fallback",
    "skipped_user_approved",
}
VALID_SOURCE_SELECTION = {"selected", "skipped"}
VALID_SOURCE_ABSORPTION_STATUS = {"pass", "partial_warn", "fail", "skipped"}
VALID_NEW_UNIT_GATE_MODES = {"first_appearance", "lifecycle_delta", "bridge_exception"}
VALID_LIFECYCLE_EVENTS = {
    "first_visible",
    "first_control",
    "formal_join",
    "new_form",
    "new_weapon",
    "pilot_relation",
    "machine_soul_relation",
    "combination_position",
    "political_reassignment",
    "fleet_transfer",
    "enemy_to_ally",
    "route_lock",
    "terminal_payoff",
    "meaningful_return",
    "scene_support",
}
QUALIFYING_LIFECYCLE_EVENTS = VALID_LIFECYCLE_EVENTS - {"first_visible", "scene_support"}
VALID_PROPAGATION_STATUS = {"pass", "accepted", "skipped", "not_applicable"}
TRUTHY_VALUES = {"yes", "y", "true", "1", "是", "visible", "present", "reader_visible", "production_visible"}
PLACEHOLDER_VALUES = {"", "-", "tbd", "todo", "placeholder", "填写", "待填"}
NON_COUNT_ANCHOR_HINTS = [
    "盒",
    "模型盒",
    "展签",
    "留言墙",
    "取件屏",
    "锚件",
    "维修单",
    "标签",
    "纸条",
    "档案",
    "终端",
]
MICRO_METRIC_HINTS = ["40秒", "四十秒", "半格", "一格", "贴标签", "贴展签", "水印"]
WEAK_SPECTACLE_HINTS = ["一帧", "短暂", "灰显", "只是", "仅"]


class PacketInfo:
    def __init__(
        self,
        *,
        path: Path,
        episode_id: str,
        chapter_id: str | None,
        slot_id: str | None,
        new_unit_gate_mode: str | None,
        status: str | None,
        gate_decision: str | None,
        subagent_ids: dict[str, str],
    ) -> None:
        self.path = path
        self.episode_id = episode_id
        self.chapter_id = chapter_id
        self.slot_id = slot_id
        self.new_unit_gate_mode = new_unit_gate_mode
        self.status = status
        self.gate_decision = gate_decision
        self.subagent_ids = subagent_ids


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def packet_episode_id(text: str) -> str | None:
    match = re.search(r"(?m)^Episode ID:\s*(\S+)", text)
    return match.group(1) if match else None


def packet_chapter_id(text: str) -> str | None:
    match = re.search(r"(?m)^Chapter ID:\s*(\S+)", text)
    return match.group(1) if match else None


def packet_slot_id(text: str) -> str | None:
    match = re.search(r"(?m)^Author Slot ID:\s*(\S+)", text)
    return match.group(1) if match else None


def packet_status(text: str) -> str | None:
    match = re.search(r"(?m)^Status:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else None


def count_episode_markers(text: str) -> int:
    markers = re.findall(r"(?m)^Episode ID:\s*\S+", text)
    markers += re.findall(r"(?m)^##\s+(?:C\d{2}E\d{2}|E\d{2})\b", text)
    return len(markers)


def field_value(text: str, label: str) -> str | None:
    match = re.search(rf"(?mi)^{re.escape(label)}:\s*(.*?)\s*$", text)
    return match.group(1).strip() if match else None


def normalized(value: str | None) -> str:
    return (value or "").strip().lower()


def is_placeholder(value: str | None, *, allow_none: bool = False) -> bool:
    norm = normalized(value)
    if allow_none and norm in {"none", "无", "no", "n/a"}:
        return False
    return norm in PLACEHOLDER_VALUES or norm in {"none", "无", "n/a", "ok"}


def parse_subagent_ids(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    result: dict[str, str] = {}
    for item in re.split(r"[;；,，]\s*", value.strip()):
        if not item:
            continue
        if "=" not in item:
            continue
        role, reviewer_id = item.split("=", 1)
        result[role.strip()] = reviewer_id.strip()
    return result


def required_review_roles(*, strict_creative_gates: bool, strict_writer_room: bool) -> list[str]:
    if strict_writer_room:
        return STRICT_WRITER_ROOM_ROLES
    return REQUIRED_AGENT_ROLES + (CREATIVE_AGENT_ROLES if strict_creative_gates else [])


def split_items(value: str | None) -> list[str]:
    if not value:
        return []
    return [
        item.strip()
        for item in re.split(r"[;；,，、|]\s*", value)
        if item.strip() and not is_placeholder(item, allow_none=True)
    ]


def require_meaningful_field(
    *,
    text: str,
    label: str,
    rel: str,
    errors: list[str],
    min_compact_chars: int = 8,
) -> str:
    value = field_value(text, label)
    compact = re.sub(r"\s+", "", value or "")
    if value is None:
        fail(errors, f"{rel}: missing strict creative field '{label}:'")
        return ""
    if is_placeholder(value) or len(compact) < min_compact_chars:
        fail(errors, f"{rel}: strict creative field '{label}:' is empty/thin")
    return value or ""


def looks_micro_only(value: str) -> bool:
    compact = re.sub(r"\s+", "", value)
    return any(hint in compact for hint in MICRO_METRIC_HINTS) and len(compact) < 60


def looks_weak_spectacle(value: str) -> bool:
    compact = re.sub(r"\s+", "", value)
    return any(hint in compact for hint in WEAK_SPECTACLE_HINTS) and len(compact) < 70


def validate_strict_creative_packet_fields(
    *,
    text: str,
    rel: str,
    episode_id: str,
    min_wanji_c01_samples: int,
    require_v35_slot_contract: bool,
    errors: list[str],
) -> None:
    required_labels = [
        "Roster-Package-Class Unit",
        "Non-Count Anchors",
        "IP Scene Projection",
        "Burn Point",
        "Tear Point",
        "Gag Point",
        "PV-Scale Spectacle",
        "Wanji Collection Density",
        "Protagonist Big Move",
        "Qihai/Jicun Big Move",
    ]
    values = {
        label: require_meaningful_field(text=text, label=label, rel=rel, errors=errors)
        for label in required_labels
    }
    new_unit_mode = normalized(field_value(text, "New Unit Gate Mode"))
    if require_v35_slot_contract and new_unit_mode in {"lifecycle_delta", "bridge_exception"}:
        real_new_value = field_value(text, "Real New IP-Mapped Units")
        if real_new_value is None:
            fail(errors, f"{rel}: V35 slot contract requires 'Real New IP-Mapped Units:' even when none")
        values["Real New IP-Mapped Units"] = real_new_value or ""
    else:
        values["Real New IP-Mapped Units"] = require_meaningful_field(
            text=text,
            label="Real New IP-Mapped Units",
            rel=rel,
            errors=errors,
        )
    if looks_micro_only(values.get("Protagonist Big Move", "")):
        fail(errors, f"{rel}: Protagonist Big Move is only a tiny metric, not a dramatic turn")
    if looks_micro_only(values.get("Qihai/Jicun Big Move", "")):
        fail(errors, f"{rel}: Qihai/Jicun Big Move is only a tiny metric, not a dramatic turn")
    if looks_weak_spectacle(values.get("PV-Scale Spectacle", "")):
        fail(errors, f"{rel}: PV-Scale Spectacle is too small/brief for a strict creative gate")
    units = split_items(values.get("Real New IP-Mapped Units"))
    if not units and not (
        require_v35_slot_contract and new_unit_mode in {"lifecycle_delta", "bridge_exception"}
    ):
        fail(errors, f"{rel}: Real New IP-Mapped Units must list actual countable units")
    anchor_like_units = [
        unit
        for unit in units
        if any(hint in unit for hint in NON_COUNT_ANCHOR_HINTS)
    ]
    if anchor_like_units:
        fail(errors, f"{rel}: anchor-like items listed as real units: {', '.join(anchor_like_units)}")
    if episode_id == "C01E01":
        raw_count = field_value(text, "Wanji Collection Sample Count")
        if raw_count is None:
            fail(errors, f"{rel}: C01E01 strict gate requires 'Wanji Collection Sample Count:'")
        else:
            try:
                count = int(raw_count.strip())
            except ValueError:
                fail(errors, f"{rel}: Wanji Collection Sample Count must be an integer, got {raw_count!r}")
            else:
                if count < min_wanji_c01_samples:
                    fail(
                        errors,
                        f"{rel}: C01E01 must show at least {min_wanji_c01_samples} Wanji collection samples, got {count}",
                    )


def validate_v35_packet_fields(text: str, rel: str, errors: list[str]) -> tuple[str | None, str | None]:
    required_labels = [
        "Canon Mode",
        "Author Slot ID",
        "Slot Mode",
        "Slot-to-Episode Mapping",
        "Route Window",
        "Route State",
        "Selected Slots",
        "Skipped Slots",
        "Available Fleet",
        "Cross-Fleet Deployment Reason",
        "New Unit Gate Mode",
        "Roster Lifecycle Payload",
        "Incoming Decision Threads",
        "Outgoing Decision Deltas",
        "Skipped-Slot World State",
    ]
    for label in required_labels:
        value = field_value(text, label)
        if value is None:
            fail(errors, f"{rel}: missing V35 slot-contract field '{label}:'")
            continue
        if label not in {
            "Cross-Fleet Deployment Reason",
            "Selected Slots",
            "Skipped Slots",
            "Incoming Decision Threads",
            "Outgoing Decision Deltas",
            "Skipped-Slot World State",
        } and is_placeholder(value):
            fail(errors, f"{rel}: V35 slot-contract field '{label}:' is empty/placeholder")

    slot_id = packet_slot_id(text)
    if slot_id and not re.fullmatch(r"V35(?:4|7)-C\d{2}-S\d{2}", slot_id):
        fail(errors, f"{rel}: Author Slot ID has invalid format {slot_id!r}")
    if slot_id and slot_id.startswith("V357-"):
        for label in [
            "V35.8 Loadout Contract ID",
            "Mystery Binding IDs",
            "Continuity Thread IDs",
            "Foreshadow Binding IDs",
            "V29 Crosswalk Selection",
            "High-Density Manifest IDs",
        ]:
            value = field_value(text, label)
            if value is None:
                fail(errors, f"{rel}: missing V35.7 slot-contract field '{label}:'")
            elif is_placeholder(value):
                fail(
                    errors,
                    f"{rel}: V35.7 field '{label}:' must list ids or give a concrete not-required reason",
                )

    canon_mode = normalized(field_value(text, "Canon Mode"))
    if canon_mode not in {"living_plus_v35_candidate", "v35_candidate_overlay"}:
        fail(
            errors,
            f"{rel}: Canon Mode must explicitly select the V35 candidate overlay, got {canon_mode!r}",
        )

    mode = normalized(field_value(text, "New Unit Gate Mode"))
    if mode not in VALID_NEW_UNIT_GATE_MODES:
        fail(errors, f"{rel}: New Unit Gate Mode must be one of {sorted(VALID_NEW_UNIT_GATE_MODES)}, got {mode!r}")
    lifecycle_payload = field_value(text, "Roster Lifecycle Payload")
    if mode == "lifecycle_delta" and is_placeholder(lifecycle_payload):
        fail(errors, f"{rel}: lifecycle_delta requires a meaningful Roster Lifecycle Payload")
    if mode == "bridge_exception":
        compensation = field_value(text, "Next Mecha Compensation Window")
        reason = field_value(text, "Bridge Exception Reason")
        if is_placeholder(reason):
            fail(errors, f"{rel}: bridge_exception requires 'Bridge Exception Reason:'")
        if is_placeholder(compensation):
            fail(errors, f"{rel}: bridge_exception requires 'Next Mecha Compensation Window:'")
    return slot_id, mode


def review_section(text: str) -> str:
    match = re.search(
        r"(?s)## 7\. Writer Room Review(?P<body>.*?)(?:\n## 8\. Patch Log|\Z)",
        text,
    )
    return match.group("body") if match else ""


def validate_role_finding(section: str, role: str, rel: str, errors: list[str]) -> None:
    match = re.search(rf"(?mi)^\s*{re.escape(role)}\s*:\s*(.*?)\s*$", section)
    if not match:
        fail(errors, f"{rel}: missing writer-room role line {role}:")
        return
    value = match.group(1).strip()
    if is_placeholder(value):
        fail(errors, f"{rel}: writer-room role {role} has empty/placeholder finding")
        return
    status_match = re.search(r"\b(pass|warn|fail)\b", value, flags=re.IGNORECASE)
    if not status_match:
        fail(errors, f"{rel}: writer-room role {role} must include pass/warn/fail")
    compact = re.sub(r"\s+", "", re.sub(r"\b(pass|warn|fail)\b", "", value, flags=re.IGNORECASE))
    if len(compact) < 8:
        fail(errors, f"{rel}: writer-room role {role} finding is too thin")


def validate_packet(
    path: Path,
    *,
    require_subagents: bool,
    require_fable_review: bool,
    require_source_absorption: bool,
    require_v35_slot_contract: bool,
    strict_creative_gates: bool,
    strict_writer_room: bool,
    min_story_chars: int,
    min_wanji_c01_samples: int,
    errors: list[str],
) -> PacketInfo | None:
    text = read_text(path)
    rel = str(path)

    for heading in REQUIRED_PACKET_HEADINGS:
        if heading not in text:
            fail(errors, f"{rel}: missing required heading {heading!r}")
    if require_fable_review and "## 7.5 Fable Fixed Review Pass" not in text:
        fail(errors, f"{rel}: missing required Fable review heading '## 7.5 Fable Fixed Review Pass'")
    if require_source_absorption:
        for marker in [
            "### Episode Input Manifest",
            "### Scene Binding Matrix",
            "Source Absorption Review",
        ]:
            if marker not in text:
                fail(errors, f"{rel}: missing required source absorption marker {marker!r}")

    slot_id = None
    new_unit_gate_mode = None
    if require_v35_slot_contract:
        slot_id, new_unit_gate_mode = validate_v35_packet_fields(text, rel, errors)

    episode_id = packet_episode_id(text)
    if not episode_id:
        fail(errors, f"{rel}: missing non-empty 'Episode ID:'")
        episode_id = ""

    chapter_id = packet_chapter_id(text)
    if not chapter_id:
        fail(errors, f"{rel}: missing non-empty 'Chapter ID:'")

    marker_count = count_episode_markers(text)
    if marker_count > 1:
        fail(errors, f"{rel}: appears to contain {marker_count} episode markers; one packet must contain exactly one episode")

    status = packet_status(text)
    if not status:
        fail(errors, f"{rel}: missing 'Status:'")
    elif normalized(status) not in VALID_STATUS:
        fail(errors, f"{rel}: packet status must be one of {sorted(VALID_STATUS)}, got {status!r}")

    story_match = re.search(
        r"(?s)## 6\. Draft Synopsis(?P<body>.*?)(?:\n## 7\. Writer Room Review|\Z)",
        text,
    )
    story_chars = len(re.sub(r"\s+", "", story_match.group("body"))) if story_match else 0
    if story_chars < min_story_chars:
        fail(errors, f"{rel}: Draft Synopsis has {story_chars} non-space chars, below {min_story_chars}")

    subagent_ids: dict[str, str] = {}
    if require_subagents:
        reviewer_mode = field_value(text, "Reviewer Mode")
        if normalized(reviewer_mode) != "subagent":
            fail(errors, f"{rel}: Reviewer Mode must be exactly 'subagent', got {reviewer_mode!r}")
        subagent_ids = parse_subagent_ids(field_value(text, "Subagent Review IDs"))
        required_roles = required_review_roles(
            strict_creative_gates=strict_creative_gates,
            strict_writer_room=strict_writer_room,
        )
        missing_ids = [
            role
            for role in required_roles
            if role not in subagent_ids or is_placeholder(subagent_ids.get(role))
        ]
        if missing_ids:
            fail(errors, f"{rel}: missing non-empty Subagent Review IDs for roles: {', '.join(missing_ids)}")

        section = review_section(text)
        for role in required_roles:
            validate_role_finding(section, role, rel, errors)

        blocking = field_value(section, "Subagent Blocking Findings")
        patch_actions = field_value(section, "Subagent Patch Actions Applied")
        if blocking is None:
            fail(errors, f"{rel}: missing 'Subagent Blocking Findings:'")
        if patch_actions is None:
            fail(errors, f"{rel}: missing 'Subagent Patch Actions Applied:'")
        if blocking and normalized(blocking) not in {"none", "no", "无"} and is_placeholder(patch_actions):
            fail(errors, f"{rel}: has blocking findings but missing concrete Subagent Patch Actions Applied")

    gate_match = re.search(r"(?mi)^Gate decision:\s*(.+?)\s*$", text)
    gate_decision = None
    if not gate_match:
        fail(errors, f"{rel}: missing 'Gate decision:'")
    else:
        gate_decision = gate_match.group(1).strip()
        if normalized(gate_decision) not in VALID_GATE_DECISION:
            fail(errors, f"{rel}: Gate decision must be one of {sorted(VALID_GATE_DECISION)}, got {gate_decision!r}")

    if not episode_id:
        return None
    if strict_creative_gates:
        validate_strict_creative_packet_fields(
            text=text,
            rel=rel,
            episode_id=episode_id,
            min_wanji_c01_samples=min_wanji_c01_samples,
            require_v35_slot_contract=require_v35_slot_contract,
            errors=errors,
        )
    if require_fable_review:
        status_value = field_value(text, "Fable Review Status")
        norm_status = normalized(status_value)
        if norm_status not in VALID_FABLE_STATUS:
            fail(errors, f"{rel}: Fable Review Status must be one of {sorted(VALID_FABLE_STATUS)}, got {status_value!r}")
        if norm_status == "fable_failed_technical":
            fallback = field_value(text, "Local fallback review")
            if is_placeholder(fallback):
                fail(errors, f"{rel}: fable_failed_technical requires non-empty Local fallback review")
    return PacketInfo(
        path=path,
        episode_id=episode_id,
        chapter_id=chapter_id,
        slot_id=slot_id,
        new_unit_gate_mode=new_unit_gate_mode,
        status=status,
        gate_decision=gate_decision,
        subagent_ids=subagent_ids,
    )


def chapter_id_from_path(path: Path) -> str | None:
    match = re.match(r"(C\d{2})", path.stem)
    return match.group(1) if match else None


def field_value_any(text: str, labels: list[str]) -> str | None:
    for label in labels:
        value = field_value(text, label)
        if value is not None:
            return value
    return None


def validate_prefix_review(
    path: Path,
    errors: list[str],
    *,
    strict_prefix_warn_policy: bool,
) -> dict[str, str]:
    text = read_text(path)
    rel = str(path)
    required = [
        "Review scope:",
        "Chapters read:",
        "Overall result:",
        "Earliest root-cause chapter:",
        "Regression ticket opened:",
        "Replay required:",
        "Advance decision:",
    ]
    for marker in required:
        if marker not in text:
            fail(errors, f"{rel}: missing prefix review marker {marker!r}")
    overall = field_value(text, "Overall result")
    ticket_opened = field_value(text, "Regression ticket opened")
    replay_required = field_value(text, "Replay required")
    warn_classification = field_value_any(text, ["Warn classification", "Warn 分类", "警告分类"])
    blocking_issue = field_value_any(text, ["Blocking issue", "阻塞问题"])
    required_action = field_value_any(text, ["Required action", "必要动作"])
    unresolved_issue = field_value_any(text, ["Unresolved issue carried", "遗留问题带出"])
    if normalized(overall) not in {"pass", "warn", "fail"}:
        fail(errors, f"{rel}: Overall result must be pass/warn/fail, got {overall!r}")
    if normalized(ticket_opened) not in {"yes", "no"}:
        fail(errors, f"{rel}: Regression ticket opened must be yes/no, got {ticket_opened!r}")
    if normalized(replay_required) not in {"yes", "no"}:
        fail(errors, f"{rel}: Replay required must be yes/no, got {replay_required!r}")
    if normalized(overall) == "fail" and normalized(ticket_opened) != "yes":
        fail(errors, f"{rel}: failed prefix review must open a regression ticket")
    if normalized(ticket_opened) == "yes" and normalized(replay_required) != "yes":
        fail(errors, f"{rel}: regression ticket requires replay")
    if strict_prefix_warn_policy and normalized(overall) == "warn":
        if is_placeholder(warn_classification):
            fail(errors, f"{rel}: warn prefix review must include non-empty Warn classification")
        if is_placeholder(blocking_issue):
            fail(errors, f"{rel}: warn prefix review must state Blocking issue, even if it is none")
        if is_placeholder(required_action):
            fail(errors, f"{rel}: warn prefix review must include concrete Required action")
        if normalized(ticket_opened) == "no" and is_placeholder(unresolved_issue):
            fail(errors, f"{rel}: warn prefix review without regression ticket must carry a tracked unresolved issue/watchpoint")
    return {
        "chapter_id": chapter_id_from_path(path) or "",
        "overall_result": overall or "",
        "regression_ticket_opened": ticket_opened or "",
        "replay_required": replay_required or "",
        "warn_classification": warn_classification or "",
        "blocking_issue": blocking_issue or "",
        "required_action": required_action or "",
        "unresolved_issue_carried": unresolved_issue or "",
    }


def read_tsv(path: Path, errors: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    rel = str(path)
    rows = path.read_text(encoding="utf-8").splitlines()
    if not rows:
        fail(errors, f"{rel}: ledger is empty")
        return [], []
    header = rows[0].split("\t")
    expected = len(header)
    if expected < 2:
        fail(errors, f"{rel}: ledger header has fewer than 2 TSV columns")
    parsed: list[dict[str, str]] = []
    for idx, row in enumerate(rows[1:], start=2):
        if not row.strip():
            continue
        parts = row.split("\t")
        got = len(parts)
        if got != expected:
            fail(errors, f"{rel}:{idx}: expected {expected} TSV columns, got {got}")
            continue
        parsed.append(dict(zip(header, parts, strict=True)))
    return header, parsed


def validate_ledger(path: Path, errors: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    header, rows = read_tsv(path, errors)
    required = REQUIRED_LEDGER_COLUMNS.get(path.name, [])
    missing = [column for column in required if column not in header]
    if missing:
        fail(errors, f"{path}: missing required columns: {', '.join(missing)}")
    return header, rows


def validate_creative_ledger_header(path: Path, header: list[str], errors: list[str]) -> None:
    required = CREATIVE_LEDGER_COLUMNS.get(path.name, [])
    missing = [column for column in required if column not in header]
    if missing:
        fail(errors, f"{path}: strict creative gate missing required columns: {', '.join(missing)}")


def validate_fable_ledger_header(path: Path, header: list[str], errors: list[str]) -> None:
    required = FABLE_LEDGER_COLUMNS.get(path.name, [])
    missing = [column for column in required if column not in header]
    if missing:
        fail(errors, f"{path}: fable review gate missing required columns: {', '.join(missing)}")


def validate_source_absorption_ledger_header(path: Path, header: list[str], errors: list[str]) -> None:
    required = SOURCE_ABSORPTION_LEDGER_COLUMNS.get(path.name, [])
    missing = [column for column in required if column not in header]
    if missing:
        fail(errors, f"{path}: source absorption gate missing required columns: {', '.join(missing)}")


def validate_v35_slot_ledger_header(path: Path, header: list[str], errors: list[str]) -> None:
    required = V35_SLOT_LEDGER_COLUMNS.get(path.name, [])
    missing = [column for column in required if column not in header]
    if missing:
        fail(errors, f"{path}: V35 slot-contract gate missing required columns: {', '.join(missing)}")


def find_project_root(run_dir: Path) -> Path | None:
    candidates = [run_dir.resolve(), *run_dir.resolve().parents, Path.cwd().resolve(), *Path.cwd().resolve().parents]
    markers = [paths["slots"][0] for paths in V35_SOURCE_SETS.values()]
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if any((candidate / marker).exists() for marker in markers):
            return candidate
    return None


def parse_slot_list(value: str | None) -> list[str]:
    if not value:
        return []
    return re.findall(r"V35(?:4|7)-C\d{2}-S\d{2}", value)


def v35_contract_version(packet_infos: list[PacketInfo], errors: list[str]) -> str:
    versions = {
        "v35_7" if (info.slot_id or "").startswith("V357-") else "v35_4"
        for info in packet_infos
        if info.slot_id
    }
    if len(versions) > 1:
        fail(errors, "V35 slot-contract run mixes V354 and V357 Author Slot IDs")
    return next(iter(versions), "v35_4")


def validate_v35_slot_contract(
    run_dir: Path,
    packet_infos: list[PacketInfo],
    ledgers: dict[str, list[dict[str, str]]],
    errors: list[str],
) -> None:
    contract_version = v35_contract_version(packet_infos, errors)
    source_paths = V35_SOURCE_SETS[contract_version]
    contract_label = "V35.7" if contract_version == "v35_7" else "V35.4"
    project_root = find_project_root(run_dir)
    if project_root is None:
        fail(errors, f"{run_dir}: cannot locate {contract_label} source tables from run directory or current workspace")
        return

    source_rows: dict[str, list[dict[str, str]]] = {}
    for source_name, relative_paths in source_paths.items():
        source_rows[source_name] = []
        for relative_path in relative_paths:
            source_path = project_root / relative_path
            header, rows = read_tsv(source_path, errors)
            if not header:
                fail(errors, f"{source_path}: {contract_label} source table could not be read")
            source_rows[source_name].extend(rows)

    slots = {row.get("slot_id", ""): row for row in source_rows["slots"]}
    routes = {row.get("route_window", ""): row for row in source_rows["routes"]}
    units = {row.get("unit_id", ""): row for row in source_rows["units"]}
    decision_threads = {
        row.get("thread_id") or row.get("mystery_id") or row.get("hook_id") or ""
        for row in source_rows["decisions"]
    }
    mystery_ids = {row.get("mystery_id", "") for row in source_rows["decisions"] if row.get("mystery_id")}
    continuity_ids = {row.get("thread_id", "") for row in source_rows["decisions"] if row.get("thread_id", "").startswith("V357")}
    foreshadow_ids = {row.get("hook_id", "") for row in source_rows["decisions"] if row.get("hook_id")}
    manifest_rows = source_rows.get("manifests", [])
    manifest_ids = {row.get("manifest_id", "") for row in manifest_rows}
    dense_slots = {row.get("slot_id", "") for row in manifest_rows}
    crosswalk_chapters = {row.get("chapter_id", "") for row in source_rows.get("crosswalk", [])}
    loadout_by_slot = {row.get("slot_id", ""): row for row in source_rows.get("loadouts", [])}

    mapping_by_episode = {row.get("episode_id", ""): row for row in ledgers.get("slot_episode_mapping.tsv", [])}
    route_by_episode = {row.get("episode_id", ""): row for row in ledgers.get("route_state.tsv", [])}
    unit_rows_by_episode = rows_by_episode(ledgers.get("unit_availability.tsv", []))
    decision_rows_by_episode = rows_by_episode(ledgers.get("decision_propagation.tsv", []))
    skipped_rows_by_episode = rows_by_episode(ledgers.get("skipped_slot_world_state.tsv", []))
    skipped_rows_by_slot: dict[str, list[dict[str, str]]] = {}
    for row in ledgers.get("skipped_slot_world_state.tsv", []):
        skipped_rows_by_slot.setdefault(row.get("skipped_slot_id", ""), []).append(row)

    route_selections: dict[str, tuple[set[str], set[str]]] = {}
    slot_mapping_orders: dict[str, tuple[int, set[int]]] = {}
    previous_bridge_episode: str | None = None

    for info in packet_infos:
        episode_id = info.episode_id
        mapping = mapping_by_episode.get(episode_id)
        if not mapping:
            fail(errors, f"{run_dir}: slot_episode_mapping.tsv missing row for {episode_id}")
            continue
        slot_id = mapping.get("slot_id", "")
        slot = slots.get(slot_id)
        if not slot:
            fail(errors, f"{run_dir}: {episode_id} maps to unknown {contract_label} slot {slot_id!r}")
        else:
            if mapping.get("chapter_id") != slot.get("chapter_id"):
                fail(errors, f"{run_dir}: {episode_id} slot mapping chapter does not match {contract_label} slot source")
            if info.chapter_id and mapping.get("chapter_id") != info.chapter_id:
                fail(errors, f"{run_dir}: {episode_id} slot mapping chapter does not match packet Chapter ID")
            if info.slot_id != slot_id:
                fail(errors, f"{run_dir}: {episode_id} packet Author Slot ID does not match slot_episode_mapping.tsv")
            if mapping.get("slot_mode") != slot.get("slot_mode"):
                fail(errors, f"{run_dir}: {episode_id} slot_mode does not match {contract_label} slot source")
        if contract_version == "v35_7":
            packet_text = read_text(info.path)
            loadout = loadout_by_slot.get(slot_id)
            if not loadout:
                fail(errors, f"{run_dir}: {episode_id}/{slot_id} has no V35.8 loadout contract")
            else:
                packet_loadout = field_value(packet_text, "V35.8 Loadout Contract ID") or ""
                if packet_loadout != loadout.get("contract_id", ""):
                    fail(
                        errors,
                        f"{run_dir}: {episode_id} V35.8 Loadout Contract ID {packet_loadout!r} "
                        f"does not match {loadout.get('contract_id', '')!r}",
                    )
                packet_gate = normalized(field_value(packet_text, "New Unit Gate Mode"))
                effective_gate = normalized(loadout.get("effective_gate_mode"))
                if packet_gate != effective_gate:
                    fail(
                        errors,
                        f"{run_dir}: {episode_id} New Unit Gate Mode {packet_gate!r} "
                        f"does not match V35.8 effective gate {effective_gate!r}",
                    )
            binding_specs = [
                ("Mystery Binding IDs", r"V356M\d{2}", mystery_ids),
                ("Continuity Thread IDs", r"V357[CF]\d{2}", continuity_ids),
                ("Foreshadow Binding IDs", r"V356H\d{3}", foreshadow_ids),
            ]
            for label, pattern, valid_ids in binding_specs:
                value = field_value(packet_text, label) or ""
                refs = set(re.findall(pattern, value))
                unknown = refs - valid_ids
                if unknown:
                    fail(errors, f"{run_dir}: {episode_id} {label} references unknown ids: {', '.join(sorted(unknown))}")
            crosswalk_value = field_value(packet_text, "V29 Crosswalk Selection") or ""
            if mapping.get("chapter_id", "") not in crosswalk_chapters:
                fail(errors, f"{run_dir}: {episode_id} chapter has no V35.7 V29 crosswalk row")
            if normalized(crosswalk_value).startswith("not_required"):
                fail(errors, f"{run_dir}: {episode_id} V29 Crosswalk Selection cannot be not_required in a V35.7 run")
            manifest_value = field_value(packet_text, "High-Density Manifest IDs") or ""
            selected_manifests = set(re.findall(r"V357MF\d{3}", manifest_value))
            unknown_manifests = selected_manifests - manifest_ids
            if unknown_manifests:
                fail(errors, f"{run_dir}: {episode_id} references unknown high-density manifests: {', '.join(sorted(unknown_manifests))}")
            if slot_id in dense_slots and not selected_manifests:
                fail(errors, f"{run_dir}: {episode_id}/{slot_id} is a high-density slot but has no valid manifest id")
        try:
            order = int(mapping.get("episode_order_within_slot", ""))
            count = int(mapping.get("episodes_in_slot", ""))
        except ValueError:
            fail(errors, f"{run_dir}: {episode_id} slot mapping order/count must be integers")
        else:
            if order < 1 or count < 1 or order > count:
                fail(errors, f"{run_dir}: {episode_id} invalid slot episode order {order}/{count}")
            if count > 1 and is_placeholder(mapping.get("split_reason"), allow_none=False):
                fail(errors, f"{run_dir}: {episode_id} split author slot requires split_reason")
            expected_count, seen_orders = slot_mapping_orders.get(slot_id, (count, set()))
            if expected_count != count:
                fail(errors, f"{run_dir}: author slot {slot_id} has inconsistent episodes_in_slot values")
            seen_orders.add(order)
            slot_mapping_orders[slot_id] = (expected_count, seen_orders)
        if normalized(mapping.get("mapping_status")) not in VALID_GATE_DECISION:
            fail(errors, f"{run_dir}: {episode_id} slot mapping status must be pass/accepted")

        route_row = route_by_episode.get(episode_id)
        if not route_row:
            fail(errors, f"{run_dir}: route_state.tsv missing row for {episode_id}")
        else:
            route_window = route_row.get("route_window", "")
            if route_window not in routes and normalized(route_window) not in {"linear", "none", "not_applicable"}:
                fail(errors, f"{run_dir}: {episode_id} uses unknown route_window {route_window!r}")
            selected = set(parse_slot_list(route_row.get("selected_slots")))
            skipped = set(parse_slot_list(route_row.get("skipped_slots")))
            unknown_slots = sorted((selected | skipped) - set(slots))
            if unknown_slots:
                fail(errors, f"{run_dir}: {episode_id} route state references unknown slots: {', '.join(unknown_slots)}")
            if selected & skipped:
                fail(errors, f"{run_dir}: {episode_id} route state has slots both selected and skipped")
            if route_window in routes:
                source = routes[route_window]
                expected_authored = int(source.get("authored_slots", "0") or 0)
                expected_play = int(source.get("playthrough_slots", "0") or 0)
                if len(selected) != expected_play:
                    fail(errors, f"{run_dir}: {episode_id}/{route_window} selected {len(selected)} slot(s), expected {expected_play}")
                if len(selected | skipped) != expected_authored:
                    fail(errors, f"{run_dir}: {episode_id}/{route_window} covers {len(selected | skipped)} authored slot(s), expected {expected_authored}")
                mandatory = set(parse_slot_list(source.get("mandatory_slots")))
                source_selectable = set(
                    parse_slot_list(source.get("selectable_slots") or source.get("exclusive_or_pool_slots"))
                )
                source_authored = mandatory | source_selectable
                if mandatory - selected:
                    fail(
                        errors,
                        f"{run_dir}: {episode_id}/{route_window} omits mandatory slot(s): {', '.join(sorted(mandatory - selected))}",
                    )
                if source_authored and selected | skipped != source_authored:
                    fail(
                        errors,
                        f"{run_dir}: {episode_id}/{route_window} selected/skipped set does not match source-authored slots",
                    )
                prior = route_selections.get(route_window)
                current = (selected, skipped)
                if prior is not None and prior != current:
                    fail(errors, f"{run_dir}: route selection for {route_window} changes between episode rows")
                route_selections[route_window] = current
            for skipped_slot in skipped:
                matching = skipped_rows_by_slot.get(skipped_slot, [])
                if not matching:
                    fail(errors, f"{run_dir}: {episode_id} skipped slot {skipped_slot} has no world-state row")
            if normalized(route_row.get("gate_result")) not in VALID_GATE_DECISION:
                fail(errors, f"{run_dir}: {episode_id} route_state gate_result must be pass/accepted")

        unit_rows = unit_rows_by_episode.get(episode_id, [])
        if not unit_rows:
            fail(errors, f"{run_dir}: unit_availability.tsv missing row for {episode_id}")
        qualifying_events = []
        for row in unit_rows:
            unit_id = row.get("unit_id", "")
            event = normalized(row.get("lifecycle_event"))
            if unit_id not in units:
                fail(errors, f"{run_dir}: {episode_id} unit_availability references unknown unit {unit_id!r}")
            if event not in VALID_LIFECYCLE_EVENTS:
                fail(errors, f"{run_dir}: {episode_id}/{unit_id} invalid lifecycle_event {event!r}")
            if event in QUALIFYING_LIFECYCLE_EVENTS and not is_placeholder(row.get("action_in_episode")):
                qualifying_events.append(event)
            for fleet_column in ["fleet_before", "fleet_after"]:
                if is_placeholder(row.get(fleet_column)):
                    fail(errors, f"{run_dir}: {episode_id}/{unit_id} missing {fleet_column}")
            if normalized(row.get("gate_result")) not in VALID_GATE_DECISION:
                fail(errors, f"{run_dir}: {episode_id}/{unit_id} unit availability gate must be pass/accepted")
        if info.new_unit_gate_mode == "lifecycle_delta" and not qualifying_events:
            fail(errors, f"{run_dir}: {episode_id} lifecycle_delta has no qualifying unit_availability event")
        if info.new_unit_gate_mode == "first_appearance" and not any(
            normalized(row.get("lifecycle_event")) in {"first_visible", "first_control"}
            for row in unit_rows
        ):
            fail(errors, f"{run_dir}: {episode_id} first_appearance mode has no first-visible/control lifecycle event")
        if info.new_unit_gate_mode == "bridge_exception":
            if previous_bridge_episode is not None:
                fail(errors, f"{run_dir}: bridge_exception used in consecutive packets {previous_bridge_episode} and {episode_id}")
            previous_bridge_episode = episode_id
        else:
            previous_bridge_episode = None

        decision_rows = decision_rows_by_episode.get(episode_id, [])
        if not decision_rows:
            fail(errors, f"{run_dir}: decision_propagation.tsv missing row for {episode_id}")
        for row in decision_rows:
            thread_id = row.get("thread_id", "")
            if normalized(thread_id) not in {"none", "not_applicable"} and thread_id not in decision_threads:
                fail(errors, f"{run_dir}: {episode_id} decision propagation references unknown thread {thread_id!r}")
            status = normalized(row.get("propagation_status"))
            if status not in VALID_PROPAGATION_STATUS:
                fail(errors, f"{run_dir}: {episode_id}/{thread_id} invalid propagation_status {status!r}")
            if status in {"pass", "accepted"}:
                for column in ["incoming_state", "bound_scene", "outgoing_state_delta", "downstream_read"]:
                    if is_placeholder(row.get(column)):
                        fail(errors, f"{run_dir}: {episode_id}/{thread_id} missing decision propagation {column}")

        for row in skipped_rows_by_episode.get(episode_id, []):
            skipped_slot = row.get("skipped_slot_id", "")
            if skipped_slot not in slots:
                fail(errors, f"{run_dir}: {episode_id} skipped world-state references unknown slot {skipped_slot!r}")
            for column in ["world_continues_as", "unit_or_character_state", "next_visibility_window"]:
                if is_placeholder(row.get(column)):
                    fail(errors, f"{run_dir}: {episode_id}/{skipped_slot} missing skipped-world-state {column}")
            if normalized(row.get("status")) not in VALID_GATE_DECISION:
                fail(errors, f"{run_dir}: {episode_id}/{skipped_slot} skipped-world-state status must be pass/accepted")

    for slot_id, (expected_count, seen_orders) in slot_mapping_orders.items():
        expected_orders = set(range(1, expected_count + 1))
        if seen_orders != expected_orders:
            fail(
                errors,
                f"{run_dir}: author slot {slot_id} mapped episode orders {sorted(seen_orders)}, expected {sorted(expected_orders)}",
            )


def rows_by_episode(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(row.get("episode_id", ""), []).append(row)
    return result


def validate_strict_creative_ledgers(
    run_dir: Path,
    packet_infos: list[PacketInfo],
    ledgers: dict[str, list[dict[str, str]]],
    errors: list[str],
    *,
    min_new_ip_units: int,
    min_wanji_c01_samples: int,
    require_v35_slot_contract: bool,
) -> None:
    if not packet_infos:
        return

    creative_rows = {row.get("episode_id", ""): row for row in ledgers.get("creative_experience_gates.tsv", [])}
    mecha_rows = {row.get("episode_id", ""): row for row in ledgers.get("mecha_ip_first_appearances.tsv", [])}
    quote_rows = ledgers.get("quote_scene_usage.tsv", [])
    quote_rows_by_episode = rows_by_episode(quote_rows)
    unit_availability_by_episode = rows_by_episode(ledgers.get("unit_availability.tsv", []))

    for info in packet_infos:
        episode_id = info.episode_id
        creative = creative_rows.get(episode_id)
        if not creative:
            fail(errors, f"{run_dir}: creative_experience_gates.tsv missing row for {episode_id}")
        else:
            for column in [
                "burn_point",
                "tear_point",
                "gag_point",
                "pv_spectacle",
                "ip_scene_projection",
                "protagonist_big_move",
                "qihai_or_core_big_move",
            ]:
                value = creative.get(column)
                if is_placeholder(value):
                    fail(errors, f"{run_dir}: creative_experience_gates {episode_id}/{column} is empty")
            if normalized(creative.get("gate_result")) not in VALID_GATE_DECISION:
                fail(errors, f"{run_dir}: creative_experience_gates {episode_id} gate_result must be pass/accepted")
            if looks_micro_only(creative.get("protagonist_big_move", "")):
                fail(errors, f"{run_dir}: creative_experience_gates {episode_id} protagonist_big_move is only a tiny metric")
            if looks_micro_only(creative.get("qihai_or_core_big_move", "")):
                fail(errors, f"{run_dir}: creative_experience_gates {episode_id} qihai_or_core_big_move is only a tiny metric")
            if looks_weak_spectacle(creative.get("pv_spectacle", "")):
                fail(errors, f"{run_dir}: creative_experience_gates {episode_id} pv_spectacle is too small/brief")
            if episode_id == "C01E01":
                raw_count = creative.get("wanji_collection_sample_count", "")
                try:
                    count = int(raw_count)
                except ValueError:
                    fail(errors, f"{run_dir}: C01E01 wanji_collection_sample_count must be an integer, got {raw_count!r}")
                else:
                    if count < min_wanji_c01_samples:
                        fail(
                            errors,
                            f"{run_dir}: C01E01 wanji_collection_sample_count must be >= {min_wanji_c01_samples}, got {count}",
                        )

        mecha = mecha_rows.get(episode_id)
        if not mecha:
            fail(errors, f"{run_dir}: mecha_ip_first_appearances.tsv missing row for {episode_id}")
        else:
            units = split_items(mecha.get("countable_first_appearance_units"))
            roster_units = split_items(mecha.get("roster_package_class_units"))
            v35_mode = info.new_unit_gate_mode if require_v35_slot_contract else None
            qualifying_lifecycle = any(
                normalized(row.get("lifecycle_event")) in QUALIFYING_LIFECYCLE_EVENTS
                and not is_placeholder(row.get("action_in_episode"))
                for row in unit_availability_by_episode.get(episode_id, [])
            )
            if len(units) < min_new_ip_units and not (
                require_v35_slot_contract
                and (
                    (v35_mode == "lifecycle_delta" and qualifying_lifecycle)
                    or v35_mode == "bridge_exception"
                )
            ):
                fail(
                    errors,
                    f"{run_dir}: {episode_id} has {len(units)} countable first-appearance unit(s), below {min_new_ip_units}",
                )
            if not roster_units and not (
                require_v35_slot_contract
                and (
                    (v35_mode == "lifecycle_delta" and qualifying_lifecycle)
                    or v35_mode == "bridge_exception"
                )
            ):
                fail(errors, f"{run_dir}: {episode_id} has no roster-package-class first appearance")
            anchor_like_units = [
                unit
                for unit in units
                if any(hint in unit for hint in NON_COUNT_ANCHOR_HINTS)
            ]
            if anchor_like_units:
                fail(errors, f"{run_dir}: {episode_id} counts anchor-like items as units: {', '.join(anchor_like_units)}")
            if normalized(mecha.get("gate_result")) not in VALID_GATE_DECISION:
                fail(errors, f"{run_dir}: mecha_ip_first_appearances {episode_id} gate_result must be pass/accepted")

        if not quote_rows_by_episode.get(episode_id):
            fail(errors, f"{run_dir}: quote_scene_usage.tsv missing quote/scene row for {episode_id}")

    direct_quote_uses: dict[str, list[tuple[str, str]]] = {}
    for row in quote_rows:
        quote = (row.get("quote_text_or_phrase") or "").strip()
        usage_type = normalized(row.get("usage_type"))
        if not quote or "direct" not in usage_type:
            continue
        direct_quote_uses.setdefault(quote, []).append((row.get("episode_id", ""), row.get("reuse_policy", "")))
    for quote, uses in direct_quote_uses.items():
        episodes = {episode_id for episode_id, _policy in uses}
        if len(episodes) <= 1:
            continue
        allowed = all(normalized(policy) in {"intentional_refrain", "allowed_repeat"} for _episode_id, policy in uses)
        if not allowed:
            fail(
                errors,
                f"{run_dir}: direct quote/phrase reused across episodes without intentional reuse policy: {quote!r} in {', '.join(sorted(episodes))}",
            )


def validate_packet_index(
    run_dir: Path,
    packet_infos: list[PacketInfo],
    rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    if not packet_infos:
        return
    by_episode = {row.get("episode_id", ""): row for row in rows}
    for info in packet_infos:
        row = by_episode.get(info.episode_id)
        if not row:
            fail(errors, f"{run_dir}: episode_packet_index.tsv missing row for {info.episode_id}")
            continue
        packet_path = row.get("packet_path", "")
        if not packet_path or packet_path.endswith(".gitkeep"):
            fail(errors, f"{run_dir}: episode_packet_index row for {info.episode_id} has empty packet_path")
        else:
            candidate = run_dir / packet_path
            if not candidate.exists() and not (run_dir / "episodes" / Path(packet_path).name).exists():
                fail(errors, f"{run_dir}: episode_packet_index path for {info.episode_id} does not exist: {packet_path}")
        if normalized(row.get("status")) not in VALID_STATUS:
            fail(errors, f"{run_dir}: episode_packet_index status for {info.episode_id} is invalid: {row.get('status')!r}")
        if normalized(row.get("gate_decision")) not in VALID_GATE_DECISION:
            fail(errors, f"{run_dir}: episode_packet_index gate_decision for {info.episode_id} is invalid: {row.get('gate_decision')!r}")
        if info.chapter_id and row.get("chapter_id") != info.chapter_id:
                fail(errors, f"{run_dir}: episode_packet_index chapter_id for {info.episode_id} does not match packet")


def validate_fable_review_ledger(
    run_dir: Path,
    packet_infos: list[PacketInfo],
    rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    if not packet_infos:
        return
    by_episode = {row.get("episode_id", ""): row for row in rows}
    for info in packet_infos:
        row = by_episode.get(info.episode_id)
        if not row:
            fail(errors, f"{run_dir}: fable_review.tsv missing row for {info.episode_id}")
            continue
        status = normalized(row.get("fable_review_status"))
        merge_status = normalized(row.get("merge_status"))
        if status not in VALID_FABLE_STATUS:
            fail(errors, f"{run_dir}: fable_review {info.episode_id} invalid status {row.get('fable_review_status')!r}")
        if merge_status not in VALID_FABLE_MERGE_STATUS:
            fail(errors, f"{run_dir}: fable_review {info.episode_id} invalid merge_status {row.get('merge_status')!r}")
        surfaces = normalized(row.get("diagnosis_surfaces"))
        for surface in [
            "readability",
            "dialogue",
            "relationship",
            "burn",
            "boring",
        ]:
            if surface not in surfaces:
                fail(errors, f"{run_dir}: fable_review {info.episode_id} missing diagnosis surface hint {surface!r}")
        if status == "fable_review_done" and is_placeholder(row.get("output_capture_path")):
            fail(errors, f"{run_dir}: fable_review_done for {info.episode_id} requires output_capture_path")
        if status == "fable_failed_technical" and is_placeholder(row.get("local_fallback_review")):
            fail(errors, f"{run_dir}: fable_failed_technical for {info.episode_id} requires local_fallback_review")


def is_truthy(value: str | None) -> bool:
    return normalized(value) in TRUTHY_VALUES


def has_meaningful_source_action(value: str | None) -> bool:
    return not is_placeholder(value) and normalized(value) not in {"none", "no", "n/a", "无"}


def validate_source_absorption_ledger(
    run_dir: Path,
    packet_infos: list[PacketInfo],
    rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    if not packet_infos:
        return
    rows_for_episode = rows_by_episode(rows)
    for info in packet_infos:
        episode_rows = rows_for_episode.get(info.episode_id, [])
        if not episode_rows:
            fail(errors, f"{run_dir}: source_absorption.tsv missing row for {info.episode_id}")
            continue

        selected_rows = [
            row
            for row in episode_rows
            if normalized(row.get("selected_or_skipped")) == "selected"
        ]
        if not selected_rows:
            fail(errors, f"{run_dir}: source_absorption.tsv has no selected source row for {info.episode_id}")

        for row in episode_rows:
            source_label = f"{info.episode_id}/{row.get('source_class', '')}/{row.get('source_id', '')}"
            selection = normalized(row.get("selected_or_skipped"))
            if selection not in VALID_SOURCE_SELECTION:
                fail(errors, f"{run_dir}: source_absorption {source_label} selected_or_skipped must be selected/skipped")
                continue

            if is_placeholder(row.get("source_class")):
                fail(errors, f"{run_dir}: source_absorption {source_label} missing source_class")
            if is_placeholder(row.get("source_id")):
                fail(errors, f"{run_dir}: source_absorption {source_label} missing source_id")

            status = normalized(row.get("absorption_status"))
            if status not in VALID_SOURCE_ABSORPTION_STATUS:
                fail(errors, f"{run_dir}: source_absorption {source_label} invalid absorption_status {row.get('absorption_status')!r}")

            if selection == "skipped":
                if status not in {"skipped", "pass"}:
                    fail(errors, f"{run_dir}: skipped source_absorption {source_label} must use absorption_status skipped/pass")
                if is_placeholder(row.get("bound_scene")):
                    fail(errors, f"{run_dir}: skipped source_absorption {source_label} must put skip reason in bound_scene")
                continue

            if is_placeholder(row.get("bound_scene")):
                fail(errors, f"{run_dir}: selected source_absorption {source_label} missing bound_scene")

            action_fields = [
                "player_action",
                "character_action",
                "mecha_or_map_action",
                "enemy_gain_or_misuse",
                "state_delta",
            ]
            if not any(has_meaningful_source_action(row.get(column)) for column in action_fields):
                fail(
                    errors,
                    f"{run_dir}: selected source_absorption {source_label} has no player/character/mecha/enemy/state action",
                )

            if not is_truthy(row.get("reader_visible")):
                fail(errors, f"{run_dir}: selected source_absorption {source_label} must have reader_visible=yes")
            if not is_truthy(row.get("production_visible")):
                fail(errors, f"{run_dir}: selected source_absorption {source_label} must have production_visible=yes")
            if status != "pass":
                fail(errors, f"{run_dir}: selected source_absorption {source_label} must have absorption_status=pass")


def validate_writer_room_ledger(
    run_dir: Path,
    packet_infos: list[PacketInfo],
    rows: list[dict[str, str]],
    require_subagents: bool,
    require_fresh_subagents: bool,
    strict_creative_gates: bool,
    strict_writer_room: bool,
    errors: list[str],
) -> None:
    if not require_subagents or not packet_infos:
        return
    keys = {(row.get("episode_id", ""), row.get("role_id", "")): row for row in rows}
    reviewer_uses: dict[str, list[str]] = {}
    required_roles = required_review_roles(
        strict_creative_gates=strict_creative_gates,
        strict_writer_room=strict_writer_room,
    )
    for info in packet_infos:
        for role in required_roles:
            row = keys.get((info.episode_id, role))
            if not row:
                fail(errors, f"{run_dir}: writer_room_reviews.tsv missing {role} row for {info.episode_id}")
                continue
            if is_placeholder(row.get("reviewer_id")):
                fail(errors, f"{run_dir}: writer_room_reviews {info.episode_id}/{role} missing reviewer_id")
            if normalized(row.get("result")) not in VALID_REVIEW_RESULT:
                fail(errors, f"{run_dir}: writer_room_reviews {info.episode_id}/{role} invalid result {row.get('result')!r}")
            if is_placeholder(row.get("blocking_findings"), allow_none=True):
                fail(errors, f"{run_dir}: writer_room_reviews {info.episode_id}/{role} missing blocking_findings")
            if normalized(row.get("result")) == "fail" and is_placeholder(row.get("patch_actions")):
                fail(errors, f"{run_dir}: writer_room_reviews {info.episode_id}/{role} failed without patch_actions")
            if normalized(row.get("result")) == "warn" and is_placeholder(row.get("patch_actions")):
                fail(errors, f"{run_dir}: writer_room_reviews {info.episode_id}/{role} warned without patch_actions")
            reviewer_id = row.get("reviewer_id", "")
            if not is_placeholder(reviewer_id):
                reviewer_uses.setdefault(reviewer_id, []).append(f"{info.episode_id}/{role}")

    if require_fresh_subagents:
        for reviewer_id, uses in reviewer_uses.items():
            if len(uses) > 1:
                fail(
                    errors,
                    f"{run_dir}: reviewer_id {reviewer_id} reused across packet reviews: {', '.join(uses)}",
                )


def validate_chapters_and_reviews(
    run_dir: Path,
    packet_infos: list[PacketInfo],
    chapter_files: list[Path],
    review_files: list[Path],
    prefix_rows: list[dict[str, str]],
    regression_rows: list[dict[str, str]],
    unresolved_rows: list[dict[str, str]],
    require_chapter_reviews: bool,
    strict_prefix_warn_policy: bool,
    errors: list[str],
) -> None:
    chapters_by_id = {chapter_id_from_path(path): path for path in chapter_files if chapter_id_from_path(path)}
    reviews_by_id = {chapter_id_from_path(path): path for path in review_files if chapter_id_from_path(path)}
    packet_by_chapter: dict[str, list[PacketInfo]] = {}
    for info in packet_infos:
        if info.chapter_id:
            packet_by_chapter.setdefault(info.chapter_id, []).append(info)

    if require_chapter_reviews:
        for chapter_id, infos in packet_by_chapter.items():
            chapter_path = chapters_by_id.get(chapter_id)
            if not chapter_path:
                fail(errors, f"{run_dir}: missing chapter assembly for {chapter_id}")
                continue
            chapter_text = read_text(chapter_path)
            for info in infos:
                rel_packet = f"episodes/{info.path.name}"
                if rel_packet not in chapter_text and info.path.name not in chapter_text:
                    fail(errors, f"{chapter_path}: does not reference packet {rel_packet}")
            if chapter_id not in reviews_by_id:
                fail(errors, f"{run_dir}: missing prefix review for {chapter_id}")

    prefix_by_chapter = {row.get("chapter_id", ""): row for row in prefix_rows}
    review_infos: list[dict[str, str]] = []
    for review in review_files:
        review_info = validate_prefix_review(
            review,
            errors,
            strict_prefix_warn_policy=strict_prefix_warn_policy,
        )
        review_infos.append(review_info)
        chapter_id = review_info.get("chapter_id")
        if chapter_id:
            row = prefix_by_chapter.get(chapter_id)
            if not row:
                fail(errors, f"{run_dir}: prefix_reviews.tsv missing row for {chapter_id}")
            else:
                review_path = row.get("review_path", "")
                if review.name not in review_path and review_path not in {str(review), str(review.relative_to(run_dir)) if review.is_relative_to(run_dir) else ""}:
                    fail(errors, f"{run_dir}: prefix_reviews.tsv path for {chapter_id} does not reference {review.name}")
                if normalized(row.get("overall_result")) not in {"pass", "warn", "fail"}:
                    fail(errors, f"{run_dir}: prefix_reviews.tsv invalid overall_result for {chapter_id}")
                if normalized(row.get("regression_ticket_opened")) not in {"yes", "no"}:
                    fail(errors, f"{run_dir}: prefix_reviews.tsv invalid regression_ticket_opened for {chapter_id}")
                if strict_prefix_warn_policy and normalized(row.get("overall_result")) == "warn":
                    if is_placeholder(row.get("warn_classification")):
                        fail(errors, f"{run_dir}: prefix_reviews.tsv missing warn_classification for {chapter_id}")
                    if is_placeholder(row.get("blocking_issue")):
                        fail(errors, f"{run_dir}: prefix_reviews.tsv missing blocking_issue for {chapter_id}")
                    if is_placeholder(row.get("required_action")):
                        fail(errors, f"{run_dir}: prefix_reviews.tsv missing required_action for {chapter_id}")
                    if is_placeholder(row.get("ledger_rows_written")):
                        fail(errors, f"{run_dir}: prefix_reviews.tsv missing ledger_rows_written for {chapter_id}")
                    if normalized(row.get("regression_ticket_opened")) == "no" and not unresolved_rows:
                        fail(
                            errors,
                            f"{run_dir}: prefix_reviews.tsv marks {chapter_id} warn/no-ticket but unresolved_issues.tsv has no rows",
                        )

    if any(normalized(row.get("regression_ticket_opened")) == "yes" for row in prefix_rows):
        if not regression_rows:
            fail(errors, f"{run_dir}: prefix review opened regression ticket but regression_tickets.tsv has no rows")

    if strict_prefix_warn_policy:
        for review_info in review_infos:
            unresolved_text = review_info.get("unresolved_issue_carried")
            if not is_placeholder(unresolved_text, allow_none=True) and not unresolved_rows:
                fail(
                    errors,
                    f"{run_dir}: {review_info.get('chapter_id')} carries unresolved issue text but unresolved_issues.tsv has no rows",
                )

    unresolved_by_root = {row.get("root_cause_id", "") for row in unresolved_rows}
    for row in regression_rows:
        ticket_id = row.get("ticket_id", "")
        root_cause = row.get("root_cause_id", "")
        attempt_raw = row.get("attempt_no", "")
        try:
            attempt_no = int(attempt_raw)
        except ValueError:
            fail(errors, f"{run_dir}: regression ticket {ticket_id} has invalid attempt_no {attempt_raw!r}")
            attempt_no = 0
        replay_log = row.get("replay_log_path", "")
        if is_placeholder(replay_log):
            fail(errors, f"{run_dir}: regression ticket {ticket_id} missing replay_log_path")
        else:
            replay_path = run_dir / replay_log
            if not replay_path.exists():
                fail(errors, f"{run_dir}: regression ticket {ticket_id} replay log does not exist: {replay_log}")
            else:
                replay_text = read_text(replay_path)
                if "Replay range:" not in replay_text and "重放范围" not in replay_text:
                    fail(errors, f"{replay_path}: replay log missing Replay range")
        if attempt_no > 3 and root_cause not in unresolved_by_root:
            fail(errors, f"{run_dir}: root cause {root_cause} exceeded 3 attempts but is not in unresolved_issues.tsv")


def validate_run_validation_log(
    run_dir: Path,
    rows: list[dict[str, str]],
    errors: list[str],
    *,
    strict_prefix_warn_policy: bool,
    strict_creative_gates: bool,
    strict_writer_room: bool,
    require_source_absorption: bool,
    require_v35_slot_contract: bool,
) -> None:
    if not rows:
        fail(errors, f"{run_dir}: run_validation.tsv has no rows; record the final validator command and result")
        return
    has_pass = False
    for row in rows:
        command = row.get("validator_command", "")
        result = normalized(row.get("validator_result"))
        if "check_episode_loop_run.py" not in command:
            fail(errors, f"{run_dir}: run_validation row missing check_episode_loop_run.py command")
        if strict_prefix_warn_policy and "--strict-prefix-warn-policy" not in command:
            fail(errors, f"{run_dir}: strict run_validation row missing --strict-prefix-warn-policy")
        if strict_creative_gates and "--strict-creative-gates" not in command:
            fail(errors, f"{run_dir}: strict creative run_validation row missing --strict-creative-gates")
        if strict_writer_room and "--strict-writer-room" not in command:
            fail(errors, f"{run_dir}: strict writer-room run_validation row missing --strict-writer-room")
        if require_source_absorption and "--require-source-absorption" not in command:
            fail(errors, f"{run_dir}: source absorption run_validation row missing --require-source-absorption")
        if require_v35_slot_contract and "--require-v35-slot-contract" not in command:
            fail(errors, f"{run_dir}: V35 slot-contract run_validation row missing --require-v35-slot-contract")
        if result not in {"pass", "fail"}:
            fail(errors, f"{run_dir}: run_validation validator_result must be pass/fail, got {row.get('validator_result')!r}")
        if result == "pass":
            has_pass = True
    if not has_pass:
        fail(errors, f"{run_dir}: run_validation.tsv has no pass result")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Run directory with episodes/, chapters/, reviews/, ledgers/")
    parser.add_argument("--require-subagents", action="store_true", help="Require explicit subagent reviewer mode and role findings")
    parser.add_argument("--min-story-chars", type=int, default=1200, help="Minimum non-space chars in each packet Draft Synopsis")
    parser.add_argument("--require-chapter-reviews", action="store_true", help="Require one prefix review per chapter file")
    parser.add_argument("--require-run-validation-log", action="store_true", help="Require ledgers/run_validation.tsv to record a passing validator command")
    parser.add_argument(
        "--strict-prefix-warn-policy",
        action="store_true",
        help="Require prefix warn results to classify warnings, open tickets for blockers, and ledger carried issues",
    )
    parser.add_argument(
        "--strict-creative-gates",
        action="store_true",
        help="Require creative/player-facing gates: real IP-mapped new units, quote reuse control, burn/tear/gag, PV spectacle, Wanji density, and major character moves",
    )
    parser.add_argument(
        "--min-new-ip-units",
        type=int,
        default=1,
        help="Minimum countable first-appearance IP-mapped units per episode when --strict-creative-gates is used",
    )
    parser.add_argument(
        "--min-wanji-c01-samples",
        type=int,
        default=8,
        help="Minimum Wanji collection/IP-spectrum samples required in C01E01 when --strict-creative-gates is used",
    )
    parser.add_argument(
        "--allow-reused-subagent-ids",
        action="store_true",
        help="Allow the same subagent id to appear in multiple episode/role review rows",
    )
    parser.add_argument(
        "--strict-writer-room",
        action="store_true",
        help="Require the full ideal writer room roles with fresh per-role/per-episode reviewer ids; implies --require-subagents",
    )
    parser.add_argument(
        "--require-fable-review",
        action="store_true",
        help="Require one Fable fixed-review status per episode and ledgers/fable_review.tsv rows",
    )
    parser.add_argument(
        "--require-source-absorption",
        action="store_true",
        help="Require V34 source absorption markers and ledgers/source_absorption.tsv rows proving selected sources became scenes/actions",
    )
    parser.add_argument(
        "--require-v35-slot-contract",
        action="store_true",
        help="Require V35 author-slot, route, unit-lifecycle/fleet, decision-propagation, and skipped-slot ledgers; auto-detect V35.4 or V35.7 from Author Slot ID",
    )
    args = parser.parse_args(argv)
    effective_require_subagents = args.require_subagents or args.strict_writer_room

    run_dir = args.run_dir
    errors: list[str] = []

    if not run_dir.exists():
        fail(errors, f"{run_dir}: run directory does not exist")
    for subdir in ["episodes", "chapters", "reviews", "ledgers"]:
        if not (run_dir / subdir).is_dir():
            fail(errors, f"{run_dir}: missing required subdirectory {subdir}/")

    packet_infos: list[PacketInfo] = []
    episode_files = sorted((run_dir / "episodes").glob("*.md")) if (run_dir / "episodes").is_dir() else []
    if not episode_files:
        fail(errors, f"{run_dir}: episodes/ has no episode packet .md files")
    for packet in episode_files:
        packet_info = validate_packet(
            packet,
            require_subagents=effective_require_subagents,
            require_fable_review=args.require_fable_review,
            require_source_absorption=args.require_source_absorption,
            require_v35_slot_contract=args.require_v35_slot_contract,
            strict_creative_gates=args.strict_creative_gates,
            strict_writer_room=args.strict_writer_room,
            min_story_chars=args.min_story_chars,
            min_wanji_c01_samples=args.min_wanji_c01_samples,
            errors=errors,
        )
        if packet_info:
            packet_infos.append(packet_info)

    episode_ids = [info.episode_id for info in packet_infos]
    if len(episode_ids) != len(set(episode_ids)):
        fail(errors, f"{run_dir}: duplicate Episode ID values found")

    ledgers_dir = run_dir / "ledgers"
    ledgers: dict[str, list[dict[str, str]]] = {}
    if ledgers_dir.is_dir():
        ledger_files = (
            REQUIRED_LEDGER_FILES
            + (CREATIVE_LEDGER_FILES if args.strict_creative_gates else [])
            + (list(FABLE_LEDGER_COLUMNS) if args.require_fable_review else [])
            + (list(SOURCE_ABSORPTION_LEDGER_COLUMNS) if args.require_source_absorption else [])
            + (list(V35_SLOT_LEDGER_COLUMNS) if args.require_v35_slot_contract else [])
        )
        for ledger in ledger_files:
            path = ledgers_dir / ledger
            if not path.exists():
                fail(errors, f"{run_dir}: missing required ledger ledgers/{ledger}")
            else:
                header, rows = validate_ledger(path, errors)
                if args.strict_creative_gates:
                    validate_creative_ledger_header(path, header, errors)
                if args.require_fable_review:
                    validate_fable_ledger_header(path, header, errors)
                if args.require_source_absorption:
                    validate_source_absorption_ledger_header(path, header, errors)
                if args.require_v35_slot_contract:
                    validate_v35_slot_ledger_header(path, header, errors)
                ledgers[ledger] = rows

        validate_packet_index(
            run_dir,
            packet_infos,
            ledgers.get("episode_packet_index.tsv", []),
            errors,
        )
        validate_writer_room_ledger(
            run_dir,
            packet_infos,
            ledgers.get("writer_room_reviews.tsv", []),
            effective_require_subagents,
            effective_require_subagents and (args.strict_writer_room or not args.allow_reused_subagent_ids),
            args.strict_creative_gates,
            args.strict_writer_room,
            errors,
        )
        if args.require_fable_review:
            validate_fable_review_ledger(
                run_dir,
                packet_infos,
                ledgers.get("fable_review.tsv", []),
                errors,
            )
        if args.require_source_absorption:
            validate_source_absorption_ledger(
                run_dir,
                packet_infos,
                ledgers.get("source_absorption.tsv", []),
                errors,
            )
        if args.strict_creative_gates:
            validate_strict_creative_ledgers(
                run_dir,
                packet_infos,
                ledgers,
                errors,
                min_new_ip_units=args.min_new_ip_units,
                min_wanji_c01_samples=args.min_wanji_c01_samples,
                require_v35_slot_contract=args.require_v35_slot_contract,
            )
        if args.require_v35_slot_contract:
            validate_v35_slot_contract(
                run_dir,
                packet_infos,
                ledgers,
                errors,
            )

    review_files = sorted((run_dir / "reviews").glob("*prefix-review*.md")) if (run_dir / "reviews").is_dir() else []
    chapter_files = sorted((run_dir / "chapters").glob("*.md")) if (run_dir / "chapters").is_dir() else []
    if args.require_chapter_reviews and chapter_files and not review_files:
        fail(errors, f"{run_dir}: chapters exist but no prefix reviews found")
    validate_chapters_and_reviews(
        run_dir,
        packet_infos,
        chapter_files,
        review_files,
        ledgers.get("prefix_reviews.tsv", []),
        ledgers.get("regression_tickets.tsv", []),
        ledgers.get("unresolved_issues.tsv", []),
        args.require_chapter_reviews,
        args.strict_prefix_warn_policy,
        errors,
    )
    if args.require_run_validation_log:
        validate_run_validation_log(
            run_dir,
            ledgers.get("run_validation.tsv", []),
            errors,
            strict_prefix_warn_policy=args.strict_prefix_warn_policy,
            strict_creative_gates=args.strict_creative_gates,
            strict_writer_room=args.strict_writer_room,
            require_source_absorption=args.require_source_absorption,
            require_v35_slot_contract=args.require_v35_slot_contract,
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} issue(s)", file=sys.stderr)
        return 1

    print(
        f"PASS: {run_dir} has {len(episode_files)} episode packet(s), "
        f"{len(chapter_files)} chapter file(s), {len(review_files)} prefix review(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
