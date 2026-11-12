# Shape: organisation description

One organisation written as B1's table: one row per process, one column per problem of organizing, and the roles
that answer them defined once. Its reader is whoever must run the organisation or change it, and asks: for each thing
the company must do, who does it, for what reward, with what information, who decides and who controls? It is a page,
and a program reads it.

**Status:** accepted, 2026-11-12. It builds on B1, named by record 0002 and accepted by the maintainer
([record 0003](../decisions/0003-describe-an-organisation-as-b1s-table.md)).

## Skeleton

```markdown
# Organisation: <the venture, in a few words>

<One sentence: what the description is for, and its date.>

**Shape:** [organisation description](<path to shapes/organisation-description.md>)

## Processes

| Process | Tasks | Who | Reward | Information | Decides | Controls | Delegated |
|---|---|---|---|---|---|---|---|
| <a process category> | <its tasks> | <a role> | <how the role is rewarded> | <what it is told> | <a role> | <a role> | <yes, no, in part> |
| Hold assets as a legal person | ... | ... | ... | ... | ... | ... | ... |

## Roles

| Role | Purpose | Filled by |
|---|---|---|
| <a role> | <what it exists to achieve> | <a person, a contractor or a program> |

## Compared with the org chart

<The boxes and lines of the same venture's org chart, and what the table shows that the chart does not.>

## Limits

<What the description leaves out: dependencies between processes, delays, when the design should change.>
```

## Where each part comes from

| Part | Evidence | Grade |
|---|---|---|
| One row per process | a list of what a firm does: the activities of a value chain (Porter 1985), a process handbook (Malone 1999), a 24-item instrument built from the cross-industry classification, used with 66 small firms (Cragg 2007) | convention; measured, descriptive, for its use |
| The rows' names | the classification's 13 level-1 categories, read in its file before use ([baseline](../evidence/organisation-design/baseline.md), item 1) | convention; version 8.0 read in its file on 12 Nov. 2026, and listed in `rows` in checks/config.toml |
| The legal person, a row of its own | the firm holds assets apart from its owners (Hansmann 2000); a menu of legal forms, chosen (Guinnane 2007) | convention; measured, descriptive |
| Tasks, Who, Reward, Information | the four [universal problems of organizing](../evidence/organisation-design/frame.md) (Puranam 2014, pages 165-166, read in the original) | convention |
| Decides and Controls, apart | ownership and control are separated (Fama 1983, located only, title); B1 keeps deciding and controlling apart on that reading ([baseline](../evidence/organisation-design/baseline.md), item 4) | convention, from a title |
| Delegated | delegation follows the value of local adaptation (McElheran 2014); information and communication tools move it in opposite directions (Bloom 2014) | measured |
| A role apart from the person | practice writes a role with a purpose and its domains (HolacracyOne 2026 Constitution, an example of practice only) | convention |
| The org chart beside it | the practice B1 is compared with ([baseline](../evidence/organisation-design/baseline.md), item 6) | convention |
| Empty cells counted by a program | B1's two measures, coverage and completeness ([baseline](../evidence/organisation-design/baseline.md#how-it-is-measured)) | convention |

## Where the file goes

One organisation is one file, `organisations/<name>/organisation.md`; the check reads every file that matches
the files of the "organisation description" entry of `[shape_conformance]` in `checks/config.toml`, which also lists
the worked example's folder.

## Worked example

- A fixture with no real venture: [a-venture-that-personalises-a-product/organisation.md](examples/a-venture-that-personalises-a-product/organisation.md).

## The rules

1. The Processes table has the eight columns in the order of the skeleton.
2. One row holds the legal person, and its Process name contains the words "legal person".
3. Who, Decides and Controls name roles from the Roles table, never a person; each role appears once in that table, and
   the table has at least one role. Several roles in one cell are joined by a comma or "and"; a role whose name holds
   "and" is matched whole first.
4. Delegated is yes, no, in part, or left empty; case is not significant.
5. An empty cell is left blank or written `?` or `-`; a program counts it and reports the count as a warning, with
   coverage and completeness. A description with no empty cell gets no warning.

## The principles it applies

| Part | Principle |
|---|---|
| One table for the whole organisation | [signal the structure](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/page/signal-the-structure.md) |
| A role defined once, used by name | [one place per fact](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/collection/one-place-per-fact.md) |

## Checked by

`organisation-description` (exact): the eight columns, the legal row, roles defined and used by name, Delegated's
values, the configured rows; a warning gives the empty cells with coverage and completeness. Whether the rows are
complete, the answers true, and a role in the Roles table a role rather than a person's name is judgment.
