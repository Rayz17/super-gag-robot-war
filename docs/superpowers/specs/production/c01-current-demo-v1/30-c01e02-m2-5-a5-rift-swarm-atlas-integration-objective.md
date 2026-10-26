# C01E02 M2.5 A5 小型突入体四向 Atlas 接入目标

> Status: `active / producer exact handoff / candidate runtime integration`
>
> Demo: `C01CDV1-M2-R2 / C01E02 S01-S07`
>
> Newly authorized art slot: `ENEMY_C01CDV1_RIFT_SWARM_MASTER`
>
> Formal Runtime promotion: `not authorized`

## 1. 本轮唯一目标

在现有 Current C01E02 Candidate Runner 内，把用户已批准的 96px 小型突入体 `idle` 四向 Atlas 接入 `ENEMY_C01CDV1_RIFT_SWARM_MASTER`，并让现有六个实例继续共用这一母版、按各自实时 `facing` 读取 `idle/north|east|south|west`。

本轮沿用 M2.4 已接入的五个 MAP-B 静态槽。活动资产链最终必须是一份新的六槽合并 validated receipt：五个 A4 地图槽加一个 A5 小体母版槽。不得并行加载第二份 active receipt，不得原地改写或冒充旧 A4 五槽 receipt。

本轮不制作或声称已经具有 `move`、`impact`、`death` 动画，不制作六套实例差分，不改变小体数量、锚点、AI、行动规则、地图或剧情。

## 2. 用户裁决与冻结输入

必须完整读取并核对：

1. `19-current-demo-inplace-rebase-producer-contract.md`；
2. `20-c01e02-j2-joint-integration-contract.md`；
3. `22-c01e02-m2-2-runner-asset-lane-objective.md`；
4. `26-c01e02-m2-4-a4-map-static-five-slot-integration-objective.md`；
5. M2.4 完成报告 `main-m2-4/05-completion-report.md`，SHA-256 `b1ee2776b74f2158f8fd32d39db06969b08286e40897e5b2dba5b1b6f54823f7`；
6. 当前 Runner，冻结 SHA-256 `de31ba758bd0490bbfa60e411f090e72a5741be322365db33fbff37e0c6c6f06`；
7. R2 静态 manifest，SHA-256 `2cc85fc524b453b255c4d8aa521236e0845664f1a8721829da7a5befa21b93c9`；
8. A5 用户批准回执 `producer-a5/a5-user-approval-receipt.tsv`，SHA-256 `45c1687c3fdbdd87d7f9e872933b48925871f680eeaa0095d360623ad1a34f75`；
9. A5 精确复制计划 `producer-a5/a5-rift-swarm-96-copy-plan.tsv`，SHA-256 `1467bf0e8dae7de0969761cd06c36ad7c8ff7259e424a457e694827d1da2b6ca`；
10. 六槽合并 handoff `producer-a5/a4-static-5-plus-a5-rift-swarm-96-exact-handoff.json`，SHA-256 `abd97837d9abe811862b3a0e5878e6263fd46379eb6f4336fb6af18bb5bd1e36`；
11. 获批源图 `art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png`，SHA-256 `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b`；
12. A5 `atlas-spec.tsv`，SHA-256 `3d52d578c1e189a4cb57d2b2691c41e29c17d6f76dde29dafc9c7269b763a6dd`；
13. 现有 A4 五槽用户回执、copy plan、exact handoff 与已复制五张生产图；
14. R2 handoff/validated receipt schema、Python preflight、Godot resolver、active binding 和 Current Canon 的 `V355-C01E02`、`ENEMY_C01_RIFT_SWARM`。

在修改 Runner 前，先以 M2.4 终态运行 A5 validator、A5 core hash、Current Demo contract、R2 baseline、Canon authority/smoke 与 Godot Canon strict，并把结果写入 M2.5 前置回执。A5 包冻结的 Runner 正是上述 `de31...f06`；M2.5 后 Runner 改变属于下游获授权消费变更，不得回写 A5 包、刷新 A5 哈希或把预期 drift 当成美术返工理由。

任何 handoff、源图、slot、build、profile、topology 或 SHA 不一致时停止，不自行修改制作人 handoff。

## 3. 字节复制与六槽预检

1. 严格按 copy plan 把所选 96px PNG 字节级复制到：
   `game-godot/content/candidate_runtime_demo/c01/e02/approved_runtime_assets_r2/a5_rift_swarm/rift-swarm-idle-96.png`。
2. 复制后 SHA 必须仍为 `1dc037...526b`；不得重新编码、缩放、改色、裁边或改名。
3. 用现有 `candidate_asset_resolver_r2.py` 严格预检六槽合并 batch，不得使用 `--allow-partial`。
4. 先输出到新的非 active 路径，预期 `submitted=6 / validated=6 / rejected=0 / probes=6 / synthetic_fixture=false`。
5. 只有全部通过后，才建立新的 frozen combined validated receipt、rejections log，并原子切换 active binding 和 Runner 常量到该新 receipt。
6. 保留旧 A4 五槽 batch、validated receipt 与回执原字节不变，作为 M2.4 历史证据。

静态 `asset_slot_manifest_r2.json` 必须继续保持 `approved_handoffs=[]`、`asset_policy.runtime_art_loaded=false`、各槽 `runtime_allowed=false / approved_asset_binding=null`。仅 exact handoff 指定的 Candidate-local 字节副本可在这条 Demo lane 中由 validated receipt 授权加载；这不是正式 Runtime 或 Canon promotion。

## 4. 绘制与实例语义

- 六个既有实例继续绑定同一 `ENEMY_C01CDV1_RIFT_SWARM_MASTER`，不得新增 variation 字段或六份纹理。
- 冻结初始 facing 为：01 east、02 east、03 north、04 north、05 west、06 north；移动后按实际 `unit.facing` 切换 `idle/<facing>`。
- Atlas 必须按 `north, east, south, west` 顺序读取四个 `96x96` frame，rect 分别为 `[0,0,96,96]`、`[96,0,96,96]`、`[192,0,96,96]`、`[288,0,96,96]`。
- 使用 `pivot=[0.5,1.0]` 的 bottom-center 落点和 manifest 既有 `footprint=[1,1]`；不得改变锚点、格位或碰撞/寻路范围。
- 真 Atlas 成功绘制时不得同时绘制小体几何 token；回退时只出现原具名几何 token。
- 本轮 `idle` frame 随朝向切换只代表站姿/移动方向，不得冒充移动、命中或死亡动画。
- M2.4 五个地图槽、遮挡淡出、地图滚动、盾牌四态与程序化 STATE fallback 均保持原行为。

## 5. Active 与 fail-closed 合同

默认 Current 生产路径预期：

- `validated_handoff_count=6`
- `loaded_slot_count=6`
- `resource_probe_count=6`
- `runtime_art_loaded=true`
- 首批 13 槽中 `fallback_count=7`

固定优先级仍为：`disable active art > explicit environment receipt > default active binding`。无效显式 receipt 不得悄悄回落默认 active receipt。

失败行为：

- 缺/坏 combined active config、receipt 路径或 receipt SHA：`0 probes / 0 loads / 13 slots fallback`，试玩继续可玩；
- 合法 receipt 加载后仅 A5 文件缺失或 SHA 漂移：六项均被探测，五个地图槽继续加载，A5 单槽回退具名几何；
- A4 单层资源漂移：只回退对应地图槽，A5 仍加载；
- disable 模式：`0 validated / 0 loaded / 0 probes / runtime_art_loaded=false`；
- 所有失败审计仅进入运行回执，不进入 save payload，不改变 gameplay/state signature。

## 6. 必做验收

至少完成并留证：

1. 默认无参数入口真实 `6/6/6`，其余七槽精确 fallback；
2. 六实例都引用同一 texture/master slot，且无几何 token 双绘；
3. 四个真实 frame 的逐向像素/rect 审计，必须包含初始阵列没有的 south；south 可由隔离 capture driver 构造显示态，不得修改正式关卡或 save；
4. 一组真实 end-turn 前后捕获，证明小体移动导致 facing 和 frame 正确变化，同时锚点、1x1 footprint、AI 结果和状态签名保持合同；
5. bottom-center 接地、Atlas 无串帧/边缘 bleed、96px 不被错误二次缩放；
6. WEST、CENTRAL、EAST 中至少各一张含真地图和真小体的 `1280x720` 截图，登记 camera、frame IDs、loaded slots、PNG SHA 与 gameplay/state signature；
7. A5 缺文件、A5 坏 SHA、单个 A4 坏 SHA、坏 receipt SHA、缺 active config、disable 与无效显式 receipt 的 fail-closed 测试，均用隔离夹具或临时副本；
8. 20 次 deterministic replay、Full/Skip 等价、CP0/CP1/CP2/PHASE_PENDING/PHASE_STATE 恢复、旧 save 拒载、失败重试、P1 payload 全部不变；
9. 默认 Current、Godot 编辑器、稳定启动脚本与 Windows 资源验证都使用相同六槽活动链；M6/legacy 显式入口不被重绑；
10. 全量 Godot、M2.2/M2.4 兼容回归、startup router smoke、active-lane audit、Current contract、Canon report/strict、authority/smoke、layered dashboard 与 `git diff --check` 通过。

M2.4 的旧五槽默认断言已被 M2.5 合法取代：历史五槽用例如需复跑，应显式指定旧 receipt 或作为 fixture；不得让它覆盖当前默认六槽预期。

## 7. 写入范围

允许写：

- copy plan 指定的一个 A5 Candidate-local 字节副本；
- 新的六槽 combined validated receipt、rejections 与 `active_asset_binding_r2.json`；
- `game-godot/scripts/candidate_runtime_demo/c01/e02/c01e02_g1_runner.gd` 中 active config/receipt/inventory/count 与显示审计所必需的局部代码；
- `game-godot/scripts/candidate_runtime_demo/c01/e02/asset_integration_r2/audit_active_asset_lane_r2.py`：更新 active receipt/rejections 和授权运行资产 inventory，同时保留 `art-a5` deny token，证明运行链不直读美术源；
- `game-godot/scripts/startup_router_smoke_test.gd`：默认 Current 改验 6/6/6，disable 仍验 0/0/0；
- 必要的 M2.5 专项 GDScript、capture driver、测试 shell 登记，以及为当前默认六槽预期所必需的 M2.2/M2.4 兼容测试局部更新；
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m2-5/**`。

只读且不得修改：

- A3/A4/A5 美术源包、用户回执和本制作人 exact handoff/copy plan；
- `asset_slot_manifest_r2.json`、R2 schemas、Python resolver、Godot resolver；若现有 resolver 真正无法完成上述合同，写 `BLOCKED.md` 并停止，由制作人决定是否扩展接口；
- Canon、剧情、C04、玩法、数值、地图拓扑、单位数量/锚点/AI、存档 schema、build/profile/content fingerprint；
- `project.godot`、Autoload、startup selector/router 架构、Current 稳定启动脚本、正式 Runtime、LibTV；
- 馆守 Z、BREAKER、重盾真实资产与 A4 STATE_LAYERS。

缺/坏资源测试不得原地篡改正式生产 PNG、正式 receipt 或 active 配置。不 `git add/commit`。

## 8. 停止门

完成后交付：

- 六槽 validated receipt、active binding 与各自 SHA；
- `6 loaded / 7 fallback` 台账；
- 四朝向、移动前后、三机位、接地与无双绘证据；
- fail-closed 矩阵、回归摘要、完成报告和交付哈希。

随后停止，等待用户联合试玩。不得自行接下一项美术、补做动画、修 A4 状态层、改玩法或升级正式 Runtime。
