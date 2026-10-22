# C01E01 游戏制作 / 关卡合同终检回执 R3

> 审核席：独立游戏制作 / 关卡合同终检席  
> 审核范围：C01E01正文、Runtime Contract、Graybox Constants、C01逐章重构地图，以及`v35_8_slot_*`中`V357-C01-S01`至`S03`相关行  
> 审核方式：只做纸面复演与跨表交叉验证，不补剧情、不用作者意图替合同圆场  
> 最终判定：`PATCH`  
> 阻断级别：`LOCAL_PRODUCTION_PATCH_ONLY`，不需要重写剧情或重做三回合结构

## 一、结论摘要

C01E01的三回合主路径已经能够完成纸面复演：32名馆内人员的工作数成立，29名撤离对象被准确压成`A11+B10+C3+D5=29`四枚Token；维修员从战斗设置开始就在D5中，不会生成第五枚人口Token；29人只能在R3进入前厅黄线，R2没有提前提交胜利。白函的资产阶段也已闭合：E02只有远程语音、投影、区域改报与从机调度，不占格、无HP、不可受击；E03才首次获得完整实体Boss身体、占格、受击、损伤与撤退动作集。

本轮仍不能签`PASS`，原因不是剧情或关卡发动机失效，而是四处实现合同尚有双重解释：S01上游失败字段仍要求失败后推进四令；机器犬挂接D5后没有锁定独立行动经济；三个胸灯反射位没有确定的安全/危险解析表；唯一物理快照没有使用上游同名状态键，也漏写了烟与喷淋的最终物理状态。四项均可用字段级补丁解决。

## 二、三回合纸面复演

### 2.1 战斗设置

| 对象 | 设置状态 | 数量校验 |
|---|---|---|
| A | 11名普通成人，起点`(2,6)` | 11 |
| B | 10名普通成人，起点`(3,7)` | 10 |
| C | 2名未成年人+1名前厅值守员，起点`(4,7)`；不可拆分 | 3 |
| D5 | 4名需协助成人+1名维修员，起点`(7,5)` | 5 |
| 核心工作人员 | 纪存、唐胶、兜灯，不进入撤离Token | 3 |

因此：撤离对象`11+10+3+5=29`，馆内人类总数`29+3=32`。正文、Runtime、Graybox与C01地图一致。

### 2.2 R1

1. 跌跌由`(1,7)`移动3格至路径框锚点`(1,4)`，使用1次情境动作复位主闸。
2. 机器犬由`(7,7)`到侧门`(7,6)`，使用1次情境动作开门；D5中的维修员是既有人口，不生成新Token。开门允许一台贴片机进入，并使机器犬与D5挂接。
3. 撤离自动相位后：`A=(2,4)`、`B=(3,5)`、`C=(4,5)`、`D5=(7,5)`。
4. 环境相位读取标准路线，路径框进入`RECLOSING`。

R1不产生黄线集结，不提交持久胜利状态，成立。

### 2.3 R2

1. 跌跌在锚点使用`主动侧倒`情境动作，玩家确认后路径框进入`JAMMED_R2_AUTO_ONLY`。
2. 撤离自动相位后：`A=(2,2)`、`B=(3,3)`、`C=(4,3)`、`D5=(5,4)`。
3. A单独抵达黄线；B、C位于最终引导格；D5抵达路径框门位。此时只有`1/4 Token`集结，不得提前胜利。
4. 堵轨只覆盖R2撤离相位，随后过期。

R2的Token位置、移动步数和`A_STAGE_BC_FINAL_LINE_D5_GATE`回执相符。

### 2.4 R3

1. 玩家进入胸灯瞄准预览；唐胶执行离散反射位，兜灯在提交前否决危险角。
2. 安全角确认后，馆守Z外圈胸灯进入`SPENT`，控制膜卷起，路径框进入`UNANCHORED`。
3. 撤离自动相位后：A留在`(2,2)`，B到`(3,2)`，C到`(4,2)`，D5移动2格到`(5,2)`。
4. 此时且仅此时得到`people=29/29; tokens=4/4`，进入战斗成功结算。

三回合成功路线在格数上成立；失败路线也能由“R1不开侧门/D5未挂接”或R3未完成安全照射产生。

## 三、重点闸门判定

| 闸门 | 判定 | 证据 |
|---|---|---|
| 29人 / 4 Token | `PASS` | 正文结算、`RT003/RT010A`、`GB002/GB010-013/GB019`完全同数 |
| D5维修员不增生 | `PASS` | `RT004`与`GB013`均明确维修员从Setup起已包含在D5中，不生成第五Token |
| R1-R3位置与步数 | `PASS` | 四条路线能按`auto=2/2/2/3/2`完成，R2只有A到黄线，R3才4/4 |
| 跌跌行动经济 | `PASS` | R1为移动3+复位，R2为主动侧倒情境动作；不存在同相位重复动作 |
| 机器犬行动经济 | `PATCH` | R1挂接成立，但挂接后是否仍可在R2/R3独立移动和行动未锁定 |
| 危险胸灯重瞄 | `PATCH` | 无消耗返回`AIM_PREVIEW`已写明，但三个反射位没有确定的安全/危险解析值 |
| 失败不提交 | `PATCH` | 本地`RT011F/GB020`正确；上游`V358GAME001.failure_pressure_contract`仍要求失败推进四令并删展区 |
| E01唯一期末快照 | `PATCH` | 只有一行`ATOMIC_SNAPSHOT`，但状态键与上游不同名，且快照正文漏烟/喷淋终态 |
| E02白函无格 | `PASS` | `V358U002-02`为`remote_command_presence/not_player_controlled_no_grid`；`V358ACT002-02`明确无实体格、无HP、不可受击；`V358ASSET002-02`仅远程投影与语音 |
| E03白函完整Boss资产 | `PASS` | `V358U003-03`为`enemy_or_boss`且首次实体首战；`V358ACT003-03`含占格、切图、调度、受击、损伤、撤退；`V358ASSET003-03`要求完整Boss动作集 |

## 四、必须修补的精确字段

### GPR3-01：S01失败合同与“失败不提交”相反

**冲突**

- `C01E01-runtime-contract-v1.tsv / C01E01_RT011F`：任务失败后从`BATTLE_SETUP`重试，不提交任何剧情或持久状态。
- `C01E01-graybox-constants-v1.tsv / C01E01_GB020`：同样规定`commit no story or persistent state`。
- `v35_8_slot_gameplay_contract_v35_8.tsv / V358GAME001.failure_pressure_contract`：仍写“失败必须让下一逻辑真实恶化：四张封存令进入，不按路线删展区”。这会使实现者把四令当作失败分支，而正文与Runtime规定四令只在成功后的消防路由/声纹捕获后进入。

**最小修法**

只改生成源中的`V358GAME001.failure_pressure_contract`并重生成V35.8表，目标值固定为：

```text
三回合未完成四枚撤离Token集结则MISSION_FAIL_TIMEOUT并从BATTLE_SETUP重试；不提交剧情、人员、失败计数、四令或展区删改状态。四令只由成功后的ADV_END消防路由与纪存声纹捕获触发。
```

`V358LOAD001.branch_or_next_carry`中的“四张封存令进入”是成功后的下一话承接，保留不改。

### GPR3-02：机器犬挂接D5后可被实现成“免费拖行+独立双动”

**冲突**

- `RT004.end_state`只有`DOG_ATTACHED_TO_D5_AND_ONE_PATCHER_ENTERED`。
- `GB009`仍给机器犬`move=3;context=1`，没有说明挂接后冻结独立行动。
- `GB013`又让D5在R2、R3分别自动移动3格和2格。若按字面实现，机器犬可一边随D5免费拖行，一边继续独立移动/开门，行动经济不闭合。

**最小修法**

1. 将`C01E01_RT004.end_state`改为：

```text
DOG_TETHERED_TO_D5_INDEPENDENT_MOVE_CONTEXT_LOCKED_UNTIL_D5_STAGED;ONE_PATCHER_ENTERED
```

2. 将`C01E01_GB009.production_rule`补为：

```text
R1 reaches and opens side door; after attachment RobotDog shares D5 evac_auto path/cell and has no independent move or context action in R2-R3 until D5 is staged at GB019
```

不需要增加新相位、新动画或新Token。

### GPR3-03：危险角可以重瞄，但纸面上没有一个可判定的危险角

**冲突**

`GB005`只列出三个反射位，`GB016/RT011B`只定义危险后的状态机；没有一行决定哪个离散位返回`BLOCKED_BY_DOUDENG`、哪个进入`SAFE_ANGLE_CONFIRMED`。因此“危险角无消耗重瞄”规则存在，但无法纸演，也无法写UI测试。

**最小修法**

在Graybox表新增一行：

```text
C01E01_GB022	reflector_resolution	(3,8)=BLOCKED_BY_DOUDENG;(4,8)=SAFE_ANGLE_CONFIRMED;(5,8)=BLOCKED_BY_DOUDENG	blocked socket returns to AIM_PREVIEW with no action/state cost; safe socket advances RT009>RT010; preview masks must visibly distinguish unsafe coverage before confirm
```

若美术最终交换左右编号，可以整体交换坐标，但必须保持“一处安全、两处危险”，并同步同一行；不能只靠演出临时判断。

### GPR3-04：唯一物理快照不是完全自包含的E02输入

**冲突**

- 上游V35.8和状态传播使用键`C01_PHYSICAL_SNAPSHOT`。
- `RT013S.end_state`使用`C01E01_PHYSICAL_SNAPSHOT_COMMITTED`，没有声明同名映射。
- `RT013`已经产生`SMOKE_IN_FRONT_HALL_SPRINKLER_FAIL`，正文和C01地图也把烟侵入、喷淋无压作为E02直接开局；但`RT013S.mandatory_outcome`的唯一快照未收录这两项。

**最小修法**

1. 将`C01E01_RT013S.end_state`改为：

```text
C01_PHYSICAL_SNAPSHOT=COMMITTED
```

2. 在同一行`mandatory_outcome`末尾追加：

```text
east-side smoke entering L1 front hall; L1 sprinkler dry/no pressure
```

3. 在正文“结算状态”只追加一条同名别名即可：

```text
C01_PHYSICAL_SNAPSHOT=RT013S_ATOMIC_PAYLOAD
```

`RT011`仍可作为战斗成功结算，但不得被保存系统或E02当成第二份Episode handoff；E02只读取`C01_PHYSICAL_SNAPSHOT`及已列出的独立剧情状态键。

## 五、已确认无需再改的部分

1. 不需要改变`A11_B10_C3_D5`拆分，也不需要给维修员新增单位或Token。
2. 不需要把29人提前判定为离开建筑；E01终点就是前厅黄线，城市安全在E02完成。
3. 不需要给危险胸灯角制造误伤Game Over；兜灯在提交前阻断、允许无损重瞄是正确教学。
4. 不需要把馆守Z的极小偏头算作首控；S01仍是受限场景支援，完整首控在S03。
5. 不需要把白函实体提前到E02。现有S02远程资产、S03完整Boss资产的三表口径已一致。
6. 不需要重做三回合地图。路线长度、Token终点和胜利时点都已经闭合。

## 六、复验与放行条件

完成上述四项最小补丁后，只需执行一次定向复验：

1. 重生成`v35_8_slot_*`，确认`V358GAME001.failure_pressure_contract`不再提交失败世界状态。
2. 重新纸演R1-R3，确认机器犬挂接后无独立双动，危险反射位能稳定返回预览，安全位才进入`SPENT/UNANCHORED`。
3. 搜索并确认E01只有一个对E02公开的`C01_PHYSICAL_SNAPSHOT`，其中包含烟侵入与喷淋无压。
4. 运行`python3 scripts/check_v35_8_slot_loadout.py`。本轮该脚本已通过，但它只证明V35.8表内闭合，不能替代上述跨表语义复验。

四项完成即可将本席结论从`PATCH`直接转为`PASS`；没有要求开启第四轮剧情创作或重写C01E01。
