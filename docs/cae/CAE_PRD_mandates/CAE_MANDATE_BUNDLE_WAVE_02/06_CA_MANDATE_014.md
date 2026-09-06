# CAE Mandate M014 — Cross-Window Continuity and Chunking Protection

**Mandate ID:** `CA-M014`  
**Wave:** `02`  
**Canonical question:** `Q14`  
**Causal stage:** `Stage 07 — Evidence Capture`  
**Governing requirement / invariant:** `FR-014 / cross-window continuity`  
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

Protect evidence meaning across chunk, window, and segment boundaries. Transcript/evidence processing must preserve semantic continuity when a sentence, answer, speaker turn, or causal statement spans adjacent processing windows. Window identity, ordering, overlap, deduplication, boundary reconstruction, and downstream evidence lineage must be explicit enough that later evidence cannot accidentally represent an isolated fragment as complete context.

The implementation must make the decision true at the correct architectural boundary. Do not simulate it in presentation code, prose, or a test-only fixture. Where state changes, use the project’s governed state/command path and emit the required receipt. Where a derivative artifact is produced, retain direct lineage to its source authority. Where revisioning applies, prior revisions remain inspectable and immutable where the contract requires immutability.

## 3. Governing doctrine and authority sources

**Primary authority**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q14`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`

**Question / product authority**
- `Architecture.md` Section 14.\n- `UI.md` Section 13.\n- `PRD-003` evidence segmentation/capture material.\n- Wave 02 readiness assessment: CA-M014 / Q14.\n- Existing chunking/window/evidence ingestion and timing surfaces.

The Wave 02 readiness assessment supplied with this execution context explicitly defines CAE Wave 02 as Q09–Q16 and names this mandate as `CA-M014` / `Q14`. That planning statement is a source of intended scope; the current repository remains the source of executable truth.

If the repository differs from the cited target, classify the discrepancy as `DOCUMENT`, `EXECUTABLE`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED` evidence. Never turn a design statement into a false completion claim.

## 4. Mandatory reading before action

Before planning or editing, read the full contents where present of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q14`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- the Wave 02 readiness assessment that defines Q09–Q16
- the CAE convergence spine / decision ledger
- directly relevant PRD module(s)
- current executable code, schemas, migrations, manifests, and direct tests

Question-specific mandatory reading:
- current chunk/window segmentation code;\n- overlap and ordering logic;\n- transcript segment identity;\n- deduplication/reconciliation logic;\n- evidence lineage and source-time binding;\n- direct ingestion tests.

If a cited path moved, locate the current equivalent and record the mapping in the evidence record. Missing required authority is `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not permission to invent a replacement.

## 5. Exact scope

Own the cross-window continuity contract at ingestion/evidence segmentation. Reuse existing identifiers, sequence, overlap, and timing semantics. Implement explicit continuity metadata and boundary validation. Prevent duplicate overlap from becoming contradictory evidence and prevent boundary fragments from being promoted as complete context when the contract requires adjacency/reconstitution evidence. The mandate may add a continuity relation or deterministic boundary-safe reconstruction. It must never invent missing text.

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

- Do not “smooth” boundaries by hallucinating words.\n- Do not treat isolated chunks as independent semantic authority.\n- Do not deduplicate solely by text similarity when stronger source/time identity exists.\n- Do not alter source bytes.\n- Do not convert this into transcript-style cleanup or speaker-diarization redesign.\n- Do not implement verbatim quote policy or Collision logic.

If a collision appears:
1. Stop before the conflicting change.
2. Identify the controlling authority.
3. Classify it using the project error taxonomy (`AUTHORITY_ERROR`, `SCOPE_ERROR`, `TAXONOMY_ERROR`, `SCHEMA_ERROR`, `RELATION_ERROR`, `STATE_ERROR`, `EVIDENCE_ERROR`, `PROVENANCE_ERROR`, `SEMANTIC_DRIFT`, `EDITORIAL_DRIFT`, `FORMAT_DRIFT`, `COMPOSITION_ERROR`, `RUNTIME_ERROR`, `REWARD_HACK`, or `ENVIRONMENT_FIDELITY_ERROR` as applicable).
4. Make the minimum correction only if this mandate clearly owns it.
5. Otherwise record the collision with evidence and stop.

### Contrastive failure — the good-looking but wrong result

The project requires at least one anti-centroid or false-proof case. A result can look polished, pass a shallow schema check, or score highly while violating the actual causal invariant. Such a result is a failure, not “partial success.” The mandate-specific false-proof case appears in the verification section and must be executable where possible.

## 8. Required work / implementation behavior

1. Inventory segmentation/window behavior. 2. Establish explicit window identity and predecessor/successor/overlap semantics. 3. Implement boundary handling using source coordinates and existing transcript data. 4. Prevent conflicting duplicate overlap from creating contradictory evidence. 5. Preserve lineage to all contributing windows and source media. 6. Create adversarial fixtures where a semantic turn crosses a boundary. 7. Add positive tests for continuity and overlap reconciliation. 8. Add negative tests for dropped boundary fragments, reordered windows, conflicting overlap, missing continuity relation, and unsupported fabricated reconstruction. 9. Record verifier limitations.

Every newly created or changed canonical object must preserve stable identity, owner/scope, authority axes, lifecycle, and direct upstream lineage. Revision or digest semantics must be retained where the contract requires them. Relations must expose their endpoints and direction/cardinality where relevant. Receipts must contain enough information for another agent to reconstruct what changed and why.

Positive tests establish the intended path. Negative tests establish the fail-closed boundary and are mandatory for stale, forged, missing, contradictory, or unanchored inputs applicable to the mandate.

## 9. Verification and evidence standard

Use deterministic fixtures to prove boundary integrity and lineage. What is measured: window order, overlap identity, boundary preservation, deduplication, and lineage. What is not measured: global transcript truth, aesthetic quality, or semantic brilliance. False-proof case: a fluent model-generated sentence hides that one half of the source statement was dropped and adds unsupported words; the system must reject it as evidence. Environment fidelity requires the real ingestion path or an explicit limitation.

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

Stop before Q15. The handoff must provide continuity metadata and a boundary-safe evidence representation that CA-M015 can treat as input without inventing missing words.

## 11. Rollback / recovery

Incorrect segmentation or continuity rules are versioned and preserve historical evidence identities. Do not rewrite historical evidence silently. If continuity cannot be proven, mark the affected evidence blocked and record the dependency rather than fabricating context.

Documentation and canonical artifacts are versioned and superseded rather than silently rewritten. Runtime changes retain receipts. External side effects must not be called transactional unless the implementation proves it.

## 12. Operator decision

**Operator decision required:** Approve CA-M014 and authorize CA-M015; confirm the continuity representation is acceptable as a prerequisite for verbatim evidence.

Until this decision is recorded in CAE control state, the next dependent mandate is unauthorized.

## 13. 200–300 word activation prompt

```text
Execute `CA-M014` only. Read the Mandate Authoring Protocol, Gemini execution skill, Master Canon Q14, `Architecture.md` Section 14, `UI.md` Section 13, Wave 02 readiness assessment, PRD-003 segmentation material, and the current chunking/window/evidence-ingestion code and tests. Protect continuity across processing windows using explicit identity, order, overlap, boundary, and lineage information. Create an adversarial fixture where a causal or semantic turn splits exactly at a boundary and prove the evidence retains the required relationship. Reject reordered windows, conflicting overlap, missing continuity links, dropped fragments, and any smooth reconstruction that introduces words unsupported by source. The false-proof case is a fluent model summary that hides missing boundary text; it must fail as evidence. Do not implement verbatim governance or Collision analysis. Record commands, environment, fixture identity, actual property proved, limitations, control state, and exact commit SHA. Request the CA-M014 operator decision and stop. Preserve the distinction between fact, hypothesis, and operator decision. Do not convert a green test into proof of a wider property. If a required dependency is unavailable or a higher-order invariant conflicts with the proposed change, record the collision, classify it, update control state, request the appropriate operator decision, and stop rather than inventing a substitute. Never claim completion from documentation alone; every completion claim must point to executable evidence and its limitations.
```
