#!/usr/bin/env python3
"""Query current, candidate, or historical project Canon without layer leakage."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANON_DIR = ROOT / "docs" / "superpowers" / "specs" / "data" / "canon"
GRAPH_DIR = ROOT / "docs" / "superpowers" / "specs" / "data" / "design_graph"

FILES = {
    "entities": CANON_DIR / "entities.tsv",
    "scenes": CANON_DIR / "scenes.tsv",
    "presence": CANON_DIR / "scene_entity_presence.tsv",
    "rules": CANON_DIR / "runtime_rules.tsv",
    "gags": CANON_DIR / "gag_hooks.tsv",
    "floors": CANON_DIR / "wanji_floors.tsv",
    "locations": CANON_DIR / "wanji_locations.tsv",
    "exhibitions": CANON_DIR / "wanji_exhibition_zones.tsv",
    "coverage": CANON_DIR / "wanji_roster_zone_coverage.tsv",
    "collections": CANON_DIR / "wanji_collection_taxonomy.tsv",
    "berths": CANON_DIR / "wanji_carrier_berths.tsv",
    "terminal": CANON_DIR / "jicun_archive_terminal_views.tsv",
    "art_locks": CANON_DIR / "character_mecha_art_locks.tsv",
    "identity": CANON_DIR / "identity_links.tsv",
    "registry": GRAPH_DIR / "doc_registry.tsv",
    "graph_nodes": GRAPH_DIR / "graph_nodes.tsv",
    "graph_edges": GRAPH_DIR / "graph_edges.tsv",
    "terms": GRAPH_DIR / "canonical_terms.tsv",
    "watchlist": GRAPH_DIR / "consistency_watchlist.tsv",
}

AUTHORITY_FILE = CANON_DIR / "authority_manifest.tsv"
CANON_SECTIONS = [
    "entities",
    "scenes",
    "presence",
    "rules",
    "gags",
    "floors",
    "locations",
    "exhibitions",
    "coverage",
    "collections",
    "berths",
    "terminal",
    "art_locks",
    "identity",
]
GRAPH_SECTIONS = ["registry", "graph_nodes", "graph_edges", "terms", "watchlist"]

RECORD_TYPES = {
    "entities": ("entity", "entity_id"),
    "scenes": ("scene", "scene_id"),
    "presence": ("scene_presence", "presence_id"),
    "rules": ("runtime_rule", "rule_id"),
    "gags": ("gag_hook", "hook_id"),
    "floors": ("wanji_floor", "floor_id"),
    "locations": ("wanji_location", "location_id"),
    "exhibitions": ("wanji_exhibition", "zone_id"),
    "coverage": ("wanji_coverage", "package_id"),
    "collections": ("wanji_collection", "collection_id"),
    "berths": ("wanji_berth", "berth_id"),
    "terminal": ("terminal_view", "view_id"),
    "art_locks": ("art_lock", "lock_id"),
    "identity": ("identity_link", "link_id"),
}

SECTION_ALIASES = {
    "entity": "entities", "entities": "entities",
    "scene": "scenes", "scenes": "scenes",
    "presence": "presence", "scene-presence": "presence", "scene_presence": "presence",
    "attendance": "presence", "in-scene": "presence",
    "rule": "rules", "rules": "rules",
    "gag": "gags", "gags": "gags", "hook": "gags", "hooks": "gags",
    "floor": "floors", "floors": "floors",
    "location": "locations", "locations": "locations",
    "exhibition": "exhibitions", "exhibitions": "exhibitions",
    "zone": "exhibitions", "zones": "exhibitions",
    "gallery": "exhibitions", "galleries": "exhibitions",
    "coverage": "coverage", "roster": "coverage",
    "rosterzone": "coverage", "roster-zones": "coverage", "roster_zones": "coverage",
    "collection": "collections", "collections": "collections",
    "taxonomy": "collections", "collect": "collections",
    "berth": "berths", "berths": "berths", "carrier": "berths", "hangar": "berths",
    "terminal": "terminal", "archive-terminal": "terminal",
    "archive_terminal": "terminal", "notebook": "terminal", "mapview": "terminal", "views": "terminal",
    "art": "art_locks", "arts": "art_locks", "visual": "art_locks", "visuals": "art_locks",
    "lock": "art_locks", "locks": "art_locks", "art-lock": "art_locks",
    "art_locks": "art_locks", "character-lock": "art_locks", "mecha-lock": "art_locks",
    "identity": "identity", "identity-link": "identity", "same-as": "identity",
    "registry": "registry", "doc": "registry", "docs": "registry", "documents": "registry",
    "term": "terms", "terms": "terms", "canonical-term": "terms", "canonical_terms": "terms",
    "watchlist": "watchlist", "risk": "watchlist", "risks": "watchlist", "consistency": "watchlist",
}

GROUP_ALIASES = {
    "layout": ["floors", "locations", "exhibitions", "coverage", "collections", "berths", "terminal", "art_locks"],
    "space": ["floors", "locations", "exhibitions", "coverage", "collections", "berths", "terminal", "art_locks"],
    "map": ["floors", "locations", "exhibitions", "coverage", "collections", "berths", "terminal", "art_locks"],
    "graph": ["graph_nodes", "graph_edges"],
    "node": ["graph_nodes", "graph_edges"],
    "nodes": ["graph_nodes", "graph_edges"],
    "edge": ["graph_nodes", "graph_edges"],
    "edges": ["graph_nodes", "graph_edges"],
    "index": GRAPH_SECTIONS,
    "indices": GRAPH_SECTIONS,
    "design-graph": GRAPH_SECTIONS,
    "design_graph": GRAPH_SECTIONS,
}

AUTHORITY_ALIASES = {
    "current": "current",
    "candidate": "candidate",
    "history": "history",
    "all": "all",
    "audit": "audit",
    "everything": "audit",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def row_text(row: dict[str, str]) -> str:
    return "\t".join(str(value) for value in row.values())


def matches(row: dict[str, str], query: str) -> bool:
    return query.casefold() in row_text(row).casefold()


def is_historical_graph(section: str, row: dict[str, str]) -> bool:
    if section == "registry":
        return any("histor" in row.get(field, "").lower() for field in ("layer", "doc_type", "notes"))
    if section == "graph_nodes":
        return any("histor" in row.get(field, "").lower() for field in ("node_type", "source_layer", "status"))
    if section == "graph_edges":
        return "histor" in row.get("relation", "").lower()
    if section == "terms":
        return "histor" in row.get("term_type", "").lower()
    if section == "watchlist":
        return "histor" in row.get("status", "").lower()
    return False


def load_authority() -> dict[tuple[str, str], dict[str, str]]:
    if not AUTHORITY_FILE.exists():
        raise FileNotFoundError(
            f"Missing {AUTHORITY_FILE.relative_to(ROOT)}; run scripts/build_canon_authority_manifest.py"
        )
    return {
        (row["record_type"], row["record_id"]): row
        for row in read_tsv(AUTHORITY_FILE)
    }


def authority_for(
    section: str,
    row: dict[str, str],
    authority: dict[tuple[str, str], dict[str, str]],
) -> dict[str, str] | None:
    record_type, id_field = RECORD_TYPES[section]
    return authority.get((record_type, row.get(id_field, "")))


def authority_allows(mode: str, meta: dict[str, str] | None) -> bool:
    if meta is None:
        return False
    level = meta.get("canon_level", "")
    lifecycle = meta.get("lifecycle_status", "")
    if mode == "current":
        return level in {"hard", "working"} and lifecycle == "active"
    if mode == "candidate":
        return level == "candidate" and lifecycle == "candidate"
    if mode == "history":
        return level == "history" or lifecycle in {"history", "deprecated"}
    if mode == "all":
        return level in {"hard", "working", "candidate"}
    return True


def graph_allows(mode: str, section: str, row: dict[str, str]) -> bool:
    historical = is_historical_graph(section, row)
    if mode == "history":
        return historical
    if mode == "audit":
        return True
    return not historical


def print_row(section: str, row: dict[str, str], meta: dict[str, str] | None) -> None:
    print(f"[{section}]")
    if meta:
        for key in (
            "canon_level",
            "lifecycle_status",
            "version_scope",
            "source_of_truth",
            "supersedes",
            "last_confirmed",
        ):
            value = meta.get(key, "")
            if value:
                print(f"authority_{key}: {value}")
    for key, value in row.items():
        if value:
            print(f"{key}: {value}")
    print("")


def deprecated_alias_target(row: dict[str, str] | None) -> str | None:
    if not row or row.get("status") != "deprecated_alias":
        return None
    for part in row.get("implementation_policy", "").split(";"):
        if part.startswith("deprecated_alias_of="):
            return part.split("=", 1)[1].strip()
    return None


def parse_args(args: list[str]) -> tuple[str, list[str], str]:
    authority_mode = "current"
    if args and args[0] in AUTHORITY_ALIASES:
        authority_mode = AUTHORITY_ALIASES[args.pop(0)]

    sections: list[str] | None = None
    if args and args[0] in GROUP_ALIASES:
        sections = GROUP_ALIASES[args.pop(0)]
    elif args and args[0] in SECTION_ALIASES:
        sections = [SECTION_ALIASES[args.pop(0)]]

    if not args:
        raise ValueError("A non-empty query is required.")
    query = " ".join(args)
    if sections is None:
        sections = CANON_SECTIONS + (
            GRAPH_SECTIONS if authority_mode in {"history", "audit"} else []
        )
    return authority_mode, sections, query


def print_help() -> None:
    print("Usage: scripts/canon-query.sh [current|candidate|history|all|audit] [section] <query>")
    print("")
    print("Authority modes:")
    print("  current    Hard + Working Canon only (default)")
    print("  candidate  Candidate Canon only")
    print("  history    Superseded/deprecated Canon; historical graph rows when index is explicit")
    print("  all        Current + Candidate Canon, no history and no graph by default")
    print("  audit      Every Canon layer plus the design graph")
    print("")
    print("Examples:")
    print("  scripts/canon-query.sh 馆守Z")
    print("  scripts/canon-query.sh entity CH_JICUN")
    print("  scripts/canon-query.sh candidate entity CONCEPT_JICUN_MACHINE_SOUL_LINK")
    print("  scripts/canon-query.sh candidate scene V359-C04E03-CREATIVE")
    print("  scripts/canon-query.sh history scene V31-C01E03-BATTLE")
    print("  scripts/canon-query.sh index C04")
    print("  scripts/canon-query.sh audit C04")


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print_help()
        return 0
    try:
        authority_mode, sections, query = parse_args(sys.argv[1:])
        authority = load_authority()
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    entity_rows = read_tsv(FILES["entities"])
    entities_by_id = {row.get("entity_id", ""): row for row in entity_rows}

    # Deprecated exact IDs remain useful entry points, but they always redirect
    # to the active identity and never print the obsolete row as current Canon.
    if sections == ["entities"] and query in entities_by_id and authority_mode != "history":
        target_id = deprecated_alias_target(entities_by_id[query])
        if target_id:
            target = entities_by_id.get(target_id)
            target_meta = authority_for("entities", target, authority) if target else None
            if target and authority_allows(authority_mode, target_meta):
                print(f"[entities:alias_redirect]\nfrom_entity_id: {query}\nto_entity_id: {target_id}\n")
                print_row("entities", target, target_meta)
                return 0

    results: list[tuple[str, dict[str, str], dict[str, str] | None]] = []
    for section in sections:
        rows = read_tsv(FILES[section])
        if len(sections) == 1 and section in RECORD_TYPES:
            _, id_field = RECORD_TYPES[section]
            exact_rows = [
                row
                for row in rows
                if row.get(id_field, "").casefold() == query.casefold()
                and authority_allows(authority_mode, authority_for(section, row, authority))
            ]
            if exact_rows:
                rows = exact_rows
        for row in rows:
            if not matches(row, query):
                continue
            if section in RECORD_TYPES:
                meta = authority_for(section, row, authority)
                if not authority_allows(authority_mode, meta):
                    continue
            else:
                meta = None
                if not graph_allows(authority_mode, section, row):
                    continue
            results.append((section, row, meta))

    if not results:
        print(f"No {authority_mode} Canon rows matched: {query}", file=sys.stderr)
        return 1

    limit = 120 if authority_mode == "audit" else 80
    for section, row, meta in results[:limit]:
        print_row(section, row, meta)
    if len(results) > limit:
        print(
            f"Matched {len(results)} rows; showing {limit}. Narrow the section or query.",
            file=sys.stderr,
        )
    else:
        print(f"Matched {len(results)} {authority_mode} row(s).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
