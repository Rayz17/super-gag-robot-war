#!/usr/bin/env python3
"""Mechanically pack the approved A3-A idle samples into two A5 atlas candidates."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]

PACKAGE_ID = "C01CDV1_A5_RIFT_SWARM_FOUR_FACING_ATLAS_V1"
SUBJECT_ID = "ENEMY_C01_RIFT_SWARM"
SLOT_ID = "ENEMY_C01CDV1_RIFT_SWARM_MASTER"
CANDIDATE_ID = "CAND_C01CDV1_A3_RIFT_SWARM_A_CARAPACE_CRAWLER_V1"
CANDIDATE_TITLE = "伏壳钳足型"
ORDER = ("north", "east", "south", "west")
SIZES = (96, 128)
PIVOT = "0.5,1.0"
FOOTPRINT = "1,1"
LIFECYCLE = "Candidate"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
PAPER = "#edf1ee"
PANEL = "#f8faf7"
INK_DEEP = "#07151b"
INK = "#182b32"
INK_SOFT = "#52666b"
IVORY = "#dfe4dc"
TEAL = "#59aaa3"
CORAL = "#e65b50"
GOLD = "#d6aa3d"

ATLAS_FILES = {
    96: "A5_RIFT_SWARM_A_IDLE_96_384x96.png",
    128: "A5_RIFT_SWARM_A_IDLE_128_512x128.png",
}

SAMPLE_HASHES = {
    ("north", 96): "45f549b2c4978cd0d2edb8ce3b227928dd24690cf7ae37106cb66be1430f6952",
    ("east", 96): "66ab008651b84f799d3c9cf7e1df7c8d9c9a0e21a5b248fca83d3f5fa37dc03a",
    ("south", 96): "e89224b2361e5a25ce1d31f4a8b6f78bf06e21d2ff3548d50ff18afbfb3f872e",
    ("west", 96): "a98a7b9c5db52fbfc6b731638aca6c4ac317a818de97c5150551ab2c5c63f81d",
    ("north", 128): "03f8f9c646a6f92c43d53ab3008012e87990390d2d8bf930ad4d897e77fc857c",
    ("east", 128): "9e1b06a783bfcb83f1ef77f73695c973b303225a860199cfdca1b72923b0bcd4",
    ("south", 128): "a1f496f06dfaa1c566a4320b49f62026f0541cfc24e271796ebd47ad7d0f716d",
    ("west", 128): "dad24d87d49f76c42c40c16bce0273174eef1106cbf3a51f4922db18eaed4385",
}


def sample_path(facing: str, size: int) -> str:
    return (
        "docs/superpowers/specs/production/c01-current-demo-v1/"
        f"art-a3-rift-swarm-qsd/samples/A3_A_{facing}_{size}_review.png"
    )


STATIC_SOURCES = (
    ("docs/superpowers/specs/production/c01-current-demo-v1/25-c01e02-a5-rift-swarm-four-facing-atlas-objective.md", "15209465805c0bec7a9fbe4b8403b81c6727dde7804a4c93a90227529a6c6d81", "a5_objective"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/27-c01e02-a5-m2-4-refreeze-resume-directive.md", "7f29715eb6d1e1e09d8faf5fb7b2d8d1a11948ddbd350a76a00bb8b995a5ad6c", "producer_refreeze_directive"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/28-c01e02-a5-bottom-contact-validator-correction.md", "bb744367a92b936e038760843ad57b1f46d0e7fc2414172f91b5111aada556de", "producer_contact_validator_correction"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/29-c01e02-a5-atlas-name-validator-correction.md", "0c5d458c9ff968b68dc1ffa8463065d228fad3b33f2d6c0d3e2bc4b43f920b77", "producer_atlas_name_validator_correction"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a5/a5-m2-4-refreeze-receipt.tsv", "938e404e5c22728006aa907069a9fb7e663bc536a6b3ce918e0836c599fd8f1e", "producer_refreeze_receipt"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a5/a5-refrozen-inputs.sha256", "7ef2553aff03036f787f692672987e4e2139931996fe68945b99d6f7c85b4702", "producer_refrozen_input_manifest"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/19-current-demo-inplace-rebase-producer-contract.md", "6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94", "producer_contract_r2"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/20-c01e02-j2-joint-integration-contract.md", "038bfb0d57aea64c1ca3a91cae7e1623a33d7c8aaeb7e7ae2af4541770ca3f0d", "joint_contract"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/21-c01e02-a3-rift-swarm-art-objective.md", "30dd540f56a6771a9d586d83cc3316a6f90a40b6aa29313d1222293091717f92", "a3_objective"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a3/a3-user-approval-receipt.tsv", "4698ab86e24483bbaf0bd95c5f72e9f2d9cf694f935a6176ee7862ed9465bab4", "a3_user_approval"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a3/a3-selected-source-hashes.sha256", "ff09490e4e0cad1c3f324c98397cd909d936a4d9447e42ff74c5c04783224355", "a3_selected_hash_manifest"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a3-rift-swarm-qsd/A3_candidate_a_identity_sheet_1800x1200.png", "6ccf90751b7a0312ce6876fc78796b28fa1be15ff4fd4de57e59871e2294cba2", "a3_selected_identity"),
    *((sample_path(facing, size), SAMPLE_HASHES[(facing, size)], f"a3_idle_{facing}_{size}") for size in SIZES for facing in ORDER),
    ("docs/superpowers/specs/production/c01-current-demo-v1/producer-a4/a4-user-approval-receipt.tsv", "dc402de8ee471953fa1de8b98676aa76a9826a2b219dc6010ba7e762f128781b", "a4_user_approval"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/asset-manifest.tsv", "035ba532001724f55287729fc4d227021baa3136779dc5be59686aaff4745b5d", "a4_asset_manifest"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/core-delivery-hashes.sha256", "450fbe15993dfa6891c7c2ecbef13339a131f91a13b2b35abf79ebedd88d7b29", "a4_delivery_hashes"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_six_layer_composite_full_2400x1350.png", "a352e0146c64d1bf33d697cf0256bba505689d49556de78a3b7f7bbfa560ba35", "a4_external_review_composite"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_west_1280x720.png", "1a6b4282d2067fa00a84302c2e2f045d7387898acf3cb05affb7a0262db88adb", "a4_west_review_viewport"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_central_1280x720.png", "b8ccc9b6eefb802b929a6d674e668611c6d9a88e123e24a2991710ae7e5f4ea9", "a4_central_review_viewport"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_east_1280x720.png", "e43d0b13317116952c5fbac111ae85d916ea383a89697a108c56f55dd5c51198", "a4_east_review_viewport"),
    ("game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/asset_slot_manifest_r2.json", "2cc85fc524b453b255c4d8aa521236e0845664f1a8721829da7a5befa21b93c9", "r2_slot_manifest"),
    ("game-godot/scripts/candidate_runtime_demo/c01/e02/c01e02_g1_runner.gd", "de31ba758bd0490bbfa60e411f090e72a5741be322365db33fbff37e0c6c6f06", "current_runner_idle_facing_reader"),
    ("docs/superpowers/specs/production/c01-current-demo-v1/main-m2-1/r2-instance-binding-receipt.tsv", "c494cb3359477ea327203a580c0752e653fccddecb7d51cc3abb41cf90a4bd51", "r2_instance_bindings"),
    ("docs/superpowers/specs/data/canon/authority_manifest.tsv", "51aedd8c9a8f7f4224e7e585e8a85e2a27c6b199fda430a6337eb270f03ba8bf", "canon_authority_manifest"),
    ("docs/superpowers/specs/data/canon/entities.tsv", "0b5b633bf575bb719fa0c4b1c2aedac87d037d2eaf424efe4732f9284764614e", "current_canon_entity"),
    ("docs/superpowers/specs/data/canon/scenes.tsv", "a2a4155847d6105f9b3067f7d0c4fad13e5b002cb999a135b199ac31e774dfb7", "current_canon_scene"),
)

CAMERAS = {
    "WEST": {
        "world_center": (-160, 320),
        "background": "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_west_1280x720.png",
    },
    "CENTRAL": {
        "world_center": (240, 480),
        "background": "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_central_1280x720.png",
    },
    "EAST": {
        "world_center": (830, 620),
        "background": "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_east_1280x720.png",
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.convert("RGBA").getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("A5 source sample has no visible pixels")
    return bbox


def red_seam_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgba_image = image.convert("RGBA")
    mask = Image.new("L", rgba_image.size, 0)
    source = rgba_image.load()
    target = mask.load()
    for y in range(rgba_image.height):
        for x in range(rgba_image.width):
            red, green, blue, alpha = source[x, y]
            if alpha > 64 and red > 170 and red > green * 1.45 and red > blue * 1.35:
                target[x, y] = 255
    bbox = mask.getbbox()
    if bbox is None:
        raise RuntimeError("A5 source sample red seam missing")
    return bbox


def validate_sources() -> list[dict[str, str]]:
    for relative, expected, _ in STATIC_SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"A5 frozen source missing: {relative}")
        actual = sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"A5 frozen source drift: {relative}: {actual}")

    a3 = load_tsv(ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-a3/a3-user-approval-receipt.tsv")
    if len(a3) != 1:
        raise RuntimeError("A5 requires one A3 approval row")
    a3_row = a3[0]
    required_a3 = {
        "subject_id": SUBJECT_ID,
        "runtime_slot_id": SLOT_ID,
        "selected_candidate_code": "A",
        "selected_candidate_id": CANDIDATE_ID,
        "movement_grammar": "diagonal_alternating_crawl",
        "instance_rule": "one_master_plus_six_light_variants",
        "runtime_allowed": "false",
        "runtime_handoff": "none",
    }
    for field, expected in required_a3.items():
        if a3_row.get(field) != expected:
            raise RuntimeError(f"A5 A3 receipt mismatch: {field}")

    for size in SIZES:
        for facing in ORDER:
            path = ROOT / sample_path(facing, size)
            with Image.open(path) as source:
                image = source.convert("RGBA")
            if image.size != (size, size) or source.mode != "RGBA":
                raise RuntimeError(f"A5 sample mode/size mismatch: {path}")
            alpha = image.getchannel("A")
            bbox = alpha_bbox(image)
            bottom_contact_bbox = alpha.crop((0, size - 1, size, size)).getbbox()
            if (
                bbox[3] != size
                or bottom_contact_bbox is None
                or not (bottom_contact_bbox[0] <= size // 2 < bottom_contact_bbox[2])
            ):
                raise RuntimeError(f"A5 bottom-center contact mismatch: {path}")
            if alpha.crop((0, 0, 1, size)).getbbox() or alpha.crop((size - 1, 0, size, size)).getbbox():
                raise RuntimeError(f"A5 sample lacks side-edge transparency: {path}")
            red_seam_bbox(image)

    a4 = load_tsv(ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/producer-a4/a4-user-approval-receipt.tsv")
    expected_layers = {"BASE", "BUILDINGS", "ROOFS", "FOREGROUND", "OCCLUSION_MASK", "STATE_LAYERS"}
    if len(a4) != 6 or {row.get("layer_code") for row in a4} != expected_layers:
        raise RuntimeError("A5 A4 six-layer approval set mismatch")
    for row in a4:
        if row.get("approval_scope") != "approved_as_demo_derivative_source":
            raise RuntimeError("A5 A4 approval scope mismatch")
        if row.get("runtime_allowed") != "false" or row.get("runtime_handoff") != "none":
            raise RuntimeError("A5 A4 runtime boundary mismatch")

    manifest_path = ROOT / "game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/asset_slot_manifest_r2.json"
    manifest = load_json(manifest_path)
    constraint = manifest.get("constraint_profiles", {}).get("qsd_1x1")
    expected_constraint = {
        "media_type": "image",
        "allowed_dimensions": [[384, 96], [512, 128]],
        "alpha": "required",
        "pivot": [0.5, 1.0],
        "atlas_required": True,
        "required_actions": ["idle"],
        "facings": list(ORDER),
    }
    if not constraint:
        raise RuntimeError("A5 qsd_1x1 constraint missing")
    for field, expected in expected_constraint.items():
        if constraint.get(field) != expected:
            raise RuntimeError(f"A5 qsd_1x1 mismatch: {field}")
    slot = next((row for row in manifest.get("slots", []) if row.get("slot_id") == SLOT_ID), None)
    if not slot or slot.get("expected_stable_id") != SUBJECT_ID or slot.get("constraint_profile") != "qsd_1x1":
        raise RuntimeError("A5 R2 slot identity mismatch")
    if slot.get("approved_asset_binding") is not None or slot.get("runtime_allowed") is not False:
        raise RuntimeError("A5 cannot pre-authorize R2 binding")

    runner = (ROOT / "game-godot/scripts/candidate_runtime_demo/c01/e02/c01e02_g1_runner.gd").read_text(encoding="utf-8")
    for token in ('var frame_id := "idle/%s" % facing', 'foot - source.size * pivot', '"swarm":\n\t\t\tslot_id = "ENEMY_C01CDV1_RIFT_SWARM_MASTER"'):
        if token not in runner:
            raise RuntimeError(f"A5 Runner contract token missing: {token}")

    instances = load_tsv(ROOT / "docs/superpowers/specs/production/c01-current-demo-v1/main-m2-1/r2-instance-binding-receipt.tsv")
    swarm = [row for row in instances if row.get("master_slot_id") == SLOT_ID]
    expected_ids = {f"ENEMY_C01_RIFT_SWARM_{index:02d}" for index in range(1, 7)}
    if len(swarm) != 6 or {row.get("instance_stable_id") for row in swarm} != expected_ids:
        raise RuntimeError("A5 six-instance master binding mismatch")
    for row in swarm:
        if row.get("footprint") != FOOTPRINT or row.get("runtime_allowed") != "false":
            raise RuntimeError("A5 instance footprint/runtime mismatch")

    entities = load_tsv(ROOT / "docs/superpowers/specs/data/canon/entities.tsv")
    entity = next((row for row in entities if row.get("entity_id") == SUBJECT_ID), None)
    if not entity or entity.get("status") != "working_current":
        raise RuntimeError("A5 Current Canon entity mismatch")
    if "E02少量" not in entity.get("implementation_policy", "") or "不锁造型" not in entity.get("notes", ""):
        raise RuntimeError("A5 Current Canon entity boundary missing")
    scenes = load_tsv(ROOT / "docs/superpowers/specs/data/canon/scenes.tsv")
    scene = next((row for row in scenes if row.get("scene_id") == "V355-C01E02"), None)
    if not scene or SUBJECT_ID not in scene.get("required_entities", "") or "各自扑击" not in scene.get("notes", ""):
        raise RuntimeError("A5 Current Canon scene mismatch")
    return swarm


def frame_image(facing: str, size: int) -> Image.Image:
    with Image.open(ROOT / sample_path(facing, size)) as source:
        return source.convert("RGBA")


def build_atlas(size: int) -> Image.Image:
    atlas = Image.new("RGBA", (size * 4, size), (0, 0, 0, 0))
    for index, facing in enumerate(ORDER):
        atlas.paste(frame_image(facing, size), (index * size, 0))
    return atlas


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def checkerboard(size: tuple[int, int], step: int = 18) -> Image.Image:
    image = Image.new("RGB", size, "#e6ebe7")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill="#d4dcd7")
    return image


def alpha_composite_at(base: Image.Image, overlay: Image.Image, position: tuple[int, int]) -> None:
    if base.mode != "RGBA":
        raise ValueError("base image must be RGBA")
    base.alpha_composite(overlay.convert("RGBA"), position)


def bottom_contact_span(image: Image.Image) -> tuple[int, int, int]:
    alpha = image.convert("RGBA").getchannel("A")
    xs = [x for x in range(image.width) if alpha.getpixel((x, image.height - 1)) > 0]
    if not xs:
        raise RuntimeError("A5 frame has no bottom-row contact")
    return min(xs), max(xs), len(xs)


def make_atlas_overview(atlases: dict[int, Image.Image]) -> Image.Image:
    board = Image.new("RGB", (3000, 1200), PAPER)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 3000, 132), fill=INK_DEEP)
    draw.text((55, 29), "A5｜A案四朝向 idle 母版 Atlas", font=font(48, bold=True), fill=IVORY)
    draw.text((2210, 52), "机械直贴｜无缩放｜无补画", font=font(22), fill="#b9c8c5")
    rows = ((96, 180, 4), (128, 670, 3))
    for size, top, scale in rows:
        draw.rounded_rectangle((45, top, 2315, top + 430), radius=8, fill=PANEL, outline="#a9b8b5", width=2)
        draw.text((72, top + 24), f"{size}px｜{size * 4}×{size} RGBA", font=font(29, bold=True), fill=TEAL if size == 96 else CORAL)
        strip = atlases[size].resize((size * 4 * scale, size * scale), Image.Resampling.NEAREST)
        checker = checkerboard(strip.size, max(12, scale * 6)).convert("RGBA")
        checker.alpha_composite(strip)
        left = 160
        y = top + 80
        board.paste(checker.convert("RGB"), (left, y))
        draw.rectangle((left, y, left + strip.width, y + strip.height), outline=INK_DEEP, width=3)
        for index, facing in enumerate(ORDER):
            x = left + index * size * scale
            if index:
                draw.line((x, y, x, y + strip.height), fill=GOLD, width=3)
            draw.text((x + 12, y + strip.height + 12), f"{index}  idle/{facing}", font=font(20, bold=True), fill=INK)

    draw.rounded_rectangle((2355, 180, 2950, 1100), radius=8, fill=PANEL, outline="#a9b8b5", width=2)
    info = (
        ("唯一身份", CANDIDATE_TITLE, TEAL),
        ("顺序", "north → east → south → west", GOLD),
        ("动作", "idle only", CORAL),
        ("pivot", PIVOT, TEAL),
        ("footprint", FOOTPRINT, GOLD),
        ("边界", "Candidate / runtime_allowed=false", CORAL),
    )
    y = 225
    for title, value, color in info:
        draw.text((2390, y), title, font=font(24, bold=True), fill=color)
        y += 42
        draw.text((2390, y), value, font=font(20), fill=INK)
        y += 83
    draw.text((50, 1150), "同一 slot 只能在后续 exact handoff 中选择一份；本图不授权 Godot 或 Runtime。", font=font(20), fill=INK_SOFT)
    return board


def make_baseline_edge_board() -> Image.Image:
    board = Image.new("RGB", (3000, 1800), PAPER)
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 3000, 132), fill=INK_DEEP)
    draw.text((55, 29), "A5｜四朝向基线、接地点、红缝与透明边缘", font=font(46, bold=True), fill=IVORY)
    draw.text((2240, 52), "frame edge / bottom_center", font=font(21), fill="#b9c8c5")
    for row_index, size in enumerate(SIZES):
        row_top = 175 + row_index * 795
        accent = TEAL if size == 96 else CORAL
        draw.text((55, row_top), f"{size}px 原生帧", font=font(30, bold=True), fill=accent)
        scale = 4 if size == 96 else 3
        for index, facing in enumerate(ORDER):
            left = 45 + index * 740
            top = row_top + 55
            draw.rounded_rectangle((left, top, left + 700, top + 680), radius=8, fill=PANEL, outline="#a9b8b5", width=2)
            draw.text((left + 24, top + 18), f"{index}｜idle/{facing}", font=font(25, bold=True), fill=INK)
            frame = frame_image(facing, size)
            scaled = frame.resize((size * scale, size * scale), Image.Resampling.NEAREST)
            check = checkerboard((560, 470), max(12, scale * 6)).convert("RGBA")
            x = (560 - scaled.width) // 2
            y = 450 - scaled.height
            check.alpha_composite(scaled, (x, y))
            board.paste(check.convert("RGB"), (left + 70, top + 72))
            draw.rectangle((left + 70, top + 72, left + 630, top + 542), outline=INK_DEEP, width=2)
            baseline_y = top + 72 + y + scaled.height - 1
            draw.line((left + 70 + x, baseline_y, left + 70 + x + scaled.width, baseline_y), fill=CORAL, width=2)
            bbox = alpha_bbox(frame)
            seam = red_seam_bbox(frame)
            contact = bottom_contact_span(frame)
            draw.text((left + 28, top + 565), f"alpha bbox={bbox}", font=font(18), fill=INK_SOFT)
            draw.text((left + 28, top + 595), f"bottom span={contact[0]}..{contact[1]} / center={size // 2}", font=font(18), fill=INK_SOFT)
            draw.text((left + 28, top + 625), f"closed red seam bbox={seam}", font=font(18), fill=INK_SOFT)
    return board


def project_world(anchor: tuple[int, int]) -> tuple[int, int]:
    x, y = anchor
    return (round(880 + (x - y) * 40), round(170 + (x + y) * 20))


def screen_point(anchor: tuple[int, int], camera: tuple[int, int]) -> tuple[int, int]:
    full_x, full_y = project_world(anchor)
    crop_left = 430 + camera[0]
    crop_top = camera[1] - 127
    return (full_x - crop_left, full_y - crop_top + 54)


def parse_anchor(value: str) -> tuple[int, int]:
    x, y = value.split(",")
    return int(x), int(y)


def atlas_frame(atlas: Image.Image, size: int, facing: str) -> Image.Image:
    index = ORDER.index(facing)
    return atlas.crop((index * size, 0, (index + 1) * size, size))


def visible_instances(instances: list[dict[str, str]], camera: tuple[int, int]) -> list[tuple[dict[str, str], tuple[int, int]]]:
    visible = []
    for instance in instances:
        point = screen_point(parse_anchor(instance["anchor"]), camera)
        if 70 <= point[0] <= 830 and 190 <= point[1] <= 620:
            visible.append((instance, point))
    return visible


def make_map_scale_compare(camera_code: str, instances: list[dict[str, str]], atlases: dict[int, Image.Image]) -> Image.Image:
    camera = CAMERAS[camera_code]
    with Image.open(ROOT / camera["background"]) as source:
        background = source.convert("RGB")
    board = Image.new("RGBA", (2560, 820), (7, 21, 27, 255))
    board.alpha_composite(background.convert("RGBA"), (0, 100))
    board.alpha_composite(background.convert("RGBA"), (1280, 100))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2560, 99), fill=INK_DEEP)
    draw.text((35, 27), f"{camera_code}｜96px actual", font=font(28, bold=True), fill=TEAL)
    draw.text((1315, 27), f"{camera_code}｜128px actual", font=font(28, bold=True), fill=CORAL)
    draw.text((1985, 34), "同机位 / 同锚点 / 外置 overlay", font=font(18), fill="#b9c8c5")
    draw.line((1280, 0, 1280, 820), fill=GOLD, width=4)

    placements = visible_instances(instances, camera["world_center"])
    for half, size in ((0, 96), (1280, 128)):
        for instance, point in placements:
            facing = instance["facing"]
            frame = atlas_frame(atlases[size], size, facing)
            position = (half + point[0] - size // 2, 100 + point[1] - size)
            alpha_composite_at(board, frame, position)
    footer = f"visible approved M2 anchors={len(placements)}｜one master / idle only｜runtime_deferred_not_bound"
    draw.rectangle((0, 792, 2560, 819), fill=(7, 21, 27, 225))
    draw.text((32, 796), footer, font=font(15), fill="#b9c8c5")
    return board.convert("RGB")


def write_tsv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_atlas_spec(atlases: dict[int, Image.Image]) -> None:
    fields = (
        "package_id", "subject_id", "candidate_id", "atlas_candidate_id", "runtime_slot_id", "relative_path",
        "sheet_dimensions", "frame_size", "frame_index", "frame_id", "frame_rect", "source_path", "source_sha256",
        "packing_operation", "binding_kind", "pivot", "footprint", "actions", "facings", "alpha", "edge_gap_px",
        "baseline_y", "bottom_center_contact", "atlas_sha256", "lifecycle", "runtime_allowed", "runtime_handoff",
        "user_decision_required",
    )
    rows = []
    for size in SIZES:
        filename = ATLAS_FILES[size]
        atlas_sha = sha256_file(OUT / filename)
        for index, facing in enumerate(ORDER):
            rows.append({
                "package_id": PACKAGE_ID,
                "subject_id": SUBJECT_ID,
                "candidate_id": CANDIDATE_ID,
                "atlas_candidate_id": f"CAND_C01CDV1_A5_RIFT_SWARM_A_IDLE_ATLAS_{size}_V1",
                "runtime_slot_id": SLOT_ID,
                "relative_path": filename,
                "sheet_dimensions": f"{size * 4}x{size}",
                "frame_size": f"{size}x{size}",
                "frame_index": index,
                "frame_id": f"idle/{facing}",
                "frame_rect": f"{index * size},0,{size},{size}",
                "source_path": sample_path(facing, size),
                "source_sha256": SAMPLE_HASHES[(facing, size)],
                "packing_operation": "mechanical_direct_paste_no_scale_no_repaint",
                "binding_kind": "sprite_sheet",
                "pivot": PIVOT,
                "footprint": FOOTPRINT,
                "actions": "idle",
                "facings": ";".join(ORDER),
                "alpha": "required_rgba",
                "edge_gap_px": 0,
                "baseline_y": size - 1,
                "bottom_center_contact": "true",
                "atlas_sha256": atlas_sha,
                "lifecycle": LIFECYCLE,
                "runtime_allowed": "false",
                "runtime_handoff": "none",
                "user_decision_required": "true",
            })
    write_tsv(OUT / "atlas-spec.tsv", fields, rows)


def write_instance_variation_defer() -> None:
    fields = (
        "instance_stable_id", "master_slot_id", "approved_master_candidate", "approved_light_variation",
        "binding_state", "atlas_output", "lifecycle", "runtime_allowed", "runtime_handoff", "notes",
    )
    variations = (
        ("01", "基准"),
        ("02", "红褐色斑"),
        ("03", "冷绿灰色斑"),
        ("04", "黄褐擦痕"),
        ("05", "末端缺口"),
        ("06", "红缝亮度差"),
    )
    rows = []
    for suffix, variation in variations:
        rows.append({
            "instance_stable_id": f"ENEMY_C01_RIFT_SWARM_{suffix}",
            "master_slot_id": SLOT_ID,
            "approved_master_candidate": CANDIDATE_ID,
            "approved_light_variation": variation,
            "binding_state": "runtime_deferred_not_bound",
            "atlas_output": "none_one_shared_master_only",
            "lifecycle": LIFECYCLE,
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "notes": "approved_direction_record_only_no_instance_variant_interface_in_A5",
        })
    write_tsv(OUT / "instance-variation-defer.tsv", fields, rows)


def write_source_receipt() -> None:
    fields = (
        "source_path", "expected_sha256", "actual_sha256", "authority_role", "validation", "usage_boundary",
        "active_source", "mutation",
    )
    rows = []
    for relative, expected, role in STATIC_SOURCES:
        actual = sha256_file(ROOT / relative)
        usage = "read_only_frozen_input"
        if role.startswith("a3_idle_"):
            usage = "pixel_exact_frame_source"
        elif role.startswith("a4_"):
            usage = "external_review_background_only_not_copied_to_runtime"
        elif role.startswith("current_canon") or role == "canon_authority_manifest":
            usage = "authority_boundary_only_no_canon_write"
        rows.append({
            "source_path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "authority_role": role,
            "validation": "PASS_exact_sha256",
            "usage_boundary": usage,
            "active_source": "true",
            "mutation": "none",
        })
    write_tsv(OUT / "source-validation-receipt.tsv", fields, rows)


def write_user_decision_card() -> None:
    atlas_96 = OUT / ATLAS_FILES[96]
    atlas_128 = OUT / ATLAS_FILES[128]
    text = f"""# C01E02 A5 小型突入体 Atlas 用户裁决卡

> Package: `{PACKAGE_ID}`  
> Candidate: `{CANDIDATE_ID}`  
> Slot: `{SLOT_ID}`  
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 两份互斥候选

- `96px`: `{ATLAS_FILES[96]}`  
  SHA-256: `{sha256_file(atlas_96)}`
- `128px`: `{ATLAS_FILES[128]}`  
  SHA-256: `{sha256_file(atlas_128)}`

## 请逐项确认

1. 四朝向是否保持 A「伏壳钳足型」身份，是否存在朝向混淆？
2. 接地点、闭合红缝和扑击端是否稳定？
3. 选择 `96px` 或 `128px` 中哪一份作为具体 Demo handoff 来源？同一 slot 不能同时绑定两份。
4. 是否接受当前 Demo 六实例先共用一个母版、轻差分继续延期？
5. 是否明确批准所选 atlas 的具体文件名与上述 SHA-256？

建议回复格式：`四向通过；接地点/红缝/扑击端通过；选择96（或128）；六实例共用母版、轻差分延后；批准 <文件名> / <SHA-256> 作为Demo handoff来源`。

本裁决只允许制作人另签 exact handoff；不直接授权 Godot、Runtime promotion 或实例差分接口。
"""
    (OUT / "user-decision-card.md").write_text(text, encoding="utf-8")


def write_completion_report(instances: list[dict[str, str]]) -> None:
    text = f"""# C01E02 A5 小型突入体四朝向 Atlas 完成报告

## Result

- Package: `{PACKAGE_ID}`
- Approved identity source: `A / {CANDIDATE_TITLE}`
- Outputs: `384×96` and `512×128`, RGBA, north/east/south/west single row
- Packing: pixel-exact direct paste; no scaling, repainting, spacing or added frames
- Binding metadata: `sprite_sheet / pivot={PIVOT} / footprint={FOOTPRINT} / actions=idle`
- Review: WEST/CENTRAL/EAST A4 MAP-B external overlay at native 96/128 sizes
- Approved shared-instance records observed: `{len(instances)}`

## Deferred

Six light instance variations are recorded as `runtime_deferred_not_bound`. A5 creates one shared master atlas candidate at each mutually exclusive size and does not create six atlases, move/impact/death animation, or an instance-variation interface.

## Boundary

All files remain `Candidate / runtime_allowed=false / runtime_handoff=none`. No Godot, Runner, R2 manifest, A4 map, Canon, gameplay, C04, LibTV, staging, commit, paid generation or production asset copy is created or modified.

## Stop Gate

Stopped for the five decisions in `user-decision-card.md`. Only one concrete atlas file may proceed to a later producer-signed exact handoff.
"""
    (OUT / "completion-report.md").write_text(text, encoding="utf-8")


def package_files(*, include_manifest: bool = False) -> list[Path]:
    excluded = {"core-delivery-hashes.sha256", "BLOCKED.md"}
    if not include_manifest:
        excluded.add("asset-manifest.tsv")
    return sorted(
        path for path in OUT.rglob("*")
        if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )


def media_info(path: Path) -> tuple[str, str, str]:
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            return "image/png", f"{image.width}x{image.height}", image.mode
    if path.suffix.lower() == ".tsv":
        return "text/tab-separated-values", "", "UTF-8"
    if path.suffix.lower() == ".md":
        return "text/markdown", "", "UTF-8"
    if path.suffix.lower() == ".py":
        return "text/x-python", "", "UTF-8"
    return "application/octet-stream", "", ""


def write_manifest() -> None:
    fields = (
        "package_id", "asset_id", "relative_path", "subject_id", "runtime_slot_id", "candidate_id", "media_type",
        "dimensions", "channels", "asset_role", "packing_operation", "contains_external_map_overlay", "actions",
        "facings", "pivot", "footprint", "lifecycle", "runtime_allowed", "runtime_handoff", "user_decision_required",
        "sha256",
    )
    rows = []
    for path in package_files():
        relative = path.relative_to(OUT).as_posix()
        media_type, dimensions, channels = media_info(path)
        if relative == ATLAS_FILES[96]:
            role = "atlas_candidate_96"
        elif relative == ATLAS_FILES[128]:
            role = "atlas_candidate_128"
        elif relative.startswith("A5_MAP_B_"):
            role = "external_map_scale_review"
        elif media_type == "image/png":
            role = "review_evidence"
        else:
            role = "machine_evidence"
        rows.append({
            "package_id": PACKAGE_ID,
            "asset_id": f"A5_{relative.upper().replace('/', '_').replace('.', '_').replace('-', '_')}",
            "relative_path": relative,
            "subject_id": SUBJECT_ID,
            "runtime_slot_id": SLOT_ID,
            "candidate_id": CANDIDATE_ID,
            "media_type": media_type,
            "dimensions": dimensions,
            "channels": channels,
            "asset_role": role,
            "packing_operation": "mechanical_direct_paste_no_scale_no_repaint" if role.startswith("atlas_candidate") else "review_or_machine_evidence",
            "contains_external_map_overlay": "true" if role == "external_map_scale_review" else "false",
            "actions": "idle" if role.startswith("atlas_candidate") else "",
            "facings": ";".join(ORDER) if role.startswith("atlas_candidate") else "",
            "pivot": PIVOT if role.startswith("atlas_candidate") else "",
            "footprint": FOOTPRINT if role.startswith("atlas_candidate") else "",
            "lifecycle": LIFECYCLE,
            "runtime_allowed": "false",
            "runtime_handoff": "none",
            "user_decision_required": "true",
            "sha256": sha256_file(path),
        })
    write_tsv(OUT / "asset-manifest.tsv", fields, rows)


def write_core_hashes() -> None:
    files = [ROOT / relative for relative, _, _ in STATIC_SOURCES]
    files.extend(package_files(include_manifest=True))
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        raise RuntimeError(f"A5 core hash files missing: {missing}")
    seen: set[Path] = set()
    lines = []
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        lines.append(f"{sha256_file(path)}  {path.relative_to(ROOT).as_posix()}")
    (OUT / "core-delivery-hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_images(instances: list[dict[str, str]]) -> dict[int, Image.Image]:
    atlases = {size: build_atlas(size) for size in SIZES}
    for size, atlas in atlases.items():
        atlas.save(OUT / ATLAS_FILES[size], optimize=True)
    make_atlas_overview(atlases).save(OUT / "A5_atlas_overview_review_3000x1200.png", optimize=True)
    make_baseline_edge_board().save(OUT / "A5_four_facing_baseline_edge_review_3000x1800.png", optimize=True)
    for camera_code in CAMERAS:
        make_map_scale_compare(camera_code, instances, atlases).save(
            OUT / f"A5_MAP_B_{camera_code}_96_128_scale_compare_2560x820.png", optimize=True
        )
    return atlases


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    instances = validate_sources()
    atlases = generate_images(instances)
    write_atlas_spec(atlases)
    write_instance_variation_defer()
    write_source_receipt()
    write_user_decision_card()
    write_completion_report(instances)
    write_manifest()
    write_core_hashes()
    print(f"Generated {PACKAGE_ID}")
    print(f"atlas_96={ATLAS_FILES[96]} sha256={sha256_file(OUT / ATLAS_FILES[96])}")
    print(f"atlas_128={ATLAS_FILES[128]} sha256={sha256_file(OUT / ATLAS_FILES[128])}")
    print("actions=idle facings=north,east,south,west pivot=0.5,1.0 footprint=1,1")
    print("runtime_allowed=false runtime_handoff=none")


if __name__ == "__main__":
    main()
