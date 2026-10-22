# C01E02 Gameplay / Production 最终定向复验 r5

- 复验日期：2026-07-15
- 复验席位：原 Gameplay / Production
- 复验范围：`GP4-01` 最终闭环，并回归 `GP3-01..09`
- 裁决：**PASS**

## 一、结论

无阻断项。

`GB039` 已提供机器可读的合法释放顺序 `F2B>Tangjiao>Jicun>Doudeng>F2A`；checker 确实从 TSV 解析该字段，验证五人完整且不重复，并逐步保留尚未撤出者的动态占格，到达 `x=2` sink 后才清格。当前 checker 退出码为 0，独立于 checker 的第二次手算也得到五人全部清出、占格集为空。

`GP4-01` 因此闭合。当前 Episode、Runtime 与 C01 地图指纹未较 r4 改变；Graybox 除五人释放顺序合同外的既有 GP3 规则保持成立。未发现路径、人口、点池、失败回滚、重复救人、已安全人员回刷、唯一提交或 HUD 回归。

## 二、当前输入指纹

| 输入 | SHA-256 |
|---|---|
| `C01E02-四张封存令-v1.md` | `b0b037dcc38a378689ba463dcf42383a2d7674d739e201e3469034a565c4c917` |
| `C01E02-runtime-contract-v1.tsv` | `c9a7e8e27d6923cdc9bcd033ab4be3384445eb69c579039661a220894824cdfc` |
| `C01E02-graybox-constants-v1.tsv` | `700dfdd1489c55ae538613fc821f0830529605700aa68da0417c8e1711adde30` |
| `scripts/check_c01e02_runtime_graybox.py` | `4c22793020e4a62a96c7ab0fb8cca7519ee72374f9e510da7246ed49db2785dd` |
| `19-runtime-graybox-paper-run-r4.md` | `0d61dc3c874536eb932f6ad9bc1cd8ecee70ed8fb8e71e0698e5a8d91cc39b79` |
| `C01-逐章重构地图-v1.md` | `937bac5994a4811f5b11cb8b0527164097c13ca82bce048695b7f788a50cdff0` |

纸演 19 第13-17行记录的五个受控输入指纹与当前磁盘一致；本轮未借用其裁决，只把它作为同版本证据核对。

## 三、GP4-01 最终复验

### 3.1 合同与解析

- `GB039`（Graybox 第40行）当前声明：

```text
release_order=F2B>Tangjiao>Jicun>Doudeng>F2A
```

- checker 第178-184行从 `GB039.production_rule` 正则解析 `release_order`，不是另写一份顺序常量。
- checker 第185-188行要求顺序无重复，且名称集合与五条 `egress_routes` 完全相同。
- checker 第190-210行以五条路线起点初始化 `human_positions`；每一步拒绝其他未撤人员当前占格；完成路线且到达 `x=2` 后才删除该人；最后要求占格集为空。
- checker 第164-176行仍保留逐边邻接、禁切角、静态设备占格、纪存唯一坡道边和跌跌凹位检查。

这已覆盖 r4 报告指出的漏检，不再以“五条路线分别连通”冒充“声明顺序可执行”。

### 3.2 当前机器执行

本轮实际执行：

```text
python3 scripts/check_c01e02_runtime_graybox.py
TOKEN_ROUTES PASS: adjacency, no-corner-cut, tick occupancy, R4 endpoints
F2_ENTRY PASS: target-distinct, Dog-safe, static-equipment-safe
FIVE_PERSON_RELEASE PASS: ordered human occupancy, sink clearing, unique ramp, static equipment
R2_BRANCH_GUARDS PASS: branch-specific smoke and tool compensation
ROUND_POOLS PASS: R1-R4 spent, F2 creates new R5 point
ATOMIC_COMMIT PASS: one transaction, 29+3 input, F2 external
ALL C01E02 RUNTIME/GRAYBOX CHECKS PASS
```

退出码：`0`。

### 3.3 独立顺序手算

R5 起点由 Runtime `RT033`（第39行）和 `GB033`（第34行）共同锁定：

```text
Jicun=(10,10)
Tangjiao=(9,8)
Doudeng=(10,4)
F2A=(3,7)
F2B=(3,8)
Diedie=(9,9) static recess
Dog=(1,7) outside
```

独立逐步结果：

| 顺序 | 路线结果 | 动态占格核验 |
|---:|---|---|
| 1. F2B | `(3,8)>(2,8)` | 先清掉旧冲突格 `(3,8)`；到 sink 后移出占格集。 |
| 2. 唐胶 | `(9,8)>...>(3,8)>(2,8)` | F2B 已清格，全程不撞其他四人；到 sink 后清格。 |
| 3. 纪存 | `(10,10)>(10,9)>(9,8)>...>(2,8)` | 必经唯一坡道边 `(10,9)>(9,8)`；不进入跌跌 `(9,9)`；唐胶已清出侧带。 |
| 4. 兜灯 | `(10,4)>...>(3,6)>(2,7)` | 不进入 F2A 的 `(3,7)`；该格只作为最后对角边的正交侧格，按 `GB001/016` 动态单位不会把侧格变成关闭地形。到 sink 后清格。 |
| 5. F2A | `(3,7)>(2,7)` | 兜灯已清 sink，最后一人合法离场。 |

复算终态：`active_human_occupancy={}`。五条路线不进入 Dog `(1,7)`、Diedie `(9,9)`、Needle `(7,10)`、Ruler `(11,12)`或消防架桥机固定机身／腿格。

`GP4-01`：**闭合**。

## 四、GP3-01..09 回归

| 项目 | 当前证据 | r5 结果 |
|---|---|---|
| `GP3-01` F2A 避让机器犬 | `RT032F/033`；`GB033/038`；checker 139-157 | F2A 走 `(1,6)>(2,6)>(3,6)>(3,7)`；四 Token 先隐藏；不进 Dog `(1,7)`。无回归。 |
| `GP3-02` 纪存避让跌跌 | `RT033/036G`；`GB033/039`；checker 171-176、190-210 | 纪存不进 `(9,9)`，声明顺序也不再被 F2B 阻断。无回归。 |
| `GP3-03` 唯一坡道 | `GB002/039`；checker 171-174 | 纪存强制包含 `(10,9)>(9,8)`。无回归。 |
| `GP3-04` A11 禁切角 | `GB001/003/012`；checker 57-73、114-137 | `(2,6)>(1,5)` 两侧 `(2,5)`、`(1,6)` 仍开放。无回归。 |
| `GP3-05` 动态占格定义 | `GB001/016/045`；checker 76-106、190-210 | 动态单位只封目标格；四 Token 与五人释放均按同一口径模拟。无回归。 |
| `GP3-06` R2 实体接触相位 | Episode 161、167；`RT010/018-020`；`GB019/021/040` | 工作人员相位只显示标尺意图；消防选择后才在敌方相位实体接触。无回归。 |
| `GP3-07` 烟3与 Token 热耐久 | Episode 313；`RT025/026G/040`；`GB017/022/043`；checker 216-230 | 无 Token 热耐久；WATER 漏补为工具／路线失败且烟2，PREEMPTIVE 漏水幕才升烟3。无回归。 |
| `GP3-08` 固定探索三证据 | Episode 111、272-274；`RT004-007` | 玩家固定执行三证链，不再承诺未实现的烟隙路线选择。无回归。 |
| `GP3-09` C01 地图口径 | C01 地图 47、68；Episode 81、211-215、308 | 四令责任分域正确；R4 归零、F2 入内后新发 R5 点、保护五人出口。无回归。 |

## 五、关键玩法合同回归

### 固定桥序与 Rig

`RT014`、`GB004/005/007/020` 仍锁定一次费用 3 的 `SEG1>SEG2>SEG3` 联合施工；错误预览零消耗；四腿不换格，R5 脚垫只在 `(3,10)` 格内滑移。Episode 151-153、291、304 与之相认。

### R2 真分支与 HUD

`RT019/020/025/026G`、`GB017/021/022/030/031/041` 仍保持两条不同中间状态：WATER 为 D5 烟1／针车接触／R3冲洗，PREEMPTIVE 为 D5 烟2／针车先退／R3迟发水幕。Episode 167、191、305-306 承认相同顺序和后果；HUD 显示烟值与工具预览。

### 点池、人口与 D5

- R1-R4 消防池仍为 `3/1/1/1` 且逐回合归零；`RT032F` 只在 F2 入内后生成 R5 新一点，`RT035` 消费后归零。
- `A11+B10+C3+D5=11+10+3+5=29`；三名核心构成原始 32；F2 为两名外部成年接驳员，不计原始 32 或万机馆编制。
- Episode 157 与 `GB015/044` 仍把 D5 定义为既有无驾驶员低速撤离托盘，不增人、不挂机器犬、不生成新单位。

### 失败回滚、唯一提交与 HUD 目标切换

- `RT031G/040`：R1-R4 失败回 SRPG setup，零持久化。
- `RT033/036F`：R5 失败回本地检查点，29 人 Token 保持隐藏，不回刷、不重复救援。
- `RT038` 仍是唯一 `ATOMIC_SNAPSHOT`；`RT039` 仍为 `NO_WRITE`；`GB036` 要求快照与全部 V35 键同生同灭。
- `GB041/042` 与 Episode 305、308 仍把 HUD 从 R1-R4 的 29 人撤离切到 R5 的五人退路，并持续显示 `29/29` 已在楼外。

以上均无回归。

## 六、最终裁决

**PASS**

`GP4-01` 已由机器可读顺序、checker 动态占格模拟和独立逐步复算三重闭合；`GP3-01..09` 及固定桥序、R2分支、点池、D5、失败回滚、唯一提交和 HUD 均保持成立。当前版本可通过 Gameplay / Production 最终定向复验，无 Runtime / Graybox 前置补丁要求。
