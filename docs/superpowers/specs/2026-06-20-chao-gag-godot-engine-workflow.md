# 超GAG机器人大战 Godot 引擎验证与工作流记录

日期：2026-06-20  
目标：确认 Godot 是否能作为《超GAG机器人大战》的正式原生游戏底座，并建立 Codex 可持续工作的 CLI 流程。

## 结论

Godot 4.7 已在本机安装并验证可用。它可以作为后续主工程方向，原因不是“画面天然更好”，而是它把战棋地图、原生窗口、资源导入、动画、输入、导出这些游戏开发问题放回了游戏引擎语境里。

Codex 后续不应该通过 Computer Use 全程点编辑器。正确工作流是：

1. 直接编辑 `.gd`、`.tscn`、`.tres`、数据文件和资源文件。
2. 用 CLI 导入资源、跑逻辑测试、启动原生窗口。
3. 用截图只做视觉验收。
4. Godot 编辑器只作为人工检查和复杂场景编辑工具，不作为 Codex 的主操作界面。

## 当前落地内容

新增 `game-godot/`，这是一个最小但真实运行的 Godot 4 战棋骨架：

- `project.godot`：Godot 项目配置。
- `scenes/main.tscn`：主场景。
- `scripts/tactical_model.gd`：纯逻辑战棋模型，包含单位、移动、攻击、行动消耗、敌方回合。
- `scripts/main.gd`：斜 45 度棋盘渲染、单位绘制、鼠标/键盘输入、左右信息面板、指挥菜单。
- `scripts/cli_smoke_test.gd`：headless 烟测，验证移动、攻击、行动消耗、回合循环。

新增根目录脚本：

```bash
./scripts/godot-import.sh
./scripts/godot-test.sh
./scripts/godot-run.sh
./scripts/godot-screenshot.sh /tmp/chao-gag-godot-screen.png
```

## 已验证

环境：

```text
Godot 4.7.stable.official.5b4e0cb0f
macOS / Apple M2 Max
OpenGL API 4.1 Metal Compatibility
```

验证项：

- `godot --version` 正常。
- `./scripts/godot-import.sh` 正常导入项目。
- `./scripts/godot-test.sh` 通过，输出 `CLI smoke test passed`。
- `./scripts/godot-screenshot.sh` 能启动原生 Godot 窗口并截图。
- 最新运行日志未出现 `SCRIPT ERROR` / `ERROR`。

截图验证内容：

- 原生窗口标题为 `Chao GAG Robot Wars Godot Prototype (DEBUG)`。
- 画面包含斜 45 度棋盘。
- 画面包含玩家单位、敌方单位、移动/攻击菜单、行动队列、敌方意图和状态栏。

## 当前原型功能边界

已经具备：

- 玩家单位选择。
- 斜 45 度棋盘坐标和屏幕坐标转换。
- 移动范围高亮。
- 攻击范围目标高亮。
- 攻击无目标时不会锁死，能取消或改选移动/待机/结束回合。
- 玩家行动消耗。
- 简单敌方回合。
- CLI 逻辑测试。

尚未具备：

- 正式剧情流程。
- 探索/AVG/管理模式。
- 战斗动画分镜。
- 数据化关卡加载。
- Web 导出。
- 正式美术管线。

## 关键技术判断

1. Godot 更适合承担正式战棋底座。

当前网页 demo 的问题不是 CSS 能不能救，而是它缺少游戏引擎的输入、场景、动画、资源和状态管理结构。继续在网页上堆会让战斗、探索、剧情和管理越来越像拼页面。

2. Phaser 仍可做浏览器 demo，但不应作为最终主线。

Phaser 可以做 2D 游戏，但项目目标已经从“网页可点”转向“Steam 独立游戏体量和质感”。Godot 的原生开发、导出、编辑器、动画和场景体系更贴合。

3. Codex 可以有效开发 Godot，但要保持 CLI-first。

Godot 的 `.tscn` 和 `.tres` 是文本资源，适合 Codex 修改。复杂美术和关卡可以先数据化，再在编辑器里检查。截图是验收，不是开发方式。

4. 后续要避免中文路径带来的原生窗口/工具链不确定性。

当前脚本通过 `cd game-godot && godot --path .` 运行，避免把完整中文路径传给 Godot。后续如果做桌面构建，也建议导出到 ASCII 路径下。

## 下一步建议

下一步不是继续堆完整第一章，而是先把 `game-godot/` 从“最小战棋骨架”升级为“可承载第一话的四模式底座”：

1. 数据层：把单位、关卡、剧情节点、探索物件、战斗目标拆成 JSON/TSV。
2. 场景层：建立 `ModeController`，统一切换 `dialogue / exploration / battle / intermission`。
3. 战斗层：保留当前模型，但拆出行动状态机和目标选择器。
4. 演出层：加入轻量相机、屏幕震动、cut-in 立绘位、攻击小动画。
5. 验证层：扩展 headless tests，覆盖“攻击范围无目标不锁死”“结束回合”“剧情推进到战斗再回剧情”。

这会比直接把现有网页 demo 翻译成 Godot 更稳，因为我们需要的是游戏骨架，不是页面复刻。

