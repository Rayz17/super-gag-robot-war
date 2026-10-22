# C01E04 Godot Runtime Parity Audit v1

> Status: `candidate_runtime_parity_57_verified_0_partial_0_missing_27_visual_receipts`
>
> Audit target: `C01E04_RT001..C01E04_RT057`
>
> Production boundary: 本报告只证明当前 Godot 候选实现与 57 条 Runtime 合同的逐行映射状态，不证明正式美术、音效、真人节奏、Windows 导出或商业版本完成。

## 1. 审计口径

本轮不再用“战斗能走通”“主路线可结算”代替逐条 Runtime 对齐。审计把以下四层同时作为证据：

1. 权威合同：`剧情梗概/V35.9/rebuild/episodes/C01/C01E04-runtime-contract-v1.tsv`；
2. 当前实现：E04 Story Graph、Spatial、Constraint、Tactical Session 与 Tactical UI；
3. 直接测试：E04 Preflight、Session、Motion、Integration 与 Chapter Runner；
4. 机器矩阵：`data/gameplay/c01e04_godot_runtime_parity_v1.tsv` 与 `scripts/check_c01e04_godot_runtime_parity.py`。

矩阵每一行必须满足：

- 与权威合同恰好一一对应，不能缺行、重号或另造 Runtime id；
- `VERIFIED_CURRENT` 必须有当前源码路径、直接测试路径和可在证据文件中找到的令牌；
- `PARTIAL_CURRENT` 必须写明仍缺什么，不能以“后续优化”代替；
- 新增的可执行高风险行 RT012、RT013、RT019、RT027、RT033、RT041、RT044、RT052、RT057 必须保持 `VERIFIED_CURRENT`。

## 2. 当前结论

| 状态 | 行数 | 含义 |
|---|---:|---|
| `VERIFIED_CURRENT` | 57 | 当前实现、直接测试与证据令牌共同覆盖合同要求 |
| `PARTIAL_CURRENT` | 0 | 没有仍以部分实现计入的 Runtime 行 |
| `NOT_IMPLEMENTED` | 0 | 没有整条 Runtime 完全缺失 |

这说明 C01E04 当前候选逻辑已达到 57/57 Runtime Parity。检查器现将任何 `PARTIAL_CURRENT` 或 `NOT_IMPLEMENTED` 视为回归并失败；这仍是候选逻辑完成，不外推正式美术、真人节奏或平台制作完成。

## 3. 本轮补成的关键行为

### 3.1 跌跌与机器狗真实改写目标

跌跌和机器狗不再把“诱导”当成一个抽象减值按钮。玩家必须在地图上选择当前 Writer 目标相邻的合法安全格；取消不消耗行动，确认后立即改写预告路径。敌方结算回执记录：

- 原始起点与最终目标格；
- `redirected` 结果；
- 具体反制来源；
- 主动 Writer 与零分 Relay 身份；
- 本回合火锁、热量、结构和城市区域后果。

医院电网、东侧管线、关键城市格、P1 锚点和 P4/P5 馆体占格不会被错误列为安全诱导格。

### 3.2 当前意图与剩余路线预测

Session 现在分别提供：

- `intent_forecast()`：当前 Writer、目标、基础/主动/总火锁、热量、结构、档案冷却、城市区域伤害与结算结果；
- `route_forecast()`：下一身体 Mask、剩余身体动作、必要停机动作、剩余回合、预计热量/冷却、可达性与阻断原因；
- `_body_action_feasibility()`：在玩家确认前阻止会令剩余路线必然超时、过热或耗尽档案冷却的身体/锁臂选择。

城市段可选展开/收回锁臂不再等到回合上限才宣告死路；当只剩三回合时，主路仍可选，额外锁臂循环会直接显示不可完成原因。

### 3.3 档案分支的下一意图预告

`archive_next_intent_preview()` 在不改动当前状态的前提下计算下一回合主动 Writer 和一条明确的假 Relay。预告有独立 UI 行，不把假意图混入当前回合结算，也不提前移动无人机。

### 3.4 城市伤害与 CITY_LOCAL 回滚

P5 不再只有抽象火锁条。主动 Writer 会依次覆盖旧址基座、医院电网、东侧管线、北侧应急区和城市压力格；未被阻止的医院、管线和关键城市命中分别写入独立损伤字段，并立即进入 RT052。回滚精确恢复 `CITY_LOCAL` 的：

- 三类城市损伤；
- 身体与锁臂 Mask；
- Writer/Relay 位置和轮换；
- 回合、行动、火锁、热量、结构；
- 生活、实体、档案分支资源；
- 七海已暂存且不重复发放的公开延迟回执。

实体缓冲只吸收对应的热量/结构冲击，不能把医院或管线受损抹掉。

### 3.5 四名操作员与五个 Owner

四名操作员现在各有独立的保护框、停止权、在舰、P3确认和P6确认状态；地图令牌显示保护框和停止权绿点。五个 Owner 也按纪存、兜灯、唐胶、陆衡、旧守护者逐人记录。任何一枚定位器失效都会阻断旧守护者确认，缺少任一 Owner 则最终巡航不可用。

### 3.6 载荷物理链与具体留置物

P2 使用独立声明的 `LOADOUT_STAGING`。两类载荷每一段都记录 body-mask 和轨道碰撞结果；实体馆藏在进入安全舱前必须让地图上的配重架向右肩缺口反方向移动两格。取消、存档恢复和 RT050 回滚恢复载荷、配重位置与回执。未选 Bundle 解析为两件具名且带旧址位置的物件，而非通用“留置点”。

### 3.7 F锚保持与馆守Z几何

夹具压线和保持已准备 F 预载是两个不同动作。F锚退销必须读取具体夹具的保持回执，且该回执由跌跌退销消费。馆守Z主动承重会把右肩 Mask 下沉一格；左臂屏蔽严格限制为距当前支撑 Mask 三格，超距时 UI 禁用并要求改用小机或夹具。

### 3.8 城市统一预测与开场四类拆除

`city_forecast()` 把下一合法 Mask、逐格进入/离开/挤压、医院、管线、应急区、火锁、热量、档案冷却与东门延迟倒计时放在同一 payload，侧栏显示紧凑摘要。开场 ADV 同时常驻四个拆除状态条，分别显示楼层与馆体、机体、档案、危险资产及其接管部门。

### 3.9 馆体连续变形与实体识别

Tactical 现在从真实 Session 状态捕获每次馆体变化的 `body_state` / `body_mask` / `lock_arms` / `stage` 前后值，在原斜45度地图上播放0.92秒可跳过同步运动。从固定建筑、东移一节、滑甲、开肋、双锁臂半身，到道路收臂、三段东移和受损巡航，都使用同一张透明移动底盘资产与可插值肋架/锁臂/地标几何，不再只以青色占格声称完成变形。动画中禁止新指令，可存档恢复中点，跳过也只到既有回执终点，不重算热量、冷却、占格或结算。如果与无人机回写同时触发，先播放敌方结算，再进入馆体同步，避免两套状态同时抢操作权。

## 4. 原十二条缺口的关闭回执

| Runtime | 当前关闭证据 |
|---|---|
| RT002 | 四张 ADV 常驻状态卡和 `C01E04_DISMANTLEMENT_CATEGORIES_VISIBLE_LOCAL` |
| RT014 | `prepared_anchor` 地图目标、夹具保持状态与 `anchor_held` 结算 |
| RT016 | `GUARDIAN_RIGHT_SHOULDER_SUNK_MASK` 与 range 3 判定 |
| RT017 | `FINAL_F_CLAMP_HOLDING` 前置及 `consumed_by_release` |
| RT020 | JSON 独立 `loadout_staging_cells` 和启动校验 |
| RT021 | 三段 `cargo_step_receipts` 的逐格碰撞字段 |
| RT022 | `PHYSICAL_BALLAST_SHIFT_TWO_CELLS` 地图位移回执 |
| RT023 | 三 Bundle 的 `UNCARRIED_ITEM_CATALOG` 具名位置清单 |
| RT026 | 独立 `physical_ballast_shifted` 状态加一次性缓冲 |
| RT032 | P3 四枚定位器逐一确认并进入 `HALF_RISE_LOCAL` |
| RT040 | 统一 `city_forecast.cell_deltas` 与 gate countdown |
| RT046 | 五 Owner 状态和四定位器最终门联合断言 |

## 5. 回归门禁

后续修改每一条 Runtime 都必须同时保留矩阵源码路径、直接测试和证据令牌。Parity Checker 要求 `57 VERIFIED_CURRENT / 0 PARTIAL_CURRENT / 0 NOT_IMPLEMENTED`；禁止只改矩阵状态绕过实现与测试。

## 6. 证明边界

当前矩阵证明的是“候选逻辑实现逐行可追溯”。它不证明：

- 正式无人机、馆体、夹具、载荷和角色逐帧资产；
- 生产级战斗动画、Cut-in、SFX、镜头停顿和手柄反馈；
- 25 至 35 分钟目标容量与真人首次理解率；
- Windows/Steam 导出、GPU 兼容、存档迁移和平台成就；
- C01E01-E04 最终商业版本质量。

这些边界不会否定当前可执行逻辑，但也不能被当前自动测试替代。

## 7. 当前机器回执

```text
C01E04_GODOT_RUNTIME_PARITY_CHECK PASS
contract_rows=57 matrix_rows=57
verified_current=57
partial_current=0
not_implemented=0
visual_evidence=27
```

本报告与图谱登记完成后，以下回归已在当前源上重新运行并通过：

- Runtime Parity Checker 与 Runtime Graybox Checker；
- Canon smoke、Godot report 与 Godot strict；
- `doc_registry`、`graph_nodes`、`graph_edges`、Parity TSV 字段宽度与三类图谱 ID 唯一性；
- Multi-play 内容编译，E04 bundle 指纹更新为 `743357a241fd63c6515d701465a06c01a2dd8c24e5ad019a00ad0afaf13b240f`；
- E04 Preflight、Carrier Session、Tactical Motion、Story-first Integration；
- C01 E01-E04 Chapter Runner；
- Content Compiler、Scenario Driver Registry、Battle Presentation Runtime、Multi-play Presentation Shell；
- 1280x720 Tactical 十八帧图形重捕获，人工抽查 P1、P4、P5、实体缓冲、敌方结算、滑甲、道路收臂、城市位移、受损巡航与新移动底盘 Cut-in；地图与侧栏无新增遮挡。
- 1280x720 Preflight 九帧图形硬绑定，覆盖开场四拆卸状态卡、B1巡检、职业反应、0号路线四态、精确二选三台和公开走廊听证；状态卡不压对话框或人物席位。

这些回执证明当前 `57/0/0` 候选逻辑状态稳定，但仍不得把正式制作边界提升为完成。
