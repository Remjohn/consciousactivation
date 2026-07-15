# ADR-006: Workflow Engine Adapter

Status: `ACCEPTED`

Owners: Workflow architecture and operations. Trace: D003, D006, D025, D026, D027, D032, D033; F18; TS-14. Blocker: BD-006.

## Context

Builder requires durable routing, long human waits, retries, timers, checkpoints, parallel branches, signals, replay, rollback, and incidents. Hand-rolled loops or one agent session would violate F18. Domain state must remain independent of a workflow vendor.

## Decision

Compile governed Workflow IR to a Temporal adapter for production scheduling. Provide an in-memory deterministic adapter for unit/integration tests. Temporal workflows coordinate; activities invoke Builder application commands. Run Ledger events, not Temporal history, remain canonical product truth.

## Alternatives

- Custom database scheduler: rejected provisionally due high correctness and incident burden.
- Celery/RQ: rejected provisionally because durable human gates, deterministic replay, and workflow migration are weak.
- Pi conversation orchestration: rejected by AG-019 and HG-011.
- Temporal as product truth: rejected because it couples domain authority to engine history.

## Interfaces, Data, And Errors

`WorkflowEnginePort.start/signal/cancel/query/replay/migrate`; typed engine binding maps workflow/node IDs, timeouts, retry policies, search attributes, and checkpoint references. Errors include engine unavailable, incompatible workflow version, activity timeout, non-deterministic replay, and signal conflict.

## Authority, Security, And Determinism

Workflow definitions and routes are deterministic. Activities receive scoped capability tokens. Human signals pass through authenticated application commands. Agent execution occurs only in sandbox activities with validated capsules.

## Consequences

Positive: proven durability and incident tooling. Cost: Temporal deployment, deterministic workflow constraints, adapter and versioning discipline.

## Observability, Performance, Migration

Correlate engine workflow/activity IDs with run/node/event IDs. Measure schedule latency, replay failures, attempts, timers, and history size. In-flight version changes use worker versioning or continue-as-new plus Builder migration receipts.

## Verification

Run the same public-seam suite against in-memory and Temporal adapters. Fault tests cover worker loss, duplicate activity completion, stale signal, timeout, engine restart, and rollback.
