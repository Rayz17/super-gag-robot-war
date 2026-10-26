# C01E02 ENV-A9：Camera V2状态物件与道路后果最小资产包任务书

状态：`DISPATCHED_ZERO_IMAGEGEN / SEVEN_RGBA_ASSETS / EXISTING_GAMEPLAY_OBJECTS_ONLY / NOT_FINAL_PLAN`

## 目标

A8已证明六栋独立建筑、Camera V2整屏构图和“只淡实际相交物件”的简单2D遮挡方法成立；actor-free整屏仍缺既有玩法地标与后果。A9只补当前玩法已经存在的盾、东门、警戒设施和道路状态，不新增战术对象、不改passability、不改anchor。

## 唯一允许的7张RGBA

1. `GROUND_DETAIL_OVERLAY_STATIC_CURRENT_V2_2400x1350.png`：独立静态地面丰富层；只含主路、撤离线与security apron内的铺装、排水、低频积水／路缝和克制方向语言。
2. `RETIRED_SHIELD_WALL_HUNG_3_SCORCHES_CAMERA_V2_RGBA.png`：anchor=`[14,10]`，墙挂、三道焦痕、本轮未取得。
3. `EAST_EXIT_FIRST_ROUND_OPEN_CAMERA_V2_RGBA.png`：anchor=`[31,7]`，第一轮开放。
4. `WARNING_FACILITY_ACTIVE_CAMERA_V2_RGBA.png`：anchor=`[27,8]`。
5. `WARNING_FACILITY_DAMAGED_CAMERA_V2_RGBA.png`：与active同canvas、同pivot、同anchor。
6. `ROAD_RESULT_A_LONG_BROKEN_ARC_42_RGBA_2400x1350.png`：全画布透明后果层，A路T5使用。
7. `ROAD_RESULT_B_TWIN_BUCKLES_24_RGBA_2400x1350.png`：全画布透明后果层，B路T5使用。

保护区`[20,5,12,7]`继续由程序overlay绘制，不生成图片；CONTACT的`micro_crack`继续归稀疏FX，不进入本包；城市炮源继续使用准确右缘HUD cue，不移入画面。

## 空间与美术冻结

- Camera V2 axes=`(40,24)/(-40,24)`，无透视汇聚；world canvas=`2400×1350`，origin=`[-920,-99]`。
- A PLAN精确脚点：盾`[400,242]`、设施`[1000,506]`、东门`[1200,578]`。资源pivot必须落在各自footprint/front-edge责任点，禁止手移。
- 盾、东门、设施必须是独立资源；道路后果必须是同origin全画布透明overlay；任何状态像素不得烘进GroundBake或六栋Structure。
- 与A7共享4—7大色值、两级硬阴影、Camera V2 exact轴、克制青灰／暖色提示。禁止动态光、shader、SubViewport、照片噪声或旧A4／ENV-A1对象像素。
- 地面丰富层只改低对比静态材质，不画保护区荧光框、路线、footprint、ghost、威胁线、UI或T5破坏。

## 时态矩阵

| 资源 | PLAN | CONTACT | T5 |
| --- | --- | --- | --- |
| 重盾 | 墙挂、未取得 | 同 | 同 |
| 东门 | open | open | open |
| 警戒设施 | active | active | A=`damaged`；B=`active` |
| 道路 | intact | 仅程序／FX `micro_crack` | A=`long_broken_arc/42`；B=`twin_buckles/24` |
| 保护区 | 程序overlay | 程序overlay | 程序overlay |

本矩阵防止把Resolver终态提前泄漏到CONTACT。若现有Candidate接口仍在CONTACT直接读取A=`damaged`，必须在真实合成前另做表现时序纠偏；美术不得用资产烘死来解决。

## 必交与停止门

- 7张RGBA、source-lineage、asset manifest、pivot／anchor／camera readback、全包SHA。
- 100%／50%对象板；A PLAN精确脚点板；PLAN、CONTACT、T5 A/B五态整屏QA，但QA合成不成为最终PLAN资产。
- active/damaged设施与A/B道路后果在50%可分，但不得误导为passability改变。
- 任何anchor/pivot/camera偏移，盾／门／设施被烘进地面，CONTACT提前出现完整T5后果，或自行新增路灯／护栏／花坛／废墟，立即停止。

本任务不开放角色正式像素、BREAKER/GZ master、最终PLAN、CONTACT演出、稀疏动作、Runtime、UA91、G2-B、Default、Save或Canon。
