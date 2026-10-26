# A18 Call01 — VISUAL_FAIL_STOP

Date: 2026-08-23  
Status: `VISUAL_FAIL_STOP / SEALED`  
Lane: `Candidate / user=false / runtime=false / canon=false`  
ImageGen calls: `1 / 1`  
Rerolls: `0`

> **2026-08-24 authority correction:** 130 号已证实 52 号用户裁决在 C01E02 Demo scope 内覆盖了源 manifest 的 `approved=false`，所以下表 `SOURCE_AUTHORITY_FAIL` 根因不再成立。但本 raw 同时未通过 Camera V2 south、R3 BASH 首读和真 alpha，整批仍为封存 History，禁止作任何正向输入。

## Sealed raw

- File: `user-confirmation-call01/generation-raw/GUARDIAN_Z_SOUTH_R2_BLOCK_R3_BASH_CALL01_RAW.png`
- SHA-256: `778939019e375e4f9fb78dc8a52287e4003e1c183c972aa809fc9eee3d9dc3c3`
- Dimensions: `1536x1024`
- `sips hasAlpha`: `no`

## Hard-gate result

| Gate | Result | Producer first read |
|---|---|---|
| One sheet / exactly two poses | PASS | Left and right poses are clearly separated and share one GZ/shield design family. |
| Two intact arms and two visible hand contacts in each pose | PASS | Both poses show two complete arms; both hands contact the shield edge/grip zone. It is no longer a back-mounted or floating prop. |
| Shield remains in chest/abdomen front | PASS | Both poses place the shield between body and threat. |
| Current identity source authority | **FAIL** | Post-call authority audit found the supplied V10X lockframe is `approved=false`; it cannot replace the CML008 Hard `guardian-z-user-selected-base.png` identity source. |
| A17 identity | PARTIAL | R2 keeps the shield silhouette and three old scars plus red heat scar well; R3 compresses/loses the exact three-old-scar read and warps some approved face structure. |
| Camera V2 south `[-40,+24]` | FAIL | Head/chest remain too close to a straight-on presentation; the body forward axis does not read decisively toward screen down-left. Raised 3/4 top-plane information is insufficiently consistent between the two poses. |
| R3 is an unambiguous two-handed horizontal bash | FAIL | R3 reads primarily as a second angled brace; lateral sweep direction and whole-body impact transfer are not clear enough for the dedicated BASH state. |
| Genuine transparent background | **FAIL** | PNG is RGB with no alpha. The visible checkerboard is baked into the image and cannot be treated as transparency. |

## Stop decision

The source-authority error and alpha failure each independently trigger the promised stop rule. Camera and R3 readability also fail, so this raw is sealed as evidence only. No user-confirmation board is issued, because wrapping the failed image in a presentation board would falsely imply an approvable Candidate.

No second generation, no deterministic repaint/cutout, no Godot binding, no Runtime registration, no Canon migration.
