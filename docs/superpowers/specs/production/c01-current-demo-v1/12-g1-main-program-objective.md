# 主程序 Session 目标：C01E02 G1 隔离运行时骨架与灰盒

## Scope

只实现能回答 D1–D3 的 Candidate Demo G1 骨架、灰盒、状态合同和可复现捕获证据；不完成正式 S01–S07 内容，不替用户批准视觉母版，不改 Current 或共享内核。

## Frozen Inputs And Build Identity

- 先按 `10-cross-session-coordination.md` 顺序读取全部合同并运行 `python3 scripts/check_c01_current_demo_contract.py`。
- 内容必须从 `09-frozen-source-snapshot.tsv` 的 `snapshot_ref:path` 物化；视觉清单只读 `09b-frozen-visual-snapshot.tsv`。不得读取工作树 latest、`.superpowers` 活动路径或旧 Demo 后冒充冻结来源。
- 机器构建身份以 `13-demo-build-contract.json` 为唯一入口：启动和物化都必须校验 `contract_id`、`contract_version`、snapshot ref、18 项源 SHA-256、7 项视觉冻结、D0-B 语义文件哈希与 `content_fingerprint`。任一缺失或不匹配必须 fail closed。
- `content_fingerprint` 不得由主程序自行发明或只覆盖旧源；必须逐字采用 `13` 定义的算法和值，并写入存档、物化回执和捕获清单。

## Exact Write Allowlist

只可新增或修改：

- `game-godot/content/candidate_runtime_demo/c01/e02/**`
- `game-godot/scripts/candidate_runtime_demo/**`
- `game-godot/scenes/candidate_runtime_demo/**`
- `game-godot/tests/candidate_runtime_demo/**`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g1/**`
- `scripts/run_c01_candidate_demo_g1.sh`
- `scripts/test_c01_candidate_demo_g1.sh`

禁止修改 `game-godot/project.godot`、默认 `game-godot/scenes/startup_router.tscn`、`game-godot/scripts/startup_router.gd`、`game-godot/scripts/core/startup/startup_target_selector.gd`、`game-godot/scripts/autoload/**`、共享 Current 场景/脚本、现有测试总入口和制作人合同。共享代码全部只读；接口不够时停下报告，不能扩大写入范围。

## Candidate-Local Runtime Architecture

- 新建独立入口 `res://scenes/candidate_runtime_demo/c01/e02/c01e02_g1_runner.tscn`，由 `scripts/run_c01_candidate_demo_g1.sh` 显式场景命令启动；不得替换项目默认入口，也不得向 startup selector 注册 Candidate。
- Candidate runner 使用本地状态容器、输入路由、内容注册、模式路由和 Episode 驱动或无副作用 adapter。不得调用全局 `GameKernel.start()`、不得依赖全局 `EpisodeDirector` 自动生成槽名；在任何 start/before-enter 逻辑前显式绑定唯一槽 `c01_candidate_demo_v1/c01e02`。
- 运行前后对所有全局 Autoload 可序列化状态和全部非 Candidate 存档做快照；测试要求字节级不变。Candidate 退出不得 reset Current 内存态，不得读写 `story_first` 槽。
- 通用 `ExploreMovementController`、ModeScene 生命周期、NarrativeDirector、EpisodeGraph/Director、StateTransaction、RunStateStore 及 DeclarativeBattleSession/Grid 的纯接口或算法可只读复用；任何带全局注册、副作用或旧内容 preload 的对象不得实例化。
- S06 必须使用 Candidate-only tactical scene 与 Candidate-only driver/factory。禁止实例化现有 `TacticalModeScene`，禁止调用 `ScenarioDriverRegistry.reload_catalog(...)`，禁止 runtime preload 旧 perspective stage/config 或任何 `story_first` 地图。

## Runtime Skeleton

建立七个精确节点与 CP0–CP3：

- `c01cdv1_e02_s01_evac_route`
- `c01cdv1_e02_s02_evac_confirm`
- `c01cdv1_e02_s03_same_body_reveal`
- `c01cdv1_e02_s04_qihai_revoke`
- `c01cdv1_e02_s05_guardian_stand`
- `c01cdv1_e02_s06_plaza_tutorial`
- `c01cdv1_e02_s07_shield_victory`

CP0 必须保存 `demo_contract_version` 与 `content_fingerprint`。完整/跳过、失败/重试和退出/重入均服从 `06-e02-state-checkpoint-contract.tsv`，不使用全局正式进度。

## G1 Graybox

1. S01/S03：1920×900 世界、1280×720 相机、三区相机、浅 X/Y 移动、Y-sort/遮挡、具名热点；人物高度按 `04` 候选值，不能只左右移动。
2. S01 两项失败必须显示具体原因并回 CP0；不得用空气墙、自然阻挡或自动纠正冒充失败合同。
3. S02：撤离原子结算与 CP1；清走全部人类尺度单位后再切巨机尺度。
4. S03：World → Shot/ADV 的同体声源切换占位，终端与胸前字幕/音频不重叠提交。
5. S04：双地 ADV 线框；七海只远程出现，不加载旧头像。
6. S05：五拍可跳过演出骨架；Full/Skip 到达完全相同 CP2。
7. S06：实现 `c01cdv1_s06_g1_v1` 的 12×9 灰盒。Candidate 自有占用模型必须真实支持馆守 Z 2×2 与 BREAKER 3×3 footprint、面向、推击、支撑、盾状态、安全线和热点；不能用单格 anchor 假装多格占位。实现行动者/目标/受影响区/安全线意图，以及移动、推击、防御/支撑、调盾、结束行动；4–6 回合，无经验、升级、杂兵或磨血。
8. S06 失败：敌体越过北线或馆守 Z 被禁用，说明原因并从 CP2 的同一 profile 重建；不得保留失败帧坐标、朝向、盾消耗或回合。
9. S06 胜利条件齐全时只设置 `finisher_ready=true`，保留可控战场并开放“强化盾拍”。玩家必须亲手执行 `confirm_shield_bash` 后才设置 `finisher_triggered=true`、进入 S07 并允许 Full/Skip；跳过只缩短结果演出，绝不替玩家执行终结指令。
10. S07：挡击—推进—强化盾拍倒地的占位演出；CP3 必须同时保存 `finisher_triggered=true`、`breaker_first_knockdown=true`、`breaker_destroyed=false`，重复进入不二次提交。

所有视觉只能使用资产矩阵中的具名几何 fallback。任何缺图必须显示 slot ID 和 `PREVIS PLACEHOLDER`；禁止无提示地使用旧头像、旧 Sprite、旧地图或空白替代。G1 不把 `art-g1` 文件装入 Runtime。

## Evidence

输出到 `docs/superpowers/specs/production/c01-current-demo-v1/main-g1/`：

1. `PV01` S01 20 秒实机捕获，明确展示浅 X/Y、三区相机、一个前景遮挡及至少一次具名交互。
2. `PV05` S06 20–30 秒实机捕获，展示意图、同一 profile 下两种站位结果，以及失败重试或取盾前后差异。
3. 一段 30–45 秒 World → Screen/Shot → Tactical 的低保真连续捕获。
4. S01 与 S06 各一张 1280×720 程序基准截图，供制作人与美术做 50% 叠图。
5. `source-materialization-receipt.tsv`、`capture-manifest.tsv`、`completion-report.md` 及测试日志。

`capture-manifest.tsv` 每条至少记录：`content_fingerprint`、入口 scene、profile/起始 CP、可重放输入序列或 driver ID、viewport、帧率、Full/Skip、输出 SHA-256。PV05 的两种站位、失败与重试必须来自同一 profile 的可重放输入，不接受手改变量后的静态截图。

## Tests

新建专用 runner，并由 `scripts/test_c01_candidate_demo_g1.sh` 精确执行；不得假设现有 `scripts/godot-test.sh` 会自动发现 Candidate 测试。完成顺序是先跑专用 runner，再跑完整既有回归 `scripts/godot-test.sh`，并在报告记录命令、退出码与日志路径。

专用测试至少覆盖：

- 18 项 frozen Git blob、7 项视觉冻结和 build-contract 语义哈希正确；工作树同名剧情改变不影响 `content_fingerprint`。
- 七节点顺序与 CP0–CP3 唯一；CP0 带合同版本与指纹。
- S01 两项失败显示具名原因并回 CP0。
- 只有 S05 和玩家已确认盾拍后的 S07 演出可跳过；Full/Skip 状态等价。
- S06 真实 2×2/3×3 footprint、面向/推击/支撑/盾状态均参与结果；两项失败回 CP2 并重建同一初态。
- S06 成功必须同时满足安全线、未禁用、改向、得盾、挡红光和 `finisher_ready=true`；在 `confirm_shield_bash` 前绝不写 CP3。
- CP3 D0-B 字段逐项正确且重复进入不二次提交。
- 运行前后全局 Autoload 快照与全部非 Candidate 存档字节级不变。
- Candidate 运行时不加载 denylist、`TacticalModeScene`、旧 perspective 内容或 `story_first` 资源，不存在静默旧资产 fallback。
- 旧 Canon/Godot 回归测试仍通过。

## Stop Conditions

- 不集成 `art-g1` 为 Runtime 资产；它们在 G1 均为 `runtime_allowed=false`，只可由制作人做叠图。
- 不重构全局 ModeRouter、保存系统、启动路由或战棋内核；若 Candidate-local adapter 无法隔离，写 `main-g1/BLOCKED.md` 后停止。
- 发现必须改变探索呈现、馆守 Z 身份、S06 核心胜法、共享接口或精确 allowlist 时停止，交用户/制作人裁决。
- 不暂存、不提交；完成后列出文件、测试、捕获和遗留风险。
