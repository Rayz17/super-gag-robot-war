# C01E02｜A9.1-A6-S整屏Scene-First精品Lookdev唯一任务书

> 日期：2026-08-20  
> Owner：新“美术资产-2”任务 `01a018f7-b863-7973-9d4e-f11e9982024a`  
> 状态：`RESUMED_BY_84 / INTEGRATED_SCENE_TARGET_ONLY / NON_SEPARABLE_CANDIDATE / REAL_ART_HANDOFF_FORBIDDEN`  
> 上游唯一放行：84号R2C-C1制作人重新签收；80号其余exact值继续有效  
> 不构成：UA91、可拆资产完成、Atlas、Godot接入、Runtime、Canon修改、付费批量生成

## 1. 任务目的

先回答一个产品问题：在当前馆守Z V10X、BREAKER B＋X、A4斜俯相机和R2C exact交互几何不漂移的前提下，第一轮能否形成一张“像完整精品游戏”的规划画面和一张巨体接触画面。

本任务不再从孤立透明机体开始，也不重画设计。先做两个统一整屏世界，制作人实际看整屏、50%游戏尺度和100%身份裁切；只有通过后，才允许A9.1-A6-D从同一世界拆最小资产。

## 2. 必读输入与权威边界

1. `84-c01e02-r2c-c1-producer-reacceptance-and-parallel-resume-receipt.md`
2. `83-c01e02-r2c-c1-primary-swarm-ground-occupancy-correction-objective.md`
3. `80-c01e02-r2c-producer-exact-geometry-acceptance-and-parallel-visual-dispatch.md`
4. `78-c01e02-scene-first-visual-composition-and-joint-gold-frame-replan.md`
5. `76-c01e02-tactical-perspective-interaction-and-asset-interface-correction.md`
6. `c01e02-tactical-visual-interface-v1.json`
7. `c01e02-current-production-asset-lineage.tsv`
8. `main-g2-a1-r2c/04-actual-frame-manifest.json`
9. `main-g2-a1-r2c/05-a4-layer-registration-readback.json`
10. `main-g2-a1-r2c-c1/**`

必须重新使用`chao-gag-canon`，只查询与本任务有关的Hard／Working／Candidate／History。C01E02 Demo保持Candidate隔离；不得把Lookdev结果写入Canon或正式Runtime。

84号已解除生成前停门；现允许按第5节最多4次全屏ImageGen调用连续施工，但仍必须停在制作人内部视觉预审门。

## 3. 唯一身份、画法与世界责任源

### 3.1 馆守Z

- Hard身份校准：CML008。
- E02限域当前设计父图：`docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`。
- 当前Q/SD身份、比例、结构、配色参考：
  - `art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_imagegen_v2.png`
  - `art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png`
- C128只约束约4.2头身动作空间与bottom-center注册，不是可见像素母版。

这些参考属于`design_orthographic`；只能约束身份，禁止直接裁成地图south／north／east／west。

### 3.2 BREAKER

- B身体关系：`art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png`。
- X表面与三处闭合关系：`art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png`。
- 必须保持低头单红缝、前肢承重半直立、闭合胸缝、封闭上背、黑甲异质生体表面。
- 禁止回到龟／猿、雪橇、椭圆豆、飞行核心、薄翼、胸部发光裂口或驾驶舱读法。

当前没有合格的B＋X地图单帧母版；本任务是在整屏中建立north charge／contact视觉意图，不得宣称已经产生可拆母版。

### 3.3 纪存与画法

- 纪存：CML001与`frozen-assets/cml001-jicun-current-base.png`；只做路线／人员判断，不扮演驾驶员。
- 常态画法：CML128 Working `KINETIC_CEL`；参考`art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png`。
- 地图与世界：A4六层共同画布；A5 96px四向小体是地图相机的现成正确正例。
- 旧`GF_PLAN_1280x720_v2.png`与`GF_CONTACT_1280x720_v2.png`只借雨夜、湿地反光、整屏焦点和重量感，不借其馆守Z、BREAKER、地图几何、人物身份或UI像素。

### 3.4 必须写入source receipt的现成世界输入

| 用途 | 路径 | SHA-256 |
|---|---|---|
| A4 base | `art-a4-map-b-six-layer/A4_MAP_B_BASE_2400x1350.png` | `6fd40a256afee225457594558edf274823de5d1e771d1f570d0263c5df217789` |
| A4 buildings | `art-a4-map-b-six-layer/A4_MAP_B_BUILDINGS_2400x1350.png` | `db3f83eeb3ed5e583d0a831a203ab0d5446a594f9ed9e34f25f175f290f62237` |
| A4 roofs | `art-a4-map-b-six-layer/A4_MAP_B_ROOFS_2400x1350.png` | `7fea3c7918ff85bb1d5df1f4bcc5856afac1d8fa7f174d59b862f985962f11a9` |
| A4 foreground | `art-a4-map-b-six-layer/A4_MAP_B_FOREGROUND_2400x1350.png` | `454b3cf845ba91d7d7f13e201874bbbe79f871297a36930a24348823df1525a3` |
| A4 occlusion | `art-a4-map-b-six-layer/A4_MAP_B_OCCLUSION_MASK_2400x1350.png` | `b5f68f4749f6bff2025409622888d8e8faa17d977aca372caa43121eec18e899` |
| A4 mixed state reference | `art-a4-map-b-six-layer/A4_MAP_B_STATE_LAYERS_2400x1350.png` | `05833205230b087b3024545a1344174fb1a73c7975087fcf06808d62b01d3ff1` |
| A5 96px four-facing | `art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png` | `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b` |
| CML001 Jicun | `.superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_jicun_stand.png` | `3e624ba9b65a712855f71c72c3ce57238719ffb83718bf2e8a495c89384bca6c` |
| CML128 KINETIC_CEL | `art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png` | `8a546082e8fd2f1b0f9c6e8a8b1e602a647f478112887e93a8f44148e4867842` |

A4 state reference仍因盾／救援／损伤混包而没有exact handoff，只能参考，不得直接当最终状态层。

## 4. exact构图合同

### 4.1 共同相机

严格抄写80号：1280×720、40×20 dimetric、camera center `[-720,350]`、zoom `1.0`、地图viewport `[0,58,1280,584]`、A4画布`2400×1350`、canvas origin `[-1680,-350]`、crop `[480,428,1280,584]`。

单位、建筑、阴影、雨、碎屑和受力方向必须共享此相机。所有顶面、脚点和阴影都要读成从东南上方观看的斜俯世界；禁止眼平纸片、自由透视或为画面好看而移动单位。

### 4.2 `GF_PLAN_TARGET`

以A路T2前规划／预览为Hero：

- 当前实体馆守Z必须仍在`[15,11] east`；`[20,9] south`只画成半透明2×2终点ghost／预测姿态，不能把规划态画成T2已经到位。
- 当前实体BREAKER必须仍在`[20,13] north`；`[20,11]`只作为公开意图终点ghost／冲撞走廊出口。focus cell `[19,10]`。
- 其余可见世界真值必须同时落位：应急车`[17,10] east`；小体01`[22,7] west`、小体02`[26,12] north`、小体03`[29,5] south`；东侧撤离口`[31,7]`；东门警戒设施`[27,8] / active`；退役重盾`[14,10] / wall_hung_3_scorches`；东侧保护线rect`[20,5,12,7]`；城市炮源`[29,2]`。
- 公开意图轨迹必须来自同一投影：应急车`[17,10]→[18,10]→[21,10]→[24,9]`；小体01`[22,7]→[21,8]→[20,9]→[20,10]`；BREAKER按前述north走廊。不得为构图自由移动、隐藏或合并这些要素。
- 清楚读到下侧A路线、2×2终点ghost、south facing、BREAKER冲撞走廊、撤离线与保护对象。
- 顶部当前目标必须逐字为`让应急车通过，挡开扑向东门的小体，并站到冲线前。`；三条最高威胁依次为`应急车先穿过落脚区`、`小体将在第二时点扑向东门`、`BREAKER沿直线冲入街区`。
- 底部只保留`应急车 / 小体 / 巨体接触 / 城市炮 / 赤红蓄能`五时点，顺序不可变。
- 纪存大型通讯构图最多占屏宽25%，不得挡路线、终点、冲撞走廊或接触预测区；台词与UI文字由确定性排版添加，禁止生成伪字。
- 纪存当前Reader句逐字为`人都在后面。把它引到南边去。`；不允许美术自行改写台词。
- A为当前已选方案，摘要逐字为`卡位迎撞｜正面承接｜较低热量｜第二轮余量1`；B为可切换备选，摘要逐字为`护线预备｜先east护线、接触前转south｜高热｜第二轮余量0`。
- 地图viewport内部无遮挡可读面积至少75%，中央60%保持战术安全区；不得把ghost误画成第二台馆守Z或第二只BREAKER。

### 4.3 `GF_CONTACT_TARGET`

以A路T3.00全前缘接触为Hero：

- 画面严格冻结在T3.00接触瞬间：实体馆守Z`[20,9] south`、实体BREAKER`[20,11] north`；impact socket `[20.5,10.5]`，contact normal `[0,1]`，受力／反冲方向服从80号。
- T1应急车实体已到`[24,9]`并离开落脚区；T2小体01必须仍存活、落在83号纠偏后的唯一合法地面格`[22,9]`，不得回到与馆守Z重叠的`[21,9]`，也不得改成仅显示offset。小体02／03显示于A路resolved位置`[27,12] / [29,5]`。退役重盾仍挂在`[14,10]`。
- `[20,8.5]`视觉recoil与`[21,11]`post-BREAKER只能出现在证据overlay的预测ghost中，不能把contact与post-contact两个时态混成一张实体画面。
- 双方脚点、身体受力和装甲压缩必须围绕同一socket；不得隔空、穿插或靠特效遮住姿势错误。
- 纪存大通讯必须退场；只允许窄小状态残留。地图viewport内部无遮挡可读面积至少88%（不是全屏面积；地图viewport本身只占全屏约81.1%）。
- T3.00实体表现只允许接触高光、局部微裂、定向小碎屑／水花、馆守Z承重姿势和BREAKER冲势被偏；完整路面翻起、T4城市炮实体射击与T5赤红蓄能实体效果均不得提前发生。
- 城市炮与red charge只能作为下一时点HUD预示，不能抢走首次巨体接触主焦点；预示射线不得画成已经命中的实体炮束。
- 若画出城市炮预示或射线，其起点必须取`[29,2]`，A路侧甲终点取`[24,12.5]`；不得自由改成更好看的屏幕方向。
- 屋顶与前景层必须保留并体现局部遮挡读法；不得删除遮挡层、把整层统一降到50%或用强闪光掩盖穿插。

### 4.4 视觉尺度

- 馆守Z按2×2、BREAKER按3×3。256×256／384×384只是76号Candidate校准画布，不是冻结的最终视觉尺寸；本任务必须在exact相机上以footprint、屏占比和50%读法重新量尺，并把建议frame canvas写入readback，不能自行晋升为handoff尺寸。
- 两者统一使用footprint bottom-center；阴影接触同一地面。
- 50%游戏尺度仍须一眼分清馆守Z头冠／胸门／肩环与BREAKER低头红缝／前肢／封闭背甲。
- BREAKER必须明显比馆守Z更重、更宽、更低，但不能成为无结构的黑色大团。

## 5. 允许的制作方法

- 必须完整使用`imagegen` skill处理整屏位图生成／编辑；参考图只约束各自职责，不得交叉借身份。
- 允许最多4次全屏ImageGen生成／编辑调用用于两张目标及定向纠偏；超过4次或需要外部付费批量时立即停门报制作人。
- 可用确定性图像脚本做裁切、缩放、UI文字、标注、对照板和颜色检查；禁止用Pillow／SVG／Blender／Python原语绘制可见机体或建筑成品。
- UI、中文文字、路线几何、接触socket和裁切板必须由确定性合成完成，不能相信生成图中的伪UI。
- Lookdev允许整屏不可拆；但必须诚实标注`non_separable_candidate`，不得伪造alpha、atlas、pivot或Runtime handoff。

## 6. 唯一写域

- `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-scene-target-lookdev/**`

不得修改A4、A5、V10X、B／X、CML001、CML128、旧A9、Godot、生产资产谱系、Canon、Reader或其他任务目录。不得git add／commit／clean。

## 7. 必交产物

1. `GF_PLAN_TARGET_1280x720.png`
2. `GF_CONTACT_TARGET_1280x720.png`
3. `GF_PLAN_TARGET_CLEANPLATE.png`与`GF_CONTACT_TARGET_CLEANPLATE.png`：必须无UI、无伪字、无debug overlay；如果生成源有烘入伪UI，必须判失败，不得以“生成器只交整图”豁免。
4. `GF_TARGET_50_100_IDENTITY_REVIEW_1920x1080.png`：馆守Z／BREAKER在50%与100%下的身份裁切。
5. `GF_TARGET_GEOMETRY_OVERLAY_1920x1080.png`：显示网格anchor、footprint、footpoint、route、contact edge、socket、normal、focus和safe zone；overlay不得混入最终目标图。
6. `exact-state-and-overlay-readback.json`：机器可读记录PLAN current／ghost、全部可见演员／对象／保护区／公开意图轨迹、CONTACT实体／post ghost、Swarm01合法`[22,9]`地面互斥、T1–T5实体／预示边界、确定性UI文案、相机、focus、safe zone、单位frame canvas建议与所有socket；不得只存在图片标注。
7. `source-receipt.tsv`：绝对路径、SHA、authority、实际用途、禁止用途。
8. `generation-log.md`：每次ImageGen调用的参考图、提示词目的、结果、取舍与是否使用。
9. `visual-self-review.md`：逐项审查身份、比例、相机、共同光向、地图完成度、UI第一读法、接触重量、伪字、手脚／甲片异常。
10. `completion-report.md`：逐项`PASS / FAIL / BLOCKED`；不能只有总PASS。
11. `delivery-hashes.sha256`。

## 8. 制作人视觉门

机器检查后必须停下等待制作人实际看图。以下任一失败即返修，不进入A9.1-A6-D：

- 馆守Z不像当前V10X，或退回旧Q版／程序图形；
- BREAKER不是B＋X，或读成龟猿／雪橇／黑豆；
- 两机不是同一斜俯相机、同一地面、同一光向；
- 50%尺度身份消失、比例像模型玩具或接触姿势站不住；
- 规划画面先读装饰而非目标／路线／威胁／时间线；
- 小体01仍在`[21,9]`与馆守Z重叠，或任一车辆／小体／门／设施／重盾／保护区偏离exact坐标；
- 接触画面需要靠大闪光掩盖隔空、穿插或错误受力；
- T3接触帧提前实体发生T4炮击、T5赤红蓄能或完整道路翻起；
- 屋顶／前景被删除、整层50%透明，或没有可验证的局部遮挡读法；
- 地图只是灰盒、平铺概念图或一张无法继续拆分的自由构图；
- 纪存遮住玩法，或CONTACT阶段仍占大屏；
- 任何输出声称UA91、Runtime、Atlas、可拆资产或real art handoff完成。

完成后状态只能是：`CANDIDATE_SCENE_TARGETS_READY_FOR_PRODUCER_INTERNAL_REVIEW`。
