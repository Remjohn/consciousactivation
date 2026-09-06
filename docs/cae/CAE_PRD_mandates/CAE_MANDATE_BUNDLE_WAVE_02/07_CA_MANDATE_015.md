# CAE Mandate M015 — Verbatim Spoken Capture Integrity

**Mandate ID:** `CA-M015`  
**Wave:** `02`  
**Canonical question:** `Q15`  
**Causal stage:** `Stage 07 — Evidence Capture`  
**Governing requirement / invariant:** `FR-015 / verbatim quote integrity`  
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

Enforce the distinction between raw spoken capture and editorial meaning. A quote admitted as verbatim evidence must preserve the exact spoken form required by the project contract, its source coordinate, transcript/character span, immutable identity, and provenance. A semantically equivalent paraphrase is not verbatim. This is the anti-genericization boundary before downstream composition.

The implementation must make the decision true at the correct architectural boundary. Do not simulate it in presentation code, prose, or a test-only fixture. Where state changes, use the project’s governed state/command path and emit the required receipt. Where a derivative artifact is produced, retain direct lineage to its source authority. Where revisioning applies, prior revisions remain inspectable and immutable where the contract requires immutability.

## 3. Governing doctrine and authority sources

**Primary authority**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q15`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`

**Question / product authority**
- `Architecture.md` Section 14 and evidence authority guidance.\n- `UI.md` Sections 13–14.\n- `PRD-003` verbatim/evidence material.\n- Wave 02 readiness assessment: CA-M015 / Q15.\n- Existing transcript storage, quote/evidence models, source-span validation, collision verifier/composer boundaries, and tests.

The Wave 02 readiness assessment supplied with this execution context explicitly defines CAE Wave 02 as Q09–Q16 and names this mandate as `CA-M015` / `Q15`. That planning statement is a source of intended scope; the current repository remains the source of executable truth.

If the repository differs from the cited target, classify the discrepancy as `DOCUMENT`, `EXECUTABLE`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED` evidence. Never turn a design statement into a false completion claim.

## 4. Mandatory reading before action

Before planning or editing, read the full contents where present of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — `Q15`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- the Wave 02 readiness assessment that defines Q09–Q16
- the CAE convergence spine / decision ledger
- directly relevant PRD module(s)
- current executable code, schemas, migrations, manifests, and direct tests

Question-specific mandatory reading:
- current transcript/span representation;\n- quote/evidence model and hash/digest behavior;\n- source-coordinate validator;\n- composition consumer for quotes;\n- direct tests;\n- current Canon Q15 / FR-015 contract if present.

If a cited path moved, locate the current equivalent and record the mapping in the evidence record. Missing required authority is `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not permission to invent a replacement.

## 5. Exact scope

Own verbatim evidence representation and admission. Reuse existing transcript/source span primitives. Preserve exact text under the project-defined verbatim policy, including relevant disfluencies/cadence markers where required, while keeping semantic annotations separate. Bind quote identity to source digest, temporal anchor, and source span. Downstream composition must consume the governed verbatim representation rather than regenerate it from summaries or model rationales.

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

- Do not clean grammar for aesthetic reasons.\n- Do not treat “same meaning” as proof of verbatim identity.\n- Do not regenerate quotes from summaries or embeddings.\n- Do not mutate historical verbatim evidence in place.\n- Do not broaden into all editorial prose.\n- Do not use similarity metrics as the sole proof of verbatimness.

If a collision appears:
1. Stop before the conflicting change.
2. Identify the controlling authority.
3. Classify it using the project error taxonomy (`AUTHORITY_ERROR`, `SCOPE_ERROR`, `TAXONOMY_ERROR`, `SCHEMA_ERROR`, `RELATION_ERROR`, `STATE_ERROR`, `EVIDENCE_ERROR`, `PROVENANCE_ERROR`, `SEMANTIC_DRIFT`, `EDITORIAL_DRIFT`, `FORMAT_DRIFT`, `COMPOSITION_ERROR`, `RUNTIME_ERROR`, `REWARD_HACK`, or `ENVIRONMENT_FIDELITY_ERROR` as applicable).
4. Make the minimum correction only if this mandate clearly owns it.
5. Otherwise record the collision with evidence and stop.

### Contrastive failure — the good-looking but wrong result

The project requires at least one anti-centroid or false-proof case. A result can look polished, pass a shallow schema check, or score highly while violating the actual causal invariant. Such a result is a failure, not “partial success.” The mandate-specific false-proof case appears in the verification section and must be executable where possible.

## 8. Required work / implementation behavior

1. Inventory source-bound quote/evidence behavior. 2. Define/reuse canonical verbatim identity. 3. Bind text to source digest, anchor, and character/span evidence. 4. Implement exact or contract-defined equality validation. 5. Ensure composition reads the canonical evidence representation. 6. Add positive tests for exact spoken text and relevant disfluencies. 7. Add negative tests for grammar-cleaned paraphrase, same-meaning rewrite, material punctuation/character changes, stale span, and missing lineage. 8. Keep a project-specific hard negative where the rewritten text sounds superior but is not spoken. 9. Record transcription limitations honestly.

Every newly created or changed canonical object must preserve stable identity, owner/scope, authority axes, lifecycle, and direct upstream lineage. Revision or digest semantics must be retained where the contract requires them. Relations must expose their endpoints and direction/cardinality where relevant. Receipts must contain enough information for another agent to reconstruct what changed and why.

Positive tests establish the intended path. Negative tests establish the fail-closed boundary and are mandatory for stale, forged, missing, contradictory, or unanchored inputs applicable to the mandate.

## 9. Verification and evidence standard

The verifier must establish actual source-text equality or the exact project-defined verbatim policy. What is measured: source-bound quote identity, span integrity, and downstream consumption of canonical spoken text. What is not measured: global transcription perfection or editorial usefulness. False-proof case: an LLM rewrites a quote into grammatically perfect prose with identical meaning; semantic similarity would pass, but the verbatim contract must reject it. Environment fidelity requires real transcript/evidence storage and the downstream composition input boundary where feasible.

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

Stop before Q16 Collision formation. The handoff must provide immutable, source-bound verbatim evidence that can be used as a grounded input. Do not implement candidate clustering, operator selection, or composition.

## 11. Rollback / recovery

Corrected transcription/quote evidence creates a new governed revision. Do not silently overwrite a prior quote referenced downstream. Invalidated quote lineage must remain discoverable so downstream objects can be blocked or rebuilt under their own mandates.

Documentation and canonical artifacts are versioned and superseded rather than silently rewritten. Runtime changes retain receipts. External side effects must not be called transactional unless the implementation proves it.

## 12. Operator decision

**Operator decision required:** Approve CA-M015 and authorize CA-M016; confirm that verbatim evidence is accepted as a grounded input for Collision formation.

Until this decision is recorded in CAE control state, the next dependent mandate is unauthorized.

## 13. 200–300 word activation prompt

```text
Execute `CA-M015` only. Read the Mandate Authoring Protocol, Gemini execution skill, Master Canon Q15, `Architecture.md` Section 14, `UI.md` Sections 13–14, Wave 02 readiness assessment, PRD-003 verbatim/evidence material, and the current transcript, source-span, evidence verifier, and composition-consumer surfaces. Enforce the distinction between raw spoken form and editorial meaning. A verbatim evidence object must remain bound to sovereign source digest, temporal anchor, transcript/character span, and immutable provenance. Prove exact-source cases and negative same-meaning rewrite cases. Specifically replace a real quote with grammatically improved prose that means the same thing; the system must reject it as verbatim even if semantic similarity is high. Reject stale spans, lineage gaps, and unauthorized quote regeneration. Do not use similarity alone. Do not implement Collision discovery. Record commands, environment, fixture/source identity, actual property proved, limitations, control state, and exact commit SHA. Request the CA-M015 operator decision and stop. Preserve the distinction between fact, hypothesis, and operator decision. Do not convert a green test into proof of a wider property. If a required dependency is unavailable or a higher-order invariant conflicts with the proposed change, record the collision, classify it, update control state, request the appropriate operator decision, and stop rather than inventing a substitute. Never claim completion from documentation alone; every completion claim must point to executable evidence and its limitations.
```
