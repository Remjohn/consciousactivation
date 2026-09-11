# CAE Mandate 017 — Multi-Dimensional Evidence Admission Predicate

**Mandate ID:** `CA-M017`  
**Wave:** `03`  
**Canonical question:** `Q17`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 17 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-003 and FR-EVID-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly the evidence admission and verifier surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q17):** Evidence admission cannot rely on a single scalar confidence score. It must satisfy a multi-dimensional boolean predicate covering at least fidelity, epistemic legality, identity fit, and domain fit. Admission requires unanimous pass across all declared evidentiary gate dimensions (`FR-EVID-001`).

**Objective of this mandate:** Make the multi-dimensional admission predicate an enforceable, fail-closed runtime contract at the authoritative evidence boundary so that any evidence fragment that fails any declared dimension is rejected before it can enter canonicalization, composition, or yield evaluation.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 17.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `FR-EVID-001`.
- PRD-003 (Evidence Capture, Grounding & Yield Analysis).
- Physical surfaces cited by the Canon: `cae_collision_intelligence/domain.py`, `cae_collision_intelligence/verifier.py`.
- Inherited Wave 02 evidence sovereignty properties (sovereign media, temporal anchoring, verbatim integrity). These remain hard prerequisites and must not be weakened.
- `Architecture.md` evidence and provenance sections.
- `UI.md` only insofar as Operator visibility of admission decisions is required; UI is a projection, never an authority source.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q17 and the corresponding FR entry in full.
3. Inspect the current implementations of `cae_collision_intelligence/domain.py` and `cae_collision_intelligence/verifier.py`.
4. Locate any existing scalar confidence scores, admission helpers, or soft gates that currently allow single-dimension passage.
5. Inspect how admitted evidence is later consumed by canonicalization and composition paths so that the new predicate is applied at the correct authority boundary.
6. Confirm that Wave 02 sovereign-media and temporal-anchoring contracts are already present or explicitly blocked; do not re-implement them.

Document the current state (what already exists, what is missing, what is contradictory) before proposing changes.

## 5. Exact scope

**In scope**

- Definition and enforcement of a multi-dimensional boolean admission predicate with at least the four dimensions: fidelity, epistemic legality, identity fit, domain fit.
- Unanimous-pass rule: any single failed dimension causes fail-closed rejection.
- Persistence or receipt of the per-dimension evaluation result so that later stages can audit why a fragment was admitted or rejected.
- Positive and negative executable tests at the real verifier/domain boundary.
- Minimal schema or type changes required to represent the multi-dimensional result.

**Out of scope**

- Expression Moments, Reaction Receipts, Anchor Hits (later Wave 03 mandates).
- Yield gating against portfolio contracts (Q23).
- Authorization policy modes (Q24).
- Composition engines, release manifests, or downstream creative surfaces.
- Redesign of the overall evidence graph topology or introduction of new authority lanes.

**Dependencies**

- Wave 02 sovereign source media and temporal anchoring must already be enforceable or explicitly recorded as residual blockers.
- Existing distinction between guest-stated evidence and inferred observations (Canon precheck) must be respected.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `cae_collision_intelligence/domain.py`
- `cae_collision_intelligence/verifier.py`
- Related test files under the collision-intelligence or pipeline test suites
- Minimal schema/type definitions required for the multi-dimensional result
- Evidence receipt or state-transition surfaces that already record admission decisions, if they exist

Prohibited surfaces include any unrelated program manifests, UI-only state, synthetic adapters used to bypass real verification, and any later-stage composition or authorization modules.

## 7. Prohibitions and collision procedure

- Do not replace the multi-dimensional predicate with a weighted score, average, or “mostly true” heuristic.
- Do not allow any dimension to be optional or silently defaulted to true.
- Do not invent new dimensions beyond those required by the Canon without Operator authorization.
- Do not weaken sovereign-media or temporal-anchoring contracts inherited from Wave 02.
- Do not implement Q18–Q24 behavior under the cover of this mandate.
- If a required upstream property (e.g., temporal coordinates) is absent, stop and report the collision rather than inventing a workaround that bypasses the dimension.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction. Do not invent a local resolution.

## 8. Required work / implementation behavior

1. Establish the authoritative admission entry point in the verifier/domain layer.
2. Define a structured multi-dimensional result (schema or typed object) that records each dimension’s boolean outcome and an overall admission decision.
3. Implement the unanimous-pass rule so that the overall decision is true only when every declared dimension is true.
4. Ensure that rejected fragments cannot proceed into any path that treats them as admitted evidence.
5. Persist or emit a receipt that makes the per-dimension evaluation auditable.
6. Preserve any existing compatible distinction between stated evidence and inferred observations.
7. Prefer the smallest change that makes the predicate enforceable at the real boundary; avoid broad refactors.

State transition (conceptual):

```text
source state: evidence fragment with optional scalar confidence or incomplete gates
→ operation: evaluate multi-dimensional predicate at verifier boundary
→ target state: fragment either admitted with per-dimension receipt or rejected fail-closed
```

Actor is the verifier/admission path. Preconditions include presence of the dimensions’ required inputs. Validators enforce unanimous pass. Postcondition is an auditable admission or rejection decision. Error route is fail-closed rejection with explicit dimension failure reason. Recovery is re-evaluation after upstream correction, never silent promotion.

## 9. Verification and evidence standard

Evidence must demonstrate that admission is multi-dimensional and unanimous, not merely that four boolean fields exist.

Required proof classes:

- `SCHEMA` / type evidence for the multi-dimensional result.
- `EXECUTABLE` positive path: a fragment that passes all dimensions is admitted.
- `EXECUTABLE` negative paths: a fragment that fails any single dimension is rejected.
- Integration evidence that the rejection is observed at the real verifier boundary, not only in a pure unit test that constructs the result in memory.
- False-proof countercase: a test that asserts four keys exist and a float confidence > 0.8. That proves shape, not the unanimous multi-dimensional contract.
- Environment fidelity: tests must exercise the repository’s real domain/verifier path.

Verification MUST include:

- a positive acceptance path;
- at least one negative/fail-closed path per dimension (or a parameterized equivalent);
- a regression test for an adjacent existing behavior (e.g., stated vs inferred distinction);
- exact evidence locators (file, test name, assertion);
- a statement of what remains unproven.

Do not mark `FR-EVID-001` as VERIFIED solely because a unit test passes if the property is integration-level.

## 10. Completion and stop condition

Stop once the multi-dimensional unanimous admission predicate is implemented and evidenced at the authoritative verifier/domain boundary. If the existing model cannot safely represent per-dimension receipts without a migration or shared-state change outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires:

1. the requested artifact/behavior exists;
2. the declared acceptance tests pass;
3. negative paths fail closed as required;
4. no prohibited surface was changed;
5. limitations and residual blockers are recorded;
6. the exact commit SHA is captured;
7. the control-state record or equivalent implementation tracker is updated if one exists;
8. the Operator decision is explicitly requested.

## 11. Rollback / recovery

Any schema or persistence change must have a safe downgrade/recovery story or an explicitly documented forward-only policy approved by the project’s migration conventions. If the change is purely in-memory evaluation logic with no schema impact, recovery is ordinary code revert. Rejected fragments must remain rejected after restart; the admission decision must not silently flip on reload.

## 12. Operator decision

Approve or reject the implementation based on whether the evidence proves that evidence admission is multi-dimensional, unanimous, and fail-closed at the canonical runtime boundary.

The executor must not infer this decision from the absence of errors. The Operator must receive a concise evidence package containing: changed files, tests executed, exact evidence locators, residual limitations, commit SHA, and the explicit approval/rejection question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M017` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q17, `FR-EVID-001`, PRD-003, `UI.md`, `Architecture.md`, and the current implementations of `cae_collision_intelligence/domain.py` and `cae_collision_intelligence/verifier.py` before editing. Implement the multi-dimensional evidence admission predicate: fidelity, epistemic legality, identity fit, and domain fit must all pass unanimously or the fragment is rejected fail-closed. Do not replace the predicate with a scalar score or “mostly true” heuristic. Do not implement Expression Moments, Reaction Receipts, Anchor Hits, yield gating, or authorization policy. Preserve Wave 02 sovereign-media and temporal-anchoring contracts. Establish positive and negative executable evidence at the real verifier boundary, including per-dimension rejection cases. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M017`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
