# Gemini Execution Mandate — Phase 15 / CA-MIG-03

**Status:** `DRAFT — BLOCKED UNTIL CA-GOV-02 OPERATOR AUTHORIZATION`  
**Phase ID:** `CA-MIG-03`  
**Title:** Forward-Only PostgreSQL Migration Design and Offline Safety Rehearsal  
**Execution classification:** Migration-package design, static/offline rehearsal, and evidence preparation; no remote database, Storage, authority, or runtime mutation  
**Required prior decision:** “Approve CA-GOV-02 and authorize CA-MIG-03 only to design and rehearse safe forward-only migrations—without applying a migration or changing operational authority.”  
**Required completion gate:** `MODEL -> VERIFY -> OPERATOR_REVIEW`; a separate mandate is required before any disposable or staging database application.

## 1. Authority, purpose, and strict migration boundary

CA-MIG-03 is governed by the CAE Governance & Specification Bridge Bundle v3, the accepted CA-AUDIT-01 and CA-GOV-02 records, `TS-CAE-TEN-001`, the CA-STATE-01 aggregate contracts, the CA-IMPL-01A/01B/02 proof records, and the current control state. PostgreSQL/Supabase remains the intended CAE operational authority for the bounded promoted aggregate. This mandate does not broaden that authority, change its environment class, retire SQLite, or move any data.

The phase exists because `scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py` contains a disposable-foundation DDL sequence that drops the CAE table chain before recreating it. The historical staging proof is not invalidated by that fact; however, that script is not an acceptable reusable migration mechanism for an environment containing durable CAE state. The new migration package must be forward-only, dependency-ordered, repeatable in its preflight checks, failure-safe, versioned, and honest about what it has not yet been exercised against.

This phase designs the eventual remediation route. It does not apply it—not even to the current Supabase staging project, an unnamed local server, or a database transaction. “Offline rehearsal” means static analysis of the current DDL, a declared precondition snapshot/schema manifest, migration dependency graph, SQL safety checks, and deterministic dry-run planning. It is not a disguised database migration.

The permitted transition is:

```text
destructive foundation scaffolder recorded as historical/disposable only
  -> forward-only migration package DESIGNED_AND_STATICALLY_REHEARSED
  -> OPERATOR_REVIEW
  -> (operator only) authorize a separately bounded disposable-environment apply proof
```

No statement produced by CA-MIG-03 may say `APPLIED`, `MIGRATED`, `REPAIRED`, `E3`, `POSTGRES_AUTHORITATIVE`, or `PRODUCTION_READY` for the new package.

## 2. Mandatory reading and required current-state inspection

Before planning, editing, or writing a SQL statement, Gemini SHALL read in full:

1. Accepted CA-AUDIT-01 and CA-GOV-02 artifacts, including the Ratification Register, governance transition ledger, current durable-control record, all findings, and all non-claims.
2. `scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py`, the exact F-01/F-02/F-03 evidence, CA-IMPL-01A/01B/02/02P proofs, reconciliation ledger, recovery rehearsal, and promotion record.
3. `TS-CAE-TEN-001`, the implementation allowlist/gate review, CA-STATE-01 contracts for Workspace through Receipt/Evidence Lineage, and the relevant CA-CAN-01A/B/C constitutions.
4. Existing repository migrations, database adapters, ORM/model definitions, SQL conventions, service `AGENTS.md` files, and test tooling before choosing a migration location or format.
5. The applicable v3 PostgreSQL State Model, State/Transition Control, Semantic Operation API, Test Governance, and Phase Promotion protocols.

First create a read-only inventory of the current intended CAE schema: table, key, foreign-key relation, uniqueness rule, RLS policy, trigger/function, index, grant, expected owner, data classification, and evidence source. The inventory must separate (a) source text that defines a desired schema, (b) a recorded staging observation, and (c) present, independently inspected local source. It must never claim live schema truth without a permitted fresh inspection.

The agent may run only local file/Git inspection, checksum, static parsing/linting, and pure tests. It SHALL NOT read `.env` for credentials, connect to PostgreSQL/Supabase, use `psql`, create a local database/container, invoke migration runners, execute SQL, upload/delete Storage objects, or run any verifier that can access remote state. Secrets and client data are prohibited from all artifacts.

## 3. Exact scope, migration semantics, and allowed design

CA-MIG-03 covers only the migration mechanics of the existing first-slice `cae.*` relational foundation and the safe replacement of the destructive scaffolder. It may design no new aggregate, attribute, object constitution, semantic operation, RLS policy purpose, or authority state. It must preserve the existing approved semantic boundaries:

```text
Workspace -> Engagement -> Guest -> MediaAsset -> HarnessRun -> Receipt
                                       -> Evidence / ReceiptEvidenceLink
```

The design must use these rules:

- Every migration has a monotonic identifier, immutable checksum, purpose, owner, explicit predecessor, preconditions, ordered statements, postconditions, failure behavior, rollback/forward-repair plan, data-impact classification, and verification requirements.
- Migrations must be forward-only. Rollback means a separately versioned compensating migration or restore strategy; it never means rerunning destructive bootstrap DDL.
- `CREATE ... IF NOT EXISTS` alone is not proof of compatibility. A preflight must detect incompatible tables, columns, types, keys, indexes, policies, triggers, extensions, ownership, or existing data and stop before a future apply.
- A migration cannot silently drop, truncate, rewrite, coerce, merge, rename, or backfill durable records. Any such operation requires its own approved package, data inventory, quarantine policy, recovery evidence, and operator authorization.
- RLS, append-only receipt controls, typed-operation assumptions, Workspace isolation, and evidence/receipt lineage must be preserved or the package is `BLOCKED`.
- The current destructive scaffolder must remain as explicitly historical/disposable proof infrastructure until a later authorized retirement decision; CA-MIG-03 may not edit, delete, execute, or re-label it as production-safe.

F-01 and F-02 are dependencies, not permission to implement a repair in this phase. The package shall identify the exact migration boundary each will require. It must not present a proposed composite FK, table-family reconciliation, or bridge repair as applied/approved.

## 4. Authorized artifacts and prohibited actions

Gemini MAY create or update only:

- `docs/cae/implementation/CAE_MIG_03_SCHEMA_INVENTORY.md`;
- `docs/cae/implementation/CAE_MIG_03_FORWARD_MIGRATION_PLAN.md`;
- `docs/cae/implementation/CAE_MIG_03_MIGRATION_DEPENDENCY_GRAPH.md`;
- `docs/cae/implementation/CAE_MIG_03_SAFETY_REHEARSAL.md`;
- `docs/cae/implementation/CAE_MIG_03_F01_F02_REPAIR_BOUNDARY.md`;
- `docs/cae/implementation/CAE_MIG_03_COMPLETION_RECORD.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`;
- a versioned, **non-executable in this phase**, forward-migration manifest and SQL draft(s) under the repository’s established migration location, only after the location/format is evidenced in the inventory;
- one read-only validator under `scripts/cae/audit/` and a pure/local test under `tests/cae/` only for migration-manifest/schema-inventory integrity.

Every SQL draft must begin with a machine- and human-readable header: migration ID, status `DRAFT_NOT_APPLIED`, checksum, intended dependency, exact preconditions, data-action class, and prohibition against direct execution outside a later approved mandate. No file may include a live endpoint, credential, client identifier, fixture insert, or DML statement.

Gemini SHALL NOT change or execute existing migration/scaffolding code, runtime code, typed operations, services/API, RLS/database state, Storage, tests unrelated to the package, constitutions, requirements, contracts, registries, `.env`, receipts, or prior mandates. It shall not use a migration tool, create a migration-history row, configure CI/CD to apply the draft, alter database authority, or perform a real rehearsal. It shall not change F-01/F-02 status or make a schema decision that their future repair mandate must make.

## 5. Required safety rehearsal, adversarial checks, and failure routes

The Safety Rehearsal must derive a step-by-step *future* apply sequence from the inventory and draft manifests. For every step, list input preconditions, expected schema delta, allowed data effect (`NONE` for this phase’s proposed foundation steps unless separately approved), lock/availability concern, detection query to be run only later, postcondition, proof artifact, and compensating/forward-repair path. It must include a no-go checklist that a later apply package cannot bypass.

At minimum, statically test or inspect for these false-safe conditions:

1. any `DROP`, `TRUNCATE`, unbounded `DELETE`, destructive `CASCADE`, or implicit data-rewrite operation in a proposed migration;
2. an existing table with an incompatible UUID/text key, relation, or column type that `IF NOT EXISTS` would conceal;
3. an RLS policy or receipt immutability trigger omitted, weakened, duplicated under a shadow name, or applied to the wrong table family;
4. a migration that records a history/checksum before all required postconditions could be proven;
5. a dependency graph that applies child keys/policies before their parent tables/functions/keys;
6. an F-01 proposal that claims cross-workspace integrity without specifying how it is structurally enforced;
7. an F-02 proposal that silently chooses a table family or changes bridge semantics without an approved topology decision;
8. a purported “rollback” that relies on restoring from an unverified backup, rerunning bootstrap drops, or deleting records;
9. a claim that static SQL checks prove live PostgreSQL/Supabase compatibility;
10. a migration draft that could be accidentally discovered and applied by existing automation without an explicit `DRAFT_NOT_APPLIED` guard.

If the current repository has no evidenced migration framework/location, record `MIGRATION_FRAMEWORK_DECISION_REQUIRED`; do not invent a production deployment mechanism. If the inventory or draft reveals an unknown schema collision, existing-data question, RLS ambiguity, unbounded operation, or unverifiable recovery path, stop that migration line as `BLOCKED` and report it. Do not broaden this package to resolve the finding.

## 6. Evidence, completion, rollback, and operator gate

The local validator shall prove at least: every inventory object has evidence class and source; every planned migration has all required metadata; dependency ordering is acyclic and parents precede children; drafts contain no prohibited destructive/DML/connection patterns; F-01/F-02 remain open dependencies; every proposed step has a future preflight, postcondition, failure path, and recovery path; and no artifact claims apply or E3 proof. This is E1/E2 design evidence only.

The Completion Record must state:

```text
A. what was designed and why
B. which parts of the historic foundation are safe only as disposable proof
C. what static/offline checks were run and their limits
D. what has not been applied, tested against a database, or proven in E3
E. every blocked migration line, open topology/integrity decision, and data-risk
F. what could still fail in a real disposable apply
G. exact migration drafts and no-go checks for operator inspection
H. exact next authorization requested
```

**Rollback:** CA-MIG-03 changes no durable system state. If rejected, revert only CA-MIG-03 planning/draft/validator files through a corrective commit. Do not delete historical evidence or the old scaffolder. If a draft is wrong, supersede it with a new draft ID and preserve its checksum and rejection reason.

CA-MIG-03 reaches `OPERATOR_REVIEW` only when allowed artifacts exist; static validation and pure tests pass; the package contains no executable/destructive/DML actions; all planned migration lines have a preflight and forward-repair path; every F-01/F-02 dependency remains visibly open; and the control state truthfully reports `DESIGNED_AND_STATICALLY_REHEARSED_ONLY`. The agent shall commit only allowed files, record the commit, request the exact decision, and stop.

Gemini SHALL request exactly:

> **Accept CA-MIG-03 as a forward-only migration design and offline safety rehearsal only, preserve every listed no-go condition and open F-01/F-02 decision, and authorize a separately bounded disposable-environment migration-application proof for the exact approved draft IDs—without changing staging authority, migrating client data, or enabling production routing?**

## 7. Gemini activation prompt (approximately 265 words)

You are the CAE governed execution agent for `CA-MIG-03 — Forward-Only PostgreSQL Migration Design and Offline Safety Rehearsal`. This mandate is blocked unless CA-GOV-02 has been accepted and explicitly authorizes only design/rehearsal. Read the entire mandate, audit/governance records, current control state, foundation/cutover proof, F-01/F-02 findings, Tech Spec/contracts/constitutions, existing migration conventions, and governing Bundle protocols before planning or editing.

Your authority is narrow: create a source-evidenced schema inventory, forward-only migration plan, dependency graph, safety rehearsal, repair-boundary note, completion record, optional static validator/pure test, and only clearly marked `DRAFT_NOT_APPLIED` migration drafts where an existing repository convention supports them. Do not apply or execute anything. Do not connect to Supabase/PostgreSQL, read credentials, create a local database, invoke a migration tool, use DML, change a migration history, or run a supposedly harmless remote verifier.

Treat the destructive CA-IMPL-01A bootstrap as historical/disposable proof infrastructure, not a safe reusable migration. Preserve Workspace isolation, RLS, append-only receipts, typed-operation assumptions, and all declared non-claims. A successful static check is not live database compatibility or E3 proof.

For each future migration, specify immutable ID/checksum, predecessor, exact preflight, ordered delta, no data effect unless separately authorized, postcondition, failure/forward-repair route, and later evidence requirement. Test for destructive statements, hidden incompatible table/key/type states, missing RLS/triggers, invalid dependency order, false rollback, premature migration history, accidental automation execution, and F-01/F-02 being falsely closed. If the repository has no evidenced migration framework, request that decision rather than inventing deployment machinery.

Commit only the permitted artifacts, mark the control state `DESIGNED_AND_STATICALLY_REHEARSED_ONLY`, request the exact Section 6 authorization, and stop. Do not repair F-01/F-02, migrate data, change authority, or start the next phase.
