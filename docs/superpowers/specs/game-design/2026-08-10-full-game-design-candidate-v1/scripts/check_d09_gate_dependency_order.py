#!/usr/bin/env python3
"""Validate the Candidate D09 gate/context dependency order.

This is a definition-level, read-only check.  It does not create gate
instances, approve receipts, or migrate the Current story-chain.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict, deque
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
DATA = PACKAGE / "data"
GATE_PATH = DATA / "game-design-gate-registry.tsv"
CONTEXT_PATH = DATA / "source-context-projection-registry.tsv"
DECISION_PATH = DATA / "user-game-design-decisions.tsv"
RECEIPT_REQUIREMENT_PATH = DATA / "decision-receipt-requirements.tsv"
D09_PATH = PACKAGE / "09-production-pipeline-and-gates.md"


def read_tsv(path: Path, key: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    ids = [row.get(key, "") for row in rows]
    if not rows or any(not value for value in ids):
        raise ValueError(f"{path}: missing rows or {key}")
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path}: duplicate {key}")
    return ids, {row[key]: row for row in rows}


def require_contains(
    errors: list[str], row_id: str, field: str, value: str, *needles: str
) -> None:
    lowered = value.lower()
    for needle in needles:
        if needle.lower() not in lowered:
            errors.append(f"{row_id}.{field} must contain {needle!r}")


def require_excludes(
    errors: list[str], row_id: str, field: str, value: str, *needles: str
) -> None:
    lowered = value.lower()
    for needle in needles:
        if needle.lower() in lowered:
            errors.append(f"{row_id}.{field} must not contain {needle!r}")


def require_order(
    errors: list[str], row_id: str, field: str, value: str, *needles: str
) -> None:
    lowered = value.lower()
    positions = [lowered.find(needle.lower()) for needle in needles]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        errors.append(f"{row_id}.{field} must order " + " -> ".join(needles))


def find_cycle(nodes: list[str], edges: set[tuple[str, str]]) -> list[str] | None:
    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree = {node: 0 for node in nodes}
    for source, target in edges:
        if source == target:
            return [source, target]
        adjacency[source].append(target)
        indegree[target] += 1

    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    visited: list[str] = []
    while queue:
        node = queue.popleft()
        visited.append(node)
        for target in sorted(adjacency[node]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(visited) == len(nodes):
        return None
    return sorted(node for node, degree in indegree.items() if degree > 0)


def main() -> int:
    errors: list[str] = []
    try:
        gate_ids, gates = read_tsv(GATE_PATH, "gate_id")
        context_ids, contexts = read_tsv(CONTEXT_PATH, "projection_id")
        _, decisions = read_tsv(DECISION_PATH, "decision_id")
        _, receipt_requirements = read_tsv(
            RECEIPT_REQUIREMENT_PATH, "requirement_id"
        )
    except (OSError, ValueError) as exc:
        print(f"D09 gate dependency validation: FAIL\n- {exc}")
        return 1

    required_gates = {
        "GATE-GD3",
        "GATE-S20",
        "GATE-S21",
        "GATE-L4",
        "GATE-REVEAL",
        "GATE-READER",
        "GATE-ASSET-AUTH",
        "GATE-ASSET-HANDOFF",
        "GATE-RUNTIME",
    }
    required_contexts = {"CTX-WRITER", "CTX-PRODUCTION", "CTX-RUNTIME"}
    for missing in sorted(required_gates - gates.keys()):
        errors.append(f"missing gate definition {missing}")
    for missing in sorted(required_contexts - contexts.keys()):
        errors.append(f"missing context projection {missing}")
    if "DEC-13" not in decisions:
        errors.append("missing decision definition DEC-13")
    if "DR-DEC13-P" not in receipt_requirements:
        errors.append("missing receipt requirement DR-DEC13-P")
    if errors:
        print("D09 gate dependency validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    gate_index = {gate_id: index for index, gate_id in enumerate(gate_ids)}
    for before, after in (
        ("GATE-GD3", "GATE-S20"),
        ("GATE-S20", "GATE-S21"),
        ("GATE-S21", "GATE-L4"),
        ("GATE-L4", "GATE-REVEAL"),
        ("GATE-REVEAL", "GATE-READER"),
        ("GATE-ASSET-AUTH", "GATE-ASSET-HANDOFF"),
        ("GATE-ASSET-HANDOFF", "GATE-RUNTIME"),
    ):
        if gate_index[before] >= gate_index[after]:
            errors.append(f"registry order must place {before} before {after}")

    gd3 = gates["GATE-GD3"]
    require_contains(errors, "GATE-GD3", "downstream_unlock", gd3["downstream_unlock"], "GATE-S20")
    require_excludes(errors, "GATE-GD3", "downstream_unlock", gd3["downstream_unlock"], "L4")

    l4 = gates["GATE-L4"]
    require_contains(
        errors,
        "GATE-L4",
        "required_inputs",
        l4["required_inputs"],
        "GATE-S20",
        "GATE-S21",
        "sealed GD3",
        "CTX-ENTITY",
    )
    require_excludes(errors, "GATE-L4", "required_inputs", l4["required_inputs"], "CTX-WRITER")
    require_contains(errors, "GATE-L4", "downstream_unlock", l4["downstream_unlock"], "GATE-REVEAL")

    reveal = gates["GATE-REVEAL"]
    require_contains(
        errors,
        "GATE-REVEAL",
        "required_inputs",
        reveal["required_inputs"],
        "GATE-L4",
        "sealed L4",
        "reveal ledger",
    )
    require_contains(errors, "GATE-REVEAL", "downstream_unlock", reveal["downstream_unlock"], "CTX-WRITER")

    reader = gates["GATE-READER"]
    require_contains(
        errors,
        "GATE-READER",
        "required_inputs",
        reader["required_inputs"],
        "GATE-L4",
        "GATE-REVEAL",
        "CTX-WRITER",
    )

    asset_handoff = gates["GATE-ASSET-HANDOFF"]
    require_contains(
        errors,
        "GATE-ASSET-HANDOFF",
        "required_inputs",
        asset_handoff["required_inputs"],
        "GATE-ASSET-AUTH",
    )
    runtime_gate = gates["GATE-RUNTIME"]
    require_contains(
        errors,
        "GATE-RUNTIME",
        "required_inputs",
        runtime_gate["required_inputs"],
        "GATE-ASSET-HANDOFF",
        "build manifest",
    )

    writer = contexts["CTX-WRITER"]
    require_contains(
        errors,
        "CTX-WRITER",
        "required_snapshot_evidence",
        writer["required_snapshot_evidence"],
        "GATE-REVEAL",
    )
    require_contains(
        errors,
        "CTX-WRITER",
        "compiler_behavior",
        writer["compiler_behavior"],
        "GATE-REVEAL",
    )

    production = contexts["CTX-PRODUCTION"]
    require_contains(
        errors,
        "CTX-PRODUCTION",
        "admitted_source_kinds",
        production["admitted_source_kinds"],
        "GATE-ASSET-AUTH",
        "authorized Candidate asset manifest",
    )
    require_excludes(
        errors,
        "CTX-PRODUCTION",
        "admitted_source_kinds",
        production["admitted_source_kinds"],
        "GATE-ASSET-HANDOFF",
        "formal asset handoff",
        "GATE-RUNTIME",
    )

    runtime = contexts["CTX-RUNTIME"]
    require_contains(
        errors,
        "CTX-RUNTIME",
        "admitted_source_kinds",
        runtime["admitted_source_kinds"],
        "GATE-ASSET-HANDOFF",
        "final asset manifest",
    )

    dec13 = decisions["DEC-13"]
    require_contains(
        errors,
        "DEC-13",
        "candidate_test_unlocks",
        dec13["candidate_test_unlocks"],
        "GATE-L4",
    )
    require_contains(
        errors,
        "DEC-13",
        "bounded_migration_evidence",
        dec13["bounded_migration_evidence"],
        "GATE-L4",
        "PASS",
    )
    require_order(
        errors,
        "DEC-13",
        "bounded_migration_unlocks",
        dec13["bounded_migration_unlocks"],
        "GATE-L4",
        "GATE-REVEAL",
        "CTX-WRITER",
    )
    if dec13["decision_status"] != "presented_no_decision":
        errors.append("DEC-13.decision_status must remain presented_no_decision")
    if dec13["user_choice"]:
        errors.append("DEC-13.user_choice must remain empty")

    dec13_production = receipt_requirements["DR-DEC13-P"]
    require_contains(
        errors,
        "DR-DEC13-P",
        "required_scope",
        dec13_production["required_scope"],
        "GATE-L4",
        "GATE-REVEAL",
    )
    require_contains(
        errors,
        "DR-DEC13-P",
        "prerequisite_evidence",
        dec13_production["prerequisite_evidence"],
        "GATE-L4",
        "PASS",
    )
    require_order(
        errors,
        "DR-DEC13-P",
        "notes",
        dec13_production["notes"],
        "GATE-L4",
        "GATE-REVEAL",
    )
    for field, expected in (
        ("receipt_path", "none"),
        ("receipt_sha256", "none"),
        ("requirement_status", "missing"),
    ):
        if dec13_production[field] != expected:
            errors.append(f"DR-DEC13-P.{field} must remain {expected}")

    gate_edges: set[tuple[str, str]] = set()
    for gate_id, row in gates.items():
        for dependency in re.findall(r"GATE-[A-Z0-9-]+", row["required_inputs"]):
            if dependency in gates:
                gate_edges.add((dependency, gate_id))
    gate_cycle = find_cycle(gate_ids, gate_edges)
    if gate_cycle:
        errors.append("gate dependency cycle: " + " -> ".join(gate_cycle))

    context_edges: set[tuple[str, str]] = set()
    for context_id, row in contexts.items():
        for dependency in re.findall(r"CTX-[A-Z0-9-]+", row["admitted_source_kinds"]):
            if dependency in contexts:
                context_edges.add((dependency, context_id))
    context_cycle = find_cycle(context_ids, context_edges)
    if context_cycle:
        errors.append("context dependency cycle: " + " -> ".join(context_cycle))

    try:
        d09 = D09_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read D09 document: {exc}")
    else:
        for case_id in (
            "FI-S20-S21-BYPASS",
            "FI-L4-WRITER-CYCLE",
            "FI-PRODUCTION-CYCLE",
        ):
            if case_id not in d09:
                errors.append(f"D09 document missing regression case {case_id}")

    if errors:
        print("D09 gate dependency validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("D09 gate dependency validation: PASS")
    print(f"- {len(gate_ids)} gate definitions; {len(gate_edges)} explicit gate dependencies; DAG")
    print(f"- {len(context_ids)} context projections; {len(context_edges)} explicit context dependencies; DAG")
    print("- order: GD3 -> S20 -> S21 -> L4 -> REVEAL -> READER")
    print("- order: ASSET-AUTH -> ASSET-HANDOFF -> RUNTIME")
    print("- DEC-13 recovery: L4 compatibility -> REVEAL -> CTX-WRITER; still unapproved")
    print("- CTX-PRODUCTION cannot consume handoff/runtime evidence")
    return 0


if __name__ == "__main__":
    sys.exit(main())
