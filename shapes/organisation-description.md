# Shape: organisation description

One organisation written as B1's table: one row per process, one column per problem of organizing, and the roles
that answer them defined once. Its reader is whoever must run the organisation or change it, and asks: for each thing
the company must do, who does it, for what reward, with what information, who decides and who controls? It is a page,
and a program reads it.

**Status:** proposed, 2026-11-12. It builds on B1, which waits on the maintainer's acceptance
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
| One row per process | a list of what a firm does: the activities of a value chain (Porter 1985), a process handbook (Malone 1999), the cross-industry classification used in 66 small firms (Cragg 2007) | convention; measured, descriptive, for its use |
| The rows' names | the classification's level-1 categories, read at source before use (baseline, item 1) | PROVISIONAL: the categories are not read yet; `rows` in checks/config.toml stays empty until they are |
| The legal person, a row of its own | the firm holds assets apart from its owners (Hansmann 2000); a menu of legal forms, chosen (Guinnane 2007) | convention; measured, descriptive |
| Tasks, Who, Reward, Information | the four [universal problems of organizing](../evidence/organisation-design/frame.md) (Puranam 2014, page 166, as quoted in Martela 2019) | convention |
| Decides and Controls, apart | decision management and decision control are separated (Fama 1983) | convention |
| Delegated | delegation follows the value of local adaptation (McElheran 2014); information and communication tools move it in opposite directions (Bloom 2014) | measured |
| A role apart from the person | practice writes a role with a purpose and its domains (HolacracyOne 2026 Constitution, an example of practice only) | convention |
| The org chart beside it | the practice B1 is compared with (baseline, item 6) | convention |
| Empty cells counted by a program | B1's two measures, coverage and completeness (baseline, How it is measured) | convention |

## Worked example

- A fixture with no real venture: [a-venture-that-personalises-a-product/organisation.md](examples/a-venture-that-personalises-a-product/organisation.md).

## The rules

1. The Processes table has the eight columns in the order of the skeleton.
2. One row holds the legal person.
3. Who, Decides and Controls name roles from the Roles table, never a person.
4. Delegated is yes, no, in part, or left empty.
5. An empty cell is left blank or written `?`; a program counts it, and the count is the description's first finding.

## The principles it applies

| Part | Principle |
|---|---|
| One table for the whole organisation | [signal the structure](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/page/signal-the-structure.md) |
| A role defined once, used by name | [one place per fact](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/collection/one-place-per-fact.md) |
| The processes before the roles | [overview first](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/document/overview-first.md) |

## Checked by

`organisation-description` (exact): the eight columns, the legal row, roles defined and used by name, Delegated's
values, the configured rows; a warning gives the empty cells with coverage and completeness. Whether the rows are
complete and the answers true is judgment.
