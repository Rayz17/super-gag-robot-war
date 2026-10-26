# Task 75 §5.1 generation log

Status: `INVALID_WIP / VIEWPOINT_PRECONDITION_FAILED / History only / runtime_allowed=false`

Task 76 correction: the source route and zero-redraw process were correctly recorded, but the front/left/back/right cells were wrongly aliased to tactical cardinals. All resulting PNGs and boards are retained only as failure evidence; none is a `map_dimetric_40x20` asset.

## Fixed source route

`V10X e1d6... -> same-sheet Q c701... -> transparent front 330346... / four-direction 3873...`

- The provisional `south` file uses a byte-identical copy of the exact 1024×1024 `330346...` front design master; this filename does not grant south-facing map semantics.
- The exact 2560×960 `3873...` sheet is divided into four fixed cells, without trim or content-aware detection:
  - front/south: `[0,0,640,960]`
  - left/west: `[640,0,1280,960]`
  - back/north: `[1280,0,1920,960]`
  - right/east: `[1920,0,2560,960]`
- Each 640×960 cell is centered in a transparent 960×960 canvas at `(160,0)`. Padding adds no visible pixels.
- Display assets are resized exactly once from the native square canvas to 256×256 with Pillow `LANCZOS`. The 50% review assets are separately resized once from native to 128×128; they are not scaled from the 256 outputs.
- Registration is bottom-center: 256 pivot `(128,243)` and 128 review pivot `(64,121)`. These preserve the source review baselines (`970/1024` for 330346 and `910/960` for 3873).
- The A4 board uses the prior review anchor `(382,434)` and 2×2 footprint only as scale/readability evidence, not event staging or Runtime coordinates.

## Explicit non-actions

- ImageGen 0; Blender 0; SVG 0; Python/Pillow visible-mecha drawing 0.
- No visible-pixel generation, repair, cleanup, despill, recolor, structure correction, frame interpolation or new action pose.
- No BREAKER consumption; no Atlas, Godot, Runtime, UA91, G2-B, exact handoff or Canon migration.

## Risks intentionally retained

- Soft gradients and fine panel lines compress at 50%; dark-blue armor can merge into A4 roofs and road.
- The four views share one sheet/source chain, but they are not a named rig and do not prove exact strict-side/front structural equivalence.
- Existing pixels provide only four cardinal idle views. A first-contact weight pose is absent; transforms and FX may express short movement/flash/recoil, but cannot automatically satisfy Task58's impact requirement.
- Machine source/crop/alpha checks do not grant visual approval.
