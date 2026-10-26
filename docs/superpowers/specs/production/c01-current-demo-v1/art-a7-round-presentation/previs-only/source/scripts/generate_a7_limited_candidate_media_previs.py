#!/usr/bin/env python3.13
"""Generate the A7 producer-authorized limited Candidate visual set.

Authorized outputs only:
- one layered R05_CUTIN_GIANT_CONTACT
- three reusable eight-frame FX atlases
- one 1280x720 review composite

The four rejected exploration images are hash-checked but never opened.
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve()
while ROOT != ROOT.parent:
    if (ROOT / "docs/superpowers/specs/production/c01-current-demo-v1").is_dir():
        break
    ROOT = ROOT.parent
else:
    raise RuntimeError("repository root not found")

PRODUCTION = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1"
TARGET = PRODUCTION / "art-a7-round-presentation"
CUTIN = TARGET / "cutin"
FX = TARGET / "fx"
REVIEW = TARGET / "review"

IDENTITY_SCRIPT = TARGET / "scripts/generate_a7_identity_lock.py"
IDENTITY_BOARD = TARGET / "A7_IDENTITY_LOCK_GUARDIAN_C_BREAKER_BX_2400x1600.png"
BG_SOURCE = TARGET / "source/imagegen/R05_CUTIN_GIANT_CONTACT_BG_imagegen_source.png"

FIXED = {
    PRODUCTION / "42-c01e02-m3-r0-5-media-packing-v2.json": "fe75667eac656756e35ddbbb784e250d39c0f8b05c2c14f719234d653b944012",
    PRODUCTION / "45-c01e02-m3-r0-5-a7-identity-lock-producer-review.md": "a90314f6357d18874e78c56312412e4253badc1365a8710e6c723471a064ca57",
    IDENTITY_BOARD: "4aed7359548052bf11b6624bfe2cce79462b0266afd99358fabc702deebde575",
    BG_SOURCE: "51d24e89f9d748e059765d504dd8bf1f9e3f01d1a2ee769ef7b5e79d96b86bcc",
    PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_BASE_2400x1350.png": "6fd40a256afee225457594558edf274823de5d1e771d1f570d0263c5df217789",
    PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_BUILDINGS_2400x1350.png": "db3f83eeb3ed5e583d0a831a203ab0d5446a594f9ed9e34f25f175f290f62237",
    PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_ROOFS_2400x1350.png": "7fea3c7918ff85bb1d5df1f4bcc5856afac1d8fa7f174d59b862f985962f11a9",
    PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_FOREGROUND_2400x1350.png": "454b3cf845ba91d7d7f13e201874bbbe79f871297a36930a24348823df1525a3",
}

REJECTED = {
    "R05_CUTIN_SWARM_INTERCEPT_imagegen_source.png": "14da360aafc93e55507659a015afb87f1f24a8b23472ad9c01c2040ed0e5879c",
    "R05_CUTIN_GIANT_CONTACT_imagegen_source.png": "a01e55edf1d14ed3601dd2dac6b8c9c98f72f37eafe54a930978b4e5f9976bf1",
    "R05_CUTIN_ARTILLERY_SIDE_HIT_imagegen_source.png": "be01ab84be1ba19bf55975040a1b29254e759c9cfa53695e737660861b31b0d5",
    "R05_CUTIN_RED_CHARGE_imagegen_source.png": "8a1093377704ca6f9ba7345900cb6a0f65ecb2bca62d97a95363daaed63edcbd",
}

W, H = 1600, 900
FRAME = 256
FRAME_COUNT = 8
ATLAS_W = FRAME * FRAME_COUNT

FONT = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")
FONT_BOLD = Path("/System/Library/Fonts/STHeiti Medium.ttc")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_sources() -> None:
    for path, expected in FIXED.items():
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"source hash mismatch: {path}: {actual}")
    quarantine = TARGET / "rejected-exploration/source"
    for name, expected in REJECTED.items():
        actual = sha256(quarantine / name)
        if actual != expected:
            raise RuntimeError(f"rejected source byte drift: {name}: {actual}")


def load_identity_module():
    spec = importlib.util.spec_from_file_location("a7_identity", IDENTITY_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("identity module import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_rgba(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGBA").save(path, format="PNG", optimize=True)


def actor_layer(identity, actor: str, cx: int, ground: int, scale: float) -> Image.Image:
    supersample = 2
    layer = Image.new("RGBA", (W * supersample, H * supersample), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    if actor == "guardian":
        identity.guardian(draw, cx * supersample, ground * supersample, scale * supersample, "three_quarter", "contact")
    elif actor == "breaker":
        identity.breaker(draw, cx * supersample, ground * supersample, scale * supersample, "side", "contact")
    else:
        raise ValueError(actor)
    layer = layer.resize((W, H), Image.Resampling.LANCZOS)

    # Cool rainy tint and a restrained cyan rim bind the exact R2 geometry to
    # the painted environment without repainting or changing the silhouette.
    alpha = layer.getchannel("A")
    rgb = layer.convert("RGB")
    rgb = ImageChops.multiply(rgb, Image.new("RGB", layer.size, (220, 235, 242)))
    tinted = rgb.convert("RGBA")
    tinted.putalpha(alpha)
    outer = alpha.filter(ImageFilter.MaxFilter(9))
    edge = ImageChops.subtract(outer, alpha).point(lambda value: min(96, value))
    rim = Image.new("RGBA", layer.size, (128, 221, 224, 0))
    rim.putalpha(edge)
    integrated = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    integrated.alpha_composite(rim)
    integrated.alpha_composite(tinted)

    if actor == "guardian":
        # Shear around the planted feet: top mass yields left while the contact
        # point and ground stay fixed. This shows displacement without redesign.
        shear = 0.105
        integrated = integrated.transform(
            integrated.size,
            Image.Transform.AFFINE,
            (1, -shear, shear * ground, 0, 1, 0),
            resample=Image.Resampling.BICUBIC,
        )
    return integrated


def contact_impact_layer() -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    rng = np.random.default_rng(705)

    # Compression streaks make the BREAKER force read right-to-left.
    for idx in range(18):
        y = int(rng.integers(275, 655))
        x1 = int(rng.integers(1120, 1500))
        length = int(rng.integers(80, 260))
        alpha = int(rng.integers(28, 80))
        draw.line((x1, y, x1 + length, y - int(rng.integers(-8, 9))), fill=(126, 210, 220, alpha), width=int(rng.integers(2, 6)))

    # Contact itself is a hard pressure snap, not an explosion or beam.
    contact = (731, 505)
    for radius, alpha, width in ((80, 70, 7), (48, 120, 5), (22, 210, 4)):
        draw.arc((contact[0] - radius, contact[1] - radius, contact[0] + radius, contact[1] + radius), 205, 335, fill=(226, 248, 242, alpha), width=width)
    for idx in range(20):
        angle = rng.uniform(math.radians(140), math.radians(220))
        length = rng.uniform(24, 92)
        x2 = contact[0] + math.cos(angle) * length
        y2 = contact[1] + math.sin(angle) * length
        draw.line((contact[0], contact[1], x2, y2), fill=(215, 240, 234, int(rng.integers(90, 210))), width=int(rng.integers(2, 6)))

    # Guardian foot scrape and shared ground dust show displacement and load.
    smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    for base_x, base_y, count in ((470, 798, 24), (730, 804, 18), (878, 809, 26)):
        for _ in range(count):
            rx = int(rng.integers(18, 64))
            ry = int(rng.integers(10, 34))
            x = int(base_x + rng.normal(0, 58))
            y = int(base_y + rng.normal(0, 16))
            alpha = int(rng.integers(28, 95))
            sd.ellipse((x - rx, y - ry, x + rx, y + ry), fill=(154, 158, 151, alpha))
    smoke = smoke.filter(ImageFilter.GaussianBlur(7))
    layer.alpha_composite(smoke)
    draw = ImageDraw.Draw(layer)
    for idx in range(28):
        x = int(rng.integers(370, 930))
        y = int(rng.integers(775, 835))
        r = int(rng.integers(2, 8))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(85, 91, 88, int(rng.integers(90, 190))))
    draw.line((335, 831, 585, 815), fill=(66, 74, 76, 170), width=7)
    draw.line((374, 844, 610, 827), fill=(54, 61, 64, 130), width=4)
    return layer


def cinematic_lighting_layer() -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((620, 392, 860, 630), fill=(188, 235, 231, 92))
    glow = glow.filter(ImageFilter.GaussianBlur(56))
    layer.alpha_composite(glow)

    rain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rain)
    rng = np.random.default_rng(1705)
    for _ in range(185):
        x = int(rng.integers(0, W))
        y = int(rng.integers(0, H))
        length = int(rng.integers(10, 34))
        rd.line((x, y, x - 7, y + length), fill=(175, 220, 231, int(rng.integers(25, 76))), width=1)
    layer.alpha_composite(rain)

    vignette = Image.new("L", (W, H), 0)
    yy, xx = np.mgrid[0:H, 0:W]
    nx = (xx - W / 2) / (W / 2)
    ny = (yy - H / 2) / (H / 2)
    edge = np.clip((nx * nx + ny * ny - 0.34) / 0.72, 0, 1)
    vignette = Image.fromarray((edge * 135).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(24))
    black = Image.new("RGBA", (W, H), (2, 8, 13, 0))
    black.putalpha(vignette)
    layer.alpha_composite(black)
    return layer


def generate_cutin(identity) -> dict[str, Image.Image]:
    with Image.open(BG_SOURCE) as source:
        background = ImageOps.fit(source.convert("RGBA"), (W, H), Image.Resampling.LANCZOS)
    background = ImageEnhance.Color(background).enhance(0.82)
    background = ImageEnhance.Contrast(background).enhance(1.06)

    guardian = actor_layer(identity, "guardian", 542, 812, 1.58)
    breaker = actor_layer(identity, "breaker", 1047, 820, 1.82)
    impact = contact_impact_layer()
    lighting = cinematic_lighting_layer()

    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for layer in (background, guardian, breaker, impact, lighting):
        composite.alpha_composite(layer)

    layers = {
        "R05_CUTIN_GIANT_CONTACT_BG_1600x900.png": background,
        "R05_CUTIN_GIANT_CONTACT_GUARDIAN_1600x900.png": guardian,
        "R05_CUTIN_GIANT_CONTACT_BREAKER_1600x900.png": breaker,
        "R05_CUTIN_GIANT_CONTACT_IMPACT_1600x900.png": impact,
        "R05_CUTIN_GIANT_CONTACT_LIGHTING_1600x900.png": lighting,
        "R05_CUTIN_GIANT_CONTACT_1600x900.png": composite,
    }
    for name, image in layers.items():
        save_rgba(image, CUTIN / name)
    return layers


def contact_dust_frame(frame_index: int) -> Image.Image:
    image = Image.new("RGBA", (FRAME, FRAME), (0, 0, 0, 0))
    rng = np.random.default_rng(4100)
    progress = frame_index / (FRAME_COUNT - 1)
    fade = math.sin(math.pi * min(1.0, progress * 1.1)) ** 0.7
    soft = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(soft)
    for particle in range(34):
        angle = rng.uniform(math.radians(195), math.radians(345))
        speed = rng.uniform(22, 112)
        bx = 128 + math.cos(angle) * speed * progress
        by = 222 + math.sin(angle) * speed * progress - 28 * progress
        rx = 5 + progress * rng.uniform(7, 20)
        ry = 3 + progress * rng.uniform(4, 11)
        alpha = int((115 - 58 * progress) * fade * rng.uniform(0.55, 1.0))
        draw.ellipse((bx - rx, by - ry, bx + rx, by + ry), fill=(157, 160, 151, max(0, alpha)))
    soft = soft.filter(ImageFilter.GaussianBlur(3 + 2 * progress))
    image.alpha_composite(soft)
    draw = ImageDraw.Draw(image)
    for particle in range(22):
        angle = rng.uniform(math.radians(200), math.radians(340))
        speed = rng.uniform(28, 126)
        x = 128 + math.cos(angle) * speed * progress
        y = 224 + math.sin(angle) * speed * progress - 18 * progress * progress
        r = rng.uniform(1.2, 4.5) * (1 - 0.35 * progress)
        alpha = int(210 * (1 - progress) ** 0.65)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(79, 86, 82, max(0, alpha)))
    return image


def artillery_hit_frame(frame_index: int) -> Image.Image:
    image = Image.new("RGBA", (FRAME, FRAME), (0, 0, 0, 0))
    rng = np.random.default_rng(5200)
    progress = frame_index / (FRAME_COUNT - 1)
    center = (128, 128)

    if frame_index <= 3:
        glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        radius = 12 + frame_index * 24
        alpha = (230, 255, 185, 100)[frame_index]
        gd.ellipse((128 - radius, 128 - radius, 128 + radius, 128 + radius), fill=(255, 247, 224, alpha))
        glow = glow.filter(ImageFilter.GaussianBlur(5 + frame_index * 4))
        image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)
    spark_fade = max(0.0, 1.0 - progress)
    for spark in range(30):
        angle = rng.uniform(0, math.tau)
        speed = rng.uniform(28, 142)
        distance = speed * min(1.0, progress * 1.55)
        x2 = center[0] + math.cos(angle) * distance
        y2 = center[1] + math.sin(angle) * distance
        tail = 8 + 24 * spark_fade
        x1 = x2 - math.cos(angle) * tail
        y1 = y2 - math.sin(angle) * tail
        color = (255, int(rng.integers(145, 231)), 45, int(230 * spark_fade))
        draw.line((x1, y1, x2, y2), fill=color, width=int(rng.integers(2, 5)))

    # Black shell fragments remain separate from flash and sparks.
    for fragment in range(15):
        angle = rng.uniform(0, math.tau)
        distance = rng.uniform(22, 112) * min(1.0, progress * 1.35)
        x = center[0] + math.cos(angle) * distance
        y = center[1] + math.sin(angle) * distance + 48 * progress * progress
        size = rng.uniform(3, 10) * (1 - 0.3 * progress)
        alpha = int(235 * (1 - 0.62 * progress))
        pts = [(x - size, y - size / 2), (x + size, y - size), (x + size / 2, y + size), (x - size / 2, y + size / 2)]
        draw.polygon(pts, fill=(13, 22, 25, max(0, alpha)))

    if frame_index >= 3:
        smoke = Image.new("RGBA", image.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(smoke)
        for puff in range(14):
            x = 128 + rng.normal(0, 26 + 36 * progress)
            y = 128 + rng.normal(-18 * progress, 18 + 24 * progress)
            r = rng.uniform(8, 24) * (0.5 + progress)
            alpha = int(82 * (1 - progress * 0.65))
            sd.ellipse((x - r, y - r, x + r, y + r), fill=(32, 40, 42, alpha))
        image.alpha_composite(smoke.filter(ImageFilter.GaussianBlur(6)))
    return image


def red_charge_frame(frame_index: int) -> Image.Image:
    image = Image.new("RGBA", (FRAME, FRAME), (0, 0, 0, 0))
    phase = math.tau * frame_index / FRAME_COUNT
    pulse = 0.5 + 0.5 * math.sin(phase)
    center = (128, 128)

    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for radius, alpha in ((76 + 8 * pulse, 24), (52 + 7 * pulse, 52), (31 + 5 * pulse, 92)):
        gd.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=(255, 33, 42, int(alpha * (0.7 + 0.3 * pulse))), width=8)
    gd.rounded_rectangle((75, 117, 181, 139), radius=9, fill=(132, 8, 18, 170))
    gd.rounded_rectangle((82, 121, 174, 135), radius=6, fill=(255, 35, 43, 225))
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((78, 118, 178, 138), radius=8, fill=(89, 5, 12, 220), outline=(240, 27, 37, 230), width=3)
    draw.rounded_rectangle((84, 123, 172, 133), radius=5, fill=(255, 63, 65, int(210 + 35 * pulse)))
    for ring_index in range(3):
        radius = 38 + ring_index * 24 + 5 * math.sin(phase + ring_index * 1.9)
        start = math.degrees(phase + ring_index * 1.3) % 360
        draw.arc((128 - radius, 128 - radius, 128 + radius, 128 + radius), start, start + 72, fill=(255, 60, 68, 150 - ring_index * 28), width=3)
        draw.arc((128 - radius, 128 - radius, 128 + radius, 128 + radius), start + 180, start + 242, fill=(255, 80, 84, 120 - ring_index * 24), width=2)
    # No line exits the circular charge volume: this is charge-only, never a beam.
    return image


def build_atlas(frame_fn, output_path: Path) -> tuple[Image.Image, list[Image.Image]]:
    frames = [frame_fn(index) for index in range(FRAME_COUNT)]
    atlas = Image.new("RGBA", (ATLAS_W, FRAME), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * FRAME, 0))
    save_rgba(atlas, output_path)
    return atlas, frames


def map_b_composite() -> Image.Image:
    paths = [
        PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_BASE_2400x1350.png",
        PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_BUILDINGS_2400x1350.png",
        PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_ROOFS_2400x1350.png",
        PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_FOREGROUND_2400x1350.png",
    ]
    with Image.open(paths[0]) as base:
        result = base.convert("RGBA")
    for path in paths[1:]:
        with Image.open(path) as layer:
            result.alpha_composite(layer.convert("RGBA"))
    return result


def framed_preview(image: Image.Image, size: tuple[int, int], background: Image.Image | None = None) -> Image.Image:
    if background is None:
        result = Image.new("RGBA", size, (5, 9, 12, 255))
    else:
        result = ImageOps.fit(background.convert("RGBA"), size, Image.Resampling.LANCZOS)
    overlay = ImageOps.contain(image.convert("RGBA"), size, Image.Resampling.LANCZOS)
    result.alpha_composite(overlay, ((size[0] - overlay.width) // 2, (size[1] - overlay.height) // 2))
    return result


def generate_review(composite: Image.Image, fx_frames: dict[str, list[Image.Image]]) -> Image.Image:
    width, height = 1280, 720
    board = Image.new("RGBA", (width, height), (10, 18, 24, 255))
    draw = ImageDraw.Draw(board)
    title = ImageFont.truetype(str(FONT_BOLD), 26)
    body = ImageFont.truetype(str(FONT), 15)
    small = ImageFont.truetype(str(FONT), 12)

    draw.rectangle((0, 0, width, 52), fill=(6, 12, 17, 255))
    draw.rectangle((0, 50, width, 53), fill=(72, 200, 192, 255))
    draw.text((22, 12), "R05 REPRESENTATIVE PERFORMANCE REVIEW", font=title, fill=(235, 243, 242, 255))
    draw.text((1258, 19), "Candidate · parent-derived · runtime_allowed=false · U1 pending", font=small, fill=(236, 194, 93, 255), anchor="ra")

    main = ImageOps.fit(composite, (820, 461), Image.Resampling.LANCZOS)
    contact_fx = fx_frames["CONTACT_DUST"][3].resize((330, 330), Image.Resampling.LANCZOS)
    main.alpha_composite(contact_fx, (354, 174))
    board.alpha_composite(main, (22, 72))
    draw.rectangle((22, 72, 842, 533), outline=(69, 91, 98, 255), width=2)
    draw.text((36, 91), "GIANT CONTACT / displaced Guardian / deflected charge line", font=body, fill=(226, 239, 236, 255))

    map_background = map_b_composite()
    rows = [
        ("CONTACT_DUST", fx_frames["CONTACT_DUST"][3]),
        ("ARTILLERY_HIT", fx_frames["ARTILLERY_HIT"][3]),
        ("RED_CHARGE", fx_frames["RED_CHARGE"][3]),
    ]
    for index, (label, frame) in enumerate(rows):
        y = 72 + index * 154
        draw.rounded_rectangle((862, y, 1258, y + 142), radius=6, fill=(18, 31, 39, 255), outline=(58, 81, 88, 255), width=1)
        black_preview = framed_preview(frame, (128, 108))
        map_preview = framed_preview(frame, (224, 108), map_background)
        board.alpha_composite(black_preview, (875, y + 25))
        board.alpha_composite(map_preview, (1019, y + 25))
        draw.text((875, y + 7), label, font=small, fill=(78, 211, 200, 255))
        draw.text((939, y + 131), "BLACK", font=small, fill=(143, 159, 162, 255), anchor="mm")
        draw.text((1131, y + 131), "A4 MAP-B", font=small, fill=(143, 159, 162, 255), anchor="mm")

    draw.rounded_rectangle((22, 554, 1258, 686), radius=6, fill=(18, 31, 39, 255), outline=(58, 81, 88, 255), width=1)
    draw.text((40, 572), "AUTHORIZED REVIEW SET", font=body, fill=(236, 194, 93, 255))
    draw.text((40, 603), "1 layered cut-in · 3 reusable 8-frame FX atlases · original non-voice audio set", font=body, fill=(226, 239, 236, 255))
    draw.text((40, 632), "STOP: no map atlas · no road states · no other cut-ins · no Godot · no Runtime handoff", font=body, fill=(165, 181, 183, 255))
    draw.text((40, 660), "RED_CHARGE is contained accumulation only: no beam, no release, no shield impact, no P1", font=body, fill=(239, 102, 101, 255))
    draw.text((1258, 706), "1280×720 review-only composite", font=small, fill=(128, 146, 149, 255), anchor="ra")
    save_rgba(board, REVIEW / "R05_REPRESENTATIVE_REVIEW_1280x720.png")
    return board


def main() -> None:
    validate_sources()
    identity = load_identity_module()
    CUTIN.mkdir(parents=True, exist_ok=True)
    FX.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)

    cutin_layers = generate_cutin(identity)
    _, contact_frames = build_atlas(contact_dust_frame, FX / "R05_FX_CONTACT_DUST_2048x256.png")
    _, artillery_frames = build_atlas(artillery_hit_frame, FX / "R05_FX_ARTILLERY_HIT_2048x256.png")
    _, red_frames = build_atlas(red_charge_frame, FX / "R05_FX_RED_CHARGE_2048x256.png")
    generate_review(
        cutin_layers["R05_CUTIN_GIANT_CONTACT_1600x900.png"],
        {"CONTACT_DUST": contact_frames, "ARTILLERY_HIT": artillery_frames, "RED_CHARGE": red_frames},
    )
    print("generated limited A7 Candidate visuals")


if __name__ == "__main__":
    main()
