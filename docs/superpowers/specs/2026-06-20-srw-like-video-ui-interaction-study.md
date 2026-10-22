# 《超GAG机器人大战：万机残响》SRW-like 交互影像研究与 Demo 重做标准 v0.1

> 目的：回答用户指出的核心问题：当前 demo 虽然从 DOM 改成 Phaser，但仍然“太 low、像网页、没有人愿意付钱”。本报告不是再写世界观，而是把 SRW 与同类战棋的交互语法拆成下一版可执行标准。

## 0. 调研方式与可信度说明

本轮使用 4 个只读 subagent 并行拆分：

1. SRW 本家玩法与交互观察：SRW 30 / V / T / X / GBA-DS 老作的流程、地图、菜单、战斗演出。
2. 同类战棋 UI/交互：Advance Wars、Into the Breach、Triangle Strategy、Fire Emblem、13 Sentinels。
3. 低成本 2D 技术方案：Phaser、Tiled、Aseprite、sprite atlas、camera、cut-in、audio、shader/scanline。
4. 中文玩家群体反馈：B站、机核、Steam、媒体测评、玩家吐槽与付费期待。

限制：YouTube/B站等视频站在当前环境无法稳定完整播放、抓评论或逐帧分析；本报告会诚实地区分“官方页面/文档/评测/玩家评论/视频标题与公开信息”。下一步如果要做逐帧演出节奏，应单独建立 3-5 条视频时间码拆解表。

## 1. 结论先行

当前 demo 的问题不是“缺美术”，而是缺少 SRW-like/战棋游戏的交互仪式。

美术可以提高第一眼质感，但不能替代这些东西：

- 玩家按键后，系统是否立即给出战棋语义反馈。
- 玩家行动前，是否能预览后果。
- 玩家确认行动时，是否有承诺感和演出爆点。
- 行动结束后，地图局势是否产生清楚变化。
- 单位是否像“机体/驾驶员组合”，而不是表格里的棋子。

下一版 demo 的目标不应是“把网页画漂亮”，而应是重做一个可试玩的垂直切片：

`战前事件 -> 出击/部署 -> 地图光标 -> 单位选择 -> 移动范围 -> 行动菜单 -> 攻击预测 -> 战斗 cut-in -> 地图结果 -> 敌方阶段 -> 战后结算/档案解锁`

## 2. 当前 Demo 为什么仍然像网页

以当前 Phaser demo 为反面样本，主要症状如下。

### 2.1 画面结构像信息面板，不像战术战场

当前画面由大标题栏、右侧文字栏、底部操作提示和规则格子组成。它有 Canvas，但视觉语言仍像管理后台：

- 胜败条件是文字清单，不是任务 UI。
- 单位是色块加单字，没有机体轮廓、朝向、阵营识别、大小重量感。
- 地图是均匀方格，没有地形信息、危险层、遮挡层、部署点、事件点的舞台感。
- 右侧面板占据大量空间，但没有战斗预测、武器信息、援护信息、敌意图这些真正有决策价值的内容。

### 2.2 输入闭环存在，但没有“手感”

底层已有 `idle -> move -> command -> target -> battleCutin` 状态，但表现层缺少：

- 光标移动音、吸附感、脉冲框。
- 选中单位后的小位移/抬升/能量环。
- 移动路径预览与单位 tween 移动。
- 菜单焦点态、确认/取消音效。
- 相机跟随与镜头重新构图。

玩家能操作，但不会觉得“这台机体被我调动了”。

### 2.3 行动没有预测，所以不像战棋决策

现在攻击目标后直接进入结算 cut-in。缺少 SRW/战棋非常关键的中间层：

- 我方武器名、射程、EN/弹数消耗。
- 预计伤害、命中、暴击、击破标记。
- 敌方是否反击、反击武器、反击伤害。
- 援护攻击/援护防御是否触发。
- 气力/士气是否达到大招阈值。

没有 forecast，攻击就像网页按钮触发事件，而不是战棋决策。

### 2.4 战斗演出太抽象，没有“机器人”

当前 cut-in 是双方剪影、武器名、伤害数字。它证明了切屏逻辑，却没有让玩家觉得看到机器人战斗：

- 没有驾驶员头像/台词/喊招。
- 没有武器轨迹、速度线、闪白、hit-stop、shake、爆炸。
- 没有地图单位受击后的回弹/冒烟/击坠。
- 没有普通攻击和必杀技之间的层级差异。

SRW 的高成本演出可简化，但“确认攻击后有一段仪式”不能没有。

### 2.5 梗点还没有玩法化

现有设定里有法务、万机馆、留言墙、0号侧廊，但 demo 里主要是文字说明。机器人粉丝向游戏的梗点应该进入系统：

- 法务敌人封印武装名，玩家需要临时改名或用“民间叫法”解锁。
- 模型厂商梗变成装备件、未打磨件、限定透明装甲。
- 监督/作画梗变成关卡 modifier，例如“低预算回合”压缩动画但提高行动效率。
- 热血/真实系梗变成气力、弹药、地形、援护、喊招蓄力。

## 3. SRW-like 的核心交互语法

### 3.1 一话的状态机

SRW-like 不是“地图打几下 + 剧情文本”，而是一套带节奏的状态机：

1. 战前剧情：角色动机、敌人出现、胜败条件。
2. 出击/整备：机体、驾驶员、强化件、精神指令、部署位置。
3. 我方阶段：地图光标、单位选择、移动、攻击、精神、待机。
4. 攻击预测：伤害、命中、反击、援护、消耗。
5. 战斗演出：驾驶员/机体 cut-in、武器演出、伤害反馈。
6. 返回地图：HP/EN/弹数变化、气力变化、击坠、掉落、事件触发。
7. 敌方阶段：敌人按目标推进，玩家承受此前决策后果。
8. 中途事件：增援、Boss 台词、特定交战对话、目标变更。
9. 战后结算：经验/资源/损伤/隐藏条件/档案/下一话钩子。

### 3.2 每次行动的三段式

下一版必须让每个行动遵循：

`预览 -> 承诺 -> 反馈`

- 预览：玩家知道移动后能打谁、敌人能打谁、预计结果是什么。
- 承诺：确认动作有短暂停顿、菜单收束、镜头指向目标。
- 反馈：动画、音效、数值变化、地图状态改变、角色短台词。

当前 demo 主要只有“承诺后的文字反馈”，缺少预览和多层反馈。

### 3.3 UI 应该像“战术驾驶舱”

SRW-like UI 不一定要复杂，但信息层级必须像游戏：

- 中央：地图、单位、光标、范围层、敌意图。
- 左下：当前单位卡，头像、机体名、HP/EN/SP、气力。
- 右下：行动菜单或武器菜单。
- 右上：胜败条件、回合、阶段、危险提示。
- 顶部/侧边：行动顺序、敌方意图、增援预告。
- 中央覆盖：PHASE、BOSS、MISSION CLEAR、CRITICAL 等大事件。

普通说明文字应退到 tooltip/帮助层，不能成为第一视觉。

## 4. 可借鉴对象的落地启示

### 4.1 SRW 系列

需要保留：

- 战略层与战术层的切换：任务选择、整备、改造、驾驶员培养、强化件、资料查看，再进入一话地图。
- 手柄式菜单节奏：即使是整备菜单，也要有光标、分页、确认/取消音效、焦点态，而不是网页表单。
- 机体/驾驶员一体化：机体有武器和性能，驾驶员有精神、台词、成长。
- 单位命令短菜单：移动、攻击、精神、能力、道具、待机，层级清晰。
- 武器列表：武器名、射程、消耗、必要气力、可移动后攻击、可用/不可用原因。
- 精神指令式爆发：必中、闪避、热血、魂、幸运等可以原创换皮，但要保留“战前预谋的戏剧性按钮”。
- 气力/士气阈值：大招不是随时可用，而是战斗越打越燃。
- 援护攻击/援护防御：站位关系带来角色关系的玩法化表达。
- 特殊战斗对话：不是剧情外说话，而是在特定交战中发生。
- 合体攻击/组合技：跨角色关系的最高爽点。
- 隐藏条件：救人、提前击坠、让特定角色交战，换来隐藏机体/武装/剧情。
- 跳过/加速：现代玩家会看新招和名场面，但不愿重复看杂兵动画；动画开关和敌方回合加速要从 demo 期设计。

可以简化：

- 完整命中/回避公式不必一开始复杂。
- 全武器长动画不必一开始全做。
- 大量改造数值、PP/技能树、复杂芯片可后置。
- 每关全灭敌人的传统目标应减少。

SRW 本家对下一版 demo 的最低要求：

`选单位 -> 单位命令 -> 移动/攻击/精神 -> 范围显示 -> 武器列表 -> 战斗预览 -> 确认 -> 战斗演出 -> 地图结果 -> 经验/资源/事件反馈`

当前 demo 最大缺口是少了“单位命令前后的预览层”：不能让玩家先查看武器、精神、反击和支援，再做承诺。

### 4.2 Into the Breach

最重要启示：低成本也能高级，但必须极致清晰。

可借鉴：

- 敌方意图预告：敌人下一步要打哪里，玩家每回合解局。
- 伤害预测清楚：每个格子的风险和收益直接显示在地图上。
- 小动画服务规则：没有华丽大招，但每个推拉、阻挡、受击都清楚。

用于《超GAG》：

- 法务无人机在敌方阶段前显示“封印线”或“回收箭头”。
- 玩家能提前看到留言墙、0号侧廊、平民、机体会被谁威胁。
- 机器人梗变成“如何拆敌意图”的地图谜题，而不是纯台词。

### 4.3 Advance Wars

可借鉴：

- 明亮清楚的格子战场。
- 单位选择、移动范围、攻击范围的低成本但稳定反馈。
- 指挥官能力/CO Power 的仪式感。
- 战斗动画可跳过，但即使短动画也有单位冲突感。

用于《超GAG》：

- “监督槽/燃魂槽/制作费槽”可以作为本作等价的全局爆发。
- 普通攻击用短动画，必杀/合体攻击用长 cut-in。

### 4.4 Fire Emblem / Triangle Strategy

可借鉴：

- combat forecast：攻击前对双方结果一眼可见。
- 地形、高低差、背刺/夹击等让地图成为规则对象。
- 行动顺序或敌方危险范围让玩家规划多步。

用于《超GAG》：

- 攻击预测窗口必须是下一版 P0。
- 地形不只“墙/空地”，应有展柜、舞台灯、消防门、模型货架、观众通道等效果。

### 4.5 13 Sentinels

不直接借战斗 UI，借结构：

- Remembrance：角色故事。
- Destruction：战斗。
- Analysis：档案/事件图谱。

用于《超GAG》：

- 战后解锁“机魂档案”“万机馆事件图谱”“被封存名场面”。
- 玩家不是被动读设定，而是在战斗后获得新线索，反推世界真相。

## 5. 下一版 Demo 的硬性验收标准

### 5.1 第一眼标准

打开 demo 后 10 秒内必须像游戏，而不是网页：

- 全屏或准全屏 Canvas 游戏画面。
- 地图是主视觉，不是文字面板。
- 有动态光标、单位 idle 动画、背景细节动画。
- UI 有统一 skin：金属边框、阵营色、像素/机战风按钮焦点态。
- 底部不要再放普通网页式操作说明条；操作提示应像游戏 HUD。

### 5.2 单位与机体标准

至少 3 台风格不同机体：

1. 超级系：高 HP、高气力成长、近战必杀、热血/燃魂。
2. 真实系：移动高、弹药/EN 管理、远程牵制、回避/集中。
3. 支援系：修理/补给/指挥/降温/援护防御。

每台机体必须有：

- SD/Q版地图 sprite，占位也要有轮廓。
- idle 动画。
- move tween。
- hit 闪白/抖动。
- 至少 1 个普通攻击短演出。
- 主角机至少 1 个大 pose cut-in。

### 5.3 地图交互标准

必须实现：

- 常驻格子光标，键盘和鼠标都驱动同一个光标状态。
- 选中单位显示蓝色移动范围。
- 选择移动格显示路径预览。
- 移动后显示行动菜单：攻击、精神、援护/技能、待机、取消。
- 攻击菜单列出武器：伤害、射程、EN/弹数、气力需求。
- 目标 hover 显示战斗预测。
- 敌方危险范围 toggle。
- 至少 1 种敌意图箭头或封印线。

### 5.4 战斗预测标准

攻击确认前必须出现 forecast：

- 我方：攻击名、预计伤害、命中、消耗、是否击破。
- 敌方：是否反击、预计伤害、命中。
- 援护：谁会援护、援护攻击/防御剩余次数。
- 特殊：气力变化、目标保护对象风险、隐藏条件提示。

即使数值系统先简化，也要有这个 UI 形态。玩家要先相信“我在做战术选择”。

### 5.5 演出反馈标准

普通攻击：

- 镜头 pan 到攻击者和目标。
- 攻击者 sprite 蓄力或后坐。
- 武器特效飞向目标。
- 命中 hit-stop 80-120ms。
- 目标闪白、抖动、伤害数字弹出。
- 若击坠，目标爆炸/淡出/残骸。

必杀/cut-in：

- 背景暗下。
- 驾驶员头像/正比例机体 pose 滑入。
- 武器名大字出现。
- 速度线/遮罩/闪白。
- 回到地图时目标受击并更新 HP。

### 5.6 战中剧情标准

demo 至少包含：

- 首次接敌短对话。
- 特定角色攻击特定敌人触发特殊战斗台词。
- 友军低血或留言墙受损触发短事件。
- 敌方增援或目标变化触发 phase interrupt。

台词要从角色视角出发，不能像系统在讲设定。

### 5.7 梗点玩法化标准

下一版至少展示 3 个“懂机战/懂机器人”的玩法化梗：

1. 法务封印武装：敌人用封存线锁某个武器名，玩家用“民间叫法/临时改名”解除。
2. 气力喊招：角色在危险中气力上升，达到阈值解锁大招。
3. 援护台词：特定角色相邻时触发援护攻击/防御，并说一句有个性的短台词。

可选强化：

- 低预算回：战斗动画被压缩，但获得行动效率 buff。
- 模型件：未打磨件便宜但暴击会掉零件，限定件强但维修贵。
- 主镜头位：站在地图上的“镜头位”开光束武器有加成。

## 6. 技术路线

继续用 Phaser，但重做表现管线：

`Tiled 地图 -> Phaser Tilemap -> 资产 manifest -> sprite atlas/animations -> Phaser Scene 状态机 -> Camera/Sound/FX -> 可替换美术`

### 6.1 为什么不现在换引擎

- Phaser 已接入项目，Codex 可直接维护。
- Tilemap、Animation、Camera、Sound、Shader/overlay 都够做下一版。
- Godot 更适合后续产品化原型，但现在切换会消耗时间，不能直接解决交互低质。
- Pixi 渲染强，但需要自建更多游戏结构。

### 6.2 一周内可落地的视觉升级

Day 1：统一分辨率、像素缩放、字体、色板、UI skin token。  
Day 2：接 Tiled 或等价 JSON 地图，拆地形层/装饰层/对象层/事件层。  
Day 3：建立单位 atlas/manifest，至少 3 台单位有 idle/move/hit。  
Day 4：重做选中、移动范围、路径预览、攻击范围、敌意图。  
Day 5：做 combat forecast 和武器菜单。  
Day 6：做普通攻击与必杀 cut-in 的演出管线。  
Day 7：接音效、shake、hit-stop、战中对话、结算档案。

### 6.3 最小资产表

| 资产 | 最小规格 | 用途 |
| --- | --- | --- |
| 地图 tileset | 16x16 或 24x24 源像素 | 展厅、通道、展柜、侧廊、消防门 |
| 单位 SD sprite | 32x32 或 48x48 | 地图单位 |
| idle | 4 帧 | 待机生命感 |
| move | 4-6 帧或 tween | 移动反馈 |
| attack | 4-6 帧 | 普通武器 |
| hit | 2-3 帧 | 受击反馈 |
| explosion | 通用 6-8 帧 | 击坠 |
| cut-in pose | 1024x512 或 1280x720 | 必杀/典藏 |
| UI skin | 9-slice 边框、按钮、选择框 | 统一质感 |
| 图标 | 24x24 或 32x32 | 武器、EN、SP、气力、援护、地形 |
| 音效 | wav/ogg | 光标、确认、取消、命中、爆炸、phase |

## 7. 下一版 Demo 建议关卡

建议不要继续从完整第一章全量铺开，而是做一个 15-20 分钟垂直切片：

### 关卡名

第 1 章第 2 话改造版：《法务警报：留言墙防卫战》

### 出击单位

- 纪存 / 策展指挥机：指挥、改名解除封印、弱攻击。
- 兜灯 / 工具支援机：降温、修理、援护防御。
- 豪司 / 勇拳试作机：超级系近战、气力阈值大招。
- 唐胶 / 拼装陷阱机：布置障碍、弹药有限、地形控制。

### 敌方

- 法务无人机：封印武装名，显示封存线意图。
- 回收框体：向留言墙推进。
- 预算审计机：使某回合进入“低预算演出”。

### 目标

- 胜利：保护留言墙 5 回合，或击退审计机。
- 失败：留言墙被清除、平民未撤离、纪存击坠。
- 隐藏：3 回合内让豪司气力到 130 并击坠审计机，解锁临时合体技“闭馆前最后一拳”。

### 必须展示的高光

- 法务无人机封印“闭馆掌”，UI 中武器变灰。
- 纪存使用“民间叫法登记”把它临时改成“把门关上那一下”，武器恢复。
- 豪司被打到低血，兜灯援护防御，触发短台词。
- 气力满后首次出现大 pose cut-in。
- 战后解锁“万机馆档案 001：为什么机魂不等于版权残影”。

## 8. 参考来源

### 官方/系统资料

- [Steam: Super Robot Wars 30](https://store.steampowered.com/app/898750/Super_Robot_Wars_30/)
- [SRW 30 官方 Steam 在线手册](https://srw30-thirty.suparobo.jp/manual/steam/)
- [《超级机器人大战30》中文官网](https://srw30-thirty.suparobo.jp/sc/)
- [Steam: SUPER ROBOT WARS Y](https://store.steampowered.com/app/1909950/SUPER_ROBOT_WARS_Y/)
- [Steam: Super Robot Wars V](https://store.steampowered.com/app/1031500/SUPER_ROBOT_WARS_V/)
- [Steam: Super Robot Wars X](https://store.steampowered.com/app/1031510/SUPER_ROBOT_WARS_X/)
- [Nintendo: Advance Wars 1+2 Re-Boot Camp](https://www.nintendo.com/us/store/products/advance-wars-1-plus-2-re-boot-camp-switch/)
- [Subset Games: Into the Breach](https://subsetgames.com/itb.html)
- [Nintendo: Triangle Strategy tactical tips](https://www.nintendo.com/au/news-and-articles/ten-tactical-tips-for-triangle-strategy-tm/)
- [Fire Emblem Wiki: Combat forecast](https://fireemblemwiki.org/wiki/Combat_forecast)
- [13 Sentinels Wiki: Analysis](https://13-sentinels-aegis-rim.fandom.com/wiki/Analysis)

### UI/设计观察

- [Interface In Game: Into the Breach](https://interfaceingame.com/games/into-the-breach/)
- [Game Developer: Into the Breach UI design](https://www.gamedeveloper.com/design/-i-into-the-breach-i-dev-on-ui-design-sacrifice-cool-ideas-for-the-sake-of-clarity-every-time-)
- [Atomic Bob-Omb: Into the Breach enemy intentions](https://atomicbobomb.home.blog/2020/05/17/into-the-breach-enemy-intentions/)
- [Inverse: 13 Sentinels Aegis Rim review](https://www.inverse.com/gaming/13-sentinels-aegis-rim-review)
- [RPGamer: 13 Sentinels Aegis Rim review](https://rpgamer.com/review/13-sentinels-aegis-rim-review-2/)

### 中文玩家/媒体反馈

- [Steam《超级机器人大战30》繁中好评](https://steamcommunity.com/app/898750/positivereviews/?browsefilter=toprated&l=tchinese)
- [Steam《超级机器人大战30》简中差评](https://steamcommunity.com/app/898750/negativereviews/?browsefilter=toprated&l=schinese)
- [Bilibili UCG《超级机器人大战Y》体验报告＆访谈](https://www.bilibili.com/opus/1097515335568850978)
- [旅法师营地《超级机器人大战Y》测评](https://www.iyingdi.com/tz/post/5625342)
- [游民星空《超级机器人大战30》评测](https://www.gamersky.com/review/202111/1436730.shtml?tag=wap)
- [PC Gamer: Why Super Robot Wars 30 is a big deal](https://www.pcgamer.com/why-super-robot-wars-30-is-a-big-deal-for-strategy-rpg-fans-worldwide/)
- [The Verge: Super Robot Wars Y impressions](https://www.theverge.com/games/773191/super-robot-wars-y-impressions-demo-nintendo-switch-2)
- [机核《钢岚》测试报告](https://www.gcores.com/articles/160778)
- [机核《SD高达激斗同盟》个人游玩感想](https://www.gcores.com/articles/193609)

### 技术方案

- [Phaser Tilemap API](https://docs.phaser.io/api-documentation/class/tilemaps-tilemap)
- [Phaser Animations](https://docs.phaser.io/phaser/concepts/animations)
- [Phaser Camera](https://docs.phaser.io/api-documentation/class/cameras-scene2d-camera)
- [Phaser Camera Shake](https://docs.phaser.io/api-documentation/class/cameras-scene2d-effects-shake)
- [Phaser Audio](https://docs.phaser.io/phaser/concepts/audio)
- [Phaser Shader GameObject](https://docs.phaser.io/phaser/concepts/gameobjects/shader)
- [Tiled Documentation](https://doc.mapeditor.org/)
- [Tiled Custom Properties](https://doc.mapeditor.org/en/stable/manual/custom-properties/)
- [Aseprite CLI](https://www.aseprite.org/cli/)
- [Aseprite Sprite Sheet](https://www.aseprite.org/docs/sprite-sheet/)
- [Spine Phaser Runtime](https://esotericsoftware.com/spine-phaser)
- [PixiJS Spritesheet](https://pixijs.download/dev/docs/assets.Spritesheet.html)
- [Godot 2D Sprite Animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html)

## 9. 下一步工作

不建议继续在当前 demo 上“补按钮”和“调颜色”。下一步应该做一次 demo 重构：

1. 写 `demo/chapter1/docs/vertical-slice-acceptance.md`，把本报告拆成验收项。
2. 在规则层加入 forecast、weapon、spirit、morale、support、enemy intent。
3. 在渲染层加入 Phaser HUD 组件、command menu、forecast overlay、phase banner。
4. 建立占位 sprite atlas，不再用纯色方块。
5. 做一个普通攻击和一个必杀 cut-in，先做到有节奏、有音效、有 shake。
6. 用 Playwright/Browser 截图验证第一屏、选中单位、攻击预测、战斗演出、敌方阶段。

验收口径：用户打开后，不需要解释，也能在 30 秒内看出这是一个“机器人战棋游戏 demo”，而不是互动网页。
