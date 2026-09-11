# M07 — Semantic Acquisition Observation

**Status:** PROPOSED
**Depends on:** M04
**Primary requirements:** FR-IP-006, FR-IP-007

## Objective

Introduce the minimum derived observation model needed to make answer-driven routing and evidence lineage explainable.

## Required observation dimensions

- resolution: abstract/general/specific/episodic/mechanistic/evidential;
- completeness: unknown/partial/sufficient/verified/exhausted;
- evidence mode;
- temporal orientation;
- social reference frame;
- interactional fit;
- discrepancy references;
- missing requirement references;
- new branch references;
- system inference references;
- Guest-validated interpretation references.

## Evidence distinction

The runtime must preserve the difference between:

1. what the Guest actually stated;
2. what the system inferred;
3. what the Guest explicitly confirmed/corrected.

## Required tests

- receipt existence alone does not make evidence authenticated;
- system inference is not serialized as Guest fact;
- an answer can change completeness without changing hypothesis identity;
- contradiction is recorded as discrepancy before reconciliation;
- observation can drive a different next-question action.

## Stop conditions

Stop if implementing this requires changing an upstream canonical evidence object that is outside the current service owner. Escalate the contract change instead.
