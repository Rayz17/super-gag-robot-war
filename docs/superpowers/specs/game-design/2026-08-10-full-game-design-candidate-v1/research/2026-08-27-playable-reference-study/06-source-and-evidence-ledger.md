# 06｜来源与证据账

> Checked: `2026-08-28`
>
> Purpose: 让后续研究者知道每个结论来自项目规则、官方页面、B站录像、模拟器数据库还是推论。动态页面可能变化；复用前先看`checked`和`limitation`。

## 1. 项目内权威来源

| ID | 来源 | 本报告用它确定什么 | 边界 |
| --- | --- | --- | --- |
| `P-CORE-00C` | [核心玩法总案v0.4](../../00c-core-game-design-master-review.md) | 当前产品定义、短全队共同轮、身体、意图、预备、目标、四战斗家族、名场面、人物牌、探索、返馆、Meta与LLM | Candidate；没有Canon／Build权威 |
| `P-FABLE-16` | [玩法母型库关闭稿](../../external-reviews/fable5/16-v3.4-gameplay-template-library-closure.md) | 创意母型如何批量出题与其适用边界 | 案例人物／台词／关卡不是项目事实 |
| `P-FABLE-17` | [采纳与规则冲突关闭稿](../../external-reviews/fable5/17-v3.4-adoption-and-rule-conflict-closure.md) | 公共轮、提交、气势、百机导演、人物能力来源、战报和信息量上限 | 只用于解释00c整合来源，不另立一套总案 |
| `P-OLD-RESEARCH` | [旧版全玩法比较研究](../01-comparative-gameplay-research.md) | 35条官方来源宽样本与早期综合轴 | 旧规则中时间窗、临时改令、C2审批、探索分类等已被00c纠正 |

本报告没有修改上述文件。

## 2. B站实际视频流证据

| ID | 来源 | 核验点 | 支持主张 | 限制 |
| --- | --- | --- | --- | --- |
| `BV-ITB-01` | [《陷阵之志》不公模式·极点守卫](https://www.bilibili.com/video/BV11N411878E/) | 04:50、05:00、05:05、05:20、05:35 | 场上意图、移动／攻击、编号顺序、结束回合、执行 | v1.2.88；只抽查一段，不证明完整战役 |
| `BV-PB-EA-01` | [《幻影旅团》4维度战术RPG](https://www.bilibili.com/video/BV1CR4y1p7Yq/) | 03:00、05:00、07:00、09:00 | 2021旧版五秒时间线、轨迹、动作放置、共同执行 | 抢先体验历史版，不能代表2.0驾驶员／战役层 |
| `BV-PB-20-01` | [《幻影旅团》中配初体验](https://www.bilibili.com/video/BV1humoB8EB2/) | 01:30、03:00、05:00、07:30、10:00 | 约2.0期仍有时间线；分层伤害、世界事件、执行与Replay | 画面未直接显示Build号；只能写“约2.0时期” |
| `BV-TBW-01` | [谜之声《战术破门巫师队》正式版第一幕](https://www.bilibili.com/video/BV1zy411H7iP/) | 12:00—12:55、13:00 | 少动词、悬停、预演、结束、Rewind、可选挑战 | 小房间手工关；不能证明大地图产能 |
| `BV-FM5-01` | [《前线任务5》通关视频 Part 1](https://www.bilibili.com/video/BV1354y1e7C2/?p=2) | 10:00、15:00、20:00、25:00—25:40 | 战斗—人物—世界交替，AP／武器／命中与部位反馈 | PS2片段；传统菜单与语言版本需另证 |
| `BV-SRWOG-01` | [《机战OGS/OG2》第22话](https://www.bilibili.com/video/BV1si421f7eR/) | 05:00、09:50—10:20、20:00、40:00、60:00、80:00 | Twin、确认页、精神、武器、技能与演出 | 单话流程；不证明整个系列所有版本 |
| `BV-BT-01` | [《BattleTech》战役 P1](https://www.bilibili.com/video/BV1ds411V7ci/?p=2) | 30:00、39:50—40:30 | 身体轮廓、武器、射线、命中、结构／驾驶员后果、Reserve | 2018正式版时期；不证明当前Mac表现 |
| `BV-BT-02` | [《BattleTech》汉化界面／经营](https://www.bilibili.com/video/BV1RF41187Xh/) | 01:30、02:30、04:00 | 飞船、驾驶员、技能、商店、吨位与库存 | 2021汉化录像；只用于菜单结构观察 |

详细操作解释见[02｜B站实机观察账](02-bilibili-gameplay-observation.md)。

## 3. B站已发现但未逐段核验

这些链接只能标`V0-discovered`，不能写成“录像证明了具体操作”。

| 研究问题 | 来源 | 后续应定位什么 |
| --- | --- | --- |
| 13人剧情／档案／战斗互解锁 | [《十三机兵防卫圈》最高难度白金全流程](https://www.bilibili.com/video/BV13E411N7cJ/) | 一次追忆、探明和崩坏之间的实际切换与解锁 |
| 《十三机兵》战斗UI | [崩坏篇基础解说](https://www.bilibili.com/video/BV1PJ411B7EK/) | 选机兵、武器范围、冷却、战后档案更新 |
| Meta完整上下文 | [《邪恶冥刻》全攻略合集](https://www.bilibili.com/video/BV1vS4y1f798/) | 离桌探索如何改牌局；版本切换前因后果；避免只看惊吓 |
| 《陷阵之志》完整任务 | [秘密战队正常模式通关](https://www.bilibili.com/video/BV1Ee4y127qn/) | 四轮目标取舍、任务结算和下一岛 |
| 《陷阵之志》深度教程 | [65P通略](https://www.bilibili.com/video/BV1oq421w7Hp/) | 不同队伍怎样换题；高难是否压缩长期判断 |
| 《机战OG2》长线 | [PS2 61P全流程](https://www.bilibili.com/video/BV19D4y1C7Ju/) | 加入、编组、名场面、战后回收 |

《樱花大战V》不再停留在本节的`V0`状态；它与另外六款PS2目标作的跨站时间点证据统一记在下一节及[07](07-ps2-cross-video-platform-audit.md)。

### 3.1 七款PS2目标作的跨站证据组

下表每一行都是一组互补证据，不表示每个链接都达到同一等级。具体时间点、观察和边界以[07｜七款PS2参考作跨视频网站实机审计](07-ps2-cross-video-platform-audit.md)为准。

| ID | 游戏 | YouTube | Niconico | B站 | 技术边界 |
| --- | --- | --- | --- | --- | --- |
| `XV-FM4` | Front Mission 4 | [6小时长流程](https://www.youtube.com/watch?v=WEq5svRbG9c)、[Windows PCSX2](https://www.youtube.com/watch?v=vCuWX1CZF_8) | [MISSION 1—4](https://www.nicovideo.jp/watch/sm45588713) | [34P流程](https://www.bilibili.com/video/BV1kKdYYVEVE) | 玩法到`V1/V3`；模拟器仅`M-B`，Mac未证 |
| `XV-FM5` | Front Mission 5 | [6.5小时长流程](https://www.youtube.com/watch?v=EJYms9QTK_g)、[Windows PCSX2](https://www.youtube.com/watch?v=ezkOFe41tGQ) | [mission01](https://www.nicovideo.jp/watch/sm40532316) | [流程P2](https://www.bilibili.com/video/BV1354y1e7C2/?p=2)、[生存系统](https://www.bilibili.com/video/BV1fU4y1C7av) | 友伤／奖励冲突部分来自作者说明；Mac未证 |
| `XV-ROR` | Ring of Red | [36小时长流程](https://www.youtube.com/watch?v=nmGm5vxBh_g)、[机制短片](https://www.youtube.com/watch?v=mVBvRUoa_eU) | [训练场1](https://www.nicovideo.jp/watch/sm2135397) | [长实况](https://www.bilibili.com/video/BV1GM6qYeErD)、[系统概览](https://www.bilibili.com/video/BV123Vp63EbQ) | 战略—接触循环到`V1-flow`；Windows PCSX2，Mac未证 |
| `XV-SWV` | Sakura Wars V | [长流程1/2](https://www.youtube.com/watch?v=LgabDDlM8Iw)、[长流程2/2](https://www.youtube.com/watch?v=GWNlyy0pQ9g) | [第一章1-1](https://www.nicovideo.jp/watch/sm36644710) | [中文字幕第一章](https://www.bilibili.com/video/BV1z4411v76K)、[战斗—战后段](https://www.bilibili.com/video/BV1z4411s75q) | 关系层到`V1`；抽帧不单独判完整战斗时制；Mac未证 |
| `XV-RAD` | Robot Alchemic Drive | [长流程](https://www.youtube.com/watch?v=Rkx2qr5z1f0)、[旧评测](https://www.youtube.com/watch?v=5HXsIK5noBU) | [Part 1](https://www.nicovideo.jp/watch/sm44167739) | [连续操作教学](https://www.bilibili.com/video/BV1Ly4y157XN)、[实体试玩](https://www.bilibili.com/video/BV1C2DpYqEXR) | 人／机尺度和肢体输入到`V1`；Windows PCSX2旧证据，Mac未证 |
| `XV-OGS` | 机战OGs | [Scenario 1—8](https://www.youtube.com/watch?v=ULWlkXtMC4A)、[系统实机](https://www.youtube.com/watch?v=C32JdDW_T74) | [挑战Part 1](https://www.nicovideo.jp/watch/sm8792359) | [第22话](https://www.bilibili.com/video/BV1si421f7eR)、[编组推荐](https://www.bilibili.com/video/BV1zk4y1571J) | 含民间翻译／中文版本变量；PCSX2 2.7.281录像仍未写OS |
| `XV-SC` | Steambot Chronicles | [长流程](https://www.youtube.com/watch?v=UveFtzHfPv4)、[深度回顾](https://www.youtube.com/watch?v=a8fMBp0JfAA) | [新系列#1](https://www.nicovideo.jp/watch/sm45393883) | [长流程](https://www.bilibili.com/video/BV1p8w8eQEcv)、[中文系统介绍](https://www.bilibili.com/video/BV1ed4y1k7gC) | 生活／维修／驾驶到`V1/V2/V3`；PCSX2技术录像最旧，Mac未证 |
| `XV-MAC-PCSX2` | 通用Mac路径 | [M1 MacBook Air / PCSX2 2.0](https://www.youtube.com/watch?v=Az8Fdt8PBx4) | 本轮无目标标题Mac闭环 | [2021 M1教程转载](https://www.bilibili.com/video/BV1AL4y1M7ia/) | 转载不重复计证；通用`M-A`不能外推七款标题 |

## 4. 模拟器官方来源

| ID | 来源 | 支持主张 | 不支持什么 |
| --- | --- | --- | --- |
| `E-MGBA-01` | [mGBA 0.10 macOS说明](https://mgba.io/2022/10/11/mgba-0.10.0/) | 现代macOS Universal Binary与最低系统 | 某款游戏已在本机跑通 |
| `E-MGBA-02` | [mGBA官方仓库](https://github.com/mgba-emu/mgba) | 平台、功能与当前项目状态 | 游戏版权或ROM来源 |
| `E-DUCK-01` | [DuckStation官方仓库](https://github.com/stenzek/duckstation) | macOS 13.3+ Universal、ARM64和渲染后端 | Front Mission 3本机完整通关 |
| `E-PCSX2-REQ` | [PCSX2系统要求](https://pcsx2.net/docs/setup/requirements/) | macOS版本、M系列与性能档 | 每个PS2标题无问题 |
| `E-PCSX2-BIOS` | [PCSX2 BIOS说明](https://pcsx2.net/docs/setup/bios/) | 需要用户提供自有PS2 BIOS | 任何网络BIOS的授权或合法性 |
| `E-PCSX2-DISC` | [PCSX2光盘转储](https://pcsx2.net/docs/setup/discs/) | 自有介质备份流程存在 | 他人镜像来源 |
| `E-PCSX2-NIGHTLY` | [PCSX2 v2.7.524官方发布](https://github.com/PCSX2/pcsx2/releases/tag/v2.7.524) | 本机安装包的官方版本、提交与发布日期 | 单个游戏必然兼容 |
| `E-PCSX2-MEMMAP` | [PCSX2 PR #11734](https://github.com/PCSX2/pcsx2/pull/11734) | 允许主内存映射到其他位置，针对无法找到可用映射位置的启动失败 | 不能替代本机安装和标题实测 |
| `E-PCSX2-CLI` | [PCSX2命令行参数](https://pcsx2.net/docs/advanced/cli/) | `-datapath`、`-batch`、`-logfile`、`--`的正式语义 | Agent自动操作质量或游戏授权 |
| `E-PPSSPP-MAC` | [PPSSPP macOS说明](https://www.ppsspp.org/docs/reference/mac/) | 正式macOS DMG路径 | 所引页面不证明包为arm64／Universal／Intel，也不证明每个标题兼容 |
| `E-PPSSPP-DUMP` | [PPSSPP自有UMD转储](https://www.ppsspp.org/docs/getting-started/dumping-games/) | 自有PSP／UMD转储流程存在 | 预制ROM／ISO；也不对所有司法辖区作法律保证 |
| `E-MELONDS-01` | [melonDS官方下载](https://melonds.kuribo64.net/downloads.php) | macOS Universal／arm64构建 | BIOS替代主张、双屏布局价值或标题兼容 |
| `E-RPCS3-DL` | [RPCS3官方下载](https://rpcs3.net/download.html) | Apple Silicon构建存在 | PS3游戏均可玩 |
| `E-RPCS3-COMPAT` | [RPCS3兼容数据库](https://rpcs3.net/compatibility) | 必须逐Game ID查状态 | 社区视频等于官方Playable |
| `E-RETRO-01` | [RetroArch macOS说明](https://docs.libretro.com/guides/install-macos/) | Universal包与驱动说明 | 适合作为最可复现实验基线 |
| `E-OPENEMU-01` | [OpenEmu 2.4.1](https://openemu.org/rnotes/2.4.1.html) | Intel-only／Rosetta与系统要求 | core版本等于独立模拟器最新版本 |

### 4.1 本机PCSX2环境证据

| ID | 本机观察 | 当前可写成 | 不能写成 |
| --- | --- | --- | --- |
| `LOCAL-PCSX2-263` | 稳定版曾位于`/Applications/PCSX2.app`，官方签名／公证通过；日志出现`mach_vm_map()`、`Failed to map data memory`、`Failed to allocate VM memory`；`2026-08-28`已卸载 | 稳定版曾安装并完成故障定位，但不适合作为这台Mac的研究基线 | 当前仍已安装；电脑内存不足；任何标题不兼容 |
| `LOCAL-PCSX2-27524` | `/Applications/PCSX2-v2.7.524.app`，签名／公证通过；中文向导、主界面、配置保存、退出后重启通过；同类内存错误未再出现 | Nightly研究环境已启动并可复现 | BIOS已启动；游戏画面、声音、输入、存档或兼容已通过 |
| `LOCAL-PCSX2-DATA` | 固定`-datapath /Users/rayz/Games/PS2/PCSX2Data/v2.7.524`；BIOS与镜像目录独立于仓库 | 后续测试能锁定版本与数据目录 | 目录为空时也算标题实测 |

详细路径和操作见[08｜PCSX2 Mac安装与操作指南](08-pcsx2-mac-install-and-operation-guide.md)。

## 5. 具体老游戏兼容来源

| 游戏 | 来源 | 当前只可写成 |
| --- | --- | --- |
| Front Mission 3 | [Square Enix官方页面](https://www.jp.square-enix.com/game/detail/fm3/)＋DuckStation平台支持 | `PS1模拟路径A-，本机未实测` |
| Front Mission 4 | [PCSX2 Wiki](https://wiki.pcsx2.net/Front_Mission_4) | `Windows端Playable；Mac栏未知；M2 Max标题L0` |
| Front Mission 5 | [PCSX2 Wiki](https://wiki.pcsx2.net/SLPM-66421) | `Windows端Playable；Mac栏未知；版本／渲染需烟测` |
| Ring of Red | [PCSX2 Wiki](https://wiki.pcsx2.net/index.php?title=Ring_of_Red) | `Windows端Playable；Mac栏未知；B+仅指烟测优先级` |
| Robot Alchemic Drive | [PCSX2 Wiki](https://wiki.pcsx2.net/index.php?title=Robot_Alchemic_Drive) | `Windows端Playable；Mac栏未知；设置和性能待测` |
| Steambot Chronicles | [PCSX2 Wiki](https://wiki.pcsx2.net/Steambot_Chronicles) | `Windows端Ingame；Mac栏未知；视频优先` |
| 机战OGs | [机战官方系统说明](https://www.suparobo.jp/srw_lineup/srw_ogps/gamedata/outline.html) | `玩法／平台事实；模拟兼容另证` |
| 第2次机战OG | [RPCS3兼容数据库](https://rpcs3.net/compatibility) | `BLJS10133 / Ingame；实验级，不作研发基线` |
| 机战OG 月之民 | [RPCS3兼容数据库](https://rpcs3.net/compatibility)＋[同引擎UYVY渲染问题](https://github.com/RPCS3/rpcs3/issues/18132) | `BLJS10335 / Ingame；实验级，仍有开放渲染风险` |

## 6. 现代游戏官方平台来源

| 游戏 | 官方／商店来源 | 平台结论 | 漂移注意 |
| --- | --- | --- | --- |
| Door Kickers 2 | [Steam](https://store.steampowered.com/app/1239080/Door_Kickers_2_Task_Force_North/) | 正式macOS，M1最低／M2推荐 | 证明官方支持Apple Silicon Mac，不单独证明arm64二进制；仍未在本机启动 |
| Into the Breach | [Steam](https://store.steampowered.com/app/590380/Into_the_Breach/) | 官方Intel时代Mac版，macOS 10.13+ | Apple Silicon原生性未证；作为Rosetta候选烟测 |
| Wildermyth | [Steam](https://store.steampowered.com/app/763890/Wildermyth/) | 有Mac版；官方提示无原生M1且Rosetta表现可能不佳 | 不得写“Apple Silicon良好支持” |
| Inscryption | [Steam](https://store.steampowered.com/app/1092790/Inscryption/) | 官方Intel时代Mac版 | Apple Silicon原生性未证；作为Rosetta候选烟测 |
| Invisible, Inc. | [Steam](https://store.steampowered.com/app/243970/Invisible_Inc/) | 官方Intel时代Mac版 | Apple Silicon原生性未证；macOS 15仍需烟测 |
| BATTLETECH | [Steam](https://store.steampowered.com/app/637090/BATTLETECH/) | Intel时代Mac版 | 旧Unity／图形与稳定性风险；无M系列保证 |
| Pyre | [Steam](https://store.steampowered.com/app/462770/Pyre/) | 官方Mac包；所引页面不足以证明二进制架构 | Mac包存在不等于arm64；先查包架构 |
| Phantom Brigade 2.0 | [Steam](https://store.steampowered.com/app/553540/Phantom_Brigade/)＋[开发者FAQ](https://steamcommunity.com/app/553540/discussions/0/3765607648978533042/) | 官方Windows；FAQ明确没有当前Mac计划 | 2.0功能已改，旧录像需版本标记 |
| Tactical Breach Wizards | [Steam](https://store.steampowered.com/app/1043810/Tactical_Breach_Wizards/) | 官方Windows | 兼容层只能另案，不能冒充官方Mac |
| 13 Sentinels | [Nintendo](https://www.nintendo.com/en-ca/store/products/13-sentinels-aegis-rim-switch/) | Switch；另有PS4 | 无正式PC／macOS版 |
| Outer Wilds | [Steam](https://store.steampowered.com/app/753640/Outer_Wilds/) | Steam系统要求只列Windows | 无已证官方macOS路径；视频／自有主机优先 |
| Marvel's Midnight Suns | [Steam](https://store.steampowered.com/app/368260/Marvels_Midnight_Suns/) | Steam PC版；无已证官方macOS路径 | 视频优先；兼容层另案 |
| Super Robot Wars 30 | [Steam](https://store.steampowered.com/app/898750/30/) | Windows Steam，另有主机版 | 无官方macOS路径 |
| Super Robot Wars Y | [官方站](https://www.bandainamcoent.com/games/super-robot-wars-y) | Windows Steam、Switch、PS5 | 无官方macOS路径 |

## 7. 来源与推论边界

### 可以从录像说

- 某时间点屏幕常驻什么；
- 玩家选中、移动、悬停、提交后画面怎样变化；
- 某版本存在Replay、Rewind、时间线、身体轮廓或某类菜单；
- 一段操作呈现了怎样的点击层级和信息密度。

### 不能只从录像说

- 该系统平衡是否长期稳定；
- 玩家群体普遍觉得好玩；
- 当前最新版本仍完全一样；
- 本项目采用后会得到同样效果；
- 没抽到的失败／关系／长期循环已经成熟。

### 可以从官方页面说

- 开发者宣称的核心功能；
- 正式平台和系统要求；
- 模拟器支持架构与官方兼容状态；
- 某次版本更新的公开变化。

### 不能只从官方页面说

- 玩家实际需要点几次；
- 信息是否易读；
- 长动画是否疲劳；
- Apple Silicon上某个Intel游戏无故障；
- 标为Playable的游戏在本机当前构建必然正常。

## 8. 后续维护规则

1. 新增视频必须分`V0发现`与`V1逐段观察`，不能一发现链接就写操作结论。
2. `Phantom Brigade`等持续更新作品必须写录像日期／版本；无法确认Build就明确写无法确认。
3. 模拟器或商店状态复核时更新`checked`，不要默默覆盖历史判断。
4. 本机完成一次实测后另建`L1`记录，包含模拟器版本、Game ID、设置、输入、关卡和证据；不要直接把本文件的`E1`改名为`L1`。
5. 外部页面消失时保留来源标题、URL、核验日期和支持范围；网页指纹不能替代逐段摘录或录像时间点。
6. 引用任何设计结论时同时带一条不可照搬项和一个失败条件。
