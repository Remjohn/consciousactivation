# CAE Mandate 036 — Real State-Local Context Projection

**Mandate ID:** `CA-M036`  
**Wave:** `05`  
**Canonical question:** `Q36`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 36 (Spine Q03) of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially INV-CTX-002).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly program state projection surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q36):** Input-scoped context projection prunes state strictly to declared inputs for the active node, masks fields by authority lane, and asserts committed `state_hash` parity. Node execution receives strictly pruned, lane-masked context snapshots bound to `state_hash` (`INV-CTX-002`).

**Objective of this mandate:** Replace any full-aggregate context dump with a pruned, lane-masked, hash-bound projection so that agents and nodes never receive unauthorized or stale state.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 36.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-CTX-002`.
- Physical surface: `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` (context projection region).
- Inherited authority lanes (COMMANDER, HUNTER, ANALYST, COMPOSER) and hierarchical context from earlier waves.
- `Architecture.md` state and authority sections.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q36 and the corresponding invariant entry in full.
3. Inspect the current `get_local_context()` or equivalent projection in `program_state_runtime.py`.
4. Locate any path that returns the entire aggregate dictionary without pruning or lane masking.
5. Confirm how authority lanes and declared node inputs are currently represented.
6. Do not implement host runner loops or provider routing under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Input-scoped pruning of context to declared inputs for the active node.
- Authority-lane masking of fields.
- Assertion of committed `state_hash` parity on the projected snapshot.
- Positive and negative executable tests at the real state-projection boundary.
- Minimal schema/type changes required for projection metadata if needed.

**Out of scope**

- Live agent host runner multi-turn loops (Q37).
- Multi-provider routing (Q38).
- Output parsing and self-repair (Q39).
- Full hierarchical context redesign (already addressed in earlier waves).

**Dependencies**

- Existing aggregate state and state_hash computation.
- Authority lane definitions.
- Real workflow dispatch (Q35) that supplies the active node identity.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
- Related tests for context projection, pruning, and lane masking
- Minimal type definitions for projected context snapshots

Prohibited surfaces include unrelated agent invocation loops, synthetic full-state dumps used in production, and later CAS transition logic beyond the hash parity check required here.

## 7. Prohibitions and collision procedure

- Do not return the entire aggregate to a node that declared only a subset of inputs.
- Do not omit lane masking for fields that are authority-restricted.
- Do not skip state_hash parity assertion when the projection claims to be bound to committed state.
- Do not implement multi-turn tool loops under this mandate.
- If lane metadata or declared inputs are missing for a node, stop and report rather than projecting full state as a workaround.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative local-context projection path.
2. Implement pruning to declared inputs for the active node.
3. Apply authority-lane masking.
4. Assert committed state_hash parity on the resulting snapshot.
5. Prefer the smallest change that makes pruned, masked, hash-bound projection enforceable.

State transition (conceptual):

```text
source state: get_local_context may expose entire aggregate without pruning or masking
→ operation: prune to declared inputs; mask by authority lane; bind to state_hash
→ target state: node receives strictly pruned, lane-masked, hash-bound snapshot
```

Actor is the program state runtime projection path. Preconditions include active node identity, declared inputs, and authority lane. Validators enforce pruning, masking, and hash parity. Postcondition is that unauthorized or stale full state is never delivered. Error route is fail-closed projection failure. Recovery is correction of node declarations or state, never silent full dump.

## 9. Verification and evidence standard

Evidence must demonstrate pruning, masking, and hash binding, not merely that a context dict is returned.

Required proof classes:

- `EXECUTABLE` positive path: a node with restricted inputs receives only those fields, correctly masked, with matching state_hash.
- `EXECUTABLE` negative path: a request that would have exposed unauthorized fields or mismatched hash fails closed.
- Integration evidence at the real state-runtime boundary.
- False-proof countercase: a test that returns a subset of keys without lane or hash checks. That proves filtering, not the full INV-CTX-002 contract.
- Environment fidelity: tests must exercise the repository’s real state projection path.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once pruned, lane-masked, hash-bound context projection is implemented and evidenced at the authoritative state boundary. If authority-lane metadata cannot be completed without work outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any change to projection logic must have a safe recovery story. Projection that is purely computational can be reverted by code; durable claims about hash-bound snapshots must not silently become unbound after restart.

## 12. Operator decision

Approve or reject based on whether the evidence proves that node execution receives strictly pruned, lane-masked context snapshots bound to state_hash at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M036` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q36, `INV-CTX-002`, `UI.md`, `Architecture.md`, and the current context projection path in `program_state_runtime.py` before editing. Implement real state-local context projection: prune to declared inputs for the active node, mask fields by authority lane, and assert committed state_hash parity. Do not return the entire aggregate. Do not implement host runner loops, provider routing, or output self-repair. Establish positive and negative executable evidence at the real state boundary, including unauthorized-field and hash-mismatch rejection. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M036`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
