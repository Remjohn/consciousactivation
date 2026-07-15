# Failure, rollback, and cleanup plan

The implementation is additive and must leave the original Format 02 path usable throughout.

Failure behavior:

- Reject an unpinned, malformed, drifted, production-eligible, category-registered, or wrong-target fixture before creating a run.
- Reject any registry other than the exact approved empty registry.
- Reject undeclared skills, dynamic discovery, unauthorized actors, invalid transitions, duplicate non-idempotent commands, and prohibited external integration before state mutation.
- Emit typed failure evidence without a success transition or success event.
- Stop the implementation if it needs an unlisted file, dependency, schema, contract, or authority change.

Rollback demonstration:

1. Remove the new synthetic repository adapter and its export.
2. Revert only the additive generalization in `target_profile.py` to its pre-branch hash.
3. Remove the branch test directory and completion evidence.
4. Run the unchanged original `ST-01.01` suite and full regression suite.
5. Prove the original completion receipt hash is unchanged and the Format 02 path retains its pre-branch behavior.

No data migration is permitted. Test-created runs and events must use isolated temporary stores and be deleted after the test. Rollback must not modify governance, planning, contracts, the original capsule, or external repositories.
