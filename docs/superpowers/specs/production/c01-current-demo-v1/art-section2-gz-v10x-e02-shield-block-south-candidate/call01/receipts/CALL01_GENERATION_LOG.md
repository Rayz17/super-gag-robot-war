# Call01 generation log

- target: `GZ_V10X_E02_SHIELD_BLOCK_SOUTH`
- date: `2026-08-25`
- generator: built-in `imagegen` skill
- imagegen_calls: `1`
- rerolls: `0`
- result: `FAIL_STOP_TRANSPARENCY`
- raw: `../generation-raw/GZ_V10X_E02_SHIELD_BLOCK_SOUTH_CALL01_RAW_FAIL_RGB_1254.png`
- raw_sha256: `cebbb904d3504e54d76ac3d00f8328fb8c4d8bb3fda155d2ae3d7e2114d6270f`

## Authority split

- Hard: `CML008` global E02 two-arm heavy-shield state; scoped `CML130` makes V10X the sole positive C01E02 visual parent.
- Working: `V353U001` current lifecycle identity and `CML128` KINETIC_CEL production language.
- Candidate: matrix row `E02_GZ_SHIELD_BLOCK_S`; this exact action sprite did not previously exist and this call did not produce an eligible Candidate sprite.
- History / forbidden: old Guardian Z visual pixels, A13/A18/A19/A22, R2 failed pose pixels, A37 and BREAKER. None were supplied to the call.

## Locked positive inputs

| Role | Path | SHA-256 |
| --- | --- | --- |
| V10X Camera V2 shared identity/body parent | `docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/masters/GUARDIAN_Z_V10X_CAMERA_V2_CARDINAL_NEUTRAL_SHARED_MASTER_RGBA_1254.png` | `3ea73fac822c7c169d2715ab95a36f549c19f330a5c02bb9c031a0ecacf9cd3a` |
| Accepted cardinal direction/registration receipt | `docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/receipts/CALL01_USER_ACCEPTED_CAMERA_V2_CARDINAL_BASE_RECEIPT.md` | `0cc5c78d514acd6060201578d1fc3613510d9ef0c8e6b70f92c905598363edcb` |
| A17 exterior/front | `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png` | `8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47` |
| A17 rear/interior handle topology only | `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_REAR_INTERIOR_RGBA_MASTER_768x1152.png` | `7e9db3af4e7ccf9c361edbc6ebbadf74a4c61c9281eaa62373814a8cefe6bfe0` |

The R2 receipt SHA `1659ef8184e978d6eb2129655f46308a9a917b263bf2a47435bcb60d180bffd8` was read only to lock the negative rule `front=0 / rear=2`; no R2 image or pose was opened or supplied.

## Matrix lock

- matrix_sha256: `8583fd046a4a57a580474eb2aee24862ada32ce1884c03d2868cb0eb89665a22`
- camera: `CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`
- facing/screen vector: `south / [-40,+24]`
- requested canvas/pivot/footprint/scale: `256x256 / [128,224] / 2x2 / [1,1]`

No 256 derivative, pivot registration, alpha extraction, QA composite, Godot binding, Runtime, Default, or Canon promotion was performed after the hard failure.
