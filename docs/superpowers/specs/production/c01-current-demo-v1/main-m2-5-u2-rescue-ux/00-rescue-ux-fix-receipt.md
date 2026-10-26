# C01E02 M2.5-U2 Rescue UX Fix Receipt

Date: 2026-08-11

## Diagnosis

The battle state was completable, but the player-facing contract was misleading:

- `intercept` only attacks a small body adjacent to Guardian-Z, while the BREAKER red impact is stopped by `brace`; both were presented with language that could be read as the same interception task.
- Rescue vehicles advanced only during enemy resolution after the red impact was blocked. The UI exposed only an incomplete checkbox, not route progress or remaining turns.
- The locked automated route used one small-body intercept, while the large in-game recommendation skipped it entirely.

## Corrections

1. `拦截 [P]` is renamed `击退小体 [P]` and its disabled reason explicitly says it cannot block the red impact.
2. The BREAKER intent panel says `应对：立盾 [B]` before impact.
3. The recommended UI route teaches exactly one legal adjacent-small-body intercept before continuing east.
4. The rescue lane exposes deterministic route progress: completed legs, total legs, evacuated vehicles, remaining turns, and lowest vehicle HP in the session API.
5. After the red impact, the intent panel and large action both state how many enemy turns remain and that `E` advances evacuation; small-body elimination is not the objective.
6. The underlying combat causality, unit positions/count, deadline, enemy AI, save schema, build identity, content fingerprint, asset lane, and Canon are unchanged.

## Verified Front-End Route

`取盾 -> 第2回合击退一次贴身小体 -> 向东推进 -> 绿色区立盾 -> 挡下赤红冲击 -> 撤离路线 2/4 -> E -> 撤离路线 4/4 -> 盾拍授权`

Marker:

`C01_CURRENT_CANDIDATE_M2_5_U2_RESCUE_UI_OK guided_route=complete intercept=taught rescue_progress=visible rescue_lane=cleared finisher=ready`

## Core Hashes

- Tactical session: `b81117259d449b9620c79a863f40e05f30c5afa34335b4db6b983bf8f154ba53`
- Runner: `e669188f25996a2038bb1e6112dd8145f36f71f29e5287b0bfbc684aa2e3555d`
- Rescue UI flow test: `7c32c32110f12a85d5378dbfed8b559afeba29abeb3d253ed52fc61e8e363393`
- Capture driver: `bd81960abdeec12cf12e36c5b55ef8fac6973edb183c466995e72dca53b68b3d`

## Verification

- U1 input UX regression: PASS
- U2 full recommended UI route: PASS
- Three 1280x720 deterministic captures: PASS
- M2 tactical contract, including 20 deterministic replays: PASS
- M2.5 compatibility and asset fail-closed suite: PASS
- No files staged or committed.
