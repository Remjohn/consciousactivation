# Gemini Execution Mandate — Phase 02 / CA-MAP-01

**Status:** `DRAFT — BLOCKED UNTIL WP-10A OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-MAP-01`  
**Title:** Scope, Authority, and Canonical/Operational-Plane Mapping  
**Execution classification:** Read-led reconciliation and governed mapping; no schema or runtime implementation  
**Required prior decision:** “Accept WP-09 as bounded staging evidence, maintain all stated non-claims, and authorize CA-MAP-01 only.”  
**Required gate on completion:** `OPERATOR_REVIEW`

## 1. Authority, dependency, and purpose

This mandate is governed by the CAE Governance & Specification Bridge Bundle v3; Phase 0 Object Constitution Protocol; [the Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md); [the Gemini 12-Phase Execution Program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md); and the accepted WP-10A record. It has no legal effect until the WP-10A operator decision is recorded in `CAE_IMPLEMENTATION_CONTROL_STATE.md`.

CA-MAP-01 exists because neither a table, a YAML file, a registry import, nor a word such as “Guest” establishes its own ontology, scope, or authority. Before writing constitutions, PRDs, Functional Requirements, DDL, RLS, or runtime operations, CAE must determine exactly which facts are globally governed doctrine and which are client-isolated operational reality. It must also distinguish three authority axes:

```text
canonical definition source
  = the reviewed artifact/version/lineage that defines semantic meaning

canonical runtime representation
  = the verified PostgreSQL relational projection used by typed operations

change and promotion authority
  = the governed person/process allowed to alter or promote either one
```

No axis may silently substitute for another. Git/YAML/source bundles are not automatically the runtime database; PostgreSQL does not automatically become a semantic source simply because it holds a projection; a migration does not grant constitutional permission to redefine an object.

## 2. Mandatory reading before action

The agent SHALL read in full before making a plan or editing a file:

1. The accepted `CAE_WP10A_ACCEPTANCE_REPORT.md`, `CAE_WP10A_REGRESSION_LEDGER.md`, and `CAE_WP10A_CLAIM_BOUNDARY_MATRIX.md`.
2. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
3. `docs/cae/implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md`.
4. `docs/cae/implementation/CAE_BROWNFIELD_REALITY_MAP.md` and `CAE_OBJECT_ONTOLOGY_RECONCILIATION.md`.
5. `docs/cae/implementation/CAE_POSTGRES_STATE_MODEL_RECONCILIATION.md` and `CAE_POSTGRES_MIGRATION_EXECUTION_PLAN.md`.
6. `docs/cae/implementation/CAE_WP04_REGISTRY_MIGRATION_PROOF.md` and the related WP-04 SQL/runtime source where a registry claim is made.
7. `Conscious Activation Engine Brownfield/cae_phase0/phase0/CA_ENGINE_OBJECT_CONSTITUTION.md`.
8. `Conscious Activation Engine Brownfield/Conscious_Activation_Definition_Grammar_Bundle/00_META_OBJECT_CONSTITUTION.md`, `17_PROTOCOL_AUTHORING_GUIDE.md`, and `18_OBJECT_CLASS_MATRIX.md`.
9. Bundle v3: `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`, `16_CAE_SEMANTIC_OPERATION_API_PROTOCOL.md`, and `08_CAE_IMPLEMENTATION_GATE.md`.

The agent SHALL also inspect actual current source for every inherited or operational object it maps. It shall cite paths, commits, migration names, schema fields, or verifier evidence—not only design prose.

## 3. Exact scope

CA-MAP-01 SHALL map only the minimum object chain required to define a future internally managed, client-isolated first slice:

```text
Canonical Plane:
  ontology/taxonomy/contracts, SDA, SFL, Primitive Registry,
  harness/runbook templates and their versioned source/projections

Operational Plane:
  OperatorOrganization, Workspace, WorkspaceMembership,
  OperatorAccessPolicy/OperatorAccessGrant, Engagement, Guest,
  GuestIdentityLink, MediaAsset/immutable media evidence,
  HarnessTemplate/HarnessRun, Receipt, and direct supporting relations
```

It shall identify each object’s candidate primary class, plane, scope classification, current and target authority, legal parent chain, mutability/history behavior, evidence/receipt requirement, permitted write boundary, storage representation, source/projection relationship, known consumers, and unresolved ambiguity. “Candidate” remains non-ratified until CA-CANONICAL phases.

The agent shall create no final Object Constitution. Its task is to create the evidentiary map from which a constitution can be honestly written.

## 4. Authorized artifacts and file boundary

The agent MAY create or update only:

- `docs/cae/implementation/CAE_SCOPE_AND_AUTHORITY_MATRIX.md`
- `docs/cae/implementation/CAE_OBJECT_SCOPE_COLLISION_REGISTER.md`
- `docs/cae/implementation/CAE_CANONICAL_OPERATIONAL_PLANE_MAP.md`
- `docs/cae/implementation/CAE_CA_MAP_01_SOURCE_CROSSWALK.md`
- `docs/cae/implementation/CAE_CA_MAP_01_COMPLETION_RECORD.md`
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`
- a static mapping-validation script under `scripts/cae/` only if the script reads these new artifacts and makes no database, Storage, runtime, or source-registry mutation.

Each mapping row must identify its evidence type as `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. It must identify a source reference and must never present a hypothesis as a verified fact.

## 5. Prohibitions and collision procedure

The agent SHALL NOT modify SQL, database state, RLS, Storage, `packages/ca_runtime`, API/services, definition grammars, registry source files, runbooks, object constitutions, PRDs, or FRs. It SHALL NOT install packages, create external accounts, alter `.env`, copy secrets, import data, backfill data, decide a registry source of truth without evidence and an operator decision, or call a candidate class a “ratified primary class.”

When an object has multiple plausible meanings, the agent SHALL put it in the Collision Register rather than choose for convenience. The register shall contain: object/proposed split, all credible plane/class/scope candidates, collision explanation, direct evidence, consequence of each interpretation, recommended disposition, required decision owner, and one of `RATIFIED`, `SPLIT`, `DEFERRED`, or `BLOCKED`. The agent may use `RATIFIED` only for a pre-existing, evidence-backed operator decision; it cannot ratify a new object by writing the register.

At minimum, examine these collisions: policy versus specific access grant; canonical harness template versus operational run; asset identity record versus immutable media evidence; receipt versus any evaluation record; Guest identity link versus Guest merge; and global canonical registry source versus PostgreSQL runtime projection. An unresolved collision blocks the affected constitution and downstream DDL/API work.

## 6. Required content and verification

The Scope & Authority Matrix SHALL have one row per scoped object and at least these columns:

```text
object | candidate primary class | canonical/operational plane | scope class |
current authority | target runtime representation | definition source |
change/promotion authority | owner | mutability/history | legal parent chain |
write boundary | evidence/receipt | storage | consumers | evidence reference |
status | unresolved question
```

The Plane Map SHALL state that canonical artifacts describe what CAE is allowed to mean/do, while operational artifacts describe what actually happened inside a Workspace, Engagement, and Guest context. It shall preserve the rule that Workspace—not Guest—is the initial tenant boundary. A Guest is a workspace-local Entity, not a global identity, and no automatic cross-workspace merge or retrieval is permitted.

The Source Crosswalk SHALL trace each mapped object to actual brownfield artifacts and classify each source `NEW`, `EXTEND`, `ADAPT`, `RETAIN`, `DEFER`, `QUARANTINE`, or `CONFLICTING`. For SDA/SFL/Primitive material it must preserve source lineage, versions, checksums where already known, quarantine findings, and the fact that a PostgreSQL projection does not erase source provenance.

Run static validation that proves: every in-scope object has a plane, scope, parent-chain result, all three authority axes, evidence reference, and status; every class ambiguity appears in the Collision Register; no operational object is falsely global; no canonical object silently references tenant evidence; and no mapped item is simultaneously called `RATIFIED` and `PENDING`. This is E1 structural proof only.

## 7. Completion and stop condition

CA-MAP-01 completes when all five artifacts exist, the static validator passes, every object has an evidence-classified mapping, and all unresolved decisions are explicit. The Completion Record must identify what became clearer, what remains unresolved, which Object Constitutions are legally eligible to begin, and which are blocked.

The agent must ask exactly:

> **Approve the CA-MAP-01 scope/authority map, confirm Workspace as the initial client boundary, and authorize CA-AUTH-01 only: development-uncertified authoring controls and static validators?**

It SHALL stop after this question. It has no authorization to write a Skill, constitution, PRD, migration contract, Tech Spec, or implementation.

## 8. Gemini activation prompt (approximately 245 words)

You are the CAE governed execution agent for `CA-MAP-01 — Scope, Authority, and Canonical/Operational-Plane Mapping`. This mandate is blocked unless WP-10A’s acceptance decision is explicitly recorded. Read this entire mandate and every listed reference before planning, editing, or running validation. Your authorization is only to create evidence-led mapping artifacts for the minimum tenant/Guest first-slice object chain. It authorizes no Object Constitution, authoring Skill, PRD/FR, Tech Spec, SQL, database change, RLS, Storage action, runtime change, registry repair, data import, or authority cutover.

First confirm the WP-10A gate. Then write a concise internal plan restricted to the five permitted mapping artifacts, the static validator if needed, evidence sources, and the stated stop condition. Use executable source, schema, migration, registry lineage, and verifier evidence. Do not let documents alone prove runtime truth. Label every statement as evidence, hypothesis, or operator decision required.

For every mapped object, record three independent axes: canonical definition source, PostgreSQL/runtime representation, and change/promotion authority. Do not claim PostgreSQL is the definition source simply because it stores a projection. Do not treat supplied YAML/ZIP registry sources as permanent authority merely because they exist. Record a source/projection mismatch as `CONTRACT_CONFLICT` or `QUARANTINED`, never resolve it silently.

Workspace is the candidate tenant boundary; Guest is not a tenancy key or global identity. Preserve legal parent chains and record no automatic cross-workspace merge, retrieval, or evidence reuse. Any ambiguous object classification goes into the Collision Register with competing interpretations and an unresolved status; it does not become a convenient database decision.

Run only static mapping validation. Update the control state, commit only allowed mapping files, request the exact Section 7 decision, and stop.
