# 0001: A repository of its own

**Decision:** What a company is, as an organisation, is one problem, so it gets one public repository, set up with its
scope and nothing more.

**Status:** accepted, 2026-11-11. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- The maintainer's rule for the family: one repository per problem, and no overlap between two. A problem left inside
  a wider repository makes every user of it depend on everything else there.
- The six members of the family were set up the same way on 2026-11-04: scope first, the review as the first job, the
  name provisional until that review's frame step.
- Each of the six holds one part of a venture: its model, its prices, its customers, its cash, its biases, its market.
  None holds the company itself: the functions it must run, the people and roles that run them, and how it adapts.
- The boundary with the neighbours is drawn on the front page's scope table. In short: the model's building blocks
  stay with business-model, cash with business-finance, demand with business-customer, prices with business-pricing
  and markets with business-market.

## Decision

- One public repository for this problem, under the family's prefix, with a provisional name that the review's frame
  step tests against the field's names.
- At its start it holds its scope, the questions its review must answer, the checks of reader-ergonomics in CI, a
  site, and this record. Nothing of the work itself.
- It pins reader-ergonomics v1.24.2 by commit, and links down only.

## Options not taken

- A section of business-model: the model's blocks say what a venture sells and earns, not who in it decides what, so
  every reader of the model would depend on the organisation too.
- No repository until a venture needs one: the family's other members are already written for any venture, and this
  one is read by them.

## Consequences

- A later session can start from the front page alone: the scope, the first job and the questions are there.
- A fact that belongs here is linked from the neighbours, never copied; a fact that belongs to a neighbour is linked
  from here.
- **Bad:** the subject is wider than any neighbour's, and the field behind it is a century of economics, sociology and
  management; a first review can only be a first pass.
- **Bad:** a rename after the frame step would move the address once.

## See also

[Decisions](README.md); [the front page](../README.md), where the scope and the first job are.
