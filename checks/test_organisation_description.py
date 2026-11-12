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
        self.assertTrue(any("header" in f.message for f in errors(run(GOOD.replace("| Reward ", "| Pay ")))))

    def test_missing_legal_row_fails(self):
        self.assertTrue(any("legal person" in f.message for f in errors(run(GOOD.replace("Hold assets as a legal person", "Own things")))))

    def test_undefined_role_fails(self):
        self.assertTrue(any("'Alice'" in f.message for f in errors(run(GOOD.replace("| founder and maker |", "| founder and Alice |")))))

    def test_bad_delegated_fails(self):
        self.assertTrue(any("Delegated" in f.message for f in errors(run(GOOD.replace("| yes |", "| maybe |")))))

    def test_empty_cells_are_counted_not_failed(self):
        findings = run(GOOD.replace("| cut, assemble |", "| ? |"))
        self.assertEqual(errors(findings), [])
        self.assertIn("1 empty cells of 12", findings[0].message)

    def test_configured_row_is_required(self):
        config = {"organisation_description": {"files": ["orgs/*.md"], "rows": ["Sell the product"]}}
        self.assertTrue(any("Sell the product" in f.message for f in errors(run(GOOD, config))))

    def test_missing_roles_section_fails(self):
        self.assertTrue(any("no Roles section" in f.message for f in errors(run(GOOD.split("## Roles")[0]))))

    def test_a_role_whose_name_holds_and_is_matched_whole(self):
        text = GOOD.replace("| maker | the product is made | one person |",
                            "| maker | the product is made | one person |\n| research and development | new recipes | one person |")
        text = text.replace("| cut, assemble | maker |", "| cut, assemble | research and development |")
        self.assertEqual(errors(run(text)), [])

    def test_a_role_holding_and_beside_another_role(self):
        text = GOOD.replace("| maker | the product is made | one person |",
                            "| maker | the product is made | one person |\n| research and development | new recipes | one person |")
        for cell in ("research and development, maker", "research and development and maker", "maker AND research and development"):
            self.assertEqual(errors(run(text.replace("| founder | founder and maker | no |", f"| founder | {cell} | no |"))), [], cell)

    def test_a_second_table_in_processes_is_not_read_as_rows(self):
        text = GOOD.replace("\n## Roles", "\nNotes:\n\n| Note | Text |\n|---|---|\n| a | b |\n\n## Roles")
        self.assertEqual(errors(run(text)), [])

    def test_a_role_defined_twice_fails(self):
        twice = GOOD.replace("| maker | the product is made | one person |",
                             "| maker | the product is made | one person |\n| maker | again | one person |")
        self.assertTrue(any("defined twice" in f.message for f in errors(run(twice))))

    def test_a_roles_table_with_no_role_fails_and_still_checks_names(self):
        empty = GOOD.replace("| founder | the venture exists | one person |\n| maker | the product is made | one person |\n", "")
        found = errors(run(empty))
        self.assertTrue(any("defines no role" in f.message for f in found))
        self.assertTrue(any("does not define" in f.message for f in found))

    def test_files_come_from_the_shape_conformance_entry(self):
        config = {"organisation_description": {"rows": []},
                  "shape_conformance": {"shapes": [{"name": "organisation description", "files": ["orgs/*.md"]}]}}
        self.assertEqual(run(GOOD, config), [])
        self.assertTrue(errors(run(GOOD.replace("Hold assets as a legal person", "Own things"), config)))


if __name__ == "__main__":
    unittest.main()
