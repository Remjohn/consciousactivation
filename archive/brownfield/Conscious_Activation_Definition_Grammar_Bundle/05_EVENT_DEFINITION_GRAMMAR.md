# Event Definition Grammar Protocol

## Artifact class

`EVENT`

## Purpose

Defines an occurrence that records something that happened to, between, or within system objects at a particular time.

## Definition grammar

Use:

**Occurrence + Subject(s) + Trigger/Precondition + Time + Payload + Consequence + Evidence/Trace**

## Definition must establish

- what happened
- when it happened
- what participated
- what triggered it
- what information was produced
- what state transition it may cause
- whether it is immutable

## Examples

`InterviewResponse`, `CandidateGenerated`, `CoalitionFormed`, `ArtifactRendered`, `OutcomeObserved`, `FatalityDetected`.

## Important distinction

An Event records occurrence. It does not automatically contain the interpretation of that occurrence.

`InterviewResponse` is evidence of expression; its semantic interpretation is a separate derived artifact.

## Hard negatives

- event mistaken for current state
- event mutated to match later interpretation
- event created without source timestamp
- derived interpretation stored as if it were source occurrence
