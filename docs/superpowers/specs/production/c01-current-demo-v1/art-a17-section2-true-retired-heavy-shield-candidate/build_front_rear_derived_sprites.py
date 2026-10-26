#!/usr/bin/env python3
"""Deterministically derive A17 front/rear shield sprites from the accepted raw.

This is a pixel registration/export utility, not an image-generation or repaint
step.  It only keeps the largest alpha-connected component inside the locked
front/rear source windows, preserves those RGBA pixels exactly in the masters,
and produces normalized 256 px inspection candidates by premultiplied-alpha
resampling.
"""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = (
    ROOT
    / "user-confirmation-call01"
    / "generation-raw"
    / "TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png"
)
EXPECTED_SOURCE_SHA256 = (
    "169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305"
)

OUT = ROOT / "derived-front-rear-sprites-v1"
MASTER_DIR = OUT / "masters"
MAP_DIR = OUT / "map-candidates"
QA_DIR = OUT / "qa"

MASTER_CANVAS = (768, 1152)
MAP_CANVAS = (256, 256)
MAP_LONG_AXIS_PX = 208
MAP_GROUND_TIP_Y = 224

SOURCE_WINDOWS = {
    "front_exterior": (0, 0, 720, 1024),
    "rear_interior": (720, 0, 1280, 1024),
}

# Source-space sockets are deterministic registration annotations made against
# the accepted raw. They do not add, move, or repaint any pixel.
SOURCE_SOCKETS = {
    "front_edge_red_beam_contact_px": (574.0, 393.0),
    "rear_left_grip_center_px": (860.0, 448.0),
    "rear_right_grip_center_px": (1023.0, 448.0),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def largest_alpha_component(
    rgba: np.ndarray, window: tuple[int, int, int, int]
) -> tuple[np.ndarray, dict[str, object]]:
    x0, y0, x1, y1 = window
    alpha = rgba[y0:y1, x0:x1, 3]
    live = alpha > 0
    height, width = live.shape
    seen = np.zeros_like(live, dtype=np.bool_)
    best_coords: list[tuple[int, int]] = []
    component_sizes: list[int] = []

    for seed_y, seed_x in zip(*np.where(live & ~seen)):
        if seen[seed_y, seed_x]:
            continue
        queue: deque[tuple[int, int]] = deque([(int(seed_y), int(seed_x))])
        seen[seed_y, seed_x] = True
        coords: list[tuple[int, int]] = []
        while queue:
            py, px = queue.pop()
            coords.append((py, px))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = py + dy, px + dx
                    if (
                        0 <= ny < height
                        and 0 <= nx < width
                        and live[ny, nx]
                        and not seen[ny, nx]
                    ):
                        seen[ny, nx] = True
                        queue.append((ny, nx))
        component_sizes.append(len(coords))
        if len(coords) > len(best_coords):
            best_coords = coords

    if not best_coords:
        raise RuntimeError(f"no alpha subject in source window {window}")

    selected = np.zeros_like(live, dtype=np.bool_)
    ys = np.fromiter((coord[0] for coord in best_coords), dtype=np.int32)
    xs = np.fromiter((coord[1] for coord in best_coords), dtype=np.int32)
    selected[ys, xs] = True

    source_x0 = x0 + int(xs.min())
    source_y0 = y0 + int(ys.min())
    source_x1 = x0 + int(xs.max()) + 1
    source_y1 = y0 + int(ys.max()) + 1
    isolated = np.zeros_like(rgba)
    window_pixels = rgba[y0:y1, x0:x1]
    isolated_window = isolated[y0:y1, x0:x1]
    isolated_window[selected] = window_pixels[selected]

    return isolated, {
        "source_window_px": list(window),
        "source_alpha_component_count": len(component_sizes),
        "selected_component_pixels": len(best_coords),
        "discarded_nonselected_alpha_pixels": int(live.sum()) - len(best_coords),
        "source_selected_bbox_xyxy": [source_x0, source_y0, source_x1, source_y1],
        "selected_component_is_largest": True,
        "connectivity": 8,
        "alpha_threshold": 0,
    }


def exact_master(
    isolated: np.ndarray, bbox: list[int]
) -> tuple[Image.Image, dict[str, object]]:
    x0, y0, x1, y1 = bbox
    crop = Image.fromarray(isolated[y0:y1, x0:x1], mode="RGBA")
    canvas = Image.new("RGBA", MASTER_CANVAS, (0, 0, 0, 0))
    offset = (
        (MASTER_CANVAS[0] - crop.width) // 2,
        (MASTER_CANVAS[1] - crop.height) // 2,
    )
    if offset[0] < 0 or offset[1] < 0:
        raise RuntimeError(f"master canvas too small for {crop.size}")
    canvas.alpha_composite(crop, offset)
    alpha = np.asarray(canvas)[:, :, 3]
    ys, xs = np.where(alpha > 0)
    out_bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    return canvas, {
        "canvas_size": list(MASTER_CANVAS),
        "copy_offset_px": list(offset),
        "alpha_bbox_xyxy": out_bbox,
        "native_source_pixels_preserved": True,
        "resampled": False,
    }


def resize_rgba_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    array = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = array[:, :, 3:4] / 255.0
    premultiplied = np.concatenate((array[:, :, :3] * alpha, array[:, :, 3:4]), axis=2)
    premultiplied_u8 = np.clip(np.rint(premultiplied), 0, 255).astype(np.uint8)
    resized = np.asarray(
        Image.fromarray(premultiplied_u8, mode="RGBA").resize(size, Image.Resampling.LANCZOS),
        dtype=np.float32,
    )
    out_alpha = resized[:, :, 3:4]
    safe_alpha = np.where(out_alpha > 0, out_alpha / 255.0, 1.0)
    rgb = np.where(out_alpha > 0, resized[:, :, :3] / safe_alpha, 0.0)
    out = np.concatenate((rgb, out_alpha), axis=2)
    return Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8), mode="RGBA")


def normalized_map_candidate(
    isolated: np.ndarray, bbox: list[int]
) -> tuple[Image.Image, dict[str, object]]:
    x0, y0, x1, y1 = bbox
    crop = Image.fromarray(isolated[y0:y1, x0:x1], mode="RGBA")
    scale = MAP_LONG_AXIS_PX / float(crop.height)
    resized_size = (max(1, round(crop.width * scale)), MAP_LONG_AXIS_PX)
    resized = resize_rgba_premultiplied(crop, resized_size)
    canvas = Image.new("RGBA", MAP_CANVAS, (0, 0, 0, 0))
    offset = (
        (MAP_CANVAS[0] - resized.width) // 2,
        MAP_GROUND_TIP_Y - resized.height,
    )
    canvas.alpha_composite(resized, offset)
    alpha = np.asarray(canvas)[:, :, 3]
    ys, xs = np.where(alpha > 0)
    return canvas, {
        "canvas_size": list(MAP_CANVAS),
        "source_selected_bbox_xyxy": bbox,
        "normalized_subject_size_px": list(resized.size),
        "copy_offset_px": list(offset),
        "alpha_bbox_xyxy": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1],
        "ground_tip_pivot_px": [128, MAP_GROUND_TIP_Y],
        "nominal_sprite_scale": [1.0, 1.0],
        "provisional_held_scale_relative_to_18m_gz": [0.40, 0.40],
        "held_scale_gate": "DEFERRED_PENDING_TRUE_USER_ACCEPTED_GZ_MASTER_ACTUAL_FRAME",
        "resample": "premultiplied_alpha_lanczos",
    }


def source_to_map(
    source_xy: tuple[float, float], map_meta: dict[str, object]
) -> list[float]:
    bbox = map_meta["source_selected_bbox_xyxy"]
    offset = map_meta["copy_offset_px"]
    size = map_meta["normalized_subject_size_px"]
    sx = size[0] / float(bbox[2] - bbox[0])
    sy = size[1] / float(bbox[3] - bbox[1])
    return [
        round(offset[0] + (source_xy[0] - bbox[0]) * sx, 3),
        round(offset[1] + (source_xy[1] - bbox[1]) * sy, 3),
    ]


def alpha_component_sizes(image: Image.Image) -> list[int]:
    live = np.asarray(image.convert("RGBA"))[:, :, 3] > 0
    seen = np.zeros_like(live, dtype=np.bool_)
    height, width = live.shape
    sizes: list[int] = []
    for seed_y, seed_x in zip(*np.where(live & ~seen)):
        if seen[seed_y, seed_x]:
            continue
        queue: deque[tuple[int, int]] = deque([(int(seed_y), int(seed_x))])
        seen[seed_y, seed_x] = True
        size = 0
        while queue:
            py, px = queue.pop()
            size += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = py + dy, px + dx
                    if (
                        0 <= ny < height
                        and 0 <= nx < width
                        and live[ny, nx]
                        and not seen[ny, nx]
                    ):
                        seen[ny, nx] = True
                        queue.append((ny, nx))
        sizes.append(size)
    return sorted(sizes, reverse=True)


def pixel_gate(
    source_rgba: np.ndarray,
    bbox: list[int],
    master: Image.Image,
    master_meta: dict[str, object],
    map_sprite: Image.Image,
) -> dict[str, object]:
    x0, y0, x1, y1 = bbox
    offset_x, offset_y = master_meta["copy_offset_px"]
    source_crop = source_rgba[y0:y1, x0:x1]
    master_rgba = np.asarray(master.convert("RGBA"))
    master_region = master_rgba[
        offset_y : offset_y + source_crop.shape[0],
        offset_x : offset_x + source_crop.shape[1],
    ]
    active = master_region[:, :, 3] > 0
    exact_active_pixels = bool(np.array_equal(master_region[active], source_crop[active]))
    master_components = alpha_component_sizes(master)
    map_components = alpha_component_sizes(map_sprite)
    master_edges = [
        int((master_rgba[0, :, 3] > 0).sum()),
        int((master_rgba[-1, :, 3] > 0).sum()),
        int((master_rgba[:, 0, 3] > 0).sum()),
        int((master_rgba[:, -1, 3] > 0).sum()),
    ]
    map_rgba = np.asarray(map_sprite.convert("RGBA"))
    map_edges = [
        int((map_rgba[0, :, 3] > 0).sum()),
        int((map_rgba[-1, :, 3] > 0).sum()),
        int((map_rgba[:, 0, 3] > 0).sum()),
        int((map_rgba[:, -1, 3] > 0).sum()),
    ]
    passed = (
        exact_active_pixels
        and len(master_components) == 1
        and len(map_components) == 1
        and master_edges == [0, 0, 0, 0]
        and map_edges == [0, 0, 0, 0]
    )
    if not passed:
        raise RuntimeError("derived sprite pixel gate failed")
    return {
        "status": "PASS_DETERMINISTIC_SPRITE_EXTRACTION_ONLY",
        "master_active_rgba_exactly_matches_source": exact_active_pixels,
        "master_alpha_components": len(master_components),
        "master_alpha_component_pixels": master_components,
        "map_alpha_components": len(map_components),
        "map_alpha_component_pixels": map_components,
        "master_edge_alpha_counts_top_bottom_left_right": master_edges,
        "map_edge_alpha_counts_top_bottom_left_right": map_edges,
        "no_other_view_pixels": True,
        "no_baked_background": True,
        "no_subject_crop": True,
    }


def composite_tile(subject: Image.Image, background: tuple[int, int, int], size: tuple[int, int]) -> Image.Image:
    tile = Image.new("RGBA", size, (*background, 255))
    tile.alpha_composite(subject, ((size[0] - subject.width) // 2, (size[1] - subject.height) // 2))
    return tile.convert("RGB")


def draw_100_board(label: str, subject: Image.Image, output: Path) -> None:
    margin = 32
    header = 82
    tile_size = (subject.width, subject.height)
    board = Image.new("RGB", (margin * 3 + tile_size[0] * 2, header + margin * 2 + tile_size[1]), "#15191D")
    d = ImageDraw.Draw(board)
    d.text((margin, 20), f"A17 {label} · alpha QA · 100% native master pixels", font=font(30, True), fill="#F3F0E8")
    dark = composite_tile(subject, (18, 22, 27), tile_size)
    light = composite_tile(subject, (234, 231, 220), tile_size)
    y = header + margin
    board.paste(dark, (margin, y))
    board.paste(light, (margin * 2 + tile_size[0], y))
    d.text((margin + 12, y + 10), "DARK", font=font(22, True), fill="#FFFFFF")
    d.text((margin * 2 + tile_size[0] + 12, y + 10), "LIGHT", font=font(22, True), fill="#1A2228")
    board.save(output)


def draw_50_board(front: Image.Image, rear: Image.Image, output: Path) -> None:
    half_front = front.resize((front.width // 2, front.height // 2), Image.Resampling.LANCZOS)
    half_rear = rear.resize((rear.width // 2, rear.height // 2), Image.Resampling.LANCZOS)
    board = Image.new("RGB", (1800, 1380), "#11161B")
    d = ImageDraw.Draw(board)
    d.text((48, 30), "A17 accepted shield · deterministic front/rear extraction QA · 50%", font=font(38, True), fill="#F4F0E6")
    d.text((48, 82), "No ImageGen · no repaint · no hands · no Godot/Runtime/Canon binding", font=font(25), fill="#AFC8D4")
    tiles = [
        ("FRONT EXTERIOR · enemy-facing", half_front, (18, 22, 27), 48, 140),
        ("REAR INTERIOR · holder-facing grips", half_rear, (18, 22, 27), 916, 140),
        ("FRONT EXTERIOR · light alpha check", half_front, (234, 231, 220), 48, 750),
        ("REAR INTERIOR · light alpha check", half_rear, (234, 231, 220), 916, 750),
    ]
    for title, subject, bg, x, y in tiles:
        tile = Image.new("RGBA", (820, 580), (*bg, 255))
        tile.alpha_composite(subject, ((820 - subject.width) // 2, 0))
        board.paste(tile.convert("RGB"), (x, y))
        color = "#FFFFFF" if sum(bg) < 150 else "#15202A"
        d.text((x + 18, y + 542), title, font=font(21, True), fill=color)
    d.text((48, 1340), "Hard gate: exterior faces enemy; rear/grips face GZ; hands may contact rear grips only; one visual owner at a time.", font=font(22, True), fill="#F4C95D")
    board.save(output)


def main() -> None:
    if sha256(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("A17 accepted raw SHA-256 drifted")

    source_image = Image.open(SOURCE).convert("RGBA")
    if source_image.size != (1536, 1024):
        raise RuntimeError(f"unexpected source size: {source_image.size}")
    source_rgba = np.asarray(source_image)

    for directory in (MASTER_DIR, MAP_DIR, QA_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    records: dict[str, dict[str, object]] = {}
    masters: dict[str, Image.Image] = {}
    maps: dict[str, Image.Image] = {}

    for role, window in SOURCE_WINDOWS.items():
        isolated, extraction = largest_alpha_component(source_rgba, window)
        bbox = extraction["source_selected_bbox_xyxy"]
        master, master_meta = exact_master(isolated, bbox)
        map_sprite, map_meta = normalized_map_candidate(isolated, bbox)

        master_name = f"A17_SHIELD_{role.upper()}_RGBA_MASTER_768x1152.png"
        map_name = f"A17_SHIELD_{role.upper()}_MAP_CANDIDATE_256x256.png"
        master_path = MASTER_DIR / master_name
        map_path = MAP_DIR / map_name
        master.save(master_path)
        map_sprite.save(map_path)

        qa_gate = pixel_gate(source_rgba, bbox, master, master_meta, map_sprite)

        records[role] = {
            "extraction": extraction,
            "master": {
                **master_meta,
                "path": str(master_path.relative_to(ROOT)),
                "sha256": sha256(master_path),
                "mode": "RGBA",
            },
            "map_candidate": {
                **map_meta,
                "path": str(map_path.relative_to(ROOT)),
                "sha256": sha256(map_path),
                "mode": "RGBA",
            },
            "pixel_gate": qa_gate,
        }
        masters[role] = master
        maps[role] = map_sprite

    rear_map = records["rear_interior"]["map_candidate"]
    front_map = records["front_exterior"]["map_candidate"]
    left_grip = source_to_map(SOURCE_SOCKETS["rear_left_grip_center_px"], rear_map)
    right_grip = source_to_map(SOURCE_SOCKETS["rear_right_grip_center_px"], rear_map)
    held_pivot = [round((left_grip[0] + right_grip[0]) / 2.0, 3), round((left_grip[1] + right_grip[1]) / 2.0, 3)]
    front_edge = source_to_map(SOURCE_SOCKETS["front_edge_red_beam_contact_px"], front_map)

    records["front_exterior"]["orientation"] = {
        "surface_role": "enemy_facing_exterior",
        "holder_and_shield_front_direction": "same",
        "holder_position": "behind_shield_rear_interior",
        "grips_visible": False,
        "hands_drawn": False,
        "hands_must_not_be_visible_on_front": True,
        "front_edge_socket_px": front_edge,
        "front_edge_socket_source_px": list(SOURCE_SOCKETS["front_edge_red_beam_contact_px"]),
        "held_attachment_pivot_px_transferred_from_rear": held_pivot,
    }
    records["rear_interior"]["orientation"] = {
        "surface_role": "holder_facing_interior",
        "holder_and_shield_front_direction": "same",
        "holder_position": "immediately_behind_this_surface",
        "grips_visible": True,
        "hands_drawn": False,
        "hands_allowed_only_at_rear_grip_sockets": True,
        "rear_grip_socket_px": [left_grip, right_grip],
        "rear_grip_socket_source_px": [
            list(SOURCE_SOCKETS["rear_left_grip_center_px"]),
            list(SOURCE_SOCKETS["rear_right_grip_center_px"]),
        ],
        "held_attachment_pivot_px": held_pivot,
    }

    front_qa = QA_DIR / "A17_SHIELD_FRONT_EXTERIOR_ALPHA_DARK_LIGHT_QA_100PCT.png"
    rear_qa = QA_DIR / "A17_SHIELD_REAR_INTERIOR_ALPHA_DARK_LIGHT_QA_100PCT.png"
    combined_qa = QA_DIR / "A17_SHIELD_FRONT_REAR_DARK_LIGHT_QA_50PCT.png"
    draw_100_board("FRONT EXTERIOR", masters["front_exterior"], front_qa)
    draw_100_board("REAR INTERIOR", masters["rear_interior"], rear_qa)
    draw_50_board(masters["front_exterior"], masters["rear_interior"], combined_qa)

    metadata = {
        "schema_id": "A17_USER_ACCEPTED_DESIGN_BASE_DERIVED_FRONT_REAR_SPRITES_V1",
        "status": "USER_ACCEPTED_DESIGN_BASE_DERIVED_MAP_SPRITE_REVIEW_ONLY",
        "candidate_only": True,
        "design_base_user_accepted": True,
        "derived_sprite_actual_frame_user_acceptance": False,
        "runtime": False,
        "canon": False,
        "godot_bound": False,
        "imagegen_called": False,
        "creative_redraw": False,
        "source": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": EXPECTED_SOURCE_SHA256,
            "size": list(source_image.size),
            "mode": "RGBA",
        },
        "derivation": {
            "method": "largest_8_connected_alpha_component_per_locked_source_window_then_exact_master_copy",
            "map_resample": "premultiplied_alpha_lanczos",
            "excluded_sources": ["A2", "A13", "A14", "A18", "A19", "A22"],
            "pixel_generation": False,
            "pixel_repaint": False,
        },
        "visual_owner_contract": {
            "single_visual_owner": True,
            "allowed_owners": ["wall_mount_state", "future_true_gz_holder_composite_state"],
            "mutual_exclusion_required": True,
            "independent_composed_prop_binding_allowed": False,
        },
        "roles": records,
        "qa": {
            "front_100pct": {"path": str(front_qa.relative_to(ROOT)), "sha256": sha256(front_qa)},
            "rear_100pct": {"path": str(rear_qa.relative_to(ROOT)), "sha256": sha256(rear_qa)},
            "combined_50pct": {"path": str(combined_qa.relative_to(ROOT)), "sha256": sha256(combined_qa)},
        },
        "hard_gates": {
            "front_exterior_and_gz_face_same_enemy_direction": True,
            "rear_interior_and_grips_face_holder": True,
            "hands_visible_on_front_forbidden": True,
            "hands_are_not_part_of_these_shield_only_sprites": True,
            "true_gz_source_required_before_held_actual_frame": True,
            "camera_v2_exact_held_pose_proven": False,
        },
    }
    metadata_path = OUT / "A17_SHIELD_FRONT_REAR_DERIVATION_METADATA.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"metadata": str(metadata_path), "metadata_sha256": sha256(metadata_path), "roles": records}, indent=2))


if __name__ == "__main__":
    main()
