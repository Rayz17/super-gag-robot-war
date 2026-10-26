# C01 电影化斜侧视壳层主程序完成报告 v1

> Goal ID：`GOAL_C01_RM_MAIN_PERSPECTIVE_TRIAL_V1`  
> Contract：`C01_RM_2P5D_PERSPECTIVE_TRIAL_V1`  
> Scene：`SCN_C01_RM_RESCUE_2P5D_V01`  
> 验证日期：2026-07-14  
> 结论：`MAIN_PROGRAM_PASS / READY_FOR_JOINT_ACCEPTANCE`

## 1. 结论与边界

主程序已在不改变剧情、RescueState、R1/R2/R3、preview outcome、Stable ID 和旧技术基线的前提下，完成可回退的电影化斜侧视试制壳层。

建议进入主程序/美术联合验收。本报告不开启 Phase B，不将试制推广为全项目正式地图或相机模板。

## 2. 入口与回退

| 项目 | 入口 |
| --- | --- |
| 旧基线 | `res://scenes/c01_real_machine_rescue_validation.tscn` |
| 新试制 | `res://scenes/c01_real_machine_rescue_perspective_trial.tscn` |
| 当前默认 | 新试制 |
| 回退方式 | 显式启动旧场景；旧场景、脚本和证据未删除 |
| 导出包 | `outputs/windows/chao-gag-c01-perspective-trial.pck` |

PCK SHA-256：`3ca12a4d0a92f38870034628875c096b5dffae44c3f9fae67f831c89dc76ee8b`。

## 3. Must Deliver 完成审计

| # | 要求 | 结果 | 权威证据 |
| ---: | --- | --- | --- |
| 1 | 保留旧基线 | PASS | 旧场景直接启动成功；新 smoke 与旧 outcome 等价 |
| 2 | 斜侧视舞台 | PASS | `1920x900`，`FAR/MID_CLEAN/PROP/FG/MASK`，地面带 `Y=430-650`，梯形可走多边形 |
| 3 | 人物屏占比与脚点 | PASS | 成人 171.1/188.2/205.3 px，小机器人 72.6/79.8/87.1 px；脚底中心定位/Y-sort/缩放 |
| 4 | 三构图区相机 | PASS | 中心 `X=640/960/1280, Y=400`；同区锁定；转场 0.56 s；迟滞阈值；电影镜头回位无脏状态 |
| 5 | 斜侧视战术覆盖层 | PASS | R2 椭圆命中、R3 梯形扇区、鼠标/键盘、撤回和具名安全拒绝由 smoke 覆盖 |
| 6 | 对白与 HUD 适配 | PASS | 安全区数值集中配置；场景标题/HUD/半身/Cut-in 保留舞台可见；旧头像未作新壳层最终效果 |
| 7 | 截图与录屏 | PASS | 5 张 1280x720 新截图 + 60.233 s/30 FPS/H.264 录屏 |

## 4. 几何与镜头实值

| 项目 | 实值 |
| --- | --- |
| 世界/视口 | `1920x900 / 1280x720` |
| 地面转折 | 世界 `Y=410` |
| 主要行走带 | 世界 `Y=470-690`，屏幕 `Y=430-650` |
| 可走梯形 | `(120,470) (1800,470) (1898,690) (22,690)` |
| 区 A/B/C 中心 | `(640,400) / (960,400) / (1280,400)` |
| 区间转场 | 配置 `0.56 s`，实测 `0.56669 s` |
| 返回转场 | `0.52 s` |
| 纵深缩放 | `0.90-1.08`，量化步长 `0.015` |
| 成人高度 | 远/中/近 `171.1 / 188.2 / 205.3 px` |
| 小机器人高度 | 远/中/近 `72.6 / 79.8 / 87.1 px` |
| UI 安全区 | 上 `56`，下 `118`，左右 `32 px` |

## 5. 截图、录屏与性能证据

| 证据 | SHA-256 |
| --- | --- |
| `outputs/c01-perspective-trial-v01/01-zone-a-entry.png` | `8c9e5b573e9cb137ae9645ad6fbbc127f44ae663b42fd7109f0089ea6eebc3ab` |
| `outputs/c01-perspective-trial-v01/02-zone-b-depth-occlusion.png` | `1e903df75d59e94e05d7f8f01499a461edbb00a4fafceb4982a612e46e7b12ab` |
| `outputs/c01-perspective-trial-v01/03-zone-c-old-door.png` | `af04e08800ad1cb72af1c1202c39601dc588d7709d0fde7ea8defda8f388e1f4` |
| `outputs/c01-perspective-trial-v01/04-r2-perspective-targets.png` | `0ddf520f4bda9f844b82ae79d8e6ec644cef0e15b7d6371364c4bfaec6a2b27b` |
| `outputs/c01-perspective-trial-v01/05-r3-low-heat-sector.png` | `3662bb95e64837016b0418ffca7e6618a73bde85b2e022c47c22fb8996ce9042` |
| `outputs/c01-perspective-trial-v01/c01-perspective-trial-60s.mp4` | `fe468dbb39beb48c9c95060f1fe5f0aa329fb5b65f6a5f9a709457c8ba10b67c` |
| `outputs/c01-perspective-trial-v01/runtime-performance.json` | `e53863364b7d6f263f4762f81607973e5cb0b1788f0d71ab31dd6b7cf8387263` |

联合查看证据：

- `outputs/c01-perspective-trial-v01/contact-sheet.png`
- `outputs/c01-perspective-trial-v01/video-contact-sheet.png`
- `outputs/c01-perspective-trial-v01/art-v03-program-alignment-contact-sheet.png`
- `outputs/c01-perspective-trial-v01/video-frame-48s.png`
- `outputs/c01-perspective-trial-v01/video-frame-56s.png`

性能结果：

| 场景 | 平均帧率 | p95 | >20 ms |
| --- | ---: | ---: | ---: |
| Zone A | 99.446 FPS | 15.555 ms | 0 |
| Zone B | 99.044 FPS | 15.464 ms | 0 |
| R3 overlay | 99.195 FPS | 15.669 ms | 0 |

## 6. 与 Phase A.5 美术的逐项对齐

A.5 美术包现已具备 `art-phase-a5-manifest-v1.json`、`art-phase-a5-layout-metrics-v1.json` 和 `art-phase-a5-completion-report-v1.md`，权威状态为 `ready_for_joint_acceptance`；五项资产均继续保持 `candidate_trial / runtime_allowed=false`。

| Stable ID / 文件 | 尺寸 | 程序对齐 | 边界 |
| --- | --- | --- | --- |
| `KF_C01_RM_2P5D_RUNTIME_LAYOUT_V03` / `kf_c01_rm_2p5d_runtime_layout_v03.png` | 1280x720 | 斜侧视、浅纵深、成人/小机尺度、馆守 Z 远层影子、低热区读法一致 | 仅作构图参考，未加载 |
| `LAYOUT_C01_RM_CAMERA_DEPTH_V01` / `layout_c01_rm_camera_depth_v01.png` | 1920x900 | 三区、`Y=410`、行走梯形、脚点、165/190/220 与 60/80/100 标尺对齐 | 区中心使用合同值，未做正式像素级美术裁切批准 |
| `PLATE_C01_RM_HALL_CLEAN_TRIAL_V01` / `plate_c01_rm_hall_clean_trial_v01.png` | 1920x900 | 墙/地转折、门、宽地面带与护栏前后层读法对齐 | 未拆分、未导入、未批准 runtime |
| `BREAKDOWN_C01_RM_RUNTIME_LAYERS_V01` / `breakdown_c01_rm_runtime_layers_v01.png` | 1920x900 | 运行时已有 `FAR/MID_CLEAN/PROP/FG/MASK` 同名节点 | 当前节点为几何占位，不是正式分层纹理 |
| `SCALE_C01_RM_ACTOR_BRIDGE_V01` / `scale_c01_rm_actor_bridge_v01.png` | 1280x720 | 成人和小机三档高度全部在合同区间 | 几何轮廓不代替四方向 Sprite/动作帧 |

联合裁切差异：A.5 metrics 的三区中心为 `(640/960/1280, 450)`，当前几何试制为 `(640/960/1280, 400)`。X 中心完全一致；Y 的 50 px 差异来自两种合法但不同的裁切目标：A.5 优先 clean plate 的 `Y=90` 裁切，程序优先把几何占位的可走带精确压在屏幕 `Y=430-650`。正式纹理导入前必须二选一或整体平移场景锚点；本报告不冒充像素级对齐完成。

Phase A.5 当前文件哈希：

| 文件 | SHA-256 |
| --- | --- |
| `kf_c01_rm_2p5d_runtime_layout_v03.png` | `2dc684d019d3afc09eca54f760732c9399529e80bcd0f778253e70ca60f3c52a` |
| `layout_c01_rm_camera_depth_v01.png` | `7dd874f30e26c4f40bddda095f3c46ef24ae1e6e21b427b1eb4d3621899212f2` |
| `plate_c01_rm_hall_clean_trial_v01.png` | `eff3d9db7bc90c42da3a07052e7af08bd86a3f5175ede2377db81bca6d7d2534` |
| `breakdown_c01_rm_runtime_layers_v01.png` | `05701e33f7f42aefd57d1412c62529007456582510a1be7fad7a52f3d71d3410` |
| `scale_c01_rm_actor_bridge_v01.png` | `70e19a091037442f1253d37918c5fe0032b4ca4e39bfab837682847cafb4ea5b` |

## 7. 复用、新增与未改动边界

复用且不改因果：

- `c01_rm_rescue_state.gd`
- `c01_real_machine_rescue_validation.gd` 和旧场景
- `cinematic_director.gd`
- `preview_transaction_ledger.gd`
- `c01_real_machine_rescue_validation.json`

新增/适配：

- 透视配置、Stage、分层占位、战术覆盖、HUD、对白、Cinematic Canvas、试制控制器和独立场景。
- `c01_rm_actor.gd` 增加可选呈现尺度、纵深缩放、最终高度测量和标签开关，默认值保留旧基线。
- 透视 smoke、截图、60 秒录制和 GUI 性能探针。
- 项目默认入口、测试脚本、导出排除、包内资源校验和 README。

## 8. 验证明细

| 验证 | 结果 |
| --- | --- |
| `GODOT_BIN=/opt/homebrew/bin/godot ./scripts/godot-test.sh` | PASS，23/23 |
| 透视专项 smoke | PASS，旧完整 = 新完整 = 新全跳过；镜头回位清洁 |
| `./scripts/canon-check-godot.sh --strict` | PASS |
| `./scripts/canon-smoke-test.sh` | PASS |
| 旧基线场景直接启动 | PASS |
| PCK 导出 | PASS，约 18 MB |
| PCK 资源校验 | PASS，17 项，默认场景正确，测试视频 fixture 排除 |
| PCK 启动 | PASS |
| A.5/preview 证据脚本包内路径扫描 | PASS，0 命中 |
| 截图脚本 headless 边界 | 无纹理时明确返回失败，不再伪报成功 |

## 9. 仍需正式资产解决的问题

1. 联合验收尚未决定相机 `Y=400` 或 A.5 clean plate `Y=450`，正式纹理导入前必须锁定并复拍三区证据。
2. clean plate 尚未成为已批准的 BG/MID/FG/MASK 运行时分层。
3. 成人、跌跌、机器犬和观众尚无已批准四方向 Sprite、脚点母版和动作循环。
4. 前景遮挡和人物可读性已用几何验证，正式纹理导入后仍需重跑五图、60 秒和点击命中验证。
5. 真人盲测不在本主程序合同内；若要升级正式模板，仍必须补。

## 10. 最终门禁

- 是否建议进入联合验收：**是**。
- 是否批准 Phase B：**否**。
- 是否升级为全项目正式 2.5D 模板：**否**。
- 是否保留旧基线：**是**。
- 下一决策：制作人联合验收先锁定相机 Y 裁切与正式分层导入边界，再决定是否开启本场景 Phase B。
