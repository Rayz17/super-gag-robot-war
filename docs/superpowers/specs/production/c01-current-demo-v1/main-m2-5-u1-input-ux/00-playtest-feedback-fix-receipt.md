# C01E02 M2.5-U1 Input UX Fix Receipt

Date: 2026-08-11

## Scope

- Active build: `C01CDV1-M2-R2`
- Content fingerprint: `00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4`
- Runner SHA-256: `be1c9d722398ef5d8225a028caf730ab8d9987fae86f60df184b3630d918f3bf`
- Candidate isolation guard SHA-256: `0b9b184030e0c973c0f79be1bec614791c13f0c1dc3f6699247069cdad818593`
- Dedicated input UX test SHA-256: `a073b385e8202c71827100184d80573234802db89a7cc15d1c90434cb57df8de`
- This change only repairs tactical input, command affordance, legality feedback, and player guidance.
- Canon, story, gameplay causality, AI, unit count, save schema, build identity, profile, topology, art handoffs, and default entry are unchanged.

## Player-Facing Corrections

1. Arrow keys, WASD, and gamepad D-pad now repeat while held (`0.24 s` initial delay, `0.075 s` repeat interval).
2. `Enter`/`Space` confirms the current move destination. It no longer silently ends the turn.
3. Move mode shows every legal 2x2 Guardian-Z anchor in blue, shield pickup anchors in yellow, the guard zone in green, and the planned path in cyan.
4. The large recommended-action button always follows the current tactical state: approach shield, take shield, end turn, advance east, brace, wait, or confirm shield bash.
5. Command buttons are disabled from the same backend availability contract that executes them. A rejected command reports its exact prerequisite instead of the generic “invalid” message.
6. Confirming the current tile is a no-op and does not spend movement.
7. After moving or taking the shield, the prompt tells the player to end the turn instead of requesting an impossible second action.
8. An invalid move remains cancellable/recoverable and explains that the destination is out of range, blocked, or cannot fit the 2x2 unit.
9. Candidate isolation no longer treats a held key, live stick axis, or last-input-device telemetry as persisted global state. Durable global state mutations still fail closed.

## Shortest Verified Route

1. Press the large `下一步` button to select the recommended shield pickup anchor.
2. Press `Enter` to move.
3. Press `H` or click `取盾`.
4. Press `E` or click the large `结束回合` recommendation.
5. Continue with the large recommendation until Guardian-Z reaches the green guard zone.
6. Press `B` to brace, then end turns while the final rescue vehicle clears the lane.
7. Press `F` to confirm the one-shot shield bash when prompted.

## Verification

- Dedicated front-end flow: `C01_CURRENT_CANDIDATE_M2_5_U1_INPUT_UX_OK repeat=continuous noop=preserved shield_path=guided invalid=explained transient_input=ignored durable_global=blocked`
- Tactical contract: `C01_CURRENT_CANDIDATE_M2_CONTRACT_OK replays=20 phase=P1`
- A5 Atlas contract: `C01_CURRENT_CANDIDATE_M2_5_ATLAS_OK instances=6 texture_masters=1 facings=4 movement_compare=pass loaded=6 fallback=7`
- M2.5 compatibility suite: PASS
- Full `scripts/godot-test.sh`: PASS
- Canon report/strict/authority/smoke: PASS
- `git diff --check`: PASS

## Boundaries

- No files were staged or committed.
- No real-art approval or handoff state was changed.
- The captures use the active M2.5 Current Candidate Runner and existing approved asset lane.
