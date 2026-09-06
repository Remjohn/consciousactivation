# CAE Mandate 023 — Deterministic Portfolio Yield Gating

**Mandate ID:** `CA-M023`  
**Wave:** `03`  
**Canonical question:** `Q23`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 23 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-003 and INV-YIELD-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly yield evaluation and pipeline gating surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q23):** Yield gating is a deterministic sufficiency check against the Content Portfolio contract. Insufficient evidence yield halts the pipeline before costly video rendering. If evidence yield fails deliverable portfolio requirements, execution halts fail-closed (`INV-YIELD-001`).

**Objective of this mandate:** Install a deterministic, fail-closed yield gate that compares acquired evidence against the frozen Content Portfolio contract and aborts downstream costly stages when sufficiency is not met.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 23.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-YIELD-001`.
- PRD-003 (Evidence Capture, Grounding & Yield Analysis).
- Physical surface cited by the Canon: `cae_collision_intelligence/verifier.py` (yield/sufficiency region).
- Inherited Content Portfolio Contract (earlier wave) and pre-production snapshot freeze.
- Q17–Q22 properties that produce the evidence and session yield being measured.
- `Architecture.md` pipeline and cost-control sections.
- `UI.md` only for Operator visibility of yield status; UI is a projection.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q23 and the corresponding invariant entry in full.
3. Inspect the current yield/sufficiency evaluation in the verifier and any pipeline gate before rendering/assembly.
4. Locate the frozen Content Portfolio Contract representation and how deliverable requirements are expressed.
5. Confirm that costly downstream stages (e.g., video rendering) are identifiable so the gate can be placed before them.
6. Do not re-implement portfolio freezing, multi-dimensional admission, or adaptive elicitation under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Deterministic comparison of acquired evidence yield against the frozen Content Portfolio contract requirements.
- Fail-closed halt of the pipeline when yield is insufficient, before costly rendering or equivalent stages.
- Positive and negative executable tests at the real verifier/pipeline gate boundary.
- Minimal schema/type or state changes required to represent yield evaluation results and the gate decision.

**Out of scope**

- Authorization policy modes (Q24).
- Implementation of the rendering pipeline itself.
- Redesign of the overall portfolio schema.
- Soft “warning only” modes that allow insufficient yield to proceed without explicit Operator override under a separate policy.

**Dependencies**

- Frozen Content Portfolio Contract and sealed pre-production snapshot from earlier waves.
- Evidence admission and elicitation resilience (Q17–Q22) that produce the yield being measured.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `cae_collision_intelligence/verifier.py` (yield/sufficiency region)
- Pipeline application surfaces that gate progression to costly stages
- Test files that exercise sufficient and insufficient yield cases
- Minimal schema/type definitions required for yield results and gate decisions

Prohibited surfaces include unrelated program manifests, UI-only state, synthetic yield scores that bypass the portfolio contract, and later authorization or release modules beyond the minimum gate required by this mandate.

## 7. Prohibitions and collision procedure

- Do not allow insufficient yield to proceed into costly rendering without an explicit, separately authorized override path (which is out of scope for this mandate).
- Do not replace the deterministic portfolio check with a heuristic confidence score.
- Do not implement authorization policy modes under this mandate.
- Do not invent portfolio requirements that contradict the frozen contract.
- If the portfolio contract is not available as a machine-readable input, stop and report rather than inventing soft requirements.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative yield evaluation and pipeline progression gate.
2. Implement a deterministic sufficiency check against the frozen Content Portfolio contract.
3. Place the gate before costly downstream stages so that insufficient yield aborts before those stages execute.
4. Emit an auditable yield result and gate decision.
5. Prefer the smallest change that makes the fail-closed gate enforceable at the real boundary.

State transition (conceptual):

```text
source state: pipeline may proceed to costly stages without deterministic portfolio yield check
→ operation: evaluate yield against frozen Content Portfolio contract; gate progression
→ target state: insufficient yield → fail-closed halt; sufficient yield → progression allowed
```

Actor is the verifier / pipeline gate path. Preconditions include a frozen portfolio contract and acquired evidence records. Validators enforce deterministic sufficiency. Postcondition is that costly stages cannot run on insufficient yield. Error route is fail-closed halt with explicit yield deficit. Recovery is additional evidence acquisition or explicit Operator action under a separate policy, never silent progression.

## 9. Verification and evidence standard

Evidence must demonstrate deterministic portfolio-based gating, not merely that a “yield score” exists.

Required proof classes:

- `EXECUTABLE` positive path: sufficient yield allows progression past the gate.
- `EXECUTABLE` negative path: insufficient yield halts before costly stages.
- Evidence that the comparison is against the frozen portfolio contract, not a free-form heuristic.
- Integration evidence at the real verifier/pipeline boundary.
- False-proof countercase: a test that asserts a float yield > 0.7 and continues. That proves a threshold, not portfolio-contract sufficiency.
- Environment fidelity: tests must exercise the repository’s real gate path and, where claimed, the blocking of costly stages.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once deterministic portfolio yield gating is implemented and evidenced at the authoritative gate boundary. If the portfolio contract or costly-stage boundary cannot be addressed without work outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or state change must have a safe recovery story. Gate logic that is purely evaluative can be reverted by code; durable yield decisions must not silently rewrite history after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that insufficient evidence yield against the Content Portfolio contract halts execution fail-closed before costly stages at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M023` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q23, `INV-YIELD-001`, PRD-003, `UI.md`, `Architecture.md`, and the current yield/sufficiency path in `cae_collision_intelligence/verifier.py` (and related pipeline gates) before editing. Implement deterministic portfolio yield gating: compare acquired evidence against the frozen Content Portfolio contract and halt fail-closed before costly rendering when yield is insufficient. Do not replace the check with a soft heuristic score. Do not implement authorization policy modes. Preserve the frozen portfolio/pre-production contracts and Q17–Q22 evidence properties. Establish positive and negative executable evidence at the real gate boundary, including progression-on-sufficient and halt-on-insufficient cases. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M023`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
