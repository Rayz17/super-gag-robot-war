# G2-A.1-R2C 测试报告

日期：2026-08-19  
结论：实现与机器回归PASS；制作人actual-frame验收仍pending。

## 专用链

执行：`scripts/test_c01e02_m3_golden_slice_g2_a1_r2c.sh`

结果：`C01E02_G2A1_R2C_SPECIALIZED_PASS`

- 新R2C contact staging测试：A/B路线、四阶段字段、无重叠／无隔空、socket、T1时序、R1 mutation、R2动态占地、A=`68/1`、B=`88/0`、preview=execute；
- 新R2C presentation测试：A T2 south、B T2 east→T3.25 south、visual recoil→discrete post、BREAKER公开北冲、T4 east side socket、路面共用impact socket；
- R2几何回归：投影、逐段facing、footpoint、binding guard、稀疏clip与最终contact staging通过；
- 11项Golden Slice / G2-A.1既有回归全部通过；
- direct Candidate scene smoke通过；
- 5张1280×720 Godot root viewport实际帧重新生成、逐张读取并校验PNG hash；
- 隔离门通过：non-default、save false、real art 0、G2-A.2 false、G2-B false、Runtime false、Canon false。

关键日志：

- `logs/10-r2c-contact-staging.log`
- `logs/11-r2c-presentation.log`
- `logs/12-r2-geometry-regression.log`
- `logs/13-receipt-validation.log`
- `logs/40-r2c-actual-frame-capture.log`
- `logs/41-actual-frame-validation.log`
- `logs/60-isolation.log`

## 全仓与Canon

| 检查 | 结果 | 日志 |
|---|---|---|
| 全仓Godot smoke suite | PASS | `logs/70-full-godot.log` |
| Godot Canon report | PASS | `logs/71-canon-godot-report.log` |
| Godot Canon strict | PASS | `logs/72-canon-godot-strict.log` |
| Canon authority manifest check | PASS | `logs/73-canon-authority-check.log` |
| V35 layered dashboard current | PASS | `logs/74-v35-dashboard-check.log` |

## 证据边界

机器PASS证明resolver、消费者、测试与隔离合同成立；本任务执行者已做actual-frame可读性复核，但不能替代制作人对接触姿态、代理画面与后续真实合成方向的签收。最终门保持`PENDING_PRODUCER_R2C_ACTUAL_FRAME_ACCEPTANCE`。

