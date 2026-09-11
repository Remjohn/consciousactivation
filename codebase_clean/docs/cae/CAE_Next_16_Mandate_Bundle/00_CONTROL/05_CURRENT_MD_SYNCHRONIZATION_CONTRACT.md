# CURRENT.md Synchronization Contract — M49–M64

`docs/PRD/CURRENT.md` is the canonical PRD current-state authority.

Affected local status files (for example `CURRENT_PROJECT_STATUS.md`) are secondary implementation-context records and must remain consistent with the canonical PRD without becoming competing authority.

Every mandate execution must record:

- exact verification date/time;
- mandate ID and title;
- current commit SHA;
- implementation truth changed;
- tests run and exact results;
- runtime verification status;
- remaining gaps;
- operator decision;
- next-phase authority.

Every phase-close mandate MUST update `docs/PRD/CURRENT.md` and affected local current-state files in the same session.

Do not append contradictory history into current-state files. Replace stale active claims; preserve historical claims only where the document's change-log design requires them.

A mandate is not complete merely because the code or bundle exists. Current-state wording must distinguish:

`DOCUMENTED` != `CODE_EXISTS` != `TEST_VERIFIED` != `RUNTIME_VERIFIED` != `OPERATOR_ACCEPTED`.
