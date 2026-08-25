# Gemini Execution Mandate — Phase 08 / CA-STATE-01

**Status:** `DRAFT — BLOCKED UNTIL CA-SPEC-01 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-STATE-01`  
**Title:** Per-Aggregate Authority, Migration, and Cutover-Contract Reconciliation  
**Execution classification:** State/authority contract authoring and source inspection only; no provisioning, backfill, dual-write, or cutover  
**Required decision:** Approve CA-SPEC-01 and authorize CA-STATE-01 only  
**Gate:** `OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by CAE Governance & Specification Bridge Bundle v3, especially the State and Transition Control, PostgreSQL State Model, Semantic Operation API, State-Control Test/Proof, and Implementation Gate protocols. It also follows the accepted CA-MAP-01 authority matrix, ratified CA-CAN-01A/B/C constitutions, accepted CA-SPEC-01 PRD/FR set, [the CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md), and [the Gemini 12-Phase Execution Program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md).

CA-STATE-01 does not “migrate SQLite to Postgres.” It authors evidence-bearing contracts for each stateful or immutable first-slice aggregate that might move from a current brownfield authority to a PostgreSQL/Supabase runtime representation. Each aggregate receives its own source/target decision, transformation rules, reconciliation method, read/write phases, cutover criterion, recovery route, receipt requirements, and operator decision. No aggregate is declared migrated merely because a target schema exists, a Supabase project is configured, or a staging proof ran.

The authority axes remain separate:

```text
definition source = reviewed artifact/version/lineage defining meaning
current operational authority = store/service currently trusted for live facts
target runtime representation = verified PostgreSQL/Supabase projection
change/promotion authority = operator process that may approve transitions
```

The aggregate authority state machine is:

```text
LEGACY_ONLY
  -> DUAL_VERIFY
  -> POSTGRES_AUTHORITATIVE
  -> LEGACY_READ_ONLY
  -> RETIRED
```

Each state is an evidence-bearing contract boundary. The next state is illegal without the preconditions, reconciliation evidence, typed operation/read-path proof, receipts, rollback/recovery evidence, and operator decision defined in the contract. An aggregate may instead be `RETAIN_OUT_OF_SCOPE`, `DISCARD_WITH_RECORD`, or `QUARANTINE`; these are valid governed outcomes, not failures to be concealed.

## 2. Mandatory reading before action

Gemini SHALL read in full before planning or editing:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. The accepted CA-SPEC-01 PRD, all FRs, traceability matrix, Brownfield Impact Map, exception register, review record, and static verifier result.
3. All accepted CA-MAP-01 artifacts and ratified CA-CAN-01A/B/C constitutions/relation map.
4. `docs/cae/implementation/CAE_POSTGRES_STATE_MODEL_RECONCILIATION.md` and `CAE_POSTGRES_MIGRATION_EXECUTION_PLAN.md`.
5. `docs/cae/implementation/CAE_WP02A_FOUNDATION_PROOF.md`, WP-03 operation proof, WP-07 receipt-lineage record, WP-08 reality-contact record, and WP-09 vertical-slice record.
6. `packages/ca_runtime/src/ca_runtime/database.py`, `semantic_operations.py`, `interview_source_bridge.py`, their relevant callers, and actual service models/repositories/migrations cited by the Brownfield Impact Map.
7. Existing database migration files and staging verification scripts only for evidence of what exists; do not apply them.
8. Bundle v3 `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`, `16_CAE_SEMANTIC_OPERATION_API_PROTOCOL.md`, `19_CAE_PRD_STATE_CONTROL_AMENDMENT.md`, and `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`.

If CA-SPEC-01 contains a deferred or blocked requirement affecting an aggregate, if a current source cannot be inspected, or if a source/projection mismatch cannot be classified, the agent SHALL mark that aggregate `BLOCKED` or `QUARANTINED`. It SHALL not assume a global source authority, invent a transform, or treat an old SQLite path as disposable.

## 3. Exact aggregate scope

This phase maps only aggregates directly required by the approved tenant/Guest first slice. Expected candidates include:

```text
Workspace/access boundary records
Engagement and Guest identity/containment records
MediaAsset metadata and immutable media-evidence links
HarnessRun context/state/event/receipt lineage
new CAE-owned receipt/evidence records
```

Candidates must be confirmed from accepted requirements and executable source. The agent must separately classify each current source as SQLite, service-local persistence, existing PostgreSQL/Supabase staging structure, registry/source artifact, none/new, or unresolved. Canonical registries are not this phase’s data-migration scope except where a runtime contract must state an immutable snapshot/version dependency.

For each aggregate the agent must recommend exactly one disposition:

- `MIGRATE` — source facts require a controlled move;
- `READ_THROUGH` — legacy source remains authoritative while a bounded target representation is used under contract;
- `RETAIN_OUT_OF_SCOPE` — legitimate existing authority outside this slice;
- `DISCARD_WITH_RECORD` — explicitly non-authoritative/ephemeral data that may be abandoned with evidence;
- `QUARANTINE` — integrity, lineage, scope, consent, or semantic conflict prohibits use.

The recommended first cutover candidate is newly created CAE-owned evidence/media metadata and its receipt lineage, not historical Guest identity or all SQLite data. This is a recommendation, not an authorization; the operator decides per aggregate.

## 4. Authorized artifacts and file boundary

Gemini MAY create or update only:

- `docs/cae/state/CAE_AGGREGATE_AUTHORITY_MATRIX.md`
- `docs/cae/state/contracts/CA-STATE-01_<AGGREGATE_ID>_AUTHORITY_MIGRATION_CONTRACT.md`
- `docs/cae/state/CAE_SOURCE_TO_TARGET_FIELD_CROSSWALK.md`
- `docs/cae/state/CAE_MIGRATION_DATA_QUALITY_AND_QUARANTINE_REGISTER.md`
- `docs/cae/state/CAE_CUTOVER_AND_RECOVERY_DECISION_LEDGER.md`
- `docs/cae/implementation/CAE_CA_STATE_01_RECONCILIATION_AND_REVIEW.md`
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`
- a static contract verifier under `scripts/cae/` that reads only these artifacts.

Each aggregate contract SHALL define: aggregate identity and constitutional owner; source authority/store/version; target runtime representation; source scope/record count/checksum method; transform and loss policy; identity mapping; required evidence; state/event/receipt model; read path and write path per authority state; idempotency/retry; reconciliation query or comparison method; validation/failure/quarantine classes; security/Workspace containment; migration/cutover preconditions; postconditions; rollback/recovery; test fidelity and countertests; operator decision; and explicit non-claims.

The field crosswalk must identify source field, target semantic field, transform, null/invalid handling, scope derivation, lineage, and whether data is copied, referenced, recomputed, discarded, or quarantined. “Same name” is not a valid mapping justification. Every transform must identify who/what owns its semantic interpretation.

## 5. Prohibitions and controlled boundaries

Gemini SHALL NOT create or change SQL, migrations, tables, indexes, RLS policies, Storage buckets, object paths, service/database code, adapters, typed operation code, schemas, APIs, `.env`, data records, or source registries. It SHALL NOT run apply/provision/backfill/import/cutover scripts, alter a read path, activate dual-write, delete source data, or write an operational receipt claiming cutover. It may inspect source and run read-only/static checks only.

No contract may say “Postgres becomes authoritative” without defining the exact aggregate, prior authority state, controlled read/write behavior, evidence target, reconciliation method, recovery, and operator promotion. No contract may conflate physical migration with semantic canonicalization. No data can cross Workspaces without a ratified legal parent chain, source basis, and policy; duplicate Guest contact information never authorizes a merge.

If a contract exposes a new ontology, scope, consent, retention, jurisdiction, or cross-layer question, record it in the quality/quarantine register and stop the affected aggregate. CA-STATE-01 may recommend a later decision but cannot make it.

## 6. Required validation and anti-reward-hack review

The static verifier must prove every in-scope aggregate has exactly one disposition, current authority classification, target or retention rationale, scope/parent chain, read/write state model, transform/loss policy, reconciliation method, receipt requirement, rollback, fidelity target, countertest, and operator decision. It must reject a `POSTGRES_AUTHORITATIVE` claim without all required evidence fields.

Review hard negatives including:

- a target table existing while source records were never reconciled;
- a count-only migration check passing despite swapped Workspace ownership;
- a `guest_id` match merging different Workspace Guests;
- idempotent retry duplicating receipt/evidence links;
- a dual-write path drifting while both writes appear successful;
- a source/projection version mismatch being silently accepted;
- a Storage key copied without readback/hash and called verified;
- a `RETIRED` source deleted before recovery rehearsal;
- an operator choosing `MIGRATE` without data-quality/quarantine handling;
- a receipt self-attesting a cutover without independent reconciliation;
- a mock/empty source proving a production-shaped migration claim.

The review record shall distinguish E1 contract completeness, E2 actual repository/source inspection, and the E3 evidence later required for authority promotion. It shall preserve the WP-00–WP-09 non-claims and state that no data movement occurred in this phase.

## 7. Completion and operator gate

CA-STATE-01 completes only when every approved aggregate has a contract or a recorded out-of-scope/quarantine decision, all source/target mappings are evidence-backed, static validation and hard negatives pass, unresolved conditions are visible, and no data/runtime change occurred.

Gemini SHALL request exactly:

> **Approve the CA-STATE-01 per-aggregate dispositions and authority/migration contracts, including the recommended first cutover candidate, and authorize CA-TS-01 only: the implementation-authorizing Tech Spec and Gate review?**

After asking, Gemini SHALL stop. It has no authority to write a Tech Spec, apply a migration, provision PostgreSQL/Supabase, run a backfill, change a read/write path, or cut over an aggregate.

## 8. Gemini activation prompt (approximately 245 words)

You are the CAE governed execution agent for `CA-STATE-01 — Per-Aggregate Authority and Migration Contracts`. This mandate is blocked unless CA-SPEC-01 is explicitly accepted. Read this mandate and every required reference before planning or editing. Your authorization is only to inspect sources and author aggregate authority matrices, contracts, crosswalks, quarantine/data-quality records, decision ledger, review record, and static verifier. You are not authorized to create SQL/migrations/schema, provision Supabase, change RLS/Storage, alter runtime or read/write paths, copy/backfill/delete data, activate dual-write, or declare any aggregate cut over.

Treat canonical definition source, current operational authority, target PostgreSQL runtime representation, and promotion authority as separate axes. Map one aggregate at a time. For each, choose only one recommended disposition: migrate, read-through, retain out of scope, discard with record, or quarantine. Never infer that a staging schema or configuration makes Postgres authoritative. The state progression from legacy-only through dual-verify to retired is an evidence-bearing transition model, not a permission to skip stages.

Define exact source/target fields, scope/parent chain, transform/loss rules, idempotency, reconciliation, evidence/receipt, validation failures, recovery, fidelity, countertests, and operator decision. Preserve Workspace isolation. Same names, emails, embeddings, or row counts do not prove identity or correct ownership. A receipt cannot self-prove cutover; target tables, mock fixtures, URLs, and flags are not independent migration proof.

Run only static contract validation and hard negatives. Record source evidence, commands/results, limitations, quarantine, and no-data-movement claim. Update control state, commit only allowed files, request exactly the Section 7 decision, and stop before CA-TS-01.
