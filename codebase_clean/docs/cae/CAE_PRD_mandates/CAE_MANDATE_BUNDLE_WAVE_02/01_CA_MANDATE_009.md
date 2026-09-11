# CAE Mandate M009 — Interactive Parameter-Sensitive Preparation Graph

**Mandate ID:** `CA-M009`  
**Wave:** `02`  
**Canonical question:** `Q09`  
**Causal stage:** `Stage 05 — Declarative PreProduction`  
**Governing requirement / invariant:** `FR-009 / preparation-graph contract`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate is one member of CAE Wave 02 and covers exactly one bounded implementation decision. It is subordinate to the CAE Mandate Authoring Protocol and to the ratified Master 57-Question Decision & Convergence Canon. It inherits the architecture, UI, product, runtime, evidence, provenance, and governance laws already established by the CAE program.

The executor is an implementation agent, not the system architect. The mandate is an execution contract, not a design invitation. The executor MUST inspect repository reality before editing, distinguish documented claims from executable evidence, reuse compatible existing objects and services, preserve exact lineage where relevant, and stop on authority or scope collisions rather than widening the work.

Authority is intentionally separated:
- **Source of meaning:** the Master Canon and the cited product/architecture contracts.
- **Runtime authority:** the canonical CAE runtime and its typed state/command paths.
- **Change/promotion authority:** the Operator and repository governance.

A document, YAML registry, database row, browser state, model response, generated artifact, or test fixture does not become authoritative merely because it exists.

## 2. Decision / objective being authorized

Implement the preparation graph as a first-class, operator-controlled, revisioned planning artifact. Before execution, an Operator may change parameters and create a new graph revision. Once a run begins, the active execution must remain bound to the exact graph revision captured for that run. The runtime, not browser-local state, is authoritative. The required lifecycle is DRAFT_GRAPH → SAVE_REVISION → CANDIDATE_GRAPH_REVISION → SEAL / EXECUTION BINDING → ACTIVE_EXECUTION_GRAPH. The mandate must prove revision isolation, stale-write rejection, explicit lineage, and runtime-authoritative read/write behavior. It is not sufficient for the graph to visually respond to changes; the stored object and run binding must change safely. Historical revisions must remain inspectable, and a later draft must never rewrite the meaning of an already-running execution.

The implementation must make the decision true at the correct architectural boundary. Do not simulate it in presentation code, prose, or a test-only fixture. Where state changes, use the project’s governed state/command path and emit the required receipt. Where a derivative artifact is produced, retain direct lineage to its source authority. Where revisioning applies, prior revisions remain inspectable and immutable where the contract requires immutability.

## 3. Governing doctrine and authority sources

**Primary authority**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q09`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`

**Question / product authority**
- `UI.md` Sections 3, 5, 8, 9, and 16.\n- `Architecture.md` Sections 4, 6, 7, 20, and the preparation/pre-production model.\n- `PRD-004` preparation-graph and pre-production material.\n- Wave 02 readiness assessment: CA-M009 / Q09.\n- Existing campaign, Control Tower, Run Graph, Timeline, Exception Queue, and Revision Composer surfaces.

The Wave 02 readiness assessment supplied with this execution context explicitly defines CAE Wave 02 as Q09–Q16 and names this mandate as `CA-M009` / `Q09`. That planning statement is a source of intended scope; the current repository remains the source of executable truth.

If the repository differs from the cited target, classify the discrepancy as `DOCUMENT`, `EXECUTABLE`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED` evidence. Never turn a design statement into a false completion claim.

## 4. Mandatory reading before action

Before planning or editing, read the full contents where present of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q09`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- the Wave 02 readiness assessment that defines Q09–Q16
- the CAE convergence spine / decision ledger
- directly relevant PRD module(s)
- current executable code, schemas, migrations, manifests, and direct tests

Question-specific mandatory reading:
- current preparation-graph implementation and types;\n- campaign creation/read/update APIs;\n- run state and active execution binding;\n- revision/concurrency utilities;\n- schema/migrations for preparation state;\n- direct UI and API tests around graph editing and stale state;\n- any existing digest/version receipt helpers.

If a cited path moved, locate the current equivalent and record the mapping in the evidence record. Missing required authority is `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not permission to invent a replacement.

## 5. Exact scope

Own only the preparation graph object, revision semantics, execution binding, and the minimum operator projection needed to inspect those states. Determine the current canonical graph representation before inventing anything. Make parameters explicit enough that a meaningful change has a deterministic serialization and a new revision identity. Ensure an active run stores the exact revision identity and, where the existing contract supports it, an integrity digest. The UI may expose editing, but all writes must pass through the canonical API/runtime path. The mandate ends when draft editing, revision preservation, execution binding, historical inspection, and stale mutation rejection are proven.

The executor owns only the smallest set of changes needed to make the decision executable and provable. Inputs, outputs, actors, validators, and authority boundaries must be explicit. For every stateful change use:

```text
source state
    → governed operation
    → target state
```

and document actor, preconditions, validators, postconditions, receipt, error route, and recovery.

Dependencies may be inspected and consumed. A prerequisite may be minimally repaired only when it is inseparable from this mandate and doing so does not change another mandate’s authority. Otherwise stop and classify the dependency.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the current implementation, schema, migration, manifest, API, UI projection, and direct tests corresponding to this mandate, plus the smallest supporting artifact needed to persist identity, revision, lineage, validation, or receipt.

Candidate physical surfaces must be discovered and confirmed from current repository reality before editing. Likely relevant families include `packages/ca_runtime`, `services/pipeline`, `programs/*_program`, `cae_collision_intelligence`, the current web/API surface, and their direct tests, but the executor must use the current equivalent rather than assume historical paths.

The executor must not modify unrelated canonical questions, global authority registries not required here, release/distribution semantics, production-authorization claims, broad UI redesign, dependency upgrades, or tests whose only purpose is to make the mandate appear green.

## 7. Prohibitions and collision procedure

- Do not perform a general UI redesign.\n- Do not let React/client state serve as proof of graph authority.\n- Do not mutate the revision an active run already uses.\n- Do not silently overwrite a newer revision from a stale editor.\n- Do not collapse draft, candidate, sealed snapshot, and active binding into one mutable record.\n- Do not implement CA-M011 snapshot sealing, except the minimum binding contract needed for a future seal.\n- Do not change unrelated campaign lifecycle semantics.

If a collision appears:
1. Stop before the conflicting change.
2. Identify the controlling authority.
3. Classify it using the project error taxonomy (`AUTHORITY_ERROR`, `SCOPE_ERROR`, `TAXONOMY_ERROR`, `SCHEMA_ERROR`, `RELATION_ERROR`, `STATE_ERROR`, `EVIDENCE_ERROR`, `PROVENANCE_ERROR`, `SEMANTIC_DRIFT`, `EDITORIAL_DRIFT`, `FORMAT_DRIFT`, `COMPOSITION_ERROR`, `RUNTIME_ERROR`, `REWARD_HACK`, or `ENVIRONMENT_FIDELITY_ERROR` as applicable).
4. Make the minimum correction only if this mandate clearly owns it.
5. Otherwise record the collision with evidence and stop.

### Contrastive failure — the good-looking but wrong result

The project requires at least one anti-centroid or false-proof case. A result can look polished, pass a shallow schema check, or score highly while violating the actual causal invariant. Such a result is a failure, not “partial success.” The mandate-specific false-proof case appears in the verification section and must be executable where possible.

## 8. Required work / implementation behavior

1. Inventory the current graph data model, API, UI, run binding, and revision/concurrency behavior. 2. Establish or reuse the smallest revisioned graph representation. 3. Implement draft-to-revision persistence and immutable historical reads. 4. Bind an active run to a specific graph revision. 5. Reject stale/conflicting writes through the existing canonical version/CAS mechanism where available. 6. Expose revision identity and active binding to the operator. 7. Add positive tests for revision creation, retrieval, run binding, later revision creation, and historical preservation. 8. Add negative tests for stale write, active-revision mutation, forged revision identifier, backend/browser divergence, and digest mismatch if applicable. 9. Record all evidence and limitations.

Every newly created or changed canonical object must preserve stable identity, owner/scope, authority axes, lifecycle, and direct upstream lineage. Revision or digest semantics must be retained where the contract requires them. Relations must expose their endpoints and direction/cardinality where relevant. Receipts must contain enough information for another agent to reconstruct what changed and why.

Positive tests establish the intended path. Negative tests establish the fail-closed boundary and are mandatory for stale, forged, missing, contradictory, or unanchored inputs applicable to the mandate.

## 9. Verification and evidence standard

The primary proof must be behavioral and runtime-backed. After a run binds to R1, a later operator edit must create R2 without changing R1 or the run’s binding. A separate test must attempt to mutate R1 in place and demonstrate rejection. A fresh read from authoritative storage must still return R1 for the active run even if the UI currently displays R2. What is measured: revision identity, immutability, binding, concurrency safety, and authoritative reads. What is not measured: visual quality or semantic correctness of the preparation content. False-proof case: the UI changes from R1 to R2 while the backend mutates the same stored row, so the active run now unknowingly uses R2. That must fail. Environment fidelity requires the real persistence and API boundary, not a mock-only simulation.

For every substantive automated test, record:
- command;
- environment identity;
- fixture/data/source identity;
- observed result;
- exact property proved;
- limitation.

A green test proves only what it actually measures. For evaluators, record the evaluator/version, whether it is descriptive or gating, and what it does not establish. For human judgments, record the operator/reviewer and the decision required.

Where cryptographic, revision, provenance, or byte-identity claims are made, verify the actual underlying representation rather than the presence of a metadata field.

## 10. Completion and stop condition

The mandate is complete only when:
1. the scoped artifact or executable behavior exists;
2. positive and negative validation passes;
3. evidence and limitations are recorded;
4. CAE control state is updated;
5. the exact git commit SHA is captured;
6. relevant identities, revisions, digests, and receipts are recorded where applicable;
7. the operator gate is explicitly requested.

Do not progress into CA-M011 or later evidence work. Stop after the graph revision lifecycle, authoritative binding, and positive/negative tests are evidenced. Request the CA-M009 operator decision and leave the next mandate unauthorized until that decision is recorded.

## 11. Rollback / recovery

Bad graph revisions are rejected or superseded; historical revisions remain inspectable. If a run is found to have an incorrect binding, do not silently edit its historical record. Use the governed repair/restart path and preserve the original receipt. Any migration must preserve existing revision identity and be reversible or forward-compatible.

Documentation and canonical artifacts are versioned and superseded rather than silently rewritten. Runtime changes retain receipts. External side effects must not be called transactional unless the implementation proves it.

## 12. Operator decision

**Operator decision required:** Approve CA-M009 and authorize CA-M010; record whether the preparation-graph revision/binding contract is accepted as an input to CA-M011.

Until this decision is recorded in CAE control state, the next dependent mandate is unauthorized.

## 13. 200–300 word activation prompt

```text
Execute `CA-M009` only. Read the CAE Mandate Authoring Protocol, Gemini execution skill, Master Canon Q09, `UI.md`, `Architecture.md`, the Wave 02 readiness assessment, PRD-004 preparation-graph material, and the current graph, campaign, run-binding, API, schema, and tests before editing. Implement the preparation graph as a runtime-authoritative, revisioned planning artifact. Operator edits before execution must create a new identifiable revision; an active run must retain the exact graph revision and must never be changed by later UI edits. Reuse existing revision and concurrency mechanisms. Do not redesign the UI and do not begin CA-M010 or CA-M011. Prove revision creation, historical retrieval, run binding, and later revision creation. Reject stale writes, in-place mutation of an active revision, forged identifiers, and UI-only changes that do not reach runtime authority. The false-proof case is a graph that visually changes while the backend mutates the revision an active run already uses; that is invalid. Record commands, environment, fixture identity, revisions/digests, limitations, control-state update, and exact commit SHA. Request the CA-M009 operator decision and stop. Preserve the distinction between fact, hypothesis, and operator decision. Do not convert a green test into proof of a wider property. If a required dependency is unavailable or a higher-order invariant conflicts with the proposed change, record the collision, classify it, update control state, request the appropriate operator decision, and stop rather than inventing a substitute. Never claim completion from documentation alone; every completion claim must point to executable evidence and its limitations.
```
