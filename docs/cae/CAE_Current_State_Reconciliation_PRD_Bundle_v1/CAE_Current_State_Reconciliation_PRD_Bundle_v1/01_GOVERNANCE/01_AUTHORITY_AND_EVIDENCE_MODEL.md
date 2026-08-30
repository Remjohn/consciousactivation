# Authority & Evidence Model

## Authority axes

Every material statement in the reconciliation must distinguish:

- **Definition authority** — the artifact that defines what something means.
- **Runtime authority** — the verified code/database/state representation that actually governs execution.
- **Change/promotion authority** — the actor/process allowed to alter or promote it.

Presence in the repository never grants authority by itself.

## Evidence classes

Use these labels exactly where applicable:

`EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `RECEIPT`, `RUNTIME`, `HYPOTHESIS`, `OPERATOR_DECISION_REQUIRED`.

A document saying “implemented” is `DOCUMENT`, not `EXECUTABLE` proof.
A test that was not actually run in the current environment is not current `TEST` evidence.
A prior receipt proves only the claim and environment captured by that receipt; it does not automatically prove present repository state.

## Status vocabulary

Use explicit statuses, not vague prose:

- `VERIFIED_IMPLEMENTED`
- `VERIFIED_PARTIAL`
- `SPECIFIED_NOT_IMPLEMENTED`
- `CLAIMED_UNVERIFIED`
- `BLOCKED`
- `QUARANTINED`
- `SUPERSEDED`
- `ARCHIVED`
- `NOT_FOUND`
- `OPERATOR_DECISION_REQUIRED`
- `NOT_APPLICABLE`

## Conflict handling

When documentation, code, tests, receipts, or control-state records disagree:

1. Preserve both claims.
2. Identify the source of each claim.
3. Identify the authority axis involved.
4. Prefer current executable evidence for runtime truth, unless a governing authority explicitly says otherwise.
5. Route unresolved authority conflicts to `OPERATOR_DECISION_REQUIRED`.
6. Do not delete or silently rewrite the losing artifact inside this reconciliation.

## Current-state rule

The goal is not to make every artifact agree by editing everything until the repository looks clean.

The goal is to make the **canonical status surface** accurately describe the repository while preserving unresolved contradictions as explicit records.
