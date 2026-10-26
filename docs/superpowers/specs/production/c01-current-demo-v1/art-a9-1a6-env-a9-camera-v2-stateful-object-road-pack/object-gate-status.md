# ENV-A9 对象门阶段回执

状态：`PRODUCER_OBJECT_GATE_PASS_7_OF_7 / SHIELD_REVISION_PASS / RELEASED_TO_FIVE_STATE_QA`

## 当前已完成

- 已用 bundled Python/Pillow 确定性生成任务书限定的 7 张独立 RGBA；`ZERO_IMAGEGEN`。
- 盾、东门、警戒设施均为独立资源；ACTIVE/DAMAGED 设施保持同 canvas、同 pivot、同 anchor。
- 两张道路后果层均为 `2400×1350` 同 origin 的透明 overlay；静态地面丰富层不含保护区、路线、威胁线、角色或 T5 后果。
- A PLAN 脚点严格读取 Task111：盾 `[400,242]`、设施 `[1000,506]`、东门 `[1200,578]`，无手移、无缩放。
- 已输出 100%/50% 对象板和 A PLAN 精确脚点板。

## 本门制作人必看

1. `qa/A9_SEVEN_RGBA_OBJECT_BOARD_1800x1200.png`
2. `qa/A9_SEVEN_RGBA_OBJECT_BOARD_50_PERCENT_900x600.png`
3. `qa/A9_A_PLAN_EXACT_FOOTPOINT_OBJECT_BOARD_1280x720.png`
4. `qa/A9_A_PLAN_EXACT_FOOTPOINT_OBJECT_BOARD_50_PERCENT_640x360.png`

## 制作人对象门裁决

- 首轮 `6/7 PASS`；唯一返工为退役重盾，其旧读法偏独立路牌。
- 盾体、三焦痕、`256×220`、pivot、anchor 和脚点保持不变；同一 asset 内补入低矮破墙残段、展陈挂架与落地承托。
- 二次门 `7/7 PASS`：50% 和 A PLAN 均可一眼读成“破墙展架墙挂退役重盾”。
- 东门右缘截切、ACTIVE/DAMAGED 区分和 A/B 道路后果均通过对象门。

制作人已放行五态 QA；当前对象板仍不成为最终 PLAN 资产。

## 边界

未新增对象、玩法、passability、Camera、anchor、角色正式像素、Runtime、Default、Save 或 Canon。旧 A4/ENV-A1 对象像素未读取、未复用；A7 仅提供风格值域和 exact 轴参考，A8 只用于脚点整屏 QA 底图。
