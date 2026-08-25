# Gemini Execution Mandate — Phase 10 / CA-IMPL-01A

**Status:** `DRAFT — BLOCKED UNTIL CA-TS-01 IMPLEMENTATION-GATE APPROVAL`  
**Phase ID:** `CA-IMPL-01A`  
**Title:** Tenant-Scoped Staging Relational, RLS, and Private-Storage Foundation  
**Execution classification:** Exact approved staging implementation allowlist only  
**Required decision:** Pass TS-CAE-TEN-001 Gate A–I review and authorize CA-IMPL-01A only  
**Gate:** `VERIFY -> OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by the approved `TS-CAE-TEN-001` Tech Spec, its Gate A–I review, operation/transition design, test/proof plan, implementation allowlist, risk/rollback register, and all ratified predecessor constitutions, requirements, and aggregate authority contracts. It also remains subject to the CAE Governance & Specification Bridge Bundle v3, especially the Implementation Gate, State and Transition Control, PostgreSQL State Model, Semantic Operation API, Reality-Contact, Test Governance, and State-Control Test/Proof protocols.

This is the first phase permitted to change staging implementation. It realizes the approved data-protection foundation for:

```text
Workspace -> Membership / approved operator access -> Engagement -> Guest
  -> MediaAsset / evidence metadata boundary -> HarnessRun / receipt-ready foundation
```

The implementation makes the relationship boundary real before any typed runtime path. PostgreSQL/Supabase is target authority for new foundation records, but no aggregate is promoted to `POSTGRES_AUTHORITATIVE`. Existing SQLite/service-local records retain their CA-STATE-01 authority. This is not bulk migration, user rollout, API launch, client portal, or WP-09 replacement.

CA-IMPL-01A implements only the Tech-Spec file allowlist. If the allowlist, migration contract, RLS/Storage model, retention decision, or acceptance criterion is incomplete, the agent SHALL stop as `BLOCKED`; it shall not add a framework default, broad service role, or shared abstraction.

## 2. Mandatory reading before action

Before planning, editing, applying a migration, or accessing staging, Gemini SHALL read in full:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. Approved `TS-CAE-TEN-001` Tech Spec, Gate A–I review, operation/transition contracts, test/proof plan, implementation file allowlist, and risk/rollback register.
3. Approved CA-STATE-01 authority matrix, aggregate contracts, crosswalks, quality/quarantine register, and decision ledger.
4. Approved CA-SPEC-01 PRD/FR set and all ratified CA-CAN-01A/B/C constitutions, relation map, and contradiction closure.
5. Relevant WP-02A through WP-09 foundation, RLS, Storage, operation, receipt, reality-contact, and vertical-slice records.
6. Every actual source, migration, test, and service `AGENTS.md` identified by the approved implementation allowlist before modifying it.
7. Active staging configuration through secret-safe inspection. Credentials/values SHALL NOT appear in output, docs, commits, logs, or receipts.

First produce a concise plan mapping every file to Tech Spec, contract, migration order, test, and rollback. Compare the working tree against the allowlist. Unrelated/overlapping change, environment mismatch, or missing recovery plan is a stop condition unless operator-resolved.

## 3. Exact authorized implementation scope

Subject to the approved allowlist only, the agent MAY implement:

1. PostgreSQL/Supabase staging migrations for Workspace-scoped first-slice tables, stable relational fields, legal parent-chain constraints, temporal/append-only records where designed, and current-projection support where required.
2. Database constraints, indexes, constrained views/functions, and migration bookkeeping needed to enforce the approved containment model. Constraints must prevent cross-Workspace parent/child relationships rather than relying on an application `WHERE` clause.
3. RLS policies and server-side authorization-context mechanisms designed in the Tech Spec, including normal membership and bounded operator-grant behavior. Service-role credentials remain server-only infrastructure credentials and must not become ordinary runtime bypasses.
4. Private Storage bucket/path/policy and media-metadata foundation: scope-bearing keys, designed short-lived access, and no raw-media blobs in ordinary rows.
5. Approved typed model/repository scaffolding, with no normal agent direct-write path or CA-IMPL-01B lifecycle.
6. Migration, structural, RLS, Storage, containment, and cleanup test code expressly named by the Tech Spec.

Only disposable synthetic staging fixtures approved by the test plan may be initialized. They are identifiable/scoped, receipted where required, and cleaned up or force-rolled back. Never use real client, Guest, legacy, or operator data.

## 4. Prohibitions and hard stops

Gemini SHALL NOT:

- migrate, backfill, delete, merge, or dual-write any legacy records;
- change a source aggregate’s authority state or declare PostgreSQL/Supabase authoritative;
- implement or expose the CA-IMPL-01B typed operations, an external API route, agent orchestrator, background worker, user workflow, client portal, search/vector retrieval, analytics, or registry runtime consumer;
- auto-link Guests by name, email, transcript, embedding, or source-system identifier;
- add global Person, generic Tenant, generalized state-engine, or schema-per-Workspace design;
- alter objects outside the approved file allowlist, or alter unrelated existing WP-02–WP-09 behavior;
- put secrets, service keys, signed URLs, raw client data, or storage objects in Git, test fixtures, receipts, or docs;
- report a Storage path, table, RLS policy, migration exit code, or self-authored receipt as independent proof of isolation.

If an external Storage effect cannot be cleaned up, a migration cannot be rolled back/forward-repaired as specified, a scope constraint is impossible under the approved model, or a test needs an unapproved runtime operation, the agent SHALL stop. It must record the failure and recovery requirement rather than widening this phase.

## 5. Required implementation laws

Operational records use the approved scope and legal parent chain. `workspace_id` is tenant boundary; `guest_id` is not universal. Direct/inherited scope follows the Tech Spec. Parent/child relations enforce the same Workspace through composite keys, constraints, or equivalent controls.

Normal access derives Workspace/privileges from trusted membership or operator-grant context. Caller IDs are claims, not authorization. Grants remain purpose/time/role/Workspace-bounded and auditable; no unbounded cross-workspace query, export, identity link, or Storage access.

Storage is private by default. MediaAsset records approved lineage, key/reference, version, count, MIME/type, checksum, provenance, lifecycle, access/retention, and links. Hash claims require fresh readback in approved topology. URL is not authenticity; `VERIFIED` cannot be self-attested.

Preserve append-only state/event/receipt history and required current projection. Do not introduce alternate local authority or an opaque JSONB warehouse; JSONB is bounded and cannot replace relations/stable semantics.

## 6. Required verification and evidence

Run exactly the approved verification plan, at least covering:

```text
structural migration and idempotent migration-runner behavior
Workspace parent-chain constraint acceptance and rejection
two-workspace RLS read/write isolation through ordinary role context
operator-grant expiry/purpose/scope denial and allowed bounded access
cross-workspace relation, receipt, and media metadata rejection
private Storage allowed read, denied cross-workspace read, byte readback/hash
path/status without matching bytes rejection where applicable
idempotent fixture retry with scoped keys and no duplicate lineage
current-projection/history behavior where foundation tables establish it
rollback or forward-repair rehearsal, fixture cleanup, and fresh-read absence check
```

Proof uses two synthetic Workspaces and a production-shaped staging target. Same-Workspace happy path, mock Storage, or admin bypass cannot prove E3 isolation. Each material test records behavior, environment, independent evidence, false-proof risk, cleanup, and limits.

Required adversarial cases include caller-forged Workspace IDs; omitted/mis-set authorization context; service-role misuse; parent-chain mismatch; source/target scope collision; same email across Workspaces; expired or reasonless operator grant; fabricated receipt/evidence reference; Storage key guess; stale signed access if applicable; duplicate operation/migration retry; and a migration history row without required structural effects.

The review separately states what is proven: staging foundation, constraints, RLS/Storage, fixture isolation, cleanup. It states what is not: broad migration, authority promotion, typed runtime, semantic/taste/E4 proof, live workflow, or production readiness.

## 7. Required artifacts, completion, and operator gate

The agent SHALL produce only the implementation artifacts defined by the allowlist, plus:

- `docs/cae/implementation/CAE_CA_IMPL_01A_FOUNDATION_PROOF.md`;
- `docs/cae/implementation/CAE_CA_IMPL_01A_MIGRATION_AND_ROLLBACK_LEDGER.md`;
- an evaluation manifest under `docs/cae/evaluations/` only if the Tech Spec requires one;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Proof record includes commits, checksums, commands/results, non-secret environment identity, evidence/receipt refs, negative outcomes, cleanup, constraints, risks, non-claims. Commit only allowed files and preserve unrelated changes.

CA-IMPL-01A completes only if foundation is applied/verified at specified fidelity, all adversarial cases have honest results, rollback/repair/cleanup are evidenced, and no prohibited expansion occurred.

Gemini SHALL request exactly:

> **Accept CA-IMPL-01A as E3 staging foundation evidence for tenant containment, RLS, and private Storage, maintain all non-claims, and authorize CA-IMPL-01B only: typed semantic operations and one narrow runtime path?**

After asking, Gemini SHALL stop. It has no authority to expose an operation, migrate legacy data, change aggregate authority, or begin CA-IMPL-01B.

## 8. Gemini activation prompt (approximately 250 words)

You are the CAE governed execution agent for `CA-IMPL-01A — Tenant-Scoped Staging Foundation`. This mandate is blocked unless TS-CAE-TEN-001 passed its Gate A–I review and the operator authorized this phase only. Read this mandate, the approved Tech Spec, exact implementation allowlist, migration contracts, proof plan, rollback register, and all referenced source instructions before planning or editing. First make a concise execution plan that maps every file and staging action to a permit, test, and rollback step. Stop if the allowlist, staging identity, recovery path, or required contract is incomplete.

You may implement only the approved staging relational containment, migration scaffolding, RLS, private Storage policy, bounded typed model/repository scaffolding, and verification code. You may create only disposable synthetic fixtures. You must not migrate/backfill/delete source data, alter legacy authority, activate dual-write, expose typed operations or APIs, build orchestration, add generic tenancy/person/state infrastructure, or use secrets/client data. Never expand a table, policy, or abstraction beyond the Tech Spec.

Enforce Workspace as tenant boundary through legal parent chains and database controls; Guest is not a universal key. Resolve access server-side from membership or purpose/time/scope-bounded operator grant. Keep Storage private, metadata relational, and bytes independently read back/hashed. A table, policy, path, URL, migration exit code, or receipt is not proof by itself.

Run the approved E3 two-Workspace tests and every adverse case, including scope forgery, RLS/service-role bypass, parent mismatch, grant expiry, cross-workspace media/receipt links, hash mismatch, duplicate retry, rollback/repair, and cleanup. Record commands, checksums, evidence, limits, and non-claims. Update the control state, commit allowed files only, ask exactly the Section 7 decision, and stop before CA-IMPL-01B.
