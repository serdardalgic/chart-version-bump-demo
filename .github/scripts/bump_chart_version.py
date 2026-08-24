#!/usr/bin/env python3
"""Bump the `version:` field in a Helm Chart.yaml (semver patch/minor/major)."""

import argparse
import re
import sys

VERSION_LINE_RE = re.compile(r"^(version:\s*)(\d+)\.(\d+)\.(\d+)\s*$")


def bump(major: int, minor: int, patch: int, bump_type: str) -> tuple[int, int, int]:
    if bump_type == "major":
        return major + 1, 0, 0
    if bump_type == "minor":
        return major, minor + 1, 0
    if bump_type == "patch":
        return major, minor, patch + 1
    raise ValueError(f"unknown bump type: {bump_type}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chart_file", help="Path to Chart.yaml")
    parser.add_argument("--bump-type", required=True, choices=["patch", "minor", "major"])
    args = parser.parse_args()

    with open(args.chart_file, encoding="utf-8") as f:
        lines = f.readlines()

    new_version = None
    for i, line in enumerate(lines):
        m = VERSION_LINE_RE.match(line)
        if m:
            prefix, major, minor, patch = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            new_major, new_minor, new_patch = bump(major, minor, patch, args.bump_type)
            new_version = f"{new_major}.{new_minor}.{new_patch}"
            lines[i] = f"{prefix}{new_version}\n"
            break

    if new_version is None:
        print(f"error: no `version: X.Y.Z` line found in {args.chart_file}", file=sys.stderr)
        return 1

    with open(args.chart_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(new_version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
