# Exact Implementation Scope

Implement one command path for `ST-01.02/SYNTHETIC_DEFINITION`:

1. Load the already-created synthetic Builder run and verify its exact target
   profile identity and current `CREATED` lifecycle state.
2. Authorize a deny-by-default `LOCK_EVIDENCE_WORKSPACE` action.
3. Load and hash-verify `SYNTHETIC_SOURCE_PROFILE.json` and its exact
   repository-relative target candidate.
4. Diagnose a supported file, directory, or ZIP before committing state.
5. Reject unsafe paths, links, archive members, executables, unsupported media,
   missing authority, missing required role, or budget overflow with typed,
   actionable evidence and no state mutation.
6. Produce immutable ordered `SourceDescriptor` records and an aggregate
   `SourceLock`. Content identity uses raw SHA-256; portable provenance uses
   `repo://` plus relative member paths and never stores a workstation path.
7. Atomically append `SOURCE_DIAGNOSTIC`, attach the Source Lock, and transition
   to `SOURCE_LOCKED` using the existing run repository/concurrency seam.
8. Make command replay idempotent, reject command-ID payload changes, and emit
   deterministic success/failure observations and a typed receipt.
9. Detect later source-byte changes without rewriting the prior lock; return a
   new lock identity and explicit invalidation relationship.

The implementation may add the evidence domain/application/adapter modules and
the minimal extensions to run state, authority, ports, the in-memory repository,
and the synthetic profile lifecycle needed for this outcome. It may update the
existing ST-01.01 architecture test only by adding the newly authorized source
paths to its exact allow-set; no assertion or prohibited import rule may weaken.

No API, CLI, database, CAS, network, schema, category registry, compiler,
external runtime, or production adapter is included.
