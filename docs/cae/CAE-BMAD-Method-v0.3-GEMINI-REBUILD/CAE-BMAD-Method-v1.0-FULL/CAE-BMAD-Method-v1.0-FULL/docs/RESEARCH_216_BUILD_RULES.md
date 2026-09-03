# 216-Source Research Library Rules

## Selection question

Would removing this source make it materially harder to reconstruct:

- what the product is
- why it is the way it is
- what capabilities exist
- what abstractions were inherited
- how the production system works
- how the operator works with it
- how the code implements it
- why major decisions were made

If yes, it belongs.

## The library must not be dominated by the latest CAE docs

The library is historical + product + engineering.

A source from CCP or CMF can be more important than a current CAE planning document.

An Atomic Harness file can be more important than an architecture overview because it may reveal a
production abstraction that later became implicit.

## Relevance score

Use 0–100.

100 — indispensable
90–99 — major product/architecture lineage
80–89 — major support
70–79 — important context
60–69 — specialist

Never use relevance as a substitute for authority.

## Operating level

Each source also gets the level at which it is most informative:

line / block / function / type / class / file / module / directory / database / table /
script / CLI / application / repository / product / documentation / plan / agent /
AI developer workflow / software factory

## Contributor

Record:

- original author
- team/org
- transcript author
- code contributor
- unknown

Use `Unknown` rather than inventing a contributor.

## Evidence status

Use:

KNOWN
INHERITED
VERIFIED
PROPOSED
INFERRED
MISSING
CONTRADICTED
DEPRECATED
