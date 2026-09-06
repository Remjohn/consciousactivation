# CAE Mandate 035 — Real Workflow Dispatch (Production Agent Resolution)

**Mandate ID:** `CA-M035`  
**Wave:** `05`  
**Canonical question:** `Q35`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 35 (Spine Q02) of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially INV-DISP-002).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly workflow dispatch and agent invocation surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q35):** `ProductionAgentWorkflowDispatcher` replaces synthetic adapters, resolving real agent classes and compiled skill capsules directly from `program_manifest.yaml`. Production workflows execute via compiled manifest agent resolution; synthetic adapters are forbidden (`INV-DISP-002`).

**Objective of this mandate:** Replace any SyntheticDeterministicAdapter or equivalent production_authorized=False path with a real dispatcher that resolves agents and skill capsules from the program manifest, so that live execution cannot silently fall back to mocks.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 35.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-DISP-002`.
- Physical surfaces: `services/pipeline/src/cmf_pipeline/adapters/synthetic.py`, `packages/ca_runtime/src/ca_runtime/agent_invocation.py`, program manifests.
- Inherited two-phase dispatch (Q34) as the caller of workflow dispatch.
- `Architecture.md` workflow and agent sections.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q35 and the corresponding invariant entry in full.
3. Inspect the current synthetic adapter and any ProductionAgentWorkflowDispatcher (or equivalent) surfaces.
4. Locate hard-coded `production_authorized: False` or mock agent resolution paths.
5. Confirm how `program_manifest.yaml` declares agents and skill capsules.
6. Do not implement host runner multi-turn loops (Q37) or provider routing (Q38) under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Real workflow dispatcher that resolves agent classes and compiled skill capsules from program manifests.
- Removal or hard-blocking of synthetic adapters from production execution paths.
- Positive and negative executable tests at the real dispatch boundary.
- Minimal changes required to wire manifest resolution into the post-lease workflow trigger.

**Out of scope**

- State-local context projection (Q36).
- Bounded multi-turn host runner (Q37).
- Multi-provider routing and token-cap removal (Q38).
- Output parsing and self-repair (Q39).
- Full live end-to-end harness (later wave).

**Dependencies**

- Two-phase atomic lease dispatch (Q34) that triggers the workflow.
- Existing program manifests that declare agents.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `services/pipeline/src/cmf_pipeline/adapters/synthetic.py` (to disable/remove from production path)
- `packages/ca_runtime/src/ca_runtime/agent_invocation.py`
- Program manifest loading / resolution helpers
- Related tests for real vs synthetic dispatch

Prohibited surfaces include unrelated UI routers, full host-runner loop rewrites beyond resolution, and later provider or parsing logic.

## 7. Prohibitions and collision procedure

- Do not leave a production path that silently uses SyntheticDeterministicAdapter.
- Do not invent agent classes that are not declared in the program manifest.
- Do not implement multi-turn tool loops or provider failover under this mandate.
- Do not weaken the requirement that production execution is manifest-driven.
- If manifest agent resolution cannot be completed without a broader registry change outside scope, stop and report rather than retaining a synthetic production path.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the workflow dispatch entry that currently may use synthetic adapters.
2. Implement or complete ProductionAgentWorkflowDispatcher (or equivalent) that resolves agents and skill capsules from the program manifest.
3. Ensure the production path refuses synthetic adapters.
4. Wire the dispatcher into the post-lease trigger established by Q34 (or record residual dependency).
5. Prefer the smallest change that makes real manifest resolution enforceable.

State transition (conceptual):

```text
source state: workflow may execute via synthetic adapter with production_authorized=False
→ operation: resolve real agents/skills from program_manifest.yaml; forbid synthetic in production
→ target state: production workflows execute only via compiled manifest agent resolution
```

Actor is the workflow dispatch path. Preconditions include a valid program manifest and acquired lease. Validators enforce real agent resolution. Postcondition is that synthetic adapters cannot serve production execution. Error route is fail-closed on missing or synthetic-only resolution. Recovery is correction of the manifest or Operator decision, never silent mock fallback.

## 9. Verification and evidence standard

Evidence must demonstrate real manifest-driven resolution and synthetic exclusion, not merely that a dispatcher class exists.

Required proof classes:

- `EXECUTABLE` positive path: a program with a declared agent resolves and dispatches without synthetic adapter.
- `EXECUTABLE` negative path: a production path that would have used synthetic is blocked or fails closed.
- Integration evidence at the real dispatch boundary.
- False-proof countercase: a test that imports ProductionAgentWorkflowDispatcher and asserts the class exists. That proves naming, not production resolution.
- Environment fidelity: tests must exercise the repository’s real manifest loading path.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once real workflow dispatch via manifest agent resolution is implemented and evidenced, and synthetic adapters are excluded from production paths. If a broader agent registry redesign is required outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any change to adapters or resolution must have a safe recovery story. If synthetic adapters remain for explicit non-production test profiles, that boundary must be clear and non-bypassable from production entry points.

## 12. Operator decision

Approve or reject based on whether the evidence proves that production workflows execute via compiled manifest agent resolution and that synthetic adapters are forbidden at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M035` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q35, `INV-DISP-002`, `UI.md`, `Architecture.md`, and the current synthetic adapter and agent invocation surfaces before editing. Implement real workflow dispatch: ProductionAgentWorkflowDispatcher (or equivalent) must resolve real agent classes and compiled skill capsules from program_manifest.yaml; synthetic adapters are forbidden on production paths. Do not implement context projection, host runner multi-turn loops, provider routing, or output self-repair. Establish positive and negative executable evidence at the real dispatch boundary, including synthetic exclusion. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M035`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
