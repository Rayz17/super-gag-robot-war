# C01E02｜G2-A.1-R2制作人部分签收与R2C接触舞台闭环唯一任务书

> 日期：2026-08-19  
> 状态：`R2_GEOMETRY_CONSUMER_ACCEPTED / CONTACT_STAGING_R2C_REQUIRED / ART_STILL_FROZEN / G2_B_BLOCKED`  
> Owner：新“主程序-2”原任务续作；不得resume／fork legacy主程序  
> 不构成：视觉成片批准、真实美术接入、UA91、Runtime晋级、G2-B、Canon修改

## 1. 制作人实际验收结论

制作人已读取77号全部回执，逐张查看7张1280×720 Godot root viewport actual frame，并从仓库根目录复验`delivery-hashes.sha256`全部通过。

### 1.1 可签收的R2能力

- north／east／south／west与40×20菱形投影一致；
- route逐段facing与endpoint settle facing分离；
- 1×1／2×2／3×3使用footprint bottom-center、binding pivot／display scale与footpoint z；
- 错误`view_space`、`camera_contract_id`与pivot fail closed；
- 显式稀疏clip与签名alias消费者成立；
- A4六层共同2400×1350 canvas、origin、crop与mask注册成立；
- impact／target socket、flash、debris、impulse与recoil能共享同一几何源。

以上是Candidate几何消费者签收，不是画面质量签收。`real_art_loaded=0`、`g2_b_allowed=false`、`integrated_visual_playtest_ready=false`继续有效。

### 1.2 条件接受的遮挡策略

“50% fade＋footpoint提示”只接受为R2代理方向，不冻结为成片策略。当前实现是单位脚点命中mask后让整张roof／foreground统一降至50%，提示也只是调试圆环，不是真实机体轮廓。

G2-A.2必须将其升级为局部遮挡判定与局部fade／cutout，并给真实复合Actor提供可读轮廓；最终规则仍需在`GF_PLAN_RECOMPOSED`／`GF_CONTACT_RECOMPOSED`中视觉验收。

### 1.3 不签收的接触舞台

- `A_CURRENT`为东西接触边，却宣称馆守Z south／BREAKER north正面承接，否决。
- 只把A移到`[19,9]`会与当前B规划终点重合，而现有回执没有把接触后的位移差写回世界，不能单独签。
- `B_CURRENT`在巨体接触时仍朝east，只能读成侧身承撞，否决。
- `B_T3_CONTACT_TURN_SOUTH`方向正确，但必须与A的新站位、B的真实后退结果、第二轮路线和城市炮侧甲窗口一起回放，不能单项签。
- 改BREAKER公开北冲轴来迁就A的方案破坏冻结意图与侧甲窗口，否决。

因此R2状态为“通用几何消费者完成；正式A/B接触舞台未闭环”。美术继续冻结。

## 2. 制作人签定的`STAGGERED_FRONT_CONTACT_V1`

两种策略共享同一公开敌方意图：BREAKER保持`[20,13] → [20,12] → [20,11]`直线向north冲锋，朝向north，不读取玩家未提交草案。两路都必须形成south对north正面承接，但以横向错位保留策略差异：

```text
A contact: guardian [20,9] south → breaker [20,11] north
           full two-cell front edge; impact socket [20.5,10.5], raw [-480,450]
B contact: guardian [19,9] south → breaker [20,11] north
           one-cell offset front edge; impact socket [20,10.5], raw [-500,440]
common contact normal   = [0,1]
common approach/impulse = [0,-1] → screen [40,-20]
```

不得用Sprite体积、FX或镜头掩盖错误矩形；正式Sprite socket只在这个共同几何上做局部像素校准。

### 2.1 A｜卡位迎撞

- 规划路线改为下侧直接线：`[15,11] → [16,11] → [17,11] → [18,11] → [18,10] → [19,10] → [19,9] → [20,9]`，正好7步；T1车辆先行后才占住其旧通道，必须用时间线证明不穿插。
- endpoint／settle facing：`[20,9] / south`。
- 主动作：`BODY_INTERCEPT`；馆守Z在T2前已经正面架住冲线。
- T3.00在A socket接触；视觉recoil到`[20,8.5]`，离散下一轮anchor保持`[20,9]`。
- BREAKER接触后保持A结果的较浅侵入／较早偏开语义，目标离散anchor为`[21,11]`。
- A继续承担较低热量、较宽第二轮时序、较大路损／警戒设施代价。

### 2.2 B｜护线预备

- 保留当前上侧宽路线：`[15,11] → [15,10] → [16,10] → [17,10] → [18,10] → [19,10] → [19,9]`。
- endpoint settle facing仍为`east`，用于T2的`PROTECT_LANE_RESPONSE / LATERAL_BODY_DEFLECT`。
- 提交摘要和预览必须明确显示：`east护线 → T3接触触发south brace`。该变化是准备反应的interaction-facing，不得悄悄覆盖玩家所见朝向。
- T3.25在`[19,9]`转为south，以相对A横向错开一格的前缘正面承接；因到位较迟且已先做护线反应，视觉recoil到`[19,8.5]`，离散下一轮anchor仍为`[19,9]`。56号允许“多退一格**或**热量更高”，本轮选择保持位置并以显著更高热量和0拍余量表达代价。
- BREAKER保持B结果的更深侵入／更晚偏开语义，目标离散anchor为`[21,10]`。
- B继续承担更高热量、更紧第二轮时序，但保住车辆、警戒设施和较小路损。

### 2.3 A/B差异不得压平

两路虽然在T3使用同一正面接触anchor与socket，但以下差异必须在画面、world mutation与第二轮约束中共同成立：

| 字段／读法 | A | B |
|---|---|---|
| 规划路线 | 下侧直达、主动作迎撞 | 上侧护线、准备反应 |
| T2姿态 | 已south brace | east侧推小体 |
| T3接触时点 | `T3.00` | `T3.25`且先转south |
| 接触前馆守Z | `[20,9]`，全两格正面接触 | `[19,9]`，横向错一格接触 |
| 接触后馆守Z | `[20,9]` | `[19,9]`，横向位置不同且热量显著更高 |
| 接触后BREAKER | `[21,11]` | `[21,10]`，侵入更深 |
| 热量／时序 | 低热、宽余量 | 高热、紧余量 |
| 环境代价 | 路损／警戒设施更重 | 车辆／设施更稳 |

不能只改文本、标签或演出offset。

## 3. G2-A.1-R2C唯一施工范围

### 3.1 必须修改

1. 在Candidate profile、resolver、fixtures和presentation中实现上述A/B路线、settle facing、B interaction-facing、接触后离散anchor与既有差异字段。
2. 将“规划终点”“接触姿态”“接触后world anchor”拆成明确字段／事件，禁止继续用一个`final_facing`或endpoint冒充三个阶段。
3. 更新第二轮A/B合法路线：
   - A必须走`[20,9] → [19,9] → [18,9] → [17,9] → [16,9] → [15,9] → [14,9] → [14,10] → [15,10] → [16,10] → [17,10]`；禁止先走`[20,10]`，因为会让2×2馆守Z穿进post-A BREAKER `[21,11]`的3×3占地；
   - B保留`[19,9] → [18,9] → [17,9] → [16,9] → [15,9] → [14,9] → [14,10] → [15,10] → [16,10] → [17,10]`，同样不得穿过post-B BREAKER `[21,10]`的3×3占地；
   - route planner／preview／resolver必须读取上一轮动态实体footprint阻挡，不能继续只检查静态terrain；
   - 两路都须在10步上限、热量与时序约束中可成功；A的geometry-derived `efficient_steps`改为10，长裂三格逐格计费后目标为`remaining_margin=1 / heat=68`；B保留9步路线并对一格小体压力计费，目标为`remaining_margin=0 / heat=88`。两者都须由同一resolver回执而非手填。
4. 城市炮必须仍在真实接触偏轴后取得侧甲射界；T4不再打固定anchor，而要命中post-contact BREAKER的east side-armor socket：A约`[24,12.5]`，B约`[24,11.5]`，炮源保持`[29,2]`。公开意图仍是冻结的条件射击，实际socket只由已结算接触状态派生；`side_armor_exposed`必须检查post姿态、side socket与炮线，禁止继续用`giant_contact && small_deflected`两个布尔值冒充几何射界。
5. 预览／提交摘要必须让玩家在执行前读到A的正面迎撞与B的“先护线、接触时转正、代价是更高热量与零拍余量”。

### 3.2 必须回归

- T1应急车先行，不与两路最终占位产生时序穿插；
- T2小体在A/B中均被挡开且仍存活，B准备反应确实触发；
- T3双方矩形只沿正确接触边相邻，不重叠、不隔空；
- A/B post-contact `guardian_position / guardian_heat / breaker_depth / road_damage / warning_facility_state / swarm_positions / remaining_timing_margin`均被第二轮读取；
- A/B第二轮取盾、挡赤红、最后车辆与关门仍能分别成功；
- 第二轮preview与execute均拒绝任何2×2馆守Z占地与post-contact 3×3 BREAKER占地重叠的route；
- 城市炮侧甲窗口、路裂、red charge与接触socket同源；
- 现有R2几何、11项Golden Slice/R1回归、全仓Godot与Canon隔离继续通过。

### 3.3 必交actual frames

至少新增四张1280×720 Godot root viewport帧：

1. A的T2 south brace与下侧路线；
2. A的T3正面contact及A post anchors／力向量；
3. B的T2 east护线、预览中的T3 south interaction-facing；
4. B的T3.25正面contact、B post anchors与“一格差”对照。

代理矩形必须画出footprint、contact edge、socket、pre／post anchor和屏幕受力箭头；不得只给文本表。

## 4. 写域、停止门与回执

写域沿用77号，仅增加：

- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a1-r2c/**`

不得写Canon、Reader、正式美术、A4/A5/A9源、默认入口或save；不得git add／commit／clean。

完成后提交：input receipt、A/B phase table、R1→R2 mutation proof、四张actual frame manifest、专用与回归测试、completion report、delivery hashes。

R2C完成后仍停在制作人实际帧签收门。未签前不得派A9.1-A6-S、G2-A.2、UA91、A9.1-B或G2-B。

## 5. 与78号DAG的关系

78号中的`P78-R2制作人几何签收＋接触舞台裁决`现拆为：

```text
R2通用几何消费者部分签收（本文件已完成）
→ R2C实现STAGGERED_FRONT_CONTACT_V1并回放A/B到第二轮
→ 制作人查看R2C actual frames并签exact PLAN／CONTACT几何
→ 才开放A9.1-A6-S与G2-A.2并行
```

这次新增窄门不是继续在夹具上空转，而是关闭会直接决定美术方向、接触姿势、后退帧、炮线和第二轮起点的最后一个空间矛盾。
