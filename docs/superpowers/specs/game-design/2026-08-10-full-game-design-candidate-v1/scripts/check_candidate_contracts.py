#!/usr/bin/env python3
"""Read-only static checks for the full-game-design Candidate package.

The checker intentionally validates Candidate design contracts only.  It never
writes generated files and does not promote any result into Canon, Reader, or
Runtime authority.
"""

from __future__ import annotations

import csv
import fnmatch
import hashlib
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SYSTEMS = {
    "SYS-NARR",
    "SYS-TACT",
    "SYS-C2",
    "SYS-ROSTER",
    "SYS-BODY",
    "SYS-EXPL",
    "SYS-HUB",
    "SYS-REL",
    "SYS-ARCH",
    "SYS-WORLD",
    "SYS-SETTLE",
    "SYS-PRESENT",
}
EXCLUDED_OWNER_STATES = {"ST_IDENTITY", "ST_UI_PROJECTION"}
EXPECTED_OPERATION_SEQUENCES = {
    "C02E04": "OP_C02_TOURNAMENT>OP_C02_STAGE_ACCIDENT",
    "C02E05": "OP_C02_STAGE_ACCIDENT>OP_C02_DEPARTURE",
}
EXPECTED_EPISODE_SETTLEMENTS = {
    "C01E04": (1, 0),
    "C02E04": (1, 0),
    "C02E05": (2, 1),
    "C03E03": (1, 0),
    "C03E04": (1, 1),
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SYSTEM_REF_RE = re.compile(r"\bSYS-[A-Z0-9-]+\b")
STATE_REF_RE = re.compile(r"\bST_[A-Z0-9_]+\b")
DELIVERABLE_REF_RE = re.compile(r"\bD(?:0[1-9]|1[0-2])\b")
NO_SINGLE_CURRENT_CANON_ENTITY = "NONE_NO_SINGLE_CURRENT_CANON_ENTITY"


class Checks:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def passed(self, message: str) -> None:
        self.passes.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        raw = list(reader)
    if not raw:
        return [], []
    header = raw[0]
    rows = [dict(zip(header, row)) for row in raw[1:] if row]
    return header, rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(repo_root: Path, *args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def check_tsv_widths(checks: Checks) -> None:
    files = sorted(PACKAGE_ROOT.rglob("*.tsv"))
    checks.require(bool(files), "No TSV files found in Candidate package")
    for path in files:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle, delimiter="\t"))
        rel = path.relative_to(PACKAGE_ROOT)
        checks.require(bool(rows), f"Empty TSV: {rel}")
        if not rows:
            continue
        expected = len(rows[0])
        checks.require(expected > 0, f"TSV has empty header: {rel}")
        for line_no, row in enumerate(rows[1:], start=2):
            if not row:
                continue
            checks.require(
                len(row) == expected,
                f"TSV width mismatch: {rel}:{line_no} has {len(row)} columns, expected {expected}",
            )
    checks.passed(f"TSV widths: {len(files)} files")


def check_workstream_parking(checks: Checks) -> None:
    """Keep parked chapter/setting inventories out of the current gameplay workstream."""

    blueprint_text = (PACKAGE_ROOT / "chapters/C01-C03-playable-blueprints.md").read_text(
        encoding="utf-8"
    )
    for token in {"parked", "not_current", "not_counted_as_gameplay_progress"}:
        checks.require(token in blueprint_text, f"Opening blueprint lacks parking token: {token}")

    parked_table_expectations = {
        "chapters/c01-c03-episode-play-contracts.tsv": 13,
        "chapters/c01-c03-playable-units.tsv": 25,
        "chapters/c01-c03-previs-needs.tsv": 20,
        "chapters/c01-c03-story-state-seeds.tsv": 13,
    }
    parking_fields = {
        "workstream_state",
        "current_next_step",
        "gameplay_progress_counting",
    }
    for relative_path, expected_rows in parked_table_expectations.items():
        header, rows = read_tsv(PACKAGE_ROOT / relative_path)
        checks.require(
            parking_fields <= set(header),
            f"Opening table lacks parking fields: {relative_path}",
        )
        checks.require(
            len(rows) == expected_rows,
            f"Opening table row count drift: {relative_path}={len(rows)}, expected {expected_rows}",
        )
        for row in rows:
            checks.require(
                row.get("workstream_state") == "parked"
                and row.get("current_next_step") == "not_current"
                and row.get("gameplay_progress_counting") == "not_counted",
                f"Opening table row escaped parking: {relative_path}:{next(iter(row.values()), '')}",
            )

    chapter_header, chapter_rows = read_tsv(PACKAGE_ROOT / "data/chapter-scope-allocation.tsv")
    checks.require(
        "workstream_state" in chapter_header,
        "Chapter scope allocation lacks workstream_state",
    )
    checks.require(len(chapter_rows) == 22, f"Expected 22 chapter scope rows, found {len(chapter_rows)}")
    checks.require(
        all(row.get("workstream_state") == "parked_forecast_not_current_plan" for row in chapter_rows),
        "Every C01-C22 scope allocation must remain parked forecast, not a current plan",
    )

    stage1_ids = {f"BF{number:04d}" for number in range(1, 6)}
    stage2_ids = {"BF0006", "BF0007", "BF0011", "BF0012", "BF0017", "BF0020"}
    stage4_ids = {"BF0038", "BF0042", "BF0049", "BF0050", "BF0051"}
    all_backfill_ids = {f"BF{number:04d}" for number in range(1, 54)}
    stage3_ids = all_backfill_ids - stage1_ids - stage2_ids - stage4_ids
    expected_phase_by_id = {
        **{backfill_id: "stage1_public_system" for backfill_id in stage1_ids},
        **{backfill_id: "stage2_cross_chapter_foundation" for backfill_id in stage2_ids},
        **{backfill_id: "stage3_c01_c03_validation" for backfill_id in stage3_ids},
        **{backfill_id: "stage4_per_chapter_adaptation" for backfill_id in stage4_ids},
    }
    backfill_header, backfill_rows = read_tsv(PACKAGE_ROOT / "data/setting-backfill-register.tsv")
    checks.require(
        {"workstream_phase", "workstream_state"} <= set(backfill_header),
        "Setting backfill register lacks workstream phase/state",
    )
    backfill_by_id = {row["backfill_id"]: row for row in backfill_rows}
    checks.require(
        set(backfill_by_id) == all_backfill_ids,
        f"Setting backfill ID coverage drift: {sorted(set(backfill_by_id) ^ all_backfill_ids)}",
    )
    for backfill_id, expected_phase in expected_phase_by_id.items():
        row = backfill_by_id.get(backfill_id)
        if not row:
            continue
        checks.require(
            row.get("workstream_phase") == expected_phase,
            f"Backfill phase drift: {backfill_id}={row.get('workstream_phase')}, expected {expected_phase}",
        )
        expected_state = (
            "current_public_system_candidate"
            if expected_phase == "stage1_public_system"
            else "parked_not_current_not_counted"
        )
        checks.require(
            row.get("workstream_state") == expected_state,
            f"Backfill workstream state drift: {backfill_id}={row.get('workstream_state')}, expected {expected_state}",
        )

    checks.passed(
        "Workstream parking: four opening tables parked; C01-C22 scope forecast parked; "
        "53 backfills classified as stage1=5, stage2=6, stage3=37, stage4=5"
    )


def check_markdown_links(checks: Checks) -> None:
    markdown_files = sorted(PACKAGE_ROOT.rglob("*.md"))
    local_count = 0
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            local_count += 1
            resolved = (path.parent / target).resolve()
            checks.require(
                resolved.exists(),
                f"Broken Markdown link: {path.relative_to(PACKAGE_ROOT)} -> {raw_target}",
            )
    checks.passed(f"Markdown local links: {local_count} targets in {len(markdown_files)} files")


def check_research_evidence(checks: Checks) -> None:
    _, sample_rows = read_tsv(PACKAGE_ROOT / "research/comparative-mechanic-matrix.tsv")
    sample_ids = {row["sample_id"] for row in sample_rows}
    checks.require(len(sample_rows) == 35, f"Expected 35 comparative samples, found {len(sample_rows)}")
    checks.require(len(sample_ids) == 35, "Comparative sample IDs are not unique")

    _, evidence_rows = read_tsv(PACKAGE_ROOT / "research/source-evidence-ledger.tsv")
    checks.require(len(evidence_rows) == 15, f"Expected 15 key source-evidence rows, found {len(evidence_rows)}")
    checks.require(
        len({row["evidence_id"] for row in evidence_rows}) == len(evidence_rows),
        "Research evidence IDs are not unique",
    )
    for row in evidence_rows:
        checks.require(row["sample_id"] in sample_ids, f"Unknown research sample: {row['evidence_id']}:{row['sample_id']}")
        checks.require(row["official_url"].startswith("https://"), f"Non-HTTPS official source: {row['evidence_id']}")
        checks.require(row["checked_on"] == "2026-08-10", f"Unexpected research check date: {row['evidence_id']}")
        checks.require(bool(row["page_or_section_locator"]), f"Missing research locator: {row['evidence_id']}")
        checks.require(bool(row["supported_candidate_claim"]), f"Missing supported claim: {row['evidence_id']}")
        checks.require(bool(row["does_not_prove"]), f"Missing inference boundary: {row['evidence_id']}")
        checks.require(
            "no_snapshot" in row["capture_level"] or "no_local_snapshot" in row["capture_level"],
            f"Research capture level must state snapshot limit: {row['evidence_id']}",
        )
        checks.require(
            row["status"] == "verified_for_candidate_hypothesis",
            f"Unexpected research evidence status: {row['evidence_id']}:{row['status']}",
        )

    _, decision_rows = read_tsv(PACKAGE_ROOT / "research/mechanic-synthesis-decisions.tsv")
    for row in decision_rows:
        for sample_id in filter(None, row["source_samples"].split(";")):
            checks.require(sample_id in sample_ids, f"Unknown synthesis source sample: {row['decision_id']}:{sample_id}")
    checks.passed(
        "Research evidence: 35 samples, 15 key official-source locators with explicit inference limits; "
        "synthesis sample references resolve"
    )


def check_deliverable_coverage(checks: Checks) -> None:
    _, deliverables = read_tsv(PACKAGE_ROOT / "01-deliverable-registry.tsv")
    expected_ids = {f"D{number:02d}" for number in range(1, 13)}
    deliverable_ids = {row["deliverable_id"] for row in deliverables}
    checks.require(len(deliverables) == 12, f"Expected 12 deliverables, found {len(deliverables)}")
    checks.require(deliverable_ids == expected_ids, f"Deliverable set differs: {sorted(deliverable_ids ^ expected_ids)}")
    for row in deliverables:
        checks.require(
            row["status"].startswith(("candidate_", "parked_")),
            f"Deliverable escaped Candidate/parked boundary: {row['deliverable_id']}",
        )
        for raw_path in filter(None, row["output_paths"].split(";")):
            checks.require(
                (PACKAGE_ROOT / raw_path).exists(),
                f"Missing deliverable output: {row['deliverable_id']}:{raw_path}",
            )
        for dependency in DELIVERABLE_REF_RE.findall(row["dependencies"]):
            checks.require(dependency in deliverable_ids, f"Unknown deliverable dependency: {row['deliverable_id']}:{dependency}")

    _, requirements = read_tsv(PACKAGE_ROOT / "data/goal-deliverable-evidence-matrix.tsv")
    expected_requirements = {f"REQ-{number:02d}" for number in range(1, 13)}
    requirement_ids = {row["requirement_id"] for row in requirements}
    checks.require(len(requirements) == 12, f"Expected 12 goal-evidence rows, found {len(requirements)}")
    checks.require(
        requirement_ids == expected_requirements,
        f"Goal requirement set differs: {sorted(requirement_ids ^ expected_requirements)}",
    )
    mapped_deliverables: set[str] = set()
    for row in requirements:
        row_deliverables = set(DELIVERABLE_REF_RE.findall(row["mapped_deliverables"]))
        mapped_deliverables.update(row_deliverables)
        checks.require(bool(row_deliverables), f"No mapped deliverable: {row['requirement_id']}")
        checks.require(
            row_deliverables <= deliverable_ids,
            f"Unknown goal mapping: {row['requirement_id']}:{sorted(row_deliverables - deliverable_ids)}",
        )
        for raw_path in filter(None, row["primary_artifacts"].split(";")):
            checks.require(
                (PACKAGE_ROOT / raw_path).exists(),
                f"Missing goal evidence artifact: {row['requirement_id']}:{raw_path}",
            )
    checks.require(
        mapped_deliverables == deliverable_ids,
        f"Not all deliverables appear in the goal evidence matrix: {sorted(deliverable_ids - mapped_deliverables)}",
    )
    checks.passed("Goal coverage: 12 Candidate deliverables and 12 user-required output rows; all declared artifacts resolve")


def check_prototype_paper_fixtures(checks: Checks) -> None:
    """Keep implementable paper fixtures distinct from Builds and human evidence."""

    expected_fixture_ids = {
        "FX-D04-P1",
        "FX-D04-P2",
        "FX-D04-P3",
        "FX-D05-EX1",
        "FX-D05-EX2",
        "FX-D05-EX3",
        "FX-D05-HUB1",
        "FX-D05-SET1",
        "FX-D05-EX1-R2-PAPER",
        "FX-D05-EX2-R2-PAPER",
        "FX-D05-EX3-R2-PAPER",
    }
    required_prototypes = {
        "D04-P1-A",
        "D04-P1-B",
        "D04-P1-C",
        "D04-P1-D",
        "D04-P2-CROSSOVER",
        "D04-P2",
        "D04-P3",
        "P-EX1",
        "P-EX2",
        "P-EX3",
        "P-EX1-R2",
        "P-EX2-R2",
        "P-EX3-R2",
        "P-HUB1",
        "P-SET1",
    }
    r2_preflight_fixture_ids = {
        "FX-D05-EX1-R2-PAPER",
        "FX-D05-EX2-R2-PAPER",
        "FX-D05-EX3-R2-PAPER",
    }
    _, prototype_rows = read_tsv(PACKAGE_ROOT / "data/prototype-test-registry.tsv")
    prototype_ids = {row["prototype_id"] for row in prototype_rows}
    _, fixture_rows = read_tsv(PACKAGE_ROOT / "data/prototype-paper-fixture-registry.tsv")
    fixture_ids = {row["fixture_id"] for row in fixture_rows}
    checks.require(len(fixture_rows) == 11, f"Expected 11 paper-fixture rows, found {len(fixture_rows)}")
    checks.require(fixture_ids == expected_fixture_ids, f"Paper-fixture set differs: {sorted(fixture_ids ^ expected_fixture_ids)}")

    covered_prototypes: set[str] = set()
    defined_count = 0
    for row in fixture_rows:
        row_prototypes = set(filter(None, row["prototype_ids"].split(";")))
        covered_prototypes.update(row_prototypes)
        checks.require(row_prototypes <= prototype_ids, f"Unknown fixture prototype: {row['fixture_id']}:{sorted(row_prototypes - prototype_ids)}")
        for raw_path in filter(None, row["required_contract_refs"].split(";")):
            checks.require((PACKAGE_ROOT / raw_path).is_file(), f"Missing fixture contract: {row['fixture_id']}:{raw_path}")
        checks.require(row["build_status"] == "zero_build", f"Paper fixture must remain zero_build: {row['fixture_id']}")
        checks.require(row["human_evidence_status"] == "not_run", f"Paper fixture must remain human not_run: {row['fixture_id']}")
        checks.require(row["status"].startswith("candidate_"), f"Non-Candidate fixture status: {row['fixture_id']}")

        definition_fields = {
            row["initial_state_defined"],
            row["player_choice_trace_defined"],
            row["expected_outcomes_defined"],
            row["automated_assertion_spec_defined"],
        }
        checks.require(
            definition_fields in ({"yes"}, {"pending_fixture"}),
            f"Fixture definition fields must move atomically: {row['fixture_id']}:{sorted(definition_fields)}",
        )
        if definition_fields == {"yes"}:
            defined_count += 1
            checks.require(
                (PACKAGE_ROOT / row["artifact_path"]).is_file(),
                f"Defined fixture artifact missing: {row['fixture_id']}:{row['artifact_path']}",
            )
            if row["fixture_id"] in r2_preflight_fixture_ids:
                checks.require(
                    row["status"] == "candidate_paper_preflight_no_replication_evidence",
                    f"R2 paper preflight overclaims evidence: {row['fixture_id']}:{row['status']}",
                )
                checks.require(
                    "no_replication_evidence" in row["authority_boundary"],
                    f"R2 paper preflight lacks no-replication boundary: {row['fixture_id']}",
                )
            else:
                checks.require(
                    row["status"] == "candidate_paper_fixture_defined",
                    f"Defined fixture has wrong status: {row['fixture_id']}:{row['status']}",
                )
        else:
            checks.require(
                row["status"] == "candidate_fixture_in_progress",
                f"Pending fixture has wrong status: {row['fixture_id']}:{row['status']}",
            )

    checks.require(
        covered_prototypes == required_prototypes,
        f"Paper-fixture prototype coverage differs: missing={sorted(required_prototypes - covered_prototypes)}, "
        f"extra={sorted(covered_prototypes - required_prototypes)}",
    )
    checks.passed(
        f"Prototype paper fixtures: 11 registry rows cover 15 prototypes; {defined_count} defined; "
        "three R2 rows remain no_replication_evidence; all remain zero_build and human not_run"
    )


def check_systems_states_and_owners(checks: Checks) -> tuple[set[str], set[str]]:
    _, node_rows = read_tsv(PACKAGE_ROOT / "data/system-node-contracts.tsv")
    _, state_rows = read_tsv(PACKAGE_ROOT / "data/system-state-contracts.tsv")
    systems = {row["system_id"] for row in node_rows}
    states = {row["state_id"] for row in state_rows}

    checks.require(len(node_rows) == 12, f"Expected 12 system rows, found {len(node_rows)}")
    checks.require(len(systems) == 12, f"Expected 12 unique systems, found {len(systems)}")
    checks.require(systems == EXPECTED_SYSTEMS, f"System set differs: {sorted(systems ^ EXPECTED_SYSTEMS)}")
    checks.require(len(state_rows) == 26, f"Expected 26 state rows, found {len(state_rows)}")
    checks.require(len(states) == 26, f"Expected 26 unique states, found {len(states)}")
    for row in state_rows:
        checks.require(
            row["owner_system"] in systems,
            f"Unknown owner_system {row['owner_system']} for {row['state_id']}",
        )

    referenced_systems: set[str] = set()
    referenced_states: set[str] = set()
    for path in sorted((*PACKAGE_ROOT.rglob("*.tsv"), *PACKAGE_ROOT.rglob("*.md"))):
        text = path.read_text(encoding="utf-8")
        referenced_systems.update(SYSTEM_REF_RE.findall(text))
        referenced_states.update(STATE_REF_RE.findall(text))
    checks.require(
        referenced_systems <= systems,
        f"Unknown SYS references: {sorted(referenced_systems - systems)}",
    )
    checks.require(
        referenced_states <= states,
        f"Unknown ST references: {sorted(referenced_states - states)}",
    )

    _, owner_rows = read_tsv(PACKAGE_ROOT / "data/settlement-owner-prepare-commit-contracts.tsv")
    checks.require(len(owner_rows) == 10, f"Expected 10 mutable owner groups, found {len(owner_rows)}")
    checks.require(
        len({row["owner_group_id"] for row in owner_rows}) == 10,
        "Mutable owner_group_id values are not unique",
    )
    owner_membership: defaultdict[str, list[str]] = defaultdict(list)
    state_owner = {row["state_id"]: row["owner_system"] for row in state_rows}
    for row in owner_rows:
        checks.require(row["owner_system"] in systems, f"Unknown owner group system: {row['owner_system']}")
        for state_id in filter(None, row["state_ids"].split(";")):
            owner_membership[state_id].append(row["owner_group_id"])
            checks.require(state_id in states, f"Unknown owner-group state: {state_id}")
            if state_id in state_owner:
                checks.require(
                    state_owner[state_id] == row["owner_system"],
                    f"Owner mismatch for {state_id}: state={state_owner[state_id]}, group={row['owner_system']}",
                )
    mutable_states = states - EXCLUDED_OWNER_STATES
    covered_states = set(owner_membership)
    checks.require(
        covered_states == mutable_states,
        "Owner coverage differs: missing="
        f"{sorted(mutable_states - covered_states)}, extra={sorted(covered_states - mutable_states)}",
    )
    checks.require(
        not (covered_states & EXCLUDED_OWNER_STATES),
        f"Immutable/derived states included in mutable owner groups: {sorted(covered_states & EXCLUDED_OWNER_STATES)}",
    )
    duplicate_states = {state: groups for state, groups in owner_membership.items() if len(groups) != 1}
    checks.require(not duplicate_states, f"States covered by multiple owner groups: {duplicate_states}")
    checks.passed(
        "System/state references: 12 systems, 26 states; 10 mutable owner groups cover 24 states; "
        "ST_IDENTITY and ST_UI_PROJECTION explicitly excluded"
    )
    return systems, states


def check_series_mechanic_lifecycle(checks: Checks, systems: set[str]) -> None:
    """Audit normalized Candidate lifecycle contracts without treating planning as evidence."""

    def refs(raw: str, none_token: str = "NONE") -> list[str]:
        return [value for value in raw.split(";") if value and value != none_token]

    def validate_prototype_refs(owner: str, raw: str) -> None:
        for raw_ref in refs(raw):
            if raw_ref.startswith("paper_fixture:"):
                fixture_id = raw_ref.split(":", 1)[1]
                checks.require(fixture_id in chapter_fixture_ids, f"Unknown chapter paper fixture evidence: {owner}:{fixture_id}")
            elif raw_ref.startswith(("pending:", "generic_only:", "prototype:")):
                prototype_id = raw_ref.split(":", 1)[1]
                checks.require(prototype_id in prototype_ids, f"Unknown prototype evidence: {owner}:{prototype_id}")
            else:
                checks.require(raw_ref.startswith("OPEN:"), f"Evidence ref must be paper_fixture/pending/generic_only/prototype/OPEN: {owner}:{raw_ref}")

    _, unlock_rows = read_tsv(PACKAGE_ROOT / "data/series-mechanic-unlock-spine.tsv")
    _, lifecycle_rows = read_tsv(PACKAGE_ROOT / "data/series-mechanic-lifecycle-ledger.tsv")
    _, governance_rows = read_tsv(PACKAGE_ROOT / "data/series-mechanic-lifecycle-governance.tsv")
    _, system_coverage_rows = read_tsv(PACKAGE_ROOT / "data/series-system-lifecycle-coverage.tsv")
    _, second_rows = read_tsv(PACKAGE_ROOT / "data/series-mechanic-second-instance-ledger.tsv")
    _, evidence_rows = read_tsv(PACKAGE_ROOT / "data/series-mechanic-stage-evidence.tsv")
    _, fragment_rows = read_tsv(PACKAGE_ROOT / "data/series-mechanic-fragment-ledger.tsv")
    _, activity_rows = read_tsv(PACKAGE_ROOT / "data/series-mechanic-chapter-activity-ledger.tsv")
    _, prototype_rows = read_tsv(PACKAGE_ROOT / "data/prototype-test-registry.tsv")
    _, chapter_fixture_rows = read_tsv(PACKAGE_ROOT / "data/opening-chapter-paper-fixture-registry.tsv")
    _, state_rows = read_tsv(PACKAGE_ROOT / "data/system-state-contracts.tsv")
    _, decision_rows = read_tsv(PACKAGE_ROOT / "data/user-game-design-decisions.tsv")
    prototype_ids = {row["prototype_id"] for row in prototype_rows}
    chapter_fixture_ids = {row["fixture_id"] for row in chapter_fixture_rows}
    state_ids = {row["state_id"] for row in state_rows}
    decision_ids = {row["decision_id"] for row in decision_rows}
    expected_chapters = {f"C{number:02d}" for number in range(1, 23)}

    checks.require(len(lifecycle_rows) == 22, f"Expected 22 mechanic lifecycle rows, found {len(lifecycle_rows)}")
    lifecycle_ids = {row["lifecycle_id"] for row in lifecycle_rows}
    checks.require({row["chapter_id"] for row in lifecycle_rows} == expected_chapters, "Mechanic lifecycle chapter coverage must be exactly C01-C22")
    checks.require(len(lifecycle_ids) == len(lifecycle_rows), "Mechanic lifecycle IDs are not unique")
    checks.require(len({row["mechanic_id"] for row in lifecycle_rows}) == len(lifecycle_rows), "Mechanic IDs are not unique across lifecycle rows")
    lifecycle_by_id = {row["lifecycle_id"]: row for row in lifecycle_rows}

    unlock_mechanics: dict[str, str] = {}
    for row in unlock_rows:
        match = re.match(r"^([A-Z][A-Z0-9_]+)", row["one_new_dimension"])
        checks.require(match is not None, f"Cannot parse one_new_dimension ID: {row['chapter_id']}")
        if match:
            unlock_mechanics[row["chapter_id"]] = match.group(1)

    status_counts = Counter(row["status"] for row in lifecycle_rows)
    checks.require(set(status_counts) <= {"proposed", "open", "blocked"}, f"Lifecycle ledger contains completion-like or unknown status: {dict(status_counts)}")
    for row in lifecycle_rows:
        lifecycle_id = row["lifecycle_id"]
        checks.require(row["system_owner"] in systems, f"Unknown lifecycle system owner: {lifecycle_id}:{row['system_owner']}")
        checks.require(unlock_mechanics.get(row["chapter_id"]) == row["mechanic_id"], f"Lifecycle/unlock mechanic mismatch: {row['chapter_id']}:{row['mechanic_id']} != {unlock_mechanics.get(row['chapter_id'])}")
        for field in (
            "introduction_window", "guided_use", "first_independent_use", "second_data_only_instance",
            "second_instance_invariants", "mastery_test", "counterplay_window", "retire_or_merge",
            "return_if_absent", "prototype_evidence", "rationale",
        ):
            checks.require(bool(row[field]), f"Lifecycle field empty: {lifecycle_id}:{field}")
        checks.require(row["declared_new_dimension_count"] == "1", f"Lifecycle new-dimension declaration differs: {lifecycle_id}")
        checks.require(row["new_always_visible_commands_budget"] == "<=2", f"Lifecycle visible-command budget differs: {lifecycle_id}")
        checks.require(row["new_persistent_state_domains_budget"] == "0", f"Lifecycle state-domain budget differs: {lifecycle_id}")
        checks.require("RISK_NO_HUMAN_EVIDENCE" in refs(row["risk_codes"]), f"Lifecycle row lacks zero-human-evidence risk: {lifecycle_id}")
        validate_prototype_refs(lifecycle_id, row["prototype_evidence"])

    # Per-row governance preserves Candidate authority and separates primary/collaborating owners.
    checks.require(len(governance_rows) == 22, f"Expected 22 lifecycle governance rows, found {len(governance_rows)}")
    checks.require({row["lifecycle_id"] for row in governance_rows} == lifecycle_ids, "Lifecycle governance coverage differs from lifecycle ledger")
    checks.require(len({row["lifecycle_id"] for row in governance_rows}) == len(governance_rows), "Duplicate lifecycle governance rows")
    governance_by_id = {row["lifecycle_id"]: row for row in governance_rows}
    unwired_chains = 0
    for row in governance_rows:
        lifecycle_id = row["lifecycle_id"]
        primary = row["primary_system_owner"]
        collaborators = refs(row["collaborating_system_owners"])
        row_states = refs(row["state_refs"])
        checks.require(primary == lifecycle_by_id[lifecycle_id]["system_owner"], f"Lifecycle primary owner drift: {lifecycle_id}:{primary}")
        checks.require(primary in systems, f"Unknown lifecycle primary owner: {lifecycle_id}:{primary}")
        checks.require(set(collaborators) <= systems, f"Unknown lifecycle collaborator: {lifecycle_id}:{sorted(set(collaborators) - systems)}")
        checks.require(primary not in collaborators, f"Primary owner repeated as collaborator: {lifecycle_id}:{primary}")
        checks.require(bool(row_states) and set(row_states) <= state_ids, f"Unknown or empty lifecycle state refs: {lifecycle_id}:{sorted(set(row_states) - state_ids)}")
        checks.require(row["authority_level"] == "candidate_only", f"Lifecycle authority is not Candidate-only: {lifecycle_id}")
        checks.require(bool(row["source_boundary"]) and bool(row["permitted_consumers"]) and bool(row["prohibited_consumers"]), f"Lifecycle governance boundary empty: {lifecycle_id}")
        checks.require(set(refs(row["decision_refs"])) <= decision_ids, f"Unknown lifecycle decision refs: {lifecycle_id}:{sorted(set(refs(row['decision_refs'])) - decision_ids)}")
        checks.require(bool(row["retired_shell_ids"]) and bool(row["preserved_base_verbs"]) and bool(row["postgame_behavior"]), f"Lifecycle retirement split incomplete: {lifecycle_id}")
        if row["chapter_chain_binding_status"] == "unwired_snapshot_only":
            unwired_chains += 1
        else:
            checks.require(row["chapter_chain_binding_status"] == "wired_live", f"Unknown chapter-chain binding status: {lifecycle_id}:{row['chapter_chain_binding_status']}")
        if lifecycle_by_id[lifecycle_id]["status"] == "blocked":
            checks.require(bool(refs(row["blocking_refs"])), f"Blocked lifecycle lacks blocking refs: {lifecycle_id}")

    # Twelve systems must be represented, including horizontal services that own no chapter mechanic.
    checks.require(len(system_coverage_rows) == len(systems), f"Expected {len(systems)} system lifecycle coverage rows, found {len(system_coverage_rows)}")
    checks.require({row["system_id"] for row in system_coverage_rows} == systems, "System lifecycle coverage does not cover all 12 systems")
    checks.require(len({row["system_id"] for row in system_coverage_rows}) == len(system_coverage_rows), "Duplicate system lifecycle coverage rows")
    primary_coverage: dict[str, set[str]] = defaultdict(set)
    collaborator_coverage: dict[str, set[str]] = defaultdict(set)
    for row in system_coverage_rows:
        system_id = row["system_id"]
        primary_refs = set(refs(row["primary_lifecycle_refs"]))
        collaborator_refs = set(refs(row["collaborating_lifecycle_refs"]))
        checks.require(primary_refs <= lifecycle_ids, f"Unknown primary lifecycle coverage: {system_id}:{sorted(primary_refs - lifecycle_ids)}")
        checks.require(collaborator_refs <= lifecycle_ids, f"Unknown collaborating lifecycle coverage: {system_id}:{sorted(collaborator_refs - lifecycle_ids)}")
        checks.require(set(refs(row["state_refs"])) <= state_ids, f"Unknown system coverage states: {system_id}")
        if row["coverage_kind"] == "horizontal_service_no_chapter_owned_mechanic":
            checks.require(not primary_refs, f"Horizontal service unexpectedly owns chapter lifecycle: {system_id}")
            checks.require(row["coverage_status"] == "explicit_non_mechanic_system", f"Horizontal service lacks explicit status: {system_id}")
        else:
            checks.require(row["coverage_kind"] == "primary_mechanic" and bool(primary_refs), f"Unknown/empty system coverage kind: {system_id}")
        for lifecycle_id in primary_refs:
            primary_coverage[lifecycle_id].add(system_id)
        for lifecycle_id in collaborator_refs:
            collaborator_coverage[lifecycle_id].add(system_id)
    for lifecycle_id, governance in governance_by_id.items():
        checks.require(primary_coverage[lifecycle_id] == {governance["primary_system_owner"]}, f"System primary coverage drift: {lifecycle_id}:{primary_coverage[lifecycle_id]}")
        checks.require(collaborator_coverage[lifecycle_id] == set(refs(governance["collaborating_system_owners"])), f"System collaborator coverage drift: {lifecycle_id}")

    # A second-instance claim is not evidence until fixture/ruleset/schema/hash/isolation all resolve.
    checks.require(len(second_rows) == 22, f"Expected 22 structured second-instance rows, found {len(second_rows)}")
    checks.require({row["lifecycle_id"] for row in second_rows} == lifecycle_ids, "Second-instance lifecycle coverage differs")
    checks.require(len({row["second_instance_id"] for row in second_rows}) == len(second_rows), "Duplicate second-instance IDs")
    unavailable_hashes = 0
    contaminated_instances = 0
    second_by_lifecycle = {row["lifecycle_id"]: row for row in second_rows}
    for row in second_rows:
        validate_prototype_refs(row["second_instance_id"], row["fixture_ref"])
        checks.require(bool(row["ruleset_ref"]), f"Second instance ruleset ref empty: {row['second_instance_id']}")
        schema_states = refs(row["schema_ref"])
        checks.require(bool(schema_states) and set(schema_states) <= state_ids, f"Unknown/empty second-instance schema: {row['second_instance_id']}")
        checks.require(row["evidence_status"] in {"unverified", "blocked"}, f"Second instance uses completion-like evidence status: {row['second_instance_id']}")
        checks.require(row["isolation_status"] in {"not_checked", "known_cross_mechanic_contamination", "blocked_by_upstream_and_contamination", "blocked_by_missing_scope"}, f"Unknown second-instance isolation status: {row['second_instance_id']}")
        if row["content_hash"] == "UNAVAILABLE":
            unavailable_hashes += 1
        else:
            checks.require(re.fullmatch(r"[0-9a-f]{64}", row["content_hash"]) is not None, f"Malformed second-instance content hash: {row['second_instance_id']}")
        if "contamination" in row["isolation_status"]:
            contaminated_instances += 1

    # Prototype evidence is bound to introduction, replication, and mastery separately.
    expected_stages = {"introduction", "second_instance", "mastery"}
    checks.require(len(evidence_rows) == 66, f"Expected 66 lifecycle-stage evidence rows, found {len(evidence_rows)}")
    stage_coverage: dict[str, set[str]] = defaultdict(set)
    for row in evidence_rows:
        checks.require(row["lifecycle_id"] in lifecycle_ids, f"Unknown lifecycle stage evidence owner: {row['binding_id']}")
        checks.require(row["lifecycle_stage"] in expected_stages, f"Unknown lifecycle evidence stage: {row['binding_id']}:{row['lifecycle_stage']}")
        stage_coverage[row["lifecycle_id"]].add(row["lifecycle_stage"])
        validate_prototype_refs(row["binding_id"], row["prototype_refs"])
        checks.require(row["evidence_status"] in {"registered_pending", "missing", "blocked"}, f"Completion-like lifecycle evidence status: {row['binding_id']}")
    checks.require(all(stages == expected_stages for stages in stage_coverage.values()) and set(stage_coverage) == lifecycle_ids, "Each lifecycle must bind introduction/second_instance/mastery evidence exactly")
    c01_second_refs = next(row["prototype_refs"] for row in evidence_rows if row["lifecycle_id"] == "LIFE-C01" and row["lifecycle_stage"] == "second_instance")
    checks.require("PC02-E01-QUALIFIER" in c01_second_refs, "C01 second-instance evidence must include PC02-E01-QUALIFIER")
    c03_mastery_refs = next(row["prototype_refs"] for row in evidence_rows if row["lifecycle_id"] == "LIFE-C03" and row["lifecycle_stage"] == "mastery")
    checks.require("D04-P2" not in c03_mastery_refs, "D04-P2 cannot prove C03 engineering mastery")

    # Compound risks are derived from independently teachable fragment rows, never a hard-coded chapter list.
    fragment_by_lifecycle: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in fragment_rows:
        checks.require(row["lifecycle_id"] in lifecycle_ids, f"Unknown mechanic fragment owner: {row['fragment_id']}")
        checks.require(row["assessment"] in {"primary_fragment", "separable_candidate"}, f"Unknown fragment assessment: {row['fragment_id']}")
        checks.require(row["separate_teachability"] == "separately_teachable", f"Fragment teachability not explicit: {row['fragment_id']}")
        checks.require(set(refs(row["state_refs"])) <= state_ids, f"Unknown fragment states: {row['fragment_id']}")
        checks.require(bool(row["distinct_player_input"]) and bool(row["evidence_basis"]), f"Fragment lacks input/evidence basis: {row['fragment_id']}")
        fragment_by_lifecycle[row["lifecycle_id"]].append(row)
    checks.require(set(fragment_by_lifecycle) == lifecycle_ids, "Fragment ledger does not cover every lifecycle")
    compound_lifecycles: set[str] = set()
    for lifecycle_id, rows in fragment_by_lifecycle.items():
        primary_count = sum(row["assessment"] == "primary_fragment" for row in rows)
        checks.require(primary_count == 1, f"Lifecycle must have exactly one primary fragment: {lifecycle_id}:{primary_count}")
        derived_count = len(rows)
        ledger_row = lifecycle_by_id[lifecycle_id]
        try:
            declared_count = int(ledger_row["candidate_fragment_count"])
        except ValueError:
            declared_count = -1
        checks.require(declared_count == derived_count, f"Derived fragment count differs: {lifecycle_id}:{derived_count}!={declared_count}")
        if derived_count > 1:
            compound_lifecycles.add(lifecycle_id)
            checks.require(ledger_row["budget_assessment"] == "risk_compound_2_gt_1", f"Compound lifecycle risk not flagged: {lifecycle_id}")
            checks.require(any(code.startswith("RISK_COMPOUND_") for code in refs(ledger_row["risk_codes"])), f"Compound lifecycle lacks specific risk code: {lifecycle_id}")

    # Many-to-many chapter activity reveals cumulative stack, UI overlap, and planned review gaps.
    checks.require(len({row["activity_id"] for row in activity_rows}) == len(activity_rows), "Duplicate lifecycle activity IDs")
    allowed_activity_stages = {"introduction", "second_instance", "mastery", "planned_review"}
    activity_by_lifecycle: dict[str, list[dict[str, str]]] = defaultdict(list)
    active_by_chapter: dict[str, set[str]] = defaultdict(set)
    for row in activity_rows:
        checks.require(row["chapter_id"] in expected_chapters, f"Unknown lifecycle activity chapter: {row['activity_id']}:{row['chapter_id']}")
        checks.require(row["lifecycle_id"] in lifecycle_ids, f"Unknown lifecycle activity owner: {row['activity_id']}:{row['lifecycle_id']}")
        checks.require(row["activity_stage"] in allowed_activity_stages, f"Unknown lifecycle activity stage: {row['activity_id']}:{row['activity_stage']}")
        checks.require(bool(row["ui_surface_refs"]), f"Lifecycle activity lacks UI surface: {row['activity_id']}")
        combined = set(refs(row["combines_with"]))
        checks.require(combined <= lifecycle_ids and row["lifecycle_id"] not in combined, f"Invalid activity combination refs: {row['activity_id']}")
        checks.require(row["evidence_status"] in {"registered_pending", "planned_unverified", "blocked"}, f"Completion-like activity evidence: {row['activity_id']}")
        activity_by_lifecycle[row["lifecycle_id"]].append(row)
        active_by_chapter[row["chapter_id"]].add(row["lifecycle_id"])
    for lifecycle_id, lifecycle_row in lifecycle_by_id.items():
        introductions = [row for row in activity_by_lifecycle[lifecycle_id] if row["activity_stage"] == "introduction"]
        checks.require(len(introductions) == 1 and introductions[0]["chapter_id"] == lifecycle_row["chapter_id"], f"Lifecycle introduction activity mismatch: {lifecycle_id}")
        second = second_by_lifecycle[lifecycle_id]
        target_match = re.match(r"^(C\d{2})", second["target_window"])
        if target_match:
            target_chapter = target_match.group(1)
            checks.require(any(row["chapter_id"] == target_chapter and row["activity_stage"] == "second_instance" for row in activity_by_lifecycle[lifecycle_id]), f"Second-instance activity missing: {lifecycle_id}:{target_chapter}")
        mastery_match = re.match(r"^(C\d{2})", lifecycle_row["mastery_test"])
        if mastery_match:
            mastery_chapter = mastery_match.group(1)
            checks.require(any(row["chapter_id"] == mastery_chapter and row["activity_stage"] == "mastery" for row in activity_by_lifecycle[lifecycle_id]), f"Mastery activity missing: {lifecycle_id}:{mastery_chapter}")

    unresolved_dormancy: list[str] = []
    planned_review_count = 0
    for lifecycle_id, rows in activity_by_lifecycle.items():
        chapters = sorted({int(row["chapter_id"][1:]) for row in rows})
        planned_review_count += sum(row["activity_stage"] == "planned_review" for row in rows)
        for first, second in zip(chapters, chapters[1:]):
            if second - first > 3:
                unresolved_dormancy.append(f"{lifecycle_id}:C{first:02d}->C{second:02d}")
    checks.require(not unresolved_dormancy, f"Lifecycle dormancy exceeds three chapters without planned review: {unresolved_dormancy}")
    max_stack = max((len(values) for values in active_by_chapter.values()), default=0)
    high_stack = {chapter: len(values) for chapter, values in active_by_chapter.items() if len(values) > 4}

    if unwired_chains:
        checks.warn(f"Lifecycle/live chapter-chain join remains unwired for {unwired_chains}/22 rows; open/blocked states are Candidate snapshots, not live chain conclusions")
    if planned_review_count:
        checks.warn(f"Lifecycle activity ledger schedules {planned_review_count} review beats, but every review is unverified/blocked and none is chapter-chain evidence")
    if high_stack:
        checks.warn(f"Lifecycle cumulative UI/decision stack exceeds four mechanisms in {high_stack}; requires load prototype before chapter use")
    checks.warn(f"Second-instance evidence remains unverified: {unavailable_hashes}/22 content hashes unavailable; {contaminated_instances}/22 instances explicitly contaminated or upstream-blocked")
    checks.passed(
        "Series mechanic lifecycle: 22 mechanisms, 12-system coverage, 66 phase bindings, "
        f"{len(activity_rows)} chapter-activity rows; {len(compound_lifecycles)} compound risks derived from fragments; "
        f"max cumulative chapter stack={max_stack}; statuses={dict(status_counts)}"
    )


def first_mermaid_block(text: str) -> str | None:
    match = re.search(r"```mermaid\s*\n(.*?)```", text, flags=re.DOTALL)
    return match.group(1) if match else None


def check_system_graph(checks: Checks, systems: set[str]) -> None:
    graph_path = PACKAGE_ROOT / "04-full-game-system-graph.md"
    block = first_mermaid_block(graph_path.read_text(encoding="utf-8"))
    checks.require(block is not None, "No Mermaid block found in 04-full-game-system-graph.md")
    if block is None:
        return
    aliases: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r'\s*([A-Za-z][A-Za-z0-9_]*)\["(SYS-[A-Z0-9-]+)', line)
        if match:
            aliases[match.group(1)] = match.group(2)
    checks.require(set(aliases.values()) == systems, "First Mermaid graph does not declare exactly the 12 systems")

    graph_edges: list[tuple[str, str]] = []
    for line in block.splitlines():
        match = re.match(r"\s*([A-Za-z][A-Za-z0-9_]*)\s+(?:-->|-\.->)\s+([A-Za-z][A-Za-z0-9_]*)\s*$", line)
        if not match:
            continue
        source_alias, target_alias = match.groups()
        checks.require(source_alias in aliases, f"Unknown Mermaid source alias: {source_alias}")
        checks.require(target_alias in aliases, f"Unknown Mermaid target alias: {target_alias}")
        if source_alias in aliases and target_alias in aliases:
            graph_edges.append((aliases[source_alias], aliases[target_alias]))

    _, edge_rows = read_tsv(PACKAGE_ROOT / "data/system-edge-contracts.tsv")
    checks.require(len(edge_rows) == 40, f"Expected 40 system-edge rows, found {len(edge_rows)}")
    checks.require(
        len({row["edge_id"] for row in edge_rows}) == 40,
        "system-edge-contracts.tsv edge_id values are not unique",
    )
    table_edges = [(row["from_id"], row["to_id"]) for row in edge_rows]
    for row in edge_rows:
        checks.require(row["from_id"] in systems, f"Unknown edge from_id: {row['from_id']}")
        checks.require(row["to_id"] in systems, f"Unknown edge to_id: {row['to_id']}")
    graph_counter = Counter(graph_edges)
    table_counter = Counter(table_edges)
    checks.require(
        graph_counter == table_counter,
        "Mermaid/system-edge mismatch: graph_only="
        f"{list((graph_counter - table_counter).elements())}, table_only={list((table_counter - graph_counter).elements())}",
    )
    checks.passed("First Mermaid system graph and 40 edge contracts agree in both directions")


def check_transitions_and_traces(checks: Checks) -> None:
    _, transitions = read_tsv(PACKAGE_ROOT / "data/mode-transition-contracts.tsv")
    transition_by_id = {row["transition_id"]: row for row in transitions}
    checks.require(len(transitions) == 37, f"Expected 37 transitions, found {len(transitions)}")
    checks.require(len(transition_by_id) == 37, "Transition IDs are not unique")

    transition_graph: defaultdict[str, set[str]] = defaultdict(set)
    reverse_graph: defaultdict[str, set[str]] = defaultdict(set)
    modes: set[str] = set()
    for row in transitions:
        source, target = row["from_mode"], row["to_mode"]
        modes.update((source, target))
        transition_graph[source].add(target)
        reverse_graph[target].add(source)
    checks.require(len(modes) == 12, f"Expected 12 transition modes, found {len(modes)}")
    for mode in modes:
        checks.require(bool(transition_graph[mode]), f"Transition mode has no exit: {mode}")
        checks.require(bool(reverse_graph[mode]), f"Transition mode has no entry: {mode}")
    reachable = {"story"}
    frontier = ["story"]
    while frontier:
        current = frontier.pop()
        for target in transition_graph[current]:
            if target not in reachable:
                reachable.add(target)
                frontier.append(target)
    checks.require(reachable == modes, f"Modes unreachable from story: {sorted(modes - reachable)}")

    _, traces = read_tsv(PACKAGE_ROOT / "data/core-loop-paper-walkthrough-traces.tsv")
    by_session: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in traces:
        by_session[row["session_id"]].append(row)
        transition = transition_by_id.get(row["transition_id"])
        checks.require(transition is not None, f"Unknown trace transition: {row['trace_step_id']} -> {row['transition_id']}")
        if transition:
            checks.require(
                row["from_mode"] == transition["from_mode"] and row["to_mode"] == transition["to_mode"],
                f"Trace endpoint mismatch at {row['trace_step_id']}: "
                f"trace {row['from_mode']}->{row['to_mode']}, contract "
                f"{transition['from_mode']}->{transition['to_mode']}",
            )
    checks.require(len(by_session) == 4, f"Expected 4 walkthrough sessions, found {len(by_session)}")
    for session_id, rows in by_session.items():
        try:
            ordered = sorted(rows, key=lambda row: int(row["step_order"]))
            orders = [int(row["step_order"]) for row in ordered]
        except ValueError:
            checks.require(False, f"Non-integer step_order in {session_id}")
            continue
        checks.require(
            orders == list(range(1, len(ordered) + 1)),
            f"Non-contiguous step_order in {session_id}: {orders}",
        )
        for previous, current in zip(ordered, ordered[1:]):
            checks.require(
                previous["to_mode"] == current["from_mode"],
                f"Trace discontinuity in {session_id}: {previous['trace_step_id']} ends "
                f"{previous['to_mode']}, {current['trace_step_id']} starts {current['from_mode']}",
            )
    checks.passed(
        f"Mode transitions/traces: 37 unique transitions across 12 live modes, "
        f"4 continuous sessions, {len(traces)} steps"
    )


def token_matches(rule: dict[str, str], token: str) -> bool:
    match_type = rule["match_type"]
    pattern = rule["token_pattern"]
    if match_type == "exact":
        return token == pattern
    if match_type == "exact_set":
        return token in pattern.split(";")
    if match_type == "glob":
        return fnmatch.fnmatchcase(token, pattern)
    return False


def check_episode_tokens(checks: Checks) -> None:
    _, rules = read_tsv(PACKAGE_ROOT / "data/episode-mode-token-contracts.tsv")
    checks.require(len(rules) == 16, f"Expected 16 token rules, found {len(rules)}")
    checks.require(len({row["rule_id"] for row in rules}) == len(rules), "Token rule IDs are not unique")
    for rule in rules:
        checks.require(rule["match_type"] in {"exact", "exact_set", "glob"}, f"Unknown match type: {rule['match_type']}")
        try:
            int(rule["priority"])
        except ValueError:
            checks.require(False, f"Non-integer token priority: {rule['rule_id']}={rule['priority']}")

    _, episodes = read_tsv(PACKAGE_ROOT / "chapters/c01-c03-episode-play-contracts.tsv")
    checks.require(len(episodes) == 13, f"Expected 13 Episode rows, found {len(episodes)}")
    checks.require(len({row["episode_id"] for row in episodes}) == 13, "Episode IDs are not unique")
    token_total = 0
    unique_tokens: set[str] = set()
    by_episode = {row["episode_id"]: row for row in episodes}
    for row in episodes:
        tokens = [token for token in row["mode_sequence"].split(">") if token]
        token_total += len(tokens)
        unique_tokens.update(tokens)
        for token in tokens:
            matching = [rule for rule in rules if token_matches(rule, token)]
            checks.require(bool(matching), f"No token rule matches {row['episode_id']}:{token}")
            if matching:
                highest_priority = min(int(rule["priority"]) for rule in matching)
                winners = [rule for rule in matching if int(rule["priority"]) == highest_priority]
                checks.require(
                    len(winners) == 1,
                    f"Token has {len(winners)} equal highest-priority matches: "
                    f"{row['episode_id']}:{token} -> {[rule['rule_id'] for rule in winners]}",
                )
        for index, token in enumerate(tokens):
            if token == "MISSION_CLEAR" or token.endswith("_MISSION_CLEAR"):
                following = tokens[index + 1] if index + 1 < len(tokens) else None
                checks.require(
                    following == "OPERATION_SETTLEMENT",
                    f"Mission Clear must be immediately followed by OPERATION_SETTLEMENT: "
                    f"{row['episode_id']}:{token} -> {following}",
                )
    checks.require(len(unique_tokens) == 91, f"Expected 91 unique Episode tokens, found {len(unique_tokens)}")

    for episode_id, expected in EXPECTED_OPERATION_SEQUENCES.items():
        actual = by_episode.get(episode_id, {}).get("operation_sequence")
        checks.require(actual == expected, f"{episode_id} operation_sequence={actual!r}, expected {expected!r}")
    for episode_id, (operation_count, chapter_count) in EXPECTED_EPISODE_SETTLEMENTS.items():
        row = by_episode.get(episode_id)
        checks.require(row is not None, f"Missing key Episode: {episode_id}")
        if not row:
            continue
        tokens = row["mode_sequence"].split(">")
        checks.require(
            tokens.count("OPERATION_SETTLEMENT") == operation_count,
            f"{episode_id} has {tokens.count('OPERATION_SETTLEMENT')} Operation settlements, expected {operation_count}",
        )
        checks.require(
            tokens.count("CHAPTER_SETTLEMENT") == chapter_count,
            f"{episode_id} has {tokens.count('CHAPTER_SETTLEMENT')} Chapter settlements, expected {chapter_count}",
        )
    checks.passed(
        f"Episode contracts: 13 Episodes, {len(unique_tokens)} unique tokens "
        f"({token_total} occurrences), clear/settlement boundaries valid"
    )


def resolve_repo_path(repo_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else repo_root / path


def check_opening_gd2_dependency_closure(checks: Checks) -> None:
    """Keep opening setting closure honest: complete debt coverage, zero sealed objects."""

    _, backfill_rows = read_tsv(PACKAGE_ROOT / "data/setting-backfill-register.tsv")
    _, binding_rows = read_tsv(PACKAGE_ROOT / "data/opening-accepted-story-bindings.tsv")
    closure_header, closure_rows = read_tsv(PACKAGE_ROOT / "data/opening-gd2-dependency-closure.tsv")
    _, canon_entity_rows = read_tsv(PACKAGE_ROOT.parents[1] / "data/canon/entities.tsv")
    backfill_by_id = {row["backfill_id"]: row for row in backfill_rows}
    binding_ids = {row["binding_id"] for row in binding_rows}
    canon_entity_ids = {row["entity_id"] for row in canon_entity_rows}
    expected_opening_gd2 = {f"BF{number:04d}" for number in range(20, 38)}

    checks.require(
        "current_canon_anchor_or_none" in closure_header and "canonical_subject_id" not in closure_header,
        "Opening GD2 closure must use current_canon_anchor_or_none, not canonical_subject_id",
    )
    checks.require(len(closure_rows) == 28, f"Expected 28 opening GD2/GD1 closure rows, found {len(closure_rows)}")
    checks.require(
        len({row["closure_id"] for row in closure_rows}) == len(closure_rows),
        "Opening GD2 closure IDs are not unique",
    )
    checks.require(
        len({row["backfill_id"] for row in closure_rows}) == len(closure_rows),
        "Opening GD2 closure backfill IDs must be one-row-per-debt",
    )
    observed_opening_gd2 = {
        row["backfill_id"] for row in closure_rows if row["backfill_id"] in expected_opening_gd2
    }
    checks.require(
        observed_opening_gd2 == expected_opening_gd2,
        f"Opening GD2 debt coverage differs: {sorted(observed_opening_gd2 ^ expected_opening_gd2)}",
    )

    for row in closure_rows:
        closure_id = row["closure_id"]
        checks.require(all(row.values()), f"Opening GD2 closure row has an empty field: {closure_id}")
        checks.require(row["backfill_id"] in backfill_by_id, f"Unknown opening closure debt: {closure_id}:{row['backfill_id']}")
        if row["backfill_id"] in backfill_by_id:
            checks.require(
                row["backfill_object_id"] == backfill_by_id[row["backfill_id"]]["object_id"],
                f"Opening closure debt object differs from backfill register: {closure_id}",
            )
        checks.require(bool(row["design_subject_id"]), f"Opening closure lacks design subject: {closure_id}")
        current_canon_anchor = row["current_canon_anchor_or_none"]
        checks.require(bool(current_canon_anchor), f"Opening closure lacks Current Canon anchor/none: {closure_id}")
        if current_canon_anchor != NO_SINGLE_CURRENT_CANON_ENTITY:
            checks.require(
                current_canon_anchor in canon_entity_ids,
                f"Opening closure Current Canon anchor does not resolve: {closure_id}:{current_canon_anchor}",
            )
        for support_ref in re.findall(r"BF\d{4}", row["supporting_backfill_refs"]):
            checks.require(support_ref in backfill_by_id, f"Unknown supporting backfill ref: {closure_id}:{support_ref}")
        row_binding_ids = set(filter(None, row["accepted_story_binding"].split(";")))
        checks.require(bool(row_binding_ids), f"Opening closure lacks an Accepted Story binding: {closure_id}")
        checks.require(
            row_binding_ids <= binding_ids,
            f"Unknown Accepted Story binding in opening closure: {closure_id}:{sorted(row_binding_ids - binding_ids)}",
        )
        checks.require(
            row["closure_status"].startswith("BLOCKED_"),
            f"Opening closure must remain blocked until real evidence exists: {closure_id}:{row['closure_status']}",
        )
        checks.require("REQUIRED:" in row["logic_diagram_requirement"], f"Missing logic requirement: {closure_id}")
        checks.require("REQUIRED:" in row["visual_direction_requirement"], f"Missing visual requirement: {closure_id}")
        checks.require(
            row["engineering_or_gameplay_graybox"].endswith(";not_run"),
            f"Opening closure graybox must remain not_run: {closure_id}",
        )
        checks.require(
            row["bom_requirement"].endswith(";not_created"),
            f"Opening closure BOM must remain not_created: {closure_id}",
        )

    design_subject_remaps = [
        row for row in closure_rows if row["design_subject_id"] != row["backfill_object_id"]
    ]
    resolved_current_canon_anchors = [
        row
        for row in closure_rows
        if row["current_canon_anchor_or_none"] != NO_SINGLE_CURRENT_CANON_ENTITY
    ]
    no_single_current_canon_entity = [
        row
        for row in closure_rows
        if row["current_canon_anchor_or_none"] == NO_SINGLE_CURRENT_CANON_ENTITY
    ]
    checks.require(
        len(design_subject_remaps) == 9,
        f"Expected nine explicit debt-to-design subject mappings, found {len(design_subject_remaps)}",
    )
    checks.require(
        len(resolved_current_canon_anchors) == 15,
        f"Expected fifteen resolved Current Canon anchors, found {len(resolved_current_canon_anchors)}",
    )
    checks.require(
        len(no_single_current_canon_entity) == 13,
        f"Expected thirteen explicit no-single-Current-Canon rows, found {len(no_single_current_canon_entity)}",
    )

    partial_logic = [
        (row["closure_id"], item.removeprefix("PARTIAL:"))
        for row in closure_rows
        for item in row["logic_diagram_requirement"].split(";")
        if item.startswith("PARTIAL:")
    ]
    checks.require(len(partial_logic) == 2, f"Expected two partial Wanji logic files, found {len(partial_logic)}")
    for closure_id, path_and_hash in partial_logic:
        raw_path, separator, expected_hash = path_and_hash.rpartition("@")
        checks.require(bool(separator), f"Malformed partial logic evidence: {closure_id}:{path_and_hash}")
        evidence_path = PACKAGE_ROOT / "setting/visuals" / raw_path
        checks.require(evidence_path.is_file(), f"Missing partial logic file: {closure_id}:{raw_path}")
        checks.require(
            bool(re.fullmatch(r"[0-9a-f]{64}", expected_hash)),
            f"Malformed partial logic hash: {closure_id}:{expected_hash}",
        )
        if evidence_path.is_file() and re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            checks.require(
                sha256_file(evidence_path) == expected_hash,
                f"Partial opening logic hash drift: {closure_id}:{raw_path}",
            )

    checks.passed(
        "Opening GD2 dependency closure: 28 one-debt rows; BF0020-BF0037 covered exactly; "
        "9 debt-to-design remaps; 15 Current Canon anchors resolve and 13 rows explicitly have no "
        "single Current Canon entity; all remain BLOCKED with "
        "grayboxes not_run and BOMs not_created"
    )


def check_opening_previs_graybox_bom(checks: Checks) -> None:
    """Require six non-circular D06 stages and fail closed on gate instances."""

    expected_classes = {
        "logic_diagram",
        "visual_direction",
        "playable_graybox",
        "continuous_previs",
        "asset_previs_candidate_bom",
        "formal_asset",
    }
    expected_stage_order = {
        "logic_diagram": "W1_DEPENDENCY_CLOSURE",
        "visual_direction": "W2_GD2_DIRECTION",
        "continuous_previs": "W3_POST_GAMEFLOW_PREVIS",
        "playable_graybox": "W4_CHAPTER_ADAPTER_TEST",
        "asset_previs_candidate_bom": "W5_ASSET_PREVIS_CANDIDATE_BOM",
        "formal_asset": "W6_POST_ASSET_AUTH_HANDOFF",
    }
    expected_required_gate = {
        "logic_diagram": "GATE-GD2;GATE-GD3",
        "visual_direction": "GATE-GD2",
        "continuous_previs": "GATE-PREVIS",
        "playable_graybox": "GATE-PROTOTYPE",
        "asset_previs_candidate_bom": "GATE-ASSET-AUTH",
        "formal_asset": "GATE-ASSET-HANDOFF",
    }
    expected_blocker_matrix = {
        "logic_diagram": ("yes", "yes", "yes", "yes"),
        "visual_direction": ("no", "yes", "yes", "yes"),
        "continuous_previs": ("no", "yes", "yes", "yes"),
        "playable_graybox": ("no", "yes", "yes", "yes"),
        "asset_previs_candidate_bom": ("no", "no", "yes", "yes"),
        "formal_asset": ("no", "no", "no", "yes"),
    }
    expected_scope_rules = {
        "logic_diagram": (
            "GATE-GD2=asset_pack:OPEN_exact_direction_pack_id_required+"
            "bind({bom_item_id},{source_previs_id});"
            "GATE-GD3=chapter:{chapter}+bind({bom_item_id},{source_previs_id})"
        ),
        "visual_direction": (
            "GATE-GD2=asset_pack:OPEN_exact_direction_pack_id_required+"
            "bind({bom_item_id},{source_previs_id})"
        ),
        "continuous_previs": (
            "GATE-PREVIS=episode:{chapter}/{episode}/{source_previs_id}_when_single_episode_"
            "else_operation:{chapter}/{episode}/{source_previs_id};exact_previs_pack_version_required"
        ),
        "playable_graybox": (
            "GATE-PROTOTYPE=build:OPEN_exact_build_id_required+"
            "bind({bom_item_id},{source_previs_id},ruleset,map)"
        ),
        "asset_previs_candidate_bom": (
            "GATE-ASSET-AUTH=asset_pack:OPEN_exact_candidate_asset_manifest_id_required+"
            "bind({bom_item_id},{source_previs_id})"
        ),
        "formal_asset": (
            "GATE-ASSET-HANDOFF=asset_pack:OPEN_exact_final_asset_manifest_id_required+"
            "bind({bom_item_id},{source_previs_id})"
        ),
    }
    expected_receipt_set_requirements = {
        "logic_diagram": (
            "GATE-GD2=GRT-GD2-DIRECTION;"
            "GATE-GD3=OPEN_compatible_scope_receipt_template_required"
        ),
        "visual_direction": "GATE-GD2=GRT-GD2-DIRECTION",
        "continuous_previs": (
            "GATE-PREVIS=GRT-PREVIS-DIRECTION_when_single_episode;"
            "OPEN_operation_scoped_template_required_when_episode_range"
        ),
        "playable_graybox": "GATE-PROTOTYPE=GRT-PROTOTYPE-GAMEPLAY",
        "asset_previs_candidate_bom": "GATE-ASSET-AUTH=GRT-ASSET-AUTH",
        "formal_asset": "GATE-ASSET-HANDOFF=GRT-ASSET-HANDOFF",
    }
    required_instance_bindings = (
        "gate_instance_id;gate_definition_id;scope_type;scope_instance;source_versions;"
        "checker_versions;actual_input_sha256;gate_receipt_set_template_id;"
        "receipt_set_instance_id;receipt_paths;receipt_sha256s;status=passed"
    )
    _, source_rows = read_tsv(PACKAGE_ROOT / "chapters/c01-c03-previs-needs.tsv")
    bom_header, bom_rows = read_tsv(PACKAGE_ROOT / "data/opening-previs-graybox-bom.tsv")
    contract_header, contract_rows = read_tsv(
        PACKAGE_ROOT / "data/opening-previs-artifact-class-contract.tsv"
    )
    _, gate_definition_rows = read_tsv(PACKAGE_ROOT / "data/game-design-gate-registry.tsv")
    _, gate_instance_schema_rows = read_tsv(
        PACKAGE_ROOT / "data/game-design-gate-instance-schema.tsv"
    )
    _, gate_receipt_template_rows = read_tsv(
        PACKAGE_ROOT / "data/gate-receipt-set-templates.tsv"
    )
    source_by_id = {row["previs_id"]: row for row in source_rows}
    contract_by_class = {row["artifact_class"]: row for row in contract_rows}
    gate_definition_ids = {row["gate_id"] for row in gate_definition_rows}
    gate_instance_schema_fields = {row["field_name"] for row in gate_instance_schema_rows}
    gate_receipt_template_ids = {
        row["receipt_set_template_id"] for row in gate_receipt_template_rows
    }

    expected_contract_header = {
        "artifact_class",
        "stage_order",
        "blocks_chapter_paper",
        "blocks_playable_build",
        "blocks_asset_authorization",
        "blocks_asset_handoff_runtime",
        "gate_definition_ids",
        "gate_instance_requirement",
        "gate_instance_scope_rule",
        "receipt_set_requirement",
        "required_instance_bindings",
        "current_instance_registry",
        "current_instance_status",
        "lifecycle",
        "notes",
    }
    checks.require(
        set(contract_header) == expected_contract_header,
        "Opening artifact-class contract schema drift: "
        f"{sorted(set(contract_header) ^ expected_contract_header)}",
    )
    checks.require(
        set(contract_by_class) == expected_classes and len(contract_rows) == len(expected_classes),
        "Opening artifact-class contract must contain exactly one row for each of six classes",
    )
    checks.require(
        "required_gate" in bom_header,
        "Opening BOM must keep required_gate as a definition-only field",
    )

    for artifact_class in sorted(expected_classes):
        contract = contract_by_class.get(artifact_class)
        if contract is None:
            continue
        blocker_tuple = (
            contract["blocks_chapter_paper"],
            contract["blocks_playable_build"],
            contract["blocks_asset_authorization"],
            contract["blocks_asset_handoff_runtime"],
        )
        checks.require(
            blocker_tuple == expected_blocker_matrix[artifact_class],
            f"Opening artifact-class blocker matrix drift: {artifact_class}:{blocker_tuple}",
        )
        checks.require(
            contract["stage_order"] == expected_stage_order[artifact_class],
            f"Opening artifact-class stage drift: {artifact_class}:{contract['stage_order']}",
        )
        checks.require(
            contract["gate_definition_ids"] == expected_required_gate[artifact_class],
            f"Opening artifact-class gate-definition drift: "
            f"{artifact_class}:{contract['gate_definition_ids']}",
        )
        checks.require(
            contract["gate_instance_requirement"]
            == "one_scoped_instance_per_gate_definition_per_bom_item",
            f"Opening gate-instance requirement drift: {artifact_class}",
        )
        checks.require(
            contract["gate_instance_scope_rule"] == expected_scope_rules[artifact_class],
            f"Opening gate-instance scope rule drift: {artifact_class}",
        )
        checks.require(
            contract["receipt_set_requirement"]
            == expected_receipt_set_requirements[artifact_class],
            f"Opening gate receipt-set requirement drift: {artifact_class}",
        )
        checks.require(
            contract["required_instance_bindings"] == required_instance_bindings,
            f"Opening gate-instance binding fields drift: {artifact_class}",
        )
        schema_names = {
            field.removesuffix("=passed")
            for field in contract["required_instance_bindings"].split(";")
        }
        checks.require(
            schema_names <= gate_instance_schema_fields,
            f"Opening gate-instance requirement names unknown schema fields: "
            f"{artifact_class}:{sorted(schema_names - gate_instance_schema_fields)}",
        )
        referenced_templates = set(
            re.findall(r"GRT-[A-Z0-9-]+", contract["receipt_set_requirement"])
        )
        checks.require(
            referenced_templates <= gate_receipt_template_ids,
            f"Opening gate receipt-set template is undefined: "
            f"{artifact_class}:{sorted(referenced_templates - gate_receipt_template_ids)}",
        )
        checks.require(
            contract["current_instance_registry"] == "OPEN:no_opening_gate_instance_registry",
            f"Opening gate-instance registry must remain explicitly OPEN: {artifact_class}",
        )
        checks.require(
            contract["current_instance_status"] == "OPEN:no_scoped_instance_bound",
            f"Opening gate-instance status cannot claim passed without a resolved instance: "
            f"{artifact_class}:{contract['current_instance_status']}",
        )
        checks.require(
            "passed" not in contract["current_instance_status"].lower(),
            f"Generic gate definition cannot directly claim a passed instance: {artifact_class}",
        )
        checks.require(
            contract["lifecycle"] == "candidate_unapproved",
            f"Opening artifact-class contract cannot promote authority: {artifact_class}",
        )
    checks.require(len(source_rows) == 20, f"Expected 20 opening Previs needs, found {len(source_rows)}")
    checks.require(
        len(source_by_id) == len(source_rows),
        "Opening Previs need IDs are not unique",
    )
    checks.require(len(bom_rows) == len(source_rows) * 6, f"Expected 120 opening BOM rows, found {len(bom_rows)}")
    checks.require(
        len({row["bom_item_id"] for row in bom_rows}) == len(bom_rows),
        "Opening BOM item IDs are not unique",
    )

    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    derived_instance_requirement_ids: set[str] = set()
    derived_instance_requirements_by_class: Counter[str] = Counter()
    for row in bom_rows:
        source_id = row["source_previs_id"]
        by_source[source_id].append(row)
        checks.require(source_id in source_by_id, f"Unknown opening BOM source_previs_id: {row['bom_item_id']}:{source_id}")
        checks.require(
            row["artifact_class"] in expected_classes,
            f"Unknown opening BOM artifact_class: {row['bom_item_id']}:{row['artifact_class']}",
        )
        if source_id in source_by_id:
            source = source_by_id[source_id]
            checks.require(row["chapter"] == source["chapter"], f"Opening BOM chapter drift: {row['bom_item_id']}")
            checks.require(row["episode"] == source["episode"], f"Opening BOM Episode drift: {row['bom_item_id']}")
            checks.require(
                row["object_or_location"] == source["location_or_object"],
                f"Opening BOM object drift: {row['bom_item_id']}",
            )
            checks.require(
                row["complexity_bucket"] == source["asset_tier"],
                f"Opening BOM complexity drift: {row['bom_item_id']}",
            )
        checks.require(
            row["stage_order"] == expected_stage_order.get(row["artifact_class"]),
            f"Opening BOM stage order drift: {row['bom_item_id']}:{row['stage_order']}",
        )
        checks.require(
            row["required_gate"] == expected_required_gate.get(row["artifact_class"]),
            f"Opening BOM target gate drift: {row['bom_item_id']}:{row['required_gate']}",
        )
        contract = contract_by_class.get(row["artifact_class"])
        if contract is not None:
            for field in (
                "stage_order",
                "blocks_chapter_paper",
                "blocks_playable_build",
                "blocks_asset_authorization",
                "blocks_asset_handoff_runtime",
            ):
                checks.require(
                    row[field] == contract[field],
                    f"Opening BOM differs from artifact-class contract: "
                    f"{row['bom_item_id']}:{field}:{row[field]}!={contract[field]}",
                )
            checks.require(
                row["required_gate"] == contract["gate_definition_ids"],
                f"Opening BOM gate definitions differ from artifact-class contract: "
                f"{row['bom_item_id']}",
            )
        blocker_tuple = (
            row["blocks_chapter_paper"],
            row["blocks_playable_build"],
            row["blocks_asset_authorization"],
            row["blocks_asset_handoff_runtime"],
        )
        checks.require(
            blocker_tuple == expected_blocker_matrix.get(row["artifact_class"]),
            f"Opening BOM blocker matrix drift: {row['bom_item_id']}:{blocker_tuple}",
        )
        checks.require(bool(row["priority_wave"]), f"Missing opening BOM priority: {row['bom_item_id']}")
        checks.require(
            row["budget_confidence"] == "provisional_uncalibrated",
            f"Opening BOM budget must remain provisional: {row['bom_item_id']}",
        )
        checks.require(
            row["lifecycle"] == "candidate_unapproved",
            f"Opening BOM cannot promote authority: {row['bom_item_id']}:{row['lifecycle']}",
        )
        dependency_ids = set(filter(None, row["dependency_ids"].split(";")))
        required_gate_list = list(filter(None, row["required_gate"].split(";")))
        required_gates = set(required_gate_list)
        checks.require(
            len(required_gate_list) == len(required_gates),
            f"Opening BOM repeats a gate definition: {row['bom_item_id']}:{required_gate_list}",
        )
        checks.require(
            required_gates <= gate_definition_ids,
            f"Opening BOM uses undefined gate definitions: "
            f"{row['bom_item_id']}:{sorted(required_gates - gate_definition_ids)}",
        )
        checks.require(
            "passed" not in row["required_gate"].lower()
            and "instance" not in row["required_gate"].lower(),
            f"required_gate may name definition types only, never a passed instance claim: "
            f"{row['bom_item_id']}:{row['required_gate']}",
        )
        checks.require(
            "passed" not in row["current_evidence_status"].lower(),
            f"Artifact evidence status cannot substitute a gate-instance PASS: "
            f"{row['bom_item_id']}:{row['current_evidence_status']}",
        )
        for gate_definition_id in required_gate_list:
            requirement_id = f"{row['bom_item_id']}@{gate_definition_id}"
            checks.require(
                requirement_id not in derived_instance_requirement_ids,
                f"Duplicate derived opening gate-instance requirement: {requirement_id}",
            )
            derived_instance_requirement_ids.add(requirement_id)
            derived_instance_requirements_by_class[row["artifact_class"]] += 1
        checks.require(
            not dependency_ids.intersection(required_gates),
            f"Opening BOM row cannot depend on its own target gate: "
            f"{row['bom_item_id']}:{sorted(dependency_ids.intersection(required_gates))}",
        )
        checks.require(
            {
                row["blocks_chapter_paper"],
                row["blocks_playable_build"],
                row["blocks_asset_authorization"],
                row["blocks_asset_handoff_runtime"],
            }
            <= {"yes", "no"},
            f"Opening BOM blocker fields must be yes/no: {row['bom_item_id']}",
        )
        checks.require(
            row["blocks_playable_build"]
            == ("yes" if row["artifact_class"] in {
                "logic_diagram",
                "visual_direction",
                "continuous_previs",
                "playable_graybox",
            } else "no"),
            f"Opening playable-build blocker semantics drift: "
            f"{row['bom_item_id']}:{row['blocks_playable_build']}",
        )
        if row["artifact_class"] == "logic_diagram":
            checks.require(row["blocks_chapter_paper"] == "yes", f"Logic gap must block chapter-paper closure: {row['bom_item_id']}")
        else:
            checks.require(row["blocks_chapter_paper"] == "no", f"Only logic rows block chapter-paper closure: {row['bom_item_id']}")
        checks.require(
            row["blocks_asset_handoff_runtime"] == "yes",
            f"Every unfinished artifact class must block asset handoff/runtime: {row['bom_item_id']}",
        )
        if row["artifact_class"] == "formal_asset":
            checks.require(
                row["blocks_asset_authorization"] == "no",
                f"Post-auth formal asset cannot block its own authorization: {row['bom_item_id']}",
            )
            checks.require(
                row["current_evidence_status"] == "OPEN",
                f"Candidate/Demo evidence cannot count as formal-asset evidence: {row['bom_item_id']}",
            )
        else:
            checks.require(
                row["blocks_asset_authorization"] == "yes",
                f"Pre-auth stage must block asset authorization while unfinished: {row['bom_item_id']}",
            )
        if row["artifact_class"] == "asset_previs_candidate_bom":
            checks.require(
                row["quantity_bucket"] == "Q1_CANDIDATE_BOM_PACKAGE",
                f"Asset-Previs stage must be one Candidate BOM package: {row['bom_item_id']}",
            )
            checks.require(
                row["required_receipt_types"] == "visual:direction;production:authorization",
                f"Asset authorization receipts must stay visual+production authorization: {row['bom_item_id']}",
            )
            checks.require(
                row["required_gate"] == "GATE-ASSET-AUTH",
                f"Asset-Previs/Candidate-BOM stage must target GATE-ASSET-AUTH: {row['bom_item_id']}",
            )
            checks.require(
                "GATE-ASSET-AUTH" not in row["dependency_ids"],
                f"GATE-ASSET-AUTH cannot be its own W5 input: {row['bom_item_id']}",
            )
        if row["artifact_class"] == "formal_asset":
            checks.require(
                row["quantity_bucket"] in {"QFROM_AUTHORIZED_MANIFEST", "QSHARED_REUSE_ONLY"},
                f"Formal asset count must come from the authorized manifest or shared reuse: {row['bom_item_id']}",
            )
            checks.require(
                row["required_receipt_types"] == "production:handoff",
                f"Formal handoff must use a distinct production handoff receipt: {row['bom_item_id']}",
            )
            checks.require(
                row["required_gate"] == "GATE-ASSET-HANDOFF",
                f"Post-auth formal asset must target GATE-ASSET-HANDOFF: {row['bom_item_id']}",
            )
            checks.require(
                "GATE-ASSET-AUTH" in row["dependency_ids"],
                f"Formal asset production must depend on passed GATE-ASSET-AUTH: {row['bom_item_id']}",
            )

    expected_instance_requirement_counts = Counter(
        {
            "logic_diagram": 40,
            "visual_direction": 20,
            "continuous_previs": 20,
            "playable_graybox": 20,
            "asset_previs_candidate_bom": 20,
            "formal_asset": 20,
        }
    )
    checks.require(
        derived_instance_requirements_by_class == expected_instance_requirement_counts,
        "Opening scoped gate-instance requirement counts drift: "
        f"{dict(derived_instance_requirements_by_class)}",
    )
    checks.require(
        len(derived_instance_requirement_ids) == 140,
        f"Expected 140 scoped gate-instance requirements, found "
        f"{len(derived_instance_requirement_ids)}",
    )

    for source_id, source in source_by_id.items():
        rows = by_source.get(source_id, [])
        classes = {row["artifact_class"] for row in rows}
        checks.require(len(rows) == 6, f"Opening BOM source must have six rows: {source_id}:{len(rows)}")
        checks.require(
            classes == expected_classes,
            f"Opening BOM class coverage differs: {source_id}:{sorted(classes ^ expected_classes)}",
        )
        if classes != expected_classes:
            continue
        row_by_class = {row["artifact_class"]: row for row in rows}
        logic_id = row_by_class["logic_diagram"]["bom_item_id"]
        visual_id = row_by_class["visual_direction"]["bom_item_id"]
        continuous_id = row_by_class["continuous_previs"]["bom_item_id"]
        graybox_id = row_by_class["playable_graybox"]["bom_item_id"]
        asset_previs_id = row_by_class["asset_previs_candidate_bom"]["bom_item_id"]

        visual_dependencies = set(filter(None, row_by_class["visual_direction"]["dependency_ids"].split(";")))
        continuous_dependencies = set(
            filter(None, row_by_class["continuous_previs"]["dependency_ids"].split(";"))
        )
        graybox_dependencies = set(filter(None, row_by_class["playable_graybox"]["dependency_ids"].split(";")))
        asset_previs_dependencies = set(
            filter(None, row_by_class["asset_previs_candidate_bom"]["dependency_ids"].split(";"))
        )
        formal_dependencies = set(filter(None, row_by_class["formal_asset"]["dependency_ids"].split(";")))

        checks.require(
            visual_dependencies == {logic_id},
            f"Opening W2 must depend exactly on same-source W1: {source_id}:{sorted(visual_dependencies)}",
        )
        checks.require(
            continuous_dependencies == {logic_id, visual_id, "GATE-GAMEFLOW"},
            f"Opening W3 must depend on same-source W1/W2 plus passed GATE-GAMEFLOW: "
            f"{source_id}:{sorted(continuous_dependencies)}",
        )
        checks.require(
            graybox_dependencies == {continuous_id, "GATE-PREVIS"},
            f"Opening W4 chapter adapter must wait for same-source W3 and passed scoped GATE-PREVIS; "
            f"neutral prototypes do not count as W4 closure: {source_id}:{sorted(graybox_dependencies)}",
        )
        checks.require(
            asset_previs_dependencies == {
                visual_id,
                continuous_id,
                graybox_id,
                "GATE-PROTOTYPE",
            },
            f"Opening W5 must depend on same-source W2/W3/W4 plus passed GATE-PROTOTYPE: "
            f"{source_id}:{sorted(asset_previs_dependencies)}",
        )
        checks.require(
            formal_dependencies == {asset_previs_id, "GATE-ASSET-AUTH"},
            f"Opening W6 must depend on same-source W5 plus passed GATE-ASSET-AUTH: "
            f"{source_id}:{sorted(formal_dependencies)}",
        )

    repo_result = git(PACKAGE_ROOT, "rev-parse", "--show-toplevel")
    checks.require(repo_result.returncode == 0, "Opening BOM evidence is not inside a Git repository")
    if repo_result.returncode == 0:
        repo_root = Path(repo_result.stdout.decode("utf-8").strip())
        for row in bom_rows:
            paths = row["current_evidence_paths"].split(";")
            hashes = row["current_evidence_sha256s"].split(";")
            if paths == ["OPEN"]:
                checks.require(hashes == ["OPEN"], f"OPEN evidence hash mismatch: {row['bom_item_id']}")
                checks.require(row["current_evidence_status"] == "OPEN", f"OPEN evidence status mismatch: {row['bom_item_id']}")
                continue
            checks.require(
                len(paths) == len(hashes),
                f"Opening BOM evidence path/hash arity mismatch: {row['bom_item_id']}",
            )
            for raw_path, expected_hash in zip(paths, hashes):
                evidence_path = (
                    resolve_repo_path(repo_root, raw_path)
                    if raw_path.startswith("docs/") or Path(raw_path).is_absolute()
                    else PACKAGE_ROOT / raw_path
                )
                checks.require(evidence_path.is_file(), f"Missing opening BOM evidence: {row['bom_item_id']}:{raw_path}")
                checks.require(
                    bool(re.fullmatch(r"[0-9a-f]{64}", expected_hash)),
                    f"Malformed opening BOM evidence hash: {row['bom_item_id']}:{expected_hash}",
                )
                if evidence_path.is_file() and re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                    checks.require(
                        sha256_file(evidence_path) == expected_hash,
                        f"Opening BOM evidence hash drift: {row['bom_item_id']}:{raw_path}",
                    )

    open_count = sum(row["current_evidence_status"] == "OPEN" for row in bom_rows)
    partial_count = len(bom_rows) - open_count
    formal_open_count = sum(
        row["artifact_class"] == "formal_asset" and row["current_evidence_status"] == "OPEN"
        for row in bom_rows
    )
    checks.require(open_count == 111, f"Expected 111 OPEN opening BOM rows, found {open_count}")
    checks.require(partial_count == 9, f"Expected 9 partial Candidate evidence rows, found {partial_count}")
    checks.require(formal_open_count == 20, f"Expected all 20 formal-asset rows OPEN, found {formal_open_count}")
    checks.passed(
        f"Opening Previs/graybox BOM: {len(source_rows)} source_previs_id values x "
        f"{len(expected_classes)} artifact classes = {len(bom_rows)} rows; {open_count} OPEN + "
        f"{partial_count} partial Candidate evidence; formal assets {formal_open_count}/20 OPEN; "
        "playable-build blockers W1-W4=yes and W5-W6=no; "
        f"{len(derived_instance_requirement_ids)} item/gate scoped-instance requirements, "
        "0 instance registries and 0 passed instances; "
        "W2<-W1, W3<-W1/W2, W4<-W3/PREVIS, W5<-W2/W3/W4/PROTOTYPE, "
        "W6<-W5/ASSET-AUTH; all non-OPEN evidence paths and hashes resolve"
    )


def check_opening_design_subject_coverage(checks: Checks) -> None:
    """Bind every opening closure subject to the W1/W5/W6 production chain."""

    closure_header, closure_rows = read_tsv(PACKAGE_ROOT / "data/opening-gd2-dependency-closure.tsv")
    coverage_header, coverage_rows = read_tsv(PACKAGE_ROOT / "data/opening-design-subject-coverage.tsv")
    _, bom_rows = read_tsv(PACKAGE_ROOT / "data/opening-previs-graybox-bom.tsv")
    _, budget_rows = read_tsv(PACKAGE_ROOT / "data/asset-budget.tsv")

    closure_by_id = {row["closure_id"]: row for row in closure_rows}
    coverage_by_closure = {row["closure_id"]: row for row in coverage_rows}
    bom_by_id = {row["bom_item_id"]: row for row in bom_rows}
    budget_ids = {row["asset_id"] for row in budget_rows}
    expected_edge_kinds = {
        "existing_subject_new_design_pack",
        "existing_location_new_state_pack",
        "existing_subject_new_interface",
        "family_pack_reuses_member_subjects",
        "shared_system_reuses_existing_subject",
    }
    required_subject_debts = {
        "BF0011",
        "BF0012",
        "BF0013",
        "BF0028",
        "BF0017",
        "BF0018",
        "BF0019",
        "BF0033",
        "BF0034",
        "BF0035",
        "BF0036",
    }

    checks.require(
        "current_canon_anchor_or_none" in closure_header and "canonical_subject_id" not in closure_header,
        "Opening closure subject coverage input must use current_canon_anchor_or_none",
    )
    checks.require(
        "current_canon_anchor_or_none" in coverage_header and "canonical_subject_id" not in coverage_header,
        "Opening subject coverage must use current_canon_anchor_or_none, not canonical_subject_id",
    )
    checks.require(len(coverage_rows) == 28, f"Expected 28 opening subject-coverage rows, found {len(coverage_rows)}")
    checks.require(
        len({row["coverage_id"] for row in coverage_rows}) == len(coverage_rows),
        "Opening subject-coverage IDs are not unique",
    )
    checks.require(
        len(coverage_by_closure) == len(coverage_rows),
        "Opening subject coverage must have one row per closure_id",
    )
    checks.require(
        set(coverage_by_closure) == set(closure_by_id),
        "Opening subject coverage and dependency-closure sets differ: "
        f"{sorted(set(coverage_by_closure) ^ set(closure_by_id))}",
    )

    coverage_by_backfill: dict[str, dict[str, str]] = {}
    for row in coverage_rows:
        coverage_id = row["coverage_id"]
        closure_id = row["closure_id"]
        checks.require(all(row.values()), f"Opening subject-coverage row has an empty field: {coverage_id}")
        checks.require(closure_id in closure_by_id, f"Unknown subject-coverage closure: {coverage_id}:{closure_id}")
        closure = closure_by_id.get(closure_id)
        if closure:
            for field in ("backfill_id", "design_subject_id", "current_canon_anchor_or_none"):
                checks.require(
                    row[field] == closure[field],
                    f"Opening subject coverage {field} differs from closure: {coverage_id}",
                )
        checks.require(
            row["backfill_id"] not in coverage_by_backfill,
            f"Opening subject coverage repeats backfill debt: {coverage_id}:{row['backfill_id']}",
        )
        coverage_by_backfill[row["backfill_id"]] = row
        checks.require(
            row["edge_kind"] in expected_edge_kinds,
            f"Unknown opening subject edge kind: {coverage_id}:{row['edge_kind']}",
        )
        checks.require(bool(row["new_or_reuse_boundary"]), f"Missing new/reuse boundary: {coverage_id}")
        checks.require(
            row["coverage_status"] == "candidate_subject_edges_defined_evidence_open_or_partial",
            f"Opening subject coverage cannot imply delivery: {coverage_id}:{row['coverage_status']}",
        )

        source_ids = list(filter(None, row["source_previs_ids"].split(";")))
        logic_ids = list(filter(None, row["logic_bom_item_ids"].split(";")))
        asset_previs_ids = list(filter(None, row["asset_previs_bom_item_ids"].split(";")))
        formal_ids = list(filter(None, row["formal_asset_bom_item_ids"].split(";")))
        checks.require(bool(source_ids), f"Opening subject coverage lacks source Previs IDs: {coverage_id}")
        checks.require(
            len(source_ids) == len(logic_ids) == len(asset_previs_ids) == len(formal_ids),
            f"Opening subject coverage W1/W5/W6 edge arity differs: {coverage_id}",
        )
        for source_id, logic_id, asset_previs_id, formal_id in zip(
            source_ids, logic_ids, asset_previs_ids, formal_ids
        ):
            for bom_id, expected_class in (
                (logic_id, "logic_diagram"),
                (asset_previs_id, "asset_previs_candidate_bom"),
                (formal_id, "formal_asset"),
            ):
                checks.require(bom_id in bom_by_id, f"Unknown subject-coverage BOM item: {coverage_id}:{bom_id}")
                bom = bom_by_id.get(bom_id)
                if bom:
                    checks.require(
                        bom["artifact_class"] == expected_class,
                        f"Subject-coverage BOM class differs: {coverage_id}:{bom_id}:{bom['artifact_class']}",
                    )
                    checks.require(
                        bom["source_previs_id"] == source_id,
                        f"Subject-coverage source/BOM edge differs: {coverage_id}:{source_id}:{bom_id}",
                    )

        manifest_refs = set(filter(None, row["manifest_subject_refs"].split(";")))
        checks.require(
            row["design_subject_id"] in manifest_refs,
            f"Opening coverage manifest lacks its design subject: {coverage_id}",
        )
        current_canon_anchor = row["current_canon_anchor_or_none"]
        if current_canon_anchor != NO_SINGLE_CURRENT_CANON_ENTITY:
            checks.require(
                current_canon_anchor in manifest_refs,
                f"Opening coverage manifest lacks its resolved Current Canon anchor: "
                f"{coverage_id}:{current_canon_anchor}",
            )
        row_budget_ids = set(filter(None, row["asset_budget_ids"].split(";")))
        checks.require(bool(row_budget_ids), f"Opening subject coverage lacks asset-budget refs: {coverage_id}")
        checks.require(
            row_budget_ids <= budget_ids,
            f"Unknown opening subject asset-budget refs: {coverage_id}:{sorted(row_budget_ids - budget_ids)}",
        )
        mapped_w5_budgets: set[str] = set()
        for bom_id in asset_previs_ids:
            bom = bom_by_id.get(bom_id)
            if bom:
                mapped_w5_budgets.update(filter(None, bom["asset_budget_ids"].split(";")))
        checks.require(
            row_budget_ids <= mapped_w5_budgets,
            f"Subject asset budgets do not resolve through mapped W5 rows: "
            f"{coverage_id}:{sorted(row_budget_ids - mapped_w5_budgets)}",
        )

    checks.require(
        required_subject_debts <= set(coverage_by_backfill),
        f"Required C02/C03 subject debts lack coverage: {sorted(required_subject_debts - set(coverage_by_backfill))}",
    )
    for backfill_id in ("BF0011", "BF0012"):
        row = coverage_by_backfill.get(backfill_id)
        if row:
            subject_budgets = set(filter(None, row["asset_budget_ids"].split(";")))
            checks.require(
                {"ASSET_CORE_CHASSIS", "ASSET_ACTION_CLIP"} <= subject_budgets,
                f"{backfill_id} must bind core-chassis and action-clip budgets",
            )
            checks.require(
                bool(row["logic_bom_item_ids"] and row["asset_previs_bom_item_ids"] and row["formal_asset_bom_item_ids"]),
                f"{backfill_id} lacks a W1/W5/W6 subject edge",
            )

    c02_lineup = coverage_by_backfill.get("BF0028")
    if c02_lineup:
        lineup_refs = set(filter(None, c02_lineup["manifest_subject_refs"].split(";")))
        checks.require(
            c02_lineup["edge_kind"] == "family_pack_reuses_member_subjects",
            "BF0028 C02 lineup must be a family/reuse boundary, not a merged production subject",
        )
        checks.require(
            {
                "VP_C02_LINEUP",
                "V353U071",
                "V353U048",
                "MECHA_C02_COMPLETE_KING",
                "MECHA_C02_DOCK_JACK",
            }
            <= lineup_refs,
            "BF0028 manifest refs must preserve the explicit C02 lineup subjects",
        )
        checks.require(
            "稳定" in c02_lineup["unresolved_manifest_questions"]
            and "entity ID" in c02_lineup["unresolved_manifest_questions"],
            "BF0028 must keep local-flight-team stable entity IDs explicitly unresolved",
        )

    for backfill_id in {"BF0017", "BF0018", "BF0019", "BF0033", "BF0034", "BF0035", "BF0036"}:
        row = coverage_by_backfill.get(backfill_id)
        if row:
            checks.require(
                bool(row["new_or_reuse_boundary"]),
                f"C03 subject debt lacks an explicit new/reuse boundary: {backfill_id}",
            )
            checks.require(
                bool(row["logic_bom_item_ids"] and row["asset_previs_bom_item_ids"] and row["formal_asset_bom_item_ids"]),
                f"C03 subject debt lacks a W1/W5/W6 edge: {backfill_id}",
            )

    checks.passed(
        "Opening subject coverage: 28/28 closure rows bind design subjects to W1/W5/W6; "
        "15 resolved Current Canon anchors and 13 explicit none values match the closure; "
        "11 required C02/C03 subject debts are explicit; mapped W5 asset-budget refs resolve"
    )


def git_blob_sha256(repo_root: Path, commit: str, repo_path: str) -> str | None:
    result = git(repo_root, "show", f"{commit}:{repo_path}")
    if result.returncode != 0:
        return None
    return hashlib.sha256(result.stdout).hexdigest()


def check_accepted_story_bindings(checks: Checks) -> None:
    repo_result = git(PACKAGE_ROOT, "rev-parse", "--show-toplevel")
    checks.require(repo_result.returncode == 0, "Candidate package is not inside a Git repository")
    if repo_result.returncode != 0:
        return
    repo_root = Path(repo_result.stdout.decode("utf-8").strip())
    _, bindings = read_tsv(PACKAGE_ROOT / "data/opening-accepted-story-bindings.tsv")
    checks.require(len(bindings) == 3, f"Expected 3 ASB rows, found {len(bindings)}")
    checks.require(len({row["binding_id"] for row in bindings}) == 3, "ASB binding IDs are not unique")
    checks.require({row["chapter"] for row in bindings} == {"C01", "C02", "C03"}, "ASB chapters must be C01/C02/C03")

    component_total = 0
    story_paths: set[str] = set()
    receipt_paths: set[str] = set()
    resolved_durable = 0
    unresolved_durable = 0
    for row in bindings:
        story_path = resolve_repo_path(repo_root, row["accepted_story_path"])
        receipt_path = resolve_repo_path(repo_root, row["receipt_path"])
        story_paths.add(row["accepted_story_path"])
        receipt_paths.add(row["receipt_path"])
        checks.require(story_path.is_file(), f"Missing accepted Reader: {row['accepted_story_path']}")
        checks.require(receipt_path.is_file(), f"Missing acceptance receipt: {row['receipt_path']}")
        if story_path.is_file():
            current_story_hash = sha256_file(story_path)
            checks.require(current_story_hash == row["accepted_story_sha256"], f"Accepted Reader hash drift: {row['binding_id']}")
            checks.require(current_story_hash == row["current_story_sha256"], f"Current Reader hash field drift: {row['binding_id']}")
        if receipt_path.is_file():
            current_receipt_hash = sha256_file(receipt_path)
            checks.require(current_receipt_hash == row["receipt_sha256"], f"Acceptance receipt hash drift: {row['binding_id']}")
            checks.require(current_receipt_hash == row["current_receipt_sha256"], f"Current receipt hash field drift: {row['binding_id']}")

        components: list[tuple[str, str, str]] = []
        for component in filter(None, row["accepted_episode_components"].split(";")):
            parts = component.rsplit("@", 2)
            checks.require(len(parts) == 3, f"Malformed ASB component: {row['binding_id']}:{component}")
            if len(parts) == 3:
                components.append((parts[0], parts[1], parts[2]))
        component_total += len(components)
        expected_component_count = {"C01": 4, "C02": 5, "C03": 4}.get(row["chapter"])
        checks.require(
            len(components) == expected_component_count,
            f"{row['binding_id']} has {len(components)} components, expected {expected_component_count}",
        )
        checks.require(
            len({component_id for component_id, _, _ in components}) == len(components),
            f"Duplicate component IDs in {row['binding_id']}",
        )
        for component_id, component_path_raw, expected_hash in components:
            component_path = resolve_repo_path(repo_root, component_path_raw)
            checks.require(component_path.is_file(), f"Missing ASB component: {component_path_raw}")
            if component_path.is_file():
                checks.require(
                    sha256_file(component_path) == expected_hash,
                    f"ASB component hash drift: {row['binding_id']}:{component_id}",
                )

        durable_status = row["durable_snapshot_status"]
        durable_ref = row["durable_snapshot_ref"]
        if durable_status == "RESOLVED_REACHABLE_GIT_COMMIT":
            resolved_durable += 1
            checks.require(durable_ref.startswith("git:"), f"Resolved durable ref is not git:<commit>: {row['binding_id']}")
            if not durable_ref.startswith("git:"):
                continue
            commit = durable_ref.removeprefix("git:")
            commit_check = git(repo_root, "cat-file", "-e", f"{commit}^{{commit}}")
            checks.require(commit_check.returncode == 0, f"Durable commit object missing: {row['binding_id']}:{commit}")
            containing_refs = git(repo_root, "for-each-ref", "--contains", commit, "--format=%(refname)")
            refs = containing_refs.stdout.decode("utf-8").splitlines() if containing_refs.returncode == 0 else []
            checks.require(bool(refs), f"Durable commit is not reachable from a Git ref: {row['binding_id']}:{commit}")
            snapshot_items = [
                (row["accepted_story_path"], row["accepted_story_sha256"]),
                (row["receipt_path"], row["receipt_sha256"]),
                *((path, digest) for _, path, digest in components),
            ]
            for repo_path, expected_hash in snapshot_items:
                snapshot_hash = git_blob_sha256(repo_root, commit, repo_path)
                checks.require(snapshot_hash is not None, f"Durable snapshot missing path: {commit}:{repo_path}")
                if snapshot_hash is not None:
                    checks.require(
                        snapshot_hash == expected_hash,
                        f"Durable snapshot hash mismatch: {commit}:{repo_path}",
                    )
        elif durable_status == "UNRESOLVED_NO_REACHABLE_GIT_COMMIT_OR_ARCHIVE":
            unresolved_durable += 1
            checks.require(durable_ref == "unresolved", f"Unresolved ASB must use durable_snapshot_ref=unresolved: {row['binding_id']}")
            checks.warn(f"{row['binding_id']} current bytes match, but no reachable durable snapshot is registered")
        else:
            checks.require(False, f"Unknown durable snapshot status: {row['binding_id']}:{durable_status}")

    checks.require(component_total == 13, f"Expected 13 ASB Episode components, found {component_total}")
    checks.require(len(story_paths) == 3, f"Expected 3 unique accepted Readers, found {len(story_paths)}")
    checks.require(len(receipt_paths) == 3, f"Expected 3 unique acceptance receipts, found {len(receipt_paths)}")
    checks.require(resolved_durable == 1, f"Expected 1 resolved durable ASB, found {resolved_durable}")
    checks.require(unresolved_durable == 2, f"Expected 2 explicitly unresolved durable ASBs, found {unresolved_durable}")
    checks.passed(
        "Accepted story bindings: 3 ASBs, 13 Episode components, 3 Readers, 3 receipts; "
        "all current hashes match; registered Git durable ref is reachable"
    )


def main() -> int:
    checks = Checks()
    check_tsv_widths(checks)
    check_workstream_parking(checks)
    check_markdown_links(checks)
    check_research_evidence(checks)
    check_deliverable_coverage(checks)
    check_prototype_paper_fixtures(checks)
    systems, _states = check_systems_states_and_owners(checks)
    check_series_mechanic_lifecycle(checks, systems)
    check_system_graph(checks, systems)
    check_transitions_and_traces(checks)
    check_episode_tokens(checks)
    check_opening_gd2_dependency_closure(checks)
    check_opening_previs_graybox_bom(checks)
    check_opening_design_subject_coverage(checks)
    check_accepted_story_bindings(checks)

    print("Candidate contract static validation")
    for message in checks.passes:
        print(f"PASS  {message}")
    for message in checks.warnings:
        print(f"WARN  {message}")
    for message in checks.errors:
        print(f"FAIL  {message}")
    if checks.errors:
        print(f"RESULT FAIL ({len(checks.errors)} error(s), {len(checks.warnings)} warning(s))")
        return 1
    print(f"RESULT PASS ({len(checks.passes)} checks, {len(checks.warnings)} known warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
