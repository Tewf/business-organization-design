"""Tests of checks/local/organisation_description.py: it fails a description that breaks B1's table and counts empties.

Run: python3 -m unittest discover -s checks
The standard's checks/ folder must be importable: set READER_ERGONOMICS_CHECKS to it, or extract the release in
checks/out/standard (AGENTS.md).
"""
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
CANDIDATES = [os.environ.get("READER_ERGONOMICS_CHECKS", ""), REPOSITORY / "checks" / "out" / "standard" / "checks",
              REPOSITORY.parent / "standard" / "checks", REPOSITORY.parent / "reader-ergonomics" / "checks"]
sys.path.insert(0, str(next(Path(c) for c in CANDIDATES if c and (Path(c) / "framework").is_dir())))
spec = importlib.util.spec_from_file_location("organisation_description",
                                              REPOSITORY / "checks" / "local" / "organisation_description.py")
description = importlib.util.module_from_spec(spec)
spec.loader.exec_module(description)

CONFIG = {"organisation_description": {"files": ["orgs/*.md"], "rows": []}}
GOOD = """# Organisation

## Processes

| Process | Tasks | Who | Reward | Information | Decides | Controls | Delegated |
|---|---|---|---|---|---|---|---|
| Make the product | cut, assemble | maker | salary | orders | maker | founder | yes |
| Hold assets as a legal person | sign, own | founder | equity | accounts | founder | founder and maker | no |

## Roles

| Role | Purpose | Filled by |
|---|---|---|
| founder | the venture exists | one person |
| maker | the product is made | one person |
"""


def run(text: str, config: dict = CONFIG) -> list:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        (root / "orgs").mkdir()
        (root / "orgs" / "a.md").write_text(text, encoding="utf-8")
        return description.check(root, config)


def errors(findings: list) -> list:
    return [f for f in findings if f.kind == "error"]


class OrganisationDescriptionTest(unittest.TestCase):
    def test_complete_description_passes(self):
        self.assertEqual(run(GOOD), [])

    def test_missing_column_fails(self):
        self.assertTrue(errors(run(GOOD.replace("| Reward ", "| Pay "))))

    def test_missing_legal_row_fails(self):
        self.assertTrue(errors(run(GOOD.replace("Hold assets as a legal person", "Own things"))))

    def test_undefined_role_fails(self):
        self.assertTrue(errors(run(GOOD.replace("| founder and maker |", "| founder and Alice |"))))

    def test_bad_delegated_fails(self):
        self.assertTrue(errors(run(GOOD.replace("| yes |", "| maybe |"))))

    def test_empty_cells_are_counted_not_failed(self):
        findings = run(GOOD.replace("| cut, assemble |", "| ? |"))
        self.assertEqual(errors(findings), [])
        self.assertIn("1 empty cells of 12", findings[0].message)

    def test_configured_row_is_required(self):
        config = {"organisation_description": {"files": ["orgs/*.md"], "rows": ["Sell the product"]}}
        self.assertTrue(errors(run(GOOD, config)))

    def test_missing_roles_section_fails(self):
        self.assertTrue(errors(run(GOOD.split("## Roles")[0])))


if __name__ == "__main__":
    unittest.main()
