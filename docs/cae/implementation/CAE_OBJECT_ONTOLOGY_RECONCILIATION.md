# CAE Object / Ontology Reconciliation

**Work package:** WP-01 — Canonical Object / Ontology Reconciliation  
**Status:** `MODEL_COMPLETE_PENDING_OPERATOR_REVIEW`  
**Date:** 2026-08-23  
**Execution boundary:** documentation and evidence reconciliation only. No runtime behavior, database schema, registry data, migration, API contract, or test was changed.

## Objective

Establish the canonical role of the principal CAE objects before selecting a shared state model or implementing semantic operations. A similarly named class, table, YAML asset, endpoint, or document does not establish canonical ownership.

## Bounded package contract

| Field | Definition |
|---|---|
| Architectural scope | Canonical roles, object boundaries, evidence classification, and ownership/collision decisions across Phase 0–7 and verified brownfield implementations. |
| Allowed changes | `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` and this reconciliation record. |
| Prohibited changes | Production code, API contracts, migrations, database provisioning, registry data, state-transition behavior, harnesses, and tests. |
| Dependencies | WP-00 Reality Map; Phase 0–7 object definitions; AIR, Pipeline, API, Campaign, and shared runtime evidence. |
| Expected artifacts | This role map, collision log, decision entry criteria for WP-02, and updated durable control state. |
| State transition | `OPERATOR_REVIEW -> MODEL` only after an explicit state-authority decision. |
| Tests | No test is applicable to this documentation-only package; source locations were read and cross-compared. |
| Evidence required | Canonical source reference, concrete brownfield evidence, and an explicit classification for every reconciled object. |
| Operator decision | Approve role boundaries and authorize WP-02 as a specification-only state-model reconciliation package. |
| Rollback | Revert only these two documentation artifacts; no runtime state or architecture has changed. |

## Canonical role rules

1. Role precedes schema; storage does not redefine ontology.
2. A target object becomes executable only after an approved contract, authoritative persistence decision, operation boundary, and evidence path exist.
3. SDA directs semantic direction and geometry; SFL modulates perceptual delivery. Neither silently replaces the Primitive Registry.
4. PostgreSQL/Supabase is the adopted target for durable CAE operational state, but no active implementation or migration is claimed until WP-02 is promoted and completed.
5. Existing local SQLite models remain verified brownfield facts. They are not, by themselves, canonical CAE authority.

## Reconciliation matrix

Classification describes the present executable status, not the quality or importance of the target specification.

| Canonical CAE object / system | Canonical role | Brownfield evidence | Classification | Reconciliation disposition |
|---|---|---|---|---|
| World / audience / guest | scoped external reality and participant context | Campaign and interview paths hold local campaign/guest-related data; no verified CAE-wide `World` or `Audience` object | PARTIAL | Define canonical context identity and ownership before shared persistence. |
| Activative Context | evidence-bounded semantic situation used by later discernment | AIR exposes a typed `ActivativeContext`; its lifecycle and authority remain service-local | PARTIAL | Preserve AIR as an implementation candidate, not canonical authority. |
| Context matrix / relational field | relation model joining entities, conditions, signals, and tensions | AIR includes `MatrixOfEdging` and related semantic models; Phase 3/4 target contracts are broader | PARTIAL | Reconcile names, relations, and evidence preconditions in WP-05 contracts. |
| Signal | observed or derived evidence-bearing indicator | Phase target documents define it; AIR/campaign data provides local adjacent concepts | DOCUMENT_ONLY | Do not infer a canonical signal schema from local fields. |
| Tension | named live incompatibility or friction in the context | Phase 4 specifies it and its state model; no verified CAE-wide runtime state machine | DOCUMENT_ONLY | First define state/transition contract in WP-02. |
| Pressure / Pressure Field | directional force produced from a validated tension configuration | Phase 4 specification only | DOCUMENT_ONLY | Retain as a target object; no code or storage claim. |
| Webhook / Activation Event | activation mechanism and resulting material event | API webhooks and campaign events exist, but do not prove Phase-4 semantic webhook behavior | DUPLICATED | Separate transport webhooks from canonical semantic activation events. |
| Authenticated Evidence | evidence that passed source, span, and authentication requirements | Interview contracts include evidence-related objects; AIR carries evidence references and epistemic transitions | PARTIAL | Adopt one evidence identity/lineage contract before shared-state design. |
| Interview evidence packet | bounded source material for semantic assessment | Interview Expression and Composer services have local repositories/models; Phase 5 target packet is not shown as an end-to-end consumer contract | PARTIAL | Keep service records; define a cross-service semantic packet boundary in WP-05. |
| Primitive Registry | canonical semantic primitives, families, compatibility, and geometry | AIR persists primitive/archetype-oriented records; no reconciled primitive authority or registry gateway | PARTIAL | Resolve registry authority/crosswalk ownership before WP-04 migration. |
| SDA Registry | semantic direction and geometry migration input | Inherited versioned YAML assets exist; no runtime resolver or verified database path | SCHEMA_ONLY | Preserve IDs, versions, lineage, rationale, and crosswalks; migrate only after integrity validation. |
| SFL Registry | perceptual delivery / experience modulation subordinate to SDA | Inherited YAML assets exist; failure corpus references missing family IDs | CONFLICTING | Quarantine unresolved references; do not invent records. |
| Coalition / Edge Product | assessed combination of primitives producing a bounded semantic edge | AIR has coalition and candidate contracts; Phase 6 target lifecycle/evidence role is not integrated CAE-wide | PARTIAL | Reconcile lifecycle, compatibility, receipt, and consumer contract before runtime slice. |
| Archetype Container / SFL Stack | experiential packaging and perceptual modulation of an eligible semantic program | AIR has archetype program candidates; Phase 7 semantic/SFL contracts are target-only | PARTIAL | Enforce Phase 7 subordination rule in registry and operation contracts. |
| Semantic Program / Execution Packet | typed handoff from semantic decision to realization | Pipeline compiler/run service and Builder artifacts are adjacent, but no verified CAE semantic-program handoff exists | PARTIAL | Define handoff ownership, versioning, and receipt requirements before integration. |
| CAE operational state | durable current projection for campaign, workflow, evidence, semantic, evaluation, and outcome state | Multiple SQLite repositories and migrations; no active shared PostgreSQL/Supabase layer | DUPLICATED | WP-02 must establish a transition and migration specification before code changes. |
| State transition | checked movement with validator, effect, failure path, idempotency, and receipt | Pipeline, campaign, and AIR implement local transitions | DUPLICATED | Establish a CAE-wide transition-contract registry; preserve local behavior during migration. |
| Events / immutable receipts | historical record and independent proof of a consequential operation | Shared runtime plus several services persist local events/receipts | DUPLICATED | Define canonical envelope, provenance, evidence-link, and anti-self-attestation requirements. |
| Semantic operation | authorized typed interaction with CAE state/evidence | Local typed service methods and routes exist; no cross-service governed gateway | ABSENT | Do not design normal state interaction before WP-02 authority/migration decision. |
| Harness / runbook binding | executable doctrine and environment-fidelity evidence | Pipeline has run service; Builder has 49 Stage 1/2 artifacts; no verified shared specimen runtime harness | PARTIAL | Reconcile only after object/state/registry contracts (WP-06). |

## Collision and contradiction log

| ID | Collision or contradiction | Evidence | Required disposition |
|---|---|---|---|
| OBJ-001 | “Context,” “Matrix of Edging,” and related AIR models resemble Phase 3/4 concepts but do not prove the full target relation/evidence semantics. | `services/air/src/cmf_activative_intelligence/domain.py`; Phase 3/4 specifications | Keep AIR models as candidate implementations; specify canonical relations and evidence requirements before adoption. |
| OBJ-002 | API-level webhooks are transport mechanisms; Phase 4 `Webhook` is a semantic activation construct. | API router surfaces; Phase 4 object definitions | Maintain separate names/types and do not map one to the other without a contract. |
| OBJ-003 | Pipeline/campaign/AIR each govern local states, events, and receipts, while the target assigns shared durable authority to PostgreSQL/Supabase. | `api/main.py`; local migrations; shared runtime database utility; bridge doctrine | WP-02 must specify coexistence and migration disposition without changing behavior. |
| OBJ-004 | AIR primitive/archetype persistence overlaps conceptually with inherited SDA/SFL inputs and the target Primitive Registry. | AIR domain/repository evidence; SDA/SFL ZIP inventories; Phase 6/7 specs | Operator must nominate canonical registry authority and crosswalk owner before WP-04. |
| OBJ-005 | SFL failure-corpus references include family IDs absent from its supplied family registry. | `sfl.zip` inventory/reference check | Preserve and quarantine the corpus reference; resolve through accountable source lineage only. |
| OBJ-006 | Builder Stage 1/2 files provide output evidence, but they are not executable harness manifests nor proof of Pipeline handoff. | `stage1_output`; `stage1_output/specs`; absence of `storage/harness-library` | Treat as evidence inputs until WP-06 defines an executable harness/runbook binding. |

## Relation and ownership boundaries

```text
World / Audience / Guest
  -> Activative Context
  -> authenticated Signals and Evidence
  -> Tension / Pressure / relational field
  -> SDA-directed Primitive candidate and Coalition
  -> Edge Product
  -> Archetype Container + SFL Stack (perceptual delivery only)
  -> Semantic Program / Execution Packet
  -> Pipeline / realization surfaces
  -> Events, receipts, evaluation, and outcome evidence
```

This is a target role sequence, not evidence that the current runtime already performs it. Existing Pipeline, AIR, Campaign, Interview, Builder, VAE, and Studio surfaces are possible bounded adapters only after their contract and authority are approved.

## WP-02 entry criteria and recommendation

WP-02 may begin as a **specification-only** package when the operator decides all of the following:

1. PostgreSQL/Supabase remains the target authority for CAE durable operational state; no infrastructure provisioning or data migration is authorized in WP-02.
2. Each current SQLite store will receive an explicit disposition: retain temporarily, adapter-backed, dual-read candidate, migrate, or retire. No store is silently replaced.
3. The first vertical transition to model is nominated. Recommendation: **Interview source evidence -> authenticated evidence -> AIR semantic eligibility assessment**. This is a candidate because its end-to-end runtime path is not yet proven.
4. Primitive, SDA, and SFL authority/crosswalk ownership is named before WP-04; SFL remains subordinate to SDA semantic direction and cannot replace primitives.

## Evidence and verification result

```yaml
phase_0_to_7_object_definitions: READ_AND_COMPARED
brownfield_object_evidence: READ_AND_COMPARED
canonical_role_map: COMPLETE_PENDING_OPERATOR_REVIEW
runtime_behavior_changed: false
schema_or_database_changed: false
registry_data_changed: false
tests_executed: false
reality_contact_claim: NOT_MADE
known_unresolved_collision_count: 6
```

## Operator gate

### A. What changed

Two durable governance records now identify canonical roles, current evidence classifications, and six collision/contradiction decisions. No runtime artifact changed.

### B. Why it changed

State-model and registry work would otherwise conflate target concepts with similarly named local implementations, risking duplicate authority and ontology drift.

### C. What was proven

The documented local models, local state systems, registry inputs, and target Phase 0–7 definitions can be distinguished by role and evidence class. The named collisions have concrete source evidence.

### D. What was not proven

No target end-to-end CAE flow, PostgreSQL/Supabase implementation, shared semantic API, registry resolver, or runtime semantic-program handoff is proven.

### E–F. Remaining uncertainty and what could still be wrong

Some local models may be more compatible with the target contracts than static source reading shows; live runtime and integration paths have not been exercised. Legacy data volume, migration compatibility, and the accountable SFL lineage source remain unknown.

### G. Operator inspection

Inspect the roles and dispositions for `Activative Context`, `Webhook`, `Primitive Registry`, SDA, SFL, the proposed evidence-to-AIR first transition, and the six entries in the collision log.

### H. Exact decision required

**Promote WP-01 and authorize WP-02 as a specification-only PostgreSQL/Supabase state-model reconciliation package, with no provisioning or data migration?**

