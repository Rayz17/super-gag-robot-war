# Task98 runtime grid registration completion correction

Authority: Task102 `e8556f917456da83d933842b9ace9542f5238635d5166a6f5b7adbfad0d62378`.

Status: `MACHINE_PASS / EXECUTOR_VISUAL_INSPECTION=PASS_TERRAIN_AND_FOOTPOINT_SINGLE_RUNTIME_COORDINATE_SYSTEM / AWAITING_PRODUCER_ACCEPTANCE / CALL03_FALSE / CALL04_FALSE`

## Corrected scope

- `cell_diamond(x,y)` now treats integer `(x,y)` as the runtime cell center.
- `polygon_for_rect([x,y,w,h])` now uses `[x-0.5,y-0.5]..[x+w-0.5,y+h-0.5]`.
- Only the actor-free guide and PLAN composite 100%/50% were re-exported.
- Their pre-fix bytes are retained under `_history/task102-pre-runtime-grid-correction/` with exact Task102 SHAs and disposition `History_invalid_runtime_registration`.

## Independent readback

- Five runtime projection controls: max error `0.0px`.
- Six PLAN actor footpoints: max error `0.0px`; each corrected board marker center was sampled at the expected pixel.
- Selection pocket and BREAKER charge avenue polygon vertices: max error `0.0px`.
- Three rendered terrain cell-center samples match the runtime-derived center pixels.

## Frozen-byte proof

- Both local Guardian/BREAKER geometry guides: byte-identical.
- Five C3 frozen contracts: byte-identical.
- Every other pre-existing top-level Task98 file outside the explicit correction allowlist: byte-identical.

## Boundary

ImageGen=0; no new visible target pixel; no Call03/04; no board/interface/Canon/Godot/Runtime write. Machine PASS does not claim producer visual acceptance. Stop at producer registration review.
