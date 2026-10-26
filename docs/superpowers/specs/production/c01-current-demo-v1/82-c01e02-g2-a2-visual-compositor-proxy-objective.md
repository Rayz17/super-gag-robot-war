# C01E02｜G2-A.2精品视觉合成器Proxy唯一任务书

> 日期：2026-08-20  
> Owner：新“主程序-2”任务 `01a01a2b-1d03-7831-b419-10cf39477ac9`  
> 状态：`RESUMED_BY_84 / VISUAL_SYSTEM_PROXY_ONLY / REAL_ART_LOADED_ZERO / G2_B_FORBIDDEN`  
> 上游唯一放行：84号R2C-C1制作人重新签收  
> 不构成：真实美术接入、视觉品质批准、UA91、G2-B、Runtime晋级、默认入口、Canon修改

## 1. 任务目的

把现有“能算对的战棋几何”升级为“能够可靠承载精品美术的画面系统”。本任务不画馆守Z或BREAKER，不接入任何单位／人物Candidate真实像素；只用无身份Proxy证明六层地图、复合Actor、局部遮挡、路线与威胁Overlay、雨夜挂点、通讯安全区和性能可以在同一个1280×720运行帧中工作。

唯一例外：允许只读绑定用户已批准的A4六层作为`fixture_validation_only`地图责任源，用于共同canvas／crop／mask／遮挡验证；它沿用R2C口径，不计入Golden Turn真实美术，manifest仍必须保持`approved_handoffs=[] / real_art_loaded=0`。禁止读取或接入A9、V10X、B＋X、CML001或81号新图的可见像素。

G2-A.2通过只代表消费者准备好，不代表目标画面达到精品质量。它必须与A9.1-A6-S、A9.1-A6-D以及联合Gold Frame重组共同过门。

## 2. 必读输入与边界

1. `84-c01e02-r2c-c1-producer-reacceptance-and-parallel-resume-receipt.md`
2. `83-c01e02-r2c-c1-primary-swarm-ground-occupancy-correction-objective.md`
3. `80-c01e02-r2c-producer-exact-geometry-acceptance-and-parallel-visual-dispatch.md`
4. `78-c01e02-scene-first-visual-composition-and-joint-gold-frame-replan.md`
5. `76-c01e02-tactical-perspective-interaction-and-asset-interface-correction.md`
6. `c01e02-tactical-visual-interface-v1.json`
7. `main-g2-a1-r2c/04-actual-frame-manifest.json`
8. `main-g2-a1-r2c/05-a4-layer-registration-readback.json`
9. `main-g2-a1-r2c-c1/**`
10. `56-c01e02-golden-slice-master-contract.md`

必须重新完整使用`chao-gag-canon`。本任务只修改隔离Candidate路径；不得把C01E02 Demo逻辑写入Current Canon，不得改Reader或正式V35活动点。

84号已恢复本任务新增实现。必须保留纠偏后的R2C resolver、A/B world result、动态占位、T1–T5时序、contact socket与T4 side socket语义。若视觉系统需要不同空间数据，应新增只读adapter／manifest，不得改玩法结果迁就画面。

## 3. exact输入

严格消费80号冻结值：

```text
camera_contract_id     = A4_MAP_SPRITE_CAMERA_V1
projection             = 32x18 / tile_half [40,20] / origin [-880,-170]
viewport               = 1280x720
map_viewport_rect      = [0,58,1280,584]
camera_center          = [-720,350]
zoom                   = 1.0
A4 canvas              = 2400x1350
A4 canvas_origin       = [-1680,-350]
A4 crop                = [480,428,1280,584]
Hero PLAN focus        = [19,10]
Hero CONTACT focus     = [20.5,10.5]
B PLAN focus           = [18.5,10]
B CONTACT focus        = [20,10.5]
B impact raw           = [-500,440]
A Swarm01 post         = [22,9] / grounded / 1x1 / blocks_route=false
```

A/B anchor、facing、socket、post state一律从R2C receipt／resolver读取，不在UI或capture driver手填第二套真相。

整屏消费者还必须从profile／resolver读取并显示：馆守Z初始`[15,11] east`、BREAKER初始`[20,13] north`、应急车`[17,10] east`及T1终点`[24,9]`、三只小体、东侧撤离口`[31,7]`、警戒设施`[27,8]`、墙挂重盾`[14,10]`、保护区rect`[20,5,12,7]`与炮源`[29,2]`。禁止只证明两只巨体而把交互对象做成自由摆放背景。

## 4. 必须实现的画面系统

### G2-A2.0 新隔离子树，不继续膨胀旧View

- 新建独立`g2_a2_visual_compositor/`内容、脚本与Scene子树，并提供专用非默认入口Scene。
- 现有约1425行`tactical_world_view.gd`、shared-round resolver／session、performance director和R2C capture driver全部只读；G2-A.2通过adapter消费其公开状态，不把新系统继续塞进旧单体View。
- 专用Scene不得进入默认启动器、save或Runtime；只供测试、Actual Frame、序列和联合重组预演。
- 若现有公开状态确实不足，先在报告中列出缺字段和最小bridge提案并停门；不得直接改resolver／session语义。

### G2-A2.1 六层地图合成器

- 六层共享2400×1350 canvas、origin、crop、zoom、filter与明确z语义。
- layer binding必须校验`view_space=map_dimetric_40x20`和`camera_contract_id=A4_MAP_SPRITE_CAMERA_V1`。
- 提供base、buildings、state／lighting、roofs、foreground、occlusion control的独立开关与只读debug manifest。
- filter必须按slot显式配置并写回manifest；不得沿用全局nearest默认值。A4地图Proxy至少比较nearest／linear后记录选择，未来单位slot保持独立可配。
- 现有A4 `STATE_LAYERS`只作Proxy输入；不得把混包状态层登记成正式real art。
- 禁止再次把任意小图scale成地图层来冒充六层注册完成。

### G2-A2.2 局部遮挡与深度

- unit sort key继续取`footpoint_screen_y + explicit small z bias`。
- roofs／foreground不能因一个单位进入mask就让整层统一降到50%。
- A4 occlusion mask通道语义冻结为：`R=fade fill / G=roof outline / B=safety fringe / A=coverage`；不得另造第二套通道解释。
- 必须实现局部mask采样后的局部fade、cutout或局部outline Candidate方案；受影响区域应跟随单位可见轮廓或footprint扩张区。
- 局部fade只能修改命中的patch，patch外roof／foreground像素alpha必须逐像素保持不变；outline必须来自CompoundActor真实alpha外轮廓，不得继续用footpoint圆环替代。
- 同一帧必须证明：1×1、2×2、3×3在建筑前后交叉时，前后关系由footpoint决定；高处机体不被整张屋顶无差别抹掉。
- 输出无遮挡／遮挡／debug mask三联actual frame；debug只用于证据，不进入产品目标帧。

### G2-A2.3 复合地图Actor

实现通用无身份`CompoundMapActor`或等价节点：

```text
root registration = footprint_bottom_center
children          = shadow / body / attachment / emissive / fx
sort source       = footpoint screen y
binding           = sparse state/facing/frame rect map
sockets           = body / shield / weapon / impact / target
```

- 每个child使用同一frame-local注册合同，可有显式小offset，不得各自猜anchor。
- shadow与地面接触一致；attachment可在不换整张body的情况下挂盾或局部件；emissive可独立做BREAKER red seam代理；fx不改变逻辑碰撞。
- 错误view_space、camera ID、pivot、canvas或缺失socket必须fail closed。
- Proxy只能用中性几何／校准轮廓，禁止仿画馆守Z、BREAKER或把旧失败Sprite当“临时真实资产”。
- Actor只允许一个ground anchor真值。A路Swarm01必须直接消费纠偏后的`[22,9]`，不得新增`display_anchor`、airborne offset或视觉别名来回避占位；测试必须证明其1×1 ground rect与馆守Z2×2、BREAKER3×3均不相交。

### G2-A2.4 正式Overlay Renderer

从同一projection与resolver数据绘制：

- 路径带、逐段方向、waypoint、2×2终点ghost、最终facing fan；
- 最多三个最高威胁、BREAKER north冲撞走廊、保护线、接触预测区；
- impact socket、contact edge、normal、impulse、recoil与T4侧甲射线；
- A／B提交摘要中的真实代价，包含A较宽余量与B高热／零余量。
- 应急车、小体、BREAKER三条公开意图轨迹，以及撤离口、警戒设施、重盾、保护区与炮源的exact位置。

禁止默认铺满全图网格；只有编辑路线或debug时显示必要格。产品帧不得出现坐标、hash、Stable ID、Candidate或英文调试字段。

### G2-A2.5 通讯、目标和时间线安全区

- PLAN阶段支持左侧大型通讯Presenter，但宽度不得超过屏宽25%，不能遮住路线、终点、冲撞走廊或接触预测。
- CONTACT前Presenter必须在明确时点退到窄状态条或完全退出；CONTACT画面在地图viewport内部的无遮挡可见面积至少88%（不是按全屏面积计算）。
- 顶部只保留一个当前目标与最多三个最高威胁。
- 底部时间线只显示车辆、小体、巨体接触、城市炮、赤红蓄能五时点。
- 命令抽屉在移动光标时可收起；中央60%保持战术安全区。
- 本任务只用中性人物框／占位构图，不加载纪存真实美术。
- 确定性文案冻结为：目标`让应急车通过，挡开扑向东门的小体，并站到冲线前。`；纪存句`人都在后面。把它引到南边去。`；威胁依次为`应急车先穿过落脚区`、`小体将在第二时点扑向东门`、`BREAKER沿直线冲入街区`；五时点标签依次为`应急车 / 小体 / 巨体接触 / 城市炮 / 赤红蓄能`。
- A已选摘要为`卡位迎撞｜正面承接｜较低热量｜第二轮余量1`；B备选为`护线预备｜先east护线、接触前转south｜高热｜第二轮余量0`。不得用自造占位文案证明排版。

### G2-A2.6 雨夜、湿地与重量挂点

- 远雨／近雨分层，不与地图同速；提供雨量、风向和前后景开关。
- 提供湿地mask、低成本烘焙反射／局部扰动挂点、foot splash和重步水花接口。
- 接触表现挂点必须共享R2C socket：hit-stop、定向shake、单帧高光、debris、水花、recoil、road damage mask。
- `A_CONTACT_COMPOSITOR_PROXY`严格冻结T3.00：实体只发生接触微裂、小碎屑和水花；T4炮击、T5赤红蓄能与完整路面翻起只允许HUD预示，不能提前播放实体FX。
- Proxy音频只验证触发与bus ducking；现有合成音不冒充正式SFX。
- LibTV／Cut-in不在本任务实现；第一次巨体接触必须在地图系统里完整可读。

### G2-A2.7 联合重组接口

导出机器可读`visual_compositor_slot_manifest.json`，至少包含：

- map layers与共同canvas／origin／crop／filter／z／mask；
- CompoundActor各slot、view_space、camera、frame canvas、pivot、display scale、footprint、sockets、sparse clips；
- Overlay数据来源与screen safe zones；
- rain／wet／damage／FX挂点；
- `GF_PLAN_RECOMPOSED`和`GF_CONTACT_RECOMPOSED`所需的capture state ID。

该manifest是A9.1-A6-D／A9.1-A7-J的消费者接口草案，不是signed exact handoff；UA91后仍需制作人冻结。

## 5. 唯一写域

- `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/**`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/**`
- `game-godot/tests/candidate_runtime_demo/m3_golden_slice/g2_a2_visual_compositor/**`
- `scripts/test_c01e02_m3_golden_slice_g2_a2.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2/**`

不得修改Canon、Reader、A4/A5源、美术任务目录、旧Runner、默认入口、save、Runtime晋级文件或其他任务回执；不得git add／commit／clean。

共享R2C文件、现有`tactical_world_view.gd`、resolver、session、director和capture driver均不在本任务写域。若独立adapter无法完成，必须以`BLOCKED_BY_MINIMAL_BRIDGE_DECISION`停门，不得扩大写域。不得覆盖R2C交付目录中的旧证据。

## 6. 必交actual evidence

至少交六张1280×720 Godot root viewport实际帧：

1. `A_PLAN_COMPOSITOR_PROXY`：六层、路线、终点、威胁、五时点、通讯安全区；
2. `A_CONTACT_COMPOSITOR_PROXY`：通讯退场、全前缘接触、socket／normal／recoil、道路状态挂点；
3. `B_EAST_TO_SOUTH_PROXY`：T2 east护线到T3 south接触的可见状态变化；
4. `LOCAL_OCCLUSION_BEFORE_AFTER`：局部fade／cutout而非全层变淡；
5. `COMPOUND_ACTOR_SLOT_DEBUG`：shadow/body/attachment/emissive/fx与共同footpoint；
6. `RAIN_WET_PERFORMANCE_PROXY`：远近雨、湿地／水花挂点同时开启。

另交一个不少于10秒的实际运行序列证据或逐帧trace，由现有session／performance事件推进而不是capture driver直接注入阶段状态，证明Presenter退场、route逐段facing、contact hit-stop与recoil不是静态注入的五张孤立图。

## 7. 性能与资源门

在当前开发机1280×720下，加载六层、三类CompoundActor、Overlay、雨与FX Proxy后：

- 先预热120帧，再采样至少600帧；
- 报告平均、p95与最大frame time，不得只写“60 FPS”；
- 报告设备型号、Godot版本、rendering method／driver、分辨率和vsync状态；
- 必须在非headless实际渲染下采样，600帧采样窗口内禁止截图编码、磁盘日志刷写或其他capture IO；截图和序列留档在采样结束后单独进行；
- 目标`p95 <= 16.7ms`、`max <= 33.3ms`；未达标则标记BLOCKED并给出热点，不得降低画面系统语义掩盖；
- 报告绑定贴图数量、原生尺寸、估算未压缩内存、过滤模式和重复加载检查；
- 禁止把隐藏整层仍留在每帧重绘或为每个雨滴创建独立高开销节点。

该结果只代表当前开发机Candidate证据，不外推正式最低配置。

## 8. 必交回执

目录：`docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2/`

1. `01-input-receipt.tsv`：路径、SHA、authority、写域；
2. `02-system-architecture.md`；
3. `03-layer-registration-and-occlusion-proof.json`；
4. `04-compound-actor-and-socket-proof.json`；
5. `05-overlay-and-safe-zone-proof.json`；
6. `06-visual-compositor-slot-manifest.json`；
7. `07-actual-frame-manifest.json`与captures；
8. `08-sequence-and-performance-report.md`与原始日志；
9. `09-test-report.md`；
10. `10-completion-report.md`；
11. `delivery-hashes.sha256`。

专用测试外，还必须回归R2C、11项Golden Slice／G2-A1 suite、全仓Godot与Canon report／strict。

## 9. 停止门

完成后状态只能是`G2_A2_PROXY_READY_FOR_PRODUCER_SYSTEM_REVIEW`。

继续禁止：

- `real_art_loaded > 0`；
- 馆守Z／BREAKER／纪存真实像素；
- 用Proxy实际帧声称A9.1-A6-S视觉通过；
- UA91、A9.1-B、G2-B、Default Entry、Runtime、save或Canon；
- 为追求截图好看而改A/B路线、socket、contact normal、world result或事件时序。
