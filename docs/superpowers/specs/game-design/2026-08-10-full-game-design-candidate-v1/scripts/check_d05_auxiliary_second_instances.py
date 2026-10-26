#!/usr/bin/env python3
"""Validate D05 auxiliary second-instance Candidate paper preflights.

This checker proves only frozen-source and structured-paper consistency.  It
does not execute P-EX1/2/3-R2, produce a Build, satisfy M6, or provide human
replication evidence.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[1]
FREEZE_PATH = PACKAGE / "data/auxiliary-replication-freeze-contracts.tsv"
FIXTURE_PATH = PACKAGE / "data/auxiliary-second-instance-paper-fixtures.json"
REGISTRY_PATH = PACKAGE / "data/prototype-paper-fixture-registry.tsv"
PROTOTYPE_PATH = PACKAGE / "data/prototype-test-registry.tsv"
STATE_PATH = PACKAGE / "data/system-state-contracts.tsv"
OUTPUT_GATE_PATH = PACKAGE / "data/auxiliary-output-gates.tsv"

EXPECTED = {
    "AUX_EX1": {
        "base_fixture_id": "FX-D05-EX1",
        "base_prototype_id": "P-EX1",
        "replication_prototype_id": "P-EX1-R2",
        "paper_fixture_id": "FX-D05-EX1-R2-PAPER",
        "fixture_sha256": "ccc75ce38d4bb8a9320a99581180acb1b06f84fb086df3c3a85efd2a0233528b",
        "heading": "## 2. P-EX1《水线分馆集合》微型自由探索",
        "section_sha256": "d99ba1bf986b01cc7c30b69ef1466bfb3449a00ff34529d1bab0d3e7140a156c",
        "actions": {"HELP", "MOVE", "OBSERVE", "PHOTO", "REPORT", "RETURN", "TALK"},
        "ui": {"UI_AUX_INTERACT_PROMPT", "UI_AUX_OUTCOME_CARD", "UI_AUX_ROUTE_NOTE", "UI_AUX_SPATIAL_VIEW"},
        "outcomes": {"clear", "partial", "withdraw"},
        "states": {"ST_EVIDENCE", "ST_LOCATION", "ST_RELATION", "ST_RESULT"},
        "output_gate_id": "AOG_SPATIAL",
    },
    "AUX_EX2": {
        "base_fixture_id": "FX-D05-EX2",
        "base_prototype_id": "P-EX2",
        "replication_prototype_id": "P-EX2-R2",
        "paper_fixture_id": "FX-D05-EX2-R2-PAPER",
        "fixture_sha256": "88dad30a898c13f0aa8ba30ba408e1ede45266f03a3784257738c607f59a30aa",
        "heading": "## 3. P-EX2《偏载试验架》工程实证",
        "section_sha256": "46a48dc1002a13ee8c4d98c62f470dbaf1a093deb9a8c3f52212c0e890b69eef",
        "actions": {"ANNOTATE_SUPPORT", "COMMIT_REPORT", "CONFIGURE", "INSPECT", "PREVIEW_SAFETY", "REVISE_HYPOTHESIS", "RUN_TEST", "WITHDRAW"},
        "ui": {"UI_AUX_CONFIG_3SLOT", "UI_AUX_EVIDENCE_BOARD", "UI_AUX_OUTCOME_CARD", "UI_AUX_REPORT_CARD", "UI_AUX_SAFETY_PREVIEW"},
        "outcomes": {"clear", "partial", "withdraw"},
        "states": {"ST_BODY", "ST_EVIDENCE", "ST_HYPOTHESIS", "ST_RESULT"},
        "output_gate_id": "AOG_EVIDENCE",
    },
    "AUX_EX3": {
        "base_fixture_id": "FX-D05-EX3",
        "base_prototype_id": "P-EX3",
        "replication_prototype_id": "P-EX3-R2",
        "paper_fixture_id": "FX-D05-EX3-R2-PAPER",
        "fixture_sha256": "321634d825cb1ce44846685e45a8a039277c5b266b023e18ca5a14064cb9add0",
        "heading": "## 4. P-EX3《倒相信号间》知识重访",
        "section_sha256": "8f5a45bac7a719853aea79ce729b2d651c338858d08f834102c4a576d9b7764b",
        "actions": {"APPLY", "LINK", "OBSERVE", "RETURN", "SUBMIT_INTERPRETATION"},
        "ui": {"UI_AUX_EVIDENCE_BOARD", "UI_AUX_KNOWLEDGE_LINKS", "UI_AUX_OUTCOME_CARD", "UI_AUX_ROUTE_DELTA", "UI_AUX_SOURCE_TIMELINE"},
        "outcomes": {"clear", "partial", "withdraw"},
        "states": {"ST_EVIDENCE", "ST_HYPOTHESIS", "ST_KNOWLEDGE", "ST_LOCATION", "ST_RESULT"},
        "output_gate_id": "AOG_EVIDENCE",
    },
}

EXPECTED_BOUNDARY = {
    "build_status": "zero_build",
    "canon_write_allowed": False,
    "demo_write_allowed": False,
    "human_evidence_status": "not_run",
    "reader_write_allowed": False,
    "replication_evidence_status": "no_replication_evidence",
    "runtime_write_allowed": False,
}
EXPECTED_REGISTRY_STATUS = "candidate_paper_preflight_no_replication_evidence"
ZERO_ADDITION_FIELDS = (
    "new_input_action_count",
    "new_persistent_state_domain_count",
    "new_settlement_page_count",
    "new_top_level_code_count",
    "new_ui_surface_count",
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def canonical_hash(fixture: dict[str, Any]) -> str:
    payload = dict(fixture)
    payload.pop("canonical_sha256", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def rehash(fixture: dict[str, Any]) -> None:
    fixture["canonical_sha256"] = canonical_hash(fixture)


def split_ids(raw: str) -> set[str]:
    return set(filter(None, raw.split(";")))


def section_bytes(path: Path, heading: str) -> bytes:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    if end < 0:
        end = len(text)
    return (text[start:end].rstrip("\n") + "\n").encode("utf-8")


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def content_id_values(value: Any, key: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if child_key.endswith("_id") and isinstance(child_value, str):
                found.append(child_value)
            if key == "adjacency":
                found.append(child_key)
            found.extend(content_id_values(child_value, child_key))
    elif isinstance(value, list):
        if key in {
            "actors",
            "future_consumers",
            "hypotheses",
            "knowledge_nodes",
            "physical_nodes",
            "requires_evidence",
        }:
            for item in value:
                if isinstance(item, str):
                    found.append(item)
        for item in value:
            found.extend(content_id_values(item, key))
    return found


def classify_ex2(content: dict[str, Any], patch: str, gain: str, load: str) -> str:
    variables = content["variables"]
    if load == "overload":
        return "rejected_scope"
    formula = content["formula"]
    score = (
        Decimal(formula["gain_coefficient"]) * Decimal(variables["gain"][gain])
        + Decimal(formula["load_coefficient"]) * Decimal(variables["load"][load])
        + Decimal(formula["intercept"])
        - Decimal(formula["patch_bonus"][patch])
    )
    if score <= Decimal(content["thresholds"]["stable_max"]):
        return "stable"
    if score <= Decimal(content["thresholds"]["bounded_max"]):
        return "bounded_oscillation"
    return "outside_safe_envelope"


def validate_ex1(errors: list[str], fixture: dict[str, Any]) -> None:
    content = fixture["content"]
    adjacency = content["adjacency"]
    entry = content["entry_node"]
    goal = content["goal_node"]
    require(errors, len(adjacency) == 6, "EX1 must have exactly six spatial nodes")
    for source, targets in adjacency.items():
        for target in targets:
            require(errors, source in adjacency.get(target, []), f"EX1 adjacency not symmetric: {source}->{target}")
    routes = content["routes"]
    for index, route in enumerate(routes, start=1):
        require(errors, bool(route) and route[0] == entry and route[-1] == goal, f"EX1 route {index} endpoints differ")
        for source, target in zip(route, route[1:]):
            require(errors, target in adjacency.get(source, []), f"EX1 route {index} has non-edge {source}->{target}")
    blocked = content["helper_gate"]["blocked_node"]
    routes_without_help = [route for route in routes if blocked not in route]
    require(errors, content["helper_gate"]["optional"] is True, "EX1 helper must remain optional")
    require(errors, len(routes_without_help) >= 2, "EX1 optional-help removal leaves fewer than two routes")
    fact_nodes = {fact["node_id"] for fact in content["facts"]}
    require(errors, len(content["facts"]) >= 4, "EX1 needs four distinct report facts")
    for index, route in enumerate(routes, start=1):
        require(errors, len(set(route) & fact_nodes) >= 2, f"EX1 route {index} lacks two report facts")
    report = content["report_rule"]
    require(errors, report == {"clear_min_supported_facts": 2, "partial_min_supported_facts": 1, "unsupported_clear_rejected": True}, "EX1 report thresholds drifted")
    require(errors, len(content["future_consumers"]) >= 2, "EX1 future consumers missing")


def validate_ex2(errors: list[str], fixture: dict[str, Any]) -> None:
    content = fixture["content"]
    require(errors, len(content["evidence"]) == 3, "EX2 must have three evidence rows")
    require(errors, len(content["hypotheses"]) == 2, "EX2 must have two hypotheses")
    supported = {item["supports"] for item in content["evidence"]}
    require(errors, set(content["hypotheses"]) <= supported, "EX2 hypothesis lacks named evidence")
    required_cases = {
        ("none", "reduced", "rated"): "stable",
        ("preload_shim", "nominal", "rated"): "stable",
        ("none", "high", "rated"): "outside_safe_envelope",
        ("none", "reduced", "overload"): "rejected_scope",
    }
    declared_cases = {
        (case["patch"], case["gain"], case["load"]): case["expected_band"]
        for case in content["required_cases"]
    }
    require(errors, declared_cases == required_cases, "EX2 preregistered cases drifted")
    for keys, expected_band in required_cases.items():
        require(errors, classify_ex2(content, *keys) == expected_band, f"EX2 solver mismatch at {keys}")
    safe_rated: list[tuple[str, str]] = []
    for patch in content["variables"]["patch"]:
        for gain in content["variables"]["gain"]:
            if classify_ex2(content, patch, gain, "rated") == "stable":
                safe_rated.append((patch, gain))
        require(errors, classify_ex2(content, patch, "reduced", "overload") == "rejected_scope", "EX2 overload became executable")
    require(errors, len(safe_rated) >= 2, "EX2 has fewer than two safe rated-load solutions")
    require(errors, len(content["future_consumers"]) >= 2, "EX2 future consumers missing")


def validate_ex3(errors: list[str], fixture: dict[str, Any]) -> None:
    content = fixture["content"]
    require(errors, len(content["physical_nodes"]) == 4, "EX3 must retain exactly four physical nodes")
    require(errors, len(content["knowledge_nodes"]) <= 5, "EX3 knowledge nodes exceed five")
    require(errors, content["inventory_items"] == [], "EX3 must not add inventory items")
    require(errors, set(content["relations_allowed"]) == {"contradicts", "later_than", "same_subject", "supports"}, "EX3 relation vocabulary drifted")
    require(errors, content["correct_current_sequence"] == "RIGHT-2-LEFT", "EX3 current sequence drifted")
    route_change = content["route_change"]
    require(errors, route_change["target_id"] in content["physical_nodes"], "EX3 route targets a new physical node")
    require(
        errors,
        set(route_change["requires_evidence"]) == {
            "TEST_KN_EX3_R2_OLD_LOG",
            "TEST_KN_EX3_R2_CALIBRATION",
            "TEST_KN_EX3_R2_LIVE_ECHO",
        },
        "EX3 route evidence chain drifted",
    )
    oracle_value = "TEST_ORACLE_EX3_R2_SEQUENCE"
    projections = content["observer_projections"]
    require(errors, oracle_value in projections.get("BACKEND_TEST_ORACLE", []), "EX3 backend oracle fixture missing")
    for observer, values in projections.items():
        if observer != "BACKEND_TEST_ORACLE":
            require(errors, oracle_value not in values, f"EX3 oracle leaked to {observer}")
    require(errors, len(content["future_consumers"]) >= 2, "EX3 future consumers missing")


def validate(
    freeze_rows: list[dict[str, str]],
    payload: dict[str, Any],
    registry_rows: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    require(errors, payload.get("schema_id") == "d05_auxiliary_second_instance_paper_preflight_v1", "schema_id differs")
    require(errors, payload.get("authority_boundary") == EXPECTED_BOUNDARY, "top-level authority boundary differs")

    freeze_by_family = {row["family_id"]: row for row in freeze_rows}
    require(errors, set(freeze_by_family) == set(EXPECTED), "freeze family set differs")
    prototype_ids = {row["prototype_id"] for row in read_tsv(PROTOTYPE_PATH)}
    state_ids = {row["state_id"] for row in read_tsv(STATE_PATH)}
    output_gate_ids = {row["output_contract_id"] for row in read_tsv(OUTPUT_GATE_PATH)}

    for family, expected in EXPECTED.items():
        row = freeze_by_family.get(family)
        if row is None:
            continue
        require(errors, row["base_fixture_id"] == expected["base_fixture_id"], f"{family} base fixture differs")
        require(errors, row["base_prototype_id"] == expected["base_prototype_id"], f"{family} base prototype differs")
        require(errors, row["replication_prototype_id"] == expected["replication_prototype_id"], f"{family} replication prototype differs")
        require(errors, row["replication_prototype_id"] in prototype_ids, f"{family} replication prototype unknown")
        require(errors, row["base_section_heading"] == expected["heading"], f"{family} base heading differs")
        require(errors, row["base_section_sha256"] == expected["section_sha256"], f"{family} declared base hash differs")
        base_path = PACKAGE / row["base_artifact_path"]
        require(errors, base_path.is_file(), f"{family} base artifact missing")
        if base_path.is_file():
            try:
                actual_hash = hashlib.sha256(section_bytes(base_path, row["base_section_heading"])).hexdigest()
            except ValueError:
                errors.append(f"{family} base heading absent")
            else:
                require(errors, actual_hash == row["base_section_sha256"], f"{family} base section hash drifted")
        require(errors, split_ids(row["frozen_action_ids"]) == expected["actions"], f"{family} frozen actions differ")
        require(errors, split_ids(row["frozen_ui_surface_ids"]) == expected["ui"], f"{family} frozen UI differs")
        require(errors, split_ids(row["frozen_outcome_ids"]) == expected["outcomes"], f"{family} frozen outcomes differ")
        require(errors, split_ids(row["frozen_persistent_state_domains"]) == expected["states"], f"{family} frozen states differ")
        require(errors, split_ids(row["frozen_persistent_state_domains"]) <= state_ids, f"{family} has unknown state domain")
        require(errors, row["output_gate_id"] == expected["output_gate_id"] and row["output_gate_id"] in output_gate_ids, f"{family} output gate differs")
        require(errors, (PACKAGE / row["settlement_contract_ref"]).is_file(), f"{family} settlement contract missing")
        require(errors, row["paper_evidence_boundary"] == "paper_preflight_only;zero_build;human_not_run;no_replication_evidence", f"{family} paper boundary differs")
        require(errors, row["status"] == "candidate_aux_replication_freeze_v1", f"{family} freeze status differs")

    fixtures = payload.get("fixtures", [])
    fixtures_by_family = {fixture.get("family_id"): fixture for fixture in fixtures}
    require(errors, len(fixtures) == 3 and set(fixtures_by_family) == set(EXPECTED), "fixture family set differs")
    for family, expected in EXPECTED.items():
        fixture = fixtures_by_family.get(family)
        row = freeze_by_family.get(family)
        if fixture is None or row is None:
            continue
        require(errors, fixture.get("fixture_id") == expected["paper_fixture_id"], f"{family} fixture id differs")
        require(errors, fixture.get("base_fixture_id") == expected["base_fixture_id"], f"{family} fixture base differs")
        require(errors, fixture.get("prototype_id") == expected["replication_prototype_id"], f"{family} fixture prototype differs")
        require(errors, fixture.get("build_status") == "zero_build", f"{family} must remain zero_build")
        require(errors, fixture.get("human_evidence_status") == "not_run", f"{family} must remain human not_run")
        require(errors, fixture.get("replication_evidence_status") == "no_replication_evidence", f"{family} must retain no_replication_evidence")
        require(errors, fixture.get("maturity_claim") == "paper_preflight_only", f"{family} maturity claim differs")
        for field in ZERO_ADDITION_FIELDS:
            require(errors, fixture.get(field) == 0, f"{family} {field} must be zero")
        require(errors, set(fixture.get("actions", [])) == split_ids(row["frozen_action_ids"]), f"{family} action reuse differs")
        require(errors, set(fixture.get("ui_surfaces", [])) == split_ids(row["frozen_ui_surface_ids"]), f"{family} UI reuse differs")
        require(errors, set(fixture.get("outcomes", [])) == split_ids(row["frozen_outcome_ids"]), f"{family} outcome reuse differs")
        require(errors, set(fixture.get("persistent_state_domains", [])) == split_ids(row["frozen_persistent_state_domains"]), f"{family} state reuse differs")
        require(errors, fixture.get("output_gate_id") == row["output_gate_id"], f"{family} output gate reuse differs")
        require(errors, fixture.get("canonical_sha256") == expected["fixture_sha256"], f"{family} declared canonical fixture hash differs")
        require(errors, canonical_hash(fixture) == expected["fixture_sha256"], f"{family} canonical fixture bytes drifted")
        for content_id in content_id_values(fixture.get("content", {})):
            require(errors, content_id.startswith("TEST_"), f"{family} non-TEST content id: {content_id}")
        if family == "AUX_EX1":
            validate_ex1(errors, fixture)
        elif family == "AUX_EX2":
            validate_ex2(errors, fixture)
        else:
            validate_ex3(errors, fixture)

    registry_by_id = {row["fixture_id"]: row for row in registry_rows}
    for expected in EXPECTED.values():
        fixture_id = expected["paper_fixture_id"]
        row = registry_by_id.get(fixture_id)
        if row is None:
            errors.append(f"registry row missing: {fixture_id}")
            continue
        require(errors, row["prototype_ids"] == expected["replication_prototype_id"], f"{fixture_id} registry prototype differs")
        require(errors, row["artifact_path"] == "validation/d05-auxiliary-second-instance-paper-fixtures-v0.1.md", f"{fixture_id} registry artifact differs")
        require(errors, row["build_status"] == "zero_build", f"{fixture_id} registry build status differs")
        require(errors, row["human_evidence_status"] == "not_run", f"{fixture_id} registry human status differs")
        require(errors, row["status"] == EXPECTED_REGISTRY_STATUS, f"{fixture_id} registry evidence status differs")
        require(errors, all(row[field] == "yes" for field in ("initial_state_defined", "player_choice_trace_defined", "expected_outcomes_defined", "automated_assertion_spec_defined")), f"{fixture_id} registry definition fields differ")
        required_refs = split_ids(row["required_contract_refs"])
        for required_ref in {
            "data/auxiliary-replication-freeze-contracts.tsv",
            "data/auxiliary-second-instance-paper-fixtures.json",
            "data/auxiliary-kernel-contracts.tsv",
            "data/auxiliary-output-gates.tsv",
            "data/settlement-owner-prepare-commit-contracts.tsv",
        }:
            require(errors, required_ref in required_refs, f"{fixture_id} missing contract ref {required_ref}")
        require(errors, "no_replication_evidence" in row["authority_boundary"], f"{fixture_id} registry boundary overclaims")
    return errors


def run_self_test(
    freeze_rows: list[dict[str, str]],
    payload: dict[str, Any],
    registry_rows: list[dict[str, str]],
) -> tuple[int, int]:
    cases: list[tuple[str, Any]] = []

    def mutation(name: str, edit: Any, *, rehash_family: str | None = None) -> None:
        frozen = copy.deepcopy(freeze_rows)
        data = copy.deepcopy(payload)
        registry = copy.deepcopy(registry_rows)
        edit(frozen, data, registry)
        if rehash_family is not None:
            fixture = next(item for item in data["fixtures"] if item["family_id"] == rehash_family)
            rehash(fixture)
        cases.append((name, (frozen, data, registry)))

    mutation("new action", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX1")["actions"].append("TEST_NEW_ACTION"), rehash_family="AUX_EX1")
    mutation("new UI", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX2")["ui_surfaces"].append("UI_TEST_NEW"), rehash_family="AUX_EX2")
    mutation("new state", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX3")["persistent_state_domains"].append("ST_RESOURCE"), rehash_family="AUX_EX3")
    mutation("new settlement page", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX1").__setitem__("new_settlement_page_count", 1), rehash_family="AUX_EX1")
    mutation("EX1 route collapse", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX1")["content"].__setitem__("routes", [next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX1")["content"]["routes"][2]]), rehash_family="AUX_EX1")
    mutation("EX2 solver drift", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX2")["content"]["formula"].__setitem__("intercept", "-0.10"), rehash_family="AUX_EX2")
    mutation("EX3 inventory key", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX3")["content"]["inventory_items"].append("TEST_ITEM_EX3_R2_KEY"), rehash_family="AUX_EX3")
    mutation("EX3 sixth knowledge node", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX3")["content"]["knowledge_nodes"].append({"knowledge_id": "TEST_KN_EX3_R2_SIXTH", "source_id": "TEST_SOURCE_EX3_R2_SIXTH", "claim": "extra", "observed_at": "VISIT2_T03"}), rehash_family="AUX_EX3")
    mutation("EX3 oracle leak", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX3")["content"]["observer_projections"]["PLAYER_VISIT_1"].append("TEST_ORACLE_EX3_R2_SEQUENCE"), rehash_family="AUX_EX3")
    mutation("canonical hash", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX1").__setitem__("canonical_sha256", "0" * 64))
    mutation("build promotion", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX2").__setitem__("build_status", "built"), rehash_family="AUX_EX2")
    mutation("replication overclaim", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX3").__setitem__("replication_evidence_status", "passed"), rehash_family="AUX_EX3")
    mutation("missing consumer", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX1")["content"].__setitem__("future_consumers", []), rehash_family="AUX_EX1")
    mutation("base section hash", lambda f, d, r: next(x for x in f if x["family_id"] == "AUX_EX2").__setitem__("base_section_sha256", "0" * 64))
    mutation("non-TEST content", lambda f, d, r: next(x for x in d["fixtures"] if x["family_id"] == "AUX_EX1")["content"]["actors"].__setitem__(0, "ACTOR_NOT_TEST"), rehash_family="AUX_EX1")
    mutation("registry evidence promotion", lambda f, d, r: next(x for x in r if x["fixture_id"] == "FX-D05-EX1-R2-PAPER").__setitem__("status", "candidate_replication_passed"))

    rejected = 0
    for name, values in cases:
        case_errors = validate(*values)
        if case_errors:
            rejected += 1
        else:
            print(f"[d05-r2:self-test] FAIL mutation escaped: {name}")
    return rejected, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run in-memory fault injections after baseline validation")
    args = parser.parse_args()

    freeze_rows = read_tsv(FREEZE_PATH)
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    registry_rows = read_tsv(REGISTRY_PATH)
    errors = validate(freeze_rows, payload, registry_rows)
    if errors:
        for error in errors:
            print(f"[d05-r2] FAIL {error}")
        print(f"[d05-r2] RESULT FAIL errors={len(errors)}")
        return 1

    print(
        "[d05-r2] PASS 3 second-instance Candidate paper preflights; "
        "frozen actions/UI/outcomes/state domains; zero_build/human_not_run/no_replication_evidence"
    )
    if args.self_test:
        rejected, total = run_self_test(freeze_rows, payload, registry_rows)
        if rejected != total:
            print(f"[d05-r2:self-test] RESULT FAIL rejected={rejected}/{total}")
            return 1
        print(f"[d05-r2:self-test] PASS rejected={rejected}/{total} injected faults")
    print("[d05-r2] RESULT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
