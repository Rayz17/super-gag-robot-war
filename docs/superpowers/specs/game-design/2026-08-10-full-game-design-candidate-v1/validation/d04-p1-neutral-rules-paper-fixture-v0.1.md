# D04-P1《断桥撤离》中性规则纸面 Fixture v0.1

> Status: `candidate_paper_fixture / zero_build / zero_target_players / no_prototype_authorization / no_gameplay_acceptance`
>
> Scope: 为 `D04-P1-A/B/C/D` 四种 Scheduler 提供同一份可实现的世界初态、动作结果、目标、AI Doctrine 与未知信息预算；各版保留原生命令语法和最小 UI。
>
> Canon boundary: 地图、单体、数值、名称和结果全部非 Canon；不映射 C01E02 Demo，不写 Reader、Runtime 或正式资产。

## 1. 为什么需要这份 Fixture

先前的 D04 已经定义了玩家动词、敌方 Intent、时制候选和人类测试门，但没有一份可交给规则程序的共用物理初态：质量、推力、稳定、同刻接触、功能损伤和具体单体菜单仍是文字方向。在这些项目没有同一份真值时，A/B/C/D 实际上会比较四套不同游戏，不能称为中立 Scheduler 对照。

本件先锁定一份待程序化和待实测的 **seed rules**。数值不是平衡结论；纸面路线不是已证明的多解；四时制也仍未定案。

## 2. 共用时间与物理核

### 2.1 时间

- 每个 P1-B/C 执行窗为 `8.0s`；四版共同的语义窗和因果日志精度为 `0.5s`。
- 每个身体实例只保存一份真实秒数；P1-A/D 按 [tactical-tempo-equivalence.tsv](../data/tactical-tempo-equivalence.tsv) 的P1-A列映射为同一1/2 Tempo，P1-D不得另造阵营回合AP。
- 一个计划包只含一条路线、一个主动作、一个反应或安全条件。未用时间转为就地观察/稳定，不跨窗累积。
- 规则结算必须完整实现 [tactical-resolution-kernel.tsv](../data/tactical-resolution-kernel.tsv)；动画帧和实体加载顺序不得参与语义。
- A的一轮交替激活、B的一个时间窗、C的一轮交替锁计划、D的双方阵营阶段都只推进一个`8.0s`世界周期；单位提交、阵营切换或反应不能各自额外推进车辆、桥梁、Deadline或观察年龄。
- 精确的开窗快照、commit边界、自主对象微刻度、环境tick、32秒Deadline、Intent冻结、反应过期与存档边界以 [scheduler-clock-adapter-contracts.tsv](../data/scheduler-clock-adapter-contracts.tsv) 为准；四版的28条共同纸面向量见 [d04-p1-adapter-event-vectors.tsv](../data/d04-p1-adapter-event-vectors.tsv)。这些向量尚未成为自动运行证据。

### 2.2 离散身体值

P1 不使用命中率、随机暴击或隐藏浮动。只使用以下可预览整数带：

| 字段 | 范围 | 作用 |
| --- | ---: | --- |
| `mass_band` | 1-4 | 阻止被推移，也参与撞击冲量 |
| `force_band` | 0-4 | 一个具名动作的主导力 |
| `momentum_band` | 0-2 | 根据接触前实际速度得到：停止 0、普通移动 1、具名冲刺 2 |
| `stability_band` | 0-2 | 失稳 0、移动/普通姿态 1、站稳 2 |
| `support_band` | 0-2 | 无支撑 0、有效地面/工具 1、已提交 Brace/具名承力 2 |
| `protection_band` | 0-3 | 指定方向的护甲、护盾、掩体或功能隔离 |
| `system_state` | 0-2 | 失效 0、降级 1、正常 2；只关闭具名动词，不抽部位 |

### 2.3 位移差值

每个同刻接触 component 按方向合并：

```text
displacement_margin =
  force_band + momentum_band + source_support + valid_helper_support
  - target_mass_band - target_stability_band - target_support_band
```

- 同一领动动作最多获得两个已经到位、方向正确、接口合法的协力，每个 `+1`。
- 反向力在同一 component 内先抵消；求解使用同一 pre-state，不先算我方或敌方。

| margin | 位移后态 |
| ---: | --- |
| `<= -2` | 目标保持；力源失去 1 级稳定或停在最后安全点 |
| `-1..0` | 互相顶住；不位移，双方各记 1 应力；累计 2 应力时稳定 -1 |
| `1` | 目标沿净力移 1 格，稳定 -1 |
| `2` | 目标移最多 2 格；遇阻时剩余位移转为应力 |
| `>= 3` | 目标移到 3 格内最后安全点并失稳；只有动作已声明 `system/structure` 时才另算功能差值 |

友军未宣告接力的路径重叠会让双方停在最后安全点；不用一个隐藏优先级让任一方穿过另一方。

### 2.4 功能效果差值

```text
effect_margin =
  penetration_band + force_band + relative_motion_band
  - protection_band - cover_band - system_guard_band
```

| margin | P1 非致死后态 |
| ---: | --- |
| `<= 0` | 不降级功能；位移、压制或目标进度仍可发生 |
| `1` | 已声明、已暴露的一个功能 `2 -> 1` |
| `2` | 该功能 `2 -> 1` 且稳定 -1，或已降级功能 `1 -> 0` |
| `>= 3` | 最多两个事先声明的后态；P1 禁止一击删除主体 |

同刻维修不能消除同刻新伤；只能处理事前已经测量并声明的功能。

## 3. 14×10 中性地图

坐标为 `(x,y)`，`x=1..14`，`y=1..10`。没有列入可行走集的格为建筑/实心阻挡。

| 对象 | 坐标 / 规则 |
| --- | --- |
| 主路 | `(1..14,5)` |
| 侧路 | `(1..14,8)` |
| 连接道 | `(3,5..8)`、`(7,5..8)`、`(11,5..8)` |
| 断桥危险格 | `(6..9,5)`；同一时刻车辆可通行，但会累积桥应力 |
| 两个支撑点 | `(6,6)` 和 `(9,6)`；与主路相邻，可用 `TACT_BRACE` / `TACT_FIELD_REPAIR` |
| 侧路闸门 | `(7,8)`；初态 closed，工程机使用 `TACT_INTERACT 4s` 开启 |
| 闸门机械端 | `(6,9)`；从 `(6,8)` 相邻操作 |
| 样本箱 | `(8,6)`；可由 Hunter 从主路或中连接道接近 |
| 撤离边界 | `(14,5)` 与 `(14,8)` |
| 初始可见性 | 全地图物理可见；敌方 Intent 按具名行为显示，不测信息战 |

车辆在玩家每窗指定的已开通路线上以 `1格/2s` 自主行驶，遇占位、未处理压制区或已声明安全条件时停车；不额外占用玩家可控单体。

### 3.1 桥梁应力

- 初态 `bridge_stress=0`，`4` 为降级，`6` 为崩塌。
- 每个 8s 窗结束时，若危险格上有任意车辆或机体，`+1`。
- Breaker 在危险格上完成一次 `INT_ADVANCE_OBJECTIVE` 的推进接触，`+2`。
- 支撑点上有完成的 `TACT_BRACE` 时，本窗增量 `-2` 但不低于 0；有效的 `TACT_FIELD_REPAIR` 可一次性将已有应力 `-1`。
- `bridge_stress>=4` 时主路车速降为 `1格/3s`；`>=6` 时危险格不可通行并生成 Secondary 失败，但只要仍有两辆车的合法侧路继续态，不立即 Game Over。

## 4. 初始实体与菜单

### 4.1 我方三台匿名测试机

| ID | 初始格 / 占位 | 身体带 | 路线速度 | 主动菜单 | 反应 / 限制 |
| --- | --- | --- | --- | --- | --- |
| `ALLY-ANCHOR` | `(3,5)+(4,5)`，1×2，向东 | mass 3；stability 1；protection 2；integrity 2 | `1格/2.5s` | `ROUTE`、`BRACE 2s`、`PUSH_TOW 4s/force 2`、`COVER 2s` | 可预留 `CATCH`；旋转需扫过格全部为空 |
| `ALLY-SKIRMISHER` | `(4,8)`，1×1，向东 | mass 1；stability 1；protection 1；integrity 2 | `1格/1.5s` | `ROUTE`、`RANGED 2s/force 1`、`SUPPRESS 4s`、`WAIT_CONDITION` | 可预留 `EVADE` 或 `INTERCEPT`；弹药 3 单位 |
| `ALLY-ENGINEER` | `(5,8)`，1×1，向东 | mass 2；stability 1；protection 1；integrity 2 | `1格/2s` | `ROUTE`、`INTERACT 4s`、`FIELD_REPAIR 6s`、`RESCUE 4s`、`PUSH_TOW 6s/force 1` | 可预留 `ABORT`；本场工具耐用 2 次 |

所有我方功能初态为 2。任一功能降为 1 时，UI 必须显示具体失去的路线速度、动作带或反应弧；不用一个模糊的“受伤”图标。

### 4.2 撤离车辆

| ID | 初始格 | 初始路线 | 信息 |
| --- | --- | --- | --- |
| `EVAC-1` | `(1,5)` | 主路 | 完整；可在 `(3,5)` 转入侧路 |
| `EVAC-2` | `(2,5)` | 主路 | 完整；与 EVAC-1 自动保留 1 格安全距离 |
| `EVAC-3` | `(1,8)` | 侧路 | 闸门未开时会在 `(6,8)` 停车 |

### 4.3 敌方

| ID | 初始格 / 占位 | 身体带 | 初始 Intent | 反制边界 |
| --- | --- | --- | --- | --- |
| `EN-BREAKER-1` | `(11,5)+(12,5)`，1×2，向西 | mass 3；force 3；stability 1；protection 2；`1格/2s` | `INT_ADVANCE_OBJECTIVE`：穿过断桥拦截 EVAC-1/2 | 路线被完全封闭才可改走中连接道；不读玩家新路线 |
| `EN-BREAKER-2` | `(11,7)+(11,8)`，1×2，向西 | 同上 | `INT_ADVANCE_OBJECTIVE`：攻击侧路闸门并拦截 EVAC-3 | 会被开门时机、占位和诱导改变接触点 |
| `EN-HUNTER-1` | `(9,8)`，1×1 | mass 1；force 2；stability 1；protection 1；`1格/1.5s` | 若样本箱可达则 `INT_EXTRACT_SAMPLE`，否则 `INT_HUNT_ISOLATED` | 只能根据实际视线/路线选目标；诱饵、保护链和占位可改变目标 |
| `EN-SUPPRESS-1` | `(11,6)`，1×1 | mass 1；stability 1；protection 1；弹药 3 | `INT_SUPPRESS_ROUTE`：主路东端 4 格走廊 | 友军进射线时必须 ABORT；可被遮挡、绕行或迫使转向 |
| `EN-SUPPRESS-2` | `(12,8)`，1×1 | 同上 | `INT_SUPPRESS_ROUTE`：侧路闸门东端 | 同上 |

### 4.4 P1 局部动作参数覆盖

本表把 [基础动作合同](../data/tactical-action-contracts.tsv) 在本 Fixture 中所有可用动作收窄为一个确定版本。未列动作不可在 P1 出现；表中值覆盖基础合同的候选区间，但不升级为全游戏数值。

| 动作 / 使用者 | 本 Fixture 的固定参数 | 结果与限制 |
| --- | --- | --- |
| `TACT_ROUTE` / 全体 | 只走四方向；每格时间使用实体表速度；1×1 原地转向 `0.5s`；1×2 转向 `2s` 且扫过格全空 | 路线与动作可串在同一 8s 计划内；未到作用点则主动作不发生，停在最后安全点 |
| `TACT_BRACE` / Anchor | `2s`，选择一个方向或相邻支撑点 | 完成后 `stability=2`、该方向 `support=2`，直到移动、失稳或支撑点损坏 |
| `TACT_PUSH_TOW` / Anchor、Engineer、Breaker | 分别 `4s/force2`、`6s/force1`、`4s/force3` | 必须接触、声明方向和终点；按位移差值结算；Engineer/Anchor 不能隔格拖带 |
| `TACT_COVER` / Anchor | 预留 `2s`，威胁接触前能到相邻合法格 | 生成新接触轨迹；来不及则不触发，不能直接删除伤害 |
| `TACT_CATCH` / Anchor | 预留 `2s`，承接弧为正面及两侧相邻格 | 将跌落/撞击接入 Anchor 的同刻接触 component；超载转为双方应力 |
| `TACT_RANGED` / Skirmisher | `2s`，直线视距 5 格，`force1 / penetration1`，弹药 `-1` | 必须声明 `control` 或一个已暴露功能；建筑格完全阻挡，不使用部分掩体或命中抽签 |
| `TACT_SUPPRESS` / Skirmisher、Suppressor | `4s`，选择连续 4 格直线走廊，`penetration1`，弹药 `-1` | 每个主体每窗首次进入时以 `relative_motion=1` 结算一次 `control` 效果；已在区内且不移动不重复受击；友军将进入则按预置 ABORT 停火 |
| `TACT_WAIT_CONDITION` / Skirmisher | 指定公开可观测条件和最晚 `0.5s` 刻度 | 条件未发生时剩余时间只转观察/稳定，不能免费改成另一动作 |
| `TACT_INTERCEPT` / Skirmisher | 预留 `2s`，3 格直线弧，`force1 / penetration1` | 只对提交时声明的轨迹类别触发；触发即失去本窗未完成主动作 |
| `TACT_EVADE` / Skirmisher | 预留 `2s`，一个四方向相邻安全格 | 从触发时刻真实移动；目标格不再安全则在当前格制动并失去主动作 |
| `TACT_INTERACT` / Engineer、Hunter | 都为 `4s` 且作用期间静止 | Engineer 从 `(6,8)` 开闸；Hunter 与样本箱相邻时建立保管链；同刻开门/损坏按 kernel 合并为 `damaged_unsafe` |
| `TACT_FIELD_REPAIR` / Engineer | `6s`，工具耐用 `-1` | 从支撑点处理事前已知桥应力时 `-1`；或把一个事前已测量功能 `1→2`；不能处理本窗同刻新伤 |
| `TACT_RESCUE` / Engineer | `4s`，工具耐用 `-1` | 将一辆已停住车辆稳定并移入一个相邻安全格；不能直接送到撤离边界 |
| `TACT_ABORT` / Engineer、Suppressor | 预置条件触发后 `1s` 制动，再走完当前半格到最近安全格边界 | 取消未完成主动作并保留已付资源；没有安全格则停在上一安全点并记应力 |
| `TACT_MELEE` / Breaker、Hunter | 分别 `4s force3 penetration1`、`2s force2 penetration1` | 必须先接触；Breaker 优先声明 `control/structure`，Hunter 优先声明 `control/system`；功能不明时只能推移/压制 |
| `TACT_WITHDRAW` / Hunter | 使用自身路线速度走向最近已公开东侧边界 | 只有已经取得样本保管链后才携物撤离；被拦截不瞬移丢失或转交样本 |

P1 不使用半掩体，建筑格完全挡线；未声明其他值时 `cover_band=0`、`system_guard_band=0`。各实体功能初态如下，所有列出的功能均为 `2`：Anchor=`mobility/anchor/manipulator/protection`，Skirmisher=`mobility/weapon/sensor/reaction`，Engineer=`mobility/tool/manipulator/sensor`，Breaker=`mobility/ram/manipulator`，Hunter=`mobility/extractor/weapon/sensor`，Suppressor=`mobility/weapon/sensor`。功能降级必须关闭或减弱表中对应动词，不能只减一条通用 HP。

### 4.5 敌方确定性计划器

敌方每窗只读取上一窗结束时自己的合法观察快照，并在玩家提交前公开最终 Intent、目标、路线和可能作用时刻：

1. `EN-BREAKER-1` 固定先阻断距离东侧出口最近的主路车辆；其主路完全不可达时才走中连接道。`EN-BREAKER-2` 在闸门未安全开启时以闸门为目标，否则转向 `EVAC-3`。
2. `EN-HUNTER-1` 在样本仍可达且尚未取得时固定使用 `INT_EXTRACT_SAMPLE`；取得后使用 `TACT_WITHDRAW`；样本不可达时才按“目标到最近两名友军的路径距离之和最大”选择孤立者。
3. 两台 Suppressor 固定覆盖表中各自 4 格走廊；走廊失去任何目标价值时才移动到同一路线下一处公开射位。
4. 最短路线并列时使用本 Fixture 的固定路线变体：Breaker-1=`RV_MAIN_WEST`、Breaker-2=`RV_SIDE_WEST`、Hunter=`RV_SAMPLE_VIA_C7`、Suppressor-1=`RV_MAIN_EAST_POST`、Suppressor-2=`RV_SIDE_EAST_POST`；镜像测试同时镜像这些路线，不使用阵营、容器或加载顺序。目标仍并列时使用界面已公开的目标 ID 次序。
5. 路线耗尽后只执行剩余时间容纳得下的主动作；否则在最后安全点稳定。所有 contingency 都必须来自 [敌方 Intent 合同](../data/enemy-intent-contracts.tsv)，不得执行窗中临时读玩家新计划。

## 5. 目标、敌人和桥的固定规则

### 5.1 目标

- `Primary / OBJ_EVACUATE`：在第 4 个 8s 执行窗结束前，至少 2/3 车辆离开 `(14,5)` 或 `(14,8)`。
- `Secondary-A / OBJ_PROTECT`：`bridge_stress < 6`。
- `Secondary-B / OBJ_INTERCEPT`（本地标签 `DENY_EXTRACTION`）：样本箱未由 Hunter 从东侧边界带走。
- 局部结果分开提交：不允许用 2/3 撤离成功自动覆盖桥断或样本丢失。
- 第 4 窗结束时少于两辆车撤离为 `retry_required`；桥断或样本丢失只分别产生 Secondary `forward_failure`。若三台我方均失去路线/交互功能，或地图已不存在两辆车的任何合法撤离路径，可提前进入同一稳定重试边界。

### 5.2 敌方承诺

- 每个 8s 窗开始时，敌方根据自身上一观察快照选择一个 Intent，公开高信息预览后才与我方同时锁定。
- 只有该 Intent 合同里已声明的 contingency 可在执行窗内触发；没有可观测理由不得转目标。
- 射击机的友军 ABORT 与玩家的友军误伤规则相同；敌我不使用两套物理。

## 6. 两类预计可行解（不是已验证结论）

### S1 正面承力＋主路护送

1. `ALLY-ANCHOR` 在断桥西端占位，用 `BRACE` 对消桥增量并接住 Breaker-1；
2. `ALLY-SKIRMISHER` 在东端压制机与 Hunter 之间做诱导，保留 `EVADE`，不追求击破；
3. `ALLY-ENGINEER` 使用第二支撑点降桥应力，再护送 EVAC-1/2 穿过；
4. 代价：侧路 EVAC-3 可能留置，样本箱也需另外分配一次拦截。

### S2 开侧路＋分流诱导

1. `ALLY-ENGINEER` 首窗优先从 `(6,8)` 开启闸门；EVAC-3 与一辆从 `(3,5)` 转入的主路车改走侧路；
2. `ALLY-SKIRMISHER` 在中连接道迫使 Hunter 暴露或消耗反应，以 `SUPPRESS` 限制 Breaker-2 的转向；
3. `ALLY-ANCHOR` 只阻挡 Breaker-1 进入桥面，不承担所有撤离；
4. 代价：工程机在开门期间不能修桥，侧路受两台敌人的时序压力更大。

S1/S2 只是为实现者提供“这个 Fixture 为什么可能有多解”的起点。必须用相同初态跑搜索/纸模并由目标玩家独立发现才能记为有效方案；如果只能按上述顺序过关，Fixture 失败而不是“教程成功”。

## 7. A/B/C/D 的中立比较边界

| 版本 | 锁定方式 | 共用真值 |
| --- | --- | --- |
| P1-A | 敌我交替激活；每台 2 Tempo，可预留 1 Tempo 反应 | 同一地图、单体、动作真实秒数、效果差值、Intent、目标和桥应力 |
| P1-B | 全部单体安排 8s 计划后同步执行 | 同上 |
| P1-C | 双方交替锁定一台单体的 8s 计划，窗末一次执行 | 同上 |
| P1-D | 我方阵营阶段内自由选择未行动单位，每台2 Tempo；再进入读取同一观察快照的敌方阶段 | 同上；镜像自动门额外检查整队先手偏差 |

四版共享世界快照、动作结果、目标、AI 与未知信息预算，详见 [time-system-neutrality-contract.tsv](../data/time-system-neutrality-contract.tsv)。禁止因 A/D 较容易教学就给更弱敌人，或因 B/C 有时间轴就提供更完整预测。各版可以使用原生命令语法和最小 UI，但教程都受 `8分钟 / 12引导输入 / 2上下文提示 / 0策略提示` 上限；UI 差异必须记录为自变量。

实现顺序固定为共享核冻结后 `D → A → C → B`，不是排名。冷测只显示 `TS-HARBOR / TS-EMBER / TS-LANTERN / TS-QUARTZ` 匿名Build标签，主指标阈值分类冻结前不向测试者和首轮分析者揭示映射。P1只能淘汰或形成shortlist，不得输出单一胜者。

## 8. Scheduler 中立的最小操作状态机

下列八步是共同语义，不是要求四版复制 WEGO 的全队草拟／时间轴 UI：

1. 进入本 Scheduler 的合法决策点，查看身体功能、当前可用动词和已经公开的敌方 Intent；
2. 选择当前可合法指挥的单体，画路线、终点朝向和安全停点；
3. 选择一个主动作，指定对象、方向、作用点与 `control/system/structure` 目的；只有 B/C 用时间轴摆放，A/D 用 Tempo 与当前激活／阵营阶段表达；
4. 可选地从同一身体预算预留一个反应，指定可观测触发、弧区、安全后态和冲突优先级；
5. 查看确认事实的精确结果和未知项的最好—最差结果带；四版信息内容相同，呈现壳可原生；
6. 在本 Scheduler 的原生 commit 边界确认：A 提交当前激活，B 提交全队草案，C 锁定当前单体计划，D 提交当前己方阶段动作；
7. 只检查该 commit 边界已经可知的占位、时间、资源、友军火线、反应槽和目标冲突；A/D 不得被迫先做一份可返回修改的全队草案，B/C 也不得少做其原生冲突检查；
8. 在本 Scheduler 的执行点应用动作并生成因果日志；玩家可点任一后态查看“来源→命令→触发→接触→变化”。

A/D 的已提交动作、C 的已锁计划和 B 的已提交全队草案都不能无代价倒带；未越过各自 commit 边界的内容才可修改。P1 的第一个可用性 Build 必须让键鼠和手柄都能完成本版八步语义循环；不允许用调试键、控制台、主持人代点，或把 B 的时间轴／全队提交伪装成四版共同操作来完成核心动词。

## 9. 必须先自动证明、再进人测的事

- 同一初态、计划与随机加载顺序运行 1000 次，`post_resolve_state_hash` 一致；
- 地图镜像+计划镜像产生镜像结果，不存在未说明的先后手偏差；
- 路径换边、大单体旋转扫格、双方同刻接触、反应来不及、同刻开门/损坏和同刻维修/新伤都有固定 Fixture；
- 计划中的已知结果和实际结果相同；未知情形的实际结果不越出提交前显示的结果带；
- Full/Skip 演出、不同帧率与存档重载不改变规则结果；
- 两类预计解在内部搜索或人工纸模中都能达成 Primary，但只有目标玩家独立使用才计入 `S-DIVERSITY`。

### 9.1 数值校准方法

1. 每次只冻结一个 `fixture_version + kernel_version`；先用深度 4 窗的有界计划搜索验证 Primary 可达，只有 `post_resolve_state_hash` 完全相同的节点才能合并，不能用启发式提前删掉另一策略族。
2. Seed 门要求至少两个第一窗动作集合不同、路线/承力职责不同的方案族能完成 Primary；Primary 不能在 3 窗前无代价完成；Primary+Secondary-A 与 Primary+Secondary-B 必须各自可达，但不强制同局全清。
3. 搜索找不到两族时，按 `地图距离/时限 → 敌方承诺 → 动作时间 → force/protection → 桥阈值` 的顺序，一版只改一个参数家族并记录前后版本、失效方案与新支配策略；禁止同时改地图、数值和 AI 后宣称已校准。
4. 自动门通过后才使用真人数据。前 18 个冷启 Session 不以 50% 胜率调参；按误读、不可预见、执行错误、风险选择、支配策略分别编码失败。只有跨至少 6 个有效 Session 重复出现同类问题，或触发 D10 报警线，才提出下一参数版。
5. 任何参数改动都重跑确定性、镜像、Forecast、两方案可达和存档/演出等价；旧真人证据按 scope 标记失效，不混入新版本统计。

## 10. 仍然未完成

- 没有 Build、程序规则核、实际地图、操作 UI、自动 Fixture 或状态 hash；
- 上述 seed values 没有平衡数据，不得复制到 C01-C03；
- 两类解没有经过搜索、冷启玩家或用户验收；
- 时制、格尺度、单体数量、身体值和 4 窗时限都可能因测试失效；
- 只有用户批准 `DEC-02/DEC-03` 的 Candidate 测试范围后，才可将本 Fixture 实现成原型。
