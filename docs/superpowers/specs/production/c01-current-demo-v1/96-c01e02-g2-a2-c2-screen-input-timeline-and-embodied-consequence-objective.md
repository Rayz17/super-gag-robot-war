# C01E02 G2-A2-C2｜屏幕输入、共同时间线与地图内因果目标书

日期：2026-08-20  
任务ID：`G2_A2_C2_SCREEN_INPUT_TIMELINE_AND_EMBODIED_CONSEQUENCE`  
执行者：主程序-2  
状态：`DISPATCHED / PROXY_ONLY / REAL_ART_ZERO`

## 1. 唯一任务

在不改变R2C几何、Resolver结果与故事顺序的前提下，把Task89从“公开Session API可连续调用的Proxy证明”推进为“玩家能在current-topology屏幕上从空草稿亲手形成责任解，并在同一时间线上看见地图内因果”的产品预审版本。

本任务不接真实美术，不证明FUN，不替代真人UGT；不新增第三战法、多机、QTE、隐藏意图、机魂同意门、第二／三轮内容或倒计时。

## 2. 冻结输入与禁止变化

必读94、93、89、88、31、00c、Current Reader、当前interface 1.6.2与`main-g2-a2-c1/**`。

绝对不改：

- A/B route family、起终点、步数、2×2／3×3占地、朝向、动作／预备；
- T1–T5逻辑顺序、A T3.00、B T3.25、contact edge／socket／normal／post；
- A/B热量、路损、警戒设施、小体落位、R2余量与全部world result；
- projection、共同PLAN相机、CONTACT相机、地图对象坐标与current topology；
- Resolver事件hash、Full／Skip、R2／R3、默认入口、save、Canon。

允许调整的只是current-topology compositor输入适配、屏幕UI状态、确定性Proxy表现和PerformanceDirector的 **表现秒数**；逻辑timeslice与结果不可改。

## 3. 必做一：真实屏幕事件链

把现有鼠标、键盘与手柄等价输入接入专用非默认current-topology Scene，实际经过Scene／Control的`InputEvent`入口，再调用Session公开API：

```text
PUBLIC empty draft
→ map click / waypoint
→ facing
→ action or prepared reaction
→ summary
→ back to edit
→ undo / redraw
→ summary
→ 0.7s hold
→ natural T1–T5
→ result
```

至少交：A键鼠、B手柄等价`InputEvent`自动回放；不得在driver中直接调用Session方法冒充屏幕输入。自动回放可以证明输入接线，不能声称物理手柄真人或FUN。

## 4. 必做二：空草稿与动态责任解

- PUBLIC只显示目标、三条公开意图、当前身体／对象和两个责任方向提示；不预填A/B完整结果卡；
- 玩家路线、终点、朝向、动作／预备尚未闭合时，逐项显示`还差：终点／步数／朝向／动作或预备`；
- 形成A或B后才展开当前方案的收益、代价、接触时点／边与第二轮余量；另一路只在玩家主动比较时展开；
- 直接点终点与另一条合法同族路线都能形成同一责任解；非法草稿可理解、可返回、可修正；
- UI只读同一Resolver预演，不另写A/B结果表。

## 5. 必做三：同一时间线预演与执行

底部五时点在草稿阶段显示车辆、小体、接触组、城市炮、赤红蓄能的公开顺序、触发与forecast；提交后同一条时间线变为playhead并逐项兑现，不切换成另一套演出清单。

必须让玩家看见：敌我来自同一轮前态、T1／T2先改变空间、T3组成接触组、T4／T5随后读取结果、轮末只推进一次。T4／T5在T3以前仍不可实体发生。

## 6. 必做四：地图内身体责任与12–15秒执行

在保持logical timeslice不变的前提下，把现有约5.8秒Proxy执行扩成确定性12–15秒地图内表现：

1. 应急车实际穿过落脚区；
2. 馆守Z依据玩家计划自行停步／转身，挡开小体，纪存只提供路线，不演成遥控机体；
3. A显示两格正面承力轴、冲量传入旧路与警戒设施；B显示east护线预备、接触前转south、一格错位承力与机体热排出；
4. T3以姿势、hit-stop、压缩、反冲、定向水花／碎屑体现18m对近30m重量；
5. T4炮击侧甲、T5路面／设施／机体热后果在地图内兑现；数字表降为复盘层。

至少80%关键表现留在滚动地图；通讯只短促放大，不能用满屏Cut-in替代身体因果。

## 7. 实现与写域

优先复用现有input root、Session、Resolver与PerformanceDirector；只写：

- `g2_a2_visual_compositor/**`的输入适配、UI、overlay、Proxy FX与专用Scene；
- 专用`g2_a2_c2_*`测试／InputEvent replay／capture driver／runner；
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c2/**`。

共享Session／Resolver／R2C语义原则上只读；若实现需要改其公开API，必须先停回制作人，不得顺手改。保留共享树所有已有改动，不git add／commit／clean。

## 8. 强制证据

1. A键鼠与B手柄等价InputEvent从Scene输入入口到ROUND_RESULT的trace；
2. trace证明Session方法只由输入适配调用，driver不直调；
3. PUBLIC空草稿、非法未闭合、A动态闭合、B动态闭合、summary、return／undo、A/B CONTACT、T5 A/B后果实际帧；
4. 同一时间线的preview／execute data token、playhead与事件首次出现回读；
5. 12–15秒执行时长、T1–T5顺序、T3前无T4/T5实体、通讯退场与地图内注意力回执；
6. A/B地图内后果与Resolver字段逐项对应，不靠静态文案；
7. direct endpoint与alternate route family、20次确定性、旧B R1/R2 exact hash、R2/R3/Full/Skip非回归；
8. 非headless 120＋600帧性能；
9. `approved_handoffs=[] / real_art_loaded=0 / default unchanged / save=false / Canon=false`；
10. delivery hashes、实际帧机器readback与完成报告。

机器证据只允许状态到`SCREEN_INPUT_PREFLIGHT_SUPPORTED / LIVE_DRAFT_PREFLIGHT_SUPPORTED / MAP_CONSEQUENCE_PREFLIGHT_SUPPORTED / FUN_NOT_PROVEN`。

## 9. 停止门

完成后停在P98制作人预审。不得自行接Call02像素、开放Call03、UA91、G2-B、Default、save、Runtime或Canon。若发现必须改R2C几何／结果、增加战法或改变故事主体性，立即停止并回制作人。

