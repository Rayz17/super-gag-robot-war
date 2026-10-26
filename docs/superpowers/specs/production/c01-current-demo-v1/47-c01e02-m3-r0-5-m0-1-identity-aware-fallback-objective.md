# C01E02 M3-R0.5 M0.1｜身份感知回退与视觉试玩门目标书

> 上游：`46-c01e02-m3-r0-5-engineering-shell-correction-receipt.md`
>
> 性质：`engineering shell correction / zero real asset / same non-default scene`

## 1. 唯一目标

在不加载任何真实美术、不改变冻结玩法、不覆盖 M0 旧证据的前提下，把 M3-R0.5 零资产 fallback 从“另一套通用设计”修成身份一致的技术 schematic，并让程序明确报告：当前没有真实 loader 和身份关键资产，因此不具备 U2 视觉试玩资格。

## 2. 精确写入 allowlist

- `game-godot/content/candidate_runtime_demo/c01/e02/m3_r05/presentation_profile.json`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_r05/presentation_asset_resolver.gd`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_r05/tactical_board_world.gd`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_r05/player_planning_hud.gd`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_r05/character_comms_layer.gd`
- 必需时只可局部修改同目录 `m3_r05_runner.gd`、`developer_overlay.gd`
- 新增 `game-godot/tests/candidate_runtime_demo/m3_r05/m3_r05_identity_aware_fallback_test.gd`
- 新增 M0.1 专用 capture driver／测试脚本，限同一 `m3_r05` 测试目录与 `scripts/*m3_r05_m0_1*`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m3-r05-m0-1/**`

不得修改旧 `main-m3-r05-shell/**`、`07-implementation-hashes.sha256`、旧截图／AVI／日志／完成报告；不得改默认入口、project.godot、startup、Autoload、Save、R0 resolver/profile、A4/A5 绑定、Canon、Reader、A6/A7 目录或 33-47 制作人合同。

## 3. 必须实现

### 3.1 证据与 loader 状态

- Profile 与运行回执明确 `evidence_class=engineering_shell_evidence_only`。
- 明确 `real_asset_loader_implemented=false`、`user_visual_playtest_eligible=false`。
- Resolver 报告全部身份关键槽的 `portrait_or_identity_unavailable`／fallback 状态；不得谎报真实消费者。
- 为未来 M1 输出 `identity_critical_slots`、`identity_critical_fallback_count`、`u2_block_reasons`。
- 不实现或假装实现真实 loader；这属于未来 M1。

### 3.2 世界 schematic

- 馆守 Z 与 BREAKER 必须逐项满足 46 第 3 节；提供可测试的 `schematic_receipt()` 或等价结构化回执。
- 双方保持 2x2／3x3 footprint、当前 pivot 和相机位置；只替换绘制内容。
- 重盾继续墙挂三旧焦痕；不提前取盾或释放红光。
- 应急车去掉医疗十字，只保留中性的应急车辆技术轮廓与“自动”语义。

### 3.3 Screen schematic 与文案

- 纪存、七海、兜灯不显示首字／加号／伪造脸；显示技术剪影、姓名、来源、职能与 `portrait unavailable` 调试回执。
- 旧守护者使用机头／胸灯／扬声波形，并写“馆守Z本体”。
- 顶栏、角色标签与频道严格按 46 第 4 节修正。
- 七海卡仍非交互、无按钮、无行动图标、无命令和炮火权。
- 兜灯原句继续在规划输入开放前出现一次；不新增台词。

## 4. 测试

至少覆盖：

1. 馆守 Z/BREAKER schematic feature receipt 与 footprint/pivot 不变；
2. 馆守 Z 双前臂完整、右肩旧伤，BREAKER 单红缝／闭合胸缝／封闭出口；
3. 纪存频道是导览席；旧守护者是馆守 Z 本体；七海无动作权；顶栏是“本轮操作：馆守Z”；
4. 应急车不存在医疗十字视觉语义；
5. 九个身份关键槽全部 fallback 时 `u2_eligible=false`；只改 manifest 开关不能使其变 true；
6. M0 原专项测试、R0、M2、M2.5、默认入口、Canon 与全量 Godot 回归不退化；
7. 新截图只写 `main-m3-r05-m0-1/**`，元数据标记 `engineering_shell_evidence_only`。

## 5. 停点

完成 M0.1 后停止。不得读取或接入 A6/A7 文件，不得开始 P1a/P1b/M1，不得邀请用户判断当前工程壳好不好看。完成报告必须列出未来 M1 真实 loader／消费者缺口和当前全部身份关键 fallback 槽。
