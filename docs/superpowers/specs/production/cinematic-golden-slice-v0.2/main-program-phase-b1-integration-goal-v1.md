# 主程序 Session 目标：C01 Phase B1 真实美术总装试点

> Goal ID：`GOAL_C01_RM_MAIN_PHASE_B1_INTEGRATION_V1`
>
> 前提：只读取美术 `approved_for_trial_runtime` 且 scope 匹配的资产
>
> 禁止解释为：旧基线删除、全量 Phase B 或全项目正式架构

## Objective

把 Phase B1 六类真实美术资产装入独立透视试制场景，关闭相机 Y、脚点、分层、遮挡、MASK、四方向移动和跌跌摔倒的实际总装风险，同时保持现有剧情、R1/R2/R3、preview outcome 和旧基线不变。

## 开工前必读

1. `joint-perspective-acceptance-report-v1.md`
2. `art-phase-b1-integration-pilot-goal-v1.md`
3. `art-phase-a5-layout-metrics-v1.json`
4. 美术最新 `art-phase-b1-manifest-v1.json` 与状态页
5. `main-program-perspective-trial-completion-report-v1.md`

主程序可以先完成坐标修正与 manifest loader；未出现合规 Phase B1 manifest 前不得猜文件名或加载 A.5 review 图。

## Must deliver

### 1. 锁定 A.5 坐标权威

- `CAMERA_Y` 从 400 改为 450。
- 三区中心改为 `(640,450) / (960,450) / (1280,450)`。
- walkable 使用 A.5 metrics 的连续梯形或经过记录的等价微调，并同步热点、脚点、FG 遮挡、R2 倒地点和 R3 扇区。
- 不通过修改美术裁切来保留旧几何坐标。
- 新增测试断言：相机中心、三裁切、屏幕脚点和战术 hit test 使用同一坐标源。

### 2. Manifest 驱动的试点加载

- 只加载 `runtime_allowed=true`、`approval_status=approved_for_trial_runtime`、`runtime_scope=SCN_C01_RM_RESCUE_2P5D_PHASE_B1_ONLY` 的资产。
- Stable ID 到运行时节点的映射集中管理，不在剧情脚本散写文件路径。
- 任一资产缺失、hash/尺寸/帧序不符时使用明确几何 fallback 并显示开发警告，不静默加载旧图。
- A.5 v03、layout、clean trial、breakdown、scale 图仍不得直接加载。

### 3. 场景底板、PROP、FG 与 MASK

- 将 opaque 基础底板放入世界坐标 1920×900，不做额外非整数拉伸。
- 旧门 PROP 对齐 Zone C 门洞，既有状态驱动 closed/opening/open。
- FG 栏杆进入正确 CanvasLayer/z/y-sort 关系；纪存和跌跌前后穿行必须发生正确遮挡。
- 环境灯、低热区、馆守 Z 胸灯和余辉由既有事件独立驱动；底板不随状态换整张图。

### 4. 纪存四方向与纵深

- 输入方向映射到前/后/左/右动画；斜向输入使用稳定的方向优先规则，不在两方向间抖动。
- 继续使用脚底中心、0.90–1.08 纵深尺度和量化/平滑。
- 运行时实测远/中/近高度落入 165–220 px。
- 动画切换不改变碰撞、热点距离或世界脚点。

### 5. 跌跌 R2 实际动作

- R2 玩家确认后播放主动前倾 → fall → down，down 脚点/占格点与战术命中中心一致。
- 跳过演出直接落到同一 down 状态和世界位置。
- 重播清理视觉状态；不得重复提交 preview outcome。

### 6. 双层 UI 安全区

- 永久 HUD 使用顶部 56、左右 32、底部 72 px。
- 临时对白保留底部 118 px，但 `scene_caption` 与当前人物/热点冲突时必须换侧或上移。
- R2/R3 操作期间任何文本面板不得覆盖当前点击目标；错误拒绝提示也要避开扇区。

### 7. 总装证据

产出同一运行时画面的：

1. Zone A 真实底板 + 纪存四方向读法。
2. Zone B 纪存前后绕行 + FG 遮挡。
3. Zone C 旧门三态 + 低热区。
4. R2 跌跌 fall/down 与倒地点。
5. R3 胸灯/低热 MASK 与具名拒绝。
6. 一张 A.5 v03/程序同坐标 50% 叠图，不得只做并排联系表。
7. 45–75 秒真实美术录屏。

未在 B1 范围内的人物继续显示明确几何占位，截图说明中必须标注，不得冒充全场景美术完成。

## Tests and performance

- 全量 Godot smoke、透视专项、Canon strict、Canon smoke。
- 新增 manifest scope/hash/尺寸失败测试。
- 新增相机 Y=450、三区裁切、FG 遮挡、四方向切换、R2 skip/down 等价、MASK 状态测试。
- 记录场景首次加载、首次四方向 Sprite、首次低热 MASK 的尖峰。
- 1280×720 稳态目标 60 FPS；若首次纹理尖峰超过一帧，提供预载或线程加载策略。

## Acceptance

- 真实底板与 v03 在同坐标叠图中地平线、门洞、馆守 Z 和地面主线一致。
- 三相机区无黑边、空洞、突变或角色脚点跳移。
- 纪存四方向与纵深移动不像贴纸滑动；FG 遮挡正确。
- 跌跌 R2 动作、占格点和跳过结果一致。
- 旧门与 MASK 均由状态驱动，不靠换整张背景。
- UI 不遮关键人物、热点和 R2/R3 点击目标。
- 完整/跳过 outcome 与旧基线一致；旧场景仍可直接运行。
- 只有 Phase B1 scope 资产被加载；其他内容保持 fallback。

## Stop and ask

- 真实底板要求改相机 Y、三区数量、世界尺寸或走图比例。
- 纪存四方向与当前移动/碰撞无法对齐，需要减方向或改变控制方式。
- FG/PROP/MASK 无法在现有 2D 架构下组合，需要引入 3D、插件或全局渲染重构。
- R2/R3 必须改玩法因果或切独立棋盘才能与美术对齐。
- 需要加载 runtime false 资产、覆盖旧基线或把试点设为正式模板。

## Completion report

完成时报告：坐标迁移、manifest 映射、实际加载 Stable ID、fallback 清单、六类截图/叠图/录屏、帧率与加载尖峰、全部测试、与 A.5/B1 manifest 的差异、残余视觉债，以及是否建议开放 Phase B2。不得自行开放 Phase B2。

