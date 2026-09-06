# CAE Mandate 007 — Activative as Derived Strategic Execution Object

**Mandate ID:** `CA-M007`  
**Wave:** `01`  
**Canonical question:** `Q07`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 07 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 01, covering Questions 01–08. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer.

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

Implement the Activative as a derived strategic execution object that can only be admitted when grounded in an approved upstream collision hypothesis and tension vector, rather than allowing raw topics or manually inserted prompts to become Activatives.

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
Canonical invariant: `INV-ACT-001`. The canon identifies `packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py#L220-L280` and the interview program's `approved_collision_hypothesis` input as the key precheck surfaces.

The executor must treat the canon as the ratified requirement and the current repository as the implementation reality. Where the canon's zero-waste precheck identifies a missing capability, do not reinterpret that gap as permission to weaken the requirement.

## 4. Mandatory reading before action

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q07
- `UI.md` — Sections 12 and 15
- `Architecture.md` — Sections 10, 12, 16, 20
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`
- `packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py`
- `programs/interview_semantic_program/program_manifest.yaml`
- current Activative models, collision hypothesis store, API, and tests

The executor MUST also inspect the relevant current code paths named by the canon and any directly imported types/functions they depend on. If a cited path has moved, locate the current equivalent and record the mapping rather than silently substituting an unrelated implementation.

## 5. Exact scope

The mandate owns Activative admission and lineage, not collision discovery itself. A valid Activative must point to the exact upstream collision hypothesis receipt/revision and the relevant tension vector/context. The Activative may contain strategic transformation instructions, but it must not masquerade as a raw question, topic, or transcript fragment.

The runtime must reject manual insertion that lacks the required upstream authority. Operator editing may be allowed only where the existing product contract permits bounded amendment, and any such amendment must remain derivative of the approved upstream hypothesis rather than replacing it.

The UI should show the Activative's source hypothesis and causal purpose.

The scope ends at the smallest set of runtime, schema, test, and operator-facing changes necessary to prove this question. Adjacent questions are dependencies, not extra deliverables.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the files/modules named by the cited authority and their direct tests, plus the minimum supporting schema/migration/API/UI projection required to make the decision executable. New files are permitted only when they are the smallest direct implementation or test artifact needed. The executor must not modify unrelated programs, global policy, release semantics, certification claims, or later canonical questions.

The implementation may add tests, fixtures, schemas, migrations, typed models, runtime helpers, API wiring, or UI projections only where they are directly required by the decision. New abstractions require a concrete need demonstrated by the existing architecture.

## 7. Prohibitions and collision procedure

- Do not allow a free-text topic to be saved directly as an Activative.
- Do not let a model response self-authorize its own collision hypothesis.
- Do not create an Activative from a raw transcript without the required upstream collision authority.
- Do not alter collision discovery logic unless the current implementation makes Q07 impossible.
- Do not use UI state as proof of derivation.

If the implementation encounters a collision with an existing invariant, authority rule, schema, migration, or state machine:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved operator decision;
4. make the minimum safe correction only if this mandate clearly owns the correction;
5. otherwise record the collision and stop.

### Contrastive failure — the good-looking but wrong result

A successful-looking implementation that satisfies a superficial UI assertion, creates an object without binding it to canonical state, accepts invalid input because a model “seems confident,” or passes only happy-path tests is not completion. Such an implementation violates CAE's fail-closed and provenance principles even if the visible feature appears correct.

## 8. Required work / implementation behavior

1. Inspect current collision hypothesis, Activative, and interview input contracts.
2. Define the minimal Activative identity/lineage fields.
3. Enforce creation/admission only from an approved collision hypothesis and required tension vector/context.
4. Persist the exact parent receipt/revision.
5. Ensure downstream interview programs receive the governed Activative rather than a raw topic.
6. Add positive tests for valid derivation.
7. Add negative tests for raw topic insertion, missing parent receipt, stale parent revision, and unauthorized workspace linkage.
8. Add integration evidence from collision hypothesis approval through Activative admission.
9. Expose lineage to the operator.
10. Record evidence and stop.

The executor must follow test-first or integration-first sequencing appropriate to the surface: establish the contract and negative cases, implement the smallest viable change, then verify the full path. For stateful behavior, test persistence and restart/reload behavior where relevant. For digest/version behavior, test mutation and mismatch cases. For UI behavior, verify that the UI is a projection of authoritative runtime data and does not invent local semantics.

## 9. Verification and evidence standard

Required proof includes executable schema/runtime evidence of parent collision-hypothesis linkage; positive derivation test; negative raw-topic/manual insertion test; stale/mismatched parent test; integration test proving interview execution receives a derived Activative; and UI evidence showing parent hypothesis and purpose.

False-proof countercase: requiring a `collision_id` field while allowing any arbitrary string. The field alone does not prove the referenced hypothesis is approved or authoritative.
Human validation may still be required for the semantic quality of the Activative; this mandate proves derivation and authority mechanics.

Verification MUST include:
- a positive acceptance path;
- a negative/fail-closed path;
- a regression test for an adjacent existing behavior;
- an evidence locator identifying the exact test/file/receipt/schema that proves each material claim;
- a statement of what remains unproven.

Do not mark a requirement `VERIFIED` merely because a unit test passes if the canonical property is integration-level. If the property crosses runtime/API/database/UI boundaries, include an integration test. If the property depends on actual runtime behavior, include executable runtime evidence.

## 10. Completion and stop condition

Stop when Activative admission is causally grounded and raw insertion is rejected. If the existing collision-hypothesis store cannot expose an authoritative approval receipt without implementing later functionality, use the smallest existing approved state/receipt mechanism and document the dependency; do not invent a parallel approval system.

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

Do not delete or rewrite collision hypotheses. Roll back only the bounded Activative admission changes. Preserve existing downstream data and migrate it explicitly if historical records lack lineage.

Rollback must preserve existing authoritative state and avoid destructive mutation. Prefer reverting the bounded implementation commit or using the repository's existing migration/revision mechanism. If a migration is introduced, it must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project's migration conventions.

## 12. Operator decision

Approve or reject whether an Activative is now demonstrably a derived strategic execution object rather than an arbitrary downstream prompt.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> Execute `CA-M007` only. Read the protocol, Master Canon Q07, `UI.md`, `Architecture.md`, the causal operating model, current collision hypothesis code/store, and the interview semantic manifest. Implement `INV-ACT-001`: an Activative must be derived from an approved upstream collision hypothesis and relevant tension vector/context. Reject raw topic/manual insertion that lacks the required upstream authority. Persist exact parent identity/revision/receipt and expose lineage to the operator. Do not redesign collision discovery or implement later collision semantics. Add positive derivation and negative raw-topic, missing-parent, stale-parent, and boundary tests, plus an integration proof through the interview input path. If the repository lacks an authoritative parent state, stop and document the dependency instead of inventing authority. Report evidence, limitations, changed files, tests, commit SHA, and request Operator approval or rejection. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
