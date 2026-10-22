# C01E03 Canon / 宏观谜团 / 物理连续性最终独立复验 r3

> Verdict: **PATCH**
>
> Scope: `C01E03`迁移后最终复验；未修改Episode、共享Canon或生成数据。

## Findings

### CMR3-01 / HIGH：E04正文仍重开RT035已经结清的五人撤离

**证据**

- `C01E03-runtime-contract-v1.tsv:36-37`在`RT035/RT036`提交并只读断言`BRIDGE_EVAC_HUMANS=5`、`FIVE_INSIDE_HUMANS=SAFE`、`E03_FIRE_HANDOFF_CARGO=2_SAFE`；Episode `结算状态:399-406`同值。
- `PB-V357-C01-S04.md:14`正确声明E04只读RT035精确27键，五人、豪司和两件消防货物均已安全。
- 但同文件`因果场面链:22`又写五人和设备“正在完成断臂退路交接”，`战斗与玩法:34`再把“五名已知馆内人员与必要设备完成交接”列为E04胜利条件、把“五人退路未闭合”列为失败压力。这会把E03已经原子结清的人口/货物重新放回E04可变状态，正是摘要拼接式继承。

**最小修复**

- 文件：`docs/superpowers/specs/剧情梗概/V35.9/chapters/C01/PB-V357-C01-S04.md`。
- 字段/段落：`## 3`第1拍改为“五人、豪司、两件消防货物均已在安全区”的只读前态；`## 4`从胜利条件和失败压力中删除五人/两货交接及退路变量。E04胜负只能作用于馆体起航、城市避难区、结构/过热和三类非人员载荷。

### CMR3-02 / HIGH：V31虽已历史化，默认Canon查询仍会把旧链与当前Episode一起返回

**证据**

- 迁移单`§2:26`、`§7:107`及`consistency_watchlist.tsv:237 / CW234`都要求旧V31链只能显式历史查询，默认查询只返回当前Episode。
- 数据标签本身正确：`entities.tsv:329-336`均为`historical_runtime_reference`；`scenes.tsv:32`为`historical_story_source / HISTORICAL_SOURCE_ONLY`；`graph_nodes.tsv:553-559`及`graph_edges.tsv:1218-1229`均使用历史节点/历史关系。
- 实际执行`./scripts/canon-query.sh scene V355-C01E03`返回10条scene：仅1条是`V355-C01E03`，另有8条`historical_*`旧scene。原因可定位到`scripts/canon_query.py:40-42,262-280`：查询对整行做无条件子串匹配，没有current/history过滤；历史行notes中提到当前ID即会被默认命中。

**最小修复**

- 文件：`scripts/canon_query.py`。
- 字段/函数：为默认`all/entity/scene/index/graph`路径增加历史状态过滤，并提供显式`history`查询模式；至少识别entity `status=historical_*`、scene `kind=historical_*`/`unlocks=HISTORICAL_*`、registry `layer/doc_type=historical_*`、graph node `source_layer/status=historical_*`及edge `relation=historical_*`。
- 增加回归断言：默认查询`scene V355-C01E03`只能返回当前scene；显式历史查询仍能取回`V31-C01E03-BATTLE`、审批锤与责任签名矩阵。

### CMR3-03 / MEDIUM：V35.8把三台回归支援单位重新登记为S03首显

**证据**

- `v35_8_lifecycle_event_review_v35_8.tsv:18-20 / V358LIFE0017..0019`把消防架桥机、跌跌、机器犬的`from_state`写成`not_visible`、`preview_count_mode`写成`count_first_visible_only`，并称“本槽首次实体显现”。
- 同表`2-5,11-13`已记录跌跌/机器犬在S01首显并于S02回归，`11`已记录消防架桥机在S02完整首显；同批生成的`slot_unit_manifest:16-18`与`slot_asset_manifest:16-18`也明确三者在S03是`return/reuse/repeat_support_not_new_first_appearance`。
- 生成源`scripts/build_v35_8_slot_loadout.py:1453-1455`只覆盖了event type，`SLOT_LIFECYCLE_REVIEW_OVERRIDES`在E03三核心生命周期之后缺少这三条回归前态，strict因只验闭合/validated状态而未捕获自相矛盾。

**最小修复**

- 文件：`scripts/build_v35_8_slot_loadout.py`的`SLOT_LIFECYCLE_REVIEW_OVERRIDES`。
- 字段：为`(S03,V353U034/038/040)`补`from_state`、`preview_count_mode`、`gameplay_effect`回归语义：分别承接S02消防机完整支援态、跌跌`small_unit_player_control`、机器犬`one_context_then_auto`；三者均不得使用`not_visible/count_first_visible_only/首次实体显现`。
- 重生成`v35_8_lifecycle_event_review_v35_8.tsv`，并给strict增加“return事件不得从not_visible开始或计first_visible”的跨槽断言。

## 已通过项

- **RT035**：脚本化集合比对确认27项、27个唯一键；Episode、迁移单、V35.5 E03输出/E04输入、slot commit及Canon scene unlocks同序、无缺、无增、值一致。
- **人口与E02伤痕**：继承5人全在L2；豪司由西门后入使峰值6；桥上恒5；29人和消防机操作员不回刷。供水、商业风道、档案冷却及消防机左前腿伤完整继承。
- **核心生命周期**：馆守Z E03受限首控并永久单臂；勇拳由豪司本人临控、六锚前企业回收及数据剥离；白函E02远程无身体、E03首次具身首战并携双伤撤离。金章仅UI/短语音，社勇王真机未前移。
- **右臂与物理锚**：五态严格前向；L2唇口至L1承台为4.2m水平净距/0.9m高差。`5.0m+1.4m`复合件扣除约4.30m斜跨及两端各0.8m搭接后仍余约0.50m，双索、副筋、滑架共同承力，几何成立。
- **谜团边界**：纪存记忆只给隐藏位置且保持低置信/来源未知；B1只暴露六锚与物理锁，不解释旧图、0号或完整馆体；白函只取得一个局部样本。`v35_7_mystery_slot_binding:5`与`v35_9_c11_s04_index_birth_state_machine:2-7`确认C11前无索引连续人格，E03未越界。
- **迁移判断**：`C01MIG013-015 / V358MIG051-053`是本话所需Canon迁移，核心命题已进入V35.5、V35.8、Canon与图谱；上述三项是迁移后的下游/查询实现缺口，不要求新增故事Canon命题。

## 验证记录

- `scripts/canon-smoke-test.sh`：PASS
- `scripts/canon-check-godot.sh --strict`：PASS
- `python3 scripts/check_v35_8_slot_loadout.py`：PASS（未覆盖CMR3-03跨槽语义）
- `python3 scripts/check_c01e03_runtime_graybox.py`：PASS（47状态、人口、五态、梁几何、20/21/23、三回滚、27键与资产范围全部通过）

**最终判定：PATCH。** 修复CMR3-01至03并重跑四项验证及两条新增回归查询后，才可将本席改判PASS。
