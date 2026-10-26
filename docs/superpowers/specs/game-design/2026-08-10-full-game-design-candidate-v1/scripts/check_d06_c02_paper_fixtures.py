#!/usr/bin/env python3
"""Static integrity check for the three D06 C02 paper fixtures.

This checker proves only document/registry/source-byte consistency.  It does
not run a resolver, search strategy space, or provide human gameplay evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
PROJECT = PACKAGE.parents[4]
DOC = PACKAGE / "validation/d06-c02e04-e05-paper-fixtures-v0.1.md"
REGISTRY = PACKAGE / "data/opening-chapter-paper-fixture-registry.tsv"
BINDINGS = PACKAGE / "data/opening-accepted-story-bindings.tsv"
TRACE = PACKAGE / "data/opening-state-transaction-paper-trace.tsv"
STORY_SEEDS = PACKAGE / "chapters/c01-c03-story-state-seeds.tsv"
EQUIPMENT_LEDGER = PACKAGE / "data/c02-paper-equipment-state-ledger.tsv"
ACTION_LEDGER = PACKAGE / "data/c02-action-authority-consent-paper-ledger.tsv"

REQUIRED_FIXTURES = {
    "FX-D06-C02E04-MATCH",
    "FX-D06-C02E04-ACCIDENT-CP",
    "FX-D06-C02E05-RESCUE-CLEAR",
}
REQUIRED_TERMINALS = {"clear", "partial", "withdraw", "fail_continue"}
FIXED_EXIT_TOKENS = {
    "FX-D06-C02E04-MATCH": {"3:2", "全装", "右臂"},
    "FX-D06-C02E04-ACCIDENT-CP": {"内环", "全装", "断电", "临海外缘", "牵引"},
    "FX-D06-C02E05-RESCUE-CLEAR": {"3:2", "拆解架", "停止下沉", "原主", "右臂"},
}
EXPECTED_TRACE_IDS = {
    "FX-D06-C02E04-MATCH": "OST-04",
    "FX-D06-C02E04-ACCIDENT-CP": "OST-05",
    "FX-D06-C02E05-RESCUE-CLEAR": "OST-06",
}
EXPECTED_STORY_SEED_GUARDS = {
    "FX-D06-C02E04-MATCH": "C02E04_END:tournament_projection",
    "FX-D06-C02E04-ACCIDENT-CP": "C02E04_END:accident_checkpoint_projection",
    "FX-D06-C02E05-RESCUE-CLEAR": "C02E05_END:accident_clear_projection",
}
EXPECTED_STATE_DOMAINS = {
    "FX-D06-C02E04-MATCH": {
        "ST_RESULT",
        "ST_BODY",
        "ST_LOCATION",
        "ST_EQUIPMENT",
        "ST_OPERATION",
        "ST_RELATION",
        "ST_ENEMY_LEARNING",
    },
    "FX-D06-C02E04-ACCIDENT-CP": {
        "ST_BODY",
        "ST_LOCATION",
        "ST_EQUIPMENT",
        "ST_KNOWLEDGE",
        "ST_RESOURCE",
        "ST_CONSENT",
        "ST_RESULT",
        "ST_OPERATION",
    },
    "FX-D06-C02E05-RESCUE-CLEAR": {
        "ST_BODY",
        "ST_LOCATION",
        "ST_EQUIPMENT",
        "ST_RESOURCE",
        "ST_KNOWLEDGE",
        "ST_AUTHORITY",
        "ST_CONSENT",
        "ST_RESULT",
        "ST_OPERATION",
    },
}
EXPECTED_RECOMPUTE_LEVELS = {
    "FX-D06-C02E04-MATCH": "static_contract_plus_match_4_contact_equations",
    "FX-D06-C02E04-ACCIDENT-CP": "static_contract_only",
    "FX-D06-C02E05-RESCUE-CLEAR": "static_contract_only",
}
EXPECTED_EQUIPMENT_IDS = {
    "EQ_WANJI_LATERAL_THRUSTER_01",
    "EQ_FK_BACK_CANNON_01",
    "EQ_FK_LONG_WING_SET_01",
    "EQ_FK_SHIELD_SET_01",
    "EQ_FK_DRILL_SET_01",
    "EQ_FK_CROWN_01",
}
EQUIPMENT_REQUIRED_FIELDS = (
    "story_binding_id",
    "state_domain",
    "owner_group",
    "owner_id",
    "owner_version",
    "match_initial_custody",
    "match_initial_installed_state",
    "match_initial_condition",
    "tournament_clear_custody",
    "tournament_clear_installed_state",
    "tournament_clear_condition",
    "e04_checkpoint_custody",
    "e04_checkpoint_installed_state",
    "e04_checkpoint_condition",
    "e05_accident_clear_custody",
    "e05_accident_clear_installed_state",
    "e05_accident_clear_condition",
    "build_status",
    "human_evidence_status",
    "authority_boundary",
    "status",
)
EXPECTED_REQUEST_WINDOWS = {
    "REQ_C02E04_DRONE_HAZARD_SCAN": ("FX-D06-C02E04-ACCIDENT-CP", "A-W1"),
    "REQ_C02E04_JACK_EVAC_COVER": ("FX-D06-C02E04-ACCIDENT-CP", "A-W2"),
    "REQ_C02E04_CARGO_EDGE_TOW": ("FX-D06-C02E04-ACCIDENT-CP", "A-W3"),
    "REQ_C02E05_RED_RING_SCAN": ("FX-D06-C02E05-RESCUE-CLEAR", "PA-W1"),
    "REQ_C02E05_BLUE_ENGINEERING_COVER": ("FX-D06-C02E05-RESCUE-CLEAR", "PA-W2"),
    "REQ_C02E05_JACK_ENGINEERING_ESCORT": ("FX-D06-C02E05-RESCUE-CLEAR", "PA-W2"),
    "REQ_C02E05_YELLOW_BRACKET_CUT": ("FX-D06-C02E05-RESCUE-CLEAR", "PA-W4"),
    "REQ_C02E05_CARGO_WANJI_TOW": ("FX-D06-C02E05-RESCUE-CLEAR", "PB-W1"),
    "REQ_C02E05_GUARDIAN_BRIDGE_BRACE": ("FX-D06-C02E05-RESCUE-CLEAR", "PB-W2"),
    "REQ_C02E05_OLD_BOXER_CLEAR_LOAD": ("FX-D06-C02E05-RESCUE-CLEAR", "PB-W2"),
    "REQ_C02E05_FULL_KING_SELF_DETACH": ("FX-D06-C02E05-RESCUE-CLEAR", "PC-W1"),
    "REQ_C02E05_FULL_KING_CANNON_SUPPORT": ("FX-D06-C02E05-RESCUE-CLEAR", "PC-W1"),
    "REQ_C02E05_OLD_BOXER_LOCK_BASE": ("FX-D06-C02E05-RESCUE-CLEAR", "PC-W2"),
    "REQ_C02E05_YELLOW_FRAME_INTERCEPT": ("FX-D06-C02E05-RESCUE-CLEAR", "PC-W4"),
    "REQ_C02E05_RED_CLEAR_PANEL": ("FX-D06-C02E05-RESCUE-CLEAR", "PC-W4"),
    "REQ_C02E05_BLUE_CREW_COVER": ("FX-D06-C02E05-RESCUE-CLEAR", "PC-W4"),
    "REQ_C02E05_JACK_FRAME_BRACE": ("FX-D06-C02E05-RESCUE-CLEAR", "PC-W4"),
}
EXPECTED_AUTHORITY_IDS = {
    "AUTH_C02E05_ASSET_PRIORITY_REVOKE",
    "AUTH_C02E05_CONTRACTOR_DETACH_UNLOCK",
}
ACTION_RESPONSE_REQUIRED_FIELDS = (
    "source_story_event",
    "source_episode_component",
    "source_episode_path",
    "source_episode_sha256",
    "source_event_token",
    "source_excerpt_start_token",
    "source_excerpt_end_token",
    "source_excerpt_sha256",
    "grantor",
    "grantee",
    "action_scope",
    "response_state",
    "conditions",
    "body_action",
    "receipt_id",
    "withdrawal_or_expiry",
    "state_domain",
    "owner_group",
    "transaction_id",
    "build_status",
    "human_evidence_status",
    "authority_boundary",
    "status",
)
EXPECTED_TRANSACTION_IDS = {
    "FX-D06-C02E04-MATCH": (
        "TX_C02E04_POINT3",
        "TX_C02E04_POINT4",
        "TX_C02E04_POINT5",
        "TX_C02E04_TOURNAMENT_CLEAR",
    ),
    "FX-D06-C02E04-ACCIDENT-CP": ("TX_C02E04_ACCIDENT_CP",),
    "FX-D06-C02E05-RESCUE-CLEAR": (
        "TX_C02E05_PA_CP",
        "TX_C02E05_PB_CP",
        "TX_C02E05_PC_CP",
        "TX_C02E05_ACCIDENT_CLEAR",
    ),
}
EXPECTED_SAVE_IDS = {
    "FX-D06-C02E04-MATCH": (
        "SAVE_C02E04_SCORE_0_2",
        "SAVE_C02E04_SCORE_1_2",
        "SAVE_C02E04_SCORE_2_2",
        "SAVE_C02E04_TOURNAMENT_CLEAR",
    ),
    "FX-D06-C02E04-ACCIDENT-CP": ("SAVE_C02E04_ACCIDENT_CP",),
    "FX-D06-C02E05-RESCUE-CLEAR": (
        "SAVE_C02E05_PA_CP",
        "SAVE_C02E05_PB_CP",
        "SAVE_C02E05_PC_CP",
        "SAVE_C02E05_ACCIDENT_CLEAR",
    ),
}
EXPECTED_STRATEGY_IDS = {
    "FX-D06-C02E04-MATCH": (
        "MATCH-S1-ANCHOR_READ",
        "MATCH-S2-MOBILITY_PROVOKE",
    ),
    "FX-D06-C02E04-ACCIDENT-CP": (
        "ACC-S1-NORTH_SHORT",
        "ACC-S2-SOUTH_STABLE",
    ),
    "FX-D06-C02E05-RESCUE-CLEAR": (
        "RESCUE-S1-MARGIN_CHAIN",
        "RESCUE-S2-RELAY_PATH",
    ),
}
EXPECTED_FUTURE_CONSUMERS = {
    "FX-D06-C02E04-MATCH": "FX-D06-C02E04-ACCIDENT-CP",
    "FX-D06-C02E04-ACCIDENT-CP": "FX-D06-C02E05-RESCUE-CLEAR",
    "FX-D06-C02E05-RESCUE-CLEAR": (
        "C02E05_STORY_SCORE_REAFFIRM_AND_DEPARTURE;"
        "C03E01_AFTER_CHAPTER_SETTLEMENT"
    ),
}
EXPECTED_WINDOW_IDS = {
    "FX-D06-C02E04-MATCH": {
        "P3-W1",
        "P3-W2",
        "P4-W1",
        "P4-W2",
        "P4-W3",
        "P5-W1",
        "P5-W2",
        "P5-W3",
    },
    "FX-D06-C02E04-ACCIDENT-CP": {"A-W1", "A-W2", "A-W3"},
    "FX-D06-C02E05-RESCUE-CLEAR": {
        "PA-W1",
        "PA-W2",
        "PA-W3",
        "PA-W4",
        "PB-W1",
        "PB-W2",
        "PB-W3",
        "PC-W1",
        "PC-W2",
        "PC-W3",
        "PC-W4",
    },
}
EXPECTED_MAP_TOKENS = {
    "FX-D06-C02E04-MATCH": {"N2", "W2", "W1", "C0", "E1", "E2", "S2", "OUT"},
    "FX-D06-C02E04-ACCIDENT-CP": {
        "A-CONTROL",
        "A-INNER-SAFE",
        "A-LINK-N",
        "A-LINK-S",
        "A-WORKSHOP-OUTER",
        "A-SEASIDE-SLOPE",
        "A-WORKROAD",
        "A-WANJI-EDGE",
    },
    "FX-D06-C02E05-RESCUE-CLEAR": {
        "R-INNER-SAFE",
        "R-LANE-N",
        "R-LANE-S",
        "R-ANCHOR",
        "R-SLOPE",
        "R-WANJI-EDGE",
        "R-WORKROAD",
        "R-BROKEN-BRIDGE",
        "R-INNER-LOAD",
        "R-DEMOLITION-FRAME",
        "R-LOCAL-MAINT",
    },
}
EXPECTED_BODY_OR_HAZARD_TOKENS = {
    "FX-D06-C02E04-MATCH": {"BODY_NO_NAME_01", "BODY_FULL_KING", "ARENA_CARGO_RING"},
    "FX-D06-C02E04-ACCIDENT-CP": {
        "GROUP_LAST_WORKSHOP",
        "ENV_LIGHT_PANEL_SLIDE",
        "ENV_CANNON_SLIDE",
        "ENV_EDGE_SETTLE",
    },
    "FX-D06-C02E05-RESCUE-CLEAR": {
        "Full King",
        "Guardian Z",
        "Old Boxer",
        "engineering vehicle",
        "cannon",
    },
}
STORY_SEED_TOKENS = {
    "C02E04_END": {"3:2", "人员撤出", "王者全装仍在", "比分已封存"},
    "C02E05_END": {"舞台炮送拆解架", "环停止下沉", "3:2保留", "王者自主卸装"},
}
EXPECTED_CONTACT_MARGINS = {
    "CONTACT-P3-REVERSE": 2,
    "CONTACT-P4-TOPPLE": 2,
    "CONTACT-P4-PIN": -4,
    "CONTACT-P5-REVERSE": 3,
}
CARRY_KEYS = (
    "score",
    "workshop_group",
    "passage",
    "full_king",
    "no_name",
    "stage_cannon",
    "wanji",
    "cargo_leader",
)

EXPECTED_STATE_DOMAIN_STRINGS = {
    "FX-D06-C02E04-MATCH": (
        "ST_RESULT;ST_BODY;ST_LOCATION;ST_EQUIPMENT;ST_OPERATION;"
        "ST_RELATION;ST_ENEMY_LEARNING"
    ),
    "FX-D06-C02E04-ACCIDENT-CP": (
        "ST_BODY;ST_LOCATION;ST_EQUIPMENT;ST_KNOWLEDGE;ST_RESOURCE;"
        "ST_CONSENT;ST_RESULT;ST_OPERATION"
    ),
    "FX-D06-C02E05-RESCUE-CLEAR": (
        "ST_BODY;ST_LOCATION;ST_EQUIPMENT;ST_RESOURCE;ST_KNOWLEDGE;"
        "ST_AUTHORITY;ST_CONSENT;ST_RESULT;ST_OPERATION"
    ),
}
EXPECTED_REGISTRY_AUTHORITY_BOUNDARIES = {
    "FX-D06-C02E04-MATCH": (
        "固定故事结果不可被玩法改写;仅MATCH四接触式可静态重算;"
        "装备实例字段不可漏;不写Reader/Canon/Runtime"
    ),
    "FX-D06-C02E04-ACCIDENT-CP": (
        "只是Phase Checkpoint非Mission Clear;自主支援需逐动作Consent receipt;"
        "无事故物理resolver;不写Reader/Canon/Runtime"
    ),
    "FX-D06-C02E05-RESCUE-CLEAR": (
        "不提交转子/推进模块/Roster/航向;自主支援逐动作Consent;"
        "卸装需Authority+Consent;无E05物理resolver;不写Reader/Canon/Runtime"
    ),
}
EXPECTED_EQUIPMENT_AUTHORITY_BOUNDARIES = {
    "EQ_WANJI_LATERAL_THRUSTER_01": (
        "纸面instance_id/owner_version为Candidate账键；借用/仍附着/"
        "后续归还来自Accepted Story"
    ),
    "EQ_FK_BACK_CANNON_01": (
        "纸面instance_id/owner_version为Candidate账键；装备仍归原主与"
        "本地维护位来自Accepted Story"
    ),
    "EQ_FK_LONG_WING_SET_01": (
        "纸面将Reader可见长翼组登记为唯一set实例；不推断未写明的翼片数量"
    ),
    "EQ_FK_SHIELD_SET_01": (
        "纸面将Reader可见盾组登记为唯一set实例；不推断未写明接口参数"
    ),
    "EQ_FK_DRILL_SET_01": (
        "纸面将Reader可见钻进组件登记为唯一set实例；不生成玩家库存"
    ),
    "EQ_FK_CROWN_01": (
        "纸面instance_id/owner_version为Candidate账键；头冠现场警报后回本地维护来自Accepted Story"
    ),
}

ACTION_CONSENT_BOUNDARY = (
    "Candidate逐动作Consent记录；不生成玩家按钮、永久服从、"
    "永久权限或Canon/Reader/Runtime写回"
)
ACTION_AUTHORITY_BOUNDARY = (
    "Candidate事故内单次Authority事件；不转移owner/custody，"
    "不授予永久解锁或Canon/Reader/Runtime写回"
)

# Each locator is deliberately tied to immutable Accepted Story component
# bytes.  The excerpt is found by unique start/end tokens, whitespace is
# normalized, and the resulting digest is line-number independent.
EXPECTED_ACTION_LOCATORS = {
    "REQ_C02E04_DRONE_HAZARD_SCAN": (
        "ASB-C02-20260806-56827053@episode_e04:survey_drones_scan",
        "episode_e04",
        "六架测绘无人机贴着外圈通过",
        "六架测绘无人机贴着外圈通过",
        "标出仍在变形的边缘。",
        "f079122d31eab961af64dcfcf62c70361fea1d268dfd21eb882b6774f1d23b42",
    ),
    "REQ_C02E04_JACK_EVAC_COVER": (
        "ASB-C02-20260806-56827053@episode_e04:jack_covers_last_workshop_group",
        "episode_e04",
        "坞工杰克放低两条装卸臂",
        "坞工杰克放低两条装卸臂",
        "挡住从斜面滑来的轻板。",
        "78cf8e2921a1c1be45fe1b9d7370995e900edb89932adc3d84eeb1e7442181fb",
    ),
    "REQ_C02E04_CARGO_EDGE_TOW": (
        "ASB-C02-20260806-56827053@episode_e04:cargo_leader_tows_wanji",
        "episode_e04",
        "火种货柜领袖拉紧牵引索",
        "火种货柜领袖拉紧牵引索",
        "正在下沉的临海外缘。",
        "213e7ee3f087a5d14161515aebba8ba47fd6bab6eab9e4e1d6cb37a499a99e48",
    ),
    "REQ_C02E05_RED_RING_SCAN": (
        "ASB-C02-20260806-56827053@episode_e05:red_scans_ring",
        "episode_e05",
        "红机抢先贴着外环飞完一圈",
        "红机抢先贴着外环飞完一圈",
        "不能再立即跑第二圈。",
        "da95baed56b463c7bebec65d062bab19362bad64ae87cc1f880685f7a6279f3d",
    ),
    "REQ_C02E05_BLUE_ENGINEERING_COVER": (
        "ASB-C02-20260806-56827053@episode_e05:blue_covers_engineering_route",
        "episode_e05",
        "蓝机放低宽翼",
        "蓝机放低宽翼",
        "轻板和碎片。",
        "1e49bd55dd0c74bab875aefb7f68ae326d9bc38500981a9524a693264fab602e",
    ),
    "REQ_C02E05_JACK_ENGINEERING_ESCORT": (
        "ASB-C02-20260806-56827053@episode_e05:jack_escorts_engineering_vehicle",
        "episode_e05",
        "坞工杰克收起主钳",
        "坞工杰克收起主钳",
        "把固定索接到炮身上。",
        "1abd4c559d716fd8d93eaac562082981a23d2306ed9fdc0c5b228643a69998ce",
    ),
    "REQ_C02E05_YELLOW_BRACKET_CUT": (
        "ASB-C02-20260806-56827053@episode_e05:yellow_cuts_two_brackets",
        "episode_e05",
        "它的第一发击断左侧支架",
        "黄机一直留在环外的高位射界",
        "翻进外轨之间。",
        "b971bcf5c13ebeeee813a9d58e5d557353c4880069dfbb34f6b8ee113c11d428",
    ),
    "REQ_C02E05_CARGO_WANJI_TOW": (
        "ASB-C02-20260806-56827053@episode_e05:cargo_leader_widens_wanji_contact",
        "episode_e05",
        "舰侧与圆环的接触面从一条窄边变宽",
        "平行作业道上，火种货柜领袖",
        "最重的那一段。",
        "3dbd4a71656ff0127e50b0e2ceaa420a671487f6057fc42d28622f8dedc983b1",
    ),
    "REQ_C02E05_GUARDIAN_BRIDGE_BRACE": (
        "ASB-C02-20260806-56827053@episode_e05:guardian_z_braces_bridge",
        "episode_e05",
        "馆守Z站在万机馆甲板边缘",
        "馆守Z站在万机馆甲板边缘",
        "驶进安全区。",
        "fb615fa7fcf279fd9921974081a3dbccf3e122439f621aa606fd6173bfe6a848",
    ),
    "REQ_C02E05_OLD_BOXER_CLEAR_LOAD": (
        "ASB-C02-20260806-56827053@episode_e05:old_boxer_clears_loadout",
        "episode_e05",
        "旧拳王已经把红色擂台牵引带",
        "旧拳王已经把红色擂台牵引带",
        "拖出工程员通路。",
        "e1956cfc74b0ff4e6a689e8030089782d95ea424d5c4f10ec958501ce0433608",
    ),
    "REQ_C02E05_FULL_KING_SELF_DETACH": (
        "ASB-C02-20260806-56827053@episode_e05:full_king_self_detaches",
        "episode_e05",
        "完全版王者自己发出解除指令",
        "“结构图已经发到你面前了。”",
        "完全版王者自己发出解除指令。",
        "ceac85d92dae74f0e208f8875a527a32cfd921e21f1b4f942d76718929dd600b",
    ),
    "REQ_C02E05_FULL_KING_CANNON_SUPPORT": (
        "ASB-C02-20260806-56827053@episode_e05:full_king_supports_cannon",
        "episode_e05",
        "完全版王者先冲上斜坡",
        "完全版王者先冲上斜坡",
        "向侧面让出拳路。",
        "2e1f497aa6b70da45772d16a46b18295ae97851baf20de33062666a3385bf612",
    ),
    "REQ_C02E05_OLD_BOXER_LOCK_BASE": (
        "ASB-C02-20260806-56827053@episode_e05:old_boxer_locks_cannon_base",
        "episode_e05",
        "旧拳王在后方锁住炮座",
        "旧拳王在后方锁住炮座。",
        "一起稳住圆环下沉的一侧。",
        "3c88e00af83fc4f2cbc4dbe9412e72ea1a32f90427a43876c7889393b1b7a5fc",
    ),
    "REQ_C02E05_YELLOW_FRAME_INTERCEPT": (
        "ASB-C02-20260806-56827053@episode_e05:yellow_intercepts_beam",
        "episode_e05",
        "黄机从高处击落一根",
        "旧拳王在后方锁住炮座。",
        "一起稳住圆环下沉的一侧。",
        "3c88e00af83fc4f2cbc4dbe9412e72ea1a32f90427a43876c7889393b1b7a5fc",
    ),
    "REQ_C02E05_RED_CLEAR_PANEL": (
        "ASB-C02-20260806-56827053@episode_e05:red_clears_panel",
        "episode_e05",
        "红机的过热警告刚刚熄灭",
        "旧拳王在后方锁住炮座。",
        "一起稳住圆环下沉的一侧。",
        "3c88e00af83fc4f2cbc4dbe9412e72ea1a32f90427a43876c7889393b1b7a5fc",
    ),
    "REQ_C02E05_BLUE_CREW_COVER": (
        "ASB-C02-20260806-56827053@episode_e05:blue_covers_crew",
        "episode_e05",
        "蓝机展开宽翼护住",
        "旧拳王在后方锁住炮座。",
        "一起稳住圆环下沉的一侧。",
        "3c88e00af83fc4f2cbc4dbe9412e72ea1a32f90427a43876c7889393b1b7a5fc",
    ),
    "REQ_C02E05_JACK_FRAME_BRACE": (
        "ASB-C02-20260806-56827053@episode_e05:jack_braces_demolition_frame",
        "episode_e05",
        "坞工杰克放下工程车",
        "旧拳王在后方锁住炮座。",
        "一起稳住圆环下沉的一侧。",
        "3c88e00af83fc4f2cbc4dbe9412e72ea1a32f90427a43876c7889393b1b7a5fc",
    ),
    "AUTH_C02E05_ASSET_PRIORITY_REVOKE": (
        "ASB-C02-20260806-56827053@episode_e05:glue_king_revokes_asset_priority",
        "episode_e05",
        "胶价王按了下去",
        "“取消优先单，就从你的项目账里扣。”",
        "“扣。”他说，“今天的事故留原片。先把它们都弄回来。”",
        "95ef10ad1e62defa1ac34126633e2a900ef8846d8f0f18a94de48e3e4b221f25",
    ),
    "AUTH_C02E05_CONTRACTOR_DETACH_UNLOCK": (
        "ASB-C02-20260806-56827053@episode_e05:maintainer_confirms_detach_unlock",
        "episode_e05",
        "事故自救可以解除外装",
        "完全版王者旧承包商的当值维护员接进频道。",
        "“东西还是原主的。”他看着还在跳动的红字，“先把锁开了。”",
        "51c3976277f7ad80fa5a289cc9b471f8b7ade13fc254521322e0f8aa5b201787",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_summary(line: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for token in line.split("|")[1:]:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        fields[key] = value
    return fields


def split_semicolon(value: str) -> tuple[str, ...]:
    return tuple(token for token in value.split(";") if token)


def calculate_signed_sum(expression: str) -> int | None:
    """Evaluate a digits-and-signs sum without using eval()."""

    if not re.fullmatch(r"-?\d+(?:[+-]\d+)*", expression):
        return None
    total = 0
    for sign, digits in re.findall(r"(^|[+-])(\d+)", expression):
        value = int(digits)
        total += -value if sign == "-" else value
    return total


def missing_required_fields(row: dict[str, str], fields: tuple[str, ...]) -> set[str]:
    return {field for field in fields if not row.get(field)}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require_exact(
    errors: list[str],
    label: str,
    row: dict[str, str],
    field: str,
    expected: str,
) -> None:
    actual = row.get(field, "")
    if actual != expected:
        fail(errors, f"{label} {field} differs: {actual!r} != {expected!r}")


def normalize_excerpt(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def load_c02_accepted_story_evidence(
    errors: list[str],
) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    binding_rows = {
        row["binding_id"]: row for row in read_tsv(BINDINGS)
    }
    binding = binding_rows.get("ASB-C02-20260806-56827053", {})
    if not binding:
        fail(errors, "C02 accepted-story binding missing")
        return {}, {}

    story_path = PROJECT / binding["accepted_story_path"]
    receipt_path = PROJECT / binding["receipt_path"]
    if not story_path.is_file() or sha256(story_path) != binding["accepted_story_sha256"]:
        fail(errors, "C02 accepted Reader bytes drifted")
    if not receipt_path.is_file() or sha256(receipt_path) != binding["receipt_sha256"]:
        fail(errors, "C02 acceptance receipt bytes drifted")

    components: dict[str, dict[str, str]] = {}
    for component in binding["accepted_episode_components"].split(";"):
        stage_id, rel_path, declared_hash = component.split("@")
        component_path = PROJECT / rel_path
        if stage_id in components:
            fail(errors, f"C02 accepted-story binding duplicates component: {stage_id}")
            continue
        text = ""
        if not component_path.is_file():
            fail(errors, f"C02 {stage_id} component missing: {rel_path}")
        else:
            current_hash = sha256(component_path)
            if current_hash != declared_hash:
                fail(errors, f"C02 {stage_id} component bytes drifted")
            text = component_path.read_text(encoding="utf-8")
        components[stage_id] = {
            "path": rel_path,
            "sha256": declared_hash,
            "text": text,
        }
    return binding, components


def validate_registry_candidate_contract(
    errors: list[str], row: dict[str, str], label: str
) -> None:
    fixture_id = row.get("fixture_id", "")
    expected_domains = EXPECTED_STATE_DOMAIN_STRINGS.get(fixture_id)
    expected_boundary = EXPECTED_REGISTRY_AUTHORITY_BOUNDARIES.get(fixture_id)
    if expected_domains is None or expected_boundary is None:
        fail(errors, f"{label} has no exact Candidate contract: {fixture_id}")
        return
    for field, expected in (
        ("state_domains", expected_domains),
        ("build_status", "zero_build"),
        ("human_evidence_status", "not_run"),
        ("authority_boundary", expected_boundary),
        ("status", "candidate_paper_fixture_defined"),
    ):
        require_exact(errors, label, row, field, expected)


def validate_equipment_candidate_contract(
    errors: list[str], row: dict[str, str], label: str
) -> None:
    equipment_id = row.get("equipment_instance_id", "")
    expected_boundary = EXPECTED_EQUIPMENT_AUTHORITY_BOUNDARIES.get(equipment_id)
    if expected_boundary is None:
        fail(errors, f"{label} has no exact Candidate contract: {equipment_id}")
        return
    for field, expected in (
        ("story_binding_id", "ASB-C02-20260806-56827053"),
        ("state_domain", "ST_EQUIPMENT"),
        ("owner_group", "SOG-BODY"),
        ("build_status", "zero_build"),
        ("human_evidence_status", "not_run"),
        ("authority_boundary", expected_boundary),
        ("status", "candidate_static_contract_only"),
    ):
        require_exact(errors, label, row, field, expected)


def expected_action_kind(record_id: str) -> str:
    if record_id in EXPECTED_AUTHORITY_IDS:
        return "authority_event"
    if record_id == "REQ_C02E05_FULL_KING_SELF_DETACH":
        return "story_bound_self_decision"
    return "story_bound_action_request"


def validate_action_candidate_contract(
    errors: list[str],
    row: dict[str, str],
    label: str,
    accepted_components: dict[str, dict[str, str]],
) -> None:
    record_id = row.get("record_id", "")
    locator = EXPECTED_ACTION_LOCATORS.get(record_id)
    if locator is None:
        fail(errors, f"{label} has no exact Accepted Story locator: {record_id}")
        return

    (
        expected_story_event,
        expected_component,
        expected_event_token,
        expected_start_token,
        expected_end_token,
        expected_excerpt_hash,
    ) = locator
    is_authority = record_id in EXPECTED_AUTHORITY_IDS
    expected_state_domain = "ST_AUTHORITY" if is_authority else "ST_CONSENT"
    expected_owner_group = "SOG-C2" if is_authority else "SOG-REL"
    expected_boundary = ACTION_AUTHORITY_BOUNDARY if is_authority else ACTION_CONSENT_BOUNDARY
    if is_authority:
        expected_fixture = "FX-D06-C02E05-RESCUE-CLEAR"
        expected_window = "PC-W1"
    else:
        expected_fixture, expected_window = EXPECTED_REQUEST_WINDOWS[record_id]
    expected_phase = (
        "E04_EVAC"
        if expected_fixture == "FX-D06-C02E04-ACCIDENT-CP"
        else expected_window.split("-", 1)[0]
    )
    expected_transaction = (
        "TX_C02E04_ACCIDENT_CP"
        if expected_phase == "E04_EVAC"
        else f"TX_C02E05_{expected_phase}_CP"
    )

    exact_fields = (
        ("record_kind", expected_action_kind(record_id)),
        ("fixture_id", expected_fixture),
        ("phase_id", expected_phase),
        ("window_id", expected_window),
        ("source_story_event", expected_story_event),
        ("source_episode_component", expected_component),
        ("source_event_token", expected_event_token),
        ("source_excerpt_start_token", expected_start_token),
        ("source_excerpt_end_token", expected_end_token),
        ("source_excerpt_sha256", expected_excerpt_hash),
        ("state_domain", expected_state_domain),
        ("owner_group", expected_owner_group),
        ("transaction_id", expected_transaction),
        ("build_status", "zero_build"),
        ("human_evidence_status", "not_run"),
        ("authority_boundary", expected_boundary),
        ("status", "candidate_static_contract_only"),
    )
    for field, expected in exact_fields:
        require_exact(errors, label, row, field, expected)

    component = accepted_components.get(expected_component)
    if component is None:
        fail(errors, f"{label} Accepted Story component missing: {expected_component}")
        return
    require_exact(errors, label, row, "source_episode_path", component["path"])
    require_exact(errors, label, row, "source_episode_sha256", component["sha256"])

    source_text = component["text"]
    if not source_text:
        return
    for token_label, token in (
        ("event", expected_event_token),
        ("start", expected_start_token),
        ("end", expected_end_token),
    ):
        if source_text.count(token) != 1:
            fail(
                errors,
                f"{label} {token_label} token must occur once in {expected_component}",
            )
    start_index = source_text.find(expected_start_token)
    end_index = source_text.find(expected_end_token, start_index)
    if start_index < 0 or end_index < 0:
        return
    end_index += len(expected_end_token)
    excerpt = source_text[start_index:end_index]
    if expected_event_token not in excerpt:
        fail(errors, f"{label} event token falls outside its excerpt")
    computed_hash = hashlib.sha256(
        normalize_excerpt(excerpt).encode("utf-8")
    ).hexdigest()
    if computed_hash != expected_excerpt_hash:
        fail(
            errors,
            f"{label} Accepted Story excerpt hash differs: "
            f"{computed_hash} != {expected_excerpt_hash}",
        )


def main() -> int:
    errors: list[str] = []

    required_files = {
        "document": DOC,
        "fixture registry": REGISTRY,
        "accepted-story bindings": BINDINGS,
        "transaction trace": TRACE,
        "chapter story-state seeds": STORY_SEEDS,
        "C02 equipment ledger": EQUIPMENT_LEDGER,
        "C02 authority/consent ledger": ACTION_LEDGER,
    }
    missing_files = [f"{label}: {path}" for label, path in required_files.items() if not path.is_file()]
    if missing_files:
        for missing in missing_files:
            print(f"FAIL missing {missing}")
        return 1

    _, accepted_components = load_c02_accepted_story_evidence(errors)
    doc_text = DOC.read_text(encoding="utf-8")
    computed_summaries: set[str] = set()
    summary_records: list[tuple[str, dict[str, str], str]] = []
    doc_lines = doc_text.splitlines()
    for index, line in enumerate(doc_lines):
        if not line.startswith("D06C02v0.1|"):
            continue
        digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
        nearby = "\n".join(doc_lines[index + 1 : index + 5])
        declared = re.search(
            r"(?:paper_summary_sha256|carry_payload_sha256) = ([0-9a-f]{64})",
            nearby,
        )
        if not declared:
            fail(errors, f"summary at line {index + 1} has no nearby declared hash")
            continue
        if digest != declared.group(1):
            fail(
                errors,
                f"summary hash mismatch at line {index + 1}: {digest} != {declared.group(1)}",
            )
        computed_summaries.add(digest)
        summary_records.append((line, parse_summary(line), digest))

    carry_records = [
        (line, fields, digest)
        for line, fields, digest in summary_records
        if fields.get("fixture") in {
            "FX-D06-C02E04-ACCIDENT-CP",
            "FX-D06-C02E05-RESCUE-CLEAR",
        }
        and fields.get("result") in {"phase_checkpoint", "pending"}
    ]
    if len(carry_records) != 2:
        fail(errors, f"expected two E04->E05 carry endpoints, got {len(carry_records)}")
    else:
        left = {key: carry_records[0][1].get(key) for key in CARRY_KEYS}
        right = {key: carry_records[1][1].get(key) for key in CARRY_KEYS}
        if left != right or any(value is None for value in left.values()):
            fail(errors, f"E04->E05 carry fields differ: {left} != {right}")
        else:
            canonical = "D06C02v0.1|carry=E04CP_to_E05|" + "|".join(
                f"{key}={left[key]}" for key in CARRY_KEYS
            )
            carry_digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            if carry_digest != "8f08c8e6670b241d7d0df5335fb19d6750368ca65e2374b66df35b45cd8b013f":
                fail(errors, f"E04->E05 canonical carry hash differs: {carry_digest}")

    contact_margins: dict[str, int] = {}
    for line_no, line in enumerate(doc_lines, 1):
        if not line.startswith("| `CONTACT-"):
            continue
        code_spans = re.findall(r"`([^`]+)`", line)
        contact_id = code_spans[0] if code_spans else ""
        formula = next(
            (
                value
                for value in code_spans[1:]
                if re.fullmatch(r"-?\d+(?:[+-]\d+)*=-?\d+", value)
            ),
            "",
        )
        if not formula:
            fail(errors, f"contact row line {line_no} has no recomputable formula")
            continue
        expression, declared_result = formula.split("=", 1)
        computed_result = calculate_signed_sum(expression)
        if computed_result is None or computed_result != int(declared_result):
            fail(errors, f"contact row line {line_no} formula differs: {formula}")
            continue
        contact_margins[contact_id] = computed_result
    if contact_margins != EXPECTED_CONTACT_MARGINS:
        fail(errors, f"contact margin set differs: {contact_margins}")

    section_markers = (
        ("FX-D06-C02E04-MATCH", "## 2. `FX-D06-C02E04-MATCH`"),
        ("FX-D06-C02E04-ACCIDENT-CP", "## 3. `FX-D06-C02E04-ACCIDENT-CP`"),
        ("FX-D06-C02E05-RESCUE-CLEAR", "## 4. `FX-D06-C02E05-RESCUE-CLEAR`"),
    )
    fixture_sections: dict[str, str] = {}
    for index, (fixture_id, marker) in enumerate(section_markers):
        start = doc_text.find(marker)
        next_start = (
            doc_text.find(section_markers[index + 1][1])
            if index + 1 < len(section_markers)
            else doc_text.find("## 5. 机器可校验纸面合同断言")
        )
        if start < 0 or next_start < 0 or next_start <= start:
            fail(errors, f"document section boundary missing for {fixture_id}")
            fixture_sections[fixture_id] = ""
        else:
            fixture_sections[fixture_id] = doc_text[start:next_start]

    discovered_window_ids = {
        "FX-D06-C02E04-MATCH": set(re.findall(r"`(P[345]-W\d+)`", fixture_sections.get("FX-D06-C02E04-MATCH", ""))),
        "FX-D06-C02E04-ACCIDENT-CP": set(re.findall(r"`(A-W\d+)`", fixture_sections.get("FX-D06-C02E04-ACCIDENT-CP", ""))),
        "FX-D06-C02E05-RESCUE-CLEAR": set(re.findall(r"`(P[ABC]-W\d+)`", fixture_sections.get("FX-D06-C02E05-RESCUE-CLEAR", ""))),
    }
    for fixture_id, expected_ids in EXPECTED_WINDOW_IDS.items():
        if discovered_window_ids.get(fixture_id) != expected_ids:
            fail(
                errors,
                f"{fixture_id} action-window ids differ: {sorted(discovered_window_ids.get(fixture_id, set()))}",
            )
        section_lines = fixture_sections.get(fixture_id, "").splitlines()
        for window_id in expected_ids:
            rows_for_window = [line for line in section_lines if line.startswith(f"| `{window_id}` |")]
            if len(rows_for_window) != 1 or rows_for_window[0].count("|") < 4:
                fail(errors, f"{fixture_id} {window_id} must have exactly one actionable table row")
        for token in EXPECTED_MAP_TOKENS[fixture_id]:
            if token not in fixture_sections.get(fixture_id, ""):
                fail(errors, f"{fixture_id} map token absent: {token}")
        for token in EXPECTED_BODY_OR_HAZARD_TOKENS[fixture_id]:
            if token not in fixture_sections.get(fixture_id, ""):
                fail(errors, f"{fixture_id} body/hazard token absent: {token}")

    expected_window_counts = {
        "FX-D06-C02E04-MATCH": len(EXPECTED_WINDOW_IDS["FX-D06-C02E04-MATCH"]),
        "FX-D06-C02E04-ACCIDENT-CP": len(EXPECTED_WINDOW_IDS["FX-D06-C02E04-ACCIDENT-CP"]),
        "FX-D06-C02E05-RESCUE-CLEAR": {
            "PA": len({value for value in EXPECTED_WINDOW_IDS["FX-D06-C02E05-RESCUE-CLEAR"] if value.startswith("PA-")}),
            "PB": len({value for value in EXPECTED_WINDOW_IDS["FX-D06-C02E05-RESCUE-CLEAR"] if value.startswith("PB-")}),
            "PC": len({value for value in EXPECTED_WINDOW_IDS["FX-D06-C02E05-RESCUE-CLEAR"] if value.startswith("PC-")}),
        },
    }

    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    with TRACE.open(encoding="utf-8", newline="") as handle:
        trace_row_list = list(csv.DictReader(handle, delimiter="\t"))
    trace_row_ids = [row["trace_row_id"] for row in trace_row_list]
    if len(trace_row_ids) != len(set(trace_row_ids)):
        fail(errors, "transaction trace contains duplicate trace_row_id")
    trace_rows = {row["trace_row_id"]: row for row in trace_row_list}
    with STORY_SEEDS.open(encoding="utf-8", newline="") as handle:
        story_seed_row_list = list(csv.DictReader(handle, delimiter="\t"))
    story_seed_ids = [row["checkpoint_id"] for row in story_seed_row_list]
    if len(story_seed_ids) != len(set(story_seed_ids)):
        fail(errors, "chapter story-state seeds contain duplicate checkpoint_id")
    story_seed_rows = {row["checkpoint_id"]: row for row in story_seed_row_list}

    with EQUIPMENT_LEDGER.open(encoding="utf-8", newline="") as handle:
        equipment_rows = list(csv.DictReader(handle, delimiter="\t"))
    equipment_ids = [row.get("equipment_instance_id", "") for row in equipment_rows]
    if set(equipment_ids) != EXPECTED_EQUIPMENT_IDS or len(equipment_ids) != len(EXPECTED_EQUIPMENT_IDS):
        fail(errors, f"C02 equipment ledger id set differs: {equipment_ids}")
    for line_no, equipment_row in enumerate(equipment_rows, 2):
        equipment_label = f"equipment ledger line {line_no}"
        missing = missing_required_fields(equipment_row, EQUIPMENT_REQUIRED_FIELDS)
        if missing:
            fail(errors, f"equipment ledger line {line_no} incomplete: {sorted(missing)}")
        validate_equipment_candidate_contract(errors, equipment_row, equipment_label)
        for field in EQUIPMENT_REQUIRED_FIELDS:
            mutated = dict(equipment_row)
            mutated[field] = ""
            if field not in missing_required_fields(mutated, EQUIPMENT_REQUIRED_FIELDS):
                fail(errors, f"A21 mutation did not reject missing equipment field: {field}")

    with ACTION_LEDGER.open(encoding="utf-8", newline="") as handle:
        action_rows = list(csv.DictReader(handle, delimiter="\t"))
    action_ids = [row.get("record_id", "") for row in action_rows]
    expected_action_ids = set(EXPECTED_REQUEST_WINDOWS) | EXPECTED_AUTHORITY_IDS
    if set(action_ids) != expected_action_ids or len(action_ids) != len(expected_action_ids):
        fail(errors, f"C02 authority/consent ledger id set differs: {action_ids}")
    action_rows_by_id = {row.get("record_id", ""): row for row in action_rows}
    for line_no, action_row in enumerate(action_rows, 2):
        record_id = action_row.get("record_id", "")
        action_label = f"authority/consent ledger line {line_no} ({record_id})"
        missing = missing_required_fields(action_row, ACTION_RESPONSE_REQUIRED_FIELDS)
        if missing:
            fail(errors, f"authority/consent ledger line {line_no} incomplete: {sorted(missing)}")
        validate_action_candidate_contract(
            errors,
            action_row,
            action_label,
            accepted_components,
        )
        for field in ACTION_RESPONSE_REQUIRED_FIELDS:
            mutated = dict(action_row)
            mutated[field] = ""
            if field not in missing_required_fields(mutated, ACTION_RESPONSE_REQUIRED_FIELDS):
                fail(errors, f"A11/A22 mutation did not reject {record_id} missing field: {field}")
        if record_id in EXPECTED_REQUEST_WINDOWS:
            expected_fixture, expected_window = EXPECTED_REQUEST_WINDOWS[record_id]
            if action_row.get("fixture_id") != expected_fixture or action_row.get("window_id") != expected_window:
                fail(errors, f"{record_id} fixture/window differs")
            if action_row.get("state_domain") != "ST_CONSENT" or action_row.get("owner_group") != "SOG-REL":
                fail(errors, f"{record_id} must be SOG-REL/ST_CONSENT")
            if not action_row.get("receipt_id", "").startswith("CONSENT_"):
                fail(errors, f"{record_id} has no consent receipt id")
            window_rows = [
                line
                for line in fixture_sections.get(expected_fixture, "").splitlines()
                if line.startswith(f"| `{expected_window}` |")
            ]
            if len(window_rows) != 1 or record_id not in window_rows[0]:
                fail(errors, f"{record_id} is not bound to its action-window row")
        elif record_id in EXPECTED_AUTHORITY_IDS:
            if action_row.get("record_kind") != "authority_event":
                fail(errors, f"{record_id} record kind differs")
            if action_row.get("state_domain") != "ST_AUTHORITY" or action_row.get("owner_group") != "SOG-C2":
                fail(errors, f"{record_id} must be SOG-C2/ST_AUTHORITY")
            if not action_row.get("receipt_id", "").startswith("AUTH_RECEIPT_"):
                fail(errors, f"{record_id} has no authority receipt id")
            if record_id not in doc_text:
                fail(errors, f"{record_id} is absent from document authority chain")

    authority_order = [row.get("record_id", "") for row in action_rows if row.get("record_kind") == "authority_event"]
    if authority_order != [
        "AUTH_C02E05_ASSET_PRIORITY_REVOKE",
        "AUTH_C02E05_CONTRACTOR_DETACH_UNLOCK",
    ]:
        fail(errors, f"E05 authority revoke/grant chain order differs: {authority_order}")
    self_detach = action_rows_by_id.get("REQ_C02E05_FULL_KING_SELF_DETACH", {})
    if self_detach.get("response_state") != "accepted_after_authority_chain":
        fail(errors, "Full King self-detach response is not authority-chain bound")

    doc_window_request_ids: set[str] = set()
    for section in fixture_sections.values():
        for line in section.splitlines():
            if not re.match(r"\| `(A-W\d+|P[ABC345]-W\d+)` \|", line):
                continue
            row_request_ids = set(re.findall(r"REQ_C02E0[45]_[A-Z0-9_]+", line))
            doc_window_request_ids.update(row_request_ids)
            if re.search(r"\brequest\b", line, flags=re.IGNORECASE) and not row_request_ids:
                fail(errors, f"action-window row has unledgered autonomous request: {line}")
    if doc_window_request_ids != set(EXPECTED_REQUEST_WINDOWS):
        fail(errors, f"document action-window request set differs: {sorted(doc_window_request_ids)}")

    fixture_ids = [row.get("fixture_id", "") for row in rows]
    if set(fixture_ids) != REQUIRED_FIXTURES or len(fixture_ids) != len(REQUIRED_FIXTURES):
        fail(errors, f"registry fixture set differs: {fixture_ids}")

    required_fields = {
        "fixture_id",
        "story_binding_id",
        "story_seed_guard_id",
        "transaction_trace_id",
        "state_domains",
        "recompute_level",
        "fixed_exit",
        "strategy_count",
        "strategy_basis",
        "action_window",
        "allowed_terminals",
        "initial_summary_sha256",
        "exit_summary_sha256",
        "transaction_ids",
        "future_consumer",
        "save_checkpoint",
        "recompute_assertion_ids",
        "build_status",
        "human_evidence_status",
        "authority_boundary",
        "status",
    }
    for line_no, row in enumerate(rows, 2):
        fixture_id = row.get("fixture_id", "")
        registry_label = f"registry line {line_no} ({fixture_id})"
        missing = sorted(field for field in required_fields if not row.get(field))
        if missing:
            fail(errors, f"registry line {line_no} missing fields: {missing}")
        validate_registry_candidate_contract(errors, row, registry_label)
        if fixture_id not in doc_text:
            fail(errors, f"registry line {line_no} fixture id absent from document")
        if row.get("story_binding_id") != "ASB-C02-20260806-56827053":
            fail(errors, f"registry line {line_no} uses wrong story binding")

        expected_trace_id = EXPECTED_TRACE_IDS.get(fixture_id, "")
        if row.get("transaction_trace_id") != expected_trace_id:
            fail(errors, f"registry line {line_no} transaction_trace_id differs")
        trace_row = trace_rows.get(expected_trace_id)
        if not trace_row:
            fail(errors, f"registry line {line_no} transaction trace missing: {expected_trace_id}")
        else:
            trace_domains = set(split_semicolon(trace_row.get("state_domains", "")))
            if trace_domains != EXPECTED_STATE_DOMAINS.get(fixture_id, set()):
                fail(errors, f"{expected_trace_id} state domains differ: {sorted(trace_domains)}")
            if len(trace_domains) != len(split_semicolon(trace_row.get("state_domains", ""))):
                fail(errors, f"{expected_trace_id} state domains contain duplicates")
            if trace_row.get("source_binding") != row.get("story_binding_id"):
                fail(errors, f"{expected_trace_id} source binding differs")
            trace_operation = trace_row.get("source_checkpoint_or_operation", "").split("@", 1)[0]
            if trace_operation != row.get("operation_id"):
                fail(errors, f"{expected_trace_id} operation differs: {trace_operation}")

        registry_domains = set(split_semicolon(row.get("state_domains", "")))
        if registry_domains != EXPECTED_STATE_DOMAINS.get(fixture_id, set()):
            fail(errors, f"registry line {line_no} state domains differ: {sorted(registry_domains)}")
        if len(registry_domains) != len(split_semicolon(row.get("state_domains", ""))):
            fail(errors, f"registry line {line_no} state domains contain duplicates")
        if f"`{row.get('state_domains', '')}`" not in doc_text:
            fail(errors, f"registry line {line_no} canonical state-domain string absent from document")
        expected_recompute_level = EXPECTED_RECOMPUTE_LEVELS.get(fixture_id, "")
        if row.get("recompute_level") != expected_recompute_level:
            fail(errors, f"registry line {line_no} recompute_level differs")
        if f"`{expected_recompute_level}`" not in doc_text:
            fail(errors, f"registry line {line_no} recompute_level absent from document")

        expected_seed_guard = EXPECTED_STORY_SEED_GUARDS.get(fixture_id, "")
        if row.get("story_seed_guard_id") != expected_seed_guard:
            fail(errors, f"registry line {line_no} story_seed_guard_id differs")
        seed_id = row.get("story_seed_guard_id", "").split(":", 1)[0]
        seed_row = story_seed_rows.get(seed_id)
        if not seed_row:
            fail(errors, f"registry line {line_no} story seed missing: {seed_id}")
        else:
            if seed_row.get("story_authority") != row.get("story_binding_id"):
                fail(errors, f"story seed {seed_id} authority differs")
            seed_payload = "\t".join(seed_row.values())
            for token in STORY_SEED_TOKENS.get(seed_id, set()):
                if token not in seed_payload:
                    fail(errors, f"story seed {seed_id} missing fixed token: {token}")
        if f"`{expected_seed_guard}`" not in doc_text:
            fail(errors, f"registry line {line_no} story seed projection absent from document")

        expected_transactions = EXPECTED_TRANSACTION_IDS.get(fixture_id, ())
        registry_transactions = split_semicolon(row.get("transaction_ids", ""))
        if registry_transactions != expected_transactions:
            fail(errors, f"registry line {line_no} transaction id sequence differs")
        expected_saves = EXPECTED_SAVE_IDS.get(fixture_id, ())
        registry_saves = split_semicolon(row.get("save_checkpoint", ""))
        if registry_saves != expected_saves:
            fail(errors, f"registry line {line_no} save id sequence differs")
        section = fixture_sections.get(fixture_id, "")
        section_transactions = set(re.findall(r"\bTX_C02E0[45]_[A-Z0-9_]+\b", section))
        if section_transactions != set(expected_transactions):
            fail(errors, f"{fixture_id} document transaction id set differs: {sorted(section_transactions)}")
        section_saves = set(re.findall(r"\bSAVE_C02E0[45]_[A-Z0-9_]+\b", section))
        if section_saves != set(expected_saves):
            fail(errors, f"{fixture_id} document save id set differs: {sorted(section_saves)}")

        expected_strategies = EXPECTED_STRATEGY_IDS.get(fixture_id, ())
        registry_strategies = split_semicolon(row.get("strategy_basis", ""))
        if registry_strategies != expected_strategies:
            fail(errors, f"registry line {line_no} strategy id sequence differs")
        try:
            strategy_count = int(row.get("strategy_count", ""))
        except ValueError:
            strategy_count = -1
        if strategy_count != len(expected_strategies) or len(set(registry_strategies)) != strategy_count:
            fail(errors, f"registry line {line_no} strategy_count/id cardinality differs")
        for strategy_id in expected_strategies:
            if strategy_id not in section:
                fail(errors, f"{fixture_id} strategy id absent from its document section: {strategy_id}")
        if row.get("future_consumer") != EXPECTED_FUTURE_CONSUMERS.get(fixture_id):
            fail(errors, f"registry line {line_no} future consumer sequence differs")
        if set(row.get("allowed_terminals", "").split(";")) != REQUIRED_TERMINALS:
            fail(errors, f"registry line {line_no} terminal set differs")
        for terminal in REQUIRED_TERMINALS:
            if section.count(f"| `{terminal}` |") != 1:
                fail(errors, f"{fixture_id} terminal row differs: {terminal}")
        if row.get("build_status") != "zero_build":
            fail(errors, f"registry line {line_no} is not zero_build")
        if row.get("human_evidence_status") != "not_run":
            fail(errors, f"registry line {line_no} human evidence is not not_run")
        for token in FIXED_EXIT_TOKENS.get(row.get("fixture_id", ""), set()):
            if token not in row.get("fixed_exit", ""):
                fail(errors, f"registry line {line_no} fixed_exit missing token: {token}")
        action_window = row.get("action_window", "")
        if fixture_id == "FX-D06-C02E04-MATCH":
            expected = expected_window_counts[fixture_id]
            if not action_window.startswith(f"{expected}x8s"):
                fail(errors, f"MATCH action_window differs from {expected} documented windows")
        elif fixture_id == "FX-D06-C02E04-ACCIDENT-CP":
            expected = expected_window_counts[fixture_id]
            if not action_window.startswith(f"{expected}x8s"):
                fail(errors, f"E04 accident action_window differs from {expected} documented windows")
        elif fixture_id == "FX-D06-C02E05-RESCUE-CLEAR":
            expected = expected_window_counts[fixture_id]
            expected_prefix = f"PA={expected['PA']}x8s;PB={expected['PB']}x8s;PC={expected['PC']}x8s"
            if not action_window.startswith(expected_prefix):
                fail(errors, f"E05 action_window differs from documented windows: {expected}")
        for hash_field in ("initial_summary_sha256", "exit_summary_sha256"):
            if row.get(hash_field) not in computed_summaries:
                fail(errors, f"registry line {line_no} {hash_field} not derived in document")
        for stable_id_field in (
            "transaction_ids",
            "save_checkpoint",
            "recompute_assertion_ids",
        ):
            for stable_id in row.get(stable_id_field, "").split(";"):
                if stable_id and stable_id not in doc_text:
                    fail(
                        errors,
                        f"registry line {line_no} {stable_id_field} id absent: {stable_id}",
                    )
                if stable_id_field == "recompute_assertion_ids" and stable_id:
                    if doc_text.count(f"| `{stable_id}` |") != 1:
                        fail(errors, f"registry line {line_no} assertion row differs: {stable_id}")
        assertion_ids = set(split_semicolon(row.get("recompute_assertion_ids", "")))
        if not {"D06-C02-A19", "D06-C02-A20"}.issubset(assertion_ids):
            fail(errors, f"registry line {line_no} lacks A19/A20 machine-ledger assertions")

    all_transaction_ids = [
        transaction_id
        for row in rows
        for transaction_id in split_semicolon(row.get("transaction_ids", ""))
    ]
    if len(all_transaction_ids) != len(set(all_transaction_ids)):
        fail(errors, "fixture registry reuses a transaction_id across fixtures")
    all_save_ids = [
        save_id
        for row in rows
        for save_id in split_semicolon(row.get("save_checkpoint", ""))
    ]
    if len(all_save_ids) != len(set(all_save_ids)):
        fail(errors, "fixture registry reuses a save checkpoint across fixtures")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print(f"RESULT FAIL ({len(errors)} error(s))")
        return 1

    print(
        "PASS D06 C02 paper fixtures: 3 registry rows; source bytes current; "
        f"{len(computed_summaries)} summaries/carry payloads reproducible; "
        "19 per-event Accepted Story locators exact; Candidate status/build/human/"
        "authority/owner/state enums exact; OST/story-seed/TX/SAVE/equipment/"
        "authority/consent/action/map contracts exact; "
        "only MATCH 4 contact equations statically recomputed; E04/E05 physics blocked; "
        "zero Build; human not run"
    )
    return 0


def run_mutation_self_test() -> int:
    """Prove that every guarded Candidate/source-locator field rejects drift."""

    setup_errors: list[str] = []
    _, accepted_components = load_c02_accepted_story_evidence(setup_errors)
    registry_rows = read_tsv(REGISTRY)
    equipment_rows = read_tsv(EQUIPMENT_LEDGER)
    action_rows = read_tsv(ACTION_LEDGER)

    for index, row in enumerate(registry_rows, 2):
        validate_registry_candidate_contract(
            setup_errors,
            row,
            f"self-test registry baseline line {index}",
        )
    for index, row in enumerate(equipment_rows, 2):
        validate_equipment_candidate_contract(
            setup_errors,
            row,
            f"self-test equipment baseline line {index}",
        )
    for index, row in enumerate(action_rows, 2):
        validate_action_candidate_contract(
            setup_errors,
            row,
            f"self-test action baseline line {index}",
            accepted_components,
        )
    if setup_errors:
        for error in setup_errors:
            print(f"SELFTEST FAIL baseline {error}")
        print(f"SELFTEST RESULT FAIL ({len(setup_errors)} baseline error(s))")
        return 1

    mutation_failures: list[str] = []
    mutation_count = 0

    def assert_rejected(
        row: dict[str, str],
        field: str,
        validator: object,
        label: str,
    ) -> None:
        nonlocal mutation_count
        mutation_count += 1
        mutated = dict(row)
        mutated[field] = "__INTENTIONAL_DRIFT__"
        local_errors: list[str] = []
        validator(local_errors, mutated, label)
        if not local_errors:
            mutation_failures.append(f"{label} field drift was accepted: {field}")

    for row in registry_rows:
        fixture_id = row["fixture_id"]
        for field in (
            "state_domains",
            "build_status",
            "human_evidence_status",
            "authority_boundary",
            "status",
        ):
            assert_rejected(
                row,
                field,
                validate_registry_candidate_contract,
                f"registry {fixture_id}",
            )

    for row in equipment_rows:
        equipment_id = row["equipment_instance_id"]
        for field in (
            "story_binding_id",
            "state_domain",
            "owner_group",
            "build_status",
            "human_evidence_status",
            "authority_boundary",
            "status",
        ):
            assert_rejected(
                row,
                field,
                validate_equipment_candidate_contract,
                f"equipment {equipment_id}",
            )

    def action_validator(
        local_errors: list[str], mutated: dict[str, str], label: str
    ) -> None:
        validate_action_candidate_contract(
            local_errors,
            mutated,
            label,
            accepted_components,
        )

    for row in action_rows:
        record_id = row["record_id"]
        for field in (
            "record_kind",
            "fixture_id",
            "phase_id",
            "window_id",
            "source_story_event",
            "source_episode_component",
            "source_episode_path",
            "source_episode_sha256",
            "source_event_token",
            "source_excerpt_start_token",
            "source_excerpt_end_token",
            "source_excerpt_sha256",
            "state_domain",
            "owner_group",
            "transaction_id",
            "build_status",
            "human_evidence_status",
            "authority_boundary",
            "status",
        ):
            assert_rejected(
                row,
                field,
                action_validator,
                f"action {record_id}",
            )

    if mutation_failures:
        for error in mutation_failures:
            print(f"SELFTEST FAIL {error}")
        print(f"SELFTEST RESULT FAIL ({len(mutation_failures)} mutation gap(s))")
        return 1
    print(
        "SELFTEST PASS D06 C02: "
        f"{mutation_count} in-memory Candidate/source-locator drifts rejected"
    )
    return 0


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check D06 C02 paper fixtures without writing project state."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="also inject in-memory field drifts and require every one to fail",
    )
    args = parser.parse_args(argv)
    result = main()
    if result != 0 or not args.self_test:
        return result
    return run_mutation_self_test()


if __name__ == "__main__":
    sys.exit(cli())
