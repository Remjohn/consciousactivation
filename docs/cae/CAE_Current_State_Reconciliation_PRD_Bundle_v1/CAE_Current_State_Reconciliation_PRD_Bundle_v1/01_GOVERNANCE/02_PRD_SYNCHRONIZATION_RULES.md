# PRD Synchronization Rules

`docs/PRD/CURRENT.md` is the canonical PRD surface but is currently marked draft in the repository. The reconciliation program MUST respect that status unless an attributable operator decision changes it.

The current PRD itself states that relevant implementation/specification sessions update the relevant section in the same session and that stale or undated verification must be treated with lower confidence.

## Required PRD operation

The PRD updater must:

1. Read the entire current PRD before editing.
2. Identify sections affected by repository work actually proven in the reconciliation.
3. Update only the sections supported by evidence.
4. Add a fresh `Verified against code: YYYY-MM-DD` line for each section genuinely re-verified in this pass.
5. Preserve superseded recommendations using the repository's existing override/preservation convention rather than silently deleting history.
6. Preserve unresolved defects and decision queues.
7. Update version/change-log metadata consistently with existing PRD conventions.
8. Record the reconciliation evidence source and control-state references.
9. Avoid describing planned work as implemented.
10. Leave unrelated sections untouched unless the reconciliation proves they are factually stale and they belong to this pass's declared status surface.

## PRD completion rule

The PRD is considered synchronized only when an independent verifier can take the reconciliation ledger and trace every material current-state claim in the updated PRD to repository evidence.

The updater must not:

- mark the entire PRD “verified” merely because some sections were checked;
- erase historical findings to make the document shorter;
- convert `CLAIMS_UNVERIFIED`, `BLOCKED`, or `OPERATOR_DECISION_REQUIRED` into success states without proof;
- invent a new requirement because a gap was discovered.
