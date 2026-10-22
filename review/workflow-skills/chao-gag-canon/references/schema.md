# Canon TSV Schema

Use stable IDs. Prefer editing existing rows over creating near-duplicates.

## entities.tsv

- `entity_id`: Stable ID, such as `CH036`, `R07`, `ORG_DAIGE`, `MECHA_GUARDIAN_Z`.
- `type`: `character`, `roster_package`, `faction`, `mecha`, `location`, or `concept`.
- `canonical_name`: Display name.
- `aliases`: Semicolon-separated lookup aliases.
- `source_group_id`: Parent roster/faction/group where useful.
- `status`: `core`, `secret`, `late_mystery`, `deprecated`, or `draft`.
- `role`: Short project role.
- `first_foreshadow`: Earliest scene where hints are allowed.
- `first_formal_appearance`: Earliest scene where the entity can be clearly introduced.
- `first_battle_join`: Earliest scene where the entity can join as a unit.
- `implementation_policy`: Binding implementation note.
- `notes`: Short design rationale.

## scenes.tsv

- `scene_id`: Stable scene/beat ID.
- `chapter`, `episode`: Story placement.
- `title`, `kind`, `location`: Human-readable scene metadata.
- `required_entities`: Semicolon-separated entity IDs that must be present.
- `optional_entities`: Entity IDs that may appear.
- `allowed_new_entities`: Entity IDs that may be introduced here.
- `unlocks`: Flags or concepts unlocked by this scene.
- `next_scene`: Primary next beat.
- `source_refs`: Existing document or code source.
- `notes`: Design intent.

## runtime_rules.tsv

- `rule_id`: Stable rule ID.
- `severity`: `P0`, `P1`, `P2`, or `P3`.
- `entity_id`, `entity_name`: Rule target.
- `implementation_key`: Code-facing key such as a Godot unit id or hotspot id.
- `scope`: Chapter/episode/implementation scope.
- `rule_type`: Example: `initial_roster`, `initial_hotspot`, `forbidden_phrase`.
- `forbidden_file`: File or directory to scan, relative to project root.
- `forbidden_regex`: Python regular expression used by `canon-check-godot.sh`.
- `allowed_from_scene`: Scene where the forbidden pattern becomes valid or the rationale target.
- `message`: Human-readable violation message.

## gag_hooks.tsv

- `hook_id`: Stable hook or interaction ID.
- `entity_id`: Main entity.
- `related_entities`: Semicolon-separated related entities.
- `first_allowed_scene`: Earliest allowed use.
- `category`: Gag or interaction class.
- `setup`: Setup line or situation.
- `payoff`: Payoff or downstream use.
- `implementation_note`: Constraints for scripts/art/code.
