#!/usr/bin/env python3
"""Build and validate the Candidate 29-package / 77-record D07 crosswalk.

This script deliberately reads the current Canon authority manifest, but it does
not migrate or rewrite Canon.  The legacy 77-record tables remain Candidate
inheritance evidence; exact Working entity rows only prove the scope stated in
the authority manifest and never promote the future lifecycle fields.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path


FIELDNAMES = [
    "coverage_id",
    "record_id",
    "record_name",
    "package_uid",
    "package_name",
    "source_record_ref",
    "source_authority_tier",
    "source_authority_scope",
    "authority_evidence_refs",
    "package_selection_state",
    "access_disposition",
    "entity_access_id",
    "related_entity_access_ids",
    "disposition_reason",
    "current_fact_window",
    "candidate_chapter_window",
    "chapter_window_audit",
    "candidate_ownership_class",
    "candidate_control_subject",
    "candidate_first_control_contract",
    "mapped_access_owner_or_custody",
    "mapped_access_control_boundary",
    "detailed_action_contract_required",
    "action_contract_scope",
    "record_asset_tier",
    "asset_family",
    "package_production_tier",
    "record_class",
    "status",
]


GAP_FIELDNAMES = [
    "gap_id",
    "candidate_key",
    "candidate_name",
    "source_ref",
    "selection_state",
    "legacy_29_member",
    "legacy_77_record_ids",
    "recordization_state",
    "entity_access_disposition",
    "entity_access_id",
    "related_entity_access_ids",
    "candidate_chapter_window",
    "package_production_tier",
    "source_ids",
    "open_decision",
    "resolution_requirement",
    "status",
]


DIRECT_ACCESS = {
    "V353U001": (
        "ENT_GUARDIAN_Z",
        "同一馆守Z主体；D07行已分开纪存路线提案、兜灯整备和机体四肢控制。",
    ),
    "V353U024": (
        "ENT_HAOSI_SOCIAL_BRAVE",
        "同一豪司/社勇王人机组；D07行已锁企业保产权、豪司主驾与社勇王主体AI可拒绝。",
    ),
    "V353U048": (
        "ENT_OLD_BOXER",
        "同一旧拳王机主体；D07行已分开章末随舰与长期部署/成长候选。",
    ),
    "V353U071": (
        "ENT_NO_NAME_ONE",
        "同一无牌一号全尺寸竞技实机；D07行已锁机体可拒绝改装且登舰不等于万机馆所有。",
    ),
}


RELATED_ACCESS = {
    "V353U050": "ENT_ARK_T",
}


DISCARDED_RECORDS = {
    "V353U002": (
        "当前Canon将“黑展柜皇影/V353U002”隔离为History；若重用必须以新角色功能、载体、尺寸、控制和生命周期重新立项，不能直接复活旧记录。",
        "docs/superpowers/specs/data/canon/entities.tsv#entity_id=MECHA_BLACK_SHOWCASE_EMPEROR_SHADOW",
    )
}


MAPPED_ACTION_SCOPE = {
    "V353U001": "body_actions;successor_arm;consent;temporary_route_input",
    "V353U024": "pilot_proposal;mecha_refusal;tool_actions;enterprise_custody",
    "V353U048": "nonlethal_boxing;stop_punch;training;damage_state",
    "V353U071": "modular_loadout;body_consent;nonlethal_competition;custody",
}


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "scripts/check_canon_authority.py").is_file():
            return candidate
    raise RuntimeError("Could not locate repository root")


def read_rows(path: Path, key: str) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise ValueError(f"Empty TSV: {path}")
    keyed = {row[key]: row for row in rows}
    if len(keyed) != len(rows):
        raise ValueError(f"Duplicate {key} in {path}")
    return rows, keyed


def clean(value: str) -> str:
    return value.replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def expand_record_ids(value: str) -> list[str]:
    expanded: list[str] = []
    for token in value.split(";"):
        token = token.strip()
        if "-" not in token:
            expanded.append(token)
            continue
        left, right = token.split("-", 1)
        left_match = re.fullmatch(r"(V\d+U)(\d+)", left)
        right_match = re.fullmatch(r"(V\d+U)(\d+)", right)
        if not left_match or not right_match or left_match.group(1) != right_match.group(1):
            raise ValueError(f"Unsupported record range: {token}")
        prefix = left_match.group(1)
        start = int(left_match.group(2))
        end = int(right_match.group(2))
        width = len(left_match.group(2))
        expanded.extend(f"{prefix}{index:0{width}d}" for index in range(start, end + 1))
    return expanded


def action_scope(record_class: str) -> str:
    if "combination" in record_class:
        return "member_consent;formation;component_occupancy;split_exit"
    if "group" in record_class or "team" in record_class:
        return "group_command;member_identity;formation_actions;partial_availability"
    if "capital_ship" in record_class or "gunboat" in record_class:
        return "C2_command;carrier_body;multi_map_support;withdrawal"
    if "infrastructure" in record_class:
        return "mode_contract;node_ownership;operator_actions;failure_state"
    if "small" in record_class or "digital" in record_class or "ai_carrier" in record_class:
        return "support_action;body_or_carrier_boundary;absence_alternative"
    return "movement;signature_actions;intent;cost;counterplay;consent_or_pilot_boundary"


def render(repo_root: Path) -> tuple[str, str]:
    story = repo_root / "docs/superpowers/specs/data/story"
    canon = repo_root / "docs/superpowers/specs/data/canon"
    package_dir = Path(__file__).resolve().parent.parent

    inv_path = story / "v35_series_roster_lifecycle_inventory_v1.tsv"
    own_path = story / "v35_series_record_ownership_lifecycle_v1.tsv"
    sem_path = story / "v35_series_roster_record_semantics_v1.tsv"
    package_lifecycle_path = story / "v35_series_package_lifecycle_spine_v1.tsv"
    alloc_path = story / "v35_series_structure_roster_chapter_allocation_v1.tsv"
    access_path = package_dir / "data/series-entity-access-spine.tsv"

    inv_rows, inv = read_rows(inv_path, "unit_id")
    _, own = read_rows(own_path, "unit_id")
    _, sem = read_rows(sem_path, "unit_id")
    package_rows, package_lifecycle = read_rows(package_lifecycle_path, "package_uid")
    _, alloc = read_rows(alloc_path, "package_uid")
    _, access = read_rows(access_path, "entity_id")
    _, entities = read_rows(canon / "entities.tsv", "entity_id")

    with (canon / "authority_manifest.tsv").open(encoding="utf-8", newline="") as handle:
        manifest_rows = list(csv.DictReader(handle, delimiter="\t"))
    manifest = {
        row["record_id"]: row
        for row in manifest_rows
        if row["record_type"] == "entity"
    }

    inv_ids = set(inv)
    inventory_packages = {row["package_uid"] for row in inv_rows}
    if len(inv_rows) != 77 or len(inventory_packages) != 29:
        raise ValueError("Authoritative Candidate inheritance set is not exactly 29 packages / 77 records")
    if set(own) != inv_ids or set(sem) != inv_ids:
        raise ValueError("77-record inventory, ownership, and semantics keys are not identical")
    missing_alloc = {row["package_uid"] for row in inv_rows} - set(alloc)
    if missing_alloc:
        raise ValueError(f"Packages missing current Candidate allocation rows: {sorted(missing_alloc)}")
    if len(package_rows) != 29 or set(package_lifecycle) != inventory_packages:
        raise ValueError("29-package lifecycle spine does not match the 77-record inventory package set")
    assigned_records: list[str] = []
    for package_uid, package_row in package_lifecycle.items():
        package_records = expand_record_ids(package_row["record_ids"])
        expected = [row["unit_id"] for row in inv_rows if row["package_uid"] == package_uid]
        if package_records != expected:
            raise ValueError(
                f"Package record membership mismatch for {package_uid}: {package_records} != {expected}"
            )
        assigned_records.extend(package_records)
    if len(assigned_records) != 77 or set(assigned_records) != inv_ids:
        raise ValueError("29-package lifecycle spine does not cover each of the 77 records exactly once")
    missing_access = {value[0] for value in DIRECT_ACCESS.values()} - set(access)
    if missing_access:
        raise ValueError(f"Direct entity_access IDs missing from D07 spine: {sorted(missing_access)}")
    missing_related = set(RELATED_ACCESS.values()) - set(access)
    if missing_related:
        raise ValueError(f"Related entity_access IDs missing from D07 spine: {sorted(missing_related)}")

    output_rows: list[dict[str, str]] = []
    for index, inventory in enumerate(inv_rows, start=1):
        record_id = inventory["unit_id"]
        ownership = own[record_id]
        semantics = sem[record_id]
        package = alloc[inventory["package_uid"]]
        authority = manifest.get(record_id)
        entity = entities.get(record_id)

        evidence_refs = [
            f"docs/superpowers/specs/data/story/{inv_path.name}#unit_id={record_id}",
            f"docs/superpowers/specs/data/story/{own_path.name}#unit_id={record_id}",
            f"docs/superpowers/specs/data/story/{sem_path.name}#unit_id={record_id}",
            f"docs/superpowers/specs/data/story/{package_lifecycle_path.name}#package_uid={inventory['package_uid']}",
            f"docs/superpowers/specs/data/story/{alloc_path.name}#package_uid={inventory['package_uid']}",
        ]

        if record_id in DISCARDED_RECORDS:
            disposition = "discarded"
            entity_access_id = "none"
            related = "none"
            reason, history_ref = DISCARDED_RECORDS[record_id]
            evidence_refs.append(history_ref)
            authority_tier = "history_conflict_plus_candidate_legacy_record"
            authority_scope = "当前Canon已隔离旧主体；77行只保留继承追溯，不得恢复或约束当前设计"
            current_window = "history_only"
            window_audit = "history_only_not_a_current_window"
            action_required = "not_applicable_discarded"
            scope = "new_record_required_if_repitched"
            mapped_owner = "none"
            mapped_control = "none"
            row_status = "candidate_crosswalk_discarded_by_current_history_boundary"
        elif record_id in DIRECT_ACCESS:
            disposition = "mapped"
            entity_access_id, reason = DIRECT_ACCESS[record_id]
            related = "none"
            authority_tier = "working_identity_plus_candidate_future_contract"
            authority_scope = "authority_manifest只证明同ID实体的当前身份与已验收场景；77账未来归属/分舰/终局与L3章窗仍为Candidate"
            evidence_refs.append(f"docs/superpowers/specs/data/canon/authority_manifest.tsv#record_id={record_id}")
            evidence_refs.append(f"data/series-entity-access-spine.tsv#entity_id={entity_access_id}")
            current_window = (
                f"manifest:{authority['version_scope']}|first_foreshadow:{entity['first_foreshadow']}|"
                f"first_formal:{entity['first_formal_appearance']}"
            )
            if record_id == "V353U071":
                window_audit = "conflict_current_C02_trial_control_vs_candidate_C06-C07_first_playable"
            else:
                window_audit = "aligned_at_current_first_control_granularity"
            action_required = "required_now"
            scope = MAPPED_ACTION_SCOPE[record_id]
            mapped_owner = access[entity_access_id]["owner_or_custody"]
            mapped_control = access[entity_access_id]["control_boundary"]
            row_status = "candidate_crosswalk_mapped_not_user_approved"
        else:
            disposition = "open"
            entity_access_id = "none"
            related = RELATED_ACCESS.get(record_id, "none")
            mapped_owner = "none"
            mapped_control = "none"
            if authority and authority["canon_level"] in {"hard", "working"} and authority["lifecycle_status"] == "active":
                authority_tier = "working_identity_plus_candidate_future_contract"
                authority_scope = "authority_manifest只证明同ID实体的当前身份与已验收场景；D07无逐实体接入行，77账未来合同仍为Candidate"
                evidence_refs.append(f"docs/superpowers/specs/data/canon/authority_manifest.tsv#record_id={record_id}")
                current_window = (
                    f"manifest:{authority['version_scope']}|first_foreshadow:{entity['first_foreshadow']}|"
                    f"first_formal:{entity['first_formal_appearance']}"
                )
                window_audit = "working_scene_or_identity_exists_but_D07_access_window_open"
                reason = "同ID Working实体或已验收场景已成立，但D07的17行接入脊柱无该逐实体行；故当前故事事实不自动扩张为正式Roster、所有权或动作合同。"
                action_required = "required_before_next_runtime_reuse"
                row_status = "candidate_crosswalk_open_working_identity"
            elif authority and authority["canon_level"] == "candidate":
                authority_tier = "candidate_identity_and_future_contract"
                authority_scope = "同ID实体及77账未来生命周期均为Candidate；无Current/Working接入承诺"
                evidence_refs.append(f"docs/superpowers/specs/data/canon/authority_manifest.tsv#record_id={record_id}")
                current_window = "none_confirmed"
                window_audit = "candidate_only_no_current_comparison"
                reason = "同ID Canon记录仍是Candidate，且D07无逐实体接入行；保留竞争资格，不允许预告入队/所有权/技能。"
                action_required = "conditional_on_selection"
                row_status = "candidate_crosswalk_open_candidate_identity"
            else:
                authority_tier = "candidate_legacy_inventory_only"
                authority_scope = "三张77表与29包章窗都是Candidate设计输入，无同ID Current/Working实体权威"
                current_window = "none_confirmed"
                window_audit = "candidate_only_no_current_comparison"
                reason = "旧77继承审计记录；当前只有包级Candidate选择与章窗，无D07逐实体接入行。保留为OPEN不等于已删除或已承诺。"
                action_required = "conditional_on_selection"
                row_status = "candidate_crosswalk_open_legacy_inventory"
            scope = action_scope(semantics["record_class"])

        candidate_window = (
            f"seed:{package['seed_chapter']}|first_playable:{package['first_playable_chapter']}|"
            f"formal_join:{package['formal_join_window']}"
        )
        record_asset_tier = inventory["asset_capacity_risk"].split(";", 1)[0]
        source_ref = (
            f"v35_series_roster_lifecycle_inventory_v1.tsv#unit_id={record_id};"
            f"v35_series_record_ownership_lifecycle_v1.tsv#unit_id={record_id};"
            f"v35_series_roster_record_semantics_v1.tsv#unit_id={record_id};"
            f"v35_series_package_lifecycle_spine_v1.tsv#package_uid={inventory['package_uid']}"
        )

        output_rows.append(
            {
                "coverage_id": f"SRCOV{index:03d}",
                "record_id": record_id,
                "record_name": inventory["display_name"],
                "package_uid": inventory["package_uid"],
                "package_name": package["package_name"],
                "source_record_ref": source_ref,
                "source_authority_tier": authority_tier,
                "source_authority_scope": authority_scope,
                "authority_evidence_refs": ";".join(evidence_refs),
                "package_selection_state": package["selection_state"],
                "access_disposition": disposition,
                "entity_access_id": entity_access_id,
                "related_entity_access_ids": related,
                "disposition_reason": reason,
                "current_fact_window": current_window,
                "candidate_chapter_window": candidate_window,
                "chapter_window_audit": window_audit,
                "candidate_ownership_class": ownership["ownership_class"],
                "candidate_control_subject": ownership["subject_anchor"],
                "candidate_first_control_contract": ownership["first_control_contract"],
                "mapped_access_owner_or_custody": mapped_owner,
                "mapped_access_control_boundary": mapped_control,
                "detailed_action_contract_required": action_required,
                "action_contract_scope": scope,
                "record_asset_tier": record_asset_tier,
                "asset_family": semantics["asset_family"],
                "package_production_tier": package["production_tier"],
                "record_class": semantics["record_class"],
                "status": row_status,
            }
        )

    counts = {value: 0 for value in ("mapped", "open", "merged", "reserve", "discarded")}
    for row in output_rows:
        counts[row["access_disposition"]] += 1
    if counts != {"mapped": 4, "open": 72, "merged": 0, "reserve": 0, "discarded": 1}:
        raise ValueError(f"Unexpected access disposition counts: {counts}")

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDNAMES, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for row in output_rows:
        writer.writerow({key: clean(value) for key, value in row.items()})

    nonlegacy_rows = [row for row in alloc.values() if row["package_uid"] not in inventory_packages]
    if len(alloc) != 44 or len(nonlegacy_rows) != 15:
        raise ValueError(
            f"Expected 44 current allocation keys = 29 legacy + 15 nonlegacy, got {len(alloc)} / {len(nonlegacy_rows)}"
        )
    gap_rows: list[dict[str, str]] = []
    for index, package in enumerate(nonlegacy_rows, start=1):
        key = package["package_uid"]
        entity_access_id = "none"
        related = "none"
        if key == "PK_CORE_INDEX_ANGEL":
            recordization_state = "working_structure_entity_without_legacy_77_record"
            access_disposition = "mapped_package_only"
            entity_access_id = "ENT_INDEX_ANGEL"
            requirement = "在正式原型/GD1前建立独立Roster record ID、身体/驾驶/共驾动作合同和资产边界。"
            row_status = "candidate_gap_working_structure_package_recordization_pending"
        elif key == "RQG01":
            recordization_state = "new_candidate_package_no_legacy_77_record"
            access_disposition = "open"
            related = "ENT_RESONANCE_GROUP"
            requirement = "先裁决与米拉/艾达/共鸣双机接入组的同一性，再建逐机体记录；不得只用包名替代两个主体。"
            row_status = "candidate_gap_open_recordization_pending"
        elif package["selection_state"] == "motif_only":
            recordization_state = "not_a_roster_record_motif_only"
            access_disposition = "not_applicable_motif_only"
            requirement = "保持场景/玩法语法；除非另行通过Roster质量门，不新造参战机或逐机记录。"
            row_status = "candidate_gap_non_roster_motif"
        elif package["selection_state"] == "retired_reserve":
            recordization_state = "retired_reserve_no_record"
            access_disposition = "reserve"
            requirement = "不建记录；若未来重启，必须以新旗舰企划重过驾驶员/宿敌/名场面/升级/玩法/终局六项门。"
            row_status = "candidate_gap_retired_reserve"
        else:
            recordization_state = "new_or_overlay_candidate_without_legacy_77_record"
            access_disposition = "open"
            requirement = "在入选与逐章GD1前裁决新增/替换/合并关系，再建主体、驾驶、所有/控制、动作与资产记录。"
            row_status = "candidate_gap_open_recordization_pending"
        if entity_access_id != "none" and entity_access_id not in access:
            raise ValueError(f"Nonlegacy package maps to missing entity_access ID: {entity_access_id}")
        if related != "none" and related not in access:
            raise ValueError(f"Nonlegacy package relates to missing entity_access ID: {related}")
        gap_rows.append(
            {
                "gap_id": f"SRGAP{index:02d}",
                "candidate_key": key,
                "candidate_name": package["package_name"],
                "source_ref": f"v35_series_structure_roster_chapter_allocation_v1.tsv#package_uid={key}",
                "selection_state": package["selection_state"],
                "legacy_29_member": "false",
                "legacy_77_record_ids": "none",
                "recordization_state": recordization_state,
                "entity_access_disposition": access_disposition,
                "entity_access_id": entity_access_id,
                "related_entity_access_ids": related,
                "candidate_chapter_window": (
                    f"seed:{package['seed_chapter']}|first_playable:{package['first_playable_chapter']}|"
                    f"formal_join:{package['formal_join_window']}"
                ),
                "package_production_tier": package["production_tier"],
                "source_ids": package["source_ids"],
                "open_decision": package["open_decision"],
                "resolution_requirement": requirement,
                "status": row_status,
            }
        )
    gap_counts: dict[str, int] = {}
    for row in gap_rows:
        disposition = row["entity_access_disposition"]
        gap_counts[disposition] = gap_counts.get(disposition, 0) + 1
    if gap_counts != {"mapped_package_only": 1, "open": 12, "not_applicable_motif_only": 1, "reserve": 1}:
        raise ValueError(f"Unexpected nonlegacy gap disposition counts: {gap_counts}")

    gap_buffer = io.StringIO(newline="")
    gap_writer = csv.DictWriter(gap_buffer, fieldnames=GAP_FIELDNAMES, delimiter="\t", lineterminator="\n")
    gap_writer.writeheader()
    for row in gap_rows:
        gap_writer.writerow({key: clean(value) for key, value in row.items()})
    return buffer.getvalue(), gap_buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the committed TSV differs")
    parser.add_argument("--output", type=Path, help="Override output path")
    parser.add_argument("--gap-output", type=Path, help="Override nonlegacy package gap output path")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = find_repo_root(script_path.parent)
    output = args.output or script_path.parent.parent / "data/series-roster-coverage-crosswalk.tsv"
    gap_output = args.gap_output or script_path.parent.parent / "data/series-roster-nonlegacy-package-gaps.tsv"
    rendered, gap_rendered = render(repo_root)

    if args.check:
        expected = ((output, rendered), (gap_output, gap_rendered))
        for path, content in expected:
            if not path.is_file():
                print(f"MISSING: {path}", file=sys.stderr)
                return 1
            if path.read_text(encoding="utf-8") != content:
                print(f"STALE: {path}", file=sys.stderr)
                return 1
        print(
            "PASS series roster coverage: legacy 29 packages / 77 records / 4 mapped / 72 open / 1 discarded; "
            "15 nonlegacy allocation keys / 1 package-only mapped / 12 open / 1 motif / 1 reserve"
        )
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    gap_output.parent.mkdir(parents=True, exist_ok=True)
    gap_output.write_text(gap_rendered, encoding="utf-8")
    print(f"WROTE {output}")
    print(f"WROTE {gap_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
