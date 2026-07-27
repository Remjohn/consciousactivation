# Implementation scope

Implement one deterministic command/query slice that consumes the exact active ST-03.04 manifest and its 21 in-memory artifacts, reads and hash-verifies the accepted constitutional-precedence contract through a bounded standard-library adapter, and emits one immutable constitutional validation report and receipt.

Validation must prove the closed artifact inventory, exact hashes, source-node resolution, semantic equality to the active HarnessIR, authority ordering, Constitution V1.1 and Builder PRD V1.2 identity, separate rich lineage keys, explicit `NOT_APPLICABLE` treatment, compatibility, and absence of lower-authority invention. Syntactically valid JSON or Markdown does not pass when its semantic or authority binding conflicts.

The validator may inspect stored bytes but never mutates HarnessIR or generated artifacts. It atomically appends one run reference/event with the report, command record, and receipt. The run remains in `GENESIS`. Duplicate commands return the original receipt; stale, altered, invalidated, incomplete, conflicting, or unauthorized inputs fail with no partial state. An upstream boundary reopen must make the report unusable while preserving immutable history.

Implementation requires additive typed contracts, one bounded file adapter, command service, tests, repository port behavior, run replay/invalidation state, and observations. It requires no schema file, database, dependency, network, external runtime, UI, API, workflow, capability graph, Atomic Harness Definition, or production behavior.
