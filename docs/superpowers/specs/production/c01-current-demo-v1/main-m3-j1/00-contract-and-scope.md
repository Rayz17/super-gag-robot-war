# C01E02 M3-J1 G1 + M1a contract receipt

## Frozen authority

- Producer plan: `48-c01e02-m3-j1-current-art-and-gameplay-joint-producer-plan.md`
  - SHA-256: `06592d45483496247f915313fd22b6f28a4b392b1a073e2960f271d0af16eb35`
- Main objective: `50-c01e02-m3-j1-common-turn-core-and-real-consumer-objective.md`
  - SHA-256: `6690773d4f3cf9182769336b72e84c87d1df4f3cf0017b2e86cc184ffd2f8deb`
- Joint build: `C01CDV1-M3-J1-G1-M1A`
- Rules profile: `c01cdv1_e02_shared_round_m3_j1`
- Fixture asset profile: `c01cdv1_e02_m3_j1_fixture_lane_v1`
- Topology: `baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`

Both contract hashes were checked before implementation and again by the specialized test runner.

## Scope actually used

Only the new `m3_j1` content, scripts, scene, tests, isolated fixtures, `scripts/*m3_j1*`, and this `main-m3-j1` evidence directory were written.

The existing default M2 Runner, startup selector/router, R0/R0.5, project settings, save/profile code, Canon, Reader, A4/A5 runtime bytes, art workspaces, old handoffs and formal Runtime were not modified by this task.

## Claim boundary

- G1 is a non-default, save-disabled, representative single-round gameplay sandbox.
- M1a is an exact-handoff loader and real Godot consumer validation using deterministic synthetic fixtures only.
- `real_art_handoff=none`, `approved_real_handoffs=0`, `runtime_art_loaded=false`.
- This is not U2, not a complete E02, not Runtime promotion and not a visual-quality review build.
