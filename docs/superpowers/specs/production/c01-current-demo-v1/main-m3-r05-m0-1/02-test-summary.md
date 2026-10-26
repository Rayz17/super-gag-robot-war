# C01E02 M3-R0.5 M0.1 测试摘要

最终总门：`PASS`。执行入口：`scripts/test_c01e02_m3_r05_m0_1.sh`。每个 Godot 子进程由 `scripts/run-godot-with-timeout.sh` 施加 60 秒硬超时；超时返回非零，不计 PASS。

| 门 | 结果 | 证据 |
|---|---|---|
| PID 16942 挂起清理 | `FAILED_INVALID_NOT_A_PASS`，TERM 后退出 | `00-ui-flow-hang-incident-receipt.json` |
| 有界 UI flow 复跑 | PASS，0.64 秒，exit 0，无残留 | `00-ui-flow-hang-incident-receipt.json` |
| 有界 M0.1 身份专测复跑 | PASS，0.45 秒，exit 0，无残留 | `00-ui-flow-hang-incident-receipt.json` |
| 更新后 40 frozen ledger | 全量 PASS | `logs/01-frozen-ledger.log` |
| media packing v2 | PASS，visual=28，audio=16，probes=0 | `logs/10-media-packing.log` |
| M0.1 identity-aware fallback | PASS，critical=9，blockers=13，probes=0 | `logs/11-m0-1-identity-aware-fallback.log` |
| M0 presentation contract | PASS，fixtures=3，modes=3，probes=0 | `logs/12-m0-presentation-contract.log` |
| M0 UI flow | PASS，Qihai visible，1280x720 | `logs/13-m0-ui-flow.log` |
| 非默认场景直接启动 | PASS，无 Godot error | `logs/14-direct-scene-smoke.log` |
| 五张 M0.1 捕获 | PASS，全部 1280x720、非空、zero real asset | `logs/20-capture-*.log` |
| R0 shared-round contract | PASS，2 success / 1 failure / 60 replays | `logs/30-r0-shared-round.log` |
| R0 playable flow | PASS | `logs/31-r0-playable-flow.log` |
| 默认 startup | PASS，仍为 `C01CDV1-M2-R2` | `logs/32-default-startup.log` |
| M2 core | PASS，20 replays | `logs/33-m2-core.log` |
| M2.5 A4/A5 atlas | PASS | `logs/34-m2-5-a4-a5.log` |
| V35 layered pipeline / current-demo contract | PASS | `logs/35-v35-layered-pipeline.log`, `logs/36-current-demo-contract.log` |
| 全量 Godot regression | PASS，最终命令 exit 0 | `logs/40-full-godot-regression.log` |
| Canon authority / smoke / Godot report / strict | 全部 PASS | `logs/50-*` 至 `logs/53-*` |
| 旧 M0 证据保护 | PASS，前后 tree digest 均为 `c9c4578...2991f` | `logs/00-*`, `logs/61-*` |

专测覆盖了双方 footprint/pivot、馆守Z双完整前臂与右肩旧伤、BREAKER 单红缝/闭胸缝/封背出口、九槽 fallback、manifest 开关无授权能力、精确角色标签、七海零动作权、兜灯原句先于输入、应急车无医疗十字，以及零 gameplay 结果变化的冻结回归。

最终系统检查：无 `godot.*m3_r05` 残留进程。
