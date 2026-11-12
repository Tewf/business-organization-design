"""Organisation description: one row per process, one column per problem of organizing, each role defined once.

A file matched by the files of the "organisation description" entry of `[shape_conformance] shapes` in
checks/config.toml (or `[organisation_description] files`, when set) must hold:
- one `Processes` section, holding one table, whose header is, in this order: Process, Tasks, Who, Reward, Information,
  Decides, Controls, Delegated (B1 of evidence/organisation-design/baseline.md);
- one row whose Process names the legal person (Hansmann 2000), since a process list may not hold it;
- one `Roles` section, holding one table, whose first column is Role, at least one role, each once: a role is defined apart from
  the person who fills it;
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
JOIN = re.compile(r"\s*(?:,|\band\b)\s*", re.IGNORECASE)


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


def extra(found: dict) -> list[tuple[int, str]]:
    """The (line, message) of a second Processes or Roles section, and of a second table inside one: a second table
    would hold rows the check never reads."""
    problems = []
    for name in ("processes", "roles"):
        titles = [t for t in found if t.startswith(name)]
        for title in titles[1:]:
            problems.append((found[title][0], f"a second {name.capitalize()} section, {title!r}: one per description"))
        if titles:
            tables, inside = 0, False
            for number, line in found[titles[0]][1]:
                if line.strip().startswith("|"):
                    if not inside:
                        tables += 1
                        if tables == 2:
                            problems.append((number, f"a second table in the {name.capitalize()} section: keep one, put notes in another section"))
                    inside = True
                else:
                    inside = False
    return problems


def section(found: dict, name: str):
    """The (line, body) of the first heading starting with name, or None."""
    for title, value in found.items():
        if title.startswith(name):
            return value
    return None


def table(body: list[tuple[int, str]]) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """The first Markdown table of a section: its lowercase header and its (line, cells) rows."""
    lines, started = [], False
    for n, l in body:
        if l.strip().startswith("|"):
            lines.append((n, l.strip()))
            started = True
        elif started:
            break
    if len(lines) < 2:
        return [], []
    split = lambda l: [c.strip() for c in l.strip("|").split("|")]
    header = [c.lower() for c in split(lines[0][1])]
    rows = [(n, split(l)) for n, l in lines[2:]]
    return header, rows


def role_names_in(cell: str, roles: set[str]) -> list[str]:
    """The role names a cell holds, read from the left: the longest defined role the rest starts with, else the text up
    to the next comma or "and"; so a role whose name holds "and" is matched whole, alone or beside others."""
    names, rest = [], cell.strip()
    ordered = sorted(roles, key=len, reverse=True)
    while True:
        rest = re.sub(r"^(?:\s|,|\band\b)+", "", rest, flags=re.IGNORECASE)
        if not rest:
            return names
        low = rest.lower()
        match = next((r for r in ordered if low.startswith(r) and (len(low) == len(r) or not low[len(r)].isalnum())), None)
        if match:
            names.append(rest[:len(match)])
            rest = rest[len(match):]
        else:
            part = JOIN.split(rest, maxsplit=1)
            names.append(part[0].strip())
            rest = part[1] if len(part) > 1 else ""


def check(root: Path, config: dict) -> list[Finding]:
    """Errors for a missing column, row or role; one warning per file with its empty cells counted."""
    settings = config.get("organisation_description", {})
    patterns, required_rows = settings.get("files"), settings.get("rows", [])
    if patterns is None:
        shapes = config.get("shape_conformance", {}).get("shapes", [])
        patterns = next((s.get("files", []) for s in shapes if s.get("name") == "organisation description"), [])
    findings: list[Finding] = []
    for path in files_in_scope(root, config, {".md"}):
        if not any(fnmatch.fnmatch(path, pattern) for pattern in patterns):
            continue
        found = sections((root / path).read_text(encoding="utf-8", errors="replace"))

        def fail(line: int, message: str, kind: str = "error") -> None:
            findings.append(Finding(NAME, path, line, message, kind))

        for line, message in extra(found):
            fail(line, message)
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
            seen: set[str] = set()
            for line, cells in role_rows:
                name = cells[0].lower() if cells else ""
                if name in seen:
                    fail(line, f"the role {cells[0]!r} is defined twice in the Roles table")
                elif name:
                    seen.add(name)
            role_names = seen
            if not role_names:
                fail(roles[0], "the Roles table defines no role: name at least one")
        legal = [line for line, cells in rows if cells and LEGAL.search(cells[0])]
        if not legal:
            fail(processes[0], "no row for the legal person: the firm holding assets apart from its owners (Hansmann 2000)")
        for line in legal[1:]:
            fail(line, "a second row for the legal person: one row holds it")
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
                if value in EMPTY or roles is None:
                    continue
                for name in role_names_in(value, role_names):
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
