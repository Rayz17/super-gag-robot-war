# A17 退役重盾｜Section 2 正反面确定性 Sprite 派生回执

> Status: `USER_ACCEPTED_DESIGN_BASE_DERIVED_MAP_SPRITE_REVIEW_ONLY`
>
> `design_base_user_accepted=true`
>
> `derived_sprite_actual_frame_user_acceptance=false`
>
> `runtime=false / canon=false / godot_bound=false`
>
> ImageGen: `not called`

## 1. 本轮边界

本轮只从用户已接受的 A17 raw 中分离盾牌自身的两个同源表面：

1. `front_exterior`：朝向敌方的盾正面，保留盾冠、向下收尖轮廓、钝厚边框、中央承力脊、三道旧宽浅擦压痕及第四道赤红热痕；没有握把，也没有手。
2. `rear_interior`：朝向馆守 Z 的盾背面，保留双握把、前臂承力轨、中央与周边框架；没有手。

唯一源文件：

`../user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`

SHA-256：`169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305`

未读取或使用 A2、A13、A14、A18、A19、A22 的像素；未重画、补画、转视角或调用 ImageGen。

## 2. 正确朝向与层级硬门

- 馆守 Z 正面与盾牌 `front_exterior` 必须同向面敌。
- 馆守 Z 位于盾背后；手只能从内侧握住 `rear_interior` 的两个握把。
- 盾正面不得出现手、握把或把馆守 Z 画成从盾前方持盾。
- `front_exterior` 与 `rear_interior` 是同一面盾的互补表面，不是两面独立盾。
- 同一时刻只能有一个视觉 owner：墙挂状态，或未来使用真正获准馆守 Z 源图制作的持盾 composite；不得另挂一份 composed 独立 prop 造成重影。

## 3. 确定性像素门

提取方法为：在锁定的左右源窗口中取 `alpha > 0` 的最大 8 邻接组件；Master 只把该组件的原始 RGBA 像素原样复制到透明画布。Map Candidate 只做预乘 Alpha 的 Lanczos 缩放。

| 门 | front exterior | rear interior |
| --- | ---: | ---: |
| 源内 Alpha 组件数 | 78 | 89 |
| 选中最大组件像素 | 443,395 | 316,457 |
| 丢弃的断开微粒像素 | 155 | 142 |
| Master 活跃 RGBA 与源逐像素一致 | PASS | PASS |
| Master Alpha 组件数 | 1 | 1 |
| 256 Map Alpha 组件数 | 1 | 1 |
| 上下左右边缘 Alpha 像素 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| 第二视图残留 | 0 | 0 |
| 烘入背景 | 0 | 0 |
| 主体裁边 | 0 | 0 |

结论：`PASS_DETERMINISTIC_SPRITE_EXTRACTION_ONLY`。这只证明像素分离和透明画布成立，不证明 Camera V2 持盾姿态或实机画面成立。

## 4. 交付文件

### 高分辨率 RGBA Master

- `masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png`
  - SHA-256 `8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47`
  - Alpha bbox `[41,68,726,1084]`
- `masters/A17_SHIELD_REAR_INTERIOR_RGBA_MASTER_768x1152.png`
  - SHA-256 `7e9db3af4e7ccf9c361edbc6ebbadf74a4c61c9281eaa62373814a8cefe6bfe0`
  - Alpha bbox `[113,126,655,1026]`

### 256×256 Map 检查候选

现有 GroundMap 的馆守 Z 对象合同为 `canvas=[256,256] / pivot=[128,224] / footprint=2×2`，所以本轮没有另造 320×320 合同；两张盾图使用同尺寸透明画布，长轴归一为 208 px，盾尖登记在 `[128,224]`。

- `map-candidates/A17_SHIELD_FRONT_EXTERIOR_MAP_CANDIDATE_256x256.png`
  - SHA-256 `447f29510ec5c19b9ad44d01741e30d3b55875f047c124bc89d078458d5b9bbe`
  - Alpha bbox `[58,16,198,224]`
  - 赤红冲击外缘 socket `[170.818,96.457]`
- `map-candidates/A17_SHIELD_REAR_INTERIOR_MAP_CANDIDATE_256x256.png`
  - SHA-256 `98aaeb90ce155dffa89b56d42c9e137aeb43a3fb061f37f079a77bfc89107be7`
  - Alpha bbox `[65,16,190,224]`
  - 左／右握把中心 `[96.827,104.747]`、`[134.419,104.747]`
  - 双握把中点／held attachment pivot `[115.623,104.747]`

`nominal_sprite_scale=[1,1]` 只用于盾牌自身检查。相对 18 m 馆守 Z 的暂定 held scale 为 `[0.40,0.40]`，但必须等真正获准的新馆守 Z Master 出现后，以实际帧重新量尺；当前不得把该数值晋升为 Runtime 合同。

### QA

- `qa/A17_SHIELD_FRONT_EXTERIOR_ALPHA_DARK_LIGHT_QA_100PCT.png`
  - SHA-256 `99f3d53c49911071a9ce2a56567792477bff67669fa44ce62b7bb6a901b1f438`
- `qa/A17_SHIELD_REAR_INTERIOR_ALPHA_DARK_LIGHT_QA_100PCT.png`
  - SHA-256 `df82cbd61118146e5d597386f190132f694c964781622dcebf7c9787e0b5dba4`
- `qa/A17_SHIELD_FRONT_REAR_DARK_LIGHT_QA_50PCT.png`
  - SHA-256 `61da1e19b51a86e40616109a3528b378edaf9612e6a7e06112e7a6706c58e2f9`
- `A17_SHIELD_FRONT_REAR_DERIVATION_METADATA.json`
  - SHA-256 `776134db606903ca9da76ee42ca7b7dbcf2b0991d29b3f730fd02d2861eb2921`

## 5. 停止门

这两张 256 图能够作为盾自身的离线墙挂／示意构图试材，但**当前不能进入馆守 Z 实际帧试装**：主线已确认现有馆守 Z 图是旧形象，而且 A17 raw 本身不是 Camera V2 斜俯视持盾姿态。必须先定位真正获准的新馆守 Z 图，再由同一 composite owner 按“盾正面与机体正面同向、双手只握背面握把”生产完整动作帧，之后另走用户实机视觉验收。

因此本轮没有复制到 `game-godot/`，没有 `res://` 路径，没有修改 binding、resolver、scene、Runtime 或 Canon。
