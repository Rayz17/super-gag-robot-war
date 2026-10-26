# GZ South Two-Hand Shield Call01 Prompt

- engine: built-in ImageGen
- calls: 1
- rerolls: 0
- mode: reference-guided generation
- intended lifecycle: Candidate raw only

## Reference roles

1. `cml008-guardian-z-current-base.png`: confirmed Guardian Z identity, head/chest language, cylindrical forearms, mass and blue/silver/red/gold palette only.
2. `retired_shield_legacy_a2_candidate.png`: retired heavy shield rectangle, thickness, wear and three old impact scars only; no wall fixture or support.
3. `PV06_S07_SHIELD_IMPACT_1280x720.png`: shield-in-front action relationship only; its one-hand/side-hold and eye-level camera are rejected.
4. `guardian-z-south-b1-1-brace-256x256.png`: south/screen-lower-left direction and planted center of mass only; its simplified identity is rejected.
5. `GF_CONTACT_1280x720_v2.png`: elevated Camera V2 dimetric view and finish target only; no actor, environment or contact composition is copied.

The incorrect `guardian_z_east_camera_v2_candidate.png` was not supplied to ImageGen and was not used as a pose anchor.

## Exact prompt

```text
Use case: stylized-concept
Asset type: Candidate master for a 2D tactical-map mecha sprite, intended to downsample cleanly to 256x256. This is one reusable static pose, not an action atlas.

Primary request: Create one isolated full-body sprite of Guardian Z in the C01E02 two-arm heavy-shield state. Guardian Z must face map SOUTH, which projects toward the SCREEN LOWER-LEFT in Camera V2. The retired heavy shield is held squarely in FRONT of the torso, between Guardian Z and an unseen BREAKER. Both intact forearms are raised and converge behind the shield; both hands must read unmistakably as gripping the shield's rear handles or the two side edges. It must never read as a shield on the back, beside the body, hanging on a wall, or floating independently.

Input image roles:
Image 1 — identity only: preserve the confirmed Guardian Z head, chest language, broad collector-toy mass, cylindrical forearms, and blue/silver/red/gold palette. Do not copy its museum background or tall realistic body proportion.
Image 2 — shield design only: preserve the retired heavy rectangular slab, thickness, dark worn surface and three old impact scars. Remove every wall fixture, hanger, stand, bracket and support.
Image 3 — action relationship only: use only the idea that the shield covers the chest/abdomen front while the body braces behind it. Reject the image's one-hand/side-hold staging and reject its flat eye-level camera.
Image 4 — direction and center-of-mass only: SOUTH means screen lower-left; use only the wide planted brace and compact four-head read. Do not copy its simplified art design.
Image 5 — camera and finish only: match the elevated Camera V2 dimetric tactical view and polished hand-painted map-art finish. Do not include BREAKER, environment, rain, UI, props, or the contact pose from that image.

Subject and pose:
- Guardian Z, approximately four heads tall, compact and very heavy, readable as an 18 m super robot.
- C01E02: BOTH arms and BOTH hands fully present and anatomically coherent.
- Recognizable helmet, gold side horns, silver grille face, red chest plates, navy-blue armor, silver joints, gold accents.
- Large cylindrical forearms remain a defining feature.
- Feet spread on one shared ground plane, knees bent, heels planted, hips lowered, torso slightly leaning back against impact: a clear defensive brace.
- Shield centered in front of chest and abdomen, slightly narrower than the shoulder span, its upper edge low enough that the entire face and both shoulders remain readable.
- Both forearms visible at the shield sides; both hands visibly wrap the rear/side grips, one hand on each side.
- Shield face normal, head, chest, pelvis and foot stance all aim toward screen lower-left. This must be an elevated three-quarter dimetric view, NOT a straight-on front elevation and NOT a side view.
- Neutral static hold with stored force: no swing trail, no second pose, no contact enemy. The same static art will be moved by root motion for both R2 block and R3 shield bash.

Composition/framing:
- One complete character only, centered in a square master canvas with generous transparent padding.
- Entire helmet horns, shield, hands and both feet visible; no cropping.
- Foot contact midpoint around 88% canvas height; stable centered pivot.
- Strong readable silhouette at 50% and 25% scale, with hands/forearms still separable from shield.

Style/medium: premium hand-painted 2D game sprite with crisp controlled edges, moderately stylized collector-mecha detail, strong value grouping, slightly brighter readable cartoon finish while retaining worn metal. No pixel art and no photoreal museum scene.

Background: genuine transparent alpha outside the subject. No checkerboard baked into RGB, no solid color, no floor, no cast shadow panel.

Constraints: exactly one Guardian Z; exactly two arms and two hands; exactly one shield; front two-handed hold; four-head body ratio; Camera V2 south/screen-lower-left; identity consistency with Image 1; shield consistency with Image 2; no logos or text.

Avoid: shield on back, shield beside body, one-hand grip, hidden/missing hands, extra limbs, asymmetrical arm loss, shield covering face or shoulders, wall mount, display stand, pedestal, enemy, environment, UI, annotations, labels, weapons, motion streaks, atlas, turnaround sheet, multiple poses, eye-level front view, baked checkerboard, watermark.
```
