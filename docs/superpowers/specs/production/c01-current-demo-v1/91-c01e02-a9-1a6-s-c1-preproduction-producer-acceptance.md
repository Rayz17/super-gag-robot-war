# C01E02 A9.1-A6-S-C1 预生产制作人验收回执

日期：2026-08-20  
状态：PREPRODUCTION_ACCEPTED_CALL02_STILL_BLOCKED  
权限：Candidate production only；不构成整屏视觉通过、UA91、Runtime或Canon晋级

## 1. 验收对象

- 任务书：90-c01e02-a9-1a6-s-c1-current-topology-scene-first-preproduction-objective.md
- 交付目录：art-a9-1a6-s-c1-current-topology-scene-first/
- 交付清单：delivery-hashes.sha256，SHA256=e2710ce24214cdb96ca647c3ffe1fa8e0db0867fa918a7531b34962e04ed07a9
- 输入锁：P88=6a26aad909719cb01e9c2f411dae251eb2bfa278d163121f9a3d68ddc0cf06af；P90=67332c6d9644ca0fbcf42aac1a850717201496d34ec0808e4c3013eae9fe4898

## 2. 制作人实际验收

- 11项交付哈希逐项复验一致；31条责任源的绝对路径与SHA均闭合。
- map-language-board.png实际目视通过预生产用途：旧A4只承担地面明度、建筑分面、屋顶、局部遮挡与灯柱方法，明确标注不是current world geometry；旧盾、旧出口、旧设施与旧救援线不得回流。
- identity-style-safe-board.png实际目视通过预生产用途：馆守Z保持V10X无翼无背包；BREAKER B身体与X表面关系分区清楚；CML128区域只提供环境画法，不提供第二套机体解剖。
- deterministic-overlay-ui-template-1280x720.png实际目视通过版面用途：目标、三威胁、纪存通讯与T1-T5可读，中央玩法区透明，不含地图、机体、建筑或目标场景像素。
- Task90回合没有新增ImageGen调用；历史Call01仍计1/4，剩余3次当前可调用数为0。
- 本轮没有Sprite、Atlas、Godot、Runtime、LibTV、Canon迁移或Git提交。

## 3. 非成品边界

- 三张板只证明来源安全、镜头职责与版面预生产，不证明精品雨夜地图、正确机体透视、打击感或玩法好玩。
- UI模板中的ROUTE FAMILY、PLAN COMM、CONTACT、HUD FORECAST ONLY等制作标记，必须在任何Gold Frame或用户画面前剥离，不得冒充成品UI。
- 馆守Z正交设计稿、Q四视和BREAKER B/X仍是身份／结构责任源，不能直接裁成地图Sprite。
- A4继续是材质与分层donor，不是current topology像素母版。

## 4. 下一停止门

CALL02_ALLOWED=false。只有89号同时交付并通过制作人逐帧验收以下证据，才可另行签发CALL02：

1. 真实公开Session API完成A/B编辑、返回修改、摘要、提交与自然结算；fixture_load_count=0且不得以直接覆写draft伪造。
2. current-topology、共同PLAN相机、A/B各自CONTACT时态和0px联合注册实际帧。
3. A/B对称收益与代价来自同一Resolver结果，而非静态文案或工程术语。
4. 11张Godot root viewport实际帧、45-75秒自然trace、性能与最终delivery hashes。

在该门之前，目标场景生图、真实美术接入、UA91、A9.1-B、signed handoff与G2-B继续阻塞。
