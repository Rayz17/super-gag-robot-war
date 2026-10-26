#!/usr/bin/env python3
"""Validate the Candidate RunState v2 / StateTransaction v2 paper contract.

This checker is deliberately a pure-Python reference oracle over static
fixtures.  It does not load Godot, migrate the v1 store, write a save file, or
provide Build/human-play evidence.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[1]
DATA = PACKAGE / "data"
TYPE_PATH = DATA / "runstate-v2-enum-type-registry.tsv"
FIELD_PATH = DATA / "runstate-v2-field-schema.tsv"
DOMAIN_PATH = DATA / "runstate-v2-domain-registry.tsv"
OP_PATH = DATA / "state-transaction-v2-op-schema.tsv"
FIXTURE_REGISTRY_PATH = DATA / "runstate-v2-r0-p1-fixture-coverage.tsv"
FIXTURE_PATH = DATA / "runstate-v2-r0-p1-fixtures.json"
STATE_CONTRACT_PATH = DATA / "system-state-contracts.tsv"
OWNER_PATH = DATA / "settlement-owner-prepare-commit-contracts.tsv"

EXPECTED_TYPE_COUNT = 47
EXPECTED_RECORD_TYPE_COUNT = 35
EXPECTED_DOMAIN_COUNT = 26
EXPECTED_OP_COUNT = 7
EXPECTED_FIXTURE_IDS = {
    "FX-RS2-R0-ATOMIC",
    "FX-RS2-R0-MISSING-OWNER",
    "FX-RS2-P1-C2-REDACTION",
    "FX-RS2-P1-STALE-REVISION",
}
EXCLUDED_OWNER_STATES = {"ST_IDENTITY", "ST_UI_PROJECTION"}
EXPECTED_BOUNDARY = {
    "canon_write_allowed": False,
    "reader_write_allowed": False,
    "runtime_write_allowed": False,
    "demo_write_allowed": False,
    "build_status": "zero_build",
    "human_evidence_status": "not_run",
}
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@/\-]*$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
DECIMAL_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$")
PATH_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*$")


def read_tsv(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError(f"empty TSV: {path.name}")
    width = len(lines[0].split("\t"))
    for line_number, line in enumerate(lines, start=1):
        if len(line.split("\t")) != width:
            raise ValueError(f"{path.name}:{line_number} width drift")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def split_values(raw: str) -> list[str]:
    if not raw or raw == "NONE":
        return []
    return raw.split(";")


def parse_signature(raw: str) -> dict[str, str]:
    if not raw or raw == "NONE":
        return {}
    result: dict[str, str] = {}
    for token in raw.split(";"):
        if ":" not in token:
            raise ValueError(f"untyped field token: {token}")
        field, type_id = token.split(":", 1)
        if not field or not type_id or field in result:
            raise ValueError(f"invalid/duplicate field token: {token}")
        result[field] = type_id
    return result


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def proposal_hash(transaction: dict[str, Any]) -> str:
    payload = copy.deepcopy(transaction)
    payload.pop("proposal_hash", None)
    return canonical_hash(payload)


def fixture_hash(fixture: dict[str, Any]) -> str:
    payload = copy.deepcopy(fixture)
    payload.pop("canonical_sha256", None)
    return canonical_hash(payload)


def contains_float(value: Any) -> bool:
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(contains_float(key) or contains_float(child) for key, child in value.items())
    if isinstance(value, list):
        return any(contains_float(child) for child in value)
    return False


def value_at(root: Any, dotted_path: str) -> Any:
    current = root
    for part in dotted_path.split("."):
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(dotted_path)
    return current


def delete_at(root: dict[str, Any], dotted_path: str) -> bool:
    parts = dotted_path.split(".")
    current: Any = root
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    if not isinstance(current, dict) or parts[-1] not in current:
        return False
    del current[parts[-1]]
    return True


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_type(
    value: Any,
    type_id: str,
    type_rows: dict[str, dict[str, str]],
    path: str,
    errors: list[str],
) -> None:
    row = type_rows.get(type_id)
    if row is None:
        errors.append(f"{path}: unknown type {type_id}")
        return
    validator = row["validator_id"]
    allowed = split_values(row["allowed_values"])
    valid = True
    if validator == "boolean":
        valid = isinstance(value, bool)
    elif validator == "int_nonnegative":
        valid = isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 2147483647
    elif validator == "int_positive":
        valid = isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 2147483647
    elif validator == "decimal_string":
        valid = isinstance(value, str) and bool(DECIMAL_RE.fullmatch(value))
    elif validator == "ratio_string":
        try:
            valid = isinstance(value, str) and bool(DECIMAL_RE.fullmatch(value)) and Decimal("0") <= Decimal(value) <= Decimal("1")
        except (InvalidOperation, TypeError):
            valid = False
    elif validator == "id":
        valid = isinstance(value, str) and bool(ID_RE.fullmatch(value))
    elif validator == "id_or_none":
        valid = isinstance(value, str) and (value == "NONE" or bool(ID_RE.fullmatch(value)))
    elif validator in {"token", "text", "version_token", "time_token", "duration_token", "source_ref"}:
        valid = isinstance(value, str) and bool(value) and "\t" not in value and "\n" not in value
    elif validator == "time_or_none":
        valid = isinstance(value, str) and (value == "NONE" or (bool(value) and "\t" not in value and "\n" not in value))
    elif validator == "hash_sha256":
        valid = isinstance(value, str) and bool(HASH_RE.fullmatch(value))
    elif validator == "hash_or_none":
        valid = isinstance(value, str) and (value == "NONE" or bool(HASH_RE.fullmatch(value)))
    elif validator == "json_value_no_float":
        valid = not contains_float(value)
    elif validator == "json_object_no_float":
        valid = isinstance(value, dict) and not contains_float(value) and all(isinstance(key, str) for key in value)
    elif validator == "json_list_no_float":
        valid = isinstance(value, list) and not contains_float(value)
    elif validator == "id_list":
        valid = isinstance(value, list) and all(isinstance(item, str) and bool(ID_RE.fullmatch(item)) for item in value) and len(value) == len(set(value))
    elif validator == "text_list":
        valid = isinstance(value, list) and all(isinstance(item, str) and bool(item) and "\t" not in item for item in value)
    elif validator == "path_list":
        valid = isinstance(value, list) and all(isinstance(item, str) and bool(PATH_RE.fullmatch(item)) for item in value) and len(value) == len(set(value))
    elif validator == "string_map":
        valid = isinstance(value, dict) and all(isinstance(key, str) and isinstance(item, str) for key, item in value.items())
    elif validator == "version_map":
        valid = isinstance(value, dict) and all(isinstance(key, str) and bool(ID_RE.fullmatch(key)) and isinstance(item, int) and not isinstance(item, bool) and item >= 0 for key, item in value.items())
    elif validator in {"domain_map", "record_map", "receipt_map"}:
        valid = isinstance(value, dict) and all(isinstance(key, str) and bool(ID_RE.fullmatch(key)) for key in value)
    elif validator in {"state_op_list", "prepared_receipt_list"}:
        valid = isinstance(value, list) and all(isinstance(item, dict) for item in value)
    elif validator == "enum":
        valid = isinstance(value, str) and value in allowed
    else:
        errors.append(f"{path}: checker has no validator implementation for {validator}")
        return
    if not valid:
        errors.append(f"{path}: value does not satisfy {type_id}")


def validate_record(
    value: dict[str, Any],
    record_type: str,
    field_rows: dict[str, dict[str, str]],
    type_rows: dict[str, dict[str, str]],
    path: str,
    errors: list[str],
    *,
    include_domain_meta: bool = False,
) -> None:
    schema = field_rows.get(record_type)
    if schema is None:
        errors.append(f"{path}: unknown record type {record_type}")
        return
    try:
        required = parse_signature(schema["required_fields_typed"])
        optional = parse_signature(schema["optional_fields_typed"])
        if include_domain_meta:
            meta = field_rows["DOMAIN_RECORD_META_V2"]
            required.update(parse_signature(meta["required_fields_typed"]))
            optional.update(parse_signature(meta["optional_fields_typed"]))
    except ValueError as error:
        errors.append(f"{path}: {error}")
        return
    missing = set(required) - set(value)
    extra = set(value) - set(required) - set(optional)
    require(errors, not missing, f"{path}: missing fields {sorted(missing)}")
    require(errors, not extra, f"{path}: unknown fields {sorted(extra)}")
    for field, type_id in {**required, **optional}.items():
        if field in value:
            validate_type(value[field], type_id, type_rows, f"{path}.{field}", errors)


def validate_snapshot(
    state: dict[str, Any],
    field_rows: dict[str, dict[str, str]],
    type_rows: dict[str, dict[str, str]],
    domain_rows: dict[str, dict[str, str]],
    errors: list[str],
    prefix: str,
) -> None:
    validate_record(state, "RUN_STATE_V2", field_rows, type_rows, prefix, errors)
    require(errors, state.get("schema_version") == 2, f"{prefix}: schema_version must be 2")
    require(errors, state.get("authority_boundary") == "candidate_only_zero_build", f"{prefix}: authority boundary differs")
    clock = state.get("world_clock")
    if isinstance(clock, dict):
        validate_record(clock, "WORLD_CLOCK_V2", field_rows, type_rows, f"{prefix}.world_clock", errors)
        require(errors, clock.get("clock_version") == 1, f"{prefix}: clock_version must be 1")
    domains = state.get("domains", {})
    versions = state.get("domain_versions", {})
    if not isinstance(domains, dict) or not isinstance(versions, dict):
        return
    require(errors, set(domains) == set(versions), f"{prefix}: domain_versions keys differ from domains")
    for state_id, bucket in domains.items():
        contract = domain_rows.get(state_id)
        if contract is None:
            errors.append(f"{prefix}: unknown state domain {state_id}")
            continue
        if not isinstance(bucket, dict):
            errors.append(f"{prefix}.{state_id}: bucket is not an object")
            continue
        validate_record(bucket, "DOMAIN_BUCKET_V2", field_rows, type_rows, f"{prefix}.domains.{state_id}", errors)
        require(errors, bucket.get("state_id") == state_id, f"{prefix}.{state_id}: bucket state_id differs")
        require(errors, bucket.get("owner_system") == contract["owner_system"], f"{prefix}.{state_id}: owner system differs")
        require(errors, bucket.get("owner_group_id") == contract["owner_group_id"], f"{prefix}.{state_id}: owner group differs")
        require(errors, bucket.get("domain_version") == versions.get(state_id), f"{prefix}.{state_id}: domain version differs")
        records = bucket.get("records", {})
        if not isinstance(records, dict):
            continue
        for record_id, record in records.items():
            if not isinstance(record, dict):
                errors.append(f"{prefix}.{state_id}.{record_id}: record is not an object")
                continue
            validate_record(record, contract["record_type"], field_rows, type_rows, f"{prefix}.domains.{state_id}.records.{record_id}", errors, include_domain_meta=True)
            require(errors, record.get(contract["record_id_field"]) == record_id, f"{prefix}.{state_id}.{record_id}: record ID field differs")
            visibility = record.get("_visibility_scope")
            observer_ids = record.get("_observer_ids", [])
            require(errors, visibility != "observer_set" or bool(observer_ids), f"{prefix}.{state_id}.{record_id}: observer_set has no observers")
            extensions = record.get("extensions", {})
            redactions = set(record.get("_redact_fields", []))
            if visibility != "backend_only" and isinstance(extensions, dict):
                for key in extensions:
                    if key.startswith("backend_"):
                        require(errors, f"extensions.{key}" in redactions, f"{prefix}.{state_id}.{record_id}: backend extension lacks redaction path")
            if state_id == "ST_RESOURCE":
                try:
                    before = Decimal(record["balance_before"])
                    delta = Decimal(record["delta"])
                    after = Decimal(record["balance_after"])
                except (InvalidOperation, KeyError):
                    pass
                else:
                    require(errors, before + delta == after, f"{prefix}.{state_id}.{record_id}: resource arithmetic differs")
            if state_id == "ST_RESULT":
                require(errors, bool(record.get("future_consumers")), f"{prefix}.{state_id}.{record_id}: future_consumers empty")
    ledger = state.get("transaction_ledger", {})
    order = state.get("commit_order", [])
    if isinstance(ledger, dict) and isinstance(order, list):
        require(errors, set(order) == set(ledger), f"{prefix}: commit_order and ledger keys differ")
        require(errors, len(order) == len(set(order)), f"{prefix}: duplicate commit_order ID")
        for transaction_id, receipt in ledger.items():
            if isinstance(receipt, dict):
                validate_record(receipt, "COMMIT_RECEIPT_V2", field_rows, type_rows, f"{prefix}.transaction_ledger.{transaction_id}", errors)
                require(errors, receipt.get("transaction_group_id") == transaction_id, f"{prefix}: ledger key differs from receipt transaction")


def current_record(state: dict[str, Any], state_id: str, record_id: str) -> dict[str, Any] | None:
    return state.get("domains", {}).get(state_id, {}).get("records", {}).get(record_id)


def validate_transaction(
    state: dict[str, Any],
    transaction: dict[str, Any],
    prepared: list[dict[str, Any]],
    field_rows: dict[str, dict[str, str]],
    type_rows: dict[str, dict[str, str]],
    domain_rows: dict[str, dict[str, str]],
    op_rows: dict[str, dict[str, str]],
    errors: list[str],
    prefix: str,
) -> None:
    validate_record(transaction, "STATE_TRANSACTION_V2", field_rows, type_rows, f"{prefix}.transaction", errors)
    require(errors, transaction.get("schema_version") == 2, f"{prefix}: transaction schema_version must be 2")
    require(errors, transaction.get("idempotency_key") == transaction.get("transaction_group_id"), f"{prefix}: idempotency_key differs from transaction_group_id")
    require(errors, transaction.get("proposal_hash") == proposal_hash(transaction), f"{prefix}: proposal_hash differs")
    operations = transaction.get("operations", [])
    op_ids: list[str] = []
    touched_groups: set[str] = set()
    for index, op in enumerate(operations):
        if not isinstance(op, dict):
            errors.append(f"{prefix}.operations.{index}: not an object")
            continue
        validate_record(op, "STATE_OP_V2", field_rows, type_rows, f"{prefix}.operations.{index}", errors)
        op_id = op.get("op_id", "")
        op_ids.append(op_id)
        state_id = op.get("state_id", "")
        contract = domain_rows.get(state_id)
        kind = op.get("op_kind", "")
        kind_contract = op_rows.get(kind)
        if contract is None or kind_contract is None:
            continue
        touched_groups.add(contract["owner_group_id"])
        require(errors, op.get("owner_group_id") == contract["owner_group_id"], f"{prefix}.{op_id}: op owner differs from domain")
        require(errors, kind in split_values(contract["allowed_op_kinds"]), f"{prefix}.{op_id}: op kind not allowed by domain")
        require(errors, state_id in split_values(kind_contract["allowed_state_ids"]), f"{prefix}.{op_id}: state not allowed by op schema")
        current = current_record(state, state_id, op.get("record_id", ""))
        if kind == "OP_CREATE_RECORD":
            require(errors, current is None, f"{prefix}.{op_id}: create target already exists")
            require(errors, op.get("from_version") == 0 and op.get("to_version") == 1, f"{prefix}.{op_id}: create version invariant differs")
            require(errors, op.get("expected_record_hash") == "NONE", f"{prefix}.{op_id}: create expected hash must be NONE")
            payload = op.get("payload")
            if isinstance(payload, dict):
                validate_record(payload, contract["record_type"], field_rows, type_rows, f"{prefix}.{op_id}.payload", errors, include_domain_meta=True)
                require(errors, payload.get(contract["record_id_field"]) == op.get("record_id"), f"{prefix}.{op_id}: payload record ID differs")
        else:
            require(errors, current is not None, f"{prefix}.{op_id}: mutation target missing")
            if current is not None:
                require(errors, op.get("from_version") == current.get("_record_version"), f"{prefix}.{op_id}: from_version differs")
                require(errors, op.get("to_version") == op.get("from_version") + 1, f"{prefix}.{op_id}: to_version differs")
                require(errors, op.get("expected_record_hash") == canonical_hash(current), f"{prefix}.{op_id}: expected_record_hash differs")
            if kind == "OP_REPLACE_RECORD" and isinstance(op.get("payload"), dict):
                validate_record(op["payload"], contract["record_type"], field_rows, type_rows, f"{prefix}.{op_id}.payload", errors, include_domain_meta=True)
            if kind == "OP_PATCH_RECORD":
                require(errors, isinstance(op.get("payload", {}).get("patch"), dict) and bool(op["payload"]["patch"]), f"{prefix}.{op_id}: patch payload absent")
            if kind == "OP_CLOSE_RECORD":
                payload = op.get("payload", {})
                require(errors, isinstance(payload.get("status_or_resolution_patch"), dict) and bool(payload.get("closed_reason")), f"{prefix}.{op_id}: close payload incomplete")
            if kind == "OP_RESOURCE_DELTA":
                payload = op.get("payload", {})
                required_payload = split_values(kind_contract["required_payload_keys"])
                require(errors, set(required_payload) <= set(payload), f"{prefix}.{op_id}: resource payload fields missing")
                try:
                    valid_sum = Decimal(payload["balance_before"]) + Decimal(payload["delta"]) == Decimal(payload["balance_after"])
                except (InvalidOperation, KeyError):
                    valid_sum = False
                require(errors, valid_sum, f"{prefix}.{op_id}: resource delta arithmetic differs")
                if current is not None:
                    require(errors, payload.get("balance_before") == current.get("balance_after"), f"{prefix}.{op_id}: resource before differs from ledger balance")
                domain_owner = payload.get("domain_owner_system")
                prepared_systems = {item.get("owner_system") for item in prepared if item.get("status") == "prepared"}
                require(errors, domain_owner in prepared_systems, f"{prefix}.{op_id}: resource domain owner did not prepare transaction")
            if kind == "OP_APPEND_EVENT":
                payload = op.get("payload", {})
                require(errors, set(split_values(kind_contract["required_payload_keys"])) <= set(payload), f"{prefix}.{op_id}: append payload incomplete")
                if current is not None:
                    target = current.get(payload.get("list_field"), [])
                    event_id = payload.get("event_id")
                    existing = {item.get("event_id") for item in target if isinstance(item, dict)} if isinstance(target, list) else set()
                    require(errors, isinstance(target, list) and event_id not in existing, f"{prefix}.{op_id}: append target/event differs")
            if kind == "OP_TRANSFER_UNIQUE" and current is not None:
                payload = op.get("payload", {})
                require(errors, set(split_values(kind_contract["required_payload_keys"])) <= set(payload), f"{prefix}.{op_id}: unique transfer payload incomplete")
                require(errors, current.get("instance_or_unique") == "unique", f"{prefix}.{op_id}: transfer target is not unique")
                require(errors, payload.get("item_id") == op.get("record_id") == current.get("item_id"), f"{prefix}.{op_id}: transfer item identity differs")
                require(
                    errors,
                    payload.get("lawful_owner") == current.get("lawful_owner")
                    and payload.get("from_current_holder") == current.get("current_holder")
                    and payload.get("from_physical_location") == current.get("physical_location")
                    and payload.get("from_slot") == current.get("slot"),
                    f"{prefix}.{op_id}: transfer source physical truth differs",
                )
                require(
                    errors,
                    payload.get("transfer_receipt_id") not in {None, "NONE"},
                    f"{prefix}.{op_id}: accepted transfer receipt ID missing",
                )
        require(errors, op.get("visibility_scope") == op.get("payload", {}).get("_visibility_scope", op.get("visibility_scope")), f"{prefix}.{op_id}: operation/payload visibility differs")
        require(errors, op.get("observer_ids") == op.get("payload", {}).get("_observer_ids", op.get("observer_ids")), f"{prefix}.{op_id}: operation/payload observers differ")
        require(errors, op.get("redact_fields") == op.get("payload", {}).get("_redact_fields", op.get("redact_fields")), f"{prefix}.{op_id}: operation/payload redaction differs")
    require(errors, len(op_ids) == len(set(op_ids)), f"{prefix}: duplicate operation IDs")
    required_groups = transaction.get("required_owner_groups", [])
    require(errors, set(required_groups) == touched_groups, f"{prefix}: required_owner_groups differs from touched owners")
    prepared_by_group: dict[str, dict[str, Any]] = {}
    for index, receipt in enumerate(prepared):
        if not isinstance(receipt, dict):
            errors.append(f"{prefix}.prepared.{index}: not an object")
            continue
        validate_record(receipt, "PREPARED_OWNER_RECEIPT_V2", field_rows, type_rows, f"{prefix}.prepared.{index}", errors)
        group = receipt.get("owner_group_id", "")
        require(errors, group not in prepared_by_group, f"{prefix}: duplicate prepared owner {group}")
        prepared_by_group[group] = receipt
        require(errors, receipt.get("proposal_hash") == transaction.get("proposal_hash"), f"{prefix}.{group}: prepared proposal hash differs")
        if receipt.get("status") == "prepared":
            require(errors, not receipt.get("rejected_operation_ids") and not receipt.get("reason_codes"), f"{prefix}.{group}: prepared receipt contains reject data")
    if set(prepared_by_group) == set(required_groups):
        for group in required_groups:
            receipt = prepared_by_group[group]
            expected_ops = [op["op_id"] for op in operations if op.get("owner_group_id") == group]
            require(errors, receipt.get("status") == "prepared", f"{prefix}.{group}: required owner did not prepare")
            require(errors, receipt.get("accepted_operation_ids") == expected_ops, f"{prefix}.{group}: accepted operation list differs")


def apply_operations(
    state: dict[str, Any],
    transaction: dict[str, Any],
    domain_rows: dict[str, dict[str, str]],
) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    touched_domains: set[str] = set()
    tx_id = transaction["transaction_group_id"]
    for op in transaction["operations"]:
        state_id = op["state_id"]
        record_id = op["record_id"]
        contract = domain_rows[state_id]
        if state_id not in updated["domains"]:
            updated["domains"][state_id] = {
                "state_id": state_id,
                "owner_system": contract["owner_system"],
                "owner_group_id": contract["owner_group_id"],
                "domain_version": 0,
                "records": {},
            }
            updated["domain_versions"][state_id] = 0
        records = updated["domains"][state_id]["records"]
        kind = op["op_kind"]
        payload = copy.deepcopy(op["payload"])
        if kind in {"OP_CREATE_RECORD", "OP_REPLACE_RECORD"}:
            record = payload
        else:
            record = copy.deepcopy(records[record_id])
            if kind == "OP_PATCH_RECORD":
                record.update(copy.deepcopy(payload["patch"]))
            elif kind == "OP_CLOSE_RECORD":
                record.update(copy.deepcopy(payload["status_or_resolution_patch"]))
                extensions = copy.deepcopy(record.get("extensions", {}))
                extensions["closed_reason"] = payload["closed_reason"]
                record["extensions"] = extensions
            elif kind == "OP_RESOURCE_DELTA":
                record.update(payload)
            elif kind == "OP_APPEND_EVENT":
                target = list(record[payload["list_field"]])
                target.append(copy.deepcopy(payload["event_value"]))
                record[payload["list_field"]] = target
            elif kind == "OP_TRANSFER_UNIQUE":
                record["lawful_owner"] = payload["lawful_owner"]
                record["current_holder"] = payload["to_current_holder"]
                record["physical_location"] = payload["to_physical_location"]
                record["loan_terms"] = copy.deepcopy(payload["loan_terms"])
                record["transfer_receipt_id"] = payload["transfer_receipt_id"]
                record["slot"] = payload["to_slot"]
                record["installed_state"] = payload["installed_state"]
            record["_record_version"] = op["to_version"]
            record["_last_transaction_id"] = tx_id
            record["_visibility_scope"] = op["visibility_scope"]
            record["_observer_ids"] = copy.deepcopy(op["observer_ids"])
            record["_redact_fields"] = copy.deepcopy(op["redact_fields"])
        records[record_id] = record
        touched_domains.add(state_id)
    for state_id in touched_domains:
        next_version = updated["domain_versions"].get(state_id, 0) + 1
        updated["domain_versions"][state_id] = next_version
        updated["domains"][state_id]["domain_version"] = next_version
    before_revision = updated["state_revision"]
    after_revision = before_revision + 1
    prepared_ids = [
        item["receipt_id"]
        for item in sorted(transaction["_prepared_receipts"], key=lambda item: item["owner_group_id"])
    ]
    commit_material = {
        "transaction_group_id": tx_id,
        "proposal_hash": transaction["proposal_hash"],
        "state_revision_before": before_revision,
        "state_revision_after": after_revision,
        "accepted_operation_ids": [op["op_id"] for op in transaction["operations"]],
        "prepared_owner_receipt_ids": prepared_ids,
    }
    receipt = {
        "receipt_id": f"RCPT_{tx_id}",
        "transaction_group_id": tx_id,
        "proposal_hash": transaction["proposal_hash"],
        "commit_hash": canonical_hash(commit_material),
        "state_revision_before": before_revision,
        "state_revision_after": after_revision,
        "accepted_operation_ids": commit_material["accepted_operation_ids"],
        "prepared_owner_receipt_ids": prepared_ids,
        "checkpoint_id": transaction["source_checkpoint_id"],
        "status": "accepted",
        "reason_codes": [],
        "player_summary": copy.deepcopy(transaction["player_summary"]),
    }
    updated["state_revision"] = after_revision
    updated["last_stable_checkpoint_id"] = transaction["source_checkpoint_id"]
    updated["transaction_ledger"][tx_id] = receipt
    updated["commit_order"].append(tx_id)
    return updated


def commit_reference(
    state: dict[str, Any],
    transaction: dict[str, Any],
    prepared: list[dict[str, Any]],
    field_rows: dict[str, dict[str, str]],
    type_rows: dict[str, dict[str, str]],
    domain_rows: dict[str, dict[str, str]],
    op_rows: dict[str, dict[str, str]],
) -> tuple[dict[str, Any], str, str, dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    tx_id = transaction.get("transaction_group_id", "")
    existing = state.get("transaction_ledger", {}).get(tx_id)
    if isinstance(existing, dict):
        if existing.get("proposal_hash") == transaction.get("proposal_hash"):
            return copy.deepcopy(state), "idempotent_replay", "already_committed", copy.deepcopy(existing), errors
        return copy.deepcopy(state), "rejected", "E_IDEMPOTENCY_CONFLICT", None, errors
    validate_transaction(state, transaction, prepared, field_rows, type_rows, domain_rows, op_rows, errors, tx_id or "transaction")
    if errors:
        return copy.deepcopy(state), "rejected", "E_CONTRACT_INVALID", None, errors
    if transaction["expected_state_revision"] != state["state_revision"]:
        return copy.deepcopy(state), "rejected", "E_STATE_REVISION_STALE", None, errors
    prepared_groups = {item["owner_group_id"] for item in prepared}
    required_groups = set(transaction["required_owner_groups"])
    if prepared_groups != required_groups:
        return copy.deepcopy(state), "rejected", "E_PREPARED_OWNER_MISSING", None, errors
    if any(item["status"] != "prepared" for item in prepared):
        return copy.deepcopy(state), "rejected", "E_OWNER_REJECTED", None, errors
    tx_for_apply = copy.deepcopy(transaction)
    tx_for_apply["_prepared_receipts"] = copy.deepcopy(prepared)
    updated = apply_operations(state, tx_for_apply, domain_rows)
    return updated, "accepted", "committed", copy.deepcopy(updated["transaction_ledger"][tx_id]), errors


def make_projection(state: dict[str, Any], receipt_id: str, knowledge_owner: str) -> dict[str, Any]:
    visible: dict[str, Any] = {}
    redacted: list[str] = []
    for state_id, bucket in state["domains"].items():
        for record_id, source_record in bucket["records"].items():
            scope = source_record["_visibility_scope"]
            observers = source_record["_observer_ids"]
            if scope == "backend_only" or (scope == "observer_set" and knowledge_owner not in observers):
                continue
            record = copy.deepcopy(source_record)
            for path in source_record["_redact_fields"]:
                if delete_at(record, path):
                    redacted.append(f"{state_id}.{record_id}.{path}")
            for meta_key in ["_record_version", "_last_transaction_id", "_source_authority", "_visibility_scope", "_observer_ids", "_redact_fields"]:
                record.pop(meta_key, None)
            visible.setdefault(state_id, {})[record_id] = record
    transaction_id = receipt_id.removeprefix("RCPT_")
    return {
        "projection_id": f"PROJ_{transaction_id}_{knowledge_owner}",
        "knowledge_owner": knowledge_owner,
        "source_state_revision": state["state_revision"],
        "visible_records": visible,
        "redacted_paths": sorted(redacted),
        "source_receipt_ids": [receipt_id],
        "detail_level": "standard",
        "accessibility_mode": "standard",
    }


def upgrade_legacy_equipment_fixture(
    state: dict[str, Any],
    transaction: dict[str, Any],
    prepared: list[dict[str, Any]],
) -> None:
    """Adapt the frozen v1 paper fixture to the explicit v2 physical-truth wire.

    The source JSON remains frozen evidence.  This in-memory adapter is narrow:
    it runs only when the fixture still carries the legacy ``owner`` field or
    the old ``from_owner/to_owner`` transfer payload.  It does not authorize a
    Runtime migration or fabricate user evidence.
    """

    records = (
        state.get("domains", {})
        .get("ST_EQUIPMENT", {})
        .get("records", {})
    )
    upgraded = False
    for record in records.values():
        if not isinstance(record, dict) or "owner" not in record:
            continue
        legacy_holder = record.pop("owner")
        record["lawful_owner"] = legacy_holder
        record["current_holder"] = legacy_holder
        record["physical_location"] = legacy_holder
        record["loan_terms"] = {}
        record["transfer_receipt_id"] = "NONE"
        upgraded = True

    for op in transaction.get("operations", []):
        if not isinstance(op, dict) or op.get("op_kind") != "OP_TRANSFER_UNIQUE":
            continue
        payload = op.get("payload", {})
        if not isinstance(payload, dict) or "from_owner" not in payload:
            continue
        current = current_record(state, "ST_EQUIPMENT", op.get("record_id", "")) or {}
        from_holder = payload.pop("from_owner")
        to_holder = payload.pop("to_owner")
        payload.update(
            {
                "lawful_owner": current.get("lawful_owner", from_holder),
                "from_current_holder": from_holder,
                "to_current_holder": to_holder,
                "from_physical_location": current.get("physical_location", from_holder),
                "to_physical_location": to_holder,
                "loan_terms": {"kind": "installed_by_current_holder"},
                "transfer_receipt_id": f"XFER_{op.get('op_id', 'LEGACY_FIXTURE')}",
            }
        )
        upgraded = True

    if not upgraded:
        return
    for op in transaction.get("operations", []):
        if not isinstance(op, dict):
            continue
        current = current_record(state, op.get("state_id", ""), op.get("record_id", ""))
        op["expected_record_hash"] = "NONE" if current is None else canonical_hash(current)
    transaction["proposal_hash"] = proposal_hash(transaction)
    for receipt in prepared:
        receipt["proposal_hash"] = transaction["proposal_hash"]


def fixture_expectation_path(path: str) -> str:
    legacy = "domains.ST_EQUIPMENT.records."
    if path.startswith(legacy) and path.endswith(".owner"):
        return f"{path[:-len('.owner')]}.current_holder"
    return path


def materialize_fixture(full_by_id: dict[str, dict[str, Any]], fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    if fixture["case_kind"] == "full":
        state = copy.deepcopy(fixture["before_state"])
        transaction = copy.deepcopy(fixture["transaction"])
        prepared = copy.deepcopy(fixture["prepared_receipts"])
    else:
        base = full_by_id[fixture["derives_from"]]
        state = copy.deepcopy(base["before_state"])
        transaction = copy.deepcopy(base["transaction"])
        prepared = copy.deepcopy(base["prepared_receipts"])
        fault = fixture["fault_injection"]
        if "remove_prepared_owner_group" in fault:
            prepared = [item for item in prepared if item["owner_group_id"] != fault["remove_prepared_owner_group"]]
        if "expected_state_revision" in fault:
            transaction["expected_state_revision"] = fault["expected_state_revision"]
            if fault.get("rebind_proposal_and_prepare_hashes") is True:
                transaction["proposal_hash"] = proposal_hash(transaction)
                for receipt in prepared:
                    receipt["proposal_hash"] = transaction["proposal_hash"]
    upgrade_legacy_equipment_fixture(state, transaction, prepared)
    return state, transaction, prepared


def observed_record_types(fixture: dict[str, Any], domain_rows: dict[str, dict[str, str]]) -> set[str]:
    base = {
        "RUN_STATE_V2",
        "WORLD_CLOCK_V2",
        "DOMAIN_BUCKET_V2",
        "DOMAIN_RECORD_META_V2",
        "STATE_TRANSACTION_V2",
        "STATE_OP_V2",
        "PREPARED_OWNER_RECEIPT_V2",
        "COMMIT_RECEIPT_V2",
        "PLAYER_PROJECTION_V2",
    }
    state_ids = set(fixture["before_state"]["domains"]) | {op["state_id"] for op in fixture["transaction"]["operations"]}
    return base | {domain_rows[state_id]["record_type"] for state_id in state_ids}


def validate_tables(
    type_rows_list: list[dict[str, str]],
    field_rows_list: list[dict[str, str]],
    domain_rows_list: list[dict[str, str]],
    op_rows_list: list[dict[str, str]],
    state_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
) -> tuple[list[str], dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    errors: list[str] = []
    type_rows = {row["type_id"]: row for row in type_rows_list}
    field_rows = {row["record_type"]: row for row in field_rows_list}
    domain_rows = {row["state_id"]: row for row in domain_rows_list}
    op_rows = {row["op_kind"]: row for row in op_rows_list}
    require(errors, len(type_rows_list) == len(type_rows) == EXPECTED_TYPE_COUNT, f"expected {EXPECTED_TYPE_COUNT} unique types")
    require(errors, len(field_rows_list) == len(field_rows) == EXPECTED_RECORD_TYPE_COUNT, f"expected {EXPECTED_RECORD_TYPE_COUNT} unique record types")
    require(errors, len(domain_rows_list) == len(domain_rows) == EXPECTED_DOMAIN_COUNT, f"expected {EXPECTED_DOMAIN_COUNT} unique domains")
    require(errors, len(op_rows_list) == len(op_rows) == EXPECTED_OP_COUNT, f"expected {EXPECTED_OP_COUNT} unique op kinds")
    for row in type_rows_list:
        require(errors, row["status"] == "candidate_runstate_v2_type_contract", f"{row['type_id']}: type status overclaims")
    for row in field_rows_list:
        require(errors, row["status"] == "candidate_runstate_v2_field_contract", f"{row['record_type']}: field status overclaims")
        try:
            signatures = {**parse_signature(row["required_fields_typed"]), **parse_signature(row["optional_fields_typed"])}
        except ValueError as error:
            errors.append(f"{row['record_type']}: {error}")
            continue
        for field, type_id in signatures.items():
            require(errors, type_id in type_rows, f"{row['record_type']}.{field}: unknown type {type_id}")
    state_by_id = {row["state_id"]: row for row in state_rows}
    require(errors, set(domain_rows) == set(state_by_id), "RunState v2 domains differ from system-state-contracts")
    owner_by_state: dict[str, str] = {}
    for owner in owner_rows:
        for state_id in split_values(owner["state_ids"]):
            require(errors, state_id not in owner_by_state, f"duplicate owner group for {state_id}")
            owner_by_state[state_id] = owner["owner_group_id"]
    require(errors, set(state_by_id) - set(owner_by_state) == EXCLUDED_OWNER_STATES, "owner exclusions differ from identity/UI only")
    for state_id, row in domain_rows.items():
        source = state_by_id.get(state_id)
        if source is None:
            continue
        require(errors, row["record_type"] in field_rows, f"{state_id}: record type missing")
        require(errors, row["owner_system"] == source["owner_system"], f"{state_id}: owner system differs from state contract")
        if state_id not in EXCLUDED_OWNER_STATES:
            require(errors, row["owner_group_id"] == owner_by_state.get(state_id), f"{state_id}: owner group differs from settlement contract")
        domain_schema = field_rows.get(row["record_type"])
        if domain_schema:
            try:
                typed_fields = set(parse_signature(domain_schema["required_fields_typed"]))
            except ValueError:
                typed_fields = set()
            require(errors, typed_fields == set(split_values(source["minimum_fields"])), f"{state_id}: typed fields differ from minimum_fields")
            require(errors, row["record_id_field"] in typed_fields, f"{state_id}: record_id_field not typed")
        require(errors, row["build_status"] == "zero_build" and row["human_evidence_status"] == "not_run", f"{state_id}: evidence boundary overclaims")
        require(errors, row["status"] == "candidate_runstate_v2_domain_contract", f"{state_id}: status overclaims")
        for kind in split_values(row["allowed_op_kinds"]):
            require(errors, kind in op_rows, f"{state_id}: unknown allowed op {kind}")
            if kind in op_rows:
                require(errors, state_id in split_values(op_rows[kind]["allowed_state_ids"]), f"{state_id}: op/domain reciprocity missing for {kind}")
    common_op_fields = set(parse_signature(field_rows["STATE_OP_V2"]["required_fields_typed"])) if "STATE_OP_V2" in field_rows else set()
    for kind, row in op_rows.items():
        require(errors, row["status"] == "candidate_state_transaction_v2_op_contract", f"{kind}: status overclaims")
        require(errors, set(split_values(row["required_op_fields"])) == common_op_fields, f"{kind}: common op field set differs")
        for state_id in split_values(row["allowed_state_ids"]):
            require(errors, state_id in domain_rows, f"{kind}: unknown state {state_id}")
            if state_id in domain_rows:
                require(errors, kind in split_values(domain_rows[state_id]["allowed_op_kinds"]), f"{kind}: domain/op reciprocity missing for {state_id}")

    relation_domain = domain_rows.get("ST_RELATION", {})
    relation_ops = set(split_values(relation_domain.get("allowed_op_kinds", "")))
    require(
        errors,
        {"OP_CREATE_RECORD", "OP_PATCH_RECORD", "OP_CLOSE_RECORD", "OP_APPEND_EVENT"} <= relation_ops,
        "ST_RELATION: protocol lifecycle create/patch/close/history path incomplete",
    )
    require(errors, "ST_RELATION" in split_values(op_rows.get("OP_PATCH_RECORD", {}).get("allowed_state_ids", "")), "ST_RELATION: protocol patch op missing")
    require(errors, "ST_RELATION" in split_values(op_rows.get("OP_CLOSE_RECORD", {}).get("allowed_state_ids", "")), "ST_RELATION: protocol retire op missing")
    relation_invariants = field_rows.get("DOMAIN_ST_RELATION_V2", {}).get("fixed_constraints", "")
    for token in ("candidate|training|available|paused|revised|retired", "supersedes_id", "same transaction group", "action consent remains separate"):
        require(errors, token in relation_invariants, f"ST_RELATION: protocol lifecycle invariant missing {token}")
    return errors, type_rows, field_rows, domain_rows, op_rows


def validate_package(
    type_rows_list: list[dict[str, str]],
    field_rows_list: list[dict[str, str]],
    domain_rows_list: list[dict[str, str]],
    op_rows_list: list[dict[str, str]],
    fixture_registry: list[dict[str, str]],
    payload: dict[str, Any],
    state_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
) -> list[str]:
    errors, type_rows, field_rows, domain_rows, op_rows = validate_tables(type_rows_list, field_rows_list, domain_rows_list, op_rows_list, state_rows, owner_rows)
    require(errors, payload.get("schema_id") == "runstate_v2_r0_p1_fixture_pack_v1", "fixture pack schema_id differs")
    require(errors, payload.get("authority_boundary") == EXPECTED_BOUNDARY, "fixture pack authority boundary differs")
    fixtures = payload.get("fixtures", [])
    fixture_by_id = {item.get("fixture_id"): item for item in fixtures if isinstance(item, dict)}
    require(errors, len(fixtures) == len(fixture_by_id) == 4, "expected four unique RunState fixtures")
    require(errors, set(fixture_by_id) == EXPECTED_FIXTURE_IDS, "RunState fixture ID set differs")
    registry_by_id = {row["fixture_id"]: row for row in fixture_registry}
    require(errors, len(fixture_registry) == len(registry_by_id) == 4, "expected four unique fixture coverage rows")
    require(errors, set(registry_by_id) == EXPECTED_FIXTURE_IDS, "fixture coverage ID set differs")
    full_by_id = {key: value for key, value in fixture_by_id.items() if value.get("case_kind") == "full"}
    require(errors, set(full_by_id) == {"FX-RS2-R0-ATOMIC", "FX-RS2-P1-C2-REDACTION"}, "full fixture set differs")
    stage_counts = {stage: sum(1 for item in fixtures if item.get("stage") == stage) for stage in ("R0", "P1")}
    require(errors, stage_counts == {"R0": 2, "P1": 2}, f"fixture stage distribution differs: {stage_counts}")
    for fixture_id, fixture in fixture_by_id.items():
        registry = registry_by_id.get(fixture_id)
        if registry is None:
            continue
        require(errors, fixture.get("stage") == registry["stage"], f"{fixture_id}: stage differs from registry")
        require(errors, fixture.get("case_kind") == registry["case_kind"], f"{fixture_id}: case kind differs from registry")
        require(errors, fixture.get("build_status") == registry["build_status"] == "zero_build", f"{fixture_id}: build boundary overclaims")
        require(errors, fixture.get("human_evidence_status") == registry["human_evidence_status"] == "not_run", f"{fixture_id}: human evidence overclaims")
        require(errors, registry["status"] == "candidate_runstate_v2_paper_fixture", f"{fixture_id}: registry status overclaims")
        require(errors, fixture.get("canonical_sha256") == fixture_hash(fixture), f"{fixture_id}: canonical fixture hash differs")
        require(errors, not contains_float(fixture), f"{fixture_id}: JSON float found")
        try:
            require(errors, json.loads(canonical_bytes(fixture).decode("utf-8")) == fixture, f"{fixture_id}: canonical round-trip differs")
        except (TypeError, ValueError) as error:
            errors.append(f"{fixture_id}: canonical serialization failed: {error}")
        if fixture.get("case_kind") == "full":
            require(errors, set(split_values(registry["record_types_covered"])) == observed_record_types(fixture, domain_rows), f"{fixture_id}: record type coverage differs")
            observed_states = set(fixture["before_state"]["domains"]) | {op["state_id"] for op in fixture["transaction"]["operations"]}
            require(errors, set(split_values(registry["state_domains_covered"])) == observed_states, f"{fixture_id}: state coverage differs")
            observed_ops = {op["op_kind"] for op in fixture["transaction"]["operations"]}
            require(errors, set(split_values(registry["op_kinds_covered"])) == observed_ops, f"{fixture_id}: op coverage differs")
        else:
            require(errors, registry["fixture_source"] == fixture.get("derives_from"), f"{fixture_id}: derived source differs")
            require(errors, registry["record_types_covered"] == registry["state_domains_covered"] == registry["op_kinds_covered"] == "INHERIT", f"{fixture_id}: derived coverage must inherit")
        if fixture.get("case_kind") == "derived_fault" and fixture.get("derives_from") not in full_by_id:
            errors.append(f"{fixture_id}: derived base missing or not full")
            continue
        state, transaction, prepared = materialize_fixture(full_by_id, fixture)
        validate_snapshot(state, field_rows, type_rows, domain_rows, errors, f"{fixture_id}.before_state")
        updated, status, reason, receipt, commit_errors = commit_reference(state, transaction, prepared, field_rows, type_rows, domain_rows, op_rows)
        errors.extend(f"{fixture_id}: {item}" for item in commit_errors)
        expected = fixture["expected"]
        require(errors, status == expected["commit_status"] == registry["expected_commit"], f"{fixture_id}: commit status differs")
        require(errors, reason == expected["reason_code"], f"{fixture_id}: reason code differs")
        require(errors, updated["state_revision"] == expected["state_revision_after"], f"{fixture_id}: revision differs")
        require(errors, updated["state_revision"] - state["state_revision"] == int(registry["expected_revision_delta"]), f"{fixture_id}: registry revision delta differs")
        if status == "accepted":
            require(errors, receipt is not None and receipt.get("receipt_id") == expected.get("receipt_id"), f"{fixture_id}: accepted receipt differs")
            validate_snapshot(updated, field_rows, type_rows, domain_rows, errors, f"{fixture_id}.after_state")
            for path, expected_value in expected.get("after_values", {}).items():
                adapted_path = fixture_expectation_path(path)
                try:
                    actual = value_at(updated, adapted_path)
                except (KeyError, IndexError, ValueError):
                    errors.append(f"{fixture_id}: after path missing {adapted_path}")
                else:
                    require(errors, actual == expected_value, f"{fixture_id}: after value differs at {adapted_path}")
            replayed, replay_status, _, replay_receipt, replay_errors = commit_reference(updated, transaction, prepared, field_rows, type_rows, domain_rows, op_rows)
            errors.extend(f"{fixture_id} replay: {item}" for item in replay_errors)
            require(errors, replay_status == expected.get("replay_status"), f"{fixture_id}: replay status differs")
            require(errors, replayed["state_revision"] == expected.get("replay_state_revision_after"), f"{fixture_id}: replay changed revision")
            require(errors, canonical_bytes(replayed) == canonical_bytes(updated), f"{fixture_id}: replay changed state bytes")
            require(errors, replay_receipt == receipt, f"{fixture_id}: replay receipt differs")
            projection = make_projection(updated, expected.get("receipt_id", "RCPT_UNEXPECTED"), expected.get("projection_knowledge_owner", "PLAYER"))
            validate_record(projection, "PLAYER_PROJECTION_V2", field_rows, type_rows, f"{fixture_id}.projection", errors)
            for path in expected.get("visible_paths", []):
                try:
                    value_at(projection, path)
                except (KeyError, IndexError, ValueError):
                    errors.append(f"{fixture_id}: visible projection path missing {path}")
            require(errors, projection["redacted_paths"] == expected.get("redacted_paths", []), f"{fixture_id}: redacted path set differs")
            projection_text = canonical_bytes(projection).decode("utf-8")
            for forbidden in expected.get("forbidden_projection_values", []):
                require(errors, forbidden not in projection_text, f"{fixture_id}: forbidden backend value leaked")
        else:
            require(errors, canonical_bytes(updated) == canonical_bytes(state), f"{fixture_id}: rejected transaction was not zero-write")
            for path in expected.get("unchanged_paths", []):
                adapted_path = fixture_expectation_path(path)
                try:
                    require(errors, value_at(updated, adapted_path) == value_at(state, adapted_path), f"{fixture_id}: rejected path changed {adapted_path}")
                except (KeyError, IndexError, ValueError):
                    errors.append(f"{fixture_id}: unchanged path missing {adapted_path}")
            if expected.get("accepted_receipt_absent"):
                require(errors, transaction["transaction_group_id"] not in updated["transaction_ledger"], f"{fixture_id}: rejected transaction created receipt")
    all_full_ops = {op["op_kind"] for fixture in full_by_id.values() for op in fixture["transaction"]["operations"]}
    require(errors, all_full_ops == set(op_rows), "R0/P1 full fixtures do not cover every transaction op kind")
    all_full_domains = {state_id for fixture in full_by_id.values() for state_id in (set(fixture["before_state"]["domains"]) | {op["state_id"] for op in fixture["transaction"]["operations"]})}
    require(errors, all_full_domains == {"ST_STORY", "ST_BODY", "ST_EQUIPMENT", "ST_RESOURCE", "ST_RESULT", "ST_CONTACT", "ST_CONSENT"}, "R0/P1 fixture domain coverage differs")
    return errors


def normalize_hashes(payload: dict[str, Any]) -> None:
    for fixture in payload["fixtures"]:
        if fixture["case_kind"] != "full":
            continue
        state = fixture["before_state"]
        for op in fixture["transaction"]["operations"]:
            current = current_record(state, op["state_id"], op["record_id"])
            op["expected_record_hash"] = "NONE" if current is None else canonical_hash(current)
        fixture["transaction"]["proposal_hash"] = proposal_hash(fixture["transaction"])
        for receipt in fixture["prepared_receipts"]:
            receipt["proposal_hash"] = fixture["transaction"]["proposal_hash"]
    for fixture in payload["fixtures"]:
        fixture["canonical_sha256"] = fixture_hash(fixture)


def run_self_test(
    type_rows: list[dict[str, str]],
    field_rows: list[dict[str, str]],
    domain_rows: list[dict[str, str]],
    op_rows: list[dict[str, str]],
    fixture_registry: list[dict[str, str]],
    payload: dict[str, Any],
    state_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
) -> tuple[int, int]:
    cases: list[tuple[str, Any]] = []

    def mutation(name: str, edit: Any, *, normalize: bool = False) -> None:
        types = copy.deepcopy(type_rows)
        fields = copy.deepcopy(field_rows)
        domains = copy.deepcopy(domain_rows)
        ops = copy.deepcopy(op_rows)
        registry = copy.deepcopy(fixture_registry)
        fixtures = copy.deepcopy(payload)
        edit(types, fields, domains, ops, registry, fixtures)
        if normalize:
            normalize_hashes(fixtures)
        cases.append((name, (types, fields, domains, ops, registry, fixtures, state_rows, owner_rows)))

    mutation("unknown field type", lambda t, f, d, o, r, p: next(x for x in f if x["record_type"] == "RUN_STATE_V2").__setitem__("optional_fields_typed", "extensions:T_UNKNOWN"))
    mutation("domain owner drift", lambda t, f, d, o, r, p: next(x for x in d if x["state_id"] == "ST_BODY").__setitem__("owner_group_id", "SOG-NARR"))
    mutation("typed state field removed", lambda t, f, d, o, r, p: next(x for x in f if x["record_type"] == "DOMAIN_ST_CONTACT_V2").__setitem__("required_fields_typed", next(x for x in f if x["record_type"] == "DOMAIN_ST_CONTACT_V2")["required_fields_typed"].replace(";confidence:T_RATIO_STR", "")))
    mutation("op reciprocity drift", lambda t, f, d, o, r, p: next(x for x in o if x["op_kind"] == "OP_RESOURCE_DELTA").__setitem__("allowed_state_ids", "ST_RESULT"))
    mutation("JSON float", lambda t, f, d, o, r, p: next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-P1-C2-REDACTION")["before_state"]["world_clock"].__setitem__("elapsed_ms", 24000.0))
    mutation("proposal hash drift", lambda t, f, d, o, r, p: next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-P1-C2-REDACTION")["transaction"].__setitem__("proposal_hash", "0" * 64))
    mutation("missing prepared owner", lambda t, f, d, o, r, p: next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-R0-ATOMIC").__setitem__("prepared_receipts", next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-R0-ATOMIC")["prepared_receipts"][:-1]), normalize=True)
    mutation("wrong owner operation", lambda t, f, d, o, r, p: next(x for x in next(y for y in p["fixtures"] if y["fixture_id"] == "FX-RS2-P1-C2-REDACTION")["prepared_receipts"] if x["owner_group_id"] == "SOG-C2").__setitem__("accepted_operation_ids", ["TEST_OP_P1_BANDWIDTH_DELTA"]), normalize=True)
    def leak_edit(t: Any, f: Any, d: Any, o: Any, r: Any, p: Any) -> None:
        fixture = next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-P1-C2-REDACTION")
        op = next(x for x in fixture["transaction"]["operations"] if x["op_id"] == "TEST_OP_P1_CONTACT_REPLACE")
        op["redact_fields"] = []
        op["payload"]["_redact_fields"] = []
    mutation("backend projection leak", leak_edit, normalize=True)
    mutation("resource arithmetic", lambda t, f, d, o, r, p: next(x for x in next(y for y in p["fixtures"] if y["fixture_id"] == "FX-RS2-R0-ATOMIC")["transaction"]["operations"] if x["op_kind"] == "OP_RESOURCE_DELTA")["payload"].__setitem__("balance_after", "2"), normalize=True)
    mutation("idempotency key drift", lambda t, f, d, o, r, p: next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-R0-ATOMIC")["transaction"].__setitem__("idempotency_key", "TEST_OTHER_KEY"), normalize=True)
    mutation("unknown root field", lambda t, f, d, o, r, p: next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-R0-ATOMIC")["before_state"].__setitem__("legacy_world_facts", {}), normalize=True)
    mutation("duplicate operation id", lambda t, f, d, o, r, p: next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-R0-ATOMIC")["transaction"]["operations"][1].__setitem__("op_id", "TEST_OP_R0_STORY_CREATE"), normalize=True)
    mutation("evidence promotion", lambda t, f, d, o, r, p: next(x for x in p["fixtures"] if x["fixture_id"] == "FX-RS2-R0-ATOMIC").__setitem__("build_status", "built"))
    mutation("expected revision overclaim", lambda t, f, d, o, r, p: next(x for x in r if x["fixture_id"] == "FX-RS2-P1-STALE-REVISION").__setitem__("expected_revision_delta", "1"))

    rejected = 0
    for name, values in cases:
        case_errors = validate_package(*values)
        if case_errors:
            rejected += 1
        else:
            print(f"[d03-runstate-v2:self-test] FAIL mutation escaped: {name}")
    return rejected, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run in-memory fault injections after baseline validation")
    parser.add_argument("--print-hashes", action="store_true", help="print normalized static hashes without writing files")
    args = parser.parse_args()
    type_rows = read_tsv(TYPE_PATH)
    field_rows = read_tsv(FIELD_PATH)
    domain_rows = read_tsv(DOMAIN_PATH)
    op_rows = read_tsv(OP_PATH)
    fixture_registry = read_tsv(FIXTURE_REGISTRY_PATH)
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    state_rows = read_tsv(STATE_CONTRACT_PATH)
    owner_rows = read_tsv(OWNER_PATH)
    if args.print_hashes:
        normalized = copy.deepcopy(payload)
        normalize_hashes(normalized)
        for fixture in normalized["fixtures"]:
            print(f"{fixture['fixture_id']} canonical_sha256={fixture['canonical_sha256']}")
            if fixture["case_kind"] == "full":
                print(f"{fixture['fixture_id']} proposal_hash={fixture['transaction']['proposal_hash']}")
                for op in fixture["transaction"]["operations"]:
                    print(f"{fixture['fixture_id']} {op['op_id']} expected_record_hash={op['expected_record_hash']}")
        return 0
    errors = validate_package(type_rows, field_rows, domain_rows, op_rows, fixture_registry, payload, state_rows, owner_rows)
    if errors:
        for error in errors:
            print(f"[d03-runstate-v2] FAIL {error}")
        print(f"[d03-runstate-v2] RESULT FAIL errors={len(errors)}")
        return 1
    if args.self_test:
        rejected, total = run_self_test(type_rows, field_rows, domain_rows, op_rows, fixture_registry, payload, state_rows, owner_rows)
        if rejected != total:
            print(f"[d03-runstate-v2:self-test] RESULT FAIL rejected={rejected}/{total}")
            return 1
        print(f"[d03-runstate-v2:self-test] PASS rejected={rejected}/{total} injected faults")
    print(
        "D03 RunState v2 PASS: 47 types, 35 typed record schemas, 26 state domains, "
        "7 transaction op kinds, 4 R0/P1 paper fixtures (2 accepted + replay, 2 rejected zero-write); "
        "zero Build/human evidence"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"D03 RunState v2 FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
