---
name: chao-gag-writing-pipeline
description: Use when drafting, revising, expanding, or reviewing 超GAG机器人大战 story outlines, scripts, dialogue, character arcs, chapter synopses, high-density multi-line chapters, mecha/roster story beats, gameplay-story beats, or art/asset-facing story briefs, especially when long outputs risk weakening, losing prior good material, forgetting 50-issue fixes, drifting from canon, or omitting mecha, gameplay, IP homage, relationships, assets, branches, or graph-index updates.
---

# Chao GAG Writing Pipeline

## Purpose

Run a multi-round writer room workflow for 超GAG story work. This skill does not replace `chao-gag-canon`; it uses canon as the fact source, then adds staged drafting, 50-issue diagnosis, review gates, patch merging, and canon/graph backfill.

Use this skill to prevent one-pass output decay: thin later episodes, unstable structure, lost old highlights, missing mecha/gameplay, shallow relationship beats, static protagonist arcs, weak IP homage, and forgotten asset or graph consequences. When the user expects a readable chapter synopsis, use `docs/superpowers/specs/剧情梗概/V22-A5厚度修复整合稿-星火战队与万机同心-v22.10.md` only as a thickness and content-class reference unless a newer accepted thick draft supersedes it. No accepted or user-confirmed draft is a correctness gold standard: Working status raises the rewrite threshold but never disables independent causality, performance, mecha/IP, gameplay, or human-voice review.

## Story-First Reconstruction Override

When an existing run is contract-complete but reads like an administrative summary, ethics report, route fixture, or field-completion memo, read `references/story-first-reconstruction.md` before `references/pipeline.md`. This mode is mandatory for the V35.9 C01-C12 creative reconstruction and for later episodes inheriting that rebuilt state.

In this mode, hard canon and locked dramatic assets are loaded first, but optional source rows, manifests, Scene Binding Matrices, production fields, and ledgers do **not** generate the initial story. The creative order is: single-playthrough causal spine and character/mecha desire; distinct dramatic fingerprint; readable camera/scene chain; player action; relationship/daily/emotional release; then source selection, contract binding, Canon/50-issue/asset/physical-budget validation, and independent review. Existing contracts remain authoritative constraints. If a stale candidate loadout harms the story, file an explicit upstream migration and revalidate rather than writing a weak scene around it.

Required fields remain completion evidence, not creative prompts. A structurally complete packet still fails when its spectacle is only a result sentence, its branch paths are narrated together, its protagonist only suffers or grants permission, its mecha merely prove personhood through refusal/damage, its relationships are isolated motifs, or every victory receives the same immediate ethical invoice.

## Entertainment-First Recovery Sandbox

Use this recovery mode when the user rejects a complete Layer4 batch as unreadable, overburdened by setting, administrative, engineering-heavy, or fundamentally not fun. It exists to test whether the story deserves another formal production pass before rebuilding every board.

1. Invalidate the rejected chapter and all downstream machine stages. Do not patch the rejected outline or continue the next chapter.
2. Select one active chapter, normally the opening chapter. Build a short setting-reduction decision that names:
   - the few facts a first-time player must understand;
   - mysteries that may appear only as images;
   - lore and workflow concepts forbidden from the foreground;
   - the mecha, battle, relationship, comedy, and reward promise.
3. Build one entertainment spine with a strictly rising sequence of character desire, mecha action, reversal, climax, and reward. It may contradict stale Working/Candidate chapter facts, but must list those contradictions as pending migrations.
4. Write one continuous pure-story chapter candidate. Do not include player instructions, production fields, design defenses, mechanism tables, state ledgers, or chapter-end compliance summaries.
5. Run two isolated reviews: one commercial-story first read and one mecha-game/robot-anime review. The lead writer alone performs targeted revisions. Regress the changed blockers once more.
6. Stop for user review. A blind-review pass is not a Layer4 pass and does not unlock L4.5, Reader, the next chapter, or Canon promotion.
7. If the user accepts, migrate conflicting Canon deliberately and rebuild the formal Layer4 chain from `series_alignment`, using the approved story as the creative target. If the user rejects it, continue in the sandbox instead of creating more boards.

The sandbox is deliberately cheaper than the full compiler. It prevents Canon, 50-issue, roster, asset, and workflow fields from being averaged into every chapter. Backstage material enters the story only when it changes the current chapter's desire, battle, relationship, visible mystery, reward, or next causal step.

## High-Density Dramatic Chapter Mode

When several factions, character arcs, IP story projections, mecha groups, gameplay forms, branches, and macro mysteries compete for one chapter-level climax, read `references/high-density-dramatic-chapter-mode.md` before episode drafting. Do not confuse this creative mode with the V35 high-density mecha manifest.

This mode adds a series-alignment and chapter-level dramatic brief above Story-First and the single-episode Pipeline. First derive a compact series-spine slice: inherited threads, this chapter's required answers, material that may only be foreshadowed, future peaks that must remain reserved, outgoing state, and any explicit outline migration. Then establish the chapter engines, energy wave, escalation boundary, minimal causality board, inherited-highlight functions, representative route, and persistent branch differences. Keep the one-episode-per-invocation contract and make every episode read the same short chapter brief.

Assign one lead-writer responsibility for Reader prose and final integration. Independent reviewers diagnose evidence, root cause, and the scene that must change; they do not co-author patches into the Reader. Rewrite a whole scene when motive, causality, control, relationship turn, IP emotional premise, battle purpose, or branch result changes. Use local patches only for genuinely local defects.

HDCM is qualitative. It must not become another quota table or chapter encyclopedia. A chapter passes when its accumulated drama, character/mecha choices, recognizable story-level IP projection, play experience, branch causality, and climax work as one continuous story.

## Story Runtime v3 Knowledge and Character Gate

For new story creation, structural rewriting, chapter selection, or any run
whose earlier Runtime pass produced technically complete but lifeless prose,
read `references/story-runtime-v3.md` before compiling writer context.

Runtime v3 is the default creative route. It treats Canon, L1-L6, character
models, mecha lifecycles and material pools as a queryable knowledge base, not
as a one-shot plot contract. The Pipeline must call the Runtime repeatedly at
the decision that needs it:

```text
ideation
-> choose/fuse one dramatic direction
-> research admission
-> admit only the needed L4/L4.5 migration references
-> entity and character modeling
-> scene planning and causality
-> draft with explicit active cast
-> independent review
-> user-confirmed writeback
```

Each phase pack generates `06-writer-view.md`. The active writer reads that
decision view by default. Full slices, TSVs, traces and conflict tables are for
auditing or targeted follow-up queries and must not all be appended to the
writer prompt.

The `ideation` pack may contain only the relevant L1 experience promise, L2
total engine, L3 chapter responsibility and future reservations, the previous
chapter's confirmed exit, a legal cast index, and a mecha/opposition index. It
must not prewrite the climax, action chain, final dialogue, scene exits, or the
answer the writer is supposed to discover. The lead writer can reject Working
chapter beats or inherited highlights by filing an explicit migration.

L4, L4.5 and L5 sources are resolved through
`story-runtime/production/chapter_layer_source_registry_v3.tsv`, never by
globbing a similarly named directory. Ideation sees no old chapter answer.
After selection, the Pipeline first shows the eligible source index and admits
only named `admitted_layer_source_ids`. L6 is currently empty and must not be
invented upstream.

After one proposal is selected, compile a separate `research` pack around that
proposal's actual questions. IP, famous-scene, relationship, comedy, model-kit
ecology and what-if pools are optional materials. Retrieval does not imply
admission.

Before causal planning, compile an `entity_model` pack for only the selected
characters, mecha, opponents, places and key objects. Important recurring
characters reuse the stable character registry and generated model facets:
formative past, desire, fear, contradiction, pressure behavior, intimacy
behavior, voice, relationships, ability boundaries, knowledge, ownership,
current arc and first-appearance state. Local NPCs receive lightweight scene
cards. Do not rebuild major characters from scratch for each episode.

The sparse scene-presence layer distinguishes physical presence, live remote
presence, recording, work trace, linked machine-soul presence and absence. A
character who matters to a chapter is not therefore physically onsite. First
appearance, arrival, control, knowledge and exit must all be visible or
explicitly open for the writer to solve.

The character/entity gate fails when:

- a character acts before their formal appearance or appears without travel;
- a work trace, recording, remote feed or machine-soul link is written as a
  physical person;
- someone silently acquires a mecha, tool, authority, knowledge or ability;
- a recurring character lacks a stable model and is improvised from function;
- a new named entity has no reason existing cast cannot serve, no lifecycle,
  no exit, or no reusable production value;
- the Pipeline silently overwrites a Working fact instead of proposing a
  migration.

After modeling, compile `scene_plan` context for position, scale, control,
knowledge, object continuity, simple alternatives, state exits and player-
visible evidence. Only then may the scene writer receive a `draft` pack. The
draft pack contains the selected scene chain, compact causality, explicit
active cast, positive voice material, admitted creative materials and the
previous scene exit. It excludes full Canon, production contracts, negative
phrase examples, old Readers, review reports and inactive cast dossiers.

For long episodes, first pass an opening or one complete-scene fuse. If plain
causality, spatial reality, character voice or entertainment fails, stop there.
Once it passes, the same lead writer may use v2.2 interaction transactions to
write later scenes in order, each inheriting the committed exit state and only
the necessary prose tail.

Independent `review_scope=cold_reader` context must not include author intent,
L4/L4.5, backstage answers or an old same-chapter Reader. A cold reader first
paraphrases what the prose actually communicated. Logic and mecha reviewers
use a separate `review_scope=design` pack. Old-draft comparison uses
`review_scope=benchmark` only after cold review is sealed. Only user-confirmed
prose can enter `writeback` and update Canon, character state, relationships,
mecha lifecycle, scene presence or graph indices.

Workspace entry points:

```bash
python3 scripts/build_story_runtime_character_models.py
python3 scripts/check_story_knowledge_base.py
python3 scripts/compile_story_runtime_stage_context.py --help
```

## Story Runtime Harness v2.2 (Legacy Interaction Runtime)

Use `references/story-runtime-harness-v2.md` only after a story direction,
entity model and scene plan have passed Runtime v3, when an already designed
long episode needs interaction-level cache, transaction and receipt handling.
Do not use v2.2 chapter contracts to invent a new story from zero. Do not send
raw Canon, support tables, retrieval packs, old Readers and all reviews to the
writer.

Apply the workspace production policy before every draft. Current facts may be
compiled into short scene-specific cards. Candidate Support and creative
materials are hidden by default and enter the writer context only after the
lead writer has chosen the scene direction and explicitly admitted record IDs.
History, old Readers, effect tests, negative phrase examples and review reports
are backstage or postwrite evidence only. Prose follows the `draft` mode of
`chao-gag-story-writer` and its Runtime v3 draft pack. Creative First v2 and the
earlier stable-kernel v1 remain only as method history and regression evidence;
they are not default prompts for new prose.

The Pipeline still owns exactly one episode per invocation, but it must not
assume that one episode equals one model interaction. Before prose, estimate
stable creative capacity and split a dense episode into complete dramatic
scenes or battle phases. Compile those transactions with the interaction-level
Runtime, then let one lead writer write, locally review and commit them in
dependency order. Each successor reads the committed exit state and only the
necessary prose tail. Multiple agents may plan or review, but they must not
parallel-write scene fragments for later prose assembly.

All interaction contexts are content-addressed caches. The complete interaction
toolchain/schema and Current/Support corpus hashes participate in invalidation. Upstream scene
changes invalidate descendants and the whole-episode assembly. Only
`contexts/` may be pruned; drafts, receipts, reviews, episode seals and history
are evidence.

When prior drafts have lost mecha, renamed entities, broken next-chapter
handoffs, flattened core characters, or created disposable named entities,
return first to Runtime v3 `ideation` or `entity_model`. v2.2 may be used only
after that root cause has been corrected and a scene plan is ready for serial
production. Contracts are shared interfaces for writers, deterministic gates,
reviewers and state backfill; they are not creative instructions.

## Chapter Creative Compiler and Human-Voice Gate

For chapter engines, complete chapter outlines, high-density chapters, new abilities, multi-scale battles, transformations, or any draft that has repeatedly created concepts and actions while expanding prose, read `references/chapter-preproduction-and-human-voice.md`.

The required order is:

1. verify the generated six-layer production dashboard and select only its current active chapter;
2. run that chapter manifest's `--next` and `--before-stage` gates;
3. compile the Runtime v3 `ideation` pack from L1/L2/L3, the predecessor exit, legal cast and mecha/opposition indices;
4. have one lead story architect produce three plain-language dramatic options and select or functionally fuse one;
5. compile `research` context for the selected option and admit only materials that strengthen its existing cause;
6. compile `entity_model` context and pass the character/entity gate before deciding detailed actions;
7. compile `scene_plan` context, then lock the chapter engine, human/mecha desires, causal spine and outgoing-state boundary;
8. prepare the director board, player-visible evidence plan and battle/gameplay preplan;
9. write and review the complete chapter outline;
10. give the readable outline, without its design-defense boards, to an independent first-read causality audit and repair any root cause before continuing;
11. complete and seal the episode structure table, state ledger, Layer4 four-view review, and cumulative continuity receipt;
12. write and review the chapter performance-carrier plan;
13. pass the exact episode stage gate before drafting exactly one Episode Reader;
14. compile the episode/scene `draft` pack, pass the opening or first-scene fuse, then convert key scenes into performance before polishing dialogue;
15. assemble the chapter Reader, then give only that Reader and the previous chapter ending to an independent time-space and physical-causality audit; the auditor may not read backstage boards to repair the story mentally;
16. after that audit passes, run independent semantic human-voice review, deterministic lint, and chapter review;
17. stop for explicit user creative acceptance; only its dedicated receipt may unlock later chapters;
18. run Runtime v3 `writeback` only after acceptance, then update state and graph sources;
19. route failures back to the earliest layer that owns them and invalidate all dependent downstream stages.

For V35 chapter production, first run `python3 scripts/report_v35_layered_pipeline.py --check` and read `V35六层创作生产看板.md`. The six creative layers are L1 experience charter, L2 total engine, L3 series structure master, L4 complete chapter outlines, L5 Episode/chapter Readers, and L6 script/production. World mechanisms, Canon, roster/IP, material pools, and the 50 issues are horizontal support; the chapter performance-carrier plan is the mandatory L4.5 interface.

`docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/Cxx-story-chain.tsv` is mandatory from the start of the active chapter. Run `scripts/check_v35_story_chain.py --next` before all work and the exact `--before-stage` gate before writing an artifact. Only `passed` and `generated` stages with matching SHA-256 unlock downstream work. Existing files, Working story facts, prior user acceptance, and C01-C03 status are not exemptions. If an upstream artifact changes, use `--invalidate-stage`; never hand-edit a passed state. If any gate fails, label existing downstream prose `invalidated_downstream_artifact` and return to the earliest missing stage.

Chapter Reader assembly must consume only the Episode paths declared in that manifest, in `stage_order`, with their current hashes. Never glob an Episode directory: superseded drafts may remain there as evidence but cannot enter the Reader. For C02 and later, sealing `series_alignment` normally binds a fingerprint of the predecessor's current chapter Reader, state ledger, and explicit user-acceptance receipt. Any later change to those three inputs makes the sealed alignment stale and blocks downstream work until it is invalidated and resealed. When the user explicitly authorizes repair of an already existing chapter range, create a bounded repair-authority file listing `Authorized-Chapters` and `Does-Not-Grant-User-Acceptance: true`, then seal each affected `series_alignment` with `--repair-batch-authority`. In that mode the fingerprint uses the predecessor Reader, state ledger, internal chapter review, and authority hash; it never marks acceptance passed and cannot unlock chapters outside the listed range.

Read the current episode ceiling from the L3 row of `V35-upper-layer-registry.tsv`; never hard-code it in prompts, scripts, or prose. It is an upper bound, not a quota. If Layer4 changes a chapter's real episode count, invalidate `first_read_causal_audit` and all later stages, then use `scripts/resize_v35_story_chain.py` with a registered migration document and reason. Do not hand-edit the registry or add or remove Reader files. Raising the total above the current ceiling requires the same transaction to migrate L3 with `--new-ceiling`.

Each chapter must declare one production profile in `V35-chapter-registry.tsv`. `light` reuses established entities, spaces, abilities, and controls and may fold compact preproduction into the standard artifacts; `standard` introduces one significant new place, ability, enemy rule, or control chain; `heavy` contains multi-scale, transformation, machine-soul crossover, major new ability, three-way battle, or spatially decisive spectacle and requires the physical board and low-fidelity previs. Profiles change evidence depth, never the stage order or user-acceptance gate.

`chapter_review` is an internal production pass, not permission to continue. The next new chapter remains locked until `scripts/record_v35_user_acceptance.py` records the user's explicit approval. A user-authorized repair batch may internally rebuild later chapters already inside its declared range, but every repaired chapter still stops at its own acceptance gate. Batch or autonomous runs may not impersonate acceptance, infer it from silence, reuse an old acceptance for a changed hash, or use repair authority to begin a new chapter.

Writing may introduce a genuinely better idea, but it must pause and amend the preproduction model before the new entity, space, power, or action enters the authoritative draft. Do not repair a control problem with dialogue, a spatial problem with a new device name, a motivation problem with narrator explanation, or an unnatural voice with more lore.

Apply available-tool and object-state conservation across episodes. A vehicle, crane, winch, access route, weapon, operator, control seat, or rescue device that remains powered, connected, reachable, and capable at the end of one scene is still a valid solution in the next; a riskier method is not causally earned until the Reader visibly destroys, depowers, disconnects, blocks, reassigns, outruns, or exceeds the simpler option. Likewise, “return”, “reinstall”, “recover”, or a renamed rescue asset requires a visible prior departure and one continuous object identity. Register these states in preproduction and test them again in both causal audits.

Before any Boss battle, faction rupture, forced sacrifice, or major accident, run a conflict non-parallel test. Explicitly try the competent alternatives: do both objectives at once, hand the disputed object or person to a neutral custodian, stop or disarm first, cut the remote line, wait for independent confirmation, retreat and pursue later, or use an available vehicle/crew/tool while the larger operation continues. “Time is short”, “they disagree about order”, and “someone blocks the route” are not enough by themselves. If a simpler peaceful action remains feasible under the current control rights, physical state, and time window, use it or redesign the conflict around a genuinely incompatible subject state, custody claim, survival risk, or irreversible objective. The outline and Reader causal receipts must state both the rejected simple solution and the visible fact that rules it out.

Track every cross-episode clue through an explicit reveal lifecycle: `emitted -> observed -> isolated/localized -> interpreted -> verified -> revised`. An episode may advance one or more stages, but adjacent episodes may not both claim the same clue was first discovered, restored, decoded, or confirmed. The director board owns the current stage; Episode Reader prose must use the corresponding verb. Open-information cards may summarize the achieved stage but cannot advance it.

The foreground information budget is qualitative: backstage may distinguish many systems, but one scene should normally require the player to understand one decisive control or causal change. A preproduction table can pass while the Reader still fails. Deterministic anti-AI lint can provide evidence; only semantic performance review can judge whether characters sound alive, distinct, listener-aware, and motivated.

The post-assembly `reader_causal_audit` is distinct from the Layer4 `first_read_causal_audit`. The first checks whether the complete outline's engine works before episode production. The second catches contradictions introduced while writing performance and prose. It must read the chapter Reader as an ordinary player would, plus the previous chapter ending or the current cumulative Reader, and test chronological order, travel time, location and scale, loads and reach, people/mecha position and control, evidence provenance, fail-safe behavior, and the simplest competent alternative. Before the audit, run the cross-chapter risk scanner. `FIRST_SCOPE`, `RELATIVE_TIME`, `ORPHAN_EVIDENCE`, `OBJECT_RETURN`, and `SPACE_TRANSITION` are auditable candidates, not banned words. The sealed receipt must declare `Audit-Scope: reader_causal_full`, exact `Reader-SHA256`, `Prefix-SHA256`, `Risk-Scan-SHA256`, `Result: PASS`, `Open-P0: 0`, and `Open-Blocking-P1: 0`; a receipt from an older Reader or partial scan cannot pass. A scene fails when it works only because the auditor imports an answer from the physical board, open-information card, or author note. Repair the earliest owning Layer4/L4.5/Episode source and regenerate; never patch a generated chapter or cumulative Reader.

For V35 chapter production, every Layer4 director board must include the per-episode reveal matrix defined in `docs/superpowers/specs/2026-07-26-chao-gag-current-open-information-system-v1.md`: what the player must understand, may suspect, must not yet know, candidate `万机馆｜本次开放资料` cards, evidence source, epistemic status, confidence, future correction window, and minimum asset. Cards are optional per episode and may summarize only knowledge already earned in story. If the next scene needs the card to make its causality intelligible, return to the director board; never use the card as a repair patch. Canon stores backend truth, not provisional player belief.

Keep disclosure cards inline in episode Readers, but fold them by default in mechanically assembled multi-chapter Readers so reference material does not repeatedly reset story momentum. Cross-chapter review must verify that every forecast destination, promised arrival, and support registration matches the later physical route. When a previously anonymous group receives names, rerun pronoun and role-reference checks and let emotionally important members be addressed by name again after introduction; naming only a roster line does not make a person present.

For V26 and later work, treat `docs/superpowers/specs/剧情梗概/V26-C01-C03锚点强化补丁-机体名场面关系-v26.2.md` as a writing-method correction, not only a patch to C01-C03. Its gates apply to future episode drafting unless a newer accepted gate supersedes it.

For V29 and later work, treat "interesting to read and play" as a first-class gate, not a final polish note. A packet can have complete fields and still fail if it feels like a clever design memo instead of a playable robot-anime episode. Each key episode must answer: why would a player keep playing, what PV-grade mecha image could sell the episode, which relationship event would be remembered, what larger G.A.G./Index/Far Star shadow is felt, and how the episode turns an abstract issue into bodies, machines, maps, loss, desire, or victory.

For V29 and later mecha/IP density, use a candidate-pool model, not a fixed episode roster. `v29_roster_bible_reserve_backfill_pool_v0_1.tsv` is the priority backfill pool for roster-package-class units from the roster Bible and reserve list: main units, rivals, successors, hidden units, and representative support units with IP/story motifs, iconic scene mappings, quote anchors, and gameplay payloads. `v29_roster_ip_first_appearance_candidate_pool_v0_1.tsv` remains selectable material for functional modules, rule units, scene-mecha, enemy modules, and supplemental candidates; it does not decide which unit appears in which episode. Each episode must choose at least one, normally two, actual first-appearance IP-mapped mecha/unit/enemy module/scene-mecha from the backfill pool, candidate pool, or a recorded chapter patch according to the episode's drama, map, gameplay, relationship pressure, and enemy learning chain. Except for bridge/business-light episodes, at least one first appearance should prioritize a roster-package-class backfill candidate. Record actual first appearances in the run ledger. Returning units and routine support returns go under `repeat_returns_not_counted`, never under first appearances.

For V35 and later deep-material selection, use `docs/superpowers/specs/research/2026-07-11-chao-gag-material-pack-depth-backfill-v1.md` and the `docs/superpowers/specs/data/research/*_v1.tsv` deep pools as a candidate research layer. These pools provide non-uniform IP dossiers, battle setpieces, relationship scenes, G.A.G./shipboard comedy, industry/faction ecology, cosmic-SF rules, branch patterns, hybrid-play activities, mecha visual/mechanical grammar, and museum reality checks. Do not load all pools or fill quotas mechanically. First define the episode's character desire, battlefield deadlock, and irreversible state change; then select only rows that materially help. Every selected row must be named in the Episode Input Manifest, bound to a concrete scene, visible in readable prose and production split/state deltas, and recorded in `source_absorption.tsv`. A row id in a field without a new action, reversal, image, relationship consequence, gameplay rule, or state change is not absorbed. The research layer is candidate fuel: it cannot lock episode rosters, promote V35, or override canon and package UID crosswalks.

For V31 and later branch/hidden/SRW-like IF drafting, use the roster what-if regret pool before inventing a route split or saved-tragedy beat. `roster_what_if_regret_pool_v0_1.tsv` records original-work regret anchors, IF repair questions, originalization payloads, trigger conditions, failure dignity, arc windows, and avoid boundaries for core roster packages, hidden packages, strong candidates, and NPC/encyclopedia/enemy ace packages. `roster_what_if_source_refs_v0_1.tsv` records local and external source anchors. This is an internal design layer: public prose must be original, and direct IP copying is forbidden. A branch or hidden unlock should feel like a robot-anime/SRW what-if the player earned through play, not a menu ideology choice. If the episode misses the hidden condition, the failure state must still have dignity: residual support, a log, an object, a scar, a later say得 window, or a different but meaningful route. Do not force every IP package to have the same number of tragedy beats: strong, widely recognized, emotionally dense IP anchors may have many candidates, while lighter or less tragic packages may skip regret material and instead carry spectacle, comedy, gameplay, or ecology. Treat the pool as selectable fuel, not an equal-rows quota.

For reality-resonance tears, use the real-world testimony pool instead of relying on chat memory. `real_world_resonance_cases_v0_1.tsv` records direct public cases and fictionalized motifs such as RWR001, the mother continuing model-parts orders after her son 千寺狐/牛牛 passed away. Use this layer for model street, prototype workshop, real machines, late replies, Far Star echoes, and finale opening testimony. Direct public-case homage must record source, usage mode, concrete object, sensitivity boundary, and publication authorization/credit review. It deepens life texture; it must not replace mecha/IP density, gameplay, protagonist growth, original character action, or become cheap tragedy.

For top-level meaning, use the robot-culture value-axis pool instead of adding a final slogan. `robot_culture_value_axes_v0_1.tsv` breaks the theme into rough-translation coexistence, love-with-responsibility, respect for nonhuman things, anti-single-correct-template, small-object civilization scale, and non-unison civilization language. Use this layer for Far Star, Index, opening-right war, real-world testimony, finale, and episode experience promises. A selected axis must become scene payload, gameplay payload, character choice, mecha action, enemy misuse, and future debt; skipping it is allowed when recorded, but key episodes cannot pass by merely stating that robot culture deserves recognition.

For V31 and later drafts, apply the common-sense stakes / word-weight gate. Read `docs/superpowers/specs/2026-07-05-chao-gag-common-sense-stakes-and-word-weight-gate-v1.md` when an episode uses testimony, opening, authorization, debt, naming, labels, records, public display, or museum/legal workflow terms. The gate asks whether the visible event is large enough for the term. A packet fails creatively if players would describe the beat as "they changed a label / logged a record / adjusted a permission" while the prose calls it 夺名, 证词, 开馆债, 开馆权, or a fate-level public choice. Big terms must follow visible consequences: mecha state change, map change, injury, money loss, shame, relationship break, route closure, enemy gain, public punishment, G.A.G./Index/Far Star fallout, or terminal voice change.

For C01, Wanji origin, naming/renaming, archive-terminal, low-power-response, Daige-clearance, or carrier-transformation work, apply the Wanji origin/authority/binding-layer setting gate. Read `docs/superpowers/specs/2026-07-06-chao-gag-wanji-origin-authority-binding-layer-v1.md`. Wanji's power comes from post-G.A.G. neutral preservation, public trust custody, offline collection binding, and dormant carrier systems; Daige's power comes from modern compliance, risk id, public registry, logistics, safety, ticketing, insurance, and external authorization overlays. Do not write "a label changed, so the robot forgot itself." Show real consequences: doors, fire routes, support buttons, maintenance orders, search entries, logistics, low-power wake filters, or battle recognition fail.

For Wanji carrier action, G.A.G. emergency rescue, body runaway, section-shift battles, or Wanjidian transformation work, apply the Wanji body-mode gate. Read `docs/superpowers/specs/2026-07-07-chao-gag-wanji-body-runaway-and-variable-fortress-v1.md`, `docs/superpowers/specs/data/story/wanji_body_mode_spine_v0_1.tsv`, and `docs/superpowers/specs/data/story/wanji_body_runaway_debt_rules_v0_1.tsv`. G.A.G. runaway is engine pressure; Wanji body runaway is visible carrier-body action; Jicun machine-soul abnormality is the protagonist/body-cost layer. A packet fails if it only says the system glows red, grants free buffs, or transforms harmlessly. It must show story prelude pressure, in-battle trigger with map/rule change, post-battle debt settlement, trigger conditions, giant body motion, player benefits, at least three visible debts, character limit/backlash, enemy/public cost, Jicun abnormal symptoms when involved, and a later read window.

For protagonist arcs, apply the protagonist crucible hard gate: 纪存、七海、白鸢 and other core party members must not remain merely "in character". Key episodes and every chapter review must show major decisions, setbacks, irreversible costs, relationship fallout, and a changed capacity or limitation. Growth can be emotional, political, tactical, relational, or system-facing, but it must alter state: permissions, routes, support skills, command authority, public responsibility, mecha unlocks, trust, or enemy learning. Tiny metrics such as seconds, half-grid movements, labels, saves, or one-turn favors cannot be the whole drama; they only pass when they expose a larger ordeal, collapse, vow, forbidden power, sacrifice, or comeback.

For V31 and later daily-life, shipboard, cooldown, aftercare, lowbrow robot-anime comedy, Qihai onsite, Baiyuan adult-storyboard, or relationship-accumulation drafting, use the daily-life character-tone layer. Read `docs/superpowers/specs/2026-07-07-chao-gag-daily-life-character-tone-layer-v1.md` and `docs/superpowers/specs/data/story/daily_life_character_scene_pool_v0_1.tsv`. A daily scene passes only when it changes character feeling or relationship/support/permission/gameplay state, and when it preserves at least one ordinary object that is not immediately converted into testimony, debt, enemy sample, or world key. Daily warmth cannot replace mecha/IP density, battle/gameplay hooks, or mainline crisis. Adult-edge material must stay with adult/adult-coded characters; child/youth lines are completely isolated.

For V31 and later thick synopsis, script, gameplay-facing outline, or accepted-packet revision, use the episode production layer split. Read `docs/superpowers/specs/2026-07-07-chao-gag-episode-production-layer-split-v1.md` and `docs/superpowers/specs/data/story/episode_production_layer_split_schema_v0_1.tsv`. A packet must keep two layers separate: readable story first, then production split. The split must identify ADV story, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, and settlement/state deltas. Unused layers need skip reasons. The gate fails if battle, triggers, daily relationship scenes, or state changes exist only as blended prose and cannot be handed to art, gameplay, scripting, or asset sessions.

For V31 and later mid-late/finale drafting, apply the finale sacrifice grammar gate. Read `docs/superpowers/specs/2026-07-06-chao-gag-finale-sacrifice-chorus-grammar-v1.md`, `docs/superpowers/specs/data/story/finale_sacrifice_grammar_v0_1.tsv`, and `docs/superpowers/specs/data/story/relationship_sacrifice_cross_recognition_v0_1.tsv` before C09-C15, Qihai/Baiyuan/Jicun sacrifice beats, future failure reports, Matrix-like false opening, Far Star judgement, Index clean-noise pressure, star-consensus greeting, double-stay/quasi-harem route, or Jicun projection/return. This gate stores grammar and eligibility only: do not pre-script final deaths or romances. Sacrifice must protect the team/world and emotionally recognize or complete another person; if it only completes the sacrificer's role, the beat fails.

For V30 and later opening/thick runs, use the strict creative gate. A packet can pass canon, structure, subagent, and gameplay checks and still fail if it repeats a consumed famous quote, counts anchors or rule modules as new playable/IP units, lacks recognizable IP scene projection, has no burn/tear/gag payload, shrinks 纪存/七海 into small arrangements, underplays a climax such as Wanji carrier transformation, or fails to show Wanji Museum's "ten thousand machines" breadth. These are blockers, not polish notes.

For V31.4 and later Notion/Fable use, treat Fable as a fixed post-local-review diagnosis and polish pass, not as the source-of-truth drafting engine. The local episode packet must first pass the Codex pipeline gates for canon, mecha/IP, gameplay, relationships, production split, and ledgers. Then create one episode-scoped Fable Review Pack and ask Fable only for reader diagnosis, dialogue naturalization, relationship heat, burn/tear/gag check, and local polish suggestions. Codex must merge or reject each suggestion locally. If the Notion/Fable GUI fails, mark `fable_failed_technical` in the run ledger and continue with a local dialogue/relationship/readability review; do not call the episode Fable-reviewed, but do not block the whole ELO on Notion UI.

For V34 and later flow repair, apply the source absorption gate. A packet must prove that selected canon rows, mother-draft highlights, accepted patches, 50-issue fixes, mecha/IP rows, quote/scene anchors, branch/what-if rows, sacrifice grammar, relationship material, daily-life hooks, value axes, Wanji body modes, production split requirements, enemy gains, and protagonist-memory beats were not merely listed. Each selected source must be recorded in an Episode Input Manifest, bound to a concrete readable scene in a Scene Binding Matrix, visible in the readable draft, visible in production split or state deltas, and written to `source_absorption.tsv`. Field-only use is failure.

For V35 drafting, also apply the V35 slot contract before source absorption. Resolve the author slot, slot-to-episode mapping, route selected/skipped state, available fleet, lifecycle events, incoming decision threads, and skipped-slot world continuation before writing the Pressure Board. Read `references/v35-slot-adapter.md`. A `V354-*` run uses the 82-slot/72-unit V35.4 source set; a declared `V357-*` run uses the 95-slot V35.7 architecture plus the V35.8 per-slot loadout layer: 72-unit remap plus five Starfire vehicles, exact mystery/continuity/foreshadow bindings, eighteen-chapter V29 crosswalk, unit/action manifest, source absorption, gameplay, effective lifecycle gate, assets, dynamic selectors, route-candidate maps, exhaustive route fixtures, and high-density mecha manifest where applicable. Never mix the prefixes in one run or promote either candidate overlay by implication. V35 completion claims require `check_episode_loop_run.py --require-v35-slot-contract`; otherwise the run is only generic Pipeline/ELO work.

For the first full `V357-*` run, start at C01E01. V35.5 supplies eleven episode-level Pressure Boards for C01-C03, not completed thick synopses or packets. Translate their legacy V354 slot ids through the V35.7 `legacy_slot_id`, write one episode at a time, review C01/C02/C03 at chapter boundaries, then run the C01-C03 opening-prefix review. Do not start C04 until those gates pass.

When the requested deliverable is the full-series V357 Pressure Board layer rather than thick Episode Packets, use `docs/superpowers/specs/2026-07-14-chao-gag-v35-pressure-board-production-loop-v2.md` and the unique state page `docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md`; V1 is only historical evidence for the C01-C12 production run. Produce one independent board per author slot (or more when a slot is explicitly split), bind the semantically locked V35.8 layer, run targeted single-board review, then strict chapter and C01-to-current prefix review. Record `contract_status`, `story_status`, `audience_status`, and `production_status` separately: machine closure, path counts, field completeness, and length never prove audience appeal. Before chapter or prefix creative PASS, generate a reader assembly without engineering fields, obtain independent writer/mecha-culture/game-production/relationship-emotion receipts, and record dramatic fingerprints, player-visible branch deltas, debt lifecycle, energy wave, antagonist intent, and reveal cadence. The readable scene layer may foreground only three to five active state changes per episode; other state remains in ledgers or production appendices. Every major mecha must possess a positive desire such as winning, transforming, combining, protecting pride, challenging a rival, returning to the stage, or choosing a pilot, rather than proving personhood only through refusal, malfunction, or defeat. Major opposition must retain a recognizable recurring body, voice, scar, machine, or operator chain across episodes, and every chapter gate must test whether the dramatic solution grammar repeats an earlier one. Empty or failed reviewer calls do not consume the three-round root-cause cap. Split A/B boards share one Author Slot and Loadout and must not duplicate first appearances, settlement, or final Episode count. Three chapters are a cold-start checkpoint, never a batch drafting unit. V35.8 is Candidate Canon: a better story may submit an explicit upstream migration request and revalidation instead of writing around a stale loadout. Do not reopen formal Episode production until all 95 author slots pass chapter, prefix, creative-evidence, and full-series gates.

For diegetic meta, outside-observer, terminal intrusion, Index UI takeover, version-profile, perfect-build, cross-run memory, second-playthrough, fake-delete, external-archive, or asynchronous-player-echo work, read `docs/superpowers/specs/2026-07-11-chao-gag-diegetic-meta-outside-observer-layer-v1.md` and its five story tables plus `docs/superpowers/specs/data/gameplay/meta_runtime_architecture_contract_v0_1.tsv`. Human characters cannot directly know that they are in a game or say player/chapter/plot/save-load language. Every meta event must identify the world-internal carrier, what the player sees, what each character can infer, the underlying truth, the mecha/map/relationship/route/enemy state consequence, the recovery path, cross-run read/write behavior, and safety/offline/accessibility fallback. The outside observer is not a god or character owner. Meta is a carrier, not a substitute for robot battles, character decisions, or plot. Exact V35 slots remain unresolved until the slot Pressure Board adopts them.

## Required Companion

Before doing project story work, load `chao-gag-canon` if available and follow its canon query and migration rules. If it is unavailable in the tool list, read `/Users/rayz/.codex/skills/chao-gag-canon/SKILL.md` directly.

## Non-Negotiable Run Contract

For V28 and later thick synopsis work, treat the following as hard stops, not advice:

- The source of truth is one episode packet per episode. A chapter file is only an assembly artifact after all episode packets pass.
- A core pipeline invocation may draft, review, patch, and gate exactly one episode. If multiple episodes are written together, label the result as a route map or failed run.
- A full-game or chapter run must keep `episodes/`, `chapters/`, `reviews/`, and `ledgers/` directories. Do not claim an ELO run if those artifacts do not exist.
- A chapter cannot be marked passed without a prefix regression review file. If the review opens a regression ticket, the replay log must show K+1..N before advancing.
- Review intensity is tiered. Default multi-episode drafting uses **Standard Episode Loop** per episode and **Strict Chapter Gate** after a chapter is complete. Do not run a 17-seat strict writer room for every normal episode unless the user explicitly requests strict per-episode review, the episode is a key climax/opening/relationship rupture, or a validator/regression demands it.
- In Standard Episode Loop, keep reviewer mode honest: use `Reviewer Mode: single-context standard` or `Reviewer Mode: targeted subagent standard`, run the hard local gates, optionally call only the needed baseline subagents, and record concise findings. Do not claim `strict writer-room` or use `--strict-writer-room`.
- If subagent tools are available and the user has authorized a writer room or subagents for the run, Standard Episode Loop may use only targeted independent subagents for the uncertain review surfaces and record those ids. Strict writer-room mode must use independent subagents for all strict seats. If subagents are unavailable, mark `Reviewer Mode: single-context fallback` and do not claim "subagent-reviewed".
- For strict writer-room runs, three shared advisory subagents are not enough. They may supply canon/material, mecha/IP, or protagonist/relationship context, but each episode still needs fresh role findings for the full strict seats in `references/writer-room-subagents.md`: showrunner, 50_issue, mecha_ip, gameplay, character_dialogue, relationship, protagonist, jicun_memory, quote_scene, spectacle_emotion, robot_anime_pv, commercial_opening, macro_mystery, player_interest, wanji_culture, thickness, and canon_asset.
- Do not reuse one subagent review result across multiple episode packets. A single-episode packet needs its own role findings; repeated reviewer ids across different episodes are treated as a failed audit unless the run is explicitly exploratory and not marked as completed ELO.
- A completed strict writer-room ELO must validate with `check_episode_loop_run.py --strict-writer-room`. Do not pass `--allow-reused-subagent-ids` in a strict writer-room completion run.
- Human-readable workflow docs, reviews, tickets, ledgers notes, and final explanations should be written in Chinese by default for this project. Keep machine-readable field names or stable ids in English only where scripts require them.
- `warn-through` is not a completion state. Any episode or prefix review marked `warn` must classify the warning as local-fix, regression, future watchpoint, implementation debt, or user-review item. Blocking/local-fix/regression warnings must be patched or ticketed before advancing. Nonblocking carried warnings must be written to the appropriate ledger, especially `unresolved_issues.tsv` or the relevant debt ledger.
- Opening chapters have a stricter promise. After C03, run an Opening Arc Review over C01-C03 as a playable trial: if the read is "well-designed but not compelling", "not enough robot-war pleasure", "relationships are dry", or "macro mystery feels absent", do not continue to C04 until the issue is patched, ticketed, or explicitly accepted by the user.
- Every thick run must keep two layers separate: the episode packet is the production source of truth; the reader synopsis is the emotional/readable artifact for judging whether the story works. Do not ask the user to judge story charm from packet scaffolding alone when a reader-facing synopsis is needed.
- The common-sense stakes gate is a hard creative gate for V31+ opening and testimony-heavy runs. If the prose uses grand terms for small visible actions, downgrade the term, enlarge the event, or mark a regression ticket before advancing. Do not let in-world importance override player common sense.
- Before finalizing a run directory, run `scripts/check_episode_loop_run.py`. A failing validator means the ELO did not complete.
- For V30+ opening/thick runs, pass `--strict-creative-gates` to `check_episode_loop_run.py`. A run without this flag is only structurally audited; do not present it as creatively gated.
- C01 has an additional Wanji breadth gate: the first playable closing route must show enough representative mecha/IP-spectrum exhibits to make "万机馆" feel true. A few props such as one model box, one cargo anchor, and one failed-machine stage do not pass. Default minimum for C01E01 is eight distinct collection/IP-spectrum samples unless the user explicitly changes the threshold.
- Fable review is a fixed second-pass after local packet pass, not an optional afterthought and not a pre-draft generator. For each episode in a Fable-enabled run, record one of: `fable_review_done`, `fable_failed_technical`, `fable_rejected_overdrift`, or `fable_skipped_user_approved`. A technical failure is nonblocking only when it is ledgered and replaced by a local dialogue/relationship/readability pass. Never silently skip Fable.
- V34+ source absorption is a hard gate for new thick full-run rewrites. Every episode must include `Episode Input Manifest`, `Scene Binding Matrix`, `Source Absorption Review`, and a `source_absorption.tsv` row for every selected source. Use `check_episode_loop_run.py --require-source-absorption` for V34/V35 completion claims. Older runs without this flag can only be described as structure/creative-field audited, not source-absorption audited.
- V35+ slot-contract runs must include `Author Slot ID`, route selected/skipped state, available fleet, lifecycle payload, incoming/outgoing decision threads, and five V35 ledgers. A returning unit may satisfy the mecha gate only through a scene-visible lifecycle delta; ordinary return does not count.

## Serial Episode Loop

For full-game or multi-episode synopsis generation where each episode must build from the previous one, first read `references/episode-loop-orchestrator.md`. Use it as the outer loop around this pipeline; each episode still runs the workflow below.

For chapter or full-run work, the outer loop must also run prefix regression review after each completed chapter: review chapters 1..N together, find the earliest root-cause chapter K for any major failure, revise K, replay K+1..N, then re-review 1..N before advancing. The same root cause may block at most three regression rounds; if it still fails, record it in the unresolved issue ledger, keep the best version, and continue. Static protagonist growth is a valid regression root cause, especially when 纪存、七海 or 白鸢 keep making small personality-correct choices without manga-protagonist-level reversals, insight, maturation, or upgrade.

A prefix result of `warn` must not silently advance. It must say why the warning is not a rollback blocker, where it is ledgered, and what later chapter must answer it. If the warning points to missing emotional event, weak mecha density, protagonist smallness, relationship ledgering, G.A.G./Index/Far Star underexposure, or continuity confusion inside already-written chapters, open a regression ticket instead of carrying it forward casually.

After C03, the outer loop must additionally run the Opening Arc Review. This review is harsher than normal prefix review because C01-C03 are the player's first proof of the game. It must judge trial-version appeal: robot battle pleasure, PV-grade images, relationship hooks, macro mystery pressure, playable variety, and whether the player would want C04. If it fails, the root cause may be in canon experience promise, material pool, episode packet, chapter assembly, or reader synopsis; fix the earliest root cause before advancing.

## Single-Episode Contract

The core pipeline produces exactly one episode packet per invocation:

- One episode card.
- One readable draft section for that episode.
- One writer-room review.
- One patch merge for that episode.
- One gate result and one state delta.

Do not use one pipeline invocation to draft a whole chapter, a chapter pair, or "two light episodes". For multi-episode or chapter work, the outer episode-loop orchestrator repeatedly calls this pipeline once per episode, carries ledgers forward, and assembles the chapter only after all included episodes pass gates.

If a draft fails a structural gate, return to that episode's pressure board or card before moving on. Do not rely on a later chapter-level patch to fix systematic missing mecha, gameplay, relationship, quote, enemy-gain, or meta-boundary problems.

## Workflow

1. **Task Brief**
   - State the requested scope, target artifact, mother draft, must-preserve material, and forbidden failure modes.
   - Identify the single episode being produced. If the user asks for multiple episodes, switch to the outer episode-loop orchestrator.
   - Declare the output class: route map, episode card, thick chapter synopsis, script, or asset brief.
   - If the target is a thick chapter synopsis, set a thickness target before drafting: V22.10-level scene chain, not a compact all-series card.
   - If the user says "do not rewrite", do patch-only work.
   - If the user wants a new draft, still preserve approved prior highlights unless explicitly discarded.

2. **Context Pack**
   - Query canon for involved characters, mecha, factions, scenes, locations, roster packages, art locks, runtime rules, gag hooks, and watchlist items.
   - Load the relevant mother draft and any accepted patches.
   - For V26 work, load V26-0 as the roster/IP remount source and V26.2 as the required drafting gate. Future accepted remount/gate docs supersede these only when explicitly recorded.
   - Load the current thickness benchmark when applicable. For A5 and full-series chapter expansion, V22.10 is the benchmark; do not compress its scenes into summary bullets.
   - Load the relevant 50-issue diagnosis/fix layer. Treat it as a thinking lens, not a checklist afterthought.
   - Load the current full-series roster/IP material pool, roster Bible/reserve backfill pool, and first-appearance candidate pool before selecting mecha or homage material. Do not use opening hook pools as the roster source; props, model boxes, exhibit labels, repair notes, and frames are anchors unless they trigger a unit with battle/gameplay function.
   - Load the roster what-if regret pool before branch choices, hidden units, hidden supports, say得, saved-death beats, original tragedy reversals, famous-scene IFs, or finale all-support payoffs. Select a candidate row or record a skip reason; prepare the IF repair question, originalization payload, trigger condition, failure dignity, and avoid boundary before drafting. Apply the non-uniform density rule: mine strong IPs deeply when the episode needs it, but do not fabricate weak tragedies for packages whose better role is mecha spectacle, gag, gameplay, or fan-ecology texture.
   - Load the real-world resonance case pool before writing model-street testimony, real-machine tears, late-reply exhibits, Far Star echoes, finale opening testimony, or reality-resonance scenes. Decide whether each episode uses a direct public case, a fictionalized motif, or no real-world testimony, and record the source/sensitivity decision.
   - Load the robot-culture value-axis pool before writing top-level theme, Far Star, Index, opening-right war, real-world testimony, finale, or episode experience promises. Decide whether the episode uses one value axis or explicitly skips it. If selected, prepare the scene/gameplay/character/mecha/enemy payload before drafting.
   - Select first-appearance mecha from the backfill pool/candidate pool according to the episode's actual dramatic/gameplay need; prioritize at least one roster-package-class backfill candidate outside bridge/business-light episodes; do not preassign the whole series or treat either pool as a fixed episode roster.
   - Load the current experience promise / opening promise canon when present: early chapters must sell robot-war pleasure, relationship curiosity, macro mystery, and the idea that the Wanji Museum is more than a lecture about robot culture.
   - Load the daily-life character-tone layer before any episode using shipboard life, aftercare, cooldown, daily comedy, Qihai onsite supervision, Baiyuan adult storyboard contrast, or adult relationship accumulation. Select a `life_hook_id` or record a skip reason; prepare the scene payload, relationship/persona change, gameplay/system change, non-converted ordinary object, and adult/child boundary.
   - Load the episode production layer split before writing or revising any thick synopsis, script-facing packet, gameplay-facing outline, or accepted episode packet. Prepare the readable story layer and the six production layers: ADV story, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, and settlement/state deltas. If a layer is absent, record a skip reason.
   - Load the Wanji origin/authority/binding-layer doc before any episode where Daige changes names, support state, archive terminal entries, fire/door routes, low-power responses, or Wanji carrier authority. Decide which layer is affected: display label, collection binding entry, modern compliance overlay, G.A.G. resonance, or physical machine state.
   - Load the Wanji body runaway and variable fortress doc and data before any episode where Wanji carrier body acts beyond ordinary support, G.A.G. takes over the battlefield through Wanji, section-shift battles occur, or Wanjidian transformation appears. Decide the `mode_id`, trigger, body action, benefit, debt ids, character backlash, enemy/public cost, and future read window.
   - Load the finale sacrifice grammar doc and data pools before C09-C15, future-failure-report pressure, Matrix-like false opening, Far Star judgement, Index clean-noise pressure, sacrifice-route eligibility, Qihai/Baiyuan cross-recognition, Jicun disappearance, star-consensus greeting, double-stay/quasi-harem endings, or projection/return beats. Record only grammar, eligibility, and debt; do not decide final deaths or final romance inside an early episode packet.
   - Record hard canon, working canon, candidate canon, prior highlights, risks, and open constraints.

3. **Pressure Board**
   - Create a single-episode pressure board before prose: premise, conflict, enemy learning chain, mecha density, gameplay shape, protagonist pressure, relationship heat, IP homage/super-robot feeling, emotion objects, branch debt, asset tiers, and canon boundary.
   - Add an experience board before prose: reader hook, PV-grade mecha image, relationship event, macro shadow, issue-to-drama conversion, and "what makes the player want the next episode".
   - Add a strict creative board before prose: real new IP-mapped units, roster-package-class unit, non-count anchors, IP scene projection, direct quote/misquote/original variation plan, burn point, tear point, gag point, PV-scale spectacle, Wanji collection density, protagonist big move, and Qihai/Jicun big move.
   - Add a what-if/regret board when the episode uses branch, hidden, say得, saved-death, famous-scene reversal, or terminal support material: selected `what_if_id`, source anchor, regret axis, IF repair question, originalization payload, trigger condition, failure dignity, route/hidden use, and avoid boundary.
   - Add a real-world testimony board when relevant: case id, usage mode, concrete object, Far Star echo, source/credit review, and do-not-use boundary.
   - Add a robot-culture value-axis board when relevant: selected axis id, dramatic question, scene payload, gameplay payload, character choice, mecha payload, enemy misuse, finale/debt link, and skip reason if not used.
   - Add a daily-life warmth board when relevant: selected `life_hook_id`, daily scene payload, persona/relationship change, gameplay/system change, non-converted ordinary object, lowbrow gag or adult-edge payload, child/youth isolation boundary, and skip reason if not used.
   - Add a production layer split board for every thick packet: readable story layer status, ADV story segment, exploration/side-play segment or skip reason, SRPG map battle segment or skip reason, in-battle drama event triggers, shipboard daily/relationship segment or skip reason, settlement/state delta, and downstream art/gameplay/script asset handoff.
   - Add a common-sense stakes board when the episode uses testimony/opening/authorization/debt/naming/label/record/public-display terms: largest term, L0-L4 stakes level, visible real-world consequence, whether the scene still works if the term is removed, and whether the term should be downgraded or the event enlarged.
   - Add a Wanji authority/binding board when the episode uses Wanji archive authority, Daige clearance, naming, renaming, support gray-out, low-power wake, or carrier systems: affected layer, who has edit authority, visible failure mode, what Wanji can still do offline, what Daige can still block externally, and what neither side can change.
   - Add a Wanji body-mode board when the episode uses carrier body action, G.A.G. body runaway, section-shift, or Wanjidian transformation: selected `mode_id`, G.A.G. pressure layer, Wanji carrier-body layer, Jicun machine-soul abnormal state, story/battle/settlement flow, trigger conditions, visible giant body action, player benefit, required debt ids, character limit/backlash, enemy sample or public cost, future read window, and forbidden shortcut.
   - Add a finale sacrifice grammar board when the episode seeds or pays off C09-C15 sacrifice pressure: global/team protected, person emotionally completed, cross-recognition direction, Jicun highest-cost eligibility, future-failure-report or false-opening pressure, star-consensus echo, route variable, and what must remain undecided.
   - Add a scene-chain promise: opening image, pressure arrival, playable problem, mid-battle twist, character choice, enemy extraction, aftermath hook.
   - Run the V26.2+ preflight gate when applicable: mecha/roster action, battle/play hook, quote/scene usage tier, relationship hard action, protagonist growth decision, emotion object, enemy gain, diegetic meta boundary, and next-episode debt must all be visible before drafting.
   - Do not write the full draft until the pressure board exposes what each part must do.

4. **Episode Cards**
   - Fill one episode card before long prose. Include: previous-state audit, story engine, A/B/C-line collision, scene-chain beats, battle/play type, map mechanics, mecha/roster appearance, protagonist decision and cost, relationship hard action, adult/romance edge where allowed, emotion object, IP homage/gag mapping and quote-use tier, enemy gain, branch debt, diegetic meta boundary, canon/asset boundary, and next-episode hook.
   - Include the experience fields: player curiosity hook, PV mecha beat, relationship hook, macro mystery pressure, trial-version appeal, and whether the episode risks reading like a design memo.
   - Include the roster/IP density fields: actual first-appearance IP-mapped mecha/unit selections, backfill source rows, candidate source rows, whether at least one selection is roster-package-class, units that count toward mecha density, returning units that do not count as new, anchors that do not count but trigger units, IP/scene/quote projections, and why the episode still feels like a robot tactics / robot-anime episode.
   - Include the what-if/regret fields when relevant: selected `what_if_id` or skip reason, source anchor, regret axis, IF repair question, originalization payload, trigger condition, failure dignity, branch/hidden/say得 use, and source/avoid boundary.
   - Include the reality-resonance fields when relevant: selected case id or skip reason, direct/inspired/fictionalized usage mode, concrete object, source/sensitivity boundary, authorization status, and whether it echoes Far Star late replies.
   - Include the value-axis fields when relevant: selected axis id or skip reason, scene/gameplay/character/mecha/enemy payload, and how it changes future debt instead of becoming a slogan.
   - Include the daily-life fields when relevant: selected `life_hook_id` or skip reason, scene/persona/relationship payload, gameplay/system payload, non-converted ordinary object, lowbrow gag/adult-edge boundary, and child/youth isolation rule.
   - Include production split fields: readable story layer, ADV story segment, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, settlement/state deltas, skipped-layer reasons, and production handoff notes.
   - Include finale sacrifice grammar fields when relevant: sacrifice eligibility seed, global/team protection target, cross-recognition direction, Jicun chorus-core option, future-failure-report or false-opening pressure, star-consensus greeting echo, route debt, and undecided ending boundary.
   - Include the strict creative fields exactly when V30+ strict mode is used: `Real New IP-Mapped Units`, `Roster-Package-Class Unit`, `Non-Count Anchors`, `IP Scene Projection`, `Burn Point`, `Tear Point`, `Gag Point`, `PV-Scale Spectacle`, `Wanji Collection Density`, `Protagonist Big Move`, `Qihai/Jicun Big Move`; C01E01 also requires `Wanji Collection Sample Count`.
   - For V35, include the slot contract fields: `Author Slot ID`, slot mapping, route window/state, selected/skipped slots, available fleet, cross-fleet reason, `New Unit Gate Mode`, lifecycle payload, incoming/outgoing decision threads, and skipped-slot world continuation. For V35.7 also include exact mystery/continuity/foreshadow binding ids, V29 crosswalk selection, high-density manifest ids or an explicit not-required reason, and the exact `V35.8 Loadout Contract ID`. Resolve V35.8 unit manifests, source rows, gameplay, effective gate, assets, and selectors before drafting.
   - If the episode lacks mecha, gameplay, relationship action, protagonist pressure/growth, enemy gain, quote/scene anchor, emotion, or next debt, fix the card before drafting.

5. **Batch Draft**
   - Draft exactly one episode, or one targeted patch to an existing episode.
   - Do not generate a long chapter in one pass unless the user explicitly asks for a rough route map; label it as a route map.
   - For V22.10-level work, draft one episode at a time. A full chapter may be assembled in one file only after each episode has passed review.
   - Do not replace story flow with field completion. Required fields are scaffolding; the prose must still contain cause, escalation, reversal, and character action.
   - Preserve approved wording and scenes by patching around them.

6. **Writer Room Review**
   - Review the single episode with separate lenses: showrunner, 50-issue auditor, mecha/IP specialist, SRW what-if/regret editor, gameplay designer, protagonist arc editor, Jicun memory editor, character/dialogue editor, relationship/adult-edge editor, common-sense stakes editor, V26.2+ gatekeeper, thickness editor, canon/asset steward, robot-anime/PV director, commercial opening producer, macro-mystery supervisor, player-interest representative, quote/scene continuity editor, spectacle/emotion/gag editor, and Wanji collection culture editor.
   - Reviews must name concrete missing scenes, contradictions, thin areas, and patch actions. Avoid generic praise.

7. **Fable Fixed Review Pass**
   - Run only after the local packet passes Writer Room Review and structure gates. Do not ask Fable to invent canon, roster, branch variables, battle rules, TSV rows, or new mainline events.
   - Provide one episode-scoped review pack: local Reader Synopsis, key relationship beats, short character voice notes, mecha/gameplay summary, forbidden changes, and the five required diagnosis surfaces.
   - Required Fable surfaces: readability/continuity, dialogue/persona naturalness, relationship/adult-edge heat, burn/tear/gag effectiveness, and boring/confusing/overwritten spots.
   - Page-body writeback is optional. Side-panel output or copied output is acceptable if captured and recorded. The local Markdown packet remains the source of truth.
   - Merge through Codex only: `accepted`, `accepted_after_rewrite`, `rejected_canon_drift`, `rejected_mecha_gameplay_drift`, `rejected_taste`, or `deferred_to_script_stage`.
   - If GUI submission, page chip, model selection, or page-body verification fails, record `fable_failed_technical` and run a local dialogue/relationship/readability pass before advancing.

8. **Patch Merge**
   - Apply targeted patches. Do not rewrite a passed draft wholesale.
   - Keep a patch log: what was preserved, what was expanded, what was added, what was downgraded or deprecated.
   - If the patch log reveals a systematic gate miss, redo the episode card and draft before advancing. Patch merge is for localized fixes, not for rescuing a structurally underbuilt episode.

9. **Structure Normalization**
   - Ensure every episode has required fields.
   - For thick chapter synopses, ensure every episode has a non-trivial `Story Flow`/`剧情流程` body, not just one or two summary paragraphs.
   - For reader-facing review, generate or assemble a `Reader Synopsis` layer when the user asks whether the story is interesting. It should read as continuous story, not a packet checklist; keep variables and gates in packet/appendix.
   - Ensure protagonist beats are concrete irreversible choices, costs, insights, upgraded capacities, or newly accepted limits. Do not pass labels such as "成长" or "更成熟".
   - Ensure relationship beats are concrete actions, permissions, support-state changes, jealousy, trust, misreadings, or debts. Do not pass labels such as "关系推进".
   - Ensure sacrifice-route beats are not mere role completion. Qihai, Baiyuan, or Jicun sacrifice seeds must visibly protect the team/world and emotionally recognize, complete, or refuse to let another person pay the price. If the beat is only "Qihai handles procedure", "Baiyuan leaves a blank", or "Jicun self-destructs heroically", rebuild it.
   - Ensure quote/scene anchors are tagged as direct short quote, misquote/misremembering, or original variation, and explain why the choice belongs in the scene.
   - Ensure every branch, hidden unit, saved-death beat, or famous-scene IF has a selected what-if row or an explicit skip reason. It must include an originalization payload, a playable trigger, and a failure dignity state. If the beat only says "choose route A/B" or copies an original IP tragedy with new names, rebuild it.
   - Ensure direct famous quotes are not consumed twice across episodes unless the quote ledger marks an intentional refrain. Reusing "我来组成头部" or any comparable high-recognition quote in two ordinary beats is a failure.
   - Ensure no model box, exhibit frame, testimony stand, label, repair note, or prop is counted as a mecha exposure unless the episode gives it an explicit battle unit, support action, enemy module, Boss phase, scene-mecha action, or gameplay-changing transformation.
   - Ensure returning units are not counted as actual first appearances. A returning unit only counts again if the episode gives it an independently named new form, weapon, pilot/support relationship, combination position, or gameplay function, and records that basis.
   - In V35 slot-contract mode, record that basis in `unit_availability.tsv`. Political reassignment, fleet transfer, enemy-to-ally state, route lock, and terminal payoff also qualify when they visibly change story and gameplay. Ordinary return, recolor, stat increase, or background Cut-in never qualifies.
   - Ensure functional modules, rule units, and scene machinery do not replace roster-package-class mecha over consecutive episodes. If an episode has no roster-package-class first appearance, record the bridge/business-light exception and the next compensation window.
   - In strict creative mode, functional modules and scene machinery cannot satisfy the "new参战机体/IP unit" promise by themselves. At least one real roster-package-class first appearance is required per episode unless the user explicitly approves an exception.
   - Ensure every episode has burn, tear, and gag payloads appropriate to its tone. A quiet episode can have a small tear or dry gag, but it must be deliberate and ledgered.
   - Ensure any real-world testimony is respectful and bounded: direct cases need source, usage mode, sensitivity boundary, and publication review; fictionalized motifs must avoid accidental one-to-one implication; neither can substitute for mecha/IP, gameplay, or protagonist decisions.
   - Ensure climax episodes have a PV-scale spectacle pass. A carrier launch, transformation, giant sortie, city-scale disaster, or equivalent climax must be staged as a multi-beat giant image, not a brief sentence or gray silhouette.
   - Ensure human characters do not speak world-outside meta such as "chapter", "player", or "plot"; only G.A.G., Index, UI, residual version layers, or designated gag carriers may thin the fourth wall.
   - Ensure abstract issues such as authorization, testimony, indexing, public trust, or opening rights have been translated into visible stakes: a machine moves, a map changes, a person is hurt or rescued, a relationship shifts, an enemy gains leverage, or a future route closes.
   - Ensure word weight matches common sense. Ordinary logs, labels, records, permissions, and small evidence should stay ordinary unless they visibly change money, bodies, relationships, mecha conditions, routes, enemy leverage, public punishment, or world-scale stakes. Downgrade overlarge terms before finalizing reader-facing prose.
   - Ensure any selected robot-culture value axis is not a slogan: it must have a visible scene, gameplay effect, character choice, mecha or object-to-mecha payload, enemy misuse, and future debt or terminal payoff.
   - Ensure any Wanji body runaway or variable fortress beat is not a free system effect: it must use a selected body mode, separate G.A.G. pressure / Wanji carrier-body action / Jicun abnormal state, show giant carrier-body motion, grant a concrete playable benefit, record at least three visible debts when triggered, and preserve those debts for later chapters or Wanjidian form.
   - Ensure any selected daily-life beat is not filler: it must change character feeling or relationship/support/permission/gameplay state, keep at least one ordinary object unconverted when possible, and avoid using daily comedy or adult-edge material to replace mecha/IP density or mainline drama.
   - Ensure every thick episode packet keeps readable story and production split separate. The production split must identify ADV story, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, and settlement/state deltas, with skip reasons for unused layers. If a battle, trigger, relationship daily scene, or state delta exists only inside prose and cannot be handed to production, fail the packet or add a targeted production-split patch.
   - Ensure final-route grammar remains open until the story earns it. Do not lock who dies, survives, returns, or becomes the final romance from an early packet; ledger eligibility, cross-recognition, unresolved cost, and future payoff windows instead.
   - Use `scripts/check_story_doc.py` with `--min-block-chars` and, when comparing a batch, `--max-min-ratio` to detect accidental thinning.
   - For V35 chapter packets, run `python3 scripts/check_v35_chapter_packet_consistency.py --chapter Cxx --strict` before sealing L4, L4.5, chapter Reader, or chapter review. With no current `passed/generated` artifact the command must fail; `--allow-noncurrent` is an explicit inventory-only inspection and never a production PASS. Story-chain hashes prove ordering, not semantic consistency.
   - Create/update machine-readable tables when useful.
   - Run the structure check script when working with Markdown episode docs.

10. **Canon/Graph Backfill**
   - If new entities, mecha, concepts, scene order, relationship beats, asset tiers, or workflow-critical docs are introduced, update canon TSVs, doc registry, graph nodes/edges, canonical terms, watchlists, and README/index files as appropriate.
   - Run `scripts/canon-smoke-test.sh`. Run Godot canon checks only when runtime/playable flow is touched.

## Required References

- Read `references/chapter-preproduction-and-human-voice.md` before expanding a chapter engine into a complete outline or Reader when new entities, abilities, spaces, multi-scale battles, transformations, dense control chains, or recurrent AI-voice defects are involved.
- Read `references/high-density-dramatic-chapter-mode.md` before any chapter whose coupled factions, characters, IP projections, mecha, gameplay, branches, or mysteries cannot be judged safely one episode at a time.
- Read `references/pipeline.md` for the full staged workflow and source layers.
- Read `references/review-roles.md` when doing writer room review.
- Read `references/templates.md` when producing pressure boards, episode cards, review memos, patch logs, or handoff notes.
- Read `references/episode-loop-orchestrator.md` when producing serial multi-episode/full-game outlines or when the user asks to loop/cycle the pipeline across episodes.
- Read `references/v35-slot-adapter.md` before any V35 Pressure Board, episode packet, route assembly, roster scheduling, C12+ fleet deployment, or completion claim. If using V35.7, query the V35.7 and V35.8 main documents plus all relevant `v35_7_*` and `v35_8_*` story tables before drafting.
- Read `references/writer-room-subagents.md` when the user authorizes subagents or when a full-run thick synopsis needs independent review roles.
- For V29+ work, opening-arc review, or any user question about whether the story is interesting, read `docs/superpowers/specs/2026-07-04-chao-gag-writing-pipeline-experience-gates-v1.md`.
- For all V29+ mecha, roster, IP homage, or episode-density decisions, read `docs/superpowers/specs/2026-07-04-chao-gag-full-series-roster-ip-material-pool-v0-2.md`, `docs/superpowers/specs/data/story/v29_roster_bible_reserve_backfill_pool_v0_1.tsv`, `docs/superpowers/specs/data/story/v29_roster_ip_first_appearance_candidate_pool_v0_1.tsv`, `docs/superpowers/specs/data/story/v26_roster_ip_remount_matrix_v0_1.tsv`, and `docs/superpowers/specs/data/story/v26_episode_slot_remount_v0_1.tsv`.
- For V31+ branch, hidden unit, hidden support, say得, saved-death, original tragedy reversal, famous-scene IF, or finale all-support payoff decisions, read `docs/superpowers/specs/2026-07-06-chao-gag-roster-what-if-regret-material-pool-v0-1.md`, `docs/superpowers/specs/data/story/roster_what_if_regret_pool_v0_1.tsv`, and `docs/superpowers/specs/data/story/roster_what_if_source_refs_v0_1.tsv`.
- For deep IP research, battle scene engines, relationship escalation, G.A.G./daily comedy, faction ecology, Far-Star/time rules, branch design, mecha visual grammar, or museum common-sense grounding, read `docs/superpowers/specs/research/2026-07-11-chao-gag-material-pack-depth-backfill-v1.md`, `docs/superpowers/specs/data/research/material_pack_source_refs_v1.tsv`, and only the relevant `robot_*_v1.tsv`, `mecha_visual_mechanical_grammar_pool_v1.tsv`, or `museum_curatorial_reality_pool_v1.tsv` tables. Selection is optional and needs a skip reason only when the episode's pressure board explicitly calls for that layer.
- For world-internal meta, outside-observer response, terminal/UI intrusion, Index Perfect Build, version switching, Echo Ledger, second-playthrough memory, fake deletion, external archive, or asynchronous player echoes, read `docs/superpowers/specs/2026-07-11-chao-gag-diegetic-meta-outside-observer-layer-v1.md`, `docs/superpowers/specs/data/story/diegetic_meta_layer_rules_v0_1.tsv`, `meta_version_profiles_v0_1.tsv`, `outside_observer_echo_ledger_schema_v0_1.tsv`, `meta_story_escalation_spine_v0_1.tsv`, `meta_event_safety_boundaries_v0_1.tsv`, and `docs/superpowers/specs/data/gameplay/meta_runtime_architecture_contract_v0_1.tsv`.
- For real-world testimony, model-street tears, late replies, Far Star echo scenes, finale opening testimony, or reality-resonance emotional material, read `docs/superpowers/specs/data/story/real_world_resonance_cases_v0_1.tsv`.
- For top-level theme, Far Star, Index, opening-right war, real-world testimony, finale, or episode experience promises, read `docs/superpowers/specs/data/story/robot_culture_value_axes_v0_1.tsv`.
- For shipboard life, aftercare, cooldown, daily comedy, Qihai onsite supervision, Baiyuan adult storyboard contrast, or adult relationship accumulation, read `docs/superpowers/specs/2026-07-07-chao-gag-daily-life-character-tone-layer-v1.md` and `docs/superpowers/specs/data/story/daily_life_character_scene_pool_v0_1.tsv`.
- For thick episode packets, accepted-packet revision, gameplay-facing outline, script handoff, or already-written synopsis repair, read `docs/superpowers/specs/2026-07-07-chao-gag-episode-production-layer-split-v1.md` and `docs/superpowers/specs/data/story/episode_production_layer_split_schema_v0_1.tsv`.
- For testimony/opening/authorization/debt/naming/label/record/public-display-heavy episodes, read `docs/superpowers/specs/2026-07-05-chao-gag-common-sense-stakes-and-word-weight-gate-v1.md`.
- For Wanji origin, archive authority, Daige clearance, naming/renaming, support gray-out, low-power response, old curator keys, or carrier transformation, read `docs/superpowers/specs/2026-07-06-chao-gag-wanji-origin-authority-binding-layer-v1.md`.
- For Wanji body runaway, G.A.G. emergency battlefield takeover through Wanji, Jicun machine-soul abnormality in runaway scenes, carrier body action, section-shift battles, or Wanjidian variable fortress transformation, read `docs/superpowers/specs/2026-07-07-chao-gag-wanji-body-runaway-and-variable-fortress-v1.md`, `docs/superpowers/specs/data/story/wanji_body_mode_spine_v0_1.tsv`, and `docs/superpowers/specs/data/story/wanji_body_runaway_debt_rules_v0_1.tsv`.
- For C09-C15 sacrifice pressure, Qihai/Baiyuan/Jicun sacrifice eligibility, future-failure-report pressure, Matrix-like false opening, Far Star judgement, Index clean-noise pressure, star-consensus greeting, double-stay/quasi-harem endings, or Jicun projection/return, read `docs/superpowers/specs/2026-07-06-chao-gag-finale-sacrifice-chorus-grammar-v1.md`, `docs/superpowers/specs/data/story/finale_sacrifice_grammar_v0_1.tsv`, and `docs/superpowers/specs/data/story/relationship_sacrifice_cross_recognition_v0_1.tsv`.
- For C01-C03 relationship hooks, opening PV shots, G.A.G./Index/Far Star early-shadow material, or anchor-trigger material, read `docs/superpowers/specs/2026-07-04-chao-gag-opening-hook-material-pool-v0-1.md`; do not treat it as the full-series roster/IP source.

## Useful Script

Use `scripts/check_story_doc.py` to verify that Markdown episode blocks contain required headings.

Example:

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_story_doc.py \
  docs/superpowers/specs/剧情梗概/V22-A5厚度修复整合稿-星火战队与万机同心-v22.10.md \
  --episode-regex '^## A\\d{2}-\\d+ ' \
  --heading '### 战斗与玩法' \
  --heading '### 机体出场' \
  --heading '### 燃点 / 爽点 / 梗点' \
  --heading '### 泪点' \
  --heading '### 感情线'
```

Use `scripts/check_episode_loop_run.py` before claiming an ELO run is complete:

Standard per-episode validation:

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V31 \
  --strict-prefix-warn-policy \
  --strict-creative-gates \
  --min-story-chars 1200
```

Fable-enabled validation adds the fixed-review ledger gate:

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V31 \
  --strict-prefix-warn-policy \
  --strict-creative-gates \
  --require-fable-review \
  --min-story-chars 1200
```

V34+ source-absorption validation adds the input-to-scene audit:

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V34 \
  --strict-prefix-warn-policy \
  --strict-creative-gates \
  --require-source-absorption \
  --min-story-chars 1200
```

Strict chapter/final validation:

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V28 \
  --require-subagents \
  --require-chapter-reviews \
  --require-run-validation-log \
  --strict-prefix-warn-policy \
  --strict-creative-gates \
  --strict-writer-room \
  --min-story-chars 1200
```

For a fresh run, first execute the relevant command without `--require-run-validation-log`; if it passes, record the command/result in `ledgers/run_validation.tsv`, then run the final command. Do not use the strict command as the default single-episode validator.

## Stop Conditions

Stop and ask or report clearly when:

- Canon hard locks conflict with the requested draft.
- The user asks for a final script but required character voice rules or role dossiers are missing.
- A draft would require new major mecha/characters without canon rows and the user has not approved candidate canon.
- The output is becoming a one-pass summary rather than a staged writer room result.
- A user-approved thick benchmark such as V22.10 is being compressed into a thin route map without explicit approval.
- A user asks for multiple finished episodes from a single core-pipeline invocation; switch to `references/episode-loop-orchestrator.md` and call the pipeline once per episode.
