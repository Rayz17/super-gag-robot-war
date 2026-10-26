# ENV-A9 Camera V2 状态物件与道路后果包完成回执

状态：`PRODUCER_ACTUAL_FRAME_SIGNED / SEVEN_RGBA_AND_FIVE_STATE_TEMPORAL_QA_PASS / NOT_FINAL_PLAN`

## 结果

- 任务书限定的 7 张独立 RGBA 已完成，`ZERO_IMAGEGEN`；未新增第 8 个资源或玩法对象。
- 退役重盾经一次制作人定点返工后通过：同 `256×220`、同 pivot、同 `[14,10] → (400,242)`，盾体与三焦痕不变；新增同 asset 内的破墙残段、挂架和落地承托。
- A PLAN、A CONTACT、A T5 RESULT、B CONTACT、B T5 RESULT 五态 actor-free 100%/50% 实帧已按 Task111 profile、crop 和脚点生成，无手移、无缩放。
- 时态严格分离：PLAN 为 intact/active；CONTACT 只有程序微裂 FX，设施仍 active，未调用 A42/B24；A T5 为 damaged + long broken arc 42；B T5 为 active + twin buckles 24。
- 盾在五态均为 wall-hung/not acquired；东门在五态均为 round-1 open。
- 制作人已实际查看五态 100% 与 50% 板并签署最终实帧 `PASS`；该签署确认 A9 Candidate 包的对象可读性与时态可读性，不晋升为最终 PLAN。

## 制作人已签实帧

1. `qa/A9_FIVE_STATE_ACTOR_FREE_TEMPORAL_BOARD_2320x1120.png`
2. `qa/A9_FIVE_STATE_ACTOR_FREE_TEMPORAL_BOARD_50_PERCENT_1160x560.png`
3. `qa/full-states/A9_A_PLAN_ACTOR_FREE_STATE_QA_1280x720.png`
4. `qa/full-states/A9_A_CONTACT_ACTOR_FREE_STATE_QA_1280x720.png`
5. `qa/full-states/A9_A_T5_RESULT_ACTOR_FREE_STATE_QA_1280x720.png`
6. `qa/full-states/A9_B_CONTACT_ACTOR_FREE_STATE_QA_1280x720.png`
7. `qa/full-states/A9_B_T5_RESULT_ACTOR_FREE_STATE_QA_1280x720.png`

对象级复核入口仍为：

- `qa/A9_SEVEN_RGBA_OBJECT_BOARD_1800x1200.png`
- `qa/A9_SEVEN_RGBA_OBJECT_BOARD_50_PERCENT_900x600.png`
- `qa/A9_A_PLAN_EXACT_FOOTPOINT_OBJECT_BOARD_1280x720.png`
- `qa/A9_A_PLAN_EXACT_FOOTPOINT_OBJECT_BOARD_50_PERCENT_640x360.png`

## 机器证据

- `receipts/A9-object-gate-readback.json`
- `receipts/A9-five-state-phase-readback.json`
- `receipts/A9-five-state-timing-matrix.tsv`
- `receipts/A9-machine-validation-report.json`
- `source-lineage.tsv`
- `asset-manifest.tsv`
- `delivery-hashes.sha256`

机器 PASS 证明资源数量、RGBA/alpha、Camera V2、脚点、时态和封包闭合；制作人已另行完成 50%/100% 五态实际帧签收。

## 关闭边界

最终 PLAN、正式角色像素、CONTACT 演出、稀疏动作、Runtime、60fps、真人试玩、Default、Save 与 Canon 均未开放。A9 到此以 `PRODUCER_ACTUAL_FRAME_SIGNED / NOT_FINAL_PLAN` 封包。
