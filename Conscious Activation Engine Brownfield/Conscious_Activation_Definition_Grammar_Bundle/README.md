# Conscious Activation — Definition Grammar Protocol Bundle

**Status:** Proposed Canonical Draft  
**Purpose:** Provide role-specific definition grammar protocols for authoring canonical Conscious Activation objects before schema, SQL/JSONB, Pydantic, Skills.md, or runtime implementation.

## Governing principle

**Role before schema.** An artifact is classified by architectural role before its schema is designed. Each artifact class therefore has its own definition grammar, constitutional requirements, legal boundaries, and validation expectations.

## Canonical chain

`ROLE → ARTIFACT CLASS → DEFINITION GRAMMAR → OBJECT CONSTITUTION → SCHEMA → IMPLEMENTATION → RUNTIME`

## Global object lifecycle classes

- `CANONICAL` — authoritative, versioned definitions.
- `DYNAMIC` — time-varying state or activation records.
- `IMMUTABLE_EVIDENCE` — source observations that must be preserved rather than overwritten.
- `DERIVED` — recomputable objects produced from upstream evidence/state/definitions.

## Global artifact classes in this bundle

1. Entity
2. Value Object
3. Relation
4. State
5. Event
6. Evidence
7. Canonical Ontology Object
8. Structural Grammar
9. Operator / Primitive
10. Policy / Contract
11. Derived Artifact
12. Execution Packet
13. Adversarial Evaluation Asset
14. IR Object
15. Longitudinal Memory Record

## Non-negotiable rules

1. Definitions must establish identity, function, boundary, and distinction from nearest neighbors.
2. Definition length is determined by semantic complexity, not a fixed word count.
3. Canonical definitions must not be inferred from runtime convenience.
4. Runtime instances must not mutate canonical definitions.
5. Evidence must remain traceable to its source.
6. Derived artifacts must preserve lineage and be reproducible where practical.
7. Every object must have an explicit owner and authority boundary.
8. Every runtime-relevant object must have validators and a typed error taxonomy.
9. Examples and hard negatives are part of object understanding, not decorative documentation.
10. Prose may be authoritative source material, but canonical machine behavior must ultimately be represented through typed structures and executable contracts.
