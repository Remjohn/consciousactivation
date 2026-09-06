# CAE Mandate 038 — Resilient Multi-Provider Routing

**Mandate ID:** `CA-M038`  
**Wave:** `05`  
**Canonical question:** `Q38`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 38 (Spine Q05) of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially INV-ROUT-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly model routing surfaces inside agent invocation.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q38):** Eliminated 500-token cap; implemented 3-tier resilient provider routing (Groq → OpenRouter → OpenAI) with exponential backoff and automatic failover. Reasoning engine implements 3-tier provider failover with exponential backoff (`INV-ROUT-001`).

**Objective of this mandate:** Remove any hard 500-token (or equivalent) artificial cap that blocks legitimate reasoning, and install a 3-tier resilient provider routing path with exponential backoff and automatic failover so that single-provider failure does not abort the entire agent run.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 38.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-ROUT-001`.
- Physical surface: `packages/ca_runtime/src/ca_runtime/agent_invocation.py` (routing region).
- Inherited live Host Runner (Q37) that consumes the routed model calls.
- `Architecture.md` model and resilience sections.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q38 and the corresponding invariant entry in full.
3. Inspect the current model call path in `agent_invocation.py`, including any hardcoded token caps and single-provider calls.
4. Locate the 500-token (or similar) cap and the absence of failover.
5. Confirm available provider credentials/config surfaces without inventing secrets.
6. Do not implement output parsing self-repair under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Removal of the artificial 500-token (or equivalent) hard cap that blocks legitimate reasoning.
- 3-tier resilient provider routing (Groq → OpenRouter → OpenAI, or the repository’s declared equivalent order).
- Exponential backoff and automatic failover on provider failure.
- Positive and negative executable tests at the real routing boundary (including simulated provider failure where feasible).
- Minimal configuration surfaces required for provider order and backoff parameters.

**Out of scope**

- Deterministic output contract and self-repair (Q39).
- Full economics / spend-ceiling enforcement (later wave).
- Redesign of the overall model abstraction layer beyond routing.
- Introduction of new providers not already contemplated by the Canon.

**Dependencies**

- Live Host Runner (Q37) that issues the model calls being routed.
- Existing provider client configurations.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `packages/ca_runtime/src/ca_runtime/agent_invocation.py`
- Related provider client helpers and configuration
- Tests for failover and backoff behavior
- Minimal config for provider order and backoff

Prohibited surfaces include unrelated UI, synthetic always-succeed model stubs on production paths, and later output-parsing or economics logic beyond the routing contract.

## 7. Prohibitions and collision procedure

- Do not retain a hard 500-token (or equivalent) cap that aborts legitimate reasoning.
- Do not leave a single-provider point of failure without failover.
- Do not invent provider credentials or call external services in a way that violates project security policy.
- Do not implement schema self-repair under this mandate.
- If provider clients are not available in the environment, stop after implementing the routing structure and recording residual environment blockers, rather than claiming live failover without evidence.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative model call site and any hard token cap.
2. Remove or raise the artificial hard cap so that legitimate reasoning is not blocked by a fixed 500-token limit.
3. Implement 3-tier provider routing with the Canon-declared order (or project-equivalent).
4. Add exponential backoff and automatic failover on failure.
5. Prefer the smallest change that makes resilient routing enforceable.

State transition (conceptual):

```text
source state: single provider + hard 500-token cap
→ operation: remove artificial cap; route Groq → OpenRouter → OpenAI with backoff/failover
→ target state: resilient 3-tier routing; single-provider failure does not abort the run
```

Actor is the agent invocation routing path. Preconditions include configured provider clients. Validators enforce order and failover behavior. Postcondition is that the reasoning engine survives single-provider failure. Error route is exhaustion of all tiers with explicit failure. Recovery is retry under backoff or Operator intervention, never silent single-provider lock-in.

## 9. Verification and evidence standard

Evidence must demonstrate cap removal and multi-tier failover, not merely that three provider names appear in a list.

Required proof classes:

- `EXECUTABLE` positive path: a call succeeds via the primary provider (or a subsequent tier when primary is simulated failed).
- `EXECUTABLE` negative path: when all tiers fail, the run fails closed with clear exhaustion signal.
- Evidence that the artificial hard token cap no longer aborts legitimate requests.
- Integration evidence at the real routing boundary.
- False-proof countercase: a test that sets provider="groq" and asserts a string. That proves naming, not failover.
- Environment fidelity: where live providers are unavailable, tests must still prove the routing decision structure and simulated failover.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once resilient 3-tier routing with exponential backoff is implemented and evidenced, and the artificial hard token cap is removed, at the authoritative routing boundary. If live provider credentials are unavailable, stop after the structure is proven and residual environment blockers are recorded.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any change to routing must have a safe recovery story. Routing logic that is purely computational can be reverted by code; production paths must not silently reintroduce a single-provider hard dependency after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that the reasoning engine implements 3-tier provider failover with exponential backoff and no longer aborts on an artificial 500-token hard cap at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M038` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q38, `INV-ROUT-001`, `UI.md`, `Architecture.md`, and the current model call path in `agent_invocation.py` before editing. Implement resilient multi-provider routing: remove the artificial 500-token hard cap; implement 3-tier routing (Groq → OpenRouter → OpenAI or project equivalent) with exponential backoff and automatic failover. Do not implement output schema self-repair. Establish positive and negative executable evidence at the real routing boundary, including simulated primary-provider failure and full-exhaustion cases. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M038`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
