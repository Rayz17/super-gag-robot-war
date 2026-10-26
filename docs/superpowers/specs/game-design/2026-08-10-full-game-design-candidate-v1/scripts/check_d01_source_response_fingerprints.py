#!/usr/bin/env python3
"""Validate D01 official-source response fingerprints without network or writes.

This checker proves only that the Candidate research snapshot is internally
well-formed and remains linked one-to-one to source-evidence-ledger.tsv.  It
does not assert that a source claim is true, that a locator occurs in a
rendered page, or that any project mechanic is Canon/Runtime.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = PACKAGE_ROOT / "research/source-evidence-ledger.tsv"
FINGERPRINT_PATH = PACKAGE_ROOT / "research/source-response-fingerprints.tsv"

EXPECTED_HEADER = [
    "evidence_id",
    "ledger_reference",
    "requested_url",
    "final_url",
    "captured_at_utc",
    "http_status",
    "content_type",
    "content_length_bytes",
    "raw_sha256",
    "locator",
    "capture_result",
    "failure_reason",
    "dynamic_content_caveat",
    "body_retention",
    "request_profile",
]
EXPECTED_EVIDENCE_IDS = {f"SEV{number:03d}" for number in range(1, 16)}
ALLOWED_OFFICIAL_HOSTS = {
    "www.subsetgames.com",
    "braceyourselfgames.com",
    "playway.com",
    "command.matrixgames.com",
    "www.bandainamcoent.com",
    "manuals.sega.com",
    "xcom.com",
    "assets.2k.com",
    "midnightsuns.2k.com",
    "www.supergiantgames.com",
    "www.mobiusdigitalgames.com",
    "whitethorngames.com",
    "www.fellowtraveller.games",
    "thunderlotusgames.com",
}
SUCCESS_RESULT = "CAPTURED_HTTP_2XX"
FAILURE_RESULTS = {"FAILED_TRANSPORT", "FAILED_TIMEOUT_ABORTED", "FAILED_HTTP_STATUS"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
HTTP_RE = re.compile(r"^[0-9]{3}$")


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


def official_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and parsed.hostname in ALLOWED_OFFICIAL_HOSTS


def validate() -> tuple[list[str], Counter[str]]:
    errors: list[str] = []
    ledger_header, ledger_rows, ledger_errors = read_tsv(LEDGER_PATH)
    fp_header, fp_rows, fp_errors = read_tsv(FINGERPRINT_PATH)
    errors.extend(ledger_errors)
    errors.extend(fp_errors)
    if not ledger_header or not fp_header:
        return errors, Counter()

    if fp_header != EXPECTED_HEADER:
        errors.append(f"fingerprint header drift: {fp_header!r}")

    if len(ledger_rows) != 15:
        errors.append(f"source ledger must contain 15 rows, found {len(ledger_rows)}")
    if len(fp_rows) != 15:
        errors.append(f"fingerprint table must contain 15 rows, found {len(fp_rows)}")

    ledger_ids = [row.get("evidence_id", "") for row in ledger_rows]
    fp_ids = [row.get("evidence_id", "") for row in fp_rows]
    if len(set(ledger_ids)) != len(ledger_ids):
        errors.append("source ledger evidence_id values are not unique")
    if len(set(fp_ids)) != len(fp_ids):
        errors.append("fingerprint evidence_id values are not unique")
    if set(ledger_ids) != EXPECTED_EVIDENCE_IDS:
        errors.append(
            "source ledger evidence set drift: "
            f"missing={sorted(EXPECTED_EVIDENCE_IDS - set(ledger_ids))}, "
            f"extra={sorted(set(ledger_ids) - EXPECTED_EVIDENCE_IDS)}"
        )
    if set(fp_ids) != set(ledger_ids):
        errors.append(
            "fingerprint-to-ledger one-to-one mismatch: "
            f"missing={sorted(set(ledger_ids) - set(fp_ids))}, "
            f"extra={sorted(set(fp_ids) - set(ledger_ids))}"
        )

    ledger_by_id = {row.get("evidence_id", ""): row for row in ledger_rows}
    result_counts: Counter[str] = Counter()

    for row in ledger_rows:
        evidence_id = row.get("evidence_id", "<missing>")
        if not row.get("source_kind", "").startswith("official_"):
            errors.append(f"{evidence_id}: source_kind is not official_*")
        if not official_https_url(row.get("official_url", "")):
            errors.append(f"{evidence_id}: ledger URL is not an allowed official HTTPS host")

    for row in fp_rows:
        evidence_id = row.get("evidence_id", "<missing>")
        ledger = ledger_by_id.get(evidence_id)
        if ledger is None:
            continue

        expected_reference = f"source-evidence-ledger.tsv#{evidence_id}"
        if row.get("ledger_reference") != expected_reference:
            errors.append(f"{evidence_id}: ledger_reference must be {expected_reference}")
        if row.get("requested_url") != ledger.get("official_url"):
            errors.append(f"{evidence_id}: requested_url differs from ledger official_url")
        if row.get("locator") != ledger.get("page_or_section_locator"):
            errors.append(f"{evidence_id}: locator differs from ledger locator")
        if not official_https_url(row.get("requested_url", "")):
            errors.append(f"{evidence_id}: requested_url is not an allowed official HTTPS host")

        captured_at = row.get("captured_at_utc", "")
        try:
            parsed_time = datetime.strptime(captured_at, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            errors.append(f"{evidence_id}: captured_at_utc is not strict UTC ISO-8601")
        else:
            if parsed_time.strftime("%Y-%m-%d") != ledger.get("checked_on"):
                errors.append(f"{evidence_id}: capture date differs from ledger checked_on")

        if not row.get("dynamic_content_caveat"):
            errors.append(f"{evidence_id}: missing dynamic-content caveat")
        if not row.get("request_profile"):
            errors.append(f"{evidence_id}: missing request profile")

        length_text = row.get("content_length_bytes", "")
        if not length_text.isdigit():
            errors.append(f"{evidence_id}: content_length_bytes must be a non-negative integer")
            content_length = -1
        else:
            content_length = int(length_text)

        result = row.get("capture_result", "")
        result_counts[result] += 1
        if result == SUCCESS_RESULT:
            status = row.get("http_status", "")
            if not HTTP_RE.fullmatch(status) or not 200 <= int(status) <= 299:
                errors.append(f"{evidence_id}: successful capture requires HTTP 2xx")
            if not official_https_url(row.get("final_url", "")):
                errors.append(f"{evidence_id}: successful final_url is not an allowed official HTTPS host")
            content_type = row.get("content_type", "").lower()
            if not (content_type.startswith("text/html") or content_type.startswith("application/pdf")):
                errors.append(f"{evidence_id}: unexpected successful content_type")
            if content_length <= 0:
                errors.append(f"{evidence_id}: successful capture requires positive content length")
            if not HASH_RE.fullmatch(row.get("raw_sha256", "")):
                errors.append(f"{evidence_id}: successful capture requires lowercase SHA-256")
            if row.get("failure_reason") != "NONE":
                errors.append(f"{evidence_id}: successful capture must use failure_reason=NONE")
            if row.get("body_retention") != "metadata_and_sha_only_body_not_retained":
                errors.append(f"{evidence_id}: successful body-retention boundary drift")
        elif result in FAILURE_RESULTS:
            status = row.get("http_status", "")
            status_is_failure = (
                status in {"000", "NOT_OBSERVED"}
                or (HTTP_RE.fullmatch(status) is not None and not 200 <= int(status) <= 299)
            )
            if not status_is_failure:
                errors.append(f"{evidence_id}: failed capture has a success-like HTTP status")
            final_url = row.get("final_url", "")
            if final_url not in {"", "NOT_OBSERVED"} and not official_https_url(final_url):
                errors.append(f"{evidence_id}: failed final_url is neither unknown nor allowed official HTTPS")
            if row.get("raw_sha256", ""):
                errors.append(f"{evidence_id}: failed capture must not claim a body SHA-256")
            if row.get("failure_reason", "") in {"", "NONE"}:
                errors.append(f"{evidence_id}: failed capture requires an explicit reason")
            if row.get("body_retention") != "metadata_only_no_body_retained":
                errors.append(f"{evidence_id}: failed body-retention boundary drift")
        else:
            errors.append(f"{evidence_id}: unknown capture_result={result!r}")

    return errors, result_counts


def main() -> int:
    errors, counts = validate()
    if errors:
        print(f"FAIL D01 source response fingerprints: {len(errors)} error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    captured = counts[SUCCESS_RESULT]
    failed = sum(counts[result] for result in FAILURE_RESULTS)
    print(
        "PASS D01 source response fingerprints: "
        f"15/15 ledger rows linked one-to-one; captured_http_2xx={captured}; "
        f"failed_honestly_without_hash={failed}; official hosts and boundary semantics valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
