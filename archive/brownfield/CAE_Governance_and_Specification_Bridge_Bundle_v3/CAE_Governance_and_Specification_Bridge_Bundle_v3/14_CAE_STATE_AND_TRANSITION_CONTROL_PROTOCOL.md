# CAE State & Transition Control Protocol v1.0

**Status:** Mandatory cross-cutting CAE protocol
**Scope:** All stateful CAE runtime procedures, from World/Context intelligence through semantic compilation, media realization, validation, and outcome learning.

## 1. Purpose

CAE requires durable state because the system is not a sequence of independent prompts. Audience state, Guest state, Context state, activation state, primitive activation, coalition state, execution state, validation state, and outcome state evolve over time.

The governing rule is:

> **PostgreSQL/Supabase is the authoritative operational state store.**

The agent must never be required to reconstruct authoritative current state from prose history alone.

The state-control layer therefore separates:

```text
STATE STORE
    PostgreSQL / Supabase

STATE MODEL
    Canonical CAE ontology + schemas + temporal rules

STATE CONTROL
    Typed semantic operations + transition contracts + validators

STATE HISTORY
    Immutable events + receipts + evidence

PROCEDURAL MEMORY
    Versioned Skills.md / runbooks / practices
```

## 2. What CAE borrows from StateM

StateM demonstrates a useful control principle: a long-running agent is more reliable when meaningful phases are explicit context-and-contract boundaries, transitions are checked, failures are recoverable, and procedural lessons persist outside the model context. Its public repository describes explicit phase boundaries, executable transition gates, dynamic checks, durable runtime history, and context lifecycle support. The paper likewise describes states as context-and-contract boundaries and separates state runtime from reusable runbook/control profiles.

CAE adopts these principles conceptually and, where useful, selectively at implementation level.

CAE does **not** adopt the StateM local runtime state directory as the authoritative CAE database. StateM's local runbook/runtime representation is a reference implementation, not the CAE ontology or storage model.

Reference:
- Paper: https://arxiv.org/abs/2608.15089
- Repository: https://github.com/henryqin1997/statem

## 3. State as a context-and-contract boundary

A CAE state represents a meaningful phase or condition of an entity, relationship, semantic field, run, or artifact.

A state has two simultaneous roles:

### 3.1 Context boundary

Entering a state refreshes the information and procedural instructions relevant to that state.

Examples:

- `AUDIENCE_SIGNAL_DETECTION`
- `GUEST_AUDIENCE_MATCHING`
- `PROVOCATION_READY`
- `AUTHENTICATION_PENDING`
- `AUTHENTICATED_EVIDENCE`
- `COALITION_FORMATION`
- `EDGE_VALIDATION`
- `SEMANTIC_PROGRAM_READY`
- `REALITY_CONTACT_PENDING`

### 3.2 Contract boundary

A state defines what must be true before transition is permitted.

The state itself does not prove completion. The transition contract determines whether the required evidence and validators have been satisfied.

## 4. State authority rule

Agents MUST NOT directly mutate authoritative state through ad-hoc database writes when a typed semantic operation exists.

Preferred:

```text
request_transition(...)
activate_tension(...)
record_authenticated_evidence(...)
form_coalition(...)
submit_validation(...)
commit_semantic_program(...)
```

Not preferred:

```sql
UPDATE state SET status = 'verified' ...
```

Raw SQL may remain available to infrastructure code, migrations, administrative tooling, and controlled repair procedures, but normal agent execution must use authorized operations.

## 5. Transition contract

Every consequential state transition must be modeled as:

```yaml
transition_id:
source_state:
target_state:
actor_role:
preconditions: []
required_evidence: []
required_validators: []
authorized_operations: []
postconditions: []
receipt_type:
failure_routes: []
```

The canonical transition procedure is:

```text
1. Resolve current authoritative state.
2. Validate that the requested transition is legal.
3. Resolve required evidence.
4. Execute applicable deterministic validators.
5. Execute semantic/human review where explicitly required.
6. Persist required pre-transition evidence.
7. Commit state change transactionally where practical.
8. Emit immutable transition event.
9. Emit receipt.
10. Initialize target-state context.
```

If a blocking condition fails, the source state remains authoritative.

## 6. No self-declared completion

Agent statements such as:

> “The evidence is sufficient.”

or:

> “The phase is complete.”

are not independent proof.

They may be recorded as structured attestations, but promotion requires the evidence mechanism specified by the transition contract.

## 7. Repair semantics

Failed transitions MUST route to an explicit outcome class:

- `REPAIR_REQUIRED`
- `BLOCKED_EXTERNAL_DEPENDENCY`
- `EVIDENCE_INSUFFICIENT`
- `VALIDATION_FAILED`
- `CONTRACT_CONFLICT`
- `QUARANTINED`

Retry policy must be error-aware. Deterministic failures must not be blindly retried.

## 8. Context refresh

State entry may trigger a compact state-local context packet containing:

- current phase;
- active state;
- unresolved obligations;
- relevant evidence references;
- relevant entities and relations;
- applicable procedures;
- authorized operations;
- pending validators;
- previous failure summaries;
- next legal transitions.

This is a control surface, not a replacement for the full canonical data model.

## 9. Dynamic checks

CAE may support state-local dynamic checks discovered during execution.

Such checks:

- belong to the current run or state entry unless explicitly promoted;
- cannot weaken canonical invariants;
- must carry provenance and author;
- must be auditable;
- require explicit promotion before becoming reusable procedural memory.

This follows the useful distinction in StateM between run-local dynamic checks and shared versioned runbooks.

## 10. Stop / handoff rule

A run must not be treated as complete merely because the agent stops producing output.

Terminal completion requires a terminal-state contract or an explicit blocked state with recorded reason.

Therefore:

```text
STOP
≠
COMPLETE
```

## 11. Brownfield integration rule

Before creating new state infrastructure, the coding agent MUST inspect existing:

- Supabase tables;
- receipt chain;
- memory tiers;
- pipelines;
- agents;
- state-like models;
- event tables;
- service orchestration;
- scheduled monitors;
- circuit breakers.

Where equivalent infrastructure exists, CAE extends it rather than creating a parallel state system.

## 12. Relationship to CAE constitutional doctrine

This protocol must preserve:

- human-first evidence acquisition;
- Matrix of Edging as pressure-selection architecture;
- SDA semantic direction and geometry;
- primitive coalition eligibility and routeability;
- SFL perceptual modulation without overriding semantic direction;
- anti-centroid enforcement;
- environment-fidelity requirements;
- reward-hacking resistance;
- immutable evidence and receipt lineage.

State control is therefore an execution-governance layer, not a censorship layer.

## 13. Fatal violations

A state-control implementation is invalid if it:

- stores authoritative CAE state only in local files;
- silently overwrites historical state;
- permits direct agent mutation of canonical state outside authorized operations;
- treats self-attestation as independent proof;
- allows transition without required evidence;
- weakens Matrix of Edging or anti-centroid requirements under the guise of safety;
- creates a parallel state model that conflicts with the canonical ontology without a migration decision.
