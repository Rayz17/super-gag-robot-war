#!/usr/bin/env python3
"""Check required headings inside Markdown episode blocks."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown file to check")
    parser.add_argument(
        "--episode-regex",
        default=r"^## .+",
        help="Regex matching episode heading lines. Default: '^## .+'",
    )
    parser.add_argument(
        "--heading",
        action="append",
        default=[],
        help="Required heading text inside each episode block. Repeatable.",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Exit 0 when no episode headings match.",
    )
    parser.add_argument(
        "--min-block-chars",
        type=int,
        default=0,
        help="Minimum non-whitespace character count required for each episode block.",
    )
    parser.add_argument(
        "--max-min-ratio",
        type=float,
        default=0.0,
        help="Maximum allowed ratio between longest and shortest episode block.",
    )
    parser.add_argument(
        "--report-lengths",
        action="store_true",
        help="Print non-whitespace character counts for each episode block.",
    )
    return parser.parse_args()


def find_blocks(text: str, episode_regex: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    pattern = re.compile(episode_regex)
    starts: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if pattern.search(line):
            starts.append((i, line.strip()))

    blocks: list[tuple[str, str]] = []
    for idx, (start, title) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        blocks.append((title, "\n".join(lines[start:end])))
    return blocks


def main() -> int:
    args = parse_args()
    text = args.path.read_text(encoding="utf-8")
    blocks = find_blocks(text, args.episode_regex)
    if not blocks:
        print(f"No episode blocks matched: {args.episode_regex}")
        return 0 if args.allow_empty else 2

    failures: list[str] = []
    lengths: list[tuple[str, int]] = []
    for title, block in blocks:
        missing = [heading for heading in args.heading if heading not in block]
        if missing:
            failures.append(f"{title}: missing {', '.join(missing)}")
        compact_len = len(re.sub(r"\s+", "", block))
        lengths.append((title, compact_len))
        if args.min_block_chars and compact_len < args.min_block_chars:
            failures.append(
                f"{title}: only {compact_len} non-whitespace chars, below minimum {args.min_block_chars}"
            )

    if args.max_min_ratio and lengths:
        shortest_title, shortest = min(lengths, key=lambda item: item[1])
        longest_title, longest = max(lengths, key=lambda item: item[1])
        if shortest == 0:
            failures.append(f"{shortest_title}: empty block prevents ratio check")
        elif longest / shortest > args.max_min_ratio:
            failures.append(
                "length ratio "
                f"{longest / shortest:.2f} exceeds maximum {args.max_min_ratio:.2f} "
                f"(shortest {shortest}: {shortest_title}; longest {longest}: {longest_title})"
            )

    print(f"Checked {len(blocks)} episode block(s) in {args.path}")
    if args.report_lengths:
        print("Block lengths:")
        for title, compact_len in lengths:
            print(f"- {compact_len}: {title}")
    if failures:
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("All required headings present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
