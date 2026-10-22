# Canon TSV Schema

This file defines the machine-readable canon tables used by `scripts/canon-query.sh`, `scripts/canon-smoke-test.sh`, and `scripts/canon-check-godot.sh`.

## General Rules

- TSV headers are binding. Add new columns only after updating scripts and this schema.
- Cell lists use semicolons, for example `CH001;MECHA_GUARDIAN_Z`.
- `entity_id`, `scene_id`, `rule_id`, `hook_id`, `lock_id`, and `link_id` must be stable IDs.
- Canon rows may point to prose or data documents in `notes`, but binding rules should be represented as table fields whenever possible.
- Gameplay systems and data-table roots may use `SYSTEM-DESIGN` in appearance fields when they are not scene-bound.
- Every row in a queryable Canon TSV must have exactly one matching row in `authority_manifest.tsv`.
- `status`, `kind`, and `asset_status` describe the source row; cross-table authority is decided by `authority_manifest.tsv`.
- Candidate and history rows must not be copied into a Hard/Working root character merely to make them easy to find.

## `authority_manifest.tsv`

Generated authority layer used by `scripts/canon-query.sh`.

| Column | Meaning |
| --- | --- |
| `record_type` | Table-neutral type such as `entity`, `scene`, `gag_hook`, `art_lock`, or `wanji_floor`. |
| `record_id` | Stable source-table ID. Unique together with `record_type`. |
| `canon_level` | `hard`, `working`, `candidate`, or `history`. |
| `lifecycle_status` | `active`, `candidate`, `history`, or `deprecated`. |
| `version_scope` | Version or design range in which the row is intended to operate. |
| `source_of_truth` | Source TSV that owns the content. |
| `supersedes` | IDs replaced by this record when the relation is explicit. |
| `last_confirmed` | Date of the latest authority audit or promotion. |
| `owner` | `canon`, `story`, `runtime`, or `art`. |
| `notes` | Short authority rationale, not story prose. |

Do not edit the generated file alone. Change source status or `authority_overrides.tsv`, then run `scripts/build_canon_authority_manifest.py`.

## `authority_overrides.tsv`

Human decisions that cannot be inferred safely from legacy row statuses. It uses the same authority columns as the manifest. An override must reference an existing `(record_type, record_id)` pair.

## `identity_links.tsv`

Explicit identity relationships between duplicated data layers.

| Column | Meaning |
| --- | --- |
| `link_id` | Stable relationship ID. |
| `left_entity_id` | Existing `entities.tsv` ID. |
| `relation` | Identity/lifecycle relation such as `same_unit_as`, `character_mecha_lifecycle_of`, `represented_by_package`, `deprecated_alias_of`, `part_of_package`, or `physical_core_combines_into`. |
| `right_entity_id` | Existing `entities.tsv` ID. |
| `scope` | Version range for the relationship. |
| `status` | Current relationship state. |
| `notes` | Why both IDs exist and which layer owns which concern. |

## `entities.tsv`

Canonical characters, factions, roster packages, mecha, locations, and core concepts.

Columns:

| Column | Meaning |
| --- | --- |
| `entity_id` | Stable ID, usually `CH###`, `R##`, `MECHA_*`, `LOC_*`, `ORG_*`, or `CONCEPT_*`. |
| `type` | Open controlled vocabulary including `character`, `faction`, `roster_package`, `mecha`, `mecha_candidate`, `location`, `concept`, and production bridge types already present in the table. New values require a schema note. |
| `canonical_name` | Canonical display name. |
| `aliases` | Semicolon-separated aliases and search terms. |
| `source_group_id` | Owning roster package, faction, project area, or concept group. |
| `status` | Legacy/source-row state. Current values include `core`, `canonical`, `story_first_migrated`, `needs_review`, `creative_candidate`, `draft`, `historical_runtime_reference`, and `deprecated_alias`. It does not replace `canon_level`. |
| `role` | Narrative, gameplay, or implementation role. |
| `first_foreshadow` | Earliest allowed foreshadowing scene, or `SYSTEM-DESIGN` for non-scene concepts. |
| `first_formal_appearance` | Earliest formal appearance/use, or `SYSTEM-DESIGN`. |
| `first_battle_join` | Earliest battle join/use; blank when not battle-bound. |
| `implementation_policy` | Binding implementation rule in plain language. |
| `notes` | Short rationale, source doc, or handoff note. |

## `scenes.tsv`

Canon chapter and episode beats, especially where runtime order matters.

Columns:

| Column | Meaning |
| --- | --- |
| `scene_id` | Stable beat ID. |
| `chapter` | Chapter ID such as `C01`. |
| `episode` | Episode or slice label. |
| `title` | Beat title. |
| `kind` | Scene/play mode vocabulary. It may include production-specific battle or candidate labels; historical/candidate meaning must also be represented in the authority manifest rather than inferred by readers. |
| `location` | Canon location. |
| `required_entities` | Semicolon-separated entity IDs that must be present. |
| `optional_entities` | Semicolon-separated entity IDs that may be present. |
| `allowed_new_entities` | Entities that may first appear or unlock here. |
| `unlocks` | Flags, flow gates, battle joins, or implementation state unlocked by the beat. |
| `next_scene` | Expected next beat. |
| `source_refs` | Primary implementation or source design file. |
| `notes` | Binding continuity note. |

## `scene_entity_presence.tsv`

Sparse authoritative overrides for how an entity exists in a scene. `scenes.tsv`
answers which entities a beat may need; this table distinguishes a body on site
from a live call, recording, work trace, deployed system, or explicit absence.
When no override exists, a character or mecha listed by the scene defaults to
`physical`.

Columns:

| Column | Meaning |
| --- | --- |
| `presence_id` | Stable presence record ID. |
| `scene_id` | Scene ID governed by this record. |
| `entity_id` | Entity whose presence is being specified. |
| `requirement` | `required`, `optional`, `required_trace`, or `forbidden`. |
| `presence_mode` | `physical`, `remote_live`, `recording`, `work_trace`, `mentioned`, `system_effect`, or `not_present`. |
| `lifecycle_claim` | First foreshadow, formal appearance, first physical arrival, continued presence, or another explicit lifecycle statement. |
| `scene_function` | What the entity or trace contributes to the scene. |
| `control_state` | What it can actually control in this scene. |
| `knowledge_state` | What it can reasonably know in this scene. |
| `entry_state` | State on entering the scene. |
| `exit_state` | State after the scene. |
| `source_refs` | Current sources supporting the presence fact. |
| `status` | `working`, `candidate`, or `history`. |
| `notes` | Misread guards and migration notes. |

## `wanji_floors.tsv`

Canonical multi-layer floor anchor for 万机馆. Use before writing maps, art briefs, exploration routes, battle layouts, or deep-dive entrances.

Columns:

| Column | Meaning |
| --- | --- |
| `floor_id` | Stable floor ID such as `WF_L1`, `WF_B1`, or `WF_B2`. |
| `canonical_name` | Canonical floor display name. |
| `layer_type` | Functional layer category, such as `public_floor`, `mezzanine`, `service_floor`, or `sealed_depth`. |
| `relative_position` | Position in the building, for example ground floor, mezzanine, or underground level. |
| `approx_scale` | Approximate size or scale cues for script, map, and art alignment. |
| `c01_access_state` | Access state during Chapter 1. |
| `public_function` | In-world public, staff, or hidden function. |
| `later_unlocks` | Later story or gameplay unlocks tied to this floor. |
| `gameplay_uses` | Exploration, battle, management, deep-dive, or presentation uses. |
| `art_anchor` | Visual anchors that should guide asset briefs. |
| `notes` | Binding continuity note. |

## `wanji_locations.tsv`

Canonical per-floor location and connection anchor for 万机馆. Use before adding rooms, moving characters, staging dialogue, defining encounter maps, or placing interactables.

Columns:

| Column | Meaning |
| --- | --- |
| `location_id` | Stable location ID such as `WL_L1_MAIN_HALL`. |
| `parent_floor_id` | Floor ID from `wanji_floors.tsv`. |
| `parent_location_id` | Parent location or related canonical entity ID. |
| `canonical_name` | Canonical display name. |
| `area_type` | Location category, such as `main_hall`, `exhibit_island`, `maintenance_zone`, or `sealed_gate`. |
| `c01_access_state` | Access state during Chapter 1. |
| `approx_position` | Relative position on the floor. |
| `connected_locations` | Semicolon-separated connected location IDs. |
| `first_scene` | Earliest scene where the space can be seen, used, or referenced. |
| `gameplay_use` | Intended interaction, battle, investigation, or management use. |
| `art_scale_anchor` | Concrete scale and visual requirements for art or map assets. |
| `notes` | Binding continuity note, including exclusions and staging rules. |

## `wanji_exhibition_zones.tsv`

Canonical exhibition-zone table for the public and semi-public 万机馆 display layer. Use before writing museum scenes, art briefs, floor plans, asset prompts, roster foreshadowing, or route maps.

Columns:

| Column | Meaning |
| --- | --- |
| `zone_id` | Stable zone ID such as `WEZ_L1_01_GUARDIAN_ATRIUM`. |
| `canonical_name` | Canonical display name for the zone. |
| `floor_band` | Floor or spatial band where the zone belongs: `L1`, `L2`, `L3`, `B1`, `B2`, or `EXT`. |
| `map_code` | Short map code for floor-plan labels and art briefs. |
| `map_position` | Relative position inside the floor or exterior. |
| `approx_scale` | Size and scale cue for floor plans, scene staging, and art. |
| `c01_access_state` | Visibility and access state in Chapter 1. |
| `roster_coverage` | Roster packages, hidden packages, or museum concepts visibly covered by this zone. |
| `signature_displays` | Iconic displays, objects, and interactables that should appear in maps or scene art. |
| `visual_density` | Intended density cue such as `medium`, `high`, or `very_high`. |
| `art_brief` | Binding visual instruction for asset sessions. |
| `scene_use` | Story, exploration, battle, or foreshadowing use. |
| `terminal_map_layer` | Archive-terminal map layers where this zone should appear. |
| `notes` | Binding continuity note. |

## `wanji_roster_zone_coverage.tsv`

Canonical mapping between playable roster packages and 万机馆 exhibition zones. Use before adding roster foreshadowing, exhibit props, hidden conditions, art prompts, or early story mentions.

Columns:

| Column | Meaning |
| --- | --- |
| `package_id` | Roster package ID such as `R01`, `S05`, or `H09`. |
| `package_name` | Canonical roster package name. |
| `primary_zone_id` | Primary exhibition-zone anchor from `wanji_exhibition_zones.tsv`. |
| `secondary_zone_ids` | Semicolon-separated secondary zone anchors. |
| `display_anchor` | What the player sees first in the museum. |
| `physical_scale` | Whether the anchor is a model, cockpit, real body, module, core, or external unit. |
| `c01_map_signal` | How much the package can be seen on the Chapter 1 map or route. |
| `first_major_unlock` | First chapter or scene where the package meaningfully unlocks. |
| `terminal_filter` | Archive-terminal filter tags. |
| `art_asset_hint` | Concrete assets or motifs that should appear in visual production. |
| `notes` | Binding continuity note. |

## `wanji_collection_taxonomy.tsv`

Canonical relationship table between 万机馆 exhibits/collections and playable roster lineages. Use before adding exhibit islands, museum collections, model/toy callbacks, black-box cores, or roster foreshadowing.

Columns:

| Column | Meaning |
| --- | --- |
| `collection_id` | Stable collection anchor ID, usually `WCT_*`. |
| `canonical_name` | Canonical display name for the exhibit or collection anchor. |
| `relation_type` | How the collection connects to units, such as `prototype_anchor`, `physical_body`, `core_echo`, `hobby_artifact`, or `archive_evidence`. |
| `display_form` | What the player sees in the museum: model, toy, cockpit, real body, black box, archive, or mixed display. |
| `linked_roster_packages` | Semicolon-separated roster packages or hidden packages foreshadowed or supported by this anchor. |
| `linked_unit_examples` | Representative units or mecha names connected to the anchor. |
| `size_class` | Size cue for art and staging, such as `DESK_TO_SMALL`, `SMALL_0_2M`, `MEDIUM_2_12M`, `SUPER_15_30M`, or `NO_FIXED_SIZE`. |
| `c01_visibility` | Whether this anchor is open, visible, limited, locked, or sealed in Chapter 1. |
| `story_function` | Narrative purpose: affection, foreshadowing, evidence, repair, mystery, or chapter payoff. |
| `gameplay_use` | Gameplay uses such as support, repair, hidden condition, say/get proof, management, or deep dive. |
| `activation_rule` | Required story, relation, repair, or data condition before the anchor can affect battle or roster state. |
| `storage_or_berth_rule` | Where the object lives and whether it can become a battle unit, support, projection, or external join. |
| `notes` | Binding continuity note, especially what the anchor must not imply. |

## `wanji_carrier_berths.tsv`

Canonical carrier capacity table for 万机馆 after it becomes a 流亡展舰. Use before saying a unit is stored on board, launched from the museum, externally docked, or only present as a resonance core.

Columns:

| Column | Meaning |
| --- | --- |
| `berth_id` | Stable berth or storage rule ID, usually `WCB_*`. |
| `canonical_name` | Canonical berth/facility display name. |
| `parent_location_id` | Related location in `wanji_locations.tsv`. |
| `capacity_type` | Facility type, such as `public_display`, `internal_hangar`, `medium_berth`, `heavy_service`, `external_berth`, `allied_carrier`, `resonance_storage`, or `soft_dock`. |
| `size_range` | Unit size or information scale this berth can reasonably host. |
| `can_host` | Semicolon-separated examples or categories the berth can host. |
| `cannot_host` | Categories the berth must not be used for. |
| `c01_state` | Availability state in Chapter 1. |
| `story_unlock` | Scene or chapter gate where the berth becomes visible or usable. |
| `gameplay_use` | Launch, repair, support, management, deep dive, or command use. |
| `art_scale_anchor` | Concrete scale and visual requirements for art or map assets. |
| `notes` | Binding continuity note, including capacity limits and exclusions. |

## `jicun_archive_terminal_views.tsv`

Canonical table for 纪存档案终端 views. This replaces the low-tech “handwritten notebook” reading: the terminal is the player-facing information layer for maps, clues, duties, roster overlays, collection links, berth status, and late-game archive anomalies.

Columns:

| Column | Meaning |
| --- | --- |
| `view_id` | Stable view ID such as `JTV_EXHIBITION_ZONES`. |
| `display_name` | Canonical UI display name. |
| `ui_mode` | View mode such as `map`, `map_overlay`, `filter`, `network`, `status`, `route`, `damage_overlay`, `signal`, `roster`, or `anomaly`. |
| `first_scene` | Earliest scene where the view can appear or be foreshadowed. |
| `source_tables` | Semicolon-separated source tables used by the view. |
| `player_use` | What the player learns or does with this view. |
| `map_expression` | How the view should look or behave in the map/UI. |
| `writing_rule` | Binding script rule for using the terminal in dialogue or narration. |
| `visual_anchor` | UI or prop visual anchor for art briefs. |
| `notes` | Binding continuity note. |

## `character_mecha_art_locks.tsv`

Canonical lock table for project-level art direction, character, mecha, roster-package, collection-anchor, system-actor, and enemy-unit presentation. Use before writing character dialogue, assigning pilots, requesting portraits/mecha art, staging battle units, or resolving conflicts between story documents and the 美术资产 session.

This table does not replace `character_layer/pilot_cast.tsv`; it records the current hard locks, current references, known conflicts, and unresolved gaps that must be respected or fixed before production.

Columns:

| Column | Meaning |
| --- | --- |
| `lock_id` | Stable row ID, usually `CML###`. |
| `subject_id` | Project art-direction key, character, mecha, roster package, collection anchor, system actor, or enemy unit ID. May reference a future entity when `canon_entity_id` is blank. |
| `subject_type` | `project_art_direction`, `character`, `character_group`, `character_ai`, `character_mecha`, `mecha`, `roster_package`, `collection_anchor`, `system_actor`, or `enemy_unit`. A project-level row locks shared rendering/production grammar only and must not replace subject-specific identity or lifecycle locks. |
| `canonical_name` | Canonical display name. |
| `canon_entity_id` | Matching `entities.tsv` ID when available; blank when the row is waiting for a canon entity. |
| `package_id` | Roster package, faction, or owning group such as `R01`, `R24`, `ORG_DAIGE`, or blank. |
| `gender_presentation` | Locked or pending gender/presentation rule. Use `待美术锁定` or similar when not fixed. |
| `age_band` | Age/scale band for writing and art, such as child, youth, adult, AI, or size class. |
| `pronouns_or_address` | Writing address and pronoun guidance. |
| `role_type` | Narrative/gameplay role. |
| `unit_or_mecha_link` | Linked unit, mecha, model, terminal, or gameplay object. |
| `personality_anchor` | Short personality and behavior anchor. |
| `wound_or_drive` | Core wound, fear, desire, or design pressure that should shape scenes. |
| `voice_rule` | Dialogue and action-writing rule. |
| `visual_lock` | Binding or pending visual direction. |
| `current_art_reference` | Current local art-session reference path when one exists. |
| `asset_status` | `locked_current`, `current_reference`, `conflict_resolved`, `needs_art_lock`, `needs_redesign`, `no_art_yet`, `contract_locked`, `direction_locked`, or similar explicit state. |
| `story_gate` | Earliest or most important story gate where the row matters. |
| `must_not` | Forbidden flattening, legal/copyright risk, or continuity trap. |
| `source_refs` | Semicolon-separated source documents, data tables, or art-session pages. |
| `notes` | Binding note or next action. |

## `runtime_rules.tsv`

Rules that can be scanned against implementation files.

Columns:

| Column | Meaning |
| --- | --- |
| `rule_id` | Stable rule ID. |
| `severity` | `P0`, `P1`, `P2`, or `P3`. |
| `entity_id` | Related canon entity. |
| `entity_name` | Display name for reports. |
| `implementation_key` | Search/implementation key. |
| `scope` | Scene, chapter, or runtime area. |
| `rule_type` | Rule category such as `initial_roster`, `initial_hotspot`, or `forbidden_phrase`. |
| `forbidden_file` | File or directory scanned by the checker. |
| `forbidden_regex` | Python regular expression that identifies a violation. |
| `allowed_from_scene` | Scene or rule gate where the forbidden pattern becomes valid. |
| `message` | Human-readable violation message. |

## `gag_hooks.tsv`

Reusable gag, relationship, and payoff hooks.

Columns:

| Column | Meaning |
| --- | --- |
| `hook_id` | Stable hook ID. |
| `entity_id` | Primary entity ID. |
| `related_entities` | Semicolon-separated related entity IDs. |
| `first_allowed_scene` | Earliest scene where the hook may be used. |
| `category` | Hook category. |
| `setup` | Setup pattern. |
| `payoff` | Payoff or gameplay result. |
| `implementation_note` | Boundary for scripts or implementation. |
