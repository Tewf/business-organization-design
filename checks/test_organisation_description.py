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
        self.assertTrue(any("'alice'" in f.message for f in errors(run(GOOD.replace("| founder and maker |", "| founder and Alice |")))))

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

    def test_a_second_table_in_processes_fails(self):
        text = GOOD.replace("\n## Roles", "\nNotes:\n\n| Note | Text |\n|---|---|\n| a | b |\n\n## Roles")
        self.assertTrue(any("second table" in f.message for f in errors(run(text))))

    def test_a_second_processes_section_fails(self):
        text = GOOD + "\n## Processes: finance\n\n| Process | Tasks |\n|---|---|\n| Pay | pay |\n"
        self.assertTrue(any("second Processes section" in f.message for f in errors(run(text))))

    def test_a_second_legal_row_fails(self):
        row = "| Hold assets as a legal person | sign, own | founder | equity | accounts | founder | founder and maker | no |"
        self.assertTrue(any("second row for the legal person" in f.message for f in errors(run(GOOD.replace(row, row + "\n" + row)))))

    def test_a_repeated_processes_title_fails(self):
        text = GOOD + "\n## Processes\n\n| Process | Tasks |\n|---|---|\n| a | b |\n"
        self.assertTrue(any("second Processes section" in f.message for f in errors(run(text))))

    def test_a_table_under_a_subheading_of_processes_fails(self):
        text = GOOD.replace("\n## Roles", "\n### Finance\n\n| Process | Tasks |\n|---|---|\n| Pay | pay |\n\n## Roles")
        self.assertTrue(any("second table" in f.message for f in errors(run(text))))

    def test_a_table_without_leading_pipes_is_a_second_table(self):
        text = GOOD.replace("\n## Roles", "\nNote | Text\n--- | ---\na | b\n\n## Roles")
        self.assertTrue(any("second table" in f.message for f in errors(run(text))))

    def test_an_html_table_fails(self):
        text = GOOD.replace("\n## Roles", "\n<table><tr><td>Pay</td></tr></table>\n\n## Roles")
        self.assertTrue(any("HTML" in f.message for f in errors(run(text))))

    def test_a_role_cell_naming_no_role_fails(self):
        self.assertTrue(any(("names no role" in f.message or "ends on a comma" in f.message) for f in errors(run(GOOD.replace("| maker | salary |", "| and | salary |")))))

    def test_illegal_is_not_legal(self):
        text = GOOD.replace("Hold assets as a legal person", "Screen out illegal personnel")
        self.assertTrue(any("no row for the legal person" in f.message for f in errors(run(text))))

    def test_a_fenced_description_is_code_and_holds_no_processes(self):
        self.assertTrue(any("no Processes section" in f.message for f in errors(run("```text\n" + GOOD + "\n```\n"))))

    def test_an_html_comment_is_not_read_as_a_reader_does_not_see_it(self):
        text = GOOD.replace("\n## Roles", "\n<!--\n## Processes again\n-->\n\n## Roles")
        self.assertEqual(errors(run(text)), [])

    def test_a_setext_heading_is_a_heading(self):
        self.assertTrue(any("second Processes section" in f.message for f in errors(run(GOOD + "\nProcesses\n---------\n"))))

    def test_a_short_delimiter_second_table_fails(self):
        text = GOOD.replace("\n## Roles", "\n| Note | Text |\n|-|-|\n| a | b |\n\n## Roles")
        self.assertTrue(any("second table" in f.message for f in errors(run(text))))

    def test_a_delimiter_that_does_not_match_the_header_makes_no_table(self):
        text = GOOD.replace("|---|---|---|---|---|---|---|---|", "|---|---|", 1)
        self.assertTrue(any("header is not" in f.message for f in errors(run(text))))

    def test_another_section_holding_the_word_processes_fails(self):
        text = GOOD + "\n## Other processes\n\nNone.\n"
        self.assertTrue(any("second Processes section" in f.message for f in errors(run(text))))

    def test_a_repeated_process_row_fails(self):
        row = "| Make the product | cut, assemble | maker | salary | orders | maker | founder | yes |"
        self.assertTrue(any("second row for the process" in f.message for f in errors(run(GOOD.replace(row, row + "\n" + row)))))

    def test_a_row_without_its_leading_pipe_is_read_as_a_row(self):
        row = "| Hold assets as a legal person | sign, own | founder | equity | accounts | founder | founder and maker | no |"
        text = GOOD.replace(row, row + "\nPay | pay | maker | none | x | maker | founder | no |")
        config = {"organisation_description": {"files": ["orgs/*.md"], "rows": ["Pay"]}}
        self.assertEqual(errors(run(text, config)), [])

    def test_a_heading_indented_by_three_spaces_is_a_heading(self):
        self.assertTrue(any("second Processes section" in f.message for f in errors(run(GOOD + "\n   ## Processes\n"))))

    def test_a_processes_heading_in_a_quote_fails(self):
        self.assertTrue(any("inside a quote or a list" in f.message for f in errors(run(GOOD + "\n> ## Processes\n"))))

    def test_a_pipe_line_above_a_dash_line_is_a_heading(self):
        self.assertTrue(any("second Processes section" in f.message for f in errors(run(GOOD + "\nProcesses | more\n---\n"))))

    def test_bold_names_are_the_same_names(self):
        text = GOOD.replace("| maker | the product is made | one person |", "| maker | the product is made | one person |\n| *maker* | again | one person |")
        self.assertTrue(any("defined twice" in f.message for f in errors(run(text))))

    def test_an_html_table_in_a_section_fails(self):
        text = GOOD.replace("\n## Roles", "\n<table><tr><td>Pay</td></tr></table>\n\n## Roles")
        self.assertTrue(any("HTML" in f.message for f in errors(run(text))))

    def test_two_spaces_in_legal_person_count(self):
        row = "| Hold assets as a legal person | sign, own | founder | equity | accounts | founder | founder and maker | no |"
        self.assertTrue(any("second row for the legal person" in f.message for f in errors(run(GOOD.replace(row, row + "\n" + row.replace("legal person", "legal  person"))))))

    def test_an_entity_reads_as_its_character(self):
        findings = run(GOOD.replace("| cut, assemble |", "| &nbsp; |"))
        self.assertEqual(errors(findings), [])
        self.assertIn("1 empty cells of 12", findings[0].message)

    def test_an_indented_table_is_code_and_not_read(self):
        text = GOOD.replace("\n## Roles", "\n    | a | b |\n    |---|---|\n\n## Roles")
        self.assertEqual(errors(run(text)), [])

    def test_roles_joined_by_a_space_fail(self):
        self.assertTrue(any("does not define" in f.message for f in errors(run(GOOD.replace("| founder and maker | no |", "| founder maker | no |")))))

    def test_a_cell_ending_on_and_fails(self):
        self.assertTrue(any("ends on a comma" in f.message for f in errors(run(GOOD.replace("| founder and maker | no |", "| founder and | no |")))))

    def test_links_and_code_in_cells_are_read_as_their_text(self):
        self.assertEqual(errors(run(GOOD.replace("| equity | accounts |", "| equity, [record](x.md) | `accounts` |"))), [])

    def test_a_prose_line_glued_under_the_table_is_a_row(self):
        text = GOOD.replace("\n\n## Roles", "\nA note under the table\n\n## Roles")
        processes = next(body for title, _, body in description.sections(text) if "processes" in title)
        self.assertEqual(description.table(processes)[1][-1][1][0], "A note under the table")

    def test_an_escaped_pipe_stays_in_its_cell(self):
        self.assertEqual(errors(run(GOOD.replace("| cut, assemble |", "| cut \\| assemble |"))), [])

    def test_a_legal_person_only_in_a_link_title_is_not_the_legal_row(self):
        text = GOOD.replace("| Hold assets as a legal person |", '| [Own things](x.md "legal person") |')
        self.assertTrue(any("no row for the legal person" in f.message for f in errors(run(text))))

    def test_markers_in_code_count_as_empty(self):
        findings = run(GOOD.replace("| cut, assemble |", "| `?` |"))
        self.assertIn("1 empty cells of 12", findings[0].message)

    def test_an_escape_reads_as_github_shows_it(self):
        text = GOOD.replace("| maker | the product is made | one person |", "| maker | the product is made | one person |\n| \\*maker\\* | again | one person |")
        self.assertFalse(any("defined twice" in f.message for f in errors(run(text))))

    def test_code_in_delegated_is_read_as_its_text(self):
        self.assertEqual(errors(run(GOOD.replace("| maker | founder | yes |", "| maker | founder | `yes` |"))), [])

    def test_an_invisible_character_glues_the_words_as_a_reader_sees_them(self):
        self.assertTrue(any("no row for the legal person" in f.message for f in errors(run(GOOD.replace("legal person", "legal\u200bperson")))))

    def test_coverage_and_completeness_are_reported(self):
        findings = run(GOOD.replace("| maker | salary |", "| ? | salary |"))
        self.assertIn("coverage 0.50, completeness 0.92", findings[0].message)

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
