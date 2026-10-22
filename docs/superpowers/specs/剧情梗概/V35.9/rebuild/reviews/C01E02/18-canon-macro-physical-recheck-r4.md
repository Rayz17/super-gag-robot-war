# C01E02 Canon / Macro / Physical 定向复审 r4

> 席位：原 Canon / 宏观谜团 / 物理连续性独立审稿席  
> 证据基线：2026-07-15 当前磁盘  
> 裁决：`PATCH`

## 1. 裁决摘要

15号回执要求的**故事与物理主体修复已经闭合**：C01地图四令分域正确；CH036正式/首战为`V355-C01E03`，CH037只在E03作远程/终端预告；旧`C01E03-01..08`均已降为historical；当前E04不再重复列馆守Zalias；E02唯一快照完整喂给S03、S04与state propagation。29人楼外、馆内3核心+F2、供水/风道/档案/消防机腿伤、勇拳零动作、馆守Z被动、白函E02远程/E03具身、完整移动脊柱未暴露及人员不入载荷均无回归。

本席仍不能给`PASS`，原因仅在**当前默认检索与图谱关系层**：精确查询`entity R07`仍返回核心包的旧`C01E03-04` formal/battle；馆守Zalias查询还会因一个子机制沿用废弃父ID而多返回一行；当前`N_GUANSHOU_Z`图节点反查只得到旧“新1-2正式战”边；旧标准化三话节点虽已标historical，仍有11条关联边使用非historical关系。`canon_query.py:40-42,245-263`执行全字段子串匹配且不做current/historical排序，因此这些不是不可见的库内注释，而是默认查询可直接命中的答案。

结论为索引级`PATCH`。E02 Episode、Runtime、Graybox、迁移单、S03/S04及state propagation不需要返工。

## 2. 已闭合项

### 2.1 权限与四令：PASS

- `C01-逐章重构地图-v1.md:68-71`现已明确：安全端锁半开门、代哥端切胸灯、平台冻钥匙、军方停B1泵；七海只下达并撤销本人东侧高压命令，门、钥匙与军方泵锁仍由现场工序处理。
- `entities.tsv:34`、`runtime_rules.tsv:5`及`canonical_terms.tsv:244`同值保存七海写权限关闭与城市消防支援继续两个独立状态。

### 2.2 first/formal、旧场景与E04 alias：PASS

- `entities.tsv:32`：CH036的`first_formal_appearance`与`first_battle_join`均为`V355-C01E03`，并明确E01/E02不得到场或支援。
- `entities.tsv:33`：CH037仅在`V355-C01E03`预告，formal/battle仍为`C08-01`；不会独立入队。
- `runtime_rules.tsv:2`、`gag_hooks.tsv:2,4`、`character_mecha_art_locks.tsv:9-10`已同步豪司E03首行动、金章预告、馆守ZE02零动作与`V353U001`制作ID。
- `scenes.tsv:22-29`八行全部为`historical_runtime_reference`且只解锁`HISTORICAL_RUNTIME_ONLY`；当前链为`:99-101`的`V355-C01E02/E03/E04`。
- `scenes.tsv:101`当前E04 required只列`V353U001`，optional只列CH036；已移除`MECHA_GUARDIAN_Z`重复alias。

### 2.3 人口、损伤与机体预算：PASS

- Episode `C01E02-四张封存令-v1.md:199-239,243-251,307-315`保持原始29人全部楼外；两名接驳员在其后进入，与纪存、唐胶、兜灯组成馆内5人。R5失败不回刷29人。
- `C01E02-runtime-contract-v1.tsv:35-48`与`C01E02-graybox-constants-v1.tsv:33-37,40,43`同值锁定：29人隐藏楼外、5人退路、跌跌非第六人、SEG3反折、消防机左前腿过载、勇拳零动作、馆守Z被动、白函远程无身体，以及白函ADV后唯一原子提交。
- Episode `:384-386`把供水总管热损、商业后勤风道局部烧损、档案主库紧急冷却、馆守Z右臂连接、完整移动脊柱未暴露和白函预布框位全部交给E03；不重演撤离、撤令或消防机承梁。
- `PB-V357-C01-S03.md:14,28,32`只从该快照起步：29人不回刷，5人不膨胀；馆守Z、勇拳、白函的首次身体动作均在E03。
- `PB-V357-C01-S04.md:14,22,27,34,50`先继承E02伤痕再叠E03增量；五人安全后才执行三类载荷选二，人员不得成为载荷。
- `v35_5_c01_c03_state_propagation_v35_5.tsv:3-5`逐话同值，含`moving_spine=NOT_EXPOSED`与`people_cargo=FORBIDDEN`。

### 2.4 快照图谱与旧入口主体降级：PASS

- `graph_nodes.tsv:885-891`存在当前E02、唯一快照、消防机包、七海分域、Runtime/Graybox及S03/S04节点。
- `graph_edges.tsv:1871,1877-1879`构成完整闭环：E02 `submits` 快照，快照分别`feeds` S03、`feeds` S04、`constrains` state propagation。精确查询`node N_C01E02_ATOMIC_PHYSICAL_SNAPSHOT`只返回这组现行关系。
- `graph_nodes.tsv:157-160,162-163`已将旧合并版、17节点流程、A/B/C路线档、执行单位池及标准化三话/33节点流程降为`historical_superseded_by_v359_story_first`。
- `canonical_terms.tsv:19-23,30`已把旧EP01、路线档与执行单位池标为historical，并把馆守Z改成E01低热、E02零动作、E03首控/断臂的现行定义。
- `consistency_watchlist.tsv:17,28,30-31,53`及`doc_registry.tsv:47-48,57-58`均已把旧六回合/三话入口降为历史来源。
- `jicun_archive_terminal_views.tsv:7`的当前档案终端入口为`V355-C01E01`唯一六站路线加两个连续视点，明确不得恢复A/B/C并排路线。

## 3. 活跃冲突与最小修法

### PATCH-1：R07默认查询仍返回旧formal/battle

**证据：**

- `entities.tsv:48`的核心`R07`仍把formal/battle写成已降历史的`C01E03-04`。
- `wanji_roster_zone_coverage.tsv:8`仍写“新1-2支援”。
- `consistency_watchlist.tsv:57`的`CW045`仍以`fixed_watch`写“新1-2第3回合再支援”。该行会被默认`canon-query 豪司`直接返回。
- `entities.tsv:144`的`MECHA_SHA_YONG_WANG_SUPPORT`也仍用`C01E03-04`作first formal，尽管自身policy与当前场景都把实际支援放在C05。

**最小修法：**

1. `entities.tsv:48`把R07 formal/battle迁到`V355-C01E03`，policy写明这是豪司驾驶勇拳的包级首次正式/战斗介入；社勇王真机首控仍为`V355-C03E03`。
2. `wanji_roster_zone_coverage.tsv:8`改为“E01锚件预告；V355-C01E03豪司/勇拳介入；V355-C03E03社勇王首控”。
3. `consistency_watchlist.tsv:57`把“新1-2第3回合”改为`V355-C01E03`，并引用当前S03 PB/Canon场景。
4. `entities.tsv:144`不再引用historical scene；formal/battle统一到当前C05场景ID`C05E20-BRAVERY-COMBO`，或若继续保留V25候选ID，则必须把该行明确降为historical/candidate source，不能给当前查询一个旧C01 formal答案。
5. 在`canon-smoke-test.sh`增加精确`entity R07`断言：核心R07不得再出现`C01E03-04`，且应能读到`V355-C01E03`。

### PATCH-2：馆守Z alias实体查询与当前图节点仍夹带旧入口

**证据：**

- 精确`canon-query entity MECHA_GUARDIAN_Z`已正确输出`alias_redirect -> V353U001`，但随后还会返回`MECHA_GUARDIAN_Z_SHOULDER_CHANNEL`；原因是`entities.tsv:332`仍用废弃alias作`source_group_id`，且first三字段仍为旧通用`C01E03`。
- `graph_nodes.tsv:55`的当前`N_GUANSHOU_Z`仍由旧数据源拥有，notes没有现行三阶段生命周期。
- 精确`canon-query node N_GUANSHOU_Z`只返回`graph_edges.tsv:87,89,139`的E113/E115/E135；其中E115/E135仍写“当前新1-2正式战”，且三条relation均未标historical。查询没有返回E01低热、E02零动作、E03首控的现行边。

**最小修法：**

1. `entities.tsv:332`把父ID改为`V353U001`，first三字段改为`V355-C01E03`；它仍是部位/地图机制，不新增机体计数。
2. `graph_nodes.tsv:55`将owner改为`DATA_CANON_ENTITIES`，aliases加入`V353U001`，notes写明E01低热、E02零身体动作/右臂连接、E03首控和断臂。
3. E113改为`historical_introduces`，E115/E135改为`historical_reenters_body`并删除“当前新1-2”措辞。
4. 新增三条现行边：E01 Story-First对馆守Z为低热预告，E02 Story-First/原子快照约束零动作和右臂连接，S03 PB定义E03首控与断臂。
5. smoke对alias查询增加“除重定向后的`V353U001`外不得返回第二个entity_id”的断言，并对`N_GUANSHOU_Z`要求至少一条当前V35.9关系。

历史场景中保留`MECHA_GUARDIAN_Z`用于追溯不构成本条失败；本条只处理默认实体查询和当前图节点。

### PATCH-3：旧标准化三话节点已历史化，但11条关系边未历史化

定向结构审计对六个本轮目标历史节点检查所有入/出边，仍得到11条非historical relation：

- `graph_edges.tsv:311-313,315-316`：E357、E358、E359、E361、E362仍为`constrained_by/uses/introduces_canon/threads_fire_alarm`。
- `graph_edges.tsv:450,455`：E496、E501仍把V12样板写成受旧33节点流程的现行约束。
- `graph_edges.tsv:1128,1131,1134,1141`：E1174、E1177、E1180、E1187仍以普通`maps_to`指向已历史化的`N_CH01_STANDARDIZED_FLOW`。

**最小修法：** E357改`historical_constrained_by`；E358/E359改`historical_uses`；E361改`historical_introduces`；E362改`historical_threads_fire_alarm`；E496/E501改`historical_constrained_by`；E1174/E1177/E1180/E1187改`historical_maps_to`。同步把notes里的“现行/新1-2/新1-3”改为“历史三话来源”，当前答案统一指向V35.9四话链。

在`canon-smoke-test.sh`增加结构断言：凡入/出`N_EP01_MERGED_V03`、`N_CH01_EP01_MERGED_FLOW`、`N_EP01_ROUTE_TIERS`、`N_EP01_LEGAL_EXECUTION_UNITS`、`N_CH01_STANDARDIZED_SCRIPT`、`N_CH01_STANDARDIZED_FLOW`的边，relation必须含`historical`。这样机器PASS才覆盖“节点与边一起降级”，而不只检查节点status。

本席没有把其余早期图谱边或全库悬空边算作E02回归；上述11条均直接接触本轮声明已迁移的六个历史节点。

## 4. 独立校验结果

- `scripts/canon-smoke-test.sh`：`PASS`，输出`Canon smoke test passed`。
- `scripts/canon-check-godot.sh --strict`：`PASS`，无运行时违规。
- `python3 scripts/check_v35_8_slot_loadout.py`：`PASS`，95槽manifest/action/source/selector/lifecycle/asset/high-density合同闭合。
- 定向TSV审计：CH036时序、CH037预告边界、E04 alias、旧八场historical、三条snapshot下游边均`PASS`；旧目标节点关系审计为`FAIL count=11`，即PATCH-3列出的11条边。

这些机器PASS与本席`PATCH`不矛盾：当前smoke在`scripts/canon-smoke-test.sh:161-182`只检查若干旧节点status与两个术语/watchlist状态，在`:69-75`只确认alias重定向主行；它没有检查R07精确查询、alias额外entity命中或历史节点关联边relation。

## 5. r4复验门槛

补丁完成后只需复验以下四项：

1. `canon-query entity R07`不再返回任何当前行的`C01E03-04`；核心包首次正式/战斗答案为`V355-C01E03`。
2. `canon-query entity MECHA_GUARDIAN_Z`只重定向到`V353U001`；`node N_GUANSHOU_Z`同时给出现行E01/E02/E03生命周期边，旧边明确historical。
3. 上述六个历史节点的所有入/出边relation均含`historical`；显式历史查询仍能追溯旧素材。
4. Canon smoke、Godot strict与V35.8 strict继续通过；`graph_edges.tsv:1877-1879`和S03/S04/state propagation保持不动。

复验通过即可转`PASS`；无需再次修改C01E02正文、Runtime/Graybox或物理快照。
