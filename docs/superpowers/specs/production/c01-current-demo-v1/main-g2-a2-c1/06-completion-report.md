# C01E02 G2-A2-C1 / Task93 完成回执

日期：2026-08-20  
任务：`89 / G2-A2-C1 Current-Topology与无夹具Golden Turn`；`93 / 连续非headless玩家链证据纠偏`  
最终状态：**Task93 Candidate 证据、全回归与交付哈希已收口；Task89 重新停在 producer P89 reacceptance gate。**

## 已完成

1. R1 成功边界保持 88 冻结的等价最短路线族：A=21、B=15；hero、直接终点 BFS、另一同族路线与负例证据均保持通过。
2. A/B 各新增一条同一非 headless 1280×720 Scene 内的连续玩家链，从实际 `PUBLIC_SITUATION` 开始，公开 Session API 动作跨真实 process frames 依次完成 append、facing、action/reaction、summary、return、undo、redraw、二次 summary 与 0.7s hold commit，再由 PerformanceDirector 自然播放 T1–T5 到 `ROUND_RESULT`。
3. 连续链主时钟只取 `Time.get_ticks_usec`，帧号只取 `Engine.get_process_frames`；每条链锁定单一 Scene/Session/Director instance id，未复用 adapter trace clock 或 `add_plan_time`。
4. 外部 validator 从原始 trace 数组重算生命周期、总时长、hold、commit、事件时序与动作间隔，不采信驱动自报 PASS。
5. 责任预演、current topology、唯一 projection、六层注册、CompoundMapActor、局部遮挡、雨/湿地/FX、中性分类 Proxy 与 A/B CONTACT 分路均未改动。
6. A4 仍仅作 fixture/material donor；`approved_handoffs=[] / real_art_loaded=0`。
7. 11 张必需 actual frames + 1 张 B CONTACT 补充帧及其 manifest 原样保留；Task93 未重抓、未改图，manifest SHA 仍为 `0b7ef06c…f06ab`。
8. 旧 `natural-sequence.json` 已明确降级为 `DIRECTOR_AND_VISUAL_REGRESSION_ONLY`，其准确 Director 时长为 A/B 各 5.8s；旧 manifest 内 natural-sequence 字段只保留视觉/事件历史资格，不再作为45–75秒完整玩家链权威。
9. 最终 120 warmup + 600 sample 非 headless 性能为 p50=6.107ms、p95=6.960ms、max=7.841ms，采样窗 screenshot/IO/log write=0。
10. 基础回归、R1/R2/R2C/R2C-C1、route-family event-hash isolation、音频边界、性能、隔离与 Canon report/strict 全部通过；运行前后源码指纹均为 `3655df85…170e3`。

## Task93 连续链回读

两条链的状态序列相同：

`PUBLIC_SITUATION → EDITABLE_DRAFT → COMMIT_SUMMARY → EDITABLE_DRAFT → COMMIT_SUMMARY → JOINT_RESOLUTION → ROUND_RESULT`

| 策略 | 外部重算总时长 | hold | hold帧数 | 最大相邻动作间隔 | commit | T1–T5 |
|---|---:|---:|---:|---:|---:|---|
| A | 46.514334s | 702.700ms | 111 | 4003.252ms | 1 | 均晚于 commit，顺序完整 |
| B | 46.536997s | 705.814ms | 113 | 4005.263ms | 1 | 均晚于 commit，顺序完整 |

两者均为 `fixture_load_count=0 / direct_draft_mutation=false / direct_phase_injection=false / authored_by_input=true / preview_execute_same_resolver=true`。这是确定性自动输入节奏证据，不声称真人回放、物理手柄回放或 FUN PASS。

## 非回归硬门

`route_family` 证据保持在 `round_receipt` 与 `plan_summary.route_family`，不进入 T1–T5 event-hashed payload。最终恢复并保持：

- B R1=`c3b307b9698d645598594cb6674c86779a13420b9934cf562f379d112d1f41fa`
- B R2=`f09de07bb6b0b32c1a44e7ca1d5e24a6cbc3bac498010cb92490b781bd6480a6`
- 各 20 次唯一；旧测试期望未改。

Task93 没有修改 route family、投影、相机、geometry、socket、world result、R2/R3、地图代理、12帧内容、真实美术、Default Entry、save、Runtime 或 Canon。

## 最终关键 SHA

| 产物 | SHA-256 |
|---|---|
| `continuous-player-trace-A.json` | `a87c878cff0da73169059fd8e14afb160a776d1af8eeac5a6d52e01d8d61eef7` |
| `continuous-player-trace-B.json` | `432660c562502ae564d1074b0e8dacb48d401c22bb2f90b18dbe3d6fb23373ef` |
| `continuous-player-trace-validation.log` | `fa72479066a408dcc7f4e74e60461a0f75f0e42807535bacba8baafeb73f6a1a` |
| `99-final-regression.log` | `b78af026496ba191c2e7deebafd1dae29e97bea574755f706b06041eff7db411` |
| `g2_a2_c1_continuous_player_trace_driver.gd` | `d704b259202088c41785c38f6d722e2574a79c2ed044a31e720dbd378db9b9e4` |
| `validate_g2_a2_c1_continuous_player_trace.py` | `1e3a2f0f8f724ee79638fab0a07fbd101c505a14dca0cdf7416fc2a8143ab59d` |
| `test_c01e02_m3_golden_slice_g2_a2_c1.sh` | `ae589ce33afc9c2e61c746e652922cb53052096cfc5eb88489cf9e0cc153198a` |
| `actual-frame-manifest.json`（未改） | `0b7ef06c11bdf59642bdd9c81364eca0f72963d064b9f1a6ae35c104ac2f06ab` |

全量文件哈希见 [delivery-hashes.sha256](delivery-hashes.sha256)。

## 证据入口

- [07-task93-continuous-nonheadless-player-trace-correction-receipt.md](07-task93-continuous-nonheadless-player-trace-correction-receipt.md)
- [continuous-player-trace-A.json](receipts/continuous-player-trace-A.json)
- [continuous-player-trace-B.json](receipts/continuous-player-trace-B.json)
- [continuous-player-trace-validation.log](logs/continuous-player-trace-validation.log)
- [continuous-player-trace-supersession.json](receipts/continuous-player-trace-supersession.json)
- [actual-frame-manifest.json](receipts/actual-frame-manifest.json)
- [performance-600-frames.json](receipts/performance-600-frames.json)
- [99-final-regression.log](logs/99-final-regression.log)

`99-final-regression.log` mtime=`1787215448`，最终源码/测试/runner 最新 mtime=`1787215088`，严格晚于；运行前后源码指纹相等。

## 停止门

当前状态：

- `REGISTRATION_SUPPORTED`
- `CURRENT_TOPOLOGY_SUPPORTED`
- `FIRST_READ_SUPPORTED_FOR_LOOKDEV`
- `COMPLETE_CONTINUOUS_PLAYER_TRACE_SUPPORTED_BY_TASK93_CANDIDATE_EVIDENCE`
- `FUN_NOT_PROVEN`
- `CALL02_ALLOWED=false`

本任务停在 producer P89 reacceptance gate。未获制作人重新签收前，不开放 Art Call02、UA91、G2-B、Default Entry、save、Runtime 或 Canon，也不声称 Task89 已被制作人接受或 FUN 已证明。
