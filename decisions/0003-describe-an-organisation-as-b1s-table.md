# 0003: Describe an organisation as B1's table, read by a program

**Decision:** An organisation is written in the shape organisation-description, B1's table of processes against the
problems of organizing with its roles defined once, and a program checks its columns and counts its empty cells.

**Status:** proposed, 2026-11-12. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- The first review ends on B1: one row per process, a column for each of the four problems of organizing, two for
  who decides and who controls, one for delegation ([baseline](../evidence/organisation-design/baseline.md)).
- Its next work, named there: a shape for one organisation's description, a check that counts empty cells, a fixture.
- The forward pass of 2026-11-12 added five sources ([protocol](../evidence/organisation-design/protocol.md), section 12);
  this record adds no column for them.
- The classification's categories are not read: its page refused an automated reader.
- The maintainer has not yet accepted B1; this record waits on that, and becomes accepted with it.

## Decision

- Write the shape [organisation-description](../shapes/organisation-description.md), with a fixture of a venture that
  personalises a product.
- Add the local check `organisation-description` and its tests; CI runs the tests.
- Keep the configured rows empty, PROVISIONAL, until the categories are read; the check then requires each one.
- Name a role in the cells, never a person, so the same table survives a change of people.

## Consequences

- An organisation's gaps are counted, not noticed: the fixture's first run reports its empty cells with B1's two
  measures.
- The ai-augmented-company work can read which rows a model could fill, by role, from one table.
- **Bad:** the rows are the fixture's own until the classification is read, so no description can yet be checked for
  completeness against it.
- **Bad:** dependencies, delays and a rule for changing the design are not in the table (baseline, What B1 lacks).
- **Bad:** proposed before the maintainer accepted B1; if B1 changes, this record is superseded, not edited.

## See also

[Decisions](README.md); [record 0002](0002-keep-the-name-and-name-the-baseline.md);
[baseline](../evidence/organisation-design/baseline.md).
