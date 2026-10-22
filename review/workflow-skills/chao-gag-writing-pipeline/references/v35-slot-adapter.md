# V35.4 / V35.7 / V35.8 Slot Contract

Read this for V35 chapter/episode drafting, route work, roster scheduling, C12+ fleet continuity, or final-run validation.

## Source order

1. `V35全剧融合完整大纲底座-v35.2.md`: chapter causality.
2. `V35.3关键剧情决策机战规模与多文化命名-v35.3.md`: fate, roster scale, packages, naming.
3. `V35.4全剧话槽分支与72机生命周期施工图-v35.4.md`: construction contract.
4. Four V35.4 data tables: author slots, route combinations, unit lifecycle slots, decision propagation.
5. For a declared `V357-*` run, add `V35.7全剧槽位回灌与机体IP装载施工图-v35.7.md` and all `v35_7_*` tables. V35.7 is a candidate overlay: 95 author slots, about 80 single-playthrough slots, and 77 candidate playable units from the remapped 72-unit base plus five Starfire vehicles.
6. Before any V357 Pressure Board or Packet, add `V35.8全剧逐槽机体IP玩法装载合同-v35.8.md` and all `v35_8_*` tables. Bind the slot to exactly one `V358LOAD` contract, then resolve its unit manifest, source absorption, gameplay, effective lifecycle gate, assets, and any dynamic selectors. V35.8 completes the loadout input layer; it is not a Pressure Board or synopsis.

## Preflight

Before Pressure Board, resolve:

- `Canon Mode: living_plus_v35_candidate`; this selects the V35 candidate overlay without promoting it.
- `Author Slot ID`, slot mode, and slot-to-episode mapping.
- route window, selected slots, skipped slots, convergence differences, and failure dignity.
- available units and fleet; after C12, cross-fleet deployment needs a reason.
- incoming decision threads and required outgoing deltas.
- skipped-slot world continuation.
- new-unit gate mode: `first_appearance`, `lifecycle_delta`, or `bridge_exception`.
- for V35.7, exact mystery, continuity, and foreshadow binding ids.
- for V35.7, V29 eighteen-chapter crosswalk selection and, for dense slots, high-density manifest ids.
- for V35.7, the exact `V35.8 Loadout Contract ID`; use V35.8 `effective_gate_mode`, not the historical authored gate when they differ.
- resolve every V35.8 dynamic selector against route, fleet, damage, survival, and hidden-state inputs; collective nouns never count as deployed units.

Do not draft prose until these are explicit.

Do not mix `V354-*` and `V357-*` ids in one run. The validator auto-detects the source set from `Author Slot ID`. A full V35.7 run uses the V35.5 C01-C03 episode-level Pressure Boards and 10-slot/11-episode mapping as input, then translates packet and ledger ids through the V35.7 table's `legacy_slot_id`. Those Pressure Boards are not completed thick synopses: the run must start at C01E01 and generate one Packet at a time, then pass C01, C02, C03 chapter reviews and the opening-prefix review before C04. In V35.7, C13's Fangzhou T log and C16's common opening/convergence are mandatory route content; skipped task-pool material must continue as offscreen world state.

The V35.8 loadout is a replace-with-reason contract, not an immutable shopping list. A stronger Pressure Board may replace, move, or downgrade an item, but must record what was preserved, what changed, where the displaced payload goes, and why the scene is stronger. Merely copying source IDs, package names, famous quotes, or “all units support” does not satisfy source absorption.

## Lifecycle gate

`lifecycle_delta` can replace a first appearance only when a returning unit gains a visible new form, weapon, pilot/machine-soul relationship, combination role, political role, fleet transfer, enemy-to-ally state, route lock, or terminal payoff. Ordinary return, recolor, stat increase, or background Cut-in does not qualify.

`bridge_exception` is for a true transition/business-light episode. It needs a reason and next compensation window and cannot be used in consecutive episodes.

## Required ledgers

- `slot_episode_mapping.tsv`
- `route_state.tsv`
- `unit_availability.tsv`
- `decision_propagation.tsv`
- `skipped_slot_world_state.tsv`

Use the templates under `docs/superpowers/specs/data/story/episode_loop_*_template_v35_0.tsv`.

## Validation

V35 completion claims require:

```bash
check_episode_loop_run.py <run> \
  --strict-creative-gates \
  --require-source-absorption \
  --require-v35-slot-contract
```

Without the V35 flag, the run is only a generic Pipeline/ELO run.
