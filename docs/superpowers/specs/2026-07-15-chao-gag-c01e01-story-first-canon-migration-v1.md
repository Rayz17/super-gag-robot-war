# C01E01 Story-First Canon Migration v1

> Status: `working_canon_migration_applied_and_validated`
>
> Scope: `C01E01 -> C01E04 / V357-C01-S01 -> S04`
>
> Reconstruction source: `V35.9/rebuild/episodes/C01/C01E01-最后一条闭馆路线-v1.md`

## 1. Reason

旧候选层同时存在五类会令C01失去常识重力或在后续写作中反复回弹的问题：

1. `C01_COLLECTION_PRIORITY`把人命与馆藏放在同一选择枚举里。
2. E01胜利状态没有区分“越过资产区闭馆线”和“真正离开建筑”。
3. 白函在E02的远程压场与实体Boss首显互相冲突，削弱E03升级峰。
4. 七海在零号异常前后的私人/公务身份及第一条系统命令时序不清。
5. 馆守Z右臂、L1远星副柜、闭馆熄灯与四令夺权缺少唯一物理快照，后话容易各写一套。

## 2. Applied Changes

| Migration | Change | Canon level | Downstream lock |
|---|---|---|---|
| `C01MIG003` | 白函E02仅远程语音、重框投影、区域改报和从机调度；无格、无HP、不可受击。E03完整身体首次占格、切图、承伤并带伤撤离 | working | E02不得制作实体Boss；E03必须制作完整首战资产 |
| `C01MIG004` | 废止E01人命/馆藏优先枚举，固定`C01_EVAC_PRIORITY=PEOPLE_FIRST_FIXED`；E04在人员全部脱险后另建载荷取舍 | working | 旧`C01_COLLECTION_PRIORITY`只保留兼容别名，不得参与人命判定 |
| `C01MIG005` | 七海在零号前仅私人语音；零号后进入只读公务风险频道；E01不改变现场系统，第一条系统命令留E02 | working | 不得把私人催饭写成监控权限或提前放水 |
| `C01MIG006` | 馆守Z右臂核心仍接在肩部，滑架仅托拆下检修的前臂外甲、检修板和安全索 | working | E03主动切离仍可修筋束，不能把右臂写成开场已拆下 |
| `C01MIG007` | L1新增只读延迟回信副柜，只读取L3离线缓存元数据；E01末提交唯一物理快照 | working | 不开放L3、不实时远星通信；E02必须逐项读取快照 |

## 3. Unique E01 End Snapshot

E01成功后必须原子提交，失败重试不得留下半套状态：

- 29人、4个撤离Token全部在L1前厅黄线集结，尚未离开建筑。
- 小满、阿澄和前厅值守员仍构成不可拆照看组。
- 展陈灯因九点闭馆程序熄灭；城市电网与维生在线。
- 半开防火门被锁死；馆守Z胸灯被切断；旧路由数字钥匙被冻结；B1消防泵压归零。
- 烟进入前厅，喷淋失效。
- 纪存只发送真实但不完整的消防回线；外部捕获路由地址和纪存声纹。
- 馆守Z右臂核心仍连接，只有前臂外甲拆检。
- L1远星副柜只读取L3离线缓存，不具备回复与实时通信能力。
- 跌跌主动侧倒卡轨由玩家确认；机器犬自主选择维修员，玩家只选择开路风险。
- 兜灯硬停权与唐胶材料否决权继续有效，不由纪存授予。

## 4. Data And Source Updates

已更新：

- `data/canon/entities.tsv`
- `data/canon/scenes.tsv`
- `data/canon/wanji_locations.tsv`
- `data/canon/wanji_exhibition_zones.tsv`
- `data/story/v35_7_author_slot_architecture_v35_7.tsv`
- `data/story/v35_5_c01_c03_state_propagation_v35_5.tsv`
- `data/story/v35_5_c01_c03_slot_episode_mapping_v35_5.tsv`
- `data/story/v35_5_c01_c03_enemy_asset_budget_v35_5.tsv`
- `data/story/v35_5_c01_c03_mecha_exposure_v35_5.tsv`
- `scripts/build_v35_8_slot_loadout.py`及其V35.8生成表
- `V35.5-C01-C03开局Pressure-Board-v35.5.md`
- `V35.9/chapters/C01/PB-V357-C01-S01.md`
- `V35.9/chapters/C01/PB-V357-C01-S02.md`
- `V35.9/rebuild/maps/C01-逐章重构地图-v1.md`

历史Reader与旧审稿回执不回写；它们保留为问题来源证据，并由本迁移和重构稿明确取代。

## 5. Blast Radius

- 故事：C01E02必须从真实火场撤离开始；C01E03独占白函实体首战和断臂成桥；C01E04才进行人员脱险后的载荷取舍。
- 玩法：E01四Token、三回合及失败重试采用唯一合同；E02无白函Boss格；E03需要完整Boss动作与受损撤退。
- 美术：E02只需白函远程投影子资产；E03需要完整白框身体。馆守Z E01不得制作空肩开场图。
- 关系：七海的私人熟悉和公务冲突有明确切换点；唐胶、兜灯的专业权不再被写成纪存赐予。
- 宏观：远星迟到效应维持离线/错序口径；索引在C11前仍无连续第一人称。
- 运行时：`C01E01-runtime-contract-v1.tsv`与`C01E01-graybox-constants-v1.tsv`是E01制作的唯一局部合同。

## 6. Validation Requirements

放行C01E01前必须同时满足：

1. V35.8生成器重跑后，S02白函为远程非实体、S03为完整实体首战。
2. 旧`C01_COLLECTION_PRIORITY`不再出现在活跃S01/S02输入合同中。
3. 两张E01 TSV列数一致，三回合纸面推演只产生一个成功提交点。
4. Canon smoke test通过。
5. 独立玩法制作席与Canon/宏观/物理席复核为PASS。

## 7. Validation Result

C01E01已于2026-07-15完成独立验收：

- 游戏制作/关卡合同席：`PASS`，见`V35.9/rebuild/reviews/C01E01/16-gameplay-targeted-recheck-r4.md`。
- Canon/宏观谜团/物理连续性席：`PASS`，见`V35.9/rebuild/reviews/C01E01/21-canon-final-recheck-r6.md`。
- V35.8 strict、Godot strict、Canon smoke、Runtime/Graybox与相关Canon/图谱/V35.5/V35.8 TSV结构全部通过。
- 当前状态升为`accepted_story_audience_production_canon`；C01E02必须且只能从本文件第三节的唯一物理期末快照继承。
