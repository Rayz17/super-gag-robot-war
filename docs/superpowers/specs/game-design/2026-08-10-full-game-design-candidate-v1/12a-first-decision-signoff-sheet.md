# 首批四项决策｜旧技术授权附录（已冻结）

> Status: `superseded_pending_public_direction_rebase / not_ready_for_signature / presented_no_decision / no_receipt_instance / no_execution_envelope`
>
> 这份附录形成于“A／B／C／D四种时制等权比较”的旧方案。当前公开策划已改为：**B 短全队协同是主策Candidate推荐，A 逐台行动是低负担备选，C／D只保留比较参考。** 因为决策对象已经改变，旧包不能继续收签，也不能用一句“按推荐批准”复活。
>
> 当前唯一评审入口是[00c核心玩法总案](00c-core-game-design-master-review.md)。本页旧批准码全部失效，**不得回复或使用**，也不得生成方向回执、执行包络、Build、真人Session或迁移。冻结覆盖见 [first-decision-signoff-freeze.tsv](data/first-decision-signoff-freeze.tsv)；旧机器包只允许作历史追溯。

## 历史内容：当时准备裁决的四项（不可签）

| 决策 | 推荐、替代与接受条款 | 批准后只授权 | 明确不授权／停止线 |
| --- | --- | --- | --- |
| **DEC-01 产品身份**<br>`APPROVE_RECOMMENDED` | **推荐：**重故事、轻练级的角色驱动 C2 机器人战术 RPG＋移动博物馆 Hub。<br>**替代：**传统 SRPG 为主/C2 弱化；剧情冒险为主/战术轻量。<br>**条款：**`D01-C01` 产品身份；`D01-C02` 目标玩家与评估准则；`D01-C03` 排除执行权限。<br>**证据：**[产品宪章](03-product-experience-charter.md)、[系统图](04-full-game-system-graph.md)、[核心循环走查](validation/d02-d03-core-loop-paper-walkthrough-v0.1.md) | 建立 `DRS-DEC01-A / DR-DEC01-A` 方向回执；锁定目标体验、目标玩家、Candidate 评估准则和排除项。**DEC-01 单独不列任何 Prototype/Gate/Build/Session。** | 不批准具体时制、规则、章节、美术、预算、GD0 迁移、Canon/Reader/story-chain、Current Runtime、正式资产、L6 或 Demo 提升。产品定位/目标玩家或来源 hash 改变即失效。 |
| **DEC-02 基础战术／失败合同**<br>`APPROVE_RECOMMENDED` | **推荐：**已知物理确定＋信息不完全＋非歼灭目标＋局部失败前向继续。<br>**替代：**传统命中率/单 HP；失败即重开。<br>**条款：**`D02-C01` 确定物理；`D02-C02` 信息不完全；`D02-C03` 非歼灭目标；`D02-C04` 失败前向仅作 Candidate；`D02-C05` P1 共同规则、不含 Scheduler/仪器。<br>**证据：**[SRPG/C2 设计](05-srpg-c2-core-design.md)、[P1 中性 Fixture](validation/d04-p1-neutral-rules-paper-fixture-v0.1.md)、[测试计划](10-prototype-test-plan.md) | 建立 `DRS-DEC02-A / DR-DEC02-A` 方向回执；锁定 P1 A/B/C/D 共同物理、动作结果、信息预算、目标与失败规则。 | 不批准角色 C2、Scheduler、测试仪器、DEC-02 单独 Build、正式数值或章节地图。单场 P1 不能迁移长期“失败前向”，仍需 P-SET1 与 Operation→Chapter 持久回写证据。共同规则/地图/信息预算漂移或角色 C2 混入 P1 即停。 |
| **DEC-03 时制选择方法**<br>`APPROVE_COMPARE_ABCD_ONLY` | **推荐：**比较 A/B/C/D；D 是正式传统阵营回合控制组。P1 只淘汰或形成 shortlist；shortlist 再承载同一组最小核心 C2，之后才由用户作最终时制裁决。<br>**替代：**现在锁短 WEGO；直接锁传统阵营回合；提交正式成本证据排除 P1-D。<br>**条款：**`D03-C01` ABCD；`D03-C02` 中立共用语义；`D03-C03` 原生语法/UI 与等价可发现性；`D03-C04` 盲化/预登记顺序、成本、阈值；`D03-C05` P1 只 shortlist；`D03-C06` C2 crossover 先于最终裁决；`D03-C07` 本次无胜者、无 crossover 权限。<br>**证据：**[时制中立合同](data/time-system-neutrality-contract.tsv)、[四版合同](data/time-system-ab-test.tsv)、[Prototype Registry](data/prototype-test-registry.tsv) | 建立 `DRS-DEC03-A / DR-DEC03-A` 方向回执；允许四版共享世界初态、动作结果、目标、AI 与未知信息预算，各用原生 command grammar/UI。P1 结果只可为 `shortlist_two/three/four`、`no_winner`、`revise_top_two` 或 `retire_all`。 | 不批准 P1 唯一胜者、预选 WEGO/D、Demo 时制倒灌或最小 C2 crossover。Crossover 另需 DEC-04-A 及独立 implementation/human_run 包络；完成后才可呈现 `DEC-03-M = select/revise/no_selection/retire_all`，只有用户 `select` 才能形成唯一时制迁移回执。破盲、共同语义/教学预算漂移、未登记实现顺序/成本、P1 选胜者或绕过 crossover 即停。 |
| **DEC-11 新生产流程**<br>`APPROVE_ISOLATED_GATE_TEST_ONLY` | **推荐：**只在隔离副本验证 D09 精确 version/hash 定义的依赖闭包、分层门和五类回执；现行流程在独立分相迁移前保持唯一有效。<br>**替代：**保留旧流程；仅作人工约定。<br>**条款：**`D11-C01` 隔离 frozen/synthetic copy；`D11-C02` R0/checker/故障注入/dry-run；`D11-C03` Current Writer 输出为 0；`D11-C04` 不写现行链；`D11-C05` M、M1–M4 分相迁移。<br>**证据：**[生产流程](09-production-pipeline-and-gates.md)、[门实例 Schema](data/game-design-gate-instance-schema.tsv)、[失效路由](data/invalidation-routing-rules.tsv)、[Preflight 合同](data/prototype-execution-preflight-requirements.tsv) | 建立 `DRS-DEC11-A / DR-DEC11-A` 方向回执；以后只有在精确 `E-R0-IMPLEMENT` 包络独立获批后，才能隔离验证 `R0-TEST-KERNEL`、Candidate gate-instance checker、synthetic/frozen-copy 故障注入与 dry-run manifest。Writer-readable Current 输出必须为 0。 | 不批准自动迁移旧链、Current Registry/schema、旧 PASS/回执升级、Canon/Reader、story-chain、Current Runtime、正式资产、L6 或 Demo 写入。后续迁移必须分别走 `DRS-DEC11-M` 计划、`M1` checker、`M2` Registry/schema、`M3` 单一 scope chain、`M4` 部署后重验/回滚；不得一张回执迁 C01–C04。任何 Current 可读输出或现行链写入即停。 |

四项通用硬停：方向回执或包络失效；来源 hash 漂移；包络到期、撤销、超限或重叠；共享预算池预检失败；尝试写禁止路径；机器硬门失败；P0 或隐私事件。

## 历史内容：旧执行边界（不得申请）

方向回执只回答“是否允许为这类问题准备证据”。每次执行还必须完整填写 [execution-envelope Schema](data/candidate-test-execution-envelope-schema.tsv)，冻结精确 scope/path/source/output/Build/日期/人时/现金/外部副作用，并由用户用 `AUTHORIZE_EXACT_ENVELOPE` **独立批准该包络的 `authorization_subject_sha256`**；真实回执 instance/path/sha256/locator/user ref、supersedes、overlap check 和 Preflight 缺一不可。

- `E-R0-IMPLEMENT`：只含 `R0-TEST-KERNEL`，`max_total_builds=1`。
- `E-P1-ABCD-IMPLEMENT`：R0 M3 后才可申请，只含 A/B/C/D 四个匿名 Scheduler Build，`max_total_builds=4`、最多 1 个并行实现。
- 两个 implementation 包络使用不同 `exclusive_scope_key`，但共同消耗 `STAGE0_R0_P1` 池，**合计**上限仍为 14 日历日、80 内部人时、外部现金 0；拆包不能翻倍。
- P1 真人测试另建 `human_run` 包络；最小 C2 crossover 再另建 implementation/human_run 包络。它们不能借用 P1 的剩余额度。本页不授权外部服务、招募、参与者或数据采集。

## 旧回复格式（已失效，不得回复或使用）

下列代码只为说明旧包当时怎样绑定选项，不再构成有效回复格式：

```text
DEC-01 = APPROVE_RECOMMENDED
DEC-02 = APPROVE_RECOMMENDED
DEC-03 = APPROVE_COMPARE_ABCD_ONLY
DEC-11 = APPROVE_ISOLATED_GATE_TEST_ONLY
```

无论回复上述任何代码、`DEFER`或泛化赞同，当前都不创建回执，不启动 Prototype/Gate/Build/Session/代码写入/上下文生成/迁移。机器完整版 [first-decision-signoff-pack.tsv](data/first-decision-signoff-pack.tsv) 与其冻结覆盖只用于追溯；若以后真的进入结构化授权，必须按届时有效的公开玩法方向重新制作一份新包，而不是修改本页状态。
