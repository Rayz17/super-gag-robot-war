#!/usr/bin/env python3
"""Task 69 mandated-stop evidence for the single Guardian Z edit attempt.

The one allowed ImageGen result is copied byte-for-byte, then mechanically
masked with the approved C alpha.  No visible mecha structure is drawn.
"""

from __future__ import annotations

import csv
import hashlib
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


OUT = Path(__file__).resolve().parent
ROOT = next(parent for parent in OUT.parents if (parent / ".git").exists())
RAW = Path("/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-2466d480-c7bb-48ea-bb8e-024a5f9f3901.png")
FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

TASK_REL = "docs/superpowers/specs/production/c01-current-demo-v1/69-c01e02-a9-1a3-scale-freeze-and-two-frame-faithful-cleanup-pilot.md"
BOARD_REL = "docs/superpowers/specs/production/c01-current-demo-v1/38-c01e02-m3-r0-5-production-board.tsv"
GZ_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-existing-source-reuse-r0/GUARDIAN_Z_C128_APPROVED_EXACT.png"
GZ_CML008_REL = ".superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png"
GZ_V10X_REL = "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png"
STYLE_REL = "docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png"
BR_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-existing-source-reuse-r0/BREAKER_B128_APPROVED_EXACT.png"
BR_B_SHEET_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png"
BR_X_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png"
MAP_REL = "docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_viewport_central_1280x720.png"

EXPECTED = {
    TASK_REL: "3040e981d9ab68a74751b0ff1d9210b4c8e70ef3f5483cfe496a45da7c72aec4",
    BOARD_REL: "39aef6db2bdc171ae9fd111a82aab9a6a0a15fce477675c49dda389c7d4c58aa",
    GZ_REL: "d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e",
    GZ_CML008_REL: "a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521",
    GZ_V10X_REL: "e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade",
    STYLE_REL: "8a546082e8fd2f1b0f9c6e8a8b1e602a647f478112887e93a8f44148e4867842",
    BR_REL: "e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4",
    BR_B_SHEET_REL: "7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868",
    BR_X_REL: "cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85",
    MAP_REL: "b8ccc9b6eefb802b929a6d674e668611c6d9a88e123e24a2991710ae7e5f4ea9",
}
RAW_SHA = "54f4716270bbec9db27ac3fc6ecf6c283f84da104f939a42bb1d448b1bb74d14"

RAW_NAME = "GUARDIAN_Z_IMAGEGEN_EDIT_ATTEMPT_RAW_RGB_1254.png"
WORK_NAME = "GUARDIAN_Z_IMAGEGEN_EDIT_ATTEMPT_MASKED_WORK_RGBA_1254.png"
FINAL_NAME = "GUARDIAN_Z_MASK_BOUND_FAILURE_256.png"
OVERLAY_NAME = "SILHOUETTE_MASK_OVERLAY_1920x1080.png"

ACTUAL_PROMPT = """Use case: identity-preserve
Asset type: transparent game Sprite cleanup work source
Input images:
- Image 1: EDIT TARGET and immutable approved composition. Its south-idle pose, approximately 4.2-head body proportion, outer silhouette, limb lengths and widths, shoulder/chest mass, foot line, bottom-center registration, and normalized placement in the square canvas must remain exactly the same.
- Image 2: CML008 Hard identity reference only. Borrow only the locked Guardian Z identity details; do not borrow its framing, proportion, pose, background, or extra surface noise.
- Image 3: V10X C01E02 local-structure reference only. Borrow only the intact two-arm E02 naked-body details; do not borrow its taller body proportion or framing.
- Image 4: CML128 KINETIC_CEL style reference only. Borrow only deep ink-navy animation line pressure, large clean color blocks, and hard cel shading. Absolutely do not borrow its character, wings, background, pose, or proportions.

Primary request: Faithfully clean up Image 1 inside its existing silhouette into a polished KINETIC_CEL south-idle Guardian Z Sprite. This is bitmap cleanup, not redesign. Preserve Image 1's exact body mask, pose, proportions, camera, center of gravity, and square-canvas placement.

Identity details to clarify only inside the unchanged silhouette: layered gold crown with a clear central red crown and blue forehead helmet; dignified silver grille face; red X chest armor; circular gold chest core; broad square shoulder rings; equal-weight cylindrical original forearms; red, deep navy blue, silver, gold and small ivory accents. Keep both arms intact for E02. No wings and no backpack.

Style/medium: clean hand-drawn animation Sprite finish; deep ink-navy pressure lines; 4–7 large color masses; at most two hard shadow values per color family; controlled material facets; very limited wear; crisp small-scale readability.

Composition/framing: one centered full-body subject on a genuinely transparent 1:1 square canvas, identical normalized silhouette and placement to Image 1, feet visible, no floor and no cast shadow outside the body.

Constraints: change internal finish only; keep every exterior contour and all body proportions unchanged; no new armor, no removed armor, no translated or resized body part, no extra object, no text, no symbols, no watermark; transparent background; all visible pixels must remain inside Image 1's silhouette mask.

Avoid: redesign; high-proportion display-mecha body; baby-toy proportions; realistic 3D render; soft gradients; airbrush shading; tiny AI detail noise; wings; backpack; missing arm; rocket-fist launch; external glow; background; ground shadow."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def validate() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for relative, expected in EXPECTED.items():
        path = ROOT / relative
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"Frozen source mismatch: {relative}")
        paths[relative] = path
    if not RAW.is_file() or sha256(RAW) != RAW_SHA:
        raise RuntimeError("Current single ImageGen attempt is missing or drifted")
    return paths


def detected_subject_mask(raw: Image.Image) -> Image.Image:
    rgb = raw.convert("RGB")
    result = Image.new("L", rgb.size, 0)
    src = rgb.load()
    dst = result.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = src[x, y]
            dst[x, y] = 255 if (min(r, g, b) < 205 or max(r, g, b) - min(r, g, b) > 28) else 0
    return result


def mask_stats(mask: Image.Image, detected: Image.Image) -> tuple[int, int, float]:
    mask_binary = mask.point(lambda value: 255 if value else 0)
    detected_binary = detected.point(lambda value: 255 if value else 0)
    mask_pixels = sum(1 for value in mask_binary.getdata() if value)
    inside_detected = sum(1 for a, b in zip(mask_binary.getdata(), detected_binary.getdata()) if a and b)
    return mask_pixels, inside_detected, inside_detected / mask_pixels


def checker(size: tuple[int, int], cell: int = 24) -> Image.Image:
    image = Image.new("RGBA", size, (238, 240, 241, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, min(x + cell - 1, size[0] - 1), min(y + cell - 1, size[1] - 1)), fill=(213, 218, 221, 255))
    return image


def contain(image: Image.Image, box: tuple[int, int]) -> Image.Image:
    return ImageOps.contain(image, box, Image.Resampling.LANCZOS)


def build_images(paths: dict[str, Path]) -> dict[str, object]:
    shutil.copyfile(RAW, OUT / RAW_NAME)
    raw = Image.open(RAW).convert("RGB")
    exact = Image.open(paths[GZ_REL]).convert("RGBA")
    exact_alpha = exact.getchannel("A")

    work_mask = exact_alpha.resize(raw.size, Image.Resampling.NEAREST)
    work = raw.convert("RGBA")
    work.putalpha(work_mask)
    work.save(OUT / WORK_NAME, optimize=False)

    final_rgb = raw.resize((256, 256), Image.Resampling.LANCZOS)
    final_mask = exact_alpha.resize((256, 256), Image.Resampling.NEAREST)
    final = final_rgb.convert("RGBA")
    final.putalpha(final_mask)
    final.save(OUT / FINAL_NAME, optimize=False)

    detected = detected_subject_mask(raw)
    mask_pixels, detected_inside, coverage = mask_stats(work_mask, detected)
    outside_work = sum(1 for a, m in zip(work.getchannel("A").getdata(), work_mask.getdata()) if a and not m)
    outside_final = sum(1 for a, m in zip(final.getchannel("A").getdata(), final_mask.getdata()) if a and not m)
    return {
        "raw": raw,
        "exact": exact,
        "work": work,
        "final": final,
        "work_mask": work_mask,
        "final_mask": final_mask,
        "detected": detected,
        "raw_subject_bbox": detected.getbbox(),
        "work_mask_bbox": work_mask.getbbox(),
        "mask_pixels": mask_pixels,
        "detected_inside": detected_inside,
        "coverage": coverage,
        "outside_work": outside_work,
        "outside_final": outside_final,
    }


def make_overlay(data: dict[str, object]) -> None:
    board = Image.new("RGBA", (1920, 1080), (9, 16, 24, 255))
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle((0, 0, 1920, 105), fill=(18, 30, 42, 255))
    draw.text((35, 18), "TASK 69 · SINGLE-CALL MASK-BOUND FAILURE EVIDENCE", font=font(31, True), fill=(247, 245, 232, 255))
    draw.text((35, 62), "Guardian Z call 1/1 used · no reroll · BREAKER call 0/1 · mandated stop", font=font(19), fill=(255, 143, 132, 255))

    panels = ((35, 130, 610, 780), (672, 130, 1247, 780), (1309, 130, 1884, 780))
    titles = ("APPROVED C128 EDIT TARGET", "ACTUAL IMAGEGEN RETURN", "EXACT-MASK RESULT · VISUAL FAIL")
    for panel, title in zip(panels, titles):
        draw.rounded_rectangle(panel, radius=10, fill=(24, 39, 51, 255), outline=(75, 104, 120, 255), width=2)
        draw.text((panel[0] + 18, panel[1] + 14), title, font=font(19, True), fill=(231, 237, 236, 255))

    exact_bg = checker((525, 525), 25)
    exact_large = data["exact"].resize((500, 500), Image.Resampling.NEAREST)
    exact_bg.alpha_composite(exact_large, (12, 12))
    board.alpha_composite(exact_bg, (60, 205))

    raw_thumb = contain(data["raw"].convert("RGBA"), (525, 525))
    board.alpha_composite(raw_thumb, (697 + (525 - raw_thumb.width) // 2, 205 + (525 - raw_thumb.height) // 2))

    final_bg = checker((525, 525), 25)
    final_large = data["final"].resize((500, 500), Image.Resampling.NEAREST)
    final_bg.alpha_composite(final_large, (12, 12))
    board.alpha_composite(final_bg, (1334, 205))
    draw.rectangle((1334 + 12, 205 + 12, 1334 + 511, 205 + 511), outline=(82, 211, 236, 255), width=2)

    raw_bbox = data["raw_subject_bbox"]
    mask_bbox = data["work_mask_bbox"]
    coverage = data["coverage"]
    draw.text((35, 808), "Machine facts", font=font(22, True), fill=(255, 195, 82, 255))
    draw.multiline_text((35, 848),
        f"Raw return: 1254×1254 RGB; alpha channel absent; checker background baked into pixels.\n"
        f"Detected non-background subject bbox: {raw_bbox}; normalized width/height = {(raw_bbox[2]-raw_bbox[0])/1254:.3f}/{(raw_bbox[3]-raw_bbox[1])/1254:.3f}.\n"
        f"Approved mask mapped bbox: {mask_bbox}; normalized width/height = {(mask_bbox[2]-mask_bbox[0])/1254:.3f}/{(mask_bbox[3]-mask_bbox[1])/1254:.3f}.\n"
        f"Conservative dark-or-saturated content coverage inside approved mask: {coverage:.1%}. Mask-outside alpha after forcing: work={data['outside_work']}, final={data['outside_final']}.",
        font=font(17), fill=(218, 228, 231, 255), spacing=7)
    draw.text((35, 965), "Visual decision: FAIL", font=font(24, True), fill=(255, 113, 101, 255))
    draw.multiline_text((250, 963),
        "The generated body is substantially narrower and differently proportioned than the approved C mask.\n"
        "Forcing the mask exposes baked checker/background and misaligns crown, shoulders, forearms, hips, and feet. It is not a faithful cleanup.",
        font=font(17), fill=(239, 233, 225, 255), spacing=6)
    draw.text((35, 1035), "No second Guardian call and no BREAKER call were made, as required by Task69 §4.7.", font=font(17, True), fill=(174, 197, 208, 255))
    board.convert("RGB").save(OUT / OVERLAY_NAME, optimize=False)


def write_source_lock(paths: dict[str, Path]) -> None:
    rows = [
        ("TASK69", "producer task authority", TASK_REL, EXPECTED[TASK_REL], "consumed", "scope and stop rule", "Canon/Runtime promotion"),
        ("BOARD38", "current production board", BOARD_REL, EXPECTED[BOARD_REL], "consumed", "current Candidate lane", "downstream opening"),
        ("GZ_EXACT_C128", "immutable edit target and alpha mask", GZ_REL, EXPECTED[GZ_REL], "consumed_imagegen_image_1_and_mask", "composition silhouette proportion pivot", "redesign or mask change"),
        ("CML008", "Hard Guardian Z identity", GZ_CML008_REL, EXPECTED[GZ_CML008_REL], "consumed_imagegen_image_2", "identity details only", "proportion framing background noise"),
        ("V10X", "Candidate E02 local structure", GZ_V10X_REL, EXPECTED[GZ_V10X_REL], "consumed_imagegen_image_3", "two-arm no-wing no-backpack detail", "tall-body composition"),
        ("CML128_A", "Working KINETIC_CEL style", STYLE_REL, EXPECTED[STYLE_REL], "consumed_imagegen_image_4", "line pressure color blocks hard shadows only", "subject wings composition or Runtime"),
        ("BR_EXACT_B128", "immutable planned BREAKER target", BR_REL, EXPECTED[BR_REL], "not_consumed_mandated_stop", "future single edit only", "new body or reroll"),
        ("BR_B_SHEET", "user-approved B topology", BR_B_SHEET_REL, EXPECTED[BR_B_SHEET_REL], "not_consumed_mandated_stop", "future topology reference only", "A/C revival"),
        ("BR_X_BOARD", "user-approved X surface relations", BR_X_REL, EXPECTED[BR_X_REL], "not_consumed_mandated_stop", "future surface relation only", "new body or open core"),
        ("A4_VIEWPORT", "Candidate map review viewport", MAP_REL, EXPECTED[MAP_REL], "not_consumed_no_valid_pilot", "future visual preview only", "event staging or Runtime"),
        ("GZ_IMAGEGEN_RAW", "one allowed built-in edit return", str(RAW), RAW_SHA, "consumed_failure_evidence", "failure audit only", "visual master or reroll seed"),
    ]
    with (OUT / "source-lock.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source_id", "authority_role", "path", "sha256", "consumption", "allowed_use", "forbidden_use"))
        writer.writerows(rows)


def write_logs(data: dict[str, object]) -> None:
    generation_log = f"""# Task 69 generation log

## Call accounting

- Mode: built-in `image_gen` edit, per `imagegen` skill.
- Guardian Z edit calls: `1` of maximum `1`.
- Guardian Z rerolls: `0`.
- BREAKER edit calls: `0` of maximum `1`; not attempted because Guardian Z triggered the mandatory stop.
- Total ImageGen calls: `1`.

## Input roles

1. `{GZ_REL}` — edit target and immutable approved mask/composition.
2. `{GZ_CML008_REL}` — CML008 Hard identity reference only.
3. `{GZ_V10X_REL}` — V10X E02 detail reference only.
4. `{STYLE_REL}` — CML128 A/KINETIC_CEL style reference only.

## Actual returned file

- Built-in default path: `{RAW}`
- Workspace evidence copy: `{OUT / RAW_NAME}`
- SHA-256: `{RAW_SHA}`
- Actual format: `1254×1254 RGB`; no alpha channel.

## Actual prompt

```text
{ACTUAL_PROMPT}
```

## Stop decision

The single return baked the checker background into RGB and moved to a substantially narrower, differently proportioned body. Exact-mask forcing leaves background/checker pixels inside approved shoulder/arm regions and misregisters internal anatomy. It cannot become a faithful cleanup without a reroll, redraw, or structural reconstruction, all forbidden. Status: `FAILED_GUARDIAN_SINGLE_CALL / STOPPED_BEFORE_BREAKER`.
"""
    (OUT / "generation-log.md").write_text(generation_log, encoding="utf-8")

    review = f"""# Task 69 pilot self-review

Status: `FAILED_GUARDIAN_SINGLE_CALL / MANDATED_STOP / BREAKER_NOT_CALLED`

## Machine checks

- Raw result: `1254×1254 RGB`, no alpha. Requested transparent output was not delivered.
- Raw detected subject bbox: `{data['raw_subject_bbox']}`.
- Approved C mask mapped bbox: `{data['work_mask_bbox']}`.
- Conservative detected content coverage inside approved mask: `{data['coverage']:.1%}`.
- Mask-outside nonzero alpha after mechanical forcing: work `{data['outside_work']}`, final `{data['outside_final']}`.
- Exact-mask alpha containment therefore passes mechanically, but visible content alignment fails.

## Visual checks

- Identity: recognizable as a Guardian-Z-like red/blue super robot, but not the exact approved C body.
- Proportion and center of gravity: fail; generated subject is materially narrower and its internal body segmentation does not register to the C mask.
- Transparency: fail at raw source; checker pattern is baked into RGB.
- KINETIC_CEL finish: cleaner than the source proxy, but cannot be accepted because identity/mask fidelity is the higher gate.
- Faithful cleanup verdict: `FAIL`.

No A4 pilot preview or identity/style acceptance board was produced because there is no valid pilot frame to present. The required failure evidence is `{OVERLAY_NAME}`.
"""
    (OUT / "pilot-self-review.md").write_text(review, encoding="utf-8")

    report = f"""# Task 69 completion report

Status: `blocked_by_single_call_visual_failure / Candidate only / no Runtime`

Task69 explicitly requires a failed single edit to stop without reroll. Guardian Z's only allowed call failed the transparent-output and immutable-composition gates, so BREAKER was not called and the two-frame pilot package was not falsely completed.

## Preserved actual evidence

- `{RAW_NAME}` — byte-identical copy of the actual built-in result.
- `{WORK_NAME}` — actual RGB result with the approved C mask mechanically imposed at working resolution.
- `{FINAL_NAME}` — 256×256 mask-bound failure frame; evidence only, not a Pilot master.
- `{OVERLAY_NAME}` — actual-source/mask/failure comparison.
- `source-lock.tsv`, `generation-log.md`, `pilot-self-review.md`, and `delivery-hashes.sha256`.

## Required omissions caused by the stop rule

- No credible Guardian Z final Pilot.
- No BREAKER ImageGen call or frame.
- No `PILOT_ON_A4_MAP_1280x720.png` or `PILOT_IDENTITY_STYLE_REVIEW_1920x1080.png`, because presenting an invalid frame as a Pilot would violate the producer visual gate.

## Governance

- ImageGen calls: Guardian `1`, BREAKER `0`; rerolls `0`.
- Blender, redraw, paint-over, script-drawn mecha structure, Atlas, Godot, Runtime, LibTV, Canon migration, git add/commit: `0`.
- Output remains Candidate evidence and does not open UA91 or downstream work.
"""
    (OUT / "completion-report.md").write_text(report, encoding="utf-8")


def write_hashes() -> None:
    names = sorted(path.name for path in OUT.iterdir() if path.is_file() and path.name != "delivery-hashes.sha256")
    (OUT / "delivery-hashes.sha256").write_text("\n".join(f"{sha256(OUT / name)}  {name}" for name in names) + "\n", encoding="utf-8")


def main() -> None:
    paths = validate()
    data = build_images(paths)
    make_overlay(data)
    write_source_lock(paths)
    write_logs(data)
    write_hashes()
    print("status=FAILED_GUARDIAN_SINGLE_CALL_STOPPED_BEFORE_BREAKER")
    print(f"raw_subject_bbox={data['raw_subject_bbox']}")
    print(f"approved_mask_bbox={data['work_mask_bbox']}")
    print(f"detected_content_coverage={data['coverage']:.6f}")
    print(f"outside_work={data['outside_work']} outside_final={data['outside_final']}")


if __name__ == "__main__":
    main()
