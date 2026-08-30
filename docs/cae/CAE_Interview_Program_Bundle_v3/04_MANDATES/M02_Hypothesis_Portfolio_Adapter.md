# M02 — Hypothesis Portfolio Adapter

**Status:** PROPOSED
**Depends on:** M01
**Primary requirements:** FR-IP-001, FR-IP-002

## Objective

Create the smallest derived adapter/view needed to represent the Interview Program candidate portfolio using existing AIR activation-hypothesis/portfolio authority and the approved coordinate model.

## Boundary

The adapter is not a new canonical hypothesis ontology. It may combine references, derived diagnostics, and candidate presentation data. Existing AIR objects remain authoritative.

## Required behavior

- accept only real upstream references available through approved interfaces;
- represent coordinate/collision information without claiming new canonical ownership;
- support candidate provenance;
- support semantic overlap/cluster information;
- support candidate scoring diagnostics as advisory, not proof;
- support candidate states such as selected/rejected/deferred for Operator workflow if an existing persistence boundary can own them;
- preserve original upstream references through every derivation.

## 96 → 16–24 rules

- ~96 is a planning/search target, not a database constraint;
- fewer candidates are valid when source density is low;
- more internal candidates may be evaluated without expanding the user-facing contract;
- selection must maximize useful diversity, not raw score;
- selected candidates are semantic acquisition targets, not guaranteed final content pieces.

## Required acceptance tests

1. invalid upstream reference cannot become launchable;
2. duplicate/near-duplicate candidates can be clustered or penalized;
3. portfolio selection can be smaller than 16 when evidence is insufficient;
4. selected candidates retain lineage;
5. no write occurs against AIR-owned objects unless the existing owning API explicitly supports the authorized mutation.

## Required evidence

- exact current adapter source path;
- actual reference examples from fixtures/tests;
- selection/diversity test results;
- no-new-object inventory.

## Stop conditions

Stop if an existing canonical object must be changed to represent the required semantics and no ratified spec authorizes that change.
