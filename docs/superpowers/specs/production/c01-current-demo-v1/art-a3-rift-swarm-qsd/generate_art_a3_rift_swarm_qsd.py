#!/usr/bin/env python3
"""Generate bounded C01E02 A3 Rift Swarm Q/SD Candidate review assets."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
SAMPLES = OUT / "samples"

PACKAGE_ID = "C01CDV1_A3_RIFT_SWARM_QSD_V1"
SUBJECT_ID = "ENEMY_C01_RIFT_SWARM"
RUNTIME_SLOT = "ENEMY_C01CDV1_RIFT_SWARM_MASTER"
PROFILE_ID = "c01cdv1_e02_scroll_m2_r2"
TOPOLOGY_SHA256 = "baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8"
MAP_CANDIDATE_ID = "CAND_C01CDV1_A2_DISTRICT_B_RESCUE_RING_V1"
MAP_CENTRAL_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_viewport_central_1280x720.png"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

PAPER = "#eef2ef"
PANEL = "#f8faf7"
INK_DEEP = "#08151b"
INK = "#182b32"
INK_SOFT = "#52656a"
BLACK_ARMOR = "#111b20"
MID_ARMOR = "#26353c"
LIGHT_ARMOR = "#405158"
FLEX_SEAM = "#52636a"
RED_SEAM = "#e4544e"
RED_DARK = "#8e3333"
TEAL = "#57aaa3"
GOLD = "#d9aa3d"
CORAL = "#e86756"
IVORY = "#dce2db"
GROUND = "#7c9295"

FACINGS = ("north", "east", "south", "west")
SAMPLE_SIZES = (96, 128)
INSTANCE_IDS = tuple(f"ENEMY_C01_RIFT_SWARM_{index:02d}" for index in range(1, 7))


STATIC_SOURCES = (
    ("docs/superpowers/specs/production/c01-current-demo-v1/19-current-demo-inplace-rebase-producer-contract.md", "6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94", "producer_contract_r2", "read_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/20-c01e02-j2-joint-integration-contract.md", "038bfb0d57aea64c1ca3a91cae7e1623a33d7c8aaeb7e7ae2af4541770ca3f0d", "j2_joint_contract", "read_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/21-c01e02-a3-rift-swarm-art-objective.md", "30dd540f56a6771a9d586d83cc3316a6f90a40b6aa29313d1222293091717f92", "a3_objective", "read_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a2/a2-user-approval-receipt.tsv", "5eae8ce88217e1ab7185ef3fbf42dd234574ab8b016c068c441f8424c41a5e76", "a2_user_approval", "read_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/candidate-spec.tsv", "43f0afcc7d576074927029592936daddd56f0491cc74f941400fe4f7d477491c", "a2_candidate_spec", "read_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_full_domain_review_2400x1350.png", "03c48e13c278cf058f223cd18590a7f9ed59e32d48676d05e33bac10ac8250b0", "map_b_full_review", "review_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_viewport_west_1280x720.png", "5dc4d77416b2e132aebc51bb078516c055119612c35d2524c47c5a879d79f519", "map_b_west", "review_only_exact"),
    (MAP_CENTRAL_PATH, "841288bf225cd4dc63d11ed20ffea5a859c9333e732eb6d5dbefa8f8c8914dc2", "map_b_central", "review_composite_base_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a2-rolling-district/A2_MAP_B_viewport_east_1280x720.png", "d396fe83b01fe06a7f89117fb6d66cf4e8fe46a2e69bd441d62ff83358e64a88", "map_b_east", "review_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv", "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920", "breaker_b1_user_approval", "derivative_relation_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png", "7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868", "breaker_b_silhouette_reference", "review_only_not_master"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png", "cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85", "breaker_x_surface_relation", "review_only_not_master"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/main-m2-1/r2-slot-registration-receipt.tsv", "d6e9bc19425a5cd7340870ba7b031aba453d14a59359749edf45fbb86bcd936a", "r2_slot_registration", "read_only_exact"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/main-m2-1/r2-instance-binding-receipt.tsv", "c494cb3359477ea327203a580c0752e653fccddecb7d51cc3abb41cf90a4bd51", "r2_instance_binding", "read_only_exact"),
)

SCOPED_CANON_SOURCES = (
    ("docs/superpowers/specs/data/canon/authority_manifest.tsv", "canon_authority", "scoped_C01_rows"),
    ("docs/superpowers/specs/data/canon/entities.tsv", "canon_entities", "scoped_ENEMY_C01_RIFT_SWARM"),
    ("docs/superpowers/specs/data/canon/scenes.tsv", "canon_scenes", "scoped_V355_C01E02"),
)


@dataclass(frozen=True)
class Candidate:
    code: str
    stable_id: str
    title: str
    silhouette: str
    center_of_mass: str
    appendages: str
    movement: str
    impact: str
    shared_ecology: str
    differentiation: str
    strength: str
    risk: str
    accent: str


CANDIDATES = (
    Candidate(
        "A",
        "CAND_C01CDV1_A3_RIFT_SWARM_A_CARAPACE_CRAWLER_V1",
        "伏壳钳足型",
        "横向低伏的三段覆甲，前端钳足明显，背线不超过一格轮廓上半部。",
        "重心贴地并略向扑击端前压。",
        "四条短承重足＋一对非武器化钳足端。",
        "对角足交替爬行；停顿时前钳探地，不同步转头。",
        "身体前送、双钳夹向目标，视觉上是近身扑击而非新技能。",
        "大块黑色生体甲、闭合红缝、少量柔性甲缝。",
        "取消 BREAKER 的高背、半直立前肢与钻地楔形，读作同生态的小型拾压体。",
        "96px 最稳，朝向、接地点和扑击端最不依赖细节。",
        "可能偏甲壳/蟹形，需要避免做成现实动物写生。",
        TEAL,
    ),
    Candidate(
        "B",
        "CAND_C01CDV1_A3_RIFT_SWARM_B_HINGED_POUNCER_V1",
        "折脊跃扑型",
        "前低后高的折脊壳体，后足形成弹簧状负形，前端只有短支撑足。",
        "重心蓄在后半身，扑击前明显下沉。",
        "两条主后足＋两条短前撑足，附肢层级最清楚。",
        "短距蓄力跃扑并立即落地；不是飞行、冲刺技能或跨格机制。",
        "肩脊先到、前撑足随后抓地，强调一拍式碰撞。",
        "覆叠黑甲、闭合红缝和有弹性的甲片接缝。",
        "不保留 BREAKER 的四肢承重比例，靠折脊与后足建立独立身份。",
        "动作性最强，idle/move/impact 三态差别最大。",
        "若腿太长会像吉祥物或小型有人机；跃起高度必须受控。",
        GOLD,
    ),
    Candidate(
        "C",
        "CAND_C01CDV1_A3_RIFT_SWARM_C_OFFSET_TRIPOD_V1",
        "偏轴三足型",
        "非对称三角壳悬在三处粗大接地点上，前端红缝偏置但仍明确。",
        "重心在三足构成的偏心支撑面内横移。",
        "一条前探足＋两条后撑足，左右甲片不完全对称。",
        "三点轮换支撑并侧向掠步；不是旋转攻击或瞬移。",
        "前探足落定后壳体侧拧，把动量压向近身目标。",
        "同源黑甲、闭合红缝、潮状非对称拼合。",
        "与 BREAKER 的人形/兽形联想都拉开，保留的是材料生态而不是身体缩放。",
        "异质感和实例差分空间最大，不容易误认成缩小 BREAKER。",
        "四朝向最容易混淆，必须依赖大红缝和前探足共同定向。",
        CORAL,
    ),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_rows(relative: str) -> list[dict[str, str]]:
    return load_tsv(ROOT / relative)


def validate_scoped_canon() -> None:
    authority = {
        (row["record_type"], row["record_id"]): row
        for row in source_rows("docs/superpowers/specs/data/canon/authority_manifest.tsv")
    }
    for key in (("entity", SUBJECT_ID), ("scene", "V355-C01E02")):
        row = authority.get(key)
        if not row or row.get("canon_level") != "working" or row.get("lifecycle_status") != "active":
            raise RuntimeError(f"A3 scoped Canon authority mismatch: {key}")

    entities = {row["entity_id"]: row for row in source_rows("docs/superpowers/specs/data/canon/entities.tsv")}
    swarm = entities.get(SUBJECT_ID, {})
    if swarm.get("status") != "working_current":
        raise RuntimeError("A3 requires Working ENEMY_C01_RIFT_SWARM")
    policy = swarm.get("implementation_policy", "")
    notes = swarm.get("notes", "")
    for token in ("E02少量", "各自扑击", "游荡", "围堵"):
        if token not in policy:
            raise RuntimeError(f"A3 swarm policy token missing: {token}")
    for token in ("不锁造型", "能力", "动机", "棋盘数量", "L6平衡"):
        if token not in notes:
            raise RuntimeError(f"A3 neutral-anchor token missing: {token}")

    scenes = {row["scene_id"]: row for row in source_rows("docs/superpowers/specs/data/canon/scenes.tsv")}
    scene = scenes.get("V355-C01E02", {})
    if SUBJECT_ID not in scene.get("required_entities", "").split(";"):
        raise RuntimeError("A3 subject missing from V355-C01E02")
    scene_notes = scene.get("notes", "")
    for token in ("少量同类弱小体", "各自扑击", "不配合Boss", "至少一组可见幸存小体"):
        if token not in scene_notes:
            raise RuntimeError(f"A3 scene token missing: {token}")


def validate_sources() -> list[dict[str, str]]:
    for relative, expected, _, _ in STATIC_SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"A3 source missing: {relative}")
        actual = sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"A3 source hash drift: {relative}: {actual}")

    contract = (ROOT / STATIC_SOURCES[0][0]).read_text(encoding="utf-8")
    for token in ("E02 小体组织态固定为 `scattered`", "具体 footprint 和小体数量仍为 Demo 平衡参数", "小体 Q/SD 身份和动作方向"):
        if token not in contract:
            raise RuntimeError(f"A3 contract token missing: {token}")

    objective = (ROOT / STATIC_SOURCES[2][0]).read_text(encoding="utf-8")
    for token in ("2–3 个可明确区分的 Q/SD 身份方向", "一个 1×1 母版身份", "bottom_center", "不得制作最终 atlas"):
        if token not in objective:
            raise RuntimeError(f"A3 objective token missing: {token}")

    a2_receipt = source_rows(STATIC_SOURCES[3][0])
    if len(a2_receipt) != 1:
        raise RuntimeError("A3 requires one A2 approval receipt")
    a2 = a2_receipt[0]
    expected_a2 = {
        "selected_candidate_id": MAP_CANDIDATE_ID,
        "tactical_readability": "passed",
        "occlusion_selection": "fade_plus_outline",
        "swarm_density": "MID",
        "swarm_anchor_count": "6",
        "swarm_organization_state": "scattered",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
        "next_gate": "A3_rift_swarm_qsd_direction_unlocked",
    }
    for key, value in expected_a2.items():
        if a2.get(key) != value:
            raise RuntimeError(f"A3 A2 receipt mismatch: {key}={a2.get(key)}")

    map_rows = source_rows(STATIC_SOURCES[4][0])
    selected_map = next((row for row in map_rows if row.get("candidate_id") == MAP_CANDIDATE_ID), None)
    if not selected_map or selected_map.get("grid") != "32x18" or selected_map.get("topology_signature") != TOPOLOGY_SHA256:
        raise RuntimeError("A3 selected MAP-B source mismatch")
    if selected_map.get("runtime_allowed") != "false" or selected_map.get("runtime_handoff") != "none":
        raise RuntimeError("A3 cannot consume MAP-B as Runtime")

    breaker_rows = source_rows(STATIC_SOURCES[9][0])
    breaker = breaker_rows[0]
    if breaker.get("silhouette_selection") != "B_FORELIMB_BEARER" or breaker.get("surface_selection") != "X_ALIEN_BIO_ARMOR":
        raise RuntimeError("A3 BREAKER B+X relation mismatch")
    if breaker.get("runtime_allowed") != "false" or breaker.get("runtime_handoff") != "none":
        raise RuntimeError("A3 cannot consume BREAKER as Runtime")

    slots = source_rows(STATIC_SOURCES[12][0])
    slot = next((row for row in slots if row.get("slot_id") == RUNTIME_SLOT), None)
    if not slot or slot.get("accepted_binding_kind") != "sprite_sheet" or slot.get("constraint_profile") != "qsd_1x1":
        raise RuntimeError("A3 R2 master slot mismatch")
    if slot.get("runtime_allowed") != "false" or slot.get("approved_asset_binding"):
        raise RuntimeError("A3 R2 slot already has unauthorized handoff")

    bindings = source_rows(STATIC_SOURCES[13][0])
    swarm_bindings = [row for row in bindings if row.get("master_slot_id") == RUNTIME_SLOT]
    if [row["instance_stable_id"] for row in swarm_bindings] != list(INSTANCE_IDS):
        raise RuntimeError("A3 six-instance identity drift")
    if any(row.get("footprint") != "1,1" or row.get("role") != "scattered_swarm" or row.get("runtime_allowed") != "false" for row in swarm_bindings):
        raise RuntimeError("A3 instance footprint/role/runtime drift")

    validate_scoped_canon()
    return swarm_bindings


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, width: int, used_font: ImageFont.FreeTypeFont) -> list[str]:
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


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, width: int, size: int, fill: str, *, bold: bool = False, spacing: int = 5) -> int:
    used_font = font(size, bold=bold)
    y = xy[1]
    for paragraph in text.split("\n"):
        for line in wrap_lines(draw, paragraph, width, used_font):
            draw.text((xy[0], y), line, font=used_font, fill=fill)
            y += size + spacing
        y += spacing
    return y


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4)) + (alpha,)


def candidate_by_code(code: str) -> Candidate:
    return next(candidate for candidate in CANDIDATES if candidate.code == code)


def polygon(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: tuple[int, int, int, int], outline: tuple[int, int, int, int], width: int) -> None:
    draw.polygon(points, fill=fill)
    draw.line(points + [points[0]], fill=outline, width=width, joint="curve")


def line_body(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], width: float, fill: tuple[int, int, int, int], outline: tuple[int, int, int, int], outline_width: int) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 1.0)
    nx = -dy / length * width / 2
    ny = dx / length * width / 2
    points = [
        (start[0] + nx, start[1] + ny),
        (end[0] + nx, end[1] + ny),
        (end[0] - nx, end[1] - ny),
        (start[0] - nx, start[1] - ny),
    ]
    polygon(draw, points, fill, outline, outline_width)


def facing_axes(facing: str) -> tuple[tuple[float, float], tuple[float, float]]:
    axes = {
        "north": ((1.0, -0.5), (1.0, 0.5)),
        "east": ((1.0, 0.5), (-1.0, 0.5)),
        "south": ((-1.0, 0.5), (-1.0, -0.5)),
        "west": ((-1.0, -0.5), (1.0, -0.5)),
    }
    return axes[facing]


def render_sprite(candidate: Candidate, facing: str, size: int, *, state: str = "idle", variation: int = 0, silhouette: bool = False) -> Image.Image:
    supersample = 4
    width = height = size * supersample
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    heading, side = facing_axes(facing)
    unit = size * supersample * 0.31
    origin = (size * supersample * 0.5, size * supersample * 0.88)
    z_scale = size * supersample * 0.35
    state_lift = 0.0
    state_forward = 0.0
    if state == "move":
        state_lift = 0.03 if candidate.code != "B" else 0.09
        state_forward = 0.05
    elif state == "impact":
        state_lift = -0.02
        state_forward = 0.13

    def point(forward: float, lateral: float, z: float) -> tuple[float, float]:
        f = forward + state_forward
        return (
            origin[0] + (f * heading[0] + lateral * side[0]) * unit,
            origin[1] + (f * heading[1] + lateral * side[1]) * unit - (z + state_lift) * z_scale,
        )

    outline = rgba("#061015")
    armor = rgba(BLACK_ARMOR)
    mid = rgba(MID_ARMOR)
    light = rgba(LIGHT_ARMOR)
    flex = rgba(FLEX_SEAM)
    seam = rgba(RED_SEAM)
    edge = rgba(IVORY)
    if silhouette:
        armor = mid = light = flex = seam = edge = rgba("#05090b")
    else:
        if variation == 1:
            light = rgba("#4a3a3b")
        elif variation == 2:
            light = rgba("#36504e")
        elif variation == 3:
            flex = rgba("#75633e")
        elif variation == 4:
            mid = rgba("#2f3d43")
        elif variation == 5:
            seam = rgba("#c94b47")

    stroke = max(5, round(size * supersample * 0.025))
    shadow_box = (
        origin[0] - size * supersample * 0.23,
        origin[1] - size * supersample * 0.055,
        origin[0] + size * supersample * 0.23,
        origin[1] + size * supersample * 0.055,
    )
    if not silhouette:
        draw.ellipse(shadow_box, fill=(2, 9, 12, 70))

    if candidate.code == "A":
        leg_specs = [(-0.34, -0.34, -0.42, -0.53), (-0.34, 0.34, -0.42, 0.53), (0.28, -0.34, 0.28, -0.56), (0.28, 0.34, 0.28, 0.56)]
        if state == "move":
            leg_specs = [(-0.34, -0.34, -0.53, -0.56), (-0.34, 0.34, -0.25, 0.46), (0.28, -0.34, 0.43, -0.50), (0.28, 0.34, 0.14, 0.58)]
        if variation == 4:
            leg_specs[-1] = (0.28, 0.34, 0.20, 0.49)
        for af, al, ff, fl in sorted(leg_specs, key=lambda spec: point(spec[2], spec[3], 0)[1]):
            line_body(draw, point(af, al, 0.36), point(ff, fl, 0.03), size * supersample * 0.12, flex, outline, stroke)
        for lateral in (-0.29, 0.29):
            claw_end = 0.83 if state == "impact" else 0.68
            line_body(draw, point(0.43, lateral, 0.26), point(claw_end, lateral * 1.08, 0.10), size * supersample * 0.10, mid, outline, stroke)
        base_points = [point(-0.63, -0.34, 0.36), point(0.38, -0.39, 0.39), point(0.66, -0.19, 0.40), point(0.66, 0.19, 0.40), point(0.38, 0.39, 0.39), point(-0.63, 0.34, 0.36), point(-0.72, 0, 0.34)]
        polygon(draw, base_points, armor, outline, stroke)
        rear_plate = [point(-0.65, -0.31, 0.43), point(-0.22, -0.38, 0.55), point(-0.18, 0.38, 0.55), point(-0.65, 0.31, 0.43)]
        mid_plate = [point(-0.20, -0.37, 0.56), point(0.25, -0.34, 0.63), point(0.28, 0.34, 0.63), point(-0.20, 0.37, 0.56)]
        prow_plate = [point(0.27, -0.32, 0.62), point(0.66, -0.17, 0.55), point(0.66, 0.17, 0.55), point(0.27, 0.32, 0.62)]
        polygon(draw, rear_plate, mid, outline, stroke)
        polygon(draw, mid_plate, light, outline, stroke)
        polygon(draw, prow_plate, mid, outline, stroke)
        draw.line((point(0.59, -0.16, 0.59), point(0.59, 0.16, 0.59)), fill=seam, width=stroke + 3)
    elif candidate.code == "B":
        rear_specs = [(-0.34, -0.25, -0.52, -0.42), (-0.34, 0.25, -0.52, 0.42)]
        front_specs = [(0.37, -0.25, 0.50, -0.34), (0.37, 0.25, 0.50, 0.34)]
        if state == "move":
            rear_specs = [(-0.34, -0.25, -0.72, -0.38), (-0.34, 0.25, -0.45, 0.50)]
            front_specs = [(0.37, -0.25, 0.62, -0.27), (0.37, 0.25, 0.41, 0.36)]
        for af, al, ff, fl in sorted(rear_specs + front_specs, key=lambda spec: point(spec[2], spec[3], 0)[1]):
            leg_width = 0.15 if (af < 0) else 0.08
            line_body(draw, point(af, al, 0.45), point(ff, fl, 0.03), size * supersample * leg_width, flex if af < 0 else mid, outline, stroke)
        base = [point(-0.56, -0.31, 0.46), point(-0.20, -0.36, 0.68), point(0.37, -0.31, 0.62), point(0.61, -0.13, 0.47), point(0.61, 0.13, 0.47), point(0.37, 0.31, 0.62), point(-0.20, 0.36, 0.68), point(-0.56, 0.31, 0.46)]
        polygon(draw, base, armor, outline, stroke)
        rear_plate = [point(-0.53, -0.29, 0.49), point(-0.18, -0.33, 0.72), point(-0.15, 0.33, 0.72), point(-0.53, 0.29, 0.49)]
        front_plate = [point(-0.14, -0.32, 0.70), point(0.41, -0.28, 0.64), point(0.60, -0.11, 0.50), point(0.60, 0.11, 0.50), point(0.41, 0.28, 0.64), point(-0.14, 0.32, 0.70)]
        polygon(draw, rear_plate, light, outline, stroke)
        polygon(draw, front_plate, mid, outline, stroke)
        draw.line((point(0.52, -0.14, 0.57), point(0.52, 0.14, 0.57)), fill=seam, width=stroke + 3)
    else:
        leg_specs = [(0.30, 0.00, 0.60, 0.00), (-0.31, -0.27, -0.50, -0.47), (-0.31, 0.27, -0.50, 0.47)]
        if state == "move":
            leg_specs = [(0.30, 0.00, 0.68, -0.06), (-0.31, -0.27, -0.36, -0.52), (-0.31, 0.27, -0.63, 0.39)]
        if variation == 4:
            leg_specs[2] = (-0.31, 0.27, -0.44, 0.39)
        for af, al, ff, fl in sorted(leg_specs, key=lambda spec: point(spec[2], spec[3], 0)[1]):
            line_body(draw, point(af, al, 0.38), point(ff, fl, 0.03), size * supersample * 0.14, flex, outline, stroke)
        body = [point(-0.52, -0.34, 0.39), point(0.13, -0.42, 0.58), point(0.58, -0.14, 0.55), point(0.62, 0.13, 0.49), point(0.06, 0.35, 0.62), point(-0.58, 0.24, 0.43)]
        polygon(draw, body, armor, outline, stroke)
        left_plate = [point(-0.50, -0.30, 0.45), point(0.10, -0.38, 0.64), point(0.05, 0.00, 0.67), point(-0.54, 0.17, 0.48)]
        right_plate = [point(0.07, -0.01, 0.66), point(0.55, -0.12, 0.59), point(0.58, 0.12, 0.53), point(0.07, 0.31, 0.65)]
        polygon(draw, left_plate, light, outline, stroke)
        polygon(draw, right_plate, mid, outline, stroke)
        draw.line((point(0.48, -0.13, 0.60), point(0.50, 0.12, 0.58)), fill=seam, width=stroke + 3)

    if not silhouette and variation == 3:
        draw.line((point(-0.25, -0.20, 0.68), point(0.04, -0.18, 0.68)), fill=rgba("#b69d61"), width=max(2, stroke - 1))
    if not silhouette and variation == 5:
        draw.line((point(-0.42, 0.23, 0.56), point(-0.12, 0.26, 0.62)), fill=edge, width=max(2, stroke - 2))

    image = image.resize((size, size), Image.Resampling.LANCZOS)
    return image


def render_strict_side(candidate: Candidate, size: int, *, silhouette: bool = False) -> Image.Image:
    supersample = 4
    canvas = Image.new("RGBA", (size * supersample, size * supersample), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")
    k = size * supersample
    def p(x: float, y: float) -> tuple[float, float]:
        return (x * k, y * k)
    outline = rgba("#061015")
    armor = rgba(BLACK_ARMOR)
    mid = rgba(MID_ARMOR)
    light = rgba(LIGHT_ARMOR)
    flex = rgba(FLEX_SEAM)
    seam = rgba(RED_SEAM)
    if silhouette:
        armor = mid = light = flex = seam = rgba("#05090b")
    stroke = max(5, round(k * 0.018))
    if candidate.code == "A":
        for x in (0.29, 0.43, 0.62, 0.75):
            polygon(draw, [p(x - 0.045, 0.53), p(x + 0.045, 0.53), p(x + 0.06, 0.78), p(x - 0.05, 0.78)], flex, outline, stroke)
        polygon(draw, [p(0.14, 0.43), p(0.24, 0.27), p(0.62, 0.25), p(0.84, 0.38), p(0.78, 0.57), p(0.22, 0.57)], armor, outline, stroke)
        polygon(draw, [p(0.18, 0.41), p(0.30, 0.29), p(0.47, 0.28), p(0.43, 0.54), p(0.22, 0.54)], mid, outline, stroke)
        polygon(draw, [p(0.45, 0.28), p(0.64, 0.28), p(0.81, 0.39), p(0.75, 0.53), p(0.43, 0.54)], light, outline, stroke)
        draw.line((p(0.72, 0.39), p(0.80, 0.41)), fill=seam, width=stroke + 4)
        polygon(draw, [p(0.79, 0.52), p(0.92, 0.58), p(0.81, 0.63)], mid, outline, stroke)
    elif candidate.code == "B":
        polygon(draw, [p(0.22, 0.50), p(0.35, 0.50), p(0.28, 0.80), p(0.16, 0.80)], flex, outline, stroke)
        polygon(draw, [p(0.60, 0.52), p(0.67, 0.52), p(0.72, 0.77), p(0.64, 0.77)], mid, outline, stroke)
        polygon(draw, [p(0.16, 0.43), p(0.29, 0.20), p(0.60, 0.23), p(0.82, 0.39), p(0.72, 0.56), p(0.29, 0.54)], armor, outline, stroke)
        polygon(draw, [p(0.18, 0.41), p(0.30, 0.22), p(0.46, 0.24), p(0.43, 0.51), p(0.29, 0.52)], light, outline, stroke)
        polygon(draw, [p(0.44, 0.25), p(0.60, 0.26), p(0.79, 0.40), p(0.70, 0.53), p(0.43, 0.51)], mid, outline, stroke)
        draw.line((p(0.70, 0.39), p(0.79, 0.41)), fill=seam, width=stroke + 4)
    else:
        for points in (
            [p(0.26, 0.52), p(0.35, 0.52), p(0.24, 0.80), p(0.13, 0.78)],
            [p(0.47, 0.53), p(0.56, 0.53), p(0.52, 0.79), p(0.42, 0.79)],
            [p(0.69, 0.50), p(0.77, 0.50), p(0.84, 0.73), p(0.75, 0.76)],
        ):
            polygon(draw, points, flex, outline, stroke)
        polygon(draw, [p(0.15, 0.44), p(0.32, 0.24), p(0.66, 0.27), p(0.84, 0.41), p(0.68, 0.57), p(0.25, 0.55)], armor, outline, stroke)
        polygon(draw, [p(0.18, 0.42), p(0.33, 0.27), p(0.51, 0.28), p(0.46, 0.54), p(0.25, 0.53)], light, outline, stroke)
        polygon(draw, [p(0.51, 0.29), p(0.65, 0.30), p(0.80, 0.41), p(0.66, 0.54), p(0.47, 0.54)], mid, outline, stroke)
        draw.line((p(0.70, 0.39), p(0.79, 0.42)), fill=seam, width=stroke + 4)
    return canvas.resize((size, size), Image.Resampling.LANCZOS)


def fit_rgba(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(copy, ((size[0] - copy.width) // 2, (size[1] - copy.height) // 2))
    return canvas


def checkerboard(size: tuple[int, int], step: int = 18) -> Image.Image:
    image = Image.new("RGB", size, "#e6ebe7")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill="#d4dcd7")
    return image


def faded_with_outline(sprite: Image.Image, alpha: int = 46) -> Image.Image:
    source = sprite.convert("RGBA")
    source_alpha = source.getchannel("A")
    faded = source.copy()
    faded.putalpha(source_alpha.point(lambda value: round(value * alpha / 255)))
    expanded = source_alpha.filter(ImageFilter.MaxFilter(7))
    outline_mask = ImageChops.subtract(expanded, source_alpha)
    outline = Image.new("RGBA", source.size, rgba(IVORY, 0))
    outline.putalpha(outline_mask)
    return Image.alpha_composite(faded, outline)


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], *, fill: str = PANEL, outline: str = "#aebbb9", width: int = 2) -> None:
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def paste_center(base: Image.Image, sprite: Image.Image, center: tuple[int, int]) -> None:
    rgba_base = base if base.mode == "RGBA" else base.convert("RGBA")
    rgba_base.alpha_composite(sprite, (center[0] - sprite.width // 2, center[1] - sprite.height // 2))
    if base.mode != "RGBA":
        base.paste(rgba_base.convert(base.mode))


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, *, size: int = 28, fill: str = INK, bold: bool = False) -> None:
    draw.text(xy, text, font=font(size, bold=bold), fill=fill)


def identity_sheet(candidate: Candidate) -> Image.Image:
    image = Image.new("RGB", (1800, 1200), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1800, 112), fill=INK_DEEP)
    draw.rectangle((0, 112, 18, 1200), fill=candidate.accent)
    label(draw, (52, 27), f"A3-{candidate.code}  {candidate.title}", size=44, fill=PAPER, bold=True)
    label(draw, (1320, 40), "Q/SD 身份方向 / CANDIDATE", size=24, fill="#bac8c7")

    visual_boxes = ((55, 148, 555, 650), (575, 148, 1075, 650), (1095, 148, 1745, 650))
    visual_titles = ("黑白主轮廓", "严格侧面", "朝北三分之四身份")
    for box, title in zip(visual_boxes, visual_titles):
        panel(draw, box)
        label(draw, (box[0] + 20, box[1] + 16), title, size=25, bold=True)

    silhouette = render_sprite(candidate, "north", 410, silhouette=True)
    side = render_strict_side(candidate, 410)
    three_quarter = render_sprite(candidate, "north", 430)
    image.paste(silhouette, (100, 205), silhouette)
    image.paste(side, (620, 205), side)
    image.paste(three_quarter, (1205, 205), three_quarter)

    panel(draw, (55, 680, 725, 1138))
    label(draw, (80, 705), "原生尺寸可读性", size=28, bold=True)
    for x, sample_size in ((110, 96), (390, 128)):
        board = checkerboard((230, 230), 16)
        sample = render_sprite(candidate, "east", sample_size)
        scaled = sample.resize((sample_size * 2, sample_size * 2), Image.Resampling.NEAREST)
        board_rgba = board.convert("RGBA")
        board_rgba.alpha_composite(scaled, ((230 - scaled.width) // 2, (230 - scaled.height) // 2))
        image.paste(board_rgba.convert("RGB"), (x, 765))
        label(draw, (x + 70, 1006), f"{sample_size}px", size=25, bold=True)
    draw.line((80, 1058, 700, 1058), fill="#b5c0bd", width=2)
    label(draw, (80, 1075), "透明 RGBA｜bottom_center｜1×1", size=23, fill=INK_SOFT)

    panel(draw, (755, 680, 1245, 1138))
    label(draw, (780, 705), "主体与动作语法", size=28, bold=True)
    y = 758
    for heading, value in (
        ("轮廓", candidate.silhouette),
        ("重心", candidate.center_of_mass),
        ("附肢", candidate.appendages),
        ("移动", candidate.movement),
        ("碰撞", candidate.impact),
    ):
        label(draw, (780, y), heading, size=22, fill=candidate.accent, bold=True)
        y = draw_wrapped(draw, (852, y), value, 355, 21, INK, spacing=3) + 5

    panel(draw, (1275, 680, 1745, 1138))
    label(draw, (1300, 705), "与 BREAKER B＋X", size=28, bold=True)
    label(draw, (1300, 754), "保留同源", size=22, fill=candidate.accent, bold=True)
    y = draw_wrapped(draw, (1300, 788), candidate.shared_ecology, 415, 22, INK, spacing=4)
    label(draw, (1300, y + 6), "主动拉开", size=22, fill=candidate.accent, bold=True)
    y = draw_wrapped(draw, (1300, y + 40), candidate.differentiation, 415, 22, INK, spacing=4)
    label(draw, (1300, y + 12), "优势", size=22, fill="#28736b", bold=True)
    y = draw_wrapped(draw, (1300, y + 45), candidate.strength, 415, 21, INK, spacing=3)
    label(draw, (1300, y + 8), "风险", size=22, fill=RED_DARK, bold=True)
    draw_wrapped(draw, (1300, y + 41), candidate.risk, 415, 21, INK, spacing=3)
    return image


def direction_board() -> Image.Image:
    image = Image.new("RGB", (3000, 1800), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 3000, 150), fill=INK_DEEP)
    label(draw, (70, 34), "C01E02 A3｜裂隙小体 Q/SD 三方向", size=58, fill=PAPER, bold=True)
    label(draw, (70, 104), "一个 1×1 母版身份；六实例仅轻差分｜不锁物种、能力、动机或最终数量", size=26, fill="#b8c8c6")
    column_width = 920
    for index, candidate in enumerate(CANDIDATES):
        left = 70 + index * 965
        panel(draw, (left, 195, left + column_width, 1715), fill="#f7f9f6", outline=candidate.accent, width=4)
        draw.rectangle((left, 195, left + column_width, 285), fill=candidate.accent)
        label(draw, (left + 30, 214), f"{candidate.code}｜{candidate.title}", size=39, fill=INK_DEEP, bold=True)

        hero = render_sprite(candidate, "north", 610)
        image.paste(hero, (left + 155, 300), hero)
        label(draw, (left + 30, 870), "核心读法", size=27, fill=candidate.accent, bold=True)
        y = draw_wrapped(draw, (left + 30, 914), candidate.silhouette, column_width - 60, 25, INK, spacing=5)
        for heading, value in (
            ("移动语法", candidate.movement),
            ("B＋X 关系", candidate.differentiation),
            ("通过点", candidate.strength),
            ("风险", candidate.risk),
        ):
            label(draw, (left + 30, y + 12), heading, size=24, fill=candidate.accent if heading != "风险" else RED_DARK, bold=True)
            y = draw_wrapped(draw, (left + 30, y + 47), value, column_width - 60, 23, INK, spacing=4)
        label(draw, (left + 30, 1618), candidate.stable_id, size=18, fill=INK_SOFT)
        label(draw, (left + 30, 1654), "Candidate｜runtime_allowed=false｜handoff=none", size=18, fill=INK_SOFT)
    return image


def four_direction_action_board() -> Image.Image:
    image = Image.new("RGB", (3000, 1800), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 3000, 138), fill=INK_DEEP)
    label(draw, (65, 32), "四朝向与动作空间验证", size=54, fill=PAPER, bold=True)
    label(draw, (1940, 53), "关键姿态，不是最终逐帧动画", size=25, fill="#b8c8c6")
    column_x = (430, 750, 1070, 1390, 1830, 2190, 2550)
    column_titles = ("NORTH", "EAST", "SOUTH", "WEST", "IDLE", "MOVE", "IMPACT")
    for x, title in zip(column_x, column_titles):
        label(draw, (x - 70, 164), title, size=24, fill=INK_SOFT, bold=True)
    for row, candidate in enumerate(CANDIDATES):
        top = 228 + row * 510
        panel(draw, (55, top, 2945, top + 460), fill="#f7f9f6", outline="#b4c1be")
        draw.rectangle((55, top, 300, top + 460), fill=candidate.accent)
        label(draw, (88, top + 50), candidate.code, size=82, fill=INK_DEEP, bold=True)
        draw_wrapped(draw, (88, top + 152), candidate.title, 180, 27, INK_DEEP, bold=True)
        for x, facing in zip(column_x[:4], FACINGS):
            sprite = render_sprite(candidate, facing, 250)
            image.paste(sprite, (x - 125, top + 65), sprite)
        for x, state in zip(column_x[4:], ("idle", "move", "impact")):
            sprite = render_sprite(candidate, "east", 280, state=state)
            image.paste(sprite, (x - 140, top + 48), sprite)
        label(draw, (335, top + 390), f"移动：{candidate.movement}", size=21, fill=INK_SOFT)
        label(draw, (1650, top + 390), f"碰撞：{candidate.impact}", size=21, fill=INK_SOFT)
    return image


CENTRAL_PLACEMENTS = {
    "ENEMY_C01_RIFT_SWARM_01": (490, 251),
    "ENEMY_C01_RIFT_SWARM_02": (730, 331),
    "ENEMY_C01_RIFT_SWARM_04": (330, 411),
    "ENEMY_C01_RIFT_SWARM_06": (490, 571),
}


def map_composite(candidate: Candidate, bindings: list[dict[str, str]]) -> Image.Image:
    base = Image.open(ROOT / MAP_CENTRAL_PATH).convert("RGBA")
    by_id = {row["instance_stable_id"]: row for row in bindings}
    for variation, (instance_id, position) in enumerate(CENTRAL_PLACEMENTS.items()):
        facing = by_id[instance_id]["facing"]
        sprite = render_sprite(candidate, facing, 96, variation=variation)
        base.alpha_composite(sprite, (position[0] - 48, position[1] - 96))
    return base.convert("RGB")


def map_comparison_board(composites: dict[str, Image.Image]) -> Image.Image:
    image = Image.new("RGB", (3000, 1200), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 3000, 132), fill=INK_DEEP)
    label(draw, (65, 31), "MAP-B 中央视口｜四个既定可见锚点", size=50, fill=PAPER, bold=True)
    label(draw, (1910, 49), "叠图评审，不烘入地图，不交 Runtime", size=24, fill="#b8c8c6")
    for index, candidate in enumerate(CANDIDATES):
        left = 55 + index * 980
        panel(draw, (left, 175, left + 930, 1125), fill="#f7f9f6", outline=candidate.accent, width=3)
        label(draw, (left + 24, 198), f"{candidate.code}｜{candidate.title}", size=31, fill=INK, bold=True)
        resized = composites[candidate.code].resize((900, 506), Image.Resampling.LANCZOS)
        image.paste(resized, (left + 15, 255))
        label(draw, (left + 24, 790), "CENTRAL 可见 4/6；另外 2 只仍在 EAST 既定锚点。", size=22, fill=INK)
        label(draw, (left + 24, 833), "散乱态：各自朝向，不排队、不围 Boss、不形成箭头。", size=22, fill=INK)
        draw_wrapped(draw, (left + 24, 888), candidate.strength, 870, 22, INK_SOFT, spacing=4)
    return image


def footprint_occlusion_board() -> Image.Image:
    image = Image.new("RGB", (2400, 1350), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 2400, 128), fill=INK_DEEP)
    label(draw, (60, 28), "1×1 FOOTPRINT｜PIVOT｜淡出＋轮廓", size=49, fill=PAPER, bold=True)
    for index, candidate in enumerate(CANDIDATES):
        left = 50 + index * 790
        panel(draw, (left, 170, left + 740, 1270), fill="#f7f9f6", outline=candidate.accent, width=3)
        label(draw, (left + 28, 195), f"{candidate.code}｜{candidate.title}", size=31, bold=True)

        center = (left + 370, 495)
        diamond = [(center[0], center[1] - 130), (center[0] + 230, center[1]), (center[0], center[1] + 130), (center[0] - 230, center[1])]
        draw.polygon(diamond, fill="#c9d4d0", outline=INK_SOFT)
        draw.line(diamond + [diamond[0]], fill=INK_SOFT, width=4)
        sprite = render_sprite(candidate, "south", 280)
        pivot = (center[0], center[1] + 130)
        image.paste(sprite, (pivot[0] - 140, pivot[1] - 280), sprite)
        draw.ellipse((pivot[0] - 8, pivot[1] - 8, pivot[0] + 8, pivot[1] + 8), fill=RED_SEAM)
        draw.line((pivot[0] - 30, pivot[1], pivot[0] + 30, pivot[1]), fill=RED_SEAM, width=3)
        label(draw, (left + 45, 665), "bottom_center pivot", size=22, fill=RED_DARK, bold=True)
        label(draw, (left + 425, 665), "1×1 / 不越格", size=22, fill=INK_SOFT)

        label(draw, (left + 45, 735), "接地点", size=25, fill=candidate.accent, bold=True)
        contact_count = {"A": 4, "B": 4, "C": 3}[candidate.code]
        for dot in range(contact_count):
            x = left + 150 + dot * 105
            draw.ellipse((x - 12, 790, x + 12, 814), fill=candidate.accent)
        label(draw, (left + 45, 835), f"{contact_count} 处主接点在 96px 下仍可分辨", size=21, fill=INK)

        label(draw, (left + 45, 895), "建筑遮挡态", size=25, fill=candidate.accent, bold=True)
        check = Image.new("RGBA", (280, 220), rgba("#1b2c32"))
        check_draw = ImageDraw.Draw(check)
        check_draw.polygon(((0, 0), (280, 0), (280, 82), (94, 220), (0, 220)), fill="#2c4147")
        check_draw.line(((0, 72), (280, 72)), fill="#52676b", width=3)
        occluded = faded_with_outline(render_sprite(candidate, "east", 170))
        check.alpha_composite(occluded, (55, 20))
        image.paste(check.convert("RGB"), (left + 45, 940))
        label(draw, (left + 350, 955), "18% 本体", size=21, fill=INK)
        label(draw, (left + 350, 997), "象牙色外轮廓", size=21, fill=INK)
        label(draw, (left + 350, 1039), "不靠血条或特效", size=21, fill=INK)
        label(draw, (left + 350, 1081), "前端红缝仍定向", size=21, fill=INK)
    return image


VARIATION_LABELS = (
    "基准母版",
    "旧红褐色斑",
    "冷绿灰色斑",
    "单处黄褐擦痕",
    "一处末端缺口",
    "红缝亮度差",
)


def variation_board() -> Image.Image:
    image = Image.new("RGB", (2400, 1200), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 2400, 130), fill=INK_DEEP)
    label(draw, (60, 29), "一个母版＋六实例轻差分", size=50, fill=PAPER, bold=True)
    label(draw, (1460, 51), "身份、比例、动作和碰撞体完全共享", size=23, fill="#b8c8c6")
    for row, candidate in enumerate(CANDIDATES):
        top = 175 + row * 325
        panel(draw, (50, top, 2350, top + 285), fill="#f7f9f6", outline=candidate.accent, width=3)
        draw.rectangle((50, top, 265, top + 285), fill=candidate.accent)
        label(draw, (82, top + 60), candidate.code, size=74, fill=INK_DEEP, bold=True)
        draw_wrapped(draw, (82, top + 150), candidate.title, 150, 23, INK_DEEP, bold=True)
        for variation in range(6):
            x = 290 + variation * 340
            sprite = render_sprite(candidate, "east", 205, variation=variation)
            image.paste(sprite, (x, top + 15), sprite)
            label(draw, (x + 22, top + 218), f"{variation + 1:02d}  {VARIATION_LABELS[variation]}", size=18, fill=INK_SOFT)
    label(draw, (60, 1160), "禁止差分：新附肢、新能力、新轮廓、新尺寸、新动画语法。", size=22, fill=RED_DARK, bold=True)
    return image


def write_tsv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_candidate_spec() -> None:
    fieldnames = (
        "package_id", "subject_id", "candidate_code", "candidate_id", "title", "silhouette", "center_of_mass",
        "appendages", "movement_grammar", "impact_grammar", "breaker_shared_ecology", "breaker_differentiation",
        "strength", "risk", "footprint", "pivot", "facings", "native_sizes", "instance_rule", "lifecycle",
        "runtime_allowed", "runtime_handoff", "user_decision_required",
    )
    rows = []
    for candidate in CANDIDATES:
        rows.append({
            "package_id": PACKAGE_ID,
            "subject_id": SUBJECT_ID,
            "candidate_code": candidate.code,
            "candidate_id": candidate.stable_id,
            "title": candidate.title,
            "silhouette": candidate.silhouette,
            "center_of_mass": candidate.center_of_mass,
            "appendages": candidate.appendages,
            "movement_grammar": candidate.movement,
            "impact_grammar": candidate.impact,
            "breaker_shared_ecology": candidate.shared_ecology,
            "breaker_differentiation": candidate.differentiation,
            "strength": candidate.strength,
            "risk": candidate.risk,
            "footprint": "1,1",
            "pivot": "bottom_center",
            "facings": ";".join(FACINGS),
            "native_sizes": "96;128",
            "instance_rule": "one_master_plus_six_light_variants",
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "user_decision_required": "true",
        })
    write_tsv(OUT / "candidate-spec.tsv", fieldnames, rows)


def write_sample_index() -> None:
    fieldnames = (
        "asset_id", "candidate_id", "facing", "native_size", "path", "channels", "pivot", "footprint",
        "alpha_nonempty", "final_atlas", "lifecycle", "runtime_allowed", "runtime_handoff",
    )
    rows = []
    for candidate in CANDIDATES:
        for facing in FACINGS:
            for native_size in SAMPLE_SIZES:
                filename = f"A3_{candidate.code}_{facing}_{native_size}_review.png"
                rows.append({
                    "asset_id": f"{candidate.stable_id}_{facing.upper()}_{native_size}_REVIEW",
                    "candidate_id": candidate.stable_id,
                    "facing": facing,
                    "native_size": f"{native_size}x{native_size}",
                    "path": f"samples/{filename}",
                    "channels": "RGBA",
                    "pivot": "bottom_center",
                    "footprint": "1,1",
                    "alpha_nonempty": "true",
                    "final_atlas": "false",
                    "lifecycle": "Candidate",
                    "runtime_allowed": "false",
                    "runtime_handoff": "none",
                })
    write_tsv(OUT / "transparent-sample-index.tsv", fieldnames, rows)


def write_instance_variation_spec() -> None:
    fieldnames = (
        "candidate_id", "instance_stable_id", "variation_index", "variation_label", "identity_shared",
        "proportion_shared", "action_grammar_shared", "collision_shared", "independent_design", "lifecycle",
        "runtime_allowed", "runtime_handoff",
    )
    rows = []
    for candidate in CANDIDATES:
        for index, instance_id in enumerate(INSTANCE_IDS):
            rows.append({
                "candidate_id": candidate.stable_id,
                "instance_stable_id": instance_id,
                "variation_index": index,
                "variation_label": VARIATION_LABELS[index],
                "identity_shared": "true",
                "proportion_shared": "true",
                "action_grammar_shared": "true",
                "collision_shared": "true",
                "independent_design": "false",
                "lifecycle": "Candidate",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
            })
    write_tsv(OUT / "instance-light-variation-spec.tsv", fieldnames, rows)


def write_map_placement(bindings: list[dict[str, str]]) -> None:
    fieldnames = (
        "candidate_id", "instance_stable_id", "profile_id", "topology_sha256", "anchor", "footprint", "facing",
        "organization_state", "central_visible", "central_screen_x", "central_screen_y", "relocated", "map_baked",
        "lifecycle", "runtime_allowed", "runtime_handoff",
    )
    rows = []
    for candidate in CANDIDATES:
        for binding in bindings:
            instance_id = binding["instance_stable_id"]
            position = CENTRAL_PLACEMENTS.get(instance_id)
            rows.append({
                "candidate_id": candidate.stable_id,
                "instance_stable_id": instance_id,
                "profile_id": PROFILE_ID,
                "topology_sha256": TOPOLOGY_SHA256,
                "anchor": binding["anchor"],
                "footprint": binding["footprint"],
                "facing": binding["facing"],
                "organization_state": "scattered",
                "central_visible": str(position is not None).lower(),
                "central_screen_x": position[0] if position else "",
                "central_screen_y": position[1] if position else "",
                "relocated": "false",
                "map_baked": "false",
                "lifecycle": "Candidate",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
            })
    write_tsv(OUT / "map-b-central-overlay-placement.tsv", fieldnames, rows)


def write_source_receipt() -> None:
    fieldnames = ("source_path", "source_sha256", "authority_role", "usage_scope", "validation", "mutation")
    rows = []
    for relative, expected, role, scope in STATIC_SOURCES:
        rows.append({
            "source_path": relative,
            "source_sha256": expected,
            "authority_role": role,
            "usage_scope": scope,
            "validation": "exact_sha256_pass",
            "mutation": "none",
        })
    for relative, role, scope in SCOPED_CANON_SOURCES:
        rows.append({
            "source_path": relative,
            "source_sha256": sha256_file(ROOT / relative),
            "authority_role": role,
            "usage_scope": scope,
            "validation": "scoped_semantic_pass_whole_file_hash_observed",
            "mutation": "none",
        })
    write_tsv(OUT / "source-validation-receipt.tsv", fieldnames, rows)


def write_user_decision_card() -> None:
    content = f"""# C01E02 A3 用户决策卡

> Package: `{PACKAGE_ID}`  
> Subject: `{SUBJECT_ID}`  
> Gate: `individual user decision required`  
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 请逐项裁决

1. **主轮廓**：A 伏壳钳足型 / B 折脊跃扑型 / C 偏轴三足型，或指出窄改组合。
2. **与 BREAKER B＋X 的同源程度**：通过 / 偏近 / 偏远。
3. **移动语法**：A 对角爬行 / B 短距跃扑 / C 三足侧掠，或指出窄改。
4. **实例规则**：一个母版＋六实例轻差分是否足够。
5. **运行尺度**：96/128px 与建筑遮挡的淡出＋轮廓是否通过。

建议回复格式：`A；同源程度通过；爬行；六实例轻差分足够；96/128与遮挡通过`。

## 当前边界

- 这些方向不锁物种名、能力、动机或最终棋盘数量，不反写 Canon。
- MAP-B 图仅是评审合成，小体没有烘入地图。
- 未生成最终 atlas、逐帧动作、死亡演出、Cut-in、视频、LibTV 或 Runtime handoff。
- 只有五项均获明确批准后，才可由制作人另派正式四向 atlas。
"""
    (OUT / "user-decision-card.md").write_text(content, encoding="utf-8")


def write_completion_report() -> None:
    content = f"""# C01E02 A3 Completion Report

## Result

- Package: `{PACKAGE_ID}`
- Subject: `{SUBJECT_ID}`
- Candidate directions: `3`
- Native transparent review samples: `24` (`3 candidates × 4 facings × 2 sizes`)
- MAP-B CENTRAL review composites: `3`; existing anchors retained; `4/6` instances visible per composite.
- Instance model: one `1×1` master identity plus six light variants.
- Pivot: `bottom_center`.
- Occlusion: `fade_plus_outline` review proof.

## Authority Boundary

`ENEMY_C01_RIFT_SWARM` remains a Working neutral technical anchor. A3 does not lock species name, final form, ability, motive, or final board count. BREAKER B＋X and MAP-B are derivative/review references only, not Runtime masters.

All outputs are `Candidate`, `runtime_allowed=false`, `runtime_handoff=none`. No Godot, Runner, R2 manifest, gameplay, footprint, Canon, Runtime, LibTV, video, final atlas, staged files, or commits were produced by this task.

## Stop Gate

Stopped for the five individual user decisions in `user-decision-card.md`. Formal four-facing atlas work is not authorized here.
"""
    (OUT / "completion-report.md").write_text(content, encoding="utf-8")


def media_info(path: Path) -> tuple[str, str, str]:
    suffix = path.suffix.lower()
    if suffix == ".png":
        with Image.open(path) as opened:
            media_type = "image/png"
            dimensions = f"{opened.width}x{opened.height}"
            channels = opened.mode
        return media_type, dimensions, channels
    if suffix == ".tsv":
        return "text/tab-separated-values", "", "UTF-8"
    if suffix == ".md":
        return "text/markdown", "", "UTF-8"
    if suffix == ".py":
        return "text/x-python", "", "UTF-8"
    return "application/octet-stream", "", ""


def package_files(*, include_manifest: bool = False) -> list[Path]:
    excluded = {"delivery-hashes.sha256", "BLOCKED.md"}
    if not include_manifest:
        excluded.add("asset-manifest.tsv")
    return sorted(
        path for path in OUT.rglob("*")
        if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )


def candidate_for_path(relative: str) -> str:
    for candidate in CANDIDATES:
        if f"A3_{candidate.code}_" in relative or f"candidate_{candidate.code.lower()}" in relative:
            return candidate.stable_id
    return "ALL_THREE_CANDIDATES"


def write_manifest() -> None:
    fieldnames = (
        "package_id", "asset_id", "relative_path", "subject_id", "candidate_scope", "media_type", "dimensions",
        "channels", "review_scope", "uses_old_asset", "uses_final_atlas", "map_baked", "lifecycle",
        "runtime_allowed", "runtime_handoff", "sha256",
    )
    rows = []
    for path in package_files():
        relative = path.relative_to(OUT).as_posix()
        media_type, dimensions, channels = media_info(path)
        rows.append({
            "package_id": PACKAGE_ID,
            "asset_id": f"A3_RIFT_SWARM_{relative.upper().replace('/', '_').replace('.', '_').replace('-', '_')}",
            "relative_path": relative,
            "subject_id": SUBJECT_ID,
            "candidate_scope": candidate_for_path(relative),
            "media_type": media_type,
            "dimensions": dimensions,
            "channels": channels,
            "review_scope": "direction_review_only",
            "uses_old_asset": "false",
            "uses_final_atlas": "false",
            "map_baked": "false",
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "sha256": sha256_file(path),
        })
    write_tsv(OUT / "asset-manifest.tsv", fieldnames, rows)


def write_hashes() -> None:
    lines = []
    for path in package_files(include_manifest=True):
        relative = path.relative_to(OUT).as_posix()
        lines.append(f"{sha256_file(path)}  {relative}")
    (OUT / "delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    bindings = validate_sources()
    SAMPLES.mkdir(parents=True, exist_ok=True)

    for candidate in CANDIDATES:
        identity_sheet(candidate).save(OUT / f"A3_candidate_{candidate.code.lower()}_identity_sheet_1800x1200.png")
        for facing in FACINGS:
            for native_size in SAMPLE_SIZES:
                render_sprite(candidate, facing, native_size).save(SAMPLES / f"A3_{candidate.code}_{facing}_{native_size}_review.png")

    direction_board().save(OUT / "A3_direction_board_3000x1800.png")
    four_direction_action_board().save(OUT / "A3_four_direction_action_space_3000x1800.png")
    footprint_occlusion_board().save(OUT / "A3_footprint_pivot_occlusion_2400x1350.png")
    variation_board().save(OUT / "A3_one_master_six_variants_2400x1200.png")

    composites: dict[str, Image.Image] = {}
    for candidate in CANDIDATES:
        composite = map_composite(candidate, bindings)
        composites[candidate.code] = composite
        composite.save(OUT / f"A3_{candidate.code}_MAP_B_CENTRAL_composite_1280x720.png")
    map_comparison_board(composites).save(OUT / "A3_MAP_B_CENTRAL_comparison_3000x1200.png")

    write_candidate_spec()
    write_sample_index()
    write_instance_variation_spec()
    write_map_placement(bindings)
    write_source_receipt()
    write_user_decision_card()
    write_completion_report()
    write_manifest()
    write_hashes()


if __name__ == "__main__":
    main()
