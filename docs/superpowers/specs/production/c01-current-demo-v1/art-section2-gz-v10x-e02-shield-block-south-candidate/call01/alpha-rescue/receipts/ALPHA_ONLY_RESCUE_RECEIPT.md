# GZ V10X E02 Shield Block South — Call01 Alpha-only Rescue Receipt

- status: `ALPHA_ONLY_RESCUE_TECHNICAL_PASS_USER_REVIEW_PENDING`
- authority: `Candidate`
- previous Call01 `candidate_created=false`: unchanged
- this receipt: independent deterministic Alpha-only rescue; not additional generation and not retroactive promotion of the prior failed delivery
- user_accepted: `false`
- runtime_allowed: `false`
- default_allowed: `false`
- canon_migrated: `false`
- godot_binding_written: `false`

## Corrected input lock

- raw PNG: `../generation-raw/GZ_V10X_E02_SHIELD_BLOCK_SOUTH_CALL01_RAW_FAIL_RGB_1254.png`
- raw PNG SHA-256: `cebbb904d3504e54d76ac3d00f8328fb8c4d8bb3fda155d2ae3d7e2114d6270f`
- the previously supplied `f72ed9a8291f0ea55ab21f57c5841fdced844790e761a5e1691fb5bb071ebb78` belongs to `../receipts/CALL01_DELIVERY_HASHES.sha256` itself; it is not used as the PNG lock

## Deterministic treatment

Only four-edge-connected checker inference, Alpha extraction, edge-band checker despill, premultiplied one-time map scaling, pivot registration, QA composition, and hashing were used. No ImageGen, Blender, repainting, silhouette modification, pose modification, global white key, legacy asset input, or Godot binding was used.

The checker model is derived only from known-clean top/left margins. Its maximum accepted model residual is `5.5`. The foreground is the largest non-background connected component. Subject pixels at least `4 px` inside the silhouette are a protected core; only the partial-Alpha edge band is unblended against the modeled checker.

## Delivered pixels

- transparent master: `../masters/GZ_V10X_E02_SHIELD_BLOCK_SOUTH_ALPHA_RESCUE_RGBA_MASTER_1254.png`
  - `1254x1254`, RGBA8, hasAlpha=`true`
  - Alpha bbox, exclusive: `[267,71,1007,1134]`
  - transparent pixels: `1,050,778`
  - partial-Alpha pixels: `11,670`
  - opaque pixels: `510,068`
- Camera V2 Candidate: `../map-candidate/GZ_V10X_E02_SHIELD_BLOCK_SOUTH_CAMERA_V2_CANDIDATE_RGBA_256.png`
  - `256x256`, RGBA8
  - pivot: `[128,224]`
  - footprint: `2x2`
  - registered Alpha bbox, exclusive: `[55,16,201,224]`
  - visible size: `146x208`
  - clipped Alpha pixels: `0`

## Alpha and RGB audit

- internal protected-core RGB changed pixels: `0`
- opaque-subject RGB changed pixels: `0`
- edge RGB changed pixels: `11,670`
- edge-change bbox, exclusive: `[267,71,1007,1134]`
- preserved neutral-white protected-core pixels: `2,734`
- outside-foreground nontransparent pixels: `0`; outside-transparent=`true`
- transparent components, 8-connected: `1`; enclosed transparent components: `0`
- opaque checker-scale contamination components: `0`
- the white A17 shield surface remains intact; no global white key was applied

The transparent exterior component reaches all confirmed real negative spaces visible between the crown/limbs/shield-body silhouette. No closed checker-background island remains in the Alpha topology.

## Visual hard-gate readback

- `front-visible-hand-count=0`
- `rear/interior contact visually occluded, user review pending`
- V10X body, A17 exterior shield face, south elevated pose, head crown, shield point, and both feet remain present
- black, white, magenta, green, transparency-check, map-50%, and internal-hole-mask QA were visually inspected for checker squares and edge loss

Independent read-only pixel review additionally confirmed that the protected light/white shield core contains `38,508` pixels with `alpha=255` and `RGB changed=0`. The 256 resize has `92` ultra-low-Alpha Lanczos fringe pixels in `63` tiny components within `2 px` of the main silhouette (`max alpha=5/255`); they are invisible on the supplied saturated-background QA and are not checker remnants. This observation is retained rather than hidden or promoted as a stricter single-component Alpha guarantee.

This is a technical Alpha pass only. It does not upgrade the asset to user acceptance, Runtime, Default, or Canon. Producer/user actual-pixel review remains required.
