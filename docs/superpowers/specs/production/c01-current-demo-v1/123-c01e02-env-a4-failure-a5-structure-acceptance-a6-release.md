# C01E02 ENV-A4失败、A5结构签收与A6单栋材质放行

状态：`PRODUCER_SIGNED / A4_NO_BATCH / A5_STRUCTURE_PASS / A6_NW_ONLY_RELEASED`

## 制作人实际帧裁决

制作人已在100%与50%实际图查看`NW_BLOCK`：

- ENV-A4保持了Camera V2、pivot、Alpha与显隐，但50%仍首先读作“贴了雨蚀材质的规整盒体”。结论为`MECHANICAL_PASS / FAIL_FINAL_QUALITY / NO_BATCH`；不得扩六栋。
- ENV-A5在不改`grid_rect=[1,0,7,5]`、pivot=`[240,378]`、front edge=`[80,288]`、Camera V2与foundation的前提下，把occluder改为低主楼、低东翼、偏置设备间和南侧短檐。50%已能脱离单一矩形盒读法，0.34显隐后方单位与路线可读。结论为`PASS_STRUCTURE_HIERARCHY / NOT_FINAL_ART`。

机器PASS不替代上述视觉裁决。A5只证明单栋体块与交互关系，未证明精品材质、六栋统一性、整屏PLAN或Runtime。

## 锁定证据

- Task122：`122-c01e02-env-a4-camera-v2-exact-six-structure-materialization-objective.md`，SHA256 `c7775c196b1eddcadeae57a33e30dab8fafba1498cad90491ee9c18652a53993`。
- A4停止回执：`art-a9-1a6-env-a4-camera-v2-exact-six-structure-materialization/pilot/receipts/A4_PRODUCER_STOP_FAIL_FINAL_QUALITY.md`，SHA256 `233fd07c7f7594c35efff4efc969eb5140c0f33e86fd37770fdf96c12e23cad5`。
- A4失败清单：`art-a9-1a6-env-a4-camera-v2-exact-six-structure-materialization/pilot/failure-hashes.sha256`，SHA256 `bd0044dc798f7e96ec9917925e1ff96b596f3b20f9e0be8bef8855837ca3dece`，8项全部通过。
- A5任务书：`art-a9-1a6-env-a5-camera-v2-one-structure-enrichment/A5-one-structure-enrichment-objective.md`，SHA256 `a05ca25289beea6b2e4b9face06c6d4f01406891a9e92044fbd72b1b78060ae6`。
- A5读回：`art-a9-1a6-env-a5-camera-v2-one-structure-enrichment/receipts/A5-NW_BLOCK-machine-readback.json`，SHA256 `3dd9d59eedd9677e80beb6490c91d416f195e1b8fd1e40aee77ab687b838a3e0`。
- A5交付清单：`art-a9-1a6-env-a5-camera-v2-one-structure-enrichment/delivery-hashes.sha256`，SHA256 `9a872192e8f827cc72b9d435c264cf396391426c6bd7013de0d94620c9423919`，17项全部通过。

## A6窄放行

仅放行`NW_BLOCK`在A5 Alpha内进行一次零ImageGen材质试制：4—7个大色值块、屋顶防水／排水、连续窗带与入口、设备间宽百叶、最多三处暖色边灯和低频雨蚀。禁止改Alpha、pivot、grid、envelope或Camera V2；禁止扩其余五栋。

A6必须停在制作人50%／100%实际图门。若仍像程序模型，立即封存`FAIL_FINAL_QUALITY`；不得用六栋批量、动态渲染、旧视角像素或新ImageGen掩盖失败。

## 继续关闭

`SIX_STRUCTURE_BATCH / FINAL_PLAN / CONTACT / REAL_ART_RUNTIME / FINAL_60FPS / UA91 / G2_B / DEFAULT / SAVE / CANON`继续关闭。
