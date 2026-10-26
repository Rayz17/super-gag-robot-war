# D05 辅助玩法第二实例纸面 Preflight v0.1

> Authority：Candidate-only / neutral `TEST_*` data。
>
> Evidence boundary：`zero_build / human_not_run / no_replication_evidence`。本文只证明三个第二实例已经被写成可机检的纯数据纸面输入；不证明 `P-EX1-R2 / P-EX2-R2 / P-EX3-R2` 已执行，不证明 M5、M6、Build、真人测试或任何章节适配。

## 1. 冻结方法

首例动作集、逻辑 UI surface、Outcome、持久状态域和输出门锁在 [auxiliary-replication-freeze-contracts.tsv](../data/auxiliary-replication-freeze-contracts.tsv)。首例原文切片以“精确二级标题至下一个二级标题前、末尾规范化为一个 LF”计算 SHA-256，防止先改首例再宣称复用。

三个第二实例的唯一结构化真值在 [auxiliary-second-instance-paper-fixtures.json](../data/auxiliary-second-instance-paper-fixtures.json)。每个 Fixture 的 `canonical_sha256` 排除自身字段后，以 UTF-8、排序键、无空白分隔的 canonical JSON 计算。任何新增顶层代码、输入动作、UI surface、持久状态域或独立结算页的计数都必须为 `0`。

纸面通过不改变原型前置条件：实际 R2 仍须首例达到 M5，并取得 `DEC-06@approved_for_candidate_test`；之后才可在同一动作/UI/Outcome 合同上做 Build 与真人复用验证。

## 2. `FX-D05-EX1-R2-PAPER`：风脊转运栈

### 初态与玩家路径

- 入口 `TEST_EX1_R2_N0_GATE`，目标 `TEST_EX1_R2_N5_CRANE_BEACON`；六节点、三条显式邻接路线。
- 玩家沿用 `HELP / MOVE / OBSERVE / PHOTO / REPORT / RETURN / TALK`。没有任务箭头、额外背包或第二套路线 UI。
- `TEST_EX1_R2_N4_COVERED_RAMP` 受可选制动楔影响；不帮助只关闭第三路线，仍保留经抗风桥与服务沟的两条合法路径。
- 四条有来源现场事实分布在不同节点。`REPORT` 引用两条本路事实才得 `clear`；一条事实或主动保留判断得 `partial`；回入口退出得 `withdraw`。

### Outcome 与未来消费

| Outcome | 静态条件 | 合法提交 | 禁止提交 |
| --- | --- | --- | --- |
| `clear` | 到达目标且至少两条所经事实支持报告 | 路线摘要、访问/对象变化、具名后续消费者 | 世界真相、通用奖励、人物入队 |
| `partial` | 一条来源事实或明确 unresolved | 已观察来源、`needs_followup` 类摘要 | 自动补齐第二事实 |
| `withdraw` | 从入口退出 | 已观察内容与检查点 | 路线结论或目标回应 |

`TEST_CONSUMER_EX1_R2_ROUTE_CARD` 消费路线摘要；`TEST_CONSUMER_EX1_R2_KEEPER_REPLY` 消费可选帮助和报告状态。两者都只是测试消费者，不建立章节资产或人物 Canon。

### 机器断言

1. 动作/UI/Outcome/状态域与冻结行完全相等，所有新增计数为零。
2. 邻接图双向；每条声明路线从入口连续到目标。
3. 移除可选帮助所开放的节点后仍至少有两条合法路线。
4. `clear_min_supported_facts=2`、`partial_min_supported_facts=1`，无证据 clear 必须拒绝。
5. 所有内容 ID 与消费者均为 `TEST_*`。

## 3. `FX-D05-EX2-R2-PAPER`：扭摆试验臂

### 初态与求解器

玩家沿用 `ANNOTATE_SUPPORT / COMMIT_REPORT / CONFIGURE / INSPECT / PREVIEW_SAFETY / REVISE_HYPOTHESIS / RUN_TEST / WITHDRAW`，只替换三证据、两假说和三槽变量数据。

```text
score = 0.70 * gain + 0.004 * load - 0.48 - patch_bonus
score <= 0.20                 -> stable
0.20 < score <= 0.45          -> bounded_oscillation
score > 0.45                  -> outside_safe_envelope
load == overload              -> rejected_scope
```

四个预注册校验点：

- `none + reduced + rated = 0.185 -> stable`；
- `preload_shim + nominal + rated = 0.115 -> stable`；
- `none + high + rated = 0.57 -> outside_safe_envelope`；
- 任意 `overload -> rejected_scope`，不得运行。

这给出至少两条不同的额定载荷安全解，但不会把公式正确性冒充真人可理解性或玩法趣味性证据。

### Outcome 与未来消费

| Outcome | 静态条件 | 合法提交 |
| --- | --- | --- |
| `clear` | 额定载荷 `stable` 且实测支持具名假说 | 证据、假说差分、测试安装请求、`ST_RESULT` |
| `partial` | 只有低载或 bounded 结果 | 保留未决判断与再测试工单 |
| `withdraw` | 实测前退出或只留危险草案 | 已收证据；不写身体、不扣材料 |

`TEST_CONSUMER_EX2_R2_ACCEPTED_SETUP` 读取已验证设置；`TEST_CONSUMER_EX2_R2_RETEST_ORDER` 读取未决工单。

### 机器断言

1. 动作/UI/Outcome/状态域与冻结行完全相等，所有新增计数为零。
2. 三条证据都有 `TEST_SOURCE_*`，两假说均可被具名证据支持；不允许无来源结论。
3. 以 Decimal 枚举 18 个变量组合，重算四个预注册校验点并验证至少两个不同额定安全解。
4. `overload` 永远拒绝，`outside_safe_envelope` 不产生身体写回。
5. 两个消费者具名存在，所有内容 ID 均为 `TEST_*`。

## 4. `FX-D05-EX3-R2-PAPER`：镜向中继室

### 两访知识链

- 同一空间只有 `ENTRY / CONSOLE / SIDE_PLATFORM / RETURN` 四个 `TEST_*` 物理节点；第二访不新增房间、钥匙或 inventory item。
- 第一次访问可读凹槽、旧日志 `LEFT-2-RIGHT` 与现场纸卡 `RIGHT-1-LEFT`，矛盾不得自动消除。
- 两访之间收到带来源的校准记录：T-10 前日志的 LEFT/RIGHT 标签镜像，时长不变。
- 第二访当前回波证明中段时长为 `2`；旧日志经规则重解释为 `RIGHT-2-LEFT`。
- 只有同时引用旧日志、校准记录和当前回波，`APPLY` 才可将同一 `TEST_EX3_R2_SIDE_PLATFORM` 从 `closed` 改为 `accessible`。

玩家沿用 `APPLY / LINK / OBSERVE / RETURN / SUBMIT_INTERPRETATION` 及四种有限关系 `contradicts / later_than / same_subject / supports`。`inventory_items=[]` 是硬条件。

### Outcome、遮罩与未来消费

| Outcome | 静态条件 | 路线后态 |
| --- | --- | --- |
| `clear` | 第二访以三来源提交 `RIGHT-2-LEFT` 并执行 | `accessible` |
| `partial` | 建立镜像规则但不执行，或只证伪字面纸卡 | `closed_but_understood` |
| `withdraw` | 任一访问从 RETURN 退出 | `closed` |

非 oracle 的玩家投影永远不含 `TEST_ORACLE_EX3_R2_SEQUENCE`。`TEST_CONSUMER_EX3_R2_ROUTE_DELTA` 消费路线变化；`TEST_CONSUMER_EX3_R2_UNRESOLVED_NOTE` 保留纸卡差异这个未知，不替故事回答原因。

### 机器断言

1. 动作/UI/Outcome/状态域与冻结行完全相等，所有新增计数为零。
2. 物理节点恰为四个，知识节点不超过五个，关系类型严格等于冻结的四类。
3. inventory 为空；路线变化只指向原有平台，不准用新门卡替代知识因果。
4. 路线开放所需三证据与正确序列精确匹配；非 oracle 投影不得含 oracle-only 值。
5. 所有内容 ID 与消费者均为 `TEST_*`。

## 5. 运行与失败语义

```bash
python3 scripts/check_d05_auxiliary_second_instances.py
python3 scripts/check_d05_auxiliary_second_instances.py --self-test
```

专用检查器验证冻结切片哈希、canonical Fixture 哈希、合同相等、语义约束、注册表证据边界和故障注入。任一失败都只允许返回 D05 Candidate 数据／合同修正，不得借机改 Canon、Reader、Runtime、Demo 或把纸面状态晋级为 R2/M6。

## 6. 当前诚实结论

三个家族现在各有一个独立的第二实例纸面数据包，静态防漂移门可以阻止新增动作、UI、状态域、结算页和知识泄漏。这满足的是“第二实例纸面 preflight 已定义”，不是“同一系统已经复用成功”。实际 `P-EX1-R2 / P-EX2-R2 / P-EX3-R2`、M6、Build、真人学习／趣味证据仍全部未完成。
