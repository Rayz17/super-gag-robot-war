# Brave Fist E03 Return Overload Fist South — Call01 Completion Receipt

## Verdict

- production verdict: `PASS_FOR_USER_VISUAL_REVIEW`
- output id: `BRAVE_FIST_E03_RETURN_OVERLOAD_FIST_SOUTH`
- authority: `Candidate`
- user accepted: `false`
- runtime allowed: `false`
- default allowed: `false`
- canon migrated: `false`
- Godot binding / `res://` copy: `false`
- machine PASS and internal visual PASS do not constitute user visual acceptance.

## Generation boundary

- built-in ImageGen calls: `1/1`
- rerolls: `0`
- sole positive visual input: `BF_A33_USER_ACCEPTED_IDENTITY`
- A13/A16/A26/A34/A35/A37 or old Brave Fist pixels used: `false`
- Blender / Three.js / procedural mecha drawing: `false`
- postprocess: deterministic checker-background removal, Alpha/despill, contain scaling, pivot registration and QA only.

## Visual review

- A33 identity: `PASS`. The short wide V crown, hero face, mechanical tiger-mane layers, solid orange-gold chest/abdomen, wide hips, round knees, load-bearing legs and stable feet remain clear.
- paired heavy fists / symmetric base structure: `PASS`. Both are the same closed black segmented fist core, orange-gold gauntlet and cyan/gold compression-ring family. The leading fist is enlarged by action foreshortening; the rear fist and full arm chain remain visible and are not a unilateral mutation.
- non-idle relay-release action: `PASS`. The lower-left fist drives forward while the other fist remains cocked and stabilizing; both forearm rings remain traceable at 256.
- Camera V2 south `[-40,+24]`: `PASS`. Feet, load axis, torso and punch share a clear upper-right to lower-left direction; elevated top planes remain visible.
- 2x2 map volume / pivot: `PASS`. Sprite bbox is `[25,16,230,224)`, visible size `205x208`, and pivot `[128,224]` sits immediately below the visible foot baseline.
- clipping: `PASS`; `clipped_alpha_pixels=0`.
- residual user-review risk: `MAP_50PCT_ASYMMETRY_READ_RISK`. At 50%, the leading fist dominates while the rear fist and its compression ring become smaller cues. The frame still reads as a south relay punch rather than idle, but the paired-fist mechanism is clearer on the 100% board.

## Alpha and RGB audit

- high-resolution master: `1254x1254 RGBA8`
- transparent pixels: `974,854`
- partial-Alpha pixels: `12,552`
- opaque pixels: `585,110`
- Alpha bbox: `[48,56,1192,1211)`
- enclosed transparent negative-space components: `3`
- opaque checker components: `0`
- pixels outside foreground with nonzero Alpha: `0`
- internal core RGB changed pixels: `0`
- opaque RGB changed pixels: `0`
- edge-only RGB changed pixels: `12,552`, bbox `[48,56,1192,1211)`
- transparent pixels with nonzero RGB: `0`

## Exact deliverables

- raw trace: `generation-raw/BRAVE_FIST_E03_RETURN_OVERLOAD_FIST_SOUTH_CALL01_RAW_RGB_1254.png`
- transparent master: `masters/BRAVE_FIST_E03_RETURN_OVERLOAD_FIST_SOUTH_CALL01_RGBA_MASTER_1254.png`
- 256 candidate: `map-candidate/BRAVE_FIST_E03_RETURN_OVERLOAD_FIST_SOUTH_CAMERA_V2_CANDIDATE_RGBA_256.png`
- Alpha QA: `qa/BRAVE_FIST_E03_RETURN_OVERLOAD_FIST_SOUTH_100PCT_4BACKGROUND_ALPHA_QA.png`
- 50% map-scale QA: `qa/BRAVE_FIST_E03_RETURN_OVERLOAD_FIST_SOUTH_50PCT_CAMERA_V2_SCALE_QA.png`
- machine audit: `receipts/CALL01_ALPHA_SCALE_MACHINE_AUDIT.json`
- delivery hashes: `receipts/CALL01_DELIVERY_HASHES.sha256`

Stop gate: Candidate actual pixels await user visual review. No downstream consumer integration is authorized.
