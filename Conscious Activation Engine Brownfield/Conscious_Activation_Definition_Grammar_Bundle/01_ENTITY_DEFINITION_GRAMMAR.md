# Entity Definition Grammar Protocol

## Artifact class

`ENTITY`

## Purpose

Defines persistent domain objects possessing identity and continuity across observations and runtime events.

## Definition grammar

Use:

**Genus + Identity + Continuity + System Function + Boundary + Nearest-Neighbor Distinction**

## Definition must establish

- what larger class of thing the entity belongs to
- what makes this entity uniquely identifiable
- what continuity means across time
- why the system needs the entity
- what it does not represent
- which neighboring objects are commonly confused with it

## Required constitution sections

1. Canonical identity
2. Definition
3. Semantic boundary
4. Taxonomic parent
5. Stable attributes
6. Relationships
7. Lifecycle
8. Provenance
9. Invariants
10. Owner / authority
11. Authorized operations
12. Prohibited operations
13. Validators
14. Error taxonomy
15. Storage representation
16. Runtime consumers
17. Examples
18. Hard negatives

## Non-negotiable distinctions

Entity identity MUST NOT be confused with:

- state
- event
- evidence
- derived interpretation

## Typical examples

`Audience`, `Subject`, `Brand`, `FormatDefinition`, `SceneDefinition`.

## Typical hard negatives

- Entity described as a current state
- Entity defined only by a single observation
- Entity whose identity changes every runtime cycle
- Entity that is actually a value object

## Validation question

“Could this object remain the same object while its state, observations, and relationships change?”
