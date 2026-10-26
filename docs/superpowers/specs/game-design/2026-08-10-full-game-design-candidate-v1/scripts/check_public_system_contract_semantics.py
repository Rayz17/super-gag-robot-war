#!/usr/bin/env python3
"""Validate public-loop semantic repairs in the Candidate package.

This is a static contract checker.  It deliberately does not claim a Build,
playtest evidence, user acceptance, Canon migration, or Runtime integration.
"""

from __future__ import annotations

import argparse
import copy
import csv
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ERRORS: list[str] = []

EXPECTED_HUB_PRESENTATIONS = {
    "HUB_WALK_RESPOND": "instant_or_optional_scene",
    "HUB_REL_EVENT": "scene",
    "HUB_REPAIR": "playable_activity_or_scene_by_work_order",
    "HUB_LOADOUT": "instant_preview_or_playable_install",
    "HUB_CURATE": "scene_or_instant",
    "HUB_INVESTIGATE": "playable_activity_or_instant_compare_if_all_sources_already_acquired",
    "HUB_OPEN_EVENT": "playable_activity",
    "HUB_DISPATCH": "instant_or_scene",
    "HUB_PREPARE": "instant_preview",
    "HUB_REST_CARE": "optional_scene_or_playable_major_care",
    "HUB_DEPART": "instant_commit",
}
HUB_PRESENTATION_ROOTS = {"playable_activity", "scene", "instant"}


def load_tsv(name: str) -> list[dict[str, str]]:
    path = DATA_DIR / name
    if not path.is_file():
        ERRORS.append(f"missing table: data/{name}")
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames:
            ERRORS.append(f"empty header: data/{name}")
            return []
        rows: list[dict[str, str]] = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                ERRORS.append(f"data/{name}:{line_number}: too many TSV cells")
                continue
            missing = [key for key, value in row.items() if value is None]
            if missing:
                ERRORS.append(
                    f"data/{name}:{line_number}: missing cells for {','.join(missing)}"
                )
                continue
            rows.append({key: value.strip() for key, value in row.items()})
        return rows


def keyed(rows: list[dict[str, str]], key: str, table: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value:
            ERRORS.append(f"{table}: blank {key}")
        elif value in result:
            ERRORS.append(f"{table}: duplicate {key}={value}")
        else:
            result[value] = row
    return result


def tokens(value: str) -> set[str]:
    return {item.strip() for item in value.split(";") if item.strip()}


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def require_contains(value: str, required: set[str], message: str) -> None:
    missing = sorted(item for item in required if item not in value)
    require(not missing, f"{message}; missing={','.join(missing)}")


def row_text(row: dict[str, str]) -> str:
    return "|".join(row.values())


def settlement_keeps_facts_readonly(row: dict[str, str]) -> bool:
    choices = row.get("allowed_player_choices", "")
    forbidden = row.get("must_not_do", "")
    return (
        all(marker in choices for marker in ("事实只读", "返回Owner", "不得生成新选择"))
        and "让玩家校验或批准事实" in forbidden
        and "结算" in forbidden
        and "新选" in forbidden
    )


def mapping_keys(value: str) -> set[str]:
    result: set[str] = set()
    for item in tokens(value):
        key, separator, _ = item.partition("=")
        if separator and key:
            result.add(key)
    return result


def hub_presentations_complete(
    actions_by_id: dict[str, dict[str, str]],
) -> bool:
    if set(actions_by_id) != set(EXPECTED_HUB_PRESENTATIONS):
        return False
    roots_seen: set[str] = set()
    for action_id, expected in EXPECTED_HUB_PRESENTATIONS.items():
        actual = actions_by_id[action_id].get("presentation_class", "")
        if actual != expected:
            return False
        roots = {root for root in HUB_PRESENTATION_ROOTS if root in actual}
        if not roots:
            return False
        roots_seen.update(roots)
    return roots_seen == HUB_PRESENTATION_ROOTS


def hub_prepare_is_free_preview(row: dict[str, str]) -> bool:
    return (
        row.get("slot_cost") == "0"
        and tokens(row.get("player_verbs", ""))
        == {"inspect", "assign", "reserve", "route", "preview"}
        and "commit" not in tokens(row.get("player_verbs", ""))
        and tokens(row.get("required_inputs", ""))
        == {
            "mission_card",
            "roster",
            "body",
            "roles",
            "route",
            "promises",
            "equipment",
            "authority",
            "consent",
        }
        and row.get("actor_conflicts") == "preview_only_until_mission_commitment"
        and tokens(row.get("result_domains", ""))
        == {
            "preview_only",
            "MISSION-COMMIT-V1_later_locks_ST_ROSTER/ST_ROUTE/ST_OPERATION",
        }
        and "0时间0资源0写入" in row.get("failure_or_delay", "")
        and "查看清单就锁定对象" in row.get("must_not_become", "")
        and row.get("presentation_class") == "instant_preview"
    )


def hub_curate_requests_physical_transfer_only(row: dict[str, str]) -> bool:
    result_domains = tokens(row.get("result_domains", ""))
    return (
        tokens(row.get("player_verbs", ""))
        == {"compare", "label", "display", "withhold", "request_transfer"}
        and "return" not in tokens(row.get("player_verbs", ""))
        and tokens(row.get("required_inputs", ""))
        == {
            "collection_entry",
            "ST_EQUIPMENT_projection",
            "reveal_scope",
            "space",
            "related_people",
        }
        and "physical_transfer_request_only" in result_domains
        and "ST_EQUIPMENT" not in result_domains
        and "实物Owner拒绝" in row.get("failure_or_delay", "")
        and "实物位置只读投影" in row.get("visible_feedback", "")
        and "直接改变产权/保管/实物位置" in row.get("must_not_become", "")
    )


def hub_state_has_presentation_semantics(row: dict[str, str]) -> bool:
    return (
        "presentation_classes" in tokens(row.get("minimum_fields", ""))
        and all(
            marker in row.get("mutation_rule", "")
            for marker in (
                "同格最多一张playable_activity",
                "其余为instant或scene",
                "从同一格前态结算",
                "界面顺序体验",
            )
        )
        and "呈现顺序改变业务态" in row.get("must_not_be_used_as", "")
    )


def sog_hub_has_three_presentation_classes(row: dict[str, str]) -> bool:
    return (
        "presentation_classes" in tokens(row.get("prepare_inputs", ""))
        and all(
            marker in row.get("owner_validation", "")
            for marker in (
                "同一格最多一张playable_activity",
                "其余只可instant或scene",
            )
        )
        and "按玩家界面顺序呈现" in row.get("atomic_commit_rule", "")
        and "从同一格前态结算" in row.get("atomic_commit_rule", "")
        and "呈现顺序不得改变业务态" in row.get("reject_or_timeout", "")
        and "呈现类型" in row.get("player_projection_rule", "")
    )


def system_hub_has_public_budget(row: dict[str, str]) -> bool:
    exit_condition = row.get("exit_condition", "")
    return (
        "标准3格" in exit_condition
        and "最多3张工作卡" in exit_condition
        and "2至5个事项组" in exit_condition
        and "只负责提示" in exit_condition
        and "2至5个行动" not in exit_condition
    )


def emt008_has_public_budget(row: dict[str, str]) -> bool:
    return (
        row.get("normalized_mode") == "hub"
        and row.get("owner_system") == "SYS-HUB"
        and row.get("boundary_kind") == "hub_cycle"
        and row.get("action_budget_rule")
        == "2_to_5_issue_groups_plus_max_3_work_cards"
        and "2至5个事项组" in row.get("business_state_rule", "")
        and "标准3格内最多3张工作卡" in row.get("business_state_rule", "")
        and "把事项组写成额外行动次数" in row.get("must_not_be_treated_as", "")
    )


def res_hub_slots_has_public_budget(row: dict[str, str]) -> bool:
    return (
        row.get("classification") == "scheduling_resource"
        and row.get("owner_system") == "SYS-HUB"
        and row.get("scope") == "hub_cycle"
        and all(
            marker in row.get("sources", "")
            for marker in (
                "标准周期固定3格",
                "最多提交3张工作卡",
                "2至5个事项组",
            )
        )
        and "逐格整组提交" in row.get("cap_or_scarcity", "")
        and "分别占工作卡名额" in row.get("cap_or_scarcity", "")
        and "离馆或周期结束重置" in row.get("reset_or_persistence", "")
        and "事项组当额外行动" in row.get("forbidden_conversion", "")
    )


def pw_d01_has_separate_issue_slot_card_fields(row: dict[str, str]) -> bool:
    expected_outputs = {
        "hub_cycle_id",
        "issue_groups",
        "time_slots",
        "work_card_cap",
        "visible_changes",
    }
    return (
        tokens(row.get("receipt_or_output", "")) == expected_outputs
        and "2至5个UI问题" in row.get("fixed_story_guard", "")
        and "标准周期固定3格" in row.get("fixed_story_guard", "")
        and "最多3张工作卡" in row.get("fixed_story_guard", "")
        and "3_available_actions" not in row_text(row)
    )


def pw_d08_keeps_prepare_preview_free(row: dict[str, str]) -> bool:
    required = tokens(row.get("required_inputs", ""))
    return (
        "presentation_classes" in required
        and "assignment_preview" in required
        and "assignment_changes" not in required
        and "第三时间格提交关系承诺工作卡" in row.get("player_commitment", "")
        and "免费查看任务准备草案" in row.get("player_commitment", "")
        and "任务准备预览0格0写入" in row.get("fixed_story_guard", "")
        and "不计第四张卡" in row.get("fixed_story_guard", "")
        and "同格最多一张playable_activity" in row.get("fixed_story_guard", "")
        and "第三张工作卡完成" in row.get("expected_closure", "")
        and "直到Mission Commit才锁定" in row.get("expected_closure", "")
        and "ST_ROSTER" not in tokens(row.get("state_domains_touched", ""))
    )


def neutral_hub_payload_bindings_preserve_free_preview(
    bindings_by_id: dict[str, dict[str, str]],
) -> bool:
    d01 = bindings_by_id.get("PLB-D01", {})
    d08 = bindings_by_id.get("PLB-D08", {})
    expected_d01 = {
        "hub_cycle_id",
        "issue_groups",
        "time_slots",
        "work_card_cap",
        "visible_changes",
    }
    d08_inputs = mapping_keys(d08.get("required_input_sources", ""))
    return (
        mapping_keys(d01.get("committed_output_refs", "")) == expected_d01
        and mapping_keys(d01.get("output_primary_consumers", "")) == expected_d01
        and "available_actions" not in row_text(d01)
        and "presentation_classes" in d08_inputs
        and "assignment_preview" in d08_inputs
        and "assignment_changes" not in d08_inputs
    )


def check_settlement_owner_choices() -> None:
    settlements = load_tsv("settlement-contracts.tsv")
    require(
        {row.get("settlement_level") for row in settlements}
        == {"ENCOUNTER", "OPERATION", "CHAPTER"},
        "settlement-contracts: expected exactly ENCOUNTER/OPERATION/CHAPTER",
    )
    for row in settlements:
        level = row.get("settlement_level", "UNKNOWN")
        require(
            "owner_decision_receipt_ids" in tokens(row.get("required_inputs", "")),
            f"{level}: settlement must consume owner_decision_receipt_ids",
        )
        require(
            settlement_keeps_facts_readonly(row),
            f"{level}: settlement must keep facts read-only, return choices to Owner modes, and forbid fact approval/new choices",
        )
    encounter = next((row for row in settlements if row.get("settlement_level") == "ENCOUNTER"), {})
    operation = next((row for row in settlements if row.get("settlement_level") == "OPERATION"), {})
    chapter = next((row for row in settlements if row.get("settlement_level") == "CHAPTER"), {})
    require_contains(
        "|".join(encounter.values()),
        {"Operation结束", "不单独", "两次"},
        "ENCOUNTER: operation-end encounter facts must not create a first approval page",
    )
    require(
        {"encounter_fact_proposal_refs", "operation_proposal"}.issubset(
            tokens(operation.get("required_inputs", ""))
        ),
        "OPERATION: merged frontend must consume both backend proposal layers",
    )
    require_contains(
        "|".join(operation.values()),
        {"一个合并摘要", "一个最终", "同transaction_group", "两次"},
        "OPERATION: one merged summary and one final submit are required",
    )
    require_contains(
        "|".join(chapter.values()),
        {"真正章末", "单独显示"},
        "CHAPTER: separate summary is legal only at actual chapter end",
    )

    receipt_rows = load_tsv("owner-decision-receipt-schema.tsv")
    receipt_by_field = keyed(
        receipt_rows, "field_id", "owner-decision-receipt-schema.tsv"
    )
    expected = {
        "owner_decision_receipt_id",
        "owner_system",
        "owner_mode",
        "choice_id",
        "selected_option_id",
        "source_state_versions",
        "prepared_at_checkpoint",
        "expires_at_or_boundary",
        "player_summary",
        "status",
    }
    require(
        set(receipt_by_field) == expected,
        "owner-decision-receipt-schema: field set drift",
    )
    for field_id, row in receipt_by_field.items():
        require(row.get("required") == "yes", f"{field_id}: receipt field must be required")
        require(
            row.get("produced_by") == "owning_system_mode",
            f"{field_id}: decision receipt must be produced in Owner mode",
        )


def check_hub_action_and_resolution() -> None:
    state_by_id = keyed(
        load_tsv("system-state-contracts.tsv"),
        "state_id",
        "system-state-contracts.tsv",
    )
    hub = state_by_id.get("ST_HUB_ACTION", {})
    expected_fields = {
        "slot_commit_id",
        "hub_cycle_id",
        "time_slot_id",
        "card_ids",
        "card_bindings",
        "presentation_classes",
        "participant_ids",
        "body_ids",
        "facility_ids",
        "tool_item_ids",
        "duration_slots_by_card",
        "card_costs",
        "facility_capacity_costs",
        "group_preflight",
        "conflicts",
        "opportunity_cost",
        "preview",
        "card_performed_outcomes",
        "slot_receipt_id",
        "commit_status",
    }
    require(
        tokens(hub.get("minimum_fields", "")) == expected_fields,
        "ST_HUB_ACTION: minimum field set must describe a complete per-slot action card",
    )
    require(hub.get("owner_system") == "SYS-HUB", "ST_HUB_ACTION: owner must be SYS-HUB")
    require_contains(
        hub.get("mutation_rule", ""),
        {"precondition_reject", "performed", "HUB_SLOT_COMMIT", "时间只推进一次", "固定3个time_slot", "最多提交3张work_card", "2至5个issue_group"},
        "ST_HUB_ACTION: mutation semantics incomplete",
    )
    require(
        hub_state_has_presentation_semantics(hub),
        "ST_HUB_ACTION: presentation classes/order-independent business semantics incomplete",
    )

    owner_by_id = keyed(
        load_tsv("settlement-owner-prepare-commit-contracts.tsv"),
        "owner_group_id",
        "settlement-owner-prepare-commit-contracts.tsv",
    )
    hub_owner = owner_by_id.get("SOG-HUB", {})
    require(
        {
            "slot_commit_id",
            "time_slot_id",
            "card_ids",
            "card_bindings",
            "presentation_classes",
            "participant_ids",
            "body_ids",
            "facility_ids",
            "tool_item_ids",
            "duration_slots_by_card",
            "card_costs",
            "facility_capacity_costs",
            "group_preflight",
        }.issubset(tokens(hub_owner.get("prepare_inputs", ""))),
        "SOG-HUB: action prepare inputs are incomplete",
    )
    require_contains(
        "|".join(hub_owner.values()),
        {"precondition_reject", "performed", "部分提交", "一个slot receipt", "时间只推进一次", "固定3个time_slot", "最多提交3张work_card", "issue_group"},
        "SOG-HUB: reject and performed failure must be distinct",
    )
    require(
        sog_hub_has_three_presentation_classes(hub_owner),
        "SOG-HUB: playable_activity/scene/instant presentation contract incomplete",
    )

    edge_by_id = keyed(
        load_tsv("system-edge-contracts.tsv"),
        "edge_id",
        "system-edge-contracts.tsv",
    )
    hub_edge = edge_by_id.get("EDGE_HUB_SETTLE", {})
    require(
        hub_edge.get("timing_priority") == "per_time_slot_group_commit",
        "EDGE_HUB_SETTLE: one complete slot group must commit atomically",
    )
    require(hub_edge.get("commit_point") == "hub_slot_receipt", "EDGE_HUB_SETTLE: one slot receipt required")
    require_contains(
        "|".join(hub_edge.values()),
        {"HUB_SLOT_COMMIT", "时间只推进一次", "不得部分提交", "card_performed_outcomes"},
        "EDGE_HUB_SETTLE: grouped preflight/outcome semantics incomplete",
    )

    hub_actions = keyed(
        load_tsv("hub-action-contracts.tsv"),
        "hub_action_id",
        "hub-action-contracts.tsv",
    )
    require(
        hub_presentations_complete(hub_actions),
        "hub-action-contracts: presentation_class coverage/mapping drift",
    )
    require(
        hub_prepare_is_free_preview(hub_actions.get("HUB_PREPARE", {})),
        "HUB_PREPARE: must remain a zero-slot preview-only draft until Mission Commitment",
    )
    require(
        hub_curate_requests_physical_transfer_only(
            hub_actions.get("HUB_CURATE", {})
        ),
        "HUB_CURATE: may only read ST_EQUIPMENT projection and request physical transfer",
    )

    repair_action = hub_actions.get("HUB_REPAIR", {})
    require(
        repair_action.get("slot_cost") == "light=1_slot;standard=2_consecutive_slots;heavy=3_consecutive_slots",
        "HUB_REPAIR: duration must be determined by explicit work-order mapping",
    )

    resolution_by_class = keyed(
        load_tsv("action-resolution-semantics.tsv"),
        "resolution_class",
        "action-resolution-semantics.tsv",
    )
    require(
        set(resolution_by_class)
        == {
            "CANCEL_BEFORE_COMMIT",
            "PRECONDITION_REJECT",
            "PERFORMED_SUCCESS",
            "PERFORMED_FAIL",
        },
        "action-resolution-semantics: expected four disjoint outcomes",
    )
    reject = resolution_by_class.get("PRECONDITION_REJECT", {})
    require(reject.get("execution_started") == "no", "PRECONDITION_REJECT: must not start")
    require_contains(
        "|".join(reject.values()),
        {"0_slot", "0_capacity", "0_consumption", "no_persistent_state_write"},
        "PRECONDITION_REJECT: zero-cost/zero-write rules incomplete",
    )
    performed_fail = resolution_by_class.get("PERFORMED_FAIL", {})
    require(performed_fail.get("execution_started") == "yes", "PERFORMED_FAIL: execution must start")
    require(performed_fail.get("accepted_commit") == "yes", "PERFORMED_FAIL: result must commit")
    require_contains(
        "|".join(performed_fail.values()),
        {"consume_declared_time_slots", "consume_actual_reserved_capacity", "do_not_refund_as_unperformed"},
        "PERFORMED_FAIL: actual costs must remain",
    )


def check_repair_capacity() -> None:
    economy_by_id = keyed(
        load_tsv("economy-flows.tsv"), "resource_id", "economy-flows.tsv"
    )
    repair = economy_by_id.get("RES_REPAIR_CAPACITY", {})
    require(repair.get("display_name") == "维修设备容量", "RES_REPAIR_CAPACITY: display name drift")
    require(repair.get("classification") == "resetting_resource", "RES_REPAIR_CAPACITY: class drift")
    require(repair.get("owner_system") == "SYS-HUB", "RES_REPAIR_CAPACITY: owner must be SYS-HUB")
    require(repair.get("scope") == "hub_cycle", "RES_REPAIR_CAPACITY: scope must be hub_cycle")
    require_contains(
        repair.get("sources", ""),
        {"重吊位", "修理台", "承力测试台"},
        "RES_REPAIR_CAPACITY: physical equipment sources incomplete",
    )
    require_contains(
        repair.get("reset_or_persistence", ""),
        {"周期结束", "不结转", "重建"},
        "RES_REPAIR_CAPACITY: cycle reset rule incomplete",
    )
    require_contains(
        repair.get("forbidden_conversion", ""),
        {"precondition_reject", "performed_fail", "人员工时"},
        "RES_REPAIR_CAPACITY: reject/failure/person-time distinction incomplete",
    )


def check_hub_public_budget_and_neutral_trace() -> None:
    systems_by_id = keyed(
        load_tsv("system-node-contracts.tsv"),
        "system_id",
        "system-node-contracts.tsv",
    )
    require(
        system_hub_has_public_budget(systems_by_id.get("SYS-HUB", {})),
        "SYS-HUB: 2-5 issue groups / fixed 3 slots / max 3 work cards drift",
    )

    episode_modes_by_id = keyed(
        load_tsv("episode-mode-token-contracts.tsv"),
        "rule_id",
        "episode-mode-token-contracts.tsv",
    )
    require(
        emt008_has_public_budget(episode_modes_by_id.get("EMT008", {})),
        "EMT008: Hub issue-group/slot/work-card budget drift",
    )

    economy_by_id = keyed(
        load_tsv("economy-flows.tsv"),
        "resource_id",
        "economy-flows.tsv",
    )
    require(
        res_hub_slots_has_public_budget(economy_by_id.get("RES_HUB_SLOTS", {})),
        "RES_HUB_SLOTS: Hub scheduling semantics drift",
    )

    traces_by_id = keyed(
        load_tsv("core-loop-paper-walkthrough-traces.tsv"),
        "trace_step_id",
        "core-loop-paper-walkthrough-traces.tsv",
    )
    require(
        pw_d01_has_separate_issue_slot_card_fields(traces_by_id.get("PW-D01", {})),
        "PW-D01: issue groups, time slots, and work-card cap must stay separate",
    )
    require(
        pw_d08_keeps_prepare_preview_free(traces_by_id.get("PW-D08", {})),
        "PW-D08: free mission-preparation preview must not become a fourth paid card",
    )

    bindings_by_id = keyed(
        load_tsv("core-loop-payload-bindings.tsv"),
        "binding_id",
        "core-loop-payload-bindings.tsv",
    )
    require(
        neutral_hub_payload_bindings_preserve_free_preview(bindings_by_id),
        "PLB-D01/PLB-D08: neutral Hub payloads reintroduced available actions or paid preparation",
    )

    transitions_by_id = keyed(
        load_tsv("mode-transition-contracts.tsv"),
        "transition_id",
        "mode-transition-contracts.tsv",
    )
    story_hub = transitions_by_id.get("TR_STORY_HUB", {})
    require(
        tokens(story_hub.get("committed_outputs", ""))
        == {
            "hub_cycle_id",
            "issue_groups",
            "time_slots",
            "work_card_cap",
            "visible_changes",
        },
        "TR_STORY_HUB: must commit separate issue-group/slot/card-cap fields",
    )
    hub_settle = transitions_by_id.get("TR_HUB_SETTLE", {})
    hub_settle_inputs = tokens(hub_settle.get("required_inputs", ""))
    require(
        "presentation_classes" in hub_settle_inputs
        and "assignment_preview" in hub_settle_inputs
        and "assignment_changes" not in hub_settle_inputs,
        "TR_HUB_SETTLE: presentation classes and free assignment preview drift",
    )
    require_contains(
        "|".join(hub_settle.values()),
        {
            "同格最多一张playable_activity",
            "呈现顺序不改业务态",
            "任务编组预览不写状态",
        },
        "TR_HUB_SETTLE: presentation/order/free-preview semantics incomplete",
    )


def check_dual_time_scale() -> None:
    bridges = load_tsv("time-scale-bridge-contracts.tsv")
    expected_adapters = {"SCA-P1-A", "SCA-P1-B", "SCA-P1-C", "SCA-P1-D"}
    require(
        {row.get("scheduler_adapter_id") for row in bridges} == expected_adapters,
        "time-scale bridge: scheduler adapter coverage drift",
    )
    for row in bridges:
        bridge_id = row.get("bridge_id", "UNKNOWN")
        require(row.get("encounter_clock_field") == "encounter_elapsed_ms", f"{bridge_id}: encounter clock drift")
        require(row.get("campaign_clock_field") == "campaign_tick", f"{bridge_id}: campaign clock drift")
        require_contains(
            row.get("scale_bridge_rule", ""),
            {"never_convert", "encounter_elapsed_ms", "campaign_tick"},
            f"{bridge_id}: direct clock conversion must be forbidden",
        )
        require(row.get("build_status") == "zero_build", f"{bridge_id}: Build claim must remain zero_build")
        require(row.get("human_evidence_status") == "not_run", f"{bridge_id}: human evidence must remain not_run")

    runstate_by_type = keyed(
        load_tsv("runstate-v2-field-schema.tsv"),
        "record_type",
        "runstate-v2-field-schema.tsv",
    )
    clock = runstate_by_type.get("WORLD_CLOCK_V2", {})
    require(
        {"encounter_elapsed_ms:T_INT_NONNEG", "campaign_tick:T_INT_NONNEG"}.issubset(
            tokens(clock.get("optional_fields_typed", ""))
        ),
        "WORLD_CLOCK_V2: dual-scale adapter fields missing",
    )
    require_contains(
        clock.get("fixed_constraints", ""),
        {"no direct", "millisecond", "campaign"},
        "WORLD_CLOCK_V2: direct conversion ban missing",
    )


def check_mission_commitment_and_sortie() -> None:
    mission_rows = load_tsv("mission-commitment-contracts.tsv")
    require(len(mission_rows) == 1, "mission commitment: expected exactly one public v1 contract")
    mission = mission_rows[0] if mission_rows else {}
    require(mission.get("contract_id") == "MISSION-COMMIT-V1", "mission commitment: ID drift")
    require(
        {
            "mission_card_ref",
            "route_ref",
            "sortie_manifest_ref",
            "operation_commitment_ref",
            "unselected_policy_ref",
            "owner_decision_receipt_ids",
            "operating_funds_before",
            "operating_funds_reserved",
            "campaign_tick_before",
            "campaign_tick_delta",
            "arrival_tick",
        }.issubset(tokens(mission.get("required_inputs", ""))),
        "MISSION-COMMIT-V1: input set is not atomic-complete",
    )
    require_contains(
        mission.get("atomic_payload", ""),
        {"route_id@version@sha256", "sortie_manifest_id@version@sha256", "operation_commitment_id", "offered_to_committed", "selected_route_ref", "locked_sortie_manifest_ref", "arrival_tick", "unselected_policy_ref", "operating_funds_before_reserved_after", "campaign_tick_before_delta_after"},
        "MISSION-COMMIT-V1: route/sortie/time/funds payload incomplete",
    )
    require_contains(
        mission.get("precondition_reject", ""),
        {"0写入", "释放", "campaign_tick", "资金", "出击锁定"},
        "MISSION-COMMIT-V1: rejection must atomically release and write nothing",
    )
    require_contains(
        mission.get("performed_fail_after_departure", ""),
        {"accepted", "不回滚", "fail_continue", "withdraw", "resolved"},
        "MISSION-COMMIT-V1: after-departure failure must continue forward",
    )

    edge_by_id = keyed(
        load_tsv("system-edge-contracts.tsv"),
        "edge_id",
        "system-edge-contracts.tsv",
    )
    edge = edge_by_id.get("EDGE_HUB_WORLD", {})
    require(edge.get("commit_point") == "mission_commitment_receipt", "EDGE_HUB_WORLD: commit point drift")
    require_contains(
        edge.get("postcondition", ""),
        {"ST_OPERATION", "offered", "committed", "selected_route_ref", "locked_sortie_manifest_ref", "arrival_tick", "campaign_tick", "运营资金"},
        "EDGE_HUB_WORLD: atomic postcondition incomplete",
    )

    transition_by_id = keyed(
        load_tsv("mode-transition-contracts.tsv"),
        "transition_id",
        "mode-transition-contracts.tsv",
    )
    transition = transition_by_id.get("TR_HUB_WORLD", {})
    require(
        {
            "mission_card_ref",
            "route_ref",
            "sortie_manifest_ref",
            "operation_commitment_ref",
            "unselected_policy_ref",
            "arrival_tick",
            "owner_decision_receipt_ids",
            "operating_funds_reservation",
            "campaign_tick_before",
        } == tokens(transition.get("required_inputs", "")),
        "TR_HUB_WORLD: commitment input fields drift",
    )
    require(
        {
            "mission_commitment_receipt",
            "operation_commitment_ref",
            "selected_route_ref",
            "locked_sortie_manifest_ref",
            "arrival_tick",
            "campaign_tick_after",
            "operating_funds_after",
        } == tokens(transition.get("committed_outputs", "")),
        "TR_HUB_WORLD: commitment output fields drift",
    )

    manifest_rows = load_tsv("sortie-manifest-contracts.tsv")
    references = [row for row in manifest_rows if row.get("row_kind") == "reference"]
    expected_classes = {
        "mission_card",
        "route",
        "roster_assignment",
        "body_state",
        "equipment_custody",
        "authority_consent",
    }
    require(
        {row.get("reference_class") for row in references} == expected_classes
        and len(references) == 6,
        "sortie manifest: expected exactly six versioned reference classes",
    )
    for row in references:
        require_contains(
            row.get("wire_contract", ""),
            {"version", "sha256"},
            f"{row.get('row_id')}: reference must lock version and sha256",
        )
    view_row = next(
        (row for row in manifest_rows if row.get("row_id") == "SORTIE-CONTROL-VIEW"),
        {},
    )
    require_contains(
        view_row.get("view_rule", ""),
        {"0_hub_slot", "0_campaign_tick", "0_funds", "0_state_mutation"},
        "sortie manifest: view/preview/lock inspection must cost zero time and funds",
    )

    mission_card_by_field = keyed(
        load_tsv("mission-card-schema.tsv"), "field_id", "mission-card-schema.tsv"
    )
    require(
        {"mission_card_version", "sortie_manifest_contract", "mission_commitment_preview"}.issubset(
            mission_card_by_field
        ),
        "mission-card-schema: version/sortie/commitment fields missing",
    )

    state_by_id = keyed(
        load_tsv("system-state-contracts.tsv"), "state_id", "system-state-contracts.tsv"
    )
    operation = state_by_id.get("ST_OPERATION", {})
    lifecycle_fields = {
        "commitment_id",
        "commitment_state",
        "mission_card_ref",
        "selected_route_ref",
        "locked_sortie_manifest_ref",
        "arrival_tick",
        "unselected_policy_ref",
    }
    require(
        lifecycle_fields.issubset(tokens(operation.get("minimum_fields", ""))),
        "ST_OPERATION: persistent Mission Commitment lifecycle fields missing",
    )
    require_contains(
        operation.get("mutation_rule", ""),
        {"offered→committed→traveling→arrived→resolved", "accepted mission_commitment_receipt", "selected_route_ref", "locked_sortie_manifest_ref", "arrival_tick", "unselected_policy_ref"},
        "ST_OPERATION: lifecycle transition rule incomplete",
    )
    runstate_operation = keyed(
        load_tsv("runstate-v2-field-schema.tsv"),
        "record_type",
        "runstate-v2-field-schema.tsv",
    ).get("DOMAIN_ST_OPERATION_V2", {})
    require(
        {f"{field}:" for field in lifecycle_fields}.issubset(
            {item.split(":", 1)[0] + ":" for item in tokens(runstate_operation.get("required_fields_typed", ""))}
        ),
        "DOMAIN_ST_OPERATION_V2: lifecycle wire fields missing",
    )
    require_contains(
        runstate_operation.get("fixed_constraints", ""),
        {"offered|committed|traveling|arrived|resolved", "accepted mission_commitment_receipt", "unselected_policy_ref"},
        "DOMAIN_ST_OPERATION_V2: lifecycle constraints incomplete",
    )


def check_equipment_custody() -> None:
    state_by_id = keyed(
        load_tsv("system-state-contracts.tsv"),
        "state_id",
        "system-state-contracts.tsv",
    )
    equipment = state_by_id.get("ST_EQUIPMENT", {})
    physical_truth_fields = {
        "lawful_owner",
        "current_holder",
        "physical_location",
        "loan_terms",
        "transfer_receipt_id",
        "slot",
        "installed_state",
    }
    require(equipment.get("owner_system") == "SYS-BODY", "ST_EQUIPMENT: owner must be SYS-BODY")
    require(
        physical_truth_fields.issubset(tokens(equipment.get("minimum_fields", "")))
        and "owner" not in tokens(equipment.get("minimum_fields", "")),
        "ST_EQUIPMENT: explicit physical-truth fields must replace ambiguous owner",
    )
    writers = tokens(equipment.get("legal_writers", ""))
    require("SYS-BODY" in writers, "ST_EQUIPMENT: SYS-BODY writer missing")
    require("SYS-HUB" not in writers and "SYS-ARCH" not in writers, "ST_EQUIPMENT: HUB/ARCH must not write custody")
    require_contains(
        equipment.get("mutation_rule", ""),
        {"lawful_owner", "current_holder", "physical_location", "loan_terms", "transfer_receipt_id", "槽位", "装配态", "同一item_id", "SYS-ARCH", "不得直写"},
        "ST_EQUIPMENT: unique physical custody rule incomplete",
    )
    collection = state_by_id.get("ST_COLLECTION", {})
    require(
        not ({"custody", "current_holder", "physical_custody"} & tokens(collection.get("minimum_fields", ""))),
        "ST_COLLECTION: must not persist a second physical custody field",
    )
    membership = state_by_id.get("ST_MEMBERSHIP", {})
    require(
        "custody" not in tokens(membership.get("minimum_fields", ""))
        and "membership_responsibility_ref" in tokens(membership.get("minimum_fields", "")),
        "ST_MEMBERSHIP: organizational responsibility must not be a second custody field",
    )
    require_contains(
        membership.get("mutation_rule", ""),
        {"membership_responsibility_ref", "ST_EQUIPMENT", "不记任何装备实物"},
        "ST_MEMBERSHIP: physical truth projection boundary missing",
    )

    owner_by_id = keyed(
        load_tsv("settlement-owner-prepare-commit-contracts.tsv"),
        "owner_group_id",
        "settlement-owner-prepare-commit-contracts.tsv",
    )
    archive_owner = owner_by_id.get("SOG-ARCH", {})
    require_contains(
        "|".join(archive_owner.values()),
        {"equipment_physical_truth_projection_ref", "physical_transfer_request", "SOG-BODY", "不直写", "lawful_owner", "current_holder", "physical_location", "loan_terms", "transfer_receipt_id"},
        "SOG-ARCH: custody must remain projection/request only",
    )

    collection_by_field = keyed(
        load_tsv("collection-entry-schema.tsv"),
        "field_id",
        "collection-entry-schema.tsv",
    )
    require("custody_state" not in collection_by_field, "collection entry: legacy custody_state is forbidden")
    require("physical_location" not in collection_by_field, "collection entry: physical_location must not become a second truth")
    custody_projection = collection_by_field.get("custody_projection", {})
    require(custody_projection.get("owner") == "SYS-BODY", "custody_projection: owner must be SYS-BODY")
    require_contains(
        custody_projection.get("type_or_values", ""),
        {"ST_EQUIPMENT", "record_version", "lawful_owner", "current_holder", "physical_location", "loan_terms", "transfer_receipt_id", "slot", "installed_state"},
        "custody_projection: versioned ST_EQUIPMENT reference missing",
    )
    location_projection = collection_by_field.get("physical_location_projection", {})
    require(location_projection.get("owner") == "SYS-BODY", "physical_location_projection: owner must be SYS-BODY")
    require_contains(
        location_projection.get("type_or_values", ""),
        {"ST_EQUIPMENT", "record_version", "physical_location"},
        "physical_location_projection: versioned ST_EQUIPMENT projection missing",
    )

    runstate_equipment = keyed(
        load_tsv("runstate-v2-field-schema.tsv"),
        "record_type",
        "runstate-v2-field-schema.tsv",
    ).get("DOMAIN_ST_EQUIPMENT_V2", {})
    typed_fields = {item.split(":", 1)[0] for item in tokens(runstate_equipment.get("required_fields_typed", ""))}
    require(
        physical_truth_fields.issubset(typed_fields) and "owner" not in typed_fields,
        "DOMAIN_ST_EQUIPMENT_V2: explicit physical truth wire is incomplete",
    )
    runstate_membership = keyed(
        load_tsv("runstate-v2-field-schema.tsv"),
        "record_type",
        "runstate-v2-field-schema.tsv",
    ).get("DOMAIN_ST_MEMBERSHIP_V2", {})
    membership_typed = {
        item.split(":", 1)[0]
        for item in tokens(runstate_membership.get("required_fields_typed", ""))
    }
    require(
        "custody" not in membership_typed
        and "membership_responsibility_ref" in membership_typed,
        "DOMAIN_ST_MEMBERSHIP_V2: legacy custody field must not persist",
    )
    transfer = keyed(
        load_tsv("state-transaction-v2-op-schema.tsv"),
        "op_kind",
        "state-transaction-v2-op-schema.tsv",
    ).get("OP_TRANSFER_UNIQUE", {})
    require(
        {"lawful_owner", "from_current_holder", "to_current_holder", "from_physical_location", "to_physical_location", "loan_terms", "transfer_receipt_id", "from_slot", "to_slot", "installed_state"}.issubset(
            tokens(transfer.get("required_payload_keys", ""))
        ),
        "OP_TRANSFER_UNIQUE: atomic physical-truth transfer payload incomplete",
    )


def run_fault_injection_self_test() -> tuple[int, int]:
    """Prove the checker predicates reject semantic field loss in memory."""

    state_by_id = keyed(
        load_tsv("system-state-contracts.tsv"), "state_id", "system-state-contracts.tsv"
    )
    equipment = state_by_id["ST_EQUIPMENT"]
    operation = state_by_id["ST_OPERATION"]
    hub = state_by_id["ST_HUB_ACTION"]
    hub_actions = keyed(
        load_tsv("hub-action-contracts.tsv"),
        "hub_action_id",
        "hub-action-contracts.tsv",
    )
    owner_by_id = keyed(
        load_tsv("settlement-owner-prepare-commit-contracts.tsv"),
        "owner_group_id",
        "settlement-owner-prepare-commit-contracts.tsv",
    )
    systems_by_id = keyed(
        load_tsv("system-node-contracts.tsv"),
        "system_id",
        "system-node-contracts.tsv",
    )
    episode_modes_by_id = keyed(
        load_tsv("episode-mode-token-contracts.tsv"),
        "rule_id",
        "episode-mode-token-contracts.tsv",
    )
    economy_by_id = keyed(
        load_tsv("economy-flows.tsv"),
        "resource_id",
        "economy-flows.tsv",
    )
    traces_by_id = keyed(
        load_tsv("core-loop-paper-walkthrough-traces.tsv"),
        "trace_step_id",
        "core-loop-paper-walkthrough-traces.tsv",
    )
    bindings_by_id = keyed(
        load_tsv("core-loop-payload-bindings.tsv"),
        "binding_id",
        "core-loop-payload-bindings.tsv",
    )
    settlements_by_level = keyed(
        load_tsv("settlement-contracts.tsv"),
        "settlement_level",
        "settlement-contracts.tsv",
    )
    physical_fields = {
        "lawful_owner",
        "current_holder",
        "physical_location",
        "loan_terms",
        "transfer_receipt_id",
        "slot",
        "installed_state",
    }
    lifecycle_fields = {
        "commitment_id",
        "commitment_state",
        "mission_card_ref",
        "selected_route_ref",
        "locked_sortie_manifest_ref",
        "arrival_tick",
        "unselected_policy_ref",
    }
    slot_fields = {
        "slot_commit_id",
        "time_slot_id",
        "card_ids",
        "card_bindings",
        "presentation_classes",
        "group_preflight",
        "card_performed_outcomes",
        "slot_receipt_id",
    }
    cases: list[tuple[str, bool]] = []
    mutant_settlement = copy.deepcopy(settlements_by_level["OPERATION"])
    mutant_settlement["allowed_player_choices"] = mutant_settlement[
        "allowed_player_choices"
    ].replace("事实只读", "玩家确认事实")
    cases.append(
        (
            "Operation settlement restored player fact approval",
            settlement_keeps_facts_readonly(mutant_settlement),
        )
    )
    for field in sorted(physical_fields):
        mutant = copy.deepcopy(equipment)
        mutant["minimum_fields"] = ";".join(
            item for item in tokens(mutant["minimum_fields"]) if item != field
        )
        cases.append(
            (f"equipment field removed: {field}", physical_fields.issubset(tokens(mutant["minimum_fields"])))
        )
    for field in sorted(lifecycle_fields):
        mutant = copy.deepcopy(operation)
        mutant["minimum_fields"] = ";".join(
            item for item in tokens(mutant["minimum_fields"]) if item != field
        )
        cases.append(
            (f"mission lifecycle field removed: {field}", lifecycle_fields.issubset(tokens(mutant["minimum_fields"])))
        )
    for field in sorted(slot_fields):
        mutant = copy.deepcopy(hub)
        mutant["minimum_fields"] = ";".join(
            item for item in tokens(mutant["minimum_fields"]) if item != field
        )
        cases.append(
            (f"hub slot field removed: {field}", slot_fields.issubset(tokens(mutant["minimum_fields"])))
        )
    cases.extend(
        [
            (
                "ambiguous equipment owner restored",
                "owner" not in tokens(equipment["minimum_fields"] + ";owner"),
            ),
            (
                "mission lifecycle order removed",
                "offered→committed→traveling→arrived→resolved"
                in operation["mutation_rule"].replace(
                    "offered→committed→traveling→arrived→resolved", ""
                ),
            ),
            (
                "hub fixed three-slot rule removed",
                "固定3个time_slot"
                in hub["mutation_rule"].replace("固定3个time_slot", ""),
            ),
        ]
    )

    mutant_prepare = copy.deepcopy(hub_actions["HUB_PREPARE"])
    mutant_prepare["slot_cost"] = "1"
    cases.append(
        (
            "Hub preparation preview charged one slot",
            hub_prepare_is_free_preview(mutant_prepare),
        )
    )

    mutant_curate = copy.deepcopy(hub_actions["HUB_CURATE"])
    mutant_curate["player_verbs"] = mutant_curate["player_verbs"].replace(
        "request_transfer", "return"
    )
    mutant_curate["result_domains"] = mutant_curate["result_domains"].replace(
        "physical_transfer_request_only", "ST_EQUIPMENT"
    )
    cases.append(
        (
            "Hub curation restored direct physical custody write",
            hub_curate_requests_physical_transfer_only(mutant_curate),
        )
    )

    mutant_presentations = copy.deepcopy(hub_actions)
    mutant_presentations["HUB_PREPARE"]["presentation_class"] = ""
    cases.append(
        (
            "Hub presentation class removed",
            hub_presentations_complete(mutant_presentations),
        )
    )

    mutant_hub_owner = copy.deepcopy(owner_by_id["SOG-HUB"])
    mutant_hub_owner["owner_validation"] = mutant_hub_owner[
        "owner_validation"
    ].replace("playable_activity", "activity")
    cases.append(
        (
            "SOG-HUB three-class presentation rule removed",
            sog_hub_has_three_presentation_classes(mutant_hub_owner),
        )
    )

    mutant_hub_system = copy.deepcopy(systems_by_id["SYS-HUB"])
    mutant_hub_system["exit_condition"] = mutant_hub_system[
        "exit_condition"
    ].replace("最多3张工作卡", "2至5个行动")
    cases.append(
        (
            "SYS-HUB work-card cap reverted to 2-5 actions",
            system_hub_has_public_budget(mutant_hub_system),
        )
    )

    mutant_emt008 = copy.deepcopy(episode_modes_by_id["EMT008"])
    mutant_emt008["action_budget_rule"] = "2_to_5_high_value_actions"
    cases.append(
        (
            "EMT008 issue groups restored as paid actions",
            emt008_has_public_budget(mutant_emt008),
        )
    )

    mutant_hub_slots = copy.deepcopy(economy_by_id["RES_HUB_SLOTS"])
    mutant_hub_slots["sources"] = mutant_hub_slots["sources"].replace(
        "标准周期固定3格", "标准周期动态5格"
    )
    cases.append(
        (
            "RES_HUB_SLOTS fixed three-slot rule removed",
            res_hub_slots_has_public_budget(mutant_hub_slots),
        )
    )

    mutant_pw_d01 = copy.deepcopy(traces_by_id["PW-D01"])
    mutant_pw_d01["receipt_or_output"] = (
        "hub_cycle_id;3_available_actions;visible_changes"
    )
    cases.append(
        (
            "PW-D01 collapsed issues slots and card cap into actions",
            pw_d01_has_separate_issue_slot_card_fields(mutant_pw_d01),
        )
    )

    mutant_pw_d08 = copy.deepcopy(traces_by_id["PW-D08"])
    mutant_pw_d08["required_inputs"] = mutant_pw_d08[
        "required_inputs"
    ].replace("assignment_preview", "assignment_changes")
    cases.append(
        (
            "PW-D08 mission preview became a state-changing paid card",
            pw_d08_keeps_prepare_preview_free(mutant_pw_d08),
        )
    )

    mutant_bindings = copy.deepcopy(bindings_by_id)
    mutant_bindings["PLB-D08"]["required_input_sources"] = mutant_bindings[
        "PLB-D08"
    ]["required_input_sources"].replace("assignment_preview", "assignment_changes")
    cases.append(
        (
            "PLB-D08 mission preview binding became assignment changes",
            neutral_hub_payload_bindings_preserve_free_preview(mutant_bindings),
        )
    )
    escaped = [name for name, still_valid in cases if still_valid]
    for name in escaped:
        print(f"[public-system-contracts:self-test] FAIL mutation escaped: {name}")
    return len(cases) - len(escaped), len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run in-memory semantic field-loss fault injections after baseline validation",
    )
    args = parser.parse_args()
    check_settlement_owner_choices()
    check_hub_action_and_resolution()
    check_repair_capacity()
    check_hub_public_budget_and_neutral_trace()
    check_dual_time_scale()
    check_mission_commitment_and_sortie()
    check_equipment_custody()
    if ERRORS:
        print(f"FAIL public system contract semantics: {len(ERRORS)} error(s)")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    if args.self_test:
        rejected, total = run_fault_injection_self_test()
        if rejected != total:
            print(
                f"FAIL public system contract fault injection: rejected={rejected}/{total}"
            )
            return 1
        print(
            f"PASS public system contract fault injection: rejected={rejected}/{total} mutations"
        )
    print(
        "PASS public system contract semantics: settlement Owner receipts, per-slot Hub "
        "actions, issue/slot/card budgets, presentation classes, free preparation previews, "
        "repair-equipment capacity, dual clocks, Mission Commitment, unique custody, and "
        "six-class sortie manifest are statically closed"
    )
    print("BOUNDARY zero_build / human_evidence_not_run / user_acceptance_pending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
