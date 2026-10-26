# 1280×720 deterministic overlay/UI and cleanplate contract

Status: `TEMPLATE_ONLY / NO_TARGET_PIXEL_GENERATED`

## 1. Cleanplate

- 文件尺寸固定`1280x720`；地图viewport固定`[0,58,1280,584]`。
- 无UI、无文字、无伪字、无路线、无ghost、无footprint、无朝向扇面、无edge cue、无forecast、无debug。
- cleanplate只含当前物理时态；PLAN不烘未来端点，CONTACT不烘post ghost、T4或T5。
- 不伪造alpha、可拆资产、pivot、Atlas或Runtime handoff。整屏仍标记`non_separable_candidate`。
- 若生成源不是1280x720，只允许在制作人选定后做一次确定性16:9 crop与一次LANCZOS缩放；不得移动相机内容来“补齐”画外对象。

## 2. Overlay层序

1. `CLEANPLATE_CURRENT_PHYSICAL_STATE`
2. `WORLD_INTENT`: 当前选中路线、路线节点、当前footprint、终点ghost、朝向扇面、敌方冲线与保护区；全部由同一projection helper计算
3. `CONTACT_EVIDENCE`: socket、normal、post/recoil ghost，仅审查overlay出现
4. `EDGE_FORECAST`: 只在真实裁切需要时显示S3／EXIT；炮源只在T4 forecast显示方向
5. `SCREEN_UI`: 目标、威胁、策略摘要、纪存通讯与五时点
6. `REVIEW_DEBUG`: anchor、crop、safe zone、SHA，只进入审查板，不进入目标图

## 3. 版面安全区

- 顶部`y=0..57`：一句目标＋三条威胁；右侧只放紧凑策略状态，不设永久竖栏。
- 地图`y=58..641`：承担约80%注意力；中央选择口袋、T1/T2/T3三线与东门不得被长期遮挡。
- 底部`y=642..719`：五时点时间线与提交状态。
- 纪存PLAN通讯：左下安全区，宽度不超过320px（屏宽25%），不遮路线、终点、冲线或接触预测；CONTACT大型通讯退场。
- 50%审查为`640x360`确定性缩略；100%审查使用原图像素裁切，不重新渲染。

## 4. 路线族UI

- 地图只画当前草稿；不把A的21条或B的15条合法最短路线全部展开。
- 摘要显示`route_family_id / valid / steps / endpoint / facing / action_or_reaction`，`hero_route_exact`仅作回归信息，不作为成功必要条件。
- 未闭合时只提示公开缺口：步数、终点、朝向、占地、动作／预备；禁止隐藏吸附或“接近标准答案”。

## 5. 时态

- PLAN：T3/T4/T5全部forecast；无物理接触、炮束、赤红蓄能或完整路损。
- CONTACT A：T3.00；CONTACT B：T3.25。实体FX上限为微裂、少量定向碎屑／水花、hit-stop与反冲。
- T4城市炮和T5赤红／完整翻路只HUD预示；炮源`[29,2]`不因构图需求移入场内。
- post位置、recoil与最终设施／路损只进入证据overlay或后果画面，不与CONTACT实体时态混合。

## 6. 文字

全部中文由确定性字体系统逐字加入，ImageGen不承担文字。逐字copy以`shot-plan.md`第7节为准；禁止生成器伪字、内部ID、调试术语或额外标签。

## 7. 模板文件

`deterministic-overlay-ui-template-1280x720.png`是透明UI／安全区预生产模板，不含地图、机体、建筑或目标场景像素。它只证明版面、层序和文字责任，不代表视觉PASS。
