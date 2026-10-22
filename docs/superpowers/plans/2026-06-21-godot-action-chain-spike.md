# Godot Action Chain Spike Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an isolated Godot 4.7 spike that proves SRW-like tactical action chaining: move preview, confirm move, cancel move, post-move command, forecast, attack, wait, and unit done.

**Architecture:** Create a tiny standalone Godot project under `experiments/oss_spikes/srpg_action_chain/`. Keep tactical rules in a pure-ish `ActionChainModel` so headless tests validate behavior without rendering, then add a minimal Node2D scene to visualize the chain.

**Tech Stack:** Godot 4.7, GDScript, headless smoke tests, drawn 2D UI only.

---

## File Structure

- Create `experiments/oss_spikes/srpg_action_chain/project.godot`: standalone Godot project.
- Create `experiments/oss_spikes/srpg_action_chain/scripts/action_chain_model.gd`: grid, units, action states, move preview, cancel, forecast, resolve.
- Create `experiments/oss_spikes/srpg_action_chain/scripts/action_chain_smoke_test.gd`: headless tests for action-chain rules.
- Create `experiments/oss_spikes/srpg_action_chain/scripts/main.gd`: small visual controller for cursor, panels, and command prompts.
- Create `experiments/oss_spikes/srpg_action_chain/scenes/main.tscn`: Node2D scene using `main.gd`.
- Create `scripts/godot-action-chain-test.sh`: convenience test runner.
- Create `scripts/godot-action-chain-screenshot.sh`: screenshot runner for the spike.

## Task 1: Headless Rule Test

**Files:**
- Create: `experiments/oss_spikes/srpg_action_chain/scripts/action_chain_smoke_test.gd`
- Create later: `experiments/oss_spikes/srpg_action_chain/scripts/action_chain_model.gd`

- [ ] **Step 1: Write the failing test**

Test behavior:

```gdscript
extends SceneTree

const ActionChainModel := preload("res://scripts/action_chain_model.gd")

func _init() -> void:
	var model := ActionChainModel.new()
	model.start()
	_assert(model.mode == "select", "starts in select mode")
	_assert(model.select_unit("alpha"), "alpha can be selected")
	_assert(model.mode == "unit_command", "selecting unit opens unit command")
	_assert(model.preview_move(Vector2i(3, 2)), "can preview legal movement")
	_assert(model.mode == "move_preview", "preview enters move_preview")
	_assert(model.confirm_move(), "can confirm move")
	_assert(model.mode == "post_move_command", "confirming move opens post-move command")
	_assert(not model.preview_move(Vector2i(4, 2)), "cannot move again after confirmed move")
	_assert(model.cancel_move(), "can cancel confirmed move before final action")
	_assert(model.get_unit("alpha")["cell"] == Vector2i(1, 2), "cancel returns alpha to origin")
	_assert(model.preview_move(Vector2i(3, 2)), "can preview movement again after cancel")
	_assert(model.confirm_move(), "can confirm movement again")
	var forecast := model.forecast_attack("drone")
	_assert(not forecast.is_empty(), "forecast exists after moving into range")
	_assert(int(forecast["damage"]) == 4, "forecast damage is stable")
	_assert(model.resolve_attack("drone"), "attack resolves")
	_assert(model.mode == "select", "attack returns to select mode")
	_assert(not model.select_unit("alpha"), "done unit cannot be selected again")
	_assert(model.select_unit("beta"), "other ready unit can act")
	_assert(model.preview_move(Vector2i(2, 3)), "beta can preview movement")
	_assert(model.confirm_move(), "beta can confirm movement")
	_assert(model.wait_unit(), "beta can wait")
	_assert(model.all_players_done(), "all player units are done")
	print("Action chain smoke test passed.")
	quit(0)

func _assert(value: bool, message: String) -> void:
	if value:
		return
	push_error(message)
	quit(1)
```

- [ ] **Step 2: Run test to verify RED**

Run:

```bash
cd experiments/oss_spikes/srpg_action_chain
godot --headless --path . --script res://scripts/action_chain_smoke_test.gd
```

Expected: fail because `action_chain_model.gd` does not exist.

## Task 2: Tactical Action Model

**Files:**
- Create: `experiments/oss_spikes/srpg_action_chain/scripts/action_chain_model.gd`

- [ ] **Step 1: Implement minimal model**

Model states:

```text
select
unit_command
move_preview
post_move_command
forecast
```

Unit fields:

```text
id, name, team, cell, hp, max_hp, move, ready, moved, original_cell, weapons
```

Rules:

- `select_unit` only accepts ready player units.
- `preview_move` only works before the unit has confirmed movement.
- `confirm_move` stores `original_cell`, moves unit, marks `moved`, and enters `post_move_command`.
- `cancel_move` returns to `original_cell`, clears `moved`, and returns to `unit_command`.
- `forecast_attack` requires target in range.
- `resolve_attack` applies damage and marks unit done.
- `wait_unit` marks unit done.

- [ ] **Step 2: Run test to verify GREEN**

Run:

```bash
cd experiments/oss_spikes/srpg_action_chain
godot --headless --path . --script res://scripts/action_chain_smoke_test.gd
```

Expected: `Action chain smoke test passed.`

## Task 3: Minimal Visual Scene

**Files:**
- Create: `experiments/oss_spikes/srpg_action_chain/scenes/main.tscn`
- Create: `experiments/oss_spikes/srpg_action_chain/scripts/main.gd`

- [ ] **Step 1: Create visual controller**

Show:

- 8x6 grid.
- Two player units and one enemy.
- Cursor.
- Move range in blue.
- Attackable target in red.
- Right command panel.
- Bottom event line.

Controls:

```text
Arrow keys: cursor
Enter/Space: confirm
M: preview move to cursor
C: cancel confirmed move
A: forecast/attack selected target
W: wait
R: reset
```

- [ ] **Step 2: Verify scene opens**

Run:

```bash
cd experiments/oss_spikes/srpg_action_chain
godot --headless --path . --quit-after 1
```

Expected: no script errors.

## Task 4: Runner Scripts

**Files:**
- Create: `scripts/godot-action-chain-test.sh`
- Create: `scripts/godot-action-chain-screenshot.sh`

- [ ] **Step 1: Add test runner**

`scripts/godot-action-chain-test.sh` runs the headless smoke test and fails on Godot errors.

- [ ] **Step 2: Add screenshot runner**

`scripts/godot-action-chain-screenshot.sh` launches the spike and captures the window using the existing screenshot style.

- [ ] **Step 3: Final verification**

Run:

```bash
./scripts/godot-action-chain-test.sh
./scripts/godot-action-chain-screenshot.sh /tmp/chao-gag-action-chain-spike.png /tmp/chao-gag-action-chain-spike.log
```

Expected: test passes and screenshot shows the action-chain prototype.
