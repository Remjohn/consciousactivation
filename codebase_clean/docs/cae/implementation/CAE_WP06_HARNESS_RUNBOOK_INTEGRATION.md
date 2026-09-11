# CAE WP-06 Harness / Skills / Runbook Integration

**Work package:** WP-06 — Harness / Skills / Runbook integration
**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`
**Boundary:** a versioned procedural runbook and companion Skill for the WP-03
first slice. No Builder Harness IR, Builder Workflow IR, Pipeline binding,
legacy service, or database schema is changed.

## Brownfield mapping

| CAE control object | Existing artifact | WP-06 disposition |
|---|---|---|
| Product harness definition | Builder Harness IR / `atomic_harness_definition.py` | READ; never store CAE procedural or runtime state in it |
| Builder orchestration | Builder Workflow IR; ADR-002 | READ; remains separate from product/runbook state |
| Skills/capsules | Builder ADR-009, skill packages, JIT capsules | READ; CAE companion Skill is doctrine, not a Builder canonical capability/capsule |
| Runtime binding | Pipeline harness binding manifest/compiler | READ; no Pipeline compilation path is invoked |
| Durable CAE state | staging aggregate/command/event/receipt tables | BIND; runbook reads this authority through typed operations |

## Implemented procedural contract

`docs/cae/runbooks/evidence_to_air_first_slice_v1.yaml` defines:

- procedural states `RECON`, `CAPTURE`, `AUTHENTICATE`, `ASSESS`,
  `OPERATOR_REVIEW`, `COMPLETE`, `REPAIR_REQUIRED`, `BLOCKED`, and `FAILED`;
- exact bindings to the five WP-03 operations and five transition contracts;
- required evidence, receipt/projection agreement, recovery routes, fidelity
  declarations, and anti-reward-hack counterchecks;
- an explicit no-shadow-state rule.

The companion Skill teaches recognition, authorized procedure, and transition
discipline. It cannot mutate operational state itself.

## What was proven

The runbook's operation/contract pairs were verified against the real staging
PostgreSQL registry. Its terminal/recovery states, no-raw-SQL rule, distinct
evaluator guard, stale-state countertest, immutable-payload countertest, and
E3-versus-E4 boundary are machine-checked. The underlying transitions retain
the WP-03 real staging proof.

## What was not proven

- No agent runtime loads or executes this runbook yet.
- No Builder Harness IR / skill package / JIT capsule is generated from it.
- No Pipeline binding or existing API/service path calls the CAE operations.
- No test establishes semantic correctness, taste, or real-world effectiveness.

## Exact operator decision

**Promote WP-06 and authorize WP-07 to design execution receipts and evidence
lineage beyond the existing operation envelope, without treating a runbook as
durable state or exposing quarantined registry records?**
