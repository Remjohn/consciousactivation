# M10 — Content Menu Readiness

**Status:** PROPOSED
**Depends on:** M05, M09
**Primary requirement:** FR-IP-010

## Objective

Prepare an operator-facing content candidate menu from authenticated evidence without forcing a fixed number of content pieces per hypothesis.

## Candidate representation

Each candidate should preserve:

- source hypothesis;
- supporting evidence refs;
- semantic role;
- response structure;
- archetype/format compatibility;
- confidence/diagnostics;
- provenance;
- any missing evidence required before production.

## Quantity rule

~32 is a planning aspiration, not a quota. One hypothesis can yield multiple viable pieces; another may yield none.

## Operator role

The system may rank and cluster. The Operator selects production-worthy candidates. Distribution performance must not compensate for semantic failure.

## Tests

- generic fluent material can be rejected;
- strong evidence may yield multiple compatible formats;
- unsupported archetype is flagged;
- candidate lineage survives selection;
- no production candidate appears without evidence lineage.

## Stop conditions

Stop if the downstream production consumer/contract is not identifiable. Do not invent a new production ontology merely to finish the menu.
