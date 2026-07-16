# Implementation Scope

Implement only these five invariant repairs:

1. Reconstruct every governed `AtomicHarnessDefinition` semantic and section field
   from active hash-pinned upstream authority, authenticate its compiler actor and
   reject any forged-and-rehashed candidate before report, event, receipt or command commit.
2. Build target-validation observations before commit, persist them through the
   current repository transaction boundary, return the committed receipt when sink
   delivery degrades, and retain deterministic pending delivery without a false
   `NOT_COMMITTED` outcome.
3. Synchronize every current in-memory stream writer across version validation,
   invariant checks and assignment so two same-version writers yield exactly one winner.
4. Commit run events, optional checkpoint, receipt and command/idempotency record
   through one repository operation for create, transition, waiver, checkpoint and resume.
5. Hash and inspect ZIP input from the same immutable byte buffer.

No new production module is authorized. Existing canonical bytes and identities for
valid historical artifacts must remain unchanged.

