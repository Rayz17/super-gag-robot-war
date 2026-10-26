#!/usr/bin/env python3
"""Build A6 text-free 720p state boards, layout reviews, and simulations."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT.parents[1]
FFMPEG = shutil.which("ffmpeg")

MAP = PRODUCTION / "c01-current-demo-v1/art-a4-map-b-six-layer/A4_MAP_B_pure_read_no_ui_2400x1350.png"
DOUDENG_OBSERVE = PRODUCTION / (
    "battle-presentation-v0.1/art-delivery/approved/cutin_doudeng_c01_observe_v01.png"
)
DOUDENG_TENSE = PRODUCTION / (
    "battle-presentation-v0.1/art-delivery/approved/cutin_doudeng_c01_tense_v01.png"
)


def render(
    output: str,
    inputs: list[Path],
    graph: str,
    *,
    color_source: str | None = None,
) -> None:
    if not FFMPEG:
        raise SystemExit("ffmpeg is required")
    destination = ROOT / output
    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y"]
    if color_source:
        command.extend(["-f", "lavfi", "-i", color_source])
    for source in inputs:
        command.extend(["-i", str(source)])
    command.extend(
        [
            "-filter_complex",
            graph,
            "-map",
            "[out]",
            "-frames:v",
            "1",
            "-pix_fmt",
            "rgba",
            str(destination),
        ]
    )
    subprocess.run(command, check=True)


def state_board(
    output: str,
    inputs: list[Path],
    *,
    image_size: tuple[int, int],
    positions: list[tuple[int, int]],
    panels: list[tuple[int, int, int, int]],
    accents: list[str],
    panel_color: str,
) -> None:
    background_filters = [
        "format=rgba",
        "drawbox=x=0:y=0:w=1280:h=720:c=0x071117:t=fill",
        "drawbox=x=0:y=52:w=1280:h=2:c=0x7ad8e8@0.28:t=fill",
        "drawbox=x=0:y=666:w=1280:h=2:c=0xffbd43@0.22:t=fill",
    ]
    for panel, accent in zip(panels, accents):
        x, y, width, height = panel
        background_filters.extend(
            [
                f"drawbox=x={x}:y={y}:w={width}:h={height}:c={panel_color}:t=fill",
                f"drawbox=x={x}:y={y}:w={width}:h={height}:c={accent}@0.48:t=2",
                f"drawbox=x={x}:y={y}:w={width}:h=7:c={accent}@0.88:t=fill",
            ]
        )
    graph_parts = [f"[0:v]{','.join(background_filters)}[bg]"]
    previous = "[bg]"
    width, height = image_size
    for index, (x, y) in enumerate(positions, start=1):
        graph_parts.append(
            f"[{index}:v]scale={width}:{height}:flags=lanczos,format=rgba[p{index}]"
        )
        graph_parts.append(
            f"{previous}[p{index}]overlay=x={x}:y={y}:format=auto[v{index}]"
        )
        previous = f"[v{index}]"
    graph_parts.append(f"{previous}format=rgba[out]")
    render(
        output,
        inputs,
        ";".join(graph_parts),
        color_source="color=c=0x071117:s=1280x720:r=1",
    )


def build_state_boards() -> None:
    state_board(
        "boards/jicun-state-board-1280x720.png",
        [
            ROOT / f"assets/portraits/jicun/r05-portrait-jicun-{state}-768.png"
            for state in ("focused", "alarm", "resolve")
        ],
        image_size=(384, 384),
        positions=[(40, 166), (448, 166), (856, 166)],
        panels=[(32, 132, 400, 470), (440, 132, 400, 470), (848, 132, 400, 470)],
        accents=["0x70d6e8", "0xff6b61", "0xffbe4d"],
        panel_color="0x101c24@0.96",
    )
    state_board(
        "boards/qihai-state-board-1280x720.png",
        [
            ROOT / (
                "assets/portraits/qihai/composite/"
                f"r05-portrait-qihai-remote-{state}-composite-768.png"
            )
            for state in ("controlled", "decision", "concerned")
        ],
        image_size=(384, 384),
        positions=[(40, 166), (448, 166), (856, 166)],
        panels=[(32, 132, 400, 470), (440, 132, 400, 470), (848, 132, 400, 470)],
        accents=["0x76dbe9", "0xffbd43", "0xe48678"],
        panel_color="0x0b1c24@0.98",
    )
    state_board(
        "boards/old-guardian-state-board-1280x720.png",
        [
            ROOT / f"assets/comms/old_guardian/states/r05-comms-old-guardian-{state}-1024x768.png"
            for state in ("guide", "contact", "shield_gaze")
        ],
        image_size=(392, 294),
        positions=[(20, 210), (444, 210), (868, 210)],
        panels=[(12, 178, 408, 358), (436, 178, 408, 358), (860, 178, 408, 358)],
        accents=["0x7bd7e8", "0xff744f", "0xffbd43"],
        panel_color="0x141b20@0.98",
    )


def build_doudeng_board() -> None:
    graph = ";".join(
        [
            "[0:v]format=rgba,"
            "drawbox=x=0:y=0:w=1280:h=720:c=0x071117:t=fill,"
            "drawbox=x=144:y=18:w=992:h=326:c=0x102129@0.96:t=fill,"
            "drawbox=x=144:y=18:w=992:h=326:c=0x72d8e8@0.60:t=2,"
            "drawbox=x=160:y=86:w=430:h=164:c=0x72d8e8@0.12:t=fill,"
            "drawbox=x=160:y=86:w=430:h=164:c=0x72d8e8@0.52:t=2,"
            "drawbox=x=144:y=376:w=992:h=326:c=0x101b22@0.96:t=fill,"
            "drawbox=x=144:y=376:w=992:h=326:c=0xff8a5d@0.60:t=2,"
            "drawbox=x=160:y=444:w=430:h=164:c=0xff8a5d@0.10:t=fill,"
            "drawbox=x=160:y=444:w=430:h=164:c=0xff8a5d@0.50:t=2[bg]",
            "[1:v]scale=960:320:flags=lanczos,format=rgba[observe]",
            "[2:v]scale=960:320:flags=lanczos,format=rgba[tense]",
            "[bg][observe]overlay=x=160:y=20:format=auto[v1]",
            "[v1][tense]overlay=x=160:y=378:format=auto,format=rgba[out]",
        ]
    )
    render(
        "boards/doudeng-approved-layout-board-1280x720.png",
        [DOUDENG_OBSERVE, DOUDENG_TENSE],
        graph,
        color_source="color=c=0x071117:s=1280x720:r=1",
    )


def build_alpha_board() -> None:
    inputs = [
        ROOT / f"assets/portraits/jicun/r05-portrait-jicun-{state}-768.png"
        for state in ("focused", "alarm", "resolve")
    ]
    inputs.extend(
        ROOT / f"assets/portraits/qihai/r05-portrait-qihai-remote-{state}-768.png"
        for state in ("controlled", "decision", "concerned")
    )
    inputs.extend(
        ROOT / f"assets/comms/old_guardian/states/r05-comms-old-guardian-{state}-1024x768.png"
        for state in ("guide", "contact", "shield_gaze")
    )
    positions = [
        (100, 10), (480, 10), (860, 10),
        (100, 250), (480, 250), (860, 250),
        (64, 490), (444, 490), (824, 490),
    ]
    graph_parts = [
        "[0:v]format=rgba,"
        "drawbox=x=0:y=0:w=1280:h=720:c=0x293239:t=fill,"
        "drawgrid=w=24:h=24:t=1:c=0xffffff@0.12,"
        "drawbox=x=0:y=0:w=10:h=240:c=0x70d6e8:t=fill,"
        "drawbox=x=0:y=240:w=10:h=240:c=0xe48678:t=fill,"
        "drawbox=x=0:y=480:w=10:h=240:c=0xffbd43:t=fill[bg]"
    ]
    previous = "[bg]"
    for index, (x, y) in enumerate(positions, start=1):
        size = "220:220" if index <= 6 else "294:220"
        graph_parts.append(f"[{index}:v]scale={size}:flags=lanczos,format=rgba[p{index}]")
        graph_parts.append(f"{previous}[p{index}]overlay=x={x}:y={y}:format=auto[v{index}]")
        previous = f"[v{index}]"
    graph_parts.append(f"{previous}format=rgba[out]")
    render(
        "boards/alpha-edge-review-board-1280x720.png",
        inputs,
        ";".join(graph_parts),
        color_source="color=c=0x293239:s=1280x720:r=1",
    )


def build_safe_area_board() -> None:
    jicun = ROOT / "assets/portraits/jicun/r05-portrait-jicun-focused-768.png"
    guardian = ROOT / "assets/comms/old_guardian/states/r05-comms-old-guardian-contact-1024x768.png"
    graph = ";".join(
        [
            "[0:v]format=rgba,"
            "drawbox=x=0:y=0:w=1280:h=720:c=0x071117:t=fill,"
            "drawbox=x=0:y=358:w=1280:h=4:c=0xffffff@0.12:t=fill,"
            "drawbox=x=18:y=32:w=290:h=296:c=0x70d6e8@0.14:t=fill,"
            "drawbox=x=18:y=32:w=290:h=296:c=0x70d6e8@0.72:t=3,"
            "drawbox=x=328:y=108:w=468:h=144:c=0x70d6e8@0.10:t=fill,"
            "drawbox=x=328:y=108:w=468:h=144:c=0x70d6e8@0.56:t=2,"
            "drawbox=x=862:y=388:w=400:h=312:c=0xffbd43@0.13:t=fill,"
            "drawbox=x=862:y=388:w=400:h=312:c=0xffbd43@0.72:t=3,"
            "drawbox=x=328:y=470:w=468:h=144:c=0xffbd43@0.10:t=fill,"
            "drawbox=x=328:y=470:w=468:h=144:c=0xffbd43@0.56:t=2[bg]",
            "[1:v]scale=288:288:flags=lanczos,format=rgba[j1]",
            "[1:v]scale=250:250:flags=lanczos,format=rgba,colorchannelmixer=aa=0.48[j2]",
            "[2:v]scale=780:260:flags=lanczos,format=rgba,colorchannelmixer=aa=0.46[d]",
            "[3:v]scale=392:294:flags=lanczos,format=rgba[g]",
            "[bg][d]overlay=x=490:y=64:format=auto[v1]",
            "[v1][j1]overlay=x=20:y=34:format=auto[v2]",
            "[v2][j2]overlay=x=24:y=432:format=auto[v3]",
            "[v3][g]overlay=x=866:y=404:format=auto,format=rgba[out]",
        ]
    )
    render(
        "boards/layout-safe-area-review-board-1280x720.png",
        [jicun, DOUDENG_OBSERVE, guardian],
        graph,
        color_source="color=c=0x071117:s=1280x720:r=1",
    )


def build_local_simulation() -> None:
    jicun = ROOT / "assets/portraits/jicun/r05-portrait-jicun-focused-768.png"
    graph = ";".join(
        [
            "[0:v]scale=1280:720:flags=lanczos,eq=brightness=-0.08:saturation=0.82,format=rgba,"
            "drawbox=x=0:y=414:w=1280:h=306:c=0x061017@0.88:t=fill,"
            "drawbox=x=20:y=420:w=306:h=300:c=0x70d6e8@0.14:t=fill,"
            "drawbox=x=20:y=420:w=306:h=300:c=0x70d6e8@0.78:t=3,"
            "drawbox=x=342:y=490:w=456:h=156:c=0x70d6e8@0.10:t=fill,"
            "drawbox=x=342:y=490:w=456:h=156:c=0x70d6e8@0.56:t=2[bg]",
            "[1:v]scale=300:300:flags=lanczos,format=rgba[j]",
            "[2:v]scale=900:300:flags=lanczos,format=rgba,colorchannelmixer=aa=0.66[d]",
            "[bg][d]overlay=x=366:y=420:format=auto[v1]",
            "[v1][j]overlay=x=24:y=420:format=auto,format=rgba[out]",
        ]
    )
    render(
        "simulations/jicun-doudeng-local-1280x720.png",
        [MAP, jicun, DOUDENG_OBSERVE],
        graph,
    )


def build_qihai_presence_simulation() -> None:
    jicun = ROOT / "assets/portraits/jicun/r05-portrait-jicun-focused-768.png"
    qihai = ROOT / (
        "assets/portraits/qihai/composite/"
        "r05-portrait-qihai-remote-decision-composite-768.png"
    )
    graph = ";".join(
        [
            "[0:v]scale=1280:720:flags=lanczos,eq=brightness=-0.05:saturation=0.86,format=rgba,"
            "drawbox=x=920:y=0:w=360:h=720:c=0x06151d@0.98:t=fill,"
            "drawbox=x=920:y=0:w=3:h=720:c=0x72d8e8@0.70:t=fill,"
            "drawbox=x=936:y=48:w=328:h=438:c=0x0a202a@0.96:t=fill,"
            "drawbox=x=936:y=48:w=328:h=438:c=0x72d8e8@0.82:t=2,"
            "drawbox=x=942:y=54:w=316:h=426:c=0x72d8e8@0.24:t=1,"
            "drawbox=x=952:y=390:w=120:h=18:c=0x72d8e8@0.10:t=fill,"
            "drawbox=x=952:y=390:w=120:h=18:c=0x72d8e8@0.50:t=1,"
            "drawbox=x=952:y=416:w=286:h=14:c=0x72d8e8@0.09:t=fill,"
            "drawbox=x=952:y=416:w=286:h=14:c=0x72d8e8@0.45:t=1,"
            "drawbox=x=952:y=442:w=286:h=28:c=0xffbd43@0.10:t=fill,"
            "drawbox=x=952:y=442:w=286:h=28:c=0xffbd43@0.58:t=1,"
            "drawbox=x=18:y=498:w=226:h=218:c=0x70d6e8@0.12:t=fill,"
            "drawbox=x=18:y=498:w=226:h=218:c=0x70d6e8@0.64:t=2,"
            "drawbox=x=268:y=574:w=520:h=112:c=0x70d6e8@0.09:t=fill,"
            "drawbox=x=268:y=574:w=520:h=112:c=0x70d6e8@0.48:t=2[bg]",
            "[1:v]scale=220:220:flags=lanczos,format=rgba[j]",
            "[2:v]scale=320:320:flags=lanczos,format=rgba[q]",
            "[bg][q]overlay=x=940:y=60:format=auto[v1]",
            "[v1][j]overlay=x=20:y=500:format=auto,format=rgba[out]",
        ]
    )
    render(
        "simulations/jicun-qihai-remote-presence-1280x720.png",
        [MAP, jicun, qihai],
        graph,
    )


def build_guardian_simulation() -> None:
    jicun = ROOT / "assets/portraits/jicun/r05-portrait-jicun-resolve-768.png"
    guardian = ROOT / "assets/comms/old_guardian/states/r05-comms-old-guardian-contact-1024x768.png"
    graph = ";".join(
        [
            "[0:v]scale=1280:720:flags=lanczos,eq=brightness=-0.10:saturation=0.78,format=rgba,"
            "drawbox=x=0:y=402:w=1280:h=318:c=0x080f14@0.90:t=fill,"
            "drawbox=x=16:y=420:w=304:h=300:c=0x83949d@0.10:t=fill,"
            "drawbox=x=16:y=420:w=304:h=300:c=0x83949d@0.36:t=2,"
            "drawbox=x=326:y=490:w=458:h=158:c=0xffbd43@0.10:t=fill,"
            "drawbox=x=326:y=490:w=458:h=158:c=0xffbd43@0.58:t=2,"
            "drawbox=x=796:y=360:w=480:h=360:c=0xffbd43@0.13:t=fill,"
            "drawbox=x=796:y=360:w=480:h=360:c=0xffbd43@0.78:t=3[bg]",
            "[1:v]scale=300:300:flags=lanczos,format=rgba,colorchannelmixer=aa=0.52[j]",
            "[2:v]scale=480:360:flags=lanczos,format=rgba[g]",
            "[bg][j]overlay=x=18:y=420:format=auto[v1]",
            "[v1][g]overlay=x=796:y=360:format=auto,format=rgba[out]",
        ]
    )
    render(
        "simulations/jicun-old-guardian-machine-1280x720.png",
        [MAP, jicun, guardian],
        graph,
    )


def main() -> None:
    build_state_boards()
    build_doudeng_board()
    build_alpha_board()
    build_safe_area_board()
    build_local_simulation()
    build_qihai_presence_simulation()
    build_guardian_simulation()
    print("A6_REVIEW_ASSETS_REBUILT")


if __name__ == "__main__":
    main()
