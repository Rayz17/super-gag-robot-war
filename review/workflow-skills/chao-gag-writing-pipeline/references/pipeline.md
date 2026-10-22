# Pipeline Reference

## Creative-Order Override

For reconstruction of a structurally complete but creatively weak run, apply `story-first-reconstruction.md`. Its one-episode creative order overrides the ordering below: establish the representative single-run causal spine, dramatic fingerprint, camera/scene chain, player action, and human temperature first; then select optional source rows and build manifests, bindings, production splits, and ledgers. Hard canon, locked states, and user-confirmed assets still constrain the first pass.

The source-layer list below remains the authoritative inventory and validation order. It is not a requirement to expose all layers to the first creative pass. In Story-First Mode, Source Layer 0 is prepared after the scene core, and source absorption proves that chosen material was used rather than forcing the choice of material.

## High-Density Dramatic Chapter Override

When the chapter's factions, character arcs, IP story projections, mecha groups, gameplay forms, branches, and macro mysteries are coupled around a shared climax, read `high-density-dramatic-chapter-mode.md` before Round 0. This is a chapter-architecture pass above the single-episode Pipeline, not permission to draft a full chapter in one invocation.

Before the chapter brief, derive one compact Series Spine Alignment Card from the current production status and relevant full-series outline, reveal, character-fate, branch, mecha-lifecycle, and loadout slices. Mark what this chapter must resolve, may advance, may only foreshadow, and must reserve for later; define the outgoing state that must still launch the next chapter. If a stronger chapter idea conflicts, file an explicit downstream outline migration instead of silently consuming a future reveal, transformation, sacrifice, romance turn, antagonist evolution, or route payoff.

Then create one compact chapter brief containing the dramatic hierarchy, episode energy wave, escalation boundary, minimal time/location/control/scale/information board, inherited-highlight functions, representative route, persistent branch deltas, and lead-writer handoff. Every episode invocation reads that brief, the Series Spine Alignment Card, and the actual accepted Reader produced so far.

Keep one lead-writer responsibility for Reader prose. Reviewers return diagnosis and rewrite targets after the Reader exists; they do not contribute paragraphs for assembly. If a finding changes motive, causality, control, relationship, IP emotional premise, battle purpose, or branch result, rewrite the complete affected scene and replay later episodes. Field completion and local patch count cannot substitute for a coherent chapter.

## Chapter Preproduction and Fault-Routing Override

Before expanding a chapter engine into a complete outline, apply `chapter-preproduction-and-human-voice.md` when the chapter introduces new mecha/enemies, new abilities, multi-scale spaces, transformations, three-party battles, control-chain ambiguity, or repeated AI-voice defects. The complete outline is mandatory before the chapter performance-carrier plan, and both are mandatory before any Episode Reader.

Accepted material is evidence, not truth. User confirmation and Working status mean “preserve proven value and justify losses”; they do not mean “skip independent review.” Historical weak drafts are regression examples, not creative templates.

Compile only the context needed for this chapter, then pre-model entities, control, abilities, spaces, large actions, and reusable assets. The draft may use only pre-modeled elements. If a better idea appears during writing, pause, amend the model, and run the affected gate before continuing.

Route failures to the earliest owner:

- desire or opponent failure -> chapter engine;
- subject, control, carrier, permission, or ability failure -> preproduction model;
- distance, scale, movement, loading, or simultaneous-location failure -> spatial graybox;
- unclear map goal or unreadable battle change -> battle/gameplay preplan;
- relationship turn without a human event -> director/performance brief;
- unnatural or same-voice dialogue -> semantic human-voice review;
- canon/status conflict -> authority migration.

Never use dialogue to repair setting, terminology to repair causality, or an additional device to repair spatial confusion.

For V35, first run `python3 scripts/report_v35_layered_pipeline.py --check` and read the generated six-layer dashboard. Only its current active chapter can advance. Create and maintain that chapter's story-chain manifest before prose production. Run `--next`, then the exact `--before-stage` gate before every artifact; seal each accepted artifact with its current hash. After `complete_outline`, an independent first-read causality audit reads the outline without its design-defense boards. Only after that audit passes may episode structure, state ledger, four-view Layer4 review, and cumulative continuity receipt close L4. Run `assemble` before chapter assembly; the assembler uses only manifest-declared Episode paths in stage order, never a directory glob. After the assembled Reader, run the cross-chapter risk scan and full-scope `reader_causal_audit`, then semantic human-voice review, deterministic lint, and `chapter_review`. The Reader audit receipt is valid only for its exact Reader, prefix, and risk-scan hashes with no open P0 or blocking P1. `advance` and later chapter initialization require the dedicated `user_acceptance` receipt created from explicit user approval. C02 and later normally bind the predecessor Reader/state/acceptance fingerprint at `series_alignment`; a changed predecessor stales that alignment. If the user explicitly orders a bounded repair of already existing chapters, record that order in a repair-authority file and pass it only while resealing the listed chapters. Repair mode binds predecessor Reader/state/chapter-review plus the authority hash, never seals acceptance, and never unlocks a chapter outside the scope. Use `--invalidate-stage` when revising upstream. A later file already existing on disk is evidence of a bypass, not permission to continue.

Layer4 may refine episode count when the chapter's real scene capacity demands it. The current ceiling comes from the L3 row of `V35-upper-layer-registry.tsv`, not from this reference. Invalidate `first_read_causal_audit` and all later stages, then use `scripts/resize_v35_story_chain.py --migration-doc ... --reason ...`; do not hand-edit the registry or create and delete Reader files. A total above the current ceiling requires `--new-ceiling` in the same registered migration transaction.

Select the chapter profile before initializing its manifest. Use `light` only when cast, space, abilities, controls, and battle grammar are already established; use `standard` for one significant new place, ability, enemy rule, or control chain; use `heavy` for new giant spaces, multi-scale interaction, transformation, machine-soul/physical crossover, major ability debut, three-way combat, or spatially decisive spectacle. The profile scales preproduction and review depth but does not remove standard artifacts, first-read causality audit, semantic voice review, or user acceptance.

## Source Layers

Load sources in this order:

0. **Source absorption control layer**
   - In standard new-episode mode, create an Episode Input Manifest before prose. In Story-First Reconstruction Mode, create it after the causal spine and readable scene core exist: list selected and skipped source rows with source class, source id, read scope, selection/skip reason, and must-preserve payload.
   - In standard mode, create a Scene Binding Matrix before drafting. In Story-First Reconstruction Mode, bind selected sources to existing readable scenes after the scene core passes its first creative check. The matrix records player/gameplay action, character action, mecha/map action, enemy misuse/gain, state delta, and next required read; it does not invent scenes merely to consume rows.
   - After drafting, run Source Absorption Review: selected sources must be visible in the readable draft and visible in production split or state deltas. Source rows that exist only in Context Pack, Pressure Board, ledgers, or field labels are not absorbed.
   - For V34+ completion claims, record rows in `source_absorption.tsv` and validate with `check_episode_loop_run.py --require-source-absorption`.

1. **Canon layer**
   - `chao-gag-canon` skill instructions.
   - `docs/superpowers/specs/data/canon/*.tsv`.
   - `docs/superpowers/specs/data/design_graph/doc_registry.tsv`.
   - `docs/superpowers/specs/data/design_graph/graph_nodes.tsv`.
   - `docs/superpowers/specs/data/design_graph/graph_edges.tsv`.
   - `docs/superpowers/specs/data/design_graph/canonical_terms.tsv`.
   - `docs/superpowers/specs/data/design_graph/consistency_watchlist.tsv`.

2. **Mother draft and accepted patches**
   - The user-approved draft or strongest prior version.
   - Any patch docs, data tables, or watchlist rows that supersede weak versions.
   - Explicitly list "must preserve" scenes, phrases, emotional objects, mecha beats, and gameplay mechanisms.
   - When the task asks for thick chapter synopsis, compare content class and scene density against the strongest accepted thick draft. Current thickness reference: `docs/superpowers/specs/剧情梗概/V22-A5厚度修复整合稿-星火战队与万机同心-v22.10.md`. It is not a correctness or canon gold standard.
   - For V26 work, load `docs/superpowers/specs/剧情梗概/V26-0全剧机器人大战化重挂载方案.md` as the remount source and `docs/superpowers/specs/剧情梗概/V26-C01-C03锚点强化补丁-机体名场面关系-v26.2.md` as a writing gate, not just a C01-C03 patch.

3. **50-issue solution layer**
   - Treat this as a diagnosis and design-thinking layer, not a post-hoc checklist.
   - Important entry points include:
     - `docs/superpowers/specs/剧情梗概/全游戏逐话剧情梗概-50项问题整改方案-v05.md`
     - `docs/superpowers/specs/剧情梗概/全游戏逐话剧情梗概-50项问题整改方案-v06.md`
     - `docs/superpowers/specs/剧情梗概/全游戏逐话剧情梗概-50项问题爆破升级-v15.md`
     - `docs/superpowers/specs/data/story/issue_deep_revision_targets_v10.tsv`
     - `docs/superpowers/specs/data/story/issue_drama_energy_diagnosis_v11.tsv`
     - `docs/superpowers/specs/data/story/issue_construction_constraints_v12.tsv`
   - Extract only the relevant issue lenses for the current scope, but always check broad recurring risks: serial structure, weak mecha scale, missing romance/adult edge, weak IP homage, no tears, no enemy gain, branch invisibility, and chapter-level granularity.

4. **Character and voice layer**
   - Character dossiers, voice rules, art locks, relationship rows, and any accepted script revisions.
   - For scripts, require each speaker to have listener, purpose, action, subtext, and speech texture.
   - For protagonist arcs, require a current arc state for 纪存、七海、白鸢 and any episode-driving core cast member: desire, fear/misjudgment, current wound, latest irreversible action, latest cost, current upgraded capacity or limitation, and next relationship debt.

5. **Mecha/gameplay/IP/asset layer**
   - Roster package docs, mecha density rules, battle systems, map anchors, asset tiers, hidden unlock boundaries, gag hooks, and IP homage matrices.
   - For V29+ work, load `v29_roster_bible_reserve_backfill_pool_v0_1.tsv` as the priority roster-package backfill pool and `v29_roster_ip_first_appearance_candidate_pool_v0_1.tsv` as the supplemental selectable material pool. Do not treat either as a fixed per-episode roster. Select actual first-appearance units for the current episode only, then record them in the run ledger.
   - A first-appearance selection should carry its IP/story motif, iconic-scene mapping, quote/phrase anchors, story conflict payload, and gameplay payload into the episode. A name-only unit list does not pass this layer.
   - For V30+ strict creative runs, separate three categories before drafting: real new IP-mapped units that can count for roster promise, functional modules/scene machinery that may change play but do not satisfy roster promise, and anchors/props that only trigger story or unlocks. Model boxes, exhibit signs, repair notes, quote walls, tags, hands, helmets, terminals, and boxes cannot be counted as new参战机体.

5a. **Deep creative material layer**
   - Apply when the episode needs stronger IP specificity, a battle reversal, relationship escalation, comedy, faction motive, cosmic-SF mechanism, branch form, mecha visual identity, or museum common-sense grounding.
   - Load the overview `docs/superpowers/specs/research/2026-07-11-chao-gag-material-pack-depth-backfill-v1.md`, then load only the relevant tables under `docs/superpowers/specs/data/research/`: `robot_ip_deep_dossier_pool_v1.tsv`, `robot_anime_battle_setpiece_pool_v1.tsv`, `robot_relationship_scene_craft_pool_v1.tsv`, `robot_gag_comedy_engine_pool_v1.tsv`, `robot_industry_faction_ecology_pool_v1.tsv`, `robot_cosmic_sf_ontology_pool_v1.tsv`, `robot_branch_route_pattern_pool_v1.tsv`, `robot_hybrid_play_activity_pool_v1.tsv`, `mecha_visual_mechanical_grammar_pool_v1.tsv`, `museum_curatorial_reality_pool_v1.tsv`, and `material_pack_source_refs_v1.tsv`.
   - Do not use this as an all-table checklist. Choose the episode's dramatic need first, then select zero to two relevant rows per needed layer. Strong IPs may be mined deeply; light IPs may contribute comedy, spectacle, design, or ecology without fake tragedy.
   - Every selected row must carry a concrete payload into the Episode Input Manifest and Scene Binding Matrix: new action, reversal, image, playable rule, relationship consequence, faction move, or state change. Record it in `source_absorption.tsv` with `reader_visible=yes` and `production_visible=yes` before pass.
   - If the same micro-engine appears in two adjacent episodes, especially delays measured in seconds, half-grid favors, label changes, hidden-record gestures, or permission loopholes, use the deep pool to replace the engine rather than decorating it.
   - These are candidate research rows, not canon. Resolve package ids through the current crosswalk and never let a research row silently promote V35, schedule a first appearance, or create an art lock.

5b. **Diegetic meta / outside-observer layer**
   - Apply only when the episode uses terminal anomalies, unknown operation signatures, Index UI intervention, version profiles, Perfect Build, cross-run echoes, second-playthrough memory, fake deletion, external archives, or asynchronous player echoes.
   - Load `docs/superpowers/specs/2026-07-11-chao-gag-diegetic-meta-outside-observer-layer-v1.md` and the relevant meta tables. Resolve the current `META_S*` escalation stage before selecting an effect; do not jump from a reliable baseline to explicit observer recognition.
   - Fill: `meta_carrier`, `player_visible_effect`, `character_knowledge_limit`, `underlying_truth`, `state_consequence`, `recovery_path`, `echo_read`, `echo_write`, `safety_class`, `offline_fallback`, and `accessibility_fallback`.
   - Human characters cannot say player/chapter/game/plot/save-load language. Jicun may feel a result was refused; Qihai may find an unknown audit signature; Baiyuan may notice a watched frame; Fangzhou-T may describe timing. None of them can independently prove the real world.
   - The outside observer is one response among many, not a god. If the episode asks the player to save, love, judge, or command a character simply because they are the player, fail the layer.
   - Meta must produce a visible mecha, map, relationship, route, enemy-learning, or persistent-state consequence. UI drift alone is a gimmick and fails source absorption.
   - Any fake-delete, external-file, window, real-time, network, or cross-run effect must pass `meta_event_safety_boundaries_v0_1.tsv`; real saves and private data are never part of the fiction.

6. **SRW what-if / original-regret layer**
   - Apply when drafting route branches, hidden units, hidden supports, say得, saved-death beats, original tragedy reversals, famous-scene IFs, or finale all-support payoffs.
   - Load `docs/superpowers/specs/2026-07-06-chao-gag-roster-what-if-regret-material-pool-v0-1.md`, `docs/superpowers/specs/data/story/roster_what_if_regret_pool_v0_1.tsv`, and `docs/superpowers/specs/data/story/roster_what_if_source_refs_v0_1.tsv`.
   - Apply the non-uniform density rule. Strong IPs with many recognizable regrets may provide multiple candidates for one chapter or arc; light, comedic, ecology-heavy, or low-tragedy packages may record a skip reason and carry spectacle/gameplay/gag material instead. Do not make every package look equally tragic just to satisfy a table.
   - Select a `what_if_id` for the episode or record a skip reason. Carry source anchor, regret axis, IF repair question, originalization payload, trigger condition, failure dignity, route/hidden use, and avoid boundary into the pressure board.
   - This layer should make branches feel like robot-anime/SRW what-if repairs earned through play. It must not become an ideology menu, direct IP copy, or cheap revival.
   - Missing a hidden condition must still produce dignity: residual support, scar, object, log, later say得 window, or alternate meaningful route.

7. **V26.2 gate layer**
   - Apply to V26 and later episode drafting unless a newer accepted gate supersedes it.
   - Required checks: mecha/roster action, battle/play hook, quote/scene usage tier, relationship hard action, emotion object, enemy gain, diegetic meta boundary, next-episode debt.
   - Treat old patch lessons as preflight requirements. Do not draft first and plan to repair these later.

8. **Protagonist growth hard-gate layer**
   - Apply to all V26 and later thick synopsis or script work.
   - 纪存、七海、白鸢 must each have an explicit long arc and rolling state. They may be absent from some episodes, but they cannot pass chapter after chapter as static advisors.
   - Growth requires cost. A character has not grown just because they say the theme more clearly; they must lose comfort, authority, status, certainty, intimacy, safety, or a preferred self-image before the new capacity feels earned.
   - Tiny metrics cannot carry protagonist drama by themselves. "存不存档", "四十秒", "半格一格", "贴不贴标签", "一回合" and similar details are only valid when they reveal a larger ordeal: betrayal, collapse, vow, forbidden power, public sacrifice, irreversible strategy, relationship rupture, or a new burden.
   - A major protagonist decision should change at least one story system: route availability, support permissions, command authority, mecha unlock, public trust, legal status, relationship state, enemy template, or next objective.
   - Use a protagonist crucible shape for key turns: desire -> restraint/preparation -> misjudgment or temptation -> external blow -> internal collapse or dangerous awakening -> irreversible choice -> visible upgrade/new limit -> debt.
   - Default arc vectors:
     - 纪存: from preserving/recording everything toward publicly choosing what cannot be preserved, limiting his own naming authority, sharing curatorial power, and accepting that other people can refuse his archive. His big turns should include hidden endurance, strategic sacrifice, loss of archive control, dangerous G.A.G./museum authority, and chosen self-limitation after tasting a stronger power.
     - 七海: from lawful exception and mature restraint toward reform with visible professional cost, accountability, sensual danger in adult relationships, and the courage to leave a trace instead of hiding mercy as delay. Her big turns should include choosing between career/ecosystem protection and live people, being punished for mercy, abusing authority once, owning the scar, and rebuilding law instead of only delaying execution.
     - 白鸢: from observer/rewriter and protective ambiguity toward letting characters, viewers, and abandoned drafts reject her authorship; she must sometimes lose control of the frame she created. Her big turns should include a work turning against her, public accusation of manipulation, jealous/control impulses, refusal to draw a safe ending, and granting a character the right to leave her page.

9. **Emotional relationship event layer**
   - Apply to adult/成年感 relationship writing, especially 纪存×七海, 纪存×白鸢, 七海×白鸢 tension, 唐胶×兜灯, and other major bonds.
   - Attraction cannot be built from neat micro-actions, debt labels, or "shared wrongdoing" alone. Those are ledger terms, not drama.
   - Attraction also cannot be built only from huge twists. Use emotional accumulation before and after explosions: awkward closeness, missed timing, nearly-spoken confession, jealousy that the character dislikes in themselves, private care, repeated objects, gaze, hesitation, guilt, and small daily gestures that later hurt.
   - Katsura Masakazu-style romance craft may be used as method reference only: longing, embarrassment, timing, sincere but clumsy desire, triangle pressure, visual intimacy, and repeated emotional objects. Do not copy plot setups, character arcs, scenes, or quoted lines.
   - A relationship beat should include at least one emotional event when it carries the episode: misunderstanding, jealousy, hurt, tenderness, recognition, rescue, sacrifice, choosing someone over the correct plan, temporary loss, impossible return, or dog-blood reversal with consequences.
   - Death, disappearance, betrayal, or apparent irreversible loss may be used when it serves the arc; mecha/G.A.G./residual/version-layer logic can support later return, but the cost must remain visible.
   - Child characters remain completely outside adult-edge and dog-blood romance.

10. **Daily-life / shipboard warmth layer**
   - Apply when drafting shipboard life, aftercare, cooldown, repair-room comedy, lowbrow robot-anime jokes, Qihai onsite supervision, Baiyuan adult-storyboard contrast, or relationship accumulation scenes.
   - Load `docs/superpowers/specs/2026-07-07-chao-gag-daily-life-character-tone-layer-v1.md` and `docs/superpowers/specs/data/story/daily_life_character_scene_pool_v0_1.tsv`.
   - Select a `life_hook_id` or record a skip reason. Carry scene payload, persona/relationship change, gameplay/system change, non-converted ordinary object, comedy/adult-edge payload, and adult/child boundary into the pressure board.
   - A daily scene is not valid because it is cute. It must change how the audience feels about a character, or change support, permission, relationship, fatigue, repair, opening, route, or next-debt state.
   - Preserve some ordinary life. Do not immediately convert every food label, coat, sketch, cable, lamp, ticket, or repair rag into testimony, debt, enemy sample, or world key.
   - Qihai's daily layer is a staged arc: C01-C05 remote pressure, C06-end/C07 short onsite review, C08 onsite supervisor, later punishment and chosen belonging. Do not write it as sudden defection or romance reward.
   - Baiyuan's adult-storyboard contrast is allowed only for adult/adult-coded material and must serve desire/control/author-right themes. It must not become explicit pornography, girlification, or child/youth involvement.
   - Daily warmth cannot replace mecha/IP density, battle/gameplay hooks, PV spectacle, or mainline crisis.

11. **Jicun machine-soul memory layer**
   - 纪存 is not only a curator or archive terminal operator; he is a machine-soul entity whose past memories wake gradually under pressure.
   - Memory awakening should be heavy, embodied, and plot-moving. It can cause pain, authority glitches, G.A.G. resonance, protective overreaction, enemy tracking, or relationship misunderstanding.
   - A memory fragment must do work: unlock a sealed map layer, reveal why a deadlock exists, expose a lie, solve a battle rule, protect someone, explain a faction's wound, or point toward the G.A.G./Wanji/Far Star truth.
   - 纪存's protagonist power is effort, protection, wisdom, restraint, and dangerous self-knowledge. He solves deadlocks by reading people, machines, records, and his own returning memories, not by merely selecting archive labels.
   - Do not reveal the whole identity at once. Track fragments in `protagonist_memory_ledger` with trigger, cost/symptom, solved problem, identity delta, and next mystery debt.

12. **Real-world testimony / reality-resonance layer**
   - Apply when drafting model-street testimony, prototype workshop repair stories, real-machine tears, late-reply exhibits, Far Star echoes, finale opening testimony, or any episode using real fan life as emotional material.
   - Load `docs/superpowers/specs/data/story/real_world_resonance_cases_v0_1.tsv`.
   - Decide before prose whether the episode uses: direct public case, inspired/fictionalized motif, or no real-world testimony. Record the skip reason if the episode has a natural tear slot but no suitable case.
   - Direct public-case homage, especially RWR001, must carry source, usage mode, concrete object, sensitivity boundary, and publication authorization/credit review.
   - These cases should turn abstract love into objects and actions: a spare joint, old order, wrong support, late ticket, repair note, old account, or awkward instruction page. They should not replace mecha/IP density, playable conflict, protagonist choices, or original relationships.
   - Never make a real bereaved person a battle unit, cheap NPC tear button, or all-purpose proof that "robot culture matters".

13. **Robot-culture value-axis layer**
   - Apply when drafting top-level theme, Far Star, Index, opening-right war, real-world testimony, finale, episode experience promises, or any scene that tries to "raise the value" of robot culture.
   - Load `docs/superpowers/specs/data/story/robot_culture_value_axes_v0_1.tsv`.
   - Choose one axis only when it serves the episode: rough-translation coexistence, love-with-responsibility, respect for nonhuman things, anti-single-correct-template, small-object civilization scale, or non-unison civilization language. Skipping is allowed, but key episodes must record why.
   - A selected axis must become at least four visible payloads before prose: scene, gameplay, character choice, and enemy misuse. Strong episodes also add mecha payload and finale/debt link.
   - Do not use the layer as a mechanical KPI. "This episode proves robot culture matters" is not a payload. A machine must move, a map must change, someone must choose, an enemy must misuse something, or a future debt must appear.
   - Use the axes to connect small objects to civilizational scale without shrinking mecha/IP density: a repair note can trigger a unit or support, but it does not count as the unit.

14. **Strict creative gate layer**
   - Apply to V30 and later opening/thick synopsis runs unless the user explicitly asks for a light route map.
   - This layer exists to catch the V29 failure mode: structurally complete packets that still feel small, repetitive, under-mechaed, under-IPed, emotionally flat, or visually weak.
   - Every single-episode packet must declare: real new IP-mapped units, at least one roster-package-class first appearance unless explicitly bridge/business-light, non-count anchors, IP scene projection, burn point, tear point, gag point, PV-scale spectacle, Wanji collection density when relevant, protagonist big move, and 七海/纪存 core big move when relevant.
   - Quote and famous-scene usage is a finite resource. Directly using a famous line or signature scene more than once in a run requires an explicit refrain reason; otherwise the quote/scene continuity editor must fail the packet.
   - Opening Wanji Museum episodes must show breadth through representative exhibits, real machines, scale differences, and recognizable mecha-culture zones. C01E01 defaults to at least eight visible collection samples because the first closing route has to sell "万机" before asking the player to care.
   - Burn/tear/gag cannot be afterthought labels. Each must be a scene payload: what the player sees, what machine moves, what relationship or joke turns, what object remains, and what state changes.
   - PV-scale spectacle must be visible as giant motion, transformation, launch, collapse, map-scale damage, impossible rescue, awakening, or crowd-scale reaction. A short UI flash, a tag, or a one-frame residual image does not pass.

15. **Episode production layer split**
   - Apply to V31 and later thick episode packets, accepted-packet revision, script-facing outlines, gameplay-facing outlines, and already-written synopsis repair.
   - Load `docs/superpowers/specs/2026-07-07-chao-gag-episode-production-layer-split-v1.md` and `docs/superpowers/specs/data/story/episode_production_layer_split_schema_v0_1.tsv`.
   - Keep the reader layer and production layer separate. First write or preserve a continuous readable synopsis; then split the same episode into ADV story, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, and settlement/state deltas.
   - Unused layers require explicit skip reasons. This distinguishes "intentionally no SRPG fight" from "forgot to design the fight".
   - The split must be useful to production: art/background/portrait needs, map and unit needs, event triggers, UI/audio/Cut-in needs, relationship event triggers, and state deltas for the next episode.
   - Do not use the split as a replacement for story. If the reader synopsis is weak, fields cannot save it. If the story is readable but production cannot identify what the player does, the packet still fails.

16. **Wanji body-mode / runaway layer**
   - Apply when an episode uses Wanji carrier body action beyond normal support, G.A.G. emergency battlefield takeover through Wanji, body runaway, section-shift battles, or Wanjidian transformation.
   - Load `docs/superpowers/specs/2026-07-07-chao-gag-wanji-body-runaway-and-variable-fortress-v1.md`, `docs/superpowers/specs/data/story/wanji_body_mode_spine_v0_1.tsv`, and `docs/superpowers/specs/data/story/wanji_body_runaway_debt_rules_v0_1.tsv`.
   - Select a `mode_id` before prose. Define trigger conditions, visible giant body action, player benefits, debt ids, character limit/backlash, enemy sample or public cost, and future read window.
   - Separate the three layers before drafting: G.A.G. runaway is the engine-pressure layer; Wanji body runaway is the carrier-body manifestation layer; Jicun machine-soul abnormal state is the protagonist/body-cost layer. They may occur together, but they are not synonyms.
   - A body-runaway episode should normally run through three production beats: story prelude pressure, in-battle trigger with map/rule change, and post-battle debt settlement. If one beat is skipped, record why.
   - Do not collapse G.A.G. original-name burst, broken-opening burst, section-shift, Wanjidian, or Jicun abnormality into one red UI event.
   - A triggered runaway needs at least three visible debts; key runaway episodes should carry five or more. These debts must be readable later in UI wounds, support limits, route costs, damaged spaces, relationship scenes, or Wanjidian weak points.

## Round Structure

In Story-First Reconstruction Mode, insert the passes from `story-first-reconstruction.md` between Round 0 and the Context Pack. Round 1 becomes a compact hard-constraint dossier plus post-scene source selection, and Round 2 records the already-established dramatic fingerprint and scene chain. Do not present the full field list below to the first creative pass.

### Round 0: Task Brief

Write:

- Scope:
- Target output:
- Single episode ID:
- If multi-episode request, outer loop file:
- Detail class: route map / episode card / thick chapter synopsis / script / asset brief
- Mother draft:
- Must preserve:
- Known weak points:
- User constraints:
- Canon update expected:

The core pipeline invocation must name exactly one episode. If the user asked for a chapter, arc, or full-game sequence, the episode-loop orchestrator owns the chapter request and calls this pipeline once per episode.

For V28 and later thick synopsis runs, also write the target packet path:

- Episode packet path:
- Reviewer mode: single-context standard / targeted subagent standard / strict subagent / single-context fallback
- Run directory:

### Round 1: Context Pack

Produce a compact pack:

- Hard canon:
- Working canon:
- Candidate canon:
- 50-issue lenses:
- Mother draft highlights:
- Watchlist risks:
- Missing canon rows:
- Open choices:
- V26.2 gates to apply:
- Protagonist arc obligations:
- Jicun memory obligations:
- Strict creative gate obligations:
- Real-world testimony candidates:
- Real-world testimony use/skip reason:
- Robot-culture value-axis candidates:
- Selected value axis or skip reason:
- Value-axis scene/gameplay/enemy payload:
- Daily-life candidates:
- Selected daily-life hook or skip reason:
- Daily-life scene/persona/gameplay payload:
- Non-converted ordinary object:
- Lowbrow gag / adult-edge boundary:
- Production layer split source:
- Readable story layer status:
- ADV story segment:
- Exploration/side-play segment or skip reason:
- SRPG map battle segment or skip reason:
- In-battle drama event segment:
- Shipboard daily/relationship segment or skip reason:
- Settlement/state delta segment:
- Production handoff risks:
- What-if/regret candidates:
- Selected what-if row or skip reason:
- Non-uniform density note:
- IF repair question:
- Originalization payload:
- Trigger condition:
- Failure dignity:
- Source / avoid boundary:
- Token budget mode: standard / strict
- Files read: exact files or row ranges only
- Not loaded: broad tables intentionally skipped and why
- Episode Input Manifest: selected/skipped source rows, source class, source id, read scope, selection reason, must-preserve payload, and rows that must become scenes
- Source absorption risk: which selected rows are most likely to remain field-only unless bound to scenes

In Standard Episode Loop, the Context Pack should be a dossier, not a document dump. Prefer previous episode state rows, current episode target rows, and selected source rows. Avoid full `rg` scans over canon, graph, and all ledgers unless debugging a specific conflict.

### Round 1.5: Chapter Preproduction Compile

For light episodes that reuse established spaces and abilities, record a short skip reason and continue. For standard or heavy chapters, produce one readable preproduction model and, when automation needs it, one machine table.

Lock:

- each driving character's current desire, limited knowledge, refusal line, active move, and state change;
- each key mecha/enemy's pilot, machine soul, AI, weapon/control ownership, scale, role, signature large action, limit, and chapter lifecycle;
- every new ability's input, processor, physical executor, output, limit, cost, and player-visible proof;
- a small spatial graybox showing where humans, 18-24m units, giant units, and the carrier can actually move;
- an action vocabulary of screenshot-readable whole-body actions before joint-level details;
- asset and reuse class, with no special name or asset for a one-use object that does not alter image, play, causality, or future reuse.

Run the preproduction validator if a machine table exists, but record the result as structural evidence only. It cannot approve drama, performance, or prose.

### Round 2: Pressure Board

Write the pressure board before prose:

- Premise:
- Main conflict:
- Enemy learning chain:
- A/B/C lines:
- Scene chain:
- Relationship heat:
- Protagonist pressure:
- Emotional relationship event:
- Emotional accumulation:
- Daily-life warmth:
- Non-converted ordinary object:
- Adult/child boundary:
- Production layer split:
- ADV story payload:
- Exploration/side-play payload or skip:
- SRPG map battle payload or skip:
- In-battle drama triggers:
- Shipboard daily/relationship payload or skip:
- Settlement/state delta:
- Production handoff:
- Jicun memory/mystery:
- Mecha roster and asset tiers:
- Actual first-appearance IP-mapped mecha/unit candidates and source rows:
- Roster Bible/Reserve backfill candidates and source rows:
- Roster-package-class candidate among first appearances:
- Functional module / rule unit candidates:
- Mecha density units that count (full/support/enemy/Boss/scene-mecha/new form):
- Repeat returns not counted:
- Anchors that do not count but trigger units:
- Strict creative gate:
- Real new IP-mapped units:
- Roster-package-class unit:
- Quote/scene continuity plan:
- Original-work regret / what-if target:
- Selected what-if row:
- IF repair question:
- Originalization payload:
- Trigger condition:
- Failure dignity:
- Source / avoid boundary:
- Burn point:
- Tear point:
- Gag point:
- PV-scale spectacle:
- Wanji collection density:
- Real-world testimony/resonance motif:
- Real-world testimony usage mode:
- Real-world testimony source/sensitivity:
- Robot-culture value axis:
- Value-axis dramatic question:
- Value-axis scene payload:
- Value-axis gameplay payload:
- Value-axis character choice:
- Value-axis mecha payload:
- Value-axis enemy misuse:
- Value-axis finale/debt link:
- Protagonist big move:
- Qihai/Jicun big move:
- Gameplay modes:
- IP homage/gag targets:
- Emotion objects:
- Branches and long debt:
- Canon boundary:
- Scene Binding Matrix:
  - source item:
  - source class:
  - bound readable scene:
  - player/gameplay action:
  - character action:
  - mecha/map action:
  - enemy misuse/gain:
  - state delta / next required read:
  - reader-visible proof:
  - production-visible proof:
  - binding status:

Then write a V26.2 preflight gate:

- Mecha/roster action: at least one, normally two, actual first-appearance IP-mapped unit/module/scene-mecha exposures selected for this episode; except for bridge/business-light episodes, at least one should be a roster-package-class unit from the roster Bible/reserve backfill pool. At least one selected unit changes battle or gameplay. Anchors, model boxes, exhibit labels, repair notes, frames, or testimony stands do not count unless they trigger a battle unit/support/enemy/Boss/scene-mecha action.
- Repeat-return audit: returning units, old support calls, and second appearances must be listed separately and cannot satisfy the first-appearance requirement.
- Battle/play hook: what the player does, where, with what objective, failure pressure, and mid-encounter change.
- Quote/scene usage tier: direct short quote / misquote or misremembering / original variation; why it belongs here.
- Quote/scene continuity audit: whether this quote/scene has already been used in the run; if repeated, why the repetition is intentional and not accidental reuse.
- What-if/regret gate: branch, hidden, say得, saved-death, famous-scene IF, and terminal all-support beats need a selected what-if row or skip reason, originalization payload, playable trigger, and failure dignity. Fail any beat that only copies an IP tragedy, asks the player to pick an abstract route menu, or gives a cheap revival.
- Burn/tear/gag gate: the concrete fuel, tear object, and joke/satire turn. If one is absent, state why this episode is allowed to be quiet; otherwise rebuild.
- PV-scale spectacle gate: the trailer-scale image and its setup/impact/aftermath. UI-only or label-only images do not pass.
- Wanji collection density gate: for museum/showcase episodes, how many representative collection samples are visible and which mecha-culture zones they imply. C01E01 default minimum is eight.
- Protagonist big-move audit: the core decision and cost must be larger than tiny metrics like "40秒", "一格", "贴标签", or "水印".
- 七海/纪存 big-move audit: when either is central, the scene must show authority, sacrifice, forbidden mercy/power, public responsibility, rupture, awakening, or state-changing protection.
- Relationship hard action: concrete permission, jealousy, trust, misread, support-state change, shared wrongdoing, apology, withheld evidence, or public choice.
- Emotional relationship event: the felt scene behind the state change: who misunderstands, hurts, recognizes, sacrifices, saves, loses, returns, or chooses whom; how the event changes support/gameplay/story state.
- Emotional accumulation: what awkward closeness, missed timing, repeated object, almost-confession, guilty care, jealousy, or daily gesture makes the relationship believable before the big event.
- Protagonist growth decision: who makes a non-trivial decision, what ordeal or temptation forces it, what collapses, what it costs, what insight is earned, what capacity or limitation changes, and how it affects gameplay/story state.
- Jicun memory/mystery: if 纪存 is central, what memory fragment wakes, what triggers it, what it costs, what deadlock/mystery it helps solve, and what identity debt remains.
- Emotion object: proof, repair mark, ticket, log, part, message, exhibit, or body-state that carries feeling.
- Real-world testimony gate: if using a public case, record case id, source, direct/inspired/fictionalized mode, sensitivity boundary, authorization status, and how the scene avoids consuming real grief; if skipped, record why this episode does not need that layer.
- Value-axis gate: if using a value axis, record axis id, scene payload, gameplay payload, character choice, mecha payload, enemy misuse, and next debt; if skipped in a key theme episode, record why. A slogan without scene/gameplay/enemy payload fails.
- Daily-life warmth gate: if using shipboard life, aftercare, cooldown, daily comedy, adult-edge accumulation, Qihai onsite, or Baiyuan adult-storyboard contrast, record selected `life_hook_id`, scene payload, relationship/persona change, gameplay/system change, non-converted ordinary object, and adult/child boundary. Fail if the daily beat is pure filler, if it replaces mecha/IP density, or if adult-edge material touches child/youth lines.
- Production layer split gate: the episode must have a continuous readable story layer and a production split layer. The split must identify ADV, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, and settlement/state deltas, with skip reasons for unused layers. Fail if battle rules, triggers, relationship events, or state changes only exist inside blended prose and cannot be handed to art, gameplay, scripting, or asset sessions.
- Enemy gain: what the enemy learns, steals, copies, seals, misreads, or converts into a later template.
- Diegetic meta boundary: if meta is present, which allowed carrier expresses it; human characters must not say chapter/player/plot-level wording.
- Next debt: what the next episode must answer.

### Round 3: Episode Cards

The single episode card must answer:

- Previous episode audit:
- Story engine:
- A/B/C-line collision:
- Scene chain:
- Scene flow:
- Battle/play type:
- Map and mechanics:
- Production layer split:
- ADV story:
- Exploration/side play:
- SRPG map battle:
- In-battle drama events:
- Shipboard daily/relationship:
- Settlement/state deltas:
- Mecha/roster:
- Actual first-appearance IP-mapped units:
- Real New IP-Mapped Units:
- Real-world testimony/resonance:
- Real-world testimony usage mode and sensitivity:
- Robot-culture value axis:
- Top-design claim in scene:
- Value-axis gameplay/enemy payload:
- Roster Bible/Reserve backfill rows:
- Roster-package-class first appearance:
- Roster-Package-Class Unit:
- Functional module only exception:
- Candidate pool source rows:
- Countable mecha density:
- Repeat returns not counted:
- Non-count anchors:
- Non-Count Anchors:
- Relationship hard action:
- Emotional relationship event:
- Emotional accumulation:
- Adult/romance edge boundary:
- Protagonist decision/cost/upgrade:
- Jicun memory/mystery:
- Emotion object:
- IP homage/gag mapping:
- IP Scene Projection:
- Quote/scene usage tier:
- Burn Point:
- Tear Point:
- Gag Point:
- PV-Scale Spectacle:
- Wanji Collection Density:
- Wanji Collection Sample Count:
- Protagonist Big Move:
- Qihai/Jicun Big Move:
- Enemy gain:
- Branch debt:
- Diegetic meta boundary:
- Asset tier:
- Canon boundary:
- Next hook:
- Source absorption plan:
  - selected sources that become scenes:
  - selected sources that become gameplay/production actions:
  - selected sources that become state deltas:
  - source rows deferred with next required read:

### Round 4: Batch Draft

Draft only the approved single episode. Do not draft two episodes in one core-pipeline call, even if they seem light. Do not flatten later episodes into summaries.

For thick chapter synopsis:

- Keep the story flow as scene prose, not a card.
- Add a production split after the readable story layer. The split is a handoff scaffold for gameplay/art/script, not a substitute for the scene prose.
- Preserve causal sequence: why the scene starts, what pressure arrives, what the player does, what changes mid-battle, who chooses, what the enemy extracts, what remains.
- If one episode can be summarized in two short paragraphs without losing anything, it is probably underbuilt.
- Do not compress a previously accepted thick draft into a shorter synthesis unless the user explicitly asks for a route map.
- Keep backstage complexity backstage. A scene may contain several systems, but should normally make the player understand one decisive causal/control change through action, image, operation, or short dialogue.
- Do not add an unmodeled entity, location, device, ability, permission chain, or giant action inside prose. Pause and update Round 1.5 first.
- Before final dialogue, write a short performance pass: listener, immediate want, body action, interruption, evasion, emotional leak, and what remains unsaid.

### Round 5: Writer Room Review

Review with role lenses from `review-roles.md`. Require patches, not vibes.

Use Standard Episode Review by default. The main orchestrator runs the hard gates locally and may call only targeted subagents for uncertain risk surfaces. Record this as `Reviewer Mode: single-context standard` or `Reviewer Mode: targeted subagent standard`. The main orchestrator must not invent subagent findings; if no subagents were called, do not record subagent ids.

If subagents are available and the episode needs targeted review, use `writer-room-subagents.md` with the short Context Pack, relevant packet sections, and role-specific instructions only. Do not fork or send the full orchestration history by default.

For strict chapter gates, opening arc gates, final run gates, user-requested strict review, or any run marked `--strict-writer-room`, use the full ideal writer-room seats from `writer-room-subagents.md`. Shared advisory agents can feed the context pack, but they do not satisfy strict review. If the full seats cannot be run, downgrade the packet/run instead of calling it ideal writer-room reviewed.

Add a thickness pass when the target is a thick synopsis: compare the batch against V22.10-style density and identify missing scene chain, mid-battle twist, character action, mecha function, emotion object, or aftermath debt.

Add an independent semantic human-voice pass:

- acceptance and Working status grant no exemption;
- test whether anonymized lines remain distinguishable, whether two speakers can be swapped without damage, whether the character knows the information being spoken, who is listening, and whether the line changes the scene;
- reject narrator pre-defense, responsibility-report dialogue, technical cookbook speech, symmetrical debate, everyone speaking in polished aphorisms, parenthetical action replacing performance, and end-of-scene thesis summaries;
- preserve useful silence, interruption, unfinished thoughts, ordinary speech particles, embarrassment, bad jokes, mishearing, and listener-specific wording;
- run deterministic phrase/density lint only after semantic review; zero lint findings never prove natural dialogue.

Add a protagonist arc pass:

- If 纪存/七海/白鸢 are central to this episode, identify their desire, restraint/preparation, misjudgment or temptation, blow, collapse/awakening, decision, cost, insight, upgraded capacity or limitation, and next debt.
- If they are not central, identify whose protagonist-level turn carries the episode and how it affects the trio or the main party.
- If a chapter has no major protagonist decision, no setback before growth, or no changed authority/support/route/relationship state, do not pass chapter assembly.
- If the only protagonist turn is a small metric, convert it into a symptom of a larger ordeal or reject it as underbuilt.
- If a relationship beat is only "债务/共犯/权限/好感", convert it into an emotional event or reject it as underbuilt.
- If a relationship beat jumps straight to sacrifice, jealousy, confession, or dog-blood reversal without earlier accumulation, add awkward, repeated, emotionally specific build-up or mark the relationship as unearned.
- If 纪存 is central and his machine-soul identity or returning memories do not affect the mystery, protection, battle rule, or deadlock, mark his role as underbuilt.
- Do not overcorrect by making 纪存 repeatedly incompetent. His魅力 should come from difficult curatorial courage, tactical reading, public responsibility, and chosen self-limitation, not from endlessly causing disasters.

Add a V26.2 gate pass:

- If the episode lacks mecha, gameplay, relationship hard action, protagonist growth pressure, quote/scene tier, enemy gain, emotion object, meta boundary, or next debt, do not pass it.
- If the episode lacks a usable production layer split, or if SRPG details, in-battle triggers, side-play operation, daily relationship events, or settlement deltas cannot be extracted from it, do not pass it for script/gameplay handoff.
- If failure is local, patch the episode.
- If failure is structural, return to Round 2 or Round 3 and rebuild the pressure board/card before drafting again.

Add a source absorption pass for V34+:

- If a selected source row is only present in Context Pack, Pressure Board, Episode Card, or a ledger, fail it as field-only.
- If a mecha/IP source is selected but the machine does not move, fight, support, transform, change a map, unlock a state, or become an enemy/Boss/scene-mecha action, fail it or downgrade it to non-count anchor.
- If a quote/scene source is selected but there is no direct short quote, misquote/misremembering, original variation, Cut-in, scene structure, or player-triggered homage in the draft, fail it.
- If a branch/what-if/sacrifice source is selected but there is no trigger, failure dignity, route difference, cross-recognition, global/team protection, or next required read, fail it.
- If 纪存、七海 or 白鸢 source material is selected but their action remains a small permission/seconds/grid/label detail without relationship, authority, support, public, memory, enemy, or route consequence, fail it.
- Write the result to `source_absorption.tsv`; selected rows in a completed V34+ run must have `reader_visible=yes`, `production_visible=yes`, and `absorption_status=pass`.
- For each selected deep-material row, also record the specific transformation: `row_id -> episode scene -> original action/reversal -> gameplay or state delta`. Merely paraphrasing the research row or naming its reference IP fails absorption.
- A battle-setpiece row must alter the objective, map, midbattle reversal, mecha payoff, or player counterplay. A relationship row must alter desire, misunderstanding, physical action, rupture, rescue, intimacy, or support state. Industry/SF/museum rows must create a common-sense consequence, not more abstract terminology.

Add a strict creative gate pass for V30+:

- If a packet reuses a direct famous line or signature scene already consumed by the run without an explicit refrain policy, fail it.
- If real new IP-mapped units are missing, or only boxes/labels/modules/anchors are counted as mecha, fail it.
- If no roster-package-class unit appears in a non-bridge episode, fail it or explicitly mark the episode bridge/business-light and compensate in the next packet.
- If burn point, tear point, gag point, IP scene projection, or PV-scale spectacle are blank, generic, UI-only, or label-only, fail it.
- If C01E01 does not sell Wanji Museum breadth with enough representative collection samples and scale variety, fail it.
- If 纪存、七海、白鸢 are central but their actions remain tiny metrics without public cost, authority change, rupture, awakening, or state consequence, fail it.
- If the same failure appears again after a local patch, rebuild Round 2 and Round 3 instead of adding another patch.

Add a real-world testimony pass when the episode uses or naturally invites that layer:

- If direct public testimony is used without source, usage mode, sensitivity boundary, and publication review status, fail it.
- If a real person's grief is converted into a battle unit, joke target, or cheap tear button, fail it.
- If the testimony is the only reason the episode is emotional while mecha, gameplay, protagonist choice, or original relationships are thin, fail the episode's experience gate.
- If the episode would be stronger with a fictionalized motif rather than a direct case, downgrade the usage mode and record the reason.

Add a robot-culture value-axis pass when the episode uses or naturally invites top-level meaning:

- If a key theme episode does not query `robot_culture_value_axes_v0_1.tsv`, fail the context pack.
- If the selected value axis only appears as a conclusion, speech, or summary line, fail it.
- If there is no scene payload, gameplay payload, character choice, and enemy misuse, rebuild Round 2 before patching prose.
- If the axis duplicates a prior episode without escalation, reversal, or debt payoff, mark it as repetition and choose a sharper axis or a new payload.
- If small-object civilization scale is used to replace mecha/IP density, fail the mecha/IP and value-axis gates together.

### Round 6: Patch Merge

Apply targeted patches:

- Preserve:
- Expand:
- Add:
- Downgrade:
- Delete:
- Reason:

Patch merge must not become the normal way to add missing core dimensions. If the same gate fails repeatedly, mark the episode card as failed and rebuild it.

### Round 7: Normalize and Backfill

Normalize headings, tables, and links. Update canon/graph/watchlist when the result becomes a project baseline or migration candidate.

For Standard Episode Loop, run `check_episode_loop_run.py` with structural and strict creative gates but without `--strict-writer-room` unless strict seats actually ran. For chapter/final strict gates, add `--require-chapter-reviews` and `--strict-writer-room` only when those artifacts exist. If the checker fails, fix artifacts or downgrade the claim.

For V34+ full rewrites, add `--require-source-absorption`. If this flag fails, the run has not proven that the source material became story and production content; return to Round 1-3 for the affected episode.

## Anti-Decay Rules

- Never use "structure is right" as a substitute for scene content.
- Never let a later episode have fewer required fields than an earlier episode unless the user requests a brief outline.
- Never add mecha as names only; each must change battle, story, asset planning, or unlock logic.
- Never count a prop, quote wall, model box, repair note, tag, or UI anchor as a new参战机体 unless it produces a battle unit/support/Boss/scene-mecha action recorded separately.
- Never add romance as labels only; it must appear through action, timing, permissions, jealousy, trust, or battle support consequences.
- Never let debt/common-crime/permission bookkeeping replace emotional romance or bond drama. The audience needs scenes of misunderstanding, hurt, recognition, sacrifice, loss, return, jealousy, tenderness, and consequential choice.
- Never add protagonist growth as labels only; it must appear through irreversible decision, setback, insight, changed capacity/limit, and state consequences.
- Never let a flagship climax such as Wanji Museum ship transformation pass as a small textual state change; it needs giant motion, spatial reveal, playable pressure, witness reaction, and aftermath debt.
- Never spend a famous quote twice by accident. If a direct quote returns, it must be a designed refrain with changed meaning.
- Never make "纪存犯错" the default way to add drama. Give him agency, taste, competence, restraint, decisive public choices, and self-limitation that costs him something.
- Never add IP homage as vague "feeling"; name the recognizable trope and bind it to gameplay or story function.
- Never force every quote into original wording. Use one of three tiers: direct short quote, misquote/misremembering, or original variation. The quote tier must serve the scene.
- Never use real-world testimony from memory only. Query the resonance case pool, record source and boundary, and choose direct homage, fictionalized motif, or skip.
- Never turn real grief into a fightable unit, cheap NPC tear machine, or substitute for mecha/IP spectacle and protagonist action.
- Never use robot-culture value axes as final slogans. Query the value-axis pool, select or skip explicitly, and make the axis alter a scene, gameplay rule, character choice, enemy misuse, mecha action, or future debt.
- Never let Wanji body runaway or Wanjidian transformation pass as a free state label. Query the body-mode spine and debt rules, separate G.A.G. pressure / Wanji carrier-body action / Jicun abnormal state, stage a giant body image, grant real playable benefit, and record concrete costs that later chapters can read.
- Never use daily life as filler or apology for thin mecha drama. Query the daily-life pool, select or skip explicitly, and make the scene alter character feeling, relationship state, support/permission/gameplay state, or later debt while preserving some ordinary, non-systematized life.
- Never let readable story and production handoff collapse into one blurry paragraph. A good episode needs both: a continuous story that can be enjoyed, and a production split that tells gameplay/art/script what to build.
- Never let a selected source row remain field-only. If it mattered enough to select, bind it to a scene, player/character/mecha/enemy action, state delta, and next required read.
- Never turn "共同语言" into a unified chorus, external approval stamp, or all-purpose moral. The project payoff is non-unison civilization language: different voices remain audible and accountable.
- Never let 50-issue solutions become a checklist detached from the scene.
- Never claim a V22.10-level chapter if the episodes are only compact cards.
- Never let a machine-readable table passing its columns substitute for a readable scene draft passing drama.
- Never call the core pipeline once to write a whole chapter. The outer loop may assemble a chapter after each episode has passed the single-episode pipeline.
- Never pass "关系推进" as a relationship beat. Name the action, permission, misread, jealousy, support-state change, debt, or public choice.
- Never allow ordinary human characters to say world-outside meta. Put meta into G.A.G., Index, UI, residual version layers, or designated gag carriers.
