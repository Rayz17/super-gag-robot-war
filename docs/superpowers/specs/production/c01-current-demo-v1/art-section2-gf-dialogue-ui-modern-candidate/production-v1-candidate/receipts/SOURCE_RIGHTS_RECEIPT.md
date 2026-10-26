# GF Modern Dialogue UI Components｜Source Rights Receipt

> Status: `PASS / PROJECT_APPROVED_DIRECTION_SOURCE_ONLY`
>
> Date: `2026-08-25`

## Sole positive pixel source

- `../../call01/raw/GF_DIALOGUE_UI_MODERN_DIRECTION_BOARD_CALL01.png`
- SHA-256: `54c2fd074699dccc363e4eeca2ea0a2021823b96b2c765f3d32859848c0fa446`
- User direction acceptance: `../../USER_ACCEPTANCE_2026-08-25.md`

The six RGBA components were deterministically derived from that accepted modern direction board. No new ImageGen call was used for component production.

## Explicit exclusions

- The user-rejected ornate/D&D Call01 raw, salvage atlas, components and QA files were not read as pixel sources and were not composited, sampled or transformed.
- `GF_PLAN` and `GF_CONTACT` were references used during creation of the accepted direction board only. Their pixels were not read by the deterministic component script.
- No character, map, logo, dialogue, beat count, internal ID, third-party UI or external game asset is baked into these files.

## Deterministic method

`../build_modern_rgba_components.py` verifies the approved source SHA, estimates only its neutral presentation backdrop from empty zones, reconstructs authored foreground color/alpha, removes unanchored low-intensity backdrop residual, opens three long perimeter segments on the dialogue panel, neutralizes warm-neutral bevel light to cool white, and emits fixed component crops plus QA.

This receipt authorizes isolated Candidate test frames only. It does not authorize Runtime, Default, Save, Canon or final visual acceptance.
