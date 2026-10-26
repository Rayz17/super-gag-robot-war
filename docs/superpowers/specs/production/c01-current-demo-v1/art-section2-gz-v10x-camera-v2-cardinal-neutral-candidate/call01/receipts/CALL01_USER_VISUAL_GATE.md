# Call01｜馆守 Z V10X Camera V2 四向中立母版｜用户视觉门

> 状态：`DIRECTION_ACCEPTED / EAST_SOUTH_ALPHA_REPAIRED_PENDING_REVIEW / Candidate`
>
> `east_south_user_actual_frame_accepted=false`、`candidate_exact_pose_review_binding_allowed=true`、`runtime_allowed=false`、`canon_promoted=false`

> 2026-08-24 纠正：原“这个通过”保留为设计/角度/尺寸/脚点认可；用户后续指出 east/south 封闭负空间有白底，两个旧 SHA 已降为 `REJECTED_ALPHA_HISTORY`。当前 E/S 修复字节为 `CANDIDATE_VISUAL_REVIEW_ONLY`且 `user_visual_acceptance=false`；下文对旧 E/S 字节的通过描述只是历史记录。详见 `CALL01_INTERNAL_ALPHA_HOLE_FIX_RECEIPT.md`。

## Section 2 自检结论

- 身份：使用 V10X 红 X 胸、金圆核、完整头冠、宽肩、等粗圆筒前臂／腿、白大腿与蓝红主体；未回流旧馆守 Z。
- 形态：C01E02 双臂完整，无盾、无翼、无背包，约 4.2 头身。
- 相机：四格共用固定抬高 dimetric，相机不绕机体；当前正式 Candidate 合同是 `CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE / map_dimetric_40x24`，数值源为 `P(x,y)=((x-y)*40,(x+y)*24)`，north/east/south/west 分别按 `(40,-24)`、`(40,24)`、`(-40,24)`、`(-40,-24)` 读回。
- 隔离：旧 76 号／旧 `map-camera-slot-contract.json` 的 40×20 preproduction 合同没有作为本包正向相机源；本包未修改全局合同。
- 注册：四张 `256×256`，共同 `pivot=[128,224]`、`footprint=2×2`、`scale=1`；四向脚点误差均为 `0px`。
- 透明：原图棋盘格烘进 RGB；确定性 alpha 仅删除边界连通的高亮中性色背景，RGB 字节未改变。深／浅底 100% 与 50% 已复核。
- 调用：内置 ImageGen `1` 次，随机重抽 `0` 次。

## 用户裁决

用户于 `2026-08-24` 对四张实际地图帧明确回复：**“这个通过”**。

因此，V10X 身份、N/E/S/W 四张 `256×256 RGBA`、Camera V2 `40×24`、`pivot=[128,224]`、`footprint=2×2`、`scale=1`，以及实际地图中的尺寸与脚点已通过 Candidate 级四向基础门。完整路径、SHA 与批准边界见 [CALL01_USER_ACCEPTED_CAMERA_V2_CARDINAL_BASE_RECEIPT.md](CALL01_USER_ACCEPTED_CAMERA_V2_CARDINAL_BASE_RECEIPT.md)。

结合用户此前明确要求地图角度精灵最终进入程序、禁止旧资产，以及当前可目视 Godot Candidate Demo 目标，当前 E02 活动消费者所需的 `idle/east` 与 `idle/south` 可按 path/SHA/pivot/scale/footprint 精确合同进入 Candidate-only pose binding。它不建立 base binding，也不允许 generic、mirror、cross-facing 或 previous-pose fallback。

本裁决仍没有批准 `brace`、任何盾动作、E03/E04 动作、材质统一结果、`idle/north|west` 活动绑定、Runtime、Default 或 Canon。后续动作只可从同一母版谱系派生，并逐项另过实际帧门。

接入后的真实 macOS GUI 复核位于 `game-godot/captures/c01_gz_v10x_bound_idle_actual_frame/run_20260824_06/`：east/south 两个 exact pose 均从活动 binding 解析，旧馆守 Z 未缓存或激活，north、brace 与盾态继续 fail-closed，world truth 未改变。
