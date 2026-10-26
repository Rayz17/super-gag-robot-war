# C01E02 Task98｜运行时格心注册制作人局部作废回执

日期：2026-08-21  
责任人：制作人-2  
状态：`SCOPED_VISUAL_REGISTRATION_SUPERSESSION / C3_MAY_CONTINUE_ON_UNAFFECTED_CONTRACTS / CALL03_FALSE`

## 1. 裁决

Task98 的三张综合导向图不能继续作为“current-topology 0px 注册已证明”的证据。它们的地形格、区域轮廓相对运行时统一下偏 20px；其中角色／对象脚点本身仍是正确值，所以综合板形成了“脚点正确、底图错误”的双坐标系。

本回执只作废受影响的视觉注册证明，不作废 R2C 玩法几何、current camera、Atlas slot、pivot、socket 或连续 phase 合同。`G2_A2_C3_CURRENT_TOPOLOGY_REAL_ATLAS_NEUTRAL_CONSUMER` 可以继续只消费下列未受影响合同；任何 Call03／Call04 生成仍保持关闭。

## 2. 根因与运行时真值

Task98 `build_preproduction_package.py` 的 `cell_diamond()` 把 `(x+0.5,y+0.5)` 当作格心；`polygon_for_rect()` 又把 `[x,y]..[x+w,y+h]` 当作矩形边界。current runtime 的唯一规则是：

- 整数 `(x,y)` 是 cell center；
- 1×1 cell 的边界是 `(x-0.5,y-0.5)..(x+0.5,y+0.5)`；
- w×h rect 的边界是 `(x-0.5,y-0.5)..(x+w-0.5,y+h-0.5)`。

在 40×20 dimetric 投影下，错误恰好表现为 screen Y `+20px`。控制点复算：

- grid `(0,0)` 正确 PLAN screen=`(240,-240)`；错误导向板=`(240,-220)`；
- grid `(15,11)` 正确 PLAN screen=`(400,280)`；错误导向板=`(400,300)`；
- A impact `(20.5,10.5)` 在 CONTACT A=`(640,350)`，不受本错误影响；
- B impact `(20,10.5)` 在 CONTACT B=`(640,350)`，不受本错误影响。

## 3. 立即降级为 History 视觉证据的文件

以下现有字节仍保留以便追溯，但不得再进入 ImageGen 参考、0px 注册验收或用户母版裁决：

1. `CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png`，SHA `8aa4909af5aefe0cf1959e1c941bb5c9437567e429ffa487dedd1663f36b5c3a`；
2. `PLAN_SLOT_COMPOSITE_QA_1280x720.png`，SHA `772c299994d47510dce3f30f6fb07fc4d2d4ba39744886dacff0b64558f96348`；
3. `PLAN_SLOT_COMPOSITE_QA_50_PERCENT_640x360.png`，SHA `75bb1b09ec4201c8b66f624b00789237766f1db41177c0fff52cf6e346681a33`。

Task98 原 `machine-validation-report.json`、`preproduction-completion-report.md` 与 `delivery-hashes.sha256` 仍可证明当时交付字节闭合，但不再证明上述三图与 runtime 0px 对齐。禁止把原整包 manifest SHA 当成视觉注册已通过的替代证据。

## 4. 保留有效且允许 C3 继续锁定的合同

以下合同没有使用错误的综合地形格心，可继续作为 Task99/C3 的 exact 输入：

- `atlas-schema-current.json`，SHA `159c0af021c99a8c778692f5b02794e5ec55a476514da55ff55958baa19e8e5d`；
- `map-camera-slot-contract.json`，SHA `17e195dcac011be803bd69d893a918830dd838a5aa7a4aedd3e76bab45fb1a24`；
- `socket-contact-contract.json`，SHA `c954af9b0ac7e5a1ef0e55f95b613367af9ab5ddbaec3fc55f5f4a258e5b8ea5`；
- `first-round-state-facing-phase-matrix.tsv`，SHA `992ff3e6c35eb5cf6aa69ae928190f5c8ac3bb11927474569e1211ebb655bb2e`；
- `first-round-phase-continuity-readback.tsv`，SHA `e03f74e3e81ce888554b7ec0ba7e8e5c8e81600a1bc1f1974b755d73b7d64199`；
- `GUARDIAN_Z_EAST_MAP_CAMERA_GEOMETRY_GUIDE_256.png` 与 `BREAKER_NORTH_MAP_CAMERA_GEOMETRY_GUIDE_384.png` 的本地 frame／pivot 几何；它们不承担整屏地图注册证明。

当前已复算正确的 PLAN 脚点保持：馆守Z `(400,340)`、BREAKER `(520,520)`、应急车 `(520,320)`、小体01 `(840,360)`、小体02 `(800,540)`、小体03 `(1200,460)`。

## 5. Call03 前强制修复门

在任何 `BREAKER_PLAN_MAP_CAMERA_MASTER_NORTH_RGBA_384` 生成前，必须：

1. 修正 `cell_diamond()` 为整数格心；
2. 修正 `polygon_for_rect()` 为 ±0.5 边界；
3. 重导 actor-free guide、PLAN composite 100% 与 50%；
4. 用 runtime projection helper 外部复算至少三个控制点，误差≤0.5px；
5. 重建对应 machine report、completion correction 与 delivery hashes；
6. 制作人重新逐图签收整屏注册。

Task101/ENV-E0 必须直接从 runtime projection 真值重导 masks/crops，不得复用本回执作废的三张可见像素。

## 6. 权限边界

本回执不改变玩法几何、A/B结果、R2C、current camera、Canon、Default、save或Runtime。当前状态继续是：

`Call03=false / Call04=false / approved_handoffs=[] / real_art_loaded=0 / UA91=false / G2-B=false / FUN_NOT_PROVEN`。
