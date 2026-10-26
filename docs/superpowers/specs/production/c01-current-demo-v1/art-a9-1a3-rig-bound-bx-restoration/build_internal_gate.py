#!/usr/local/bin/python3
"""Assemble the producer-only A9.1-A3 internal visual gate.

Pillow only lays out locally rendered Rig images and approved A4 layers. It
does not draw, repaint or redesign either mecha.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[5]
GATE = HERE / "review/internal-gate"
A4 = PROJECT / "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer"
REGULAR = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")
BOLD = Path("/System/Library/Fonts/STHeiti Medium.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(BOLD if bold else REGULAR), size)


def rgba(color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def trim(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("transparent source")
    return image.crop(bbox)


def contain(image: Image.Image, width: int, height: int, nearest: bool = False) -> Image.Image:
    method = Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS
    return ImageOps.contain(image.convert("RGBA"), (width, height), method=method)


def paste_bottom_center(canvas: Image.Image, image: Image.Image, x: int, baseline: int) -> None:
    canvas.alpha_composite(image, (round(x - image.width / 2), baseline - image.height))


def project(tile_x: float, tile_y: float) -> tuple[int, int]:
    return round(880 + (tile_x - tile_y) * 40), round(170 + (tile_x + tile_y) * 20)


def build_identity_board() -> Path:
    board = Image.new("RGBA", (2400, 1350), rgba("#e8ecea"))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2400, 104), fill=rgba("#081820"))
    draw.text((44, 22), "A9.1-A3 INTERNAL GATE / RIG-BOUND COLOR", font=font(38, True), fill="#f3f1e8")
    draw.text((2352, 36), "Candidate / producer preflight only", font=font(20), fill="#ef5a50", anchor="ra")
    panels = (
        (GATE / "GATE_GUARDIAN_Z_FRONT_RGBA_1024.png", (32, 132, 800, 1260), "馆守Z / FRONT", "V10X identity + chamfered KINETIC_CEL"),
        (GATE / "GATE_GUARDIAN_Z_STRICT_LEFT_RGBA_1024.png", (816, 132, 1584, 1260), "馆守Z / STRICT LEFT", "same named-component Rig / no painted side cheat"),
        (GATE / "GATE_BREAKER_BX_PLANNING_RGBA_1024.png", (1600, 132, 2368, 1260), "BREAKER / PLANNING", "B semi-upright forelimb bearer + X alien armor"),
    )
    for source, box, title, note in panels:
        draw.rounded_rectangle(box, radius=8, fill=rgba("#f6f7f3"), outline=rgba("#28434a"), width=3)
        art = contain(trim(Image.open(source)), box[2] - box[0] - 50, box[3] - box[1] - 160)
        x = box[0] + (box[2] - box[0] - art.width) // 2
        y = box[1] + 40 + (box[3] - box[1] - 160 - art.height) // 2
        board.alpha_composite(art, (x, y))
        draw.rectangle((box[0], box[3] - 112, box[2], box[3]), fill=rgba("#102630"))
        draw.text((box[0] + 22, box[3] - 94), title, font=font(24, True), fill="#edf2ef")
        draw.text((box[0] + 22, box[3] - 56), note, font=font(16), fill="#a8bab9")
    draw.text((44, 1302), "Raw Rig and color render are the same geometry; this board is not a user approval or Runtime handoff.", font=font(18), fill="#5c7075")
    path = GATE / "A91A3_INTERNAL_IDENTITY_GATE_2400x1350.png"
    board.convert("RGB").save(path)
    return path


def build_map_gate() -> Path:
    layers = {
        name: Image.open(A4 / filename).convert("RGBA")
        for name, filename in {
            "base": "A4_MAP_B_BASE_2400x1350.png",
            "buildings": "A4_MAP_B_BUILDINGS_2400x1350.png",
            "state": "A4_MAP_B_STATE_LAYERS_2400x1350.png",
            "roofs": "A4_MAP_B_ROOFS_2400x1350.png",
            "foreground": "A4_MAP_B_FOREGROUND_2400x1350.png",
        }.items()
    }
    world = layers["base"].copy()
    world.alpha_composite(layers["buildings"])
    world.alpha_composite(layers["state"])
    gz = contain(trim(Image.open(GATE / "GATE_GUARDIAN_Z_FRONT_RGBA_1024.png")), 300, 210, nearest=True)
    bx = contain(trim(Image.open(GATE / "GATE_BREAKER_BX_PLANNING_RGBA_1024.png")), 520, 350, nearest=True)
    gz_anchor = project(11.5, 11.5)
    bx_anchor = project(19, 9)
    paste_bottom_center(world, gz, gz_anchor[0], gz_anchor[1] + 6)
    paste_bottom_center(world, bx, bx_anchor[0], bx_anchor[1] + 12)
    world.alpha_composite(layers["roofs"])
    world.alpha_composite(layers["foreground"])

    crop = world.crop((500, 250, 1780, 970)).resize((1280, 720), Image.Resampling.LANCZOS)
    crop_path = GATE / "A91A3_A4_ACTUAL_SCALE_CENTRAL_1280x720.png"
    crop.convert("RGB").save(crop_path)

    board = Image.new("RGBA", (2400, 1350), rgba("#07151a"))
    draw = ImageDraw.Draw(board)
    draw.text((44, 26), "A9.1-A3 / A4 ACTUAL SCALE INTERNAL GATE", font=font(42, True), fill="#edf2ef")
    draw.text((2350, 42), "18m 2x2 / near-30m 3x3 / same A4 camera", font=font(20), fill="#dfb13e", anchor="ra")
    full = contain(world, 1530, 1120)
    board.alpha_composite(full, (32, 116))
    zoom = contain(crop, 790, 445)
    board.alpha_composite(zoom, (1580, 116))
    draw.rectangle((1580, 116, 2370, 561), outline=rgba("#58c5ca"), width=3)
    draw.rounded_rectangle((1580, 600, 2370, 1228), radius=8, fill=rgba("#102630"), outline=rgba("#42616a"), width=2)
    notes = (
        ("馆守Z", "2x2 footprint / 210px visual height", "#dfb13e"),
        ("BREAKER", "3x3 footprint / 350px visual height", "#ef5a50"),
        ("Pivot", "bottom_center on approved A4 projection", "#58c5ca"),
        ("Occlusion", "approved roofs + foreground unchanged", "#edf2ef"),
        ("Gate", "identity and first-read at actual scale only", "#a8bab9"),
    )
    for index, (title, note, color) in enumerate(notes):
        y = 646 + index * 102
        draw.text((1624, y), title, font=font(24, True), fill=color)
        draw.text((1624, y + 38), note, font=font(19), fill="#d4dfdc")
    draw.text((44, 1302), "No map redraw; no Runtime binding; no final Atlas.", font=font(18), fill="#a8bab9")
    path = GATE / "A91A3_A4_ACTUAL_SCALE_GATE_2400x1350.png"
    board.convert("RGB").save(path)
    return path


def main() -> None:
    GATE.mkdir(parents=True, exist_ok=True)
    identity = build_identity_board()
    map_gate = build_map_gate()
    print(identity)
    print(map_gate)


if __name__ == "__main__":
    main()
