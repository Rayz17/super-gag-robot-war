# D06 C02E04–E05 赛事／事故纸面 Fixtures v0.1

> Status: `candidate_chapter_paper_fixtures / accepted_story_fixed / static_contract_only_except_match_contact_math / zero_build / human_not_run / user_review_required / gd2_blocked / no_runtime_authority`
>
> Scope: 只补齐 C02E04 固定 `0:2 → 3:2` 的玩家过程、E04 事故持续 Checkpoint，以及 C02E05 三阶段救援到 Accident Mission Clear 的可否证纸面实例。
>
> Boundary: 不改 Reader、Canon、story-chain、Runtime、Demo 或正式资产；不把本件的区域、数值、时序或策略当成已验收设定。

## 0. 权威锁与使用边界

### 0.1 本件不得改写的事实

| 字段 | 锁定值 |
| --- | --- |
| `story_binding_id` | `ASB-C02-20260806-56827053` |
| 已验收章 Reader | `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C02-章节连续阅读稿.md` |
| Reader SHA-256 | `56827053dcf5e17922b143acbcb99457b284080dcef041d1d6be58880f6e03a1` |
| E04 组件 SHA-256 | `7ef2c51975b5438f3ca1f8fbea5d4b710ec7ea63d9ab770205a6493f1b51f6bc` |
| E05 组件 SHA-256 | `4f0931cdeec7beb4ca5b0addb1eccd3785cd2d8ad02bc0ca863de9c67d94b930` |
| 用户验收回执 | `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C02/C02-用户创作验收回执.md` |
| 回执 SHA-256 | `dc5e2e50a7c07d7aec36ad84cc40146a90aab30d43787a2c5364effd57738392` |

下列为 `hard story guards`，玩法不得用分数、失败、隐藏分支或人工补丁改写：

1. 无牌一号在事故发生前已以 `3:2` 赢得木桶杯；事故不计分、不重赛、不改冠军。
2. 前两分归完全版王者；无牌一号连追三分。第三分用正面承力的逆转天冲拳，第四分用推进横移、贴身抢位与五秒压制，第五分在王者正拳交锋后主动踏入并逆转。
3. E04 事故发生时，完全版王者仍带全装；一条腿和一片外翼被卡，舞台炮已断电但仍下滑。
4. 白鸢按下停止，本地裁判／安全席断电；七海只能远程问人数与伤员，不远控木桶街。
5. 普通观众已在固定观景厅；外圈只有最后一组工房人员需撤出。
6. E04 只到事故 Checkpoint：人员撤出，两机仍顶炮，万机馆只接住临海外缘，火种货柜领袖与地面车队仍在牵引。
7. E05 必须保留红机过热、蓝机护送、黄机按已固定的两索切断两根支架，以及万机馆／货柜领袖／馆守Z／旧拳王的承重链。
8. 完全版王者本人决定卸装；装备仍归原主。无牌一号与王者最后把断电舞台炮送回拆解架，环停止下沉。
9. 救援后的新旧转子、推进模块归还、登舰／留街和不停机直达工务城属于后续 `Departure / Chapter Settlement`；事故战术结算不得抢先提交。

### 0.2 设计推测的显式标记

本件凡出现 `INF-C02-*` 均是为了让纸面规则可计算而新增的 Candidate 推测，不是 Reader 事实。

| inference_id | Candidate 推测 | 为什么现在不能当设定 |
| --- | --- | --- |
| `INF-C02-01` | 决赛前两分用透明的 Story Showcase，`0:2` 后才开放完整战术输入 | 尚无用户玩法裁决与可用性证据 |
| `INF-C02-02` | 决赛用八节点逻辑区域图，事故用十一区持续图 | 货运环 GD2 尚无平面、剖面与承重真值 |
| `INF-C02-03` | 单体质量、力、稳定、应力、热量使用 0–4 整数带 | 只是 D04 结算核的章内 seed values |
| `INF-C02-04` | 每个阶段有南／北线或承力／机动两类局部策略 | 尚未经规则搜索或玩家独立发现 |
| `INF-C02-05` | 环应力、炮车下滑与支撑余量有离散阈值 | 必须由 GD2 结构档案和低模动作回算 |
| `INF-C02-06` | `withdraw` 为显式交回故事承载；`fail_continue` 只回滚至稳定检查点 | 尚无失败体感与可理解性测试 |
| `INF-C02-07` | `partial` 产生的额外负担只在同一事故 Operation 内继承 | 防止临时玩法债务反向污染 C03 |
| `INF-C02-08` | 三飞行机、货柜领袖和本地机的操作是具名请求／支援实例 | 不生成长期召唤菜单或永久入队 |

### 0.3 证据级别，不把静态合同称作物理解算

| fixture_id | `recompute_level` | 当前机器实际能证明 | 当前不能证明 |
| --- | --- | --- | --- |
| `FX-D06-C02E04-MATCH` | `static_contract_plus_match_4_contact_equations` | Story 字节、summary/carry、账本引用、行动窗，以及四条接触差值算式的静态重算 | 完整比赛 resolver、AI、多解可达、平衡、体感 |
| `FX-D06-C02E04-ACCIDENT-CP` | `static_contract_only` | 固定出口、区域／行动／事务／请求回执合同的机器结构校验 | 撤离路线与结构载荷的物理可达性 |
| `FX-D06-C02E05-RESCUE-CLEAR` | `static_contract_only` | 三阶段顺序、状态域、装备／权限／同意／事务合同的机器结构校验 | 逐窗数值 delta、承重 resolver、设施 Boss 物理、多解可达 |

因此本件是“三个机器可校验纸面合同”，不是“三个物理可重算 Fixture”。只有 MATCH 表内四条接触式可以静态重算；E04 事故与 E05 救援在 GD2、身体包和 resolver 完成前一律保持 blocked。

## 1. 共用语义核

### 1.1 与 D04 共用的规则

- 执行窗按 `8.0s`、因果日志按 `0.5s` 精度写纸面 Trace；这不表示 Scheduler 已定案。
- 表中窗数只计玩家需要提交的执行脉冲；两窗之间可有故定的安全等待、人员作业或 Story Cut-in。不得由窗数倒推整场比赛／救援只花了几十秒；叙事总时长待 GD2 与 Previs 校验。
- 每个身体每窗只有一条 `TACT_ROUTE`、一个主动作和一个已预留的反应／安全条件。
- 章内具名动作不得创造第二套物理核，必须展开为 `TACT_INSPECT / ROUTE / BRACE / WAIT_CONDITION / MELEE / RANGED / PUSH_TOW / COUNTER / COVER / ABORT / RESCUE / INTERACT / SCAN_LOCAL`。
- 已知条件下无隐藏命中率、暴击或加载顺序。结果由 D04 的同刻接触、位移差值和功能差值解算。
- 完全版王者的 Boss Intent 必须有物理承诺窗；事故环境的下滑／断裂为可见 Hazard Forecast，不伪装成敌人 AI。
- 自主机体的支援是 `request → response → body action`，不是玩家取得所有权、驾驶权或永久服从。

### 1.2 本件的四种结果语义

| result | 精确语义 | 故事固定结果怎样处理 |
| --- | --- | --- |
| `clear` | 玩家用当前规则完成 Primary，且不触发该 Fixture 的额外负担带 | 由玩法 receipt 与 hard story guard 一起 prepare |
| `partial` | Primary 已成，但一个公开的临时应力／过热／额外支撑债务带入同 Operation 下一阶段 | 不得改变 `3:2`、人员安全、卸装同意或事故最终出口 |
| `withdraw` | 玩家在稳定点明确选择“交回故事承载”；当前局不算 Gameplay Clear，不给伪成绩 | 单独读取已验收故事出口，并记 `gameplay_resolution=withdraw_to_story` |
| `fail_continue` | 提案会越过安全阈值时，拒绝该事务并原子回到最近 Checkpoint；不将灾难出口写入世界 | 重试或改选 `withdraw`；不用“剧情无敌”偷交 Primary |

`fail_continue` 不是将已坍塌的世界倒带后宣称成功；它只是未提交的危险方案校验失败。任何已 accepted 的位置、伤损、设备和知识都不得因重试而被治愈或删除。

### 1.3 事务与存档

- 每个 Checkpoint 使用一个 `transaction_id + payload_hash`；同负载重放 1000 次只返回同一 receipt，状态版本只 `+1`。
- 任一 Owner prepare 拒绝，整组身体、位置、资源、同意、比分和故事提案 `0 write`。
- `Phase Checkpoint` 不发奖、不治疗、不刷新空间；`Tournament Mission Clear` 与 `Accident Mission Clear` 必须分开结算。
- Full / Skip 演出、键鼠／手柄、帧率、存档重载只能改变投影，不得改 `state_hash / receipt_hash / event_queue`。

### 1.4 Story seed、事务追踪与状态域统一账

本件不新造一份章末事实。每个 Fixture 都绑定 `chapters/c01-c03-story-state-seeds.tsv` 的既有 checkpoint 投影，并与 `data/opening-state-transaction-paper-trace.tsv` 的事务行使用同一组状态域。分号串是机器账 canonical value；checker 按集合精确比较，不按“差不多包含”放行。

| fixture_id | story_seed_guard_id／只读投影 | transaction_trace_id | canonical `state_domains` | 域边界说明 |
| --- | --- | --- | --- | --- |
| `FX-D06-C02E04-MATCH` | `C02E04_END:tournament_projection` | `OST-04` | `ST_RESULT;ST_BODY;ST_LOCATION;ST_EQUIPMENT;ST_OPERATION;ST_RELATION;ST_ENEMY_LEARNING` | `ST_LOCATION` 保存每分位置／朝向与复位；`ST_EQUIPMENT` 保存借用推进模块和王者全装的唯一实例连续；`ST_RELATION`／`ST_ENEMY_LEARNING` 只接固定的冠军标交接、可见适应与再战回应 |
| `FX-D06-C02E04-ACCIDENT-CP` | `C02E04_END:accident_checkpoint_projection` | `OST-05` | `ST_BODY;ST_LOCATION;ST_EQUIPMENT;ST_KNOWLEDGE;ST_RESOURCE;ST_CONSENT;ST_RESULT;ST_OPERATION` | `ST_EQUIPMENT` 保留推进模块／全装的 owner、version、custody、installed state；`ST_CONSENT` 保存无人机、杰克、货柜领袖逐动作回应；支援分配不改成员关系，故禁止 `ST_ROSTER` |
| `FX-D06-C02E05-RESCUE-CLEAR` | `C02E05_END:accident_clear_projection` | `OST-06` | `ST_BODY;ST_LOCATION;ST_EQUIPMENT;ST_RESOURCE;ST_KNOWLEDGE;ST_AUTHORITY;ST_CONSENT;ST_RESULT;ST_OPERATION` | `ST_AUTHORITY` 保存资产优先撤销与承包商动作级解锁；`ST_CONSENT` 保存王者和所有自主支援的请求／回应；`ST_EQUIPMENT` 保存卸装前后唯一实例链；不生成关系许可或成员变化，故无 `ST_RELATION/ST_ROSTER` |

`C02E05_END` 同一 seed 行还包含新旧转子、随舰／留街和工务城航向，但本 Fixture 只读其中的 accident-clear projection；不得因为 seed 的章末事实已存在，就让 `TX_C02E05_ACCIDENT_CLEAR` 抢写 Departure 域。反过来，E04 Checkpoint 的 `ST_OPERATION`、路线知识和资源负担也不得因它不是 Mission Clear 而漏存。

### 1.5 装备、动作权限与自主支援的机器账

- `data/c02-paper-equipment-state-ledger.tsv` 逐实例保存 `owner / owner_version / custody / installed_state / condition`，覆盖借用推进模块及王者背炮、长翼组、盾组、钻进组、头冠。纸面 instance ID 是 Candidate 账键；装备归属、卸装与本地维护出口仍由 Accepted Story 固定。
- `data/c02-action-authority-consent-paper-ledger.tsv` 将胶价王撤销资产优先、承包商当值维护员限本次救援确认解锁写入 `SOG-C2 / ST_AUTHORITY`，并将每个自主机体支援写成 `request 或 story-bound precommit → response_state/conditions → body_action → receipt → withdrawal/expiry`。
- 玩家只选择路线、焦点、时机、支援分配或中止条件；不得出现“按 Blue／Jack／Yellow／货柜领袖／馆守Z／旧拳王按钮即服从”的直接控制。Accepted Story 固定某一身体动作时，账本把它记为 `accepted_precommitted_story_event`，主体仍有可见 response state，玩家不重投其主体决定。
- 任一装备实例缺 `owner/version/custody/installed_state/condition`，或 E05 自主卸装缺 `AUTH_C02E05_ASSET_PRIORITY_REVOKE → AUTH_C02E05_CONTRACTOR_DETACH_UNLOCK` 的有效动作范围与版本，相关 Owner prepare 必须拒绝，事务整组 `0 write`。

## 2. `FX-D06-C02E04-MATCH`：0:2 之后的三分逆转

### 2.1 玩家边界裁决

`INF-C02-01` 选择下列候选承载：

1. `0:0 → 0:1`：短 Story Showcase，展示彩烟逼位、长翼跟进、双盾把无牌一号推出白线。
2. `0:1 → 0:2`：短 Story Showcase，展示钻进假动作、无牌一号让位、王者肩撞及双盾压制五秒。
3. 记分板到 `0:2` 后，才出现完整战术规则、可编辑路线、反应槽和结果预览。

前两分可暂停、查看 Intent 与力线，但不出现伪路线、伪攻击按钮或“无论怎样都输”的隐藏操控。如果日后要把前两分也变成完整战术，必须重开本 Fixture：要么允许真实改写比分并迁移故事，要么明确将每分设为可重试的成功门；不得同时宣称“完全可玩”与“必定被强制失分”。

### 2.2 精确初态与逻辑地图

`SAVE_C02E04_SCORE_0_2` 为第一个玩家可控存档点：

```text
D06C02v0.1|fixture=FX-D06-C02E04-MATCH|score=0:2|point=3|no_name=arena_west,arm_stress1,thruster1|full_king=arena_east,full_loadout|ring=locked|rotor=isolated|people=fixed_viewing_hall|result=pending
```

`paper_summary_sha256 = 6bf863b702838788ec44eb374a23765aaf27c675f55b290f0a18812ed7d0945b`

纸面解算只使用对称节点图，不假装已有精确米数：

```text
                  N2(edge)
                     |
W2(edge) - W1(inner) - C0 - E1(inner) - E2(edge)
                     |
                  S2(edge)

OUT 与 N2/E2/S2/W2 分别相邻；整机进入 OUT 得分。
每分复位时：NO_NAME=W1 facing E，FULL_KING=E1 facing W。
```

| 主体 | 初态带 | 可用动词／禁止 |
| --- | --- | --- |
| `BODY_NO_NAME_01` | `mass3; stability1; support1; mobility2; right_arm=2; left_arm=2; right_arm_stress=1; borrowed_thruster=normal,charge1` | `ROUTE/BRACE/WAIT/MELEE/COUNTER/ABORT`；借用推进只能在第四分用一次 |
| `BODY_FULL_KING` | `mass4; stability2; support1; mobility2; shield2; wing2; cannon2; drill2; base_body2` | 按具名 Intent 执行；不读玩家隐藏路线；E04 不允许卸装 |
| `ARENA_CARGO_RING` | `locked; white_line=active; live_ammo=locked; people_on_ring=two_mecha+referee+required_staff` | 只有出界或压制五秒得分；冠军转子与擂台有实体防护隔离 |

计分复位只重置位置、朝向和当分 Intent；`right_arm_stress / heat / system_state / thruster_charge` 持续。

三次得分接触使用 D04 唯一位移公式，不为本章改变参数含义：

| contact_id | 接触初态／动作声明 | `force + momentum + source_support - target_mass - target_stability - target_support` | 可重算结果 |
| --- | --- | ---: | --- |
| `CONTACT-P3-REVERSE` | 王者冲入 `W2` 且离地；无牌一号从已承力接触弧以 `force4/momentum1/support1` 向最近白线外执行上击；王者为 `mass4/stability0/support0` | `4+1+1-4-0-0=2` | 沿已声明的外向弧从 `W2` 进 `OUT`；得第三分，右臂应力 `1→2` |
| `CONTACT-P4-TOPPLE` | 双方在 `C0` 近身；无牌一号以 `force3/momentum2/support1` 顶翻；王者肩部已承诺、`mass4/stability0/support0` | `3+2+1-4-0-0=2` | 王者移到一个相邻内圈节点并失稳，不出界；本窗不得分 |
| `CONTACT-P4-PIN` | 王者起身为 `force3/momentum0/source_support0`；无牌一号压翼后为 `mass3/stability2/support2` | `3+0+0-3-2-2=-4` | 五秒内不位移；第四分只在 5s 计时完成后提交 |
| `CONTACT-P5-REVERSE` | 双方在 `C0` 对冲；无牌一号先踏入，以 `force4/momentum2/support1` 向王者后方白线执行上击；王者正拳承诺后为 `mass4/stability0/support0` | `4+2+1-4-0-0=3` | `C0→E1→E2→OUT`；得第五分，右臂应力 `2→3`、功能 `2→1` 但仍可用 |

上表的外向弧、节点和整数带全属 `INF-C02-02/03`。它们使纸面结果可重算，但不是格数、米数或平衡结论；GD2 一旦给出真实半径、白线与动作包络，必须重新求解而不是只刷新 hash。

### 2.3 八个玩家行动窗

| 窗 | 王者公开 Intent | 玩家必须解决的问题 | 固定故事接触 | 不同的局部选择 |
| --- | --- | --- | --- | --- |
| `P3-W1` | `KING_SHIELD_WALL_COMMIT`：双盾并拢，4–6s 正面压进 | 在 W1/W2 之间设承力点或受控后退，预留 `COUNTER` | 无牌一号左臂承力，右拳收紧 | `BRACE@W1` 或 `ROUTE W1→W2 + WAIT` |
| `P3-W2` | 盾墙进入接触弧且王者离地，`stability/support=0/0` | 使用已预留的 `TACT_COUNTER` | 逆转天冲拳把王者轰出白线，`1:2` | 接触方向可为中路或偏北，不改变动作主体 |
| `P4-W1` | `KING_SMOKE_ZONE + SINGLE_CANNON_SHOT`：烟区、一发炮、不主动送冲力 | 用唯一次短横移从烟区侧面进入 | 推进模块喷出尾焰，无牌一号撞入王者怀中 | 北侧空隙或南侧炮冷却窗 |
| `P4-W2` | `KING_SHOULDER_COUNTER` 在近身后承诺 | 左肩承受反击，右臂从盾下穿入，以一个 `TACT_MELEE` 完成顶翻 | 王者被送翻在地，但尚未得分 | 玩家选先占内侧再顶，或用更大右臂应力换更好压制朝向 |
| `P4-W3` | 王者用长翼尝试撑起，其起身时间公开 | 左臂压住一片长翼，用一个完整 `TACT_BRACE` 保持 5s；右拳只停在胸甲上方 | 五秒到才提交第四分，`2:2` | 可在北／南支撑面间选更稳定的一侧；不允许在同窗再攻击 |
| `P5-W1` | `KING_SHIELD_DISC_BLOCK_N_S + COLOR_BARRAGE_CENTER + DRILL_LOW` | 不使用已耗尽的横移，从中路进入并保持右拳反应槽 | 无牌一号左肩中弹、右腿被钻进擦过 | 穿彩烟中轴或利用一面滑盾后的短空窗 |
| `P5-W2` | `KING_STRAIGHT_PUNCH_COMMIT`：王者收炮并正面冲出 | 不后退等待，把右脚先踏入王者两脚之间 | 王者正拳先落在无牌一号左臂 | 较早踏入保稳定，或较晚踏入换更高臂应力 |
| `P5-W3` | 王者进入接触，`stability/support=0/0` | 触发 `TACT_COUNTER` 并完成收招 | 第二步逆转天冲拳把王者轰出，`3:2` | `TACT_COUNTER` 内附的安全中止条件可降低越界风险，不额外占第二反应槽、不产生第二次攻击 |

所有“逆转天冲拳”都展开为 `TACT_ROUTE/BRACE/WAIT_CONDITION + TACT_COUNTER/MELEE`，不是一个无视位置、时间和承力的剧情必杀键。

### 2.4 两个预计策略族

| strategy_id | 第一个不同行动 | 路线／承力分工 | 公开代价 | 共同固定出口 |
| --- | --- | --- | --- | --- |
| `MATCH-S1-ANCHOR_READ` | `P3-W1 BRACE@W1` | 较早承力，P4 走北侧烟隙，P5 较早踏入 | 左臂和右臂应力更高，热量较低 | `3:2`，王者全装，无牌一号右臂可用但明显受损 |
| `MATCH-S2-MOBILITY_PROVOKE` | `P3-W1 ROUTE W1→W2 + WAIT` | 受控后退换王者更长承诺，P4 走南侧冷却窗，P5 较晚踏入 | 稳定与热量代价更高，右臂应力较低 | 同左 |

策略族只是纸面可达假设。程序搜索若只找到一个严格点击序列，本 Fixture 失败；不得把上表当成“作者已走通两解”。

### 2.5 结果、事务与出口

| result | 规则条件 | 事务处理 |
| --- | --- | --- |
| `clear` | P3/P4/P5 三张得分 receipt 齐；两机未进入禁止攻击区；右臂仍可执行一个安全接触 | `TX_C02E04_POINT3/4/5` 顺序提交，再 prepare `TX_C02E04_TOURNAMENT_CLEAR` |
| `partial` | 三分仍由规则完成，但 `arm_stress` 或 `thruster_heat` 进入公开重负担带 | 仍为 `3:2`；负担只进 E04 事故初态，不生成永久数值成长 |
| `withdraw` | 玩家在分数 Checkpoint 显式交回 Story | 不生成 Gameplay Clear；已验收 Story 单独投影 `3:2` |
| `fail_continue` | 无预留反应、已知线区违规或应力越界 | 该分 `0 write`，回当分复位点；前面已得分和伤损不回滚 |

| 稳定边界 | 事务 | 存档 | 必须保存 |
| --- | --- | --- | --- |
| 第三分完成 | `TX_C02E04_POINT3` | `SAVE_C02E04_SCORE_1_2` | `score=1:2`、两机身体／热量，推进充能仍在 |
| 第四分完成 | `TX_C02E04_POINT4` | `SAVE_C02E04_SCORE_2_2` | `score=2:2`、五秒压制 receipt、推进已用一次，累计臂应力 |
| 第五分完成 | `TX_C02E04_POINT5` | 尚不单独结算 | `score=3:2`、出界接触、收招后身体态 |
| Tournament Clear | `TX_C02E04_TOURNAMENT_CLEAR` | `SAVE_C02E04_TOURNAMENT_CLEAR` | 三张得分 receipt、固定冠军、王者全装、比赛伤损；不含事故结果 |

上述 MATCH 存档精确保存 `ST_RESULT / ST_BODY / ST_LOCATION / ST_EQUIPMENT / ST_OPERATION / ST_RELATION / ST_ENEMY_LEARNING`。每分复位只对 `ST_LOCATION.position/facing` 写新值，不删除此前位置 receipt；借用推进模块和王者全装按 `data/c02-paper-equipment-state-ledger.tsv` 的 owner/version/custody/installed state 连续保存，不能用“比赛复位”重生装备或归还推进模块。

Tournament Clear 摘要：

```text
D06C02v0.1|fixture=FX-D06-C02E04-MATCH|score=3:2|winner=no_name|full_king=full_loadout|right_arm=stressed_functional|thruster=used_once_attached|tournament=clear|accident=not_started
```

`paper_summary_sha256 = c462760028fcd56cec981d54a01090656ded5f151923cdd7924bfcced2d1d1fd`

Future consumer 为 `FX-D06-C02E04-ACCIDENT-CP`。Tournament Settlement 必须先封存 `score=3:2`、比赛伤损和推进模块仍附着，随后才允许故事地图开始；不回 Hub，不治疗。

## 3. `FX-D06-C02E04-ACCIDENT-CP`：人员撤出与持续地图

### 3.1 精确初态

```text
D06C02v0.1|fixture=FX-D06-C02E04-ACCIDENT-CP|score=3:2|outer_rail=broken|full_king=leg_and_one_wing_trapped,full_loadout|no_name=supporting|stage_cannon=powered_off_sliding|workshop_group=outer_ring|wanji=workroad|cargo_leader=ready_tow
```

`paper_summary_sha256 = 0e8e88e1ca59440baf3b9bad7145d0584f76247bf8dd7854ef30d37a8c84b38e`

| 区域 | 初态 | 连接 |
| --- | --- | --- |
| `A-CONTROL` | 白鸢已停演；本地安全席已断电；纪存／白鸢按现场工作人员指引撤往内环 | `A-INNER-SAFE` |
| `A-INNER-SAFE` | 赵梅点名工位；不含普通观众棋子 | `A-LINK-N;A-LINK-S;A-WORKROAD` |
| `A-LINK-N` | 较短，每窗边缘下沉预测更高 | `A-WORKSHOP-OUTER` |
| `A-LINK-S` | 较长，轻板滑落更多，但地面承重较高 | `A-WORKSHOP-OUTER` |
| `A-WORKSHOP-OUTER` | `GROUP_LAST_WORKSHOP` 等待撤出 | `A-LINK-N;A-LINK-S` |
| `A-SEASIDE-SLOPE` | 王者腿／翼被卡；无牌一号支撑；断电炮下滑 | 不是人员撤离线 |
| `A-WORKROAD` | 万机馆在船台托架；货柜领袖与地面车队可沿现有直线牵引 | `A-WANJI-EDGE` |
| `A-WANJI-EDGE` | 只允许接住下沉外缘，不允许万机馆飞起或托整环 | `A-SEASIDE-SLOPE` |

Hazard Forecast：`ENV_LIGHT_PANEL_SLIDE` 指向撤离线；`ENV_CANNON_SLIDE` 只指向两机和临海侧；`ENV_EDGE_SETTLE` 每窗更新两条 Link 的可走投影。三者都必须显示来源与时间，不能突然换区。

### 3.2 行动窗与两类路线

| 窗 | 玩家动词 | 现场主体动作 | 稳定输出 |
| --- | --- | --- | --- |
| `A-W1` | 选择扫描焦点／路线；提交 `REQ_C02E04_DRONE_HAZARD_SCAN`，不可直接操纵无人机 | 无人机组返回 `CONSENT_C02E04_DRONE_HAZARD_SCAN` 后沿外圈扫描，只把红光投在无人危险区 | 两条路的当窗风险可见；白鸢不生成精确未来 |
| `A-W2` | 选择 N/S Link；提交 `REQ_C02E04_JACK_EVAC_COVER` 并保留 `ABORT` | 杰克按自身安全条件回应后放低两条装卸臂，为最后工房组挡住轻板 | 工房组进入选定 Link；杰克臂应力和撤回条件公开 |
| `A-W3` | `ROUTE / ABORT / open_passage`；提交 `REQ_C02E04_CARGO_EDGE_TOW` | 货柜领袖回应后与车队拖近万机馆；工房组到内环；两台决赛机仍顶炮 | `people_evacuated=true; inner_passage=open; cannon_sliding=true` |

`ACC-S1-NORTH_SHORT` 选北连线，快但需杰克继续 `COVER`；`ACC-S2-SOUTH_STABLE` 选南连线，慢但允许无人机先更新一次地面。两者都不改变“杰克挡板、人员齐、万机馆只接外缘”。

### 3.3 结果与 Checkpoint

| result | 条件 | 后续 |
| --- | --- | --- |
| `clear` | 工房组撤到 `A-INNER-SAFE`；通路开；杰克主工具仍 normal | 写 `TX_C02E04_ACCIDENT_CP` |
| `partial` | 人员和通路仍完成；杰克一个举升臂 `2→1` | E05 护送工程车时预览额外支撑窗；不改变救援出口 |
| `withdraw` | 在 W1/W2 稳定点交回 Story | 不记玩法 Clear，单独读取 E04 固定 Checkpoint |
| `fail_continue` | 路线已被新红光判为失效，或计划未预留 `ABORT` | 当窗 0 write，回到最近的人员位置；地图已有伤损不消失 |

稳定出口：

```text
D06C02v0.1|fixture=FX-D06-C02E04-ACCIDENT-CP|score=3:2|workshop_group=inner_safe|passage=open|full_king=trapped_full_loadout|no_name=supporting|stage_cannon=powered_off_sliding|wanji=holding_seaside_edge|cargo_leader=towing|result=phase_checkpoint
```

`paper_summary_sha256 = 3c1a18a1fb08ba38d46a059027003de98978aa748ad8faa6b9b5cf064281f964`

`SAVE_C02E04_ACCIDENT_CP` 精确保存 `ST_BODY / ST_LOCATION / ST_EQUIPMENT / ST_KNOWLEDGE / ST_RESOURCE / ST_CONSENT / ST_RESULT / ST_OPERATION`；`ST_OPERATION` 为 `OP_C02_STAGE_ACCIDENT:active, phase=E04_checkpoint`。三条自主支援 receipt 及其 withdrawal/expiry 进入 `ST_CONSENT`，推进模块／全装唯一实例进入 `ST_EQUIPMENT`。它不保存 `ST_ROSTER`：杰克、货柜领袖等只是本 Operation 的具名支援／身体分配，没有发生长期成员变化。这不是 Encounter/Operation Clear，不能发奖、回馆或治疗。Future consumer 唯一为 `FX-D06-C02E05-RESCUE-CLEAR` 的初态。

E04 出口与 E05 入口用下列去除 Fixture envelope 的共享 carry payload 校验：

```text
D06C02v0.1|carry=E04CP_to_E05|score=3:2|workshop_group=inner_safe|passage=open|full_king=trapped_full_loadout|no_name=supporting|stage_cannon=powered_off_sliding|wanji=holding_seaside_edge|cargo_leader=towing
```

`carry_payload_sha256 = 8f08c8e6670b241d7d0df5335fb19d6750368ca65e2374b66df35b45cd8b013f`

## 4. `FX-D06-C02E05-RESCUE-CLEAR`：三阶段事故救援

### 4.1 连续初态与区域

```text
D06C02v0.1|fixture=FX-D06-C02E05-RESCUE-CLEAR|score=3:2|workshop_group=inner_safe|passage=open|full_king=trapped_full_loadout|no_name=supporting|stage_cannon=powered_off_sliding|wanji=holding_seaside_edge|cargo_leader=towing|result=pending
```

`paper_summary_sha256 = 1b68a88a64ba2962f0d7ee99813ad7783599661a707a8dc82656f7e18aa0b512`

| 区域 | 用途／初态 |
| --- | --- |
| `R-INNER-SAFE` | 人员全部安全；工程调度与设备内移的唯一人员区 |
| `R-LANE-N / R-LANE-S` | 工程车到炮座的两条 Candidate 路；危险投影每窗更新 |
| `R-ANCHOR` | 两根扭曲支架拖着炮座撕环；两条固定索拉紧后才可切断 |
| `R-SLOPE` | 两台决赛机和下滑炮身；王者腿／翼被卡 |
| `R-WANJI-EDGE` | 万机馆只支撑下沉一侧，不托起整环 |
| `R-WORKROAD` | 货柜领袖、地面车队、船台托架的直线牵引线 |
| `R-BROKEN-BRIDGE` | 馆守Z用现有巡展臂和完好战斗臂固定，不生成新右前臂 |
| `R-INNER-LOAD` | 旧拳王用红色牵引带拖移松脱外装和后续背炮 |
| `R-DEMOLITION-FRAME` | 断电舞台炮必须送回的高处拆解架；吊机只在炮入架后可接 |
| `R-LOCAL-MAINT` | 完全版王者外装的原地保管／维修去向；不是玩家库存 |

事故 Hazard 每窗固定按此顺序解算：`personnel safety guard → committed body reactions → cannon slide → ring tear/settle → support margin → checkpoint derivation`。动画不得改变该顺序。

### 4.2 Phase A `SCAN_ESCORT_CUT`

Primary：把工程车和坞工杰克送到 `R-ANCHOR`，连好两条固定索，再让黄机依次切断左／右支架。

| 窗 | 可见 Intent／Forecast | 玩家动词 | 固定动作／事务 |
| --- | --- | --- | --- |
| `PA-W1` | 红机绕环标记，本窗结束进入 overheat | 选择扫描焦点；提交 `REQ_C02E05_RED_RING_SCAN` | 红机回应后完成一圈；白鸢线若与新红灯冲突就整段删除，不给未来真值 |
| `PA-W2` | N/S 路风险、轻板下滑 | 选路并提交 `REQ_C02E05_BLUE_ENGINEERING_COVER`、`REQ_C02E05_JACK_ENGINEERING_ESCORT`；保留 `ABORT` | 蓝机／杰克分别按热量、路线、工具条件回应后，蓝机临海挡板，杰克托工程车过缝 |
| `PA-W3` | 炮座仍通过支架撕环 | `BRACE; INTERACT attach two lines` | 杰克顶炮座，工程车落地；`line_left/right=tensioned` |
| `PA-W4` | 两条索已拉紧；断一根后炮身压力可预览 | 提交 `REQ_C02E05_YELLOW_BRACKET_CUT`；`ABORT if line invalid` | 黄机只在两索有效的 response 后左后右切断；炮不再横向撕环，但全重交给两机 |

`PA-S1-CONTINUOUS_BLUE` 让蓝机全程贴工程车，路短但蓝机热量高；`PA-S2-CHOKEPOINT_RELAY` 让蓝机先占轻板落点，杰克按无人机标记走稳定路，同在 PA-W3 到达锚点，但杰克工具应力较低、蓝机承受更大的单点拦截力。红机过热、黄机左后右切断都是两路共同固定动作。

Checkpoint `TX_C02E05_PA_CP` 必须写：`routes/current danger; red heat; blue position; Jack tool state; engineering vehicle position; line_left/right; both brackets detached; cannon support transfer; ring tear stopped laterally`。

### 4.3 Phase B `WEIGHT_TOW_SUPPORT`

Primary：把万机馆／货柜领袖、馆守Z、旧拳王和地面工程对齐成一条可解释的承重链，不用百米馆体飞起或一键顶住所有区。

| 窗 | 环境 Forecast | 玩家动词 | 固定动作／出口 |
| --- | --- | --- | --- |
| `PB-W1` | 临海侧主载点可见；作业道不允许船台离架 | 选承力线并提交 `REQ_C02E05_CARGO_WANJI_TOW`；`BRACE workroad` | 货柜领袖按作业道条件回应后与车队把万机馆拖近，接触面变宽 |
| `PB-W2` | 断桥和松脱外装分别威胁工程线 | 依次提交 `REQ_C02E05_GUARDIAN_BRIDGE_BRACE`、`REQ_C02E05_OLD_BOXER_CLEAR_LOAD` | 馆守Z／旧拳王分别回应后，严格按馆守Z固定断桥→旧拳王拖出外装执行 |
| `PB-W3` | 炮仍向两机下压；平台支撑余量可见 | `WAIT_CONDITION; support allocation; ABORT overload` | 整条救援线同时站住；尚未解决炮 |

`PB-S1-WORKROAD_BRACE` 的第一个玩家动作是给作业道／船台预留承力，让 PB-W1 牵引余量更高；`PB-S2-LOAD_RISK_PREVIEW` 的第一个玩家动作是查看断桥与松脱外装的两个威胁窗，预留馆守Z／旧拳王各自的反应，因未先 Brace 而让 PB-W1 作业道应力更高。两策略的已提交身体动作和玩家可见演出顺序都严格保持 `货柜领袖牵引万机馆接宽 → 馆守Z固定断桥 → 旧拳王拖出外装`；只有准备、反应槽和公开应力不同。两者在相同 W3 形成共同承重终态，不改变货柜领袖的主体性、地面支撑或馆守Z独臂边界。

Checkpoint `TX_C02E05_PB_CP` 完整继承 PA，再增加 `wanji_contact_width; workroad_support; cargo_leader_tow_state; bridge_state; Guardian Z body state; Old Boxer position/tool; loose_load_state; cannon_load_margin`。

### 4.4 Phase C `SELF_DETACH_AND_CANNON_BOSS`

#### C1. 自主卸装不是玩家解锁技能

1. 胶价王撤销资产优先，承担已验收故事里的项目损失；`SOG-C2` 写 `AUTH_C02E05_ASSET_PRIORITY_REVOKE`，范围仅为本次事故自救。
2. 原承包商当值维护员确认事故自救可解除外装；`SOG-C2` 写 `AUTH_C02E05_CONTRACTOR_DETACH_UNLOCK`，grantor、grantee、action scope、expiry 均完整。这不转移所有权或保管。
3. 兜灯只给出“背炮先走、外翼后解”的工程顺序；玩家可分配支援，不能代按确认。
4. 完全版王者本人通过 `REQ_C02E05_FULL_KING_SELF_DETACH` 返回具体回应，然后自己提交卸装。`SOG-REL` 只记本次行动同意，不写永久服从。
5. 卸装顺序固定为背炮 → 被卡外翼 → 其他外翼／钻进 → 双盾 → 头冠。长翼作工程踏板，双盾撑环，头冠只作现场警报。

#### C2. 施设 Boss 行动窗

| 窗 | Hazard Forecast | 玩家动词 | 固定动作 |
| --- | --- | --- | --- |
| `PC-W1` | 炮下滑速度上升，拆解架只能从高处接炮 | 校验两条 Authority receipt；读取 `REQ_C02E05_FULL_KING_SELF_DETACH` 的本人回应，再提交 `REQ_C02E05_FULL_KING_CANNON_SUPPORT` | 王者本人卸装后回应支援请求并上坡托炮；无牌一号在坡下留出接触弧 |
| `PC-W2` | 炮口偏向万机馆的风险可见 | `WAIT_CONDITION; COUNTER reserve`；提交 `REQ_C02E05_OLD_BOXER_LOCK_BASE` | 旧拳王回应后锁炮座；王者侧让，无牌一号正面承接 |
| `PC-W3` | 逆向位移结果带显示炮可达拆解架 | `TACT_COUNTER/MELEE; support handoff` | 逆转天冲拳把炮车送回拆解架；王者用肩背补接 |
| `PC-W4` | 断梁／护板会干扰吊索 | 分别提交 `REQ_C02E05_YELLOW_FRAME_INTERCEPT`、`REQ_C02E05_RED_CLEAR_PANEL`、`REQ_C02E05_BLUE_CREW_COVER`、`REQ_C02E05_JACK_FRAME_BRACE` | 四主体分别按射线／热量／人员路线／工具条件回应后执行；吊机最后移走炮 |

`PC-S1-RING_MARGIN_FIRST` 把额外反应留给环与万机馆，王者托炮时间更长；`PC-S2-EQUIPMENT_PATH_FIRST` 用旧拳王／坞工杰克更早清外装通路，两机接力窗更窄。两者都必须到达“王者先托、无牌一号后接并反送”，不允许网格上的另一台机替换这个固定主体动作。

E05 的 `strategy_count=2` 指两条端到端方案族，不是把每个 Phase 的局部变体相加冒充多解：

| strategy_id | PA | PB | PC | 第一个实质差异 | 固定共同出口 |
| --- | --- | --- | --- | --- | --- |
| `RESCUE-S1-MARGIN_CHAIN` | `PA-S1-CONTINUOUS_BLUE` | `PB-S1-WORKROAD_BRACE` | `PC-S1-RING_MARGIN_FIRST` | 蓝机连续护送，随后优先把作业道／环余量做厚 | 人员安全、王者自主卸装、炮入拆解架并吊离、环停止下沉、比分仍 `3:2` |
| `RESCUE-S2-RELAY_PATH` | `PA-S2-CHOKEPOINT_RELAY` | `PB-S2-LOAD_RISK_PREVIEW` | `PC-S2-EQUIPMENT_PATH_FIRST` | 先占轻板落点并预览断桥／外装风险，随后压缩装备通路 | 同左 |

两族必须各自从 E05 初态连续走到 Accident Clear；若只能把 S1 的某阶段与 S2 的另一阶段拼成唯一解，`D06-C02-A16` 仍判失败。

`TX_C02E05_PC_CP` 在 PC-W4 完成后、Accident Settlement 之前写入：`cannon in demolition frame; crane custody transfer complete; ring/ground support; all body stress; Full King equipment owner/version/custody/installed_state/condition; action-scoped authority receipts; all autonomous action-bound consent receipts; score still 3:2`。它不允许提前写转子、推进模块、Roster 或航向。

四个 E05 稳定边界使用同一套状态域 schema；“域存在”不等于提前伪造事件。PA/PB 已保存当阶段每个自主支援的具名 `ST_CONSENT` receipt；PC 再增加动作级 `ST_AUTHORITY` 链和王者本人卸装／支援 receipt，不能用 `no_action_proposal` 掩盖已发生的主体回应。

| save／transaction | `ST_OPERATION` | `ST_CONSENT` | `ST_AUTHORITY` | 装备与其余累计状态 |
| --- | --- | --- | --- | --- |
| `SAVE_C02E05_PA_CP / TX_C02E05_PA_CP` | `active, phase=PA_committed` | Red／Blue／Jack／Yellow 的 response、conditions、body action、withdrawal/expiry receipt | `no_action_authority_yet` | 累计 Body／Location／Equipment／Resource／Knowledge／Result |
| `SAVE_C02E05_PB_CP / TX_C02E05_PB_CP` | `active, phase=PB_committed` | 完整继承 PA，再加 Cargo Leader／Guardian Z／Old Boxer receipts | `no_action_authority_yet` | 继承装备 owner/version/custody/installed state，再加承重链与局部应力 |
| `SAVE_C02E05_PC_CP / TX_C02E05_PC_CP` | `active, phase=PC_committed, settlement=pending` | 王者本人／王者支援／Old Boxer／Red／Blue／Yellow／Jack receipts | 资产优先撤销＋承包商动作级解锁两条 receipt | 完整继承 PA/PB，再加外装逐实例状态与炮入架 |
| `SAVE_C02E05_ACCIDENT_CLEAR / TX_C02E05_ACCIDENT_CLEAR` | `clear, future_consumer=OP_C02_DEPARTURE` | 原样封存动作回执，不升级永久许可 | 两条动作权限按 expiry 结清并保留审计，不变长期权力 | 事故最终 Body／Location／Equipment／Resource／Knowledge／Result |

### 4.5 三阶段结果与 Accident Settlement

| result | 精确条件 | 持久差分 |
| --- | --- | --- |
| `clear` | PA 两索后切断；PB 承重链成立；PC 自主卸装 receipt 有效，炮入拆解架并由吊机移走；地面支撑车接重 | 写事故 Operation Clear；不写新转子或登舰 |
| `partial` | 所有 Primary 仍完成，但 PA/PB 带来的一个公开临时应力迫使 PC 多用一个安全窗 | 额外应力在 `TX_C02E05_ACCIDENT_CLEAR` 中收束为已验收的封场／临时支撑状态，不进 C03 成为新债务 |
| `withdraw` | 在 PA/PB/PC Checkpoint 明示交回 Story | 不记玩法 Clear；故事出口从验收绑定单独投影 |
| `fail_continue` | 先切支架后固索、强制卸装、万机馆离架，或炮未对齐拆解架就提交反击 | 当窗整组拒绝并回最近 Checkpoint；不得部分留下已扣资源或伪同意 |

Accident Clear 摘要：

```text
D06C02v0.1|fixture=FX-D06-C02E05-RESCUE-CLEAR|score=3:2|people=safe|stage_cannon=demolition_frame_secured_and_removed|ring=stopped_sinking|full_king=base_body_safe,loadout_original_owner_local_maintenance|no_name=right_arm_stressed_functional|wanji=edge_support_released_after_ground_support|accident=operation_clear
```

`paper_summary_sha256 = 13659bf329474561536e5fd8257381b9623d1e9a49854a0ce40c81b6909a3d69`

`TX_C02E05_ACCIDENT_CLEAR` 的 Owner prepare 必须分开：

| owner | 必须验证 | 只在本事务提交 |
| --- | --- | --- |
| `SOG-NARR` | `score=3:2` 不变；人员安全；事故不计分；不提前改 Roster/航向 | `stage_accident=clear; next=STORY_SCORE_REAFFIRM` |
| `SOG-BODY` | 王者卸装来自其本人回应；每个装备实例的 owner/version/custody/installed_state/condition 完整；无牌一号伤损不被治愈 | 具体身体／装备位置、装配、功能、应力 |
| `SOG-WORLD` | 炮身已被吊离；环已停止下沉；万机馆没有托起整环 | 封场、地面支撑与设备安全位 |
| `SOG-C2` | 胶价王撤销资产优先与承包商维护员动作解锁的 grantor/grantee/scope/expiry 合法 | 只写本次事故动作权限与撤销审计，不生成万能权限 |
| `SOG-REL` | 本次卸装及全部自主支援的 request/precommit、回应、条件、身体动作、撤回／过期一致 | 只写行动级 consent，不写永久服从 |
| `SOG-SETTLE` | PA/PB/PC receipts 齐；全部 `proposal_hash` 一致；无负资源或重复对象 | 一次提交并生成唯一 Accident receipt |

Future consumers 严格分两步：

1. `C02E05 STORY_SCORE_REAFFIRM / DEPARTURE`读事故清理回执，再独立处理新旧转子、推进模块、泊位、登舰／留街和不停机航线。
2. `C03E01` 只能读已封存 Chapter Settlement，不直读 PA/PB/PC 微观分数、路线或临时应力。

存档边界为 `SAVE_C02E05_PA_CP → SAVE_C02E05_PB_CP → SAVE_C02E05_PC_CP → SAVE_C02E05_ACCIDENT_CLEAR`。每个存档都精确保存累计 `ST_BODY / ST_LOCATION / ST_EQUIPMENT / ST_RESOURCE / ST_KNOWLEDGE / ST_AUTHORITY / ST_CONSENT / ST_RESULT / ST_OPERATION`；只有成功 commit 的当窗能推进一个边界。`SOG-C2` 只允许本次 `authority_ops`，`SOG-REL` 只允许 `consent_ops`，其 `relation_ops/promise_ops` 必须为空，所以机器状态域不含 `ST_RELATION`。

## 5. 机器可校验纸面合同断言

当前 checker 实际执行的是 A01、A08、A11、A19–A22 的静态账本／hash／字段完整性，以及 MATCH 四条接触式的算术重算。其余行是未来 resolver、自动搜索、Build 或真人测试必须实现的计划断言；列在这里不等于已经运行。

| assertion_id | 输入／操作 | 必须结果 |
| --- | --- | --- |
| `D06-C02-A01` | 重算 Reader/E04/E05/回执 SHA-256 | 全部等于 0.1 节；否则全 Fixture `source_drift_stop` |
| `D06-C02-A02` | 查看前两分 UI action graph | 不存在可点却注定失败的伪战术动词；只有 Story Showcase 投影 |
| `D06-C02-A03` | 枚举 Tournament Clear | `score=3:2; winner=no_name` 且王者仍 full_loadout；其他比分不能 commit |
| `D06-C02-A04` | 从各分 Checkpoint 重载 | 前分、伤损、推进使用和热量保留；只复位位置／朝向／当分 Intent |
| `D06-C02-A05` | 对 P3/P4/P5 分别删掉承诺 Intent | 对应 `COUNTER` 不能神秘触发；无隐藏目标修正 |
| `D06-C02-A06` | E04 事故 Checkpoint 请求 Mission Clear/奖励/治疗 | 拒绝 `E_OPERATION_STILL_ACTIVE` |
| `D06-C02-A07` | E04 事故从 N/S 两路回放 | 人员都到 inner_safe；普通观众棋子数=0；王者仍被卡且全装 |
| `D06-C02-A08` | E04 Checkpoint 直接加载 E05 | 两侧去除 `fixture/result` envelope 后的 carry payload hash 都等于 `8f08c8e...013f`；不满血／满资源 |
| `D06-C02-A09` | 在 PA 未固定两索前请求黄机切断 | 整组 0 write，返回 `E_SUPPORT_LINES_NOT_TENSIONED` |
| `D06-C02-A10` | 直接让万机馆飞起／离开托架／托整环 | 拒绝 `E_WANJI_BODY_MODE_NOT_AVAILABLE` |
| `D06-C02-A11` | 枚举 E04/E05 每个 `REQ_C02*` 自主支援／本人决定记录，并删除任一 response、conditions、body action、receipt 或 withdrawal/expiry | 静态 checker 报 `E_ACTION_CONSENT_CONTRACT_INCOMPLETE`；未来 Owner prepare 必须整组 0 write，不能只检查王者或把支援做成按钮服从 |
| `D06-C02-A12` | 将王者外装写入玩家库存或改写任一装备 owner/custody | `SOG-BODY reject E_OWNERSHIP_DRIFT`；其他 Owner 0 write |
| `D06-C02-A13` | 用 Accident 成绩修改比分或发赛事奖励 | `SOG-NARR reject E_HARD_STORY_GUARD` |
| `D06-C02-A14` | Full/Skip、30/60/120fps、加载顺序与同存档回放各 1000 次 | 每个 Checkpoint 的 `state_hash;receipt_hash;event_queue` 分别唯一且一致 |
| `D06-C02-A15` | 从空状态按 receipt order 重建 | rebuild hash = stable save hash；转子、外装、机体和人员唯一实例不重复 |
| `D06-C02-A16` | 搜索两个 Tournament 策略族和各救援 Phase 的两个局部方案 | 至少两个第一动作、路线或承力职责不同的方案可达；否则不进 Build |
| `D06-C02-A17` | 移除三飞行机、货柜领袖或本地机的本话支援实例 | 不得自动生成其长期召唤菜单或乘员身份 |
| `D06-C02-A18` | Accident Clear 之后直接请求 C03 读 PA/PB/PC 微观差分 | 拒绝 `E_CHAPTER_SETTLEMENT_MISSING`；必须先走 Departure/Chapter Settlement |
| `D06-C02-A19` | 对三条 fixture registry 读取 `transaction_trace_id/state_domains` 并与 `OST-04/05/06` 比较 | 每条状态域集合精确相等；MATCH 含 Location/Equipment，E04事故含 Equipment/Consent，E05事故含 Equipment/Authority/Consent；事故均无 `ST_ROSTER`，E05无 `ST_RELATION` |
| `D06-C02-A20` | 将每条 Fixture 的 TX／SAVE ID 与正文覆盖、story seed guard、ASB 逐项重算 | ID 无缺漏／重复；seed 行存在且同属 `ASB-C02-20260806-56827053`；固定出口 token 仍来自对应只读投影 |
| `D06-C02-A21` | 对 `data/c02-paper-equipment-state-ledger.tsv` 每行依次删 `owner/owner_version/custody/installed_state/condition` 任一字段 | 静态 checker 必须拒绝 `E_EQUIPMENT_LEDGER_INCOMPLETE`；未来 `SOG-BODY` prepare 整组 0 write，不得用 full_loadout 名词代替唯一实例链 |
| `D06-C02-A22` | 删除 E05 的资产优先撤销或承包商动作解锁记录，或清空 grantor/grantee/action_scope/expiry 任一字段 | 静态 checker 必须拒绝 `E_ACTION_AUTHORITY_CHAIN_INCOMPLETE`；未来 `SOG-C2` prepare 整组 0 write，且不能偷留王者卸装 consent |

## 6. 停止门

1. **GD2 停止：** 在 `LOC_C02_CARGO_RING` 交付决赛／事故双态平面、承重图、外轨／炮车／拆解架剖面、通路与安全控制链前，八节点／十一区只是逻辑纸模，不得转网格或正式地图。
2. **D04 停止：** P1 Scheduler 未裁决、resolver 未实现；本件只写语义窗，不得称已证明 WEGO 或交替制。
3. **多解停止：** 完整搜索找不到两个非换名方案，或其一成为严格支配策略，则返地图／动词层重做；不用两段演出文字伪装多解。
4. **玩家诚实停止：** 冷启测试者若认为前两分是“可玩但系统暗中让我输”，`INF-C02-01` 失败；改 UI/承载或重开故事适配。
5. **因果停止：** 任一方案需要 E04 提前卸装、白鸢精确预知、七海远控、普通观众棋子、万机馆飞起、迫使王者卸装或改写 `3:2`，立即拒绝该玩法方案，不回修 Reader。
6. **产出停止：** 本件没有 Build、灰盒、自动搜索、状态 hash 运行、目标玩家或用户玩法验收；E04事故/E05救援没有数值 resolver，三个实例只能标为 `candidate_paper_fixture_defined`，其中仅 MATCH 四接触式具静态算术重算证据。
