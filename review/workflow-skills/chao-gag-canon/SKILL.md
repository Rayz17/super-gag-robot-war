---
name: chao-gag-canon
description: Use when working in the 超GAG机器人大战 project on story, scripts, dialogue, characters, mecha, roster packages, art briefs, gameplay, Godot implementation, scene flow, or continuity. Query the project authority manifest before changes, keep Hard/Working/Candidate/History separate, and run Canon validation after migrations.
---

# Chao GAG Canon

## Purpose

Canon is the shared, living authority baseline for 《超GAG机器人大战》. It aligns sessions without freezing stronger ideas or treating every old draft as current truth.

This skill is a router and governance contract. Creative authorship belongs to `chao-gag-story-writer`; file/stage orchestration and accepted-state integration belong to `chao-gag-writing-pipeline`. Neither a context pack nor a production checklist decides the story for its author.

## Authority Model

Always distinguish four levels:

1. **Hard Canon**
   - User-confirmed identity, spatial/physical capacity, locked current art, accepted Runtime, and rules many sessions depend on.
   - Change only through an explicit migration with affected tables/docs updated and checks run.

2. **Working Canon**
   - Accepted current story or design direction.
   - It guides work now but may be migrated when a better dramatic, gameplay, or production solution appears.

3. **Candidate Canon**
   - Draft chapters, future beats, relationship scenes, 50-issue solutions, material-pool selections, art exploration, and unapproved mechanisms.
   - It may inspire work but cannot constrain other sessions until promoted.

4. **History**
   - Superseded drafts, deprecated aliases, old Runtime, and retained source material.
   - Use only for traceability or deliberate recovery of a proven high point.

The machine authority is:

`docs/superpowers/specs/data/canon/authority_manifest.tsv`

Do not infer cross-table authority from legacy `status`, scene `kind`, graph `status`, filename version, or prose saying “pass”.

## Required Entry Sequence

Before changing story, art, gameplay, or implementation:

1. Run `python3 scripts/report_v35_layered_pipeline.py --check` and read `docs/superpowers/specs/剧情梗概/V35六层创作生产看板.md`. Only its current active chapter may advance.
2. Read `docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md` for narrative migrations, user decisions, and historical state changes; it is not the machine stage authority.
3. For V35 chapter, outline, performance, Reader, or continuation work, first run the generated six-layer dashboard check, then read the matching `docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/Cxx-story-chain.tsv` and run `--next`. Apply `docs/superpowers/specs/2026-07-27-chao-gag-v35-production-gates-v2.md`: a downstream file with `missing`, `blocked`, or `invalidated` status is not a current creative source, and internal chapter review is not a substitute for user creative acceptance.
4. Query current Canon for the exact character, unit, location, chapter, scene, and rule involved.
5. If a chapter has a Current Canon Pack, verify its live source hashes and acceptance scope before using it. An invalidated pack is not current authority. Do not infer readiness from a cached chapter-specific statement in this skill.
6. Query Candidate only when deliberately selecting or reviewing unapproved material.
7. Query History only when tracing a conflict or recovering a specific earlier high point.
8. Query Design Graph explicitly for document ownership, dependencies, watchlists, and source discovery.
9. For drafting or substantial story review, use `chao-gag-story-writer` and `chao-gag-writing-pipeline` after this authority pass. Candidate exploration and formal integration are separate; only the latter changes sealed production artifacts.

## Query Commands

Run from the project root:

```bash
scripts/canon-query.sh 纪存
scripts/canon-query.sh entity CH_QIHAI
scripts/canon-query.sh scene V359-C03
scripts/canon-query.sh layout B1
```

Default mode is `current`: Hard + Working Canon only, with no Design Graph.

Use explicit layers:

```bash
scripts/canon-query.sh candidate C04
scripts/canon-query.sh candidate entity CONCEPT_JICUN_MACHINE_SOUL_LINK
scripts/canon-query.sh history scene V31-C01E03-BATTLE
scripts/canon-query.sh index C04
scripts/canon-query.sh audit C04
```

- `candidate`: Candidate Canon only.
- `history`: superseded/deprecated Canon; also searches historical graph rows when no section is specified.
- `all`: current plus candidate Canon, no history or graph by default.
- `index`: Design Graph only.
- `audit`: all Canon layers plus Design Graph. Never use this as a normal writing context dump.

If a broad query truncates, narrow by section or exact ID. Do not paste full `audit` output into a drafting context.

## Data Boundaries

### Root Canon

Use `docs/superpowers/specs/data/canon/` for stable identities, accepted/candidate scene continuity, Wanji spatial and collection anchors, runtime rules, art locks, hooks, and cross-layer identity links.

### Design Graph

Use `docs/superpowers/specs/data/design_graph/` for document ownership, dependencies, migrations, watchlists, scripts, and history. A graph node marked `canonical` is not automatically Hard Canon.

### Creative Material

IP research, famous scenes, quote anchors, what-if/regret cases, model/toy ecology, 50-issue solutions, daily-life pools, adult relationship material, branch craft, and writing workflow contracts are creative input. Select them through the writing pipeline and source-absorption ledgers; do not promote them into world entities merely for discoverability.

### Runtime and Art

Accepted story, current Runtime, and asset completion are separate states. A story can be Working while Runtime or art remains candidate; a contract can pass while story/audience quality fails. Never copy one layer's `pass` into another.

## Current Layer4 Boundary

Resolve current production state from the live dashboard, manifest and latest user decision, not from dates embedded in a Skill:

- C01, C02 and C03 current Readers have explicit user-acceptance receipts and may be used as formal previous context.
- C03's accepted story authority is its four pure-story Episode Readers and mechanically assembled chapter Reader. Its separate gameflow and open-information files remain Candidate production aids; they do not become character memory or later-story facts by default.
- Resolve the active chapter and NEXT from its live manifest. Consult the registered C04/C05 responsibility migration for their current division; do not restore superseded five-episode sources. A machine READY flag cannot override a later user rejection of the story.
- Resolve future-chapter locks from current registries and explicit user authorization. Do not infer permission to begin a chapter, game implementation or asset work from an upstream internal PASS.
- Any change to an accepted or sealed upstream artifact must use story-chain invalidation and regenerate all dependent stages. Never hand-edit a mechanical chapter Reader or cross-chapter bundle.

Current reading and decision sequence:

1. Direct accepted Readers: C01, C02, then `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C03-章节连续阅读稿.md`.
2. C03 acceptance evidence: `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C03/C03-用户创作验收回执.md`.
3. C04 current machine entry: `docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C04-story-chain.tsv`; run `--next` before work.
4. C03 gameflow/open-information files, C04/C05 old Readers and `C01-C05连续阅读稿-v3.md` are Candidate or History production references, never automatic story context.

Accepted first-part facts that must not drift:

- C01: Guardian Z is an 18 m one-armed playable guardian; its original right forearm remains destroyed. At this stage Wanji departs as a 130-160 m low touring carrier, not in humanoid or berserk form.
- C02: White Kite enters the story and boards for the trip to Works City. Model/toy repair records can anchor engineering and machine-soul recognition but do not directly enlarge into real mecha. The repaint aircraft remain locally operated support rather than permanent Wanji berths. Unbranded One and Old Boxer travel with Wanji; Cargo Leader takes the land route, is not mute, and retains later transforming-life story obligations.
- C03: Nanami boards as the onboard accident observer and investigator of misuse of her old signature; Lu Heng boards; White Kite and Hao Si/Social Brave King remain with the team; Guardian Z, Unbranded One and Old Boxer are aboard; Cargo Leader travels overland; Wanji departs for the Sky Forge Ring after the current request for help and Jicun's reply to the 27-year-old signal. These are accepted previous-context facts.

Do not restore superseded White Letter, three-load triage, 36-hour punishment, arm bridge, twelve Jicun slices, Perfect Jicun, root burning, calibration bodies in C04, Shen as the black-head pilot, paper-drawn reality control, or an early humanoid/beserk Wanji from History.

## Migration Workflow

When a stronger idea conflicts with current Canon:

1. Identify the exact Hard/Working rows and affected consumers.
2. State why the old rule fails dramatically, logically, physically, or in production.
3. Decide the new authority level and lifecycle.
4. Update source TSVs and, when needed, `authority_overrides.tsv`.
5. Update the production status page, chapter Current Canon Pack, handoff/state ledgers, art locks, and Design Graph entries affected by the change.
6. Preserve superseded material as History when it has traceability or reusable high points; do not leave two active truths.
7. Rebuild and validate the authority layer.

Required commands:

```bash
python3 scripts/build_canon_authority_manifest.py
python3 scripts/check_canon_authority.py
scripts/canon-smoke-test.sh
```

For active V35 chapter production also run the matching story-chain target:

```bash
python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/Cxx-story-chain.tsv
```

For Godot/runtime changes also run:

```bash
scripts/canon-check-godot.sh --report
scripts/canon-check-godot.sh --strict
```

## Non-Negotiable Practices

- Do not copy unapproved chapter outcomes into core character rows.
- Do not restore a historical scene because a broad search found it first.
- Do not count character, package, and lifecycle IDs as separate units when `identity_links.tsv` says they are one subject.
- Do not let model boxes, labels, frames, props, or workflow concepts replace actual mecha, character actions, or playable stakes.
- Do not use Canon compliance to defend a dull, tiny, repetitive, or unreadable draft. Propose a migration.
- Do not update only prose. Keep machine tables, graph pointers, packs, and checks aligned.

## Reference

- Canon architecture and commands: `docs/superpowers/specs/data/canon/README.md`
- TSV schema: `docs/superpowers/specs/data/canon/references/schema.md`
- Stabilization rationale: `docs/superpowers/specs/2026-07-18-chao-gag-canon-authority-stabilization-v1.md`
- V35.9 rebuild navigation: `docs/superpowers/specs/剧情梗概/V35.9/rebuild/README.md`

If a required file or authority row is missing, stop treating the result as confirmed Canon. Record the gap, use the safest current source, and repair the authority layer before claiming alignment.
