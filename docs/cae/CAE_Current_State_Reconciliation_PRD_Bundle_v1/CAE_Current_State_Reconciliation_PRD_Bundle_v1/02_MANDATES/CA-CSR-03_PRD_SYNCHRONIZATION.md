# CA-CSR-03 — Canonical PRD Synchronization

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Program: `CAE Current-State Reconciliation & PRD Synchronization`
Atomic boundary: synchronize the current PRD from the accepted reconciliation; no runtime or architecture changes.

## 1. Identity and status

**Mandate ID:** `CA-CSR-03`

**Objective:** Update `docs/PRD/CURRENT.md` so its current-state claims accurately reflect the accepted repository evidence.

**Completion state:** `PRD_SYNCHRONIZED_PENDING_FINAL_VERIFICATION`

## 2. Decision / objective being authorized

Turn the accepted reconciliation ledger into a current, traceable PRD state without inventing requirements or claiming implementation beyond evidence.

## 3. Governing doctrine and authority sources

Mandatory:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `01_GOVERNANCE/02_PRD_SYNCHRONIZATION_RULES.md`
- accepted CA-CSR-02 ledger/report
- complete `docs/PRD/CURRENT.md`
- current Tech Specs and control-state records cited by the ledger

The current PRD's own maintenance rule governs PRD edits.

## 4. Mandatory reading before action

Read the complete PRD, not just the sections referenced by the ledger. Locate its current version/change-log conventions, section verification convention, preserved supersession/override patterns, and open-decision structure.

Then trace every proposed change back to CA-CSR-02 evidence.

## 5. Exact scope

Edit only:

`docs/PRD/CURRENT.md`

and the designated reconciliation status record required to record this mandate's completion evidence.

No source code, migration, runtime-state, schema, or canonical-object changes are permitted.

## 6. Allowed artifacts and file boundary

Allowed: `docs/PRD/CURRENT.md` and the reconciliation completion record.

## 7. Prohibitions and collision procedure

Do not rewrite the PRD wholesale. Do not remove historical overrides or preserved superseded guidance. Do not mark an unverified capability complete merely because its mandate exists. Do not turn a hypothesis into a PRD fact.

Contrastive failure: replacing a stale “not implemented” statement with “implemented” because the corresponding Tech Spec and mandate exist, while no executable proof exists, is a false synchronization.

## 8. Required work / implementation behavior

1. Compare PRD claims with the accepted ledger.
2. Update only materially affected sections.
3. Add current verification dates for sections actually checked.
4. Correct stale implementation claims.
5. Add newly verified capabilities only when supported by evidence.
6. Preserve open defects and operator decisions.
7. Preserve historical recommendations using the existing PRD convention.
8. Update version/change-log metadata consistently.
9. Record reconciliation ledger reference and repository revision used.
10. Run a self-check that every changed paragraph has a traceable evidence source.

The target is not “a nicer PRD.” The target is a **truthful PRD**.

## 9. Verification and evidence standard

Required proof:

- exact before/after PRD diff;
- reconciliation ledger reference;
- repository commit hash used;
- verification date for each changed section;
- list of claims intentionally left unverified/blocked;
- no changed implementation claim lacking an evidence source.

## 10. Completion and stop condition

The mandate is complete only when the PRD diff is internally coherent, every changed material claim traces to accepted evidence, history is preserved, and no implementation work occurred outside scope.

Then run the limited documentation-integrity verifier. Do not begin runtime convergence.

## 11. Rollback / recovery

If an edit cannot be supported by the ledger, revert that edit. If PRD conventions conflict with the reconciliation, stop and classify `DOCUMENTATION_CONFLICT` for operator resolution.

## 12. Operator decision

Operator question: **“Do you authorize final verification and closure of the current-state synchronization?”**

## 13. Activation prompt

Gemini: execute `CA-CSR-03` only, using the accepted CA-CSR-02 ledger as the sole factual change basis. Read the current PRD in full and obey its existing maintenance/versioning/supersession conventions. Update only `docs/PRD/CURRENT.md` plus the designated reconciliation completion record. Do not implement code, migrations, runtime behavior, schemas, or new architecture. Correct stale claims, add genuinely verified work, preserve open defects and operator decisions, and preserve historical superseded recommendations instead of deleting them. Every materially changed current-state claim must trace to a specific ledger row and ultimately to repository evidence. Do not turn a mandate file, Tech Spec, receipt, or plan into implementation proof without executable evidence. Record exact repository revision, verification dates, PRD diff, intentionally unresolved claims, and limitations. Run documentation integrity checks after editing. A PRD that is comprehensive but contains unsupported implementation claims is a failed result. Stop after the PRD synchronization is complete and ask the operator to authorize final verification; do not start runtime-convergence work.
 Load `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` and `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` verbatim before editing. Treat them as execution controls and `docs/PRD/CURRENT.md` as the object being synchronized, not as permission to expand the scope. Preserve section-level verification discipline and do not use broad assertions such as “the repository is now complete.” Only evidenced claims belong in the PRD.
