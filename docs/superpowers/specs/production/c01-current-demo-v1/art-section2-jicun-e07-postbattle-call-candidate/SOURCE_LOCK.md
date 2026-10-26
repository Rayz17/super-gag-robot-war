# JICUN E07 post-battle call — source lock

## Exact story consumer

- File: `game-godot/content/c01_breaker_demo/story_bridges.json`
- Beat: `E07_NEXT_TIME_I_BOOK`
- Line: `下次我来订。`
- Slot: `JICUN_POST_BATTLE_CALL`
- Subject: `纪存`
- Kind: `character`
- Visual mode: `remote_comms`
- Stage meaning: continuation of the post-battle relationship, not a victory reward and not a route-setting beat.

## Current identity authority

Only the current user-approved GF identity anchor was used:

- `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-gold-frame/delivery/GF_PLAN_1280x720_v2.png`
- SHA-256: `c1d2219354a7c8bd6fcccc326181e4875f4e292d916fb0b7512cafd06fce5f1c`
- Deterministic identity crop: `references/JICUN_GF_PLAN_CURRENT_IDENTITY_CROP.png`
- Crop SHA-256: `9deec2ec28708ffbeaa6c59a0c1ea08a637f1e039756e1275440599973cf0cdf`

The crop changes no identity pixels; it is a 430×470 crop of the same GF frame used only to make the approved face, hair, coat and terminal legible to ImageGen.

## Forbidden sources and drift

- no A6 young three-state Jicun;
- no glasses or older-curator Jicun;
- no `core_jicun_stand.png` pixel parent;
- no History art;
- no pointing hand, route gesture, command pose, battle pose or victory pose;
- no Godot binding or Runtime/Canon promotion in this package.

Status remains `Candidate`; `user_approved=false`, `runtime_allowed=false`, `canon=false`.
