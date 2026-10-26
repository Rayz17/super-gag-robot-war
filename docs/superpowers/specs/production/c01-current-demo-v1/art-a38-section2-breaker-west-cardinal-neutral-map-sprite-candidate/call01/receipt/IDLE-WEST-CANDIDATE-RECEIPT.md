# BREAKER Camera V2 idle/west — Candidate visual-gate receipt

- Status: `CANDIDATE_PENDING_PRODUCER_ACTUAL_PIXEL_REVIEW`
- Consumer key: `ENEMY_C01_BREAKER|idle|west`
- Contract: `384x384 RGBA`, footprint `3x3`, pivot `[192,320]`, west screen axis `-149.0362°`
- Generation budget: `1/1`; reroll: `0`
- Godot/Atlas/Runtime/Canon binding: `0`

## Positive inputs

- Current north map identity/scale base: `breaker_north_camera_v2_candidate.png`
  - SHA-256: `6b20111c80e3dc76adb5a05b55395359b7d1bdc2ec189060859058e53dbffde1`
- GF PLAN/CONTACT were used only for human comparison of the approved long-leaf shell, low red slit and load-bearing language. They were not used as map pose, background, scale or registration pixels.
- A37 and every other matrix-listed forbidden-history asset contributed zero asset bytes, pixels, geometry or prompt references.

## Actual outputs

- Raw: `generation-raw/BREAKER_A38_CALL01_IDLE_WEST_RAW.png`
  - SHA-256: `0a87b9fe134778f5f221ad206500c1f363a5d83c7ce6c6059c1bdf73d726435d`
  - Generator returned `1254x1254 RGB` with a baked neutral checker, so it is retained as raw evidence and is not the map candidate.
- Transparent map candidate: `map-candidate/BREAKER_A38_IDLE_WEST_CAMERA_V2_CANDIDATE_384.png`
  - SHA-256: `0e01e320a7c8c84c4e56cb7614bd33609a9a4a322e8c1f680b1767ee5a7ca9f0`
  - Mechanical operations only: checker removal/despill, largest connected subject isolation, one proportional premultiplied-alpha resample, bottom-center registration.
  - RGBA bbox: `(16,19)-(367,320)` = `351x301`; current north bbox is `(16,16)-(367,320)` = `351x304`.
- 100%/50%/silhouette/direction board: `qa/BREAKER_A38_IDLE_WEST_100_50_DIRECTION_REVIEW.png`
  - SHA-256: `34eb63ee593406475fd57acec09a7d4ea7b8d881aca73b743c679c06f5c555b7`

## Honest self-review

- First read: same low-slung BREAKER family identity, single low red slit, four load-bearing limbs and a large asymmetric leaf-shell mass remain readable.
- Camera/facing: the head/front reads toward screen upper-left and the shell flow returns toward lower-right; top planes remain visible in the elevated Camera V2 reading. This is newly drawn west-facing art, not a flipped or rotated north bitmap.
- Map scale: visible width exactly matches current north and visible height differs by three pixels; the registered bottom center is `[192,320]`. At 50%, the red slit and shell flow remain readable.
- Residual visual risk: the new west view consolidates some dorsal plates into a broader central blade than the current north/GF views. Whether that is acceptable physical continuity of the same asymmetric shell must be decided from actual pixels by the producer/user; machine geometry does not approve it.

Stop gate: no east/south/action expansion and no Godot consumption before producer visual acceptance of this exact west Candidate.
