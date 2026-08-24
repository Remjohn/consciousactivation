# FR-CA-02-013 — World Intelligence Authorized Query Functions

## Requirement
Agents MUST access World Intelligence through authorized semantic functions/views rather than unrestricted database exploration.

## Constraints
Functions MUST specify inputs, filters, returned fields, confidence semantics, and authorization.

## Implementation Principle
Query planning should resolve intent → schema → entities/relations → time/state filters → evidence → typed result.

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
