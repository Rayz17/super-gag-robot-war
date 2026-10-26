#!/usr/bin/env python3
"""Rebuild A6 state masters, source-layer composites, and packing-v2 atlases."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = shutil.which("ffmpeg")


def run_ffmpeg(inputs: list[Path], output: Path, *, vf: str | None = None, graph: str | None = None) -> None:
    if not FFMPEG:
        raise SystemExit("ffmpeg is required")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y"]
    for source in inputs:
        cmd.extend(["-i", str(source)])
    if vf:
        cmd.extend(["-vf", vf])
    if graph:
        cmd.extend(["-filter_complex", graph])
    cmd.extend(["-frames:v", "1", str(output)])
    subprocess.run(cmd, check=True)


def keyed_state(source: str, output: str, size: tuple[int, int], inner: tuple[int, int], offset: tuple[int, int]) -> None:
    width, height = size
    inner_width, inner_height = inner
    x, y = offset
    vf = (
        "chromakey=0x00ff00:0.10:0.08,despill=green,"
        f"scale={inner_width}:{inner_height}:flags=lanczos,format=rgba,"
        f"pad={width}:{height}:{x}:{y}:color=black@0,format=rgba"
    )
    run_ffmpeg([ROOT / source], ROOT / output, vf=vf)


def overlay(base: str, layer: str, output: str) -> None:
    run_ffmpeg(
        [ROOT / base, ROOT / layer],
        ROOT / output,
        graph="[0:v][1:v]overlay=0:0:format=auto,format=rgba",
    )


def hstack(inputs: list[str], output: str) -> None:
    labels = "".join(f"[{index}:v]" for index in range(len(inputs)))
    graph = f"{labels}hstack=inputs={len(inputs)},format=rgba"
    run_ffmpeg([ROOT / source for source in inputs], ROOT / output, graph=graph)


def build_qihai_noise_mask() -> None:
    """Build a low-alpha, deterministic remote-signal mask inside Qihai's safe rect."""
    if not FFMPEG:
        raise SystemExit("ffmpeg is required")
    output = ROOT / "source-layers/qihai/remote-noise-mask-768.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    filters = ["color=c=black@0.0:s=768x768", "format=rgba"]
    for y in range(58, 744, 19):
        opacity = "0.09" if y % 38 else "0.14"
        filters.append(
            f"drawbox=x=96:y={y}:w=576:h=1:c=0xd8f8ff@{opacity}:t=fill:replace=1"
        )
    for index in range(46):
        x = 104 + (index * 83) % 552
        y = 61 + (index * 137) % 668
        width = 2 + (index * 7) % 13
        opacity = "0.22" if index % 5 == 0 else "0.13"
        filters.append(
            f"drawbox=x={x}:y={y}:w={width}:h=2:c=0xe8fbff@{opacity}:t=fill:replace=1"
        )
    subprocess.run(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            ",".join(filters),
            "-frames:v",
            "1",
            str(output),
        ],
        check=True,
    )


def build_guardian_waveform(state: str) -> None:
    """Build the separate amber waveform layer required by packing v2."""
    if not FFMPEG:
        raise SystemExit("ffmpeg is required")
    patterns = {
        "guide": [8, 12, 18, 10, 22, 14, 9, 16, 11, 7, 13, 9],
        "contact": [10, 26, 15, 34, 20, 42, 17, 30, 12, 24, 16, 9],
        "shield_gaze": [7, 11, 8, 16, 10, 20, 9, 14, 8, 12, 7, 6],
    }
    output = ROOT / f"source-layers/old_guardian/{state}/waveform-rgba-1024x768.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    filters = ["color=c=black@0.0:s=1024x768", "format=rgba"]
    filters.append(
        "drawbox=x=292:y=694:w=440:h=1:c=0xffbd43@0.20:t=fill:replace=1"
    )
    for index, height in enumerate(patterns[state]):
        x = 316 + index * 34
        y = 694 - height // 2
        filters.append(
            f"drawbox=x={x}:y={y}:w=8:h={height}:c=0xffc35a@0.72:t=fill:replace=1"
        )
    subprocess.run(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            ",".join(filters),
            "-frames:v",
            "1",
            str(output),
        ],
        check=True,
    )


def split_guardian_layer(state: str) -> None:
    body = ROOT / f"source-layers/old_guardian/{state}/body-rgba-1024x768.png"
    run_ffmpeg(
        [body],
        ROOT / f"source-layers/old_guardian/{state}/head-rgba-1024x768.png",
        vf="crop=1024:400:0:0,pad=1024:768:0:0:color=black@0,format=rgba",
    )
    run_ffmpeg(
        [body],
        ROOT / f"source-layers/old_guardian/{state}/chest-rgba-1024x768.png",
        vf="crop=1024:368:0:400,pad=1024:768:0:400:color=black@0,format=rgba",
    )


def main() -> None:
    jicun_states = ["focused", "alarm", "resolve"]
    qihai_states = ["controlled", "decision", "concerned"]
    guardian_sources = {
        "guide": "old-guardian-guide-keyed-source.png",
        "contact": "old-guardian-contact-keyed-source.png",
        "shield_gaze": "old-guardian-shield-gaze-keyed-source.png",
    }

    build_qihai_noise_mask()

    for state in jicun_states:
        keyed_state(
            f"sources/chroma/jicun-{state}-keyed-source.png",
            f"assets/portraits/jicun/r05-portrait-jicun-{state}-768.png",
            (768, 768),
            (576, 576),
            (96, 168),
        )

    for state in qihai_states:
        keyed_state(
            f"sources/chroma/qihai-{state}-keyed-source.png",
            f"assets/portraits/qihai/r05-portrait-qihai-remote-{state}-768.png",
            (768, 768),
            (576, 576),
            (96, 168),
        )
        overlay(
            f"assets/portraits/qihai/r05-portrait-qihai-remote-{state}-768.png",
            "source-layers/qihai/remote-noise-mask-768.png",
            f"assets/portraits/qihai/composite/r05-portrait-qihai-remote-{state}-composite-768.png",
        )

    for state, source in guardian_sources.items():
        build_guardian_waveform(state)
        keyed_state(
            f"sources/chroma/{source}",
            f"source-layers/old_guardian/{state}/body-rgba-1024x768.png",
            (1024, 768),
            (928, 696),
            (48, 36),
        )
        split_guardian_layer(state)
        overlay(
            f"source-layers/old_guardian/{state}/body-rgba-1024x768.png",
            f"source-layers/old_guardian/{state}/waveform-rgba-1024x768.png",
            f"assets/comms/old_guardian/states/r05-comms-old-guardian-{state}-1024x768.png",
        )

    hstack(
        [f"assets/portraits/jicun/r05-portrait-jicun-{state}-768.png" for state in jicun_states],
        "assets/atlases/r05-portrait-jicun-states-2304x768.png",
    )
    hstack(
        [
            f"assets/portraits/qihai/composite/r05-portrait-qihai-remote-{state}-composite-768.png"
            for state in qihai_states
        ],
        "assets/atlases/r05-portrait-qihai-remote-states-2304x768.png",
    )
    hstack(
        [
            f"assets/comms/old_guardian/states/r05-comms-old-guardian-{state}-1024x768.png"
            for state in guardian_sources
        ],
        "assets/atlases/r05-comms-old-guardian-states-3072x768.png",
    )

    print("A6_CORE_ASSETS_REBUILT")


if __name__ == "__main__":
    main()
