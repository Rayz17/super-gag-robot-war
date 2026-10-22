# D04-P1 Fixture v0.2 hash-bound declared-event ledger

Status: `Candidate / zero_build / human_not_run / user_not_decided`

This directory is a static, machine-readable **declared-event ledger** for the first neutral tactics paper fixture. It is deliberately independent from Canon, Reader, Runtime, the C01E02 Demo, Godot scenes, UI and formal assets.

## What these files prove

- `world.json` fully names the 14×10 topology, two-cell-wide main bridge, three allied test bodies, five enemy test bodies, three vehicles, gate, bridge and sample.
- `rules.json` fixes the 0.5-second tick, 8-second window, 32-second deadline, one 16-action allowlist, common physics and the A/B/C/D adapter boundary.
- `ai-objective.json` gives each enemy deterministic priorities, cell-by-cell route variants, tie-breaks and fallbacks.
- `traces.json` instantiates all 20 clock references and two four-window regression seeds.
- `save-log-schema.json` fixes the minimum stable snapshot, event and receipt fields.
- `manifest.json` binds the package with canonical-JSON SHA-256 values.

The reference checker replays events already declared in `traces.json`; it does **not** derive those events from plans. In particular it is not yet the common movement/contact/reaction/object-ownership resolver, a pathfinding AI, a game Build, a balance solver, a fun test, a UI prototype or a human-playtest receipt. The two registered seeds are mutually non-dominated only within their three recorded outcome axes. They do not prove that a third mixed plan cannot dominate both. Bounded search is still required, and the seeds do not prove that either family is executable by the future resolver, discoverable, balanced or enjoyable.

The ledger files are bound with raw-file SHA-256; semantic state/event hashes use canonical JSON. The checker and external A/B/C/D vector table are also bound. No real save serialization/restore round trip has run.

Current honest result: `HASH_BOUND_DECLARED_EVENT_LEDGER_PASS / RESOLVER_NOT_IMPLEMENTED / NO_GO_UNTIL_PLAN_TO_EVENT_RULES_EXIST`.

## Run

From the package root:

```bash
python3 scripts/check_d04_p1_v0_2.py
python3 scripts/check_d04_p1_v0_2.py --self-test
```

Both commands are read-only.
