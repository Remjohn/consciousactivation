# CA-CSR-04 — Final Verification, Freeze & Runtime-Convergence Handoff

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Program: `CAE Current-State Reconciliation & PRD Synchronization`
Atomic boundary: independently verify the synchronized current state and freeze the handoff; do not implement the next program.

## 1. Identity and status

**Mandate ID:** `CA-CSR-04`

**Objective:** Independently prove that the repository evidence, reconciliation ledger, control-state surfaces, and updated PRD agree sufficiently to establish one verified current state.

**Completion state:** `CURRENT_STATE_FROZEN_FOR_NEXT_PROGRAM`

## 2. Decision / objective being authorized

Perform a fresh read-only verification after CA-CSR-03. The verifier must not rely solely on the same claims made by the PRD updater.

## 3. Governing doctrine and authority sources

Mandatory:

- both CAE mandate-authoring/execution skills;
- CA-CSR-01 evidence packet;
- accepted CA-CSR-02 ledger/report;
- updated `docs/PRD/CURRENT.md`;
- current control-state/authority artifacts;
- current repository revision after CA-CSR-03.

## 4. Mandatory reading before action

Read the evidence packet, ledger, updated PRD, and relevant authority records. Then independently sample high-materiality claims directly in the repository and re-run targeted validators.

## 5. Exact scope

Allowed outputs:

`03_FINAL_RECONCILIATION_VERDICT.yaml`
`04_CURRENT_STATE_HANDOFF.md`

and the existing program-control completion record required by repository convention.

No code/runtime/PRD edits are allowed in this mandate unless a specific factual typo in the completion record is required by the verification itself; the updated PRD must be treated as the artifact under verification, not edited here.

## 6. Allowed artifacts and file boundary

Read-only repository verification plus final reconciliation artifacts.

## 7. Prohibitions and collision procedure

Do not “fix” a failed verification inside this mandate. Record the failure and route it back to CA-CSR-02 or CA-CSR-03 as appropriate.

Contrastive failure: a verifier that only checks that the PRD and ledger agree textually, without sampling the underlying code/evidence, is insufficient.

## 8. Required work / implementation behavior

Verify:

1. repository revision and clean/dirty state relevant to claims;
2. PRD version/change-log and verification dates;
3. reconciliation ledger coverage;
4. a representative sample of implemented/partial/blocked/quarantined claims;
5. at least one high-impact recently executed mandate from direct repository evidence;
6. open-defect preservation;
7. no unsupported “implemented” claims;
8. no accidental architecture or ontology additions made by the reconciliation program;
9. the next runtime-convergence frontier is derived from verified gaps, not from stale planning documents.

Produce a concise handoff with:

`VERIFIED_NOW`
`VERIFIED_PARTIAL`
`OPEN_BLOCKERS`
`UNVERIFIED_CLAIMS`
`OPERATOR_DECISIONS_REQUIRED`
`NEXT_RUNTIME_CONVERGENCE_CANDIDATES`

The final section is planning input only; it does not authorize implementation.

## 9. Verification and evidence standard

This mandate must use an independent verifier path from the updater wherever practical. Capture command, environment, source, result, and limitation for each executed check.

The final verdict is one of:

`PASS`
`PASS_WITH_LIMITATIONS`
`BLOCKED`
`FAIL`

## 10. Completion and stop condition

Complete only when the verdict is supported by fresh evidence and the handoff explicitly separates verified fact from next-step proposal.

Stop. No runtime implementation begins under this mandate.

## 11. Rollback / recovery

No product rollback is authorized. If verification fails, leave the failed evidence intact, classify the issue, and return an explicit rework request to the appropriate prior mandate.

## 12. Operator decision

Operator question: **“Do you accept this frozen current-state handoff and authorize a separate runtime-convergence program?”**

## 13. Activation prompt

Gemini: execute `CA-CSR-04` only as an independent final verifier. Read the authoritative mandate authoring and Gemini execution skills, the CA-CSR-01 evidence packet, accepted CA-CSR-02 ledger, updated `docs/PRD/CURRENT.md`, and current program-control authority records. Do not edit code or the PRD. Re-check high-materiality claims directly in the repository and rerun targeted validation where feasible; do not merely compare two documents for textual agreement. Verify repository revision, PRD verification dates, recent mandate execution evidence, implementation versus specification boundaries, open defects, quarantined assets, and the Editorial Intelligence chain. Any unsupported “implemented” claim, stale status, missing evidence, or authority conflict is a failure or limitation, not something to patch silently. Produce a final machine-readable verdict and a human-readable current-state handoff separating VERIFIED_NOW, VERIFIED_PARTIAL, OPEN_BLOCKERS, UNVERIFIED_CLAIMS, OPERATOR_DECISIONS_REQUIRED, and NEXT_RUNTIME_CONVERGENCE_CANDIDATES. The last category is planning input only. Use the governed evidence standard and explicitly record commands, environment, fixtures/data sources, results, and limitations. Stop after the final verdict and ask the operator whether to authorize a separate runtime-convergence program.
 Load `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` and `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` verbatim before verification. They require explicit evidence, independent checking, precise failure classification, operator decision, commit capture, and a hard stop after the mandate. 
