# CAE Mandate 020 — Reaction Receipts as First-Class Evidence

**Mandate ID:** `CA-M020`  
**Wave:** `03`  
**Canonical question:** `Q20`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 20 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-003 and FR-REACT-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly evidence capture and receipt surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q20):** Reaction receipts (pauses, micro-expressions, vocal pitch changes, emotional shifts) are first-class evidence that contextualize the veracity of spoken words. Reaction receipts are cryptographically linked to corresponding audio/video timecodes (`FR-REACT-001`).

**Objective of this mandate:** Elevate reaction receipts to first-class, cryptographically linked evidence objects so that they cannot be treated as optional annotations and so that any reaction without a verifiable media coordinate link is rejected.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 20.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `FR-REACT-001`.
- PRD-003 (Evidence Capture, Grounding & Yield Analysis).
- Physical surfaces cited by the Canon: `services/pipeline/src/cmf_pipeline/application.py` (evidence capture region).
- Inherited Wave 02 temporal anchoring and sovereign media contracts (required for cryptographic linkage to timecodes).
- Q17 multi-dimensional admission and Q18 hierarchical context as consumers of reaction evidence.
- `Architecture.md` evidence and provenance sections.
- `UI.md` only for Operator visibility; UI is a projection.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q20 and the corresponding FR entry in full.
3. Inspect the current evidence capture and reaction handling in the pipeline application and related domain models.
4. Locate any existing reaction metrics that are stored without media coordinate linkage.
5. Confirm that temporal anchoring (Wave 02) is available so that cryptographic linkage is possible; do not invent a parallel timing system.
6. Confirm Expression Moment packaging (Q19) leaves a clear extension point or record residual dependency.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Definition of Reaction Receipt as a first-class evidence object.
- Cryptographic or strong cryptographic-style linkage (hash / digest / coordinate binding) to corresponding audio/video timecodes.
- Enforcement that a reaction without a valid media coordinate link is not admitted as first-class evidence.
- Positive and negative executable tests at the real capture/receipt boundary.
- Minimal schema/type changes required to represent Reaction Receipts and their linkages.

**Out of scope**

- Full computer-vision or audio analysis pipelines that generate the raw reaction signals.
- Anchor Hits as coordinate references (Q21); this mandate focuses on reaction objects and their media linkage.
- Yield gating and authorization policy (Q23–Q24).
- Redesign of the overall media storage system.

**Dependencies**

- Wave 02 temporal anchoring and sovereign media byte supremacy are hard prerequisites for legitimate linkage.
- Q17 admission may later evaluate reaction-backed evidence; this mandate supplies the receipt objects.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `services/pipeline/src/cmf_pipeline/application.py` (evidence capture region)
- Related domain types for reaction receipts
- Test files that exercise capture, linkage, and admission of reactions
- Minimal schema/type definitions required for Reaction Receipts

Prohibited surfaces include unrelated program manifests, UI-only state, synthetic reaction generators that invent coordinates, and later composition or authorization modules beyond the minimum linkage required by this mandate.

## 7. Prohibitions and collision procedure

- Do not treat reactions as free-form notes or optional metadata without media linkage.
- Do not invent timecodes or byte offsets that are not derived from the sovereign media container.
- Do not implement full Anchor Hit contracts under this mandate.
- Do not implement yield gating or authorization policy.
- Do not weaken sovereign media or temporal anchoring contracts.
- If cryptographic linkage cannot be achieved without a migration outside scope, stop and report rather than weakening the invariant.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Define the Reaction Receipt structure with required media coordinate linkage fields.
2. Enforce that a Reaction Receipt is only admitted when the linkage to audio/video timecodes (or equivalent sovereign coordinates) is present and verifiable.
3. Integrate the receipt into the evidence path so that later stages can consume it as first-class evidence.
4. Prefer the smallest change that makes the first-class status and linkage enforceable at the real capture boundary.

State transition (conceptual):

```text
source state: reaction signals optionally recorded without media coordinate binding
→ operation: elevate to Reaction Receipt with cryptographic/coordinate linkage
→ target state: only linked Reaction Receipts are admitted as first-class evidence
```

Actor is the evidence capture / receipt path. Preconditions include valid temporal coordinates from sovereign media. Validators enforce linkage presence and consistency. Postcondition is that reactions contextualize spoken words only when coordinates are bound. Error route is fail-closed rejection of unlinked reactions. Recovery is re-binding from the original media, never invention of coordinates.

## 9. Verification and evidence standard

Evidence must demonstrate first-class status and media linkage, not merely that a reaction object exists.

Required proof classes:

- `SCHEMA` / type evidence for Reaction Receipt and linkage fields.
- `EXECUTABLE` positive path: a reaction with valid media coordinates is admitted as first-class evidence.
- `EXECUTABLE` negative path: a reaction without valid media coordinates is rejected.
- Integration evidence at the real pipeline/application capture boundary.
- False-proof countercase: a test that stores a reaction string and asserts a “linked” boolean is true without verifying coordinates against media. That proves labeling, not linkage.
- Environment fidelity: tests must exercise real coordinate binding against the repository’s media/temporal surfaces where the claim is made.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once Reaction Receipts are first-class, media-linked evidence objects and evidenced at the authoritative capture boundary. If a broader media subsystem change is required outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or persistence change must have a safe recovery story. Linkage enforcement that is evaluative can be reverted by code; durable receipts must not silently lose their coordinate bindings after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that reaction receipts are first-class evidence cryptographically (or equivalently strongly) linked to corresponding audio/video timecodes at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M020` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q20, `FR-REACT-001`, PRD-003, `UI.md`, `Architecture.md`, and the current evidence capture path in `services/pipeline/src/cmf_pipeline/application.py` before editing. Implement Reaction Receipts as first-class evidence: pauses, micro-expressions, pitch changes, and emotional shifts must be represented as linked objects whose media coordinates are cryptographically (or equivalently strongly) bound to sovereign audio/video timecodes. Do not invent coordinates. Do not fully implement Anchor Hits, yield gating, or authorization policy. Preserve Wave 02 temporal anchoring and sovereign media contracts, and Q17–Q19 properties. Establish positive and negative executable evidence at the real capture boundary, including unlinked-reaction rejection. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M020`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
