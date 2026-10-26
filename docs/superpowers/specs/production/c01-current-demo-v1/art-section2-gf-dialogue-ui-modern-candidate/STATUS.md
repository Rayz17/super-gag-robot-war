# Section 2 GF Dialogue UI Modern Refit

Status: `SIX_COMPONENTS_BOUND_TO_C01_CANDIDATE_HUD / READABILITY_AND_LAYOUT_VISIBILITY_TESTED / AWAITING_ACTUAL_FRAME_USER_GATE`

- User accepted direction: `true`
- Candidate HUD adoption authorized: `true`
- Component visual acceptance: `false`
- Internal component visual gate: `pass_for_isolated_test_only`
- Test-only consumption allowed: `true`
- C01 Candidate HUD consumption: `true`
- Runtime allowed: `false`
- Canon allowed: `false`
- Positive visual references: approved `GF_PLAN` / `GF_CONTACT` hierarchy and color relationship only
- Rejected Call01 pixels used: `false`
- Current stage: six deterministic true-alpha components are SHA-bound to the formal C01 Candidate HUD; B06/E07 action inserts remain independently unbound and all Runtime/Default/Canon promotions remain false
- Post-binding full-chain visual evidence: `game-godot/captures/c01_breaker_full_demo_runs/run_modern_candidate_hud_gui_20260825_01/` (`16` real Godot GUI frames; `user_visual_acceptance=false`)
- Readability/layout evidence: `game-godot/captures/c01_breaker_full_demo_runs/run_modern_hud_readability_gui_20260825_01/` (`16` real-input Godot GUI frames; main dialogue `23px`; secondary copy at least `13px`; remote/map-wide layouts hide the unused local-scene frame; action-insert layouts retain it)
- Automated coverage: all `35` story beats were checked with AUTO off/on for `70` typography states and `70` component-visibility states across `action_insert`, `remote_comms`, and `map_wide`
- Stop gate: the checks above prove implementation behavior only. They do not approve the UI as Runtime/Default/Canon and do not approve B06/E07 or any actual frame on the user's behalf
