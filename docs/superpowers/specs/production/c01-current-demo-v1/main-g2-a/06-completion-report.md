# C01E02 G2-A Golden Slice internal completion report

## Result

`G2-A internal engineering PASS` at the exact producer stop defined by objective 58.

This result proves the non-default Golden Slice code path can run a deterministic three-round shared-resolution loop with formal UI components, camera/input plumbing, data-driven presentation cues, concurrent audio consumers and fail-closed semantic asset slots. It does **not** prove final UI quality, visual appeal, game feel or an integrated user Demo because no approved art or audio was loaded.

## Implemented slice

The new implementation lives only under `m3_golden_slice` and does not replace the existing default M2 Runner.

1. Round 1 resolves the first giant contact from one shared pre-state. Strategy A intercepts the collision; strategy B protects the lane with a prepared response.
2. The A/B result materially changes all seven required Round 2 inputs: Guardian position, heat, BREAKER depth, road damage, warning facility state, swarm positions and remaining timing margin.
3. Round 2 takes the wall-hung shield, blocks the red impact and only then permits the final vehicle to pass and clear the rescue lane.
4. Round 3 derives the contextual shield bash from route, body position, final facing, shield state and timing. A valid result reaches P1 with BREAKER alive after its first knockdown; it does not write mission clear.

Preview and execution call the same pure resolver. Draft editing is zero-write; returning from the confirmation summary preserves the draft; the 0.7-second hold can be cancelled without mutation; retry restores the exact round pre-state and intents. Route hashes are based on the actual authored waypoint route, and event/mutation counts are derived from emitted receipts.

## Interaction and presentation shell

- Godot `Control`, `Container` and `Theme` nodes provide the planning HUD, command drawer, threat cards, five-step timeline and returnable commit summary.
- Keyboard hold, mouse selection and gamepad input feed the same route/facing/action draft model.
- The tactical camera uses a configurable central safe zone, smooth threshold scrolling and world-bound clamping on a map larger than the viewport.
- Giant contact, red shield block and shield bash each use data-driven camera, anticipation, hit-stop, directional shake, flash, recoil and aftermath cues.
- Full, Skip and missing-media fallback restore the same gameplay state, map focus and semantic result.
- The audio director exposes independent impact, debris, machinery, voice, BGM and ambient channels, including BGM/ambient ducking. Missing formal audio marks presentation as not ready instead of synthesizing user-facing sound.

## Asset boundary

The semantic manifest pre-registers the required map, unit, shield, character, cut-in, FX, SFX, BGM and ambient slots. Every slot remains `runtime_allowed=false`; approved handoffs are empty. The resolver does not scan directories or probe old assets, and a malformed handoff fails closed per slot.

Current evidence is therefore:

- `real_art_loaded=0`
- `real_art_probes=0`
- `integrated_visual_playtest_ready=false`
- no fixture screenshot or capture was produced for user judgment

## Verification

- G2-A domain contract: PASS, three rounds, two materially distinct strategies, 40 deterministic replays.
- Session flow: PASS, returnable summary, 0.7-second hold, cancel/retry and three round receipts.
- UI/input/camera contract: PASS, formal controls, threshold camera and continuous input.
- Presentation/asset contract: PASS, three cue families, at least four concurrent audio layers, zero real-art probes and U2 false.
- Specialized G2-A suite: PASS.
- Existing M3-J1 G1 regression: PASS.
- Default startup smoke: PASS; default remains `C01CDV1-M2-R2` and explicit legacy routes remain available.
- Full Godot test suite: PASS.
- Canon Godot report/strict, authority and smoke checks: PASS.
- JSON, shell syntax and scoped whitespace checks: PASS.

No files were staged or committed.

## Deliberately unfinished

- No A8, story-first, old portrait/unit, old receipt or art-workspace file was selected, loaded or displayed.
- No real image, atlas, cut-in, FX, music, ambience or voice asset was integrated.
- No default-entry replacement, formal save, Runtime promotion, Reader/Canon change, LibTV work or complete E02 expansion was performed.
- No G2-B work was started, and no user-facing visual-quality claim is made.

## Stop

Work stops at the producer gate. The next permitted step is the approved Gold Frame plus producer-signed exact handoff, followed by a separately authorized G2-B real-asset integration and 45-75 second Golden Turn capture.

