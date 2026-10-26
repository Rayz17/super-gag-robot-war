# BREAKER Camera V2脚本预生产停止回执

状态：`COMPLETE_STOP_PACKAGE / STOP_SCRIPT_SCAFFOLD_REQUIRES_HUMAN_CONCEPT_REDRAW / NOT_FINAL_ART`

## 最终结论

本包完成了零ImageGen、零旧失败像素复用的Camera V2预生产探索，但没有产出可交人工覆画的结构底稿。

REV1—REV4依次暴露圆壳四足、龟、驼背猿／熊和双足大脚等第一读法。REV4是最后一次脚本尝试；其192纯黑union仍被制作人与执行者独立判定为驼背猿／双足熊。因此按停止门终止脚本迭代，不制作REV5，不把REV4冒充sole scaffold。

真实人工美术像素仍为0。下一步需要真人概念重构，而不是在REV4上覆画。

## 交付与失败证据

- `qa/BREAKER_NORTH_CAMERA_V2_REV4_REJECTED_SCAFFOLD_RGBA_1536.png`：最后一次脚本底稿，History rejected；
- `qa/BREAKER_NORTH_CAMERA_V2_REV4_BLACK_SILHOUETTE_192.png`：无内部线的192纯黑union；
- `qa/BREAKER_NORTH_CAMERA_V2_REV4_BLACK_SILHOUETTE_GATE_1200x720.png`：明确FAIL的黑剪影门；
- `qa/BREAKER_NORTH_CAMERA_V2_REV1_REV2_REV3_REV4_COMPARISON_2400x900.png`：四版失败收敛对照；
- `qa/BREAKER_NORTH_CAMERA_V2_EXACT_REGISTRATION_1536.png`：Camera V2、3×3和pivot精确注册证据，不代表视觉通过；
- `delivery/BREAKER_BX_RESPONSIBILITY_BOARD_1920x1200.png`：责任合同板，图中REV4明确 rejected，只保留B／X职责；
- `paint-layer-contract.md`、`layer-socket-pivot-contract.json`、`source-lineage.tsv`、`forbidden-sources.md`、`paint-brief.md`、`50-100-acceptance-template.md`、`producer-gate.md`；
- `receipts/geometry-readback.json`和`delivery-hashes.sha256`。

## 精确接口保留

- 工作目标`1536×1536`；最终槽`384×384`；
- pivot工作图`[768,1280]`，最终`[192,320]`；
- footprint=`3×3`；
- tile half最终`[40,24]`，north=`[40,-24]`；
- registration=`footprint_bottom_center`；
- ImageGen=`0`；Call03 raw读取／消费=`false`；历史失败像素复制／合成=`false`。

这些数值只供未来真人从空白画布重构时使用，不升级REV4。

## Canon与生命周期

Current Canon仍只确认BREAKER是近30米黑甲突入壳，可钻地、冲撞并发射赤红冲击。B身体与X表面继续是本Demo Candidate责任源，没有反向晋升Canon。本包不改Canon、玩法、production board、tactical interface、Godot、Default或Save。

## 最终停止状态

`NO_SOLE_SCAFFOLD / HUMAN_CONCEPT_REDRAW_REQUIRED / RESOURCE_NOT_AUTHORIZED / REAL_ART_ZERO / CALL04_FALSE`
