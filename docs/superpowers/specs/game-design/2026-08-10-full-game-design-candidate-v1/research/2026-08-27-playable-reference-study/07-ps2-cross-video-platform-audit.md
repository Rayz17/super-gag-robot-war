# 07｜七款 PS2 参考作的跨视频网站实机审计

> Checked: `2026-08-28`
>
> Status: `candidate_research / video-evidence-expansion / no-local-playtest`
>
> Scope: 本文专门补足此前过度依赖 PCSX2 Wiki 的问题。它回答“网上到底有没有足够的实际游玩材料”“视频里真正看见了什么”“哪些内容值得学”，不把视频存在等同于本机可玩，也不把他人评价等同于本项目已经得到答案。

## 先说结论

有，而且远比项目 Wiki 丰富。七款游戏在 YouTube、Niconico 和B站都能找到长流程、系统片段或系列内容；B站还补到了中文讲解、整备／编组、关系差分和模拟器设置；Dailymotion 能补到少量旧评测。AcFun、优酷和 Twitch 在本轮公开索引检索中没有得到足以支持具体操作结论的可靠目标结果。

这次看视频以后，原先那张“PS2 参考优先级”应拆成三张，不再混为一谈：

| 排序目的 | 建议顺序 | 理由 |
| --- | --- | --- |
| 战术底盘与身体设计 | `Ring of Red → Front Mission 4/5 → 机战OGs` | 前三款分别回答宏观命令怎样落到具身接触、部位和队形怎样进入决策、短输入怎样获得巨大角色回报 |
| 完整机战／RPG幻想 | `樱花大战V → Robot Alchemic Drive → Steambot Chronicles → 机战OGs` | 分别回答关系与出击、人在巨机旁的尺度、机器人生活、名机名招名台词 |
| M2 Max 本机技术烟测 | `Front Mission 4 → Ring of Red → 樱花大战V → 机战OGs → RAD → Front Mission 5 → Steambot Chronicles` | 这是按现有 PCSX2 录像的新旧、版本和变量多少排序，不代表设计价值高低 |

最大的修正不是“找到了一款可以照搬的母版”，而是明确了七款各自能提供哪块拼图：

```text
Front Mission 4/5：身体、射界、队形与协作
Ring of Red：棋盘命令之后展开短具身接触
樱花大战V：共同生活、关系选择、出击与战后余韵形成往返
Robot Alchemic Drive：人类视点、巨机尺度和城市后果同屏
机战OGs：极短输入换来角色、机体、台词、音乐与名招的大回报
Steambot Chronicles：机器人是交通、职业、生活与社会身份，不只是一件武器
```

没有任何一款同时解决本项目的短全队共同轮、诚实敌方意图、人物牌、失败继续、探索、战报与敌方学习、Meta 和有边界 LLM。它们是部件库，不是总案替代品。

## 1. 本轮怎样核验证据

### 1.1 视频证据等级

| 标记 | 本文含义 | 可以支持 | 不能支持 |
| --- | --- | --- | --- |
| `V1-flow` | 取到实际视频流，并在相邻时间点核对操作前后 | 屏幕信息、操作顺序、模式切换、即时反馈 | 完整游戏长期节奏与平衡 |
| `V1-frame` | 取到实际视频流和精确时间点，但没有连续逐按钮记录 | 某时刻确实存在某界面、演出或状态 | 精确输入步数、是否经剪辑省略 |
| `V2-explain` | 系统演示、教程或作者说明与画面相互支持 | 规则形状、典型用法 | 普通玩家真实负担、失败频率 |
| `V3-longplay` | 有完整／长流程和章节，但本轮只抽查关键段 | 游戏总体结构、剧情与战斗的大致比例 | 每一段都已完整看过 |
| `R1-review` | 评测、回顾或榜单片段 | 发现问题、理解历史口碑、形成待核假设 | 代替实机操作证据 |

### 1.2 模拟器视频证据等级

| 标记 | 本文含义 |
| --- | --- |
| `M-A` | 同一视频明确确认 Mac、Apple 芯片、PCSX2 版本和实际运行游戏 |
| `M-B` | 明确是 PCSX2 实际运行，但宿主是 Windows，或操作系统／芯片信息不全 |
| `M-C` | 明确为真实 PS2 采集；只证明原作画面，不证明模拟器 |

本轮找到了 Apple Silicon Mac 运行 PCSX2 的通用 `M-A` 证据，但七款目标游戏都没有形成标题级 `M-A` 闭环。因此本文不会写“七款已确认能在这台 M2 Max 上玩”。

### 1.3 各视频网站分别适合回答什么

| 平台 | 本轮找到的材料 | 最适合回答 | 主要限制 |
| --- | --- | --- | --- |
| YouTube | 七款都有长流程、系统演示、评测或 PCSX2 实机 | 英文版完整流程、章节定位、模拟器版本与设置 | 部分无登录播放触发验证；自动关键帧不能假装成连续观看 |
| Niconico | 七款都有日文实况或系列；多款有完整分 P | 原版 UI、教程、长线章节、玩家实际停留时间 | 老视频分辨率低；标题和说明不一定写采集平台 |
| B站 | 七款均有已抽查的流程／系统素材；另有中文讲解、关系差分、编组、模拟器设置和动画合集 | 中文理解、分P定位、系统讲解、国内玩家操作习惯 | 转载不算独立证据；分 P 和播放器状态需要逐段核验 |
| Dailymotion | RAD 旧评测、Ring of Red 榜单片段、FM4 短实机、Steambot 回顾片段 | 老游戏评论史与补充镜头 | 多为二手评论或短片，不能单独证明操作链 |
| AcFun／优酷／Twitch | 本轮没有取得可稳定复核的目标实机结果 | 以后若有明确直链可补 | “这次没找到”不等于网络上绝对不存在 |

## 2. 七款作品总览

| 游戏 | 最有价值的可核验内容 | 本轮最高玩法证据 | 对本项目的首要用途 | 最重要的反例 |
| --- | --- | --- | --- | --- |
| Front Mission 4 | 任务、AP、部位、武器与 Link 共同出现；战斗—基地—整备连续可见 | `V1-flow + V3-longplay` | 身体信息贴近攻击决定；站位关系立刻产生团队结果 | 菜单和逐台确认过多；Link 退化为追加伤害 |
| Front Mission 5 | 基地人物—任务—部位战往返；射线、友伤与 Link | `V1-frame + V3-longplay` | 让队形、射界和保护责任比纯输出更重要 | 奖励目标可能诱导玩家违背剧情责任 |
| Ring of Red | 战略格命令→局部接触→距离／装填／开火→回战略图 | `V1-flow` | 棋盘抽象怎样兑现为有重量的短身体段 | 每次接敌都展开会极慢，重复动画吞掉战略节奏 |
| 樱花大战V | 城市／剧院生活、LIPS 选择、关系、出击、Boss、战后预告 | `V1-flow`（非战斗）+ `V3-longplay` | 人物关系与战斗形成完整往返 | 默认限时对白、查表好感和长时间无战斗不可照搬 |
| Robot Alchemic Drive | 人在城市中找位置、遥控巨机、新闻插播、建筑与战斗同屏 | `V1-flow + V3-longplay` | 人类视点制造巨大尺度；燃爽和城市责任同时发生 | 操作笨重、视角遮挡、以难控制冒充重量感 |
| 机战OGs | 地图对白、部署／移动／武器、Twin、角色台词与长演出 | `V1-flow + V2-explain` | “输入短、身份回报大”；人物与战斗不分家 | 全歼、倍率技能和重复演出让地图决策变薄 |
| Steambot Chronicles | 人物生活、双杆身体教学、旅行／维修／竞技／战斗、改装回城 | `V1-flow + V3-longplay` | 机器人是日常、职业、交通和关系载体 | 广而浅的小游戏、慢旅行和摩擦操作稀释主循环 |

## 3. Front Mission 4

### 3.1 推荐视频

- YouTube 长流程：[Front Mission 4 Playthrough #1 (No Commentary)](https://www.youtube.com/watch?v=WEq5svRbG9c)，Look Back Gaming，6:13:01。作者说明为英文北美 PS2 版、PCSX2 软件渲染；章节含 `00:31:31 Mission 1`、`00:44:19 Mission 2`、`05:04:16 Mission 9`、`05:28:40 Mission 10`。
- YouTube 评测：[Classic Game Room HD - FRONT MISSION 4 review Part 1](https://www.youtube.com/watch?v=VSsarCNTt1o)，11:21。用于理解当时玩家怎样评价攻击与 Link 规划，标 `R1-review`。
- YouTube 模拟器长实机：[Front Mission 4 PS2 Gameplay HD (PCSX2 v1.7.0)](https://www.youtube.com/watch?v=vCuWX1CZF_8)，Windows 10、PCSX2 1.7.0；`07:17` 教程、`31:14` Mission 1、`46:14` Mission 2、`01:16:23` Mission 3，标 `M-B`。
- Niconico 系列首篇：[MISSION 1—4，回收全部隐藏要素](https://www.nicovideo.jp/watch/sm45588713)，2:46:07；同系列继续覆盖后续任务，标 `V3-longplay`。
- B站英文版流程：[前线任务4 通关流程](https://www.bilibili.com/video/BV1kKdYYVEVE)，34P、总27:29:43；P3 `04:10—07:10` 覆盖部位、目标、主命令和AP落位，P13覆盖人物、技能、基地房间和机库，标 `V1-flow`。
- B站补充流程：[前线任务4 通关视频](https://www.bilibili.com/video/BV1eK4y1v7dp)，23P、总32:56:15，标 `V3-longplay`。
- Dailymotion 短实机：[Front Mission 4](https://www.dailymotion.com/video/x19k028)，只作为老视频补充，不用它覆盖上述长流程证据。

### 3.2 视频实际支持什么

抽查能确认：办公室／任务说明、战略地图、人物头像对白、单位选择、AP 和移动／作用范围、武器与部位状态、战斗演出、任务之间的整备属于同一条产品链。YouTube 长流程约 `04:40:00` 的实机关键帧可见战棋界面同时显示单位肖像、AP、身体／部位状态和武器项；B站 P3 又显示主命令只有 `Attack / Items / Status / End`，复杂度主要在选择后的预测窗。P13 则可见技能购买、休息室和机库。这不是只靠 Wiki 推导出的系统表。

可归纳的操作语句是：

```text
看任务与编组
→ 选 Wanzer
→ 看 AP、范围和身体状态
→ 移动
→ 选武器与目标
→ 看命中／部位
→ 确认
→ Link 单位共同开火
→ 看部件结果并进入下一次决策
```

这条链最值得移植的不是 Link 名字，而是两个界面原则：身体状态要在做攻击决定时出现；协作要由当前站位和关系立刻改变“这次怎么做”，而不是战后给一个被动加成。

### 3.3 给《超GAG》的结论

- 可学：部位先翻译成可用／失去的动词；人物牌和机体关系改变协作形状；同一场任务让对白、身体和战术互相解释。
- 不学：长配装表、同质灰色战场、逐台重复打开菜单、Link 只等于多打一枪。
- 需要本项目另解：不限时短共同轮、敌方意图、非歼灭目标和角色主体性。

## 4. Front Mission 5: Scars of the War

### 4.1 推荐视频

- YouTube 长流程：[Front Mission 5 Playthrough #1](https://www.youtube.com/watch?v=EJYms9QTK_g)，6:30:54，日本 PS2 原作配英文民间补丁、PCSX2；章节含 `00:24:25 Mission 1`、`00:37:23 Mission 2`、`01:15:01 Mission 3`、`05:59:35 Mission 10`。
- YouTube 十分钟实机：[Front Mission 5 English Patched Gameplay](https://www.youtube.com/watch?v=yjY6USxKwRQ)，可快速看见沙漠战、驾驶员头像、部位条和 Link 火力。
- Niconico TAS 首篇：[見るフロントミッション5 mission01](https://www.nicovideo.jp/watch/sm40532316)，25:08；系列继续到后续任务，标 `V1-frame / V3-longplay`。
- B站已逐段核验：[《前线任务5》通关视频 Part 1](https://www.bilibili.com/video/BV1354y1e7C2/?p=2)，项目观察点为 `10:00`、`15:00`、`20:00`、`25:00—25:40`，标 `V1-flow`。
- B站系统补充：[生存模式第100层攻略](https://www.bilibili.com/video/BV1fU4y1C7av)，`00:20` 武器消耗／弹数／命中／伤害，`01:00` 机械师 `REPAIR`，`03:00` AP落位，`04:00` 机体状态，标 `V1-flow`；只用来观察系统，不把100层重复挑战当主线范式。
- Windows 模拟器证据：[Front Mission 5 PS2 Gameplay HD](https://www.youtube.com/watch?v=ezkOFe41tGQ)，Windows 10、OpenGL Hardware、8×分辨率并使用 Half-pixel Offset 等修正，标 `M-B`。

### 4.2 视频实际支持什么

Niconico `约11:24` 的实际帧可见俯视移动选择、蓝色格区、驾驶员头像、AP、Move、武器／伤害／命中信息；`约22:48` 可见多单位战斗、头像面板、伤害与 Miss。B站连续片段又补足了人物—世界—战斗的切换。因此它不是只有“部位战”这一项，而是：基地里的组织与人物，确实进入了任务前后的节奏。

长流程作者说明还提供两个必须验证的设计问题：除近战与导弹外的友军误伤迫使玩家看射线；Mission 10 的击杀奖励会诱导理性玩家牺牲运输队。后者先标 `V2-explain`，因为这轮没有把整张 Mission 10 从输入到结算逐步复演。

### 4.3 给《超GAG》的结论

- 可学：友伤／遮线用来塑造队形，不作为纯惩罚；玩家改装后的机体继续出现在剧情中；基地人物与伤损不能和战斗各过各的。
- 不学：高血量围攻、刷模拟战、任务过长、装备管理占据主循环。
- 奖励规则：高奖励可以奖励更难、更漂亮、更负责任的解法，不能系统性诱导玩家背叛剧情中已明确承担的责任；若故意设计道德诱惑，游戏必须承认这是一次角色／立场选择，而不是把它伪装成“最佳操作”。理性玩家卡规则本身应保留为乐趣。

## 5. Ring of Red

### 5.1 推荐视频

- Niconico 经典完整系列首篇：[訓練場その1](https://www.nicovideo.jp/watch/sm2135397)，23:57；系列 mylist 覆盖后续流程。本文对 `13:00—15:06` 做了相邻视频段核验，标 `V1-flow`。
- YouTube 36小时完整流程：[Ring Of Red Full Game Longplay Complete](https://www.youtube.com/watch?v=nmGm5vxBh_g)，PCSX2、UHD 60fps，标 `V3-longplay / M-B`。
- YouTube 机制短片：[active time battle system used creatively](https://www.youtube.com/watch?v=mVBvRUoa_eU)，4:19，适合先看接触战，标 `V2-explain`。
- YouTube 评测：[Ring of Red: Avalanche Reviews](https://www.youtube.com/watch?v=9u0eh5TcYuc)，20:29，标 `R1-review`。
- Windows PCSX2：[Ring of Red — PCSX2 1.7.0-1189](https://www.youtube.com/watch?v=MQwqCJouttw)，Windows、1080p，标 `M-B`。
- B站长实况：[PS2《赤血风暴》](https://www.bilibili.com/video/BV1GM6qYeErD)，1:59:43；`01:56:40` 可见 AFW 与多个步兵班、前后列、弹药、地形、开始距离和昼夜的接战编组，标 `V1-frame / V3-longplay`。
- B站系统概览：[赤血风暴 Ring of Red（2000）](https://www.bilibili.com/video/BV123Vp63EbQ)，`06:00` 基地菜单，`08:00` 交战HUD，`10:00` 本体／武器／腿部结果，`12:00 / 16:00` 前进／停止／后退，`14:00` 手动瞄准，标 `V2-explain`。
- B站后期压力样本：[美版最终关零瞄准硬打](https://www.bilibili.com/video/BV1uJSrBsEcp)，2:20:48；只作为高压战补充，不据此宣称完整流程已核验。
- Dailymotion 评论片段：[20 Hardest PS2 Games](https://www.dailymotion.com/video/x957j6o)，`约10:06` 涉及本作的手动瞄准与敌方压力，只标 `R1-review`。

### 5.2 已经真正看清的操作链

Niconico 首篇前半先花时间解释任务和战略格。约 `13:00—15:06` 的连续片段清楚显示：

1. 局部接触战开始；
2. 玩家在前进／停止／后退之间控制距离；
3. 画面同时显示武器、腿部状态、装填与 `Ready / Fire`；
4. 玩家选择开火时机与距离；
5. 圆形手动瞄准读数出现，例如约 `57.59%`；
6. 炮弹命中，以近景身体演出结算伤害；
7. 画面回到战略格地图；
8. 下一次接敌再进入局部身体层。

因此它真正证明的不是“有战棋也有动画”，而是：宏观棋盘上的接敌命令，会展开成一小段由距离、姿态、装填、随伴兵与时机共同决定的身体接触，然后把结果还回战略层。

### 5.3 给《超GAG》的结论

- 可学：只把关键接触展开为短身体段；镜头、声音和承力必须兑现棋盘命令；随伴角色可以给当前接触提供局部战法。
- 不学：每次接敌都进入长半实时战斗；执行阶段继续大量微操；相同动画反复完整播放。
- 原型假设：共同轮仍由玩家在提交前完成决定，执行时只在少数焦点接触展开具身镜头和已经预备好的条件反应，不突然变成另一个动作游戏。

## 6. 樱花大战V：再见吾爱

### 6.1 推荐视频

- YouTube 长流程上半：[Longplay 1/2](https://www.youtube.com/watch?v=LgabDDlM8Iw)，10:16:55；下半：[Longplay 2/2](https://www.youtube.com/watch?v=GWNlyy0pQ9g)，11:58:04，均明确为北美 PS2 版，标 `V3-longplay`。
- Niconico 实况系列首篇：[サクラ大戦Ⅴで良い夢を 1-1](https://www.nicovideo.jp/watch/sm36644710)，22:38，本文抽查了开篇城市／人物互动和 `约12:18` 的三项对白选择，标 `V1-flow`（非战斗层）。
- B站中文字幕主线：[第一章第1幕](https://www.bilibili.com/video/BV1z4411v76K)，46:35；`约10:00` 后可见城市地图、街道移动和人物事件，`25:00 / 30:00` 关系推进，`40:00` 星组说明，标 `V1-flow`（非战斗层）。
- B站战斗—战后片段：[第三章第7幕](https://www.bilibili.com/video/BV1z4411s75q)，`05:00` 战场与通信，`07:00` 角色切入，`09:00—15:00` 机甲行动、队友呼叫、协力演出和台词，`17:00` 战后轻喜剧，标 `V1-frame`。抽帧不足以判定完整回合边界，本文不把“画面连续运动”直接写成实时动作制。
- B站好感差分：[洁蜜妮好感最高的情况](https://www.bilibili.com/video/BV1g4411j7bx)，`00:30—02:25` 显示相同事件中理解、亲近态度和帮助内容的差异，标 `V2-explain`。
- YouTube 评测：[The Roaring 20's, Mechs, and Waifus… Sakura Wars 5](https://www.youtube.com/watch?v=x5jboEmB7hE)，8:56，标 `R1-review`。
- PCSX2 4K 实机：[HD Remaster Textures 4K](https://www.youtube.com/watch?v=cxtPrG6E4Mc)，PCSX2 1.7.5709 QT、Vulkan、8×分辨率、可见约100%叠层；宿主 OS 未写明，标 `M-B`。

### 6.2 模式比例和完整往返

YouTube 上半段章节提供了很直观的产品节奏：

- Chapter 1：`00:02:16` 开始，`00:17:36 / 00:51:39` 生活与剧情，`01:35:52` 首战，`02:05:32` Boss，`02:22:18` 下回预告；
- Chapter 2：`02:23:00` 开始，经过四段 Intermission，到 `04:12:12` 才战斗；
- Chapter 3：`06:14:15` Battle 1，`07:08:46` Battle 2，`07:31:47` Boss。

Niconico 实际流又证明：开篇很长一段确实以城市地点、人物对话、回应选择和关系气氛为主，而不是菜单里给好感点。可归纳的整条循环是：

```text
在城市和剧院生活／分配时间
→ 以回应表达当前态度
→ 关系和理解发生变化
→ 出击
→ 不同角色以不同移动、射程、治疗或专属动作参战
→ Boss与名场面
→ 战后回应
→ 下回预告制造下一章期待
```

### 6.3 给《超GAG》的结论

- 可学：关系不是战前菜单 Buff，而是共同生活让“带谁出击、谁在身边、谁会怎样做”有情感意义；战斗结果再回到关系和生活空间。
- 可学：章节预告是低成本、高机战感的期待装置；角色能力要兼有性格、战法和演出身份。
- 不学：限时回答作为默认压力；查攻略寻找唯一高好感答案；让所有关系围绕单一男性；两小时 ADV 后才偶尔给一次战斗。
- 对本项目：默认决策不限现实时间。若个别剧情把迟疑本身写成戏，可明确做成少量可选／特殊节点，不把它扩成整套游戏的倒计时。

## 7. Robot Alchemic Drive

### 7.1 推荐视频

- Niconico 实况首篇：[大鉄人を操縦してみた Part 1](https://www.nicovideo.jp/watch/sm44167739)，35:07；本文抽查 `15:54`、`19:06`、`28:42`、`31:54`，标 `V1-frame / V3-longplay`。
- YouTube 长流程：[Longplay of Robot Alchemic Drive](https://www.youtube.com/watch?v=Rkx2qr5z1f0)，10:29:51，NTSC PS2 版，标 `V3-longplay`。
- YouTube 评测：[Classic Game Room - RAD review](https://www.youtube.com/watch?v=5HXsIK5noBU)，9:17，标 `R1-review`。
- Dailymotion 旧评测：[Classic Game Room - ROBOT ALCHEMIC DRIVE PS2 review](https://www.dailymotion.com/video/xqmgx8)，可作为早期英文评论补充，不作为独立操作证明。
- Windows PCSX2：[RAD / Robot Alchemic Drive — PCSX2 4K](https://www.youtube.com/watch?v=5qUN2SnhY2I)，Windows 10、PCSX2 1.5 开发版，标 `M-B`。
- B站长流程／速通：[Robot Alchemic Drive Laguiole Speedrun](https://www.bilibili.com/video/BV1Ly4y157XN)，6:20:30；`13:40` 肩键迈步，`14:00` 右摇杆驱动右臂，`14:20 / 15:00 / 15:20` 方向与旋转形成不同拳击动作，`16:00` 面键武器，标 `V1-flow`。
- B站实体试玩：[美版PS2实体试玩](https://www.bilibili.com/video/BV1C2DpYqEXR)，`06:00` 三台巨机差异，`10:00` 电视新闻，`15:00` 人在地面且巨敌在身后，`25:00—30:00` 战斗HUD和人物通信，标 `V1-frame`。
- B站分屏验证：[Robot Alchemic Drive 分屏对战](https://www.bilibili.com/video/BV1vo4y1U74v)，`05:00` 一侧仍控制地面人物逃离巨机，证明“操作者肉身在场”不是只存在于剧情描述，标 `V1-frame`。

### 7.2 视频真正显示了什么

Niconico 画面依次可见：

- `15:54`：人类角色站在屋顶／城市高处，手持遥控器，HUD 与人类位置同时存在；
- `19:06`：从人所在位置看见远处巨机，尺度来自人和建筑，不来自数字说明；
- `28:42`：BNN LIVE 新闻式画面覆盖巨机与城市事件；
- `31:54`：巨型机器人在道路和建筑之间拳斗。

核心操作不是普通驾驶舱第三人称，而是：人先跑到能看见战场的位置，再遥控机器人，人的安全、视野、巨机身体和建筑破坏同时成立。B站连续教学还证明原作把双腿、双臂和摇杆／肩键做了强对应；这能制造身体感，也直接暴露了高频疲劳风险。

### 7.3 给《超GAG》的结论

- 可学：偶尔把镜头放回人类身边；让机体从“我的光标”重新变成庞然大物；新闻、旁观者和环境后果可以把一拳重新写成社会事件。
- 不学：一肢一键、故意别扭的移动和遮挡视角；用难操作代替重量；反复一对一摔跤。
- 适用位置：少量名场面、现场调查、救援、城市守护或角色亲历段。它不是整个战棋输入层的替代品。

## 8. 超级机器人大战 Original Generations（PS2）

### 8.1 推荐视频

- YouTube 长流程：[OG1 ATX - Scenario 1—8](https://www.youtube.com/watch?v=ULWlkXtMC4A)，6:55:54；作者说明为真实 PS2 配英文民间补丁，标 `V3-longplay / M-C`。
- YouTube 系统实机：[PS2 Super Robot Taisen OG: Original Generations](https://www.youtube.com/watch?v=C32JdDW_T74)，41:06；约 `10:17` 必杀演出、`20:33` 地图与人物、`30:50` 移动范围与地图输入，标 `V2-explain`。
- YouTube Twin 短片：[Twin Battle System Demo](https://www.youtube.com/watch?v=rfZS5TS-nWo)，1:31，标 `V2-explain`。
- Niconico 挑战系列首篇：[OG2 低改造挑战 Part 1](https://www.nicovideo.jp/watch/sm8792359)，12:42；本文核对了开篇地图对白到移动／攻击的连续过渡，标 `V1-flow`。
- B站逐段核验：[OGS/OG2 第22话](https://www.bilibili.com/video/BV1si421f7eR/)，观察点 `05:00`、`09:50—10:20`、`20:00`、`40:00`、`60:00`、`80:00`，标 `V1-flow`。
- B站完整回顾：[第一次超级机器人大战OG回顾合集（OGS+OGG）](https://www.bilibili.com/video/BV1rb411y7k4)，36P、总109:26:10，标 `V3-longplay`。
- B站编组讲解：[OGS1主力搭配推荐](https://www.bilibili.com/video/BV1zk4y1571J)，`02:00` 驾驶员／精神／Ace／地形，`04:00` 援护，`06:00` 合体攻击，`10:00` Twin Command，`12:00` 组合台词与招式，标 `V2-explain`。
- B站技术补充：[PS2模拟器玩各版本机战最优化效果演示](https://www.bilibili.com/video/BV1wL4y1B7ii/)、[电脑上完美畅玩机战OG/OG外传](https://www.bilibili.com/video/BV1Lg411M7fn/)、[OG战斗动画合集](https://www.bilibili.com/video/BV1P64y1z76E/)。这些只能证明上传者的 PCSX2 路径／设置经验，不能据“完美”二字推导 Mac 兼容。
- 2026 PCSX2 新录像：[OGs English Translation on PCSX2 2.7.281](https://www.youtube.com/watch?v=HiMdw0Mxc2g)，操作系统未写明，标 `M-B`。

### 8.2 视频实际支持什么

Niconico 首篇前约七分钟，人物头像和对白直接长在战场地图上；随后进入地图移动、攻击确认和战斗动画，对话继续穿过动作，而不是等战斗结束再补人物戏。YouTube 与B站片段共同呈现的基本链是：

```text
部署／编组
→ 选机
→ 看移动范围
→ 选武器并看射程、EN、弹药、命中与反击
→ 确认
→ 人物台词、音乐和专属战斗演出兑现
→ 回到地图
→ 精神、援护、Twin与关系改变下一次选择
```

### 8.3 给《超GAG》的结论

- 可学：地图输入应尽量短，回报由角色、机体、台词、镜头、音乐和结果共同放大；人物对白可以在地图和行动之间持续存在。
- 可学：出席与编组应生成新的战法和对应演出，而不只是出场名单；Twin 是“组合产生新语法”的粗糙先例。
- 不学：全歼默认、必中／热血堆倍率、地图长期缺少身体性、每次普通攻击都播放完整长动画。
- 版本边界：这里是 2007 年 PS2《OGs》及民间翻译材料，不是 PS3《第二次OG》或其他作品。

## 9. Steambot Chronicles

### 9.1 推荐视频

- Niconico 新系列首篇：[ポンコツ浪漫大活劇バンピートロット #1](https://www.nicovideo.jp/watch/sm45393883)，20:57；本文核验 `约05:42` 与 `07:36` 的驾驶教学，标 `V1-flow`。
- YouTube 长流程：[Steambot Chronicles - Full Game Longplay Part 1](https://www.youtube.com/watch?v=UveFtzHfPv4)，11:45:58，标 `V3-longplay`。
- YouTube 深度回顾：[The Greatest PS2 Game Nobody Cares About](https://www.youtube.com/watch?v=a8fMBp0JfAA)，2:05:31；用于观察生活、改装和 HUD，标 `R1-review`。
- Windows PCSX2 旧录像：[Steambot Chronicles — PS2 Gameplay SD + FXAA](https://www.youtube.com/watch?v=2lMGk30ouC4)，Windows 7、PCSX2 1.2.1，标 `M-B`，但证据非常陈旧。
- Dailymotion 回顾片段：[10 Weirdest PS2 RPGs](https://www.dailymotion.com/video/x8n75gz)，约 `02:21` 起涉及本作，只作二手评论。
- B站长流程：[ナンコツ浪漫大活劇【バンピートロット】](https://www.bilibili.com/video/BV1p8w8eQEcv)，9P、总29:20:57；P2 可见生活选择、旅行、修理厂、城市昼夜和说明书，标 `V1-frame / V3-longplay`。
- B站中文系统介绍：[破烂机器人的浪漫大活剧](https://www.bilibili.com/video/BV1ed4y1k7gC)，`04:00` 城市交通，`05:30—06:00` 双杆／冲刺／跳跃，`07:00` NPC与物品，`08:30` 战斗、拾取与加油，`09:00` 竞技场，`10:00` 饥饿，`13:30` 关系场面，标 `V2-explain`。

### 9.2 已经看清的教学和产品身份

Niconico `约05:42` 的教学把画面分成四块，分别说明左右摇杆怎样驱动左右腿；`约07:36` 再讲冲刺／跳跃。后续实际画面出现机器人战斗、探索、人物对话和选择。YouTube 长流程及回顾又补足了竞技场、城镇、燃料／Boost、左右臂、改装外形等长期层。

它最重要的启发不是双杆操作，而是同一台机器人在不同场合拥有不同社会身份：交通工具、劳动工具、竞技身体、战斗机体、个人外观和人与人相识的媒介。B站长流程 P2 还可见修理菜单分别处理本体、双臂和燃料，让旅行损耗回到生活空间，而不是只在战后弹一个维修账单。

### 9.3 给《超GAG》的结论

- 可学：机体部件优先改变能做的事与生活用途；万机馆、城市巡访和共同出行要真正读取机体状态；角色可以和机体在非战斗场景中持续相处。
- 不学：什么小游戏都做、长距离慢移动、隐蔽收集劳动、把身体感等同于难操作。
- 对本项目：非战棋层不应另造三套无关小游戏。它们要共享角色、机体动词、伤损、知识、关系和地点状态。

## 10. Apple Silicon 与七款游戏：视频能证明到哪一步

### 10.1 通用 Mac 路径已经有实机证据

- [PCSX2 2.0 on Mac](https://www.youtube.com/watch?v=Az8Fdt8PBx4)：明确为 M1 MacBook Air、8GB、PCSX2 2.0；含安装、BIOS、游戏镜像、手柄、图形设置和多款游戏，标通用 `M-A`。
- [PCSX2 setup for M1 Mac](https://www.youtube.com/watch?v=vBeSD4F4IUs)：2021 年 tellowkrinkle 1.7 分支的历史路径，明确为 M1 Mac，标历史 `M-A`。
- [B站转载](https://www.bilibili.com/video/BV1AL4y1M7ia/)明确来自上一条，因此不能再算一份独立证据。

这能支持“PCSX2 在 Apple Silicon Mac 上有真实运行路径”。M2 Max 的性能大概率不是第一风险，但不能外推为某一标题无渲染、存档或关卡问题。

### 10.2 七款标题级证据

| 游戏 | 最高模拟器视频证据 | 当前能否写“Mac可玩” |
| --- | --- | --- |
| Front Mission 4 | `M-B`：Windows PCSX2 1.7.0，多任务 | 不能 |
| Front Mission 5 | `M-B`：Windows PCSX2，旧版且使用图形修正 | 不能 |
| Ring of Red | `M-B`：Windows PCSX2 1.7.0-1189 | 不能 |
| 樱花大战V | `M-B`：PCSX2 1.7.5709、Vulkan、可见100%叠层，OS未写 | 不能 |
| Robot Alchemic Drive | `M-B`：Windows PCSX2 1.5 开发版 | 不能 |
| 机战OGs | `M-B`：PCSX2 2.7.281，OS未写 | 不能 |
| Steambot Chronicles | `M-B`：Windows PCSX2 1.2.1，证据很旧 | 不能 |

本轮分别检索了游戏名加 `M1 / M2 / M3 / MacBook / PCSX2`，没有取得七款中任何一款的标题级 `M-A` 视频。准确说法只能是“本轮没找到”，不能宣称它们在 Mac 上一定不能运行。

## 11. 最省时间的观看路线

用户或研发者不需要先看几十小时。第一轮可按下列顺序跳看，目标是建立完整的交互印象，不是云通关：

1. **Ring of Red，12分钟左右**：Niconico `13:00—15:06` 看完整接触循环，再看 YouTube 4:19 机制短片；回答“棋盘命令怎样长出身体”。
2. **Robot Alchemic Drive，12分钟左右**：Niconico 跳 `15:54 / 19:06 / 28:42 / 31:54`；回答“怎样从人类尺度看巨机和城市后果”。
3. **樱花大战V，15分钟左右**：Niconico `约12:18` 看回应，再跳 YouTube `01:35:52` 首战与 `02:22:18` 下回预告；回答“关系怎样进出战斗”。
4. **Front Mission 4，15分钟左右**：YouTube `00:31:31` 开始看 Mission 1，随后抽看 Link 与部位确认；回答“站位、身体和协作怎样在一次确认中汇合”。
5. **Front Mission 5，12分钟左右**：Niconico `约11:24 / 22:48`，再看B站 `25:00—25:40`；回答“基地人物、队形与部位结果怎样同属一条循环”。
6. **机战OGs，12分钟左右**：Niconico 首篇前十二分钟或 YouTube `10:17 / 20:33 / 30:50`；回答“短输入怎样换取巨大的角色／机体回报”。
7. **Steambot Chronicles，10分钟左右**：Niconico `05:42 / 07:36`，再抽看 YouTube 长流程的城镇与竞技场；回答“机器人怎样成为生活身体”。

如果只能看三款：先看 `Ring of Red + 樱花大战V + Robot Alchemic Drive`。它们分别补战棋具身、角色关系和巨物尺度，是此前只读 Wiki 最容易漏掉的三件事。

## 12. 交给 Cursor 时的使用规则

### 12.1 可以交给实现者的内容

每个参考只交付一条可实现、可反驳的观察语句，例如：

```text
观察：Ring of Red在战略接敌后展开一段距离／装填／开火的局部身体战，再回战略图。
假设：本项目只对焦点接触展开5—12秒具身兑现，普通接触精简结算。
失败条件：玩家每轮等待时间明显增加，或执行阶段又要求临时微操。
```

```text
观察：樱花大战V让城市关系、角色打法、Boss和战后回应形成往返。
假设：C01中至少一项关系状态同时改变可用人物动作、战场对白和返馆场景。
失败条件：关系只换伤害倍率，或战斗结果不被角色生活读取。
```

### 12.2 不可以交给实现者的伪结论

- “照着某款游戏做一套 UI”；
- “Wiki 写 Playable，所以 Mac 不用测”；
- “长流程里出现了很多系统，所以这些系统都好玩”；
- “评测说独特，所以操作摩擦也应该保留”；
- “OG 的回报强，所以人物牌可以重新退回必中、增伤和再动”；
- “樱花大战关系有效，所以默认加入倒计时选项”；
- “RAD 很有重量，所以每个动作都做成笨重手操”。

### 12.3 原型必须保持的项目边界

1. 默认回合不限现实思考时间；时间压力若出现，只能是少量明确的特殊／可选规则。
2. 理性玩家利用公开规则做漂亮强解是一项乐趣；应修的是唯一答案、隐藏例外和奖励诱导叙事背叛，不是消灭钻规则。
3. 普通动作不走审批链；人物牌和机魂只在真正改变打法、关系或边界的节点前台化。
4. 战棋、探索、返馆和关系共享角色、机体、伤损、知识、地点与后果，不做互不相干的小游戏合集。
5. 竞品视频只提供交互证据，不提供项目角色、台词、地图、美术、数值和关卡资产。
6. 在本机完成启动、输入、第一段实玩、存档／载入、渲染器和代表性关卡复核前，标题状态保持 `L0`。

## 13. 本轮仍未解决的研究问题

- 七款中没有一款可直接证明“短全队共同轮＋诚实敌意＋巨型身体”的完整界面；仍需本项目灰盒比较。
- 没有视频替本项目解决人物牌如何在五张出席、每轮两张上限内保持长期新鲜。
- 七款都没有成熟的世界内 Meta、版本战争、事实账／战报／敌方学习闭环。
- 七款都不能提供有边界 LLM 长期陪伴的答案。
- 视频可以筛选值得亲手玩的游戏，不能替代这台 Mac 上的输入延迟、字体、菜单负担、存档和长任务疲劳实测。

所以，下一步若取得合法自有介质，不是把七款全部通关，而是按[03｜Mac 模拟器与运行矩阵](03-mac-emulator-and-running-matrix.md)建立短烟测，每款只回答一两个项目问题。若暂时没有介质，这份跨平台录像证据已经足够支持 Cursor 做隔离灰盒比较，但还不够把任何竞品机制直接写进核心总案。
