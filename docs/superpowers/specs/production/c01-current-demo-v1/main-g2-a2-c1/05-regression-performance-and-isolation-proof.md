# G2-A2-C1 回归、性能与隔离证明

## 最终 runner

`scripts/test_c01e02_m3_golden_slice_g2_a2_c1.sh` 以最终源码完整通过，未放宽 `SCRIPT ERROR / ERROR / ObjectDB leak` 检查。

涵盖：

- 6 项 G2-A2-C1 专项：路线族、公开 API 玩家链、投影/五组相机、current-topology pre-scene、A4 donor mask、自然序列。
- 9 项 G2-A/G2-A1 基础回归。
- R1 接触音频、R1 真消费者、R2 几何、R2C 接触、R2C 呈现、route-family event-hash isolation、原 R2C-C1 20 次回归。
- 12 张非 headless actual frames、600 帧非 headless 性能窗、隔离检查、Canon report/strict。

所有最终日志扫描为绿。证据：[logs/](logs/)、[35-regressions.log](logs/35-regressions.log)。

## 关键非回归

- B hero 旧签名：R1=`c3b307b9698d645598594cb6674c86779a13420b9934cf562f379d112d1f41fa`，R2=`f09de07bb6b0b32c1a44e7ca1d5e24a6cbc3bac498010cb92490b781bd6480a6`，各 20 次唯一。
- A/B CONTACT、post、socket、T1–T5、R2 动态 3×3 占地、R3 均通过。
- A Swarm01=`[22,9]`，B Swarm01=`[22,8]`；均 1×1、grounded、`deflected_alive`、non-blocking。
- 音频接触边界、skip/fallback 与消费者生命周期未退化。

证据：[r2c-c1-determinism-nonregression.json](receipts/r2c-c1-determinism-nonregression.json)、[r2c-c1-ground-nonregression.json](receipts/r2c-c1-ground-nonregression.json)、[r1-contact-audio-nonregression.json](receipts/r1-contact-audio-nonregression.json)。

## 600 帧非 headless 性能窗

| 项 | 值 |
|---|---|
| 设备 | Apple M2 Max / Mac14,6 / macOS 15.7.5 |
| Godot | 4.7-stable official |
| Driver | opengl3 / gl_compatibility / macOS display server |
| VSync | 0 |
| 分辨率 | 1280×720 |
| Warmup / sample | 120 / 600 frames |
| p50 / p95 / max | 6.123 / 7.641 / 11.344 ms |
| >16.7ms / >33.3ms | 0 / 0 |
| 采样窗 screenshot / capture IO / disk log | 0 / 0 / 0 |
| 重复纹理路径 | 0 |
| Gate | PASS（p95≤16.7ms，max≤33.3ms） |

采样窗保持 rain/wet road/scene clock 非静态；自然序列另行采样，截图 IO 不进性能窗。

证据：[performance-600-frames.json](receipts/performance-600-frames.json)、[50-performance.log](logs/50-performance.log)。

## 执行透明性记录

最终五组相机收口后的首次整链复跑，音频测试本体 PASS，但 Godot 退出阶段一次性报告 8 个 ObjectDB 实例，runner 按硬门停止。原测试独立立即复跑无泄漏，随后最终整链亦无泄漏通过；未屏蔽告警，未改测试或门限。

## 隔离与 Canon

`approved_handoffs=[] / real_art_loaded=0 / default_entry_changed=false / save_enabled=false / runtime_promotion=false / canon_modified=false / g2_b_allowed=false`。

`scripts/canon-check-godot.sh --report` 与 `--strict` 均 PASS。证据：[60-isolation.log](logs/60-isolation.log)、[61-canon-report.log](logs/61-canon-report.log)、[62-canon-strict.log](logs/62-canon-strict.log)。
