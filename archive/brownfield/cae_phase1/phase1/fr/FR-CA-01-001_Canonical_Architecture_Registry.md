# FR-CA-01-001 — Canonical Architecture Registry

## Requirement
The system SHALL maintain a versioned registry of canonical architectural objects, artifact classes, ontological planes, and ownership boundaries.

## Purpose
Prevent agents and developers from inventing inconsistent object identities or placing objects in undocumented layers.

## Inputs
- Phase 0 architecture
- object constitution
- approved object definitions
- brownfield inventory evidence

## Outputs
- canonical object register
- versioned taxonomy mapping
- object ownership map

## Rules
- Every canonical object has exactly one primary artifact class.
- Every object has one primary ontological plane.
- Cross-plane participation must be represented through explicit mappings/relations.
- The registry is versioned and append/change controlled.

## Acceptance Criteria
1. Every object can be located by identity, class, plane, and owner.
2. Duplicate object names are detected before promotion.
3. Registry changes carry rationale, source lineage, and migration impact.
4. An unclassified object cannot enter production as canonical.

## Brownfield
Current code location and implementation status MUST be populated during repository audit.
