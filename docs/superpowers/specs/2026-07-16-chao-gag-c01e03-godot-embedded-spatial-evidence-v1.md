# C01E03 Godot Candidate Runtime And Embedded Spatial Evidence v1

> Status: `candidate_runtime_parity_47_verified_0_partial_0_missing`
>
> Scope: `C01E02 RT038 -> C01E03 four-node graph -> eight-stage bridge Tactical -> P6 nested Spatial -> RT035 -> C01 chapter runner`

## 1. Implemented Runtime Slice

The current Godot package compiles and runs a four-node C01E03 chain:

1. Baihan enters with a complete physical body while C01E02's RT038 snapshot remains intact;
2. an eight-stage event battle carries the inherited five people, Haosi's sourced later entry, Guardian Z's first control, Brave Fist's temporary load-bearing, the recoverable right arm, the bridge crossing, and Baihan's damaged withdrawal;
3. Tangjiao and Doudeng perform local aftercare without committing episode state;
4. the six B1 anchors lock and RT035 commits one exact 27-key snapshot.

The bridge node owns one Tactical Session from P1 through P8. P6 no longer exposes eight authored receipts as Tactical menu commands. After P5 settles at `EXPLORE_ENTRY_LOCAL`, the Tactical mode pauses its board and pushes a walkable human-scale Spatial child into Guardian Z's right forearm. A successful local result applies the eight contract actions atomically to the same battle session and resumes at P7 `PRECUT_LOCAL`.

The surrounding Tactical stages now consume the dual-plane map instead of treating it as a result illustration. Brave Fist has exactly one pre-contact move from L1 `(3,9)` to the secondary-beam anchor `(4,9)` and can cancel back before committing. Guardian Z's P5 rail strike selects Baihan's physical L1 frame. Doudeng's P7 cut exposes one correct subrib point and one non-consuming shoulder-side misread. Each of the five human crossings then records four visible states: L2 overlap, arm midpoint, L1 slider overlap, and a distinct west-safe clear cell; the two cargo crossings carry their declared companion object through the same occupancy states. Tangjiao's route is split into entry and exit actions, while the lower-person lane exposes one optional visible misstep, L2 recovery, and explicit arm-mid reentry. The three legal routes settle at exact bridge budgets of 20, 21, and 23 ticks.

Baihan exposes one data-authored structural intent at every stage. The map draws its current target and the side panel names the pressure that will be settled when the player ends the stage. Missing required work still resolves through the existing setup, explore, or post-cut local rollback rather than HP loss or a whole-battle restart.

No P1-P8 local result writes cross-episode state. Only `C01E03:RT035:ATOMIC_SNAPSHOT:V01` may persist E03 facts.

## 2. P6 Playable Spatial Contract

The right-arm interior contains eight stable objects and a four-slot search window:

- three visible but false ribs: upper cavity, outer armor beam, and heat-brittle third rib;
- one hidden unnumbered panel revealed only after all three false ribs are excluded;
- three external independent inputs: Tangjiao's short-short-long material knock, Brave Fist's load center, and Diedie's green bottom shim;
- one final fourth-rib alignment choice.

The player walks with held keyboard direction or held/clicked mouse movement, approaches physical markers, and opens authored multi-beat dialogue. Repeat interactions use short recaps rather than replaying the original sequence. Portrait presentation is active-speaker-only.

The scene preserves the following contract boundaries:

- Jicun's low-confidence body memory locates a door only; it cannot provide bridge permission;
- all three external inputs must be independently ready before public verification;
- successful verification consumes exactly four search ticks and leaves the arm repairable at `PRECUT_LOCAL`;
- closing the final dialogue without choosing consumes nothing and restores the pre-interaction registry;
- forcing the visible outline produces a local soft failure, rolls only P6 back to `EXPLORE_ENTRY_LOCAL`, and reopens a fresh Spatial child;
- Qihai is absent from the physical scene;
- Diedie is bound to canon character `CH057` and tactical mecha lifecycle `V353U038`; `CH005B` remains Acheng and is explicitly rejected by compiler regression.

## 3. Nested Mode And Save Architecture

`TacticalModeScene` owns an optional `embedded_spatial_interlude` declaration. The E03 declaration supplies the trigger stage/checkpoint, scene id, local outcome contract, and exact action bridge. While the child is active:

- outer Tactical input is blocked but the board and BattleSession stay alive;
- save captures both the outer Session and the inner stable-object registry, player position, active dialogue, notice, and final-choice rollback snapshot;
- restore recreates the child above the same stage-six Session;
- success pops only the child, applies the eight hidden battle receipts atomically, auto-ends P6, and resumes P7;
- failure restores the battle's stage-six checkpoint and opens a clean child with a visible reset explanation;
- restart and episode exit clear the child with the parent.

The dedicated smoke test proves that inspecting the first rib, suspending, restoring, failing once, retrying, and then succeeding does not duplicate search ticks, leak P6 commands, or commit RT035 early.

The outer Session also snapshots active map targeting. Automated evidence deliberately rejects beam contact from the wrong cell, cancels and repeats Brave Fist's move, probes the wrong cut point without consuming Doudeng, saves at the cut selector, saves again with Tangjiao physically at `ARM_MID`, restores both states, cancels back to the original L2 cell, and completes the crossing once.

## 4. Visual And Asset Evidence

The Spatial scene uses a 1672x941 pixel-art-inspired production candidate background showing a giant forearm interior, human-scale service rails, structural ribs, tendon bundles, heat damage, an access panel, and the torn opening toward the external recovery rail. Object markers and the player remain legible without hiding the mechanical scale.

Final image-generation brief:

> Create a polished pixel-art-inspired 16:9 game background showing the human-scale interior of a giant robot's severed right forearm: enormous curved structural ribs, bundled tendon cables, heat-brittle white residue, an unnumbered access panel, a torn opening toward an external recovery rail, and maintenance catwalks and railings for scale. Use a dark industrial palette with cyan work lights and warm amber maintenance lights. No characters, text, logos, or UI; preserve readable space for game interaction markers.

Tool: OpenAI image generation.

Project asset:

- `game-godot/assets/backgrounds/story_first/bg_c01e03_right_arm_interior_v01.png`

Four visually inspected 1280x720 frames are archived under `outputs/c01e03-embedded-spatial-v01/`:

- `01-right-arm-entry.png`
- `02-memory-finds-door-only.png`
- `03-external-material-knock.png`
- `04-three-external-inputs-ready.png`

The visual pass caught and fixed two runtime-only presentation faults: the newly generated PNG could be unavailable before Godot's editor import pass, and the third external input overlapped the nearby-object heading. The mode now has a development-source image fallback and fixed vertical tracks for all three information groups.

Ten 1280x720 Tactical frames are archived under `outputs/c01e03-story-first-production-v2/tactical/`:

- `01-p1-baihan-intent.png` and `01b-p2-haosi-real-name-cutin.png` show the opening pressure and Haosi's sourced entry;
- `02-p4-brave-contact-goal.png` shows the one-cell beam anchor and reversible move command;
- `03-p5-rail-strike-target.png` and `03b-p5-rail-strike-presentation.png` show physical targeting and the flying-fist spectacle;
- `03c-p6-scale-descent.png` and `03d-p6-scale-ascent.png` show the continuous 18 m body -> 5 m forearm -> human-scale inspection -> bridge-map return;
- `04a-p7-cut-main-tendon-cutin.png` shows the irreversible human decision;
- `04b-p7-tangjiao-bridge-motion.png` shows an interpolated L2-to-arm movement with its start, destination and route;
- `04-p7-tangjiao-arm-mid.png` shows Tangjiao occupying the bridge midpoint while the next L1 overlap is highlighted.

The second visual pass removed the false phase-menu fallback during target selection, separated enemy intent from other status text, and added a fixed map-target legend so giant unit art cannot hide the next interaction cell.

## 5. Current Verification

Current E03 bundle fingerprint:

```text
c88501d940d59766b84052275489f4b8fc54a673dd55f1c8206774bfa1b23581
```

The following checks pass:

- `compile_multi_play_content.gd` with 21 C01E03 resources;
- `multi_play_content_compiler_smoke_test.gd`;
- `c01e03_bridge_session_smoke_test.gd`;
- `c01e03_embedded_spatial_smoke_test.gd`;
- `c01e03_story_first_episode_integration_smoke_test.gd`;
- `c01_story_first_chapter_runner_smoke_test.gd`;
- `multi_play_presentation_shell_smoke_test.gd`;
- `python3 scripts/check_c01e03_runtime_graybox.py`.
- `python3 scripts/check_c01e03_godot_runtime_parity.py` (`47 verified / 0 partial / 0 missing`).

The integration test proves that the P6 child returns to the same Session at P7, search tick equals four, the fourth rib is verified and still repairable, all eight Tactical stages remain nonpersistent, aftercare precedes the lock, and RT035 commits exactly once with 27 facts. Compiler regression additionally locks eight stage intents, Brave Fist's one-cell movement, physical rail-strike targeting, four generic four-state crossings, Tangjiao's split entry/exit, and the optional lower-person recovery sequence. The dedicated parity matrix now binds all 47 Runtime rows to current source, direct tests, and machine-checked evidence tokens.

## 6. Remaining Gap

This evidence proves the current candidate playable mapping, nested P6 architecture, and 47/47 Runtime logic parity. It does not prove final commercial-demo production quality. Remaining work includes:

- convert the remaining P1 support allocation, P3 lane selection, and most P4 Owner checks from actor-selected command rows into richer physical previews or short presentation interactions without obscuring their professional responsibility order;
- add production-grade Baihan ruler/retractor hazard animation and bridge-load feedback; the current scale transition and receipt-driven bridge motion are spatially explicit but do not yet form a full autonomous movement/combat animation pass;
- replace reused E01 narrative backgrounds, procedural tactical geometry, SVG placeholders, and limited unit states with E03 production assets and animation;
- give the complete episode a human pacing, comprehension, controller, failure-recovery, and capacity play receipt rather than relying on automated completion;
- validate Windows/export behavior, production GPU captures, and saved-game compatibility across content revisions;
- promote the candidate implementation to production only after the asset-state matrix, human play evidence, save migration, and platform checks agree.

Do not use this document to claim that C01E03's formal art, full Tactical choreography, human capacity, or platform acceptance is complete. Use it to preserve the verified 47-row candidate logic, four-node graph, map-bound bridge interactions, nested Spatial behavior, local rollback, RT035 boundary, identity fix, and visual candidates from regression.
