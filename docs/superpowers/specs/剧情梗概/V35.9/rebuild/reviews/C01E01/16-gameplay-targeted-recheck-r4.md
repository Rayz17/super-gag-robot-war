# C01E01 游戏制作 / 关卡合同定向复验回执 R4

> 审核席：原独立游戏制作 / 关卡合同终检席  
> 复验范围：仅复核`13-gameplay-final-pass-r3.md`中的`GPR3-01`至`GPR3-04`，重新纸演R1-R3，并检查S02机器犬人口连续性及白函E02/E03生成资产分期  
> 审核方式：读取当前工作区事实源与生成器Override；脚本结果只作旁证，不替代人工语义核验  
> 最终判定：`PASS`  
> 生产状态：`C01E01_GAMEPLAY_CONTRACT_RELEASED_R4`

## 一、定向结论

R3提出的四项局部生产补丁均已真实落入当前工作区，并且跨越了“正文/Runtime/Graybox/生成器源/生成表”必要层级，不是只在回执或生成结果中写了说明。

- S01任务失败现在只重试，不提交四令、展区删改或其他持久状态。
- 机器犬挂接D5后，R2-R3共享D5自动撤离路径并冻结独立移动/情境动作，不再存在免费拖行加独立双动。
- 三个胸灯反射位已有确定解析：左右危险、中间安全；危险预览无消耗返回瞄准。
- `RT013S`是唯一Episode持久提交，使用上游同名键`C01_PHYSICAL_SNAPSHOT`，并已收录烟侵入和喷淋无压。
- S02机器犬读取E01的29人前厅状态，不会再次生成或救出维修员。
- 白函仍严格保持E02远程无格、E03完整实体Boss，且生成器源持有对应生命周期、参与状态、动作与资产Override。

本轮没有遗留`PATCH`或`BLOCKER`。

## 二、GPR3-01至04关闭证据

### GPR3-01：S01失败不提交

**状态：`CLOSED`**

当前三层口径一致：

1. `C01E01_RT011F`规定三回合结束仍未集结4枚Token时进入`MISSION_FAIL_TIMEOUT_THEN_RETRY`，从`BATTLE_SETUP`重开，`RETRY_NO_STATE_COMMIT / NO_DOWNSTREAM_RECEIPT`。
2. `C01E01_GB020`规定`people<29_or_tokens<4`时重试，且`commit no story or persistent state`。
3. `V358GAME001.failure_pressure_contract`已改为：未完成四Token集结则重试，不提交剧情、人员、失败计数、四令或展区删改；四令只由成功后的ADV尾声消防路由与声纹捕获触发。

生成器源中的`SLOT_FAILURE_PRESSURE_OVERRIDES["V357-C01-S01"]`持有同一文本，重新生成不会回退到通用的“失败使下一逻辑恶化”模板。

`V358LOAD001.branch_or_next_carry`仍保留成功后的四令物理承接，这是正确的下一话状态，不是失败分支。

### GPR3-02：机器犬挂接D5后的行动经济

**状态：`CLOSED`**

1. `C01E01_RT004.end_state`现在是：

```text
DOG_TETHERED_TO_D5_INDEPENDENT_MOVE_CONTEXT_LOCKED_UNTIL_D5_STAGED;ONE_PATCHER_ENTERED
```

2. `C01E01_GB009.production_rule`明确：R1开侧门并挂接后，机器犬在R2-R3与D5共享`evac_auto`路径/格位，在D5于`GB019`集结前没有独立移动或情境动作。
3. `C01E01_GB013`只让D5在R2自动移动3格、R3自动移动2格；这两段移动同时携带挂接中的机器犬，不另给机器犬一次行动。

因此当前行动经济为：R1机器犬使用一次移动和一次情境动作完成开门/挂接；R2-R3转入护送挂接状态，没有“免费拖D5同时另走3格”的解释空间。

### GPR3-03：危险胸灯重瞄

**状态：`CLOSED`**

`C01E01_GB022`已建立唯一离散解析：

```text
(3,8)=BLOCKED_BY_DOUDENG
(4,8)=SAFE_ANGLE_CONFIRMED
(5,8)=BLOCKED_BY_DOUDENG
```

与之配套的状态机也一致：

- `GB016`：危险预览进入`BLOCKED_BY_DOUDENG`后无消耗返回`AIM_PREVIEW`。
- `RT011B`：无效角度不触发任务失败、不消耗小机行动、不提交状态。
- `RT009 > RT010`：只有`(4,8)`安全确认后才让胸灯进入`SPENT`并使路径框`UNANCHORED`。
- `GB022.production_rule`要求预览遮罩在确认前可视化危险覆盖，玩法不是盲猜。

危险角、重瞄路径和安全提交现在都可以写成确定测试用例。

### GPR3-04：E01唯一物理快照

**状态：`CLOSED`**

1. `C01E01_RT011`已降为`BATTLE_CLEAR_RECEIPT_NONPERSISTENT`，明确不写Episode handoff，并指向`RT013S_IS_ONLY_PERSISTENT_COMMIT`。
2. `C01E01_RT013S`以`COMMIT_UNIQUE_PHYSICAL_STATE_AS_SINGLE_PERSISTENT_TRANSACTION`提交，状态键为上游同名的：

```text
C01_PHYSICAL_SNAPSHOT=COMMITTED
```

3. 快照内容包含29人尚未城市安全、C3照看关系、馆守Z臂核/外甲、L1远星只读副柜、展陈灯、城市电网/维生、半开防火门、旧路由钥匙、B1泵压、馆守Z胸灯，以及R3要求补入的：

```text
east-side smoke entering L1 front hall
L1 sprinkler dry/no pressure
```

4. 正文“结算状态”已有同名别名`C01_PHYSICAL_SNAPSHOT=RT013S_ATOMIC_PAYLOAD`。
5. `RT013S.downstream_receipt`明确E02只读取该Episode handoff，不读取另一份期末快照。

因此没有第二份竞争性Episode快照，E02火场输入也不再依赖从前置行推断烟与喷淋状态。

## 三、R1-R3重新纸演

### 3.1 Setup与人数

| Token | 构成 | 起点 | 人数 |
|---|---|---:|---:|
| A | 普通成人 | `(2,6)` | 11 |
| B | 普通成人 | `(3,7)` | 10 |
| C | 小满、阿澄、前厅值守员；不可拆分 | `(4,7)` | 3 |
| D5 | 4名需协助成人+E01既有维修员 | `(7,5)` | 5 |

撤离对象为`11+10+3+5=29`；纪存、唐胶、兜灯另计，总人数`29+3=32`。维修员从Setup起就在D5内。

### 3.2 R1

1. 跌跌从`(1,7)`移动3格到锚点`(1,4)`，消耗一次情境动作复位主闸。
2. 机器犬从`(7,7)`抵达侧门`(7,6)`，消耗一次情境动作开门；一台贴片机进入，机器犬挂接D5。此处不生成维修员或新Token。
3. 撤离自动相位：A到`(2,4)`，B到`(3,5)`，C到`(4,5)`；D5只完成挂接，仍在`(7,5)`。
4. 环境相位：路径框读取标准路线并进入`RECLOSING`。

R1结束时`0/4 Token`位于黄线。

### 3.3 R2

1. 跌跌在传感锚点执行玩家确认的`主动侧倒`，路径框进入`JAMMED_R2_AUTO_ONLY`。
2. 机器犬处于D5挂接锁定，不能独立移动或使用情境动作。
3. 撤离自动相位：A由`(2,4)`到`(2,2)`；B由`(3,5)`到`(3,3)`；C由`(4,5)`到`(4,3)`；D5连同机器犬由`(7,5)`沿路线移动3格到`(5,4)`。
4. 堵轨在本次撤离自动相位后过期。

R2结束时只有A集结，即`1/4 Token`；B/C处于最终引导格，D5处于门位，不得提前结算胜利。

### 3.4 R3

1. 选择`(3,8)`或`(5,8)`：进入`BLOCKED_BY_DOUDENG`，无行动/状态损失返回`AIM_PREVIEW`。
2. 重新选择`(4,8)`：进入`SAFE_ANGLE_CONFIRMED`；馆守Z场景支援使胸灯`SPENT`、路径框`UNANCHORED`。
3. 最终撤离自动相位：A保持`(2,2)`；B到`(3,2)`；C到`(4,2)`；D5连同机器犬移动2格到`(5,2)`。
4. 此时首次达到`29/29 people; 4/4 tokens`，战斗只产生本地Clear回执；尾声完成后由`RT013S`一次性持久提交。

成功路径闭合。若三回合结束时少于29人或4枚Token，进入`RT011F/GB020`重试且零持久提交；危险胸灯预览本身不会制造误伤或失败提交。

## 四、S02机器犬连续性

**判定：`PASS`**

S02三处生成合同均已改为读取E01结果，而非重复E01事件：

- `V358U002-05.signature_or_rule`：读取`ALL_29_STAGED_FRONT_HALL_NOT_CITY_SAFE`，侦察前厅至建筑出口烟流、牵引C3、稳住消防软管，明确“不重复生成或救出维修员”。
- `V358ACT002-05.action`：同样规定机器犬不重复寻找维修员，而是帮助人员真正离楼。
- `V358LOAD002.unit_gameplay_consequence`：保留相同限制与E02动作。

生成器源同时具有：

- `PREVIEW_ACTION_OVERRIDES[("V357-C01-S02", "V353U040")]`
- `SLOT_SIGNATURE_OVERRIDES[("V357-C01-S02", "V353U040")]`

所以当前生成表不是一次性手改，重新生成也不会恢复“再次拖出最后一名维修员”的旧模板。

## 五、白函生成资产分期

### 5.1 E02

**判定：`PASS`**

- `V358U002-02`：`remote_command_presence / not_player_controlled_no_grid`。
- `V358ACT002-02`：只有远程语音、重框投影、区域改报与从机调度；无实体格、无HP、不可受击。
- `V358ASSET002-02`：资产类型为`remote_projection_and_voice`，动画范围仅远程语音、重框投影与区域重框；计数边界为`remote_projection_non_count_until_physical_body_S03`。

### 5.2 E03

**判定：`PASS`**

- `V358U003-03`：`enemy_or_boss`，生命周期为`first_visible_physical_body_and_first_battle`。
- `V358ACT003-03`：完整身体占格、切图、调度贴片机/针车、承受地形冲击、右肩与内收索损伤、带伤撤离。
- `V358ASSET003-03`：`full_enemy_rule_set_shared_frame_family_plus_complete_boss_actions_damage_and_retreat`。

### 5.3 生成器耐久性

生成器源中同时存在并匹配当前生成表：

- S02/S03 `PREVIEW_ACTION_OVERRIDES`
- S02 `SLOT_SIGNATURE_OVERRIDES`
- S02/S03 `SLOT_LIFECYCLE_OVERRIDES`
- S02/S03 `SLOT_LIFECYCLE_REVIEW_OVERRIDES`
- S02 `SLOT_PARTICIPATION_CONTROL_OVERRIDES`
- S02/S03 `SLOT_ANIMATION_SCOPE_OVERRIDES`
- S02远程资产类型、复用方式和非计数边界Override

因此没有发现生成器把E02回退为实体Boss，或把E03降回受限首显动作的迹象。

## 六、机器检查旁证

1. Runtime、Graybox及全部`v35_8_slot_*`表未发现TSV列数错位。
2. `python3 scripts/check_v35_8_slot_loadout.py`返回成功：95个槽位及manifest/action/source/selector/lifecycle/asset/high-density合同闭合。
3. 本席没有据此自动给`PASS`；放行依据是前述四项定向字段、三回合纸演、S02人口连续性及白函两阶段资产的人工交叉验证。

## 七、残留与最终放行

**范围内残留：无。**

- `GPR3-01=CLOSED`
- `GPR3-02=CLOSED`
- `GPR3-03=CLOSED`
- `GPR3-04=CLOSED`
- `S02_ROBOT_DOG_REPAIR_WORKER_DUPLICATION=FALSE`
- `BAIHAN_E02_REMOTE_NO_GRID=TRUE`
- `BAIHAN_E03_FULL_PHYSICAL_BOSS=TRUE`

最终判定：`PASS`。C01E01的游戏制作/关卡合同可结束定向返修，并向C01E02输入层放行；本回执不对剧情质量、角色对白或C01E02正文作延伸评价。
