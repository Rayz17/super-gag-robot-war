# D10 真人试玩 Session 实例与证据链合同 v0.1

> Status: `candidate_contract / zero_participant / zero_session / not_run / no_human_run_authorization`
>
> Authority boundary: 本文只定义未来如何合法、可复核地记录一次真人试玩。它不是同意书、招募公告、执行包络、Preflight实例、Build、真人证据或用户玩法验收。当前 [Session实例表](../data/human-playtest-session-instances.tsv) 只有表头；[状态表](../data/human-playtest-program-status.tsv) 固定为 `0 participant / 0 session / not_run`。

## 1. 为什么原有计划还不能生成M5

[prototype-test-registry.tsv](../data/prototype-test-registry.tsv) 定义Prototype、样本下限和问题，[playtest-cases.tsv](../data/playtest-cases.tsv) 定义任务与阈值，[playtest-session-result-schema.tsv](../data/playtest-session-result-schema.tsv) 定义结果字段，[acceptance-evidence-registry.tsv](../data/acceptance-evidence-registry.tsv) 定义证据消费者；但此前没有一个可实例化的行同时证明：

1. 哪个被用户精确授权的 `human_run` 包络允许接触这名参与者；
2. 哪个仍有效的Preflight把Session绑定到冻结Build、规则、地图、Case、主持脚本和隐私快照；
3. 参与者是否真是首次接触、看到了什么提示、允许保存哪些记录、是否退出或不适；
4. 行为、自由复述、偏好、录像和日志是否属于同一Session且hash未漂移；
5. 内部证据判定与用户最终裁决是否被严格分离。

[human-playtest-session-instance-schema.tsv](../data/human-playtest-session-instance-schema.tsv) 现在补上这条实例链；[result crosswalk](../data/human-playtest-session-result-crosswalk.tsv) 保留原39个结果字段，并增加授权、冻结、隐私、提示污染、退出和用户裁决边界。

## 2. Session准入：七项AND，一项缺失即不得建实例

主持人只能在以下七项全部成立后，把一行由`planned`推进至`ready`：

1. `prototype_id`与全部非自动`case_ids`存在，且Case的`applicable_prototype_ids`包含该Prototype；
2. 对应`acceptance_evidence_id`已预登记全部Case，但尚未把它标为真人PASS；
3. 一个独立获用户 `AUTHORIZE_EXACT_ENVELOPE` 的 `human_run` 包络仍在有效期内，Prototype、参与者上限、招募、采集、补偿、保留与删除范围都覆盖本Session；
4. 一个`execution_phase=human_run / status=passed`的Preflight绑定同一包络、授权主体hash、回执hash、Build ID、Case和隐私快照；
5. 所有自动前置门已PASS；不能以Demo PASS、内部试玩、M2纸面Fixture、implementation包络或方向回执替代；
6. Build、content manifest、ruleset、map/scene、tutorial、UI、source snapshot、Case、主持脚本、遥测Schema、隐私模板和已知问题均已冻结，并分别记录path/opaque ref与SHA-256；
7. 参与者在开始前逐项同意实际采集范围，且匿名ID、首次接触资格和合理便利已经核定。

`ready`之后任一来源hash、包络、Preflight、自动门或隐私范围变化，立即回到`invalidated`；不得只更新hash后继续。

## 3. 生命周期与一人一行

合法状态为：

~~~text
planned -> ready -> running -> completed
                         |-> withdrawn
                         |-> aborted
任一有效状态 -> invalidated
~~~

- 一行只能记录一名匿名参与者、一个Prototype和一次连续Session；多个Case可以同场执行，但必须在冻结脚本中明确顺序与休息点。
- P2的Session A/B、跨日回访、P1冷启/回访必须使用不同`session_instance_id`；用同一`participant_pseudonym_id`关联，不能合并成一行。
- 重试是新Session；原行保留`retry_required`与真实失败，不能覆盖。
- `withdrawn`不是失败样本，保留范围只限参与者没有要求删除且同意继续保留的安全/可用性证据；不得计入完成率、理解、策略或偏好分母。
- 纠正登记错误使用`supersedes_session_instance_id`，旧行进入`invalidated`；不得删除旧行制造干净结果。

## 4. 匿名ID、首次接触与破盲

### 4.1 匿名ID

- 证据表只使用`PT-...`假名ID，禁止姓名、邮箱、电话、社交账号、设备硬件ID、IP地址或可反查自由文本。
- 招募联系表与试玩证据分开保存，Session只记录`contact_data_separation_result=pass`和最小访问角色。
- `consent_record_ref_and_sha256`使用受限opaque ref，不把含PII的同意记录复制进Candidate包或普通报告。

### 4.2 首次接触

`cold/content_cold`必须同时满足：未读设计文档、未玩该原型/章节灰盒、未看录像或答案、不是作者/制作人/QA/项目成员。任一条件不满足写`first_exposure_eligibility=fail`，该行仍可作为诊断材料，但不能进入冷启动分母。

回访、已学习、无障碍专项分别写`returning / learned / specialist`；不得把它们改名为cold。P1与crossover只向参与者展示预登记匿名标签，`blind_variant_label`和偏好记录不得出现A/B/C/D、Scheduler名称、推荐顺序或工程成本排序。

## 5. 主持逐字脚本最低骨架

每批可以增加任务专属句子，但下列顺序和语义必须保留，版本与hash在招募前冻结。

### 5.1 开场与同意确认

主持人逐项说明：

1. “我们在测试游戏设计，不是在测试你的能力；没有必须完成或答对的要求。”
2. “你可以随时暂停、跳过问题或退出，不需要解释，也不会因此失去已经承诺的补偿。”
3. 逐项点明本场是否保存屏幕、输入、结构化遥测、语音、人脸和匿名引文；未勾选的项目不采集。
4. 说明谁能访问、最迟保留到何时、如何申请删除，以及聚合匿名数据在删除请求后的处理边界。
5. 询问当前输入、字幕、缩放、闪烁、声音、时间压力或其他合理便利需求；便利在任务前登记，不算策略提示。
6. 再次确认参与者愿意开始，记录同意时间；在这一步之前不启动Build、录屏、语音或遥测。

只有参与者明确确认退出权后，实例才可写`right_to_withdraw_acknowledged=true`；主持人或招募者不得代填。

本合同不是任何法域的最终法律文本。若进入外部招募，实际同意/补偿/保留模板必须由包络列明的`LEGAL_OWNER`或用户指定责任者审阅；默认不招募未成年人或包络未明确覆盖的敏感群体。

### 5.2 任务说明

主持人只读冻结任务卡，不解释最佳路线、敌方规则、角色权能、失败原因、版本差别或系统意图。开始后保持沉默，除非参与者主动请求、出现安全/设备问题，或达到预注册提示触发点。

### 5.3 事后顺序

1. 先给90秒无引导自由复述；主持人不补词、不点名角色、不提示因果。
2. 再做预注册迁移题、责任链或分类题。
3. 再询问身体感、代理权、疲劳、不适、复玩/继续意愿。
4. 最后才询问盲态版本偏好及理由；不得先揭示版本映射或主策推荐。
5. 重新说明退出/删除渠道和证据保留期。

自由复述前出现定向因果问题，`R-FREE`必须排除；偏好前破盲，偏好指标必须排除。

## 6. 提示、主持救援与污染

唯一提示等级见 [human-playtest-hint-level-contracts.tsv](../data/human-playtest-hint-level-contracts.tsv)：

- `H0`：无介入；
- `H1`：安全、退出权、预登记便利或纯设备恢复；
- `H2`：逐字重读任务或指出已经可见的通用说明，排除无主持完成指标；
- `H3`：解释核心规则/UI含义，排除完成、学习、迁移与自由复述指标，该Session不计M5理解；
- `H4`：泄露路线、下一行动、权能用法、失败原因、因果答案或版本映射，所有表现/策略/偏好指标无效。

每次介入必须写时间、触发状态、逐字内容、参与者回应、恢复/停止结果和受影响指标。`strategy_hint_count>0`时，`evidence_validity`不能为`valid`。主持人需要逐帧、逐句解释才可继续时，应停止该版本，不继续消耗样本。

## 7. 不适、退出、隐私与删除

- 参与者说停、表示不适、出现严重疲劳、晕动/闪烁风险、隐私意外、坏档或不可恢复输入时立即暂停录制与Build。
- 主持人先确认安全与退出意愿，不追问敏感原因；`withdrawal_reason_category=declined_to_say`是合法完整记录。
- `moderate/severe`不适、敏感数据事件、P0、坏档或状态hash漂移必须进入`adverse_event_ref_and_sha256`，Session为`withdrawn/aborted`并交QA/隐私责任者复核。
- 删除请求优先于研究便利；原始录像、语音、日志和转录按同意与保留策略处理，状态写入`deletion_request_state`。不得为了保住样本劝参与者撤回删除请求。
- 报告只使用聚合结果和同意范围内的必要匿名片段；禁止在Candidate文档里粘贴可识别原始录像、语音或自由文本。

## 8. 必须绑定的行为与证据

每个`completed/withdrawn/aborted`实例至少绑定：

- 任务结果、行为路线、输入/撤销/提交、提示与主持介入；
- 结构化遥测和状态hash报告；若参与者未同意遥测，只能保留明确获同意的更小范围，不能声称相关指标成立；
- 先自由复述、后定向题、再盲态偏好的顺序证据；
- 完成/partial/withdraw/abort、方案族、误操作、因果题、迁移题、身体感、代理权、疲劳、不适和退出方式；
- 同意范围内的录像/语音或`none`，以及每个实际保存artifact的SHA-256；
- 已知问题、无效原因、被排除指标和不可推论边界。

Artifact ref可以是包络允许目录中的相对路径，或受限证据库opaque ref；凡非`none`都必须有小写64位SHA-256。hash只证明内容未漂移，不证明内容真实、合规或足以过门。

`candidate_human_playtest_session_v1`的行hash规范为：取Schema定义的全部字段，排除`session_payload_sha256`本身；以字段名为key、原始TSV字符串为value构造对象；UTF-8编码，JSON key字典序，`ensure_ascii=false`，分隔符为`,`和`:`且无额外空白；最后计算小写SHA-256。任何字段更正都必须生成新hash并走`supersedes_session_instance_id`，不能原地覆盖已消费行。

## 9. 证据判定

一场Session只有在以下全部为`pass`时，才能写`evidence_validity=valid`：

1. `artifact_integrity_result`：所有必需文件存在、hash一致、同一Session时间线闭合；
2. `frozen_binding_result`：Build、规则、地图、教程、UI、Case与Preflight完全一致；
3. `authorization_binding_result`：Session发生时human_run包络、回执、预算/人数上限和Preflight有效；
4. `privacy_compliance_result`：采集不超同意，联系数据分离，访问/保留/删除符合快照；
5. `first_exposure_result`：若Case要求冷启动/回访，样本分类与暴露声明吻合；
6. 没有H4；H2/H3污染的指标已列入`metric_exclusion_ids`；
7. 没有未处置P0、严重不适、隐私事件、状态漂移或任务脚本越权。

`needs_review`不能计过门；`invalid`只保留失败原因；`withdrawal_only`只能支持退出、安全或可用性诊断，不能支持完成、理解、趣味、策略或偏好。批次聚合前必须按`prototype + build + rules + map + case + participant cohort`分组，禁止把不同版本人数相加。

## 10. 用户裁决边界

Session行固定写`claim_boundary=evidence_only_no_user_acceptance`。QA/主策可以判定证据有效、建议`candidate_for_review / revise / retire_or_merge`，但不能把`completed`、阈值达标、内部PASS或多数偏好写成玩法批准。

只有以下链条完整后，`acceptance-evidence-registry.tsv`才可消费真人证据：

~~~text
valid Session instances
-> 预注册批次聚合（含失败与排除样本）
-> 指定 evidence_id / build / rules / map / cases / source hashes
-> 明确 claim_allowed / claim_forbidden
-> 用户看到同一证据包并作范围化 gameplay 裁决
-> 真实 receipt ref + sha256 + locator
~~~

用户可以保留、返修、淘汰或只批准有界迁移；沉默、试玩时的口头反应、方向回执和Session偏好都不是用户验收。单一Build回执不得外推到未测试角色、章节、视觉、资产、全游戏平衡或Current Runtime。

## 11. 当前零状态与验证

当前合同故意保持：

| 项 | 当前值 |
| --- | ---: |
| 真人参与者 | 0 |
| Session实例 | 0 |
| 已授权human_run包络 | 0 |
| 已通过human_run Preflight | 0 |
| 真人结果 | `not_run` |
| 用户玩法裁决 | `none` |

运行：

~~~bash
python3 docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/scripts/check_d10_human_playtest_sessions.py
python3 docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/scripts/check_d10_human_playtest_sessions.py --self-test
~~~

普通PASS只证明：112字段实例Schema、原39字段crosswalk、5级提示合同、33个非自动Case的证据账入口与当前零状态互相一致。它不证明已经有参与者、同意、Build、Session、M5/M6、玩法有趣或用户批准。
