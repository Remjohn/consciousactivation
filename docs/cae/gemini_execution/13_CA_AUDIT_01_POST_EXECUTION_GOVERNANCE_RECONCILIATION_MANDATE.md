# Gemini Execution Mandate — Phase 13 / CA-AUDIT-01

**Status:** `DRAFT — REQUIRES EXPLICIT OPERATOR AUTHORIZATION`  
**Phase ID:** `CA-AUDIT-01`  
**Title:** Post-Execution Governance, Evidence, and Reality Reconciliation  
**Execution classification:** Read-led, evidence-classification and durable-control reconciliation only; no runtime, database, Storage, service, registry, or migration repair  
**Required prior fact:** The Phase 1–12 program has produced documented implementation and a staging-only, one-aggregate promotion record for `MC-CAE-MED-001`; this mandate does not itself accept, broaden, or reverse that record.  
**Required completion gate:** `AUDIT -> OPERATOR_REVIEW`; only the operator may authorize `CA-GOV-02`.

## 1. Authority, purpose, and governing distinction

This mandate is governed by the CAE Governance & Specification Bridge Bundle v3, especially its implementation gate, state/transition control, PostgreSQL authority, semantic-operation, test-governance, reality-contact, and phase-promotion protocols. It also inherits the bounded-execution rules in `docs/cae/gemini_execution/00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md` and all accepted or recorded Phase 1–12 artifacts.

CA-AUDIT-01 exists because successful implementation, a passing static validator, an execution proof, operator ratification, authority promotion, and production readiness are different facts. A later implementation artifact must not silently convert an earlier document marked `PENDING_OPERATOR_RATIFICATION` into an approved constitutional definition. Conversely, a historical pending decision must not remain presented as a current blocker after a later, specific operator decision has resolved it.

The goal is one durable, evidence-led answer to the following question:

```text
For each claimed CAE capability or governance fact:
what was authored, ratified, implemented, independently verified,
promoted, staging-only, production-authorized, deferred, or contradicted?
```

This is an audit and reconciliation phase, not a repair phase. It may identify and classify `F-01`, `F-02`, `F-03`, a non-reproducible verifier, stale control-state statements, or missing ratification; it shall not fix them. It must preserve historical evidence and distinguish it from the current durable execution state.

The only permitted high-level transition is:

```text
CA-IMPL-02/02P recorded outcome
  -> CA-AUDIT-01 evidence reconciliation
  -> OPERATOR_REVIEW
  -> (only by operator decision) CA-GOV-02
```

No aggregate authority transition, source retirement, migration, or production transition is authorized.

## 2. Mandatory reading and inspection before action

Before planning, editing, validating, or describing a phase outcome, Gemini SHALL read in full:

1. `CAE_IMPLEMENTATION_CONTROL_STATE.md`, `CAE_WP00_TO_WP09_REVIEW_EVIDENCE_HANDOFF.md`, and all Phase 10–12 proof, reconciliation, recovery, and promotion artifacts.
2. The complete Phase 1–12 execution program and the twelve prior mandates, including their operator questions and stated non-claims.
3. `CAE_CA_CAN_01A_CONSTITUTION_REVIEW.md`, `CAE_CA_CAN_01B_CONSTITUTION_REVIEW.md`, CA-CAN-01C records, CA-SPEC-01, CA-STATE-01, and CA-TS-01 review/completion records.
4. The current implementation files, local CAE tests, static validators, DDL/scaffolding source, and verifier source cited by a claim. A proof document alone is never sufficient to classify runtime implementation.
5. The Git log and commit/file boundary for Phase 1–12 artifacts. Record consolidated commits as consolidated; do not invent phase-level commits that do not exist.
6. The relevant v3 Bundle protocols and current `docs/PRD/CURRENT.md` truth record.

The agent SHALL inspect current source without changing it. It may run local, non-mutating commands such as static validators, targeted `pytest`, checksum calculation, Git inspection, and text/schema inspection. It SHALL NOT execute a script merely because it is called a “verifier.” A verifier that creates fixtures, uploads/deletes Storage objects, performs database writes, cleanup, migration, provisioning, or remote state queries is write-capable and is prohibited in CA-AUDIT-01.

Secrets, connection strings, passwords, signed URLs, Guest data, workspace identifiers, and real evidence bytes must never appear in any artifact, command output, commit, or report. An unavailable or network-blocked environment is a reproducibility limitation, not evidence that a documented proof never happened.

## 3. Exact scope, evidence model, and classification law

CA-AUDIT-01 SHALL cover only the evidence and governance status of:

```text
Phase 1–12 outputs;
the tenant / Guest / media / evidence / harness / receipt first slice;
the recorded MC-CAE-MED-001 staging authority promotion;
the named F-01, F-02, and F-03 findings;
and the explicit deferrals for SQLite migration, SDA/SFL runtime authority,
SemanticProgram, semantic intelligence, production routing, and E4/taste proof.
```

It SHALL NOT newly audit or implement broader CAE concepts, select another aggregate, decide SDA/SFL canonical authority, import data, or infer a client/data migration plan.

Every claim in the Status Matrix must have an exact evidence reference and use all of these independent fields:

```text
claim_id | domain | claim | evidence reference | evidence class |
verification fidelity | environment class | reproducible now |
ratification state | implementation state | authority state |
scope / non-claim | contradiction or finding | owner / next decision
```

Permitted evidence classes are `EXECUTABLE_SOURCE`, `SCHEMA_OR_MIGRATION`, `LOCAL_TEST`, `STATIC_VALIDATOR`, `STAGING_E3_TRANSCRIPT`, `IMMUTABLE_RECEIPT`, `OPERATOR_DECISION`, `DOCUMENT_ONLY`, `HISTORICAL_RECORD`, `ENVIRONMENT_BLOCKED`, `HYPOTHESIS`, and `CONTRADICTION`.

Use the following terms precisely:

- **AUTHORED** means a versioned artifact exists; it does not establish runtime behavior or ratification.
- **RATIFIED** requires an explicit, attributable operator decision. A review state, later implementation, or successful test is not ratification.
- **IMPLEMENTED** requires current executable source, schema, or runtime configuration evidence.
- **VERIFIED_LOCAL** requires a recorded local test/validator plus the actual behavior and limits it exercises.
- **VERIFIED_E3_RECORDED** means an existing staging proof/receipt is present and internally traceable; it is not `REPRODUCED_NOW` unless CA-AUDIT-01 reruns a non-mutating equivalent, which this mandate does not authorize if it touches remote state.
- **POSTGRES_AUTHORITATIVE_STAGING_ONLY** applies only to the exact aggregate, contract version, environment, and operator decision evidenced in the record.
- **PRODUCTION_AUTHORIZED** requires an explicit production decision and proof. It must remain `NO` unless such evidence exists.
- **DEFERRED**, **QUARANTINED**, **BLOCKED**, and **CONTRADICTION** must name the reason, owner, and reopening condition.

Historical text in the control file may remain as history, but it must be labeled `HISTORICAL_SUPERSEDED`, `RESOLVED_BY`, `STILL_OPEN`, or `CONTRADICTORY`. The agent may never silently delete an inconvenient historical claim or rewrite a prior decision.

## 4. Authorized artifacts and prohibited actions

Gemini MAY create or update only:

- `docs/cae/implementation/CAE_POST_EXECUTION_GOVERNANCE_AUDIT.md`;
- `docs/cae/implementation/CAE_GOVERNANCE_STATUS_MATRIX.md`;
- `docs/cae/implementation/CAE_AUDIT_01_FINDINGS_AND_DECISIONS_REGISTER.md`;
- `docs/cae/implementation/CAE_AUDIT_01_EVIDENCE_REPRODUCIBILITY_LOG.md`;
- `docs/cae/implementation/CAE_AUDIT_01_COMPLETION_RECORD.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`;
- one read-only static validator under `scripts/cae/audit/`, and a targeted pure/local test under `tests/cae/` only when it validates the audit artifact structure without database, Storage, network, or runtime mutation.

The control state update must retain the current recorded cutover/promotion evidence but set the current phase to `CA-AUDIT-01`, record `AUDIT` as the active stage, list prior unresolved statements by disposition, and state that no operational authority changed during this phase.

Gemini SHALL NOT modify DDL, migrations, policies, tables, Storage configuration, `.env`, application/runtime code, typed operations, existing tests, registries, constitutions, PRDs/FRs, Tech Specs, source records, or the previous twelve mandates. It SHALL NOT call Supabase, apply migrations, run CA-IMPL staging or promotion scripts, provision infrastructure, upload/delete test objects, alter receipts, change an authority state, or use an operator token. It shall not write a migration design as though it has been approved; a repair recommendation belongs in the Findings Register only.

## 5. Required audit method, adversarial checks, and failure routes

The Governance Audit must produce a concise executive verdict, a phase-by-phase ledger, an object/capability ledger, and a residual-risk register. It must separately report: (a) what exists in current source, (b) what local/static verification was reproduced, (c) what E3 evidence is recorded but not replayed, and (d) what cannot presently be reproduced and why.

At minimum, independently challenge these false proofs:

1. a document or YAML exists but its claimed runtime consumer does not;
2. a static validator passes while ignoring a pending ratification or stale control-state status;
3. a test passes without a database/Storage topology and is reported as E3;
4. a receipt or self-authored proof is treated as independent confirmation without a verifier/source/decision trace;
5. an operator approval for one staging aggregate is generalized to all PostgreSQL state or production;
6. a historical pending decision is treated as current despite a recorded later resolution, or a later implementation is treated as retroactive ratification;
7. a script labelled “reproducible” is write-capable, cannot connect, has missing dependencies, or has environment-specific assumptions;
8. the destructive CA-IMPL-01A scaffolder is misrepresented as a safe forward migration;
9. F-01 or F-02 is treated as closed merely because the original cutover had compensating controls;
10. deferral of SDA/SFL runtime authority, SemanticProgram, or production cutover is omitted from the final verdict.

For every failed, blocked, or contradictory check, record the exact command or inspection, non-secret failure category, impact, affected claim IDs, recommended next repair phase, and whether it blocks continued authority. Do not fix it. A network denial, for example, must be stated as `ENVIRONMENT_BLOCKED` with its tested endpoint class, not fabricated as a database failure or proof success.

## 6. Required evidence, verification, completion, and operator gate

The static audit validator shall prove the presence and completeness of every matrix field; that every Phase 1–12 phase has a classification; that every `RATIFIED`, `POSTGRES_AUTHORITATIVE_STAGING_ONLY`, or `PRODUCTION_AUTHORIZED` claim cites the required evidence class; that unresolved findings have an owner/next phase; and that recorded non-claims are not silently marked implemented. It is E1 structural evidence only.

The Completion Record must include:

```text
A. what changed
B. why it changed
C. what was proven in this audit
D. what remains only recorded, rather than independently reproduced
E. what remains uncertain or blocked
F. what could still be wrong
G. exact files and statuses for operator inspection
H. exact decision required
```

CA-AUDIT-01 reaches `OPERATOR_REVIEW` only when all allowed artifacts exist, the static audit validator and permitted local tests pass, the control-state snapshot is internally consistent, each contradiction has a disposition, and the report does not overclaim remote/runtime proof. The agent must commit only allowed files, record the commit, and stop.

**Rollback:** CA-AUDIT-01 changes no operational state. If its artifact update is rejected, revert only the CA-AUDIT-01 documentation/validator commit and restore the preceding control-record wording through a new, explicit corrective commit. Never use a documentation rollback to erase historical proof, receipt references, findings, or operator decisions; supersede them with an attributable correction.

Gemini SHALL request exactly:

> **Accept CA-AUDIT-01 as the authoritative post-execution status record, preserve all listed limitations and non-claims, and authorize CA-GOV-02 only to reconcile formal ratification states and control-state governance—without any schema, runtime, database, Storage, registry, or authority transition?**

It SHALL stop after this question. The operator’s approval does not repair F-01/F-02, change PostgreSQL authority, authorize production, or authorize CA-MIG-03.

## 7. Gemini activation prompt (approximately 260 words)

You are the CAE governed execution agent for `CA-AUDIT-01 — Post-Execution Governance, Evidence, and Reality Reconciliation`. Read this complete mandate and every required reference before planning, editing, or validation. Your authority is narrow: reconcile the recorded Phase 1–12 governance/evidence state into the permitted audit artifacts and durable control record. This is not authorization to repair code, schema, DDL, RLS, Storage, registries, documentation doctrine, or runtime behavior.

First create an internal, read-only evidence plan: one row per phase and material capability, with source/commit/validator/proof/receipt/decision references and an explicit distinction among authored, ratified, implemented, verified locally, recorded E3, staging-authoritative, production-authorized, deferred, blocked, and contradictory. Do not infer ratification from later implementation; do not keep historical decisions presented as current after a documented resolution. Preserve prior history with explicit dispositions rather than deleting it.

Inspect actual source, DDL, validator, test, proof, and Git evidence. You may run only local, non-mutating checks. Never run a remote verifier merely because it is named a verifier: database queries, fixtures, cleanup, uploads, migrations, or remote calls are prohibited. Record an unavailable endpoint or network denial honestly as an environment/reproducibility limitation; do not claim that either proves or disproves historical staging evidence.

Challenge false proof: documents without consumers, static validation mistaken for E3, self-attested receipts, pending ratification ignored by later code, one staging aggregate generalized to all authority, destructive scaffolding called a migration, and F-01/F-02 called fixed without repair. Maintain all explicit non-claims: no broad SQLite migration, SDA/SFL runtime authority, semantic-engine implementation, production authorization, or E4/taste proof.

Create only the named audit artifacts and optional read-only validator/test, update control state without changing operational authority, commit scope-only files, request the exact Section 6 decision, and stop.
