# D02–D03 核心循环与开篇状态内部纸面走查 v0.1

> Status: `internal_static_design_evidence / route_continuity_checked / payload_static_contract_checked / zero_target_players / no_prototype_authorization / no_gameplay_acceptance`
>
> Date: `2026-08-10`
>
> Scope: D02 统一核心循环、D03 系统/模式/状态合同、D06 C01–C03 Accepted Story 绑定蓝图。

## 1. 结论

三条 Accepted Opening 代表性会话、一条中性 Hub-only 会话和 C01→C03 的十二段状态事务/桥接守卫现在可以在两个互不替代的纸面检查层上追踪：

- **路线连续：** 每一步的 `from_mode → to_mode` 都能命中合法 transition，并与同一会话的前后步骤连续；
- **payload 静态闭合：** 35步中每条 transition 的189项 `required_inputs` 都声明来源，106项 `committed_outputs` 都声明稳定引用、边界、主要消费者，13个结算目的地都声明模式回执；owner、可见性与存档边界另行受检。

在这两个检查层内，四条会话分别覆盖：

1. C01E01–E02：短探索可以回到剧情，再进入非歼灭战术，并停在不冒充 Mission Clear 的 Encounter 检查点；
2. C02E03：发生在馆内的 Story 调查、主体同意、两场半决赛和 Episode 停点可以分开提交，且不会提前结算赛事；
3. C03E04：无敌军工程实证、馆内 Story 回应、双时间信号、Operation/Chapter 两级结算和世界路线可以连续成立；
4. 中性 Hub fixture：真正的 `HUB_CYCLE` 能以三项高价值行动、机会成本和离馆承诺闭合，而不冒充前三章里只发生在馆内的固定剧情场面。

本次走查不证明这些玩法可运行、好玩、轻松、可理解或有多解。目标玩家数为 0，Build 数为 0，用户玩法批准为 0。路线连续只证明图上有合法相邻边；payload 静态闭合只证明字段存在可追踪的声明来源与去向，不验证运行时值、业务语义、原子提交或消费成功。两者都不能升级成 Build/Runtime 证据。

逐步路线证据见 [core-loop-paper-walkthrough-traces.tsv](../data/core-loop-paper-walkthrough-traces.tsv)，逐步 payload 合同见 [core-loop-payload-bindings.tsv](../data/core-loop-payload-bindings.tsv)，跨章事务见 [opening-state-transaction-paper-trace.tsv](../data/opening-state-transaction-paper-trace.tsv)。

## 2. 走查前真实断点

原 `mode-transition-contracts.tsv` 只有 12 条转换，存在以下不可闭合状态：

- `operation_settlement` 没有入边；
- `investigation_or_engineering`、`next_encounter`、`chapter_settlement` 没有合法出边；
- 探索若不进战斗，没有“调查即解决”的结算路；
- 纯故事任务、Hub-only 行动和世界图交付/会谈没有合法写回；
- Archive 只有出边、没有入口，也没有统一结算；
- C02E04/E05 用拼接 Operation ID 掩盖了赛事、事故和交割三个不同结算边界；
- C03E03 结束 `OP_C03_CITY_WEIGHT` 后未显式写 Operation Settlement。

因此旧表虽然有统一循环图，却不能从实际 Episode 模式序列证明闭环。

## 3. 本轮修复

### 3.1 系统边

补入此前图意存在、合同缺失的主路径与 owner 回写：

- `SYS-NARR → SYS-EXPL`：当前地点直接进入有边界探索/实证；
- `SYS-HUB → SYS-EXPL`：Hub 内档案调查或实体试验；
- `SYS-WORLD → SYS-NARR`：交付、会谈或纯故事到达；
- `SYS-NARR → SYS-SETTLE`：纯故事/无战斗 Operation 也必须交统一事务；
- `SYS-ARCH → SYS-SETTLE`：收藏、展签和揭示变化不能绕过结算。
- `SYS-SETTLE → SYS-ROSTER / SYS-C2 / SYS-EXPL`：成员/部署、接触/权限、证据/假说各自由真正 owner prepare；
- 原有 `SETTLE → BODY/WORLD/REL/NARR` payload 补齐 Equipment/Custody、Location、Consent、Entity 与 Knowledge 变化。

系统图与机器边表同步为 40 条有向连接；这仍是 Candidate 数据合同，不是 Runtime 实现。

### 3.2 模式转换

模式合同扩为 37 条，新增或补齐：

- Story/Hub/World 到探索、实证、Archive 与纯故事入口；
- Exploration/Proof/Hub/Archive 到统一 Activity Settlement；
- Activity Settlement 到 Story、Hub、Tactical 或 Operation Settlement；
- Encounter Settlement 到下一 Encounter 或 Operation Settlement；
- 下一 Encounter 到 Story、Exploration 或 Tactical；
- Operation Settlement 到 Story、Hub、World 或 Chapter Settlement；
- Chapter Settlement 到下一 Story 或 World；
- Archive 只读取消与提交后返回分开。

任何需要修改长期状态的退出都必须持有 receipt；只读取消不得伪装提交。

### 3.3 Story-in-Hub 与 HUB_CYCLE 分离

新增 [episode-mode-token-contracts.tsv](../data/episode-mode-token-contracts.tsv)，把 Episode 流程 token 显式归一到 owner/mode/boundary：

- `STORY_IN_HUB_*` 仍是 Story，只表示场景发生在万机馆，不消耗2至5个经营行动格；
- 只有 `HUB_CYCLE_*` 才能进入完整 Hub 系统；
- `SETPIECE_*` 只能消费已经成立的状态，不能在动画中偷偷补业务结果；
- `*_CHECKPOINT`、`*_MISSION_CLEAR`、`OPERATION_SETTLEMENT`、`CHAPTER_SETTLEMENT` 是不同边界；
- `TACTICAL_*`、`AUX_*`、Story 内联同意/关系节点分别归到对应 owner，不再靠前缀猜测。

因此 C02E03 的 `STORY_IN_HUB_NIGHT` 和 C03E04 的 `STORY_IN_HUB_RELATIONSHIP` 目前都不是经营循环。若未来要升级成真正 Hub Cycle，必须另走 Candidate 设计与用户玩法门，而不是仅改 token 名称。

### 3.4 Membership、Knowledge 与多 owner 原子提交

状态合同从24项补为26项：

- `ST_MEMBERSHIP` 保存跨章随舰、离舰、试用、访客、联络和托管；`ST_ROSTER` 只保存一次 Operation 的岗位/部署；
- `ST_KNOWLEDGE` 保存逐观察者的已知、未知、来源、置信度和揭示门，避免“玩家镜头看见=全队知道”。

新增 [settlement-owner-prepare-commit-contracts.tsv](../data/settlement-owner-prepare-commit-contracts.tsv)：十个可变状态 owner group 必须先对同一 proposal hash 生成 prepared receipt；任一拒绝、超时或版本冲突，整组0写入；全部 prepared 后才由 `SYS-SETTLE` 一次提交唯一 accepted receipt。十组覆盖24个可变持久状态；`ST_IDENTITY` 仅允许批准的设计迁移，`ST_UI_PROJECTION` 仅由 accepted receipt 派生，二者显式排除在玩法提交之外。它修复的是纸面原子性定义，尚无 Runtime 实现。

### 3.5 Episode Operation 边界

`c01-c03-episode-play-contracts.tsv` 的单值 `operation_id` 改成 `operation_sequence`：

- C02E04：`OP_C02_TOURNAMENT > OP_C02_STAGE_ACCIDENT`；
- C02E05：`OP_C02_STAGE_ACCIDENT > OP_C02_DEPARTURE`；
- C01E04、C02E04、C02E05、C03E03、C03E04 均补显式 `OPERATION_SETTLEMENT`；
- Tournament Clear、Accident Checkpoint、Accident Clear、Departure Settlement 不再混成一个完成标记。

### 3.6 路线连续与 payload 静态闭合分开

原有路线检查只回答“35步是否逐步命中合法 transition、相邻 mode 是否接得上”，不能据此声称 transition 所需字段已经有生产者、提交结果已经有消费者。为避免把拓扑可达误写成数据闭合，新增 [core-loop-payload-bindings.tsv](../data/core-loop-payload-bindings.tsv) 和专用只读 checker [check_d02_d03_core_loop_payload_bindings.py](../scripts/check_d02_d03_core_loop_payload_bindings.py)：

- 每一步逐项绑定 transition 的 `required_inputs`，来源只允许为 session seed、owner state read、同会话较早 committed output、较早 settlement receipt 或较早 mode result；
- 每一步逐项绑定 `committed_outputs`，并声明稳定字段引用、commit boundary、主要下一消费者；
- owner、visibility、stable-save、下一步、结算 receipt 与即时前序锚点分别受检；
- `--self-test` 对缺输入、错 owner、错 visibility、缺输出、缺消费者、错边界、错下一步、错存档、占位词与坏 provenance 引用做内存故障注入。

这仍是静态合同：checker 不执行 mode、不生成 receipt、不读取玩家输入，也不证明字段值在 Runtime 中被正确生产、提交或消费。

## 4. 四条会话为什么有代表性

| 会话 | 候选时长 | 主要模式 | 证明的结构问题 | 不证明什么 |
| --- | ---: | --- | --- | --- |
| PW-A C01E01–E02 | 42–65 分钟 | Story→Explore→Story→Tactical→Encounter Settlement | 开篇轻探索不是战斗门票；E02可稳定停靠但不能假称清章 | C01战术好玩、地图成立、Demo可迁移 |
| PW-B C02E03 | 62–89 分钟 | Story-in-Hub→Proof→Story→两场Tactical | 证据、主体同意、两个Encounter和未完Tournament分别记账 | 半决赛有两解、比赛规则公平、角色UI可懂 |
| PW-C C03E04 | 47–74 分钟 | Story→Proof→Story Activity→Operation/Chapter Settlement→World | 无敌军玩法也能完整闭环；馆内关系场面与双信不会吞掉章结算 | 工程玩法轻松有趣、C-1空间/惯性真实可玩 |
| PW-D 中性Hub | 43–66 分钟 | Story→HUB_CYCLE→Archive/Proof/Relationship→World | 真正Hub有三项高价值行动、机会成本、可见变化和离馆承诺 | Hub节奏有趣、事件池成立、前三章必须采用该模式 |

候选时长只是把 D02 的会话承诺落到步骤预算；PW-A 下界和 PW-D 中性fixture略低于45分钟，说明“每次都要45分钟”本身也应保留弹性。没有真人计时，不进入 D11 实测预算。

## 5. 跨章状态结论

十二段事务/桥接守卫揭示三个必须保留的分离：

1. **C01→C02：** 万机馆低速、馆守Z独臂、转子过热、勇拳离队和木桶街路线不能在新章默认刷新；
2. **C02内部：** 3:2赛事、事故处理、转子/推进模块/随舰交割是三个不同的 Operation/Chapter 结果；
3. **C02→C03→C04：** 新旧转子身份、长期 Membership、本次 Operation Roster、C-1泊位、货柜地面线、当前求援和27年前旧讯息必须分别保存和消费。

当前 `ST_RESULT`/`ST_OPERATION` 等合同能表达这些差异；现有 Runtime 尚未实现相应 v2 schema、owner 校验、跨章迁移与确定性重放。

## 6. 仍然阻塞的工作

- C01/C03 Accepted Story 当前字节与登记值一致，但没有可达 Git commit 或不可变归档；正式门实例不能把“当前无净漂移”写成“历史快照已保存”；
- C01万机馆/南广场、C02资料区/货运环、C03 C-1/工务城等 GD2 未封存；
- P1、P-EX1/2/3、P-HUB1、P-SET1 均未获授权、无 Build、无 M5/M6；中性Hub纸面fixture不授权把C01-C03馆内Story场面升级为经营循环；
- C02 Candidate gameflow/preplan 仍须向 Accepted Reader 重基；
- D09 只有门定义，没有可执行实例和故障注入证据；
- C04 天空铸环 Master Pack 与 E03 上游门仍未完成。

## 7. 本轮静态校验

以下结果可由包根目录的中央静态检查与 D02–D03 payload 专用检查分别只读重放：

- `scripts/check_candidate_contracts.py`已重放通过包内TSV列宽与Markdown本地链接解析；文件和链接计数以该checker当次输出为准，不在本纸面走查回执中固化易漂移数字；
- 12个系统、26个状态、40条边及10个可变状态owner组引用闭合；40条Mermaid连接与40条边合同双向一致；
- 24个可变持久状态各落入且只落入一个owner组；`ST_IDENTITY`与`ST_UI_PROJECTION`按设计显式排除；
- 37条模式转换覆盖12种mode，均有入边和出边；4条会话35步的from/to与transition逐步连续；
- `python3 -B scripts/check_d02_d03_core_loop_payload_bindings.py`独立通过：4条会话、35步、189项required input、106项committed output、13个结算receipt的owner/visibility/save/provenance/consumer静态合同闭合；
- 同一checker的`--self-test`拒绝381/381个内存故障注入；该数字只证明当前故障类别能触发拒绝，不是Runtime覆盖率；
- C01–C03共13话的91种Episode token均唯一命中最高优先级规则；所有Mission Clear后均紧接Operation Settlement；
- 3个Accepted Story binding、13个Episode组件、3个章Reader和3个回执当前SHA256一致；仅C02存在可达Git快照，C01/C03仍保留归档风险；
- 旧29包/77条Roster交叉账与15个非旧库key缺口账可由生成器重建并通过`--check`。

这些是结构与引用检查，不是玩法运行、确定性重放、真人理解或用户批准。

## 8. 合法声明

本证据只允许声明：

> D02 的三条 Accepted Opening 代表性循环与一条中性 Hub 循环，在 Candidate 层分别通过了路线连续检查和 payload 静态来源/去向合同检查；D03 的 C01–C03 状态事务可以在纸面上追踪到声明的稳定回执与下一消费者。

不得声明：

- 核心循环已可玩；
- 战棋、探索、Hub或结算已经成立；
- 目标玩家理解或喜欢；
- C01–C03 已具备地图、资产或连续 Previs；
- 用户已批准 DEC-01/02/03/11 或任何后续原型/制作。
