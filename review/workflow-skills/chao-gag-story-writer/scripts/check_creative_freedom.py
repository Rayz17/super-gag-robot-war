#!/usr/bin/env python3
"""Check whether a story-writer brief leaves meaningful creative freedom."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "已锁事实",
    "戏剧要求",
    "主笔可改写范围",
    "开放问题",
    "未来保留",
)

SOLUTION_LEAK_PATTERNS = (
    re.compile(r"追逐最终由"),
    re.compile(r"(?:高潮|终局)(?:必须|固定|依次|最终)"),
    re.compile(r"四个(?:大)?动作完成"),
    re.compile(r"第一步.{0,120}第二步.{0,120}第三步", re.S),
    re.compile(r"正确答案"),
)

REVIEW_CONTAMINATION = re.compile(
    r"阻塞性问题|审稿结论|失败案例|坏句|回归案例|"
    r"PASS_FOR_USER_READ|REWRITE_ONCE|RESTART_FROM_IDEATION"
)


def section_body(text: str, title: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(title)}\s*$\n(.*?)(?=^##\s+|\Z)",
        re.M | re.S,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def bullet_count(body: str) -> int:
    return len(re.findall(r"^\s*(?:[-*]|\d+[.)])\s+", body, re.M))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    text = args.brief.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    if len(text) > 9000:
        warnings.append(f"brief is long: {len(text)} characters")

    for section in REQUIRED_SECTIONS:
        if not section_body(text, section):
            errors.append(f"missing or empty section: {section}")

    locked = bullet_count(section_body(text, "已锁事实"))
    dramatic = bullet_count(section_body(text, "戏剧要求"))
    open_questions = bullet_count(section_body(text, "开放问题"))

    if locked > 12:
        warnings.append(f"too many locked facts: {locked}")
    if dramatic > 8:
        warnings.append(f"too many dramatic requirements: {dramatic}")
    if open_questions < 3:
        errors.append(f"too few open questions: {open_questions}")

    for pattern in SOLUTION_LEAK_PATTERNS:
        if pattern.search(text):
            errors.append(f"possible climax solution leak: {pattern.pattern}")

    if REVIEW_CONTAMINATION.search(text):
        errors.append("review or negative-example language leaked into writer brief")

    quoted_lines = len(re.findall(r"^[^#\n]*[“”\"].*$", text, re.M))
    if quoted_lines > 8:
        warnings.append(
            f"many prewritten dialogue/quotation lines in brief: {quoted_lines}"
        )

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors or (args.strict and warnings):
        return 1

    print(
        "Creative freedom check passed: facts bounded, open questions present, "
        "no obvious climax-answer or review contamination."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
