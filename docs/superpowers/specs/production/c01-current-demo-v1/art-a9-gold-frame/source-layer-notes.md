# A9 Gold Frame｜源层说明

## GF-PLAN

1. `GF_PLAN_imagegen_source_v3.png`：ImageGen 成片母层，包含雨夜街区、正式 Q/SD 单位、纪存表演、路线、威胁走廊与 UI 外框。
2. `gf-plan-ui-text.ass`：只装配当前目标与 Reader 原句，不绘制人物、机体、地图或 FX。
3. `retired-shield-cold-wall-hung-keyed.png`：ImageGen 盾牌源层，经色键提取 alpha 后贴到展墙同一挂点；三道旧痕，冷态，未取得。
4. `GF_PLAN_1280x720_v2.png`：Phase GF 评审帧。不是地图 tile、角色 Atlas 或 Runtime 消费件。

## GF-CONTACT

1. `GF_CONTACT_imagegen_source_v2.png`：以 GF-PLAN 场景母锚生成的首次巨体接触母层；包含承力、路面翻起、雨水扇形、侧甲炮击和被挡开的小体。
2. UI 外框机械复用 GF-PLAN 的 ImageGen UI 图素并缩减；执行态移除路线、幽灵占位、朝向与命令抽屉。
3. `gf-contact-ui-text.ass`：只装配目标和当前三个结算事件。
4. 同一盾牌源层贴到同一展墙挂点，保持冷态墙挂。
5. `GF_CONTACT_1280x720_v2.png`：Phase GF 评审帧。不是 Cut-in、动画帧或 Runtime 消费件。

## 生产边界

- 图像本体由内置 ImageGen 生成/编辑；FFmpeg 仅执行缩放、裁切、叠层、文字装配和 alpha 提取。
- A4 只提供拓扑与相机方向；Gold Frame 不声明像素级坐标 handoff。
- V10X、纪存、B+X、A 小体、A/F 盾均只按已批准范围派生，不晋升 Canon 或 Runtime。
- 七海、兜灯没有进入本轮双帧画面；未重画，也未把 A6/A8 工程夹具回流。
- 未制作完整地图六层、正式 Atlas、Golden Turn、音频、Cut-in、LibTV、Godot 或 Runtime。
