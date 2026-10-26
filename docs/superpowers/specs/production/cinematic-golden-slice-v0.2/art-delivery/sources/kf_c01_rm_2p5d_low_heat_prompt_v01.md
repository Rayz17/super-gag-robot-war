# Phase A Keyframe Prompt v1

## Use

- Scene: `SCN_C01_RM_RESCUE_2P5D_V01`
- Asset: `KF_C01_RM_2P5D_STYLE_V01`
- Tool: OpenAI built-in image generation
- Mode: `stylized-concept`
- Intent: style/composition reference, not runtime art

## Reference Roles

1. `core_jicun_stand.png`: exact Jicun identity, youth/adult balance, uniform and left-arm terminal.
2. `core_doudeng_stand.png`: exact Doudeng mechanic identity and tool language.
3. `core_tangjiao_stand.png`: exact Tangjiao male punk repair-artisan identity.
4. `pose_gz_c01_kneel_start_v01.png`: locked Guardian Z design and half-kneeling restriction.
5. `wanji_c01_mecha_single_settings_v1.svg` rendered preview: Diedie's small practical real-machine silhouette.

## Production Prompt

Create one polished 16:9 in-game keyframe of the Million Mech Museum real-machine zone at night closing time. Use a coherent modern Japanese 2.5D SRPG language: production-ready cel-shaded people, hard-surface semi-painted environment, crisp silhouettes, stable geometric perspective and clear foot contact.

Use a low 35mm-feel diagonal camera and three readable depth layers. Foreground: a safety railing partially occludes Diedie and a practical quadruped rescue machine dog beside a charging dock with two green lights. Midground: Jicun is the protagonist with black hair, blue eyes, no glasses and the archive terminal on his left forearm; Doudeng works at a maintenance stop console; Tangjiao works separately at a cracked guide-panel bench; an adult visitor with a knee brace and folding cane independently tests one step toward an old service door. Far/upper layer: the locked 18m Guardian Z remains half-kneeling and only emits a restrained amber low-heat chest glow.

Include a cyan-marked low-heat floor sector, controlled guide-panel cracks, one old service door, one charging dock, one detached-corner white misclassification frame with a curled adhesive tab, and one blank scene-caption UI sample. No readable text.

Palette: night closing but readable, deep navy architecture, cyan structure lines, neutral steel/off-white surfaces, sparse warning gold and narrow amber low heat. Avoid black crush, blue monochrome and orange/brown dominance.

Hard constraints: Jicun has no glasses and is neither childlike nor middle-aged; Tangjiao remains a young man; Doudeng reads as a mechanic; Guardian Z does not stand, punch, attack or glow at full power; the adult visitor is not carried; Diedie and the machine dog remain practical real machines. No top-down isometric map, flat single lane, photoreal lobby, vector figures, old runtime portraits, gibberish text, logos, watermarks, extra people, duplicated limbs, monster machinery or weapons.

## Postprocess

- Fit the generated 1672x941 source to 1280x720 with Lanczos resampling.
- Apply a non-semantic gamma/midtone lift (`gamma 0.82`) and slight color lift (`1.04`) to keep the night palette readable.
- No semantic repaint, compositing or object replacement after generation.
