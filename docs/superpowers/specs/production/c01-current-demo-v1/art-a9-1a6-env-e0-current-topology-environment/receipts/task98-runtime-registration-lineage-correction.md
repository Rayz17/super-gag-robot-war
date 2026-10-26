# Task98 runtime registration lineage correction

Authority: Task102 producer receipt `e8556f917456da83d933842b9ace9542f5238635d5166a6f5b7adbfad0d62378`.

## Downgraded to History trace only

1. `CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png` — terrain grid is +20px screen Y.
2. `PLAN_SLOT_COMPOSITE_QA_1280x720.png` — correct footpoints over invalid terrain registration.
3. `PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png` — invalid composite derivative.

None of those pixels was opened or consumed by Task101 as registration proof.

## Still inherited as numeric contracts

- 32x18 grid; integer grid coordinate is cell center; tile half 40x20.
- raw origin [-880,-170]; world canvas 2400x1350 at raw origin [-1760,-340].
- map viewport [0,58,1280,584].
- NO_FOCUS / PLAN / CONTACT_A / CONTACT_B camera centers, exact crops, and layer top-left values.
- z and layer ownership rules independent of the invalid guide pixels.

## Fresh Task101 readback

Five distinct grid points were recomputed through grid -> raw -> canvas -> each of four camera screens. All twenty rows have 0.000000px error; see `registration-control-points.tsv` and `camera-registration-receipt.json`.
