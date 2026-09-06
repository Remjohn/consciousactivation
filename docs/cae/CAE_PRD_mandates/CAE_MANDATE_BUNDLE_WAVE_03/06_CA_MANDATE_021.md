# CAE Mandate 021 — Anchor Hits as Exact Coordinate References

**Mandate ID:** `CA-M021`  
**Wave:** `03`  
**Canonical question:** `Q21`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 21 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-003 and FR-ANCH-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly evidence retrieval and coordinate surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q21):** An Anchor Hit is an exact spatio-temporal coordinate reference in the source media, not an interpretive summary or conclusion. Anchor hits specify exact stream byte offsets and frame numbers (`FR-ANCH-001`).

**Objective of this mandate:** Establish Anchor Hits as precise, non-interpretive coordinate references so that any “anchor” that is merely a paraphrase, summary, or approximate time range is rejected as non-compliant.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 21.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `FR-ANCH-001`.
- PRD-003 (Evidence Capture, Grounding & Yield Analysis).
- Physical surface cited by the Canon: `cae_collision_intelligence/domain.py`.
- Inherited Wave 02 temporal anchoring and sovereign media contracts (required for exact byte/frame coordinates).
- Q17–Q20 properties as consumers or producers of coordinate-bound evidence.
- `Architecture.md` evidence and retrieval sections.
- `UI.md` only for Operator visibility; UI is a projection.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q21 and the corresponding FR entry in full.
3. Inspect the current domain model for anchors or coordinate references in `cae_collision_intelligence/domain.py` and related retrieval paths.
4. Locate any approximate time ranges, free-form “anchor” strings, or interpretive summaries currently treated as anchors.
5. Confirm that sovereign media and temporal coordinates are available so that exact byte offsets and frame numbers can be expressed; do not invent a parallel coordinate system.
6. Confirm Reaction Receipt linkage (Q20) is compatible or record residual dependency.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Definition of Anchor Hit as an exact coordinate reference (stream byte offsets, frame numbers, and any additional exact temporal fields required by the media model).
- Enforcement that an Anchor Hit is not an interpretive summary or approximate range.
- Positive and negative executable tests at the real domain/retrieval boundary.
- Minimal schema/type changes required to represent exact coordinates.

**Out of scope**

- Full media indexing or search infrastructure beyond the coordinate representation.
- Yield gating and authorization policy (Q23–Q24).
- Redesign of the overall media storage format.
- Implementation of composition algorithms that consume anchors.

**Dependencies**

- Wave 02 temporal anchoring and sovereign media byte supremacy are hard prerequisites.
- Reaction Receipts (Q20) may share coordinate vocabulary; keep them consistent but do not re-implement reaction logic.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `cae_collision_intelligence/domain.py`
- Related retrieval or evidence types
- Test files that exercise exact coordinate construction and validation
- Minimal schema/type definitions required for Anchor Hits

Prohibited surfaces include unrelated program manifests, UI-only state, synthetic coordinate generators that invent byte offsets, and later composition or authorization modules beyond the minimum coordinate contract.

## 7. Prohibitions and collision procedure

- Do not accept approximate time ranges or free-form textual “anchors” as Anchor Hits.
- Do not invent byte offsets or frame numbers that are not derived from the sovereign media container.
- Do not implement yield gating or authorization policy under this mandate.
- Do not weaken sovereign media or temporal anchoring contracts.
- If exact coordinate representation cannot be achieved without a migration outside scope, stop and report rather than weakening the invariant.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Define the Anchor Hit structure with required exact coordinate fields (byte offsets, frame numbers, and any additional exact fields mandated by the media model).
2. Enforce that an object claiming to be an Anchor Hit carries those exact fields and is not merely an interpretive summary.
3. Integrate validation so that approximate or interpretive forms are rejected at the domain boundary.
4. Prefer the smallest change that makes exactness enforceable at the real domain/retrieval boundary.

State transition (conceptual):

```text
source state: optional approximate or interpretive “anchor” representations
→ operation: require exact stream byte offsets and frame numbers
→ target state: only exact coordinate Anchor Hits are admitted
```

Actor is the domain / evidence retrieval path. Preconditions include valid sovereign media coordinates. Validators enforce exact field presence and consistency. Postcondition is that anchors are coordinates, not conclusions. Error route is fail-closed rejection of approximate or interpretive forms. Recovery is re-derivation from media, never invention of coordinates.

## 9. Verification and evidence standard

Evidence must demonstrate exact coordinate representation, not merely that an “anchor” type exists.

Required proof classes:

- `SCHEMA` / type evidence for exact coordinate fields.
- `EXECUTABLE` positive path: an Anchor Hit with valid byte offsets and frame numbers is accepted.
- `EXECUTABLE` negative path: an approximate range or interpretive summary is rejected as a non-compliant Anchor Hit.
- Integration evidence at the real domain boundary.
- False-proof countercase: a test that stores a start/end second pair and labels it “anchor.” That proves approximate timing, not exact byte/frame coordinates.
- Environment fidelity: tests must exercise real coordinate validation against the repository’s media model where the claim is made.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once Anchor Hits are exact coordinate references and evidenced at the authoritative domain boundary. If a broader media subsystem change is required outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or persistence change must have a safe recovery story. Coordinate enforcement that is evaluative can be reverted by code; durable Anchor Hits must not silently lose exactness after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that Anchor Hits specify exact stream byte offsets and frame numbers (and are not interpretive summaries) at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M021` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q21, `FR-ANCH-001`, PRD-003, `UI.md`, `Architecture.md`, and the current domain model in `cae_collision_intelligence/domain.py` before editing. Implement Anchor Hits as exact spatio-temporal coordinate references: they must specify exact stream byte offsets and frame numbers and must not be interpretive summaries or approximate ranges. Do not invent coordinates. Do not implement yield gating or authorization policy. Preserve Wave 02 temporal anchoring and sovereign media contracts, and Q17–Q20 properties. Establish positive and negative executable evidence at the real domain boundary, including approximate/interpretive rejection. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M021`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
