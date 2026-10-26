#!/usr/bin/env python3
"""Add current-Canon labels to the accepted relationship-board pixels.

The source board is pasted at native resolution.  This script draws only UI
labels outside the mecha art plus a replacement status badge; it never redraws,
repairs, generates, or transforms mecha pixels.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SOURCE = PARENT / "BRAVE_FIST_TO_SOCIAL_BRAVE_RELATIONSHIP_CORRECTION_BOARD_2400x1600.png"
OUT = HERE / "BRAVE_FIST_TO_SOCIAL_BRAVE_CURRENT_CANON_USER_CONFIRMATION_BOARD_2400x1840.png"
PREVIEW = HERE / "BRAVE_FIST_TO_SOCIAL_BRAVE_CURRENT_CANON_USER_CONFIRMATION_BOARD_50PCT_1200x920.png"
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

TOP_H = 80
BOTTOM_H = 160
SOURCE_SIZE = (2400, 1600)


def font(size: int):
    return ImageFont.truetype(FONT_PATH, size)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def round_panel(draw, box, outline, fill=(20, 28, 35, 255), radius=18, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != SOURCE_SIZE:
        raise SystemExit(f"unexpected source size: {source.size}")

    canvas = Image.new("RGBA", (2400, TOP_H + 1600 + BOTTOM_H), (7, 13, 18, 255))
    canvas.alpha_composite(source, (0, TOP_H))
    d = ImageDraw.Draw(canvas)

    # Current authority banner; relationship is locked, only visual expression awaits review.
    d.rectangle((0, 0, 2399, TOP_H - 1), fill=(10, 18, 24, 255))
    d.line((0, TOP_H - 2, 2399, TOP_H - 2), fill=(242, 157, 40, 255), width=3)
    d.text((36, 15), "CURRENT CANON｜同一勇拳核心 + 外部组件 = 社勇王", font=font(38), fill=(244, 247, 248, 255))
    d.text((1260, 22), "关系已锁定；本板只确认视觉表达，不定稿最终社勇王", font=font(25), fill=(120, 207, 219, 255))

    # Replace only the old Candidate status badge; no mecha region is touched.
    old_badge_cover = (1980, TOP_H + 8, 2390, TOP_H + 92)
    d.rectangle(old_badge_cover, fill=(10, 18, 24, 255))
    badge = (2010, TOP_H + 18, 2370, TOP_H + 78)
    round_panel(d, badge, (242, 157, 40, 255), fill=(39, 34, 20, 255), radius=18, width=2)
    d.text((2040, TOP_H + 33), "关系 HARD已锁｜视觉待确认", font=font(22), fill=(249, 202, 112, 255))

    cards = [
        (
            "① 完整勇拳",
            ["头／胸／躯干／四肢完整", "可独立战斗；不是空壳"],
            (242, 157, 40, 255),
        ),
        (
            "② 同一大拳 0→50→100",
            ["D区左→右：常态／压缩／释放", "拳本体不缩；只动拳后环与套筒"],
            (242, 157, 40, 255),
        ),
        (
            "③ 同一核心完成合体",
            ["外部双臂／下肢／飞行·工具件", "围绕同一勇拳锁合；主体可追认"],
            (91, 196, 216, 255),
        ),
        (
            "④ 仍待用户确认的几何",
            ["精确头胸变形、组件数量／主题／徽标", "AI安装／觉醒来源未锁，不从本图反推"],
            (183, 143, 229, 255),
        ),
    ]
    gap = 18
    x0 = 28
    width = (2400 - x0 * 2 - gap * 3) // 4
    y0 = TOP_H + 1600 + 14
    for i, (title, body, color) in enumerate(cards):
        x = x0 + i * (width + gap)
        box = (x, y0, x + width, y0 + 130)
        round_panel(d, box, color, fill=(17, 25, 32, 255), radius=15, width=2)
        d.rectangle((x + 14, y0 + 17, x + 21, y0 + 111), fill=color)
        d.text((x + 34, y0 + 14), title, font=font(24), fill=color)
        d.text((x + 34, y0 + 56), body[0], font=font(19), fill=(224, 232, 237, 255))
        d.text((x + 34, y0 + 89), body[1], font=font(19), fill=(224, 232, 237, 255))

    canvas.convert("RGB").save(OUT, format="PNG", optimize=False, compress_level=9)
    canvas.convert("RGB").resize((1200, 920), Image.Resampling.LANCZOS).save(
        PREVIEW, format="PNG", optimize=False, compress_level=9
    )

    readback = {
        "status": "CURRENT_CANON_RELATION_LOCKED_VISUAL_CONFIRMATION_PENDING",
        "source": {"path": str(SOURCE), "sha256": sha(SOURCE), "size": list(source.size)},
        "operations": ["native_pixel_paste", "text_labels", "layout", "single_50pct_lanczos_resize"],
        "imagegen_calls": 0,
        "mecha_redraw": False,
        "sprite_or_runtime_work": False,
        "source_placement": {"top_left": [0, TOP_H], "size": list(source.size)},
        "source_pixel_overlays": [
            {"purpose": "replace_old_candidate_status_badge_only", "rect_xyxy": list(old_badge_cover)}
        ],
        "mecha_art_regions_modified": False,
        "outputs": {
            "board": {"path": str(OUT), "sha256": sha(OUT), "size": [2400, 1840]},
            "preview": {"path": str(PREVIEW), "sha256": sha(PREVIEW), "size": [1200, 920]},
        },
        "visual_gate": {
            "already_locked": [
                "brave_fist_is_complete_independent_core_robot",
                "same_large_fist_across_0_50_100_energy_states",
                "external_components_combine_around_same_brave_fist_core",
            ],
            "still_unapproved": [
                "exact_head_chest_transformation_geometry",
                "external_component_count_and_vehicle_theme",
                "final_emblem",
                "ai_installation_awakening_source_and_exact_timing",
            ],
        },
    }
    (HERE / "machine-readback.json").write_text(json.dumps(readback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
