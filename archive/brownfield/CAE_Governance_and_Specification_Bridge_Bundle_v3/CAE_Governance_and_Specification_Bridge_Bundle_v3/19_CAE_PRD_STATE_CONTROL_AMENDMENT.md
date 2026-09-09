# CAE PRD State-Control Amendment Plan v1.0

## 1. Objective

Make stateful procedural control part of the CAE PRD architecture rather than leaving it as implementation folklore.

## 2. Cross-cutting PRD doctrine

All CAE PRDs that introduce stateful behavior should inherit the following rule:

```text
Canonical state lives in PostgreSQL/Supabase.
Procedural state-control rules live in versioned contracts/runbooks/Skills.md.
State changes occur through authorized typed operations.
Consequential transitions require evidence and validation.
Transitions emit immutable events and receipts.
Historical state is preserved.
```

## 3. PRD-01 / Platform Strategy additions

Add a cross-system state-control subsection covering:

- authoritative state architecture;
- typed semantic operation layer;
- transition contracts;
- event and receipt model;
- harness/runbook relationship;
- recovery and continuation;
- operator visibility;
- StateM as external reference only.

Candidate FRs:

- `FR-CAE-STATE-01` Authoritative Operational State;
- `FR-CAE-STATE-02` Transition Contract Engine;
- `FR-CAE-STATE-03` Semantic Operation Gateway;
- `FR-CAE-STATE-04` Immutable State/Event/Receipt Lineage;
- `FR-CAE-STATE-05` Harness State-Control Integration.

## 4. PRD-02 / CCF additions

The content factory must declare the state boundaries of its intelligence pipeline, including:

```text
World Context
→ Active Pressure
→ Provocation
→ Human Response
→ Authenticated Evidence
→ Candidate Field
→ Coalition
→ Edge
→ Semantic Program
→ Realization
→ Validation
```

Each transition must reference the relevant evidence and validator contract.

## 5. PRD-08 / Primitive additions

Primitive activation must remain separate from canonical primitive definition.

Runtime primitive activation should be stateful and receipt-backed:

```text
PrimitiveDefinition
→ Candidate
→ Eligibility
→ Activation
→ Coalition
→ Receipt
```

A runtime activation must never mutate the canonical primitive registry record.

## 6. Other PRDs

Downstream PRDs should consume state transitions rather than invent competing state stores.

Examples:

- CMF consumes SemanticProgram / Scene / Composition state;
- CBCS consumes authenticated coaching evidence and profile state;
- Conscious Reactions consumes reaction/session state and outcome events;
- V2WS consumes validated semantic programs and delivery state;
- CPSC consumes verified opportunity and offer state.

## 7. PRD acceptance rule

Any future stateful PRD requirement must declare:

- state object;
- current-state source;
- transition(s);
- required evidence;
- validators;
- events;
- receipts;
- recovery behavior;
- failure/error taxonomy;
- minimum environment fidelity.

## 8. No pseudo-state

A prompt variable, JSON field, cached value, or agent memory string does not become authoritative state merely because it is called `status`, `state`, `active`, or `current`.
