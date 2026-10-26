# A9.1-A6-S generation log

## Reference exclusion

- `source-guides/IDENTITY_STYLE_REFERENCE_MOSAIC_2400x1800.png`: `unused_identity_conflicting`; contains conflicting wing/backpack anatomy and was never supplied to ImageGen.
- `source-guides/IDENTITY_STYLE_REFERENCE_MOSAIC_SAFE_2400x1800.png`: approved safe replacement; SHA-256 `dc473235883669165e0eef58ce8c9d390e719e946e133648893b7d0ca83f3276`.
- A prior seven-reference request failed local input validation (`referenced_image_paths must contain at most 5 paths`) before generation began; it consumed no generation budget and produced no image.

## PLAN call 01

- Actual generation count after call: `1/4`
- Mode: built-in ImageGen
- Intent: full-screen PLAN cleanplate generation from references
- Input 1: `source-guides/GF_PLAN_GEOMETRY_GUIDE_1280x720.png` — exact camera, crop, geometry, scale, actor-position and occlusion guide
- Input 2: `source-guides/IDENTITY_STYLE_REFERENCE_MOSAIC_SAFE_2400x1800.png` — sole identity/style board
- Input 3: `../art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png` — Rift Swarm map-camera identity only
- Raw built-in output: `/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-8a80f887-a114-4d30-995b-038039fbfa4b.png`
- Project copy: `generation-raw/GF_PLAN_CLEANPLATE_CALL01_RAW_1672x941.png`
- Output SHA-256: `3ef48a982f5b85f0322451e50c1560b3666dd537b68aafecb5499dde96ac1c46`
- Output dimensions: `1672x941`
- Producer gate: stopped immediately after project copy; no second call or deterministic resampling performed.

### Exact prompt

```text
Use case: stylized-concept
Asset type: 1280x720 integrated tactical-game PLAN cleanplate; non-separable Candidate whole-screen lookdev.

Input images:
Image 1 is the mandatory exact geometry and A4 city-map camera guide. Preserve its fixed 2:1 dimetric camera, crop, street/building layout, actor marker locations, relative scale, roof/foreground local occlusion, and narrow dark navy bands above and below the map viewport. Turn it into finished art, then remove every guide polygon, route line, footprint marker, label, ghost, debug box, and safe-zone tint.
Image 2 is the only approved identity/style board. Top-left is Guardian Z V10X anatomy and color identity; top-right is BREAKER B body topology; bottom-left is BREAKER X surface relationship; bottom-right is CML128 STYLE ONLY. The bottom-right area is style evidence only: ignore depicted anatomy absolutely. Guardian Z must have no wings and no backpack.
Image 3 is the approved small Rift Swarm map-camera identity; use it only for the three small swarm bodies.

Primary request:
Create a polished rainy-night tactical PLAN cleanplate in the exact world and positions of Image 1. This is the present-time PLAN state, not an action tableau. Render only the current physical entities. Do not render future endpoints, intent ghosts, route lines, predictions, UI, captions, text, pseudo-writing, logos, or watermark.

Exact current entities and directions:
- Guardian Z current body at grid [15,11], facing east, occupying its 2x2 footprint. The [20,9] south marker is prediction only and must be absent.
- BREAKER current body at [20,13], facing north, occupying its 3x3 footprint. The [20,11] marker/corridor is intent only and must be absent.
- Emergency vehicle at [17,10], facing east.
- Rift Swarm units at [22,7] facing west, [26,12] facing north, and [29,5] facing south.
- The security gate at [27,8] remains active; the wall-hung shield at [14,10] retains three scorch marks.
- Preserve the east protection area as ordinary city terrain, not as a visible debug zone.

Guardian Z identity lock:
18m old-super-robot weight, about four heads tall, compact broad shoulders, E02 two arms only, no wings, no backpack. Gold layered crown with central red crest and blue forehead armor, stern silver grille face, red X chest armor with real interlocking thickness, circular gold chest core, broad square shoulder rings, equal-weight cylindrical forearms, V10X red/navy/white/gold palette. Do not redesign or add equipment.

BREAKER B+X identity lock:
About 30m and visibly larger than Guardian Z. High giant back shell compressing the torso; very low head embedded into the shell front with one narrow red slit; front limbs bear the mass in a semi-upright topology; short hind feet only stabilize. Asymmetric alien/biological armor plates and flexible seams form one continuous load path; closed chest seam and sealed upper-back outlet. It must not read as a vehicle, sled, armored car, turtle, gorilla, ape, or ordinary quadruped animal. Do not redesign its body.

Style/finish:
KINETIC_CEL tactical illustration: clean confident ink pressure, four to seven dominant color masses, no more than two levels of hard-edged shadow, restrained material facets and near-zero wear. Rain-dark navy city, wet asphalt reflections kept subtle and readable, warm emergency lights and controlled red threat accents. Units must remain legible at 50% scale, with clear silhouettes and believable tile-ground contact. Keep the A4 buildings and streets recognizable and preserve local roof/foreground occlusion rather than globally fading layers.

Critical crop and time invariants:
S3 [29,5] and EXIT [31,7] must remain only partially visible at the far right edge exactly as Image 1. Never move either inward or toward the center. The artillery source [29,2] remains offscreen outside the fixed crop; never depict it in-frame. No artillery beam, shell, muzzle flash, impact, crater, road buckle, red charge, contact collision, explosion, or T4/T5 event.

Composition/framing:
Exact fixed 16:9 whole-screen composition matching Image 1. No camera rotation, no zoom change, no coordinate relocation, no cinematic close-up, no enlarged hero framing. Leave the top and bottom bands visually quiet for later deterministic UI.

Avoid:
No extra actors or vehicles; no human figures; no generated text; no pseudo-glyphs; no speech bubble; no HUD; no guide shapes; no full-frame bloom; no soft plastic 3D; no photorealism; absolutely no Guardian wings or backpack; no conflicting alternate mecha anatomy.
```
