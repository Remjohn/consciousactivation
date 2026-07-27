# ADR-003: Authoritative State And Artifact Storage

Status: `ACCEPTED`

Owners: Architecture and operations. Trace: D003, D006, D011, D025, D027, D029; TS-01, TS-05, TS-06, TS-10, TS-12, TS-13. Blocker: BD-005.

## Context

Builder needs atomic commands, optimistic concurrency, event replay, queryable projections, immutable large artifacts, exact identity, and backup/restore. Files alone do not provide concurrency or relational traceability; storing media blobs in the event database harms operations.

## Decision

Use PostgreSQL as the authoritative event, snapshot, command-receipt, registry, and projection store. Use a SHA-256 content-addressed artifact store with filesystem adapter for development and S3-compatible adapter for production. Commit artifact references and events atomically after staged bytes verify.

## Alternatives

- SQLite: rejected for production proposal because concurrent workers and operational recovery need stronger shared semantics; retained only as a possible test adapter after parity proof.
- Document database: rejected because stream concurrency, relational traceability, and migration constraints dominate.
- Event broker as source of truth: rejected; brokers deliver notifications but do not own product state.
- Filesystem-only state: rejected for concurrency, query, and authority reasons.

## Interfaces, Data, And Errors

Ports: `EventStore`, `SnapshotStore`, `ProjectionStore`, `RegistryStore`, `ArtifactStore`, `TransactionManager`. Tables include streams, events, snapshots, command receipts, outbox, artifact index, and projections. Errors include version conflict, duplicate command mismatch, missing artifact, hash mismatch, event discontinuity, and storage unavailable.

## Authority, Security, And Determinism

Only application command handlers append events. Database roles separate command, projection, benchmark-label, and operations access. CAS objects are immutable and encrypted in transit/at rest.

## Consequences

Positive: transactional authority, replay, strong queries, and artifact scalability. Cost: PostgreSQL/object-store operations and referential-integrity tooling.

## Observability, Performance, Migration

Measure append latency, conflicts, projection lag, artifact throughput, orphan staging, backup age, and restore integrity. Migrations use expand/migrate/contract, event upcasters, dual readers, and rollback receipts. RPO/RTO require operations ratification.

## Verification

Contract tests run against real PostgreSQL and both CAS adapters. Fault tests cover crash between staging and event commit, duplicate delivery, backup/restore, missing object, and projection rebuild.
