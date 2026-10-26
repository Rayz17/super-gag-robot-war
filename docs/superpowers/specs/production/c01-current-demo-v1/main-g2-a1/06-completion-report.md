# C01E02 G2-A.1 Completion Report

## Disposition

`G2-A.1 internal readiness: PASS`

This closes the correction gate for map performance consumers, three-device interaction, A/B round-two constraints, AudioServer routing, and fixture-only semantic consumers. It does **not** approve real art, U2, G2-B, a user-facing visual Demo, or promotion to the default Runtime.

Current classification:

| Layer | Result |
|---|---|
| Shared-round domain | PASS, retained from G2-A |
| UI/input runtime skeleton | PASS for internal readiness |
| Map performance consumers | PASS with fixture-only evidence |
| Audio buses and timing | PASS with generated audio fixtures |
| Semantic consumer shape | PASS with generated image/audio fixtures |
| Real asset exact binding | NOT EXECUTED; `real_art_loaded=0` |
| Integrated visual playtest / U2 | BLOCKED |
| G2-B | BLOCKED by producer gate |

## Implemented

### Map and presentation

- Projection is `tile_half=(40,20)` with A4-compatible origin `(-880,-170)`.
- The 32x18 map remains larger than the viewport; edge threshold now gates smooth scrolling.
- Round one plays on one persistent map and one set of actor nodes:
  - T1 emergency vehicle crosses the landing area.
  - T2 swarm follows its frozen route; Guardian Z route/reaction plays and the swarm survives.
  - T3 Guardian Z and BREAKER move into contact, hit-stop, directional shake, flash, recoil, debris, and aftermath.
  - T4 an independent city-artillery beam hits exposed side armor.
  - T5 road damage persists while BREAKER begins red charging.
- Event focus is derived from each contact/event anchor, not the planning cursor.
- Full, Skip, and fallback restore the same semantic result, camera context, and round-two entrance.

### Planning and input

- Protection zones, charge corridor, contest cells, all five T anchors, target anchors, authored route, waypoints, 2x2 endpoint ghost, and final-facing fan are drawn in the tactical world.
- All five frozen intents in rounds 1-3 have a drawable route, area, or target anchor.
- Summary stays over the visible map and states protected subject, contact timing, main/prepared action, route/waypoints/endpoint, final facing, fallback, exposed risk, timing, and heat.
- Keyboard, mouse, and gamepad each cover planning entry, waypoint editing, facing, action/prepared choice, summary open/return, visible 0.7 second hold, cancel, and commit.
- Invalid map actions are translated to player-facing Chinese and do not expose resolver tokens.
- Command drawer and summary buttons have explicit focus navigation.

### A/B consequences

- Strategy A enters round two with four timing beats, a long-road-break risk zone, damaged security pressure, and projected heat 56/90 on its accepted route.
- Strategy B enters round two with one timing beat, a swarm-pressure risk zone, only zero remaining margin after its accepted route, and projected heat 88/90.
- Route-cost cells, pressure anchors, timing, and heat are visible in the map, HUD, and commit summary and are consumed by the resolver. These remain convergent Candidate constraints, not permanent story branches.

### Audio and semantic consumers

- Runtime-only buses exist for BGM, AMBIENT, VOICE, IMPACT, and DEBRIS/MACHINERY.
- Giant contact performs true pre-contact bus mute, simultaneous four-layer start, 6dB BGM/ambient ducking, and exact aftermath restoration.
- Thirty-nine generated fixture slots bind to live hosts: 6 map, 5 unit/object, 4 FX, 9 screen, and 15 audio consumers.
- Bad fixture media fails only its slot; identity-critical fallback keeps `integrated_visual_playtest_ready=false`.
- No art directory scan, handoff probe, historical asset, A8/A9 file, or real asset load occurs.

## Evidence

- Specialized gate: `scripts/test_c01e02_m3_golden_slice_g2_a1.sh` PASS.
- Domain replay: 40 deterministic replays covering A/B plus container-reorder invariance PASS.
- Full Godot regression: PASS; see `logs/50-full-regression.log`.
- Canon report and strict: PASS.
- Canon authority and smoke: PASS.
- V35 layered dashboard: current.
- `git diff --check`: PASS.
- Internal capture: 9 frames for Public, Edit, Summary, T1-T5, and round-two entry; see `captures/C01E02_G2A1_RUNTIME_CAPTURE_RECEIPT.json`.

The PNGs are classified `internal_fixture_validation_only`; they must not be shown as user-facing art or visual-quality evidence.

## Isolation audit

- Default main scene remains `res://scenes/startup_router.tscn` and default M2 routing is untouched.
- `project.godot`, startup router/selector, save/profile, Canon, Reader, and formal Runtime are unchanged.
- No media files exist in the Golden Slice runtime content lane.
- `approved_handoffs=[]`, `probe_count=0`, `real_art_loaded=0`, `user_visual_playtest_eligible=false`.
- No files were staged or committed.

## Stop point

Work stops at the producer gate. Next work requires producer-authorized P1 exact handoff for approved identity and environment assets, followed by real-loader integration and U2. G2-B, real art integration, default-entry replacement, and complete E02 expansion were not started.
