# Gemini Execution Mandate — Phase 06 / CA-CAN-01C

**Status:** `DRAFT — BLOCKED UNTIL CA-CAN-01A AND CA-CAN-01B OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-CAN-01C`  
**Title:** Harness, Receipt, and First-Slice Relation Integration Constitutions  
**Execution classification:** Constitution/relation reconciliation only; no PRD, schema, or runtime implementation  
**Required prior decisions:** Ratify CA-CAN-01A and CA-CAN-01B; authorize CA-CAN-01C only  
**Completion gate:** `OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by the CAE Governance & Specification Bridge Bundle v3; the Phase 0 Object Constitution Protocol; the Conscious Activation Definition Grammar Bundle; the accepted CA-MAP-01 and CA-AUTH-01 outputs; the ratified CA-CAN-01A and CA-CAN-01B constitution groups; [the CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md); and [the 12-phase Gemini execution program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md).

CA-CAN-01C is the convergence phase for the first constitutional dependency chain. It distinguishes a reusable canonical procedure, one tenant-scoped execution, the operation that may act, the event recording occurrence, and the receipt recording the controlled result.

```text
Canonical Plane
  HarnessTemplate (versioned procedural/structural doctrine)
       ↓ referenced by, never mutated by
Operational Plane
  Workspace -> Engagement -> Guest
       ↓
  HarnessRun (one bounded execution)
       ↓ typed operation / transition
  event + evidence links + Receipt
```

An existing YAML runbook, runtime “Skill,” database row, or fixture does not settle these roles. A template is not its run; a run is not an operation; an event is not a receipt; and a receipt is not semantic, taste, human, or world-outcome proof. This mandate resolves or blocks them before requirements and schemas.

## 2. Mandatory reading before action

Gemini SHALL read in full before planning, editing, or validation:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. Accepted CA-MAP-01 matrix, plane map, source crosswalk, collision register, and completion record.
3. Accepted CA-AUTH-01 authoring packages, especially constitution author and independent collision reviewer.
4. All ratified CA-CAN-01A and CA-CAN-01B constitution files and their review records.
5. `docs/cae/runbooks/evidence_to_air_first_slice_v1.yaml` and `docs/cae/skills/EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md`.
6. `docs/cae/implementation/CAE_WP06_HARNESS_RUNBOOK_INTEGRATION.md`.
7. `docs/cae/implementation/CAE_WP03_SEMANTIC_OPERATION_DISCOVERY.md`, `CAE_WP03_SEMANTIC_OPERATION_PROOF.md`, `CAE_WP07_EXECUTION_RECEIPTS_EVIDENCE_LINEAGE.md`, and `CAE_WP08_REALITY_CONTACT_AND_REWARD_HACKING.md`.
8. Actual related source: `packages/ca_runtime/src/ca_runtime/semantic_operations.py`, relevant WP-07/WP-09 verifiers, and cited migrations whenever a runtime fact is asserted.
9. `Conscious Activation Engine Brownfield/cae_phase0/phase0/CA_ENGINE_OBJECT_CONSTITUTION.md`, especially receipt/evaluation rules and the 26 dimensions.
10. Definition Grammar Bundle: meta constitution, Structural Grammar, Event, Evidence, Policy/Contract, Derived Artifact, Execution Packet, Adversarial Asset, Object Definition Checklist, Protocol Authoring Guide, and Object Class Matrix.
11. Bundle v3: State and Transition Control, PostgreSQL State Model, Semantic Operation API, Harness/Runbook Integration, Test/Proof, and Implementation Gate protocols.

There is no separate receipt grammar file in the supplied Definition Grammar Bundle. The agent SHALL use the Phase 0 `Receipt / Evaluation Record` class requirements and the relevant Event/Evidence/Execution Packet grammars without inventing an undocumented universal receipt grammar.

If either predecessor group is not ratified, a parent/scope/authority collision is blocked, or the existing runbook conflicts with accepted boundaries, Gemini SHALL stop as `BLOCKED` or `CONTRACT_CONFLICT`. It may not correct runbook/runtime code.

## 3. Exact object and relation scope

The agent MAY author constitutions for:

- `HarnessTemplate` — a candidate canonical Structural Grammar, Policy/Contract, or another single approved class; its class must be resolved from role and evidence, not the `.yaml` file extension;
- `HarnessRun` — a candidate operational Execution Packet or another single approved class; it must be distinct from the template and linked to exactly one versioned template where applicable;
- `Receipt` — candidate `Receipt / Evaluation Record`, emitted for a controlled operation or transition and linked to, but not identical with, events and evidence;
- only the direct typed relations needed to state the first-slice graph, such as `HarnessRunUsesTemplate`, `HarnessRunScopedToEngagement`, `HarnessRunConcernsGuest`, `ReceiptRecordsOperation`, and `ReceiptLinksEvidence`, if the collision reviewer finds separate Relation objects necessary.

The agent SHALL create a canonical relation map for this group and ratified predecessors. This is a legal relationship/containment model, not an SQL entity-relationship diagram. It states source, target, direction, cardinality/temporal behavior, scope inheritance, authority, evidentiary meaning, allowed operations, prohibited inference, and evidence source.

No constitution may be authored for an orchestrator, agent, generic state engine, execution queue, Outcome, SemanticProgram, Scene, Builder IR, Pipeline, registry resolver, or new generalized harness system. A type/operation/state named in existing sources may be cited only as evidence or a nearest neighbor. This phase must not generalize the one WP-06 procedural runbook into a CAE-wide runtime.

## 4. Authorized artifacts and file boundary

The agent MAY create or update only:

- `docs/cae/constitutions/CA-CAN-01C_HARNESS_TEMPLATE.yaml`
- `docs/cae/constitutions/CA-CAN-01C_HARNESS_RUN.yaml`
- `docs/cae/constitutions/CA-CAN-01C_RECEIPT.yaml`
- `docs/cae/constitutions/CA-CAN-01C_<RELATION_ID>.yaml` only when a direct relation must be independently constituted;
- `docs/cae/implementation/CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- `docs/cae/implementation/CAE_CA_CAN_01C_CONSTITUTION_AND_RELATION_REVIEW.md`
- `docs/cae/implementation/CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Every constitution SHALL account for all 26 Phase 0 dimensions as `APPLICABLE`, `INAPPLICABLE_WITH_REASON`, or `PENDING_WITH_BLOCKER`. Each file states source, runtime-projection status, promotion authority, scope/parent chain, history, operations, validators/errors, examples/hard negatives, and version history. Candidate class is not ratified without independent evidence.

The contradiction-closure record SHALL consolidate conflicts from CA-MAP-01, CA-CAN-01A, and CA-CAN-01B as `RESOLVED_BY_RATIFIED_BOUNDARY`, `DEFERRED`, `QUARANTINED`, `CONTRACT_CONFLICT`, or `BLOCKED`. It must not conceal inconsistency by changing a prior constitution without a versioned decision.

## 5. Constitutional laws for template, run, and receipt

`HarnessTemplate` is global canonical doctrine only if evidence establishes a reusable structural/procedural role. It is versioned, has no Workspace, Guest, private Storage, or mutable run facts, and identifies referenced operations/contracts. It states whether a file is source authority, representation, or migration input; it never owns tenant history.

`HarnessRun` is one bounded operational execution. It inherits Workspace containment, identifies applicable Engagement/Guest scope, references its template/version, and preserves inputs, state/event/receipt links, recovery, and outputs. It must not alter template, bypass access, or become global memory. Its existence does not prove an agent orchestrator ran.

`Receipt` answers action, actor, inputs, operation/contract version, state boundary, evidence, validators, fidelity, postcondition, timestamp, repair/failure, and output lineage. It is append-only history. It may link evidence but cannot self-authenticate it or prove outcomes beyond declared measurement/fidelity. It is not event, state projection, log, or artifact.

All direct relations must preserve Workspace isolation. A global template can be referenced from a run, but cannot reference a private run/evidence/receipt. A receipt may record a global template version and tenant-scoped run, but its access and disclosure scope must follow its operational subject. A receipt cannot link evidence, Guest, or run from another Workspace. An operation is the legal execution interface; a run is the bounded context; an event records occurrence; a receipt records controlled evidence of the action. These roles must remain distinct.

## 6. Required review and proof

Run the constitution author and independent collision reviewer in distinct passes. Review and execute at least these hard negatives:

- a `HarnessTemplate` containing a Workspace ID, Guest ID, private Storage key, mutable status, or evidence payload;
- a `HarnessRun` that does not reference a versioned template or has no legal Workspace parent chain;
- one template version silently overwritten after runs exist;
- a run mutating its template or becoming a permanent global procedure;
- a receipt inserted/claimed before the operation/transition commits;
- a receipt with no actor, operation/contract version, scope, input/output snapshot, or validator outcome;
- a receipt linked to evidence from a different Workspace;
- receipt presence treated as independent authentication or semantic/taste/outcome proof;
- an event called a receipt merely because it has a timestamp;
- an execution run granted direct database mutation instead of a typed semantic operation;
- an existing WP-06 runbook used as proof that a general agent orchestrator exists.

The review record SHALL include sources, class decisions, dimension statuses, relation-map validation, hard-negative verdicts, reviewer result, artifact hashes/versions, unresolved dependencies, and non-claims. This establishes E1 constitutional/relation coherence; cited prior executable proof may add E2/E3 evidence. It does not prove schema, RLS/Storage enforcement, orchestration, full receipt coverage, registry consumption, or E4 outcomes.

## 7. Completion and operator gate

CA-CAN-01C completes only when the three authorized object constitutions are class-resolved or explicitly blocked, the relation map connects them legally to the ratified first-slice objects, contradiction closure is honest, independent review and hard negatives are recorded, and no implementation claim is implied.

Gemini SHALL request exactly:

> **Ratify the CA-CAN-01C HarnessTemplate, HarnessRun, Receipt, and first-slice relation model; accept the recorded contradictions and deferrals; and authorize CA-SPEC-01 only for the tenant/Guest operational PRD and Functional Requirements?**

After asking, Gemini SHALL stop. It has no authority to create a PRD, Functional Requirement, migration contract, Tech Spec, schema, RLS policy, Storage policy, runtime operation, or data migration.

## 8. Gemini activation prompt (approximately 250 words)

You are the CAE governed execution agent for `CA-CAN-01C — Harness, Receipt, and First-Slice Relation Integration`. This mandate is blocked unless CA-CAN-01A and CA-CAN-01B have been explicitly ratified. Read this mandate and every required source before planning or editing. Your authorization is only to author/review HarnessTemplate, HarnessRun, Receipt, any essential direct relation constitutions, the canonical relation map, and the contradiction-closure record. You are not authorized to create a PRD/FR, Tech Spec, SQL, migration, RLS/Storage policy, agent orchestrator, generic state engine, API, runtime change, or data movement.

Use the accepted matrix, collision register, predecessor constitutions, and WP-06/WP-07/WP-08 evidence. Do not treat a YAML runbook or runtime Skill as proof of a general orchestrator. Do not select a primary class from file extension or schema convenience. Every constitution must account for 26 dimensions and preserve three authority axes: canonical definition source, runtime projection, and change/promotion authority.

Keep these boundaries strict: template is reusable canonical doctrine and has no tenant facts; run is a scoped operational execution and does not mutate its template; operation is the legal interface; event records occurrence; receipt is append-only controlled record, not self-authenticating evidence or outcome proof. Enforce Workspace containment through the legal parent chain and prevent global templates from referencing private data.

Run authoring and collision review separately. Execute every Section 6 hard negative; retain conflicts/deferred issues rather than repairing them silently. Record sources, hashes, validator results, limitations, and non-claims. Update control state, commit only allowed files, ask the Section 7 decision, and stop before CA-SPEC-01.
