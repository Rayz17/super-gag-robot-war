# G1 common-turn core evidence

## Implemented

- Player-authored short routes preserve ordered waypoints; adding a waypoint extends rather than replaces the route.
- Final facing is edited independently and never rewrites route points.
- The frozen vehicle, swarm, BREAKER, artillery and road intents carry concrete action, target, trajectory/condition and timeslice data.
- Trigger matching compares the declared frozen event with the prepared reaction; it no longer uses a fixed reaction rectangle.
- Preview and execution call the same pure resolver. Draft editing and summary return write zero world/intent state.
- Commit summary repeats route, route hash, waypoints, endpoint/effective endpoint, facing, main action or trigger-to-response, protected target, fallback risk, contact group and contact time.
- `route_hash` hashes the submitted route points. Mutation count and per-domain settlement counts are derived from the field-level mutation ledger.
- Two successful plans produce different route modes, swarm cells, Guardian load and road outcomes. A third legal plan resolves to an explainable failure.
- Full and Skip projections preserve one semantic result and commit once.
- 20 replays for each of three plans plus reversed entity/object/intent containers are invariant.

## Player-input regression caught

The first UI pass still wrote the obsolete `trigger_id/response_id` shape while the J1 resolver required `reaction_id`. The playable-flow test exposed this even though fixture-based resolver tests passed. The button now writes `LATERAL_LANE_DEFLECT`, and both main-action and prepared paths can enter, leave and re-enter the summary.

## Frozen outcome

Both successful variants stop at `M3_J1_PROTOTYPE_STOP`: BREAKER is alive, first knockdown is false, red charge is only `charging`, shield is `wall_hung_3_scorches`, rescue lane is `active`, mission clear is false, and story checkpoint is false.
