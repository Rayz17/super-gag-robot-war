# C01E02 A9.1-A6-S-C2｜Sprite-First地图相机母版预生产任务书

日期：2026-08-20  
任务ID：`A9_1A6_S_C2_SPRITE_FIRST_MAP_CAMERA_MASTER_PREPRODUCTION`  
执行者：美术资产-2  
状态：`READY_FOR_DISPATCH / PREPRODUCTION_ONLY / IMAGEGEN_FALSE`

## 1. 唯一任务

在Call02整屏身份与注册失败后，把视觉生产拆成四个互不冒充的责任层：

1. current-topology静态环境与可分离对象槽；
2. 馆守Z／BREAKER单主体地图相机母版；
3. 小体／车辆／对象／UI／路线的确定性消费层；
4. 母版通过后才扩展的稀疏state×facing×frame clip。

本任务只做来源冻结、exact view-space／pivot／socket guide、环境donor裁切、组合模板与两次剩余调用的逐次任务预案。**不得调用ImageGen，不得生成可见目标像素，不得把程序几何当美术成品。**

## 2. 根因与纠偏边界

Call02证明整屏生成器不能同时忠实承担身份、地图相机、脚点注册、对象拓扑和环境完成度。后续禁止：

- 继续以Call02为父图生成CONTACT；
- 在错误整屏上挪机体、补脸、改轮廓并声称修复；
- 把V10X眼平正／侧／背四视裁成地图cardinal；
- 把B样张或X关系板单独冒充最终B＋X母版；
- 使用Blender／Python／SVG原语直接画最终可见机体；
- 一次性铺满四向×全状态Atlas。

程序绘制只可用于投影、脚点、占地、方向箭头、socket、bbox、mask和组合QA；画面美术必须另过50%／100%视觉门。

## 3. 冻结身份责任源

### 3.1 馆守Z

| 角色 | 路径 | SHA-256 | 允许用途 |
|---|---|---|---|
| Hard校准锚 | `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png` | `a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521` | 身份偏差校准，不作地图图 |
| E02 V10X派生父图 | `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png` | `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade` | 双臂、裸机、无翼背结构责任源 |
| 最新Q／SD身份源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_imagegen_v2.png` | `c701f3efa72301720117bae08b1479d704315c5a4de62034bf385263ea57f412` | 约四头身、结构／配色／重量参考 |
| 正交四向审查源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png` | `3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9` | 跨面身份一致性；禁止直接当地图四向 |
| 已批动作空间方向板 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png` | `4d8e7975649b2b85458a838afd9bc2fe8e3a90fd8cbcfe8a7929b8ae9ae6c225` | 约4.2头身／动作空间约束，非exact mask |

### 3.2 BREAKER

| 角色 | 路径 | SHA-256 | 允许用途 |
|---|---|---|---|
| 用户批准B身体关系 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png` | `7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868` | 高背壳、低嵌头、前肢承重半直立、短后足 |
| 用户批准X表面关系 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png` | `cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85` | 异质生体甲、柔性缝与三处闭合关系 |
| B 128方向样张 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png` | `e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4` | 外轮廓／尺度／pivot方向校准；X尚未烘入，非成品 |

### 3.3 共同画法与小体

- CML128 KINETIC_CEL：`docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png`，SHA `8a546082e8fd2f1b0f9c6e8a8b1e602a647f478112887e93a8f44148e4867842`；只取线色、材质、硬阴影和运动感，禁止继承其中机体解剖。
- A5小体地图相机Atlas：`docs/superpowers/specs/production/c01-current-demo-v1/art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png`，SHA `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b`；继续作为当前三只小体身份／相机正例，不重生成。

Call02两台巨体与三小体像素永久排除；Call02只允许裁出不含任何单位／对象／文字的局部环境材质donor。

## 4. 唯一地图相机与注册

共同接口：

- `view_space=map_dimetric_40x20`；
- `camera_contract_id=CURRENT_TOPOLOGY_CAMERA_V1`；
- 2:1正交二测，世界north→屏幕右上`(+40,-20)`，east→右下`(+40,+20)`，south→左下`(-40,+20)`，west→左上`(-40,-20)`；
- `registration_point=footprint_bottom_center`；
- `sort_key=footpoint_screen_y + explicit_z_bias`；
- 不允许跨facing fallback，不允许眼平四视别名为地图方向。

### 馆守Z PLAN单帧槽

- `native_size=[256,256]`；`footprint=[2,2]`；
- `pivot_normalized=[0.5,0.875]`；`pivot_px=[128,224]`；
- 首帧clip=`idle/east/0`；east正面向量必须落在屏幕右下；
- PLAN是站定待命、非接触、非后坐；可见顶面与地图俯视一致；
- frame内必须留出未来`body/shield/weapon/impact/target` socket，不可把肢体贴边裁死。

### BREAKER PLAN单帧槽

- `native_size=[384,384]`；`footprint=[3,3]`；
- `pivot_normalized=[0.5,0.8333333333]`；`pivot_px=[192,320]`；
- 首帧clip=`charge/north/0`；north正面向量必须落在屏幕右上；
- PLAN为压低重心、尚未接触的蓄冲，不得画成四足龟伏或车辆；
- frame内必须留出未来`body/shield/weapon/impact/target` socket与T4侧甲受击区。

256／384是当前Candidate消费者槽，不等于Hard美术尺寸。预生产必须做同屏50%尺度板，确认18m馆守Z与近30m BREAKER的体量、占地和选择口袋可读；若视觉尺度需改，先停回制作人改接口，禁止美术自行缩放。

### 4.1 真实Atlas消费者前置门

当前G2-A2-C1／C2的`CompoundMapActor`仍是`Polygon2D` Proxy：它会校验clip metadata，却没有真实加载PNG／`AtlasTexture.region`。因此本预生产包通过后，Call03以前必须由独立主程序P0任务证明：

- 256／384中性透明测试Atlas被专用current-topology Scene真实加载；
- sparse clip rect随state／facing／frame变化；
- `pivot_px`对齐`footprint_bottom_center`，z-sort、局部roof mask与五socket读回闭合；
- 缺clip严格fail-closed但连续T1–T5不丢角色；
- `approved_handoffs=[] / real_art_loaded=0`，中性测试图不冒充真实美术。

此门未过，不能因JSON槽齐全就生成母版。

### 4.2 socket与shadow所有权

预生产须新增`socket-contact-contract.json`并明确socket坐标基准为**相对footpoint的local offset**，不得与旧R2的frame-top-left坐标混用。当前Proxy校准起点为：

- 馆守Z：`body=[0,-74] / shield=[-46,-62] / weapon=[46,-72] / impact=[-20,-10] / target=[-20,-10]`；
- BREAKER：`body=[0,-98] / shield=[-68,-84] / weapon=[68,-96] / impact=[12,-18] / target=[12,-18]`。

这些是生成前的语义区与目标容差，不是未经测量的最终像素真值。单帧出图后必须按alpha轮廓实测并在PLAN重组前回填；CONTACT派生前再以A world impact`[20.5,10.5]`、B world impact`[20,10.5]`做联合签收。

shadow唯一由引擎独立层持有；主体PNG禁止烘入地面投影。若未来美术阴影取代引擎阴影，必须另改接口并显式关闭原shadow，绝不允许双影。

### 4.3 环境交付空间

1280×720 actor-free图只负责PLAN framing与生成／绘制guide。未来可运行环境不能只交屏幕截图，须保持`2400×1350` world canvas与`canvas_origin=[-1760,-340]`，并分离：

- base／building world body；
- roof／foreground；
- occlusion／weather控制；
- 可变盾、门、设施与保护区overlay。

任何屏幕cleanplate都不能取代world canvas、共同origin或可变对象层。

## 5. 必交预生产包

唯一新目录：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c2-sprite-first-map-camera-masters/**`

必须交：

1. `source-lineage.tsv`：绝对路径、SHA、authority、view_space、允许／禁止用途；
2. `map-camera-slot-contract.json`：上述两槽的canvas、footprint、pivot、facing vector、z_bias、socket占位与fail-closed规则；
3. `GUARDIAN_Z_EAST_MAP_CAMERA_GEOMETRY_GUIDE_256.png`：只含脚点、2×2投影、east向量、bbox安全区、socket占位与结构文字标记；无成品像素；
4. `BREAKER_NORTH_MAP_CAMERA_GEOMETRY_GUIDE_384.png`：只含脚点、3×3投影、north向量、bbox安全区、socket／侧甲区与B轮廓正负空间标记；无成品像素；
5. 两张**完全隔离**的safe reference board：GZ板不得含BREAKER像素；BREAKER板不得含馆守Z像素；共同CML128区只能是无机体的线色／环境裁切或规则卡；
6. `CURRENT_TOPOLOGY_ACTOR_FREE_WORLD_GUIDE_1280x720.png`：严格使用共同PLAN相机、current block／road／selection-pocket／charge-avenue；动态单位、车、三小体、墙挂盾、东门、设施、保护区overlay和UI全部为空槽；只作环境生成／绘制几何guide；另交`environment-layer-contract.json`写清未来2400×1350 world canvas、共同origin与四类分层；
7. Call02环境donor crop sheet：每一格必须不含机体、小体、车辆、盾、门、设施、伪字或旧语义对象，并登记raw父图坐标／SHA；
8. `PLAN_SLOT_COMPOSITE_QA_1280x720.png`：用纯色slot／A5小体／当前对象proxy证明所有脚点0px、选择口袋无遮挡、屋顶局部mask与50%尺度关系；不得冒充美术候选；
9. `first-round-state-facing-phase-matrix.tsv`：只规划不绘制，并逐项声明`new_frame`或带签名的同facing alias／engine tween，禁止跨facing fallback。馆守Z至少闭合`idle/east`、`move/east,north`、`brace/east,north,south`、`contact/south`、`recoil/east,south`；BREAKER闭合`charge/contact/recoil/side_hit/red_charge`的north；车辆须覆盖`waiting/drive/recoil/passed east`，小体01须覆盖`idle/move/recoil/deflected west`，其余小体保持各自idle facing。离散capture无missing clip不能替代连续phase矩阵证明；
10. `atlas-schema-current.json`：直接使用`CURRENT_TOPOLOGY_CAMERA_V1`，冻结resource路径／SHA、stable／slot／revision、native／atlas size、sparse rect、fps／hold／loop、filter／mipmap、state alias签名、双pivot、z_bias、五socket与fail-closed；旧M2 96／128四向横条schema只作History donor，不得alias回退；
11. `socket-contact-contract.json`：记录上述local offset基准、语义目标区／容差、A／B world contact与shadow唯一owner；
12. `call03-call04-plan.md`：逐次引用图、prompt职责、solid-background／alpha策略、失败门与剩余预算；
13. generation log明确`ImageGen calls=0`、delivery hashes、完成报告。

所有guide必须醒目标记`GEOMETRY_GUIDE_ONLY / NOT_VISIBLE_ART / NOT_RUNTIME`。

## 6. 剩余两次调用的预案（本任务不得执行）

### 未来Call03：BREAKER单主体地图母版

只有制作人签收本预生产包后才能另行逐字授权。唯一目标：`BREAKER_PLAN_MAP_CAMERA_MASTER_NORTH_RGBA_384`。

四图职责建议：exact 384 guide、B身份板、X关系板、无机体CML128 style-only板。输出必须是单主体、均匀纯色背景、无地面／环境／文字／第二台机体／接触FX；后处理只允许抠背景、despill、裁切到固定canvas与登记pivot，不允许重画身体或挪肢体。

50%先过“前肢承重半直立、短后足、低嵌头、高背壳、不是龟／猿／普通四足／车”；100%再过X柔性缝、异质甲、闭胸缝、封背出口与单红缝。任一失败即停，Call04保留不用。

### 未来Call04：馆守Z单主体地图母版

只有Call03通过制作人50%／100%门后才可另行授权。唯一目标：`GUARDIAN_Z_PLAN_MAP_CAMERA_MASTER_EAST_RGBA_256`。

四图职责建议：exact 256 guide、V10X父图、最新Q／SD身份源、无机体CML128 style-only板。必须过约四头身旧超级系重量、金冠／银栅格脸、红X胸甲与金核、方肩环、等重圆柱前臂、双臂、无翼、无背包；east地图视角必须可见顶面，禁止正交侧视纸片。失败不reroll。

两次调用均不是Atlas、Runtime或用户母版批准。若两次均通过，才允许把单帧装入确定性PLAN整屏重组并送制作人视觉门；不得自动扩动作。

## 7. 停止门

出现任一项立即停止：

- source SHA／权限不闭合；
- guide与`CURRENT_TOPOLOGY_CAMERA_V1`或pivot不一致；
- 当前C2真实Atlas中性夹具消费尚未通过；
- 连续phase矩阵、socket基准／容差、shadow owner或current atlas schema未闭合；
- safe board出现另一台机体、CML128翼背或Call02错误机体；
- actor-free guide烘入动态对象、旧A4坐标或保护区发光实体；
- 以程序图形、旧正交四视或Call02整屏像素冒充目标美术；
- 任何ImageGen调用、Call03／Call04、Godot真实像素接入、UA91、G2-B、Runtime、Canon或付费批量生成。

完成后停在制作人预审；`real_art_loaded=0 / FUN_NOT_PROVEN`保持不变。
