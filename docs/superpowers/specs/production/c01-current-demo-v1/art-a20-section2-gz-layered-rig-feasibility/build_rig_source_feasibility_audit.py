from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[5]
GZ = PROJECT / ".superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png"
SHIELD = (
    PROJECT
    / "docs/superpowers/specs/production/c01-current-demo-v1"
    / "art-a17-section2-true-retired-heavy-shield-candidate"
    / "user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png"
)

OUT = ROOT / "qa/RIG_SOURCE_FEASIBILITY_AUDIT_NOT_CANDIDATE_2400x1600.png"
OUT_HALF = ROOT / "qa/RIG_SOURCE_FEASIBILITY_AUDIT_NOT_CANDIDATE_1200x800.png"
AUDIT = ROOT / "qa/source-pixel-audit.json"

EXPECTED_GZ_SHA256 = "a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521"
EXPECTED_SHIELD_SHA256 = "169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305"

FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, light: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_LIGHT if light else FONT_MEDIUM, size=size)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fit(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = im.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    return copy


def checkerboard(size: tuple[int, int], cell: int = 24) -> Image.Image:
    bg = Image.new("RGB", size, "#E8E7E2")
    d = ImageDraw.Draw(bg)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#D6D5CF")
    return bg


def alpha_crop(im: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    view = im.crop(box)
    bbox = view.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError(f"empty alpha crop: {box}")
    return view.crop(bbox)


def labeled_card(
    canvas: Image.Image,
    xy: tuple[int, int],
    title: str,
    body: Image.Image,
    note: str,
) -> None:
    x, y = xy
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x, y, x + 252, y + 328), radius=16, fill="#F5F1E8", outline="#AFA99D", width=2)
    d.text((x + 14, y + 12), title, font=font(20), fill="#2B3030")
    d.rectangle((x + 12, y + 48, x + 240, y + 276), fill="#252B2C")
    card = body.copy()
    card.thumbnail((224, 224), Image.Resampling.LANCZOS)
    if card.mode == "RGBA":
        px = x + 14 + (224 - card.width) // 2
        py = y + 50 + (224 - card.height) // 2
        canvas.paste(card, (px, py), card)
    else:
        px = x + 14 + (224 - card.width) // 2
        py = y + 50 + (224 - card.height) // 2
        canvas.paste(card, (px, py))
    d.text((x + 14, y + 286), note, font=font(16, True), fill="#9B3C35")


def make_cell_source(gz: Image.Image) -> Image.Image:
    cell = Image.new("RGB", (256, 256), "#252B2C")
    crop = gz.crop((285, 25, 1100, 1254))
    crop.thumbnail((220, 244), Image.Resampling.LANCZOS)
    cell.paste(crop, ((256 - crop.width) // 2, 6))
    return cell


def make_cell_composite(gz: Image.Image, shield_front: Image.Image, bash: bool) -> Image.Image:
    cell = make_cell_source(gz).convert("RGBA")
    s = shield_front.copy()
    if bash:
        s = s.rotate(66, resample=Image.Resampling.BICUBIC, expand=True)
        s.thumbnail((206, 142), Image.Resampling.LANCZOS)
        pos = (24, 62)
    else:
        s.thumbnail((152, 194), Image.Resampling.LANCZOS)
        pos = (38, 38)
    cell.alpha_composite(s, pos)
    d = ImageDraw.Draw(cell)
    # These marks are QA callouts, not painted replacement pixels.
    d.ellipse((38, 116, 68, 146), outline="#FF5147", width=4)
    d.ellipse((182, 118, 212, 148), outline="#FF5147", width=4)
    d.line((52, 130, 82, 103), fill="#FF5147", width=3)
    d.line((198, 132, 170, 104), fill="#FF5147", width=3)
    return cell


gz_sha = sha256(GZ)
shield_sha = sha256(SHIELD)
if gz_sha != EXPECTED_GZ_SHA256:
    raise RuntimeError(f"CML008 source hash drift: {gz_sha}")
if shield_sha != EXPECTED_SHIELD_SHA256:
    raise RuntimeError(f"A17 source hash drift: {shield_sha}")

gz = Image.open(GZ)
shield = Image.open(SHIELD)
if gz.mode != "RGB" or gz.size != (1254, 1254):
    raise RuntimeError(f"unexpected CML008 pixels: mode={gz.mode} size={gz.size}")
if shield.mode != "RGBA" or shield.size != (1536, 1024):
    raise RuntimeError(f"unexpected A17 pixels: mode={shield.mode} size={shield.size}")

alpha = shield.getchannel("A")
alpha_hist = alpha.histogram()
front = alpha_crop(shield, (0, 0, 720, 1024))
back = alpha_crop(shield, (650, 0, 1305, 1024))
edge = alpha_crop(shield, (1270, 0, 1536, 1024))

canvas = Image.new("RGB", (2400, 1600), "#EEEAE1")
d = ImageDraw.Draw(canvas)
d.rectangle((0, 0, 2400, 126), fill="#22292A")
d.text((54, 22), "馆守 Z 分层 2D 来源可行性审计", font=font(48), fill="#F6F0E4")
d.text((1680, 32), "RIG_SOURCE_AUDIT", font=font(25, True), fill="#D7C9B7")
d.text((1680, 66), "NOT CANDIDATE · NOT FOR GODOT", font=font(22), fill="#FF8C78")

panels = [(42, 154, 742, 1260), (770, 154, 1470, 1260), (1498, 154, 2358, 1260)]
for rect in panels:
    d.rounded_rectangle(rect, radius=20, fill="#FAF7F0", outline="#BFB7A9", width=3)

# Panel 1: CML008 source audit.
d.text((72, 178), "01·唯一馆守 Z 身份源", font=font(31), fill="#263032")
d.text((72, 219), "CML008 Hard · pixels only", font=font(20, True), fill="#5B6767")
gz_fit = fit(gz, (640, 640))
gx, gy = 72, 265
canvas.paste(gz_fit, (gx, gy))
scale_x = gz_fit.width / gz.width
scale_y = gz_fit.height / gz.height
for box, color in [
    ((285, 25, 1100, 1254), "#FF8B4A"),
    ((0, 270, 355, 605), "#54B9E6"),
    ((0, 600, 355, 920), "#54B9E6"),
]:
    x0, y0, x1, y1 = box
    d.rectangle(
        (gx + x0 * scale_x, gy + y0 * scale_y, gx + x1 * scale_x, gy + y1 * scale_y),
        outline=color,
        width=4,
    )
d.text((72, 930), "像素事实", font=font(25), fill="#273032")
facts1 = [
    "1254×1254 · RGB · 无 alpha",
    "单张压平的设定展示板",
    "主体与展馆背景 / 栏目 / 插图交叠",
    "主视图只有垂臂、张手的近正面姿势",
    "上臂、前臂、手、躯干在像素上相互遮挡",
]
yy = 970
for line in facts1:
    d.text((82, yy), "· " + line, font=font(20, True), fill="#454E4E")
    yy += 39
d.rounded_rectangle((72, 1170, 712, 1228), radius=12, fill="#F8DDD8")
d.text((91, 1184), "结论：不存在可直接拆出的身体 / 双臂 / 握手层", font=font(19), fill="#8A312B")

# Panel 2: A17 source audit.
d.text((800, 178), "02·唯一退役重盾源", font=font(31), fill="#263032")
d.text((800, 219), "A17 user-accepted Candidate · pixels only", font=font(20, True), fill="#5B6767")
checker = checkerboard((640, 430), 22)
shield_fit = fit(shield, (628, 418))
checker.paste(shield_fit, ((640 - shield_fit.width) // 2, (430 - shield_fit.height) // 2), shield_fit)
canvas.paste(checker, (800, 265))
d.rectangle((800, 265, 1440, 695), outline="#868278", width=2)
d.text((800, 728), "像素事实", font=font(25), fill="#273032")
facts2 = [
    "1536×1024 · RGBA",
    f"alpha extrema {alpha.getextrema()}",
    f"全透明 {alpha_hist[0]:,} px",
    "正面 / 背面 / 侧面空间分开",
    "可按 alpha 和裁切框独立取出三个盾视图",
    "背面双握把可用于绘制接触约束",
]
yy = 770
for line in facts2:
    d.text((810, yy), "· " + line, font=font(20, True), fill="#454E4E")
    yy += 39
d.rounded_rectangle((800, 1042, 1440, 1122), radius=12, fill="#DDEADB")
d.text((819, 1057), "结论：盾牌本体可拆层", font=font(21), fill="#2D6638")
d.text((819, 1085), "但它不能补出馆守 Z 的屈肘、握持与 south 视面", font=font(18, True), fill="#3D5941")
d.text((800, 1162), f"front {front.size} · back {back.size} · edge {edge.size}", font=font(18, True), fill="#5B6767")

# Panel 3: deterministic reuse ceiling.
d.text((1528, 178), "03·确定性复用上限", font=font(31), fill="#263032")
d.text((1528, 219), "crop + scale + rotate + occlusion only", font=font(20, True), fill="#5B6767")
source_cell = make_cell_source(gz)
block_cell = make_cell_composite(gz, front, bash=False)
bash_cell = make_cell_composite(gz, front, bash=True)
labeled_card(canvas, (1528, 264), "原始主体裁切", source_cell, "背景与人形不可分")
labeled_card(canvas, (1798, 264), "BLOCK 盖盾", block_cell, "手臂仍垂下，未握把")
labeled_card(canvas, (2068, 264), "BASH 旋盾", bash_cell, "无屈肘 / 扭身 / 接触")

d.text((1528, 628), "为什么不能进入 Candidate", font=font(27), fill="#8B332D")
reasons = [
    "• BLOCK 只能把盾盖在待机机体上；双手与背面握把没有像素接触。",
    "• BASH 旋转的只是盾；双臂、肩、腰、重心与脚步不会跟随。",
    "• 原始人形是近正面，不是 Camera V2 south [-40,+24] 的统一三四分轴。",
    "• 任何手工挖图都会同时挖走关节后方的躯干、背景或隐藏表面。",
]
yy = 680
for line in reasons:
    for wrapped in [line[:44], "   " + line[44:] if len(line) > 44 else ""]:
        if wrapped.strip():
            d.text((1538, yy), wrapped, font=font(19, True), fill="#424B4B")
            yy += 31
    yy += 8

d.rounded_rectangle((1528, 1040, 2328, 1198), radius=16, fill="#F6D9D4", outline="#C96E62", width=3)
d.text((1554, 1060), "GATE: INFEASIBLE_FROM_ALLOWED_PIXELS", font=font(24), fill="#8A302A")
d.text((1554, 1100), "可确定拆出：盾牌三视图", font=font(20, True), fill="#5B3834")
d.text((1554, 1136), "不可确定拆出：馆守 Z south 身体、双臂、握手、遮挡层", font=font(20, True), fill="#5B3834")

# Bottom decision strip.
d.rectangle((0, 1290, 2400, 1600), fill="#252C2D")
d.text((54, 1320), "工程裁决", font=font(33), fill="#F2ECE1")
d.text((240, 1324), "不做“伪分层 rig”；需 Section 2 补画 2 张固定关键姿势，程序再用位移 / 震动 / VFX 组合。", font=font(24, True), fill="#F0C7B8")
d.text((54, 1380), "BLOCK：Camera V2 south、双臂完整、双手正面握盾、弓步承冲、手-握把遮挡关系完整。", font=font(22), fill="#ECE5D9")
d.text((54, 1424), "BASH_CONTACT：同一 south 轴，躯干扭转、双肘屈曲、双手持盾缘 / 握把、前脚压地、铝边接触朝向敌方。", font=font(22), fill="#ECE5D9")
d.text((54, 1470), "交付时必须同时提供：256×256 RGBA、pivot [128,224]、无背景、视图轴与当前地图同源、两手接触放大图。", font=font(22), fill="#ECE5D9")
d.text((54, 1532), "RIG_TECHNICAL_PROOF_NOT_CANDIDATE · runtime=false · Canon=false · no Godot binding", font=font(20, True), fill="#AEB7B6")

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT)
canvas.resize((1200, 800), Image.Resampling.LANCZOS).save(OUT_HALF)

audit = {
    "status": "RIG_TECHNICAL_PROOF_NOT_CANDIDATE",
    "gate": "INFEASIBLE_FROM_ALLOWED_PIXELS",
    "runtime": False,
    "canon": False,
    "godot_binding": False,
    "camera_v2_south_screen_vector": [-40, 24],
    "sources": {
        "guardian_z": {
            "path": str(GZ.relative_to(PROJECT)),
            "sha256": gz_sha,
            "mode": gz.mode,
            "size": list(gz.size),
            "alpha": False,
            "authority": "CML008 Hard identity source",
        },
        "shield": {
            "path": str(SHIELD.relative_to(PROJECT)),
            "sha256": shield_sha,
            "mode": shield.mode,
            "size": list(shield.size),
            "alpha_extrema": list(alpha.getextrema()),
            "alpha_zero_pixels": alpha_hist[0],
            "alpha_partial_pixels": sum(alpha_hist[1:255]),
            "alpha_opaque_pixels": alpha_hist[255],
            "authority": "A17 user-accepted Candidate design base",
            "view_crop_sizes": {"front": list(front.size), "back": list(back.size), "edge": list(edge.size)},
        },
    },
    "deterministically_reusable": ["shield_front", "shield_back", "shield_edge"],
    "missing_for_block_bash": [
        "guardian_z_south_three_quarter_body_base",
        "left_upper_arm_south",
        "left_forearm_south_block_and_bash",
        "left_closed_grip_hand_with_handle_contact",
        "right_upper_arm_south",
        "right_forearm_south_block_and_bash",
        "right_closed_grip_hand_with_handle_contact",
        "shield_body_and_hand_occlusion_masks",
        "block_braced_leg_and_weight_shift",
        "bash_torso_twist_braced_leg_and_contact_edge",
    ],
    "outputs": {},
}
audit["outputs"][str(OUT.relative_to(ROOT))] = {"size": list(canvas.size), "sha256": sha256(OUT)}
audit["outputs"][str(OUT_HALF.relative_to(ROOT))] = {
    "size": [1200, 800],
    "sha256": sha256(OUT_HALF),
}
AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps(audit, ensure_ascii=False, indent=2))
