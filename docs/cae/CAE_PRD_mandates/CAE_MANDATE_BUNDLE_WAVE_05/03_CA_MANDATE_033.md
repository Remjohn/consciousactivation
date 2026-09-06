# CAE Mandate 033 — Canonical Functional Requirements Test Contract

**Mandate ID:** `CA-M033`  
**Wave:** `05`  
**Canonical question:** `Q33`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 33 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially FR-PRD-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths only insofar as they are referenced by acceptance tests; the normative contract itself lives in FUNCTIONAL_REQUIREMENTS.md and associated test harnesses.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q33):** `FUNCTIONAL_REQUIREMENTS.md` is the normative test contract where every FR-xxx is stage-mapped, atomic, acceptance-testable, and tracked through SPECIFIED → IMPLEMENTED → VERIFIED. Requirements without automated negative and positive acceptance tests cannot claim VERIFIED status (`FR-PRD-001`).

**Objective of this mandate:** Establish and enforce the SPECIFIED → IMPLEMENTED → VERIFIED lifecycle for functional requirements so that no FR may be marked VERIFIED without both positive and negative automated acceptance tests that exercise the real system boundary.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 33.
- `FUNCTIONAL_REQUIREMENTS.md` itself as the normative contract.
- `docs/PRD/CURRENT.md` and related PRD index materials.
- Program manifests that already declare evaluators and gates (e.g., editorial storyboard program).
- `Architecture.md` verification and traceability sections.
- CAE-BMAD method insistence on reality-contact verification.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q33 and the corresponding FR entry in full.
3. Inspect the current `FUNCTIONAL_REQUIREMENTS.md` (or equivalent) and any existing status tracking (SPECIFIED/IMPLEMENTED/VERIFIED).
4. Locate any FR that is already marked VERIFIED without positive and negative automated tests.
5. Inspect how program manifests and test suites currently reference FR identifiers.
6. Do not re-implement individual FR bodies under this mandate; only the lifecycle and verification gate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Explicit lifecycle states SPECIFIED → IMPLEMENTED → VERIFIED for each FR.
- Rule that VERIFIED may be claimed only when automated positive and negative acceptance tests exist and pass against the real boundary.
- Minimal tooling or metadata (status fields, validators, or scripts) required to enforce the rule.
- Positive and negative executable tests that demonstrate the lifecycle gate itself.
- Documentation of residual FRs that remain SPECIFIED or IMPLEMENTED only.

**Out of scope**

- Writing the full body of every remaining FR.
- Implementing the runtime behavior of individual FRs (that is the job of their own mandates).
- Redesign of the overall PRD modular structure.
- CI policy changes beyond the minimum required to surface the lifecycle gate.

**Dependencies**

- Existing FUNCTIONAL_REQUIREMENTS.md and PRD index.
- Existing test harnesses that can host acceptance tests.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `docs/cae/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md` (or the repository’s canonical location)
- Related status tracking, validators, or scripts (e.g., validate_constitution.py style)
- Test files that assert the lifecycle rule
- Minimal metadata or schema for FR status

Prohibited surfaces include unrelated product code, UI-only status badges treated as authority, and synthetic “VERIFIED” stamps without tests.

## 7. Prohibitions and collision procedure

- Do not mark any FR as VERIFIED without both positive and negative automated acceptance tests.
- Do not invent a parallel status vocabulary that bypasses SPECIFIED → IMPLEMENTED → VERIFIED.
- Do not implement the runtime behavior of other FRs under the cover of this mandate.
- Do not weaken the requirement that tests must exercise the real system boundary (unit-only tests that never touch the integration path are insufficient for VERIFIED).
- If the current FR set cannot be fully instrumented without work outside scope, stop after establishing the gate and recording residual status, rather than stamping VERIFIED prematurely.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Confirm or introduce explicit status tracking for FRs (SPECIFIED / IMPLEMENTED / VERIFIED).
2. Implement a gate or validator that refuses VERIFIED status when positive or negative automated acceptance tests are missing or failing.
3. Demonstrate the gate with at least one FR that correctly transitions and one that is blocked from false VERIFIED claims.
4. Prefer the smallest change that makes the lifecycle enforceable.

State transition (conceptual):

```text
source state: FR may be labeled complete without automated positive+negative tests
→ operation: require SPECIFIED → IMPLEMENTED → VERIFIED; block VERIFIED without tests
→ target state: only FRs with passing positive and negative acceptance tests may claim VERIFIED
```

Actor is the FR status / validation path. Preconditions include presence of the FR identifier and test locators. Validators enforce both positive and negative tests. Postcondition is that VERIFIED is never a documentation-only claim. Error route is refusal to mark VERIFIED. Recovery is addition of the missing tests, never silent promotion.

## 9. Verification and evidence standard

Evidence must demonstrate the lifecycle gate, not merely that a status field exists.

Required proof classes:

- `DOCUMENT` / schema evidence for the lifecycle states.
- `EXECUTABLE` positive path: an FR with both positive and negative tests can reach VERIFIED.
- `EXECUTABLE` negative path: an FR lacking one of the test classes cannot be marked VERIFIED.
- Integration evidence that the gate runs against real test discovery or execution.
- False-proof countercase: a test that sets status = "VERIFIED" in a markdown table. That proves labeling, not the automated test contract.
- Environment fidelity: the gate must be runnable in the repository’s actual test environment.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once the SPECIFIED → IMPLEMENTED → VERIFIED lifecycle is enforced and evidenced, and no FR can claim VERIFIED without the required automated tests. If full instrumentation of every FR is outside scope, stop after the gate is proven and residual statuses are recorded.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any metadata or script change must have a safe recovery story. Status fields that are purely documentary can be reverted; the gate itself must not leave the repository in a state where false VERIFIED claims are easier than before.

## 12. Operator decision

Approve or reject based on whether the evidence proves that requirements without automated negative and positive acceptance tests cannot claim VERIFIED status at the canonical contract boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M033` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q33, `FR-PRD-001`, `FUNCTIONAL_REQUIREMENTS.md`, `docs/PRD/CURRENT.md`, `UI.md`, `Architecture.md`, and any existing FR status tracking or validators before editing. Implement the canonical FR test contract: every FR is tracked SPECIFIED → IMPLEMENTED → VERIFIED, and VERIFIED may be claimed only when automated positive and negative acceptance tests exist and pass against the real boundary. Do not implement the runtime bodies of other FRs. Do not stamp VERIFIED without tests. Establish positive and negative executable evidence for the lifecycle gate itself. Preserve existing compatible behavior and use the canonical documentation/test boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M033`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
