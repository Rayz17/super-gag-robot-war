# C01E02 R2C乐趣优先的Current-Topology地图与交互合同

日期：2026-08-20  
任务ID：`P88_R2C_FUN_FIRST_CURRENT_TOPOLOGY_MAP_AND_INTERACTION_CONTRACT`  
状态：`PRODUCER_SIGNED_FOR_CANDIDATE_PREFLIGHT / VISIBLE_PIXEL_AND_REAL_ART_STILL_GATED`  
权限：`Candidate Demo product and implementation contract only`  
不构成：Canon迁移、默认入口替换、Runtime晋级、UA91、美术母版批准、G2-B开放

## 1. 制作人结论

用户已经批准：保留R2C互动骨架，按当前玩法空间重做精品地图，并以主策划总案为准尽可能提高可玩性。

本合同保留R2C已经闭合的“公开意图→可反悔编辑→提交摘要→长按提交→共同结算→后果写回”内核、A/B接触几何和三轮因果；撤销两种会让Demo看似能玩、实则只是在演夹具的施工习惯：

1. 第一轮不得继续要求玩家逐格复刻隐藏的`planning_route`才算成功；
2. B路线不得只显示“高热／零余量”，而隐藏它保住警戒设施、降低路损的真实收益。

第一轮精品目标不是完整大系统，而是一段45–75秒可亲手完成、可看懂、可反悔、可复述的Golden Turn：

> 车先通过；小体扑线；玩家决定馆守Z先用身体迎撞，还是先护住撤离线；馆守Z按玩家路线与朝向完成承接；城市炮获得侧甲窗口；路面与下一轮局势把这次选择留下来。

## 2. 权威与限域

### 2.1 必读责任源

- 用户裁决与重开回执：`87-c01e02-u86-route-a-user-approval-and-gameplay-alignment-reopen-receipt.md`
- 主策划唯一总案：`docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/00c-core-game-design-master-review.md`
- Demo原地换内核合同：`19-current-demo-inplace-rebase-producer-contract.md`
- 联合注册纠偏：`85-c01e02-a4-runtime-joint-registration-and-current-object-space-correction.md`
- 当前逻辑责任源：`golden_slice_profile.json`、`golden_slice_session.gd`、`golden_slice_resolver.gd`
- 已签几何：79、80、83、84号及`main-g2-a1-r2c*`证据

### 2.2 保持不变

- 32×18、40×20的2:1正交二测投影；
- 馆守Z2×2、BREAKER 3×3、小体1×1的身体；
- A接触：馆守Z`[20,9]/south`、BREAKER`[20,11]/north`、T3.00、两格前缘；
- B接触：馆守Z`[19,9]`先`east`护线、接触前转`south`，T3.25、一格错位前缘；
- A/B post位置、impact/side-armor socket、Swarm01唯一`[22,9]`纠偏、T1–T5顺序；
- 第一轮写回到第二轮的热量、余量、警戒设施、路损和动态3×3占位；
- 第二轮取盾挡击、第三轮侧压盾拍、首次击倒但不歼灭的骨架；
- 非默认、存档关闭、`approved_handoffs=[] / real_art_loaded=0`。

第一轮路线接受规则的修正不授权改变上述接触与后果。第二、三轮的路线判定本轮不改，待第一轮UGT后再决定是否同样开放路线族。

## 3. 第一轮从“隐藏标准答案”改为“合法路线族”

### 3.1 现有问题

当前`append_waypoint()`允许玩家自由点地图并由BFS生成合法短路；但`_resolve_round_one()`又用`_route_equals(route, expected_route)`逐格比对夹具路线。玩家直接点击正确终点时，BFS生成的另一条同长度合法路线也会在结算中失败；界面没有提前说明必须复刻哪几格。

制作人按当前`UP→RIGHT→DOWN→LEFT`搜索顺序复算：直接点击A终点会生成`[15,11]→[15,10]→[15,9]→[16,9]→[17,9]→[18,9]→[19,9]→[20,9]`，直接点击B终点会生成同一路径至`[19,9]`；两条都与冻结hero route不同。当前topology中A有21条、B有15条连续且2×2可放的单调最短排列。它们不应被误判成第三种战法或失败。

这不符合00c“移动、朝向、动作／预备是玩家字母”和“规则精通不被隐藏免疫收回”的要求。

### 3.2 新的唯一接受合同

原`planning_route`继续保留为：

- Golden Frame与自动回归的`hero_route`；
- 镜头、时序与美术构图的代表路线；
- 不再是唯一成功序列。

第一轮成功改由机器可读`route_family_contract`判断：

| 路线族 | 起点 | 步数 | 终点 | 玩家选择 | 终点朝向 | 仍须满足 |
|---|---:|---:|---:|---|---|---|
| `A_BODY_INTERCEPT_FAMILY` | `[15,11]` | 恰好7步 | `[20,9]` | `BODY_INTERCEPT` | `south` | 2×2逐格可放、路线连续、T1车辆先行、T2挡开小体、T3接触几何闭合 |
| `B_PROTECT_LANE_FAMILY` | `[15,11]` | 恰好6步 | `[19,9]` | `PROTECT_LANE_RESPONSE` | `east` settle，接触前按公开phase转`south` | 2×2逐格可放、路线连续、预备触发闭合、T2护线、T3.25接触几何闭合 |

因此：

- 玩家直接点A或B终点，由当前BFS生成的合法最短路必须能成功；
- 玩家用waypoint改出另一条同长度、同终点、同责任的合法路线也必须能成功；
- 超步数、错误终点、错误朝向、占地冲突、未选动作／预备仍必须fail closed；
- Resolver回执同时记录`route_family_id`、`hero_route_exact`、`route_steps`和失败原因；
- 不得以模糊“接近标准路线”或静默吸附掩盖非法计划。

## 4. A/B必须成为真实的责任取舍

现有Resolver已经写回两种不同结果，精品UI必须对称呈现：

| | A：主动迎撞 | B：先护撤离线 |
|---|---|---|
| 玩家身体选择 | 提前站入完整受力轴，两格正面承接 | 先用east侧推挡开小体，接触前转south，一格错位承接 |
| 收益 | 接触更早、馆守Z热量24、第二轮目标热量68／余量1 | 警戒设施保持active、路损24、小体被推到更安全的`[22,8]` |
| 代价 | 警戒设施damaged、路损42、城市空间替机体承担更多破坏 | 接触延后到T3.25、馆守Z热量46、第二轮目标热量88／余量0 |
| 第一读法 | “我用正面吃住它，保住下一轮操作余量” | “我先保城市和撤离线，把热与时间压到自己身上” |

现有差异必须补一条可见因果，不新增敌方意图：A的两格正面承接把更多冲量传给旧路面，T3接触后到T5形成更重路损并波及警戒设施；B的一格错位承接把更多冲量和转身代价留在馆守Z自身，因而机体更热、下一轮更紧，但道路和设施保全。该解释只消费既有contact geometry与world result；不得擅自新增外围小体攻击设施的隐藏事件。

动态预演与提交摘要至少回答：

1. 我保护了谁；
2. 谁／什么承担了代价；
3. 接触发生在何时、哪条边；
4. 第二轮还剩多少热量与时序余量；
5. 哪些仍是预测／未知，而不是已发生事实。

不得把A/B做成两个替玩家自动填好路线的剧情按钮。玩家仍亲手画路、定朝向并选择动作或预备；系统只在草稿变化时显示当前是否形成A/B责任解，以及尚缺哪个公开条件。

## 5. Current-topology精品地图舞台

### 5.1 唯一语义空间

地图逻辑只来自current `golden_slice_profile.json`：

- 主路：`[0,7,32,7]`；
- 东侧撤离／保护区：`[20,5,12,7]`；
- NW/NM/NE/SW/SE建筑block、断裂连廊、安全前场按当前`terrain_zones`；
- 退役重盾`[14,10]`、东侧撤离口`[31,7]`、警戒设施`[27,8]`、炮源`[29,2]`；
- 当前车辆、小体、两巨体、意图轨迹与动态对象只从Session／Resolver公开态读取。

旧A4是光色、湿地反光、建筑层次、材质和局部遮挡方法donor，不是地图语义、对象坐标或可见像素母版。Call01只留History／mood donor。

### 5.2 画面必须读出五个空间角色

1. **中央承接大道：**宽阔湿路让2×2与3×3身体、A两格前缘、B一格错位都一眼可读；
2. **东侧生命线：**撤离口、警戒设施、车辆路线与保护区形成一个清楚的“城市还在运作”的目标；
3. **西侧下一轮钩子：**墙挂退役重盾在PLAN中可见但未取得，不抢第一轮主焦点；
4. **南侧冲线：**BREAK​ER从`[20,13]→[20,11]`的北冲轴是最强红色威胁读法；
5. **右缘支援方向：**炮源`[29,2]`可在画外，只以克制的T4 HUD edge cue表示；不得偷移入场或在T3提前开炮。

具体舞台边界：

- `[15..20,9..11]`为无遮挡“选择口袋”，不得放看似可碰撞的路灯、花坛、车或废墟；
- BREAKER扫掠区`x=20..22 / y=11..15`两侧各留一格视觉肩带，形成五格宽承力大道；
- 保护区与security apron用连续青色边灯、疏散箭头和低矮护栏连接，但不把整块地面涂成高饱和荧光矩形；
- 东门是章级英雄地标，万机馆破墙／墙挂重盾是次地标；周边建筑只落在current不可通行block内；
- 三条最重要的线必须能同时读出：T1车辆撤离线、T2小体扑线、T3 BREAKER冲线。

建筑、雨夜、灯带和装饰必须服务这些读法。关键路径、接触边、出口和设施不可被屋顶、通讯框或角色Cut-in长期遮住。

### 5.3 层与动态对象

新地图仍采用2400×1350共同canvas和可组合层，但全部按current topology重派生：

- `GROUND_BASE_CURRENT`：道路、广场、排水、静态地面材质；
- `STRUCTURES_CURRENT`：建筑立面与非交互固定结构；
- `ROOFS_FOREGROUND_CURRENT`：可局部fade/cutout的屋顶与前景；
- `OCCLUSION_CONTROL_CURRENT`：与共同canvas逐像素注册的控制层；
- `STATIC_LIGHT_WEATHER_CURRENT`：静态灯光、湿地与雨夜底；
- `DYNAMIC_WORLD_OBJECTS`：盾、出口、设施、车辆、单位、破坏、路线、FX，必须独立并由公开态驱动。

cleanplate不得烘入旧盾、旧出口、旧设施、状态图标、单位或未来炮击。

## 6. 镜头、投影与整屏交互

联合变换完全服从85号：`canvas_origin_raw=[-1760,-340]`，整数grid point是cell center，crop与layer top-left逐帧由effective camera派生；不得复用81/82旧`[-1680,-350] / [480,428]`。

为让玩家公平比较A/B且切换草稿时地图不跳，P88在PLAN范围内覆盖85号两条独立PLAN focus，冻结共同总览：

```text
PUBLIC / PLAN / SUMMARY shared camera center = [-480,420]
zoom = 1
shake = [0,0]
crop = [640,468,1280,584]
layer top-left = [-640,-410]
```

CONTACT仍服从85号按socket居中的A`[-480,450]`与B`[-500,440]`。自然播放只通过同一公式做0.16秒连续平移，不硬切、不用zoom裁掉出口。共同PLAN、A CONTACT、B CONTACT与无focus派生值必须重验。

整屏目标接近用户给出的精品战棋参考，但不复制具体IP：

- 地图在map viewport内承担约80%注意力；
- 左上：一句任务责任与三条威胁；
- 地图内：cyan玩家路线／footprint／朝向，red敌方冲线与未来作用区；
- 左下：纪存通讯只占安全区，Reader句逐字为“人都在后面。把它引到南边去。”；
- 底部：应急车／小体／巨体接触／城市炮／赤红蓄能五时点；
- 朝向、动作、预备与摘要入口收进顶部右侧或按需抽屉；禁止永久右侧竖栏遮住约`x=1200`的东门；
- CONTACT只兑现T3微裂、碎屑、水花、hit-stop与反冲；T4炮、T5赤红／完整翻路只能是forecast。

通讯与Cut-in总量维持约20%；不得用独立满屏插画替代滚动地图内的规划、接触和后果。

## 7. 两道施工门

### 7.1 G2-A2-C1先行门

主程序-2必须先交：

- 单一projection helper、current-topology注册板和无身份Proxy Scene；
- 不调用`load_fixture()`的A/B完整手动编排证据；
- route family、动态责任预演、返回修改、长按提交、同Resolver preview/execute；
- A/B PLAN、SUMMARY、CONTACT actual frames与45–75秒第一轮自然序列；
- `approved_handoffs=[] / real_art_loaded=0`、非默认、存档关闭；
- 对旧R2C几何、第二／三轮、Full/Skip与确定性非回归。

只有制作人实际查看这些帧并签收，Art2才可消费新的current-topology guide发起下一次ImageGen。

### 7.2 Art scene-first门

美术资产-2可先做只读源整理、shot plan、prompt与安全参考板；在G2-A2-C1签收前禁止Call02。解门后最多使用81号剩余`3/4`次整屏调用，先做current-topology PLAN／CONTACT目标，不做完整Atlas或Runtime资产。

制作人验收顺序：

1. 整屏身份、透视、玩法第一读法；
2. 50%下A/B责任与主要对象；
3. 100%下两机结构、接触、遮挡、材质和时态；
4. 由可拆资产重组出的actual Gold Frame，而非生成整图本身。

## 8. 产品验收与停止门

内部机器证据只能把状态推进到`FUN_HYPOTHESIS_SUPPORTED`，不能宣称“已好玩”。用户UGT前至少满足：

- 从空草稿完成A与B，各至少一次；
- 直接点终点生成的合法短路可成功，另一个同族合法短路也可成功；
- 玩家提交前能看到当前方案的收益、代价与下一轮余量；
- A/B不是颜色差异，actual frame与world result都能看出设施／路损／热量／余量差异；
- 预览与执行语义hash一致，执行只提交一次；
- 45–75秒首轮中至少80%关键演出留在地图内；
- 第一轮失败可解释、可返回／重试，不以隐藏路线答案惩罚玩家。

继续Blocked：真实美术接入、UA91、A9.1-B、signed handoff、G2-B、第二／三轮正式视觉扩写、完整4.5分钟Golden Slice、Default Entry、Runtime、Canon、付费批量与LibTV。
