# C01E02 Current Demo 原位重基制作人合同

> Status: `producer_contract / authorized / in_place_rebase / candidate_runtime_demo`
>
> Contract identity: `C01CDV1 / revision=2 / save_schema=2`
>
> User decisions: 使用当前已验收 C01 制作完整 E02 试玩；覆盖当前 Demo，不保留另一套可运行 v1/v2；重大故事、玩法、美术及付费生成决策继续停给用户。

## 1. 本合同现在替代什么

本合同授权在原 Godot 项目、原 Candidate Demo 入口和原内容目录上直接重基：

- `game-godot/content/candidate_runtime_demo/c01/e02/**`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/**`
- 现有 C01E02 Candidate Demo 启动入口

不新建第二套可运行 Demo，也不保留旧入口供选择。旧 `12x9` 单 Boss 战棋、旧 CP3 Episode 终局、旧 G1/G1.5 捕获和旧 B3 地图全部退出活跃生产链；若文件仍在磁盘，只能作为 Git/审计历史，不得被入口、构建、资产回退或测试读取。

本合同在语义和 Runtime 处置上高于本目录 `00`–`18` 的旧约定。后续应原位重写 `00`–`13` 并让检查器只接受 revision 2；在此之前，任何旧合同 PASS 都不能作为继续制作的依据。

## 2. 冻结的当前故事截面

| 层级 | 文件 | SHA-256 | 用途 |
|---|---|---|---|
| 已验收纯剧情 Reader | `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C01-闭馆以后万机出击.md` | `c9a9aa490badea3d2de937e0003b80547974fed27103b31ec9181cd3583cfc8b` | 人物、对白、动作结果、事件顺序和章节事实 |
| 用户验收回执 | `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C01/C01-用户创作验收回执.md` | `3d11387d92120cfdeeb0069a2a7cdfbe677ed0ea2ac5ae6649038de7b0cd532b` | 验收范围与明确排除项 |
| 剧情游玩拓扑 | `docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-剧情游玩拓扑与状态桥接.tsv` | `5d640ed3e70854a178194ceeeffe7d444a928547a414af3407674b9d4f4be5aa` | Operation、Encounter、Phase、Checkpoint 和跨话状态 |
| 游戏流程解构 | `docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/gameflow/C01-游戏流程解构-v1.md` | `68ac0efa2d8316f33eb41ca745568684dd180021931355e8ff1d0798196b5296` | 玩家代理、滚动地图、目标与失败条件 |
| 全局拓扑合同 | `docs/superpowers/specs/2026-08-08-chao-gag-story-play-operation-topology-contract-v1.md` | `550da9196bb9029aa0ceb7d75cd1bfdb73c852dd806fb4b609f1765c652eee76` | 剧情话数与游戏战斗阶段的多对多关系 |

冲突时按以下顺序裁决：Canon Hard/Working 锁 → 已验收 Reader 与回执 → 本制作人合同的显式实现裁决 → 拓扑/游戏流程中不冲突的部分 → 已获批的 A1/B1/B2 美术派生方向 → 旧 Demo 与 History。

已发现并裁决一处制作层顺序冲突：已验收 Reader 明确为“取得重盾 → 挡下赤红冲击 → 最后应急车辆通过且撤离线清空 → 盾拍”。旧游戏流程/拓扑中“先清空撤离线，再取盾”的句子不得进入 Demo。此处只按更高权威 Reader 对齐，不改变故事，不需要再次请求用户决策。

## 3. 构建与存档身份

原位重基必须同时更新：

- `contract_revision=2`
- 新 `build_id`
- 新 `content_fingerprint`
- `save_schema=2`
- 新的 Current Candidate 存档命名空间或槽位版本

这只是同一 Demo 的内部身份换代，不是并行 v2 产品。旧存档因 schema、build 或 fingerprint 不匹配而 fail-closed；不迁移旧进度，不允许旧存档字段、旧地图 ID、旧 CP3 payload 或旧资产路径被兼容加载。

## 4. E02 的完整游玩结构

范围仍为 S01–S07，目标是可连续游玩的完整 E02，而不是只做一张战棋技术图。

1. 人类尺度完成观众撤离；观众进入避难所后退出巨机棋盘，但东门最后应急车辆仍在收尾。
2. 同体揭示、七海撤令、馆守 Z 起身；未获批的角色/头像资产只能使用具名占位，不得回退旧美术。
3. 进入大于视口的户外滚动战棋。道路、楼房、街区、破损连廊、警戒设施和可破坏物是棋盘世界层，不是固定棋盘外的前后景贴图。
4. 馆守 Z 站到 BREAKER 与东侧撤离线之间，同时牵制散乱小体、保护最后车辆。
5. 馆守 Z 取得退役重盾，挡下赤红冲击；最后车辆通过，`rescue_lane` 从 `active` 变为 `cleared`。
6. 满足站位、盾状态、撤离线和 Boss 重心条件后，玩家亲手确认一次性 `shield_bash` 情境动作。
7. 盾拍 Cut-in/静态回退与高潮台词播放后返回同一战场，BREAKER 首次倒地但未毁，小体仍有幸存者；以 E02 Phase Checkpoint 退出，不是 Mission Clear。

## 5. 战棋技术与玩法硬要求

- 户外地图必须大于单屏；光标或选中单位进入屏幕边缘阈值时平滑滚动，键盘、手柄和鼠标均不能丢失选中态。
- 室内战斗将来可使用固定地图；本 E02 户外战斗不得退回固定小棋盘。
- 单位层必须数据驱动，支持多格馆守 Z、BREAKER、多个 1 格小型突入体及非可控应急对象；具体 footprint 和小体数量仍为 Demo 平衡参数，不升 Canon。
- E02 小体组织态固定为 `scattered`：逐体追逐附近应急车辆、出口或警戒设施，不编队、不共享目标、不听从 BREAKER。`synchronized` 只允许 E03 首次出现。
- 全灭小体不是胜利条件；阶段出口至少保存一组幸存小体的 Stable ID、位置、状态和组织态。
- `rescue_lane` 是非可控保护状态，不把普通人或车辆变成玩家可操作战斗单位。
- `shield_bash` 不是常驻招式、练级技能或数值解锁；它只在本剧情条件成立时出现，执行后消耗本阶段一次性授权。
- 结算层先原子提交结果，演出播放器只读表现。Full/Skip、缺视频回退、退出重入及重复触发必须得到相同状态且只提交一次。
- 玩家失败可重试当前战棋阶段，不重播同体揭示、撤令和起身，也不污染正式章节或其他存档。

## 6. E02 Phase Checkpoint 最小状态

出口至少保存：

```text
operation_id=OP-C01-BREAKER
encounter_id=ENC-C01-GROUND
phase_id=P1
mission_clear=false
breaker_alive=true
breaker_first_knockdown=true
breaker_destroyed=false
retired_shield_acquired=true
red_impact_blocked=true
retired_shield_fourth_scorch=true
retired_shield_heat_deformed=true
retired_shield_penetrated=false
rescue_lane_cleared=true
swarm_organization_state=scattered
swarm_survivor_count=<positive integer>
swarm_survivor_positions=<stable serialized positions>
road_damage_state=<serialized>
building_damage_state=<serialized>
episode_boundary=phase_checkpoint
```

不得写 `episode_complete=true`、`mission_clear=true`、BREAKER 核心显形、飞行态、小体同步、馆守 Z 右臂毁损或 E03/E04 战后奖励。

## 7. 演出与资产调用

- 战棋常态使用 Q/SD 地图单位与轻量 Sprite 动作；地图必须首先服务可读性和操作。
- 取盾、挡击、盾拍等剧情动作可调用正比例 Pose、短 Cut-in、角色高潮台词及后续可选短视频；视频缺失时必须由静态分镜、镜头运动、FX 和音频完整回退。
- LibTV 不是本轮开工依赖。只有静态镜头本、占位合成和游戏返回连续性通过后，才单独向用户申请具体镜头与额度。
- A1 馆守 Z、B1 BREAKER、B2 重盾只批准作为继续派生的方向，仍为 Candidate、`runtime_allowed=false`；主程序本轮使用具名几何占位，不得直接接入这些图冒充 Runtime 资产。
- 旧头像、旧人物设计、旧馆守 Z/敌机图、旧 `story_first` 资产和旧 B3 地图均禁止自动 fallback。

## 8. 首轮并行目标与用户停止门

### 主程序 M2：滚动战棋与阶段状态闭环

先用具名几何占位原位重写 CP2 至 E02 Phase Checkpoint，完成滚动大图、动态单位、小体散乱 AI、撤离线、盾拍 Setpiece 播放器、存档身份和自动测试。此轮不以画面好看为完成条件，但必须交可操作构建、完整/跳过捕获、滚动边界捕获及状态回执。

### 美术 A2：滚动旧会展街区布局方向

先只做 2–3 套共用同一灰盒拓扑的方向板：道路与建筑入格、东侧撤离线、西北重盾位置、南侧 Boss 来向、多方向散乱小体压力、相机滚动范围和遮挡淡出。小体只用几何 token，不在本任务顺带决定其造型。用户逐项选择场景身份、战术可读性和遮挡原则后才开放下一项“小体 Q/SD 设计”。全部保持 Candidate、`runtime_allowed=false`。

以下事项必须停给用户：

1. A2 地图方向与遮挡方案；
2. 小体 Q/SD 身份和动作方向；
3. M2 战棋是否真的可读、可操作并有压力；
4. 任何玩法因果改变、人物/机体重设计、正式 Runtime promotion、批量生图或付费 LibTV。

## 9. 万机馆视觉基线边界

尚未制作的《万机馆空间与形态视觉基线 v1》不阻塞 E02 技术灰盒、滚动街区方向和本 Demo 的早期验证；但它继续硬阻塞 E04 正式美术/Demo、巡展舰正式资产及复杂馆体空间演出。旧万机馆移动底盘资产不得作为正式巡展舰母版。

## 10. 本轮完成定义

本轮只有在以下条件全部满足时才算完成：

1. 旧 Demo 没有第二入口、第二构建或可加载存档；revision 1 内容不能进入运行时。
2. S01–S07 可连续完成，E02 以 Phase Checkpoint 而非 Mission Clear 退出。
3. 户外战棋能滚动并将街区建筑纳入地图；小体、救援线和 Boss 同场成立。
4. 盾拍由玩家确认，短演出后回到同一连续战局；Full/Skip 和回退状态等价。
5. 没有旧头像、旧剧情、旧 B3、12x9 单 Boss 或 History 资产回流。
6. 自动检查、存档 fail-closed、确定性重放及真人试玩证据齐全。
7. 用户试玩后明确决定是否继续正式美术、LibTV 镜头与完整 E02 打磨；内部 PASS 不代替该决定。
