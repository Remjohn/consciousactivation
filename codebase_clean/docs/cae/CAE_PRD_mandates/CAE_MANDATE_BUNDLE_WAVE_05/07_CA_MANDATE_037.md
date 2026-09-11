# CAE Mandate 037 — Real Agent Invocation Host Runner

**Mandate ID:** `CA-M037`  
**Wave:** `05`  
**Canonical question:** `Q37`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 37 (Spine Q04) of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially INV-RUN-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly agent invocation surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q37):** Live Host Runner binds compiled `AgentInvocation` directly to the model reasoning engine without mocks; enforces bounded multi-turn tool loops (max 5) and `SideEffectClass` restrictions. Real agent execution is bounded to max 5 turns with strict side-effect class verification (`INV-RUN-001`).

**Objective of this mandate:** Replace mock loops and unbounded agent calls with a live Host Runner that executes real model invocations under a hard 5-turn bound and SideEffectClass restrictions, so that production agents cannot run open-ended or unauthorized side-effecting tool loops.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 37.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-RUN-001`.
- Physical surface: `packages/ca_runtime/src/ca_runtime/agent_invocation.py`.
- Inherited real workflow dispatch (Q35) and context projection (Q36).
- `Architecture.md` agent and tool sections.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q37 and the corresponding invariant entry in full.
3. Inspect the current agent invocation host / loop logic in `agent_invocation.py`.
4. Locate mock loops, unbounded turn counts, or missing SideEffectClass checks.
5. Confirm how SideEffectClass is (or should be) declared for tools.
6. Do not implement multi-provider routing or output self-repair under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Live Host Runner that binds AgentInvocation to the real model reasoning engine (no mocks on production path).
- Hard bound of max 5 turns for multi-turn tool loops.
- Enforcement of SideEffectClass restrictions on tools.
- Positive and negative executable tests at the real agent-invocation boundary.
- Minimal changes required to wire the runner into the post-dispatch path.

**Out of scope**

- Multi-provider routing and token-cap removal (Q38).
- Greedy JSON extraction and 1-turn self-repair (Q39).
- Full human gate milestone suspension (later wave).
- Redesign of the overall tool registry.

**Dependencies**

- Real workflow dispatch and context projection from Q35–Q36.
- Existing AgentInvocation and tool declaration structures.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `packages/ca_runtime/src/ca_runtime/agent_invocation.py`
- Related tests for turn bounds and SideEffectClass enforcement
- Minimal type definitions for SideEffectClass if required

Prohibited surfaces include synthetic model adapters used on production paths, unrelated UI surfaces, and later provider/parsing logic beyond the host runner contract.

## 7. Prohibitions and collision procedure

- Do not leave a production host path that uses mock model responses.
- Do not allow multi-turn loops to exceed 5 turns.
- Do not allow tools to execute outside their declared SideEffectClass.
- Do not implement provider failover or output schema repair under this mandate.
- If SideEffectClass metadata is missing for tools, stop and report rather than running unrestricted tools.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative agent host / invocation loop.
2. Bind the host to the real model reasoning engine for production paths.
3. Enforce a hard max of 5 turns.
4. Enforce SideEffectClass restrictions before tool execution.
5. Prefer the smallest change that makes the bounded live host enforceable.

State transition (conceptual):

```text
source state: agent loops may be mocked or unbounded and may ignore SideEffectClass
→ operation: live host; max 5 turns; SideEffectClass verification
→ target state: real agent execution bounded to 5 turns with side-effect class checks
```

Actor is the agent invocation host path. Preconditions include resolved agent, projected context, and tool declarations. Validators enforce turn count and SideEffectClass. Postcondition is that production agents cannot run open-ended or unauthorized side-effecting loops. Error route is fail-closed on bound violation or class mismatch. Recovery is correction of tool declarations or Operator decision, never silent unbounded execution.

## 9. Verification and evidence standard

Evidence must demonstrate live binding, turn bound, and SideEffectClass enforcement, not merely that a runner class exists.

Required proof classes:

- `EXECUTABLE` positive path: a live invocation completes within 5 turns under allowed SideEffectClass.
- `EXECUTABLE` negative path: exceeding 5 turns or violating SideEffectClass fails closed.
- Integration evidence at the real agent-invocation boundary.
- False-proof countercase: a test that calls a mock model three times and asserts success. That proves looping, not the live bounded contract.
- Environment fidelity: tests must exercise the repository’s real host path (mocks only if explicitly labeled non-production).

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once the live bounded Host Runner with SideEffectClass enforcement is implemented and evidenced at the authoritative invocation boundary. If tool metadata cannot be completed without work outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any change to the host loop must have a safe recovery story. Bound and class checks that are evaluative can be reverted by code; production paths must not silently reintroduce mocks after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that real agent execution is bounded to max 5 turns with strict side-effect class verification at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M037` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q37, `INV-RUN-001`, `UI.md`, `Architecture.md`, and the current agent invocation host in `agent_invocation.py` before editing. Implement the real Agent Invocation Host Runner: bind to the live model reasoning engine without mocks on production paths; enforce max 5 turns and SideEffectClass restrictions. Do not implement multi-provider routing or output self-repair. Establish positive and negative executable evidence at the real invocation boundary, including turn-bound and SideEffectClass failure cases. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M037`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
