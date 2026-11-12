"""Organisation description: one row per process, one column per problem of organizing, each role defined once.

A file matched by the files of the "organisation description" entry of `[shape_conformance] shapes` in
checks/config.toml (or `[organisation_description] files`, when set) must hold:
- the description read as GitHub renders it, by a GitHub-flavoured Markdown parser (markdown-it-py, CommonMark with
  tables), so that what the check reads is what a reader sees (issue #2, decided 12 Nov. 2026). A table in HTML, or a
  Processes or Roles table or heading inside a quote or a list, is refused: the check reads the top-level Markdown
  tables only. Cells are compared as they read: their rendered text, invisible characters dropped;
- one section whose title holds the word Processes (a subheading inside it belongs to it), holding one Markdown table
  and no other, one row per process, whose header is, in this order: Process, Tasks, Who, Reward, Information,
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
import unicodedata
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ImportError:  # the check then reports one error naming the package
    MarkdownIt = None

from framework.check_api import Finding, files_in_scope

NAME = "organisation-description"
EXACT = True

COLUMNS = ["process", "tasks", "who", "reward", "information", "decides", "controls", "delegated"]
MEASURED = ["tasks", "who", "reward", "information", "decides", "controls"]
ROLE_COLUMNS = ["who", "decides", "controls"]
EMPTY = {"", "?", "-"}
DELEGATED = {"yes", "no", "in part"}
LEGAL = re.compile(r"\blegal\s+person\b", re.IGNORECASE)
WORD = {"processes": re.compile(r"^processes$"), "roles": re.compile(r"^roles$")}
NUMBER = re.compile(r"^\d+(?:\.\d+)*\s+")
_DOC: dict = {}  # the whole file as the parser read it, set by sections() and used by table() and extra()
JOIN = re.compile(r"\s*(?:,|\band\b)\s*", re.IGNORECASE)


def plain(cell: str) -> str:
    """A rendered cell as it reads: invisible characters removed, spaces collapsed, lowercase. Names, empty markers and
    Delegated are compared so; the parser has already turned links, code, escapes and entities into their text."""
    text = "".join(ch for ch in cell if unicodedata.category(ch) != "Cf" and ch != "\u034f")
    return re.sub(r"\s+", " ", text).strip().lower()


def parsed(text: str) -> dict:
    """The blocks a reader sees, from the parser: headings and tables with their 1-based lines, whether each is at the
    top level (not inside a quote or a list), and the lines of HTML blocks that hold a table."""
    tokens = MarkdownIt("commonmark").enable(["table", "strikethrough"]).parse(text)
    out = {"headings": [], "tables": [], "html_tables": []}
    depth, i = 0, 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.type in ("blockquote_open", "bullet_list_open", "ordered_list_open"):
            depth += 1
        elif tok.type in ("blockquote_close", "bullet_list_close", "ordered_list_close"):
            depth -= 1
        elif tok.type == "inline" and any(c.type == "html_inline" and re.match(r"<table\b", c.content, re.I)
                                          for c in tok.children or []):
            out["html_tables"].append(tok.map[0] + 1)
        elif tok.type == "heading_open":
            out["headings"].append((tok.map[0] + 1, int(tok.tag[1]), inline_text(tokens[i + 1]).lower(), depth == 0))
        elif tok.type == "html_block" and re.search(r"<table\b", tok.content, re.I):
            out["html_tables"].append(tok.map[0] + 1)
        elif tok.type == "table_open":
            header, rows, row, line = [], [], None, tok.map[0] + 1
            j = i + 1
            while tokens[j].type != "table_close":
                t = tokens[j]
                if t.type == "tr_open":
                    row = (t.map[0] + 1, [])
                elif t.type == "inline" and row is not None:
                    row[1].append(inline_text(t))
                elif t.type == "tr_close":
                    if header:
                        rows.append(row)
                    else:
                        header.extend(row[1])
                    row = None
                j += 1
            out["tables"].append((line, header, rows, depth == 0))
            i = j
        i += 1
    return out


def inline_text(token) -> str:
    """The text a reader sees in an inline token: text and code as written, a break as a space; markup, inline HTML,
    struck text and images dropped, since a reader sees none of them as text."""
    parts, struck = [], 0
    for child in token.children or []:
        if child.type == "s_open":
            struck += 1
        elif child.type == "s_close":
            struck -= 1
        elif struck:
            continue
        elif child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
    return "".join(parts)


def unread(lines: list[str]) -> list[tuple[int, str]]:
    """The (line, message) of what a reader sees but the check does not read: a table in HTML, and a Processes or
    Roles heading or table inside a quote or a list. Everything else is read as GitHub renders it."""
    blocks = parsed("\n".join(lines))
    problems = [(n, "a table in HTML: the check reads Markdown tables; write it as one") for n in blocks["html_tables"]]
    for n, _, title, top in blocks["headings"]:
        if not top and (WORD["processes"].search(title) or WORD["roles"].search(title)):
            problems.append((n, f"a heading {title!r} inside a quote or a list: write it at the top level"))
    return problems


def sections(text: str) -> list[tuple[str, int, list[tuple[int, str]]]]:
    """Every top-level heading the parser reads as (lowercase title, line, body), its body running to the next heading
    of the same or a higher level, so a subheading's lines belong to the section above it too."""
    lines = text.splitlines()
    _DOC.clear()
    _DOC.update(parsed(text))
    heads = [(n, level, plain(title)) for n, level, title, top in _DOC["headings"] if top]
    found = []
    for i, (number, level, title) in enumerate(heads):
        end = next((n for n, lv, _ in heads[i + 1:] if lv <= level), len(lines) + 1)
        found.append((title, number, [(n, lines[n - 1]) for n in range(number + 1, end)]))
    return found


def extra(found: list) -> list[tuple[int, str]]:
    """The (line, message) of every way a description could hold rows the check does not read: a second Processes or
    Roles section, a Roles section nested in Processes, a second table inside one, or a table there inside a quote or a
    list."""
    problems = []
    spans = {}
    for name in ("processes", "roles"):
        titled = [(title, number, body) for title, number, body in found if WORD[name].search(title)]
        for title, number, _ in titled[1:]:
            problems.append((number, f"a second {name.capitalize()} section, {title!r}: one per description"))
        if titled:
            spans[name] = (titled[0][1], titled[0][2][-1][0] if titled[0][2] else titled[0][1])
    if "processes" in spans and "roles" in spans and spans["processes"][0] < spans["roles"][0] <= spans["processes"][1]:
        problems.append((spans["roles"][0], "the Roles section is nested under Processes: give it a heading of the same level"))
        return problems
    for line, header, _, at_top in _DOC.get("tables", []):
        if not at_top or any(start < line <= end for start, end in spans.values()):
            continue
        names = {plain(c) for c in header}
        title = next((t for t, n, _ in reversed(found) if n < line), "")
        if {"process", "who", "decides", "controls"} <= names:
            problems.append((line, f"a Processes table under the heading {title!r}: every row belongs in the one Processes table"))
        if {"role", "filled by"} <= names:
            problems.append((line, f"a Roles table under the heading {title!r}: every role is defined in the one Roles table"))
    for name in ("processes", "roles"):
        titled = [(title, number, body) for title, number, body in found if WORD[name].search(title)]
        if not titled:
            continue
        top = 0
        for line, _, _, at_top in tables_in(titled[0][2]):
            if not at_top:
                problems.append((line, f"a table inside a quote or a list in the {name.capitalize()} section: write it as the section's table"))
                continue
            top += 1
            if top == 2:
                problems.append((line, f"a second table in the {name.capitalize()} section: keep one, put notes in another section"))
    return problems

def section(found: list, name: str):
    """The (line, body) of the first heading whose title holds the word name, or None."""
    for title, number, body in found:
        if WORD[name].search(title):
            return number, body
    return None


def table(body: list[tuple[int, str]]) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """The section's first top-level table, from the whole file as the parser read it (so link definitions elsewhere
    count): its header and its rows, each cell's rendered text, with the rows' lines in the file."""
    for line, header, rows, top in tables_in(body):
        if top:
            return [plain(c) for c in header], rows
    return [], []


def tables_in(body: list[tuple[int, str]]) -> list:
    """The tables of the whole file whose first line falls inside the body's lines."""
    if not body:
        return []
    first, last = body[0][0], body[-1][0]
    return [t for t in _DOC.get("tables", []) if first <= t[0] <= last]

def role_names_in(cell: str, roles: set[str]) -> list[str]:
    """The role names a cell holds, read from the left: the longest defined role the rest starts with, else the text up
    to the next comma or "and"; so a role whose name holds "and" is matched whole, alone or beside others. Names are
    joined by a comma or "and" only: a role followed by more text with no joiner comes back with that text, and a
    cell ending on a joiner comes back with an empty name, so the caller reports both."""
    names, rest = [], plain(cell)
    ordered = sorted(roles, key=len, reverse=True)
    if re.search(r"(?:,|\band)\s*$", rest):
        names.append("")
    while True:
        rest = re.sub(r"^(?:\s|,|\band\b)+", "", rest, flags=re.IGNORECASE)
        if not rest:
            return names
        match = next((r for r in ordered if rest.startswith(r) and (len(rest) == len(r) or not rest[len(r)].isalnum())), None)
        if match and re.match(r"^\s*(?:,|\band\b|$)", rest[len(match):]):
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
    if MarkdownIt is None:
        return [Finding(NAME, "checks/local/organisation_description.py", 1,
                        "markdown-it-py is not installed: pip install markdown-it-py (the check reads Markdown with it)")]
    for path in files_in_scope(root, config, {".md"}):
        if not any(fnmatch.fnmatch(path, pattern) for pattern in patterns):
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        found = sections(text)

        def fail(line: int, message: str, kind: str = "error") -> None:
            findings.append(Finding(NAME, path, line, message, kind))

        for line, message in unread(text.splitlines()) + extra(found):
            fail(line, message)
        processes, roles = section(found, "processes"), section(found, "roles")
        if processes is None:
            fail(1, "no Processes section: one row per process, one column per problem (B1)")
            continue
        header, rows = table(processes[1])
        header = [plain(c) for c in header]
        if header != COLUMNS:
            fail(processes[0], "the Processes table's header is not: " + ", ".join(c.capitalize() for c in COLUMNS))
            continue
        role_names: set[str] = set()
        if roles is None:
            fail(1, "no Roles section: define each role once, apart from the person who fills it")
        else:
            role_header, role_rows = table(roles[1])
            if not role_header or plain(role_header[0]) != "role":
                fail(roles[0], "the Roles table's first column is not Role")
            seen: set[str] = set()
            for line, cells in role_rows:
                name = plain(cells[0]) if cells else ""
                if name in seen:
                    fail(line, f"the role {cells[0]!r} is defined twice in the Roles table")
                elif name and name not in EMPTY:
                    seen.add(name)
            role_names = seen
            if not role_names:
                fail(roles[0], "the Roles table defines no role: name at least one")
        legal = [line for line, cells in rows if cells and LEGAL.search(plain(cells[0]))]
        if not legal:
            fail(processes[0], "no row for the legal person: the firm holding assets apart from its owners (Hansmann 2000)")
        for line in legal[1:]:
            fail(line, "a second row for the legal person: one row holds it")
        seen_rows: set[str] = set()
        for line, cells in rows:
            if cells and plain(cells[0]) in EMPTY:
                fail(line, "a row with no process named: name the process, or drop the row")
                continue
            if cells and plain(cells[0]) in seen_rows:
                fail(line, f"a second row for the process {cells[0]!r}: one row per process")
            elif cells:
                seen_rows.add(plain(cells[0]))
        names = {NUMBER.sub("", plain(cells[0])) for _, cells in rows if cells}
        for wanted in required_rows:
            if plain(wanted) not in names:
                fail(processes[0], f"no row for the configured process {wanted!r}")
        filled = total = with_who = 0
        for number, cells in rows:
            if len(cells) != len(COLUMNS):
                fail(number, f"a row of {len(cells)} cells where the header has {len(COLUMNS)}")
                continue
            cell = dict(zip(COLUMNS, cells))
            for column in ROLE_COLUMNS:
                value = cell[column]
                if plain(value) in EMPTY or roles is None:
                    continue
                names = role_names_in(value, role_names)
                if not names:
                    fail(number, f"{column.capitalize()} holds {value!r}, which names no role: write a role, or leave it empty")
                for name in names:
                    if not name:
                        fail(number, f"{column.capitalize()} holds {value!r}, which ends on a comma or \"and\"")
                    elif name not in role_names:
                        fail(number, f"{column.capitalize()} names {name!r}, which the Roles table does not define")
            if plain(cell["delegated"]) not in DELEGATED | EMPTY:
                fail(number, "Delegated is not yes, no, in part or empty")
            total += len(MEASURED)
            filled += sum(plain(cell[c]) not in EMPTY for c in MEASURED)
            with_who += plain(cell["who"]) not in EMPTY
        if rows and total:
            coverage, completeness = with_who / len(rows), filled / total
            if filled < total:
                fail(processes[0], f"{total - filled} empty cells of {total}: coverage {coverage:.2f}, "
                     f"completeness {completeness:.2f} (B1's two measures)", "warning")
    return findings
