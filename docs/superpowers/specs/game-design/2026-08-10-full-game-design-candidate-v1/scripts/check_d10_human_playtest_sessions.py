#!/usr/bin/env python3
"""Validate the D10 human-playtest Session evidence chain.

A PASS proves only that the Candidate contract is internally consistent and
that the current ledger truthfully remains at zero people / zero Sessions /
not_run.  It never creates consent, authorizes recruitment or collection,
provides M5/M6 evidence, or records user gameplay acceptance.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable


PACKAGE = Path(__file__).resolve().parents[1]
DATA = PACKAGE / "data"
SCHEMA_PATH = DATA / "human-playtest-session-instance-schema.tsv"
INSTANCE_PATH = DATA / "human-playtest-session-instances.tsv"
HINT_PATH = DATA / "human-playtest-hint-level-contracts.tsv"
STATUS_PATH = DATA / "human-playtest-program-status.tsv"
CROSSWALK_PATH = DATA / "human-playtest-session-result-crosswalk.tsv"
LEGACY_RESULT_SCHEMA_PATH = DATA / "playtest-session-result-schema.tsv"
PROTOTYPE_PATH = DATA / "prototype-test-registry.tsv"
CASE_PATH = DATA / "playtest-cases.tsv"
EVIDENCE_PATH = DATA / "acceptance-evidence-registry.tsv"
PREFLIGHT_PATH = DATA / "prototype-execution-preflight-instances.tsv"
ENVELOPE_PATH = DATA / "candidate-test-execution-envelopes.tsv"
ENVELOPE_RECEIPT_PATH = DATA / "execution-envelope-authorization-receipts.tsv"
ROLE_PATH = DATA / "production-role-registry.tsv"
CONTRACT_DOC_PATH = PACKAGE / "validation/d10-human-playtest-session-evidence-chain-v0.1.md"

SCHEMA_HEADER = (
    "field_name",
    "data_type",
    "required",
    "purpose",
    "validation",
    "invalid_if_missing",
    "status",
)

EXPECTED_FIELDS = (
    "schema_version",
    "session_instance_id",
    "test_run_id",
    "lifecycle_status",
    "prototype_id",
    "case_ids",
    "acceptance_evidence_id",
    "human_run_preflight_instance_id",
    "preflight_payload_sha256",
    "execution_envelope_id",
    "authorization_subject_sha256",
    "envelope_authorization_receipt_instance_id",
    "envelope_authorization_receipt_sha256",
    "participant_cohort_id",
    "facilitator_role_id",
    "observer_role_ids",
    "started_at",
    "ended_at",
    "asset_authorization_state",
    "build_id",
    "build_manifest_path_and_sha256",
    "content_manifest_id",
    "content_manifest_path_and_sha256",
    "ruleset_version",
    "ruleset_path_and_sha256",
    "map_or_scene_version",
    "map_or_scene_path_and_sha256",
    "tutorial_version",
    "tutorial_path_and_sha256",
    "ui_version",
    "ui_path_and_sha256",
    "source_snapshot_manifest_path_and_sha256",
    "case_snapshot_path_and_sha256",
    "facilitator_script_version",
    "facilitator_script_path_and_sha256",
    "telemetry_schema_version",
    "telemetry_schema_path_and_sha256",
    "privacy_consent_snapshot_path_and_sha256",
    "known_issues_snapshot_path_and_sha256",
    "participant_pseudonym_id",
    "participant_profile",
    "first_contact_class",
    "prior_exposure_tokens",
    "first_exposure_eligibility",
    "blind_variant_label",
    "variant_order",
    "device_and_accessibility_profile",
    "accommodation_ref_and_sha256",
    "consent_record_ref_and_sha256",
    "consent_scope_tokens",
    "consent_captured_at",
    "right_to_withdraw_acknowledged",
    "retention_delete_at",
    "privacy_access_role_ids",
    "contact_data_separation_result",
    "compensation_state",
    "deletion_request_state",
    "sensitive_data_event_ref",
    "hint_event_log_ref_and_sha256",
    "maximum_hint_level",
    "hint_count",
    "facilitator_rescue_count",
    "strategy_hint_count",
    "hint_contamination_result",
    "safety_or_withdrawal_interventions",
    "completion_state",
    "solution_family",
    "task_result_ref_and_sha256",
    "behavior_log_ref_and_sha256",
    "input_log_ref_and_sha256",
    "telemetry_log_ref_and_sha256",
    "state_hash_report_ref_and_sha256",
    "video_ref_and_sha256",
    "audio_ref_and_sha256",
    "retell_transcript_ref_and_sha256",
    "observer_notes_ref_and_sha256",
    "preference_reason_ref_and_sha256",
    "planning_time_median_seconds",
    "input_error_count",
    "causal_items_correct",
    "transfer_result",
    "free_retell_score",
    "body_score",
    "agency_score",
    "replay_intent",
    "blind_preference_token",
    "fatigue_score",
    "discomfort_level",
    "participant_exit_state",
    "withdrawal_reason_category",
    "adverse_event_ref_and_sha256",
    "artifact_integrity_result",
    "frozen_binding_result",
    "authorization_binding_result",
    "privacy_compliance_result",
    "first_exposure_result",
    "evidence_validity",
    "metric_exclusion_ids",
    "invalid_reason_codes",
    "claim_scope",
    "claim_boundary",
    "aggregation_batch_id",
    "session_payload_sha256",
    "recorded_by",
    "recorded_at",
    "reviewed_by",
    "reviewed_at",
    "supersedes_session_instance_id",
    "invalidation_reason",
    "user_adjudication_state",
    "user_adjudication_receipt_ref_and_sha256",
    "user_adjudication_scope",
)

PATH_HASH_FIELDS = {
    field
    for field in EXPECTED_FIELDS
    if field.endswith("_path_and_sha256") or field.endswith("_ref_and_sha256")
}
NON_NONE_HASH_FIELDS = {
    "build_manifest_path_and_sha256",
    "content_manifest_path_and_sha256",
    "ruleset_path_and_sha256",
    "map_or_scene_path_and_sha256",
    "tutorial_path_and_sha256",
    "ui_path_and_sha256",
    "source_snapshot_manifest_path_and_sha256",
    "case_snapshot_path_and_sha256",
    "facilitator_script_path_and_sha256",
    "telemetry_schema_path_and_sha256",
    "privacy_consent_snapshot_path_and_sha256",
    "known_issues_snapshot_path_and_sha256",
    "consent_record_ref_and_sha256",
    "task_result_ref_and_sha256",
    "behavior_log_ref_and_sha256",
    "input_log_ref_and_sha256",
    "state_hash_report_ref_and_sha256",
    "retell_transcript_ref_and_sha256",
    "observer_notes_ref_and_sha256",
}
SHA_FIELDS = {
    "preflight_payload_sha256",
    "authorization_subject_sha256",
    "envelope_authorization_receipt_sha256",
    "session_payload_sha256",
}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
SESSION_ID_RE = re.compile(r"^HPS-[A-Z0-9._-]+$")
RUN_ID_RE = re.compile(r"^HTR-[A-Z0-9._-]+$")
PARTICIPANT_ID_RE = re.compile(r"^PT-[A-Z0-9._-]+$")
BLIND_FORBIDDEN_RE = re.compile(r"^(A|B|C|D)$|wego|scheduler|阵营|交替|混合", re.IGNORECASE)

NON_TERMINAL_USER_STATES = {"not_submitted", "pending_user"}
TERMINAL_USER_STATES = {"approved_for_bounded_migration", "revise", "retire", "invalidated"}

EXPECTED_HINTS = {
    "H0": ("none", "valid_if_other_gates_pass"),
    "H1": ("none_if_predeclared_else_U-RESCUE", "valid_or_withdrawal_only"),
    "H2": ("U-COMPLETE_excluded;U-RESCUE_counted", "other_metrics_may_remain_after_review"),
    "H3": ("U-COMPLETE,L-CAUSE,L-TRANSFER,R-FREE_excluded", "needs_review_not_counted_for_M5_understanding"),
    "H4": ("U-COMPLETE,L-CAUSE,L-TRANSFER,S-DIVERSITY,F-REPLAY,R-FREE,F-AGENCY_excluded", "performance_invalid_not_counted_for_M5"),
}


def read_tsv(path: Path, errors: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            header = list(reader.fieldnames or [])
            rows: list[dict[str, str]] = []
            for line_no, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    errors.append(f"{path.name}:{line_no}: TSV width mismatch")
                    continue
                row["_line"] = str(line_no)
                rows.append(row)
    except OSError as exc:
        errors.append(f"cannot read {path}: {exc}")
        return [], []
    if not header:
        errors.append(f"{path.name}: missing header")
    return header, rows


def keyed(rows: list[dict[str, str]], key: str, label: str, errors: list[str]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value or value in result:
            errors.append(f"{label}: missing/duplicate {key}={value!r}")
        else:
            result[value] = row
    return result


def split_tokens(value: str) -> list[str]:
    if value in {"", "none", "not_applicable", "not_tested"}:
        return []
    return [token for token in value.split(";") if token]


def parse_time(value: str, label: str, errors: list[str]) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label}: invalid ISO-8601 {value!r}")
        return None


def integer(value: str, label: str, errors: list[str]) -> int | None:
    try:
        parsed = int(value)
    except ValueError:
        errors.append(f"{label}: expected integer, got {value!r}")
        return None
    if parsed < 0:
        errors.append(f"{label}: must be >=0")
        return None
    return parsed


def parse_hash_pairs(value: str, label: str, errors: list[str]) -> list[tuple[str, str]]:
    if value == "none":
        return []
    pairs: list[tuple[str, str]] = []
    for token in split_tokens(value):
        if "=" not in token:
            errors.append(f"{label}: expected locator=sha256 token, got {token!r}")
            continue
        locator, digest = token.rsplit("=", 1)
        if not locator or not SHA_RE.fullmatch(digest):
            errors.append(f"{label}: invalid locator/hash pair {token!r}")
            continue
        pairs.append((locator, digest))
    if not pairs and value != "none":
        errors.append(f"{label}: no valid locator/hash pairs")
    return pairs


def canonical_session_hash(row: dict[str, str]) -> str:
    payload = {
        field: row.get(field, "")
        for field in EXPECTED_FIELDS
        if field != "session_payload_sha256"
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evidence_case_ids(row: dict[str, str]) -> set[str]:
    return set(split_tokens(row.get("case_ids", "")))


def validate_instance(
    row: dict[str, str],
    *,
    prototypes: dict[str, dict[str, str]],
    cases: dict[str, dict[str, str]],
    evidence: dict[str, dict[str, str]],
    preflights: dict[str, dict[str, str]],
    envelopes: dict[str, dict[str, str]],
    receipts: dict[str, dict[str, str]],
    roles: set[str],
    errors: list[str],
) -> None:
    sid = row.get("session_instance_id", "<missing>")
    label = f"Session {sid}"
    for field in EXPECTED_FIELDS:
        if field not in row or row[field] == "":
            errors.append(f"{label}: missing {field}")

    if row.get("schema_version") != "candidate_human_playtest_session_v1":
        errors.append(f"{label}: schema_version drift")
    if not SESSION_ID_RE.fullmatch(row.get("session_instance_id", "")):
        errors.append(f"{label}: invalid session_instance_id")
    if not RUN_ID_RE.fullmatch(row.get("test_run_id", "")):
        errors.append(f"{label}: invalid test_run_id")
    if row.get("lifecycle_status") not in {"planned", "ready", "running", "completed", "withdrawn", "aborted", "invalidated"}:
        errors.append(f"{label}: invalid lifecycle_status")

    prototype_id = row.get("prototype_id", "")
    if prototype_id not in prototypes:
        errors.append(f"{label}: unknown prototype_id {prototype_id!r}")
    case_ids = set(split_tokens(row.get("case_ids", "")))
    if not case_ids:
        errors.append(f"{label}: no case_ids")
    for case_id in case_ids:
        case = cases.get(case_id)
        if case is None:
            errors.append(f"{label}: unknown case {case_id}")
            continue
        if case.get("test_kind") == "automated":
            errors.append(f"{label}: automated case {case_id} cannot be a human Session")
        applicable = set(split_tokens(case.get("applicable_prototype_ids", "")))
        if prototype_id not in applicable:
            errors.append(f"{label}: case {case_id} does not apply to {prototype_id}")

    evidence_id = row.get("acceptance_evidence_id", "")
    evidence_row = evidence.get(evidence_id)
    if evidence_row is None:
        errors.append(f"{label}: unknown acceptance_evidence_id {evidence_id!r}")
    elif not case_ids <= evidence_case_ids(evidence_row):
        errors.append(f"{label}: evidence {evidence_id} does not cover all case_ids")

    preflight_id = row.get("human_run_preflight_instance_id", "")
    preflight = preflights.get(preflight_id)
    if preflight is None:
        errors.append(f"{label}: unknown human_run preflight {preflight_id!r}")
    else:
        expected = {
            "execution_phase": "human_run",
            "status": "passed",
            "prototype_id": prototype_id,
            "execution_envelope_id": row.get("execution_envelope_id", ""),
            "envelope_authorization_subject_sha256": row.get("authorization_subject_sha256", ""),
            "envelope_authorization_receipt_instance_id": row.get("envelope_authorization_receipt_instance_id", ""),
            "envelope_authorization_receipt_sha256": row.get("envelope_authorization_receipt_sha256", ""),
            "build_id": row.get("build_id", ""),
            "preflight_payload_sha256": row.get("preflight_payload_sha256", ""),
        }
        for field, value in expected.items():
            if preflight.get(field) != value:
                errors.append(f"{label}: preflight {field} mismatch")
        if not case_ids <= set(split_tokens(preflight.get("test_case_ids", ""))):
            errors.append(f"{label}: preflight does not freeze all case_ids")

    envelope_id = row.get("execution_envelope_id", "")
    envelope = envelopes.get(envelope_id)
    if envelope is None:
        errors.append(f"{label}: unknown execution envelope {envelope_id!r}")
    else:
        expected = {
            "envelope_phase": "human_run",
            "status": "authorized",
            "authorization_subject_sha256": row.get("authorization_subject_sha256", ""),
            "envelope_authorization_receipt_instance_id": row.get("envelope_authorization_receipt_instance_id", ""),
            "envelope_authorization_receipt_sha256": row.get("envelope_authorization_receipt_sha256", ""),
        }
        for field, value in expected.items():
            if envelope.get(field) != value:
                errors.append(f"{label}: envelope {field} mismatch")
        if prototype_id not in set(split_tokens(envelope.get("authorized_prototype_ids", ""))):
            errors.append(f"{label}: envelope does not authorize prototype")
        actions = set(split_tokens(envelope.get("authorized_action_codes", "")))
        if not {"prepare_human", "collect_data"} <= actions:
            errors.append(f"{label}: envelope lacks prepare_human/collect_data actions")
        cap = integer(envelope.get("participant_cap", ""), f"{label}.envelope.participant_cap", errors)
        if cap is not None and cap < 1:
            errors.append(f"{label}: envelope participant_cap must be >=1")

    receipt_id = row.get("envelope_authorization_receipt_instance_id", "")
    receipt = receipts.get(receipt_id)
    if receipt is None:
        errors.append(f"{label}: unknown envelope authorization receipt {receipt_id!r}")
    else:
        if receipt.get("status") != "accepted":
            errors.append(f"{label}: envelope receipt is not accepted")
        if receipt.get("envelope_id") != envelope_id:
            errors.append(f"{label}: envelope receipt envelope mismatch")
        if receipt.get("authorization_subject_sha256") != row.get("authorization_subject_sha256"):
            errors.append(f"{label}: envelope receipt subject hash mismatch")
        if receipt.get("receipt_artifact_sha256") != row.get("envelope_authorization_receipt_sha256"):
            errors.append(f"{label}: envelope receipt artifact hash mismatch")

    for field in SHA_FIELDS:
        if not SHA_RE.fullmatch(row.get(field, "")):
            errors.append(f"{label}: {field} is not lowercase SHA-256")
    for field in PATH_HASH_FIELDS:
        pairs = parse_hash_pairs(row.get(field, ""), f"{label}.{field}", errors)
        if field in NON_NONE_HASH_FIELDS and not pairs:
            errors.append(f"{label}: {field} cannot be none")

    participant_id = row.get("participant_pseudonym_id", "")
    if not PARTICIPANT_ID_RE.fullmatch(participant_id):
        errors.append(f"{label}: invalid participant_pseudonym_id")
    if "@" in participant_id or re.search(r"\d{7,}", participant_id):
        errors.append(f"{label}: participant pseudonym appears to contain contact data")

    contact_class = row.get("first_contact_class")
    exposure = row.get("prior_exposure_tokens")
    eligibility = row.get("first_exposure_eligibility")
    if contact_class in {"cold", "content_cold"} and (exposure != "none" or eligibility != "pass"):
        errors.append(f"{label}: cold Session has prior exposure or failed eligibility")
    if contact_class not in {"cold", "content_cold", "returning", "learned", "specialist", "not_applicable"}:
        errors.append(f"{label}: invalid first_contact_class")
    if BLIND_FORBIDDEN_RE.search(row.get("blind_variant_label", "")):
        errors.append(f"{label}: blind_variant_label reveals variant identity")
    expected_contact_classes = {
        "human_cold": {"cold"},
        "content_cold": {"content_cold"},
        "chapter_continuous_cold": {"content_cold"},
        "human_returning": {"returning"},
        "human_learned": {"learned"},
        "human_replication": {"cold", "content_cold"},
        "human_crossover": {"cold", "returning"},
        "accessibility": {"specialist"},
        "input_accessibility": {"specialist"},
        "cognitive_accessibility": {"specialist"},
        "vertical_slice": {"cold", "content_cold"},
    }
    for case_id in case_ids:
        case = cases.get(case_id, {})
        allowed_classes = expected_contact_classes.get(case.get("test_kind"))
        if allowed_classes is not None and contact_class not in allowed_classes:
            errors.append(f"{label}: {case_id} requires first_contact_class in {sorted(allowed_classes)}")

    consent_scope = set(split_tokens(row.get("consent_scope_tokens", "")))
    allowed_consent = {"screen", "input", "telemetry", "voice", "face", "anonymous_quote"}
    if not consent_scope <= allowed_consent:
        errors.append(f"{label}: unknown consent scope tokens")
    if row.get("right_to_withdraw_acknowledged") != "true":
        errors.append(f"{label}: right to withdraw not acknowledged")
    if row.get("contact_data_separation_result") != "pass":
        errors.append(f"{label}: contact/test data not separated")
    if row.get("video_ref_and_sha256") != "none" and not ({"screen", "face"} & consent_scope):
        errors.append(f"{label}: video saved outside consent scope")
    if row.get("audio_ref_and_sha256") != "none" and "voice" not in consent_scope:
        errors.append(f"{label}: audio saved outside consent scope")
    if row.get("telemetry_log_ref_and_sha256") != "none" and "telemetry" not in consent_scope:
        errors.append(f"{label}: telemetry saved outside consent scope")
    if row.get("sensitive_data_event_ref") != "none" and row.get("lifecycle_status") not in {"withdrawn", "aborted", "invalidated"}:
        errors.append(f"{label}: sensitive data event did not stop/invalidate Session")

    role_fields = [row.get("facilitator_role_id", ""), row.get("recorded_by", ""), row.get("reviewed_by", "")]
    role_fields.extend(split_tokens(row.get("observer_role_ids", "")))
    role_fields.extend(split_tokens(row.get("privacy_access_role_ids", "")))
    for role_id in role_fields:
        if role_id and role_id != "none" and role_id not in roles:
            errors.append(f"{label}: unknown role {role_id}")
    if row.get("recorded_by") == row.get("reviewed_by"):
        errors.append(f"{label}: recorder cannot independently review own Session")

    hint_count = integer(row.get("hint_count", ""), f"{label}.hint_count", errors)
    rescue_count = integer(row.get("facilitator_rescue_count", ""), f"{label}.facilitator_rescue_count", errors)
    strategy_count = integer(row.get("strategy_hint_count", ""), f"{label}.strategy_hint_count", errors)
    if hint_count is not None and rescue_count is not None and rescue_count > hint_count:
        errors.append(f"{label}: facilitator_rescue_count exceeds hint_count")
    if hint_count is not None and strategy_count is not None and strategy_count > hint_count:
        errors.append(f"{label}: strategy_hint_count exceeds hint_count")
    if row.get("maximum_hint_level") == "H0" and hint_count != 0:
        errors.append(f"{label}: H0 requires zero hints")
    if hint_count == 0 and row.get("hint_event_log_ref_and_sha256") != "none":
        errors.append(f"{label}: zero hints must use none hint log")
    if hint_count is not None and hint_count > 0 and row.get("hint_event_log_ref_and_sha256") == "none":
        errors.append(f"{label}: hinted Session lacks hint event log")
    if strategy_count is not None and strategy_count > 0 and row.get("hint_contamination_result") != "performance_invalid":
        errors.append(f"{label}: strategy hint did not invalidate performance")
    if row.get("maximum_hint_level") == "H4" and row.get("evidence_validity") == "valid":
        errors.append(f"{label}: H4 Session cannot be valid")

    exit_state = row.get("participant_exit_state")
    completion = row.get("completion_state")
    validity = row.get("evidence_validity")
    if exit_state == "withdrew" and completion != "withdraw":
        errors.append(f"{label}: withdrawal exit/completion mismatch")
    lifecycle = row.get("lifecycle_status")
    lifecycle_exit_pairs = {
        "completed": "completed",
        "withdrawn": "withdrew",
        "aborted": {"facilitator_abort", "technical_abort"},
    }
    expected_exit = lifecycle_exit_pairs.get(lifecycle)
    if isinstance(expected_exit, str) and exit_state != expected_exit:
        errors.append(f"{label}: lifecycle/participant exit mismatch")
    if isinstance(expected_exit, set) and exit_state not in expected_exit:
        errors.append(f"{label}: aborted lifecycle lacks abort exit state")
    if exit_state in {"withdrew", "facilitator_abort", "technical_abort"} and validity == "valid":
        errors.append(f"{label}: withdrawn/aborted Session cannot be fully valid")
    if row.get("discomfort_level") in {"moderate", "severe"} and row.get("adverse_event_ref_and_sha256") == "none":
        errors.append(f"{label}: material discomfort lacks adverse event record")

    pass_fields = ("artifact_integrity_result", "frozen_binding_result", "authorization_binding_result", "privacy_compliance_result")
    if validity == "valid":
        if lifecycle != "completed" or exit_state != "completed":
            errors.append(f"{label}: valid evidence requires completed lifecycle and exit")
        for field in pass_fields:
            if row.get(field) != "pass":
                errors.append(f"{label}: valid evidence requires {field}=pass")
        if row.get("hint_contamination_result") == "performance_invalid":
            errors.append(f"{label}: performance-invalid hints cannot yield valid evidence")
        if row.get("invalid_reason_codes") != "none":
            errors.append(f"{label}: valid evidence carries invalid reasons")
    if validity == "withdrawal_only" and exit_state != "withdrew":
        errors.append(f"{label}: withdrawal_only requires participant withdrawal")

    for field in ("hint_count", "facilitator_rescue_count", "strategy_hint_count", "input_error_count", "causal_items_correct"):
        value = row.get(field, "")
        if value != "not_tested":
            integer(value, f"{label}.{field}", errors)
    for field in ("planning_time_median_seconds",):
        value = row.get(field, "")
        if value != "not_tested":
            try:
                if float(value) < 0:
                    raise ValueError
            except ValueError:
                errors.append(f"{label}.{field}: expected non-negative decimal or not_tested")

    started = parse_time(row.get("started_at", ""), f"{label}.started_at", errors)
    ended = parse_time(row.get("ended_at", ""), f"{label}.ended_at", errors)
    consent_at = parse_time(row.get("consent_captured_at", ""), f"{label}.consent_captured_at", errors)
    retention_at = parse_time(row.get("retention_delete_at", ""), f"{label}.retention_delete_at", errors)
    recorded_at = parse_time(row.get("recorded_at", ""), f"{label}.recorded_at", errors)
    reviewed_at = parse_time(row.get("reviewed_at", ""), f"{label}.reviewed_at", errors)
    if started and ended and not started < ended:
        errors.append(f"{label}: ended_at must be after started_at")
    if consent_at and started and not consent_at <= started:
        errors.append(f"{label}: consent must precede Session start")
    if retention_at and ended and not retention_at > ended:
        errors.append(f"{label}: retention_delete_at must follow Session end")
    if recorded_at and started and recorded_at < started:
        errors.append(f"{label}: recorded_at precedes Session")
    if reviewed_at and ended and reviewed_at < ended:
        errors.append(f"{label}: reviewed_at precedes Session end")
    if envelope is not None:
        effective = parse_time(envelope.get("effective_at", ""), f"{label}.envelope.effective_at", errors)
        expires = parse_time(envelope.get("expires_at", ""), f"{label}.envelope.expires_at", errors)
        if started and effective and expires and not effective <= started < expires:
            errors.append(f"{label}: Session outside authorized envelope window")

    if row.get("claim_boundary") != "evidence_only_no_user_acceptance":
        errors.append(f"{label}: claim_boundary overclaims user acceptance")
    claim_scope = row.get("claim_scope", "")
    for value in (prototype_id, row.get("build_id", ""), row.get("ruleset_version", ""), row.get("map_or_scene_version", ""), *sorted(case_ids)):
        if value and value not in claim_scope:
            errors.append(f"{label}: claim_scope omits bound value {value}")
    user_state = row.get("user_adjudication_state")
    user_receipt = row.get("user_adjudication_receipt_ref_and_sha256")
    user_scope = row.get("user_adjudication_scope")
    if user_state in NON_TERMINAL_USER_STATES and (user_receipt != "none" or user_scope != "none"):
        errors.append(f"{label}: non-terminal user state carries a receipt/scope")
    if user_state in TERMINAL_USER_STATES and (user_receipt == "none" or user_scope == "none"):
        errors.append(f"{label}: terminal user adjudication lacks receipt/scope")
    if user_state not in NON_TERMINAL_USER_STATES | TERMINAL_USER_STATES:
        errors.append(f"{label}: invalid user_adjudication_state")

    if row.get("session_payload_sha256") != canonical_session_hash(row):
        errors.append(f"{label}: session_payload_sha256 mismatch")


def load_context(errors: list[str]) -> dict[str, object]:
    _, prototype_rows = read_tsv(PROTOTYPE_PATH, errors)
    _, case_rows = read_tsv(CASE_PATH, errors)
    _, evidence_rows = read_tsv(EVIDENCE_PATH, errors)
    _, preflight_rows = read_tsv(PREFLIGHT_PATH, errors)
    _, envelope_rows = read_tsv(ENVELOPE_PATH, errors)
    _, receipt_rows = read_tsv(ENVELOPE_RECEIPT_PATH, errors)
    _, role_rows = read_tsv(ROLE_PATH, errors)
    return {
        "prototypes": keyed(prototype_rows, "prototype_id", "prototype registry", errors),
        "cases": keyed(case_rows, "case_id", "playtest cases", errors),
        "evidence": keyed(evidence_rows, "evidence_id", "evidence registry", errors),
        "preflights": keyed(preflight_rows, "preflight_instance_id", "preflight instances", errors),
        "envelopes": keyed(envelope_rows, "envelope_id", "execution envelopes", errors),
        "receipts": keyed(receipt_rows, "envelope_receipt_instance_id", "envelope receipts", errors),
        "roles": {row["role_id"] for row in role_rows},
        "prototype_rows": prototype_rows,
        "case_rows": case_rows,
        "evidence_rows": evidence_rows,
        "preflight_rows": preflight_rows,
        "envelope_rows": envelope_rows,
    }


def validate_package() -> tuple[list[str], dict[str, int | str]]:
    errors: list[str] = []
    schema_header, schema_rows = read_tsv(SCHEMA_PATH, errors)
    instance_header, instance_rows = read_tsv(INSTANCE_PATH, errors)
    hint_header, hint_rows = read_tsv(HINT_PATH, errors)
    status_header, status_rows = read_tsv(STATUS_PATH, errors)
    crosswalk_header, crosswalk_rows = read_tsv(CROSSWALK_PATH, errors)
    legacy_header, legacy_rows = read_tsv(LEGACY_RESULT_SCHEMA_PATH, errors)
    context = load_context(errors)

    if tuple(schema_header) != SCHEMA_HEADER:
        errors.append("human Session schema header differs")
    schema_fields = [row.get("field_name", "") for row in schema_rows]
    if tuple(schema_fields) != EXPECTED_FIELDS:
        errors.append("human Session schema field order/set differs")
    if len(schema_fields) != len(set(schema_fields)):
        errors.append("human Session schema has duplicate fields")
    for row in schema_rows:
        if row.get("status") != "candidate_contract_v1":
            errors.append(f"schema field {row.get('field_name')}: status drift")
        for field in SCHEMA_HEADER:
            if not row.get(field, ""):
                errors.append(f"schema field {row.get('field_name')}: missing {field}")
    if tuple(instance_header) != EXPECTED_FIELDS:
        errors.append("human Session instance header does not match schema")

    if crosswalk_header != ["result_schema_field", "session_instance_field", "binding_rule", "status"]:
        errors.append("result crosswalk header differs")
    legacy_fields = [row.get("field_name", "") for row in legacy_rows]
    crosswalk = keyed(crosswalk_rows, "result_schema_field", "result crosswalk", errors)
    if set(crosswalk) != set(legacy_fields) or len(crosswalk_rows) != len(legacy_rows):
        errors.append("result crosswalk does not cover the legacy result schema exactly")
    for old_field, row in crosswalk.items():
        if row.get("session_instance_field") not in EXPECTED_FIELDS:
            errors.append(f"crosswalk {old_field}: unknown Session field")
        if row.get("status") != "candidate_crosswalk_v1" or not row.get("binding_rule"):
            errors.append(f"crosswalk {old_field}: incomplete binding")
    if legacy_header != ["field_name", "required", "purpose", "invalid_if_missing"]:
        errors.append("legacy result schema header drift")

    if hint_header != ["hint_level", "name", "allowed_trigger", "allowed_content", "required_log_fields", "metric_effect", "session_effect", "forbidden_content", "status"]:
        errors.append("hint contract header differs")
    hints = keyed(hint_rows, "hint_level", "hint contracts", errors)
    if set(hints) != set(EXPECTED_HINTS):
        errors.append("hint contract must contain exactly H0-H4")
    for level, expected in EXPECTED_HINTS.items():
        row = hints.get(level, {})
        if (row.get("metric_effect"), row.get("session_effect")) != expected:
            errors.append(f"hint {level}: effect drift")
        if row.get("status") != "candidate_contract_v1" or not row.get("forbidden_content"):
            errors.append(f"hint {level}: incomplete boundary")

    if status_header != ["program_id", "status", "session_count", "participant_count", "authorized_human_run_envelope_count", "passed_human_run_preflight_count", "human_evidence_claim", "user_adjudication_status", "notes"]:
        errors.append("human playtest program status header differs")
    if len(status_rows) != 1:
        errors.append("human playtest program status must have exactly one row")

    cases = context["cases"]
    prototypes = context["prototypes"]
    evidence = context["evidence"]
    assert isinstance(cases, dict) and isinstance(prototypes, dict) and isinstance(evidence, dict)
    nonauto = {case_id: row for case_id, row in cases.items() if row.get("test_kind") != "automated"}
    if len(nonauto) != 33:
        errors.append(f"expected 33 non-automated Cases, found {len(nonauto)}")
    for case_id, row in nonauto.items():
        if row.get("status") != "pending":
            errors.append(f"non-automated case {case_id}: status must remain pending before Sessions")
        for prototype_id in split_tokens(row.get("applicable_prototype_ids", "")):
            if prototype_id not in prototypes:
                errors.append(f"non-automated case {case_id}: unknown prototype {prototype_id}")
    evidence_cover = set().union(*(evidence_case_ids(row) for row in evidence.values())) if evidence else set()
    missing_evidence = set(nonauto) - evidence_cover
    if missing_evidence:
        errors.append(f"non-automated Cases missing evidence route: {sorted(missing_evidence)}")

    session_ids: set[str] = set()
    participant_ids: set[str] = set()
    for row in instance_rows:
        sid = row.get("session_instance_id", "")
        if sid in session_ids:
            errors.append(f"duplicate Session instance {sid}")
        session_ids.add(sid)
        participant_ids.add(row.get("participant_pseudonym_id", ""))
        validate_instance(
            row,
            prototypes=context["prototypes"],
            cases=context["cases"],
            evidence=context["evidence"],
            preflights=context["preflights"],
            envelopes=context["envelopes"],
            receipts=context["receipts"],
            roles=context["roles"],
            errors=errors,
        )

    authorized_human_envelopes = [
        row for row in context["envelope_rows"]
        if row.get("envelope_phase") == "human_run" and row.get("status") == "authorized"
    ]
    passed_human_preflights = [
        row for row in context["preflight_rows"]
        if row.get("execution_phase") == "human_run" and row.get("status") == "passed"
    ]
    if status_rows:
        status = status_rows[0]
        derived = {
            "session_count": len(instance_rows),
            "participant_count": len(participant_ids - {""}),
            "authorized_human_run_envelope_count": len(authorized_human_envelopes),
            "passed_human_run_preflight_count": len(passed_human_preflights),
        }
        for field, value in derived.items():
            if status.get(field) != str(value):
                errors.append(f"program status {field}={status.get(field)!r}, derived {value}")
        if status.get("program_id") != "D10-HUMAN-SESSION-CHAIN":
            errors.append("program status ID drift")
        if status.get("status") == "not_run":
            if any(derived.values()):
                errors.append("not_run program has Session/participant/authorization instances")
            if status.get("human_evidence_claim") != "none" or status.get("user_adjudication_status") != "none":
                errors.append("not_run program overclaims evidence or user adjudication")
            for row in context["evidence_rows"]:
                if row.get("participant_count") != "0" or row.get("human_result") != "not_run" or row.get("user_acceptance") != "none":
                    errors.append(f"not_run program conflicts with evidence row {row.get('evidence_id')}")
        elif status.get("status") not in {"authorized", "running", "evidence_ready", "closed"}:
            errors.append("invalid human playtest program status")

    try:
        contract_text = CONTRACT_DOC_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read human Session contract doc: {exc}")
    else:
        required_markers = (
            "zero_participant / zero_session / not_run / no_human_run_authorization",
            "七项AND",
            "H0",
            "H4",
            "right_to_withdraw_acknowledged",
            "evidence_only_no_user_acceptance",
            "0 participant / 0 session / not_run",
        )
        for marker in required_markers:
            if marker not in contract_text:
                errors.append(f"human Session contract doc missing marker {marker!r}")

    stats: dict[str, int | str] = {
        "schema_fields": len(schema_rows),
        "crosswalk_rows": len(crosswalk_rows),
        "hint_levels": len(hint_rows),
        "nonauto_cases": len(nonauto),
        "evidence_rows": len(context["evidence_rows"]),
        "participants": len(participant_ids - {""}),
        "sessions": len(instance_rows),
        "authorized_human_envelopes": len(authorized_human_envelopes),
        "passed_human_preflights": len(passed_human_preflights),
        "program_status": status_rows[0].get("status", "missing") if status_rows else "missing",
    }
    return errors, stats


def file_pair(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return f"{path.relative_to(PACKAGE).as_posix()}={digest}"


def synthetic_fixture(context: dict[str, object]) -> tuple[dict[str, str], dict[str, object]]:
    digest_a = "a" * 64
    digest_b = "b" * 64
    digest_c = "c" * 64
    pair = file_pair(PROTOTYPE_PATH)
    row = {field: "none" for field in EXPECTED_FIELDS}
    row.update({
        "schema_version": "candidate_human_playtest_session_v1",
        "session_instance_id": "HPS-SELFTEST-001",
        "test_run_id": "HTR-SELFTEST-P1A",
        "lifecycle_status": "completed",
        "prototype_id": "D04-P1-A",
        "case_ids": "HUM-P1-A-COLD",
        "acceptance_evidence_id": "EV-P1-A-COLD",
        "human_run_preflight_instance_id": "PXI-SELFTEST-P1A-HUMAN",
        "preflight_payload_sha256": digest_a,
        "execution_envelope_id": "E-SELFTEST-P1A-HUMAN",
        "authorization_subject_sha256": digest_b,
        "envelope_authorization_receipt_instance_id": "EAR-SELFTEST-P1A-HUMAN",
        "envelope_authorization_receipt_sha256": digest_c,
        "participant_cohort_id": "COHORT-P1-COLD-SELFTEST",
        "facilitator_role_id": "QA_LEAD",
        "observer_role_ids": "LEAD_DESIGNER",
        "started_at": "2026-08-11T10:00:00+08:00",
        "ended_at": "2026-08-11T10:40:00+08:00",
        "asset_authorization_state": "candidate_only",
        "build_id": "BUILD-P1A-SELFTEST",
        "build_manifest_path_and_sha256": pair,
        "content_manifest_id": "CONTENT-P1-SELFTEST",
        "content_manifest_path_and_sha256": pair,
        "ruleset_version": "RULES-P1-SELFTEST",
        "ruleset_path_and_sha256": pair,
        "map_or_scene_version": "MAP-P1-SELFTEST",
        "map_or_scene_path_and_sha256": pair,
        "tutorial_version": "TUTORIAL-P1-SELFTEST",
        "tutorial_path_and_sha256": pair,
        "ui_version": "UI-P1-SELFTEST",
        "ui_path_and_sha256": pair,
        "source_snapshot_manifest_path_and_sha256": pair,
        "case_snapshot_path_and_sha256": pair,
        "facilitator_script_version": "FACILITATOR-V1",
        "facilitator_script_path_and_sha256": pair,
        "telemetry_schema_version": "TEL-V1",
        "telemetry_schema_path_and_sha256": pair,
        "privacy_consent_snapshot_path_and_sha256": pair,
        "known_issues_snapshot_path_and_sha256": pair,
        "participant_pseudonym_id": "PT-SELFTEST-001",
        "participant_profile": "srpg_familiar;target_player",
        "first_contact_class": "cold",
        "prior_exposure_tokens": "none",
        "first_exposure_eligibility": "pass",
        "blind_variant_label": "TS-HARBOR",
        "variant_order": "single",
        "device_and_accessibility_profile": "keyboard_mouse;scale_100",
        "accommodation_ref_and_sha256": "none",
        "consent_record_ref_and_sha256": f"secure://consent/PT-SELFTEST-001={digest_a}",
        "consent_scope_tokens": "screen;input;telemetry;voice;anonymous_quote",
        "consent_captured_at": "2026-08-11T09:55:00+08:00",
        "right_to_withdraw_acknowledged": "true",
        "retention_delete_at": "2026-09-10T10:40:00+08:00",
        "privacy_access_role_ids": "QA_LEAD;LEAD_DESIGNER",
        "contact_data_separation_result": "pass",
        "compensation_state": "fulfilled",
        "deletion_request_state": "none",
        "sensitive_data_event_ref": "none",
        "hint_event_log_ref_and_sha256": "none",
        "maximum_hint_level": "H0",
        "hint_count": "0",
        "facilitator_rescue_count": "0",
        "strategy_hint_count": "0",
        "hint_contamination_result": "none",
        "safety_or_withdrawal_interventions": "none",
        "completion_state": "clear",
        "solution_family": "route_flank_body_block",
        "task_result_ref_and_sha256": pair,
        "behavior_log_ref_and_sha256": pair,
        "input_log_ref_and_sha256": pair,
        "telemetry_log_ref_and_sha256": pair,
        "state_hash_report_ref_and_sha256": pair,
        "video_ref_and_sha256": pair,
        "audio_ref_and_sha256": pair,
        "retell_transcript_ref_and_sha256": pair,
        "observer_notes_ref_and_sha256": pair,
        "preference_reason_ref_and_sha256": pair,
        "planning_time_median_seconds": "120",
        "input_error_count": "1",
        "causal_items_correct": "3",
        "transfer_result": "pass",
        "free_retell_score": "4",
        "body_score": "6",
        "agency_score": "6",
        "replay_intent": "yes",
        "blind_preference_token": "TS-HARBOR",
        "fatigue_score": "2",
        "discomfort_level": "none",
        "participant_exit_state": "completed",
        "withdrawal_reason_category": "none",
        "adverse_event_ref_and_sha256": "none",
        "artifact_integrity_result": "pass",
        "frozen_binding_result": "pass",
        "authorization_binding_result": "pass",
        "privacy_compliance_result": "pass",
        "first_exposure_result": "pass",
        "evidence_validity": "valid",
        "metric_exclusion_ids": "none",
        "invalid_reason_codes": "none",
        "claim_scope": "prototype=D04-P1-A;build=BUILD-P1A-SELFTEST;rules=RULES-P1-SELFTEST;map=MAP-P1-SELFTEST;case=HUM-P1-A-COLD",
        "claim_boundary": "evidence_only_no_user_acceptance",
        "aggregation_batch_id": "HAB-P1A-SELFTEST",
        "recorded_by": "QA_LEAD",
        "recorded_at": "2026-08-11T10:45:00+08:00",
        "reviewed_by": "LEAD_DESIGNER",
        "reviewed_at": "2026-08-11T11:00:00+08:00",
        "supersedes_session_instance_id": "none",
        "invalidation_reason": "none",
        "user_adjudication_state": "not_submitted",
        "user_adjudication_receipt_ref_and_sha256": "none",
        "user_adjudication_scope": "none",
    })
    row["session_payload_sha256"] = canonical_session_hash(row)

    synthetic = copy.deepcopy(context)
    synthetic["preflights"] = {
        "PXI-SELFTEST-P1A-HUMAN": {
            "preflight_instance_id": "PXI-SELFTEST-P1A-HUMAN",
            "execution_phase": "human_run",
            "status": "passed",
            "prototype_id": "D04-P1-A",
            "execution_envelope_id": "E-SELFTEST-P1A-HUMAN",
            "envelope_authorization_subject_sha256": digest_b,
            "envelope_authorization_receipt_instance_id": "EAR-SELFTEST-P1A-HUMAN",
            "envelope_authorization_receipt_sha256": digest_c,
            "build_id": "BUILD-P1A-SELFTEST",
            "test_case_ids": "HUM-P1-A-COLD",
            "preflight_payload_sha256": digest_a,
        }
    }
    synthetic["envelopes"] = {
        "E-SELFTEST-P1A-HUMAN": {
            "envelope_id": "E-SELFTEST-P1A-HUMAN",
            "envelope_phase": "human_run",
            "status": "authorized",
            "authorization_subject_sha256": digest_b,
            "envelope_authorization_receipt_instance_id": "EAR-SELFTEST-P1A-HUMAN",
            "envelope_authorization_receipt_sha256": digest_c,
            "authorized_prototype_ids": "D04-P1-A",
            "authorized_action_codes": "prepare_human;recruit;collect_data",
            "participant_cap": "6",
            "effective_at": "2026-08-11T00:00:00+08:00",
            "expires_at": "2026-08-12T00:00:00+08:00",
        }
    }
    synthetic["receipts"] = {
        "EAR-SELFTEST-P1A-HUMAN": {
            "envelope_receipt_instance_id": "EAR-SELFTEST-P1A-HUMAN",
            "envelope_id": "E-SELFTEST-P1A-HUMAN",
            "authorization_subject_sha256": digest_b,
            "receipt_artifact_sha256": digest_c,
            "status": "accepted",
        }
    }
    return row, synthetic


def run_self_test() -> tuple[bool, str]:
    base_errors: list[str] = []
    context = load_context(base_errors)
    if base_errors:
        return False, "cannot load package context: " + "; ".join(base_errors[:5])
    row, synthetic = synthetic_fixture(context)
    baseline_errors: list[str] = []
    validate_instance(row, errors=baseline_errors, **{
        key: synthetic[key]
        for key in ("prototypes", "cases", "evidence", "preflights", "envelopes", "receipts", "roles")
    })
    if baseline_errors:
        return False, "synthetic valid fixture rejected: " + "; ".join(baseline_errors[:8])

    Fault = tuple[str, Callable[[dict[str, str], dict[str, object]], None], bool]

    def set_row(field: str, value: str) -> Callable[[dict[str, str], dict[str, object]], None]:
        return lambda candidate, _: candidate.__setitem__(field, value)

    def mutate_preflight(field: str, value: str) -> Callable[[dict[str, str], dict[str, object]], None]:
        return lambda _, ctx: ctx["preflights"]["PXI-SELFTEST-P1A-HUMAN"].__setitem__(field, value)

    def mutate_envelope(field: str, value: str) -> Callable[[dict[str, str], dict[str, object]], None]:
        return lambda _, ctx: ctx["envelopes"]["E-SELFTEST-P1A-HUMAN"].__setitem__(field, value)

    faults: list[Fault] = [
        ("missing_build", set_row("build_id", ""), True),
        ("automated_case", set_row("case_ids", "AUTO-P1-DETERMINISM"), True),
        ("wrong_prototype", set_row("prototype_id", "P-EX1"), True),
        ("unknown_evidence", set_row("acceptance_evidence_id", "EV-NOT-THERE"), True),
        ("preflight_not_passed", mutate_preflight("status", "ready"), True),
        ("preflight_wrong_build", mutate_preflight("build_id", "OTHER-BUILD"), True),
        ("envelope_wrong_phase", mutate_envelope("envelope_phase", "implementation"), True),
        ("envelope_not_authorized", mutate_envelope("status", "draft"), True),
        ("envelope_no_collect", mutate_envelope("authorized_action_codes", "prepare_human"), True),
        ("subject_hash_mismatch", set_row("authorization_subject_sha256", "d" * 64), True),
        ("cold_prior_exposure", set_row("prior_exposure_tokens", "watched_video"), True),
        ("broken_blind_label", set_row("blind_variant_label", "A"), True),
        ("bad_participant_id", set_row("participant_pseudonym_id", "player@example.com"), True),
        ("withdraw_not_acknowledged", set_row("right_to_withdraw_acknowledged", "false"), True),
        ("missing_consent_record", set_row("consent_record_ref_and_sha256", "none"), True),
        ("contact_data_not_separated", set_row("contact_data_separation_result", "fail"), True),
        ("video_without_consent", set_row("consent_scope_tokens", "input;telemetry;voice"), True),
        ("H0_with_hint", lambda candidate, _: (candidate.__setitem__("hint_count", "1"), candidate.__setitem__("facilitator_rescue_count", "1")), True),
        ("hint_without_log", lambda candidate, _: (candidate.__setitem__("maximum_hint_level", "H2"), candidate.__setitem__("hint_count", "1"), candidate.__setitem__("facilitator_rescue_count", "1")), True),
        ("strategy_hint_still_valid", lambda candidate, _: (candidate.__setitem__("maximum_hint_level", "H4"), candidate.__setitem__("hint_count", "1"), candidate.__setitem__("strategy_hint_count", "1"), candidate.__setitem__("hint_event_log_ref_and_sha256", file_pair(HINT_PATH))), True),
        ("withdrawal_counted_valid", lambda candidate, _: (candidate.__setitem__("participant_exit_state", "withdrew"), candidate.__setitem__("completion_state", "withdraw")), True),
        ("material_discomfort_no_event", set_row("discomfort_level", "severe"), True),
        ("valid_with_failed_privacy", set_row("privacy_compliance_result", "fail"), True),
        ("overclaim_boundary", set_row("claim_boundary", "gameplay_approved"), True),
        ("approved_without_user_receipt", set_row("user_adjudication_state", "approved_for_bounded_migration"), True),
        ("same_recorder_reviewer", set_row("reviewed_by", "QA_LEAD"), True),
        ("consent_after_start", set_row("consent_captured_at", "2026-08-11T10:05:00+08:00"), True),
        ("outside_envelope_window", mutate_envelope("expires_at", "2026-08-11T09:00:00+08:00"), True),
        ("payload_hash_tamper", set_row("free_retell_score", "5"), False),
    ]

    rejected = 0
    failures: list[str] = []
    for name, mutate, rehash in faults:
        candidate = copy.deepcopy(row)
        candidate_context = copy.deepcopy(synthetic)
        mutate(candidate, candidate_context)
        if rehash:
            candidate["session_payload_sha256"] = canonical_session_hash(candidate)
        fault_errors: list[str] = []
        validate_instance(candidate, errors=fault_errors, **{
            key: candidate_context[key]
            for key in ("prototypes", "cases", "evidence", "preflights", "envelopes", "receipts", "roles")
        })
        if fault_errors:
            rejected += 1
        else:
            failures.append(name)
    if failures:
        return False, f"accepted injected faults: {', '.join(failures)}"
    return True, f"rejected={rejected}/{len(faults)} injected faults"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run in-memory fault-injection tests")
    args = parser.parse_args()

    if args.self_test:
        ok, message = run_self_test()
        if ok:
            print(f"D10 human Session self-test PASS: {message}")
            return 0
        print(f"D10 human Session self-test FAIL: {message}")
        return 1

    errors, stats = validate_package()
    if errors:
        print("D10 human Session contract FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "D10 human Session contract PASS: "
        f"{stats['schema_fields']} schema fields / "
        f"{stats['crosswalk_rows']} result crosswalks / "
        f"{stats['hint_levels']} hint levels / "
        f"{stats['nonauto_cases']} non-automated Cases / "
        f"{stats['evidence_rows']} evidence rows / "
        f"{stats['participants']} participants / "
        f"{stats['sessions']} Sessions / "
        f"{stats['authorized_human_envelopes']} authorized human_run envelopes / "
        f"{stats['passed_human_preflights']} passed human_run preflights / "
        f"status={stats['program_status']}; no Build/M5/M6/user acceptance claim"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
