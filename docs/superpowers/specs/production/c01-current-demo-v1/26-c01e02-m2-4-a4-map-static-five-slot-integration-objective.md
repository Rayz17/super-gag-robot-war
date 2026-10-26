# C01E02 M2.4 A4 MAP-B 五槽真实接入目标

> Status: `active / producer exact handoff / candidate runtime integration`
>
> Demo: `C01CDV1-M2-R2 / C01E02 S01–S07`
>
> Authorized real-art slots: `5`
>
> Formal Runtime promotion: `not authorized`

## 1. 本轮唯一目标

在同一个 Current C01E02 Candidate Runner 中，按制作人 exact handoff 接入 A4 已获用户批准且技术安全的五个 MAP-B 槽：

1. `MAP_C01CDV1_R2_BASE`
2. `MAP_C01CDV1_R2_BUILDINGS`
3. `MAP_C01CDV1_R2_ROOFS`
4. `MAP_C01CDV1_R2_FOREGROUND`
5. `MAP_C01CDV1_R2_OCCLUSION_MASK`

让无参数默认试玩、Godot 编辑器直接运行和稳定启动脚本都能消费同一份冻结 validated receipt；其余八个 M2.2 槽继续逐槽具名几何 fallback。

本轮不接 `MAP_C01CDV1_R2_STATE_LAYERS`。该文件视觉上已获用户批准，但当前单一静态槽不能切换撤离线/盾架/损伤状态，且图内墙挂盾会与独立重盾四态槽重影；因此保留为获批派生来源，等待技术拆包，不得绕过。

## 2. 冻结输入

完整读取并核对：

1. `19-current-demo-inplace-rebase-producer-contract.md`；
2. `20-c01e02-j2-joint-integration-contract.md`；
3. `22-c01e02-m2-2-runner-asset-lane-objective.md`；
4. `23-c01e02-m2-3-current-entry-rebind-objective.md`；
5. `main-m2-2/05-completion-report.md` 与正式测试/哈希；
6. `main-m2-3/02-completion-report.md`；
7. `producer-a4/a4-user-approval-receipt.tsv`，SHA-256 `dc402de8ee471953fa1de8b98676aa76a9826a2b219dc6010ba7e762f128781b`；
8. `producer-a4/a4-map-static-5-copy-plan.tsv`，SHA-256 `21bed025aa4efff116003b952b4e9450071d96b4f18021e52f82f7b9d845181d`；
9. `producer-a4/a4-map-static-5-exact-handoff.json`，SHA-256 `494defbd783f478b8c51458457b514295e5e8e026f59a3e48c024451fb10e429`；
10. R2 handoff/validated receipt schema、Python preflight、Godot resolver、活动 Runner；
11. Current Canon 的 `V355-C01E02`。

先跑 C01 Demo 合同、R2 基线、Canon 和 exact source hash 检查。任何 source/slot/build/profile/topology/hash 不一致时停止，不自行更新制作人 handoff。

## 3. 精确复制与预检

- 只按 copy plan 把五个源 PNG 字节级复制到：
  `game-godot/content/candidate_runtime_demo/c01/e02/approved_runtime_assets_r2/a4_map_b/**`
- 复制后 SHA 必须与 copy plan 和 handoff JSON 完全一致；不得重新编码、缩放、改色、裁边或重命名为未授权路径。
- 使用现有 `candidate_asset_resolver_r2.py` 对制作人 batch 做严格预检，生成一份非 fixture 的冻结 validated receipt 与 rejection log。
- 预期 `submitted=5 / validated=5 / rejected=0 / synthetic_fixture=false / runtime_art_loaded=true`。
- validated receipt、其 SHA 和显式激活配置必须位于 Candidate-local 路径；不得扫描美术目录或按文件名猜测资产。
- 原美术源仍是 `Candidate / runtime_allowed=false`；只有 copy plan 中五个字节级副本在本 Candidate Demo lane 获 `runtime_allowed=true`。这不构成正式 Runtime 或 Canon promotion。

## 4. 默认激活方式

M2.2 的外部 receipt 注入与 fixture 测试必须保留。本轮另建立一个显式、哈希锁定、Candidate-local 的 active-art 配置，使没有环境变量时也只加载上述正式 validated receipt：

- 配置必须记录 receipt 的固定 `res://` 路径、文件 SHA、预期 slot 列表和 `candidate_runtime_demo` 生命周期；
- 不允许目录扫描、最近文件选择、通配符或缺哈希加载；
- 环境变量显式 receipt 继续拥有测试优先级；
- 必须提供一个显式“禁用 active art、回到零 handoff”的测试开关，用于 M2/M2.2 既有几何基线回归；
- 稳定优先级固定为：`disable active art > 显式环境变量 receipt > 默认 active-art 配置`；显式 receipt 无效时必须全几何回退，不能悄悄改读默认 active receipt；
- 缺配置、坏配置、receipt SHA 漂移时，默认 active-art 路径必须以 `0 probes / 五槽全回退` 继续可玩，不能把整个试玩变成 fatal；receipt 已合法加载后若单一资源 SHA 漂移，只回退该槽；
- 静态 `asset_slot_manifest_r2.json` 的 `approved_handoffs=[]` 注册基线不得被改写。运行态另报告 `validated_handoff_count=5`、`loaded_slot_count=5`、`runtime_art_loaded=true`。

不得修改 `project.godot`、Autoload、save schema、build ID、content fingerprint 或正式入口架构。

## 5. 绘制与状态边界

- BASE/BUILDINGS 在单位前绘制；
- ROOFS/FOREGROUND 在单位后绘制；
- OCCLUSION_MASK 只采样控制淡出，不作为可见彩色层绘制；
- `STATE_LAYERS` 必须明确记录为 fallback，继续使用现有程序化可破坏物与状态表现；
- 馆守 Z、BREAKER、小体与重盾继续使用各自具名几何 fallback；禁止读取 A3/A5 或旧美术；
- 不得出现墙挂盾双绘、撤离线状态卡死、屋顶吞单位、路径/光标被地图遮住或 HUD 随地图滚动；
- 相机、格位、锚点、footprint、AI、胜负条件与状态提交均不得改变。
- 生产模式也必须记录逐槽 fallback audit；该审计只存在于显示回执，不得进入 save payload。
- 完成报告必须把“尚无 A4 撤离灯/空架/战损完整动态切换”登记为视觉债，不能把五槽接入称为动态状态美术完成。

## 6. 验收

至少完成：

1. 默认入口真实加载 5/5，其他 8 槽精确 fallback；
2. WEST `(-160,320)`、CENTRAL `(240,480)`、EAST `(830,620)` 三张 `1280×720` 同一 `turn=1 / shield=wall_hung / rescue=active / swarm_survivors=6` 状态捕获及连续滚动录像；每张登记 camera/source rect、loaded slots、PNG SHA 与 gameplay/state signature；
3. 遮挡区内馆守 Z 的淡出＋轮廓，离开后恢复；
4. `STATE_LAYERS` 未加载且盾只绘制一次的证据；
5. 缺单层、坏单层 SHA、坏 receipt SHA、缺 active 配置的 fail-closed 测试；
6. 显式零 handoff 模式与 M2.1/M2.2 几何基线保持一致；
7. 20 次确定性重放、五类恢复、旧存档拒载、Full/Skip 等价、E02 P1 Checkpoint 全部保持；
8. 无参数默认入口、M6/legacy 显式入口、Windows 资源验证与全量 Godot 回归通过；
9. Canon report/strict、authority、smoke、分层看板及 `git diff --check` 通过。
10. 另交一张 EAST 阶段后状态截图，证明真实地图没有冻结盾、撤离线、小体幸存数或 P1 状态。

视觉捕获必须同时报告 gameplay/state signature，证明只是显示层变化。

## 7. 写入范围

允许写：

- 上述 `approved_runtime_assets_r2/a4_map_b/**` 五个字节级副本；
- Candidate-local 的 active-art 配置与 validated receipt；
- 为默认显式加载、fail-closed 和审计所必需的 Runner 局部代码；只有 Runner 无法在现有接口完成时才允许最小修改 R2 Godot resolver，Python resolver 与 schema 只读；
- 对应 R2/M2.4 新测试、捕获驱动和专项测试脚本；
- `scripts/test_c01_candidate_asset_r2_m2_2.sh`：所有旧零-handoff路径显式设置新 disable 开关，并把“生产资产根必须不存在”改为“只允许制作人授权的五个文件且静态 manifest 仍为零 handoff”；
- `game-godot/scripts/startup_router_smoke_test.gd`：默认 Current Runner 改验 validated/loaded/probes=5 与 runtime art=true，disable模式另验0/0/0与false；
- `game-godot/scripts/candidate_runtime_demo/c01/e02/asset_integration_r2/audit_active_asset_lane_r2.py`：把 active config/receipt 纳入明确白名单与旧资产 denylist；
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m2-4/**`。

禁止写：

- A4/A5 美术源、Canon、剧情、C04、玩法、数值、存档、地图拓扑；
- `project.godot`、Autoload、startup router/selector、现有 Current 稳定启动脚本、正式 Runtime、LibTV；
- `candidate_tactical_session.gd`、local state/save、episode/profile/build identity 和现有场景文件；
- 馆守 Z/BREAKER/小体/重盾真实资产；
- `asset_slot_manifest_r2.json` 的 `approved_handoffs` 注册基线；
- 第二套 Demo 或新 build/profile/save 身份。

不 `git add/commit`。

缺/坏资源测试必须使用隔离夹具或临时副本，不得原地篡改五个生产 PNG、正式 receipt 或 active 配置。

## 8. 停止门

完成后交：

- 五槽 validated receipt 与 SHA；
- active-art 配置与 SHA；
- 五槽加载/八槽 fallback 台账；
- 三机位、滚动、遮挡与盾不重影证据；
- 回归摘要、完成报告与交付哈希。

随后停止，等待用户联合试玩。不得自行接 A5 atlas、修 A4 状态层、接其他美术或升级正式 Runtime。
