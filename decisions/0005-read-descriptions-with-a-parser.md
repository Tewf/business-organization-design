# 0005: Read an organisation description with a Markdown parser

**Decision:** The check `organisation-description` reads a description with markdown-it-py (CommonMark with GitHub's
tables and strikethrough), instead of regular expressions.

**Status:** accepted, 2026-11-12. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- Six review passes on 12 Nov. 2026 each found Markdown that GitHub renders one way and the patterns read another:
  a table without its leading pipes, a setext heading, an escaped pipe, an entity, emphasis in a name.
- Each was closed by refusing the form (the shape's rule 6, the plain form), and the sixth pass still found five
  new ones, so the approach did not converge ([issue #2](https://github.com/Tewf/business-organization-design/issues/2)).
- The maintainer was asked on a decision page and chose a parser (12 Nov. 2026).

## Decision

- The check reads headings and tables from markdown-it-py 4.2.0, CommonMark with GitHub's tables and strikethrough,
  parsing the whole file once. A cell is its
  rendered text: a link, code, an escape or an entity counts as what it shows.
- It still refuses what a reader sees but it does not read: a table in HTML, and a Processes or Roles heading or
  table inside a quote or a list.
- Rule 6 of the shape says so; the plain form is no longer asked.

## Options not taken

- Keep the patterns and the plain form: no dependency, but every pass found another form.
- Another parser (mistune, the GitHub API): mistune's tables differ from GitHub's in edge cases, and the API needs a
  network call on every run.

## Consequences

- The program tier has its first dependency: CI installs markdown-it-py, and a local run needs it in its environment;
  without it the check reports one error naming the package.
- Forms the patterns refused are now read as GitHub shows them. 14 tests were rewritten to the parser's reading
  and one added. A pass the same day added nine more, for what the parser first missed: inline HTML, link
  definitions, empty roles, format characters.
- **Bad:** the check is as right as markdown-it-py's tables are close to GitHub's.

## See also

[Decisions](./); [issue #2](https://github.com/Tewf/business-organization-design/issues/2); [the shape](../shapes/organisation-description.md).
