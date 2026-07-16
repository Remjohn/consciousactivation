# ADR-016: Deployment And Observability

Status: `ACCEPTED`

Owners: Operations, security, and architecture. Trace: D003, D020, D024, D025, D032; TS-12, TS-14. Blockers: BD-005, BD-006, BD-009, BD-012.

## Context

Release 1 needs reproducible environments, isolated workers, durable state, telemetry, promotion, rollback, incident handling, and backup/restore. No deployment assets currently exist.

## Decision

Package API, workflow worker, deterministic worker, sandboxed agent/evaluator workers, projection worker, and Control Tower UI as separate containers/processes around shared PostgreSQL, CAS, proposed workflow engine, and OpenTelemetry collector. Environments are development, CI, shadow, and production. Configuration is versioned; secrets are external references.

## Alternatives

- One desktop process: rejected for worker isolation and operational proof.
- Kubernetes required initially: rejected pending measured scale; container contracts permit later orchestration.
- Provider-specific serverless: rejected for long workflows, sandboxes, and portability.
- Logs only: rejected because traces, metrics, events, and receipts serve different purposes.

## Interfaces, Data, And Errors

Health/readiness, metrics, traces, structured logs, deployment manifests, backup/restore, migration jobs, and promotion receipts. Failures include dependency unavailable, schema mismatch, unhealthy worker, telemetry interruption, backup failure, and rollback incompatibility.

## Authority, Security, And Determinism

Deployments use least-privilege service identities, immutable image digests, signed manifests, secret references, network policies, and environment separation. Promotion requires human authority and exact test/benchmark/policy identities.

## Consequences

Positive: isolated scaling, repeatable promotion, and operational evidence. Cost: container/runtime operations and multiple deployable units.

## Observability, Performance, Migration

OpenTelemetry correlates run/workflow/node/command/artifact IDs. SLOs include availability, latency, queue, projection lag, workflow success, cost, backup age, and restore time; exact targets require ratification. Schema/deployment migrations use expand/migrate/contract and tested rollback.

## Verification

CI must run image, dependency, secret, network, migration, backup/restore, telemetry, promotion, and rollback tests in an environment matching production contracts.
