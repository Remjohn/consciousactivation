# FR-CA-01-006 — Dynamic State and Temporal Model Governance

## Requirement
The engine SHALL represent time-varying conditions as state records and preserve observation history rather than mutating identity.

## Core State Families
- AudienceState
- GuestState
- ContextualState
- PrimitiveActivation
- CoalitionState
- Render/ExecutionState where needed

## Example State Vocabulary
`latent | active | intensified | saturated | resolved | blocked | superseded | historical`

## Acceptance Criteria
- Every state has temporal provenance.
- State transitions are explicit and validatable.
- Current-state projections do not erase historical observations.
- Decay/expiry can be modeled where relevant.
- State is never used as a hidden synonym for entity identity.
