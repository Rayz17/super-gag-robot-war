#!/usr/bin/env python3
"""Generate C01E02 G1.5-B3 tactical-map Candidate layer packages."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[6]

CONTRACT_COMMIT = "a851398347806850c8b0e0ce6a4d83a14e0677bb"
SNAPSHOT_REF = "fe7a0764d11f5ac5f9d11accb7398df664132b0b"
CONTENT_FINGERPRINT = "944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94"
PROFILE_ID = "c01cdv1_s06_g1_v1"
STABLE_STATE = "C01CDV1_JOINT_S06_T2_STAGE1_V1"
MAP_SLOT = "BG_C01CDV1_PLAZA_TACTICAL"

WIDTH = 1280
HEIGHT = 720
BOARD_COLS = 12
BOARD_ROWS = 9
BOARD_BBOX = (105, 132, 840, 510)
UI_GAP = (852, 54, 884, 648)
INTENT_PANEL = (885, 78, 1240, 196)
COMMAND_PANEL = (885, 210, 1240, 624)
GZ_BBOX = (420, 276, 560, 348)
BREAKER_BBOX = (280, 330, 490, 438)
IMPACT_BBOX = (385, 222, 700, 384)
HOTSPOT = (1, 2)
HOTSPOT_CENTER = (385, 204)

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

INK_DEEP = "#071318"
INK = "#14272f"
INK_SOFT = "#263942"
PAPER = "#eef2f0"
PAPER_WARM = "#f7f5ed"
MUTED = "#809097"
TEAL = "#55a7a2"
TEAL_DARK = "#2f7475"
RED = "#d9473f"
RED_BRIGHT = "#ff6655"
GOLD = "#d6a63c"
AMBER = "#ef9b4a"
BLUE = "#426b8c"
OLIVE = "#687766"
WHITE = "#ffffff"


# path, ref, expected git blob, expected sha256, receipt role
SOURCE_LOCKS = (
    ("docs/superpowers/specs/production/c01-current-demo-v1/00-demo-source-authorization.md", CONTRACT_COMMIT, "59f394ce9610da3c38ecbcf4852c1bbc2b3dc8d8", "4b13e04b45fbc3c5d5f8c770c7a5921044cde5c9238ca91aabd571101e97e6ab", "demo_authorization"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/02-e02-s01-s07-beat-runtime-map.tsv", CONTRACT_COMMIT, "6ac539981b4743272a47861fcadafbd300d333a2", "cb7c74b80af20f339ecea63b1cb11e13162abb1ef257bbf575f79a2e28b34584", "beat_runtime_map"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/04-e02-previs-v0.1.md", CONTRACT_COMMIT, "339f72163af25b37a2fd1415e98e704f5e196183", "ca601618c484250c2db5bf6677cb122715476e08561e8229f4fa5f8881192640", "previs_contract"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/05-e02-asset-call-matrix.tsv", CONTRACT_COMMIT, "1ec11b928c033050ceee11290027c970fd0b4831", "d4b1db2ab9c93129329ae86860e25e66a42f992593ed8bd1d9d1dc480e23f267", "asset_matrix"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/06-e02-state-checkpoint-contract.tsv", CONTRACT_COMMIT, "eaf89203798d7274201a2e259ecb0154c4afd16f", "c1450b64d941b9ee513d3a0800b712eac522a726217c759e07a773813b333bbf", "checkpoint_contract"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/07-legacy-denylist.tsv", CONTRACT_COMMIT, "ea2930809ceaa302c0758cb92057e6f27d9a7884", "53eac4ef1b0c4b9a8d173c8392daa58510a31b4bda3290fd0be9942e61a5c920", "denylist"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/09-frozen-source-snapshot.tsv", CONTRACT_COMMIT, "288b87d11fc8333212b1a1559a02380233a29a6b", "5d37ad8c5639ae41f01f856097656caa378598c13ce3278d17876803412808d4", "frozen_source_manifest"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/09b-frozen-visual-snapshot.tsv", CONTRACT_COMMIT, "108b101aeb13dce0b6a15861fab970dea4d4c763", "4eec352ef11b7f6706559c2d7f3285136dba6781e4892066718696795dd89713", "frozen_visual_manifest"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/10-cross-session-coordination.md", CONTRACT_COMMIT, "2648869284ff890a09753ed7bd0ee85a29e16fbb", "2440f94bc880e89990d9825b51bcb7d476b106db8a4ffe1ae740dccff063d82d", "cross_session"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/13-demo-build-contract.json", CONTRACT_COMMIT, "93d5727b25d8c397f25fa355d88e7ed1edf9e362", "ff76cba762dfb7458cb1a33784ccca766f549ce929d9d04f8b2ebc24c128f0b7", "build_contract"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/14-g1-joint-alignment-rework.md", CONTRACT_COMMIT, "13d6b3abd90365b2ff33ae6cc2050429cd763081", "b2fc581490e3314608dbd0da683dadbac763a61d6f7775fd0c30797f2c46fbd6", "joint_alignment"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/15-g1-5-representative-art-pilot.md", CONTRACT_COMMIT, "9fa5548a4ce81f935a86ba1f3ea322146a00e750", "844e9d15b8be1575f33b0b06992044a0cc7338284d27747802bce88eaae84b6f", "g15_parent"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/16-g1-5-b1-breaker-art-objective.md", CONTRACT_COMMIT, "f7647acbd306d6e5abe20c4a03f94e330a89ad10", "b9e858adce3b3bd8184c979e6702f2dec97c7cd7735f9c6e2f062a0f4d5dcc12", "b1_objective"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/17-g1-5-b2-retired-shield-art-objective.md", CONTRACT_COMMIT, "dbd893e0463b0684244335f181e1a20eb8a8f015", "83ec0b8041a934290561b19ab08b6d2d7407ae363ff74ab5326fe30cd5ff4147", "b2_objective"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/18-g1-5-b3-tactical-map-art-objective.md", CONTRACT_COMMIT, "16da40a63467f0a897ee3e97b9c87aa067785fc7", "d9f1c67ce7beddaf376cbcfee707e145f0c36f21c246fad7e9fcb977de587bcc", "b3_objective"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv", CONTRACT_COMMIT, "3fecd3ea5bef592611bf0dbd9ce920b60c26d57f", "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee", "a1_receipt"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv", CONTRACT_COMMIT, "4004e1db13e96d54a48241bb5cc03233f2a95540", "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920", "b1_receipt"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b2-user-approval-receipt.tsv", CONTRACT_COMMIT, "53feb12efe346862b3346408322bfc03b0b19abb", "792d9061b804ec3d87d79c777171f5aa4bd44979416c40d45d8968a2004d0c51", "b2_receipt"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/g15-b1-readonly-review.md", CONTRACT_COMMIT, "1fb367bef75b123ccc9447a6c79460e29f6655c3", "285c16dfae9eb205c5ceb0c001ab47035bcb6d31a6c692b2a6bd6864db18c20f", "b1_review"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/g15-b2-readonly-review.md", CONTRACT_COMMIT, "fc27e4566f2407a9f164fddcb3c13c029daee8a6", "0a083c49c8102186693ee6dbdd236fcc3b5905f10b54048b4c55e7bf62c665e3", "b2_review"),
    ("docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-物理因果与人物站位板.md", SNAPSHOT_REF, "f8f3b3e05e3cdcc1a6b9a83c5c22447543848343", "9ac19c4a71918f61a41945706ca4088e5647ebd186d5b28cbadb192310a16c5a", "physical_board"),
    ("docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-战斗与玩法预案.md", SNAPSHOT_REF, "59271ccad7ee74790e06f1cd3f2e89bc864d11e9", "4cd3a68cc15e3761c67335c76849ca4b66058a08770447505d38059069572769", "battle_preplan"),
    ("docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/episodes/C01/C01E02-巨神从展台起身-v1.md", SNAPSHOT_REF, "baaa4722f88ec291bfa7351249b87a8534a24463", "f6e8d94a69a8bc9967a9deb30173b56a4e9daa65904a85fcb90c3c454fbc1f81", "current_e02_reader_regression"),
    ("docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/story/C01E02-纯剧情Reader-v2.md", SNAPSHOT_REF, "2e0a52e14bec4f91b10c8703ee60f627afe15be9", "dd07412d84e8b21918a8369a312b0125fdd452b74d229602c8dde1922b8237b1", "candidate_e02_reader"),
    ("docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/gameflow/C01-游戏流程解构-v1.md", SNAPSHOT_REF, "d776ff397c8ba45467e0c08a24a1f6ff019e4817", "284771d905e0283b32e33c436e9a9c47a5578b1a7bbed6927ffb4fea7b14312b", "candidate_gameflow"),
    ("docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md", SNAPSHOT_REF, "b91c05116e8d102652fe3d582a5dc6c64eb11276", "083b4678567f6d7e664939bc0e5227063765308a2f71b2be71168cb1215162ab", "full_outline"),
    ("docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md", SNAPSHOT_REF, "ef7a08099fd2f7fb164df1334b5416ba11d0a603", "ec061505dc395c96136e9415985706ecf6c99c564e68c0c5686968581f40b653", "art_language_A"),
    ("docs/superpowers/specs/data/canon/authority_manifest.tsv", SNAPSHOT_REF, "fdb2057b833f4dfa0ad49a1229590c515d0e1a08", "d5203da48a7634c1ed977e5a638403d03cc3797980342747c83cfbb39c24969a", "frozen_authority"),
    ("docs/superpowers/specs/data/canon/entities.tsv", SNAPSHOT_REF, "5d84ad9c4a3d82dac7015248261e22fe752bbd1c", "5c296a4f181257b1d8cfa05dc704339b70d38b6fd9f7a23fbb03ca920feb7b95", "frozen_entities"),
    ("docs/superpowers/specs/data/canon/scenes.tsv", SNAPSHOT_REF, "9724d7b814368f0bf2279430ad40797278c822ce", "66addddc57b2a0827008c5b8e32e9aa0155ca7627e6f1a7d109432b0bfbac434", "frozen_scenes"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/main-g1/BASELINE_S06_T2_STAGE1_1280x720.png", CONTRACT_COMMIT, "e54cb24e3dd36f301cc949a10a9b6799942b1143", "cda95fcfd14dc6ed9ba52fbe04810130ae348f1fb2153acb4feb59b1f1ebe943", "program_baseline"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png", CONTRACT_COMMIT, "a5863aa4f8913b211cd4479c1d5cd895396e17d3", "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e", "GZ_C_scale_evidence"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png", CONTRACT_COMMIT, "eec78e45a5d93e6e6e9eadfa9bcbdd41a0f6d678", "e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4", "BREAKER_B_scale_evidence"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b2-retired-shield/RETIRED_SHIELD_B2_candidate_A_wall_hung_128.png", CONTRACT_COMMIT, "3aa00129f34f8080456b7f9fb27d9c6c91ae29e5", "17e8821b773ad53302ea2358d34c76465f7b01cc01347b6e8c53c78f66860923", "shield_A_wall_evidence"),
)


@dataclass(frozen=True)
class Candidate:
    code: str
    stable_id: str
    title: str
    identity: str
    material: str
    lighting: str
    density: str
    occlusion: str
    strength: str
    risk: str
    seed: int


CANDIDATES = (
    Candidate(
        "A",
        "CAND_C01CDV1_PLAZA_MAP_A_TRACK_OPEN_V1",
        "旧会展轨道开阔型",
        "宽阔旧混凝土、失活轨槽与低矮服务线；主战面最开阔。",
        "冷灰混凝土 + 深墨蓝失活轨槽 + 少量旧黄铜边件。",
        "北侧馆体冷白漏光，南侧承冲区保持低明度。",
        "低；大面优先，旧损集中在轨槽和南缘。",
        "棋盘外低矮检修栏；南缘入格部分使用软淡出。",
        "移动、面向和冲撞带最容易读。",
        "需防止过空、像测试场，或把旧轨槽误读成舰体机关。",
        1101,
    ),
    Candidate(
        "B",
        "CAND_C01CDV1_PLAZA_MAP_B_MUSEUM_DISASTER_V1",
        "馆墙防灾广场型",
        "西北破损展墙、开放式重盾挂架与东北城市立面形成明确保护方向。",
        "制式防灾铺装 + 冷白馆墙 + 克制的港区修补色块。",
        "馆墙背光较亮，居民方向用少量暖窗保持城市存在感。",
        "中；细节集中在棋盘外馆墙和边缘，不进入主战格。",
        "棋盘外馆墙框景；仅南角低栏进入投影区并配软淡出。",
        "万机馆、重盾来源与北侧保护对象最清楚。",
        "墙和防灾设施必须保持开放/架空，不能像 blocked cell。",
        2202,
    ),
    Candidate(
        "C",
        "CAND_C01CDV1_PLAZA_MAP_C_RAIN_MIX_V1",
        "雨夜混合型",
        "轨槽骨架与馆墙同时保留，以雨面、烟和远处火光增强战场电影感。",
        "深蓝灰湿面 + 冷白建筑边 + 少量琥珀火光反射。",
        "整体更暗，单位和程序 UI 仍保持最高对比。",
        "中高但受控；反射为大块，雨线稀疏，不做碎高光。",
        "棋盘外弧形雨棚和破损栏杆；南缘软淡出面积最大。",
        "场景气氛和章节峰值最强，同时保留两个空间锚。",
        "需防止雨、反光与旧损形成假格线或假障碍。",
        3303,
    ),
)


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_bytes(ref: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def tsv_rows(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8")), delimiter="\t"))


def validate_sources() -> dict[str, bytes]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()
    if head != CONTRACT_COMMIT:
        raise RuntimeError(f"B3 requires HEAD {CONTRACT_COMMIT}, got {head}")

    source_bytes: dict[str, bytes] = {}
    for path, ref, expected_blob, expected_sha, _ in SOURCE_LOCKS:
        actual_blob = subprocess.run(
            ["git", "rev-parse", f"{ref}:{path}"], cwd=ROOT, check=True,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.strip()
        data = git_bytes(ref, path)
        if actual_blob != expected_blob or sha256_bytes(data) != expected_sha:
            raise RuntimeError(f"B3 frozen source mismatch: {ref}:{path}")
        source_bytes[path] = data

    build = json.loads(source_bytes[
        "docs/superpowers/specs/production/c01-current-demo-v1/13-demo-build-contract.json"
    ])
    if build["content_fingerprint"] != CONTENT_FINGERPRINT:
        raise RuntimeError("B3 content fingerprint mismatch")

    task = source_bytes[
        "docs/superpowers/specs/production/c01-current-demo-v1/18-g1-5-b3-tactical-map-art-objective.md"
    ].decode("utf-8")
    for token in (
        "12×9", "108 格", STABLE_STATE,
        "当前 profile 没有 blocked-cell", "A tower shield",
    ):
        if token not in task:
            raise RuntimeError(f"B3 task missing required token: {token}")

    b2_receipt = source_bytes[
        "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b2-user-approval-receipt.tsv"
    ].decode("utf-8")
    for token in ("A_TOWER_SHIELD", "F_D70_P30", "FOUR_STATE_CONTINUITY_APPROVED_AS_SHOWN", "not_final_A_plus_F_master"):
        if token not in b2_receipt:
            raise RuntimeError(f"B3 B2 approval mismatch: {token}")

    b1_receipt = source_bytes[
        "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv"
    ].decode("utf-8")
    for token in ("B_FORELIMB_BEARER", "X_ALIEN_BIO_ARMOR", "X_surface_requires_future_derivation"):
        if token not in b1_receipt:
            raise RuntimeError(f"B3 B1 approval mismatch: {token}")

    return source_bytes


def project(x: float, y: float) -> tuple[int, int]:
    return (round(420 + (x - y) * 35), round(150 + (x + y) * 18))


def cell_center(x: int, y: int) -> tuple[int, int]:
    return project(x, y)


def cell_polygon(x: int, y: int) -> list[tuple[int, int]]:
    cx, cy = cell_center(x, y)
    return [(cx, cy - 18), (cx + 35, cy), (cx, cy + 18), (cx - 35, cy)]


def board_polygon() -> list[tuple[int, int]]:
    return [(420, 132), (840, 348), (525, 510), (105, 294)]


def geometry_payload() -> dict[str, object]:
    return {
        "state": STABLE_STATE,
        "profile": PROFILE_ID,
        "board": [BOARD_COLS, BOARD_ROWS],
        "centers": [cell_center(x, y) for y in range(BOARD_ROWS) for x in range(BOARD_COLS)],
        "board_bbox": BOARD_BBOX,
        "ui_gap": UI_GAP,
        "gz_bbox": GZ_BBOX,
        "breaker_bbox": BREAKER_BBOX,
        "impact_bbox": IMPACT_BBOX,
        "hotspot": [*HOTSPOT, *HOTSPOT_CENTER],
    }


GEOMETRY_SIGNATURE = sha256_bytes(
    json.dumps(geometry_payload(), ensure_ascii=False, sort_keys=True).encode("utf-8")
)


def board_mask() -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(mask).polygon(board_polygon(), fill=255)
    return mask


def rgba_color(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    value = hex_color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def composite_rgba(base: Image.Image, layer: Image.Image) -> Image.Image:
    canvas = base.convert("RGBA")
    return Image.alpha_composite(canvas, layer.convert("RGBA"))


def paste_by_alpha_bottom(canvas: Image.Image, sprite: Image.Image, center_x: int, bottom_y: int) -> None:
    sprite = sprite.convert("RGBA")
    bbox = sprite.getchannel("A").getbbox()
    if bbox is None:
        return
    visual_center_x = (bbox[0] + bbox[2]) // 2
    origin = (center_x - visual_center_x, bottom_y - bbox[3])
    canvas.alpha_composite(sprite, origin)


def text_wrap(draw: ImageDraw.ImageDraw, text: str, box_width: int, text_font: ImageFont.FreeTypeFont) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if current and draw.textbbox((0, 0), trial, font=text_font)[2] > box_width:
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
    spacing: int = 6,
) -> int:
    used_font = font(size, bold=bold)
    y = xy[1]
    for paragraph in text.split("\n"):
        for line in text_wrap(draw, paragraph, width, used_font):
            draw.text((xy[0], y), line, font=used_font, fill=fill)
            y += size + spacing
        y += spacing
    return y


def _clip_to_board(layer: Image.Image) -> Image.Image:
    layer = layer.convert("RGBA")
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), board_mask()))
    return layer


def _draw_distant_city(draw: ImageDraw.ImageDraw, candidate: Candidate) -> None:
    skyline = "#17282f" if candidate.code != "C" else "#13242b"
    mid = "#21343b" if candidate.code != "B" else "#2a3b41"
    draw.rectangle((0, 54, 884, 300), fill=skyline)
    blocks = [
        (18, 142, 94, 300), (86, 118, 158, 300), (151, 166, 236, 300),
        (594, 166, 648, 306), (642, 118, 708, 306), (700, 150, 770, 306),
        (760, 105, 838, 306), (825, 174, 884, 306),
    ]
    for index, rect in enumerate(blocks):
        draw.rectangle(rect, fill=mid if index % 2 else skyline)
        x0, y0, x1, _ = rect
        for x in range(x0 + 12, x1 - 5, 19):
            for y in range(y0 + 18, min(250, y0 + 90), 25):
                if (x + y + candidate.seed) % 3:
                    color = "#7d877b" if candidate.code == "B" else "#536c70"
                    draw.rectangle((x, y, x + 5, y + 8), fill=color)
    draw.polygon([(0, 254), (190, 226), (360, 268), (548, 232), (884, 284), (884, 340), (0, 340)], fill="#1a2d34")


def _draw_museum_frame(draw: ImageDraw.ImageDraw, candidate: Candidate) -> None:
    # The rack is deliberately skeletal: it gives the shield a physical source
    # without reading as a blocked ground cell.
    if candidate.code == "A":
        draw.line([(238, 216), (306, 116), (448, 122), (515, 238)], fill=INK_DEEP, width=18, joint="curve")
        draw.line([(250, 213), (312, 132), (442, 137), (500, 232)], fill="#53666d", width=8, joint="curve")
        draw.line([(306, 116), (365, 92), (448, 122)], fill="#6c7773", width=11, joint="curve")
        draw.line([(269, 208), (483, 228)], fill="#354950", width=6)
    elif candidate.code == "B":
        draw.polygon([(188, 226), (244, 98), (370, 82), (356, 192), (292, 216)], fill="#34474e", outline=INK_DEEP)
        draw.polygon([(438, 115), (562, 154), (598, 277), (504, 244), (464, 188)], fill="#3e5056", outline=INK_DEEP)
        draw.polygon([(212, 213), (262, 119), (342, 108), (328, 178), (282, 202)], fill="#738083")
        draw.polygon([(460, 135), (535, 162), (563, 239), (510, 222), (480, 178)], fill="#6b7778")
        draw.line([(288, 218), (338, 130), (455, 139), (511, 245)], fill=INK_DEEP, width=15, joint="curve")
        draw.line([(300, 211), (346, 145), (447, 153), (495, 235)], fill="#a1aaa5", width=6, joint="curve")
    else:
        draw.polygon([(206, 230), (268, 108), (380, 90), (355, 194), (288, 220)], fill="#2f444b", outline=INK_DEEP)
        draw.line([(282, 215), (333, 120), (456, 135), (520, 247)], fill=INK_DEEP, width=17, joint="curve")
        draw.line([(294, 210), (341, 137), (447, 149), (504, 239)], fill="#637377", width=7, joint="curve")
        draw.line([(334, 121), (391, 98), (456, 135)], fill="#7f8982", width=9, joint="curve")


def _draw_board_surface(base: Image.Image, candidate: Candidate) -> None:
    colors = {"A": "#51636a", "B": "#5d6a6d", "C": "#465960"}
    draw = ImageDraw.Draw(base)
    draw.polygon(board_polygon(), fill=colors[candidate.code], outline=INK_DEEP, width=5)

    detail = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    dd = ImageDraw.Draw(detail)
    # Large paving seams are intentionally off the tactical-cell cadence.
    seam = rgba_color("#253b43", 92)
    for x in (1.8, 5.9, 10.3):
        dd.line([project(x, -0.6), project(x, 9.5)], fill=seam, width=3)
    for y in (2.7, 6.25):
        dd.line([project(-0.8, y), project(12.4, y)], fill=seam, width=3)

    if candidate.code == "A":
        for y in (6.1, 6.72):
            dd.line([project(-0.5, y), project(12.1, y)], fill=rgba_color("#172b33", 205), width=9)
            dd.line([project(-0.5, y - 0.06), project(12.1, y - 0.06)], fill=rgba_color("#9a8b66", 118), width=2)
        dd.line([project(1.2, -0.4), project(1.2, 9.2)], fill=rgba_color("#c5c6b7", 75), width=6)
        dd.polygon([project(7.4, 7.2), project(11.8, 7.2), project(11.8, 8.7), project(7.4, 8.7)], fill=rgba_color("#394c53", 125))
    elif candidate.code == "B":
        dd.polygon([project(-0.2, 0.4), project(5.3, 0.4), project(5.3, 2.1), project(-0.2, 2.1)], fill=rgba_color("#a8b4af", 55))
        dd.polygon([project(7.4, 0.3), project(12.1, 0.3), project(12.1, 2.0), project(7.4, 2.0)], fill=rgba_color("#8c9a96", 48))
        for offset in (0, 18, 36):
            dd.arc((150 + offset, 188 + offset, 812 - offset, 548 - offset), 196, 334, fill=rgba_color("#30484f", 105), width=3)
        dd.line([project(-0.2, 7.1), project(11.7, 7.1)], fill=rgba_color("#86928a", 80), width=8)
    else:
        for y in (6.35, 6.86):
            dd.line([project(-0.4, y), project(12.0, y)], fill=rgba_color("#152c34", 190), width=8)
            dd.line([project(-0.4, y - 0.07), project(12.0, y - 0.07)], fill=rgba_color("#8b866d", 95), width=2)
        dd.polygon([project(0.0, 0.5), project(4.3, 0.5), project(4.3, 2.3), project(0.0, 2.3)], fill=rgba_color("#9faeaa", 42))
        dd.polygon([project(7.6, 5.0), project(11.8, 5.0), project(11.8, 8.4), project(7.6, 8.4)], fill=rgba_color("#263d45", 110))
        dd.line([project(2.4, -0.2), project(2.4, 9.1)], fill=rgba_color("#bbc1b4", 50), width=5)

    base.alpha_composite(_clip_to_board(detail))
    draw = ImageDraw.Draw(base)
    draw.line(board_polygon() + [board_polygon()[0]], fill="#9aa7a4", width=2, joint="curve")


def make_base(candidate: Candidate) -> Image.Image:
    sky = "#102129" if candidate.code != "C" else "#0d1d25"
    base = Image.new("RGBA", (WIDTH, HEIGHT), sky)
    draw = ImageDraw.Draw(base)
    _draw_distant_city(draw, candidate)
    # The UI reserve stays quiet but remains an opaque scene plate.
    draw.rectangle((884, 54, 1279, 648), fill="#18272e")
    draw.rectangle((884, 0, 1279, 53), fill="#102028")
    draw.rectangle((884, 649, 1279, 719), fill="#102028")
    _draw_museum_frame(draw, candidate)
    # Southern apron is continuous ground, drawn beneath the tactical surface.
    draw.polygon([(53, 493), (534, 568), (852, 488), (852, 648), (0, 648), (0, 532)], fill="#20343b")
    draw.line([(58, 493), (534, 559), (852, 480)], fill="#40555b", width=5)
    _draw_board_surface(base, candidate)

    draw = ImageDraw.Draw(base)
    # Open north-east city edge. No wall closes any tactical cell.
    draw.line([(670, 238), (804, 307)], fill="#91a29f", width=5)
    draw.line([(683, 224), (817, 292)], fill="#2d434a", width=13)
    draw.line([(692, 225), (821, 291)], fill="#83918d", width=4)
    for cx, cy in ((731, 253), (767, 272), (802, 290)):
        draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill="#b5b7a3")

    return base.convert("RGB")


def make_weather_damage(candidate: Candidate) -> Image.Image:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    rng = random.Random(candidate.seed)

    # Broad wet reflections, clipped to the continuous plaza surface.
    wet = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wet)
    puddle_count = {"A": 5, "B": 4, "C": 8}[candidate.code]
    for _ in range(puddle_count):
        cx = rng.randint(180, 760)
        cy = rng.randint(230, 485)
        rx = rng.randint(36, 105)
        ry = rng.randint(5, 13)
        color = rgba_color("#b7cbc7", rng.randint(18, 42) if candidate.code != "C" else rng.randint(28, 58))
        wd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=color)
    layer.alpha_composite(_clip_to_board(wet))

    draw = ImageDraw.Draw(layer)
    rain_count = {"A": 46, "B": 54, "C": 82}[candidate.code]
    for _ in range(rain_count):
        x = rng.randint(28, 850)
        y = rng.randint(64, 620)
        length = rng.randint(8, 22)
        alpha = rng.randint(30, 72) if candidate.code != "C" else rng.randint(42, 92)
        draw.line((x, y, x - 4, y + length), fill=(200, 218, 218, alpha), width=1)

    # Old surface damage is sparse and does not follow cell boundaries.
    crack_sets = {
        "A": [((172, 374), (205, 385), (226, 379)), ((642, 421), (670, 414), (691, 425))],
        "B": [((146, 340), (176, 351), (194, 347)), ((716, 388), (744, 380), (766, 387))],
        "C": [((160, 362), (187, 372), (215, 366)), ((617, 438), (653, 428), (681, 436)), ((515, 201), (538, 213), (557, 207))],
    }
    for points in crack_sets[candidate.code]:
        draw.line(points, fill=(20, 35, 42, 105), width=3, joint="curve")
        for px, py in points[1:]:
            draw.line((px, py, px + 8, py + 6), fill=(22, 39, 45, 70), width=2)

    # Smoke and a restrained distant amber reflection remain separate atmosphere.
    haze = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze)
    for cx, cy, rx, ry, alpha in (
        (242, 168, 86, 34, 42), (282, 143, 62, 27, 38), (760, 318, 54, 19, 26),
    ):
        hd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(49, 62, 63, alpha))
    if candidate.code == "C":
        hd.ellipse((733, 298, 823, 342), fill=(238, 137, 69, 38))
        hd.ellipse((747, 310, 809, 333), fill=(255, 185, 92, 28))
    haze = haze.filter(ImageFilter.GaussianBlur(16))
    layer.alpha_composite(haze)
    return layer


def make_shield_state(candidate: Candidate, *, empty: bool) -> Image.Image:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = HOTSPOT_CENTER
    frame = "#8c8266" if candidate.code != "C" else "#777765"
    dark = "#12252c"
    # Open gantry: no feet or solid wall occupy the hotspot cell.
    draw.line((cx - 45, cy - 52, cx + 45, cy - 52), fill=rgba_color(dark, 245), width=10)
    draw.line((cx - 39, cy - 52, cx - 30, cy + 42), fill=rgba_color(dark, 230), width=7)
    draw.line((cx + 39, cy - 52, cx + 30, cy + 42), fill=rgba_color(dark, 230), width=7)
    draw.line((cx - 42, cy - 52, cx + 42, cy - 52), fill=rgba_color(frame, 255), width=4)

    if empty:
        draw.arc((cx - 27, cy - 24, cx - 7, cy + 6), 80, 276, fill=rgba_color("#a99b72", 230), width=5)
        draw.arc((cx + 7, cy - 24, cx + 27, cy + 6), -96, 100, fill=rgba_color("#a99b72", 230), width=5)
        draw.line((cx - 18, cy + 30, cx + 18, cy + 30), fill=rgba_color(frame, 210), width=6)
        draw.line((cx - 31, cy + 42, cx - 13, cy + 32), fill=rgba_color("#6f5f4d", 190), width=3)
        draw.line((cx + 31, cy + 42, cx + 13, cy + 32), fill=rgba_color("#6f5f4d", 190), width=3)
        return layer

    outline = [
        (cx - 25, cy - 40), (cx + 24, cy - 40), (cx + 31, cy - 24),
        (cx + 29, cy + 25), (cx + 18, cy + 42), (cx - 18, cy + 42),
        (cx - 29, cy + 24), (cx - 31, cy - 24),
    ]
    draw.polygon(outline, fill=rgba_color("#12262e", 255))
    inner = [
        (cx - 19, cy - 34), (cx + 17, cy - 34), (cx + 23, cy - 20),
        (cx + 21, cy + 21), (cx + 13, cy + 34), (cx - 13, cy + 34),
        (cx - 21, cy + 20), (cx - 23, cy - 20),
    ]
    draw.polygon(inner, fill=rgba_color("#5c6c70", 255))
    # F direction: one large 30% repair patch, not small noisy repairs.
    patch = [(cx - 17, cy + 5), (cx + 1, cy - 2), (cx + 8, cy + 30), (cx - 12, cy + 34)]
    draw.polygon(patch, fill=rgba_color(OLIVE, 245), outline=rgba_color("#33463f", 240))
    draw.rectangle((cx - 4, cy - 31, cx + 5, cy + 30), fill=rgba_color("#849397", 210))
    for sx, sy in ((cx - 14, cy - 21), (cx + 14, cy + 9), (cx - 8, cy + 24)):
        draw.ellipse((sx - 3, sy - 2, sx + 3, sy + 2), fill=rgba_color("#2a211d", 255), outline=rgba_color("#895c4e", 220))
    return layer


def make_foreground(candidate: Candidate) -> tuple[Image.Image, Image.Image]:
    fg = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fg)
    if candidate.code == "A":
        draw.polygon([(18, 548), (144, 496), (267, 518), (282, 647), (0, 647)], fill=rgba_color("#0d1d23", 238))
        draw.line([(43, 562), (153, 518), (252, 535)], fill=rgba_color("#71807d", 230), width=11, joint="curve")
        draw.line([(46, 574), (154, 531), (245, 548)], fill=rgba_color("#253b42", 255), width=5, joint="curve")
        draw.polygon([(735, 510), (844, 478), (851, 493), (851, 647), (690, 647)], fill=rgba_color("#102229", 230))
        draw.line([(724, 526), (846, 491)], fill=rgba_color("#5f706e", 225), width=10)
        draw.line([(704, 421), (778, 377), (830, 354)], fill=rgba_color("#20373e", 220), width=18, joint="curve")
        draw.line([(708, 416), (780, 373), (830, 351)], fill=rgba_color("#70807c", 205), width=5, joint="curve")
    elif candidate.code == "B":
        draw.polygon([(0, 404), (67, 372), (112, 418), (106, 647), (0, 647)], fill=rgba_color("#0e2027", 242))
        draw.line([(69, 393), (69, 604)], fill=rgba_color("#75827f", 225), width=12)
        draw.polygon([(739, 527), (842, 496), (851, 524), (851, 647), (708, 647)], fill=rgba_color("#12252c", 236))
        draw.line([(735, 539), (841, 509)], fill=rgba_color("#7f8982", 218), width=12)
        draw.line([(706, 422), (777, 379), (829, 355)], fill=rgba_color("#243b42", 222), width=20, joint="curve")
        draw.line([(710, 416), (780, 374), (829, 351)], fill=rgba_color("#87928c", 212), width=6, joint="curve")
    else:
        draw.polygon([(0, 566), (123, 505), (284, 518), (312, 647), (0, 647)], fill=rgba_color("#0b1c23", 242))
        draw.arc((45, 446, 330, 640), 197, 345, fill=rgba_color("#74817d", 240), width=16)
        draw.arc((58, 460, 318, 628), 198, 345, fill=rgba_color("#203941", 255), width=7)
        draw.polygon([(705, 525), (844, 485), (851, 515), (851, 647), (676, 647)], fill=rgba_color("#0d2028", 235))
        draw.line([(699, 543), (846, 500)], fill=rgba_color("#667875", 230), width=13)
        draw.arc((705, 350, 850, 460), 196, 326, fill=rgba_color("#1d353d", 225), width=20)
        draw.arc((711, 355, 845, 454), 198, 326, fill=rgba_color("#71817d", 205), width=6)

    inside = ImageChops.multiply(fg.getchannel("A"), board_mask())
    fade = inside.filter(ImageFilter.GaussianBlur(18))
    return fg, fade


def apply_occlusion_fade(fg: Image.Image, fade: Image.Image) -> Image.Image:
    reduction = fade.point(lambda value: 255 - round(value * 0.72))
    effective = fg.copy()
    effective.putalpha(ImageChops.multiply(fg.getchannel("A"), reduction))
    return effective


def make_geometry_overlay(*, center_dots: bool = True) -> Image.Image:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((0, 0, WIDTH - 1, 54), fill=(66, 63, 110, 45), outline=(180, 170, 235, 120))
    draw.rectangle((0, 648, WIDTH - 1, 719), fill=(66, 63, 110, 45), outline=(180, 170, 235, 120))
    draw.rectangle(UI_GAP, fill=(229, 184, 75, 30), outline=(229, 184, 75, 200), width=2)
    draw.rectangle(INTENT_PANEL, fill=(212, 69, 62, 20), outline=(212, 69, 62, 220), width=2)
    draw.rectangle(COMMAND_PANEL, fill=(51, 102, 131, 18), outline=(71, 127, 155, 220), width=2)
    for rect in (
        (905, 390, 1050, 428), (1070, 390, 1215, 428),
        (905, 442, 1050, 480), (1070, 442, 1215, 480),
        (905, 494, 1050, 532), (1070, 494, 1215, 532),
    ):
        draw.rectangle(rect, outline=(218, 182, 74, 190), width=2)

    for y in range(BOARD_ROWS):
        for x in range(BOARD_COLS):
            poly = cell_polygon(x, y)
            if y <= 1:
                draw.polygon(poly, fill=(76, 159, 153, 48))
            if 5 <= x <= 7 and 0 <= y <= 5:
                draw.polygon(poly, fill=(220, 57, 49, 58))
            draw.line(poly + [poly[0]], fill=(219, 231, 228, 125), width=1)
            if center_dots:
                cx, cy = cell_center(x, y)
                draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=(247, 249, 244, 230))

    draw.rectangle(GZ_BBOX, fill=(70, 167, 171, 46), outline=(84, 205, 205, 235), width=3)
    draw.rectangle(BREAKER_BBOX, fill=(218, 68, 60, 42), outline=(235, 88, 75, 235), width=3)
    draw.rectangle(IMPACT_BBOX, outline=(255, 94, 75, 220), width=2)
    hx, hy = HOTSPOT_CENTER
    draw.ellipse((hx - 13, hy - 13, hx + 13, hy + 13), outline=(238, 189, 74, 255), width=4)
    draw.line((hx - 18, hy, hx + 18, hy), fill=(238, 189, 74, 220), width=2)
    draw.line((hx, hy - 18, hx, hy + 18), fill=(238, 189, 74, 220), width=2)
    return overlay


def make_readability_composite(
    candidate: Candidate,
    base: Image.Image,
    weather: Image.Image,
    shield_wall: Image.Image,
    foreground: Image.Image,
    fade: Image.Image,
) -> Image.Image:
    canvas = base.convert("RGBA")
    canvas = Image.alpha_composite(canvas, weather)
    canvas = Image.alpha_composite(canvas, make_geometry_overlay(center_dots=False))
    canvas = Image.alpha_composite(canvas, shield_wall)

    gz = Image.open(ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png").convert("RGBA")
    breaker = Image.open(ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png").convert("RGBA")
    paste_by_alpha_bottom(canvas, gz, 490, 348)
    paste_by_alpha_bottom(canvas, breaker, 385, 438)
    canvas = Image.alpha_composite(canvas, apply_occlusion_fade(foreground, fade))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1279, 54), fill=rgba_color("#101f27", 235))
    draw.rectangle((0, 648, 1279, 719), fill=rgba_color("#101f27", 235))
    draw.text((22, 15), f"MAP-{candidate.code}  candidate_evidence", font=font(19, bold=True), fill=PAPER)
    draw.text((1056, 678), "not_runtime", font=font(17), fill=GOLD)
    return canvas.convert("RGB")


def make_state_preview(
    base: Image.Image,
    weather: Image.Image | None,
    shield: Image.Image | None,
    foreground: Image.Image | None,
    fade: Image.Image | None,
) -> Image.Image:
    canvas = base.convert("RGBA")
    if weather is not None:
        canvas = Image.alpha_composite(canvas, weather)
    if shield is not None:
        canvas = Image.alpha_composite(canvas, shield)
    if foreground is not None and fade is not None:
        canvas = Image.alpha_composite(canvas, apply_occlusion_fade(foreground, fade))
    return canvas.convert("RGB")


def fit_image(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Contain an image inside a stable review-board slot."""
    source = image.convert("RGB")
    scale = min(size[0] / source.width, size[1] / source.height)
    resized = source.resize(
        (round(source.width * scale), round(source.height * scale)),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGB", size, "#0b171d")
    canvas.paste(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
    return canvas


def alpha_preview(layer: Image.Image, size: tuple[int, int]) -> Image.Image:
    checker = Image.new("RGBA", (WIDTH, HEIGHT), (31, 46, 53, 255))
    check_draw = ImageDraw.Draw(checker)
    block = 32
    for y in range(0, HEIGHT, block):
        for x in range(0, WIDTH, block):
            if (x // block + y // block) % 2:
                check_draw.rectangle((x, y, x + block - 1, y + block - 1), fill=(48, 64, 69, 255))
    return fit_image(Image.alpha_composite(checker, layer.convert("RGBA")), size)


def labeled_thumbnail(
    board: Image.Image,
    image: Image.Image,
    box: tuple[int, int, int, int],
    label: str,
    *,
    alpha_layer: bool = False,
) -> None:
    x0, y0, x1, y1 = box
    draw = ImageDraw.Draw(board)
    draw.rectangle(box, fill="#0b171d", outline="#607279", width=2)
    preview = alpha_preview(image, (x1 - x0 - 4, y1 - y0 - 38)) if alpha_layer else fit_image(
        image, (x1 - x0 - 4, y1 - y0 - 38)
    )
    board.paste(preview, (x0 + 2, y0 + 2))
    draw.rectangle((x0 + 2, y1 - 35, x1 - 2, y1 - 2), fill="#13252c")
    draw.text((x0 + 12, y1 - 30), label, font=font(18, bold=True), fill=PAPER)


def make_direction_board(packages: dict[str, dict[str, Image.Image]]) -> Image.Image:
    board = Image.new("RGB", (2400, 1600), "#e7ece9")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2399, 108), fill=INK_DEEP)
    draw.text((54, 28), "C01E02 B3 | 旧会展广场战棋地图三方向", font=font(38, bold=True), fill=PAPER)
    draw.text((1770, 39), "Candidate / not_runtime", font=font(23), fill=GOLD)

    column_width = 752
    gap = 20
    left = 52
    accents = {"A": TEAL, "B": GOLD, "C": RED_BRIGHT}
    for index, candidate in enumerate(CANDIDATES):
        x = left + index * (column_width + gap)
        draw.rectangle((x, 132, x + column_width, 1540), fill="#f6f7f3", outline="#aab6b5", width=2)
        draw.rectangle((x, 132, x + column_width, 202), fill=accents[candidate.code])
        draw.text((x + 24, 150), f"MAP-{candidate.code}  {candidate.title}", font=font(27, bold=True), fill=INK_DEEP)

        main = fit_image(packages[candidate.code]["readability"], (704, 396))
        board.paste(main, (x + 24, 226))
        draw.rectangle((x + 24, 226, x + 727, 621), outline=INK_DEEP, width=2)

        mini_width = 224
        labeled_thumbnail(board, packages[candidate.code]["base"], (x + 24, 646, x + 24 + mini_width, 812), "环境底板")
        labeled_thumbnail(board, make_state_preview(
            packages[candidate.code]["base"], packages[candidate.code]["weather"],
            packages[candidate.code]["shield_wall"], None, None,
        ), (x + 264, 646, x + 264 + mini_width, 812), "墙挂重盾")
        labeled_thumbnail(board, make_state_preview(
            packages[candidate.code]["base"], packages[candidate.code]["weather"],
            packages[candidate.code]["shield_empty"], None, None,
        ), (x + 504, 646, x + 504 + mini_width, 812), "取走后空挂点")

        y = 842
        fields = (
            ("场景身份", candidate.identity),
            ("材质 / 光线", f"{candidate.material}\n{candidate.lighting}"),
            ("战棋读法", candidate.strength),
            ("遮挡组织", candidate.occlusion),
            ("主要风险", candidate.risk),
        )
        for label, value in fields:
            draw.text((x + 28, y), label, font=font(20, bold=True), fill=accents[candidate.code])
            y = draw_wrapped(draw, (x + 164, y - 2), value, 548, 19, INK, spacing=4) + 8

        draw.rectangle((x + 24, 1459, x + column_width - 24, 1512), fill="#13252c")
        draw.text((x + 40, 1474), f"geometry {GEOMETRY_SIGNATURE[:12]} | 12x9 / 108 cells", font=font(18), fill="#c8d4d0")

    draw.text((54, 1560), "三案只改变材质、明暗、环境密度与遮挡组织；坐标、路径、单位、胜法与程序 UI 完全不变。", font=font(20), fill=INK_SOFT)
    return board


def make_contact_sheet(packages: dict[str, dict[str, Image.Image]]) -> Image.Image:
    sheet = Image.new("RGB", (2200, 1400), "#e9eeeb")
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, 2199, 96), fill=INK_DEEP)
    draw.text((48, 25), "B3 分层开关与重盾互斥状态", font=font(34, bold=True), fill=PAPER)
    draw.text((1680, 34), "all Candidate / no handoff", font=font(20), fill=GOLD)

    labels = ("底板", "天气旧损", "墙挂重盾", "空挂点", "前景遮挡 + fade", "T2/S1 可读性")
    draw.text((43, 110), "候选", font=font(18, bold=True), fill=INK_SOFT)
    for index, label in enumerate(labels):
        draw.text((130 + index * 338, 110), label, font=font(18, bold=True), fill=INK_SOFT)

    row_y = (150, 555, 960)
    for row, candidate in enumerate(CANDIDATES):
        y = row_y[row]
        draw.rectangle((30, y, 2168, y + 370), fill="#f7f8f4", outline="#aab6b5", width=2)
        draw.rectangle((42, y + 16, 107, y + 350), fill={"A": TEAL, "B": GOLD, "C": RED_BRIGHT}[candidate.code])
        draw.text((59, y + 36), f"{candidate.code}", font=font(30, bold=True), fill=INK_DEEP)
        draw.text((50, y + 90), "12x9", font=font(14, bold=True), fill=INK_DEEP)
        draw.text((48, y + 117), "same", font=font(14), fill=INK_DEEP)
        draw.text((46, y + 141), "coords", font=font(14), fill=INK_DEEP)

        data = packages[candidate.code]
        effective_fg = apply_occlusion_fade(data["foreground"], data["fade"])
        previews = (
            (data["base"], False),
            (data["weather"], True),
            (data["shield_wall"], True),
            (data["shield_empty"], True),
            (effective_fg, True),
            (data["readability"], False),
        )
        for column, (preview, alpha_layer) in enumerate(previews):
            x0 = 126 + column * 338
            labeled_thumbnail(sheet, preview, (x0, y + 30, x0 + 316, y + 264), labels[column], alpha_layer=alpha_layer)
        draw.text((130, y + 291), "z: base 0 | weather 20 | shield state 30 (exclusive) | units/UI program-owned | foreground 80", font=font(16), fill=INK_SOFT)
        draw.text((130, y + 323), "遮挡碰撞语义: none  |  入格部分只读 soft fade  |  重盾状态不烘进底板", font=font(16), fill=INK_SOFT)
    return sheet


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def layer_file(candidate: Candidate, layer: str) -> str:
    names = {
        "base": "base_opaque",
        "foreground": "foreground_occlusion_rgba",
        "fade": "occlusion_fade_mask",
        "shield_wall": "shield_wall_hung_rgba",
        "shield_empty": "shield_acquired_empty_mount_rgba",
        "weather": "weather_damage_rgba",
        "readability": "T2S1_readability_composite",
    }
    return f"MAP_{candidate.code}_{names[layer]}_1280x720.png"


def save_packages(packages: dict[str, dict[str, Image.Image]]) -> None:
    for candidate in CANDIDATES:
        data = packages[candidate.code]
        for key in ("base", "foreground", "fade", "shield_wall", "shield_empty", "weather", "readability"):
            data[key].save(OUT / layer_file(candidate, key), optimize=True)

    make_direction_board(packages).save(OUT / "TACTICAL_MAP_B3_direction_board_2400x1600.png", optimize=True)
    make_contact_sheet(packages).save(OUT / "TACTICAL_MAP_B3_layer_contact_sheet_2200x1400.png", optimize=True)
    make_geometry_overlay(center_dots=True).save(
        OUT / "TACTICAL_MAP_B3_geometry_alignment_overlay_1280x720.png", optimize=True
    )


def alpha_max_in_cell(alpha: Image.Image, x: int, y: int) -> int:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(mask).polygon(cell_polygon(x, y), fill=255)
    return ImageChops.multiply(alpha, mask).getextrema()[1]


def write_candidate_spec() -> None:
    rows = []
    for candidate in CANDIDATES:
        rows.append({
            "candidate_id": candidate.stable_id,
            "map_slot": MAP_SLOT,
            "candidate_code": f"MAP-{candidate.code}",
            "title": candidate.title,
            "scene_identity": candidate.identity,
            "material_language": candidate.material,
            "lighting": candidate.lighting,
            "environment_density": candidate.density,
            "occlusion_organization": candidate.occlusion,
            "tactical_strength": candidate.strength,
            "risk": candidate.risk,
            "stable_state": STABLE_STATE,
            "profile_id": PROFILE_ID,
            "geometry_signature": GEOMETRY_SIGNATURE,
            "board": "12x9 / 108 cells / NW origin",
            "blocked_cell_topology": "none",
            "lifecycle": "Candidate",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "user_decision_required": "true",
        })
    fields = list(rows[0].keys())
    write_tsv(OUT / "candidate-spec.tsv", fields, rows)


def write_layer_spec() -> None:
    rows: list[dict[str, object]] = []
    layer_data = (
        ("base", 0, "opaque RGB", "always", "environment_ground", "art", "none"),
        ("weather", 20, "straight RGBA", "optional", "atmosphere_only", "art", "none"),
        ("shield_wall", 30, "straight RGBA", "shield_state=wall_hung", "interactive_anchor_visual", "art_state", "none"),
        ("shield_empty", 30, "straight RGBA", "shield_state=acquired", "interactive_anchor_visual", "art_state", "none"),
        ("foreground", 80, "straight RGBA + paired L mask", "optional_depth", "foreground_occlusion", "art", "none"),
        ("fade", 81, "L mask", "paired_with_foreground", "soft_fade_control", "art", "none"),
        ("readability", 900, "opaque RGB", "review_only", "joint_review_evidence", "review", "none"),
    )
    for candidate in CANDIDATES:
        for key, z_order, alpha, state, purpose, owner, collision in layer_data:
            rows.append({
                "candidate_id": candidate.stable_id,
                "layer_id": f"{candidate.stable_id}_{key.upper()}",
                "layer_kind": key,
                "filename": layer_file(candidate, key),
                "z_order_reference": z_order,
                "alpha_mode": alpha,
                "canvas": "1280x720",
                "anchor": "screen_origin=(0,0)",
                "pivot": "top_left=(0,0)",
                "state_condition": state,
                "mutual_exclusion_group": "shield_state" if key in ("shield_wall", "shield_empty") else "none",
                "collision_semantic": collision,
                "visual_owner": owner,
                "program_owned_not_baked": "grid;safe_line;impact_zone;intent;menu;unit_state;hotspot_icon",
                "geometry_signature": GEOMETRY_SIGNATURE,
                "lifecycle": "Candidate",
                "runtime_allowed": "false",
                "runtime_handoff": "none",
            })
    fields = list(rows[0].keys())
    write_tsv(OUT / "map-layer-spec.tsv", fields, rows)


def write_cell_audit(packages: dict[str, dict[str, Image.Image]]) -> None:
    rows: list[dict[str, object]] = []
    for y in range(BOARD_ROWS):
        for x in range(BOARD_COLS):
            cx, cy = cell_center(x, y)
            polygon = ";".join(f"{px},{py}" for px, py in cell_polygon(x, y))
            row: dict[str, object] = {
                "x": x,
                "y": y,
                "center_x": cx,
                "center_y": cy,
                "polygon": polygon,
                "zone": "north_safety" if y <= 1 else ("south_impact" if y >= 6 else "central_maneuver"),
                "north_safety_line": str(y <= 1).lower(),
                "shield_hotspot": str((x, y) == HOTSPOT).lower(),
                "impact_affected": str(5 <= x <= 7 and 0 <= y <= 5).lower(),
                "gz_occupancy": str(5 <= x <= 6 and 3 <= y <= 4).lower(),
                "breaker_occupancy": str(5 <= x <= 7 and 6 <= y <= 8).lower(),
                "blocked": "false",
                "movement_semantic": "uniform_ground",
                "collision_semantic": "none",
            }
            for candidate in CANDIDATES:
                foreground = packages[candidate.code]["foreground"]
                fade = packages[candidate.code]["fade"]
                effective = apply_occlusion_fade(foreground, fade)
                row[f"map_{candidate.code.lower()}_raw_occlusion_alpha_max"] = alpha_max_in_cell(
                    foreground.getchannel("A"), x, y
                )
                row[f"map_{candidate.code.lower()}_effective_occlusion_alpha_max"] = alpha_max_in_cell(
                    effective.getchannel("A"), x, y
                )
            rows.append(row)
    fields = list(rows[0].keys())
    write_tsv(OUT / "cell-visual-audit.tsv", fields, rows)


def write_source_receipt() -> None:
    rows = []
    evidence_notes = {
        "GZ_C_scale_evidence": "A1-C approved direction; review scale/occlusion only; no Sprite Master or Runtime handoff",
        "BREAKER_B_scale_evidence": "B1-B silhouette approved; B1 sample does not yet contain approved X surface language; review only",
        "shield_A_wall_evidence": "B2-A silhouette approved; sample does not yet contain approved F(D70/P30) surface language; review only",
    }
    for path, ref, blob, sha, role in SOURCE_LOCKS:
        rows.append({
            "source_path": path,
            "frozen_ref": ref,
            "git_blob": blob,
            "sha256": sha,
            "role": role,
            "validation": "PASS_exact_blob_and_sha256",
            "use_boundary": evidence_notes.get(role, "authority_or_contract_read_only"),
            "runtime_source": "false",
        })
    fields = list(rows[0].keys())
    write_tsv(OUT / "source-validation-receipt.tsv", fields, rows)


def write_decision_card() -> None:
    text = f"""# C01E02 G1.5-B3 用户裁决卡

> Lifecycle: `Candidate`
>
> `runtime_allowed=false` / `runtime_handoff=none`
>
> 稳定态：`{STABLE_STATE}` / `{PROFILE_ID}`
>
> 几何签名：`{GEOMETRY_SIGNATURE}`

## 1. 地图主方向

- `MAP-A 旧会展轨道开阔型`：战术读法最强，场景叙事最克制。
- `MAP-B 馆墙防灾广场型`：万机馆、重盾来源与北侧保护最清楚。
- `MAP-C 雨夜混合型`：气氛和章节峰值最强，需最严格控噪。

请选择 `MAP-A / MAP-B / MAP-C`，或指定不改几何的窄修改。

## 2. 遮挡方式

- `棋盘外硬遮挡`
- `棋盘外硬遮挡 + 格内软淡出`

请确认纵深组织不影响操作；所有遮挡的 `collision_semantic=none`。

## 3. 无说明文字的功能读法

请确认是否仍能指出：

1. 北侧保护方向；
2. 南侧承冲区；
3. 西北重盾热点与取盾后的空挂点；
4. 馆守 Z 2×2、BREAKER 3×3、冲撞带与 108 格操作边界。

请回复 `通过`，或指出哪一项需窄修改。

## 停止门

三项都获得明确裁决前，不开始 B4，不向主程序交接任何地图层。
"""
    (OUT / "user-decision-card.md").write_text(text, encoding="utf-8")


def write_completion_report() -> None:
    text = f"""# C01E02 G1.5-B3 完成报告

## 结果

- 交付 `MAP-A / MAP-B / MAP-C` 三组严格同坐标、同 T2/S1 状态的地图分层候选。
- 每组包含不烘入程序信息的环境底板、独立天气旧损、前景遮挡/软淡出、墙挂重盾/空挂点互斥态与 T2/S1 可读性合成。
- 共享几何为 `12x9 / 108 cells`，签名 `{GEOMETRY_SIGNATURE}`。
- 当前 profile 不包含 blocked-cell 拓扑；108 格均登记为 `uniform_ground / collision_semantic=none`。

## 证据边界

- 馆守 Z A1-C、BREAKER B1-B/X、退役重盾 B2-A/F 都只是获批派生方向，没有 Sprite Master 或 Runtime handoff。
- B1-B 比例样张尚未真正绘入 X 异质/生体装甲；B2-A 样张也尚未真正绘入 F(D70/P30)。
- 上述样张仅出现在可读性审查合成图，未烘入底板、遮挡或天气层。

## 生命周期

- 全部产物：`Candidate`
- `runtime_allowed=false`
- `runtime_handoff=none`
- 未写入 Godot，未改 Canon/Runtime/玩法/坐标/footprint/CP2，未开始 B4/C1/D1/LibTV/Cut-in/视频。

## 生成侧自检

- 冻结来源：34 项 git blob + SHA-256 逐项精确匹配。
- 合同提交：`{CONTRACT_COMMIT}`。
- Demo fingerprint：`{CONTENT_FINGERPRINT}`。
- 交付后仍需由用户完成三项独立裁决；未获批前不解锁 B4。
"""
    (OUT / "completion-report.md").write_text(text, encoding="utf-8")


def write_manifest() -> None:
    files = sorted(
        path for path in OUT.iterdir()
        if path.is_file() and path.name not in {"asset-manifest.tsv", "delivery-hashes.sha256", "BLOCKED.md"}
        and path.name != ".DS_Store"
        and path.suffix != ".pyc"
    )
    rows = []
    for path in files:
        media = "image/png" if path.suffix == ".png" else (
            "text/tab-separated-values" if path.suffix == ".tsv" else (
                "text/markdown" if path.suffix == ".md" else "text/x-python"
            )
        )
        dimensions = ""
        channels = ""
        if path.suffix == ".png":
            with Image.open(path) as image:
                dimensions = f"{image.width}x{image.height}"
                channels = image.mode
        rows.append({
            "asset_id": path.stem,
            "relative_path": path.name,
            "media_type": media,
            "dimensions": dimensions,
            "channels": channels,
            "lifecycle": "Candidate",
            "canon_level": "Working_source_bounded_candidate_output",
            "scope": "C01E02_G1.5_B3_only",
            "geometry_signature": GEOMETRY_SIGNATURE if path.suffix in (".png", ".tsv") else "n/a",
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "sha256": sha256_file(path),
        })
    fields = list(rows[0].keys())
    write_tsv(OUT / "asset-manifest.tsv", fields, rows)


def write_hashes() -> None:
    files = sorted(
        path for path in OUT.iterdir()
        if path.is_file() and path.name not in {"delivery-hashes.sha256", "BLOCKED.md"}
        and path.name != ".DS_Store" and path.suffix != ".pyc"
    )
    lines = [f"{sha256_file(path)}  {path.name}" for path in files]
    (OUT / "delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_packages() -> dict[str, dict[str, Image.Image]]:
    packages: dict[str, dict[str, Image.Image]] = {}
    for candidate in CANDIDATES:
        base = make_base(candidate)
        weather = make_weather_damage(candidate)
        shield_wall = make_shield_state(candidate, empty=False)
        shield_empty = make_shield_state(candidate, empty=True)
        foreground, fade = make_foreground(candidate)
        readability = make_readability_composite(candidate, base, weather, shield_wall, foreground, fade)
        packages[candidate.code] = {
            "base": base,
            "weather": weather,
            "shield_wall": shield_wall,
            "shield_empty": shield_empty,
            "foreground": foreground,
            "fade": fade,
            "readability": readability,
        }
    return packages


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    validate_sources()
    packages = build_packages()
    save_packages(packages)
    write_candidate_spec()
    write_layer_spec()
    write_cell_audit(packages)
    write_source_receipt()
    write_decision_card()
    write_completion_report()
    write_manifest()
    write_hashes()
    print(f"Generated B3 package: {OUT}")
    print(f"Geometry signature: {GEOMETRY_SIGNATURE}")


if __name__ == "__main__":
    main()
