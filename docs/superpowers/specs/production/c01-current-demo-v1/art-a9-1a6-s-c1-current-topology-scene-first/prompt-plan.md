# A9.1-A6-S-C1 prompt plan

> `CALL02_ALLOWED=false`。以下只是解门后的提示词与输入职责计划；本包没有调用ImageGen，也没有生成／编辑任何目标场景像素。

## 1. 解门条件

Call02前必须同时收到并重新校验：

1. 89号完成回执的绝对路径与SHA；
2. 制作人已经目视签收的A/B actual frame、current-topology guide与机器readback SHA；
3. 显式文本`CALL02_ALLOWED`；
4. 90、88、87、85、接口与安全身份板仍为当前SHA。

缺一项即保持`call02_allowed=false`。

## 2. 剩余预算与顺序

- 已用：Call01=`1/4`，状态`INVALIDATED_AS_EXACT_TARGET_BY_P85 / MATERIAL_LIGHTING_MOOD_DONOR_ONLY`。
- 剩余总上限：`3`次；当前可调用：`0`次。
- 解门后Call02：current-topology **A PLAN** cleanplate／整屏look target。
- Call03：仅当Call02是可修基础时，以同一世界、相机、光线与身份制作 **A CONTACT**。
- Call04：只允许一次局部纠偏或B对照；不承诺四张都生成，不盲目reroll。

## 3. 引用优先级与最多五图

每次调用最多引用五图，默认只用四类：

1. **Image 1 / exact guide**：制作人签收的89号当前topology实际guide；其相机、crop、道路、建筑block、actor/object位置、footprint、局部遮挡绝对优先。
2. **Image 2 / identity-style safe board**：本目录`identity-style-safe-board.png`；V10X、B＋X分别锁身份；右下只作STYLE，`ignore anatomy`。
3. **Image 3 / map language**：本目录`map-language-board.png`；只借A4 donor的暗值、层次、建筑面、灯带与局部遮挡方法，忽略旧拓扑与旧对象。
4. **Image 4 / swarm identity**：A5四向96px，只约束小体地图相机身份与数量。

纪存不进入cleanplate引用；由确定性screen UI加入。Call01默认不引用，避免其错误拓扑、低位龟猿BREAKER与多余小体串入；若制作人以后明确授权，只能先机械裁出无actor的雨湿／灯光区域并单独校验SHA。

永久禁用：`IDENTITY_STYLE_REFERENCE_MOSAIC_2400x1800.png`，状态`unused_identity_conflicting`。

## 4. 每次提示词不可变前缀

```text
Use case: stylized-concept
Asset type: 1280x720 integrated tactical-game whole-scene cleanplate; non-separable Candidate look target.

Reference roles:
Image 1 is the producer-signed exact current-topology guide. Its projection, camera, crop, roads, blocks, actor/object positions, footprints, ground contacts, and local occlusion are mandatory and override every other image.
Image 2 is identity and style only. Guardian Z anatomy comes only from its V10X quadrant; BREAKER body comes only from B and its surface only from X; the style quadrant is STYLE ONLY, IGNORE ANATOMY.
Image 3 is material, rain-night value, building-plane, light-band, and local-occlusion method only. Ignore every legacy object, route, topology, shield, exit, facility, rescue line, and coordinate.
Image 4 is Rift Swarm identity only. Render exactly the current three swarm actors from Image 1, never extra swarms.

Invariants:
exact guide first; no coordinate relocation; no camera rotation or zoom invention; no baked UI, text, pseudo-writing, route, ghost, footprint, edge cue, or forecast; no redesign; Guardian Z absolutely has no wings and no backpack; BREAKER must remain B body plus X surface; no extra actors.
```

## 5. Call02 A PLAN差分

```text
Present-time PLAN cleanplate. Render only current physical actors and current world objects from the signed guide. Guardian Z remains at [15,11]/east and BREAKER at [20,13]/north. Do not render the player endpoint [20,9], enemy intent endpoint [20,11], route-family alternatives, T3 contact, T4 artillery, or T5 red charge/road buckle. Keep the choice pocket and five-cell load-bearing avenue unobstructed. Preserve true right-edge/offscreen placement; never move S3, EXIT, or artillery inward for visibility.
```

路线、ghost、facing fan、A/B责任摘要、21条／15条路线族状态与edge cue全部由确定性overlay加入；ImageGen不绘制。

## 6. Call03 A CONTACT差分

```text
Freeze the exact T3.00 contact instant from the signed guide. Current physical actors only: Guardian Z [20,9]/south, BREAKER [20,11]/north, vehicle [24,9], Swarm01 [22,9] alive and grounded, and the signed resolved positions of Swarm02/03. Align both bodies, feet, shadows, armor compression, debris and water to the same signed impact socket and normal. Physical FX are limited to contact highlight, micro-crack, small directional debris, water splash and hit-stop. No post-contact duplicate, no T4 artillery, no T5 red charge, no complete road buckle.
```

## 7. 身份负面约束

- 馆守Z：18m、约4头身旧超级系重量、E02双臂、无翼、无背包；金色层叠头冠／中央红冠／蓝额盔／银栅格脸／红X胸甲／圆形金核／宽方肩环／等重圆柱前臂。禁止V21、红翼、背包、细长商品比例或第二套解剖。
- BREAKER：近30m、B前肢承重半直立、短后足仅稳定、低嵌头窄红缝、巨背壳、X异质生体甲、闭合胸缝、封闭上背。禁止龟、猿、普通四足、雪橇、装甲车、豆壳、飞行核心、薄翼与发光开胸。
- 画法：CML128 A常态；深墨蓝线压、4–7大色块、最多两级硬阴影、有限材质分面、近零磨损。风格图永远不提供解剖。

## 8. 失败停门

若Call02出现身份拼接、旧拓扑、额外小体、自由透视、眼平机体、烘入UI／伪字或无法确定性分离的未来时态，本轮即标失败并回制作人；不得自动消耗Call03/04补抽。
