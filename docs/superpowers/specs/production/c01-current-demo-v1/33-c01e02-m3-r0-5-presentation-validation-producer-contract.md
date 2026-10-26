# C01E02 M3-R0.5｜角色 UI 与共同结算演出验证制作人合同

> 日期：2026-08-18
>
> 状态：`active / user playtest direction confirmed / R1 paused`
>
> 性质：`Candidate development presentation slice`
>
> 不是：完整 E02、R1、R2、R3 最终表现、默认 Demo、正式 Runtime 或 Canon 晋升

## 1. 用户试玩裁决与迁移原因

M3-R0 已证明共开意图、路线／朝向／动作编辑、可返回摘要、长按提交、同前态结算和确定性回执可以运行。用户实际试玩后的结论是：

> “主要现在没有角色 UI 和演出，游戏过程比较枯燥无味。”

这不是单纯美术缺口，而是当前灰盒不足以让用户判断共同回合是否好玩：

- 角色不在场，数值和规则没有变成人的判断、担心与行动；
- 公开意图和提交摘要仍像开发表单，没有危险层级与视觉期待；
- 共同结算主要是状态替换，没有车辆通过、小体突入、巨体碰撞、炮击与红光蓄能的时间性；
- `RoundReceipt`、hash 和 Candidate 调试语言占据玩家主界面，行动没有情绪回报。

因此，31 号合同中“R1 后才进入 R3 表现”的顺序在用户试玩后被局部修正：**R1 暂停，先插入 R0.5 最小代表性表现验证**。R0.5 不生产完整 R3 资产，只让同一个已验证单回合达到可判断角色、节奏和爽感的程度。

## 2. 冻结输入

| 输入 | SHA-256 | 用途 |
| --- | --- | --- |
| `31-c01e02-m3-common-turn-inplace-migration-producer-contract.md` | `06d17169f8002a09617a8acb2a92886495ad8dbe524cfca237f9079159050860` | 玩法、故事结果与迁移边界 |
| `32-c01e02-m3-r0-single-round-sandbox-objective.md` | `c7f4cd589d04d4bcc398a02a4e8c113a12d4227ca9cedac9efda7bd64157a350` | R0 实现与证据合同 |
| `main-m3-r0/04-completion-report.md` | `7a7baeb946efb59b616117d80af6cbe888b1fcfbe545e1eba970b42000e0cea6` | 用户试玩基线 |
| `C01-闭馆以后万机出击.md` | `c9a9aa490badea3d2de937e0003b80547974fed27103b31ec9181cd3583cfc8b` | 已验收 E02 角色与行动事实 |
| `C01-用户创作验收回执.md` | `3d11387d92120cfdeeb0069a2a7cdfbe677ed0ea2ac5ae6649038de7b0cd532b` | 故事用户验收证据 |
| `shared_round_resolver.gd` | `09de5610d7896abe4c516f98b91e5c7427e5a54d51dd3039e14588e95a6a8386` | 冻结的共同结算因果 |
| `sandbox_profile.json` | `f62a8be16d1aec0da3986bdee20d94366190b7ae428c78a1d20ecdc1fc3d4f2e` | 冻结的单轮前态与验收方案 |
| `producer-a4/a4-user-approval-receipt.tsv` | `dc402de8ee471953fa1de8b98676aa76a9826a2b219dc6010ba7e762f128781b` | 已批准 MAP-B 来源 |
| `producer-a5/a5-user-approval-receipt.tsv` | `45c1687c3fdbdd87d7f9e872933b48925871f680eeaa0095d360623ad1a34f75` | 已批准小体四向来源 |
| `cutin_doudeng_c01_observe_v01.png` | `b8530e98b9d76edb9275680488558167ad368697fe6f55a3af00ac5492196d3a` | 已批准兜灯观察 Cut-in，只可经 R0.5 精确重绑复用 |
| `cutin_doudeng_c01_tense_v01.png` | `c846e48b04b7d8671fd4853330487d0f39d1df98a70550d1f03d49770a26f159` | 已批准兜灯紧张 Cut-in，只可经 R0.5 精确重绑复用 |

R0.5 不改 `shared_round_resolver.gd`、`sandbox_profile.json` 和三个验收草案的结算结果。若表现需要改变同前态、事件顺序、位置、行动合法性或回执，必须停下重开玩法裁决，不得用演出“顺便修规则”。

### 2.1 显示投影裁决

R0 `sandbox_profile.json` 中的 `tile_half=[30,15]` 只作原灰盒显示参数；A4 MAP-B、M2 profile 和既有正式地图槽使用 `isometric_tile_half_40x20`。R0.5 显示层锁定：

```text
logical_grid=32x18
resolver_coordinates=unchanged_integer_cells
visual_projection=isometric_tile_half_40x20
topology_sha256=baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8
```

主程序用独立 `PresentationGridTransform` 把 resolver 整数格投影到 40×20 显示空间，通过 `Camera2D.zoom` 和视口裁切调整构图，不改 resolver/profile 中的位置、footprint、寻路或接触。A6/A7 按 40×20 投影制作 720p 评审合成。

## 3. R0.5 运行身份

```text
presentation_contract_id=C01E02M3R05
presentation_contract_revision=1
build_id=C01CDV1-M3-R0.5-PRES
rules_profile_id=c01cdv1_e02_shared_round_m3_r0
presentation_profile_id=c01cdv1_e02_m3_r05_presentation_v1
runtime_lane=candidate_development_presentation
entry_role=non_default
save_mode=disabled
story_checkpoint_write=false
operation_commit=false
default_demo_unchanged=true
```

R0.5 可新增一个非默认场景，R0 原场景作机器对照基线只读保留。R0.5 通过后，R1 才能决定是否吸收其表现架构；不维护两套长期 Demo。

## 4. 本轮唯一产品目标

让用户在同一个单回合内同时感到：

1. **这些人在作判断**：纪存、旧守护者、兜灯和七海有明确的信息位置、个性和当下风险；
2. **危险在逼近**：车辆、小体、BREAKER、城市炮火和路面在同一时间线上可读；
3. **我的计划被演出了**：路线、朝向、主动作／预备反应真正改变镜头、受力、台词和可见结果；
4. **结尾有悬念**：首次冲撞偏轴、城市炮命中侧甲，BREAKER 开始聚集红光，旧守护者的视线望向墙上重盾后停止。这只是表现提示，不生成取盾路线／意图，不修改 `shield_state=wall_hung_3_scorches`。

首次试玩目标 4–7 分钟；熟悉后重玩 2–4 分钟。一次结算演出目标 15–25 秒，不用长视频代替棋盘中的真实移动与状态变化。

## 5. 生产 DAG

```text
P0 制作人冻结联合接口（本合同 + 34）
 |
 +--> M0 主程序零资产表现壳（35） --------+
 |                                                   |
 +--> A6 角色通讯 UI 美术（36） --------------+--> U1 用户美术逐项批准
 |                                                   |
 +--> A7 共同结算演出资产（37） --------+
                                                     |
                                                     v
P1 制作人 exact handoff + 冻结绑定
 |
 v
M1 主程序真实接入 + Full/Skip/回退验证
 |
 v
U2 用户联合试玩
 |
 +--> 通过：重开 R1 设计与任务书
 +--> 修订：只返回失败的表现车道
 +--> 不通过：重审共同回合产品方向
```

M0、A6、A7 写入目录互斥，允许并行。M0 不得在 U1/P1 前探测美术目录；A6/A7 不得写 Godot。P1 的精确哈希交接和 M1 真实接入未在本合同自动授权。

## 6. 角色与台词边界

- 纪存只提供路线、人员与危险方向，不操纵馆守 Z 四肢；
- 旧守护者是馆守 Z 同一主体，可以在胸前扬声器／导览席 UI 中出现，不画成独立人形 AI；
- 兜灯只从机况与维修角度发言，不替纪存下战术结论；
- 七海是远程通讯，只能撤回本人停机令，不指挥城市炮火、应急车或馆守 Z；
- 主程序不得临时编台词。R0.5 只用 34 号合同登记的已验收 Reader 原句、无文字反应或制作人后续类型化批准的短句。

## 7. 素材权限

- A4 MAP-B 五静态层与 A5 96px 小体已有用户批准与 M2 exact handoff，可作 R0.5 的**待重绑源**；不得直接复活旧 build/fingerprint binding。
- 兜灯 `CUTIN_DOUDENG_C01_OBSERVE_V01` 与 `CUTIN_DOUDENG_C01_TENSE_V01` 已是 `approved_for_runtime`；A6 只验证它们在新通讯布局中的适配，不得重画、裁切覆盖原件或用新文件冒充既有 Stable ID。P1 仍需为 R0.5 作精确跨车道重绑。
- `frozen-assets/` 只是角色／机体身份锚，`runtime_allowed=false`，只允许 A6/A7 派生设计。
- G1/G1.5 的馆守 Z、BREAKER、重盾只有方向级批准，不是 sprite master，不得直接导入。
- 新 A6/A7 资产必须用户逐项批准并由制作人签 exact handoff 后才可加载。
- 禁止从目录自动搜索、用旧 story_first 头像／B3／G1 animatic 隐式回退，也禁止用“已批准风格”代替对具体文件的批准。

## 8. 验收标准

### 8.1 客观门

1. 正常玩家界面不显示 hash、build、`RoundReceipt`、Candidate 调试文字；F3 可打开独立调试层。
2. 1280×720 下规划期地图和可交互目标不被角色对话占位；大型通讯只在暂停战术输入时出现。
3. 纪存、旧守护者、兜灯、七海在首次试玩 30 秒内有清楚的姓名／通讯来源／当下职能。
4. 车辆通过、小体截击、巨体碰撞、城市炮击、红光蓄能按回执五个节拍播放，无单帧跳结果。
5. Full、Skip 和缺资产 fallback 必须得到完全相同的 `round_result_hash` 与世界结果。
6. 两个成功草案在镜头、纪存／兜灯反应、馆守 Z 承力、小体落位和路面破坏上有可见差异；失败草案的警告与结果一致。
7. 无对话重复触发、无单句弹窗连发、无开发术语替代角色反应。

### 8.2 用户门

联合试玩后用户只需回答：

1. 不看帮助是否理解只操作馆守 Z，车辆／城市炮火自主行动；
2. 是否记得至少一名角色以及他／她此刻在担心什么；
3. 执行前是否能预判大致事件顺序，执行时是否仍有惊喜；
4. 两种成功方案是否真的像两种决策；
5. 结束时是否愿意立即重玩另一种解，或继续到取盾。

不得以“美术资产已加载”代替上述用户回答。

## 9. 全局禁止

- 不改 Reader、Canon、玩法因果、单位数量，不提前取盾、赤红冲击、撤离线清空、盾拍或 P1。
- 不改默认入口、`project.godot`、startup、Autoload、存档或 M2 active binding。
- 不建第二套长期 Demo，不进入 R1，不宣称完整 E02 或商业品质通过。
- 不用付费批量生成或 LibTV，不使用未经核验的第三方 IP 音频／视觉资产。
- 各车道不 `git add/commit`，不清理或覆盖其他 Session 的工作树。

## 10. 当前授权与停点

本合同授权：

- 主程序执行 35 号**零真实资产表现壳**；
- 美术并行执行 36 号 A6 与 37 号 A7 Candidate 资产；
- 制作人维护 38 号生产看板和用户验收。

本合同不授权真实资产接入、修改默认 Demo 或进入 R1。A6/A7 交付后必须先停给用户逐项批准；制作人另签 exact handoff 和 M1 目标后才可接入。
