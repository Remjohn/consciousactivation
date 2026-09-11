# M09 — Authenticated Evidence Handoff

**Status:** PROPOSED
**Depends on:** M07, M08
**Primary requirements:** FR-IP-007, FR-IP-010

## Objective

Preserve the full lineage from hypothesis/question attempt to human response/evidence and make downstream content candidates traceable to that evidence.

## Minimum lineage

`upstream hypothesis refs`
`→ question candidate/version`
`→ question attempt`
`→ response/source reference`
`→ observation`
`→ accepted evidence reference`
`→ downstream candidate reference`.

## Anti-fabrication rules

- no evidence from a receipt alone;
- no inference relabeled as Guest statement;
- no archetype readiness without supporting response structure;
- no downstream candidate without source lineage;
- no cross-workspace reference laundering.

## Required tests

1. missing response prevents evidence acceptance;
2. wrong workspace/session reference is rejected;
3. fabricated receipt cannot authenticate evidence;
4. accepted evidence can be read back from the authoritative store;
5. downstream candidate can trace back to the same source evidence.

## Stop conditions

Stop if the repository lacks a canonical owner for source/interview evidence handoff. Report the gap and owner.
