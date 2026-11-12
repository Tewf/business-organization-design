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
| <a role> | <what it exists to achieve> | <a person, a contractor, an agent or a program> |

## Compared with the org chart

<The boxes and lines of the same venture's org chart, and what the table shows that the chart does not.>

## Limits

<What the description leaves out: dependencies between processes, delays, when the design should change.>
```

## Where each part comes from

| Part | Evidence | Grade |
|---|---|---|
| One row per process | a list of what a firm does: the activities of a value chain (Porter 1985), a process handbook (Malone 1999), a 24-item instrument built from the cross-industry classification, used with 66 small firms (Cragg 2007, secondary) | convention; measured, descriptive, for its use |
| The rows' names | the classification's 13 level-1 categories, read in its file before use ([baseline](../evidence/organisation-design/baseline.md), item 1) | convention; version 8.0 read in its file on 12 Nov. 2026, and listed in `rows` in checks/config.toml |
| The legal person, a row of its own | the firm holds assets apart from its owners (Hansmann 2000); a menu of legal forms, chosen (Guinnane 2007) | convention; measured, descriptive |
| Tasks, Who, Reward, Information | the four [universal problems of organizing](../evidence/organisation-design/frame.md) (Puranam 2014, pages 165-166, read in the original) | convention |
| Decides and Controls, apart | ownership and control are separated (Fama 1983, located only, title); B1 keeps deciding and controlling apart on that reading ([baseline](../evidence/organisation-design/baseline.md), item 4) | convention, from a title |
| Delegated | delegation follows the value of local adaptation (McElheran 2014); information and communication tools move it in opposite directions (Bloom 2014) | measured |
| A role apart from the person | practice writes a role with a purpose and its domains (HolacracyOne 2026 Constitution, an example of practice only) | convention |
| The org chart beside it | the practice B1 is compared with ([baseline](../evidence/organisation-design/baseline.md), item 6) | convention |
| Empty cells counted by a program | B1's two measures, coverage and completeness ([baseline](../evidence/organisation-design/baseline.md#how-it-is-measured)) | convention |

## Where the file goes

A real company's description lives in the company's own repository, never in this public one, which holds only the
worked example. To check it there, copy three things: `checks/local/organisation_description.py`, the `rows` list of
`checks/config.toml` and its files pattern, and install markdown-it-py 4.2.0. The check reads every file that matches
the files of the "organisation description" entry of `[shape_conformance]`.

## Worked example

- A fixture with no real venture: [a-venture-that-personalises-a-product/organisation.md](examples/a-venture-that-personalises-a-product/organisation.md).

## The rules

1. One section titled exactly Processes holds one table, with the eight columns in the order of the skeleton; one
   section titled exactly Roles holds one table. A heading that only mentions processes or roles is another section.
   A table with the Processes or the Roles columns under any other heading is refused. A second table or section would hold rows no program reads. Roles may come before Processes:
   defining a term before its use argues for it, and the check reads either order.
2. One row holds the legal person, and its Process name contains the words "legal person".
3. Who, Decides and Controls name roles from the Roles table, never a person; each role appears once in that table, and
   the table has at least one role. Several roles in one cell are joined by a comma or "and"; a role whose name holds
   "and" is matched whole first.
4. Delegated is yes, no, in part, or left empty; case is not significant. It says whether the role in Decides holds
   the decision by delegation from those who hold the company, the members, rather than as one of them: yes, no, or
   shared with them (in part). Controls names the role that ratifies and monitors the decision, as against initiating
   and carrying it out, on the reading of Fama 1983 the review keeps (located only, title).
4a. Each process category the configuration lists (`rows` in checks/config.toml) is a row, named as listed; a leading
   number such as 1.0 is dropped before the names are compared.
5. An empty cell is left blank or written `?` or `-`. A program counts the empty cells of the six measured columns,
   the four problems and the two rights. It reports the count as a warning, with coverage and completeness as B1
   measures them; Delegated is read, not measured. A description with no empty measured cell gets no warning.
6. The description is read as GitHub renders it, by markdown-it-py with CommonMark, tables and strikethrough, so that
   what a program reads is what a reader sees. Each of the Processes and Roles sections holds one Markdown table at
   its top level: not in HTML, a quote or a list. A cell is read as its rendered text: a link, code, an escape or an
   entity counts as what it shows; inline HTML, an image and struck text count as nothing. A footnote is read as
   written, since GitHub's footnotes are outside that subset.

## The principles it applies

| Part | Principle |
|---|---|
| One table for the whole organisation | [signal the structure](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/page/signal-the-structure.md) |
| A role defined once, used by name | [one place per fact](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/collection/one-place-per-fact.md) |

## Checked by

`organisation-description` (exact): rule 6, read with markdown-it-py. Then one Processes and one Roles table, the eight
columns, one legal row, roles defined and used by name, Delegated's
values, the configured rows; a warning gives the empty cells with coverage and completeness. Whether the rows are
complete, the answers true, and a role in the Roles table a role rather than a person's name is judgment.
