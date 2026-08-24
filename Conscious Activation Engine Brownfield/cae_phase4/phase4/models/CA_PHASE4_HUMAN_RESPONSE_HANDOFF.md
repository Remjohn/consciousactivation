# Human Response Handoff Contract

Phase 4 hands control to Phase 5 through a typed boundary.

## Input from Phase 4

- BroadPrimarySignal
- ActivationEvent
- PressureField lineage
- candidate alternatives
- EdgingAssessment
- AntiCentroidPatrolResult
- provenance

## What Phase 5 must produce

- InterviewResponse
- AuthenticationAssessment
- EvidenceExtraction
- GuestPosition / GuestInterpretation objects where justified
- response-linked state updates

## Constitutional rule

The ActivationEvent is a hypothesis about what may produce useful human evidence. It is not evidence itself.

## Forbidden conversion

```text
BroadPrimarySignal → GuestBelief
```

without:

```text
ActivationEvent → HumanResponse → EvidenceAssessment → AuthenticatedEvidence
```
