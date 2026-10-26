from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


def project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "game-godot").exists():
            return parent
    raise RuntimeError("project root not found")


ROOT = project_root()
BASE = ROOT / "docs/superpowers/specs/production/cinematic-golden-slice-v0.2"
A5 = BASE / "art-delivery/a5"
SOURCES = A5 / "sources"
REVIEW = A5 / "review"
PLATE = REVIEW / "plate_c01_rm_hall_clean_trial_v01.png"
BRIDGE_SHEET = SOURCES / "bridge_subjects_alpha_v01.png"
JICUN = ROOT / ".superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_jicun_stand.png"
DOUDENG = ROOT / ".superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_doudeng_stand.png"
TANGJIAO = ROOT / ".superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_tangjiao_stand.png"


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def trim_alpha(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    box = image.getchannel("A").getbbox()
    if box is None:
        raise ValueError("image has no visible alpha content")
    return image.crop(box)


def resize_to_height(image: Image.Image, height: int) -> Image.Image:
    image = trim_alpha(image)
    width = max(1, round(image.width * height / image.height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def paste_at_foot(canvas: Image.Image, sprite: Image.Image, height: int, foot_x: int, foot_y: int, shadow=True):
    sprite = resize_to_height(sprite, height)
    x = round(foot_x - sprite.width / 2)
    y = foot_y - sprite.height
    if shadow:
        shadow_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow_layer)
        sd.ellipse((foot_x - sprite.width * 0.36, foot_y - 6, foot_x + sprite.width * 0.36, foot_y + 8), fill=(2, 9, 14, 110))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(3))
        canvas.alpha_composite(shadow_layer)
    canvas.alpha_composite(sprite, (x, y))
    return (x, y, x + sprite.width, y + sprite.height)


def bridge_subjects():
    sheet = Image.open(BRIDGE_SHEET).convert("RGBA")
    thirds = []
    for i in range(3):
        left = round(sheet.width * i / 3)
        right = round(sheet.width * (i + 1) / 3)
        thirds.append(trim_alpha(sheet.crop((left, 0, right, sheet.height))))
    return thirds


def draw_label(draw, xy, text, fill=(232, 239, 242, 255), size=20, bold=False, anchor=None):
    draw.text(xy, text, fill=fill, font=font(size, bold), anchor=anchor)


def draw_fg_rail(canvas: Image.Image, start=(0, 640), end=(520, 730), alpha=255):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=(6, 13, 18, alpha), width=22)
    draw.line((sx, sy - 4, ex, ey - 4), fill=(68, 83, 88, min(alpha, 210)), width=4)
    for t in (0.05, 0.48, 0.88):
        x = round(sx + (ex - sx) * t)
        y = round(sy + (ey - sy) * t)
        draw.rectangle((x - 10, y - 70, x + 10, y + 16), fill=(7, 15, 20, alpha), outline=(74, 88, 91, min(alpha, 220)), width=3)
        draw.ellipse((x - 8, y - 76, x + 8, y - 60), fill=(222, 153, 61, min(alpha, 235)))
    canvas.alpha_composite(layer)


def build_runtime_keyframe():
    plate = Image.open(PLATE).convert("RGBA")
    view = plate.crop((320, 90, 1600, 810)).convert("RGBA")
    diedie, dog, visitor = bridge_subjects()
    jicun = Image.open(JICUN).convert("RGBA")
    doudeng = Image.open(DOUDENG).convert("RGBA")
    tangjiao = Image.open(TANGJIAO).convert("RGBA")

    overlay = Image.new("RGBA", view.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    od.polygon([(895, 445), (1190, 445), (1275, 615), (820, 615)], fill=(58, 191, 194, 22), outline=(86, 218, 218, 112), width=2)
    od.line([(80, 565), (1240, 565)], fill=(124, 215, 219, 38), width=1)
    view.alpha_composite(overlay)

    # Far-to-near placement follows footpoint/Y-sort order.
    paste_at_foot(view, doudeng, 180, 180, 555)
    paste_at_foot(view, visitor, 175, 1185, 575)
    paste_at_foot(view, jicun, 190, 680, 605)
    paste_at_foot(view, tangjiao, 200, 410, 620)
    paste_at_foot(view, diedie, 78, 810, 615)
    paste_at_foot(view, dog, 84, 965, 635)
    draw_fg_rail(view, (-40, 625), (520, 730))

    ui = Image.new("RGBA", view.size, (0, 0, 0, 0))
    ud = ImageDraw.Draw(ui, "RGBA")
    ud.rectangle((32, 56, 1248, 602), outline=(226, 239, 239, 95), width=1)
    ud.line((32, 56, 112, 56), fill=(238, 245, 245, 180), width=2)
    ud.line((32, 56, 32, 104), fill=(238, 245, 245, 180), width=2)
    ud.line((1248, 56, 1168, 56), fill=(238, 245, 245, 180), width=2)
    ud.line((1248, 56, 1248, 104), fill=(238, 245, 245, 180), width=2)
    ud.line((32, 602, 112, 602), fill=(238, 245, 245, 180), width=2)
    ud.line((1248, 602, 1168, 602), fill=(238, 245, 245, 180), width=2)
    view.alpha_composite(ui)
    view.convert("RGB").save(REVIEW / "kf_c01_rm_2p5d_runtime_layout_v03.png", quality=96)


def camera_frame(draw, rect, color, label):
    x0, y0, x1, y1 = rect
    draw.rectangle(rect, outline=color, width=4)
    draw.rectangle((x0 + 32, y0 + 56, x1 - 32, y1 - 118), outline=color[:3] + (105,), width=2)
    draw.rectangle((x0 + 12, y0 + 12, x0 + 290, y0 + 46), fill=(5, 14, 20, 225), outline=color, width=2)
    draw_label(draw, (x0 + 24, y0 + 19), label, fill=color, size=20, bold=True)


def build_camera_depth_layout():
    plate = Image.open(PLATE).convert("RGBA")
    plate = ImageEnhance.Brightness(plate).enhance(0.58)
    canvas = plate.copy()
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    colors = [(71, 211, 217, 230), (240, 190, 77, 230), (239, 105, 105, 230)]
    frames = [
        (0, 90, 1280, 810),
        (320, 90, 1600, 810),
        (640, 90, 1920, 810),
    ]
    labels = ["ZONE_A_ENTRY", "ZONE_B_REAL_MACHINE", "ZONE_C_OLD_DOOR_LOW_HEAT"]
    for rect, color, label in zip(frames, colors, labels):
        camera_frame(draw, rect, color, label)

    walkable = [(90, 510), (1810, 510), (1900, 760), (40, 760)]
    draw.polygon(walkable, fill=(73, 197, 172, 30), outline=(109, 236, 202, 220))
    draw_label(draw, (960, 748), "WALKABLE TRAPEZOID", fill=(134, 242, 215, 255), size=21, bold=True, anchor="ms")
    draw.line((0, 410, 1920, 410), fill=(255, 255, 255, 190), width=3)
    draw_label(draw, (18, 380), "GROUND TURN  Y=410", size=18, bold=True)
    for y, name in [(525, "FAR FOOTLINE"), (625, "MID FOOTLINE"), (725, "NEAR FOOTLINE")]:
        draw.line((50, y, 1880, y), fill=(218, 235, 238, 115), width=2)
        draw_label(draw, (1870, y - 24), name, fill=(218, 235, 238, 220), size=16, anchor="ra")
    for end in [(0, 900), (480, 900), (1440, 900), (1920, 900)]:
        draw.line((960, 390, end[0], end[1]), fill=(125, 196, 204, 70), width=2)

    anchors = {
        "DOUDENG": (400, 575), "TANGJIAO": (626, 650), "DIEDIE": (969, 605),
        "CHARGE": (1059, 730), "MACHINE_DOG": (1186, 690), "LOW_HEAT": (1336, 520),
        "VISITOR": (1449, 610), "OLD_DOOR": (1675, 560), "GUARDIAN_Z_FAR": (1180, 350),
    }
    for name, (x, y) in anchors.items():
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(244, 200, 82, 255), outline=(7, 19, 26, 255), width=2)
        draw_label(draw, (x + 13, y - 20), name, fill=(245, 225, 167, 255), size=15, bold=True)

    canvas.alpha_composite(overlay)
    draw_fg_rail(canvas, (-30, 760), (1920, 860), alpha=150)
    jicun = Image.open(JICUN).convert("RGBA")
    diedie, dog, _visitor = bridge_subjects()
    paste_at_foot(canvas, jicun, 165, 170, 700)
    paste_at_foot(canvas, jicun, 190, 330, 700)
    paste_at_foot(canvas, jicun, 220, 510, 700)
    paste_at_foot(canvas, diedie, 60, 645, 700)
    paste_at_foot(canvas, diedie, 80, 720, 700)
    paste_at_foot(canvas, dog, 100, 830, 700)
    final = ImageDraw.Draw(canvas, "RGBA")
    for x, label in [(170, "165 px"), (330, "190 px"), (510, "220 px"), (645, "60 px"), (720, "80 px"), (830, "100 px")]:
        draw_label(final, (x, 722), label, size=15, bold=True, anchor="ma")
    canvas.convert("RGB").save(REVIEW / "layout_c01_rm_camera_depth_v01.png", quality=96)


def build_layer_breakdown():
    plate = Image.open(PLATE).convert("RGBA")
    plate = ImageEnhance.Brightness(plate).enhance(0.62)
    canvas = plate.copy()
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    draw.rectangle((0, 0, 1920, 440), fill=(57, 108, 178, 38), outline=(84, 153, 231, 220), width=3)
    draw.rectangle((0, 410, 1920, 820), fill=(66, 181, 139, 30), outline=(90, 224, 172, 220), width=3)
    draw.rectangle((0, 715, 1920, 900), fill=(232, 155, 62, 30), outline=(247, 179, 77, 220), width=3)
    draw_label(draw, (30, 115), "FAR  / OPAQUE PLATE", fill=(137, 195, 255, 255), size=26, bold=True)
    draw_label(draw, (30, 455), "MID_CLEAN  / OPAQUE PLATE", fill=(142, 244, 199, 255), size=26, bold=True)
    draw_label(draw, (30, 850), "FG  / ALPHA PNG + OCCLUSION RANGE", fill=(255, 205, 128, 255), size=24, bold=True)

    props = [
        (330, 420, 520, 610, "PROP work bay A"),
        (520, 420, 720, 610, "PROP work bay B"),
        (1040, 620, 1185, 760, "PROP charge states"),
        (1600, 335, 1845, 620, "PROP old door open/close"),
        (760, 500, 900, 650, "PROP guide panel clean/cracked"),
    ]
    for x0, y0, x1, y1, label in props:
        draw.rectangle((x0, y0, x1, y1), fill=(236, 188, 67, 35), outline=(246, 201, 84, 245), width=3)
        draw_label(draw, (x0 + 8, y0 + 8), label, fill=(255, 224, 137, 255), size=15, bold=True)

    low_heat = [(1240, 505), (1540, 505), (1660, 720), (1140, 720)]
    draw.polygon(low_heat, fill=(64, 222, 222, 42), outline=(92, 238, 238, 245))
    draw_label(draw, (1390, 565), "MASK low-heat sector", fill=(135, 255, 250, 255), size=18, bold=True, anchor="mm")
    draw.ellipse((1105, 235, 1245, 375), fill=(255, 176, 72, 28), outline=(255, 188, 86, 230), width=3)
    draw_label(draw, (1175, 382), "MASK chest / beam / afterglow", fill=(255, 213, 153, 255), size=16, bold=True, anchor="ma")

    sprite_points = [(400, 580), (650, 650), (980, 610), (1190, 700), (1480, 610)]
    for x, y in sprite_points:
        draw.line((x - 16, y, x + 16, y), fill=(242, 122, 229, 255), width=3)
        draw.line((x, y - 16, x, y + 16), fill=(242, 122, 229, 255), width=3)
        draw.rectangle((x - 70, y - 220, x + 70, y + 10), outline=(242, 122, 229, 130), width=2)
    draw_label(draw, (1040, 830), "SPRITE / ALPHA PNG / FOOT-CENTER PIVOT", fill=(255, 157, 240, 255), size=22, bold=True, anchor="ma")

    legend = [
        ("OPAQUE", "FAR + MID_CLEAN, no switchable state"),
        ("ALPHA", "PROP + FG + SPRITE, transparent edges"),
        ("MASK", "ambient / low heat / chest / afterglow, grayscale or vector"),
        ("VECTOR", "walkable / pivots / occlusion / camera safe areas"),
    ]
    y = 22
    for key, value in legend:
        draw.rectangle((1290, y, 1900, y + 34), fill=(5, 15, 21, 220), outline=(186, 213, 217, 150), width=1)
        draw_label(draw, (1304, y + 7), key, fill=(245, 203, 105, 255), size=16, bold=True)
        draw_label(draw, (1395, y + 7), value, size=15)
        y += 40
    canvas.alpha_composite(overlay)
    canvas.convert("RGB").save(REVIEW / "breakdown_c01_rm_runtime_layers_v01.png", quality=96)


def build_actor_scale_bridge():
    canvas = Image.new("RGBA", (1280, 720), (16, 27, 35, 255))
    draw = ImageDraw.Draw(canvas, "RGBA")
    for x in range(0, 1281, 32):
        draw.line((x, 0, x, 720), fill=(78, 116, 128, 26), width=1)
    for y in range(0, 721, 32):
        draw.line((0, y, 1280, y), fill=(78, 116, 128, 26), width=1)
    draw_label(draw, (32, 24), "SCALE_C01_RM_ACTOR_BRIDGE_V01", size=25, bold=True)
    draw_label(draw, (32, 58), "CML001: BLACK HAIR / BLUE EYES / NO GLASSES / LEFT-ARM TERMINAL", fill=(137, 215, 229, 255), size=17, bold=True)
    draw.line((32, 525, 880, 525), fill=(221, 232, 235, 135), width=2)
    draw_label(draw, (32, 532), "FOOT-CENTER BASELINE", fill=(191, 208, 212, 230), size=14)
    jicun = Image.open(JICUN).convert("RGBA")
    for x, height in [(155, 165), (425, 190), (735, 220)]:
        box = paste_at_foot(canvas, jicun, height, x, 525)
        d = ImageDraw.Draw(canvas, "RGBA")
        d.line((box[0] - 16, box[1], box[0] - 16, box[3]), fill=(243, 194, 76, 230), width=2)
        d.line((box[0] - 22, box[1], box[0] - 10, box[1]), fill=(243, 194, 76, 230), width=2)
        d.line((box[0] - 22, box[3], box[0] - 10, box[3]), fill=(243, 194, 76, 230), width=2)
        draw_label(d, (x, 554), f"{height} px", fill=(255, 220, 130, 255), size=19, bold=True, anchor="ma")

    diedie, dog, _visitor = bridge_subjects()
    draw.rounded_rectangle((900, 100, 1245, 660), radius=8, fill=(7, 17, 24, 190), outline=(79, 143, 154, 190), width=2)
    draw_label(draw, (1072, 118), "SMALL ROBOT READ", fill=(137, 215, 229, 255), size=18, bold=True, anchor="ma")
    rows = [(245, 60), (405, 80), (585, 100)]
    for foot_y, height in rows:
        paste_at_foot(canvas, diedie, height, 990, foot_y)
        paste_at_foot(canvas, dog, height, 1155, foot_y)
        draw_label(ImageDraw.Draw(canvas, "RGBA"), (1072, foot_y + 12), f"{height} px", fill=(255, 220, 130, 255), size=16, bold=True, anchor="ma")
    draw_label(ImageDraw.Draw(canvas, "RGBA"), (990, 638), "DIEDIE", size=15, bold=True, anchor="ma")
    draw_label(ImageDraw.Draw(canvas, "RGBA"), (1155, 638), "MACHINE DOG", size=15, bold=True, anchor="ma")
    canvas.convert("RGB").save(REVIEW / "scale_c01_rm_actor_bridge_v01.png", quality=96)


def build_zone_evidence():
    plate = Image.open(PLATE).convert("RGB")
    zone_dir = REVIEW / "zone-evidence"
    zone_dir.mkdir(parents=True, exist_ok=True)
    zones = [
        ("zone_a_entry_clean_crop.png", "ZONE_A_ENTRY", 0),
        ("zone_b_real_machine_clean_crop.png", "ZONE_B_REAL_MACHINE", 320),
        ("zone_c_old_door_low_heat_clean_crop.png", "ZONE_C_OLD_DOOR_LOW_HEAT", 640),
    ]
    sheet = Image.new("RGB", (1920, 400), (7, 16, 22))
    sd = ImageDraw.Draw(sheet, "RGBA")
    for index, (filename, label, x) in enumerate(zones):
        crop = plate.crop((x, 90, x + 1280, 810))
        crop.save(zone_dir / filename, quality=96)
        preview = crop.resize((640, 360), Image.Resampling.LANCZOS)
        sheet.paste(preview, (index * 640, 40))
        sd.rectangle((index * 640, 0, index * 640 + 639, 39), fill=(5, 15, 21, 255), outline=(105, 196, 204, 220), width=1)
        draw_label(sd, (index * 640 + 18, 10), label, fill=(157, 229, 233, 255), size=18, bold=True)
    sheet.save(zone_dir / "camera_zone_clean_contact_sheet.png", quality=96)


if __name__ == "__main__":
    REVIEW.mkdir(parents=True, exist_ok=True)
    build_runtime_keyframe()
    build_camera_depth_layout()
    build_layer_breakdown()
    build_actor_scale_bridge()
    build_zone_evidence()
    print("A5_ARTIFACT_BUILD_OK")
