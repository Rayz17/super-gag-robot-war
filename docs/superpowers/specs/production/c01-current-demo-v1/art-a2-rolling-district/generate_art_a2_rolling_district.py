#!/usr/bin/env python3
"""Generate C01E02 A2 rolling old-expo district Candidate review assets."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]

CONTRACT_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/19-current-demo-inplace-rebase-producer-contract.md"
CONTRACT_SHA256 = "6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94"
CONTRACT_ID = "C01CDV1"
CONTRACT_REVISION = 2
BUILD_ID = "C01CDV1-M2-R2"
CONTENT_FINGERPRINT = "00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4"
TACTICAL_PROFILE_ID = "c01cdv1_e02_scroll_m2_r2"
MAP_SLOT = "MAP_C01CDV1_SCROLLING_STREET"
PACKAGE_ID = "C01CDV1_A2_ROLLING_DISTRICT_V1"

PROFILE_PATH = "game-godot/content/candidate_runtime_demo/c01/e02/graybox_profiles.json"
FALLBACK_PATH = "game-godot/content/candidate_runtime_demo/c01/e02/named_geometry_fallbacks.json"
BUILD_IDENTITY_PATH = "game-godot/content/candidate_runtime_demo/c01/e02/generated/build_identity.json"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

WIDTH = 1280
HEIGHT = 720
TACTICAL_RECT = (0, 54, 900, 648)
TACTICAL_SIZE = (900, 594)
UI_RECT = (900, 54, 1280, 648)
TOP_HUD = (0, 0, 1280, 54)
BOTTOM_HUD = (0, 648, 1280, 720)

PAPER = "#edf1ee"
INK_DEEP = "#08151b"
INK = "#162930"
INK_SOFT = "#40545a"
TEAL = "#56aaa3"
GOLD = "#d9aa3d"
CORAL = "#e85e51"
IVORY = "#d9ddd5"
CYAN = "#68c5c8"
ORANGE = "#e68149"
RED = "#d9504b"
GREEN = "#5fc49f"


# Exact live revision-2 sources at dispatch time. Old B3 is deliberately absent.
SOURCE_LOCKS = (
    (CONTRACT_PATH, CONTRACT_SHA256, "producer_contract_r2", "active"),
    ("docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C01-闭馆以后万机出击.md", "c9a9aa490badea3d2de937e0003b80547974fed27103b31ec9181cd3583cfc8b", "accepted_reader", "active"),
    ("docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C01/C01-用户创作验收回执.md", "3d11387d92120cfdeeb0069a2a7cdfbe677ed0ea2ac5ae6649038de7b0cd532b", "story_acceptance", "active"),
    ("docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-剧情游玩拓扑与状态桥接.tsv", "5d640ed3e70854a178194ceeeffe7d444a928547a414af3407674b9d4f4be5aa", "story_play_topology", "active"),
    ("docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/gameflow/C01-游戏流程解构-v1.md", "68ac0efa2d8316f33eb41ca745568684dd180021931355e8ff1d0798196b5296", "candidate_gameflow", "active_with_contract_override"),
    ("docs/superpowers/specs/2026-08-08-chao-gag-story-play-operation-topology-contract-v1.md", "550da9196bb9029aa0ceb7d75cd1bfdb73c852dd806fb4b609f1765c652eee76", "global_play_topology", "active"),
    (PROFILE_PATH, "07f611fabb1a41c713da5019ce433820f95229cbf83b633fe67fa43d836278da", "live_m2_graybox_topology", "active_read_only"),
    (FALLBACK_PATH, "cfcabcdf5dca0efebdc982ce59012cb8c7c89dc55a7ad71672b90140f2758c01", "named_geometry_policy", "active_read_only"),
    (BUILD_IDENTITY_PATH, "3ceadfee30defad3ed606759165da2f88df9c402c5d130585e07147f7b97bdb8", "revision2_build_identity", "active_read_only"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv", "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee", "guardian_direction_receipt", "active_direction_only"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv", "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920", "breaker_direction_receipt", "active_direction_only"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b2-user-approval-receipt.tsv", "792d9061b804ec3d87d79c777171f5aa4bd44979416c40d45d8968a2004d0c51", "shield_direction_receipt", "active_direction_only"),
    ("docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md", "ec061505dc395c96136e9415985706ecf6c99c564e68c0c5686968581f40b653", "series_art_language", "active"),
    ("docs/superpowers/specs/data/canon/authority_manifest.tsv", None, "canon_authority", "active_read_only_scoped"),
    ("docs/superpowers/specs/data/canon/entities.tsv", None, "canon_entities", "active_read_only_scoped"),
    ("docs/superpowers/specs/data/canon/scenes.tsv", None, "canon_scenes", "active_read_only_scoped_with_sequence_residual"),
    ("docs/superpowers/specs/data/canon/wanji_exhibition_zones.tsv", None, "wanji_external_zone", "active_read_only_scoped"),
)

SUPERSEDED_ITEMS = (
    ("docs/superpowers/specs/production/c01-current-demo-v1/18-g1-5-b3-tactical-map-art-objective.md", "d9f1c67ce7beddaf376cbcfee707e145f0c36f21c246fad7e9fcb977de587bcc", "superseded_history_only"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b3-tactical-map/asset-manifest.tsv", "424bc211fbeb79d6fbdb6b614729cc3f8aa8932e2d47374230074f82ece4cbff", "superseded_history_only"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b3-tactical-map/delivery-hashes.sha256", "e61700d0fbc5cb7696fd3aec9fffb0aee80ae4787364aaa852d378db3faf5b69", "superseded_history_only"),
    ("profile:c01cdv1_s06_g1_v1", "n/a", "superseded_history_only"),
    ("slot:BG_C01CDV1_PLAZA_TACTICAL", "n/a", "superseded_history_only"),
)


@dataclass(frozen=True)
class Candidate:
    code: str
    stable_id: str
    title: str
    identity: str
    spatial_organization: str
    visual_language: str
    strength: str
    risk: str
    asset_volume: str
    runtime_tech: str
    accent: str
    seed: int


CANDIDATES = (
    Candidate(
        "A",
        "CAND_C01CDV1_A2_DISTRICT_A_EXPO_SPINE_V1",
        "会展中轴大道型",
        "把旧会展区读成一条宽阔的展馆服务中轴，低矮展馆在两侧后退。",
        "西侧起步区、中央巨机路口、东侧撤离廊道呈一条连续长轴。",
        "大色块混凝土、深墨蓝路面、象牙边和旧黄铜节点；细节密度最低。",
        "滚动方向与主路攻防一眼可读，对小体和车辆最友好。",
        "若展馆边缘做得太克制，容易像城市测试场或普通工业区。",
        "LOW: 4组展馆模块 + 2组道路 + 1组破损连廊 + 共享道具",
        "LOW: 建筑分组2级；单组屋顶淡出即可；连续滚动成本最低",
        TEAL,
        4101,
    ),
    Candidate(
        "B",
        "CAND_C01CDV1_A2_DISTRICT_B_RESCUE_RING_V1",
        "馆墙防灾环廊型",
        "万机馆南侧旧展墙、防灾铺装和东门应急带共同构成场景身份。",
        "北侧馆墙与居民建筑形成保护面，中央空场让两台巨体回旋，东侧防灾环廊引向撤离口。",
        "冷白馆墙、墨蓝铺装、朱红应急结构与低饱和绿灰修补面。",
        "万机馆、取盾点、北侧保护和东侧撤离线四件事同时成立。",
        "馆墙、连廊和应急设施若没有明确淡出组，中景容易堵住一格小体。",
        "MID: 6组展馆/防灾模块 + 2组闸门状态 + 1组连廊 + 共享道具",
        "MID: 建筑分组3级；撤离口状态切换；屋顶淡出与轮廓候选",
        GOLD,
        5202,
    ),
    Candidate(
        "C",
        "CAND_C01CDV1_A2_DISTRICT_C_LAYERED_RAIN_V1",
        "层叠旧馆雨谷型",
        "用高低错落的旧展馆、断裂连廊和弧形雨棚把战场变成一条雨夜街谷。",
        "西侧有馆体破口，中央道路在层叠屋檐间打开，东侧撤离灯带成为雨幕中的出口。",
        "深蓝灰湿面、冷白屋檐、朱红断面与少量琥珀反射；大块湿光不做碎高光。",
        "章节气氛和巨体尺度最强，三段滚动会有明显的场景进程。",
        "遮挡、雨面反射和屋顶层级最多；若不做严格 LOD，会吞掉路径与意图提示。",
        "HIGH: 8组展馆/屋顶模块 + 3组雨棚/连廊 + 2组湿面 LOD + 共享道具",
        "HIGH: 建筑分组4级；淡出+轮廓更必要；雨面/屋檐需低端o LOD",
        CORAL,
        6303,
    ),
)


REVIEW_CAMERAS = (
    ("WEST", "A2_CAM_WEST_GUARDIAN_SHIELD", (-160, 320), "西/南主战起步：馆守Z与取盾点"),
    ("CENTRAL", "A2_CAM_CENTRAL_BOSS_PRESSURE", (240, 480), "中央主战：重盾、BREAKER与多向小体"),
    ("EAST", "A2_CAM_EAST_RESCUE_LANE", (830, 620), "东侧撤离：rescue_lane、最后车辆与东门"),
)

DENSITY_ANCHORS = {
    "LOW": [(13, 6), (27, 6), (15, 12), (29, 11)],
    "MID": [(13, 6), (18, 5), (27, 6), (15, 12), (29, 11), (21, 14)],
    "HIGH": [(9, 8), (13, 6), (18, 5), (22, 4), (27, 6), (15, 12), (24, 12), (29, 11), (21, 14)],
}


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_sha(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def load_tsv(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_scoped_canon() -> None:
    authority = {
        (row["record_type"], row["record_id"]): row
        for row in load_tsv("docs/superpowers/specs/data/canon/authority_manifest.tsv")
    }
    for key in (
        ("entity", "V353U001"),
        ("entity", "ENEMY_C01_BREAKER"),
        ("entity", "ENEMY_C01_RIFT_SWARM"),
        ("scene", "V355-C01E02"),
    ):
        row = authority.get(key)
        if not row or row.get("canon_level") != "working" or row.get("lifecycle_status") != "active":
            raise RuntimeError(f"A2 scoped Canon authority mismatch: {key}")

    entities = {row["entity_id"]: row for row in load_tsv("docs/superpowers/specs/data/canon/entities.tsv")}
    guardian = entities.get("V353U001", {})
    breaker = entities.get("ENEMY_C01_BREAKER", {})
    swarm = entities.get("ENEMY_C01_RIFT_SWARM", {})
    if guardian.get("status") != "working_current" or "18米" not in guardian.get("role", ""):
        raise RuntimeError("A2 scoped Canon mismatch: Guardian Z scale/state")
    if breaker.get("status") != "working_current" or "近30米" not in breaker.get("implementation_policy", ""):
        raise RuntimeError("A2 scoped Canon mismatch: BREAKER ground scale/state")
    if swarm.get("status") != "working_current" or "E02少量" not in swarm.get("implementation_policy", ""):
        raise RuntimeError("A2 scoped Canon mismatch: E02 swarm quantity state")
    if "各自扑击" not in swarm.get("implementation_policy", "") or "不锁造型" not in swarm.get("notes", ""):
        raise RuntimeError("A2 scoped Canon mismatch: scattered/non-design swarm boundary")

    scenes = {row["scene_id"]: row for row in load_tsv("docs/superpowers/specs/data/canon/scenes.tsv")}
    scene = scenes.get("V355-C01E02", {})
    required = set(scene.get("required_entities", "").split(";"))
    if not {"V353U001", "ENEMY_C01_BREAKER", "ENEMY_C01_RIFT_SWARM"}.issubset(required):
        raise RuntimeError("A2 scoped Canon mismatch: C01E02 required entities")
    scene_text = scene.get("location", "") + scene.get("notes", "")
    for token in ("旧会展广场与相连街区", "最后应急车辆", "退役重盾", "各自扑击"):
        if token not in scene_text:
            raise RuntimeError(f"A2 scoped Canon scene token missing: {token}")

    zones = {row["zone_id"]: row for row in load_tsv("docs/superpowers/specs/data/canon/wanji_exhibition_zones.tsv")}
    external = zones.get("WEZ_EXT_01_DOCKYARD_LOCKS", {})
    if external.get("map_code") != "EXT-D01" or "旧会展广场" not in external.get("canonical_name", ""):
        raise RuntimeError("A2 scoped Canon mismatch: external old-expo zone")


def validate_sources() -> tuple[dict, str]:
    for relative_path, expected_sha, _, _ in SOURCE_LOCKS:
        path = ROOT / relative_path
        if not path.is_file():
            raise RuntimeError(f"A2 source missing: {relative_path}")
        actual = sha256_file(path)
        if expected_sha is not None and actual != expected_sha:
            raise RuntimeError(f"A2 source hash drift: {relative_path}: {actual}")

    contract = (ROOT / CONTRACT_PATH).read_text(encoding="utf-8")
    for token in (
        "revision=2", "户外地图必须大于单屏", "scattered",
        "A1 馆守 Z、B1 BREAKER、B2 重盾只批准作为继续派生的方向",
        "旧 B3 地图全部退出活跃生产链",
    ):
        if token not in contract:
            raise RuntimeError(f"A2 producer contract token missing: {token}")

    validate_scoped_canon()
    profile_doc = load_json(PROFILE_PATH)
    tactical = profile_doc["tactical_profile"]
    identity = load_json(BUILD_IDENTITY_PATH)
    fallbacks = load_json(FALLBACK_PATH)
    if identity.get("contract_revision") != CONTRACT_REVISION:
        raise RuntimeError("A2 requires revision-2 build identity")
    if identity.get("build_id") != BUILD_ID or identity.get("content_fingerprint") != CONTENT_FINGERPRINT:
        raise RuntimeError("A2 revision-2 build identity mismatch")
    if tactical.get("profile_id") != TACTICAL_PROFILE_ID:
        raise RuntimeError("A2 tactical profile mismatch")
    if tactical.get("grid") != [32, 18]:
        raise RuntimeError("A2 requires the 32x18 rolling topology")
    if tactical.get("swarm_organization_state") != "scattered":
        raise RuntimeError("A2 E02 swarm must remain scattered")
    if tactical.get("projection", {}).get("tile_half") != [40, 20]:
        raise RuntimeError("A2 projection drift")
    slot = next((item for item in fallbacks.get("slots", []) if item.get("slot_id") == MAP_SLOT), None)
    if not slot or slot.get("geometry") != "programmatic_isometric_street_blocks" or slot.get("runtime_allowed") is not False:
        raise RuntimeError("A2 named geometry policy mismatch")

    topology_payload = {
        "profile_id": tactical["profile_id"],
        "grid": tactical["grid"],
        "projection": tactical["projection"],
        "swarm_organization_state": tactical["swarm_organization_state"],
        "minimum_phase_survivors": tactical["minimum_phase_survivors"],
        "shield_hotspot": tactical["shield_hotspot"],
        "guard_zone": tactical["guard_zone"],
        "units": tactical["units"],
        "terrain_zones": tactical["terrain_zones"],
        "destructibles": tactical["destructibles"],
        "phase_checkpoint": tactical["phase_checkpoint"],
    }
    return tactical, canonical_json_sha(topology_payload)


def rgba(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    value = hex_color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def mix(a: str, b: str, amount: float) -> str:
    av = tuple(int(a.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    bv = tuple(int(b.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    cv = tuple(round(av[i] * (1.0 - amount) + bv[i] * amount) for i in range(3))
    return "#%02x%02x%02x" % cv


def text_wrap(draw: ImageDraw.ImageDraw, text: str, width: int, used_font: ImageFont.FreeTypeFont) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if current and draw.textbbox((0, 0), trial, font=used_font)[2] > width:
            lines.append(current)
            current = char
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    width: int,
    size: int,
    fill: str,
    *,
    bold: bool = False,
    spacing: int = 5,
) -> int:
    used_font = font(size, bold=bold)
    y = xy[1]
    for paragraph in text.split("\n"):
        for line in text_wrap(draw, paragraph, width, used_font):
            draw.text((xy[0], y), line, font=used_font, fill=fill)
            y += size + spacing
        y += spacing
    return y


def world_point(x: float, y: float) -> tuple[float, float]:
    return ((x - y) * 40.0, (x + y) * 20.0)


def camera_bounds() -> tuple[float, float, float, float]:
    min_world = (-720.0, -20.0)
    max_world = (1280.0, 980.0)
    return (
        min_world[0] + TACTICAL_SIZE[0] / 2,
        min_world[1] + TACTICAL_SIZE[1] / 2,
        max_world[0] - TACTICAL_SIZE[0] / 2,
        max_world[1] - TACTICAL_SIZE[1] / 2,
    )


def viewport_projector(camera: tuple[float, float]) -> Callable[[float, float], tuple[int, int]]:
    def project(x: float, y: float) -> tuple[int, int]:
        wx, wy = world_point(x, y)
        return (round(450 + wx - camera[0]), round(297 + wy - camera[1]))
    return project


def overview_projector() -> Callable[[float, float], tuple[int, int]]:
    def project(x: float, y: float) -> tuple[int, int]:
        wx, wy = world_point(x, y)
        return (round(880 + wx), round(170 + wy))
    return project


def cell_polygon(project: Callable[[float, float], tuple[int, int]], x: int, y: int) -> list[tuple[int, int]]:
    cx, cy = project(x, y)
    return [(cx, cy - 20), (cx + 40, cy), (cx, cy + 20), (cx - 40, cy)]


def rect_footprint_polygon(
    project: Callable[[float, float], tuple[int, int]], rect: list[int]
) -> list[tuple[int, int]]:
    x, y, w, h = rect
    p0 = project(x, y)
    p1 = project(x + w - 1, y)
    p2 = project(x + w - 1, y + h - 1)
    p3 = project(x, y + h - 1)
    return [
        (p0[0], p0[1] - 20),
        (p1[0] + 40, p1[1]),
        (p2[0], p2[1] + 20),
        (p3[0] - 40, p3[1]),
    ]


def rect_contains(rect: list[int], x: int, y: int) -> bool:
    return rect[0] <= x < rect[0] + rect[2] and rect[1] <= y < rect[1] + rect[3]


def terrain_kind(tactical: dict, x: int, y: int) -> str:
    result = "plaza"
    for zone in tactical["terrain_zones"]:
        if rect_contains(zone["rect"], x, y):
            result = zone["kind"]
    return result


def candidate_palette(candidate: Candidate) -> dict[str, str]:
    if candidate.code == "A":
        return {
            "background": "#0c181e", "plaza": "#596d72", "road": "#283941",
            "rescue_lane": "#38635e", "security_apron": "#586047",
            "building_roof": "#728389", "building_side_a": "#354a52", "building_side_b": "#243840",
            "corridor": "#626e70", "line": "#8a9a98", "trim": "#d2d5c9", "accent": TEAL,
        }
    if candidate.code == "B":
        return {
            "background": "#0d171c", "plaza": "#566a6c", "road": "#28363d",
            "rescue_lane": "#315d58", "security_apron": "#5b5c40",
            "building_roof": "#687980", "building_side_a": "#35474e", "building_side_b": "#23363e",
            "corridor": "#715c59", "line": "#9aa7a3", "trim": "#dde0d7", "accent": CORAL,
        }
    return {
        "background": "#09161d", "plaza": "#455a61", "road": "#1e3038",
        "rescue_lane": "#285451", "security_apron": "#4e553b",
        "building_roof": "#4a626b", "building_side_a": "#293e47", "building_side_b": "#1a3039",
        "corridor": "#655458", "line": "#71878a", "trim": "#ccd3ce", "accent": CORAL,
    }


def draw_ground(
    canvas: Image.Image,
    tactical: dict,
    candidate: Candidate,
    project: Callable[[float, float], tuple[int, int]],
    *,
    grid_alpha: int = 58,
) -> None:
    palette = candidate_palette(candidate)
    draw = ImageDraw.Draw(canvas, "RGBA")
    for y in range(tactical["grid"][1]):
        for x in range(tactical["grid"][0]):
            kind = terrain_kind(tactical, x, y)
            fill = palette.get(kind, palette["plaza"])
            poly = cell_polygon(project, x, y)
            draw.polygon(poly, fill=rgba(fill, 255))
            draw.line(poly + [poly[0]], fill=rgba(palette["line"], grid_alpha), width=1)

    # Main road lane rhythm and east rescue lane are world markings, not tactical UI.
    for y_line, color, width in ((8.45, palette["trim"], 2), (10.55, palette["trim"], 2)):
        points = [project(x, y_line) for x in range(0, 32)]
        draw.line(points, fill=rgba(color, 105), width=width, joint="curve")
    for x in range(16, 31, 2):
        a = project(x, 4.15)
        b = project(x + 0.9, 4.15)
        draw.line((a, b), fill=rgba("#dbe3d9", 165), width=3)
    # Large crosswalk blocks near the east gate, deliberately off tactical-cell cadence.
    for offset in range(4):
        x = 27.2 + offset * 0.7
        draw.line((project(x, 3.45), project(x, 5.0)), fill=rgba("#e2e5dc", 115), width=5)

    # South approach damage is surface-only and never changes passability.
    damage_points = [project(22.8, 17.0), project(23.1, 14.7), project(22.7, 12.7), project(23.0, 9.4)]
    draw.line(damage_points, fill=rgba("#1a2429", 145), width=8, joint="curve")
    draw.line(damage_points, fill=rgba("#9b594b", 82), width=2, joint="curve")


def draw_building_volume(
    canvas: Image.Image,
    candidate: Candidate,
    project: Callable[[float, float], tuple[int, int]],
    rect: list[int],
    height: int,
    index: int,
    *,
    alpha: int = 255,
    outline_only: bool = False,
) -> None:
    palette = candidate_palette(candidate)
    draw = ImageDraw.Draw(canvas, "RGBA")
    foot = rect_footprint_polygon(project, rect)
    roof = [(x, y - height) for x, y in foot]
    if candidate.code == "C":
        roof = [
            (roof[0][0], roof[0][1] - 10),
            (roof[1][0], roof[1][1] + 4),
            (roof[2][0], roof[2][1] - 5),
            (roof[3][0], roof[3][1] - 16),
        ]

    if not outline_only:
        draw.polygon([roof[1], roof[2], foot[2], foot[1]], fill=rgba(palette["building_side_a"], alpha))
        draw.polygon([roof[2], roof[3], foot[3], foot[2]], fill=rgba(palette["building_side_b"], alpha))
        roof_color = palette["building_roof"]
        if candidate.code == "B" and index % 2:
            roof_color = mix(roof_color, "#d8ddd6", 0.15)
        draw.polygon(roof, fill=rgba(roof_color, alpha), outline=rgba(INK_DEEP, min(230, alpha)))

        # One legible roof gesture per volume, never a field of tiny panels.
        if candidate.code == "A":
            draw.line((roof[0], roof[2]), fill=rgba(palette["trim"], min(130, alpha)), width=5)
        elif candidate.code == "B":
            draw.line((roof[0], roof[1]), fill=rgba(CORAL, min(210, alpha)), width=9)
            center = (sum(p[0] for p in roof) // 4, sum(p[1] for p in roof) // 4)
            draw.polygon(
                [(center[0] - 28, center[1] + 7), (center[0], center[1] - 19), (center[0] + 28, center[1] + 7)],
                fill=rgba(IVORY, min(115, alpha)),
            )
        else:
            draw.line((roof[3], roof[1]), fill=rgba("#cbd4ce", min(125, alpha)), width=4)
            draw.line((roof[0], roof[2]), fill=rgba(CORAL, min(105, alpha)), width=6)

    outline_color = palette["trim"] if outline_only else palette["line"]
    outline_alpha = 235 if outline_only else min(190, alpha)
    draw.line(roof + [roof[0]], fill=rgba(outline_color, outline_alpha), width=3 if outline_only else 2, joint="curve")
    if outline_only:
        draw.line((roof[1], foot[1]), fill=rgba(outline_color, outline_alpha), width=2)
        draw.line((roof[2], foot[2]), fill=rgba(outline_color, outline_alpha), width=2)
        draw.line((roof[3], foot[3]), fill=rgba(outline_color, outline_alpha), width=2)


def building_zones(tactical: dict) -> list[dict]:
    return [zone for zone in tactical["terrain_zones"] if zone["kind"] == "building"]


def building_height(candidate: Candidate, index: int) -> int:
    bases = {"A": (82, 112, 96, 90, 100, 86), "B": (118, 132, 106, 102, 118, 96), "C": (146, 164, 126, 138, 155, 120)}
    return bases[candidate.code][index % len(bases[candidate.code])]


def draw_buildings(
    canvas: Image.Image,
    tactical: dict,
    candidate: Candidate,
    project: Callable[[float, float], tuple[int, int]],
    *,
    alpha: int = 255,
    outline_only: bool = False,
) -> None:
    zones = sorted(building_zones(tactical), key=lambda item: item["rect"][0] + item["rect"][1])
    for index, zone in enumerate(zones):
        draw_building_volume(
            canvas, candidate, project, zone["rect"], building_height(candidate, index), index,
            alpha=alpha, outline_only=outline_only,
        )


def draw_broken_corridor(
    canvas: Image.Image,
    candidate: Candidate,
    project: Callable[[float, float], tuple[int, int]],
    *,
    alpha: int = 255,
    outline_only: bool = False,
) -> None:
    palette = candidate_palette(candidate)
    draw = ImageDraw.Draw(canvas, "RGBA")
    left = rect_footprint_polygon(project, [8, 5, 4, 2])
    right = rect_footprint_polygon(project, [13, 5, 3, 2])
    height = {"A": 58, "B": 70, "C": 88}[candidate.code]
    for index, foot in enumerate((left, right)):
        roof = [(x, y - height - index * 5) for x, y in foot]
        if not outline_only:
            draw.polygon([roof[1], roof[2], foot[2], foot[1]], fill=rgba("#26383f", alpha))
            draw.polygon([roof[2], roof[3], foot[3], foot[2]], fill=rgba("#1b2d34", alpha))
            draw.polygon(roof, fill=rgba(palette["corridor"], alpha))
        draw.line(roof + [roof[0]], fill=rgba(palette["trim"], 230 if outline_only else min(180, alpha)), width=3)
    # Broken center remains visually closed by collapsed truss, matching blocked topology.
    a = project(11.4, 5.6)
    b = project(13.0, 5.8)
    draw.line((a[0], a[1] - height, b[0], b[1] - height + 18), fill=rgba(CORAL, min(215, alpha)), width=9)
    draw.line((a[0] + 15, a[1] - height + 24, b[0] - 10, b[1] - height - 5), fill=rgba(palette["trim"], min(165, alpha)), width=5)


def draw_static_world_objects(
    canvas: Image.Image,
    tactical: dict,
    candidate: Candidate,
    project: Callable[[float, float], tuple[int, int]],
) -> None:
    palette = candidate_palette(candidate)
    draw = ImageDraw.Draw(canvas, "RGBA")
    for object_data in tactical["destructibles"]:
        x, y = object_data["anchor"]
        cx, cy = project(x, y)
        state = object_data.get("state", "intact")
        color = "#a98555" if state == "intact" else "#bb6251"
        draw.polygon([(cx, cy - 28), (cx + 12, cy - 16), (cx + 9, cy), (cx - 9, cy), (cx - 12, cy - 16)], fill=rgba(color, 235))
        draw.line((cx - 12, cy - 16, cx + 12, cy - 16), fill=rgba(palette["trim"], 185), width=2)

    # Open shield rack at the approved M2 hotspot: interaction source, not a final shield asset.
    sx, sy = tactical["shield_hotspot"]
    cx, cy = project(sx, sy)
    draw.line((cx - 29, cy - 46, cx - 23, cy + 8), fill=rgba("#473d32", 255), width=7)
    draw.line((cx + 29, cy - 46, cx + 23, cy + 8), fill=rgba("#473d32", 255), width=7)
    draw.line((cx - 30, cy - 46, cx + 30, cy - 46), fill=rgba(GOLD, 235), width=5)
    draw.polygon(
        [(cx, cy - 43), (cx + 18, cy - 27), (cx + 14, cy + 4), (cx, cy + 16), (cx - 14, cy + 4), (cx - 18, cy - 27)],
        fill=rgba("#3c4c50", 245), outline=rgba(GOLD, 230),
    )


def footprint_center(
    project: Callable[[float, float], tuple[int, int]], anchor: list[int], footprint: list[int]
) -> tuple[int, int]:
    return project(anchor[0] + (footprint[0] - 1) / 2, anchor[1] + (footprint[1] - 1) / 2)


def draw_guardian_token(draw: ImageDraw.ImageDraw, center: tuple[int, int], scale: float = 1.0, *, outline_only: bool = False) -> None:
    cx, cy = center
    s = scale
    if not outline_only:
        draw.polygon([(cx - 22*s, cy - 61*s), (cx + 22*s, cy - 61*s), (cx + 32*s, cy - 25*s), (cx + 20*s, cy - 3*s), (cx - 20*s, cy - 3*s), (cx - 32*s, cy - 25*s)], fill=rgba("#365e72", 255))
        draw.polygon([(cx - 9*s, cy - 77*s), (cx + 9*s, cy - 77*s), (cx + 14*s, cy - 61*s), (cx - 14*s, cy - 61*s)], fill=rgba("#d7ddd5", 255))
        draw.polygon([(cx - 46*s, cy - 53*s), (cx - 24*s, cy - 49*s), (cx - 30*s, cy - 15*s), (cx - 48*s, cy - 19*s)], fill=rgba("#d14e46", 255))
        draw.polygon([(cx + 46*s, cy - 53*s), (cx + 24*s, cy - 49*s), (cx + 30*s, cy - 15*s), (cx + 48*s, cy - 19*s)], fill=rgba("#d14e46", 255))
        draw.rectangle((cx - 19*s, cy - 30*s, cx + 19*s, cy - 20*s), fill=rgba(GOLD, 255))
        draw.rectangle((cx - 27*s, cy - 4*s, cx - 7*s, cy + 30*s), fill=rgba("#315468", 255))
        draw.rectangle((cx + 7*s, cy - 4*s, cx + 27*s, cy + 30*s), fill=rgba("#315468", 255))
    draw.line([(cx - 46*s, cy - 53*s), (cx - 24*s, cy - 49*s), (cx - 20*s, cy - 61*s), (cx + 20*s, cy - 61*s), (cx + 24*s, cy - 49*s), (cx + 46*s, cy - 53*s)], fill=rgba(CYAN, 245), width=max(2, round(3*s)), joint="curve")


def draw_breaker_token(draw: ImageDraw.ImageDraw, center: tuple[int, int], scale: float = 1.0, *, outline_only: bool = False) -> None:
    cx, cy = center
    s = scale
    body = [(cx - 63*s, cy - 57*s), (cx - 22*s, cy - 86*s), (cx + 48*s, cy - 69*s), (cx + 70*s, cy - 35*s), (cx + 50*s, cy - 6*s), (cx - 54*s, cy - 6*s), (cx - 74*s, cy - 31*s)]
    if not outline_only:
        draw.polygon(body, fill=rgba("#182127", 255))
        for dx in (-52, -20, 25, 54):
            draw.ellipse((cx + (dx-14)*s, cy - 26*s, cx + (dx+14)*s, cy + 12*s), fill=rgba("#242e34", 255))
        draw.line((cx - 34*s, cy - 55*s, cx + 20*s, cy - 53*s), fill=rgba(RED, 255), width=max(3, round(6*s)))
    draw.line(body + [body[0]], fill=rgba("#d45b55", 240), width=max(2, round(3*s)), joint="curve")


def draw_swarm_token(draw: ImageDraw.ImageDraw, center: tuple[int, int], index: int, scale: float = 1.0, *, outline_only: bool = False) -> None:
    cx, cy = center
    s = scale
    angle = (index * 53 + 17) % 360
    points = []
    for radius, offset in ((19, 0), (10, 74), (17, 158), (9, 248)):
        rad = math.radians(angle + offset)
        points.append((cx + math.cos(rad)*radius*s, cy - 12*s + math.sin(rad)*radius*s*0.62))
    if not outline_only:
        draw.polygon(points, fill=rgba("#9c4a37", 255))
        draw.ellipse((cx - 6*s, cy - 17*s, cx + 6*s, cy - 5*s), fill=rgba(ORANGE, 255))
    draw.line(points + [points[0]], fill=rgba("#f0a066", 240), width=max(2, round(2*s)))


def draw_vehicle_token(draw: ImageDraw.ImageDraw, center: tuple[int, int], index: int, scale: float = 1.0) -> None:
    cx, cy = center
    s = scale
    fill = "#d6a53b" if index % 2 == 0 else "#d8dcd5"
    draw.rounded_rectangle((cx - 24*s, cy - 24*s, cx + 24*s, cy - 5*s), radius=max(2, round(5*s)), fill=rgba(fill, 255), outline=rgba(INK_DEEP, 240), width=2)
    draw.rectangle((cx + 7*s, cy - 31*s, cx + 19*s, cy - 24*s), fill=rgba(CORAL, 255))
    draw.ellipse((cx - 18*s, cy - 8*s, cx - 8*s, cy + 2*s), fill=rgba("#192a31", 255))
    draw.ellipse((cx + 8*s, cy - 8*s, cx + 18*s, cy + 2*s), fill=rgba("#192a31", 255))


def draw_target_token(draw: ImageDraw.ImageDraw, center: tuple[int, int], kind: str, scale: float = 1.0) -> None:
    cx, cy = center
    s = scale
    color = GREEN if kind == "evacuation_exit" else "#8ba6ce"
    draw.rectangle((cx - 18*s, cy - 43*s, cx + 18*s, cy), fill=rgba("#23373e", 255), outline=rgba(color, 245), width=max(2, round(3*s)))
    draw.line((cx - 13*s, cy - 25*s, cx + 13*s, cy - 25*s), fill=rgba(color, 235), width=max(2, round(3*s)))


def draw_units(
    canvas: Image.Image,
    tactical: dict,
    project: Callable[[float, float], tuple[int, int]],
    *,
    density: str = "MID",
    outline_only: bool = False,
) -> None:
    draw = ImageDraw.Draw(canvas, "RGBA")
    units = [unit for unit in tactical["units"] if unit["kind"] != "swarm"]
    units.sort(key=lambda unit: sum(unit["anchor"]))
    for index, unit in enumerate(units):
        center = footprint_center(project, unit["anchor"], unit.get("footprint", [1, 1]))
        kind = unit["kind"]
        if kind == "guardian":
            draw_guardian_token(draw, center, 0.82, outline_only=outline_only)
        elif kind == "boss":
            draw_breaker_token(draw, center, 0.95, outline_only=outline_only)
        elif kind == "emergency_vehicle" and not outline_only:
            draw_vehicle_token(draw, center, index, 0.9)
        elif kind in ("evacuation_exit", "security_target") and not outline_only:
            draw_target_token(draw, center, kind, 0.9)

    for index, anchor in enumerate(DENSITY_ANCHORS[density]):
        draw_swarm_token(draw, project(anchor[0], anchor[1]), index, 0.92, outline_only=outline_only)


def draw_weather(canvas: Image.Image, candidate: Candidate, *, strength: float = 1.0) -> None:
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(candidate.seed + canvas.size[0] * 7 + canvas.size[1])
    count = int({"A": 50, "B": 64, "C": 94}[candidate.code] * strength)
    for _ in range(count):
        x = rng.randint(0, canvas.size[0] - 1)
        y = rng.randint(0, canvas.size[1] - 1)
        length = rng.randint(8, 22)
        alpha = rng.randint(24, 58) if candidate.code != "C" else rng.randint(36, 76)
        draw.line((x, y, x - 5, y + length), fill=(205, 222, 219, alpha), width=1)
    if candidate.code == "C":
        haze = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        haze_draw = ImageDraw.Draw(haze, "RGBA")
        haze_draw.ellipse((canvas.size[0]*0.55, canvas.size[1]*0.52, canvas.size[0]*0.92, canvas.size[1]*0.83), fill=(224, 116, 65, 28))
        haze = haze.filter(ImageFilter.GaussianBlur(32))
        layer = Image.alpha_composite(layer, haze)
    canvas.alpha_composite(layer)


def render_world_layer(
    tactical: dict,
    candidate: Candidate,
    project: Callable[[float, float], tuple[int, int]],
    size: tuple[int, int],
    *,
    density: str = "MID",
    show_units: bool = True,
    show_weather: bool = True,
    defer_corridor: bool = False,
    occlusion_mode: str = "none",
) -> Image.Image:
    palette = candidate_palette(candidate)
    canvas = Image.new("RGBA", size, rgba(palette["background"], 255))
    draw_ground(canvas, tactical, candidate, project)
    draw_buildings(canvas, tactical, candidate, project)
    if not defer_corridor:
        draw_broken_corridor(canvas, candidate, project)
    draw_static_world_objects(canvas, tactical, candidate, project)
    if show_units:
        draw_units(canvas, tactical, project, density=density)
    if defer_corridor:
        if occlusion_mode == "fade":
            draw_broken_corridor(canvas, candidate, project, alpha=64)
        elif occlusion_mode == "fade_outline":
            draw_broken_corridor(canvas, candidate, project, alpha=42)
            draw_broken_corridor(canvas, candidate, project, outline_only=True)
            draw_units(canvas, tactical, project, density=density, outline_only=True)
        else:
            draw_broken_corridor(canvas, candidate, project, alpha=255)
    if show_weather:
        draw_weather(canvas, candidate)
    return canvas


def render_viewport(
    tactical: dict,
    candidate: Candidate,
    camera: tuple[float, float],
    *,
    density: str = "MID",
    pure: bool = True,
    occlusion_mode: str = "fade_outline",
) -> Image.Image:
    view_project = viewport_projector(camera)
    view = render_world_layer(
        tactical, candidate, view_project, TACTICAL_SIZE,
        density=density, show_units=True, show_weather=True,
        defer_corridor=True, occlusion_mode=occlusion_mode,
    )
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), rgba("#0b171d", 255))
    canvas.alpha_composite(view, (0, 54))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle(TOP_HUD, fill=rgba("#0a151b", 255))
    draw.rectangle(BOTTOM_HUD, fill=rgba("#0a151b", 255))
    draw.rectangle(UI_RECT, fill=rgba("#102129", 255))
    draw.rectangle((915, 70, 1260, 207), fill=rgba("#1a151a", 255), outline=rgba(RED, 210), width=2)
    draw.rectangle((915, 219, 1260, 634), fill=rgba("#0d1b21", 255), outline=rgba("#397885", 210), width=2)
    for rect in ((933, 405, 1075, 443), (1092, 405, 1234, 443), (933, 455, 1075, 493), (1092, 455, 1234, 493), (933, 505, 1075, 543), (1092, 505, 1234, 543)):
        draw.rectangle(rect, outline=rgba(GOLD, 190), width=2)
    if not pure:
        draw.text((18, 15), candidate.stable_id, font=font(15, bold=True), fill=IVORY)
        draw.text((1018, 673), "Candidate / no handoff", font=font(15), fill=GOLD)
    return canvas.convert("RGB")


def camera_world_rect(camera: tuple[float, float]) -> tuple[int, int, int, int]:
    return (
        round(camera[0] - TACTICAL_SIZE[0] / 2),
        round(camera[1] - TACTICAL_SIZE[1] / 2),
        round(camera[0] + TACTICAL_SIZE[0] / 2),
        round(camera[1] + TACTICAL_SIZE[1] / 2),
    )


def draw_review_overlays(
    canvas: Image.Image,
    tactical: dict,
    candidate: Candidate,
    project: Callable[[float, float], tuple[int, int]],
) -> None:
    draw = ImageDraw.Draw(canvas, "RGBA")
    # Camera crop frames are review overlays only.
    camera_colors = (TEAL, GOLD, CORAL)
    for index, (_, camera_id, camera, _) in enumerate(REVIEW_CAMERAS):
        x0w, y0w, x1w, y1w = camera_world_rect(camera)
        x0, y0 = round(880 + x0w), round(170 + y0w)
        x1, y1 = round(880 + x1w), round(170 + y1w)
        draw.rectangle((x0, y0, x1, y1), outline=rgba(camera_colors[index], 220), width=4)
        draw.rectangle((x0 + 8, y0 + 8, x0 + 178, y0 + 42), fill=rgba(INK_DEEP, 225))
        draw.text((x0 + 18, y0 + 14), camera_id, font=font(17, bold=True), fill=camera_colors[index])

    # Functional arrows are not baked into runtime map layers.
    north = project(8, 0)
    draw.line((north[0], north[1] - 130, north[0], north[1] - 28), fill=rgba(GREEN, 235), width=7)
    draw.polygon([(north[0], north[1] - 150), (north[0] - 13, north[1] - 126), (north[0] + 13, north[1] - 126)], fill=rgba(GREEN, 235))
    draw.text((north[0] - 125, north[1] - 190), "北侧：万机馆 / 居民区保护面", font=font(21, bold=True), fill=GREEN)

    east = project(30, 4)
    draw.line((east[0] - 30, east[1] - 75, east[0] + 95, east[1] - 75), fill=rgba(GOLD, 240), width=7)
    draw.polygon([(east[0] + 115, east[1] - 75), (east[0] + 90, east[1] - 88), (east[0] + 90, east[1] - 62)], fill=rgba(GOLD, 240))
    draw.text((east[0] - 80, east[1] - 119), "东侧 rescue_lane / 最后车辆", font=font(21, bold=True), fill=GOLD)

    south = project(23, 16)
    draw.line((south[0], south[1] + 84, south[0], south[1] + 16), fill=rgba(CORAL, 238), width=7)
    draw.polygon([(south[0], south[1] - 4), (south[0] - 13, south[1] + 20), (south[0] + 13, south[1] + 20)], fill=rgba(CORAL, 238))
    draw.text((south[0] - 105, south[1] + 92), "南侧 BREAKER 来向", font=font(21, bold=True), fill=CORAL)

    shield = project(*tactical["shield_hotspot"])
    draw.line((shield[0] - 120, shield[1] - 118, shield[0] - 18, shield[1] - 33), fill=rgba(GOLD, 220), width=3)
    draw.text((shield[0] - 320, shield[1] - 155), "馆侧退役重盾取得点", font=font(21, bold=True), fill=GOLD)


def render_full_domain(
    tactical: dict,
    candidate: Candidate,
    topology_signature: str,
    *,
    pure: bool,
    density: str = "MID",
) -> Image.Image:
    project = overview_projector()
    canvas = render_world_layer(
        tactical, candidate, project, (2400, 1350), density=density,
        show_units=True, show_weather=True, defer_corridor=True, occlusion_mode="fade_outline",
    )
    if pure:
        return canvas.convert("RGB")

    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, 2399, 104), fill=rgba(INK_DEEP, 242))
    draw.text((46, 24), f"MAP-{candidate.code}  {candidate.title}", font=font(35, bold=True), fill=IVORY)
    draw.text((1535, 34), "32x18 rolling topology / Candidate", font=font(20), fill=candidate.accent)
    draw_review_overlays(canvas, tactical, candidate, project)
    draw.rectangle((0, 1190, 2399, 1349), fill=rgba("#0c1a20", 242))
    draw.text((46, 1213), "全域关系", font=font(22, bold=True), fill=candidate.accent)
    draw.text((196, 1214), "西侧起步 / 中央主战 / 东侧撤离相邻且有重叠视口；道路、建筑、连廊、设施与可破坏物全部在棋盘世界内。", font=font(20), fill=PAPER)
    draw.text((46, 1254), "几何锁", font=font(22, bold=True), fill=candidate.accent)
    draw.text((196, 1256), f"{TACTICAL_PROFILE_ID}  |  topology {topology_signature[:16]}  |  runtime_allowed=false", font=font(19), fill="#b8c6c3")
    draw.text((46, 1297), "证据边界", font=font(22, bold=True), fill=candidate.accent)
    draw.text((196, 1299), "馆守Z、BREAKER、重盾与小体均为几何 token；不是 Sprite Master，不授权 Godot 导入。", font=font(19), fill="#b8c6c3")
    return canvas.convert("RGB")


def fit_image(image: Image.Image, size: tuple[int, int], *, background: str = "#0a171d") -> Image.Image:
    source = image.convert("RGB")
    scale = min(size[0] / source.width, size[1] / source.height)
    resized = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, background)
    canvas.paste(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
    return canvas


def make_continuity_strip(candidate: Candidate, viewports: dict[str, Image.Image]) -> Image.Image:
    strip = Image.new("RGB", (3840, 820), INK_DEEP)
    draw = ImageDraw.Draw(strip)
    labels = {"WEST": "WEST / 馆守Z + 取盾", "CENTRAL": "CENTRAL / Boss + 多向压力", "EAST": "EAST / rescue_lane + 最后车辆"}
    colors = {"WEST": TEAL, "CENTRAL": GOLD, "EAST": CORAL}
    for index, key in enumerate(("WEST", "CENTRAL", "EAST")):
        x = index * 1280
        draw.rectangle((x, 0, x + 1279, 99), fill=INK_DEEP)
        draw.text((x + 34, 28), labels[key], font=font(25, bold=True), fill=colors[key])
        draw.text((x + 830, 36), "shared topology / overlapping crop", font=font(17), fill="#aab9b6")
        strip.paste(viewports[key], (x, 100))
        if index < 2:
            draw.rectangle((x + 1269, 0, x + 1279, 819), fill=colors[key])
    return strip


def make_pure_read_triptych(pure_maps: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGB", (2400, 900), "#071319")
    widths = (800, 800, 800)
    for index, candidate in enumerate(CANDIDATES):
        preview = fit_image(pure_maps[candidate.code], (widths[index], 900))
        board.paste(preview, (sum(widths[:index]), 0))
    # No report text, labels or icons are drawn on this file.
    return board


def make_direction_board(
    tactical: dict,
    topology_signature: str,
    full_maps: dict[str, Image.Image],
    continuity: dict[str, Image.Image],
) -> Image.Image:
    board = Image.new("RGB", (3000, 1800), "#e9eeeb")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2999, 112), fill=INK_DEEP)
    draw.text((52, 27), "C01E02 A2 | 滚动旧会展街区布局三方向", font=font(39, bold=True), fill=PAPER)
    draw.text((2370, 39), "Candidate / no Runtime handoff", font=font(21), fill=GOLD)

    column_w = 960
    gap = 20
    left = 40
    for index, candidate in enumerate(CANDIDATES):
        x = left + index * (column_w + gap)
        draw.rectangle((x, 136, x + column_w, 1748), fill="#f8f9f5", outline="#a7b3b1", width=2)
        draw.rectangle((x, 136, x + column_w, 210), fill=candidate.accent)
        draw.text((x + 24, 155), f"MAP-{candidate.code}  {candidate.title}", font=font(27, bold=True), fill=INK_DEEP)

        preview = fit_image(full_maps[candidate.code], (912, 513))
        board.paste(preview, (x + 24, 234))
        draw.rectangle((x + 24, 234, x + 935, 746), outline=INK_DEEP, width=2)

        strip_preview = fit_image(continuity[candidate.code], (912, 195))
        board.paste(strip_preview, (x + 24, 770))
        draw.rectangle((x + 24, 770, x + 935, 964), outline=INK_DEEP, width=2)

        y = 994
        fields = (
            ("场景身份", candidate.identity),
            ("空间组织", candidate.spatial_organization),
            ("视觉语言", candidate.visual_language),
            ("优点", candidate.strength),
            ("风险", candidate.risk),
            ("资产量", candidate.asset_volume),
            ("程序要求", candidate.runtime_tech),
        )
        for label, value in fields:
            draw.text((x + 27, y), label, font=font(19, bold=True), fill=candidate.accent)
            y = draw_wrapped(draw, (x + 158, y - 2), value, 754, 18, INK, spacing=3) + 6
        draw.rectangle((x + 24, 1672, x + 936, 1722), fill="#102128")
        draw.text((x + 38, 1686), f"{TACTICAL_PROFILE_ID} | topology {topology_signature[:12]}", font=font(17), fill="#b7c6c3")

    draw.text((52, 1765), "三案共用 32x18 玩法拓扑、单位坐标、可破坏物、胜负与剧情结果；只改场景身份、建筑语汇、明暗与遮挡分组。", font=font(20), fill=INK_SOFT)
    return board


def render_neutral_occlusion_view(
    tactical: dict,
    candidate: Candidate,
    mode: str,
) -> Image.Image:
    # Camera centers the approved swarm token that occupies the broken skywalk zone.
    camera = (260, 300)
    project = viewport_projector(camera)
    view = render_world_layer(
        tactical, candidate, project, (900, 594), density="MID",
        show_units=True, show_weather=False, defer_corridor=True, occlusion_mode=mode,
    )
    return view.convert("RGB")


def make_occlusion_board(tactical: dict, topology_signature: str) -> Image.Image:
    neutral = CANDIDATES[1]
    board = Image.new("RGB", (2400, 1350), "#e8edeb")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2399, 100), fill=INK_DEEP)
    draw.text((46, 25), "A2 遮挡 / UI 安全区用户选择", font=font(35, bold=True), fill=PAPER)
    draw.text((1770, 35), "topology locked / art rule pending", font=font(19), fill=GOLD)

    modes = (
        ("fade", "A  纯淡出", "屋顶/连廊进入单位、路径或意图区时降到约25%不透明度。", TEAL),
        ("fade_outline", "B  淡出 + 轮廓", "建筑降低至约18%，同时保留屋檐和被遮单位外轮廓。", GOLD),
    )
    for index, (mode, title, body, accent) in enumerate(modes):
        x = 50 + index * 790
        draw.rectangle((x, 135, x + 750, 870), fill="#f8f9f5", outline="#aab6b4", width=2)
        draw.rectangle((x, 135, x + 750, 202), fill=accent)
        draw.text((x + 23, 153), title, font=font(27, bold=True), fill=INK_DEEP)
        preview = fit_image(render_neutral_occlusion_view(tactical, neutral, mode), (702, 463))
        board.paste(preview, (x + 24, 228))
        draw.rectangle((x + 24, 228, x + 725, 690), outline=INK_DEEP, width=2)
        draw_wrapped(draw, (x + 28, 722), body, 690, 20, INK, spacing=5)
        draw.text((x + 28, 814), "collision_semantic = unchanged", font=font(17), fill=INK_SOFT)

    x = 1630
    draw.rectangle((x, 135, 2350, 870), fill="#f8f9f5", outline="#aab6b4", width=2)
    draw.rectangle((x, 135, 2350, 202), fill=CORAL)
    draw.text((x + 23, 153), "硬安全区", font=font(27, bold=True), fill=INK_DEEP)
    safe = Image.new("RGB", (672, 463), "#0b171d")
    sd = ImageDraw.Draw(safe)
    sd.rectangle((0, 0, 671, 41), fill="#3e3b6a", outline="#b9b2de", width=2)
    sd.rectangle((0, 413, 671, 462), fill="#3e3b6a", outline="#b9b2de", width=2)
    sd.rectangle((474, 42, 671, 412), fill="#17313a", outline="#5b9aac", width=2)
    sd.rectangle((18, 62, 453, 392), fill="#31484f", outline="#789095", width=2)
    sd.line((38, 330, 430, 122), fill=GREEN, width=7)
    sd.ellipse((196, 205, 240, 249), fill=CYAN, outline=PAPER, width=3)
    sd.polygon([(430, 122), (404, 123), (417, 145)], fill=GREEN)
    board.paste(safe, (x + 24, 228))
    draw.text((x + 28, 722), "地图只进入 900x594 内容区；屋顶、雨棚与镜头边缘不进入顶/底 HUD 或右侧 UI。", font=font(19), fill=INK)
    draw.text((x + 28, 789), "路径、选中、敌方意图和目标提示永远绘制在遮挡层上方。", font=font(19), fill=INK)

    draw.rectangle((50, 915, 2350, 1300), fill="#102129")
    rows = (
        ("触发", "建筑屋顶/连廊与已选单位、预览路径、意图目标的屏幕包围盒相交"),
        ("分组", "按展馆体块分组，不以单格闪烁；连廊独立分组"),
        ("镜头边缘", "建筑可被裁切，选中点、脚点和操作路径不能被裁切"),
        ("所有权", "程序拥有选中/路径/意图/UI；美术只提供建筑组、淡出 mask 与轮廓 mask"),
    )
    y = 945
    for label, value in rows:
        draw.text((86, y), label, font=font(20, bold=True), fill=GOLD)
        draw.text((250, y), value, font=font(19), fill=PAPER)
        y += 74
    draw.text((1835, 1264), f"topology {topology_signature[:14]}", font=font(16), fill="#81989b")
    return board


def make_density_board(tactical: dict, topology_signature: str) -> Image.Image:
    candidate = CANDIDATES[0]
    board = Image.new("RGB", (2400, 1000), "#e9eeeb")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2399, 96), fill=INK_DEEP)
    draw.text((45, 24), "A2 小体压力密度 | 仅布局数量，不是造型批准", font=font(33, bold=True), fill=PAPER)
    draw.text((1970, 35), "all scattered", font=font(20), fill=ORANGE)
    labels = {
        "LOW": ("低  4 token", "双线压力较轻，玩家更容易聚焦 Boss 与撤离。"),
        "MID": ("中  6 token", "沿用当前 M2 六个散乱锚点，西/中/东均有局部压力。"),
        "HIGH": ("高  9 token", "压力路线最多，需更强轮廓、LOD 与意图提示。"),
    }
    for index, key in enumerate(("LOW", "MID", "HIGH")):
        x = 45 + index * 785
        draw.rectangle((x, 125, x + 740, 935), fill="#f8f9f5", outline="#a9b5b3", width=2)
        draw.rectangle((x, 125, x + 740, 187), fill=(TEAL if key == "LOW" else GOLD if key == "MID" else CORAL))
        draw.text((x + 22, 143), labels[key][0], font=font(25, bold=True), fill=INK_DEEP)
        project = overview_projector()
        map_image = render_world_layer(tactical, candidate, project, (2400, 1350), density=key, show_units=True, show_weather=False, defer_corridor=True, occlusion_mode="fade_outline")
        preview = fit_image(map_image, (692, 574))
        board.paste(preview, (x + 24, 211))
        draw.rectangle((x + 24, 211, x + 715, 784), outline=INK_DEEP, width=2)
        draw_wrapped(draw, (x + 27, 812), labels[key][1], 684, 18, INK, spacing=4)
    draw.text((45, 962), f"三档均不排队、不组成箭头、不围绕 Boss 同步；具体数值继续属于 Demo 平衡参数。 topology {topology_signature[:12]}", font=font(18), fill=INK_SOFT)
    return board


def write_tsv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def candidate_filename(candidate: Candidate, suffix: str) -> str:
    return f"A2_MAP_{candidate.code}_{suffix}"


def write_candidate_spec(topology_signature: str) -> None:
    rows = []
    for candidate in CANDIDATES:
        rows.append({
            "candidate_id": candidate.stable_id,
            "map_slot": MAP_SLOT,
            "candidate_code": f"MAP-{candidate.code}",
            "title": candidate.title,
            "scene_identity": candidate.identity,
            "spatial_organization": candidate.spatial_organization,
            "visual_language": candidate.visual_language,
            "strength": candidate.strength,
            "risk": candidate.risk,
            "asset_volume": candidate.asset_volume,
            "runtime_technical_requirement": candidate.runtime_tech,
            "tactical_profile_id": TACTICAL_PROFILE_ID,
            "topology_signature": topology_signature,
            "grid": "32x18",
            "viewport": "900x594 inside 1280x720",
            "swarm_organization_state": "scattered",
            "art_language": "A_KINETIC_CEL_layout_prototype",
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "user_decision_required": "true",
        })
    write_tsv(OUT / "candidate-spec.tsv", list(rows[0].keys()), rows)


def write_camera_spec(topology_signature: str) -> None:
    rows = []
    for order, (code, stable_id, center, intent) in enumerate(REVIEW_CAMERAS, start=1):
        rect = camera_world_rect(center)
        rows.append({
            "order": order,
            "camera_code": code,
            "stable_id": stable_id,
            "review_center_world": f"{center[0]},{center[1]}",
            "review_world_rect": f"{rect[0]},{rect[1]},{rect[2]},{rect[3]}",
            "screen_rect": "0,54,900,594",
            "continuity_intent": intent,
            "previous_overlap_world_x": "n/a" if order == 1 else ("500" if order == 2 else "310"),
            "runtime_camera_owner": "M2_program_smooth_scroll",
            "review_camera_is_runtime_lock": "false",
            "topology_signature": topology_signature,
            "runtime_allowed": "false",
            "runtime_handoff": "none",
        })
    write_tsv(OUT / "camera-continuity.tsv", list(rows[0].keys()), rows)


def write_topology_receipt(tactical: dict, topology_signature: str) -> None:
    rows: list[dict[str, object]] = []
    for zone in tactical["terrain_zones"]:
        rows.append({
            "record_kind": "terrain_zone",
            "stable_id": zone["zone_id"],
            "kind": zone["kind"],
            "anchor_or_rect": ",".join(map(str, zone["rect"])),
            "footprint_or_route": "n/a",
            "passable": str(zone["passable"]).lower(),
            "organization_state": "n/a",
            "source_profile": TACTICAL_PROFILE_ID,
            "topology_signature": topology_signature,
            "art_change_allowed": "material_height_grouping_only",
        })
    for unit in tactical["units"]:
        rows.append({
            "record_kind": "unit_or_target",
            "stable_id": unit["unit_id"],
            "kind": unit["kind"],
            "anchor_or_rect": ",".join(map(str, unit["anchor"])),
            "footprint_or_route": ",".join(map(str, unit.get("footprint", [1, 1]))) + ("|route=" + ";".join(",".join(map(str, point)) for point in unit.get("route", [])) if unit.get("route") else ""),
            "passable": "n/a",
            "organization_state": "scattered" if unit["kind"] == "swarm" else "n/a",
            "source_profile": TACTICAL_PROFILE_ID,
            "topology_signature": topology_signature,
            "art_change_allowed": "geometry_token_only",
        })
    for object_data in tactical["destructibles"]:
        rows.append({
            "record_kind": "destructible",
            "stable_id": object_data["object_id"],
            "kind": object_data["kind"],
            "anchor_or_rect": ",".join(map(str, object_data["anchor"])),
            "footprint_or_route": "1x1",
            "passable": "profile_owned",
            "organization_state": "n/a",
            "source_profile": TACTICAL_PROFILE_ID,
            "topology_signature": topology_signature,
            "art_change_allowed": "large_shape_candidate_only",
        })
    fields = list(rows[0].keys())
    write_tsv(OUT / "topology-receipt.tsv", fields, rows)


def write_density_spec(topology_signature: str) -> None:
    rows = []
    for key in ("LOW", "MID", "HIGH"):
        rows.append({
            "density_option": key,
            "token_count": len(DENSITY_ANCHORS[key]),
            "anchors": ";".join(f"{x},{y}" for x, y in DENSITY_ANCHORS[key]),
            "organization_state": "scattered",
            "queue_or_arrow_formation": "false",
            "boss_synchronization": "false",
            "design_approval": "layout_density_only_not_mecha_design",
            "topology_signature": topology_signature,
            "runtime_allowed": "false",
            "runtime_handoff": "none",
        })
    write_tsv(OUT / "swarm-density-spec.tsv", list(rows[0].keys()), rows)


def write_occlusion_spec(topology_signature: str) -> None:
    rows = [
        {
            "rule_id": "A2_OCCLUSION_FADE_ONLY",
            "candidate_mode": "pure_fade",
            "trigger": "building_group_or_corridor_intersects_selected_unit_path_intent_bbox",
            "building_alpha": "0.25_candidate",
            "outline": "none",
            "z_order": "environment_occluder_below_program_path_intent",
            "safe_area": "content_only_0,54,900,594",
            "collision_semantic": "unchanged_profile_owned",
            "user_decision_required": "true",
        },
        {
            "rule_id": "A2_OCCLUSION_FADE_PLUS_OUTLINE",
            "candidate_mode": "fade_plus_outline",
            "trigger": "building_group_or_corridor_intersects_selected_unit_path_intent_bbox",
            "building_alpha": "0.18_candidate",
            "outline": "roof_edge_and_occluded_unit_outer_contour",
            "z_order": "environment_fill_below_program_path_intent_outline_above_fill",
            "safe_area": "content_only_0,54,900,594",
            "collision_semantic": "unchanged_profile_owned",
            "user_decision_required": "true",
        },
        {
            "rule_id": "A2_CAMERA_EDGE_UI_SAFE",
            "candidate_mode": "hard_rule",
            "trigger": "always",
            "building_alpha": "n/a",
            "outline": "n/a",
            "z_order": "map_clipped_before_HUD_and_right_UI",
            "safe_area": "top_0..54;bottom_648..720;right_900..1280",
            "collision_semantic": "unchanged_profile_owned",
            "user_decision_required": "false",
        },
    ]
    for row in rows:
        row.update({
            "topology_signature": topology_signature,
            "runtime_allowed": "false",
            "runtime_handoff": "none",
        })
    write_tsv(OUT / "occlusion-rule.tsv", list(rows[0].keys()), rows)


def write_source_receipt() -> None:
    rows = []
    notes = {
        "candidate_gameflow": "Reader/producer contract override the stale evacuation-before-shield sentence; layout only, no temporal order encoded",
        "live_m2_graybox_topology": "read-only shared topology; no Godot write; 32x18 rolling map",
        "guardian_direction_receipt": "A1-C derivative direction only; geometry token here; not Sprite Master",
        "breaker_direction_receipt": "B silhouette + X direction only; geometry token here; not final B+X master",
        "shield_direction_receipt": "A tower + F parameter direction only; geometry token here; not final A+F master",
        "canon_scenes": "current row contains stale evacuation-before-shield sequence residual; revision-2 contract and accepted Reader control implementation order; A2 remains spatial only",
        "wanji_external_zone": "hard spatial anchor read only; E04 berth/ship mechanisms remain locked and are not designed in A2",
    }
    for path, digest, role, status in SOURCE_LOCKS:
        observed_digest = sha256_file(ROOT / path) if digest is None else digest
        validation = "PASS_scoped_semantics_observed_sha256" if digest is None else "PASS_exact_sha256"
        rows.append({
            "source_path": path,
            "sha256": observed_digest,
            "role": role,
            "source_status": status,
            "active_source": "true",
            "validation": validation,
            "use_boundary": notes.get(role, "read_only_authority_or_art_direction"),
            "runtime_source": "false",
        })
    write_tsv(OUT / "source-receipt.tsv", list(rows[0].keys()), rows)


def write_superseded_ledger() -> None:
    rows = []
    for path, digest, classification in SUPERSEDED_ITEMS:
        rows.append({
            "history_item": path,
            "dispatch_sha256_or_na": digest,
            "classification": classification,
            "active_source": "false",
            "allowed_use": "audit_trace_only",
            "forbidden_use": "decision_board;active_manifest_source;runtime;fallback;topology",
            "superseding_authority": f"{CONTRACT_PATH}#{CONTRACT_SHA256}",
            "modified_by_A2": "false",
        })
    write_tsv(OUT / "superseded-history-ledger.tsv", list(rows[0].keys()), rows)


def write_decision_card(topology_signature: str) -> None:
    text = f"""# C01E02 A2 滚动旧会展街区用户裁决卡

> Package: `{PACKAGE_ID}`
>
> Tactical profile: `{TACTICAL_PROFILE_ID}`
>
> Topology signature: `{topology_signature}`
>
> `Candidate / runtime_allowed=false / runtime_handoff=none`

## a. 场景身份

- `MAP-A 会展中轴大道型`
- `MAP-B 馆墙防灾环廊型`
- `MAP-C 层叠旧馆雨谷型`

请选择 A/B/C，或指定不改玩法拓扑的窄修改。

## b. 战术方向读法

请确认无解释文字时是否仍能读出：

1. 北侧万机馆/居民区保护面；
2. 东侧 `rescue_lane` 、最后应急车辆和东门；
3. 馆侧退役重盾获取点；
4. 南侧 BREAKER 来向与多向 `scattered` 小体压力；
5. 三帧从西/南主战滚到东侧撤离线的连续关系。

请回复 `通过`，或指出哪一个空间锚点不清楚。

## c. 遮挡原则

- `纯淡出`
- `淡出 + 轮廓`

两案都保持屋顶/连廊分组、地图只进入 900×594 内容区，且路径/目标/意图永远在遮挡上方。

## d. 小体压力密度

- `低`：4 个布局 token
- `中`：6 个布局 token，对应当前 M2 锚点
- `高`：9 个布局 token

此项只批准布局密度，不批准小体造型、最终数值或 Sprite。

## 停止门

四项都获得用户明确回复前，不开始小体 Q/SD、正式地图、动作帧、Cut-in、视频或 Runtime handoff。
"""
    (OUT / "decision-card.md").write_text(text, encoding="utf-8")


def write_completion_report(topology_signature: str) -> None:
    text = f"""# C01E02 A2 滚动旧会展街区完成报告

## 交付边界

- 包 ID：`{PACKAGE_ID}`
- 只写入 `art-a2-rolling-district/**`。
- 全部为 `Candidate / runtime_allowed=false / runtime_handoff=none`。
- 未写 Godot，未改 Canon/剧情/玩法，未生产小体机设、正式 tile/sprite、动作帧、Cut-in、视频或 LibTV。

## 共享拓扑

- 源 profile：`{TACTICAL_PROFILE_ID}`
- 拓扑签名：`{topology_signature}`
- 棋盘：`32x18`，大于 `900x594` 战术视口。
- 三案完整复用地形区、单位锚点/footprint、非可控救援对象、可破坏物、取盾点和 `scattered` 组织态。

## 旧 B3 处置

- `18-g1-5-b3-tactical-map-art-objective.md`、旧 `12x9` profile、`BG_C01CDV1_PLAZA_TACTICAL` 和旧 B3 交付只在 `superseded-history-ledger.tsv` 登记为 `superseded_history_only`。
- 它们没有进入新判断板、没有进入 active source receipt，也没有被修改。

## 已知来源残留

- Current Canon 场景备注仍保留旧的“撤离后取盾”句子；已验收 Reader 和 revision-2 制作人合同明确实现顺序为“取盾挡下赤红冲击 -> 最后车辆通过 -> 盾拍”。
- A2 只表达空间关系，不把时序烘进地图，未修改 Canon。
- A2 开工时 `check_canon_authority.py` 通过；交付复核期间，并行 C04 写入使全局检查暂时报告 `ANT_BROKEN_CROWN` authority coverage 缺项，并在其 `authority_manifest.tsv` 差异中留下尾随空白。A2 未修改这些文件；C01 的 `ENEMY_C01_RIFT_SWARM` Working 行仍可正常查询，且明确不锁造型和棋盘数量。

## 用户停止门

等待用户分别决定：A/B/C 场景身份、战术读法、遮挡原则、小体布局密度。
"""
    (OUT / "completion-report.md").write_text(text, encoding="utf-8")


def write_manifest(topology_signature: str) -> None:
    files = sorted(
        path for path in OUT.iterdir()
        if path.is_file() and path.name not in {"asset-manifest.tsv", "delivery-hashes.sha256", "BLOCKED.md"}
        and path.name != ".DS_Store" and path.suffix != ".pyc"
    )
    rows = []
    for path in files:
        if path.suffix == ".png":
            media_type = "image/png"
        elif path.suffix == ".tsv":
            media_type = "text/tab-separated-values"
        elif path.suffix == ".md":
            media_type = "text/markdown"
        else:
            media_type = "text/x-python"
        dimensions = ""
        channels = ""
        contains_report_text = "n/a"
        if path.suffix == ".png":
            with Image.open(path) as image:
                dimensions = f"{image.width}x{image.height}"
                channels = image.mode
            lower_name = path.name.lower()
            contains_report_text = "false" if "pure_read" in lower_name or "viewport_" in lower_name else "true"
        rows.append({
            "asset_id": path.stem,
            "relative_path": path.name,
            "media_type": media_type,
            "dimensions": dimensions,
            "channels": channels,
            "package_id": PACKAGE_ID,
            "scope": "C01E02_A2_rolling_district_only",
            "source_profile": TACTICAL_PROFILE_ID,
            "topology_signature": topology_signature,
            "contains_report_text": contains_report_text,
            "uses_old_B3_asset": "false",
            "uses_final_sprite_master": "false",
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "sha256": sha256_file(path),
        })
    write_tsv(OUT / "asset-manifest.tsv", list(rows[0].keys()), rows)


def write_hashes() -> None:
    files = sorted(
        path for path in OUT.iterdir()
        if path.is_file() and path.name not in {"delivery-hashes.sha256", "BLOCKED.md"}
        and path.name != ".DS_Store" and path.suffix != ".pyc"
    )
    (OUT / "delivery-hashes.sha256").write_text(
        "\n".join(f"{sha256_file(path)}  {path.name}" for path in files) + "\n",
        encoding="utf-8",
    )


def generate_images(tactical: dict, topology_signature: str) -> None:
    full_maps: dict[str, Image.Image] = {}
    pure_maps: dict[str, Image.Image] = {}
    continuity: dict[str, Image.Image] = {}

    for candidate in CANDIDATES:
        full = render_full_domain(tactical, candidate, topology_signature, pure=False)
        pure_full = render_full_domain(tactical, candidate, topology_signature, pure=True)
        full.save(OUT / candidate_filename(candidate, "full_domain_review_2400x1350.png"), optimize=True)
        pure_full.save(OUT / candidate_filename(candidate, "pure_read_full_domain_2400x1350.png"), optimize=True)
        full_maps[candidate.code] = full
        pure_maps[candidate.code] = pure_full

        viewports: dict[str, Image.Image] = {}
        for code, _, center, _ in REVIEW_CAMERAS:
            viewport = render_viewport(tactical, candidate, center, density="MID", pure=True, occlusion_mode="fade_outline")
            viewport.save(OUT / candidate_filename(candidate, f"viewport_{code.lower()}_1280x720.png"), optimize=True)
            viewports[code] = viewport
        strip = make_continuity_strip(candidate, viewports)
        strip.save(OUT / candidate_filename(candidate, "three_viewport_continuity_3840x820.png"), optimize=True)
        continuity[candidate.code] = strip

    make_pure_read_triptych(pure_maps).save(OUT / "A2_PURE_READ_triptych_no_text_2400x900.png", optimize=True)
    make_direction_board(tactical, topology_signature, full_maps, continuity).save(
        OUT / "A2_DIRECTION_BOARD_ABC_3000x1800.png", optimize=True
    )
    make_occlusion_board(tactical, topology_signature).save(
        OUT / "A2_OCCLUSION_SAFEZONE_BOARD_2400x1350.png", optimize=True
    )
    make_density_board(tactical, topology_signature).save(
        OUT / "A2_SWARM_DENSITY_LMH_BOARD_2400x1000.png", optimize=True
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tactical, topology_signature = validate_sources()
    generate_images(tactical, topology_signature)
    write_candidate_spec(topology_signature)
    write_camera_spec(topology_signature)
    write_topology_receipt(tactical, topology_signature)
    write_density_spec(topology_signature)
    write_occlusion_spec(topology_signature)
    write_source_receipt()
    write_superseded_ledger()
    write_decision_card(topology_signature)
    write_completion_report(topology_signature)
    write_manifest(topology_signature)
    write_hashes()
    print(f"Generated {PACKAGE_ID}")
    print(f"profile={TACTICAL_PROFILE_ID}")
    print(f"topology_signature={topology_signature}")
    print("runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
