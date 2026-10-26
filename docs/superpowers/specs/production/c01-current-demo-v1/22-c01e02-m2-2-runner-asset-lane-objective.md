# C01E02 M2.2 活动 Runner 资产车道接线目标

> Status: `active / implementation preflight / zero real handoff`
>
> Entry: `res://scenes/candidate_runtime_demo/c01/e02/c01e02_g1_runner.tscn`
>
> Scope: `same in-place Candidate Demo; no parallel v1/v2`

## 1. 本轮目标

把 M2.1 的 Revision-2 resolver 从隔离测试壳接入当前活动 Runner，建立完整的：

```text
producer exact handoff
→ batch preflight
→ frozen validated receipts
→ Godot resource consumption
→ per-slot render or named-geometry fallback
```

本轮没有任何真实美术 handoff，只使用合成测试夹具验证链路。完成后，零 handoff 的试玩必须和当前 M2 在画面、玩法、存档与 Phase P1 上保持不变。

## 2. 冻结身份

```text
contract_revision=2
build_id=C01CDV1-M2-R2
save_schema=2
content_fingerprint=00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4
profile_id=c01cdv1_e02_scroll_m2_r2
topology_sha256=baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8
active_entry=res://scenes/candidate_runtime_demo/c01/e02/c01e02_g1_runner.tscn
approved_handoffs=0
runtime_art_loaded=false
```

权威输入：`19-current-demo-inplace-rebase-producer-contract.md`、`20-c01e02-j2-joint-integration-contract.md`、`main-m2/14-m2-completion-report.md`、`main-m2-1/16-m2-1-test-summary.md`、`main-m2-1/17-m2-1-completion-report.md` 及现有 R2 schema/manifest/resolvers/tests。

## 3. 必须实现

### 3.1 Handoff 预检链

- 在保留现有 `--check-manifest` 的同时，增加明确的批量 handoff 输入与 preflight 入口；不得再靠测试专用代码绕开生产 CLI。
- 逐槽核验 handoff ID、slot、Stable/Subject ID、usage、binding、build、fingerprint、profile、topology、生命周期、授权范围、路径、realpath、SHA、实际媒体参数、pivot、atlas/frame regions、actions/facings。
- 只有元数据授权通过后才触碰资源文件；拒绝隐式搜索、`..`、编码绕过、前缀伪装和 symlink 逃逸。
- 输出可冻结、可哈希、可复核的 validated receipt；失败项不得出现在有效 receipt 中。

### 3.2 Runner 消费链

- 当前 Runner 必须显式调用 R2 resolver；不能继续只在独立 shell test 中证明接口存在。
- 支持逐槽部分装载。一个槽失败只回退该槽的具名几何，不使整个 Demo 失效，也不得悄悄采用其他目录里的相似资产。
- 首批只实现并实测 13 个战棋视觉槽：MAP 六层、馆守 Z/BREAKER/小体三个 Q/SD atlas、重盾四态。
- MAP 支持 base/buildings/roofs/foreground/occlusion mask/state layers 的固定 z-order、相机滚动和状态切换；遮挡采用已批准的“淡出＋轮廓”，路径、目标与意图层保持可读。
- Q/SD 支持四朝向、atlas/frame region、bottom-center pivot 和 2×2/3×3/1×1 footprint；显示层不得改变单位真实 anchor 或碰撞/寻路。
- 重盾四态只读取现有状态机：wall_hung、held_cold、red_blocked、heat_deformed；不得改取盾、挡击或盾拍因果。
- 可保留仅供测试/捕获的灰盒—资产对照开关，但不得写入正式存档、改变游戏状态或建立第二个 Demo 入口。

### 3.3 零 handoff 不变性

默认仓库状态继续为：

```text
approved_handoffs=[]
runtime_art_loaded=false
```

零 handoff 时必须：

- 仍从 `scripts/run_c01_candidate_demo_g1.sh` 进入同一 Runner；
- 现有 M2 WEST/CENTRAL/EAST 捕获及 Full/Skip 语义不变；
- 20 次确定性重放、Checkpoint 磁盘恢复、旧存档拒载、失败重试和 Phase P1 全部通过；
- 不改玩法状态机、单位数、位置、footprint、相机边界、存档 schema 或 build identity。

## 4. 合成夹具测试

只在测试目录或临时隔离目录生成可识别的合成 PNG/atlas/mask/state sheet，不读取、复制或探测美术 Session 的资产目录。

至少覆盖：

1. 13 槽全部合法；
2. 只批准单一槽的部分装载；
3. 坏 hash、错 Stable ID、错 topology、错尺寸/alpha、缺 frame、越界 pivot、路径逃逸；
4. 一个坏槽不影响其他合法槽；
5. 缺屋顶/遮挡/state layer 时精确回退；
6. 四朝向与状态切换实际渲染，而非只返回文件路径；
7. 零 handoff 输出和当前 M2 基线一致；
8. 对照开关不写存档、不改变 Phase payload。

## 5. 交付与写入边界

允许修改当前 C01E02 Candidate lane 内为实现上述目标所必需的 R2 resolver、Runner/场景和专项测试；文档只写：

`docs/superpowers/specs/production/c01-current-demo-v1/main-m2-2/**`

交付至少包括：实现说明、批量 preflight/validated receipt schema、13 槽测试矩阵、零 handoff 哈希回执、三机位程序基线、完整测试日志、完成报告和 delivery hashes。

不得修改 `project.godot` 默认入口、Autoload、共享 Current、Canon、剧情、美术源、正式 Runtime 或 C04；不得 `git add/commit`。

## 6. 停止门

完成合成夹具和零 handoff 回归后立即停止。不得自行把 A1/B1/B2/A2 或任何新 A3 图登记为真实 handoff；不得创建 `approved_runtime_assets_r2` 正式内容。真实资产接入必须等待用户逐项批准与制作人 exact handoff。
