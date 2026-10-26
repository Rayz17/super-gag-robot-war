# C01 Phase A.5 运行时构图桥接完成报告 v1

> Goal：`GOAL_C01_RM_ART_PHASE_A5_PERSPECTIVE_TRIAL_V1`  
> 状态：`ready_for_joint_acceptance`  
> 门禁：`phase_b_generation_allowed=false`

## 五项交付

| Stable ID | 路径 | 尺寸 | SHA-256 | 状态 |
|---|---|---:|---|---|
| `KF_C01_RM_2P5D_RUNTIME_LAYOUT_V03` | `art-delivery/a5/review/kf_c01_rm_2p5d_runtime_layout_v03.png` | 1280x720 | `2dc684d019d3afc09eca54f760732c9399529e80bcd0f778253e70ca60f3c52a` | `candidate_trial`, runtime false |
| `LAYOUT_C01_RM_CAMERA_DEPTH_V01` | `art-delivery/a5/review/layout_c01_rm_camera_depth_v01.png` | 1920x900 | `7dd874f30e26c4f40bddda095f3c46ef24ae1e6e21b427b1eb4d3621899212f2` | `candidate_trial`, runtime false |
| `PLATE_C01_RM_HALL_CLEAN_TRIAL_V01` | `art-delivery/a5/review/plate_c01_rm_hall_clean_trial_v01.png` | 1920x900 | `eff3d9db7bc90c42da3a07052e7af08bd86a3f5175ede2377db81bca6d7d2534` | `candidate_trial`, runtime false |
| `BREAKDOWN_C01_RM_RUNTIME_LAYERS_V01` | `art-delivery/a5/review/breakdown_c01_rm_runtime_layers_v01.png` | 1920x900 | `05701e33f7f42aefd57d1412c62529007456582510a1be7fad7a52f3d71d3410` | `candidate_trial`, runtime false |
| `SCALE_C01_RM_ACTOR_BRIDGE_V01` | `art-delivery/a5/review/scale_c01_rm_actor_bridge_v01.png` | 1280x720 | `70e19a091037442f1253d37918c5fe0032b4ca4e39bfab837682847cafb4ea5b` | `candidate_trial`, runtime false |

Manifest：`art-phase-a5-manifest-v1.json`。精确构图数据：`art-phase-a5-layout-metrics-v1.json`。

## 保留与不批准

保留自 `KF_C01_RM_2P5D_STYLE_V01`：斜侧视 35mm 感、闭馆夜景、深海军蓝结构、青色导向线、警示金与琥珀实用灯、硬表面半厚涂场景、现代赛璐璐人物、18 米馆守 Z 半跪低热语义。

不批准：原 Keyframe 的半屏人物比例、满屏压平构图、烘焙人物/小机/活动物件、白框 UI 样例和直接切层。原 Keyframe 未覆盖、未改名，仍为 `pending_user_approval`、`runtime_allowed=false`。

## 构图与尺度

- 三相机裁切：A `[0,90,1280,720]`，B `[320,90,1280,720]`，C `[640,90,1280,720]`；中心 X 为 640/960/1280。
- UI 安全区：上 56、下 118、左右 32 px。
- v03 纪存 190 px；兜灯 180 px、唐胶 200 px、成年观众 175 px；跌跌 78 px、机器犬 84 px。
- 独立尺度图验证成人 165/190/220 px 与小机器人 60/80/100 px。
- 所有位置以脚底中心为 pivot。v03 主要动作脚点在屏幕 Y=555–635，落入合同地面行动带。
- walkable 规划为连续梯形 `[(90,510),(1810,510),(1900,760),(40,760)]`，不是三条轨道。
- R2 跌跌位置映射到 `DIEDIE / rail sensor` 中央脚点；R3 低热区位于 B/C 重叠区，旧门、观众、机器犬和馆守 Z 同时可读。

## Clean Plate 与拆层

clean plate 已补全人物和原前景栏杆遮住的地面；不含人、小机、贴片机、白框、对白 UI、可读文字、活动旧门叶、充电设备、可切换工作台、低热光束或胸灯。馆守 Z 只作为 FAR 半跪无灯参照。

拆层图明确：`FAR + MID_CLEAN` 为 opaque；`PROP + FG + SPRITE` 为 Alpha；环境灯、低热区、胸灯与余辉为 mask；walkable、pivot、遮挡范围和安全区交程序矢量。A5 没有伪造正式 Alpha 切图，缺失项留给联合验收后的 Phase B。

## AI 与人工步骤

- built-in image generation：4 次。
- 定点返修：2 次，分别处理亮度/活动物件和移除烘焙 FG 栏杆。
- 本地色键去背：1 次，用于 A5 小机/观众桥接剪影。
- 确定性合成：1 个 Pillow 脚本，输出 v03、规划图、拆层图、尺度图和三构图区裁切证据。
- Phase B 角色方向、走路、动作、半身、Cut-in 产量：0。

一致性风险：A5 小机与观众是比例桥接剪影，不是运行时母版；v03 人物缩到 165–220 px 后轮廓和左臂终端可读，但脸部微表情仍需 Phase B 专门简化线条。馆守 Z FAR 参照已与批准 Pose 同源，但尚未拆出胸灯 MASK。

## 主程序对齐

| 构图区 | 主程序当前依据 | 1920 映射 | A5 裁切 | 对齐结论 |
|---|---|---|---|---|
| A 入口 | `rail_camera_target=(620,555)`；兜灯 `(425,555)`、唐胶 `(665,650)` | 镜头 X 584；热点 X 400/626 | center `(640,450)` | 热点 X 已精确映射；镜头需 +56 X、-90 Y |
| B 现实机器 | `rail_camera_target=(1080,565)`；跌跌/回充/机器犬 `(1030/1125/1260, ...)` | 镜头 X 1016；热点 X 969/1059/1186 | center `(960,450)` | 热点 X 已精确映射；镜头需 -56 X、-90 Y |
| C 旧门低热 | `rail_camera_target=(1530,560)`；低热/观众/门 `(1420/1540/1780, ...)` | 镜头 X 1440；热点 X 1336/1449/1675 | center `(1280,450)` | 热点 X 已精确映射；镜头需 -160 X、-90 Y |

X 映射使用 `1920/2040=0.941176`。程序现有六张截图仍是几何占位；本轮逐项对齐使用其中的 `01-explore-panorama.png`、`03-failure-block.png`、`04-guardian-low-heat.png` 与 `c01_rm_room.gd` 的坐标作为权威证据。A/B/C clean crop 和 contact sheet 已提供，等待主程序按上述中心复拍三张截图。镜头调整属于本合同允许的普通裁切/脚点调整，不改剧情、R1/R2/R3 或 X/Y 玩法。

## Decision Request

建议进入联合验收，确认：三个相机中心、斜侧视投影、成人 165–220 px、小机 60–100 px、clean plate 与层级职责。当前不宣布 Phase B 开门，不宣布运行时批准，也不锁定全项目美术风格。
