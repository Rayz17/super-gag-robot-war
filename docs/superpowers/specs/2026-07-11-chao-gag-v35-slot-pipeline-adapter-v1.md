# 《超GAG机器人大战》V35.4 / V35.7 Pipeline / Episode Loop 槽位适配层 v1.1

日期：2026-07-11

> 2026-07-20状态：`legacy_contract_adapter / new_outline_migration_required`。本适配器继续负责复现V35.4/V35.7/V35.8的槽位、路线、机体生命周期和资产证据，但不再把旧十八章、82/95槽或V35.2当作当前剧情母稿。新逐章总纲必须先由六层融合前提形成，再建立旧槽到新章/话的显式迁移映射。

## 一、问题

在旧V35结构中，V35.2、V35.3和V35.4分别提供章级大纲、关键决策/72机规模、82作者槽/九组路线/机体生命周期/命运传播。这些表现在是可迁移的素材与制作证据；适配器仍需稳定回答：

- 当前单话来自哪个`slot_id`，一个作者槽是否被拆成多话。
- 本周目选了哪些槽、跳过哪些槽，未走内容如何继续存在。
- 某台机体此刻是否已经可控、位于哪支舰、能否跨舰部署。
- 班主任潮、纪存、七海、白鸢和馆长的旧状态是否必须进入本话。
- 本话没有新机入队时，旧机是否产生了足够大的生命周期变化。

因此增加V35槽位适配层。它不替代单话Pipeline，而是在Pressure Board之前解析结构输入，在Gate Result之后验证状态输出。旧V35.4运行继续可复现；声明使用`V357-*`槽号时，适配器自动切换到V35.7候选覆盖层。

## 一点五、版本选择

- `V354-*`：读取82作者槽、约67单周目槽和72机生命周期，用于复现V35.4设计。
- `V357-*`：读取95作者槽、约80单周目槽、72机迁移表与星火五车补表，用于V35.7候选施工。
- 同一Episode Loop运行不得混用`V354-*`与`V357-*`槽号。
- 两种旧模式都保留`Canon Mode: living_plus_v35_candidate`作为验证器兼容字段，但新故事运行还必须写`Outline Premise: V35_six_layer_upper_integration_20260720`和`Legacy Slot Migration ID`。没有迁移ID时只能复现旧设计，不能产出当前Reader。
- C01-C03继承V35.5的11个逐话Pressure Board、10槽11话映射和开局门禁，但这些只是上游施工输入，**不是已完成逐话梗概**。V35.7全剧运行必须从C01E01逐话生成Packet与账本，并通过V35.7槽表的`legacy_slot_id`把10槽映射为对应`V357-*`编号；不允许把Pressure Board直接标记为成稿，也不允许C01-C03用V354、C04以后用V357混跑。

## 二、执行顺序

```text
Current Outline Premise / Chapter Brief
-> Legacy Slot Migration Resolver
-> V35.4 / V35.7 Author Slot Resolver
-> Slot-to-Episode Mapping
-> Route / Skipped-State Resolver
-> Unit Availability & Fleet Resolver
-> Decision Propagation Resolver
-> V35.7 Mystery / Foreshadow / Continuity Resolver（仅V357）
-> V29 Eighteen-Chapter Crosswalk / High-Density Manifest（按槽需要）
-> Episode Input Manifest / Scene Binding
-> 单话Pipeline
-> V35 Contract Gate
-> 五张账本更新
-> 下一话Context Pack
```

### 1. Author Slot Resolver

从`v35_4_author_slot_route_architecture_v35_4.tsv`读取当前槽的标题、模式、玩法、机体、剧情翻面、状态变化和下一槽逻辑。Packet必须写`Author Slot ID`，不能只写章号和最终话号。

若`Author Slot ID`以`V357-`开头，则改读`v35_7_author_slot_architecture_v35_7.tsv`，并同时读取：

- `v35_7_chapter_capacity_audit_v35_7.tsv`
- `v35_7_playthrough_route_combinations_v35_7.tsv`
- `v35_7_unit_lifecycle_slot_remap_v35_7.tsv`
- `v35_7_starfire_playable_lifecycle_patch_v35_7.tsv`
- `v35_7_mystery_slot_binding_v35_7.tsv`
- `v35_7_continuity_thread_backflow_v35_7.tsv`
- `v35_7_foreshadow_slot_binding_v35_7.tsv`
- `v35_7_v29_eighteen_chapter_crosswalk_v35_7.tsv`
- 高密度槽额外读取`v35_7_high_density_slot_mecha_manifest_v35_7.tsv`

随后必须按同一`slot_id`绑定唯一的`v35_8_slot_mecha_ip_play_contract_v35_8.tsv`行，并继续读取：

- `v35_8_slot_unit_manifest_v35_8.tsv`
- `v35_8_slot_source_absorption_v35_8.tsv`
- `v35_8_slot_gameplay_contract_v35_8.tsv`
- `v35_8_slot_asset_manifest_v35_8.tsv`
- `v35_8_gate_lifecycle_reconciliation_v35_8.tsv`
- `v35_8_dynamic_unit_selectors_v35_8.tsv`
- `v35_8_unit_source_crosswalk_v35_8.tsv`
- `v35_8_package_source_crosswalk_v35_8.tsv`

Packet写入`V35.8 Loadout Contract ID`。新机门禁采用`effective_gate_mode`；动态机群必须先按路线、舰群、损伤、存活和隐藏条件解析。V35.8是可替换但必须说明理由的装载合同，不是把表中所有候选机械塞进正文。

V35.5开局层通过`legacy_slot_id`兼容：原V354槽与逐话Pressure Board是写作输入，最终Packet与五张运行账本写V357槽号。C03一个作者槽拆成两话的映射继续成立，第二话不得重复计算首登。没有Packet、Writer Room Review、Gate Result和账本提交时，不得称该话已经完成Pipeline。

旧模式Packet仍写`Canon Mode: living_plus_v35_candidate`以兼容验证器。当前故事Packet必须另写`Outline Premise: V35_six_layer_upper_integration_20260720`与`Legacy Slot Migration ID`：前者声明当前章级因果来自六层融合前提，后者说明本话具体打捞了哪些旧槽、机体、IP、分支或资产。两字段都不会把候选升格为Working Canon，也不允许旧槽位静默决定新剧情。

### 2. Slot-to-Episode Mapping

作者槽不是最终话号。一个槽可以映射一话，也可以因双地图、重要关系场或巨物高潮拆成两话；多个槽不得在未说明的情况下压成一话。映射写入`slot_episode_mapping.tsv`。

### 3. Route / Skipped-State Resolver

从路线组合表读取mandatory、互斥和任务池。每个Packet必须知道当前选中槽、跳过槽和汇流差异。跳过内容写入`skipped_slot_world_state.tsv`，转成敌方、独立援军、残响、后来者代收、路线缺口或后续补救。

### 4. Unit Availability & Fleet Resolver

V35.4从72机生命周期表读取首见、首控、正式加入、分支状态、C12后默认舰群和终局动作。V35.7改读72机槽位迁移表与星火五车补表，得到77台候选可操作收藏；星火巨神是组合形态，不重复计数。每话部署前先生成`Available Fleet`；C13以后无解释跨舰部署直接失败。

### 5. Decision Propagation Resolver

从50节点传播表选出本话输入状态和输出变化。没有相关线程时也要明确写`none`及理由，避免把未读取误装成“不适用”。

V35.7还必须把十谜、二十一条人物/阵营连续线程和三十五条伏笔绑定作为合法`thread_id`来源。Packet不能只声称“推进谜团”或“人物成长”，而要列出本槽读入的阶段、场面和提交状态。

### 6. IP / Loadout / High-Density Resolver（V35.7 + V35.8）

普通槽先用十八章V29交叉表选择参战包、名场面/台词锚和文化生态材料，再在Scene Binding中证明吸收。C05-C06、C11-C12、C16-C18的高密度槽必须读取具名manifest；“众机支援”“全路线机群”“百机齐射”只能描述镜头，不能替代具体单位、舰群、玩法动作和生命周期结算。

V35.8进一步要求每个槽至少解析两条具名机体/支援/敌机/场景巨构动作，并将所选来源落实为可读场面、玩家或机体动作、人物选择/敌方收益及状态提交。只抄`BFR/CAND/V351ABS`、作品名或名台词视为未吸收。

## 三、五张运行账本

### `slot_episode_mapping.tsv`

记录最终`episode_id`与当前V35合同版本`slot_id`之间的映射、槽内顺序、拆分数量和拆分理由。

### `route_state.tsv`

记录本周目选择槽、跳过槽、当前路线状态、汇流差异、失败尊严和下一次必读。

### `unit_availability.tsv`

记录每话机体的生命周期事件、战前/战后可用性、舰群归属、实际动作和来源行。

### `decision_propagation.tsv`

记录本话读取的命运线程、输入状态、绑定场面、输出变化与后续必读。

### `skipped_slot_world_state.tsv`

记录未走槽如何继续存在，不允许只写`not_selected`。

同一个跳过槽在做出分支选择时登记一次即可，后续Packet引用该状态，不重复抄整行；若状态后来发生变化，再新增一条事件行。

## 四、新机体门禁修正

旧严格门禁要求每话至少一台、默认两台首次出现IP映射机体。该规则对开篇补密度有效，但对V35.4后半程会迫使成熟机体失去生命周期。

V35正式运行改为三种模式：

1. `first_appearance`：本话有真实新机体首登，继续执行原门禁。
2. `lifecycle_delta`：本话无新机，但至少一台既有机体发生可见且不可替代的生命周期变化，例如新形态、新武器、新驾驶/机魂关系、新合体位置、新政治归属、跨舰转移、敌转友、路线锁或终局回收。
3. `bridge_exception`：纯过场/经营轻话，可无新机和生命周期升级，但必须给出原因与下一补偿窗口；不得连续两话使用。

返回机体只有在变化进入可读场面、玩法和`unit_availability.tsv`时，才能满足`lifecycle_delta`。普通复出、换色、数值提升和背景Cut-in不算。

## 五、Packet新增字段

- `Author Slot ID`
- `Slot Mode`
- `Slot-to-Episode Mapping`
- `Route Window`
- `Route State`
- `Selected Slots`
- `Skipped Slots`
- `Available Fleet`
- `Cross-Fleet Deployment Reason`
- `New Unit Gate Mode`
- `Roster Lifecycle Payload`
- `Incoming Decision Threads`
- `Outgoing Decision Deltas`
- `Skipped-Slot World State`
- `Mystery Binding IDs`（V35.7相关槽）
- `Continuity Thread IDs`（V35.7相关槽）
- `Foreshadow Binding IDs`（V35.7相关槽）
- `V29 Crosswalk Selection`（V35.7）
- `High-Density Manifest IDs`（V35.7高密度槽；其他槽写`not_required`与原因）
- `V35.8 Loadout Contract ID`（所有V35.7 Packet必填且必须与Author Slot ID唯一对应）

这些字段必须同时进入Scene Binding、Reader Synopsis或Production Split，不能只填表。

## 六、Episode Loop新增章末检查

1. 本章实际Packet是否映射到同一版本的合法槽，槽内拆分顺序是否完整。
2. 单周目选择数量、mandatory槽和selected/skipped全集是否符合对应版本路线组合。
3. 跳过槽是否有世界状态和后续窗口。
4. 首控、入队、离队、分舰和终局动作是否符合72机生命周期；V35.7还要合并星火五车并排除组合形态重复计数。
5. C12后三舰是否保持可用性差异。
6. 进入本章的命运传播节点是否在可读场面中生效。
7. 汇流是否只共享事件，不清空身份、政治、关系、设施和机体差异。
8. V35.7关键谜团、人物/阵营线程与伏笔是否在精确槽位提交；C13方舟T日志和C16共同开场/汇流是否必经。
9. 高密度槽是否列出具名机体与舰群裁剪，没有用集合词冒充规模。
10. V35.8合同ID是否匹配；有效门禁、具名动作、素材吸收、玩法反转与资产风险是否进入Pressure Board而非只留在表里。

## 七、验证器

`check_episode_loop_run.py`新增：

```bash
--require-v35-slot-contract
```

开启后要求Packet新增字段、五张账本和对应版本源表引用；验证器从`Author Slot ID`自动识别V35.4或V35.7，并验证slot/chapter、unit_id、thread_id、route_window、mandatory槽和舰群状态。V35正式厚梗概完成态必须同时启用：

```bash
--strict-creative-gates \
--require-source-absorption \
--require-v35-slot-contract
```

旧V31/V34运行不启用该开关时保持兼容，但不能声称已经按V35槽位施工图执行。V35.7验证通过只证明施工合同闭合，不等于95槽、77机或具体剧情已获用户批准。

## 八、V35.7首次正式运行顺序

1. 以V35.5的11个逐话Pressure Board生成C01-C03槽话输入，不把原文复制成成稿。
2. 初始化V357运行目录、五张V35账本及创作/source-absorption账本。
3. 从C01E01开始，一次只写一话；每话依次通过Context Pack、Episode Card、单话草稿、Writer Room Review、补丁合并和Gate Result。
4. C01、C02、C03各自完成后做章末连读；C03后追加C01-C03整体试玩、机器人大战成立性、人物关系、谜团和机体/IP密度审查。
5. 前三章通过后，才为C04制作正式Pressure Board并继续Episode Loop。
