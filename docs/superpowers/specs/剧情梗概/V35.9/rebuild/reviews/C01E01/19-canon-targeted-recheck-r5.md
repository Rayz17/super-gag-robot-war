# C01E01 Canon / 宏观谜团 / 物理连续性定向复验 r5

> Review seat: `Canon / macro mystery / physical continuity`
>
> Scope: 只复验`17-canon-targeted-recheck-r4.md`的`R4-P01/P02/P03`及其7条转PASS门槛；不补剧情，不审查范围外的新创作。
>
> Evidence rule: `18-canon-r4-patch-resolution.md`仅作为待证清单；本结论来自当前工作区的源生成器、生成产物、Canon/图谱、Runtime/Graybox、V35.5/V35.7活跃上游与实际检查命令。
>
> Ruling: **`PATCH`**
>
> Release effect: **R4三项残留已全部关闭，但7条总门槛中的白函E02/E03资产连续性仍有一处活跃生产回弹；C01E01暂不转`accepted_story_audience_production_canon`。无需重写Story Core，只需修两张V35.5表中的同一根因。**

## 一、独立总判定

本轮没有采用补丁关闭记录的自报结论。重新取证后，`R4-P01/P02/P03`均已真实关闭：S02馆守Z高层合同不再调用飞拳；V31右臂桥只以历史源返回；Graybox不再形成第二持久事务；Canon smoke已更新到当前事实并完整通过。

但七条总门槛不能全部转PASS。当前仍有两张被图谱登记为生产入口的V35.5机器表，把白函在E02登记成可计数的具名Boss/旗舰敌机，并在E02资产预算中挂上折叠封存臂和“承受飞拳改图”。这与现行`C01MIG003`的“E02仅远程投影、无格无HP且非计数；E03才完整身体首显/首战”直接冲突。

这是一个根因、两处表面残留。除此之外，本次限定范围内未发现新的阻断。

## 二、R4-P01/P02/P03复验

| 项目 | r5判定 | 当前实际证据 |
|---|---|---|
| `R4-P01` S02右臂动作与V31图谱回弹 | **PASS** | 生成器`build_v35_8_slot_loadout.py:1198-1200,1297-1305,1319-1365`存在S02馆守Z槽位级单位补丁、动作、签名和`battle_role`覆盖。生成后的`V358GAME002`、`V358LOAD002`、`V358U002-06`、`V358ACT002-06`统一为被动温度传感、冷却继电、连接态右臂，并明确不开胸灯、不抬肩、不飞拳、不形成断臂地形；`V358ACT003-01`才执行飞拳/断臂成桥。`canon-query.sh 展柜飞拳单元`把当前实体首伏笔、正式出现和首战全部锁到`V355-C01E03`，旧V31 packet返回为`historical_superseded_episode_packet`；图谱节点为`historical_superseded_by_v359_c01mig006`，`graph_edges.tsv:1860`提供`superseded_by`重定向。 |
| `R4-P02` Graybox第二持久提交 | **PASS** | `runtime-contract-v1.tsv:13-19`中`RT011`只产生非持久Battle Clear，失败与瞄准重试均零提交，`RT013S`是唯一持久事务。`graybox-constants-v1.tsv:15`把GB014明确为`local_round_receipt`，`:20`把GB019明确为本地Battle Clear且不写持久状态，唯一Episode persistence仍指向`RT013S`。 |
| `R4-P03` Canon smoke旧断言 | **PASS** | `canon-smoke-test.sh:22-27`现验证旧六回合场景为`historical_runtime_reference/HISTORICAL_RUNTIME_ONLY`，`:58-64`验证七海当前公务风险频道及`qihai_official_risk_channel_unlocked`。本轮实际执行完整到末尾，输出`Canon smoke test passed`。 |

## 三、7条转PASS门槛

| # | 验收条款 | r5判定 | 证据与理由 |
|---|---|---|---|
| 1 | `C01_COLLECTION_PRIORITY`只在弃用/迁移语境 | **PASS** | V35.5/V35.7活跃上游、V35.8 S01-S03、现行PB与Runtime均以`C01_EVAC_PRIORITY`为E01人命状态，E04另用`C01_CARGO_PRIORITY`。现行PB S01只把旧字段称为弃用兼容别名；迁移文件只用于描述旧问题与废止规则。 |
| 2 | 无活跃三选二、旧六回合战、E02离体右臂 | **PASS** | `scenes.tsv:19-21`旧六回合链均为`historical_runtime_reference/HISTORICAL_RUNTIME_ONLY`；`:30-31`V31右臂桥均为`historical_story_source/HISTORICAL_SOURCE_ONLY`；`:35`三类载荷取舍只在全部人员脱险后的E04。`entities.tsv:46,59,66`及V35.8 S02生成产物均锁定E02右臂连接，E03才飞拳、成桥与永久切离。 |
| 3 | S01失败零提交，成功只有一个原子持久事务 | **PASS** | `RT011F`失败回到`BATTLE_SETUP`且无下游回执；`RT011B`危险角只重瞄；`RT011`为本地Clear；`RT013S`一次提交完整物理快照。GB014/GB019均不再声明持久化。`V358GAME001`同步写明失败不提交剧情、人员、失败计数、四令或展区状态。 |
| 4 | S02读取29人在前厅且不再救维修员 | **PASS** | `v35_5_c01_c03_state_propagation_v35_5.tsv:2-3`把E01输出锁为29人只到前厅、E02才真正离馆；`V358U002-05`与`V358ACT002-05`读取`ALL_29_STAGED_FRONT_HALL_NOT_CITY_SAFE`，机器犬改做出口烟流侦察、牵引C3照看组和稳定消防软管，明确不重复生成或救出维修员。 |
| 5 | L1副柜所有活跃锚点均为旧影像厅出口/L3离线缓存 | **PASS** | `entities.tsv:64`、`scenes.tsv:14`、`wanji_locations.tsv:14-15`、`wanji_exhibition_zones.tsv:9`、`v35_5_c01_closing_route_anchor_v35_5.tsv:20`与Episode正文`:107`一致：物理位置为L1旧影像厅出口，只读L3离线缓存，无回复键、实时通信、导航或当前远星政治信息。 |
| 6 | 白函E02远程/E03具身；索引C11前无连续第一人称 | **PATCH** | 白函的Canon实体、V35.5正文、V35.8生命周期/单位/动作/资产均已正确，索引边界也由`v35_7_mystery_slot_binding_v35_7.tsv:5`锁定；但两张活跃V35.5生产表仍回弹完整白函Boss，详见第四节。 |
| 7 | V35.8 strict、Godot strict、smoke、TSV shape、定向查询与语义复验全通过 | **PATCH** | 三项脚本与TSV shape均通过，右臂查询已分层；但定向语义复验发现门槛#6的活跃生产反证，因此本条不能只凭脚本绿灯判PASS。 |

## 四、唯一精确残留

### R5-P01 白函两阶段资产仍从V35.5生产表回弹

**严重度：P1。对应验收#6，并连带验收#7。**

当前正确事实非常明确：

- `entities.tsv:471`：E02仅远程封存语音、重框投影、区域改报和从机调度，无格、无HP、不可受击；E03才完整身体首显、首战和带伤撤离。
- `V35.5-C01-C03开局Pressure-Board-v35.5.md:200`：白函E02只以远程指挥标识和封存语音出现，实体Boss留到下一话。
- `v35_8_slot_asset_manifest_v35_8.tsv:8,15`：E02是`remote_projection_and_voice`且`remote_projection_non_count_until_physical_body_S03`；E03才是`enemy_or_boss`完整资产。
- `v35_8_lifecycle_event_review_v35_8.tsv:10,17`：E02远程非格位，E03才`first_visible_physical_body_and_first_battle`。

但当前仍有两处活跃反证：

1. `v35_5_c01_c03_enemy_asset_budget_v35_5.tsv:6`把白函的`first_episode`写为`V355-C01E02`，角色写为`C01具名Boss`，资产级为`flagship_enemy`，必做动作直接包含“折叠封存臂；承受飞拳改图”，且没有把这些实体动作锁到E03。
2. `v35_5_c01_c03_mecha_exposure_v35_5.tsv:3`把白函列入E02的`named_enemy_or_boss`并计入`countable_mecha_exposure=7`；同表`:4`又在E03再次列白函。现行V35.8已经明确E02远程投影不计实体机体暴露，因此E02的可计数值应排除白函远程子资产。

这两张表不能按旧稿/历史Reader豁免：`doc_registry.tsv:440`要求生成开局机体/IP账本和敌方资产前查暴露表，`:442`要求制作开局敌机美术、动画、战斗动作前查敌方资产预算。它们会直接把完整白函身体和飞拳受击动作提前排到E02。

**最小修复：**

1. 在敌方资产预算中把白函拆清两阶段：E02只预算远程语音、重框投影、区域改报和从机调度的非实体子资产；`flagship_enemy`、折叠封存臂、占格/承伤、飞拳改图、Boss阶段和伤退动作全部显式锁到`V355-C01E03`。若表结构不拆行，至少在`first_episode/role/asset_tier/mandatory_actions/production_boundary`五列写出E02远程、E03实体的阶段边界。
2. 在机体暴露表把E02白函标为`remote_projection_non_count`，从`countable_mecha_exposure`中剔除；按当前行内计数应由`7`改为`6`。E03白函实体计数保持不变。
3. 修后只需重跑这两表的TSV shape、白函定向`rg`、Canon smoke、V35.8 strict和Godot strict；无需改Episode、Runtime/Graybox、Canon实体、V35.8生成器或Story Core。

## 五、实际验证记录

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_v35_8_slot_loadout.py`：**PASS**，95槽及manifest/action/source/selector/lifecycle/asset/high-density合同闭合。
- `PYTHONDONTWRITEBYTECODE=1 scripts/canon-check-godot.sh --strict`：**PASS**，无runtime violation。
- `PYTHONDONTWRITEBYTECODE=1 scripts/canon-smoke-test.sh`：**PASS**，完整运行到`Canon smoke test passed`。
- `PYTHONDONTWRITEBYTECODE=1 scripts/canon-query.sh 展柜飞拳单元`：当前实体锁E03；V31 registry/node明确为historical/superseded。
- `PYTHONDONTWRITEBYTECODE=1 scripts/canon-query.sh 封存指挥机“白函”`：Canon查询口径正确，为E02远程、E03实体。
- TSV shape：Runtime/Graybox、Canon四表、图谱三表、V35.5状态/空间表及本次发现的两张生产表、V35.7两张表、V35.8四张关键生成表均无异形行；残留是字段语义错误，不是列宽错误。
- 生成器修改时间`2026-07-15 16:22:38`；四张关键V35.8产物均为`2026-07-15 16:22:59`，晚于生成器。为遵守“只写审稿文件”，本席没有运行会重写生成产物的builder。

## 六、最终裁定

**`PATCH`。** `R4-P01/P02/P03`均已关闭；唯一剩余根因是白函E02远程/E03实体的阶段边界尚未传播到两张活跃V35.5生产表。修复上述两行并定向r6复验即可，无需扩大施工范围。
