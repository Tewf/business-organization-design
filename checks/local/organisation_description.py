"""Organisation description: one row per process, one column per problem of organizing, each role defined once.

A file matched by `[organisation_description] files` of checks/config.toml must hold:
- a `Processes` section with a table whose header is, in this order: Process, Tasks, Who, Reward, Information,
  Decides, Controls, Delegated (B1 of evidence/organisation-design/baseline.md);
- a row whose Process names the legal person (Hansmann 2000), since a process list may not hold it;
- a `Roles` section with a table whose first column is Role: a role is defined apart from the person who fills it;
- in Who, Decides and Controls, only roles from that table (several joined by "and" or a comma), or an empty cell;
- in Delegated, yes, no, in part or an empty cell.
An empty cell is blank, "?" or "-". When `rows` in the config is not empty, each of its names must be a Process row.

The empty cells are counted, not forbidden: the file gets one warning with its coverage (the share of rows with a Who)
and its completeness (the share of the six cells Tasks to Controls that are filled), the two measures of B1.

A run with no error guarantees: every description has B1's columns, the legal row, roles defined once and used by name.
It does not guarantee the rows are complete or the answers true (judgment). Time O(text).
"""
from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from framework.check_api import Finding, files_in_scope

NAME = "organisation-description"
EXACT = True

COLUMNS = ["process", "tasks", "who", "reward", "information", "decides", "controls", "delegated"]
MEASURED = ["tasks", "who", "reward", "information", "decides", "controls"]
ROLE_COLUMNS = ["who", "decides", "controls"]
EMPTY = {"", "?", "-"}
DELEGATED = {"yes", "no", "in part"}
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
LEGAL = re.compile(r"legal person", re.IGNORECASE)
JOIN = re.compile(r"\s*(?:,|\band\b)\s*")


def sections(text: str) -> dict[str, tuple[int, list[tuple[int, str]]]]:
    """Each heading's lowercase title mapped to its line number and its numbered body lines."""
    found: dict[str, tuple[int, list[tuple[int, str]]]] = {}
    current = None
    for number, line in enumerate(text.splitlines(), 1):
        match = HEADING.match(line)
        if match:
            current = match.group(1).lower()
            found[current] = (number, [])
        elif current:
            found[current][1].append((number, line))
    return found


def section(found: dict, name: str):
    """The (line, body) of the first heading starting with name, or None."""
    for title, value in found.items():
        if title.startswith(name):
            return value
    return None


def table(body: list[tuple[int, str]]) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """The first Markdown table of a section: its lowercase header and its (line, cells) rows."""
    lines = [(n, l.strip()) for n, l in body if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    split = lambda l: [c.strip() for c in l.strip("|").split("|")]
    header = [c.lower() for c in split(lines[0][1])]
    rows = [(n, split(l)) for n, l in lines[2:]]
    return header, rows


def check(root: Path, config: dict) -> list[Finding]:
    """Errors for a missing column, row or role; one warning per file with its empty cells counted."""
    settings = config.get("organisation_description", {})
    patterns, required_rows = settings.get("files", []), settings.get("rows", [])
    findings: list[Finding] = []
    for path in files_in_scope(root, config, {".md"}):
        if not any(fnmatch.fnmatch(path, pattern) for pattern in patterns):
            continue
        found = sections((root / path).read_text(encoding="utf-8", errors="replace"))

        def fail(line: int, message: str, kind: str = "error") -> None:
            findings.append(Finding(NAME, path, line, message, kind))

        processes, roles = section(found, "processes"), section(found, "roles")
        if processes is None:
            fail(1, "no Processes section: one row per process, one column per problem (B1)")
            continue
        header, rows = table(processes[1])
        if header != COLUMNS:
            fail(processes[0], "the Processes table's header is not: " + ", ".join(c.capitalize() for c in COLUMNS))
            continue
        role_names: set[str] = set()
        if roles is None:
            fail(1, "no Roles section: define each role once, apart from the person who fills it")
        else:
            role_header, role_rows = table(roles[1])
            if not role_header or role_header[0] != "role":
                fail(roles[0], "the Roles table's first column is not Role")
            role_names = {cells[0].lower() for _, cells in role_rows if cells and cells[0]}
        if not any(LEGAL.search(cells[0]) for _, cells in rows if cells):
            fail(processes[0], "no row for the legal person: the firm holding assets apart from its owners (Hansmann 2000)")
        names = {cells[0].lower() for _, cells in rows if cells}
        for wanted in required_rows:
            if wanted.lower() not in names:
                fail(processes[0], f"no row for the configured process {wanted!r}")
        filled = total = with_who = 0
        for number, cells in rows:
            if len(cells) != len(COLUMNS):
                fail(number, f"a row of {len(cells)} cells where the header has {len(COLUMNS)}")
                continue
            cell = dict(zip(COLUMNS, cells))
            for column in ROLE_COLUMNS:
                value = cell[column]
                if value in EMPTY or not role_names:
                    continue
                for name in filter(None, JOIN.split(value)):
                    if name.lower() not in role_names:
                        fail(number, f"{column.capitalize()} names {name!r}, which the Roles table does not define")
            if cell["delegated"].lower() not in DELEGATED | EMPTY:
                fail(number, "Delegated is not yes, no, in part or empty")
            total += len(MEASURED)
            filled += sum(cell[c] not in EMPTY for c in MEASURED)
            with_who += cell["who"] not in EMPTY
        if rows and total:
            coverage, completeness = with_who / len(rows), filled / total
            if filled < total:
                fail(processes[0], f"{total - filled} empty cells of {total}: coverage {coverage:.2f}, "
                     f"completeness {completeness:.2f} (B1's two measures)", "warning")
    return findings
