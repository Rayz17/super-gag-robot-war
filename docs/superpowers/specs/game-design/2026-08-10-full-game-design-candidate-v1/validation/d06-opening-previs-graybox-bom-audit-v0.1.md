# D06｜C01–C03 Previs／灰盒／正式资产 BOM 审计 v0.1

> Status: `candidate_audit_complete / zero_stage_closed / budget_provisional / no_production_authorization`
>
> Authority boundary: 只审计 Candidate 设计与当前工作区证据；不修改 Canon、Reader、Runtime、C01E02 Demo 或正式资产身份。

阶段机器账见 [opening-previs-graybox-bom.tsv](../data/opening-previs-graybox-bom.tsv)，六类字段与门实例要求见 [opening-previs-artifact-class-contract.tsv](../data/opening-previs-artifact-class-contract.tsv)，28项设计主体边见 [opening-design-subject-coverage.tsv](../data/opening-design-subject-coverage.tsv)，来源全集见 [c01-c03-previs-needs.tsv](../chapters/c01-c03-previs-needs.tsv)。阶段账按 **20 个 `source_previs_id` × 6 种 `artifact_class` = 120 行** 建立全覆盖，任一来源都必须同时出现：

1. `logic_diagram`：比例、拓扑、流线、状态、身体或控制链的可核验逻辑文件；
2. `visual_direction`：真实低保真图与范围化视觉方向回执；
3. `continuous_previs`：Accepted Story 之后，操作、演出、失败与结算连续成立的捕获；
4. `playable_graybox`：绑定 ruleset/map/build 的可玩灰盒与真人 gameplay 回执；
5. `asset_previs_candidate_bom`：资产 Previs、Candidate asset manifest、BOM、预算和排除项；它连同 visual 与独立 production authorization 回执是 `GATE-ASSET-AUTH` 的输入；
6. `formal_asset`：只在 `GATE-ASSET-AUTH` 通过后制作，再由最终 manifest、成品 hash、QA 与独立 production handoff 回执进入 `GATE-ASSET-HANDOFF`。

`required_output` 是要交的内容，不是已有证据；`OPEN` 表示没有属于该类别的真实文件与 SHA-256。文字 Reader、Markdown 镜头表、蓝图和“可以画”声明都只作为依赖，不填进 Previs 收据。当前工作区外部证据的 hash 只是本次快照，不等于可达 Git/归档恢复点。

## 1. 机器覆盖结论

- 120 行中，`111` 行为 `OPEN`，`9` 行只有范围受限的 Candidate 证据；
- 20 个来源均恰有 6 行，六类各 20 行；没有漏掉或重复来源；
- `17/20` 个来源六类全部 OPEN；
- `3/20` 个来源有局部证据：`PV_C01_WANJI_MASTER`、`PV_C01_GROUND_MAP`、`PV_C01_MECHA_ACTIONS`；
- **0/20** 完成六类闭包，**0/20** 可以据此进入正式资产授权、handoff 或正式 Runtime。
- W6 `formal_asset` **20/20全部OPEN**；Candidate Demo manifest、方向板和方向回执只登记在W5 `asset_previs_candidate_bom` 的related Candidate证据中，绝不计为成品partial。

### 28项设计主体覆盖

20个Previs包不是主体清单，因此另以28行把 [opening-gd2-dependency-closure.tsv](../data/opening-gd2-dependency-closure.tsv) 的每个 `closure_id / backfill_id / design_subject_id / current_canon_anchor_or_none` 连接到一组W1逻辑行、W5 Candidate BOM行和W6 formal行。其中15行保存能在 Current Canon `entities.tsv` 解析的单一实体锚点，13行因属于复合包、地点状态或接口设计而显式写 `NONE_NO_SINGLE_CURRENT_CANON_ENTITY`；后者不是缺列，也不把 Candidate ID 提升成 Canon。每条边同时声明：

- `manifest_subject_refs`：最终manifest必须保留的实体/地点/家族包身份；
- `edge_kind` 与 `new_or_reuse_boundary`：新建设计包、复用现有主体、共享系统接口或家族聚合，禁止把复用变成主体合并；
- `asset_budget_ids`：必须落入所连接W5行的预算类别；
- `unresolved_manifest_questions`：未解决时继续阻断授权。

其中BF0011无牌一号、BF0012旧拳王、BF0013完全版王者和BF0028 C02 lineup都已连接到C02训练/决赛/救援的W1/W5/W6边；无牌一号与旧拳王保留各自Chassis/动作身份，lineup只定义Rig复用，不能合并主体。BF0017/18/19与BF0033/34/35/36同样分别连接社勇王、衡令、城梁和C03家族包。当前红/蓝/黄地方飞行队仍缺稳定entity ID，已作为BF0028的授权阻断问题记录，而不是临时发明ID。

### 已有但不能升级的三组证据

| 来源 | 当前真正存在 | 仍未证明 |
| --- | --- | --- |
| `PV_C01_WANJI_MASTER` | 两张带 hash 的逻辑 SVG | 万机馆外观三视、整馆正式剖面、楼层/外泊视觉方向、可走灰盒、连续 Previs、用户视觉回执 |
| `PV_C01_GROUND_MAP` | C01E02 MAP-B Candidate 方向回执、A4 六层 Demo 派生包、局部 Runner 捕获；M2.4 内部门通过并等待联合试玩；A4 manifest只作为W5输入候选 | E02→E03 同图继承、两种策略真人成立、章级连续 Previs、独立production authorization、正式资产handoff、正式 Runtime |
| `PV_C01_MECHA_ACTIONS` | E02 的馆守Z/BREAKER/重盾方向板、局部盾拍灰盒与 36 秒 Candidate Animatic；方向manifest只作为W5输入候选 | 勇拳、E03破壳、E04飞行核心/托肩、整组身体规则、跨三话联合 Previs、独立production authorization、正式 Chassis/Rig/动作handoff |

C01E02 的活动 Candidate lane 可以在默认入口加载五个 A4 地图槽，不改变静态 manifest 仍为 `approved_handoffs=[]`、不改变正式 Runtime 未授权的事实。该证据只登记在 C01E02 局部行，不能向 C01 全章、C02/C03 或正式资产横向外推。

## 2. 优先级与数量口径

`priority_wave` 先按消费顺序排：

- `P0A_VERTICAL_SLICE`：C01 五包，先关闭万机馆、E01路线、E02-E03连续图、联合机体动作、E04沿海母舰战；
- `P0B_SECOND_CHAPTER`：C02 七包，重点先做木桶街总图、货运环多态、E04决赛/事故、E05救援与双转子工程链；
- `P0C_THIRD_CHAPTER`：C03 七包，重点先做工务城总图、坞桥换位、移动/中央环、社勇王和C-1归港；
- `P1_SHARED_UI_REUSE`：C03双信的专属视觉/连续段/正式资产延后，当前只先完成信息逻辑，并复用共享 UI Shell。

`stage_order` 遵守 [D09生产门](../09-production-pipeline-and-gates.md)：`W1逻辑闭包 → W2 GD2方向 → W3 story验收后连续Previs → passed scoped GATE-PREVIS实例 → W4章节适配灰盒/真人测试 → passed scoped GATE-PROTOTYPE实例 → W5资产Previs与Candidate BOM → passed scoped GATE-ASSET-AUTH实例 → W6正式资产制作与handoff`。逐来源依赖强制为：W2读取同源W1；W3读取同源W1/W2与passed scoped `GATE-GAMEFLOW`实例；W4只以同源W3与passed scoped `GATE-PREVIS`实例作为阶段前置；W5读取同源W2/W3/W4与passed scoped `GATE-PROTOTYPE`实例；W6读取同源W5与passed scoped `GATE-ASSET-AUTH`实例。`dependency_ids`和`required_gate`里的 `GATE-*` 只表示门类型与依赖位置，不是已经通过的实例；每行目标门也不得同时出现在自己的 `dependency_ids`。中性 D04/D05 规则纸模可独立验证系统，但不计入正式章节W4依赖或收据，不能替代同源W3，也不能让章节适配抢跑。

数量只用不含人日的组合桶：

- `Q0`：当前不建专属包；
- `Q1`：单一包/序列/地图；
- `Q2`：2–4 个关联件；
- `Q3`：5–8 个关联件；
- `Q1_CANDIDATE_BOM_PACKAGE`：一份W5资产Previs与Candidate BOM包，不代表已授权资产数量；
- `QFROM_AUTHORIZED_MANIFEST`：W6成品数量只能继承已通过 `GATE-ASSET-AUTH` 的精确manifest；
- `QSHARED_REUSE_ONLY`：只建共享系统内容实例。

复杂度 `A0–A3` 原样继承源表；它不是人日、报价或已批准预算。资产类只绑定 [D11现有预算类别](../11-scope-budget-production-plan.md)，所有行的 `budget_confidence` 均保持 `provisional_uncalibrated`。

## 3. 四个阻断字段的精确定义

四个字段不是自由备注，而是逐 `artifact_class` 的固定矩阵；机器表与中央checker都必须逐行等于下表：

| `artifact_class` | `blocks_chapter_paper` | `blocks_playable_build` | `blocks_asset_authorization` | `blocks_asset_handoff_runtime` |
| --- | --- | --- | --- | --- |
| `logic_diagram` / W1 | `yes` | `yes` | `yes` | `yes` |
| `visual_direction` / W2 | `no` | `yes` | `yes` | `yes` |
| `continuous_previs` / W3 | `no` | `yes` | `yes` | `yes` |
| `playable_graybox` / W4 | `no` | `yes` | `yes` | `yes` |
| `asset_previs_candidate_bom` / W5 | `no` | `no` | `yes` | `yes` |
| `formal_asset` / W6 | `no` | `no` | `no` | `yes` |

- `blocks_chapter_paper=yes` 只属于W1：缺它时仍可写假设纸模，但不能把具体章节地图/空间/身体纸模记为依赖闭包。当前20个logic行都未关闭，其中19个OPEN、1个仅部分逻辑图。
- `blocks_playable_build=yes` 固定属于W1–W4：Build必须同时继承逻辑、视觉、连续Previs和章节适配灰盒；W5 Candidate BOM与W6成品位于可玩Build门之后，所以固定为`no`，不能反向制造循环。中性纸模PASS与C01E02局部Runner都不能解除同源W1–W4阻断。
- `blocks_asset_authorization=yes` 固定属于W1–W5；W6 `formal_asset` 必须为`no`，因为成品资产不能反过来成为自身开工授权的前置。
- `blocks_asset_handoff_runtime=yes` 六类全部为`yes`；其中W6只阻断 `GATE-ASSET-HANDOFF` 与下游，不阻断已经发生在上游的资产授权。

### 3.1 Gate定义不等于Gate实例

六类合同把120个BOM项派生为 **140个** `bom_item_id@GATE-*` 实例要求：W1每项需要`GATE-GD2`和`GATE-GD3`两个scope实例，共40个；其余W2–W6每项各需要一个，共100个。每个要求都必须按 [game-design-gate-instance-schema.tsv](../data/game-design-gate-instance-schema.tsv) 绑定：

- 独立 `gate_instance_id` 与所引用的 `gate_definition_id`；
- 精确 `scope_type / scope_instance`，并把该 `bom_item_id / source_previs_id` 纳入输入；
- `source_versions / checker_versions` 与实际输入path的SHA-256集合；
- 相容的gate receipt template、独立 `receipt_set_instance_id`、真实回执path/hash；
- 实例自己的`status=passed`，而不是在 `required_gate`、`dependency_ids` 或证据状态里写“GATE-X passed”。

尚未生成精确方向包、跨话operation Previs模板、build ID、Candidate asset manifest或final asset manifest的scope，合同明确写 `OPEN_*_required`，不捏造占位实例。目前 `current_instance_registry=OPEN:no_opening_gate_instance_registry`、`current_instance_status=OPEN:no_scoped_instance_bound`，即 **140/140要求均未绑定实例，0个passed**。中央checker因此fail-closed：在真实实例Registry与完整schema绑定接入前，任何把通用Gate ID直接改成passed的做法都会失败。

因此无需等待制作人完成 C01E02 Demo 才继续 W1/W2：万机馆、C01其余地图、C02与C03的逻辑闭包和设计方向可以并行推进。Demo 只有在带精确 build/ruleset/map、录像、输入日志、复述与 gameplay 回执后，才回填对应 `playable_graybox` 行；它不会自动补齐其他五类收据。

## 4. 下一批可签发的最小工作包

1. `P0A-W1`：把万机馆两张逻辑 SVG 扩成整馆邻接、三尺度、七流线与三态闭包，并补 C01E01、E02-E03、E04 三张逻辑地图和联合动作控制图；
2. `P0A-W2`：逐包给用户看真实低保真外形/剖面/俯视/前后态，回执只批准指定路径与 hash；
3. Accepted Story 不变的前提下，先完成 C01 同源连续 Previs 并通过 scoped `GATE-PREVIS`，再启动对应章节适配灰盒；将 C01E02 联合试玩证据作为一个局部附加输入，而不是W3替代物；
4. C01 局部闭包过程中并行启动 `P0B-W1` 木桶街/货运环/双转子链，避免下一章再次依靠 gameflow 临场发明；
5. W5只交资产Previs、Candidate manifest/BOM、预算、排除项和两类授权回执；`GATE-ASSET-AUTH` 通过后才建立W6成品，W6数量严格继承已授权manifest，并另取production handoff回执。

本审计没有给出人日或成本结论，也没有把 Markdown、SVG 逻辑图、Demo 方向批准或活动 Runtime 加载提升为正式视觉、正式资产或正式游戏系统。
