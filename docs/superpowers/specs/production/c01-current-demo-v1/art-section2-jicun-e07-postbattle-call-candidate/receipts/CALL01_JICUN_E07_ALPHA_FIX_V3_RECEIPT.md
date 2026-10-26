# JICUN E07 Alpha Fix V3 receipt

## Result

`ALPHA_ONLY_LOCAL_FIX_COMPLETE / CANDIDATE / USER_REVIEW_REQUIRED / NOT_BOUND`

- source V2 SHA-256: `de06a6775c65e56370e71aa52f85c080df659b7e0bab6abbae09c46e8cc53298`
- repaired V3 SHA-256: `a828de1699a493589c611ea52ef0125603e6e934ec149ec5246880c2871b113e`
- size/mode: `1022x1538 RGBA8`
- ImageGen: `0`; Blender: `0`; global white key: `false`

## Manual negative-space decision

At 10x on dark, light, saturated-magenta and saturated-green backgrounds, the previous held component `[590,103,599,114)` follows a narrow hair specular/edge stroke. Only `6/41` pixels support the fitted checker phase (`14.6%`), with no checker-scale alternation. Independent visual/topology review agrees that it is not a confirmed background hole. It is therefore reclassified as `KEEP_CONFIRMED_HAIR_HIGHLIGHT_OR_EDGE`; no Alpha pixel was changed.

| audited zone | decision |
| --- | --- |
| hair strands | existing loops remain transparent; the 41-pixel hold was reviewed and kept as hair highlight/edge |
| left arm / torso | the V2 enclosed gap remains transparent; no new opaque background found |
| crossed hand / terminal | visible inter-finger spaces fall over shirt, sleeve or terminal pixels, not scene background; kept |
| hanging hand / fingers | visible gaps fall over the coat/trouser body behind the hand, not scene background; kept |
| coat hem / legs | leg and tail negative spaces were already transparent; kept unchanged |
| shirt / skin / badge / highlights | confirmed subject; untouched |

## Byte evidence

| metric | V2 | V3 |
| --- | ---: | ---: |
| alpha=0 | 820,918 | 820,918 |
| alpha=255 | 750,918 | 750,918 |
| partial Alpha | 0 | 0 |
| RGB pixels changed | 0 | 0 |
| Alpha pixels changed | 0 | 0 |

- Alpha change bbox list: `[]`
- Alpha changed pixels: `0`
- manually reviewed/kept bbox: `[590,103,599,114)`; `41` subject pixels
- full-person alpha bbox: `[109,24,804,1521)`
- `safe_crop_rect` with at least 16-pixel subject padding: `[93,8,820,1538)`

## Lifecycle

- `status=Candidate`
- `user_approved=false`
- `runtime_allowed=false`
- `canon=false`
- `godot_bound=false`
- local `asset-manifest.tsv`: V2 retained as `Candidate_Superseded_By_Manual_Alpha_Audit`; V3 registered as the unapproved Candidate
