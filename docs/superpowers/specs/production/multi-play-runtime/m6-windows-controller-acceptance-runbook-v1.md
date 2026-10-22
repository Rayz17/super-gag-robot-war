# 《超GAG机器人大战》M6 Windows 真机与实体手柄验收手册 v1

> 日期：2026-07-15  
> 状态：`ready_for_external_validation`；验收器已实现，真实 Windows/手柄回执尚未产生。  
> 适用制品：`outputs/windows/chao-gag-m6-validation.exe`  
> Canon 边界：本手册只验收候选多玩法运行时，不提升正式 C02E03，不解冻 V35.10。

## 1. 为什么需要这套验收

EXE 导出成功只证明制品能被构建；合成 `InputEventJoypad*` 通过只证明代码路径成立。平台门禁真正需要回答：

1. 官方 Windows x86_64 制品能否在 Windows 真机启动并走完五节点。
2. 实体手柄是否真的操作了叙事、探索、`CONSTRAINT/TIMING`、战棋和 Desk，而不是只被系统枚举。
3. 中文字形、斜 45 度地图、侧栏、对话和提示在 Windows 缩放下是否仍可读。
4. `user://` 是否能写出完整 M6 回执，五个事务是否恰好提交一次。

## 2. 回执 v2 的证据边界

M6 可视入口现在聚合记录：

- 运行系统与 Godot 版本。
- 启动时已连接手柄数量。
- `keyboard / mouse / joypad` 的意图次数。
- 手柄在 `narrative / spatial / activity / tactical / desk` 上下文中的使用次数。
- 手柄在 `m6_intro / m6_workshop / m6_tactical / m6_reaction / m6_desk` 各节点的使用次数。
- 按下与松开分开计数，用于证明 `TIMING` 长按/释放链。

不记录原始按键序列、手柄名称、厂商/VID/PID、用户路径或网络信息；回执只写本机，不上传。

## 3. 验收前提

- Windows 10/11 x86_64。
- 一只能被 Windows 识别的 XInput/SDL 手柄。
- 仓库中的 EXE 与 `chao-gag-m6-validation-build.json` 成对存在。
- 测试者愿意用手柄走完整个 M6，而不是进入后立即退出。

## 4. 一键流程

在仓库根目录打开 Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows-m6-platform-acceptance.ps1
```

验收器会：

1. 按构建 manifest 校验 EXE SHA-256，哈希不一致则拒绝启动。
2. 启动 M6，等待游戏进程关闭。
3. 读取 `%APPDATA%\Godot\app_userdata\Chao GAG Robot Wars Godot Prototype\chao_gag_playtests\latest-m6.json`。
4. 检查新回执是否来自 Windows、是否完成五节点和五次提交。
5. 检查手柄是否在五节点和五种输入上下文中都留下了真实意图。
6. 请测试者确认中文字形和布局没有缺字/荒谬遮挡。
7. 将结果写到 `outputs/windows/acceptance/m6-windows-acceptance-*.json`。

## 5. 测试者必须怎样玩

- 插好手柄后再启动验收器。
- 开场叙事用 A 推进。
- 维修棚用左摇杆或 D-pad 行走，用 A 调查。
- `CONSTRAINT` 中用导航、A、X 和 Start 完成至少一次安排与提交。
- `TIMING` 中用 A 按下与松开完成三段取样。
- Tactical 中用手柄选中单位、移动/攻击/待机，并至少打开一次 Start 阶段菜单。
- 战后反应与 Desk 都用 A 确认。
- Desk 显示完成后关闭游戏窗口，让 PowerShell 继续检查。

## 6. 通过条件

| 门禁 | 机器证据 | 通过条件 |
| --- | --- | --- |
| 制品身份 | EXE SHA-256 | 与 build manifest 一致 |
| Windows 运行 | `runtime_environment.os` | 等于 `Windows` |
| 流程完成 | `status / node_visits / commit_count` | `completed`，五节点各至少一次，提交恰好五次 |
| 真实手柄 | `connected_joypad_count_at_start` | 大于 0 |
| 跨模式手柄 | `device_context_counts.joypad` | 五种上下文均大于 0 |
| 跨节点手柄 | `device_node_counts.joypad` | 五个 M6 节点均大于 0 |
| 字形 | 测试者回答 | 无 tofu 框、无缺字 |
| 布局 | 测试者回答 | 地图、菜单、文本无荒谬重叠 |

只有全部成立时，验收器才输出 `windows_runtime_controller_visual_passed` 并以退出码 0 结束。跳过人工视觉问题时，最高只能得到 `runtime_controller_passed_visual_pending`。

## 7. 失败不能被怎样解读

- 某个节点没有 joypad 记录，不能用“其他地方能用手柄”覆盖。
- 流程完成但字形失败，不是平台验收通过。
- 回执存在但时间早于本次启动，视为旧证据。
- 自动化事件通过不能代替这份外部回执。
- 本门禁通过也不等于真人剧情可理解性、实际时长或正式 Episode 内容验收通过。
