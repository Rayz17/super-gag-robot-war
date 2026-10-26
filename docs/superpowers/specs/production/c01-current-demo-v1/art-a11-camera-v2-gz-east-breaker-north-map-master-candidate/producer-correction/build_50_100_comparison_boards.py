#!/usr/bin/env python3
"""Create additive 50/100 review boards from existing pixels only.

No ImageGen, alpha extraction, repaint, geometry completion, or subject-pixel
modification occurs here. Operations are crop, deterministic resize, layout,
labels, and readback metrics.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent

GF_PLAN = Path("/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-a9-gold-frame/delivery/GF_PLAN_1280x720_v2.png")
GF_CONTACT = Path("/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-a9-gold-frame/delivery/GF_CONTACT_1280x720_v2.png")
GZ_RAW = PACKAGE / "generation-raw/GZ_EAST_CALL01_RAW.png"
BREAKER_RAW = PACKAGE / "generation-raw/BREAKER_NORTH_CALL01_RAW.png"

FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
PLAN_BREAKER_BOX = (233, 330, 591, 584)      # half-open; scene occlusion retained
CONTACT_BREAKER_BOX = (355, 136, 781, 487)  # half-open; GZ/FX occlusion retained


def font(size: int):
    return ImageFont.truetype(FONT, size)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def place(canvas, image, xy, label, label_size=26, border=(98, 143, 166, 255)):
    x, y = xy
    canvas.alpha_composite(image.convert("RGBA"), (x, y))
    d = ImageDraw.Draw(canvas)
    d.rectangle((x - 2, y - 2, x + image.width + 1, y + image.height + 1), outline=border, width=2)
    d.text((x, y + image.height + 10), label, font=font(label_size), fill=(221, 232, 238, 255))


def scale_exact(image: Image.Image, size: tuple[int, int]):
    return image.resize(size, Image.Resampling.LANCZOS)


def conservative_subject_bbox(rgb: Image.Image):
    """Measure only; never used as a mask or crop for delivered raw panels."""
    a = np.asarray(rgb.convert("RGB"), dtype=np.int16)
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    # Baked checkerboard is near-white neutral; colored/dark subject is conservative foreground.
    fg = (mn < 218) | ((mx - mn) > 28)
    ys, xs = np.where(fg)
    if not len(xs):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]


def breaker_board():
    plan = Image.open(GF_PLAN).convert("RGBA")
    contact = Image.open(GF_CONTACT).convert("RGBA")
    raw = Image.open(BREAKER_RAW).convert("RGBA")
    plan_crop = plan.crop(PLAN_BREAKER_BOX)
    contact_crop = contact.crop(CONTACT_BREAKER_BOX)
    raw_100 = scale_exact(raw, (384, 384))
    raw_50 = scale_exact(raw_100, (192, 192))

    c = Image.new("RGBA", (2400, 1800), (9, 16, 22, 255))
    d = ImageDraw.Draw(c)
    d.text((54, 38), "BREAKER｜GF已确认设计 vs 本轮Camera V2 north raw", font=font(52), fill=(244, 247, 248, 255))
    d.text((56, 108), "用户纠偏：低伏四足/巨型叠壳本身不是否决项；只评GF忠实度、north、地图缩放与Candidate资格。", font=font(28), fill=(250, 194, 95, 255))

    d.text((56, 176), "GF PLAN（完整场景50%；主体原生像素crop 100% / 50%）", font=font(31), fill=(113, 205, 219, 255))
    place(c, scale_exact(plan, (640, 360)), (56, 226), "GF PLAN full frame 50%｜scene context only")
    place(c, plan_crop, (752, 226), "GF PLAN BREAKER crop 100%｜occlusion retained")
    place(c, scale_exact(plan_crop, (179, 127)), (1158, 226), "GF PLAN crop 50%")

    d.text((56, 670), "GF CONTACT（完整场景50%；主体原生像素crop 100% / 50%）", font=font(31), fill=(113, 205, 219, 255))
    place(c, scale_exact(contact, (640, 360)), (56, 720), "GF CONTACT full frame 50%｜scene context only")
    place(c, contact_crop, (752, 720), "GF CONTACT BREAKER crop 100%｜GZ/FX occlusion retained")
    place(c, scale_exact(contact_crop, (213, 176)), (1222, 720), "GF CONTACT crop 50%")

    d.text((56, 1196), "本轮raw（未抠图；棋盘格烘入RGB；按384目标全画布一次缩放）", font=font(31), fill=(113, 205, 219, 255))
    place(c, raw_100, (56, 1250), "RAW target-canvas 100% = 384×384｜NOT MASTER")
    place(c, raw_50, (500, 1250), "RAW 50% = 192×192", label_size=22)

    notes = [
        "纠偏评判：",
        "1  GF具体轮廓/表面：部分继承；壳片变宽圆，长叶叠压与前后节奏减弱。",
        "2  Camera V2 north：不成立；头/承力端首读偏左下，未锁定右上−30.96°。",
        "3  地图缩放：192px仍能读黑壳与红缝，纯可读性成立。",
        "4  临时Candidate：不足。原因是GF忠实度与north失败，不再以“像龟/四足”单独否决。",
        "结论：MUST_REDRAW_CAMERA_ADAPTATION；GF DESIGN REMAINS APPROVED。",
    ]
    y = 1260
    for i, line in enumerate(notes):
        d.text((780, y), line, font=font(30 if i else 34), fill=(239, 222, 198, 255) if i else (250, 194, 95, 255))
        y += 62 if i else 72

    out = HERE / "BREAKER_GF_VS_RAW_50_100_COMPARISON_2400x1800.png"
    c.convert("RGB").save(out, format="PNG", optimize=False, compress_level=9)
    return out, {
        "gf_plan_breaker_crop_half_open": list(PLAN_BREAKER_BOX),
        "gf_contact_breaker_crop_half_open": list(CONTACT_BREAKER_BOX),
        "raw_source_dimensions": list(raw.size),
        "raw_review_100_dimensions": [384, 384],
        "raw_review_50_dimensions": [192, 192],
        "raw_conservative_measurement_bbox_not_used_for_mask": conservative_subject_bbox(raw),
    }


def guardian_board():
    raw = Image.open(GZ_RAW).convert("RGBA")
    raw_100 = scale_exact(raw, (256, 256))
    raw_50 = scale_exact(raw_100, (128, 128))

    c = Image.new("RGBA", (1600, 1000), (9, 16, 22, 255))
    d = ImageDraw.Draw(c)
    d.text((52, 38), "馆守Z｜本轮east raw 50% / 100% 单体评审", font=font(48), fill=(244, 247, 248, 255))
    d.text((54, 104), "未抠图、未做pivot注册；棋盘格烘入RGB。只评身份、视角和目标缩放读法。", font=font(27), fill=(250, 194, 95, 255))
    place(c, raw_100, (70, 210), "100% target canvas = 256×256｜NOT MASTER", label_size=25)
    place(c, raw_50, (414, 210), "50% target canvas = 128×128", label_size=25)

    notes = [
        "身份：V10X/Q/SD冠、脸、红X胸、圆金核、肩环与圆柱前臂保留。",
        "E02：双臂、无翼、无背包、无武器成立。",
        "Camera V2 east：顶面可见，主体首读朝右下，方向基本成立。",
        "缩放：256可读；128仍读配色与重量，但脸部栅格和核心开始粘连。",
        "资格：LOOK_CANDIDATE_ONLY；因无alpha/pivot，不是地图MASTER或Runtime资产。",
    ]
    y = 215
    for line in notes:
        d.text((620, y), line, font=font(30), fill=(221, 232, 238, 255))
        y += 82

    out = HERE / "GUARDIAN_Z_RAW_50_100_REVIEW_1600x1000.png"
    c.convert("RGB").save(out, format="PNG", optimize=False, compress_level=9)
    return out, {
        "raw_source_dimensions": list(raw.size),
        "raw_review_100_dimensions": [256, 256],
        "raw_review_50_dimensions": [128, 128],
        "raw_conservative_measurement_bbox_not_used_for_mask": conservative_subject_bbox(raw),
    }


def main():
    b_path, b_data = breaker_board()
    g_path, g_data = guardian_board()
    receipt = {
        "operation_scope": ["crop", "deterministic_lanczos_resize", "layout", "text_labels", "measurement_only"],
        "imagegen_calls": 0,
        "rerolls": 0,
        "alpha_extraction": False,
        "godot_changes": 0,
        "sources": {
            "gf_plan": {"path": str(GF_PLAN), "sha256": sha(GF_PLAN)},
            "gf_contact": {"path": str(GF_CONTACT), "sha256": sha(GF_CONTACT)},
            "guardian_z_raw": {"path": str(GZ_RAW), "sha256": sha(GZ_RAW)},
            "breaker_raw": {"path": str(BREAKER_RAW), "sha256": sha(BREAKER_RAW)},
        },
        "outputs": {
            "breaker_board": {"path": str(b_path), "sha256": sha(b_path), **b_data},
            "guardian_z_board": {"path": str(g_path), "sha256": sha(g_path), **g_data},
        },
        "supersession": {
            "old_turtle_gate": "OVERRIDDEN_BY_LATER_USER_CONFIRMATION",
            "gf_design": "USER_CONFIRMED_CORRECT",
            "prior_record_preserved": True,
        },
    }
    (HERE / "correction-machine-readback.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
