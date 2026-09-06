# CAE Mandate M013 — Temporal Evidence Anchoring

**Mandate ID:** `CA-M013`  
**Wave:** `02`  
**Canonical question:** `Q13`  
**Causal stage:** `Stage 07 — Evidence Capture`  
**Governing requirement / invariant:** `FR-013 / temporal anchoring`  
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

Make evidence moments physically locatable inside sovereign source media. A semantic statement or quote is not admissible merely because it exists in a transcript; the evidence object must carry a precise temporal anchor that resolves to authoritative media. The conceptual form is EvidenceMoment(source_media_digest, stream, start_offset, end_offset, timebase, transcript_span, provenance). Use the repository’s existing timing, stream, and precision contract rather than inventing a competing coordinate system.

The implementation must make the decision true at the correct architectural boundary. Do not simulate it in presentation code, prose, or a test-only fixture. Where state changes, use the project’s governed state/command path and emit the required receipt. Where a derivative artifact is produced, retain direct lineage to its source authority. Where revisioning applies, prior revisions remain inspectable and immutable where the contract requires immutability.

## 3. Governing doctrine and authority sources

**Primary authority**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q13`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`

**Question / product authority**
- `Architecture.md` Section 14.\n- `UI.md` Section 13.\n- `PRD-003` evidence capture/temporal anchoring material.\n- Wave 02 readiness assessment: CA-M013 / Q13.\n- Existing `cmf_pipeline` evidence segment models, timebase utilities, and media identity logic.

The Wave 02 readiness assessment supplied with this execution context explicitly defines CAE Wave 02 as Q09–Q16 and names this mandate as `CA-M013` / `Q13`. That planning statement is a source of intended scope; the current repository remains the source of executable truth.

If the repository differs from the cited target, classify the discrepancy as `DOCUMENT`, `EXECUTABLE`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED` evidence. Never turn a design statement into a false completion claim.

## 4. Mandatory reading before action

Before planning or editing, read the full contents where present of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q13`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- the Wave 02 readiness assessment that defines Q09–Q16
- the CAE convergence spine / decision ledger
- directly relevant PRD module(s)
- current executable code, schemas, migrations, manifests, and direct tests

Question-specific mandatory reading:
- current transcript segment/evidence models;\n- media stream and timebase utilities;\n- source-resolution code;\n- evidence validation and storage;\n- operator evidence inspection;\n- direct tests for temporal ranges and source lookup.

If a cited path moved, locate the current equivalent and record the mapping in the evidence record. Missing required authority is `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not permission to invent a replacement.

## 5. Exact scope

Own the temporal coordinate contract for evidence moments. Bind every evidence object to sovereign source digest, stream, timebase, start/end coordinate, and existing transcript/character span where available. Implement source-resolution and interval validation. Where multiple streams/timebases exist, make them explicit. The mandate ends at temporal anchoring; continuity and verbatim behavior remain separate.

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

- Do not accept floating quotes without source coordinates.\n- Do not treat model-generated timestamps as authority merely because they look plausible.\n- Do not round away required precision.\n- Do not replace temporal anchoring with transcript character offsets where time is required.\n- Do not silently shift bad timestamps to make a test pass.\n- Do not implement chunk continuity or verbatim normalization here.

If a collision appears:
1. Stop before the conflicting change.
2. Identify the controlling authority.
3. Classify it using the project error taxonomy (`AUTHORITY_ERROR`, `SCOPE_ERROR`, `TAXONOMY_ERROR`, `SCHEMA_ERROR`, `RELATION_ERROR`, `STATE_ERROR`, `EVIDENCE_ERROR`, `PROVENANCE_ERROR`, `SEMANTIC_DRIFT`, `EDITORIAL_DRIFT`, `FORMAT_DRIFT`, `COMPOSITION_ERROR`, `RUNTIME_ERROR`, `REWARD_HACK`, or `ENVIRONMENT_FIDELITY_ERROR` as applicable).
4. Make the minimum correction only if this mandate clearly owns it.
5. Otherwise record the collision with evidence and stop.

### Contrastive failure — the good-looking but wrong result

The project requires at least one anti-centroid or false-proof case. A result can look polished, pass a shallow schema check, or score highly while violating the actual causal invariant. Such a result is a failure, not “partial success.” The mandate-specific false-proof case appears in the verification section and must be executable where possible.

## 8. Required work / implementation behavior

1. Inspect current timing contract. 2. Define/reuse canonical EvidenceMoment fields. 3. Bind source digest, stream, timebase, start, end, and transcript span. 4. Validate non-negative, ordered, in-bounds intervals and required precision. 5. Expose source-resolvable evidence in the operator surface. 6. Add positive exact-boundary and multi-stream tests where supported. 7. Add negative tests for missing source, missing coordinates, negative/reversed intervals, invalid timebase, source mismatch, and out-of-bounds anchor. 8. Verify a fresh source read resolves the evidence moment. 9. Record the timebase/precision contract and limitations.

Every newly created or changed canonical object must preserve stable identity, owner/scope, authority axes, lifecycle, and direct upstream lineage. Revision or digest semantics must be retained where the contract requires them. Relations must expose their endpoints and direction/cardinality where relevant. Receipts must contain enough information for another agent to reconstruct what changed and why.

Positive tests establish the intended path. Negative tests establish the fail-closed boundary and are mandatory for stale, forged, missing, contradictory, or unanchored inputs applicable to the mandate.

## 9. Verification and evidence standard

A timestamp field is not proof unless the runtime can resolve it to source media. What is measured: source-resolvable temporal identity, interval validity, and provenance. What is not measured: semantic correctness, chunk continuity, speaker accuracy, or editorial usefulness. False-proof case: a highly convincing quote with no source-resolvable media interval. It must fail. Use deterministic fixtures with known media boundaries and exercise the real evidence path where possible.

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

Stop after canonical temporal anchoring and fail-closed validation are proven. Do not implement Q14 continuity, Q15 verbatim governance, or Q16 Collision formation.

## 11. Rollback / recovery

Invalid anchors are rejected or represented as inadmissible; they are not silently shifted. A corrected evidence object is a new revision. Preserve invalid historical records needed for audit and route any underlying timebase bug outside this mandate’s scope.

Documentation and canonical artifacts are versioned and superseded rather than silently rewritten. Runtime changes retain receipts. External side effects must not be called transactional unless the implementation proves it.

## 12. Operator decision

**Operator decision required:** Approve CA-M013 and authorize CA-M014; confirm the temporal-anchor contract is accepted as the evidence coordinate root.

Until this decision is recorded in CAE control state, the next dependent mandate is unauthorized.

## 13. 200–300 word activation prompt

```text
Execute `CA-M013` only. Read the Mandate Authoring Protocol, Gemini execution skill, Master Canon Q13, `Architecture.md` Section 14, `UI.md` Section 13, Wave 02 readiness assessment, PRD-003 temporal/evidence material, and the current transcript/evidence/media timebase surfaces. Implement canonical temporal anchoring so each evidence object resolves to sovereign media through exact source digest, stream, timebase, start, and end coordinates, using the repository’s existing timing contract. Prove valid intervals, source resolution, multi-stream handling where supported, and required precision. Reject missing coordinates, negative/reversed intervals, invalid timebases, source-digest mismatch, and out-of-range anchors. The false-proof case is a semantically persuasive quote without a source-resolvable anchor; it must fail. Do not implement continuity, verbatim rewriting, or Collision logic. Record commands, environment, fixture/source identity, coordinate contract, limitations, control state, and exact commit SHA. Request the CA-M013 operator decision and stop. Preserve the distinction between fact, hypothesis, and operator decision. Do not convert a green test into proof of a wider property. If a required dependency is unavailable or a higher-order invariant conflicts with the proposed change, record the collision, classify it, update control state, request the appropriate operator decision, and stop rather than inventing a substitute. Never claim completion from documentation alone; every completion claim must point to executable evidence and its limitations.
```
