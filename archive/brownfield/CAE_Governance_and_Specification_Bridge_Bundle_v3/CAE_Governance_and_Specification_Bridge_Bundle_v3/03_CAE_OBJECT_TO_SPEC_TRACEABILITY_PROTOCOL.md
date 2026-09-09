# CAE Object-to-Spec Traceability Protocol v2.0

## Purpose

This protocol ensures that the object constitutions created during CAE architectural work do not become disconnected documentation. Every important object must have a traceable path from ontology to runtime.

## Traceability chain

```text
OBJECT CONSTITUTION
→ DEFINITION GRAMMAR
→ CANONICAL SCHEMA
→ RELATION / STATE / EVENT MODEL
→ FUNCTIONAL REQUIREMENT
→ TECH SPEC
→ CODE
→ TEST
→ RECEIPT
→ OUTCOME
```

## Required trace matrix

| Object | Constitution | Grammar | Schema | Relations | States | Events | FR | Tech Spec | Code | Tests | Receipts | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

No object is considered operationally established until the relevant cells are populated or explicitly marked `NOT APPLICABLE` with rationale.

## Class-aware traceability

Different artifact classes require different downstream artifacts.

### Canonical Entity
Must trace to identity, schema, relations, lifecycle, storage, and owner.

### Value Object
Must trace to field schema, equality/immutability semantics, serialization, and validators.

### Relation
Must trace to endpoint types, direction, cardinality, temporal semantics, evidence/provenance, and query access.

### State
Must trace to state vocabulary, transition graph, events, current-state view, historical state table, and transition validators.

### Event
Must trace to immutable event schema, producer, timestamp rules, payload contract, and consumers.

### Evidence
Must trace to immutable storage, source metadata, integrity/provenance, and derived artifacts that cite it.

### Operator / Primitive
Must trace to canonical definition, source evidence, admissible range, activation object, receipt, and evaluation.

### Policy / Contract
Must trace to authorized operations, prohibited operations, enforcement point, violation error, and test suite.

### Derived Artifact
Must trace backward to source lineage and forward to consumers/evaluation.

### Execution Packet / IR
Must trace to producer, consumer, serialization, validator, and runtime observation.

## Gap handling

A gap may not be silently repaired in the trace matrix. Use:

- `MISSING`
- `UNVERIFIED`
- `CONTRADICTED`
- `DEFERRED`
- `N/A`

Each non-ready status must have an owner and next decision artifact.

## Reality-contact traceability

For every material object or operation, extend the trace chain with:

```text
CODE
→ TEST
→ ENVIRONMENT FIDELITY
→ REWARD-HACK TEST
→ TASTE / ANTI-CENTROID TEST
→ RECEIPT
→ OUTCOME
```

Required additional columns:

| Object | Claim | Required Fidelity | Actual Fidelity | Reward-Hack Suite | Taste/Anti-Centroid Suite | Receipt | Outcome Evidence |
|---|---|---|---|---|---|---|---|

A missing reality-contact cell MUST remain `MISSING`, `UNVERIFIED`, or `N/A` with rationale. It may not be inferred from a green unit test.

## Evaluator traceability

Material validators and scoring functions are themselves architecture assets and MUST be traceable to:

```text
Evaluator Definition
→ Intended Property
→ Proxy Metric
→ Known Gaming Modes
→ False-Proof Tests
→ Taste Fixtures
→ Calibration History
→ Promotion Decision
```

This prevents an evaluator from becoming an ungoverned reward surface.


## State-control traceability extension

For every dynamic object, trace:

```text
Object
→ State Model
→ State Table / Projection
→ Event
→ Transition Contract
→ Authorized Operation
→ Validator
→ Receipt
→ Test
→ Reality-Contact Proof
```

A dynamic object is not implementation-complete if it exists only as a table/model without a legal transition path.
