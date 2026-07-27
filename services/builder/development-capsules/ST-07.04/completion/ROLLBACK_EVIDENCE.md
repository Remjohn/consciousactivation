# ST-07.04 Rollback Evidence

Verdict: **PASS**

## Atomic failure

The in-memory development/test repository was instructed to fail the next target-validation commit. The command raised the typed `AtomicCommitFailed` error and left:

- zero validation reports;
- zero validation receipts;
- zero validation attachment events;
- zero command records;
- zero run validation references;
- zero Story observations for the failed atomic attempt.

After fault removal, the identical command completed normally at stream version 24. This proves clean retry without partial state.

## Non-destructive invalidation

An authorized upstream atomic-boundary reopen generated the complete descendant invalidation chain through the Atomic Harness Definition and ST-07.04 validation. Active validation became unusable, the report was marked invalidated, and historical report bytes remained exactly reproducible.

Replay and checkpoint resume preserved validation identity without duplicate acceptance or state. Conflicting command reuse failed closed.

## Source rollback boundary

Rollback is limited to the two new ST-07.04 source modules, four bounded source integrations, five exact-source additions, six Story tests, and six completion outputs. It does not mutate the ST-07.02 definition or receipt, authority files, planning baselines, schemas, governance, external repositories, or historical evidence.

No destructive rollback command was required or executed.
