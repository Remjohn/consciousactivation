# CAE Mandate 001 — Immutable Three-Layer Audience Context

**Mandate ID:** `CA-M001`  
**Wave:** `01`  
**Canonical question:** `Q01`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 01 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 01, covering Questions 01–08. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer.

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.


## Execution posture

This mandate is an implementation contract, not a design invitation. The executing model MUST inspect the repository before changing anything, establish the current implementation state, and distinguish documented/ratified requirements from executable evidence. The Master 57-Question Canon is authoritative for the decision being implemented, while the repository's code, tests, schemas, migrations, manifests, and receipts determine what is actually implemented. A document that says a property is implemented is not executable proof of that property.

The implementation MUST preserve the authority hierarchy:

`Master 57-Question Canon → Product Brief / PRD / FR → UI.md + Architecture.md → this mandate → code → executable evidence`.

The mandate does not authorize redesign of adjacent stages, broad cleanup, opportunistic refactoring, or implementation of later questions merely because a dependency is encountered. If a dependency is missing, the executor must either implement only the minimum prerequisite explicitly required by this mandate or stop and record the blocker. Do not silently widen scope.

All new or changed behavior must be testable. Positive tests establish the intended path; negative tests establish the fail-closed boundary. Where a requirement depends on cryptographic identity, versioning, or immutable state, tests must verify those properties rather than merely checking that an object exists.

Every substantive claim in the completion report must be labeled by evidence class where useful: `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`.


## 2. Decision / objective being authorized

Implement the canonical Audience Context boundary as three strictly segregated, immutable layers — Market Macro Signals, Segment Cultural Archetypes, and Live Audience Tensions — with independent identity/digest/version handling so downstream systems cannot consume an ungoverned blended blob.

The implementation must make this decision true at the correct architectural boundary. It must not simulate the property in a presentation layer or encode a second authority model in the frontend. If the mandate requires a new object, revision, digest, admission predicate, or state transition, that object must be connected to the canonical runtime and must survive process boundaries where the architecture requires persistence.

## 3. Governing doctrine and authority sources

**Primary authority:**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md`
- `UI.md`
- `Architecture.md`

**Product/causal authority:**
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`

**Question-specific authority:**
Canonical invariant: `INV-AUD-001 / FR-AUD-001`. The canon identifies `services/pipeline/src/cmf_pipeline/adapters/synthetic.py` and `docs/cae/CAE_Product_Brief/01_Audience_Context.md` as the physical precheck surfaces.

The executor must treat the canon as the ratified requirement and the current repository as the implementation reality. Where the canon's zero-waste precheck identifies a missing capability, do not reinterpret that gap as permission to weaken the requirement.

## 4. Mandatory reading before action

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q01
- `UI.md` — audience/research inspection and runtime-authority sections
- `Architecture.md` — Sections 10–12 and authority model
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`
- `docs/cae/CAE_Product_Brief/01_Audience_Context.md` if present in the repository
- current audience context models/services, especially `services/pipeline/src/cmf_pipeline/adapters/synthetic.py` and their callers/tests

The executor MUST also inspect the relevant current code paths named by the canon and any directly imported types/functions they depend on. If a cited path has moved, locate the current equivalent and record the mapping rather than silently substituting an unrelated implementation.

## 5. Exact scope

Implement only the audience-context representation, persistence/identity semantics, validation/admission boundary, and the operator-readable projection required to make the three-layer contract real. Preserve the existing Campaign/workspace identity model. Each layer must be addressable independently and must not be silently merged into a mutable catch-all context object. A derived convergence object may reference the three layers, but it is not allowed to mutate them.

The implementation should make it mechanically possible to answer: which audience layer was used, which exact revision/digest was used, whether that layer is valid, and whether a downstream consumer attempted to use an unsealed or mutated layer. If the existing repository already has compatible structured signal types, extend them rather than creating duplicate models.

The operator surface should expose the three layers distinctly and expose revision/provenance information without creating browser-owned truth.

The scope ends at the smallest set of runtime, schema, test, and operator-facing changes necessary to prove this question. Adjacent questions are dependencies, not extra deliverables.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the files/modules named by the cited authority and their direct tests, plus the minimum supporting schema/migration/API/UI projection required to make the decision executable. New files are permitted only when they are the smallest direct implementation or test artifact needed. The executor must not modify unrelated programs, global policy, release semantics, certification claims, or later canonical questions.

The implementation may add tests, fixtures, schemas, migrations, typed models, runtime helpers, API wiring, or UI projections only where they are directly required by the decision. New abstractions require a concrete need demonstrated by the existing architecture.

## 7. Prohibitions and collision procedure

- Do not implement Question 02's convergence logic except for the minimum interface needed to expose the three audience layers.
- Do not treat a free-form audience note, LLM summary, or cached UI object as authoritative.
- Do not silently migrate all legacy callers to a new model if that migration would change unrelated semantics; use an explicit compatibility boundary.
- Do not claim immutability if callers can mutate the persisted object in place.
- Do not rely on a frontend snapshot to prove layer isolation.

If the implementation encounters a collision with an existing invariant, authority rule, schema, migration, or state machine:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved operator decision;
4. make the minimum safe correction only if this mandate clearly owns the correction;
5. otherwise record the collision and stop.

### Contrastive failure — the good-looking but wrong result

A successful-looking implementation that satisfies a superficial UI assertion, creates an object without binding it to canonical state, accepts invalid input because a model “seems confident,” or passes only happy-path tests is not completion. Such an implementation violates CAE's fail-closed and provenance principles even if the visible feature appears correct.

## 8. Required work / implementation behavior

1. Inventory current audience context types, storage, API contracts, tests, and synthetic adapters.
2. Define or normalize explicit types for the three layers and a parent audience-context package/reference.
3. Add deterministic identity/digest/version semantics for each layer.
4. Enforce write/update rules so a sealed revision cannot be mutated in place.
5. Add validation that rejects missing layers, duplicate/conflicting layer identities, and invalid revisions where the contract requires completeness.
6. Provide a canonical read path that returns the authoritative three-layer representation.
7. Update the relevant operator projection so the UI can inspect the layers separately.
8. Add positive and negative tests, including attempted cross-layer mutation and legacy/blended payload rejection where appropriate.
9. Run focused tests, then the relevant integration suite.
10. Record the exact evidence and any legacy compatibility limitations.

The executor must follow test-first or integration-first sequencing appropriate to the surface: establish the contract and negative cases, implement the smallest viable change, then verify the full path. For stateful behavior, test persistence and restart/reload behavior where relevant. For digest/version behavior, test mutation and mismatch cases. For UI behavior, verify that the UI is a projection of authoritative runtime data and does not invent local semantics.

## 9. Verification and evidence standard

Evidence must demonstrate independent layer identity and immutability, not merely that three JSON keys exist. Required proof includes schema/type evidence, executable positive tests, negative mutation/blended-representation tests, integration evidence through the real runtime/persistence boundary, and UI projection evidence.

False-proof countercase: a test that constructs `{market, archetype, tension}` in memory and asserts the keys exist. That proves shape, not immutable identity or runtime governance.
Environment fidelity: tests must exercise the repository's real persistence/runtime boundary for any claim about immutability or digest pinning.

Verification MUST include:
- a positive acceptance path;
- a negative/fail-closed path;
- a regression test for an adjacent existing behavior;
- an evidence locator identifying the exact test/file/receipt/schema that proves each material claim;
- a statement of what remains unproven.

Do not mark a requirement `VERIFIED` merely because a unit test passes if the canonical property is integration-level. If the property crosses runtime/API/database/UI boundaries, include an integration test. If the property depends on actual runtime behavior, include executable runtime evidence.

## 10. Completion and stop condition

Stop once the three-layer contract is implemented and evidenced at the authoritative boundary. If the existing persistence model cannot safely provide immutable revisions without a migration or a broader shared-state change, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires:
1. the requested artifact/behavior exists;
2. the declared acceptance tests pass;
3. negative paths fail closed as required;
4. no prohibited surface was changed;
5. limitations and residual blockers are recorded;
6. the exact commit SHA is captured;
7. the control-state record or equivalent implementation tracker is updated if one exists;
8. an explicit Operator decision is requested.

The executor MUST STOP after these conditions are met. It must not automatically begin the next mandate.

## 11. Rollback / recovery

Use an isolated revision or reversible migration. Never rewrite historical audience context rows in place. If a compatibility adapter is required, keep it read-only or explicitly versioned. If the implementation is found to have conflated the three layers, revert that change rather than adding another abstraction on top.

Rollback must preserve existing authoritative state and avoid destructive mutation. Prefer reverting the bounded implementation commit or using the repository's existing migration/revision mechanism. If a migration is introduced, it must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project's migration conventions.

## 12. Operator decision

Approve or reject the implementation based on whether the evidence proves independent, immutable, digest-addressable audience layers at the canonical runtime boundary.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M001` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q01, `UI.md`, `Architecture.md`, the CAE causal operating model, and the current audience-context implementation before editing. Implement `INV-AUD-001 / FR-AUD-001`: three strictly segregated, immutable layers — Market Macro Signals, Segment Cultural Archetypes, Live Audience Tensions — each independently identifiable and revision/digest pinned. Do not build Q02 convergence or any adjacent mandate. Do not use UI state, free-form notes, or model output as authority. Establish positive and negative executable evidence, including mutation rejection and invalid/blended representation rejection where applicable. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M001`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
