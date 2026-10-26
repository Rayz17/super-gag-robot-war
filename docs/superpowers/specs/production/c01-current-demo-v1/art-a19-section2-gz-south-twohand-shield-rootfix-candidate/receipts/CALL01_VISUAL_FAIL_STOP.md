# A19 Call01 — VISUAL_FAIL_STOP

Date: 2026-08-23  
Status: `VISUAL_FAIL_STOP / SEALED`  
Lane: `Candidate / user=false / runtime=false / canon=false`  
Built-in ImageGen calls: `1 / 1`  
Rerolls: `0`

> **2026-08-24 scope correction:** 本稿使用的 CML008 旧视觉路由已被 130 号在 C01E02 Demo scope 明确退为 History/crosscheck-only。原 Camera V2 south、BASH 和 alpha 失败结论不变，且本 raw 不得再作馆守 Z 身份、姿态或 ImageGen 正向输入。

## Sealed raw

- File: `user-confirmation-call01/generation-raw/GUARDIAN_Z_CML008_SOUTH_R2_BLOCK_R3_BASH_CALL01_RAW.png`
- SHA-256: `6b2adb4feb4394845f9362414ea4015e80d1e8ec350efe36e930f0853c75db7e`
- Dimensions: `1536x1024`
- `sips hasAlpha`: `no`

## Hard-gate result

| Gate | Result | Producer first read |
|---|---|---|
| CML008 identity only | PASS | Helmet, gold horn/brow language, star-bearing red/blue chest, round shoulder drums, worn dark body and asymmetric original forearms now read as the Hard identity rather than V10X/QSD. |
| A17 shield identity only | PASS | Both poses retain the dedicated shield silhouette, crown/spine/thick rim, blue/ivory/gold palette, three old silver scars and fourth red thermal scar. |
| Two intact original arms / two hand contacts | PASS | Both poses show two complete original arms; each hand visibly contacts a shield grip/edge. No back-mounted or floating prop. |
| R2 BLOCK | PASS | Left pose clearly reads as planted frontal protection with the body behind the shield. |
| Camera V2 south `[-40,+24]` | FAIL | R2 head/chest/feet remain substantially straight-on and symmetrical; R3 also does not establish one common body-forward axis toward screen down-left. The requested raised south cardinal is not uniquely readable without the guide arrow. |
| R3 horizontal BASH | FAIL | Right pose reads as a crouched forward push/thrust with the shield still upright, not the guide's laterally swept broadside silhouette. It is not a unique reusable `BASH` action state. |
| Genuine transparent background | **FAIL** | PNG is RGB with `hasAlpha: no`; the visible checkerboard is baked into the pixels. |

## Stop decision

The guide solved the identity-source drift and improved hand contact, but it did not force the generated output through the south-camera, BASH-silhouette or alpha gates. Any one failure requires sealing; all three are present.

No second call, no reroll, no extraction/repaint, no user-confirmation board, no Godot/Runtime binding and no Canon migration.
