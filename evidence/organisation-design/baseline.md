# Baseline

Step 5 of the review: the baseline the work is compared against. Evidence is in [review](review.md).

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/baseline.md)

## B1: a process list with the four problems of organizing answered for each process

![B1 is a table with one row per process category and one column per problem: tasks, who, reward, information, who decides and who controls; it is compared, on the same venture, with an org chart of boxes and reporting lines.](b1.svg)

<details>
<summary>Graphviz source</summary>

```dot
// B1 against the practice. Colours: purple for this repository's baseline, grey for the practice it is compared with.
digraph b1 {
  graph [rankdir=LR, nodesep=0.5, ranksep=0.7, bgcolor="white", pad=0.2, fontname="Inter"];
  node  [shape=plaintext, fontname="Inter", fontsize=12, fontcolor="#1F2328"];
  edge  [fontname="Inter", fontsize=11, color="#3D434B", fontcolor="#55575F", penwidth=1.3, arrowsize=0.8];
  B1 [label=<<table border="1" cellborder="1" cellspacing="0" cellpadding="6" color="#7A4FA3" bgcolor="#F1EAF7">
    <tr><td colspan="7"><b>B1: one row per process, one column per problem</b></td></tr>
    <tr><td><b>process</b></td><td>tasks</td><td>who</td><td>reward</td><td>information</td><td>decides</td><td>controls</td></tr>
    <tr><td>category 1</td><td>.</td><td>.</td><td>.</td><td>.</td><td>.</td><td>.</td></tr>
    <tr><td>category 2</td><td>.</td><td>.</td><td>.</td><td>.</td><td>.</td><td>.</td></tr>
    <tr><td>...</td><td colspan="6"><font color="#55575F">an empty cell is counted by a program</font></td></tr>
  </table>>];
  OC [label=<<table border="1" cellborder="0" cellspacing="0" cellpadding="6" color="#6A6D77" bgcolor="#FFFFFF">
    <tr><td><b>the practice: an org chart</b></td></tr>
    <tr><td>boxes for people, lines for who reports to whom</td></tr>
    <tr><td><font color="#55575F">what is not drawn is not seen</font></td></tr>
  </table>>];
  B1 -> OC [label=" compared on the same venture", dir=both, style=dashed];
}
```

</details>

1. The rows are the level-1 categories of the cross-industry process classification, the most adopted list of what a company does (Cragg 2007). The maintainer reads them at their source before use, since its page refused an automated reader (protocol, G7).
2. One row is added for the legal function the classification may not hold: the firm as a person holding assets apart from its owners (Hansmann 2000).
3. The columns are the four universal problems of organizing for that process: its tasks, who does them, how they are rewarded and what information they receive (Puranam 2014). The "who" is a role, defined apart from the person who fills it (HolacracyOne 2026 Constitution).
4. Two more columns name who decides and who controls each process, kept apart (Fama 1983), and whether the decision is delegated (McElheran 2014).
5. The table is data a program reads, so that a missing cell is counted, not noticed.
6. It is compared with the practice, an org chart of the same venture: boxes for people and lines for reporting (Mintzberg 1979 for the parts it draws).

## Compared with what the review found

| Item | In B1 | Fit |
|---|---|---|
| A list of what a firm does (Porter 1985, Malone 1999, Cragg 2007) | the rows | matches, for a practice list; its completeness is untested |
| The legal person (Hansmann 2000, Hansmann 2006) | one added row | in part: one row, not the law of any country |
| The four universal problems (Puranam 2014, Martela 2019) | four columns | matches |
| Decision rights, ownership and control apart (Fama 1983, Jensen 1976) | two columns | in part: who owns is left to business-finance |
| Delegation by the value of adaptation (McElheran 2014) | a column marks it | in part: the value is not measured |
| Coordination as the management of dependencies (Malone 1994) | none | lacks |
| Efficiency as the number of processors and the delay (Radner 1993) | none | lacks |
| Adaptation and a change of design (March 1991, Levinthal 1997, Siggelkow 2005) | none | lacks |
| Fit to a configuration (Mintzberg 1979) | none, on purpose | the five types did not predict effectiveness (Doty 1993) |

## What B1 lacks

- The dependencies between processes, which coordination theory makes the core of an organisation (Malone 1994).
- A measure of the information each process must handle and the delay of its decisions (Radner 1993, Van Zandt 1999).
- Any rule for when the design should change, though a sequence of structures can beat a fixed one (Siggelkow 2005).
- A test that the rows are complete (position, Not found).
- Evidence on young firms: the field's results come from established ones (against, a young venture).

## How it is measured

- Coverage: the share of process rows with a role in the "who" column.
- Completeness: the share of the cells of the table that are filled, four problems and two rights per row.
- Gaps found: the number of empty cells in B1 for a venture whose org chart shows no gap, on the same venture.
- A repeat: a program counts the cells of any description written as the table, and its test passes on a fixture that holds no real company.

## The review is finished

The baseline is named: B1. The next work is a shape for the description of one organisation as B1's table, with a check that counts its empty cells, filled first on a fixture of a venture that personalises a product.
