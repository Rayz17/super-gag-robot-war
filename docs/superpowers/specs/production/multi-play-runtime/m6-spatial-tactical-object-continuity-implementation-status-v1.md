# 《超GAG机器人大战》M6 Spatial / Tactical 同物连续性实现状态 v1

> 日期：2026-07-15  
> 状态：`candidate_object_continuity_validated`。  
> 上游：`2026-07-15-chao-gag-multi-play-experience-production-contract-v1.md` P2/P3。  
> Canon 边界：只在 M6 `runtime_validation_only` 样例中验证稳定对象、互动合同与战术映射；不提升 C02E03、不把旧拳王右拳护具登记成独立机体、不锁定正式地图或美术、不解冻 V35.10。

## 1. 本轮结论

多玩法不再靠“上一页记了一个 flag，下一页发一个 bonus”维持联系。M6 现在让同一件东西拥有跨模式身份：玩家在维修棚走近、检查、回看并据此打开维修草案；统一状态保存它的访问和认知；战棋解析器再把同一个 ID 投影为单位部件、武器、保护目标、敌方单位、地图格或中段事件。

活动结果仍负责数值和行动条件，稳定对象负责“它还是刚才那件东西”。因此调查不会无缘无故加攻防，玩家先获得理解，随后在 CONSTRAINT、TIMING 和 TACTICAL 中承担结果。

## 2. 共享合同

### 2.1 StableObjectNode

Graph 节点声明 `stable_objects[]`。运行时为每项生成 `Area2D` 场景节点，承载：

- `stable_object_id` 与候选别名。
- 玩家可读名称、位置和交互半径。
- 初始对象状态。
- `interaction_offers[]`。

位置和交互范围不再写死在 Workshop 脚本的热点数组里。后续 P2 生产层已让对象按房间显示，并接入三房间 Portal、精确返回点、动态唐胶与多轮 NarrativeOverlay；当前仍使用候选背景裁切、程序信息层和场内人物标记，正式分层 Sprite、碰撞遮挡与步行动画尚未完成。

### 2.2 InteractionOffer

每个 Offer 声明：

- `offer_id`、动作、说话者、首轮文本和重复文本。
- `repeat_policy`：首轮后回顾、变化式回顾、持续可用或提交后关闭。
- `requires_all_offer_ids`、`requires_any_offer_ids` 或分组前置。
- `known_state`、标签和对象状态变化。
- 可选 `opens_phase`，明确由哪个世界动作打开活动。

重复交互增加访问记录但不再次完成 Offer，不重复发结算。锁定对象保留在场景里，但不会伪装成可调查目标。

### 2.3 统一状态

`ActivityOutcome` 新增 `world_object_changes[]`，事务层和 `ChaoGagRunStateStore` 新增 `world_objects`。对象状态至少保存：

- `known_state`
- `visit_count`
- `completed_offer_ids`
- `last_offer_id`
- `tags`

Workshop 快照同时保存注册表状态、人物位置、活动草案和 TIMING 进度；切换模式和读档都不会把对象重新变成未调查。

## 3. M6 互动因果

维修草案不再由“任意检查两个点”自动打开：

1. 玩家至少确认右拳护具或膝轴之一，得到一条身体依据。
2. 玩家至少确认原速录像或仓门报警器之一，得到一条现场依据。
3. 唐胶的零件盘才变为可操作对象。
4. 玩家走到零件盘并主动确认，才进入 CONSTRAINT。

直播终端初始只显示倒计时；必须先从原速录像发现自动补帧掩盖了漏拍，才可关闭“动作优化”。这条解锁由 Offer 前置声明，不由场景脚本写特殊判断。

## 4. 同物战术映射

| Stable object | Tactical 投影 | 意义 |
| --- | --- | --- |
| `OBJ_M6_RIGHT_GLOVE` | 旧拳王 `right_fist` 部件与 `body_jab` 武器 | 右拳是整机拳路锚点，不是第二台机体 |
| `OBJ_M6_KNEE_BEARING` | 旧拳王 `left_knee` 承力部件 | 漏拍与身体负重顺序相连 |
| `OBJ_M6_SHADOW_TAPE` | 影子陪练机、失败录像目标 | 玩家在战前看见的时间差进入战场 |
| `OBJ_M6_WAREHOUSE_GATE_PANEL` | 仓门保护目标、坍塌事件、撤离格 | “只剩一套撑杆”在第二回合变成取舍 |
| `OBJ_M6_LIVE_TERMINAL` | 镜头无人机、证据目标 | 镜头压力有可攻击身体和可保护记录 |
| `OBJ_M6_REPAIR_BENCH` | `repair_plan` 战斗来源 | 草案与两项 Activity Patch 属于同一现场决定 |

`BattleSetupResolver` 读取 `world_objects` 后生成 `resolved_stable_objects`，并给单位、部件、武器、目标、事件和格位附加来源信息。`DeclarativeBattleSession` 把该 trace 带入战果。战术地图用短符号字标避免全名互相遮挡；已在维修棚确认的对象显示小型金色来源标记，光标侧栏显示其玩家可读状态。

## 5. 构建门禁

`EpisodeBundleCompiler` 现在同时校验：

- StableObject ID 与 Offer ID 唯一。
- 每个 Offer 有合法重复策略。
- 前置 Offer 指向存在的 ID。
- Tactical binding 的单位、部件、武器、目标、事件和格位引用有效。
- Graph 中每个稳定对象都有战术映射，或明确声明 `tactical_skip_reason`。

删除任一 M6 对象的战术 binding 会以具名对象 ID 阻断构建。Bundle 合同新增 `stable_object_continuity_validated=true`。

## 6. 验证证据

自动证据覆盖：

- 终端前置、维修台分组前置、首轮与重复交互。
- 六个 Graph 对象生成六个 `Area2D` 场景节点。
- Workshop 精确存取和四个已访问对象恢复。
- `world_object_changes` 经事务进入统一状态。
- Tactical 对右拳和原速录像解析为已知的同一对象。
- 缺失映射时内容编译失败。
- 34 组 Godot 全量回归通过。

1280×720 像素证据已由后续 Spatial 生产层刷新：

- `outputs/multi-play-presentation-validation/04a-m6-workshop-front.png`
- `outputs/multi-play-presentation-validation/04b-m6-workshop-repair-floor.png`
- `outputs/multi-play-presentation-validation/04c-m6-workshop-back-storage.png`
- `outputs/multi-play-presentation-validation/05-m6-workshop-dialogue-overlay.png`
- `outputs/multi-play-presentation-validation/06-m6-tactical-object-continuity.png`
- `outputs/multi-play-presentation-validation/07-m6-tactical-held-punch-presentation.png`
- `outputs/multi-play-presentation-validation/08-m6-tactical-collapse-presentation.png`

第二轮截图修正了中文长句裁切、战棋全名堆叠和棋盘尺度；后续 P3 截图补入完整旧拳王地图图、原速漏拍 Pose 与 controlled rescue 事件演出。这仍只证明候选几何、资产接线和状态版本可读，不等于正式机体资产、地图美术或真人理解通过。

## 7. 仍未完成

1. 三房间、返回点、动态唐胶和 NarrativeOverlay 已由 `m6-spatial-production-layer-implementation-status-v1.md` 接续完成；正式地图分层、碰撞、步行 Sprite 和鼠标寻路仍未完成。
2. 中段坍塌仍在第二回合触发，但现已根据仓门报警器与维修草案组合选择默认、提前警告和 controlled rescue；正式 Episode 是否沿用这一固定回合仍待内容验收。
3. 旧拳王已完成候选地图图、标志 Pose、唐胶 Cut-in、武器与救援短演出；P3b 已为其余八个实体补齐 A 档程序化地图轮廓，独立动作帧、正式 Sprite/Cut-in、音效和性能档仍未生产。
4. P4 的 `experience_contract`、四消费槽、失败继续和容量回执门禁已进入 Bundle Compiler；M6 结构通过，但真人时长回执仍为 pending。
5. Windows 真机、实体手柄和外部真人盲测仍为空。

## 8. 下一步

P2/P3 的“同一对象可跨玩法识别并改变规则与演出”已在候选 M6 上形成可运行底座；P2 空间生产层与 P4 结构门禁也分别由 `m6-spatial-production-layer-implementation-status-v1.md`、`m6-experience-contract-build-gate-implementation-status-v1.md` 接续完成。P3b 已让九个战场实体摆脱圆点占位；下一轮应把具名机体升级为正式 Sprite 与动作资产、补 Spatial 正式地图分层，取得真人容量/理解回执，再选择一话通过 Pressure Board 与 Reader 的正式 Episode 做 P5 生产验收。
