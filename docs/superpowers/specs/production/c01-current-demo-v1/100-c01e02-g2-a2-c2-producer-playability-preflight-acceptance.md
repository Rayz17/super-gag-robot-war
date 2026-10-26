# C01E02 G2-A2-C2｜制作人可玩性预演签收

日期：2026-08-20  
任务ID：`P98_G2_A2_C2_PRODUCER_PLAYABILITY_PREFLIGHT_REVIEW`  
结论：`ACCEPTED_PRODUCT_PREFLIGHT / SCREEN_INPUT_LIVE_DRAFT_MAP_CONSEQUENCE_AND_13S_EXECUTION_SUPPORTED / FUN_NOT_PROVEN / REAL_ART_ZERO`

## 1. 本次真正签收的东西

本签收只关闭Task96要求的产品预演门，不把Proxy机器帧冒充精品美术或真人试玩：

- 玩家输入从空草稿开始，经实际`InputEvent`在current-topology画路线、定朝向、选动作／预备；capture driver未直接调用Session；
- 一条被Session入口拒绝的落点能fail closed；另有一条已真实写入draft、但被Resolver判为route-family失败的路线，玩家可见错误后用Z撤销并重画成功；
- A／B当前方案的热量、设施、路损、接触时点／前缘与第二轮热量／余量，全部由同一Resolver预演字段动态格式化；C／Back只读展开另一路预演，不替换当前草稿；
- preview时间线从`live_preview.event_log`构造，execute时间线在Director开始后从`active_plan.events`独立重算；交换相邻事件会得到不同hash；
- A／B自然执行分别约13.335秒／13.322秒，T1–T5在同一地图依次兑现，T3以前没有实体T4炮击，轮末只推进一次；
- A路在地图上兑现警戒设施受损、路损42；B路兑现设施保全、路损24。当前Proxy足以证明因果数据流与表现挂点，不证明最终打击感。

## 2. 制作人独立复核

我逐张查看了15张1280×720非headless实际帧，包括：PUBLIC空草稿、未闭合草稿、真实非法路线、A／B动态闭合、A／B主动比较、摘要、返回撤销、A／B接触和A／B T5后果。

产品预读结果：

- 错误路线帧能直接说清“已经写入草稿，但没有到达可承担接触的位置”，且明确允许撤销重画；
- A／B比较帧同层级展示真实收益与代价，A不再严格支配B；比较前后当前draft signature和selected strategy均不变；
- T5 A／B帧在地图内用警戒设施红叉／绿环、路损与机体热排出区分结果，数字卡只作解释，不再是唯一后果载体；
- 顶部目标、三条公开意图、地图中央路线与底部五时点保持同屏，未出现全屏插画替代玩法。

机器证据复核：

- `delivery-hashes.sha256`：169项逐项PASS，证据树差集为0，SHA `b8bcb8c0f94f56ba60a48ad7b2c756108ebee16a1e712facece8946c30877d60`；
- `actual-input-frame-manifest.json`：15帧，SHA `a1ba2c37b592dfbc983dd6ffa1944098582eabc6edaab2875474e3b30ea08a47`；
- `raw-screen-trace-validation.json`：外部重算四项产品链与A／B时间，SHA `be9538cff8e1a1cf0d0fcb712b4869152d997ad6a49d84f59f7b7827dad66bed`；
- `screen-input-contract.json`：SHA `2cb97b025c8c36258229d65c34788935585147d14da7d3058c629da68b77fdd0`；
- 600帧非headless性能：p95 `8.090ms`、max `11.459ms`、采样窗截图IO为0，receipt SHA `83fde14e30ee5452c19ee1f4f007105c5be0f2d39bb427519dec85894449b2d8`；
- 唯一最终回归日志SHA `0a51d5bc29a8de79a698b13649574976189ff259eb9016a98f0e8efcaa522134`，晚于最终源码；完成报告晚于日志，manifest晚于完成报告；
- Resolver／Session／PerformanceDirector／R2C几何、旧B R1／R2 exact hash、R2／R3、Full／Skip、Default、save、Canon、G2-B均未改变。

旧音频测试存在Godot退出期偶发8个ObjectDB清理告警；其语义断言始终PASS，最终runner另证`attempts=2 / consecutive_clean=2 / semantic_errors=0`。这不阻断Task96，但也不冒充根因已修复。

## 3. 明确不签的东西

- `FUN_NOT_PROVEN`：没有真人从空草稿试玩，也没有手柄硬件回放；
- `REAL_ART_ZERO`：当前机体、对象、地图与FX仍是几何Proxy；
- 角色身份、精品地图、打击感、雨湿成片、LibTV Cut-in、45–75秒首轮完整试玩均未通过；
- 不开放UA91、A9.1-B、signed exact handoff、G2-B、Default、save、Runtime或Canon；
- 不允许把15张Proxy帧送用户当美术母版或“精品Demo完成”。

## 4. 本签收只开放的下一步

1. `G2_A2_C3_CURRENT_TOPOLOGY_REAL_ATLAS_NEUTRAL_CONSUMER`：只用身份中性Atlas证明真实`AtlasTexture`、sparse rect、pivot、socket、局部遮挡和连续phase；仍`real_art_loaded=0`。
2. `A9_1A6_ENV_E0_CURRENT_TOPOLOGY_ENVIRONMENT_DERIVATION`：只用Call02六块无语义环境donor和current masks做零生图分层重装；旧A4／Call02整屏像素不得回流。

两条都通过制作人门以后，才联合审查是否逐字开放一次`BREAKER_PLAN_MAP_CAMERA_MASTER_NORTH_RGBA_384`。当前仍为`Call03=false / Call04=false`。
