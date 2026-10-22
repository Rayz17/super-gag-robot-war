# Noncombat Layer Demo Iteration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the Chapter Kernel Demo so story, exploration, notebook management, and battle read as separate SRPG modes, with continuous exploration movement.

**Architecture:** Keep `KernelChapterFlow` as the chapter state source, add a small `ExploreMovementController` for hold-to-walk behavior, and upgrade `kernel_chapter_demo_scene.gd` presentation/input without touching battle rules. Notebook data is exposed from `KernelChapterFlow` so it can be tested headlessly.

**Tech Stack:** Godot 4.7, GDScript, existing smoke scripts under `game-godot/scripts`.

---

### Task 1: Continuous Exploration Movement

**Files:**
- Create: `game-godot/scripts/core/explore/explore_movement_controller.gd`
- Create: `game-godot/scripts/explore_movement_controller_smoke_test.gd`
- Modify: `scripts/godot-test.sh`

- [ ] **Step 1: Write failing smoke test**

Test that holding an axis moves across multiple updates, mouse-hold target moves toward a point, release stops movement, and bounds clamp the avatar.

- [ ] **Step 2: Implement controller**

Add a `RefCounted` movement controller with `position`, `bounds`, `speed`, `set_axis()`, `set_mouse_target()`, `clear_mouse_target()`, and `update(delta)`.

- [ ] **Step 3: Wire test into `godot-test.sh`**

Run `godot --headless --path . --script res://scripts/explore_movement_controller_smoke_test.gd`.

### Task 2: Notebook Data Mode

**Files:**
- Modify: `game-godot/scripts/core/scenario/kernel_chapter_flow.gd`
- Create: `game-godot/scripts/kernel_notebook_smoke_test.gd`
- Modify: `scripts/godot-test.sh`

- [ ] **Step 1: Write failing smoke test**

Test `open_notebook(tab)`, `close_notebook()`, tab names, objectives, clues after exploration, people records, and log entries.

- [ ] **Step 2: Implement notebook API**

Add `previous_mode`, `notebook_tab`, `open_notebook()`, `close_notebook()`, `notebook_tabs()`, and `notebook_entries(tab)`.

### Task 3: Scene Presentation Split

**Files:**
- Modify: `game-godot/scripts/kernel_chapter_demo_scene.gd`
- Modify: `game-godot/README.md`

- [ ] **Step 1: Replace tap movement with continuous movement**

Use `ExploreMovementController` in `_process()`, `Input.is_key_pressed()`, and mouse press/release.

- [ ] **Step 2: Add notebook scene**

Draw a full-screen notebook with tabbed objectives, clues, people, log, settings. `N` opens/closes; `Left/Right` changes tabs.

- [ ] **Step 3: Reduce exploration dashboard clutter**

Draw exploration as a large small-scene view with contextual hotspots and bottom dialogue. Move checklists and logs into notebook.

- [ ] **Step 4: Verify**

Run all smoke tests, parse the scene headlessly, then screenshot `explore`, `notebook`, and `battle` preview modes.
