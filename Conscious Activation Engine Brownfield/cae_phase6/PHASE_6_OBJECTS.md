# Phase 6 Objects

## Canonical definitions / registries
- PrimitiveDefinition
- PrimitiveFamily
- PrimitiveCompatibilityRule
- PrimitiveGeometryDefinition
- CoalitionPolicy
- EdgeTypeDefinition

## Runtime / derived semantic objects
- InvariantFieldPacket
- RepresentationGeometryPacket
- ArchetypalGeometryPacket
- PrimitiveCandidate
- CandidateAssessment
- CoalitionCandidate
- CoalitionSignature
- EdgeProduct

## Runtime state
- CandidateState
- CoalitionState
- EdgeState
- ActivationState

## Events
- SemanticFieldConstructed
- PrimitiveCandidateGenerated
- CandidateRejected
- CandidateSurvived
- CompatibilityEvaluated
- CoalitionFormed
- CoalitionRejected
- EdgeProductDerived
- SemanticCompilationValidated
- SemanticCompilationFailed

## Receipts
- CandidateReceipt
- CoalitionReceipt
- SemanticCompilationReceipt

## Important distinction

`PrimitiveDefinition` is canonical and must not become runtime state.

`PrimitiveActivation` / candidate objects carry contextual activation.

`CoalitionSignature` records selected operator geometry.

`EdgeProduct` records the emergent tension object.

None of these may overwrite the registry definition from which they were derived.
