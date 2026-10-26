# A31 馆守 Z V10X `shield_block/south` BODY-ONLY + A17 确定性合成｜来源锁

> 状态：`CALL01_HARD_GATE_FAILED / COMPOSITE_NOT_BUILT / NO_BINDING`
>
> 不构成：用户实际帧验收、Godot 绑定、Runtime / Default / Canon 迁移。

## BODY-ONLY 唯一正向身份谱系

1. CML130 限域唯一正向设计母图：
   - `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`
   - SHA-256 `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`
2. CML130 谱系的 Camera V2 south 当前角度参考：
   - `docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png`
   - SHA-256 `d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796`
   - 它保留用户认可的 V10X 设计方向、Camera V2 south、尺寸与脚点；Alpha 修复后仍是 `CANDIDATE_VISUAL_REVIEW_ONLY`，不代签本动作。

BODY-ONLY ImageGen 只读上述两图；输出禁止包含盾、握把、背景、FX、文字或第二机体。

## A17 确定性合成源

- 热态／受击后 `front_exterior`：
  - `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png`
  - SHA-256 `8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47`
- 握把 socket 的不可见注册只读 A17 `rear_interior` 元数据：
  - `derived-front-rear-sprites-v1/A17_SHIELD_FRONT_REAR_DERIVATION_METADATA.json`
  - rear map grip centers `[96.827,104.747]` / `[134.419,104.747]`
  - front-edge socket `[170.818,96.457]`

盾牌像素不进入 ImageGen。合成时只对已接受的 front exterior 做确定性预乘 Alpha 缩放／Camera V2 south 仿射登记，不重画、不去热痕、不添加像素。

## Camera / 地图合同

- `CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`
- south screen vector `[-40,+24]`
- 最终 `256×256 RGBA`
- pivot `[128,224]`
- footprint `[2,2]`
- scale `[1,1]`
- 机体正面与盾正面同向 south；馆守 Z 位于盾后。

## 严禁输入或回退

- CML008 旧视觉像素；
- A13 / A18 / A19 / A22 任何 raw、guide、姿态或像素；
- 旧 `guardian_z_east_camera_v2_candidate.png`；
- A2 旧弹孔装甲板；
- `failed-cold-front-deterministic-experiments-do-not-use/` 全部冷盾；
- 任何 mirror / rotation / cross-facing / generic / previous-pose fallback。

## 停线规则

- ImageGen 最多 1 次，随机 reroll = 0。
- 身份、south 朝向、双臂双手、透明 Alpha 任一硬门失败：停止，不合成、不重抽。
- 只有 BODY-ONLY 通过后，才可生成一个单一 visual owner 的离线 Candidate composite。

## Call01 执行结果

- ImageGen 调用：`1`；随机 reroll：`0`。
- BODY-ONLY raw：已仅作为失败证据保留；`1024×1536 RGB`，无 Alpha 通道，浅色棋盘烘入 RGB。
- Camera V2 south：失败。输出为接近正面平视的 hero view，未形成 lower-left `[-40,+24]` 轴与高俯视 top-plane 关系。
- 双臂双手：通过局部门；两臂完整、肘部弯曲、双拳分离。
- 停线动作：未对 A17 盾做缩放、仿射、登记或合成；未生成 `256×256` Candidate；未绑定 Godot，未改 Runtime / Default / Canon。
