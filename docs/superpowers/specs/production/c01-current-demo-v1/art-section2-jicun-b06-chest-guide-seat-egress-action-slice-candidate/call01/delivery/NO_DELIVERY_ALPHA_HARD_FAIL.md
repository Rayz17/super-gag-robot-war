# No delivery image

Call 01 is ineligible for delivery because its checkerboard backdrop is baked into an RGB PNG (`hasAlpha=no`). The raw result is retained only as failure evidence. It must not be bound in Godot, presented as a transparent Candidate, or used as a source for deterministic background removal.

Lifecycle remains: `Candidate attempt / user=false / runtime=false / canon=false`.

## Later technical-salvage authorization

This file preserves the result of the original ImageGen-call gate. A later,
explicitly scoped instruction authorized a zero-ImageGen deterministic salvage
audit of the same SHA-locked raw. That audit did not make the original RGB raw
deliverable; it produced a separate RGBA Candidate at
`JICUN_B06_CHEST_GUIDE_SEAT_EGRESS_RGBA_CANDIDATE_V1.png`. See
`../receipts/B06-CALL01-DETERMINISTIC-ALPHA-SALVAGE-CANDIDATE-RECEIPT.md`.
