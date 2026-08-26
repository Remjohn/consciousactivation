# Gemini Execution Mandate — Phase 14 / CA-GOV-02

**Status:** `DRAFT — BLOCKED UNTIL CA-AUDIT-01 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-GOV-02`  
**Title:** Formal Ratification and Durable Control-State Reconciliation  
**Execution classification:** Governance-record reconciliation and operator-decision preparation only; no canonical-content, schema, runtime, data, authority, or migration change  
**Required prior decision:** “Accept CA-AUDIT-01 as the authoritative post-execution status record, preserve its limitations and non-claims, and authorize CA-GOV-02 only.”  
**Required completion gate:** `AUDIT -> OPERATOR_REVIEW`; no decision becomes ratified until the operator records it.

## 1. Authority, objective, and decision boundary

CA-GOV-02 is governed by the CAE Governance & Specification Bridge Bundle v3, particularly the Implementation Gate, Phase Promotion and Proof, State and Transition Control, Object-to-Spec Traceability, Test Governance, and Coding Agent State Control protocols. It inherits the completed evidence classification from `CA-AUDIT-01`, all Phase 1–12 mandates and records, and the existing `CAE_IMPLEMENTATION_CONTROL_STATE.md`.

This phase closes a governance problem, not an implementation problem. The repository contains authored constitutional, requirement, state-contract, and implementation artifacts, while some review records still state `PENDING_OPERATOR_RATIFICATION` and the durable control record contains historical decisions alongside later recorded outcomes. These are not interchangeable states:

```text
artifact maturity: DRAFT -> REVIEWED -> OPERATOR_RATIFIED -> SUPERSEDED / RETIRED
implementation:   NOT_IMPLEMENTED -> IMPLEMENTED -> VERIFIED -> REPAIRED
operational authority: LEGACY_ONLY / DUAL_VERIFY -> POSTGRES_AUTHORITATIVE
environment:      LOCAL / STAGING -> PRODUCTION
```

No state on one line implies a state on another. In particular, E3 evidence does not ratify a constitution; an implementation does not silently authorize the specification that it follows; a staging promotion for one aggregate does not establish production authorization; and an operator’s later approval may resolve a particular decision without rewriting the historical fact that it was previously pending.

CA-GOV-02 shall produce a reviewable operator decision packet and an internally consistent durable-control snapshot. It may classify an existing explicit operator decision as `RECORDED_RATIFIED` only when the decision’s source, authority, scope, date, and artifact version are all evidenced. It shall never manufacture, infer, backdate, or generalize an operator decision.

The permitted transition is:

```text
CA-AUDIT-01 accepted
  -> CA-GOV-02 decision preparation and control-state reconciliation
  -> OPERATOR_REVIEW
  -> (operator only) selected governance facts become RATIFIED / DEFERRED / REJECTED
```

`CA-GOV-02` does not authorize `CA-MIG-03`; a separate operator authorization is required after this phase’s decision packet has been accepted.

## 2. Mandatory reading and evidence prerequisites

Before planning, editing, classifying, or validating, Gemini SHALL read in full:

1. The accepted `CAE_POST_EXECUTION_GOVERNANCE_AUDIT.md`, `CAE_GOVERNANCE_STATUS_MATRIX.md`, findings/decisions register, reproducibility log, completion record, and the resulting control-state entry from CA-AUDIT-01.
2. The Phase 1–12 execution program, all mandates, their exact operator questions, all completion/review records, and recorded operator decisions or promotion receipts.
3. CA-CAN-01A/B/C review records and all 15 constitution YAMLs; CA-SPEC-01 PRD/FR records; CA-STATE-01 authority/migration contracts; and CA-TS-01 Gate A–I review/implementation boundary.
4. CA-IMPL-01A/01B/02/02P proof, reconciliation, recovery, and receipt records, including their non-claims and F-01/F-02/F-03 findings.
5. The governing Bundle v3 documents named in Section 1 and `docs/PRD/CURRENT.md`.
6. Git history for the claimed decision and the current working tree. Record the source commit/record accurately; never treat a Git commit message as an operator decision unless the record itself meets the decision evidence rule.

The minimum decision evidence is an attributable operator instruction, approval token, signed/recorded acceptance, or an unambiguous operator statement in the controlled work record. It must identify the precise object/package/aggregate and authorized action. “Continue,” a test command, a code commit, a prior-agent summary, or a generic approval is insufficient to ratify unenumerated canonical content.

CA-GOV-02 may run only local, non-mutating text, Git, checksum, static-validator, and pure-test commands. It SHALL NOT query remote databases, invoke staging/provisioning/cutover/recovery scripts, mutate Git history, inspect or emit secrets, or rely on a live system to settle a governance ambiguity.

## 3. Exact scope and classification rules

This phase covers the governance status—not the semantic correctness—of these defined records:

```text
CA-MAP-01, CA-AUTH-01, CA-CAN-01A/B/C, CA-SPEC-01, CA-STATE-01,
CA-TS-01, CA-IMPL-01A, CA-IMPL-01B, CA-IMPL-02/02P, and CA-AUDIT-01;
their explicitly named constitutions, requirements, state contracts, and
MC-CAE-MED-001 staging authority record.
```

It must also retain explicit deferrals: broad SQLite retirement/migration, SDA/SFL runtime authority, Primitive Registry reconciliation, SemanticProgram, intelligence/orchestration, production routing, client data migration, and E4/operator-taste proof. No deferred domain becomes “out of scope” merely because it is not in this phase’s ratification packet.

The Ratification Register shall have one row for each governance object or coherent decision group and must include:

```text
decision_id | subject/version | current documented status | evidence reference |
decision type | eligible decision owner | proposed disposition |
operator decision record | effective date | supersedes / preserves |
implementation relationship | authority/environment boundary |
open risk | next permitted phase
```

Permitted dispositions are only `RECORDED_RATIFIED`, `PENDING_OPERATOR_RATIFICATION`, `DEFERRED`, `REJECTED`, `SUPERSEDED`, `HISTORICAL_RESOLVED`, `CONTRADICTORY`, and `NOT_APPLICABLE`. An item is `RECORDED_RATIFIED` only when it satisfies Section 2’s evidence rule. If an older pending decision was later resolved, retain the old state as history and link it to `HISTORICAL_RESOLVED`; if it was not resolved, retain it as pending. If the evidence is ambiguous, use `CONTRADICTORY` or `PENDING_OPERATOR_RATIFICATION`, never a convenient conclusion.

The Control-State Reconciliation must divide the durable record into exactly three layers:

```text
CURRENT EXECUTION STATE       — the active package, valid current authority, next gate
HISTORICAL EXECUTION LEDGER   — completed/recorded facts and their supersession links
OPEN GOVERNANCE DECISIONS     — decisions still requiring the named operator authority
```

It must state that `MC-CAE-MED-001` is, at most, `POSTGRES_AUTHORITATIVE_STAGING_ONLY` for the exact approved aggregate and recorded contract; all other authority and production claims remain unchanged unless independently evidenced.

## 4. Authorized artifacts, file boundary, and prohibitions

Gemini MAY create or update only:

- `docs/cae/implementation/CAE_GOV_02_RATIFICATION_REGISTER.md`;
- `docs/cae/implementation/CAE_GOV_02_CONTROL_STATE_RECONCILIATION.md`;
- `docs/cae/implementation/CAE_GOV_02_OPERATOR_DECISION_PACKET.md`;
- `docs/cae/implementation/CAE_GOV_02_GOVERNANCE_TRANSITION_LEDGER.md`;
- `docs/cae/implementation/CAE_GOV_02_COMPLETION_RECORD.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`;
- one read-only validator under `scripts/cae/audit/` and a targeted pure/local test under `tests/cae/` only if they validate the newly authored governance artifacts without database, Storage, network, or source mutation.

The decision packet must quote no secrets or client data. It must give the operator one concise, independently decidable statement per decision ID, followed by: what changes if approved; what does not change; evidence; risks; non-claims; and the next legal phase. It must not bundle ontology ratification, schema repair, operational cutover, and production authorization into one approval.

Gemini SHALL NOT alter constitution YAML, the object map, authoring Skills, PRD/FR content, contracts, Tech Spec, DDL/migrations/RLS, databases, Storage, runtime/services/API, registries, code, old mandates, receipts, or evidence. It may not edit a prior review status simply to make it appear ratified; the register and control-state ledger must carry the status transition. It shall not apply any operator decision itself, mark a new decision `RECORDED_RATIFIED`, widen `MC-CAE-MED-001`, close F-01/F-02/F-03, or remove an open risk.

## 5. Required checks, adversarial review, and failure routes

The Governance Transition Ledger must cite each transition as `from_status -> to_status`, its evidence, its decision owner, and its allowed consequence. It must identify all older control-record fields that were historical, stale, contradictory, or still open. “Current” information must never be hidden among a chronological narrative.

At minimum, perform and record these adversarial checks:

1. Attempt to classify a review document as ratified without an operator decision; the validator must reject it.
2. Attempt to use the CA-IMPL-02 promotion token to ratify all constitutions, requirements, and contracts; the validator must reject it as scope expansion.
3. Attempt to use a later implementation/test as evidence that a pending review was approved; reject it.
4. Attempt to relabel staging authority as production or as all-aggregate PostgreSQL authority; reject it.
5. Attempt to remove a historic pending decision rather than preserving a `HISTORICAL_RESOLVED` link; reject it.
6. Attempt to mark F-01/F-02/F-03 closed without a separately authorized repair and evidence; reject it.
7. Attempt to treat a generic “continue” or agent-authored text as an operator decision; reject it.
8. Attempt to omit any declared deferred CAE domain from the open-decision/deferred ledger; reject it.

If a decision’s owner, scope, artifact version, or evidence is missing, the agent SHALL mark it pending and surface it in the operator packet. If documents assert incompatible present states, mark `CONTRADICTORY`, preserve both source references, and do not choose a winner. If updating the control state would discard history or create ambiguity, stop as `BLOCKED` and request an operator direction; no cosmetic rewrite is allowed.

## 6. Evidence, completion, rollback, and operator gate

The static governance validator must verify decision IDs, complete fields, valid disposition vocabulary, evidence references, owner/next-phase fields, preservation of all known F-01/F-02/F-03 and deferrals, and a single current-state entry. It provides E1 structural proof only; it cannot prove the operator’s intent, production safety, runtime correctness, or remote staging state.

The Completion Record must report:

```text
A. what governance records changed and why
B. which facts were only classified versus formally ratified
C. what evidence was inspected and locally rechecked
D. what E3/runtime claims remain recorded rather than replayed
E. every unresolved decision, contradiction, finding, and deferral
F. what could still be wrong in the control record
G. exact operator inspection paths and decision IDs
H. exact next authorization requested
```

**Rollback:** This phase changes no operational state. If rejected, revert only the CA-GOV-02 documentation/validator commit via a new corrective commit. Never erase historical decisions, promotion receipts, audit findings, or prior wording; supersede an incorrect classification with an attributable correction and retain the evidence trail.

CA-GOV-02 reaches `OPERATOR_REVIEW` only when all allowed artifacts exist; local validation passes; every current, historical, and open control-state field is unambiguous; no claim has been upgraded without evidence; and the decision packet contains separately decidable IDs. The agent shall commit scope-only files, record the commit, request the exact decision below, and stop.

Gemini SHALL request exactly:

> **Approve the CA-GOV-02 Ratification Register and Control-State Reconciliation: record only the decision IDs explicitly approved in the attached operator packet as ratified, retain every other item as pending/deferred/contradictory exactly as listed, preserve all F-01/F-02/F-03 and non-claims, and authorize CA-MIG-03 only to design and rehearse safe forward-only migrations—without applying a migration or changing operational authority?**

## 7. Gemini activation prompt (approximately 260 words)

You are the CAE governed execution agent for `CA-GOV-02 — Formal Ratification and Durable Control-State Reconciliation`. This mandate is blocked unless CA-AUDIT-01 is explicitly accepted. Read this mandate, the complete CA-AUDIT-01 record, all Phase 1–12 mandates/reviews/proofs, the constitutions/specification/contracts, current control state, and relevant Bundle v3 protocols before planning or editing.

Your authority is only to prepare governance records and a precise operator decision packet. Create the Ratification Register, control-state reconciliation, transition ledger, completion record, optional read-only validator, and the specified control-state update. Do not change constitutional content or declare a decision ratified merely because code, a validator, a receipt, or a later phase exists.

Keep four axes independent: artifact ratification, implementation verification, operational authority, and environment. An E3 record does not ratify a constitution. `MC-CAE-MED-001` is not broad PostgreSQL authority or production authorization. Preserve all historical pending states through explicit disposition links; do not delete them to make the record cleaner. When evidence has no attributable operator decision, mark it pending. When two documents materially disagree, mark them contradictory and surface both; never choose silently.

Run local, non-mutating artifact/Git/static checks only. Do not call Supabase, use credentials, run staging scripts, modify SQL/RLS/migrations/runtime/registries, alter earlier mandates, apply a decision, or close F-01/F-02/F-03. Test against false proofs: test success as ratification, one approval generalized across scopes, staging called production, history erased, generic instruction called approval, and unmentioned deferrals dropped.

Commit only allowed governance artifacts, request the exact Section 6 decision with separately decidable IDs, and stop. Do not begin CA-MIG-03, repair anything, or change authority.
