# 超GAG机器人大战 C01 macOS 可见窗口键盘验收 v1

> 日期：2026-07-18  
> 状态：`machine_assisted_visible_sample_passed / full_chapter_human_and_device_gates_pending`  
> 范围：正式 `Godot.app`、C01 Chapter Runner、标题、Narrative、Spatial、纪存笔记、存取与窗口伸缩

## 1. 本层回答什么

Headless 原始输入能证明软件路径，却不能证明 macOS 窗口里真的看得见焦点、中文字形和布局。本层通过系统级 Computer Use 操作正式 Godot 窗口，回答：

1. 标题焦点能否用键盘开始和继续。
2. Narrative、Spatial 与笔记本能否在真实窗口接收键盘输入。
3. 笔记本的页签、页内按钮、保存、返回标题和恢复是否可达。
4. `1280x720` 与 `1600x900` 请求窗口下是否出现明显缺字或不连贯遮挡。
5. 验收运行能否与玩家正常存档、回执完全隔离。

## 2. 本轮发现并修复的问题

第一次可见运行进入笔记本“系统”页后发现：页面有“保存进度 / 读取进度 / 保存并返回标题”，但 `Tab` 和方向键被 Chapter Runner 全部解释成切换页签，键盘玩家无法进入页内按钮。

修正后的焦点规则是：

- 左右方向切换五个笔记页签。
- 系统页上下方向进入或移动页内控件。
- 键盘 `Tab / Shift+Tab` 在系统页控件间移动。
- `Enter` 激活当前控件；焦点以金色描边显示。
- 手柄 `LB/RB` 继续只切页签，不与页内控件语义混用。
- 笔记本输入在 `_input` 阶段先于 Godot 原生 GUI 消费，按下与松开各只记录一次。

原始输入走廊因此从 `154/154` 提升为 `172/172`，新增真实 Notebook 系统页聚焦与保存动作。

## 3. 隔离运行

Chapter Runner 新增用户参数：

```text
--acceptance-namespace=<safe-id>
```

该参数只改变验收运行的本地 build id、回执目录和存档槽。普通启动仍使用原来的 `c01_story_first_chapter_manual`；本次样本使用：

```text
c01_story_first_chapter_manual__macos-visible-20260718-a
```

因此可见验收不会覆盖玩家当前进度，也不会把测试 Session 混入默认容量样本。

## 4. 冻结证据

汇总回执：`outputs/c01-macos-visible-acceptance-v01/receipt.json`

| 项目 | 结果 |
|---|---:|
| Godot 可见 Session | 3 |
| 系统级键盘接受意图 | 130 |
| Narrative / Spatial / Overlay | 24 / 37 / 69 |
| 手动保存 / 恢复 | 3 / 2 |
| 冷开场、三小时前、闭馆路线 | 均实际进入 |
| 隔离存档命名空间与当前节点 | 通过 |
| 中文字形、布局、键盘焦点机器复看 | 通过 |

关键截图：

- `00-title-1280x720.png`：新游戏/继续焦点与标题字形。
- `01-spatial-front-hall-1280x720.png`：地图、右侧目标和人物同屏。
- `02-notebook-keyboard-save-1280x720.png`：键盘焦点落在“保存进度”。
- `03-return-title-keyboard-1280x720.png`：保存并返回后继续入口成立。
- `04-title-wide-1600x900.png`：宽窗口标题布局。
- `06-notebook-return-focus-wide-1600x900.png`：宽窗口页内焦点与三组系统按钮。
- `07-spatial-restored-wide-1600x900.png`：读档后恢复前厅 Spatial 状态。

Computer Use 截图包含 macOS 标题栏，并由截图服务缩放；回执记录请求窗口尺寸，但不从 PNG 像素反推 Retina 逻辑尺寸。

## 5. 验证入口

聚合器会校验新鲜 Session、系统、build id、三个节点、三个输入上下文、存取次数、隔离槽、截图格式与两组不同捕获尺寸：

```bash
python3 scripts/summarize_c01_macos_visible_acceptance.py \
  --namespace macos-visible-20260718-a \
  --receipt-dir "<Godot user data>/chao_gag_playtests/c01_story_first/macos-visible-20260718-a" \
  --save-path "<Godot user data>/chao_gag_saves/c01_story_first_chapter_manual__macos-visible-20260718-a.json" \
  --screenshot-dir outputs/c01-macos-visible-acceptance-v01 \
  --output outputs/c01-macos-visible-acceptance-v01/receipt.json \
  --font-readable --layout-clear --focus-visible
```

## 6. 证据边界

当前可以宣称：**C01 在 macOS 正式 Godot 可见窗口中，标题、Narrative、Spatial、Notebook、保存、返回标题和恢复的键盘代表路线，在两种请求窗口尺寸下通过机器辅助验收；中文字形、已捕获布局和页内焦点可读。**

当前不能宣称：

- 真人首次游玩、剧情理解、容量、情感或商业品质通过。
- 可见 Tactical、Desk、话末结算或完整24节点已经由系统键盘走完。
- 鼠标路线、实体手柄、热插拔、震动或辅助设备通过。
- 签名 macOS 独立应用包、Windows、全屏、多显示器或所有对话长度通过。

