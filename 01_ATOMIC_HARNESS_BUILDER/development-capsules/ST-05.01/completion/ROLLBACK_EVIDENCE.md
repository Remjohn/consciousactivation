# ST-05.01 Rollback Evidence

## Verdict

`PASS` — both transactional rollback and governed lifecycle invalidation were demonstrated without destructive mutation.

## Injected transaction failure

`test_ac_10_injected_atomic_failure_leaves_zero_partial_state_then_retry_succeeds` injects the repository's next atomic-commit failure at the single ST-05.01 write boundary. After the failure:

- the run event count is unchanged;
- no skill-registry snapshot exists;
- no consumption receipt exists;
- no command record exists;
- no run snapshot reference exists;
- removing the injected fault permits the same deterministic command to commit successfully.

This proves that validation and object construction do not leak partial repository state.

## Governed upstream invalidation

`test_ac_09_upstream_reopen_invalidates_snapshot_and_preserves_history` completes the entire Builder Core chain through ST-05.01, then reopens the authoritative atomic boundary. The repository commits one ordered eleven-event descendant invalidation chain. `SkillRegistrySnapshotInvalidated` follows `MinimumContextInvalidated`, the active snapshot becomes unavailable, and the historical snapshot's canonical bytes remain byte-identical and independently retrievable.

The source registry fixture, policy, schema, governance receipt, predecessor artifacts, and original snapshot bytes are never mutated.

## Source rollback boundary

If this Story must be reverted, remove only the two ST-05.01 source modules and six Story test files, revert the four allowed integration source changes and five exact-source-set test entries, and remove the six ST-05.01 completion artifacts. No governance file, schema, predecessor receipt, planning baseline, external repository, or historical event is part of the rollback set.

## Evidence

- Story failure and retry suite: `PASS`
- descendant invalidation and history suite: `PASS`
- run replay/state-hash equality: `PASS`
- full regression after implementation: `380/380 PASS`
- prohibited destructive rollback behavior: none

verdict: `PASS`
