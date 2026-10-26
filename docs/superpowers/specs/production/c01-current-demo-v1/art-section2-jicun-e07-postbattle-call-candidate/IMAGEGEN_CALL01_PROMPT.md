# Built-in ImageGen call 01

- Mode: built-in ImageGen
- Calls: 1
- Rerolls: 0
- Inputs: current GF PLAN frame and a deterministic crop of that same frame, both identity references only

```text
Use case: stylized-concept
Asset type: transparent game character action-slice for C01 post-battle dialogue, slot JICUN_POST_BATTLE_CALL, beat E07_NEXT_TIME_I_BOOK
Input images: Image 1 is the user-approved current GF PLAN screen identity anchor; Image 2 is a deterministic crop of the same current anchor emphasizing Ji Cun. Both are reference images only, not edit targets.
Primary request: Generate one new transparent cutout of the exact same Ji Cun during a private remote call immediately after an exhausting battle. He has just heard that the restaurant kitchen has closed and calmly answers, "Next time I will book it." Do not render this text.
Subject identity — preserve exactly from the references: adult Chinese male Ji Cun; same slightly long adult face, small grey-blue eyes, black layered tousled hair, no glasses, no facial hair; same simple dark navy museum curator coat over open-collar white shirt; same museum badge; same left-forearm archive terminal hardware.
Pose and acting: mid-thigh-up or three-quarter character slice with both hands clearly visible. His shoulders are lowered and relaxed, posture subtly tired after the battle but still composed. Calm restrained adult expression with a trace of warmth, not a broad smile. His left forearm is turned inward and the archive terminal is being used quietly with a dim restrained cyan interface, not projected as a large map. His right arm and hand rest naturally at his side or loosely near his waist, fingers relaxed and slightly curled. Absolutely no pointing finger, no route gesture, no command gesture, no battle pose, no victory pose.
Style/medium: match the GF PLAN character's polished Japanese 2D game/anime cut-in language; deep ink-blue pressure lines, large clean color masses, two-step hard cel shading, restrained archive-interface glow. Preserve adult proportions and grounded weight.
Composition/framing: isolated single character, readable silhouette, full head and both hands included, generous transparent margin, no cropping through fingers or hair.
Scene/backdrop: genuinely transparent background, alpha channel; no scenery, no panel, no frame, no floor, no shadow plate.
Constraints: same identity and costume as current GF; left-arm terminal only; correct left/right anatomy; five natural fingers on each visible hand; no extra limbs; no handheld phone; no weapons; no headset; no eyeglasses; no youth redesign; no old curator; no pointing; no battle tension; no route/map diagram; no text; no logos; no watermark. Preserve actual transparency with clean edges and no white halo.
```

The built-in result arrived as RGB with a baked checker. It was preserved verbatim under `raw/`; deterministic edge-connected alpha recovery was then applied without changing any RGB pixel.
