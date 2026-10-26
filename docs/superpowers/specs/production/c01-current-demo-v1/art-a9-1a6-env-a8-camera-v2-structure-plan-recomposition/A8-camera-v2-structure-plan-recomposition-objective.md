# C01E02 ENV-A8：Camera V2 Structure整屏试装任务书

状态：`DISPATCHED_ZERO_IMAGEGEN / QA_ONLY / NOT_PLAN_ASSET / A_PLAN_GATE_FIRST`

## 制作人放行与本轮目标

Task125已签收ENV-A7六栋独立foundation/occluder为exact重组候选资产。本轮只把它们按Task111 Camera V2原world坐标装回A2唯一保留地面，先用`A_PLAN` 1280×720与50%实帧判断整屏构图、视角和建筑存在感是否成立。本包不是PLAN资产，不接入Runtime。

## 唯一读取输入

1. `125-c01e02-env-a6-a7-producer-asset-acceptance-and-a8-plan-recomposition-release.md`。
2. A2 `GROUND_BAKE_CURRENT_V2_2400x1350.png`，只作GroundBake，不读A2旧Structure或成品整帧。
3. A7 `delivery/structures/`中六栋各自foundation/occluder，共12张RGBA。
4. Task111 `current-topology-camera-v2-40x24-contract.json`与`camera-v2-structure-object-registration.tsv`。
5. Task111 `camera-v2-sprite-slot-and-socket-contract.json`只用于GZ/BREAKER QA proxy的native canvas、pivot、footprint和z-bias；`golden_slice_profile.json`只用于A/B馆守Z路线与BREAKER公开北冲路线。

输入基线：GroundBake SHA256=`893e0df76d0cbcacba93fc22ef307f15e1dd04748cc4b016ed4bf8cc2537d27a`；Camera V2合同=`756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a`；Structure registration=`0133cf5c5af7a6dba659221249b9e0bb45c51bebc8cb9b81c50cf9d920d25b7b`。A7的12张由其已签署`delivery-hashes.sha256`锁定。

## Exact合成合同

- world canvas固定`2400×1350`，raw origin固定`[-920,-99]`，因此每栋局部画布左上角只能是`visual_bounds_raw - world_canvas_origin_raw`。
- 六栋foundation先合成；六occluder再按`front_edge_raw.y`稳定排序。不得手移、screen offset、单独缩放、为构图改pivot/grid/front edge。
- `A_PLAN/B_PLAN/A_CONTACT/B_CONTACT`裁切只读Camera V2 `source_canvas_crop_px`；1280×584 map crop固定放入1280×720画面`(0,58)`，其他区域为中性背板。
- actor-free cleanplate不绘制单位、路线、UI、标注、状态物件或特效。六栋仍是可独立toggle的模块，整帧PNG只是QA读图。

## 两段生产与停止门

### Gate 1：只交A_PLAN

必交`A_PLAN` actor-free 1280×720与640×360，以及机器readback；readback必须明确`four_profile_built=false`。如果制作人判定构图、地面/建筑统一性、遮挡或尺度不成立，立即停在`FAIL_A_PLAN_COMPOSITION`，不生成其他三帧。

### Gate 2：仅在制作人放行后

生成四profile actor-free cleanplate；再用冻结的馆守Z 2×2、BREAKER 3×3和权威route生成QA proxy。对应显隐帧只允许将与真实fotoprint/route mask相交的occluder降到0.34；foundation和未相交occluder保持1.00，必须列出相交ID与逐栋toggle状态。

## 关闭边界

`STATEFUL_OBJECT_ART / REAL_ACTOR_PIXELS / FINAL_PLAN / FINAL_CONTACT / RUNTIME / DEFAULT / SAVE / CANON / HUMAN_PLAYTEST`全部继续关闭。机器PASS不替代制作人对A_PLAN实帧的签收。

## Gate 1制作人裁决

`PASS_GAMEPLAY_STAGING_AND_LOW_OCCLUSION / FAIL_FINAL_ENVIRONMENT_RICHNESS`。不得移建筑或改Camera；放行Gate 2的四profile cleanplate和exact proxy对照。本轮报告必须把后续缺口记为“独立、低矮、非阻挡的地面细节／状态物件包”，不得记为重烘建筑或改玩法拓扑。
