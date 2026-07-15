# ADR-004: Deterministic Compilation And Schema Evolution

Status: `ACCEPTED`

Owners: Compiler and schema architecture. Trace: D003, D011, D029; TS-06, TS-09, TS-13.

## Context

Many human and machine artifacts must remain consistent with one canonical IR. Independent templates or manual editing create drift. Schema changes must not strand in-flight runs or invalidate receipts silently.

## Decision

Use canonical JSON serialization, content hashes, immutable compiler identities, declared IR-path dependencies, atomic artifact manifests, generated JSON Schemas, and explicit migration/upcaster registries. Identical inputs must produce byte-identical deterministic artifacts or an approved nondeterminism exception.

## Alternatives

- Hand-authored documents as peers: rejected because authoritative truth duplicates.
- Regenerate everything after every change: rejected because it obscures impact and wastes evaluation.
- In-place schema mutation: rejected because it destroys replay and compatibility evidence.

## Interfaces, Data, And Errors

`Compiler.compile(snapshot, profile, config) -> ArtifactManifest`; `Migration.upgrade(from_version, to_version) -> snapshot + receipt`. Errors include invalid IR, missing migration, nondeterminism, undeclared dependency, cross-artifact mismatch, and drift.

## Authority, Security, And Determinism

Compiler workers use immutable inputs, empty output workspaces, no network/model access, and secret scans. Agents propose typed patches only. Human approval is required for breaking migrations and nondeterminism exceptions.

## Consequences

Positive: reproducibility, targeted invalidation, reliable rollback, and generated-schema consistency. Cost: strict canonicalization and golden vectors for every compiler/migration.

## Observability, Performance, Migration

Record cache hits, compile duration, dependency selectors, manifest hashes, drift, and migration outcomes. Builder Next migration applies to its own versions; V2.1 import remains excluded by ADR-015.

## Verification

Golden tests run across platforms/locales. Property tests verify canonical serialization. Migration tests prove forward conversion, rollback or explicit irreversibility, and old-event replay.
