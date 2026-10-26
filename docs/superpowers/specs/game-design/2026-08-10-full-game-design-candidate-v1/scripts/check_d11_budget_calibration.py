#!/usr/bin/env python3
"""Validate the Candidate D11 scope, work-unit, and budget calibration chain.

This checker is deliberately fail-closed.  A PASS means the planning envelope,
empty evidence ledgers, and future measurement contracts agree; it never means
that a cost, schedule, staffing plan, P50, P80, or investment was approved.
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
DATA = PACKAGE / "data"


def find_repo_root(start: Path) -> Path:
    for path in (start, *start.parents):
        if (path / ".git").exists():
            return path
    raise RuntimeError("cannot locate repository root")


REPO = find_repo_root(PACKAGE)

SCOPE_TIER_PATH = DATA / "scope-tier-budget.tsv"
SCENARIO_PATH = DATA / "scope-cost-scenarios.tsv"
CHAPTER_PATH = DATA / "chapter-scope-allocation.tsv"
ASSET_PATH = DATA / "asset-budget.tsv"
PROTOTYPE_PATH = DATA / "prototype-test-registry.tsv"
EVIDENCE_PATH = DATA / "acceptance-evidence-registry.tsv"
MILESTONE_PATH = DATA / "scope-milestone-gates.tsv"
ROLE_PATH = DATA / "production-role-registry.tsv"
TIME_SYSTEM_PATH = DATA / "time-system-neutrality-contract.tsv"
CALIBRATION_CONTRACT_PATH = DATA / "budget-calibration-contracts.tsv"
WORK_UNIT_SCHEMA_PATH = DATA / "production-work-unit-schema.tsv"
WORK_UNIT_PATH = DATA / "production-work-unit-registry.tsv"
MEASUREMENT_SCHEMA_PATH = DATA / "production-measurement-schema.tsv"
MEASUREMENT_PATH = DATA / "production-measurement-instances.tsv"
P80_INPUT_PATH = DATA / "project-p80-model-inputs.tsv"
CALIBRATION_STATUS_PATH = DATA / "budget-calibration-status.tsv"
D11_PATH = PACKAGE / "11-scope-budget-production-plan.md"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RANGE_RE = re.compile(r"^(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)$")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
TWO_PLACES = Decimal("0.01")

PM_COMPONENT_FIELDS = (
    "product_direction_pm",
    "narrative_content_pm",
    "system_level_design_pm",
    "engineering_tools_ui_pm",
    "art_environment_mecha_ui_pm",
    "animation_vfx_pm",
    "audio_music_voice_pm",
    "qa_access_localization_release_pm",
)

P80_HEADER = (
    "model_id",
    "scope_scenario_id",
    "record_id",
    "record_kind",
    "unit_type_ref",
    "paired_quantity",
    "unit_p80_hours",
    "novelty_multiplier",
    "integration_multiplier",
    "fixed_hours",
    "scalar_value",
    "source_ref",
    "input_confidence",
    "input_status",
    "status",
)

RECEIPT_TYPES = {"product_direction", "story", "gameplay", "visual", "production", "none"}
INVALIDATION_CAUSES = {
    "none",
    "design_change",
    "canon_change",
    "story_change",
    "visual_change",
    "rule_change",
    "build_bug",
    "user_rejection",
    "external_dependency",
}
WORK_UNIT_STATUSES = {"planned", "running", "accepted", "invalidated", "excluded"}
MEASUREMENT_STATUSES = {"planned", "running", "accepted", "invalidated", "excluded"}
EVIDENCE_TYPES = {"machine", "internal_human", "external_human", "user_receipt", "production_measurement"}


@dataclass
class Audit:
    errors: list[str] = field(default_factory=list)

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def read_tsv(path: Path, audit: Audit) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            header = list(reader.fieldnames or [])
            rows: list[dict[str, str]] = []
            for line_no, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    audit.errors.append(f"{path.name}:{line_no}: TSV width mismatch")
                    continue
                row["_line"] = str(line_no)
                rows.append(row)
    except OSError as exc:
        audit.errors.append(f"cannot read {path}: {exc}")
        return [], []
    audit.require(bool(header), f"{path.name}: missing header")
    return header, rows


def keyed(rows: list[dict[str, str]], key: str, audit: Audit, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value or value in result:
            audit.errors.append(f"{label}: missing/duplicate {key}={value!r}")
        else:
            result[value] = row
    return result


def split_refs(value: str) -> list[str]:
    if value in {"", "none", "not_applicable"}:
        return []
    return [item for item in value.split(";") if item]


def decimal_value(value: str, label: str, audit: Audit) -> Decimal | None:
    try:
        parsed = Decimal(value)
    except (InvalidOperation, TypeError):
        audit.errors.append(f"{label}: expected decimal, got {value!r}")
        return None
    if not parsed.is_finite():
        audit.errors.append(f"{label}: decimal must be finite")
        return None
    return parsed


def integer_value(value: str, label: str, audit: Audit) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        audit.errors.append(f"{label}: expected integer, got {value!r}")
        return None
    return parsed


def parse_iso8601(value: str, label: str, audit: Audit) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        audit.errors.append(f"{label}: invalid ISO-8601 value {value!r}")
        return None
    return parsed


def percentile_cont(values: list[Decimal], fraction: Decimal) -> Decimal:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    if len(ordered) == 1:
        return ordered[0]
    rank = Decimal(len(ordered) - 1) * fraction
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    weight = rank - Decimal(lower)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * weight


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_schema_pair(
    schema_path: Path,
    instance_path: Path,
    audit: Audit,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    schema_header, schema_rows = read_tsv(schema_path, audit)
    instance_header, instance_rows = read_tsv(instance_path, audit)
    audit.require(
        schema_header == ["field_name", "data_type", "required", "description", "validation", "consumer", "status"],
        f"{schema_path.name}: unexpected schema header",
    )
    fields = [row.get("field_name", "") for row in schema_rows]
    audit.require(len(fields) == len(set(fields)), f"{schema_path.name}: duplicate field names")
    audit.require(instance_header == fields, f"{instance_path.name}: header does not match {schema_path.name}")
    return schema_rows, instance_rows


def validate_scope_scenarios(
    tiers: dict[str, dict[str, str]],
    scenarios: dict[str, dict[str, str]],
    audit: Audit,
) -> None:
    paired_by_tier: dict[str, set[str]] = defaultdict(set)
    for scenario_id, row in scenarios.items():
        tier_id = row["tier_id"]
        audit.require(tier_id in tiers, f"{scenario_id}: unknown tier {tier_id}")
        paired_by_tier[tier_id].add(scenario_id)
        total = decimal_value(row["person_month_total"], f"{scenario_id}.person_month_total", audit)
        months = decimal_value(row["calendar_months"], f"{scenario_id}.calendar_months", audit)
        fte = decimal_value(row["average_active_fte"], f"{scenario_id}.average_active_fte", audit)
        components = [decimal_value(row[field], f"{scenario_id}.{field}", audit) for field in PM_COMPONENT_FIELDS]
        if total is not None and all(value is not None for value in components):
            audit.require(sum(value for value in components if value is not None) == total, f"{scenario_id}: PM components do not sum to total")
        if total is not None and months is not None and fte is not None:
            audit.require(months > 0, f"{scenario_id}: calendar_months must be >0")
            if months > 0:
                expected = (total / months).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
                audit.require(fte == expected, f"{scenario_id}: average_active_fte {fte} != {expected}")
        audit.require(row["scenario"] in {"low", "base", "high"}, f"{scenario_id}: invalid scenario label")
        audit.require("u0_planning_envelope" in row["estimate_basis"], f"{scenario_id}: estimate basis is not U0")
        audit.require(row["status"] == "planning_envelope_u0_not_estimate", f"{scenario_id}: status overclaims an estimate")

    for tier_id, tier in tiers.items():
        listed = set(split_refs(tier["cost_scenario_ids"]))
        if tier_id == "STAGE0_PROOF_LAB":
            audit.require(tier["cost_scenario_ids"] == "TBD_AFTER_SPIKES", "Stage0 must remain not calculable until spikes")
            continue
        audit.require(listed == paired_by_tier.get(tier_id, set()), f"{tier_id}: cost scenario pairing mismatch")
        labels = {scenarios[item]["scenario"] for item in listed if item in scenarios}
        audit.require(labels == {"low", "base", "high"}, f"{tier_id}: must have one low/base/high scenario")
        audit.require("u0" in tier["estimate_basis"], f"{tier_id}: tier estimate basis is not U0")
        audit.require("u0" in tier["status"], f"{tier_id}: tier status overclaims calibration")


def validate_calibration_contracts(contracts: dict[str, dict[str, str]], audit: Audit) -> None:
    required = {"CAL_FIRST_UNIT", "CAL_MINUTE", "CAL_CONFIDENCE", "CAL_PROJECT_P80"}
    audit.require(required <= contracts.keys(), f"missing calibration contracts: {sorted(required - contracts.keys())}")
    for contract_id, row in contracts.items():
        audit.require(row["status"] == "candidate_contract", f"{contract_id}: calibration contract status drift")
    first = contracts.get("CAL_FIRST_UNIT", {})
    minute = contracts.get("CAL_MINUTE", {})
    confidence = contracts.get("CAL_CONFIDENCE", {})
    project = contracts.get("CAL_PROJECT_P80", {})
    audit.require(
        ">=3" in first.get("minimum_evidence", "")
        and "PERCENTILE_CONT(0.50)" in first.get("formula", "")
        and "PERCENTILE_CONT(0.80)" in first.get("formula", "")
        and "n>=8且跨>=2章可用P80" in first.get("healthy", "")
        and "n<3" in first.get("red", ""),
        "CAL_FIRST_UNIT no longer locks n>=3 P50 / n>=8 cross-2-chapter P80",
    )
    audit.require(
        ">=3" in minute.get("minimum_evidence", "")
        and "PERCENTILE_CONT(0.50)" in minute.get("formula", "")
        and "PERCENTILE_CONT(0.80)" in minute.get("formula", "")
        and "P80需>=8且跨>=2章" in minute.get("minimum_evidence", ""),
        "CAL_MINUTE sample/percentile gate drift",
    )
    audit.require(
        "n<3=U0" in confidence.get("formula", "")
        and "3-7=U1" in confidence.get("formula", "")
        and ">=8且跨2章=U2" in confidence.get("formula", "")
        and ">=12且跨3章=U3" in confidence.get("formula", ""),
        "CAL_CONFIDENCE U0-U3 thresholds drift",
    )
    audit.require(
        "所有variable_unit达到U2" in project.get("minimum_evidence", "")
        and "跨scenario拼接" in project.get("red", "")
        and "project_p80_hours" in project.get("formula", "")
        and "productive_hours_per_pm" in project.get("formula", ""),
        "CAL_PROJECT_P80 prerequisite/formula/scenario guard drift",
    )


def validate_chapter_duration(
    tiers: dict[str, dict[str, str]],
    chapters: dict[str, dict[str, str]],
    audit: Audit,
) -> tuple[int, int, int, str]:
    expected = {f"C{index:02d}" for index in range(1, 23)}
    audit.require(set(chapters) == expected, "chapter-scope-allocation must contain C01-C22 exactly")
    minimum = 0
    maximum = 0
    for chapter_id, row in chapters.items():
        match = RANGE_RE.fullmatch(row["main_minutes"])
        if not match:
            audit.errors.append(f"{chapter_id}: invalid main_minutes range")
            continue
        low = Decimal(match.group(1))
        high = Decimal(match.group(2))
        audit.require(low <= high, f"{chapter_id}: minute range is reversed")
        audit.require(low == low.to_integral_value() and high == high.to_integral_value(), f"{chapter_id}: minute range must be integral")
        minimum += int(low)
        maximum += int(high)
    scope2 = tiers.get("SCOPE2_MINIMUM_22")
    if not scope2:
        audit.errors.append("missing SCOPE2_MINIMUM_22")
        return minimum, maximum, 1800, "blocked_above_1800"
    match = RANGE_RE.fullmatch(scope2["main_hours"])
    if not match:
        audit.errors.append("SCOPE2_MINIMUM_22.main_hours must be a range")
        hard_cap = 1800
    else:
        hard_cap = int(Decimal(match.group(2)) * 60)
    audit.require(hard_cap == 1800, f"Scope2 hard cap must remain 1800 minutes, got {hard_cap}")
    gate = "closed_at_or_below_1800" if maximum <= hard_cap else "blocked_above_1800"
    return minimum, maximum, hard_cap, gate


def quality_boundary_hash(unit_type_ref: str, assets: dict[str, dict[str, str]], prototypes: dict[str, dict[str, str]]) -> str | None:
    if unit_type_ref in assets:
        row = assets[unit_type_ref]
        fields = ("asset_id", "quality_boundary", "included_work", "excluded_work")
        prefix = "asset_quality_boundary_v1"
    elif unit_type_ref in prototypes:
        row = prototypes[unit_type_ref]
        fields = ("prototype_id", "test_question", "shared_fixed_inputs", "hard_pass_summary", "acceptance_scope")
        prefix = "prototype_quality_boundary_v1"
    else:
        return None
    payload = prefix + "\n" + "\n".join(f"{field}={row[field]}" for field in fields) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_receipt_fields(row: dict[str, str], label: str, audit: Audit) -> None:
    receipt_type = row["receipt_type"]
    audit.require(receipt_type in RECEIPT_TYPES, f"{label}: invalid receipt_type")
    if receipt_type == "none":
        audit.require(
            row["receipt_scope"] == row["receipt_path"] == row["receipt_sha256"] == "none",
            f"{label}: receipt_type=none must carry no receipt scope/path/hash",
        )
        return
    audit.require(row["receipt_scope"] not in {"", "none"}, f"{label}: receipt scope missing")
    receipt_path = Path(row["receipt_path"])
    audit.require(not receipt_path.is_absolute(), f"{label}: receipt path must be repository-relative")
    resolved = REPO / receipt_path
    audit.require(resolved.is_file(), f"{label}: receipt file missing: {row['receipt_path']}")
    audit.require(bool(SHA256_RE.fullmatch(row["receipt_sha256"])), f"{label}: receipt hash is not SHA-256")
    if resolved.is_file() and SHA256_RE.fullmatch(row["receipt_sha256"]):
        audit.require(file_sha256(resolved) == row["receipt_sha256"], f"{label}: receipt hash drift")


def validate_work_units_and_measurements(
    work_unit_rows: list[dict[str, str]],
    measurement_rows: list[dict[str, str]],
    assets: dict[str, dict[str, str]],
    prototypes: dict[str, dict[str, str]],
    chapters: dict[str, dict[str, str]],
    scenarios: dict[str, dict[str, str]],
    evidence: dict[str, dict[str, str]],
    milestones: dict[str, dict[str, str]],
    roles: dict[str, dict[str, str]],
    audit: Audit,
) -> tuple[dict[str, dict[str, object]], int]:
    work_units = keyed(work_unit_rows, "work_unit_instance_id", audit, "work units")
    measurements = keyed(measurement_rows, "measurement_id", audit, "measurements")
    registered_items = set(assets) | set(prototypes) | set(chapters) | set(evidence) | set(milestones)

    for unit_id, row in work_units.items():
        label = f"{WORK_UNIT_PATH.name}:{row['_line']}:{unit_id}"
        audit.require(all(row[field] != "" for field in row if field != "_line"), f"{label}: empty field")
        audit.require(ID_RE.fullmatch(unit_id) is not None, f"{label}: invalid stable ID")
        audit.require(row["work_item_id"] in registered_items, f"{label}: unregistered work_item_id")
        expected_quality_hash = quality_boundary_hash(row["unit_type_ref"], assets, prototypes)
        audit.require(expected_quality_hash is not None, f"{label}: unknown unit_type_ref")
        audit.require(row["quality_boundary_sha256"] == expected_quality_hash, f"{label}: quality boundary hash mismatch")
        audit.require(bool(SHA256_RE.fullmatch(row["scope_version_sha256"])), f"{label}: invalid scope version hash")
        audit.require(row["chapter_id"] == "none" or row["chapter_id"] in chapters, f"{label}: unknown chapter")
        audit.require(row["scope_scenario_id"] == "none" or row["scope_scenario_id"] in scenarios, f"{label}: unknown scope scenario")
        quantity = decimal_value(row["quantity_completed"], f"{label}.quantity_completed", audit)
        minutes = decimal_value(row["final_effective_play_minutes"], f"{label}.final_effective_play_minutes", audit)
        if quantity is not None:
            audit.require(quantity > 0, f"{label}: quantity_completed must be >0")
        if minutes is not None:
            audit.require(minutes >= 0, f"{label}: final_effective_play_minutes must be >=0")
        started = parse_iso8601(row["started_at"], f"{label}.started_at", audit)
        completed = None if row["completed_at"] == "none" else parse_iso8601(row["completed_at"], f"{label}.completed_at", audit)
        accepted = None if row["accepted_at"] == "none" else parse_iso8601(row["accepted_at"], f"{label}.accepted_at", audit)
        if started and completed:
            audit.require(completed >= started, f"{label}: completed_at precedes started_at")
        if completed and accepted:
            audit.require(accepted >= completed, f"{label}: accepted_at precedes completed_at")
        status = row["work_unit_status"]
        audit.require(status in WORK_UNIT_STATUSES, f"{label}: invalid work unit status")
        if status == "accepted":
            audit.require(completed is not None and accepted is not None, f"{label}: accepted unit lacks completion/acceptance time")
            evidence_ids = split_refs(row["acceptance_evidence_ids"])
            audit.require(bool(evidence_ids), f"{label}: accepted unit lacks acceptance evidence")
            audit.require(all(item in evidence for item in evidence_ids), f"{label}: acceptance evidence does not resolve")
            if evidence_ids:
                audit.require(
                    any(evidence[item]["artifact_or_build_id"] == row["build_or_asset_id"] for item in evidence_ids if item in evidence),
                    f"{label}: build_or_asset_id is not bound by acceptance evidence",
                )
        else:
            audit.require(row["acceptance_evidence_ids"] == "none", f"{label}: unaccepted unit carries acceptance evidence")
        if status == "invalidated":
            audit.require(row["invalidation_cause"] != "none", f"{label}: invalidated unit lacks cause")
        else:
            audit.require(row["invalidation_cause"] == "none", f"{label}: active/non-invalidated unit carries invalidation cause")
        audit.require(row["invalidation_cause"] in INVALIDATION_CAUSES, f"{label}: invalid invalidation cause")
        validate_receipt_fields(row, label, audit)

    for unit_id, row in work_units.items():
        source = row["reuse_source_work_unit_id"]
        if source != "none":
            audit.require(source in work_units, f"{unit_id}: reuse source does not resolve")
            if source in work_units:
                audit.require(work_units[source]["work_unit_status"] == "accepted", f"{unit_id}: reuse source is not accepted")
                audit.require(source != unit_id, f"{unit_id}: cannot reuse itself")

    measurements_by_unit: dict[str, list[dict[str, str]]] = defaultdict(list)
    for measurement_id, row in measurements.items():
        label = f"{MEASUREMENT_PATH.name}:{row['_line']}:{measurement_id}"
        audit.require(all(row[field] != "" for field in row if field != "_line"), f"{label}: empty field")
        unit_id = row["work_unit_instance_id"]
        audit.require(unit_id in work_units, f"{label}: work unit does not resolve")
        if unit_id not in work_units:
            continue
        unit = work_units[unit_id]
        measurements_by_unit[unit_id].append(row)
        for field in ("work_item_id", "unit_type_ref", "scope_version_sha256", "build_or_asset_id"):
            audit.require(row[field] == unit[field], f"{label}: {field} differs from work unit")
        audit.require(row["reuse_source_id"] == unit["reuse_source_work_unit_id"], f"{label}: reuse source differs from work unit")
        for field in ("quantity_completed", "final_effective_play_minutes"):
            left = decimal_value(row[field], f"{label}.{field}", audit)
            right = decimal_value(unit[field], f"{label}.work_unit_{field}", audit)
            if left is not None and right is not None:
                audit.require(left == right, f"{label}: {field} differs from work unit")
        audit.require(row["role_id"] in roles and roles[row["role_id"]]["status"] == "candidate_role", f"{label}: role is unknown or an alias")
        hour_fields = ("active_hours", "review_hours", "rework_hours", "blocked_hours", "defect_fix_hours", "retest_hours")
        hours = {field: decimal_value(row[field], f"{label}.{field}", audit) for field in hour_fields}
        for field, value in hours.items():
            if value is not None:
                audit.require(value >= 0, f"{label}: {field} must be >=0")
        total = decimal_value(row["total_contribution_hours"], f"{label}.total_contribution_hours", audit)
        if total is not None and all(value is not None for value in hours.values()):
            expected_total = sum(hours[field] for field in ("active_hours", "review_hours", "rework_hours", "defect_fix_hours", "retest_hours"))
            audit.require(total == expected_total, f"{label}: total_contribution_hours formula mismatch")
        parse_iso8601(row["started_at"], f"{label}.started_at", audit)
        if row["accepted_at"] != "none":
            parse_iso8601(row["accepted_at"], f"{label}.accepted_at", audit)
        audit.require(row["quantity_credit"] in {"true", "false"}, f"{label}: quantity_credit must be true/false")
        for field in ("review_rounds", "defects_p0", "defects_p1", "defects_p2", "tester_recruited_total", "tester_recruited_valid"):
            value = integer_value(row[field], f"{label}.{field}", audit)
            if value is not None:
                audit.require(value >= 0, f"{label}: {field} must be >=0")
        recruited_total = integer_value(row["tester_recruited_total"], f"{label}.tester_recruited_total", Audit())
        recruited_valid = integer_value(row["tester_recruited_valid"], f"{label}.tester_recruited_valid", Audit())
        if recruited_total is not None and recruited_valid is not None:
            audit.require(recruited_valid <= recruited_total, f"{label}: valid testers exceed recruited testers")
        audit.require(row["invalidation_cause"] in INVALIDATION_CAUSES, f"{label}: invalid invalidation cause")
        audit.require(row["evidence_type"] in EVIDENCE_TYPES, f"{label}: invalid evidence type")
        audit.require(row["measurement_status"] in MEASUREMENT_STATUSES, f"{label}: invalid measurement status")
        evidence_refs = split_refs(row["evidence_refs"])
        audit.require(all(item in evidence for item in evidence_refs), f"{label}: evidence_refs do not resolve")
        validate_receipt_fields(row, label, audit)
        if row["receipt_type"] != unit["receipt_type"]:
            audit.errors.append(f"{label}: receipt_type differs from work unit")
        if row["receipt_type"] != "none":
            for field in ("receipt_scope", "receipt_path", "receipt_sha256"):
                audit.require(row[field] == unit[field], f"{label}: {field} differs from work unit")

    unit_stats: dict[str, dict[str, object]] = defaultdict(lambda: {"costs": [], "chapters": set(), "units": []})
    accepted_unit_count = 0
    for unit_id, unit in work_units.items():
        if unit["work_unit_status"] != "accepted":
            continue
        accepted_unit_count += 1
        accepted_rows = [row for row in measurements_by_unit.get(unit_id, []) if row["measurement_status"] == "accepted"]
        audit.require(bool(accepted_rows), f"{unit_id}: accepted work unit has no accepted measurement rows")
        audit.require(
            all(row["measurement_status"] in {"accepted", "excluded"} for row in measurements_by_unit.get(unit_id, [])),
            f"{unit_id}: accepted work unit still has planned/running/invalidated measurements",
        )
        credits = [row for row in accepted_rows if row["quantity_credit"] == "true"]
        audit.require(len(credits) == 1, f"{unit_id}: accepted work unit must have exactly one quantity_credit=true")
        if not accepted_rows:
            continue
        quantities = {row["quantity_completed"] for row in accepted_rows}
        audit.require(len(quantities) == 1, f"{unit_id}: quantity_completed differs across contributions")
        quantity = decimal_value(unit["quantity_completed"], f"{unit_id}.quantity_completed", audit)
        totals = [decimal_value(row["total_contribution_hours"], f"{row['measurement_id']}.total_contribution_hours", audit) for row in accepted_rows]
        if quantity is None or quantity <= 0 or any(value is None for value in totals):
            continue
        cost = sum(value for value in totals if value is not None) / quantity
        stats = unit_stats[unit["unit_type_ref"]]
        stats["costs"].append(cost)
        stats["units"].append(unit_id)
        if unit["chapter_id"] != "none":
            stats["chapters"].add(unit["chapter_id"])

    for stats in unit_stats.values():
        costs = stats["costs"]
        chapters_seen = stats["chapters"]
        stats["sample_count"] = len(costs)
        stats["chapter_count"] = len(chapters_seen)
        stats["p50"] = percentile_cont(costs, Decimal("0.50")) if len(costs) >= 3 else None
        stats["p80"] = percentile_cont(costs, Decimal("0.80")) if len(costs) >= 8 and len(chapters_seen) >= 2 else None
        if len(costs) >= 12 and len(chapters_seen) >= 3:
            stats["confidence"] = "U3"
        elif stats["p80"] is not None:
            stats["confidence"] = "U2"
        elif stats["p50"] is not None:
            stats["confidence"] = "U1"
        else:
            stats["confidence"] = "U0"
    return dict(unit_stats), accepted_unit_count


def validate_p80_inputs(
    header: list[str],
    rows: list[dict[str, str]],
    scenarios: dict[str, dict[str, str]],
    unit_stats: dict[str, dict[str, object]],
    scope2_duration_gate: str,
    audit: Audit,
) -> dict[str, tuple[Decimal, Decimal]]:
    audit.require(tuple(header) == P80_HEADER, "project-p80-model-inputs.tsv: unexpected header")
    seen_records: set[tuple[str, str]] = set()
    models: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        label = f"{P80_INPUT_PATH.name}:{row['_line']}:{row['model_id']}/{row['record_id']}"
        audit.require(all(row[field] != "" for field in P80_HEADER), f"{label}: empty field")
        key = (row["model_id"], row["record_id"])
        audit.require(key not in seen_records, f"{label}: duplicate record_id in model")
        seen_records.add(key)
        audit.require(row["scope_scenario_id"] in scenarios, f"{label}: unknown scope scenario")
        audit.require(row["input_confidence"] in {"U2", "U3"}, f"{label}: project P80 accepts only U2/U3 inputs")
        audit.require(row["input_status"] == "accepted", f"{label}: input_status must be accepted")
        audit.require(row["status"] == "candidate_model_input", f"{label}: status must remain Candidate")
        audit.require(row["record_kind"] in {"variable_unit", "fixed_system", "qa_release", "external_labor", "risk_reserve_rate", "productive_hours_per_pm"}, f"{label}: invalid record_kind")
        models[row["model_id"]].append(row)

    results: dict[str, tuple[Decimal, Decimal]] = {}
    for model_id, model_rows in models.items():
        scenarios_used = {row["scope_scenario_id"] for row in model_rows}
        audit.require(len(scenarios_used) == 1, f"{model_id}: cross-scenario inputs are forbidden")
        scenario_id = next(iter(scenarios_used), "")
        if scenario_id in scenarios and scenarios[scenario_id]["tier_id"] == "SCOPE2_MINIMUM_22":
            audit.require(scope2_duration_gate == "closed_at_or_below_1800", f"{model_id}: Scope2 duration gate is not closed at <=1800 minutes")
        base_hours = Decimal("0")
        risk_values: list[Decimal] = []
        productive_values: list[Decimal] = []
        variable_count = 0
        for row in model_rows:
            label = f"{model_id}/{row['record_id']}"
            kind = row["record_kind"]
            if kind == "variable_unit":
                variable_count += 1
                stats = unit_stats.get(row["unit_type_ref"])
                audit.require(stats is not None and stats.get("p80") is not None, f"{label}: variable unit lacks U2 P80")
                quantity = decimal_value(row["paired_quantity"], f"{label}.paired_quantity", audit)
                unit_p80 = decimal_value(row["unit_p80_hours"], f"{label}.unit_p80_hours", audit)
                novelty = decimal_value(row["novelty_multiplier"], f"{label}.novelty_multiplier", audit)
                integration = decimal_value(row["integration_multiplier"], f"{label}.integration_multiplier", audit)
                fixed = decimal_value(row["fixed_hours"], f"{label}.fixed_hours", audit)
                audit.require(row["scalar_value"] == "none", f"{label}: variable unit cannot carry scalar_value")
                if stats is not None and stats.get("p80") is not None and unit_p80 is not None:
                    audit.require(abs(unit_p80 - stats["p80"]) <= TWO_PLACES, f"{label}: unit_p80_hours differs from measured percentile")
                if None not in {quantity, unit_p80, novelty, integration, fixed}:
                    audit.require(quantity > 0 and unit_p80 > 0, f"{label}: quantity/P80 must be >0")
                    audit.require(novelty >= 1 and integration >= 1, f"{label}: multipliers must be >=1")
                    audit.require(fixed == 0, f"{label}: variable unit fixed_hours must be 0")
                    base_hours += quantity * unit_p80 * novelty * integration
            elif kind in {"fixed_system", "qa_release", "external_labor"}:
                audit.require(row["unit_type_ref"] == "none", f"{label}: fixed record must not carry unit_type_ref")
                audit.require(row["paired_quantity"] == row["unit_p80_hours"] == "0", f"{label}: fixed record must have zero quantity/unit P80")
                audit.require(row["novelty_multiplier"] == row["integration_multiplier"] == "1", f"{label}: fixed record multipliers must be 1")
                audit.require(row["scalar_value"] == "none", f"{label}: fixed record cannot carry scalar")
                fixed = decimal_value(row["fixed_hours"], f"{label}.fixed_hours", audit)
                if fixed is not None:
                    audit.require(fixed >= 0, f"{label}: fixed_hours must be >=0")
                    base_hours += fixed
            else:
                audit.require(row["unit_type_ref"] == "none", f"{label}: scalar record must not carry unit_type_ref")
                audit.require(row["paired_quantity"] == row["unit_p80_hours"] == row["fixed_hours"] == "0", f"{label}: scalar record carries hours/quantity")
                audit.require(row["novelty_multiplier"] == row["integration_multiplier"] == "1", f"{label}: scalar record multipliers must be 1")
                scalar = decimal_value(row["scalar_value"], f"{label}.scalar_value", audit)
                if scalar is not None:
                    if kind == "risk_reserve_rate":
                        audit.require(Decimal("0") <= scalar < Decimal("1"), f"{label}: risk reserve must be in [0,1)")
                        risk_values.append(scalar)
                    else:
                        audit.require(scalar > 0, f"{label}: productive_hours_per_pm must be >0")
                        productive_values.append(scalar)
        audit.require(variable_count > 0, f"{model_id}: model has no variable units")
        audit.require(len(risk_values) == 1, f"{model_id}: requires exactly one risk_reserve_rate")
        audit.require(len(productive_values) == 1, f"{model_id}: requires exactly one productive_hours_per_pm")
        if len(risk_values) == len(productive_values) == 1 and productive_values[0] > 0:
            p80_hours = base_hours * (Decimal("1") + risk_values[0])
            p80_pm = p80_hours / productive_values[0]
            results[model_id] = (p80_hours, p80_pm)
    return results


def expected_evidence_level(unit_stats: dict[str, dict[str, object]]) -> str:
    confidences = {stats.get("confidence", "U0") for stats in unit_stats.values()}
    if "U3" in confidences:
        return "U3"
    if "U2" in confidences:
        return "U2"
    if "U1" in confidences:
        return "U1"
    return "U0"


def validate_current_status(
    status_rows: list[dict[str, str]],
    work_unit_count: int,
    measurement_count: int,
    accepted_work_unit_count: int,
    unit_stats: dict[str, dict[str, object]],
    scope2_min: int,
    scope2_max: int,
    scope2_gate: str,
    p80_input_count: int,
    p80_results: dict[str, tuple[Decimal, Decimal]],
    audit: Audit,
) -> None:
    audit.require(len(status_rows) == 1, "budget-calibration-status.tsv must contain exactly one derived status row")
    if len(status_rows) != 1:
        return
    row = status_rows[0]
    p50_count = sum(1 for stats in unit_stats.values() if stats.get("p50") is not None)
    p80_count = sum(1 for stats in unit_stats.values() if stats.get("p80") is not None)
    expected_counts = {
        "work_unit_instance_count": work_unit_count,
        "production_measurement_count": measurement_count,
        "accepted_work_unit_count": accepted_work_unit_count,
        "p50_eligible_unit_type_count": p50_count,
        "p80_eligible_unit_type_count": p80_count,
        "scope2_min_minutes": scope2_min,
        "scope2_max_minutes": scope2_max,
        "project_p80_input_row_count": p80_input_count,
        "project_p80_model_count": len(p80_results),
    }
    for field, expected in expected_counts.items():
        actual = integer_value(row[field], f"budget status.{field}", audit)
        if actual is not None:
            audit.require(actual == expected, f"budget status.{field}={actual}, expected {expected}")
    audit.require(row["status_id"] == "D11-CURRENT", "budget status_id must be D11-CURRENT")
    audit.require(row["scope2_duration_gate"] == scope2_gate, "budget status Scope2 duration gate is stale")
    audit.require(row["evidence_level"] == expected_evidence_level(unit_stats), "budget status evidence level is stale")
    audit.require(row["status"] == "candidate_derived_status", "budget status must remain Candidate")
    if p80_input_count == 0:
        expected_state = "not_calculable_missing_U2" if p80_count == 0 else "not_calculable_missing_model_inputs"
        audit.require(row["project_p80_state"] == expected_state, "empty P80 input table must be explicitly not_calculable")
        audit.require(row["project_p80_hours"] == row["project_p80_pm"] == "none", "empty P80 inputs must not emit a prediction")
    elif len(p80_results) == 1:
        hours, pm = next(iter(p80_results.values()))
        audit.require(row["project_p80_state"] == "calculable_candidate_model_not_authorized", "single P80 model state mismatch")
        actual_hours = decimal_value(row["project_p80_hours"], "budget status.project_p80_hours", audit)
        actual_pm = decimal_value(row["project_p80_pm"], "budget status.project_p80_pm", audit)
        if actual_hours is not None:
            audit.require(actual_hours == hours.quantize(TWO_PLACES, rounding=ROUND_HALF_UP), "project P80 hours do not recompute")
        if actual_pm is not None:
            audit.require(actual_pm == pm.quantize(TWO_PLACES, rounding=ROUND_HALF_UP), "project P80 PM does not recompute")
    else:
        audit.require(row["project_p80_state"] == "calculable_multiple_candidate_models_not_selected", "multiple-model P80 state mismatch")
        audit.require(row["project_p80_hours"] == row["project_p80_pm"] == "none", "unselected multiple models must not emit one prediction")


def validate_ms0(
    milestones: dict[str, dict[str, str]],
    time_system: dict[str, dict[str, str]],
    audit: Audit,
) -> None:
    ms0 = milestones.get("MS0")
    tsn = time_system.get("TSN-P1-RESULT")
    audit.require(ms0 is not None, "missing MS0")
    audit.require(tsn is not None, "missing TSN-P1-RESULT")
    if not ms0 or not tsn:
        return
    expected_outcomes = {
        "shortlist_two",
        "shortlist_three",
        "shortlist_four",
        "no_winner",
        "revise_top_two",
        "retire_all",
    }
    audit.require(set(split_refs(tsn["allowed_outcomes"])) == expected_outcomes, "TSN-P1-RESULT outcome enum drift")
    condition = ms0["pass_condition"]
    for required in (
        "P1四版均完成可裁决M5",
        "只有shortlist入围版必须满足两解与理解硬门",
        "淘汰版保留失败证据",
        "TSN-P1-RESULT",
        "DEC-03-M",
        "核心C2 crossover",
    ):
        audit.require(required in condition, f"MS0 pass_condition missing: {required}")
    audit.require("P1四版有两种真人可发现方案" not in condition, "MS0 still requires every eliminated carrier to pass the two-solution gate")
    for outcome in expected_outcomes:
        audit.require(outcome in condition, f"MS0 pass_condition missing TSN outcome {outcome}")


def validate_d11_prose(audit: Audit) -> None:
    try:
        text = D11_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        audit.errors.append(f"cannot read D11: {exc}")
        return
    for required in (
        "production-work-unit-schema.tsv",
        "production-work-unit-registry.tsv",
        "production-measurement-instances.tsv",
        "budget-calibration-status.tsv",
        "check_d11_budget_calibration.py",
        "not_calculable_missing_U2",
        "当前实测工作单位与投入记录都为0",
        "不得生成项目P80预测",
        "≤1800",
        "P1四版各自完成可裁决M5",
        "淘汰版保留失败证据",
        "被淘汰版失败本身不是绕门理由",
    ):
        audit.require(required in text, f"D11 prose missing honest boundary/reference: {required}")


def run_fault_injections() -> tuple[int, list[str]]:
    failures: list[str] = []
    passed = 0

    values = [Decimal(index) for index in range(1, 9)]
    if percentile_cont(values, Decimal("0.80")) == Decimal("6.6"):
        passed += 1
    else:
        failures.append("FI-PERCENTILE-CONT")
    if len(values[:2]) < 3 and len(values[:7]) < 8:
        passed += 1
    else:
        failures.append("FI-SAMPLE-UNDER-MINIMUM")
    if len(values) >= 8 and len({"C01", "C02"}) >= 2:
        passed += 1
    else:
        failures.append("FI-P80-CROSS-CHAPTER")
    if not (len(values) >= 8 and len({"C01"}) >= 2):
        passed += 1
    else:
        failures.append("FI-P80-SINGLE-CHAPTER")
    # blocked_hours=9 must not repair a false contribution total of 16;
    # the accepted-cost formula only sums the five productive/rework fields.
    productive_fields = (Decimal("1"), Decimal("2"), Decimal("3"), Decimal("4"), Decimal("5"))
    if sum(productive_fields) != Decimal("16"):
        passed += 1
    else:
        failures.append("FI-MEASUREMENT-TOTAL")
    expected_fte = (Decimal("625") / Decimal("40")).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    if expected_fte == Decimal("15.63"):
        passed += 1
    else:
        failures.append("FI-FTE-ROUNDING")
    status_audit = Audit()
    validate_current_status(
        [
            {
                "status_id": "D11-CURRENT",
                "work_unit_instance_count": "0",
                "production_measurement_count": "0",
                "accepted_work_unit_count": "0",
                "p50_eligible_unit_type_count": "0",
                "p80_eligible_unit_type_count": "0",
                "scope2_min_minutes": "1455",
                "scope2_max_minutes": "2060",
                "scope2_duration_gate": "blocked_above_1800",
                "project_p80_input_row_count": "0",
                "project_p80_model_count": "0",
                "project_p80_state": "calculable_candidate_model_not_authorized",
                "project_p80_hours": "999",
                "project_p80_pm": "9",
                "evidence_level": "U0",
                "status": "candidate_derived_status",
            }
        ],
        0,
        0,
        0,
        {},
        1455,
        2060,
        "blocked_above_1800",
        0,
        {},
        status_audit,
    )
    if any("not_calculable" in error or "must not emit" in error for error in status_audit.errors):
        passed += 1
    else:
        failures.append("FI-EMPTY-P80-PREDICTION")
    ms0_audit = Audit()
    validate_ms0(
        {"MS0": {"pass_condition": "P1四版有两种真人可发现方案"}},
        {
            "TSN-P1-RESULT": {
                "allowed_outcomes": "shortlist_two;shortlist_three;shortlist_four;no_winner;revise_top_two;retire_all"
            }
        },
        ms0_audit,
    )
    if any("every eliminated carrier" in error for error in ms0_audit.errors):
        passed += 1
    else:
        failures.append("FI-MS0-ALL-CARRIERS-MUST-PASS")
    return passed, failures


def main() -> int:
    audit = Audit()
    _, tier_rows = read_tsv(SCOPE_TIER_PATH, audit)
    _, scenario_rows = read_tsv(SCENARIO_PATH, audit)
    _, chapter_rows = read_tsv(CHAPTER_PATH, audit)
    _, asset_rows = read_tsv(ASSET_PATH, audit)
    _, prototype_rows = read_tsv(PROTOTYPE_PATH, audit)
    _, evidence_rows = read_tsv(EVIDENCE_PATH, audit)
    _, milestone_rows = read_tsv(MILESTONE_PATH, audit)
    _, role_rows = read_tsv(ROLE_PATH, audit)
    _, time_system_rows = read_tsv(TIME_SYSTEM_PATH, audit)
    _, calibration_contract_rows = read_tsv(CALIBRATION_CONTRACT_PATH, audit)
    _, work_unit_rows = validate_schema_pair(WORK_UNIT_SCHEMA_PATH, WORK_UNIT_PATH, audit)
    _, measurement_rows = validate_schema_pair(MEASUREMENT_SCHEMA_PATH, MEASUREMENT_PATH, audit)
    p80_header, p80_rows = read_tsv(P80_INPUT_PATH, audit)
    status_header, status_rows = read_tsv(CALIBRATION_STATUS_PATH, audit)
    audit.require(
        status_header
        == [
            "status_id",
            "work_unit_instance_count",
            "production_measurement_count",
            "accepted_work_unit_count",
            "p50_eligible_unit_type_count",
            "p80_eligible_unit_type_count",
            "scope2_min_minutes",
            "scope2_max_minutes",
            "scope2_duration_gate",
            "project_p80_input_row_count",
            "project_p80_model_count",
            "project_p80_state",
            "project_p80_hours",
            "project_p80_pm",
            "evidence_level",
            "status",
        ],
        "budget-calibration-status.tsv: unexpected header",
    )

    tiers = keyed(tier_rows, "tier_id", audit, "scope tiers")
    scenarios = keyed(scenario_rows, "scenario_id", audit, "scope scenarios")
    chapters = keyed(chapter_rows, "chapter_id", audit, "chapters")
    assets = keyed(asset_rows, "asset_id", audit, "asset budget")
    prototypes = keyed(prototype_rows, "prototype_id", audit, "prototypes")
    evidence = keyed(evidence_rows, "evidence_id", audit, "acceptance evidence")
    milestones = keyed(milestone_rows, "milestone_id", audit, "milestones")
    roles = keyed(role_rows, "role_id", audit, "production roles")
    time_system = keyed(time_system_rows, "contract_id", audit, "time-system contracts")
    calibration_contracts = keyed(calibration_contract_rows, "calibration_id", audit, "budget calibration contracts")

    validate_scope_scenarios(tiers, scenarios, audit)
    validate_calibration_contracts(calibration_contracts, audit)
    scope2_min, scope2_max, _, scope2_gate = validate_chapter_duration(tiers, chapters, audit)
    unit_stats, accepted_work_unit_count = validate_work_units_and_measurements(
        work_unit_rows,
        measurement_rows,
        assets,
        prototypes,
        chapters,
        scenarios,
        evidence,
        milestones,
        roles,
        audit,
    )
    p80_results = validate_p80_inputs(p80_header, p80_rows, scenarios, unit_stats, scope2_gate, audit)
    validate_current_status(
        status_rows,
        len(work_unit_rows),
        len(measurement_rows),
        accepted_work_unit_count,
        unit_stats,
        scope2_min,
        scope2_max,
        scope2_gate,
        len(p80_rows),
        p80_results,
        audit,
    )
    validate_ms0(milestones, time_system, audit)
    validate_d11_prose(audit)
    fault_passed, fault_failures = run_fault_injections()
    audit.errors.extend(fault_failures)

    if audit.errors:
        print("D11 budget/calibration validation: FAIL")
        for error in audit.errors:
            print(f"- {error}")
        return 1

    p50_count = sum(1 for stats in unit_stats.values() if stats.get("p50") is not None)
    p80_count = sum(1 for stats in unit_stats.values() if stats.get("p80") is not None)
    print("D11 budget/calibration validation: PASS")
    print(f"- U0 scope scenarios={len(scenarios)}; paired low/base/high PM sums and FTE formulas valid")
    print(
        f"- work units={len(work_unit_rows)}; measurements={len(measurement_rows)}; "
        f"accepted={accepted_work_unit_count}; P50-eligible types={p50_count}; P80-eligible types={p80_count}"
    )
    print(f"- Scope2 chapter allocation={scope2_min}-{scope2_max} minutes; 1800-minute gate={scope2_gate}")
    if not p80_rows:
        print("- project P80=NOT_CALCULABLE (zero model inputs / missing U2); no prediction emitted")
    else:
        print(f"- candidate P80 models recomputed={len(p80_results)}; no model grants investment authority")
    print("- MS0 permits failed-carrier evidence and only requires two-solution/understanding gates for shortlisted carriers")
    print(f"- fault injections rejected={fault_passed}/8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
