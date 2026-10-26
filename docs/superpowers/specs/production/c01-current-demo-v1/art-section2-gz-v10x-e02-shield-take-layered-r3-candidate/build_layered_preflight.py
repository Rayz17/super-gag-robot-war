#!/usr/bin/env python3
"""Build the R3 body-only pose guide and a rejected cold-layer diagnostic.

No ImageGen pixels are created here. The accepted A17 exterior is subjected to
a documented, fixed source-space harmonic restoration attempt. The attempt is
retained only as PRE_IMAGEGEN failure evidence: it visibly blurs a large band
and must never be used as a positive input or Candidate. The body guide contains
no shield, plate, wall rack, or identity design.
"""

from __future__ import annotations

from hashlib import sha256
from math import cos, radians, sin
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[5]
GUIDE = ROOT / "guide"
PREFLIGHT_FAIL = ROOT / "preflight-fail"

V10X_SOUTH = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png"
A17_FRONT = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png"
A17_REAR_MAP = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/map-candidates/A17_SHIELD_REAR_INTERIOR_MAP_CANDIDATE_256x256.png"

EXPECTED = {
    V10X_SOUTH: "d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796",
    A17_FRONT: "8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47",
    A17_REAR_MAP: "98aaeb90ce155dffa89b56d42c9e137aeb43a3fb061f37f079a77bfc89107be7",
}

SCALE = 2
W = H = 1024


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for name in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def p(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(x * SCALE, y * SCALE) for x, y in points]


def ellipse(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], **kwargs: object) -> None:
    draw.ellipse(tuple(v * SCALE for v in box), **kwargs)


def line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], width: int, **kwargs: object) -> None:
    draw.line(p(points), width=width * SCALE, joint="curve", **kwargs)


def body_only_guide() -> Image.Image:
    canvas = Image.new("RGBA", (W * SCALE, H * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)

    # Registration plane only; not a wall rack or held prop.
    d.polygon(p([(390, 858), (650, 702), (814, 800), (555, 956)]), fill=(55, 75, 92, 30), outline=(83, 111, 132, 92))

    # Asymmetric loaded step from the already-passed take guide.
    d.polygon(p([(585, 541), (665, 560), (696, 720), (630, 758), (571, 690)]), fill=(108, 118, 126, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(628, 742), (708, 732), (760, 782), (716, 824), (622, 814)]), fill=(90, 100, 108, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(505, 536), (575, 552), (566, 733), (489, 779), (449, 689)]), fill=(129, 138, 145, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(478, 758), (563, 737), (602, 792), (547, 842), (449, 835)]), fill=(105, 115, 123, 255), outline=(39, 47, 54, 255))

    d.polygon(p([(493, 474), (599, 456), (646, 527), (576, 577), (486, 548)]), fill=(88, 98, 106, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(468, 279), (588, 252), (664, 336), (614, 483), (500, 501), (431, 398)]), fill=(120, 130, 138, 255), outline=(39, 47, 54, 255))
    d.polygon(p([(460, 303), (542, 280), (611, 337), (580, 430), (494, 451), (449, 391)]), fill=(147, 154, 160, 255), outline=(62, 70, 77, 255))
    d.polygon(p([(478, 218), (535, 190), (584, 224), (570, 289), (510, 304), (467, 265)]), fill=(98, 108, 116, 255), outline=(39, 47, 54, 255))
    line(d, [(508, 251), (466, 276)], width=10, fill=(236, 177, 58, 255))

    ellipse(d, (405, 293, 490, 378), fill=(92, 102, 110, 255), outline=(39, 47, 54, 255))
    ellipse(d, (596, 290, 682, 377), fill=(92, 102, 110, 255), outline=(39, 47, 54, 255))

    # The future rear-handle centres are deliberately on a -22 degree line,
    # matching the rolled A17 shield. Both complete arm chains remain visible.
    left_hand = (330, 640)
    right_hand = (465, 585)
    line(d, [(445, 347), (390, 475), left_hand], width=48, fill=(105, 115, 123, 255))
    line(d, [(641, 348), (565, 455), right_hand], width=48, fill=(105, 115, 123, 255))
    ellipse(d, (left_hand[0] - 28, left_hand[1] - 28, left_hand[0] + 28, left_hand[1] + 28), fill=(62, 70, 77, 255), outline=(236, 177, 58, 255), width=10 * SCALE)
    ellipse(d, (right_hand[0] - 28, right_hand[1] - 28, right_hand[0] + 28, right_hand[1] + 28), fill=(62, 70, 77, 255), outline=(236, 177, 58, 255), width=10 * SCALE)

    return canvas.resize((W, H), Image.Resampling.LANCZOS)


def rejected_harmonic_cold_attempt(front: Image.Image) -> tuple[Image.Image, Image.Image]:
    """Reproduce the rejected harmonic attempt for failure evidence only.

    The line and widths are frozen in the accepted A17 front master space. Each
    pixel in the narrow future-mark band is harmonically reconstructed from its
    untouched boundary. Visual QA rejected the output because the band destroys
    panel texture and changes the accepted A17 shield identity.
    """
    arr = np.asarray(front.convert("RGBA"), dtype=np.float32)
    out = arr.copy()
    h, w = arr.shape[:2]
    yy, xx = np.indices((h, w), dtype=np.float32)

    p0 = np.array([238.0, 674.0], dtype=np.float32)
    p1 = np.array([625.0, 463.0], dtype=np.float32)
    direction = p1 - p0
    length = float(np.linalg.norm(direction))
    unit = direction / length
    normal = np.array([-unit[1], unit[0]], dtype=np.float32)

    dx = xx - p0[0]
    dy = yy - p0[1]
    t = (dx * unit[0] + dy * unit[1]) / length
    signed = dx * normal[0] + dy * normal[1]
    outer = 62.0
    active = (t >= -0.025) & (t <= 1.035) & (np.abs(signed) <= outer) & (arr[:, :, 3] > 0)

    # Initialize with the mean of the two untouched sides, then solve the
    # discrete Laplace equation inside the fixed mask. Boundary pixels remain
    # byte-identical to A17.
    sample_offset = 68.0
    sx_minus = np.clip(np.rint(xx - normal[0] * sample_offset), 0, w - 1).astype(np.int32)
    sy_minus = np.clip(np.rint(yy - normal[1] * sample_offset), 0, h - 1).astype(np.int32)
    sx_plus = np.clip(np.rint(xx + normal[0] * sample_offset), 0, w - 1).astype(np.int32)
    sy_plus = np.clip(np.rint(yy + normal[1] * sample_offset), 0, h - 1).astype(np.int32)
    minus = arr[sy_minus, sx_minus, :3]
    plus = arr[sy_plus, sx_plus, :3]
    work = arr[:, :, :3].copy()
    work[active] = ((minus + plus) * 0.5)[active]
    active_y, active_x = np.where(active)
    y0, y1 = int(active_y.min()) - 2, int(active_y.max()) + 3
    x0, x1 = int(active_x.min()) - 2, int(active_x.max()) + 3
    sub = work[y0:y1, x0:x1].copy()
    sub_active = active[y0:y1, x0:x1]
    for _ in range(900):
        padded = np.pad(sub, ((1, 1), (1, 1), (0, 0)), mode="edge")
        average = (
            padded[:-2, 1:-1]
            + padded[2:, 1:-1]
            + padded[1:-1, :-2]
            + padded[1:-1, 2:]
            + padded[:-2, :-2]
            + padded[:-2, 2:]
            + padded[2:, :-2]
            + padded[2:, 2:]
        ) / 8.0
        sub[sub_active] = average[sub_active]
    work[y0:y1, x0:x1] = sub
    out[:, :, :3] = work
    out[:, :, 3] = arr[:, :, 3]

    mask = np.zeros((h, w, 4), dtype=np.uint8)
    mask[:, :, 0] = np.where(active, 255, 0).astype(np.uint8)
    mask[:, :, 3] = np.where(active, 170, 0).astype(np.uint8)
    return Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8), "RGBA"), Image.fromarray(mask, "RGBA")


def resize_rgba_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    arr = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = arr[:, :, 3:4] / 255.0
    pre = np.concatenate((arr[:, :, :3] * alpha, arr[:, :, 3:4]), axis=2)
    resized = np.asarray(Image.fromarray(np.clip(np.rint(pre), 0, 255).astype(np.uint8), "RGBA").resize(size, Image.Resampling.LANCZOS), dtype=np.float32)
    out_alpha = resized[:, :, 3:4]
    safe = np.where(out_alpha > 0, out_alpha / 255.0, 1.0)
    rgb = np.where(out_alpha > 0, resized[:, :, :3] / safe, 0.0)
    return Image.fromarray(np.clip(np.rint(np.concatenate((rgb, out_alpha), axis=2)), 0, 255).astype(np.uint8), "RGBA")


def map_candidate(master: Image.Image) -> Image.Image:
    bbox = master.getchannel("A").getbbox()
    assert bbox is not None
    crop = master.crop(bbox)
    target_h = 208
    target_w = round(crop.width * target_h / crop.height)
    resized = resize_rgba_premultiplied(crop, (target_w, target_h))
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((256 - target_w) // 2, 224 - target_h))
    return canvas


def preflight_fail_qa(body: Image.Image, hot: Image.Image, cold: Image.Image, cold_map: Image.Image, mask: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (2000, 1400), (16, 24, 33, 255))
    d = ImageDraw.Draw(board)
    d.text((38, 28), "R3 PRE-IMAGEGEN STOP · BODY GUIDE PASS / COLD A17 RESTORATION FAIL", font=font(32, True), fill=(246, 248, 250, 255))
    d.text((38, 72), "No R2 pixels · ImageGen calls: 0 · harmonic output below is failure evidence, never a positive input", font=font(20), fill=(255, 178, 88, 255))

    body_50 = body.resize((512, 512), Image.Resampling.LANCZOS)
    for idx, bg in enumerate(((238, 236, 230, 255), (8, 15, 23, 255))):
        x = 28 + idx * 548
        y = 132
        d.rounded_rectangle((x, y, x + 520, y + 520), radius=14, fill=bg)
        board.alpha_composite(body_50, (x + 4, y + 4))
    d.text((38, 666), "50% body-only: complete V-shaped arm chains; two empty-hand targets; no shield/plate/rack", font=font(19, True), fill=(246, 198, 75, 255))

    # Hot/cold 100% crop reveals exactly what the deterministic band changes.
    crop = (170, 360, 700, 780)
    for label, image, x in (("A17 accepted future HOT", hot, 1120), ("R3 deterministic COLD", cold, 1558)):
        detail = image.crop(crop).resize((408, 324), Image.Resampling.LANCZOS)
        d.rounded_rectangle((x - 8, 130, x + 416, 462), radius=12, fill=(236, 233, 224, 255))
        board.alpha_composite(detail, (x, 134))
        d.text((x, 476), label, font=font(17, True), fill=(246, 248, 250, 255))

    # 50% cold layer on light/dark at map source scale.
    shield_2x = cold_map.resize((512, 512), Image.Resampling.NEAREST)
    for idx, bg in enumerate(((238, 236, 230, 255), (8, 15, 23, 255))):
        x = 1120 + idx * 438
        y = 620
        d.rounded_rectangle((x, y, x + 408, y + 408), radius=12, fill=bg)
        board.alpha_composite(shield_2x.resize((408, 408), Image.Resampling.NEAREST), (x, y))
    d.text((1120, 1044), "FAIL: removed heat trace but introduced a broad blurred diagonal band", font=font(18, True), fill=(255, 114, 114, 255))
    d.text((38, 1110), "Stop gate: exact pre-impact pixels are absent; tested deterministic fills alter panels, scars, or surface continuity.", font=font(20, True), fill=(255, 126, 126, 255))
    d.text((38, 1152), "No body ImageGen call, final composite, Candidate, socket, Godot binding, Runtime, or Canon promotion exists.", font=font(18), fill=(255, 198, 75, 255))
    return board


def main() -> None:
    for path, expected in EXPECTED.items():
        assert digest(path) == expected, f"source SHA drift: {path}"
    for directory in (GUIDE, PREFLIGHT_FAIL):
        directory.mkdir(parents=True, exist_ok=True)

    body = body_only_guide()
    body.save(GUIDE / "GZ_V10X_SHIELD_TAKE_SOUTH_BODY_ONLY_FUTURE_HANDLES_GUIDE_1024.png")
    body.resize((512, 512), Image.Resampling.LANCZOS).save(GUIDE / "GZ_V10X_SHIELD_TAKE_SOUTH_BODY_ONLY_FUTURE_HANDLES_GUIDE_50PCT.png")

    hot = Image.open(A17_FRONT).convert("RGBA")
    cold, mask = rejected_harmonic_cold_attempt(hot)
    cold.save(PREFLIGHT_FAIL / "A17_SHIELD_FRONT_EXTERIOR_COLD_HARMONIC_FAIL_MASTER_768x1152.png")
    mask.save(PREFLIGHT_FAIL / "A17_SHIELD_FUTURE_HOT_TRACE_HARMONIC_FAIL_MASK.png")
    cold_map = map_candidate(cold)
    cold_map.save(PREFLIGHT_FAIL / "A17_SHIELD_FRONT_EXTERIOR_COLD_HARMONIC_FAIL_MAP_256.png")
    preflight_fail_qa(body, hot, cold, cold_map, mask).save(PREFLIGHT_FAIL / "R3_LAYERED_BODY_AND_COLD_SHIELD_PREFLIGHT_FAIL_50_100_QA.png")


if __name__ == "__main__":
    main()
