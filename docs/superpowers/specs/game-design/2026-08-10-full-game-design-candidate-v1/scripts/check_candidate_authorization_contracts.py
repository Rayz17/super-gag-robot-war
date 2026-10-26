#!/usr/bin/env python3
"""Fail-closed validation for Candidate decisions and execution authority.

Product-direction receipts, exact-envelope authorization receipts, scoped Gate
instances, budget-pool state, and execution preflights are distinct artifacts.
No status label or generic definition may substitute for one of those instances.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
DATA = PACKAGE / "data"

DECISION_PATH = DATA / "user-game-design-decisions.tsv"
DECISION_SET_PATH = DATA / "decision-receipt-sets.tsv"
DECISION_REQUIREMENT_PATH = DATA / "decision-receipt-requirements.tsv"
DECISION_RECEIPT_SCHEMA_PATH = DATA / "decision-receipt-instance-schema.tsv"
DECISION_RECEIPT_INSTANCE_PATH = DATA / "decision-receipt-instances.tsv"
ENVELOPE_SCHEMA_PATH = DATA / "candidate-test-execution-envelope-schema.tsv"
ENVELOPE_INSTANCE_PATH = DATA / "candidate-test-execution-envelopes.tsv"
ENVELOPE_RECEIPT_SCHEMA_PATH = DATA / "execution-envelope-authorization-receipt-schema.tsv"
ENVELOPE_RECEIPT_INSTANCE_PATH = DATA / "execution-envelope-authorization-receipts.tsv"
BUDGET_POOL_SCHEMA_PATH = DATA / "candidate-test-budget-pool-schema.tsv"
BUDGET_POOL_INSTANCE_PATH = DATA / "candidate-test-budget-pools.tsv"
PREFLIGHT_SCHEMA_PATH = DATA / "prototype-execution-preflight-schema.tsv"
PREFLIGHT_REQUIREMENT_PATH = DATA / "prototype-execution-preflight-requirements.tsv"
PREFLIGHT_INSTANCE_PATH = DATA / "prototype-execution-preflight-instances.tsv"
PROTOTYPE_PATH = DATA / "prototype-test-registry.tsv"
GATE_PATH = DATA / "game-design-gate-registry.tsv"
GATE_INSTANCE_SCHEMA_PATH = DATA / "game-design-gate-instance-schema.tsv"
GATE_INSTANCE_PATH = DATA / "candidate-game-design-gate-instances.tsv"
TIME_SYSTEM_PATH = DATA / "time-system-neutrality-contract.tsv"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ENVELOPE_CANONICALIZATION_VERSION = "candidate_envelope_subject_v1"
POOL_CANONICALIZATION_VERSION = "candidate_budget_pool_subject_v1"

# Authorization-event and runtime-ledger fields are not part of the immutable
# envelope scope.  All scope, resource, path, prototype and pool-cap fields are.
ENVELOPE_SUBJECT_EXCLUDED_FIELDS = {
    "authorization_subject_sha256",
    "envelope_authorization_receipt_instance_id",
    "envelope_authorization_receipt_path",
    "envelope_authorization_receipt_sha256",
    "envelope_authorization_record_locator",
    "authorized_by_user_ref",
    "authorized_at",
    "shared_budget_pool_ledger_sha256",
    "shared_budget_pool_preflight_result",
    "result_evidence_ids",
    "closed_at",
    "invalidation_reason",
}

POOL_SUBJECT_FIELDS = (
    "budget_pool_schema_version",
    "shared_budget_pool_id",
    "shared_budget_program_scope_key",
    "pool_subject_canonicalization_version",
    "effective_at",
    "expires_at",
    "cap_calendar_days",
    "cap_person_hours",
    "cap_external_cash",
)


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    if not raw_lines:
        raise ValueError(f"empty TSV: {path}")
    width = len(raw_lines[0].split("\t"))
    for line_number, line in enumerate(raw_lines, 1):
        actual = len(line.split("\t"))
        if actual != width:
            raise ValueError(
                f"{path}: line {line_number} has {actual} fields; expected {width}"
            )
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def keyed(
    rows: list[dict[str, str]], field: str, audit: Audit, label: str
) -> dict[str, dict[str, str]]:
    values = [row.get(field, "") for row in rows]
    audit.require(all(values), f"{label}: empty {field}")
    duplicates = [value for value, count in Counter(values).items() if value and count > 1]
    audit.require(not duplicates, f"{label}: duplicate {field}: {sorted(duplicates)}")
    return {row[field]: row for row in rows if row.get(field)}


def split_refs(value: str) -> list[str]:
    return [item for item in value.split(";") if item and item != "none"]


def check_schema_registry_pair(
    audit: Audit, schema_path: Path, registry_path: Path, label: str
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    _, schema_rows = read_tsv(schema_path)
    registry_fields, registry_rows = read_tsv(registry_path)
    schema_fields = [row["field_name"] for row in schema_rows]
    audit.require(
        registry_fields == schema_fields,
        f"{label}: instance registry header differs from schema order",
    )
    audit.require(
        len(schema_fields) == len(set(schema_fields)),
        f"{label}: duplicate schema field names",
    )
    return schema_rows, registry_rows


def hash_json(payload: dict[str, str]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def canonical_envelope_subject(row: dict[str, str]) -> str:
    payload = {
        key: value
        for key, value in row.items()
        if key not in ENVELOPE_SUBJECT_EXCLUDED_FIELDS
    }
    payload["status"] = "draft"
    return hash_json(payload)


def canonical_budget_pool_subject(row: dict[str, str]) -> str:
    return hash_json({field: row.get(field, "") for field in POOL_SUBJECT_FIELDS})


def canonical_preflight_payload(row: dict[str, str]) -> str:
    payload = {key: value for key, value in row.items() if key != "preflight_payload_sha256"}
    payload["status"] = "ready"
    return hash_json(payload)


def decimal_value(value: str) -> Decimal | None:
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def parse_caps(value: str) -> dict[str, str]:
    if value in {"", "none", "not_applicable", "separate_user_approved_human_caps", "new_user_approved_pool_caps"}:
        return {}
    result: dict[str, str] = {}
    for item in value.split(","):
        if "=" not in item:
            return {}
        key, item_value = item.split("=", 1)
        result[key] = item_value
    return result


def parse_hash_bindings(value: str) -> dict[str, str] | None:
    bindings: dict[str, str] = {}
    for item in split_refs(value):
        if "=" not in item:
            return None
        subject, digest = item.rsplit("=", 1)
        if not subject or not SHA256_RE.fullmatch(digest):
            return None
        if subject in bindings:
            return None
        bindings[subject] = digest
    return bindings


def validate_hash_bindings(value: str, required_ids: list[str]) -> bool:
    if not required_ids:
        return value == "none"
    bindings = parse_hash_bindings(value)
    return bindings is not None and set(bindings) == set(required_ids)


def parse_outcomes(value: str) -> dict[str, str] | None:
    if value == "none":
        return {}
    outcomes: dict[str, str] = {}
    for item in split_refs(value):
        if "=" not in item:
            return None
        key, token = item.split("=", 1)
        if not key or not token or key in outcomes:
            return None
        outcomes[key] = token
    return outcomes


def validate_decision_receipt_row(
    row: dict[str, str],
    sets: dict[str, dict[str, str]],
    requirements: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    receipt_id = row.get("receipt_instance_id", "<missing>")
    template = sets.get(row.get("receipt_set_template_id", ""))
    if not template:
        return [f"{receipt_id}: unknown decision receipt set template"]
    if row.get("decision_id") != template.get("decision_id"):
        errors.append(f"{receipt_id}: decision differs from receipt set template")
    if row.get("decision_phase") != template.get("phase"):
        errors.append(f"{receipt_id}: phase differs from receipt set template")
    expected_requirements = set(split_refs(template.get("requirement_ids", "")))
    actual_requirements = set(split_refs(row.get("requirement_ids", "")))
    if actual_requirements != expected_requirements:
        errors.append(f"{receipt_id}: requirement set differs from template")
    for requirement_id in actual_requirements:
        requirement = requirements.get(requirement_id)
        if not requirement:
            errors.append(f"{receipt_id}: unknown requirement {requirement_id}")
        elif (
            requirement.get("decision_id") != row.get("decision_id")
            or requirement.get("phase") != row.get("decision_phase")
        ):
            errors.append(f"{receipt_id}: requirement decision/phase mismatch: {requirement_id}")

    if row.get("status") == "accepted":
        if row.get("requirement_result") != "all_required_accepted":
            errors.append(f"{receipt_id}: accepted receipt is not all-required accepted")
        if row.get("selected_option_token") in {"", "none", "DEFER", "REJECT"}:
            errors.append(f"{receipt_id}: accepted receipt lacks an affirmative option token")
        for field in (
            "decision_spec_path",
            "decision_record_locator",
            "accepted_clause_ids",
            "explicit_non_authorization_codes",
            "prerequisite_evidence_ids_and_sha256",
            "user_message_ref",
            "receipt_record_locator",
            "issued_by_user_ref",
            "issued_at",
            "recorded_by",
            "receipt_artifact_path",
        ):
            if row.get(field) in {"", "none"}:
                errors.append(f"{receipt_id}: accepted receipt missing {field}")
        for field in (
            "decision_spec_sha256",
            "user_message_sha256",
            "receipt_artifact_sha256",
        ):
            if not SHA256_RE.fullmatch(row.get(field, "")):
                errors.append(f"{receipt_id}: invalid {field}")
        for requirement_id in actual_requirements:
            requirement = requirements.get(requirement_id, {})
            if (
                requirement.get("requirement_status") != "accepted"
                or requirement.get("receipt_path") in {"", "none"}
                or not SHA256_RE.fullmatch(requirement.get("receipt_sha256", ""))
            ):
                errors.append(f"{receipt_id}: requirement lacks accepted evidence: {requirement_id}")
    return errors


def validate_envelope_receipt_row(row: dict[str, str]) -> list[str]:
    errors: list[str] = []
    receipt_id = row.get("envelope_receipt_instance_id", "<missing>")
    if row.get("status") == "accepted":
        if row.get("choice_token") != "AUTHORIZE_EXACT_ENVELOPE":
            errors.append(f"{receipt_id}: accepted envelope receipt is not exact authorization")
        if not SHA256_RE.fullmatch(row.get("authorization_subject_sha256", "")):
            errors.append(f"{receipt_id}: invalid authorization subject SHA-256")
        for field in (
            "envelope_id",
            "envelope_schema_version",
            "envelope_draft_path",
            "user_message_ref",
            "record_locator",
            "issued_by_user_ref",
            "issued_at",
            "recorded_by",
            "receipt_artifact_path",
        ):
            if row.get(field) in {"", "none"}:
                errors.append(f"{receipt_id}: accepted envelope receipt missing {field}")
        for field in (
            "envelope_draft_sha256",
            "user_message_sha256",
            "receipt_artifact_sha256",
        ):
            if not SHA256_RE.fullmatch(row.get(field, "")):
                errors.append(f"{receipt_id}: invalid {field}")
    return errors


def validate_budget_pool_row(
    row: dict[str, str],
    envelopes: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    pool_id = row.get("shared_budget_pool_id", "<missing>")
    if row.get("pool_subject_canonicalization_version") != POOL_CANONICALIZATION_VERSION:
        errors.append(f"{pool_id}: unsupported pool canonicalization version")
    if row.get("pool_subject_sha256") != canonical_budget_pool_subject(row):
        errors.append(f"{pool_id}: budget pool subject hash mismatch")

    numeric_fields = (
        "cap_calendar_days",
        "cap_person_hours",
        "cap_external_cash",
        "consumed_calendar_span_days",
        "consumed_person_hours",
        "consumed_external_cash",
        "remaining_calendar_days",
        "remaining_person_hours",
        "remaining_external_cash",
    )
    values = {field: decimal_value(row.get(field, "")) for field in numeric_fields}
    for field, value in values.items():
        if value is None or value < 0:
            errors.append(f"{pool_id}: invalid nonnegative number in {field}")
    for cap_field, used_field, remaining_field in (
        ("cap_calendar_days", "consumed_calendar_span_days", "remaining_calendar_days"),
        ("cap_person_hours", "consumed_person_hours", "remaining_person_hours"),
        ("cap_external_cash", "consumed_external_cash", "remaining_external_cash"),
    ):
        cap, used, remaining = values[cap_field], values[used_field], values[remaining_field]
        if cap is not None and used is not None and remaining is not None:
            if used > cap or remaining != cap - used:
                errors.append(f"{pool_id}: consumed/remaining values exceed or differ from {cap_field}")

    member_ids = split_refs(row.get("member_envelope_ids", ""))
    member_subjects = split_refs(row.get("member_envelope_subject_sha256s", ""))
    member_receipts = split_refs(row.get("member_envelope_receipt_instance_ids", ""))
    if not (len(member_ids) == len(member_subjects) == len(member_receipts)):
        errors.append(f"{pool_id}: member envelope/subject/receipt cardinality mismatch")
    if row.get("status") == "authorized":
        if row.get("cap_and_overlap_result") != "pass":
            errors.append(f"{pool_id}: authorized pool cap/overlap check is not pass")
        if not SHA256_RE.fullmatch(row.get("ledger_sha256", "")):
            errors.append(f"{pool_id}: authorized pool ledger SHA-256 is invalid")
        for index, envelope_id in enumerate(member_ids):
            envelope = envelopes.get(envelope_id)
            if not envelope or envelope.get("status") != "authorized":
                errors.append(f"{pool_id}: member envelope absent or not authorized: {envelope_id}")
                continue
            if member_subjects[index] != envelope.get("authorization_subject_sha256"):
                errors.append(f"{pool_id}: member subject mismatch: {envelope_id}")
            if member_receipts[index] != envelope.get("envelope_authorization_receipt_instance_id"):
                errors.append(f"{pool_id}: member receipt mismatch: {envelope_id}")
    return errors


def validate_envelope_row(
    row: dict[str, str],
    envelope_receipts: dict[str, dict[str, str]],
    decision_receipts: dict[str, dict[str, str]],
    requirements: dict[str, dict[str, str]],
    budget_pools: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    envelope_id = row.get("envelope_id", "<missing>")
    if row.get("authorization_subject_canonicalization_version") != ENVELOPE_CANONICALIZATION_VERSION:
        errors.append(f"{envelope_id}: unsupported canonicalization version")
    expected_subject = canonical_envelope_subject(row)
    if row.get("authorization_subject_sha256") != expected_subject:
        errors.append(f"{envelope_id}: authorization subject hash mismatch")
    if row.get("extension_policy") != "new_envelope_new_subject_hash_new_receipt":
        errors.append(f"{envelope_id}: extension policy is not fail-closed")
    if row.get("overlap_check_result") != "pass":
        errors.append(f"{envelope_id}: overlap check is not pass")

    if row.get("status") == "authorized":
        decision_instance_ids = split_refs(row.get("receipt_set_instance_ids", ""))
        if not decision_instance_ids:
            errors.append(f"{envelope_id}: authorized envelope lacks decision receipt instances")
        for receipt_id in decision_instance_ids:
            receipt = decision_receipts.get(receipt_id)
            if not receipt or receipt.get("status") != "accepted":
                errors.append(f"{envelope_id}: decision receipt absent or not accepted: {receipt_id}")
        resolved_receipts = [decision_receipts[value] for value in decision_instance_ids if value in decision_receipts]
        resolved_decisions = {receipt.get("decision_id", "") for receipt in resolved_receipts}
        resolved_requirements: set[str] = set()
        for receipt in resolved_receipts:
            resolved_requirements.update(split_refs(receipt.get("requirement_ids", "")))
        if set(split_refs(row.get("authorizing_decision_ids", ""))) != resolved_decisions:
            errors.append(f"{envelope_id}: authorizing decision IDs differ from receipt instances")
        if set(split_refs(row.get("requirement_ids", ""))) != resolved_requirements:
            errors.append(f"{envelope_id}: requirement IDs differ from receipt instances")
        expected_requirement_bindings = {
            requirements[requirement_id]["receipt_path"]: requirements[requirement_id]["receipt_sha256"]
            for requirement_id in resolved_requirements
            if requirement_id in requirements
        }
        if parse_hash_bindings(row.get("receipt_paths_and_sha256", "")) != expected_requirement_bindings:
            errors.append(f"{envelope_id}: requirement receipt path/hash bindings mismatch")

        envelope_receipt_id = row.get("envelope_authorization_receipt_instance_id", "")
        receipt = envelope_receipts.get(envelope_receipt_id)
        if envelope_receipt_id in {"", "none"}:
            errors.append(f"{envelope_id}: missing independent envelope authorization receipt")
        if not receipt or receipt.get("status") != "accepted":
            errors.append(f"{envelope_id}: envelope receipt is absent or not accepted")
        elif (
            receipt.get("envelope_id") != envelope_id
            or receipt.get("authorization_subject_sha256") != expected_subject
            or receipt.get("envelope_schema_version") != row.get("envelope_schema_version")
            or receipt.get("choice_token") != "AUTHORIZE_EXACT_ENVELOPE"
            or receipt.get("receipt_artifact_path") != row.get("envelope_authorization_receipt_path")
            or receipt.get("receipt_artifact_sha256") != row.get("envelope_authorization_receipt_sha256")
        ):
            errors.append(f"{envelope_id}: envelope receipt does not bind exact subject/artifact")
        for field in (
            "envelope_authorization_receipt_path",
            "envelope_authorization_receipt_sha256",
            "envelope_authorization_record_locator",
            "authorized_by_user_ref",
            "authorized_at",
            "effective_at",
        ):
            if row.get(field) in {"", "none"}:
                errors.append(f"{envelope_id}: authorized envelope missing {field}")
        if not SHA256_RE.fullmatch(row.get("envelope_authorization_receipt_sha256", "")):
            errors.append(f"{envelope_id}: invalid envelope receipt SHA-256")

        for field in (
            "formal_asset_work_allowed",
            "current_runtime_write_allowed",
            "canon_reader_story_chain_write_allowed",
        ):
            if row.get(field) != "false":
                errors.append(f"{envelope_id}: Candidate envelope must keep {field}=false")
        if row.get("envelope_phase") == "implementation" and (
            row.get("external_recruitment_allowed") != "false"
            or row.get("participant_cap") != "0"
        ):
            errors.append(f"{envelope_id}: implementation envelope grants human-session authority")

        pool_id = row.get("shared_budget_pool_id", "")
        pool = budget_pools.get(pool_id)
        if not pool or pool.get("status") != "authorized":
            errors.append(f"{envelope_id}: shared budget pool absent or not authorized")
        else:
            cap_pairs = (
                ("shared_budget_pool_cap_calendar_days", "cap_calendar_days"),
                ("shared_budget_pool_cap_person_hours", "cap_person_hours"),
                ("shared_budget_pool_cap_external_cash", "cap_external_cash"),
            )
            if (
                row.get("shared_budget_program_scope_key") != pool.get("shared_budget_program_scope_key")
                or row.get("shared_budget_pool_subject_sha256") != pool.get("pool_subject_sha256")
                or any(row.get(left) != pool.get(right) for left, right in cap_pairs)
                or row.get("shared_budget_pool_ledger_path") != pool.get("ledger_path")
                or row.get("shared_budget_pool_ledger_sha256") != pool.get("ledger_sha256")
                or row.get("shared_budget_pool_preflight_result") != "pass"
            ):
                errors.append(f"{envelope_id}: shared budget pool binding/current-ledger mismatch")
            member_ids = split_refs(pool.get("member_envelope_ids", ""))
            if envelope_id not in member_ids:
                errors.append(f"{envelope_id}: envelope is not a member of its shared budget pool")
    return errors


def validate_scope_rule(rule: str, authorized_prototypes: set[str]) -> bool:
    for clause in split_refs(rule):
        if clause.startswith("must_equal_bundle:"):
            expected = set(clause.split(":", 1)[1].split(","))
            if authorized_prototypes != expected:
                return False
        elif clause.startswith("must_equal:"):
            target = clause.split(":", 1)[1]
            expected = set() if target == "none" else {target}
            if authorized_prototypes != expected:
                return False
        elif clause.startswith("must_not_include:"):
            forbidden = set(clause.split(":", 1)[1].split(","))
            if authorized_prototypes & forbidden:
                return False
        else:
            return False
    return True


def validate_contract_build_cap(rule: str, envelope_value: str) -> bool:
    if rule == "not_applicable":
        return envelope_value in {"", "none", "not_applicable"}
    if rule == "1_to_4_equal_shortlist_count_from_M5":
        value = decimal_value(envelope_value)
        return value is not None and value == value.to_integral_value() and 1 <= value <= 4
    return envelope_value == rule


def validate_gate_instance_row(
    row: dict[str, str],
    gate_definitions: dict[str, dict[str, str]],
    decision_receipts: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    gate_id = row.get("gate_instance_id", "<missing>")
    if row.get("gate_definition_id") not in gate_definitions:
        errors.append(f"{gate_id}: unknown Gate definition")
    if row.get("status") != "passed":
        return errors

    paths = split_refs(row.get("actual_input_paths", ""))
    hashes = split_refs(row.get("actual_input_sha256", ""))
    if not paths or len(paths) != len(hashes) or any(not SHA256_RE.fullmatch(value) for value in hashes):
        errors.append(f"{gate_id}: passed Gate lacks one-to-one input path/hash evidence")
    for field in ("file_existence_result", "hash_match_result", "zero_block_result"):
        if row.get(field) != "pass":
            errors.append(f"{gate_id}: passed Gate has {field}!=pass")
    for field in ("mime_dimension_result", "semantic_binding_result", "cross_phase_reuse_result"):
        if row.get(field) not in {"pass", "not_applicable"}:
            errors.append(f"{gate_id}: passed Gate has invalid {field}")
    if row.get("checker_entrypoints") in {"", "none"} or row.get("checker_versions") in {"", "none"}:
        errors.append(f"{gate_id}: passed Gate lacks checker entrypoint/version")

    authority_kind = row.get("receipt_authority_kind")
    receipt_instance_id = row.get("receipt_set_instance_id", "")
    if authority_kind == "decision":
        receipt = decision_receipts.get(receipt_instance_id)
        if not receipt or receipt.get("status") != "accepted":
            errors.append(f"{gate_id}: decision-authorized Gate lacks accepted receipt instance")
        elif (
            receipt.get("decision_id") != row.get("decision_id")
            or receipt.get("decision_phase") != row.get("decision_phase")
            or set(split_refs(receipt.get("requirement_ids", "")))
            != set(split_refs(row.get("requirement_ids", "")))
        ):
            errors.append(f"{gate_id}: Gate decision receipt binding mismatch")
    elif authority_kind == "gate_template":
        for field in ("gate_receipt_set_template_id", "receipt_set_instance_id", "receipt_paths", "receipt_sha256s"):
            if row.get(field) in {"", "none"}:
                errors.append(f"{gate_id}: gate-template authority missing {field}")
    elif authority_kind != "none":
        errors.append(f"{gate_id}: invalid receipt authority kind")
    return errors


def validate_preflight_row(
    row: dict[str, str],
    contracts: dict[str, dict[str, str]],
    gate_definition_ids: set[str],
    gate_instances: dict[str, dict[str, str]],
    decision_receipts: dict[str, dict[str, str]],
    envelopes: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    preflight_id = row.get("preflight_instance_id", "<missing>")
    contract = contracts.get(row.get("preflight_contract_id", ""))
    if not contract:
        return [f"{preflight_id}: unknown preflight contract"]
    if row.get("prototype_id") != contract.get("prototype_id"):
        errors.append(f"{preflight_id}: prototype differs from contract")
    if row.get("execution_phase") != contract.get("execution_phase"):
        errors.append(f"{preflight_id}: execution phase differs from contract")

    if row.get("status") in {"ready", "passed"}:
        receipt_ids = split_refs(row.get("decision_receipt_set_instance_ids", ""))
        receipts = [decision_receipts.get(value) for value in receipt_ids]
        if not receipts or any(item is None or item.get("status") != "accepted" for item in receipts):
            errors.append(f"{preflight_id}: missing accepted decision receipt instances")
        actual_templates = {
            item["receipt_set_template_id"] for item in receipts if item is not None
        }
        expected_templates = set(split_refs(contract.get("required_decision_receipt_set_templates", "")))
        if actual_templates != expected_templates:
            errors.append(f"{preflight_id}: decision receipt template set mismatch")
        expected_requirements = set(split_refs(contract.get("required_requirement_ids", "")))
        if set(split_refs(row.get("decision_requirement_ids", ""))) != expected_requirements:
            errors.append(f"{preflight_id}: decision requirement set mismatch")
        receipt_requirements: set[str] = set()
        for receipt in receipts:
            if receipt:
                receipt_requirements.update(split_refs(receipt.get("requirement_ids", "")))
        if receipt_requirements != expected_requirements:
            errors.append(f"{preflight_id}: receipt instances do not cover exact requirements")

        required_gate_definitions = set(split_refs(contract.get("required_scoped_gate_definitions", "")))
        actual_gate_ids = split_refs(row.get("scoped_gate_instance_ids", ""))
        actual_gate_definitions: set[str] = set()
        for gate_id in actual_gate_ids:
            if gate_id in gate_definition_ids:
                errors.append(f"{preflight_id}: gate definition used as gate instance")
            gate_instance = gate_instances.get(gate_id)
            if not gate_instance or gate_instance.get("status") != "passed":
                errors.append(f"{preflight_id}: Gate instance absent or not passed: {gate_id}")
            else:
                actual_gate_definitions.add(gate_instance.get("gate_definition_id", ""))
                if (
                    gate_instance.get("gate_definition_id") == "GATE-GD1"
                    and (
                        gate_instance.get("receipt_authority_kind") != "decision"
                        or gate_instance.get("receipt_set_instance_id") not in receipt_ids
                    )
                ):
                    errors.append(f"{preflight_id}: GD1 Gate is not bound to a preflight decision receipt")
        if actual_gate_definitions != required_gate_definitions:
            errors.append(f"{preflight_id}: scoped Gate definition coverage mismatch")
        if required_gate_definitions:
            if (
                row.get("gate_instance_status_snapshot_path") in {"", "none"}
                or not SHA256_RE.fullmatch(row.get("gate_instance_status_snapshot_sha256", ""))
            ):
                errors.append(f"{preflight_id}: missing Gate status snapshot path/hash")
        elif actual_gate_ids or row.get("gate_instance_status_snapshot_path") != "none" or row.get("gate_instance_status_snapshot_sha256") != "none":
            errors.append(f"{preflight_id}: Gate-free contract contains Gate instance/snapshot")

        required_evidence = split_refs(contract.get("required_upstream_evidence", ""))
        if not validate_hash_bindings(row.get("upstream_evidence_ids_and_sha256", ""), required_evidence):
            errors.append(f"{preflight_id}: upstream evidence ID/hash set mismatch")
        outcomes = parse_outcomes(row.get("upstream_outcomes", ""))
        if contract.get("prototype_id") == "D04-P2-CROSSOVER":
            if outcomes is None or set(outcomes) != {"TSN-P1-RESULT"} or outcomes.get("TSN-P1-RESULT") not in {
                "shortlist_two", "shortlist_three", "shortlist_four"
            }:
                errors.append(f"{preflight_id}: upstream outcome does not permit crossover")
        elif outcomes != {}:
            errors.append(f"{preflight_id}: contract carries an unrequired upstream outcome")
        expected_receipt_bindings = {
            item.get("receipt_artifact_path", ""): item.get("receipt_artifact_sha256", "")
            for item in receipts
            if item
        }
        if parse_hash_bindings(row.get("decision_receipt_paths_and_sha256", "")) != expected_receipt_bindings:
            errors.append(f"{preflight_id}: decision receipt path/hash bindings invalid")
        source_bindings = parse_hash_bindings(row.get("source_paths_and_sha256", ""))
        if not source_bindings:
            errors.append(f"{preflight_id}: source path/hash bindings invalid")

        phase = row.get("execution_phase")
        envelope_fields = (
            "execution_envelope_id",
            "envelope_authorization_subject_sha256",
            "envelope_authorization_receipt_instance_id",
            "envelope_authorization_receipt_sha256",
        )
        if phase == "analysis_only":
            if any(row.get(field) != "none" for field in envelope_fields):
                errors.append(f"{preflight_id}: analysis-only preflight carries execution authority")
            if any(row.get(field) != "none" for field in ("build_id", "test_case_ids", "privacy_and_consent_snapshot")):
                errors.append(f"{preflight_id}: analysis-only preflight carries Build/session fields")
        else:
            envelope_id = row.get("execution_envelope_id", "")
            required_envelope_id = contract.get("required_execution_envelope_id", "")
            if required_envelope_id.startswith("E-") and envelope_id != required_envelope_id:
                errors.append(f"{preflight_id}: exact required execution envelope ID mismatch")
            if required_envelope_id.startswith("new_separate") and envelope_id in {
                "E-R0-IMPLEMENT", "E-P1-ABCD-IMPLEMENT", "", "none"
            }:
                errors.append(f"{preflight_id}: separate execution envelope not provided")
            envelope = envelopes.get(envelope_id)
            if not envelope or envelope.get("status") != "authorized":
                errors.append(f"{preflight_id}: execution envelope absent or not authorized")
            else:
                if set(receipt_ids) != set(split_refs(envelope.get("receipt_set_instance_ids", ""))):
                    errors.append(f"{preflight_id}: preflight receipts differ from envelope receipts")
                if expected_requirements != set(split_refs(envelope.get("requirement_ids", ""))):
                    errors.append(f"{preflight_id}: preflight requirements differ from envelope requirements")
                if (
                    row.get("envelope_authorization_subject_sha256") != envelope.get("authorization_subject_sha256")
                    or row.get("envelope_authorization_receipt_instance_id") != envelope.get("envelope_authorization_receipt_instance_id")
                    or row.get("envelope_authorization_receipt_sha256") != envelope.get("envelope_authorization_receipt_sha256")
                ):
                    errors.append(f"{preflight_id}: exact envelope authorization binding mismatch")
                if phase != envelope.get("envelope_phase"):
                    errors.append(f"{preflight_id}: envelope phase mismatch")
                authorized_prototypes = set(split_refs(envelope.get("authorized_prototype_ids", "")))
                if not validate_scope_rule(contract.get("envelope_prototype_scope_rule", ""), authorized_prototypes):
                    errors.append(f"{preflight_id}: envelope prototype scope rule failed")
                if not validate_contract_build_cap(
                    contract.get("required_envelope_max_total_builds", ""),
                    envelope.get("max_total_builds", ""),
                ):
                    errors.append(f"{preflight_id}: envelope total-build cap mismatch")
                if contract.get("required_shared_budget_program_scope_key") != envelope.get("shared_budget_program_scope_key"):
                    errors.append(f"{preflight_id}: shared budget program scope mismatch")
                caps = parse_caps(contract.get("required_shared_budget_pool_caps", ""))
                if caps and (
                    envelope.get("shared_budget_pool_cap_calendar_days") != caps.get("calendar_days")
                    or envelope.get("shared_budget_pool_cap_person_hours") != caps.get("person_hours")
                    or envelope.get("shared_budget_pool_cap_external_cash") != caps.get("external_cash")
                ):
                    errors.append(f"{preflight_id}: shared budget pool caps mismatch")
                if envelope.get("shared_budget_pool_preflight_result") != "pass":
                    errors.append(f"{preflight_id}: shared budget pool preflight is not pass")
            if phase == "human_run":
                for field in ("build_id", "test_case_ids", "privacy_and_consent_snapshot"):
                    if row.get(field) in {"", "none"}:
                        errors.append(f"{preflight_id}: human preflight missing {field}")
            elif any(row.get(field) != "none" for field in ("build_id", "test_case_ids", "privacy_and_consent_snapshot")):
                errors.append(f"{preflight_id}: implementation preflight carries human-run fields")

        if row.get("forbidden_substitution_result") != "pass":
            errors.append(f"{preflight_id}: forbidden-substitution check not pass")
        if row.get("preflight_payload_sha256") != canonical_preflight_payload(row):
            errors.append(f"{preflight_id}: preflight payload hash mismatch")
    return errors


def make_fixture_pool(fields: list[str]) -> dict[str, str]:
    row = {field: "fixture" for field in fields}
    row.update(
        {
            "budget_pool_schema_version": "candidate_budget_pool_v1",
            "shared_budget_pool_id": "POOL-FI-STAGE0",
            "shared_budget_program_scope_key": "STAGE0_R0_P1",
            "status": "draft",
            "pool_subject_canonicalization_version": POOL_CANONICALIZATION_VERSION,
            "pool_subject_sha256": "pending",
            "effective_at": "2026-08-11T00:00:00+08:00",
            "expires_at": "2026-08-25T00:00:00+08:00",
            "cap_calendar_days": "14",
            "cap_person_hours": "80",
            "cap_external_cash": "0",
            "member_envelope_ids": "none",
            "member_envelope_subject_sha256s": "none",
            "member_envelope_receipt_instance_ids": "none",
            "ledger_path": "validation/fixture-budget-ledger.tsv",
            "ledger_sha256": "0" * 64,
            "consumed_calendar_span_days": "0",
            "consumed_person_hours": "0",
            "consumed_external_cash": "0",
            "remaining_calendar_days": "14",
            "remaining_person_hours": "80",
            "remaining_external_cash": "0",
            "last_updated_at": "2026-08-11T00:00:00+08:00",
            "cap_and_overlap_result": "pass",
        }
    )
    row["pool_subject_sha256"] = canonical_budget_pool_subject(row)
    return row


def make_fixture_envelope(fields: list[str], pool: dict[str, str]) -> dict[str, str]:
    row = {field: "fixture" for field in fields}
    row.update(
        {
            "envelope_schema_version": "candidate_execution_envelope_v2",
            "envelope_id": "ENV-FI-001",
            "envelope_phase": "implementation",
            "status": "draft",
            "authorization_subject_canonicalization_version": ENVELOPE_CANONICALIZATION_VERSION,
            "authorization_subject_sha256": "pending",
            "envelope_authorization_receipt_instance_id": "none",
            "envelope_authorization_receipt_path": "none",
            "envelope_authorization_receipt_sha256": "none",
            "envelope_authorization_record_locator": "none",
            "authorized_by_user_ref": "none",
            "authorized_at": "none",
            "effective_at": "2026-08-11T00:00:00+08:00",
            "expires_at": "2026-08-25T00:00:00+08:00",
            "receipt_set_instance_ids": "DRSI-FI-DEC11",
            "authorized_prototype_ids": "R0-TEST-KERNEL",
            "authorized_gate_instance_ids": "GI-FI-001",
            "authorized_action_codes": "create_source;build;run_machine",
            "max_total_builds": "1",
            "max_calendar_days": "14",
            "max_person_hours": "80",
            "max_external_cash_spend": "0",
            "formal_asset_work_allowed": "false",
            "current_runtime_write_allowed": "false",
            "canon_reader_story_chain_write_allowed": "false",
            "external_recruitment_allowed": "false",
            "participant_cap": "0",
            "exclusive_scope_key": "FI-R0",
            "shared_budget_program_scope_key": pool["shared_budget_program_scope_key"],
            "shared_budget_pool_id": pool["shared_budget_pool_id"],
            "shared_budget_pool_subject_sha256": pool["pool_subject_sha256"],
            "shared_budget_pool_cap_calendar_days": pool["cap_calendar_days"],
            "shared_budget_pool_cap_person_hours": pool["cap_person_hours"],
            "shared_budget_pool_cap_external_cash": pool["cap_external_cash"],
            "shared_budget_pool_ledger_path": pool["ledger_path"],
            "shared_budget_pool_ledger_sha256": pool["ledger_sha256"],
            "shared_budget_pool_preflight_result": "pass",
            "supersedes_envelope_id": "none",
            "overlap_check_result": "pass",
            "extension_policy": "new_envelope_new_subject_hash_new_receipt",
            "result_evidence_ids": "pending",
            "closed_at": "none",
            "invalidation_reason": "none",
        }
    )
    row["authorization_subject_sha256"] = canonical_envelope_subject(row)
    return row


def run_fault_injections(
    envelope_fields: list[str], pool_fields: list[str]
) -> tuple[int, list[str]]:
    failures: list[str] = []
    rejected = 0
    pool = make_fixture_pool(pool_fields)
    base = make_fixture_envelope(envelope_fields, pool)
    receipt = {
        "envelope_receipt_instance_id": "ERI-FI-001",
        "envelope_id": base["envelope_id"],
        "authorization_subject_sha256": base["authorization_subject_sha256"],
        "envelope_schema_version": base["envelope_schema_version"],
        "choice_token": "AUTHORIZE_EXACT_ENVELOPE",
        "receipt_artifact_path": "fixture-receipt.tsv",
        "receipt_artifact_sha256": "0" * 64,
        "status": "accepted",
    }
    decision_receipt = {
        "receipt_instance_id": "DRSI-FI-DEC11",
        "receipt_set_template_id": "DRS-DEC11-A",
        "requirement_ids": "DR-DEC11-A",
        "receipt_artifact_path": "fixture-decision.tsv",
        "status": "accepted",
    }

    mutated = copy.deepcopy(base)
    mutated["max_person_hours"] = "999"
    if canonical_envelope_subject(mutated) != base["authorization_subject_sha256"]:
        rejected += 1
    else:
        failures.append("FI-ENV-RESOURCE-DRIFT unexpectedly preserved subject hash")

    mutated = copy.deepcopy(base)
    mutated["writable_workspace_paths"] += ";docs/superpowers/specs/data/canon"
    if canonical_envelope_subject(mutated) != base["authorization_subject_sha256"]:
        rejected += 1
    else:
        failures.append("FI-ENV-WRITE-SCOPE-DRIFT unexpectedly preserved subject hash")

    pool_for_base = copy.deepcopy(pool)
    pool_for_base.update(
        {
            "status": "authorized",
            "member_envelope_ids": base["envelope_id"],
            "member_envelope_subject_sha256s": base["authorization_subject_sha256"],
            "member_envelope_receipt_instance_ids": "ERI-FI-001",
        }
    )
    mutated = copy.deepcopy(base)
    mutated["status"] = "authorized"
    errors = validate_envelope_row(
        mutated,
        {},
        {decision_receipt["receipt_instance_id"]: decision_receipt},
        {},
        {pool_for_base["shared_budget_pool_id"]: pool_for_base},
    )
    if any("missing independent envelope authorization receipt" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-ENV-SELF-AUTH was not rejected")

    mutated = copy.deepcopy(base)
    mutated.update(
        {
            "status": "authorized",
            "envelope_authorization_receipt_instance_id": "ERI-FI-001",
            "envelope_authorization_receipt_path": "fixture-receipt.tsv",
            "envelope_authorization_receipt_sha256": "0" * 64,
            "envelope_authorization_record_locator": "row:1",
            "authorized_by_user_ref": "USER",
            "authorized_at": "2026-08-10T00:00:00+08:00",
        }
    )
    wrong_receipt = dict(receipt)
    wrong_receipt["authorization_subject_sha256"] = "f" * 64
    errors = validate_envelope_row(
        mutated,
        {"ERI-FI-001": wrong_receipt},
        {decision_receipt["receipt_instance_id"]: decision_receipt},
        {},
        {pool_for_base["shared_budget_pool_id"]: pool_for_base},
    )
    if any("does not bind exact subject/artifact" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-ENV-CROSS-SUBJECT-RECEIPT was not rejected")

    preflight_contract = {
        "preflight_contract_id": "PX-FI",
        "prototype_id": "R0-TEST-KERNEL",
        "execution_phase": "implementation",
        "required_execution_envelope_id": "ENV-FI-001",
        "required_decision_receipt_set_templates": "DRS-DEC11-A",
        "required_requirement_ids": "DR-DEC11-A",
        "required_scoped_gate_definitions": "GATE-GD1",
        "required_upstream_evidence": "EVIDENCE-FI",
        "envelope_prototype_scope_rule": "must_equal:R0-TEST-KERNEL",
        "required_envelope_max_total_builds": "1",
        "required_shared_budget_program_scope_key": "STAGE0_R0_P1",
        "required_shared_budget_pool_caps": "calendar_days=14,person_hours=80,external_cash=0",
    }
    authorized_fixture = copy.deepcopy(base)
    authorized_fixture.update(
        {
            "status": "authorized",
            "envelope_authorization_receipt_instance_id": "ERI-FI-001",
            "envelope_authorization_receipt_path": "fixture-receipt.tsv",
            "envelope_authorization_receipt_sha256": "0" * 64,
        }
    )
    preflight = {
        "preflight_instance_id": "PFI-FI",
        "preflight_contract_id": "PX-FI",
        "prototype_id": "R0-TEST-KERNEL",
        "execution_phase": "implementation",
        "status": "passed",
        "decision_receipt_set_instance_ids": "DRSI-FI-DEC11",
        "decision_requirement_ids": "DR-DEC11-A",
        "decision_receipt_paths_and_sha256": "fixture-decision.tsv=" + "1" * 64,
        "scoped_gate_instance_ids": "GATE-GD1",
        "gate_instance_status_snapshot_path": "fixture-gate.tsv",
        "gate_instance_status_snapshot_sha256": "2" * 64,
        "upstream_evidence_ids_and_sha256": "EVIDENCE-FI=" + "3" * 64,
        "upstream_outcomes": "none",
        "execution_envelope_id": "ENV-FI-001",
        "envelope_authorization_subject_sha256": base["authorization_subject_sha256"],
        "envelope_authorization_receipt_instance_id": "ERI-FI-001",
        "envelope_authorization_receipt_sha256": "0" * 64,
        "source_paths_and_sha256": "fixture-source.tsv=" + "4" * 64,
        "build_id": "none",
        "test_case_ids": "none",
        "privacy_and_consent_snapshot": "none",
        "forbidden_substitution_result": "pass",
        "preflight_payload_sha256": "pending",
    }
    preflight["preflight_payload_sha256"] = canonical_preflight_payload(preflight)
    errors = validate_preflight_row(
        preflight,
        {"PX-FI": preflight_contract},
        {"GATE-GD1"},
        {},
        {decision_receipt["receipt_instance_id"]: decision_receipt},
        {authorized_fixture["envelope_id"]: authorized_fixture},
    )
    if any("gate definition used as gate instance" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-PREFLIGHT-GATE-DEFINITION was not rejected")

    mutated_preflight = copy.deepcopy(preflight)
    mutated_preflight["scoped_gate_instance_ids"] = "GI-FI-001"
    mutated_preflight["decision_receipt_set_instance_ids"] = "none"
    mutated_preflight["preflight_payload_sha256"] = canonical_preflight_payload(mutated_preflight)
    errors = validate_preflight_row(
        mutated_preflight,
        {"PX-FI": preflight_contract},
        {"GATE-GD1"},
        {"GI-FI-001": {"gate_definition_id": "GATE-GD1", "status": "passed"}},
        {},
        {authorized_fixture["envelope_id"]: authorized_fixture},
    )
    if any("missing accepted decision receipt instances" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-PREFLIGHT-DECISION-STATUS-SUBSTITUTE was not rejected")

    pool_a = make_fixture_pool(pool_fields)
    pool_a["status"] = "authorized"
    pool_b = copy.deepcopy(pool_a)
    pool_b["shared_budget_pool_id"] = "POOL-FI-STAGE0-B"
    pool_b["pool_subject_sha256"] = canonical_budget_pool_subject(pool_b)
    active_programs = [
        item["shared_budget_program_scope_key"] for item in (pool_a, pool_b)
        if item["status"] == "authorized"
    ]
    if any(count > 1 for count in Counter(active_programs).values()):
        rejected += 1
    else:
        failures.append("FI-POOL-DUPLICATE-ACTIVE-SCOPE was not rejected")

    overrun = make_fixture_pool(pool_fields)
    overrun.update(
        {
            "consumed_person_hours": "81",
            "remaining_person_hours": "0",
        }
    )
    errors = validate_budget_pool_row(overrun, {})
    if any("consumed/remaining values exceed" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-POOL-CAP-OVERRUN was not rejected")

    wrong_envelope_preflight = copy.deepcopy(preflight)
    wrong_envelope_preflight["execution_envelope_id"] = "E-R0-IMPLEMENT"
    wrong_envelope_preflight["preflight_payload_sha256"] = canonical_preflight_payload(wrong_envelope_preflight)
    p1_contract = dict(preflight_contract)
    p1_contract["required_execution_envelope_id"] = "E-P1-ABCD-IMPLEMENT"
    errors = validate_preflight_row(
        wrong_envelope_preflight,
        {"PX-FI": p1_contract},
        set(),
        {},
        {decision_receipt["receipt_instance_id"]: decision_receipt},
        {},
    )
    if any("exact required execution envelope ID mismatch" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-PREFLIGHT-R0-P1-ENVELOPE-REUSE was not rejected")

    analysis_contract = dict(preflight_contract)
    analysis_contract.update(
        {
            "execution_phase": "analysis_only",
            "required_execution_envelope_id": "none",
            "required_scoped_gate_definitions": "none",
            "envelope_prototype_scope_rule": "must_equal:none",
            "required_envelope_max_total_builds": "not_applicable",
            "required_shared_budget_program_scope_key": "none",
            "required_shared_budget_pool_caps": "not_applicable",
        }
    )
    analysis = copy.deepcopy(preflight)
    analysis["execution_phase"] = "analysis_only"
    analysis["scoped_gate_instance_ids"] = "none"
    analysis["gate_instance_status_snapshot_path"] = "none"
    analysis["gate_instance_status_snapshot_sha256"] = "none"
    analysis["preflight_payload_sha256"] = canonical_preflight_payload(analysis)
    errors = validate_preflight_row(
        analysis,
        {"PX-FI": analysis_contract},
        set(),
        {},
        {decision_receipt["receipt_instance_id"]: decision_receipt},
        {authorized_fixture["envelope_id"]: authorized_fixture},
    )
    if any("analysis-only preflight carries execution authority" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-ANALYSIS-ONLY-EXECUTION-AUTHORITY was not rejected")

    crossover_contract = dict(preflight_contract)
    crossover_contract["prototype_id"] = "D04-P2-CROSSOVER"
    bad_crossover = copy.deepcopy(preflight)
    bad_crossover["prototype_id"] = "D04-P2-CROSSOVER"
    bad_crossover["upstream_outcomes"] = "TSN-P1-RESULT=no_winner"
    bad_crossover["preflight_payload_sha256"] = canonical_preflight_payload(bad_crossover)
    errors = validate_preflight_row(
        bad_crossover,
        {"PX-FI": crossover_contract},
        {"GATE-GD1"},
        {},
        {decision_receipt["receipt_instance_id"]: decision_receipt},
        {authorized_fixture["envelope_id"]: authorized_fixture},
    )
    if any("upstream outcome does not permit crossover" in error for error in errors):
        rejected += 1
    else:
        failures.append("FI-CROSSOVER-NONSHORTLIST-OUTCOME was not rejected")

    return rejected, failures


def main() -> int:
    audit = Audit()
    try:
        envelope_schema, envelope_rows = check_schema_registry_pair(
            audit, ENVELOPE_SCHEMA_PATH, ENVELOPE_INSTANCE_PATH, "execution envelope"
        )
        decision_receipt_schema, decision_receipt_rows = check_schema_registry_pair(
            audit, DECISION_RECEIPT_SCHEMA_PATH, DECISION_RECEIPT_INSTANCE_PATH, "decision receipt"
        )
        envelope_receipt_schema, envelope_receipt_rows = check_schema_registry_pair(
            audit, ENVELOPE_RECEIPT_SCHEMA_PATH, ENVELOPE_RECEIPT_INSTANCE_PATH,
            "envelope authorization receipt",
        )
        budget_pool_schema, budget_pool_rows = check_schema_registry_pair(
            audit, BUDGET_POOL_SCHEMA_PATH, BUDGET_POOL_INSTANCE_PATH, "shared budget pool"
        )
        preflight_schema, preflight_rows = check_schema_registry_pair(
            audit, PREFLIGHT_SCHEMA_PATH, PREFLIGHT_INSTANCE_PATH, "prototype preflight"
        )
        gate_instance_schema, gate_instance_rows = check_schema_registry_pair(
            audit, GATE_INSTANCE_SCHEMA_PATH, GATE_INSTANCE_PATH, "Candidate Gate instance"
        )
        _, decision_rows = read_tsv(DECISION_PATH)
        _, set_rows = read_tsv(DECISION_SET_PATH)
        _, requirement_rows = read_tsv(DECISION_REQUIREMENT_PATH)
        _, preflight_contract_rows = read_tsv(PREFLIGHT_REQUIREMENT_PATH)
        _, prototype_rows = read_tsv(PROTOTYPE_PATH)
        _, gate_rows = read_tsv(GATE_PATH)
        _, time_system_rows = read_tsv(TIME_SYSTEM_PATH)
    except (OSError, ValueError) as exc:
        print(f"Candidate authorization contracts: FAIL\n- {exc}")
        return 1

    decisions = keyed(decision_rows, "decision_id", audit, "decisions")
    sets = keyed(set_rows, "receipt_set_id", audit, "decision receipt sets")
    requirements = keyed(requirement_rows, "requirement_id", audit, "decision requirements")
    contracts = keyed(preflight_contract_rows, "preflight_contract_id", audit, "preflight contracts")
    prototypes = keyed(prototype_rows, "prototype_id", audit, "prototypes")
    gates = keyed(gate_rows, "gate_id", audit, "Gate definitions")
    time_system = keyed(time_system_rows, "contract_id", audit, "time-system contracts")
    decision_receipts = keyed(decision_receipt_rows, "receipt_instance_id", audit, "decision receipt instances")
    envelope_receipts = keyed(
        envelope_receipt_rows, "envelope_receipt_instance_id", audit, "envelope receipt instances"
    )
    envelopes = keyed(envelope_rows, "envelope_id", audit, "execution envelopes")
    budget_pools = keyed(budget_pool_rows, "shared_budget_pool_id", audit, "shared budget pools")
    gate_instances = keyed(gate_instance_rows, "gate_instance_id", audit, "Candidate Gate instances")
    keyed(preflight_rows, "preflight_instance_id", audit, "preflight instances")

    required_envelope_fields = {
        "authorization_subject_sha256",
        "envelope_authorization_receipt_instance_id",
        "envelope_authorization_receipt_path",
        "envelope_authorization_receipt_sha256",
        "envelope_authorization_record_locator",
        "authorized_by_user_ref",
        "authorized_action_codes",
        "workspace_root_id",
        "base_revision",
        "source_snapshot_manifest_path",
        "source_snapshot_manifest_sha256",
        "exclusive_scope_key",
        "shared_budget_program_scope_key",
        "shared_budget_pool_id",
        "shared_budget_pool_subject_sha256",
        "shared_budget_pool_cap_calendar_days",
        "shared_budget_pool_cap_person_hours",
        "shared_budget_pool_cap_external_cash",
        "shared_budget_pool_ledger_path",
        "shared_budget_pool_ledger_sha256",
        "shared_budget_pool_preflight_result",
        "supersedes_envelope_id",
        "overlap_check_result",
        "extension_policy",
    }
    envelope_schema_fields = {row["field_name"] for row in envelope_schema}
    audit.require(
        required_envelope_fields <= envelope_schema_fields,
        f"execution envelope schema missing fields: {sorted(required_envelope_fields - envelope_schema_fields)}",
    )
    audit.require(
        {"user_message_ref", "decision_spec_sha256", "receipt_artifact_sha256"}
        <= {row["field_name"] for row in decision_receipt_schema},
        "decision receipt schema lacks exact source/message/artifact binding",
    )
    audit.require(
        {"envelope_id", "authorization_subject_sha256", "receipt_artifact_sha256"}
        <= {row["field_name"] for row in envelope_receipt_schema},
        "envelope receipt schema lacks exact envelope subject/artifact binding",
    )
    audit.require(
        {"shared_budget_program_scope_key", "pool_subject_sha256", "cap_person_hours"}
        <= {row["field_name"] for row in budget_pool_schema},
        "budget pool schema lacks cumulative scope/subject/cap binding",
    )
    audit.require(
        {"execution_envelope_id", "envelope_authorization_receipt_instance_id", "preflight_payload_sha256"}
        <= {row["field_name"] for row in preflight_schema},
        "preflight schema lacks exact envelope/receipt/payload binding",
    )

    # No decision, receipt, envelope, pool, Gate instance or preflight is pre-approved.
    for decision_id, row in decisions.items():
        if row["decision_status"] == "presented_no_decision":
            audit.require(not row["user_choice"], f"{decision_id}: user choice prefilled")
            for requirement in requirement_rows:
                if requirement["decision_id"] == decision_id:
                    audit.require(
                        requirement["receipt_path"] == "none"
                        and requirement["receipt_sha256"] == "none"
                        and requirement["requirement_status"] == "missing",
                        f"{requirement['requirement_id']}: unapproved decision has receipt evidence",
                    )

    audit.require(not decision_receipt_rows, "Candidate package prefilled decision receipt instances")
    audit.require(not envelope_receipt_rows, "Candidate package prefilled envelope authorization receipts")
    audit.require(not envelope_rows, "Candidate package prefilled execution envelopes")
    audit.require(not budget_pool_rows, "Candidate package prefilled budget pools")
    audit.require(not gate_instance_rows, "Candidate package prefilled Candidate Gate instances")
    audit.require(not preflight_rows, "Candidate package prefilled execution preflights")

    for decision_id in ("DEC-01", "DEC-02", "DEC-11"):
        audit.require(decision_id in decisions, f"missing {decision_id}")
    if all(decision_id in decisions for decision_id in ("DEC-01", "DEC-02", "DEC-11")):
        dec01, dec02, dec11 = decisions["DEC-01"], decisions["DEC-02"], decisions["DEC-11"]
        audit.require(
            "本决策单独不解锁任何prototype/gate/build/session" in dec01["candidate_test_unlocks"],
            "DEC-01 still grants broad executable scope",
        )
        audit.require(
            "不单独解锁Scheduler或测试仪器" in dec02["candidate_test_unlocks"]
            and "DEC-01/03/11" in dec02["candidate_test_unlocks"]
            and "scope化GD1" in dec02["candidate_test_unlocks"],
            "DEC-02 execution AND-dependencies are not explicit",
        )
        audit.require(
            "synthetic/frozen-copy" in dec11["candidate_test_unlocks"]
            and "dry-run manifest" in dec11["candidate_test_unlocks"]
            and "不得产生Current Writer可读内容" in dec11["candidate_test_unlocks"],
            "DEC-11 isolated test scope is too broad",
        )
        for row in (dec01, dec02, dec11):
            audit.require(
                "Build" in row["default_if_deferred"] and "Session" in row["default_if_deferred"],
                f"{row['decision_id']}: deferred default is not explicitly fail-closed",
            )

    required_dec11_sets = {
        "DRS-DEC11-A": ("candidate_test_authorization", "DR-DEC11-A"),
        "DRS-DEC11-M": ("bounded_migration_plan", "DR-DEC11-M"),
        "DRS-DEC11-M1": ("bounded_migration_checker", "DR-DEC11-M1"),
        "DRS-DEC11-M2": ("bounded_migration_registry", "DR-DEC11-M2"),
        "DRS-DEC11-M3": ("bounded_migration_chain", "DR-DEC11-M3"),
        "DRS-DEC11-M4": ("bounded_migration_postcheck", "DR-DEC11-M4"),
    }
    for set_id, (phase, requirement_id) in required_dec11_sets.items():
        row = sets.get(set_id)
        audit.require(row is not None, f"missing DEC-11 staged set {set_id}")
        if row:
            audit.require(
                row["decision_id"] == "DEC-11"
                and row["phase"] == phase
                and row["requirement_ids"] == requirement_id,
                f"{set_id}: phase/requirement mismatch",
            )
        requirement = requirements.get(requirement_id)
        audit.require(requirement is not None, f"missing {requirement_id}")
        if requirement:
            audit.require(requirement["phase"] == phase, f"{requirement_id}: phase differs from receipt set")
    if "DR-DEC11-M3" in requirements:
        audit.require(
            "一个精确chapter/episode/scope" in requirements["DR-DEC11-M3"]["required_scope"]
            and "不得复合批量迁移" in requirements["DR-DEC11-M3"]["notes"],
            "DEC-11 M3 is not one-scope-only",
        )

    required_contracts = {
        "PX-R0-IMPLEMENT",
        "PX-P1A-IMPLEMENT", "PX-P1B-IMPLEMENT", "PX-P1C-IMPLEMENT", "PX-P1D-IMPLEMENT",
        "PX-P1A-HUMAN", "PX-P1B-HUMAN", "PX-P1C-HUMAN", "PX-P1D-HUMAN",
        "PX-P1-SHORTLIST-ANALYSIS", "PX-P1-SHORTLIST-HUMAN",
        "PX-P2-CROSSOVER-IMPLEMENT", "PX-P2-CROSSOVER-HUMAN",
    }
    audit.require(
        required_contracts <= contracts.keys(),
        f"missing preflight contracts: {sorted(required_contracts - contracts.keys())}",
    )
    audit.require("PX-P1-DECISION-HUMAN" not in contracts, "obsolete P1 decision-human carrier reintroduced")
    for contract_id, row in contracts.items():
        audit.require(row["prototype_id"] in prototypes, f"{contract_id}: unknown prototype {row['prototype_id']}")
        audit.require(
            all(value in sets for value in split_refs(row["required_decision_receipt_set_templates"])),
            f"{contract_id}: unknown receipt set template",
        )
        audit.require(
            all(value in requirements for value in split_refs(row["required_requirement_ids"])),
            f"{contract_id}: unknown decision requirement",
        )
        audit.require(
            all(value in gates for value in split_refs(row["required_scoped_gate_definitions"])),
            f"{contract_id}: unknown Gate definition",
        )
        audit.require(
            "gate_definition" in row["forbidden_substitutions"]
            and "decision_status" in row["forbidden_substitutions"],
            f"{contract_id}: does not reject definition/status substitution",
        )
        audit.require(
            "DRS-DEC03-M" not in row["required_decision_receipt_set_templates"]
            and "DR-DEC03-M" not in row["required_requirement_ids"],
            f"{contract_id}: DEC-03 final migration receipt wrongly grants prototype execution",
        )

    p1_variants = ("A", "B", "C", "D")
    expected_direction_sets = {"DRS-DEC01-A", "DRS-DEC02-A", "DRS-DEC03-A", "DRS-DEC11-A"}
    for variant in p1_variants:
        contract_id = f"PX-P1{variant}-IMPLEMENT"
        row = contracts.get(contract_id)
        if row:
            audit.require(
                set(split_refs(row["required_decision_receipt_set_templates"])) == expected_direction_sets,
                f"{contract_id}: P1 implementation does not require all four direction receipts",
            )
            audit.require(
                row["required_execution_envelope_id"] == "E-P1-ABCD-IMPLEMENT"
                and row["required_scoped_gate_definitions"] == "GATE-GD1"
                and row["required_upstream_evidence"] == "R0-TEST-KERNEL@M3"
                and row["required_envelope_max_total_builds"] == "4"
                and row["required_shared_budget_program_scope_key"] == "STAGE0_R0_P1"
                and row["required_shared_budget_pool_caps"] == "calendar_days=14,person_hours=80,external_cash=0"
                and "must_equal_bundle:D04-P1-A,D04-P1-B,D04-P1-C,D04-P1-D" in row["envelope_prototype_scope_rule"]
                and "must_not_include:R0-TEST-KERNEL" in row["envelope_prototype_scope_rule"],
                f"{contract_id}: P1 ABCD envelope/R0 M3/GD1/shared-pool contract incomplete",
            )
    r0_contract = contracts.get("PX-R0-IMPLEMENT")
    if r0_contract:
        audit.require(
            r0_contract["required_execution_envelope_id"] == "E-R0-IMPLEMENT"
            and r0_contract["required_envelope_max_total_builds"] == "1"
            and r0_contract["required_shared_budget_program_scope_key"] == "STAGE0_R0_P1"
            and r0_contract["required_shared_budget_pool_caps"] == "calendar_days=14,person_hours=80,external_cash=0"
            and "must_equal:R0-TEST-KERNEL" in r0_contract["envelope_prototype_scope_rule"]
            and "must_not_include:D04-P1-A,D04-P1-B,D04-P1-C,D04-P1-D" in r0_contract["envelope_prototype_scope_rule"],
            "R0 exact envelope/build cap/shared-pool isolation incomplete",
        )
    shortlist = contracts.get("PX-P1-SHORTLIST-ANALYSIS")
    if shortlist:
        audit.require(
            shortlist["execution_phase"] == "analysis_only"
            and shortlist["required_execution_envelope_id"] == "none"
            and shortlist["envelope_prototype_scope_rule"] == "must_equal:none"
            and shortlist["required_envelope_max_total_builds"] == "not_applicable"
            and shortlist["required_shared_budget_program_scope_key"] == "none"
            and set(split_refs(shortlist["required_upstream_evidence"]))
            == {f"D04-P1-{variant}@M5" for variant in p1_variants}
            and "single_winner" in shortlist["forbidden_substitutions"],
            "P1 SHORTLIST analysis is not read-only/four-carrier/non-winner",
        )
    tsn_result = time_system.get("TSN-P1-RESULT", {})
    for crossover_id in ("PX-P2-CROSSOVER-IMPLEMENT", "PX-P2-CROSSOVER-HUMAN"):
        crossover = contracts.get(crossover_id)
        if crossover:
            audit.require(
                set(split_refs(crossover["required_decision_receipt_set_templates"]))
                == expected_direction_sets | {"DRS-DEC04-A"}
                and "D04-P1-SHORTLIST@M5" in split_refs(crossover["required_upstream_evidence"])
                and crossover["required_execution_envelope_id"].startswith("new_separate")
                and all(token in crossover["preflight_logic"] for token in (
                    "shortlist_two", "shortlist_three", "shortlist_four",
                    "no_winner", "revise_top_two", "retire_all",
                ))
                and all(token in crossover["forbidden_substitutions"] for token in (
                    "DEC03_M", "no_winner", "revise_top_two", "retire_all",
                ))
                and "only_shortlist_two_or_three_or_four_may_enter_crossover"
                in tsn_result.get("reversible_carrier_rule", "")
                and "no_winner_or_revise_top_two_or_retire_all_unlock_nothing"
                in tsn_result.get("reversible_carrier_rule", ""),
                f"{crossover_id}: lacks DEC04-A/shortlist-only result/evidence/separate envelope/DEC03-M exclusion",
            )

    for row in decision_receipt_rows:
        audit.errors.extend(validate_decision_receipt_row(row, sets, requirements))
    for row in envelope_receipt_rows:
        audit.errors.extend(validate_envelope_receipt_row(row))
    for row in envelope_rows:
        audit.errors.extend(
            validate_envelope_row(
                row, envelope_receipts, decision_receipts, requirements, budget_pools
            )
        )
    for row in budget_pool_rows:
        audit.errors.extend(validate_budget_pool_row(row, envelopes))
    for row in gate_instance_rows:
        audit.errors.extend(validate_gate_instance_row(row, gates, decision_receipts))
    for row in preflight_rows:
        audit.errors.extend(
            validate_preflight_row(row, contracts, set(gates), gate_instances, decision_receipts, envelopes)
        )

    active_scope_keys = [row["exclusive_scope_key"] for row in envelope_rows if row["status"] == "authorized"]
    duplicate_scope_keys = [value for value, count in Counter(active_scope_keys).items() if count > 1]
    audit.require(
        not duplicate_scope_keys,
        f"authorized envelopes overlap exclusive scope keys: {sorted(duplicate_scope_keys)}",
    )
    active_program_keys = [
        row["shared_budget_program_scope_key"] for row in budget_pool_rows if row["status"] == "authorized"
    ]
    duplicate_program_keys = [value for value, count in Counter(active_program_keys).items() if count > 1]
    audit.require(
        not duplicate_program_keys,
        f"multiple active budget pools share program scope: {sorted(duplicate_program_keys)}",
    )

    envelope_fields = [row["field_name"] for row in envelope_schema]
    pool_fields = [row["field_name"] for row in budget_pool_schema]
    rejected_faults, fault_failures = run_fault_injections(envelope_fields, pool_fields)
    audit.errors.extend(fault_failures)
    audit.require(rejected_faults == 11, f"authorization fault injection rejected {rejected_faults}/11")

    if audit.errors:
        print("Candidate authorization contracts: FAIL")
        for error in audit.errors:
            print(f"- {error}")
        return 1

    print("Candidate authorization contracts: PASS")
    print(
        f"- schemas: envelope={len(envelope_schema)}; decision_receipt={len(decision_receipt_schema)}; "
        f"envelope_receipt={len(envelope_receipt_schema)}; budget_pool={len(budget_pool_schema)}; "
        f"preflight={len(preflight_schema)}; gate_instance={len(gate_instance_schema)}"
    )
    print(
        f"- instances: decision_receipts={len(decision_receipt_rows)}; envelope_receipts={len(envelope_receipt_rows)}; "
        f"envelopes={len(envelope_rows)}; budget_pools={len(budget_pool_rows)}; "
        f"gate_instances={len(gate_instance_rows)}; preflights={len(preflight_rows)}"
    )
    print("- R0/P1 implementation envelopes separated; shared Stage0 14d/80h/cash0 pool enforced")
    print("- P1 A/B/C/D, SHORTLIST and P2 CROSSOVER preflight contracts are fail-closed")
    print("- DEC-11 migration split: plan -> checker -> registry -> one-scope chain -> postcheck")
    print(f"- preflight contracts={len(preflight_contract_rows)}; fault injections rejected={rejected_faults}/11")
    return 0


if __name__ == "__main__":
    sys.exit(main())
