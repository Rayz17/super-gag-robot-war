# 142 · 公式台交接：Claude 会话停点 → Astra 接手

> **2026-09-18 接续说明：本文件保留为GLM增量与证据线索，当前目标和停点分别以[140](140-formula-lab-integrated-visual-production-goal.md)、[141](141-formula-lab-fresh-session-handoff.md)为准。** 用户随后明确要求：先实际研究金标视频、操作与机制，再形成统一体验语言；新增七个定稿章节场景包，并允许基于既定美术制作Candidate验证资源，然后据标准评估与打磨。下文“第一件事收集①–⑤回复”“只差两个签名和六项裁决”“十包实玩等于体验收口”及“加四句已修复首玩困惑”均不作为新目标指令或完成依据。已做成果保留，必要缺口定向复测。

> 撰写：2026-09-18。撰写者：Claude（GLM，ZCode 会话）。
> 接手者：Astra（或任何后续 agent）。
> 性质：公式台路线一（打磨至完成）的停点交接。读完本文 + 141 + `completion-audit-2026-09-16.md` 即可零上下文接手。

---

## 一、停点概述

- 分支：`codex/srw-kernel-sandbox`。工作区：`/Users/rayz/Documents/超gag机器人大战`。
- 前一棒：Claude 会话（2026-09-15 ~ 09-18），完成了十包实机测试、A/B 原生录制补全、⑤A 键盘回源落地、采集器加固、编辑→重建→实玩证明、全套决策准备材料。
- **用户已选路线一**（公式台打磨至完成），并亲手试玩了 A 包 v2（package-a-onboarding-v2）。
- 用户反馈（原话）：首玩「基本看不懂需要我干啥」→ 已修复（A 包 v2 加四行引导对白，见 §三）；再看「这个包就是测试一下传送带载荷，没有任何内容」→ **这是对的真实感受**：十包是验证台不是游戏内容，见 §五路线分岔。
- 用户沟通偏好（重要）：**说人话，不要内部术语轰炸**。141 的六项裁决清单用 TAC_T4/WR/导航循环等术语呈现，用户回复「看都看不懂」。后续向用户呈现裁决必须用游戏体验语言举例说明。

---

## 二、六项裁决状态（当前最大阻塞，全部悬置未获回复）

裁决清单全文：`pending-decisions-2026-09-16.md`。**按 141 纪律不得凭沉默推进**。

| # | 裁决 | 选项 | 现状 | 卡什么 |
| --- | --- | --- | --- | --- |
| ① | T4 对抗核心 | A 中性三分赛（含完整合同表，见 candidate-decision.md）/ B 敌方不重复招式（缺计分/复位/装备合同设计稿） | 未答 | **卡 T4 全部实现** |
| ② | T1 教练段 | 做（R1 结算后插不占回合教练走近观察）/ 缓（保持 capability_gap） | 未答 | 不卡其他项 |
| ③ | T5 取盾顺序 | A 新 Reader / B 旧解构 / C 两源并置（推荐；**只卡 T5 后段**，首段护线+导流不依赖此裁决） | 未答 | 不卡 T5 首段 |
| ④ | WR 多周期编写授权 | A 催办 / B 挂起 / C 混合（机制已实现：cycle_limit=2 + chosen/unchosen 双分支 + hold 防罚；缺第二周期文本行。预拟文本行见 wr-multi-cycle-proposal-2026-09-16.md 末尾） | 未答 | 卡 WR 周期 2 内容 |
| ⑤ | 回跳键位 | **A 已落地为 Candidate 默认**（事实卡入导航循环，J=回来源）/ B ← 最近回跳 / C 维持鼠标 | A 默认已实现，用户可改 | 不卡 |
| ⑥ | 手感/规格门签收 | **需用户亲手试玩后签署** | 用户已试玩 A v2 并给出负反馈（见 §四），未签 | 卡 freeze |

**Astra 接手第一件事：向用户收集 ①–⑤ 的一行字回复**（说人话地问，别贴术语清单——参考 §三的翻译范例重新问一遍）。收到后按「落地改动 → 补测试 → 重跑 formula-desk test/swap/freeze」执行。

---

## 三、用户沟通教训（Astra 必读）

1. **说人话**。首次呈现六项裁决时用了 TAC_T4/WR 多周期/导航循环等术语，用户回复「看都看不懂」。正确做法：用用户玩过的包举例，说清每个选项在游戏里意味着什么。
2. **引导层是真实缺口**。A 包 v1 前言只有一句「先把这次的条件讲清楚，再请求开始。」——首次玩家完全不知道自己是谁、要去哪、按什么。已修复（A v2 四行：任务→身份+三步→上手三件事→原收尾）。**其余九包的前言仍是一句或零句，需要复制这个模式**（见 §六 G1）。
3. **用户选了路线一（公式台完成）而非路线二（开始做真游戏内容）**。但用户也说了十包「没有任何内容」——路线一做完后，路线二（用公式搭 C01 真关卡）是自然下一步。

---

## 四、本会话完成清单（全部有磁盘证据，勿重做）

### 实机测试与录制

| 项 | 证据 |
| --- | --- |
| 十包全部真实操作与结果 | 本会话实玩：A 完整闭环 / B 三路线 / C 器材棚 / D 三室知识门 / E 擂台两轮 / F 三轮双打法 / G 派遣到场 / H 全流程 / I Hub 闭环 / J 复核闭环 |
| A/B 原生录制 8 会话 | gui-a-manual-v3（329帧）+ v4（5帧来源回跳）+ gui-b-success-v1（201帧）+ activestop-v1（1200帧）+ v2（1200帧）+ v4（4帧离开选择）+ neverstarted（3帧），录前/录后 138 项来源 SHA256 零漂移 |
| F 双结局证据 | 成功侧=E 擂台目标达成；失败侧=F 限时穿越目标未达成（两次） |

### 代码修复与新增

| 项 | 文件 | 验证 |
| --- | --- | --- |
| ⑤A 事实卡入导航循环，J=回来源 | `investigation_lab_shell.gd`（_rebuild + _handle_manual advance + _page_keys 提示） | 回归 52 项 0 失败（含 source row 可达/J 回跳/世界不变断言） |
| 回归测试新增 source-row 覆盖 | `investigation_config_input_flow_test.gd` | 52 checks 0 failures |
| 采集器检查点 readback 全采样 | `production_manual_package_capture.gd`（needs_clip_readback 加 checkpoint_pending） | 冒烟验证 |
| 采集器帧上限参数化 | 同上（`--max-frames N`，默认仍 1200） | 冒烟验证 |
| 浮动宿主 `/tmp/float_host.gd` | 悬浮置顶窗口，支持后台键投（见 §五） | 多包实玩验证 |

### 文档归档

| 项 | 路径 |
| --- | --- |
| 完成度审计（单文件全景） | `formula-harness-v1/completion-audit-2026-09-16.md` |
| 裁决清单 | `formula-harness-v1/pending-decisions-2026-09-16.md` |
| T5 两源对照 | `formula-harness-v1/t5-order-comparison-2026-09-16.md` |
| WR 多周期提案 | `formula-harness-v1/wr-multi-cycle-proposal-2026-09-16.md` |
| 回跳键位提案 | `qa/investigation-onsite-20260910/source-jump-keyboard-proposal.md` |
| 试玩引导 | `formula-harness-v1/playtest-guide-2026-09-16.md` |
| A/B 会话记录 | `qa/investigation-onsite-20260910/gui-b-routes-session-note.md`（含全部附录） |
| 项目分析报告 | `docs/项目分析报告-2026-09-16.md` |

---

## 五、已定案问题（Astra 勿重做、勿翻案）

| 问题 | 定案 | 定案依据 |
| --- | --- | --- |
| A 包「配置改后结算用旧值」 | **非缺陷**。探针实证：INV_T0/T3 的 ROW_LOAD/ROW_GAIN 循环后提交，_config 保持循环值、结局正确解析（三箱一次→OUT_T0_DIAGNOSTIC）。首玩异常系按键丢失致操作序列错位 | 回归 38→52 检查含此断言 |
| J→J 450ms 吞键 | **OS 层事件丢失**（遮挡瞬态）。核查 formula_lab_input.gd（纯键→动作映射）与 _press_main_commit（无时间门），壳层与输入层均无去抖 | 代码阅读 + 700ms 未复现 |
| F 朴素打法无法通关 | **场景设计如此**：横移仅 2 次×2 格，3 轮需 6 格，差 3 格——成功需推搡借位或组合规则，需研读 TAC_T2 行动合同 | 三次尝试记录 |

**勿重做清单**：十包实玩（全部有结果）、A/B 原生录制（8+3 会话）、机器门实跑、回归测试、五份决策准备文档、浮宿/键投工具验证。

---

## 六、工具与技巧（Astra 必读，血泪换来的）

### 后台实玩三件套

```bash
# 1. 浮动宿主（/tmp/float_host.gd，重 boot 后需重建——内容见本文件 §七）
# 2. 键投二进制（/tmp/keypost，swiftc 编译，源码同目录）
/tmp/keypost <PID> <KEYCODE> [count] [delay_us]
# 3. 窗口级截图
screencapture -o -x -l <WINDOW_ID> /tmp/shot.png
```

- KEYCODE：J=38 K=37 Z=6 F=3 A=0 Tab=48 Esc=53 ←=123 →=124 ↓=125 ↑=126
- 窗口 ID：用 computer-use 的 `list_windows` 查
- **keypost 的 keycode 是 CGEvent 虚拟键码，不受 macOS fn 键模式影响——F8=100/F9=101/F10=109 可靠**

### 输入通道的坑

| 坑 | 原因 | 解法 |
| --- | --- | --- |
| 键盘突然全部失效（CUA 和 keypost 同时死） | 用户切换桌面空间或全屏应用 → 游戏窗口所在 Space 退后台 → macOS 不投递不可见窗口按键 | 悬浮置顶窗口（float_host 已内置）保持游戏在当前 Space 可见 |
| CUA `get_app_state` 报 "raster withheld" | Godot 无 AX 树，仅窗口框元素可交互 | 用 `screencapture -l` 代替；元素定位用 CUA 截图 + 坐标换算 |
| --script 模式 --resolution 失效 | Godot script 模式忽略 resolution 参数 | 窗口会以 640×388 点打开（retina 2× = 1280×776 px 实际渲染），文字仍清晰可读 |

### 采集协议（正式证据）

```bash
# 采集驱动（F8=检查点 F9=12fps实录 F10=排空退出）
/Applications/Godot.app/Contents/MacOS/Godot --path game-godot --script \
  res://tests/formula_lab/production_manual_package_capture.gd -- \
  --package "<包>/flow.json" --out-dir "<fresh目录>" [--max-frames N]
# 录前/录后来源核对：138 项 SHA256（清单见 qa/investigation-onsite-20260910/gui-a-manual-v2-sources-before.json）
```

### formula-desk 门禁

```bash
scripts/formula-desk test --formula FML_X [--preset P]   # 测例门
scripts/formula-desk swap --formula FML_X --preset A --preset B  # 换档门
scripts/formula-desk freeze --formula FML_X              # 冻结门（需四门全过）
```

---

## 七、路线一剩余工作（按优先级）

### 需用户回复才能开工

| 项 | 阻塞 |
| --- | --- |
| T4 对抗核心实现 | ① A/B 未答 |
| WR 周期 2 内容编写 | ④ A/B/C 未答 |
| T1 教练段 | ② 做/缓未答 |
| T5 后段（取盾） | ③ 顺序未答（首段护线+导流不需要） |

### 可自主开工（不需要裁决）

| 项 | 说明 |
| --- | --- |
| G1 其余九包引导层 | 需要 producer 白名单扩展（允许前导叙事段）——结构性改动，建议先做 **浏览器帮助面板方案**（已实现，见 browser_help panel）作为过渡，producer 扩展列为后续 |
| F 成功结局 | 需研读 TAC_T2 行动合同后规划式对局——三次盲试已证明不可行 |
| A/B 手感门签收 | 等用户试玩 + 按模板签 |

### 建议路线一完成定义

formula-desk freeze 对全部公式放行 = 测例门 + 换档门（已✅）+ 手感门（用户签）+ 规格门（用户签，前提：角色/机体规格定案）。当前差的就是**用户的两个签名 + 六项裁决回复**。

---

## 八、禁止事项（141 + 本会话补充）

- 不凭沉默落产品状态机（六项裁决未答不得擅自选边实现）
- 不改已验收 Reader / 不升 Canon / Runtime / Default
- 不重做：十包实玩、A/B 录制、机器门实跑、回归测试、五份决策文档
- 不把六指令 / HP·EN·气力·HIT% / 战斗舞台 写进公式台（OG 对照 §四禁止搬清单）
- 不在用户窗口可能被遮挡时盲点鼠标（先截图确认可见性）
- 向用户汇报用说人话的格式（§三教训）
