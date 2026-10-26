# C01E02 G1.1 Joint Art Alignment Completion Report

> Status: `candidate_previs_g1_1_s01_occluder_corrected / producer_overlay_recheck_pending / D1-D3_pending`
>
> Contract: `C01CDV1-G1 / 1.0.0`
>
> Snapshot: `fe7a0764d11f5ac5f9d11accb7398df664132b0b`
>
> Content fingerprint: `944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`
>
> Runtime permission: `false` for every deliverable

## Scope completed

- Preserved the original PV01 clean plate and Camera A/B/C review images byte-for-byte.
- Preserved `PV01_S01_EVAC_WORLD_coordinate-lock.tsv`; the Camera B overlay source now masks y=0..54 and y=648..720 as text-free HUD safe bands while keeping the middle world anchors unchanged.
- Final point correction: the foreground occluder now matches the producer exactly at world `Rect(1025,400,110,270)` / Camera B screen `Rect(705,310,110,270)`.
- Rebuilt only PV05 to the producer program's isometric projection and `C01CDV1_JOINT_S06_T2_STAGE1_V1` gameplay state, with the six exact program button rectangles.
- The PV05 overlay source contains geometry only: board, affected cells, both silhouettes, shield, panel boundaries, and button rectangles; all art-side annotations are absent.
- The previously corrected PV05, PV05 overlay source, 36-second Animatic, self-check, shot list, and audio were hash-protected and not regenerated in this final S01-only pass.
- PV02/PV03/PV04/PV06, identity/contact sheets, source receipt, and placeholder audio were not regenerated.

## Delivery inventory

- Artifact rows: `20` in `asset-manifest.tsv`.
- New S01 overlay source and both PV05 outputs: `1280x720`.
- Coordinate lock: tab-separated world/screen/shot alignment evidence.
- Animatic: `1280x720`, 24 fps, 36 seconds, procedural placeholder audio.

## Boundaries preserved

- No Godot, Canon, producer contract, source manifest, or runtime files were modified.
- No external generation service or video-generation service was used.
- No design promotion, identity lock, Runtime promotion, or batch derivative was created.
- All seven frozen visual inputs are still covered by the unchanged `source-validation-receipt.tsv`.
- Every protected G1/G1.1 file, including both S06 outputs and the Animatic, was hash-checked before and after the S01-only correction.
- All outputs remain `runtime_allowed=false` and are for composition/overlay review only.

## User decisions still open

- D1: approve or reject the oblique shallow-X/Y exploration presentation.
- D2: approve or reject V10X as the Demo derivation base.
- D3: approve or reject the tactical pose puzzle read.

Internal technical completion is not user visual acceptance. Stop after the G1.1 S01 occluder correction and wait for the producer pixel-overlay recheck plus D1-D3 decisions.
