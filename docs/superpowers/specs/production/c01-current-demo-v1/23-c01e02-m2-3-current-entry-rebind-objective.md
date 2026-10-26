# C01E02 M2.3 当前试玩默认入口换轨目标

> Status: `active / current candidate entry rebind / no real art handoff`
>
> Scope: `C01E02 Current Candidate Demo only`
>
> Runtime boundary: `candidate_runtime_demo / no promotion`

## 1. 为什么现在执行

M2.2 已完成同一 C01E02 Runner 的资产车道、合成夹具、逐槽回退与零 handoff 回归；当前仍为：

```text
build_id=C01CDV1-M2-R2
approved_handoffs=[]
runtime_art_loaded=false
```

但 Godot 默认启动仍经 `startup_router` 落入旧 `c01_story_first_chapter_playable.tscn`。这会让编辑器直接运行或默认 Windows Candidate 继续展示已退出当前 Demo 生产链的旧剧情和旧美术，与用户已批准的“原位覆盖当前 Demo、不保留第二套用户可运行 v1/v2”相冲突。

本轮只修正这个入口身份问题，不等待 A3/A4，也不接入任何美术。

## 2. 开工前读取

完整读取并核对：

1. `19-current-demo-inplace-rebase-producer-contract.md`；
2. `20-c01e02-j2-joint-integration-contract.md`；
3. `22-c01e02-m2-2-runner-asset-lane-objective.md`；
4. `main-m2-2/05-completion-report.md` 与当前 M2.2 测试摘要；
5. `game-godot/project.godot`、`startup_router.gd`、`startup_target_selector.gd`、`startup_router_smoke_test.gd`；
6. `game-godot/export_presets.cfg` 与 `windows_export_resource_validation.gd`；
7. `scripts/run_c01_candidate_demo_g1.sh` 与当前 Candidate Runner 身份文件。

先运行：

```bash
python3 scripts/check_c01_current_demo_contract.py
scripts/test_c01_candidate_asset_r2_m2_2.sh
```

若 M2.2 当前失败、活动 Runner 身份不是 `C01CDV1-M2-R2`，或必须修改玩法/存档/Autoload 才能换轨，写 `main-m2-3/BLOCKED.md` 并停止。

## 3. 唯一实现目标

让“编辑器直接运行／默认本地启动／默认 Windows Candidate 预设”进入：

```text
res://scenes/candidate_runtime_demo/c01/e02/c01e02_g1_runner.tscn
```

具体要求：

1. `project.godot` 继续以 `startup_router.tscn` 为 `run/main_scene`，不直接绕过路由器；
2. 修改 `startup_target_selector.gd` 的无参数默认目标为当前 C01E02 Candidate Runner；
3. `--m6`、`--validation=m6` 与 `m6_validation` feature 继续进入 M6；`--legacy-perspective` 行为保持不变；
4. 旧 `story_first` 场景、脚本、素材和测试不得删除或重写，但不再是默认用户入口；它们只保留为 History/回归库存，由既有测试显式实例化；
5. 更新 startup smoke test，直接验证默认目标、M6、legacy 三条路由，并确认默认目标加载的 build ID、profile、save schema 与 content fingerprint 属于 M2-R2；
6. 将 Windows preset 0 的名称、输出文件名、产品名和描述改为 C01E02 Current Candidate Demo，不能继续以 `Story First Chapter` 冒充当前默认试玩；同步更新 Windows export validation；
7. 新增稳定用户入口 `scripts/run_c01_candidate_demo_current.sh`。现有 `run_c01_candidate_demo_g1.sh` 可保留为兼容包装，但应转调稳定入口或明确标为旧脚本名、当前 M2-R2 内容；不得形成两套实现；
8. 默认启动不得读取或加载 `story_first` 资产，且零 handoff 状态保持 `approved_handoffs=[] / runtime_art_loaded=false / resource_probes=0`。

## 4. 写入范围

允许修改或新增：

- `game-godot/scripts/core/startup/startup_target_selector.gd`
- `game-godot/scripts/startup_router_smoke_test.gd`
- 为默认入口身份新增的一个窄 smoke test（如确有必要）
- `game-godot/export_presets.cfg`
- `game-godot/scripts/windows_export_resource_validation.gd`
- `scripts/run_c01_candidate_demo_current.sh`
- `scripts/run_c01_candidate_demo_g1.sh`（仅作为兼容包装或说明）
- `scripts/godot-test.sh`（只登记新增 smoke test）
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m2-3/**`

明确只读：

- `game-godot/project.godot`
- `game-godot/scripts/startup_router.gd`
- C01E02 Runner、战棋、存档、内容与 R2 asset lane 实现
- 全部美术目录、Canon、剧情和 C04

不得删除旧 `story_first` 文件，不得建立另一套 Demo，不得 `git add/commit`。

## 5. 验收

至少证明：

1. 无参数 selector 精确返回当前 Candidate Runner；
2. M6 与 legacy 显式路径保持；
3. 默认入口实际能加载且身份为 M2-R2；
4. 默认入口文本链不引用 `story_first`；
5. 零 handoff、20 次重放、存档恢复、旧存档拒载和 M2.2 资产车道回归保持通过；
6. Windows preset 0 不再命名为 Story First；
7. `project.godot`、玩法、存档、Canon、美术、C04 未改变；
8. `git diff --check` 通过。

本轮不重复制作大规模上游 source receipt 或逐文件交付哈希；只交 `route-matrix.tsv`、测试摘要和完成报告，报告中记录当前 build ID/fingerprint 与实际修改文件。

## 6. 停止门

完成入口换轨后立即停止。不得继续接入 A1/B1/B2/A2/A3、创建真实 handoff、修改玩法、升级正式 Runtime 或清理旧 History 文件。

若默认换轨会破坏非 Demo 产品入口、M6、共享 Autoload、存档 schema 或正式导出策略，必须给用户列出影响与 2–3 个方案后停止，不得自行扩大改造。
