# D07 全剧机制生命周期纸面审计 v0.1（已被v0.2取代）

> Status: `superseded_audit_snapshot / see_d07-series-lifecycle-paper-audit-v0.2 / no_longer_current_machine_interpretation`
>
> Current audit: [D07全剧机制生命周期规范化审计v0.2](d07-series-lifecycle-paper-audit-v0.2.md)。本页只保留最初单表审计过程；其中“五章复合风险”等数量已被规范化碎片账重新推导，不再作为当前结论。
>
> Scope: 只审 [22章机制生命周期账](../data/series-mechanic-lifecycle-ledger.tsv) 是否把教学、独立使用、第二数据实例、延迟掌握、反制、退役/合并和缺席回退写成可检查字段。
>
> Authority boundary: 本件读取 [逐章机制预测](../data/series-mechanic-unlock-spine.tsv)、[系统节点合同](../data/system-node-contracts.tsv) 与 [原型登记](../data/prototype-test-registry.tsv)，不修改 Canon、L3、Reader、Runtime、Demo、正式资产或任何章节验收状态。

## 1. 本轮实际补了什么

旧的22章路线每章只有一个 `one_new_dimension` 预测，第二数据实例、玩家掌握、反制窗口和退役/合并散落在自然语言里，无法逐机制追责。本轮新增一张22行账，每章一行，并固定以下机器字段：

- `mechanic_id / system_owner`：机制主键与唯一主系统；
- `introduction_window / guided_use / first_independent_use`：安全看见、单变量练习和第一次无提示使用；
- `second_data_only_instance / second_instance_invariants`：第二实例在哪里发生，以及哪些输入、规则核、UI、状态域和存档边界必须冻结；
- `mastery_test / counterplay_window`：延迟掌握和公平反制；
- `retire_or_merge / return_if_absent`：新片段怎样退役/合并，角色、成员或情境缺席时怎样回退；
- `prototype_evidence / status / rationale`：现有证据、未决状态和为什么不能称闭环；
- `declared_new_dimension_count / candidate_fragment_count / budget_assessment / risk_codes`：逐章新维度预算和机器可筛选风险。

第二数据实例不是“同一教程再播一次”。它必须冻结顶层输入、Resolver、UI shell、持久状态域、结算页和存档schema，只允许替换实体、地点、目标、来源、时窗或事件卡等内容数据。违反任一不变量，就要登记为新机制片段并重新过预算，而不是把开发债藏在“复用”里。

## 2. 状态语义

本账只允许三种状态，均不等于完成：

| status | 含义 | 不能推论 |
| --- | --- | --- |
| `proposed` | 生命周期假说已绑定具体章窗、第二实例不变量和现有待测原型行，可继续写中性纸面 Fixture | 不表示规则成立、有人玩过、可迁入L3 |
| `open` | 章窗可以讨论，但缺专用原型、对象级数据实例、延迟掌握或退役证据之一 | 不表示“以后自然会解决” |
| `blocked` | 当前有明确上游/产品范围门，或现有22章结构根本没有第二阶段，不能靠本账自行闭合 | 不授权越过用户裁决、章节链或Build门 |

`prototype_evidence` 中的 `pending:` 只表示 D10 已有待测登记；`generic_only:` 只表示通用技术核可能被复用；`OPEN:` 表示专用原型尚未登记。三者都不是 M5/M6 证据。

## 3. 当前机器结果

| 检查 | 结果 | 解释 |
| --- | ---: | --- |
| 章覆盖 | 22/22 | C01–C22各一行，机制ID与逐章预测前缀一一对应 |
| `status=proposed` | 1 | 只有C01已有足够具体的现行原型登记可继续纸面实现；仍有复合维度风险 |
| `status=open` | 18 | 缺专用原型、第二实例或掌握证据，且未来章仍只是Candidate章窗 |
| `status=blocked` | 3 | C04、C05受当前上游门限制；C22在现有路线内没有后续第二阶段 |
| 名义单维度 | 22/22 | 逐章表都声明1个新维度；这只是声明值 |
| 复合碎片风险 | 5/22 | C01、C03、C05、C11、C21的候选描述各含2个可独立形成输入/教学的片段，超过“每章1维度”预算，必须拆测或合并 |
| 名义在预算内但未证明 | 15/22 | 只有纸面字段，尚无对象级命令/UI/状态域差分统计 |
| 无真人证据 | 22/22 | 每行都有 `RISK_NO_HUMAN_EVIDENCE`；没有M5/M6或用户裁决 |

因此，本账把“组合爆炸已解决”改成了可定位的未决问题，但没有解决它。当前最重要的五条新维度预算风险是：

1. C01把基础身体战术与跨尺度连续Operation并在同一首次学习中；
2. C03把地图身体与工程工作单并在同一维度名下；
3. C05把实时占用与逐路退出同时作为新判断；
4. C11把战略编成与跨战区状态边同时引入；
5. C21把物理载荷诊断与政治停机/物理退出的治理区分同时教学。

这五行进入任何GD3前，必须选择其一：把第二片段降为既有系统的数据表现；拆到另一章；或用同一输入/状态机的中性 Fixture 证明二者确实是一个决策维度。不能只改名为一个复合名词。

## 4. 前三章与后续演进结论

### C01–C03

- C01已有 `D04-P1-*` 和 `PC01-E02` 待测登记，可继续把身体底盘做成对象级中性 Fixture；但跨尺度Operation应暂时视为第二碎片，不和基础时制一起宣称通过。
- C02的非致死与功能损伤还没有专用Resolver/Fixture。现有章节原型名只能说明需要测试，不能证明“赛事规则”和“救援功能损伤”共用同一核。
- C03可把E01工作单与E04无敌军校准当成候选第二实例，但“地图身体”和“工程工作单”是否共享一个输入/状态机仍未证明；C04延迟掌握又受当前上游门限制。

因此前三章不是“三个玩法已经设计完”，而是：C01有较具体的基础Fixture，C02/C03仍缺各自的对象级规则核和第二实例证据。

### C04–C22

- C04/C05不能借生命周期表越过当前章链、地点/战斗语法重设计、用户裁决或新L4门；两行明确为 `blocked`。
- C06–C21的章窗只使用现有Candidate机制ID与系统合同，没有预写未来人物事件、胜负或资产。它们的 `open` 说明仍可继续做匿名中性纸模，不说明章节可推进。
- C22在现有C01–C22结构内没有1–3章后的延迟掌握窗口，也没有跨阶段第二数据实例。除非用户以后批准“提前安全预显影”或独立postgame测试范围，否则该机制生命周期天然不能闭合。

## 5. 退役/合并纪律

`retire_or_merge` 不是删除玩家已经学会的基础动词，而是主动删除系统碎片：

- 教程页退为可选复盘；
- 赛事、三线、四线、分舰、终局等一次性壳合并回 `SYS-TACT / SYS-C2 / SYS-ROSTER / SYS-BODY / SYS-WORLD / SYS-HUB` 的共享schema；
- 情境缺席时折叠UI，不生成空面板、匿名替身、补偿buff或另一套小游戏；
- 后续机制只能扩内容数据、合法动作映射和公平反制，不能偷偷新增存档域或结算页。

任何一行如果第二实例必须新增顶层输入、持久状态域或UI shell，就把 `status` 退回 `open`，新增风险码，并回到逐章新维度预算重审。

## 6. 本轮局部检查

本轮只跑静态shape与交叉引用检查，没有Build、搜索、纸模求解、真人测试或用户验收：

```text
TSV width: 23 columns x 22 data rows, all rows equal width
chapter coverage: C01..C22 exactly once
mechanic mapping: 22 lifecycle mechanic_id values equal 22 unlock-spine prefixes
system owners: all resolve to the 12 Candidate system-node IDs
status vocabulary: proposed/open/blocked only
prototype refs: every pending:/generic_only: ID resolves to prototype-test-registry.tsv
budget guard: all 5 rows with candidate_fragment_count=2 carry risk_compound_2_gt_1
closure guard: no row uses complete/passed/validated/accepted status
```

这些检查只证明账的结构可审计，不证明任何玩法有趣、可实现、可学习或适合本项目。

## 7. 下一证据顺序

1. 先把C01复合维度拆成“基础身体战术”与“连续Operation承载”两个可分别失败的纸面检查，不扩大现有Build授权；
2. 为C02功能损伤/非致死、C03地图身体/工作单各补一个中性对象级Fixture和第二数据实例；
3. C04只在地点/战斗语法与用户门解决后，把D04-P2绑定到真正的章级对象；
4. 后续机制先补中性原型登记，再以同一输入/UI/状态域做第二数据实例，最后才安排真人掌握测试；
5. 用户未裁决C22第二阶段来源前，终章生命周期保持 `blocked`。

在上述证据完成前，D07仍是Candidate路线与风险账，不是全剧玩法封板，也不是制作排期的完成依据。
