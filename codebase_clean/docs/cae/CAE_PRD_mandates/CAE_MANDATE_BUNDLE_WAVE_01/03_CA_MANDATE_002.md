# CAE Mandate 002 — Dual-Context Convergence Gate

**Mandate ID:** `CA-M002`  
**Wave:** `01`  
**Canonical question:** `Q02`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 02 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 01, covering Questions 01–08. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer.

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

Implement the hard admission boundary that prevents downstream narrative compilation unless validated Guest Genesis Semantic Territory and Audience Tensions are both present, valid, and converged under the canonical runtime.

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
Canonical invariant: `FR-CONV-001`. The canon identifies `packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py` and `programs/guest_genesis_semantic_territory_program/program_manifest.yaml` as the precheck surfaces.

The executor must treat the canon as the ratified requirement and the current repository as the implementation reality. Where the canon's zero-waste precheck identifies a missing capability, do not reinterpret that gap as permission to weaken the requirement.

## 4. Mandatory reading before action

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q02
- `UI.md` — Sections 10, 15, 18, and 22
- `Architecture.md` — Sections 10–12 and authority model
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`
- `packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py`
- `programs/guest_genesis_semantic_territory_program/program_manifest.yaml`
- current tests and API/runtime callers for collision/narrative admission

The executor MUST also inspect the relevant current code paths named by the canon and any directly imported types/functions they depend on. If a cited path has moved, locate the current equivalent and record the mapping rather than silently substituting an unrelated implementation.

## 5. Exact scope

The mandate owns the admission predicate and its authoritative execution boundary. It does not own the creation of Guest DNA, Audience Context, or downstream narrative composition. It may introduce or normalize a typed converged-context receipt only if that is the minimum physical representation needed to prove the gate.

The gate must verify both sides independently: Guest Genesis Semantic Territory and Audience Tensions. “Present” is not enough; each required source must be valid under its own contract, and the convergence result must identify the exact upstream revisions/digests. The resulting admission record must be inspectable by runtime and UI projections.

The operator must be able to see why execution is blocked without being able to bypass the gate through a browser flag or direct API shortcut.

The scope ends at the smallest set of runtime, schema, test, and operator-facing changes necessary to prove this question. Adjacent questions are dependencies, not extra deliverables.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the files/modules named by the cited authority and their direct tests, plus the minimum supporting schema/migration/API/UI projection required to make the decision executable. New files are permitted only when they are the smallest direct implementation or test artifact needed. The executor must not modify unrelated programs, global policy, release semantics, certification claims, or later canonical questions.

The implementation may add tests, fixtures, schemas, migrations, typed models, runtime helpers, API wiring, or UI projections only where they are directly required by the decision. New abstractions require a concrete need demonstrated by the existing architecture.

## 7. Prohibitions and collision procedure

- Do not create a fallback path that proceeds with only one context source.
- Do not allow a model-generated convergence narrative to substitute for validated upstream artifacts.
- Do not make the UI responsible for deciding whether convergence exists.
- Do not mark a downstream program ready merely because the gate returned a human-readable explanation.
- Do not implement broader narrative architecture in this mandate.

If the implementation encounters a collision with an existing invariant, authority rule, schema, migration, or state machine:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved operator decision;
4. make the minimum safe correction only if this mandate clearly owns the correction;
5. otherwise record the collision and stop.

### Contrastive failure — the good-looking but wrong result

A successful-looking implementation that satisfies a superficial UI assertion, creates an object without binding it to canonical state, accepts invalid input because a model “seems confident,” or passes only happy-path tests is not completion. Such an implementation violates CAE's fail-closed and provenance principles even if the visible feature appears correct.

## 8. Required work / implementation behavior

1. Inspect current collision/narrative admission flow and identify every entry path that could bypass the convergence prerequisite.
2. Define the minimal canonical predicate: both required upstream artifacts valid, exact revisions/digests available, and a valid convergence relation/receipt.
3. Enforce the predicate in the canonical runtime admission boundary, not only in one UI route.
4. Ensure failed admission returns a structured reason and permitted next action.
5. Ensure successful admission binds downstream execution to the exact upstream revisions.
6. Add positive tests for valid convergence.
7. Add negative tests for missing Guest DNA, missing Audience Tensions, invalid source revisions, and stale/mismatched convergence.
8. Add an integration test proving downstream compilation cannot start when the gate fails.
9. Expose the gate state/provenance to the operator surface without duplicating authority.
10. Run the relevant runtime and API suites and record evidence.

The executor must follow test-first or integration-first sequencing appropriate to the surface: establish the contract and negative cases, implement the smallest viable change, then verify the full path. For stateful behavior, test persistence and restart/reload behavior where relevant. For digest/version behavior, test mutation and mismatch cases. For UI behavior, verify that the UI is a projection of authoritative runtime data and does not invent local semantics.

## 9. Verification and evidence standard

The evidence standard is an execution-level admission proof. Required evidence includes executable predicate tests, negative tests for each missing/invalid side, mismatch/staleness tests, integration proof that downstream compilation is blocked before execution, exact runtime admission locators, and UI projection evidence.

False-proof countercase: a unit test that calls the convergence helper directly while the actual narrative entrypoint bypasses it. That is not sufficient.
Environment fidelity: at least one test must exercise the same canonical command/program admission path used by the application.

Verification MUST include:
- a positive acceptance path;
- a negative/fail-closed path;
- a regression test for an adjacent existing behavior;
- an evidence locator identifying the exact test/file/receipt/schema that proves each material claim;
- a statement of what remains unproven.

Do not mark a requirement `VERIFIED` merely because a unit test passes if the canonical property is integration-level. If the property crosses runtime/API/database/UI boundaries, include an integration test. If the property depends on actual runtime behavior, include executable runtime evidence.

## 10. Completion and stop condition

Stop when every known downstream entry path is governed by the canonical convergence predicate and the positive/negative integration evidence passes. If a bypass exists in an adjacent program that this mandate does not safely own, stop and report the exact bypass rather than patching unrelated architecture.

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

Rollback by reverting the bounded admission changes. Do not remove or alter upstream evidence to make tests pass. If a new receipt/schema is introduced and the repository requires migrations, use the project's migration mechanism and record recovery instructions.

Rollback must preserve existing authoritative state and avoid destructive mutation. Prefer reverting the bounded implementation commit or using the repository's existing migration/revision mechanism. If a migration is introduced, it must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project's migration conventions.

## 12. Operator decision

Approve or reject based on whether downstream narrative admission is demonstrably fail-closed on absent, invalid, or stale dual-context convergence.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> Execute `CA-M002` only. Read the Mandate Authoring Protocol, Master Canon Q02, `UI.md`, `Architecture.md`, the causal operating model, `collision_hypothesis_program.py`, and the guest-genesis manifest. Implement `FR-CONV-001`: downstream narrative compilation must fail closed unless Guest Genesis Semantic Territory and Audience Tensions are both independently valid and converged, with exact upstream revision/digest binding. Do not build new narrative semantics or bypass runtime authority. Inspect every downstream entry path that could avoid the gate. Add positive evidence for valid convergence and negative evidence for missing, invalid, stale, or mismatched sources. Ensure the UI exposes the blocker as a runtime contract failure, not an AI error, while remaining a projection. If a bypass or dependency is outside this mandate’s safe scope, stop and report it rather than widening scope. Finish with changed files, tests, evidence locators, limitations, commit SHA, and an explicit Operator approval/rejection request. Stop after `CA-M002` is evidenced. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
