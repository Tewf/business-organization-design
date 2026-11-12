"""Organisation description: one row per process, one column per problem of organizing, each role defined once.

A file matched by the files of the "organisation description" entry of `[shape_conformance] shapes` in
checks/config.toml (or `[organisation_description] files`, when set) must hold:
- one `Processes` section (a subheading inside it belongs to it), holding one Markdown table and no other, whose
  header is, in this order: Process, Tasks, Who, Reward, Information,
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
It does not guarantee the rows are complete or the answers true (judgment). Time O(text x roles), roles being
matched in each role cell.
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
LEGAL = re.compile(r"\blegal person\b", re.IGNORECASE)
SEPARATOR = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
JOIN = re.compile(r"\s*(?:,|\band\b)\s*", re.IGNORECASE)


def sections(text: str) -> list[tuple[str, int, list[tuple[int, str]]]]:
    """Every heading as (lowercase title, line, body), its body running to the next heading of the same or a higher
    level, so a subheading's lines belong to the section above it too."""
    lines = text.splitlines()
    heads = [(n, len(m.group(0)) - len(m.group(0).lstrip("#")), m.group(1).lower())
             for n, line in enumerate(lines, 1) if (m := HEADING.match(line))]
    found = []
    for i, (number, level, title) in enumerate(heads):
        end = next((n for n, lv, _ in heads[i + 1:] if lv <= level), len(lines) + 1)
        found.append((title, number, [(n, lines[n - 1]) for n in range(number + 1, end)]))
    return found


def extra(found: list) -> list[tuple[int, str]]:
    """The (line, message) of every way a description could hold rows the check does not read: a second Processes or
    Roles section (whatever its title says after the word), a second table inside one, a table written without its
    leading pipes, or an HTML table."""
    problems = []
    for name in ("processes", "roles"):
        titled = [(title, number, body) for title, number, body in found if title.startswith(name)]
        for title, number, _ in titled[1:]:
            problems.append((number, f"a second {name.capitalize()} section, {title!r}: one per description"))
        if not titled:
            continue
        tables = 0
        for number, line in titled[0][2]:
            if "<table" in line.lower():
                problems.append((number, f"an HTML table in the {name.capitalize()} section: write it as one Markdown table"))
            if SEPARATOR.match(line):
                tables += 1
                if not line.strip().startswith("|"):
                    problems.append((number, f"a table without its leading pipes in the {name.capitalize()} section: start each row with |"))
                if tables == 2:
                    problems.append((number, f"a second table in the {name.capitalize()} section: keep one, put notes in another section"))
    return problems


def section(found: list, name: str):
    """The (line, body) of the first heading starting with name, or None."""
    for title, number, body in found:
        if title.startswith(name):
            return number, body
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
                names = role_names_in(value, role_names)
                if not names:
                    fail(number, f"{column.capitalize()} holds {value!r}, which names no role: write a role, or leave it empty")
                for name in names:
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
