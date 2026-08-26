# Gemini Execution Mandate — Phase 16 / CA-APPLY-04

**Status:** `DRAFT — BLOCKED UNTIL CA-MIG-03 OPERATOR ACCEPTANCE AND DISPOSABLE-ENVIRONMENT IDENTIFICATION`  
**Phase ID:** `CA-APPLY-04`  
**Title:** Disposable PostgreSQL Migration Application and Recovery Proof  
**Execution classification:** One isolated, non-production migration-application proof for exact approved draft IDs; no shared staging, client data, source retirement, runtime cutover, or authority change  
**Required prior decision:** “Accept CA-MIG-03 as design-only and authorize CA-APPLY-04 for the exact listed migration draft IDs in the named disposable environment only.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; database destruction/teardown is permitted only for the named disposable target and only after evidence capture.

## 1. Authority, purpose, and environment boundary

CA-APPLY-04 is governed by the CAE Governance & Specification Bridge Bundle v3, accepted CA-AUDIT-01, CA-GOV-02, and CA-MIG-03 artifacts, `TS-CAE-TEN-001`, the first-slice constitutions/contracts, and the current durable control record. Its sole purpose is to test whether the exact forward-only migration draft package designed in CA-MIG-03 can be safely applied, verified, re-applied/preflighted, rejected on incompatible topology, and recovered inside an isolated disposable PostgreSQL environment.

This phase is not permission to apply migrations to the current CAE staging project, the project containing the `MC-CAE-MED-001` recorded promotion, production, a developer database containing work, any brownfield SQLite database, or an environment containing client/Guest/evidence data. It does not alter the authority of any aggregate. A successful application proof shows only that the named migration drafts behaved as stated in the named disposable environment.

Before any command, the operator must provide or explicitly approve one target satisfying all conditions:

```text
environment class: DISPOSABLE_POSTGRESQL_ONLY
identity: named host/project/container/database and evidence it is not current CAE staging/production
data classification: empty or synthetic fixtures only; no client, Guest, media, receipt, registry, or source data
recovery: deletion/recreation or isolated restore route available
access: least-privilege, secret-safe, single designated execution owner
```

If any condition is missing, contradictory, or cannot be independently preflighted, CA-APPLY-04 is `BLOCKED`. Do not substitute a convenient reachable database. Network denial is not a reason to weaken the target rule.

The sole permitted transition is:

```text
CA-MIG-03 draft IDs: DESIGNED_AND_STATICALLY_REHEARSED_ONLY
  -> APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY
  -> OPERATOR_REVIEW
```

It does not update `MC-CAE-MED-001`, current staging authority, production status, or the forward-migration draft status beyond the bounded proof record.

## 2. Mandatory reading, admission, and exact target verification

Before planning, connecting, creating a fixture, or applying a migration, Gemini SHALL read in full:

1. The accepted CA-MIG-03 schema inventory, migration plan, dependency graph, safety rehearsal, F-01/F-02 repair boundary, completion record, draft manifests/SQL, validator, and control-state entry.
2. CA-AUDIT-01 and CA-GOV-02 records, especially all non-claims, open findings, ratification status, and the exact next-phase authorization.
3. The current CA-IMPL-01A scaffolder and proof, CA-IMPL-01B/02/02P proof/recovery artifacts, and `TS-CAE-TEN-001` migration/verification requirements.
4. The migration runner, database adapter, test tooling, and all relevant `AGENTS.md` instructions before modifying execution code or invoking a command.
5. The approved target identity and recovery evidence through secret-safe inspection. Do not print credentials, passwords, connection strings, access tokens, URLs bearing tokens, or data rows.

The admission record must include: operator-approved target label; non-production/non-current-staging comparison; fresh database identity; server/version/extensions; current schema inventory; data classification; backup/recreation method; exact draft IDs/checksums; git commit; executor; timestamp; and a declared teardown owner. A target schema with pre-existing `cae.*` state is permitted only if it is expressly synthetic/disposable and its state is documented before mutation. Client or unknown data is an absolute stop.

No migration may run until the admission checklist, draft checksum, static validator, and recovery route pass. The agent must use the approved migration runner rather than ad-hoc direct SQL, except where the approved runner itself is the subject of this proof and its execution boundary is documented.

## 3. Exact authorized scope and execution sequence

The agent may apply only the migration IDs and checksums enumerated by CA-MIG-03 and repeated in the operator authorization. The foundation schema is the only in-scope aggregate surface. F-01/F-02 repairs, legacy data migration, Storage policy deployment, real Supabase credentials, application routing, semantic operations, receipt issuance from normal runtime traffic, and source/authority cutover are excluded.

The required sequence is:

1. **Admission/preflight.** Prove disposable target identity; take a non-secret schema/data snapshot; verify draft checksums, ordered predecessors, compatibility preconditions, and no forbidden DML/destructive statements.
2. **Clean apply.** Apply the ordered drafts once. Capture migration ID/checksum/result, schema delta, lock/elapsed measurements, and runner logs without secrets or row content.
3. **Structural verification.** Verify intended tables, key/foreign-key/uniqueness constraints, extensions, functions/triggers, RLS enablement/policies, grants, and migration-history state match the approved manifest.
4. **Behavioral containment proof.** Using synthetic, non-client fixture data only, prove the minimum Workspace isolation, cross-workspace parent rejection, receipt immutability, and no-context/RLS denial required by the approved plan. This is a database-foundation proof, not a normal CAE runtime or authority proof.
5. **Re-run/preflight behavior.** Re-run the approved migration command or its preflight exactly as designed. It must report an honest no-op/verified-applied outcome, or fail safely with a documented, non-mutating message. It must not silently reapply, change checksums, duplicate policies/triggers, or alter data.
6. **Incompatible-topology proof.** In a second disposable synthetic topology—or a reset/recreated target—introduce only the approved incompatible schema condition. Prove that preflight rejects it before migration state or schema changes occur. Do not use an unknown/shared database for this test.
7. **Failure and recovery rehearsal.** Induce one approved, bounded failure prior to final commit or postcondition confirmation. Prove transaction/runner failure behavior, migration-history honesty, and the prescribed forward-repair or environment-recreation route. Never use destructive bootstrap DDL as recovery.
8. **Teardown/retention.** Capture evidence, remove synthetic objects/data according to the named disposable recovery plan, verify no residue, and preserve only non-secret receipts/logs/checksums/artifacts in the repository.

If any step calls for a migration not in the approved draft list, data transformation, F-01/F-02 structural repair, Storage, or authority state update, stop as `SCOPE_VIOLATION`.

## 4. Files, data, and mutation boundaries

Gemini MAY create or update only the exact migration draft/runner files approved in CA-MIG-03 plus:

- `docs/cae/implementation/CAE_APPLY_04_DISPOSABLE_ADMISSION_RECORD.md`;
- `docs/cae/implementation/CAE_APPLY_04_MIGRATION_APPLICATION_PROOF.md`;
- `docs/cae/implementation/CAE_APPLY_04_SCHEMA_AND_CONTAINMENT_RESULTS.md`;
- `docs/cae/implementation/CAE_APPLY_04_FAILURE_RECOVERY_REHEARSAL.md`;
- `docs/cae/implementation/CAE_APPLY_04_TEARDOWN_RECEIPT.md`;
- `docs/cae/implementation/CAE_APPLY_04_COMPLETION_RECORD.md`;
- explicitly scoped proof scripts and tests under `scripts/cae/implementation/` and `tests/cae/`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Every remote-mutating command must name the disposable target guard and execute through a runner that rejects current CAE staging/production endpoints, unapproved project/database identities, missing `DISPOSABLE_POSTGRESQL_ONLY` environment declaration, or a draft checksum mismatch. All synthetic fixture names must carry an execution-run prefix so cleanup cannot target unrelated state.

Gemini SHALL NOT touch the existing staging project, production, SQLite databases, Supabase Storage, client data, registry data, services/API/runtime paths, RLS design outside named foundation drafts, constitutions/specs/contracts, prior proof records, or `.env` content. It shall not run the destructive CA-IMPL-01A scaffolder, issue a normal operational receipt, alter the recorded MC-CAE-MED-001 authority, or leave a database mutated without the documented teardown/retention decision.

## 5. Required E3 proof, adversarial tests, and hard stops

The proof must identify real database engine/version and isolated environment class, but it must not mistake a successful connection or a migration history row for proof. It must include independent schema inspection after the runner completes and preserve command/checksum/result evidence.

At minimum, execute and report these countertests:

1. wrong target identity or current-staging-like identity is rejected before connection/mutation;
2. altered migration draft/checksum is rejected before execution;
3. incompatible UUID/text table/key or relation topology is rejected by preflight without partial apply;
4. a forbidden `DROP`, `TRUNCATE`, `CASCADE`, or DML token in a draft is rejected by static guard;
5. child migration attempted before predecessor is rejected;
6. second invocation cannot duplicate a table, policy, trigger, grant, index, or migration-history row;
7. RLS is enabled and an unscoped synthetic connection cannot read protected fixture state;
8. swapped Workspace parent scope is rejected by the applicable constraint/control;
9. receipt UPDATE/DELETE is rejected by the append-only trigger;
10. induced runner/statement failure leaves no false applied-history record and follows the recorded recovery route;
11. teardown proves scoped synthetic fixture removal or documented environment destruction with no claim about shared staging cleanliness.

The test must distinguish a schema limitation from a successful foundation application. F-01 may be observed as still open; it must not make the test pass through a typed-operation workaround. F-02 must remain untouched. A mock database, parser-only test, row count, receipt-like log, or self-attested teardown alone is insufficient E3 evidence.

Stop immediately as `BLOCKED` or `REPAIR_REQUIRED` for target-identity doubt, non-synthetic data, unexpected existing state, failed preflight, partial application without an honest recovery route, RLS/constraint/trigger bypass, checksum divergence, fixture cleanup uncertainty, or a requested scope expansion. Preserve evidence; do not retry against a different target without a new admission record.

## 6. Completion, rollback, and operator gate

CA-APPLY-04 completes only when admission, clean apply, independent structural/containment checks, safe re-run, incompatible-topology rejection, failure/recovery rehearsal, and teardown evidence all pass for the exact draft IDs. The Completion Record must report what changed in the disposable target, why, tests/environment/evidence, what failed or remained unproven, cleanup result, F-01/F-02 status, risks, and non-claims.

**Rollback and recovery:** The target is disposable. The primary recovery route is its documented recreation/destruction procedure; any forward repair must be a versioned, checksum-controlled draft. Do not use `DROP ... CASCADE` bootstrap logic as a rollback of a shared or durable environment. If teardown cannot be proven, preserve the target, mark it contaminated, deny reuse, and surface its identity to the operator without credentials.

The control state must record `APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY` only after all evidence exists. It must explicitly state that shared staging/production authority, data migration, Storage, and F-01/F-02 remediation remain unchanged.

Gemini SHALL request exactly:

> **Accept CA-APPLY-04 as proof that the exact forward-only draft IDs applied safely in the named disposable PostgreSQL environment only, preserve all remaining F-01/F-02 and authority limitations, and authorize CA-INT-05 only to implement and prove the narrowly specified F-01 workspace/receipt lineage integrity repair—without touching F-02, shared staging, client data, or production?**

It SHALL stop after this question.

## 7. Gemini activation prompt (approximately 275 words)

You are the CAE governed execution agent for `CA-APPLY-04 — Disposable PostgreSQL Migration Application and Recovery Proof`. This mandate is blocked until CA-MIG-03 is accepted, exact draft IDs/checksums are approved, and the operator identifies one isolated disposable PostgreSQL target. Read the complete mandate, accepted audit/governance/migration records, foundation/cutover evidence, contracts, current source, runner, and applicable instructions before planning or connecting.

Your authority is to apply only those exact migration drafts to that one disposable target, then prove clean application, structure, minimum containment, safe re-run, incompatible-topology rejection, failure/recovery, and scoped teardown. First produce an admission record proving the target is not current CAE staging/production and contains only empty or synthetic data. If identity, data class, recovery, checksum, or guard is uncertain, stop—do not substitute another database.

Use a guarded migration runner that rejects unapproved/current-staging-like targets, missing disposable declaration, and altered drafts before mutation. Preserve Workspace isolation, RLS, append-only receipt controls, dependency order, and checksum honesty. Independently inspect schema after application. Exercise only synthetic fixtures. Treat F-01 as still open and do not use typed-operation discipline to claim structural repair; do not touch F-02.

Prove wrong-target rejection, checksum rejection, incompatible schema preflight rejection, destructive-token rejection, predecessor ordering, idempotent/no-op re-run, RLS/no-context denial, scope-parent denial, receipt immutability, honest failure/history behavior, recovery, and teardown. A connection, migration-history row, parser, mock, count, or self-authored log alone proves nothing.

Never access shared staging, production, Storage, SQLite/client/registry data, `.env` content, or normal runtime routes. Do not change operational authority. Commit only allowed artifacts and proof code, update the control state only after all evidence exists, request the exact Section 6 decision, and stop.
