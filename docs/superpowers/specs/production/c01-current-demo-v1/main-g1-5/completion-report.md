# C01E02 G1.5-A M1 Main Program Completion Report

## Delivery Status

- Result: `PASS / integration shell ready / waiting producer`
- Runtime nature: `candidate_runtime_demo`; interface fixture only
- Producer contract commit: `cf49dac4d539d23337999807114676c9d060ec3e`
- Contract SHA-256: `844e9d15b8be1575f33b0b06992044a0cc7338284d27747802bce88eaae84b6f`
- Parent production baseline: `4347597e7f7960dc605a8ec1b53d26b7d8df91cb`
- Frozen snapshot: `fe7a0764d11f5ac5f9d11accb7398df664132b0b`
- Content fingerprint: `944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`
- Approved handoffs: `0`
- Runtime art loaded: `0`

No stop condition was triggered. No art candidate was imported, copied, opened by the runtime, or promoted. The shell is waiting for an exact producer handoff.

## Candidate-Local Interface

The manifest `C01CDV1-G1.5-M1-ASSET-SLOTS-V1` registers six data-driven slots:

| Kind | Slots | Interface |
|---|---|---|
| Tactical Q/SD | Guardian-Z; BREAKER ground shell | 2x2 / 3x3 footprint, north-west cell anchor, bottom-center pivot, four facings, 96/128 px preview |
| Named actions | Both tactical slots | required `idle`; optional `move`, `brace`, `impact`; declared optional fallback to `idle` |
| Static shot | Guardian stand; shield victory | 640x360 or 1280x720 static Pose/Cut-in gate with named geometry fallback |
| Optional video | Guardian stand; shield victory | exact producer handoff gate and same-shot static fallback |

The resolver performs no directory search. A binding is considered only when its slot explicitly selects the exact producer handoff ID. It then validates Stable ID, usage, Candidate resource root, fingerprint, binding kind, runtime permission, SHA-256, dimensions, action and facing before returning an asset descriptor.

Missing handoff, `runtime_allowed=false`, incomplete metadata, out-of-root path, missing file, wrong SHA-256, wrong dimensions, missing required action, unknown action or missing facing all fail closed to a named fixture. Rejection before an authorized binding does not probe the filesystem.

Full and Skip resolve to the same semantic result IDs. With no approved video, Full uses the same-shot static fallback and Skip resolves to its static end pose. The shell has no gameplay state mutation API.

## Evidence

- Explicit scene: `res://scenes/candidate_runtime_demo/c01/e02/asset_integration_g1_5/c01e02_g1_5_asset_shell.tscn`
- Screenshot: `BASELINE_G1_5_ASSET_SHELL_1280x720.png`
- Dimensions: `1280x720 RGBA`
- Screenshot SHA-256: `5c3572e726b960eaa76e2d32e19cc12e033a27b4019e2104efa696e82ee7fecc`
- Capture validation: 3,600 sampled pixels above the nonblank threshold
- Fixture view resource probes: `0`

The screenshot demonstrates slot dimensions, pivot, footprint anchor, facing, foreground mask separation, static Cut-in fallback and Full/Skip semantic equivalence. It is interface evidence, not an art review.

## G1.1 Freeze

No existing G1.1 Candidate content, runner, tactical session, scene, tests or `main-g1/**` evidence was modified. Protected tracked diff from `cf49dac` is zero; representative hashes are recorded in `g1-1-freeze-receipt.tsv`.

Direct G1.1 regression reconfirmed:

- frozen source materialization: 18 semantic sources, 7 visual records, exact fingerprint;
- seven-node route and D0-B player confirmation contract;
- CP0-CP3 physical save, Runner destruction/recreation and restore;
- bad fingerprint fail-closed with unchanged save bytes.

## Verification

| Check | Result | Evidence |
|---|---|---|
| Producer frozen contract | PASS | `logs/01-producer-contract.log` |
| G1.5 schema, resolver and fixture scene | PASS | `logs/02-g1-5-asset-shell-test.log` |
| Deterministic 1280x720 capture | PASS | `logs/03-g1-5-capture.log`, `logs/04-evidence-dimensions.log` |
| G1.1 materialization | PASS | `logs/05-g1-1-materialization-readonly.log` |
| G1.1 route, tactical and D0-B contract | PASS | `logs/06-g1-1-contract-regression.log` |
| G1.1 CP0-CP3 persistence | PASS | `logs/07-g1-1-persistence-regression.log`, `checkpoint-restore-receipt.tsv` |
| G1.1 bad fingerprint rejection | PASS | `logs/08-g1-1-bad-fingerprint-regression.log` |
| Existing Godot regression | PASS | `logs/09-existing-godot-regression.log` |
| Canon report / strict | PASS / PASS | `logs/10-canon-report.log`, `logs/11-canon-strict.log` |
| V35 layered pipeline check | PASS | `logs/12-v35-layered-pipeline-check.log` |
| Protected paths, deny literals, staging, whitespace and cache audit | PASS | `logs/13-scope-isolation-audit.log` |

## Isolation

- No change to `project.godot`, default startup, startup router, Autoload, shared Current, shared kernel, Save/Profile or gameplay rules.
- No change to G1.1 run/test scripts or default behavior.
- No art or video resource path is present in the fixture manifest.
- No file under another Session's art or C03 ownership was modified.
- Nothing was staged or committed.

Integration shell ready. Awaiting producer review and an exact approved-asset handoff; no art integration is performed by M1.
