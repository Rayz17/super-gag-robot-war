# M3-J1 direct play instructions

Run the non-default sandbox from the project root:

```bash
scripts/run_c01e02_m3_j1_sandbox.sh
```

The default no-argument Demo remains `C01CDV1-M2-R2`; this command directly opens the isolated J1 scene.

## Controls

1. Read the five frozen intents and press `Enter`.
2. Hold arrow keys or `WASD` to move the cursor continuously.
3. Press `Enter` or left-click to append the current cell as a waypoint. Earlier route segments remain intact.
4. Press `Backspace`, `Delete`, or right-click to remove the last waypoint segment.
5. Press `Q/E` to choose final facing independently from the route.
6. Press `1` for `BODY_REDIRECT`, `2` for the declared trigger-to-response preparation, or `3` for `HOLD_EXIT`; action and preparation are exclusive.
7. Press `F` to cycle the declared fallback, then `Tab` to inspect the complete commit summary.
8. Press `Esc` to return from the summary without changing the world, or hold `Space/Enter` to commit.

Two successful examples are `(18,10) + south + 1` and `(19,9) + east + 2`. The sandbox also accepts valid but causally losing plans and explains the uncovered responsibility before and after commitment.

The story stops after the first giant contact is redirected, city artillery hits the exposed side armor, and BREAKER begins gathering red light. The shield stays wall-hung, the rescue lane stays active, and no P1/checkpoint is written.
