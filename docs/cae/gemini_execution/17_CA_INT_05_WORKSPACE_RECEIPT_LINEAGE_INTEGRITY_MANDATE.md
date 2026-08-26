# Gemini Execution Mandate — Phase 17 / CA-INT-05

**Status:** `DRAFT — BLOCKED UNTIL CA-APPLY-04 OPERATOR ACCEPTANCE AND A NEW DISPOSABLE-TARGET ADMISSION`  
**Phase ID:** `CA-INT-05`  
**Title:** F-01 Workspace/Receipt Evidence-Lineage Integrity Repair and Proof  
**Execution classification:** One approved structural integrity repair in a new isolated disposable PostgreSQL environment; no F-02 topology repair, shared staging, runtime cutover, data migration, or authority change  
**Required prior decision:** “Accept CA-APPLY-04 and authorize CA-INT-05 only to implement and prove the F-01 workspace/receipt lineage repair in a named disposable target.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; only a later explicit decision may admit the repair to shared staging.

## 1. Authority, objective, and exact defect

CA-INT-05 is governed by the CAE Governance & Specification Bridge Bundle v3; accepted CA-AUDIT-01, CA-GOV-02, CA-MIG-03, and CA-APPLY-04 records; the current control state; `TS-CAE-TEN-001`; and the CA-STATE/constitution rules governing Workspace, Receipt, Immutable Evidence, and ReceiptEvidenceLink. It acts only on finding F-01.

F-01 is the verified schema-fidelity limitation that `cae.receipt_evidence_link.receipt_id` is protected by a global single-column foreign key to `cae.receipt(receipt_id)`, while the link itself also has `workspace_id`. A raw SQL writer that can bypass application-path discipline could create a link carrying Workspace B with a receipt belonging to Workspace A. Existing typed-operation discipline, RLS, parity detection, and repair were compensating controls; they were not structural rejection of that invalid relationship.

The sole objective is to design, apply, and prove a forward-only schema repair that makes an attempted cross-Workspace `(workspace_id, receipt_id)` lineage link fail at the database constraint layer before a row exists. The expected direction is a composite parent candidate key and matching child foreign key, but the agent must inspect the actual approved draft/schema before selecting exact constraint names or SQL. It must not assume that a textual proposal is compatible with a real schema.

The only permitted status change is:

```text
F-01: OPEN_SCHEMA_FIDELITY_LIMITATION
  -> REPAIRED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY

shared staging / production F-01 status:
unchanged
```

This phase does not remedy F-02, solve table-family duality, alter receipt semantics, add a new evidence model, grant broad PostgreSQL authority, or change `MC-CAE-MED-001`’s staging-only authority record.

## 2. Mandatory reading and target admission

Before planning, editing, connecting, or running a migration, Gemini SHALL read in full:

1. F-01 evidence in CA-AUDIT-01, CA-GOV-02, CA-MIG-03, CA-APPLY-04, the current control state, and `CAE_CA_IMPL_02_MC_CAE_MED_001_CUTOVER_PROOF.md`.
2. The exact CA-MIG-03 forward migration drafts/manifests, CA-APPLY-04 application proof, schema inventory, dependency graph, migration runner, static guards, and teardown record.
3. Current first-slice DDL/model/runtime operation source and the constitutions/contracts for Receipt, Evidence, ReceiptEvidenceLink, Workspace, and tenancy/RLS behavior.
4. `TS-CAE-TEN-001` and all applicable v3 state, PostgreSQL, semantic-operation, test-governance, evidence, and promotion protocols.
5. Existing repository migration conventions and all relevant `AGENTS.md` instructions.

The agent must obtain a **new admission record** for a named `DISPOSABLE_POSTGRESQL_ONLY` target. It may not reuse CA-APPLY-04’s target without proving its teardown/recreation and clean synthetic state. Admission must prove the target is not current CAE staging/production, contains no client/Guest/media/receipt/registry data, can be recreated or safely discarded, and is guarded by endpoint/project/database identity checks. It must record exact baseline migration IDs/checksums and the F-01 repair draft checksum.

If any precondition is unknown—especially existing receipt/link rows, constraint names, parent key compatibility, target identity, ownership/privilege model, RLS behavior, or recovery path—stop as `BLOCKED`. Do not modify an existing shared environment, guess a constraint name, or use the current staging project as a fallback.

## 3. Exact authorized scope and repair law

The only permitted schema delta is the minimum forward-only repair necessary to bind a receipt-evidence link’s `workspace_id` and `receipt_id` to one matching receipt parent pair. A valid solution must be enforceable by PostgreSQL, not merely a typed runtime validation, trigger that repairs after insertion, parity sweep, report, or UI/API convention.

The future repair migration must, at minimum:

```text
1. declare exact preconditions for the existing receipt/link relation and data;
2. establish a legally referenceable parent key for the pair if PostgreSQL requires it;
3. replace only the inadequate child receipt reference with a composite relationship;
4. retain Workspace containment and receipt immutability;
5. verify existing data compatibility before an actual future shared-environment apply;
6. provide a forward repair/recovery route without destructive bootstrap, deletion, or source retirement.
```

The agent may create a new versioned migration draft and its explicitly scoped runner/test only under the established migration convention identified by CA-MIG-03. The manifest must state `F01_REPAIR_DISPOSABLE_PROOF_ONLY`, immutable ID/checksum, dependency on the foundation migration IDs, preflight queries to be executed only inside the approved disposable target, expected constraints, failure behavior, and later shared-staging no-go conditions.

The following are prohibited: changing any table unrelated to the minimum parent/child relationship; adding columns or data transformations unless a previously unknown precondition makes the repair impossible, in which case stop; weakening RLS/grants/triggers; deleting/recreating `cae.*`; using a global receipt ID as an excuse to omit Workspace parity; changing typed operations to hide schema failure; repairing, renaming, or selecting the F-02 table family; using live or client data; or recording shared-staging/production authority.

## 4. Execution sequence and evidence requirements

The agent shall perform only these stages in the named disposable target:

1. **Admission and baseline.** Verify identity, clean/synthetic data class, foundation migration version, target schema, constraints, RLS/triggers, repair-draft checksum, and teardown route. Capture non-secret baseline schema metadata.
2. **Preflight.** Evaluate the repair’s exact compatibility checks. If a pre-existing cross-Workspace link or incompatible key exists, do not silently repair it; quarantine the condition and stop unless the approved manifest defines a non-destructive synthetic-only route.
3. **Apply.** Execute the single F-01 forward migration using the guarded runner. Capture migration result, schema delta, and history/checksum evidence. No normal runtime traffic is permitted.
4. **Independent structure inspection.** Prove the required parent candidate key and the composite child foreign key exist, reference the intended columns in the intended order, and coexist with RLS and append-only receipt control. A migration history row is not sufficient.
5. **Direct integrity countertest.** Create two synthetic Workspaces and one synthetic receipt belonging to Workspace A. Attempt a direct SQL insert of a receipt-evidence link labelled Workspace B but using A’s receipt ID. The database must reject the insert through the named structural constraint and leave no child row. This test must execute under a controlled proof role/path that can reach the constraint; it may not pass merely because application validation, RLS concealment, or a typed operation blocked it first.
6. **Positive-path countercheck.** Insert the matching Workspace A link under the same structural path and prove it succeeds, subject to applicable legitimate constraints. Confirm receipt UPDATE and DELETE remain rejected and that Workspace isolation/RLS is not weakened.
7. **Replay/failure proof.** Re-run migration/preflight safely, test altered checksum rejection, and induce one approved failure to prove no false migration-history record or partial unaccounted constraint state exists.
8. **Teardown.** Remove only run-prefixed synthetic fixtures or recreate/destroy the disposable target through the admitted route. Capture a non-secret teardown receipt and deny target reuse if cleanup is uncertain.

## 5. Adversarial checks, hard stops, and non-claims

At minimum, the proof must detect and reject:

1. a direct cross-Workspace link with an existing global receipt ID;
2. a child composite FK that points to the wrong parent columns/order or uses an unconstrained parent pair;
3. a repair that succeeds only because RLS blocks visibility rather than because the database reports the intended integrity constraint;
4. a trigger, parity sweep, or typed validation substituted for the requested foreign-key enforcement;
5. a migration that deletes/rebuilds receipt or link tables, changes existing receipt IDs, or uses destructive `CASCADE`;
6. missing/disabled receipt append-only trigger or weakened Workspace RLS after apply;
7. an altered repair draft/checksum or omitted predecessor migration;
8. an existing incompatible/cross-scope synthetic relation silently coerced, corrected, or hidden;
9. repeat execution that creates duplicate constraints/history or changes data;
10. positive valid Workspace-local linkage being incorrectly rejected;
11. cleanup that could remove unscoped/shared data.

Stop as `BLOCKED`, `REPAIR_REQUIRED`, or `SCOPE_VIOLATION` if the actual schema cannot support the minimum composite relation without an unapproved broader topology decision; the preflight finds non-synthetic data; F-02 becomes implicated; RLS/trigger behavior changes; constraint failure cannot be independently attributed; a failure leaves ambiguity; or teardown cannot be proven. Preserve evidence and do not improvise a trigger, data rewrite, or table recreation.

This proof does not establish a shared-staging repair, production safety, full media/evidence cutover correctness, source retirement, broad PostgreSQL authority, F-02 resolution, or an E4/taste result.

## 6. Artifacts, completion, rollback, and operator gate

Gemini MAY create/update only the exact versioned F-01 migration draft/manifest/guarded runner approved by the migration convention plus:

- `docs/cae/implementation/CAE_INT_05_F01_ADMISSION_RECORD.md`;
- `docs/cae/implementation/CAE_INT_05_F01_SCHEMA_REPAIR_PROOF.md`;
- `docs/cae/implementation/CAE_INT_05_F01_ADVERSARIAL_RESULTS.md`;
- `docs/cae/implementation/CAE_INT_05_F01_RECOVERY_AND_TEARDOWN.md`;
- `docs/cae/implementation/CAE_INT_05_COMPLETION_RECORD.md`;
- scoped scripts/tests under the approved migration/implementation and `tests/cae/` locations;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

CA-INT-05 completes only when all admission, preflight, migration application, independent constraint inspection, direct negative and positive structural tests, replay/failure proof, and teardown evidence pass. The control state must report `F01_REPAIRED_AND_E3_PROVEN_DISPOSABLE_ONLY`, preserve `F02_OPEN`, and make no shared authority claim.

**Rollback/recovery:** The repair is tested only in a disposable target. The recovery route is target recreation or an approved forward compensating migration; never destructive bootstrap or deletion of durable records. If the repair has been applied but structure/proof fails, retain the target for inspection, mark it contaminated, and do not reuse it. There is no authorization to roll this change into shared staging.

Gemini SHALL request exactly:

> **Accept CA-INT-05 as disposable-environment proof that F-01 is structurally rejected by the exact approved forward migration, preserve F-02 and all shared-staging/production limitations, and authorize CA-TOPO-06 only to reconcile and prove the WP-03 versus CA-IMPL table-family topology—without applying F-01 to shared staging or changing operational authority?**

It SHALL stop after this question.

## 7. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-INT-05 — F-01 Workspace/Receipt Evidence-Lineage Integrity Repair and Proof`. This mandate is blocked until CA-APPLY-04 is accepted, the exact F-01 draft scope is authorized, and a newly admitted disposable PostgreSQL target is verified. Read the mandate, all audit/governance/migration/application evidence, F-01/F-02 records, current DDL/models, contracts/constitutions, runner, and relevant instructions before planning or connecting.

Your authority is exactly one structural repair: make a receipt-evidence link carrying `(workspace_id, receipt_id)` reference the matching receipt parent pair at the PostgreSQL constraint layer. Inspect the actual schema first; do not assume constraint names or compatibility. Use a forward-only draft with checksum, predecessor, preflight, guarded runner, failure route, and later shared-staging no-go conditions. Do not use a trigger, parity sweep, typed operation, RLS denial, or application validation as a substitute for structural enforcement.

Apply only in the new disposable target after proving it is not shared staging/production and contains no client data. Verify the parent candidate key, composite child FK, RLS, and receipt immutability independently. Under a controlled proof role that reaches the constraint, create two synthetic Workspaces and a receipt in A, then attempt the direct B-to-A link. It must fail by the intended database constraint and create no row. Also prove an A-to-A link succeeds and existing RLS/append-only controls remain intact.

Reject destructive/rebuilding SQL, altered checksums, wrong column order, incompatible existing state, duplicate replay, silent coercion, F-02 scope expansion, and uncertain teardown. Never touch shared staging, production, Storage, SQLite, client/registry data, typed runtime behavior, or authority. Record E3 proof as disposable only, commit only allowed artifacts, ask the exact Section 6 decision, and stop.
