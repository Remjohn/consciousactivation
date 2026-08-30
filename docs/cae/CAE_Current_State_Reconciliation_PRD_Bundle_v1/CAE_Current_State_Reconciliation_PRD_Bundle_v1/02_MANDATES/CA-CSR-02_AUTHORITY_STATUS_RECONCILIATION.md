# CA-CSR-02 — Authority & Status Reconciliation

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Program: `CAE Current-State Reconciliation & PRD Synchronization`
Atomic boundary: convert verified evidence into one reconciled current-state model; do not update the PRD.

## 1. Identity and status

**Mandate ID:** `CA-CSR-02`

**Objective:** Reconcile repository evidence into one current-state ledger that distinguishes authority, implementation, proof, supersession, quarantine, blockage, and unresolved decision.

**Completion state:** `CURRENT_STATE_RECONCILED`

## 2. Decision / objective being authorized

Determine the repository's actual present state using CA-CSR-01 evidence plus targeted re-checks. This is the authoritative analytical pass that decides how existing artifacts relate for status purposes. It may classify overlap, but it must not delete or structurally merge artifacts.

## 3. Governing doctrine and authority sources

Read:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- CA-CSR-01 evidence packet
- `docs/PRD/CURRENT.md`
- `governance/program-control/03_PROGRAM_STATUS/MASTER_STATUS.md`
- `governance/program-control/03_PROGRAM_STATUS/STATUS_TRUTH_RECONCILIATION.yaml`
- `governance/program-control/03_PROGRAM_STATUS/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml`
- `docs/cae/editorial_intelligence/`
- current Tech Specs / object constitutions / mandate bundle
- relevant `.zcode/plans/`

## 4. Mandatory reading before action

Read the full CA-CSR-01 packet. Then independently re-check high-materiality items in code. At minimum inspect:

- canonical PRD and its change log/verification lines;
- control-plane status records;
- Editorial Intelligence authority/dependency/object register;
- existing Interview Composer boundaries;
- current PostgreSQL/migration/runtime authority references;
- evidence-to-AIR and other proven vertical slices;
- mandate execution evidence and recent plan/receipt records;
- open blockers and quarantine records.

## 5. Exact scope

Produce/update only the designated reconciliation record:

`governance/program-control/03_PROGRAM_STATUS/RECONCILIATION_2026-08-30/01_CURRENT_STATE_LEDGER.yaml`

and its human-readable companion:

`02_CURRENT_STATE_REPORT.md`

If the directory already exists under another current reconciliation operation, reuse the authoritative location rather than creating a competing status system.

## 6. Allowed artifacts and file boundary

Allowed: reconciliation ledger/report only.

Prohibited: PRD, source code, migrations, runtime state, canonical registries, product UI, and deletion of historical artifacts.

## 7. Prohibitions and collision procedure

Never resolve an authority conflict by silently picking the nicer document. Preserve both sides and classify the conflict.

Do not call an artifact redundant merely because it has similar nouns. Record `POSSIBLE_OVERLAP` unless the authority and lifecycle analysis proves equivalence.

Contrastive failure: two documents describe the same capability, but one is the current implementation authority and the other is a historical plan. Calling that “duplicate” and deleting one would be incorrect.

## 8. Required work / implementation behavior

Build a matrix at minimum covering:

`artifact | owner | authority_axis | class/plane | implementation_status | proof_status | supersession_status | quarantine_status | source_refs | dependency_refs | current_PRD_claim | reconciliation_verdict | next_action`

Reconcile at least:

1. CAE constitution/control plane.
2. PRD state.
3. Tech Spec state.
4. PostgreSQL/state/typed-operation foundation.
5. evidence/receipt first slices.
6. Interview Composer and Interview Expression boundaries.
7. Editorial Intelligence object/dependency chain.
8. SDA/SFL/Primitive registry and quarantine status.
9. World/Audience/Guest/Collision/Interview stages.
10. downstream editorial/prod stages.
11. mandate execution records.
12. open blockers/decisions.

For each recently “executed” mandate, distinguish:

`MANDATE_DOCUMENTED`, `CODE_CHANGED`, `TEST_VERIFIED`, `RUNTIME_VERIFIED`, `OPERATOR_ACCEPTED`.

Do not collapse these states.

## 9. Verification and evidence standard

Independent verifier must be able to reproduce every `VERIFIED_*` row from the recorded source path/command/test/receipt. Any unresolved contradiction becomes a named reconciliation issue.

False-proof countercase: a mandate has a completion receipt but no corresponding current code/test/commit. Classify it `CLAIMED_UNVERIFIED`, not complete.

## 10. Completion and stop condition

Complete only when every high-materiality subsystem has one reconciliation verdict and all unresolved conflicts have an owner/next action.

Do not update `docs/PRD/CURRENT.md`.

## 11. Rollback / recovery

Reconciliation artifacts are append/update within their designated status surface. If analysis reveals an authority conflict, preserve it and stop that branch; do not alter the contested artifact.

## 12. Operator decision

Operator question: **“Do you accept this as the evidence-backed current-state ledger for PRD synchronization?”**

## 13. Activation prompt

Gemini: execute `CA-CSR-02` only, after receiving an accepted CA-CSR-01 evidence base. Read the two authoritative mandate skills and every source named in this mandate before acting. Reconcile, do not redesign. Independently re-check the highest-materiality implementation claims directly in code, tests, migrations, runtime contracts, receipts, control-state records, and the current Editorial Intelligence authorities. Produce one current-state ledger and report that distinguish definition authority, runtime authority, and change/promotion authority. For every major mandate or feature, separate what is documented, what code exists, what tests actually passed, what runtime evidence exists, and whether an operator accepted it. Preserve contradictions rather than normalizing them. “Duplicate-looking” artifacts must remain unless equivalence and authority are actually proven; historical/superseded documents are not deletions. Explicitly reconcile the CAE editorial chain, Interview Composer boundary, evidence slices, PostgreSQL/state foundation, Editorial Intelligence objects, registry quarantine, open blockers, and mandate execution records. Use explicit statuses such as VERIFIED_IMPLEMENTED, VERIFIED_PARTIAL, SPECIFIED_NOT_IMPLEMENTED, CLAIMED_UNVERIFIED, BLOCKED, QUARANTINED, SUPERSEDED, ARCHIVED, NOT_FOUND, or OPERATOR_DECISION_REQUIRED. A receipt without current implementation proof is not implementation proof. Leave a machine-readable ledger and human-readable report. Do not edit the PRD. Stop and ask the operator whether this ledger is accepted for PRD synchronization.
 Load `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` and `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` verbatim. Their evidence, scope, authority, stop, and failure rules apply to this reconciliation. The accepted evidence packet is an input, not an authority override. 
