# C01E02 M3｜共同回合“原地换内核”制作人迁移合同

> 日期：2026-08-18  
> 状态：`Candidate production contract / user direction confirmed / no Canon or formal Runtime authority`  
> 适用范围：现有 C01E02 Candidate Demo 的战棋内核迁移  
> 不做：不改已验收 Reader，不改 Canon，不启动正式资产，不把 M3 结论外推为完整多机玩法已验证

## 1. 制作人结论

本次采用**原地换内核**：保留现有 Demo 的故事、地图、资产、镜头与产品闭环，替换“即时单机行动→敌方阶段”的战棋时制。

迁移分四段：

1. `R0`：独立但同项目的单轮共同结算沙盒；
2. `R1`：接通完整 E02 战斗并实证两条打法；
3. `R2`：在原入口内替换旧战棋核，接回存档、失败重试、Full/Skip 与 P1；
4. `R3`：玩法通过后才补声音、命中反馈、动作帧与高潮演出。

`R0` 不是第二个产品 Demo。它只是过渡期验证新内核的开发沙盒；当前默认入口继续运行 M2.5。只有 `R1` 通过制作人与用户试玩门后，才允许在同一 Runner 中切换内核，并在切换后停止维护旧即时制。

## 2. 权威与冻结输入

### 2.1 玩法方向

- `docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/00c-core-game-design-master-review.md`
- SHA-256：`eadd8add793eced85bdd1fa7b2a56566bc17ba8bb586069b96e9644e9345899a`
- 权威边界：`Candidate / user_direction_approved / no_Canon_or_Build_authority`

本合同只把 00c 的共同回合语言落到 C01E02 Candidate；不授权五张人物牌、气势、正式请战、Meta、LLM、Hub 经济或长期成长。

### 2.2 已验收故事

- Reader：`docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C01-闭馆以后万机出击.md`
- Reader SHA-256：`c9a9aa490badea3d2de937e0003b80547974fed27103b31ec9181cd3583cfc8b`
- 用户回执：`docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C01/C01-用户创作验收回执.md`
- 回执 SHA-256：`3d11387d92120cfdeeb0069a2a7cdfbe677ed0ea2ac5ae6649038de7b0cd532b`

不可删改的 E02 顺序是：

1. 应急车辆先通过馆守 Z 的落脚区；
2. 馆守 Z 横腿挡开扑向东门的小体，站到撤离线与 BREAKER 之间；
3. 馆守 Z 与 BREAKER 首次正撞、被推出并迫使其改线；
4. 馆守 Z 取得退役重盾；
5. 重盾挡住赤红冲击，最后车辆与架桥机完成撤离；
6. 馆守 Z 以盾拍使 BREAKER 首次倒地但未毁；
7. 小型突入体仍有可见幸存者且保持散乱；
8. 结果停在 `OP-C01-BREAKER / ENC-C01-GROUND / P1`，不是 Mission Clear。

### 2.3 现有 Demo 基线

- 原合同：`19-current-demo-inplace-rebase-producer-contract.md` @ `6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94`
- M2.5 完成回执：`main-m2-5/05-completion-report.md` @ `437fd3aa0d50260c843e2b7eb1d9f8bedf8f6721bcd1285fe095c5a84c30eb29`
- U1／U2／U3／U4 回执分别为：
  - `1ec66ec6c286db2058222d999cb326b3108e3d0c26782caad2c0ca4ba8803a79`
  - `4320c77ed03170aa243f41fc121fa2b9922dd70dcf8216c6aa9cba6d3ea643da`
  - `ebff38b7e4c4269a15a6fa26144a909d5d0424bf41947dcce2b9ac81a8de86b1`
  - `b5ea24f0967a6cb277eeadfc1d0953e448466947e978df36fd513738276ae2df`

19 号合同继续约束故事结果、地图、单位、P1、失败重试、Full/Skip 和隔离边界；其中“即时移动／动作、再按 E 进入敌方阶段”的玩法语义，由本合同在 M3 Candidate 内替代。

现有 M2.5 仍是迁移期间最后一个可完整运行的 Candidate 基线；它的 PASS 不等于 M3 已完成。

## 3. M3 身份与生命周期

| 项 | 值 |
| --- | --- |
| 迁移族 | `C01CDV1-M3` |
| R0 构建标识 | `C01CDV1-M3-R0-SANDBOX` |
| R0 战术配置 | `c01cdv1_e02_shared_round_m3_r0` |
| 正式接回时的存档 schema | `3`（R0 不写正式存档） |
| 正式接回时的存档 namespace | 必须与 M2-R2 隔离，具体稳定名留给 R2 合同 |
| 生命周期 | `Candidate` |
| 默认入口 | R0 期间仍为现有 M2.5 Current Demo |
| Runtime／Canon | `not authorized` |

R0 只允许测试态快照；不得写入现有 Candidate 正式存档。R2 接回时，旧 M2-R2 战术中存档必须 fail-closed 并安全回到 CP2，不做逐字段猜测迁移。

## 4. 新共同回合的规范合同

每轮必须依次经过：

1. **局势公开**：敌方真实计划在玩家编辑前冻结；显示可合法观察到的 BREAKER、小体、车辆与环境下一轮变化；
2. **计划编辑**：为每台直接控制机记录短路线、终点朝向、一个主动作或一条预备反应；E02 当前计划数组长度为 1；
3. **提交摘要**：显示接触、争格、保护对象、触发条件、备用方案和未覆盖风险；摘要不锁定，可以返回修改；
4. **执行本轮**：长按唯一提交键后锁定；敌人不得读取草稿或在看见局部结果后改计划；
5. **轮末结算**：单位、任务对象与环境从同一轮前态结算，公共任务与环境只推进一次，然后敌方再规划下一轮。

实现状态必须保持单向：

```text
ROUND_START_SNAPSHOT
→ PUBLIC_SITUATION
→ EDITABLE_DRAFT
→ COMMIT_SUMMARY
→ COMMITTED_PLAN
→ JOINT_RESOLUTION
→ ROUND_RESULT
→ NEXT_ROUND
```

强制语义：

- 编辑、预览、撤销不得改变世界状态或确定性签名；
- 路线与终点朝向必须独立，移动不能偷偷代替朝向选择；
- 主动作与预备反应二选一；预备必须有 `trigger → response`，每轮最多触发一次，未触发则轮末失效；
- **备用方案不是预备反应**：它只在前置接触令后续路线／动作不再合法时使用，必须提交前公开，不赠送额外行动；没有备用时停在最后合法状态；
- 同一时点的接触从共同前态组成接触组，不得按单位 ID 顺序逐只抢占结果；
- 摘要和执行必须调用同一套 resolver；不能维护两套因果；
- 不限制玩家现实思考时间；等待只表示放弃本轮动作，世界仍在提交后推进；
- 每条公开意图的数据合同至少保留 `confirmed / estimated / unknown`、动作类型、目标实体／区域、预计生效时点、信息来源和有效时间；R0 只实际作者化诚实的 `confirmed` 意图，不提前引入复杂未知分支；
- 规划辅助最多解释合法起手与代价，不得移动光标、自动填完整方案或替玩家执行。

轮回执至少记录：`round_id`、`round_start_hash`、`public_intent_hash`、`committed_plan_hash`、`timeslice`、`prestate_hash`、`contact_group_id`、`prepare_triggered`、`fallback_taken`与`round_result_hash`。

## 5. C01E02 的证据边界

M3 E02 可以证明：

- 单机路线、朝向、主动作／预备、摘要、提交与共同结算语言；
- 公开威胁、身体占位、保护、非歼灭目标和确定性重放；
- 同一 Reader 结果下两条有真实代价的战法。

它不能证明：

- 多机编辑负担、友军争格、跨机反应链与行动交接；
- 五张人物牌、共同动词、正式气势／请战／让台；
- 3—5 机常规阵容或四种战斗家族均已成立。

最早的双机 Candidate 验证留给 C01E03 馆守 Z 与勇拳自然同场之后；不得向 E02 凭空加入第二台直接控制机。完整 3—5 机证明另立后续目标。

## 6. 两条打法与固定汇合

R1 必须实测而不是书面宣称：

- **快取盾**：更早进入挡击准备，回合余量较大；代价是撤离侧的非关键设施或小体压力更高；
- **先守撤离线**：多投入一轮保护／预备，减少设施损失；代价是 BREAKER 推进更深、馆守 Z 承力更高或后续容错更低。

两路至少在非关键设施状态、小体落位、馆守 Z 承力、剩余轮次或战报评价之一产生可见且由因果导致的差异。不得只换结算文案。两路都必须在 P1 前汇合，不改变第 2.2 节的固定事实。

若当前地图锚点、车辆时序和公开截止无法同时容纳两路，R1 允许调整 Candidate 战术锚点与公开时窗；不得修改 Reader 或伪造第二解。

## 7. 盾拍分类

E02 盾拍是**基础战中的剧情动作窗口／焦点机会预演**，不是 00c 正式焦点战：

- 不接气势条、不生成正式请战、不运行五牌；
- 必须由持盾、已经挡过赤红冲击、撤离线清空、BREAKER 处于偏轴／重心恢复窗口、馆守 Z 的接触位置与朝向共同形成；
- 进入正常计划、提交摘要与共同结算，不得由进度清单自动点亮后脱离回合系统执行；
- R0 不实现盾拍。

## 8. 复用、重绑定与暂停

### 8.1 继续复用

- 32×18 地图、2×2 馆守 Z、3×3 BREAKER、散乱小体、车辆、撤离线与非关键设施数据；
- 等距坐标、滚动相机、边缘阈值、光标、footprint、通行与寻路纯逻辑；
- Candidate 隔离、原子状态提交、失败从 CP2 重试、Full/Skip 同结果与 P1 外壳；
- A4 五张地图资产、A5 96px 四朝向母版及其用户批准。

### 8.2 必须替换或重绑定

- 即时 `move/acquire/intercept/brace/end_player_turn` 状态机；
- 自动朝向、顺序小体结算、轮转式无因果环境损坏、唯一黄金路线推荐、清单式盾拍；
- 旧即时制测试与捕获；
- M3 接回时的 build、fingerprint、profile、存档 schema／namespace；
- A4/A5 像素不重做，但其旧 build/fingerprint 绑定须在 R2 做最小技术重绑定。

### 8.3 立即暂停

- 围绕旧“下一步／E 敌方阶段”的 U5 类 UX 与平衡；
- 为旧即时击退、立盾和固定五回合路线制作动画、声音或视频；
- A4 动态 STATE_LAYERS、馆守 Z、BREAKER、盾牌的下一轮正式接入；
- LibTV 盾拍视频与最终 HUD；
- 正式 Runtime／Canon promotion，以及五牌、气势、Meta、LLM、Hub 经济。

## 9. 四阶段用户门

| 阶段 | 可试玩停止点 | 未经确认不得继续 |
| --- | --- | --- |
| R0 | 单轮沙盒：草案可改、摘要可退、一次共同执行 | 不进入完整 E02 |
| R1 | 两条打法均到同一 P1，真实代价不同 | 不切默认入口 |
| R2 | 从开场完整玩到 P1，存档／重试／Full-Skip／A4-A5 恢复 | 不启动正式表现资产 |
| R3 | 命中、声音、动作与 Cut-in 联合验收 | 不升正式 Runtime／Canon |

重大玩法归属、Reader变化、正式资产、付费批量生成、默认入口切换和 Runtime／Canon 晋升都必须停下交用户确认。

## 10. 当前授权

本合同授权制作人编写并派发 `R0 单轮共同结算沙盒`任务书。它不授权 R1、R2、R3 自动开工，也不授权主程序修改当前默认 Runner、现有 tactical session、正式存档或资产绑定。
