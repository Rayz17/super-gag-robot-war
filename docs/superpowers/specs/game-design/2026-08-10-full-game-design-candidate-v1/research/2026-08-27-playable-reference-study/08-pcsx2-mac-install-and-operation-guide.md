# 08｜PCSX2 在这台 Mac 上的安装、使用与研发操作指南

> Checked: `2026-08-28`
>
> Audience: 用户本人，以及后续使用 Codex／Cursor 做玩法调研的人。
>
> Current truth: PCSX2 官方 Nightly `2.7.524` 已经安装、完成初始配置并通过退出后重启复验；目前没有 PS2 BIOS 和游戏镜像，因此还没有任何商业游戏的本机运行结论。

## 1. 先说最重要的结论

这台 Mac 上现在只保留一个 PCSX2：

| 应用 | 版本 | 当前判断 | 是否使用 |
| --- | --- | --- | --- |
| `/Applications/PCSX2-v2.7.524.app` | 官方 Nightly `2.7.524` | 包含官方内存映射修复；已进入中文主界面并完成退出—重启复验 | **本轮固定使用** |

曾经安装的 Homebrew 稳定版 `2.6.3` 因本机 Rosetta 虚拟内存映射失败，已于 `2026-08-28` 使用 `brew uninstall --cask pcsx2` 卸载。其故障证据仍保留在研究记录中。

最省事的启动方式，是双击：

`/Users/rayz/Games/PS2/Launch PCSX2 Research.command`

启动后先看窗口标题。必须显示：

```text
PCSX2 v2.7.524
```

如果标题不是 `v2.7.524`，请退出后改用上面的启动文件。

当前已经确认的是“模拟器应用和配置环境可以启动”，还没有确认“某款游戏可以玩”。要进入游戏，仍需两样东西：

1. 从自己实际拥有的 PS2 主机导出的 BIOS；
2. 从自己实际拥有的游戏光盘制作的镜像。

“只是测试一下”“测完不传播”或“游戏已经绝版”不会自动给网络 ROM／ISO／BIOS 增加授权。本文不是法律意见；实际使用仍应遵守所在地法律、许可条款及技术保护规则。PCSX2官方也明确要求 BIOS 来自用户自己的主机，并说明没有可替代的开源 BIOS：[BIOS 官方指南](https://pcsx2.net/docs/setup/bios/)。

## 2. 本次实际完成了什么

### 2.1 安装与安全核验

- 曾安装并完成故障定位、现已卸载的 Homebrew 稳定版：`2.6.3`；
- 另行安装的官方 Nightly：`2.7.524`；
- Nightly 下载自 [PCSX2 官方 GitHub 发布页](https://github.com/PCSX2/pcsx2/releases/tag/v2.7.524)；
- 下载包 SHA-256：`f772a91ea3444258a27df28831c7b9b39387f034e44b60fac2ebb8b5414b31fe`；
- 应用签名者：`Developer ID Application: Ty Lamontagne (PTMR35SWS3)`；
- macOS Gatekeeper 判定为已公证的开发者应用；
- Rosetta 2 已安装并运行。PCSX2当前在 M 系列 Mac 上经 Rosetta 2 工作，这与[官方系统要求](https://pcsx2.net/docs/setup/requirements/)一致。

### 2.2 为什么不用稳定版

稳定版 `2.6.3` 在本机日志里出现：

```text
mach_vm_map() failed
Failed to map data memory at an acceptable location.
Failed to allocate VM memory.
```

这不是 96GB 内存不够，而是虚拟地址空间无法按旧方式映射。PCSX2在 2026-03-28 合入 [PR #11734](https://github.com/PCSX2/pcsx2/pull/11734)，允许把主内存映射到其他可用位置；该修复晚于稳定版 `2.6.3`，但已经包含在 `2.7.524` 中。

Nightly 已在同一台 Mac 上完成：

```text
首次启动
→ 中文设置向导
→ 主界面 v2.7.524
→ 正常退出
→ 使用固定数据目录重新启动
→ 再次进入 v2.7.524 主界面
```

Nightly 日志没有再出现上述三个内存映射错误。由于当前没有 BIOS 和游戏，这仍不是模拟执行、画面、声音、存档或某个标题兼容性的证明。

本次重启后的主界面截图、日志和边界说明保存在：

```text
/Users/rayz/Games/PS2/Evidence/PCSX2-environment/2026-08-28-install/
```

## 3. 已建好的目录

游戏和模拟器数据没有放进《超GAG机器人大战》仓库，避免把专有资产、存档或大文件混入项目。

```text
/Users/rayz/Games/PS2/
├── BIOS/                              # 只放自己PS2导出的BIOS文件组
├── DiscImages/
│   ├── Original/                     # 自有光盘的原始转储
│   └── Patched/                      # 自己应用差分补丁后的副本
├── PCSX2Data/
│   └── v2.7.524/
│       └── PCSX2/                    # 配置、记忆卡、即时存档和日志
├── Evidence/                         # 自己的测试截图、短片和观察记录
└── Launch PCSX2 Research.command     # 双击启动固定研究环境
```

当前 PCSX2 已配置为：

- BIOS 目录：`/Users/rayz/Games/PS2/BIOS/`
- 游戏扫描目录：`/Users/rayz/Games/PS2/DiscImages/`
- 扫描子目录：开启
- 数据目录：`/Users/rayz/Games/PS2/PCSX2Data/v2.7.524/PCSX2/`
- 自动更新：关闭，避免一次研究中途换版本
- 在线成就：关闭
- 控制器 1：默认键盘映射
- 图形 API：自动
- 内部分辨率：原生 1x
- 宽屏／反隔行补丁：关闭

## 4. 你实际怎样开始用

### 4.1 第一步：准备自己的 BIOS

PCSX2不能在没有 BIOS 的情况下运行游戏。官方推荐的基本流程是：

1. 在自己拥有的 PS2 上准备 FreeMcBoot 或适用的 FreeDVDBoot 环境；
2. 从官方指南链接取得 `biosdrain`；
3. 用 FAT32、MBR 格式的 U 盘在 PS2 上运行 `biosdrain.elf`；
4. 等它明确提示完成；
5. 把输出的完整文件组复制到：

```text
/Users/rayz/Games/PS2/BIOS/
```

常见输出包括以主机型号开头、以 `.rom0`、`.rom1`、`.nvm` 等结尾的文件。保留同一次导出的整组文件，不要只挑一个。

然后：

1. 双击 `Launch PCSX2 Research.command`；
2. 打开 `设置 > BIOS`；
3. 点击`刷新列表`；
4. 选中识别出的 BIOS；
5. 关闭设置窗口。

完整步骤、兼容方法与校验方式见[PCSX2 BIOS 官方指南](https://pcsx2.net/docs/setup/bios/)。如果需要格式化 U 盘，这一步会清空所选磁盘；务必先确认选中的确是 U 盘，并备份其中资料。

### 4.2 第二步：把自己的游戏光盘制作成镜像

推荐从镜像运行，不建议把实体光盘当作长期研究介质。官方说明 PS2 游戏使用普通 DVD 或 CD，标准光驱可以读取：[光盘转储官方指南](https://pcsx2.net/docs/setup/discs/)。

DVD 游戏在 Mac 上可这样做：

1. 用 USB 光驱放入自己的 PS2 DVD；
2. 打开 macOS`磁盘工具`；
3. 在左侧选中游戏光盘，不要选中系统盘或其他硬盘；
4. 使用`文件 > 新建映像 > 来自“光盘名称”的映像`；
5. 映像格式选择`DVD/CD 主映像`；
6. 完成后会得到 `.cdr`；
7. 按官方说明把扩展名改为 `.iso`；
8. 放到：

```text
/Users/rayz/Games/PS2/DiscImages/Original/
```

蓝底 PS2 CD 不应直接套用 DVD 流程。官方给 macOS／Linux 的 CD 路径使用 `cdrdao`，产出 `.bin` 数据；具体命令和多音轨注意项以官方页面为准。

PCSX2当前会扫描这些格式：`.bin`、`.iso`、`.mdf`、`.chd`、`.cso`、`.zso`、`.gz`。

### 4.3 第三步：让游戏出现在列表中

镜像放入 `DiscImages` 后：

1. 启动 PCSX2；
2. 选择`设置 > 扫描新游戏`；
3. 仍未出现时选择`设置 > 重新扫描所有游戏`；
4. 检查标题、区域和序列号是否合理。

临时打开一个不在游戏目录里的文件，可以使用：

```text
系统 > 启动文件...
```

### 4.4 第四步：启动游戏

最简单的方法是双击游戏列表中的条目。右键游戏时常用的启动方式是：

- `默认启动`：使用当前全局或该游戏的设置；
- `快速启动`：跳过 PS2 开机动画；
- `完整启动`：经过完整 BIOS 启动，适合排查区域、记忆卡或启动问题。

第一次测试某款游戏时，按下面顺序：

```text
默认设置、原生1x、窗口模式
→ 能进入标题画面
→ 能进入第一段实际操作
→ 画面、声音、输入无明显错误
→ 游戏内记忆卡保存并重新读取
→ 再单独提高分辨率或开补丁
```

不要一开始同时开 4K、宽屏、反隔行、汉化、作弊和大量图形修正，否则出现问题时无法知道是哪一项导致的。

## 5. 键盘、手柄和 Codex 操作

### 5.1 当前默认键盘

| PS2 输入 | 当前默认键盘 |
| --- | --- |
| 方向键 | 方向键 |
| 左摇杆 | `W / A / S / D` |
| 右摇杆 | `T / F / G / H` |
| Triangle | `I` |
| Circle | `L` |
| Cross | `K` |
| Square | `J` |
| L1 / R1 | `Q / E` |
| L2 / R2 | `1 / 3` |
| L3 / R3 | `2 / 4` |
| Start | `Return` |
| Select | `Delete / ⌫（Backspace）` |

这套映射适合 Codex 用截图加键盘操作回合制／菜单型游戏。动作游戏、压力感应按键和精确双摇杆仍应由真人手柄完成。

### 5.2 接手柄

1. 先在 macOS 蓝牙或 USB 中连好 DualSense、DualShock 4 或其他手柄；
2. 打开`设置 > 控制器`；
3. 保持`控制器端口 1 > DualShock 2`；
4. 输入源优先使用官方推荐的 `SDL`；
5. 点击`自动映射`并选择手柄；
6. 实际进入游戏菜单检查方向、确认、取消、摇杆和震动。

DualSense／DualShock 4 用户可以启用对应的增强模式。真正的 DualShock 2 压力感应不能由普通现代手柄完整替代；PCSX2提供`Pressure Modifier`作为有限替代。详见[控制器官方说明](https://pcsx2.net/docs/configuration/controllers/)。

PCSX2界面目前没有内置完整输入测试器，因此“自动映射成功”不等于每个按键都已实测。

### 5.3 常用模拟器快捷键

| 操作 | 默认按键 |
| --- | --- |
| 保存当前即时存档槽 | `F1` |
| 下一个槽 | `F2` |
| 上一个槽 | `Shift + F2` |
| 读取当前槽 | `F3` |
| 开关速度限制 | `F4` |
| 切换隔行模式 | `F5` |
| 切换画面比例 | `F6` |
| 截图 | `F8` |
| 切换软件／硬件渲染 | `F9` |
| 暂停／继续 | `Space` |
| 暂停菜单 | `Escape` |
| 快进开关 | `Tab` |
| 全屏 | `Option + Return` |

Mac 的功能键可能先控制亮度或媒体，需要按 `Fn + F键`，或者在`设置 > 热键`里改成不冲突的组合。

## 6. 这台 M2 Max 的图形设置

当前保守基线已经设好：

```text
图形 API：自动（默认）
内部分辨率：原生（PS2）1x
高宽比：自动标准
反交错：自动
宽屏补丁：关
反隔行补丁：关
```

PCSX2官方建议不确定时保持`自动`，让程序先以稳定性、再以准确性选择图形 API：[图形 API 官方说明](https://pcsx2.net/docs/configuration/general/)。

一款游戏完成原生基线后，可以在该游戏上单独试：

1. `3x Native`，大致对应 1080p 档；
2. 画面和速度稳定，再试 `4x Native`；
3. 出现阴影、文字线、粒子或混合错误时，先恢复该游戏默认；
4. 再用 `F9` 比较软件渲染，确认是原作问题还是硬件渲染问题。

每个游戏的问题用右键`属性`单独调整，不要因为一款游戏改坏全部游戏的全局设置。

## 7. 存档、截图、录像和日志

### 7.1 长期进度用记忆卡

当前记忆卡目录：

```text
/Users/rayz/Games/PS2/PCSX2Data/v2.7.524/PCSX2/memcards/
```

长期进度必须用游戏自己的保存功能写入记忆卡。即时存档只是临时书签，不是游戏存档；PCSX2官方不保证即时存档跨版本兼容：[即时存档说明](https://pcsx2.net/docs/configuration/general/#save-states)。

### 7.2 即时存档

目录：

```text
/Users/rayz/Games/PS2/PCSX2Data/v2.7.524/PCSX2/sstates/
```

适合：快速重试、暂时离开、固定研究观察点。

不适合：唯一长期进度、跨版本迁移、带着作弊或补丁反复覆盖同一档。

### 7.3 截图和录像

```text
截图：/Users/rayz/Games/PS2/PCSX2Data/v2.7.524/PCSX2/snaps/
录像：/Users/rayz/Games/PS2/PCSX2Data/v2.7.524/PCSX2/videos/
```

截图可用`系统 > 截图`或 `F8`；录像可用`系统 > 视频捕获`。第一次研究不要边 4K 升频边高码率录像，先确认游戏本身稳定。

建议每次正式观察另建：

```text
/Users/rayz/Games/PS2/Evidence/游戏名/YYYY-MM-DD-session/
├── notes.md
├── screenshots/
├── clips/
└── emulog.txt
```

日志原位于：

```text
/Users/rayz/Games/PS2/PCSX2Data/v2.7.524/PCSX2/logs/emulog.txt
```

重现故障后先退出 PCSX2，再复制日志，避免下一次启动覆盖关键上下文。

## 8. 给 Cursor／Codex 的固定启动方式

### 8.1 只启动主界面

```bash
open '/Applications/PCSX2-v2.7.524.app' --args \
  -datapath '/Users/rayz/Games/PS2/PCSX2Data/v2.7.524' \
  -nofullscreen
```

不要在 PCSX2 已经运行时再执行一次命令；这可能让两个进程同时写同一套配置。日常请优先双击固定启动文件，它会先检查是否已有 Nightly 或稳定版进程。

### 8.2 启动一个用户自有镜像并单独写日志

先退出已经运行的 PCSX2，再创建本次证据目录并启动：

```bash
mkdir -p '/Users/rayz/Games/PS2/Evidence/游戏名/日期-session'

'/Applications/PCSX2-v2.7.524.app/Contents/MacOS/PCSX2' \
  -datapath '/Users/rayz/Games/PS2/PCSX2Data/v2.7.524' \
  -batch \
  -nofullscreen \
  -logfile '/Users/rayz/Games/PS2/Evidence/游戏名/日期-session/emulog.txt' \
  -- '/Users/rayz/Games/PS2/DiscImages/Original/游戏名.iso'
```

`-datapath`、`-batch`、`-logfile`和`--`均为[PCSX2官方命令行参数](https://pcsx2.net/docs/advanced/cli/)。

### 8.3 两种 Agent 能做什么

| 工作 | Codex桌面版 | Cursor默认 Agent |
| --- | --- | --- |
| 启动固定版本和读取日志 | 可以 | 可以 |
| 整理截图、配置与研究记录 | 可以 | 可以 |
| 操作 PCSX2 原生菜单 | 可以使用本机 Computer Use | 默认不具备，需要额外受限的 GUI 控制层 |
| 看游戏画面并按键 | 可以用截图和键盘做低速操作 | 默认只能分析已有文件 |
| 精确摇杆、压力键、实时动作 | 不可靠 | 默认不能 |

最适合 Agent 亲自体验的是《Front Mission 4/5》《Ring of Red》的菜单与战略阶段、《机战OGs》以及《樱花大战V》的 ADV／回合段。`Robot Alchemic Drive`等高频双摇杆动作仍应由真人操作，Agent负责截图、日志和观察整理。

## 9. 常见问题

### 9.1 启动后的版本不是 v2.7.524

当前稳定版已经卸载。若仍显示其他版本，说明打开了另一份旧应用或绕过了固定启动文件。

处理：退出，双击`Launch PCSX2 Research.command`，确认标题是 `v2.7.524`；不要用 Finder 搜索结果里来源不明的旧副本。

### 9.2 出现 `mach_vm_map` 或 `Failed to allocate VM memory`

先确认版本。稳定版 `2.6.3`曾在这台 Mac 触发该错误，现已卸载；本轮应固定用 `2.7.524`。如果官方 Nightly 也出现，保存完整日志，不要先反复换渲染器或删除配置。

### 9.3 提示没有 BIOS

这是当前预期状态。把自己主机导出的完整 BIOS 文件组放入`/Users/rayz/Games/PS2/BIOS/`，再到`设置 > BIOS > 刷新列表`选择它。

### 9.4 游戏列表为空

当前也是预期状态，因为没有游戏镜像。已有自有镜像时检查：

1. 文件是否放在 `DiscImages`；
2. 扩展名是否受支持；
3. `设置 > 扫描新游戏`；
4. 仍失败时使用`系统 > 启动文件...`。

### 9.5 黑屏或加载卡死

1. 先恢复原生 1x、自动图形 API、关闭补丁；
2. 在游戏属性中执行镜像校验；
3. 重新从自己的光盘制作镜像；
4. 用 `F9` 比较软件渲染；
5. 保存 Game ID、PCSX2版本、设置和日志。

### 9.6 手柄能连 Mac，但游戏不响应

1. `设置 > 控制器`确认 Port 1 不是`未连接`；
2. 保持 SDL，重新`自动映射`；
3. 在游戏菜单实测确认／取消和方向；
4. 完全退出 Steam，排除 Steam Input 桌面映射重复发送按键；
5. 第三方手柄仍错位时再做手动映射。

## 10. 本轮怎样判定“测试完成”

不要把下面四件事混成一句“能玩”：

| 层级 | 现在的状态 | 能证明什么 |
| --- | --- | --- |
| 应用安装 | 已完成 | 官方应用存在，签名、公证和架构可核验 |
| 环境启动 | 已完成 | Nightly能在本机进入主界面并保存配置 |
| BIOS与镜像启动 | 未完成 | 需要用户自有 BIOS 和自有光盘转储 |
| 指定游戏观察 | 未完成 | 需要进入具体任务、验证输入／画面／声音／存档并形成记录 |

所以当前准确说法是：

> PCSX2研究环境已经装好；目标游戏仍是本机`L0未实测`。用户提供合法自有 BIOS 和镜像后，Codex可以继续完成标题级烟测与玩法观察。

## 11. 更新与移除

本轮研究应固定 `2.7.524`，不要中途自动更新。以后若稳定版明确包含 PR #11734 或发布 `2.8+`，先另开一个数据目录烟测，再决定是否迁移；迁移前务必用游戏内记忆卡保存。

当前稳定版 `2.6.3`已经通过 `brew uninstall --cask pcsx2`移除。以后若不再需要剩余环境：

- Nightly 是并排安装的独立应用，可在 Finder 中只把`/Applications/PCSX2-v2.7.524.app`移到废纸篓；
- `/Users/rayz/Games/PS2/`里有配置、存档和用户自己的资产，不应随应用一起随意删除。

本轮只删除了不能使用的稳定版应用；没有删除 Nightly、BIOS、游戏、存档、研究证据或项目文件。稳定版可通过 Homebrew 重新安装，但没有恢复它的必要。
