# Gemini Execution Mandate — Phase 22 / CA-ACCEPT-10

**Status:** `DRAFT — BLOCKED UNTIL CA-STAGE-09 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-ACCEPT-10`  
**Title:** Independent Regression, Operator Acceptance, and Next-Aggregate Decision  
**Execution classification:** Independent review and acceptance preparation; read-only evidence inspection, local regression, and optionally admitted read-only shared-staging health inspection only; no deployment, migration, data mutation, authority promotion, or next-aggregate implementation  
**Required prior decision:** “Accept CA-STAGE-09 as the bounded shared-staging deployment and authorize CA-ACCEPT-10 only for independent regression/acceptance review and selection of at most one next aggregate.”  
**Required completion gate:** `VERIFY -> OPERATOR_REVIEW -> HANDOFF`; no next aggregate begins within this mandate.

## 1. Authority, purpose, and independence boundary

CA-ACCEPT-10 is governed by the CAE Governance & Specification Bridge Bundle v3, particularly Implementation Gate, Reality-Contact Evaluation, Test Governance and Reward-Hacking, State/Transition Control, Phase Promotion/Proof, and Coding-Agent State-Control rules. It inherits accepted CA-AUDIT-01 through CA-STAGE-09 records and the current durable control state.

The purpose is to decide whether the repaired first-slice substrate has enough bounded evidence to be accepted as shared-staging work, while keeping its limits precise. It must not become a post-hoc justification for broad CAE completion, full PostgreSQL authority, production readiness, SDA/SFL runtime adoption, semantic intelligence, client-data migration, source retirement, or a new vertical-slice implementation.

Review independence is required. The reviewer must not rely solely on its own prior transcript or self-attested receipt. Where possible, a reviewer other than the implementing agent performs the review. If the same agent/session must perform it, the Completion Record SHALL say `REVIEWER_INDEPENDENCE_LIMITED`, identify the overlap, and downgrade the review from independent to `SELF_REVIEW_WITH_ADVERSARIAL_CHECKS`; it may not label it independent. The operator remains the only authority that accepts the outcome or chooses the next aggregate.

The permitted transition is:

```text
CA-STAGE-09 bounded shared-staging proof
  -> independent or explicitly limited regression/acceptance review
  -> OPERATOR_REVIEW
  -> HANDOFF

next aggregate:
NOT_STARTED until separately authorized
```

Acceptance may record a shared-staging fact only where exact evidence supports it. It does not change the authority state of `MC-CAE-MED-001`, other aggregates, or production.

## 2. Mandatory reading and review admission

Before planning, testing, or editing, the reviewer SHALL read in full:

1. All mandates, decisions, proofs, admission records, preflight/deployment/recovery/cleanup results, and Completion Records from CA-AUDIT-01 through CA-STAGE-09.
2. `CAE_IMPLEMENTATION_CONTROL_STATE.md`, Governance Status Matrix, Ratification Register, Findings/Decisions Register, deferred-domain list, and original Phase 1–12 evidence handoff.
3. The actual current migrations, topology/route source, guarded runners, F-01/F-02 tests, related models/operations, and existing CAE test suite.
4. `TS-CAE-TEN-001`, relevant constitutions/FRs/state contracts, `docs/PRD/CURRENT.md`, and Bundle v3 protocols named in Section 1.
5. Git history and working-tree state. The review must identify commits/artifact checksums actually inspected and any uncommitted or unrelated worktree changes it did not assess.

Local static validators and pure/local tests are permitted. A shared-staging inspection is optional and requires separate, operator-approved **read-only** admission: target identity; non-production guard; read-only role/session; query allowlist limited to schema, migration history, non-identifying status/count/health metadata; no mutation/function invocation/payload access; and secret-safe logs. It must never rerun fixture-producing E3 scripts, operational routes, cleanup jobs, migrations, or Storage tests against shared staging in this phase.

If review environment access is unavailable, classify the limitation. Do not rewrite historical staging proof as newly observed. If Git/artifact evidence cannot be reconciled, stop as `EVIDENCE_CONFLICT` rather than approving an inferred state.

## 3. Exact review scope and claim model

CA-ACCEPT-10 reviews only the bounded chain:

```text
governance/control-state reconciliation
-> forward-only migration safety
-> disposable foundation application
-> F-01 structural integrity proof
-> F-02 topology decision and selected-route proof
-> independent E3 replay
-> controlled shared-staging deployment
```

It must make a separate finding for each of these claims:

- current governance/risk/control record is coherent and preserves history;
- shared staging received only the approved migration/route checksums;
- F-01 cross-Workspace receipt-evidence links are structurally rejected in shared staging;
- selected F-02 topology and canonical route are unambiguous in shared staging;
- RLS/Workspace isolation and append-only receipt controls remain intact;
- deployment had recovery/cleanup evidence and did not migrate client/legacy data;
- all stated proof limitations and deferred domains remain visible;
- production authority, broad aggregate authority, and next aggregate status remain unchanged.

Every finding must contain: claim ID, evidence sources/checksums, review method, evidence class/fidelity, reviewer independence class, result (`ACCEPTED`, `LIMITED`, `UNPROVEN`, `CONTRADICTORY`, or `REJECTED`), risks, falsification route, and required owner/next action. A passing local test cannot upgrade a shared-staging claim; a recorded staging proof cannot upgrade a production claim; and a static document validator cannot prove operator intent.

The Next-Aggregate Candidate Register may list at most three candidates drawn only from accepted CA-STATE-01 dispositions and current evidence. For each candidate state: aggregate/contract, reason it is next, source/target authority, data classification, legal parent chain, dependencies, migration/route implications, E3 prerequisites, recovery/rollback, unproven risks, and operator decision required. It may not choose, design, implement, or expose a candidate. It must exclude any aggregate with unresolved canonical ownership, F-01/F-02 dependency, ambiguous topology, client-data classification, or missing contract.

## 4. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- `docs/cae/implementation/CAE_ACCEPT_10_REVIEW_ADMISSION.md`;
- `docs/cae/implementation/CAE_ACCEPT_10_REGRESSION_AND_CLAIM_MATRIX.md`;
- `docs/cae/implementation/CAE_ACCEPT_10_INDEPENDENCE_AND_EVIDENCE_REPORT.md`;
- `docs/cae/implementation/CAE_ACCEPT_10_NEXT_AGGREGATE_CANDIDATE_REGISTER.md`;
- `docs/cae/implementation/CAE_ACCEPT_10_OPERATOR_ACCEPTANCE_PACKET.md`;
- `docs/cae/implementation/CAE_ACCEPT_10_COMPLETION_RECORD.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`;
- a read-only acceptance validator under `scripts/cae/audit/` and pure/local regression tests under `tests/cae/` only.

Gemini SHALL NOT modify migrations, schema, topology/route/runtime code, RLS, triggers, grants, Storage, data, registries, canonical artifacts, service/API deployment, `.env`, authorities, receipts, source/SQLite state, or any earlier proof record. It shall not execute staging migrations, routes, fixtures, cleanup, or remote writes; select/provision a next aggregate; call a candidate accepted; or claim an operator decision has occurred before it is recorded.

## 5. Required regression, adversarial review, and failure routes

Run and report the permitted local regression suite plus static validators for governance, migration safety, F-01/F-02 scope, and acceptance artifact integrity. The review must make clear what each check really exercises and what it does not. It must challenge, at minimum:

1. a prior acceptance record is treated as proof although its source/checksum/commit is missing or changed;
2. shared-staging deployment is generalized to production, all aggregates, or client-data migration;
3. F-01 is called fixed because a typed path/RLS blocks a test, rather than the database constraint being evidenced;
4. F-02 is called resolved because a substituted operation passes, rather than the operator-selected route being proven;
5. static/local success is reported as fresh E3/shared-staging proof;
6. a self-review is labeled independent;
7. a recovery claim lacks a named executable route or no-residue evidence;
8. a deferred domain disappears from the final report because it is inconvenient;
9. a next-aggregate candidate is selected from documentation alone without contract/data/authority prerequisites;
10. an uncommitted/unreviewed change is treated as part of accepted evidence;
11. an operator packet bundles acceptance with production promotion or new implementation;
12. a clean status/count hides a bypass, wrong route, or absent downstream receipt/state effect.

If any material claim is unproven, contradictory, checksum-divergent, dependent on a failed test, or lacks recovery/cleanup/owner evidence, mark it `LIMITED`, `UNPROVEN`, or `REJECTED`; do not repair it inside acceptance. If a finding changes the scope of a prior package, return it to the appropriate repair phase or create a proposed future mandate only after operator direction.

## 6. Completion, handoff, rollback, and operator gate

CA-ACCEPT-10 completes only when its admission is recorded; all relevant evidence is classified; permitted regressions/validators pass or are honestly limited; review independence is stated; all F-01/F-02, authority, production, data, and deferred-domain claims are explicit; at most three next candidates are qualified; and the operator packet contains separately decidable statements.

The Completion Record must provide:

```text
A. what was reviewed and what changed
B. what is accepted versus limited/unproven/rejected
C. what evidence was independently observed versus inherited
D. what remains staging-only and what remains deferred
E. what could still be wrong and its falsification path
F. the complete F-01/F-02/recovery/authority status
G. exact reviewer-independence limitations and inspection paths
H. the one next decision required
```

**Rollback:** This is a documentation/review phase. If rejected, issue a corrective commit that preserves earlier evidence and records the reason for changed classification. No system state may be rolled back or changed by CA-ACCEPT-10. Any shared-staging corrective action requires a new authorized repair/deployment package.

Control state may record `FIRST_SLICE_SHARED_STAGING_ACCEPTANCE_READY_FOR_OPERATOR_REVIEW`; it must not record production approval, global PostgreSQL authority, next-aggregate implementation, or retirement of source systems.

Gemini SHALL request exactly:

> **Accept the CA-ACCEPT-10 bounded shared-staging substrate review as stated, preserve every limited/unproven/deferred claim and all production/data/authority non-claims, and authorize CA-NEXT-01 only to write a mandate and evidence plan for the one named next aggregate in the Candidate Register—without implementing, migrating, or promoting that aggregate?**

It SHALL stop after this question.

## 7. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-ACCEPT-10 — Independent Regression, Operator Acceptance, and Next-Aggregate Decision`. This mandate is blocked until CA-STAGE-09 is accepted. Read all preceding mandates, decisions, proof/admission/recovery/cleanup records, control-state/governance artifacts, current source/tests, contracts/constitutions, PRD truth record, Git history, and governing Bundle protocols before planning or reviewing.

Your role is review, not repair or new implementation. First declare reviewer independence. If you share authorship/session with the implementation lane, label the review `SELF_REVIEW_WITH_ADVERSARIAL_CHECKS`, never independent. Build a claim matrix distinguishing inherited evidence from newly observed local/read-only evidence, and classify every material statement accepted, limited, unproven, contradictory, or rejected.

Run only permitted local/static regressions. Shared-staging inspection is optional and strictly read-only after target/role/query admission; do not run migrations, routes, fixtures, cleanup, Storage tests, or any remote writer. Challenge false proof: deployment called production, typed/RLS workaround called F-01 structural repair, substituted route called F-02 resolution, static pass called E3, self-review called independent, recovery asserted without a real route, deferred domains omitted, and documentation-only next candidate selection.

Keep all non-claims explicit: no production authority, broad PostgreSQL authority, client-data migration, source/SQLite retirement, SDA/SFL runtime authority, full semantic engine, or next aggregate implementation. List no more than three candidates; do not choose one or create its implementation plan. Commit only allowed review artifacts, request the exact Section 6 decision, and stop.
