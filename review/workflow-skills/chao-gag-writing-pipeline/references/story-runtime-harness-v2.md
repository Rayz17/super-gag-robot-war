# Story Runtime Harness v2.2

For any chapter or episode whose correct writing depends on Current Canon,
series structure, mecha lifecycle, character arcs, prior story state, or broad
creative material, compile a Story Runtime v2.2 production pack before drafting.

The project method authority is:

`docs/superpowers/specs/2026-07-29-chao-gag-story-runtime-harness-v2.md`

## Mandatory interface

1. Rebuild and check the isolated project Vault when Canon or series support
   tables changed.
2. Compile the chapter request with
   `scripts/compile_story_runtime_context_pack.py`.
3. Pass `scripts/check_story_runtime_harness.py` before writing.
4. The writer reads only the stable writer context, chapter director board,
   current episode card, and prior episode state delta. Raw retrieval packs stay
   backstage.
5. Apply
   `docs/superpowers/specs/story-runtime/production/production_source_policy_v1.tsv`.
   Current facts may enter as short scene facts. Candidate Support and creative
   material are hidden by default and require explicit record-id admission after
   the lead writer chooses the scene direction. History, old Readers, effect
   tests, negative examples, and reviews never enter the first-draft context.
6. Decide whether the episode fits one reliable model interaction. Do not use
   the technical context/output ceiling as the creative capacity estimate.
7. For a long or dense episode, compile a scene-transaction run with
   `scripts/compile_story_runtime_episode_run.py`. Each transaction must be a
   complete dramatic scene or battle phase, not an arbitrary word chunk.
8. Use one lead writer sequentially. Assemble, write, locally review, and
   commit exactly one transaction before assembling its dependent successor.
   Never let several writers fill blank scene slots in parallel.
9. After every transaction, commit an exit-state receipt and a seven-dimension
   narrow review. A changed upstream commit invalidates all descendants and the
   episode assembly.
10. Mechanically assemble all committed transactions, run the whole-episode
   seam review, then seal the next-episode state.
11. Run strict episode and chapter receipts before user review. Do not promote
    accepted-looking prose to Canon without explicit user acceptance and Canon
    migration.

## Contract semantics

Contracts are not prose checklists. They are shared typed interfaces for the
writer, deterministic gates, semantic reviewers, and next-episode state
compiler:

- series alignment and chapter handoff;
- entity identity and mecha lifecycle;
- core character action obligations;
- new named-entity admission and exit.

The harness locks facts, lifecycle and outgoing state while leaving conflict,
scene invention, dialogue, humor, sexuality, emotion, battle reversal and
spectacle to the lead writer. A stronger idea that changes a contract must
amend and recompile the request rather than silently changing the Reader.

## Context discipline

Keep the Creative First v2 writer kernel and chapter contracts byte-identical
throughout a chapter for prefix-cache reuse. The retired v1 kernel is
regression evidence, not a writer source. An interaction package is:

- chapter stable prefix;
- episode stable prefix;
- current transaction card, compact contract slice, and bounded local retrieval;
- committed entry state, necessary prior receipts, a short prose tail, and an
  optional revision note.

Local retrieval may be broad; only compiled contracts and a bounded digest
enter the model context. Every context is content addressed. The complete
interaction toolchain/schema hashes and Current/Support retrieval-corpus hashes
participate in cache validation.

Only `contexts/` is reproducible cache. Drafts, state receipts, semantic
reviews, episode seals, and `history/` are production evidence. Use
`scripts/prune_story_runtime_interaction_cache.py` in dry-run mode first; only
`--apply` may remove unreferenced contexts.

The minimum transaction must close its local objective, opposition, turn, and
exit state. If it cannot fit the safe output range, revise the scene plan before
writing. The model must not improvise a cutoff and hope the next call repairs
it.

Deterministic scripts never certify that a story is interesting, human, sexy,
funny or emotionally effective. They certify identity, lifecycle, state,
budget, source and receipt integrity. Those qualitative questions require
independent semantic review and the user's judgment.
