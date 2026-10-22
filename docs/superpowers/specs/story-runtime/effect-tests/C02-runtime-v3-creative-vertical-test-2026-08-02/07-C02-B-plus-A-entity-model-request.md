# C02 B+A实体建模请求

```json
{
  "schema_version": 3,
  "request_id": "C02-BPLUS-A-ENTITY-20260802",
  "runtime_phase": "entity_model",
  "chapter": "C02",
  "scope_scene_ids": [
    "V359-C02E01-CREATIVE",
    "V359-C02E02-CREATIVE",
    "V359-C02E03-CREATIVE",
    "V359-C02E04-CREATIVE"
  ],
  "active_character_ids": [
    "CH_JICUN",
    "CH_TANGJIAO",
    "CH001",
    "CH002",
    "CH_QIHAI",
    "N_BAIYUAN",
    "CH036"
  ],
  "active_entity_ids": [
    "LOC_MODEL_STREET",
    "ORG_PLATFORM",
    "CONCEPT_C02_PLATFORM_EXECUTION_CHAIN",
    "MECHA_WANJI_MOBILE_CHASSIS",
    "V353U001",
    "MECHA_GUARDIAN_TOURING_ARM",
    "V353U043",
    "V353U044",
    "V353U045",
    "V353U046",
    "V353U047",
    "V353U048",
    "V353U049",
    "V353U071",
    "ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN",
    "ENEMY_C02_UNITY_RECLAIMER",
    "MECHA_WANJI_MAIN_CIRCULATION_ROTOR",
    "MECHA_OLDPARTS_LABOR_TEAM"
  ],
  "query_terms": [
    "C02当前出场边界与首次登场",
    "人物位置知识控制关系",
    "机体尺寸驾驶者控制权章末去向",
    "模型数据到全尺寸工程边界",
    "平台商品执行链权限",
    "C01到C03生命周期交接"
  ],
  "current_state_sources": [
    "docs/superpowers/specs/剧情梗概/V35.9/rebuild/handoff/C01-v3.1创作基线与C02继承包-v2.md",
    "docs/superpowers/specs/story-runtime/effect-tests/C02-runtime-v3-creative-vertical-test-2026-08-02/04-selected-B-plus-A-working-direction-v1.md",
    "docs/superpowers/specs/story-runtime/effect-tests/C02-runtime-v3-creative-vertical-test-2026-08-02/06-research-admission-v1.md"
  ],
  "admitted_layer_source_ids": [
    "CLS_C02_L4_OUTLINE",
    "CLS_C02_L4_CAUSALITY"
  ],
  "admitted_material_ids": [
    "V353U071",
    "PK_GUEST_BUILD_ARENA",
    "V353U048",
    "V353U049",
    "ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN",
    "V353U044",
    "V353U047",
    "H07",
    "H08",
    "MECHA_WANJI_MAIN_CIRCULATION_ROTOR"
  ],
  "max_material_items": 12,
  "selected_scene_chain": "B零点转子劫案为唯一母故事；A只提供E03的预定败位反转与百刃主动卸甲。四话只追踪同一套主转子从仓库到万机馆。",
  "proposed_new_entities": [
    {
      "display_name": "玛拉·瓦尔加 / Mara Varga",
      "chapter_function": "木桶街转子运输负责人、唐胶旧同行、旧拳王驾驶者",
      "why_existing_cannot_fill": "唐胶与兜灯必须保留随舰立场，豪司承担企业线；本地需要一个拥有生活、运输和拳王历史的人来主动发动劫案并承受街区后果",
      "lifecycle_or_exit": "C02结束后与旧拳王正式随舰；木桶街由原运输班维持地面节点。她成为长期B级驾驶员与模型街联系人，后续可在分舰或百机航路阶段回到地面带队",
      "asset_cost": "B级长期角色：一套半身立绘、一套旧拳王驾驶服差分；不新增个人机体或独立场景"
    }
  ]
}
```
