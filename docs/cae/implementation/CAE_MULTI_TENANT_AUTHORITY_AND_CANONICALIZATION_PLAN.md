# CAE Multi-Tenant Authority and Canonicalization Plan

**Status:** `PROPOSED — OPERATOR REVIEW REQUIRED`  
**Prepared:** 2026-08-24  
**Predecessor evidence:** [CAE_WP00_TO_WP09_REVIEW_EVIDENCE_HANDOFF.md](CAE_WP00_TO_WP09_REVIEW_EVIDENCE_HANDOFF.md)  
**Scope:** convert the proven CAE staging slice into a safe foundation for internally managed, client-isolated workspaces. This document authorizes no production implementation, data migration, authority cutover, or external API exposure.

## 1. Decision being proposed

CAE shall use a **shared canonical plane / isolated operational plane** model:

```text
CAE internal operator organization
├── canonical plane — shared, versioned doctrine
│   ├── ontology, taxonomy, contracts, registry snapshots
│   ├── SDA direction and geometry
│   ├── SFL perceptual functions
│   ├── Primitive definitions and controlled crosswalks
│   └── versioned harness and runbook templates
└── operational plane — observed and derived reality
    └── client workspace (tenant boundary)
        └── engagement / project
            └── guest-scoped operational history
            ├── source and immutable evidence
            ├── media references and verification facts
            ├── dynamic state history and current projection
            ├── runs, decisions, derived artifacts, and outcomes
            └── events and receipts
```

Canonical artifacts describe what CAE is allowed to mean and do. Operational artifacts describe what happened for a bounded client, engagement, and Guest. The fact that CAE is internally operated does not weaken isolation. It changes the access model: a trusted internal operator may be authorized to work across client workspaces, but access is explicit, least-privileged, and auditable. It must never make data from one client silently visible to another client, Guest, agent, run, or query.

## 2. Governing doctrine and non-negotiable laws

This plan applies the following authoritative materials:

- `Conscious Activation Engine Brownfield/cae_phase0/phase0/CA_ENGINE_OBJECT_CONSTITUTION.md`
- `Conscious Activation Engine Brownfield/CAE_Governance_and_Specification_Bridge_Bundle_v3/CAE_Governance_and_Specification_Bridge_Bundle_v3/00_BUNDLE_MANIFEST.md`
- `08_CAE_IMPLEMENTATION_GATE.md`
- `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`
- `15_CAE_POSTGRES_STATE_MODEL.md`
- `16_CAE_SEMANTIC_OPERATION_API_PROTOCOL.md`
- `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`
- the WP-00 through WP-09 evidence records and their immutable commits.

The following laws govern every package in this plan:

1. **Role precedes schema.** An object gets one primary artifact class and a class-specific constitution before its canonical schema is promoted.
2. **PostgreSQL/Supabase is the CAE operational authority.** SQLite may be retained only as an explicitly non-authoritative legacy, local-cache, test-fixture, or portable-export layer until a per-aggregate migration decision says otherwise.
3. **Canonical doctrine is shared; client operational facts are workspace-scoped.** Global registry data cannot inherit client evidence, and tenant history cannot become globally reusable merely by being useful.
4. **No implicit identity merging.** Same-looking Guest records are distinct across workspaces unless an authorized, receipted identity-link decision creates a bounded relationship.
5. **Agents use typed semantic operations.** No normal agent may directly update authoritative state or bypass workspace authorization with ad-hoc SQL.
6. **History is append-only.** Current state is a projection from state/event history, not a destructive overwrite.
7. **External media is verified, not assumed.** Raw bytes belong in private Supabase Storage/S3; PostgreSQL stores the authoritative reference, hash, byte count, provenance, lifecycle, access boundary, and receipt lineage.
8. **A passing test is not proof.** Every material claim declares fidelity, a false-proof/reward-hack case, receipts, and the limits of the claim.
9. **SDA remains semantic-direction authority; SFL remains perceptual delivery/modulation.** Neither silently replaces Primitive Registry authority.
10. **No premature general engine.** One canonical dependency chain is proved before it becomes a general tenancy or ontology framework.

## 3. Precise vocabulary and default boundaries

These are proposed canonical roles, pending their individual Object Constitutions.

| Term | Primary class | Proposed role and boundary |
|---|---|---|
| `OperatorOrganization` | Entity | The CAE-owned administrative organization. It owns platform governance, not a client’s operational facts. |
| `Workspace` | Entity | The initial client/tenant isolation boundary. A workspace owns all client-scoped operational records. No client record is global by default. |
| `WorkspaceMembership` | Relation | Binds an authenticated principal to a workspace role. It is the ordinary authorization source for client-scoped work. |
| `OperatorAccessGrant` | Policy/Contract or Relation | Explicit, time/role/reason-bounded cross-workspace authority for internal operators. Its use is receipted. It is not a client-visible membership shortcut. |
| `Engagement` | Entity | A bounded project/program inside one Workspace. It groups a client’s work without being the tenant boundary itself. |
| `Guest` | Entity | A guest as known within one Workspace. It has persistent local identity and local history only. |
| `GuestIdentityLink` | Crosswalk/Mapping Object | An exceptional, auditable link between Guest records. It must never merge or expose histories automatically. |
| `HarnessTemplate` | Canonical Structural Grammar / Execution Packet | A globally versioned procedure shape. It contains no tenant facts. |
| `HarnessRun` | Execution Packet | A Workspace- and Engagement-scoped execution of a template. Its inputs, state, evidence, receipts, and outputs are tenant-scoped. |
| `MediaAsset` | Immutable Evidence plus storage reference | The authoritative metadata and verification identity for private object-store bytes; it does not place raw media blobs in ordinary relational rows. |
| `Receipt` | Receipt/Evaluation Record | Immutable evidence of a scoped operation. It carries workspace, actor, operation, contract/version, inputs, outputs, and proof classification. |

### 3.1 Scope classification is mandatory

Every canonical table, operation, event, receipt, view, Storage path, queue message, and cache key must be classified as exactly one of:

- `GLOBAL_CANONICAL` — controlled definitions and versioned registry material; no client operational facts.
- `WORKSPACE_SCOPED` — client facts; requires a `workspace_id` and authorization.
- `ENGAGEMENT_SCOPED` — still workspace-scoped; additionally constrained to one Engagement.
- `GUEST_SCOPED` — still workspace-scoped; additionally constrained to one Guest.
- `OPERATOR_AUDIT` — access-control/audit data; visible only under explicitly governed operator policy.
- `EPHEMERAL_NONAUTHORITATIVE` — cache/fixture/export data with a declared rebuild or expiration path.

An unclassified datum is not eligible for implementation.

### 3.2 Scope & Authority Matrix is mandatory before DDL

Before any table, API, queue, cache, or Storage policy is designed, the current package must create and maintain a **CAE Scope & Authority Matrix**. This is the bridge between the 26-dimensional Object Constitution and physical design. At minimum, every proposed or inherited object records:

| Dimension | Required decision |
|---|---|
| Object and primary artifact class | What it is; no multi-class ambiguity is hidden in its schema. |
| Plane and scope classification | Canonical, operational, and the exact scope class from §3.1. |
| Authority and owner | Which system is authoritative now/at target, and who is accountable for change. |
| Mutability/history | Immutable, versioned, stateful, derived, or ephemeral; and its historical record/projection rule. |
| Parent chain | Required Workspace/Engagement/Guest containment chain, if operational. |
| Evidence and receipt | What independently proves material changes and which receipt captures them. |
| Legal write boundary | Which typed semantic operations may write it; whether controlled administration is allowed. |
| Cross-workspace rule | Forbidden, explicitly linked, aggregate-only, or not applicable. |
| Storage and consumers | PostgreSQL, Storage, cache/export classification and authorized runtime consumers. |

An object marked `PENDING` in this matrix is not promoted to DDL or runtime implementation.

### 3.3 Isolation invariants

The following must be database-enforced where feasible, then independently verified:

```text
workspace_id is immutable after creation for all tenant-scoped records.
All parent/child relations must resolve within the same workspace.
An Engagement cannot reference a Guest from another workspace.
Evidence, media, state, event, receipt, run, and outcome inherit the workspace of their root subject.
Idempotency keys are unique within an operation + workspace scope, never globally shared by accident.
Global canonical records cannot reference tenant evidence or tenant receipt IDs.
Tenant-facing queries cannot return cross-workspace facts, including counts, search snippets, vectors, signed URLs, or errors.
```

Implement the parent/child check with composite foreign keys, constrained views/functions, or equivalent database checks—not only application conventions.

`guest_id` is not a universal tenancy key. The mandatory isolation key is `workspace_id`; an Engagement- or Guest-scoped record may inherit the workspace through a legal, database-enforced parent chain where repeating `guest_id` would distort its actual role. The technical design must choose direct versus inherited scope explicitly for every relation.

## 4. Target authority and access model

### 4.1 Authoritative persistence

| Concern | Authoritative representation | Notes |
|---|---|---|
| Canonical ontology/taxonomy/contracts/registries | Versioned PostgreSQL tables | Immutable source lineage and version histories remain queryable. |
| Workspace/Guest/Engagement identity and relations | PostgreSQL typed tables | Relational constraints enforce containment. |
| Dynamic state | PostgreSQL state history plus current-state projection | Current values are never created by erasing history. |
| Events/receipts/evidence lineage | Append-only PostgreSQL records | Receipt links and hashes provide historical chain, not self-attestation. |
| Media bytes | Private Supabase Storage or S3 | Bytes must be independently read back and hash-verified at consequential boundaries. |
| Media identity/provenance/access/lifecycle | PostgreSQL | A URL alone is not proof or authority. |
| Procedures/templates | Versioned repository runbooks/Skills plus referenced version in a run | Procedures are not runtime authority. |
| Local cache/export/test fixture | SQLite/files only when explicitly classified `EPHEMERAL_NONAUTHORITATIVE` | No authority fallback after PostgreSQL cutover. |

### 4.2 Normal access path

```text
authenticated principal
  -> WorkspaceMembership or OperatorAccessGrant resolution
  -> typed semantic operation
  -> workspace/role/transition/evidence validation
  -> transactional state + event + receipt commit
  -> fresh-read verification of any external Storage effect
```

`workspace_id` must be validated from the authorization context, not trusted solely because it was supplied in an agent or UI payload. Service-role credentials are server-only infrastructure credentials; they are never exposed to browser/client code and are not a normal runtime bypass.

The default physical pattern is a shared operational schema with mandatory workspace containment and Row-Level Security (RLS), because it permits one migration path and one governed model. Schema-per-workspace is not the initial design: it duplicates migration and operational complexity without first proving that a regulatory or contractual isolation requirement needs it. A later ADR may select stronger physical separation for a specifically justified client class.

### 4.3 Operator access

Operator access is powerful but controlled:

- An operator request declares the target Workspace, operation, purpose, actor, and applicable access grant/policy.
- Each cross-workspace operation emits an immutable receipt with those identifiers.
- Bulk/cross-workspace export, search, analytics, or model-training use is a separate operation family with an explicit consent, policy, and aggregation contract. It is **not** implied by operator access.
- Initial implementation permits no automatic cross-workspace identity resolution, semantic retrieval, or vector search.

## 5. Package sequence and gates

No package may expand its scope without a new operator decision. Every package begins by reading its listed authority documents and ends by updating the durable control-state record with actual evidence, limitations, and commit.

### WP-10A — Vertical-slice containment and acceptance

| Field | Plan |
|---|---|
| Objective | Accept or reject WP-00–WP-09 as bounded staging evidence, and prevent accidental interpretation as a production or repository-wide authority cutover. |
| Architectural scope | Evidence classification, regression design, proof reproducibility, and promotion boundary only. |
| Allowed changes | Evidence documentation, test manifests/runners, control-state records, and narrowly scoped regression corrections if a pre-existing claim is false. |
| Prohibited changes | Production routing, legacy authority retirement, broad tenant schema, bulk data copy, new CAE feature scope. |
| Dependencies | WP-00 through WP-09 handoff and their configured staging environment. |
| Required artifacts | Acceptance report, regression ledger, unambiguous claim/non-claim matrix, and operator decision request. |
| Evidence | Re-run static evidence checks; selectively reproduce E3 proof in disposable staging; record environment identity, receipts, rollback and cleanup. |
| Operator decision | “Accept WP-09 as bounded staging evidence and authorize CA-MAP-01?” |
| Rollback | Revert only the corrective documentation/test commit; all proof fixtures remain disposable. |

**Transition:** `OPERATOR_REVIEW -> VERIFY -> OPERATOR_REVIEW`. It cannot transition to `PROMOTE` as a general production claim.

### CA-MAP-01 — Scope, authority, and canonical/operational-plane map

| Field | Plan |
|---|---|
| Objective | Establish the authoritative plane, scope, ownership, current/target persistence, and legal parent chain for all first-slice objects before constitution prose or DDL. |
| Scope | The Canonical Plane objects consumed by the first slice and the Operational Plane objects `Workspace`, `Engagement`, `Guest`, `MediaAsset`, `HarnessRun`, `Receipt`, their access relations, and inherited brownfield counterparts. |
| Allowed changes | Scope & Authority Matrix, plane map, authority/collision register, and explicit `NEW`/`EXTEND`/`ADAPT`/`RETAIN`/`DEFER` decisions. |
| Prohibited changes | SQL migrations, runtime model changes, RLS policies, identity merge, legacy data migration. |
| Dependencies | WP-00 reality map, WP-09 evidence, Phase 0 object register/constitution, registry proof, and direct inspection of relevant legacy sources. |
| Required artifacts | Versioned matrix described in §3.2; canonical/operational plane map; object-to-existing-source crosswalk; unresolved-authority register. |
| Tests/evidence | Static coverage validation: no first-slice object is missing scope/authority/parent/write boundary; adversarial review of a false global classification and a false Guest scope. E1 is sufficient because this makes no runtime claim. |
| Operator decision | Approve the first-slice plane and scope map, including the statement that Workspace—not Guest—is the initial tenant boundary. |
| Rollback | Matrix decisions are versioned/superseded. No runtime state exists. |

**Transition:** `MODEL -> OPERATOR_REVIEW`. CA-CANONICAL-01 cannot start until this map is approved.

### CA-CANONICAL-01 — Tenant boundary and pilot Object Constitutions

| Field | Plan |
|---|---|
| Objective | Ratify the minimum dependency chain that makes client isolation and Guest history unambiguous before schema design. |
| Canonical objects | `Workspace`, `WorkspaceMembership`, `OperatorAccessGrant`, `Engagement`, `Guest`, `GuestIdentityLink`, `MediaAsset`, `HarnessTemplate`, `HarnessRun`, `Receipt`. |
| Required constitutional depth | Use all 26 Object Constitution dimensions, marking each dimension applicable, inapplicable with rationale, or pending with an explicit blocker. Apply the appropriate class-specific grammar; do not force prose uniformity. |
| Allowed changes | Canonical constitutions, glossary, object register status, neighbor/collision maps, hard negatives, and version history. |
| Prohibited changes | SQL migrations, runtime model changes, RLS policies, identity merge, legacy data migration. |
| Dependencies | Approved CA-MAP-01; Phase 0 constitution, definition grammar bundle, WP-00 reality map, existing Interview service semantics, and WP-09 evidence. |
| Required artifacts | Ten ratified constitution files, a tenant-boundary decision record, canonical relation map, scope-classification matrix, and a contradiction register. |
| Tests/evidence | Constitutional completeness validator; class/plane/neighbor collision tests; hard negatives for global-Guest conflation, operator-as-tenant conflation, and implicit Guest merge. E1 is sufficient because this package makes no runtime claim. |
| Operator decision | Confirm whether `Workspace` represents the client boundary initially; approve the no-implicit-merge rule and the exact Operator access policy. |
| Rollback | Constitutions are versioned; deprecate/supersede, never silently rewrite a ratified definition. |

**Exit criterion.** Each object has a coherent primary class, scope classification, owner, relational boundary, lifecycle, authority model, operations, error classes, examples, and hard negatives. Any unresolved concept is `PENDING`, not schematized.

### CA-SPEC-01 — Tenant and Guest operational PRD/FR reconciliation

| Field | Plan |
|---|---|
| Objective | Turn the ratified constitutions into implementation-grade requirements for the first tenant-scoped vertical slice. |
| Scope | Tenant isolation, Guest lifecycle/history, operator access, media/evidence handling, run lifecycle, receipt lineage, and authority migration. |
| Allowed changes | New CAE module PRD, FRs, traceability matrix, existing-service brownfield mappings, requirements inventory and exceptions. |
| Prohibited changes | Implementation code, DDL, production data movement, broad World/Coalition/SFL runtime requirements. |
| Dependencies | Approved CA-MAP-01, CA-CANONICAL-01 ratification, and existing system audit. |
| Required artifacts | One module PRD plus individually traceable FRs. Each material FR states source, problem, behavior, inputs/outputs, objects/relations, state/transitions, operation, validation, errors, acceptance, test class/fidelity, brownfield impact, migration, and receipts. |
| Tests/evidence | Static traceability/coverage check; adversarial review that tests whether a generic “tenant_id column” could pass while relations, Storage, or receipts still leak. |
| Operator decision | Approve the first implementation slice and explicitly defer cross-workspace analytics, automatic identity resolution, and bulk legacy import. |
| Rollback | Requirements are versioned; rejected requirements remain traceable as rejected/superseded. |

**Transition:** `MODEL -> OPERATOR_REVIEW`. This package must not make the implementation gate `READY_FOR_DEVELOPMENT` by itself.

### CA-STATE-01 — Per-aggregate authority and migration contract

| Field | Plan |
|---|---|
| Objective | Specify exactly how each existing stateful aggregate moves from its current authority to PostgreSQL/Supabase, or is intentionally retained outside CAE scope. |
| Scope | `Guest`, media/evidence, run state, receipt/event lineage, registry resolution, and their existing SQLite/service-local representations. |
| Allowed changes | Authority matrix, source inventory, migration contract, data-quality classification, dual-read/cutover/rollback design, and migration fixtures. |
| Prohibited changes | Bulk copy, deletion, broad dual-write activation, “SQLite no longer matters” declaration without aggregate proof. |
| Dependencies | CA-SPEC-01 and direct inspection of actual source schemas/data owners. |
| Required artifacts | Per-aggregate table with current authority, target authority, source count/checksum method, transform, loss policy, idempotency key, read path by phase, dual-write decision, backfill evidence, cutover criterion, rollback, and accountable owner. |
| State model | `LEGACY_ONLY -> DUAL_VERIFY -> POSTGRES_AUTHORITATIVE -> LEGACY_READ_ONLY -> RETIRED`, applied independently per aggregate. A transition is illegal without receipts, reconciliation evidence, and rollback proof. |
| Tests/evidence | Reconciliation totals/hashes, repeatable migration dry run, duplicate/retry behavior, rejected/quarantined record proof, cross-workspace boundary checks, and rollback test. E2 for real repository source; E3 before an authority claim. |
| Operator decision | For each aggregate: `MIGRATE`, `READ_THROUGH`, `RETAIN_OUT_OF_SCOPE`, `DISCARD_WITH_RECORD`, or `QUARANTINE`. |
| Rollback | Preserve source state; cutover uses an explicit prior-read path until authoritative-postgres evidence passes. |

### CA-TS-01 — Tenant-scoped operational Tech Spec

| Field | Plan |
|---|---|
| Objective | Produce the implementation-authorizing Tech Spec for one tenant-scoped Guest/evidence/run slice. |
| Scope | Exact API/service signatures, Pydantic/SQL models, migration order, RLS, Storage policy, typed semantic operations, events, receipts, error taxonomy, test fixtures, and release/rollback steps. |
| Allowed changes | Tech Spec and executable test-plan artifacts only. |
| Prohibited changes | Implementation before the CAE Implementation Gate passes `READY_FOR_DEVELOPMENT`. |
| Dependencies | CA-CANONICAL-01, CA-SPEC-01, CA-STATE-01, relevant class definition grammars, and actual brownfield service inspection. |
| Required artifacts | Gate checklist A–I, operation/transition contracts, SQL relation diagram, Storage/RLS policy, API boundary, migration sequence, exact test commands, E0–E4 claim table, reward-hack suite, and anti-centroid applicability statement. |
| Evidence | Independent spec review must prove that the design cannot gain a green test while bypassing workspace containment, operations, receipt emission, or Storage verification. |
| Operator decision | “Does CA-TS-01 pass the implementation gate and authorize CA-IMPL-01 only?” |
| Rollback | Tech Spec changes are versioned; no runtime state exists yet. |

### CA-IMPL-01 — Tenant foundation vertical slice

| Field | Plan |
|---|---|
| Objective | Implement one minimal, real Workspace → Engagement → Guest → verified MediaAsset → HarnessRun → Receipt path in staging. |
| Architectural scope | PostgreSQL/Supabase only; one narrow service boundary; no general client portal or repository-wide refactor. |
| Allowed changes | The exact DDL, migration runner, typed models, operation adapters, RLS policies, Storage policy, tests, receipts, and runbook defined by CA-TS-01. |
| Prohibited changes | Unapproved tables, client-side service credentials, implicit global Guest registry, automatic Guest merge, unbounded JSONB, direct agent SQL, production cutover. |
| Dependencies | Passed CA-TS-01 gate and staging backup/rollback plan. |
| Required operations | `create_workspace`, `grant_workspace_membership`, `create_engagement`, `register_guest`, `register_verified_media_asset`, `start_harness_run`, and operation/transition receipt capture. Names are provisional until the Tech Spec ratifies them. |
| Required data protections | Workspace-scoped RLS; composite containment constraints; server-side authorization resolution; private Storage bucket/path policy; no signed-URL logging; auditable operator grant use. |
| Tests/evidence | Structural migration test; two-workspace E3 isolation test; cross-workspace foreign-key and operation denial; RLS direct-query denial; Storage read denial; idempotent retry; duplicate ID across workspaces; operator-access receipt; restart/recovery; event/receipt atomicity; external byte readback/hash; cleanup. |
| Reward-hack cases | Caller forges `workspace_id`; service-role path bypasses membership; receipt exists without transition; object path exists without matching bytes; same email auto-merges Guests; vector/search returns another workspace’s snippet; global count leaks; a signed URL survives scope revocation. |
| Operator decision | Promote only if E3 proof demonstrates isolation and the operation is usable without a legacy-authority fallback. |
| Rollback | Transactional DB rollback where possible; external Storage cleanup with fresh-read verification; migrations reversible or explicitly forward-repaired; no legacy source deletion. |

### CA-IMPL-02 — One aggregate authority cutover

| Field | Plan |
|---|---|
| Objective | Move exactly one approved aggregate (recommended: CAE-owned evidence/media metadata created by the new slice) to PostgreSQL/Supabase authority. |
| Scope | One aggregate and its direct events, receipts, media references, and read/write path. |
| Dependencies | CA-IMPL-01 E3 proof plus an approved CA-STATE-01 migration contract for that aggregate. |
| Required evidence | Source/target reconciliation, immutable snapshot/hash, read-after-write proof, old/new divergence detection, cutover receipt, operator acceptance, and recovery rehearsal. |
| Prohibited changes | Migrating unrelated legacy Guest history or declaring all SQLite retired. |
| Operator decision | “Promote `<aggregate>` to `POSTGRES_AUTHORITATIVE`?” |
| Rollback | Return only that aggregate’s approved read path to `DUAL_VERIFY`/`LEGACY_ONLY`; do not delete target history. |

### CA-RUNTIME-02 onward — Expansion by ratified dependency chain

Only after the tenant foundation and first authority cutover are proven should CAE expand to the broader dependency sequence:

```text
World / Context
  -> Relational Intelligence
  -> Pressure / Matrix of Edging
  -> Interview / Evidence
  -> Primitive Candidates
  -> Coalitions / Edge
  -> Archetype / SDA / SFL resolution
  -> SemanticProgram
  -> Scene / Composition / IR
  -> outcome observation and E4 learning
```

Each domain receives its own constitution, PRD/FR reconciliation, Tech Spec, bounded vertical slice, and operator gate. Shared tenancy infrastructure may be reused only if the new object’s scope classification, state contract, evidence requirements, and anti-centroid requirements are explicitly compatible.

## 6. Mandatory data and storage design rules for CA-TS-01

The Technical Spec must address these items concretely, not merely state that “the system is multi-tenant.”

### 6.1 Relational containment

- All tenant-scoped primary identities use durable opaque identifiers; display names and emails are not boundary keys.
- Each child relation has a containment check to the same workspace, including joins through Guest, Engagement, evidence, execution, receipt, and outcome.
- Current-state views filter by workspace before joining tenant facts.
- Vector retrieval, full-text search, analytics, cache keys, observability tags, and background jobs carry scope explicitly.
- Deletion/retention uses a policy-defined lifecycle and receipt; it cannot silently erase historical state required for evidence.

### 6.2 Storage and media

- Object paths follow a non-guessable, scope-bearing convention such as `cae-media/{workspace_id}/{engagement_id}/{guest_id}/{media_asset_id}/{content_version}`.
- The database row records immutable hash, byte count, MIME type, source/provenance, verification lifecycle, Storage key, and evidence/receipt links.
- Access is private by default. Signed URLs are short-lived derived access mechanisms, not a database authority model.
- Storage lifecycle change requires the corresponding CAE transition/receipt and fresh-read byte verification where the claim depends on actual content.

### 6.3 State, events, and operations

- Every dynamic state carries its workspace lineage and source event/receipt lineage.
- The state transition contract identifies source, target, actor role, required evidence/validators, operation, postconditions, receipt type, error routes, and recovery path.
- State mutation + event + receipt commit transactionally where possible. External object-store effects are an explicit non-transactional boundary with compensation/cleanup verification.
- Typed errors must distinguish authorization, scope, state, evidence, registry, and contract failure. A generic failure cannot hide a tenant-boundary violation.

## 7. Evidence standard and evaluator suite

The following evidence is required before claiming that tenancy or authority is proven.

| Claim | Minimum fidelity | Independent proof |
|---|---|---|
| Constitution is internally coherent | E1 | Completeness/neighbor/hard-negative review |
| Schema represents the approved model | E1/E2 | Migration inspection plus constraints/views tests |
| Repository adapter supplies valid source structure | E2 | Real isolated repository fixture, not only synthetic objects |
| Workspace isolation works in the target topology | E3 | Two-workspace staging test through normal operations, RLS, Storage, and direct-query denial |
| A single aggregate has changed authority | E3 | Reconciliation, read/write evidence, cutover receipt, rollback rehearsal |
| Client/operator outcome or semantic/taste quality | E4 | Human/world observation and governed contrastive evaluation |

Every material verifier must include at least one adversarial countertest. A recommended tenant-isolation suite includes:

```text
TEN-STRUCT-001  tenant-scoped tables cannot omit workspace lineage
TEN-REL-001     cross-workspace composite relation is rejected
TEN-RLS-001     ordinary member cannot query another workspace
TEN-RLS-002     operator access without grant/reason is rejected
TEN-STOR-001    cross-workspace media retrieval is denied
TEN-STOR-002    matching path/status without matching bytes is rejected
TEN-OP-001      forged workspace_id cannot redirect an authorized operation
TEN-OP-002      duplicate operation is idempotent only in its true scope
TEN-REC-001     receipt cannot exist without committed scoped transition
TEN-ID-001      same name/email does not merge Guests
TEN-SEARCH-001  search/vector/cache response cannot leak another workspace
TEN-MIG-001     migration retry does not duplicate or cross-scope records
TEN-RECOVER-001 restart preserves current-state projection and receipt lineage
```

For content/semantic phases, include applicable Matrix of Edging, SDA direction, SFL modulation, anti-centroid, and hard-negative tests. Structural tenant isolation does not itself prove those quality claims.

## 8. Required operator decisions before implementation

No schema or runtime implementation begins until the operator explicitly decides:

1. **Tenant boundary:** Is one `Workspace` exactly one client boundary for the first release? If a client has multiple engagements, are they all inside that workspace?
2. **Operator model:** Which internal roles exist, what cross-workspace access is allowed, what purpose/reason must be recorded, and what audit retention applies?
3. **Guest identity:** Confirm that no automatic cross-workspace identity merging or cross-client history visibility is permitted. Specify who can create a `GuestIdentityLink`, under what consent/legal basis, and what it may reveal.
4. **Data jurisdiction/retention:** Which regions, retention periods, deletion requests, consent rules, and media restrictions apply? These cannot be inferred from architecture.
5. **Global learning boundary:** Is any de-identified aggregate learning allowed? If yes, define a later, separate policy and E4 review; it is prohibited in the first slice.
6. **First aggregate cutover:** Which CAE-owned aggregate is eligible first? The recommendation is newly created CAE evidence/media metadata, not legacy Guest history.
7. **WP-10A authorization:** Accept the WP-00–WP-09 evidence boundary and authorize containment/acceptance work only.

## 9. Completion definition

A package in this plan is complete only when:

1. its allowed scope is respected;
2. its required constitutional/specification/implementation artifact exists;
3. all applicable Implementation Gate items are evidenced;
4. required tests and adversarial countertests execute at the declared fidelity;
5. receipts and evidence lineage exist where state changes occur;
6. actual non-claims, gaps, and risks are recorded;
7. any required operator decision is made explicitly;
8. the control-state record is updated; and
9. the exact git commit is recorded.

## 10. Current next transition

```text
Current:  WP09_COMPLETE_PENDING_OPERATOR_REVIEW

Proposed:
  OPERATOR_REVIEW
    -> VERIFY (WP-10A bounded acceptance/reproduction)
    -> OPERATOR_REVIEW
    -> MODEL (CA-MAP-01 scope/authority and plane map)
    -> OPERATOR_REVIEW
    -> MODEL (CA-CANONICAL-01)
    -> OPERATOR_REVIEW
    -> MODEL (CA-SPEC-01 and CA-STATE-01)
    -> OPERATOR_REVIEW
    -> READY_FOR_DEVELOPMENT only after CA-TS-01 passes Gates A–I
    -> IMPLEMENT (CA-IMPL-01)
    -> VERIFY
    -> OPERATOR_REVIEW
```

The next permitted action is **operator review of this plan and an explicit decision on WP-10A**. No database provisioning, migration, code-path cutover, or client data import is authorized by this document.
