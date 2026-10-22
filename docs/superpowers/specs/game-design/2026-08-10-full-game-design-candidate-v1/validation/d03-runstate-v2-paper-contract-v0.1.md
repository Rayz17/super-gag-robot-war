# D03 RunState v2／StateTransaction v2 最小纸面合同 v0.1

> Status: `candidate_typed_wire_contract / zero_build / human_evidence_not_run`
>
> Authority boundary: 只约束本 Candidate 包的未来实现与迁移验收；不改 Current Canon、Reader、story-chain、现有 Godot Runtime 或 C01E02 Demo。

## 1. 本轮真正补了什么

此前 `system-state-contracts.tsv` 已经说明 26 个状态域“至少要保存哪些字段”，但还不足以交给实现：没有统一线格式、字段类型、未知字段策略、领域 bucket、记录版本、字段级删改、事务 op 语义和可执行 owner／幂等检查。本轮把它们补成以下机器合同：

- [47项枚举与线类型](../data/runstate-v2-enum-type-registry.tsv)：包含禁止 JSON float 的小数串、稳定 ID、版本、时间、Hash、容器和核心枚举；
- [35种记录 Schema](../data/runstate-v2-field-schema.tsv)：9种共用记录与26种状态记录，覆盖现有 `system-state-contracts.tsv` 的全部215个 `minimum_fields`；
- [26域映射](../data/runstate-v2-domain-registry.tsv)：给每个状态域绑定记录类型、唯一 owner group、记录主键、合法 op、持久性、投影策略和 v1 适配风险；
- [7种事务操作](../data/state-transaction-v2-op-schema.tsv)：创建、补丁、完整替换、关闭、资源差分、事件追加和唯一物件转移；不提供物理删除；
- [4个R0/P1纸面案例](../data/runstate-v2-r0-p1-fixture-coverage.tsv)及其[确定性输入](../data/runstate-v2-r0-p1-fixtures.json)；
- [独立检查器](../scripts/check_d03_runstate_v2_contracts.py)，含15项内存故障注入。

这只是“实现前可执行规格”，没有新增 Godot 类、存档迁移器、运行时事务或 UI。

## 2. 对现有 Godot v1 接口的只读审计

审读对象是当前 `game-godot/scripts/core/state/run_state_store.gd`、`state_transaction.gd`、`outcome_validator.gd` 与 `autoload/save_service.gd`；本轮未修改它们。

现有技术种子可以保留：

- `transaction_id` 去重与回执；
- snapshot／restore；
- Episode稳定边界存档；
- facts、实体、世界对象、权限、关系、债务、资源和活动结果的通用差分壳。

但 v1 不能被称为全游戏状态系统：

1. `RunStateStore.SCHEMA_VERSION = 1`，九个业务字典没有每域 Schema、记录主键、owner 或领域版本；
2. `_apply_diff()` 在生成 accepted receipt 前直接改写字典，没有多 owner prepare、expected revision、proposal hash 或统一0写入拒绝路径；
3. `world_facts`、`episode_memory`、`inventory_and_resources` 等容器混合多个产品语义，无法可靠自动拆出 Knowledge／Evidence／Roster／Body／Collection；
4. `StateTransaction` 只有四个头字段和通用 outcome，未约束完整记录、版本、字段类型、唯一物件或资源算术；
5. snapshot/restore 只检查 schema version，没有逐记录验证、迁移策略、字段级观察者投影或后台删改；
6. `SaveService` 能稳定写 JSON，但 v1 数字和任意 Dictionary 仍允许跨平台浮点／未知字段漂移。

所以 v2 采用“显式适配或拒绝”，禁止把 v1 字典直接改名后宣称迁移完成。

## 3. RunState v2 线格式

根对象固定包含：

```text
schema_id = run_state_v2
schema_version = 2
run_id
state_revision
run_status
authority_boundary = candidate_only_zero_build
last_stable_checkpoint_id
world_clock
domain_versions{state_id -> nonnegative integer}
domains{state_id -> DOMAIN_BUCKET_V2}
transaction_ledger{transaction_group_id -> COMMIT_RECEIPT_V2}
commit_order[]
```

每个 bucket 必须重复声明 `state_id / owner_system / owner_group_id / domain_version`；每条记录除领域字段外还必须有：

```text
_record_version
_last_transaction_id
_source_authority
_visibility_scope
_observer_ids[]
_redact_fields[]
extensions{}    # 唯一允许的扩展入口
```

根、bucket、事务、回执都拒绝未知字段；领域记录只允许把尚未升入正式 Schema 的值放入 `extensions`。任何 `backend_*` 扩展若不是整条 `backend_only`，必须在 `_redact_fields` 中列出路径。

### 3.1 为什么不用 JSON float

资源余额、比例和置信度都用规范十进制字符串。这样 proposal hash、存档重放和跨平台比较不会被二进制浮点或 `NaN/Infinity` 破坏。机体能源／热量仍允许对象或整数，因为其产品模型尚未定型；但其中同样禁止 float。

### 3.2 两个显式非事务域

- `ST_IDENTITY`：只允许经批准的设计迁移改变，普通玩法事务无权写；
- `ST_UI_PROJECTION`：只由 `SYS-PRESENT` 从已提交快照派生，不能反写权威状态。

余下24域必须落到 `settlement-owner-prepare-commit-contracts.tsv` 的十个 owner group 中，检查器逐项验证没有漏组或双 owner。

## 4. StateTransaction v2 提交顺序

一个事务固定包含 `transaction_group_id / proposal_hash / expected_state_revision / required_owner_groups / operations / future_consumers / player_summary` 等头字段。合法提交顺序是：

1. 用不含 `proposal_hash` 本身的规范 JSON 计算 SHA-256；
2. 验证 `expected_state_revision`；
3. 每个被触及领域的 owner 对同一个 proposal hash 产生 `PREPARED_OWNER_RECEIPT_V2`，只校验不写状态；
4. 每个 op 必须且只能被自己的 owner group 接受；资源还必须有 `domain_owner_system` 对应的 prepared owner；
5. 所有 op、版本、当前记录 hash、算术、唯一身份和删改路径全部通过后，`SYS-SETTLE` 在副本上执行；
6. 全组成功才把 `state_revision` 加1、各被触及 domain version 加1并生成唯一 commit receipt；
7. 任一失败返回原因码并保持原快照规范字节不变；
8. 重放相同 `transaction_group_id + proposal_hash` 返回原 receipt；同 ID 不同 hash 拒绝为幂等冲突。

不提供 `DELETE_RECORD`。已发出的许可、同意、路线、债务和结果以 `OP_CLOSE_RECORD` 关闭并保留审计史；唯一物件使用 `OP_TRANSFER_UNIQUE` 改变同一 record 的 owner／slot，不能复制成第二条。

## 5. R0／P1最小案例

| Fixture | 层 | 结果 | 覆盖 |
| --- | --- | --- | --- |
| `FX-RS2-R0-ATOMIC` | R0 | accepted + replay | 三owner、创建事实、身体补丁、材料差分、唯一物件转移、结果事件追加、玩家投影 |
| `FX-RS2-R0-MISSING-OWNER` | R0 | rejected / zero-write | 缺 `SOG-BODY` 时不修身体、不转物件、不扣材料、不生成 accepted receipt |
| `FX-RS2-P1-C2-REDACTION` | P1 | accepted + replay | Contact完整替换、Consent关闭、指挥带宽差分、observer投影、后台精确身份字段删改 |
| `FX-RS2-P1-STALE-REVISION` | P1 | rejected / zero-write | proposal与owner回执一致但 expected revision 过期，整组拒绝 |

两条 accepted 案例覆盖全部7种 op；两次立即重放都保持状态规范字节与 revision 不变。P1投影允许玩家看到 `reported_type / confidence`，但不得出现 `backend_exact_identity` 的值。

## 6. 检查命令与当前证据

```bash
python3 -B scripts/check_d03_runstate_v2_contracts.py
python3 -B scripts/check_d03_runstate_v2_contracts.py --self-test
```

基线预期：

```text
D03 RunState v2 PASS: 47 types, 35 typed record schemas, 26 state domains, 7 transaction op kinds, 4 R0/P1 paper fixtures (2 accepted + replay, 2 rejected zero-write); zero Build/human evidence
```

故障注入覆盖：未知类型、owner漂移、领域字段漏型、op互映漂移、JSON float、proposal hash、缺owner、owner接受错误op、后台泄漏、资源不守恒、idempotency key、未知根字段、重复op、Build证据冒升和revision证据冒升，共15项。

## 7. 仍未完成，不能据此宣称什么

本合同仍没有证明：

- Godot v2 store／validator／projection／save migration 已实现；
- v1九个字典能无损自动迁移；实际上多数域明确标成 `no_safe_automatic_split`；
- 崩溃、磁盘损坏、跨版本升级、并发提交或性能预算通过；
- R0/P1已形成可玩 Build，或真人理解、趣味、策略空间成立；
- C01–C03的215个字段都有正式实例数据；本轮只证明字段类型与最小R0/P1样例；
- 经济数值、时制、Contact UX或结算页面已获用户批准。

进入实现前仍需用户批准精确执行包络；实现顺序应是：只读 v1 adapter 与迁移报告 → v2 strict validator → copy-on-write prepare/commit store → projection service → 存读档与崩溃恢复测试 → R0/P1 Build。任何一步都不得反向修改 Current 内容来迎合适配器。
