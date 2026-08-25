# Gemini Execution Mandate — Phase 11 / CA-IMPL-01B

**Status:** `DRAFT — BLOCKED UNTIL CA-IMPL-01A OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-IMPL-01B`  
**Title:** Typed Tenant-Scoped Semantic Operations and E3 Runtime Proof  
**Execution classification:** Exact approved typed runtime path and staging proof only  
**Required decision:** Accept CA-IMPL-01A E3 foundation evidence and authorize CA-IMPL-01B only  
**Gate:** `VERIFY -> OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by accepted CA-IMPL-01A foundation proof, the approved `TS-CAE-TEN-001` Tech Spec, operation/transition contracts, test/proof plan, file allowlist, risk/rollback register, and all prior constitutional, requirements, and aggregate-authority records. It remains subject to the CAE Governance & Specification Bridge Bundle v3, particularly the State and Transition Control, Semantic Operation API, PostgreSQL State Model, Harness/Runbook Integration, Reality-Contact, Test Governance, and State-Control Test/Proof protocols.

CA-IMPL-01B implements/proves one narrow tenant-scoped path over verified foundation. It is not a general workflow engine; it demonstrates a scoped chain without bypassing authority, RLS, Storage verification, event history, or receipt lineage:

```text
trusted actor context
  -> Workspace membership or bounded operator grant
  -> approved typed semantic operation(s)
  -> legal Workspace/Engagement/Guest containment
  -> verified MediaAsset/evidence boundary where applicable
  -> HarnessRun lifecycle boundary
  -> transactional event/current state/receipt lineage
  -> E3 independent staging evidence and cleanup
```

Exact operation names, schemas, transitions, errors, modules, and tests come from `TS-CAE-TEN-001`; this mandate invents none. The path shows a scoped operation, required verified-media boundary, run/transition effect, and receipt lineage. Omit any element not authorized by the Tech Spec.

PostgreSQL/Supabase remains target authority for new foundation data. CA-IMPL-01B does not migrate/read legacy state, change authority, or promote to production. E3 proof uses synthetic staging fixtures and normal server-side boundaries.

## 2. Mandatory reading before action

Before planning, editing, applying a migration, invoking a runtime path, or accessing staging, Gemini SHALL read in full:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` and accepted `CAE_CA_IMPL_01A_FOUNDATION_PROOF.md` / migration-and-rollback ledger.
2. Approved `TS-CAE-TEN-001` Tech Spec, Gate A–I review, operation/transition contracts, test/proof plan, implementation allowlist, and risk/rollback register.
3. CA-STATE-01 contracts for every aggregate/runtime representation the operation may touch.
4. All CA-SPEC-01 requirements and CA-CAN-01A/B/C constitutions/relation map applicable to the path.
5. WP-03 operations; WP-06 runbook; WP-07 receipts; WP-08 reality contact; WP-09 bridge proof; and actual source/tests when behavior is reused/adapted.
6. All current runtime modules, migrations, tests, service instructions, and `AGENTS.md` paths named by the allowlist before modification.
7. Staging configuration through secret-safe inspection. Never expose credentials, service keys, tokenized URLs, fixture content, or operational identifiers.

Create a concise plan mapping each code/migration/test/document change to allowlist, contract, authority state, event/receipt, test, and cleanup. Missing contract/foundation/RLS/Storage guarantee, dirty overlap, or unapproved operation is a hard stop.

## 3. Exact authorized runtime scope

Subject only to the approved CA-IMPL-01B file allowlist, Gemini MAY:

1. Implement approved typed operation handler/service/repository adapters and schemas. Normal use enters here; ad-hoc authoritative mutation is prohibited.
2. Implement approved actor/context, parent chain, membership/grant, transition/evidence/validator, typed error, idempotency, repair, and current-projection validation.
3. Implement approved HarnessRun/receipt/event integration, fixed template version, input/output, contract/template version, fidelity, and evidence lineage.
4. Implement approved MediaAsset/evidence verification only where verified bytes are claimed: fresh-read, byte count/hash, and explicit external compensation/cleanup.
5. Add the named staging tests, E3 reality-contact runner, evaluation manifest, proof documents, and source-safe fixture utilities.

Only disposable synthetic fixture Workspaces, Engagements, Guests, media metadata, runs, events, and receipts may be created. No client endpoint or generic registry. Reuse/adapt WP-03/WP-09 only by Tech-Spec decision without weakening evidence boundaries.

## 4. Prohibitions and hard stops

Gemini SHALL NOT:

- backfill, import, merge, delete, dual-write, or query through legacy client/Guest/media data;
- declare any aggregate `POSTGRES_AUTHORITATIVE`, retire SQLite/service-local authority, or change normal production read/write routing;
- expose browser/client APIs, long-running agents, background orchestration, queue workers, client dashboards, bulk search/vector retrieval, analytics, or registry runtime consumption;
- add operations outside approved contracts, bypass RLS with exposed service credentials, or issue normal operations via raw SQL;
- broaden the HarnessTemplate into a general orchestration engine or turn the runbook into state authority;
- treat receipt presence, self-attestation, successful HTTP status, object URL, Storage path, or test fixture as independent evidence without the defined operation/readback/receipt checks;
- alter unrelated WP-00–WP-09 functionality, production configuration, `.env`, registry sources, retention policy, or unapproved files.

If state/event/receipt effects cannot commit consistently, external object verification/compensation fails, recovery classification is missing, E3 needs unapproved infrastructure, or an operator decision is needed, stop as `BLOCKED` or `CONTRACT_CONFLICT`. Never replace this with mock, permissive role, or catch-all error.

## 5. Runtime and transition laws

Each operation resolves current state from PostgreSQL/Supabase staging and derives Workspace/actor authority from trusted context, not request scope. Scope, membership/grant, parent-chain, state, evidence, validator, idempotency, template-version, and transient external-side-effect errors are distinguishable where applicable.

Consequential transition processing follows the CAE doctrine:

```text
resolve current state
-> validate legal transition and actor scope
-> resolve/verify required evidence
-> run deterministic validators and required review boundary
-> persist pre-transition evidence where required
-> commit state + event + receipt transactionally where feasible
-> verify external side effect by fresh read
-> initialize/return legal target context or repair route
```

If Storage cannot share DB transaction, record its boundary and use approved compensation/recovery. Failed transition leaves source state authoritative. Retries distinguish transient from deterministic; never blindly retry deterministic violations.

Receipts record operation/transition, actor, input/output snapshots/hashes, evidence, template/contract versions, validators, fidelity, repair/error, time, and postcondition. They are lineage, not outcome proof. Current projection agrees with append-only history after success and stays unchanged after rejection.

## 6. Required E3 proof and adversarial cases

Run only the exact E3 plan from the Tech Spec, at minimum proving with two synthetic Workspaces:

```text
valid authorized operation produces only scoped state/event/receipt effects
valid operator grant is bounded, audited, and cannot become membership
cross-workspace request/parent/evidence/media/receipt linkage is rejected
forged or omitted Workspace/actor context is rejected before mutation
unverified/tampered/missing media bytes are rejected; verified bytes read back/hash
idempotent retry returns safe result without duplicate run/event/receipt lineage
invalid/stale/duplicate/legal-transition violations preserve source state
event + receipt + current projection agree after commit and not after rejection
transient external failure follows recovery; deterministic failure is not retried
test fixtures, staged Storage objects, and temporary state are cleaned or rolled back
```

Runner uses real staging RLS/Storage and approved service boundary. Mock-only, same-Workspace path, admin writes, or hard-coded IDs cannot prove claim. Each test records behavior, environment, independent evidence, shortcut, falsification, receipts, cleanup, and limits.

Adversarial cases must include service-role misuse; operator-grant expiry/reason/scope failure; same email across Workspaces; template/run version mismatch; receipt/evidence fabrication; receipt before commit; Storage object status without matching bytes; stale projection; duplicate idempotency key across scopes; source-state mutation on failure; retrying deterministic error; and a test that succeeds while a downstream receipt or event is absent.

Proof distinguishes E3 path evidence from no migration/cutover, global identity, general orchestrator, registry runtime, semantic/SDA/SFL/taste/anti-centroid outcome, E4, or production-readiness claim.

## 7. Required artifacts, completion, and operator gate

The agent SHALL create only artifacts on the approved allowlist plus:

- `docs/cae/implementation/CAE_CA_IMPL_01B_TYPED_RUNTIME_AND_E3_PROOF.md`;
- `docs/cae/implementation/CAE_CA_IMPL_01B_OPERATION_RECEIPT_LEDGER.md`;
- required evaluation manifest(s) under `docs/cae/evaluations/`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Proof document includes commits, migration/version checks, commands/results, non-secret environment, test/evidence/receipts, false-proof results, cleanup/recovery, risks, non-claims. Preserve unrelated changes and commit only allowed files.

CA-IMPL-01B completes when approved operations/path execute at E3, all negative cases have honest results, receipt/evidence/current state agree, cleanup/recovery is evidenced, and no legacy authority/data/runtime expansion occurred.

Gemini SHALL request exactly:

> **Accept CA-IMPL-01B as bounded E3 staging evidence for the tenant-scoped typed runtime path, maintain all non-claims, and authorize CA-IMPL-02 only for the one approved aggregate authority cutover?**

After asking, Gemini SHALL stop. It has no authority to cut over any aggregate, migrate legacy data, expose an API, or broaden the runtime.

## 8. Gemini activation prompt (approximately 250 words)

You are the CAE governed execution agent for `CA-IMPL-01B — Typed Tenant-Scoped Runtime Path and E3 Proof`. This mandate is blocked unless CA-IMPL-01A foundation evidence is accepted and this phase alone is authorized. Read the approved Tech Spec, exact allowlist, operation/transition contracts, aggregate contracts, proof plan, prior foundation proof, and all source instructions before planning. First map each code, migration, test, and documentation change to an allowlist entry, transition contract, evidence effect, and recovery/cleanup step. Stop if a required operation, foundation guarantee, policy, or staging condition is absent.

Implement only the approved typed operation path: trusted actor/Workspace resolution, membership or bounded operator grant, parent-chain and state validation, required verified media/evidence where applicable, HarnessRun/Template versioning, event/current projection/immutable receipt lineage, typed errors, idempotency, and explicit external-side-effect recovery. Do not use raw normal writes, expose APIs, start an orchestrator, touch legacy data, change authority, or add a general engine.

Prove the path in real PostgreSQL/Supabase staging with two synthetic Workspaces. Exercise the valid path and every specified failure: scope forgery, cross-workspace links, role/grant misuse, tampered bytes, stale/illegal transition, duplicate retry, receipt fabrication, missing downstream effect, transient recovery, deterministic non-retry, cleanup. A URL, HTTP status, mock, self-authored receipt, or same-workspace happy path is not proof. Record actual commands, receipts, hashes, environment class, evidence, limitations, cleanup, and all non-claims. Update control state, commit allowed files only, ask exactly the Section 7 decision, and stop before CA-IMPL-02.
