# Gemini Execution Mandate — Phase 21 / CA-STAGE-09

**Status:** `DRAFT — BLOCKED UNTIL CA-E3-08 OPERATOR ACCEPTANCE, SHARED-STAGING TARGET APPROVAL, AND RECOVERY ADMISSION`  
**Phase ID:** `CA-STAGE-09`  
**Title:** Controlled Shared-Staging Deployment of the Proven Foundation Repairs  
**Execution classification:** One guarded shared-staging deployment of exact E3-proven forward migrations and selected canonical topology; no production deployment, client-data migration, source retirement, or authority promotion  
**Required prior decision:** “Accept CA-E3-08 and authorize CA-STAGE-09 only for the named shared staging target, exact migration/route checksums, approved maintenance window, and proven recovery route.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; a deployed staging schema is not production authority or acceptance.

## 1. Authority, purpose, and authority boundary

CA-STAGE-09 is governed by the CAE Governance & Specification Bridge Bundle v3; accepted CA-AUDIT-01 through CA-E3-08 records; the current control state; approved CA-MIG-03 drafts; F-01 repair; operator-selected F-02 topology/route; `TS-CAE-TEN-001`; applicable contracts/constitutions; and the operator’s specific staging-deployment decision. It is the first phase authorized to mutate the named shared staging environment.

Its purpose is narrowly to install the exact migration/route chain independently proven in CA-E3-08 into the named current shared CAE staging environment, verify it against actual staging topology and approved synthetic test scope, and leave the environment in a known, recoverable state. It does not migrate existing client/legacy data, retire source tables or SQLite, expand aggregate authority, or enable production traffic.

The status boundary is absolute:

```text
exact foundation/F-01/F-02 repair chain:
DISPOSABLE_E3_PROVEN
  -> SHARED_STAGING_DEPLOYED_AND_VERIFIED

MC-CAE-MED-001 authority:
unchanged (its exact existing staging-only record only)

all other aggregates and production:
unchanged
```

CA-STAGE-09 must not represent a successful schema deployment as broad `POSTGRES_AUTHORITATIVE`, source retirement, production readiness, or a decision that unresolved deferred domains have been implemented. F-01/F-02 become shared-staging repaired only if their exact structural/route proof passes after deployment; their production status remains unchanged.

## 2. Non-negotiable admission, backup, and change-window requirements

Before planning, connecting, taking a backup, or changing a file/database, Gemini SHALL read in full:

1. Accepted CA-E3-08 environment admission, replay plan/proof, adversarial results, recovery/teardown evidence, completion record, and all prior audit/governance/migration/topology records.
2. The operator decision naming the exact shared staging target, approved migration IDs/checksums, selected route/version, maintenance/change window, recovery owner, and go/no-go authority.
3. Current migration runner/target guards, deployment conventions, DDL/route source, current staging control state, existing data/authority contracts, and all relevant `AGENTS.md` instructions.
4. `TS-CAE-TEN-001`, applicable v3 state/transition, PostgreSQL, test, proof, promotion, receipt/evidence, and semantic-operation rules.

No target is implicitly “the Supabase project in `.env`.” Admission must compare an operator-approved staging identity against configured identity using secret-safe validation and reject production-like or non-approved endpoints/projects/databases. It must record only non-secret target label/ref class, engine/version, target guard result, timezone/window, executor, migration/route checksums, expected schema version, and change owner.

Before mutation, the agent must obtain and verify a recovery package suitable for this exact shared staging target:

```text
pre-change schema and migration-history snapshot
approved data-impact inventory for affected tables
restorable backup or explicitly tested target-restore mechanism
named recovery executor and maximum decision time
forward compensating migration checksum, when recovery is not full restore
proof that recovery artifacts are accessible without emitting their secrets/data
```

The data-impact inventory must classify existing affected records as `NONE`, `SYNTHETIC`, `KNOWN_NON_CLIENT`, `CLIENT_OR_UNKNOWN`, or `QUARANTINED`. This mandate permits no transformation/migration of existing records. If any operation would touch or require interpretation of `CLIENT_OR_UNKNOWN` records, stop as `DATA_BOUNDARY_BLOCKED`. A schema migration that is preflighted as no-data-rewrite may proceed only if its contract and actual query plan/preflight prove that claim.

## 3. Exact authorized scope and staged deployment sequence

The agent may apply only the exact checksum-locked migration IDs, guarded runner, and route/adapter code that passed CA-E3-08 and were repeated in the operator decision. It may use only an explicitly run-prefixed synthetic Workspace/fixture set for post-deployment proof. No other deployment, package upgrade, configuration change, service change, Storage policy change, or data backfill is implied.

The sequence SHALL be:

1. **Change admission/freeze.** Confirm change window, target identity, clean working tree/deployment artifact, checksum lock, backup/recovery availability, data boundary, current migration history, preflight query allowlist, and no conflicting active deployment. Record a go/no-go checklist and stop if any item fails.
2. **Read-only preflight.** Independently inspect current affected schema/keys/RLS/triggers/route registrations and run only approved compatibility checks. Detect pre-existing incompatible table family, key shape, duplicate constraint, cross-scope relation, unapproved data dependency, or missing predecessor before any change.
3. **Recovery readiness rehearsal.** Verify that the named backup/restore or compensating-migration route is executable by the designated owner. Do not deliberately restore shared staging before deployment; prove accessibility/validity through the approved non-destructive check. If recovery cannot be executed when needed, do not deploy.
4. **Guarded apply.** Apply the exact forward migrations through the approved target-guarded runner. Capture non-secret runner output, statement/migration checksums, timing/lock observations, migration history, and a before/after schema manifest. A failure must halt progression and follow the documented recovery decision; no blind retry or manual SQL.
5. **Route deployment/binding.** Deploy only the selected canonical route/adapter version, if it is part of the approved scope. Prove one canonical route is registered and no unapproved shadow/fallback route becomes active. No normal workload is redirected until this proof passes.
6. **Post-deployment structural proof.** Independently inspect F-01 composite lineage enforcement, selected F-02 relation/namespace/key route, RLS, receipt immutability trigger, required grants, migration-history consistency, and absence of unauthorized schema deltas.
7. **Synthetic staging reality-contact proof.** In the approved isolated synthetic Workspace prefix only, execute the selected canonical route, two-Workspace isolation, no-context denial, F-01 direct constraint rejection, F-02 wrong-family/key denial, receipt/state/evidence effects, replay/idempotency, and one bounded failure/recovery check. Private Storage verification is required only if it is part of the approved route and must use a run-prefixed private object path.
8. **Reconciliation, cleanup, and decision record.** Reconcile expected versus actual schema/route/fixture/receipt effects; remove only run-prefixed synthetic fixtures/objects; verify no residual synthetic data; preserve the backup/recovery package according to retention; record exact results and residual risk.

## 4. Required hard negatives, proof standards, and stop conditions

At minimum, prove and record:

1. wrong/current-production-like target, altered route, or altered migration checksum is rejected before mutation;
2. preflight rejects incompatible pre-existing key/table/topology, required data rewrite, or unknown/client-data dependency;
3. backup/recovery readiness failure blocks the deployment;
4. migration failure cannot create a false applied-history record or silently proceed to route binding;
5. F-01 direct cross-Workspace receipt-evidence link is structurally rejected and leaves no row;
6. a valid same-Workspace link remains possible under intended controls;
7. selected F-02 canonical route reaches its intended family while wrong/shadowed family or key shape is denied/detected with no hidden fallback;
8. no-context/cross-Workspace access remains denied and receipt UPDATE/DELETE remains rejected;
9. route success without required state/receipt/evidence effect is detected as failure;
10. idempotent replay does not duplicate schema, target, evidence, or receipt effect;
11. synthetic cleanup cannot escape its explicit Workspace/storage/run prefix;
12. recovery/forward-repair decision preserves evidence and does not use destructive bootstrap DDL or source deletion.

A green migration history, a service startup, a successful HTTP response, a test fixture, or an operator-authored receipt alone proves nothing. Each check must identify behavior, environment, independent evidence, shortcut risk, falsification path, and cleanup/recovery result. Tests must not pass only because a privileged service role bypasses RLS; the proof must separately exercise the intended scoped/no-context boundary.

Stop as `BLOCKED`, `DATA_BOUNDARY_BLOCKED`, `REPAIR_REQUIRED`, `RECOVERY_REQUIRED`, or `SCOPE_VIOLATION` if any admission/preflight/backup condition fails; schema/route drifts; deployment expands scope; RLS/receipt controls weaken; F-01/F-02 proof fails; a normal workload/client row is encountered; a recovery path is uncertain; or cleanup is unproven. Do not compensate by changing the migration, using direct SQL, disabling controls, retrying indefinitely, or switching target.

## 5. Files, data, and prohibitions

Gemini MAY update only exact checksum-locked deployment/guard/test files previously allowed by CA-E3-08 plus:

- `docs/cae/implementation/CAE_STAGE_09_ADMISSION_AND_BACKUP_RECORD.md`;
- `docs/cae/implementation/CAE_STAGE_09_PREFLIGHT_AND_DEPLOYMENT_RECORD.md`;
- `docs/cae/implementation/CAE_STAGE_09_POST_DEPLOYMENT_PROOF.md`;
- `docs/cae/implementation/CAE_STAGE_09_RECOVERY_READINESS_AND_CLEANUP.md`;
- `docs/cae/implementation/CAE_STAGE_09_COMPLETION_RECORD.md`;
- scoped evaluation/proof scripts/tests under established locations;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Gemini SHALL NOT deploy to production; migrate/transform/delete/merge client or legacy data; retire SQLite, source tables, or an unselected F-02 family; change aggregate authority; alter unrelated application/configuration; change Storage outside approved synthetic proof prefix; print/access secrets beyond the approved runtime environment; or start CA-ACCEPT-10. It must not create an unrecoverable shared-staging state or use destructive scaffolding.

## 6. Completion, rollback, and operator gate

CA-STAGE-09 completes only when admission, backup/recovery readiness, preflight, exact guarded apply, route binding, structural proof, synthetic reality-contact tests, reconciliation, cleanup, and evidence capture pass. The Completion Record must distinguish shared-staging deployment facts from production authority; list migration/route checksums, backup/recovery identity, data-impact results, proof limits, F-01/F-02 status, all non-claims, and remaining deferred domains.

**Rollback/recovery:** Before apply, the operator must choose the approved restore or forward-compensating route. If post-deployment proof fails, stop normal progression, preserve evidence, notify the named recovery owner, and execute only that approved route after operator decision where required. Never use the destructive CA-IMPL-01A bootstrap, delete evidence/source records, or run an unreviewed ad-hoc reversal. A completed recovery must itself be verified and receipted.

Control state may record `FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY` only after all evidence passes. It must retain: no production authorization, no broad PostgreSQL authority, no client-data migration, and all non-first-slice deferrals.

Gemini SHALL request exactly:

> **Accept CA-STAGE-09 as controlled shared-staging deployment and verification of the exact proven foundation, F-01, and selected F-02 chain only; preserve every production, authority, client-data, and deferred-domain limitation; and authorize CA-ACCEPT-10 only for independent regression review, operator acceptance, and selection of at most one next aggregate—without beginning that aggregate or promoting production authority?**

It SHALL stop after this question.

## 7. Gemini activation prompt (approximately 275 words)

You are the CAE governed execution agent for `CA-STAGE-09 — Controlled Shared-Staging Deployment of the Proven Foundation Repairs`. This mandate is blocked until CA-E3-08 is accepted and the operator names the exact shared staging target, migration/route checksums, change window, recovery owner, and backup/restore or forward-repair route. Read the complete evidence chain, current source/runner, contracts, staging conventions, data boundary, and applicable instructions before planning or connecting.

Your authority is only to deploy the exact E3-proven foundation, F-01, and selected F-02 chain to that one staging target. First prove identity, checksum lock, data class, no conflicting deployment, preflight compatibility, and recovery readiness. No target is implied by `.env`; reject wrong or production-like identities. If an affected record is client or unknown, a schema change requires data rewrite, backup/recovery is not executable, or any preflight fails, stop before mutation.

Apply only through the guarded runner. Independently inspect schema, F-01 constraint, selected F-02 route/family, RLS, receipt trigger, grants, and migration history afterward. Exercise only a run-prefixed synthetic Workspace/Storage prefix, never normal workload data. Prove no-context and cross-Workspace denial, direct F-01 constraint rejection, valid local linkage, selected-route success, shadow/key-route denial, receipt/state/evidence effect, idempotency, failure/recovery behavior, and scoped cleanup.

Never promote production authority, migrate client/legacy data, retire source/SQLite/unselected family, weaken controls, use destructive bootstrap, alter unrelated services, or start acceptance. Record exact backup/recovery, checksums, environment, proofs, limits, and non-claims; if proof fails, follow only approved recovery. Commit scope-only artifacts, request the exact Section 6 decision, and stop.
