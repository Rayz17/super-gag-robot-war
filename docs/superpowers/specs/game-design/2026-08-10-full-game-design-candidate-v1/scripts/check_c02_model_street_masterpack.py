#!/usr/bin/env python3
"""Validate the C02 Model Street/Cargo Ring Candidate location master pack.

This checker proves only that the paper dossier, state chain, reveal projection,
accepted-story binding, and real low-fi SVG remain mutually consistent.  It
does not prove geometry, physics, fun, visual direction, GD2 sealing, a Build,
human evidence, production authorization, or Runtime readiness.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import sys
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
WORKSPACE = PACKAGE.parents[4]
DATA = PACKAGE / "data"
DOSSIER_PATH = DATA / "c02-model-street-location-dossier.tsv"
STATE_PATH = DATA / "c02-cargo-ring-state-variants.tsv"
REVEAL_PATH = DATA / "c02-model-street-reveal-projection.tsv"
BINDING_PATH = DATA / "opening-accepted-story-bindings.tsv"
MASTER_PATH = PACKAGE / "setting/model-street-master-pack-v0.1.md"
SVG_PATH = PACKAGE / "setting/visuals/model-street-topology-v0.1.svg"

STORY_REL = "docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C02-章节连续阅读稿.md"
RECEIPT_REL = "docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C02/C02-用户创作验收回执.md"
STORY_SHA = "56827053dcf5e17922b143acbcb99457b284080dcef041d1d6be58880f6e03a1"
RECEIPT_SHA = "dc5e2e50a7c07d7aec36ad84cc40146a90aab30d43787a2c5364effd57738392"
BINDING_ID = "ASB-C02-20260806-56827053"

EXPECTED_ZONES = {f"MS-Z{index:02d}" for index in range(1, 9)}
EXPECTED_STATES = {f"CR-S{index:02d}" for index in range(0, 9)}
EXPECTED_REVEALS = {f"MS-R{index:02d}" for index in range(1, 13)}
ZONE_REQUIRED_FIELDS = {
    "location_id",
    "display_name",
    "daily_function",
    "primary_users_and_responsibility",
    "scale_and_capacity",
    "adjacent_zone_ids",
    "human_flow",
    "machine_flow",
    "cargo_service_flow",
    "access_and_emergency_control",
    "visual_sound_anchor",
    "chapter_consumers",
    "locked_accepted_story_fields",
    "open_candidate_fields",
    "status",
}
STATE_REQUIRED_FIELDS = {
    "chapter_window",
    "state_label",
    "operation_boundary",
    "ring_mobility",
    "support_state",
    "central_rotor_state",
    "outer_arena_state",
    "people_state",
    "mecha_state",
    "cargo_and_service_state",
    "control_chain",
    "hazard_state",
    "allowed_player_verbs",
    "state_inputs",
    "state_outputs",
    "checkpoint_or_receipt",
    "locked_accepted_story_fields",
    "open_candidate_fields",
    "status",
}
REVEAL_STATUSES = {
    "fully_revealed_in_accepted_story_candidate_gameplay_open",
    "partially_revealed_accepted_story_candidate_projection",
    "partially_revealed_candidate_hub_open",
    "partially_revealed_engineering_blocked",
    "revealed_and_locked",
    "revealed_in_accepted_story",
    "revealed_in_accepted_story_candidate_interaction_open",
    "revealed_in_accepted_story_candidate_physics_blocked",
    "revealed_in_accepted_story_candidate_rules_open",
    "seeded_unresolved",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_ids(value: str) -> set[str]:
    return {item for item in value.split(";") if item}


def index_unique(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value:
            raise AssertionError(f"{label}: empty {key}")
        if value in result:
            raise AssertionError(f"{label}: duplicate {key}={value}")
        result[value] = row
    return result


def require_nonempty(row: dict[str, str], fields: set[str], label: str) -> None:
    missing = sorted(field for field in fields if not row.get(field, "").strip())
    if missing:
        raise AssertionError(f"{label}: empty required fields {missing}")


def validate(
    zones: list[dict[str, str]],
    states: list[dict[str, str]],
    reveals: list[dict[str, str]],
    bindings: list[dict[str, str]],
    master_text: str,
    svg_text: str,
    story_sha: str,
    receipt_sha: str,
) -> tuple[int, int, int]:
    zone_by_id = index_unique(zones, "zone_id", "location dossier")
    if set(zone_by_id) != EXPECTED_ZONES:
        raise AssertionError(f"zone set mismatch: {sorted(set(zone_by_id) ^ EXPECTED_ZONES)}")
    graph: dict[str, set[str]] = {}
    for zone_id, row in zone_by_id.items():
        require_nonempty(row, ZONE_REQUIRED_FIELDS, zone_id)
        if not row["status"].startswith("candidate_dossier_"):
            raise AssertionError(f"{zone_id}: false non-Candidate status {row['status']}")
        neighbors = split_ids(row["adjacent_zone_ids"])
        if not neighbors or not neighbors <= EXPECTED_ZONES or zone_id in neighbors:
            raise AssertionError(f"{zone_id}: invalid adjacency {sorted(neighbors)}")
        graph[zone_id] = neighbors
    for source, targets in graph.items():
        for target in targets:
            if source not in graph[target]:
                raise AssertionError(f"asymmetric adjacency: {source}->{target}")
    visited = {"MS-Z01"}
    queue: deque[str] = deque(visited)
    while queue:
        current = queue.popleft()
        for target in graph[current] - visited:
            visited.add(target)
            queue.append(target)
    if visited != EXPECTED_ZONES:
        raise AssertionError(f"disconnected location graph: {sorted(EXPECTED_ZONES - visited)}")

    state_by_id = index_unique(states, "state_id", "cargo ring states")
    if set(state_by_id) != EXPECTED_STATES:
        raise AssertionError(f"state set mismatch: {sorted(set(state_by_id) ^ EXPECTED_STATES)}")
    for index in range(9):
        state_id = f"CR-S{index:02d}"
        row = state_by_id[state_id]
        require_nonempty(row, STATE_REQUIRED_FIELDS, state_id)
        if row["sequence_order"] != str(index):
            raise AssertionError(f"{state_id}: sequence drift")
        if not row["status"].startswith("candidate_state_"):
            raise AssertionError(f"{state_id}: false non-Candidate status")
        if len(split_ids(row["allowed_player_verbs"])) < 3:
            raise AssertionError(f"{state_id}: too few player verbs")
    fixed_tokens = {
        "CR-S00": "直径超过200米",
        "CR-S01": "左掌敲钟",
        "CR-S03": "机魂来源仍未知",
        "CR-S04": "三比二获胜",
        "CR-S05": "越过黄线",
        "CR-S06": "普通观众不在环面",
        "CR-S07": "事故不改3:2",
        "CR-S08": "旧/新转子是两件实体",
    }
    for state_id, token in fixed_tokens.items():
        if token not in state_by_id[state_id]["locked_accepted_story_fields"]:
            raise AssertionError(f"{state_id}: missing locked token {token}")
    if "OP_C02_TOURNAMENT_MISSION_CLEAR" not in state_by_id["CR-S04"]["checkpoint_or_receipt"]:
        raise AssertionError("S04 must close Tournament before the stage accident")
    if "phase_checkpoint_not_mission_clear" not in state_by_id["CR-S06"]["checkpoint_or_receipt"]:
        raise AssertionError("S06 accident boundary must remain a phase checkpoint")
    if "OP_C02_STAGE_ACCIDENT_MISSION_CLEAR" not in state_by_id["CR-S07"]["checkpoint_or_receipt"]:
        raise AssertionError("S07 must own Accident Mission Clear")

    reveal_by_id = index_unique(reveals, "reveal_id", "reveal projection")
    if set(reveal_by_id) != EXPECTED_REVEALS:
        raise AssertionError(f"reveal set mismatch: {sorted(set(reveal_by_id) ^ EXPECTED_REVEALS)}")
    for reveal_id, row in reveal_by_id.items():
        require_nonempty(row, set(row) - {""}, reveal_id)
        if not row["truth_source_ref"].startswith(BINDING_ID + "#"):
            raise AssertionError(f"{reveal_id}: truth source is not the accepted C02 binding")
        if row["authority_level"] != "working_story_fact":
            raise AssertionError(f"{reveal_id}: authority promotion/drift")
        if row["design_status"] not in {"blocked", "sealed", "seeded"}:
            raise AssertionError(f"{reveal_id}: invalid design status")
        if row["status"] not in REVEAL_STATUSES:
            raise AssertionError(f"{reveal_id}: invalid projection status {row['status']}")
        if not row["state_writeback"].startswith("ST_"):
            raise AssertionError(f"{reveal_id}: missing typed state writeback")

    binding_by_id = index_unique(bindings, "binding_id", "accepted story bindings")
    if BINDING_ID not in binding_by_id:
        raise AssertionError("accepted C02 binding missing")
    binding = binding_by_id[BINDING_ID]
    expected_binding = {
        "accepted_story_path": STORY_REL,
        "accepted_story_sha256": STORY_SHA,
        "receipt_path": RECEIPT_REL,
        "receipt_sha256": RECEIPT_SHA,
        "durable_snapshot_status": "RESOLVED_REACHABLE_GIT_COMMIT",
        "current_match_status": "STORY_COMPONENTS_AND_RECEIPT_MATCH",
        "binding_status": "RESOLVED_DURABLE_CONTENT_BINDING",
    }
    for field, expected in expected_binding.items():
        if binding.get(field) != expected:
            raise AssertionError(f"accepted binding {field} drift")
    if story_sha != STORY_SHA or receipt_sha != RECEIPT_SHA:
        raise AssertionError("accepted C02 Reader or receipt bytes drifted")

    required_master_tokens = {
        "candidate_location_master_pack",
        "not_user_visual_approved",
        "not_gd2_sealed",
        BINDING_ID,
        "8 个可辨识宏观分区",
        "9 个连续状态",
        "不允许回 Hub、治疗、装备复原、地图重置",
        "OGD2-010/011/012/013",
        "进入 GD2 封存前仍缺的证据",
    }
    missing_master = sorted(token for token in required_master_tokens if token not in master_text)
    if missing_master:
        raise AssertionError(f"master pack missing boundary tokens {missing_master}")

    lowered_svg = svg_text.lower()
    external_reference_tokens = ('href="http://', 'href="https://', "url(http://", "url(https://")
    if "<script" in lowered_svg or any(token in lowered_svg for token in external_reference_tokens):
        raise AssertionError("SVG contains executable or external content")
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as error:
        raise AssertionError(f"SVG parse error: {error}") from error
    if root.attrib.get("viewBox") != "0 0 1600 1000":
        raise AssertionError("SVG viewBox drift")
    required_svg_tokens = EXPECTED_ZONES | {
        "约九米转子",
        "直径＞200m",
        "Candidate logic sketch",
        "S04 决赛锁定",
        "S06 事故CP",
        "S08 恢复/转子交割/离城",
        "人流",
        "机体",
        "重件/服务",
        "事故撤离",
    }
    missing_svg = sorted(token for token in required_svg_tokens if token not in svg_text)
    if missing_svg:
        raise AssertionError(f"SVG missing topology/state tokens {missing_svg}")

    return len(zone_by_id), len(state_by_id), len(reveal_by_id)


def run_self_test(
    zones: list[dict[str, str]],
    states: list[dict[str, str]],
    reveals: list[dict[str, str]],
    bindings: list[dict[str, str]],
    master_text: str,
    svg_text: str,
    story_sha: str,
    receipt_sha: str,
) -> int:
    cases: list[tuple[str, list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], str, str, str, str]] = []
    z = copy.deepcopy(zones); z.pop(); cases.append(("missing zone", z, states, reveals, bindings, master_text, svg_text, story_sha, receipt_sha))
    z = copy.deepcopy(zones); z[0]["adjacent_zone_ids"] = "MS-Z02"; cases.append(("asymmetric adjacency", z, states, reveals, bindings, master_text, svg_text, story_sha, receipt_sha))
    z = copy.deepcopy(zones); z[0]["status"] = "passed"; cases.append(("false zone pass", z, states, reveals, bindings, master_text, svg_text, story_sha, receipt_sha))
    s = copy.deepcopy(states); s.pop(); cases.append(("missing state", zones, s, reveals, bindings, master_text, svg_text, story_sha, receipt_sha))
    s = copy.deepcopy(states); s[4]["sequence_order"] = "9"; cases.append(("state order drift", zones, s, reveals, bindings, master_text, svg_text, story_sha, receipt_sha))
    s = copy.deepcopy(states); s[4]["locked_accepted_story_fields"] = "winner_open"; cases.append(("3:2 erased", zones, s, reveals, bindings, master_text, svg_text, story_sha, receipt_sha))
    r = copy.deepcopy(reveals); r.pop(); cases.append(("missing reveal", zones, states, r, bindings, master_text, svg_text, story_sha, receipt_sha))
    r = copy.deepcopy(reveals); r[0]["authority_level"] = "hard"; cases.append(("false authority promotion", zones, states, r, bindings, master_text, svg_text, story_sha, receipt_sha))
    b = copy.deepcopy(bindings); next(row for row in b if row["binding_id"] == BINDING_ID)["accepted_story_sha256"] = "0" * 64; cases.append(("binding hash drift", zones, states, reveals, b, master_text, svg_text, story_sha, receipt_sha))
    cases.append(("story bytes drift", zones, states, reveals, bindings, master_text, svg_text, "0" * 64, receipt_sha))
    cases.append(("master false completion", zones, states, reveals, bindings, master_text.replace("not_gd2_sealed", "gd2_sealed"), svg_text, story_sha, receipt_sha))
    cases.append(("svg missing zone", zones, states, reveals, bindings, master_text, svg_text.replace("MS-Z08", "ZONE_REMOVED"), story_sha, receipt_sha))

    rejected = 0
    for label, z_rows, s_rows, r_rows, b_rows, master, svg, s_sha, r_sha in cases:
        try:
            validate(z_rows, s_rows, r_rows, b_rows, master, svg, s_sha, r_sha)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(f"self-test mutation was not rejected: {label}")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    zones = read_tsv(DOSSIER_PATH)
    states = read_tsv(STATE_PATH)
    reveals = read_tsv(REVEAL_PATH)
    bindings = read_tsv(BINDING_PATH)
    master_text = MASTER_PATH.read_text(encoding="utf-8")
    svg_text = SVG_PATH.read_text(encoding="utf-8")
    story_sha = file_sha256(WORKSPACE / STORY_REL)
    receipt_sha = file_sha256(WORKSPACE / RECEIPT_REL)
    zone_count, state_count, reveal_count = validate(
        zones,
        states,
        reveals,
        bindings,
        master_text,
        svg_text,
        story_sha,
        receipt_sha,
    )
    print(
        "C02 Model Street master pack PASS: "
        f"zones={zone_count}; cargo_ring_states={state_count}; reveals={reveal_count}; "
        f"accepted_story_sha={story_sha[:12]}; svg_sha={file_sha256(SVG_PATH)[:12]}; "
        "Candidate only; zero Build; zero human evidence; zero visual/GD2/asset authority"
    )
    if args.self_test:
        rejected = run_self_test(
            zones,
            states,
            reveals,
            bindings,
            master_text,
            svg_text,
            story_sha,
            receipt_sha,
        )
        print(f"C02 Model Street self-test PASS: rejected={rejected}/{rejected}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"C02 Model Street master pack FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
