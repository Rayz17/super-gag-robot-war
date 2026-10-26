# ENV-A8 Camera V2 Structure整屏试装回执

状态：`PRODUCER_PASS_EXACT_STRUCTURE_RECOMPOSITION_AND_INTERSECT_ONLY_REVEAL / FAIL_FINAL_ENVIRONMENT_RICHNESS / QA_ONLY / NOT_FINAL_PLAN`

## 本轮结果

- Gate 1制作人裁决已记录为`PASS_GAMEPLAY_STAGING_AND_LOW_OCCLUSION / FAIL_FINAL_ENVIRONMENT_RICHNESS`。
- A/B PLAN、A/B CONTACT四个Camera V2 profile均已输出actor-free 1280×720与50%帧；画面只读A2 GroundBake与A7六栋独立foundation/occluder。
- 六栋位置全部由`visual_bounds_raw - [-920,-99]`派生，无手移、无缩放、无Camera或拓扑修改。
- QA proxy使用Task111冻结的馆守Z `[15,11] / 2×2 / east / pivot 128,224`、BREAKER `[20,13] / 3×3 / north / pivot 192,320`，以及A路线和BREAKER公开北冲路线。proxy不是真实单位像素，不进入资产。
- 相交审计只触发`SE_BLOCK`：其occluder在depth key上位于BREAKER之前，与proxy body有109个相交像素。对照帧仅把`SE_BLOCK` occluder从1.00降到0.34；其余5栋与foundation全部1.00。normal/reveal的48497个变化像素全部位于`SE_BLOCK` alpha范围，范围外变化为0，不是全图淡化。
- 六栋仍保留独立foundation/occluder toggle；所有整帧合成图都只是制作人QA。
- 制作人已独立目视四profile与A PLAN normal/reveal，签收`PASS_EXACT_STRUCTURE_RECOMPOSITION_AND_INTERSECT_ONLY_REVEAL / FAIL_FINAL_ENVIRONMENT_RICHNESS / NOT_FINAL_PLAN`；机器相交报告不替代该实帧裁决。

## 制作人必看

1. `qa/four-profile-actor-free-cleanplates/A8_FOUR_PROFILE_ACTOR_FREE_BOARD_1280x780.png`
2. `qa/occlusion-proxy/A8_A_PLAN_EXACT_FOOTPRINT_ROUTE_PROXY_NORMAL_1280x720.png`
3. `qa/occlusion-proxy/A8_A_PLAN_EXACT_FOOTPRINT_ROUTE_PROXY_INTERSECT_ONLY_REVEAL_034_1280x720.png`
4. `qa/occlusion-proxy/A8_A_PLAN_OCCLUSION_NORMAL_VS_INTERSECT_ONLY_034_COMPARISON_1280x420.png`
5. `receipts/A8-full-recomposition-and-occlusion-readback.json`与`receipts/A8-structure-toggle-and-reveal-matrix.tsv`

## 后续缺口（不在A8内扩做）

当前已证明中心留白是馆守Z、BREAKER、footprint和路线占据的玩法舞台，但静态整帧仍缺丰富度。后续正确缺口严格是以下7张独立玩法对象／道路结果层：

1. `PROP_C01CDV1_RETIRED_SHIELD`；
2. `PROP_C01CDV1_RETIRED_SHIELD_SUPPORT_PLINTH`；
3. `TARGET_C01_EAST_EXIT`；
4. `TARGET_C01_SECURITY_GATE_ACTIVE`；
5. `TARGET_C01_SECURITY_GATE_DAMAGED`；
6. `ROAD_DAMAGE_A_42_OVERLAY`；
7. `ROAD_DAMAGE_B_24_OVERLAY`。

这7张必须保持独立、低矮／地面结果层、玩法语义可读，不能被扩写为“任意增加装饰”。缺口不是重烘六栋建筑，不是改Camera、建筑位置、route或玩法拓扑。A8本轮不继续制作该对象包。

## 关闭边界

`STATEFUL_OBJECT_ART / REAL_ACTOR_PIXELS / FINAL_PLAN / FINAL_CONTACT / RUNTIME / DEFAULT / SAVE / CANON / HUMAN_PLAYTEST`仍关闭。A8只封包为制作人签收的exact QA证据，不是最终PLAN或Runtime candidate。
