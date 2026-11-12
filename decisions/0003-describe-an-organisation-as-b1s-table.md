# 0003: Describe an organisation as B1's table, read by a program

**Decision:** An organisation is written in the shape organisation-description, B1's table of processes against the
problems of organizing with its roles defined once, and a program checks its columns and counts its empty cells.

**Status:** accepted, 2026-11-12, with B1 on [issue 1](https://github.com/Tewf/business-organization-design/issues/1). **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- The first review ends on B1: one row per process, a column for each of the four problems of organizing, two for
  who decides and who controls, one for delegation ([baseline](../evidence/organisation-design/baseline.md)).
- Its next work, named there: a shape for one organisation's description, a check that counts empty cells, a fixture.
- The forward pass of 2026-11-12 added five sources ([protocol](../evidence/organisation-design/protocol.md), section 12);
  this record adds no column for them.
- The classification's 13 categories were read in its file, version 8.0, on 12 Nov. 2026, after its page refused an
  automated reader.
- Record 0002 names B1, which the maintainer accepted as the baseline further work builds on ([issue 1](https://github.com/Tewf/business-organization-design/issues/1)).

## Decision

- Write the shape [organisation-description](../shapes/organisation-description.md), with a fixture of a venture that
  personalises a product.
- Add the local check `organisation-description` and its tests; CI runs the tests.
- The configured rows are the 13 categories; the check requires each one, and the legal person beside them.
- Name a role in the cells, never a person, so the same table survives a change of people. The check reads that the
  names are roles of the table; whether a role is a person's name is judgment.

## Consequences

- An organisation's gaps are counted, not noticed: the fixture's first run reports its empty cells with B1's two
  measures.
- **Bad:** the rows are a practice list, not a tested one: a description complete against it may still miss a process
  (baseline, What B1 lacks).
- **Bad:** dependencies, delays and a rule for changing the design are not in the table (baseline, What B1 lacks).
- **Bad:** if B1 changes, this record is superseded, not edited.

## See also

[Decisions](./); [record 0002](0002-keep-the-name-and-name-the-baseline.md);
[baseline](../evidence/organisation-design/baseline.md).
