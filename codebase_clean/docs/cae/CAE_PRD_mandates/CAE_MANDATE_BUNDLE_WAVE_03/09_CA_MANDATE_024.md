# CAE Mandate 024 — Configurable Campaign Authorization Policy

**Mandate ID:** `CA-M024`  
**Wave:** `03`  
**Canonical question:** `Q24`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 24 of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 03, covering Questions 17–24. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially PRD-005 and FR-AUTH-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly policy configuration and gate surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q24):** Authorization policy is a configurable campaign parameter governing agent delegation autonomy, while constitutional invariants remain non-waivable. Operators configure delegation policies (YOLO / Checkpoint / Strict / Custom); constitutional security invariants cannot be disabled (`FR-AUTH-001`).

**Objective of this mandate:** Expose a configurable campaign-level authorization policy surface for delegation modes while hard-enforcing that constitutional security invariants remain non-waivable under every mode.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 24.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `FR-AUTH-001`.
- PRD-005 (Multi-Agent Runtime, Security & Certification) and Product Brief Stage 12 (Human Authorization).
- Physical surfaces cited by the Canon: `docs/cae/CAE_Product_Brief/12_Human_Authorization.md`, `apps/web/src/api/types.ts`, and related runtime policy evaluation paths.
- Inherited constitutional invariants from earlier waves (sovereign media, multi-dimensional admission, yield gating, tenant fencing, etc.) that must remain non-waivable.
- `Architecture.md` authority and gate sections.
- `UI.md` for Operator configuration of policy modes; UI is a projection of policy, not the authority source.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q24 and the corresponding FR entry in full.
3. Inspect the current authorization policy representation in API types, product brief, and runtime evaluation paths.
4. Locate any hard-coded single mode or any path that allows constitutional invariants to be disabled.
5. Confirm which invariants are already treated as constitutional and must remain non-waivable.
6. Do not implement durable authorization decision receipts (later question) or full gate milestone machinery under this mandate; only the configurable policy surface and non-waivability of constitutional invariants.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Campaign-level configurable delegation policy modes: at minimum YOLO, Checkpoint, Strict, and a Custom extension point if already present in types.
- Enforcement that constitutional security invariants cannot be disabled under any mode.
- Positive and negative executable tests at the real policy evaluation boundary.
- Minimal schema/type or state changes required to represent the selected policy mode and the non-waivable invariant set.

**Out of scope**

- Durable signed Authorization Decision Receipts (Q25).
- Full declarative policy rule packages and prospective revision binding (Q26–Q27).
- Implementation of the full human gate milestone suspension/resume machinery.
- Redesign of authority lanes or introduction of new constitutional invariants beyond those already ratified.

**Dependencies**

- Existing constitutional invariants from Waves 01–03 that must remain non-waivable.
- Existing API type surfaces that already mention policy modes (Canon precheck).

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `apps/web/src/api/types.ts` and related API/runtime policy evaluation code
- Product brief / configuration surfaces that declare policy modes
- Test files that exercise mode selection and non-waivability of constitutional invariants
- Minimal schema/type definitions required for policy mode and invariant enforcement

Prohibited surfaces include unrelated program manifests, UI-only local storage treated as authority, synthetic policy flags that disable constitutional checks, and later receipt or gate modules beyond the minimum policy surface required by this mandate.

## 7. Prohibitions and collision procedure

- Do not allow any policy mode to disable or bypass constitutional security invariants.
- Do not invent new constitutional invariants under this mandate; only protect those already ratified.
- Do not implement durable authorization receipts or full gate suspension machinery under this mandate.
- Do not treat UI selection alone as runtime authority without a corresponding runtime policy evaluation path.
- If the non-waivable invariant set cannot be expressed without broader work outside scope, stop and report rather than leaving a mode that can silently disable them.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative campaign policy configuration and evaluation path.
2. Ensure the declared modes (YOLO, Checkpoint, Strict, Custom as applicable) are representable and selectable at the campaign level.
3. Implement evaluation logic such that constitutional security invariants remain enforced under every mode.
4. Provide clear fail-closed behavior if a mode attempts to waive a non-waivable invariant.
5. Prefer the smallest change that makes configurability and non-waivability enforceable at the real boundary.

State transition (conceptual):

```text
source state: authorization behavior may be hard-coded or may allow invariant waiver
→ operation: expose configurable campaign policy modes; enforce non-waivable constitutional invariants under all modes
→ target state: Operators can select YOLO/Checkpoint/Strict/Custom; no mode disables constitutional security invariants
```

Actor is the policy configuration and evaluation path. Preconditions include a declared set of constitutional invariants. Validators enforce mode validity and non-waivability. Postcondition is that delegation autonomy is configurable while constitutional security remains intact. Error route is fail-closed rejection of any attempt to waive a non-waivable invariant. Recovery is correction of the policy selection, never silent waiver.

## 9. Verification and evidence standard

Evidence must demonstrate both configurability and non-waivability, not merely that a mode enum exists.

Required proof classes:

- `SCHEMA` / type evidence for policy modes.
- `EXECUTABLE` positive path: each declared mode can be selected and is honored for delegation behavior within its intended autonomy envelope.
- `EXECUTABLE` negative path: any attempt to disable or bypass a constitutional security invariant is rejected regardless of mode.
- Integration evidence at the real policy evaluation boundary.
- False-proof countercase: a test that sets `policy = "YOLO"` and asserts a string field. That proves naming, not non-waivability of constitutional invariants.
- Environment fidelity: tests must exercise the repository’s real policy evaluation path.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once configurable campaign authorization policy modes are implemented and evidenced, and constitutional security invariants are proven non-waivable under every mode, at the authoritative evaluation boundary. If the non-waivable set or mode evaluation cannot be completed without work outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or state change must have a safe recovery story. Policy evaluation logic that is purely computational can be reverted by code; durable campaign policy selections must not silently rewrite history after restart, and constitutional enforcement must not silently disappear.

## 12. Operator decision

Approve or reject based on whether the evidence proves that Operators can configure delegation policies (YOLO/Checkpoint/Strict/Custom) while constitutional security invariants remain non-waivable at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M024` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q24, `FR-AUTH-001`, PRD-005, Product Brief Stage 12, `UI.md`, `Architecture.md`, and the current policy types/evaluation surfaces (including `apps/web/src/api/types.ts` and related runtime paths) before editing. Implement configurable campaign authorization policy: Operators may select YOLO, Checkpoint, Strict, or Custom delegation modes, but constitutional security invariants must remain non-waivable under every mode. Do not implement durable authorization receipts or full gate suspension machinery. Do not allow any mode to disable constitutional invariants. Preserve earlier constitutional properties from Waves 01–03. Establish positive and negative executable evidence at the real policy evaluation boundary, including mode selection and invariant non-waivability cases. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M024`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
