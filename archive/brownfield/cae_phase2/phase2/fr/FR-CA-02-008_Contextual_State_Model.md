# FR-CA-02-008 — Contextual State Model

## Requirement
ContextualState MUST represent the condition of an entity, relationship, or semantic field within a specified contextual and temporal interval.

## Constraints
It MUST preserve source, observation time, confidence, activation level, and resolution lifecycle.

## Implementation Principle
ContextualState is not a static attribute and MUST NOT erase prior states.

## Acceptance Criteria
- Canonical identity/ownership is explicit.
- Object Constitution fields are defined or marked pending.
- Provenance and lifecycle are testable.
- No silent flattening of evidence into unsupported canonical claims.
- Brownfield status is recorded before replacement.

## Source Basis
- PRD-CA-01 Engine Constitution & Canonical Architecture
- PRD-CA-02 World Intelligence & Contextual State
- Phase 0/1 Context Premise, Trigger Matching, Psychological Routing, SDA, and Matrix of Edging doctrine supplied to the project.
