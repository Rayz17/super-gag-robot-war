# C01E02 Canon / 宏观谜团 / 物理连续性定向复核 r3

> 席位：原 Canon / Macro / Physical 独立审稿席  
> 复核对象：当前 C01E02 正式稿、Runtime/Graybox、迁移单、C01 地图、S03/S04 PB、state propagation、Canon、design graph 与 r2 确定性纸演  
> 裁决：`PATCH`

## 1. 裁决摘要

C01E02 的**可执行物理链与下游状态链已经闭合**：原始人口严格为 29 人，R4 后 29 人在楼外；R5 馆内严格为纪存、唐胶、兜灯与两名新到消防接驳员，共 5 人。供水、风道、档案冷却、消防架桥机腿伤、馆守Z连接态、勇拳零动作、白函远程态及“完整移动脊柱未暴露”均进入唯一原子快照，并被 S03/S04 与 state propagation 消费而不重生。

但本席不能给 `PASS`：当前 C01 地图仍错误合并四令主体；Canon 仍有当前首现字段和馆守Z废弃 alias 泄入现行场景；design graph 仍有若干标为 current/canonical 的旧合并版入口。它们都是可被当前查询直接命中的活跃冲突，不是与 E02 无关的全库悬空边。

## 2. r2 迁移闭合复核

| 项 | r3 结果 | 当前证据 |
|---|---|---|
| 2.1 四令主体与七海权限分域 | **未闭合** | Episode 已把安全端锁门、代哥端切胸灯、平台冻钥匙、军方停泵分开，且七海只撤本人东侧高压令；但 `C01-逐章重构地图-v1.md:68` 仍写成“代哥锁门、切胸灯”，吞掉安全端。 |
| 2.2 29 人 / 5 人及唯一快照 | **闭合** | `C01E02-四张封存令-v1.md:207-239,307-316,384-386`；`13-runtime-graybox-paper-run-r2.md:23-34,57-74`；`C01E02-graybox-constants-v1.tsv:37`。 |
| 2.3 当前 first/formal 查询 | **部分闭合** | 纪存、兜灯、唐胶及代哥已迁离旧 `C01E02-BATTLE-START` / `C01E02-MAP-STORY`；但 `entities.tsv:32` 的豪司 formal/battle 仍指旧 `C01E03-04`，与当前 `scenes.tsv:100` 的 `V355-C01E03` 冲突。 |
| 2.4 馆守Z alias 与 E02 零动作 | **状态闭合，索引未全闭合** | `entities.tsv:45,474` 已把 `MECHA_GUARDIAN_Z` 降为 `V353U001` alias；Episode `:163,251,292,396,428` 和迁移单 `:36,40-41,51` 锁定馆守Z被动、勇拳零动作、白函无身体。但 `scenes.tsv:101` 仍把废弃 alias 放入当前 E04 optional_entities。 |
| 2.5 旧三话/六回合降级与 snapshot 图边 | **部分闭合** | 旧六回合场景已在 `scenes.tsv:19-21` 降为 historical，旧合并/三话节点已在 `graph_nodes.tsv:157,162-163` 降级；三条新下游边 `graph_edges.tsv:1877-1879` 完整存在。可是 `graph_nodes.tsv:160`、`canonical_terms.tsv:19,23,30`、`consistency_watchlist.tsv:28,31` 仍把旧合并版口径标成 current/canonical。 |

## 3. 物理与宏观逐项结论

### 3.1 人员守恒：PASS

- `C01E02-四张封存令-v1.md:157,193-215` 没有重复生成维修员；原始 29 人由既有四组离楼，两名接驳员明确在 29 人离楼后进入且不属于最初 32 人。
- `:239,307-314` 把楼外 `29/29` 与馆内 5 人分成两个不同回执；R5 失败只回本地检查点，29 人不回刷。
- 独立纸演 `13-runtime-graybox-paper-run-r2.md:25-34,59-66` 重放出 `A11+B10+C3+D5=29`、F2 两条入场路径和五人退路；跌跌是设备，不是第六人。
- S03 唯一入口 `PB-V357-C01-S03.md:14,28,32` 与 S04 `PB-V357-C01-S04.md:14,22,27,34` 均保持 29 人楼外、已知五人及必要设备，不把人员转成载荷。

### 3.2 损伤预算与设施继承：PASS

- Episode `:243,307,312-315,384` 固定唯一代表路线伤痕为供水总管热损；商业后勤风道局部烧损、档案主库紧急冷却为伴随状态；消防架桥机为 SEG3 反折与左前腿过载。
- 迁移单 `:27,36-41,49-53,74,78-79` 与 S03 `:14` 对上述物理状态逐项同值，没有恢复双设施分支或增加第二代表伤痕。
- `v35_5_c01_c03_state_propagation_v35_5.tsv:3-5` 让 E03 读取 E02 快照，E04 再叠 E03 增量；E04 只能在人员安全后从生活维持设备、实体独有馆藏、档案服务器三类中选二，`people_cargo=FORBIDDEN`。

### 3.3 机体与敌方生命周期：PASS

- 勇拳：Episode `:219-231,293,308,395,428` 为运输架自动请求止于机外许可继电，本体零位移、豪司缺席；S03 `:14,24,32` 才首次越权驾驶并产生肩背承重。
- 馆守Z：Episode `:103,163,251,292,396,428` 只有温感与低压继电，半跪、主动力/胸灯关闭、右臂连接且零身体动作；S03 `:14,23-28` 才首控、抬肩、飞拳与主动切臂。
- 白函：Episode `:247-255,300,386,398,427` 在 E02 只有远程语音、投影、改报和预量，无格、HP、受击或完整身体；S03 `:14,22,25,32` 才具身为 Boss。
- 消防架桥机：Episode `:141-163,219-231,291,392` 给予完整固定 Rig 动作包并承担本话机体高潮，同时没有自由移动、HP、攻击、反击、首控或入队偷跑。

### 3.4 地图公开边界与下游消费：PASS

- Episode `:125-145,251` 只公开共同消防/撤离层；`完整移动脊柱`未被唤醒或公开。敌方收益仅是公共消防图、行动样本与中庭预量，不足以推出馆体全图。
- S03 `:14` 明写完整移动脊柱未暴露；S04 `:14` 先继承该状态，再由军方封锁和 E03 增量推进起航，不把 E02 的公开图倒推为完整脊柱曝光。
- Canon 当前行 `scenes.tsv:99-101` 已把 E02 远程态、E03 具身/首控/首次勇拳动作、E04 人员非载荷写成连续三话。
- 图谱三条必要边已闭合：`graph_edges.tsv:1877` 喂给 S03，`:1878` 喂给 S04，`:1879` 约束 state propagation。没有发现由本轮 E02 新增的下游悬空边。

## 4. 必须修复的活跃冲突

### PATCH-1：C01 地图四令主体仍错

**冲突：** `C01-逐章重构地图-v1.md:68` 写“代哥锁死半开防火门、切断馆守Z胸灯”，而 Episode `:81`、迁移单 `:24,36` 及 Canon `scenes.tsv:18,99` 要求锁门与切灯属于不同控制端。该句会让后续查询错误扩大代哥权限，也削弱七海“只能撤本人命令”的因果。

**最小修法：** 只把该句四令改为：`安全端锁死半开防火门，代哥端切断馆守Z胸灯，平台冻结旧路数字钥匙，军方把B1泵压到零位`；其余段落不动。

### PATCH-2：Canon 当前首现与 alias 尚有旧入口

**冲突 A：** `entities.tsv:32` 仍把豪司 `first_formal_appearance/first_battle_join` 指向旧 `C01E03-04`；当前正式下游是 `scenes.tsv:100` / `PB-V357-C01-S03.md:24,32` 的 `V355-C01E03`。旧三话链 `scenes.tsv:22-29` 也仍使用普通 `cutscene/battle/event` 类型，未像 `:19-21` 一样显式 historical。

**最小修法 A：** 把 CH036 的 formal/battle 改为 `V355-C01E03`；将 `scenes.tsv:22-29` 整链降为 historical source/runtime reference，并在 notes 指向 `V355-C01E03/E04`。若保留 CH037 在 E03 仅作远程支援预告，则至少把 `entities.tsv:33` 的 first_foreshadow 改为 `V355-C01E03`，formal/battle 可继续留 C08，但 policy 必须写清 E03 非独立入队。

**冲突 B：** `entities.tsv:45` 已正确声明 `MECHA_GUARDIAN_Z` 是 `V353U001` 的 deprecated alias，但当前 `scenes.tsv:101` 同时把 `V353U001` 列为 required、旧 alias 列为 optional，查询仍可能把同一机体计成两项。

**最小修法 B：** 从 `scenes.tsv:101` 的 optional_entities 删除 `MECHA_GUARDIAN_Z`，只保留 `V353U001`。

### PATCH-3：旧合并版图谱仍有 current/canonical 命中

**冲突：** 虽然 `graph_nodes.tsv:157,162-163`、`scenes.tsv:19-21`、`consistency_watchlist.tsv:17,30,53` 已完成历史降级，但以下条目仍会给出旧答案：

- `graph_nodes.tsv:160`：旧“第一话法务封存执行单位”仍为 `canonical`。
- `canonical_terms.tsv:19`：`TERM_EP01` 仍把当前第一话定义为合并旧 1-1/1-2 的六回合保护战。
- `canonical_terms.tsv:23`：仍把封存无人机、0号开启臂、采样贴片整体当作当前第一话单位。
- `canonical_terms.tsv:30`：仍把馆守Z旧保护战末接入与“新1-2”半启动写成当前时序。
- `consistency_watchlist.tsv:28,31`：仍以 `fixed_watch` 声称合并版 v0.3 是当前前后半结构和推荐稿。

**最小修法：** 将 node 160、TERM_EP01、TERM_LEGAL_EXECUTION_UNITS 及 CW016/CW024 明确降为 `historical_superseded_by_v359_story_first`；TERM_GUANSHOU_Z 改写为“E01低热可见、E02被动零动作且右臂连接、E03首控/首身体动作/断臂”，source_refs 指向当前 V35.9 Episode/迁移。旧素材可继续保留，不删除。

## 5. 复验门槛

完成上述最小迁移后，只需定向复验：

1. 当前查询不再把四令锁门与切灯都归给代哥。
2. 豪司 first formal/battle 返回 `V355-C01E03`；馆守Z当前场景只返回 `V353U001`，不重复计 alias。
3. 默认图谱/术语查询不再返回旧三话或六回合保护战；historical 显式查询仍可追溯旧源。
4. `graph_edges.tsv:1877-1879` 保持不变；S03/S04/state propagation 继续只消费 `C01E02_PHYSICAL_SNAPSHOT`，29 人不回刷、5 人不膨胀、人员不入载荷。

在这些活跃入口清理前，本席结论维持 `PATCH`；E02 正文、Runtime/Graybox 与 S03/S04 物理状态本身无需返工。
