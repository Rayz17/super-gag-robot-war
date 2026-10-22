# D07 全剧机制生命周期规范化审计 v0.2

> Status: `candidate_normalized_paper_audit / lifecycle_not_closed / live_chain_unwired / zero_build / zero_human_evidence / no_canon_or_l3_migration`
>
> Supersedes: [v0.1单表审计](d07-series-lifecycle-paper-audit-v0.1.md)。v0.1保留为发现过程，不再代表当前D07机器口径。
>
> Authority boundary: 本审计及六张子账只服务D07复核、D09依赖规划与D10中性原型规划；不得进入Canon、L3、Reader、gameflow、Runtime、Demo或正式资产。

## 1. 修正后的结论

v0.1把“22章各有一个主机制行”误当成了完整生命周期视图。它能说明每个候选机制想在哪里首次出现，却不能回答：同一章同时活跃多少旧机制、UI会叠几层、机制休眠多久、第二实例是否真的只换数据、哪个系统协作、以及教程壳退休后保留什么。

v0.2不把这些问题写成已解决，而是把它们拆成可机器交叉检查的子账。当前真实结果是：

- 22个候选主机制仍为 `1 proposed / 18 open / 3 blocked`，没有任何一项完成；
- 12个系统都有生命周期身份，但 `SYS-NARR / SYS-EXPL / SYS-ARCH / SYS-PRESENT` 明确是横向服务，不伪造章级主机制；
- 22个第二实例全部没有可验证内容hash，18个明确受另一新机制污染或上游阻断；
- 66个阶段证据绑定覆盖“首次出现/第二实例/延迟掌握”，但全部只是registered pending、missing或blocked；
- 70行章×机制活动揭示C16有5个、C17有5个、C20有6个生命周期同时活跃，不能继续用“本章只新增一个机制”掩盖累积负荷；
- 六个中间复习点已排进Candidate活动账，但全部未进入实时章链，也没有Build/真人证据；
- 复合风险不再由checker写死为五章。规范化碎片账当前推导出七个风险：C01、C02、C03、C05、C06、C11、C21；
- D07检查器无法自动读取全部实时章链，22/22行均明确 `unwired_snapshot_only`。因此当前open/blocked是Candidate快照，不是动态章链结论。

## 2. 六张规范化子账

| 子账 | 解决的问题 | 当前证据边界 |
| --- | --- | --- |
| [生命周期治理账](../data/series-mechanic-lifecycle-governance.tsv) | primary/collaborating owner、state refs、来源、允许/禁止消费者、决策、章链连接、阻断、退役拆分 | 22/22均Candidate；章链未接线 |
| [12系统覆盖账](../data/series-system-lifecycle-coverage.tsv) | 12系统是否有主机制、协作机制或明确“非章级主机制”身份 | 覆盖完整不等于玩法成立 |
| [第二实例账](../data/series-mechanic-second-instance-ledger.tsv) | instance、fixture、ruleset、schema、hash、隔离和污染 | 22/22 hash unavailable；零验证 |
| [阶段证据账](../data/series-mechanic-stage-evidence.tsv) | intro / second / mastery各自由什么原型证明 | 66行均未达到M5/M6 |
| [机制碎片账](../data/series-mechanic-fragment-ledger.tsv) | 一个复合名词是否含可分别输入、分别教学的判断 | 当前推导7个复合风险，非固定名单 |
| [章×机制活动账](../data/series-mechanic-chapter-activity-ledger.tsv) | 每章活跃、复用、掌握、复习、组合与UI叠加 | 70行规划；六个复习点均未证实 |

旧的 [22行主生命周期账](../data/series-mechanic-lifecycle-ledger.tsv) 继续保存引入、引导、独立使用、反制和缺席回退等可读判断，但不再独自承担所有审计责任。

## 3. 所有者与12系统覆盖

v0.1只有一个 `system_owner`，会把跨系统机制强行归给一方。v0.2使用：

```text
primary_system_owner
+ collaborating_system_owners
+ state_refs
```

其中C15已从 `SYS-WORLD` 改为 `SYS-C2` 主责，因为四时间戳与置信投影的主状态是 `ST_CONTACT`；`SYS-WORLD`负责路线、等待和改道，`SYS-PRESENT`只投影时间与置信，不另建状态。

四个没有章级主机制的系统也不再消失：

- `SYS-NARR`：权威入口、故事事实与Operation编排；
- `SYS-EXPL`：D05探索家族及C03/C16实证协作；
- `SYS-ARCH`：收藏、知识和后续消费者；
- `SYS-PRESENT`：所有生命周期的可访问投影与UI叠加审计。

“横向服务”不是“没有设计”，也不是“应补一个小游戏”。它明确禁止为了凑12系统覆盖而增加章级新维度。

## 4. 第二数据实例仍未成立

每个第二实例现在必须同时登记：

```text
second_instance_id
fixture_ref
ruleset_ref
schema_ref
content_hash
evidence_status
isolation_status
contamination_refs
```

当前22行均为 `UNAVAILABLE` hash，不能证明同一规则版本、同一schema和只换内容数据。18行还明确记录跨机制污染或上游阻断。例如：

- C01的C02E01第二实例现已绑定 `PC02-E01-QUALIFIER`，但它同时引入C02功能损伤/非致死目标，所以是已知污染，不是复制证据；
- C04→C05同时叠加占用/退出新维度，并受C04验收、C05 L4重建阻断；
- C12→C21相隔九章且C21另有载荷诊断，不能直接称Hub内核复用成功；
- C22没有获批postgame或提前预显影范围，第二阶段保持blocked。

今后只有当fixture、ruleset、schema、内容hash和隔离报告全部可复现，且没有新增顶层输入/UI/持久状态域时，第二实例才可从 `unverified` 进入证据审查。

## 5. 阶段证据不能互相代签

原型证据现按三阶段分开：

1. `introduction`：证明首次规则可被理解；
2. `second_instance`：证明只换数据仍可玩；
3. `mastery`：在延迟场景无强制提示地掌握。

两个原审计错误已显式修正：

- C01第二实例必须提到 `PC02-E01-QUALIFIER`，不能只列C01/P1原型；
- C03延迟掌握不能用 `D04-P2` 代签，因为P2测试C2责任链，不测试工程工作单掌握。

同一章里的第二实例和mastery也不能互相代签。C17/C18在C20、C12在C21、C20/C21在C22的两种阶段仍各自保持missing。

## 6. 累积栈与复习

章×机制活动账按一行一个 `(chapter_id, lifecycle_id, activity_stage)` 记录，并带UI surface和组合对象。机器当前推导：

| 章 | 同时活跃机制数 | 风险 |
| --- | ---: | --- |
| C16 | 5 | 权限、视角、分舰、异步信息、身份握手同时进入界面 |
| C17 | 5 | 跨线复习、地方视角掌握、异步掌握、握手复用、敌方学习首次出现 |
| C20 | 6 | 多线、握手、学习账、并行承诺、模块装配、终局接力叠加 |

这些章必须先做负荷/UI原型；“只新增一个新判断”不能当通过理由。

为避免已知长休眠，Candidate活动账新增六个计划复习点：

- LIFE-C05：C07、C12；
- LIFE-C07：C09；
- LIFE-C11：C17；
- LIFE-C12：C15、C18。

它们把纸面计划间隔控制在三章以内，但都只是 `planned_review`。没有实时章链、内容fixture、Build与真人复述，不得称遗忘管理闭合。

## 7. 复合风险由碎片推导

每个碎片必须写清独立玩家输入、状态引用、可否单独教学和证据依据。checker只根据碎片行数推导复合风险，不再接受固定章节名单。

当前七个风险是：

| 章 | 可分别教学的碎片 |
| --- | --- |
| C01 | 基础身体动作 / 跨Encounter连续Operation |
| C02 | 功能损伤动词关闭 / 非致死胜利合同 |
| C03 | 地点承重身体 / 工程工作单与实证 |
| C05 | 实时请求占用 / 逐路安全退出 |
| C06 | 固定成员组合与同意 / 负载判断与安全中止 |
| C11 | 战略行动组编成 / 跨战区状态边 |
| C21 | 物理载荷诊断 / 政治停机与物理退出区分 |

C02与C06是v0.1漏报。未来若中性fixture证明两碎片确实共享一个输入、状态机和教学步骤，可合并；在此之前保持风险，而不是改复合名词掩盖。

## 8. 退役不等于删掉能力

每行现在拆成三项：

- `retired_shell_ids`：删除赛事页、教程页、三线/四线专用页等一次性壳；
- `preserved_base_verbs`：玩家已经学会且进入共享系统的基础动词；
- `postgame_behavior`：战后是继续共享核、只保留档案/复盘，还是在用户批准范围内开放安全重试。

这样可阻止“退休赛事壳”被误读为删除功能损伤，也可阻止终章机制默认扩成未批准postgame。

## 9. 实时章链仍是明确未闭合项

D07 checker当前不读取C01-C22每章的实时story-chain和用户回执，也没有把未来章的OPEN章窗接成机器依赖。治理账因此统一记录 `unwired_snapshot_only`，检查器输出WARN：

```text
Lifecycle/live chapter-chain join remains unwired for 22/22 rows
```

这不是格式缺陷，而是当前权限边界：D07不能用自身快照覆盖C04当前活动点、C05失效状态、C06以后冻结状态或未来用户决定。后续若要自动化，必须新建只读chain adapter，记录manifest path/hash/check time和不可用原因；在此之前不得把静态blocked名单写死进checker。

## 10. 当前机器结果与下一门

本轮静态检查结果：

```text
22 mechanisms
12 system coverage rows
66 phase evidence bindings
70 chapter-mechanic activity rows
7 derived compound risks
max cumulative chapter stack = 6
22/22 second-instance hashes unavailable
18/22 second instances contaminated or upstream-blocked
6 planned review beats, zero verified
22/22 live chapter-chain bindings unwired
```

下一合法证据顺序仍是：

1. 用户先裁决对应DEC和有界执行包络；
2. 为复合碎片各做可单独失败的中性fixture；
3. 冻结ruleset/schema并制作带内容hash的第二实例；
4. 做隔离差分，证明新增顶层输入/UI/持久状态域为0；
5. 安排延迟掌握和复习真人测试；
6. 只有用户证据后迁移回执允许，才进入GD3/L3或章级消费者。

在这些证据出现前，D07仍是Candidate风险与实验路线，不是全剧玩法封板、章节批准或制作授权。
