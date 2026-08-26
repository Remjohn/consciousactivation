# Gemini Execution Mandate — Phase 18 / CA-TOPO-06

**Status:** `DRAFT — BLOCKED UNTIL CA-INT-05 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-TOPO-06`  
**Title:** F-02 Table-Family Topology Reconciliation and Canonical Route Decision  
**Execution classification:** Read-led topology inventory, contract-route analysis, and operator decision preparation; read-only staging metadata inspection only if separately admitted; no rename, DDL, migration, data movement, runtime reroute, or authority change  
**Required prior decision:** “Accept CA-INT-05, preserve all shared-staging limitations, and authorize CA-TOPO-06 only to reconcile F-02 and prepare a canonical topology decision.”  
**Required completion gate:** `RECON -> MODEL -> OPERATOR_REVIEW`; no topology repair begins until the operator selects one option.

## 1. Authority, objective, and the F-02 boundary

CA-TOPO-06 is governed by the CAE Governance & Specification Bridge Bundle v3; accepted CA-AUDIT-01, CA-GOV-02, CA-MIG-03, CA-APPLY-04, and CA-INT-05 records; the active control state; `TS-CAE-TEN-001`; CA-STATE-01 contracts; and first-slice constitutions. It acts only on F-02.

F-02 is the recorded staging topology duality in which earlier WP-03 text-keyed tables and later CA-IMPL UUID-keyed tables occupy conflicting or shadowing names/expectations. The intended WP-03-shaped bridge operation, `register_verified_interview_source`, cannot execute against the CA-IMPL-01B target family as originally assumed. The cutover proof used the separately authorized typed `verify_media_asset` route. That was a bounded workaround, not a resolution of table-family authority, namespace, key shape, or bridge-contract compatibility.

The purpose of CA-TOPO-06 is to establish exactly which families exist or are claimed to exist; their schema/name/key/version/provenance differences; which contracts, operations, scripts, tests, and consumers expect each family; which route is executable and why; which future options preserve tenancy, receipts, authority, and recovery; and which operator choice is required before a repair can be designed.

No agent may choose a table family because it is newer, easier, more populated, or happens to make a test pass. A table name is not canonical authority, and resident staging existence is not correct runtime ownership.

The permitted transition is:

```text
F-02: OPEN_TOPOLOGY_DUALITY
  -> TOPOLOGY_EVIDENCED_DECISION_REQUIRED
  -> OPERATOR_REVIEW
  -> (operator only) one canonical route/topology option selected for CA-TOPO-07
```

F-01’s status, shared staging, `MC-CAE-MED-001` scope, and all production limitations remain unchanged.

## 2. Mandatory reading and optional read-only staging admission

Before planning or inspection, Gemini SHALL read in full:

1. F-02 statements and non-claims in CA-AUDIT-01, CA-GOV-02, CA-MIG-03, CA-APPLY-04, CA-INT-05, CA-IMPL-01B, CA-IMPL-02/02P, and `CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. WP-03 state/semantic-operation schema, bridge operation/contract source, CA-IMPL-01A DDL, CA-IMPL-01B typed operations/models, CA-IMPL-02 verifier/reconciliation code, and all scripts/tests naming an affected relation or route.
3. Relevant constitutions, requirements, CA-STATE contracts, `TS-CAE-TEN-001`, the current PRD truth record, Git history, migration conventions, and all applicable Bundle protocols.
4. Any service `AGENTS.md` instructions before inspecting a consumer or route.

Source inspection is mandatory. Read-only resident staging inspection is optional and requires a separate admission record. It may inspect schema metadata only: relation names/namespaces, columns/types/nullability, constraints, indexes, policies, triggers, functions, view definitions, migration history, extension/version metadata, ownership/grants, and non-identifying row estimates/counts. It SHALL NOT select payload rows, evidence bytes, Guest identities, receipt contents, or source records.

Before a remote connection, the admission record must prove endpoint/project identity, read-only role/session, query allowlist, secret-safe logging, and non-production target. The inspection runner must reject DDL, DML, `COPY`, function invocation, non-allowlisted statements, and production identities. If network policy, credentials, role, target identity, or data-boundary certainty is missing, record `ENVIRONMENT_BLOCKED`; source evidence remains valid and the phase continues without remote inspection.

## 3. Exact scope, inventory, and classification law

CA-TOPO-06 covers only relations, schemas, bridge operations/contracts, and consumers directly implicated by F-02. It SHALL map source-defined and metadata-observed topology separately. The Topology Inventory must contain:

```text
topology_item_id | relation/schema/function/operation | family label |
evidence class | provenance/creating package | key shape/type |
columns and constraints | RLS/trigger/grant state | contract/operation bindings |
runtime/test/script consumers | observed versus claimed existence |
current executability | authority/scope classification |
collision role | risk | proposed disposition | decision dependency
```

Use `SOURCE_DEFINED`, `METADATA_OBSERVED`, `DOCUMENT_CLAIMED`, `HISTORICAL`, `NOT_OBSERVED`, `CONFLICTING`, `QUARANTINED`, and `DECISION_REQUIRED` precisely. Source-defined does not mean resident; metadata-observed does not mean canonical; a contract/class does not make an operation executable.

The Contract-Route Matrix shall trace every affected operation from input/key shape through relation family, typed/bridge handler, state transition, receipt/evidence behavior, and consumer. It must show why `register_verified_interview_source` is unusable under the documented topology and why `verify_media_asset` was permitted for bounded cutover without claiming bridge compatibility.

The Operator Decision Packet must present at least three materially distinct evidence-backed options: (a) retain the CA-IMPL UUID-keyed family as future target with a versioned adapter/migration; (b) retain a WP-03-compatible family with a defined boundary; and (c) use deliberate namespaced/versioned coexistence. Each option must state authority/identity implications, migration/data work, contract/typed-operation changes, RLS/receipt effects, recovery, E3 test requirements, and non-claims. A workaround cannot become a canonical topology unless explicitly approved as temporary, with owner and expiry.

## 4. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- `docs/cae/implementation/CAE_TOPO_06_F02_TOPOLOGY_INVENTORY.md`;
- `docs/cae/implementation/CAE_TOPO_06_F02_CONTRACT_ROUTE_MATRIX.md`;
- `docs/cae/implementation/CAE_TOPO_06_F02_COLLISION_AND_OPTION_ANALYSIS.md`;
- `docs/cae/implementation/CAE_TOPO_06_F02_READ_ONLY_STAGING_INSPECTION.md` only if admission succeeds;
- `docs/cae/implementation/CAE_TOPO_06_OPERATOR_DECISION_PACKET.md`;
- `docs/cae/implementation/CAE_TOPO_06_COMPLETION_RECORD.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`;
- one read-only inspection/validation script under `scripts/cae/audit/` and a pure/local test only if remote writes are impossible.

Gemini SHALL NOT create, alter, drop, rename, or migrate relations; modify DDL, models, bridge/typed operations, APIs/services, RLS, triggers, grants, data, Storage, receipts, registries, requirements, constitutions, or contracts; run a cutover/recovery verifier; change authority; edit `.env`; or create an executable repair migration. The topology choice has not yet been made.

## 5. Required verification, adversarial review, and hard stops

The local validator must prove inventory/route/option fields are complete; every observed assertion has evidence; every affected operation has a route classification; every option states scope, migration, identity, RLS/receipt, recovery, and proof consequences; and F-02 remains `DECISION_REQUIRED`. This is E1 structural evidence only.

Actively challenge these false conclusions:

1. a source table exists, therefore it is resident or canonical;
2. one relation name means one compatible schema/key shape;
3. a typed route succeeds, therefore the specified bridge route works;
4. a count, fixture, or query proves cross-family identity/receipt compatibility;
5. a newer UUID family may replace the older family without an authority/identity/migration decision;
6. a legacy/text family may remain merely because it avoids migration;
7. an alias, view, shim, or adapter is “no change” rather than a new contract/runtime surface;
8. F-01 resolves F-02;
9. a read-only role is safe while it can invoke mutating functions or non-allowlisted SQL;
10. an unavailable connection proves topology presence or absence.

Stop as `BLOCKED` or `CONTRACT_CONFLICT` if evidence reveals a third incompatible family, an uncontracted consumer, unknown client-data dependency, identity/receipt semantic difference, no read-only boundary, or an option requiring unapproved data transformation. Record the fact; do not choose or repair.

## 6. Completion, rollback, and operator gate

CA-TOPO-06 completes only when source topology is inventoried, optional staging metadata inspection is honestly recorded or blocked, route compatibility is explicit, every known F-02 consumer is classified, at least three bounded options are presented, no option is silently selected, and local validation passes. The Completion Record must state what was learned, proven versus documented, environment/fidelity, conflicts, F-01/F-02 status, non-claims, risks, and exact operator decision IDs.

**Rollback:** This phase changes only audit/governance artifacts. Correct a wrong classification with a new attributable commit that preserves the old evidence reference. No durable state is changed and no database rollback is permitted or required.

The control state must report `F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED` only. It must not assert repair, compatibility, shared-staging readiness, or an authority transition.

Gemini SHALL request exactly:

> **Select one CA-TOPO-06 topology option and its named canonical route/identity boundary for the F-02-affected relations, preserve all other options and non-claims as rejected or deferred, and authorize CA-TOPO-07 only to implement and prove that selected topology in a new disposable environment—without moving client data, altering shared staging, or changing operational authority?**

It SHALL stop after this question.

## 7. Gemini activation prompt (approximately 265 words)

You are the CAE governed execution agent for `CA-TOPO-06 — F-02 Table-Family Topology Reconciliation and Canonical Route Decision`. This mandate is blocked until CA-INT-05 is accepted. Read this mandate, every F-02 record, WP-03 and CA-IMPL schema/operation source, contracts/constitutions, audit/governance records, control state, Git history, migration conventions, and applicable instructions before planning or inspecting.

Your authority is topology classification and an operator decision packet only. Build an evidence-classified inventory of conflicting text-keyed and UUID-keyed table families, their provenance/key/constraint/RLS/trigger shapes, their contracts/operations/consumers, and their route compatibility. Explain why the documented bridge route is not executable and why the bounded typed media route did not resolve topology. Never infer canonical authority from a name, source file, staging relation, key type, or passing test.

Inspect staging metadata only after separate admission proves non-production target identity, a read-only role, query allowlist, secret-safe logging, and no payload access. Never select client/evidence/receipt content, run service/ORM calls, invoke functions, alter `.env`, or use a write-capable script. If inspection is unavailable, record `ENVIRONMENT_BLOCKED`; absence of evidence is not a topology conclusion.

Present at least three bounded topology options with migration, identity, runtime, RLS/receipt, recovery, and E3 consequences. No option may be selected or implemented. Leave F-02 `DECISION_REQUIRED`; F-01 is separate. Commit only allowed artifacts, update control state without changing authority, request the exact Section 6 decision, and stop.
