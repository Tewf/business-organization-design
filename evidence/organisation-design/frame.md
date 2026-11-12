# Frame: what a company is, as an organisation, and its names

Step 1 of the review, read on 2026-11-11. It states the problem, gives the field's names beside the practitioners', and says whether the repository's name matches.

**Shape:** [frame](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/frame.md)

## The problem in one sentence

What must a company do, which people and roles must do it and decide it, how can that be written so a program can read it, and how does the design change itself?

## What the field calls it

| Level | The field's name | First met in |
|---|---|---|
| Why a firm exists and where it ends | **theory of the firm**, the **boundary of the firm**: transaction costs, team production, property rights | Coase 1937, Alchian 1972, Williamson 1985 |
| The economics of what happens inside it | **organizational economics** | Gibbons 2012 |
| The firm as a legal person | **organizational law**, **asset partitioning** and **entity shielding** | Hansmann 2000, Hansmann 2006 |
| What a firm does, as a list | **business process**, a **process classification framework**, PCF, and the **value chain** | Porter 1985, Malone 1999, Cragg 2007 |
| How work is divided and coordinated | **organization design** within **organization theory**: **division of labour**, **coordination**, **configurations** | Mintzberg 1979, Thompson 1967 |
| What every organisation must solve | the **universal problems of organizing**: task division, task allocation, reward provision, information provision | Puranam 2014 |
| Who owns and who decides | **corporate governance**, **agency theory**, **decision rights** and **delegation** | Jensen 1976, Fama 1983, Shleifer 1997 |
| The organisation as a processor of information | **information processing view**, OIPT; **team theory**; **decentralized information processing** | Galbraith 1974, Marschak 1972, Radner 1993 |
| Dependencies and how they are managed | **coordination theory** | Malone 1994 |
| Written as a model a program runs | **computational organization theory**; **process models** and **process mining**; **enterprise ontology** | Levitt 1999, van der Aalst 2013, Uschold 1998 |
| Decomposition | **near decomposability**, **modularity**, the **design structure matrix**, DSM | Simon 1962, Baldwin 2000, Browning 2001 |
| How an organisation decides and adapts | the **behavioural theory of the firm**, the **Carnegie school**: aspirations, search, slack | Cyert 1963, March 1958 |
| How it learns | **organizational learning**, **exploration and exploitation**, **routines**, **dynamic capabilities** | March 1991, Levitt 1988, Nelson 1982, Teece 1997 |
| How a design is searched | **adaptation on a rugged landscape**, the NK model | Levinthal 1997 |

## What practice calls it

- **Org chart** and **operating model**: the boxes and lines of a company. The field's word is the formal structure, one of Mintzberg's parameters of design.
- **Process map** or **process framework**: a list of every process, grouped (G7, version 8.0). The field's word is a process classification framework.
- **Enterprise architecture**: a description of a company's processes, structures, information and systems, kept as models in a standard language (OpenGroup 2026 TOGAF, OpenGroup 2026 ArchiMate, Zachman 2026 Framework). The field's word is an enterprise model or an enterprise ontology.
- **Process notation**: a diagram of one process a tool can execute (OMG 2013 BPMN). The field's word is a process model.
- **Roles, accountabilities and domains**: a role defined apart from the person who fills it (HolacracyOne 2026 Constitution). The field's word is task allocation, one of the four universal problems.

## Does the repository's name match?

- In part. The field says **organization**, in American spelling, and splits the subject in two: organization design and organization theory on one side, the theory of the firm and organizational economics on the other.
- "Organisation" names the shared object of both halves, and the subtitle "what a company is" restricts it to the firm. The maintainer later renamed the repository after the design side ([record 0004](../../decisions/0004-rename-to-business-organization-design.md)).

## Sub-questions

| Question | Strand in review.md |
|---|---|
| Q1 what must a company do, as an enumerable list of functions or processes, economic, legal, technical and human? | Strand 1 |
| Q2 what problems must its human architecture solve, and who decides what? | Strand 2 |
| Q3 how is an organisation written as an information-processing system, so that a program can read it? | Strand 3 |
| Q4 how does an organisation adapt and learn, and change its own design? | Strand 4 |

## Held elsewhere

- The business model's blocks, value, channels, revenue and costs: [business-model](https://github.com/Tewf/business-model).
- Cash, runway and funding, so the finance side of governance: [business-finance](https://github.com/Tewf/business-finance).
- Demand and customers: [business-customer](https://github.com/Tewf/business-customer). Prices: [business-pricing](https://github.com/Tewf/business-pricing). Markets: [business-market](https://github.com/Tewf/business-market).
