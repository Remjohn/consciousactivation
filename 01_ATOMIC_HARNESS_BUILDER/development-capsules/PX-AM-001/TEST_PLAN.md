# PX-AM-001 Test Plan

PZ-01 proves canonical generic and Activative manifest parsing, complete rich
Activative Intelligence validation, structured lineage, forbidden production
claims, deterministic bytes and typed failures.

PZ-02 proves schema migration, fresh-process durability, expected-version
concurrency, payload-safe idempotency, hash integrity, transaction rollback and
zero partial state.

PZ-03 proves command parsing, deterministic human and JSON output, stable exit
codes, service delegation and end-to-end ingest/build/inspect/export composition.

PZ-04 proves generic and Activative `AtomicHarnessDefinition` package generation,
portable relative paths, complete structured lineage, byte equality, changed-input
identity changes, no external runtime, and explicit non-production/non-certification.

The integrator runs the complete regression after PZ-01, PZ-02 and PZ-03, then
twice from fresh processes after PZ-04. No receipt may claim PASS before its gate.
