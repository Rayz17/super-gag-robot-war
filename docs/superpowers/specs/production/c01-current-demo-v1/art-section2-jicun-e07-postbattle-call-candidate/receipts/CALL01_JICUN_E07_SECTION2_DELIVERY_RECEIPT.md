# JICUN E07 Section2 delivery receipt

## Result

`PASS_INTERNAL_CANDIDATE_GATE / USER_REVIEW_REQUIRED / NOT_BOUND`

One exact missing C01 post-battle action slice was produced for `E07_NEXT_TIME_I_BOOK`. It is a review Candidate only. No Godot, Runtime, Canon, story or binding file was changed.

## Story readback

| Field | Exact value |
| --- | --- |
| beat | `E07_NEXT_TIME_I_BOOK` |
| line | `下次我来订。` |
| slot | `JICUN_POST_BATTLE_CALL` |
| subject | `纪存` |
| visual mode | `remote_comms` |
| dramatic use | private post-battle continuation; not victory reward; not route-setting |

`story_bridges.json` SHA-256 at production time: `91184a97f3276d8f3d992bc7ab12c375ed237f195e4a0b6ba2b33f756075b6df`.

## Identity hard gate

Pass for Candidate review:

- adult Chinese male reading retained;
- slightly long adult face, small grey-blue eyes and black layered hair remain traceable to current GF PLAN;
- no glasses, beard, old-curator face or A6 young-face reuse;
- dark navy museum coat, open white shirt, badge and left-forearm archive terminal retained;
- only current GF PLAN and a deterministic crop of the same GF frame were supplied as visual references.

This is not a claim of user visual approval. `CML001` remains the authority; the new pixels remain Candidate.

## E07 semantic hard gate

Pass for Candidate review:

- shoulders lowered and posture visibly tired without collapsing;
- expression restrained, calm and adult;
- right arm hangs naturally, fingers relaxed, no pointing or route gesture;
- left forearm terminal is used quietly with a compact dim interface;
- no battle, command or victory pose;
- no text, background, panel, weapon or map route graphic.

## Alpha hard gate and preservation metrics

The built-in raw result failed the direct-alpha gate because it arrived as `RGB 1022×1538` with a baked checker. The raw file was preserved unchanged and was never treated as delivery.

The delivery was recovered deterministically by removing only bright/neutral pixels connected to the canvas edge. The white shirt, badge, skin highlights and terminal remain enclosed foreground. No generated RGB pixel was repainted or recolored.

| Metric | Result |
| --- | --- |
| raw mode | `RGB` |
| delivery mode | `RGBA` |
| RGB pixels changed | `0` |
| alpha values | `{0,255}` only |
| alpha=0 pixels | `818542` |
| alpha=255 pixels | `753294` |
| nonzero alpha bbox | `x=109..803, y=24..1520` |
| transparent components | `1` |
| edge-connected transparent components | `1` |
| enclosed transparent components | `0` |
| 100% dark/magenta review | pass for Candidate review; no baked checker field remains |
| 50% checker/light review | pass for Candidate review; full silhouette and both hands remain readable |

The reproducible extraction and QA builder is `build_alpha_and_qa.py`.

## Files

- Raw ImageGen output: `raw/JICUN_E07_POSTBATTLE_CALL_CALL01_RAW.png`
- Candidate RGBA: `delivery/JICUN_E07_POSTBATTLE_CALL_CANDIDATE_RGBA.png`
- 50/100 alpha QA: `qa/JICUN_E07_POSTBATTLE_CALL_50_100_ALPHA_QA.png`
- Prompt: `IMAGEGEN_CALL01_PROMPT.md`
- Source boundary: `SOURCE_LOCK.md`

## Lifecycle

- `status=Candidate`
- `user_approved=false`
- `runtime_allowed=false`
- `canon=false`
- `godot_bound=false`
- built-in ImageGen calls: `1`
- rerolls: `0`

Next legal gate: user/producer visual review of the exact Candidate pixels. Binding is a separate later task.
