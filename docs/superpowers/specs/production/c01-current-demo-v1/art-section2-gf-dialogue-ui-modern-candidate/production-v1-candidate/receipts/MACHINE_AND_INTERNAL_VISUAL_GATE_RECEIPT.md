# GF Modern Dialogue UI Components｜Machine + Internal Visual Gate

> Status: `PASS_FOR_ISOLATED_TEST_ONLY_HUD`
>
> Date: `2026-08-25`
>
> User accepted direction: `true`
>
> Component / actual-frame user acceptance: `false`
>
> Runtime / Default / Save / Canon: `false`

## 1. Delivery root

`docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gf-dialogue-ui-modern-candidate/production-v1-candidate`

Manifest SHA-256: `2c58f60701fded3ca4f9a75d695957d6469de3352ecc7e5ba06405f693d72c93`

## 2. Six independent assets

| Asset | File | Size / layout | Nine-slice margins L/T/R/B | SHA-256 |
| --- | --- | --- | --- | --- |
| `C01_GF_DIALOGUE_PANEL_9SLICE` | `delivery/gf_modern_dialogue_panel_9slice_rgba.png` | `768×192` | `104/48/92/48` | `68b9b94dc89a3c7f1669769e7e7fcacacedf64c422a89581278f510f4fad9f71` |
| `C01_GF_SPEAKER_TAB_9SLICE` | `delivery/gf_modern_speaker_tab_9slice_rgba.png` | `320×72` | `48/20/48/20` | `02120684e6e91a810bf8982ee24c0f1f5f7b2f38509b947c277c596b7ae743df` |
| `C01_GF_LOCAL_SCENE_STATUS_RAIL_9SLICE` | `delivery/gf_modern_local_scene_status_rail_9slice_rgba.png` | `360×320` | `64/72/64/72` | `2adfd945fe325158f5ee8c697aa6c7435036d4b9dc31696bff7d90ad11863fa4` |
| `C01_GF_DIALOGUE_PROGRESS_ATLAS` | `delivery/gf_modern_dialogue_progress_atlas_rgba.png` | `192×48`, `4×1`, cell `48×48` | `0/0/0/0` | `2d3677074c08c79170ecbe827e3336546d7b22a89060afc7d2cc4908aa111987` |
| `C01_GF_DIALOGUE_NEXT_PROMPT_ATLAS` | `delivery/gf_modern_dialogue_next_prompt_atlas_rgba.png` | `288×144`, `3×3`, cell `96×48` | `0/0/0/0` | `9243198f3835c774fa839203ef261622342a8f9eca4907213bcafcdf71ea1b6d` |
| `C01_GF_COMMS_STATUS_RAIL_ATLAS` | `delivery/gf_modern_comms_status_rail_atlas_rgba.png` | `768×48`, `2×1`, cell `384×48` | `0/0/0/0` | `2be0a79e5c5857794b49e96e7077c672b706f84147578f694cbd23a4e566063b` |

State order is authoritative in `asset-manifest.tsv`; consumers must not infer cells from filenames.

## 3. Alpha hard gate

All six files are PNG `RGBA8` and meet these machine checks:

- every asset contains alpha-zero pixels and partial-alpha material pixels;
- every asset has zero non-transparent RGB beneath alpha `0`;
- every outer image boundary has zero non-transparent alpha pixels;
- the local-scene rail center remains true transparent and does not erase or replace B06 scene content;
- edge sheets on black/navy, white and magenta show no baked presentation rectangle, white checker residue or old-Call01 matte;
- full delivery hash verification passes.

Per-asset counts are recorded in `receipts/machine-metrics.json`.

## 4. Visual hard gate

Passed internally for isolated actual-frame testing:

- the dialogue structure has explicit long openings on top, right and bottom; it no longer reads as the approved direction board's nearly closed generic frame;
- left rail, clipped terminals, matte graphite material and cyan signal details retain the approved modern avionics identity;
- five non-orange assets contain zero machine-detected gold-like pixels; the comms atlas retains only its declared sparse safety-orange decision state;
- the speaker tab, progress states, prompt states and status rails share one thin-layer material system;
- 679×163 and 1144×163 dialogue stretches, 210/330 speaker widths and 342×512 local-scene rail stretch remain coherent without corner collision;
- the 1280×720 navy gate preserves the current left-action / lower-dialogue layout and Chinese safe area.

Visual evidence:

- `qa/GF_MODERN_COMPONENTS_EDGE_GATE_DARK_WHITE_MAGENTA.png`
- `qa/GF_MODERN_COMPONENTS_ALPHA_BACKGROUNDS_50PCT.png`
- `qa/GF_MODERN_NINESLICE_STRETCH_QA.png`
- `qa/GF_MODERN_HUD_ACTUAL_1280x720_NAVY_GATE.png`
- `qa/GF_MODERN_HUD_ACTUAL_50PCT_NAVY_GATE.png`

## 5. Permission boundary

```text
user_accepted_direction = true
internal_visual_gate = pass_for_isolated_test_only
test_only_consumption_allowed = true
component_user_visual_acceptance = false
actual_frame_user_acceptance = false
formal_binding_allowed = false
runtime_allowed = false
runtime_handoff = none
godot_runtime_modified = false
canon_modified = false
```

The next authorized consumer is an isolated Candidate overlay used to capture B06 local-scene, E07 character-cutout and wide-fallback actual frames. Those frames remain review evidence only; they cannot promote these components to Runtime or Canon.
