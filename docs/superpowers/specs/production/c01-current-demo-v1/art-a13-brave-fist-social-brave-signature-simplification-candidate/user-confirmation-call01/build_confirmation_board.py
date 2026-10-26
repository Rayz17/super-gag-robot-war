#!/usr/bin/env python3
"""Compose the single Section 2 user-confirmation board.

The ImageGen source sheet is kept intact.  This script only scales it as one
rectangle and adds deterministic labels/status panels around or over empty
backdrop areas.  It does not repaint any mecha pixels.
"""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
RAW = HERE / "BRAVE_FIST_SOCIAL_BRAVE_SIGNATURE_CALL01_RAW.png"
OUT = HERE / "BRAVE_FIST_SOCIAL_BRAVE_SIGNATURE_USER_CONFIRMATION_BOARD_2400x1840.png"
READBACK = HERE / "machine-readback.json"
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

W, H = 2400, 1840
BG = (7, 13, 18, 255)
PANEL = (17, 25, 32, 245)
WHITE = (240, 244, 247, 255)
MUTED = (171, 184, 194, 255)
ORANGE = (246, 156, 35, 255)
CYAN = (84, 202, 222, 255)
MINT = (106, 210, 176, 255)
RED = (255, 101, 96, 255)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def panel(draw: ImageDraw.ImageDraw, box, outline=MUTED, fill=PANEL, radius=18, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def tag(draw: ImageDraw.ImageDraw, xy, text: str, color) -> None:
    x, y = xy
    f = font(23)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.rounded_rectangle((x, y, x + tw + 34, y + th + 22), radius=13,
                           fill=(8, 15, 20, 232), outline=color, width=2)
    draw.text((x + 17, y + 9), text, font=f, fill=WHITE)


def multiline(draw: ImageDraw.ImageDraw, xy, lines, size=22, fill=WHITE, gap=12):
    x, y = xy
    f = font(size)
    line_h = size + gap
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=f, fill=fill)


def extract_black_silhouette(raw: Image.Image, crop_box, target_height: int = 128) -> Image.Image:
    """Extract the generated solid-black silhouette and normalize it to 128 px high."""
    crop = np.asarray(raw.crop(crop_box).convert("RGB"), dtype=np.uint8)
    mask = crop.mean(axis=2) < 12
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=bool)
    largest = []

    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            queue = deque([(y, x)])
            seen[y, x] = True
            component = []
            while queue:
                yy, xx = queue.popleft()
                component.append((yy, xx))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = yy + dy, xx + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        queue.append((ny, nx))
            if len(component) > len(largest):
                largest = component

    if not largest:
        raise SystemExit(f"no silhouette component found in {crop_box}")

    ys = [p[0] for p in largest]
    xs = [p[1] for p in largest]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    component_mask = np.zeros((h, w), dtype=np.uint8)
    for yy, xx in largest:
        component_mask[yy, xx] = 255

    # Fill small interior gaps so thumbnail evaluation is shape-only.
    inverse = component_mask == 0
    outside = np.zeros((h, w), dtype=bool)
    queue = deque()
    for x in range(w):
        for y in (0, h - 1):
            if inverse[y, x] and not outside[y, x]:
                outside[y, x] = True
                queue.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if inverse[y, x] and not outside[y, x]:
                outside[y, x] = True
                queue.append((y, x))
    while queue:
        yy, xx = queue.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = yy + dy, xx + dx
            if 0 <= ny < h and 0 <= nx < w and inverse[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True
                queue.append((ny, nx))
    filled = np.where(~outside, 255, 0).astype(np.uint8)
    alpha = Image.fromarray(filled[y0:y1 + 1, x0:x1 + 1], mode="L")
    target_width = max(1, round(alpha.width * target_height / alpha.height))
    alpha = alpha.resize((target_width, target_height), Image.Resampling.NEAREST)
    result = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
    result.paste((0, 0, 0, 255), (0, 0, alpha.width, alpha.height), alpha)
    return result


def main() -> None:
    raw = Image.open(RAW).convert("RGBA")
    if raw.size != (1536, 1024):
        raise SystemExit(f"unexpected raw size: {raw.size}")

    canvas = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # Header
    draw.rectangle((0, 0, W, 120), fill=(8, 15, 20, 255))
    draw.line((0, 118, W, 118), fill=ORANGE, width=4)
    draw.text((40, 20), "勇拳 → 社勇王｜特征简化 + 新英雄头 Candidate", font=font(44), fill=WHITE)
    draw.text((1572, 33), "SECTION 2｜USER FALSE｜RUNTIME FALSE｜CANON 未晋级",
              font=font(23), fill=CYAN)

    # Preserve the generated sheet as a single, uncropped rectangle.
    art_box = (40, 145, 1800, 1318)
    art = raw.resize((1760, 1173), Image.Resampling.LANCZOS)
    canvas.alpha_composite(art, (art_box[0], art_box[1]))
    draw.rounded_rectangle(art_box, radius=16, outline=(95, 111, 123, 255), width=2)

    tag(draw, (58, 163), "A  简化勇拳｜完整核心机", ORANGE)
    tag(draw, (522, 163), "B  简化社勇王｜正 3/4", CYAN)
    tag(draw, (1306, 163), "C  新头部特写｜双环 + 箭冠", CYAN)
    tag(draw, (1245, 580), "D  三步深度重组示意", MINT)
    tag(draw, (1195, 1080), "E  128px 黑剪影首读", ORANGE)

    # Right review rail.
    rail = (1825, 145, 2360, 1318)
    panel(draw, rail, outline=(94, 112, 124, 255), fill=(17, 25, 32, 255))
    draw.text((1857, 178), "本轮只解决三件事", font=font(32), fill=WHITE)

    items = [
        ("01", "细节降噪", ["删去约 35% 小甲片／刻线", "改用橙、金、黑三大色块"], ORANGE),
        ("02", "唯一主特征", ["多级回送环 + 安全橙承力箭轴", "巨拳始终保持主体比例"], CYAN),
        ("03", "社勇王新头", ["原头收纳，不露小机器人", "双环侧冠 + 箭冠，不用通用 V 头"], MINT),
    ]
    y = 245
    for num, title, body, color in items:
        draw.rounded_rectangle((1855, y, 1919, y + 54), radius=14, fill=color)
        draw.text((1870, y + 8), num, font=font(25), fill=(8, 15, 20, 255))
        draw.text((1940, y + 3), title, font=font(27), fill=color)
        multiline(draw, (1940, y + 47), body, size=20, fill=WHITE, gap=10)
        y += 205

    draw.line((1857, 868, 2328, 868), fill=(76, 92, 104, 255), width=2)
    draw.text((1857, 895), "SECTION 2 诚实自审", font=font(29), fill=WHITE)
    draw.text((1857, 940), "自审通过 ≠ 用户视觉通过", font=font(21), fill=ORANGE)
    multiline(draw, (1857, 995), [
        "通过｜细节密度已明显下降",
        "通过｜新头部成为第一焦点",
        "通过｜两形态仍是同一大拳",
        "开放｜三步图只锁方向，不锁工程几何",
    ], size=20, fill=WHITE, gap=13)

    draw.rounded_rectangle((1855, 1195, 2330, 1278), radius=14,
                           fill=(47, 22, 24, 255), outline=RED, width=2)
    draw.text((1880, 1214), "未确认前：不接 Godot、不做动作包", font=font(20), fill=(255, 181, 176, 255))
    draw.text((1880, 1247), "不进入 Runtime，不晋级 Canon", font=font(20), fill=(255, 181, 176, 255))

    # Bottom decision cards.
    bottom_y = 1343
    boxes = [
        (40, bottom_y, 800, 1798),
        (820, bottom_y, 1580, 1798),
        (1600, bottom_y, 2360, 1798),
    ]
    for box, color in zip(boxes, (ORANGE, CYAN, MINT)):
        panel(draw, box, outline=color, fill=(15, 23, 30, 255), radius=18, width=2)

    draw.text((72, 1372), "① 勇拳：保留身份，降低噪声", font=font(28), fill=ORANGE)
    multiline(draw, (72, 1426), [
        "完整头／胸／腰／四肢不变；不是空胸壳。",
        "肩、腿、脚改成大块面；小刻线退为次级。",
        "腕部多级压缩环仍是第一识别。",
    ], size=21, fill=WHITE, gap=15)

    # True 128 px silhouette normalization for first-read comparison.
    brave_sil = extract_black_silhouette(raw, (995, 750, 1155, 985), 128)
    social_sil = extract_black_silhouette(raw, (1135, 705, 1425, 995), 128)
    draw.text((420, 1575), "128px SILHOUETTE", font=font(18), fill=MUTED)
    for x, sil, label in ((438, brave_sil, "勇拳"), (610, social_sil, "社勇王")):
        tile = (x, 1610, x + 142, 1764)
        draw.rounded_rectangle(tile, radius=12, fill=(221, 226, 225, 255), outline=(109, 119, 121, 255), width=2)
        px = x + (142 - sil.width) // 2
        canvas.alpha_composite(sil, (px, 1622))
        draw.text((x + 71, 1754), label, font=font(15), fill=(22, 28, 31, 255), anchor="mm")

    draw.text((852, 1372), "② 社勇王：深度重组，不是套壳", font=font(28), fill=CYAN)
    multiline(draw, (852, 1426), [
        "勇拳原头完全收纳；核心进入头胸—腰腹承力链。",
        "外部件形成完成形四肢与紧凑背部。",
        "同一巨拳／腕环可追认；不露一台小机器人。",
        "三步图为视觉逻辑，不是已批准工程变形图。",
    ], size=20, fill=WHITE, gap=13)

    draw.text((1632, 1372), "③ 用户只需确认这一版方向", font=font(28), fill=MINT)
    multiline(draw, (1632, 1426), [
        "A. 降低细节后，勇拳是否仍是原来的勇拳？",
        "B. 双回送环 + 橙色箭轴是否足够形成个性？",
        "C. 社勇王新头与深度重组关系是否成立？",
        "通过后才拆分正侧背／动作／地图资产。",
    ], size=20, fill=WHITE, gap=13)

    canvas.convert("RGB").save(OUT, format="PNG", optimize=False, compress_level=9)

    readback = {
        "producer_lane": "Art Asset Section 2",
        "status": "Candidate_user_false_runtime_false_canon_not_promoted",
        "imagegen_calls": 1,
        "rerolls": 0,
        "identity_reference": str(HERE / "reference" / "BRAVE_FIST_USER_APPROVED_PIXEL_IDENTITY_REFERENCE.png"),
        "raw": {"path": str(RAW), "size": list(raw.size), "sha256": sha256(RAW)},
        "board": {"path": str(OUT), "size": [W, H], "sha256": sha256(OUT)},
        "operations": ["single_source_scale", "layout", "labels", "status_panels"],
        "godot_or_runtime_changes": False,
        "canon_promotion": False,
        "section2_self_review": {
            "detail_reduction_readable": True,
            "new_head_is_primary_focal_point": True,
            "same_fist_continuity_readable": True,
            "transformation_steps_are_visual_direction_only": True,
            "silhouette_normalization_height_px": 128,
        },
    }
    READBACK.write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
