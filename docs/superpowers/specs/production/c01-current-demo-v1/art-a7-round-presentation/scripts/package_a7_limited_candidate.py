#!/usr/bin/env python3.13
"""Build the producer-authorized A7 limited Candidate media package.

Inputs are restricted to the 13:25 direction-pass master, its clean plate,
the frozen identity/packing evidence, and the three already-created FX atlases.
No previs-only or rejected-exploration media is opened by this script.
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


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
AUDIO = TARGET / "audio"
REVIEW = TARGET / "review"
SOURCE = TARGET / "source"

APPROVED_MASTER = SOURCE / "approved/R05_CUTIN_GIANT_CONTACT_1325_APPROVED_MASTER.png"
CLEAN_PLATE = SOURCE / "imagegen/R05_CUTIN_GIANT_CONTACT_BG_CLEANPLATE_imagegen_source.png"
MAP_B_BASE = PRODUCTION / "art-a4-map-b-six-layer/A4_MAP_B_BASE_2400x1350.png"

W = 1600
H = 900
SR = 48_000
TARGET_PEAK_DBFS = -4.0
TARGET_PEAK = 10 ** (TARGET_PEAK_DBFS / 20.0)
RNG = np.random.default_rng(70520260818)

FIXED_SHA256 = {
    PRODUCTION / "42-c01e02-m3-r0-5-media-packing-v2.json": "fe75667eac656756e35ddbbb784e250d39c0f8b05c2c14f719234d653b944012",
    PRODUCTION / "45-c01e02-m3-r0-5-a7-identity-lock-producer-review.md": "a90314f6357d18874e78c56312412e4253badc1365a8710e6c723471a064ca57",
    TARGET / "A7_IDENTITY_LOCK_GUARDIAN_C_BREAKER_BX_2400x1600.png": "4aed7359548052bf11b6624bfe2cce79462b0266afd99358fabc702deebde575",
    APPROVED_MASTER: "b7430a2a03b7de4bd7f55ebe3d3aeb2ea4c71c6fcc49f0d8e367026d6070c630",
    CLEAN_PLATE: "88650d79b614356e90dac98495205094046f6e7b2378e626eb81286de7a08758",
    FX / "R05_FX_ARTILLERY_HIT_2048x256.png": "4ff5f3b5b6376e6f473a7f5612a0c14224fd04528750318cc3a10a6c80598caf",
    FX / "R05_FX_RED_CHARGE_2048x256.png": "29ae2c1975503ac7363255710ed4cf17fc003b9931e65f7eeaa4a57871210a0c",
}

AUDIO_SLOTS = [
    ("R05_SFX_COMMS_OPEN", 180, 2, False),
    ("R05_SFX_COMMS_CLOSE", 160, 2, False),
    ("R05_SFX_CURSOR", 60, 2, False),
    ("R05_SFX_CONFIRM", 160, 2, False),
    ("R05_SFX_ILLEGAL", 220, 2, False),
    ("R05_SFX_SUMMARY_OPEN", 240, 2, False),
    ("R05_SFX_HOLD_LOOP", 1000, 2, True),
    ("R05_SFX_FOOTSTEP", 450, 1, False),
    ("R05_SFX_ROAD_BREAK", 1200, 1, False),
    ("R05_SFX_VEHICLE_PASS", 1200, 1, False),
    ("R05_SFX_SWARM_RUSH", 750, 1, False),
    ("R05_SFX_GIANT_CONTACT", 1400, 1, False),
    ("R05_SFX_ARTILLERY_HIT", 1250, 1, False),
    ("R05_SFX_RED_CHARGE_LOOP", 1500, 1, True),
    ("R05_SFX_RED_CHARGE_STING", 2500, 1, False),
    ("R05_SFX_RAIN_ALERT_AMBIENCE", 36000, 2, True),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_fixed_sources() -> None:
    for path, expected in FIXED_SHA256.items():
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"fixed source hash mismatch: {path}: {actual}")


def correct_contact_dust_tail() -> None:
    path = FX / "R05_FX_CONTACT_DUST_2048x256.png"
    with Image.open(path) as source:
        atlas = source.convert("RGBA")
    if atlas.size != (2048, 256):
        raise RuntimeError(f"contact dust atlas size mismatch: {atlas.size}")
    source_frame = atlas.crop((6 * 256, 0, 7 * 256, 256))
    tail = source_frame.copy()
    alpha = tail.getchannel("A").point(lambda value: round(value * 0.22))
    tail.putalpha(alpha)
    atlas.paste(Image.new("RGBA", (256, 256), (0, 0, 0, 0)), (7 * 256, 0))
    atlas.alpha_composite(tail, (7 * 256, 0))
    atlas.save(path, format="PNG", optimize=True)


def polygon_mask(polygons: list[list[tuple[int, int]]]) -> np.ndarray:
    image = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(image)
    for polygon in polygons:
        draw.polygon(polygon, fill=255)
    return np.asarray(image, dtype=np.uint8) > 0


def guardian_mask() -> np.ndarray:
    return polygon_mask([
        [(429, 228), (466, 207), (529, 205), (565, 229), (580, 268), (566, 315), (533, 326), (465, 321), (431, 296), (420, 260)],
        [(323, 256), (395, 244), (433, 261), (456, 299), (451, 358), (431, 420), (397, 443), (350, 439), (310, 414), (282, 365), (280, 301)],
        [(582, 306), (626, 296), (661, 312), (688, 341), (699, 382), (687, 420), (668, 458), (636, 482), (594, 460), (570, 426), (566, 356)],
        [(430, 306), (489, 293), (564, 299), (615, 323), (646, 360), (651, 422), (624, 477), (578, 527), (506, 544), (438, 524), (399, 485), (385, 429), (391, 355)],
        [(343, 350), (432, 338), (481, 349), (516, 378), (540, 422), (538, 454), (508, 487), (459, 500), (401, 486), (354, 462), (324, 428), (318, 389)],
        [(526, 342), (574, 337), (621, 348), (658, 374), (681, 407), (681, 445), (656, 476), (626, 491), (585, 478), (551, 454), (528, 424), (516, 383)],
        [(300, 479), (389, 486), (430, 518), (451, 559), (447, 602), (412, 651), (378, 701), (351, 748), (296, 777), (247, 786), (162, 786), (127, 769), (117, 728), (130, 690), (166, 645), (217, 588), (263, 532)],
        [(418, 493), (501, 493), (564, 512), (611, 553), (650, 606), (692, 663), (725, 710), (742, 754), (720, 785), (662, 790), (573, 787), (523, 773), (484, 744), (459, 695), (435, 639), (427, 579)],
    ])


def breaker_mask() -> np.ndarray:
    return polygon_mask([
        [(561, 276), (588, 230), (631, 186), (688, 143), (757, 102), (833, 72), (912, 49), (1010, 43), (1112, 47), (1211, 66), (1303, 97), (1383, 139), (1450, 194), (1501, 257), (1534, 325), (1544, 391), (1535, 445), (1510, 493), (1468, 530), (1418, 553), (1368, 563), (1315, 559), (1262, 544), (1218, 526), (1170, 503), (1127, 480), (1082, 454), (1032, 430), (985, 416), (941, 414), (899, 431), (863, 456), (815, 471), (773, 464), (738, 452), (703, 429), (674, 400), (652, 365), (621, 335), (581, 312)],
        [(668, 288), (718, 276), (794, 274), (844, 286), (873, 315), (888, 350), (887, 389), (870, 421), (843, 447), (812, 477), (754, 480), (709, 467), (678, 438), (660, 402), (656, 354)],
        [(898, 344), (952, 322), (1019, 328), (1062, 350), (1090, 387), (1112, 432), (1108, 471), (1088, 507), (1064, 539), (1036, 565), (1024, 600), (1016, 636), (1002, 677), (980, 718), (953, 759), (918, 782), (866, 786), (826, 779), (793, 759), (781, 728), (791, 695), (812, 664), (832, 627), (851, 588), (863, 547), (868, 504), (856, 466), (851, 426), (861, 383)],
        [(1032, 421), (1110, 405), (1192, 409), (1265, 434), (1316, 475), (1340, 526), (1337, 581), (1310, 620), (1272, 640), (1224, 640), (1188, 622), (1162, 589), (1137, 555), (1098, 536)],
        [(1292, 347), (1350, 342), (1401, 364), (1440, 395), (1470, 441), (1485, 486), (1494, 531), (1511, 576), (1543, 616), (1572, 655), (1590, 703), (1588, 747), (1567, 775), (1527, 788), (1489, 779), (1463, 753), (1445, 720), (1436, 681), (1432, 640), (1407, 609), (1380, 583), (1355, 550), (1338, 510), (1329, 462)],
        [(1125, 503), (1178, 491), (1230, 501), (1266, 532), (1280, 572), (1277, 625), (1260, 675), (1236, 716), (1202, 742), (1171, 746), (1146, 730), (1124, 701), (1112, 661), (1113, 610)],
        [(1370, 505), (1421, 498), (1460, 514), (1484, 547), (1497, 592), (1491, 638), (1476, 680), (1458, 719), (1436, 745), (1408, 752), (1384, 738), (1367, 708), (1359, 667), (1361, 617), (1358, 564)],
    ])


def impact_mask(master_rgb: np.ndarray, actor_union: np.ndarray) -> np.ndarray:
    broad = polygon_mask([
        [(0, 345), (301, 359), (526, 532), (665, 842), (0, 846)],
        [(370, 286), (828, 276), (1053, 620), (1057, 837), (380, 842)],
        [(602, 588), (1146, 580), (1175, 841), (602, 845)],
    ])
    luminance = (
        master_rgb[..., 0].astype(np.float32) * 0.2126
        + master_rgb[..., 1].astype(np.float32) * 0.7152
        + master_rgb[..., 2].astype(np.float32) * 0.0722
    )
    blurred = np.asarray(
        Image.fromarray(master_rgb, "RGB").filter(ImageFilter.GaussianBlur(4)),
        dtype=np.int16,
    )
    contrast = np.max(np.abs(master_rgb.astype(np.int16) - blurred), axis=2)
    particles = broad & (luminance > 52) & (contrast > 13)
    return particles & ~actor_union


def rgba_cutout(master_rgb: np.ndarray, mask: np.ndarray) -> Image.Image:
    rgba = np.zeros((H, W, 4), dtype=np.uint8)
    rgba[mask, :3] = master_rgb[mask]
    rgba[..., 3] = mask.astype(np.uint8) * 255
    return Image.fromarray(rgba, "RGBA")


def build_layers() -> dict[str, Path]:
    with Image.open(APPROVED_MASTER) as source:
        master = source.convert("RGB")
    if master.size != (W, H):
        raise RuntimeError(f"approved master size mismatch: {master.size}")
    with Image.open(CLEAN_PLATE) as source:
        clean = source.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)

    master_rgb = np.asarray(master, dtype=np.uint8)
    clean_rgb = np.asarray(clean, dtype=np.uint8)
    guardian = guardian_mask()
    breaker = breaker_mask() & ~guardian
    actors = guardian | breaker
    impact = impact_mask(master_rgb, actors)
    union = actors | impact

    bg_rgb = master_rgb.copy()
    bg_rgb[union] = clean_rgb[union]
    background = Image.fromarray(bg_rgb, "RGB").convert("RGBA")
    breaker_layer = rgba_cutout(master_rgb, breaker)
    guardian_layer = rgba_cutout(master_rgb, guardian)
    impact_layer = rgba_cutout(master_rgb, impact)
    composite = master.convert("RGBA")

    outputs = {
        "background": CUTIN / "R05_CUTIN_GIANT_CONTACT_BG_1600x900.png",
        "breaker": CUTIN / "R05_CUTIN_GIANT_CONTACT_BREAKER_1600x900.png",
        "guardian": CUTIN / "R05_CUTIN_GIANT_CONTACT_GUARDIAN_1600x900.png",
        "impact": CUTIN / "R05_CUTIN_GIANT_CONTACT_IMPACT_1600x900.png",
        "composite": CUTIN / "R05_CUTIN_GIANT_CONTACT_1600x900.png",
    }
    for key, image in (
        ("background", background),
        ("breaker", breaker_layer),
        ("guardian", guardian_layer),
        ("impact", impact_layer),
        ("composite", composite),
    ):
        outputs[key].parent.mkdir(parents=True, exist_ok=True)
        image.save(outputs[key], format="PNG", optimize=True)

    recomposed = background.copy()
    recomposed.alpha_composite(breaker_layer)
    recomposed.alpha_composite(guardian_layer)
    recomposed.alpha_composite(impact_layer)
    delta = np.abs(np.asarray(recomposed, dtype=np.int16) - np.asarray(composite, dtype=np.int16))
    if int(delta.max()) != 0:
        raise RuntimeError(f"layer recomposition is not pixel exact: max_delta={int(delta.max())}")
    return outputs


def frame_from_atlas(path: Path, frame_index: int = 4) -> Image.Image:
    with Image.open(path) as source:
        atlas = source.convert("RGBA")
    return atlas.crop((frame_index * 256, 0, (frame_index + 1) * 256, 256))


def fitted(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def build_review_images(composite_path: Path) -> dict[str, Path]:
    with Image.open(composite_path) as source:
        composite = source.convert("RGBA")
    representative = composite.resize((1280, 720), Image.Resampling.LANCZOS).convert("RGB")
    representative_path = REVIEW / "R05_REPRESENTATIVE_REVIEW_1280x720.png"
    representative_path.parent.mkdir(parents=True, exist_ok=True)
    representative.save(representative_path, format="PNG", optimize=True)

    board = Image.new("RGB", (1280, 720), (11, 17, 21))
    draw = ImageDraw.Draw(board)
    title_font = font(22)
    label_font = font(15)
    draw.text((24, 14), "R0.5 LIMITED FX TECHNICAL REVIEW | Candidate | no Runtime handoff", fill=(228, 234, 232), font=title_font)
    draw.text((24, 43), "Rows: black / A4 MAP-B / 1280x720 approved Cut-in crop", fill=(142, 165, 169), font=label_font)

    fx_items = [
        ("CONTACT_DUST", FX / "R05_FX_CONTACT_DUST_2048x256.png"),
        ("ARTILLERY_HIT", FX / "R05_FX_ARTILLERY_HIT_2048x256.png"),
        ("RED_CHARGE", FX / "R05_FX_RED_CHARGE_2048x256.png"),
    ]
    with Image.open(MAP_B_BASE) as source:
        map_base = fitted(source, (394, 188)).convert("RGBA")
    cutin_base = fitted(composite, (394, 188)).convert("RGBA")

    panel_w, panel_h = 394, 188
    x_positions = [24, 443, 862]
    y_positions = [78, 294, 510]
    for column, (slot, path) in enumerate(fx_items):
        fx_frame = frame_from_atlas(path, 4).resize((150, 150), Image.Resampling.LANCZOS)
        for row, y in enumerate(y_positions):
            if row == 0:
                panel = Image.new("RGBA", (panel_w, panel_h), (0, 0, 0, 255))
            elif row == 1:
                panel = map_base.copy()
            else:
                panel = cutin_base.copy()
            px = (panel_w - fx_frame.width) // 2
            py = 24 if row == 0 else 28
            panel.alpha_composite(fx_frame, (px, py))
            x = x_positions[column]
            board.paste(panel.convert("RGB"), (x, y))
            draw.rectangle((x, y, x + panel_w - 1, y + panel_h - 1), outline=(69, 91, 94), width=1)
            draw.text((x + 10, y + 7), slot, fill=(231, 235, 230), font=label_font)

    fx_review_path = REVIEW / "R05_FX_CONDITIONS_TECH_REVIEW_1280x720.png"
    board.save(fx_review_path, format="PNG", optimize=True)
    return {"representative_review": representative_path, "fx_technical_review": fx_review_path}


def chirp(t: np.ndarray, f0: float, f1: float, duration: float) -> np.ndarray:
    rate = (f1 - f0) / max(duration, 1e-9)
    return np.sin(2 * np.pi * (f0 * t + 0.5 * rate * t * t))


def gaussian(t: np.ndarray, center: float, width: float) -> np.ndarray:
    return np.exp(-0.5 * ((t - center) / width) ** 2)


def periodic_noise(sample_count: int, cutoff_hz: float, rng: np.random.Generator) -> np.ndarray:
    noise = rng.standard_normal(sample_count)
    spectrum = np.fft.rfft(noise)
    frequencies = np.fft.rfftfreq(sample_count, d=1 / SR)
    spectrum *= np.exp(-((frequencies / cutoff_hz) ** 4))
    output = np.fft.irfft(spectrum, n=sample_count)
    return output / max(float(np.max(np.abs(output))), 1e-9)


def stereoize(signal: np.ndarray, delay_samples: int = 17, width: float = 0.16, loop: bool = False) -> np.ndarray:
    if loop:
        delayed = np.roll(signal, delay_samples)
    else:
        delayed = np.zeros_like(signal)
        delayed[delay_samples:] = signal[:-delay_samples]
    left = signal * (1 + width) - delayed * width * 0.35
    right = signal * (1 - width * 0.25) + delayed * width
    return np.column_stack((left, right))


def edge_fade(signal: np.ndarray, milliseconds: float = 5.0) -> np.ndarray:
    count = min(int(SR * milliseconds / 1000), max(1, len(signal) // 4))
    ramp = np.sin(np.linspace(0, np.pi / 2, count, endpoint=True)) ** 2
    output = signal.copy()
    output[:count] *= ramp[:, None] if output.ndim == 2 else ramp
    output[-count:] *= ramp[::-1, None] if output.ndim == 2 else ramp[::-1]
    return output


def normalize(signal: np.ndarray, loop: bool) -> np.ndarray:
    output = np.asarray(signal, dtype=np.float64)
    output -= np.mean(output, axis=0, keepdims=True) if output.ndim == 2 else np.mean(output)
    if not loop:
        output = edge_fade(output)
    peak = float(np.max(np.abs(output)))
    if peak <= 1e-12:
        raise RuntimeError("silent audio candidate")
    return output * (TARGET_PEAK / peak)


def make_audio(slot_id: str, duration_ms: int, channels: int, loop: bool) -> np.ndarray:
    sample_count = int(SR * duration_ms / 1000)
    t = np.arange(sample_count, dtype=np.float64) / SR
    duration = duration_ms / 1000
    x = t / duration
    seed = int.from_bytes(hashlib.sha256(slot_id.encode("ascii")).digest()[:8], "little")
    rng = np.random.default_rng(seed)

    if slot_id == "R05_SFX_COMMS_OPEN":
        mono = chirp(t, 280, 2100, duration) * np.sin(np.pi * x) ** 1.5
        mono += 0.34 * np.sin(2 * np.pi * 2480 * t) * gaussian(t, 0.13, 0.035)
    elif slot_id == "R05_SFX_COMMS_CLOSE":
        mono = chirp(t, 1850, 240, duration) * np.sin(np.pi * x) ** 1.4
        mono += 0.25 * np.sin(2 * np.pi * 720 * t) * gaussian(t, 0.06, 0.025)
    elif slot_id == "R05_SFX_CURSOR":
        mono = np.sin(2 * np.pi * 1640 * t) * np.exp(-58 * t)
        mono += 0.25 * chirp(t, 2400, 1300, duration) * np.exp(-72 * t)
    elif slot_id == "R05_SFX_CONFIRM":
        mono = np.sin(2 * np.pi * 620 * t) * gaussian(t, 0.048, 0.026)
        mono += 0.78 * np.sin(2 * np.pi * 930 * t) * gaussian(t, 0.105, 0.035)
    elif slot_id == "R05_SFX_ILLEGAL":
        pulse = gaussian(t, 0.052, 0.022) + 0.86 * gaussian(t, 0.151, 0.026)
        mono = (np.sin(2 * np.pi * 178 * t) + 0.42 * np.sin(2 * np.pi * 233 * t)) * pulse
    elif slot_id == "R05_SFX_SUMMARY_OPEN":
        mono = 0.7 * chirp(t, 190, 1180, duration) * np.sin(np.pi * x) ** 1.3
        mono += 0.28 * chirp(t, 760, 2640, duration) * gaussian(t, 0.17, 0.06)
    elif slot_id == "R05_SFX_HOLD_LOOP":
        noise = periodic_noise(sample_count, 220, rng)
        mono = 0.42 * np.sin(2 * np.pi * 47 * t)
        mono += 0.21 * np.sin(2 * np.pi * 83 * t + 0.7)
        mono += 0.12 * np.sin(2 * np.pi * 131 * t + 1.4)
        mono += 0.08 * noise * (0.75 + 0.25 * np.sin(2 * np.pi * 3 * t))
    elif slot_id == "R05_SFX_FOOTSTEP":
        phase = 2 * np.pi * (72 * t - 34 * t * t / max(duration, 1e-9))
        mono = np.sin(phase) * np.exp(-9.5 * t)
        mono += 0.32 * np.sin(2 * np.pi * 390 * t) * np.exp(-15 * t)
        mono += 0.13 * rng.standard_normal(sample_count) * np.exp(-20 * t)
    elif slot_id == "R05_SFX_ROAD_BREAK":
        mono = 0.65 * np.sin(2 * np.pi * (45 * t - 8 * t * t)) * np.exp(-2.7 * t)
        mono += 0.24 * rng.standard_normal(sample_count) * np.exp(-3.8 * t)
        for center, scale in ((0.05, 0.6), (0.19, 0.42), (0.37, 0.31), (0.62, 0.22)):
            mono += scale * rng.standard_normal(sample_count) * gaussian(t, center, 0.012 + center * 0.015)
    elif slot_id == "R05_SFX_VEHICLE_PASS":
        phase = 2 * np.pi * (132 * t - 29 * t * t / duration)
        envelope = np.sin(np.pi * x) ** 1.1
        mono = (0.65 * np.sin(phase) + 0.18 * np.sin(2.03 * phase)) * envelope
        mono += 0.14 * periodic_noise(sample_count, 850, rng) * envelope
    elif slot_id == "R05_SFX_SWARM_RUSH":
        mono = np.zeros(sample_count)
        for index in range(7):
            start = 0.03 + index * 0.072
            local = np.clip(t - start, 0, duration)
            env = gaussian(t, start + 0.17, 0.12)
            mono += 0.16 * chirp(local, 190 + 43 * index, 1120 + 91 * index, duration) * env
        mono += 0.12 * periodic_noise(sample_count, 1900, rng) * np.sin(np.pi * x)
    elif slot_id == "R05_SFX_GIANT_CONTACT":
        phase = 2 * np.pi * (52 * t - 12 * t * t / duration)
        mono = 0.82 * np.sin(phase) * np.exp(-2.8 * t)
        mono += 0.34 * np.sin(2 * np.pi * 126 * t) * np.exp(-4.2 * t)
        mono += 0.22 * rng.standard_normal(sample_count) * np.exp(-5.3 * t)
        mono += 0.18 * chirp(t, 460, 105, duration) * np.sin(np.pi * x) ** 2
    elif slot_id == "R05_SFX_ARTILLERY_HIT":
        mono = 0.72 * rng.standard_normal(sample_count) * np.exp(-7.2 * t)
        phase = 2 * np.pi * (62 * t - 14 * t * t / duration)
        mono += 0.74 * np.sin(phase) * np.exp(-3.4 * t)
        for center in (0.12, 0.23, 0.41, 0.68):
            mono += 0.13 * rng.standard_normal(sample_count) * gaussian(t, center, 0.01 + center * 0.012)
    elif slot_id == "R05_SFX_RED_CHARGE_LOOP":
        pulse_rate = 2 / duration
        noise = periodic_noise(sample_count, 420, rng)
        mono = 0.46 * np.sin(2 * np.pi * 32 * t)
        mono += 0.22 * np.sin(2 * np.pi * 64 * t + 0.45)
        mono += 0.11 * np.sin(2 * np.pi * 128 * t + 1.1)
        mono += 0.10 * noise * (0.72 + 0.28 * np.sin(2 * np.pi * pulse_rate * t - np.pi / 2))
    elif slot_id == "R05_SFX_RED_CHARGE_STING":
        rise = np.clip(x / 0.78, 0, 1)
        mono = 0.40 * chirp(t, 54, 312, duration) * rise ** 1.4
        mono += 0.18 * chirp(t, 220, 1080, duration) * rise ** 2.1
        mono += 0.22 * np.sin(2 * np.pi * 38 * t) * gaussian(t, 2.08, 0.28)
        mono *= np.clip((duration - t) / 0.20, 0, 1)
    elif slot_id == "R05_SFX_RAIN_ALERT_AMBIENCE":
        rain_left = periodic_noise(sample_count, 9200, rng)
        rain_right = periodic_noise(sample_count, 8700, np.random.default_rng(seed ^ 0xA7A7A7A7))
        low_left = periodic_noise(sample_count, 560, np.random.default_rng(seed ^ 0x13579BDF))
        low_right = periodic_noise(sample_count, 610, np.random.default_rng(seed ^ 0x2468ACE0))
        left = 0.26 * (rain_left - 0.46 * low_left)
        right = 0.26 * (rain_right - 0.44 * low_right)
        left += 0.08 * np.sin(2 * np.pi * 37 * t + 0.2)
        right += 0.08 * np.sin(2 * np.pi * 37 * t + 0.55)
        stereo = np.column_stack((left, right))
        return normalize(stereo, loop=True)
    else:
        raise KeyError(slot_id)

    signal = stereoize(mono, loop=loop) if channels == 2 else mono
    return normalize(signal, loop)


def write_pcm24(path: Path, signal: np.ndarray) -> None:
    channels = 1 if signal.ndim == 1 else signal.shape[1]
    samples = np.clip(np.rint(signal * 8_388_607), -8_388_608, 8_388_607).astype(np.int32)
    flat = samples.reshape(-1)
    unsigned = (flat & 0xFFFFFF).astype(np.uint32)
    packed = np.empty((len(unsigned), 3), dtype=np.uint8)
    packed[:, 0] = unsigned & 0xFF
    packed[:, 1] = (unsigned >> 8) & 0xFF
    packed[:, 2] = (unsigned >> 16) & 0xFF
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(3)
        handle.setframerate(SR)
        handle.writeframes(packed.tobytes())


def ffprobe(path: Path) -> dict[str, object]:
    command = [
        "/opt/homebrew/bin/ffprobe",
        "-v", "error",
        "-show_entries", "stream=codec_name,sample_rate,channels,bits_per_sample,bits_per_raw_sample:format=duration",
        "-of", "json",
        str(path),
    ]
    return json.loads(subprocess.check_output(command, text=True))


def build_audio() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    rights_note = "Original deterministic procedural synthesis; no external samples, recordings, melodies, voice, or third-party library audio."
    for slot_id, duration_ms, channels, loop in AUDIO_SLOTS:
        signal = make_audio(slot_id, duration_ms, channels, loop)
        path = AUDIO / f"{slot_id}.wav"
        write_pcm24(path, signal)
        probe = ffprobe(path)
        stream = probe["streams"][0]
        detected_duration_ms = round(float(probe["format"]["duration"]) * 1000)
        peak = float(np.max(np.abs(signal)))
        record = {
            "slot_id": slot_id,
            "resource_path": str(path.relative_to(ROOT)),
            "codec": stream["codec_name"],
            "sample_rate": int(stream["sample_rate"]),
            "channels": int(stream["channels"]),
            "bits_per_sample": int(stream.get("bits_per_raw_sample") or stream.get("bits_per_sample") or 0),
            "duration_ms": detected_duration_ms,
            "sample_peak_dbfs": round(20 * math.log10(max(peak, 1e-12)), 3),
            "loop": loop,
            "loop_start_sample": 0 if loop else None,
            "loop_end_sample_exclusive": len(signal) if loop else None,
            "loop_boundary_delta": round(float(np.max(np.abs(signal[0] - signal[-1]))), 6) if loop else None,
            "rights_note": rights_note,
            "sha256": sha256(path),
        }
        records.append(record)
    probe_path = AUDIO / "audio-media-probe.json"
    probe_path.write_text(json.dumps({"probe_tool": "ffprobe", "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return records


def image_probe(paths: list[Path]) -> list[dict[str, object]]:
    records = []
    for path in paths:
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            alpha = rgba.getchannel("A")
            records.append({
                "resource_path": str(path.relative_to(ROOT)),
                "format": image.format,
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "has_alpha_channel": "A" in image.getbands(),
                "alpha_bbox": alpha.getbbox(),
                "sha256": sha256(path),
            })
    output = TARGET / "visual-media-probe.json"
    output.write_text(json.dumps({"probe_tool": "Pillow direct media decode", "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return records


def main() -> None:
    validate_fixed_sources()
    correct_contact_dust_tail()
    layers = build_layers()
    reviews = build_review_images(layers["composite"])
    build_audio()
    image_paths = list(layers.values()) + list(reviews.values()) + [
        TARGET / "A7_IDENTITY_LOCK_GUARDIAN_C_BREAKER_BX_2400x1600.png",
        APPROVED_MASTER,
        CLEAN_PLATE,
        FX / "R05_FX_CONTACT_DUST_2048x256.png",
        FX / "R05_FX_ARTILLERY_HIT_2048x256.png",
        FX / "R05_FX_RED_CHARGE_2048x256.png",
    ]
    image_probe(image_paths)
    print("A7 limited Candidate media package generated")
    print(f"layers={len(layers)} reviews={len(reviews)} audio={len(AUDIO_SLOTS)} fx=3")


if __name__ == "__main__":
    main()
