# 141 · 公式台当前停点：进入游戏体验评估与集中修复

2026-09-18。工作区 `/Users/rayz/Documents/超gag机器人大战`，分支 `codex/srw-kernel-sandbox`。
**Candidate / not_canon / runtime_allowed=false / user_visual_acceptance=false。目标尚未完成。**

## 1. 从这里接手

用户已要求主对话结合原始目标重新订清任务，重点关注游戏体验；用户将删除旧 goal 后重新开启。

1. 完整读 [140 唯一目标](140-formula-lab-integrated-visual-production-goal.md)与本文件。
2. 按 140 §6.1 从现存产物进行独立体验评估，形成一份按玩家影响排序的问题清单；评估后直接进入具体修复。当前还没有这次完整体验评估，不把目标修订当成评估完成。
3. [142 GLM 交接](142-formula-lab-astra-handoff.md)用于查 09-15～18 增量；不沿用“只差签名和六项裁决”的完成判断，也不照其指令先催用户填表。
4. 137 按生产合同查，138 按正在评估的公式查具体金标片段；00c 看产品幻想与玩法边界。不要重载旧会话或所有历史报告。

本次只修订目标与接手材料，未改游戏源码、资产、包索引、正式 Reader/Canon/Runtime；未重跑全套测试或重新试玩。原 141 全文已保存为 [_history/141-before-experience-goal-2026-09-18.md](_history/141-before-experience-goal-2026-09-18.md)。历史证据继续有效到其实际覆盖范围。

## 2. 已核到的新进展及证据范围

以下为 09-18 主对话对磁盘代码、JSON、报告与部分原PNG的核查；不是对全部新增帧的逐帧审查，也不是用户验收。

| 项目 | 核到什么 | 仍不能据此宣布什么 |
| --- | --- | --- |
| A 新录制 | `qa/investigation-onsite-20260910/gui-a-manual-v3/` 329 PNG与索引一致；00328为真实成功结果对白，状态为A_RESULT、2/3段、LOW_GAIN_PASS=true；v4另有5帧回源过程 | v3 final字段已回A_INTRO，不能拿它作3/3终态截图；需要某一终态时定向补证，不因此重录全部A |
| B 成功与中止后离开 | success-v1 201帧；activestop-v4 4帧。final均为2/2、result；前者BRACE_PASS/TOOL_LEFT=true，后者仅ABORTED_SAFE=true。已看成功回执与中止结果对白原图 | 成功片末PNG是结果卡，完成状态另来自final；不能混称每一步均有原图。v1/v2各1200帧封顶，不能当完整离开过程；v3仅1帧失败录制 |
| B 未开始 | neverstarted-v1 3帧，00002已到B_RESULT对白，未写成功/中止事实 | final又处B_TEST，不能宣称有最终汇总原帧 |
| 写盘状态 | 上述capture的帧数与PNG数相符，writer pending=0、errors=[] | 只证明记录落盘。GLM所报138源零漂移还须定位对应录后证据；主对话本轮只找到明确的录前文件和较早baseline录后文件，不把会话文字当新核验 |
| 键盘回到来源 | `investigation_lab_shell.gd`已有ROW_SOURCE导航与J回跳；`investigation_config_input_flow_test.gd`已有回源检查 | 事实Widget当前未为SRC焦点实现高亮和自动滚动。代码级缺口已观察，实际玩家影响仍要在新评估中核验 |
| 采集器 | `production_manual_package_capture.gd`已有检查点完整readback与`--max-frames` | 不补造修改前录像中缺失的状态/画面 |
| 测例与换输入 | 七公式现存test/swap报告gate_pass均true，共24档案例；战术报告实际覆盖T0–T3且仍报18项能力缺口 | 不是七公式体验完成、不是T4–T11实现完成。本轮未重新执行这些测试 |
| 引导与生产增量 | A onboarding-v2有四句前言；package browser有“怎么玩”面板；K rebuild-proof有输入、产物和重建说明 | 四句说明未证明解决首玩困惑；改一句台词不计第二实质输入；编辑后完整实玩来自GLM记录，未在本轮重做 |

上述调查QA目录前缀：`artifacts/formulas/production-lab-v1/`。
GLM会话细节在 `qa/investigation-onsite-20260910/gui-a-manual-v3-session-note.md`、`gui-b-routes-session-note.md`。
十包实玩、D/H补全等已有记录应复用；需要更强结论时查所需帧和状态，不把“勿重做”解释成禁止核实或禁止针对缺口复测。

**09-10 的锁屏停点已被后续新增录制越过。** 不再按旧PID70997/session51887续接，不预设今日仍锁屏或仍有同一进程；实际操作时重新确认当前进程、包、窗口及用户占用情况。

## 3. 当前入口：默认列表与隔离变体分开

唯一默认Candidate索引为 [current-packages.json](../../../../../artifacts/formulas/production-lab-v1/current-packages.json)，本轮未改。目录均相对 `artifacts/formulas/production-lab-v1/builds/`：

| 包 | 默认目录 | 承担体验 |
| --- | --- | --- |
| A | package-a-briefing-v1 | 同场前言→调查试验→结果对白 |
| B | package-b-onsite-v2 | 承力/交割试验，成功/中止/未开始各自承接 |
| C | package-c-exploration-actors-v1 | 器材棚走近、观察、问人、路线计划 |
| D | package-d-exploration-actors-v1 | 三空间线索、归档与知识开路 |
| E | package-e-registered-map-v1 | 固定擂台与真实战损结算 |
| F | package-f-registered-map-v1 | 限时穿越、动态阻挡、撤出与失败 |
| G | package-g-environment-v2 | 派遣→器材棚巡访→真实报告 |
| H | package-h-environment-v1 | 派遣→三室观察归档→路线报告 |
| I | package-i-hub-in-room-v1 | 自然返馆、闲聊、安排、同室后果 |
| J | package-j-hub-review-v1 | 试验约束复核、书页标记与现场查看 |

较新隔离入口：

- A `package-a-manual-v1`、`package-a-onboarding-v2`；B `package-b-manual-v1`。
- F `package-f-lookdev-v1`；K战术对抗已审入口 `package-k-tactical-duel-v1`，见原T3主审，不与下条K混名。磁盘另有K战术v2，启用前核它自己的来源与验证范围。
- K编辑重建证明 `package-k-rebuild-proof-v1`，是C内容变体，不是新的战术输入。
- L/T1 `package-l-camera-v1`。

A v2没有进入默认索引。体验评估应核对“用户真正打开的入口”与待测变体，不能看着v2说明去验旧A，也不为追最新直接覆盖默认。隔离变体不计新增实质输入。

统一浏览场景：`game-godot/scenes/formula_lab/formula_lab_package_browser.tscn`；单包场景：`game-godot/scenes/formula_lab/formula_lab_package.tscn`。单包可按各自REBUILD.txt启动/重建；先验证文件存在，再选当前入口，不按名称猜“latest”。

## 4. 首轮体验评估需要回答的实际问题

- **理解与动机**：玩家只知道在测试载荷，还是知道情境、关心对象、自己能作的判断及完成后的回报？新前言与场内真正可做的动作是否一致？帮助面板不能替代场内理解。
- **操作与信息**：当前对象、焦点、合法性、回源和滚动是否看得见？新增键盘回源是否让人不知道选中了哪张事实卡？确认、取消和跨层返回是否自然？
- **玩法与可解性**：F的成功路线尚无本轮新增证明。三次失败只说明所试打法失败；先读行动合同并验证可解性，再判问题在引导、规则、输入或调优，不先归因为“设计如此”。E成功不能替代F成功。
- **后果与回报**：结果卡数字正确之外，玩家是否看懂为什么、看见实体变化和人物回应？下一段是否使用这些后果，还是重新开一张互不相关的表？
- **声画和角色**：人物/机体静态图位移、装置灰盒和结果文字分别能表达什么、缺什么？应按场景修动作、接触、空间、声音与表演，不把这些整体转成“待用户签名”。
- **七公式与连续体验**：按140矩阵覆盖，不只修A/F；已有两输入/两组合是否实质不同、是否各自达到体验要求？叙事与结算不能仅凭被别的包调用便算充分验证。

主评估计划路径 `artifacts/formulas/production-lab-v1/qa/experience-review-20260918/experience-review.md` 尚未产出。不要先填PASS，也不以本文件代替评估。

## 5. 自主工作与待答边界

- 主对话自行负责目标拆解、优先级、普通引导/焦点/反馈/布局/键鼠缺陷、定向测试、实际试玩和复用回写。用户最新指令授权这次目标重订，未自动批准旧重大待答事项。
- T4新对抗核心、T1教练人类段、T5后段取盾来源冲突、WR第二周期具体文本/后果保留裁决边界；只阻塞依赖它们的工作。T5首段护线/导流不依赖取盾顺序，不把所有工作等在问卷前。
- 三图紫机/白青机/靶机的RGB保留透明修复已获准且完成。第四灰炮机`mecha-si.png`与金机`mecha-ye.png`不在这三图许可内；前者实际用于E及F拦机甲，后者用于F拦机乙，不能按旧payload的doll字样换身份。
- 白青Blender母型、分件R1/R2、双人共骨架身份试验均未通过并保持停止；不复用失败资产、不擅自追加姿态/动画/默认替换。
- 新Candidate环境/空间资产Blender制作已获准；单人临时Lab人物试验、T3音效等按140§5原范围执行。正式角色身份、全局风格、核心规则、付费、外发及正式晋升仍需具体方案和确认。
- 保留共享工作树，不add/commit/reset/清理，不改正式Reader、Canon、默认Demo或正式Runtime。模型按140§8.1实际能力/接口及总成本选择；主对话负责判断，不为派工而拆任务。

## 6. 既有成果入口：按问题查，不重做

以下相对 `artifacts/formulas/production-lab-v1/qa/`：

| 成果 | 证据入口及限制 |
| --- | --- |
| HP/E/F第二轮与三张alpha | `tactical-package-capture-v1/review-20260908-hp-motion/ROUND-REVIEW.md`；Full/Skip状态一致，不等于动作/声画/视觉通过 |
| A/B手册显示/鼠标/生产依赖 | `investigation-onsite-20260910/root-review.md`及新增两份session-note；旧Root报告锁屏段为历史，新证据以具体会话为准 |
| T3/K实际对抗与音效 | `tactical-t3-production-20260910/root-review.md`、`tactical-t3-production-20260910/native-audit/skip-fixed-v1-review.md`；原生Full/早K与真实PCM已取证，用户视听未验收 |
| T1/L相机、点选与交接 | `tactical-t1-camera-20260910/root-review.md`；79帧，R1运动已审，R2/R3未采到中间execute；未实现人类控制段 |
| F同源空间与视觉变体 | `tactical-lookdev-20260910/root-review.md`；250帧三轮真实运动及遮挡，最终失败；静态机体姿态/接触/整体美术未过 |
| G/H世界派遣与探索 | `world-route-production-20260909/manual-g-review.md`、`manual-h-and-branches.md`、`g-shed-depth-v2-root-review.md`、`h-environment-root-review.md`；场地行走/知识门已有证据，不是完整队伍和世界多周期 |
| J返馆复核 | `hub-review-production-20260909/j-review-root-review.md`；试验约束与书页变化已证，人物生活动作与声画未过 |
| 金标缺证 | `investigation-onsite-20260910/obradinn-confirmation-source-note.md`；Obra Dinn作者文字不等于确认动画。Y指令菜单、XCOM编队AAR、Banner行军等按140§4.1补对应专帧 |

工具以当前安装为准，历史可用路径：Godot `/Applications/Godot.app/Contents/MacOS/Godot`；Blender `/Applications/Blender.app/Contents/MacOS/Blender`。原生采集使用fresh目录与当前拥有的进程；F8检查点、F9实录、F10排空。旧浮动宿主/keypost位于临时目录，仅在核实存在、代码、用途及窗口归属后选用，不根据142重建脚本的指令盲执行。

下一轮交接只写新增可见改善、实际证据、未通过和下一问题；不要继续把完整历史叠加到本文件。
