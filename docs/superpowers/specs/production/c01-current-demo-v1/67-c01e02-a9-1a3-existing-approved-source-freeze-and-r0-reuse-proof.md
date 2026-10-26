# C01E02 A9.1-A3｜既有获批来源冻结与 R0 零重设计复用证明

> 日期：2026-08-19  
> 状态：`producer source freeze signed / Candidate only / no Runtime`  
> 上游：66号已有批准母版优先纠偏  
> 裁决：馆守 Z 与 BREAKER 的设计选择已经完成；本阶段只做已有稿的忠实 Sprite 转译，不再重开机设。

## 1. 制作人结论

```text
design_selection = closed
approved_source_reuse = mandatory
new_identity_generation = forbidden
runtime_sprite_adaptation = open_after_R0_preflight
```

“未成为最终 Sprite Master”只说明尚缺方向、状态、目标像素清稿和 Atlas，不表示旧设计无效，也不授权重新设计。

来源优先级固定为：

```text
用户／Canon批准责任源 > Candidate绘画工作层 > History动作与pivot证据
```

低层来源只能补充高层未表达的像素或动作信息；冲突时必须丢弃低层内容，不得反向改写批准轮廓。

## 2. 馆守 Z exact source freeze

| 角色 | 固定文件 | SHA-256 | 允许用途 | 明确禁止 |
| --- | --- | --- | --- | --- |
| Hard身份责任源 | `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png` | `a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521` | CML008身份、头冠、脸、胸、肩环、圆柱前臂、旧超级系重量 | 直接当地图比例；被Candidate稿覆盖 |
| E02限域细节责任源 | `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png` | `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade` | C01E02双臂裸机、无翼／无背包的局部结构 | Canon／Runtime晋级；改变CML008身份 |
| 地图Q比例与动作轮廓责任源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png` | `d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e` | 用户“C可以”；约4.2头身、腿部与关节动作空间、2×2读法、bottom-center pivot | 再做A/B/C选择；改变头身、肩宽、胸甲大形、四肢比例 |
| Q方向父板 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png` | `4d8e7975649b2b85458a838afd9bc2fe8e3a90fd8cbcfe8a7929b8ae9ae6c225` | 解释C案为何被选及其不可丢失识别点 | 把A/B重新作为候选 |
| 四向主绘画工作层 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a2-master-production-correction/delivery/GUARDIAN_Z_V10X_KINETIC_FOURVIEW_RGBA_2560x960.png` | `cc75ed94a1676488d6b1f777775192893c8037b23e08a06f802b714bbfca5243` | 回收四向局部绘画、配色、线压；逐方向裁切／清脏／局部paint-over | 继承其高身比；整体缩小冒充Q Sprite；覆盖C案轮廓 |
| 四向补充工作层 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png` | `3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9` | 仅补侧背方向局部细节和透明清稿工作量 | 继承未闭合turnaround结构；独立成为母版 |
| History动作证据 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b1-1/assets/atlases/R05_GUARDIAN_Z_SOUTH_ACTION_B1_1_1280x256.png` | `720f23edc1e069b1cd9780f973fb9df84d423466800d796dcfb8ff8180e1ad59` | `idle/step_a/step_b/brace/recoil`节奏、脚点、pivot和动作幅度 | 复用可见程序图形像素；视觉晋级 |

### 馆守 Z 合成规则

以 `C128` 的Q比例／大轮廓为不可变身体模板，以 `CML008 + V10X` 校正身份，以A9.1-A2／A9.1-A只回收能装回该身体模板的局部绘画；A8只提供动作和注册数据。

## 3. BREAKER exact source freeze

| 角色 | 固定文件 | SHA-256 | 允许用途 | 明确禁止 |
| --- | --- | --- | --- | --- |
| B外轮廓／拓扑责任源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png` | `7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868` | 用户“B可以”；前肢承重半直立、短后稳定结构、3×3、近30m、north读法 | 再提A/C；改成龟、猿、雪橇、车辆或普通四足 |
| 地图B轮廓／pivot责任源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png` | `e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4` | 用户批准B的128px外轮廓、重心与bottom-center pivot | 改肢体数量／类型；独立声称已完成B＋X |
| X表面与三点关系责任源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png` | `cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85` | 用户选择X；异质／生体装甲；红缝—闭合胸缝—封闭上背出口关系 | 把X当另一具身体；打开核心；改变三点关系 |
| 高分局部绘画工作层 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/BREAKER_BX_GROUND_SHELL_MASTER_RGBA_1400.png` | `cbeb1ecb18e9d1ed41dd96d939c56e1f00f0eeab3f1af6bd4ddca048e8e02113` | 仅回收壳片、暗色材质、红缝和前肢局部绘画 | 继承龟壳／猿类整体外轮廓；整体缩小成为母版 |
| KINETIC_CEL画法工作层 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a2-master-production-correction/delivery/BREAKER_BX_NONANIMAL_KINETIC_MASTER_RGBA_1400.png` | `b47ebc4a6b8538f23892229f5554ae6c33b066ac37cf7077a71399e6931fb89d` | 仅回收硬色块、描边、低亮度配色和两级阴影画法 | 继承雪橇／装甲车身体；覆盖B轮廓 |
| History动作证据 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b1-1/assets/atlases/R05_BREAKER_NORTH_ACTION_B1_1_960x320.png` | `3d4b3f2e4cd07238a87fdf17b8d5756446709dccdd37dc5dc23905e52ad4f9f7` | `idle/charge/contact`节奏、前冲、接触、pivot | 复用可见程序图形像素；视觉晋级 |

### BREAKER 合成规则

以 `B身份板 + B128` 锁外轮廓、承重拓扑和重心，把 `X关系板` 的表面语言覆盖到同一身体；A9.1-A只捐局部绘画，A9.1-A2只捐画法，A8只捐动作／pivot。任何步骤都不得再生成一具新的BREAKER身体。

## 4. 立即派工：R0 existing-source reuse proof

### 4.1 目的

先用零重画证据证明后续确实从既有批准稿出发，并在真实地图尺度上确认两者第一读法。R0不是美术母版验收，不重复请用户选择设计。

### 4.2 唯一写入范围

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-existing-source-reuse-r0/**`

### 4.3 必交物

1. `source-freeze-receipt.tsv`：逐行登记本单全部来源路径、SHA、authority role、allowed use、forbidden use；
2. `GUARDIAN_Z_C128_APPROVED_EXACT.png`：批准C128的字节等同授权副本，SHA必须仍为`d72c...14e`；
3. `BREAKER_B128_APPROVED_EXACT.png`：批准B128的字节等同授权副本，SHA必须仍为`e800...ac4`；
4. `R0_EXISTING_APPROVED_SOURCES_ON_A4_MAP_1280x720.png`：只把两张exact 128样张按其bottom-center pivot合成到A4地图视口，保持原生1:1像素，不拉伸、不补画；明确标注“source scale proof / not event staging / not final art”；
5. `R0_SOURCE_ROLE_BOARD_1920x1080.png`：机械排版显示批准责任源、Candidate工作层和History动作证据；标签必须写清“锁什么／不能改什么”；
6. `delivery-hashes.sha256`与`completion-report.md`：说明零ImageGen、零Blender、零新造型、零可见像素重绘、零Runtime。

允许用脚本做字节复制、裁切、缩略图、文字标签和alpha合成；不得用脚本绘制、补齐或重构机体可见像素。

### 4.4 R0通过门

- exact副本哈希相同；
- 馆守 Z 一眼仍是用户选定C，BREAKER一眼仍是用户选定B；
- BREAKER在1:1地图读法上明显大于馆守 Z，且2×2／3×3重心相容；
- 无任何新造型、ImageGen、Blender或程序几何冒充美术；
- 制作人直接查看实际PNG后签视觉预审，validator不能代替。

若原生128样张不足以表达近30m／18m比例，只记录为下一轮目标显示尺寸待校准；R0不得通过拉伸或重画来“修正”。

## 5. R0之后才可开的单帧忠实转译 Pilot

R0经制作人视觉预审后，另派两张单帧而非四向全套：

- 馆守 Z：`south idle`，C轮廓mask不变，补CML008／V10X身份细节和KINETIC_CEL清稿；
- BREAKER：`north charge-ready`，B轮廓／拓扑mask不变，烘入X表面关系和KINETIC_CEL清稿。

只验收身份、比例、地图第一读法和画面完成度。单帧过后才扩方向与动作；不得再以逐帧独立生成方式重抽身体。

## 6. 冻结边界

- UA91仍等待单帧与四向关键帧完成后的制作人视觉预审；不要求用户重选C或B＋X；
- A9.1-B、Atlas、Godot、exact handoff、G2-B、LibTV继续冻结；
- 本单不修改Canon，不将Candidate方向批准提升为Runtime；
- 65号中的Sprite-first、稀疏Clip和Godot／LibTV分工保留；65号中“新生成身份源图”继续由66／67覆盖。
