# C01E02｜R2C-C1测试报告

总结果：`PASS`。执行入口：

```bash
./scripts/test_c01e02_m3_golden_slice_g2_a1_r2c_c1.sh
```

环境：macOS 15.7.5（24G624）／arm64／Apple M2 Max；Godot `4.7.stable.official.5b4e0cb0f`。Actual Frame使用非headless OpenGL 4.1 Metal Compatibility窗口；其余机器测试使用headless。

## 专项与冻结合同

| 检查 | 结果 |
|---|---|
| C1 ground occupancy＋A/B R1/R2各20次 | PASS |
| 02／04机器回执结构校验 | PASS |
| R2C contact staging A/B | PASS |
| Performance T2 settle／T3 contact／T4 socket | PASS |
| R2投影、route facing、footpoint、guard、sparse clip | PASS |

## 11项逐一回归

| # | 测试 | 结果 |
|---:|---|---|
| 20 | `g2_a_domain_contract_test.gd` | PASS |
| 21 | `g2_a_session_flow_test.gd` | PASS |
| 22 | `g2_a_ui_interaction_test.gd` | PASS |
| 23 | `g2_a_presentation_asset_test.gd` | PASS |
| 24 | `g2_a1_map_performance_consumer_test.gd` | PASS |
| 25 | `g2_a1_input_overlay_test.gd` | PASS |
| 26 | `g2_a1_strategy_constraint_visibility_test.gd` | PASS |
| 27 | `g2_a1_audio_bus_runtime_test.gd` | PASS |
| 28 | `g2_a1_asset_fail_closed_test.gd` | PASS |
| 29 | `g2_a1_r1_contact_audio_timing_test.gd` | PASS |
| 30 | `g2_a1_r1_real_fixture_consumer_test.gd` | PASS |

## Actual Frame、隔离与Canon

- 两张连续序列Godot root viewport帧：PASS；manifest及PNG SHA逐项回读PASS。
- Candidate Scene直接启动smoke：PASS；无`SCRIPT ERROR`、`ERROR:`或ObjectDB leak。
- 旧R2C证据整树不变：PASS。
- G2-A.2暂停文件SHA不变：PASS。
- 默认入口、save、真实美术、G2-B、Runtime、Canon隔离：PASS。
- `scripts/canon-check-godot.sh --report`：PASS。
- `scripts/canon-check-godot.sh --strict`：PASS。

所有完整标准输出保存在`logs/`，结构化回读保存在`receipts/`、`02-ground-occupancy-proof.json`、`04-determinism-receipt.json`与`05-actual-frame-manifest.json`。

测试结论只证明83号范围内的实现与回归；制作人Actual Frame复签仍为必需门。
