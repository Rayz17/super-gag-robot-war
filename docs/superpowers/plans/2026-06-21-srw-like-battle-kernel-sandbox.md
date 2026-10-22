# SRW-like Battle Kernel Sandbox Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a tested Godot battle-kernel sandbox for 《超GAG机器人大战》 that proves SRW-like action flow, enemy intent, combat forecast, scenario events, and the exploration-to-battle data bridge before migrating the full Chapter 01 demo.

**Architecture:** Keep the existing `game-godot` project and add a focused `scripts/core/` runtime beside the current prototype files. The new kernel owns rules and data flow; the existing `demo_v03_model.gd` and `main.gd` remain playable reference material until the sandbox passes, then later plans can migrate the Chapter 01 presentation onto the new kernel.

**Tech Stack:** Godot 4.7, GDScript `RefCounted` core objects, headless Godot smoke tests, existing `scripts/godot-test.sh`, optional native Godot visual sandbox scene.

---

## Scope Check

The interaction spec covers several subsystems: battle state machine, scenario events, exploration scenes, content data, UI layout, and full first-chapter content. This plan implements the first testable slice only:

- P0 battle kernel.
- P1 scenario event bridge.
- One small visual sandbox.
- Test runner integration.

This plan does not migrate all Chapter 01 content or replace `game-godot/scripts/main.gd` as the default scene. That migration should be a follow-up plan once this kernel is verified.

---

## Existing Context

Read these files before implementing:

- `docs/superpowers/specs/2026-06-21-srw-like-gameplay-interaction-spec.md`
- `docs/superpowers/specs/2026-06-21-open-source-srpg-code-reading-comparative-report.md`
- `game-godot/README.md`
- `game-godot/scripts/demo_v03_model.gd`
- `game-godot/scripts/demo_v03_smoke_test.gd`
- `game-godot/scripts/main.gd`
- `scripts/godot-test.sh`

Current useful reference:

- `demo_v03_model.gd` already proves some behavior: exploration flags, map-story, move preview, cancel move, weapon select, target select, forecast, attack, wait, enemy phase, two battles.

Current problem:

- `demo_v03_model.gd` is a large prototype model. Rules, content, phase strings, event text, AI, and battle state live together. The new kernel must separate those responsibilities.

---

## File Structure

Create these directories:

- `game-godot/scripts/core/battle/`
- `game-godot/scripts/core/scenario/`
- `game-godot/scripts/core/presentation/`
- `game-godot/scripts/core/content/`

Create these files:

- `game-godot/scripts/core/battle/action_context.gd`  
  Owns one in-progress unit action: original cell, current cell, path, selected command, weapon, target, forecast, committed state.

- `game-godot/scripts/core/battle/grid_service.gd`  
  Owns board bounds, passability, occupancy checks, Manhattan distance, reachable cells, simple straight-line path.

- `game-godot/scripts/core/battle/battle_phase_machine.gd`  
  Owns legal phase transitions and names every player/enemy/scenario state.

- `game-godot/scripts/core/battle/targeting_service.gd`  
  Owns weapon availability, post-move filtering, legal target lookup, no-target detection.

- `game-godot/scripts/core/battle/combat_resolver.gd`  
  Owns `CombatForecast` generation and deterministic combat resolution for the sandbox.

- `game-godot/scripts/core/battle/objective_system.gd`  
  Owns protect-objective integrity, victory/failure checks, and objective text.

- `game-godot/scripts/core/battle/enemy_intent_system.gd`  
  Owns enemy intent generation and intent interruption detection.

- `game-godot/scripts/core/battle/command_queue.gd`  
  Owns queued rule commands and command result history.

- `game-godot/scripts/core/battle/battle_session.gd`  
  Owns one battle instance and composes the battle services.

- `game-godot/scripts/core/scenario/run_state.gd`  
  Owns cross-mode flags, relationship counters, map-object state, and post-battle records.

- `game-godot/scripts/core/scenario/scenario_event_bus.gd`  
  Owns trigger matching and action emission for the sandbox.

- `game-godot/scripts/core/presentation/presentation_queue.gd`  
  Owns presentation events emitted by rules and scenario events.

- `game-godot/scripts/core/content/sandbox_content_db.gd`  
  Owns small hardcoded sandbox content: units, weapons, map objects, events, and objective text.

- `game-godot/scripts/srw_kernel_smoke_test.gd`  
  End-to-end headless smoke test for the new kernel.

- `game-godot/scripts/kernel_sandbox_scene.gd`  
  Optional visual sandbox controller.

- `game-godot/scenes/kernel_sandbox.tscn`  
  Optional scene for manual play of the kernel sandbox.

Modify these files:

- `scripts/godot-test.sh`  
  Add the new kernel smoke test to the existing test runner.

- `game-godot/README.md`  
  Document the kernel sandbox and how it differs from the current v0.3 playable prototype.

---

## Definition of Done

The plan is complete when:

- `./scripts/godot-test.sh` runs the new kernel smoke test and existing smoke tests without `SCRIPT ERROR`, `ERROR:`, or `push_error`.
- A headless test proves:
  - exploration flag changes objective wording;
  - `READY -> MOVED_READY -> DONE` works;
  - move cancel restores original cell;
  - attack with no target returns to unit command;
  - weapon select, target select, forecast, cancel, confirm attack work;
  - enemy intent line is created and can be interrupted;
  - objective damage emits an event and writes a post-battle record;
  - battle can reach victory.
- The visual sandbox can be launched manually without replacing the current default `main.tscn`.

---

### Task 1: Action Context And Grid Service

**Files:**
- Create: `game-godot/scripts/core/battle/action_context.gd`
- Create: `game-godot/scripts/core/battle/grid_service.gd`
- Create: `game-godot/scripts/srw_kernel_smoke_test.gd`

- [ ] **Step 1: Write the first failing smoke test**

Create `game-godot/scripts/srw_kernel_smoke_test.gd` with this initial content:

```gdscript
extends SceneTree

const ActionContext := preload("res://scripts/core/battle/action_context.gd")
const GridService := preload("res://scripts/core/battle/grid_service.gd")

var failed := false

func _init() -> void:
	_test_action_context()
	_test_grid_service()
	if failed:
		print("SRW kernel smoke test failed.")
		quit(1)
	print("SRW kernel smoke test passed.")
	quit(0)

func _test_action_context() -> void:
	var ctx := ActionContext.new("haosi", Vector2i(1, 5))
	_assert(ctx.unit_id == "haosi", "context records unit id")
	_assert(ctx.original_cell == Vector2i(1, 5), "context records original cell")
	_assert(not ctx.moved, "context starts unmoved")
	ctx.record_move([Vector2i(2, 5), Vector2i(3, 5)], Vector2i(3, 5))
	_assert(ctx.moved, "record_move marks context moved")
	_assert(ctx.current_cell == Vector2i(3, 5), "record_move updates current cell")
	_assert(ctx.rollback_allowed, "move can be rolled back before commitment")
	ctx.commit("wait")
	_assert(ctx.committed, "commit locks the context")
	_assert(not ctx.rollback_allowed, "committed context cannot roll back")

func _test_grid_service() -> void:
	var grid := GridService.new()
	grid.configure(6, 5, [Vector2i(2, 2)])
	_assert(grid.in_bounds(Vector2i(5, 4)), "last legal cell is in bounds")
	_assert(not grid.in_bounds(Vector2i(6, 4)), "x outside board is invalid")
	_assert(grid.distance(Vector2i(1, 1), Vector2i(3, 2)) == 3, "distance uses manhattan metric")
	_assert(not grid.is_passable(Vector2i(2, 2)), "blocked cell is not passable")
	var cells := grid.reachable_cells(Vector2i(1, 1), 2, [])
	_assert(cells.has(Vector2i(3, 1)), "reachable cells include range endpoint")
	_assert(not cells.has(Vector2i(2, 2)), "reachable cells exclude blocked cell")

func _assert(value: bool, message: String) -> void:
	if value:
		return
	failed = true
	push_error(message)
```

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: FAIL because `res://scripts/core/battle/action_context.gd` does not exist.

- [ ] **Step 3: Implement `ActionContext`**

Create `game-godot/scripts/core/battle/action_context.gd`:

```gdscript
class_name ActionContext
extends RefCounted

var id := ""
var unit_id := ""
var original_cell := Vector2i(-1, -1)
var current_cell := Vector2i(-1, -1)
var path: Array[Vector2i] = []
var moved := false
var selected_command := ""
var selected_weapon := ""
var selected_target := ""
var forecast: Dictionary = {}
var committed := false
var rollback_allowed := true
var started_events: Array[String] = []

func _init(p_unit_id := "", p_original_cell := Vector2i(-1, -1)) -> void:
	id = "%s_action" % p_unit_id
	unit_id = p_unit_id
	original_cell = p_original_cell
	current_cell = p_original_cell

func record_move(p_path: Array, p_current_cell: Vector2i) -> void:
	path.clear()
	for cell in p_path:
		path.append(cell)
	current_cell = p_current_cell
	moved = true
	selected_command = "move"
	rollback_allowed = not committed

func select_weapon(weapon_id: String) -> void:
	selected_weapon = weapon_id
	selected_command = "attack"

func select_target(target_id: String, p_forecast: Dictionary) -> void:
	selected_target = target_id
	forecast = p_forecast.duplicate(true)

func commit(command_id: String) -> void:
	selected_command = command_id
	committed = true
	rollback_allowed = false

func clear_attack_selection() -> void:
	selected_weapon = ""
	selected_target = ""
	forecast.clear()
```

- [ ] **Step 4: Implement `GridService`**

Create `game-godot/scripts/core/battle/grid_service.gd`:

```gdscript
class_name GridService
extends RefCounted

var width := 0
var height := 0
var blocked: Array[Vector2i] = []

func configure(p_width: int, p_height: int, p_blocked: Array = []) -> void:
	width = p_width
	height = p_height
	blocked.clear()
	for cell in p_blocked:
		blocked.append(cell)

func in_bounds(cell: Vector2i) -> bool:
	return cell.x >= 0 and cell.y >= 0 and cell.x < width and cell.y < height

func distance(a: Vector2i, b: Vector2i) -> int:
	return abs(a.x - b.x) + abs(a.y - b.y)

func is_passable(cell: Vector2i) -> bool:
	return in_bounds(cell) and not blocked.has(cell)

func reachable_cells(origin: Vector2i, move_range: int, occupied: Array = []) -> Array[Vector2i]:
	var result: Array[Vector2i] = []
	for y in range(height):
		for x in range(width):
			var cell := Vector2i(x, y)
			if cell == origin:
				continue
			if distance(origin, cell) > move_range:
				continue
			if not is_passable(cell):
				continue
			if occupied.has(cell):
				continue
			result.append(cell)
	return result

func simple_path(origin: Vector2i, target: Vector2i) -> Array[Vector2i]:
	var result: Array[Vector2i] = []
	var cursor := origin
	while cursor.x != target.x:
		cursor.x += 1 if target.x > cursor.x else -1
		result.append(cursor)
	while cursor.y != target.y:
		cursor.y += 1 if target.y > cursor.y else -1
		result.append(cursor)
	return result
```

- [ ] **Step 5: Run test and verify GREEN**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: PASS with `SRW kernel smoke test passed.`

- [ ] **Step 6: Commit**

```bash
git add game-godot/scripts/core/battle/action_context.gd game-godot/scripts/core/battle/grid_service.gd game-godot/scripts/srw_kernel_smoke_test.gd
git commit -m "feat: add SRW kernel action context and grid service"
```

---

### Task 2: Phase Machine And Move/Wait Battle Session

**Files:**
- Create: `game-godot/scripts/core/battle/battle_phase_machine.gd`
- Create: `game-godot/scripts/core/battle/battle_session.gd`
- Modify: `game-godot/scripts/srw_kernel_smoke_test.gd`

- [ ] **Step 1: Extend the smoke test for phase and movement**

Add these constants near the top of `srw_kernel_smoke_test.gd`:

```gdscript
const BattleSession := preload("res://scripts/core/battle/battle_session.gd")
```

Call this function before the final pass/fail block:

```gdscript
	_test_battle_move_wait_flow()
```

Add this function:

```gdscript
func _test_battle_move_wait_flow() -> void:
	var battle := BattleSession.new()
	battle.start_sandbox({})
	_assert(battle.phase() == "player_map_idle", "battle starts in player map idle")
	_assert(battle.select_unit("haosi"), "ready unit can be selected")
	_assert(battle.phase() == "unit_command", "selecting ready unit opens unit command")
	_assert(battle.start_move(), "move command enters move preview")
	_assert(battle.phase() == "move_preview", "phase is move preview")
	_assert(battle.preview_move(Vector2i(3, 5)), "legal move can be previewed")
	_assert(battle.confirm_move(), "move can be confirmed")
	_assert(battle.phase() == "post_move_command", "confirmed move opens post-move command")
	_assert(battle.get_unit("haosi")["action_state"] == "MOVED_READY", "unit is moved-ready after move")
	_assert(not battle.start_move(), "moved-ready unit cannot start second move")
	_assert(battle.cancel_move(), "post-move cancel works")
	_assert(battle.get_unit("haosi")["cell"] == Vector2i(1, 5), "cancel move restores original cell")
	_assert(battle.get_unit("haosi")["action_state"] == "READY", "cancel move restores ready state")
	_assert(battle.start_move(), "unit can move again after cancel")
	_assert(battle.preview_move(Vector2i(3, 5)), "same destination can be previewed again")
	_assert(battle.confirm_move(), "same destination can be confirmed again")
	_assert(battle.wait_unit(), "wait commits action")
	_assert(battle.get_unit("haosi")["action_state"] == "DONE", "wait changes unit to done")
	_assert(not battle.select_unit("haosi"), "done unit cannot be selected for action")
```

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: FAIL because `battle_session.gd` does not exist.

- [ ] **Step 3: Implement `BattlePhaseMachine`**

Create `game-godot/scripts/core/battle/battle_phase_machine.gd`:

```gdscript
class_name BattlePhaseMachine
extends RefCounted

const SCENARIO_EVENT := "scenario_event"
const PLAYER_MAP_IDLE := "player_map_idle"
const UNIT_COMMAND := "unit_command"
const MOVE_PREVIEW := "move_preview"
const MOVING_ANIMATION := "moving_animation"
const POST_MOVE_COMMAND := "post_move_command"
const WEAPON_SELECT := "weapon_select"
const TARGET_SELECT := "target_select"
const FORECAST := "forecast"
const BATTLE_RESOLVE := "battle_resolve"
const ACTION_END := "action_end"
const OBJECTIVE_CHECK := "objective_check"
const GLOBAL_MENU := "global_menu"
const ENEMY_PHASE := "enemy_phase"
const PHASE_REPORT := "phase_report"
const RESULT := "result"

var current := PLAYER_MAP_IDLE

var transitions := {
	PLAYER_MAP_IDLE: [UNIT_COMMAND, GLOBAL_MENU, SCENARIO_EVENT, RESULT],
	UNIT_COMMAND: [MOVE_PREVIEW, WEAPON_SELECT, ACTION_END, PLAYER_MAP_IDLE],
	MOVE_PREVIEW: [MOVING_ANIMATION, UNIT_COMMAND],
	MOVING_ANIMATION: [POST_MOVE_COMMAND],
	POST_MOVE_COMMAND: [WEAPON_SELECT, ACTION_END, UNIT_COMMAND],
	WEAPON_SELECT: [TARGET_SELECT, UNIT_COMMAND, POST_MOVE_COMMAND],
	TARGET_SELECT: [FORECAST, WEAPON_SELECT],
	FORECAST: [BATTLE_RESOLVE, TARGET_SELECT],
	BATTLE_RESOLVE: [SCENARIO_EVENT, ACTION_END],
	SCENARIO_EVENT: [PLAYER_MAP_IDLE, ACTION_END, RESULT],
	ACTION_END: [OBJECTIVE_CHECK],
	OBJECTIVE_CHECK: [PLAYER_MAP_IDLE, PHASE_REPORT, RESULT],
	GLOBAL_MENU: [PLAYER_MAP_IDLE, PHASE_REPORT],
	PHASE_REPORT: [ENEMY_PHASE, PLAYER_MAP_IDLE],
	ENEMY_PHASE: [SCENARIO_EVENT, PLAYER_MAP_IDLE, RESULT],
	RESULT: [],
}

func reset() -> void:
	current = PLAYER_MAP_IDLE

func can_enter(next: String) -> bool:
	return transitions.get(current, []).has(next)

func enter(next: String) -> bool:
	if not can_enter(next):
		return false
	current = next
	return true

func force(next: String) -> void:
	current = next
```

- [ ] **Step 4: Implement `BattleSession` with movement and wait**

Create `game-godot/scripts/core/battle/battle_session.gd`:

```gdscript
class_name BattleSession
extends RefCounted

const ActionContextScript := preload("res://scripts/core/battle/action_context.gd")
const GridServiceScript := preload("res://scripts/core/battle/grid_service.gd")
const BattlePhaseMachineScript := preload("res://scripts/core/battle/battle_phase_machine.gd")

var grid := GridServiceScript.new()
var phases := BattlePhaseMachineScript.new()
var units: Array[Dictionary] = []
var selected_unit_id := ""
var preview_cell := Vector2i(-1, -1)
var action_context
var last_prompt := ""

func start_sandbox(run_flags: Dictionary) -> void:
	grid.configure(12, 8, [])
	phases.reset()
	selected_unit_id = ""
	preview_cell = Vector2i(-1, -1)
	action_context = null
	last_prompt = "PLAYER PHASE：选择可行动单位。"
	units = [
		_player("jicun", "纪存 / 临时指挥机", Vector2i(1, 4), 18, 30, 3, []),
		_player("haosi", "豪司 / 社勇拳", Vector2i(1, 5), 20, 24, 4, []),
		_player("doudeng", "兜灯 / 整备机", Vector2i(1, 6), 16, 28, 3, []),
		_enemy("drone_a", "封存无人机A", Vector2i(6, 5), 6),
		_objective("message_wall", "留言墙", Vector2i(8, 4), 3),
	]
	if bool(run_flags.get("message_wall", false)):
		last_prompt = "PLAYER PHASE：留言墙已被探索确认，保护目标说明增强。"

func phase() -> String:
	return phases.current

func get_unit(unit_id: String) -> Dictionary:
	for unit in units:
		if unit.get("id", "") == unit_id:
			return unit
	return {}

func living_units(team := "") -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for unit in units:
		if int(unit.get("hp", 0)) <= 0:
			continue
		if team != "" and unit.get("team", "") != team:
			continue
		result.append(unit)
	return result

func occupied_cells(except_unit_id := "") -> Array[Vector2i]:
	var result: Array[Vector2i] = []
	for unit in living_units():
		if unit.get("id", "") == except_unit_id:
			continue
		result.append(unit.get("cell", Vector2i(-1, -1)))
	return result

func select_unit(unit_id: String) -> bool:
	var unit := get_unit(unit_id)
	if unit.is_empty():
		last_prompt = "没有这个单位。"
		return false
	if unit.get("team", "") != "player" or unit.get("action_state", "") != "READY":
		last_prompt = "该单位本阶段不能行动。"
		return false
	selected_unit_id = unit_id
	action_context = ActionContextScript.new(unit_id, unit.get("cell", Vector2i.ZERO))
	phases.force(BattlePhaseMachineScript.UNIT_COMMAND)
	last_prompt = "单位命令：移动、攻击、资料、待机。"
	return true

func start_move() -> bool:
	if not [BattlePhaseMachineScript.UNIT_COMMAND].has(phases.current):
		return false
	var unit := get_unit(selected_unit_id)
	if unit.is_empty() or unit.get("action_state", "") != "READY":
		last_prompt = "该单位不能再次移动。"
		return false
	preview_cell = unit.get("cell", Vector2i.ZERO)
	return phases.enter(BattlePhaseMachineScript.MOVE_PREVIEW)

func reachable_cells(unit_id: String) -> Array[Vector2i]:
	var unit := get_unit(unit_id)
	if unit.is_empty():
		return []
	return grid.reachable_cells(unit.get("cell", Vector2i.ZERO), int(unit.get("move", 0)), occupied_cells(unit_id))

func preview_move(cell: Vector2i) -> bool:
	if phases.current != BattlePhaseMachineScript.MOVE_PREVIEW:
		return false
	if not reachable_cells(selected_unit_id).has(cell):
		last_prompt = "不能移动到该格。"
		return false
	preview_cell = cell
	last_prompt = "移动预览：确认后进入移动后命令。"
	return true

func confirm_move() -> bool:
	if phases.current != BattlePhaseMachineScript.MOVE_PREVIEW:
		return false
	if not grid.in_bounds(preview_cell):
		return false
	var unit := get_unit(selected_unit_id)
	if unit.is_empty():
		return false
	var origin: Vector2i = unit.get("cell", Vector2i.ZERO)
	var path := grid.simple_path(origin, preview_cell)
	action_context.record_move(path, preview_cell)
	unit["cell"] = preview_cell
	unit["action_state"] = "MOVED_READY"
	phases.force(BattlePhaseMachineScript.POST_MOVE_COMMAND)
	last_prompt = "移动完成：可攻击、待机或取消移动。"
	return true

func cancel_move() -> bool:
	if phases.current != BattlePhaseMachineScript.POST_MOVE_COMMAND:
		return false
	if action_context == null or not action_context.rollback_allowed:
		return false
	var unit := get_unit(selected_unit_id)
	if unit.is_empty():
		return false
	unit["cell"] = action_context.original_cell
	unit["action_state"] = "READY"
	preview_cell = Vector2i(-1, -1)
	action_context = ActionContextScript.new(selected_unit_id, unit["cell"])
	phases.force(BattlePhaseMachineScript.UNIT_COMMAND)
	last_prompt = "已取消移动，单位回到原位。"
	return true

func wait_unit() -> bool:
	if not [BattlePhaseMachineScript.UNIT_COMMAND, BattlePhaseMachineScript.POST_MOVE_COMMAND].has(phases.current):
		return false
	var unit := get_unit(selected_unit_id)
	if unit.is_empty():
		return false
	unit["action_state"] = "DONE"
	if action_context != null:
		action_context.commit("wait")
	_end_current_action()
	last_prompt = "%s 待机。" % unit.get("name", selected_unit_id)
	return true

func all_players_done() -> bool:
	for unit in living_units("player"):
		if unit.get("action_state", "") == "READY":
			return false
	return true

func _end_current_action() -> void:
	selected_unit_id = ""
	preview_cell = Vector2i(-1, -1)
	action_context = null
	phases.force(BattlePhaseMachineScript.PLAYER_MAP_IDLE)

func _player(id: String, name: String, cell: Vector2i, hp: int, en: int, move: int, weapons: Array) -> Dictionary:
	return {"id": id, "name": name, "team": "player", "cell": cell, "hp": hp, "max_hp": hp, "en": en, "max_en": en, "move": move, "weapons": weapons, "action_state": "READY"}

func _enemy(id: String, name: String, cell: Vector2i, hp: int) -> Dictionary:
	return {"id": id, "name": name, "team": "enemy", "cell": cell, "hp": hp, "max_hp": hp, "move": 3, "weapons": [], "action_state": "READY"}

func _objective(id: String, name: String, cell: Vector2i, integrity: int) -> Dictionary:
	return {"id": id, "name": name, "team": "object", "cell": cell, "hp": integrity, "max_hp": integrity, "integrity": integrity, "action_state": "SCRIPT_LOCKED"}
```

- [ ] **Step 5: Run test and verify GREEN**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add game-godot/scripts/core/battle/battle_phase_machine.gd game-godot/scripts/core/battle/battle_session.gd game-godot/scripts/srw_kernel_smoke_test.gd
git commit -m "feat: add SRW kernel phase machine and movement flow"
```

---

### Task 3: Targeting, Forecast, No-Target Recovery, And Attack Commit

**Files:**
- Create: `game-godot/scripts/core/battle/targeting_service.gd`
- Create: `game-godot/scripts/core/battle/combat_resolver.gd`
- Modify: `game-godot/scripts/core/battle/battle_session.gd`
- Modify: `game-godot/scripts/srw_kernel_smoke_test.gd`

- [ ] **Step 1: Extend smoke test for no-target and attack flow**

Add this function call:

```gdscript
	_test_weapon_target_forecast_flow()
```

Add this function:

```gdscript
func _test_weapon_target_forecast_flow() -> void:
	var battle := BattleSession.new()
	battle.start_sandbox({"message_wall": true})
	_assert(battle.select_unit("doudeng"), "doudeng can be selected")
	_assert(not battle.open_weapon_select(), "attack with no legal target fails safely")
	_assert(battle.phase() == "unit_command", "no-target attack remains in unit command")
	_assert(battle.last_prompt.contains("没有可攻击目标"), "no-target prompt is explicit")

	battle = BattleSession.new()
	battle.start_sandbox({"message_wall": true})
	_assert(battle.select_unit("haosi"), "haosi can be selected for attack flow")
	_assert(battle.start_move(), "haosi can enter move preview")
	_assert(battle.preview_move(Vector2i(3, 5)), "haosi can move toward drone")
	_assert(battle.confirm_move(), "haosi confirms movement")
	_assert(battle.open_weapon_select(), "weapon select opens after moving into range")
	_assert(battle.phase() == "weapon_select", "phase is weapon select")
	_assert(battle.select_weapon("haosi_fist"), "haosi fist can be selected")
	_assert(battle.phase() == "target_select", "weapon selection enters target select")
	_assert(battle.select_target("drone_a"), "target selection creates forecast")
	_assert(battle.phase() == "forecast", "target selection enters forecast")
	_assert(int(battle.current_forecast.get("damage", 0)) > 0, "forecast has damage")
	_assert(bool(battle.current_forecast.get("interrupts_intent", false)), "forecast reports intent interruption")
	battle.cancel_attack_flow()
	_assert(battle.phase() == "target_select", "cancel from forecast returns to target select")
	_assert(battle.select_target("drone_a"), "target can be selected again after cancel")
	_assert(battle.confirm_attack(), "attack can be confirmed")
	_assert(battle.get_unit("haosi")["action_state"] == "DONE", "confirmed attack spends unit")
	_assert(int(battle.get_unit("drone_a")["hp"]) < int(battle.get_unit("drone_a")["max_hp"]), "target HP is reduced")
```

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: FAIL because `open_weapon_select` is not defined.

- [ ] **Step 3: Implement `TargetingService`**

Create `game-godot/scripts/core/battle/targeting_service.gd`:

```gdscript
class_name TargetingService
extends RefCounted

func available_weapons(attacker: Dictionary, moved: bool) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for weapon in attacker.get("weapons", []):
		if moved and not bool(weapon.get("post_move", true)):
			continue
		if int(attacker.get("en", 0)) < int(weapon.get("en", 0)):
			continue
		result.append(weapon)
	return result

func legal_targets(attacker: Dictionary, weapon: Dictionary, units: Array, grid) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for target in units:
		if int(target.get("hp", 0)) <= 0:
			continue
		if target.get("team", "") == attacker.get("team", ""):
			continue
		if target.get("team", "") == "object" and attacker.get("team", "") != "enemy":
			continue
		var d: int = grid.distance(attacker.get("cell", Vector2i.ZERO), target.get("cell", Vector2i.ZERO))
		if d < int(weapon.get("min", 1)):
			continue
		if d > int(weapon.get("max", 1)):
			continue
		result.append(target)
	return result

func any_legal_target(attacker: Dictionary, units: Array, grid) -> bool:
	for weapon in available_weapons(attacker, bool(attacker.get("action_state", "") == "MOVED_READY")):
		if not legal_targets(attacker, weapon, units, grid).is_empty():
			return true
	return false
```

- [ ] **Step 4: Implement `CombatResolver`**

Create `game-godot/scripts/core/battle/combat_resolver.gd`:

```gdscript
class_name CombatResolver
extends RefCounted

func build_forecast(attacker: Dictionary, weapon: Dictionary, target: Dictionary, intent_target_id := "") -> Dictionary:
	if attacker.is_empty() or weapon.is_empty() or target.is_empty():
		return {}
	var damage: int = int(weapon.get("power", 1)) + int(attacker.get("attack_bonus", 0))
	var target_hp_after: int = max(0, int(target.get("hp", 0)) - damage)
	return {
		"attacker_id": attacker.get("id", ""),
		"target_id": target.get("id", ""),
		"weapon_id": weapon.get("id", ""),
		"weapon_name": weapon.get("name", weapon.get("id", "")),
		"hit_rate": int(weapon.get("hit", 100)),
		"damage": damage,
		"target_hp_before": int(target.get("hp", 0)),
		"target_hp_after": target_hp_after,
		"en_cost": int(weapon.get("en", 0)),
		"counter_possible": false,
		"counter_damage": 0,
		"interrupts_intent": target.get("id", "") == intent_target_id or target_hp_after <= 0,
		"reasons": ["距离满足武器射程", "沙盒使用确定性命中"],
	}

func resolve(forecast: Dictionary, attacker: Dictionary, target: Dictionary) -> Dictionary:
	if forecast.is_empty() or attacker.is_empty() or target.is_empty():
		return {}
	attacker["en"] = max(0, int(attacker.get("en", 0)) - int(forecast.get("en_cost", 0)))
	target["hp"] = int(forecast.get("target_hp_after", target.get("hp", 0)))
	return {
		"attacker_id": attacker.get("id", ""),
		"target_id": target.get("id", ""),
		"weapon_id": forecast.get("weapon_id", ""),
		"damage": int(forecast.get("damage", 0)),
		"destroyed": int(target.get("hp", 0)) <= 0,
		"interrupts_intent": bool(forecast.get("interrupts_intent", false)),
	}
```

- [ ] **Step 5: Extend `BattleSession` with weapons and attack methods**

Modify the top of `battle_session.gd` by adding preloads and fields:

```gdscript
const TargetingServiceScript := preload("res://scripts/core/battle/targeting_service.gd")
const CombatResolverScript := preload("res://scripts/core/battle/combat_resolver.gd")

var targeting := TargetingServiceScript.new()
var combat := CombatResolverScript.new()
var selected_weapon_id := ""
var selected_target_id := ""
var current_forecast: Dictionary = {}
```

Replace the `units = [` block in `start_sandbox` with weapons:

```gdscript
	units = [
		_player("jicun", "纪存 / 临时指挥机", Vector2i(1, 4), 18, 30, 3, [
			{"id": "archive_hook", "name": "档案钩索", "power": 3, "min": 1, "max": 2, "hit": 95, "en": 0, "post_move": true},
		]),
		_player("haosi", "豪司 / 社勇拳", Vector2i(1, 5), 20, 24, 4, [
			{"id": "haosi_fist", "name": "社勇冲拳", "power": 6, "min": 1, "max": 3, "hit": 100, "en": 5, "post_move": true},
		]),
		_player("doudeng", "兜灯 / 整备机", Vector2i(1, 6), 16, 28, 3, [
			{"id": "wrench_arc", "name": "扳手电弧", "power": 3, "min": 1, "max": 2, "hit": 90, "en": 0, "post_move": true},
		]),
		_enemy("drone_a", "封存无人机A", Vector2i(6, 5), 6),
		_objective("message_wall", "留言墙", Vector2i(8, 4), 3),
	]
```

Add these methods to `battle_session.gd`:

```gdscript
func available_weapons(unit_id: String) -> Array[Dictionary]:
	var unit := get_unit(unit_id)
	if unit.is_empty():
		return []
	return targeting.available_weapons(unit, unit.get("action_state", "") == "MOVED_READY")

func open_weapon_select() -> bool:
	if not [BattlePhaseMachineScript.UNIT_COMMAND, BattlePhaseMachineScript.POST_MOVE_COMMAND].has(phases.current):
		return false
	var attacker := get_unit(selected_unit_id)
	if attacker.is_empty():
		return false
	if not targeting.any_legal_target(attacker, units, grid):
		last_prompt = "当前射程内没有可攻击目标。可先移动或待机。"
		return false
	phases.force(BattlePhaseMachineScript.WEAPON_SELECT)
	last_prompt = "选择武器。"
	return true

func select_weapon(weapon_id: String) -> bool:
	if phases.current != BattlePhaseMachineScript.WEAPON_SELECT:
		return false
	var attacker := get_unit(selected_unit_id)
	var weapon := _weapon_by_id(attacker, weapon_id)
	if weapon.is_empty():
		return false
	var targets := targeting.legal_targets(attacker, weapon, units, grid)
	if targets.is_empty():
		last_prompt = "该武器当前没有合法目标。"
		return false
	selected_weapon_id = weapon_id
	if action_context != null:
		action_context.select_weapon(weapon_id)
	phases.force(BattlePhaseMachineScript.TARGET_SELECT)
	last_prompt = "选择目标。"
	return true

func weapon_targets_in_range(unit_id: String, weapon_id: String) -> Array[Dictionary]:
	var attacker := get_unit(unit_id)
	var weapon := _weapon_by_id(attacker, weapon_id)
	if attacker.is_empty() or weapon.is_empty():
		return []
	return targeting.legal_targets(attacker, weapon, units, grid)

func select_target(target_id: String) -> bool:
	if phases.current != BattlePhaseMachineScript.TARGET_SELECT:
		return false
	var attacker := get_unit(selected_unit_id)
	var target := get_unit(target_id)
	var weapon := _weapon_by_id(attacker, selected_weapon_id)
	if not weapon_targets_in_range(selected_unit_id, selected_weapon_id).has(target):
		last_prompt = "该目标不在射程内。"
		return false
	selected_target_id = target_id
	current_forecast = combat.build_forecast(attacker, weapon, target, "message_wall")
	if current_forecast.is_empty():
		return false
	if action_context != null:
		action_context.select_target(target_id, current_forecast)
	phases.force(BattlePhaseMachineScript.FORECAST)
	last_prompt = "战斗预测：确认后不可取消。"
	return true

func cancel_attack_flow() -> void:
	if phases.current == BattlePhaseMachineScript.FORECAST:
		current_forecast.clear()
		selected_target_id = ""
		phases.force(BattlePhaseMachineScript.TARGET_SELECT)
		last_prompt = "已返回目标选择。"
		return
	if phases.current == BattlePhaseMachineScript.TARGET_SELECT:
		selected_target_id = ""
		selected_weapon_id = ""
		phases.force(BattlePhaseMachineScript.WEAPON_SELECT)
		last_prompt = "已返回武器选择。"
		return
	if phases.current == BattlePhaseMachineScript.WEAPON_SELECT:
		selected_weapon_id = ""
		phases.force(BattlePhaseMachineScript.POST_MOVE_COMMAND if _selected_unit_moved() else BattlePhaseMachineScript.UNIT_COMMAND)
		last_prompt = "已返回单位命令。"

func confirm_attack() -> bool:
	if phases.current != BattlePhaseMachineScript.FORECAST:
		return false
	var attacker := get_unit(selected_unit_id)
	var target := get_unit(selected_target_id)
	var result := combat.resolve(current_forecast, attacker, target)
	if result.is_empty():
		return false
	attacker["action_state"] = "DONE"
	if action_context != null:
		action_context.commit("attack")
	_end_current_action()
	last_prompt = "%s 使用%s命中 %s。" % [attacker.get("name", ""), current_forecast.get("weapon_name", ""), target.get("name", "")]
	current_forecast.clear()
	selected_weapon_id = ""
	selected_target_id = ""
	return true

func _selected_unit_moved() -> bool:
	var unit := get_unit(selected_unit_id)
	return not unit.is_empty() and unit.get("action_state", "") == "MOVED_READY"

func _weapon_by_id(attacker: Dictionary, weapon_id: String) -> Dictionary:
	if attacker.is_empty():
		return {}
	for weapon in attacker.get("weapons", []):
		if weapon.get("id", "") == weapon_id:
			return weapon
	return {}
```

- [ ] **Step 6: Run test and verify GREEN**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add game-godot/scripts/core/battle/targeting_service.gd game-godot/scripts/core/battle/combat_resolver.gd game-godot/scripts/core/battle/battle_session.gd game-godot/scripts/srw_kernel_smoke_test.gd
git commit -m "feat: add SRW kernel targeting and forecast flow"
```

---

### Task 4: Objectives, Enemy Intents, And Enemy Phase

**Files:**
- Create: `game-godot/scripts/core/battle/objective_system.gd`
- Create: `game-godot/scripts/core/battle/enemy_intent_system.gd`
- Modify: `game-godot/scripts/core/battle/battle_session.gd`
- Modify: `game-godot/scripts/srw_kernel_smoke_test.gd`

- [ ] **Step 1: Extend smoke test for intents and objectives**

Add this function call:

```gdscript
	_test_intent_and_objective_flow()
```

Add this function:

```gdscript
func _test_intent_and_objective_flow() -> void:
	var battle := BattleSession.new()
	battle.start_sandbox({"message_wall": true})
	_assert(battle.current_objective_text().contains("留言墙"), "objective mentions protected object")
	_assert(battle.enemy_intents.has("drone_a"), "enemy intent is generated")
	_assert(battle.enemy_intents["drone_a"]["target_id"] == "message_wall", "drone intent targets message wall")
	_assert(battle.select_unit("haosi"), "haosi selected for intent interruption")
	_assert(battle.start_move(), "haosi starts move")
	_assert(battle.preview_move(Vector2i(3, 5)), "haosi previews move")
	_assert(battle.confirm_move(), "haosi confirms move")
	_assert(battle.open_weapon_select(), "weapon select opens")
	_assert(battle.select_weapon("haosi_fist"), "weapon selected")
	_assert(battle.select_target("drone_a"), "target selected")
	_assert(battle.confirm_attack(), "attack confirmed")
	_assert(not battle.enemy_intents.has("drone_a"), "destroyed or interrupted enemy intent is removed")

	battle = BattleSession.new()
	battle.start_sandbox({"message_wall": true})
	var before_integrity := int(battle.get_unit("message_wall").get("integrity", 0))
	battle.force_all_players_done_for_test()
	_assert(battle.end_player_phase(), "enemy phase can resolve")
	var after_integrity := int(battle.get_unit("message_wall").get("integrity", 0))
	_assert(after_integrity < before_integrity, "uninterrupted enemy intent damages objective")
	_assert(battle.post_battle_records.size() > 0, "objective damage creates record")
```

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: FAIL because `current_objective_text` is not defined.

- [ ] **Step 3: Implement `ObjectiveSystem`**

Create `game-godot/scripts/core/battle/objective_system.gd`:

```gdscript
class_name ObjectiveSystem
extends RefCounted

var protected_object_id := "message_wall"
var explored_message_wall := false

func configure(flags: Dictionary) -> void:
	explored_message_wall = bool(flags.get("message_wall", false))

func objective_text() -> String:
	if explored_message_wall:
		return "保护留言墙：纸条已经被确认不是附件。击退封存无人机。"
	return "保护馆内记忆对象：击退封存无人机。"

func damage_objective(units: Array, object_id: String, amount: int) -> Dictionary:
	for unit in units:
		if unit.get("id", "") != object_id:
			continue
		unit["integrity"] = max(0, int(unit.get("integrity", unit.get("hp", 0))) - amount)
		unit["hp"] = int(unit["integrity"])
		return {
			"objective_id": object_id,
			"integrity": int(unit["integrity"]),
			"failed": int(unit["integrity"]) <= 0,
		}
	return {}

func victory_reached(units: Array) -> bool:
	for unit in units:
		if unit.get("team", "") == "enemy" and int(unit.get("hp", 0)) > 0:
			return false
	return true

func failure_reached(units: Array) -> bool:
	for unit in units:
		if unit.get("id", "") == protected_object_id:
			return int(unit.get("integrity", unit.get("hp", 0))) <= 0
	return false
```

- [ ] **Step 4: Implement `EnemyIntentSystem`**

Create `game-godot/scripts/core/battle/enemy_intent_system.gd`:

```gdscript
class_name EnemyIntentSystem
extends RefCounted

func build_intents(units: Array, grid) -> Dictionary:
	var result := {}
	var objective := _find_unit(units, "message_wall")
	if objective.is_empty():
		return result
	for unit in units:
		if unit.get("team", "") != "enemy" or int(unit.get("hp", 0)) <= 0:
			continue
		result[unit.get("id", "")] = {
			"actor_id": unit.get("id", ""),
			"action_type": "archive_object",
			"target_id": objective.get("id", ""),
			"target_cell": objective.get("cell", Vector2i.ZERO),
			"predicted_result": {"objective_damage": 1, "status_added": "archived"},
			"interrupt_conditions": ["destroy_actor", "push_actor_out_of_range", "block_line"],
			"in_range": grid.distance(unit.get("cell", Vector2i.ZERO), objective.get("cell", Vector2i.ZERO)) <= 2,
		}
	return result

func remove_interrupted_intents(intents: Dictionary, combat_result: Dictionary) -> void:
	var target_id := String(combat_result.get("target_id", ""))
	if bool(combat_result.get("destroyed", false)) and intents.has(target_id):
		intents.erase(target_id)

func _find_unit(units: Array, unit_id: String) -> Dictionary:
	for unit in units:
		if unit.get("id", "") == unit_id:
			return unit
	return {}
```

- [ ] **Step 5: Extend `BattleSession` with objectives, intents, enemy phase, and test helper**

Add preloads and fields:

```gdscript
const ObjectiveSystemScript := preload("res://scripts/core/battle/objective_system.gd")
const EnemyIntentSystemScript := preload("res://scripts/core/battle/enemy_intent_system.gd")

var objectives := ObjectiveSystemScript.new()
var enemy_intents := {}
var enemy_intent_system := EnemyIntentSystemScript.new()
var post_battle_records: Array[String] = []
var outcome := ""
```

Add this at the end of `start_sandbox`:

```gdscript
	objectives.configure(run_flags)
	_refresh_enemy_intents()
```

In `confirm_attack`, after `var result := combat.resolve(...)`, add:

```gdscript
	enemy_intent_system.remove_interrupted_intents(enemy_intents, result)
```

Add these methods:

```gdscript
func current_objective_text() -> String:
	return objectives.objective_text()

func end_player_phase() -> bool:
	if not all_players_done():
		last_prompt = "还有单位可行动，暂不能结束阶段。"
		return false
	phases.force(BattlePhaseMachineScript.ENEMY_PHASE)
	for enemy_id in enemy_intents.keys():
		var intent: Dictionary = enemy_intents[enemy_id]
		if intent.get("action_type", "") != "archive_object":
			continue
		var actor := get_unit(enemy_id)
		if actor.is_empty() or int(actor.get("hp", 0)) <= 0:
			continue
		var damage_result := objectives.damage_objective(units, intent.get("target_id", ""), 1)
		if not damage_result.is_empty():
			post_battle_records.append("%s 封存了 %s，完整度剩余 %d。" % [actor.get("name", enemy_id), intent.get("target_id", ""), damage_result.get("integrity", 0)])
	for unit in living_units("player"):
		unit["action_state"] = "READY"
	_refresh_enemy_intents()
	phases.force(BattlePhaseMachineScript.PLAYER_MAP_IDLE)
	last_prompt = "PLAYER PHASE：敌方意图已结算。"
	return true

func force_all_players_done_for_test() -> void:
	for unit in living_units("player"):
		unit["action_state"] = "DONE"

func _refresh_enemy_intents() -> void:
	enemy_intents = enemy_intent_system.build_intents(units, grid)
```

- [ ] **Step 6: Run test and verify GREEN**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add game-godot/scripts/core/battle/objective_system.gd game-godot/scripts/core/battle/enemy_intent_system.gd game-godot/scripts/core/battle/battle_session.gd game-godot/scripts/srw_kernel_smoke_test.gd
git commit -m "feat: add SRW kernel objectives and enemy intents"
```

---

### Task 5: Scenario Event Bus, Run State, And Presentation Queue

**Files:**
- Create: `game-godot/scripts/core/scenario/run_state.gd`
- Create: `game-godot/scripts/core/scenario/scenario_event_bus.gd`
- Create: `game-godot/scripts/core/presentation/presentation_queue.gd`
- Create: `game-godot/scripts/core/content/sandbox_content_db.gd`
- Modify: `game-godot/scripts/srw_kernel_smoke_test.gd`

- [ ] **Step 1: Extend smoke test for scenario events**

Add constants:

```gdscript
const RunState := preload("res://scripts/core/scenario/run_state.gd")
const ScenarioEventBus := preload("res://scripts/core/scenario/scenario_event_bus.gd")
const PresentationQueue := preload("res://scripts/core/presentation/presentation_queue.gd")
const SandboxContentDB := preload("res://scripts/core/content/sandbox_content_db.gd")
```

Add this function call:

```gdscript
	_test_scenario_event_bridge()
```

Add this function:

```gdscript
func _test_scenario_event_bridge() -> void:
	var run_state := RunState.new()
	var content := SandboxContentDB.new()
	var events := ScenarioEventBus.new()
	var presentation := PresentationQueue.new()
	events.configure(content.events(), run_state, presentation)

	events.emit("hotspot_inspect", {"object_id": "message_wall"})
	_assert(bool(run_state.flags.get("message_wall", false)), "hotspot inspect sets message wall flag")
	_assert(run_state.map_objects["message_wall"]["known"], "hotspot inspect marks map object known")

	var actions := events.emit("map_start", {"battle_id": "kernel_sandbox"})
	_assert(actions.size() > 0, "map start emits presentation actions")
	_assert(presentation.has_next(), "presentation queue receives map start action")
	var first := presentation.pop()
	_assert(first["kind"] == "dialogue", "presentation queue stores dialogue action")

	events.emit("before_attack", {"attacker_id": "haosi", "target_id": "drone_a"})
	events.emit("before_attack", {"attacker_id": "haosi", "target_id": "drone_a"})
	_assert(run_state.once_events.has("first_haosi_attack"), "once event is recorded")

	events.emit("objective_damaged", {"objective_id": "message_wall", "integrity": 2})
	_assert(run_state.post_battle_records.size() == 1, "objective damage writes post-battle record")
```

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: FAIL because `run_state.gd` does not exist.

- [ ] **Step 3: Implement `RunState`**

Create `game-godot/scripts/core/scenario/run_state.gd`:

```gdscript
class_name RunState
extends RefCounted

var flags := {}
var relationships := {"qihai": 0, "doudeng": 0, "guardian": 0, "audience": 0}
var map_objects := {
	"message_wall": {"known": false, "emotional_weight": 0, "integrity": 3},
	"guardian_z": {"known": false, "emotional_weight": 0, "integrity": 1},
	"zero_corridor": {"known": false, "emotional_weight": 0, "integrity": 2},
}
var once_events: Array[String] = []
var post_battle_records: Array[String] = []

func set_flag(flag_id: String, value := true) -> void:
	flags[flag_id] = value

func mark_object_known(object_id: String) -> void:
	if not map_objects.has(object_id):
		map_objects[object_id] = {"known": true, "emotional_weight": 1, "integrity": 1}
		return
	map_objects[object_id]["known"] = true
	map_objects[object_id]["emotional_weight"] = int(map_objects[object_id].get("emotional_weight", 0)) + 1

func record_once(event_id: String) -> void:
	if not once_events.has(event_id):
		once_events.append(event_id)

func add_record(text: String) -> void:
	post_battle_records.append(text)
```

- [ ] **Step 4: Implement `PresentationQueue`**

Create `game-godot/scripts/core/presentation/presentation_queue.gd`:

```gdscript
class_name PresentationQueue
extends RefCounted

var queue: Array[Dictionary] = []

func push(action: Dictionary) -> void:
	queue.append(action.duplicate(true))

func push_many(actions: Array) -> void:
	for action in actions:
		push(action)

func has_next() -> bool:
	return not queue.is_empty()

func pop() -> Dictionary:
	if queue.is_empty():
		return {}
	return queue.pop_front()

func clear() -> void:
	queue.clear()
```

- [ ] **Step 5: Implement `SandboxContentDB`**

Create `game-godot/scripts/core/content/sandbox_content_db.gd`:

```gdscript
class_name SandboxContentDB
extends RefCounted

func events() -> Array[Dictionary]:
	return [
		{
			"id": "inspect_message_wall",
			"trigger": "hotspot_inspect",
			"conditions": {"object_id": "message_wall"},
			"actions": [
				{"kind": "set_flag", "flag": "message_wall", "value": true},
				{"kind": "mark_object_known", "object_id": "message_wall"},
				{"kind": "dialogue", "speaker": "纪存", "text": "这些纸条不是附件。它们是人来过的证据。"},
			],
		},
		{
			"id": "map_start_message_wall_known",
			"trigger": "map_start",
			"conditions": {"flag": "message_wall"},
			"actions": [
				{"kind": "dialogue", "speaker": "七海", "text": "封存线的第一目标是留言墙。它知道那里最不该被归档。"},
			],
		},
		{
			"id": "first_haosi_attack",
			"trigger": "before_attack",
			"once": true,
			"conditions": {"attacker_id": "haosi"},
			"actions": [
				{"kind": "dialogue", "speaker": "豪司", "text": "名字可以不合规，拳头先合格。"},
			],
		},
		{
			"id": "message_wall_damaged",
			"trigger": "objective_damaged",
			"conditions": {"objective_id": "message_wall"},
			"actions": [
				{"kind": "append_record", "text": "留言墙受损：纸条边缘出现封存白线。"},
				{"kind": "dialogue", "speaker": "纪存", "text": "别碰那面墙。那不是资料，那是人。"},
			],
		},
	]
```

- [ ] **Step 6: Implement `ScenarioEventBus`**

Create `game-godot/scripts/core/scenario/scenario_event_bus.gd`:

```gdscript
class_name ScenarioEventBus
extends RefCounted

var event_defs: Array[Dictionary] = []
var run_state
var presentation

func configure(p_events: Array, p_run_state, p_presentation) -> void:
	event_defs = p_events.duplicate(true)
	run_state = p_run_state
	presentation = p_presentation

func emit(trigger: String, payload: Dictionary) -> Array[Dictionary]:
	var emitted: Array[Dictionary] = []
	for event_def in event_defs:
		if event_def.get("trigger", "") != trigger:
			continue
		var event_id := String(event_def.get("id", ""))
		if bool(event_def.get("once", false)) and run_state.once_events.has(event_id):
			continue
		if not _conditions_match(event_def.get("conditions", {}), payload):
			continue
		if bool(event_def.get("once", false)):
			run_state.record_once(event_id)
		for action in event_def.get("actions", []):
			_apply_action(action, payload)
			emitted.append(action)
	return emitted

func _conditions_match(conditions: Dictionary, payload: Dictionary) -> bool:
	for key in conditions.keys():
		if key == "flag":
			if not bool(run_state.flags.get(conditions[key], false)):
				return false
			continue
		if payload.get(key, null) != conditions[key]:
			return false
	return true

func _apply_action(action: Dictionary, payload: Dictionary) -> void:
	match String(action.get("kind", "")):
		"set_flag":
			run_state.set_flag(action.get("flag", ""), bool(action.get("value", true)))
		"mark_object_known":
			run_state.mark_object_known(action.get("object_id", ""))
		"append_record":
			run_state.add_record(action.get("text", ""))
		"dialogue":
			presentation.push(action)
```

- [ ] **Step 7: Run test and verify GREEN**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_kernel_smoke_test.gd
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add game-godot/scripts/core/scenario/run_state.gd game-godot/scripts/core/scenario/scenario_event_bus.gd game-godot/scripts/core/presentation/presentation_queue.gd game-godot/scripts/core/content/sandbox_content_db.gd game-godot/scripts/srw_kernel_smoke_test.gd
git commit -m "feat: add SRW kernel scenario event bridge"
```

---

### Task 6: Test Runner Integration And Visual Sandbox Scene

**Files:**
- Create: `game-godot/scripts/kernel_sandbox_scene.gd`
- Create: `game-godot/scenes/kernel_sandbox.tscn`
- Modify: `scripts/godot-test.sh`

- [ ] **Step 1: Modify test runner**

In `scripts/godot-test.sh`, add this log variable after `DEMO_V03_LOG`:

```bash
KERNEL_LOG="$LOG_DIR/chao-gag-godot-srw-kernel-smoke.log"
```

Add this command after the existing demo test commands:

```bash
"$GODOT_BIN" --headless --path . --script res://scripts/srw_kernel_smoke_test.gd 2>&1 | tee "$KERNEL_LOG"
```

Update the final `rg` command to include `"$KERNEL_LOG"`:

```bash
if rg -n "SCRIPT ERROR|ERROR:|push_error" "$CLI_LOG" "$CHAPTER_LOG" "$SRW_SLICE_LOG" "$DEMO_V02_LOG" "$DEMO_V03_LOG" "$KERNEL_LOG"; then
  exit 1
fi
```

- [ ] **Step 2: Run full test suite**

Run:

```bash
./scripts/godot-test.sh
```

Expected: PASS through all existing smoke tests plus `SRW kernel smoke test passed.`

- [ ] **Step 3: Create a minimal visual sandbox controller**

Create `game-godot/scripts/kernel_sandbox_scene.gd`:

```gdscript
extends Node2D

const BattleSession := preload("res://scripts/core/battle/battle_session.gd")

const TILE := 56.0
const ORIGIN := Vector2(96, 112)

var battle := BattleSession.new()
var cursor := Vector2i(1, 5)
var font: Font

func _ready() -> void:
	font = ThemeDB.fallback_font
	battle.start_sandbox({"message_wall": true})
	set_process(true)

func _process(_delta: float) -> void:
	queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_LEFT:
				cursor.x = max(0, cursor.x - 1)
			KEY_RIGHT:
				cursor.x = min(11, cursor.x + 1)
			KEY_UP:
				cursor.y = max(0, cursor.y - 1)
			KEY_DOWN:
				cursor.y = min(7, cursor.y + 1)
			KEY_ENTER, KEY_SPACE:
				_confirm()
			KEY_M:
				if battle.phase() == "unit_command":
					battle.start_move()
				elif battle.phase() == "move_preview":
					battle.preview_move(cursor)
			KEY_C, KEY_ESCAPE:
				_cancel()
			KEY_W:
				battle.wait_unit()
			KEY_E:
				battle.end_player_phase()
			KEY_A:
				_attack_step()
		queue_redraw()

func _confirm() -> void:
	match battle.phase():
		"player_map_idle":
			for unit in battle.living_units("player"):
				if unit.get("cell", Vector2i(-1, -1)) == cursor:
					battle.select_unit(unit.get("id", ""))
					return
		"move_preview":
			if battle.preview_cell == cursor:
				battle.confirm_move()
			else:
				battle.preview_move(cursor)
		"forecast":
			battle.confirm_attack()

func _cancel() -> void:
	match battle.phase():
		"post_move_command":
			battle.cancel_move()
		"forecast", "target_select", "weapon_select":
			battle.cancel_attack_flow()

func _attack_step() -> void:
	match battle.phase():
		"unit_command", "post_move_command":
			battle.open_weapon_select()
		"weapon_select":
			var weapons := battle.available_weapons(battle.selected_unit_id)
			if not weapons.is_empty():
				battle.select_weapon(weapons[0].get("id", ""))
		"target_select":
			for target in battle.weapon_targets_in_range(battle.selected_unit_id, battle.selected_weapon_id):
				if target.get("cell", Vector2i(-1, -1)) == cursor:
					battle.select_target(target.get("id", ""))
					return
		"forecast":
			battle.confirm_attack()

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, get_viewport_rect().size), Color(0.015, 0.020, 0.028), true)
	_draw_text("SRW-like Kernel Sandbox", Vector2(64, 54), 30, Color(1.0, 0.84, 0.22))
	_draw_text("Phase: %s    %s" % [battle.phase(), battle.last_prompt], Vector2(64, 84), 16, Color(0.82, 0.94, 1.0))
	for y in range(8):
		for x in range(12):
			var cell := Vector2i(x, y)
			var rect := _cell_rect(cell)
			draw_rect(rect, Color(0.055, 0.090, 0.105), true)
			draw_rect(rect, Color(0.20, 0.40, 0.46), false, 1)
	if battle.phase() == "move_preview":
		for cell in battle.reachable_cells(battle.selected_unit_id):
			draw_rect(_cell_rect(cell).grow(-4), Color(0.08, 0.50, 0.92, 0.32), true)
	for enemy_id in battle.enemy_intents.keys():
		var enemy := battle.get_unit(enemy_id)
		var target := battle.get_unit(battle.enemy_intents[enemy_id].get("target_id", ""))
		if not enemy.is_empty() and not target.is_empty():
			draw_line(_cell_center(enemy.get("cell")), _cell_center(target.get("cell")), Color(1.0, 0.20, 0.25), 3)
	for unit in battle.living_units():
		var fill := Color(0.18, 0.62, 0.80)
		if unit.get("team", "") == "enemy":
			fill = Color(0.80, 0.18, 0.24)
		elif unit.get("team", "") == "object":
			fill = Color(0.88, 0.68, 0.22)
		draw_rect(_cell_rect(unit.get("cell")).grow(-10), fill, true)
		_draw_text(String(unit.get("id", "")), _cell_rect(unit.get("cell")).position + Vector2(4, 18), 11, Color.WHITE)
	draw_rect(_cell_rect(cursor).grow(-2), Color(1.0, 0.84, 0.22), false, 3)
	_draw_text("Enter 选单位/确认  M移动  A攻击链  W待机  C取消  E阶段结束", Vector2(64, 650), 16, Color(0.78, 0.90, 0.96))
	if battle.phase() == "forecast":
		_draw_forecast()

func _draw_forecast() -> void:
	var rect := Rect2(760, 160, 420, 220)
	draw_rect(rect, Color(0.02, 0.026, 0.036, 0.96), true)
	draw_rect(rect, Color(1.0, 0.72, 0.24), false, 2)
	var f := battle.current_forecast
	_draw_text("Forecast", rect.position + Vector2(20, 34), 24, Color(1.0, 0.84, 0.22))
	_draw_text("Damage %d  Hit %d%%" % [f.get("damage", 0), f.get("hit_rate", 0)], rect.position + Vector2(20, 74), 18, Color.WHITE)
	_draw_text("Target HP -> %d" % f.get("target_hp_after", 0), rect.position + Vector2(20, 108), 18, Color.WHITE)
	_draw_text("Interrupt intent: %s" % ("YES" if f.get("interrupts_intent", false) else "NO"), rect.position + Vector2(20, 142), 18, Color(0.70, 1.0, 0.72))
	_draw_text("Enter confirm / C cancel", rect.position + Vector2(20, 184), 14, Color(0.72, 0.86, 0.92))

func _cell_rect(cell: Vector2i) -> Rect2:
	return Rect2(ORIGIN + Vector2(cell.x * TILE, cell.y * TILE), Vector2(TILE, TILE))

func _cell_center(cell: Vector2i) -> Vector2:
	return _cell_rect(cell).get_center()

func _draw_text(text: String, pos: Vector2, size: int, color: Color) -> void:
	draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)
```

- [ ] **Step 4: Create sandbox scene**

Create `game-godot/scenes/kernel_sandbox.tscn`:

```ini
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/kernel_sandbox_scene.gd" id="1"]

[node name="KernelSandbox" type="Node2D"]
script = ExtResource("1")
```

- [ ] **Step 5: Launch visual sandbox manually**

Run:

```bash
cd game-godot
godot --path . res://scenes/kernel_sandbox.tscn --resolution 1280x720
```

Expected:

- Native window opens.
- Grid, units, message wall, and red intent line are visible.
- Arrow keys move cursor.
- `Enter` selects a unit.
- `M` previews move.
- `A` walks weapon/target/forecast flow.
- `C` cancels post-move or forecast flow.
- `E` resolves enemy phase only after all player units are done.

- [ ] **Step 6: Commit**

```bash
git add scripts/godot-test.sh game-godot/scripts/kernel_sandbox_scene.gd game-godot/scenes/kernel_sandbox.tscn
git commit -m "feat: add SRW kernel visual sandbox"
```

---

### Task 7: Documentation, Full Verification, And Handoff

**Files:**
- Modify: `game-godot/README.md`
- Verify: `scripts/godot-test.sh`
- Verify: `game-godot/scenes/kernel_sandbox.tscn`

- [ ] **Step 1: Update `game-godot/README.md`**

Add this section after the current commands:

```markdown
## SRW-like Kernel Sandbox

The current default playable demo remains `res://scenes/main.tscn` and uses the v0.3 prototype model.

The new kernel sandbox is a separate verification scene:

```bash
cd game-godot
godot --path . res://scenes/kernel_sandbox.tscn --resolution 1280x720
```

The sandbox is intentionally small. It verifies the next runtime architecture:

- `ActionContext`: original cell, move path, selected weapon, target, forecast, commitment.
- `BattlePhaseMachine`: legal state transitions for unit command, move preview, post-move command, weapon select, target select, forecast, action end, enemy phase.
- `EnemyIntentSystem`: visible enemy intent toward a protect object.
- `CombatResolver`: deterministic forecast and result payload.
- `ScenarioEventBus`: exploration and battle events routed through shared state.

Use this before migrating Chapter 01 content into the new core.
```

- [ ] **Step 2: Run full headless verification**

Run:

```bash
./scripts/godot-test.sh
```

Expected:

- Existing smoke tests still pass.
- New line appears: `SRW kernel smoke test passed.`
- Final `rg` error scan prints no matches.

- [ ] **Step 3: Run import verification**

Run:

```bash
./scripts/godot-import.sh
```

Expected: command exits `0` and no script parse errors appear.

- [ ] **Step 4: Run manual visual verification**

Run:

```bash
cd game-godot
godot --path . res://scenes/kernel_sandbox.tscn --resolution 1280x720
```

Manual checklist:

- Select `haosi`.
- Move to `Vector2i(3, 5)` or nearby legal tile.
- Cancel movement and confirm the unit returns to original cell.
- Move again.
- Open attack flow.
- Select weapon and target.
- View forecast.
- Cancel forecast back to target select.
- Confirm attack.
- Confirm `haosi` cannot act again.
- End phase after all players are done.
- Confirm objective loses integrity if enemy intent is not interrupted.

- [ ] **Step 5: Record implementation notes**

Add a short note to `game-godot/README.md` under the sandbox section:

```markdown
### Current Kernel Boundaries

This sandbox uses deterministic combat and a tiny hardcoded content database. It does not replace the Chapter 01 v0.3 demo yet. The next migration should move real Chapter 01 exploration flags, map objects, battle events, and UI panels onto this kernel.
```

- [ ] **Step 6: Commit**

```bash
git add game-godot/README.md
git commit -m "docs: document SRW kernel sandbox"
```

---

## Self-Review Checklist

Before executing this plan, verify:

- Every new class has one responsibility.
- No task modifies `demo_v03_model.gd`.
- No task replaces the default playable `main.tscn`.
- Smoke tests cover move cancel, no-target attack, forecast cancel, attack commit, intent interruption, objective damage, and scenario event records.
- `scripts/godot-test.sh` runs the new test alongside existing tests.
- The visual sandbox is optional and isolated at `game-godot/scenes/kernel_sandbox.tscn`.

---

## Follow-Up Plans After This Passes

Once this sandbox is verified, create separate plans for:

1. **Chapter 01 Content Migration:** move real exploration scenes, map-story events, and two battles from `demo_v03_model.gd` into `ContentDB` + `ScenarioEventBus`.
2. **Main Scene UI Rebuild:** replace direct `DemoV03Model` calls in `main.gd` with a controller that consumes `BattleSession`, `PresentationQueue`, and content data.
3. **Asset And Animation Pass:** add sprite states, short attack animation, cut-in timing, objective damage effects, and better intent-line visuals.
