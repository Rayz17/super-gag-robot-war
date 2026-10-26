# M1a fixture-only loader and consumer evidence

## New slot inventory

The J1 manifest registers 19 slots without importing an old M2 receipt:

- Map: `MAP_BASE`, `MAP_BUILDINGS`, `MAP_ROOFS`, `MAP_FOREGROUND`, sampled-only `MAP_OCCLUSION_MASK`.
- World: swarm, Guardian Z, BREAKER and emergency-vehicle atlases; wall shield; round FX atlas.
- Screen: Jicun, Qihai, Old Guardian and Doudeng atlases; static `GIANT_CONTACT` cut-in.
- Audio: independent UI, world one-shot and ambience-loop channels.

## Exact loader gates

- Exact slot/stable ID/usage/media type.
- Fixture-only user and producer receipt IDs; build, rules profile, asset profile and topology.
- Normalized resource path under `res://tests/fixtures/candidate_runtime_demo/m3_j1/assets` only.
- Denylist, prefix-spoof, traversal and symlink checks before a resource probe.
- Actual SHA-256, decoded PNG dimensions/alpha, declared frame order, pivot and safe-rect bounds.
- Actual WAV RIFF/PCM16 format, sample rate, channels and duration.
- Single-slot hash drift falls back only that slot. An identity-critical fallback always leaves U2 blocked.

## Real Godot consumers

- Map and world media are consumed by `Sprite2D`; frame selections use `AtlasTexture`.
- Portraits and cut-in are consumed by `TextureRect`; loaded textures suppress technical fallback nodes.
- Layer order is `BASE/BUILDINGS -> units/shield/FX -> ROOFS/FOREGROUND`; the mask is sampled and never drawn.
- A4 mapping is fixed at origin `(-880,-170)` with `pixel=(880+(x-y)*40,170+(x+y)*20)`.
- Three independent `AudioStreamPlayer` nodes can play UI, world one-shot and looping ambience concurrently.

The generated PNG/WAV files are deterministic test fixtures. Their captures are deliberately labelled `REAL ART: 0 | U2: BLOCKED`; they are not design proposals or visual acceptance material.
