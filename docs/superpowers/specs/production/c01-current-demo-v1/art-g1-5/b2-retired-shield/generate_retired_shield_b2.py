#!/usr/bin/env python3
"""Generate C01E02 G1.5-B2 retired-shield Candidate decision assets."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[6]

CONTRACT_COMMIT = "8f709de1c40132cf9c6a8b8bc918b1638a310cb0"
SNAPSHOT_REF = "fe7a0764d11f5ac5f9d11accb7398df664132b0b"
CONTENT_FINGERPRINT = "944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94"

P00 = "docs/superpowers/specs/production/c01-current-demo-v1/00-demo-source-authorization.md"
P01 = "docs/superpowers/specs/production/c01-current-demo-v1/01-source-lock.tsv"
P02 = "docs/superpowers/specs/production/c01-current-demo-v1/02-e02-s01-s07-beat-runtime-map.tsv"
P04 = "docs/superpowers/specs/production/c01-current-demo-v1/04-e02-previs-v0.1.md"
P05 = "docs/superpowers/specs/production/c01-current-demo-v1/05-e02-asset-call-matrix.tsv"
P06 = "docs/superpowers/specs/production/c01-current-demo-v1/06-e02-state-checkpoint-contract.tsv"
P07 = "docs/superpowers/specs/production/c01-current-demo-v1/07-legacy-denylist.tsv"
P08 = "docs/superpowers/specs/production/c01-current-demo-v1/08-g1-user-decision-card.md"
P09 = "docs/superpowers/specs/production/c01-current-demo-v1/09-frozen-source-snapshot.tsv"
P09B = "docs/superpowers/specs/production/c01-current-demo-v1/09b-frozen-visual-snapshot.tsv"
P10 = "docs/superpowers/specs/production/c01-current-demo-v1/10-cross-session-coordination.md"
P13 = "docs/superpowers/specs/production/c01-current-demo-v1/13-demo-build-contract.json"
P14 = "docs/superpowers/specs/production/c01-current-demo-v1/14-g1-joint-alignment-rework.md"
P15 = "docs/superpowers/specs/production/c01-current-demo-v1/15-g1-5-representative-art-pilot.md"
A1_RECEIPT = "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv"
P16 = "docs/superpowers/specs/production/c01-current-demo-v1/16-g1-5-b1-breaker-art-objective.md"
B1_RECEIPT = "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv"
B1_REVIEW = "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/g15-b1-readonly-review.md"
TASK_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/17-g1-5-b2-retired-shield-art-objective.md"
AUTHORITY_PATH = "docs/superpowers/specs/data/canon/authority_manifest.tsv"
ENTITIES_PATH = "docs/superpowers/specs/data/canon/entities.tsv"
SCENES_PATH = "docs/superpowers/specs/data/canon/scenes.tsv"
ART_LOCKS_PATH = "docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv"
REBASE_PATH = "docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md"
OUTLINE_PATH = "docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md"
STYLE_PATH = "docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md"
STORY_PATH = "docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/story/C01E02-纯剧情Reader-v2.md"
GAMEFLOW_PATH = "docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/gameflow/C01-游戏流程解构-v1.md"
GZ_C96_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_96.png"
GZ_C128_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png"
BREAKER_B96_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_96.png"
BREAKER_B128_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png"
BREAKER_SPEC_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/candidate-spec.tsv"


# path: (git ref, expected blob, expected sha256, receipt role)
SOURCE_LOCKS = {
    P00: (CONTRACT_COMMIT, "59f394ce9610da3c38ecbcf4852c1bbc2b3dc8d8", "4b13e04b45fbc3c5d5f8c770c7a5921044cde5c9238ca91aabd571101e97e6ab", "demo_authorization"),
    P01: (CONTRACT_COMMIT, "9e4d763dc6282c5cd03ffdd814ef9319fa9028fa", "0b5edbd8a7472d6a6c0ef3ce3e70efb858d715855721f5d44a858dc82189dc2d", "source_lock"),
    P02: (CONTRACT_COMMIT, "6ac539981b4743272a47861fcadafbd300d333a2", "cb7c74b80af20f339ecea63b1cb11e13162abb1ef257bbf575f79a2e28b34584", "beat_runtime_map"),
    P04: (CONTRACT_COMMIT, "339f72163af25b37a2fd1415e98e704f5e196183", "ca601618c484250c2db5bf6677cb122715476e08561e8229f4fa5f8881192640", "previs_contract"),
    P05: (CONTRACT_COMMIT, "1ec11b928c033050ceee11290027c970fd0b4831", "d4b1db2ab9c93129329ae86860e25e66a42f992593ed8bd1d9d1dc480e23f267", "asset_slot_matrix"),
    P06: (CONTRACT_COMMIT, "eaf89203798d7274201a2e259ecb0154c4afd16f", "c1450b64d941b9ee513d3a0800b712eac522a726217c759e07a773813b333bbf", "checkpoint_contract"),
    P07: (CONTRACT_COMMIT, "ea2930809ceaa302c0758cb92057e6f27d9a7884", "53eac4ef1b0c4b9a8d173c8392daa58510a31b4bda3290fd0be9942e61a5c920", "legacy_denylist"),
    P08: (CONTRACT_COMMIT, "6bc6f9f539dba2bc831319d6cadbb5229a86fc2c", "52d6486d17f81b9914231f402f726106b2fa8cf67264650b15c2e0db5fe2e36b", "g1_decision_contract"),
    P09: (CONTRACT_COMMIT, "288b87d11fc8333212b1a1559a02380233a29a6b", "5d37ad8c5639ae41f01f856097656caa378598c13ce3278d17876803412808d4", "frozen_source_manifest"),
    P09B: (CONTRACT_COMMIT, "108b101aeb13dce0b6a15861fab970dea4d4c763", "4eec352ef11b7f6706559c2d7f3285136dba6781e4892066718696795dd89713", "frozen_visual_manifest"),
    P10: (CONTRACT_COMMIT, "2648869284ff890a09753ed7bd0ee85a29e16fbb", "2440f94bc880e89990d9825b51bcb7d476b106db8a4ffe1ae740dccff063d82d", "cross_session_boundary"),
    P13: (CONTRACT_COMMIT, "93d5727b25d8c397f25fa355d88e7ed1edf9e362", "ff76cba762dfb7458cb1a33784ccca766f549ce929d9d04f8b2ebc24c128f0b7", "demo_build_contract"),
    P14: (CONTRACT_COMMIT, "13d6b3abd90365b2ff33ae6cc2050429cd763081", "b2fc581490e3314608dbd0da683dadbac763a61d6f7775fd0c30797f2c46fbd6", "joint_alignment_contract"),
    P15: (CONTRACT_COMMIT, "9fa5548a4ce81f935a86ba1f3ea322146a00e750", "844e9d15b8be1575f33b0b06992044a0cc7338284d27747802bce88eaae84b6f", "g15_parent_contract"),
    A1_RECEIPT: (CONTRACT_COMMIT, "3fecd3ea5bef592611bf0dbd9ce920b60c26d57f", "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee", "guardian_z_C_approval"),
    P16: (CONTRACT_COMMIT, "f7647acbd306d6e5abe20c4a03f94e330a89ad10", "b9e858adce3b3bd8184c979e6702f2dec97c7cd7735f9c6e2f062a0f4d5dcc12", "b1_objective"),
    B1_RECEIPT: (CONTRACT_COMMIT, "4004e1db13e96d54a48241bb5cc03233f2a95540", "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920", "b1_user_approval"),
    B1_REVIEW: (CONTRACT_COMMIT, "1fb367bef75b123ccc9447a6c79460e29f6655c3", "285c16dfae9eb205c5ceb0c001ab47035bcb6d31a6c692b2a6bd6864db18c20f", "b1_producer_review"),
    TASK_PATH: (CONTRACT_COMMIT, "dbd893e0463b0684244335f181e1a20eb8a8f015", "83ec0b8041a934290561b19ab08b6d2d7407ae363ff74ab5326fe30cd5ff4147", "unique_B2_objective"),
    AUTHORITY_PATH: (CONTRACT_COMMIT, "fdb2057b833f4dfa0ad49a1229590c515d0e1a08", "d5203da48a7634c1ed977e5a638403d03cc3797980342747c83cfbb39c24969a", "machine_authority_manifest"),
    ENTITIES_PATH: (CONTRACT_COMMIT, "5d84ad9c4a3d82dac7015248261e22fe752bbd1c", "5c296a4f181257b1d8cfa05dc704339b70d38b6fd9f7a23fbb03ca920feb7b95", "working_entity_identities"),
    SCENES_PATH: (CONTRACT_COMMIT, "9724d7b814368f0bf2279430ad40797278c822ce", "66addddc57b2a0827008c5b8e32e9aa0155ca7627e6f1a7d109432b0bfbac434", "working_scene_identity"),
    ART_LOCKS_PATH: (CONTRACT_COMMIT, "d568385869482a51e20ebb158fab5a6bb63529c7", "b680eb94d464a3b9e1f93a31f6a4e018d8958160dd0a9e774058bdcf5c7607eb", "art_lock_table"),
    REBASE_PATH: (CONTRACT_COMMIT, "e4241dea1d4c10093e3867fa34f12c7010640e27", "e1ef7f96343433b589e3f1134dd4beb43dd773a922764a38fc47e43151995756", "working_canon_rebase"),
    OUTLINE_PATH: (CONTRACT_COMMIT, "b91c05116e8d102652fe3d582a5dc6c64eb11276", "083b4678567f6d7e664939bc0e5227063765308a2f71b2be71168cb1215162ab", "C01_story_source"),
    GZ_C96_PATH: (CONTRACT_COMMIT, "113fa85ba8542bcd0ffbda7e94481c0a4648a048", "82694df3f5f8f2c78bbea55cc5d982ef93a0f1a89f6eb293313933353f984a97", "approved_GZ_C_scale_anchor_96"),
    GZ_C128_PATH: (CONTRACT_COMMIT, "a5863aa4f8913b211cd4479c1d5cd895396e17d3", "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e", "approved_GZ_C_scale_anchor_128"),
    BREAKER_B96_PATH: (CONTRACT_COMMIT, "a0ef379218afd2763ee9f5a4f943b4bcc9c5d442", "699f2f45ecc3371a87dd88e200851c20b5f0b750cfb1cb8ca6446d85ac872876", "approved_BREAKER_B_scale_anchor_96"),
    BREAKER_B128_PATH: (CONTRACT_COMMIT, "eec78e45a5d93e6e6e9eadfa9bcbdd41a0f6d678", "e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4", "approved_BREAKER_B_scale_anchor_128"),
    BREAKER_SPEC_PATH: (CONTRACT_COMMIT, "ab500cc25c5986703559cf8455763b25b80ee617", "fb15c3fb39f5d51d9eba1f5248c136b2f7f85d005983e8f43f35e020793b8b8c", "approved_BREAKER_B_technical_spec"),
    STYLE_PATH: (SNAPSHOT_REF, "ef7a08099fd2f7fb164df1334b5416ba11d0a603", "ec061505dc395c96136e9415985706ecf6c99c564e68c0c5686968581f40b653", "frozen_A_art_language"),
    STORY_PATH: (SNAPSHOT_REF, "2e0a52e14bec4f91b10c8703ee60f627afe15be9", "dd07412d84e8b21918a8369a312b0125fdd452b74d229602c8dde1922b8237b1", "frozen_candidate_story_E02"),
    GAMEFLOW_PATH: (SNAPSHOT_REF, "d776ff397c8ba45467e0c08a24a1f6ff019e4817", "284771d905e0283b32e33c436e9a9c47a5578b1a7bbed6927ffb4fea7b14312b", "frozen_candidate_gameflow"),
}

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

INK = "#172730"
INK_DEEP = "#081217"
PAPER = "#edf1f1"
PAPER_LIGHT = "#fbfbf8"
MUTED = "#718087"
GRID = "#8d9ca2"
STEEL_DARK = "#26343a"
STEEL = "#52646a"
STEEL_LIGHT = "#73858a"
PATCH = "#50665d"
MOUNT = "#8a7a58"
OLD_SCORCH = "#27211e"
OLD_RUST = "#785446"
RED = "#d13a32"
RED_BRIGHT = "#ff6750"
ORANGE = "#f39b47"
GOLD = "#d5a43b"
TEAL = "#4b9594"
BLUE = "#315f83"
WHITE = "#ffffff"


@dataclass(frozen=True)
class Candidate:
    code: str
    stable_id: str
    title: str
    motif: str
    strength: str
    risk: str
    silhouette_note: str
    mount_note: str
    action_note: str


CANDIDATES = (
    Candidate(
        "A",
        "CAND_RETIRED_SHIELD_B2_TOWER_V1",
        "高窄塔盾型",
        "纵向主脊把重量压到地面，墙挂与正面完整格挡最直接。",
        "馆内展品身份、两层楼高度和顶盾推进最清楚。",
        "需避免骑士盾、人物比例盾与大面积制式徽章感。",
        "上窄下收、双肩钝角；下缘可落地，不做尖锐盾尖。",
        "双上挂耳 + 中部抗摆销 + 下托座；左手从背脊横把扯下。",
        "立盾推进稳定；横拍依赖上肩钝角与整面惯性。",
    ),
    Candidate(
        "B",
        "CAND_RETIRED_SHIELD_B2_BLAST_PLATE_V1",
        "宽体防爆板型",
        "横向折流肩与中央承力脊把赤红冲击导向两侧。",
        "热分流、重物感与正面挡击最清楚。",
        "容易遮住馆守Z或读成建筑墙板，必须保留收腰与手臂窗口。",
        "宽肩、收腰、下缘双支点；右臂和头冠仍能从盾后读出。",
        "四点墙托分担宽体扭矩；背部偏左握把适配馆守Z左手。",
        "顶盾最强；横拍用宽体外角，受损后仍可双点落地。",
    ),
    Candidate(
        "C",
        "CAND_RETIRED_SHIELD_B2_OFFSET_RAM_V1",
        "偏心撞角型",
        "一侧加厚钝角形成旧盾自己的受力方向和盾拍焦点。",
        "横向盾拍、旧损伤与第四新焦痕的视觉重心最鲜明。",
        "必须保持钝厚，不得读成刀刃或馆守Z专属武器。",
        "偏心厚肩 + 弧形回收边；撞角是承力块，不开刃。",
        "上挂轨偏置补偿重心；下托座承担长期展陈重量。",
        "侧向盾拍最明确；放平时厚肩可承担归舰缓冲。",
    ),
)

OLD_SCARS = ((-0.23, -0.22), (0.24, 0.12), (-0.12, 0.29))
NEW_SCAR = (0.06, -0.02)


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
        raise RuntimeError(f"B2 requires HEAD {CONTRACT_COMMIT}, got {head}")

    source_bytes: dict[str, bytes] = {}
    for path, (ref, expected_blob, expected_sha, _) in SOURCE_LOCKS.items():
        actual_blob = subprocess.run(
            ["git", "rev-parse", f"{ref}:{path}"], cwd=ROOT, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.strip()
        data = git_bytes(ref, path)
        if actual_blob != expected_blob or sha256_bytes(data) != expected_sha:
            raise RuntimeError(f"B2 frozen source mismatch: {ref}:{path}")
        source_bytes[path] = data

    contract = json.loads(source_bytes[P13].decode("utf-8"))
    if contract.get("content_fingerprint") != CONTENT_FINGERPRINT:
        raise RuntimeError("Frozen Demo content fingerprint mismatch")
    if contract.get("d0", {}).get("outcome") != "gameplay_finisher":
        raise RuntimeError("D0 gameplay finisher contract missing")

    authority = tsv_rows(source_bytes[AUTHORITY_PATH])
    if any(row.get("record_id") == "PROP_C01CDV1_RETIRED_SHIELD" for row in authority):
        raise RuntimeError("Demo shield slot unexpectedly became a Canon entity")

    entities = tsv_rows(source_bytes[ENTITIES_PATH])
    wanji = [row for row in entities if row.get("entity_id") == "MECHA_WANJI_MOBILE_CHASSIS"]
    guardian = [row for row in entities if row.get("entity_id") == "V353U001"]
    if len(wanji) != 1 or "退役重盾" not in wanji[0].get("implementation_policy", ""):
        raise RuntimeError("Working Wanji touring equipment does not include the retired shield")
    if len(guardian) != 1 or guardian[0].get("status") != "working_current":
        raise RuntimeError("Guardian Z Working identity missing")

    scenes = tsv_rows(source_bytes[SCENES_PATH])
    e02 = [row for row in scenes if row.get("scene_id") == "V355-C01E02"]
    if len(e02) != 1 or "扯下退役重盾" not in e02[0].get("notes", ""):
        raise RuntimeError("Current E02 shield action missing")

    art_locks = source_bytes[ART_LOCKS_PATH].decode("utf-8")
    if "RETIRED_SHIELD" in art_locks or "退役重盾" in art_locks:
        raise RuntimeError("Unexpected independent retired-shield art lock")

    matrix = [row for row in tsv_rows(source_bytes[P05]) if row.get("asset_slot_id") == "PROP_C01CDV1_RETIRED_SHIELD"]
    if len(matrix) != 1:
        raise RuntimeError("Expected one retired shield Demo slot")
    if matrix[0].get("runtime_allowed_now") != "false" or "三旧焦痕" not in matrix[0].get("lifecycle_or_state", ""):
        raise RuntimeError("Retired shield slot lifecycle mismatch")

    checkpoints = [row for row in tsv_rows(source_bytes[P06]) if row.get("checkpoint_id") == "CP3"]
    if len(checkpoints) != 1 or "retired_shield_fourth_scorch=true" not in checkpoints[0].get("must_save", ""):
        raise RuntimeError("CP3 fourth scorch fact missing")

    a1 = tsv_rows(source_bytes[A1_RECEIPT])
    if len(a1) != 2 or any(row.get("selection") != "C_ACTION_FRAME" for row in a1):
        raise RuntimeError("A1-C scale approval mismatch")
    if any(row.get("runtime_allowed") != "false" for row in a1):
        raise RuntimeError("A1-C unexpectedly Runtime allowed")

    b1 = tsv_rows(source_bytes[B1_RECEIPT])
    if not b1 or any(row.get("runtime_allowed") != "false" for row in b1):
        raise RuntimeError("B1 approval receipt missing or Runtime allowed")
    first = b1[0]
    if first.get("silhouette_selection") != "B_FORELIMB_BEARER":
        raise RuntimeError("B1 silhouette decision mismatch")
    if first.get("surface_selection") != "X_ALIEN_BIO_ARMOR":
        raise RuntimeError("B1 surface decision mismatch")
    if first.get("structure_selection") != "CURRENT_THREE_CLOSED_RELATION_APPROVED":
        raise RuntimeError("B1 structure decision mismatch")

    frozen = {row["source_id"]: row for row in tsv_rows(source_bytes[P09])}
    if frozen.get("C01CDV1_STORY_E02", {}).get("sha256") != SOURCE_LOCKS[STORY_PATH][2]:
        raise RuntimeError("Frozen E02 story source receipt mismatch")
    if frozen.get("C01CDV1_GAMEFLOW_C01", {}).get("sha256") != SOURCE_LOCKS[GAMEFLOW_PATH][2]:
        raise RuntimeError("Frozen gameflow source receipt mismatch")

    story = source_bytes[STORY_PATH].decode("utf-8")
    for phrase in ("接近两层楼高", "挡过三次碎片雨", "冲击从两侧分开", "第四道焦痕"):
        if phrase not in story:
            raise RuntimeError(f"Frozen story fact missing: {phrase}")
    gameflow = source_bytes[GAMEFLOW_PATH].decode("utf-8")
    for phrase in ("扯下退役重盾", "完整挡住一次赤红冲击", "强化盾拍"):
        if phrase not in gameflow:
            raise RuntimeError(f"Frozen gameflow fact missing: {phrase}")

    outline = source_bytes[OUTLINE_PATH].decode("utf-8")
    for phrase in ("退役防卫巨机", "港口挡过三次碎片雨", "左手已经伸向破开的展墙"):
        if phrase not in outline:
            raise RuntimeError(f"Current outline fact missing: {phrase}")

    style = source_bytes[STYLE_PATH].decode("utf-8")
    for phrase in ("KINETIC_CEL", "4 至 7 个大色块", "细碎划痕"):
        if phrase not in style:
            raise RuntimeError(f"A art language fact missing: {phrase}")

    task = source_bytes[TASK_PATH].decode("utf-8")
    for phrase in (
        "墙挂冷态 -> 左手持盾冷态 -> 挡下赤红冲击的烧红态 -> 强化盾拍后的 E02 受损态",
        "三次港口碎片雨",
        "第四道新焦痕",
        "未贯穿裂纹",
        "wall_mount_center",
        "不得开始 B3",
    ):
        if phrase not in task:
            raise RuntimeError(f"B2 objective fact missing: {phrase}")
    return source_bytes


def polygon(draw: ImageDraw.ImageDraw, points, fill, *, outline=INK_DEEP, width: int = 6) -> None:
    draw.polygon(points, fill=fill, outline=outline)
    draw.line((*points, points[0]), fill=outline, width=width, joint="curve")


def wrap_text(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in value.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and draw.textbbox((0, 0), candidate, font=fnt)[2] > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def board_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    value: str,
    size: int,
    fill=INK,
    *,
    bold: bool = False,
    max_width: int | None = None,
    spacing: int = 6,
) -> int:
    fnt = font(size, bold=bold)
    lines = wrap_text(draw, value, fnt, max_width) if max_width else value.split("\n")
    x, y = xy
    line_h = size + spacing
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], *, accent=INK, fill=PAPER_LIGHT, width: int = 3) -> None:
    draw.rounded_rectangle(box, radius=4, fill=fill, outline=accent, width=width)


def shape_norm(candidate: Candidate) -> list[tuple[float, float]]:
    if candidate.code == "A":
        return [(-0.27, -0.50), (0.27, -0.50), (0.42, -0.36), (0.40, 0.31), (0.25, 0.50), (-0.25, 0.50), (-0.40, 0.31), (-0.42, -0.36)]
    if candidate.code == "B":
        return [(-0.46, -0.38), (0.46, -0.38), (0.50, -0.17), (0.41, 0.35), (0.26, 0.47), (-0.26, 0.47), (-0.41, 0.35), (-0.50, -0.17)]
    return [(-0.42, -0.43), (0.20, -0.48), (0.40, -0.35), (0.54, -0.08), (0.47, 0.24), (0.20, 0.48), (-0.37, 0.36), (-0.50, 0.08), (-0.48, -0.28)]


def shield_dimensions(candidate: Candidate, canvas: int) -> tuple[int, int]:
    if candidate.code == "A":
        return int(canvas * 0.52), int(canvas * 0.82)
    if candidate.code == "B":
        return int(canvas * 0.78), int(canvas * 0.61)
    return int(canvas * 0.72), int(canvas * 0.68)


def shape_points(candidate: Candidate, cx: float, cy: float, w: float, h: float, *, damaged: bool = False) -> list[tuple[int, int]]:
    pts = []
    for nx, ny in shape_norm(candidate):
        if damaged and nx > 0.34:
            nx -= 0.025
            ny += 0.035 if ny < 0 else -0.025
        if damaged and ny > 0.34 and nx < 0:
            ny -= 0.025
        pts.append((round(cx + nx * w), round(cy + ny * h)))
    return pts


def scaled_points(points: list[tuple[int, int]], cx: float, cy: float, factor: float) -> list[tuple[int, int]]:
    return [(round(cx + (x - cx) * factor), round(cy + (y - cy) * factor)) for x, y in points]


def dashed_line(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int], fill, width: int = 3, dash: int = 12) -> None:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    length = max(1.0, (dx * dx + dy * dy) ** 0.5)
    steps = max(1, int(length / dash))
    for index in range(0, steps, 2):
        t0 = index / steps
        t1 = min(1.0, (index + 1) / steps)
        draw.line((ax + dx * t0, ay + dy * t0, ax + dx * t1, ay + dy * t1), fill=fill, width=width)


def draw_mount(layer: Image.Image, candidate: Candidate, cx: int, cy: int, w: int, h: int) -> None:
    draw = ImageDraw.Draw(layer)
    rail_y = round(cy - h * 0.48)
    draw.rounded_rectangle((cx - w * 0.44, rail_y - 18, cx + w * 0.44, rail_y + 16), radius=8, fill=MOUNT, outline=INK_DEEP, width=5)
    for offset in (-0.24, 0.24):
        x = round(cx + w * offset)
        draw.rounded_rectangle((x - 14, rail_y + 2, x + 14, rail_y + 82), radius=6, fill="#655b47", outline=INK_DEEP, width=4)
    draw.rounded_rectangle((cx - 36, cy + h * 0.40, cx + 36, cy + h * 0.49), radius=6, fill=MOUNT, outline=INK_DEEP, width=5)


def draw_scars(draw: ImageDraw.ImageDraw, cx: int, cy: int, w: int, h: int, *, include_new: bool, hot: bool) -> None:
    for index, (nx, ny) in enumerate(OLD_SCARS):
        x = cx + nx * w
        y = cy + ny * h
        radius = max(10, int(min(w, h) * (0.055 + index * 0.006)))
        draw.ellipse((x - radius, y - radius * 0.72, x + radius, y + radius * 0.72), fill=OLD_SCORCH, outline=OLD_RUST, width=max(3, radius // 5))
        draw.arc((x - radius * 1.35, y - radius, x + radius * 1.35, y + radius), 205, 335, fill=STEEL_LIGHT, width=max(2, radius // 7))
    if include_new:
        nx, ny = NEW_SCAR
        x = cx + nx * w
        y = cy + ny * h
        radius = max(14, int(min(w, h) * 0.08))
        fill = RED_BRIGHT if hot else "#371a18"
        outline = ORANGE if hot else RED
        draw.ellipse((x - radius * 1.25, y - radius * 0.78, x + radius * 1.25, y + radius * 0.78), fill=fill, outline=outline, width=max(4, radius // 5))
        if not hot:
            for dx, dy in ((1.45, -0.25), (-1.30, 0.35), (0.25, 1.05)):
                draw.line((x, y, x + radius * dx, y + radius * dy), fill=OLD_SCORCH, width=max(3, radius // 6))


def draw_front_surface(
    layer: Image.Image,
    candidate: Candidate,
    points: list[tuple[int, int]],
    cx: int,
    cy: int,
    w: int,
    h: int,
    *,
    state: str,
    surface: str,
) -> None:
    draw = ImageDraw.Draw(layer)
    polygon(draw, points, STEEL_DARK, width=max(5, w // 70))
    inner = scaled_points(points, cx, cy, 0.88)
    polygon(draw, inner, STEEL, outline=INK, width=max(4, w // 90))

    if candidate.code == "A":
        draw.polygon(((cx - w * 0.10, cy - h * 0.40), (cx + w * 0.10, cy - h * 0.40), (cx + w * 0.13, cy + h * 0.38), (cx - w * 0.13, cy + h * 0.38)), fill=STEEL_LIGHT, outline=INK)
        draw.line((cx - w * 0.34, cy - h * 0.20, cx - w * 0.11, cy - h * 0.02), fill=INK, width=max(4, w // 90))
        draw.line((cx + w * 0.34, cy - h * 0.20, cx + w * 0.11, cy - h * 0.02), fill=INK, width=max(4, w // 90))
    elif candidate.code == "B":
        draw.polygon(((cx - w * 0.38, cy - h * 0.18), (cx + w * 0.38, cy - h * 0.18), (cx + w * 0.30, cy + h * 0.12), (cx - w * 0.30, cy + h * 0.12)), fill=STEEL_LIGHT, outline=INK)
        draw.line((cx, cy - h * 0.31, cx, cy + h * 0.34), fill=INK, width=max(4, w // 90))
        draw.line((cx - w * 0.40, cy + h * 0.20, cx - w * 0.18, cy + h * 0.05), fill=INK, width=max(4, w // 90))
        draw.line((cx + w * 0.40, cy + h * 0.20, cx + w * 0.18, cy + h * 0.05), fill=INK, width=max(4, w // 90))
    else:
        draw.polygon(((cx - w * 0.30, cy - h * 0.30), (cx + w * 0.18, cy - h * 0.34), (cx + w * 0.33, cy - h * 0.05), (cx + w * 0.16, cy + h * 0.26), (cx - w * 0.25, cy + h * 0.22)), fill=STEEL_LIGHT, outline=INK)
        draw.polygon(((cx + w * 0.31, cy - h * 0.29), (cx + w * 0.46, cy - h * 0.08), (cx + w * 0.37, cy + h * 0.20), (cx + w * 0.22, cy + h * 0.12)), fill="#44575b", outline=INK)

    if surface == "defense":
        for offset in (-0.30, 0.30):
            x = cx + w * offset
            draw.line((x, cy - h * 0.25, x, cy + h * 0.25), fill="#93a1a1", width=max(5, w // 80))
        for offset in (-0.28, 0, 0.28):
            draw.ellipse((cx + w * offset - 5, cy + h * 0.34 - 5, cx + w * offset + 5, cy + h * 0.34 + 5), fill=MOUNT, outline=INK)
    elif surface == "port":
        patch = ((cx - w * 0.34, cy + h * 0.03), (cx - w * 0.04, cy - h * 0.02), (cx + w * 0.02, cy + h * 0.26), (cx - w * 0.29, cy + h * 0.31))
        draw.polygon(patch, fill=PATCH, outline=INK)
        dashed_line(draw, (round(cx - w * 0.31), round(cy + h * 0.05)), (round(cx - w * 0.06), round(cy + h * 0.00)), "#b59666", max(3, w // 130), 14)
        draw.line((cx + w * 0.20, cy - h * 0.30, cx + w * 0.35, cy - h * 0.12), fill="#8a6b52", width=max(5, w // 90))

    draw_scars(draw, cx, cy, w, h, include_new=state in {"hot", "damaged"}, hot=state == "hot")

    if state == "damaged":
        crack_color = "#30201d"
        x0 = cx + w * 0.34
        y0 = cy + h * 0.22
        draw.line((x0, y0, x0 - w * 0.08, y0 - h * 0.05, x0 - w * 0.04, y0 - h * 0.12), fill=crack_color, width=max(4, w // 100))
        draw.line((x0 - w * 0.08, y0 - h * 0.05, x0 - w * 0.15, y0 - h * 0.02), fill=crack_color, width=max(3, w // 120))
        draw.polygon(((cx + w * 0.36, cy + h * 0.35), (cx + w * 0.45, cy + h * 0.28), (cx + w * 0.40, cy + h * 0.40)), fill=STEEL_DARK, outline=INK_DEEP)

    if state == "hot":
        heat = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        hd = ImageDraw.Draw(heat)
        hx = cx + NEW_SCAR[0] * w
        hy = cy + NEW_SCAR[1] * h
        for radius, color in ((0.34, (181, 34, 28, 52)), (0.23, (224, 53, 36, 76)), (0.12, (255, 111, 55, 108))):
            rx = w * radius
            ry = h * radius * 0.68
            hd.ellipse((hx - rx, hy - ry, hx + rx, hy + ry), fill=color)
        hd.line((hx, hy, cx - w * 0.43, cy - h * 0.02), fill=(255, 77, 54, 155), width=max(10, w // 35))
        hd.line((hx, hy, cx + w * 0.43, cy - h * 0.02), fill=(255, 77, 54, 155), width=max(10, w // 35))
        mask = Image.new("L", layer.size, 0)
        ImageDraw.Draw(mask).polygon(points, fill=255)
        heat.putalpha(ImageChops.multiply(heat.getchannel("A"), mask))
        layer.alpha_composite(heat)


def draw_back_surface(layer: Image.Image, candidate: Candidate, points: list[tuple[int, int]], cx: int, cy: int, w: int, h: int) -> None:
    draw = ImageDraw.Draw(layer)
    polygon(draw, points, STEEL_DARK, width=max(5, w // 70))
    inner = scaled_points(points, cx, cy, 0.84)
    polygon(draw, inner, "#34444a", outline=INK, width=max(4, w // 90))
    rib = max(14, w // 28)
    draw.line((cx - w * 0.27, cy - h * 0.30, cx + w * 0.26, cy + h * 0.30), fill=STEEL_LIGHT, width=rib)
    draw.line((cx + w * 0.27, cy - h * 0.30, cx - w * 0.26, cy + h * 0.30), fill=STEEL_LIGHT, width=rib)
    draw.line((cx, cy - h * 0.36, cx, cy + h * 0.37), fill=MOUNT, width=max(12, w // 35))
    grip_x = cx + (w * 0.12 if candidate.code != "C" else w * 0.03)
    draw.rounded_rectangle((grip_x - w * 0.05, cy - h * 0.12, grip_x + w * 0.05, cy + h * 0.16), radius=max(5, w // 50), fill=INK_DEEP, outline=MOUNT, width=max(4, w // 90))
    for xoff in (-0.22, 0.22):
        x = cx + w * xoff
        draw.rounded_rectangle((x - w * 0.04, cy - h * 0.43, x + w * 0.04, cy - h * 0.34), radius=5, fill=MOUNT, outline=INK_DEEP, width=max(3, w // 120))


def draw_side_surface(layer: Image.Image, candidate: Candidate, cx: int, cy: int, w: int, h: int) -> None:
    draw = ImageDraw.Draw(layer)
    thickness = w * (0.17 if candidate.code != "C" else 0.23)
    left = cx - thickness * 0.52
    right = cx + thickness * 0.52
    if candidate.code == "A":
        pts = ((left, cy - h * 0.47), (right, cy - h * 0.42), (right, cy + h * 0.40), (left, cy + h * 0.47))
    elif candidate.code == "B":
        pts = ((left, cy - h * 0.40), (right, cy - h * 0.35), (right, cy + h * 0.35), (left, cy + h * 0.40))
    else:
        pts = ((left, cy - h * 0.42), (right + thickness * 0.35, cy - h * 0.22), (right + thickness * 0.30, cy + h * 0.18), (left, cy + h * 0.42))
    polygon(draw, [(round(x), round(y)) for x, y in pts], STEEL, width=max(5, int(w // 75)))
    draw.line((cx, cy - h * 0.34, cx, cy + h * 0.34), fill=STEEL_LIGHT, width=max(8, int(w // 45)))
    draw.rounded_rectangle((right - 4, cy - h * 0.12, right + thickness * 0.32, cy + h * 0.14), radius=6, fill=MOUNT, outline=INK_DEEP, width=4)


def render_shield(
    candidate: Candidate,
    *,
    canvas: int = 640,
    view: str = "front",
    state: str = "cold",
    surface: str = "neutral",
    mount: bool = False,
) -> Image.Image:
    layer = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    cx, cy = canvas // 2, canvas // 2
    w, h = shield_dimensions(candidate, canvas)
    if mount:
        draw_mount(layer, candidate, cx, cy, w, h)
    if view == "side":
        draw_side_surface(layer, candidate, cx, cy, w, h)
        return layer
    points = shape_points(candidate, cx, cy, w, h, damaged=state == "damaged")
    if view == "back":
        draw_back_surface(layer, candidate, points, cx, cy, w, h)
    else:
        draw_front_surface(layer, candidate, points, cx, cy, w, h, state=state, surface=surface)
    return layer


def crop_alpha(image: Image.Image) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if not box:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    return image.crop(box)


def contain(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    crop = crop_alpha(image)
    scale = min(size[0] / crop.width, size[1] / crop.height)
    return crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)


def paste_center(canvas: Image.Image, image: Image.Image, center: tuple[int, int], max_size: tuple[int, int]) -> None:
    item = contain(image, max_size)
    canvas.alpha_composite(item, (round(center[0] - item.width / 2), round(center[1] - item.height / 2)))


def make_sample(candidate: Candidate, state: str, size: int) -> Image.Image:
    mount = state == "wall_hung"
    source = render_shield(candidate, canvas=720, state="cold", mount=mount)
    crop = crop_alpha(source)
    if state == "wall_hung":
        max_w, max_h = int(size * 0.84), int(size * 0.82)
        center_y = size // 2
    else:
        max_w, max_h = int(size * 0.80), int(size * 0.82)
        center_y = int(size * 0.50)
    scale = min(max_w / crop.width, max_h / crop.height)
    item = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = round((size - item.width) / 2)
    if state == "wall_hung":
        y = round(center_y - item.height / 2)
    else:
        bottom_target = 88 if size == 96 else 119
        y = bottom_target - item.height
    out.alpha_composite(item, (x, y))
    return out


def state_tile(candidate: Candidate, state: str, gz: Image.Image | None, size: tuple[int, int]) -> Image.Image:
    tile = Image.new("RGBA", size, (0, 0, 0, 0))
    if state == "wall_hung":
        shield = render_shield(candidate, canvas=640, mount=True)
        paste_center(tile, shield, (size[0] // 2, size[1] // 2 + 5), (int(size[0] * 0.78), int(size[1] * 0.80)))
    elif state == "held_cold":
        if gz is not None:
            gz_item = contain(gz, (int(size[0] * 0.58), int(size[1] * 0.78)))
            tile.alpha_composite(gz_item, (int(size[0] * 0.42), int(size[1] * 0.16)))
        shield = render_shield(candidate, canvas=640)
        paste_center(tile, shield, (int(size[0] * 0.38), int(size[1] * 0.55)), (int(size[0] * 0.52), int(size[1] * 0.72)))
    elif state == "hot":
        shield = render_shield(candidate, canvas=640, state="hot")
        paste_center(tile, shield, (size[0] // 2, size[1] // 2), (int(size[0] * 0.72), int(size[1] * 0.78)))
        draw = ImageDraw.Draw(tile)
        impact = (size[0] // 2, size[1] // 2)
        draw.line((impact[0] - 18, impact[1], 25, impact[1] - 42), fill=RED_BRIGHT, width=8)
        draw.line((impact[0] + 18, impact[1], size[0] - 25, impact[1] - 42), fill=RED_BRIGHT, width=8)
        draw.polygon(((25, impact[1] - 42), (42, impact[1] - 51), (39, impact[1] - 31)), fill=RED_BRIGHT)
        draw.polygon(((size[0] - 25, impact[1] - 42), (size[0] - 42, impact[1] - 51), (size[0] - 39, impact[1] - 31)), fill=RED_BRIGHT)
    else:
        shield = render_shield(candidate, canvas=640, state="damaged")
        paste_center(tile, shield, (size[0] // 2, size[1] // 2), (int(size[0] * 0.72), int(size[1] * 0.78)))
    return tile


def add_header(canvas: Image.Image, title: str, subtitle: str = "Candidate / runtime_allowed=false") -> None:
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, canvas.width, 92), fill=INK)
    board_text(draw, (30, 23), title, 28, WHITE)
    bbox = draw.textbbox((0, 0), subtitle, font=font(18))
    board_text(draw, (canvas.width - (bbox[2] - bbox[0]) - 30, 30), subtitle, 18, GOLD)


def draw_sample_pair(canvas: Image.Image, candidate: Candidate, samples: dict[tuple[str, str, int], Image.Image], origin: tuple[int, int]) -> None:
    draw = ImageDraw.Draw(canvas)
    x, y = origin
    for column, state in enumerate(("wall_hung", "held_cold")):
        label = "墙挂" if state == "wall_hung" else "持盾"
        board_text(draw, (x + column * 150 + 34, y), label, 14, MUTED, bold=True)
        for row, size in enumerate((96, 128)):
            source = samples[(candidate.code, state, size)]
            preview = source.resize((72 if size == 96 else 88, 72 if size == 96 else 88), Image.Resampling.NEAREST)
            px = x + column * 150 + 20 + (8 if size == 96 else 0)
            py = y + 25 + row * 90
            canvas.alpha_composite(preview, (px, py))
            board_text(draw, (px + 82, py + 26), str(size), 13, MUTED)


def draw_direction_board(samples: dict[tuple[str, str, int], Image.Image], gz128: Image.Image) -> Path:
    canvas = Image.new("RGBA", (2400, 1600), PAPER)
    add_header(canvas, "C01E02 G1.5-B2 | 退役重盾身份方向 + 四态连续性判断板")
    draw = ImageDraw.Draw(canvas)
    panel(draw, (20, 110, 335, 1570), accent=INK)
    board_text(draw, (42, 130), "共同锁定事实", 22, INK, bold=True)
    facts = [
        "另一台退役防卫巨机的旧装备",
        "接近两层楼高 / 墙挂实物",
        "馆守Z 18m / 左手取盾",
        "三处旧凹痕与焦痕持续存在",
        "赤红冲击由受击区向两侧分流",
        "第四道新焦痕只在挡击后出现",
        "E02 仅变形、掉漆与非贯穿表裂",
        "仍能立盾、推进和横向盾拍",
    ]
    for index, fact in enumerate(facts, 1):
        y = 182 + (index - 1) * 74
        draw.ellipse((42, y, 68, y + 26), fill=RED if index in (4, 5, 6) else INK)
        board_text(draw, (49, y + 4), str(index), 11, WHITE, bold=True)
        board_text(draw, (78, y), fact, 15, INK, max_width=225)
    board_text(draw, (42, 830), "E02 禁止提前出现", 18, RED, bold=True)
    board_text(draw, (42, 866), "贯穿裂纹 / 断成两半 / 完全碎裂\n能量护罩 / 手臂替换 / 独立机魂\n组织徽章 / 型号史 / 传奇战役", 15, RED, max_width=250, spacing=8)
    board_text(draw, (42, 1035), "表面语言本轮待选", 18, TEAL, bold=True)
    board_text(draw, (42, 1072), "D：退役防卫巨机的制式重装\nP：港防工业修补感\n或明确比例融合。候选主体先用中性大色块，不替用户锁定。", 15, INK, max_width=250, spacing=8)
    board_text(draw, (42, 1272), "父级边界", 18, GOLD, bold=True)
    board_text(draw, (42, 1308), "馆守Z A1-C：尺度与左手持盾\nBREAKER B：尺度、接触、遮挡\nB+X 尚未形成正式敌机图\n两者均不是 Godot handoff", 14, INK, max_width=250, spacing=8)

    column_x = (355, 1035, 1715)
    accents = (RED, TEAL, GOLD)
    state_names = (("wall_hung", "墙挂冷态"), ("held_cold", "左手持盾冷态"), ("hot", "赤红冲击烧红态"), ("damaged", "E02盾拍后受损态"))
    for candidate, x, accent in zip(CANDIDATES, column_x, accents):
        panel(draw, (x, 110, x + 655, 1570), accent=accent)
        board_text(draw, (x + 20, 130), f"{candidate.code} | {candidate.title}", 24, INK, bold=True)
        board_text(draw, (x + 20, 169), candidate.stable_id, 11, accent)
        front = render_shield(candidate, canvas=680)
        paste_center(canvas, front, (x + 327, 390), (540, 430))
        state_y = 615
        for idx, (state, label) in enumerate(state_names):
            sx = x + 20 + (idx % 2) * 310
            sy = state_y + (idx // 2) * 250
            panel(draw, (sx, sy, sx + 295, sy + 225), accent=GRID, fill="#f7f8f6", width=2)
            board_text(draw, (sx + 12, sy + 10), label, 14, INK, bold=True)
            tile = state_tile(candidate, state, gz128, (270, 178))
            canvas.alpha_composite(tile, (sx + 12, sy + 37))
        board_text(draw, (x + 20, 1127), "透明方向样张", 15, MUTED, bold=True)
        draw_sample_pair(canvas, candidate, samples, (x + 20, 1158))
        board_text(draw, (x + 330, 1138), "轮廓母题", 15, accent, bold=True)
        board_text(draw, (x + 330, 1170), candidate.motif, 14, INK, max_width=285)
        board_text(draw, (x + 330, 1255), "优势", 14, TEAL, bold=True)
        board_text(draw, (x + 385, 1255), candidate.strength, 14, INK, max_width=235)
        board_text(draw, (x + 330, 1330), "风险", 14, RED, bold=True)
        board_text(draw, (x + 385, 1330), candidate.risk, 14, INK, max_width=235)
        board_text(draw, (x + 330, 1435), "动作余量", 14, GOLD, bold=True)
        board_text(draw, (x + 330, 1465), candidate.action_note, 13, INK, max_width=285)

    path = OUT / "RETIRED_SHIELD_B2_direction_board_2400x1600.png"
    canvas.convert("RGB").save(path, quality=95)
    return path


def draw_candidate_sheet(candidate: Candidate, samples: dict[tuple[str, str, int], Image.Image], gz128: Image.Image) -> Path:
    canvas = Image.new("RGBA", (1800, 1200), PAPER)
    add_header(canvas, f"C01E02 G1.5-B2 | 退役重盾 {candidate.code} {candidate.title}")
    draw = ImageDraw.Draw(canvas)
    top_boxes = ((28, 116, 585, 540), (612, 116, 1169, 540), (1196, 116, 1772, 540))
    for box, title in zip(top_boxes, ("正面与三旧痕", "背面握持 / 挂点", "严格侧面 / 厚度")):
        panel(draw, box, accent=INK)
        board_text(draw, (box[0] + 18, box[1] + 14), title, 18, INK, bold=True)
    front = render_shield(candidate, canvas=680)
    back = render_shield(candidate, canvas=680, view="back")
    side = render_shield(candidate, canvas=680, view="side")
    paste_center(canvas, front, (306, 340), (480, 350))
    paste_center(canvas, back, (890, 340), (480, 350))
    paste_center(canvas, side, (1484, 340), (410, 350))
    board_text(draw, (1225, 488), "钝厚承力，不开刃", 14, RED, bold=True)

    state_names = (("wall_hung", "墙挂冷态"), ("held_cold", "左手持盾冷态"), ("hot", "赤红冲击烧红态"), ("damaged", "E02盾拍后受损态"))
    for idx, (state, label) in enumerate(state_names):
        x = 28 + idx * 436
        panel(draw, (x, 565, x + 410, 895), accent=(RED if state in {"hot", "damaged"} else GRID))
        board_text(draw, (x + 15, 580), label, 17, INK, bold=True)
        tile = state_tile(candidate, state, gz128, (380, 255))
        canvas.alpha_composite(tile, (x + 15, 620))
        if state == "wall_hung":
            board_text(draw, (x + 15, 856), "挂点 / 重心 / 左手扯下受力", 12, MUTED)
        elif state == "held_cold":
            board_text(draw, (x + 15, 856), "右臂与头冠仍可辨", 12, MUTED)
        elif state == "hot":
            board_text(draw, (x + 15, 856), "局部烧红并向两侧分流", 12, MUTED)
        else:
            board_text(draw, (x + 15, 856), "新焦痕 + 非贯穿表裂；仍可立盾", 12, MUTED)

    panel(draw, (28, 920, 560, 1172), accent=GOLD)
    board_text(draw, (48, 938), "96 / 128 px 透明原生样张", 16, INK, bold=True)
    draw_sample_pair(canvas, candidate, samples, (52, 976))
    board_text(draw, (360, 980), "pivot", 14, GOLD, bold=True)
    board_text(draw, (360, 1012), "wall_mount_center\ngrip_center\nbottom_center", 13, INK, spacing=9)
    board_text(draw, (360, 1115), "仅方向样张\n不是 Sprite Master", 12, RED, spacing=7)

    panel(draw, (585, 920, 1180, 1172), accent=RED)
    board_text(draw, (605, 938), "三旧痕与第四新焦痕", 16, INK, bold=True)
    board_text(draw, (605, 976), "旧1：左上凹痕焦边\n旧2：右中冲蚀坑\n旧3：左下旧烧蚀\n新4：中央偏上赤红冲击焦痕", 14, INK, spacing=8)
    board_text(draw, (605, 1100), "新4不得覆盖旧1–3；E02裂纹止于表层。", 13, RED, bold=True, max_width=535)

    panel(draw, (1205, 920, 1772, 1172), accent=TEAL)
    board_text(draw, (1225, 938), "轮廓 / 挂载 / 动作判断", 16, INK, bold=True)
    board_text(draw, (1225, 976), candidate.silhouette_note, 13, INK, max_width=515)
    board_text(draw, (1225, 1038), candidate.mount_note, 13, INK, max_width=515)
    board_text(draw, (1225, 1100), candidate.action_note, 13, INK, max_width=515)

    path = OUT / f"RETIRED_SHIELD_B2_candidate_{candidate.code}_four_state_sheet_1800x1200.png"
    canvas.convert("RGB").save(path, quality=95)
    return path


def draw_surface_board() -> Path:
    canvas = Image.new("RGBA", (1800, 1050), PAPER)
    add_header(canvas, "C01E02 G1.5-B2 | 退役重盾表面语言判断板")
    draw = ImageDraw.Draw(canvas)
    columns = (
        (30, "D | 退役防卫巨机制式重装", "defense", TEAL, "规则化大装甲、重复承力脊、克制的制式涂层。", "风险：过新、过整齐，像现役装备。"),
        (620, "P | 港防工业修补感", "port", GOLD, "异色补板、可读焊线、角部加固与防腐旧漆。", "风险：细节过多，Q版易乱。"),
        (1210, "F | 比例融合示例", "neutral", RED, "主结构保持制式，修补只集中在旧受击与承力区。", "可指定 D70/P30 等比例。"),
    )
    for x, title, surface, accent, note, risk in columns:
        panel(draw, (x, 120, x + 560, 1008), accent=accent)
        board_text(draw, (x + 20, 140), title, 21, INK, bold=True)
        board_text(draw, (x + 20, 184), note, 15, INK, max_width=510)
        for idx, candidate in enumerate(CANDIDATES):
            y = 300 + idx * 205
            board_text(draw, (x + 22, y - 18), f"{candidate.code} {candidate.title}", 14, accent, bold=True)
            shield_surface = surface
            shield = render_shield(candidate, canvas=620, surface=shield_surface)
            paste_center(canvas, shield, (x + 280, y + 80), (450, 165))
        board_text(draw, (x + 20, 930), risk, 14, RED if surface != "neutral" else INK, max_width=510, bold=True)
    board_text(draw, (45, 1018), "不随表面选择改变：轮廓、三旧痕坐标、第四新焦痕、墙挂/握持结构与E02非贯穿损伤上限。", 13, MUTED)
    path = OUT / "RETIRED_SHIELD_B2_surface_language_board_1800x1050.png"
    canvas.convert("RGB").save(path, quality=95)
    return path


def draw_continuity_board(gz128: Image.Image) -> Path:
    canvas = Image.new("RGBA", (2200, 1250), PAPER)
    add_header(canvas, "C01E02 G1.5-B2 | 三旧痕—第四新焦痕—烧红分流—E02受损连续性")
    draw = ImageDraw.Draw(canvas)
    headers = ("墙挂冷态", "左手持盾冷态", "赤红冲击烧红态", "E02盾拍后受损态")
    for idx, header in enumerate(headers):
        board_text(draw, (270 + idx * 455, 118), header, 18, INK, bold=True)
    board_text(draw, (24, 118), "候选", 18, INK, bold=True)
    states = ("wall_hung", "held_cold", "hot", "damaged")
    for row, candidate in enumerate(CANDIDATES):
        y = 165 + row * 310
        panel(draw, (20, y, 2180, y + 285), accent=(RED, TEAL, GOLD)[row], width=3)
        board_text(draw, (40, y + 28), candidate.code, 34, (RED, TEAL, GOLD)[row], bold=True)
        board_text(draw, (40, y + 82), candidate.title, 17, INK, bold=True, max_width=180)
        board_text(draw, (40, y + 145), "旧1/2/3\n位置不漂移", 14, MUTED, spacing=9)
        for col, state in enumerate(states):
            tile = state_tile(candidate, state, gz128, (420, 238))
            canvas.alpha_composite(tile, (220 + col * 455, y + 25))
            if state == "hot":
                board_text(draw, (250 + col * 455, y + 238), "受击中心局部热化，左右分流", 12, RED, bold=True)
            elif state == "damaged":
                board_text(draw, (250 + col * 455, y + 238), "新4留痕；裂纹未贯穿", 12, RED, bold=True)
    panel(draw, (20, 1110, 2180, 1225), accent=INK)
    board_text(draw, (42, 1128), "连续性通过条件", 16, INK, bold=True)
    board_text(draw, (220, 1128), "旧1–3始终可追踪；烧红不是整面均匀发光；新4只在赤红冲击后出现；受损边、掉漆和短表裂不穿透盾体，盾仍有双点落地与继续立盾余量。", 14, INK, max_width=1900)
    path = OUT / "RETIRED_SHIELD_B2_four_state_continuity_board_2200x1250.png"
    canvas.convert("RGB").save(path, quality=95)
    return path


def iso_center(origin: tuple[int, int], x: int, y: int, sx: int = 19, sy: int = 10) -> tuple[int, int]:
    return origin[0] + (x - y) * sx, origin[1] + (x + y) * sy


def draw_iso_cell(draw: ImageDraw.ImageDraw, center: tuple[int, int], sx: int, sy: int, fill, outline=GRID, width: int = 1) -> None:
    cx, cy = center
    draw.polygon(((cx, cy - sy), (cx + sx, cy), (cx, cy + sy), (cx - sx, cy)), fill=fill, outline=outline)
    if width > 1:
        draw.line((cx, cy - sy, cx + sx, cy, cx, cy + sy, cx - sx, cy, cx, cy - sy), fill=outline, width=width)


def draw_s07_panel(canvas: Image.Image, candidate: Candidate, box: tuple[int, int, int, int], gz128: Image.Image, breaker128: Image.Image, accent) -> None:
    draw = ImageDraw.Draw(canvas)
    panel(draw, box, accent=accent)
    x0, y0, x1, y1 = box
    board_text(draw, (x0 + 18, y0 + 16), f"{candidate.code} {candidate.title}", 18, INK, bold=True)
    board_text(draw, (x0 + 18, y0 + 50), "同一2×2 / 3×3 / 北侧安全线 / 发射轴", 12, MUTED)
    origin = (x0 + 292, y0 + 220)
    sx, sy = 22, 11
    for y in range(9):
        for x in range(12):
            fill = "#d8ece9" if y <= 1 else "#e6eaeb"
            if 5 <= x <= 6 and 3 <= y <= 4:
                fill = "#c7d7e5"
            if 5 <= x <= 7 and 6 <= y <= 8:
                fill = "#ded3d0"
            if (x, y) == (1, 2):
                fill = "#ead7a2"
            draw_iso_cell(draw, iso_center(origin, x, y, sx, sy), sx, sy, fill)
    north_a = iso_center(origin, 0, 0, sx, sy)
    north_b = iso_center(origin, 11, 0, sx, sy)
    draw.line((north_a[0] - sx, north_a[1], north_b[0] + sx, north_b[1]), fill=TEAL, width=5)
    board_text(draw, (x0 + 18, y0 + 98), "NORTH SAFE", 12, TEAL, bold=True)
    hotspot = iso_center(origin, 1, 2, sx, sy)
    draw.ellipse((hotspot[0] - 8, hotspot[1] - 8, hotspot[0] + 8, hotspot[1] + 8), fill=GOLD, outline=INK, width=2)

    gz_center = iso_center(origin, 5, 3, sx, sy)
    breaker_center = iso_center(origin, 5, 6, sx, sy)
    gz_item = contain(gz128, (74, 74))
    canvas.alpha_composite(gz_item, (gz_center[0] - 37, gz_center[1] - 63))
    shield = render_shield(candidate, canvas=600)
    shield_item = contain(shield, (54, 62))
    canvas.alpha_composite(shield_item, (gz_center[0] - 48, gz_center[1] - 52))
    breaker_item = contain(breaker128, (88, 88))
    canvas.alpha_composite(breaker_item, (breaker_center[0] - 44, breaker_center[1] - 70))

    start = (breaker_center[0], breaker_center[1] - 54)
    impact = (gz_center[0] - 25, gz_center[1] - 36)
    draw.line((*start, *impact), fill=RED, width=5)
    draw.line((*impact, impact[0] - 52, impact[1] - 22), fill=RED_BRIGHT, width=4)
    draw.line((*impact, impact[0] + 48, impact[1] - 22), fill=RED_BRIGHT, width=4)
    draw.ellipse((impact[0] - 6, impact[1] - 6, impact[0] + 6, impact[1] + 6), fill=ORANGE)

    inset = (x0 + 38, y0 + 440, x1 - 38, y0 + 690)
    panel(draw, inset, accent=GRID, fill="#f7f8f6", width=2)
    board_text(draw, (inset[0] + 14, inset[1] + 12), "屏幕尺度放大验证", 13, INK, bold=True)
    large_gz_center = (x0 + 174, y0 + 580)
    large_breaker_center = (x0 + 414, y0 + 578)
    large_gz = contain(gz128, (150, 150))
    canvas.alpha_composite(large_gz, (large_gz_center[0] - 75, large_gz_center[1] - 105))
    large_shield = contain(shield, (118, 142))
    canvas.alpha_composite(large_shield, (large_gz_center[0] - 112, large_gz_center[1] - 86))
    large_breaker = contain(breaker128, (165, 165))
    canvas.alpha_composite(large_breaker, (large_breaker_center[0] - 82, large_breaker_center[1] - 112))
    large_start = (large_breaker_center[0] - 48, large_breaker_center[1] - 62)
    large_impact = (large_gz_center[0] - 64, large_gz_center[1] - 44)
    draw.line((*large_start, *large_impact), fill=RED, width=7)
    draw.line((*large_impact, large_impact[0] - 42, large_impact[1] - 44), fill=RED_BRIGHT, width=6)
    draw.line((*large_impact, large_impact[0] - 38, large_impact[1] + 48), fill=RED_BRIGHT, width=6)
    draw.ellipse((large_impact[0] - 7, large_impact[1] - 7, large_impact[0] + 7, large_impact[1] + 7), fill=ORANGE)
    board_text(draw, (inset[0] + 12, inset[3] - 30), "左手盾前置；头冠、右肩、右前臂保留", 11, MUTED, bold=True)

    board_text(draw, (x0 + 18, y1 - 172), "遮挡复核", 14, accent, bold=True)
    board_text(draw, (x0 + 18, y1 - 142), "盾在左手前方；馆守Z头冠、右肩与右前臂仍可辨。\n盾不扩张2×2 footprint；BREAKER B仅作已批尺度/接触锚。", 13, INK, max_width=x1 - x0 - 36, spacing=8)
    board_text(draw, (x0 + 18, y1 - 74), "B1 X方向只以文字确认，本板不冒充已完成B+X正式敌机。", 12, RED, bold=True, max_width=x1 - x0 - 36)


def draw_s07_board(gz128: Image.Image, breaker128: Image.Image) -> Path:
    canvas = Image.new("RGBA", (1800, 1050), PAPER)
    add_header(canvas, "C01E02 G1.5-B2 | S07 尺度、遮挡与赤红冲击分流验证")
    boxes = ((25, 120, 585, 1005), (620, 120, 1180, 1005), (1215, 120, 1775, 1005))
    for candidate, box, accent in zip(CANDIDATES, boxes, (RED, TEAL, GOLD)):
        draw_s07_panel(canvas, candidate, box, gz128, breaker128, accent)
    path = OUT / "RETIRED_SHIELD_B2_S07_scale_occlusion_board_1800x1050.png"
    canvas.convert("RGB").save(path, quality=95)
    return path


def write_candidate_spec() -> Path:
    path = OUT / "candidate-spec.tsv"
    fields = [
        "candidate_id", "code", "silhouette_direction", "physical_origin", "world_scale", "holder",
        "wall_hotspot", "wall_state", "held_state", "hot_state", "e02_damage_state",
        "old_scar_1", "old_scar_2", "old_scar_3", "new_scar_4", "heat_split",
        "wall_mount_center_96", "wall_mount_center_128", "grip_center_96", "grip_center_128",
        "bottom_center_96", "bottom_center_128", "surface_language", "e03_e04_excluded",
        "lifecycle", "runtime_allowed",
    ]
    rows = []
    grips = {"A": ((57, 47), (76, 63)), "B": ((56, 49), (75, 65)), "C": ((54, 48), (72, 64))}
    for candidate in CANDIDATES:
        g96, g128 = grips[candidate.code]
        rows.append({
            "candidate_id": candidate.stable_id,
            "code": candidate.code,
            "silhouette_direction": candidate.title,
            "physical_origin": "retired_defense_giant_full_scale_mechanical_shield;not_guardian_z_original",
            "world_scale": "near_two_storeys;usable_by_18m_guardian_z",
            "holder": "guardian_z_left_hand;right_arm_remains_visible",
            "wall_hotspot": "c01cdv1_s06_g1_v1:(1,2);demo_profile_only;coordinate_unchanged",
            "wall_state": "wall_hung_cold;mount_and_lower_saddle_visible",
            "held_state": "left_hand_held_cold;can_stand_advance_and_bash",
            "hot_state": "localized_material_heat_from_impact_center;split_left_and_right;no_energy_field",
            "e02_damage_state": "edge_deformation;paint_loss;surface_crack_nonpenetrating;still_standable",
            "old_scar_1": "upper_left_dent_scorch;persists_all_states",
            "old_scar_2": "right_mid_erosion_dent;persists_all_states",
            "old_scar_3": "lower_left_old_burn;persists_all_states",
            "new_scar_4": "center_upper_new_red_impact_scorch;appears_after_block;does_not_erase_old_scars",
            "heat_split": "impact_center_to_both_lateral_edges;material_conduction_not_uniform_glow",
            "wall_mount_center_96": "(48,48)",
            "wall_mount_center_128": "(64,64)",
            "grip_center_96": str(g96).replace(" ", ""),
            "grip_center_128": str(g128).replace(" ", ""),
            "bottom_center_96": "(48,88)",
            "bottom_center_128": "(64,119)",
            "surface_language": "unresolved_user_decision:defense_heavy_vs_port_repair_or_ratio",
            "e03_e04_excluded": "no_penetration;no_split;no_total_break",
            "lifecycle": "candidate_direction_sample",
            "runtime_allowed": "false",
        })
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_source_receipt() -> Path:
    path = OUT / "source-validation-receipt.tsv"
    fields = ("input_id", "authority_role", "contract_commit_or_snapshot", "source_path", "expected_sha256", "actual_sha256", "validation", "runtime_allowed")
    rows = []
    for index, (source_path, (ref, _, sha, role)) in enumerate(SOURCE_LOCKS.items(), 1):
        validation = "match_from_contract_commit" if ref == CONTRACT_COMMIT else "match_from_frozen_snapshot"
        notes = []
        if source_path == TASK_PATH:
            notes.append("B2_only")
        elif source_path == B1_RECEIPT:
            notes.append("B+X+closed_relation_approved_for_derivative_only")
        elif source_path == ART_LOCKS_PATH:
            notes.append("retired_shield_art_lock=absent")
        elif source_path == AUTHORITY_PATH:
            notes.append("demo_slot_not_canon_entity")
        elif source_path == P05:
            notes.append("PROP_C01CDV1_RETIRED_SHIELD=runtime_false")
        elif source_path in (GZ_C96_PATH, GZ_C128_PATH):
            notes.append("scale_and_left_hand_relation_only")
        elif source_path in (BREAKER_B96_PATH, BREAKER_B128_PATH, BREAKER_SPEC_PATH):
            notes.append("B_scale_contact_occlusion_only;X_not_rendered")
        if notes:
            validation += ";" + ";".join(notes)
        rows.append({
            "input_id": f"B2SRC{index:02d}",
            "authority_role": role,
            "contract_commit_or_snapshot": ref,
            "source_path": source_path,
            "expected_sha256": sha,
            "actual_sha256": sha,
            "validation": validation,
            "runtime_allowed": "false",
        })
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_decision_card() -> Path:
    path = OUT / "user-decision-card.md"
    path.write_text(
        """# C01E02 G1.5-B2 退役重盾用户裁决卡

> Status: `awaiting_individual_user_decision`
>
> 本轮全部为 `Candidate / runtime_allowed=false`；不会自动进入 B3 或主程序。

## 1. 主轮廓

- `A 高窄塔盾型`
- `B 宽体防爆板型`
- `C 偏心撞角型`
- 或：选定路线但按意见修改 / 全部重做 / 仅参考

## 2. 表面语言

- `D 退役防卫巨机的制式重装`
- `P 港防工业修补感`
- 或：指定比例融合，例如 `D70/P30`

不得由本选择新增所属组织、型号史、驾驶员或传奇战役。

## 3. 四态连续性

请确认：三处旧凹痕/焦痕始终可追踪；第四道新焦痕在赤红冲击后清楚出现；烧红由受击中心向两侧分流而非整面均匀发光；E02 受损只有变形、掉漆和未贯穿表裂，盾仍能立住并继续使用，没有提前泄露 E03/E04。

未获得这三项明确回复前，本任务停止，不开始 B3 地图。
""",
        encoding="utf-8",
    )
    return path


def manifest_dimensions(path: Path, kind: str) -> str:
    if kind.startswith("png"):
        with Image.open(path) as image:
            return f"{image.width}x{image.height}"
    return kind


def write_manifest(entries: list[tuple[str, Path, str, str, str]]) -> Path:
    path = OUT / "asset-manifest.tsv"
    fields = ("asset_id", "path", "type", "dimensions_or_format", "source_ids", "parent_slot", "lifecycle", "status", "sha256", "runtime_allowed", "notes")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for asset_id, asset_path, kind, lifecycle, notes in entries:
            writer.writerow({
                "asset_id": asset_id,
                "path": asset_path.name,
                "type": kind,
                "dimensions_or_format": manifest_dimensions(asset_path, kind),
                "source_ids": "V355-C01E02_WORKING;MECHA_WANJI_MOBILE_CHASSIS_WORKING;G15_A1_C_SCALE_ONLY;G15_B1_B_CONTACT_ONLY;TASK_17",
                "parent_slot": "PROP_C01CDV1_RETIRED_SHIELD",
                "lifecycle": lifecycle,
                "status": "awaiting_individual_user_decision",
                "sha256": sha256_file(asset_path),
                "runtime_allowed": "false",
                "notes": notes,
            })
    return path


def write_completion_report(manifest_count: int, source_count: int) -> Path:
    path = OUT / "completion-report.md"
    path.write_text(
        f"""# C01E02 G1.5-B2 退役重盾交付报告

> Result: `COMPLETE / awaiting_individual_user_decision`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 已完成

- 三个受控轮廓方向：A 高窄塔盾、B 宽体防爆板、C 偏心撞角。
- 每个方向含正面、背面握持/挂点、严格侧面与四态连续条。
- 每个方向含 `wall_hung`、`held_cold` 的 96/128 px 透明方向样张。
- 三旧痕、第四新焦痕、局部烧红两侧分流与 E02 非贯穿受损均可追踪。
- S07 板仅使用馆守 Z A1-C 与 BREAKER B 的尺度/接触证据；未冒充正式 B+X 敌机。
- 表面语言单独保留 D/P/比例融合用户门，不新增组织或型号史。

## 技术状态

- 合同提交：`{CONTRACT_COMMIT}`
- 冻结指纹：`{CONTENT_FINGERPRINT}`
- 来源回执：`{source_count}` 项
- Manifest：`{manifest_count}` 项，全部 `runtime_allowed=false`
- 没有 Sprite Master、动作帧、Cut-in、视频、LibTV、Godot、Canon 或 Runtime 修改。
- 没有覆盖 A1/B1，没有开始 B3/B4/C1。

## 停止门

等待用户分别选择主轮廓、表面语言与四态连续性。未完成三项裁决前不开始 B3。
""",
        encoding="utf-8",
    )
    return path


def write_delivery_hashes() -> Path:
    path = OUT / "delivery-hashes.sha256"
    files = sorted(p for p in OUT.iterdir() if p.is_file() and p.name != path.name)
    path.write_text("".join(f"{sha256_file(item)}  {item.name}\n" for item in files), encoding="utf-8")
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = validate_sources()
    gz128 = Image.open(io.BytesIO(sources[GZ_C128_PATH])).convert("RGBA")
    breaker128 = Image.open(io.BytesIO(sources[BREAKER_B128_PATH])).convert("RGBA")

    samples: dict[tuple[str, str, int], Image.Image] = {}
    sample_paths: list[tuple[str, Path, str, str, str]] = []
    for candidate in CANDIDATES:
        for state in ("wall_hung", "held_cold"):
            for size in (96, 128):
                sample = make_sample(candidate, state, size)
                samples[(candidate.code, state, size)] = sample
                sample_path = OUT / f"RETIRED_SHIELD_B2_candidate_{candidate.code}_{state}_{size}.png"
                sample.save(sample_path)
                sample_paths.append((
                    f"{candidate.stable_id}_{state.upper()}_{size}", sample_path, "png_rgba",
                    "candidate_qprop_scale_sample",
                    f"transparent {size}px {state} direction sample;not Sprite Master",
                ))

    direction = draw_direction_board(samples, gz128)
    sheets = [draw_candidate_sheet(candidate, samples, gz128) for candidate in CANDIDATES]
    surface = draw_surface_board()
    continuity = draw_continuity_board(gz128)
    s07 = draw_s07_board(gz128, breaker128)
    candidate_spec = write_candidate_spec()
    source_receipt = write_source_receipt()
    decision_card = write_decision_card()

    entries: list[tuple[str, Path, str, str, str]] = [
        ("G15_B2_RETIRED_SHIELD_DIRECTION_BOARD", direction, "png", "candidate_direction_board", "three controlled shield silhouettes and four-state reads"),
        ("G15_B2_RETIRED_SHIELD_SURFACE_BOARD", surface, "png", "candidate_surface_decision_board", "defense heavy vs port repair vs explicit blend"),
        ("G15_B2_RETIRED_SHIELD_CONTINUITY_BOARD", continuity, "png", "candidate_state_decision_board", "old scars;new scorch;heat split;E02 nonpenetrating damage"),
        ("G15_B2_RETIRED_SHIELD_S07_SCALE_BOARD", s07, "png", "candidate_scale_occlusion_board", "GZ C and BREAKER B scale/contact evidence only;not handoff"),
    ]
    for candidate, sheet in zip(CANDIDATES, sheets):
        entries.append((f"{candidate.stable_id}_FOUR_STATE_SHEET", sheet, "png", "candidate_identity_state_sheet", "front;back;strict side;wall;held;hot;E02 damaged"))
    entries.extend(sample_paths)
    entries.extend([
        ("G15_B2_RETIRED_SHIELD_CANDIDATE_SPEC", candidate_spec, "tsv", "candidate_design_evidence", "pivots;scar continuity;state bounds;surface unresolved"),
        ("G15_B2_SOURCE_VALIDATION_RECEIPT", source_receipt, "tsv", "source_validation_evidence", f"{len(SOURCE_LOCKS)} exact frozen inputs"),
        ("G15_B2_USER_DECISION_CARD", decision_card, "md", "decision_gate", "silhouette;surface;four-state continuity required"),
        ("G15_B2_GENERATOR_SOURCE", Path(__file__), "py", "reproducible_generator", "procedural static generation;no ImageGen;no LibTV"),
    ])
    manifest = write_manifest(entries)
    report = write_completion_report(len(entries), len(SOURCE_LOCKS))
    hashes = write_delivery_hashes()

    print(f"Generated {direction.name}")
    print(f"Candidate sheets: {len(sheets)}")
    print(f"Transparent samples: {len(sample_paths)}")
    print(f"Manifest rows: {len(entries)}")
    print(f"Completion report: {report.name}")
    print(f"Delivery hashes: {hashes.name}")
    print(f"Contract commit: {CONTRACT_COMMIT}")
    print(f"Content fingerprint: {CONTENT_FINGERPRINT}")


if __name__ == "__main__":
    main()
