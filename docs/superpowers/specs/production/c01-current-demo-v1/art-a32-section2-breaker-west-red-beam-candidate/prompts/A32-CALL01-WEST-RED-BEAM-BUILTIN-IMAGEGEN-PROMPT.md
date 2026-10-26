# A32 Call01 | BREAKER red_beam/west

Use case: stylized-concept
Asset type: one isolated Camera V2 tactical-map master for `ENEMY_C01_BREAKER|red_beam/west`

Input images:

- Image 1: positive high-resolution identity and material reference only. Preserve this exact BREAKER identity: low massive body, heterogeneous irregular long leaf armor, four load-bearing limbs, and one low embedded red sensor slit.
- Image 2: current north 384 map master for approved map scale, rendering density, and silhouette fidelity only. Do not mirror or rotate its pixels.
- Image 3: non-identity Camera V2 west geometry guide only. It owns the screen-space west vector `[-40,-24]`, 3x3 footprint, head/tail polarity, and bottom-center pivot intent; none of its abstract shapes or colors are final design.
- Image 4: CML129 GF PLAN full-frame reference only for the user-approved design read. Ignore all people, map, UI, environment, and other units.

Primary request: Create exactly one complete ground-shell BREAKER in a static red-beam firing/aiming pose, facing Camera V2 west. This is a new west-view redraw of the same approved unit, not a redesign and not a mirrored north image.

Composition/framing: elevated dimetric tactical-game view; transparent square canvas; whole subject fully visible; compact 3x3 footprint; low body; front/head must be at screen upper-left along `[-40,-24]`, tail at lower-right. The one low embedded red slit is on the upper-left west-facing head, never at the tail. Keep four limbs visibly load-bearing. The beam itself may be only a short contained red muzzle glow immediately outside the slit; do not draw a long beam that leaves the canvas.

Style/material: retain the exact dark charcoal-to-black stone-metal material, worn fine gold/brass seams, and irregular non-uniform long overlapping leaf plates from Image 1. Keep the silhouette heavy, asymmetrical, compressed, and alien.

Output intent: project-bound game sprite source with genuinely transparent alpha, clean edge coverage, no baked checkerboard. Leave enough transparent margin for deterministic crop and registration to a final 384x384 RGBA canvas with pivot `[192,320]`.

Hard invariants: one BREAKER only; same identity and armor topology family; one head only; one red slit only; correct west polarity; four load-bearing limbs; no missing or repeated limbs; no ordinary turtle, beetle, crab, spider, quadruped animal, tank, shuttle, or symmetric vehicle redesign; no eye pair; no mouth; no cockpit; no wings; no environment; no floor; no cast shadow; no UI; no text; no labels; no border; no watermark; no second view; no turnaround sheet.

Forbidden inputs: do not use or imitate A30 East fail, B/X schematics, Call03 outputs, or any History pixels.
