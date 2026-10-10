"""Contract checks for the optional practice skill and skill checkout portability."""

from __future__ import annotations

import importlib.util
import sys
import unittest
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
