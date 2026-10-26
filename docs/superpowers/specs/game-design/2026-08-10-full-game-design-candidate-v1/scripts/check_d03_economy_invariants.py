#!/usr/bin/env python3
"""Validate Candidate paper-only economy conservation cases."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA = PACKAGE_ROOT / "data"


def read_tsv(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError(f"empty TSV: {path}")
    width = len(lines[0].split("\t"))
    for index, line in enumerate(lines, start=1):
        if len(line.split("\t")) != width:
            raise ValueError(f"{path.name}:{index} width drift")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def integer(row: dict[str, str], field: str) -> int:
    try:
        return int(row[field])
    except ValueError as error:
        raise ValueError(f"{row['case_id']} {field} is not an integer") from error


def main() -> int:
    flows = read_tsv(DATA / "economy-flows.tsv")
    cases = read_tsv(DATA / "economy-invariant-paper-cases.tsv")
    flows_by_id = {row["resource_id"]: row for row in flows}
    if len(flows_by_id) != 25:
        raise ValueError(f"expected 25 economy flow IDs, found {len(flows_by_id)}")
    if len(cases) != 9 or len({row["case_id"] for row in cases}) != 9:
        raise ValueError(f"expected 9 unique economy invariant cases, found {len(cases)}")

    expected_scopes = {"tactical_pulse", "hub_cycle", "operation", "global"}
    seen_scopes: set[str] = set()
    accepted = rejected = replay = 0
    for row in cases:
        case_id = row["case_id"]
        if row["resource_id"] not in flows_by_id:
            raise ValueError(f"{case_id} references unknown resource")
        flow = flows_by_id[row["resource_id"]]
        if row["domain_owner"] != flow["owner_system"]:
            raise ValueError(f"{case_id} owner differs from economy flow")
        seen_scopes.add(row["scope"])
        before = integer(row, "balance_before")
        reserved = integer(row, "reserved")
        source = integer(row, "source_delta")
        sink = integer(row, "sink_delta")
        arithmetic = integer(row, "arithmetic_after")
        after = integer(row, "balance_after")
        if arithmetic != before + source - sink:
            raise ValueError(f"{case_id} arithmetic_after does not match before+source-sink")
        if reserved < 0 or reserved > before + max(source, 0):
            raise ValueError(f"{case_id} has an impossible reservation")

        expectation = row["commit_expectation"]
        if expectation == "accepted":
            accepted += 1
            if after != arithmetic or after < 0:
                raise ValueError(f"{case_id} accepted balance is not conserved/nonnegative")
            if row["receipt_ref"].startswith("NONE_") or row["reject_code"] != "none":
                raise ValueError(f"{case_id} accepted case lacks a valid receipt boundary")
            if row["forbidden_conversion_probe"] != "none":
                raise ValueError(f"{case_id} accepted case contains a forbidden conversion")
        elif expectation == "rejected":
            rejected += 1
            if after != before or row["receipt_ref"] != "NONE_NO_ACCEPTED_RECEIPT":
                raise ValueError(f"{case_id} rejected case did not remain zero-write")
            if not row["reject_code"].startswith("E_"):
                raise ValueError(f"{case_id} rejected case lacks a reject code")
        elif expectation == "idempotent_replay":
            replay += 1
            if not row["replay_of_case_id"] or row["replay_of_case_id"] == "none":
                raise ValueError(f"{case_id} replay lacks its original case")
            original = next((item for item in cases if item["case_id"] == row["replay_of_case_id"]), None)
            if original is None or original["transaction_id"] != row["transaction_id"]:
                raise ValueError(f"{case_id} replay does not bind the original transaction")
            if source != 0 or sink != 0 or after != before or row["receipt_ref"] != original["receipt_ref"]:
                raise ValueError(f"{case_id} replay would apply a second delta or change receipt")
        else:
            raise ValueError(f"{case_id} has unknown commit expectation")

        if row["resource_id"] == "RES_KEY_COMPONENT" and (before, arithmetic, after) != (1, 1, 1):
            raise ValueError("unique component invariant must preserve exactly one instance")
        if "STATE_RELATIONSHIP" in row["forbidden_conversion_probe"] and expectation != "rejected":
            raise ValueError("relationship conversion probe must be rejected")
        if "STATE_CONSENT" in row["forbidden_conversion_probe"] and expectation != "rejected":
            raise ValueError("consent conversion probe must be rejected")
        if (
            row["build_status"] != "zero_build"
            or row["human_evidence_status"] != "not_run"
            or row["status"] != "candidate_economy_invariant_case_v1"
        ):
            raise ValueError(f"{case_id} overstates economy evidence")

    if seen_scopes != expected_scopes:
        raise ValueError(f"economy invariant scope coverage differs: {sorted(seen_scopes)}")
    if (accepted, rejected, replay) != (4, 4, 1):
        raise ValueError(f"economy outcome distribution drift: {(accepted, rejected, replay)}")
    print(
        "D03 economy invariant PASS: 9 paper cases across tactical/Hub/Operation/global; "
        "4 accepted, 4 rejected zero-write, 1 idempotent replay; zero Build/human evidence"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"D03 economy invariant FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
