#!/usr/bin/env python3
"""Generate C01E02 G1.5-B1 BREAKER ground-shell Candidate decision boards."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[6]

CONTRACT_COMMIT = "3c15d33a2af030ce3bcdf8d03ed4c627df5d9d45"
CONTENT_FINGERPRINT = "944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94"

TASK_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/16-g1-5-b1-breaker-art-objective.md"
PARENT_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/15-g1-5-representative-art-pilot.md"
APPROVAL_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv"
BUILD_CONTRACT_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/13-demo-build-contract.json"
VISUAL_SNAPSHOT_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/09b-frozen-visual-snapshot.tsv"
AUTHORITY_PATH = "docs/superpowers/specs/data/canon/authority_manifest.tsv"
ENTITIES_PATH = "docs/superpowers/specs/data/canon/entities.tsv"
ART_LOCKS_PATH = "docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv"
REBASE_PATH = "docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md"
OUTLINE_PATH = "docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md"
GZ_C96_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_96.png"
GZ_C128_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png"
GZ_BOARD_PATH = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png"

SOURCE_LOCKS = {
    TASK_PATH: ("f7647acbd306d6e5abe20c4a03f94e330a89ad10", "b9e858adce3b3bd8184c979e6702f2dec97c7cd7735f9c6e2f062a0f4d5dcc12"),
    PARENT_PATH: ("9fa5548a4ce81f935a86ba1f3ea322146a00e750", "844e9d15b8be1575f33b0b06992044a0cc7338284d27747802bce88eaae84b6f"),
    APPROVAL_PATH: ("3fecd3ea5bef592611bf0dbd9ce920b60c26d57f", "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee"),
    BUILD_CONTRACT_PATH: ("93d5727b25d8c397f25fa355d88e7ed1edf9e362", "ff76cba762dfb7458cb1a33784ccca766f549ce929d9d04f8b2ebc24c128f0b7"),
    VISUAL_SNAPSHOT_PATH: ("108b101aeb13dce0b6a15861fab970dea4d4c763", "4eec352ef11b7f6706559c2d7f3285136dba6781e4892066718696795dd89713"),
    AUTHORITY_PATH: ("fdb2057b833f4dfa0ad49a1229590c515d0e1a08", "d5203da48a7634c1ed977e5a638403d03cc3797980342747c83cfbb39c24969a"),
    ENTITIES_PATH: ("5d84ad9c4a3d82dac7015248261e22fe752bbd1c", "5c296a4f181257b1d8cfa05dc704339b70d38b6fd9f7a23fbb03ca920feb7b95"),
    ART_LOCKS_PATH: ("d568385869482a51e20ebb158fab5a6bb63529c7", "b680eb94d464a3b9e1f93a31f6a4e018d8958160dd0a9e774058bdcf5c7607eb"),
    REBASE_PATH: ("e4241dea1d4c10093e3867fa34f12c7010640e27", "e1ef7f96343433b589e3f1134dd4beb43dd773a922764a38fc47e43151995756"),
    OUTLINE_PATH: ("b91c05116e8d102652fe3d582a5dc6c64eb11276", "083b4678567f6d7e664939bc0e5227063765308a2f71b2be71168cb1215162ab"),
    GZ_C96_PATH: ("113fa85ba8542bcd0ffbda7e94481c0a4648a048", "82694df3f5f8f2c78bbea55cc5d982ef93a0f1a89f6eb293313933353f984a97"),
    GZ_C128_PATH: ("a5863aa4f8913b211cd4479c1d5cd895396e17d3", "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e"),
    GZ_BOARD_PATH: ("11e412b63fc7479865d62a71a029d37174f96148", "4d8e7975649b2b85458a838afd9bc2fe8e3a90fd8cbcfe8a7929b8ae9ae6c225"),
}

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

INK = "#16232c"
INK_DEEP = "#091117"
ARMOR = "#111a20"
ARMOR_2 = "#1f2c34"
ARMOR_3 = "#34434a"
JOINT = "#69767b"
STEEL = "#98a3a5"
RED = "#c93632"
RED_BRIGHT = "#ff5948"
RED_DARK = "#761f23"
TEAL = "#4f9295"
GOLD = "#d7a33c"
PAPER = "#edf1f2"
PAPER_LIGHT = "#fbfbf8"
MUTED = "#6e7d86"
GRID = "#8c9aa2"
WHITE = "#ffffff"


@dataclass(frozen=True)
class Candidate:
    code: str
    stable_id: str
    title: str
    motif: str
    strength: str
    risk: str
    red_relation: str
    action_note: str


CANDIDATES = (
    Candidate(
        "A",
        "CAND_BREAKER_B1_SIEGE_WEDGE_V1",
        "低伏攻城楔型",
        "长楔重壳把冲撞方向直接写进轮廓，收肢后最接近完整巨钻。",
        "3×3 占地、低头冲撞和侧甲受击面最直观。",
        "站立态较低，必须靠高背甲与巨爪维持近30米压迫感。",
        "头缝在楔首；胸缝垂直闭合；核心出口退到上背后段。",
        "idle 重压地面；move 四点推进；brace 横摆侧甲；impact 楔首下沉。",
    ),
    Candidate(
        "B",
        "CAND_BREAKER_B1_FORELIMB_BEARER_V1",
        "前肢承重半直立型",
        "上背高拱、前肢落地，双爪和抬头发射赤红冲击最清楚。",
        "侧推反馈、翻身和E03夹拳能力的动作空间最大。",
        "最容易过度类人，头必须持续埋在肩壳之间。",
        "头缝在肩壳下；胸缝藏在腹甲；出口为封闭的后颈背舱。",
        "idle 前爪承重；move 猛兽式换步；brace 双爪撑地；impact 肩背回弹。",
    ),
    Candidate(
        "C",
        "CAND_BREAKER_B1_ARMORED_POD_BEAST_V1",
        "装甲舱壳兽型",
        "椭圆舱壳包覆内部主体，四肢像锁扣一样围住外壳。",
        "最能预埋‘地面壳包住飞行核心’，侧翻后仍像完整重物。",
        "容易读成坦克或泛用怪兽，必须保留无履带、双爪与钻地闭合逻辑。",
        "头缝在前端帽壳；胸缝横向闭合；出口为上背独立封舱。",
        "idle 壳体微俯；move 四锁扣踏行；brace 壳缘接地；impact 整舱侧滚。",
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


def git_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{CONTRACT_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def validate_authority() -> tuple[dict[str, bytes], list[dict[str, str]]]:
    commit = subprocess.run(
        ["git", "rev-parse", f"{CONTRACT_COMMIT}^{{commit}}"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()
    if commit != CONTRACT_COMMIT:
        raise RuntimeError(f"B1 contract commit drifted: {commit}")

    source_bytes: dict[str, bytes] = {}
    for path, (expected_blob, expected_sha) in SOURCE_LOCKS.items():
        actual_blob = subprocess.run(
            ["git", "rev-parse", f"{CONTRACT_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip()
        data = git_bytes(path)
        if actual_blob != expected_blob or sha256_bytes(data) != expected_sha:
            raise RuntimeError(f"B1 source lock mismatch: {path}")
        source_bytes[path] = data

    build_contract = json.loads(source_bytes[BUILD_CONTRACT_PATH].decode("utf-8"))
    if build_contract["content_fingerprint"] != CONTENT_FINGERPRINT:
        raise RuntimeError("Frozen Demo content fingerprint mismatch")

    authority_rows = list(csv.DictReader(io.StringIO(source_bytes[AUTHORITY_PATH].decode("utf-8")), delimiter="\t"))
    breaker_authority = [row for row in authority_rows if row.get("record_type") == "entity" and row.get("record_id") == "ENEMY_C01_BREAKER"]
    if len(breaker_authority) != 1:
        raise RuntimeError("Expected one ENEMY_C01_BREAKER authority row")
    authority = breaker_authority[0]
    if authority.get("canon_level") != "working" or authority.get("lifecycle_status") != "active":
        raise RuntimeError("BREAKER is not Working/active")

    entity_rows = list(csv.DictReader(io.StringIO(source_bytes[ENTITIES_PATH].decode("utf-8")), delimiter="\t"))
    breaker_rows = [row for row in entity_rows if row.get("entity_id") == "ENEMY_C01_BREAKER"]
    if len(breaker_rows) != 1:
        raise RuntimeError("Expected one BREAKER entity row")
    implementation = breaker_rows[0].get("implementation_policy", "")
    for required in ("近30米黑甲突入壳", "钻地", "冲撞", "赤红冲击", "十余米核心", "近50米薄翼"):
        if required not in implementation:
            raise RuntimeError(f"BREAKER Working identity missing: {required}")

    if "ENEMY_C01_BREAKER" in source_bytes[ART_LOCKS_PATH].decode("utf-8"):
        raise RuntimeError("Unexpected BREAKER art lock found")

    approval_rows = list(csv.DictReader(io.StringIO(source_bytes[APPROVAL_PATH].decode("utf-8")), delimiter="\t"))
    if len(approval_rows) != 2:
        raise RuntimeError("Expected two A1-C approval rows")
    approved_paths = {row["path"]: row for row in approval_rows}
    for path, expected in ((GZ_C96_PATH, SOURCE_LOCKS[GZ_C96_PATH][1]), (GZ_C128_PATH, SOURCE_LOCKS[GZ_C128_PATH][1])):
        row = approved_paths.get(path)
        if not row or row["selection"] != "C_ACTION_FRAME" or row["sha256"] != expected:
            raise RuntimeError(f"A1-C approval mismatch: {path}")
        if row["runtime_allowed"].lower() != "false" or row["approval_scope"] != "direction_approved_for_derivative_design":
            raise RuntimeError(f"A1-C approval scope mismatch: {path}")

    task_text = source_bytes[TASK_PATH].decode("utf-8")
    for required in ("地面阶段站立后接近 30 米", "层层黑甲包覆", "96×96 与 128×128", "3×3 footprint", "内部与上背结构"):
        if required not in task_text:
            raise RuntimeError(f"B1 task fact missing: {required}")
    return source_bytes, approval_rows


def polygon(draw: ImageDraw.ImageDraw, points, fill, *, width: int = 7, outline=INK_DEEP) -> None:
    draw.polygon(points, fill=fill, outline=outline)
    draw.line((*points, points[0]), fill=outline, width=width, joint="curve")


def rounded(draw: ImageDraw.ImageDraw, box, radius: int, fill, *, width: int = 7, outline=INK_DEEP) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def red_slit(draw: ImageDraw.ImageDraw, box, *, vertical: bool = False) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, max(3, min(x1 - x0, y1 - y0) // 3), RED_DARK, width=5)
    if vertical:
        draw.line(((x0 + x1) // 2, y0 + 4, (x0 + x1) // 2, y1 - 4), fill=RED_BRIGHT, width=max(3, (x1 - x0) // 3))
    else:
        draw.line((x0 + 6, (y0 + y1) // 2, x1 - 6, (y0 + y1) // 2), fill=RED_BRIGHT, width=max(3, (y1 - y0) // 3))


def seam(draw: ImageDraw.ImageDraw, points, *, width: int = 6) -> None:
    draw.line(points, fill=INK_DEEP, width=width, joint="curve")
    draw.line(points, fill=ARMOR_3, width=max(2, width // 3), joint="curve")


def claw(draw: ImageDraw.ImageDraw, center: tuple[int, int], scale: float, *, mirror: int = 1) -> None:
    cx, cy = center
    palm = ((cx - 44 * mirror * scale, cy - 31 * scale), (cx + 26 * mirror * scale, cy - 38 * scale),
            (cx + 50 * mirror * scale, cy + 17 * scale), (cx - 18 * mirror * scale, cy + 42 * scale))
    polygon(draw, palm, ARMOR_2, width=max(4, int(7 * scale)))
    for offset in (-24, 0, 24):
        base_x = cx + (22 + offset * 0.25) * mirror * scale
        base_y = cy + (8 + abs(offset) * 0.18) * scale
        tip_x = cx + (74 + abs(offset) * 0.45) * mirror * scale
        tip_y = cy + (22 + offset * 0.62) * scale
        polygon(
            draw,
            ((base_x, base_y - 9 * scale), (tip_x, tip_y), (base_x + 8 * mirror * scale, base_y + 16 * scale)),
            STEEL,
            width=max(3, int(5 * scale)),
        )


def leg(draw: ImageDraw.ImageDraw, x: int, top: int, bottom: int, width: int, *, lean: int = 0) -> None:
    polygon(
        draw,
        ((x - width // 2, top), (x + width // 2, top + lean),
         (x + width // 2 + 10, bottom - 54), (x - width // 2 - 12, bottom - 42)),
        ARMOR_2,
        width=7,
    )
    rounded(draw, (x - width // 2 - 18, bottom - 67, x + width // 2 + 24, bottom), 18, ARMOR, width=7)
    draw.rectangle((x - 8, bottom - 61, x + 11, bottom - 8), fill=ARMOR_3)


def draw_a(view: str) -> Image.Image:
    image = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    if view == "front":
        leg(draw, 255, 455, 716, 92, lean=-7)
        leg(draw, 545, 455, 716, 92, lean=7)
        polygon(draw, ((105, 300), (215, 160), (400, 92), (585, 160), (695, 300), (618, 470), (182, 470)), ARMOR, width=11)
        polygon(draw, ((160, 295), (280, 178), (400, 135), (400, 450), (210, 420)), ARMOR_2, width=7)
        polygon(draw, ((640, 295), (520, 178), (400, 135), (400, 450), (590, 420)), ARMOR_3, width=7)
        rounded(draw, (285, 250, 515, 350), 26, ARMOR_2, width=9)
        red_slit(draw, (325, 286, 475, 310))
        polygon(draw, ((274, 348), (526, 348), (575, 494), (400, 548), (225, 494)), ARMOR_2, width=9)
        seam(draw, ((400, 365), (400, 520)), width=8)
        seam(draw, ((285, 183), (400, 144), (515, 183)), width=5)
        polygon(draw, ((178, 342), (88, 410), (152, 594), (265, 510)), ARMOR, width=9)
        polygon(draw, ((622, 342), (712, 410), (648, 594), (535, 510)), ARMOR_3, width=9)
        claw(draw, (145, 565), 1.05, mirror=-1)
        claw(draw, (655, 565), 1.05, mirror=1)
    elif view == "side":
        leg(draw, 445, 430, 716, 105, lean=4)
        leg(draw, 610, 445, 711, 88, lean=12)
        polygon(draw, ((92, 327), (178, 230), (520, 118), (690, 175), (710, 360), (570, 485), (220, 475)), ARMOR, width=11)
        polygon(draw, ((170, 308), (392, 184), (650, 188), (664, 350), (521, 428), (225, 433)), ARMOR_2, width=7)
        rounded(draw, (85, 292, 285, 383), 26, ARMOR_2, width=9)
        red_slit(draw, (112, 326, 239, 348))
        seam(draw, ((305, 355), (440, 412)), width=8)
        seam(draw, ((500, 146), (605, 170), (657, 225)), width=6)
        polygon(draw, ((210, 385), (120, 464), (184, 630), (312, 510)), ARMOR_2, width=9)
        claw(draw, (175, 606), 1.02, mirror=-1)
    else:
        leg(draw, 310, 448, 715, 92, lean=-8)
        leg(draw, 565, 438, 700, 80, lean=9)
        polygon(draw, ((100, 312), (218, 172), (470, 90), (688, 190), (650, 390), (500, 505), (190, 480)), ARMOR, width=11)
        polygon(draw, ((175, 308), (300, 196), (474, 133), (472, 462), (230, 445)), ARMOR_2, width=7)
        polygon(draw, ((474, 133), (640, 211), (612, 369), (472, 462)), ARMOR_3, width=7)
        rounded(draw, (184, 276, 395, 368), 25, ARMOR_2, width=9)
        red_slit(draw, (218, 311, 354, 333))
        polygon(draw, ((236, 362), (474, 342), (538, 494), (343, 548), (210, 472)), ARMOR_2, width=9)
        seam(draw, ((370, 365), (386, 520)), width=8)
        seam(draw, ((470, 125), (560, 164), (623, 216)), width=6)
        polygon(draw, ((185, 386), (101, 476), (173, 625), (289, 510)), ARMOR, width=9)
        polygon(draw, ((528, 374), (648, 432), (620, 576), (500, 508)), ARMOR_3, width=9)
        claw(draw, (154, 601), 0.98, mirror=-1)
        claw(draw, (632, 558), 0.88, mirror=1)
    return image


def draw_b(view: str) -> Image.Image:
    image = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    if view == "front":
        leg(draw, 310, 455, 716, 84, lean=-4)
        leg(draw, 490, 455, 716, 84, lean=4)
        polygon(draw, ((165, 260), (255, 120), (400, 82), (545, 120), (635, 260), (558, 485), (242, 485)), ARMOR, width=11)
        polygon(draw, ((210, 258), (315, 148), (400, 126), (400, 454), (260, 433)), ARMOR_2, width=7)
        polygon(draw, ((590, 258), (485, 148), (400, 126), (400, 454), (540, 433)), ARMOR_3, width=7)
        rounded(draw, (296, 224, 504, 326), 24, ARMOR_2, width=9)
        red_slit(draw, (335, 262, 465, 284))
        polygon(draw, ((288, 322), (512, 322), (545, 485), (400, 553), (255, 485)), ARMOR_2, width=9)
        seam(draw, ((400, 342), (400, 525)), width=8)
        for x, mirror in ((177, -1), (623, 1)):
            polygon(draw, ((x - 58, 282), (x + 55, 272), (x + 64, 558), (x - 40, 610)), ARMOR_2 if mirror < 0 else ARMOR_3, width=9)
            rounded(draw, (x - 52, 440, x + 55, 640), 24, ARMOR, width=8)
            claw(draw, (x, 651), 0.94, mirror=mirror)
        seam(draw, ((315, 151), (400, 126), (485, 151)), width=6)
    elif view == "side":
        leg(draw, 500, 450, 716, 92, lean=12)
        leg(draw, 635, 456, 704, 76, lean=13)
        polygon(draw, ((120, 290), (260, 135), (530, 105), (680, 205), (640, 430), (410, 510), (205, 440)), ARMOR, width=11)
        polygon(draw, ((210, 270), (330, 168), (580, 158), (625, 382), (420, 464), (226, 410)), ARMOR_2, width=7)
        rounded(draw, (112, 272, 300, 365), 24, ARMOR_2, width=9)
        red_slit(draw, (140, 308, 258, 330))
        seam(draw, ((330, 345), (445, 450)), width=8)
        seam(draw, ((476, 129), (570, 160), (625, 210)), width=6)
        polygon(draw, ((235, 350), (157, 430), (190, 638), (310, 545)), ARMOR_2, width=9)
        rounded(draw, (175, 445, 288, 655), 25, ARMOR, width=8)
        claw(draw, (205, 665), 0.96, mirror=-1)
    else:
        leg(draw, 365, 465, 716, 82, lean=-6)
        leg(draw, 555, 443, 700, 74, lean=8)
        polygon(draw, ((120, 284), (260, 130), (468, 82), (675, 190), (623, 425), (420, 520), (218, 454)), ARMOR, width=11)
        polygon(draw, ((195, 275), (315, 160), (470, 126), (440, 478), (244, 420)), ARMOR_2, width=7)
        polygon(draw, ((470, 126), (625, 205), (585, 392), (440, 478)), ARMOR_3, width=7)
        rounded(draw, (180, 255, 370, 350), 24, ARMOR_2, width=9)
        red_slit(draw, (212, 292, 332, 314))
        polygon(draw, ((240, 344), (452, 328), (500, 500), (350, 563), (218, 472)), ARMOR_2, width=9)
        seam(draw, ((350, 356), (366, 534)), width=8)
        seam(draw, ((470, 119), (560, 153), (619, 200)), width=6)
        polygon(draw, ((190, 360), (112, 456), (160, 648), (288, 532)), ARMOR_2, width=9)
        rounded(draw, (132, 448, 245, 655), 24, ARMOR, width=8)
        claw(draw, (160, 665), 0.94, mirror=-1)
        polygon(draw, ((510, 355), (640, 400), (621, 578), (490, 520)), ARMOR_3, width=9)
        claw(draw, (625, 585), 0.78, mirror=1)
    return image


def draw_c(view: str) -> Image.Image:
    image = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    if view == "front":
        leg(draw, 270, 480, 715, 82, lean=-8)
        leg(draw, 530, 480, 715, 82, lean=8)
        rounded(draw, (135, 130, 665, 545), 178, ARMOR, width=12)
        polygon(draw, ((180, 245), (285, 145), (400, 115), (400, 522), (185, 493)), ARMOR_2, width=7)
        polygon(draw, ((620, 245), (515, 145), (400, 115), (400, 522), (615, 493)), ARMOR_3, width=7)
        rounded(draw, (268, 245, 532, 350), 34, ARMOR_2, width=9)
        red_slit(draw, (318, 286, 482, 311))
        seam(draw, ((280, 390), (400, 420), (520, 390)), width=9)
        seam(draw, ((330, 150), (400, 126), (470, 150)), width=6)
        for x, mirror in ((145, -1), (655, 1)):
            polygon(draw, ((x - 50, 320), (x + 55, 300), (x + 70, 540), (x - 30, 580)), ARMOR_2 if mirror < 0 else ARMOR_3, width=9)
            claw(draw, (x, 568), 0.96, mirror=mirror)
    elif view == "side":
        leg(draw, 430, 470, 716, 83, lean=8)
        leg(draw, 620, 470, 704, 73, lean=12)
        rounded(draw, (115, 145, 700, 550), 180, ARMOR, width=12)
        polygon(draw, ((165, 260), (330, 165), (610, 178), (670, 350), (585, 510), (230, 500)), ARMOR_2, width=7)
        rounded(draw, (105, 278, 300, 382), 32, ARMOR_2, width=9)
        red_slit(draw, (137, 319, 258, 342))
        seam(draw, ((310, 400), (478, 455)), width=9)
        seam(draw, ((500, 168), (603, 190), (655, 240)), width=6)
        polygon(draw, ((230, 382), (130, 470), (183, 625), (318, 525)), ARMOR_2, width=9)
        claw(draw, (175, 612), 0.96, mirror=-1)
    else:
        leg(draw, 350, 490, 716, 80, lean=-6)
        leg(draw, 560, 465, 704, 72, lean=10)
        rounded(draw, (120, 135, 688, 548), 180, ARMOR, width=12)
        polygon(draw, ((175, 252), (315, 155), (485, 125), (455, 527), (207, 486)), ARMOR_2, width=7)
        polygon(draw, ((485, 125), (640, 210), (645, 395), (455, 527)), ARMOR_3, width=7)
        rounded(draw, (170, 270, 370, 373), 31, ARMOR_2, width=9)
        red_slit(draw, (202, 310, 329, 333))
        seam(draw, ((252, 410), (382, 437), (500, 400)), width=9)
        seam(draw, ((475, 139), (565, 169), (625, 215)), width=6)
        polygon(draw, ((188, 380), (104, 475), (164, 628), (292, 520)), ARMOR_2, width=9)
        polygon(draw, ((525, 375), (664, 435), (632, 590), (510, 520)), ARMOR_3, width=9)
        claw(draw, (145, 611), 0.92, mirror=-1)
        claw(draw, (650, 580), 0.80, mirror=1)
    return image


def draw_breaker(candidate: Candidate, view: str) -> Image.Image:
    if candidate.code == "A":
        return draw_a(view)
    if candidate.code == "B":
        return draw_b(view)
    return draw_c(view)


def draw_mode(candidate: Candidate, mode: str) -> Image.Image:
    image = Image.new("RGBA", (800, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    if mode == "drill":
        if candidate.code == "A":
            shell = ((92, 250), (300, 108), (675, 142), (738, 250), (675, 358), (300, 392))
        elif candidate.code == "B":
            shell = ((86, 250), (318, 95), (650, 132), (736, 250), (650, 368), (318, 405))
        else:
            shell = ((88, 250), (270, 116), (635, 110), (736, 250), (635, 390), (270, 384))
        polygon(draw, shell, ARMOR, width=11)
        for x in (248, 355, 470, 585):
            draw.line((x, 145, x + 30, 355), fill=ARMOR_3, width=12)
        polygon(draw, ((64, 250), (150, 206), (150, 294)), STEEL, width=8)
        red_slit(draw, (154, 236, 245, 260))
        seam(draw, ((520, 150), (630, 164)), width=5)
    else:
        body = draw_breaker(candidate, "side").resize((520, 520), Image.Resampling.LANCZOS)
        image.alpha_composite(body, (180, -25))
        draw.polygon(((76, 265), (300, 205), (300, 325)), fill=(201, 54, 50, 75))
        draw.line((92, 265, 325, 265), fill=RED_BRIGHT, width=10)
        for y in (150, 205, 320, 375):
            draw.line((80, y, 230, y + 18), fill=(110, 125, 133, 115), width=7)
    return image


def native_sprite(candidate: Candidate, size: int) -> Image.Image:
    source = draw_breaker(candidate, "threeq")
    bbox = source.getbbox()
    if not bbox:
        raise RuntimeError(f"Empty BREAKER candidate: {candidate.code}")
    crop = source.crop(bbox)
    target = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    max_w = int(size * 0.88)
    max_h = int(size * 0.86)
    scale = min(max_w / crop.width, max_h / crop.height)
    resized = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)
    x = (size - resized.width) // 2
    ground_y = round(size * 0.91)
    target.alpha_composite(resized, (x, ground_y - resized.height))
    return target


def board_text(draw: ImageDraw.ImageDraw, xy, value: str, size: int, color=INK, *, bold=False, anchor=None) -> None:
    draw.text(xy, value, font=font(size, bold=bold), fill=color, anchor=anchor)


def wrap_text(draw: ImageDraw.ImageDraw, box, value: str, size: int, color=INK, *, bold=False, spacing=5) -> None:
    x0, y0, x1, _ = box
    current = ""
    lines: list[str] = []
    for char in value:
        trial = current + char
        if draw.textbbox((0, 0), trial, font=font(size, bold=bold))[2] > x1 - x0 and current:
            lines.append(current)
            current = char
        else:
            current = trial
    if current:
        lines.append(current)
    draw.multiline_text((x0, y0), "\n".join(lines), font=font(size, bold=bold), fill=color, spacing=spacing)


def panel(draw: ImageDraw.ImageDraw, box, *, fill=PAPER_LIGHT, outline=GRID, width=2, radius=6) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def fit_alpha(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    bbox = source.getbbox()
    if not bbox:
        return Image.new("RGBA", size, (0, 0, 0, 0))
    crop = source.crop(bbox)
    scale = min(size[0] / crop.width, size[1] / crop.height)
    return crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)


def paste_center(canvas: Image.Image, source: Image.Image, box: tuple[int, int, int, int], *, bottom=False) -> None:
    x0, y0, x1, y1 = box
    fitted = fit_alpha(source, (x1 - x0, y1 - y0))
    x = x0 + (x1 - x0 - fitted.width) // 2
    y = y1 - fitted.height if bottom else y0 + (y1 - y0 - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))


def draw_iso_cells(draw: ImageDraw.ImageDraw, origin: tuple[int, int], count: int, *, cell_w=42, cell_h=22, anchor=False) -> tuple[int, int]:
    ox, oy = origin
    for layer in range(count * 2 - 1):
        for y in range(count):
            for x in range(count):
                if x + y != layer:
                    continue
                cx = ox + (x - y) * cell_w
                cy = oy + (x + y) * cell_h
                points = ((cx, cy - cell_h), (cx + cell_w, cy), (cx, cy + cell_h), (cx - cell_w, cy))
                fill = "#dfe7e9" if (x + y) % 2 == 0 else "#d3dde0"
                draw.polygon(points, fill=fill, outline=GRID)
                if anchor and x == 0 and y == 0:
                    draw.line((*points, points[0]), fill=RED, width=4)
    return ox, oy + (count - 1) * cell_h


def draw_footprint(canvas: Image.Image, origin: tuple[int, int], sprite: Image.Image, *, count: int, label_anchor=True) -> None:
    draw = ImageDraw.Draw(canvas, "RGBA")
    _, ground_y = draw_iso_cells(draw, origin, count, anchor=label_anchor)
    px = origin[0] - sprite.width // 2
    py = ground_y + 18 - sprite.height
    canvas.alpha_composite(sprite, (px, py))
    draw.ellipse((origin[0] - 5, ground_y + 13, origin[0] + 5, ground_y + 23), fill=RED, outline=INK, width=2)


def make_scale_compare(candidate: Candidate, gz96: Image.Image, sprite128: Image.Image) -> Image.Image:
    image = Image.new("RGBA", (520, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_footprint(image, (130, 155), gz96, count=2)
    draw_footprint(image, (365, 118), sprite128, count=3)
    board_text(draw, (130, 276), "馆守 Z C / 18m / 2×2", 15, INK, bold=True, anchor="mm")
    board_text(draw, (365, 276), "BREAKER / 近30m / 3×3", 15, INK, bold=True, anchor="mm")
    return image


def relation_diagram(candidate: Candidate) -> Image.Image:
    image = Image.new("RGBA", (520, 260), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    side = fit_alpha(draw_breaker(candidate, "side"), (360, 230))
    image.alpha_composite(side, (8, 12))
    if candidate.code == "A":
        markers = ((80, 120, RED_BRIGHT, "头部红缝"), (190, 165, STEEL, "闭合胸缝"), (290, 70, TEAL, "封闭上背出口"))
    elif candidate.code == "B":
        markers = ((88, 118, RED_BRIGHT, "头部红缝"), (208, 176, STEEL, "闭合胸缝"), (292, 62, TEAL, "封闭后颈出口"))
    else:
        markers = ((78, 126, RED_BRIGHT, "头部红缝"), (215, 177, STEEL, "闭合胸缝"), (302, 65, TEAL, "封闭背舱出口"))
    label_y = 36
    for x, y, color, label in markers:
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color, outline=INK_DEEP, width=2)
        draw.line((x + 6, y, 382, label_y + 8), fill=color, width=3)
        board_text(draw, (392, label_y), label, 15, INK, bold=True)
        label_y += 58
    return image


def generate_candidate_sheet(candidate: Candidate, sprites: dict[tuple[str, int], Image.Image], gz96: Image.Image) -> Path:
    canvas = Image.new("RGBA", (1800, 1200), PAPER)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, 1800, 92), fill=INK)
    board_text(draw, (34, 24), f"C01E02 G1.5-B1｜BREAKER {candidate.code} {candidate.title}", 30, WHITE, bold=True)
    board_text(draw, (1768, 31), "Candidate / runtime_allowed=false", 18, GOLD, anchor="ra")

    view_boxes = ((28, 116, 560, 650), (576, 116, 1108, 650), (1124, 116, 1772, 650))
    for box, label, view in zip(view_boxes, ("正面黑白轮廓", "严格侧面轮廓", "朝北三分之四主视图"), ("front", "side", "threeq")):
        panel(draw, box, outline=ARMOR_3, width=3)
        board_text(draw, (box[0] + 20, box[1] + 18), label, 20, INK, bold=True)
        paste_center(canvas, draw_breaker(candidate, view), (box[0] + 18, box[1] + 52, box[2] - 18, box[3] - 20), bottom=True)
    draw.line((1510, 145, 1510, 210), fill=RED, width=5)
    polygon(draw, ((1498, 160), (1510, 135), (1522, 160)), RED, width=3)
    board_text(draw, (1530, 148), "NORTH", 14, RED, bold=True)

    panel(draw, (28, 670, 550, 926), outline=RED, width=3)
    board_text(draw, (48, 688), "收肢钻地 / 低伏冲撞缩略", 19, INK, bold=True)
    paste_center(canvas, draw_mode(candidate, "drill"), (44, 728, 290, 900))
    paste_center(canvas, draw_mode(candidate, "charge"), (300, 728, 534, 900))
    board_text(draw, (167, 900), "DRILL", 13, MUTED, bold=True, anchor="mm")
    board_text(draw, (417, 900), "CHARGE", 13, MUTED, bold=True, anchor="mm")

    panel(draw, (568, 670, 910, 926), outline=GOLD, width=3)
    board_text(draw, (588, 688), "透明原生样张", 19, INK, bold=True)
    draw.rectangle((592, 730, 722, 890), fill="#dfe5e7", outline=GRID)
    draw.rectangle((746, 710, 886, 890), fill="#dfe5e7", outline=GRID)
    canvas.alpha_composite(sprites[(candidate.code, 96)], (609, 754))
    canvas.alpha_composite(sprites[(candidate.code, 128)], (752, 735))
    board_text(draw, (657, 902), "96×96", 13, INK, bold=True, anchor="mm")
    board_text(draw, (816, 902), "128×128", 13, INK, bold=True, anchor="mm")

    panel(draw, (928, 670, 1772, 926), outline=TEAL, width=3)
    board_text(draw, (948, 688), "3×3 实读 / north_west_cell anchor / bottom_center pivot", 18, INK, bold=True)
    draw_footprint(canvas, (1125, 763), sprites[(candidate.code, 128)], count=3)
    scale = make_scale_compare(candidate, gz96, sprites[(candidate.code, 128)])
    canvas.alpha_composite(scale.resize((480, 240), Image.Resampling.LANCZOS), (1265, 680))
    board_text(draw, (1000, 878), "红框：north_west_cell", 13, RED, bold=True)
    board_text(draw, (1000, 898), "红点：接地中心 / pivot", 13, MUTED, bold=True)
    board_text(draw, (1510, 710), "战棋视觉压缩，米制高度以 18m / 近30m 标注为准", 11, MUTED, anchor="mm")

    panel(draw, (28, 946, 710, 1172), outline=ARMOR_3, width=3)
    board_text(draw, (48, 964), "轮廓判断", 18, INK, bold=True)
    wrap_text(draw, (48, 1000, 690, 1048), candidate.motif, 16, INK, bold=True)
    board_text(draw, (48, 1060), "优势", 15, TEAL, bold=True)
    wrap_text(draw, (112, 1060, 690, 1108), candidate.strength, 15, INK)
    board_text(draw, (48, 1120), "风险", 15, RED, bold=True)
    wrap_text(draw, (112, 1120, 690, 1162), candidate.risk, 15, INK)

    panel(draw, (728, 946, 1260, 1172), outline=RED, width=3)
    board_text(draw, (748, 964), "红缝—胸缝—核心出口关系", 18, INK, bold=True)
    relation = relation_diagram(candidate).resize((500, 180), Image.Resampling.LANCZOS)
    canvas.alpha_composite(relation, (744, 988))

    panel(draw, (1278, 946, 1772, 1172), outline=GOLD, width=3)
    board_text(draw, (1298, 964), "动作扩展（不制作动作帧）", 18, INK, bold=True)
    wrap_text(draw, (1298, 1004, 1750, 1080), candidate.action_note, 16, INK, bold=True)
    board_text(draw, (1298, 1094), "表面语言仍待用户裁决", 15, RED, bold=True)
    wrap_text(draw, (1298, 1120, 1750, 1162), "本页使用中性机械/异质混合大色块，不锁定后续敌群表面语法。", 14, MUTED)

    path = OUT / f"BREAKER_B1_candidate_{candidate.code}_identity_sheet_1800x1200.png"
    canvas.convert("RGB").save(path)
    return path


def generate_direction_board(sprites: dict[tuple[str, int], Image.Image], gz96: Image.Image) -> Path:
    board = Image.new("RGBA", (2400, 1600), PAPER)
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 2400, 104), fill=INK)
    board_text(draw, (34, 27), "C01E02 G1.5-B1｜BREAKER 地面壳轮廓身份 + Q/SD 地图转译判断板", 32, WHITE, bold=True)
    board_text(draw, (2368, 34), "Working text lock → Candidate art / runtime_allowed=false", 18, GOLD, anchor="ra")

    panel(draw, (24, 126, 430, 1574), outline=ARMOR_3, width=3)
    board_text(draw, (46, 146), "共同锁定事实", 24, INK, bold=True)
    facts = (
        "近30m / 馆守 Z 18m",
        "黑甲地面壳 / 3×3 footprint",
        "头部常态只有一道红缝",
        "胸缝闭合，不是亮弱点",
        "双爪 / 可收肢成巨钻",
        "低伏冲撞 / 侧甲可受击",
        "上背能容纳后置核心",
        "E02倒地未毁，可重新压低",
    )
    y = 196
    for index, fact in enumerate(facts, start=1):
        draw.ellipse((46, y, 76, y + 30), fill=RED if index in (3, 4) else ARMOR_3, outline=INK_DEEP, width=2)
        board_text(draw, (61, y + 15), f"{index:02d}", 11, WHITE, bold=True, anchor="mm")
        board_text(draw, (88, y + 3), fact, 16, INK, bold=True)
        y += 56
    board_text(draw, (46, 674), "E02 禁止提前出现", 19, RED, bold=True)
    forbidden = "飞行核心 / 薄翼 / 胸部发光红裂 / 破甲洞 / 阵营编号 / 驾驶舱"
    wrap_text(draw, (46, 710, 404, 790), forbidden, 16, RED)
    board_text(draw, (46, 824), "共同生产语法", 19, TEAL, bold=True)
    wrap_text(draw, (46, 862, 404, 970), "A / KINETIC_CEL：深墨压力线、大色块、两级硬阴影；不做碎划痕、碎贴纸或AI式表面噪声。", 16, INK)
    board_text(draw, (46, 1010), "尺度只读锚", 19, GOLD, bold=True)
    compare = make_scale_compare(CANDIDATES[0], gz96, sprites[("A", 128)])
    board.alpha_composite(compare.resize((365, 211), Image.Resampling.LANCZOS), (42, 1045))
    board_text(draw, (224, 1266), "战棋视觉压缩，不等于米制 1:1", 12, MUTED, anchor="mm")
    board_text(draw, (46, 1288), "本轮不决定", 19, RED, bold=True)
    wrap_text(draw, (46, 1326, 404, 1412), "最终Sprite Sheet、动作帧、Cut-in、视频、重盾、地图、E03破甲和飞行核心造型。", 15, INK)
    board_text(draw, (46, 1480), "用户需分别选择：轮廓 / 表面语言 / 三处结构关系", 15, MUTED, bold=True)

    x_positions = (450, 1102, 1754)
    accents = (RED, TEAL, GOLD)
    for candidate, x0, accent in zip(CANDIDATES, x_positions, accents):
        x1 = x0 + 628
        panel(draw, (x0, 126, x1, 1574), outline=accent, width=4)
        board_text(draw, (x0 + 22, 146), f"{candidate.code}｜{candidate.title}", 25, INK, bold=True)
        board_text(draw, (x1 - 20, 151), candidate.stable_id, 11, accent, bold=True, anchor="ra")

        view_y = 194
        view_w = 186
        for index, (view, label) in enumerate((("front", "正面"), ("side", "严格侧面"), ("threeq", "朝北3/4"))):
            bx0 = x0 + 18 + index * 198
            panel(draw, (bx0, view_y, bx0 + view_w, 570), outline=GRID, width=2)
            board_text(draw, (bx0 + 12, view_y + 12), label, 15, INK, bold=True)
            paste_center(board, draw_breaker(candidate, view), (bx0 + 7, view_y + 42, bx0 + view_w - 7, 558), bottom=True)

        board_text(draw, (x0 + 22, 590), "DRILL / CHARGE 轮廓验证", 16, INK, bold=True)
        panel(draw, (x0 + 18, 622, x0 + 305, 802), outline=GRID)
        panel(draw, (x0 + 321, 622, x1 - 18, 802), outline=GRID)
        paste_center(board, draw_mode(candidate, "drill"), (x0 + 26, 632, x0 + 296, 788))
        paste_center(board, draw_mode(candidate, "charge"), (x0 + 329, 632, x1 - 26, 788))

        board_text(draw, (x0 + 22, 828), "透明 96 / 128 px", 16, INK, bold=True)
        panel(draw, (x0 + 18, 858, x0 + 270, 1038), outline=GRID)
        board.alpha_composite(sprites[(candidate.code, 96)], (x0 + 42, 900))
        board.alpha_composite(sprites[(candidate.code, 128)], (x0 + 130, 878))
        board_text(draw, (x0 + 92, 1020), "96", 12, MUTED, bold=True, anchor="mm")
        board_text(draw, (x0 + 194, 1020), "128", 12, MUTED, bold=True, anchor="mm")
        panel(draw, (x0 + 286, 858, x1 - 18, 1038), outline=GRID)
        draw_footprint(board, (x0 + 450, 920), sprites[(candidate.code, 128)], count=3)
        board_text(draw, (x0 + 450, 1020), "3×3 / NW anchor / bottom pivot", 12, MUTED, bold=True, anchor="mm")

        board_text(draw, (x0 + 22, 1062), "轮廓母题", 16, accent, bold=True)
        wrap_text(draw, (x0 + 22, 1094, x1 - 20, 1152), candidate.motif, 15, INK, bold=True)
        board_text(draw, (x0 + 22, 1170), "优势", 15, TEAL, bold=True)
        wrap_text(draw, (x0 + 82, 1170, x1 - 20, 1225), candidate.strength, 14, INK)
        board_text(draw, (x0 + 22, 1240), "风险", 15, RED, bold=True)
        wrap_text(draw, (x0 + 82, 1240, x1 - 20, 1295), candidate.risk, 14, INK)
        board_text(draw, (x0 + 22, 1310), "三处关系", 15, GOLD, bold=True)
        wrap_text(draw, (x0 + 110, 1310, x1 - 20, 1364), candidate.red_relation, 14, INK)
        board_text(draw, (x0 + 22, 1378), "动作空间", 15, ARMOR_3, bold=True)
        wrap_text(draw, (x0 + 110, 1378, x1 - 20, 1460), candidate.action_note, 14, INK)
        board_text(draw, (x0 + 22, 1512), "表面语言未锁：机械攻城壳 ↔ 异质/生体装甲", 13, RED, bold=True)

    path = OUT / "BREAKER_B1_direction_board_2400x1600.png"
    board.convert("RGB").save(path)
    return path


def generate_surface_relation_board() -> Path:
    board = Image.new("RGBA", (1800, 1100), PAPER)
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 1800, 92), fill=INK)
    board_text(draw, (34, 24), "G1.5-B1｜BREAKER 表面语言与三处结构关系裁决板", 30, WHITE, bold=True)
    board_text(draw, (1768, 31), "Candidate / no selection implied", 18, GOLD, anchor="ra")

    panel(draw, (28, 116, 872, 590), outline=TEAL, width=4)
    board_text(draw, (54, 142), "M｜机械攻城壳", 25, INK, bold=True)
    board_text(draw, (54, 182), "直线折板、承力梁、少量大铰接；城市突入兵器感更强。", 17, MUTED)
    polygon(draw, ((100, 360), (230, 230), (570, 202), (780, 330), (680, 500), (225, 510)), ARMOR, width=12)
    polygon(draw, ((145, 355), (290, 258), (475, 240), (470, 478), (220, 470)), ARMOR_2, width=7)
    polygon(draw, ((475, 240), (660, 290), (716, 365), (650, 470), (470, 478)), ARMOR_3, width=7)
    red_slit(draw, (130, 350, 265, 378))
    seam(draw, ((330, 360), (450, 430)), width=8)
    seam(draw, ((555, 230), (650, 285)), width=6)

    panel(draw, (928, 116, 1772, 590), outline=RED, width=4)
    board_text(draw, (954, 142), "X｜异质 / 生体装甲", 25, INK, bold=True)
    board_text(draw, (954, 182), "曲面叠壳、非对称咬合、少量柔性缝；裂星潮异物感更强。", 17, MUTED)
    rounded(draw, (1010, 220, 1680, 512), 145, ARMOR, width=12)
    polygon(draw, ((1038, 365), (1160, 255), (1390, 230), (1330, 488), (1115, 475)), ARMOR_2, width=7)
    polygon(draw, ((1390, 230), (1580, 270), (1660, 375), (1550, 492), (1330, 488)), ARMOR_3, width=7)
    red_slit(draw, (1036, 354, 1170, 382))
    seam(draw, ((1240, 370), (1360, 428), (1490, 390)), width=8)
    seam(draw, ((1470, 246), (1580, 282)), width=6)

    board_text(draw, (28, 622), "三条轮廓的结构关系（均为闭合态，不绘制核心）", 22, INK, bold=True)
    x_positions = (28, 616, 1204)
    accents = (RED, TEAL, GOLD)
    for candidate, x0, accent in zip(CANDIDATES, x_positions, accents):
        panel(draw, (x0, 662, x0 + 568, 1068), outline=accent, width=3)
        board_text(draw, (x0 + 20, 682), f"{candidate.code}｜{candidate.title}", 20, INK, bold=True)
        diagram = relation_diagram(candidate).resize((520, 260), Image.Resampling.LANCZOS)
        board.alpha_composite(diagram, (x0 + 20, 728))
        wrap_text(draw, (x0 + 20, 996, x0 + 548, 1054), candidate.red_relation, 14, INK, bold=True)

    path = OUT / "BREAKER_B1_surface_relation_board_1800x1100.png"
    board.convert("RGB").save(path)
    return path


def write_candidate_spec() -> Path:
    path = OUT / "candidate-spec.tsv"
    fields = (
        "candidate_id", "code", "silhouette_direction", "world_scale", "footprint", "default_facing",
        "footprint_anchor", "sprite_pivot", "ground_center_96", "ground_center_128", "head_red_slit",
        "chest_seam", "core_exit", "drill_read", "charge_read", "double_claws", "surface_language",
        "idle_move_brace_impact_space", "lifecycle", "runtime_allowed",
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for candidate in CANDIDATES:
            writer.writerow(
                {
                    "candidate_id": candidate.stable_id,
                    "code": candidate.code,
                    "silhouette_direction": candidate.title,
                    "world_scale": "near_30m;larger_than_18m_guardian_z",
                    "footprint": "3x3_locked",
                    "default_facing": "north_three_quarter",
                    "footprint_anchor": "north_west_cell",
                    "sprite_pivot": "bottom_center",
                    "ground_center_96": "(48,87)",
                    "ground_center_128": "(64,116)",
                    "head_red_slit": "single_visible_red_slit;impact_emission_direction",
                    "chest_seam": "closed_dark_structure_seam;not_weakpoint",
                    "core_exit": "closed_upper_back_hatch;core_not_visible",
                    "drill_read": "four_limbs_tighten_into_giant_drill",
                    "charge_read": "lowered_head_heavy_siege_charge",
                    "double_claws": "present;future_E03_grab_capacity_only",
                    "surface_language": "unresolved_user_decision_mechanical_vs_alien",
                    "idle_move_brace_impact_space": candidate.action_note,
                    "lifecycle": "candidate_direction_sample",
                    "runtime_allowed": "false",
                }
            )
    return path


def write_source_receipt(source_bytes: dict[str, bytes]) -> Path:
    path = OUT / "source-validation-receipt.tsv"
    fields = (
        "input_id", "authority_role", "contract_commit_or_snapshot", "source_path", "expected_sha256",
        "actual_sha256", "validation", "runtime_allowed",
    )
    roles = {
        TASK_PATH: "unique_B1_objective",
        PARENT_PATH: "G1_5_parent_contract",
        APPROVAL_PATH: "A1_C_user_approval_receipt",
        BUILD_CONTRACT_PATH: "frozen_demo_contract",
        VISUAL_SNAPSHOT_PATH: "frozen_visual_snapshot_context",
        AUTHORITY_PATH: "machine_authority_manifest",
        ENTITIES_PATH: "working_BREAKER_text_identity",
        ART_LOCKS_PATH: "art_lock_table_no_BREAKER_row",
        REBASE_PATH: "working_canon_migration_source",
        OUTLINE_PATH: "C01_story_action_source",
        GZ_C96_PATH: "approved_GZ_C_scale_anchor_96",
        GZ_C128_PATH: "approved_GZ_C_scale_anchor_128",
        GZ_BOARD_PATH: "approved_GZ_C_parent_board",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for index, source_path in enumerate(SOURCE_LOCKS, start=1):
            expected_sha = SOURCE_LOCKS[source_path][1]
            validation = "match_from_contract_commit"
            if source_path == AUTHORITY_PATH:
                validation += ";ENEMY_C01_BREAKER=working_active"
            elif source_path == ART_LOCKS_PATH:
                validation += ";BREAKER_art_lock=absent"
            elif source_path == APPROVAL_PATH:
                validation += ";A1_C=direction_approved_for_derivative_design"
            writer.writerow(
                {
                    "input_id": f"B1SRC{index:02d}",
                    "authority_role": roles[source_path],
                    "contract_commit_or_snapshot": CONTRACT_COMMIT,
                    "source_path": source_path,
                    "expected_sha256": expected_sha,
                    "actual_sha256": sha256_bytes(source_bytes[source_path]),
                    "validation": validation,
                    "runtime_allowed": "false",
                }
            )
    return path


def write_user_decision_card() -> Path:
    path = OUT / "user-decision-card.md"
    path.write_text(
        """# C01E02 G1.5-B1 BREAKER 用户裁决卡

> Status: `awaiting_individual_user_decision`
>
> 本轮全部为 `Candidate / runtime_allowed=false`；不会自动进入 B2 或主程序。

## 1. 主轮廓

- `A 低伏攻城楔型`
- `B 前肢承重半直立型`
- `C 装甲舱壳兽型`
- 或：选定路线但按意见修改 / 全部重做 / 仅参考

## 2. 表面语言

- `M 机械攻城壳`
- `X 异质/生体装甲`
- 或：指定比例融合，例如 `M70/X30`

## 3. 三处结构关系

请确认头部红缝、闭合胸缝与封闭上背核心出口是否清楚，并且没有提前泄露 E03。可按 A/B/C 任一路线单独提出修改。

未获得这三项明确回复前，本任务停止，不开始 B2 重盾。
""",
        encoding="utf-8",
    )
    return path


def write_manifest(files: list[tuple[str, Path, str, str, str]]) -> tuple[Path, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    for asset_id, path, kind, lifecycle, notes in files:
        if path.suffix.lower() == ".png":
            with Image.open(path) as image:
                dimensions = f"{image.width}x{image.height}"
        else:
            dimensions = "n/a"
        rows.append(
            {
                "asset_id": asset_id,
                "path": path.name,
                "type": kind,
                "dimensions_or_format": dimensions,
                "source_ids": "ENEMY_C01_BREAKER_WORKING;G15_A1_C_SCALE_ONLY;TASK_16",
                "parent_slot": "ENEMY_C01CDV1_BREAKER_GROUND",
                "lifecycle": lifecycle,
                "status": "awaiting_individual_user_decision" if "candidate" in lifecycle else "complete",
                "sha256": sha256_file(path),
                "runtime_allowed": "false",
                "notes": notes,
            }
        )
    manifest = OUT / "asset-manifest.tsv"
    fields = (
        "asset_id", "path", "type", "dimensions_or_format", "source_ids", "parent_slot", "lifecycle",
        "status", "sha256", "runtime_allowed", "notes",
    )
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return manifest, rows


def write_completion_report(manifest: Path, rows: list[dict[str, str]]) -> Path:
    path = OUT / "completion-report.md"
    path.write_text(
        f"""# C01E02 G1.5-B1 BREAKER 地面壳方向板交付

> Status: `candidate_direction_board_complete / awaiting_individual_user_decision / B2_locked`
>
> Runtime: `runtime_allowed=false`

## 权威结论

- 唯一任务提交：`{CONTRACT_COMMIT}`
- Demo fingerprint：`{CONTENT_FINGERPRINT}`
- `ENEMY_C01_BREAKER`：`Working / active` 文字身份。
- BREAKER 当前没有美术锁；三案均为 Candidate，不得冒充 Current 或 Runtime。
- 馆守 Z 仅使用用户已批准的 A1-C 96/128 文件做 18m、2×2 尺度对照，不构成 Godot handoff。

## 本轮交付

- 总判断板 1 张、单路线身份页 3 张、表面/结构关系裁决板 1 张。
- A/B/C 各 96×96 与 128×128 透明原生样张，共 6 张；它们不是最终 Sprite Master 或 Sprite Sheet。
- 每案包含正面、严格侧面、朝北三分之四、钻地、低伏冲撞、3×3 footprint、anchor/pivot、馆守 Z C 尺度对照与动作扩展说明。
- `{manifest.name}` 共 `{len(rows)}` 行，全部 `runtime_allowed=false`。

## 设计边界

- 三案都保留近30m黑甲重壳、头部单红缝、闭合胸缝、双爪、收肢钻地和低伏冲撞。
- 上背只画封闭出口；不显示核心、薄翼、胸部亮红裂、破甲洞或 E03 状态。
- 表面语言暂以中性机械/异质大色块表达，机械攻城壳与异质/生体装甲仍留给用户单独裁决。
- 未调用 ImageGen、LibTV、视频或付费/批量生成；未写 Godot、Canon、玩法、footprint 或 Runtime。

## 停止门

请用户分别选择：

1. `A 低伏攻城楔`、`B 前肢承重半直立` 或 `C 装甲舱壳兽`；
2. `M 机械攻城壳`、`X 异质/生体装甲` 或明确融合比例；
3. 头部红缝、闭合胸缝与封闭上背出口的关系是否通过，或需要怎样修改。

在三项明确回复前停止，不开始 B2，不向主程序交接。
""",
        encoding="utf-8",
    )
    return path


def write_delivery_hashes() -> Path:
    path = OUT / "delivery-hashes.sha256"
    lines = []
    for item in sorted(OUT.iterdir(), key=lambda value: value.name):
        if item.is_file() and item.name != path.name and not item.name.startswith("."):
            lines.append(f"{sha256_file(item)}  {item.name}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    source_bytes, _ = validate_authority()
    gz96 = Image.open(io.BytesIO(source_bytes[GZ_C96_PATH])).convert("RGBA")

    sprites: dict[tuple[str, int], Image.Image] = {}
    sprite_paths: dict[tuple[str, int], Path] = {}
    for candidate in CANDIDATES:
        for size in (96, 128):
            sprite = native_sprite(candidate, size)
            path = OUT / f"BREAKER_B1_candidate_{candidate.code}_{size}.png"
            sprite.save(path)
            sprites[(candidate.code, size)] = sprite
            sprite_paths[(candidate.code, size)] = path

    direction_board = generate_direction_board(sprites, gz96)
    candidate_sheets = [generate_candidate_sheet(candidate, sprites, gz96) for candidate in CANDIDATES]
    surface_board = generate_surface_relation_board()
    candidate_spec = write_candidate_spec()
    source_receipt = write_source_receipt(source_bytes)
    decision_card = write_user_decision_card()

    files: list[tuple[str, Path, str, str, str]] = [
        ("G15_B1_BREAKER_DIRECTION_BOARD", direction_board, "png", "candidate_direction_board", "three controlled silhouette directions; no selection implied"),
        ("G15_B1_BREAKER_SURFACE_RELATION_BOARD", surface_board, "png", "candidate_decision_board", "mechanical vs alien surface axis and closed three-point relation"),
    ]
    for candidate, sheet in zip(CANDIDATES, candidate_sheets):
        files.append((f"{candidate.stable_id}_IDENTITY_SHEET", sheet, "png", "candidate_identity_sheet", "front;strict side;north 3q;drill;charge;footprint;scale;actions"))
        for size in (96, 128):
            files.append((f"{candidate.stable_id}_{size}", sprite_paths[(candidate.code, size)], "png_rgba", "candidate_qsd_scale_sample", f"transparent {size}px sample;not sprite master;bottom_center pivot"))
    files.extend(
        [
            ("G15_B1_BREAKER_CANDIDATE_SPEC", candidate_spec, "tsv", "candidate_design_evidence", "3x3;north_west_cell;bottom_center;action-space metadata"),
            ("G15_B1_SOURCE_VALIDATION_RECEIPT", source_receipt, "tsv", "validation_evidence", "Working identity, absent art lock, A1-C approval and hashes"),
            ("G15_B1_USER_DECISION_CARD", decision_card, "md", "decision_gate", "B2 remains locked pending three explicit user decisions"),
            ("G15_B1_GENERATOR_SOURCE", Path(__file__), "python", "reproducibility_evidence", "procedural KINETIC_CEL candidates;no ImageGen or LibTV"),
        ]
    )
    manifest, manifest_rows = write_manifest(files)
    report = write_completion_report(manifest, manifest_rows)
    hashes = write_delivery_hashes()

    print(f"Generated {direction_board.name}")
    print(f"Candidate sheets: {len(candidate_sheets)}")
    print(f"Transparent samples: {len(sprite_paths)}")
    print(f"Manifest rows: {len(manifest_rows)}")
    print(f"Completion report: {report.name}")
    print(f"Delivery hashes: {hashes.name}")
    print(f"Contract commit: {CONTRACT_COMMIT}")
    print(f"Content fingerprint: {CONTENT_FINGERPRINT}")


if __name__ == "__main__":
    main()
