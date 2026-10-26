#!/usr/bin/env python3
"""Fail-closed validation for the first four user decision sign-off records.

A PASS means the sheet is safe to present for a direction decision.  It never
means that a user decision receipt, budget pool, execution envelope, Build, or
human-run authorization already exists.
"""

from __future__ import annotations

import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
DATA = PACKAGE / "data"
SIGNOFF_TSV = DATA / "first-decision-signoff-pack.tsv"
FREEZE_TSV = DATA / "first-decision-signoff-freeze.tsv"
SIGNOFF_MD = PACKAGE / "12a-first-decision-signoff-sheet.md"

DECISIONS = ("DEC-01", "DEC-02", "DEC-03", "DEC-11")
TOKENS = {
    "DEC-01": "APPROVE_RECOMMENDED",
    "DEC-02": "APPROVE_RECOMMENDED",
    "DEC-03": "APPROVE_COMPARE_ABCD_ONLY",
    "DEC-11": "APPROVE_ISOLATED_GATE_TEST_ONLY",
}
SCOPES = {
    "DEC-01": "PRODUCT_IDENTITY_AND_EVALUATION_ONLY",
    "DEC-02": "P1_COMMON_PHYSICS_OBJECTIVE_FAILURE_ONLY",
    "DEC-03": "P1_NEUTRAL_ABCD_SHORTLIST_NO_WINNER",
    "DEC-11": "ISOLATED_R0_CHECKER_SYNTHETIC_FAULT_DRYRUN_ZERO_CURRENT_WRITER_OUTPUT",
}
CLAUSES = {
    "DEC-01": {
        "D01-C01_PRODUCT_IDENTITY",
        "D01-C02_TARGET_PLAYER_AND_EVALUATION",
        "D01-C03_EXCLUSIONS_NO_EXECUTION",
    },
    "DEC-02": {
        "D02-C01_KNOWN_PHYSICS_DETERMINISTIC",
        "D02-C02_INCOMPLETE_INFORMATION",
        "D02-C03_NON_ANNIHILATION_OBJECTIVES",
        "D02-C04_LOCAL_FORWARD_FAILURE_CANDIDATE_ONLY",
        "D02-C05_SHARED_P1_RULES_NO_SCHEDULER_OR_INSTRUMENT",
    },
    "DEC-03": {
        "D03-C01_COMPARE_P1_ABCD",
        "D03-C02_SHARED_NEUTRALITY_BOUNDARY",
        "D03-C03_NATIVE_GRAMMAR_UI_EQUIVALENT_ACCESS",
        "D03-C04_BLIND_PREREGISTER_ORDER_COST_THRESHOLDS",
        "D03-C05_P1_SHORTLIST_ONLY",
        "D03-C06_MINIMAL_C2_CROSSOVER_BEFORE_FINAL",
        "D03-C07_NO_WINNER_AND_NO_CROSSOVER_AUTH",
    },
    "DEC-11": {
        "D11-C01_ISOLATED_FROZEN_SYNTHETIC_COPY",
        "D11-C02_R0_CHECKER_FAULT_DRYRUN_ONLY",
        "D11-C03_ZERO_CURRENT_WRITER_OUTPUT",
        "D11-C04_NO_CURRENT_CHAIN_WRITE",
        "D11-C05_MIGRATION_M_M1_M2_M3_M4_SEPARATE",
    },
}
EVIDENCE = {
    "DEC-01": {
        "03-product-experience-charter.md",
        "04-full-game-system-graph.md",
        "validation/d02-d03-core-loop-paper-walkthrough-v0.1.md",
    },
    "DEC-02": {
        "05-srpg-c2-core-design.md",
        "validation/d04-p1-neutral-rules-paper-fixture-v0.1.md",
        "10-prototype-test-plan.md",
        "data/time-system-neutrality-contract.tsv",
        "data/prototype-execution-preflight-requirements.tsv",
    },
    "DEC-03": {
        "data/time-system-neutrality-contract.tsv",
        "data/time-system-ab-test.tsv",
        "data/prototype-test-registry.tsv",
        "data/prototype-execution-preflight-requirements.tsv",
    },
    "DEC-11": {
        "09-production-pipeline-and-gates.md",
        "data/game-design-gate-instance-schema.tsv",
        "data/invalidation-routing-rules.tsv",
        "data/prototype-execution-preflight-requirements.tsv",
        "scripts/check_candidate_authorization_contracts.py",
    },
}
DIRECTION_PRECONDITIONS = {
    "EXACT_DECISION_SPEC_PATH_AND_SHA256",
    "EXACT_RECORD_LOCATOR",
    "EXACT_OPTION_TOKEN",
    "ALL_RECOMMENDED_CLAUSE_IDS_ACCEPTED",
    "USER_MESSAGE_REF_AND_SHA256",
    "ISSUED_BY_USER_REF",
}
COMMON_NON_AUTH = {
    "NO_CANON",
    "NO_CURRENT_RUNTIME",
    "NO_FORMAL_ASSET",
    "NO_L6",
}
SPECIAL_NON_AUTH = {
    "DEC-01": {"NO_PROTOTYPE", "NO_GATE_INSTANCE", "NO_BUILD", "NO_HUMAN_SESSION", "NO_DEMO_PROMOTION"},
    "DEC-02": {"NO_ROLE_C2", "NO_SCHEDULER_SELECTION", "NO_TEST_INSTRUMENT", "NO_FORWARD_FAILURE_MIGRATION_WITHOUT_PSET1"},
    "DEC-03": {"NO_P1_WINNER", "NO_WEGO_PRESELECTION", "NO_D_PRESELECTION", "NO_C2_CROSSOVER_AUTH", "NO_DEC03_M_BEFORE_CROSSOVER"},
    "DEC-11": {"NO_AUTOMATIC_CHAIN_MIGRATION", "NO_CURRENT_REGISTRY_MIGRATION", "NO_CURRENT_WRITER_READABLE_OUTPUT", "NO_STORY_CHAIN_WRITE", "NO_DEMO_WRITE"},
}
COMMON_STOPS = {
    "AUTH_OR_RECEIPT_INVALID",
    "ENVELOPE_EXPIRED_REVOKED_OR_LIMIT_EXCEEDED",
    "P0_OR_PRIVACY",
    "FORBIDDEN_PATH_WRITE_ATTEMPT",
    "SOURCE_HASH_DRIFT",
    "OVERLAPPING_ENVELOPE_OR_SHARED_POOL_FAIL",
}
SPECIAL_STOPS = {
    "DEC-01": {"PRODUCT_IDENTITY_OR_TARGET_PLAYER_CHANGED"},
    "DEC-02": {"ROLE_C2_ENTERED_NEUTRAL_P1", "FORWARD_FAILURE_MIGRATION_WITHOUT_PSET1"},
    "DEC-03": {"ABCD_SHARED_SEMANTICS_DRIFT", "BLIND_OR_PREREGISTRATION_BROKEN", "P1_SINGLE_WINNER_ATTEMPT", "CROSSOVER_BYPASSED", "DEMO_ROUTE_IMPORTED"},
    "DEC-11": {"FAULT_INJECTION_UNEXPECTED_PASS", "CURRENT_CHAIN_WRITE_ATTEMPT", "CURRENT_WRITER_READABLE_OUTPUT_NONZERO"},
}
LATER_BINDINGS = {
    "DEC-01": ({"DRS-DEC01-M"}, {"DR-DEC01-M"}),
    "DEC-02": ({"DRS-DEC02-M"}, {"DR-DEC02-M"}),
    "DEC-03": ({"DRS-DEC03-M"}, {"DR-DEC03-M"}),
    "DEC-11": (
        {"DRS-DEC11-M", "DRS-DEC11-M1", "DRS-DEC11-M2", "DRS-DEC11-M3", "DRS-DEC11-M4"},
        {"DR-DEC11-M", "DR-DEC11-M1", "DR-DEC11-M2", "DR-DEC11-M3", "DR-DEC11-M4"},
    ),
}
EMPTY_INSTANCE_REGISTRIES = (
    "decision-receipt-instances.tsv",
    "candidate-test-execution-envelopes.tsv",
    "execution-envelope-authorization-receipts.tsv",
    "candidate-test-budget-pools.tsv",
    "prototype-execution-preflight-instances.tsv",
)


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError(f"empty TSV: {path.relative_to(PACKAGE)}")
    width = len(lines[0].split("\t"))
    for number, line in enumerate(lines, 1):
        if len(line.split("\t")) != width:
            raise ValueError(f"{path.relative_to(PACKAGE)}:{number} width drift")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def split(value: str) -> set[str]:
    return {item for item in value.split(";") if item and item != "none"}


def index(rows: list[dict[str, str]], key: str, errors: list[str], label: str) -> dict[str, dict[str, str]]:
    values = [row.get(key, "") for row in rows]
    duplicates = [value for value, count in Counter(values).items() if value and count > 1]
    if duplicates:
        errors.append(f"{label}: duplicate {key}: {duplicates}")
    if any(not value for value in values):
        errors.append(f"{label}: empty {key}")
    return {row[key]: row for row in rows if row.get(key)}


def main() -> int:
    errors: list[str] = []
    try:
        _, signoff_rows = read_tsv(SIGNOFF_TSV)
        _, freeze_rows = read_tsv(FREEZE_TSV)
        _, source_rows = read_tsv(DATA / "user-game-design-decisions.tsv")
        _, set_rows = read_tsv(DATA / "decision-receipt-sets.tsv")
        _, requirement_rows = read_tsv(DATA / "decision-receipt-requirements.tsv")
        _, receipt_schema_rows = read_tsv(DATA / "decision-receipt-instance-schema.tsv")
        _, envelope_schema_rows = read_tsv(DATA / "candidate-test-execution-envelope-schema.tsv")
        _, preflight_rows = read_tsv(DATA / "prototype-execution-preflight-requirements.tsv")
        _, neutrality_rows = read_tsv(DATA / "time-system-neutrality-contract.tsv")
    except (OSError, ValueError) as exc:
        print(f"First-decision sign-off validation: FAIL\n- {exc}")
        return 1

    signoffs = index(signoff_rows, "decision_id", errors, "sign-off")
    sources = index(source_rows, "decision_id", errors, "decision ledger")
    receipt_sets = index(set_rows, "receipt_set_id", errors, "receipt sets")
    requirements = index(requirement_rows, "requirement_id", errors, "receipt requirements")
    preflights = index(preflight_rows, "preflight_contract_id", errors, "preflight contracts")
    neutrality = index(neutrality_rows, "contract_id", errors, "neutrality contracts")

    if len(signoff_rows) != 4 or set(signoffs) != set(DECISIONS):
        errors.append(f"sign-off coverage must be exactly {list(DECISIONS)}")

    # The old four-way test sign-off pack is retained as a traceable technical
    # appendix, but a newer public design direction has superseded its ability
    # to collect a signature.  A one-row, content-addressed freeze record wins
    # over the historical `ready_for_signature` field without rewriting the
    # old packet as if it had always described the new direction.
    if freeze_rows:
        if len(freeze_rows) != 1:
            errors.append("sign-off freeze registry must contain exactly one active row")
            freeze = {}
        else:
            freeze = freeze_rows[0]
        expected_freeze = {
            "freeze_id": "FDSF-2026-08-11-01",
            "effective_status": "superseded_pending_public_direction_rebase",
            "effective_public_direction": "B_SHORT_TEAM_COORDINATION_PRIMARY_A_ALTERNATING_ACTIVATION_BACKUP",
            "applies_to_decision_ids": ";".join(DECISIONS),
            "source_pack_path": "data/first-decision-signoff-pack.tsv",
            "supersedes_signoff_readiness": "ready_for_signature",
            "allowed_use": "history_trace_only",
            "forbidden_use": "decision_receipt;execution_envelope;build;human_session;runtime_migration",
            "user_review_entry": "00c-core-game-design-master-review.md",
            "reason": "public_direction_changed_since_old_ABCD_equal_comparison_pack",
            "effective_at": "2026-08-11",
        }
        for field, expected in expected_freeze.items():
            if freeze.get(field) != expected:
                errors.append(f"freeze record {field} drift: expected {expected!r}")
        actual_source_hash = hashlib.sha256(SIGNOFF_TSV.read_bytes()).hexdigest()
        if freeze.get("source_pack_sha256") != actual_source_hash:
            errors.append("freeze record no longer addresses the current historical sign-off packet")
        for decision_id in DECISIONS:
            row = signoffs.get(decision_id, {})
            source = sources.get(decision_id, {})
            if row.get("signoff_readiness") != "ready_for_signature":
                errors.append(f"{decision_id}: historical readiness changed instead of being overridden")
            if row.get("current_status") != "presented_no_decision" or source.get("decision_status") != "presented_no_decision" or source.get("user_choice"):
                errors.append(f"{decision_id}: frozen packet contains a decision or preselection")
        for filename in EMPTY_INSTANCE_REGISTRIES:
            try:
                _, rows = read_tsv(DATA / filename)
            except (OSError, ValueError) as exc:
                errors.append(str(exc))
                continue
            if rows:
                errors.append(f"{filename}: frozen packet must have zero instances, found {len(rows)}")
        markdown = SIGNOFF_MD.read_text(encoding="utf-8") if SIGNOFF_MD.is_file() else ""
        for marker in (
            "superseded_pending_public_direction_rebase / not_ready_for_signature",
            "B 短全队协同",
            "A 逐台行动",
            "旧批准码全部失效",
            "不得回复或使用",
            "first-decision-signoff-freeze.tsv",
            "00c核心玩法总案",
        ):
            if marker not in markdown:
                errors.append(f"frozen human sign-off sheet lacks marker: {marker}")

        print("First-decision sign-off validation")
        if errors:
            for error in errors:
                print(f"FAIL  {error}")
            print(f"RESULT FAIL ({len(errors)} error(s))")
            return 1
        print("PASS  historical DEC-01/02/03/11 packet is content-addressed and safely frozen")
        print("PASS  B short-team coordination is the current Candidate recommendation; A alternating activation is the backup")
        print("PASS  no receipt, envelope, Build, human session, or migration instance exists")
        print("NOT_READY_FOR_SIGNATURE")
        print("PENDING_PUBLIC_DIRECTION_REBASE")
        print("RESULT PASS (frozen safety boundary)")
        return 0

    receipt_schema_fields = {row["field_name"] for row in receipt_schema_rows}
    for field in ("decision_spec_sha256", "selected_option_token", "accepted_clause_ids", "user_message_ref", "user_message_sha256", "receipt_artifact_sha256", "supersedes_receipt_instance_id"):
        if field not in receipt_schema_fields:
            errors.append(f"decision receipt schema lacks {field}")

    active_envelope_fields = [
        row["field_name"]
        for row in envelope_schema_rows
        if row["required"] in {"yes", "conditional:status=authorized"}
    ]
    active_envelope_field_string = ";".join(active_envelope_fields)
    for required_field in ("authorization_subject_sha256", "envelope_authorization_receipt_instance_id", "exclusive_scope_key", "shared_budget_pool_id", "shared_budget_pool_subject_sha256", "shared_budget_pool_preflight_result", "supersedes_envelope_id", "overlap_check_result", "extension_policy"):
        if required_field not in active_envelope_fields:
            errors.append(f"authorized envelope field set lacks {required_field}")

    for decision_id in DECISIONS:
        row = signoffs.get(decision_id)
        source = sources.get(decision_id)
        if not row or not source:
            continue
        if row["signoff_readiness"] != "ready_for_signature":
            errors.append(f"{decision_id}: not ready for signature")
        if row["requested_phase"] != "candidate_test_authorization":
            errors.append(f"{decision_id}: wrong requested phase")
        if row["signoff_token"] != TOKENS[decision_id]:
            errors.append(f"{decision_id}: sign-off token drift")
        if row["authorization_scope_code"] != SCOPES[decision_id]:
            errors.append(f"{decision_id}: scope code drift")
        if split(row["recommended_clause_ids"]) != CLAUSES[decision_id]:
            errors.append(f"{decision_id}: atomic clause set drift")
        for field in ("recommendation", "alternatives", "invalidation_triggers"):
            if row[field] != source[field]:
                errors.append(f"{decision_id}: {field} differs from decision ledger")
        if row["current_status"] != "presented_no_decision" or source["decision_status"] != "presented_no_decision" or source["user_choice"]:
            errors.append(f"{decision_id}: decision was prefilled or already changed")

        evidence = split(row["evidence_paths"])
        missing = EVIDENCE[decision_id] - evidence
        if missing:
            errors.append(f"{decision_id}: missing evidence {sorted(missing)}")
        for raw_path in sorted(evidence):
            resolved = (PACKAGE / raw_path).resolve()
            try:
                resolved.relative_to(PACKAGE.resolve())
            except ValueError:
                errors.append(f"{decision_id}: evidence escapes Candidate package: {raw_path}")
                continue
            if not resolved.is_file():
                errors.append(f"{decision_id}: missing evidence file: {raw_path}")

        if split(row["direction_receipt_preconditions"]) != DIRECTION_PRECONDITIONS:
            errors.append(f"{decision_id}: direction receipt can be issued without exact user/spec binding")
        required_non_auth = COMMON_NON_AUTH | SPECIAL_NON_AUTH[decision_id]
        if not required_non_auth <= split(row["explicit_non_authorization_codes"]):
            errors.append(f"{decision_id}: non-authorization set is incomplete")
        required_stops = COMMON_STOPS | SPECIAL_STOPS[decision_id]
        if not required_stops <= split(row["stop_condition_codes"]):
            errors.append(f"{decision_id}: stop-condition set is incomplete")
        for field in ("what_approval_authorizes", "explicit_non_authorizations", "stop_conditions", "execution_prerequisites", "defer_effect"):
            if not row[field].strip():
                errors.append(f"{decision_id}: empty {field}")
        for marker in ("Build", "Session", "代码写入", "上下文生成", "迁移"):
            if marker not in row["defer_effect"]:
                errors.append(f"{decision_id}: DEFER does not explicitly block {marker}")

        auth_set_id = f"DRS-{decision_id.replace('-', '')}-A"
        auth_requirement_id = f"DR-{decision_id.replace('-', '')}-A"
        if row["authorization_receipt_set_id"] != auth_set_id or row["authorization_requirement_ids"] != auth_requirement_id:
            errors.append(f"{decision_id}: Candidate receipt binding drift")
        auth_set = receipt_sets.get(auth_set_id)
        auth_requirement = requirements.get(auth_requirement_id)
        if not auth_set or auth_set["decision_id"] != decision_id or auth_set["phase"] != "candidate_test_authorization" or split(auth_set["requirement_ids"]) != {auth_requirement_id}:
            errors.append(f"{decision_id}: Candidate receipt set does not resolve")
        if not auth_requirement or auth_requirement["decision_id"] != decision_id or auth_requirement["phase"] != "candidate_test_authorization":
            errors.append(f"{decision_id}: Candidate receipt requirement does not resolve")

        expected_sets, expected_requirements = LATER_BINDINGS[decision_id]
        if split(row["later_migration_receipt_set_ids"]) != expected_sets or split(row["later_migration_requirement_ids"]) != expected_requirements:
            errors.append(f"{decision_id}: later migration binding drift")
        for set_id, requirement_id in zip(sorted(expected_sets), sorted(expected_requirements)):
            receipt_set = receipt_sets.get(set_id)
            requirement = requirements.get(requirement_id)
            if not receipt_set or receipt_set["decision_id"] != decision_id or split(receipt_set["requirement_ids"]) != {requirement_id}:
                errors.append(f"{decision_id}: unresolved later set {set_id}")
            if not requirement or requirement["decision_id"] != decision_id:
                errors.append(f"{decision_id}: unresolved later requirement {requirement_id}")

        if row["receipt_instance_schema_ref"] != "data/decision-receipt-instance-schema.tsv" or row["receipt_instance_status"] != "not_instantiated;receipt_path=none;receipt_sha256=none;user_approval_missing":
            errors.append(f"{decision_id}: receipt-instance pre-sign state drift")
        if row["execution_envelope_schema_ref"] != "data/candidate-test-execution-envelope-schema.tsv" or row["envelope_authorization_receipt_schema_ref"] != "data/execution-envelope-authorization-receipt-schema.tsv":
            errors.append(f"{decision_id}: execution authorization schema binding drift")
        if row["required_authorized_envelope_fields"] != active_envelope_field_string:
            errors.append(f"{decision_id}: authorized-envelope required field list drift")
        for marker in ("authorization_subject_sha256", "AUTHORIZE_EXACT_ENVELOPE", "instance/path/sha256/locator/user ref", "supersedes", "overlap_check", "新包络+新hash+新回执"):
            if marker not in row["envelope_authorization_rule"]:
                errors.append(f"{decision_id}: envelope authorization rule lacks {marker}")
        for marker in ("E-R0-IMPLEMENT", "E-P1-ABCD-IMPLEMENT", "STAGE0_R0_P1", "14日历日", "80内部人时", "外部现金0", "不得各得一份", "max_total_builds=1", "max_total_builds=4"):
            if marker not in row["envelope_shared_budget_rule"]:
                errors.append(f"{decision_id}: split/shared envelope rule lacks {marker}")

    # Direction receipts must not be executable permissions.
    if "DEC01_ALONE_HAS_NO_EXECUTION" not in signoffs.get("DEC-01", {}).get("execution_prerequisites", ""):
        errors.append("DEC-01 does not fail closed before downstream execution authorization")
    for decision_id in ("DEC-02", "DEC-03"):
        prerequisites = signoffs.get(decision_id, {}).get("execution_prerequisites", "")
        for marker in ("ACCEPTED_DEC01_02_03_11_RECEIPT_INSTANCES", "R0_TEST_KERNEL_M3_EXACT_EVIDENCE", "PASSED_GD1_INSTANCE", "AUTHORIZED_E_P1_ABCD_IMPLEMENT_EXACT_SUBJECT", "CURRENT_SHARED_BUDGET_POOL_PREFLIGHT", "PROTOTYPE_PREFLIGHT_PASSED"):
            if marker not in prerequisites:
                errors.append(f"{decision_id}: executable P1 prerequisite lacks {marker}")
    for marker in ("ACCEPTED_DEC11_A_RECEIPT_INSTANCE", "D09_EXACT_VERSION_AND_HASH", "EXACT_NEW_CANDIDATE_GATE_INSTANCE_IDS", "AUTHORIZED_E_R0_IMPLEMENT_EXACT_SUBJECT", "PROTOTYPE_PREFLIGHT_PASSED"):
        if marker not in signoffs.get("DEC-11", {}).get("execution_prerequisites", ""):
            errors.append(f"DEC-11: executable R0 prerequisite lacks {marker}")

    # Exact preflight split: R0 one build, P1 four-build bundle, no direction/status substitution.
    expected_preflights = {
        "PX-R0-IMPLEMENT",
        "PX-P1A-IMPLEMENT", "PX-P1B-IMPLEMENT", "PX-P1C-IMPLEMENT", "PX-P1D-IMPLEMENT",
        "PX-P1A-HUMAN", "PX-P1B-HUMAN", "PX-P1C-HUMAN", "PX-P1D-HUMAN",
        "PX-P1-SHORTLIST-ANALYSIS", "PX-P1-SHORTLIST-HUMAN",
        "PX-P2-CROSSOVER-IMPLEMENT", "PX-P2-CROSSOVER-HUMAN",
    }
    if not expected_preflights <= set(preflights):
        errors.append(f"missing fail-closed preflight contracts: {sorted(expected_preflights - set(preflights))}")
    r0 = preflights.get("PX-R0-IMPLEMENT", {})
    if r0.get("envelope_prototype_scope_rule") != "must_equal:R0-TEST-KERNEL;must_not_include:D04-P1-A,D04-P1-B,D04-P1-C,D04-P1-D" or r0.get("required_envelope_max_total_builds") != "1":
        errors.append("R0 preflight does not isolate its single Build")
    for suffix in "ABCD":
        row = preflights.get(f"PX-P1{suffix}-IMPLEMENT", {})
        if row.get("envelope_prototype_scope_rule") != "must_equal_bundle:D04-P1-A,D04-P1-B,D04-P1-C,D04-P1-D;must_not_include:R0-TEST-KERNEL" or row.get("required_envelope_max_total_builds") != "4" or row.get("required_shared_budget_program_scope_key") != "STAGE0_R0_P1" or row.get("required_upstream_evidence") != "R0-TEST-KERNEL@M3":
            errors.append(f"P1{suffix} implementation preflight split/budget drift")
        if not {"gate_definition", "decision_status"} <= split(row.get("forbidden_substitutions", "")):
            errors.append(f"P1{suffix} permits a Gate definition or decision status as execution evidence")
    crossover = preflights.get("PX-P2-CROSSOVER-IMPLEMENT", {})
    if "DRS-DEC04-A" not in split(crossover.get("required_decision_receipt_set_templates", "")) or "DEC03_M" not in split(crossover.get("forbidden_substitutions", "")):
        errors.append("C2 crossover is not separately authorized before DEC-03-M")

    shared = neutrality.get("TSN-P1-SHARED", {})
    result = neutrality.get("TSN-P1-RESULT", {})
    variant_d = neutrality.get("TSN-P1-D", {})
    final = neutrality.get("TSN-DEC03-FINAL", {})
    expected_p1_outcomes = {"shortlist_two", "shortlist_three", "shortlist_four", "no_winner", "revise_top_two", "retire_all"}
    if split(shared.get("prototype_id", "")) != {"D04-P1-A", "D04-P1-B", "D04-P1-C", "D04-P1-D"}:
        errors.append("neutrality shared boundary is not formal A/B/C/D")
    if split(result.get("allowed_outcomes", "")) != expected_p1_outcomes or not {"select", "single_winner", "approved_for_bounded_migration"} <= split(result.get("prohibited_outcomes", "")):
        errors.append("P1 result can choose or migrate a winner")
    if "formal_baseline_not_fallback_or_preselected_loser" not in variant_d.get("reversible_carrier_rule", ""):
        errors.append("P1-D is not a formal neutral control")
    if split(final.get("allowed_outcomes", "")) != {"select", "revise", "no_selection", "retire_all"}:
        errors.append("DEC-03-M final result enum drift")

    # Pre-sign registries must be real but empty: no fabricated approval or execution.
    for filename in EMPTY_INSTANCE_REGISTRIES:
        try:
            _, rows = read_tsv(DATA / filename)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if rows:
            errors.append(f"{filename}: pre-sign package already contains {len(rows)} instance(s)")

    markdown = SIGNOFF_MD.read_text(encoding="utf-8") if SIGNOFF_MD.is_file() else ""
    for marker in (
        "ready_for_signature / presented_no_decision / no_receipt_instance / no_execution_envelope",
        "现在只请求四项 Candidate 测试方向裁决",
        "不授权包络、Build、真人招募、数据采集、现行链迁移或任何 Current 写入",
        "D 是正式传统阵营回合控制组",
        "P1 只淘汰或形成 shortlist",
        "最小核心 C2",
        "Writer-readable Current 输出必须为 0",
        "E-R0-IMPLEMENT",
        "E-P1-ABCD-IMPLEMENT",
        "共同消耗 `STAGE0_R0_P1` 池",
        "合计**上限仍为 14 日历日、80 内部人时、外部现金 0",
        "方向回执只回答",
        "AUTHORIZE_EXACT_ENVELOPE",
        "任何 `DEFER` 都保持 fail-closed",
    ):
        if marker not in markdown:
            errors.append(f"human sign-off sheet lacks marker: {marker}")
    for decision_id, token in TOKENS.items():
        if f"{decision_id} = {token}" not in markdown:
            errors.append(f"human sign-off sheet lacks exact token for {decision_id}")
    for short_clause in ("D01-C01", "D02-C05", "D03-C07", "D11-C05"):
        if short_clause not in markdown:
            errors.append(f"human sign-off sheet lacks atomic clause {short_clause}")

    print("First-decision sign-off validation")
    if errors:
        for error in errors:
            print(f"FAIL  {error}")
        print(f"RESULT FAIL ({len(errors)} error(s))")
        return 1
    print("PASS  DEC-01/02/03/11 are presentable for a direction-only user decision; none is preselected")
    print("PASS  exact option tokens, atomic clauses, alternatives, evidence, exclusions, invalidation, and DEFER behavior are bound")
    print("PASS  direction receipts cannot substitute for R0/P1/crossover execution preflights or exact-hash envelope authorization")
    print("PASS  R0=1 Build and P1=A/B/C/D=4 Builds are split but share one 14d/80h/cash0 Stage0 pool")
    print("PASS  P1 can only shortlist; minimal C2 crossover precedes DEC-03-M; DEC-11 remains isolated and phased")
    print("PASS  no decision receipt, envelope receipt, budget pool, envelope, Gate instance, or preflight instance is fabricated")
    print("RESULT PASS (6 checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
