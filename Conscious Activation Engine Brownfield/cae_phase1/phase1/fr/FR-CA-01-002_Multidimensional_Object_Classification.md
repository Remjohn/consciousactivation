# FR-CA-01-002 — Multidimensional Object Classification

## Requirement
The system SHALL classify objects across independent axes: artifact class, plane, canonicality, mutability, epistemic status, authority status, lifecycle, and runtime role.

## Purpose
Prevent false simplicity such as treating all dynamic objects, all registries, or all prose artifacts as the same kind of thing.

## Acceptance Criteria
- A state can be dynamic without becoming a canonical ontology object.
- An immutable evidence record may remain contextual without being derived.
- A canonical primitive definition can be versioned without being mutable runtime state.
- A derived artifact can be reproducible without being canonical.
- No single lifecycle label may encode multiple independent dimensions.

## Failure Codes
`TAXONOMY_ERROR.class_conflict`, `TAXONOMY_ERROR.plane_conflict`, `ONTOLOGY_ERROR.role_ambiguity`.
