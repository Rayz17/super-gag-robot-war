#!/usr/bin/env python3
"""Deterministic annotation/layout only; never draws or reconstructs mecha pixels."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "generation-raw" / "BRAVE_FIST_SOCIAL_BRAVE_RELATIONSHIP_RAW.png"
OUT = ROOT / "BRAVE_FIST_TO_SOCIAL_BRAVE_RELATIONSHIP_CORRECTION_BOARD_2400x1600.png"
PREVIEW = ROOT / "BRAVE_FIST_TO_SOCIAL_BRAVE_RELATIONSHIP_CORRECTION_BOARD_50PCT_1200x800.png"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def f(size: int, bold: bool = False):
    # Hiragino Sans GB collection index 1 is the heavier face on current macOS.
    return ImageFont.truetype(FONT, size=size, index=1 if bold else 0)


def rr(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        line = ""
        for ch in paragraph:
            test = line + ch
            if line and draw.textlength(test, font=font) > max_width:
                lines.append(line)
                line = ch
            else:
                line = test
        lines.append(line)
    return lines


def text_block(draw, xy, text, font, fill, max_width, spacing=8):
    x, y = xy
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line or "国", font=font)
        y += bbox[3] - bbox[1] + spacing
    return y


def tag(draw, xy, label, accent, max_w=None):
    x, y = xy
    font = f(24, True)
    tw = draw.textlength(label, font=font)
    w = min(max_w, tw + 34) if max_w else tw + 34
    rr(draw, (x, y, x + w, y + 44), 12, (15, 19, 23, 230), accent, 2)
    draw.text((x + 17, y + 8), label, font=font, fill=(245, 247, 249, 255))


canvas = Image.new("RGBA", (2400, 1600), (17, 20, 24, 255))
draw = ImageDraw.Draw(canvas, "RGBA")

# Header
draw.rectangle((0, 0, 2400, 132), fill=(11, 14, 18, 255))
draw.rectangle((0, 128, 2400, 132), fill=(242, 156, 42, 255))
draw.text((42, 24), "勇拳 → 社勇王｜关系与轮廓纠偏板", font=f(54, True), fill=(248, 249, 251, 255))
draw.text((44, 88), "ONE CANDIDATE PROPOSAL · 关系先行 · 不是最终全套设计", font=f(24), fill=(182, 192, 203, 255))
rr(draw, (2022, 34, 2355, 97), 16, (52, 40, 20, 255), (242, 156, 42, 255), 2)
draw.text((2071, 51), "CANDIDATE / 待确认", font=f(25, True), fill=(255, 207, 119, 255))

# Original single ImageGen sheet, scaled uniformly and never cropped.
raw = Image.open(RAW).convert("RGBA")
raw = raw.resize((1800, 1200), Image.Resampling.LANCZOS)
canvas.alpha_composite(raw, (40, 150))
draw = ImageDraw.Draw(canvas, "RGBA")
draw.rectangle((40, 150, 1840, 1350), outline=(92, 101, 111, 255), width=2)

# Panel labels; annotations only.
tag(draw, (58, 166), "A  勇拳独立形态｜完整核心机器人", (242, 156, 42, 255), 510)
tag(draw, (625, 166), "B  社勇王合体结构示意｜暖色=勇拳保留区", (83, 174, 223, 255), 660)
tag(draw, (1305, 166), "C  正面／侧面保留关系", (83, 174, 223, 255), 490)
tag(draw, (1090, 1074), "D  大拳三态｜外轮廓不缩小", (242, 156, 42, 255), 500)

# Deterministic chest nameplate copy required by the approved identity brief.
# These are text annotations placed only inside the two blank nameplate areas.
for cx, cy, size in ((311, 480, 45), (877, 500, 42)):
    txt = "勇拳"
    font = f(size, True)
    bbox = draw.textbbox((0, 0), txt, font=font, stroke_width=2)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2, cy - th / 2 - 4), txt, font=font,
              fill=(63, 37, 9, 255), stroke_width=2, stroke_fill=(255, 223, 132, 220))

# Right-side decision notes.
side = (1860, 150, 2360, 1350)
rr(draw, side, 22, (24, 29, 35, 255), (73, 82, 92, 255), 2)
draw.text((1890, 180), "判读要点", font=f(36, True), fill=(249, 250, 251, 255))
draw.text((1892, 229), "机器 PASS ≠ 用户视觉 PASS", font=f(21), fill=(241, 171, 73, 255))

sections = [
    ("A  勇拳本体", "约17m；豪司驾驶；无独立机魂。\n头、胸、躯干完整；金+安全橙+暗骨架；比18m馆守Z更轻快；大拳为第一识别。", (242, 156, 42, 255)),
    ("B  外部合体部件", "腿足：增高与承重\n肩臂：支架与前臂蓄能套筒\n背／上身：飞行框与护甲\n灰色部分仅表示功能类，非最终造型。", (83, 174, 223, 255)),
    ("C  合体后仍外露", "英雄脸／“勇拳”胸牌与中央胸块／腹部核心脊／大拳正面轮廓。\n社勇王能明确看出“勇拳在其中”。", (111, 199, 166, 255)),
    ("D  大拳三态", "常态 → 蓄能压缩 → 释放。\n拳掌外形始终大且基本不变；变化只在拳后蓄能环、套筒锁定和前臂行程。", (242, 156, 42, 255)),
    ("E  致敬与原创边界", "只取“完整核心机器人 + 外部合体机”的结构逻辑。\n无狮核／兽胸；不复制机数、载具主题、徽标、翼型或变形序列。", (190, 157, 232, 255)),
]

y = 278
for title, body, accent in sections:
    draw.rectangle((1890, y + 8, 1900, y + 41), fill=accent)
    draw.text((1916, y), title, font=f(25, True), fill=accent)
    y = text_block(draw, (1890, y + 43), body, f(22), (218, 224, 231, 255), 438, 6) + 16

# Bottom relationship lock and user gate.
rr(draw, (40, 1370, 2360, 1565), 22, (22, 26, 31, 255), (242, 156, 42, 255), 2)
draw.text((72, 1391), "正确关系", font=f(27, True), fill=(242, 156, 42, 255))
draw.text((235, 1388), "勇拳（完整、可独立作战的17m核心机器人）  +  外部合体部件  →  社勇王",
          font=f(32, True), fill=(246, 248, 250, 255))
draw.text((72, 1443), "立即作废：空胸试验壳 · 未来狮形核心入座 · “同工程族但非核心” · 简单放大换皮",
          font=f(25, True), fill=(239, 113, 101, 255))
draw.line((72, 1490, 2328, 1490), fill=(72, 81, 91, 255), width=2)
draw.text((72, 1507), "用户确认门：① 勇拳独立形态的“轻快完整核心机 + 大拳”是否成立；② 合体后保留脸、胸牌、腹脊与大拳正面是否正确。",
          font=f(24), fill=(196, 207, 218, 255))

# Final border and outputs.
draw.rectangle((18, 18, 2382, 1582), outline=(75, 84, 94, 255), width=2)
canvas.convert("RGB").save(OUT, format="PNG", optimize=False, compress_level=9)
canvas.resize((1200, 800), Image.Resampling.LANCZOS).convert("RGB").save(
    PREVIEW, format="PNG", optimize=False, compress_level=9
)
print(OUT)
print(PREVIEW)
