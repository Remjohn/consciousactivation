# ST-11.01 Rollback Evidence

Verdict: **PASS**

## Atomic failure

The in-memory development/test repository was instructed to fail the next Development Capsule commit. The command raised typed `AtomicCommitFailed` and left zero capsules, receipts, attachment events, command records, run capsule references or Story observations. After fault removal, the identical command completed at stream version 25.

## Non-destructive invalidation

An authorized upstream atomic-boundary reopen generated the complete 15-event descendant chain through the Atomic Harness Definition, ST-07.04 validation and ST-11.01 capsule. Active capsule access failed closed, the capsule was marked invalidated, and historical capsule bytes remained exactly reproducible.

Replay returned the original receipt without duplicate state. Checkpoint resume preserved capsule identity. Conflicting command reuse failed closed.

## Source rollback boundary

Rollback is limited to the two new ST-11.01 source modules, four bounded source integrations, five exact-source additions, six Story-test files and Story completion outputs. It does not mutate predecessor implementations or receipts, constitutional/product authority, planning baselines, governance, schemas, contracts, Program Control or external repositories.

No destructive rollback command was required or executed.
