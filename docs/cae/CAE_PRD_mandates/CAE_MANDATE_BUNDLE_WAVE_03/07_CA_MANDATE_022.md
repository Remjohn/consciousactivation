# CAE Mandate 022 — Adaptive Elicitation & Missing-Unit Resilience

**Mandate ID:** `CA-M022`  
**Wave:** `03`  
**Canonical question:** `Q22`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 22 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-002 and FR-ELIC-002).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly interview/elicitation program surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q22):** An interview session can succeed even if specific planned elicitation units are omitted, provided overall narrative yield criteria are satisfied. Interview completion is evaluated on holistic yield sufficiency, not 100% linear script execution (`FR-ELIC-002`).

**Objective of this mandate:** Replace any rigid “all planned units must execute” completion rule with a holistic yield-sufficiency evaluation so that missing units do not automatically fail the session when the overall narrative yield criteria are met, while still preventing silent under-delivery against those criteria.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 22.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `FR-ELIC-002`.
- PRD-002 (Question & Interview Intelligence).
- Physical surface cited by the Canon: `programs/interview_semantic_program/program_manifest.yaml` and related runtime evaluation paths.
- Inherited portfolio contract and pre-production snapshot properties (from earlier waves) that define the yield criteria.
- `Architecture.md` elicitation and program execution sections.
- `UI.md` only for Operator visibility of completion and missing-unit status; UI is a projection.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q22 and the corresponding FR entry in full.
3. Inspect the current interview/elicitation completion logic and any turn-by-turn acquisition tracking.
4. Locate any hard requirement that every planned elicitation unit must execute for session success.
5. Confirm how narrative yield criteria are currently expressed (or record residual blockers).
6. Do not re-implement portfolio freezing or multi-dimensional evidence admission under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Evaluation of interview completion based on holistic yield sufficiency rather than 100% linear script execution.
- Explicit handling of omitted elicitation units so that omission is visible and does not silently count as success.
- Positive and negative executable tests at the real interview/elicitation evaluation boundary.
- Minimal schema/type or program-state changes required to represent missing units and yield sufficiency.

**Out of scope**

- Deterministic portfolio yield gating against deliverable contracts (Q23); this mandate focuses on session completion resilience.
- Authorization policy modes (Q24).
- Redesign of the overall interview program topology or question sequencing algorithms.
- Implementation of full Expression Moment or Reaction Receipt pipelines.

**Dependencies**

- Earlier portfolio and pre-production contracts that define what “yield sufficiency” means for the campaign.
- Existing turn-by-turn acquisition tracking (Canon precheck) should be leveraged, not discarded.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `programs/interview_semantic_program/program_manifest.yaml` and related program runtime evaluation code
- State or evaluation helpers that decide interview completion
- Test files that exercise completion with missing units and with insufficient yield
- Minimal schema/type definitions required for missing-unit and yield-sufficiency records

Prohibited surfaces include unrelated program manifests, UI-only state, synthetic completion flags that bypass yield evaluation, and later authorization or release modules.

## 7. Prohibitions and collision procedure

- Do not treat “all units executed” as the sole or mandatory success criterion.
- Do not allow missing units to disappear from the record; omission must remain visible.
- Do not implement full portfolio yield gating (Q23) under this mandate.
- Do not implement authorization policy (Q24).
- Do not invent yield criteria that contradict the frozen portfolio or pre-production snapshot.
- If yield criteria are not yet expressible without work outside scope, stop and report rather than inventing soft success.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative interview completion evaluation path.
2. Replace or augment any pure linear-script success rule with a holistic yield-sufficiency check.
3. Ensure omitted elicitation units are recorded and visible in the completion evidence.
4. Fail closed when overall yield criteria are not met, even if some units executed.
5. Prefer the smallest change that makes adaptive resilience enforceable at the real evaluation boundary.

State transition (conceptual):

```text
source state: completion tied to 100% planned unit execution
→ operation: evaluate holistic narrative yield sufficiency; record omitted units
→ target state: session may succeed with missing units if yield criteria are met; otherwise fail-closed
```

Actor is the interview/elicitation evaluation path. Preconditions include declared yield criteria and unit acquisition records. Validators enforce sufficiency and visibility of omissions. Postcondition is that linear completeness is not required for success and under-yield is not silently accepted. Error route is fail-closed on insufficient yield. Recovery is additional elicitation or explicit Operator acceptance under policy, never silent promotion.

## 9. Verification and evidence standard

Evidence must demonstrate holistic yield evaluation and missing-unit resilience, not merely that a “success” flag can be set.

Required proof classes:

- `EXECUTABLE` positive path: a session with one or more omitted units still succeeds when yield criteria are met.
- `EXECUTABLE` negative path: a session that fails yield criteria is rejected even if some units executed.
- Evidence that omitted units remain visible in the completion record.
- Integration evidence at the real interview evaluation boundary.
- False-proof countercase: a test that marks success whenever at least one unit executed. That proves partial progress, not holistic yield sufficiency.
- Environment fidelity: tests must exercise the repository’s real program evaluation path.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once interview completion is evaluated on holistic yield sufficiency (with visible missing units) and evidenced at the authoritative evaluation boundary. If yield criteria cannot be expressed without work outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or state change must have a safe recovery story. Evaluation logic that is purely computational can be reverted by code; durable completion records must not silently rewrite history after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that interview completion is evaluated on holistic yield sufficiency rather than 100% linear script execution, with omitted units remaining visible, at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M022` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q22, `FR-ELIC-002`, PRD-002, `UI.md`, `Architecture.md`, and the current interview/elicitation completion logic (including `programs/interview_semantic_program/program_manifest.yaml` and related runtime evaluation) before editing. Implement adaptive elicitation resilience: interview completion must be evaluated on holistic narrative yield sufficiency, not 100% linear script execution; omitted units must remain visible. Do not treat “all units executed” as mandatory success. Do not implement full portfolio yield gating (Q23) or authorization policy (Q24). Preserve earlier portfolio and pre-production contracts and Wave 02/03 evidence properties. Establish positive and negative executable evidence at the real evaluation boundary, including success-with-missing-units and fail-on-insufficient-yield cases. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M022`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
