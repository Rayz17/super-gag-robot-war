# 馆守 Z V10X｜E02 `shield_take/south`｜R3 分层源锁

> `Section 2 internal workbench / candidate_emitted=false / user=false / runtime=false / canon=false`

## 唯一合法馆守 Z 身份源

- 用户通过的 V10X south Camera V2 256：
  `../art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png`
- SHA-256：`d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796`
- 同谱系 RGBA master（仅供身份交叉核验）：
  `../art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/masters/GUARDIAN_Z_V10X_CAMERA_V2_CARDINAL_NEUTRAL_SHARED_MASTER_RGBA_1254.png`
- SHA-256：`3ea73fac822c7c169d2715ab95a36f549c19f330a5c02bb9c031a0ecacf9cd3a`

## 唯一合法盾牌设计源

- 用户接受的 A17 原稿：
  `../art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`
- SHA-256：`169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305`
- 同源确定性 front exterior master：
  `../art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png`
- SHA-256：`8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47`
- 同源 rear interior master：
  `../art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_REAR_INTERIOR_RGBA_MASTER_768x1152.png`
- SHA-256：`7e9db3af4e7ccf9c361edbc6ebbadf74a4c61c9281eaa62373814a8cefe6bfe0`
- 同源 rear interior 对位图（只用于背面双握把位置核验）：
  `../art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/map-candidates/A17_SHIELD_REAR_INTERIOR_MAP_CANDIDATE_256x256.png`
- SHA-256：`98aaeb90ce155dffa89b56d42c9e137aeb43a3fb061f37f079a77bfc89107be7`
- rear grip centres：left `[96.827,104.747]`，right `[134.419,104.747]`，midpoint `[115.623,104.747]`。
- 派生回执：
  `../art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/SECTION2_DERIVATION_RECEIPT.md`
- SHA-256：`d813fd753a8147c99c5785ced14a90ac383e77ebaf90a62d4dc7b249347df75d`
- 派生 metadata：
  `../art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/A17_SHIELD_FRONT_REAR_DERIVATION_METADATA.json`
- SHA-256：`776134db606903ca9da76ee42ca7b7dbcf2b0991d29b3f730fd02d2861eb2921`

## 禁止输入

- R2 失败 raw 及其任何派生像素；
- CML008 旧馆守 Z、旧 east、旧 Runtime copy；
- A2/A13/A14 弹孔装甲板；
- A18/A19/A22 失败 raw；
- 任意旧动作图、fallback、mirror 或 cross-facing 像素。

本 R3 没有读取或传入上述禁止像素。唯一盾牌编辑调用只传入已锁定的 A17 front exterior master；调用数 `1`、reroll `0`。该调用在 50%/100% 门失败并被隔离，body-only 调用数为 `0`。
