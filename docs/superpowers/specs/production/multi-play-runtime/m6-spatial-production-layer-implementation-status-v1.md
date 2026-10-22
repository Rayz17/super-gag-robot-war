# 《超GAG机器人大战》M6 Spatial 生产层实现状态 v1

日期：2026-07-15  
状态：`candidate_spatial_production_layer_validated`  
适用边界：`C02E03-MULTI-PLAY-M6-VALIDATION`，仍为 `runtime_validation_only`

## 1. 本轮解决的问题

旧 M6 Workshop 虽有六个稳定对象，但仍是一张大画布上的六个热点。玩家没有空间方向、返程记忆、人物位置变化，也只能在侧栏读一句调查结果。它能证明对象合同，不能证明 Spatial 是一种成立的玩法。

本轮将 Workshop 改造成可复用的空间运行时样例：

```text
SpatialModeScene
  LocationSceneRuntime
    Room[3]
    Portal[]
    SpawnPoint[]
    ReturnPoint[]
  StableObjectRegistry + StableObjectNode[]
  SpatialNpcRegistry
  SpatialInteractionDirector
  SpatialNarrativeOverlay
  ActivityHost
    CONSTRAINT
    TIMING
```

它没有增加新的模式语法，而是让 Spatial 内部具备“移动、发现、交谈、判断、动手”的完整层次。

## 2. 房间网络

M6 维修棚拆为三个相连的小场景：

| 房间 | 主地标 | 稳定对象 | 主要作用 |
|---|---|---|---|
| `workshop_front` 直播前台 | 黄灯下的老录像机 | 原速录像、复活直播终端 | 先看见“影子半拍”和直播修饰 |
| `repair_floor` 维修内场 | 两层楼高的旧拳王本体 | 右拳护具、左膝旧轴 | 用身体痕迹确认问题不是单一右拳故障 |
| `back_storage` 零件后仓 | 每次报警少回一下的后仓门 | 仓门报警器、唐胶零件盘 | 把库存、出口和擂台承力放进同一责任选择 |

入口由 Graph 的 `spatial_layout` 声明。每个 Portal 都有动作动词、目标房间、目标出生点和交互范围。离开房间时记录玩家的实际位置；使用返程 Portal 时恢复该位置，不把主角重置到房间默认出生点。

## 3. 非清单推进

维修草案只要求：

- 右拳或膝轴中的任一条身体依据。
- 原速录像或仓门中的任一条现场依据。

因此存在多条有效路径：

```text
录像 -> 右拳 -> 零件盘
录像 -> 膝轴 -> 零件盘
仓门 -> 右拳 -> 零件盘
仓门 -> 膝轴 -> 零件盘
```

直播终端是录像后的可选消费，不是主线搜齐门槛；唐胶对话也不作为强制钥匙。玩家可多理解，但不需要清空所有发光点才能推进。

## 4. 动态人物

当前只使用 Canon 已登记的 `CH_TANGJIAO`，没有为填空间临时创造会说话的 NPC。

- 调查不足时，唐胶留在维修内场的旧拳王旁。
- 取得一条身体依据和一条现场依据后，唐胶移动到后仓零件盘。
- 人物位置由 `placements + priority + InteractionOffer prerequisites` 解析，不由 M6 脚本硬编码。

这次移动同时承担导航和戏剧功能：玩家不需要侧栏提示“草案已解锁”，看见唐胶离开机体、站到零件盘旁就能理解下一步。

## 5. 多轮 NarrativeOverlay

稳定对象首轮调查不再只显示一句结果。`StableObjectRegistry` 会返回 `first_sequence` 或 `repeat_sequence`，由共享 `SpatialNarrativeOverlay` 播放：

- 左右人物头像与面向布局。
- 当前说话者高亮。
- 手边动作和舞台动作。
- 多轮来回，不把设定压进单句说明。
- 首轮与重复回顾分离，不重复结算状态。
- 选择后的条件台词；未选分支不会播放。

唐胶在零件盘前会追问“先保承力还是先保出口”。选择改变纪存当场的回应，但真正的责任仍要在后续 CONSTRAINT 中以零件落槽确认；台词选择不越权替玩家提交系统方案。

## 6. 共享交互和状态

`SpatialInteractionDirector` 统一比较当前房间内的稳定对象、Portal 和动态人物距离。玩家只使用一个交互键，不需要在“调查模式、对话模式、换房模式”间切工具。

保存快照新增：

- 当前房间和玩家位置。
- 每个房间的返程点。
- NPC 已完成对话 Offer。
- 正在播放的 Overlay 行号、选择和待结算 InteractionOffer。
- 原有稳定对象、CONSTRAINT、TIMING 和复合 Outcome 状态。

Overlay 关闭后才进入 CONSTRAINT，避免世界状态已结算、界面却仍停留在调查台词中的权限错位。

## 7. 构建门禁

`EpisodeBundleCompiler` 新增声明式 Spatial 校验：

- 至少两个房间。
- 房间 ID、出生点、Portal ID 和目标闭包有效。
- 稳定对象引用存在的房间。
- NPC placement 引用存在的房间。
- NPC Offer 有可播放 beats。

M6 bundle 的 `compiler_contract.spatial_layout_validated=true`。Windows 包验证器也将五个 Spatial 生产脚本列为必需资源，并检查 M6 三房间和动态人物合同。

## 8. 验证结果

自动验证覆盖：

- 三房间 Graph 声明和运行时配置。
- 前台进入内场、内场返前台时精确恢复离开位置。
- 唐胶从机体旁移动到后仓零件盘。
- 调查 Overlay 完成后才打开维修草案。
- 房间、NPC、Overlay、稳定对象和活动未完成状态精确存取。
- 五节点完整 Episode 仍能把 Spatial 结果送进 Tactical、Reaction 与 Desk。

本机 Metal/OpenGL 1280x720 像素证据：

- `outputs/multi-play-presentation-validation/04a-m6-workshop-front.png`
- `outputs/multi-play-presentation-validation/04b-m6-workshop-repair-floor.png`
- `outputs/multi-play-presentation-validation/04c-m6-workshop-back-storage.png`
- `outputs/multi-play-presentation-validation/05-m6-workshop-dialogue-overlay.png`

无头 Godot 使用 dummy 渲染器，无法取得有效像素；本轮没有把无头逻辑通过误报为视觉通过。

## 9. 仍未完成

1. 当前 Room 仍由同一张候选背景裁切和程序信息层承载，不是正式分房间背景、碰撞遮挡和角色行走 Sprite。
2. 唐胶有动态位置和完整对话头像，但场内 Actor 仍是候选标记，不是正式走动动画。
3. P3 已接入旧拳王候选地图图、Pose、唐胶 Cut-in、两项武器与救援事件；P3b 已为其余八个实体补齐 A 档程序化地图轮廓，但正式机体 Sprite、独立动作帧与音效资产仍未生产。
4. 鼠标点击寻路、复杂碰撞、声源方向和镜头分层尚未进入共享 LocationScene。
5. 外部真人容量、理解、Windows 真机和实体手柄回执仍为空。
6. 本实现不提升 `C02E03`、V35 剧情或任何候选美术为 Working Canon。

## 10. 下一步

P2 候选生产层已经完成。下一轮不应再给 Workshop 增加热点，而应：

1. 把 Tactical 九实体的候选地图识别层推进为正式 Sprite/动作/音效资产，并将旧拳王 Pose、Cut-in 与短演出纳入正式资产验收。
2. 为 LocationScene 补正式地图分层、碰撞和角色步行动画。
3. 取得一轮完整 M6 真人容量与普通语言理解回执。
4. 选择通过 Pressure Board 与 Reader 的正式 Episode 做 P5 验收。
