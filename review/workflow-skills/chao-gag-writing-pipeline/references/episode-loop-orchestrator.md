# Episode Loop Orchestrator

## Story-First Reconstruction Runs

When rebuilding an existing prefix that passed contracts but failed audience or story review, read `story-first-reconstruction.md` first. The loop must not copy the old pressure boards into prettier prose. Before any episode rewrite it creates a chapter reconstruction map, selects one representative single-playthrough route for the reader assembly, locks approved highlights, identifies repeated solution grammar, and then calls the single-episode Story-First Pipeline.

For these runs, manifests and engineering ledgers remain mandatory but are populated after the readable causal spine and scene chain exist. Independent reviewers receive the reader layer first. Contract review cannot substitute for showrunner, mecha/IP/spectacle, gameplay, character/relationship, and canon/macro/physical-budget evidence.

The loop must preserve alternate branch deltas without narrating mutually exclusive paths together. A prefix pass tests both the representative route's continuity and whether alternate routes retain visible long-term consequences. Reconstruction is complete only after a C13 seam test starts from the rebuilt state with a different dramatic fingerprint and without recap dumping.

Use this reference when generating serial multi-episode or full-game story outlines for 超GAG机器人大战.

This is an outer loop around the normal `chao-gag-writing-pipeline`. The core pipeline writes and reviews one episode per invocation. This orchestrator is responsible for chapter, arc, or full-game continuity by repeatedly calling the single-episode pipeline, carrying ledgers forward, assembling accepted episodes, and stopping only when a gate cannot be repaired locally. It must also preserve the requested detail class: a route map is allowed to be compact, but a thick chapter synopsis must reach V22.10-level scene density.

Accepted and user-confirmed chapters are never used as unquestionable content standards. They may serve as continuity facts, thickness references, and evidence of proven scenes, but the same causality, gameplay, mecha/IP, relationship, performance, and human-voice gates apply when they enter a regression review.

For V35, the orchestrator must first obey the full-series layered production state. Run `python3 scripts/report_v35_layered_pipeline.py --check`, read `V35六层创作生产看板.md`, and select only its current active chapter. The creative layers are L1 experience charter, L2 total engine, L3 series structure master, L4 complete chapter outlines, L5 Episode/chapter Readers, and L6 scripts/production; world mechanisms and Canon are horizontal support, while the performance-carrier plan is the mandatory L4.5 interface.

Create `docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/Cxx-story-chain.tsv` only after every earlier produced chapter has a sealed `user_acceptance` receipt. The required order is alignment, profile-scaled preproduction, director/battle/physical boards, complete chapter outline, independent first-read causality audit, episode structure/state/review/continuity evidence, performance-carrier plan, single-episode Readers, mechanical chapter assembly, semantic human-voice review, chapter review, explicit user creative acceptance, then the next chapter. Before every artifact, run `--next` and its exact `--before-stage`; use `--invalidate-stage` for upstream revision. Only sealed stages with matching hashes unlock the next stage. C01-C03 and previously accepted files have no bypass when their content hash changes.

If Layer4 changes a chapter's actual episode count, invalidate `first_read_causal_audit` and all later stages, then run `scripts/resize_v35_story_chain.py` with a registered migration document and reason. Never change episode count while producing Readers. Read the current Layer3 ceiling from `V35-upper-layer-registry.tsv`; it is an upper bound, not a per-chapter quota, and increasing it is an explicit L3 migration in the same transaction.

Before manifest initialization, classify the chapter as `light`, `standard`, or `heavy` in `V35-chapter-registry.tsv`. Light chapters reuse established entities and may keep preproduction compact; standard chapters introduce one significant new rule or place; heavy chapters trigger full physical/previs evidence. The profile controls cost, not quality gates. Every profile still receives first-read causality, semantic human-voice, chapter review, and user acceptance.

After every completed chapter N, run a prefix regression review over chapters 1..N. This is a professional whole-work read, not another field checklist. Build a reader assembly that removes ids, fixtures, contracts, historical PASS claims, and review narration before creative reviewers read it. For V35 Pressure Boards, use four independent creative receipts: professional writer, mecha-culture audience, game producer, and relationship/emotion editor. Track contract, story, audience, and production status separately; continuity success cannot stand in for audience success. The review must compare dramatic fingerprints, energy waveform, antagonist intention, player-visible branch divergence, debt retirement, IP-native pleasure, mystery answers, positive mecha desire, recurring opponent bodies, and repeated solution grammar, and must name the most memorable and most forgettable material. The reader-facing episode may spotlight only three to five state changes; all other contract state stays backstage until it becomes dramatic. If the issue exposed at chapter N has its root cause in an earlier chapter K, revise K, replay K+1..N, then review 1..N again before advancing to N+1. The review must include protagonist arc escalation, Jicun's machine-soul memory progression, emotional accumulation, and emotional relationship events: 纪存、七海、白鸢 and the main party need visible纠葛、挫折、成长、互相吸引、误会、体谅、牺牲 and upgraded capacity, not only personality-consistent small choices, tidy debts, or tiny metric beats. A failed/empty reviewer call is a technical failure, not a valid regression round.

After C03, run an **Opening Arc Review** over C01-C03 before advancing. This review asks whether the opening works as a playable trial, not whether the packet fields are complete. It must judge: whether robot-anime/SRW fans have enough mecha pleasure, whether C01-C03 contain at least three PV-grade images, whether 纪存/七海/白鸢/唐胶/兜灯 have hooks worth following, whether G.A.G./Index/Far Star cast a real shadow, whether the story reads as drama rather than a design memo, and whether the player would want C04. Failure here is a valid regression root cause.

For V30+ strict creative runs, the loop must also prove player-facing robot-anime appeal before chapter assembly: no repeated high-recognition direct quote unless intentionally refrained, no anchor/box/repair note counted as a real new unit, at least one roster-package-class first appearance per episode unless explicitly exempted, burn/tear/gag payloads, PV-scale spectacle for climax episodes, and enough Wanji collection breadth in C01E01 to sell the museum's scale.

For V31+ branch, hidden, say得, saved-death, famous-scene reversal, or terminal all-support material, the loop must treat SRW-style what-if/regret repair as a tracked material layer. `roster_what_if_regret_pool_v0_1.tsv` may feed route splits, hidden units, hidden supports, cross-work say得, original tragedy reversals, and failure dignity states. Every use must record selected `what_if_id`, source anchor, regret axis, IF repair question, originalization payload, trigger condition, failure dignity, route/hidden use, and avoid boundary. The loop should reject branches that read like ideology menus, direct IP copying, or cheap revival. Missing a hidden condition should leave a meaningful scar, residual support, object, log, or later window rather than simple punishment. The loop must also reject false equality: do not require each roster package to supply the same number of regret beats. Strong IPs may be mined repeatedly across an arc, while lighter packages can be skipped or used for spectacle, comedy, ecology, or gameplay if the skip reason is recorded.

For reality-resonance material, the loop must treat true fan testimony as a tracked source layer. `real_world_resonance_cases_v0_1.tsv` may feed model-street tears, prototype workshop repair stories, late-reply exhibits, Far Star echoes, and finale opening testimony. Direct public-case usage must record case id, source, usage mode, concrete object, sensitivity boundary, and publication authorization/credit review. Fictionalized motifs are preferred when a direct real case would become too consumptive or would displace mecha/IP, gameplay, or protagonist action.

For top-level meaning, the loop must treat robot-culture value axes as a tracked source layer. `robot_culture_value_axes_v0_1.tsv` may feed Far Star mistranslation, Index cleanup, opening-right war, real-world testimony, finale, and episode experience promises. A selected axis must record scene payload, gameplay payload, character choice, mecha payload, enemy misuse, finale/debt link, and result in `robot_culture_value_axis_ledger`. If a key episode skips the layer, the skip reason must be explicit. The loop should reject slogan-only "robot culture matters" conclusions.

For daily life and character temperature, the loop must treat shipboard warmth as a tracked source layer. `daily_life_character_scene_pool_v0_1.tsv` may feed aftercare, cooldowns, Qihai onsite supervision, Baiyuan adult-storyboard contrast, repair-room comedy, lowbrow robot-anime jokes, and relationship accumulation. A selected hook must record scene payload, persona/relationship change, gameplay/system change, non-converted ordinary object, adult/child boundary, and result in `daily_life_tone_ledger`. The loop should reject filler slice-of-life, daily scenes that replace mecha/IP density, or adult-edge material touching child/youth lines.

For production handoff, the loop must treat episode layer split as a tracked output layer. `episode_production_layer_split_schema_v0_1.tsv` defines the required readable layer plus six production segments: ADV story, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, and settlement/state deltas. A packet may keep a flowing story, but it must also expose what the player does, what the battle map requires, what event triggers fire, what daily/relationship event changes state, and what production assets are needed. Unused segments need skip reasons. The loop should reject packets whose battle, gameplay, relationship, or state changes exist only as blended prose and cannot be handed to art, gameplay, scripting, or asset sessions.

For V31 and later mid-late/finale material, the loop must treat finale sacrifice as a tracked grammar layer, not a prewritten ending. `finale_sacrifice_grammar_v0_1.tsv` and `relationship_sacrifice_cross_recognition_v0_1.tsv` feed C09-C15 sacrifice eligibility, future-failure-report pressure, Matrix-like false opening, Far Star judgement, Index clean-noise pressure, Qihai/Baiyuan/Jicun cross-recognition, double-stay/quasi-harem route eligibility, Jicun disappearance, star-consensus greeting, and projection/return beats. Each use must record what global/team state is protected, who emotionally recognizes or completes whom, what route variable is created, and what ending detail remains undecided. The loop should reject sacrifice that only completes a role such as "Qihai handles procedure", "Baiyuan leaves a blank", or "Jicun self-destructs heroically".

For V31.4 and later Fable-enabled runs, the loop is local-first: Codex writes and gates the episode packet locally, then sends only a constrained Fable Review Pack for second-pass diagnosis and local polish suggestions. Fable does not draft canon, roster, branch variables, battle rules, TSV rows, or new mainline events. A Notion/Fable GUI failure is nonblocking only when recorded as `fable_failed_technical` and replaced by a local dialogue/relationship/readability pass. Do not call an episode Fable-reviewed unless `fable_review_status` is `fable_review_done`.

For V34+ flow repair, the loop must prove source absorption. Every selected source row from canon, mother drafts, accepted patches, 50-issue fixes, mecha/IP pools, quote/scene anchors, branch variables, what-if/regret pools, sacrifice grammar, relationship material, daily-life hooks, value axes, Wanji body modes, production split requirements, enemy gains, or protagonist memory must be listed in an Episode Input Manifest, bound in a Scene Binding Matrix, visible in readable story, visible in production split or state deltas, and recorded in `source_absorption.tsv`. If a chapter reads as if a selected source never happened, treat it as a regression root cause even when all other ledgers have rows.

For V35, run the V35.4 slot resolver before the V34 source-absorption gate. Every episode packet must resolve `Author Slot ID`, slot-to-episode mapping, route selected/skipped state, available fleet, lifecycle payload, incoming/outgoing decision threads, and skipped-slot world continuation. Read `v35-slot-adapter.md`. Do not draft a V35 episode from a chapter paragraph or blank episode number.

## High-Density Dramatic Chapter Runs

When several factions, character arcs, IP story projections, mecha groups, gameplay forms, branches, and macro mysteries compete for one chapter-level climax, read `high-density-dramatic-chapter-mode.md` before entering the Core Loop. Do not confuse this mode with a high-density mecha manifest; the trigger is dramatic coupling, not row count.

Before the first episode, the orchestrator must derive a Series Spine Alignment Card from the current production status and relevant full-series dramatic wave, integrated outline, reveal ladder, character-fate spine, branch propagation, mecha lifecycle, and loadout state. It marks what this chapter must resolve, may advance, may only foreshadow, must reserve, and must hand to the next chapter. A better conflicting idea requires an explicit downstream outline migration; it may not silently consume a later reveal, transformation, sacrifice, relationship turn, enemy evolution, or route payoff.

The orchestrator then persists one compact chapter brief, episode energy wave, minimal causality board, inherited-highlight function table, representative route with persistent branch differences, escalation boundary, and lead-writer handoff. The core Pipeline still writes exactly one episode per invocation. Each later episode must read the alignment card and accepted Reader already written for this chapter, not only a prefilled episode card.

Before the first Episode Reader of every chapter, require a passed complete chapter outline, first-read causality audit, and performance-carrier plan. Standard or heavy chapters must also run the chapter preproduction compile from `chapter-preproduction-and-human-voice.md`; store at most one readable model, one optional machine table, and one review result. Light chapters that reuse established entities, spaces, abilities, and controls may fold preproduction into the director board with a recorded skip reason, but they may not skip the complete outline, first-read audit, performance plan, semantic voice review, or user gate.

Reader prose has one lead-writer owner. Independent reviewers examine completed Reader text and report symptom, evidence, root cause, and scene-level rewrite target; their prose is not merged as co-authored patches. A change to motive, causality, control, relationship turn, IP emotional premise, battle purpose, or branch result triggers a whole-scene rewrite and ordered replay of later episodes.

At chapter close, review the Reader without production fields first. Pass only when the chapter has a legible dramatic hierarchy, changing energy, consequential protagonist/mecha choices, story-level IP projection, clear playable conflict, persistent branch causality, physical coherence, and a climax earned by earlier actions. Reconcile actual answers, unresolved questions, character/mecha states, and the outgoing hook against the Series Spine Alignment Card before advancing. Do not pass from completed templates or quotas.

## Artifact Contract

For V28 and later thick synopsis runs, ELO is not considered executed unless the run directory has this shape:

```text
<run>/
  episodes/   # one packet per episode; source of truth
  chapters/   # assembled only after packets pass
  reviews/    # prefix regression reviews and replay logs
  ledgers/    # TSV ledgers
```

Rules:

- Every V35 run requires a current six-layer dashboard and the active chapter's `Cxx-story-chain.tsv`; a run is invalid when the dashboard is stale, the chapter is locked, or the exact stage gate was not executed or failed.
- One episode packet file contains exactly one `Episode ID`.
- Chapter files are assembly artifacts. They must cite the included episode packet files.
- Multi-chapter thick synopsis files are forbidden. Use an index file or route map if multiple chapters must be listed together.
- A chapter pass requires `reviews/Cxx-prefix-review.md`.
- A chapter with `Overall result: warn` is not automatically passable. The review must classify every warning, state whether it blocks replay, and ledger every carried issue. A warn with no ticket and no ledger row is a failed loop.
- C03 cannot be considered ready for C04 without `reviews/C01-C03-opening-arc-review.md` or an equivalent opening review section in `reviews/C03-prefix-review.md`.
- A regression ticket requires a replay log before advancing.
- Run `scripts/check_episode_loop_run.py` before claiming completion.
- V30+ strict creative runs must include `ledgers/creative_experience_gates.tsv` and `ledgers/mecha_ip_first_appearances.tsv`, plus expanded `quote_scene_usage.tsv` columns: `quote_text_or_phrase`, `quote_family`, and `reuse_policy`.
- V30+ strict creative validation uses `check_episode_loop_run.py --strict-creative-gates`. Without that flag, the run is only structurally validated.
- Strict writer-room validation uses `check_episode_loop_run.py --strict-writer-room`. This is the completion mode for chapter gates, opening arc review, final run completion, or episodes explicitly escalated to strict. It requires the full per-episode writer-room seats from `writer-room-subagents.md` and fresh reviewer ids; three shared advisory agents are not enough.
- Human-readable ELO artifacts for this project default to Chinese. English field names and ids may remain where validators depend on them, but findings, judgments, tickets, and explanations should be Chinese.
- Fable-enabled runs require a `fable_review_ledger` or equivalent TSV row per episode. Valid statuses: `fable_review_done`, `fable_failed_technical`, `fable_rejected_overdrift`, `fable_skipped_user_approved`.
- V34+ source-absorption runs require `ledgers/source_absorption.tsv`, `### Episode Input Manifest`, `### Scene Binding Matrix`, and `Source Absorption Review` in every episode packet. Final claims should validate with `--require-source-absorption`.
- V35 slot-contract runs also require `slot_episode_mapping.tsv`, `route_state.tsv`, `unit_availability.tsv`, `decision_propagation.tsv`, and `skipped_slot_world_state.tsv`, plus `--require-v35-slot-contract`.

## Review Intensity Tiers

Cost-control target: compared with 17-seat strict review on every episode, Standard Episode Loop should reduce subagent review calls by roughly 60%-80% per chapter and total token use by roughly 50%-75%, depending on how many targeted seats are needed. If a normal episode still reads full canon/graph/ledger tables, forks full context to many agents, or writes long review essays, the run has drifted back into strict mode and should be corrected.

Use **Standard Episode Loop** by default for normal episode drafting:

- Build a short Context Pack from the previous `Clear State`, `Auto Next Brief`, target canon rows, target ledgers, and selected material pools. Do not scan full canon/graph/ledger tables unless the packet introduces or migrates baseline facts.
- Review locally with hard gates: mecha/IP density, gameplay clarity, protagonist/relationship event, macro-shadow debt, canon/asset boundary, quote/scene continuity, burn/tear/gag/PV payload.
- Use targeted subagents only for risk surfaces that the local pass cannot confidently judge. A normal episode should use 0-3 targeted seats; a dense or risky episode may use the baseline seats from `writer-room-subagents.md`.
- Subagent prompts must include only the short Context Pack, the relevant packet sections, and role instructions. Do not fork the whole orchestration context or ask every subagent to read the whole repository.
- Subagent output must be short: `pass/fail`, up to three evidence bullets, must-fix actions, ledger risks, advance sentence.
- Update only necessary ledgers during the episode. Canon/graph backfill is required when new baseline entities, scenes, concepts, or workflow docs are introduced, but full graph sweeps are not.

Use **Strict Chapter Gate** after all episodes in a chapter pass Standard Loop:

- Assemble the chapter file.
- Run prefix regression review over chapters 1..N.
- Run the full strict writer-room seats only for chapter gate, opening arc review, final validation, or a specific episode that failed standard review in a way requiring independent audit.
- Run `check_episode_loop_run.py --require-chapter-reviews --strict-creative-gates --strict-prefix-warn-policy`; add `--strict-writer-room` only when strict seats actually ran and were recorded.

## When To Use

Use this workflow when:

- The user asks to write a full-game outline, multi-arc outline, or many episodes in sequence.
- The user asks to loop, cycle, recurse, or repeatedly call the writing pipeline.
- The work risks dropping mecha, gameplay, quote/scene anchors, 50-issue fixes, relationship heat, branch consequences, or enemy gains.
- The user wants the output to continue without stopping after every episode.

Do not use it for a single isolated patch unless that patch must update rolling state for later episodes.

## Core Loop

For each episode:

1. Audit the previous episode.
1a. In Story-First Reconstruction Mode, read the chapter reconstruction map and write the single-run causal spine, desire/opponent pair, dramatic fingerprint, climax image, aftermath temperature, and repetition veto before loading optional material rows.
1b. At a new chapter boundary, compile or refresh the chapter entity/space/action preproduction model before drafting the first episode. Do not inherit a previous chapter's ad hoc device, control chain, or space by implication.
2. For V35, resolve author slot, slot mapping, route/skipped state, available fleet, lifecycle event, and decision threads.
3. Decide the next episode's progression type.
4. Build the next single-episode brief and context pack.
4a. In standard mode, build Episode Input Manifest and Scene Binding Matrix before prose. In Story-First Reconstruction Mode, first draft and check the readable scene core, then select optional sources and bind them to those scenes. Selected sources cannot remain field-only in either mode.
5. Call the normal writing pipeline for that episode only.
6. Run Standard Episode Review by default. Use local hard gates plus targeted baseline seats only where needed. Always keep deterministic anti-AI lint separate from semantic human-voice review; if dialogue or readable prose matters, semantic review must cite live scene evidence. In strict writer-room mode, use fresh findings for every strict seat: showrunner, 50_issue, mecha_ip, gameplay, character_dialogue, relationship, protagonist, jicun_memory, quote_scene, spectacle_emotion, robot_anime_pv, commercial_opening, macro_mystery, player_interest, wanji_culture, thickness, and canon_asset. Shared consultant notes may be included in the context pack but cannot satisfy strict mode.
7. Review gates and patch local failures.
8. If the failure is structural, rebuild that episode's pressure board/card and rerun the single-episode pipeline before advancing.
9. In a Fable-enabled run, run the fixed Fable Review Pass: create the Fable Review Pack, request diagnosis/polish only, capture output or technical failure, merge or reject suggestions locally, and record `fable_review_status`.
10. Update rolling ledgers, including V35 slot/route/unit/decision/skipped-state ledgers, Fable review status when enabled, and source absorption status when V34+ is enabled.
11. Produce the next episode brief.

The next episode must start from the latest brief and ledger state, not from a blank outline slot.

The orchestrator may output a full chapter file only after all included episode packets have passed gates. It must not ask the core pipeline to draft the full chapter in one pass.

If a user asks to "write all chapters" at thick-synopsis density, ELO still produces and gates episode packets first. The user-facing answer may summarize progress, but project files must keep packet-level artifacts.

## Prefix Regression Review

Run this after each completed chapter:

1. Read chapters 1..N as one continuous playable story.
2. Review as showrunner, robot-culture expert, and game producer: drama, mecha/IP pleasure, playable variety, relationship escalation, enemy learning, G.A.G./Index/Far Star progression, branch visibility, and emotional payoff.
2a. In strict creative mode, also review as quote/scene continuity editor, spectacle/emotion/gag editor, and Wanji collection culture editor: famous quote consumption, recognizable IP scene projection, burn/tear/gag payloads, PV-scale climax staging, and Wanji collection density.
2b. In V31+ branch/hidden work, also review as SRW what-if editor: whether branch, hidden unit, say得, saved-death, famous-scene reversal, or terminal support material repairs, twists, or dignifies a recognizable robot-anime regret through original action; whether trigger conditions are playable; whether failure has dignity; and whether public-facing prose avoids protected IP copying.
2c. In V34+ source-absorption work, also review as source absorption editor: whether selected rows from canon, patches, 50 issues, mecha/IP, quote/scene, branch/what-if, sacrifice grammar, relationship, daily-life, value-axis, Wanji body-mode, enemy gain, and protagonist memory are visible in the chapter's readable story and production split, not only in packet fields.
2d. In V35 slot-contract work, also verify that assembled packets map to a legal route combination; every skipped slot has a continuing world state; unit deployment matches lifecycle and fleet; incoming decision threads changed scenes; and convergence preserved political, relational, facility, and roster differences.
3. Review as protagonist-arc editor: whether 纪存、七海、白鸢 have endured a real crucible, made costly choices, suffered reversals, gained or lost authority, changed support/route permissions, and grown beyond their initial defensive patterns.
4. Review as Jicun memory editor: whether his machine-soul identity wakes through heavy fragments that help solve mysteries, protect people, break deadlocks, and deepen identity rather than only add lore.
5. Review as relationship melodrama editor: whether major adult/成年感 relationships have both accumulation and events: awkward closeness, missed timing, repeated objects, attraction, misunderstanding, hurt, tenderness, jealousy, sacrifice, loss, return, or dog-blood reversal that alter story or gameplay state.
5a. Review as finale sacrifice grammar editor after C09 or whenever the episode touches terminal-route pressure: whether sacrifice seeds protect the team/world, whether Qihai/Baiyuan/Jicun emotionally recognize or complete another person, whether Jicun's highest-cost option is earned rather than heroic self-destruction, whether future-failure-report or false-opening pressure remains one pressure among many, and whether the draft avoids locking final deaths/romance too early.
6. If a problem appears, identify the earliest root-cause chapter K, not merely the chapter where the symptom appears.
6a. Route the root cause to the earliest owning layer: engine, preproduction/control, spatial graybox, battle preplan, director/performance, semantic human voice, or canon migration. Do not patch the latest Reader with explanation when the error belongs upstream.
7. Classify each issue before advancing:
   - `local_fix`: fix inside the just-finished chapter before assembly.
   - `regression`: root cause is in an earlier chapter K; open a ticket and replay.
   - `future_watchpoint`: deliberately reserved for later and ledgered with an explicit payoff window.
   - `implementation_debt`: numerics/UI/asset tuning that does not change story logic.
   - `user_review`: needs user-level tonal, route, or canon decision.
8. Create a Regression Ticket for every `regression` or unpatched `local_fix` with: symptom, root-cause chapter, affected ledgers, must-preserve highlights, revision target, replay range K+1..N, and pass condition.
9. Revise chapter K using the single-episode pipeline for affected episodes.
10. Replay K+1..N in order:
   - keep unaffected chapters and only update ledgers;
   - patch locally affected chapters;
   - rerun structurally affected chapters through ELO.
11. Re-run prefix review over 1..N.
12. If it passes, advance to N+1. If it is warn, advance only when every warning has a classification, ledger row, and later payoff/watchpoint.

Do not jump from revised K directly to N+1. The rewritten K changes input state for K+1..N.

The prefix review must be written to `reviews/Cxx-prefix-review.md`. If it opens a ticket, also write `reviews/<ticket-id>-replay-log.md` after replay. Without these files, the chapter status is not pass.

## Opening Arc Review

Run this once after C03 is assembled and its normal prefix review exists. It may be repeated later if C01-C03 are revised.

Questions:

- **Trial hook**: If the story stopped after C03, would a player want to continue to C04? What exact question, unit, relationship, or mystery pulls them forward?
- **Robot-war promise**: Do C01-C03 feel like the opening of a robot tactics game, or like a museum/culture essay? Count full units, support units, enemy units, Cut-ins, and modules separately; anchors alone do not satisfy the promise.
- **PV images**: Can the producer cut at least three trailer shots from the opening? Example categories: a giant machine protecting something small, a real unit entering the grid, a failed prototype changing the battle, a mothership/venue transformation, a villain rule system being punched through.
- **Wanji breadth**: Does C01E01 show enough representative exhibits, mecha silhouettes, roster-zone anchors, or collection samples for mecha fans to feel the place contains far more than the current playable route?
- **Quote discipline**: Are famous direct quotes and名台词 consumed once with purpose, or repeated because the draft lacked new ideas?
- **Relationship hook**: Would players start caring about or shipping any adult/成年感 relationship? Identify felt events, not only permissions, debts, or watermarks.
- **Macro shadow**: Did G.A.G., Index, Far Star, or the old catastrophe feel like a larger threat or wonder without being lore-dumped?
- **Issue-to-drama conversion**: Are authorization, testimony, labels, price, and unfinishedness embodied as people, machines, maps, loss, rescue, or victory?
- **Value-axis conversion**: Did the opening already show that robot culture is not only "worthy", but rough, responsible, nonhuman, anti-template, object-level, and non-unison? If a value axis appears, is it embodied as play and conflict?
- **Reader synopsis check**: Can the opening be read as continuous drama without packet scaffolding? If not, require a reader synopsis layer before user-facing review.

Results:

- `pass`: C01-C03 are strong enough to carry the player into C04.
- `warn`: only allowed if every weakness is classified and ledgered, with a specific C04-C06 payoff window or user-review decision.
- `fail`: open regression tickets for the earliest root-cause chapters and replay through C03.

The review should be written to `reviews/C01-C03-opening-arc-review.md` when available. It may also be mirrored in `prefix_reviews.tsv` or a dedicated opening review ledger. Do not advance on "后面会补" without a payoff window and ledger row.

## Warn Classification Gate

`warn-through` is only allowed as a tracked, nonblocking state. It cannot mean "I noticed a problem but moved on."

A prefix review with `Overall result: warn` must contain:

- `Warn classification`: one or more of `local_fix`, `regression`, `future_watchpoint`, `implementation_debt`, `user_review`.
- `Blocking issue`: `none` only if no already-written chapter needs repair.
- `Required action`: exact patch, ticket, ledger entry, or later payoff chapter.
- `Unresolved issue carried`: concrete issue id or `none`.

Rules:

- If classification includes `local_fix` or `regression`, do not advance until the fix/ticket/replay is done.
- If classification is only `future_watchpoint` or `implementation_debt`, write the carried item to the matching ledger. A prose note alone does not count.
- If classification is `user_review`, stop after writing the issue and the decision required.
- If no classification exists, treat the prefix review as failed.
- If `Unresolved issue carried` is non-empty but `unresolved_issues.tsv` has no row, the loop is failed.

## Regression Deadloop Breaker

Use root-cause identity, not wording, to count rounds. A "same root cause" means the same underlying failure remains, such as "Qihai/Jicun trust crisis lacks earlier dangerous intimacy" or "G.A.G. macro scale is not seeded before the space arc".

For the same root cause:

- Round 1: revise the root-cause chapter and replay to N.
- Round 2: revise again if the first fix created new issues or remained weak.
- Round 3: final blocking attempt; choose the strongest version generated by the three rounds.
- After Round 3: do not block forward progress. Record the issue in the unresolved issue ledger, mark chosen version and residual risk, then continue to N+1.

Stop for user decision only when the unresolved issue requires a high-level choice: changing the central premise, removing a locked character/mecha, changing a user-confirmed relationship route, or accepting a major tonal tradeoff.

## Detail Classes

Before a run starts, classify the requested output:

- **Route map**: compact full-series navigation. This may summarize each episode briefly, but it must be labeled as a blueprint and cannot be presented as a finished thick synopsis.
- **Episode card**: design card for one episode. It must contain all planning fields but does not replace prose.
- **Thick chapter synopsis**: readable chapter draft like V22.10. This requires full scene flow, battle/play mechanics, mecha actions, relationship beats, emotion objects, branch debt, and clear state for every episode.
- **Script**: dialogue and stage action. Requires character voice rules and scene-by-scene work after the thick synopsis.

If the user compares output against V22.10, or asks for "完整", "厚度", "别偷懒", "尽可能完整", or "保持V22.10强度", choose **Thick chapter synopsis**. Do not silently downgrade to route map.

## V22.10 Thickness Benchmark

Until superseded by a newer accepted thick draft, use `docs/superpowers/specs/剧情梗概/V22-A5厚度修复整合稿-星火战队与万机同心-v22.10.md` as a chapter-synopsis thickness and content-class reference, not as proof that its structure, causality, voice, or canon is correct.

A V22.10-level episode normally includes:

- A clear function/purpose statement.
- A multi-paragraph story flow with opening image, pressure arrival, playable problem, mid-battle twist, character choice, enemy extraction, and aftermath hook.
- Battle/play rules: map, victory/failure conditions, special mechanics, and at least one mid-battle change.
- Mecha appearance that explains what each unit does, not only what it is named.
- Heat/spectacle/gag that maps recognizable robot-culture memory into original action.
- Emotion and relationship beats carried by concrete objects, permissions, gestures, and consequences.
- Branches/debt and clear state that force the next episode to respond.

Length is not art by itself, but a thick synopsis that is only a few hundred characters per episode is almost certainly a route map. Use length checks as a tripwire, then review content quality.

## Previous Episode Audit

Extract:

- Clear state: what changed in the world, Wanji Museum, party, enemies, mecha, and systems.
- Debts: relationship, branch, object, enemy, gag, canon, and gameplay debts.
- Escalation: what cannot repeat at the same intensity.
- Mecha exposure: which units, modules, support forms, or anchors appeared.
- Quote/scene use: which homage anchors were consumed or left open.
- What-if/regret use: which `what_if_id` rows were consumed, left open, failed with dignity, or carried forward as hidden/say得 debt.
- Gameplay change: what the player actually did.
- Character turn: who made an irreversible action.
- Protagonist arc turn: which core character entered a crucible, what desire/restraint/misjudgment/blow/collapse/awakening drove the choice, what it cost, what capacity/limit changed, and how this affects 纪存/七海/白鸢 or the main party.
- Emotional relationship event: which relationship produced a memorable emotional scene, not just a ledger debt; what misread, sacrifice, tenderness, loss, return, jealousy, or dog-blood reversal changes state.
- Emotional accumulation: which awkward closeness, missed timing, repeated object, almost-confession, private care, or embarrassing jealousy makes the relationship feel earned.
- Jicun memory: what machine-soul memory fragment woke, what it cost, what mystery/deadlock it helped solve, and what identity debt remains.
- Real-world testimony: which case or motif was used, skipped, or carried forward; whether any direct public case has source, boundary, and publication review status.
- Robot-culture value axis: which axis was selected, skipped, or carried forward; what scene/gameplay/character/mecha/enemy payload it produced; what debt or terminal payoff it creates.
- Finale sacrifice grammar: whether the episode created sacrifice eligibility, cross-recognition, future-failure-report pressure, false-opening pressure, Jicun chorus-core option, star-consensus echo, double-stay cost-sharing capacity, or an explicit undecided ending boundary.
- Source absorption: which selected source rows were absorbed into readable scene, production split, state delta, and next required read; which rows remained field-only and must be patched.
- Enemy gain: what an opposing force learned, stole, copied, sealed, or misread.

If the previous episode lacks clear state, patch the previous episode before moving on.

If the previous episode lacks mecha action, gameplay hook, relationship turn, quote/scene tier, emotion object, enemy gain, or diegetic meta boundary, do not advance. Rerun the single-episode pipeline for that episode or apply a local patch and re-gate it.

## Progression Types

Choose at least one per episode:

- Seed: plant a future object, enemy sample, quote, misunderstanding, or mecha condition.
- Advance: make a prior debt produce visible consequences.
- Reverse: prove a prior win helped an enemy.
- Break: fracture trust, formation, route logic, or mecha synchronization.
- Burst: deliver a major battle, disaster, hearing, launch, public show, transformation, or runaway event.
- Cooldown: let characters process cost through repair, opening, ship life, or small social scenes.
- Payoff: return an old object, quote, choice, unit, branch scar, or promise with changed meaning.

## Context Pack

Before drafting an episode, gather:

- Canon or working setting for relevant characters, mecha, factions, locations, G.A.G., Index, Far Star, Wanji Museum, and gameplay rules.
- Previous clear state and debts.
- At least two candidate actual first-appearance IP-mapped mecha/unit/module/scene-mecha exposures from the full-series roster/IP material pool, the roster Bible/reserve backfill pool, the first-appearance candidate pool, or a recorded chapter patch. The backfill pool is the priority source for roster-package-class units with IP/story/scene/quote payloads; the candidate pool is selectable material, not a fixed episode roster. Anchors, model boxes, exhibit labels, repair notes, frames, and testimony stands must be gathered separately as triggers, not counted as mecha.
- Except for bridge/business-light episodes, at least one candidate should be a roster-package-class first appearance: main unit, rival, successor, hidden unit, or representative support unit. Functional modules, rule units, and scene machinery may supplement this but should not be the only new mecha layer across consecutive episodes.
- Returning units from prior episodes must be listed as `repeat_returns_not_counted`. They do not satisfy the first-appearance requirement unless the episode gives an independently named new form, weapon, pilot/support relationship, combination position, or gameplay function.
- At least one or two quote, scene, or robot-culture anchors.
- At least one candidate what-if/regret row when the episode contains branch, hidden, say得, rescue, tragedy reversal, famous-scene IF, or terminal all-support material. If the episode intentionally skips this layer, record the skip reason.
- At least one candidate PV image and one player curiosity hook.
- At least one macro-shadow candidate when the episode belongs to an opening or arc-launch segment.
- At least one model/toy/ecology material.
- Real-world testimony/resonance candidate when the episode touches model street, real-machine grief, late replies, Far Star echoes, finale opening testimony, or reality-resonance tears. If using a direct public case, include case id, source, usage mode, sensitivity boundary, and authorization status; if not, record a fictionalized motif or skip reason.
- Robot-culture value-axis candidate when the episode touches Far Star, Index, opening rights, real-world testimony, finale, or top-level theme. Choose from rough-translation coexistence, love-with-responsibility, respect for nonhuman things, anti-single-correct-template, small-object civilization scale, or non-unison civilization language; prepare scene/gameplay/character/mecha/enemy payload before drafting.
- Wanji body-mode candidate when the episode touches carrier body action, G.A.G. emergency battlefield takeover through Wanji, body runaway, section-shift battles, or Wanjidian transformation. Choose a `mode_id` from `wanji_body_mode_spine_v0_1.tsv`, prepare the three-layer separation (G.A.G. pressure layer, Wanji carrier-body manifestation, Jicun machine-soul abnormal state), trigger conditions, visible giant body action, player benefits, debt ids from `wanji_body_runaway_debt_rules_v0_1.tsv`, character limit/backlash, enemy/public cost, future read window, and the story-prelude / in-battle-trigger / post-battle-settlement flow.
- Daily-life character-tone candidate when the episode touches shipboard life, aftercare, cooldown, relationship accumulation, Qihai onsite supervision, Baiyuan adult-storyboard contrast, repair-room comedy, or lowbrow robot-anime jokes. Choose from `daily_life_character_scene_pool_v0_1.tsv`, or record a skip reason; prepare scene/persona/gameplay payload, non-converted ordinary object, and adult/child boundary before drafting.
- Episode production layer split plan for every thick packet or script/gameplay-facing outline: readable story status, ADV story segment, exploration/side-play segment or skip reason, SRPG map battle segment or skip reason, in-battle drama event triggers, shipboard daily/relationship segment or skip reason, settlement/state delta, and production handoff risks.
- Finale sacrifice grammar candidate when the episode is C09-C15 or touches sacrifice, future reports, false openings, Far Star judgement, Index clean-noise pressure, double-stay/quasi-harem route, Jicun disappearance, star-consensus greeting, or projection/return. Choose relevant grammar rows and cross-recognition beats; prepare global/team protection, emotional completion, route debt, and undecided boundary before prose.
- Relevant 50-issue fix layers and forbidden failure modes.
- Gameplay candidate: battle, exploration, deep dive, opening, repair, hearing, chase, infiltration, or hybrid segment.
- Relationship pressure and adult-edge boundary when applicable.
- Protagonist pressure: the current desire, fear/misjudgment, preparation/restraint, external blow, collapse or dangerous awakening, decision, growth/upgrade and next debt for involved core cast. For 纪存、七海、白鸢, avoid static competence, avoid using only "做错事" to create drama, and reject tiny metrics as the main dramatic event unless they reveal a larger ordeal.
- Emotional relationship event: if a relationship carries the episode, define the felt event before prose: misunderstanding, hurt, tenderness, recognition, jealousy, sacrifice, temporary loss, impossible return, or choosing someone over the correct plan.
- Emotional accumulation: pick one or more build-up methods before event-level payoffs: awkward repair/cockpit/medical proximity, missed timing, repeated object, almost-confession, guilty retreat, private care, or jealousy the character is ashamed of.
- Jicun memory/mystery: if 纪存 is central, define the memory trigger, symptom/cost, clue unlocked, deadlock solved, protection action, and next identity mystery.
- Asset tier: full unit, support unit, enemy unit, Boss module, scene-mecha, Cut-in, map object, anchor item, text/UI evidence. Mark which entries count toward mecha density and which are only anchors.
- V26.2 gate inputs when applicable: remount source, accepted patches, mecha/roster action, quote/scene tier, relationship hard action, enemy gain, diegetic meta boundary, and next debt.

## Episode Gates

Each episode must pass:

- The declared detail class is honored. A thick synopsis must not be delivered as a compact card.
- Scene chain exists: opening image, pressure, playable problem, mid-battle twist, character choice, enemy extraction, and aftermath hook.
- At least one, normally two, actual first-appearance IP-mapped mecha/unit/module/scene-mecha exposures selected for this episode. Except for bridge/business-light episodes, at least one should come from the roster Bible/reserve backfill pool or an equivalent recorded roster-package chapter patch. Anchors must be listed separately and do not count by themselves.
- Returning units are welcome for continuity and payoff, but must be listed separately and cannot satisfy first-appearance density.
- At least one mecha/unit is tied to battle or gameplay rules.
- At least one episode-level reader hook exists. "It advances the theme" is not enough; the hook must be a question, danger, unit, relationship, mystery, or reward the player can anticipate.
- In opening or key episodes, at least one PV-grade mecha/spectacle image exists. A named anchor item or UI table does not count unless it makes a machine move, transform, defend, fail, awaken, or change the map.
- At least one or two quote/scene/culture anchors are used through a declared tier: direct short quote, misquote/misremembering, or original variation. Direct short quotes are allowed only when short, scene-bound, and not a substitute for original drama.
- Branch, hidden, say得, rescue, saved-death, famous-scene IF, and terminal all-support beats must select a what-if/regret row or record a skip reason. The beat must have originalization payload, playable trigger, and failure dignity. If it is only a route menu, a copied IP tragedy, or a cheap revival, it fails.
- At least one playable hook exists.
- At least one enemy gain or enemy misread exists.
- Daily-life, aftercare, cooldown, and relationship-accumulation scenes must select a life hook or record a skip reason; if selected, they must change character feeling or relationship/support/permission/gameplay state and preserve a non-converted ordinary object when possible.
- Thick packets, accepted-packet revisions, and script/gameplay-facing outlines must include a production layer split. ADV story, exploration/side play, SRPG map battle, in-battle drama events, shipboard daily/relationship events, and settlement/state deltas must be separable, with skip reasons for unused layers.
- Battle or gameplay cannot be left as prose only. A SRPG segment needs map, units, victory/failure, special rules, and mid-encounter change; an in-battle drama segment needs triggers and state effects.
- At least one relationship hard action exists: permission, jealousy, trust, misread, support-state change, shared wrongdoing, apology, withheld evidence, public choice, or debt.
- Relationship beats that carry the episode must include an emotional event. Debt/common-crime/permission labels alone do not pass; the beat needs felt misread, hurt, recognition, sacrifice, loss, return, jealousy, tenderness, or consequential choice.
- Sacrifice-route beats must include global/team protection and cross-recognition. A sacrifice seed does not pass if it only completes the sacrificer's personal theme or job function.
- Relationship events need enough emotional accumulation to feel earned unless the point is sudden shock. If sudden, later episodes must process the lack of preparation as a wound.
- In adult/成年感 relationship scenes, "权限/债务/共犯" does not pass by itself. There must be felt attraction, embarrassment, jealousy, hurt, tenderness, misread, sacrifice, or a dangerous choice that changes support, trust, route, or public responsibility.
- At least one protagonist growth pressure exists in every key episode, and every chapter must leave a visible protagonist arc delta. A passable delta includes ordeal, restraint/preparation, collapse, awakening, costly decision, public responsibility, authority gain/loss, support permission change, route commitment, relationship rupture/reconciliation, forbidden power, comeback, or a new limitation accepted by the character.
- If 纪存 is central, his machine-soul memory progression must affect more than exposition: it should solve or complicate a mystery, protection choice, battle rule, map layer, or G.A.G./Wanji/Far Star truth.
- At least one macro-shadow or scale signal must be present in arc-launch and opening chapters: G.A.G. abnormality, Index optimization, Far Star misread/late signal, old catastrophe scar, or Wanji Museum hidden-scale reveal. It must be visible as an event, UI wound, map anomaly, enemy extraction, or object behavior, not only a lore sentence.
- Wanji carrier body action, body runaway, section-shift, and Wanjidian transformation must not be left as a state label. If selected, the packet must separate G.A.G. pressure, Wanji body action, and Jicun abnormal state; then show giant body motion, playable benefit, concrete debt ids, character backlash, enemy/public cost, and future read window.
- At least one emotion object or recoverable proof exists.
- If real-world testimony is used, it is sourced, bounded, and ledgered; direct public cases require publication authorization/credit review, and fictionalized motifs must avoid one-to-one implication.
- At least one next-episode debt exists.
- Finale-route material must not lock the final death/survival/romance state before the written story earns it; record eligibility and debt instead.
- Human characters do not speak world-outside meta. If meta exists, it is carried by G.A.G., Index, UI, residual version layers, or designated gag carriers.
- Abstract issue gates: if the episode focuses on testimony, authorization, labeling, pricing, safety, public trust, or unfinishedness, it must dramatize the issue through a person, machine, battle objective, route loss, rescue, public humiliation, or enemy gain.

Do not pass an episode by promising to fix these later.

## Full Run Mode

When the user asks to continue through the whole outline without a per-episode approval stop:

- Continue episode by episode internally.
- Call the core writing pipeline once per episode. Do not combine multiple episodes into one core-pipeline invocation.
- Write one packet file under `episodes/` per accepted episode before assembling any chapter file.
- Use Standard Episode Loop for normal episodes. Use writer-room subagents only as targeted reviewers unless the episode is escalated.
- In Fable-enabled mode, run Fable once per accepted local episode packet after local gates and before chapter assembly. If Fable technically fails, record the failure and run local fallback review; do not skip silently and do not block the full outline on Notion UI.
- When the run reaches a chapter gate, opening arc gate, final run gate, or user-requested strict review, use strict writer-room mode. If strict mode cannot be executed because reviewer tools are unavailable, explicitly downgrade the run to `single-context fallback` or `shared advisory only`; do not describe it as ideal writer-room reviewed.
- Run continuity review every three to five episodes.
- Run arc review at the end of each arc.
- Stop only for hard canon contradiction, user-level structural choice, missing locked roster/character decision, or scale/safety boundary.
- Never produce sixty thin episode summaries first and promise to enrich later.
- If the requested detail class is **thick chapter synopsis**, full-run mode still writes and reviews chapter batches. It may output one finished chapter at a time or a staged series of files, but it must not flatten the whole game into compact cards.
- If time/context pressure forces route-map density, label the result as a route map and do not update canon/graph as if it were a thick synopsis.

For thick chapter synopsis output, prefer producing one accepted chapter file after all of that chapter's episodes pass. If an episode fails a gate, fix that episode before assembling the chapter; do not add a later "chapter patch" as the expected workflow.

## Ledgers

Maintain rolling ledgers:

- `episode_state_ledger`
- `roster_exposure_ledger`
- `quote_scene_usage_ledger`
- `relationship_heat_ledger`
- `protagonist_arc_ledger`
- `protagonist_memory_ledger`
- `branch_debt_ledger`
- `enemy_gain_ledger`
- `emotion_object_ledger`
- `daily_life_tone_ledger`
- `production_layer_split_ledger`
- `real_world_testimony_ledger`
- `meta_boundary_ledger`
- `regression_ticket_ledger`
- `unresolved_issue_ledger`
- `open_questions_ledger`
- `experience_gate_ledger`
- `opening_arc_review_ledger`
- `fable_review_ledger`
- `source_absorption_ledger`

The project-side template files are:

- `docs/superpowers/specs/2026-07-02-chao-gag-episode-loop-writing-workflow.md`
- `docs/superpowers/specs/data/story/episode_loop_workflow_phases_v0_1.tsv`
- `docs/superpowers/specs/data/story/episode_loop_gate_checklist_v0_1.tsv`
- `docs/superpowers/specs/data/story/episode_loop_ledger_schema_v0_1.tsv`
- `docs/superpowers/specs/data/story/episode_loop_run_config_template_v0_1.tsv`
- `docs/superpowers/specs/data/story/episode_loop_episode_packet_template_v0_1.md`

V28 and later should prefer the v0.2 versions of those templates when present. The v0.2 templates add subagent writer-room recording, packet-first file layout, prefix review artifacts, and validator requirements.

## Output Shape

For each episode packet, include:

- Previous Episode Audit
- Next Episode Brief
- Context Pack
- Pipeline Pressure Board
- Episode Card
- Draft Synopsis
- Reader Synopsis when the user-facing task is judging story interest or continuous readability
- Production Split when the output will feed gameplay, art, scripts, or accepted packet revision
- Writer Room Review
- Fable Fixed Review Pass when enabled
- Patch Log
- Gate Result
- State Deltas
- Auto Next Brief

If the user asks for a readable final draft instead of packets, keep this structure internally and output a polished synopsis plus compact state notes.

When assembling a chapter from multiple accepted episode packets, include a compact chapter-level continuity note:

- Episodes included:
- Rolling state at chapter start:
- Rolling state at chapter end:
- Relationship debts carried forward:
- Protagonist arc deltas:
- Roster/IP exposures consumed:
- Enemy gains carried forward:
- Prefix review result:
- Opening arc review result when C01-C03 are in scope:
- Regression tickets opened/closed:
- Unresolved issues carried forward:
- Open canon/candidate decisions:

For thick chapter synopsis output, use project-native headings:

- Function / 本话功能
- Story Flow / 剧情流程
- Battle and Gameplay / 战斗与玩法
- Production Split / 制作拆分
- Mecha Appearance / 机体出场
- Heat / Spectacle / Gag / 燃点 / 爽点 / 梗点
- Emotion / 泪点 or 情绪物件
- Real-world Testimony / 真实证词 or 现实共鸣
- Relationship / 感情线
- Protagonist Arc / 主角团成长
- Branches and Debt / 分支与债务
- Clear State / 通关结算
