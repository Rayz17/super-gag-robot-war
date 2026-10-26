# Brave Fist E03 Idle South — Call01 Completion Receipt

## Verdict

- production verdict: `PASS_FOR_USER_VISUAL_REVIEW`
- authority: `Candidate`
- user accepted: `false`
- runtime allowed: `false`
- default allowed: `false`
- canon migrated: `false`
- Godot binding / `res://` copy: `false`
- machine PASS does not constitute user visual acceptance.

## Generation boundary

- built-in ImageGen calls: `1/1`
- rerolls: `0`
- sole positive visual input: `BF_A33_USER_ACCEPTED_IDENTITY`
- prior north FAIL_STOP trace used: `false`
- Blender / Three.js / procedural mecha drawing: `false`
- postprocess: deterministic checker-background removal, Alpha/despill, contain scaling, pivot registration and QA only.

## Visual self-review

- A33 identity: `PASS`. The orange-gold solid-body hero robot, short/wide V antenna, mechanical tiger-mane crown, paired massive closed fists, wide hips, round knees and load-bearing lower body remain legible at 256 and 50%.
- south Camera V2 heading `[-40,24]`: `PASS`. Feet, load axis, torso, face and crown read toward screen lower-left while elevated front/top planes remain visible.
- paired-fist constraint: `PASS`. The near fist is larger from three-quarter perspective, but the far fist remains a clearly paired closed heavy fist; there is no single elongated arm mutation.
- 2x2 map volume / pivot: `PASS`. Visible bbox is `[58,16,199,224)`, visible size `141x208`, and pivot `[128,224]` sits between the feet immediately below the lowest visible pixel.
- clipping: `PASS`; `clipped_alpha_pixels=0`.
- residual review note: at 50% the lower-left heading is subtler than at 100%, so final acceptance remains an actual-pixel user decision.

## Alpha and RGB audit

- high-resolution master: `1254x1254 RGBA8`
- transparent pixels: `1,031,552`
- partial-Alpha pixels: `11,908`
- opaque pixels: `529,056`
- Alpha bbox: `[201,58,993,1225)`
- enclosed transparent negative-space components: `3`
- opaque checker components: `0`
- pixels outside foreground with nonzero Alpha: `0`
- internal core RGB changed pixels: `0`
- opaque RGB changed pixels: `0`
- edge-only RGB changed pixels: `11,908`, bbox `[201,58,993,1225)`
- transparent pixels with nonzero RGB: `0`

## Exact deliverables

- raw trace: `generation-raw/BRAVE_FIST_E03_IDLE_SOUTH_CALL01_RAW_RGB_1254.png`
- transparent master: `masters/BRAVE_FIST_E03_IDLE_SOUTH_CALL01_RGBA_MASTER_1254.png`
- 256 candidate: `map-candidate/BRAVE_FIST_E03_IDLE_SOUTH_CAMERA_V2_CANDIDATE_RGBA_256.png`
- Alpha QA: `qa/BRAVE_FIST_E03_IDLE_SOUTH_100PCT_4BACKGROUND_ALPHA_QA.png`
- 50% map-scale QA: `qa/BRAVE_FIST_E03_IDLE_SOUTH_50PCT_CAMERA_V2_SCALE_QA.png`
- machine audit: `receipts/CALL01_ALPHA_SCALE_MACHINE_AUDIT.json`
- delivery hashes: `receipts/CALL01_DELIVERY_HASHES.sha256`

Stop gate: Candidate actual pixels await user visual review. No downstream consumer integration is authorized.
