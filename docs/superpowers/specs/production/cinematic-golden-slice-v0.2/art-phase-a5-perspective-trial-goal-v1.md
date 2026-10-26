# 美术资产 Session 目标：C01 Phase A.5 运行时构图桥接试验

> Goal ID：`GOAL_C01_RM_ART_PHASE_A5_PERSPECTIVE_TRIAL_V1`
>
> 性质：Phase A 与 Phase B 之间的运行时构图桥接
>
> 当前 Keyframe：保留为风格参考；人物比例和满屏构图不直接批准

## Objective

基于现有 `KF_C01_RM_2P5D_STYLE_V01` 的斜侧视气氛、材质、光影和角色视觉语言，制作一组最小的 Phase A.5 证据，证明它能够转化为“电影化斜侧视舞台 + X/Y 浅纵深 + 三个构图区相机”的可玩画面。

本轮不是 Phase B：不得批量生产四方向角色、走路循环、全套动作、半身或 Cut-in。先解决当前满屏 Keyframe 无法直接运行、人物比例过大、背景被人物烘焙、相机裁切未知的问题。

## 开工前必读

1. `perspective-integration-trial-contract-v1.md`
2. `producer-brief-and-shotbook-v1.md`
3. `art-status.md` 与 `art-keyframe-manifest-v1.json`
4. `main-program-joint-acceptance-report-v1.md`
5. 主程序 Session 最新三个构图区截图、屏幕坐标和技术限制
6. `character_mecha_art_locks.tsv` 的 `CML001/002/003/004/008`

读取后先更新自己的状态页：明确进入 `phase_a5_runtime_composition_trial`，但 `phase_b_generation_allowed` 仍为 false。

## Must deliver

### 1. 运行时构图 Keyframe v03

新建独立 Stable ID，建议：

```text
KF_C01_RM_2P5D_RUNTIME_LAYOUT_V03
```

要求：

- 1280×720，模拟真实游戏视口，不是宣传插画。
- 保留现有 Keyframe 的斜侧视、夜间闭馆色脚本和硬表面半厚涂场景方向。
- 纪存中景高度控制在 180–200 px；远侧人物不低于 165 px，近侧人物不高于 220 px。
- 跌跌与机器犬控制在 60–100 px，并能读出功能差异。
- 地面主要落在 `Y=430–650`，给 X/Y 浅纵深和前景遮挡留下可操作空间。
- 构图中允许展示角色，但必须同时交付不含角色的 clean plate 试验，不能把 v03 当运行时底图。
- UI 只画安全区/框线示意，不烘焙对白文字、姓名、按钮或乱码。

### 2. 1920×900 相机与脚点规划图

新建独立 Stable ID，建议：

```text
LAYOUT_C01_RM_CAMERA_DEPTH_V01
```

在同一张 1920×900 规划图中标出：

- `ZONE_A_ENTRY / ZONE_B_REAL_MACHINE / ZONE_C_OLD_DOOR_LOW_HEAT` 三个 1280×720 裁切框。
- 地面转折线、主要透视线、walkable trapezoid、前/中/后脚点线。
- 成人角色 165/190/220 px 三档尺度样例。
- 小机器人 60/80/100 px 三档尺度样例。
- 旧门、充电位、跌跌、机器犬、成年观众、低热扇区和馆守 Z 的功能位置。
- 顶部 56 px、底部 118 px、左右 32 px 的 UI/关键画面安全区。

三个裁切框都必须是可成立的游戏构图，不能只有中央 1280×720 好看、左右区域只是被 AI 随意扩图的空壳。

### 3. 无人 clean plate 试验

新建独立 Stable ID，建议：

```text
PLATE_C01_RM_HALL_CLEAN_TRIAL_V01
```

要求：

- 1920×900，不含纪存、兜灯、唐胶、观众、跌跌、机器犬、贴片机、对白 UI 和白框。
- 保留完整地面、墙面、廊道和被原人物遮住的合理结构，不能直接裁切当前 Keyframe 后留下修补糊块。
- 馆守 Z 可作为 FAR 层构图参照，但胸灯、照射扇和硬停余辉必须规划为独立 MASK。
- 需要开关/破损/回充变化的物件不得永久烘焙进 clean plate。
- 本轮 clean plate 可以是 `candidate_trial`，不要求直接标为 `approved_for_runtime`。

### 4. 分层与可动物件拆解图

新建独立 Stable ID，建议：

```text
BREAKDOWN_C01_RM_RUNTIME_LAYERS_V01
```

至少标明：

- `FAR`：馆墙、上层廊道、馆守 Z 半跪主体。
- `MID_CLEAN`：无人地面、墙面、固定结构。
- `PROP`：旧门开/关、充电桩灯态、工作台、导光板完好/裂纹。
- `FG`：栏杆、展台边、吊臂及各自遮挡范围。
- `MASK`：环境灯、低热区、胸灯、熄灯余辉。
- `SPRITE`：人物、小机和贴片机的脚点及建议画布范围。

要明确哪些部件需要透明 Alpha、哪些是 opaque plate、哪些只交程序矢量/遮罩，不得只写“后续拆层”。

### 5. 角色尺度与风格桥接样例

只制作一张尺度样例，不生产动画：

```text
SCALE_C01_RM_ACTOR_BRIDGE_V01
```

- 纪存使用 `CML001` 锁定造型：黑发蓝眼、无眼镜、青年而不幼、左臂终端。
- 同一角色展示 165/190/220 px 三种运行时缩放结果，检查脸、发型、终端和腿部是否仍可读。
- 可在旁边放置跌跌/机器犬 60/80/100 px 轮廓样例。
- 只验证最终游戏尺寸的线条密度、色块和辨识度，不延伸四方向或走路帧。

## 当前 Keyframe 的处理规则

- `KF_C01_RM_2P5D_STYLE_V01` 继续保留，不覆盖、不重命名、不标记 runtime approved。
- 它可作为风格和光影参考，但当前约半屏的人物比例不作为运行时比例批准。
- 不把当前图里的角色直接抠出当 Sprite；遮挡、脚底、方向和隐藏肢体不足以支持动画。
- 不把当前图简单切成 FAR/MID/FG；被人物和物件遮住的背景必须在 clean plate 中补全。
- v03 若明显偏离当前美术风格，应解释偏离原因，不得悄悄换成像素、扁平矢量或写实照片风。

## AI 生产约束

- 优先用现有 Keyframe 和 Canon 锁图做 reference/inpaint/outpaint，不以纯文字重新抽卡角色身份。
- 先锁透视线、裁切框、脚点和人物像素高度，再做细节；不得先画满细节再硬缩放。
- 三个相机区的结构连续性必须人工检查，门、栏杆、地面线、廊道和馆守 Z 不得在裁切间跳形。
- 不生成可读中/日/英文文字，不用乱码模拟 UI。
- 所有交付保留生成来源、Prompt/工作流、尺寸、hash、Alpha、状态与返修记录。

## Manifest 与状态

- 上述五项全部使用新 Stable ID，不能覆盖 Phase A 或既有 `approved_for_runtime` ID。
- manifest 必须标明 `candidate_trial`、`runtime_allowed` 和 `phase_b_generation_allowed=false`。
- 只有真正满足透明、尺寸、轴点和状态要求的试验层才可单项申请 `runtime_allowed=true`；v03 合成图默认 false。
- 状态页必须列出：当前 Keyframe 保留项、未批准项、Phase A.5 产物、程序待确认字段和 Decision Request。

## Acceptance

- v03 静止 3 秒读成斜侧视游戏场景，而不是宣传 CG 或正上方地图。
- 纪存中景高度 180–200 px，脸和左臂终端可读，同时屏幕至少容纳两个相邻热点。
- 三个 1280×720 裁切框都具有明确主体、前景遮挡和可行走空间。
- clean plate 没有烘焙角色、小机、白框、文字和必须变化的物件状态。
- walkable trapezoid、脚点线、FG 遮挡与主程序几何壳层能够逐项对齐。
- 旧门、跌跌、机器犬、成年观众、低热扇区和馆守 Z 的位置支持现有剧情和 R1/R2/R3，不需要改写因果。
- 角色缩到 165–220 px 后仍保持同一美术语言，没有变成糊缩略图。
- Phase B 角色动画产出数量为 0；当前 Keyframe 仍未被冒充为运行时资产。

## Stop and ask

- 必须改变斜侧视、地平线、人物 165–220 px 范围或三个相机区才能构图。
- 认为只能做纯横版、正上方/等距俯视或固定满屏 CG。
- clean plate 无法从当前方向稳定生成，需要完全重做场景设计。
- 需要减少/增加角色方向数、修改 Canon 锁定造型或重画馆守 Z 姿态。
- 需要把 v03/clean plate 直接标记为正式运行时批准，或开始批量 Phase B。
- 主程序截图与本合同冲突，不能通过普通裁切、脚点或尺寸微调解决。

## Completion report

完成时必须报告：

- 五项 Phase A.5 产物及 Stable ID、路径、尺寸、hash 和状态。
- 当前 Keyframe 哪些特征被保留，哪些未获批准。
- 三个相机裁切框、人物像素高度、脚点和 walkable 区域。
- clean plate 与分层拆解的完成度和仍缺失区域。
- AI/人工步骤、生成次数、返修次数和一致性风险。
- 与主程序三张截图的逐项对齐表。
- 是否建议进入联合验收；不得自行宣布 Phase B 开门或全项目风格锁定。

