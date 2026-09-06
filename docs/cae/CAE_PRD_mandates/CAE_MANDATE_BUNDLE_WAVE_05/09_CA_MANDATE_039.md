# CAE Mandate 039 — Deterministic Output Contract & Bounded Self-Repair

**Mandate ID:** `CA-M039`  
**Wave:** `05`  
**Canonical question:** `Q39`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 39 (Spine Q06) of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially INV-OUT-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly output parsing surfaces inside agent invocation.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q39):** Greedy regex JSON extraction paired with a bounded 1-turn repair loop feeding Pydantic validation errors back to the model before fail-closed abort. Model output parsing enforces greedy JSON extraction and 1-turn bounded schema self-repair (`INV-OUT-001`).

**Objective of this mandate:** Replace fragile non-greedy or prose-intolerant parsing with greedy JSON extraction and a single bounded repair turn that feeds validation errors back to the model, after which failure is fail-closed—so that markdown-wrapped or slightly malformed model outputs do not crash the pipeline, and unbounded repair loops cannot run.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 39.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-OUT-001`.
- Physical surface: `packages/ca_runtime/src/ca_runtime/agent_invocation.py` (output parsing region).
- Inherited live Host Runner and resilient routing (Q37–Q38).
- `Architecture.md` agent output and schema sections.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q39 and the corresponding invariant entry in full.
3. Inspect the current output parsing logic in `agent_invocation.py`.
4. Locate non-greedy parsers, missing repair loops, or unbounded repair attempts.
5. Confirm the Pydantic (or equivalent) schema validation path used for agent outputs.
6. Do not implement human gate milestones or CAS transitions under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Greedy regex (or equivalent robust) JSON extraction that tolerates markdown prose wrapping.
- Bounded 1-turn repair loop that feeds Pydantic (or equivalent) validation errors back to the model.
- Fail-closed abort after the single repair attempt fails.
- Positive and negative executable tests at the real output-parsing boundary.
- Minimal changes required to wire the parser into the host runner path.

**Out of scope**

- Human gate milestones (Q40).
- Atomic CAS state transitions (later wave).
- Full economics / spend tracking of repair turns.
- Redesign of the overall schema catalog beyond the parsing contract.

**Dependencies**

- Live Host Runner and multi-provider routing from Q37–Q38.
- Existing Pydantic (or project-equivalent) output schemas.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `packages/ca_runtime/src/ca_runtime/agent_invocation.py`
- Related schema definitions and tests for parsing and repair
- Minimal helpers for greedy extraction and error feedback

Prohibited surfaces include unrelated UI, unbounded repair loops, and later gate or CAS logic beyond the parsing contract.

## 7. Prohibitions and collision procedure

- Do not leave a parser that crashes on common markdown-wrapped JSON.
- Do not allow more than one repair turn.
- Do not silently accept invalid schema output after repair failure.
- Do not implement human gate suspension or CAS under this mandate.
- If the output schema catalog is incomplete, stop after implementing the extraction/repair structure and recording residual schema blockers, rather than accepting arbitrary free-form output.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative model-output parsing path.
2. Implement greedy JSON extraction tolerant of markdown prose wrapping.
3. Implement a bounded 1-turn repair loop that feeds validation errors back to the model.
4. Fail closed after the single repair attempt fails.
5. Prefer the smallest change that makes the deterministic output contract enforceable.

State transition (conceptual):

```text
source state: non-greedy parse may crash on markdown-wrapped JSON; no bounded repair
→ operation: greedy extract; 1-turn repair with validation errors; then fail-closed
→ target state: robust extraction + single repair; invalid output never proceeds
```

Actor is the agent invocation output-parsing path. Preconditions include a model response and an output schema. Validators enforce schema after extraction/repair. Postcondition is that only schema-valid output proceeds, and repair is strictly bounded. Error route is fail-closed after one repair. Recovery is Operator intervention or upstream prompt correction, never unbounded repair.

## 9. Verification and evidence standard

Evidence must demonstrate greedy extraction, single-turn repair, and fail-closed abort, not merely that a regex exists.

Required proof classes:

- `EXECUTABLE` positive path: markdown-wrapped valid JSON is extracted and accepted; a one-shot repair recovers a near-miss into valid schema.
- `EXECUTABLE` negative path: after one failed repair, the path fails closed and does not accept invalid output.
- Integration evidence at the real agent-invocation parsing boundary.
- False-proof countercase: a test that runs `json.loads` on a clean string. That proves basic parsing, not the greedy + bounded-repair contract.
- Environment fidelity: tests must exercise the repository’s real parsing path, including prose-wrapped fixtures.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once greedy JSON extraction and 1-turn bounded schema self-repair are implemented and evidenced at the authoritative parsing boundary. If output schemas cannot be completed without work outside scope, stop after the extraction/repair structure is proven and residual schema blockers are recorded.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any change to parsing must have a safe recovery story. Parsing logic that is purely computational can be reverted by code; production paths must not silently reintroduce crash-on-markdown behavior after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that model output parsing enforces greedy JSON extraction and 1-turn bounded schema self-repair at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M039` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q39, `INV-OUT-001`, `UI.md`, `Architecture.md`, and the current output parsing path in `agent_invocation.py` before editing. Implement the deterministic output contract: greedy JSON extraction that tolerates markdown prose wrapping, paired with a bounded 1-turn repair loop that feeds Pydantic (or equivalent) validation errors back to the model, then fail-closed abort. Do not allow more than one repair turn. Do not implement human gate milestones or CAS transitions. Establish positive and negative executable evidence at the real parsing boundary, including prose-wrapped success and post-repair failure cases. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M039`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
