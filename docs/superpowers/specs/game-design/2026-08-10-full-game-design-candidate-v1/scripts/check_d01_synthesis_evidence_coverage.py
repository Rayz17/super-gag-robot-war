#!/usr/bin/env python3
"""Check D01 synthesis-decision evidence grading without network access.

The check distinguishes page-index references, locator-backed Candidate claims,
and successful response fingerprints.  A response hash is not retained body
content and is never treated as a recoverable quotation archive.
"""

from __future__ import annotations

import argparse
import copy
import csv
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[1]
RESEARCH = PACKAGE / "research"
MATRIX_PATH = RESEARCH / "comparative-mechanic-matrix.tsv"
DECISIONS_PATH = RESEARCH / "mechanic-synthesis-decisions.tsv"
LEDGER_PATH = RESEARCH / "source-evidence-ledger.tsv"
RESPONSES_PATH = RESEARCH / "source-response-fingerprints.tsv"
COVERAGE_PATH = RESEARCH / "synthesis-evidence-coverage.tsv"

EXPECTED_MATRIX_SAMPLES = 35
EXPECTED_DECISIONS = 22
EXPECTED_LEDGER_ROWS = 15
EXPECTED_LOCATOR_SAMPLES = 14
EXPECTED_CAPTURED_ROWS = 13
EXPECTED_CAPTURED_SAMPLES = 12
EXPECTED_FAILED_ROWS = 2
EXPECTED_GRADE_COUNTS = {
    "response_fingerprint_full": 4,
    "response_fingerprint_partial": 13,
    "locator_only_partial": 2,
    "hypothesis_only": 3,
}
EXPECTED_STATUS = "candidate_synthesis_evidence_coverage_v1"
EXPECTED_BODY_BOUNDARY = "no_body_snapshot_or_recoverable_excerpt"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def split_ids(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def unique_in_order(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def expected_grade(source_samples: list[str], locator_samples: list[str], captured_samples: list[str]) -> str:
    if not locator_samples:
        return "hypothesis_only"
    if set(captured_samples) == set(source_samples):
        return "response_fingerprint_full"
    if captured_samples:
        return "response_fingerprint_partial"
    if set(locator_samples) == set(source_samples):
        return "locator_only_full"
    return "locator_only_partial"


def expected_scope(grade: str) -> str:
    return {
        "response_fingerprint_full": "all_source_samples_current_response_fingerprinted",
        "response_fingerprint_partial": "captured_subset_only;not_full_decision_verification",
        "locator_only_full": "locator_claim_only;zero_successful_response_this_review",
        "locator_only_partial": "locator_claim_only;zero_successful_response_this_review",
        "hypothesis_only": "page_index_only;hypothesis_not_source_verified",
    }[grade]


def validate(
    matrix_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    response_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []

    sample_ids = [row["sample_id"] for row in matrix_rows]
    decision_ids = [row["decision_id"] for row in decision_rows]
    evidence_ids = [row["evidence_id"] for row in ledger_rows]
    response_ids = [row["evidence_id"] for row in response_rows]
    coverage_ids = [row["decision_id"] for row in coverage_rows]

    require(errors, len(sample_ids) == EXPECTED_MATRIX_SAMPLES, f"matrix row count differs: {len(sample_ids)}")
    require(errors, len(set(sample_ids)) == len(sample_ids), "matrix sample_id values are not unique")
    require(errors, len(decision_ids) == EXPECTED_DECISIONS, f"decision row count differs: {len(decision_ids)}")
    require(errors, len(set(decision_ids)) == len(decision_ids), "decision_id values are not unique")
    require(errors, len(ledger_rows) == EXPECTED_LEDGER_ROWS, f"ledger row count differs: {len(ledger_rows)}")
    require(errors, len(set(evidence_ids)) == len(evidence_ids), "evidence_id values are not unique")
    require(errors, set(response_ids) == set(evidence_ids) and len(response_ids) == len(evidence_ids), "response rows are not one-to-one with evidence ledger")
    require(errors, len(coverage_rows) == EXPECTED_DECISIONS, f"coverage row count differs: {len(coverage_rows)}")
    require(errors, set(coverage_ids) == set(decision_ids) and len(set(coverage_ids)) == len(coverage_ids), "coverage rows are not one-to-one with RDEC rows")

    sample_set = set(sample_ids)
    ledger_by_sample: dict[str, list[dict[str, str]]] = {}
    for row in ledger_rows:
        require(errors, row["sample_id"] in sample_set, f"ledger sample unknown: {row['evidence_id']}:{row['sample_id']}")
        require(errors, bool(row["page_or_section_locator"].strip()), f"ledger locator empty: {row['evidence_id']}")
        require(errors, bool(row["supported_candidate_claim"].strip()), f"ledger supported claim empty: {row['evidence_id']}")
        require(errors, bool(row["does_not_prove"].strip()), f"ledger inference limit empty: {row['evidence_id']}")
        ledger_by_sample.setdefault(row["sample_id"], []).append(row)

    locator_sample_ids = set(ledger_by_sample)
    require(errors, len(locator_sample_ids) == EXPECTED_LOCATOR_SAMPLES, f"locator-backed unique sample count differs: {len(locator_sample_ids)}")
    require(errors, len(sample_set - locator_sample_ids) == 21, f"page-index-only sample count differs: {len(sample_set - locator_sample_ids)}")

    response_by_id = {row["evidence_id"]: row for row in response_rows}
    captured_ids: set[str] = set()
    failed_ids: set[str] = set()
    for row in response_rows:
        evidence_id = row["evidence_id"]
        capture_result = row["capture_result"]
        if capture_result == "CAPTURED_HTTP_2XX":
            captured_ids.add(evidence_id)
            require(errors, row["http_status"].isdigit() and 200 <= int(row["http_status"]) < 300, f"captured response is not 2xx: {evidence_id}")
            require(errors, bool(HASH_RE.fullmatch(row["raw_sha256"])), f"captured response hash invalid: {evidence_id}")
            require(errors, row["content_length_bytes"].isdigit() and int(row["content_length_bytes"]) > 0, f"captured response length invalid: {evidence_id}")
            require(errors, row["failure_reason"] == "NONE", f"captured response has failure reason: {evidence_id}")
        else:
            failed_ids.add(evidence_id)
            require(errors, capture_result.startswith("FAILED_"), f"unknown response result: {evidence_id}:{capture_result}")
            require(errors, row["raw_sha256"] == "", f"failed response fabricated a hash: {evidence_id}")
            require(errors, row["content_length_bytes"] == "0", f"failed response fabricated body length: {evidence_id}")
            require(errors, row["failure_reason"] not in {"", "NONE"}, f"failed response lacks reason: {evidence_id}")
        require(
            errors,
            row["body_retention"] in {
                "metadata_and_sha_only_body_not_retained",
                "metadata_only_no_body_retained",
            },
            f"response body-retention boundary differs: {evidence_id}",
        )

    require(errors, len(captured_ids) == EXPECTED_CAPTURED_ROWS, f"captured response count differs: {len(captured_ids)}")
    require(errors, len(failed_ids) == EXPECTED_FAILED_ROWS, f"failed response count differs: {len(failed_ids)}")
    captured_sample_ids = {row["sample_id"] for row in ledger_rows if row["evidence_id"] in captured_ids}
    require(errors, len(captured_sample_ids) == EXPECTED_CAPTURED_SAMPLES, f"captured unique sample count differs: {len(captured_sample_ids)}")

    coverage_by_id = {row["decision_id"]: row for row in coverage_rows}
    for decision in decision_rows:
        decision_id = decision["decision_id"]
        source_samples = split_ids(decision["source_samples"])
        require(errors, bool(source_samples), f"RDEC has no source samples: {decision_id}")
        require(errors, len(set(source_samples)) == len(source_samples), f"RDEC repeats a source sample: {decision_id}")
        require(errors, set(source_samples) <= sample_set, f"RDEC source sample unknown: {decision_id}:{sorted(set(source_samples) - sample_set)}")
        coverage = coverage_by_id.get(decision_id)
        if coverage is None:
            continue

        locator_evidence: list[str] = []
        locator_samples: list[str] = []
        for sample_id in source_samples:
            rows = ledger_by_sample.get(sample_id, [])
            if rows:
                locator_samples.append(sample_id)
                locator_evidence.extend(row["evidence_id"] for row in rows)
        captured_evidence = [evidence_id for evidence_id in locator_evidence if evidence_id in captured_ids]
        captured_samples = unique_in_order(
            [next(row["sample_id"] for row in ledger_rows if row["evidence_id"] == evidence_id) for evidence_id in captured_evidence]
        )
        failed_evidence = [evidence_id for evidence_id in locator_evidence if evidence_id in failed_ids]
        page_index_only = [sample_id for sample_id in source_samples if sample_id not in locator_samples]
        grade = expected_grade(source_samples, locator_samples, captured_samples)

        require(errors, coverage["source_sample_ids"] == decision["source_samples"], f"coverage source order differs: {decision_id}")
        require(errors, coverage["source_sample_count"] == str(len(source_samples)), f"coverage source count differs: {decision_id}")
        require(errors, split_ids(coverage["locator_evidence_ids"]) == locator_evidence, f"coverage locator evidence differs: {decision_id}")
        require(errors, split_ids(coverage["locator_backed_sample_ids"]) == locator_samples, f"coverage locator samples differ: {decision_id}")
        require(errors, coverage["locator_backed_sample_count"] == str(len(locator_samples)), f"coverage locator count differs: {decision_id}")
        require(errors, split_ids(coverage["captured_response_evidence_ids"]) == captured_evidence, f"coverage captured evidence differs: {decision_id}")
        require(errors, split_ids(coverage["captured_response_sample_ids"]) == captured_samples, f"coverage captured samples differ: {decision_id}")
        require(errors, coverage["captured_response_sample_count"] == str(len(captured_samples)), f"coverage captured count differs: {decision_id}")
        require(errors, split_ids(coverage["failed_response_evidence_ids"]) == failed_evidence, f"coverage failed evidence differs: {decision_id}")
        require(errors, coverage["failed_response_count"] == str(len(failed_evidence)), f"coverage failed count differs: {decision_id}")
        require(errors, not (set(split_ids(coverage["captured_response_evidence_ids"])) & failed_ids), f"failed response counted as current review: {decision_id}")
        require(errors, split_ids(coverage["page_index_only_sample_ids"]) == page_index_only, f"coverage page-index set differs: {decision_id}")
        require(errors, coverage["evidence_grade"] == grade, f"coverage grade differs: {decision_id}:{coverage['evidence_grade']} != {grade}")
        require(errors, bool(locator_samples) or coverage["evidence_grade"] == "hypothesis_only", f"zero-locator RDEC promoted: {decision_id}")
        require(errors, coverage["current_review_scope"] == expected_scope(grade), f"coverage review scope differs: {decision_id}")
        require(errors, coverage["body_archive_status"] == EXPECTED_BODY_BOUNDARY, f"coverage body archive overclaim: {decision_id}")
        require(errors, coverage["status"] == EXPECTED_STATUS, f"coverage status differs: {decision_id}")

    actual_grade_counts = Counter(row["evidence_grade"] for row in coverage_rows)
    require(errors, dict(actual_grade_counts) == EXPECTED_GRADE_COUNTS, f"grade counts differ: {dict(actual_grade_counts)}")
    return errors


def run_self_test(
    matrix_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    response_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
) -> tuple[int, int]:
    baseline = (matrix_rows, decision_rows, ledger_rows, response_rows, coverage_rows)
    cases: list[tuple[str, tuple[list[dict[str, str]], ...]]] = []

    def add(name: str, editor: Any) -> None:
        values = copy.deepcopy(baseline)
        editor(*values)
        cases.append((name, values))

    add("missing coverage row", lambda m, d, l, r, c: c.pop())
    add("unknown RDEC sample", lambda m, d, l, r, c: d[0].__setitem__("source_samples", d[0]["source_samples"] + ";TEST_UNKNOWN_SAMPLE"))
    add("zero-locator promotion", lambda m, d, l, r, c: next(x for x in c if x["decision_id"] == "RDEC007").__setitem__("evidence_grade", "response_fingerprint_full"))
    add("failed response counted", lambda m, d, l, r, c: next(x for x in c if x["decision_id"] == "RDEC010").__setitem__("captured_response_evidence_ids", "SEV008"))
    add("failed response fake hash", lambda m, d, l, r, c: next(x for x in r if x["evidence_id"] == "SEV008").__setitem__("raw_sha256", "0" * 64))
    add("captured response missing hash", lambda m, d, l, r, c: next(x for x in r if x["evidence_id"] == "SEV001").__setitem__("raw_sha256", ""))
    add("locator omitted", lambda m, d, l, r, c: next(x for x in c if x["decision_id"] == "RDEC001").__setitem__("locator_evidence_ids", "SEV001"))
    add("count drift", lambda m, d, l, r, c: next(x for x in c if x["decision_id"] == "RDEC005").__setitem__("captured_response_sample_count", "2"))
    add("page index drift", lambda m, d, l, r, c: next(x for x in c if x["decision_id"] == "RDEC012").__setitem__("page_index_only_sample_ids", "EXPL004"))
    add("partial promoted full", lambda m, d, l, r, c: next(x for x in c if x["decision_id"] == "RDEC003").__setitem__("evidence_grade", "response_fingerprint_full"))
    add("body archive overclaim", lambda m, d, l, r, c: next(x for x in c if x["decision_id"] == "RDEC008").__setitem__("body_archive_status", "recoverable_body_archive"))
    add("response row removed", lambda m, d, l, r, c: r.pop())
    add("ledger locator erased", lambda m, d, l, r, c: next(x for x in l if x["evidence_id"] == "SEV006").__setitem__("page_or_section_locator", ""))

    rejected = 0
    for name, values in cases:
        if validate(*values):
            rejected += 1
        else:
            print(f"[d01-synthesis:self-test] FAIL mutation escaped: {name}")
    return rejected, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run in-memory fault injections after baseline validation")
    args = parser.parse_args()

    values = (
        read_tsv(MATRIX_PATH),
        read_tsv(DECISIONS_PATH),
        read_tsv(LEDGER_PATH),
        read_tsv(RESPONSES_PATH),
        read_tsv(COVERAGE_PATH),
    )
    errors = validate(*values)
    if errors:
        for error in errors:
            print(f"[d01-synthesis] FAIL {error}")
        print(f"[d01-synthesis] RESULT FAIL errors={len(errors)}")
        return 1

    print(
        "[d01-synthesis] PASS 22/22 RDEC refs resolve; matrix=35; "
        "locator_rows=15/unique_samples=14/page_index_only=21; "
        "captured_responses=13/unique_samples=12; failed_responses=2 excluded"
    )
    print(
        "[d01-synthesis] PASS grades: response_full=4; response_partial=13; "
        "locator_only_partial=2; hypothesis_only=3; no response body retained"
    )
    if args.self_test:
        rejected, total = run_self_test(*values)
        if rejected != total:
            print(f"[d01-synthesis:self-test] RESULT FAIL rejected={rejected}/{total}")
            return 1
        print(f"[d01-synthesis:self-test] PASS rejected={rejected}/{total} injected faults")
    print("[d01-synthesis] RESULT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
