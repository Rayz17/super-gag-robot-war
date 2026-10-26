# GF Dialogue UI Skin Atlas — ImageGen Call 01

Use case: stylized-concept

Asset type: production-quality 2D game dialogue HUD component atlas on a genuinely transparent canvas

Input images:

- Image 1 (`GF_PLAN_1280x720_v2.png`): mood, finish, material hierarchy, restrained map-overlay relationship, deep navy + antique gold + cyan accent reference only. Do not copy, trace, crop, or reproduce any pixel, layout, character, map, icon, text, or exact ornament from it.
- Image 2 (`GF_CONTACT_1280x720_v2.png`): mood, finish, UI restraint and weight reference only. Do not copy, trace, crop, or reproduce any pixel, layout, character, map, icon, text, or exact ornament from it.

Primary request: Create one original, coherent GF-style dialogue HUD skin component atlas for a tactical mecha game. It must look like finished hand-authored game UI art rather than rectangles drawn by code: layered deep navy / graphite mechanical material, restrained warm antique-gold metal edges, small controlled cyan-energy accents, clear thick-versus-thin hierarchy, chamfered corners, shallow engraved details, believable bevels, readable highlights and strong negative space. Modern, premium, compact, and functional.

Canvas and separation: Use a landscape transparent canvas. Arrange every component as a separate, isolated island with very large clear transparent gutters on all four sides. No component may touch, overlap, share a shadow with, or be connected to another component. Keep all outer shadows and glows tightly contained within each component's own bounding box so deterministic rectangular cropping is safe.

Required isolated components:

1. One large horizontal dialogue-frame border designed for nine-slice stretching. Empty transparent center. Four corners are substantial but compact; long middle edges remain visually simple and stretch-safe. No text.
2. One separate speaker-name tab designed for nine-slice stretching, with an empty dark center safe for live Chinese text. No text, no portrait, no emblem.
3. One separate left-side action-slice holder: a portrait/local-scene insert frame with an empty transparent window, one side open or stepped so it can visually join a dialogue panel without being physically connected in this atlas. No character or scene.
4. Four separate beat-progress ornaments in a single clean horizontal row, states visually distinguishable as idle, completed, current, locked through shape and material as well as brightness. No numerals.
5. Three separate control-hint capsules or mechanical glyph shells in one clean horizontal row, compatible with keyboard, mouse and controller prompts, but leave their centers empty; no letters, no device logo, no text.
6. One separate long gold/cyan accent divider with calm mechanical end caps, suitable for stretching or tiling.
7. One separate square seamless-looking navy/graphite fill-material sample with quiet microtexture and no strong motif, intended as a tileable dialogue-panel interior.
8. One separate narrow white/neutral alpha-mask-style highlight strip for a controlled edge sweep; no fixed colored background.

Style/medium: hand-authored premium 2D game UI asset art, crisp raster edges with subtle painterly metal finish, production-ready, visually compatible with a contemporary Japanese tactical super-robot game without copying any franchise interface.

Color palette: deep navy and graphite dominate; antique metallic gold is restrained; cyan is a limited energy accent; orange is extremely sparse and only a tiny status accent if needed.

Materials/textures: layered coated metal, fine machined bevels, subtle brushed grain, shallow engraved seams, controlled luminous cyan inserts. Avoid dirt, grunge, scratches, excessive bolts or dense greebles.

Transparency contract: The canvas background must be genuinely transparent alpha, not white, gray, black, a checkerboard, a simulated checkerboard, or a translucent rectangle. Every empty window and every gutter must also be genuinely transparent. Preserve clean antialiased edges with no white or black matte halo.

Text: none. Absolutely no letters, words, numbers, pseudo-writing, labels, logos, watermarks, candidate/debug marks, or franchise emblems.

Constraints: all components fully visible and uncropped; orthographic front-facing UI pieces; no perspective mockup; no screen, map, character, mecha, dialogue text, speech bubble, software window or background scene; keep large clean gutters; make shapes readily crop-safe and nine-slice-safe.

Avoid: generic thin-line sci-fi HUD; default geometric rectangles; flat solid-color boxes; cyberpunk neon overload; holographic wireframes; bulky industrial military warning UI; excessive orange/red; copied GF screen layout; component collage that visually merges; baked checkerboard; typography.

Output intent: one source atlas only for a Candidate art gate. It will be validated for true alpha and deterministic component separation before any crop. Runtime, Canon, Default and user acceptance remain false.
