# A9.1-A6-S-C1 shot plan

Status: `PRE_GENERATION_ONLY / CALL02_NOT_ALLOWED`

本计划只冻结镜头职责、时态与确定性overlay边界。机体、建筑或地图目标像素尚未生成；89号完成帧与制作人actual-frame签收仍是唯一解门输入。

## 1. 共同世界与镜头

- 投影：`32x18`、`tile_half=[40,20]`、2:1 dimetric；整数grid point是cell center，不加半格。
- current canvas origin：`[-1760,-340]`；旧`[-1680,-350]`禁止。
- PUBLIC / PLAN / SUMMARY共享相机：center `[-480,420]`，crop `[640,468,1280,584]`，layer top-left `[-640,-410]`。
- A CONTACT：center `[-480,450]`；B CONTACT：center `[-500,440]`。自然播放只允许同一公式的0.16s连续平移。
- 共同起始current actors：馆守Z`[15,11]/2x2/east`；BREAKER`[20,13]/3x3/north`；应急车`[17,10]/east`；小体01`[22,7]/west`、02`[26,12]/north`、03`[29,5]/south`。
- current objects：退役重盾`[14,10]`、撤离口`[31,7]`、警戒设施`[27,8]`、保护区`[20,5,12,7]`、炮源`[29,2]`。
- 三条公开意图：车辆`[17,10]→[18,10]→[21,10]→[24,9]`；小体01`[22,7]→[21,8]→[20,9]→[20,10]`；BREAKER`[20,13]→[20,12]→[20,11]`。
- 89号未签收前，所有上述值只用于shot plan与overlay合同，不作为可见像素生成指南。

## 2. 路线族的视觉表达

- A族：7步到`[20,9]`，settle `south`；当前topology有21条连续、2x2可放的单调最短路线。
- B族：6步到`[19,9]`，settle `east`，接触前公开转`south`；当前topology有15条连续、2x2可放的单调最短路线。
- 直接点A终点的BFS证据：`[15,11]→[15,10]→[15,9]→[16,9]→[17,9]→[18,9]→[19,9]→[20,9]`。
- 直接点B终点的BFS证据：同一路径截至`[19,9]`。
- 画面一次只显示玩家当前草稿路线；不得把21/15条路线同时铺满地图，也不得把hero route画成唯一合法答案。
- `hero_route_exact`只作为Golden Frame代表构图／回归字段；实际成功由`route_family_id`、步数、终点、朝向、动作／预备与可放性共同判断。

## 3. Hero A — PLAN

| 项 | 冻结内容 |
|---|---|
| current actor | 共同起始六实体全部为实体；馆守Z仍在`[15,11]/east`，BREAKER仍在`[20,13]/north` |
| ghost | 馆守Z`[20,9]/2x2/south`是唯一玩家终点ghost；BREAKER`[20,11]`是敌方意图ghost／走廊出口，不得读成第二只实体 |
| intent | 当前选择的一条A族合法路线；车辆、小体01、BREAKER三条公开意图同屏 |
| UI | A被选中；显示目标、三威胁、五时点、A收益／代价与R2余量；B只作可切换对照，不替玩家自动填路 |
| T3 | 只预示“巨体接触”将发生，不画实体碰撞、裂地、水花或反冲 |
| T4 | 城市炮只显示HUD forecast；炮源若在画外只作edge cue，不移入画面 |
| T5 | 赤红蓄能与完整路损只显示forecast，不实体化 |
| 第一读法 | “我用正面吃住它，保住下一轮操作余量；城市与旧路面承担更多损伤” |

## 4. Hero A — CONTACT

| 项 | 冻结内容 |
|---|---|
| current actor | T3.00馆守Z`[20,9]/south`、BREAKER`[20,11]/north`；应急车`[24,9]`；小体01`[22,9]/alive/grounded`；小体02`[27,12]`；小体03`[29,5]` |
| current object | 重盾仍挂`[14,10]`；警戒设施的最终damaged与路损42属于后果读法，不在T3提前做完 |
| ghost | 视觉recoil`[20,8.5]`与post-BREAKER`[21,11]`仅可进入证据overlay，cleanplate不出现第二时态实体 |
| intent | impact socket`[20.5,10.5]`、normal`[0,1]`与受力轴同源；路线退为已执行痕迹，不抢接触焦点 |
| UI | 纪存大型通讯退场；只留窄状态、五时点与A责任摘要 |
| T3 | 只允许contact highlight、micro-crack、少量定向碎屑／水花、hit-stop与反冲 |
| T4 | 只HUD forecast；不得出现炮束、弹道、命中或炮源实体 |
| T5 | 只HUD forecast；不得出现赤红蓄能、完整翻路或已结算42路损的大面积完成态 |
| 第一读法 | 两格正面承接，冲量更多传给旧路面；馆守Z热24，R2目标68／余量1 |

## 5. Contrast B — PLAN

| 项 | 冻结内容 |
|---|---|
| current actor | 与A PLAN完全相同；切换草稿不能让相机或当前实体跳位 |
| ghost | 馆守Z`[19,9]/2x2/east`是settle ghost；接触前转`south`必须由公开phase扇面解释，不能把整条路画成south |
| intent | 当前选择的一条B族6步合法路线；同一车辆、小体01与BREAKER公开意图 |
| UI | B被选中；明确“设施active／路损24／机体热46／R2目标88／余量0”；A作为可切换对照 |
| T3 | 只预示T3.25一格错位承接，不提前出现碰撞效果 |
| T4 | 城市炮只forecast；edge cue不改变炮源`[29,2]` |
| T5 | 设施保全与较轻路损仍是预测，不在PLAN画成已结算 |
| 第一读法 | “我先保城市和撤离线，把热与时间压到馆守Z自己身上” |

## 6. Contrast B — CONTACT

| 项 | 冻结内容 |
|---|---|
| current actor | T3.25馆守Z`[19,9]/south`、BREAKER`[20,11]/north`；应急车按签收resolver readback；小体01`[22,8]/alive/grounded`。小体02／03的B路resolved位置必须等89签收回读，禁止套用A值猜测 |
| current object | 警戒设施仍active；路损24是B后果。重盾仍在`[14,10]`未取得 |
| ghost | post anchors、recoil与最终损伤只取89签收overlay readback；cleanplate不得混入post时态 |
| intent | 一格错位前缘、接触前south转身与B socket必须同源；不得用闪光遮住隔空或穿插 |
| UI | 只留窄状态、五时点与B责任摘要；明确高热与零余量是保城市的代价 |
| T3 | 同A的微裂／少量碎屑／水花／hit-stop上限；时点为T3.25 |
| T4 | 只HUD forecast，炮源不进场 |
| T5 | 只HUD forecast；设施active、路损24、热46、R2 88/0在后果层兑现 |
| 第一读法 | 错位承接把更多冲量与转身代价留在机体，道路／设施得到保护 |

## 7. UI逐字copy

- 目标：`让应急车通过，挡开扑向东门的小体，并站到冲线前。`
- 纪存：`人都在后面。把它引到南边去。`
- 威胁：`应急车先穿过落脚区`；`小体将在第二时点扑向东门`；`BREAKER沿直线冲入街区`
- 时间线：`应急车 / 小体 / 巨体接触 / 城市炮 / 赤红蓄能`
- A：`卡位迎撞｜正面承接｜较低热量｜第二轮余量1`
- B：`护线预备｜先east护线、接触前转south｜高热｜第二轮余量0`

所有中文由确定性UI排版；cleanplate和ImageGen prompt都禁止文字／伪字／baked UI。

## 8. 右缘与画外元素

S3、EXIT是否被当前共同PLAN crop部分裁切，必须以89签收帧为准；若在右缘，只加克制edge cue，不移动grid坐标。炮源`[29,2]`允许并优先保持画外，只在T4 HUD forecast显示方向。任何shot都不得为了“全部看见”而改相机、移动对象或提前实体化T4。
