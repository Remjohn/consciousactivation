# CAE Mandate 018 — Hierarchical Context Lineage Preservation

**Mandate ID:** `CA-M018`  
**Wave:** `03`  
**Canonical question:** `Q18`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 18 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-003 and INV-CTX-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly program state and evidence fragment surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q18):** Context must preserve hierarchical lineage: Turn Context → Episode Narrative → Campaign Theme. An utterance stripped of episode context is semantically corrupted. Every evidence fragment must preserve hierarchical context references to its parent episode and campaign (`INV-CTX-001`).

**Objective of this mandate:** Make hierarchical context lineage a non-optional, structurally enforced property of every evidence fragment at the authoritative state boundary so that any fragment lacking the required parent references is rejected or reconstructed only under explicit, tested recovery rules—never silently dropped.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 18.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-CTX-001`.
- PRD-003 (Evidence Capture, Grounding & Yield Analysis).
- Physical surface cited by the Canon: `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` (context projection and hierarchical scopes).
- Inherited Wave 02 and Q17 properties (sovereign media, temporal anchoring, multi-dimensional admission). These remain hard prerequisites.
- `Architecture.md` state and evidence sections.
- `UI.md` only for Operator visibility of context lineage; UI is a projection.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q18 and the corresponding invariant entry in full.
3. Inspect the current implementation of hierarchical scopes in `program_state_runtime.py` (turn / episode / campaign).
4. Locate how evidence fragments are currently constructed, stored, and projected.
5. Identify any paths that allow an utterance or fragment to travel without parent episode or campaign references.
6. Confirm that Q17 multi-dimensional admission is either already present or explicitly recorded as a residual blocker; do not re-implement it.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Structural enforcement that every evidence fragment carries explicit hierarchical context references (at minimum: turn → episode → campaign).
- Fail-closed rejection or controlled recovery when hierarchy is missing or inconsistent.
- Preservation of lineage across persistence, reload, and projection boundaries.
- Positive and negative executable tests at the real state/runtime boundary.
- Minimal schema or type changes required to represent the hierarchy.

**Out of scope**

- Expression Moments packaging (Q19).
- Reaction Receipts or Anchor Hits (Q20–Q21).
- Yield gating or authorization policy (Q23–Q24).
- Redesign of the overall program state machine or introduction of new authority lanes.
- Broad cleanup of unrelated context projection logic.

**Dependencies**

- Multi-dimensional admission (Q17) should already gate fragments; this mandate consumes admitted fragments and ensures their context lineage.
- Wave 02 temporal and sovereignty contracts remain intact.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` (especially local context projection and hierarchical scope handling)
- Related domain or evidence fragment types in collision-intelligence packages
- Test files that exercise state persistence, projection, and hierarchy
- Minimal schema/type definitions required for hierarchical references

Prohibited surfaces include unrelated program manifests, UI-only state stores, synthetic adapters that invent context, and later-stage composition or authorization modules.

## 7. Prohibitions and collision procedure

- Do not allow an evidence fragment to be treated as canonical if it lacks parent episode or campaign references.
- Do not invent a “default campaign” or “orphan episode” silently.
- Do not flatten hierarchy into a single free-form context string.
- Do not implement Q19–Q24 behavior under this mandate.
- Do not weaken multi-dimensional admission or Wave 02 sovereignty contracts.
- If the current persistence model cannot store hierarchical references without a migration outside scope, stop and report rather than weakening the invariant.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative construction and persistence path for evidence fragments.
2. Ensure each fragment carries explicit, typed references to its parent turn (if applicable), episode, and campaign.
3. Enforce the hierarchy at write and at projection time so that a missing or inconsistent parent is detected.
4. Provide a clear fail-closed or controlled-recovery path; recovery must never invent missing semantic parents.
5. Preserve lineage across restart/reload where the property is claimed to be durable.
6. Prefer the smallest change that makes hierarchy enforceable at the real boundary.

State transition (conceptual):

```text
source state: evidence fragment with partial or missing hierarchical references
→ operation: enforce and persist Turn → Episode → Campaign lineage at state boundary
→ target state: fragment either carries complete hierarchy or is rejected / recovered under explicit rule
```

Actor is the state/runtime path that constructs or projects fragments. Preconditions include existence of the parent episode and campaign identities. Validators enforce presence and consistency of references. Postcondition is a fragment that is never stripped of episode/campaign context. Error route is fail-closed rejection or explicit recovery receipt. Recovery does not invent parent meaning.

## 9. Verification and evidence standard

Evidence must demonstrate that hierarchy is preserved and enforced, not merely that three optional fields exist.

Required proof classes:

- `SCHEMA` / type evidence for hierarchical references.
- `EXECUTABLE` positive path: a fragment written with complete hierarchy is projected with the same hierarchy after persistence/reload where applicable.
- `EXECUTABLE` negative path: a fragment missing episode or campaign reference is rejected or fails the invariant check.
- Integration evidence at the real `program_state_runtime` (or equivalent) boundary.
- False-proof countercase: a test that constructs a dict with “turn/episode/campaign” keys in memory and asserts they are present. That proves shape, not durable hierarchical preservation.
- Environment fidelity: tests must exercise the repository’s real state/persistence boundary for any durability claim.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and a statement of residual unproven claims.

## 10. Completion and stop condition

Stop once hierarchical context lineage is implemented and evidenced at the authoritative state boundary. If a migration or shared-state change outside scope is required, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing acceptance tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or persistence change must have a safe downgrade/recovery story or an explicitly documented forward-only policy. Hierarchy enforcement that is purely evaluative can be reverted by code; durable references must not silently disappear after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that every evidence fragment preserves hierarchical context references to its parent episode and campaign at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M018` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q18, `INV-CTX-001`, PRD-003, `UI.md`, `Architecture.md`, and the current hierarchical context handling in `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` before editing. Implement hierarchical context lineage preservation: every evidence fragment must carry explicit Turn → Episode → Campaign references; a fragment stripped of episode or campaign context is invalid. Do not invent default parents or flatten hierarchy into free-form notes. Do not implement Expression Moments, Reaction Receipts, Anchor Hits, yield gating, or authorization policy. Preserve Q17 multi-dimensional admission and Wave 02 sovereignty contracts. Establish positive and negative executable evidence at the real state/runtime boundary, including missing-hierarchy rejection. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M018`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
