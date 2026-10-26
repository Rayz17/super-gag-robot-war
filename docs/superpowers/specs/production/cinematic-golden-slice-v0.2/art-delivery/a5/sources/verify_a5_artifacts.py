import hashlib
import json
from pathlib import Path

from PIL import Image


def project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "game-godot").exists():
            return parent
    raise RuntimeError("project root not found")


ROOT = project_root()
BASE = ROOT / "docs/superpowers/specs/production/cinematic-golden-slice-v0.2"
MANIFEST = BASE / "art-phase-a5-manifest-v1.json"
METRICS = BASE / "art-phase-a5-layout-metrics-v1.json"
OLD_MANIFEST = BASE / "art-keyframe-manifest-v1.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


manifest = json.loads(MANIFEST.read_text())
metrics = json.loads(METRICS.read_text())
old_manifest = json.loads(OLD_MANIFEST.read_text())

expected_ids = {
    "KF_C01_RM_2P5D_RUNTIME_LAYOUT_V03",
    "LAYOUT_C01_RM_CAMERA_DEPTH_V01",
    "PLATE_C01_RM_HALL_CLEAN_TRIAL_V01",
    "BREAKDOWN_C01_RM_RUNTIME_LAYERS_V01",
    "SCALE_C01_RM_ACTOR_BRIDGE_V01",
}
assets = manifest["assets"]
assert {asset["stable_id"] for asset in assets} == expected_ids
assert manifest["phase"] == "phase_a5_runtime_composition_trial"
assert manifest["phase_b_generation_allowed"] is False

for asset in assets:
    path = ROOT / asset["delivery_path"]
    assert path.is_file(), path
    with Image.open(path) as image:
        assert image.size == (asset["width"], asset["height"]), (path, image.size)
        assert image.mode in ("RGB", "RGBA")
    assert sha256(path) == asset["sha256"], path
    assert asset["approval_status"] == "candidate_trial"
    assert asset["runtime_allowed"] is False
    assert asset["phase_b_generation_allowed"] is False

assert metrics["world_art_canvas"] == [1920, 900]
assert metrics["viewport"] == [1280, 720]
assert metrics["ui_safe_area_screen"] == {"left": 32, "top": 56, "right": 32, "bottom": 118}
assert [zone["center"][0] for zone in metrics["camera_zones"].values()] == [640, 960, 1280]
assert metrics["v03_actor_samples"]["jicun"]["height_px"] == 190
assert 180 <= metrics["v03_actor_samples"]["jicun"]["height_px"] <= 200
for actor_id in ("doudeng", "visitor", "jicun", "tangjiao"):
    assert 165 <= metrics["v03_actor_samples"][actor_id]["height_px"] <= 220
for actor_id in ("diedie", "machine_dog"):
    assert 60 <= metrics["v03_actor_samples"][actor_id]["height_px"] <= 100
assert metrics["scale_bridge"]["adult_heights_px"] == [165, 190, 220]
assert metrics["scale_bridge"]["small_robot_heights_px"] == [60, 80, 100]

old_asset = old_manifest["assets"][0]
old_path = ROOT / old_asset["delivery_path"]
assert old_asset["stable_id"] == "KF_C01_RM_2P5D_STYLE_V01"
assert old_asset["runtime_allowed"] is False
assert sha256(old_path) == old_asset["sha256"]

source_alpha = Image.open(BASE / "art-delivery/a5/sources/bridge_subjects_alpha_v01.png").convert("RGBA")
assert source_alpha.getchannel("A").getextrema() == (0, 255)
for corner in ((0, 0), (source_alpha.width - 1, 0), (0, source_alpha.height - 1), (source_alpha.width - 1, source_alpha.height - 1)):
    assert source_alpha.getpixel(corner)[3] == 0

phase_b_tokens = ("walk", "idle_", "four_direction", "cutin_", "halfbody_")
for path in (BASE / "art-delivery/a5").rglob("*"):
    if path.is_file():
        assert not any(token in path.name.lower() for token in phase_b_tokens), path

print("A5_ARTIFACT_VERIFY_OK 5/5 assets; Phase B assets 0; original keyframe unchanged")
