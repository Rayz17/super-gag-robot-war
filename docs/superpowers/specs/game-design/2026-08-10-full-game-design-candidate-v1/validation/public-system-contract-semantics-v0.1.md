# 公共系统合同语义校验 v0.1

> Status: `candidate_static_contract / zero_build / human_evidence_not_run / user_acceptance_pending`

这个校验只回答七项公共玩法合同是否在 Candidate 表之间自洽，不代表 Godot Runtime 已实现、任何章节已可玩、人类已试玩或用户已验收。

校验范围：

1. 结算只消费 Owner 模式先产生的决定回执；Operation 结束时后台保留 Encounter 事实 proposal 与 Operation proposal 两层，前台却只显示一个合并摘要和一个最终“继续/提交”，不得连续要求两次批准；Chapter 仅在真正章末单独显示；
2. 标准 Hub 周期固定 3 个 `time_slot`、最多 3 张 `work_card`；同格全部卡先整组 preflight，再作为一个 `HUB_SLOT_COMMIT` 原子提交，生成单一 slot receipt 且时间只推进一次；2–5 个 `issue_group` 仅是 UI 候选事项组；
3. `RES_REPAIR_CAPACITY` 只表示维修设备容量，周期重建且不结转，并分开 `PRECONDITION_REJECT` 与 `PERFORMED_FAIL`；
4. 战内 `encounter_elapsed_ms` 与长线 `campaign_tick` 分属两个时标，不允许按 8 秒窗数直接换算长线时间；
5. Mission Commitment 在唯一 accepted receipt 内原子提交路线、出击清单、`campaign_tick` 与运营资金，并把 `ST_OPERATION` 从 `offered` 推进至 `committed`；后续持久表达 `traveling / arrived / resolved`、到达刻度和未选处置；
6. `ST_EQUIPMENT` / `SOG-BODY` 在同一 item 记录中唯一保存 `lawful_owner / current_holder / physical_location / loan_terms / transfer_receipt_id / slot / installed_state`；`SYS-ARCH` 与 `SYS-HUB` 只读版本投影或提交转移请求；
7. 出击清单有且仅有任务卡、路线、编队岗位、机体状态、装备保管、权限同意六类版本引用；查看、预演与锁定预览0时间、0资金、0写入。

执行：

```bash
python3 -B scripts/check_public_system_contract_semantics.py
```

通过只表示静态 TSV 合同和字段闭合；上述规则仍需纸模实例、Build 实现、自动化测试与人类试玩分别产生证据。

可用 `--self-test` 运行内存故障注入；当前覆盖实物真值字段、任务承诺生命周期字段、Hub slot group 字段及关键顺序/数量规则的缺失。
