---
type: functional-requirement
module: PRD-CA-04
id: FR-CA-04-006
title: Matrix of Edging Candidate Generation
status: proposed
phase: 4
---

# 006 — Matrix of Edging Candidate Generation

## Requirement
The system SHALL implement the Matrix of Edging Candidate Generation capability as a typed, provenance-preserving component of the Pressure / Matrix of Edging layer.

## Purpose
This requirement exists to ensure pressure selection remains grounded in the canonical CAE architecture and does not collapse into free-form prompt behavior.

## Inputs
- authorized Phase 2 World Intelligence objects
- authorized Phase 3 relational objects
- relevant state/history
- canonical taxonomy and policies

## Outputs
- typed Phase 4 artifact(s)
- decision lineage
- validation status
- typed errors when the requirement cannot be satisfied

## Deterministic obligations
1. Do not mutate immutable evidence.
2. Do not convert hypotheses into facts.
3. Preserve contradictions and rejected alternatives.
4. Record provenance for every derived decision.
5. Fail diagnostically rather than issuing a generic retry.

## Acceptance criteria
- schema-valid output
- explicit owner and role
- reproducible retrieval path
- validator result recorded
- error taxonomy used on failure
- brownfield observability available
