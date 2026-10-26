# Task 67 R0 completion report

Status: `R0 mechanical reuse evidence delivered / Candidate only / runtime_allowed=false / producer visual review required`

## Delivered proof

- `GUARDIAN_Z_C128_APPROVED_EXACT.png`: exact byte copy; SHA-256 `d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e`.
- `BREAKER_B128_APPROVED_EXACT.png`: exact byte copy; SHA-256 `e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4`.
- `R0_EXISTING_APPROVED_SOURCES_ON_A4_MAP_1280x720.png`: A4 central viewport plus only the two exact 128 samples at native 1:1; labels and footprint/pivot annotations are review evidence, not event positions.
- `R0_SOURCE_ROLE_BOARD_1920x1080.png`: mechanical thumbnail layout of responsibility sources, Candidate painting layers, and History action evidence.
- `source-freeze-receipt.tsv`: every consumed governance, visual, approval, and map source with path, expected/actual SHA, authority role, allowed use, and forbidden use.

## Exact-copy and pivot checks

- Guardian Z source/output SHA match: `PASS`; 128×128 RGBA; alpha bbox `(13, 6, 115, 127)` (right/bottom exclusive), 102×121, 8443 nonzero-alpha pixels.
- BREAKER source/output SHA match: `PASS`; 128×128 RGBA; alpha bbox `(11, 6, 117, 116)` (right/bottom exclusive), 106×110, 8719 nonzero-alpha pixels.
- Guardian Z source manifest states `foot-center pivot` but has no integer coordinate. R0 uses `(64,127)` derived from the alpha-bbox bottom edge and labels that inference; it is not presented as a source-spec value.
- BREAKER source `candidate-spec.tsv` explicitly states `bottom_center` and `ground_center_128=(64,116)`; R0 uses that coordinate.

## Native 1:1 scale finding

`native_1x_30m_18m_scale_proven=false`

Both approved samples are fixed 128×128 canvases. At native 1:1, BREAKER is only 106px wide vs Guardian Z 102px, and is 110px high vs Guardian Z 121px. It therefore does **not** visibly prove the near-30m/18m relationship. Per Task 67 §4.4, R0 did not stretch, rescale, redraw, outline, or reconstruct either sample to force a pass.

`scale_gate=DEFERRED_NOT_PROVEN`

`next_round_target_display_size=pending_producer_calibration`

The 2×2/3×3 diamonds only annotate approved footprint responsibilities. They do not repair the display-size gap and do not claim actual event staging.

## Zero-operation attestation

- ImageGen calls: `0`
- Blender calls: `0`
- new identity/body design: `0`
- visible mecha pixel drawing, completion, paint-over, outline, or reconstruction: `0`
- reads from `.codex/generated_images`: `0`
- execution/modification of `build_p0_sprite_first_evidence.py`: `0`
- Godot/Atlas/Runtime/LibTV/Canon migration: `0`
- git add/commit: `0`

Machine checks do not constitute visual approval. Work stops at the producer R0 PNG review gate.
