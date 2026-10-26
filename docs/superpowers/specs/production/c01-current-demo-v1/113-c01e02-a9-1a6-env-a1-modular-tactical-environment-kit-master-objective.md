# C01E02 A9.1-A6 ENV-A1｜40×24模块化精品战术环境套件任务书

日期：2026-08-21  
任务ID：`A9_1A6_ENV_A1_MODULAR_TACTICAL_ENVIRONMENT_KIT_MASTER`  
执行者：美术资产-2  
状态：`DISPATCH_READY / ONE_ENVIRONMENT_IMAGEGEN_CALL / NO_REROLL / NO_CHARACTERS`

## 1. 唯一目标

在已签40×24 Camera V2和current-topology玩法空间上，制作一套可由Godot确定性摆放、排序和整件淡出的精品环境Candidate：

`GroundBake + 6个独立Structure资源 + 独立战术物件／道路结果资源`。

本任务不是生成一张完整战斗场景，也不是把建筑、盾、东门、设施和结果烘进地图底图。建筑与物件必须作为有占地、有前缘脚点、有战术存在感的单独资源；只有地面、道路、排水、低矮铺装和不承担玩法的轻微环境光影可以进入GroundBake。

## 2. 开工顺序与工具

1. 必须先完整读取并使用`chao-gag-canon`与`imagegen`技能；
2. 逐项核对本任务冻结输入的绝对路径和SHA；
3. 先做一张无角色、无文字的模块化生成guide，不设置新的制作人预生图停门；
4. 使用ImageGen**恰好1次**生成模块化环境套件母板；
5. 只做抠背景、despill、裁切、alpha清理、色阶统一、模块拆分与确定性装配，不准重画结构来掩盖生成失败；
6. 自动完成50%／100%自审和交付封包后停回P102。

本任务没有reroll。首次调用如果不能提供可分离、可用的环境基础，就记录失败并停止，不得自动调用第二次。

## 3. 冻结输入

### 3.1 权威与空间

| 输入 | 路径 | SHA-256 | 用途 |
|---|---|---|---|
| Route A2用户批准 | `108-c01e02-route-a2-modular-environment-and-interaction-user-approval.md` | `c33bc0ffa4fe6f5ecc553001e640eba18a39a917a0c4691def8c940ca0ad0280` | 独立建筑／物件与显隐交互上位责任 |
| P111制作人签收 | `112-c01e02-p111-camera-v2-exact-interface-producer-acceptance.md` | 派工时锁定 | ENV-A1调用与相机放行 |
| Camera V2 exact合同 | `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json` | `756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a` | 32×18、40×24、world canvas、四相机 |
| 建筑／对象注册表 | `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv` | `0133cf5c5af7a6dba659221249b9e0bb45c51bebc8cb9b81c50cf9d920d25b7b` | 六结构、独立物件、前缘与crop |
| Task111实际帧manifest | `main-g2-a2-c4b-camera-v2-freeze/receipts/06-camera-v2-capture-manifest.json` | `4275e63d9b748ce512995fa7cc316186d48dcb9fb4b1ab71c20507d639233242` | 只作摆位／安全区／遮挡校验 |

唯一相机为：

- `camera_contract_id=CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`；
- `view_space=map_dimetric_40x24`；
- 正交dimetric，无透视汇聚、无按y缩放；
- world canvas `2400×1350`，origin `[-920,-99]`；
- `registration_point=footprint_bottom_center`；
- 建筑排序使用`structure_front_edge`，不得用anchor y或固定全层z替代。

### 3.2 只准借画法的环境参考

| 输入 | 路径 | SHA-256 | 允许用途 |
|---|---|---|---|
| A4方法板 | `art-a9-1a6-s-c1-current-topology-scene-first/map-language-board.png` | `4776660f7ab282f1434286e6670f080256b56a3208f2f5a0d13b754b78797819` | 只供美术先阅读暗值、湿地、工业分面、屋顶边灯、局部遮挡方法；不得作为ImageGen像素参考，不得继承旧拓扑 |
| Call02无语义环境裁片板 | `art-a9-1a6-s-c2-sprite-first-map-camera-masters/CALL02_ENVIRONMENT_METHOD_DONOR_CROP_SHEET_1600x1200.png` | `4dba9ba7590edb227a934dd4e363da1cc9718e316a01469d76230c4cd1450273` | 材质、雨湿、冷暖灯色方法；不得继承任何对象坐标或轮廓 |

禁止把以下内容作为ImageGen参考或可见像素父图：旧A4整层、Call02整屏、ENV-E0 E1/E2失败像素、旧盾／门／设施、任何馆守Z／BREAKER／车辆／小体像素、含机体解剖的CML128图格。

## 4. 唯一一次ImageGen调用

### 4.1 生成对象

生成一张**无文字、无角色、纯色分隔背景的模块化战术环境资产母板**，而不是战斗场景截图。母板必须在同一40×24地图视角和同一雨夜工业画法中清楚分隔：

- 3—4组可平铺的湿地／道路／路缘／排水材质模块；
- 6栋互不接触的旧会展街区Structure：`NW_BLOCK`、`NM_BLOCK`、`NE_BLOCK`、`SW_BLOCK`、`SE_BLOCK`、`BROKEN_SKYWALK`；
- 独立墙挂退役重盾；
- 独立东门／撤离口；
- 独立警戒设施的`active`与`damaged`状态；
- 独立A路高路损与B路低路损地面overlay。

结构必须是机战地图资产：体量存在感强、能承担战术空间，但不做写实高楼峡谷；顶面、立面、footprint和前缘明确，遮挡区域可整件半透明。不得出现人物、机体、车辆、小体、炮击、路线、ghost、UI、文字、编号或第二套视角。

六结构slot envelope逐字冻结为：`NW/NE/SE=HIGH 90px`、`NM/SW=MEDIUM 72px`、`BROKEN_SKYWALK=LOW 54px`。这是Camera V2的world-height上限，不得把任一结构画成更高的楼塔来获取“精品感”。

### 4.2 生成guide与参考数

实际ImageGen只允许引用：

1. ENV-A1新制的模块化几何／分区guide；
2. `CALL02_ENVIRONMENT_METHOD_DONOR_CROP_SHEET_1600x1200.png`。

Task111产品帧只用于本地几何校验，不直接作为ImageGen图像参考，避免把Proxy建筑、单位、文字和路线带入母板。

模块化guide必须是明确的slot sheet：各slot有纯色隔离带、统一40×24方向、无旧A4可见几何；至少将地面材质、六结构、盾、东门、设施双态和A/B路损分入互不接触的区域。若原始结果中任一必交slot无法隔离，整次调用判失败，不得从旧A4、Call02整屏或ENV-E0补像素。

generation log必须记录：完整prompt、精确引用路径／SHA、调用时间、原始结果路径、`environment_calls_used=1/1`、`Call03_used=0`、`Call04_used=0`。

## 5. 必交模块

唯一写域：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-env-a1-modular-tactical-environment-kit-master/**`

### 5.1 地面

- `GROUND_BAKE_CURRENT_V2_2400x1350.png`：只含道路、场地、排水、铺装、低矮边缘和克制的静态环境光影；
- 不得含任何六建筑、盾、东门、警戒设施、道路损伤结果、actor阴影或未来时态；
- 中央选择口袋`[15..20,9..11]`、BREAKER五格承力大道与东侧生命线必须保持清楚、低噪、无遮挡。

### 5.2 六个Structure

每个结构交同local canvas／pivot的两层RGBA：

- `<OBJECT_ID>_FOUNDATION_RGBA.png`：常显的低矮基础／占地边缘；
- `<OBJECT_ID>_OCCLUDER_RGBA.png`：整件可由focus-reveal控制器在1.00和0.34 alpha间切换的主体。

六个ID必须逐字为：`NW_BLOCK / NM_BLOCK / NE_BLOCK / SW_BLOCK / SE_BLOCK / BROKEN_SKYWALK`。每项同时交：native size、pivot、grid rect、front-edge footpoint、world-height class、alpha bbox、50%缩略图与SHA。

生图前须先交`module-slot-contract.json`。local crop尺寸可由内容派生，但同一Structure的foundation与occluder必须同canvas、同pivot；pivot必须把Task111派生的`structure_front_edge`准确映入local坐标。`front_edge / visual_bounds / reveal_cells`只能从Task111 Camera V2合同和注册表派生，禁止美术手填第二套空间真值。

foundation不得高到继续遮住被揭示单位；occluder透明后仍能看出建筑占地，但不能形成黑洞或整张地图“鬼城”。建筑自身不烘路线、状态灯、单位阴影或地面反射。

### 5.3 独立战术物件与结果

透明RGBA独立交付：

- `PROP_C01CDV1_RETIRED_SHIELD`；
- `TARGET_C01_EAST_EXIT`；
- `TARGET_C01_SECURITY_GATE_ACTIVE`；
- `TARGET_C01_SECURITY_GATE_DAMAGED`；
- `ROAD_DAMAGE_A_42_OVERLAY`；
- `ROAD_DAMAGE_B_24_OVERLAY`。

状态名与责任逐字冻结为：

- shield=`wall_hung_3_scorches`，第一轮始终墙挂／未取得；
- east exit=`active_first_round_open`，本任务不交第二轮`closed`状态；
- warning facility=`active / damaged`；
- A road=`long_broken_arc / damage=42`；
- B road=`twin_buckles / damage=24`。

两张ROAD overlay必须是`2400×1350`、与GroundBake相同origin的全画布透明层，不能靠运行时手移补注册。A/B道路结果只改变受损范围和裂痕强度，不改变passability或地形拓扑。所有状态对象都不得烘进GroundBake或Structure。

PLAN道路保持intact；CONTACT T3只允许独立`micro_crack`接触微裂表现。`long_broken_arc/42`与`twin_buckles/24`只能出现在专用world-result／后果toggle板，禁止提前合成进PLAN或CONTACT cleanplate。

`ALLY_C01_CITY_ARTILLERY`本轮仍由程序侧右缘T4 edge cue表达，`PROTECTION_ZONE_RECT`仍由程序overlay表达；ENV-A1不得新增炮体、炮线或荧光保护区像素。

### 5.4 确定性重组QA

必须用Camera V2 exact合同生成：

- actor-free `A_PLAN / B_PLAN / A_CONTACT / B_CONTACT` cleanplate；
- 同四帧的slot／footprint／route overlay QA版，Proxy只作校准且不得写入资产；
- `A_PLAN` 50%与100%环境审图；
- 六结构单独toggle、foundation／occluder toggle、shield／exit／facility／road A-B state toggle；
- 同一结构`OPAQUE 1.00 / REVEALED 0.34 / RESTORED 1.00`三态板。

禁止为构图好看而手移anchor、脚点、建筑grid rect或状态对象位置。

### 5.5 生产封包

必须同时交付：

- `source-lineage.tsv`：所有输入绝对路径、SHA、权限、允许／禁止用途；
- `module-slot-contract.json`与`asset-manifest.tsv`：resource ID、state owner、尺寸、alpha、pivot、origin、front edge、SHA；
- `generation-log.md`：唯一一次ImageGen调用、完整prompt、引用图、raw路径和预算读回；
- `machine-validation-report.json`：来源、尺寸、alpha、槽位、注册、污染、调用数；必须分开`mechanical_pass / visual_self_review_pass / overall_pass`；
- `50-100-visual-self-review.md`、`completion-report.md`、`delivery-hashes.sha256`；
- raw母板、拆分中间件、最终delivery与所有QA帧均须被manifest覆盖。

## 6. 制作人50%／100%门

### 50%

- 3秒读出：中央巨体承接大道、东侧撤离生命线、西侧盾钩子、六建筑围合而不堵玩法；
- 地面、建筑、盾、门、设施、道路结果是不同资源责任，不依靠文字标签才可分辨；
- 选择口袋和接触区无遮挡；
- 无明显切片拼贴、重复斜纹、程序挤出感、整屏生成漂移或旧A4拓扑回流。

### 100%

- 所有结构服从同一40×24地图视角，顶面／立面／footprint关系一致；
- 4—7大色块、最多两级硬阴影成立，避免高噪照片厚涂；
- 湿地反光克制且不伪造UI危险区；
- 透明边、alpha bbox、front-edge pivot、状态切换和四相机crop无错位；
- 结构0.34时后方单位／路线可读，foundation仍清楚表达阻挡；
- 东门、盾、设施和A/B道路结果在各自独立层中仅出现一次。

## 7. 停止门与完成态

出现任一项立即失败收口且不reroll：

- 输出是一张建筑与地面烘死的整屏场景；
- 六结构或战术物件无法干净分离；
- 相机不是40×24、出现透视汇聚或朝向漂移；
- 结构遮住选择口袋／接触口袋，或为了避让擅改玩法坐标；
- 出现角色、机体、车辆、小体、UI、伪字、旧A4对象、ENV-E0失败像素；
- 需要第二次环境调用、整屏reroll或挪用Call03／04才能成立。

允许自报：`ENV_A1_MODULAR_ENVIRONMENT_AND_OBJECT_KIT_CANDIDATE_FOR_P102 / ENVIRONMENT_IMAGEGEN_1_OF_1 / NO_REROLL / NOT_RUNTIME / FUN_NOT_PROVEN`。

完成后停在P102实际帧审查；不得自行开放Call03／04、CONTACT、Atlas扩展、Godot真实资产接入、UA91、G2-B、Default、Save、Runtime或Canon。
