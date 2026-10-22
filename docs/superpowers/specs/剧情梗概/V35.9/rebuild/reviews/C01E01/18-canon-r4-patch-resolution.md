# C01E01 Canon r4残留补丁关闭记录

> Status: `patched_pending_independent_targeted_r5`
>
> Scope: 只关闭`17-canon-targeted-recheck-r4.md`的`R4-P01`、`R4-P02`、`R4-P03`；不改Story Core，不代替独立PASS。

## 1. R4-P01：馆守Z右臂动作不再从高层合同回弹

- 在`build_v35_8_slot_loadout.py`中为`V357-C01-S02 + V353U001`增加槽位级角色与签名覆盖。
- 重新生成后，`V358U002-06`、`V358ACT002-06`、`V358GAME002`、`V358LOAD002`统一为：
  - 馆守Z保持半跪断电；
  - 右臂核心保持连接；
  - 仅提供被动温度传感与一段冷却继电；
  - 不开胸灯、不抬肩、不飞拳、不形成断臂地形。
- `DOC_V31_C01E02_PACKET`、`N_V31_C01E02_PACKET`和原右臂桥相关图谱边已显式降为历史来源，并增加指向V35.9 C01重构地图的`superseded_by`重定向。
- `canon-query.sh 展柜飞拳单元`现在只把V31材料作为`historical_superseded_episode_packet`返回；当前实体首伏笔、正式出现和首战均锁在`V355-C01E03`。

## 2. R4-P02：Graybox取消第二持久提交

- `GB014`改为`local_round_receipt`，明确三回合内回执不写Episode持久状态。
- `GB019`只满足本地`Battle Clear`，不写持久状态。
- `RT011`仍为非持久战斗Clear；`RT013S`仍是消防路由捕获、四令接管完成后的唯一持久事务。
- 因此不存在“29人状态先提交、四令和物理快照后提交”的半套中间态。

## 3. R4-P03：Canon smoke迁到当前事实

- 旧六回合场景断言改为验证`historical_runtime_reference`，不再把历史文本当作当前流程。
- 七海零号后解锁断言改为`qihai_official_risk_channel_unlocked`。
- 七海实体行断言改为当前现场监督/流程口径。
- 脚本已完整跑至末尾并输出`Canon smoke test passed`。

## 4. 本轮实际验证

| 检查 | 结果 |
|---|---|
| `python3 -m py_compile scripts/build_v35_8_slot_loadout.py` | PASS |
| `python3 scripts/build_v35_8_slot_loadout.py` | PASS；生成95槽、609单位/动作/资产行 |
| `python3 scripts/check_v35_8_slot_loadout.py --max-errors 80` | PASS |
| `scripts/canon-check-godot.sh --strict` | PASS |
| `scripts/canon-smoke-test.sh` | PASS；完整运行到末尾 |
| V35.8四张关键表、Runtime/Graybox、图谱三表列宽 | PASS；无异形行 |
| `git diff --check` | PASS |
| `canon-query.sh 展柜飞拳单元` | PASS；当前E03口径与V31历史来源明确分层 |

## 5. 独立放行门槛

原Canon / 宏观谜团 / 物理连续性审稿席必须只针对上述三项重新取证，并复核r4所列7条转PASS门槛。只有其独立结论为`PASS`，C01E01才可转为`accepted_story_audience_production_canon`并生成C01E02继承包。
