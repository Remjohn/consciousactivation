# CAE PostgreSQL Authoritative State Model v1.0

**Status:** Canonical implementation pattern
**Purpose:** Translate CAE state doctrine into an auditable PostgreSQL/Supabase model without collapsing ontology into SQL.

## 1. Principle

SQL is the implementation language for the relational representation. It is not the ontology.

The conceptual chain remains:

```text
Ontology → Taxonomy → Schema → Relations → State → Programs → IR → Runtime → Outcomes
```

PostgreSQL provides the durable operational representation of that model.

## 2. Storage classes

CAE should distinguish at minimum:

| Class | Examples | Storage pattern |
|---|---|---|
| Canonical | ontology, taxonomy, primitive definitions, scene definitions, contracts | versioned tables + typed columns |
| Dynamic | AudienceState, GuestState, ContextState, TensionState, PrimitiveActivation, CoalitionState, ExecutionState | temporal tables / state projections |
| Immutable Evidence | interview responses, source citations, original media, operator notes | append-only evidence tables + object storage refs |
| Derived | Edge, SpeciesHypothesis, SemanticProgram, CompositionIR | reproducible records with lineage |
| Events | state transitions, candidate generation, validator execution, outcome observations | append-only event tables |
| Receipts | transition receipts, coalition receipts, compiler receipts, render receipts, evaluation receipts | append-only receipt tables |

## 3. Recommended dynamic-state pattern

Every dynamic state record SHOULD support:

```yaml
state_id:
subject_type:
subject_id:
state_type:
status:
valid_from:
valid_to:
observed_at:
source_event_id:
confidence:
activation_level:
resolution_status:
previous_state_id:
current: boolean
version:
```

Stable fields use typed columns. Evolving structured detail may use bounded JSONB.

## 4. Current vs historical state

Do not overwrite historical state to create the current state.

Use:

```text
history table
      ↓
current-state projection/view
```

A current-state view can expose the latest effective state while immutable history preserves what was true at prior observation times.

## 5. Events

Event tables preserve what happened.

Examples:

- `ResearchSignalObserved`
- `AudienceStateObserved`
- `TensionActivated`
- `GuestAudienceResonanceComputed`
- `ProvocationIssued`
- `InterviewResponseRecorded`
- `EvidenceAuthenticated`
- `CandidateGenerated`
- `CandidateRejected`
- `CoalitionFormed`
- `EdgeFormed`
- `SemanticProgramCompiled`
- `ValidationExecuted`
- `StateTransitionRequested`
- `StateTransitionCommitted`
- `StateTransitionRejected`
- `OutcomeObserved`
- `VerificationPromoted`
- `VerificationQuarantined`

Exact canonical names remain subject to object reconciliation.

## 6. Receipts

Receipts should connect the causal chain rather than merely report status.

Minimum useful lineage:

```yaml
receipt_id:
run_id:
mission_id:
actor_id:
source_state:
target_state:
object_ids: []
evidence_ids: []
operation_id:
validator_results: []
input_snapshot_hash:
registry_snapshot_hash:
output_snapshot_hash:
environment_fidelity:
reward_hack_status:
taste_status:
anticentroid_status:
timestamp:
```

## 7. JSONB rule

JSONB is permitted for:

- evolving attributes;
- structured annotations;
- bounded examples;
- hypotheses awaiting canonicalization;
- function profiles;
- compact state-local context;
- evaluator diagnostics.

JSONB must not become an untyped replacement for stable semantic columns or first-class relations.

## 8. Vector layer

Vector indexes may support fuzzy retrieval of:

- evidence;
- Context Premise fragments;
- examples;
- semantic candidates;
- prior outcomes;
- perceptual/taste fixtures.

Vector similarity must not override canonical relations, validators, source provenance, or transition contracts.

## 9. Graph-like relations

Relational tables remain authoritative. Graph projections may expose high-value traversal patterns:

```text
Guest ↔ Audience
Audience ↔ Tension
Tension ↔ Invariant
Guest ↔ ExperiencedTension
Primitive ↔ Primitive
Primitive → Coalition
Coalition → Edge
Edge → Archetype
SemanticProgram → Scene
Scene → Composition
```

## 10. Transactional state change

Consequential state changes should use database transactions where feasible so that:

```text
state mutation
+
transition event
+
receipt
```

are committed consistently.

External side effects cannot always be rolled back; those actions must therefore be recorded as explicitly non-transactional boundaries with subsequent fresh-read verification.

## 11. Brownfield rule

Do not create new CAE tables until the coding agent has mapped existing tables such as receipt/audit infrastructure, person or guest registries, performance history, context registries, and any existing state models.

Produce a migration map first.
