# 破壳台（breaker-desk）｜C01 Demo 制作组 + 评委会

> 状态：`CANDIDATE_PROCESS / NO_CANON_OR_RUNTIME_PROMOTION`
>
> 日期：`2026-08-27`
>
> 范围：给 C01 Current Demo 一套可重复的制作组与独立评委会。不另起 Demo，不另起 Session，不改已验收 Reader，不升 Runtime / Default / Canon，不宣称视觉验收。

## 1. 这份合同立什么

现网已有产品范围、交互、玩法和体验绑定，也有测例与窗口抽帧。缺的是两层班子：谁锁范围并改现网，谁对**已经交出来的产出**做独立专业评价。

- **制作组**：锁切片、跑机器门、抽本轮窗口实帧、综合评委卡、落一张最小工单。
- **评委会**：评本轮产出（读回、测例、回执、实帧 PNG），不改代码，不给自己打通过。实帧席只看图，不代签用户目视。

LOOK / PLACE / LOCK 是玩家叫法，现网状态仍是 `PUBLIC` / `EDIT` / `SUMMARY`。

语言与手感源（Candidate，不因本文升 Canon）：

- `00c-core-game-design-master-review.md`、`00d-c01-c03-common-system-adaptation.md`
- `134` 体验门与「责任点亮题目，不写解」
- `docs/superpowers/specs/2026-08-26-srw-y-bilibili-full-series-design-notes.md` §8–§9（收层不收皮）

入口：`chao-gag-canon` 先于本 harness。实现与评审协议见 `chao-gag-c01-demo-harness` skill。命令：`scripts/breaker-desk`。旧入口 `scripts/c01-demo-harness.sh` 仍转发到同一套过程。

## 2. 权威分层

冲突时按这次序：

1. Canon Hard / Working
2. 已验收 C01 Reader 与用户创作验收回执
3. `133-c01-e02-gameplay-establishment-contract.md`
4. `134-c01-e02-play-experience-binding-design.md`
5. `132-c01-e02-interaction-establishment-contract.md`
6. `128-c01-full-breaker-operation-demo-product-objective-and-execution-plan.md`
7. `19-current-demo-inplace-rebase-producer-contract.md`
8. History

本文只拥有**过程**：谁评、谁改、何时停、三道完成态怎么记账。不改 133 结算，不改 Reader，不把评委 PASS 写成用户目视。

## 3. 三道完成态

| 完成态 | 谁签 | 含义 |
| --- | --- | --- |
| `machine_pass` | CLI 机器门 | 本切片 headless 测例与 `canon-check-godot --strict` 绿 |
| `jury_consensus` | 本档评委全过或只剩 warn | 内部认为这一刀 Candidate 够格。无实帧时不得对盘面 / 体验门判 `pass` |
| `user_visual_acceptance` | 只有用户 | 134 §14 盖住字只看地图。harness 与 ledger 永远写 `false` |

制作组不能给自己打 `jury_consensus`。`machine_pass` 不能关体验门。自动多轮最多收到 `machine_and_role_code_consensus`，不是「看起来对了」。

## 4. 制作组（动手，不投票）

| 席 | 做什么 | 不做什么 |
| --- | --- | --- |
| 项目经理 | 锁切片与归属层；综合评委卡成一张工单；裁硬停 | 不改代码；不冒充评委；不升格 |
| 机器门 | 跑本切片测例 + canon-check | 不重写「可玩」定义；不把抽帧算进 machine_pass |
| 实帧抽帧 | 窗口跑 E02 capture，写入 `round_NNN/frames/` | 无窗不强跑；不签 `user_visual_acceptance` |
| 主笔 | 只落工单上的一个主切口 | 不兼任评委；不顺手改桥 / E03 / 过场 / 西向馆守 |

默认切片 `e02`。表面顺序仍是 `PROLOGUE → E02 → BRIDGE_A → E03 → BRIDGE_B → E04 → Clear`。第一批自动切片不含 E03 / E04，除非用户口头放开。

工单必须写：归属文件、preserve、至多 3 条 must-fix、不改什么。

## 5. 评委会（投票，不改代码）

不把写作管线 17 席整包搬来。评委出卡前互不看稿。多数票压不过一席有证据的 fail。长文即协议失败。

卡上限：`pass` / `fail` / `warn`、最多 3 条证据、must-fix、preserve、一句 advance。

### 5.1 常设六席（每一自动轮必开）

| 席 id | 席 | 模型 slug |
| --- | --- | --- |
| `gameplay` | 玩法 | `cursor-grok-4.6-xhigh-fast` |
| `interaction` | 交互手感 | `cursor-grok-4.6-xhigh-fast` |
| `first_play` | 冷读玩家 | `cursor-grok-4.6-xhigh-fast` |
| `frames` | 实帧 | `cursor-grok-4.6-xhigh-fast` |
| `engineering` | 程序边界 | `composer-2.5-fast` |
| `producer` | 制作人批次 | `composer-2.5-fast` |

玩法查规则是否成立。冷读查没读说明书的人还懂不懂。两席必须分开。实帧席只评本轮 PNG；无图只许 `warn`。有新实帧时，冷读必须看图，并加开盘面 / 机体席。

### 5.2 加严三席

在要宣称 `jury_consensus`、本轮有新窗口实帧、或用户点名时加开：

| 席 id | 席 | 模型 slug |
| --- | --- | --- |
| `board` | 盘面可读 | `cursor-grok-4.6-xhigh-fast` |
| `spectacle` | 机体奇观 | `cursor-grok-4.6-xhigh-fast` |
| `reader` | Reader 事实 | `composer-2.5-fast` |

无窗口实帧：`board` / `spectacle` 与体验门相关项不得 `pass`，记 `frame_evidence=missing`。日常 E02 战斗轮不开关系席。

Brief：`docs/superpowers/specs/production/c01-current-demo-v1/harness/roles/`。

## 6. 模型纪律

- Grok：手感、冷读、实帧、「还是不是棋」、盘面、机体。不得单独裁定升格或视觉过关。
- Composer：边界清单、批次、Reader 事实、工单收束。不得单独裁定好不好玩。
- 主笔不得兼任任何评委席。同一子代理不得连续评两席。
- 冷读席不得读 134 全文；只给玩家可见表面 + 最多 134 §14 六句。玩法席才许带 133 / 00d。

## 7. 自动多轮

一批最多 **10** 轮。未到第 10 轮、也未撞真硬停，不得收批。用户说「继续」再开下一批。用户要求加严时，评委按量产战棋／机战标准挑刺，可指认才 `pass`。

1. 项目经理锁切片与归属层。
2. 机器门。红则先修回归，修不了硬停。
3. `frames` 抽本轮窗口实帧。有窗必抽；无窗写 `frames.json` missing，不挡机器门。
4. 对本轮已有产出开评委会（常设含实帧席；有 PNG 则冷读看图，并加开盘面 / 机体）。
5. 项目经理写一张工单。
6. 先做换刀检查，再做真硬停检查。过了主笔才改。
7. 再跑机器门。绿了进入下一轮，评的是新产出。

### 7.1 换刀（不是硬停）

同一 must-fix 连续 2 轮落地仍无评委进展：冻结该切口，本批不再落同一刀法。项目经理必须立刻换下一条未用 / 未冻结的 must-fix，继续 `open` 下一轮。

- ledger 记 `same_must_fix_parked`，**不是**整批停
- 禁止把换刀写成 `same_must_fix_no_progress` 后收批
- 禁止再调已被评委否决的色相 / alpha / 标签盖法
- 未到第 10 轮，`open` 必须仍可用

### 7.2 真硬停（整批停）

只有这些才收批：

- 要改已验收 Reader、检查点语义、一次性盾拍
- 要升 Runtime / Default / Canon，或把 `user_visual_acceptance` 翻成 true
- 要本批改 E03 / E04 动词，或把 `1/2` 升回主动词
- 要新开平行 Demo / 第二套 Session / 六指令
- 要 B5 资产峰值或新母版
- 评委权威冲突且项目经理裁不了
- 机器门修不了
- 到达本批第 10 轮

到第 10 轮仍无 `jury_consensus`：记 `batch_round_cap`，等用户口头开下一批。不得在第 5 轮自行收工。

## 8. 机器门（E02）

复用现网，不另写可玩定义：

- `game-godot/tests/c01_breaker_demo/e02_experience_binding_test.gd`
- `game-godot/tests/c01_breaker_demo/e02_gameplay_establishment_test.gd`
- `game-godot/tests/c01_breaker_demo/e02_full_input_controller_test.gd`
- `game-godot/tests/c01_breaker_demo/c01_gf_operation_hud_test.gd`
- `game-godot/tests/c01_breaker_demo/e02_public_rule_family_test.gd`
- `game-godot/tests/c01_breaker_demo/c01_breaker_e02_to_e03_input_integration_test.gd`
- `scripts/canon-check-godot.sh --strict`

窗口抽帧是评委会的图证，不是机器门。入口：`scripts/breaker-desk frames --slice e02 --round-dir PATH`。复用 `e02_gameplay_hud_actual_frame_capture.gd`，禁止 `--headless`。无窗写 missing，不挡 `machine_pass`。manifest 继续写死 `user_visual_acceptance=false`。

## 9. 产物

```text
artifacts/c01_breaker_demo/harness/
  ledger.tsv
  round_NNN/
    brief.md
    machine.json
    frames.json
    frames/*.png
    jury/{gameplay,interaction,first_play,frames,engineering,producer}.md
    jury/strict/{board,spectacle,reader}.md
    ticket.md
    receipt.md
```

`ledger.tsv` 列：`round_id	slice	authority_layer	machine	jury_tier	jury	user_visual	stop_reason`。`user_visual` 只许 `false`。

## 10. 本文明确不做

- 不另起平行 Demo，不把 LOOK / PLACE / LOCK 做成第二套 Session
- 不把评委 PASS 写成用户视觉验收或 Canon 升格
- 不把写作管线 17 席整包塞进每一轮
- 不自动生产 B5 / 新母版 / LibTV 片
- 不把机战 Y 菜单皮写进工单
- 不改已验收 Reader
- 第一批自动切片不含 E03 / E04
- 整章成片、E01/E03/E04、L1 幻想门与美术补完改走 `136-c01-chapter-l6-production-harness.md`（成片台）
