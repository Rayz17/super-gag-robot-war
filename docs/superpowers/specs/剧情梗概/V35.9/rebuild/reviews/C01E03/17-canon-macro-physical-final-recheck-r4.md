# C01E03 Canon / 宏观谜团 / 物理连续性最终复核 r4

> **结论：PATCH**

## 阻断证据

- **CMR4-01｜`canon-smoke-test.sh` 当前不可通过。** `scripts/canon-smoke-test.sh:52-56` 查询历史实体 `封存无人机` 后，`:54` 强制匹配 `安静的流程执行单位`；但 `docs/superpowers/specs/data/canon/entities.tsv:54` 的当前 `role` 是 `已锁美术但当前Story-First未排期的法务执行单位`，`implementation_policy` 仅保留 `安静流程语气`，查询结果不存在前一整句。实跑 `scripts/canon-smoke-test.sh` 稳定 `exit 1`，且 `bash -x` 精确停在 `scripts/canon-smoke-test.sh:54`。**最小修复：** 将 `:54` 的断言改为现行 Canon 中稳定存在的历史边界字段/值（优先 `current_story_first_unscheduled` 或当前完整 `role`）；不得为迎合测试改写 Canon 语义。修复后重跑四项检查。

## 其余复核证据

- **CMR3-01 已闭合：** `PB-V357-C01-S04.md:14,22,34` 唯一完整继承 RT035 精确 27 键，并明确五人、豪司及两件消防货物已安全，E04 不再重开人数/货物判定。
- **CMR3-02 已闭合：** `scripts/canon_query.py:45-63,293-303` 已加入默认历史过滤、`history` 显式模式及 scene 精确 ID 优先；默认查询 `scene V31-C01E03-BATTLE` 与 `entity MECHA_APPROVAL_HAMMER_SUPPORT` 均无结果，显式 `history` 查询可精确返回历史记录。V31 审批锤/责任签名链未泄漏为当前事实。
- **CMR3-03 已闭合：** `scripts/build_v35_8_slot_loadout.py:1526-1555` 将 S03 三个回归单位修正为既有生命周期前态后的 `return`；生成表 `v35_8_lifecycle_event_review_v35_8.tsv:18-20` 同步一致，`scripts/check_v35_8_slot_loadout.py:2903-2905` 已拒绝把 `return` 计为首现。
- **RT035 / E04：** Episode、V35.5 E03 outgoing、V35.5 E04 incoming、slot commit 与 Canon E03 unlocks 均为同序、唯一的精确 27 键；未发现摘要拼接或第二继承源。
- **人口与生命周期：** checker 实证 `inherited5 + Haosi = peak6, bridge5`；馆守Z/勇拳/白函及右臂五态均通过生命周期与物理连续性校验。
- **桥体与谜团边界：** L2-L1 复合桥 owner/contact 链、4.2m 锚点、回滚图与 E04 handoff 均闭合；未发现 Index 人格化、白函二阶段身体、豪司/勇拳/金印时序或宏观谜团提前解释。
- **当前四项实跑：** `canon-check-godot.sh --strict` PASS；`check_v35_8_slot_loadout.py` PASS（95 slots）；`check_c01e03_runtime_graybox.py` 全项 PASS（含人口、五态、复合桥、RT035 27 键）；`canon-smoke-test.sh` FAIL（`exit 1`，即 CMR4-01）。

**最终：PATCH。**
