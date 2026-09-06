#!/usr/bin/env python3
"""Run self-contained structural and unit checks for this skill tree."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
NAME_RE = re.compile(r"(?m)^name:\s*([a-z0-9-]+)\s*$")
LOCAL_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)")


def structural_errors() -> list[str]:
    errors: list[str] = []
    skill_files = sorted(SKILL_ROOT.rglob("SKILL.md"))
    if len(skill_files) != 9:
        errors.append(f"expected root plus eight child SKILL.md files, found {len(skill_files)}")

    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8-sig")
        frontmatter = FRONTMATTER_RE.match(text)
        if not frontmatter:
            errors.append(f"missing YAML frontmatter: {skill_file.relative_to(SKILL_ROOT)}")
            continue
        name_match = NAME_RE.search(frontmatter.group(1))
        expected_name = SKILL_ROOT.name if skill_file.parent == SKILL_ROOT else skill_file.parent.name
        if not name_match or name_match.group(1) != expected_name:
            actual = name_match.group(1) if name_match else None
            errors.append(f"skill name mismatch in {skill_file}: {actual!r} != {expected_name!r}")

        for target in LOCAL_LINK_RE.findall(text):
            clean_target = target.split("#", 1)[0]
            if clean_target and not (skill_file.parent / clean_target).resolve().exists():
                errors.append(f"broken local link in {skill_file}: {target}")

    return errors


def main() -> int:
    errors = structural_errors()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(SKILL_ROOT / "scripts" / "tests"), "-v"],
        check=False,
    )
    if result.returncode:
        return result.returncode
    print("Skill structure and tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
