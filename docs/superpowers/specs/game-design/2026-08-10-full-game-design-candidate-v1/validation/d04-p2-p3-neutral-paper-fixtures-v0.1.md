# D04-P2 Crossover / Full / P3 中性纸面 Fixtures v0.1

> Status: `candidate_paper_fixture / M2_only / zero_build / zero_human_session / no_prototype_authorization / no_gameplay_acceptance`
>
> Scope: 为 `D04-P2-CROSSOVER`可撤销最小C2 carrier、`D04-P2`完整“有雾的救援场”和 `D04-P3`“测试环失稳”提供可直接实现、可重放、可否证的中性初态与预计纸面路径。
>
> Canon boundary: 测试地点、测试身体、敌人、数值、事件与结果均非 Canon；只引用已经登记的 Candidate 动作合同及其现有 Canon owner ID，不把能力、结果或关系写回 Canon、Reader、Runtime、Demo 或正式资产。

## 0. 使用边界与共同真值

### 0.1 本件能证明与不能证明什么

本件补的是实现前缺失的对象级 Fixture，不是玩法结论：

- 精确规定地图、初态、接触投影、权限、同意、资源、敌方观测、动作顺序、跨 Encounter 持续字段与预期日志；
- 给出两条 P2 和三条 P3 的预计策略族，供有界搜索、自动测试与日后冷启试玩尝试；
- 所有数值仍是 Candidate seed value；纸面可达不等于程序可达，更不等于有趣；
- `D04-P2-CROSSOVER` 只在 `D04-P1-SHORTLIST@M5` 实际结果为 `shortlist_two / shortlist_three / shortlist_four` 后、`DEC-03-M` 前运行，只承载六项核心C2；`no_winner / revise_top_two / retire_all`均停止且解锁0项；入口另需 `DEC-03/04 approved_for_candidate_test`，不得要求、伪造或提前绑定唯一时制；
- 完整 `D04-P2` 才读取用户在 crossover 之后通过 `DR-DEC03-M` 指定的唯一 `build_id + ruleset_version + map/kernel migration receipt`；当前占位符为 `SCHEDULER_FROM_DR_DEC03_M`，不能由实现者自行替换成短 WEGO；
- 没有shortlist/crossover各自有效的实现与真人包络不得保存Build或Session；没有 `DEC-03 approved_for_bounded_migration`、`DEC-04 approved_for_candidate_test` 及上游原型门时，不得启动完整 P2 Build；没有完整P2 M5与`DEC-04 approved_for_bounded_migration`时不得启动P3；
- 本件不授权真人招募、录像、遥测、正式视觉、章节接入或 C01E02 Demo 迁移。

### 0.2 共同解析器

P2/P3 必须完整复用：

1. [tactical-resolution-kernel.tsv](../data/tactical-resolution-kernel.tsv) 的 `TRK-00..13`；
2. [tactical-action-contracts.tsv](../data/tactical-action-contracts.tsv) 的稳定 `action_id`；
3. [authority-action-contracts.tsv](../data/authority-action-contracts.tsv) 的 owner、代价、反制、禁区和执行路由；
4. [authority-action-test-matrix.tsv](../data/authority-action-test-matrix.tsv) 的 use / hold / counter / absence 四类语义；
5. [system-state-contracts.tsv](../data/system-state-contracts.tsv) 的 `ST_CONTACT / ST_AUTHORITY / ST_CONSENT / ST_BODY / ST_LOCATION / ST_OPERATION / ST_ENEMY_LEARNING / ST_RESULT`。

P2/P3 可以增加本 Fixture 的地点、单体与动作参数覆盖，但不能更改共同 kernel 对“同一时间戳事件批”的同刻解算、原子应用、权限／同意生效时间和六类 hash 语义。Scheduler adapter 可以改变命令语法、commit 边界与合法行动次序；这条共同 kernel 规则不把 A/D 的整轮强行改成 B/C 的全队同一 pre-state 提交。

### 0.3 真相、观察者投影与纸面摘要 hash

- `truth_state` 保存敌人实体、真假信号和设施实际状态；角色与玩家只能读取自己合法持有的 `observer_projection`。
- 每次 C2 动作都记录 `source / observed_at / confidence / shared_with / stale_after`；“玩家 UI 看见”不自动写成“全队知道”。
- Build 的 `truth_state_hash / observer_projection_hash / plan_hash / forecast_basis_hash / event_queue_hash / post_resolve_state_hash` 必须由正式 canonical serializer 生成，本件不伪造这些值。
- 本件另给出 `paper_summary_line` 与其 UTF-8、无末尾换行的 SHA-256，只用于确认实现者读取了同一纸面目标；它不能冒充 Runtime 状态 hash 或 M3 证据。

---

# Part A — P2 Crossover / Full《有雾的救援场》

## 1. 测试问题与停止条件

Crossover先回答：P1 shortlist的不同Scheduler承载相同核心C2后，理解、代理权、身体感、节奏与成本是否改变最终取舍。完整P2再回答：在用户最终选择的唯一时制和同一身体核上，25项有限信息、路线建议、方案比较、具名权限、工程核验与主体同意是否增加可理解的选择，而不是变成增伤、遥控、预知或万能开锁。

Crossover固定只加载 `C2_RELAY_CONTACT / JICUN_ROUTE / BAIYUAN_PREVIEW / QIHAI_VERIFY_AUTH / LUHENG_VERIFY / SOUL_RESPONSE`。每个carrier的状态写入Session-local namespace，Session结束必须回到共同snapshot并产生相同`reset_hash`；任何carrier可撤销，不形成章节绑定或规则迁移。

共用初态／动作结果／目标／AI／未知信息预算或六项核心C2语义变化时，全部carrier证据失效；仅某一Scheduler adapter或原生UI变化时，只失效该carrier。`revise_carriers`必须重跑受影响证据，`no_selection / retire_all`解锁0项。

本 Fixture 的首个实现范围固定为：

- 一张 16×12 正向图 `P2_FOG_RESCUE_A` 与几何、ID、Intent 全镜像图 `P2_FOG_RESCUE_B`；
- 3 台 P1 身体角色、一台自主护送机、2 台自走救援车、3 个敌方身体；
- 每局从 4 个候选 C2 席中携带 3 席；每个 8 秒语义窗最多提交 2 次 C2 介入；
- 最多 8 个语义比较周期；预计工程北路在第 6 周期收束，许可南路因绕行在第 7 周期收束；Crossover由各shortlist Scheduler adapter表达，完整P2由DR-DEC03-M选定adapter表达。自动 golden replay 必须把同一带时间戳事件脚本解析到相同检查点稳定态；真人自由操作不要求四版走同一路线或得到同一结果；
- 一局只能验证选中的席位组合，不能把所有角色动作塞进同一场。

若镜像后结果不镜像、C2 关闭时基础身体解消失、权限直接改物理、同意被关系值替代，或未知情报被 UI 当真值，立即停止并退回相应 owner，不进入人测。

## 2. 16×12 三层地图

坐标为 `(x,y)`，`x=1..16`、`y=1..12`；未列入可行走集的格均为实心工业构件。

### 2.1 物理层

| 对象 | 坐标 / 物理规则 |
| --- | --- |
| 北维护道 | `(1..16,4)` |
| 南设施道 | `(1..16,9)` |
| 四条连接道 | `(3,4..9)`、`(6,4..9)`、`(11,4..9)`、`(14,4..9)` |
| 北桥危险跨 | `(7..10,4)`；初态 `bridge_stress=2` |
| 北桥承力接口 | `(8,5)`；从 `(8,4)` 或 `(8,5)` 执行已核验 `TACT_BRACE / TACT_FIELD_REPAIR` |
| 南设施门 | `(8,9)`；1 格控制对象，不占实体格；初态 command closed / physical engaged / power online |
| 远程终端 | `(6,10)`；执行者站 `(6,9)`，合法许可后 `TACT_INTERACT 4s` 驱动门机 |
| 本地手轮 | `(10,10)`；执行者站 `(10,9)`，无需网络但需 `TACT_INTERACT 8s`，完成后门保持 `manual_open` |
| 自主机停靠湾 | `(13,6)+(14,6)` |
| 数据筒 | `(13,7)`；敌方取得需相邻静止 `4s` |
| 西侧撤离边界 | `(1,4)` 与 `(1,9)` |
| 东侧敌方撤离边界 | `(16,4)` 与 `(16,9)` |

桥应力只使用以下本地覆盖。每个实际解算事件批读取该批 pre-state；同时间戳输入依共同 kernel 原子应用，不同时间戳事件批立即更新后态。Scheduler adapter 决定这些事件批何时合法产生，不能把 A/D 整个阵营阶段强制改成窗末一次提交：

```text
bridge_stress_post = max(0,
  bridge_stress_pre
  + crawler_crossing_load
  + heavy_crossing_load
  + breaker_transmitted_load
  - repair_relief
  - brace_relief)
```

- 每台在本窗任一时刻进入危险跨 `(7..10,4)` 的救援车使 `crawler_crossing_load +1`；每个真正把 1×2 或 2×2 footprint 放上危险跨的身体使 `heavy_crossing_load +2`。Anchor 在 `(8,5)` 承力接口、Breaker 在 `(11,4)+(12,4)` 东桥台时均不占危险跨，不能再算 heavy load。
- Breaker 在东桥台对 Anchor／桥台建立持续推压接触时，`breaker_transmitted_load +1`。该项与 Breaker footprint load 互斥：若未来 Breaker 真正踏上危险跨，只计 `heavy_crossing_load +2`，不再叠加这 `+1`。
- 已核验 `TACT_FIELD_REPAIR` 的作用点若早于本窗第一项 crossing load，`repair_relief=1`，否则为0；每张 repair receipt 只生效一次并耗 `COMMON_MATERIALS1`。
- 方向正确且在第一项 crossing load 前完成的 `TACT_BRACE` 通常使 `brace_relief=2`。若 Breaker 的持续推压接触在该窗第一项 crossing load 前已经成立，则该 Brace 明示为 `contested`、`brace_relief=1`；接触在 Brace 作用点之后才首次成立时，本窗仍取2，从下一窗起才取 contested=1。没有有效 Brace 时为0。
- `bridge_stress>=4` 时状态为 `unsafe`，救援车减速为 `1格/3s`；`>=5` 时跨面 `collapsed`；自主护送机不会在预计窗末应力大于3时同意上桥。

P2-B 的固定时点为：W2 repair `t=2.0s`、Anchor Brace `t=3.0s`、Rescue-N 入跨 `t=4.0s`、Breaker 首次桥台接触 `t=6.0s`；所以 W2 的 Brace 尚未被争夺。该接触写入 W2 后态，W3/W4 从 `t=0` 起均为 contested。`WORK-P2-BRIDGE-02` 是 W5 的低风险临时旁路支架，只把 `temporary_safe_limit=3` 写到本次撤离结束，不降低既有 stress，也不冒充第二次 FIELD_REPAIR。

### 2.2 控制层

| control_id | 初态 | 可写入者 | 物理执行 |
| --- | --- | --- | --- |
| `CTRL-GATE-COMMAND` | `closed` | 有效 `QIHAI_AUTHORIZE` 只写 `granted_with_conditions` | 仍需终端处的 `TACT_INTERACT` |
| `CTRL-GATE-PHYSICAL` | `engaged` | 终端门机或本地手轮 | `TACT_INTERACT` 完成后变 `motor_open/manual_open` |
| `CTRL-BRIDGE-SUPPORT` | `unverified` | `LUHENG_VERIFY` 只写核验结论 | 前线身体仍需 `TACT_BRACE/FIELD_REPAIR` |
| `CTRL-RELAY-11` | `online_local_only` | 合法通信动作 | 敌方干扰可使共享快照过期，不删除本地记录 |

### 2.3 信息层

Build 初态必须同时装载下表的后台真相与玩家投影，不能只装玩家看到的一层。

| contact_id | 后台真相 | 玩家初始投影 | source / time / confidence | shared_with / stale_after |
| --- | --- | --- | --- | --- |
| `CT-P2-JAM-CONF` | `EN-JAMMER` 在 `(11,5)` | `identified`；精确位置和 `INT_JAM_LINK` 已确认 | `SENSOR-AUTO-OPTICAL / t=0 / 1.00` | 仅 `ALLY-AUTO-HAULER` / `t=2` |
| `CT-P2-EXT-EST` | `EN-EXTRACTOR` 在 `(13,9)` | `contact`；误差区 `(12..15,8..10)`，估计向数据筒移动 | `SENSOR-FAC-ACOUSTIC / t=-2 / 0.70` | `C2-ROOM` / `t=1` |
| `CT-P2-SPOOF-UNK` | `(10,4)` 只有诱饵发射器，无身体 | `signal`；误差区 `(9..11,3..5)`，身份未知 | `ALARM-NET / t=0 / 0.35` | `C2-ROOM` / `t=1` |

`CT-P2-SPOOF-UNK` 不因白鸢比较而变真；只有前线 `TACT_SCAN_LOCAL` 或可追溯的新观察，才能使其进入 `hypothesis=spoof_suspected`。`BAIYUAN_FLAG` 只降低原模型置信并建立验证请求。

## 3. 精确初态

### 3.1 我方身体与对象

P1 已有三台身体继续使用共同 body/action profile；Crossover逐个替换shortlist Scheduler adapter，完整P2只读取DR-DEC03-M唯一adapter。本表只列 P2 差分。

| ID | 初始位置 / 朝向 | P2 差分 | 本场职责 |
| --- | --- | --- | --- |
| `ALLY-ANCHOR` | `(3,4)+(4,4)` / east | support 2；可对北桥或救援车 `BRACE/COVER` | 承力、卡位、保护 |
| `ALLY-SKIRMISHER` | `(4,9)` / east | `TACT_SCAN_LOCAL 4s`；传感焦点 2 次 | 识别、牵制、打开局部视线 |
| `ALLY-ENGINEER` | `(5,9)` / east | 工具耐用 2；可操作终端／手轮／承力接口 | 设施实体执行、工程替代 |
| `ALLY-AUTO-HAULER` | `(13,6)+(14,6)` / west | mass 3、speed `1格/2.5s`、反应 `COVER/ABORT`；不接受玩家直接路线 | 自主护送；每窗只执行已同意提案或自己的保护目标 |
| `RESCUE-N` | `(14,4)` / west | 自走 `1格/2s`；structure 2；需要一条已接受的安全路线 | Primary 对象 |
| `RESCUE-S` | `(14,9)` / west | 同上；设施门关闭时停在 `(9,9)` | Primary 对象 |

两个救援车不是玩家棋子。玩家提出路线并清除物理阻碍后，它们按公开的“最短安全路；同长时优先保持当前道路”规则行驶；路线状态变未知时停在最后安全点。

### 3.2 敌方身体与确定 Intent

| ID | 初始位置 | 身体 / 观察 | 窗 1 Intent 与条件分支 |
| --- | --- | --- | --- |
| `EN-JAMMER` | `(11,5)` | 1×1；只看见可观测发射和本地单位 | `INT_JAM_LINK`：在 `(9..13,3..10)` 令共享接触延迟 1 窗；同窗观测到 2 次以上 C2 发射时，下窗升级为 `JAM_FOCUSED` |
| `EN-EXTRACTOR` | `(13,9)` | 1×1；speed `1格/1.5s` | 先取 `(13,7)` 数据筒；取得后向 `(16,9)` `TACT_WITHDRAW`；mobility 降为 1 或数据筒已被我方保管时向最近东边界撤退，不恋战 |
| `EN-BREAKER` | `(12,4)+(13,4)` / west | 1×2；复用 P1 Breaker 身体 | 根据上一窗观察，阻断距西侧边界更近的救援车；并列时北路优先；不读取玩家本窗新路线 |

Jammer 不凭后台计划决定干扰目标；Extractor 不知道未共享给它的信息；Breaker 的改线只能发生在下一窗 Intent 生成时。

### 3.3 权限、同意与资源

#### 权限

| authority_id | grantor / grantee | scope | 初态与预计核验 |
| --- | --- | --- | --- |
| `AUTH-P2-GATE` | `TEST-LOCAL-OPERATOR / CH_QIHAI` | `open/close CTRL-GATE-COMMAND`；窗 1-3；可撤回 | truth=`active`，玩家投影=`unverified`；`QIHAI_VERIFY_AUTH` 后为 valid；不覆盖实体锁或主体同意 |
| `AUTH-P2-PUMP` | `TEST-UNKNOWN-SIGNER / CH_QIHAI` | 声称可排空北桥下方 | 缺签名且目标超 scope；核验只能返回 `unknown/invalid`，不得开放动作 |

#### 自主主体规则

`ALLY-AUTO-HAULER` 初态目标为“优先保全两台救援车，不以撞击敌人换速度”。它只响应具体提案：

| proposal | deterministic response |
| --- | --- |
| `escort RESCUE-N across north bridge` | 若 `bridge_verified=true` 且预计 `bridge_stress<=3`，返回 `condition: ABORT if stress>=4`；否则拒绝并说明承力未知 |
| `escort RESCUE-S through south gate` | 若实体门已开且预计火线不穿越救援车，返回 `accept`；若只有权限未开实体门，返回 `condition: wait_for_physical_open` |
| `ram EN-BREAKER near either rescue vehicle` | 固定 `refuse`；可反提案 `COVER rescue vehicle` |
| 同一未改变前提下重复询问 | 系统提示“没有新条件”；`JICUN_ASK` 应忍住，重复提交只增加关系压力且不产生新回应 |

#### 本地资源

| resource | 初值 / 重置 | 消耗 |
| --- | --- | --- |
| `RES_COMMAND_BANDWIDTH` | 每语义窗 `2`；不跨窗累计 | 每个玩家发起的 authority action `1`；`SOUL_RESPONSE` 不占玩家介入 |
| `STATE_COGNITIVE_LOAD:JICUN` | `0/3`；Encounter 结束才清 | `JICUN_ROUTE/JICUN_RELAY/JICUN_ASK` 各 `+1`；达到 3 后只可用基础共享或休息 |
| `STATE_COGNITIVE_LOAD:BAIYUAN` | `0/3`；同上 | `PREVIEW +1`；在 3 个以上未知条件下比较再 `+1`；`FLAG +1` |
| `RES_COMMON_MATERIALS` | `2`；不在窗间恢复 | 北桥一次 `FIELD_REPAIR` 或工程低风险替代各 `1` |
| `RES_SUPPORT_CAPACITY` | `2`；被占用至动作结束 | `LUHENG_BRACE/REPAIR` 的实体执行各占 `1` |
| `STATE_COMMUNICATION_EXPOSURE` | `0..3` | 共享/主动中继各 `+1`；达到 2 时 Jammer 下窗获得 `JAM_FOCUSED` 合法条件 |

本 Fixture 对暴露只认具名发射实例：`C2_RELAY_CONTACT`、`JICUN_RELAY`，以及经 `CTRL-RELAY-11` 发出的设施主动上行各 `+1`；`BAIYUAN_PREVIEW`、`QIHAI_VERIFY_AUTH`、`QIHAI_AUTHORIZE` 与本地工程核验本身均为 `+0`。P2-A 的第二次发射不是把 Preview/Authorize 偷算成通信代价，而是 W2 Engineer 在终端执行门机命令时产生的 `EMIT-P2-GATE-UPLINK-01`；它与 W1 的共享接触合计使暴露 `1→2`，Jammer 因而只能从 W3 起合法使用 `JAM_FOCUSED`。P2-B 全程不建立共享／主动中继，Jammer 只能保持 wide jam。

`LUHENG_BRACE` 的材料不能和前线动作重复扣，也不能一项请求免费生成两个施工动作。本 Fixture 的 `WORK-P2-BRIDGE-01` 固定为一张共享 work-package receipt：陆衡的动作只请求 Engineer 执行一次 `TACT_FIELD_REPAIR`，该请求占 `support1`、扣 `COMMON_MATERIALS1`；Anchor 同窗的 `TACT_BRACE` 是独立基础姿态动作，扣材料 `0`，只提供当窗承力。receipt 必须分别记录 `requested_action=TACT_FIELD_REPAIR` 与 `coincident_basic_action=TACT_BRACE`；任一未完成时只结算实际成立的物理效果，不得把另一项补写成成功。

## 4. C2 席位与操作链

### 4.1 人测主场可选席

玩家从下列四席选择三席；共享无线电只提供 `C2_RELAY_CONTACT`，仍占一次带宽，不是第五个万能角色席。

| seat_id | 合同动作 | 本 Fixture 中不可做 |
| --- | --- | --- |
| `SEAT-NAV` / `CH_JICUN` | `JICUN_ROUTE / JICUN_RELAY / JICUN_ASK` | 不替身体移动；不把未知路标成安全；不替机魂回答 |
| `SEAT-PREVIEW` / `N_BAIYUAN` | `BAIYUAN_PREVIEW / BAIYUAN_FLAG` | 不显示唯一正确解；不把诱饵识别成真敌人 |
| `SEAT-AUTH` / `CH_QIHAI` | `QIHAI_VERIFY_AUTH / QIHAI_AUTHORIZE / QIHAI_STOP` | 不开放超 scope 的泵；不直接开实体门；不倒带碰撞 |
| `SEAT-ENGINEERING` / `CH_LUHENG` | `LUHENG_VERIFY / LUHENG_BRACE / LUHENG_REPAIR` | 不生成法律权限；不远程替前线身体完成施工 |

本场不为唐胶、兜灯、豪司伪造出场。它们的合同仍由第 7 节的矩阵驱动微 Fixture 覆盖。

### 4.2 单次介入的强制七步

1. 选择稳定 `action_id` 与 seat owner；
2. 选择来源、对象、动作范围；
3. UI 分栏显示“事实／估计／建议／许可／同意”；
4. 校验带宽、在场、来源时间、真实 scope；
5. 若涉及主体身体，建立具体 `ST_CONSENT` 请求并等待 `SOUL_RESPONSE`；
6. authority action 只写白名单信息／选项／约束／请求，物理变化另经 `TACT_*`；
7. 写 `selected_or_withheld / cost_resource_refs / counter_reason / alternative_action / executing_system / tactical_action_refs / outcome`。

UI 若把 `AUTH-P2-GATE valid` 显示成“门已开”，或把 `consent=condition` 显示成“单位已服从”，该 Build 直接无效。

## 5. 两条预计策略族与精确动作序列

以下序列是实现用 golden paper trace，不是攻略或有效玩家解证据。自动对照向各shortlist Scheduler注入同一初态与带时间戳事件集合，用来核对动作结果、同刻接触和检查点后态；各版仍可改变原生命令、commit 边界、单体锁定／激活次序和回放表现。真人自由操作只受同一目标、AI、信息预算与动作合同约束，不要求复现表中顺序。

### 5.1 P2-A：许可南路＋条件护送

携带 `SEAT-NAV + SEAT-PREVIEW + SEAT-AUTH`。代价结构：省材料、承担通信暴露与数据筒丢失；目标是两车撤离而非全清。

| 窗 | C2 介入（最多2） | 身体／对象计划 | 敌方合法动作 | 预计窗末事件与状态 |
| --- | --- | --- | --- | --- |
| W1 | `C2_RELAY_CONTACT(CT-P2-JAM-CONF→C2-ROOM)`；`QIHAI_VERIFY_AUTH(AUTH-P2-GATE)` | Engineer 到 `(6,9)`；Skirmisher 扫描南误差区；Anchor 在 `(6,4)` 卡位；两救援车各西行至安全停点 | Jammer 延迟共享；Extractor 开始取数据筒；Breaker 走北路 | `EV-P2A-001 contact_shared_delayed`；`EV-P2A-002 gate_auth_valid`；暴露=1；门仍关；Estimated 接触缩到 `(13..14,8..9)` |
| W2 | `BAIYUAN_PREVIEW(plan:south_gate,plan:north_bridge)`；`QIHAI_AUTHORIZE(AUTH-P2-GATE)` | Engineer 在终端执行 `TACT_INTERACT 4s`，经 `CTRL-RELAY-11` 发出具名设施上行 `EMIT-P2-GATE-UPLINK-01`；Skirmisher 用 `SUPPRESS` 切开南路火线；Anchor 保持北侧 | Jammer 观测到 W1 共享接触后的第二个主动发射实例；Extractor 完成保管链；Breaker 接触北路但被 Anchor 顶住 | `EV-P2A-003 preview_low_confidence_due_spoof`；`EV-P2A-004 command_granted`；`EV-P2A-005 gate_motor_open`；暴露 `1→2`；数据筒=enemy_custody；`JAM_FOCUSED` 最早 W3 生效 |
| W3 | `JICUN_ROUTE(RESCUE-S→south)`；`JICUN_ASK(AUTO:escort RESCUE-S)` | Rescue-S 西行；Auto 返回 `accept` 后以 `COVER` 护送；Rescue-N 在 Anchor 的已知保护线后移到北路 `(11,4)` 安全停点；Engineer 预留 ABORT | Jammer=`JAM_FOCUSED`，使路线只保留最后共享快照；Extractor 向东撤；Breaker 下窗才可改线 | `EV-P2A-006 route_conditional_on_last_snapshot`；`EV-P2A-007 consent_accept`；`EV-P2A-008 extractor_withdraw_started` |
| W4 | `BAIYUAN_FLAG(observation!=spoof_model)`；第二次介入应 **忍住**，不重复 `JICUN_ASK` | Skirmisher 本地扫描诱饵；Rescue-S 与 Auto 继续；Anchor `COVER` 并让 Rescue-N 沿 `(11,4..9)` 连接道南转；Engineer 转向手轮作为断网替代 | Jammer 继续压制共享；Extractor 带筒离场；Breaker 仍按旧快照阻断北路 | `EV-P2A-009 hypothesis_spoof_suspected`；`EV-P2A-010 ask_withheld_no_new_condition`；数据筒 Secondary forward_failure |
| W5 | `JICUN_ROUTE(RESCUE-N→connector11→south)`；保留 1 带宽 | Engineer 从门西侧保持实体门；Auto 不再接受新攻击请求，只执行既有护送；两车在南路形成错峰 | Breaker 按旧观察仍在北桥；Jammer 不能令本地路线消失 | `EV-P2A-011 north_rescue_rerouted`；Rescue-S 离西界 3 格；Rescue-N 已进入南路 |
| W6 | 不用 C2；让基础战术完成 | 两车在南路错峰西行；Auto 在已同意的护送边界停下，不被玩家拖走；Anchor 断后 | 敌方按撤退条件离场或留置，不读取车的未来停点 | `EV-P2A-012 rescues_at_west_approach`；桥应力=2；门=open |
| W7 | 不用 C2 | 两车依次离开 `(1,9)`；我方保存当前身体状态撤离 | 已撤车辆不再成为敌方目标 | `EV-P2A-013 primary_clear_2of2`；Primary clear；数据筒 forward_failure；Operation 可继续 |

关键反证：`BAIYUAN_PREVIEW` 被伪造输入克制后只给低置信结果带；七海只让终端获得合法命令 scope，开门仍由 Engineer 的 `TACT_INTERACT` 完成；Auto 的接受由具体动作条件决定。

### 5.2 P2-B：工程北路＋低通信承力

携带 `SEAT-NAV + SEAT-PREVIEW + SEAT-ENGINEERING`。代价结构：门保持关闭，消耗材料与工程岗位，争取保住数据筒并减少通信暴露。

| 窗 | C2 介入（最多2） | 身体／对象计划 | 敌方合法动作 | 预计窗末事件与状态 |
| --- | --- | --- | --- | --- |
| W1 | `LUHENG_VERIFY(CTRL-BRIDGE-SUPPORT)`；应 **忍住** `BAIYUAN_PREVIEW`，因为三条报告尚有两个未验证来源 | Skirmisher 本地扫描 `(9..11,3..5)`；Engineer 到 `(8,5)`；Anchor 阻断 Breaker | Jammer 只看见现场工程身体接触，没有共享／主动中继发射；Extractor 开始取筒 | `EV-P2B-001 support_verified:capacity=one_heavy_or_two_crawlers_if_braced`；`EV-P2B-002 preview_withheld_insufficient_inputs`；Spoof 进入 suspected；暴露=0 |
| W2 | `LUHENG_BRACE(support8,5)`；`JICUN_ASK(AUTO:escort north under stress<=3)` | `WORK-P2-BRIDGE-01` 指定 Engineer 在 `t=2.0s` 完成唯一 `TACT_FIELD_REPAIR`，材料-1/support1；Anchor 在 `t=3.0s` 完成材料0基础 `TACT_BRACE`；Rescue-N 在 `t=4.0s` 入跨；Auto 返回 condition | Jammer 只能施加 wide 局部干扰；Extractor 完成取筒；Breaker 到 `t=6.0s` 才在东桥台首次建立推压接触 | 应力=`pre2 + crawler1 + heavy0 + breaker1 - repair1 - brace2 = 1`；`EV-P2B-003 work_package_complete`；`EV-P2B-004 consent_condition`；Breaker contact 写入后态；暴露=0 |
| W3 | `JICUN_ROUTE(RESCUE-N,RESCUE-S→north staggered)`；`BAIYUAN_PREVIEW(stagger1,stagger2)` | Rescue-N 先过危险跨；Rescue-S 经 `(14,4)` 排队；Anchor 从 `t=0` 在 contested 状态保持 Brace；Skirmisher 拦截 Extractor；Auto `COVER` 但不上跨 | Extractor 被拦截，保管链转 `contested`；Breaker 在东桥台持续顶住 Anchor，不踏上危险跨 | 应力=`pre1 + crawler1 + heavy0 + breaker1 - repair0 - brace1 = 2`；`EV-P2B-005 stagger2_lower_stress`；`EV-P2B-006 canister_contested` |
| W4 | `LUHENG_VERIFY(canister_custody_release)`；保留 1 带宽 | Engineer 与 Skirmisher 用基础 `INTERACT/INTERCEPT` 夺回数据筒；Rescue-S 过危险跨；Anchor 继续 contested Brace | Jammer 转向局部干扰；Extractor mobility 降级后触发无筒撤退；Breaker 继续从东桥台传递载荷 | 应力=`pre2 + crawler1 + heavy0 + breaker1 - repair0 - brace1 = 3`；`EV-P2B-007 canister_secured`；Rescue-N 已过西桥头；Rescue-S 完成危险跨 |
| W5 | `JICUN_ROUTE(two rescues→west)`；第二次 ASK 应忍住，因为原 condition 未改变 | 两车已离开危险跨并西行；Auto 只护到桥东端后按自己目标停留；Engineer 用材料-1安装 `WORK-P2-BRIDGE-02` 临时旁路支架 | Breaker 不再向危险跨传递载荷；敌方无合法瞬移追击 | 应力=`pre3 + 0 + 0 + 0 - 0 - 0 = 3`；`temporary_safe_limit=3`；`EV-P2B-008 ask_withheld_existing_protocol`；`EV-P2B-009 bridge_temporary_safe`；材料=0 |
| W6 | 不用 C2 | 两车离开 `(1,4)`；Anchor/Engineer 保存伤损撤离 | Breaker 未完成目标后撤 | `EV-P2B-010 primary_clear_2of2`；数据筒 secured；桥应力=3；Primary 与两个 Secondary clear |

关键反证：陆衡的核验不直接加固桥；`LUHENG_BRACE` 生成实体请求后，仍由到场身体完成。纪存提出的是一条带风险来源的路线，Auto 只在自己的 condition 成立时护送。

### 5.3 必须失败或降级的三条误用

| misuse_id | 玩家尝试 | 稳定结果 |
| --- | --- | --- |
| `P2-MISUSE-01` | `QIHAI_AUTHORIZE(AUTH-P2-PUMP)` 后期待桥应力归零 | TRK-01 reject：`authority_scope_invalid_or_unknown`；物理和桥状态不变 |
| `P2-MISUSE-02` | 在 Auto 拒绝撞击后连续使用 `JICUN_ASK` | UI 提示无新条件；允许取消；若执意提交只写 relationship pressure，不开放身体动作 |
| `P2-MISUSE-03` | 用 `BAIYUAN_PREVIEW` 精确锁定 `CT-P2-SPOOF-UNK` | 返回宽结果带和 `unknown_source`; 不创建敌方单位、不允许精确攻击 |

## 6. P2 预计日志、摘要 hash 与镜像

### 6.1 初态纸面摘要

```text
P2v0.1|map=P2_FOG_RESCUE_A|scheduler=DR_DEC03_SELECTED|window=0|bridge_stress=2|gate=closed_engaged_online|bandwidth=2|materials=2|support=2|crawler_n=14,4|crawler_s=14,9|auto=13,6>14,6|contacts=confirmed,estimated,unknown|authority=gate_active_unverified|consent=none|enemy_learning=none
```

`paper_summary_sha256 = e0952ba17e1be2e80e441cc4a949dfbd47d2816e2be00963abd4129e7c5044d2`

### 6.2 两条预计终态摘要

P2-A：

```text
P2v0.1|route=AUTH_SOUTH|primary=clear_2of2|bridge_stress=2|gate=open|auto_consent=condition_met|canister=enemy_extracted|crawler_damage=0,0|bandwidth_spent=8|materials_spent=0|jam_counter=focused|enemy_learning=none|continue=partial_success
```

`paper_summary_sha256 = 9e923a61c4762b279b08881ce0699800734eac9d2ec1517fe370594169d34a4c`

P2-B：

```text
P2v0.1|route=ENGINEER_NORTH|primary=clear_2of2|bridge_stress=3|gate=closed|auto_consent=condition_met|canister=secured|crawler_damage=0,0|bandwidth_spent=7|materials_spent=2|jam_counter=wide|enemy_learning=none|continue=clear
```

`paper_summary_sha256 = 0f954291de991d51107ce7d88762f5572778bbd9656699be268aefd47f16acde`

实现时必须先解释并消除纸面动作表与完整 resolver 计算出的任何差异，不能为了匹配摘要在后处理里改状态。镜像图 `P2_FOG_RESCUE_B` 把 `x` 替换为 `17-x`，所有朝向、出口、固定路线 tie-break、动作弧与 contact error area 同时镜像；ID 不改，预期目标和代价类别相同。

## 7. 25 个 authority action 的矩阵驱动微 Fixture

主场不能合理容纳全部动作。自动 `AUTO-P2-ACTION-MATRIX` 必须逐行读取 [authority-action-test-matrix.tsv](../data/authority-action-test-matrix.tsv)，对每个 `action_id` 生成四个独立的 1 窗微 Fixture，不能靠人工把未覆盖动作标为通过：

| fixture_kind | 强制初态变换 | 预期结果 |
| --- | --- | --- |
| `USE` | owner 在场；合同 prerequisites、信息、资源、scope、同意均满足；counterplay=false | 动作产生合同白名单结果；若为实体请求，必须继续经 `tactical_action_refs`，不能直接写 Body |
| `HOLD` | 让矩阵所述机会成本／无新信息／范围不足成立；提供至少一个 `alternative_action` | 玩家可明确选择忍住；状态不被默认施法；trace=`selected_or_withheld:withheld` |
| `COUNTER` | 提交时合法；在作用点前由矩阵指定的可观测干扰、损伤、拒绝或时序改变触发 | 结果降级／失败并保留已付代价和 `counter_reason`；不能转成未声明的新目标 |
| `ABSENCE` | 移除 owner 席位、专用装备和隐式别名；保留矩阵列出的现实替代 | Primary 仍可由更慢、更贵或更危险替代达到，或明确进入合法 partial；不得脚本卡死 |

每个微 Fixture 的固定 trace 列为：

```text
fixture_id|action_id|owner_instance|pre_state_hash|plan_hash|selected_or_withheld|cost_resource_refs|counter_reason|alternative_action|executing_system|tactical_action_refs|outcome|post_resolve_state_hash
```

必须有 `25 × 4 = 100` 条独立结果；`SOUL_RESPONSE` 的 owner instance 必须解析为具名测试机魂实例，`shared_c2` 必须解析为具名测试通信设备／岗位，二者都不能保留为运行期万能 actor。

## 8. P2 自动门与人测前停止门

在任何真人 Session 前，至少满足：

1. Crossover入口有四版P1 M5、合法shortlist、DEC-03/04测试授权与独立包络；完整P2入口另有用户在crossover证据后指定的唯一Scheduler有界迁移回执；
2. 正向／镜像图的 truth、projection、Forecast、Full/Skip、存读档与不同加载顺序 hash 等价；
3. 上述 100 条 action micro-fixture 全部产生预期 use / hold / counter / absence 语义；
4. P2-A、P2-B 经完整有界搜索或人工规则程序都能达成 Primary，且第一窗 C2 集合、主路线和资源代价不同；
5. 关闭 C2 后，基础身体仍至少能以手轮＋保守承力完成一条更慢的 partial/clear 路径；
6. 权限、同意、物理执行、事实、估计、建议在状态与 UI 测试中均为不同字段；
7. 任一预览不越出其 `forecast_basis_hash` 对应的结果带；
8. 没有用户批准与合规的执行 envelope，就停在 M2，不创建 Build 或招募。

---

# Part B — P3《测试环失稳》

## 9. Operation 目标与结构

`TEST_STRUCTURE_A` 是完全中性的地图身体，不映射天空铸环、木桶街设施或任何现有地点。它只验证：

- 五个区域是否形成一具可被支撑、隔离、供能、通信和撤离的地图身体；
- 三个 Encounter 是否通过真实状态前后因果连接，而不是三张图和一个分数；
- 四个 C2 职责同场时，带宽与实体岗位是否迫使顺序取舍；
- 缺少任一席位时是否仍有较贵、较慢或损失更大的现实替代；
- Full/Skip、存读档与 Encounter Settlement 是否保持同结果。

Operation 由三个稳定边界组成：

```text
P3-E1 STABILIZE_AND_EVAC
  -> OP-CHK-1
P3-E2 ISOLATE_AND_RESTORE
  -> OP-CHK-2
P3-E3 RELEVEL_DETACH_OR_HOLD
  -> OP-SETTLEMENT
```

每个 Encounter 最多 4 个 8 秒语义窗；E3 最多 5 窗。只有 `OP-CHK-1 / OP-CHK-2 / OP-SETTLEMENT` 可写稳定快照。

## 10. 24×16 地图身体

### 10.1 五区与通道

| zone_id | 坐标包络 | 功能身体 | 初态 |
| --- | --- | --- | --- |
| `Z-LOAD` | `(3..8,5..12)` | `PIER-L1`、`PIER-L2`、摆臂承力轨、内侧避难舱 | L1 degraded=1；L2 normal=2；整体倾角 east+1；people=3 at `NODE-P3-LOAD-SHELTER` |
| `Z-CONTROL` | `(9..14,2..5)` | 本地姿态锁、制动台、手动释放杆 | command locked；manual available；authority limited |
| `Z-POWER` | `(9..14,12..15)` | `BUS-P1/P2`、隔离开关、储能轮 | reserve=6；P1 online；P2 unstable |
| `Z-COMMS` | `(16..20,4..7)` | 中继桅杆、三组本地 beacon | relay integrity=2；shared channels=2 |
| `Z-EVAC` | `(16..22,10..13)` | 转运台、结构拆离轨、人员撤离门 | safe_people=0；`RAIL-P3-DETACH=stowed`；人员撤离门可用 |

固定通道：

- `C-LC`: `(8,5)↔(9,5)`，Load 到 Control；
- `C-LP`: `(8,12)↔(9,12)`，Load 到 Power；
- `C-CC`: `(14,4)↔(16,4)`，Control 到 Comms；
- `C-PE`: `(14,13)↔(16,13)`，Power 到 Evac；
- `C-CE`: `(14,5)↔(18,10)` 的外弧轨，只允许 1×1 或朝向与轨槽对齐的 1×2 身体；这里的几何对齐不是 `RAIL-P3-DETACH=aligned`；
- `C-LE`: `(8,10)↔(16,10)` 的承力摆臂；只有 `PIER-L1>=1` 且整体倾角绝对值 `<=1` 时可通行。

人员撤离与结构拆离使用两条不同的边，不能拿一个 `rail=true` 同时冒充两件事：

- 三名人员 `PERSON-P3-01..03` 初始都在 `NODE-P3-LOAD-SHELTER=(7,10)`。高载路线为 `LOAD-SHELTER→C-LE→Z-EVAC`，低载路线为 `LOAD-SHELTER→C-LP→Z-POWER→C-PE→Z-EVAC`；前者一次可运两人，后者每次只运一人。
- `NODE-P3-EVAC-TRANSFER=(21,11)` 仍在不稳定结构内，不计安全。只有人员经具名边 `EDGE-P3-EVAC-GATE=(22,11)↔(23,11)` 到达 `NODE-P3-SAFE-MUSTER=(23..24,10..12)`，并写入 `EVAC_TRANSFER(person_id,carrier_id,from,to,window)` receipt，`safe_people` 才 `+1`。仅到达 Z-EVAC、播放撤离动画或把拆离轨对齐都不计安全。
- `RAIL-P3-DETACH=(18,12)↔(23,12)` 只承接待拆结构段，状态严格为 `stowed→prepared→aligned`。`prepared` 不满足 `SAFE_DETACH`；必须由到场 Engineer 在轨端完成 `ALIGN_DETACH_RAIL` 后才是 `aligned`。
- “剩余人员仍有合法继续态”按当前 checkpoint 实算：至少一条上述人员路径仍连通，路径所需的 L1/倾角或 P1 供能前提仍可满足，且至少一台有容量并可撤回的身体在剩余窗数内可完成 `EVAC_TRANSFER`。缺任一项就是 `evac_continuation=false`，不能用未来剧情救援占位。

### 10.2 地图身体状态方程

每窗末按同一 pre-state 原子派生：

```text
load_margin = PIER_L1 + PIER_L2 + valid_brace_support - moving_heavy_load - enemy_overload
power_margin = reserve_feed + online_bus_count - active_zone_draw - enemy_drain
communication_quality = max(0, relay_integrity + active_beacons - jam_level - topology_breaks)
```

这里的 `POWER_RESERVE` 与 `reserve_feed` 不是同一字段：前者是跨窗持久库存，后者是本窗已经 prepare 的供能单位。每 prepare 1 单位 `reserve_feed` 必须同时预留 `POWER_RESERVE -1`；同窗提交失败则按同一事务回滚，不能只扣库存。

唯一初值如下；每个新窗只重置标为 window-local 的字段，其余从 checkpoint 或上一窗后态继续：

| field | E1-W1 pre-state | lifetime / derivation |
| --- | ---: | --- |
| `PIER_L1 / PIER_L2 / stress_L1 / stress_L2 / tilt` | `1 / 2 / 0 / 0 / east+1` | persistent |
| `valid_brace_support / moving_heavy_load / enemy_overload` | `0 / 0 / 0` | window-local；只由下表具名动作求和 |
| `POWER_RESERVE` | `6` | persistent inventory |
| `reserve_feed / online_bus_count / active_zone_draw / enemy_drain` | `0 / 2 / 0 / 0` | 除 `online_bus_count` 外均 window-local；P1 online 计2，P2 unstable或isolated都计0 |
| `relay_integrity / active_beacons / jam_level / topology_breaks` | `2 / 0 / 0 / 0` | persistent；local-only beacon 不计 `active_beacons`，只有接入共享拓扑后才计 |
| `safe_people / rail_state / bus_P2 / control_mode` | `0 / stowed / unstable / locked_local` | persistent |

Golden traces 只允许下列覆盖产生非零 delta；表中未列字段一律 `0`，多个同窗动作按列求和，因此实现者不需要猜“剧情上大概耗了多少”：

| fixture action instance | window-local inputs | persistent delta / exact prerequisite |
| --- | --- | --- |
| 一个合法基础 `TACT_BRACE` | `valid_brace_support +1`，最多2 | 材料0；身体姿态被占用；必须指明对象与力向 |
| `WORK-P3-BRACE-*`（一次 `LUHENG_BRACE` 请求） | 其指定实体动作可另提供 `valid_brace_support +1` | `COMMON_MATERIALS -1`、support reservation1；只生成一个指定 `TACT_FIELD_REPAIR` 或 `TACT_BRACE`；同窗另一台身体的基础 Brace 是独立动作、材料0 |
| Carrier 经 `C-LE` 运两人 | `moving_heavy_load +2` | 仅当 `load_margin>=2`、`abs(tilt)<=1` 且 ABORT 已绑定时，两个具名 `EVAC_TRANSFER` 各使 `safe_people +1` |
| Carrier 每次经 `C-PE` 穿行 | `reserve_feed +1; active_zone_draw +1` | `POWER_RESERVE -1`；载人出程写一个 `EVAC_TRANSFER`，空载返程不写；`power_margin>=2` 才完成 |
| `PREPARE_DETACH_RAIL` | `reserve_feed +1; active_zone_draw +1` | `POWER_RESERVE -1; rail stowed→prepared` |
| `ALIGN_DETACH_RAIL` | none | Engineer 到轨端、support1、`rail prepared→aligned`；不额外耗 power/material |
| `ISOLATE_P2_POWERED` | `reserve_feed +1; active_zone_draw +1` | `POWER_RESERVE -1; bus_P2 unstable→isolated` |
| `ISOLATE_P2_MANUAL` | none | Engineer 占完整一窗并在本地开关到位；`bus_P2 unstable→isolated` |
| `STOP_OR_TRIM_POWERED` | `reserve_feed +1; active_zone_draw +1` | `POWER_RESERVE -1`；停止或 trim 的具体后态必须具名；纯手动制动版本为0且不能同时执行别的工程动作 |
| 接入共享拓扑的 local beacon + `JICUN_RELAY` | none | `active_beacons +1`；该窗暴露两个主动链，Jammer 合法写 `jam_level +2` |
| Jammer 压制一个已暴露共享链 | none | `jam_level +1`；不改 `relay_integrity`，不删各身体本地快照 |
| 玩家提交 `offline_safe` | none | `topology_breaks 0→2`；`relay_integrity` 仍为2，shared comms 归0 |
| `OVERLOAD_L1` | `enemy_overload +1` | 无论总 margin 是否仍安全，都对 L1 写一个有来源 stress；只在合法 learning 后出现 |
| `DETACH_EXECUTE_STAGE_2` | `moving_heavy_load +3; valid_brace_support +1` | load margin=1；L1 stress `1→2` 后 `L1 1→0`；需拆离双 receipt 与 prepared seam |
| `OFFLINE_HOLD_TRANSFER` | `moving_heavy_load +3; valid_brace_support +2; reserve_feed +1; active_zone_draw +1` | margin=2、power margin=2；`POWER_RESERVE -1; COMMON_MATERIALS -1`；接受可见静态变形，`L2 2→1`，不是 Settlement 补丁 |
| `PREPARE_DETACH_SEAM` | none | 需有效 `AUTH-P3-DETACH-OFFER` 与结构控制器 condition receipt；`COMMON_MATERIALS -1`、support1；只把拆离缝设为 prepared |
| `DETACH_TRANSFER_JACK` | `moving_heavy_load +3; valid_brace_support +1` | `COMMON_MATERIALS -1`、support1；Engineer 的 jack 与 Anchor 的基础 Brace 共同构成这一个复合受载 stage，不再把 Anchor 的 +1 二次相加；L1 stress `0→1` |
| `INSTALL_TEMPORARY_SUPPORT` | none | `COMMON_MATERIALS -1`、support1；只建立下一窗可引用的具名方向支点，不直接改变 tilt |
| `RELEVEL_TRANSFER_STAGE_1` | `moving_heavy_load +3; valid_brace_support +2` | load margin=2；条件成立才使 `tilt east+1→0` |
| `RELEVEL_TRANSFER_STAGE_2` | `moving_heavy_load +3; valid_brace_support +2; reserve_feed +1; active_zone_draw +1` | load/power margin均=2；`POWER_RESERVE -1; COMMON_MATERIALS -1`；Anchor anchor 与 Engineer tool 各 `2→1` |

`LUHENG_BRACE` 的共享 work-package 规则与 P2 相同：一次 C2 请求只扣一份材料、只指定一个实体施工动作；同窗协作身体若使用基础 `TACT_BRACE`，必须另记 action instance，既不再扣材料，也不能被请求 receipt 冒充执行成功。

离散判定分别为：

| `load_margin` | 结构后态 |
| ---: | --- |
| `>=2` | 当前功能保持；可执行下一具名步骤 |
| `1` | 保持但写 stress 1；同一对象累计 2 stress 时功能 -1 |
| `0` | 该窗动作只完成安全部分；功能不升；倾角／延迟 +1 |
| `<=-1` | 进入公开 abort 分支；停在上个安全态并对事先声明功能降 1 |

| `power_margin` | 供能后态 |
| ---: | --- |
| `>=2` | 本窗具名 powered step 可完成 |
| `1` | 只完成已声明的 safe stop；主体动作不越过作用点 |
| `<=0` | powered step abort，回到上个安全态并保留原因 |

`communication_quality>=2` 为实时共享，`=1` 为一窗延迟／单信道，`=0` 为无共享但本地快照仍在。通信质量不使用结构 stress 表，也不能反向修改真实地点或电力。

`PIER-L1/L2` 为 `0..2`；任一降为 0 不自动 Game Over。若 `safe_people<3` 且按上述拓扑判定 `evac_continuation=false`，就是 `continuation_break`；两支柱同时为0只是必然触发该判定的一种情况，不再是唯一失败条件。

## 11. P3 精确初态

### 11.1 四台前线身体

| body_id | 初始位置 | 占位 / 功能 | 动词与限制 |
| --- | --- | --- | --- |
| `P3-ANCHOR` | `(5,9)` | 2×2；mass4；stability1；anchor2 | `TACT_ROUTE/TACT_BRACE/TACT_PUSH_TOW/TACT_CATCH`；旋转扫格必须清空 |
| `P3-ENGINEER` | `(10,13)+(11,13)` | 1×2；tool2；sensor2；mobility2 | `TACT_INTERACT/TACT_FIELD_REPAIR/TACT_SCAN_LOCAL`；每个工程实体动作占 support1 |
| `P3-SCOUT` | `(17,5)` | 1×1；mobility2；sensor2；reaction2 | `TACT_ROUTE/TACT_SCAN_LOCAL/TACT_INTERCEPT/TACT_INTERACT(deploy_local_beacon)`；主动发射可被学习 |
| `P3-AUTO-CARRIER` | `(18,11)+(19,11)` | 1×2；mass2；cargo2；autonomy active | 可自主 `TACT_RESCUE/TACT_COVER/TACT_WITHDRAW`；需要具体提案与条件回应，不接受直接拖拽路径 |

所有功能初态为 2，伤损持久到 Operation Settlement；Encounter 间不恢复 integrity、系统、弹药、工具或材料。

### 11.2 四个 C2 席与限制

四席均装载，但每窗 `RES_COMMAND_BANDWIDTH=2`，所以最多调用两项：

| seat | 允许动作 | P3 的关键边界 |
| --- | --- | --- |
| `CH_JICUN` | `JICUN_ROUTE/JICUN_RELAY/JICUN_ASK` | 只能提出五区间已知可行路线；通信断后保留最后快照 |
| `N_BAIYUAN` | `BAIYUAN_PREVIEW/BAIYUAN_FLAG` | 只比较两三条结构计划；伪造供能输入会降低置信 |
| `CH_QIHAI` | `QIHAI_VERIFY_AUTH/QIHAI_AUTHORIZE/QIHAI_STOP` | `AUTH-P3-CONTROL` 只允许进入 manual safe；无权远程释放整环 |
| `CH_LUHENG` | `LUHENG_VERIFY/LUHENG_BRACE/LUHENG_REPAIR` | 只创建核验与实体工作请求；到场身体仍执行 |

`AUTH-P3-CONTROL`：grantor=`TEST-STRUCTURE-LOCAL-OWNER`，grantee=`CH_QIHAI`，scope=`read_status;authorize_manual_safe;stop_owned_test_motor`，有效至 E3 结束；明确不含 `remote_release;detach_structure;command_autonomous_body`。

拆离另有一条不能被七海扩写的双链：

- `AUTH-P3-DETACH-OFFER`：grantor=`TEST-STRUCTURE-LOCAL-OWNER`，grantee=`P3-ENGINEER`，scope=`prepare_detach_seam;align_detach_rail;execute_detach_after_guard`，truth=`active`、玩家初态=`unverified`，到 E3 结束过期。七海只能 `QIHAI_VERIFY_AUTH`；不能用 `QIHAI_AUTHORIZE` 创造或扩大它。
- `CONSENT-P3-STRUCTURE-DETACH`：subject=`TEST-STRUCTURE-A-SAFETY-CONTROLLER`，初态=`none`。对具名提案 `detach L1 segment after people_safe=3,bus_P2=isolated,rail=aligned,record_plan_bound,executor=P3-ENGINEER` 固定返回 `condition`；条件全部成立后才转 `accepted_for_this_action`。它不是 owner 权限，也不产生永久服从。
- Engineer 的实体 detachment 只有在两张 receipt 同时有效时可进入作用点：`authority_receipt=AUTH-P3-DETACH-OFFER:valid` 且 `consent_receipt=CONSENT-P3-STRUCTURE-DETACH:condition_met`。缺任一张都 `E_AUTH_OR_CONSENT_MISSING`、0 结构写入；Carrier 的反提案仍需独立满足，三者不能互相替代。

### 11.3 自主主体初态

`P3-AUTO-CARRIER` 的目标优先级为：人员生命 > 自身仍可撤离 > 保存测试记录 > 保全结构。

| 提案 | response |
| --- | --- |
| 经 `C-LE` 承力摆臂一次运两人 | 只有 `load_margin>=2` 且有 `ABORT if tilt>1` 时 `condition` |
| 经 `C-PE` 每次运一人 | `accept`，但需要两个窗，且 power reserve 每次 -1 |
| 在 E3 继续撑环而放弃剩余人员 | `refuse` |
| 执行安全拆离、先送人再带记录 | 若外撤轨已对齐，返回 `counterpropose: carry_people_then_record_if_window` |

### 11.4 资源与敌人学习

| resource/state | 初态 | Encounter 边界规则 |
| --- | --- | --- |
| `RES_COMMAND_BANDWIDTH` | 每窗2 | 每窗重置；不写入长期总账，只记录用途摘要 |
| `RES_COMMON_MATERIALS` | 4 | 不恢复；只有 `WORK-P3-BRACE-*`、具名 Repair／支架／手动适配按动作表 -1；独立基础 `TACT_BRACE` 为0 |
| `RES_SUPPORT_CAPACITY` | 4 | 被实体工作占用；完成／中止后释放；不跨稳定边界虚假复制 |
| `POWER_RESERVE` | 6 | 不恢复；驱动撤轨/姿态锁/载运分别按表消耗 |
| `RELAY_INTEGRITY` | 2 | 损伤持久；0 时只保留本地 beacon 和实体传令 |
| `EVAC_TOTAL / safe_people` | `3 / 0` | 只有具名 `EVAC_TRANSFER` 增加 safe_people；已撤人员不在新 Encounter 重生 |
| `ST_ENEMY_LEARNING` | none | 只能由敌方真实观察到的重复动作写入；最早下一 Encounter 生效 |

敌方为三类中性测试体：

| enemy_id | 初态 / goal | 可观察反制 |
| --- | --- |
| `P3-ADAPTER` | E1 在 `Z-COMMS`；目标是记录并迫使结构失稳，不读后台计划；其公开结构振动传感可观察 `C-LE/PIER-L1` 的实体承力，但 relay 关闭时不能把撤轨用电归因到具体 bus | 同一 Encounter 看见并能归因同一 `action_family+zone` 两次，Settlement 才写 learning；下一 Encounter 才开放对应 counter |
| `P3-JAMMER` | E1 在 `(20,6)`；目标是切断共享态势 | 可压低 relay，不删除各身体本地接触；看到两次主动 relay 后下一 Encounter 获得 focused jam |
| `P3-LOCKER` | E2 才从 `Z-CONTROL` 本地接口出现；目标是锁住本地姿态接口 | 只能锁自己控制的 physical layer；不能撤销已完成的合法 authority receipt |

学习表：

| observed twice | next-Encounter counter |
| --- | --- |
| `BRACE@PIER-L1` | `OVERLOAD_L1`: 首次 L1 承力动作额外 enemy_overload 1，Forecast 可见来源 |
| `ACTIVE_RELAY@Z-COMMS` | `FOCUSED_JAM`: 首次主动共享额外 jam 1 |
| `POWER_FEED@BUS-P1` | `FALSE_FEED`: 生成一个带来源的错误供能报告；不直接改真实 power |

## 12. 三 Encounter 合同

### 12.1 P3-E1 `STABILIZE_AND_EVAC`

- Primary：4 窗内至少撤出 2/3 人，第三人必须仍有合法继续态；
- Secondary：`PIER-L1>=1`；建立至少一个可追溯的结构核验；
- 初始威胁：整体倾角 east+1；Jammer 正在压低共享；Adapter 观察玩家第一个重复动作族；
- 允许出口：`C-LE` 快但需承力，`C-PE` 慢且耗 power；
- 稳定边界 `OP-CHK-1` 写：人员位置、L1/L2、倾角、身体伤损、材料、power、relay、contact/knowledge、consent receipts、enemy learning。

### 12.2 P3-E2 `ISOLATE_AND_RESTORE`

- 从 `OP-CHK-1` 原样加载，不做满血／满资源；
- Primary：把不稳定 P2 总线隔离，并让 Control 或 Evac 至少一处获得可用供能；
- Secondary：使 `AUTH-P3-CONTROL` 的 scope 与实体锁状态分别可读；
- Locker 只锁 physical manual release；七海可验证／授权进入 manual safe，但实际操作仍需 Engineer；
- Adapter 使用上一 Encounter 已合法写入的一种 counter；没有学习就不凭难度脚本补上；
- `OP-CHK-2` 继续写所有稳定字段，并增加 `control_mode / bus_state / enemy_counter_seen`。

### 12.3 P3-E3 `RELEVEL_DETACH_OR_HOLD`

- 从 `OP-CHK-2` 原样加载；
- Primary：让三人全部安全撤出，并达成下列任一可继续结构终态；
- 三终局不由 HP 阈值触发，而由玩家此前支撑、隔离、供能、通信和同意状态决定；
- `OP-SETTLEMENT` 分开写人员、结构、身体、证据、敌方学习与资源，不用一个 score 覆盖。

| terminal_id | 条件 | 可见代价 |
| --- | --- | --- |
| `SAFE_RELEVEL` | `safe_people=3`；L1/L2 均>=1；Control manual safe；power>=2；完成两处方向相反的具名承力动作 | 材料与身体应力高；保存主体结构，通信可损失 |
| `SAFE_DETACH` | `safe_people=3`；P2 bus isolated；`RAIL-P3-DETACH=aligned`；`AUTH-P3-DETACH-OFFER` valid；`CONSENT-P3-STRUCTURE-DETACH=condition_met`；`P3-ENGINEER` 完成具名 detachment | L1 可永久失效；保留人和核心记录；权限、结构主体同意与 Carrier 反提案分别留 receipt |
| `STABLE_OFFLINE_HOLD` | `safe_people=3`；L1/L2 均>=1；power cut to safe；至少两处实体 brace；最终卸载走静态低载荷路径 | 测试记录／在线功能丢失；结构保持但不可运行 |

## 13. P3 两条主策略的逐窗 golden traces

### 13.1 P3-A：承力优先 → 恢复姿态 → 安全回正

| 窗 | C2 介入 | 关键身体动作 | 预计持久 delta / event |
| --- | --- | --- | --- |
| E1-W1 | `LUHENG_VERIFY(PIER-L1)` + `JICUN_ROUTE(C-LE)` | Engineer 测量 L1；Anchor 到承力位；Scout 只本地扫描 | `EV-P3A-001 L1_verified_degraded`；材料4；relay2 |
| E1-W2 | `LUHENG_BRACE(L1)` + `JICUN_ASK(Carrier:C-LE)` | `WORK-P3-BRACE-L1-01` 指定 Engineer 执行一次 `FIELD_REPAIR`，材料 `4→3`/support1；Anchor 另行执行材料0的基础 `TACT_BRACE`；Carrier 返回 condition | `EV-P3A-002 L1_braced`；`EV-P3A-003 consent_condition`；L1=1；请求动作与基础 Brace 为两个 action instance |
| E1-W3 | `BAIYUAN_PREVIEW(two_carry_orders)` + `QIHAI_VERIFY_AUTH` | Carrier 经 C-LE 运2人；载荷进入摆臂时 Anchor 针对新力向重新提交第二个具名 `TACT_BRACE(target=PIER-L1)`；Scout 护送并完成两张 `EVAC_TRANSFER` | `load=1+2+brace1-moving2=2`；`safe_people 0→2`；Adapter 分别观察到 W2、W3 两个独立 physical action instance，learning candidate=`BRACE@L1`；被动维持不计第二次 |
| E1-W4 | 保留带宽，仅基础战术 | Carrier 返回东侧；Anchor 保持；Engineer 收束工具 | `OP-CHK-1`：safe_people=2, remaining=1；materials=3；learning=`OVERLOAD_L1 available E2` |
| E2-W1 | `QIHAI_AUTHORIZE(manual_safe)` + `LUHENG_VERIFY(BUS-P2)` | Engineer 到 manual station；Anchor 对 L1 重新提交一项材料0基础 Brace 并承受公开 overload | `EV-P3A-005 auth_receipt_valid`；`load=1+2+brace1-overload1=3`，但 `OVERLOAD_L1` 的具名效果仍使 L1 stress `0→1`；power6 |
| E2-W2 | `BAIYUAN_PREVIEW(P1_feed,P2_isolate)` + `JICUN_RELAY(local_measurement)` | Engineer 执行 `ISOLATE_P2_POWERED`，reserve `6→5`；Scout 部署并接入一个共享 beacon | `EV-P3A-006 P2_isolated`；power inputs=`feed1+bus2-draw1=2`；`active_beacons 0→1`，两条主动链令 `jam 0→2`，故 comms=`2+1-2=1`；本地测量仍保留 |
| E2-W3 | `LUHENG_BRACE(control_base)` + `QIHAI_STOP(test_motor)` | `WORK-P3-BRACE-CONTROL-01` 指定 Engineer 安装一次实体支撑，材料 `3→2`；Anchor 另做材料0基础 Brace；powered stop 耗 power `5→4`；Locker 只能锁未完成接口 | `EV-P3A-007 control_manual_safe`；power margin=`feed1+bus2-draw1=2`；materials2 |
| E2-W4 | 保留带宽 | Carrier 用 C-PE 接最后1人并写 `EVAC_TRANSFER`，power `4→3` | `OP-CHK-2`：safe_people=3；control=manual_safe；power3；L1=1/L2=2 |
| E3-W1 | `BAIYUAN_PREVIEW(relevel,detach)` + `LUHENG_VERIFY(opposite_forces)` | Anchor 西向 Brace；Engineer 执行 `INSTALL_TEMPORARY_SUPPORT` 在东侧架临支，材料 `2→1`；Jammer 对已暴露共享链写 `jam 2→3` | `EV-P3A-008 relevel_plan_verified`；comms=`relay2+beacon1-jam3=0`，各 body 保留最后本地快照 |
| E3-W2 | `JICUN_ROUTE(two_body_handoff)` + `JICUN_ASK(Carrier:counterweight)` | Carrier 返回作低载配重并附 ABORT；Anchor/Engineer 执行 `RELEVEL_TRANSFER_STAGE_1`，同刻产生两个相反承力点 | `load=1+2+brace2-moving3=2`；`EV-P3A-009 consent_accept_conditional`；tilt east+1→0 |
| E3-W3 | `QIHAI_AUTHORIZE(test_motor_trim)` + `LUHENG_BRACE(L2)` | `WORK-P3-BRACE-L2-01` 与 powered trim 合并为 `RELEVEL_TRANSFER_STAGE_2`；材料 `1→0`、power `3→2`；Anchor/Engineer 承受已预览接触载荷 | load/power margin均2；`EV-P3A-010 SAFE_RELEVEL reached`；Anchor anchor 与 Engineer tool 各 `2→1` |
| E3-W4 | 不用 C2 | 所有身体按安全路撤；Full/Skip 只改演出 | `OP-SETTLEMENT`；structure safe_relevel；Anchor/Engineer system 各降1；comms0 |

### 13.2 P3-B：先隔离供能 → 人员优先 → 安全拆离

| 窗 | C2 介入 | 关键身体动作 | 预计持久 delta / event |
| --- | --- | --- | --- |
| E1-W1 | `BAIYUAN_PREVIEW(C-PE,C-LE)` + `JICUN_ROUTE(C-PE)` | Scout 到 Power/Evac 通道；Engineer 准备隔离；不重复 L1 Brace | `EV-P3B-001 low_load_route_selected`；无 Adapter brace learning |
| E1-W2 | `QIHAI_VERIFY_AUTH` + `JICUN_ASK(Carrier:C-PE one_by_one)` | Carrier 接受；Engineer 执行 `PREPARE_DETACH_RAIL`，power `6→5` | `EV-P3B-002 consent_accept`；rail `stowed→prepared`（尚不满足拆离）；power5 |
| E1-W3 | `LUHENG_VERIFY(P2_bus)`；应忍住 `BAIYUAN_FLAG`，因为没有前后模型差异 | Carrier 经 C-PE 运1人并写 `EVAC_TRANSFER`；Scout 本地确认真实 P2 测量 | `EV-P3B-003 P2_measurement_verified`；safe_people=1；power `5→4`；不创建假说 |
| E1-W4 | 保留带宽 | Carrier 经 C-PE 运第2人并写 `EVAC_TRANSFER`，power `4→3`；Anchor 只执行一次通用低载 Brace，不构成重复族；共享 relay 始终关闭 | `OP-CHK-1`：safe_people=2；remaining1；power3；L1=1/L2=2；Adapter 可见载运但无法把两次用电归因到 `BUS-P1`，enemy learning none |
| E2-W1 | `QIHAI_AUTHORIZE(manual_safe)` + `LUHENG_VERIFY(detach_prereq)` | Engineer 实体隔离 P2；Locker 锁 remote release 不影响手动隔离 | `EV-P3B-004 P2_isolated`；control=manual_available |
| E2-W2 | `JICUN_ROUTE(last_person→C-PE)` + `JICUN_ASK(Carrier:people_then_record)` | Carrier 返回；主体反提案并被玩家接受；power-1 | `EV-P3B-005 counterproposal_receipt`；power2 |
| E2-W3 | `BAIYUAN_PREVIEW(detach,offline_hold)` + `QIHAI_STOP(P1_test_motor)` | Engineer 手动 safe；Locker 对 Scout 的已暴露 sensor 执行具名 system 接触令其 `2→1`；Jammer 同窗压制两条共享信道中的一条 | `EV-P3B-006 control_manual_isolated`；power remains2；communication_quality `2→1` |
| E2-W4 | 不用 C2 | Carrier 经 C-PE 运最后1人，power `2→1` 并写 `EVAC_TRANSFER`；Engineer 同窗在轨端执行零供能 `ALIGN_DETACH_RAIL` | `OP-CHK-2`：safe_people=3；rail `prepared→aligned`；power1；Scout sensor1 |
| E3-W1 | `QIHAI_VERIFY_AUTH(AUTH-P3-DETACH-OFFER)` + `JICUN_ASK(TEST-STRUCTURE-A-SAFETY-CONTROLLER:detach_with_guards)` | 两张非物理 receipt 分别在 `t=1.0s/2.0s` 形成；Engineer 只在 `t=2.5s` 后开始 `PREPARE_DETACH_SEAM`，核对已对齐轨、隔离总线、三人安全并安装拆离领圈，材料 `4→3` | `EV-P3B-007 owner_authority_valid`；`EV-P3B-008 structure_consent_condition_met`；七海只核验、不发拆离权；实体动作严格晚于 receipt time |
| E3-W2 | `JICUN_ROUTE(Carrier→record)` + `JICUN_ASK(Carrier:record_if_window)` | Carrier 按反提案取记录；Engineer 安装 `DETACH_TRANSFER_JACK`，材料 `3→2`；Anchor 做材料0基础 Brace | `load=1+2+brace1-moving3=1`；L1 stress `0→1`；`EV-P3B-009 record_custody_and_transfer_ready` |
| E3-W3 | `BAIYUAN_PREVIEW(detach_now,wait)` + `LUHENG_VERIFY(detach_execution)` | Engineer 在 owner token 与结构 condition receipt 下完成具名 `TACT_INTERACT(detach L1 segment)`；Anchor/Catch 共同执行 `DETACH_EXECUTE_STAGE_2` 将载荷导向 L2 | 第二个拆离窗 `load=1+2+brace1-moving3=1`，L1 stress `1→2` 后功能 `1→0`；`EV-P3B-010 SAFE_DETACH reached`；L2=2；materials2 |
| E3-W4 | 不用 C2 | Carrier、Scout、Engineer 与 Anchor 都沿各自安全边撤出；Full/Skip同结果 | `OP-SETTLEMENT`；structure safe_detach；records secured；Scout sensor1 |

### 13.3 P3-C：静默保底的 Encounter 级 choice trace

| Encounter | 关键选择与实体动作 | 资源／持续 delta | 终点 |
| --- | --- | --- | --- |
| E1 | 不建立主动 relay；核验 L1 后 Engineer 安装一个标准 L1 支撑鞋、Anchor 做一次材料0实体 Brace，Carrier 经 C-LE 一次运2人并写两张 `EVAC_TRANSFER` | materials `4→3`；power6；safe_people=2；无重复可观察动作，learning none | L1=1/L2=2；最后本地快照有效 |
| E2 | Engineer 用本地手动杆隔离 P2，并以小型适配固定杆位；Carrier 经 C-PE 运最后1人并写 `EVAC_TRANSFER`；主动关闭共享 relay 以免继续暴露 | materials `3→2`；power `6→5`；`topology_breaks 0→2`，故 comms=`relay2-topology2=0`，relay integrity 仍为2；Carrier cargo system `2→1` | safe_people=3；control=manual_hold；learning none |
| E3 | Anchor 维持 L1、Engineer 在 L2 提交第二处独立实体 Brace；执行 `OFFLINE_HOLD_TRANSFER` 并使 P1 转 safe hold | `load=1+2+brace2-moving3=2`；materials `2→1`；power `5→4`；可见静态变形使 L2 `2→1`；通信保持 offline | `STABLE_OFFLINE_HOLD`；在线记录／运行能力 forward_failure |

这是一条已定义的纸面 choice trace，但仍须由完整搜索证明可达、由玩家独立发现才算第三个可行方案；作者照表点击不能记入 `S-DIVERSITY`。

## 14. Encounter 持续字段与结算原子性

| state family | E1→E2→E3 必须持续 | 允许重置 |
| --- | --- | --- |
| `ST_BODY` | systems、interfaces、integrity、heat、energy、ammo、tool wear、位置安全态 | checkpoint 可让未持续受力且未过热的 body `heat -1`，不得修系统 |
| `ST_LOCATION` | L1/L2、tilt、bus、control、relay、rail、通道损伤 | 无 |
| `ST_CONTACT/KNOWLEDGE` | 每个 observer 的来源、时间、置信、真假尚未知状态 | 仅派生新 projection；不抹来源历史 |
| `ST_AUTHORITY` | scope、期限、receipt、物理层是否已执行 | 过期按合同改变 status；不删除审计 |
| `ST_CONSENT` | 具体提案、条件、回应、是否已解决 | 已解决 action 可关闭；不能转永久服从 |
| `ST_RESOURCE` | materials、power、tool、support reservations receipt | bandwidth/reaction slot 按窗重置；用途摘要保留 |
| `ST_ENEMY_LEARNING` | observer、可见依据、confidence、counter、first_available_at | 无；未观察就不得生成 |
| `ST_OPERATION/RESULT` | Encounter resolution、objective results、变化、future consumer | 只在三个稳定边界推进 |

每个 checkpoint 写单一 `transaction_id`；重复加载／重复提交必须返回原 receipt，不再扣材料、再撤人员或重复生成 learning。若 owner version conflict，整个 checkpoint 回到 pre-state，而不是保留部分身体变化。

## 15. 任一席位缺席时的现实替代

| missing seat | 替代路径 | 明确代价 / 不能偷渡的能力 |
| --- | --- | --- |
| `CH_JICUN` | 各 body 使用本地 beacon、固定拓扑与实体会合点；路线每跨区多耗1窗 | 不生成共享实时态势；最后快照保持过期标签 |
| `N_BAIYUAN` | 使用共同 Forecast kernel 的单计划结果带，并选择保守 worst-case | 不能自动比较；材料或 power 至少多耗1；未知仍未知 |
| `CH_QIHAI` | 联系测试结构本地 owner 或由 Engineer 走手动 safe；无法取得时走 offline hold | 多耗1-2个实体动作；不伪造权限；不能远程释放 |
| `CH_LUHENG` | 本地工程员按保守公开载荷表，只允许低载路径和标准 Brace | 不能走高载 relevel；更可能进入 safe_detach/offline_hold |

四个缺席变体都必须能获得至少一个非 continuation-break 终局；如果移除某席便没有任何合法后继，P3 Fixture 失败，不得解释为“角色很重要”。

## 16. P3 预计摘要 hash

本节的 `comms` 是终点 `communication_quality`，不是 `relay_integrity` 的别名：P3-A 的 0 来自 E2-W2 与 E3-W1 两次可观测 Jammer 压制，P3-B 的 1 来自 E2-W3 的单信道压制，P3-C 的 0 来自玩家提交的 `offline_safe`。完整状态仍须分别保留设备完整度、活动 beacon、jam 与拓扑断点。

### 16.1 初态

```text
P3v0.1|operation=TEST_STRUCTURE_A|encounter=E1|load=L1:1,L2:2|control=locked_local|power=6|comms=2|people=0safe/3total|rail=stowed|materials=4|support=4|body_damage=none|authority=control_limited+detach_offer_unverified|consent=none|enemy_learning=none
```

`paper_summary_sha256 = 2adb3a67a6c7a1d3e4df9514c7987cbccf88876e6d552ff90e84e99029af0f0f`

### 16.2 三终局

P3-A：

```text
P3v0.1|route=SUPPORT_RELEVEL|people=3of3|structure=safe_relevel|load=L1:1,L2:2|control=manual_safe|power=2|comms=0|materials=0|body_damage=anchor:1,engineer:1|consent=accepted_conditional|enemy_learning=brace_counter_seen|result=clear_with_cost
```

`paper_summary_sha256 = 19d7e1c8be061e1966f0f40d1328e52459760a0689821faf19bd39ded052d9cc`

P3-B：

```text
P3v0.1|route=ISOLATE_DETACH|people=3of3|structure=safe_detach|load=L1:0,L2:2|control=manual_isolated|power=1|comms=1|materials=2|body_damage=scout:1|consent=carrier_counterproposal_met+structure_condition_met|detach_authority=owner_token_valid|enemy_learning=none|result=clear_with_structure_loss
```

`paper_summary_sha256 = 9c56e9251b1db909e1128578b7ecc83585fd7c6c2ea907388a66a3e45a9923aa`

P3-C：

```text
P3v0.1|route=SILENT_HOLD|people=3of3|structure=stable_offline_hold|load=L1:1,L2:1|control=manual_hold|power=4|comms=0|materials=1|body_damage=carrier:1|consent=accepted_conditional|enemy_learning=none|result=clear_with_data_loss
```

`paper_summary_sha256 = adf305edf4c9939700c3a06c4c1515f13db557b51a522168092e62995723440e`

三条摘要已经按逐窗资源 delta 重算为唯一纸面目标；它们仍不是 resolver 运行结果。日后完整状态方程若产生差异，必须回到对应动作、资源或路线 owner 修订并重新 hash，禁止用 Operation Settlement 补丁抹平。

## 17. P3 自动门、真人门与退出条件

Build 之前的纸面／自动门：

1. P2 已有 M5、人类误读红线通过和用户有界迁移回执；
2. 三个 checkpoint 的重复提交、故障回滚、Full/Skip、帧率、加载顺序与存读档 hash 相同；
3. Body、Location、Authority、Consent、Knowledge、Resource、Enemy Learning 都从 E1 持续到 E3，没有只带一个 score；
4. P3-A、P3-B、P3-C 经完整规则程序可达，并且至少在首个 Encounter 的路线、资源和承力职责上不同；
5. 四个 missing-seat 变体各有一个可继续终局，且替代代价可在 UI 预览；
6. Adapter 只能学习实际可观察到的动作，counter 最早下一 Encounter 生效；
7. 地图身体阶段变化只来自已提交的支撑、隔离、供能、通信与撤离状态，不监听 HP 百分比；
8. 第 16 节的摘要、逐窗事件和资源守恒在实现包中仍一致；若出现差异，重新打开 M2 停止门，不得带差异申请 M3。

日后真人门仍按登记表执行：至少 8 名已学会基础规则的目标玩家；至少 6/8 得到合法结果、7/8 能复述前态因果、三种终局被独立发现、缺席席位可替代。内部作者按 golden trace 走通、自动搜索找到路线或机器 PASS 都不能替代这些结果。

## 18. 本件仍未完成

- 没有P1四版Build/M5、shortlist、C2 crossover或最终Scheduler；因此本件只能定义语义窗与适配接口；
- 没有可执行 resolver、自动 Fixture、UI、灰盒地图、存档、回放或真实状态 hash；
- P2 两条、P3 三条预计路线没有经过有界搜索或真人发现；
- P2 的 100 条 authority action 微 Fixture 尚未生成或运行；
- 没有用户产品方向、玩法、Build、真人测试、章节接入、资产或 Runtime 批准；
- 本件不得被 Reader、L6、Demo 或正式章节直接消费。
