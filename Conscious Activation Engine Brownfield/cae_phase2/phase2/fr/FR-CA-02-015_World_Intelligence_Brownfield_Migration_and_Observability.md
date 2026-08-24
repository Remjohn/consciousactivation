# FR-CA-02-015 — World Intelligence Brownfield Migration and Observability

## Requirement
The Phase 2 implementation MUST be brownfield-first and observable.

## Constraints
Repository components must be classified as EXISTS, PARTIAL, DUPLICATED, CONFLICTING, SPEC-ONLY, MISSING, or DEPRECATED before migration decisions.

## Implementation Principle
Every migrated object needs lineage, compatibility notes, test coverage, and operational observability.

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
