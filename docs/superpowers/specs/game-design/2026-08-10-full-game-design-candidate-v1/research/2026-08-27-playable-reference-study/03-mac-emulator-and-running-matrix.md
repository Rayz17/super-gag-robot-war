# 03｜Mac 模拟器与运行矩阵

> Checked: `2026-08-28`
>
> Local status: PCSX2 Nightly `2.7.524`已经安装、配置并完成退出—重启复验；没有下载 BIOS、游戏镜像或取得任何商业游戏资产，也没有标题级本机实测。下文的`A/B/C`只表示“研究优先级与平台路径证据”，不是某标题在Mac上的兼容等级，更不是本机实测帧率或通关证明。

## 1. 这台机器的研究能力

| 项目 | 当前值 | 对调研的含义 |
| --- | --- | --- |
| 机型 | MacBook Pro `Mac14,6` | Apple Silicon平台 |
| SoC | Apple M2 Max，12核CPU | 足以覆盖本轮列出的低世代模拟器；PS3仍看游戏 |
| 内存 | 96GB | 不是GBA—PS2研究的瓶颈 |
| 系统 | macOS 15.7.5 | 需要警惕旧Intel Mac游戏和旧OpenGL程序 |
| 架构 | arm64 | 优先原生／Universal模拟器；Intel应用经Rosetta 2 |
| Rosetta 2 | 已存在并运行 | 可烟测Intel 64位Mac游戏与当前PCSX2路径 |
| 已安装研究工具 | 只保留PCSX2官方Nightly `2.7.524`；稳定版`2.6.3`故障定位后已卸载；未安装表内其他模拟器、CrossOver或Whisky | Nightly环境已启动；所有PS2标题仍是`L0`，没有游戏`L1`实测 |

本机性能不是第一风险。第一风险依次是：

1. 游戏是否有可用的自有介质／设备转储，并符合适用法律与许可；
2. 模拟器是否支持该平台和具体Game ID；
3. macOS 15、Apple Silicon与渲染器组合；
4. 旧游戏本身的语言、UI和输入；
5. 观察过程是否固定版本和设置，能否复现。

## 2. 模拟器选择

### 2.1 推荐矩阵

| 原平台 | 首选 | Apple Silicon／macOS依据 | BIOS／固件 | 研究建议 | 路径优先级 |
| --- | --- | --- | --- | --- | --- |
| GBA | **mGBA 独立版** | 官方现代macOS包为Universal，支持macOS 10.13+ | 普通GBA研究不要求外部BIOS | 第一批；键盘／手柄、快进、倒带、录像都方便 | A |
| PS1 | **DuckStation** | 官方提供macOS 13.3+ Universal，含ARM64；Metal/Vulkan/OpenGL | 需要从自己主机提取BIOS | 第一批；每游戏配置、记忆卡和录像适合可复现实验 | A |
| PS2 | **PCSX2 Nightly 2.7.524** | 官方支持macOS 11+，推荐macOS 14—15；当前M系列仍经Rosetta；本机稳定版2.6.3曾有内存映射故障，现已卸载 | 需要从自己PS2提取BIOS | 环境已安装并启动；重点标题仍无本机结果 | B+环境／标题待测 |
| PSP | **PPSSPP** | 官方提供macOS DMG；所引页面没有证明二进制是arm64、Universal还是Intel | 不需要PSP BIOS | 第二／三批；先检查包架构，再在M2 Max上确认原生或Rosetta运行 | A- |
| NDS | **melonDS** | 官方有Universal与arm64构建 | BIOS／固件需求按所测模式与官方说明另核；本轮来源不足以支持“开源替代BIOS”结论 | 双屏布局要固定；适合研究便携UI压缩 | A- |
| PS3 | **RPCS3** | 官方提供Apple Silicon构建 | Sony官方固件；游戏仍须自己转储 | 只作逐Game ID实验，不进入研发基线 | C—B |
| 多平台 | RetroArch | 官方Universal；Metal驱动仍有实验性说明 | 随core | 适合统一陈列，不适合首轮严谨基线 | B |
| 多平台 | OpenEmu 2.4.1 | 官方Intel-only，Apple Silicon靠Rosetta | 随core | 界面友好，但core版本与独立版不一定同步 | B- |

### 2.2 为什么优先独立模拟器

调研不是只要“能启动”。我们需要知道结果来自哪个模拟器版本、哪个渲染器和哪组设置。独立版的变量更少：

- GBA：mGBA；
- PS1：DuckStation；
- PS2：PCSX2；
- PSP：PPSSPP；
- NDS：melonDS。

RetroArch／OpenEmu更适合浏览统一游戏库，但会额外引入前端版本、core版本、视频驱动和存档路径差异，不利于把“原作交互问题”和“模拟器配置问题”分开。

### 2.3 官方来源

- mGBA：[Universal macOS说明](https://mgba.io/2022/10/11/mgba-0.10.0/)、[官方仓库](https://github.com/mgba-emu/mgba)
- DuckStation：[官方仓库与macOS要求](https://github.com/stenzek/duckstation)
- PCSX2：[系统要求](https://pcsx2.net/docs/setup/requirements/)、[BIOS说明](https://pcsx2.net/docs/setup/bios/)、[自有光盘转储](https://pcsx2.net/docs/setup/discs/)
- PPSSPP：[macOS说明](https://www.ppsspp.org/docs/reference/mac/)、[自有UMD转储](https://www.ppsspp.org/docs/getting-started/dumping-games/)
- melonDS：[官方下载](https://melonds.kuribo64.net/downloads.php)
- RPCS3：[官方下载](https://rpcs3.net/download.html)、[兼容性维护说明](https://github.com/RPCS3/rpcs3/wiki/Game-Compatibility)
- RetroArch：[macOS安装与架构](https://docs.libretro.com/guides/install-macos/)
- OpenEmu：[2.4.1发布说明](https://openemu.org/rnotes/2.4.1.html)

### 2.4 本机已安装的PCSX2环境

| 项目 | 当前值 | 证据边界 |
| --- | --- | --- |
| 使用版本 | 官方Nightly `2.7.524` | 固定研究批次，不自动升级 |
| 应用路径 | `/Applications/PCSX2-v2.7.524.app` | 官方签名与Apple公证通过 |
| 启动方式 | `/Users/rayz/Games/PS2/Launch PCSX2 Research.command` | 固定`-datapath`，避免误用稳定版配置 |
| 数据目录 | `/Users/rayz/Games/PS2/PCSX2Data/v2.7.524/PCSX2/` | 配置、记忆卡、即时存档、日志与项目仓库隔离 |
| BIOS目录 | `/Users/rayz/Games/PS2/BIOS/` | 当前为空；只接受自己PS2导出 |
| 镜像目录 | `/Users/rayz/Games/PS2/DiscImages/` | 当前为空；只接受自己光盘转储 |
| 图形基线 | 自动API、原生1x、窗口、无宽屏／反隔行补丁 | 先测准确基线，再逐游戏提高 |
| 已完成验证 | 中文主界面、设置保存、正常退出、按固定数据目录重启 | 不证明BIOS启动、游戏画面、声音、输入或存档 |

稳定版`2.6.3`日志曾出现`mach_vm_map()`和`Failed to allocate VM memory`，完成故障取证后已于`2026-08-28`卸载。官方 [PR #11734](https://github.com/PCSX2/pcsx2/pull/11734)于2026-03-28合入，Nightly `2.7.524`已包含该修复。本机完整操作见[08｜PCSX2 Mac安装与操作指南](08-pcsx2-mac-install-and-operation-guide.md)。

## 3. 最值得在本机烟测的老游戏

| 优先 | 游戏 | 原平台／语言 | 首选路径 | 烟测优先级 | 只为本项目回答什么 | 主要风险 |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | **Front Mission 3** | PS1；有官方英文版 | DuckStation | A- | 部位、AP、弹射／夺机、双路线、网络界面；“身体先于血条” | 配装与命中数字多；BIOS与自有光盘转储 |
| 2 | **超级机器人大战OG2** | GBA；有官方英文版 | mGBA | A | 角色／机体存在感、支援、出击、招牌演出和快速正反馈 | 战术底盘薄、命中率与数值碾压不可照搬 |
| 3 | **Z.O.E. The Fist of Mars** | GBA；英文版 | mGBA | A | 战棋命令与攻击／回避互动段怎样交替 | 互动段可能从新鲜变重复 |
| 4 | **Ring of Red** | PS2；英文版 | PCSX2 | B+ | 大地图命令→短实时接触→巨大步行机与步兵协同 | Wiki只有Windows端`Playable`记录、Mac栏为未知；本机标题L0；接触段可能拖 |
| 5 | **Robot Alchemic Drive** | PS2；英文版 | PCSX2 | B | 城市尺度、人／机双视角、巨机动作和破坏反馈 | Wiki只有Windows端`Playable`记录、Mac栏为未知；本机标题L0；非战棋 |
| 6 | **Front Mission 4** | PS2；官方英文版 | PCSX2 | B+ | Link System、双主角战线、基地—整备—战斗循环 | Wiki只有Windows端`Playable`记录、Mac栏为未知；升频文字线／阴影待烟测 |
| 7 | **Front Mission 5** | PS2；官方日文 | PCSX2 | B | 部位战、链接、基地人物和长战争组织 | Wiki只有Windows端`Playable`记录、Mac栏为未知；语言与本机标题L0 |
| 8 | **超级机器人大战OG Original Generations** | PS2；官方日文 | PCSX2 | B- | Twin、角色组合、名机名招名台词和系列回收 | 缺少可靠Mac标题测试；语言／补丁边界 |
| 9 | **超级机器人大战A Portable** | PSP；官方日文 | PPSSPP | B+ | 便携端怎样压缩人物、支援、技能和演出输入 | 难度尖锐；传统数值战棋 |
| 10 | **Valkyria Chronicles 3** | PSP；官方日文 | PPSSPP | B | 指挥点、出席、具身移动与迎击火力 | 不是机甲主导；标题级Mac兼容需烟测 |
| 11 | **超级机器人大战W** | NDS；日文 | melonDS | A- | 双屏信息分工与便携菜单压缩 | 与核心机制相似度低于OG2 |
| 12 | **Steambot Chronicles** | PS2；英文版 | PCSX2 | C+ | 机器人用于生活、劳动、城镇关系与自定义 | Wiki为Windows端`Ingame`、Mac栏未知；优先视频，不占首批烟测 |
| 13 | **第2次超级机器人大战OG** | PS3；日文；`BLJS10133` | RPCS3 | C | 高规格角色合体与长线回收 | RPCS3为`Ingame`而非Playable；仍有同引擎渲染问题，不作研发依赖 |
| 14 | **机战OG 月之民** | PS3；日文；`BLJS10335` | RPCS3 | C | 现代OG编队与演出 | RPCS3为`Ingame`而非Playable；优先视频 |

标题兼容参考：

- [Front Mission 4 — PCSX2 Wiki](https://wiki.pcsx2.net/Front_Mission_4)
- [Front Mission 5 — PCSX2 Wiki](https://wiki.pcsx2.net/SLPM-66421)
- [Ring of Red — PCSX2 Wiki](https://wiki.pcsx2.net/index.php?title=Ring_of_Red)
- [Robot Alchemic Drive — PCSX2 Wiki](https://wiki.pcsx2.net/index.php?title=Robot_Alchemic_Drive)
- [Steambot Chronicles — PCSX2 Wiki](https://wiki.pcsx2.net/Steambot_Chronicles)
- [RPCS3兼容数据库](https://rpcs3.net/compatibility)
- [RPCS3 UYVY竖纹问题 #18132](https://github.com/RPCS3/rpcs3/issues/18132)
- [机战OGs官方系统说明](https://www.suparobo.jp/srw_lineup/srw_ogps/gamedata/outline.html)
- [Front Mission 3官方页面](https://www.jp.square-enix.com/game/detail/fm3/)

上列PS2 Wiki的`Playable`／`Ingame`是Windows端记录，Mac栏为未知。它只能说明PCSX2项目存在标题级历史记录，不能证明macOS兼容；这台M2 Max现在已经有可启动的PCSX2环境，但所有标题仍是`L0未实测`。表中的`B+／B`只是烟测优先级。

### 3.1 跨视频网站补强了什么

Wiki不是现在唯一的技术依据。跨站录像已经证明七款各自至少在某个 PCSX2 构建进入实际玩法，但仍没有一款形成“同一视频确认 Apple Silicon Mac＋具体标题＋PCSX2版本”的闭环。

| 游戏 | 视频中的最强技术证据 | 仍缺什么 |
| --- | --- | --- |
| Front Mission 4 | [Windows 10 / PCSX2 1.7.0，多任务实机](https://www.youtube.com/watch?v=vCuWX1CZF_8) | Mac标题实测、存档、升频阴影和长任务 |
| Front Mission 5 | [Windows PCSX2，使用多项图形修正](https://www.youtube.com/watch?v=ezkOFe41tGQ) | 当前构建、Mac、未修改日版与补丁变量拆分 |
| Ring of Red | [Windows / PCSX2 1.7.0-1189，进入接触战](https://www.youtube.com/watch?v=MQwqCJouttw) | Mac、长接触战、存档与渲染稳定性 |
| Sakura Wars V | [PCSX2 1.7.5709 / Vulkan / 约100%叠层](https://www.youtube.com/watch?v=cxtPrG6E4Mc) | 宿主OS未写；Mac、长ADV与战斗切换、存档 |
| Robot Alchemic Drive | [Windows 10 / PCSX2 1.5开发版 / 4K](https://www.youtube.com/watch?v=5qUN2SnhY2I) | 证据较旧；Mac、输入与视角、高负载城市战 |
| 机战OGs | [PCSX2 2.7.281＋英文民间补丁](https://www.youtube.com/watch?v=HiMdw0Mxc2g) | OS未写；Mac、原版与补丁变量、长演出 |
| Steambot Chronicles | [Windows 7 / PCSX2 1.2.1](https://www.youtube.com/watch?v=2lMGk30ouC4) | 证据严重陈旧；当前Mac全链路 |

另有通用 [M1 MacBook Air / PCSX2 2.0 实际设置与运行录像](https://www.youtube.com/watch?v=Az8Fdt8PBx4)，能证明 Apple Silicon 路径存在，不能外推七款标题。更完整的玩法与视频证据见[07｜七款PS2参考作跨视频网站实机审计](07-ps2-cross-video-platform-audit.md)。

## 4. 现代参考游戏怎样在这台 Mac 访问

| 游戏 | 官方路径 | Apple Silicon判断 | 推荐做法 | 状态 |
| --- | --- | --- | --- | --- |
| **Door Kickers 2** | Windows、macOS | Steam要求明确列M1最低、M2推荐；这证明官方支持Apple Silicon Mac，不单独证明arm64原生二进制 | 直接使用正式Steam macOS版 | **A，最值得直接本机研究** |
| **Into the Breach** | Windows、macOS、Linux | 官方Intel时代Mac版；Apple Silicon原生性未证 | 作为Rosetta候选烟测；游戏很轻，但不能写arm64原生 | A- |
| **Wildermyth** | Windows、macOS、Linux | 官方明确“无原生M1支持，Rosetta性能可能不佳” | Rosetta 2烟测，保守记录 | B |
| **Inscryption** | Windows、macOS、Linux | 官方Intel时代Mac版；Apple Silicon原生性未证 | 作为Rosetta候选烟测 | B+ |
| **Invisible, Inc.** | Windows、macOS、Linux | 官方Intel时代Mac版；已有Catalina兼容更新，Apple Silicon原生性未证 | 作为Rosetta候选烟测 | B+ |
| **BATTLETECH** | Windows、macOS、Linux | 官方Intel时代Mac版，无官方M系列保证 | 先试官方Intel版macOS包经Rosetta，不先上兼容层 | B- |
| **Pyre** | Windows、macOS、Linux、PS4 | 官方有Mac包；当前引用不足以证明其二进制架构 | 检查包架构后作原生／Rosetta烟测；更适合手柄 | B |
| **Phantom Brigade 2.0** | Windows PC | 无官方Mac构建 | 首选B站／官方视频；兼容层应另开已购Windows版实验 | 视频优先 |
| **Tactical Breach Wizards** | Windows PC | 无官方Mac构建 | 首选B站／官方长流程；兼容层另案 | 视频优先 |
| **13 Sentinels** | PS4、Switch | 无官方PC／macOS版 | B站流程或自有主机实机 | 视频／主机 |

官方页面：

- [Door Kickers 2](https://store.steampowered.com/app/1239080/Door_Kickers_2_Task_Force_North/)
- [Into the Breach](https://store.steampowered.com/app/590380/Into_the_Breach/)
- [Wildermyth](https://store.steampowered.com/app/763890/Wildermyth/)
- [Inscryption](https://store.steampowered.com/app/1092790/Inscryption/)
- [Invisible, Inc.](https://store.steampowered.com/app/243970/Invisible_Inc/)
- [BATTLETECH](https://store.steampowered.com/app/637090/BATTLETECH/)
- [Pyre](https://store.steampowered.com/app/462770/Pyre/)
- [Phantom Brigade](https://store.steampowered.com/app/553540/Phantom_Brigade/)
- [Tactical Breach Wizards](https://store.steampowered.com/app/1043810/Tactical_Breach_Wizards/)
- [13 Sentinels — Nintendo](https://www.nintendo.com/en-ca/store/products/13-sentinels-aegis-rim-switch/)

### 4.1 其余入选样本的访问结论

下表补齐[01窄样本矩阵](01-similarity-and-priority.md)中未在上表逐项出现的主要参考。`Windows Steam`不等于可在Mac直接运行；兼容层一律另案，不进入当前基线。

| 样本 | 正式平台／本机路径 | 当前建议 | 本机证据 |
| --- | --- | --- | --- |
| `Outer Wilds` | 正式PC版以Windows为主，另有主机版；无官方macOS路径 | B站／官方视频或自有主机；兼容层另案 | `L0` |
| `Marvel's Midnight Suns` | 正式PC版以Windows为主，另有主机版；无官方macOS路径 | 视频优先；已购Windows版兼容层另案 | `L0` |
| `Super Robot Wars 30` | Windows Steam、Switch、PS4；无官方macOS路径 | 视频／自有主机；Windows兼容层另案 | `L0` |
| `Super Robot Wars Y` | Windows Steam、Switch、PS5；无官方macOS路径 | 视频／自有主机；Windows兼容层另案 | `L0` |
| `Sakura Wars V` | PS2／Wii旧作 | PS2版可列PCSX2标题烟测候选，但Mac标题级兼容未证；当前视频优先 | `L0` |
| `Front Mission 3` | PS1旧作 | DuckStation＋自有主机／介质转储；首批烟测 | `L0` |
| `Ring of Red`、`Robot Alchemic Drive` | PS2旧作 | PCSX2平台路径；Windows兼容记录不能代替Mac烟测 | `L0` |
| `SRW OG2`、`Z.O.E. The Fist of Mars` | GBA旧作 | mGBA＋自有介质转储；首批烟测 | `L0` |

平台来源补充：[Super Robot Wars 30 — Steam](https://store.steampowered.com/app/898750/30/)、[Super Robot Wars Y — 官方站](https://www.bandainamcoent.com/games/super-robot-wars-y)。`Outer Wilds`与`Midnight Suns`在正式本机复核前仍按“无已证官方Mac路径”处理，不把社区兼容层报告升格为官方支持。

几个必须写准的边界：

- “Steam有Mac版”不等于Apple Silicon原生；此表只有`Door Kickers 2`有足够官方系统要求证据判为Apple Silicon正式支持路径，但仍不单独证明arm64二进制。
- `Wildermyth`要比普通Rosetta候选更保守，因为商店页直接警告M1／Rosetta性能。
- `Phantom Brigade`与`Tactical Breach Wizards`是“无官方Mac构建”，不是断言任何兼容层绝不可能启动。
- `13 Sentinels`没有正式PC版；主机模拟不作为本轮正规研发路径。
- `Phantom Brigade`当前已是2.0，2023旧版录像不能替代当前版本操作复核。

## 5. 建议的烟测顺序

PCSX2环境安装已经得到用户授权并完成。现代原生游戏只使用官方购买版本；PCSX2标题仍只在用户提供自己PS2导出的BIOS和自己光盘制作的镜像后执行。购买记录本身不提供网络ISO授权，所有实测仍需符合适用法律与许可。

### 第0批：不用模拟器

1. `Door Kickers 2`正式Mac版：验证画线、朝向、Go Code、暂停、执行和鼠标负担；
2. `Into the Breach`正式Mac版：验证意图、推拉、攻击顺序、撤销和完整四轮节奏。

### 第1批：环境风险最低

1. `超级机器人大战OG2` / mGBA；
2. `Z.O.E. The Fist of Mars` / mGBA；
3. `Front Mission 3` / DuckStation。

### 第2批：PS2标题技术烟测

1. `Front Mission 4`：现有录像的版本、宿主与多任务覆盖最清楚；
2. `Ring of Red`：可较快进入本项目最关心的接触战；
3. `Sakura Wars V`：已有较新的 Vulkan／百分比叠层证据，但 Mac 未证；
4. `机战OGs`：有2026年 PCSX2 新构建录像；首次先测未修改自有介质，翻译补丁另列；
5. `Robot Alchemic Drive`：设计价值高，技术录像较旧；
6. `Front Mission 5`：旧录像使用多项图形修正，另有语言／补丁变量；
7. `Steambot Chronicles`：现有 PCSX2 技术录像最旧，放最后。

这只是按技术证据强弱排序。如果按玩法研究价值，仍优先 `Ring of Red → Robot Alchemic Drive → Front Mission 4`。不要把“最值得研究”和“最容易在Mac验证”混成同一个榜。

### 第3批：其他角色、系列与长期层

1. `机战A Portable`；
2. `Valkyria Chronicles 3`；
3. 根据前两批的缺口再决定是否增加其他标题，不以“全装一遍”为目标。

### 第4批：只作技术实验

- RPCS3上的`第2次OG`和`月之民`；
- 其他只有陈旧兼容层证据、且确有新增研究价值的标题。

## 6. 每次本机实测必须记录什么

```text
test_id
date
machine_model / macOS / architecture / Rosetta
emulator_name / exact_version / update_channel
game_title / region / Game ID
legitimate_source_type
BIOS_region / BIOS_hash（不提交BIOS）
renderer / internal_resolution / widescreen_or_patch
input_device / mapping
save_type / save_location
mission / turn / observation_start_end
what_player_sees
exact_input_sequence
preview_before_commit
undo_boundary
execution_and_feedback
performance_or_rendering_issue
design_learning
do_not_copy
evidence_file_or_note
```

操作记录统一写成：

```text
玩家看见什么
→ 按什么
→ 系统怎样预告
→ 提交前能否撤销
→ 怎样执行
→ 结果怎样反馈
→ 状态进入哪一屏
```

正式基线先用原生分辨率和默认设置。画质增强另列，不能把升频阴影、文字错位或滤镜问题误判为原作交互。

即时存档可能跨模拟器版本失效；研究进度同时保留游戏原生存档。一个观察批次中途不升级模拟器。

## 7. 介质、适用法律与仓库边界

- 不下载网络ROM、ISO、CHD、BIOS、预补丁镜像或“整合包”。
- 项目只接受自有设备／介质的自行转储，不使用网络镜像；具体合法性仍取决于适用法律、技术保护措施和许可条款。
- PS1／PS2 BIOS从自己拥有的主机提取；PCSX2官方也要求用户提供自有BIOS。
- PSP游戏按PPSSPP官方流程从自己的PSP与UMD转储。
- PS3系统固件可以从Sony官方取得，游戏数据仍来自自己的主机／光盘。
- 汉化只考虑“差分补丁＋自有转储”；不使用已经含游戏数据的镜像。
- “绝版”“弃置软件”或“研究用途”不会自动消除版权。
- 模拟器、BIOS和游戏资产不随本项目或Demo分发。
- 仓库只保存研究文字、经授权且符合适用条款的必要自录证据与配置说明；不保存整段竞品录像或原始游戏资产。

## 8. 当前结论

纸面与视频证据下，预计风险最低的模拟研究范围是**GBA、PS1、PSP、NDS**；**PS2的PCSX2环境已经在本机启动，但七款目标游戏仍没有这台Mac的标题级`L1`结果**；**PS3只作额外实验**。第一批最值得争取亲手证据的五款仍是：`Front Mission 3`、`Ring of Red`、`超级机器人大战OG2`、`Z.O.E. The Fist of Mars`、`Robot Alchemic Drive`。其中两款PS2游戏排在前列是因为研究价值高，不是因为已证明Mac兼容。
