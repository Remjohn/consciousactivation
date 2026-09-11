# Gemini Execution Mandate — Phase 20 / CA-E3-08

**Status:** `DRAFT — BLOCKED UNTIL CA-TOPO-07 OPERATOR ACCEPTANCE AND INDEPENDENT ENVIRONMENT ADMISSION`  
**Phase ID:** `CA-E3-08`  
**Title:** Independent Staging-Equivalent Reality-Contact Replay  
**Execution classification:** Independent E3 replay of the approved tenant foundation, F-01 repair, and selected F-02 topology in one fresh staging-equivalent environment; synthetic data only; no shared-staging mutation, client migration, or authority promotion  
**Required prior decision:** “Accept CA-TOPO-07 disposable proof and authorize CA-E3-08 only to independently replay its exact approved chain in a named staging-equivalent environment, without promoting any authority.”  
**Required completion gate:** `VERIFY -> OPERATOR_REVIEW`; a green replay is evidence, not shared-staging admission.

## 1. Authority, objective, and independence rule

CA-E3-08 is governed by the CAE Governance & Specification Bridge Bundle v3, especially the Reality-Contact Evaluation, Test Governance and Reward-Hacking, State/Transition Control, PostgreSQL State Model, Semantic Operation API, Harness/Runbook, and Phase Promotion protocols. It inherits only the explicitly accepted decisions, checksums, boundaries, and non-claims from CA-AUDIT-01 through CA-TOPO-07.

The purpose is to test whether the approved proof chain is reproducible in an independently admitted, production-shaped staging-equivalent environment—not whether a prior transcript says it passed. The chain comprises exactly: the forward-only first-slice foundation drafts, the F-01 Workspace/Receipt structural repair, the operator-selected F-02 topology and canonical route, and only the required tenant/receipt/evidence controls directly exercised by that route.

Independence requires a fresh environment identity, a fresh schema/fixture lifecycle, independent schema/route inspection, and a replay harness that does not accept a historical proof, receipt, migration-history row, expected count, or self-authored log as success. The same source code and approved migration drafts may be used; reusing the same staging project, target data, or unverified proof conclusion is prohibited. The evaluator must record where it is relying on the original chain and where it has newly observed behavior.

The only permitted transition is:

```text
approved disposable proofs
  -> independently replayed E3 evidence in a staging-equivalent environment
  -> OPERATOR_REVIEW

shared staging, production, aggregate authority, source retirement:
unchanged
```

CA-E3-08 may never report a replay as production readiness, shared-staging repair, all-aggregate PostgreSQL authority, semantic/taste validation, or a replacement for operator acceptance.

## 2. Mandatory reading and environment admission

Before planning, connecting, provisioning, applying migrations, or uploading a fixture, Gemini SHALL read in full:

1. The accepted CA-AUDIT-01 through CA-TOPO-07 mandates, decisions, completion records, current control state, and all stated limitations/non-claims.
2. Exact migration/adapter/route IDs and checksums approved by CA-MIG-03, CA-INT-05, and the selected CA-TOPO-06 option/CA-TOPO-07 proof.
3. The current source for the guarded migration runner, typed/bridge canonical operation, models, RLS/receipt controls, test helpers, and teardown procedures.
4. `TS-CAE-TEN-001`, relevant constitutions/FRs/state contracts, reality-contact/test-governance protocols, and all applicable `AGENTS.md` instructions.

The operator must identify one target meeting all of these requirements before action:

```text
environment class: E3_STAGING_EQUIVALENT_DISPOSABLE
identity: separate project/database/container from current CAE staging and production
engine/topology: PostgreSQL/Supabase-equivalent features required by selected route
data: empty or synthetic-only; no client, Guest, source, media, receipt, registry, or SQLite data
storage: private synthetic-only bucket/prefix only if selected canonical route requires byte verification
recovery: target can be destroyed/recreated; teardown owner and route are identified
access: least privilege and secret-safe configuration; no credentials printed or committed
```

If private object storage, RLS/session context, extensions, a read/write role, network access, target identity, or teardown cannot be independently established, record `ENVIRONMENT_BLOCKED` or `ENVIRONMENT_NON_EQUIVALENT` and stop before mutation. Do not downgrade E3 to a mock/local unit suite or substitute the current shared staging project.

The admission record must capture non-secret target label, engine/version, feature parity, approved commit, exact checksums, target-guard result, data classification, Storage policy/bucket class when applicable, executor, timestamp, and recovery route. It must explicitly compare the target identity to the current shared staging identity and prove non-equality.

## 3. Exact scope and replay procedure

Only the approved migration IDs, F-01 repair, selected F-02 topology/route, and their minimum proof scripts/tests may run. The replay shall use fresh run-prefixed synthetic Workspaces, receipts, evidence/link metadata, and—only when the selected route requires it—synthetic private Storage bytes. It shall not import any historical CAE, client, Guest, SDA/SFL, registry, or SQLite data.

The replay SHALL execute these evidence-bearing stages:

1. **Admission and clean baseline.** Prove target guard, empty/synthetic classification, required engine features, baseline schema absence or approved clean state, migration checksums, and clean Storage prefix if applicable.
2. **Independent forward application.** Apply approved drafts via the guarded runner. Independently inspect schema, parent/child keys, RLS policies, receipt append-only triggers, migration history, and selected topology route. Do not accept runner output alone.
3. **Canonical route exercise.** Execute the exact operator-selected F-02 canonical operation with fresh synthetic input. Trace the input key/identity boundary, target relation family, Workspace chain, state transition, required receipt/evidence effect, and Storage fresh-read hash when the route requires media bytes. A different typed operation cannot substitute for the selected route.
4. **Two-Workspace containment proof.** Create equivalent synthetic records in two Workspaces and independently prove no-context denial, cross-Workspace read/write denial, parent-chain rejection, Guest/evidence locality where in scope, and no cross-scope receipt-evidence linkage.
5. **F-01 structural proof.** Attempt a direct, controlled cross-Workspace `(workspace_id, receipt_id)` receipt-evidence link insertion that reaches the database constraint. It must be rejected by the approved structural integrity constraint and leave no row; RLS or application validation alone is insufficient.
6. **F-02 topology proof.** Attempt a wrong/shadowed relation-family or key-shape route and prove deterministic denial/detection under the selected option. Prove that the selected canonical route uses no hidden fallback or ambiguous dual-write.
7. **Adversarial/recovery proof.** Run the required countertests, repeat/idempotency checks, one bounded failure/repair route, and a fresh independent read after each relevant state effect.
8. **Teardown.** Remove only run-prefixed synthetic data/objects or destroy the target through its admitted route. Prove cleanup/target disposition and preserve only non-secret evidence artifacts, checksums, receipts, and logs.

## 4. Required E3 countertests and reward-hack resistance

The E3 Replay Plan must answer for each check: real behavior exercised, environment feature, independent evidence, shortcut risk, falsification route, recovery/cleanup result, and non-claim. At minimum execute and report:

1. current-shared-staging/production-like target is rejected before mutation;
2. altered migration/topology/route checksum is rejected;
3. migration succeeds only when ordered predecessors/preconditions exist;
4. static/migration history success with missing actual RLS/trigger/key is detected by independent inspection;
5. no-session/unscoped read and write paths are denied;
6. swapped Workspace parent or Guest/evidence scope is rejected;
7. direct cross-Workspace receipt-evidence link reaches and is rejected by F-01 structural enforcement;
8. selected route succeeds while wrong/shadowed family/key-shape route is denied/detected, not silently adapted;
9. selected route cannot write target state without its mandated receipt/evidence/state effect;
10. stale/altered synthetic media bytes are quarantined or rejected when Storage verification is in scope;
11. receipt UPDATE/DELETE and fabricated-success mutation are rejected by append-only controls;
12. replay/duplicate idempotency input neither duplicates target/evidence/receipt state nor changes route selection;
13. an induced failure leaves no false history/receipt/state and follows the named forward-repair/recreation path;
14. teardown rejects unscoped cleanup and proves run-prefix/target-only residue disposition.

Mocks may test guards but never replace the actual E3 environment. A unit suite, schema dump, expected row count, an agent-authored receipt, a successful HTTP status, or a prior transcript does not satisfy any countertest. If a test cannot reach the required real topology/control, mark it `NOT_PROVEN`, explain why, and do not promote the package.

## 5. Files, mutation authority, and hard stops

Gemini MAY create/update only the approved replay harness/guarded scripts and tests plus:

- `docs/cae/implementation/CAE_E3_08_ENVIRONMENT_ADMISSION_RECORD.md`;
- `docs/cae/implementation/CAE_E3_08_REPLAY_PLAN.md`;
- `docs/cae/implementation/CAE_E3_08_INDEPENDENT_PROOF.md`;
- `docs/cae/implementation/CAE_E3_08_ADVERSARIAL_RESULTS.md`;
- `docs/cae/implementation/CAE_E3_08_RECOVERY_AND_TEARDOWN_RECEIPT.md`;
- `docs/cae/implementation/CAE_E3_08_COMPLETION_RECORD.md`;
- scoped scripts/tests under established CAE implementation/evaluation locations;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Gemini SHALL NOT mutate current shared staging, production, SQLite, client/Guest/source/registry data, existing promoted aggregate authority, broad runtime/API routes, constitutions/PRD/FR/contracts, SDA/SFL, or `.env`. It shall not promote a migration or topology to shared staging; use a normal customer workload; preserve real media; leave the target dirty; or start CA-STAGE-09.

Stop as `BLOCKED`, `ENVIRONMENT_NON_EQUIVALENT`, `REPAIR_REQUIRED`, or `SCOPE_VIOLATION` for wrong target/data class, failed guard, missing feature, checksum/source divergence, no direct F-01 constraint proof, ambiguous F-02 route, weakened RLS/receipt control, required effect absent, recovery uncertainty, or cleanup failure. Preserve non-secret evidence; do not retry against another target without a new admission.

## 6. Completion, rollback, and operator gate

CA-E3-08 completes only when all admission, clean application, independent structural inspection, selected canonical-route behavior, two-Workspace isolation, F-01/F-02 adversarial proof, replay/failure/recovery, and teardown checks pass in the named staging-equivalent target. The completion record must separate newly observed proof from historical recorded proof and list every limitation, unsupported feature, deferred domain, and remaining shared-staging risk.

**Rollback/recovery:** The target is disposable. The recovery route is its named recreation/destruction mechanism or a checksum-controlled forward repair. Never use destructive bootstrap logic against shared state. If target cleanup cannot be proven, mark it contaminated and deny reuse; do not claim replay success.

Control state may record `INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY`; it must state that no current shared staging/prod/schema authority changed and that this is not a data migration or production promotion.

Gemini SHALL request exactly:

> **Accept CA-E3-08 as independent staging-equivalent evidence for the exact approved foundation, F-01, and selected F-02 chain only, preserve all shared-staging/production/data-migration limitations, and authorize CA-STAGE-09 only to admit and deploy those exact proven migrations/routes to the named shared staging environment under a separate backup, recovery, and operator gate—without promoting production authority?**

It SHALL stop after this question.

## 7. Gemini activation prompt (approximately 275 words)

You are the CAE governed execution agent for `CA-E3-08 — Independent Staging-Equivalent Reality-Contact Replay`. This mandate is blocked until CA-TOPO-07 is accepted and the operator admits one fresh, separate, staging-equivalent target. Read the complete chain of accepted audit, governance, migration, F-01, F-02, topology, source, contract, test, and Bundle references before planning, connecting, provisioning, or writing fixtures.

Your task is an independent E3 replay—not a transcript review and not a shared-staging deployment. Verify target identity, engine/features, synthetic-only data, required private Storage parity if applicable, draft/route checksums, recovery, and teardown before mutation. Reject current staging/production-like targets and any non-equivalent environment. Never print or commit credentials, payload data, signed URLs, or client identifiers.

Apply only the approved chain through guarded runners and inspect the resulting schema/keys/RLS/triggers/routes independently. Exercise the exact operator-selected canonical F-02 operation with fresh synthetic data; never replace it with another passing route. Prove two-Workspace isolation, no-session denial, F-01 direct structural cross-workspace-link rejection, F-02 wrong-family/key denial, receipt immutability, required receipt/state/evidence effects, idempotency, relevant Storage fresh-read/hash behavior, bounded failure/recovery, and scoped teardown.

Treat mocks, unit tests, migration history, counts, success statuses, historical transcripts, and self-authored logs as insufficient. Record behavior, environment, independent evidence, shortcut/falsification, recovery, cleanup, and limits for every check. If a required control cannot be reached in real topology, mark it unproven and stop; do not promote. Do not touch shared staging, production, SQLite, Storage outside the disposable prefix, client/registry data, authority records, or broad runtime surfaces. Commit only allowed proof artifacts, request the exact Section 6 decision, and stop.
