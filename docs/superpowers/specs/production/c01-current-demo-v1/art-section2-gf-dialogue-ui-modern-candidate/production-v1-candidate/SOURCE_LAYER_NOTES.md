# GF Modern Dialogue UI Components｜Editable Source-Layer Notes

Source type: deterministic RGBA reconstruction from the user-approved RGB direction board.

The source is intentionally reproducible through `build_modern_rgba_components.py`; there is no hidden PSD or manually painted replacement layer.

Layers performed by the script:

1. SHA-locked accepted direction board.
2. Degree-4 smooth neutral-backdrop reconstruction from declared empty zones.
3. Per-component polygon support and low-intensity residual rejection.
4. Foreground color recovery from the observed composite.
5. Dialogue-panel top/right/bottom open cuts.
6. Warm-neutral bevel normalization to cool white while retaining the comms safety-orange state.
7. Premultiplied resize, atlas assembly and alpha-zero RGB cleanup.
8. Nine-slice, multi-background, edge and 1280×720 navy-layout QA.

All generated PNGs and machine receipts are reproducible by running the script with the bundled Pillow/NumPy workspace Python runtime.
