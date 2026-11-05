# C01 Current Demo｜馆守 Z V10X 跨话视觉血统优先锁

> 日期：2026-08-25  
> 状态：`CURRENT_SCOPED_ART_AUTHORITY / CML008_VISUAL_HISTORY_ONLY / TWO_D_SPRITE_PRODUCTION_ONLY`  
> 范围：`C01 Current Demo / C01E02–C01E04 / 馆守 Z 身份与阶段形态派生`  
> 不构成：全局 CML008 替换、任何 Camera V2 精灵批准、用户实际像素验收、Runtime／Default／Canon 美术晋级

## 1. 为什么需要 CML131

`CML130` 已经把用户确认的 V10X 锁为 C01E02 唯一正向视觉母图，但它只覆盖 E02。当前 Demo 的 E03、E04 生产矩阵仍然要延续同一台馆守 Z；若美术任务只按话次查询当前权威，E03／E04 会重新看到全局 `CML008` 的旧图片并合法回退到旧形象。

`CML131` 只修复这个 scope 缺口：C01 Current Demo 从 E02 到 E04 的馆守 Z 都沿用 V10X 身份结构，再叠加当前剧情已经确定的阶段损伤与臂装变化。它不重新设计馆守 Z，也不把 V10X 原图或任何派生图升为 Runtime。

## 2. 唯一正向身份父图

- 唯一正向身份父图：  
  `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`
- SHA-256：`e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`
- 固定身份模块：头部与层叠头冠、头胸比例、胸甲与圆形核心、腰胯、左臂、双腿、配色、结构语言。
- `CML008` 在本 scope 只保留 18 m、伤损时序、巡展臂装性质等生命周期语义；其 `guardian-z-user-selected-base.png` 旧视觉像素为 `HISTORY_CROSSCHECK_ONLY`，不得作为美术输入。

## 3. 分话阶段差异

1. **E02｜双臂完整**：V10X 身份，完整双臂；持盾状态只叠加用户已接受的 A17 重盾正反结构。盾正面／外侧必须与馆守 Z 正面同向朝向威胁，双手与握把只允许位于盾背面／内侧，敌方可见的盾正面不得出现握持手。
2. **E03 过载前｜双臂完整**：继续使用 V10X 身份；不能因进入 E03 换回旧 CML008 外观。
3. **E03 过载后｜原右拳与完整前臂毁损**：头、胸、腰、左臂和腿仍必须追认 V10X；损伤是独立阶段精灵，不得用双臂完整图改标签。
4. **E04｜巡展臂装**：V10X 核心身份加非拳击式临时巡展臂装；该臂装只含抓握、放锚、牵引和固定结构，不得画回完整右拳或后继右臂。

精确阶段表由 `c01-current-demo-guardian-z-v10x-visual-lineage-lock-v1.tsv` 机器化登记。

## 4. 2D 多朝向生产方法锁

- 各朝向、各动作必须从同一 V10X 2D 身份母版分别制作与校验，再经过 Camera V2 实际地图帧和用户目视确认。
- 多朝向一致性不等于共享 3D 转台；不得再引入 Blender、Three.js、`bpy`、Python／程序建模、低模渲染或程序原语绘制可见机体。
- Python 只允许用于确定性 Alpha、尺寸、pivot、footprint、QA 与 hash；不得补画、生成或建模机体结构。
- A9.1-A3 的 Blender／Three.js 可见像素与 A37 BREAKER Blender 产物均为失败路线证据，不能成为任何馆守 Z 或其他机体的正向输入。

## 5. 旧稿与失败稿隔离

以下来源在本 scope 均为 `FORBIDDEN_HISTORY`：旧 CML008 图片、A13／A18／A19／A22 馆守 Z 持盾失败稿、旧 east Sprite、旧 A2 弹孔装甲板、A9.1-A3 Blender／Three.js 可见像素。文件可以留盘追溯，但不得进入 ImageGen 参考、合成母图、姿态派生、Godot 绑定或实际帧证据。

测试专用 Overlay 也必须锁到生产矩阵中相应 row 的固定 path 与 SHA，不能接受任意绝对路径和调用方自报 SHA 后冒充实际帧。

## 6. 停点

本锁只回答“馆守 Z 在 C01 当前 Demo 的 E02–E04 应从哪一个已确认形象继续制作”。每一张方向／动作 Sprite 仍是独立 Candidate，必须保持 `user=false / runtime=false / default=false / canon=false`，直到实际地图帧获得用户目视签收。
