"""Contract checks for the optional practice skill and skill checkout portability."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("project_learning_self_check", ROOT / "scripts" / "self_check.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load self_check")
self_check = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = self_check
SPEC.loader.exec_module(self_check)


class SkillStructureTests(unittest.TestCase):
    def test_skill_structure_is_valid_independent_of_checkout_folder(self):
        self.assertEqual(self_check.structural_errors(), [])
        with tempfile.TemporaryDirectory(prefix="arbitrary-checkout-") as directory:
            checkout = Path(directory) / "different-folder-name"
            shutil.copytree(
                ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache")
            )
            with mock.patch.object(self_check, "SKILL_ROOT", checkout):
                self.assertEqual(self_check.structural_errors(), [])

    def test_missing_guided_practice_cannot_hide_behind_total_skill_count(self):
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "checkout"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            (checkout / "extensions" / "guided-practice" / "SKILL.md").unlink()
            unexpected = checkout / "extensions" / "unrelated" / "SKILL.md"
            unexpected.parent.mkdir(parents=True)
            unexpected.write_text("\n".join(["---", "name: unrelated", "description: test", "---", ""]), encoding="utf-8")
            with mock.patch.object(self_check, "SKILL_ROOT", checkout):
                issues = self_check.structural_errors()
            self.assertIn("missing SKILL.md: extensions/guided-practice/SKILL.md", issues)
            self.assertIn("unexpected SKILL.md: extensions/unrelated/SKILL.md", issues)
            self.assertFalse(any("missing YAML frontmatter" in issue for issue in issues), issues)

    def test_all_eight_core_skill_names_remain_present(self):
        for i, name in enumerate(
            (
                "repo-discovery", "config-and-installation", "architecture-analysis",
                "code-flow-analysis", "concept-extraction", "tutorial-writer",
                "example-generator", "learning-review",
            ), start=1
        ):
            self.assertTrue((ROOT / f"{i:02d}-{name}" / "SKILL.md").is_file())

    def test_guided_practice_is_opt_in_and_preserves_ten_chapters(self):
        root = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        practice = (ROOT / "extensions" / "guided-practice" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("explicitly", root)
        self.assertIn("does **not** add a ninth core child skill", root)
        self.assertIn("Read-only by default", practice)
        self.assertIn("not a ninth core phase", practice)
        self.assertIn("ten stable chapter names", practice)


if __name__ == "__main__":
    unittest.main()
