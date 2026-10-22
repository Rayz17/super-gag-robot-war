# 《超GAG机器人大战：万机残响》机体数值、成长改装与关卡平衡 Bible v0.1

> 承接 [机体数值、成长改装与关卡平衡调研报告](./2026-06-22-mecha-stats-growth-balance-research.md)。  
> 本文定义本项目的 SRPG 数值骨架、机体原型、武器型谱、升级改装路线、关卡目标模板和平衡验收标准。

---

## 0. 一句话目标

《超GAG》的数值系统要让玩家觉得：

> 我不是在把所有机器人喂成同一台高攻高防机，而是在把每台机体修回它自己的战斗人格。

所以本系统按这个顺序设计：

```text
角色/机体定位 -> 数值预算 -> 武器动词 -> 改装路径 -> 关卡目标 -> 平衡验收
```

---

## 1. 系统边界

本文定义：

- 机体和驾驶员的基础数值字段。
- 伤害、命中、EN、士气/燃魂的轻量公式口径。
- 12 类机体原型。
- 20 类武器型谱。
- 12 条成长改装路线。
- 14 类关卡目标模板。
- 十二章平衡目标。

本文不定义：

- 每个具体角色的最终完整数值。
- 全部具体武器名称。
- 每张地图的格子布局。
- 最终难度曲线的精确经济掉落。

---

## 2. 基础数值字段

### 2.1 机体字段

| 字段 | 推荐范围 | 作用 | 设计说明 |
| --- | --- | --- | --- |
| `hp` | 1800-12000 | 生存时间 | 超级系和战舰高，现实机器和支援低 |
| `en` | 80-260 | 高级武器、护盾、飞行、同步消耗 | EN 是机战味核心资源，不要让所有武器都无成本 |
| `armor` | 500-2300 | 减少受到的物理/爆炸伤害 | 重装和超级系高，高机动低 |
| `mobility` | 50-170 | 回避、被锁定难度、部分再行动条件 | 高机动单位主轴 |
| `sensor` | 50-170 | 命中、侦测隐藏意图、远程稳定 | 炮击/支援/AI 系重要 |
| `move` | 3-8 | 地图移动力 | 战舰/重装低，高机动/飞行高 |
| `size` | S/M/L/XL | 命中、回避、承伤和地形限制 | 大型机不应只强不弱 |
| `terrain` | land/air/space/water/digital | 地形适应 | 用来制造章节差异 |
| `slots` | 1-4 | 强化件容量 | 低数值单位可用槽位补定位 |
| `stability` | 0-100 | 机魂稳定/过载风险 | 连接剧情变量和战斗状态 |

### 2.2 驾驶员字段

| 字段 | 推荐范围 | 作用 |
| --- | --- | --- |
| `melee` | 80-220 | 近战武器伤害和部分命中 |
| `ranged` | 80-220 | 射击/炮击/远程武器伤害和部分命中 |
| `defense` | 80-220 | 受伤减免、保护动作 |
| `evasion` | 80-220 | 回避和脱离锁定 |
| `skill` | 80-220 | 暴击、反击、状态命中、非致命压制 |
| `focus` | 50-180 | 精神/燃魂资源上限与恢复 |
| `command` | 50-180 | 指挥、援护、舰长、支援派遣 |
| `sync` | 0-200 | 合体、同步、机魂共鸣、过载判定 |

### 2.3 派生字段

| 派生字段 | 计算来源 | 用途 |
| --- | --- | --- |
| `hit_score` | 机体 sensor + 驾驶员对应攻击 stat + 武器 accuracy | 命中预测 |
| `evade_score` | 机体 mobility + 驾驶员 evasion + 地形 | 回避预测 |
| `guard_score` | 机体 armor + 驾驶员 defense + 防御状态 | 承伤预测 |
| `intent_visibility` | sensor + command + 资料完整度 | 看见敌方意图和隐藏目标 |
| `overdrive_limit` | stability + sync + 机魂状态 | 燃魂/同步/合体的安全窗口 |

---

## 3. 轻量战斗公式

公式要可读，先服务预测界面，再服务数值细节。

### 3.1 伤害

```text
attack_stat =
  weapon.type == melee  ? pilot.melee  :
  weapon.type == ranged ? pilot.ranged :
  max(pilot.melee, pilot.ranged) * 0.5 + pilot.sync * 0.5

base_damage =
  weapon.power
  + attack_stat * weapon.stat_scale
  + mech.weapon_upgrade_bonus
  + morale_bonus

mitigation =
  target.armor * armor_scale
  + target.pilot.defense * defense_scale
  + terrain_guard

final_damage =
  max(min_damage, base_damage - mitigation)
  * size_modifier
  * terrain_modifier
  * barrier_modifier
  * critical_modifier
  * objective_modifier
```

推荐参数：

| 参数 | 初始值 |
| --- | --- |
| `weapon.stat_scale` | 4 到 8 |
| `armor_scale` | 0.55 |
| `defense_scale` | 2.0 |
| `min_damage` | 武器威力的 8% 到 12% |
| `critical_modifier` | 1.25 到 1.5 |
| `guard_action_modifier` | 0.6 |
| `barrier_modifier` | 0.5 或固定减伤，消耗 EN |

设计说明：

- 机体装甲和驾驶员防御都重要，但不能完全把伤害压成 0。
- 暴击不能太高，否则战斗预测失去可信度。
- 保护目标和非致命目标可以有 `objective_modifier`，避免剧情对象被普通公式秒掉。

### 3.2 命中

```text
hit_rate =
  70
  + (attacker.hit_score - defender.evade_score) * 0.35
  + weapon.accuracy
  + terrain_hit
  + support_bonus
  - status_penalty

hit_rate = clamp(hit_rate, 15, 95)
```

设计说明：

- 命中上下限保留机战味，但关键剧情动作应尽量使用确定性或高命中。
- 低命中不应用来制造主要难度。主要难度来自目标压力和敌方意图。
- 控场、封锁、说得标记类武器可以使用固定成功或分段成功，减少挫败。

### 3.3 EN 和弹药

武器资源分三类：

| 资源类型 | 用途 | 平衡价值 |
| --- | --- | --- |
| `ammo` | 实弹、特殊弹、一次性道具 | 限制强控场和高爆发 |
| `en` | 光束、屏障、飞行、合体、燃魂 | 让高性能机体有作战时长压力 |
| `cooldown` | 支援、地图兵器、特殊动作 | 防止强效果每回合重复 |

规则：

- 普通武器至少有 1 个低成本选择。
- 必杀技必须消耗 EN 或弹药，并绑定士气/燃魂门槛。
- 地图兵器必须有明显预备、冷却、误伤或目标限制。

### 3.4 士气、燃魂、同步

| 系统 | 功能 | 来源 | 约束 |
| --- | --- | --- | --- |
| 士气 | 解锁武器、提升少量伤害和防御 | 击坠、被攻击、保护成功、剧情事件 | 主线不要求极高士气 |
| 燃魂 | 3 回合左右的短时爆发 | 剧情、机魂稳定、关键行动 | 结束后可能过热 |
| 同步 | 援护链、合体、双人驾驶、灯槽事件 | 角色关系、同步玩法、支援行动 | 过高会有失真风险 |

推荐：

```text
morale range: 80-170
normal weapon gate: 100-120
signature weapon gate: 120-140
dangerous overdrive gate: 140+
```

---

## 4. 机体原型

正式数据见 `data/gameplay/unit_archetypes.tsv`。本 Bible 使用 12 类原型：

| 原型 | 队伍职责 |
| --- | --- |
| `SUPER_GUARDIAN` | 高 HP/装甲，保护、反击、承伤、燃魂爆发 |
| `COMBINER_BURST` | 合体、短爆发、高 EN 压力、同步风险 |
| `REAL_SNIPER` | 远程、命中、弱点打击、低承伤 |
| `HIGH_MOBILITY` | 抢点、诱敌、截击、回避、脆弱 |
| `SUPPORT_REPAIR` | 修理、补给、护盾、非致命辅助 |
| `BATTLESHIP_COMMAND` | 指挥、补给、地图支援、巨大目标 |
| `SWARM_CONTROL` | 控场、推拉、封锁、地形改写 |
| `HEAVY_ARTILLERY` | 大范围火力、低机动、资源压力 |
| `DUEL_COUNTER` | 近身、反击、单挑、非致命击倒 |
| `CIVILIAN_ESCORT` | 护送对象、成长叙事、低攻击高剧情价值 |
| `SIGNAL_HACKER` | 侦测、清噪、敌方意图、资料战 |
| `RITUAL_SYNC` | 同步、歌、灯槽、合体链和关系爆发 |

原型不是职业锁死，而是数值预算和升级偏向。

---

## 5. 武器型谱

正式数据见 `data/gameplay/weapon_patterns.tsv`。每个武器必须至少有一个战术动词：

| 动词 | 说明 |
| --- | --- |
| `damage` | 纯伤害，但必须有资源或站位约束 |
| `guard` | 保护目标、援护防御、减伤 |
| `push/pull` | 改变敌我位置 |
| `intercept` | 阻止移动、截断路线、反击突入 |
| `seal` | 封锁刷兵点、区域、技能或敌方意图 |
| `pierce` | 破屏障、破装甲、破护盾 |
| `nonlethal` | 压制、说得前置、避免击坠 |
| `sync` | 提升同步、共享行动、援护链 |
| `persuade_mark` | 给说得/剧情触发做标记 |
| `transmit` | 传递战报、信号、远星信息 |

平衡禁区：

- 不做无消耗全屏地图炮。
- 不做同时高伤害、高命中、长射程、无反制的武器。
- 非致命武器不能比普通武器永远更优，必须牺牲伤害或资源。
- 控场武器对 Boss 使用时改为削阶段、打断意图或降护盾，不直接封死。

---

## 6. 成长与改装

正式数据见 `data/gameplay/upgrade_paths.tsv`。

### 6.1 资源分层

| 资源 | 用途 |
| --- | --- |
| `credits` | 机体基础改装、普通维修 |
| `repair_parts` | 特殊机体节点、战后损伤、展品维护 |
| `pilot_pp` | 驾驶员技能和少量 stat 增强 |
| `mxbits` | 万机馆设施、支援系统、开馆收益 |
| `soul_shards` | 机魂调律、隐藏机体、非致命路线 |
| `evidence` | 清算谈判、说得、合规限制解除 |
| `relationship` | 援护、合体、同步、结局质量 |

### 6.2 改装层级

推荐首版采用 5+5 结构：

| 阶段 | 说明 |
| --- | --- |
| Tier 1-5 | 主线标准改装，上限控制在普通玩家可理解范围 |
| Full Custom Bonus | 某台机体核心五项达到 Tier 5 后获得专属特性 |
| Tier 6-10 | 中后期/隐藏/挑战扩展，不作为主线通关要求 |
| EX Bonus | Tier 10 或角色线完成后获得，但必须有代价或定位限制 |

### 6.3 改装路线

| 路线 | 功能 |
| --- | --- |
| 框架改装 | HP、EN、装甲、机动、传感 |
| 武器组改装 | 普通武器整体提升，避免逐把武器刷钱 |
| 标志武器改装 | 每台机体 1 到 2 个特色武器获得动词强化 |
| 机魂调律 | 稳定度、燃魂、同步、暴走风险 |
| 支援槽位 | 强化件、展舰支援、辅助装备 |
| 驾驶员训练 | stat、技能、精神、援护 |
| 羁绊/关系 | 合体、同步、说得、援护台词 |
| 万机馆设施 | 全局支援、维修效率、资源转换 |

### 6.4 改装原则

- 改装不删除弱点，只改变玩家处理弱点的方式。
- 每台主线机体至少有 1 个“爱用可见”的专属改装。
- 现实机器和支援单位不能通过改装变成普通输出单位。
- 隐藏机体可以强，但必须绑定路线、关系或关卡责任，不做纯奖励火力。

---

## 7. 关卡模板

正式数据见 `data/gameplay/encounter_templates.tsv`。  
关卡不再以“全灭敌人”作为默认目标，而以动词建库：

| 动词 | 目标 |
| --- | --- |
| 守 | 保护留言墙、展品、城市建筑、信号阵列 |
| 撤 | 让市民、舰队、量产兵、展舰安全离开 |
| 截 | 阻止敌方到达封存线、仪式节点、撤退路线 |
| 诱 | 把敌人引到安全区、陷阱区或非致命范围 |
| 护 | 护送无法战斗或低战力单位 |
| 拆 | 拆除节点、炮台、清噪塔、剧本锁 |
| 说得 | 削弱、标记、满足关系条件后说服 |
| 同步 | 维持多点压力、灯槽、合体或歌声支援 |
| 封锁 | 控制刷兵口、门、航线和数据通道 |
| 传递 | 保护信号、战报、日志、回信或最后问题 |
| 维持 | 在一定回合内撑住而非获胜 |
| 决斗 | 单挑/镜像战/非致命压制 |
| 调度 | 舰内灾害或城市风险多点分配 |
| 终局保存 | 保护记忆节点和差异，不追求最大击坠 |

---

## 8. 平衡标准

正式数据见 `data/gameplay/mission_balance_targets.tsv`。

### 8.1 三套队伍验收

每关必须用三套队伍模拟：

| 队伍 | 改装水平 | 验收 |
| --- | --- | --- |
| 低改队 | 关键单位 Tier 1-2，武器少量改 | 能过主线，可能失去 1 到 2 个副目标 |
| 正常队 | 主力 Tier 3-5，关键武器 Tier 3 | 能完成主目标和多数副目标 |
| 高改队 | 爱用单位 Tier 5+，有专属 bonus | 能挑战隐藏目标，但不能无视敌方意图 |

### 8.2 时间到击破标准

| 敌人类型 | 正常队标准 |
| --- | --- |
| 杂兵 | 1 到 2 次普通攻击 |
| 重装杂兵 | 2 到 3 次普通攻击或 1 次破甲 + 1 次攻击 |
| 精英 | 3 到 5 次有效行动，需要克制或资源 |
| 小 Boss | 5 到 8 次有效行动，有阶段或护盾 |
| 章节 Boss | 8 到 12 次有效行动，必须绑定目标机制 |
| 不可击破敌 | 不用 HP 平衡，用撑回合、传递、封锁或撤退目标平衡 |

### 8.3 敌方预算

每个敌人有 `threat_points`：

| 类型 | threat_points |
| --- | --- |
| 低级杂兵 | 1 |
| 标准杂兵 | 2 |
| 重装/高机动杂兵 | 3 |
| 精英 | 5 |
| 小 Boss | 8 |
| 章节 Boss 阶段 | 10-16 |
| 地图炮/封存/清噪装置 | 4-8 |

一场普通主线战的总威胁建议：

```text
enemy_budget = deploy_count * target_turns * 0.65 到 0.9
objective_pressure = 2 到 6
hidden_pressure = 0 到 4
```

设计解释：

- 我方不是每次行动都应击坠敌人，很多行动要用于移动、保护、补给、说得、封锁。
- 如果目标压力很高，敌方 HP 和数量要下调。
- 如果敌方数量很多，就不要再给每个敌人复杂机制。

### 8.4 难度档

| 难度 | 调整方向 |
| --- | --- |
| Story | 敌方预算 80%-85%，隐藏目标默认宽松，失败后果轻 |
| Normal | 标准预算，要求读敌方意图和目标 |
| Hard | 敌方预算 110%-115%，更多意图组合，副目标更紧 |
| Expert | 少量资源限制、更多精英机制，不靠 HP 翻倍 |

---

## 9. 第一章垂直切片平衡

### 9.1 1-1 闭馆探索

非战斗段输出：

| 行为 | 战斗影响 |
| --- | --- |
| 修好右臂线路 | 1-2 馆守Z可提前 1 回合援护 |
| 检查防火系统 | 留言墙/展柜获得一次减伤 |
| 和七海对清单 | 清算压力初始 -1 或白名单目标可见 |
| 调查 0 号侧廊 | 黑展柜共鸣 +1，隐藏意图提示 |

### 9.2 1-2 法务保护战

建议参数：

| 项 | 目标 |
| --- | --- |
| 我方部署 | 3 到 4 单位，含馆守Z/支援/低火力保护者 |
| 回合数 | 6 回合保护 |
| 敌人 | 6 到 9 个封存无人机，1 个清单执行机 |
| 主目标 | 留言墙或关键展品完整度不归零 |
| 副目标 | 不击坠清单执行机、保护两个孩子留言、阻止封存线抵达 |
| 教学点 | 敌方意图线、保护目标、非致命、援护防御、右臂过热 |

三套队伍标准：

- 低改队：能守住留言墙，但可能损坏 1 个展岛。
- 正常队：守住留言墙和多数展岛，完成非致命副目标。
- 高改队：保全全部展岛，并触发七海额外台词，但不能直接击破所有敌人跳过封存压力。

---

## 10. 实现接口

### 10.1 CombatResolver 读取

```text
UnitInstance
  archetype_id
  mech_stats
  pilot_stats
  weapons[]
  upgrade_state
  statuses[]
  relationship_modifiers

WeaponInstance
  pattern_id
  power
  range
  cost
  accuracy
  tags[]

BattleContext
  terrain
  morale
  objective_modifiers
  difficulty
  hybrid_activity_results
```

### 10.2 ObjectiveSystem 读取

```text
EncounterTemplate
  template_id
  objective_type
  target_objects
  turn_limit
  enemy_intent_rules
  reward_rules
  soft_fail_rules
```

### 10.3 BalanceReport 输出

每场战斗测试后应输出：

```text
BalanceReport
- mission_id
- difficulty
- team_profile: low / normal / high
- clear_rate
- average_turns
- objective_loss_rate
- enemy_kill_rate
- repair_cost
- en_pressure
- dominant_strategy
- units_unused
- notes
```

---

## 11. 后续落地顺序

1. 先用 `unit_archetypes.tsv` 给垂直切片单位定原型。
2. 用 `weapon_patterns.tsv` 给每个单位 2 到 4 个武器动词。
3. 用 `encounter_templates.tsv` 选第一章 1-2 的“守 + 截 + 非致命”模板。
4. 用 `mission_balance_targets.tsv` 写第一章的敌方预算和三套队伍标准。
5. 再进入具体 `units/*.yml`、`weapons/*.yml`、`missions/*.yml` 的实现数据。

这样主程序对话可以先做一场小而像游戏的战斗，而不是继续堆界面和剧情文本。

