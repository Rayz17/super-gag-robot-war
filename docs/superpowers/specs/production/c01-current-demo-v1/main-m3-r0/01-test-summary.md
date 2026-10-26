# C01E02 M3-R0｜测试摘要

## 总结

`./scripts/test_c01e02_m3_r0.sh`完整通过，最终标记：

`C01E02_M3_R0_ALL_GATES_OK captures=1 full_regression=1`

全部日志位于`main-m3-r0/logs/`。最终日志中没有 `SCRIPT ERROR`、`ERROR:` 或 `push_error`。

## R0 专项

| 检查 | 结果 |
| --- | --- |
| 两种单轮成功草案 | PASS |
| 一种可解释失败草案 | PASS |
| 三种验收草案各 20 次确定性重放 | PASS，合计 60 次 |
| 草案编辑、撤销、摘要不改轮前世界 | PASS，`draft_writes=0` |
| 编辑后公开意图保持冻结 | PASS |
| 同一路线可独立选择不同朝向 | PASS |
| 摘要与执行共用 resolver | PASS，RoundReceipt 逐字段相等 |
| 预备满足条件恰好触发一次 | PASS |
| 预备未触发时轮末失效 | PASS |
| fallback 提交前公开且不赠送行动 | PASS |
| 实体与意图容器反序 | PASS，Receipt 与语义签名不变 |
| 六个结算子系统各推进一次 | PASS |
| 连续光标、摘要返回、长按提交、重置 | PASS |

专项标记：

- `C01E02_M3_R0_SHARED_ROUND_OK successes=2 failure=1 replays=60 reorder=invariant draft_writes=0`
- `C01E02_M3_R0_PLAYABLE_FLOW_OK continuous_cursor=pass summary_return=pass hold_commit=pass save=disabled`

## 成功草案差异

| 草案 | 接触时点 | 预备 | 馆守 Z 承力 | 小体落位 | 路面 |
| --- | --- | --- | ---: | --- | --- |
| 主动作前压 | `T3.00` | 未使用 | 5 | `[21,9]` | `long_broken_arc / 72` |
| 预备守线 | `T3.25` | 触发一次 | 3 | `[22,8]` | `twin_buckles / 80` |

两者都完成“车辆先过、小体侧推存活、馆守 Z 站入责任位、首次正撞偏轴、城市炮命中侧甲、BREAKER 开始聚集红光”。差异来自路线、朝向与动作因果，不是换文案。

错误草案停在`T3.00_UNOPPOSED`：馆守 Z 没有站在撤离线与 BREAKER 之间，界面与回执都明确说明北向冲线无人承担。

## 旧链回归

| 回归 | 结果 |
| --- | --- |
| 默认启动冒烟 | PASS；默认仍是 `C01CDV1-M2-R2` |
| M2 核心合同 | PASS；20 次重放、出口仍为 P1 |
| M2.5 六槽资产 | PASS；`loaded=6 / fallback=7` |
| Current revision-2 checker | PASS |
| 全量 `scripts/godot-test.sh` | PASS |
| `check_canon_authority.py` | PASS |
| `canon-smoke-test.sh` | PASS |
| `canon-check-godot.sh --report` | PASS |
| `canon-check-godot.sh --strict` | PASS |
| `git diff --check` | PASS |
| R0 旧内核/资产/存档 denylist | PASS |

## 尚未证明

- 未经用户真实试玩，不能证明操作学习成本和乐趣；
- 单机 R0 不证明多机编辑、友军争格或反应链负担；
- 不证明完整 E02 两条打法，也没有进入 R1；
- 具名几何只验证信息结构，不代表最终美术、动作、声音或商业表现。
