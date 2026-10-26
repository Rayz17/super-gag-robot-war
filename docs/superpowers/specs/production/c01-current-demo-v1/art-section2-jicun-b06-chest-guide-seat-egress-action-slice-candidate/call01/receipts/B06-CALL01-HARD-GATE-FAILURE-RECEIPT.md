# B06 Jicun chest-guide-seat egress — Call 01 hard-gate receipt

## Authored beat lock

- Source: `game-godot/content/c01_breaker_demo/story_bridges.json`
- Beat: `B06_JICUN_IS_STILL_INSIDE`
- Speaker: `纪存`
- Exact line: `有点响，别的没事。`
- Action slot: `JICUN_EXITS_GUARDIAN_CHEST`
- Subject/kind: `纪存 / character`
- Existing visual mode: `map_wide_caption`
- Stage direction: `纪存从馆守Z胸前导览席进入主厅；右臂残片留在封锁广场。`

No story line, visual mode, Reader, Canon, or Godot binding was changed.

## Authority and reference isolation

- Current identity authority: `CML001` and `V35-GF纪存与BREAKER用户视觉锚Current-Canon迁移-2026-08-23.md`.
- Sole image reference: `art-a9-gold-frame/delivery/GF_PLAN_1280x720_v2.png`.
- Reference SHA-256: `c1d2219354a7c8bd6fcccc326181e4875f4e292d916fb0b7512cafd06fce5f1c`.
- A6 young three-state art, glasses variants, old `core_jicun_stand`, and all History images were excluded.

## Execution

- Tool: OpenAI built-in ImageGen.
- Calls: `1`.
- Rerolls: `0`.
- Raw: `../raw/JICUN_B06_CHEST_GUIDE_SEAT_EGRESS_RAW_CALL01.png`.
- Raw SHA-256: `4ae747191473e7f2a84601f15cc5d061a4c1bd3d807bfbf6029c22358163c493`.
- Raw geometry: `1024x1536`, PNG RGB, `hasAlpha=no`.
- QA 100% SHA-256: `4ae747191473e7f2a84601f15cc5d061a4c1bd3d807bfbf6029c22358163c493`.
- QA 50% SHA-256: `e44e1c8747bf1ecec4403fbddba6fdea8ef048093103de7331edea20f15643b7`.

## Hard-gate result

- Identity: internal pass. It preserves the current adult GF face/age direction, black hair, no glasses, navy museum coat, white shirt, and visible left-forearm terminal.
- Semantics: internal pass. One hand braces against the seat/cabin frame, the body carries a slight post-impact weight shift, and there is no route-pointing gesture.
- Text/UI contamination: internal pass.
- Alpha: **hard fail**. The output is an RGB PNG with a baked checkerboard, not a genuinely transparent action slice.

Final disposition: `FAIL_STOP_ALPHA / NO_DELIVERY / NO_GODOT_BINDING`.

Lifecycle: `Candidate attempt / user_visual_acceptance=false / runtime_allowed=false / canon=false`.
