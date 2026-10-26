# C01E02 M2.3 完成报告

> Result: `PASS / default entry rebound in place / stop gate reached`
>
> Date: `2026-08-09`

## 结论

同一个 Godot 项目的无参数默认试玩已经从旧 `story_first` 换轨到：

```text
res://scenes/candidate_runtime_demo/c01/e02/c01e02_g1_runner.tscn
```

活动身份保持：

```text
build_id=C01CDV1-M2-R2
content_fingerprint=00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4
save_schema=2
profile_id=c01cdv1_e02_scroll_m2_r2
approved_handoffs=0
runtime_art_loaded=false
resource_probes=0
```

这只是 `candidate_runtime_demo` 的当前入口绑定，不是正式 Runtime promotion。

## 实现

- `startup_target_selector.gd` 的无参数默认目标改为 Current C01E02 Runner；M6 feature/参数和 legacy 显式参数优先级未变。
- `startup_router_smoke_test.gd` 现在真实加载并启动默认 Runner，核对 build/profile/schema/fingerprint、零 handoff 与默认文本链污染。
- Windows preset 0 的显示名、exe、产品名和描述已改为 C01E02 Current Candidate Demo；Windows resource validation 同步核对 Current 身份。
- 新增稳定入口 `scripts/run_c01_candidate_demo_current.sh`；旧 `run_c01_candidate_demo_g1.sh` 仅作兼容包装。
- 旧 `story_first` 文件未删除、未重写，仍由显式回归测试覆盖，但不再由默认 selector 暴露。

## 试玩入口

```bash
scripts/run_c01_candidate_demo_current.sh
```

Godot 编辑器直接运行项目也会经只读的 `startup_router.tscn` 进入同一 Current Runner。需要保留进度时使用：

```bash
C01_M2_PERSIST_SAVE=1 scripts/run_c01_candidate_demo_current.sh
```

## 修改范围

- `game-godot/scripts/core/startup/startup_target_selector.gd`
- `game-godot/scripts/startup_router_smoke_test.gd`
- `game-godot/export_presets.cfg`
- `game-godot/scripts/windows_export_resource_validation.gd`
- `scripts/run_c01_candidate_demo_current.sh`
- `scripts/run_c01_candidate_demo_g1.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m2-3/**`

未修改 `project.godot`、`startup_router.gd`、Autoload、Runner、战棋、存档 schema、内容 JSON、R2 asset lane、Canon、剧情、美术、C04 或正式 Runtime。没有接入 A1/B1/B2/A2/A3，没有真实 handoff，没有建立第二套 Demo，也没有执行 `git add` 或 commit。

`generated/build_identity.json` 继续作为冻结的 M2 生成回执保留，因此其中原有的 `default_entry_modified=false` 未被重写；当前默认入口事实由 selector、route matrix 和 M2.3 smoke 共同证明。这符合 23 号目标对 Candidate 身份文件的只读要求。

## 证据

- [路由矩阵](route-matrix.tsv)
- [测试摘要](01-test-summary.md)

M2.3 的内部验收已完成，本任务在入口换轨停止门处停止；这不代替用户对最终 Demo 内容与观感的验收。
