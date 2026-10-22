# C01–C03 上游 GD2 依赖闭包审计 v0.1

> Status: `candidate_dependency_closure_register_complete / 0_sealed / no_visual_direction_or_graybox_authorized`
>
> Machine source: [opening-gd2-dependency-closure.tsv](../data/opening-gd2-dependency-closure.tsv)
>
> Scope boundary: 本审计只整理 Candidate 设计依赖，不修改 Canon、Accepted Reader、Runtime、C01E02 Demo 或正式资产。

## 1. 结论

前三章已经有足以锁定剧情出口的 Accepted Story，也有万机馆楼层、节点、泊位和若干 Working 机体身份；但这不等于地点、机体或玩法已经设计成立。

本轮登记 28 条开篇依赖：

- 18 条主键逐项覆盖 `BF0020`–`BF0037`，不含 `BF0038` 天空铸环；
- 10 条是这些 GD2 包不可缺的 GD1 身体、敌人、控制接口或对象级设计行；
- 28 条全部保持 `BLOCKED_*`，0 条 `sealed`；
- 当前只有两张万机馆逻辑问题图有真实路径与哈希，二者都不是正式外观、总平、剖面、视觉方向回执或工程灰盒；
- 没有任何一项具备完整的“逻辑图 + 用户视觉方向 + 工程/玩法灰盒 + BOM + 下游绑定”证据链。

所以，现阶段能成立的表述是：

> 已经知道哪些故事事实不能再临时改，也已经知道每个地点和机体还缺什么；尚未完成任何一个可供正式 gameflow、连续 Previs、美术或 Runtime 直接消费的开篇 GD2/GD1 包。

## 2. 权威快照与使用边界

### 2.1 可锁定的输入

| 输入 | 可依赖范围 | 不能据此推断 |
| --- | --- | --- |
| `ASB-C01-20260808-C9A9AA49` | 当前 C01 Reader、四话组件与回执字节相符；事件、时序、人物/机体行动及章末出口 | 万机馆完整建筑、C01地图、正式机设、玩法、镜头、资产或 Runtime 已验收 |
| `ASB-C02-20260806-56827053` | 当前 C02 五话故事、3:2结果、事故不改赛果、约九米两转子、随舰/留街事实；有可达 Git 快照 | 赛事规则、货运环多态地图、九米工程链、机体动作包已成立 |
| `ASB-C03-20260808-AE2F1628` | 当前 C03 四话顺序、工具归还、第一/第二锤、人物/机体去向、C-1与双信出口 | 旧预生产表仍可用、工务城总图、中央环负载网络、C2玩法或连续 Previs 已验收 |
| Current Canon `entities.tsv` | 万机馆、木桶街、工务城及核心机体的 Working 身份、边界和生命周期 | `needs_review` 对象已有完整身体、视觉或玩法设计 |
| 万机馆 `wanji_floors.tsv` / `wanji_locations.tsv` / `wanji_carrier_berths.tsv` | 6层、30节点、8类泊位及局部尺度/邻接/容量锚点 | 这些表已经构成可行建筑、舰体、流线、工程或美术方案 |

C01 与 C03 的当前 Reader 字节虽与验收绑定相符，但缺可恢复的可达 Git 提交或外部归档。本表将其写为 `current bytes match; durable archive unresolved`，不能把“当前相符”误报为“历史可恢复”。

### 2.2 Candidate 资料的角色

- [Design-L0–L3 设定回补合同](../08-l0-l3-setting-backfill.md)定义字段、门禁和失效范围；
- [万机馆 Master Pack v0.1](../setting/wanji-master-pack-v0.1.md)是证据底座和交付清单，不是完成的 Master Pack；
- [开篇 Previs 需求表](../chapters/c01-c03-previs-needs.tsv)定义问题和消费者，不是实际图片、灰盒或验收证据；
- C01E02 Demo 只能提供隔离的 Candidate 运行证据，不能批准正式 C01 地图、全局战棋规则、视觉方向或 GD2；
- 旧 C03 预生产顺序是 History/漂移证据，不能覆盖 Accepted Reader 的 `E01换梁与失工具 → E02四工具归还 → E03负载反转`。

## 3. 机器表怎样判读

每行以单值 `backfill_id` 作为主回补项；`backfill_object_id` 必须逐行等于 `setting-backfill-register.tsv` 中该债务的 `object_id`，`supporting_backfill_refs` 只表示依赖，不替主键。`design_subject_id` 保存本行实际设计对象；`current_canon_anchor_or_none` 只允许两类值：能够在 Current Canon `entities.tsv` 逐行解析的单一实体 ID，或显式哨兵 `NONE_NO_SINGLE_CURRENT_CANON_ENTITY`。复合地点包、视觉包和接口包没有单一 Current 实体时必须写哨兵，不能把 Candidate 设计 ID 冒充 Canon。

因此正确的机器结论是：只对债务主键做 `(backfill_id, backfill_object_id)` 比较时，它与回补总表逐行 diff 为 0；这个结果不代表 28 个设计主体都有 Canon 实体。`design_subject_id` 与债务对象之间有 9 条有意映射，不会覆盖 `MECHA_GUARDIAN_Z`、`MECHA_NO_NAME_ONE` 等原始回补债务 ID；Current Canon 锚点则是 **15 条实体 ID 全部可解析、13 条明确无单一实体**。`BF0020`–`BF0037` 仍由 checker 做精确全集比较。

关键字段含义如下：

| 字段 | 含义 |
| --- | --- |
| `backfill_object_id` | 回补总表拥有的债务对象 ID；必须与 `backfill_id` 对应行精确相等，不能换成 Current Canon 主体 |
| `design_subject_id` | 本闭包行真正设计、验证或出图的主体；别名迁移后可与债务对象不同 |
| `current_canon_anchor_or_none` | 有且仅有单一 Current Canon 实体时写可由 `entities.tsv` 解析的稳定 ID；否则写 `NONE_NO_SINGLE_CURRENT_CANON_ENTITY`，禁止填 Candidate 设计包 ID |
| `locked_current_fields` | 来自 Current Canon 或 Accepted Story、下游不能自行改变的事实 |
| `open_candidate_fields` | 必须由 GD1/GD2 设计而非 Writer、关卡、美术或 Demo 临时决定的内容 |
| `logic_diagram_requirement` | 因果、拓扑、控制、状态、承重或接口需要哪种可审计图；已有文件须带哈希 |
| `visual_direction_requirement` | 哪些轮廓、尺度、状态、材质或动作必须给用户看图裁决；`not_created` 不得推断方向 |
| `engineering_or_gameplay_graybox` | 需要哪种低模、纸模或规则验证；本轮全部 `not_run` |
| `bom_requirement` | 进入资产或 Runtime 前必须给出的模块、状态、Rig、碰撞、动画、UI、镜头、音频、复用和性能边界 |
| `approval_chain` | 内部封存责任与用户裁决范围；内部负责人不能代签用户视觉/玩法/产品回执 |
| `reader_migration_trigger` | 何时才允许提出 Accepted Reader 迁移；普通设计困难和省资产不是理由 |

`BLOCKED_*` 不是说故事无效，而是说该对象不能进入指定下游门。

## 4. 四个必须单独抬高的阻断

### 4.1 C01 馆守Z时序必须读取 Current 主体行与 Accepted Reader

`OGD2-006` 绑定的是当前生命周期主体 `V353U001` 和 C01 Accepted Reader：E02 正式起身/首战，E03 原右前臂与回收机构永久毁损，E04 换装非拳击型黄色巡展臂。`MECHA_GUARDIAN_Z` 已是 deprecated alias；`wanji_locations.tsv` 局部备注仍残留“E03首次完整行动”等旧时序，不能进入 GD2、Writer-safe context 或 Demo→正式设计迁移。

本审计不改 Canon，因此该残留仍需单独的非语义修正票；在修正前，机器表的 `locked_current_fields` 明示上述读取优先级。

### 4.2 万机馆不是一张舰体图就能关闭

`OGD2-001` 与 `OGD2-002` 共同阻断开篇：前者要求 WMP-03/04/06–10/12–15 的建筑、流线、功能、形态和 BOM；后者要求固定馆、低速场景身体与未来多格母舰之间的控制梯度、状态写回和硬停合同。

现有两张 SVG 只能证明问题已经被显式列出：

- `setting/visuals/wanji-cutaway-schematic-v0.1.svg`，SHA-256 `0cd02aa60b1a60a8269a9c050aac5a2b2c322171eb190abb45fc1951b8028c64`；
- `setting/visuals/wanji-control-gradient-v0.1.svg`，SHA-256 `5444b75a8b2781bc5b2e31f8f27dec32d45ac83402938d54193c6b4335c14bb8`。

它们没有批准固定馆/巡展舰外形、楼层能否装入同一船骨、七流线、生活动力损管空间、场景身体操作反馈或资产量。

### 4.3 约九米转子是工程迁移门，不是美术自由区

`OGD2-013 / BF0029` 锁定的是一条已验收的实体链：两件约九米转子、旧件整件移出并锁存、新件依次经过港口龙门吊、泊位吊机与 B1 大型货运升降台安装，随后不停机直达工务城。

当前缺质量、厚度、叶片包络、吊点、运输架、各节点净空、B1剖面、承重、锁存和停机责任。处理方法只能二选一：

1. 真实低模和工程走查证明成立，再补档案、图与 BOM；
2. 证明不成立，提交可行替代尺寸/路线对比和影响清单，由用户决定是否迁移 Reader。

禁止在关卡、美术或 Runtime 中静默缩小、折叠、传送或把两件物体合并成一个升级数值。

### 4.4 C03 必须按 Accepted Story 重绘，而不是修补旧表

`OGD2-020 / BF0032` 的第一输入是当前 C03 Reader，不是旧预生产：

```text
E02：四工具归还原主体 → 衡令主动越过黄线进入环心
E03：巨环升起 → 第一锤 → 地下缆索揭示真实城市负载
    → 第二锤停止 → 改为拆除城市连接 → 衡令旧核撤离
```

移动货运环、中央巨环、医院/住宅/城梁承重网络、万机馆进退空间和安全观测线必须在同一重基图上闭合。只改旧表标题或刷新哈希不能通过。

## 5. 建议的独立 Session 顺序

这是一条依赖顺序，不要求等待 C01E02 Demo；Demo 继续隔离并行，正式 GD2 不读取它的专用脚本作为规则或空间权威。

| 顺序 | Session 边界 | 必须产出 | 停止门 |
| --- | --- | --- | --- |
| 1 | 万机馆建筑/舰体基础 | WMP-03/04/06；固定馆总平、统一剖面、七流线低模；三项用户看图选项 | 未获空间/视觉方向回执，不做正式资产 |
| 2 | 万机馆控制与开篇形态 | WMP-02/05/07/08/09/12；身体状态、岗位、泊位、重件路线与控制图；匿名灰盒问题单 | 战棋时制/控制未定时，不把候选操作写入 Runtime |
| 3 | C01 地点与联合机体包 | `BF0021`–`BF0024`；导览撤离图、E02/E03连续图、E04长图、三主体比例/动作包 | C01E02 Demo 不得代签正式图、玩法或视觉 |
| 4 | 木桶街与 C02 工程包 | `BF0025`–`BF0029`；城市总图、货运环多态、跨尺度空间、阵容包、九米工程裁决包 | 九米链未证实前，不启动正式 C02 Previs/资产 |
| 5 | 工务城与 C03 巨构包 | `BF0030`–`BF0037`；城市总图、E01承重图、E02/E03重基图、职业接口、三台核心身体包、C-1/双信接口 | 旧预生产顺序、通用工具Buff或强制第二锤均直接退回 |
| 6 | 章级 GD3/BOM | 章策只绑定已封存 ID/hash，编制地图状态、玩法目标、Previs与 Candidate BOM | 任一 `OPEN/BLOCKED`、缺回执或哈希漂移即停止 |

地点与机体可以在同一章并行设计，但它们不能彼此假设未批准的尺度。例如，C03中央环不能先假定社勇王合体占位，社勇王也不能先假定中央环给得下完整合体通道；二者必须通过联合低模收敛。

## 6. 关闭一行的最低证据

一条依赖从 `BLOCKED_*` 进入 `sealed` 前必须同时满足：

1. `authority_sources` 和 Accepted Story 绑定仍为当前匹配；
2. 锁定字段与开放字段已逐项裁决，且没有从 Candidate 偷升 Working/Hard；
3. 需要的逻辑图、方向图或连续动作图有真实路径、版本和 SHA-256；
4. 用户只对表中明确 scope 的产品/玩法/空间/视觉方向签具名回执；沉默和内部 PASS 不算；
5. 工程或玩法灰盒绑定版本、任务、日志/录像、失败结果与结论；纸面问题图不能冒充真人/Build 证据；
6. BOM 给出新建/复用、资产等级、负责人、状态差分、性能与下游消费者；
7. `reader_migration_trigger` 未触发；若触发则先完成 Canon/Reader 影响裁决，不能一边改图一边保持旧验收；
8. 章级 GD3 只引用封存 ID/hash，不复制第二份规则或真相。

本轮没有用户授权 Build、真人测试、正式视觉方向或资产生产，所以这些证据均未执行，也没有以计划状态代替结果。

## 7. 对后续 Writer、Reader 与游戏解构的直接约束

- `open_candidate_fields` 不能作为 Reader 安全上下文；Writer 不得补新房间、路线、部件、权限、巨大动作或工程参数；
- Accepted Reader 仍是前三章故事权威；设计优先适配它，而不是为了让灰盒更容易而回写剧情；
- 只有表中 `reader_migration_trigger` 被真实工程/物理证据触发，才提交范围化迁移请求；
- gameflow 必须等待相应 GD1/GD2 封存，并绑定真实图/hash；“有剧情结果”不等于“已有玩家动作”；
- 正式美术、连续 Previs 和 Runtime 必须等待用户方向、灰盒与 BOM，不得从名词、文字描述或隔离 Demo 推断批准。

这份审计的价值不是补出了新的城市或机器人外观，而是把 Writer 曾经被迫临时创造的部分，改成了有 Owner、审批范围、消费者和停止门的上游设计债。
