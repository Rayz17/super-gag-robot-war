# C01E02 G2-A.1 Authority Receipt

Status: `candidate_internal_engineering / non-default / fixture-only`

## Frozen authority

| Authority | SHA-256 | Result |
|---|---|---|
| `59-c01e02-a9-g2-producer-correction-and-map-performance-gate.md` | `c5ce47da08a59d3d580806a74149bb55470911e61ddabd4e700c9896ba77e9ae` | exact |
| `61-c01e02-g2-a1-map-performance-consumer-readiness-objective.md` | `aa80b59f58604023fc8d43f54c8f4e0878b0402dcda9b0d3712a7040afae2e62` | exact |
| `38-c01e02-m3-r0-5-production-board.tsv` | `d1dce62260a91ef5e2ae97d2fc10d61ecb5b259d80bb64fd5e25731b8879f103` | exact |

`chao-gag-canon` authority checks were run before implementation. The implementation remains below Canon and Reader authority: no story fact, Reader order, default M2 entry, save/profile, or formal Runtime state was changed.

## Scope lock

Writes are limited to the existing non-default `m3_golden_slice` content/scripts/scene/tests, the dedicated G2-A.1 test script, and `main-g2-a1/**` internal evidence.

Explicitly unchanged:

- `game-godot/project.godot`
- startup router/selector and default M2 Runner
- Canon, Reader, formal save/profile, and Runtime
- A8/A9 and all real or historical art assets
- G2-B

The capture set is `internal_fixture_validation_only`. It is not eligible for user visual review or U2.
