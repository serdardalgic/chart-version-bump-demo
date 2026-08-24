#!/usr/bin/env python3
"""Read/rewrite the `## Unreleased` section of CHANGELOG.md.

Subcommands:
  check-unreleased FILE
      Exit 0 if "## Unreleased" (exact heading) exists with at least one
      non-empty bullet under it, exit 1 otherwise (with a reason on stderr).

  finalize FILE --version X.Y.Z [--date DD.MM.YYYY]
      Rename "## Unreleased" to "## X.Y.Z (DATE)" and insert a fresh, empty
      "## Unreleased" heading above it.

  insert-entry FILE --version X.Y.Z --note TEXT [--date DD.MM.YYYY]
      Insert a new "## X.Y.Z (DATE)" entry (note text split into bullets)
      right after the existing "## Unreleased" section (left untouched), or
      after the intro paragraph if there is no "## Unreleased" section.
"""

import argparse
import datetime
import sys

UNRELEASED_HEADING = "## Unreleased\n"


def today() -> str:
    return datetime.date.today().strftime("%d.%m.%Y")


def find_unreleased(lines: list[str]) -> int | None:
    for i, line in enumerate(lines):
        if line.rstrip("\n") == "## Unreleased":
            return i
    return None


def find_section_end(lines: list[str], heading_index: int) -> int:
    for i in range(heading_index + 1, len(lines)):
        if lines[i].startswith("## "):
            return i
    return len(lines)


def has_bullet(lines: list[str], start: int, end: int) -> bool:
    for line in lines[start:end]:
        stripped = line.strip()
        if stripped.startswith("- ") and stripped[2:].strip():
            return True
    return False


def cmd_check_unreleased(args: argparse.Namespace) -> int:
    with open(args.file, encoding="utf-8") as f:
        lines = f.readlines()

    heading_index = find_unreleased(lines)
    if heading_index is None:
        print("## Unreleased heading not found (must be exactly `## Unreleased`)", file=sys.stderr)
        return 1

    section_end = find_section_end(lines, heading_index)
    if not has_bullet(lines, heading_index + 1, section_end):
        print("## Unreleased has no non-empty bullets", file=sys.stderr)
        return 1

    print("## Unreleased has at least one non-empty bullet")
    return 0


def cmd_finalize(args: argparse.Namespace) -> int:
    with open(args.file, encoding="utf-8") as f:
        lines = f.readlines()

    heading_index = find_unreleased(lines)
    if heading_index is None:
        print("## Unreleased heading not found", file=sys.stderr)
        return 1

    section_end = find_section_end(lines, heading_index)
    if not has_bullet(lines, heading_index + 1, section_end):
        print("## Unreleased has no non-empty bullets", file=sys.stderr)
        return 1

    date = args.date or today()
    content = lines[heading_index + 1 : section_end]
    finalized_section = [f"## {args.version} ({date})\n"] + content
    fresh_unreleased = [UNRELEASED_HEADING, "\n"]

    new_lines = lines[:heading_index] + fresh_unreleased + finalized_section + lines[section_end:]

    with open(args.file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return 0


def cmd_insert_entry(args: argparse.Namespace) -> int:
    with open(args.file, encoding="utf-8") as f:
        lines = f.readlines()

    date = args.date or today()
    bullets = []
    for raw_line in args.note.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        if not stripped.startswith("-"):
            stripped = f"- {stripped}"
        bullets.append(f"{stripped}\n")

    if not bullets:
        print("--note produced no bullets", file=sys.stderr)
        return 1

    entry_lines = [f"## {args.version} ({date})\n", "\n"] + bullets + ["\n"]

    heading_index = find_unreleased(lines)
    if heading_index is not None:
        insert_at = find_section_end(lines, heading_index)
    else:
        insert_at = next((i for i, line in enumerate(lines) if line.startswith("## ")), len(lines))

    new_lines = lines[:insert_at] + entry_lines + lines[insert_at:]

    with open(args.file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_check = subparsers.add_parser("check-unreleased")
    p_check.add_argument("file")
    p_check.set_defaults(func=cmd_check_unreleased)

    p_finalize = subparsers.add_parser("finalize")
    p_finalize.add_argument("file")
    p_finalize.add_argument("--version", required=True)
    p_finalize.add_argument("--date")
    p_finalize.set_defaults(func=cmd_finalize)

    p_insert = subparsers.add_parser("insert-entry")
    p_insert.add_argument("file")
    p_insert.add_argument("--version", required=True)
    p_insert.add_argument("--note", required=True)
    p_insert.add_argument("--date")
    p_insert.set_defaults(func=cmd_insert_entry)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
