# C01E02 M3-J1｜共同回合内核与真实消费者前置任务

> Owner：主程序 Session
>
> 依赖：48 号联合计划
>
> 状态：`Candidate development / no real art handoff yet`

## 总要求

M0.1 已完成，到此停止继续打磨程序假美术。主程序不再负责寻找最新图片，也不得从美术目录、frozen identity anchor 或旧 Demo 目录自行挑图。本任务并行完成两个可独立验收的前置车道；收到制作人 P1 handoff 前，只使用测试 fixture 验证真实消费者。

## G1：共同回合内核硬门

在当前 R0 代表轮故事边界内完成：

1. 玩家可以编辑一条有上限的短路线／waypoint，而不是只点终点后由 BFS 强制替换成唯一最短路。
2. 终点朝向独立于路线和最后一步移动，提交前可自由修改且世界零写入。
3. `FrozenIntentSet` 的敌方动作、目标、时间窗和场地／车辆意图真正驱动 resolver；预备反应由 `trigger → response` 和已冻结意图触发，不再只检查固定矩形。
4. 提交摘要完整复述：路线与终点、final facing、主动作或预备反应、保护对象、触发条件、fallback、预计接触组与时点；摘要可返回编辑且不改变世界。
5. Preview 与执行调用同一个纯 resolver；共同结算从同一前态计算，同一时点接触不依赖实体容器顺序。
6. `route_hash` 哈希真实路线；mutation／settlement counts 从实际事件账推导，不允许硬编码“1”再由测试反查。
7. 保留至少两种合法单轮方案与一种明确失败方案；20次重放、容器重排、Full／Skip 的结果签名必须一致。
8. “下一步”不得给唯一标准答案；只能作为可关闭的规划辅助。

这条车道不改美术、Canon、Reader、默认 M2、正式存档或完整 E02 结局。

## M1a：真实 handoff loader 与消费者骨架

先只接隔离 fixture，不接任何正式美术：

1. 建立 M3-J1 专属 build/profile/receipt；参考 M2 的路径、SHA、尺寸与 fail-closed 思路，但不得复用旧 M2 receipt 或硬编码旧 slot inventory。
2. 实现逐槽 loader：校验 Stable ID、规范化路径、SHA、尺寸、alpha、帧序、pivot、safe rect、build/profile/topology和用户／制作人回执。
3. 世界层：A4 `BASE/BUILDINGS → 单位/盾/FX → ROOFS/FOREGROUND`；occlusion mask 只作采样。固定 `canvas_world_origin=(-880,-170)`，映射为 `pixel=(880+(x-y)*40,170+(x+y)*20)`。
4. 实现 A5、馆守 Z、BREAKER、车辆、盾与 FX 的真实 Sprite／Atlas 消费者。
5. 实现纪存、七海、旧守护者、兜灯与 `GIANT_CONTACT` 的 TextureRect／AtlasTexture 消费者；真实图加载后不得再叠画技术剪影。
6. 音频至少分 UI、世界一次性、环境／循环三类通道，支持同时播放，不再每个节拍只取第一条音效。
7. 单槽坏 SHA／尺寸／帧序／pivot 只回退该槽；任一身份关键槽 fallback 时 `U2_visual_playtest_ready=false`。
8. 禁止目录扫描、相似文件猜测和“找不到就换旧图”。

## 允许写入与隔离

- 只在新的 M3-J1 子目录、专项测试目录和完成报告目录写入；现有 M0／M0.1 证据只读。
- 默认 M2 入口、R0 profile／正式存档、旧 handoff、A4/A5运行字节、Canon、Reader均只读。
- 正式资产消费必须等制作人后续 P1 exact handoff；P1 前的 loader 只能读取专项 fixture 根。

## 验收停点

- G1：路线、意图、摘要、共同前态、真实证据和确定性专项全部 PASS，并提供可直接试玩的非默认工程入口。
- M1a：所有槽以 fixture 验证真实加载、帧切换、层级、音频并发和逐槽 fail-closed；旧资产 denylist 零命中。
- 两车道不得自行合并正式美术。完成后停给制作人，等待 U1 与 P1 handoff。
- 不得声称完整 E02、U2视觉试玩、正式 Runtime 或商业质量已经完成。

