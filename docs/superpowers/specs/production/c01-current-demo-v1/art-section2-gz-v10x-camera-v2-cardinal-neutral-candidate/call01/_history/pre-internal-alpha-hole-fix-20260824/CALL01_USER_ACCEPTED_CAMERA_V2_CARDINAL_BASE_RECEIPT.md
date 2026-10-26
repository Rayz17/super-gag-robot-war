# Call01｜馆守 Z V10X Camera V2 四向基础｜用户裁决回执

> 状态：`USER_ACCEPTED_CAMERA_V2_CARDINAL_BASE / Candidate`
>
> `candidate_exact_pose_binding_allowed=true`、`runtime_allowed=false`、`default_allowed=false`、`canon_promoted=false`

## 用户原话与裁决对象

- 日期：`2026-08-24`
- 用户原话：**“这个通过”**
- 原话所回应的唯一视觉对象，是上一条消息展示的馆守 Z V10X 四张 Camera V2 实际地图帧，以及“是否可以保留这套四向结构”的裁决。结合用户此前要求“先按战斗地图角度规划并制作精灵，再在程序里使用”、禁止旧馆守 Z，以及当前可目视 Godot Candidate Demo 目标，本回执允许当前 E02 实际消费者所需的 `idle/east` 与 `idle/south` 两个精确 pose 进入 Candidate-only Godot binding；这不是动作、Runtime、Default 或 Canon 批准。

## 获准范围

本次只批准以下同一 Candidate 基础：

1. 馆守 Z 使用 V10X 身份与四向一致结构；不再回到旧馆守 Z 形象。
2. `idle / north|east|south|west` 四张透明 RGBA 地图基础图，均为 `256×256`：
   - `north`：`map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_NORTH_CANDIDATE_256.png`，SHA-256 `467118cb7f98b315b50b9ae3b530024a1e42e55c56bf0f392e8560030416b5fb`
   - `east`：`map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_EAST_CANDIDATE_256.png`，SHA-256 `c6dd358980e19045626e0ed17de0614b543a971d7275cde76816e3f1d1f3b0de`
   - `south`：`map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png`，SHA-256 `0b3d2f437558216b8d3a94a1ea5255f7b9310a94447ba530a1d89b210ccfc12d`
   - `west`：`map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_WEST_CANDIDATE_256.png`，SHA-256 `d598b63903b87c76027401aa140a3b52cd4b689f13ce38570a60aa44f9a92351`
3. 相机合同：`CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE / map_dimetric_40x24`，tile half `[40,24]`。
4. 地图注册：`pivot=[128,224]`、`footprint=[2,2]`、`display_scale=[1,1]`。
5. 四张 `1280×720` 实际地图帧中的尺寸与脚点，四向共享 `world_anchor=[15,11]`、`footpoint_screen=[400,338]`：
   - `game-godot/captures/c01_gz_v10x_cardinal_actual_frame/run_20260824_01/01_GZ_V10X_IDLE_NORTH_CAMERA_V2_1280x720.png`，SHA-256 `3175047c5890a3db1ebe56f97588e01ebdb15fcaa77e269a075607be57124943`
   - `game-godot/captures/c01_gz_v10x_cardinal_actual_frame/run_20260824_01/02_GZ_V10X_IDLE_EAST_CAMERA_V2_1280x720.png`，SHA-256 `df483daa18808420fbad8c69cb0d3956060685a0c4ac4424bdc8846a8ce88951`
   - `game-godot/captures/c01_gz_v10x_cardinal_actual_frame/run_20260824_01/03_GZ_V10X_IDLE_SOUTH_CAMERA_V2_1280x720.png`，SHA-256 `777ea5f7d922412843bb6a2c3553772646ab7e61188694d8fbedb3a70b185232`
   - `game-godot/captures/c01_gz_v10x_cardinal_actual_frame/run_20260824_01/04_GZ_V10X_IDLE_WEST_CAMERA_V2_1280x720.png`，SHA-256 `82ed2198fb241660c7c132294a5274bf4adc059032c9870229506789f00567f8`
6. Candidate-only 精确接入范围：
   - `V353U001 / idle / east`：允许 `texture_load=true`，只绑定上述 east PNG 与 SHA；
   - `V353U001 / idle / south`：允许 `texture_load=true`，只绑定上述 south PNG 与 SHA；
   - 每行保持 `pivot=[128,224]`、`footprint=[2,2]`、`scale=[1,1]`，并保持 `candidate_only=true`、`runtime_promotion=false`、`default_promotion=false`、`canon_promotion=false`；
   - 禁止 base binding、generic fallback、mirror、cross-facing、previous-pose fallback。

实际帧清单为 `game-godot/captures/c01_gz_v10x_cardinal_actual_frame/run_20260824_01/actual-frame-manifest.json`，本次裁决时 SHA-256 为 `97378ff16ac1477ff160bda70388c945b7d9bbffe3c2d5b7992e2b68fe8c6c36`。该清单保留捕获时的 `user_visual_acceptance=false` 历史状态；本回执是其后发生的用户裁决，不反写捕获时证据。

## 明确未批准

- `brace`；
- 取盾、持盾、正面双手格挡、盾击等全部盾动作；
- C01E03 与 C01E04 的损伤态、飞拳、断臂、空战及组合演出动作；
- 与 BREAKER／环境统一的材质旧化与色调收敛；
- `idle/north` 与 `idle/west` 的活动绑定（当前只登记库存，没有精确 active consumer）；
- 任何 base binding、generic／mirror／cross-facing／previous-pose fallback；
- Runtime、Default 或 Canon 晋级。

## 后续合法动作

`idle/east` 与 `idle/south` 可以按上述精确合同进入 C01 Candidate Demo；它们在矩阵中继续保持 `USER_ACCEPTED_CAMERA_V2_CARDINAL_BASE`，不伪装为 Runtime/Default `REUSABLE_CURRENT`。`idle/north` 与 `idle/west` 只登记库存。美术资产 Section 2 可以从四向共享母版谱系继续派生缺失动作；每个动作仍需独立实际帧视觉门。旧馆守 Z History 路径与 SHA 继续禁止作为输入、回退或活动绑定。

## Candidate-only 接入验证

- 实际 macOS GUI 验证清单：`game-godot/captures/c01_gz_v10x_bound_idle_actual_frame/run_20260824_06/actual-frame-manifest.json`，SHA-256 `f61875cfdcda8fbd655caf37e72814777c1e475e774ed797036adca2335b4735`；
- `idle/east` 实际帧：`01_GZ_V10X_BOUND_IDLE_EAST_CAMERA_V2_1280x720.png`，SHA-256 `c2dfaeecc5f3dd56dcd69cb8bbca4be0f0fba5ce4da77aff8edbe985888500d5`；
- `idle/south` 实际帧：`02_GZ_V10X_BOUND_IDLE_SOUTH_CAMERA_V2_1280x720.png`，SHA-256 `0e84531c0f9b6ad3c6441782ff40618465f97c351d49fb3cfb028db993059a32`；
- 清单证明：两个 exact pose 的期望/实际 SHA 相等，Camera V2 40×24、pivot、scale、2×2 均一致；north 只库存、brace/盾动作/base binding 均未打开；旧馆守 Z History 未缓存、未激活，presentation probe 前后 world truth 完全一致。
