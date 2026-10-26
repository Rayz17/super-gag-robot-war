#!/usr/bin/env python3
"""Read-only release entry point for the Candidate game-design package.

The central checker intentionally does not invoke this script.  This wrapper
runs every package-level specialist that can currently execute without a Build
or user authorization, streams all outputs unchanged, and returns the first
non-zero child exit code.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CHECKS = (
    ("central Candidate contracts", SCRIPT_DIR / "check_candidate_contracts.py", ()),
    (
        "public system contract semantics",
        SCRIPT_DIR / "check_public_system_contract_semantics.py",
        (),
    ),
    ("D01 source/response fingerprints", SCRIPT_DIR / "check_d01_source_response_fingerprints.py", ()),
    ("D01 synthesis/evidence coverage", SCRIPT_DIR / "check_d01_synthesis_evidence_coverage.py", ()),
    ("D02 core-loop payload closure", SCRIPT_DIR / "check_d02_d03_core_loop_payload_bindings.py", ()),
    ("D03 economy invariant paper cases", SCRIPT_DIR / "check_d03_economy_invariants.py", ()),
    ("D03 RunState v2 paper contracts", SCRIPT_DIR / "check_d03_runstate_v2_contracts.py", ()),
    ("D04 P1 declared-event ledger", SCRIPT_DIR / "check_d04_p1_v0_2.py", ()),
    ("Candidate authorization contracts", SCRIPT_DIR / "check_candidate_authorization_contracts.py", ()),
    ("first-decision sign-off pack", SCRIPT_DIR / "check_first_decision_signoff_pack.py", ()),
    ("D05 auxiliary R2 paper preflights", SCRIPT_DIR / "check_d05_auxiliary_second_instances.py", ()),
    ("D06 C02 paper fixtures", SCRIPT_DIR / "check_d06_c02_paper_fixtures.py", ()),
    ("D09 gate dependency order", SCRIPT_DIR / "check_d09_gate_dependency_order.py", ()),
    ("D10 prototype/test bijection", SCRIPT_DIR / "check_d10_test_registry_bijection.py", ()),
    ("D10 prototype/preflight coverage", SCRIPT_DIR / "check_d10_preflight_coverage.py", ()),
    ("D10 human Session evidence contract", SCRIPT_DIR / "check_d10_human_playtest_sessions.py", ()),
    ("D11 budget calibration contracts", SCRIPT_DIR / "check_d11_budget_calibration.py", ()),
    (
        "D07 roster coverage regeneration",
        SCRIPT_DIR / "build_series_roster_coverage_crosswalk.py",
        ("--check",),
    ),
)


def portable_exit_code(return_code: int) -> int:
    if return_code >= 0:
        return return_code
    return min(255, 128 + abs(return_code))


def main() -> int:
    first_failure = 0
    for label, script_path, extra_args in CHECKS:
        if not script_path.is_file():
            print(f"[candidate-release] FAIL missing {label}: {script_path}")
            if first_failure == 0:
                first_failure = 1
            continue
        print(f"[candidate-release] RUN {label}", flush=True)
        completed = subprocess.run(
            [sys.executable, "-B", str(script_path), *extra_args],
            cwd=SCRIPT_DIR.parent,
            check=False,
        )
        child_code = portable_exit_code(completed.returncode)
        outcome = "PASS" if child_code == 0 else "FAIL"
        print(
            f"[candidate-release] {outcome} {label} exit={child_code}",
            flush=True,
        )
        if child_code != 0 and first_failure == 0:
            first_failure = child_code

    if first_failure:
        print(
            f"[candidate-release] RESULT FAIL first_exit={first_failure}",
            flush=True,
        )
        return first_failure
    print("[candidate-release] RESULT PASS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
