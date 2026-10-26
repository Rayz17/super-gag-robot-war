# JICUN E07 Alpha Fix V2 receipt

## Result

`PASS_INTERNAL_ALPHA_GATE / CANDIDATE / USER_REVIEW_REQUIRED / NOT_BOUND`

This was a deterministic, zero-ImageGen Alpha-only repair.  It does not alter story data, production HUD bindings, Runtime, Canon or Default.

## Exact scope

- beat: `E07_NEXT_TIME_I_BOOK`
- line: `下次我来订。`
- slot: `JICUN_POST_BATTLE_CALL`
- source V1 SHA-256: `2cd8d55529e94bfd9c49afc4080218036b698f3f8e8ee8d16a191d1ded08a35e`
- repaired V2 SHA-256: `de06a6775c65e56370e71aa52f85c080df659b7e0bab6abbae09c46e8cc53298`
- ImageGen calls in this repair: `0`

## Checker evidence and component decision

- fitted raw checker: cell=`21 px`, offsets=`(14,16)`, parity-true=`dark`
- exterior fit pixels: `47,685`
- fit MAE: `2.462521`
- no global white key was used

Removed only these confirmed enclosed-background components (half-open bbox):

| bbox | area | decision |
| --- | ---: | --- |
| `[244,762,269,947)` | 2,113 | left-arm/torso enclosed checker gap |
| `[532,51,562,70)` | 153 | enclosed hair-loop checker gap |
| `[464,32,492,39)` | 110 | enclosed top hair-loop checker gap |

Held `[590,103,599,114)` because its true white core is already exterior-connected and the remaining opaque fragment is ambiguous hair-edge antialias/highlight, not a reliable enclosed hole.

## Protection ROIs

| ROI | bbox | protected content |
| --- | --- | --- |
| P01 | `[330,175,570,445)` | face, eyes, skin |
| P02 | `[350,285,620,955)` | white shirt and highlights |
| P03 | `[315,470,415,600)` | museum badge |
| P04 | `[340,640,820,930)` | right hand, arm terminal, hologram |
| P05 | `[135,1135,315,1405)` | left hand and white cuff |

## Preservation metrics

| Metric | Before | After |
| --- | ---: | ---: |
| alpha=0 | 818,542 | 820,918 |
| alpha=255 | 753,294 | 750,918 |
| partial Alpha | 0 | 0 |
| transparent components | 7 | 10 |
| RGB pixels changed | 0 | 0 |
| Alpha pixels changed | 0 | 2,376 |

The remaining opaque-subject RGB and all transparent RGB are byte-identical to the original raw Candidate.

## Files

- repaired Candidate: `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-section2-jicun-e07-postbattle-call-candidate/delivery/JICUN_E07_POSTBATTLE_CALL_CANDIDATE_RGBA_ALPHA_FIX_V2.png`
- preflight report: `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-section2-jicun-e07-postbattle-call-candidate/receipts/CALL01_ALPHA_FIX_V2_COMPONENT_PREFLIGHT.json`
- component preflight: `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-section2-jicun-e07-postbattle-call-candidate/qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V2_COMPONENT_PREFLIGHT.png`
- black/light/magenta/saturated 50/100 QA: `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-section2-jicun-e07-postbattle-call-candidate/qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V2_50_100_QA.png`
- component proof: `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-section2-jicun-e07-postbattle-call-candidate/qa/JICUN_E07_POSTBATTLE_CALL_ALPHA_FIX_V2_COMPONENT_PROOF.png`

## Lifecycle

- `status=Candidate`
- `user_approved=false`
- `runtime_allowed=false`
- `canon=false`
- `godot_bound=false`
