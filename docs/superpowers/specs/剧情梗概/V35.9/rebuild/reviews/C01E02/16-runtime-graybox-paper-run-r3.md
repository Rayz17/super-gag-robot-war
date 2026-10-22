# C01E02 Runtime / Graybox 确定性纸演 r3

> Status: `PASS_FOR_ORIGINAL_GAMEPLAY_SEAT_RECHECK`
>
> Scope: 对 Gameplay r3 的 `GP3-01..09` 做修补后重放；本文件不是独立玩法席最终 PASS。
>
> Machine checker: `scripts/check_c01e02_runtime_graybox.py`

## 1. 固定输入与文件指纹

| 文件 | SHA-256 |
|---|---|
| `C01E02-四张封存令-v1.md` | `b0b037dcc38a378689ba463dcf42383a2d7674d739e201e3469034a565c4c917` |
| `C01E02-runtime-contract-v1.tsv` | `c9a7e8e27d6923cdc9bcd033ab4be3384445eb69c579039661a220894824cdfc` |
| `C01E02-graybox-constants-v1.tsv` | `cd391f6fdd807048383fbaff2fdcbe82f39781009d2946e97175bb4b56ea9a1b` |
| `C01-逐章重构地图-v1.md` | `937bac5994a4811f5b11cb8b0527164097c13ca82bce048695b7f788a50cdff0` |
| `check_c01e02_runtime_graybox.py` | `5198441ce8c62f26610b964b188a4c9a135c28457db535473abade10d9590dbe` |

纸演读取上述版本。后续任一文件变化，都必须重跑检查并更新指纹，不能沿用本结论。

## 2. GP3修补闭合表

| 项 | 修补 | 可复算证据 | r3纸演 |
|---|---|---|---|
| `GP3-01` F2A撞机器犬 | F2A改走上门口`(1,6)>(2,6)>(3,6)>(3,7)`；F2B仍走下门口；机器犬固定`(1,7)` | `GB033/038`、`RT032F/033` | PASS |
| `GP3-02` 纪存撞跌跌 | 纪存路线改为`(10,10)>(10,9)>(9,8)>...`，不再进入`(9,9)` | `GB033/039/045` | PASS |
| `GP3-03` 绕过唯一坡道 | 纪存路线强制包含唯一坡道边`(10,9)>(9,8)` | `GB002/039` | PASS |
| `GP3-04` A11禁切角 | 明示`(2,5)`为门前可走格；`(1,6)`本就为楼外安全格 | `GB001/003/012` | PASS |
| `GP3-05` 动态占格定义 | 禁切角检查固定地形/关闭设施；动态实体只封其落点，不把正交侧格变成墙 | `GB001/016/045` | PASS |
| `GP3-06` R2相位错位 | 标尺机在工作人员相位只显示意图；消防选择结算后，敌方相位才实体接触并被挡回 | Episode §5、`RT010/018-020`、`GB019/021/040` | PASS |
| `GP3-07` 热耐久/烟3 | 删除不存在的Token热耐久；两条R2分支分别写出R3漏补救的真实失败链 | Episode胜败、`GB017/022/043`、`RT025/026G` | PASS |
| `GP3-08` 假探索选择 | 三证据改为固定玩家动作；烟隙由角色按实时温度调度，不再承诺未实现的路线选择 | Episode §3、`RT004-007` | PASS |
| `GP3-09` 地图旧口径 | 四令主体拆清；R4池归零，F2入场后才新发R5点，保护五人出口 | C01地图E02行与§E02-1 | PASS |

## 3. 路径、禁切角与占格重放

### 3.1 四枚撤离Token

检查器从区域矩形、中央轴、三格西门、门前格`(2,5)`和四格楼外端点重建可走地形，再逐边验证：

1. 每条边的`dx/dy`均不超过1，且不是零移动。
2. 每条对角边的两个正交地形侧格均开放。
3. 按`C3 > B10 > D5 > A11`的每tick优先级推进；后走Token可以进入本tick已腾空的格，不能交换或进入仍被占用的落点。
4. 四回合步数分别为：
   - A11：`3/2/3/3`
   - B10：`2/3/3/3`
   - C3：`2/2/2/2`
   - D5：`1/2/4/4`
5. R4精确终点仍为A`(1,5)`、B`(1,6)`、C3`(1,7)`、D5`(1,8)`，人口仍为`11+10+3+5=29`。

结果：`TOKEN_ROUTES PASS`。

### 3.2 F2入场

- F2A：`(1,6)>(2,6)>(3,6)>(3,7)`。
- F2B：`(1,8)>(2,8)>(3,8)`。
- 两路同步推进时每tick目标格不同。
- 两路均不进入机器犬`(1,7)`、跌跌`(9,9)`、针车`(7,10)`、标尺机`(11,12)`或消防架桥机固定身体/腿格。
- 两人仍是R4完成后从城市消防外侧进入的新接驳员，不属于最初32人，也不写入参战编制。

结果：`F2_ENTRY PASS`。

### 3.3 五人退路

退路只证明R5斜撑完成后存在可走出口，不在R5自动搬运五人。为消除共享走廊的伪碰撞，证明按`唐胶 > 纪存 > 兜灯 > F2A > F2B`逐人释放；到达西门`x=2`即进入门外sink并清格。

- 唐胶从`(9,8)`沿侧带到`(2,8)`。
- 纪存从`(10,10)`先到`(10,9)`，再沿唯一坡道边进入`(9,8)`，随后走侧带；不经过跌跌`(9,9)`。
- 兜灯从`(10,4)`走`y6`通道到`(2,7)`。
- F2A、F2B分别从`(3,7)`、`(3,8)`退到对应西门sink。
- SEG3反折后中心格`(7,7)|(8,7)`被斜撑占用，但`(7,8)|(8,8)`侧带和`y6`通道保持开放。

结果：`FIVE_PERSON_EGRESS PASS`。

## 4. R2两分支与失败守卫

### `WATER_CURTAIN`

- R2先保人，D5烟值保持1；针车在敌方相位真实接触接口。
- R3必须消费1点`INTERFACE_FLUSH`。完成时针车退回、D5走到`(5,8)`，烟值低于3。
- 若漏掉冲洗，针车/泵站路线守卫先失败；D5留`(9,8)`，环境只把烟值加到2，不再错误声称单因必到3。

### `PREEMPTIVE_INTERFACE_FLUSH`

- R2先保工具，针车接触前退回；D5烟值升到2。
- R3必须消费1点`DELAYED_WATER_CURTAIN`。完成时D5走到`(5,8)`，烟值低于3。
- 若漏掉水幕且D5留`(9,8)`，环境由2加到3，明确硬失败。

两路都不改变代表路线唯一物理伤痕`FIRE_SUPPLY_BURNED`，但R2/R3过程、镜头和失败条件不同。结果：`R2_BRANCH_GUARDS PASS`。

## 5. 点池、相位与工具实体

| 回合 | 消防点 | 唯一合法消费 | 回合末 |
|---|---:|---|---:|
| R1 | 3 | 固定`SEG1>SEG2>SEG3`联合施工 | 0 |
| R2 | 1 | 水幕或抢先冲洗二选一 | 0 |
| R3 | 1 | 与R2选择匹配的补救 | 0 |
| R4 | 1 | 桥面冷却与慢速托盘保护 | 0 |
| R5 | 新发1 | F2入场后反折SEG3承梁 | 0 |

相位始终为`small_units > staff_work > fire_support > enemy_tools > evac_auto > environment > local_receipt`。Episode正文已把标尺机实际接触移到R2消防选择之后；针车/标尺均以机身、轨道、伸缩臂、接触和回弹端点存在，不是红线特效。

结果：`ROUND_POOLS PASS`。

## 6. 人口、失败回滚与唯一提交

- 输入人口：29名撤离对象在前厅，另有纪存、唐胶、兜灯三名核心人员，合计原始32人。
- D5托盘无驾驶员、无人格、无HP，不增加人口。
- F2为R4后进入的两名外部接驳员，不属于原始32人。
- R1-R4失败回SRPG设置且零持久化。
- R5失败回本地检查点，四Token继续隐藏在楼外，不重刷。
- `RT038`是唯一`ATOMIC_SNAPSHOT`行；`RT039`显式`NO_WRITE`。
- 白函远程预布完成前没有任何Episode持久提交。

结果：`ATOMIC_COMMIT PASS`。

## 7. 机器检查原始输出

```text
TOKEN_ROUTES PASS: adjacency, no-corner-cut, tick occupancy, R4 endpoints
F2_ENTRY PASS: target-distinct, Dog-safe, static-equipment-safe
FIVE_PERSON_EGRESS PASS: unique ramp, sequential sinks, no equipment overlap
R2_BRANCH_GUARDS PASS: branch-specific smoke and tool compensation
ROUND_POOLS PASS: R1-R4 spent, F2 creates new R5 point
ATOMIC_COMMIT PASS: one transaction, 29+3 input, F2 external
ALL C01E02 RUNTIME/GRAYBOX CHECKS PASS
```

## 8. 裁决边界

本轮证明 Gameplay r3 指出的字面不可执行问题已经进入可机器重放状态。它不代替原 Gameplay / Production 独立席：该席仍需确认地图规则在制作表达上清楚、路线修补没有制造新玩法假象，并在当前文件指纹上给出最终`PASS`或新`PATCH`。
