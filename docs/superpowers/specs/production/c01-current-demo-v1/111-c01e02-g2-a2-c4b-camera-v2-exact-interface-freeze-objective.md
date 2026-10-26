# C01E02 Task111｜G2-A.2-C4B Camera V2精确接口冻结任务书

日期：2026-08-21  
Owner：主程序-2  
任务ID：`G2_A2_C4B_CAMERA_V2_EXACT_INTERFACE_FREEZE`  
状态：`DISPATCH_READY / SELECTED_40X24_ONLY / ADDITIVE_CONTRACT / IMAGEGEN_FALSE / REAL_ART_ZERO`

## 1. 目标

把P109已选的`CAM_A0_V2A_40X24`从Pilot参数收敛为ENV-A1、BREAKER北向、馆守Z东向和后续Godot消费者可共同读取的Candidate exact视觉接口。

本任务不生成环境或机体，不迁移Default，不改玩法；只冻结：投影、相机、crop／canvas、方向screen vector、footpoint、建筑／物件注册、sprite slot、socket screen readback和A5小体兼容性。

## 2. 必读输入

- `110-c01e02-p109-camera-a0-and-focus-reveal-producer-acceptance.md`：派发时锁SHA；
- `109-c01e02-g2-a2-c4-camera-a0-modular-structure-focus-reveal-pilot-objective.md`：SHA `f67a86dda43d1a509e92f13a2f1f3e26fb29892c9d56a58fb9c5f7755242fd80`；
- `main-g2-a2-c4-camera-a0-pilot/06-completion-report.md`：SHA `0d33c774c47620789d31a3131408f2137a98e890b2e68064b7890d24bbe5a773`；
- `main-g2-a2-c4-camera-a0-pilot/delivery-hashes.sha256`：SHA `185e3fc55de904cb096e6073236a2e51bc8acd7bb1cb2489101cae0b7efb798f`；
- `golden_slice_profile.json`、`current_topology_map_contract.json`、`visual_compositor_profile.json`、Task104／105／106、A5 atlas与Task98 sprite／socket合同：全部只读并在回执锁实际SHA；
- tactical interface与production board：派发时锁定，任务内禁止修改。

## 3. 唯一写域

- `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/**`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/**`
- `game-godot/tests/candidate_runtime_demo/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/**`
- `scripts/test_c01e02_g2_a2_c4b_camera_v2_freeze.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c4b-camera-v2-freeze/**`

禁止修改现有V1 projection、C2/C3/C4、Session、Resolver、PerformanceDirector、gameplay profile、现有证据包、真实资产、board/interface、Default、Save与Canon。

## 4. 必须冻结的唯一合同

### 4.1 投影与方向

- `camera_contract_id=CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`；
- `view_space=map_dimetric_40x24`；
- grid=`32×18`；tile half=`[40,24]`；
- orthographic、无透视汇聚、无按map-y缩放；
- `P(x,y)=((x-y)*40,(x+y)*24)`；integer grid coordinate仍为cell center；
- north／east／south／west screen delta依次为`[40,-24] / [40,24] / [-40,24] / [-40,-24]`；
- PLAN focus=`[19.75,9.75]`，A CONTACT=`[20.5,10.5]`，B CONTACT=`[20,10.5]`；zoom=1、shake=0；
- 正式camera raw、world canvas origin、2400×1350或替代canvas fit、四镜头crop必须从上述公式派生并写成单一合同，不复制V1 y常量。

### 4.2 注册与排序

- actor继续`registration_point=footprint_bottom_center`；
- 1×1／2×2／3×3、六Structure与盾／东门／设施共用同一公式；
- Structure front edge由grid_rect内所有格中心投影后计算：`x=(min_x+max_x)/2`、`y=max_y+tile_half_y`；
- foundation与occluder同一pivot／front edge，只有occluder可被显隐；
- depth key=`front_edge_or_actor_footpoint.screen_y + z_bias`；
- 旧anchor-y、固定类别层级与独立手填screen offset继续禁止。

### 4.3 Sprite与socket

- 给GZ 256、BREAKER 384、小体96、车辆128重新写出Camera V2 slot合同；
- canvas尺寸可以继承，但view_space／camera ID不得沿用V1；
- A/B impact、target、body／shield／weapon五socket须同时交local与V2 screen readback；
- 不得以移动world anchor或修改R2C contact point修正视觉误差；
- A5现有四向小体必须给出`V2_COMPATIBLE_FOR_PLAN / REDRAW_REQUIRED`实帧裁决。若仅需显示尺度／pivot重注册，必须列exact值；若地图视角明显不合，停在缺口，不伪称可复用。

## 5. 必交证据

- `current-topology-camera-v2-40x24-contract.json`；
- `camera-v2-direction-registration.tsv`；
- `camera-v2-structure-object-registration.tsv`；
- `camera-v2-sprite-slot-and-socket-contract.json`；
- `A5-camera-v2-compatibility-receipt.json`；
- 至少12个grid控制点、六actor footpoint、六Structure front edge、盾／东门／设施、A/B contact与T4 side socket外部重算，误差≤0.5px；
- A PLAN、B PLAN、A CONTACT、B CONTACT四张非headless exact readback帧；
- A5 west／north／south至少三张100%局部裁切与一张50%地图帧；
- V1/C2/C3/C4输入SHA前后不变；DAG／JSON／Canon report／strict通过；
- 完成报告、外部validator、final log与delivery hashes。

## 6. 停止门

出现任一项立即停止：

- 40×24 world canvas无法容纳Current topology且只能靠挪对象解决；
- V2 screen关系需要改route、anchor、footprint、contact或A/B结果；
- 继续使用V1 camera ID／方向delta／crop冒充V2；
- A5不兼容却强行签复用；
- 修改既有C2/C3/C4证据或正式玩法字节；
- 生成／接入真实环境、馆守Z或BREAKER像素；
- 开放ENV-A1、Call03或Runtime。

完成态只能是：

`CAMERA_V2_40X24_EXACT_INTERFACE_CANDIDATE / A5_COMPATIBILITY_RECORDED / GAMEPLAY_UNCHANGED / REAL_ART_ZERO / AWAITING_PRODUCER_RELEASE_TO_ENV_A1`

