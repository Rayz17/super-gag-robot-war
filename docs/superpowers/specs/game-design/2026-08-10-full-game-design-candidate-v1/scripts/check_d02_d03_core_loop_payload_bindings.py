#!/usr/bin/env python3
"""Validate the Candidate D02-D03 core-loop payload binding contract.

This checker is intentionally read-only.  It proves static payload provenance,
owner/visibility boundaries, committed-output coverage, settlement-receipt
handoffs, and the declared next consumer for the four paper walkthroughs.  It
does not execute a game loop, a settlement owner, a Build, or a human test.
"""

from __future__ import annotations

import argparse
import copy
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = PACKAGE_ROOT / "data/core-loop-paper-walkthrough-traces.tsv"
TRANSITION_PATH = PACKAGE_ROOT / "data/mode-transition-contracts.tsv"
BINDING_PATH = PACKAGE_ROOT / "data/core-loop-payload-bindings.tsv"
STATE_PATH = PACKAGE_ROOT / "data/system-state-contracts.tsv"
SYSTEM_PATH = PACKAGE_ROOT / "data/system-node-contracts.tsv"

EXPECTED_HEADER = [
    "binding_id",
    "trace_step_id",
    "session_id",
    "transition_id",
    "transition_owner",
    "visibility_contract",
    "required_input_sources",
    "committed_output_refs",
    "boundary_output",
    "mode_receipt_ref",
    "output_primary_consumers",
    "next_step_id",
    "stable_save_contract",
    "status",
]
ALLOWED_SOURCE_KINDS = {"seed", "owner_read", "prior_output", "receipt", "mode_result"}
ALLOWED_VISIBILITY = {"player_visible", "observer_scoped", "mixed", "internal_owner_only"}
SETTLEMENT_MODES = {
    "activity_settlement",
    "encounter_settlement",
    "operation_settlement",
    "chapter_settlement",
}
EXPECTED_STATUS = "candidate_static_payload_binding_v1"
FORBIDDEN_PLACEHOLDERS = ("TBD", "TODO", "UNKNOWN", "PLACEHOLDER")
STEP_FIELD_RE = re.compile(r"^(PW-[A-D][0-9]{2})\.([a-z][a-z0-9_]*)$")


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]], list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return [], [], [f"missing file: {path.relative_to(PACKAGE_ROOT)}"]
    with path.open("r", encoding="utf-8", newline="") as handle:
        raw_rows = list(csv.reader(handle, delimiter="\t"))
    if not raw_rows:
        return [], [], [f"empty file: {path.relative_to(PACKAGE_ROOT)}"]
    header = raw_rows[0]
    rows: list[dict[str, str]] = []
    for line_no, raw in enumerate(raw_rows[1:], start=2):
        if len(raw) != len(header):
            errors.append(
                f"{path.relative_to(PACKAGE_ROOT)}:{line_no}: "
                f"TSV width {len(raw)} != {len(header)}"
            )
            continue
        rows.append(dict(zip(header, raw)))
    return header, rows, errors


def split_fields(raw: str) -> list[str]:
    return [field for field in raw.split(";") if field]


def parse_mapping(raw: str, owner: str, column: str, errors: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    if not raw:
        errors.append(f"{owner}: empty {column}")
        return result
    for item in raw.split(";"):
        key, separator, value = item.partition("=")
        if not separator or not key or not value:
            errors.append(f"{owner}: malformed {column} item {item!r}")
            continue
        if key in result:
            errors.append(f"{owner}: duplicate {column} key {key}")
            continue
        result[key] = value
    return result


def parse_step_field(raw: str) -> tuple[str, str] | None:
    match = STEP_FIELD_RE.fullmatch(raw)
    if match is None:
        return None
    return match.group(1), match.group(2)


def validate_rows(
    binding_rows: list[dict[str, str]],
    trace_rows: list[dict[str, str]],
    transition_rows: list[dict[str, str]],
    systems: set[str],
    states: set[str],
) -> tuple[list[str], Counter[str]]:
    errors: list[str] = []
    stats: Counter[str] = Counter()
    trace_by_id = {row["trace_step_id"]: row for row in trace_rows}
    transition_by_id = {row["transition_id"]: row for row in transition_rows}

    ordered_by_session: dict[str, list[dict[str, str]]] = defaultdict(list)
    for trace in trace_rows:
        ordered_by_session[trace["session_id"]].append(trace)
    for session_rows in ordered_by_session.values():
        session_rows.sort(key=lambda row: int(row["step_order"]))

    expected_next: dict[str, str] = {}
    step_order: dict[str, tuple[str, int]] = {}
    for session_id, session_rows in ordered_by_session.items():
        for index, trace in enumerate(session_rows):
            step_id = trace["trace_step_id"]
            step_order[step_id] = (session_id, index)
            expected_next[step_id] = (
                session_rows[index + 1]["trace_step_id"]
                if index + 1 < len(session_rows)
                else "SESSION_EXIT"
            )

    binding_ids = [row.get("binding_id", "") for row in binding_rows]
    bound_steps = [row.get("trace_step_id", "") for row in binding_rows]
    if len(binding_ids) != len(set(binding_ids)):
        errors.append("binding_id values are not unique")
    if len(bound_steps) != len(set(bound_steps)):
        errors.append("trace_step_id values are bound more than once")
    if set(bound_steps) != set(trace_by_id):
        errors.append(
            "payload binding coverage differs: "
            f"missing={sorted(set(trace_by_id) - set(bound_steps))}, "
            f"extra={sorted(set(bound_steps) - set(trace_by_id))}"
        )

    parsed_inputs: dict[str, dict[str, str]] = {}
    parsed_outputs: dict[str, dict[str, str]] = {}
    parsed_consumers: dict[str, dict[str, str]] = {}
    row_by_step: dict[str, dict[str, str]] = {}
    receipt_producer: dict[str, str] = {}

    for row in binding_rows:
        step_id = row.get("trace_step_id", "<missing-step>")
        row_by_step[step_id] = row
        trace = trace_by_id.get(step_id)
        if trace is None:
            continue
        transition = transition_by_id.get(row.get("transition_id", ""))
        if transition is None:
            errors.append(f"{step_id}: unknown transition_id {row.get('transition_id')!r}")
            continue

        if row.get("session_id") != trace["session_id"]:
            errors.append(f"{step_id}: session_id differs from trace")
        if row.get("transition_id") != trace["transition_id"]:
            errors.append(f"{step_id}: transition_id differs from trace")
        if row.get("transition_owner") != transition["owner"]:
            errors.append(
                f"{step_id}: transition_owner={row.get('transition_owner')!r} "
                f"!= {transition['owner']!r}"
            )
        if row.get("transition_owner") not in systems:
            errors.append(f"{step_id}: unknown transition_owner {row.get('transition_owner')!r}")
        if row.get("visibility_contract") not in ALLOWED_VISIBILITY:
            errors.append(f"{step_id}: invalid visibility_contract {row.get('visibility_contract')!r}")
        if row.get("status") != EXPECTED_STATUS:
            errors.append(f"{step_id}: status drift {row.get('status')!r}")
        if row.get("stable_save_contract") != trace["stable_save"]:
            errors.append(f"{step_id}: stable_save_contract differs from trace")
        if row.get("stable_save_contract") != transition["stable_save_boundary"]:
            errors.append(f"{step_id}: stable_save_contract differs from transition")
        if row.get("next_step_id") != expected_next.get(step_id):
            errors.append(
                f"{step_id}: next_step_id={row.get('next_step_id')!r} "
                f"!= {expected_next.get(step_id)!r}"
            )

        row_text = "\t".join(row.values()).upper()
        for placeholder in FORBIDDEN_PLACEHOLDERS:
            if placeholder in row_text:
                errors.append(f"{step_id}: forbidden placeholder {placeholder}")

        inputs = parse_mapping(row.get("required_input_sources", ""), step_id, "required_input_sources", errors)
        outputs = parse_mapping(row.get("committed_output_refs", ""), step_id, "committed_output_refs", errors)
        consumers = parse_mapping(
            row.get("output_primary_consumers", ""),
            step_id,
            "output_primary_consumers",
            errors,
        )
        parsed_inputs[step_id] = inputs
        parsed_outputs[step_id] = outputs
        parsed_consumers[step_id] = consumers

        required_fields = set(split_fields(transition["required_inputs"]))
        committed_fields = set(split_fields(transition["committed_outputs"]))
        if set(inputs) != required_fields:
            errors.append(
                f"{step_id}: required-input coverage differs: "
                f"missing={sorted(required_fields - set(inputs))}, "
                f"extra={sorted(set(inputs) - required_fields)}"
            )
        if set(outputs) != committed_fields:
            errors.append(
                f"{step_id}: committed-output coverage differs: "
                f"missing={sorted(committed_fields - set(outputs))}, "
                f"extra={sorted(set(outputs) - committed_fields)}"
            )
        if set(consumers) != committed_fields:
            errors.append(
                f"{step_id}: output-consumer coverage differs: "
                f"missing={sorted(committed_fields - set(consumers))}, "
                f"extra={sorted(set(consumers) - committed_fields)}"
            )
        if row.get("boundary_output") not in committed_fields:
            errors.append(f"{step_id}: boundary_output is not a committed output")

        for field, reference in outputs.items():
            if reference != f"{step_id}.{field}":
                errors.append(f"{step_id}: output {field} must use stable ref {step_id}.{field}")

        next_step = expected_next.get(step_id)
        for field, consumer in consumers.items():
            if consumer.startswith("OWNER:"):
                owner_system = consumer.split(":", 1)[1]
                if owner_system not in systems:
                    errors.append(f"{step_id}: output {field} has unknown owner consumer {consumer}")
            elif consumer == "SESSION_EXIT":
                if next_step != "SESSION_EXIT":
                    errors.append(f"{step_id}: nonterminal output {field} cannot use SESSION_EXIT")
            elif consumer != next_step:
                errors.append(
                    f"{step_id}: output {field} consumer {consumer!r} is neither next step nor owner"
                )

        receipt_ref = row.get("mode_receipt_ref", "")
        if trace["to_mode"] in SETTLEMENT_MODES:
            expected_receipt = f"RCPT-{step_id}"
            if receipt_ref != expected_receipt:
                errors.append(f"{step_id}: settlement mode requires mode_receipt_ref={expected_receipt}")
            elif receipt_ref in receipt_producer:
                errors.append(f"{step_id}: duplicate mode_receipt_ref {receipt_ref}")
            else:
                receipt_producer[receipt_ref] = step_id
        elif receipt_ref != "NONE":
            errors.append(f"{step_id}: non-settlement destination must use mode_receipt_ref=NONE")

        stats["required_inputs"] += len(inputs)
        stats["committed_outputs"] += len(outputs)
        stats[f"visibility:{row.get('visibility_contract', '')}"] += 1

    for step_id, inputs in parsed_inputs.items():
        if step_id not in step_order:
            continue
        session_id, current_index = step_order[step_id]
        prior_steps = {
            trace["trace_step_id"]
            for trace in ordered_by_session[session_id][:current_index]
        }
        immediately_previous = (
            ordered_by_session[session_id][current_index - 1]["trace_step_id"]
            if current_index > 0
            else None
        )
        direct_previous_anchor = current_index == 0

        for field, source in inputs.items():
            kind, separator, reference = source.partition("@")
            if not separator or kind not in ALLOWED_SOURCE_KINDS or not reference:
                errors.append(f"{step_id}: input {field} has malformed source {source!r}")
                continue
            stats[f"source:{kind}"] += 1

            if kind == "owner_read":
                state_id = reference.split(".", 1)[0]
                if state_id not in states:
                    errors.append(f"{step_id}: input {field} reads unknown state {state_id}")
            elif kind == "prior_output":
                parsed = parse_step_field(reference)
                if parsed is None:
                    errors.append(f"{step_id}: input {field} has invalid prior_output ref {reference}")
                    continue
                producer_step, producer_field = parsed
                if producer_step not in prior_steps:
                    errors.append(f"{step_id}: input {field} prior_output is not earlier in same session")
                elif producer_field not in parsed_outputs.get(producer_step, {}):
                    errors.append(f"{step_id}: input {field} references undeclared output {reference}")
                if producer_step == immediately_previous:
                    direct_previous_anchor = True
            elif kind == "mode_result":
                anchor, result_separator, result_field = reference.partition(":")
                parsed = parse_step_field(anchor)
                if parsed is None or not result_separator or not result_field:
                    errors.append(f"{step_id}: input {field} has invalid mode_result ref {reference}")
                    continue
                producer_step, producer_field = parsed
                if producer_step not in prior_steps:
                    errors.append(f"{step_id}: input {field} mode_result anchor is not earlier in same session")
                elif producer_field not in parsed_outputs.get(producer_step, {}):
                    errors.append(f"{step_id}: input {field} anchors unknown output {anchor}")
                if producer_step == immediately_previous:
                    direct_previous_anchor = True
            elif kind == "receipt":
                producer_step = receipt_producer.get(reference)
                if producer_step is None:
                    errors.append(f"{step_id}: input {field} references unknown receipt {reference}")
                elif producer_step not in prior_steps:
                    errors.append(f"{step_id}: input {field} receipt is not earlier in same session")
                elif producer_step == immediately_previous:
                    direct_previous_anchor = True
            elif kind == "seed":
                if any(character.isspace() for character in reference):
                    errors.append(f"{step_id}: input {field} seed reference contains whitespace")

        if current_index > 0 and not direct_previous_anchor:
            errors.append(f"{step_id}: no input is anchored to the immediately previous walkthrough step")

    stats["settlement_receipts"] = len(receipt_producer)
    stats["sessions"] = len(ordered_by_session)
    stats["steps"] = len(binding_rows)
    return errors, stats


def load_contract() -> tuple[
    list[str],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    set[str],
    set[str],
    list[str],
]:
    header, bindings, binding_errors = read_tsv(BINDING_PATH)
    _, traces, trace_errors = read_tsv(TRACE_PATH)
    _, transitions, transition_errors = read_tsv(TRANSITION_PATH)
    _, system_rows, system_errors = read_tsv(SYSTEM_PATH)
    _, state_rows, state_errors = read_tsv(STATE_PATH)
    errors = binding_errors + trace_errors + transition_errors + system_errors + state_errors
    if header and header != EXPECTED_HEADER:
        errors.append(f"binding header drift: {header!r}")
    systems = {row["system_id"] for row in system_rows}
    states = {row["state_id"] for row in state_rows}
    return header, bindings, traces, transitions, systems, states, errors


def run_self_test(
    bindings: list[dict[str, str]],
    traces: list[dict[str, str]],
    transitions: list[dict[str, str]],
    systems: set[str],
    states: set[str],
) -> tuple[int, int, list[str]]:
    attempted = 0
    rejected = 0
    failures: list[str] = []

    def mutate_and_expect_reject(label: str, row_index: int, mutation) -> None:
        nonlocal attempted, rejected
        attempted += 1
        candidate = copy.deepcopy(bindings)
        mutation(candidate[row_index])
        errors, _ = validate_rows(candidate, traces, transitions, systems, states)
        if errors:
            rejected += 1
        else:
            failures.append(label)

    for index, row in enumerate(bindings):
        step_id = row["trace_step_id"]

        def drop_first_mapping(column: str):
            def mutation(target: dict[str, str]) -> None:
                parts = target[column].split(";")
                target[column] = ";".join(parts[1:])
            return mutation

        mutate_and_expect_reject(f"{step_id}:drop_required_input", index, drop_first_mapping("required_input_sources"))
        mutate_and_expect_reject(f"{step_id}:bad_owner", index, lambda target: target.__setitem__("transition_owner", "SYS-INVALID"))
        mutate_and_expect_reject(f"{step_id}:bad_visibility", index, lambda target: target.__setitem__("visibility_contract", "omniscient"))
        mutate_and_expect_reject(f"{step_id}:drop_output", index, drop_first_mapping("committed_output_refs"))
        mutate_and_expect_reject(f"{step_id}:drop_consumer", index, drop_first_mapping("output_primary_consumers"))
        mutate_and_expect_reject(f"{step_id}:bad_boundary", index, lambda target: target.__setitem__("boundary_output", "not_an_output"))
        mutate_and_expect_reject(f"{step_id}:bad_next", index, lambda target: target.__setitem__("next_step_id", "PW-Z99"))
        mutate_and_expect_reject(f"{step_id}:bad_save", index, lambda target: target.__setitem__("stable_save_contract", "never"))
        mutate_and_expect_reject(f"{step_id}:bad_status", index, lambda target: target.__setitem__("status", "complete"))
        mutate_and_expect_reject(
            f"{step_id}:placeholder",
            index,
            lambda target: target.__setitem__("required_input_sources", target["required_input_sources"] + ";injected=seed@TBD"),
        )

        if any(
            f"={kind}@" in row["required_input_sources"]
            for kind in ("prior_output", "receipt", "mode_result")
        ):
            def corrupt_dynamic_ref(target: dict[str, str]) -> None:
                for kind in ("prior_output", "receipt", "mode_result"):
                    marker = f"={kind}@"
                    if marker in target["required_input_sources"]:
                        target["required_input_sources"] = target["required_input_sources"].replace(
                            marker,
                            marker + "BROKEN-",
                            1,
                        )
                        return
            mutate_and_expect_reject(f"{step_id}:bad_dynamic_ref", index, corrupt_dynamic_ref)

    return rejected, attempted, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run in-memory fault-injection checks")
    args = parser.parse_args()

    _, bindings, traces, transitions, systems, states, load_errors = load_contract()
    errors = list(load_errors)
    stats: Counter[str] = Counter()
    if not errors:
        validation_errors, stats = validate_rows(bindings, traces, transitions, systems, states)
        errors.extend(validation_errors)

    if errors:
        print(f"FAIL D02-D03 core-loop payload bindings: {len(errors)} error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "PASS D02-D03 core-loop payload bindings: "
        f"sessions={stats['sessions']}; steps={stats['steps']}; "
        f"required_inputs={stats['required_inputs']}; "
        f"committed_outputs={stats['committed_outputs']}; "
        f"settlement_receipts={stats['settlement_receipts']}; "
        "owners, visibility, save boundaries, provenance and consumers valid"
    )

    if args.self_test:
        rejected, attempted, failures = run_self_test(
            bindings,
            traces,
            transitions,
            systems,
            states,
        )
        if failures:
            print(
                f"FAIL D02-D03 payload self-test: rejected={rejected}/{attempted}",
                file=sys.stderr,
            )
            for failure in failures:
                print(f"- mutation escaped: {failure}", file=sys.stderr)
            return 1
        print(f"PASS D02-D03 payload self-test: rejected={rejected}/{attempted} injected faults")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
