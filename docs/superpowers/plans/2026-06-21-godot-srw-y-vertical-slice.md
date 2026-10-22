# Godot SRW-Y-Inspired Vertical Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the chapter-flow debug UI with a first playable SRW-like vertical slice that shows task entry, map-story dialogue, tactical cursor play, enemy intents, forecast, short cut-in, and themed result.

**Architecture:** Keep the current Godot project, but add a focused slice model so tactical rules can be tested without rendering. `main.gd` becomes the presentation/state controller for this vertical slice, while `srw_slice_model.gd` owns units, intents, forecast, attacks, and enemy phase. Existing chapter-flow files remain as reference but are no longer the main experience.

**Tech Stack:** Godot 4.7, GDScript, SVG/PNG assets, headless Godot smoke tests, existing shell scripts.

---

## File Structure

- Create `game-godot/scripts/srw_slice_model.gd`: pure-ish tactical state for units, map cells, enemy intents, forecasts, player/enemy turns, and win/loss state.
- Create `game-godot/scripts/srw_slice_smoke_test.gd`: headless test covering initial state, forecast, attack, enemy phase, result path.
- Replace `game-godot/scripts/main.gd`: SRW-like vertical slice renderer and input state machine.
- Add `game-godot/assets/backgrounds/bg_wanji_map.svg`: painted isometric-style map backdrop.
- Add `game-godot/assets/cutins/cutin_guardian_z_first_light.svg`: short attack/cut-in art.
- Add `game-godot/assets/ui/ui_srw_hud_frame.svg`: HUD frame skin.
- Modify `scripts/godot-test.sh`: include the new smoke test.
- Modify `game-godot/README.md`: document the new controls and scope.

## Task 1: Tactical Slice Model

**Files:**
- Create: `game-godot/scripts/srw_slice_model.gd`
- Test: `game-godot/scripts/srw_slice_smoke_test.gd`

- [ ] **Step 1: Write failing smoke test**

Create `srw_slice_smoke_test.gd` that:

```gdscript
extends SceneTree

const SliceModel := preload("res://scripts/srw_slice_model.gd")

func _init() -> void:
	var model := SliceModel.new()
	model.start()
	_assert(model.phase == "map_story", "slice starts with map-story")
	model.advance_story()
	model.advance_story()
	model.advance_story()
	_assert(model.phase == "player", "story advances into player phase")
	_assert(model.units.size() >= 6, "battle has enough units and objects")
	_assert(model.current_objective().contains("留言墙"), "objective names the protected target")
	model.select_unit("haosi")
	var cells := model.reachable_cells("haosi")
	_assert(cells.has(Vector2i(3, 3)), "haosi can reach the forward lane")
	_assert(model.move_unit("haosi", Vector2i(3, 3)), "haosi can move")
	var forecast := model.forecast("haosi", "drone_a")
	_assert(not forecast.is_empty(), "forecast exists for target")
	_assert(int(forecast["damage"]) > 0, "forecast has damage")
	_assert(bool(forecast["clears_intent"]), "forecast tells if intent is cleared")
	_assert(model.attack("haosi", "drone_a"), "attack resolves")
	_assert(model.last_cutin["attacker"] == "haosi", "attack stores cut-in payload")
	model.end_player_phase()
	_assert(model.phase == "player", "enemy phase returns to player")
	_assert(model.turn == 2, "turn advances")
	print("SRW vertical slice smoke test passed.")
	quit(0)

func _assert(value: bool, message: String) -> void:
	if value:
		return
	push_error(message)
	quit(1)
```

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_slice_smoke_test.gd
```

Expected: fail because `srw_slice_model.gd` does not exist.

- [ ] **Step 3: Implement `srw_slice_model.gd`**

Implement units, objects, enemy intents, forecast, attack, and enemy phase with no rendering dependencies.

- [ ] **Step 4: Run test and verify GREEN**

Run:

```bash
cd game-godot
godot --headless --path . --script res://scripts/srw_slice_smoke_test.gd
```

Expected: `SRW vertical slice smoke test passed.`

## Task 2: SRW-like Main Scene

**Files:**
- Replace: `game-godot/scripts/main.gd`

- [ ] **Step 1: Rewrite main state controller**

States:

```text
mission -> map_story -> player -> command -> move -> target -> forecast -> cutin -> enemy -> result
```

Input:

```text
Space/Enter: advance/confirm
Arrow/WASD: move tactical cursor
Mouse: select tiles/buttons
M: move
A: attack
I: inspect/codex
E: end phase
Esc/right click: cancel
```

- [ ] **Step 2: Render SRW-like layout**

Draw full-screen map as primary visual, with:

- top phase banner
- right objective panel
- bottom unit card
- command menu
- forecast panel
- dialogue layer over map
- intent arrows and danger tiles
- short cut-in overlay
- result report

- [ ] **Step 3: Verify with screenshot**

Run:

```bash
./scripts/godot-screenshot.sh /tmp/chao-gag-srw-slice.png /tmp/chao-gag-srw-slice.log
```

Expected: first screen looks like mission/game UI, not a chapter debug panel.

## Task 3: Art Assets

**Files:**
- Create: `game-godot/assets/backgrounds/bg_wanji_map.svg`
- Create: `game-godot/assets/cutins/cutin_guardian_z_first_light.svg`
- Create: `game-godot/assets/ui/ui_srw_hud_frame.svg`

- [ ] **Step 1: Add map backdrop**

Create SVG with isometric museum floor, roads/corridors, exhibit islands, message wall, 0号侧廊, warning lights, and darker sealed corners.

- [ ] **Step 2: Add cut-in art**

Create SVG with Guardian Z silhouette, chest light, speedlines, and attack flash.

- [ ] **Step 3: Add HUD skin**

Create SVG with dark translucent cockpit-style frame, cyan/yellow accents, and hard rectangular corners.

- [ ] **Step 4: Wire assets in `main.gd`**

Load the assets through `ResourceLoader.exists()` and fall back to drawn shapes if missing.

## Task 4: Script Integration and Docs

**Files:**
- Modify: `scripts/godot-test.sh`
- Modify: `game-godot/README.md`

- [ ] **Step 1: Add smoke test to shell script**

Run `srw_slice_smoke_test.gd` after the existing model tests and scan logs for Godot errors.

- [ ] **Step 2: Update README**

Document that the current default scene is now the SRW-Y-inspired vertical slice.

- [ ] **Step 3: Final verification**

Run:

```bash
./scripts/godot-import.sh
./scripts/godot-test.sh
./scripts/godot-screenshot.sh /tmp/chao-gag-srw-slice-final.png /tmp/chao-gag-srw-slice-final.log
```

Expected: tests pass, no `SCRIPT ERROR`, screenshot shows the new slice.
