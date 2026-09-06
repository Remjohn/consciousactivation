# CAE Mandate 004 — Canonical Pipeline Ordering and Causal Admission

**Mandate ID:** `CA-M004`  
**Wave:** `01`  
**Canonical question:** `Q04`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 04 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 01, covering Questions 01–08. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer.

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

Enforce the canonical causal order so downstream programs cannot execute out of order or back-fill missing upstream meaning; every stage must be admitted only when its required ancestor outputs and integrity identities are valid.

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
Canonical invariant: `INV-CAUSAL-001`. The canon identifies `programs/editorial_storyboard_program/program_manifest.yaml` and `docs/PRD/CURRENT.md` as precheck surfaces.

The executor must treat the canon as the ratified requirement and the current repository as the implementation reality. Where the canon's zero-waste precheck identifies a missing capability, do not reinterpret that gap as permission to weaken the requirement.

## 4. Mandatory reading before action

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q04
- `UI.md` — Sections 8, 9, 15, 18, 22
- `Architecture.md` — Sections 4, 7, 10, 22–24, 31
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`
- `docs/PRD/CURRENT.md`
- `programs/editorial_storyboard_program/program_manifest.yaml`
- current program registry, state machine, admission, and dependency-resolution code

The executor MUST also inspect the relevant current code paths named by the canon and any directly imported types/functions they depend on. If a cited path has moved, locate the current equivalent and record the mapping rather than silently substituting an unrelated implementation.

## 5. Exact scope

The mandate owns causal admission/order enforcement and the minimum manifest/state metadata required to enforce it. It does not redesign every program's business logic. The canonical 17-stage sequence remains the product-level spine, while individual programs may have their own local state machines.

For each governed transition, the runtime must know the required upstream objects and integrity identities. A downstream node cannot fabricate an upstream placeholder merely to satisfy an input schema. If an upstream artifact is missing, stale, invalid, or not admitted, the correct result is a structured block.

Where the repository already has dependency declarations, use them as inputs to the enforcement mechanism rather than duplicating a second dependency graph.

The scope ends at the smallest set of runtime, schema, test, and operator-facing changes necessary to prove this question. Adjacent questions are dependencies, not extra deliverables.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the files/modules named by the cited authority and their direct tests, plus the minimum supporting schema/migration/API/UI projection required to make the decision executable. New files are permitted only when they are the smallest direct implementation or test artifact needed. The executor must not modify unrelated programs, global policy, release semantics, certification claims, or later canonical questions.

The implementation may add tests, fixtures, schemas, migrations, typed models, runtime helpers, API wiring, or UI projections only where they are directly required by the decision. New abstractions require a concrete need demonstrated by the existing architecture.

## 7. Prohibitions and collision procedure

- Do not enforce ordering only in React or route guards.
- Do not allow “force run” to bypass causal admission.
- Do not create fake ancestor artifacts for tests that are later mistaken for production evidence.
- Do not conflate chronological execution with semantic authority.
- Do not implement all 17 stages in this mandate.

If the implementation encounters a collision with an existing invariant, authority rule, schema, migration, or state machine:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved operator decision;
4. make the minimum safe correction only if this mandate clearly owns the correction;
5. otherwise record the collision and stop.

### Contrastive failure — the good-looking but wrong result

A successful-looking implementation that satisfies a superficial UI assertion, creates an object without binding it to canonical state, accepts invalid input because a model “seems confident,” or passes only happy-path tests is not completion. Such an implementation violates CAE's fail-closed and provenance principles even if the visible feature appears correct.

## 8. Required work / implementation behavior

1. Map the current program registry, manifests, state machines, and dependency checks.
2. Define the minimal admission representation for required ancestors and their digests/revisions.
3. Implement runtime admission checks for the affected execution path(s).
4. Reject out-of-order execution, missing ancestors, stale/mismatched ancestor identities, and invalid prerequisite states.
5. Preserve explicit recovery paths rather than silently synthesizing missing meaning.
6. Add positive tests for valid causal progression.
7. Add negative tests for missing ancestor, wrong order, stale digest, invalid state, and forced UI/API invocation.
8. Add an integration test through the canonical program execution boundary.
9. Ensure the pipeline UI reports the actual blocked stage and reason from runtime state.
10. Record evidence and stop.

The executor must follow test-first or integration-first sequencing appropriate to the surface: establish the contract and negative cases, implement the smallest viable change, then verify the full path. For stateful behavior, test persistence and restart/reload behavior where relevant. For digest/version behavior, test mutation and mismatch cases. For UI behavior, verify that the UI is a projection of authoritative runtime data and does not invent local semantics.

## 9. Verification and evidence standard

Evidence must show that ordering is enforced where execution actually occurs: executable admission tests; negative tests for bypass attempts through API/runtime paths; integration evidence using a real declared program manifest; proof that ancestor identity is bound to the admitted object rather than a display name; and UI evidence that blocked state is a projection of runtime truth.

False-proof countercase: testing a helper function while the program runner can invoke the downstream program directly. That is not evidence of causal enforcement.
Environment fidelity: the strongest test must traverse the same runtime admission boundary used by production program execution.

Verification MUST include:
- a positive acceptance path;
- a negative/fail-closed path;
- a regression test for an adjacent existing behavior;
- an evidence locator identifying the exact test/file/receipt/schema that proves each material claim;
- a statement of what remains unproven.

Do not mark a requirement `VERIFIED` merely because a unit test passes if the canonical property is integration-level. If the property crosses runtime/API/database/UI boundaries, include an integration test. If the property depends on actual runtime behavior, include executable runtime evidence.

## 10. Completion and stop condition

Stop once the affected canonical execution paths are causally gated and evidence is recorded. If enforcing all program dependencies requires a registry redesign outside this mandate, implement the smallest safe boundary and document the remaining paths rather than widening scope.

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

Revert the admission changes if they create deadlocks or invalidate legitimate existing program execution. Preserve historical state. Do not delete artifacts to make ordering tests pass.

Rollback must preserve existing authoritative state and avoid destructive mutation. Prefer reverting the bounded implementation commit or using the repository's existing migration/revision mechanism. If a migration is introduced, it must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project's migration conventions.

## 12. Operator decision

Approve or reject whether the runtime now demonstrably prevents downstream execution from inventing or bypassing missing upstream meaning for the scoped programs.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> Execute `CA-M004` only. Read the protocol, Master Canon Q04, `UI.md`, `Architecture.md`, the causal operating model, `docs/PRD/CURRENT.md`, and the editorial storyboard manifest plus current runtime registry/state code. Implement `INV-CAUSAL-001`: causal order and required ancestor integrity must be enforced at the runtime admission boundary. A downstream program must not run because a UI says it is ready, because a caller supplies a display-name placeholder, or because a missing ancestor was synthesized. Add positive and negative executable evidence for valid progression, missing ancestors, wrong order, stale/mismatched identity, invalid state, and API/runtime bypass attempts. Keep scope bounded; do not implement the entire 17-stage system. Surface real blockers to the UI as runtime facts. Stop on unresolved architectural collisions. Finish with evidence locators, changed files, tests, limitations, commit SHA, and an explicit Operator decision. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
