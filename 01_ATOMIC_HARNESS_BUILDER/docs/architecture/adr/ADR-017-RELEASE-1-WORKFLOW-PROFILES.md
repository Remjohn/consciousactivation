# ADR-017: Release 1 Workflow Profiles

Status: `ACCEPTED`

Owners: Product lead, Builder maintainer, and workflow architecture. Trace: D006, D022, D025, D026, D027, D032; F18; TS-14. Blocker: BD-013.

## Context

F18 requires specialized workflows for materially different work. Release 1 cannot certify an unbounded registry, but new-harness compilation alone omits evidence changes, benchmark regressions, repair, re-certification, and incidents.

## Decision

Require five profiles in Release 1:

1. New harness compilation.
2. Incremental evidence refresh.
3. Benchmark regression.
4. Repair and re-certification.
5. Constrained incident hotfix.

Format 02 new-harness compilation is the primary shadow and production candidate. Other profiles derive from its nodes/contracts while preserving distinct triggers, authority, budgets, and gates.

## Alternatives

- New compilation only: rejected because operational failure paths remain untested.
- Every PRD-listed future profile: rejected as unnecessary Release 1 scope.
- One profile with mode flags: rejected because authority, routing, and risk differ materially.

## Interfaces, Data, And Errors

Each `WorkflowProfile` declares trigger, target, Workflow IR, actor matrix, routing predicate, budgets, sandbox policies, human gates, tests, certification, and rollback. Unknown/ambiguous route fails closed.

## Authority, Security, And Determinism

Deterministic router selects only registered profiles. Incident profile has narrower grants and stronger human gates, never emergency authority over evidence, labels, or constitutional decisions.

## Consequences

Positive: sufficient operational coverage without profile sprawl. Cost: five end-to-end/fault suites and promotion lifecycles.

## Observability, Performance, Migration

Compare latency, cost, intervention, failures, and outcomes per profile. Profile versions are immutable; in-flight runs stay bound or migrate through a receipt.

## Verification

Routing, authority, checkpoint, fault, promotion, rollback, and cross-profile isolation tests are mandatory. Product authority must ratify the list.
