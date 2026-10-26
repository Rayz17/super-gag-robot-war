# C01E02 Candidate Demo 跨 Session 协作合同 v1

> Status: `active / G1_dispatched_after_D0`
>
> Frozen source snapshot: `fe7a0764d11f5ac5f9d11accb7398df664132b0b`
>
> Demo outcome override: `D0_S07_OUTCOME=gameplay_finisher`

## 共同读取顺序

所有参与 Demo 的 Session 在写入前必须依次读取：

1. `00-demo-source-authorization.md`
2. `01-source-lock.tsv`
3. `09-frozen-source-snapshot.tsv`
4. `09b-frozen-visual-snapshot.tsv`
5. `13-demo-build-contract.json`
6. `02-e02-s01-s07-beat-runtime-map.tsv`
7. `04-e02-previs-v0.1.md`
8. `05-e02-asset-call-matrix.tsv`
9. `06-e02-state-checkpoint-contract.tsv`
10. `07-legacy-denylist.tsv`
11. `08-g1-user-decision-card.md`
12. 本文件及各自的 G1 目标

先运行：

```bash
python3 scripts/check_c01_current_demo_contract.py
```

合同检查失败时不得继续制作，也不得自行修改制作人合同。

## 数据流边界

```text
设定/剧情/台本继续推进 C03+
              |
              | 不自动回灌
              v
工作树 latest（持续变化）

Git snapshot fe7a0764...（不可变）
              |
              +--> Demo source bundle
              +--> 美术 G1 Previs
              +--> 主程序 G1 灰盒
```

- Demo 只从 `snapshot_ref:path` 读取冻结内容。工作树同名文件发生变化不构成 source drift，也不得被静默吸收。
- 若未来确需采用剧情 Session 的新版本，必须由制作人另签 snapshot ref、登记差异并重跑合同与下游回归。
- D0-B 是 Demo 专用结果裁决，不是 C01 Candidate Reader 或 Current Canon 的静默迁移。

## 写入所有权

| Session | 可写范围 | 本阶段不得写 |
|---|---|---|
| 制作人 | `docs/superpowers/specs/production/c01-current-demo-v1/`、合同校验器、联合验收 | 正式美术母版、主程序实现、C03正文 |
| 设定/剧情/台本 | C03 分层 Candidate、其审查与合法生产记录 | 本 Demo 00–12 合同、Godot Demo、美术 G1 |
| 美术资产 | `docs/superpowers/specs/production/c01-current-demo-v1/art-g1/` | Godot、主程序 G1、Canon/Runtime promotion、制作人合同 |
| 主程序 | 下列精确 allowlist 与 `.../main-g1/` 证据 | `art-g1/`、正式 Current 入口、旧 Demo 内容、制作人合同、共享内核与 Autoload |

各 Session 不执行 `git add`、`git commit`、Canon 迁移或工作区清理；由制作人统一审计和提交。遇到其他 Session 的文件变化时，不回滚、不覆盖。

### 主程序 G1 精确写入 allowlist

主程序只可新增或修改以下路径；“Candidate 专用命名空间”不是建议而是 fail-closed 边界：

- `game-godot/content/candidate_runtime_demo/c01/e02/**`
- `game-godot/scripts/candidate_runtime_demo/**`
- `game-godot/scenes/candidate_runtime_demo/**`
- `game-godot/tests/candidate_runtime_demo/**`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g1/**`
- `scripts/run_c01_candidate_demo_g1.sh`
- `scripts/test_c01_candidate_demo_g1.sh`

特别禁止修改 `game-godot/project.godot`、`game-godot/scenes/startup_router.tscn`、`game-godot/scripts/startup_router.gd`、`game-godot/scripts/core/startup/startup_target_selector.gd`、`game-godot/scripts/autoload/**`、共享 Current 场景/脚本以及现有测试总入口。G1 必须通过显式 Candidate 场景命令独立启动；共享接口不足时写 `main-g1/BLOCKED.md` 并停下，不以“临时接线”为由越界。

## 互通机制

- 美术和主程序均以 `PV01`–`PV06`、1280×720 画幅、`04` 中坐标/镜头号对接。
- 每项输出必须带 Stable ID、来源 snapshot/contract copy、父级、状态、SHA-256 和 `runtime_allowed`；实际母版只能来自 `09b-frozen-visual-snapshot.tsv`。
- 主程序只接受资产矩阵中已登记的 slot；G1 美术仍为 `runtime_allowed=false`，只能用于叠图验证，不能进入正式 Runtime。
- 任何 Session 发现来源冲突，写入自己的 `BLOCKED.md` 并停止相关分支，不在共享合同中自行裁决。

## 重大决策门

以下事项必须停下交用户确认：

1. D1：S01/S03 是否采用斜侧视浅 X/Y 探索。
2. D2：馆守 Z 是否以 V10X 作为本 Demo 派生基准。
3. D3：S06 的姿态谜题是否好懂、值得继续。
4. 任何人物/机体重设计、Canon 迁移、正式 Runtime promotion、批量 AI 生图、付费 LibTV 或玩法因果改变。

不属于重大决策的局部修复，如占位尺寸、测试、命名空间、无障碍提示和捕获脚本，可在各自范围内完成。

## G1 联合完成条件

- 美术目标 `11-g1-art-session-objective.md` 全部完成。
- 主程序目标 `12-g1-main-program-objective.md` 全部完成。
- 制作人完成两张 50% 叠图、旧新对照和独立只读审查。
- 自动检查通过，但不把内部 PASS 视为用户视觉/玩法验收。
- 将 D1–D3 的实际画面和可玩证据交给用户，用户选择前不开放 G2。
