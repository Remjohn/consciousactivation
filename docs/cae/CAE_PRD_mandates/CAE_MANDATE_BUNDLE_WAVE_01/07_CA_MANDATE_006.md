# CAE Mandate 006 — Many-to-Many Activative to Elicitation Binding

**Mandate ID:** `CA-M006`  
**Wave:** `01`  
**Canonical question:** `Q06`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 06 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 01, covering Questions 01–08. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer.

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

Implement explicit many-to-many causal links between Activatives and Elicitation Units so one strategic transformation vector can require multiple elicitation units and one elicitation unit can contribute evidence to multiple Activatives.

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
Canonical invariant: `FR-ELIC-001`. The canon identifies `programs/interview_semantic_program/program_manifest.yaml` and `docs/cae/CAE_Product_Brief/06_Structured_Elicitation.md` as precheck surfaces.

The executor must treat the canon as the ratified requirement and the current repository as the implementation reality. Where the canon's zero-waste precheck identifies a missing capability, do not reinterpret that gap as permission to weaken the requirement.

## 4. Mandatory reading before action

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q06
- `UI.md` — Sections 12, 15, 17
- `Architecture.md` — Sections 10, 12, 13
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`
- `docs/cae/CAE_Product_Brief/06_Structured_Elicitation.md`
- `programs/interview_semantic_program/program_manifest.yaml`
- current Activative/Elicitation Unit types, interview planning, persistence, and tests

The executor MUST also inspect the relevant current code paths named by the canon and any directly imported types/functions they depend on. If a cited path has moved, locate the current equivalent and record the mapping rather than silently substituting an unrelated implementation.

## 5. Exact scope

The mandate owns the relationship model and its runtime/API projections. It does not own the creation semantics of Activatives; Q07 governs that. It does not own holistic interview completion; Q22 does.

Each link must preserve causal identity: which Activative, which Elicitation Unit, which revisions, and what role the relationship plays. The relationship must be queryable in both directions. A many-to-many model must not be implemented as duplicated free-text labels.

The Operator must be able to inspect an Elicitation Unit and see all linked Activatives, and inspect an Activative and see all supporting Elicitation Units.

The scope ends at the smallest set of runtime, schema, test, and operator-facing changes necessary to prove this question. Adjacent questions are dependencies, not extra deliverables.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the files/modules named by the cited authority and their direct tests, plus the minimum supporting schema/migration/API/UI projection required to make the decision executable. New files are permitted only when they are the smallest direct implementation or test artifact needed. The executor must not modify unrelated programs, global policy, release semantics, certification claims, or later canonical questions.

The implementation may add tests, fixtures, schemas, migrations, typed models, runtime helpers, API wiring, or UI projections only where they are directly required by the decision. New abstractions require a concrete need demonstrated by the existing architecture.

## 7. Prohibitions and collision procedure

- Do not use comma-separated IDs or free-text topic labels as the authoritative relationship.
- Do not force one-to-one ownership merely because the current UI is simpler.
- Do not silently duplicate Elicitation Units to simulate many-to-many semantics.
- Do not allow links to nonexistent or unauthorized parent objects.
- Do not implement Activative derivation in this mandate.

If the implementation encounters a collision with an existing invariant, authority rule, schema, migration, or state machine:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved operator decision;
4. make the minimum safe correction only if this mandate clearly owns the correction;
5. otherwise record the collision and stop.

### Contrastive failure — the good-looking but wrong result

A successful-looking implementation that satisfies a superficial UI assertion, creates an object without binding it to canonical state, accepts invalid input because a model “seems confident,” or passes only happy-path tests is not completion. Such an implementation violates CAE's fail-closed and provenance principles even if the visible feature appears correct.

## 8. Required work / implementation behavior

1. Inspect existing Activative and Elicitation Unit representations and determine whether a join/edge object already exists.
2. Define the smallest explicit relationship representation needed for many-to-many linkage.
3. Enforce referential integrity and revision semantics.
4. Provide canonical read paths in both directions.
5. Update interview planning/runtime inputs so the relationship can be consumed without parsing labels.
6. Update the operator projection to expose the relationship.
7. Add positive tests for one-to-many, many-to-one, and true many-to-many cases.
8. Add negative tests for missing parents, duplicate edges, invalid revisions, and unauthorized cross-workspace links where applicable.
9. Add integration evidence that the interview manifest can consume the relationships.
10. Record evidence and stop.

The executor must follow test-first or integration-first sequencing appropriate to the surface: establish the contract and negative cases, implement the smallest viable change, then verify the full path. For stateful behavior, test persistence and restart/reload behavior where relevant. For digest/version behavior, test mutation and mismatch cases. For UI behavior, verify that the UI is a projection of authoritative runtime data and does not invent local semantics.

## 9. Verification and evidence standard

Evidence must prove actual bidirectional causal linkage: schema/model evidence for the relationship; executable tests for one-to-many, many-to-one, and many-to-many; negative tests for invalid/duplicate/cross-boundary links; integration proof that interview planning can retrieve linked Activatives/Elicitation Units from authoritative state; and UI projection proof.

False-proof countercase: storing arrays of IDs on both objects and testing only that they contain matching strings. That can drift and does not establish a governed edge.
Environment fidelity: use the repository's actual persistence and runtime path for relationship integrity.

Verification MUST include:
- a positive acceptance path;
- a negative/fail-closed path;
- a regression test for an adjacent existing behavior;
- an evidence locator identifying the exact test/file/receipt/schema that proves each material claim;
- a statement of what remains unproven.

Do not mark a requirement `VERIFIED` merely because a unit test passes if the canonical property is integration-level. If the property crosses runtime/API/database/UI boundaries, include an integration test. If the property depends on actual runtime behavior, include executable runtime evidence.

## 10. Completion and stop condition

Stop when explicit many-to-many linkage exists, is authoritative, queryable in both directions, and is consumed by the scoped interview-planning path. If a broader schema migration is required, implement only the relationship migration and document unrelated consumers that remain to be migrated.

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

Prefer additive relationship records/migrations. Preserve existing historical references. If dual-read compatibility is required, keep one authoritative representation and make the compatibility layer read-only or transitional.

Rollback must preserve existing authoritative state and avoid destructive mutation. Prefer reverting the bounded implementation commit or using the repository's existing migration/revision mechanism. If a migration is introduced, it must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project's migration conventions.

## 12. Operator decision

Approve or reject whether Activatives and Elicitation Units now have explicit, durable, revision-aware many-to-many causal links.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> Execute `CA-M006` only. Read the protocol, Master Canon Q06, `UI.md` Section 12, `Architecture.md` Section 12, the causal operating model, the Structured Elicitation product brief, and the interview semantic manifest. Implement `FR-ELIC-001`: explicit many-to-many causal links between Activatives and Elicitation Units. Do not derive or redesign Activatives; do not implement holistic yield completion. Use a governed relationship representation rather than labels or duplicated IDs, preserve revision/workspace identity, and make both directions queryable. Add positive one-to-many, many-to-one, and many-to-many tests plus negative invalid/duplicate/boundary tests. Ensure the interview planning path consumes the authoritative relationships and the UI only projects them. Stop if required authority is missing. Finish with exact evidence locators, changed files, tests, limitations, commit SHA, and Operator approval/rejection request. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
