# C01E01 Godot Runtime Parity Audit v1

> Status: `candidate_runtime_parity_20_verified_0_partial_0_missing`
>
> Runtime target: `C01E01_RT001..C01E01_RT015`，含 `RT010A / RT011F / RT011B / RT011Q`，共 20 行。
>
> Graybox target: `C01E01_GB001..C01E01_GB022`，共 22 行。
>
> Boundary: 本报告证明当前 Godot 候选逻辑与 E01 Runtime/Graybox 合同可逐行追溯；不证明正式美术、最终动画、真人节奏、平台导出或商业完成度。

## 1. 审计方法

本轮把“能打通三回合”拆成四类证据：

1. 权威 Runtime 合同 `C01E01-runtime-contract-v1.tsv`；
2. 权威 Graybox 常量 `C01E01-graybox-constants-v1.tsv`；
3. 当前 Graph、Battle JSON、Scenario Session 与直接/整话测试；
4. 十张 1280x720 的 Narrative、Spatial、Tactical 视觉证据。

`scripts/check_c01e01_godot_runtime_parity.py` 要求 20 行合同与证据矩阵顺序完全一致。`scripts/check_c01e01_runtime_graybox.py` 则直接读取 Battle JSON，验证 8x10 地图、四条路线、三回合步数预算、四个端点、三枚反光位和失败检查点。任一部分实现、证据令牌漂移、缺图或常量偏移都会失败。

## 2. 当前结论

| 审计层 | 已验证 | 部分 | 缺失 |
|---|---:|---:|---:|
| Runtime Contract | 20 | 0 | 0 |
| Graybox Constants | 22 | 0 | 0 |

当前 E01 候选实现达到 `20/20 Runtime + 22/22 Graybox` 一致性。这个结论覆盖可执行状态、失败语义、路线物理、Episode 接续和当前候选画面。

## 3. 本轮修正的结构性错误

### 3.1 机器犬只在 R1 拥有独立行动

机器犬抵达侧门后一次完成三件事：接受一台贴片机、自动认领 D5 中既有维修员、与 D5 建立牵引。此后它与 D5 共用每个自动移动格，R2-R3 不再可选，也没有第二次“绑定”或“守线”命令。这样不会把同一个机器决定重复向玩家收费，也不会生成第五个人群 Token。

### 3.2 四组人不再瞬移到回合终点

四条路线与回合预算已经写入 Battle JSON：

| 组 | R1 | R2 | R3 | 总边数 |
|---|---:|---:|---:|---:|
| A11 | 2 | 2 | 0 | 4 |
| B10 | 2 | 2 | 1 | 5 |
| C3 | 2 | 2 | 1 | 5 |
| D5 | 0 | 3 | 2 | 5 |

Session 按 Tick 和固定优先级逐边验证起点、终点、正交相邻、占用与路线索引，共生成 19 条移动回执。`29/29` 与 `4/4` 从四个真实端点反算，不再由第三回合直接赋值。

### 3.3 漏动作会阻塞，不会提前判负

结束阶段始终合法。R1 漏开侧门时，A/B/C 继续移动，只有 D5 停住；R2 漏主动侧倒时，四组人在本轮自动阶段停住。路径框和环境仍结算，Session 写入不完整回执并进入下一回合。

只有 R3 环境阶段结束后仍不足 `29/29、4/4` 才判负。失败从 `battle_start` 重试，不写 World Fact、Episode 快照或战斗结果。

### 3.4 反光角拥有完整且可退的状态

胸灯现在执行：

```text
READY > AIM_PREVIEW > SAFE_CONFIRM > SPENT
```

左右两个危险角被兜灯挡回 `AIM_PREVIEW`，不消耗跌跌行动，也不触发失败；中央安全角确认后，馆守Z只完成外瓣灯与微小保护转身，仍是场景支援而非首次可控机体。

### 3.5 Battle Clear 与持久化边界分离

本地 Battle Clear 不写 Episode 结果。后续 Narrative 明确演出跌跌自己走完最后四格回到充电位、机器犬确认 D5 后解除牵引并回充电位。七海从私人语音转为公务风险只读频道；E01 不存在她的系统改写命令。

纪存发送真实但不完整的消防路线后，外网捕获路由地址与声纹。门、灯、数字钥匙、泵四令依次落下，只有终端 `C01E01:RT013S:ATOMIC_SNAPSHOT:V01` 提交唯一物理快照。

## 4. 直接失败矩阵

专项测试当前覆盖：

- R1 只复位主闸：A/B/C 各走两格，D5 原地，继续 R2；
- R2 不主动侧倒：四组零移动，继续 R3；
- R3 在此前失步后选中安全角：仍因端点不足而只在 R3 末失败；
- 三回合全部提前结束：前两回合不失败，第三回合末失败；
- 机器犬 R2 选取被拒绝；
- 危险反光角零成本返回；
- 成功路线正好 19 条边，C3 不拆组，D5 维修员不漂移；
- E01 战场没有白函身体、格位、HP、攻击或反击。

## 5. 机器回执

```text
C01E01_RUNTIME_GRAYBOX_CHECK PASS
constant_rows=22 verified=22
grid=8x10 routes=4 route_edges=19 visuals>=8

C01E01_GODOT_RUNTIME_PARITY_CHECK PASS
contract_rows=20 matrix_rows=20
verified_current=20
partial_current=0
not_implemented=0
visual_evidence=10
```

同时通过：

- C01E01 Story-first P5 smoke；
- C01E01 Story-first Episode Integration smoke；
- Multi-play Content Compiler smoke。

当前 E01 Bundle 指纹：

```text
c6af27a95fbaa48e7eba22ac4e2799569885037c729e860379511b01262ddc9d
```

## 6. 证明边界

本审计不证明：

- 小机器、人群 Token、馆守Z与贴片机已经拥有正式 Sprite 和逐帧动画；
- 19 条移动边虽然已按正式回执逐边插值播放，但单位仍缺正式步态Sprite、音效、镜头和环境联动动画；
- 三回合目标时长、首次理解率、手柄操作和失败恢复已经过真人测试；
- 正式音效、语音、Cut-in、镜头停顿与平台导出完成。

后续生产打磨可以改善演出，但不得重新引入机器犬重复行动、端点瞬移、R1/R2 提前失败、白函提前实体化或 Battle Clear 提前持久化。
