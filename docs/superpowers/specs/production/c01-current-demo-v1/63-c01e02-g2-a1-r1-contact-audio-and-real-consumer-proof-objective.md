# C01E02 G2-A.1-R1｜接触声音与真实消费者窄返修

> Owner：主程序 Session  
> 性质：Candidate internal readiness correction  
> 依赖：59、61及G2-A.1实际交付  
> 完成即停：`real_art_loaded=0 / U2=false / G2-B blocked`

## 制作人验收结论

G2-A.1核心地图结算与玩法约束真实成立，但总体只能记为`PARTIAL PASS`。保留并冻结已经证明的40×20投影、同地图T1–T5、共同回合、三设备输入、A/B第二轮约束、五个AudioServer Bus和逐槽fail-closed；不得重做玩法内核。

必须关闭两个夸大点：

1. 多层冲击声当前从`anticipation`开始计时，T3约早于真实接触490ms，T4等事件也未与impact/contact phase绑定。
2. 39个槽目前只证明宿主NodePath存在；单位state/facing/animation多为metadata，人物／机魂状态未随事件真正切换，部分Cut-in槽没有显示链。

## 允许且必须完成

### A. 声音时点

- 由PerformanceDirector发出明确的`pre_contact / contact / aftermath`事件边界。
- 预接触静默可以在contact前开始；IMPACT、DEBRIS和机体机械层必须在contact/impact帧启动，T4炮击同理。
- Full／Skip／fallback结果等价；Skip不得残留ducking、mute或bus状态。
- 测试记录实际时间戳，断言声音相对contact边界，而不是只单测AudioDirector布尔值。

### B. 至少三类真实消费证明（仍只用fixture）

1. 馆守Z与BREAKER：各用一份多帧fixture atlas，按`state + facing + frame`实际改变AtlasTexture region／动画帧；不得只把字符串写入metadata。
2. 人物／机魂：至少一组纪存或旧守护者fixture状态随Public→Planning→Contact真实切换TextureRect region／texture与显隐；身份仍只是synthetic fixture，不得读取任何真美术或旧portrait。
3. Cut-in／FX：至少一个已登记屏幕槽进入真实show→hold→hide链，且与地图事件phase同步。

### C. 非自报验收

- 新测试须从运行节点读取Texture、AtlasTexture region、animation/frame、visible/modulate和音频播放时间；禁止只反查manifest或metadata自报。
- 保留现有T1–T5、A/B、输入和确定性回归；默认M2、Reader、Canon、存档、启动入口不变。

## 边界

- `real_art_loaded=0`，不得读取A8、A9、A9.1、旧units、旧portraits、story_first或历史receipt。
- 不开始P1 exact handoff、G2-B、用户视觉捕获、默认入口替换或完整E02。
- T1–T3写死但合法的事件焦点本轮可保留；不得宣称已成为通用动态接触求解器。

完成后交专项测试、时间线回执、三类实际消费证据及短完成报告，然后停止在制作人回收点。
