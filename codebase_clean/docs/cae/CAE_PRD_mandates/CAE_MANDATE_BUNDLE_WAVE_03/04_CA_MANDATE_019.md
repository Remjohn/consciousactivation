# CAE Mandate 019 — Expression Moments as Semantic Composition Bridge

**Mandate ID:** `CA-M019`  
**Wave:** `03`  
**Canonical question:** `Q19`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 19 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-003 / PRD-004 and FR-EXPR-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly composition and evidence packaging surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q19):** Expression Moments represent the bridge between raw evidentiary utterances and creative composition, packaging emotion, theme, and spoken truth into narrative building blocks. Composition engines must consume Expression Moments rather than navigating raw unparsed audio or transcript tokens (`FR-EXPR-001`).

**Objective of this mandate:** Establish Expression Moments as the exclusive, structured, evidence-anchored intermediate representation that composition may consume, so that any path that feeds raw tokens or unanchored prose into composition is rejected or redirected.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 19.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `FR-EXPR-001`.
- PRD-003 and PRD-004 (Evidence Capture / Editorial Composition).
- Physical surface cited by the Canon: `cae_collision_intelligence/composer.py`.
- Inherited Q17–Q18 and Wave 02 properties (multi-dimensional admission, hierarchical context, sovereign media, temporal anchoring, verbatim integrity).
- `Architecture.md` composition and evidence sections.
- `UI.md` only for Operator visibility of Expression Moment status; UI is a projection.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q19 and the corresponding FR entry in full.
3. Inspect the current composition path in `cae_collision_intelligence/composer.py` and any related packaging logic.
4. Locate where raw turns, transcripts, or unparsed tokens currently flow into composition.
5. Confirm that admitted evidence already carries hierarchical context and multi-dimensional admission results (or record residual blockers).
6. Do not re-implement admission or hierarchy under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Definition of Expression Moment as a structured, evidence-anchored package (emotion, theme, spoken truth, lineage references).
- Enforcement that composition engines consume Expression Moments, not raw unparsed audio or transcript tokens.
- Construction of Expression Moments only from already-admitted, context-preserving evidence.
- Positive and negative executable tests at the real composition boundary.
- Minimal schema/type changes required to represent Expression Moments.

**Out of scope**

- Reaction Receipts and Anchor Hits as first-class attachments (Q20–Q21); this mandate may leave extension points but must not implement their full contracts.
- Yield gating against portfolio contracts (Q23).
- Authorization policy (Q24).
- Full creative composition algorithms or rendering pipelines.
- Redesign of the overall evidence DAG topology.

**Dependencies**

- Q17 multi-dimensional admission and Q18 hierarchical context must already gate the inputs that become Expression Moments.
- Wave 02 sovereignty and temporal contracts remain intact.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `cae_collision_intelligence/composer.py`
- Related domain types for Expression Moments
- Test files that exercise packaging and composition consumption
- Minimal schema/type definitions required for Expression Moments

Prohibited surfaces include unrelated program manifests, UI-only state, synthetic composition adapters that invent content, and later authorization or release modules.

## 7. Prohibitions and collision procedure

- Do not allow composition to consume raw transcript tokens or unparsed audio as a primary input once Expression Moments are the declared bridge.
- Do not invent emotional or thematic content that is not anchored to admitted evidence.
- Do not implement full Reaction Receipt or Anchor Hit contracts under this mandate.
- Do not implement yield gating or authorization policy.
- Do not weaken multi-dimensional admission or hierarchical context contracts.
- If the composition surface cannot be safely redirected without broader changes outside scope, stop and report rather than weakening the invariant.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Define the Expression Moment structure with required evidence anchors and hierarchical lineage.
2. Implement construction of Expression Moments only from admitted, context-preserving fragments.
3. Redirect or gate the composition entry point so that it requires Expression Moments.
4. Reject or fail-closed any path that attempts to feed raw tokens as the primary composition input.
5. Prefer the smallest change that establishes the bridge at the real composition boundary.

State transition (conceptual):

```text
source state: admitted evidence fragments + existing composition path that may accept raw tokens
→ operation: package into Expression Moments; gate composition on Expression Moments
→ target state: composition consumes only Expression Moments; raw-token primary path is blocked
```

Actor is the packaging/composition path. Preconditions include prior admission and hierarchy. Validators enforce presence of anchors and lineage. Postcondition is that composition cannot legitimately invent upstream meaning from raw tokens. Error route is fail-closed rejection of unanchored input. Recovery is re-packaging from valid admitted evidence.

## 9. Verification and evidence standard

Evidence must demonstrate that composition is gated on Expression Moments, not merely that a new type exists.

Required proof classes:

- `SCHEMA` / type evidence for Expression Moment.
- `EXECUTABLE` positive path: composition succeeds when supplied with valid Expression Moments derived from admitted evidence.
- `EXECUTABLE` negative path: composition fails closed when supplied only with raw tokens or unanchored prose.
- Integration evidence at the real composer boundary.
- False-proof countercase: a test that constructs an object named “ExpressionMoment” in memory and asserts a field exists. That proves naming, not the consumption gate.
- Environment fidelity: tests must exercise the repository’s real composition entry path.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once Expression Moments are the enforced composition bridge and evidenced at the authoritative composer boundary. If a broader refactor is required outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or packaging change must have a safe recovery story. Composition gating that is evaluative can be reverted by code; durable Expression Moment records must not silently lose their evidence anchors after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that composition engines consume Expression Moments rather than navigating raw unparsed audio or transcript tokens at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M019` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q19, `FR-EXPR-001`, PRD-003/PRD-004, `UI.md`, `Architecture.md`, and the current composition path in `cae_collision_intelligence/composer.py` before editing. Implement Expression Moments as the exclusive semantic composition bridge: composition must consume structured, evidence-anchored Expression Moments rather than raw unparsed audio or transcript tokens. Do not invent emotional or thematic content without evidence anchors. Do not fully implement Reaction Receipts, Anchor Hits, yield gating, or authorization policy. Preserve Q17 admission, Q18 hierarchy, and Wave 02 sovereignty contracts. Establish positive and negative executable evidence at the real composer boundary, including raw-token rejection. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M019`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
