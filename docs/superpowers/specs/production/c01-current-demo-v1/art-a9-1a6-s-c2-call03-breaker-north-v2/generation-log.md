# Call03 BREAKER north generation log

Verdict: `CALL03_VISUAL_FAIL_TURTLE_QUADRUPED_READ / NO_MASTER_PROMOTION / CALL04_FALSE`

- tool_mode: built-in imagegen skill
- use_case: stylized-concept
- Call03_used: 1
- Call03_reroll_count: 0
- Call03_edit_count: 0
- Call04_used: 0
- Call04_allowed: false
- environment_reference_count: 0
- supplied_image_reference_count: 2 exactly
- original_result_path: `/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-22b63db9-aba5-4477-83b3-a858ba117a93.png`
- workspace_raw_copy: `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c2-call03-breaker-north-v2/generation-raw/CALL03_BREAKER_NORTH_RAW.png`
- workspace_raw_sha256: `0aef14923503f0c132343cb0223306580470911bfe32b9e57a5fe33e0664c592`
- raw_dimensions: 1254x1254 RGB opaque
- call_dispatched_under_task116_sha256: `bc65baa50b3cebe4d87accc6b36ac58e318ae0a1bfca273818664a665efefda1`
- packaged_under_current_task116_sha256: `da9a7f3add17703a477eb3bb90db92b413b37f2a5107b36301ac5ebc691002fd`
- current_board_sha256: `4bf4234b6d5e31732b832ffdc78252eb13ec3eaa7bcb9e3e68f14821f85247be`
- current_interface_sha256: `5023cd88413a77ea28c86c3723cd76fee292d58d89e8310f3d7bde1b573fd8b8`
- reference_1: `BREAKER_NORTH_CAMERA_V2_40X24_GEOMETRY_GUIDE_384.png` / `fedfd4e3150b4856f4120fb832b2b3a8f1ba00f9a0b6b90f2c2c4701497d7131`
- reference_2: `BREAKER_BX_ISOLATED_SAFE_REFERENCE_BOARD_2400x1800.png` / `e36bd3c9d186806d88614bd9f9df1eb97b56228889cc96b2cad1fda992170ee3`
- no ENV-A1, Call02, old A4, Guardian Z, CONTACT, UI, or other unit image was supplied

The governance update added Task115/current packaging hashes without changing the two image inputs, generation target, prompt, or budget. No second call was made.

## Exact prompt

```text
Use case: stylized-concept
Asset type: single game-unit master for a 384×384 tactical-map sprite, Candidate only.

Input images:
- Image 1 is the exact Camera V2 geometry and framing guide. Preserve its square safe area, 3×3 footprint, bottom-center pivot [192,320], semi-upright load-bearing envelope, and map north facing toward screen upper-right [40,-24]. Do not reproduce its cyan/magenta outlines, arrow, frame, or markers.
- Image 2 is the only identity and style reference. Faithfully adapt its approved BREAKER B body topology together with X heterogeneous bio-armor. Do not redesign the body and do not use any anatomy, unit, environment, or text outside the approved BREAKER crops/rule card.

Primary request:
Create exactly one isolated full-body BREAKER north-facing Camera V2 master. It is a near-30-meter black armored breach shell. The first read must be a giant high back shell pressing down over the torso, a very low head embedded under the front shell lip with one narrow red slit, two massive load-bearing forelimbs holding a semi-upright charge-ready posture, and very short rear feet used only for stabilization. The silhouette must remain the approved B load path; X surface treatment must cover it with asymmetric heterogeneous curved bio-armor plates, flexible seams, continuous organic load paths, a closed chest seam, and a sealed upper-back outlet.

View and pose:
Orthographic 40×24 dimetric tactical-map view, body facing screen upper-right. Show the top of the shell and shoulder/back planes while keeping both weight-bearing forelimbs and short rear stabilizers readable. Full subject visible, centered, generous keying margin, feet/ground contacts aligned to the Image 1 bottom-center pivot. No free-perspective hero angle and no eye-level front view.

Style:
KINETIC_CEL finished game art: clean controlled line pressure, 4–7 large value/color masses, at most two hard-shadow levels, restrained wear, crisp readable silhouette at 50%. Black and deep blue-gray shell, limited cold steel facets, one narrow red eye slit only. Alien bio-armor rather than industrial symmetric boxes.

Backdrop:
Perfectly uniform flat chroma-key green (#00FF00), edge-to-edge. No gradient, texture, floor, horizon, contact shadow, cast shadow, reflection, glow, atmosphere, or environmental pixels.

Hard constraints:
Single subject only. No text, labels, arrows, UI, footprint diamond, guide marks, weapons, projectile, FX, environment, ground, rocks, buildings, vehicles, people, swarm, second unit, wings, or open back outlet.
Must NOT read as turtle, ape/gorilla, ordinary quadruped animal, car, sled, tank, beetle, crawling vehicle, or symmetrical four-legged walker.
Do not make four equal animal legs: the forelimbs carry the body in a semi-upright breach posture; rear feet are short stabilizers.
Do not add a tail, horns, cockpit, wheels, treads, backpack, cannon, claws as the main read, or a second red light.
No photopaint, high-frequency noise, industrial kitbash symmetry, watermark, or signature.
```

The producer inspected the raw pixels and invoked the Task116 one-vote failure rule. No background extraction, pivot registration, 384 master, or QA promotion was executed.
