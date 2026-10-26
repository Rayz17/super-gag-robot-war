# C01 电影化斜侧视壳层主程序状态 v1

> Goal ID：`GOAL_C01_RM_MAIN_PERSPECTIVE_TRIAL_V1`  
> Contract：`C01_RM_2P5D_PERSPECTIVE_TRIAL_V1`  
> 当前状态：`main_program_validated_awaiting_joint_acceptance`  
> 日期：2026-07-14

## 结论

主程序透视试制已完成实现和独立验证，建议进入程序/美术联合验收。这个结论只说明新壳层可玩、可回退、可测试，不批准 Phase B，不升级为全项目正式 2.5D 模板。

## 可回退基线

- 旧基线场景：`res://scenes/c01_real_machine_rescue_validation.tscn`
- 旧基线脚本：`res://scripts/c01_real_machine_rescue/c01_real_machine_rescue_validation.gd`
- 旧验收证据：`outputs/c01-real-machine-rescue-v01/`
- 直接回退：显式启动旧场景；新试制未删除或覆盖旧入口。

## 新试制入口

- 当前默认场景：`res://scenes/c01_real_machine_rescue_perspective_trial.tscn`
- 世界/视口：`1920x900 / 1280x720`
- 相机区：`ZONE_A_ENTRY / ZONE_B_REAL_MACHINE / ZONE_C_OLD_DOOR_LOW_HEAT`
- 当前壳层：明确标注的几何占位；不加载任何 `runtime_allowed=false` 美术产物。

## 程序验证

- Godot 全量 smoke：23/23 通过。
- 新透视 smoke：旧基线完整路径、新壳层完整路径、新壳层全跳过路径的 preview outcome 一致。
- 镜头回位：当前构图区误差不超过 2 px，`zoom=(1,1)`，`offset=(0,0)`，无残留所有权。
- Canon：`canon-check-godot --strict` 和 `canon-smoke-test` 通过。
- 性能：A/B/R3 三段稳态约 99 FPS，p95 约 15.5 ms，0 帧超过 20 ms。
- 转场：配置 0.56 s，实测 0.567 s，正确落点。
- 导出：18 MB PCK 通过 17 项资源和默认场景验证。

## 美术同步状态

Phase A.5 的五个 review 文件、独立 manifest、精确 metrics 与美术完成报告均已在工作区出现，美术权威状态为 `ready_for_joint_acceptance`。主程序已按共同合同对齐 `1920x900` 世界、`GROUND TURN Y=410`、三区 X 中心、脚点、人物高度、安全区和分层职责；所有 A.5 资产仍为 `runtime_allowed=false`，运行时没有加载它们。

当前只剩一项明确的联合裁切选择：A.5 metrics 使用相机中心 `Y=450`，几何试制使用 `Y=400`。后者使当前占位地面行动带严格落在屏幕 `Y=430-650`；前者对应正式 clean plate 的 `[0/320/640, 90, 1280, 720]` 裁切。这个 50 px 差异应在正式纹理导入前由联合验收决定，不影响本轮主程序 PASS，也不得被写成已经像素级一致。

## 当前门禁

- `main_program_complete=true`
- `recommend_joint_acceptance=true`
- `phase_b_generation_allowed=false`
- `formal_template_promoted=false`
- `art_status_handoff_pending=false`
- `joint_camera_y_choice_pending=true`

完整证据、对齐表和剩余债见 `main-program-perspective-trial-completion-report-v1.md`。
