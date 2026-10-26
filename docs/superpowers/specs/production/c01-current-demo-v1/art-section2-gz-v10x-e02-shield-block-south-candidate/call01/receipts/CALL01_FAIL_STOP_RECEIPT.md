# GZ V10X E02 shield block south — Call01 fail-stop receipt

> `verdict=FAIL_STOP_TRANSPARENCY`
>
> `candidate_created=false` · `user=false` · `runtime=false` · `default=false` · `canon=false`

## Raw visual audit

| Gate | Result | Evidence |
| --- | --- | --- |
| V10X identity / E02 two complete arms | PASS on raw | compact V10X head, shoulders, colors and two-arm topology remain readable |
| no wings / no backpack | PASS on raw | neither is present |
| Camera V2 south elevated read | PASS on raw | top planes are visible and the front is oriented toward the south screen quadrant |
| A17 exterior faces camera | PASS on raw | front panel rhythm, central spine and three established diagonal scars are visible; rear brace is not shown |
| front-visible-hand-count | `0` on raw | no hand, wrist, or forearm crosses onto the shield exterior |
| rear/interior-hand-contact-count | `NOT_DIRECTLY_VERIFIABLE` | both upper arms lead behind the shield, but the hidden two-handle contacts cannot be directly proven from the exterior image |
| added circular bullet holes | PASS on raw | no new obvious circular ballistic hole; normal rivets remain |
| single subject | PASS on raw | one complete Guardian Z plus one shield |
| transparent RGBA / no checkerboard | **FAIL** | raw is `1254x1254` RGB PNG, `hasAlpha=no`; checkerboard is baked into RGB |

Transparency is an explicit hard gate. Per task instruction, the call stopped immediately: no keying, cutout, RGB repair, 256 resize, pivot placement, map QA, old-pixel patch, second call, or Godot integration was attempted.

The raw may be retained only as failure evidence. It is not a sprite, Candidate master, fallback, or input for later production.
