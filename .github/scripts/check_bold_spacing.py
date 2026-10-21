# -*- coding: utf-8 -*-
"""检查 Markdown 加粗（**...**）两侧的空格是否符合规范。

规则：
1. 第一个 ** 前必须有且只有一个半角空格；行首、列表/引用/标题标记之后属例外。
2. 第二个 ** 后必须有且只有一个半角空格；行尾属例外。
3. 加粗紧邻标点（中英文标点）时，该侧免加空格，避免出现
   ``**Phil Agre** ,`` 这类错误排版。

代码块（含引用块内的围栏）、行内代码不参与检查。

用法：
    python .github/scripts/check_bold_spacing.py          # 只检查，有问题时退出码为 1
    python .github/scripts/check_bold_spacing.py --fix    # 就地修复
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".github", ".gitbook", "en", "node_modules", "script"}

FENCE_RE = re.compile(r"^\s*(?:>\s*)*(?:`{3,}|~{3,})")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return files


def mask_inline_code(line: str) -> str:
    """把行内代码替换为等长占位符，保持列号对齐。"""
    chars = list(line)
    i = 0
    while i < len(line):
        if line[i] != "`":
            i += 1
            continue
        j = i
        while j < len(line) and line[j] == "`":
            j += 1
        ticks = line[i:j]
        end = line.find(ticks, j)
        if end == -1:
            i = j
            continue
        for k in range(i, end + len(ticks)):
            chars[k] = "\x00"
        i = end + len(ticks)
    return "".join(chars)


def is_punctuation(ch: str) -> bool:
    if ch == "\x00":
        return False
    return unicodedata.category(ch).startswith("P")


def count_leading_spaces(text: str) -> int:
    return len(text) - len(text.lstrip(" "))


def count_trailing_spaces(text: str) -> int:
    return len(text) - len(text.rstrip(" "))


def scan_line(line: str) -> list[tuple[int, str]]:
    """返回 [(列号, 问题描述)]。"""
    problems: list[tuple[int, str]] = []
    masked = mask_inline_code(line)
    for m in BOLD_RE.finditer(masked):
        start, end = m.start(), m.end()

        before = masked[:start]
        if before and before.strip():
            spaces = count_trailing_spaces(before)
            if spaces == 0 and not is_punctuation(before[-1]):
                problems.append((start, "第一个 ** 前缺少空格"))
            elif spaces > 1:
                problems.append((start, "第一个 ** 前空格多于一个"))

        after = masked[end:]
        if after and after.strip():
            spaces = count_leading_spaces(after)
            if spaces == 0 and not is_punctuation(after[0]):
                problems.append((end, "第二个 ** 后缺少空格"))
            elif spaces > 1:
                problems.append((end, "第二个 ** 后空格多于一个"))
    return problems


def fix_line(line: str) -> str:
    """收集插入/合并空格的编辑，再按原字符串坐标逆序应用。"""
    edits: list[tuple[int, int, int]] = []  # (起始位置, 删除长度, 插入长度)
    masked = mask_inline_code(line)

    for m in BOLD_RE.finditer(masked):
        start, end = m.start(), m.end()

        before = masked[:start]
        if before and before.strip():
            spaces = count_trailing_spaces(before)
            if spaces == 0 and not is_punctuation(before[-1]):
                edits.append((start, 0, 1))
            elif spaces > 1:
                edits.append((start - spaces, spaces, 1))

        after = masked[end:]
        if after and after.strip():
            spaces = count_leading_spaces(after)
            if spaces == 0 and not is_punctuation(after[0]):
                edits.append((end, 0, 1))
            elif spaces > 1:
                edits.append((end, spaces, 1))

    for pos, remove, insert in sorted(edits, reverse=True):
        line = line[:pos] + (" " * insert) + line[pos + remove:]
    return line


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="就地修复")
    args = parser.parse_args()

    total = 0
    fixed_files = 0
    report: list[str] = []

    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        in_fence = False
        out_lines: list[str] = []
        changed = False

        for lineno, line in enumerate(lines, 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                out_lines.append(line)
                continue
            if in_fence or not line.strip():
                out_lines.append(line)
                continue

            problems = scan_line(line)
            for col, msg in problems:
                snippet = line[max(0, col - 12):col + 16]
                report.append(
                    f"{path.relative_to(ROOT).as_posix()}:{lineno}:{col + 1}: "
                    f"{msg} | {snippet}"
                )
                total += 1

            if args.fix and problems:
                line = fix_line(line)
                changed = True
            out_lines.append(line)

        if changed:
            new_text = "\n".join(out_lines)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                fixed_files += 1

    for item in report:
        print(item)

    files = {item.split(":", 1)[0] for item in report}
    print(f"\n共 {total} 处问题，涉及 {len(files)} 个文件。")
    if args.fix:
        print(f"已修复 {fixed_files} 个文件。")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
