# CAE Mandate 005 — Format and Archetype Matchmaking Gate

**Mandate ID:** `CA-M005`  
**Wave:** `01`  
**Canonical question:** `Q05`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 05 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 01, covering Questions 01–08. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer.

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

Implement the format-feasibility and archetype-coalition admission gate so incompatible narrative structures cannot proceed into PreProduction.

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
Canonical invariant: `FR-ARCH-001`. The canon identifies `cae_collision_intelligence/composer.py` and `services/pipeline/src/cmf_pipeline/candidates/service.py` as precheck surfaces.

The executor must treat the canon as the ratified requirement and the current repository as the implementation reality. Where the canon's zero-waste precheck identifies a missing capability, do not reinterpret that gap as permission to weaken the requirement.

## 4. Mandatory reading before action

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q05
- `UI.md` — Sections 6, 9, 15, 18, 19
- `Architecture.md` — Sections 4, 10, 13, 17–19
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`
- `cae_collision_intelligence/composer.py`
- `services/pipeline/src/cmf_pipeline/candidates/service.py`
- current format profiles, artifact contracts, candidate generation, and PreProduction manifest code

The executor MUST also inspect the relevant current code paths named by the canon and any directly imported types/functions they depend on. If a cited path has moved, locate the current equivalent and record the mapping rather than silently substituting an unrelated implementation.

## 5. Exact scope

Scope is the gate between approved collision/hypothesis material and preproduction compilation. The gate must evaluate declared target formats against the narrative/archetype requirements and reject combinations that cannot be physically or stylistically realized under the product contract.

The mandate may normalize an existing format-profile schema or add a typed feasibility result. It must preserve the Blueprint-First principle: target deliverables and their requirements are known before evidence acquisition. It must not create new creative content merely to make an incompatible format appear feasible.

The scope ends at the smallest set of runtime, schema, test, and operator-facing changes necessary to prove this question. Adjacent questions are dependencies, not extra deliverables.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the files/modules named by the cited authority and their direct tests, plus the minimum supporting schema/migration/API/UI projection required to make the decision executable. New files are permitted only when they are the smallest direct implementation or test artifact needed. The executor must not modify unrelated programs, global policy, release semantics, certification claims, or later canonical questions.

The implementation may add tests, fixtures, schemas, migrations, typed models, runtime helpers, API wiring, or UI projections only where they are directly required by the decision. New abstractions require a concrete need demonstrated by the existing architecture.

## 7. Prohibitions and collision procedure

- Do not treat every format as feasible by default.
- Do not let a model override deterministic format constraints.
- Do not redesign the rendering engine.
- Do not change target formats silently after the portfolio contract is frozen.
- Do not collapse archetype matching into an opaque score with no inspectable reasons.

If the implementation encounters a collision with an existing invariant, authority rule, schema, migration, or state machine:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved operator decision;
4. make the minimum safe correction only if this mandate clearly owns the correction;
5. otherwise record the collision and stop.

### Contrastive failure — the good-looking but wrong result

A successful-looking implementation that satisfies a superficial UI assertion, creates an object without binding it to canonical state, accepts invalid input because a model “seems confident,” or passes only happy-path tests is not completion. Such an implementation violates CAE's fail-closed and provenance principles even if the visible feature appears correct.

## 8. Required work / implementation behavior

1. Inventory existing format profiles, output targets, artifact contracts, candidate services, and composer assumptions.
2. Define explicit feasibility inputs and a structured result with pass/fail reasons.
3. Define archetype coalition constraints required by the existing product contract.
4. Enforce the gate before PreProduction manifest compilation.
5. Bind the result to the exact narrative/hypothesis and format revisions evaluated.
6. Add positive tests for feasible combinations.
7. Add negative tests for incompatible aspect ratios, missing required format capabilities, and disallowed archetype/format combinations as supported by the current contract.
8. Add integration evidence showing an invalid combination cannot produce a sealed PreProduction plan.
9. Expose the gate reason to the operator.
10. Preserve deterministic behavior and record evidence.

The executor must follow test-first or integration-first sequencing appropriate to the surface: establish the contract and negative cases, implement the smallest viable change, then verify the full path. For stateful behavior, test persistence and restart/reload behavior where relevant. For digest/version behavior, test mutation and mismatch cases. For UI behavior, verify that the UI is a projection of authoritative runtime data and does not invent local semantics.

## 9. Verification and evidence standard

Evidence must prove the gate is real and upstream: schema/contract evidence for format and archetype constraints; positive executable feasibility tests; negative executable incompatibility tests; integration test proving the PreProduction compiler refuses an invalid combination; revision binding evidence; and UI projection evidence.

False-proof countercase: a test that calls the feasibility calculator while the production compiler ignores its result. That does not establish FR-ARCH-001.
Human validation is required for the semantic quality of an archetype coalition rule; automated verification can prove the declared rule is enforced.

Verification MUST include:
- a positive acceptance path;
- a negative/fail-closed path;
- a regression test for an adjacent existing behavior;
- an evidence locator identifying the exact test/file/receipt/schema that proves each material claim;
- a statement of what remains unproven.

Do not mark a requirement `VERIFIED` merely because a unit test passes if the canonical property is integration-level. If the property crosses runtime/API/database/UI boundaries, include an integration test. If the property depends on actual runtime behavior, include executable runtime evidence.

## 10. Completion and stop condition

Stop after the gate is enforced at the PreProduction admission boundary and evidence proves incompatible combinations cannot advance. If the repository lacks a sufficiently authoritative format/archetype contract to evaluate a case, record the missing source as an operator decision rather than inventing a new creative policy.

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

Use a reversible rule/schema change. Do not mutate existing campaign contracts in place. If an already-frozen portfolio becomes invalid under newly enforced rules, surface it as blocked/revision-required rather than silently rewriting it.

Rollback must preserve existing authoritative state and avoid destructive mutation. Prefer reverting the bounded implementation commit or using the repository's existing migration/revision mechanism. If a migration is introduced, it must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project's migration conventions.

## 12. Operator decision

Approve or reject whether the implementation demonstrably prevents incompatible format/archetype plans from entering PreProduction.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> Execute `CA-M005` only. Read the protocol, Master Canon Q05, `UI.md`, `Architecture.md`, the causal operating model, current composer/candidate services, format profiles, and artifact contracts. Implement `FR-ARCH-001`: format feasibility and archetype coalition constraints must pass before PreProduction manifest compilation. Do not redesign rendering or invent new creative policy. Make the gate deterministic, revision-aware, inspectable, and authoritative at runtime. Add positive and negative tests and an integration test proving invalid combinations cannot yield a sealed PreProduction plan. The UI may display the result but may not decide it. If a required format/archetype rule is not actually specified by authoritative project sources, stop and record the missing decision rather than guessing. Report exact evidence, limitations, changed files, tests, commit SHA, and request Operator approval or rejection. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
