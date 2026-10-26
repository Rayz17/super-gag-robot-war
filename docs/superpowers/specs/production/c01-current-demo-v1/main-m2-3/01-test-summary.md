# C01E02 M2.3 测试摘要

> Result: `PASS / current default entry rebound / no real art handoff`
>
> Producer objective SHA-256: `2c0aec4b8d83a2c2d534d45240ad346ec649a4771505978051703386e2883cf5`

## 聚焦入口验证

- `python3 scripts/check_c01_current_demo_contract.py`：PASS；`contract_revision=2`、`build_id=C01CDV1-M2-R2`、`save_schema=2` 与冻结 fingerprint 不变。
- `startup_router_smoke_test.gd`：PASS；无参数默认、`m6_validation` feature、`--m6`、`--validation=m6`、`--legacy-perspective` 全部命中正确场景。
- 默认 Candidate Scene 已真实 `load -> instantiate -> start_candidate`；加载后的 Runner 报告 `approved_handoffs=0`、`resource_probe_count=0`、`runtime_art_loaded=false`。
- Current 默认文本链 10 个文件与两条启动脚本均通过 `story_first` deny 检查。
- 无显式 scene 的 `godot --path game-godot --quit-after 8 -- --candidate-no-save` 实际启动探针退出码为 0。
- M6 与 legacy 的无显式 scene 实际启动探针退出码均为 0。

## 启动脚本与 Windows

- `run_c01_candidate_demo_current.sh` shell 语法、执行权限和参数投影：PASS；实际命令为 `godot --path <project> -- --candidate-no-save ...`，通过项目默认路由进入 Current。
- `run_c01_candidate_demo_g1.sh`：PASS；仅转调稳定脚本，没有第二套 Runner 路径。
- 两条脚本的物化自检均保持 build identity 与 materialized snapshot SHA-256 不变。
- Windows preset 0：名称、exe 输出名、产品名、描述均已改为 C01E02 Current Candidate Demo；`custom_features` 仍为空。
- `windows_export_resource_validation.gd`：PASS；检查 91 个资源路径，Current 身份、默认 target、零 handoff、M6 与 legacy inventory 均通过。
- Windows 验证同步接受当前 `MultiPlayPlaytestRecorder` schema 3；未修改 recorder 或 M6 行为。

## M2/M2.2 全量回归

`scripts/test_c01_candidate_asset_r2_m2_2.sh` 在换轨后完整 PASS：

- 14/14 R2 resolver 测试；13 槽全量、单槽、部分坏槽、缺层与坏 receipt 均按预期处理。
- WEST/CENTRAL/EAST 零 handoff 捕获继续与 M2.1 基线字节级一致。
- 20 次确定性重放 PASS，出口仍为 Phase P1。
- CP0、CP1、CP2、PHASE_PENDING、PHASE_STATE 五类 Runner 销毁后落盘恢复 PASS。
- schema/build/fingerprint 错误的旧存档继续 fail-closed，坏存档 SHA 不变。
- M2.1 denylist 16 路径、112 项检查 PASS。
- 全量 `scripts/godot-test.sh` PASS；M6 smoke PASS；旧 Story-First 章节、连续章节、输入、E03/E04 显式回归全部 PASS。
- Canon authority、Canon smoke、Godot report/strict PASS；`approved_runtime_assets_r2` 仍不存在。

## 冻结边界

| 文件 | 最终 SHA-256 | 结论 |
|---|---|---|
| `game-godot/project.godot` | `482437d3830366dc00c97a0e7dd1a5a6806e39e3203df09d1b79d3fd653eac29` | 未修改 |
| `game-godot/scripts/startup_router.gd` | `79bb61c6dafc6635aee850c836db4afdca38527648c3107e28bbb32d71b9262c` | 未修改 |
| `generated/build_identity.json` | `3ceadfee30defad3ed606759165da2f88df9c402c5d130585e07147f7b97bdb8` | 未修改 |
| `generated/materialized_snapshot.json` | `3b7470d42c5ff45f5960d141c5504d7bf58c92d4437d4869ba49ec543c53cd70` | 未修改 |
| `candidate_tactical_session.gd` | `450fef381ce977f61c74fd7fc08f345def617a7dc46061a9e0d708bbe1bdcb11` | 未修改 |

最终 `git diff --check`：PASS。没有执行 `git add` 或 commit。
