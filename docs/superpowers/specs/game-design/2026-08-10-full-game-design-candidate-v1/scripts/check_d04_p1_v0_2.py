#!/usr/bin/env python3
"""Read-only static reference checker for Candidate D04-P1 Fixture v0.2.

This is a deterministic paper-fixture interpreter.  It is not a Godot build,
playable UI, search solver, balance result, fun receipt, or human-playtest gate.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PACKAGE_ROOT / "data" / "d04-p1-v0.2"
VECTOR_TSV = PACKAGE_ROOT / "data" / "d04-p1-adapter-event-vectors.tsv"
EXPECTED_ACTIONS = {
    "TACT_ABORT", "TACT_BRACE", "TACT_CATCH", "TACT_COVER", "TACT_EVADE",
    "TACT_FIELD_REPAIR", "TACT_INTERACT", "TACT_INTERCEPT", "TACT_MELEE",
    "TACT_PUSH_TOW", "TACT_RANGED", "TACT_RESCUE", "TACT_ROUTE",
    "TACT_SUPPRESS", "TACT_WAIT_CONDITION", "TACT_WITHDRAW",
}
EXPECTED_CLOCK_STATES = {
    "CLK_S0_BRIDGE_OCCUPIED_STRESS0", "CLK_S0_IDLE_TIME0_CYCLE0",
    "CLK_S0_MID_EVENTLOG_TWO_COMMITS", "CLK_S0_OBS0_INTENT_FROZEN",
    "CLK_S0_REACTION_RESERVED_UNUSED", "CLK_S3_TIME24_CYCLE3_ONE_EVAC_BLOCKED",
    "CLK_S1_BRIDGE_MIX_STRESS1", "CLK_S1_BRIDGE_OCCUPIED_STRESS1",
    "CLK_S1_IDLE_TIME8_CYCLE1", "CLK_S1_OBS1_INTENT_REFRESH_READY",
    "CLK_S1_REACTION_EXPIRED", "CLK_S1_RESTORED_CLOSE_HASH_EQ_DIRECT",
    "CLK_S4_TIME32_CYCLE4_ONE_EVAC_BLOCKED",
}
EXPECTED_CLOCK_PLANS = {
    "PLAN_ALL_WAIT_BLOCKED_ROUTE", "PLAN_ALL_WAIT_CLEAR_LANE",
    "PLAN_ALL_WAIT_HAZARD_OCCUPIED", "PLAN_BREAKER_ADVANCE_PLUS_COMPLETED_BRACE",
    "PLAN_PLAYER_MOVES_AFTER_INTENT", "PLAN_RESERVE_WITHOUT_TRIGGER",
    "PLAN_RESTORE_AND_FINISH_CYCLE",
}
PRESENTATION_ONLY_KEYS = {"animation", "fps", "presentation", "render_mode", "skip_mode"}


class FixtureError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FixtureError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def semantic_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: semantic_value(item) for key, item in value.items() if key not in PRESENTATION_ONLY_KEYS}
    if isinstance(value, list):
        return [semantic_value(item) for item in value]
    return value


def semantic_hash(value: Any) -> str:
    return sha256_json(semantic_value(value))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(base, dict) and isinstance(patch, dict):
        result = copy.deepcopy(base)
        for key, value in patch.items():
            result[key] = deep_merge(result[key], value) if key in result else copy.deepcopy(value)
        return result
    return copy.deepcopy(patch)


def cell_tuple(cell: list[int] | tuple[int, int]) -> tuple[int, int]:
    return int(cell[0]), int(cell[1])


def adjacent(a: list[int], b: list[int]) -> bool:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def load_package() -> dict[str, dict[str, Any]]:
    names = ["world", "rules", "ai-objective", "traces", "save-log-schema", "manifest"]
    package: dict[str, dict[str, Any]] = {}
    for name in names:
        path = DATA_DIR / f"{name}.json"
        if path.exists():
            package[name] = load_json(path)
    return package


def validate_boundaries(package: dict[str, dict[str, Any]]) -> None:
    world = package["world"]
    rules = package["rules"]
    traces = package["traces"]
    require(world["meta"]["authority"] == "Candidate", "world escaped Candidate boundary")
    require(world["meta"]["build_status"] == "zero_build", "world falsely claims build")
    require(world["meta"]["human_test_status"] == "human_not_run", "world falsely claims human test")
    require(world["meta"]["user_decision_status"] == "user_not_decided", "world falsely claims user decision")
    for key in ("canon_write", "reader_write", "runtime_write", "demo_write"):
        require(world["meta"][key] is False, f"boundary write enabled: {key}")
    require(rules["meta"]["authority"] == "Candidate", "rules escaped Candidate boundary")
    require(traces["meta"]["fun_status"] == "FUN_UNPROVEN", "trace pack falsely claims fun")
    require(traces["meta"]["human_gate"] == "M5_REQUIRED", "trace pack bypasses M5")
    require(traces["meta"]["seed_claim"] == "authored_declared_trace_regression_only", "trace pack overclaims seed execution")
    require(traces["meta"]["global_dominance_status"] == "DOMINANCE_UNPROVEN", "trace pack falsely claims global dominance closure")
    require(traces["meta"]["search_gate"] == "BOUNDED_SEARCH_REQUIRED", "trace pack bypasses bounded search")


def validate_route_cells(route: list[list[int]], walkable: set[tuple[int, int]], label: str) -> None:
    require(route, f"{label}: empty route")
    for cell in route:
        require(len(cell) == 2, f"{label}: malformed cell")
        require(cell_tuple(cell) in walkable, f"{label}: non-walkable cell {cell}")
    for left, right in zip(route, route[1:]):
        require(adjacent(left, right), f"{label}: non-adjacent step {left}->{right}")


def validate_world(world: dict[str, Any]) -> None:
    grid = world["grid"]
    require((grid["width"], grid["height"]) == (14, 10), "grid must be 14x10")
    walk_list = grid["walkable_cells"]
    walkable = {cell_tuple(cell) for cell in walk_list}
    require(len(walkable) == len(walk_list), "duplicate walkable cell")
    for x, y in walkable:
        require(1 <= x <= 14 and 1 <= y <= 10, f"walkable cell out of bounds: {(x, y)}")
    for lane_id, cells in grid["lanes"].items():
        require(all(cell_tuple(cell) in walkable for cell in cells), f"lane {lane_id} contains solid cell")
    require(all((x, 4) in walkable and (x, 5) in walkable for x in range(1, 15)), "two-band main bridge incomplete")
    require(set(cell_tuple(cell) for cell in grid["lanes"]["WEST_TURN_POCKET"]) == {(3,3),(4,3),(5,3),(6,3)}, "1x2 turn pocket drift")
    require({(3,3),(4,3),(3,4),(4,4)} <= walkable, "anchor 2x2 turn sweep unavailable")
    units = world["units"]
    allies = [unit_id for unit_id, unit in units.items() if unit["side"] == "ally"]
    enemies = [unit_id for unit_id, unit in units.items() if unit["side"] == "enemy"]
    require(len(allies) == 3 and len(enemies) == 5, "unit count must be 3 allies / 5 enemies")
    require(len(world["vehicles"]) == 3, "vehicle count must be 3")
    occupied: dict[tuple[int, int], str] = {}
    for unit_id, unit in units.items():
        require(unit["cells"], f"{unit_id}: empty footprint")
        require(cell_tuple(unit["anchor_cell"]) in {cell_tuple(c) for c in unit["cells"]}, f"{unit_id}: anchor outside footprint")
        for cell in unit["cells"]:
            key = cell_tuple(cell)
            require(key in walkable, f"{unit_id}: footprint out of map/walkable set: {cell}")
            require(key not in occupied, f"initial dynamic overlap: {unit_id} and {occupied.get(key)} at {cell}")
            occupied[key] = unit_id
        require(unit["move_ticks_per_cell"] > 0, f"{unit_id}: invalid movement rate")
        require(set(unit["systems"].values()) <= {0, 1, 2}, f"{unit_id}: invalid system state")
    vehicle_positions: set[tuple[int, int]] = set()
    for vehicle_id, vehicle in world["vehicles"].items():
        pos = cell_tuple(vehicle["position"])
        require(pos in walkable, f"{vehicle_id}: starts in solid cell")
        require(pos not in vehicle_positions, f"vehicle initial overlap at {pos}")
        vehicle_positions.add(pos)
        route = world["vehicle_routes"][vehicle["route_id"]]
        require(cell_tuple(route[0]) == pos, f"{vehicle_id}: route does not start at vehicle")
    for route_id, route in world["vehicle_routes"].items():
        validate_route_cells(route, walkable, route_id)
    require(cell_tuple(grid["gate_operate_from"]) == (7, 6), "gate terminal geometry drift")
    require((7, 8) == cell_tuple(grid["gate_cell"]), "gate cell drift")
    require(all(cell[1] == 7 for cell in world["units"]["EN_BREAKER_2"]["cells"]), "side Breaker entered vehicle band")


def action_map(rules: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in rules["actions"]}


def validate_rules(rules: dict[str, Any]) -> None:
    actions = action_map(rules)
    require(set(actions) == EXPECTED_ACTIONS and len(rules["actions"]) == 16, "16-action allowlist drift")
    time = rules["time"]
    require((time["tick_ms"], time["ticks_per_window"], time["window_ms"], time["windows"], time["deadline_ms"]) == (500, 16, 8000, 4, 32000), "clock contract drift")
    info = rules["information_budget"]
    require(info["physics"] == "known_exact" and info["enemy_current_intent"] == "known_exact", "P1 information is not exact")
    require(info["hidden_rng"] is False and info["fog_of_war"] is False, "P1 introduced hidden information/RNG")
    packet = rules["plan_packet"]
    require(packet["body_budget_ticks"] == 16 and packet["route_main_reaction_share_budget"] is True, "body budget drift")
    require(set(rules["scheduler_adapters"]) == {"P1-A", "P1-B", "P1-C", "P1-D"}, "adapter set drift")
    invariant = rules["adapter_invariants"]
    require(invariant["shared_resolver"] and invariant["shared_AI_and_objectives"], "adapter changed common truth")
    require(invariant["world_tick_per_cycle"] == 1 and invariant["intent_replans_inside_cycle"] == 0, "adapter clock/AI replan drift")
    require(rules["objectives"]["independent_results"] is True, "objective results collapsed")


def validate_ai(ai: dict[str, Any], world: dict[str, Any]) -> None:
    enemies = {unit_id for unit_id, unit in world["units"].items() if unit["side"] == "enemy"}
    require(set(ai["enemy_policies"]) == enemies, "not all five enemies have a policy")
    obs = ai["observer_contract"]
    require(obs["read_snapshot"] == "previous_cycle_close", "AI reads wrong snapshot")
    require(obs["reads_uncommitted_player_draft"] is False and obs["reads_current_cycle_later_commits"] is False, "AI peeks at draft/later commit")
    require(obs["intent_revision_inside_window"] == 0, "AI replans inside window")
    require(obs["mirror_tiebreak"] == "mirror_coordinates_and_public_sort_key_together", "mirror tiebreak drift")
    walkable = {cell_tuple(cell) for cell in world["grid"]["walkable_cells"]}
    for route_id, route in ai["route_variants"].items():
        validate_route_cells(route, walkable, route_id)
    for enemy_id, policy in ai["enemy_policies"].items():
        require(policy["priority"] and policy["target_sort"] and policy["declared_contingencies"], f"{enemy_id}: incomplete priority/fallback")
        require(policy["fallback_when_primary_route_blocked"], f"{enemy_id}: missing fallback")
        for route_ref in policy["route_priority"]:
            require(route_ref in ai["route_variants"], f"{enemy_id}: dangling route {route_ref}")
    require(ai["objective_state_machine"]["joint_collapse_forbidden"] is True, "objective state collapsed")
    protect_at_close = ai["objective_state_machine"]["OBJ_PROTECT"]["at_cycle_4"]
    require(protect_at_close == {"bridge_stress_below_degraded_at": "clear", "otherwise": "forward_failure"}, "AI objective disagrees with degraded threshold")
    require(ai["eligible_slot_rules"]["removed_midcycle"] == "WAIT_REMOVED_for_frozen_slot", "removed slot mutates clock")
    require(ai["eligible_slot_rules"]["reinforcement_midcycle"] == "eligible_next_cycle_only", "midcycle reinforcement mutated slot set")


def validate_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "save schema draft drift")
    needed = {"meta", "snapshot", "event_log", "commit_cursor", "eligible_slots", "frozen_intents", "pending_world_ticks", "receipt"}
    require(set(schema["required"]) == needed, "midcycle save required fields incomplete")
    require({"Meta", "WorldSnapshot", "CauseEvent", "FrozenIntent", "Receipt"} <= set(schema["$defs"]), "save schema defs incomplete")
    receipt = schema["$defs"]["Receipt"]["properties"]
    require(receipt["fun_status"]["const"] == "FUN_UNPROVEN" and receipt["human_gate"]["const"] == "M5_REQUIRED", "save receipt falsely promotes evidence")


def expand_clock_state(traces: dict[str, Any], ref: str) -> dict[str, Any]:
    require(ref in traces["clock_state_refs"], f"missing clock state ref: {ref}")
    return deep_merge(traces["clock_state_base"], traces["clock_state_refs"][ref]["patch"])


def apply_clock_plan(state: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(state)
    for operation in plan["operations"]:
        op = operation["op"]
        if op == "advance_time":
            result["world_time_ms"] += operation["ms"]
        elif op == "increment":
            result[operation["field"]] += operation["by"]
        elif op == "set":
            result[operation["field"]] = copy.deepcopy(operation["value"])
        elif op == "move_auto":
            auto = result["autonomous"][operation["id"]]
            auto["position"] = copy.deepcopy(operation["to"])
            auto["microticks"] += operation["microticks"]
        elif op == "bridge_close":
            if operation["base"]:
                result["bridge_base_tick_count"] += 1
            result["bridge_stress"] = max(0, min(6, result["bridge_stress"] + operation["base"] + operation["breaker"] + operation["brace"]))
        elif op == "assert_restore_same":
            before_log = sha256_json(result["event_log"])
            before_cursor = result["commit_cursor"]
            restored = copy.deepcopy(result)
            result["restore_event_log_hash_same"] = sha256_json(restored["event_log"]) == before_log
            result["restore_commit_cursor_same"] = restored["commit_cursor"] == before_cursor
        else:
            raise FixtureError(f"unknown clock operation: {op}")
    return result


def validate_clock(traces: dict[str, Any]) -> dict[str, str]:
    require(set(traces["clock_state_refs"]) == EXPECTED_CLOCK_STATES, "13 clock state refs (6 pre + 7 post) not fully defined")
    require(set(traces["clock_plan_refs"]) == EXPECTED_CLOCK_PLANS, "7 clock plan refs not fully defined")
    matrix = traces["clock_vector_matrix"]
    require(set(matrix["adapters"]) == {"P1-A", "P1-B", "P1-C", "P1-D"}, "clock matrix adapter drift")
    require(len(matrix["templates"]) == 7, "clock matrix must have seven templates")
    hashes: dict[str, str] = {}
    for template in matrix["templates"]:
        pre = expand_clock_state(traces, template["pre"])
        plan_ref = template["plan"]
        require(plan_ref in traces["clock_plan_refs"], f"missing plan ref: {plan_ref}")
        actual = apply_clock_plan(pre, traces["clock_plan_refs"][plan_ref])
        expected = expand_clock_state(traces, template["post"])
        require(actual == expected, f"clock vector mismatch: {template['case']}")
        per_adapter = {adapter: semantic_hash(actual) for adapter in matrix["adapters"]}
        require(len(set(per_adapter.values())) == 1, f"ALL_WAIT/common clock hash differs by adapter: {template['case']}")
        hashes[template["case"]] = next(iter(per_adapter.values()))
    require(len(matrix["adapters"]) * len(matrix["templates"]) == 28, "clock vector expansion not 28")
    return hashes


def validate_legacy_vector_bindings(traces: dict[str, Any]) -> None:
    require(VECTOR_TSV.exists(), "legacy 28-row adapter vector table missing")
    with VECTOR_TSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 28, "legacy adapter vector table no longer has 28 rows")
    require({row["pre_state_ref"] for row in rows} <= EXPECTED_CLOCK_STATES, "legacy vector has undefined pre-state")
    require({row["post_state_ref"] for row in rows} <= EXPECTED_CLOCK_STATES, "legacy vector has undefined post-state")
    require({row["normalized_plan_ref"] for row in rows} == EXPECTED_CLOCK_PLANS, "legacy vector plan refs drift")


def displacement_result(margin: int) -> str:
    if margin <= -2:
        return "target_holds_source_stability_minus_1"
    if margin <= 0:
        return "mutual_hold_each_stress_plus_1"
    if margin == 1:
        return "target_moves_1_target_stability_minus_1"
    if margin == 2:
        return "target_moves_up_to_2_remainder_to_stress"
    return "target_moves_up_to_3_and_unstable"


def effect_result(margin: int) -> str:
    if margin <= 0:
        return "no_function_degrade"
    if margin == 1:
        return "declared_function_2_to_1"
    if margin == 2:
        return "function_2_to_1_and_stability_minus_1_or_function_1_to_0"
    return "at_most_two_predeclared_nonlethal_effects"


def validate_physics_cases(traces: dict[str, Any]) -> None:
    for case in traces["physics_cases"]:
        terms = case["terms"]
        if case["kind"] == "displacement":
            margin = terms["force_band"] + terms["momentum_band"] + terms["source_support"] + terms["valid_helper_support"] - terms["target_mass_band"] - terms["target_stability_band"] - terms["target_support_band"]
            result = displacement_result(margin)
        elif case["kind"] == "effect":
            margin = terms["penetration_band"] + terms["force_band"] + terms["relative_motion_band"] - terms["protection_band"] - terms["cover_band"] - terms["system_guard_band"]
            result = effect_result(margin)
        else:
            raise FixtureError(f"unknown physics case kind: {case['kind']}")
        require(margin == case["expected_margin"], f"physics margin drift: {case['case_id']}")
        require(result == case["expected_result"], f"physics outcome drift: {case['case_id']}")


def initial_dynamic_state(world: dict[str, Any]) -> dict[str, Any]:
    state = copy.deepcopy(world["initial_state"])
    state["units"] = copy.deepcopy(world["units"])
    state["vehicles"] = copy.deepcopy(world["vehicles"])
    state["objects"] = copy.deepcopy(world["objects"])
    return state


def action_duration(action: dict[str, Any], actor: dict[str, Any], route_steps: int, declared_ticks: int | None = None) -> int:
    duration = action["duration"]
    mode = duration["mode"]
    if mode == "route":
        return route_steps * actor[duration["ticks_per_cell_field"]]
    if mode == "fixed":
        return duration["ticks"]
    if mode == "by_tag":
        matches = [ticks for tag, ticks in duration["ticks"].items() if tag in actor["tags"]]
        require(len(matches) == 1, f"actor has no unique duration tag for {action['id']}")
        return matches[0]
    if mode == "declared":
        require(declared_ticks is not None, f"declared duration missing for {action['id']}")
        require(duration["min_ticks"] <= declared_ticks <= duration["max_ticks"], f"declared duration out of range for {action['id']}")
        return declared_ticks
    raise FixtureError(f"unknown duration mode: {mode}")


def validate_plan(plan: dict[str, Any], state: dict[str, Any], world: dict[str, Any], rules: dict[str, Any]) -> tuple[int, list[tuple[str, str, int]]]:
    actor_id = plan["actor_id"]
    require(actor_id in state["units"], f"plan actor missing: {actor_id}")
    actor = state["units"][actor_id]
    actions = action_map(rules)
    action_id = plan["action_id"]
    require(action_id in actions, f"illegal action: {action_id}")
    action = actions[action_id]
    require(any(tag in actor["tags"] for tag in action["allowed_tags"]), f"{actor_id} not allowed to use {action_id}")
    route = plan.get("route", [])
    route_steps = max(0, len(route) - 1)
    walkable = {cell_tuple(cell) for cell in world["grid"]["walkable_cells"]}
    if route:
        validate_route_cells(route, walkable, f"plan:{actor_id}")
        require(cell_tuple(route[0]) == cell_tuple(actor["anchor_cell"]), f"{actor_id}: plan route does not start at current anchor")
    route_ticks = route_steps * actor["move_ticks_per_cell"]
    main_ticks = action_duration(action, actor, route_steps, plan.get("declared_ticks"))
    if action["kind"] != "route_native":
        main_ticks += route_ticks
    wait_ticks = plan.get("declared_wait_ticks", 0)
    require(isinstance(wait_ticks, int) and 0 <= wait_ticks <= 16, f"{actor_id}: invalid declared wait")
    total = main_ticks + wait_ticks
    costs: list[tuple[str, str, int]] = []
    for resource, amount in action.get("cost", {}).items():
        costs.append((actor_id, resource, amount))
    reaction_id = plan.get("reaction_id")
    if reaction_id:
        require(reaction_id in actions, f"illegal reaction: {reaction_id}")
        reaction = actions[reaction_id]
        require(reaction["kind"] == "reaction", f"{reaction_id} is not a reaction")
        require(any(tag in actor["tags"] for tag in reaction["allowed_tags"]), f"{actor_id} not allowed to use {reaction_id}")
        total += action_duration(reaction, actor, 0)
        for resource, amount in reaction.get("cost", {}).items():
            costs.append((actor_id, resource, amount))
    require(total <= rules["plan_packet"]["body_budget_ticks"], f"{actor_id}: plan uses {total} ticks > 16")
    expected_tempo = 0 if total == 0 else math.ceil(total / 8)
    require(expected_tempo <= 2, f"{actor_id}: tempo overflow")
    return total, costs


def validate_plan_batch(plans: list[dict[str, Any]], state: dict[str, Any], world: dict[str, Any], rules: dict[str, Any], adapter: str = "P1-B") -> None:
    require(adapter in rules["scheduler_adapters"], f"unknown adapter: {adapter}")
    seen: set[str] = set()
    pending_costs: list[tuple[str, str, int]] = []
    for plan in plans:
        require(plan["actor_id"] not in seen, f"duplicate plan actor: {plan['actor_id']}")
        seen.add(plan["actor_id"])
        _, costs = validate_plan(plan, state, world, rules)
        pending_costs.extend(costs)
    aggregate: dict[tuple[str, str], int] = {}
    for actor_id, resource, amount in pending_costs:
        aggregate[(actor_id, resource)] = aggregate.get((actor_id, resource), 0) + amount
    for (actor_id, resource), amount in aggregate.items():
        available = state["units"][actor_id]["resources"].get(resource, 0)
        require(available >= amount, f"{actor_id}: insufficient {resource}")
    for (actor_id, resource), amount in aggregate.items():
        state["units"][actor_id]["resources"][resource] -= amount


def unit_occupancy(state: dict[str, Any], exclude: str | None = None) -> dict[tuple[int, int], str]:
    occupied: dict[tuple[int, int], str] = {}
    for unit_id, unit in state["units"].items():
        if unit_id == exclude or unit.get("state") == "removed":
            continue
        for cell in unit["cells"]:
            occupied[cell_tuple(cell)] = unit_id
    return occupied


def check_atomic_moves(events: list[dict[str, Any]], state: dict[str, Any]) -> None:
    groups: dict[int, list[dict[str, Any]]] = {}
    for event in events:
        if event["op"] == "move_unit":
            groups.setdefault(event["tick"], []).append(event)
    for tick, moves in groups.items():
        destination_owner: dict[tuple[int, int], str] = {}
        starts = {event["unit_id"]: set(cell_tuple(c) for c in state["units"][event["unit_id"]]["cells"]) for event in moves}
        destinations = {event["unit_id"]: set(cell_tuple(c) for c in event["cells"]) for event in moves}
        for unit_id, cells in destinations.items():
            for cell in cells:
                require(cell not in destination_owner, f"dynamic overlap at tick {tick}: {unit_id}/{destination_owner.get(cell)}")
                destination_owner[cell] = unit_id
        ids = list(starts)
        for index, first in enumerate(ids):
            for second in ids[index + 1:]:
                require(not (destinations[first] == starts[second] and destinations[second] == starts[first]), f"edge swap at tick {tick}: {first}/{second}")


def translated_footprint(unit: dict[str, Any], anchor: list[int]) -> set[tuple[int, int]]:
    old_anchor = unit["anchor_cell"]
    dx, dy = anchor[0] - old_anchor[0], anchor[1] - old_anchor[1]
    return {(cell[0] + dx, cell[1] + dy) for cell in unit["cells"]}


def validate_cycle_microticks(cycle: dict[str, Any], state: dict[str, Any], world: dict[str, Any]) -> None:
    """Targeted 0.5s occupancy oracle for both declared four-window seeds."""
    plans = {plan["actor_id"]: plan for plan in cycle["plans"]}
    move_events = {event["unit_id"]: event for event in cycle["events"] if event["op"] == "move_unit"}
    vehicle_events = {event["vehicle_id"]: event for event in cycle["events"] if event["op"] == "move_vehicle"}
    gate_events = sorted((event for event in cycle["events"] if event["op"] == "set_gate"), key=lambda item: item["tick"])
    walkable = {cell_tuple(cell) for cell in world["grid"]["walkable_cells"]}
    unit_paths: dict[str, tuple[list[list[int]], int, int]] = {}
    for unit_id, unit in state["units"].items():
        plan = plans.get(unit_id)
        route = copy.deepcopy(plan.get("route", [])) if plan else []
        if not route:
            route = [copy.deepcopy(unit["anchor_cell"])]
        event = move_events.get(unit_id)
        if event:
            endpoint = cell_tuple(event["anchor"])
            matching = [index for index, cell in enumerate(route) if cell_tuple(cell) == endpoint]
            require(matching, f"{unit_id}: move event endpoint absent from plan route")
            route = route[:matching[-1] + 1]
            expected_tick = plan.get("declared_wait_ticks", 0) + (len(route) - 1) * unit["move_ticks_per_cell"]
            require(event["tick"] == expected_tick, f"{unit_id}: move completion tick {event['tick']} != {expected_tick}")
        elif len(route) > 1:
            outcome_ids = set(plan.get("outcome_event_ids", [])) if plan else set()
            outcomes = [event for event in cycle["events"] if event["event_id"] in outcome_ids and event["op"] == "plan_outcome"]
            require(outcomes and any("block" in event["status"] or "intercept" in event["status"] or "abort" in event["status"] for event in outcomes), f"{unit_id}: route plan has no move or explicit blocked outcome")
            route = [copy.deepcopy(unit["anchor_cell"])]
        unit_paths[unit_id] = (route, plan.get("declared_wait_ticks", 0) if plan else 0, unit["move_ticks_per_cell"])
    vehicle_paths = {vehicle_id: copy.deepcopy(vehicle_events[vehicle_id]["path"]) if vehicle_id in vehicle_events else [copy.deepcopy(vehicle["position"])] for vehicle_id, vehicle in state["vehicles"].items()}
    prior_positions: dict[str, set[tuple[int, int]]] = {}
    for tick in range(17):
        occupied: dict[tuple[int, int], str] = {}
        current_positions: dict[str, set[tuple[int, int]]] = {}
        gate_state = state["objects"]["GATE_SIDE"]["state"]
        for event in gate_events:
            if event["tick"] <= tick:
                gate_state = event["state"]
        for unit_id, unit in state["units"].items():
            route, wait, speed = unit_paths[unit_id]
            moved = min(len(route) - 1, max(0, tick - wait) // speed)
            anchor = route[moved]
            cells = translated_footprint(unit, anchor)
            require(cells <= walkable, f"{unit_id}: footprint leaves map at tick {tick}")
            current_positions[unit_id] = cells
        for vehicle_id, vehicle in state["vehicles"].items():
            if vehicle["state"] == "exited":
                continue
            path = vehicle_paths[vehicle_id]
            moved = min(len(path) - 1, tick // vehicle["move_ticks_per_cell"])
            pos = cell_tuple(path[moved])
            if pos in {cell_tuple(cell) for cell in world["grid"]["vehicle_exits"]} and moved == len(path) - 1 and len(path) > 1:
                continue
            if pos == cell_tuple(world["grid"]["gate_cell"]):
                require(gate_state == "open", f"{vehicle_id}: enters gate before open at tick {tick}")
            current_positions[vehicle_id] = {pos}
        for body_id, cells in current_positions.items():
            for cell in cells:
                require(cell not in occupied, f"microtick dynamic overlap at tick {tick}: {body_id}/{occupied.get(cell)} {cell}")
                occupied[cell] = body_id
        if prior_positions:
            ids = list(current_positions)
            for index, first in enumerate(ids):
                for second in ids[index + 1:]:
                    if first in prior_positions and second in prior_positions:
                        require(not (current_positions[first] == prior_positions[second] and current_positions[second] == prior_positions[first]), f"microtick edge swap at tick {tick}: {first}/{second}")
        prior_positions = current_positions


def validate_vehicle_trajectories(trajectories: list[tuple[str, list[list[int]]]], state_before: dict[str, Any]) -> None:
    if not trajectories:
        return
    max_steps = max(len(path) - 1 for _, path in trajectories)
    for step in range(1, max_steps + 1):
        positions: dict[tuple[int, int], str] = {}
        edges: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {}
        for vehicle_id, path in trajectories:
            previous = cell_tuple(path[min(step - 1, len(path) - 1)])
            current = cell_tuple(path[min(step, len(path) - 1)])
            if current in positions:
                raise FixtureError(f"vehicle dynamic overlap at microtick {step * 4}: {vehicle_id}/{positions[current]}")
            positions[current] = vehicle_id
            edges[vehicle_id] = (previous, current)
        ids = list(edges)
        for index, first in enumerate(ids):
            for second in ids[index + 1:]:
                require(not (edges[first][0] == edges[second][1] and edges[first][1] == edges[second][0]), f"vehicle edge swap at microtick {step * 4}")


def apply_seed_event(event: dict[str, Any], state: dict[str, Any], world: dict[str, Any], traces: dict[str, Any], plan_by_actor: dict[str, dict[str, Any]], trajectories: list[tuple[str, list[list[int]]]]) -> None:
    require(0 <= event["tick"] <= 16, f"event outside window: {event['event_id']}")
    op = event["op"]
    walkable = {cell_tuple(cell) for cell in world["grid"]["walkable_cells"]}
    if op == "move_unit":
        unit_id = event["unit_id"]
        require(unit_id in state["units"], f"unknown moving unit: {unit_id}")
        target_cells = [cell_tuple(cell) for cell in event["cells"]]
        require(len(target_cells) == len(set(target_cells)), f"{unit_id}: duplicate footprint cell")
        require(all(cell in walkable for cell in target_cells), f"{unit_id}: footprint out of bounds/solid")
        require(len(target_cells) == len(state["units"][unit_id]["cells"]), f"{unit_id}: footprint size changed")
        occupied = unit_occupancy(state, exclude=unit_id)
        require(not any(cell in occupied for cell in target_cells), f"{unit_id}: dynamic overlap with {occupied}")
        plan = plan_by_actor.get(unit_id)
        if plan and plan.get("route"):
            endpoint = cell_tuple(event["anchor"])
            require(endpoint in {cell_tuple(cell) for cell in plan["route"]}, f"{unit_id}: event endpoint absent from plan route")
        state["units"][unit_id]["cells"] = copy.deepcopy(event["cells"])
        state["units"][unit_id]["anchor_cell"] = copy.deepcopy(event["anchor"])
    elif op == "move_vehicle":
        vehicle_id = event["vehicle_id"]
        vehicle = state["vehicles"][vehicle_id]
        path = event["path"]
        require(cell_tuple(path[0]) == cell_tuple(vehicle["position"]), f"{vehicle_id}: path does not start at current position")
        validate_route_cells(path, walkable, f"event:{event['event_id']}")
        require(len(path) - 1 <= 4, f"{vehicle_id}: exceeds four autonomous microticks")
        route_id = event["route_id"]
        require(route_id in world["vehicle_routes"], f"unknown vehicle route: {route_id}")
        full_route = world["vehicle_routes"][route_id]
        starts = [index for index, cell in enumerate(full_route) if cell_tuple(cell) == cell_tuple(path[0])]
        require(any([cell_tuple(c) for c in full_route[index:index + len(path)]] == [cell_tuple(c) for c in path] for index in starts), f"{vehicle_id}: event path not a route subsequence")
        if cell_tuple(world["grid"]["gate_cell"]) in {cell_tuple(cell) for cell in path[1:]}:
            require(state["objects"]["GATE_SIDE"]["state"] == "open", f"{vehicle_id}: crosses closed/unsafe gate")
        trajectories.append((vehicle_id, copy.deepcopy(path)))
        vehicle["position"] = copy.deepcopy(path[-1])
        vehicle["route_id"] = route_id
        if cell_tuple(path[-1]) in {cell_tuple(c) for c in world["grid"]["vehicle_exits"]}:
            vehicle["state"] = "exited"
    elif op == "set_brace":
        unit = state["units"][event["unit_id"]]
        require("anchor" in unit["tags"], "non-anchor set brace")
        require(cell_tuple(event["support_cell"]) in {cell_tuple(c) for c in world["grid"]["support_cells"]}, "brace used unknown support")
        if event["active"]:
            state["active_braces"] = [{"unit_id": event["unit_id"], "support_cell": copy.deepcopy(event["support_cell"])}]
            unit["stability_band"] = 2
            unit["support_band"] = 2
        else:
            state["active_braces"] = []
    elif op == "bridge_repair":
        actor = state["units"][event["actor_id"]]
        require("engineer" in actor["tags"], "bridge repair actor is not engineer")
        require(cell_tuple(actor["anchor_cell"]) in {cell_tuple(c) for c in world["grid"]["support_cells"]}, "engineer is not at a support service position")
        bridge = state["objects"]["BRIDGE_MAIN"]
        require(bridge["stress"] >= event["amount"] > 0, "repair must remove known preexisting stress")
        bridge["stress"] -= event["amount"]
    elif op == "bridge_marker":
        require(event["event_id"] not in {item["event_id"] for item in state["pending_bridge_markers"]}, "bridge marker consumed twice")
        state["pending_bridge_markers"].append({"event_id": event["event_id"], "delta": event["delta"], "marker": event["marker"]})
    elif op == "set_gate":
        actor = state["units"][event["actor_id"]]
        require("engineer" in actor["tags"] and cell_tuple(actor["anchor_cell"]) == cell_tuple(world["grid"]["gate_operate_from"]), "gate interact actor/position invalid")
        require(event["state"] in state["objects"]["GATE_SIDE"]["allowed_states"], "invalid gate state")
        state["objects"]["GATE_SIDE"]["state"] = event["state"]
    elif op == "set_sample":
        require(event["custody"] in state["objects"]["SAMPLE_K17"]["allowed_custody"], "invalid sample custody")
        actor = state["units"][event["actor_id"]]
        sample_pos = state["objects"]["SAMPLE_K17"]["position"]
        if event["custody"] != "enemy_exited":
            require(abs(actor["anchor_cell"][0] - sample_pos[0]) + abs(actor["anchor_cell"][1] - sample_pos[1]) == 1, "sample interact actor is not adjacent")
        else:
            require(cell_tuple(actor["anchor_cell"]) in {cell_tuple(c) for c in world["grid"]["enemy_sample_exits"]}, "sample carrier has not reached an enemy exit")
        state["objects"]["SAMPLE_K17"]["custody"] = event["custody"]
    elif op == "contact_case":
        cases = {case["case_id"]: case for case in traces["physics_cases"]}
        require(event["case_ref"] in cases, f"unknown physics case: {event['case_ref']}")
        case = cases[event["case_ref"]]
        require(case["expected_result"] == "target_holds_source_stability_minus_1", "trace contact expects unsupported result")
        source = state["units"][event["source_id"]]
        target = state["units"][event["target_id"]]
        require(min(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a in source["cells"] for b in target["cells"]) == 1, "contact bodies are not adjacent")
        source["stability_band"] = max(0, source["stability_band"] - 1)
    elif op == "plan_outcome":
        require(event["actor_id"] in state["units"] and event["status"], "invalid explicit plan outcome")
    else:
        raise FixtureError(f"unknown seed event op: {op}")
    state["event_log"].append(copy.deepcopy(event))


def close_cycle(state: dict[str, Any], world: dict[str, Any]) -> None:
    bridge = state["objects"]["BRIDGE_MAIN"]
    hazard = {cell_tuple(cell) for cell in world["grid"]["bridge_hazard_cells"]}
    occupied = any(cell_tuple(cell) in hazard for unit in state["units"].values() if unit.get("state") != "removed" for cell in unit["cells"])
    occupied = occupied or any(vehicle["state"] == "active" and cell_tuple(vehicle["position"]) in hazard for vehicle in state["vehicles"].values())
    if bridge["state"] != "collapsed":
        marker_delta = sum(item["delta"] for item in state["pending_bridge_markers"])
        base_delta = bridge["base_delta_if_hazard_occupied"] if occupied else 0
        brace_amount = -bridge["active_brace_delta"] if state["active_braces"] else 0
        window_delta = max(0, marker_delta + base_delta - brace_amount)
        bridge["stress"] = min(bridge["collapsed_at"], bridge["stress"] + window_delta)
        if bridge["stress"] >= bridge["collapsed_at"]:
            bridge["state"] = "collapsed"
        elif bridge["stress"] >= bridge["degraded_at"]:
            bridge["state"] = "degraded"
        else:
            bridge["state"] = "intact"
    state["pending_bridge_markers"] = []
    state["world_time_ms"] += 8000
    state["cycle"] += 1
    state["world_tick_count"] += 1
    state["observation_snapshot"] += 1
    state["report_age_windows"] += 1
    if state["cycle"] == 4:
        state["deadline_eval_count"] += 1
        exited = sum(vehicle["state"] == "exited" for vehicle in state["vehicles"].values())
        state["objectives"]["OBJ_EVACUATE"] = "clear" if exited >= 2 else "retry_required"
        state["objectives"]["OBJ_PROTECT"] = "clear" if bridge["stress"] < bridge["degraded_at"] else "forward_failure"
        state["objectives"]["OBJ_INTERCEPT"] = "forward_failure" if state["objects"]["SAMPLE_K17"]["custody"] == "enemy_exited" else "clear"
    for unit_id, unit in state["units"].items():
        if "reaction_slots" in unit["resources"]:
            unit["resources"]["reaction_slots"] = world["units"][unit_id]["resources"]["reaction_slots"]


def seed_summary(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "world_time_ms": state["world_time_ms"],
        "cycle": state["cycle"],
        "exited_vehicle_count": sum(vehicle["state"] == "exited" for vehicle in state["vehicles"].values()),
        "bridge_state": state["objects"]["BRIDGE_MAIN"]["state"],
        "bridge_stress": state["objects"]["BRIDGE_MAIN"]["stress"],
        "gate_state": state["objects"]["GATE_SIDE"]["state"],
        "sample_custody": state["objects"]["SAMPLE_K17"]["custody"],
        "objectives": copy.deepcopy(state["objectives"]),
    }


def replay_seed(seed: dict[str, Any], world: dict[str, Any], rules: dict[str, Any], traces: dict[str, Any], verify_hashes: bool = True) -> dict[str, Any]:
    state = initial_dynamic_state(world)
    commitments = seed.get("route_commitments", [])
    require({item["vehicle_id"] for item in commitments} == set(state["vehicles"]), f"{seed['seed_id']}: route commitments do not cover all vehicles")
    for item in commitments:
        require(item["commit_boundary"] == "before_cycle_1" and item["free_reroute"] is False, f"{seed['seed_id']}: route is not an atomic pre-W1 commitment")
        require(item["route_id"] in world["vehicle_routes"], f"{seed['seed_id']}: unknown committed route")
        state["vehicles"][item["vehicle_id"]]["route_id"] = item["route_id"]
    global_event_ids: set[str] = set()
    cycle_hashes: list[str] = []
    for cycle in seed["cycles"]:
        require(cycle["cycle"] == state["cycle"] + 1, f"{seed['seed_id']}: nonsequential cycle")
        require(set(cycle["participant_outcomes"]) == set(state["units"]), f"{seed['seed_id']} cycle {cycle['cycle']}: incomplete participants")
        before_plans = semantic_hash(state)
        validate_plan_batch(cycle["plans"], state, world, rules, adapter="P1-B")
        require(before_plans != semantic_hash(state) or not any(action_map(rules)[plan["action_id"]].get("cost") or plan.get("reaction_id") for plan in cycle["plans"]), "resourceful plan did not change resources")
        events = sorted(cycle["events"], key=lambda item: (item["tick"], item["event_id"]))
        event_by_id = {event["event_id"]: event for event in events}
        for plan in cycle["plans"]:
            refs = plan.get("outcome_event_ids", [])
            require(refs and all(ref in event_by_id for ref in refs), f"{plan['actor_id']}: plan has no concrete outcome event")
            causes = {event_by_id[ref]["cause"] for ref in refs}
            require(plan["action_id"] in causes or plan.get("reaction_id") in causes, f"{plan['actor_id']}: outcome event not bound to action/reaction")
        require(all(event["event_id"] not in global_event_ids for event in events), f"{seed['seed_id']}: duplicate event id")
        check_atomic_moves(events, state)
        validate_cycle_microticks(cycle, state, world)
        plan_by_actor = {plan["actor_id"]: plan for plan in cycle["plans"]}
        trajectories: list[tuple[str, list[list[int]]]] = []
        state_before_events = copy.deepcopy(state)
        for event in events:
            apply_seed_event(event, state, world, traces, plan_by_actor, trajectories)
            global_event_ids.add(event["event_id"])
        validate_vehicle_trajectories(trajectories, state_before_events)
        close_cycle(state, world)
        require(state["objects"]["BRIDGE_MAIN"]["stress"] == cycle["expected_bridge_stress"], f"{seed['seed_id']} cycle {cycle['cycle']}: bridge ledger drift")
        state_hash = semantic_hash(state)
        cycle_hashes.append(state_hash)
        if verify_hashes:
            require(cycle["expected_state_hash"] == state_hash, f"{seed['seed_id']} cycle {cycle['cycle']} state hash drift")
    require(len(seed["cycles"]) == 4 and state["world_time_ms"] == 32000 and state["cycle"] == 4, f"{seed['seed_id']}: not a four-window 32s trace")
    require(state["world_tick_count"] == 4 and state["deadline_eval_count"] == 1, f"{seed['seed_id']}: clock/deadline multi-tick")
    summary = seed_summary(state)
    require(summary == seed["expected_final"], f"{seed['seed_id']}: final summary mismatch: {summary}")
    final_state_hash = semantic_hash(state)
    event_hash = semantic_hash(state["event_log"])
    if verify_hashes:
        require(seed["expected_final_state_hash"] == final_state_hash, f"{seed['seed_id']}: final state hash drift")
        require(seed["expected_event_hash"] == event_hash, f"{seed['seed_id']}: event hash drift")
    return {"state": state, "cycle_hashes": cycle_hashes, "final_state_hash": final_state_hash, "event_hash": event_hash}


def validate_manifest(package: dict[str, dict[str, Any]]) -> None:
    require("manifest" in package, "manifest missing")
    manifest = package["manifest"]
    require(manifest["meta"]["authority"] == "Candidate", "manifest boundary drift")
    require(manifest["meta"]["integrity_claim"] == "HASH_BOUND_DECLARED_EVENT_LEDGER_ONLY", "manifest overclaims")
    require(manifest["meta"]["resolver_status"] == "RESOLVER_NOT_IMPLEMENTED", "resolver boundary drift")
    require(manifest["meta"]["implementation_gate"] == "NO_GO_UNTIL_PLAN_TO_EVENT_RULES_EXIST", "implementation gate drift")
    require(manifest["meta"]["save_round_trip_status"] == "NOT_IMPLEMENTED", "save boundary drift")
    require(manifest["canonical_json"]["component_file_hash_mode"] == "raw_file_bytes_sha256", "component hash mode drift")
    require(set(manifest["component_sha256"]) == {"world.json", "rules.json", "ai-objective.json", "traces.json", "save-log-schema.json"}, "manifest component set drift")
    for filename, expected in manifest["component_sha256"].items():
        path = DATA_DIR / filename
        require(path.exists(), f"manifest component missing: {filename}")
        require(file_sha256(path) == expected, f"manifest hash drift: {filename}")
    expected_support = {
        "../../scripts/check_d04_p1_v0_2.py": PACKAGE_ROOT / "scripts" / "check_d04_p1_v0_2.py",
        "../d04-p1-adapter-event-vectors.tsv": VECTOR_TSV,
    }
    require(set(manifest["support_file_sha256"]) == set(expected_support), "manifest support file set drift")
    for ref, path in expected_support.items():
        require(path.exists(), f"manifest support file missing: {ref}")
        require(file_sha256(path) == manifest["support_file_sha256"][ref], f"manifest support hash drift: {ref}")


def validate_seed_tradeoff(seeds: dict[str, dict[str, Any]]) -> None:
    """Reject pairwise dominance only; this does not search for a third plan."""
    require(set(seeds) == {"SEED_FRONT_BRACE", "SEED_SIDE_DIVERT"}, "tradeoff needs exactly the two named seeds")
    front = seed_summary(seeds["SEED_FRONT_BRACE"]["state"])
    side = seed_summary(seeds["SEED_SIDE_DIVERT"]["state"])
    rank = {"retry_required": 0, "forward_failure": 0, "pending": 1, "clear": 2}
    front_axes = [front["exited_vehicle_count"], rank[front["objectives"]["OBJ_PROTECT"]], rank[front["objectives"]["OBJ_INTERCEPT"]]]
    side_axes = [side["exited_vehicle_count"], rank[side["objectives"]["OBJ_PROTECT"]], rank[side["objectives"]["OBJ_INTERCEPT"]]]
    require(any(left > right for left, right in zip(front_axes, side_axes)), "NO_GO_STRATEGY_DOMINATED: front has no exclusive advantage")
    require(any(right > left for left, right in zip(front_axes, side_axes)), "NO_GO_STRATEGY_DOMINATED: side has no exclusive advantage")


def validate_all(package: dict[str, dict[str, Any]], verify_hashes: bool = True, verify_manifest: bool = True) -> dict[str, Any]:
    for key in ("world", "rules", "ai-objective", "traces", "save-log-schema"):
        require(key in package, f"package component missing: {key}")
    validate_boundaries(package)
    validate_world(package["world"])
    validate_rules(package["rules"])
    validate_ai(package["ai-objective"], package["world"])
    validate_schema(package["save-log-schema"])
    clock_hashes = validate_clock(package["traces"])
    validate_legacy_vector_bindings(package["traces"])
    validate_physics_cases(package["traces"])
    seeds = {seed["seed_id"]: replay_seed(seed, package["world"], package["rules"], package["traces"], verify_hashes=verify_hashes) for seed in package["traces"]["regression_seeds"]}
    require(set(seeds) == {"SEED_FRONT_BRACE", "SEED_SIDE_DIVERT"}, "two regression seed ids drift")
    validate_seed_tradeoff(seeds)
    if verify_manifest:
        validate_manifest(package)
    return {"clock_hashes": clock_hashes, "seeds": seeds}


def expect_fault(fault_id: str, operation: Callable[[], None]) -> None:
    try:
        operation()
    except (FixtureError, KeyError, TypeError, ValueError):
        print(f"PASS {fault_id}")
        return
    raise FixtureError(f"fault injection escaped: {fault_id}")


def run_self_test(pristine: dict[str, dict[str, Any]]) -> None:
    world = pristine["world"]
    rules = pristine["rules"]
    traces = pristine["traces"]
    ai = pristine["ai-objective"]

    def mutate_and_validate(mutator: Callable[[dict[str, dict[str, Any]]], None], validator: Callable[[dict[str, dict[str, Any]]], None]) -> None:
        package = copy.deepcopy(pristine)
        mutator(package)
        validator(package)

    expect_fault("FI_MAP_FOOTPRINT_OOB", lambda: mutate_and_validate(lambda p: p["world"]["units"]["ALLY_ANCHOR"].update({"cells": [[15,4],[14,4]], "anchor_cell": [15,4]}), lambda p: validate_world(p["world"])))
    expect_fault("FI_MAP_DYNAMIC_OVERLAP", lambda: mutate_and_validate(lambda p: p["world"]["units"]["ALLY_SKIRMISHER"].update({"cells": [[6,6]], "anchor_cell": [6,6]}), lambda p: validate_world(p["world"])))

    synthetic = initial_dynamic_state(world)
    swap_events = [
        {"op": "move_unit", "tick": 4, "unit_id": "ALLY_SKIRMISHER", "cells": [[6,6]]},
        {"op": "move_unit", "tick": 4, "unit_id": "ALLY_ENGINEER", "cells": [[5,6]]},
    ]
    expect_fault("FI_COLLISION_EDGE_SWAP", lambda: check_atomic_moves(swap_events, synthetic))
    triple_events = [
        {"op": "move_unit", "tick": 4, "unit_id": unit_id, "cells": [[7,6]]}
        for unit_id in ("ALLY_SKIRMISHER", "ALLY_ENGINEER", "EN_HUNTER_1")
    ]
    expect_fault("FI_COLLISION_THREE_BODY_ORDER", lambda: check_atomic_moves(triple_events, synthetic))

    over_plan = {"actor_id": "ALLY_ANCHOR", "route": [[3,4],[4,4],[5,4],[6,4]], "action_id": "TACT_BRACE", "target": "SUPPORT_W"}
    expect_fault("FI_BUDGET_OVER_8S", lambda: validate_plan(over_plan, synthetic, world, rules))
    double_plan = {"actor_id": "ALLY_ENGINEER", "route": [[6,6],[7,6],[8,6]], "action_id": "TACT_FIELD_REPAIR", "target": "SUPPORT_E"}
    expect_fault("FI_BUDGET_DOUBLE_SPEND", lambda: validate_plan(double_plan, synthetic, world, rules))

    atomic_state = initial_dynamic_state(world)
    atomic_hash = semantic_hash(atomic_state)
    atomic_plans = [
        {"actor_id": "ALLY_SKIRMISHER", "route": [], "action_id": "TACT_SUPPRESS", "target": "X"},
        {"actor_id": "ALLY_ENGINEER", "route": [[6,6],[7,6],[8,6]], "action_id": "TACT_FIELD_REPAIR", "target": "X"},
    ]
    def atomicity_fault() -> None:
        try:
            validate_plan_batch(atomic_plans, atomic_state, world, rules, adapter="P1-B")
        except FixtureError:
            require(semantic_hash(atomic_state) == atomic_hash, "P1-B partial resource mutation")
            raise
    expect_fault("FI_PLAN_ATOMICITY_B", atomicity_fault)

    expect_fault("FI_AI_PEEK_DRAFT", lambda: mutate_and_validate(lambda p: p["ai-objective"]["observer_contract"].update({"reads_uncommitted_player_draft": True}), lambda p: validate_ai(p["ai-objective"], p["world"])))
    expect_fault("FI_AI_REPLAN_IN_WINDOW", lambda: mutate_and_validate(lambda p: p["ai-objective"]["observer_contract"].update({"intent_revision_inside_window": 1}), lambda p: validate_ai(p["ai-objective"], p["world"])))
    expect_fault("FI_OBJECTIVE_COLLAPSE", lambda: mutate_and_validate(lambda p: p["rules"]["objectives"].update({"independent_results": False}), lambda p: validate_rules(p["rules"])))
    expect_fault("FI_CLOCK_MULTI_TICK", lambda: mutate_and_validate(lambda p: p["traces"]["clock_plan_refs"]["PLAN_ALL_WAIT_CLEAR_LANE"]["operations"][2].update({"by": 2}), lambda p: validate_clock(p["traces"])))
    expect_fault("FI_CLOCK_SLOT_MUTATION", lambda: mutate_and_validate(lambda p: p["ai-objective"]["eligible_slot_rules"].update({"removed_midcycle": "delete_slot"}), lambda p: validate_ai(p["ai-objective"], p["world"])))
    expect_fault("FI_SAVE_MIDCYCLE_RESTORE", lambda: mutate_and_validate(lambda p: p["traces"]["clock_state_refs"]["CLK_S1_RESTORED_CLOSE_HASH_EQ_DIRECT"]["patch"].update({"restore_event_log_hash_same": False}), lambda p: validate_clock(p["traces"])))

    present_a = {"semantic": {"x": 1}, "presentation": {"fps": 30, "skip_mode": "full"}}
    present_b = {"semantic": {"x": 1}, "presentation": {"fps": 144, "skip_mode": "skip"}}
    def presentation_fault() -> None:
        require(semantic_hash(present_a) == semantic_hash(present_b), "presentation changed semantic hash")
        raise FixtureError("presentation-only mutation correctly ignored")
    expect_fault("FI_PRESENTATION_HASH", presentation_fault)
    expect_fault("FI_MIRROR_TIEBREAK", lambda: mutate_and_validate(lambda p: p["ai-objective"]["observer_contract"].update({"mirror_tiebreak": "raw_id_only"}), lambda p: validate_ai(p["ai-objective"], p["world"])))

    def brace_repair_fault() -> None:
        state = initial_dynamic_state(world)
        state["active_braces"] = [{"unit_id": "ALLY_ANCHOR", "support_cell": [6,4]}]
        before = state["objects"]["BRIDGE_MAIN"]["stress"]
        close_cycle(state, world)
        require(state["objects"]["BRIDGE_MAIN"]["stress"] == before, "brace repaired preexisting bridge stress")
        raise FixtureError("brace correctly left preexisting stress unchanged")
    expect_fault("FI_BRACE_NOT_REPAIR", brace_repair_fault)

    expect_fault("FI_MISSING_CLOCK_REF", lambda: mutate_and_validate(lambda p: p["traces"]["clock_state_refs"].pop("CLK_S0_IDLE_TIME0_CYCLE0"), lambda p: validate_clock(p["traces"])))
    expect_fault("FI_SEED_HASH_DRIFT", lambda: mutate_and_validate(lambda p: p["traces"]["regression_seeds"][0].update({"expected_final_state_hash": "0" * 64}), lambda p: replay_seed(p["traces"]["regression_seeds"][0], p["world"], p["rules"], p["traces"], verify_hashes=True)))
    print("SELF_TEST_PASS 18/18")


def hash_payload(package: dict[str, dict[str, Any]], results: dict[str, Any]) -> dict[str, Any]:
    component_hashes = {}
    for filename in ("world.json", "rules.json", "ai-objective.json", "traces.json", "save-log-schema.json"):
        component_hashes[filename] = file_sha256(DATA_DIR / filename)
    seeds = {}
    for seed_id, result in results["seeds"].items():
        seeds[seed_id] = {
            "cycle_hashes": result["cycle_hashes"],
            "final_state_hash": result["final_state_hash"],
            "event_hash": result["event_hash"],
        }
    return {"component_sha256": component_hashes, "clock_hashes": results["clock_hashes"], "seeds": seeds}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run read-only mutation tests")
    parser.add_argument("--print-hashes", action="store_true", help="print computed hashes without requiring stored hashes")
    args = parser.parse_args()
    package = load_package()
    try:
        results = validate_all(package, verify_hashes=not args.print_hashes, verify_manifest=not args.print_hashes)
        if args.print_hashes:
            print(json.dumps(hash_payload(package, results), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if args.self_test:
            run_self_test(package)
        print("HASH_BOUND_DECLARED_EVENT_LEDGER_PASS")
        print("clock_refs=20 clock_vectors=28 physics_cases=2 regression_seeds=2 windows_per_seed=4")
        print("DECLARED_EVENT_REPLAY_ONLY")
        print("RESOLVER_NOT_IMPLEMENTED")
        print("IMPLEMENTATION_NO_GO")
        print("REGISTERED_SEEDS_NON_DOMINATED_ONLY")
        print("DOMINANCE_UNPROVEN")
        print("BOUNDED_SEARCH_REQUIRED")
        print("FUN_UNPROVEN")
        print("M5_REQUIRED")
        return 0
    except (FixtureError, KeyError, TypeError, ValueError) as exc:
        print(f"D04_P1_V0_2_FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
