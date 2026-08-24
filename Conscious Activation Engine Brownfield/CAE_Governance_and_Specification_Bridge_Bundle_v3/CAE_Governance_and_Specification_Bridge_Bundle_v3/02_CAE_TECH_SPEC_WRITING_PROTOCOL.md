# CAE Tech-Spec Writing Protocol v2.0

**Purpose:** Successor to the legacy Era 3 Tech-Spec Writing Protocol for the Conscious Activation Engine brownfield program.

## 1. Position

The legacy Era 3 protocol remains a valuable engineering precedent. CAE adopts its strongest controls—evidence loading, exact backend integration, typed schemas, acceptance criteria, failure examples, explicit testing, dependency tracing—but adds the architectural layers required by CAE:

```text
Architectural Role
→ Object Constitution
→ Brownfield Reconciliation
→ Functional Requirement
→ Tech Spec
→ Implementation
```

A Tech Spec is not allowed to invent ontology.

## 2. Mandatory pre-work

Before writing the spec, read in this order:

1. CAE phase architecture relevant to the assignment.
2. Phase validation result.
3. Relevant Object Constitution(s).
4. Relevant definition grammar skill/protocol.
5. Relevant PRD / FR.
6. Existing repository implementation.
7. Existing database schema/migrations.
8. Inherited registries: SDA, SFL, Primitive registries and crosswalks.
9. Existing services, agents, pipelines, and routes.
10. Existing tests.
11. Relevant RSCS / CBAR / reasoning protocols.
12. Existing receipts/evidence patterns.
13. CAE State & Transition Control Protocol.
14. StateM reference boundary, if the spec involves harness/runtime state control.

If a referenced source cannot be inspected, the writer MUST record `UNVERIFIED` and stop the affected portion rather than fabricate it.

## 3. Mandatory evidence log

Every Tech Spec begins with:

```text
1. ARCHITECTURE LOADED
2. PHASE VALIDATION LOADED
3. OBJECT CONSTITUTION(S) LOADED
4. DEFINITION GRAMMAR LOADED
5. PRD/FR LOADED
6. BROWNFIELD CODE READ
7. DATABASE/SHEMA READ
8. REGISTRIES READ
9. TEST PATTERN READ
10. REASONING/VALIDATION PROTOCOLS READ
```

Each line must contain a concrete fact proving the source was actually read.

## 4. Mandatory 14-section spec format

```text
1. Files and Evidence Read
2. Architectural Role and Boundaries
3. Brownfield Reality
4. Functional Requirement Traceability
5. Canonical Object / Schema Contract
6. Relationships, State, Events, and Temporal Rules
7. Authorized Operations and Agent Program Contract
8. IR / Runtime Contract
9. Validation and Error Taxonomy
10. Implementation Plan
11. Backward Compatibility / Migration / Rollback
12. Acceptance Criteria
13. Dependencies
14. Testing and Verification
```

## 5. Section 2 — Architectural role

State:

- artifact class
- ontological plane
- architectural role
- nearest neighbors
- explicit boundaries
- authority owner

This section prevents schema convenience from determining ontology.

## 6. Section 3 — Brownfield reality

Every reused or extended service MUST be listed with:

- exact path;
- existing class/function/method;
- current behavior;
- compatibility constraints;
- proposed extension point.

The spec MUST distinguish `NEW`, `EXTEND`, `ADAPT`, `REPLACE`, `READ`, and `DEPRECATE`.

## 7. Section 5 — Canonical schema contract

All stable semantic fields MUST be strongly typed.

Use:

- PostgreSQL typed columns for stable canonical semantics;
- relational tables for first-class relationships;
- JSONB for evolving structured attributes and bounded examples/annotations;
- vector indexes for fuzzy semantic retrieval;
- event tables for observations/history;
- Pydantic/SQLModel/Zod schemas for program boundaries.

JSONB MUST NOT be used as an unstructured repository for the entire object.

## 8. Section 6 — State and temporal semantics

If an object has state, the spec MUST define:

- state vocabulary;
- valid transitions;
- transition triggers;
- temporal provenance;
- decay/expiry if applicable;
- supersession rules;
- historical preservation;
- concurrency behavior if relevant.

Current state MUST NOT overwrite immutable observations.

## 9. Section 7 — Agent program contract

The system MUST prefer:

```text
Human/Agent Intent
→ Schema Linking
→ Relevant Entities/Relations
→ Subproblem Decomposition
→ Retrieval/Composition Plan
→ Structured Query/Function
→ Execute
→ Validate
→ Typed Error
→ Repair
```

Agents should use authorized SQL views/functions/services instead of arbitrary database access where governance requires it.

Each program MUST define:

- inputs;
- allowed data sources;
- query functions;
- decision predicates;
- output type;
- validation gates;
- error classes;
- repair policy;
- receipt requirements.

## 10. Section 9 — Error taxonomy

A spec MUST identify typed failures. CAE minimum taxonomy:

```text
SCHEMA_ERROR
RELATION_ERROR
STATE_ERROR
EVENT_ERROR
EVIDENCE_ERROR
PROVENANCE_ERROR
TAXONOMY_ERROR
ONTOLOGY_ERROR
REGISTRY_ERROR
PRIMITIVE_ERROR
COALITION_ERROR
SEMANTIC_DRIFT
PERCEPTUAL_DRIFT
FORMAT_DRIFT
COMPOSITION_ERROR
CONTRACT_ERROR
QUERY_PLAN_ERROR
RUNTIME_ERROR
VALIDATION_ERROR
FATALITY
```

Error messages MUST identify the violated relation, state, contract, schema, or policy whenever possible.

## 11. Anti-centroid / anti-RLHF requirement

CAE Tech Specs MUST NOT silently inject generic safety, politeness, corporate tone, authorization language, or risk-avoidance boilerplate into semantic definitions unless that behavior is an explicit architectural requirement.

The protection stack is designed to prevent:

- centroid collapse;
- synthetic smoothness;
- false depth;
- over-resolution;
- generic professionalization;
- semantic edge dilution.

Normative rules MUST preserve architectural sharpness while enforcing genuine integrity, evidence, and system constraints.

`Matrix of Edging`, SDA, SFL, anti-centroid assets, and authenticated human evidence remain authoritative sources for preserving semantic force.

## 12. Acceptance criteria

Every AC MUST specify:

- Given
- When
- Then
- measurable pass condition
- concrete failure example
- governing object/contract
- applicable validator/error taxonomy

## 13. Testing

At minimum:


- schema/model tests;
- relation/state transition tests;
- SQL function/query tests;
- program orchestration tests;
- registry integrity tests;
- regression tests for hard negatives where applicable;
- integration tests using existing repository patterns;
- receipt verification;
- environment-fidelity verification;
- reward-hacking / false-proof tests;
- taste / anti-centroid regression tests where the claim is meaning- or perceptual-sensitive;
- outcome tests where the requirement claims real-world effectiveness.

## 13A. Reality-Contact Evaluation Requirements

Every material Tech Spec MUST include a dedicated validation table:

| Claim | Proxy | Intended Property | Minimum Fidelity | Gaming Strategy | Counter-Test | Taste/Reality Test | Receipt |
|---|---|---|---|---|---|---|---|

The spec MUST NOT use “test passes” as shorthand for “quality proven.”

Where the claim concerns human response, audience resonance, authenticity, taste, or real-world performance, the spec MUST identify the path from synthetic/integration evidence to E4 observation.

A Tech Spec may define a `taste_profile`, but it MUST NOT reduce the entire claim to a scalar score.

## 14. Implementation gate

A spec cannot enter implementation if:

- object role is unresolved;
- brownfield integration is unverified;
- required registry IDs are unverified;
- primary schema contains untyped core semantics;
- state transitions are ambiguous;
- error taxonomy is missing;
- no test can prove a critical requirement;
- migration behavior is undefined for an existing implementation.

## 7. Section 6 — Relationships, State, Events, and Temporal Rules

Every stateful spec MUST define:

- authoritative current-state source;
- historical-state representation;
- legal transitions;
- transition preconditions;
- required evidence;
- validators;
- transition events;
- receipts;
- recovery behavior;
- stale/conflict semantics;
- idempotency expectations.

The spec must identify whether each state change is `NEW`, `EXTEND`, `ADAPT`, or `REPLACE` existing state infrastructure. PostgreSQL/Supabase is the CAE default authority unless brownfield evidence establishes an explicit exception.

## 8. Section 7 — Authorized Operations and Agent Program Contract

Consequential state changes MUST occur through typed authorized operations where available. Raw database mutation by the agent is not a substitute for the semantic operation layer.

Each operation MUST identify its preconditions, writes, validators, errors, receipt, and idempotency behavior.

## 9. StateM reference requirement

When borrowing or adapting StateM patterns, the spec MUST include:

- the exact StateM repository URL;
- the paper URL;
- the StateM concept being borrowed;
- the CAE adaptation;
- why local StateM storage is or is not used;
- any code-reuse decision and source commit/license record.

StateM is an external implementation precedent, not CAE ontology or authority.
