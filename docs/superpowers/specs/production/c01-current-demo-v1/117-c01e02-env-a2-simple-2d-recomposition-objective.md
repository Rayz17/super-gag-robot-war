# C01E02 ENV-A2：简单2D地面与独立建筑重组任务书

状态：`DISPATCHED_ZERO_GENERATION / SIMPLE_2D_ONLY / PARALLEL_WITH_CALL03`

## 1. 目标

使用ENV-A1已生成且可分离的模块，做一次不新增ImageGen、不新增渲染系统的整屏重组，解决P102的两个明确失败：地面拼贴第一读法与盾缺乏承托关系。

## 2. 允许输入

- `115-c01e02-p102-env-a1-producer-visual-review-and-parallel-release.md`
- ENV-A1 raw及独立structure/object Candidate源；不得读取ENV-A1失败GroundBake作为像素父图。
- Camera V2 exact合同与structure/object registration表。

禁止旧A4、ENV-E0、Call02整屏、角色、机体、车辆、小体、UI、路线、CONTACT FX或新ImageGen。

## 3. 最小施工

1. Ground只用一个连续、低对比的冷蓝灰湿地底色；ENV-A1 wet-asphalt中心纹理只以低强度宏观变化叠加，禁止平铺母块和可见重复。
2. 道路、保护区前场、警戒前场只用同一底面上的轻微明度／材质差和稀疏车道线；多边形边界做16—24px柔和过渡，不画荧光UI区。
3. 六Structure仍是独立`foundation + occluder`资源，按Camera V2原grid rect/front-edge/pivot放置；不得移动锚点。
4. 盾、东门、设施仍独立。盾可增加一个由其自身／结构foundation像素派生的低矮展陈基座或破墙承托层；该层不改变盾anchor、state或玩法占位。
5. 只用简单Canvas层／Pillow合成；不建SubViewport、逐像素mask、动态光照、轮廓shader或新遮挡系统。

## 4. 输出

唯一目录：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-env-a2-simple-recomposition/**`

必须交：

- 新GroundBake 2400×1350；
- 六structure和四tactical object原字节继承清单；
- A/B PLAN与A/B CONTACT actor-free cleanplate；
- A_PLAN 50%／100%；
- 简单slot/footprint overlay QA；
- source lineage、machine report、visual review、completion与delivery hashes。

## 5. 视觉门

- 50%无矩形母块、硬拼贴或明显重复纹理；三秒可读中央承力大道、东侧撤离方向、西侧盾钩子和周边建筑围合。
- 100%无品红边、邻slot碎片或错误pivot；结构视角统一，foundation／occluder可独立；盾的展陈／墙挂关系成立。
- 选择口袋与接触口袋保持无遮挡。

失败则诚实停为环境整合未解决，但不得阻塞已经并行的Call03单主体制作。最终PLAN重组仍必须等待本环境门通过。
