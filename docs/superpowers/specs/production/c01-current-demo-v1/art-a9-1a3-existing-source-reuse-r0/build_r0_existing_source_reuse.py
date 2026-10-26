#!/usr/bin/env python3
"""Task 67 R0: mechanical reuse only.

This script validates frozen sources, makes byte-identical copies, creates
source/pivot annotations, thumbnails existing art, and alpha-composites the two
approved 128 px samples.  It does not draw, complete, or reconstruct mecha.
"""

from __future__ import annotations

import csv
import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / ".git").exists())
FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

GZ_EXACT_NAME = "GUARDIAN_Z_C128_APPROVED_EXACT.png"
BR_EXACT_NAME = "BREAKER_B128_APPROVED_EXACT.png"
MAP_NAME = "R0_EXISTING_APPROVED_SOURCES_ON_A4_MAP_1280x720.png"
ROLE_NAME = "R0_SOURCE_ROLE_BOARD_1920x1080.png"


@dataclass(frozen=True)
class Source:
    source_id: str
    subject: str
    authority_role: str
    lifecycle: str
    runtime_allowed: str
    relative_path: str
    expected_sha256: str
    allowed_use: str
    forbidden_use: str
    consumed_in_r0: str


SOURCES = (
    Source("GOV67", "package", "producer signed task authority", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/67-c01e02-a9-1a3-existing-approved-source-freeze-and-r0-reuse-proof.md", "2cba2466a135278245cf6ddda805d76d6943d0319cd41d43c8e748b0eeda55db", "R0 scope and source freeze", "Canon or Runtime migration", "validation"),
    Source("BOARD38", "package", "current production board", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv", "13637a61ee502cb7795a3c9e06c58e7eac211dc49777d9d542d933f0bab02ef3", "current production state", "treating R0 as final art", "validation"),
    Source("GZ_APPROVAL", "Guardian Z", "user approval receipt: C", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv", "9b87022bf58750324cf88a9dd01e36d438aee48d83c67169401a4ff08b24ecee", "prove user-selected C direction", "claim final Sprite Master or Runtime", "receipt only"),
    Source("GZ_CML008", "Guardian Z", "Hard identity responsibility source", "Hard", "false", ".superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png", "a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521", "identity crown face chest shoulder rings cylindrical forearms weight", "direct map scale or Candidate overwrite", "role board thumbnail"),
    Source("GZ_V10X", "Guardian Z", "E02 detail responsibility source", "Candidate", "false", "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png", "e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade", "two-arm naked E02 no wings no backpack local structure", "Canon Runtime promotion or CML008 change", "role board thumbnail"),
    Source("GZ_C128", "Guardian Z", "user-approved C map proportion and silhouette responsibility source", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png", "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e", "C silhouette 4.2-head proportion 2x2 foot-center pivot", "new A/B/C selection or proportion change", "exact byte copy; native 1:1 map composite; role board"),
    Source("GZ_Q_BOARD", "Guardian Z", "approved direction parent board", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png", "4d8e7975649b2b85458a838afd9bc2fe8e3a90fd8cbcfe8a7929b8ae9ae6c225", "explain selected C identity", "revive A/B as candidates", "role board thumbnail"),
    Source("GZ_A2_FOURVIEW", "Guardian Z", "Candidate main painting work layer", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a2-master-production-correction/delivery/GUARDIAN_Z_V10X_KINETIC_FOURVIEW_RGBA_2560x960.png", "cc75ed94a1676488d6b1f777775192893c8037b23e08a06f802b714bbfca5243", "local direction painting color line pressure", "inherit tall proportions or overwrite C silhouette", "role board thumbnail only"),
    Source("GZ_A_FOURVIEW", "Guardian Z", "Candidate supplementary painting work layer", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png", "3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9", "local side/rear detail and cleanup", "independent master or unclosed turnaround structure", "role board thumbnail only"),
    Source("GZ_A8_ACTION", "Guardian Z", "History motion and pivot evidence", "History", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b1-1/assets/atlases/R05_GUARDIAN_Z_SOUTH_ACTION_B1_1_1280x256.png", "720f23edc1e069b1cd9780f973fb9df84d423466800d796dcfb8ff8180e1ad59", "motion rhythm foot point pivot amplitude", "visible pixel reuse or visual promotion", "role board thumbnail only"),
    Source("BR_APPROVAL", "BREAKER", "user approval receipt: B plus X plus three relations", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv", "cf7f1c226f4da0c8e77d025faf264a4756dbc4ff279c26f56a99bcc85f043920", "prove user-selected B and X direction", "claim final Sprite Master or Runtime", "receipt only"),
    Source("BR_B_SHEET", "BREAKER", "user-approved B silhouette and topology responsibility source", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png", "7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868", "forelimb-bearing semi-upright short stabilizing rear legs 3x3 near30m north read", "A/C revival or turtle gorilla sled vehicle ordinary quadruped", "role board thumbnail"),
    Source("BR_B128", "BREAKER", "user-approved B map silhouette and pivot responsibility source", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png", "e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4", "B 128px silhouette center of gravity bottom-center pivot", "limb change or claim completed B plus X", "exact byte copy; native 1:1 map composite; role board"),
    Source("BR_X_BOARD", "BREAKER", "user-approved X surface and three-relation responsibility source", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png", "cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85", "alien bio-armor plus red slit closed chest seam sealed upper-back exit", "new body open core or relation change", "role board thumbnail"),
    Source("BR_A_MASTER", "BREAKER", "Candidate high-resolution local painting work layer", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/BREAKER_BX_GROUND_SHELL_MASTER_RGBA_1400.png", "cbeb1ecb18e9d1ed41dd96d939c56e1f00f0eeab3f1af6bd4ddca048e8e02113", "local shell plates dark material red slit forelimb paint", "inherit turtle/gorilla silhouette or whole shrink", "role board thumbnail only"),
    Source("BR_A2_MASTER", "BREAKER", "Candidate KINETIC_CEL painting-style work layer", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a2-master-production-correction/delivery/BREAKER_BX_NONANIMAL_KINETIC_MASTER_RGBA_1400.png", "b47ebc4a6b8538f23892229f5554ae6c33b066ac37cf7077a71399e6931fb89d", "hard color outline dark palette two shadows", "inherit sled/armored vehicle body or overwrite B", "role board thumbnail only"),
    Source("BR_A8_ACTION", "BREAKER", "History motion and pivot evidence", "History", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-a8-current-visual-pack/phase-b1-1/assets/atlases/R05_BREAKER_NORTH_ACTION_B1_1_960x320.png", "3d4b3f2e4cd07238a87fdf17b8d5756446709dccdd37dc5dc23905e52ad4f9f7", "idle charge contact rhythm thrust contact pivot", "visible pixel reuse or visual promotion", "role board thumbnail only"),
    Source("A4_VIEWPORT", "A4 map", "Candidate map review viewport", "Candidate", "false", "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_central_1280x720.png", "b8ccc9b6eefb802b929a6d674e668611c6d9a88e123e24a2991710ae7e5f4ea9", "R0 source-scale context", "event staging final art or Runtime claim", "map composite background"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def validate_sources() -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for source in SOURCES:
        if ".codex/generated_images" in source.relative_path or "sprite-first-master-pilot" in source.relative_path:
            raise RuntimeError(f"Forbidden source routed into R0: {source.relative_path}")
        path = ROOT / source.relative_path
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = sha256(path)
        if actual != source.expected_sha256:
            raise RuntimeError(f"Source hash mismatch: {source.source_id}: {actual}")
        resolved[source.source_id] = path
    return resolved


def alpha_metrics(path: Path) -> tuple[tuple[int, int, int, int], int]:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        bbox = alpha.getbbox()
        if bbox is None:
            raise RuntimeError(f"Empty alpha source: {path}")
        return bbox, sum(1 for value in alpha.getdata() if value)


def write_receipt(paths: dict[str, Path]) -> None:
    with (HERE / "source-freeze-receipt.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source_id", "subject", "authority_role", "lifecycle", "runtime_allowed", "project_relative_path", "absolute_path", "expected_sha256", "actual_sha256", "hash_check", "allowed_use", "forbidden_use", "consumed_in_r0"))
        for source in SOURCES:
            path = paths[source.source_id]
            actual = sha256(path)
            writer.writerow((source.source_id, source.subject, source.authority_role, source.lifecycle, source.runtime_allowed, source.relative_path, str(path), source.expected_sha256, actual, "PASS", source.allowed_use, source.forbidden_use, source.consumed_in_r0))


def draw_diamond(draw: ImageDraw.ImageDraw, center: tuple[int, int], cells: int, color: tuple[int, int, int, int]) -> None:
    x, y = center
    half_w, half_h = 40 * cells, 20 * cells
    points = ((x, y - half_h), (x + half_w, y), (x, y + half_h), (x - half_w, y))
    draw.polygon(points, fill=(color[0], color[1], color[2], 34))
    draw.line((*points, points[0]), fill=color, width=3, joint="curve")


def make_map(paths: dict[str, Path]) -> None:
    base = Image.open(paths["A4_VIEWPORT"]).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    draw.rectangle((0, 0, 1280, 66), fill=(5, 13, 19, 235))
    draw.rectangle((0, 648, 1280, 720), fill=(5, 13, 19, 238))
    draw.text((24, 14), "R0 EXISTING APPROVED SOURCES ON A4 MAP", font=font(27, True), fill=(245, 247, 239, 255))
    draw.text((760, 20), "source scale proof / not event staging / not final art", font=font(19, True), fill=(255, 200, 82, 255))

    gz_anchor = (382, 434)
    br_anchor = (688, 505)
    draw_diamond(draw, gz_anchor, 2, (82, 205, 232, 235))
    draw_diamond(draw, br_anchor, 3, (255, 184, 64, 235))
    draw.ellipse((gz_anchor[0] - 4, gz_anchor[1] - 4, gz_anchor[0] + 4, gz_anchor[1] + 4), fill=(82, 205, 232, 255))
    draw.ellipse((br_anchor[0] - 4, br_anchor[1] - 4, br_anchor[0] + 4, br_anchor[1] + 4), fill=(255, 184, 64, 255))
    base = Image.alpha_composite(base, overlay)

    gz = Image.open(paths["GZ_C128"]).convert("RGBA")
    br = Image.open(paths["BR_B128"]).convert("RGBA")
    if gz.size != (128, 128) or br.size != (128, 128):
        raise RuntimeError("Exact samples are not 128x128")
    # GZ has no numeric pivot in its manifest; (64,127) is the alpha-bbox bottom-center inference.
    base.alpha_composite(gz, (gz_anchor[0] - 64, gz_anchor[1] - 127))
    # BREAKER candidate-spec.tsv explicitly fixes ground_center_128=(64,116).
    base.alpha_composite(br, (br_anchor[0] - 64, br_anchor[1] - 116))

    labels = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(labels, "RGBA")
    draw.rounded_rectangle((250, 250, 515, 304), radius=8, fill=(4, 10, 15, 220), outline=(82, 205, 232, 255), width=2)
    draw.text((265, 260), "馆守Z C128 · native 1:1", font=font(19, True), fill=(235, 250, 255, 255))
    draw.text((265, 283), "2×2 · pivot (64,127)*", font=font(15), fill=(162, 229, 242, 255))
    draw.rounded_rectangle((548, 323, 835, 377), radius=8, fill=(4, 10, 15, 220), outline=(255, 184, 64, 255), width=2)
    draw.text((563, 333), "BREAKER B128 · native 1:1", font=font(19, True), fill=(255, 247, 222, 255))
    draw.text((563, 356), "3×3 · pivot (64,116) spec", font=font(15), fill=(255, 213, 129, 255))
    draw.rounded_rectangle((914, 77, 1258, 203), radius=8, fill=(8, 15, 22, 238), outline=(238, 93, 84, 255), width=2)
    draw.text((934, 93), "NATIVE 128 LIMIT EXPOSED", font=font(20, True), fill=(255, 220, 214, 255))
    draw.multiline_text((934, 124), "Both source canvases are 128×128.\nB is not clearly larger at native 1:1.\nScale calibration remains deferred.", font=font(16), fill=(235, 240, 240, 255), spacing=5)
    draw.multiline_text((24, 661), "* GZ pivot integer is derived from alpha-bbox bottom edge; source manifest says foot-center but provides no numeric coordinate.\nNo scaling, stretching, paint-over, sprite outline, or event-position claim was applied.", font=font(16), fill=(225, 234, 236, 255), spacing=4)
    Image.alpha_composite(base, labels).convert("RGB").save(HERE / MAP_NAME, optimize=False)


def place_thumb(board: Image.Image, path: Path, box: tuple[int, int, int, int], *, native: bool = False) -> None:
    x0, y0, x1, y1 = box
    image = Image.open(path).convert("RGBA")
    if native:
        if image.size[0] > x1 - x0 or image.size[1] > y1 - y0:
            raise RuntimeError(f"Native thumbnail box too small: {path}")
        thumb = image
    else:
        thumb = ImageOps.contain(image, (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    x = x0 + ((x1 - x0) - thumb.width) // 2
    y = y0 + ((y1 - y0) - thumb.height) // 2
    board.alpha_composite(thumb, (x, y))


def make_role_board(paths: dict[str, Path]) -> None:
    board = Image.new("RGBA", (1920, 1080), (9, 16, 24, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 1920, 92), fill=(18, 30, 42, 255))
    draw.text((42, 18), "R0 SOURCE ROLE BOARD · EXISTING APPROVED SOURCE REUSE", font=font(31, True), fill=(247, 245, 232, 255))
    draw.text((42, 58), "priority: approved responsibility sources > Candidate painting layers > History motion/pivot evidence · runtime_allowed=false", font=font(18), fill=(164, 194, 210, 255))

    # Section backgrounds and lane dividers are annotations only.
    for box, color in (((30, 106, 1890, 463), (29, 48, 62, 255)), ((30, 478, 1890, 797), (24, 38, 49, 255)), ((30, 812, 1890, 1053), (19, 31, 41, 255))):
        draw.rounded_rectangle(box, radius=12, fill=color, outline=(75, 104, 120, 255), width=2)
    draw.line((960, 142, 960, 1040), fill=(75, 104, 120, 255), width=2)
    draw.text((52, 117), "1 · APPROVED / CANON RESPONSIBILITY SOURCES — LOCKS THE BODY", font=font(22, True), fill=(255, 207, 94, 255))
    draw.text((52, 490), "2 · CANDIDATE PAINTING WORK LAYERS — LOCAL PIXELS ONLY", font=font(22, True), fill=(107, 204, 232, 255))
    draw.text((52, 824), "3 · HISTORY ACTION EVIDENCE — MOTION / PIVOT ONLY", font=font(22, True), fill=(176, 154, 214, 255))
    draw.text((52, 151), "馆守 Z", font=font(24, True), fill=(130, 218, 240, 255))
    draw.text((982, 151), "BREAKER", font=font(24, True), fill=(255, 188, 87, 255))

    approved_cards = (
        ("GZ_CML008", (52, 184, 238, 326), "CML008 Hard\n锁：身份/头冠/脸\n胸/肩环/圆柱臂"),
        ("GZ_V10X", (250, 184, 436, 326), "V10X E02\n锁：双臂裸机\n无翼/无背包"),
        ("GZ_C128", (448, 184, 596, 326), "C128 原生\n锁：C约4.2头身\n2×2 / pivot"),
        ("GZ_Q_BOARD", (608, 184, 932, 326), "Q父板\n锁：C已选\nA/B不得回流"),
        ("BR_B_SHEET", (982, 184, 1265, 326), "B身份板\n锁：前肢承重半直立\n短后足 / 3×3"),
        ("BR_B128", (1277, 184, 1425, 326), "B128 原生\n锁：B轮廓/重心\nbottom-center pivot"),
        ("BR_X_BOARD", (1437, 184, 1868, 326), "X关系板\n锁：异质生体甲\n红缝/闭胸缝/封出口"),
    )
    for source_id, box, label in approved_cards:
        draw.rounded_rectangle(box, radius=7, fill=(5, 12, 18, 255), outline=(93, 122, 139, 255), width=2)
        place_thumb(board, paths[source_id], (box[0] + 4, box[1] + 4, box[2] - 4, box[3] - 4), native=source_id in {"GZ_C128", "BR_B128"})
        draw.multiline_text((box[0], 334), label, font=font(13, True), fill=(231, 237, 236, 255), spacing=2)
    draw.text((52, 421), "不能改：CML008识别点、E02双臂裸机、C身体比例与四肢大形。", font=font(17, True), fill=(255, 145, 135, 255))
    draw.text((982, 421), "不能改：B身体/承重拓扑；不得龟、猿、雪橇、车辆或普通四足；不得打开核心。", font=font(17, True), fill=(255, 145, 135, 255))

    draw.text((52, 527), "馆守 Z · 只捐配色/线压/侧背局部；禁止继承高身比或整体缩小", font=font(17, True), fill=(210, 235, 241, 255))
    draw.text((982, 527), "BREAKER · 只捐壳片/暗色/红缝/硬色块；禁止继承龟猿或雪橇车体", font=font(17, True), fill=(247, 226, 190, 255))
    candidate_cards = (
        ("GZ_A2_FOURVIEW", (52, 560, 477, 718), "A9.1-A2 fourview · local painting donor"),
        ("GZ_A_FOURVIEW", (489, 560, 932, 718), "A9.1-A fourview · side/rear cleanup donor"),
        ("BR_A_MASTER", (982, 560, 1410, 718), "A9.1-A · local shell/material donor"),
        ("BR_A2_MASTER", (1422, 560, 1868, 718), "A9.1-A2 · KINETIC_CEL style donor"),
    )
    for source_id, box, label in candidate_cards:
        draw.rounded_rectangle(box, radius=7, fill=(5, 12, 18, 255), outline=(76, 143, 166, 255), width=2)
        place_thumb(board, paths[source_id], (box[0] + 5, box[1] + 5, box[2] - 5, box[3] - 5))
        draw.text((box[0], 730), label, font=font(15, True), fill=(224, 233, 234, 255))
    draw.text((52, 763), "Candidate work layers cannot become whole-body masters and cannot override the approved silhouettes.", font=font(16), fill=(155, 184, 197, 255))

    draw.text((52, 860), "馆守 Z A8 · idle / step_a / step_b / brace / recoil", font=font(17, True), fill=(207, 191, 231, 255))
    draw.text((982, 860), "BREAKER A8 · idle / charge / contact", font=font(17, True), fill=(207, 191, 231, 255))
    place_thumb(board, paths["GZ_A8_ACTION"], (52, 894, 932, 1005))
    place_thumb(board, paths["BR_A8_ACTION"], (982, 894, 1868, 1005))
    draw.text((52, 1015), "VISIBLE PIXELS FORBIDDEN · rhythm / foot point / pivot / amplitude only", font=font(16, True), fill=(255, 136, 128, 255))
    draw.text((982, 1015), "VISIBLE PIXELS FORBIDDEN · thrust / contact / pivot only", font=font(16, True), fill=(255, 136, 128, 255))
    board.convert("RGB").save(HERE / ROLE_NAME, optimize=False)


def write_report(paths: dict[str, Path]) -> None:
    gz_bbox, gz_area = alpha_metrics(paths["GZ_C128"])
    br_bbox, br_area = alpha_metrics(paths["BR_B128"])
    gz_w, gz_h = gz_bbox[2] - gz_bbox[0], gz_bbox[3] - gz_bbox[1]
    br_w, br_h = br_bbox[2] - br_bbox[0], br_bbox[3] - br_bbox[1]
    report = f"""# Task 67 R0 completion report

Status: `R0 mechanical reuse evidence delivered / Candidate only / runtime_allowed=false / producer visual review required`

## Delivered proof

- `GUARDIAN_Z_C128_APPROVED_EXACT.png`: exact byte copy; SHA-256 `{sha256(HERE / GZ_EXACT_NAME)}`.
- `BREAKER_B128_APPROVED_EXACT.png`: exact byte copy; SHA-256 `{sha256(HERE / BR_EXACT_NAME)}`.
- `{MAP_NAME}`: A4 central viewport plus only the two exact 128 samples at native 1:1; labels and footprint/pivot annotations are review evidence, not event positions.
- `{ROLE_NAME}`: mechanical thumbnail layout of responsibility sources, Candidate painting layers, and History action evidence.
- `source-freeze-receipt.tsv`: every consumed governance, visual, approval, and map source with path, expected/actual SHA, authority role, allowed use, and forbidden use.

## Exact-copy and pivot checks

- Guardian Z source/output SHA match: `PASS`; 128×128 RGBA; alpha bbox `{gz_bbox}` (right/bottom exclusive), {gz_w}×{gz_h}, {gz_area} nonzero-alpha pixels.
- BREAKER source/output SHA match: `PASS`; 128×128 RGBA; alpha bbox `{br_bbox}` (right/bottom exclusive), {br_w}×{br_h}, {br_area} nonzero-alpha pixels.
- Guardian Z source manifest states `foot-center pivot` but has no integer coordinate. R0 uses `(64,127)` derived from the alpha-bbox bottom edge and labels that inference; it is not presented as a source-spec value.
- BREAKER source `candidate-spec.tsv` explicitly states `bottom_center` and `ground_center_128=(64,116)`; R0 uses that coordinate.

## Native 1:1 scale finding

`native_1x_30m_18m_scale_proven=false`

Both approved samples are fixed 128×128 canvases. At native 1:1, BREAKER is only {br_w}px wide vs Guardian Z {gz_w}px, and is {br_h}px high vs Guardian Z {gz_h}px. It therefore does **not** visibly prove the near-30m/18m relationship. Per Task 67 §4.4, R0 did not stretch, rescale, redraw, outline, or reconstruct either sample to force a pass.

`scale_gate=DEFERRED_NOT_PROVEN`

`next_round_target_display_size=pending_producer_calibration`

The 2×2/3×3 diamonds only annotate approved footprint responsibilities. They do not repair the display-size gap and do not claim actual event staging.

## Zero-operation attestation

- ImageGen calls: `0`
- Blender calls: `0`
- new identity/body design: `0`
- visible mecha pixel drawing, completion, paint-over, outline, or reconstruction: `0`
- reads from `.codex/generated_images`: `0`
- execution/modification of `build_p0_sprite_first_evidence.py`: `0`
- Godot/Atlas/Runtime/LibTV/Canon migration: `0`
- git add/commit: `0`

Machine checks do not constitute visual approval. Work stops at the producer R0 PNG review gate.
"""
    (HERE / "completion-report.md").write_text(report, encoding="utf-8")


def write_hashes() -> None:
    names = (
        BR_EXACT_NAME,
        GZ_EXACT_NAME,
        MAP_NAME,
        ROLE_NAME,
        "build_r0_existing_source_reuse.py",
        "completion-report.md",
        "source-freeze-receipt.tsv",
    )
    lines = [f"{sha256(HERE / name)}  {name}" for name in sorted(names)]
    (HERE / "delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    paths = validate_sources()
    shutil.copyfile(paths["GZ_C128"], HERE / GZ_EXACT_NAME)
    shutil.copyfile(paths["BR_B128"], HERE / BR_EXACT_NAME)
    if sha256(HERE / GZ_EXACT_NAME) != SOURCES[5].expected_sha256:
        raise RuntimeError("Guardian Z exact-copy hash mismatch")
    if sha256(HERE / BR_EXACT_NAME) != SOURCES[12].expected_sha256:
        raise RuntimeError("BREAKER exact-copy hash mismatch")
    write_receipt(paths)
    make_map(paths)
    make_role_board(paths)
    write_report(paths)
    write_hashes()
    print(f"R0 outputs written under: {HERE}")
    print(f"Guardian exact: {sha256(HERE / GZ_EXACT_NAME)}")
    print(f"BREAKER exact: {sha256(HERE / BR_EXACT_NAME)}")
    print("Scale gate: DEFERRED_NOT_PROVEN")


if __name__ == "__main__":
    main()
