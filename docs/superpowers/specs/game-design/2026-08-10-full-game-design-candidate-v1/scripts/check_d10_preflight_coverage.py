#!/usr/bin/env python3
"""Validate fail-closed execution-preflight coverage for every registered prototype.

This checker does not authorize execution.  It proves that every Registry node is
either backed by the exact current preflight contracts or explicitly blocked.
"""

from __future__ import annotations

import argparse
import copy
import csv
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROTOTYPE_PATH = ROOT / "data/prototype-test-registry.tsv"
REQUIREMENT_PATH = ROOT / "data/prototype-execution-preflight-requirements.tsv"
INSTANCE_PATH = ROOT / "data/prototype-execution-preflight-instances.tsv"
COVERAGE_PATH = ROOT / "data/prototype-preflight-coverage-ledger.tsv"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def split_set(value: str) -> set[str]:
    if not value or value == "none":
        return set()
    return {item for item in value.split(";") if item}


def unique_index(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value:
            raise AssertionError(f"{label}: empty {key}")
        if value in result:
            raise AssertionError(f"{label}: duplicate {key}={value}")
        result[value] = row
    return result


def expected_phases(prototype: dict[str, str]) -> set[str]:
    prototype_id = prototype["prototype_id"]
    if prototype_id == "R0-TEST-KERNEL":
        return {"implementation"}
    if prototype_id == "D04-P1-SHORTLIST":
        return {"analysis_only", "human_run"}
    if prototype["sample_min"] == "not_applicable":
        return {"implementation"}
    return {"implementation", "human_run"}


def validate(
    prototypes: list[dict[str, str]],
    requirements: list[dict[str, str]],
    instances: list[dict[str, str]],
    coverage: list[dict[str, str]],
) -> tuple[int, int, int]:
    prototype_by_id = unique_index(prototypes, "prototype_id", "prototype registry")
    unique_index(requirements, "preflight_contract_id", "preflight requirements")
    coverage_by_prototype = unique_index(coverage, "prototype_id", "coverage ledger")
    unique_index(coverage, "coverage_id", "coverage ledger")

    if set(coverage_by_prototype) != set(prototype_by_id):
        missing = sorted(set(prototype_by_id) - set(coverage_by_prototype))
        extra = sorted(set(coverage_by_prototype) - set(prototype_by_id))
        raise AssertionError(f"coverage/prototype set mismatch missing={missing} extra={extra}")

    if instances:
        raise AssertionError("preflight instances are no longer zero; refresh authority and coverage audit")

    requirements_by_prototype: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in requirements:
        prototype_id = row["prototype_id"]
        if prototype_id not in prototype_by_id:
            raise AssertionError(f"preflight requirement references unknown prototype {prototype_id}")
        requirements_by_prototype[prototype_id].append(row)

    exact_count = 0
    blocked_count = 0
    for prototype_id, prototype in prototype_by_id.items():
        row = coverage_by_prototype[prototype_id]
        if row["sequence_order"] != prototype["sequence_order"]:
            raise AssertionError(f"{prototype_id}: sequence_order drift")
        if row["family"] != prototype["family"]:
            raise AssertionError(f"{prototype_id}: family drift")
        if row["registry_dependency_refs"] != prototype["dependency_refs"]:
            raise AssertionError(f"{prototype_id}: dependency snapshot drift")
        if row["status"] != "candidate_plan_only":
            raise AssertionError(f"{prototype_id}: status must remain candidate_plan_only")
        if row["current_execution_authority"] != "none_zero_instances":
            raise AssertionError(f"{prototype_id}: no execution authority may be claimed")

        expected = expected_phases(prototype)
        if split_set(row["expected_execution_phases"]) != expected:
            raise AssertionError(f"{prototype_id}: expected execution phases drift")

        actual_requirements = requirements_by_prototype.get(prototype_id, [])
        actual_contract_ids = {item["preflight_contract_id"] for item in actual_requirements}
        actual_phases = {item["execution_phase"] for item in actual_requirements}
        if not actual_phases.issubset(expected):
            raise AssertionError(f"{prototype_id}: unexpected preflight phase {sorted(actual_phases - expected)}")
        if split_set(row["exact_preflight_contract_ids"]) != actual_contract_ids:
            raise AssertionError(f"{prototype_id}: exact contract IDs drift")
        if split_set(row["covered_execution_phases"]) != actual_phases:
            raise AssertionError(f"{prototype_id}: covered phases drift")

        missing = expected - actual_phases
        if split_set(row["missing_execution_phases"]) != missing:
            raise AssertionError(f"{prototype_id}: missing phases drift")

        if missing:
            blocked_count += 1
            if row["coverage_status"] != "blocked_missing_exact_preflight_contracts":
                raise AssertionError(f"{prototype_id}: incomplete contracts must remain blocked")
            if row["notes"] != "registry_node_is_not_execution_authority":
                raise AssertionError(f"{prototype_id}: missing-contract boundary drift")
            expected_next = (
                "define_exact_"
                + "_and_".join(phase for phase in ["implementation", "analysis_only", "human_run"] if phase in missing)
                + "_preflight_contracts_before_any_execution"
            )
            if row["next_required_contract_or_evidence"] != expected_next:
                raise AssertionError(f"{prototype_id}: next contract instruction drift")
        else:
            exact_count += 1
            if row["coverage_status"] != "exact_contracts_defined_instances_zero":
                raise AssertionError(f"{prototype_id}: complete definitions still have zero instances")
            if row["notes"] != "definition_only_no_instances_no_build":
                raise AssertionError(f"{prototype_id}: definition-only boundary drift")
            if row["next_required_contract_or_evidence"] != "instantiate_after_direction_and_exact_envelope_authorization":
                raise AssertionError(f"{prototype_id}: authorization boundary drift")

    if (len(prototypes), len(requirements), exact_count, blocked_count) != (30, 13, 7, 23):
        raise AssertionError(
            "expected current baseline 30 prototypes / 13 contracts / 7 exact / 23 blocked, got "
            f"{len(prototypes)} / {len(requirements)} / {exact_count} / {blocked_count}"
        )
    return exact_count, blocked_count, len(requirements)


def run_self_test(
    prototypes: list[dict[str, str]],
    requirements: list[dict[str, str]],
    instances: list[dict[str, str]],
    coverage: list[dict[str, str]],
) -> int:
    mutations: list[tuple[str, list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]] = []

    c = copy.deepcopy(coverage); c.pop(); mutations.append(("missing coverage row", prototypes, requirements, instances, c))
    c = copy.deepcopy(coverage); c[0]["registry_dependency_refs"] = "none"; mutations.append(("dependency drift", prototypes, requirements, instances, c))
    c = copy.deepcopy(coverage); c[1]["coverage_status"] = "exact_contracts_defined_instances_zero"; mutations.append(("false exact status", prototypes, requirements, instances, c))
    c = copy.deepcopy(coverage); c[1]["missing_execution_phases"] = "none"; mutations.append(("hidden missing phase", prototypes, requirements, instances, c))
    c = copy.deepcopy(coverage); c[0]["current_execution_authority"] = "authorized"; mutations.append(("fabricated authority", prototypes, requirements, instances, c))
    c = copy.deepcopy(coverage); c[0]["exact_preflight_contract_ids"] = "PX-FAKE"; mutations.append(("fake contract", prototypes, requirements, instances, c))
    r = copy.deepcopy(requirements); r.pop(); mutations.append(("removed requirement", prototypes, r, instances, coverage))
    r = copy.deepcopy(requirements); r[0]["execution_phase"] = "human_run"; mutations.append(("wrong phase", prototypes, r, instances, coverage))
    i = [{"preflight_instance_id": "FAKE-PASS", "status": "passed"}]; mutations.append(("fabricated instance", prototypes, requirements, i, coverage))

    rejected = 0
    for label, p_rows, r_rows, i_rows, c_rows in mutations:
        try:
            validate(p_rows, r_rows, i_rows, c_rows)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(f"self-test mutation was not rejected: {label}")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    prototypes = read_tsv(PROTOTYPE_PATH)
    requirements = read_tsv(REQUIREMENT_PATH)
    instances = read_tsv(INSTANCE_PATH)
    coverage = read_tsv(COVERAGE_PATH)
    exact, blocked, contract_count = validate(prototypes, requirements, instances, coverage)
    print(
        "D10 preflight coverage PASS: "
        f"{len(prototypes)}/30 prototypes ledgered; {contract_count} exact contracts cover {exact}; "
        f"{blocked} remain fail-closed; instances=0; execution authority=0"
    )
    if args.self_test:
        rejected = run_self_test(prototypes, requirements, instances, coverage)
        print(f"D10 preflight coverage self-test PASS: rejected={rejected}/{rejected}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"D10 preflight coverage FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
