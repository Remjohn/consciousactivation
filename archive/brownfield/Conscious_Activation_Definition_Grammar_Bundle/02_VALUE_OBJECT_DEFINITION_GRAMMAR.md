# Value Object Definition Grammar Protocol

## Artifact class

`VALUE_OBJECT`

## Purpose

Defines a semantically meaningful value whose identity is determined by its canonical value rather than an independent persistent identity.

## Definition grammar

Use:

**Value Semantics + Domain Meaning + Equality Semantics + Admissible Range + Boundary**

## Definition must establish

- what the value means
- how it is represented
- which dimensions constitute equivalence
- permitted range or enumerations
- what the value does not represent

## Required constitution sections

1. Canonical name
2. Definition
3. Value domain
4. Units / dimensions where applicable
5. Admissible range
6. Equality rules
7. Serialization form
8. Invariants
9. Consumers
10. Validators
11. Error taxonomy
12. Examples
13. Hard negatives

## Examples

`EmotionalRegister`, `VoiceRegister`, `BoundingBox`, `DHD`, `SemanticRole`, `ArousalValenceVector`.

## Boundary rules

A value object should NOT acquire identity merely because it is stored in a table. If two instances are semantically equal, their database identifiers do not make them different concepts.

## Hard negatives

- A mutable state disguised as a value object
- A persistent entity disguised as a value object
- A free-form string that should be a controlled vocabulary
