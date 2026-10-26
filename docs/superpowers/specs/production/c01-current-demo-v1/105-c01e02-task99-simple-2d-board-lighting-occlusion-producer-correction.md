# C01E02 Task99｜简化2D棋盘光影与遮挡制作人纠偏

日期：2026-08-21  
任务：`G2_A2_C3_CURRENT_TOPOLOGY_REAL_ATLAS_NEUTRAL_CONSUMER`  
裁决者：制作人-2  
状态：`USER_DIRECTED_SCOPE_REDUCTION / GAMEPLAY_UNCHANGED / CALL03_FALSE`

## 1. 用户裁决

用户要求：不要把战棋棋盘的光影、遮挡做成接近实时渲染系统的复杂度。精品 Demo 的重点是交互第一读法、角色与机体身份、路线责任、受力、打击感和演出结合，而不是证明一套通用2D渲染技术。

本文件从落盘起，限定并覆盖Task99第6节“局部遮挡”与第7节第7项的实现口径。Task99其余真实Atlas、clip、pivot、footpoint、z、socket、输入链、非回归和`real_art_loaded=0`要求继续有效。

## 2. 保留的必要能力

1. 真正消费`Sprite2D + AtlasTexture + 透明PNG`，按稀疏clip切换region；
2. 单位注册点统一为`footprint_bottom_center`，显示尺寸、pivot与五socket遵守current contract；
3. 单位之间按脚点Y加`z_bias`排序；用一张实际场景图证明1×1、2×2、3×3前后关系正确即可，不再要求构造逐像素GPU反证实验；
4. 地图固定拆为：底地／后景建筑、单位与独立椭圆阴影、少量屋顶或前景遮挡片、UI／演出FX；
5. 雨、湿地反光、接触闪光、水花等只做低成本2D层或预烘像素，不改变玩法格、脚点或对象anchor；
6. 继续保留A／B真实InputEvent自然执行、完整T1–T5 clip连续性、缺clip fail-closed、性能与非回归。

## 3. 唯一允许的遮挡方案

- 每个真正需要遮挡的屋檐／前景使用预先制作的局部`CanvasItem`遮挡片；不使用全地图统一淡化。现有`ROOFS_FOREGROUND_CURRENT`若保持逐roof-cell局部淡化，可以直接复用为唯一owner，不必另造一套节点系统。
- 遮挡片常态按固定z显示；任一可见单位进入该遮挡片覆盖区时，只允许相交的局部片切换到预设alpha（建议0.30–0.45）或预设cutout状态，离开后恢复。玩家当前单位不要求另设第二套特殊遮挡算法。
- 触发可以直接复用现有廉价判定：固定roof-cell polygon与由`footprint_bottom_center + 1×1／2×2／3×3`预设显示框推导的确定性subject bounds相交。它是近似可读性规则，不是玩法碰撞；不得采样Sprite轮廓，也不得生成逐像素动态mask。
- 同一时刻只允许一个遮挡owner：现有逐cell局部淡化层或等价的局部遮挡片二选一。actor alpha shader、实时轮廓mask和第二套遮挡层不得同时生效。
- 阴影由单位独立椭圆层唯一持有；主体PNG不烘地面阴影。

## 4. 明确停止的复杂路线

以下内容不再是Task99验收要求，也不得为了“证明得更严”继续扩建：

- `SubViewport`／`ViewportTexture`实时Actor-alpha采样；
- 每帧轮廓重建、dirty-patch像素扫描或逐主体GPU遮挡toggle；
- roof与foreground共享实时coverage纹理；
- 逐像素inside／outside diff作为产品放行门；
- 为性能优化另造缓存投影、重画current-topology全部地形／建筑／天气；
- 把2D棋盘变成通用动态光照、法线、投影或遮挡渲染系统。

已经形成的相关WIP代码／临时证据可以保留在共享树中等待收口，但不得进入最终Scene主路径、完成回执或后续真实美术接口。不得用清理命令破坏并行任务或用户文件。

## 5. 简化后的验收证据

Task99最终只需在原有Atlas／输入／连续phase／性能证据之外补交：

1. PLAN与CONTACT各一张非headless实际帧，能看到主体、独立椭圆阴影、一个后景建筑和一个局部前景／屋檐遮挡片；
2. 一张局部遮挡片常态图和一张同片触发淡化图；若复用旧owner，可提交逐cell触发图，若采用等价的预制局部片，则只要求相交片改变。两种情况都必须确认单位Sprite实例、Atlas region与主体alpha不变；允许触发者是任一可见单位；
3. Scene-tree／receipt证明只有一个逐cell／逐片局部遮挡owner；旧owner与等价新owner必须二选一，实时Actor-alpha mask、SubViewport与第二套遮挡路径均未启用；
4. z-readback加一张可见重叠图，覆盖1×1／2×2／3×3三类主体的脚点排序；
5. 120＋600帧自然T1–T5动态窗口仍满足现有性能门，资源不重复加载；无需证明实时mask更新计数。

机器通过仍只可签：`REAL_ATLAS_NEUTRAL_CONSUMER_PREFLIGHT_SUPPORTED / SIMPLE_2D_OCCLUSION / FIXTURE_ONLY / REAL_ART_ZERO`。

### 5.1 中性夹具性能门与正式Demo性能门分离

Task99当前画面仍使用会随动态相机整层重画的C2程序代理地面／建筑；它不是后续2400×1350正式静态地图图层，也不会进入真实美术handoff。独立动态诊断已确认：慢帧与该代理的`GROUND_BASE_CURRENT + STRUCTURES_CURRENT`同时重画严格同现，真实Atlas、六片局部遮挡owner、纹理加载与显存均不是瓶颈。不得为了让一次性代理满足正式成片指标，恢复缓存投影、拆分渲染或修改已签C2字节。

因此本Task99中性消费者的120＋600帧门限定为：`p50<=16.7ms / p95<=33.3ms / max<=33.3ms / frames_over_33_3ms=0`，且A路T1–T5后必须自然回到PLAN、资源零重复加载、显存不增长。通过时只能标记`FIXTURE_30FPS_STABILITY_ONLY / FINAL_60FPS_NOT_PROVEN`。

在正式current-topology静态地图图层与真实单位资产完成确定性组合后、任何G2-B signed handoff或UGT以前，必须重新执行`p95<=16.7ms / max<=33.3ms`的非headless严格门；该门不得被本夹具回执替代。此裁决不授权固定镜头、删除动态相机、修改R2C、降低最终Demo帧率或隐藏性能结果。

## 6. 未改变的制作门

- R2C A／B路线、接触几何、结果、相机、地图topology、T1–T5与Current Canon均不变；
- `FUN_NOT_PROVEN / UA91_NOT_OPEN / real_art_loaded=0`不变；
- Call03／Call04仍为`false`。本纠偏不是生图授权，也不是Runtime晋级授权。
