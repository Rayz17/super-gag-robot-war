# Brave Fist E03 Idle — Call01 Dispatch-Superseded FAIL_STOP

- verdict: `FAIL_STOP_DISPATCH_SUPERSEDED_AFTER_1_OF_1_CALL`
- raw_trace_only: `true`
- candidate_created: `false`
- user_accepted: `false`
- runtime_allowed: `false`
- default_allowed: `false`
- canon_migrated: `false`
- godot_binding_written: `false`
- ImageGen calls: `1/1`
- rerolls: `0`
- Blender / Three.js / Python geometry / 3D used: `false`

## Authority separation

### Hard

- `CML026 / hard / active`: Brave Fist is a complete piloted core robot with a solid body and the same large fists; no empty chest shell, tiny fist-core, unrelated replacement robot, premature independent machine soul, or premature complete Social Brave King.

### Working

- `MECHA_BRAVE_FIST_PROTOTYPE / working / active`: the complete C01 robot independently fights under Hao Si, is recovered by the company, and the same physical core later combines with external components in C03.

### Candidate

- A33 is `USER_ACCEPTED_DESIGN_ONLY`, the sole identity image source for this call. It does not imply Camera V2 sprite, Runtime, Default, or Canon acceptance.
- A34/A35 mechanisms remain Candidate awaiting user review and were not supplied or used.

### History / forbidden

- The superseded/rejected Brave Fist identities and mechanism images listed by the dispatch were not opened, supplied, copied, or used.
- This north raw becomes trace/History evidence only because the consumer target changed before delivery.

## Producer consumer correction that stops this call

Current real consumer audit establishes the first required sprite as:

- matrix row: `E03_BF_IDLE_S`
- output id: `BRAVE_FIST_E03_IDLE_SOUTH`
- action/facing: `idle / south`
- Camera V2 heading: screen lower-left `[-40,24]`
- consumer: `C01E03 / GroundMapView`
- canvas/pivot/footprint/scale: `256x256 / [128,224] / 2x2 / [1,1]`

Reason: in current R5/R6, Brave Fist stands north of BREAKER and faces it, so GroundMapView directly requests `idle/south`; that sprite can honestly replace the marker in `06A_E03_RELAY` and `06B_E03_SHELL_BREAK`. E03 first entry is actually east, while the matrix still lacks `idle/east`; north must not impersonate east. A33 is a front-biased three-quarter identity source and is more suitable for establishing a south baseline first; producing north now would invent an unconfirmed back view.

The one north-target ImageGen call had already completed when this correction arrived. A second south call would violate the explicit maximum-one-call rule. Therefore:

- no south ImageGen call was made;
- no south output directory was created;
- the north raw is retained byte-for-byte only as a trace;
- no Alpha rescue, resize, pivot registration, QA sprite, Godot copy, Runtime binding, or Candidate promotion was performed;
- a future south production attempt requires a new explicit call budget/dispatch.

This stop is caused by the corrected consumer target, not by a claim that the raw constitutes a valid north or south master.
