# C01E02 Runtime / Graybox 确定性纸演 r4

> Status: `PASS_FOR_ORIGINAL_GAMEPLAY_SEAT_RECHECK`
>
> Scope: 修复 Gameplay r4 的 `GP4-01`，并对既有路径、分支、点池和原子提交断言做全量回归。
>
> Machine checker: `scripts/check_c01e02_runtime_graybox.py`

## 1. 固定输入与文件指纹

| 文件 | SHA-256 |
|---|---|
| `C01E02-四张封存令-v1.md` | `b0b037dcc38a378689ba463dcf42383a2d7674d739e201e3469034a565c4c917` |
| `C01E02-runtime-contract-v1.tsv` | `c9a7e8e27d6923cdc9bcd033ab4be3384445eb69c579039661a220894824cdfc` |
| `C01E02-graybox-constants-v1.tsv` | `700dfdd1489c55ae538613fc821f0830529605700aa68da0417c8e1711adde30` |
| `C01-逐章重构地图-v1.md` | `937bac5994a4811f5b11cb8b0527164097c13ca82bce048695b7f788a50cdff0` |
| `check_c01e02_runtime_graybox.py` | `4c22793020e4a62a96c7ab0fb8cca7519ee72374f9e510da7246ed49db2785dd` |

后续任一被审输入变化，均须重跑检查并更新指纹；本记录不能跨版本借用。

## 2. GP4-01修补

### 2.1 原错误

r3声明按`唐胶 > 纪存 > 兜灯 > F2A > F2B`逐人释放。唐胶路线必经`(3,8)`，但该格在她行动时仍由F2B占据，因此旧纸演是假阳性。

### 2.2 当前合同

`GB039.production_rule`现在提供机器可读字段：

```text
release_order=F2B>Tangjiao>Jicun>Doudeng>F2A
```

五人的路线几何未改。顺序调整利用西门`x=2`作为完成路径后立即清格的出口sink：

1. F2B先由`(3,8)`退到`(2,8)`并离开占格集。
2. 唐胶沿侧带从`(9,8)`退到`(2,8)`，释放馆内侧带。
3. 纪存从`(10,10)`经唯一坡道边`(10,9)>(9,8)`进入侧带，不经过跌跌`(9,9)`。
4. 兜灯沿`y6`通道退到`(2,7)`。
5. F2A最后由`(3,7)`退到`(2,7)`。

### 2.3 动态占格重放

checker不再只分别验证五条路线。它从`GB039`解析`release_order`，以五个起点初始化动态占格；每一步拒绝进入尚未撤出的其他人所在格；到达`x=2`后才把该人从占格集移除。检查同时保留：

- 路径邻接与固定地形禁切角；
- 消防架桥机、机器犬、跌跌和工具机静态/设备占格；
- 纪存唯一坡道边；
- 西门sink和五人完整覆盖。

结果：`FIVE_PERSON_RELEASE PASS`。

## 3. 全量回归

| 检查域 | 结果 | 当前证明 |
|---|---|---|
| 四Token撤离 | PASS | 邻接、禁切角、逐tick动态占格及R4四个楼外端点成立 |
| F2入场 | PASS | 两路目标不同，不进入机器犬或固定设备格 |
| 五人退路 | PASS | 机器可读顺序逐步模拟，无人际碰撞，sink逐人清格 |
| R2/R3局部分支 | PASS | 护人水幕与抢先冲洗各有匹配补救和不同失败链 |
| 五回合点池 | PASS | R1-R4逐回合清零；F2入内后另发R5一点并消费 |
| 原子提交 | PASS | 只有`RT038`写持久快照；`RT039`只读；失败不留半套状态 |

## 4. 机器检查原始输出

```text
TOKEN_ROUTES PASS: adjacency, no-corner-cut, tick occupancy, R4 endpoints
F2_ENTRY PASS: target-distinct, Dog-safe, static-equipment-safe
FIVE_PERSON_RELEASE PASS: ordered human occupancy, sink clearing, unique ramp, static equipment
R2_BRANCH_GUARDS PASS: branch-specific smoke and tool compensation
ROUND_POOLS PASS: R1-R4 spent, F2 creates new R5 point
ATOMIC_COMMIT PASS: one transaction, 29+3 input, F2 external
ALL C01E02 RUNTIME/GRAYBOX CHECKS PASS
```

命令退出码为`0`。本纸演证明当前合同在声明顺序下可执行，但不代替原Gameplay / Production独立席的最终裁决。
