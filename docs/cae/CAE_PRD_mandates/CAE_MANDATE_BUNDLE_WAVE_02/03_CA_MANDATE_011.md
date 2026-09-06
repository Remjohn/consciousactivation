# CAE Mandate M011 — Cryptographically Sealed Pre-Production Snapshot

**Mandate ID:** `CA-M011`  
**Wave:** `02`  
**Canonical question:** `Q11`  
**Causal stage:** `Stage 05 — Declarative PreProduction / execution boundary`  
**Governing requirement / invariant:** `FR-011 / sealed pre-production snapshot`  
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

Implement the governed boundary at which mutable preparation state becomes an immutable, execution-admissible Pre-Production Snapshot. The snapshot must bind the exact upstream revisions required for execution, use deterministic canonical serialization and an integrity digest or the repository’s equivalent integrity primitive, and prevent execution from silently refreshing any input from later mutable state. The required transition is PREPARATION_STATE → COMPILE_SNAPSHOT → SEALED_PREPROD_SNAPSHOT → EXECUTION_ADMISSION. The snapshot is the bridge between operator-editable planning and immutable runtime execution.

The implementation must make the decision true at the correct architectural boundary. Do not simulate it in presentation code, prose, or a test-only fixture. Where state changes, use the project’s governed state/command path and emit the required receipt. Where a derivative artifact is produced, retain direct lineage to its source authority. Where revisioning applies, prior revisions remain inspectable and immutable where the contract requires immutability.

## 3. Governing doctrine and authority sources

**Primary authority**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q11`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`

**Question / product authority**
- `UI.md` Sections 8–12.\n- `Architecture.md` Sections 4, 6, 7, 20 and its state/provenance model.\n- `PRD-002` / `PRD-004` pre-production material.\n- Wave 02 readiness assessment: CA-M011 / Q11.\n- CA-M009 and CA-M010 as prerequisite outputs, verified rather than assumed.

The Wave 02 readiness assessment supplied with this execution context explicitly defines CAE Wave 02 as Q09–Q16 and names this mandate as `CA-M011` / `Q11`. That planning statement is a source of intended scope; the current repository remains the source of executable truth.

If the repository differs from the cited target, classify the discrepancy as `DOCUMENT`, `EXECUTABLE`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED` evidence. Never turn a design statement into a false completion claim.

## 4. Mandatory reading before action

Before planning or editing, read the full contents where present of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q11`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- the Wave 02 readiness assessment that defines Q09–Q16
- the CAE convergence spine / decision ledger
- directly relevant PRD module(s)
- current executable code, schemas, migrations, manifests, and direct tests

Question-specific mandatory reading:
- current preparation graph/revision store;\n- current Research Brief implementation;\n- manifest/compiler pipeline;\n- runtime state and run admission;\n- digest/receipt utilities;\n- schema/migrations for snapshots or run metadata;\n- direct tests for sealing, integrity, and execution admission.

If a cited path moved, locate the current equivalent and record the mapping in the evidence record. Missing required authority is `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not permission to invent a replacement.

## 5. Exact scope

Own snapshot compilation, deterministic identity/digest, constituent revision binding, seal operation, persistence, active-run binding, and execution admission. Inventory all upstream artifacts required by the existing pre-production contract and reference their exact identities/revisions/digests. The seal must be durable and inspectable. Execution must accept an exact matching snapshot and reject stale, tampered, or mismatched inputs. Include the minimum integration needed for the active run to remember and verify the snapshot. Do not redesign the runtime globally or implement evidence capture.

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

- Do not make a UI button alone the seal authority.\n- Do not recompute a sealed snapshot from latest mutable state.\n- Do not make serialization non-deterministic.\n- Do not mutate a sealed snapshot in place.\n- Do not silently upgrade a live run to a new snapshot.\n- Do not weaken admission for legacy campaigns; classify compatibility gaps.\n- Do not implement Q12–Q16 evidence logic.

If a collision appears:
1. Stop before the conflicting change.
2. Identify the controlling authority.
3. Classify it using the project error taxonomy (`AUTHORITY_ERROR`, `SCOPE_ERROR`, `TAXONOMY_ERROR`, `SCHEMA_ERROR`, `RELATION_ERROR`, `STATE_ERROR`, `EVIDENCE_ERROR`, `PROVENANCE_ERROR`, `SEMANTIC_DRIFT`, `EDITORIAL_DRIFT`, `FORMAT_DRIFT`, `COMPOSITION_ERROR`, `RUNTIME_ERROR`, `REWARD_HACK`, or `ENVIRONMENT_FIDELITY_ERROR` as applicable).
4. Make the minimum correction only if this mandate clearly owns it.
5. Otherwise record the collision with evidence and stop.

### Contrastive failure — the good-looking but wrong result

The project requires at least one anti-centroid or false-proof case. A result can look polished, pass a shallow schema check, or score highly while violating the actual causal invariant. Such a result is a failure, not “partial success.” The mandate-specific false-proof case appears in the verification section and must be executable where possible.

## 8. Required work / implementation behavior

1. Inventory required pre-production inputs and their canonical identities. 2. Establish deterministic snapshot serialization and identity. 3. Implement compile → seal with actor, timestamp, constituent revisions, and integrity digest. 4. Persist the sealed snapshot and run binding. 5. Verify exact snapshot integrity at execution admission. 6. Add positive tests for repeatability, seal/retrieve, run binding, and successful admission. 7. Add negative tests for tampered inputs, changed upstream revisions, digest mismatch, stale snapshot, duplicate/conflicting seals, latest-state substitution, and UI-only seal. 8. Verify that a later draft creates a new candidate rather than mutating the sealed object. 9. Record snapshot identity and all evidence.

Every newly created or changed canonical object must preserve stable identity, owner/scope, authority axes, lifecycle, and direct upstream lineage. Revision or digest semantics must be retained where the contract requires them. Relations must expose their endpoints and direction/cardinality where relevant. Receipts must contain enough information for another agent to reconstruct what changed and why.

Positive tests establish the intended path. Negative tests establish the fail-closed boundary and are mandatory for stale, forged, missing, contradictory, or unanchored inputs applicable to the mandate.

## 9. Verification and evidence standard

Because this mandate contains an integrity claim, tests must inspect actual serialized bytes or the repository’s canonical serialization primitive. Two equivalent logical snapshots must serialize deterministically; a material mutation must change the integrity result or cause admission failure. What is measured: deterministic binding, immutability, run association, and fail-closed admission. What is not measured: semantic quality of research or graph inputs. False-proof case: the system reports a seal but silently rehydrates latest mutable data during execution. That must fail. Environment fidelity requires real persistence and admission paths.

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

This is the integration owner for Wave 02’s mutable-to-immutable boundary. Stop after snapshot sealing, exact run binding, integrity checking, and fail-closed admission are proven. Do not implement source media or later evidence stages. Request the explicit CA-M011 gate.

## 11. Rollback / recovery

Incorrect snapshots are invalidated/superseded and replaced with new snapshots from corrected upstream revisions. Historical snapshot identities and run bindings remain inspectable. Do not edit a snapshot in place or silently repair an already-started run. Migrations must preserve historical identity and receipts.

Documentation and canonical artifacts are versioned and superseded rather than silently rewritten. Runtime changes retain receipts. External side effects must not be called transactional unless the implementation proves it.

## 12. Operator decision

**Operator decision required:** Approve CA-M011 and authorize the evidence chain beginning with CA-M012; record any legacy compatibility decision that affects snapshot admissibility.

Until this decision is recorded in CAE control state, the next dependent mandate is unauthorized.

## 13. 200–300 word activation prompt

```text
Execute `CA-M011` only. Read the Mandate Authoring Protocol, Gemini execution skill, Master Canon Q11, `UI.md`, `Architecture.md`, Wave 02 readiness assessment, relevant pre-production PRD material, and the current graph/revision, Research Brief, runtime state, manifest/compiler, digest, receipt, and run-admission surfaces. Implement the authoritative transition from mutable preparation to an immutable, cryptographically identifiable Pre-Production Snapshot. Bind exact upstream revisions and prevent execution from silently using later state. Prove deterministic serialization, snapshot identity, persistence, run binding, and admission. Then mutate an upstream constituent or attempt a stale/forged snapshot and show execution fails closed. The false-proof case is a system that reports a seal but silently rehydrates latest preparation data at execution time; that must fail. Do not implement Q12–Q16. Record actor, snapshot identity, constituent revisions/digests, commands, environment, limitations, control-state update, and exact commit SHA. Request the CA-M011 operator decision and stop. Preserve the distinction between fact, hypothesis, and operator decision. Do not convert a green test into proof of a wider property. If a required dependency is unavailable or a higher-order invariant conflicts with the proposed change, record the collision, classify it, update control state, request the appropriate operator decision, and stop rather than inventing a substitute. Never claim completion from documentation alone; every completion claim must point to executable evidence and its limitations.
```
