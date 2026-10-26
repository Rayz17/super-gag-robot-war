# C01E02｜R2C制作人exact几何签收与精品视觉并行派工回执

> 日期：2026-08-20  
> 状态：`CANDIDATE_EXACT_GEOMETRY_REACCEPTED_BY_84 / A9_1A6_S_AND_G2_A2_RESUMED / REAL_ART_AND_G2_B_BLOCKED`  
> 制作人：新“制作人-2”  
> 不构成：视觉成片批准、UA91、真实美术接入、Runtime晋级、默认入口、Canon修改、付费批量生成批准

> 2026-08-20后续纠偏：制作人复核整屏演员时发现A路`Swarm01=[21,9]`与馆守Z`[20,9] / 2×2`发生地面占位重叠。83号已把唯一合法地面真值纠正为`[22,9]`；84号完成63项hash、核心测试与两张Actual Frame复验并重新签收。本回执现由84号恢复并行放行。

## 1. 权威与交付复验

本次按`chao-gag-canon`重新核验：当前V35正式活动点仍为C04 L5 `episode_e03`；C01E02本Demo只作为隔离Candidate切片推进，不修改馆守Z正式首控时序、C01 Reader、Hard／Working Canon或Runtime。

制作人从仓库根目录执行：

```bash
shasum -a 256 -c docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a1-r2c/delivery-hashes.sha256
```

55项全部`OK`。签收输入指纹：

| 输入 | SHA-256 |
|---|---|
| 79号R2C唯一任务书 | `55494be8c73b39806c9e1acf4b3d4fbab580e323fec6697f4e5e63296c5d5594` |
| R2C Actual Frame Manifest | `4bb072ec7eb2572d6bbf073ae6e4c67f1694a4407e4d9268270d8d4cd92a8487` |
| A4 Layer Registration Readback | `ca9e3c0d30c752c924836040392f0ca49ba9e79046d2eae1782c343c5846a6f0` |
| R2C Completion Report | `37883c9afd4afb312553a1cfdab934996779af252da55dcf6887c2432a8b60c2` |
| Contact Staging Receipt | `199b098524cb4cd7cfcd637d81ba0a2ee2509332d327867f8399178029af1d8c` |

制作人已实际查看五张1280×720 Godot root viewport帧。帧证明空间注册与接触几何；不证明真实轮廓、成片遮挡、连续时序、打击感或视觉品质。

## 2. 制作人签收结论

### 2.1 Candidate exact geometry重新签收

- `STAGGERED_FRONT_CONTACT_V1`连同84号`Swarm01=[22,9]`纠偏成为第一轮Scene-First视觉施工空间底板；其余接触几何未重开。
- A／B的规划终点、settle facing、contact facing、视觉recoil、离散post anchor已经分离。
- 2×2馆守Z与3×3 BREAKER以footprint bottom-center注册；接触矩形只沿合法前缘相邻，不重叠、不隔空。
- A／B第一轮world mutation由第二轮同一resolver读取；动态3×3 BREAKER占位同时阻断preview与execute非法路线。
- T4城市炮east-side socket由post-contact BREAKER矩形派生，不再由两个布尔值冒充。

### 2.2 明确不签收

- R2C半透明矩形Proxy不是地图Sprite产品质量。
- `fade 50% + footpoint ring`只作R2校准History；G2-A.2必须实现局部遮挡、局部fade／cutout与真实Actor轮廓策略。
- 五张帧由capture driver注入阶段状态，不等于45–75秒Session连续演出完成。
- 第二轮Actual Frame只画A路；B路第二轮只由resolver／session机器证明，本回执不宣称B路视觉完成。
- `11 fixture bindings / real_consumer_count=0 / real_art_loaded=0`继续有效。

## 3. 冻结给美术与程序的exact空间合同

### 3.1 共同投影与相机

```text
camera_contract_id     = A4_MAP_SPRITE_CAMERA_V1
view_space             = map_dimetric_40x20
grid                   = 32 x 18
tile_half_px           = [40,20]
projection_origin_raw  = [-880,-170]
viewport_px            = [1280,720]
map_viewport_rect      = [0,58,1280,584]
camera_center_raw      = [-720,350]
zoom                   = 1.0
safe_ratio             = 0.60
perspective            = orthographic / no convergence / no depth scale
```

方向映射继续以公式为权威：north右上、east右下、south左下、west左上；禁止把设计正／侧／背四视别名为地图cardinal。

### 3.2 A4共同画布

```text
canvas_size_px         = [2400,1350]
canvas_origin_raw_px   = [-1680,-350]
screen_top_left_px     = [-480,-370]
crop_rect_px           = [480,428,1280,584]
layer_count            = 6
```

六层必须共享canvas、origin、crop、filter和mask语义。A4现有`STATE_LAYERS`因混包仍不能冒充最终状态层；Scene-First可引用其拓扑和注册，不得宣称正式地图完成。

### 3.3 Hero视觉路径：A路

首个`GF_PLAN_TARGET`与`GF_CONTACT_TARGET`统一以A路作为Hero画面，先锁共同世界，不一次扩满A/B资产。

```text
A route                = [15,11] [16,11] [17,11] [18,11] [18,10] [19,10] [19,9] [20,9]
A settle               = guardian [20,9] south
BREAKER public route   = [20,13] -> [20,12] -> [20,11] north
A contact              = T3.00 / full 2-cell front edge
impact_socket_grid     = [20.5,10.5]
impact_socket_raw_px   = [-480,450]
contact_normal_grid    = [0,1]
approach_impulse_grid  = [0,-1]
recoil_screen_px       = [20,-10]
visual_recoil_anchor   = [20,8.5]
post_guardian_anchor   = [20,9]
post_breaker_anchor    = [21,11]
T4_side_socket         = [24,12.5]
T4_artillery_source    = [29,2]
GF_PLAN_focus_cell     = [19,10]
GF_CONTACT_focus_cell  = [20.5,10.5]
```

### 3.4 B路保留为系统必须支持的exact对照

```text
B route                = [15,11] [15,10] [16,10] [17,10] [18,10] [19,10] [19,9]
B settle               = guardian [19,9] east at T2
B contact              = guardian [19,9] south at T3.25
B impact_socket_grid   = [20,10.5]
B impact_socket_raw_px = [-500,440]
B visual_recoil        = [19,8.5]
B post_guardian        = [19,9]
B post_breaker         = [21,10]
B T4_side_socket       = [24,11.5]
B PLAN focus           = [18.5,10]
B CONTACT focus        = [20,10.5]
B R2 result target     = heat 88 / remaining margin 0
```

G2-A.2必须保持A/B读取与显示能力；但Scene-First首轮Hero图不要求同时生产B路完整可见像素。UA91通过后再扩B路稀疏状态。

### 3.5 第一轮回写与第二轮exact读取

T1应急车在馆守Z占住最终接触位前完成通过；该时序必须继续由T1–T5事件序列验证，不能只用静态占格推断。

```text
A R2 route = [20,9] [19,9] [18,9] [17,9] [16,9] [15,9] [14,9] [14,10] [15,10] [16,10] [17,10]
A R2       = 10 steps / heat 68 / remaining margin 1
A R1 world = guardian [20,9] / heat 24 / BREAKER depth 11 / road damage 42 / warning facility damaged / margin 4
A swarms   = [22,9] / [27,12] / [29,5]  # Swarm01由83号纠偏并经84号重新签收
A blocker  = post BREAKER [21,11] 3x3; route through [20,10] must reject

B R2 route = [19,9] [18,9] [17,9] [16,9] [15,9] [14,9] [14,10] [15,10] [16,10] [17,10]
B R2       = 9 steps / heat 88 / remaining margin 0
B R1 world = guardian [19,9] / heat 46 / BREAKER depth 10 / road damage 24 / warning facility active / margin 1
B swarms   = [22,8] / [28,12] / [30,6]
B blocker  = post BREAKER [21,10] 3x3; route through [20,9] must reject
```

`guardian_position / guardian_heat / breaker_depth / road_damage / warning_facility_state / swarm_positions / remaining_timing_margin`必须继续从第一轮`world_result`进入第二轮；禁止在视觉Proxy、UI或capture driver重造手填快照。

### 3.6 整屏演员、对象与意图轨迹

整屏目标不能只冻结两只巨体。`GF_PLAN_TARGET`以执行前公开意图态为唯一真值：

| 可见要素 | 当前实体／对象 | 公开意图或限制 |
|---|---|---|
| 馆守Z | `[15,11] / 2×2 / east` | A终点`[20,9] / south`只作2×2 ghost；服从3.3完整路线 |
| BREAKER | `[20,13] / 3×3 / north` | north冲锋`[20,13]→[20,12]→[20,11]`；终点只作3×3 ghost／走廊 |
| 应急车 | `[17,10] / 1×1 / east` | T1轨迹`[17,10]→[18,10]→[21,10]→[24,9]` |
| 突入小体01 | `[22,7] / 1×1 / west` | T2轨迹`[22,7]→[21,8]→[20,9]→[20,10]`，随后由馆守Z挡开 |
| 突入小体02 | `[26,12] / 1×1 / north` | 外围威胁，不得自由挪位 |
| 突入小体03 | `[29,5] / 1×1 / south` | 外围威胁，不得自由挪位 |
| 东侧撤离口 | `[31,7]` | 车辆路线终点语义；不是装饰门洞 |
| 东门警戒设施 | `[27,8]` | A路后果会受损；PLAN仍为active |
| 退役重盾 | `[14,10] / wall_hung_3_scorches` | 第一轮仍挂墙，严禁提前持盾或消失 |
| 东侧保护线 | rect `[20,5,12,7]` | 路线、威胁与冲撞读法的战术对象 |
| 城市边缘炮火 | source `[29,2]` | T4条件炮击来源；PLAN只作公开意图／时间线预示 |

`GF_CONTACT_TARGET`严格取T3.00：T1应急车实体已到`[24,9]`并离开落脚区；T2小体01必须仍存活并在83号纠偏后的合法地面格`[22,9]`；馆守Z／BREAKER取3.3接触实体anchor。小体02／03按A路resolved world显示`[27,12] / [29,5]`。退役重盾仍在`[14,10]`，保护线、撤离口和警戒设施不得为了构图被删除。

### 3.7 小体地面互斥与83号唯一纠偏

```text
A Swarm01 invalid History anchor = [21,9]
A Swarm01 sole ground anchor     = [22,9]
Guardian ground rect             = x20..21 / y9..10
BREAKER contact ground rect      = x20..22 / y11..13
Swarm01 ground rect              = x22 / y9
overlap                          = false
```

resolver、entity、T2 performance track、Overlay、Lookdev和后续Runtime消费者必须统一读取`[22,9]`。禁止airborne/display-only别名、视觉offset或隐藏小体绕过逻辑纠偏。83号已实现，84号已重新签收；81／82恢复并行。

### 3.8 确定性文案、策略第一读法与时态

以下文字由确定性UI排版，不交给ImageGen生成：

```text
当前目标 = 让应急车通过，挡开扑向东门的小体，并站到冲线前。
纪存通讯 = 人都在后面。把它引到南边去。
威胁1    = 应急车先穿过落脚区
威胁2    = 小体将在第二时点扑向东门
威胁3    = BREAKER沿直线冲入街区
五时点   = 应急车 / 小体 / 巨体接触 / 城市炮 / 赤红蓄能
A已选    = 卡位迎撞｜正面承接｜较低热量｜第二轮余量1
B备选    = 护线预备｜先east护线、接触前转south｜高热｜第二轮余量0
```

T3.00实体画面只允许已经发生的T1车辆通过、T2小体挡开，以及巨体接触瞬间的微裂、定向碎屑和水花。T4城市炮、T5赤红蓄能与完整路面翻起只能作为HUD下一时点预示，不得在`GF_CONTACT_TARGET`中实体发生。屋顶／前景必须保留并用局部fade、cutout或局部outline解决；禁止删层、全层50%透明或用大特效掩盖遮挡错误。

### 3.9 对旧Candidate接口阻塞字段的override

本回执是`c01e02-tactical-visual-interface-v1.json`旧R2阻塞字段的后续权威：

| 旧字段 | 80号后状态 |
|---|---|
| `a4_to_runtime_registration.status=BLOCKED` | R2C Proxy exact registration已签；真实地图美术仍Blocked |
| `round_1_contact_geometry.status=BLOCKED` | `STAGGERED_FRONT_CONTACT_V1`连同84号小体`[22,9]`纠偏已重新签收；Scene Target Lookdev恢复；real art handoff仍Blocked |
| `roof_foreground_policy=BLOCKED` | 仍未签成片策略；转由G2-A.2局部遮挡门处理 |

对应JSON必须同步为同一状态，不能让下游自行选择新旧口径。

## 4. 84号恢复的两项并行施工

### A9.1-A6-S｜整屏Scene Target Lookdev

- 唯一任务书：`81-c01e02-a9-1a6-s-scene-first-lookdev-objective.md`。
- 产出两张exact几何1280×720整屏目标图，以及50%／100%关键裁切和来源日志。
- 这是Candidate视觉意图，不是可拆资产、UA91、Runtime或real art handoff。
- 84号已解除`pre-generation gate`；按81号生成预算与停止门施工。

### G2-A.2｜无身份视觉合成器Proxy

- 唯一任务书：`82-c01e02-g2-a2-visual-compositor-proxy-objective.md`。
- 证明六层地图、复合Actor、局部遮挡、Overlay、雨夜挂点、通讯安全区和性能。
- 全程`real_art_loaded=0`，不得用Proxy宣称目标视觉完成。
- 84号已恢复G2-A.2新增实现；继续原地保留83阶段前的既有文件。

两项现已恢复并行，且都必须停在A9.1-A6-D／联合重组前的制作人检查点。

## 5. 精品Demo停止门

后续不按“文件齐全”放行，而按玩家最终画面验证：

1. 身份：馆守Z必须读作当前V10X，BREAKER必须读作B身体关系＋X表面关系；不重新设计。
2. 透视：单位、建筑、阴影、雨和FX必须在同一斜俯世界；不得出现眼平纸片。
3. 比例：2×2／3×3的巨体重量、遮挡和footpoint在50%游戏尺度仍成立。
4. 交互第一读法：玩家先看到目标、路线、威胁、接触和A／B代价，而不是先看装饰。
5. 接触重量：姿势、socket、hit-stop、反冲、碎地、声音和震屏同源；不能靠白闪或整帧插画冒充。
6. 可组合：Lookdev目标最终必须能由可拆资产＋同一消费者重组；禁止另一张整帧生成图补洞。

UA91、A9.1-B、G2-B、UGT及完整Golden Slice继续保持Blocked。
