# CAE Mandate 003 — Subject Constitution Exception Lifecycle

**Mandate ID:** `CA-M003`  
**Wave:** `01`  
**Canonical question:** `Q03`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 03 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 01, covering Questions 01–08. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer.

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

Implement the governed Subject Constitution lifecycle so the baseline is elicitation-derived, becomes immutable once signed, and can change only through a versioned operator amendment packet when voice drift or forbidden-boundary conditions require intervention.

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
Canonical invariant: `INV-SUB-001`. The canon identifies `cae_collision_intelligence/domain.py` and `docs/cae/CAE_Product_Brief/03_Subject_Baseline.md` as primary precheck surfaces.

The executor must treat the canon as the ratified requirement and the current repository as the implementation reality. Where the canon's zero-waste precheck identifies a missing capability, do not reinterpret that gap as permission to weaken the requirement.

## 4. Mandatory reading before action

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q03
- `UI.md` — Section 11
- `Architecture.md` — Sections 12, 20–22, and 31
- `docs/cae/CAE_Product_Brief/05_CAE_Causal_Operating_Model.md`
- `docs/cae/CAE_Product_Brief/03_Subject_Baseline.md`
- `cae_collision_intelligence/domain.py`
- current Subject Constitution/voice/baseline models, storage, API, and tests

The executor MUST also inspect the relevant current code paths named by the canon and any directly imported types/functions they depend on. If a cited path has moved, locate the current equivalent and record the mapping rather than silently substituting an unrelated implementation.

## 5. Exact scope

The scope is the Subject Constitution aggregate and its exception/amendment lifecycle. The mandate may implement the signed baseline, revision identity, amendment packet, exception detection boundary, and operator approval path needed to make immutability real. It does not authorize redesign of interview capture, Voice DNA algorithms, or all subject intelligence.

A baseline may be formed from approved source/interview evidence, but once signed it is a governed historical revision. A later observation can trigger an exception; it cannot silently rewrite the signed baseline. The amendment path must preserve parent lineage and identify the operator decision that authorized the new revision.

The normal UI must expose current constitution, source evidence, validation state, exceptions, and revision, while runtime remains authoritative.

The scope ends at the smallest set of runtime, schema, test, and operator-facing changes necessary to prove this question. Adjacent questions are dependencies, not extra deliverables.

## 6. Allowed artifacts and file boundary

The allowed change surface is limited to the files/modules named by the cited authority and their direct tests, plus the minimum supporting schema/migration/API/UI projection required to make the decision executable. New files are permitted only when they are the smallest direct implementation or test artifact needed. The executor must not modify unrelated programs, global policy, release semantics, certification claims, or later canonical questions.

The implementation may add tests, fixtures, schemas, migrations, typed models, runtime helpers, API wiring, or UI projections only where they are directly required by the decision. New abstractions require a concrete need demonstrated by the existing architecture.

## 7. Prohibitions and collision procedure

- Do not permit direct field mutation on a signed Subject Constitution.
- Do not let an LLM response become a new canonical subject identity without the required lifecycle.
- Do not auto-promote a voice-drift observation into a permanent amendment.
- Do not erase prior constitutions or overwrite history.
- Do not solve unrelated interview or evidence-capture deficiencies under this mandate.

If the implementation encounters a collision with an existing invariant, authority rule, schema, migration, or state machine:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved operator decision;
4. make the minimum safe correction only if this mandate clearly owns the correction;
5. otherwise record the collision and stop.

### Contrastive failure — the good-looking but wrong result

A successful-looking implementation that satisfies a superficial UI assertion, creates an object without binding it to canonical state, accepts invalid input because a model “seems confident,” or passes only happy-path tests is not completion. Such an implementation violates CAE's fail-closed and provenance principles even if the visible feature appears correct.

## 8. Required work / implementation behavior

1. Inventory current Subject Constitution/baseline data structures and mutation paths.
2. Define signed baseline state and immutable revision identity.
3. Define the minimal amendment packet carrying parent revision, proposed change, evidence/reason, operator identity, and resulting revision.
4. Enforce mutation rules at the authoritative persistence/runtime boundary.
5. Add exception representation for voice drift and forbidden-boundary triggers without making the detector itself the authority.
6. Implement the governed operator decision path required to approve an amendment.
7. Add positive tests for signing and reading a baseline and for creating a valid amendment revision.
8. Add negative tests for direct mutation, stale-parent amendment, missing operator authority, and amendment without required evidence.
9. Verify UI projection uses authoritative revision/exception data.
10. Run focused and integration tests and record exact evidence.

The executor must follow test-first or integration-first sequencing appropriate to the surface: establish the contract and negative cases, implement the smallest viable change, then verify the full path. For stateful behavior, test persistence and restart/reload behavior where relevant. For digest/version behavior, test mutation and mismatch cases. For UI behavior, verify that the UI is a projection of authoritative runtime data and does not invent local semantics.

## 9. Verification and evidence standard

Required evidence must prove lifecycle semantics, not merely model structure: executable proof that a signed baseline cannot be mutated in place; proof that a valid amendment creates a new revision with parent lineage; negative proof for stale-parent and unauthorized amendment; evidence that an exception can exist without automatically changing the baseline; integration proof that operator authorization is required; and UI projection evidence.

False-proof countercase: a test that copies the baseline object and changes the copy while never attempting persistence. That does not prove runtime immutability.
Human/operator validation is required for the semantic adequacy of an amendment; automated tests can prove lifecycle and authority mechanics but cannot decide whether the new Subject Constitution is substantively faithful.

Verification MUST include:
- a positive acceptance path;
- a negative/fail-closed path;
- a regression test for an adjacent existing behavior;
- an evidence locator identifying the exact test/file/receipt/schema that proves each material claim;
- a statement of what remains unproven.

Do not mark a requirement `VERIFIED` merely because a unit test passes if the canonical property is integration-level. If the property crosses runtime/API/database/UI boundaries, include an integration test. If the property depends on actual runtime behavior, include executable runtime evidence.

## 10. Completion and stop condition

Stop once signed-baseline immutability, exception creation, and versioned operator amendment are evidenced. If the existing Subject model is too entangled with interview capture to separate safely, record the dependency and stop rather than rewriting the interview subsystem.

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

Use revisioned records or the repository's existing aggregate versioning. Never delete historical constitutions. If an incorrect amendment path is introduced, revert the bounded implementation and preserve source evidence.

Rollback must preserve existing authoritative state and avoid destructive mutation. Prefer reverting the bounded implementation commit or using the repository's existing migration/revision mechanism. If a migration is introduced, it must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project's migration conventions.

## 12. Operator decision

Approve or reject whether the Subject Constitution now has a defensible immutable-signed baseline and governed amendment lifecycle, with evidence that operator authority—not model output—controls promotion.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> Execute `CA-M003` only. Read the Mandate Authoring Protocol, Master Canon Q03, `UI.md` Section 11, `Architecture.md`, the causal operating model, the Subject Baseline product brief, and current Subject Constitution code. Implement `INV-SUB-001`: a Subject Constitution is elicitation-derived, becomes immutable once signed, and can change only through a versioned operator amendment packet when a governed exception requires it. Do not rewrite the interview system or invent a new identity model. Establish signed revision lineage, exception representation, authorized amendment, and fail-closed rejection of direct or stale mutation. Test both happy and adversarial paths. Make the UI a projection of runtime truth. Distinguish automated lifecycle evidence from human semantic judgment. Stop if safe separation is impossible within scope. Report changed files, tests, evidence locators, limitations, commit SHA, and request explicit Operator approval or rejection. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
