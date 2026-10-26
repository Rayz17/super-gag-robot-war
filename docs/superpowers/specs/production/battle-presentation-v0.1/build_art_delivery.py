#!/usr/bin/env python3
"""Build deterministic C01 Guardian Z and seal-drone art derivatives."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[5]
PACKAGE = Path(__file__).resolve().parent / "art-delivery"
APPROVED = PACKAGE / "approved"
STAGING = PACKAGE / "staging"
REVIEW = PACKAGE / "review"

HALF_KNEEL = ROOT / ".superpowers/brainstorm/37837-1782033239/content/asset-production/v31-c01-opening-p0-v1/guardian_z_half_kneel_guard.png"
DOUDENG = ROOT / ".superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_doudeng_expressions.png"
DRONE_BASE = STAGING / "seal_drone_b_base_cutout_v01.png"


def alpha_crop(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("image has no visible alpha content")
    return rgba.crop(bbox)


def place_bottom_center(
    source: Image.Image,
    canvas_size: tuple[int, int],
    pivot: tuple[int, int],
    target_height: int,
    max_width: int,
) -> Image.Image:
    subject = alpha_crop(source)
    scale = min(target_height / subject.height, max_width / subject.width)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    x = round(pivot[0] - subject.width / 2)
    y = pivot[1] - subject.height
    canvas.alpha_composite(subject, (x, y))
    return canvas


def make_pose(source: Path, output: Path) -> None:
    image = Image.open(source)
    result = place_bottom_center(image, (2048, 2048), (1024, 1856), 1500, 1408)
    result.save(output, optimize=True)


def make_sprite(source: Path, output: Path) -> None:
    image = Image.open(source)
    result = place_bottom_center(image, (512, 512), (256, 432), 400, 448)
    result.save(output, optimize=True)


def make_shadow(output: Path) -> None:
    layer = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((112, 402, 400, 454), fill=(13, 19, 24, 112))
    layer = layer.filter(ImageFilter.GaussianBlur(10))
    layer.save(output, optimize=True)


def make_drone_shadow(output: Path) -> None:
    layer = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((104, 386, 408, 442), fill=(13, 19, 24, 96))
    layer = layer.filter(ImageFilter.GaussianBlur(12))
    layer.save(output, optimize=True)


def drone_master() -> Image.Image:
    return place_bottom_center(Image.open(DRONE_BASE), (512, 512), (256, 416), 300, 448)


def glow_layer(shapes: Image.Image, radius: int = 10) -> Image.Image:
    return shapes.filter(ImageFilter.GaussianBlur(radius))


def add_drone_status_lamp(image: Image.Image, color: tuple[int, int, int, int]) -> None:
    """Three abstract segments read as an archive sequence lamp without text."""
    draw = ImageDraw.Draw(image)
    for index in range(3):
        x = 370 + index * 12
        draw.rounded_rectangle((x, 244, x + 8, 252), radius=2, fill=color)


def make_drone_states() -> None:
    Image.open(DRONE_BASE).convert("RGBA").save(
        APPROVED / "design_seal_drone_b_master_v01.png",
        optimize=True,
    )
    base = drone_master()

    idle = base.copy()
    add_drone_status_lamp(idle, (226, 164, 78, 220))
    idle.save(APPROVED / "sprite_seal_drone_c01_idle_v01.png", optimize=True)

    scan_beam = Image.new("RGBA", base.size, (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scan_beam)
    scan_draw.polygon(
        [(132, 308), (388, 308), (438, 438), (74, 438)],
        fill=(220, 75, 53, 36),
    )
    scan_draw.line((96, 398, 416, 398), fill=(239, 116, 71, 104), width=5)
    scan = Image.alpha_composite(glow_layer(scan_beam, 8), base)
    scan = Image.alpha_composite(scan, scan_beam)
    scan_draw = ImageDraw.Draw(scan)
    scan_draw.line((132, 308, 388, 308), fill=(255, 153, 91, 238), width=4)
    add_drone_status_lamp(scan, (255, 113, 72, 255))
    scan.save(APPROVED / "sprite_seal_drone_c01_scan_v01.png", optimize=True)

    lock_field = Image.new("RGBA", base.size, (0, 0, 0, 0))
    lock_draw = ImageDraw.Draw(lock_field)
    lock_draw.polygon(
        [(126, 314), (386, 314), (424, 446), (88, 446)],
        fill=(215, 68, 49, 30),
        outline=(240, 115, 73, 170),
        width=4,
    )
    corner_color = (255, 178, 95, 232)
    corners = [
        ((88, 410), (88, 446), (124, 446)),
        ((388, 446), (424, 446), (424, 410)),
        ((126, 350), (126, 314), (162, 314)),
        ((350, 314), (386, 314), (386, 350)),
    ]
    for first, second, third in corners:
        lock_draw.line((*first, *second, *third), fill=corner_color, width=7)
    lock_draw.line((112, 422, 402, 422), fill=(255, 117, 70, 148), width=5)
    lock = Image.alpha_composite(glow_layer(lock_field, 9), base)
    lock = Image.alpha_composite(lock, lock_field)
    lock_draw = ImageDraw.Draw(lock)
    lock_draw.line((128, 307, 389, 307), fill=(255, 185, 98, 255), width=6)
    add_drone_status_lamp(lock, (255, 82, 58, 255))
    lock.save(APPROVED / "sprite_seal_drone_c01_lock_v01.png", optimize=True)

    hit = base.rotate(
        7,
        resample=Image.Resampling.BICUBIC,
        center=(256, 416),
        translate=(14, -10),
    )
    hit_fx = Image.new("RGBA", base.size, (0, 0, 0, 0))
    hit_draw = ImageDraw.Draw(hit_fx)
    hit_draw.line((76, 262, 126, 292), fill=(255, 240, 206, 230), width=7)
    hit_draw.line((58, 286, 116, 310), fill=(230, 93, 60, 190), width=5)
    hit_draw.line((410, 352, 456, 376), fill=(255, 176, 94, 170), width=5)
    hit = Image.alpha_composite(glow_layer(hit_fx, 6), hit)
    hit = Image.alpha_composite(hit, hit_fx)
    add_drone_status_lamp(hit, (255, 71, 51, 255))
    hit.save(APPROVED / "sprite_seal_drone_c01_hit_v01.png", optimize=True)

    disabled = ImageEnhance.Color(base).enhance(0.32)
    disabled = ImageEnhance.Brightness(disabled).enhance(0.72)
    disabled = disabled.rotate(
        -11,
        resample=Image.Resampling.BICUBIC,
        center=(256, 416),
        translate=(-10, 18),
    )
    disabled_draw = ImageDraw.Draw(disabled)
    disabled_draw.rounded_rectangle((137, 305, 379, 318), radius=4, fill=(28, 35, 39, 232))
    add_drone_status_lamp(disabled, (104, 111, 112, 190))
    disabled.save(APPROVED / "sprite_seal_drone_c01_disabled_v01.png", optimize=True)

    make_drone_shadow(APPROVED / "shadow_seal_drone_c01_v01.png")


def make_cutin(source: Image.Image, box: tuple[int, int, int, int], output: Path) -> None:
    portrait = alpha_crop(source.crop(box))
    scale = min(512 / portrait.height, 960 / portrait.width)
    portrait = portrait.resize(
        (max(1, round(portrait.width * scale)), max(1, round(portrait.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", (1920, 640), (0, 0, 0, 0))
    x = round(1180 - portrait.width / 2)
    y = 576 - portrait.height
    canvas.alpha_composite(portrait, (x, y))
    canvas.save(output, optimize=True)


def make_video_frame(source: Path, output: Path) -> None:
    subject = alpha_crop(Image.open(source))
    scale = min(860 / subject.height, 1180 / subject.width)
    subject = subject.resize(
        (max(1, round(subject.width * scale)), max(1, round(subject.height * scale))),
        Image.Resampling.LANCZOS,
    )
    frame = Image.new("RGB", (1920, 1080), (229, 232, 231))
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 820, 1920, 1080), fill=(191, 199, 201))
    draw.rectangle((0, 818, 1920, 824), fill=(169, 154, 118))
    x = round(960 - subject.width / 2)
    y = 940 - subject.height
    frame.paste(subject, (x, y), subject)
    frame.save(output, optimize=True)


def make_drone_candidates(source_path: Path) -> list[Path]:
    source = Image.open(source_path).convert("RGB")
    names = ["rail", "hover_archive", "ring"]
    outputs = []
    for index, name in enumerate(names):
        left = round(source.width * index / 3)
        right = round(source.width * (index + 1) / 3)
        crop = source.crop((left, 0, right, source.height))
        output = REVIEW / f"seal_drone_candidate_{name}_v01.png"
        crop.save(output, optimize=True)
        outputs.append(output)
    return outputs


def make_map_scale_check(output: Path) -> None:
    canvas = Image.new("RGB", (1800, 900), (232, 233, 230))
    draw = ImageDraw.Draw(canvas)
    title_font = font(38)
    label_font = font(23)
    draw.text((48, 30), "25% MAP READABILITY CHECK - 128 px subjects", fill=(29, 35, 40), font=title_font)
    items = [
        ("GZ idle", APPROVED / "sprite_gz_c01_kneel_idle_v01.png"),
        ("GZ guard", APPROVED / "sprite_gz_c01_kneel_guard_v01.png"),
        ("GZ recoil", APPROVED / "sprite_gz_c01_kneel_recoil_v01.png"),
        ("Drone idle", APPROVED / "sprite_seal_drone_c01_idle_v01.png"),
        ("Drone scan", APPROVED / "sprite_seal_drone_c01_scan_v01.png"),
        ("Drone lock", APPROVED / "sprite_seal_drone_c01_lock_v01.png"),
        ("Drone hit", APPROVED / "sprite_seal_drone_c01_hit_v01.png"),
        ("Drone disabled", APPROVED / "sprite_seal_drone_c01_disabled_v01.png"),
    ]
    for index, (label, path) in enumerate(items):
        x = 48 + (index % 4) * 432
        y = 105 + (index // 4) * 380
        draw.rounded_rectangle((x, y, x + 394, y + 330), radius=10, fill=(250, 249, 246), outline=(158, 161, 159), width=2)
        image = Image.open(path).convert("RGBA")
        image.thumbnail((128, 128), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", (128, 128), (244, 243, 239, 255))
        tile.alpha_composite(image, ((128 - image.width) // 2, (128 - image.height) // 2))
        canvas.paste(tile.convert("RGB"), (x + 133, y + 64))
        draw.rectangle((x + 132, y + 63, x + 261, y + 192), outline=(185, 188, 185), width=1)
        draw.text((x + 18, y + 230), label, fill=(38, 44, 49), font=label_font)
        draw.text((x + 18, y + 270), "same 512 px canvas / fixed pivot", fill=(92, 99, 103), font=font(18))
    canvas.save(output, optimize=True)


def checkerboard(size: tuple[int, int], cell: int = 24) -> Image.Image:
    board = Image.new("RGBA", size, (238, 238, 235, 255))
    draw = ImageDraw.Draw(board)
    dark = (194, 198, 198, 255)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, min(size[0], x + cell), min(size[1], y + cell)), fill=dark)
    return board


def make_alpha_edge_check(output: Path) -> None:
    canvas = Image.new("RGB", (2200, 2020), (230, 231, 228))
    draw = ImageDraw.Draw(canvas)
    title_font = font(42)
    label_font = font(24)
    draw.text((60, 38), "ALPHA EDGE VISUAL CHECK - checkerboard composite", fill=(29, 35, 40), font=title_font)
    items = [
        ("locked pose", APPROVED / "pose_gz_c01_kneel_palm_guard_v01.png"),
        ("start pose", APPROVED / "pose_gz_c01_kneel_start_v01.png"),
        ("map idle", APPROVED / "sprite_gz_c01_kneel_idle_v01.png"),
        ("map guard", APPROVED / "sprite_gz_c01_kneel_guard_v01.png"),
        ("map recoil", APPROVED / "sprite_gz_c01_kneel_recoil_v01.png"),
        ("Doudeng safety stop", APPROVED / "cutin_doudeng_c01_safety_lock_v01.png"),
        ("drone idle", APPROVED / "sprite_seal_drone_c01_idle_v01.png"),
        ("drone scan", APPROVED / "sprite_seal_drone_c01_scan_v01.png"),
        ("drone lock", APPROVED / "sprite_seal_drone_c01_lock_v01.png"),
        ("drone hit", APPROVED / "sprite_seal_drone_c01_hit_v01.png"),
        ("drone disabled", APPROVED / "sprite_seal_drone_c01_disabled_v01.png"),
    ]
    boxes = [
        (60, 120, 680, 680),
        (760, 120, 680, 680),
        (1460, 120, 310, 310),
        (1810, 120, 310, 310),
        (1460, 470, 310, 310),
        (60, 850, 2060, 560),
        (60, 1480, 390, 390),
        (480, 1480, 390, 390),
        (900, 1480, 390, 390),
        (1320, 1480, 390, 390),
        (1740, 1480, 390, 390),
    ]
    for (label, path), (x, y, w, h) in zip(items, boxes):
        board = checkerboard((w, h))
        source = Image.open(path).convert("RGBA")
        source.thumbnail((w - 28, h - 64), Image.Resampling.LANCZOS)
        board.alpha_composite(source, ((w - source.width) // 2, (h - 48 - source.height) // 2))
        canvas.paste(board.convert("RGB"), (x, y))
        draw.rectangle((x, y, x + w, y + h), outline=(130, 134, 134), width=2)
        draw.text((x + 14, y + h - 40), label, fill=(30, 36, 41), font=label_font)
    canvas.save(output, optimize=True)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def thumb(image: Image.Image, box: tuple[int, int], background=(244, 243, 239, 255)) -> Image.Image:
    source = image.convert("RGBA")
    source.thumbnail(box, Image.Resampling.LANCZOS)
    tile = Image.new("RGBA", box, background)
    tile.alpha_composite(source, ((box[0] - source.width) // 2, (box[1] - source.height) // 2))
    return tile


def make_contact_sheet(output: Path) -> None:
    width, height = 2400, 4200
    sheet = Image.new("RGB", (width, height), (235, 235, 231))
    draw = ImageDraw.Draw(sheet)
    title_font = font(54)
    section_font = font(32)
    label_font = font(24)
    draw.text((80, 48), "C01 Guardian Z Defense + Seal Drone Art Delivery", fill=(25, 31, 36), font=title_font)

    def panel(x: int, y: int, w: int, h: int, label: str, path: Path) -> None:
        draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=(250, 249, 246), outline=(165, 167, 164), width=2)
        image = thumb(Image.open(path), (w - 32, h - 72))
        sheet.paste(image.convert("RGB"), (x + 16, y + 16))
        draw.text((x + 18, y + h - 46), label, fill=(36, 42, 48), font=label_font)

    draw.text((80, 132), "MAP STATES - 512 x 512 / pivot 256,432", fill=(45, 52, 58), font=section_font)
    map_items = [
        ("idle / approved", APPROVED / "sprite_gz_c01_kneel_idle_v01.png"),
        ("palm guard / approved", APPROVED / "sprite_gz_c01_kneel_guard_v01.png"),
        ("recoil / approved", APPROVED / "sprite_gz_c01_kneel_recoil_v01.png"),
        ("separate shadow", APPROVED / "shadow_gz_c01_kneel_v01.png"),
    ]
    for index, (label, path) in enumerate(map_items):
        panel(80 + index * 570, 186, 530, 500, label, path)

    draw.text((80, 730), "DOUDENG CUT-INS - 1920 x 640 / independent alpha", fill=(45, 52, 58), font=section_font)
    cutin_items = [
        ("command", APPROVED / "cutin_doudeng_c01_command_v01.png"),
        ("observe", APPROVED / "cutin_doudeng_c01_observe_v01.png"),
        ("tense", APPROVED / "cutin_doudeng_c01_tense_v01.png"),
        ("safety stop", APPROVED / "cutin_doudeng_c01_safety_lock_v01.png"),
    ]
    for index, (label, path) in enumerate(cutin_items):
        panel(80 + (index % 2) * 1140, 786 + (index // 2) * 374, 1100, 340, label, path)

    draw.text((80, 1558), "FULL-SCALE POSES - 2048 x 2048 / pivot 1024,1856", fill=(45, 52, 58), font=section_font)
    pose_items = [
        ("start / approved", APPROVED / "pose_gz_c01_kneel_start_v01.png"),
        ("locked-source palm guard", APPROVED / "pose_gz_c01_kneel_palm_guard_v01.png"),
        ("contact / approved", APPROVED / "pose_gz_c01_kneel_contact_v01.png"),
    ]
    for index, (label, path) in enumerate(pose_items):
        panel(80 + index * 760, 1614, 720, 650, label, path)

    draw.text((80, 2310), "AI VIDEO MOTHER FRAMES - REFERENCE ONLY / no baked FX", fill=(45, 52, 58), font=section_font)
    panel(80, 2364, 1100, 250, "start frame / no video generated", STAGING / "video_gz_c01_palm_guard_start_frame_v01.png")
    panel(1220, 2364, 1100, 250, "end frame / no video generated", STAGING / "video_gz_c01_palm_guard_end_frame_v01.png")

    draw.text((80, 2660), "SEAL DRONE DESIGN REVIEW - B SELECTED", fill=(45, 52, 58), font=section_font)
    panel(80, 2714, 2240, 560, "A not selected / B selected / C not selected", REVIEW / "seal_drone_candidate_comparison_v01.png")

    draw.text((80, 3320), "SEAL DRONE B RUNTIME STATES - 512 x 512 / pivot 256,416", fill=(45, 52, 58), font=section_font)
    drone_items = [
        ("idle", APPROVED / "sprite_seal_drone_c01_idle_v01.png"),
        ("scan", APPROVED / "sprite_seal_drone_c01_scan_v01.png"),
        ("lock", APPROVED / "sprite_seal_drone_c01_lock_v01.png"),
        ("hit", APPROVED / "sprite_seal_drone_c01_hit_v01.png"),
        ("disabled", APPROVED / "sprite_seal_drone_c01_disabled_v01.png"),
    ]
    for index, (label, path) in enumerate(drone_items):
        panel(80 + index * 448, 3374, 420, 650, label, path)
    sheet.save(output, quality=94)


def make_drone_state_sheet(output: Path) -> None:
    sheet = Image.new("RGB", (3000, 820), (232, 233, 230))
    draw = ImageDraw.Draw(sheet)
    draw.text((60, 34), "Seal Drone B - Identity-Preserved Runtime States", fill=(29, 35, 40), font=font(46))
    items = [
        ("idle", APPROVED / "sprite_seal_drone_c01_idle_v01.png"),
        ("scan", APPROVED / "sprite_seal_drone_c01_scan_v01.png"),
        ("lock", APPROVED / "sprite_seal_drone_c01_lock_v01.png"),
        ("hit", APPROVED / "sprite_seal_drone_c01_hit_v01.png"),
        ("disabled", APPROVED / "sprite_seal_drone_c01_disabled_v01.png"),
    ]
    for index, (label, path) in enumerate(items):
        x = 60 + index * 584
        board = checkerboard((540, 650), 30)
        source = Image.open(path).convert("RGBA")
        board.alpha_composite(source, (14, 60))
        sheet.paste(board.convert("RGB"), (x, 110))
        draw.rectangle((x, 110, x + 540, 760), outline=(128, 132, 132), width=2)
        draw.text((x + 18, 704), label, fill=(31, 37, 42), font=font(28))
    sheet.save(output, optimize=True)


def main() -> None:
    for directory in (APPROVED, STAGING, REVIEW):
        directory.mkdir(parents=True, exist_ok=True)

    make_pose(HALF_KNEEL, APPROVED / "pose_gz_c01_kneel_palm_guard_v01.png")
    make_pose(STAGING / "guardian_z_pose_start_cutout_v01.png", APPROVED / "pose_gz_c01_kneel_start_v01.png")
    make_pose(STAGING / "guardian_z_pose_contact_cutout_v01.png", APPROVED / "pose_gz_c01_kneel_contact_v01.png")

    make_sprite(STAGING / "guardian_z_map_idle_cutout_v01.png", APPROVED / "sprite_gz_c01_kneel_idle_v01.png")
    make_sprite(STAGING / "guardian_z_map_guard_cutout_v01.png", APPROVED / "sprite_gz_c01_kneel_guard_v01.png")
    make_sprite(STAGING / "guardian_z_map_recoil_cutout_v02.png", APPROVED / "sprite_gz_c01_kneel_recoil_v01.png")
    make_shadow(APPROVED / "shadow_gz_c01_kneel_v01.png")

    source = Image.open(DOUDENG).convert("RGBA")
    half = source.width // 2
    boxes = {
        "command": (0, 0, half, half),
        "observe": (half, 0, source.width, half),
        "tense": (0, half, half, source.height),
        "safety_lock": (half, half, source.width, source.height),
    }
    for name, box in boxes.items():
        make_cutin(source, box, APPROVED / f"cutin_doudeng_c01_{name}_v01.png")

    make_video_frame(APPROVED / "pose_gz_c01_kneel_start_v01.png", STAGING / "video_gz_c01_palm_guard_start_frame_v01.png")
    make_video_frame(APPROVED / "pose_gz_c01_kneel_contact_v01.png", STAGING / "video_gz_c01_palm_guard_end_frame_v01.png")
    make_drone_candidates(REVIEW / "seal_drone_candidate_comparison_v01.png")
    make_drone_states()
    make_contact_sheet(REVIEW / "guardian_z_c01_art_delivery_contact_sheet_v02.jpg")
    make_drone_state_sheet(REVIEW / "seal_drone_b_state_contact_sheet_v01.png")
    make_map_scale_check(REVIEW / "map_scale_readability_check_v02.png")
    make_alpha_edge_check(REVIEW / "alpha_edge_check_v02.png")


if __name__ == "__main__":
    main()
