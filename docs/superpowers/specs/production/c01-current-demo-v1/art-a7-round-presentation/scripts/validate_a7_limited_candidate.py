#!/usr/bin/env python3.13
"""Read-only fail-closed validator for the A7 limited Candidate package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve()
while ROOT != ROOT.parent:
    if (ROOT / "docs/superpowers/specs/production/c01-current-demo-v1").is_dir():
        break
    ROOT = ROOT.parent
else:
    raise RuntimeError("repository root not found")

PRODUCTION = ROOT / "docs/superpowers/specs/production/c01-current-demo-v1"
TARGET = PRODUCTION / "art-a7-round-presentation"
PACKING = PRODUCTION / "42-c01e02-m3-r0-5-media-packing-v2.json"
IDENTITY = TARGET / "A7_IDENTITY_LOCK_GUARDIAN_C_BREAKER_BX_2400x1600.png"
APPROVED_MASTER = TARGET / "source/approved/R05_CUTIN_GIANT_CONTACT_1325_APPROVED_MASTER.png"

EXPECTED_SHA = {
    PACKING: "fe75667eac656756e35ddbbb784e250d39c0f8b05c2c14f719234d653b944012",
    PRODUCTION / "45-c01e02-m3-r0-5-a7-identity-lock-producer-review.md": "a90314f6357d18874e78c56312412e4253badc1365a8710e6c723471a064ca57",
    IDENTITY: "4aed7359548052bf11b6624bfe2cce79462b0266afd99358fabc702deebde575",
    APPROVED_MASTER: "b7430a2a03b7de4bd7f55ebe3d3aeb2ea4c71c6fcc49f0d8e367026d6070c630",
}

EXPECTED_CUTIN = {
    "R05_CUTIN_GIANT_CONTACT_1600x900.png",
    "R05_CUTIN_GIANT_CONTACT_BG_1600x900.png",
    "R05_CUTIN_GIANT_CONTACT_BREAKER_1600x900.png",
    "R05_CUTIN_GIANT_CONTACT_GUARDIAN_1600x900.png",
    "R05_CUTIN_GIANT_CONTACT_IMPACT_1600x900.png",
}
EXPECTED_FX = {
    "R05_FX_CONTACT_DUST_2048x256.png",
    "R05_FX_ARTILLERY_HIT_2048x256.png",
    "R05_FX_RED_CHARGE_2048x256.png",
}
EXPECTED_REVIEW = {
    "R05_REPRESENTATIVE_REVIEW_1280x720.png",
    "R05_FX_CONDITIONS_TECH_REVIEW_1280x720.png",
}
REQUIRED_DOCS = {
    "asset-manifest.tsv",
    "atlas-spec.tsv",
    "cutin-layer-spec.tsv",
    "fx-spec.tsv",
    "audio-spec.tsv",
    "source-validation-receipt.tsv",
    "user-decision-card.md",
    "completion-report.md",
    "core-delivery-hashes.sha256",
    "visual-media-probe.json",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class Checks:
    def __init__(self) -> None:
        self.records: list[dict[str, object]] = []

    def add(self, check_id: str, passed: bool, detail: str) -> None:
        self.records.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    @property
    def failures(self) -> list[dict[str, object]]:
        return [record for record in self.records if not record["passed"]]


def file_names(path: Path, suffix: str | None = None) -> set[str]:
    if not path.is_dir():
        return set()
    return {
        item.name
        for item in path.iterdir()
        if item.is_file() and (suffix is None or item.suffix.lower() == suffix)
    }


def decode_pcm24(path: Path) -> tuple[np.ndarray, int, int, int]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_width = handle.getsampwidth()
        sample_rate = handle.getframerate()
        frame_count = handle.getnframes()
        raw = handle.readframes(frame_count)
    if sample_width != 3:
        return np.empty((0, channels)), sample_rate, channels, sample_width
    bytes_ = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
    unsigned = bytes_[:, 0].astype(np.int32)
    unsigned |= bytes_[:, 1].astype(np.int32) << 8
    unsigned |= bytes_[:, 2].astype(np.int32) << 16
    signed = np.where(unsigned & 0x800000, unsigned - 0x1000000, unsigned)
    signal = signed.astype(np.float64).reshape(-1, channels) / 8_388_608.0
    return signal, sample_rate, channels, sample_width


def ffprobe(path: Path) -> dict[str, object]:
    command = [
        "/opt/homebrew/bin/ffprobe", "-v", "error",
        "-show_entries", "stream=codec_name,sample_rate,channels,bits_per_sample,bits_per_raw_sample:format=duration",
        "-of", "json", str(path),
    ]
    return json.loads(subprocess.check_output(command, text=True))


def validate_receipt(checks: Checks, path: Path, prefix: str) -> None:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        checks.add(f"{prefix}.present", bool(rows), f"rows={len(rows)}")
        for row in rows:
            resource_value = row.get("resource_path") or row.get("source_path")
            if not resource_value:
                raise KeyError("resource_path/source_path")
            resource = ROOT / resource_value
            actual = sha256(resource) if resource.is_file() else "missing"
            checks.add(
                f"{prefix}.{row.get('receipt_id', resource.name)}",
                actual == row["sha256"],
                f"expected={row['sha256']} actual={actual}",
            )
    except Exception as exc:
        checks.add(f"{prefix}.parse", False, str(exc))


def validate_visuals(checks: Checks, packing: dict[str, object]) -> None:
    cutin_dir = TARGET / "cutin"
    fx_dir = TARGET / "fx"
    review_dir = TARGET / "review"
    checks.add("scope.active_cutin_exact", file_names(cutin_dir, ".png") == EXPECTED_CUTIN, str(sorted(file_names(cutin_dir, ".png"))))
    checks.add("scope.active_fx_exact", file_names(fx_dir, ".png") == EXPECTED_FX, str(sorted(file_names(fx_dir, ".png"))))
    checks.add("scope.active_review_exact", file_names(review_dir, ".png") == EXPECTED_REVIEW, str(sorted(file_names(review_dir, ".png"))))
    checks.add("scope.no_map_atlas", not any((TARGET / "atlas").glob("*")), "atlas directory must contain no files")
    checks.add("scope.no_road_states", not any((TARGET / "road").glob("*")), "road directory must contain no files")
    videos = [path for path in TARGET.rglob("*") if path.is_file() and path.suffix.lower() in {".mp4", ".mov", ".webm", ".gif"}]
    checks.add("scope.no_animatic", not videos, str([str(path.relative_to(ROOT)) for path in videos]))

    composite_path = cutin_dir / "R05_CUTIN_GIANT_CONTACT_1600x900.png"
    with Image.open(composite_path) as source:
        composite = source.convert("RGBA")
        checks.add("cutin.composite_rgba", source.mode == "RGBA", f"mode={source.mode}")
        checks.add("cutin.composite_size", source.size == (1600, 900), f"size={source.size}")
    with Image.open(APPROVED_MASTER) as source:
        approved = np.asarray(source.convert("RGB"))
    checks.add(
        "cutin.approved_master_rgb_exact",
        np.array_equal(np.asarray(composite.convert("RGB")), approved),
        "active RGB pixels must equal the producer-passed 13:25 master",
    )

    layer_paths = [
        cutin_dir / "R05_CUTIN_GIANT_CONTACT_BG_1600x900.png",
        cutin_dir / "R05_CUTIN_GIANT_CONTACT_BREAKER_1600x900.png",
        cutin_dir / "R05_CUTIN_GIANT_CONTACT_GUARDIAN_1600x900.png",
        cutin_dir / "R05_CUTIN_GIANT_CONTACT_IMPACT_1600x900.png",
    ]
    layers: list[Image.Image] = []
    for path in layer_paths:
        with Image.open(path) as source:
            checks.add(f"layer.{path.stem}.rgba", source.mode == "RGBA", f"mode={source.mode}")
            checks.add(f"layer.{path.stem}.size", source.size == (1600, 900), f"size={source.size}")
            layer = source.convert("RGBA")
        alpha = np.asarray(layer.getchannel("A"))
        checks.add(f"layer.{path.stem}.alpha_present", int(alpha.max()) == 255, f"alpha_min={int(alpha.min())} alpha_max={int(alpha.max())}")
        if "_BG_" not in path.name:
            rgba = np.asarray(layer)
            hidden_rgb = rgba[..., :3][alpha == 0]
            clean = hidden_rgb.size == 0 or int(hidden_rgb.max()) == 0
            checks.add(f"layer.{path.stem}.transparent_rgb_zero", clean, "transparent pixels must not retain hidden master RGB")
        layers.append(layer)
    recomposed = layers[0].copy()
    for layer in layers[1:]:
        recomposed.alpha_composite(layer)
    delta = np.abs(np.asarray(recomposed, dtype=np.int16) - np.asarray(composite, dtype=np.int16))
    checks.add("layer.pixel_exact_recompose", int(delta.max()) == 0, f"max_channel_delta={int(delta.max())}")

    review_path = review_dir / "R05_REPRESENTATIVE_REVIEW_1280x720.png"
    with Image.open(review_path) as source:
        review = source.convert("RGB")
    expected_review = composite.resize((1280, 720), Image.Resampling.LANCZOS).convert("RGB")
    checks.add("review.master_from_active_only", np.array_equal(np.asarray(review), np.asarray(expected_review)), "review master must be a direct resize of active composite")

    slots = {slot["slot_id"]: slot for slot in packing["visual_slots"]}
    fx_map = {
        "R05_FX_CONTACT_DUST": fx_dir / "R05_FX_CONTACT_DUST_2048x256.png",
        "R05_FX_ARTILLERY_HIT": fx_dir / "R05_FX_ARTILLERY_HIT_2048x256.png",
        "R05_FX_RED_CHARGE": fx_dir / "R05_FX_RED_CHARGE_2048x256.png",
    }
    for slot_id, path in fx_map.items():
        spec = slots[slot_id]
        with Image.open(path) as source:
            checks.add(f"fx.{slot_id}.rgba", source.mode == "RGBA", f"mode={source.mode}")
            checks.add(f"fx.{slot_id}.size", list(source.size) == spec["total_size"], f"size={source.size}")
            atlas = source.convert("RGBA")
        nonempty = []
        for index in range(spec["frame_count"]):
            frame = atlas.crop((index * 256, 0, (index + 1) * 256, 256))
            nonempty.append(frame.getchannel("A").getbbox() is not None)
        checks.add(f"fx.{slot_id}.eight_nonempty_frames", len(nonempty) == 8 and all(nonempty), str(nonempty))


def validate_audio(checks: Checks, packing: dict[str, object]) -> None:
    audio_dir = TARGET / "audio"
    expected = {slot["slot_id"]: slot for slot in packing["audio_slots"]}
    actual_names = file_names(audio_dir, ".wav")
    expected_names = {f"{slot_id}.wav" for slot_id in expected}
    checks.add("audio.all_16_slots_exact", actual_names == expected_names, f"count={len(actual_names)} names={sorted(actual_names)}")

    for slot_id, spec in expected.items():
        path = audio_dir / f"{slot_id}.wav"
        if not path.is_file():
            checks.add(f"audio.{slot_id}.present", False, "missing")
            continue
        signal, rate, channels, width = decode_pcm24(path)
        probe = ffprobe(path)
        stream = probe["streams"][0]
        duration_ms = round(float(probe["format"]["duration"]) * 1000)
        bits = int(stream.get("bits_per_raw_sample") or stream.get("bits_per_sample") or 0)
        checks.add(f"audio.{slot_id}.codec", stream["codec_name"] == "pcm_s24le" and width == 3 and bits == 24, f"codec={stream['codec_name']} width={width} bits={bits}")
        checks.add(f"audio.{slot_id}.rate", rate == spec["sample_rate"] == 48000, f"rate={rate}")
        checks.add(f"audio.{slot_id}.channels", channels == spec["channels"], f"channels={channels} expected={spec['channels']}")
        checks.add(f"audio.{slot_id}.duration", duration_ms == spec["duration_ms"] and len(signal) == round(spec["duration_ms"] * rate / 1000), f"duration_ms={duration_ms} frames={len(signal)}")
        peak = float(np.max(np.abs(signal))) if signal.size else 0.0
        peak_dbfs = 20 * math.log10(max(peak, 1e-12))
        checks.add(f"audio.{slot_id}.peak", peak_dbfs <= -3.0, f"sample_peak_dbfs={peak_dbfs:.3f}")
        if spec["loop"]:
            boundary = float(np.max(np.abs(signal[-1] - signal[0])))
            sample_count = min(len(signal) - 1, 200_000)
            indices = np.linspace(0, len(signal) - 2, sample_count, dtype=np.int64)
            typical = float(np.percentile(np.abs(signal[indices + 1] - signal[indices]), 99))
            checks.add(f"audio.{slot_id}.loop_boundary", boundary <= max(0.006, typical * 1.5), f"boundary_delta={boundary:.6f} p99_adjacent={typical:.6f}")

    probe_path = audio_dir / "audio-media-probe.json"
    try:
        probe = json.loads(probe_path.read_text(encoding="utf-8"))
        probe_slots = {record["slot_id"] for record in probe["records"]}
        checks.add("audio.probe_all_16", probe_slots == set(expected), f"count={len(probe_slots)}")
        current = all(sha256(ROOT / record["resource_path"]) == record["sha256"] for record in probe["records"])
        checks.add("audio.probe_sha_current", current, "probe SHA values match current WAV bytes")
    except Exception as exc:
        checks.add("audio.probe_parse", False, str(exc))


def validate_documents(checks: Checks) -> None:
    checks.add("docs.required_present", REQUIRED_DOCS.issubset(file_names(TARGET)), str(sorted(REQUIRED_DOCS - file_names(TARGET))))
    manifest_path = TARGET / "asset-manifest.tsv"
    if manifest_path.is_file():
        with manifest_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        checks.add("manifest.nonempty", bool(rows), f"rows={len(rows)}")
        checks.add("manifest.candidate_only", all(row["classification"] == "Candidate" for row in rows), "all rows must be Candidate")
        checks.add("manifest.runtime_false", all(row["runtime_allowed"] == "false" for row in rows), "all rows runtime_allowed=false")
        checks.add("manifest.no_handoff", all(row["runtime_handoff"] == "none" for row in rows), "all rows runtime_handoff=none")
        forbidden = [row["resource_path"] for row in rows if "previs-only/" in row["resource_path"] or "rejected-exploration/" in row["resource_path"]]
        checks.add("manifest.no_previs_or_rejected", not forbidden, str(forbidden))
        paths_ok = True
        hashes_ok = True
        for row in rows:
            path = ROOT / row["resource_path"]
            paths_ok &= path.is_file()
            hashes_ok &= path.is_file() and sha256(path) == row["sha256"]
        checks.add("manifest.paths_exist", paths_ok, "all manifest resources exist")
        checks.add("manifest.hashes_current", hashes_ok, "all manifest SHA values match")
    else:
        checks.add("manifest.present", False, "asset-manifest.tsv missing")

    completion = TARGET / "completion-report.md"
    if completion.is_file():
        text = completion.read_text(encoding="utf-8")
        claims = [
            "Claim level: presentation judgeability only",
            "General common-turn causality: NOT PROVEN",
            "Editable route/waypoints: NOT IMPLEMENTED",
            "Commit summary completeness: INCOMPLETE IN FROZEN R0",
            "Derived mutation/settlement evidence: NOT PROVEN",
            "Actual route hash: NOT IMPLEMENTED",
            "R1 readiness: BLOCKED BY PRODUCTION BOARD HARD GATES",
        ]
        checks.add("completion.claim_boundary", all(claim in text for claim in claims), "43 mandatory claim block")
        checks.add("completion.runtime_boundary", "runtime_allowed=false" in text and "runtime_handoff=none" in text, "zero handoff boundary")

    hashes_path = TARGET / "core-delivery-hashes.sha256"
    if hashes_path.is_file():
        lines = [line.strip() for line in hashes_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]
        ok = True
        for line in lines:
            expected, resource = line.split(maxsplit=1)
            resource = resource.lstrip("*")
            path = ROOT / resource
            ok &= path.is_file() and sha256(path) == expected
        checks.add("hashes.core_current", bool(lines) and ok, f"entries={len(lines)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks = Checks()

    for path, expected in EXPECTED_SHA.items():
        actual = sha256(path) if path.is_file() else "missing"
        checks.add(f"authority.{path.name}", actual == expected, f"expected={expected} actual={actual}")
    with PACKING.open(encoding="utf-8") as handle:
        packing = json.load(handle)
    checks.add("authority.runtime_false", packing["runtime_allowed"] is False and packing["runtime_handoff"] == "none", "42 zero handoff")

    validate_visuals(checks, packing)
    validate_audio(checks, packing)
    validate_documents(checks)
    validate_receipt(checks, TARGET / "previs-only/previs-only-receipt.tsv", "isolation.v1")
    validate_receipt(checks, TARGET / "previs-only/v2-punch-misread/v2-punch-misread-receipt.tsv", "isolation.v2")
    validate_receipt(checks, TARGET / "rejected-exploration-receipt.tsv", "isolation.rejected")

    caches = [path for path in TARGET.rglob("*") if path.name == "__pycache__" or path.suffix == ".pyc"]
    checks.add("hygiene.no_python_cache", not caches, str([str(path.relative_to(ROOT)) for path in caches]))

    passed = not checks.failures
    payload = {
        "validator": "validate_a7_limited_candidate.py",
        "result": "PASS" if passed else "FAIL",
        "check_count": len(checks.records),
        "failure_count": len(checks.failures),
        "runtime_allowed": False,
        "runtime_handoff": "none",
        "checks": checks.records,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for record in checks.records:
            status = "PASS" if record["passed"] else "FAIL"
            print(f"[{status}] {record['check_id']}: {record['detail']}")
        print(f"RESULT={payload['result']} checks={payload['check_count']} failures={payload['failure_count']}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
