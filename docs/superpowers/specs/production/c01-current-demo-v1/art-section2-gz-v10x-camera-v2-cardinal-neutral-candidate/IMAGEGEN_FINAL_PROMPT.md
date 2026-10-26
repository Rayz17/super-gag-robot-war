# Call01｜内置 ImageGen 最终提示词

> 模式：内置 `imagegen`
>
> 调用：`1`
>
> 随机重抽：`0`

```text
Use case: stylized-concept
Asset type: C01 tactical battle-map shared sprite master sheet, Candidate art only
Input images: Image 1 is the sole high-priority Guardian Z V10X identity parent; Image 2 is only an auxiliary design-orthographic reference for the same robot's proportions, construction, asymmetry and palette. Do not copy Image 2's eye-level orthographic camera.
Primary request: Create one clean 2x2 shared master sheet containing exactly four neutral-idle full-body renders of the SAME Guardian Z V10X robot under one fixed battle-map camera. This is camera adaptation, not redesign.
Grid order: top-left = NORTH, top-right = EAST, bottom-left = SOUTH, bottom-right = WEST. Do not render any labels or text.
Camera: fixed parallel orthographic 2:1 dimetric camera for all four cells, approximately 45-degree azimuth and 30-degree downward elevation, with clearly visible top planes, no vanishing points and no perspective size falloff. The camera remains fixed while the robot rotates on the ground.
Facing screen vectors and view read:
- NORTH faces screen upper-right and shows rear plus one side in elevated three-quarter view.
- EAST faces screen lower-right and shows front plus one side in elevated three-quarter view.
- SOUTH faces screen lower-left and shows front plus the other side in elevated three-quarter view.
- WEST faces screen upper-left and shows rear plus the other side in elevated three-quarter view.
Subject identity invariants: exactly the V10X design from Image 1; about 4.2 heads tall; both E02 arms complete; broad round shoulders; equally thick cylindrical forearms and lower legs; white thighs; deep navy blue and vivid red main armor; bright red X-shaped chest armor split around the white vertical sternum; round gold chest core; complete gold horned crown and navy helmet with red center crest; silver vented lower face; sturdy large feet. Preserve the same right-shoulder old-wear asymmetry without mirroring it. No shield, no wings, no backpack, no weapon, no effect.
Pose: neutral alert idle, weight evenly supported, arms relaxed and slightly separated from torso, fists down, feet planted on a shared ground plane. All four are the identical model with identical proportions and armor, rotated only; consistent foot contact, height, shoulder width, volume and silhouette.
Composition/framing: transparent-background 2x2 sheet; each robot centered within an equal quadrant, completely visible with generous padding; same pixel height and same foot baseline relative to its quadrant; no overlap and no cropping.
Style/medium: bright modern Japanese animation game-sprite concept render; KINETIC_CEL language with deep ink-navy pressure outlines, large readable color blocks and two-step hard cel shadows; clean enough to remain readable when reduced to 256x256. Fixed shared light: top planes medium bright, screen-right-facing planes slightly brighter, screen-left-facing planes darker. Keep detail restrained and silhouette-first.
Constraints: genuinely transparent background; exact four subjects only; no floor, no cast shadow, no grid, no frame, no labels, no text, no watermark. Maintain the same design in every cell.
Avoid: eye-level hero view; front/side/back turnaround views; camera orbit; foreshortening; near-big/far-small perspective; mirrored east/west substitution; different head, chest, limbs, proportions or color layout per cell; old Guardian Z designs; gritty catalog rendering; excessive micro-detail; chibi deformation beyond the established 4.2-head V10X proportion.
```

ImageGen 返回 RGB 棋盘格；后续脚本只删除与画布边界连通的高亮中性色背景像素。RGBA 母版的 RGB 字节与 raw 完全一致，未重绘、旋转、镜像或修补机体。

当前视觉门按 Task111 的 `CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE / map_dimetric_40x24 / P(x,y)=((x-y)*40,(x+y)*24)` 读回。提示词中的“approximately 45-degree azimuth and 30-degree downward elevation”是画面语言，旧 40×20 合同不参与本包正向校准。
