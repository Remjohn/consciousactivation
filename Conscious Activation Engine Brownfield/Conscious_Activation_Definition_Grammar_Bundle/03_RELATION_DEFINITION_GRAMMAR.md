# Relation Definition Grammar Protocol

## Artifact class

`RELATION`

## Purpose

Defines a typed assertion connecting two or more objects with direction, semantics, and optionally temporal scope.

## Definition grammar

Use:

**Source + Relation Semantics + Target + Direction + Temporal Scope + Evidence Basis + Non-Implications**

## Definition must establish

- what entities participate
- relationship direction
- what the relation asserts
- whether it is symmetric or asymmetric
- whether it is temporal
- what evidence supports it
- what the relationship DOES NOT imply

## Required constitution sections

1. Relation identity
2. Source class
3. Target class
4. Cardinality
5. Directionality
6. Temporal semantics
7. Evidence requirements
8. Attributes
9. State if applicable
10. Invariants
11. Authorized creation/update/deletion semantics
12. Validators
13. Error taxonomy
14. Storage representation
15. Examples
16. Hard negatives

## Example

`GuestExperiencedTension` asserts that a Subject directly experienced a specified human tension during an identifiable contextual or historical interval. It does not imply that the Subject currently experiences the tension, has resolved it, or is authorized to discuss it publicly.

## Hard negatives

- “experienced” interpreted as “currently experiencing”
- “related to” used where direction matters
- relationship inferred without evidence
- relationship deleted instead of historically superseded
