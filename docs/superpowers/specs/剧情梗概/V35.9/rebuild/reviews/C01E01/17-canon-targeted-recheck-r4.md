# C01E01 Canon / 宏观谜团 / 物理连续性定向复验 r4

> Review seat: `Canon / macro mystery / physical continuity`
>
> Scope: 只复验`14-canon-final-pass-r3.md`的7项最小修复与7条转PASS验收；不补剧情，不替上游圆场。
>
> Evidence boundary: 当前工作区中的C01E01正文/结算、Runtime/Graybox、C01地图、C01MIG003-007、活跃Canon与图谱查询面、V35.5/V35.7、生成后的V35.8 S01-S03。
>
> Ruling: **`PATCH`**
>
> Release effect: **暂不得转`accepted_story_audience_production_canon`。Story Core无需重写；关闭下列三个根因并定向r5复验即可。**

## 一、独立总判定

本轮不是沿用`15-r3-semantic-propagation-resolution.md`的自报结论，而是从当前文件重新取证。C01E01的主体事实已经大体收束：29人只到L1前厅；闭馆灯与四令分开；七海时序正确；L1副柜只读L3离线缓存；S02不再重复救维修员；白函E02远程、E03具身；索引在C11前没有连续第一人称。

但是，7项最小修复中只有**5项完全关闭**。剩余两项存在活跃层反证：

1. **右臂E03迁移仍会从图谱查询面和V35.8 S02高层合同回弹。** 精确动作行写了“不飞拳”，但同槽高层玩法/装载字段仍要求馆守Z以“飞拳/断臂成桥”改变战场；`canon-query`还会返回未标历史的V31节点和“C01E02登记飞拳单元首登”边。
2. **S01唯一原子提交仍被Graybox第二提交点破坏。** Runtime已经把`RT011`改成非持久Clear、把`RT013S`定为唯一持久事务，但`GB019`仍明确写`commit persistent state only here`。

此外，第7条总验收未通过：V35.8 strict validation与Godot strict均绿，但`canon-smoke-test.sh`当前实际退出1，仍在断言迁移前的旧场景文案与旧七海unlock名。因此本席不能用“生成表validated”代替跨层语义关闭，最终判`PATCH`，不判`PASS`。

## 二、7项最小修复复验

| # | r3最小修复 | r4判定 | 当前证据 | 残留 |
|---|---|---|---|---|
| 1 | 清理Canon场景活跃旧链 | **PASS** | `scenes.tsv:16-18,98`建立三回合救援、七海公务台、四令接管与V355入口；`:19-21`旧六回合链均为`historical_runtime_reference/HISTORICAL_RUNTIME_ONLY`；`:35`只在人员脱险后提交`C01_CARGO_PRIORITY`。 | 无本项活跃场景残留。历史行按本轮规则允许保留。 |
| 2 | 右臂离体/飞拳/成桥锁到E03 | **PATCH** | `entities.tsv:46,59,66`、`scenes.tsv:30-31,99-100`、`V355A03:4`及S02精确动作`V358ACT002-06`都写明E02不离体、不抬肩、不飞拳，E03才首显/首战/切离。 | 图谱与V35.8高层合同仍可回弹，详见第三节R4-P01。 |
| 3 | 修正V35.5闭馆锚 | **PASS** | `v35_5_c01_closing_route_anchor:4`为连接态右臂；`:19-21`拆为B1机库窗、L1旧影像厅副柜、B2远端监视窗。V35.5母板`:149,165,176`同步同一物理口径。 | 未发现远星副柜重新绑定B1或右臂开场已离体。 |
| 4 | 统一S01胜败合同 | **PASS** | PB S01`:32`、V35.5母板`:178`、正文`:199-202`、`RT011F/RT011B`与`V358GAME001`一致：唯一失败为R3仍有Token未集结；失败回到setup且零提交；危险角只重瞄；回充为post-clear。 | 无“关键展件坠落/胸灯误烧Game Over”活跃残留。 |
| 5 | 生成器覆盖S01失败与S02机器犬 | **PASS** | 生成器`SLOT_FAILURE_PRESSURE_OVERRIDES`含S01零提交重试；S02动作/签名覆盖读取`ALL_29_STAGED_FRONT_HALL_NOT_CITY_SAFE`。产物`V358GAME001:2`、`V358U002-05:11`、`V358ACT002-05:11`已同步。 | S01的“维修员”属于初始D5内部人员，不是S02重生；S02没有再生成第五Token。 |
| 6 | 原子化成功提交 | **PATCH** | `RT011:13`明确只写非持久Battle Clear，`RT013S:19`明确唯一持久事务；正文结算`:248`指向`RT013S_ATOMIC_PAYLOAD`。 | `graybox-constants:20`仍令`GB019/R3_success`“commit persistent state only here”，形成第二持久提交语义，详见R4-P02。 |
| 7 | 消除“断灯”歧义 | **PASS** | `v35_7_author_slot_architecture:2`与V35.5母板`:176`均分开写：展陈灯由闭馆程序熄灭，城市电网/维生在线；四令另锁门、断馆守Z胸灯、冻钥匙、停B1泵。`RT013S`同口径。 | 未发现活跃S01把“断灯”重新解释成全馆断电。 |

## 三、仍未关闭的精确残留

### R4-P01 右臂E03在活跃查询面与V35.8高层合同回弹

**严重度：P1。对应最小修复#2、验收#2。**

已正确的下层事实：

- `entities.tsv:46`将飞拳单元的首伏笔、正式出现、首战全部锁到`V355-C01E03`。
- `entities.tsv:59`允许切割标尺机在E02切消防/排火设施和检修外甲，明确禁止让右臂离体或成桥。
- `V358ACT002-06:12`明确馆守Z在S02只开放被动温度传感与冷却继电，`不开胸灯、不抬肩、不飞拳`。
- `V358ACT003-01:13`才让馆守Z执行飞拳与断臂成桥。

但活跃读取面仍有两组反证：

1. `v35_8_slot_gameplay_contract_v35_8.tsv:3`的S02 `map_or_space_contract`与`named_unit_action_contract`仍列`馆守Z:承重/飞拳/展舰护卫`，并要求这些单位“分别改变地形、目标或规则”。`v35_8_slot_mecha_ip_play_contract_v35_8.tsv:3`的S02单位后果也仍挂`半跪托馆、断臂成桥、终局托开馆门`。这与同槽精确动作的“不飞拳”冲突；制作端若读高层合同，仍会提前消费E03动作。
2. `canon-query.sh 展柜飞拳单元`除了返回正确实体行，还会返回未降级的旧图谱：`doc_registry.tsv:346`仍要求制作中庭巨机地图/右臂桥时优先查V31 C01E02；`graph_nodes.tsv:539`仍为`needs_review`而非historical；`graph_edges.tsv:1209-1210,1218`仍声称C01E02右臂卡桥、飞拳单元首登，并让下一话承接右臂桥债。这些不是Reader正文，也没有明确historical状态，属于活跃Canon查询回弹。

**最小修复：**

- 在生成器给`V357-C01-S02 + V353U001`增加槽位级`battle_role/signature`覆盖，使重新生成后的`V358GAME002`与`V358LOAD002`只写“被动温度传感/冷却继电/连接态右臂”，不得出现飞拳、断臂成桥或离体地图动作。
- 不必删除V31源packet；将`DOC_V31_C01E02_PACKET`、`N_V31_C01E02_PACKET`及相关E1257/E1258/E1260/E1266等边显式降为historical/deprecated source，或增加迁移重定向，使普通`canon-query`不能把它与当前首登规则并列为可执行口径。

### R4-P02 Graybox仍存在第二持久提交点

**严重度：P1。对应最小修复#6、验收#3。**

- `RT011`已经正确：`BATTLE_CLEAR_RECEIPT_NONPERSISTENT`，下游明确`RT013S_IS_ONLY_PERSISTENT_COMMIT`。
- `RT013S`已经正确：在四令完成后一次提交29人、右臂、L1副柜、灯光、电网、门、钥匙、泵、烟与喷淋状态。
- 但`C01E01-graybox-constants-v1.tsv:20`仍把`GB019/R3_success`定义为`commit persistent state only here`。此时消防图声纹捕获和四令尚未进入`RT013/RT013S`，故会产生“29人已持久化、四令与物理快照尚未持久化”的半套状态。

**最小修复：** 将`GB019`改成“只满足本地Battle Clear条件，不写持久状态；唯一持久提交由RT013S完成”。如保留`GB014`的`atomic_receipt`名称，应明确它是回合内局部回执而非Episode persistence，避免实现端再次生成第二事务。

### R4-P03 Canon smoke仍断言迁移前事实

**严重度：P2，但直接导致验收#7失败。**

- `python3 scripts/check_v35_8_slot_loadout.py --max-errors 80`：PASS。
- `scripts/canon-check-godot.sh --strict`：PASS。
- `scripts/canon-smoke-test.sh`：**exit 1**。首个失败位于脚本`:24`，它仍要求历史`C01E02-BATTLE-START`包含“第一话高潮保护战”，而当前Canon已正确将该行改为`historical_runtime_reference/HISTORICAL_RUNTIME_ONLY`。
- 脚本`:61`还预期旧unlock `qihai_console_unlocked`，当前`scenes.tsv:15`已迁为`qihai_official_risk_channel_unlocked`；修完首个断言后这里仍会继续失败。

**最小修复：** 更新smoke断言，使旧六回合行验证“明确历史且不得覆盖新E01”，并使七海unlock验证当前正式风险频道名；随后让脚本完整跑到末尾，而不是只绕过首个失败。

## 四、7条转PASS验收复核

| # | 验收条款 | r4判定 | 证据与理由 |
|---|---|---|---|
| 1 | `C01_COLLECTION_PRIORITY`只在弃用/迁移语境 | **PASS** | 本轮定向`rg`只命中PB S01`:48`的“弃用兼容别名”；活跃scene unlock、V35.5/V35.7状态和V35.8 S01-S03均使用`C01_EVAC_PRIORITY`或E04的`C01_CARGO_PRIORITY`。 |
| 2 | 无活跃三选二、旧六回合战、E02离体右臂 | **PATCH** | 三选二已改为E04载荷二保一，六回合场景已标历史；但右臂仍从V35.8 S02高层合同和未历史化图谱查询面回弹。 |
| 3 | S01失败零提交；成功只有一个原子持久事务 | **PATCH** | 失败合同已关闭；Runtime只有`RT013S`，但Graybox `GB019`仍声明另一个persistent commit。 |
| 4 | S02读取29人在前厅且不再救维修员 | **PASS** | `V358U002-05`与`V358ACT002-05`均读取29人前厅态，改做出口烟流侦察、C3牵引和消防软管稳定；PB S02`:14,25,32`要求29人从前厅真正离楼。 |
| 5 | L1副柜所有活跃锚点均为旧影像厅出口/L3离线缓存 | **PASS** | `entities.tsv:64`、`scenes.tsv:14`、`wanji_locations.tsv:14-15`、`wanji_exhibition_zones.tsv:9`、`V355A18B:20`及正文`:107,233`一致；B1只剩独立机库参观窗。 |
| 6 | 白函E02远程/E03具身；索引C11前无连续第一人称 | **PASS** | 白函由`entities.tsv:471`、`V358U002-02:8`、`V358ASSET002-02:8`锁为远程无格无HP，`V358U003-03:15`与资产`:15`才为完整实体Boss。索引由`v35_7_mystery_slot_binding:5`锁`INDEX_COMPONENT_ONLY -> INDEX_PERSONHOOD_BORN_LOCK`，正式出生在C11；C01-C10活跃场面未发现索引自述。“我来组成头部”等IP台词候选不是索引发言。 |
| 7 | 生成、strict、smoke、定向rg及语义复验全通过 | **PATCH** | 生成产物时间晚于生成器且覆盖已进入产物；V35.8 strict与Godot strict通过；相关TSV列宽均一致。但Canon smoke实际失败，定向rg/查询又发现R4-P01与R4-P02。 |

## 五、验证记录与边界

- V35.8生成器修改时间为`2026-07-15 15:57:20`，四张关键生成表时间均为`2026-07-15 16:02:24`；可确认当前产物在本轮生成器补丁之后生成。本席遵守“除审稿文件外不修改文件”，没有再次执行会重写产物的builder。
- `check_v35_8_slot_loadout.py --max-errors 80`通过：95槽闭合，当前V35.8行均为`validated_v35_8`。
- `canon-check-godot.sh --strict`通过：当前Godot运行文件没有命中既有runtime rule。
- Runtime为21行/9列，Graybox为23行/4列；Canon四表、V35.5/V35.7与V35.8关键表均无列宽异常。
- `canon-smoke-test.sh`失败；因此`15-r3-semantic-propagation-resolution.md:41`所记“PASS”不再代表当前工作区实况。
- 历史Reader、`historical_runtime_reference`与`historical_story_source`行不计活跃冲突；本轮只拦截未显式历史化、仍会被查询/生成/制作读取的口径。

## 六、转PASS的最小r5门槛

只需关闭三个根因，无需重写C01E01剧情：

1. 生成器为S02馆守Z覆盖高层角色/签名字段，重跑后`V358GAME002`、`V358LOAD002`和精确动作统一“不飞拳”；V31右臂桥图谱行显式历史化或迁移重定向。
2. Graybox `GB019`取消持久提交，唯一Episode persistence仍为`RT013S`。
3. 更新并完整跑通Canon smoke；随后重跑V35.8 strict、Godot strict与本轮定向查询，确认不再出现活跃回弹。

**最终裁定：`PATCH`。五项已真实关闭；两项语义迁移与一项验收脚本仍需定向修复。**
