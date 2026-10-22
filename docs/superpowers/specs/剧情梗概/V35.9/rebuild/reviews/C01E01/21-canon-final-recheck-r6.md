# C01E01 Canon / 宏观谜团 / 物理连续性最终定向复验 r6

> Review seat: `Canon / macro mystery / physical continuity`
>
> Scope: 只复验`19-canon-targeted-recheck-r5.md`提出的唯一残留`R5-P01`，并据当前工作区重验该文列明的7条转PASS门槛；不补剧情，不扩大审稿范围。
>
> Evidence rule: `20-baihan-production-boundary-resolution-r5.md`只作为待证定位单，不作为关闭证据。结论来自两张当前V35.5生产表、活跃Canon/上游/生成产物、Runtime/Graybox、定向查询和实际校验命令。
>
> Ruling: **`PASS`**
>
> Release effect: **未发现新的活跃反证。`R5-P01`与7条总门槛均已真实关闭，允许C01E01转入`accepted_story_audience_production_canon`。**

## 一、最终独立判定

本轮独立读取了`v35_5_c01_c03_enemy_asset_budget_v35_5.tsv`与`v35_5_c01_c03_mecha_exposure_v35_5.tsv`的当前内容，并以结构化字段断言复核白函两阶段边界。两张表已与Canon实体、V35.8单位/动作/资产/生命周期口径一致：

- E02只有远程语音、重框投影、区域改报与从机调度；无格、无HP、不可受击，也不计入实体机体暴露。
- E03才首次出现完整身体，进入Boss格位、承伤、执行折叠臂动作、承受飞拳改图并带伤撤离。

此前`R5-P01`的两处表面残留已由同一根因修复真实关闭；没有发现白函完整实体或Boss动作再次提前到E02的活跃生产入口。

## 二、R5-P01定向复验

| 待验位置 | r6判定 | 当前实际证据 |
|---|---|---|
| `v35_5_c01_c03_enemy_asset_budget_v35_5.tsv:6` | **PASS** | `first_episode`明确拆为`V355-C01E02远程非实体;V355-C01E03实体首战`；`role`拆为E02远程指挥/E03实体Boss；`asset_tier`为`remote_subasset_then_flagship_enemy`。`mandatory_actions`以E02与E03分段，`production_boundary`进一步锁定E02只制作无格、无HP、不可受击且不计实体暴露的远程子资产，完整轮廓、Boss阶段、折叠臂、受击和伤退全部留E03。 |
| `v35_5_c01_c03_mecha_exposure_v35_5.tsv:3-4` | **PASS** | E02具名实体敌机只列冷却针车、切割标尺机，暴露数已为`6`；白函仅位于`non_count_anchors`，显式标注`remote_projection_non_count`。E03才把`ENEMY_C01_SEAL_COMMANDER_BAIHAN`列入具名敌机并计入实体暴露。 |
| 跨层一致性 | **PASS** | `entities.tsv:471`、`v35_8_slot_unit_manifest_v35_8.tsv:8,15`、`v35_8_slot_action_delta_v35_8.tsv:8,15`、`v35_8_slot_asset_manifest_v35_8.tsv:8,15`、`v35_8_lifecycle_event_review_v35_8.tsv:10,17`均维持同一E02远程/E03具身边界。`canon-query.sh '封存指挥机“白函”'`返回首伏笔E02、正式出现与首战E03。 |

结构化语义断言也已通过：E02实体敌机栏不含白函实体ID，白函投影标为非计数；E03实体敌机栏包含白函；敌方资产预算的五个阶段字段均具备明确E02/E03边界。

## 三、7条总门槛最终复验

| # | 验收条款 | r6判定 | 当前证据 |
|---|---|---|---|
| 1 | `C01_COLLECTION_PRIORITY`只在弃用/迁移语境 | **PASS** | 当前S01状态仍为`C01_EVAC_PRIORITY`；`runtime-contract-v1.tsv:20`仅把旧字段作为弃用兼容别名，不能选择人命；`v35_8_candidate_canon_migrations_v35_8.tsv:46`只记录迁移规则。E04在人员脱险后另用`C01_CARGO_PRIORITY`。 |
| 2 | 无活跃三选二、旧六回合战、E02离体右臂 | **PASS** | `scenes.tsv:19-21`旧六回合链为`historical_runtime_reference/HISTORICAL_RUNTIME_ONLY`；`:30-31`旧V31右臂桥为`historical_story_source/HISTORICAL_SOURCE_ONLY`；`:35`载荷取舍只在人员脱险后的E04。`entities.tsv:46,59,66`继续锁定E02右臂连接、E03才飞拳/成桥/永久切离。`canon-query.sh '展柜飞拳单元'`也把三项首时序全部返回E03，并把V31 packet标为historical/superseded。 |
| 3 | S01失败零提交，成功只有一个原子持久事务 | **PASS** | `runtime-contract-v1.tsv:13-15`中本地Battle Clear、失败和危险角重瞄均不提交持久状态；`:19`的`RT013S`仍是唯一原子持久事务。`graybox-constants-v1.tsv:15,20`同步声明局部回执不持久化。 |
| 4 | S02读取29人在前厅且不再救维修员 | **PASS** | `v35_5_c01_c03_state_propagation_v35_5.tsv:2-3`仍为E01的29人只到前厅、E02才真正离馆；`v35_8_slot_unit_manifest_v35_8.tsv:11`读取`ALL_29_STAGED_FRONT_HALL_NOT_CITY_SAFE`，机器犬只侦察烟流、牵引C3照看组和稳消防软管，明确不重复生成或救出维修员。对应动作表口径一致。 |
| 5 | L1副柜所有活跃锚点均为旧影像厅出口/L3离线缓存 | **PASS** | `entities.tsv:64`、`scenes.tsv:14`、`wanji_locations.tsv:15`、`wanji_exhibition_zones.tsv:9`、`v35_5_c01_closing_route_anchor_v35_5.tsv:20`一致：副柜位于L1旧影像厅出口，只读L3离线缓存，无回复键、实时通信、导航或当前远星政治信息。`RT013S`快照也沿用这一口径。 |
| 6 | 白函E02远程/E03具身；索引C11前无连续第一人称 | **PASS** | 白函两张V35.5生产表已按第二节关闭；Canon与V35.8交叉一致。索引仍由`v35_7_mystery_slot_binding_v35_7.tsv:5`锁定`INDEX_COMPONENT_ONLY > INDEX_LEARNING_VECTOR > INDEX_PERSONHOOD_BORN_LOCK`，并明确C11前不得出现连续人格第一人称；`canon-query.sh '索引天使'`返回C09仅预显影、C11才正式出现和首战。 |
| 7 | V35.8 strict、Godot strict、smoke、TSV shape、定向查询与语义复验全通过 | **PASS** | 三项正式脚本均以退出码0通过；20张相关TSV全部列宽一致；白函两表结构化字段断言、白函/右臂/索引定向查询和其余六门槛的定向`rg`均未发现活跃反证。 |

## 四、实际验证记录

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_v35_8_slot_loadout.py`：**PASS**。95个槽位的manifest/action/source/selector/lifecycle/asset/high-density合同闭合，全部为`validated_v35_8`。
- `PYTHONDONTWRITEBYTECODE=1 scripts/canon-check-godot.sh --strict`：**PASS**，无runtime violation。
- `PYTHONDONTWRITEBYTECODE=1 scripts/canon-smoke-test.sh`：**PASS**，完整输出`Canon smoke test passed`。
- `scripts/canon-query.sh '封存指挥机“白函”'`：**PASS**，E02远程首伏笔，E03实体首显/首战。
- `scripts/canon-query.sh '展柜飞拳单元'`：**PASS**，当前首伏笔/首显/首战均为E03，V31来源为historical/superseded。
- `scripts/canon-query.sh '索引天使'`：**PASS**，C09只预显影，C11正式出现/首战。
- TSV shape：**PASS**。两张目标V35.5表、V35.5状态/空间表、V35.7两表、V35.8单位/动作/资产/生命周期/玩法表、Canon四表、图谱三表及Runtime/Graybox共20张表均无异形行。
- 定向结构化语义断言：**PASS**。白函E02投影非计数、E03实体计数与完整Boss资产边界全部成立。

## 五、残留与放行

本次限定范围内：

- **没有未关闭残留。**
- **没有新增活跃反证。**
- 历史Reader、旧Godot试玩链和V31旧右臂桥仅以明确的historical/superseded记录保留，不构成活跃冲突。
- 不需要再改Episode、Runtime/Graybox、Canon实体、V35.5生产表或V35.8生成产物。

## 六、最终裁定

**`PASS`。** `R5-P01`已关闭，7条总门槛全部通过。C01E01获准转入：

`accepted_story_audience_production_canon`
