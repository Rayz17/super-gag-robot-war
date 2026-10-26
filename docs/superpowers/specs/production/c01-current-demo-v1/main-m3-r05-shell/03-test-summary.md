# C01E02 M3-R0.5 M0｜测试摘要

> 日期：2026-08-18
>
> 结论：M0 零资产表现壳机器门与视觉证据通过；不构成真实 handoff 或 R1 ready。

| 门 | 结果 | 证据 |
| --- | --- | --- |
| 更新后 40 ledger | PASS | `logs/00-frozen-ledger.log`，含 41-44 与冻结 R0/A4/A5/Reader 输入 |
| 42 packing validator | PASS | `C01E02_M3_R05_MEDIA_PACKING_OK visual=28 audio=16 probes=0` |
| Manifest 负向夹具 | PASS | 坏 hash、错 Stable ID、路径逸出、symlink、错尺寸、错帧、错音频、错 build/profile 均拒绝 |
| 三草案冻结 | PASS | Main `6262…8fa`；Prepared `51fd…8adc`；Failure `be7b…e209` |
| Full / Skip / fallback | PASS | 三草案逐字段 semantic 等价，final visual state 等价，玩法 hash 前后相同 |
| B03-B08 | PASS | 固定顺序；每 beat started/finished；每主体结算 1 次；道路 process + final 双槽消费 |
| 中间视觉状态 | PASS | 首帧非 final snapshot；所有采样帧 `gameplay_write_count=0` |
| 两个成功解差异 | PASS | presentation plan、camera、reaction、sampled frame tracks 均不同 |
| 失败解释 | PASS | 摘要首条警告与执行首条 failure reason 相同 |
| 通讯 trigger_once/reset | PASS | 同轮单次；reset 后可再次触发 |
| 44 七海 presence | PASS | 恰好一次；remote/decision；无台词、按钮、命令或炮火权；0 probe |
| 40×20 / 32×18 | PASS | 七个锚点 roundtrip 与冻结坐标一致；新壳无 30×15 投影 |
| 1280×720 UI | PASS | 七海卡不遮棋盘、时间线或确认按钮；正常捕获不含开发回执 |
| F3 | PASS | 默认隐藏，可切换；显示 hashes、packing receipt 与 beat receipts |
| 零 handoff | PASS | `approved=0 validated=0 loaded=0 probes=0 runtime_art_loaded=false` |
| 直接场景 smoke | PASS | 无 `SCRIPT ERROR`、parse/compile error 或 runtime error |
| 冻结 R0 | PASS | shared-round + playable-flow；60 次 replay、结果与输入冻结 |
| 默认 startup | PASS | `default=C01CDV1-M2-R2` |
| M2 | PASS | `C01_CURRENT_CANDIDATE_M2_CONTRACT_OK` |
| M2.5 / A4-A5 | PASS | `C01_CURRENT_CANDIDATE_M2_5_ATLAS_OK`；40 ledger A4/A5 receipts OK |
| V35 / current-demo | PASS | dashboard current；revision-2 contract check OK |
| Canon | PASS | authority、smoke、Godot report、strict 全部通过 |
| 全量 Godot regression | PASS | `logs/40-full-godot-regression.log`，最终 `SCENARIO_DRIVER_REGISTRY_SMOKE_OK` |
| PNG 视觉检查 | PASS | PLAN_EDIT、PLAN_SUMMARY、FULL_RESULT、DEBUG_OVERLAY 均逐张检查，无重叠/空白 |
| AVI 检查 | PASS | 1280×720、30fps、968 帧、32.266667 秒；16 秒中间帧为 B04 共同结算且非空 |

## 音频边界

42 的真实音频合同为每槽 `wav_pcm_s24le / 48000 Hz / exact channels-duration-loop`，manifest 与 validator 已严格覆盖。当前只有 48k 程序合成 fallback；Godot AVI 载体为 48k stereo PCM16，不是 A7 24-bit exact handoff 证据。

## 未通过声明

本测试没有证明 43 所列的一般共同回合因果、可编辑路线/waypoint、完整 commit summary、派生 mutation/settlement 或真实 route hash。
