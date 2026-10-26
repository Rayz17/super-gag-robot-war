# GF Dialogue UI Skin Atlas｜Call 01 Section 2 Hard-Gate Failure Receipt

> Superseding visual decision: `USER_REJECTED / HISTORY_ONLY / DO_NOT_USE`
>
> See `../USER_REJECTED_HISTORY_ONLY_DO_NOT_USE.md`. The deterministic recovery performed after this original technical failure is diagnostic history only and has no consumer permission.

> Status: `FAIL_STOP / SOURCE_ATLAS_REJECTED / NO_DERIVATIVES`
>
> Date: `2026-08-24`
>
> ImageGen calls: `1`
>
> Rerolls: `0`
>
> Runtime / Default / Save / Canon: `false`
>
> User visual acceptance: `false`

## 1. Requested output

One original GF dialogue HUD source atlas with isolated, crop-safe components and a genuinely transparent canvas. `GF_PLAN_1280x720_v2.png` and `GF_CONTACT_1280x720_v2.png` were supplied only as mood, finish, material-hierarchy and UI-restraint references. Their pixels were not authorized for extraction or direct reuse.

Prompt record:

- `../../IMAGEGEN_CALL01_PROMPT.md`

## 2. Raw output retained for audit only

- `../raw/GF_DIALOGUE_UI_SKIN_ATLAS_CALL01_RAW.png`
- Size: `1672 x 941`
- PNG storage: `8-bit/color RGB, non-interlaced`
- SHA-256: `a14c8f917578c60cc786f9b976a9b3788d17e78be6dd9c901519153277b9030f`

The output is visually organized into a main frame, speaker tab, action-slice holder, progress ornaments, control capsules, divider, fill sample and highlight strip. The material direction is closer to the requested hand-authored navy / antique-gold / cyan language than the current program geometry.

This positive visual observation does **not** pass the asset gate.

## 3. Hard-gate failure

The raw PNG contains no alpha channel. Its visible checkerboard is baked into RGB pixels rather than representing transparent canvas data.

Required:

```text
PNG RGBA8
canvas gutters alpha = 0
frame and holder windows alpha = 0
component outside alpha = 0
```

Observed:

```text
PNG RGB
alpha channel = absent
checkerboard = baked pixels
```

This directly violates both `SECTION2_GF_DIALOGUE_UI_ASSET_BRIEF.md` §4 and the Call 01 prompt transparency contract. It also prevents reliable proof of clean independent component boundaries, because every proposed crop would inherit synthetic checker pixels.

## 4. Fail-stop consequences

Per the task's explicit stop gate:

- no color-key extraction or deterministic checker removal was attempted;
- no component crop was produced;
- no nine-slice asset, fill tile, speaker tab, action holder, progress atlas, prompt atlas, divider or accent mask was delivered;
- no `asset-manifest.tsv`, nine-slice margin receipt or source-rights delivery receipt was emitted for consumable assets;
- no B06 local-scene, E07 character-cutout or wide-fallback 1280x720 review mockup was assembled;
- no Godot, Candidate HUD, Runtime, Default, Save or Canon consumer was changed;
- the raw file is audit-only and must never be scanned or bound by a consumer.

Current gate state:

```text
formal_gf_dialogue_skin_loaded = false
integrated_visual_playtest_ready = false
runtime_allowed = false
runtime_handoff = none
user_visual_acceptance = false
```

## 5. Next legal action

The next legal production attempt is a new Section 2 generation call that explicitly returns native RGBA transparency. It must be treated as a new call and pass alpha plus separation checks before any deterministic crop or static review composition. This receipt does not authorize a reroll in the current one-call / zero-reroll task.
