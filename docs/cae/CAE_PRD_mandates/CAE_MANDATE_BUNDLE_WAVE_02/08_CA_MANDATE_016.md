# CAE Mandate M016 — Grounded Collision Tension Matrix

**Mandate ID:** `CA-M016`  
**Wave:** `02`  
**Canonical question:** `Q16`  
**Causal stage:** `Stage 08 — Collision Analysis`  
**Governing requirement / invariant:** `FR-016 / grounded Collision tension matrix`  
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

Implement the Collision as a grounded multi-pole semantic relation, not as an attractive model-generated sentence or a single confidence score. A valid Collision must connect Guest/Subject DNA, Audience Tension, and World Signal through explicit supporting evidence and a defined tension/paradox/latent-truth relationship. It must retain grounding, source evidence, tension vectors, falsification conditions, receipt, revision, and downstream dependencies. Admission must fail closed when required poles or evidence are missing, provenance is stale, the relation is unsupported, or a falsification condition cannot be stated.

The implementation must make the decision true at the correct architectural boundary. Do not simulate it in presentation code, prose, or a test-only fixture. Where state changes, use the project’s governed state/command path and emit the required receipt. Where a derivative artifact is produced, retain direct lineage to its source authority. Where revisioning applies, prior revisions remain inspectable and immutable where the contract requires immutability.

## 3. Governing doctrine and authority sources

**Primary authority**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q16`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`

**Question / product authority**
- `Architecture.md` Sections 4, 15, and 16.\n- `UI.md` Section 14.\n- `PRD-003` collision-analysis material.\n- Wave 02 readiness assessment: CA-M016 / Q16.\n- Existing `cae_collision_intelligence/verifier.py`, collision/hypothesis stores, evidence reads, audience-tension and Subject/Activative lineage, manifests, and tests.

The Wave 02 readiness assessment supplied with this execution context explicitly defines CAE Wave 02 as Q09–Q16 and names this mandate as `CA-M016` / `Q16`. That planning statement is a source of intended scope; the current repository remains the source of executable truth.

If the repository differs from the cited target, classify the discrepancy as `DOCUMENT`, `EXECUTABLE`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED` evidence. Never turn a design statement into a false completion claim.

## 4. Mandatory reading before action

Before planning or editing, read the full contents where present of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q16`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- the Wave 02 readiness assessment that defines Q09–Q16
- the CAE convergence spine / decision ledger
- directly relevant PRD module(s)
- current executable code, schemas, migrations, manifests, and direct tests

Question-specific mandatory reading:
- current collision/hypothesis schema and store;\n- collision verifier/admission;\n- audience tension representation;\n- Subject DNA/Activative lineage;\n- World Signal/research lineage;\n- admitted evidence representation from CA-M012–CA-M015;\n- operator review/projection and direct tests.

If a cited path moved, locate the current equivalent and record the mapping in the evidence record. Missing required authority is `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not permission to invent a replacement.

## 5. Exact scope

Own the grounded Collision representation and its admission predicate. Reuse existing stable identifiers, revision, receipt, evidence, tension-vector, and operator-gate primitives. The minimum object must identify each required pole, exact upstream revisions, supporting admitted evidence, relation/tension semantics, falsification condition, and lifecycle/admission state. A model may propose a candidate, but only canonical runtime validation can make it authoritative. The scope ends at grounded Collision admission; candidate clustering, expression moments, yield, composition, and later runtime work are out of scope.

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

- Do not admit a Collision from one evidence pole.\n- Do not treat eloquence, novelty, or score as proof.\n- Do not invent missing Audience, Guest, World, or source evidence.\n- Do not let a model response self-authorize a Collision.\n- Do not make UI or cached ranking authoritative.\n- Do not hide missing falsification conditions behind generic confidence.\n- Do not implement Q17–Q23.

If a collision appears:
1. Stop before the conflicting change.
2. Identify the controlling authority.
3. Classify it using the project error taxonomy (`AUTHORITY_ERROR`, `SCOPE_ERROR`, `TAXONOMY_ERROR`, `SCHEMA_ERROR`, `RELATION_ERROR`, `STATE_ERROR`, `EVIDENCE_ERROR`, `PROVENANCE_ERROR`, `SEMANTIC_DRIFT`, `EDITORIAL_DRIFT`, `FORMAT_DRIFT`, `COMPOSITION_ERROR`, `RUNTIME_ERROR`, `REWARD_HACK`, or `ENVIRONMENT_FIDELITY_ERROR` as applicable).
4. Make the minimum correction only if this mandate clearly owns it.
5. Otherwise record the collision with evidence and stop.

### Contrastive failure — the good-looking but wrong result

The project requires at least one anti-centroid or false-proof case. A result can look polished, pass a shallow schema check, or score highly while violating the actual causal invariant. Such a result is a failure, not “partial success.” The mandate-specific false-proof case appears in the verification section and must be executable where possible.

## 8. Required work / implementation behavior

1. Inventory collision representations and admission logic. 2. Reuse/define canonical grounded Collision structure. 3. Bind Guest/Subject, Audience Tension, and World Signal to exact upstream identities/revisions. 4. Bind supporting evidence to admitted evidence with provenance. 5. Add explicit tension/paradox relation and falsification condition. 6. Implement multi-dimensional admission checks without collapsing them to one score. 7. Add positive tests for fully grounded Collision. 8. Add negative tests for single-pole, unsupported relation, missing/stale evidence, missing falsification, forged lineage, and score-only admission. 9. Provide operator inspection showing grounding, tension, evidence, falsification, and downstream implications. 10. Record exact Collision identity/revision/receipt and limitations.

Every newly created or changed canonical object must preserve stable identity, owner/scope, authority axes, lifecycle, and direct upstream lineage. Revision or digest semantics must be retained where the contract requires them. Relations must expose their endpoints and direction/cardinality where relevant. Receipts must contain enough information for another agent to reconstruct what changed and why.

Positive tests establish the intended path. Negative tests establish the fail-closed boundary and are mandatory for stale, forged, missing, contradictory, or unanchored inputs applicable to the mandate.

## 9. Verification and evidence standard

The main proof is that a Collision cannot become admissible unless the required poles and evidence lineage pass. What is measured: structural grounding, evidence lineage, revision integrity, falsification-condition presence, and runtime admission. What is not measured: whether an admitted Collision is aesthetically brilliant or commercially successful. False-proof case one: a compelling emotional statement supported by only one pole; it must fail. False-proof case two: three labeled poles with no actual evidence or falsification condition; it must also fail. A score threshold is not evidence. Environment fidelity requires real stores/runtime admission or a documented limitation.

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

Wave 02 closes at this boundary. Stop after CA-M016 is evidenced and operator-gated. Do not start Q17–Q23, candidate formation, expression moments, yield, composition, or runtime infrastructure without a new mandate.

## 11. Rollback / recovery

Invalid Collisions are rejected or superseded; prior revisions remain inspectable. If upstream evidence is revoked or a pole changes, create a new Collision revision. Do not repair by editing historical lineage. If an earlier evidence contract is missing, block the Collision and route the dependency rather than weakening admission.

Documentation and canonical artifacts are versioned and superseded rather than silently rewritten. Runtime changes retain receipts. External side effects must not be called transactional unless the implementation proves it.

## 12. Operator decision

**Operator decision required:** Approve CA-M016 and record Wave 02 closure; authorize handoff to Wave 03 (Q17–Q23) only after reviewing the evidence chain and limitations.

Until this decision is recorded in CAE control state, the next dependent mandate is unauthorized.

## 13. 200–300 word activation prompt

```text
Execute `CA-M016` only. Read the Mandate Authoring Protocol, Gemini execution skill, Master Canon Q16, `Architecture.md` Sections 15–16, `UI.md` Section 14, Wave 02 readiness assessment, PRD-003 collision/evidence material, and the current collision verifier/store, Audience Tension, Subject/Activative lineage, World Signal/research, evidence, runtime admission, and tests. Implement Collision as a grounded multi-pole relation connecting Guest/Subject DNA, Audience Tension, and World Signal with exact upstream revisions and admitted evidence. Require an explicit tension/paradox relation and falsification condition. Reject single-pole, unsupported, stale, forged, and score-only Collisions. The signature false-proof cases are a beautiful statement with only one evidentiary pole and a three-pole object with no real evidence or falsification condition; both must fail. Do not implement Q17–Q23. Record exact Collision identity/revision/receipt, commands, environment, fixture lineage, actual properties proved, limitations, control state, and exact commit SHA. Request the CA-M016 operator decision and Wave 02 closure decision, then stop. Preserve the distinction between fact, hypothesis, and operator decision. Do not convert a green test into proof of a wider property. If a required dependency is unavailable or a higher-order invariant conflicts with the proposed change, record the collision, classify it, update control state, request the appropriate operator decision, and stop rather than inventing a substitute. Never claim completion from documentation alone; every completion claim must point to executable evidence and its limitations.
```
