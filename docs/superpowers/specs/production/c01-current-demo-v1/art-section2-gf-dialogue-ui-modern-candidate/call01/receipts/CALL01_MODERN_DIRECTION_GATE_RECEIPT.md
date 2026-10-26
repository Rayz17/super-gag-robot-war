# GF Dialogue UI Modern Direction Board｜Call 01 Visual Gate

> Status: `PASS_MODERN_DIRECTION_GATE / CANDIDATE_DIRECTION_ONLY`
>
> Date: `2026-08-24`
>
> ImageGen calls in this modern refit: `1`
>
> User acceptance / transparent-component production / Godot / Runtime / Canon: `false`

## 1. Output

- Full direction board: `../raw/GF_DIALOGUE_UI_MODERN_DIRECTION_BOARD_CALL01.png`
- 50% visual gate: `../qa/GF_DIALOGUE_UI_MODERN_DIRECTION_BOARD_50PCT.png`
- Full size: `1672 x 941`, RGB presentation board
- Full SHA-256: `54c2fd074699dccc363e4eeca2ea0a2021823b96b2c765f3d32859848c0fa446`
- 50% SHA-256: `279d4aa0720e93100ece2839a8698be741db85d103901d88f573b725e531fa0d`

This call intentionally requested a neutral dark presentation board. Native alpha was not a gate at this direction stage and the RGB mode is not a failure. The image is not a production atlas and must not be sliced or consumed.

## 2. Reference isolation

Positive image references supplied to ImageGen:

- `GF_PLAN_1280x720_v2.png` — hierarchy, restraint and navy/cyan/white relationship only; SHA-256 `c1d2219354a7c8bd6fcccc326181e4875f4e292d916fb0b7512cafd06fce5f1c`
- `GF_CONTACT_1280x720_v2.png` — hierarchy, restraint and battle-peak UI reduction only; SHA-256 `83b713d6f700aa3b0bacc541902d98b92baa3de7730f502a1197a783b71c1633`

The user-rejected Call01 raw, deterministic salvage atlas, crops and QA images were **not** supplied as image inputs and no rejected pixels were copied, cropped, sampled or composited into this board.

## 3. Internal 50% gate

Passed for modern-direction review:

- no gold ornamental edge, filigree, jewel, shield, lock, crest, rune or fantasy arrow;
- no Gothic, magical, medieval, D&D, embossed ceremonial or steampunk material language;
- asymmetrical left structural rail, thin clipped planes, smoked navy glass and restrained cyan/white signals read as modern bridge avionics;
- the six requested specimens remain distinct at 50%: dialogue field, speaker/data tab, local-scene bracket, progress rail, three control states and signal divider;
- cyan and orange remain sparse functional signals rather than full-frame decoration;
- no readable text, logo, character, map or scene was generated.

## 4. Non-passing production details

This is **not** approval of the specimens as final assets:

- the dominant dialogue specimen still closes too much of its perimeter; production refinement must open at least two edges more decisively;
- the current language is convincingly modern but still somewhat generic tactical sci-fi; the next design must add a restrained, ownable “Wanji Museum bridge + museum guidance” identity without adding decoration;
- cool-white information hierarchy is lighter than the target and must be proven with actual Chinese dialogue at 1280x720;
- the direction board is RGB on a presentation background, so it has no component alpha or crop permission.

Therefore the next legal action is user judgment of **style direction only**. True-alpha component production starts only after that judgment and requires a separate call and separate technical gate.

## 5. Lifecycle

```text
candidate_direction_board_only = true
user_visual_acceptance = false
production_component_source = false
test_only_consumption_allowed = false
godot_modified = false
runtime_allowed = false
runtime_handoff = none
canon_modified = false
```
