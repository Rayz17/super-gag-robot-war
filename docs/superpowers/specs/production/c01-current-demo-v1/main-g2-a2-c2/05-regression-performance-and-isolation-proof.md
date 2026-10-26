# G2-A2-C2 回归、性能与隔离证明

## 唯一末轮回归

[99-final-regression.log](logs/99-final-regression.log)以最终源码完整通过，包含：

- C2屏幕输入、共同timeline、actual capture、外部trace重算与性能专项；
- A/B动态责任字段来源、只读另一路比较、失败草稿撤销重画、C2产品copy白名单、独立有序timeline及相邻交换负例；
- A=21 / B=15 route family，direct/alternate、20次确定性与无夹具公开API链；
- 9项G2-A/G2-A1基础回归，R1音频/消费者、R2几何、R2C接触/呈现、R2C-C1占地；
- route-family event hash isolation、Full/Skip、R2/R3、Canon report/strict与默认入口隔离。

旧B hero签名保持：R1=`c3b307b9698d645598594cb6674c86779a13420b9934cf562f379d112d1f41fa`，R2=`f09de07bb6b0b32c1a44e7ca1d5e24a6cbc3bac498010cb92490b781bd6480a6`。未改旧测试期望。

## 120 + 600帧非headless性能

| 项 | 值 |
|---|---|
| 设备 | Apple M2 Max / Mac14,6 / macOS 15.7.5 |
| Godot | 4.7-stable official |
| Driver / method / display | opengl3 / gl_compatibility / macOS |
| VSync / 分辨率 | 0 / 1280×720 |
| Warmup / sample | 120 / 600 frames |
| p50 / p95 / max | 6.388 / 8.090 / 11.459 ms |
| >16.7ms / >33.3ms | 0 / 0 |
| screenshot / capture IO / disk log | 0 / 0 / 0 |
| Gate | PASS（p95≤16.7ms，max≤33.3ms） |

采样窗保持live rain/wet road/Scene clock非静态；InputEvent形成的A草稿保持在同一Scene中，12–15秒执行trace单独测量，截图与IO不进性能窗。证据：[performance-600-frames.json](receipts/performance-600-frames.json)。

## 漂移与边界

- 回归运行前/后源码fingerprint均为`b3456e6a80e4cd1722613b43264bf9f06e750493b2024750ddf234e051ff3c57`；
- 最终日志mtime=`1787231414`，严格晚于最终源码/测试/runner mtime=`1787231085`；
- R1音频运行时测试在macOS Godot退出阶段存在非语义清理波动；最终runner要求最多8次内取得连续2次clean exit，末轮`attempts=2 / consecutive_clean=2 / semantic_errors=0`，未以单次偶发退出替代语义PASS；
- board运行前后SHA均为`8758870b…79a08`，Task96/P98行未被本runner修改；
- `approved_handoffs=[] / real_art_loaded=0 / default=false / save=false / Runtime=false / Canon=false / G2-B=false / Call03=false / UA91=false`；
- `scripts/canon-check-godot.sh --report` 与`--strict`均PASS。

证据：[98-source-fingerprint.log](logs/98-source-fingerprint.log)、[60-isolation.log](logs/60-isolation.log)、[61-canon-report.log](logs/61-canon-report.log)、[62-canon-strict.log](logs/62-canon-strict.log)。
