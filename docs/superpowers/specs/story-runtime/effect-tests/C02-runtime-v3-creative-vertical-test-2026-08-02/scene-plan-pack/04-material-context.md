# 定向素材上下文

### 拼装诸侯会 (`H07`)

- 权威：working
- 分数：1005.005
- 来源：docs/superpowers/specs/story-runtime/generated/runtime_corpus.jsonl

```json
{
  "art_asset_hint": "限定盒堆;促销牌;授权章",
  "c01_map_signal": "C01模型街暗示",
  "display_anchor": "厂商展柜;限定版样件;价格标签;说明书",
  "first_major_unlock": "C02;C08",
  "notes": "商品化不能单一反派化，要既有爱也有生意。",
  "package_id": "H07",
  "package_name": "拼装诸侯会",
  "physical_scale": "模型/商品柜",
  "primary_zone_id": "WEZ_L1_03_MODEL_TOY_STREET",
  "secondary_zone_ids": "WEZ_L1_05_COURAGE_COMPLIANCE_TOOLS",
  "terminal_filter": "model_company;commerce;love"
}
```

### 木桶街后巷 (`H08`)

- 权威：working
- 分数：1005.005
- 来源：docs/superpowers/specs/story-runtime/generated/runtime_corpus.jsonl

```json
{
  "art_asset_hint": "手绘街图;街坊照片",
  "c01_map_signal": "C01留言墙轻触",
  "display_anchor": "小镇街坊留言;旧玩具维修摊照片",
  "first_major_unlock": "C02",
  "notes": "给模型圣地生活感，不只是商店菜单。",
  "package_id": "H08",
  "package_name": "木桶街后巷",
  "physical_scale": "生活档案/后巷地图",
  "primary_zone_id": "WEZ_L1_06_MESSAGE_COMMONS",
  "secondary_zone_ids": "WEZ_L1_03_MODEL_TOY_STREET",
  "terminal_filter": "town_life;daily;sidequest"
}
```

### 万机馆主循环磁流散热转子 (`MECHA_WANJI_MAIN_CIRCULATION_ROTOR`)

- 权威：working
- 分数：1005.005
- 来源：docs/superpowers/specs/story-runtime/generated/runtime_corpus.jsonl

```json
{
  "aliases": "主循环转子;巨型转子;展舰散热转子",
  "canonical_name": "万机馆主循环磁流散热转子",
  "entity_id": "MECHA_WANJI_MAIN_CIRCULATION_ROTOR",
  "first_battle_join": "V359-C02E01-CREATIVE",
  "first_foreshadow": "V359-C02E01-CREATIVE",
  "first_formal_appearance": "V359-C02E01-CREATIVE",
  "implementation_policy": "它是场景巨构和任务载荷，不是人格机体、不计参战；模型批次与维修史只能帮助辨认版本和适配方法，真正安装仍需全尺寸实物与工程复核。安装只恢复有限航行，不解决永久外泊、校正和保险。",
  "notes": "正式资产应突出巨大转子、运输架、吊装和万机馆检修窗，不制作密集内部机构动画；精确尺寸、重量和安装动作由C02预生产确定。",
  "role": "C02使万机馆恢复有限航行的全尺寸工业总成，必须由重型运输和吊装设备搬运，不能退化成手掌大的密封件",
  "source_group_id": "MUSEUM",
  "status": "needs_review",
  "type": "scene_mecha"
}
```

### 玩家模型机“无牌一号” (`V353U071`)

- 权威：candidate_support
- 分数：1005.005
- 来源：docs/superpowers/specs/story-runtime/generated/support/support_runtime_corpus.jsonl

```json
{
  "asset_capacity_risk": "standard_32;build_custom;尺寸泊位驾驶员仍需结算",
  "candidate_macro_window": "A-G",
  "candidate_terminal_action": "把模型改件同构制造成可追责实机模块",
  "counting_rule": "one_playable_collection_record",
  "current_state": "creative_working_visible_or_controlled",
  "display_name": "玩家模型机“无牌一号”",
  "earliest_story_dependency": "无牌一号改装来源与主体关系",
  "history_slot_policy": "C02 / C02竞技临时 / 四链登记后以全尺寸模块竞赛实机加入；仅作旧生命周期证据，不锁新章序",
  "lifecycle_mandate": "认名/首见 -> 首控或实质支援 -> 作品级关系困局 -> 身体/阵营/能力改变 -> 离队/独立站位 -> 不可替代终局回援",
  "mainline_visibility": "must_be_mainline_visible",
  "package_uid": "PK_GUEST_BUILD_ARENA",
  "playability_requirement": "representative_route_playable",
  "source_anchor": "Gundam Build/玩家改件",
  "source_ref": "v35_3_playable_roster_expansion_v35_3.tsv",
  "status": "candidate_lifecycle_inventory_v1",
  "unit_id": "V353U071"
}
```

### 玩家模型机“无牌一号” (`V353U071`)

- 权威：working
- 分数：1004.038
- 来源：docs/superpowers/specs/story-runtime/generated/runtime_corpus.jsonl

```json
{
  "aliases": "无牌一号;全尺寸改件竞技实机",
  "canonical_name": "玩家模型机“无牌一号”",
  "entity_id": "V353U071",
  "first_battle_join": "V359-C02E01-CREATIVE",
  "first_foreshadow": "V359-C02E01-CREATIVE",
  "first_formal_appearance": "V359-C02E01-CREATIVE",
  "implementation_policy": "木桶街原有全尺寸模块竞赛底盘和低权限竞赛AI；缩尺模型只提供改件同构数据，不会放大成机体。它在C02首控，V359-C03E04-CREATIVE经正常运输取得随舰构筑席；首个作业模块由C03 L4确定。",
  "notes": "内部锚Gundam Build与模型竞技；名称可由玩家改，不共享社勇王许可。",
  "role": "自由改装、零件兼容和玩家构筑单位",
  "source_group_id": "PK_GUEST_BUILD_ARENA",
  "status": "needs_review",
  "type": "mecha"
}
```

### 拼装战场 (`PK_GUEST_BUILD_ARENA`)

- 权威：candidate_support
- 分数：1000.0
- 来源：docs/superpowers/specs/story-runtime/generated/support/support_runtime_corpus.jsonl

```json
{
  "damage_or_form_change": "模型锚只提供形态/关系信息，全尺寸模块必须工程制造；无牌一号可持续换装但保留主体连续",
  "driver_subject_mapping": "玩家代理/模型师驾驶员OPEN+无牌一号主体边界",
  "midcourse_change": "无牌一号的设计被平台包装成官方套件，玩家代理也要面对“我的改件是否等于机体自己的愿望”",
  "original_what_if": "玩家模型可以不变巨机仍影响实机；无牌一号可以拒绝玩家的最强配装而不是“叛变玩家”",
  "package_name": "拼装战场",
  "package_uid": "PK_GUEST_BUILD_ARENA",
  "positive_desire": "想把自己真的喜欢的零件、涂装和作品混成一台能打、能修、不需要版权证明爱的机体",
  "quote_scene_state": "Build系“我的机体是最强的”玩家口号和武器乱入作为爽点，不把混搭本身判成错",
  "record_ids": "V353U071",
  "representative_victory": "无牌一号在全尺寸竞技中通过玩家预先组装的不兼容模块变换三种战法，打赢只能复制一个完美配装的对手",
  "rivalry_relationship": "玩家构筑欲、模型师职业、无牌一号主体性和商品化平台形成直接的创作/所有关系",
  "source_ids": "FACT-08;GAME-06;PSM027",
  "status": "candidate_package_lifecycle_v1",
  "terminal_F_action": "玩家为无牌一号配出神座中最强自由换装形态，先享受构筑正收益",
  "terminal_G_action": "无牌一号主动卸下一件最贵/最强但卡住别人的配件，将同构模块让给另一台机"
}
```

### 万机初开 (`V359-C02E04-CREATIVE`)

- 权威：working
- 分数：15.355
- 来源：docs/superpowers/specs/story-runtime/generated/runtime_corpus.jsonl

```json
{
  "allowed_new_entities": "MECHA_UNRELEASED_TRANSFORM_SAMPLE;CONCEPT_C02_REPRODUCTION_OPEN_DAY",
  "chapter": "C02",
  "episode": "2-4",
  "kind": "creative_working_open_day_airship_boss",
  "location": "木桶街开放日内街/外环/城市空域/万机馆临时饭桌",
  "next_scene": "V359-C03E01-CREATIVE",
  "notes": "白鸢已肉身到场并完成第一次现场L1预演；七海仍只从本市封存中心远程参与，陆衡尚未正式登场。复产开放日建立最低一条复产线。清仓鲸拔起空测试架、折断馆守Z固定叉并攻击万机馆新转子；万机馆半幅转向、馆守Z地锚与机群共同迫降Boss。未发售样件自行解除工业测试架固定，玩家短时控制它取回旧控制器、爬上抓臂并打开检修口。白鸢临时登舰，转子与外泊架仍需工务城实装验证。",
  "optional_entities": "CH036;V353U049;ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN",
  "required_entities": "CH_JICUN;CH_QIHAI;N_BAIYUAN;CH_TANGJIAO;CH001;V353U001;V353U043;V353U044;V353U045;V353U046;V353U047;V353U048;V353U071;MECHA_UNRELEASED_TRANSFORM_SAMPLE;CONCEPT_C02_REPRODUCTION_OPEN_DAY",
  "scene_id": "V359-C02E04-CREATIVE",
  "source_refs": "docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35-C02四话拓扑恢复与Current-Canon迁移-2026-07-26.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C02/C02-完整剧情总纲.md",
  "title": "万机初开",
  "unlocks": "BAYUAN_TEMPORARY_PASSENGER;MODEL_STREET_REPRODUCTION_NETWORK;PUBLIC_PORT_TEST_GRANTED;ROUTE_PUBLIC_WORKS_CITY;GUARDIAN_FIXED_FORK_DESTROYED;WANJI_ROTOR_FIRST_BATTLE_LOAD"
}
```

### 天穹联装，我们共同造过的神 (`C19`)

- 权威：candidate_support
- 分数：14.505
- 来源：docs/superpowers/specs/story-runtime/generated/support/support_runtime_corpus.jsonl

```json
{
  "asset_scope": "全球装配环境+馆守Z后继臂主Rig+天穹共享模块；不新造独立OG旗舰",
  "authority_state": "candidate",
  "branch_topology": "读取BR04-LEGAL/BR04-BREAK形成不同停止席；模块内槽/外线H2；馆守Z新臂共享Rig小差分",
  "chapter_id": "C19",
  "chapter_title": "天穹联装，我们共同造过的神",
  "entry_state": "全相环进入倒计时；索引给出唯一可行神座式；各阵营既有真实模块也有退出条件；馆守Z单臂已无法承担联装接口",
  "irreversible_result": "各阵营交付最好模块并保留条件；神座式因C20窗口进入战时物理锁合，不是索引凭空制造",
  "line_collision": "L1-L7围绕二十七年共同工程、原创旗舰质量门、后继右臂和是否交给索引碰撞",
  "location_necessity": "天穹联装模块分散在城市、归航群、异文明盟友和历代机群，必须通过多地同时自愿交付与工程装配才能形成，不可在终局凭空出现",
  "macro_wave": "F_PREP",
  "next_chapter_engine": "全相环九相位与三个星际节点同时锁合，只剩一次战争窗口",
  "opponent_proactive_action": "断冠攻击三装配节点；沈砺争统一军令；阿德里安提供政治日落；罗莎琳提供可替换模块；河原真造争唯一轮廓",
  "part_id": "P6_共同工程与终局",
  "permanent_player_gain": "馆守Z完整后继右臂;神座式试运转;全球装配网;世界停止席",
  "primary_gameplay": "全球模块争夺/护送;巨构装配;馆守Z后继右臂首战;天穹联装多模块试运转",
  "protagonist_desire": "纪存要敢接受最强力量又为反驳留下物理位置；七海要组织带日落条款的世界联盟；白鸢要画不预知结果的开放装配计划",
  "protected_future_peak": "C20真胜利;C21物理退槽危机;C22万机殿开放解",
  "relationship_character_turn": "三主角共同制定可互相叫停总攻；唐胶/兜灯/陆衡与馆守Z共同选择后继臂；群像按独立事业交付模块",
  "roster_ip_first_arrivals": "天穹联装模块家族;馆守Z完整后继右臂;无独立OG旗舰空降",
  "roster_returns_upgrades": "三舰/地方/归航/工房/城市机群交付独立模块;馆守Z完成承力背架→代用臂架→后继臂三段生涯",
  "secondary_gameplay": "制造装配终阶;战略网络;多舰泊位;主体同意链",
  "source_authority": "ROOT-14; CW327/328/329; Roster Quality",
  "status": "candidate_master_board_v2",
  "suggested_episode_range": "4_episode_candidate",
  "world_reveal": "天穹共同工程早于索引；百相=局部多体载体，神座式=封闭拓扑，万机殿=开放运行法；政治日落有效但战时退槽未验证"
}
```
