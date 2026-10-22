# C01E01 Canon / 宏观谜团 / 物理连续性终检 r3

> Review seat: `Canon / macro mystery / physical continuity`
>
> Evidence boundary: C01E01正文与结算、runtime/graybox、C01章地图、C01E01 Canon migration、四张Canon表、V35.5/V35.7活跃上游、生成后的V35.8 S01-S03
>
> Ruling: **`PATCH`**
>
> Release effect: **不得把C01E01改为`accepted_story_audience_production_canon`；完成下列定向传播补丁并重验后可转PASS。无需重写剧情。**

## 一、独立总判定

C01E01的当前可读正文、局部运行时合同和章节重构地图已经形成一套基本自洽的主事实：20:47馆内32人，其中29人为四枚撤离Token；E01胜利只把29人送到L1前厅黄线；展陈灯因九点闭馆熄灭，四令随后分别锁门、断馆守Z胸灯、冻旧路由数字钥匙、停B1消防泵；七海在零号前只作私人语音，零号后才进入只读公务频道；馆守Z右臂核心仍连接；L1副柜只读L3离线缓存；白函E02远程、E03具身；索引在C11前没有连续第一人称。

但是，**迁移声明已经写对，不等于所有活跃读取面已经迁完**。当前仍有Canon场景行、Canon实体行、V35.5锚点/母板、S01 Pressure Board和生成后的V35.8语义合同能够重新产出旧事实。严格校验器与smoke test均通过，只证明表结构和既有断言通过，没有发现这些跨层语义冲突。因此本席判`PATCH`，不是`PASS`；剩余问题均可定向修复，不构成推倒Story Core的`BLOCKER`。

证据简称：

- `EP` = `剧情梗概/V35.9/rebuild/episodes/C01/C01E01-最后一条闭馆路线-v1.md`
- `RT` = `剧情梗概/V35.9/rebuild/episodes/C01/C01E01-runtime-contract-v1.tsv`
- `GB` = `剧情梗概/V35.9/rebuild/episodes/C01/C01E01-graybox-constants-v1.tsv`
- `MAP` = `剧情梗概/V35.9/rebuild/maps/C01-逐章重构地图-v1.md`
- `MIG` = `2026-07-15-chao-gag-c01e01-story-first-canon-migration-v1.md`
- `PB1/PB2/PB3` = `剧情梗概/V35.9/chapters/C01/PB-V357-C01-S01..S03.md`

## 二、C01MIG003-007传播矩阵

| Migration | 判定 | 已成立证据 | 未关闭证据 / 风险 |
|---|---|---|---|
| `C01MIG003` 白函E02远程、E03具身 | **PASS** | `MAP:45-46,77-83,208`；`entities.tsv:471`；`PB2:14,28,32,36`；`PB3:14,22,28,32`；`v35_8_slot_unit_manifest:8,15`；`v35_8_slot_action_delta:8,15`；`v35_8_slot_asset_manifest:8,15`。S02明确无格、无HP、不可受击；S03为完整身体、完整Boss动作、承伤和带伤撤退。 | 无本迁移级冲突。`scenes.tsv:97`只列白函进入E02场面，但实体政策由`entities.tsv:471`和V35.8三表明确限制，当前不构成第二次实体首显。 |
| `C01MIG004` 人命固定优先、载荷取舍后移 | **PATCH** | `EP:221-225,247-249`；`RT:19-21`；`MAP:25,44-45,156-157,209`；`v35_5_c01_c03_state_propagation:2-3`；`V358MIG045`均已改为`PEOPLE_FIRST_FIXED`。 | `data/canon/scenes.tsv:96`仍在V355-C01E01的`unlocks`中提交`C01_COLLECTION_PRIORITY`；同表`:33`仍把“人、展品、服务器”作为三选二；`:17-19`仍把1-1接入旧六回合保护战，绕开29人前厅快照。旧Reader可保留，但这些是可被`canon-query`读到的活跃Canon行，不能按历史Reader豁免。 |
| `C01MIG005` 七海私人/公务/首命令时序 | **PASS** | `EP:73-83,107-113,155-171,236`；`RT:16`；`entities.tsv:34`；`scenes.tsv:13-16`；`PB1:40`。零号前无公务UI，零号后只读风险频道，E01没有改变现场系统的七海命令。`EP:171`是对人的口头疏散指示，不是系统写入。 | `EP:240`的`AVAILABLE_UNTIL_QH_CUTOFF`应由E02读取为“尚未发生的下一阶段”，但`RT:16,19`已把E01终态锁清，当前不单独阻断。 |
| `C01MIG006` 馆守Z右臂连接态到E03主动切离 | **PATCH** | `EP:91,237-238`；`RT:19`；`MAP:23,46,158,211`；`entities.tsv:66,474`；`wanji_locations.tsv:8,18`。00:30冷开场`EP:55-59`明确是E03切臂后的未来画面，不是E01当前快照。 | `entities.tsv:46`仍把“展柜飞拳单元/馆守Z右臂桥”首显、正式出现、首战全部放在C01E02；`scenes.tsv:28-29`仍把右臂卡桥、滑拳和切割右臂安排在1-2；`entities.tsv:59`仍令切割标尺机在E02触发右臂桥；`v35_5_c01_closing_route_anchor:4`仍写`real_mecha_fragment`，母板`V35.5:149`仍写“真机残肢/维修架”。这些会把E03的主动切离重新提前。 |
| `C01MIG007` L1只读副柜与唯一E01物理快照 | **PATCH** | `EP:107,153-169,225-249`；`RT:18-19`；`MAP:44-45,55,156,212`；`entities.tsv:64`；`scenes.tsv:14`；`wanji_locations.tsv:14-15`；`wanji_exhibition_zones.tsv:9`。当前正文和局部合同明确L1只读L3离线缓存、29人尚未离楼、闭馆灯与四令分离。 | `v35_5_c01_closing_route_anchor:19`仍把“远星延迟柜”与B1机库窗、零号侧廊合并在`ST06_DEPTH / WEZ_B1_01_HANGAR_VIEW`，会把L1载体重新挪回深层。`RT:13`先写`SUCCESS_COMMIT`，`RT:19`又写`COMMIT_UNIQUE_PHYSICAL_STATE`，与`MIG:31,78`要求的原子、唯一成功提交点存在事务歧义；需要明确两行同属一个原子事务，或只保留一个持久化commit。 |

## 三、跨迁移专项检查

### 1. 29人只到前厅

**局部事实PASS，活跃传播PATCH。**

- `EP:63-65`固定`21+4+1+1+2=29`，另有纪存、唐胶、兜灯三名核心员工，总数32。
- `EP:133,153,196,221-226`与`GB:3,11-20`固定四Token为`A11+B10+C3+D5=29`，C3不拆，R3才形成`29/29, 4/4`；尚未离开建筑。
- `RT:12-14,19`固定成功、失败回滚和E01末快照。
- 但`V358ACT002-05`及`V358LOAD002`仍让机器犬在S02“拖出最后一名维修员”。维修员已经包含在D5并在E01到达前厅，这会在E02重生一名不存在的滞留者。S02若继续使用机器犬，应改为从前厅向建筑出口侦察/牵引，不得再次救同一维修员。

### 2. 闭馆灯与四令分离

**局部事实PASS，上游措辞PATCH。**

- `EP:153`先写展陈灯按闭馆程序熄灭，城市电网、维生、B1泵仍在线；`EP:167`再写四令锁半开防火门、断馆守Z胸灯、冻数字钥匙、令B1泵压归零。
- `RT:18-19`与`MIG:33-40`完全一致。
- `v35_7_author_slot_architecture.tsv:2`的`next_logic`仍只写“锁门、断灯、冻钥匙、停泵”，“断灯”可被制作端误读为展陈灯或城市照明。应明确为“断馆守Z导览胸灯”，并保留展陈灯已经由闭馆程序熄灭。
- `V35.5母板:174`仍以“全馆逐区熄灯，唯独纪存脚下导览灯不灭”结束旧场面链，没有提交随后四令对胸灯/门/钥匙/泵的区别，需按唯一快照更新或明确被新PB取代。

### 3. 索引C11前无第一人称

**PASS。**

- `EP:21,248`只写共享分类组件与`NO_CONTINUOUS_SELF`。
- `v35_7_mystery_slot_binding.tsv:5`固定`INDEX_COMPONENT_ONLY -> ... -> INDEX_PERSONHOOD_BORN_LOCK`且写明“C11前不得出现连续人格第一人称”。
- `entities.tsv:100`把索引天使正式出现和首战均放在C11；`entities.tsv:471`明确白函不是索引人格。
- 在本次指定的活跃C01输入和V35.8 S01-S03中未发现索引以“我/我们”自述，白框相似性仍可由共享组件解释。

### 4. S01局部玩法合同是否能保持唯一快照

**PATCH。**

- `GB`全部22行均为4列，`RT`全部21行均为9列；纸面路线可在R3唯一形成`29/29,4/4`，失败回到setup且不提交故事状态。
- 但`PB1:32`与`V35.5母板:176`仍把“两台小机回充”“关键展件坠落”“胸灯误烧”写成胜败条件；这与`EP:199-202`、`RT:13-15`的“回充是通关后演出、失败仅为R3撤离未完成、非法角无损重瞄”冲突。
- `v35_8_slot_gameplay_contract.tsv:2`仍写“失败必须让下一逻辑真实恶化”，而`RT:14`明确`RETRY_NO_STATE_COMMIT`。严格校验器目前允许两者同时为validated，说明需要生成器级S01失败合同覆盖，不能只手改生成表。

## 四、验证结果与其边界

- `python3 scripts/check_v35_8_slot_loadout.py`：通过，95槽及相关生成表均为`validated_v35_8`。
- `scripts/canon-smoke-test.sh`：通过。
- `C01E01-runtime-contract-v1.tsv`：21行，全部9列。
- `C01E01-graybox-constants-v1.tsv`：22行，全部4列。

这些结果证明生成表结构、ID引用和现有程序断言闭合，**不能反证上面列出的语义冲突**。本次终检因此不接受“自动检查已绿”作为Canon传播完成证明。

## 五、最小修复清单

1. **清理Canon场景活跃旧链。** 更新`scenes.tsv:96`为`C01_EVAC_PRIORITY;C01_VISITOR_RESCUE_SEED;JICUN_COLLECTION_ANOMALY_SEED;C01_FIRE_ROUTE_CAPTURE;C01_PHYSICAL_SNAPSHOT`；将`:17-19`旧1-1六回合链明确降为历史/实现来源或重定向到新E01三回合合同；将`:33`改成只在人员脱险后选择`collection_core|living_area|public_archive`，人不得进入载荷枚举。
2. **封住右臂提前离体入口。** 将`entities.tsv:46,59`和`scenes.tsv:28-29`的右臂桥/飞拳实体动作迁到C01E03；E02的切割标尺机只可威胁消防管、路线或外甲，不得让右臂成为已离体地图单位。
3. **修正V35.5闭馆锚。** `V355A03`改为“右臂核心连接、仅外甲/检修板/安全索在滑架”；把`V355A18`拆成B1机库远景与L1旧影像厅出口副柜，远星副柜不得绑定B1 zone或暗示可达L3。
4. **统一S01胜败合同。** 更新`PB1:32`和`V35.5:176`：唯一失败为R3结束仍有Token未到黄线；小机回充是post-clear；兜灯否决只返回重瞄；不再出现关键展件坠落/误烧Game Over。
5. **修生成器而非只改产物。** 给`V358GAME001.failure_pressure_contract`加`MISSION_FAIL_TIMEOUT -> RETRY_NO_STATE_COMMIT`覆盖；给S02机器犬动作加槽位覆盖，读取`ALL_29_STAGED_FRONT_HALL_NOT_CITY_SAFE`，不得重复“拖出最后一名维修员”；重跑V35.8。
6. **原子化成功提交。** 将`RT011`与`RT013S`标成同一transaction，或让`RT011`只宣告战斗成功、唯一持久化commit留`RT013S`。任何中断都不得留下“29人已救但四令/物理快照未提交”的半套状态。
7. **消除“断灯”歧义。** 将V35.7 S01的下一逻辑明确为“锁半开防火门、断馆守Z胸灯、冻旧路由钥匙、停B1泵”，并另列“展陈灯已由闭馆程序熄灭；城市电网/维生在线”。

## 六、转PASS的精确验收

完成补丁后，需同时满足：

1. 在活跃Canon/V35.5/V35.7/V35.8 S01-S03中，`C01_COLLECTION_PRIORITY`只能出现在明确的弃用/迁移说明里，不能出现在scene unlock、choice domain或运行时输入。
2. 活跃场景不得再出现“人、展品、服务器三选二”、C01E01旧六回合保护战，或C01E02右臂已离体/已成桥。
3. S01失败只返回重试且零状态提交；成功只存在一个原子持久化事务。
4. S02读取29人全在前厅，不得再次生成或救出维修员。
5. L1远星副柜的所有活跃地点/锚点均指向旧影像厅出口，只读L3离线缓存。
6. 白函仍保持S02远程非实体、S03完整具身首战；索引仍保持C11前无连续第一人称。
7. 重新运行V35.8生成器、strict semantic validation、Canon smoke test和定向`rg`，并由本席复验上述语义而非只看脚本绿灯。

**最终裁定：`PATCH`。本话Story Core可保留；最终Canon放行暂缓。**
