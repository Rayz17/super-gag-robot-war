# FB art-direction log — 2026-10-14 02:39 CST

Agent: Grok Bot executor subagent (Ray Yang / Game仔)
Style lock: KINETIC_CEL (STYLE.md + style-lock refs)

## Hard block

`CallDynamicTool` → namespace `cursor` / tool `GenerateImage` **FAILED**:
> MCP server "cursor" is not available here. HTTP/SSE servers execute on the backend and stdio servers run on Grok Bot's computer; this server is neither reachable nor supported in this context.

`GetDynamicTools` catalog for this session does **not** include `cursor` (only cursor-github, cursor-origin, user-github-local, x, and several needsAuth/error MCPs).

No sanctioned alternate image generator is available to this executor. Did **not** route around via browser/API credentials.

## Reversible work completed

- Read STYLE.md, F.json, B.json, identity-slim.json, inventory.json
- Confirmed B01 already locked at `incoming/dir-B01-refuge-v2-locked.jpg`
- Built priority-ordered prompt pack for all remaining F/B:
  - `_meta/prompts/MANIFEST.json` (51 entries: F01–F18 + B02–B34)
  - `_meta/prompts/{ID}.txt` per asset
  - Each manifest entry has: filename, out_path, aspect_ratio, reference_image_paths, full description
- Updated inventory.json fields: `prompt_pack`, `prompt_status=ready`, `gen_block`, `out_target` (status remains `todo` — no fake drafts)

## Written image files

**None.** Zero `incoming/dir-F*-v1.jpg` / `incoming/dir-B*-v1.jpg` drafts produced (tool hard-blocked before first generate).

## Remaining gaps (all)

### F forms/parts (18) — priority order
F09 brave_core, F10 brave_combined, F11 brave_boots, F12 brave_shoulders,
F01 king_light, F02 king_cannon, F03 king_shield, F04 king_wing, F05 king_drill,
F06 cargo_vehicle, F07 leiling_aircraft, F08 song_aircraft,
F13 hydraulic, F14 repair_tool, F15 tether_tool, F16 barrier_kit, F17 bridge_kit, F18 projectile_kit

### B buildings (33; B01 locked)
Mission-critical first: B12 train-front, B13 train, B07 switchgear, B26 rift, B14 bridge
Then: B02–B06, B08–B11, B15–B25, B27–B34

## Parent action required

Parent (or main agent with `cursor` namespace) must call GenerateImage per MANIFEST entry:

```
namespace: cursor
toolName: GenerateImage
arguments:
  description: <from MANIFEST or _meta/prompts/ID.txt>
  filename: dir-{ID}-{slug}-v1.jpg
  reference_image_paths: <from MANIFEST>
  aspect_ratio: 3:4 (F) or 4:3 (B)
```

Then move/copy outputs to:
`/workspace/grok-delivery/iterations/20261014-full-direction/incoming/dir-{ID}-{slug}-v1.jpg`
and set inventory `status` → `draft`.

## Style self-check (intended; unverified on pixels)

Planned lock for every prompt:
- Cel blocks + pressure ink + ≤2 hard shadows
- Gongwu palette steel teal / concrete beige / warning vermilion
- Buildings = cel industrial architecture (refs include B01 locked)
- King F01–F05 refs include dir-M05-king-v4-locked.jpg
- Brave F09–F12 refs include dir-M04-brave-core-v11.jpg
- Forbidden: photoreal / PBR rust / wasteland / Vek skin

Pixel self-check **cannot** run until images exist.

---

## Update 2026-10-14 02:39 CST — parent steer: pack only

Stopped GenerateImage attempts (cursor namespace unavailable to executors).

### Written
- `_meta/prompts/FB-todo-GenerateImage-pack.json` — **51** ready GenerateImage payloads (schema = M-todo-GenerateImage-pack.json)
  - Keys: id, slug, filename, aspect_ratio, reference_image_paths, description
  - F01–F18 (18) + B02–B34 (33); B01 excluded (already locked)
  - Order: brave F09–F12 → king F01–F05 → alt F06–F08 → tools F13–F18 → mission B12/B13/B07/B26/B14 → remaining B
  - Style: KINETIC_CEL; buildings use B01 + style-lock refs; king/brave F use locked M05/M04 refs
- Per-ID `_meta/prompts/{ID}.txt` and earlier MANIFEST.json remain (longer dumps); **canonical parent consume path = FB-todo-GenerateImage-pack.json**

### Not written
- No `incoming/dir-F*-v1.jpg` / `incoming/dir-B*-v1.jpg` (no fake JPGs)

### Remaining for parent
Call GenerateImage for every pack entry; save to `incoming/{filename}`; then mark inventory draft.
