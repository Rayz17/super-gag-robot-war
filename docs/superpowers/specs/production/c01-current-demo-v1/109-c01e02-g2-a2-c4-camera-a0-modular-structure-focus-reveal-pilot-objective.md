# C01E02 Task109｜G2-A.2-C4 相机A0＋模块建筑＋焦点显隐Pilot任务书

日期：2026-08-21  
Owner：主程序-2  
任务ID：`G2_A2_C4_CAMERA_A0_MODULAR_STRUCTURE_FOCUS_REVEAL_PILOT`  
状态：`DISPATCHED_AFTER_PRODUCER_REVIEW / ADDITIVE_PILOT_ONLY / IMAGEGEN_FALSE / REAL_ART_ZERO / GAMEPLAY_BYTES_LOCKED`

## 1. 任务目的

在不改R2C玩法、Current topology、C2／C3验收字节和真实资产的前提下，一次回答两个正式美术开工前的问题：

1. `40×20 / 40×24 / 40×26`哪档相机最适合巨体战棋、建筑存在感和低遮挡读法；
2. 独立建筑／物件能否用低成本的焦点驱动整件淡化完成机战式遮挡交互。

本任务只交Candidate proxy actual frames、交互回执和性能回执。机器PASS不能选择Camera V2，也不能开放ENV-A1、Call03或真实资产。

## 2. 必读及锁定输入

| 输入 | SHA-256 | 用途 |
|---|---|---|
| `104-c01e02-task98-runtime-grid-registration-producer-acceptance.md` | `1ad0c1d0d5958f432f81479a119310769eaba3b769637b07ba7bcde127edfe61` | integer cell center与0px注册边界 |
| `105-c01e02-task99-simple-2d-board-lighting-occlusion-producer-correction.md` | `6046293f86788b561e8e78f581cc1dcfa4968c206e0c5cadc74943aa9c5ef0b7` | 简化遮挡原则／禁止复杂渲染 |
| `106-c01e02-p99-sprite-first-preproduction-and-c3-producer-acceptance.md` | `10c8df7490f21c2df12c513981867fd0168e86f9e789e46105c192996d2d4bf1` | C3 fixture边界 |
| `108-c01e02-route-a2-modular-environment-and-interaction-user-approval.md` | 派发时锁定 | 用户批准与Route A2方法 |
| `c01e02-tactical-visual-interface-v1.json` | 派发时锁定（避免接口／任务书循环自哈希） | Candidate接口1.6.6与停门 |
| `golden_slice_profile.json` | `61b49e5328e702cd654d28ff39c5c380ba0ae3e78753330635036d33f689523c` | Current topology／玩法公开态 |
| `current_topology_map_contract.json` | `74c6bbb3f732a61d3ed5a55d9c209b628152b9411395339d665aeeb0d76ab875` | 当前对象／空间责任源，只读 |
| `visual_compositor_profile.json` | `13719d8a3bde0cc06acbed893198943164f2541cdc0b112cc5897ff38f4c3451` | C2/C3产品态与文案，只读 |
| `c3_neutral_atlas_binding.json` | `60ae9fe302779ace5570f674b379efe55fdc3d50ccd3b93895ce610ff2fcde30` | 中性Atlas proxy，只读 |

派发时必须补写108号与本文件自身SHA到交付回执；禁止修改上述输入来过测。

## 3. 唯一写域

允许新增：

- `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_a0_pilot/**`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_a0_pilot/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/m3_golden_slice/camera_a0_pilot/**`
- `game-godot/tests/candidate_runtime_demo/m3_golden_slice/g2_a2_visual_compositor/camera_a0_pilot/**`
- `scripts/test_c01e02_g2_a2_c4_camera_a0_pilot.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c4-camera-a0-pilot/**`

禁止修改：C2/C3脚本、Scene、证据包、Resolver、Session、PerformanceDirector、gameplay profile、current topology合同、visual profile、Default入口、Save、Canon、真实资产和生产看板／接口文件。

## 4. 相机对照实现

### 4.1 三档Candidate

- `CAM_A0_V1_40X20`：当前基线；
- `CAM_A0_V2A_40X24`：中等抬高；
- `CAM_A0_V2B_40X26`：较高俯视。

三档保持：

- 32×18、grid x=east／y=south；
- orthographic、无透视汇聚、无按y缩放；
- map viewport `[0,58,1280,584]`与UI安全区；
- 相同当前演员／对象anchor、footprint、facing、路线、状态与T1—T5；
- PLAN稳定总览，CONTACT impact world point居中；
- 所有单位注册点仍为footprint bottom-center。

公平对照唯一投影式：

```text
P_h(x,y) = ((x-y)*40, (x+y)*h)
screen = map_rect.center + P_h(cell) - P_h(focus)
zoom = 1.0
shake = [0,0]
```

语义焦点写死：

- A／B PLAN：`[19.75,9.75]`；
- A CONTACT：`[20.5,10.5]`；
- B CONTACT：`[20,10.5]`；
- no-focus数值回读：`[15,11]`。

相对crop为`P_h(focus)-[640,292]`、尺寸`1280×584`。每档独立派生world-to-screen、crop和四向screen vector，不把V1的`raw_origin/canvas_origin/crop`常量拼贴到新Y比率；2400×1350正式canvas本轮只报告fit余量，不冻结。40×20 Pilot还必须与现行`visual_projection.gd`控制点逐点≤0.5px，证明它是真基线；三档均须用至少三处grid控制点、六actor footpoint与A/B contact world point做外部数值回读，误差≤0.5px。

三个Pilot camera ID都必须`runtime_bindable=false`；C3 binding只读提供尺寸／注册测试来源，禁止修改C3 registry或把V2伪装成`CURRENT_TOPOLOGY_CAMERA_V1`。为比较遮挡和空间体量，三档使用同一组Candidate-only中性world-height proxy，由候选投影派生顶面／立面；固定V1平面Sprite不得冒充视角体量证明。本门只验证空间体量和遮挡，不验证馆守Z／BREAKER最终身份美术。

### 4.2 模块建筑proxy

将六个passable=false terrain zone在Pilot内实例化为六个独立对象；Pilot只作者化：

`object_id / grid_rect / world_height_class / z_bias / foundation / occluder / focusable`

`front_edge_footpoint / visual_bounds / reveal_cells`必须从`grid_rect + candidate projection + node bounds`派生，禁止作为第二套手填空间真值。front edge严格复用单位footprint-bottom-center公式：投影该grid_rect内所有占用格中心，`x=(min_screen_x+max_screen_x)/2`、`y=max_screen_y+tile_half_y`。foundation只画占地底座／不高于主体脚点的低立面并常显；所有会挡住单位主体的高立面／屋面只归occluder，禁止双份像素责任。

六建筑在三档使用同一`world_height_class`、结构、材质、alpha与状态，只能改变候选投影派生结果，不能为某档单独降低高度。对象与单位共用front-edge／footpoint Y排序。不得在Pilot中新增玩法碰撞、建筑HP、LOS、掩体或破坏规则。

## 5. 焦点驱动显隐实现

### 5.1 单一只读输入

```text
focus_context = {
  stage,
  focus_source,
  cursor_cell,
  mouse_hover_cell,
  selected_subject_ids,
  route_cells,
  planning_endpoint,
  focused_object_id,
  active_execution_subject_ids,
  camera_signature
}
```

- route／endpoint只读当前plan readback；
- selected subject固定读取当前可控馆守Z`V353U001`，不建设selection manager；
- building self-focus仅表示presentation焦点格落入该对象`grid_rect`，不建设建筑选择／Session状态；
- active execution subjects仅在`director.playing=true`、`event_id!=SEQUENCE_COMPLETE`且phase属于实际event阶段时读取当前performance frame的entity overrides；结束后进入100ms release hold，不得被settled entities粘住；
- Controller不得调用Session／Resolver／Director写方法；
- mouse motion只在跨grid cell时更新presentation focus；地图外清空；
- 手柄复用当前战术cursor并在真实手柄输入后清空mouse hover优先权；现有键盘没有格光标移动，本Pilot只做键盘no-regression，不新增键盘focus cursor。

### 5.2 状态机

- `OPAQUE=1.00`；
- `REVEALED target=0.34`；
- `RELEASE_HOLD=0.34`；
- 90ms reveal、100ms hold、160ms restore；同签名dedupe。

理由优先级：

`execution > selected > route_or_endpoint > building_self_focus_exception > cursor`

建筑自身focus保持不透明并高亮；但其后有selected／execution主体时，主体可读性优先。CONTACT挡住双方的对象保持透明到动作读清。只淡实际相交对象；同屏通常≤2是构图目标，不得漏掉真实第3个遮挡对象。

### 5.3 简化技术边界

唯一Owner只改独立occluder CanvasItem的`self_modulate.a`。严禁：

`SubViewport / ViewportTexture / pixel mask / alpha contour / per-pixel shader / normal map / realtime light / actor alpha mutation / second occlusion owner`

C4使用一个独立Scene与C4-only `PilotProjection`，启动前注入候选参数；不得修改或放松现有`visual_projection.gd`、C3 registry的40×20／Camera V1 fail-closed。C4中只存在一个`ModularStructureOwner`：旧`STRUCTURES_CURRENT`与旧roof owner不得实例化或必须在首个可见帧前禁用，严禁六栋立面／屋顶双画。C3中性Atlas至多作为只读尺寸／颜色来源，不得冒充V2 camera绑定；C3原Scene只做回归。

## 6. 必交actual frames

### 6.1 相机对照：12张1280×720非headless帧

每档各四张：

1. `A_PLAN`
2. `B_PLAN`
3. `A_CONTACT`
4. `B_CONTACT`

所有帧使用同一proxy身份、同一UI状态与同一时态；禁止通过挪actor／object或隐藏建筑美化某档。

### 6.2 遮挡交互：至少8张

总计8张，不是每档8张：

- V2-A完整交互链6张：`OPAQUE_BASELINE / MOUSE_HOVER_REVEAL / BUILDING_SELF_FOCUS_STAYS_OPAQUE / ROUTE_ENDPOINT_REVEAL / T3_CONTACT_AUTO_REVEAL / RELEASE_RESTORED`；
- V2-B交叉验证2张：`OPAQUE_BASELINE / CONTROLLER_CURSOR_REVEAL`。

鼠标与手柄对同一格的一致性通过真实InputEvent trace和机器回执证明，不额外堆截图；键盘只证明既有输入无退化。每个同名状态在三档间snapshot／UI／time／weather完全相同；A PLAN、B PLAN、A CONTACT、B CONTACT彼此保留原合法差异。两设备的`revealed_object_ids / alpha / bounds`必须一致；以冻结时钟和数值receipt证明非目标对象、actor、ground、FX状态不变，不要求雨FX全帧字节相同。

## 7. 机器门与负测

必须证明：

- 玩法输入文件派发前后SHA一致；
- A/B route、contact、world result、T1—T5 token一致；
- hover前后draft signature、resolver token、intent token、commit count完全不变；
- 地图外hover、同cell重复motion、非相交cursor／path不触发；
- self-focus不淡，但不能压制selected／execution理由；
- invalid cell、unknown subject、dead／invisible subject忽略并fail-closed opaque；
- 缺object metadata或重复Owner启动失败，不fallback全层淡化；
- camera变化后无旧bounds残留；
- actor alpha／material／Atlas region／pivot／shadow不变；
- C3原Scene与证据字节不变；
- Scene tree无复杂遮挡节点或第二Owner。

性能：

- 300次mouse motion与手柄扫格，decision仅在grid／签名变化时运行；键盘执行既有输入no-regression；
- 预热后的纯焦点判定函数记录CPU p95／max作为诊断，不设脱离整机帧时的微秒级硬门；
- texture/node count不增长、reload=0；Pilot内唯一Ground proxy的`queue_redraw_count`在纯focus变化前后为0；
- 整体Pilot至少满足fixture 30fps：p95≤33.3ms、max≤33.3ms、0帧>33.3；
- 本任务不得宣称最终60fps。真实美术完成后仍执行p95≤16.7ms、max≤33.3ms的正式门。

## 8. 制作人／用户视觉门

每档按同一四问表评分，不由程序自动选优：

| 门 | 失败表现 |
|---|---|
| 巨体体量 | 俯视过高、机体变扁或方向难辨 |
| 地图第一读法 | 3秒说不出车、东门、北冲、馆守Z承接 |
| 建筑存在感 | 正常态像贴片／摆设，或遮挡过强 |
| 显隐可用性 | 淡化后阻挡范围消失、全图变淡或CONTACT仍看不清 |

通过后只签：`CAMERA_A0_COMPARISON_COMPLETE / FOCUS_REVEAL_INTERACTION_SUPPORTED / AWAITING_USER_CAMERA_SELECTION`。P109用户选定候选后仍须执行C4B精确接口重注册，ENV-A1不得直接消费本Pilot临时camera ID。

停止于：`P109_CAMERA_A0_AND_FOCUS_REVEAL_PRODUCER_USER_VISUAL_SELECTION`。

## 9. 禁止过报

本任务不得声明：

`FINAL_CAMERA_V2 / ENVIRONMENT_ART_APPROVED / REAL_ART / FINAL_60FPS / FUN_PROVEN / UGT_READY / UA91 / G2-B / Default / Save / Runtime / Canon`
