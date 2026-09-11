# CAE Mandate 032 — Governed Memory Write-Back Promotion

**Mandate ID:** `CA-M032`  
**Wave:** `05`  
**Canonical question:** `Q32`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 32 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially Stage 17 and INV-MEM-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly memory promotion and learning-candidate surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q32):** Raw outcomes cannot directly overwrite canonical memory. Insights become Learning Candidates that must satisfy explicit evidence, attribution, and confidence thresholds. Memory promotion requires verified attribution proof; raw observations cannot overwrite durable models (`INV-MEM-001`).

**Objective of this mandate:** Install a governed promotion path in which only Learning Candidates that pass explicit evidence, attribution, and confidence thresholds may update durable memory, and any attempt by raw observations to overwrite canonical models is rejected fail-closed.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 32.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-MEM-001`.
- Product Brief Stage 17 (`docs/cae/CAE_Product_Brief/17_Memory_Writeback.md`).
- Inherited outcome measurement and release-manifest attribution from earlier waves.
- `Architecture.md` memory and learning sections.
- `UI.md` only for Operator visibility of promotion candidates; UI is a projection.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q32 and the corresponding invariant entry in full.
3. Inspect the current memory write-back or learning-candidate surfaces (if any) and the Product Brief Stage 17 text.
4. Locate any path that allows raw outcome telemetry or un-attributed observations to mutate durable models.
5. Confirm that outcome measurement and release-manifest hashes from earlier waves are available as attribution inputs, or record residual blockers.
6. Do not re-implement outcome measurement or release sealing under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Definition of Learning Candidate as an intermediate object carrying evidence, attribution, and confidence fields.
- Enforcement that durable memory updates occur only via promoted Learning Candidates that satisfy explicit thresholds.
- Fail-closed rejection of raw observation overwrite of canonical models.
- Positive and negative executable tests at the real memory-promotion boundary.
- Minimal schema/type changes required to represent Learning Candidates and promotion decisions.

**Out of scope**

- Full post-training flywheel or preference-pair generation (later spine questions).
- Redesign of the overall memory store topology.
- Implementation of the entire outcome measurement pipeline.
- Authorization policy changes or gate milestone machinery.

**Dependencies**

- Causal outcome attribution and release-manifest hashes from earlier waves as sources of attribution proof.
- Existing distinction between ephemeral observations and durable models.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- Memory / learning-candidate modules referenced by Stage 17 Product Brief
- Related state or domain types that currently hold durable models
- Test files that exercise promotion and rejection of raw overwrite
- Minimal schema/type definitions required for Learning Candidates

Prohibited surfaces include unrelated program manifests, UI-only state, synthetic memory writers that bypass attribution, and later telemetry or fine-tuning pipelines beyond the minimum promotion gate.

## 7. Prohibitions and collision procedure

- Do not allow raw outcome records to mutate durable models directly.
- Do not invent confidence thresholds that contradict the Canon’s requirement for explicit evidence and attribution.
- Do not implement the full post-training corpus generation under this mandate.
- Do not weaken release-manifest or outcome-attribution contracts inherited from earlier waves.
- If attribution proof cannot be obtained without work outside scope, stop and report rather than promoting on incomplete evidence.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative path that currently (or should) update durable memory.
2. Introduce Learning Candidate as the only promotion vehicle, requiring evidence, attribution, and confidence fields.
3. Enforce that raw observations are never written directly into durable model state.
4. Emit an auditable promotion or rejection receipt.
5. Prefer the smallest change that makes governed promotion enforceable at the real boundary.

State transition (conceptual):

```text
source state: raw outcomes or un-attributed observations may overwrite durable memory
→ operation: require Learning Candidate with evidence + attribution + confidence; promote only on pass
→ target state: durable memory updates only via verified promotion; raw overwrite rejected fail-closed
```

Actor is the memory write-back / promotion path. Preconditions include presence of attribution proof and threshold configuration. Validators enforce evidence, attribution, and confidence. Postcondition is that durable models cannot be silently overwritten by raw observations. Error route is fail-closed rejection with explicit reason. Recovery is construction of a proper Learning Candidate, never silent promotion.

## 9. Verification and evidence standard

Evidence must demonstrate governed promotion and rejection of raw overwrite, not merely that a “candidate” type exists.

Required proof classes:

- `SCHEMA` / type evidence for Learning Candidate.
- `EXECUTABLE` positive path: a fully attributed candidate that meets thresholds is promoted.
- `EXECUTABLE` negative path: a raw observation or under-attributed candidate is rejected.
- Integration evidence at the real memory-promotion boundary.
- False-proof countercase: a test that inserts a dict labeled “LearningCandidate” and asserts a write succeeded. That proves naming, not attribution-gated promotion.
- Environment fidelity: tests must exercise the repository’s real durable-memory boundary where the claim is made.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once governed memory promotion is implemented and evidenced at the authoritative write-back boundary. If attribution inputs or durable store contracts cannot be satisfied without work outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or persistence change must have a safe recovery story. Promotion logic that is purely evaluative can be reverted by code; durable promotions must not silently reverse after restart without an explicit compensating action.

## 12. Operator decision

Approve or reject based on whether the evidence proves that memory promotion requires verified attribution proof and that raw observations cannot overwrite durable models at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M032` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q32, `INV-MEM-001`, Product Brief Stage 17, `UI.md`, `Architecture.md`, and the current memory write-back surfaces before editing. Implement governed memory promotion: raw outcomes cannot overwrite durable models; insights become Learning Candidates that must satisfy explicit evidence, attribution, and confidence thresholds before promotion. Do not implement the full post-training flywheel. Do not weaken earlier outcome-attribution or release-manifest contracts. Establish positive and negative executable evidence at the real promotion boundary, including raw-overwrite rejection. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M032`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
