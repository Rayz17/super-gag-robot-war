#!/usr/bin/env python3
"""Validate D10 prototype dependencies and automated-case bidirectionality."""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict, deque
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PACKAGE_DIR / "data"
PROTOTYPE_PATH = DATA_DIR / "prototype-test-registry.tsv"
CASE_PATH = DATA_DIR / "playtest-cases.tsv"
METRIC_PATH = DATA_DIR / "playtest-metric-contracts.tsv"
EVIDENCE_PATH = DATA_DIR / "acceptance-evidence-registry.tsv"
TIME_SYSTEM_PATH = DATA_DIR / "time-system-ab-test.tsv"
NEUTRALITY_PATH = DATA_DIR / "time-system-neutrality-contract.tsv"
TEMPO_EQUIVALENCE_PATH = DATA_DIR / "tactical-tempo-equivalence.tsv"
CLOCK_ADAPTER_PATH = DATA_DIR / "scheduler-clock-adapter-contracts.tsv"
CLOCK_VECTOR_PATH = DATA_DIR / "d04-p1-adapter-event-vectors.tsv"
GATE_PATH = DATA_DIR / "game-design-gate-registry.tsv"
DECISION_PATH = DATA_DIR / "user-game-design-decisions.tsv"
DELIVERABLE_PATH = PACKAGE_DIR / "01-deliverable-registry.tsv"

DEPENDENCY_PATTERN = re.compile(
    r"^(?:prototype:[A-Za-z0-9_-]+@M[0-6]"
    r"|gate:[A-Za-z0-9_-]+(?:@scope=[A-Za-z0-9_-]+)?"
    r"|deliverable:[A-Za-z0-9_-]+"
    r"|decision:[A-Za-z0-9_-]+@(?:approved_for_candidate_test|approved_for_bounded_migration)"
    r"|evidence:[A-Za-z0-9_-]+)$"
)


def split_refs(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def read_tsv(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError(f"empty TSV: {path}")
    expected_width = len(lines[0].split("\t"))
    bad_widths = [
        f"line {line_number} has {len(line.split(chr(9)))} fields"
        for line_number, line in enumerate(lines, start=1)
        if len(line.split("\t")) != expected_width
    ]
    if bad_widths:
        raise ValueError(f"{path}: " + "; ".join(bad_widths))
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require_unique(rows: list[dict[str, str]], field: str, label: str) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        value = row[field]
        if not value:
            raise ValueError(f"{label} has an empty {field}")
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise ValueError(f"duplicate {label} IDs: {sorted(duplicates)}")
    return seen


def parse_weight_contract(value: str, label: str) -> dict[str, float]:
    weights: dict[str, float] = {}
    for token in split_refs(value):
        if "=" not in token:
            raise ValueError(f"{label} has an invalid weight token: {token}")
        metric_id, raw_weight = token.split("=", 1)
        if metric_id in weights:
            raise ValueError(f"{label} has duplicate metric weight: {metric_id}")
        try:
            weights[metric_id] = float(raw_weight)
        except ValueError as error:
            raise ValueError(f"{label} has a non-numeric weight: {token}") from error
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError(f"{label} weights must sum to 1.0, found {sum(weights.values())}")
    return weights


def check_time_system_neutrality(
    prototypes: list[dict[str, str]],
    cases: list[dict[str, str]],
    evidence_rows: list[dict[str, str]],
) -> None:
    time_rows = read_tsv(TIME_SYSTEM_PATH)
    neutrality_rows = read_tsv(NEUTRALITY_PATH)
    tempo_rows = read_tsv(TEMPO_EQUIVALENCE_PATH)
    time_by_variant = {row["variant_id"]: row for row in time_rows}
    neutrality_by_id = {row["contract_id"]: row for row in neutrality_rows}
    prototype_by_id = {row["prototype_id"]: row for row in prototypes}
    case_by_id = {row["case_id"]: row for row in cases}
    evidence_by_id = {row["evidence_id"]: row for row in evidence_rows}

    expected_variants = {"P1_A", "P1_B", "P1_C", "P1_D"}
    if set(time_by_variant) != expected_variants:
        raise ValueError(
            f"time-system comparison must contain formal A/B/C/D variants, found {sorted(time_by_variant)}"
        )
    if len(tempo_rows) != 21:
        raise ValueError(f"tempo equivalence must cover 21 tactical actions, found {len(tempo_rows)}")
    require_unique(tempo_rows, "action_id", "tempo-equivalence action")
    for row in tempo_rows:
        if row.get("p1_d_tempo_cost_rule") != row["p1_a_tempo_cost_rule"]:
            raise ValueError(
                f"{row['action_id']} P1-D formal control must use the same action-cost truth as P1-A"
            )
        if row["status"] != "candidate_tempo_mapping_v2":
            raise ValueError(f"{row['action_id']} tempo equivalence status must remain Candidate v2")
    expected_contracts = {
        "TSN-P1-SHARED",
        "TSN-P1-A",
        "TSN-P1-B",
        "TSN-P1-C",
        "TSN-P1-D",
        "TSN-P1-RESULT",
        "TSN-P2-CROSSOVER",
        "TSN-DEC03-FINAL",
    }
    if set(neutrality_by_id) != expected_contracts:
        raise ValueError(
            "time-system neutrality contract row set differs: "
            f"{sorted(set(neutrality_by_id) ^ expected_contracts)}"
        )

    p1_ids = {"D04-P1-A", "D04-P1-B", "D04-P1-C", "D04-P1-D"}
    required_prototypes = p1_ids | {"D04-P1-SHORTLIST", "D04-P2-CROSSOVER", "D04-P2"}
    missing_prototypes = sorted(required_prototypes - set(prototype_by_id))
    if missing_prototypes:
        raise ValueError(f"neutrality flow lacks prototypes: {missing_prototypes}")
    if "D04-P1-DECISION" in prototype_by_id:
        raise ValueError("legacy D04-P1-DECISION must not coexist with P1 shortlist/crossover flow")
    for prototype_id in required_prototypes:
        if prototype_by_id[prototype_id]["status"] != "pending":
            raise ValueError(f"new time-system prototype must remain pending: {prototype_id}")

    shared = neutrality_by_id["TSN-P1-SHARED"]
    required_shared_values = {
        "shared_world_initial_state": "validation/d04-p1-neutral-rules-paper-fixture-v0.1.md#3-5_same_snapshot_and_entity_ids",
        "shared_action_outcomes": "data/tactical-action-contracts.tsv+data/tactical-resolution-kernel.tsv_same_resolved_duration_force_effect_and_post_state",
        "shared_objectives": "OBJ_EVACUATE+OBJ_PROTECT+DENY_EXTRACTION_same_primary_secondary_deadline_and_outcome_rules",
        "shared_ai_doctrine": "validation/d04-p1-neutral-rules-paper-fixture-v0.1.md#4.5_same_observation_snapshot_intent_contingency_and_tiebreak",
        "shared_unknown_information_budget": "C2_off;known_physics_exact;enemy_target_route_action_class_time_band_equal;hidden_rng=0;report_age=0;confidence_budget=identical",
        "tutorial_budget": "max_8m;max_12_guided_inputs;max_2_context_hints;no_strategy_hint;native_terms_allowed",
        "implementation_order": "R0_SHARED_KERNEL_FREEZE>P1_D>P1_A>P1_C>P1_B",
        "build_status": "zero_build",
        "human_evidence_status": "not_run",
        "user_decision_status": "presented_no_decision",
    }
    for field, expected in required_shared_values.items():
        if shared[field] != expected:
            raise ValueError(f"TSN-P1-SHARED {field} drift: {shared[field]!r}")
    p1_allowed = {
        "shortlist_two",
        "shortlist_three",
        "shortlist_four",
        "no_winner",
        "revise_top_two",
        "retire_all",
    }
    if set(split_refs(shared["allowed_outcomes"])) != p1_allowed:
        raise ValueError("P1 outcome enum must be shortlist/no_winner/revise_top_two/retire_all only")
    if "select" not in split_refs(shared["prohibited_outcomes"]):
        raise ValueError("P1 must explicitly prohibit select")
    parse_weight_contract(shared["preregistered_metric_weights"], "P1")

    expected_variant_contracts = {
        "P1_A": ("TSN-P1-A", "D04-P1-A", "2", "TS-EMBER"),
        "P1_B": ("TSN-P1-B", "D04-P1-B", "4", "TS-QUARTZ"),
        "P1_C": ("TSN-P1-C", "D04-P1-C", "3", "TS-LANTERN"),
        "P1_D": ("TSN-P1-D", "D04-P1-D", "1", "TS-HARBOR"),
    }
    labels: set[str] = set()
    command_policies: set[str] = set()
    ui_policies: set[str] = set()
    for variant_id, (contract_id, prototype_id, order, label) in expected_variant_contracts.items():
        row = neutrality_by_id[contract_id]
        if row["variant_id"] != variant_id or row["prototype_id"] != prototype_id:
            raise ValueError(f"{contract_id} variant/prototype binding drift")
        if row["implementation_order"] != order or row["anonymous_build_label"] != label:
            raise ValueError(f"{contract_id} implementation order or anonymous label drift")
        for field in (
            "shared_world_initial_state",
            "shared_action_outcomes",
            "shared_objectives",
            "shared_ai_doctrine",
            "shared_unknown_information_budget",
            "tutorial_budget",
            "preregistered_metric_weights",
            "preregistered_hard_thresholds",
            "allowed_outcomes",
            "prohibited_outcomes",
        ):
            if row[field] != "SAME_AS_TSN-P1-SHARED":
                raise ValueError(f"{contract_id} may not override shared neutrality field {field}")
        if row["build_status"] != "zero_build" or row["human_evidence_status"] != "not_run":
            raise ValueError(f"{contract_id} falsely implies Build or human evidence")
        if "native" not in row["native_command_syntax_policy"] or "allowed" not in row["native_ui_policy"]:
            raise ValueError(f"{contract_id} does not preserve scheduler-native command/UI policy")
        labels.add(label)
        command_policies.add(row["native_command_syntax_policy"])
        ui_policies.add(row["native_ui_policy"])
        if time_by_variant[variant_id]["status"] != "candidate_time_test_v3_zero_build_human_not_run":
            raise ValueError(f"{variant_id} time-system row overstates evidence")
        if "shortlist" not in time_by_variant[variant_id]["p1_result_rule"]:
            raise ValueError(f"{variant_id} does not limit P1 to shortlist/elimination")
    if "traditional_faction_turn" not in neutrality_by_id["TSN-P1-D"]["native_command_syntax_policy"]:
        raise ValueError("P1-D must remain the formal traditional faction-turn control")
    if len(labels) != 4 or len(command_policies) != 4 or len(ui_policies) != 4:
        raise ValueError("four Scheduler variants need unique anonymous labels and native command/UI policies")

    shortlist = neutrality_by_id["TSN-P1-RESULT"]
    if set(split_refs(shortlist["allowed_outcomes"])) != p1_allowed:
        raise ValueError("P1 shortlist result row has the wrong outcome enum")
    if "select" not in split_refs(shortlist["prohibited_outcomes"]):
        raise ValueError("P1 shortlist result row must prohibit select")
    expected_shortlist_carrier_rule = (
        "only_shortlist_two_or_three_or_four_may_enter_crossover;"
        "no_winner_or_revise_top_two_or_retire_all_unlock_nothing;"
        "shortlist_never_unlocks_chapter_or_full_P2"
    )
    if shortlist["reversible_carrier_rule"] != expected_shortlist_carrier_rule:
        raise ValueError("P1 shortlist entry/stop/unlock rule drift")

    crossover = neutrality_by_id["TSN-P2-CROSSOVER"]
    expected_crossover_outcomes = {"advance_to_DEC03_M", "revise_carriers", "no_selection", "retire_all"}
    if set(split_refs(crossover["allowed_outcomes"])) != expected_crossover_outcomes:
        raise ValueError("P2 crossover outcome enum drift")
    parse_weight_contract(crossover["preregistered_metric_weights"], "P2 crossover")
    expected_crossover_values = {
        "shared_action_outcomes": (
            "C2_RELAY_CONTACT+JICUN_ROUTE+BAIYUAN_PREVIEW+QIHAI_VERIFY_AUTH+"
            "LUHENG_VERIFY+SOUL_RESPONSE_same_semantics_costs_counters_and_post_states"
        ),
        "reversible_carrier_rule": (
            "all_C2_patches_session_local_and_resettable;"
            "each_carrier_can_be_retired_without_ruleset_migration;"
            "shared_truth_or_six_C2_semantic_drift_invalidates_all_carriers;"
            "native_adapter_or_UI_drift_invalidates_affected_carrier;"
            "revise_carriers_requires_rerun;no_selection_or_retire_all_unlocks_nothing"
        ),
        "implementation_order": (
            "only_after_TSN-P1-RESULT=shortlist_two_or_three_or_four;"
            "without_DEC03_M;carrier_order_balanced_latin_square"
        ),
        "prohibited_outcomes": "select_inside_prototype;chapter_binding;full_25_action_validation",
    }
    for field, expected in expected_crossover_values.items():
        if crossover[field] != expected:
            raise ValueError(f"P2 crossover {field} drift: {crossover[field]!r}")
    if (
        crossover["build_status"] != "zero_build"
        or crossover["human_evidence_status"] != "not_run"
        or crossover["user_decision_status"] != "presented_no_decision"
    ):
        raise ValueError("P2 crossover falsely implies Build or human evidence")

    final = neutrality_by_id["TSN-DEC03-FINAL"]
    if set(split_refs(final["allowed_outcomes"])) != {"select", "revise", "no_selection", "retire_all"}:
        raise ValueError("DEC-03-M final result enum must be select/revise/no_selection/retire_all")
    if "automatic_winner" not in split_refs(final["prohibited_outcomes"]):
        raise ValueError("DEC-03-M must prohibit an automatic winner")
    if (
        final["build_status"] != "zero_build"
        or final["human_evidence_status"] != "not_run"
        or final["user_decision_status"] != "presented_no_decision"
    ):
        raise ValueError("DEC-03-M policy falsely implies Build, human evidence, or user selection")

    expected_dependencies = {
        "D04-P1-SHORTLIST": {
            "prototype:D04-P1-A@M5",
            "prototype:D04-P1-B@M5",
            "prototype:D04-P1-C@M5",
            "prototype:D04-P1-D@M5",
        },
        "D04-P2-CROSSOVER": {
            "prototype:D04-P1-SHORTLIST@M5",
            "gate:GATE-GD1",
            "decision:DEC-03@approved_for_candidate_test",
            "decision:DEC-04@approved_for_candidate_test",
        },
        "D04-P2": {
            "prototype:D04-P2-CROSSOVER@M5",
            "gate:GATE-GD1",
            "decision:DEC-03@approved_for_bounded_migration",
            "decision:DEC-04@approved_for_candidate_test",
        },
    }
    for prototype_id, expected in expected_dependencies.items():
        found = set(split_refs(prototype_by_id[prototype_id]["dependency_refs"]))
        if found != expected:
            raise ValueError(f"{prototype_id} dependency contract drift: {sorted(found ^ expected)}")

    required_cases = {"HUM-P1-D-COLD", "HUM-P1-SHORTLIST", "AUTO-P2-CARRIER-EQUIVALENCE", "HUM-P2-CROSSOVER"}
    if not required_cases <= set(case_by_id):
        raise ValueError(f"time-system cases missing: {sorted(required_cases - set(case_by_id))}")
    required_evidence = {"EV-P1-D-COLD", "EV-P1-SHORTLIST", "EV-P2-CROSSOVER"}
    if not required_evidence <= set(evidence_by_id):
        raise ValueError(f"time-system evidence rows missing: {sorted(required_evidence - set(evidence_by_id))}")
    for evidence_id in required_evidence:
        row = evidence_by_id[evidence_id]
        if row["participant_count"] != "0" or row["human_result"] != "not_run" or row["status"] != "pending":
            raise ValueError(f"{evidence_id} falsely implies human evidence")


def check_scheduler_clock_adapters() -> tuple[int, int]:
    """Require every Scheduler to map the same eight-second world-cycle events."""

    adapters = read_tsv(CLOCK_ADAPTER_PATH)
    vectors = read_tsv(CLOCK_VECTOR_PATH)
    adapter_ids = require_unique(adapters, "adapter_id", "scheduler clock adapter")
    vector_ids = require_unique(vectors, "case_id", "scheduler clock vector")
    expected_adapters = {
        "SCA-P1-A": ("P1_A", "D04-P1-A"),
        "SCA-P1-B": ("P1_B", "D04-P1-B"),
        "SCA-P1-C": ("P1_C", "D04-P1-C"),
        "SCA-P1-D": ("P1_D", "D04-P1-D"),
    }
    if adapter_ids != set(expected_adapters):
        raise ValueError(
            "scheduler clock adapter set differs: "
            f"{sorted(adapter_ids ^ set(expected_adapters))}"
        )

    required_clock_fields = {
        "window_open_snapshot",
        "commit_boundary",
        "eligible_set_freeze",
        "unit_action_time_mapping",
        "world_clock_advance",
        "autonomous_actor_tick",
        "environment_tick",
        "deadline_tick",
        "observation_snapshot_at",
        "enemy_intent_freeze_at",
        "reaction_open_expire",
        "resource_reset_at",
        "save_boundary",
        "declared_non_equivalence",
        "neutrality_assertions",
    }
    for row in adapters:
        variant_id, prototype_id = expected_adapters[row["adapter_id"]]
        if row["variant_id"] != variant_id or row["prototype_id"] != prototype_id:
            raise ValueError(f"{row['adapter_id']} variant/prototype binding drift")
        if row["semantic_window_duration_s"] != "8.0":
            raise ValueError(f"{row['adapter_id']} must use one 8.0s semantic world cycle")
        missing = sorted(field for field in required_clock_fields if not row[field])
        if missing:
            raise ValueError(f"{row['adapter_id']} has empty clock fields: {missing}")
        if "exactly_plus_8s_once" not in row["world_clock_advance"] and "plus_8s_once" not in row["world_clock_advance"]:
            raise ValueError(f"{row['adapter_id']} does not advance world time exactly once")
        for token in ("t2_t4_t6_t8", "exactly_once"):
            if token not in row["autonomous_actor_tick"]:
                raise ValueError(f"{row['adapter_id']} autonomous tick lacks {token}")
        if "once_at_cycle_close" not in row["environment_tick"]:
            raise ValueError(f"{row['adapter_id']} environment tick is not cycle-close once")
        if "32s_deadline" not in row["deadline_tick"] or "cycle_4_close" not in row["deadline_tick"]:
            raise ValueError(f"{row['adapter_id']} deadline mapping is not fixed at 32s")
        if "immutable_until_cycle_close" not in row["enemy_intent_freeze_at"]:
            raise ValueError(f"{row['adapter_id']} permits mid-cycle enemy intent replanning")
        if "expires_at_cycle_close" not in row["reaction_open_expire"]:
            raise ValueError(f"{row['adapter_id']} reaction lifetime is not one cycle")
        for token in (
            "clock_after_4_cycles=32s",
            "autonomous_microticks=16",
            "bridge_base_tick_max_1_per_cycle",
            "intent_snapshot_age_equal",
            "all_wait_world_event_hash_equal",
        ):
            if token not in row["neutrality_assertions"]:
                raise ValueError(f"{row['adapter_id']} lacks neutrality assertion {token}")
        if (
            row["build_status"] != "zero_build"
            or row["human_evidence_status"] != "not_run"
            or row["user_decision_status"] != "presented_no_decision"
            or row["status"] != "candidate_scheduler_clock_adapter_v1"
        ):
            raise ValueError(f"{row['adapter_id']} overstates clock-adapter evidence")

    expected_classes = {
        "world_clock_and_autonomous_tick",
        "environment_once_per_cycle",
        "environment_named_markers",
        "observation_and_intent_age",
        "reaction_and_resource_reset",
        "deadline_exactly_once",
        "midcycle_restore_determinism",
    }
    if len(vectors) != 28 or len(vector_ids) != 28:
        raise ValueError(f"scheduler clock vectors must be 4x7=28, found {len(vectors)}")
    vectors_by_adapter: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in vectors:
        if row["adapter_id"] not in adapter_ids:
            raise ValueError(f"{row['case_id']} references unknown clock adapter")
        vectors_by_adapter[row["adapter_id"]].append(row)
        if row["assertion_class"] not in expected_classes:
            raise ValueError(f"{row['case_id']} has unknown assertion class")
        if not row["mirror_case_id"].startswith("SELF_MIRROR_"):
            raise ValueError(f"{row['case_id']} lacks explicit mirror invariant")
        if row["status"] != "candidate_clock_event_vector_v1":
            raise ValueError(f"{row['case_id']} overstates vector evidence")
        if row["assertion_class"] == "deadline_exactly_once":
            if row["event_time_s"] != "32.0" or "deadline_eval_count:0>1" not in row["expected_delta"]:
                raise ValueError(f"{row['case_id']} does not evaluate the deadline once at 32s")
        elif row["event_time_s"] != "8.0":
            raise ValueError(f"{row['case_id']} must close its first semantic cycle at 8s")

    canonical_vectors: dict[str, tuple[str, ...]] = {}
    for adapter_id, rows in vectors_by_adapter.items():
        classes = {row["assertion_class"] for row in rows}
        if classes != expected_classes or len(rows) != 7:
            raise ValueError(f"{adapter_id} does not cover all seven clock-vector classes")
        for row in rows:
            signature = (
                row["pre_state_ref"],
                row["normalized_plan_ref"],
                row["event_time_s"],
                row["batch_id"],
                row["expected_delta"],
                row["post_state_ref"],
                row["objective_delta"],
            )
            previous = canonical_vectors.setdefault(row["assertion_class"], signature)
            if signature != previous:
                raise ValueError(
                    f"{row['assertion_class']} expected world vector differs for {adapter_id}"
                )
    return len(adapters), len(vectors)


def main() -> int:
    prototypes = read_tsv(PROTOTYPE_PATH)
    cases = read_tsv(CASE_PATH)
    metrics = read_tsv(METRIC_PATH)
    evidence_rows = read_tsv(EVIDENCE_PATH)
    gate_rows = read_tsv(GATE_PATH)
    decision_rows = read_tsv(DECISION_PATH)
    deliverable_rows = read_tsv(DELIVERABLE_PATH)
    check_time_system_neutrality(prototypes, cases, evidence_rows)
    clock_adapter_count, clock_vector_count = check_scheduler_clock_adapters()
    prototype_ids = require_unique(prototypes, "prototype_id", "prototype")
    case_ids = require_unique(cases, "case_id", "case")
    metric_ids = require_unique(metrics, "metric_id", "metric")
    evidence_ids = require_unique(evidence_rows, "evidence_id", "evidence")
    gate_ids = require_unique(gate_rows, "gate_id", "gate")
    decision_ids = require_unique(decision_rows, "decision_id", "decision")
    deliverable_ids = require_unique(deliverable_rows, "deliverable_id", "deliverable")

    try:
        order_by_prototype = {
            row["prototype_id"]: int(row["sequence_order"]) for row in prototypes
        }
    except ValueError as error:
        raise ValueError("prototype sequence_order values must be integers") from error
    sequence_orders = list(order_by_prototype.values())
    if len(sequence_orders) != len(set(sequence_orders)):
        raise ValueError("prototype sequence_order values must be unique")

    case_by_id = {row["case_id"]: row for row in cases}
    dependency_edges: set[tuple[str, str]] = set()
    for row in prototypes:
        prototype_id = row["prototype_id"]
        dependencies = split_refs(row["dependency_refs"])
        if len(dependencies) != len(set(dependencies)):
            raise ValueError(f"{prototype_id} has duplicate dependency refs")
        for dependency in dependencies:
            if not DEPENDENCY_PATTERN.fullmatch(dependency):
                raise ValueError(f"{prototype_id} has invalid dependency ref: {dependency}")
            if dependency.startswith("prototype:"):
                upstream = dependency.removeprefix("prototype:").split("@", 1)[0]
                if upstream not in prototype_ids:
                    raise ValueError(f"{prototype_id} references unknown prototype: {upstream}")
                if order_by_prototype[upstream] >= order_by_prototype[prototype_id]:
                    raise ValueError(
                        f"{prototype_id} depends on {upstream}, but its sequence_order is not later"
                    )
                dependency_edges.add((upstream, prototype_id))
            elif dependency.startswith("gate:"):
                gate_id = dependency.removeprefix("gate:").split("@", 1)[0]
                if gate_id not in gate_ids:
                    raise ValueError(f"{prototype_id} references unknown gate: {gate_id}")
            elif dependency.startswith("decision:"):
                decision_id = dependency.removeprefix("decision:").split("@", 1)[0]
                if decision_id not in decision_ids:
                    raise ValueError(f"{prototype_id} references unknown decision: {decision_id}")
            elif dependency.startswith("deliverable:"):
                deliverable_id = dependency.removeprefix("deliverable:")
                if deliverable_id not in deliverable_ids:
                    raise ValueError(f"{prototype_id} references unknown deliverable: {deliverable_id}")
            elif dependency.startswith("evidence:"):
                evidence_id = dependency.removeprefix("evidence:")
                if evidence_id not in evidence_ids:
                    raise ValueError(f"{prototype_id} references unknown evidence: {evidence_id}")

        human_metrics = split_refs(row["human_metric_ids"])
        if len(human_metrics) != len(set(human_metrics)):
            raise ValueError(f"{prototype_id} has duplicate human_metric_ids")
        unknown_metrics = sorted(set(human_metrics) - metric_ids)
        if unknown_metrics:
            raise ValueError(f"{prototype_id} references unknown metrics: {unknown_metrics}")

        machine_cases = split_refs(row["machine_case_ids"])
        if len(machine_cases) != len(set(machine_cases)):
            raise ValueError(f"{prototype_id} has duplicate machine_case_ids")
        for case_id in machine_cases:
            if case_id not in case_ids:
                raise ValueError(f"{prototype_id} references unknown case: {case_id}")
            if case_by_id[case_id]["test_kind"] != "automated":
                raise ValueError(f"{prototype_id} machine_case_ids includes non-automated case: {case_id}")

    indegree = {prototype_id: 0 for prototype_id in prototype_ids}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for upstream, downstream in dependency_edges:
        outgoing[upstream].append(downstream)
        indegree[downstream] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    visited: list[str] = []
    while queue:
        node = queue.popleft()
        visited.append(node)
        for downstream in sorted(outgoing[node]):
            indegree[downstream] -= 1
            if indegree[downstream] == 0:
                queue.append(downstream)
    if len(visited) != len(prototype_ids):
        cyclic_nodes = sorted(node for node, degree in indegree.items() if degree)
        raise ValueError(f"prototype dependency graph is cyclic: {cyclic_nodes}")

    registry_pairs = {
        (row["prototype_id"], case_id)
        for row in prototypes
        for case_id in split_refs(row["machine_case_ids"])
    }
    automated_case_pairs: set[tuple[str, str]] = set()
    human_case_pairs: set[tuple[str, str]] = set()
    for row in cases:
        applicable = split_refs(row["applicable_prototype_ids"])
        if len(applicable) != len(set(applicable)):
            raise ValueError(f"{row['case_id']} has duplicate applicable_prototype_ids")
        for prototype_id in applicable:
            if prototype_id not in prototype_ids:
                raise ValueError(f"{row['case_id']} references unknown prototype: {prototype_id}")
            if row["test_kind"] == "automated":
                automated_case_pairs.add((prototype_id, row["case_id"]))
            else:
                human_case_pairs.add((prototype_id, row["case_id"]))

    only_registry = sorted(registry_pairs - automated_case_pairs)
    only_cases = sorted(automated_case_pairs - registry_pairs)
    if only_registry or only_cases:
        raise ValueError(
            "automated prototype/case pairs are not bidirectional: "
            f"only_registry={only_registry}; only_cases={only_cases}"
        )

    prototypes_with_human_cases = {prototype_id for prototype_id, _ in human_case_pairs}
    missing_human_cases = sorted(
        row["prototype_id"]
        for row in prototypes
        if row["family"] != "instrumentation" and row["prototype_id"] not in prototypes_with_human_cases
    )
    if missing_human_cases:
        raise ValueError(
            "non-instrumentation prototypes have sample/M5 claims but no executable human case: "
            f"{missing_human_cases}"
        )

    evidence_case_ids: set[str] = set()
    for row in evidence_rows:
        for case_id in split_refs(row["case_ids"]):
            if case_id == "not_applicable":
                continue
            if case_id not in case_ids:
                raise ValueError(f"{row['evidence_id']} references unknown case: {case_id}")
            evidence_case_ids.add(case_id)
        try:
            participant_count = int(row["participant_count"])
        except ValueError as error:
            raise ValueError(f"{row['evidence_id']} participant_count must be an integer") from error
        if participant_count == 0 and row["human_result"] not in {"not_run", "not_applicable"}:
            raise ValueError(
                f"{row['evidence_id']} has participant_count=0 but human_result={row['human_result']}"
            )

    human_case_ids = {case_id for _, case_id in human_case_pairs}
    unledgered_human_cases = sorted(human_case_ids - evidence_case_ids)
    if unledgered_human_cases:
        raise ValueError(f"human/non-automated cases missing from evidence registry: {unledgered_human_cases}")

    print(
        "D10 registry PASS: "
        f"{len(prototype_ids)} prototypes, {len(dependency_edges)} dependency edges (DAG), "
        f"{len(case_ids)} cases, {len(registry_pairs)} bidirectional automated prototype/case pairs, "
        f"{len(human_case_ids)} human/non-automated cases ledgered; typed gate/decision/deliverable/evidence "
        "dependencies and metric refs resolve; A/B/C/D neutrality with 21 explicit A/D action-cost mappings, "
        f"{clock_adapter_count} scheduler clock adapters/{clock_vector_count} paper event vectors, "
        "P1 shortlist, reversible C2 crossover, and DEC-03-M result enums are locked"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"D10 registry FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
