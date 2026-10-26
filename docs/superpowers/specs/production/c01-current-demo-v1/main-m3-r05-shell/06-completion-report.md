# C01E02 M3-R0.5 M0｜主程序零资产表现壳完成报告

> 日期：2026-08-18
>
> 状态：`M0 shell evidence complete / non-default / zero real handoff`
>
> 最高结论：`presentation judgeability only`

## 1. 完成内容

- 新增非默认 `M3R05Runner` 与直接启动脚本；默认入口保持 `C01CDV1-M2-R2`。
- 使用冻结 R0 resolver/profile 的只读 adapter，启动时校验二者 SHA；没有修改玩法结果。
- 实现 32×18 全域的 40×20 等距投影、实际 `SubViewport` clipping、规划/结算镜头与具名几何棋盘。
- 实现玩家 HUD、角色信息、3.4 秒局势揭示、可返回摘要、1.15 秒长按提交、B03-B08 共同结算中间视觉状态与结果页。
- 实现 F3 开发层，默认隐藏；正常捕获不显示 hash、receipt、Candidate 或 stop 字段。
- 按 42 重建 28 视觉 + 16 音频槽 manifest/schema/validator，包含 A4、A6 state atlas、A7 atlas、road process 与 48k/24-bit 合同。
- 按 44 选项 B 实现七海远程 presence card；无台词、交互、命令或炮火权，零 probe。
- 在表现层把 `最后应急车 [自动]` 映射为“应急车 / 收尾应急车”，未修改 R0 profile。

## 2. 零 handoff 回执

```text
approved_handoffs=[]
validated_handoff_count=0
loaded_slot_count=0
resource_probe_count=0
runtime_art_loaded=false
```

未读取或探测 A6/A7 输出目录。所有视觉均为具名几何 fallback；音频是程序合成 fallback。42 的 24-bit WAV 仅被 schema/validator 锁定，未形成真实媒体验收。

## 3. 测试与捕获

- Packing、表现语义、UI/44 presence 三组专项测试均 PASS。
- 三个冻结草案在 Full/Skip/fallback 下逐字段语义等价；R0 frozen result hashes 不变。
- 默认 R0、startup、M2、M2.5/A4-A5、V35/current-demo、Canon 与全量 Godot 回归均 PASS。
- 四张 1280×720 PNG 已逐张视觉检查。
- 完整回合 AVI：1280×720、30fps、968 帧、32.266667 秒；中间 B04 帧已抽查，非空且空间连续。

详见 `03-test-summary.md`、`04-capture-manifest.tsv` 与 `logs/`。

## 4. 保护结果

- 未修改 R0 resolver/profile/tests、默认 Runner、`project.godot`、startup、Autoload、Save、A4/A5、Canon/Reader、33-44 或美术目录。
- 所有新增路径均位于 35 号 allowlist。
- 未执行 `git add`、`git commit`。

## 5. 43 第 6 节强制边界

```text
Claim level: presentation judgeability only
General common-turn causality: NOT PROVEN
Editable route/waypoints: NOT IMPLEMENTED
Commit summary completeness: INCOMPLETE IN FROZEN R0
Derived mutation/settlement evidence: NOT PROVEN
Actual route hash: NOT IMPLEMENTED
R1 readiness: BLOCKED BY PRODUCTION BOARD HARD GATES
```

## 6. 遗留项

- 冻结 R0 仍存在 43 所列 hard gates：FrozenIntentSet 因果、可编辑 route/waypoint、完整 commit summary、派生 mutation/settlement 与真实 route hash 均未补齐。
- A6/A7 真实媒体仍需 U1 与制作人 P1 exact handoff；本车道没有权限自行读取或接入。
- 人类试玩与制作人视觉评审尚未发生。

本报告不声明可交接，不声明真实资产完成，不声明一般共同回合因果，也不声明 R1 ready。
