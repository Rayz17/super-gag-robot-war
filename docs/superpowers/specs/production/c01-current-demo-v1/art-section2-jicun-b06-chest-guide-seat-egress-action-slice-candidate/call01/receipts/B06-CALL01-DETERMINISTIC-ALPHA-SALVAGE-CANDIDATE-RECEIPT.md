# B06 Jicun chest-guide-seat egress — deterministic alpha salvage receipt

## Disposition

- Result: `CANDIDATE_DELIVERY_READY_FOR_USER_VISUAL_REVIEW`.
- Lifecycle: `Candidate / user_visual_acceptance=false / runtime_allowed=false / canon=false`.
- Godot binding: not changed.
- ImageGen calls in this salvage: `0`.
- The original Call 01 RGB hard failure remains preserved as historical evidence.

## B06 source lock

- Source: `game-godot/content/c01_breaker_demo/story_bridges.json`.
- Beat: `B06_JICUN_IS_STILL_INSIDE`.
- Exact line: `有点响，别的没事。`
- Action slot: `JICUN_EXITS_GUARDIAN_CHEST`.
- Existing visual mode: `map_wide_caption`.
- Stage direction: `纪存从馆守Z胸前导览席进入主厅；右臂残片留在封锁广场。`
- No story, Reader, Canon, visual-mode, or runtime file was modified.

## Source and delivery locks

- Raw: `../raw/JICUN_B06_CHEST_GUIDE_SEAT_EGRESS_RAW_CALL01.png`.
- Raw SHA-256: `4ae747191473e7f2a84601f15cc5d061a4c1bd3d807bfbf6029c22358163c493`.
- Raw geometry: `1024x1536`, PNG RGB, `hasAlpha=no`.
- Delivery: `../delivery/JICUN_B06_CHEST_GUIDE_SEAT_EGRESS_RGBA_CANDIDATE_V1.png`.
- Delivery SHA-256: `5cfa39e2d5c0723f972ea758a3c85e90f27ad90b73a8020d1c05d87136a9a569`.
- Delivery geometry: `1024x1536`, 8-bit PNG RGBA, `hasAlpha=yes`.
- Reproducible script: `../technical-salvage-v1/salvage_b06_checker_alpha.py`.
- Selected evidence run: `../technical-salvage-v1/output-v3/`.

## Deterministic method

1. Lock the exact Call 01 source hash before reading pixels.
2. Model only bright near-neutral checker candidates (`chroma <= 8`) and flood
   from the canvas border with 4-connectivity. This is not a global white key.
3. Admit enclosed negative-space components only when area, chroma and the two
   checker-luma phases independently match the border model.
4. Use a 10-pixel trimap and inset high-confidence subject colour donors to
   solve only checker-contaminated edge pixels.
5. Zero RGB only where alpha is zero; decontaminate RGB only in the partial-alpha
   edge band. Every alpha-255 subject pixel retains its source RGB exactly.

## Exact pixel metrics

- Canvas pixels: `1,572,864`.
- Alpha 0: `987,272`.
- Alpha 1–254: `16,861`.
- Alpha 255: `568,731`.
- Subject alpha bounds at every tested threshold: `(98,30)–(941,1514)`.
- RGB changed total: `1,004,133`.
- RGB changed at alpha 0: `987,272`.
- RGB changed at alpha 1–254: `16,861`.
- RGB changed at alpha 255: `0`.
- Unsolved trimap pixels: `0`.

## Threshold and negative-space stability

Three luma floors were evaluated with all other rules fixed:

- L230 versus L235: `2,663` alpha pixels differ; mean absolute drift
  `0.0105756/255`; nonzero p95 `22`; maximum `69`.
- L238 versus L235: `1,957` alpha pixels differ; mean absolute drift
  `0.00685628/255`; nonzero p95 `17.2`; maximum `66`.
- The alpha bounds are identical at L230, L235 and L238.
- Accepted enclosed checker-background pixels are `38,218`, `38,304` and
  `38,172` respectively. The component-count change (`7/8/8`) is a topology
  merge of a tiny hair-side opening at the lower floor, not loss of the three
  large cabin/seat negative spaces.
- Base L235 admits exactly eight enclosed background components. The three large
  ones are `31,080 px` at `205,378–348,824`, `5,048 px` at
  `454,799–500,982`, and `1,830 px` at `220,685–297,855`; five small stable
  openings account for the remainder.

Complete measurements are in `../qa/deterministic-alpha-v1/threshold-stability.tsv`,
`enclosed-components.tsv`, `protected-roi-metrics.tsv`, and
`salvage-report.json`.

## Protected-feature and visual QA

- Face/hair, bracing hand, terminal/other hand, white shirt, and seat frame each
  have `strong_foreground_alpha_zero=0`.
- Opaque RGB changes are zero globally and in every protected ROI.
- The bracing hand, fingers, face, hair silhouette, white shirt, arm terminal,
  and seat-frame edges were visually checked on dark, light, and saturated
  magenta backgrounds at 100% and 50%.
- No checker squares remain in the three large cabin/seat negative spaces.
- No route-pointing gesture, text, map UI, or background was introduced.

Machine/technical result: `PASS_FOR_USER_VISUAL_QA`. This is not user approval,
Runtime approval, Canon approval, or authorization to bind the file in Godot.
