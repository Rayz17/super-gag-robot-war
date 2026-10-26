# Task 68 R0.1 completion report

Status: `deterministic display-scale sweep delivered / Candidate only / producer selection pending / runtime_allowed=false`

## Fixed inputs

- Task 68 SHA-256: `ac9b42a1ddc187ac9dc1f17251736c1321c517b7936fa50fc89dc2d39c1a5797`
- Current production board SHA-256: `a289d00095b9a2787f2186c66615e4a4357f78ecd420202d34b4b601b3019619`
- Guardian Z exact C128 SHA-256: `d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e`
- BREAKER exact B128 SHA-256: `e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4`
- A4 central viewport SHA-256: `b8ccc9b6eefb802b929a6d674e668611c6d9a88e123e24a2991710ae7e5f4ea9`

## Mechanical method

- Guardian Z: full 128×128 frame → 256×256 at exactly 2.0×, Pillow `NEAREST`.
- BREAKER: full 128×128 frame → 320/384/448 at exactly 2.5×/3.0×/3.5×, Pillow `NEAREST`.
- No alpha-bbox crop; no aspect-ratio change; no independent movement of head, shell, limbs, or center of gravity.
- All lanes use the same map, Guardian Z anchor `(382, 434)`, BREAKER anchor `(688, 505)`, fixed 2×2/3×3 annotations, and scaled bottom-center pivots.
- The script asserts that every resized RGBA value already exists in the corresponding exact source, preventing interpolated colors.

## Comparison metrics

Guardian Z fixed target alpha bbox: `204×242`.

| option | BREAKER frame | scale | target alpha bbox | B/GZ width / height | right-UI / topbar clearance | lane occlusion |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A | 320 | 2.5× | 265×275 | 1.30× / 1.14× | 80 / 164 px | LOW |
| B | 384 | 3.0× | 318×330 | 1.56× / 1.36× | 53 / 109 px | MEDIUM |
| C | 448 | 3.5× | 371×385 | 1.82× / 1.59× | 27 / 54 px | HIGH |

These are display-scale and screen-occupancy measurements, not world-position, event-staging, final Sprite, Atlas, or Runtime claims.

## Delivered files

- `R0_1_SCALE_SWEEP_A4_3840x720.png` — three independent 1280×720 A4 lanes concatenated without resampling.
- `R0_1_SCALE_DECISION_BOARD_1920x1080.png` — three native crops with alpha-bbox, footprint, clearance, occlusion, and first-read annotations.
- `scale-sweep.tsv` — source/target frame, bboxes, pivots, anchors, footprints, and lane notes.
- `delivery-hashes.sha256` — hashes for every R0.1 deliverable except itself.

## Zero-operation attestation

- ImageGen: `0`
- Blender: `0`
- redraw / cleanup / paint-over / detail completion / outline: `0`
- sharpening / denoise / color change: `0`
- reads from temporary generated_images: `0`
- Atlas / Godot / Runtime / LibTV / Canon migration: `0`
- git add / commit: `0`

`producer_scale_selection=PENDING_320_384_448`

Machine checks do not select an option or approve final art. Work stops at the producer review gate.
