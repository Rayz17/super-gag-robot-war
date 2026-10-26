# C01E02 M3-R0｜单轮共同结算可试玩沙盒任务书

> 派发对象：主程序 Session  
> 状态：`authorized Candidate implementation / R0 only`  
> 停点：交付可试玩单轮、机器证据与完成报告后停止，等待用户试玩  
> 美术：本任务不派发美术、不生成新资产

R0 运行身份固定为：

```text
sandbox_contract_id=C01E02M3R0
sandbox_contract_revision=1
build_id=C01CDV1-M3-R0-SANDBOX
rules_profile_id=c01cdv1_e02_shared_round_m3_r0
runtime_lane=candidate_development_sandbox
entry_role=non_default
save_mode=disabled
save_schema=null
save_namespace=null
operation_commit=false
story_checkpoint_write=false
asset_mode=named_geometry_only
```

合同中预留的正式存档 schema `3` 只在 R2 接回时生效；R0 不得宣称已经采用正式 M3 存档。

## 1. 唯一目标

在现有 Godot 项目内制作一个**开发态、可试玩的单轮共同结算沙盒**，证明：

```text
公开冻结意图
→ 编辑馆守Z短路线与独立朝向
→ 选择主动作或预备反应及备用方案
→ 查看可返回的提交摘要
→ 长按执行一次
→ 馆守Z、小体、车辆、BREAKER、环境从同一轮前态结算
→ 生成轮回执
```

本任务不接完整 E02，不切换默认 Demo，不实现盾牌、赤红冲击、盾拍或 P1。

## 2. 冻结输入与开工检查

唯一制作人合同：

- `docs/superpowers/specs/production/c01-current-demo-v1/31-c01e02-m3-common-turn-inplace-migration-producer-contract.md`
- SHA-256：`06d17169f8002a09617a8acb2a92886495ad8dbe524cfca237f9079159050860`
- 开工前必须精确核验；不一致则停止，不得自行刷新。

当前实现快照仅用于复用与对照，不是新玩法权威：

| 角色 | 路径 | 派发时 SHA-256 |
| --- | --- | --- |
| 旧 tactical session | `game-godot/scripts/candidate_runtime_demo/c01/e02/candidate_tactical_session.gd` | `ea317189282cb4f86101892c615dc1d1ba663dd107fa0c26972495ecfda9ae18` |
| 当前 Runner | `game-godot/scripts/candidate_runtime_demo/c01/e02/c01e02_g1_runner.gd` | `60c588a6ec158cc367071476961d69f50a41d12efb7d693216e521657c8764aa` |
| 当前战术 profile | `game-godot/content/candidate_runtime_demo/c01/e02/graybox_profiles.json` | `07f611fabb1a41c713da5019ce433820f95229cbf83b633fe67fa43d836278da` |
| 当前资产 active binding | `game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/active_asset_binding_r2.json` | `7a6e993a4452b9e6888c936341bfe614d0cf18dfe9a913d68a84d7a7ddd48b49` |
| 当前六槽 validated receipt | `game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/validated_receipts/a4_static_5_plus_a5_rift_swarm_96.validated.json` | `c284fe2b04f04526cd22280e47e89f879f2d3d5e3d5c8a82528e27b71b7e2e5e` |

若上述文件在开工时漂移：先判断是否为本任务以外的并行修改；不得刷新期望哈希掩盖冲突。只要旧 session 的纯逻辑接口仍能辨认，允许记录漂移并继续新目录实现；涉及默认入口、profile身份或资产绑定语义冲突则写 `BLOCKED.md` 并停止。

## 3. R0 场景边界

R0 从馆守 Z 刚走出展厅、抬起第二步且应急车辆即将穿过落脚区时开始，停在第一次身体责任与巨体接触完成后：

- 观众已全部进入加固避难所，不出现在巨机棋盘；纪存已在导览席提供路线判断但不控制四肢，七海只完成撤回本人停机令；
- 馆守 Z 双前臂完整，退役重盾仍挂在展位并只有三道旧焦痕；
- 一辆应急车辆按公开时序先通过馆守 Z 的落脚区；
- 一只小型突入体公开意图为进入／攻击撤离线；
- BREAKER 公开为沿穿向北侧城市的直线冲撞，本轮只在结尾开始聚集红光，不释放赤红冲击；
- 城市边缘炮火公开为自主支援：若馆守 Z 使冲角偏开、侧甲暴露，则按冻结计划命中侧甲；它不由玩家或七海控制；
- 玩家给馆守 Z 画短路线、选终点朝向，并可设置：
  `小体进入撤离保护线 → 横腿侧顶；否则守住出口`；
- 提交后反应若触发，小体只被侧推／改线，不被消灭；
- 馆守 Z 最终站在撤离线与 BREAKER 之间，与 BREAKER 组成同前态接触组；
- 首次正撞使馆守 Z 被推出、广场路面翻起，玩家正确占位／朝向时将冲角偏开一截，城市炮随后命中暴露侧甲；
- 轮末 BREAKER 开始聚集红光；
- 本轮不取得重盾、不释放／结算赤红冲击、不清空整条撤离线、不出现盾拍、不写 P1。

允许玩家提交其他合法计划并看到相应风险或失败回执；不得把推荐计划自动填入。至少两种**单轮成功计划**应以不同路线／朝向完成上述固定身体责任，并在接触时点、小体落位、馆守 Z 承力或路面状态上产生可见差异；另有至少一种错误计划能给出明确失败原因。它们不是 R1 的两条完整战法证明。

R0 固定成功出口至少包含：

```text
guardian_between_lane_and_breaker=true
first_vehicle_crossing_resolved=true
first_swarm_deflected=true
breaker_first_charge_contact=true
breaker_charge_line_partially_redirected=true
breaker_red_charge_state=charging
shield_state=wall_hung_3_scorches
rescue_lane_state=active
breaker_alive=true
breaker_first_knockdown=false
swarm_organization_state=scattered
story_checkpoint_reached=false
mission_clear=false
prototype_stop=M3_R0_PROTOTYPE_STOP
```

## 4. 实现结构

建议最小分层，命名可等价调整：

```text
RoundStartSnapshot
FrozenIntentSet
UnitPlanDraft[]
  - route
  - final_facing
  - main_action XOR prepared_reaction
  - fallback
PreviewSummary
SharedRoundResolver
RoundReceipt
```

生命周期必须严格为：

```text
ROUND_START_SNAPSHOT
→ PUBLIC_SITUATION
→ EDITABLE_DRAFT
→ COMMIT_SUMMARY
→ COMMITTED_PLAN
→ JOINT_RESOLUTION
→ ROUND_RESULT
```

硬要求：

- `UnitPlanDraft` 使用数组／按 unit_id 映射，即使当前只有馆守 Z；
- 每条公开意图保留 `confidence_state`（`confirmed/estimated/unknown`）、动作类型、目标、预计时点、来源与有效时间；R0 实例可以全部为 `confirmed`；
- `PreviewSummary` 与 `execute_round` 共用同一个 resolver；预览在克隆前态上运行；
- 同时接触按时间片／接触组处理，不依赖单位容器遍历顺序；
- prepared reaction 每轮最多触发一次，反应链必须终止；
- prepared reaction 未触发时轮末失效；fallback 是另一概念，只在后续路线／动作因前置接触失效时启用，不赠送额外行动，并在触发失败前写入摘要；
- 所有随机性关闭；相同前态与计划产生相同 `RoundReceipt`；
- 编辑阶段不启动计时，不推进敌人、车辆或环境；
- 执行阶段不接受临时战术输入。

`RoundReceipt` 至少包含：`round_id`、`round_start_hash`、`public_intent_hash`、`committed_plan_hash`、`timeslice`、`prestate_hash`、`contact_group_id`、`prepare_triggered`、`fallback_taken`和`round_result_hash`。

## 5. 最低可玩界面

同一画面至少可读：

- 馆守 Z、目标小体、应急车辆、BREAKER、撤离线；
- 每个非玩家主体的公开意图、时间窗、可能接触组与公开结算优先规则；不得显示按单位 ID 逐只行动的伪顺序；
- 可走区域、当前路线、终点格和终点朝向；
- 主动作／预备反应二选一，以及 trigger、response、fallback；
- `查看摘要`、`返回修改`、带可见进度的`长按执行本轮`；
- 执行后的事件顺序、是否触发预备、车辆／小体／馆守 Z／BREAKER／城市炮火／路面的新状态；
- 一键重置到同一轮前态。

规划辅助可以解释两个合法起手及其代价，但默认关闭；不得操纵光标、填计划或执行。

R0 可使用具名几何和程序色块。不得以新美术、动作动画、LibTV、声音或最终 HUD 为前置。

## 6. 允许写入

除下列新路径外，工作区其他文件一律只读：

- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_r0/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/m3_r0/**`
- `game-godot/content/candidate_runtime_demo/c01/e02/m3_r0/**`
- `game-godot/tests/candidate_runtime_demo/m3_r0/**`
- `scripts/run_c01e02_m3_r0_sandbox.sh`
- `scripts/test_c01e02_m3_r0.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m3-r0/**`

如果 Godot 导入需要生成 `.uid`，只允许生成与上述新文件对应的 `.uid`。

`run_c01e02_m3_r0_sandbox.sh` 必须直接启动新增的非默认 `.tscn`；不得经过 startup router、Current 启动脚本，也不得调用 `materialize_sources.py --write`。

## 7. 禁止写入

- 当前 `c01e02_g1_runner.gd`、`candidate_tactical_session.gd`、`graybox_profiles.json`；
- `candidate_input_router.gd`、`candidate_isolation_guard.gd`、`candidate_local_state.gd`、`candidate_save_store.gd`；
- `materialize_sources.py`、`build_capture_manifest.py`、现有 Runner 场景与所有旧 R2 测试／`main-m2*` 证据；
- `episode_g1.json`、当前 build identity、materialized snapshot；
- `project.godot`、默认 startup router／selector、当前启动脚本；
- Candidate 正式存档类、存档目录与 namespace；
- `named_geometry_fallbacks.json`、A4/A5 源文件、approved runtime assets、active binding、validated receipts、resolver 与静态 manifest；
- 19／31／32 号合同正文；
- Canon、Reader、剧情、C04、美术、LibTV、正式 Runtime；
- `git add`、`git commit`。

同时禁止把应急车辆、小体、城市炮火或普通人做成可控友军；禁止让 BREAKER 因“仇恨值”改成追馆守 Z；禁止让散乱小体编队或响应 BREAKER；禁止调用勇拳、E03 双拳、飞行核心、红孔同步或任何 E03／E04 状态。

如确有必要修改禁止文件才能获得可玩入口，先停下说明原因与最小替代方案，由制作人重新裁决；不得先改后报。

## 8. 必须通过的验收

### 8.1 语义测试

1. 路线、朝向、动作、预备的任意编辑／撤销均不改变轮前世界签名；
2. 玩家开始编辑后，敌方真实计划与公开意图保持冻结；
3. 同一路线可选择不同合法终点朝向，移动不自动覆盖选择；
4. 摘要与执行来自同一 resolver，摘要承诺的确定事件与实际回执一致；
5. 预备在满足 trigger 时恰好触发一次；未触发时轮末失效，执行中不弹窗补选；
6. 前置接触使后续路线／动作非法时，只能进入摘要预先声明的 fallback；没有 fallback 时停在最后合法状态；
7. 车辆、BREAKER、小体、城市炮火条件与路面状态在同一轮日志中各结算一次，编辑期间为零次；
8. 小体被侧推但不被消灭，组织状态保持 `scattered`；
9. 改变小体或其他实体容器／stable ID 遍历顺序，不改变接触组结果；
10. 每种验收计划从同一前态连续 20 次得到相同 RoundReceipt 与世界签名；
11. R0 不写现有正式存档，不修改默认入口、M2.5 build、资产 binding 或 P1。

### 8.2 可玩验收

- 提供一个明确启动命令，用户无需打开 Godot 编辑器配置场景；
- 从局势公开到轮回执可完整操作；
- 摘要可以返回修改，执行必须实际长按；
- 至少两种单轮成功计划有可见差异；另有至少一种错误计划给出可理解原因；
- 1280×720 下无关键文字溢出或被遮挡；
- 提供至少一张摘要截图、一张执行后截图，以及一段完整单轮捕获或逐事件状态记录。

## 9. 回归边界

R0 至少运行：

- 新增 R0 专项测试；
- 现有默认启动冒烟；
- M2.5 核心合同与六槽资产测试，证明未被 R0 影响；
- `python3 scripts/check_canon_authority.py`；
- `scripts/canon-smoke-test.sh`；
- `scripts/canon-check-godot.sh --report` 与 `--strict`；
- `git diff --check`。

不要为了让旧测试适配 M3 而修改旧测试；R0 尚未切换默认内核。

## 10. 交付与停点

交付到 `main-m3-r0/`：

- `00-implementation-notes.md`
- `01-test-summary.md`
- `02-playable-controls.md`
- `03-capture-manifest.tsv`
- `04-completion-report.md`
- `captures/**`

完成报告必须明确：

- 哪些逻辑复用了旧 M2.5，哪些是新 M3；
- R0 证明了什么、没有证明什么；
- 默认 Demo、存档、A4/A5 与 P1 均未改变；
- 任何已知的摘要／执行差异、UI可读性问题或实现债；
- R1 是否具备开工条件。

交付后停止。不得自行进入 R1、修改完整 Demo、接入资产或请求美术生产；等待制作人与用户试玩裁决。
