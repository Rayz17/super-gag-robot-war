# C01E02 A6 角色通讯 UI Candidate 完成报告

> Package: `C01CDV1_A6_CHARACTER_COMMS_UI_R05_CANDIDATE`
>
> Status: `candidate art package complete for U1 judgment / user approval pending`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## Result

- 纪存：`focused / alarm / resolve` 三张 `768×768 RGBA` 状态母版，按 `focused;alarm;resolve` 横排为 `2304×768` atlas。
- 七海：`controlled / decision / concerned` 三张 `768×768 RGBA` 人物母版，保留独立 `remote-noise-mask-768.png`，并按冻结顺序横排为 `2304×768` 评审 atlas。
- 旧守护者：`guide / contact / shield_gaze` 三张 `1024×768 RGBA` 通讯母版，每态保留 `body / head / chest / waveform` 源层，按冻结顺序横排为 `3072×768` atlas。
- 兜灯：只引用外部已批准 `OBSERVE/TENSE` 原件制作适配板和模拟图；保持 3:1 比例整幅缩放，无裁切、无变形、无原件改写、无 A6 新母版。
- 评审输出：3 张人物状态板、1 张兜灯适配板、1 张左/右占位与长文安全区板、1 张透明边缘板，以及 3 张 `1280×720` 通讯模拟图。

## Qihai Correction

活动 `decision` 已按制作人中途复核局部纠偏：嘴唇闭合，下颌与眼神更坚定，身份、服装、平板与构图不变。旧张嘴源图更名为 `qihai-decision-speaking-drift-rejected-source.png` 留作拒绝轨迹，不进入状态母版、atlas 或模拟图。

七海的明确消费者是规划侧栏 `presence_cards/R05_PRESENCE_QIHAI_REMOTE`，不是 `character_comms` 台词。模拟图中：

- portrait 使用闭口 `decision` 和远程 noise mask；
- 留出姓名“七海”、来源“代哥东区封存中心”、状态“本人停机令已撤回”的程序安全区；
- 不烘入上述文字，`line_text` 为空；
- 无按钮、目标线、行动点、火力图标或可操作提示，不给七海新增命令/炮火权。

## Validation

- `40-c01e02-m3-r0-5-frozen-contracts.sha256`: 更新 ledger 全项 `OK`，包含 `41/42/43/44`。
- `validate_delivery.py`: 校验 3 张 atlas 的真实尺寸、9 格顺序、单格像素一致、alpha bbox、safe rect、外缘透明和绿边比例；校验七海 mask 与旧守护者必需源层。
- `alpha-edge-review-board-1280x720.png`: 使用明暗格底板直观检查 9 态透明边缘。
- `asset-manifest.tsv`: 逐文件登记 `source_tool / rights_note / forbidden_states / lifecycle / runtime_allowed / runtime_handoff / sha256`。

## Deferred And Stop Gate

- 未获用户 U1 批准，不产生用户验收回执、不自签 exact handoff。
- 未写 Godot、Canon、合同、Runner、runtime assets 或 `character_comms.json/presence_cards` 数据。
- 七海真实程序接入、名称/来源/状态文字渲染与无交互权限测试等待 U1 与制作人 P1 exact handoff。
- 当前所有 A6 文件继续 `Candidate / runtime_allowed=false / runtime_handoff=none`。

## Mandatory Claim Boundary

```text
Claim level: presentation judgeability only
General common-turn causality: NOT PROVEN
Editable route/waypoints: NOT IMPLEMENTED
Commit summary completeness: INCOMPLETE IN FROZEN R0
Derived mutation/settlement evidence: NOT PROVEN
Actual route hash: NOT IMPLEMENTED
R1 readiness: BLOCKED BY PRODUCTION BOARD HARD GATES
```

机器 PASS、视觉 PASS 或用户喜欢都不会自动关闭上述 R1 硬门。
