# C01 2.5D 低热救援美术状态

> Status Authority: `art_session_current`
>
> 更新日期：2026-07-14
>
> 当前门禁：`phase_a5_runtime_composition_trial`

## 当前结论

Phase A 已按合同制作一张 1280x720 最终感 Keyframe。候选方向为“现代赛璐璐走图人物 + 硬表面半厚涂场景”的 2.5D 混合风格。它继续作为气氛、材质、光影和角色视觉语言参考，但人物比例、满屏构图和压平背景不获运行时批准。

当前依据 `C01_RM_2P5D_PERSPECTIVE_TRIAL_V1` 进入 `phase_a5_runtime_composition_trial`，只制作运行时构图桥接证据。在联合验收之前，Phase B 的背景正式分层、角色四方向、走路循环、动作帧、半身和 Cut-in 均禁止批量生成；`phase_b_generation_allowed=false`。

## Phase A.5 运行中

| Stable ID | 交付 | 当前状态 | 运行时 |
|---|---|---|---|
| `KF_C01_RM_2P5D_RUNTIME_LAYOUT_V03` | 1280x720 运行时构图 Keyframe | `candidate_trial` | `runtime_allowed=false` |
| `LAYOUT_C01_RM_CAMERA_DEPTH_V01` | 1920x900 三相机区、脚点与安全区规划图 | `candidate_trial` | `runtime_allowed=false` |
| `PLATE_C01_RM_HALL_CLEAN_TRIAL_V01` | 1920x900 无人 clean plate 试验 | `candidate_trial` | `runtime_allowed=false` |
| `BREAKDOWN_C01_RM_RUNTIME_LAYERS_V01` | 分层、Alpha/opaque/mask 与遮挡拆解图 | `candidate_trial` | `runtime_allowed=false` |
| `SCALE_C01_RM_ACTOR_BRIDGE_V01` | 纪存与两台小机最终像素高度样例 | `candidate_trial` | `runtime_allowed=false` |

程序对齐基准为 1280x720 视口、1920x900 场景、三个横向构图区、脚底中心轴点、`Y=430-650` 主要行走带，以及顶部 56 px、底部 118 px、左右 32 px 安全区。美术 Session 不修改 Godot；当前程序截图仍是几何占位，只用于核对热点、R2 倒地点与 R3 低热扇区。

Phase A.5 五项证据已完成，当前状态为 `ready_for_joint_acceptance`：

- Manifest：[`art-phase-a5-manifest-v1.json`](./art-phase-a5-manifest-v1.json)
- 精确坐标：[`art-phase-a5-layout-metrics-v1.json`](./art-phase-a5-layout-metrics-v1.json)
- 完成报告：[`art-phase-a5-completion-report-v1.md`](./art-phase-a5-completion-report-v1.md)
- 三构图区联系表：[`camera_zone_clean_contact_sheet.png`](./art-delivery/a5/review/zone-evidence/camera_zone_clean_contact_sheet.png)

程序待确认字段：将现有 2040x900 壳层按 X 比例 `0.941176` 映射到 1920x900；三构图区中心改为 X=640/960/1280、Y=450；复拍 A/B/C 三张 1280x720 截图，并逐项确认地平线、脚点、前景遮挡、R2 倒地点、R3 低热区与安全区。该确认未发生前，A5 仍是候选试验。

Decision Request：是否以本轮斜侧视投影、三相机中心、成人 165-220 px、小机 60-100 px 和拆层职责进入联合验收。此决定不等于 `runtime_allowed=true`、不等于 Phase B 开门，也不等于全项目风格锁定。

## Phase A.5 验证

```text
five Stable IDs / files / dimensions / SHA-256   PASS
camera crops A/B/C = 1280x720                    PASS
Jicun height = 190 px                            PASS
adult range = 165-220 px                         PASS
small robot range = 60-100 px                    PASS
clean plate dynamic objects / baked FG           none PASS
original Phase A keyframe hash                   unchanged PASS
Phase B generated assets                         0 PASS
runtime_allowed                                  false PASS
Canon smoke                                      PASS
```

## Keyframe

- Stable ID：`KF_C01_RM_2P5D_STYLE_V01`
- 文件：[`kf_c01_rm_2p5d_low_heat_v02.png`](./art-delivery/review/kf_c01_rm_2p5d_low_heat_v02.png)
- 尺寸：1280x720
- 状态：`pending_user_approval`
- 运行时：`runtime_allowed=false`
- Manifest：[`art-keyframe-manifest-v1.json`](./art-keyframe-manifest-v1.json)
- Prompt：[`kf_c01_rm_2p5d_low_heat_prompt_v01.md`](./art-delivery/sources/kf_c01_rm_2p5d_low_heat_prompt_v01.md)

## 已验证读法

1. 三层空间成立：前景栏杆遮挡、浅纵深地面带、远景上层廊道与馆守 Z 构成可拆分的 2.5D 层级。
2. 纪存位于中景主轴，黑发蓝眼、无眼镜、青年不幼，左臂档案终端可读。
3. 兜灯保持女性整备员与青绿维修服；唐胶保持青年男性朋克修复师，两人不靠换色区分。
4. 跌跌与机器犬均是现实尺度的功能机器，不是幻想机体或萌宠；成年观众带膝部支具和折叠杖，自主向旧门试步。
5. 旧服务门、充电桩、两枚回充绿灯、低热地面扇区、受控裂纹导光板、白框误分类样例均可直接指出。
6. 馆守 Z 仍为 18 米半跪体量，只保留琥珀低热胸光，没有站立、挥拳、武器或全功率表达。
7. 夜景中间调已抬升，人物脸、工具、脚底和互动区不压成黑；深海军蓝、青色结构线、警示金和琥珀低热形成多色层级。

## 未完成且不得冒充完成

- Keyframe 尚未拆成 `BG / MID / FG / MASK`。
- 角色仍是构图级姿态，不是四方向 Sprite 或动画帧。
- 跌跌、机器犬、观众没有单体母版、轴点或动作循环。
- 白框与对白 UI 只是样式样例，不是最终程序贴图。
- 没有制作七海远程审计半身或纪存审计半身。
- 没有覆盖任何既有 `approved_for_runtime` ID，也没有修改 Godot、V35.8、V35.9、V35.10 或 Canon TSV。

## 确认门

需要用户/制作人确认：是否以这张 Keyframe 的人物比例、2.5D 视角、明暗范围、馆守 Z 压入程度和 UI 克制度作为 Phase B 的生产基准。

确认只允许进入本场景 Phase B，不等于锁定全项目美术风格。若需要调整，应先在 Keyframe 上定点返修，仍不得提前生产走路帧。

## 验证

```text
final dimensions                 1280 x 720 PASS
delivery SHA-256                 250c6a70378f65c1e98770cef3848bd9c97763f0065f4034d3d54fb40e9b5f60
runtime_allowed                  false PASS
approval_status                  pending_user_approval PASS
Japanese/Chinese/English text    none PASS
Phase B generated assets         0 PASS
```
