# Call01｜Built-in ImageGen prompts

> Mode: `built_in_imagegen`
>
> Calls: `3` · random rerolls: `0`

## 1. `brace/east` — internal PASS

```text
Use case: stylized-concept
Asset type: single tactical-map mecha action sprite for a 256 x 256 RGBA game canvas
Input images: Image 1 is the edit target and the sole positive identity, design, material, lighting, camera, and EAST-facing reference for the user-approved Guardian Z V10X Camera V2 sprite.
Primary request: change only the pose of Image 1 from neutral idle to a clear impact-ready BRACE pose. Preserve the exact same Guardian Z V10X robot design, proportions, head, grille face, gold horns, red chest plates, dark navy armor, white thigh armor, cylindrical forearms, intact two arms, material wear, and fixed high-oblique dimetric Camera V2 EAST view.
Pose: lower the center of mass; spread both feet firmly on one shared ground plane; bend both knees; keep heels planted; compress the hips and torso; angle shoulders and both empty forearms into the expected collision so the silhouette reads as bracing even at 50 percent size. No shield and no weapon. Do not rotate or mirror the unit; preserve the exact EAST screen direction and top-plane visibility from Image 1.
Composition/framing: one complete full-body unit only, centered, generous transparent margin; do not crop horns, fists, knees, or feet; bottom-center foot contact is the sprite anchor; visually match the approved idle sprite scale.
Scene/backdrop: genuinely transparent background, no checkerboard pixels and no floor plane.
Constraints: edit only the pose; preserve exact identity and camera; exactly two arms, two hands, two legs; both forearms intact; no text, no labels, no UI, no enemy, no VFX, no projectile, no impact flash, no dust, no cast shadow, no logo, no watermark.
Avoid: redesign, generic super robot substitutions, old Guardian Z designs, wings, backpack, shield, armor plate, extra limbs, missing limbs, cross-facing drift, eye-level view, orthographic turnaround, baked background.
```

## 2. `brace/south` — internal PASS

与第一条同一合同，只将唯一输入和方向换为用户已通过的 south 基础；明确 `SOUTH = screen lower-left`，禁止旋转、镜像、跨朝向或盾。

## 3. `shield_take/south` — blocked, no Candidate promotion

```text
Use case: compositing
Asset type: single tactical-map mecha action sprite for a 256 x 256 RGBA game canvas
Input images: Image 1 is the edit target and sole positive Guardian Z identity, design, material, scale, lighting, Camera V2, and SOUTH-facing reference. Image 2 is the user-accepted A17 shield FRONT EXTERIOR design reference. Image 3 is the same shield REAR INTERIOR mechanical reference and defines the two rear handles.
Primary request: create one SHIELD_TAKE key pose by changing only Image 1's pose and adding exactly one A17 shield. Guardian Z is pulling the heavy shield into fighting position with both hands already gripping the two handles on the shield's REAR INTERIOR. Preserve the exact V10X identity and fixed high-oblique SOUTH Camera V2 direction toward screen lower-left.
Action pose: a visibly transitional lift, not a neutral hold. Both shoulder-to-elbow-to-forearm chains continue naturally behind the shield to the two rear handles. Exactly two rear-handle contacts. The shield is in front of the chest and abdomen and its FRONT EXTERIOR faces the same SOUTH enemy direction as Guardian Z. No hand or finger may appear on the exterior/front surface.
Shield continuity: preserve A17's crown, tapered point, thick rim, blue-white-old-metal palette, gold accents, and central load-bearing spine. This is before the red impact, so show exactly the three broad shallow old scrape scars as cold pale damage and remove the later fourth glowing red heat scar. No bullet holes, no round perforations.
Constraints: exactly one robot, one shield, two arms, two hands, two legs; front hand count = 0; rear handle hand count = 2; transparent background; no UI, enemy, VFX, text or watermark.
Avoid: old Guardian Z, perforated armor plates, one-hand side carry, hands on the front or edge, shield behind the robot, opposite facings, wrist mounting, missing forearms, cross-facing drift, redesign.
```

首次结果把冷盾画成四道浅痕，且动作首读偏 `hold/block`；因此本包在该门停止，没有调用后三姿势。

