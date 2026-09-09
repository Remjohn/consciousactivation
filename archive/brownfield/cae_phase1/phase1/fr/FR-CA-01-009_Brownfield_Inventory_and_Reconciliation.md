# FR-CA-01-009 — Brownfield Inventory and Reconciliation

## Requirement
Before implementation changes are authorized, the existing codebase SHALL be inspected and mapped to the canonical architecture.

## Required Inventory Dimensions
- existing implementation
- current behavior
- duplicated responsibility
- schema already present
- registry already present
- missing relationship/state model
- missing runtime/validation
- historical spec only
- deprecated behavior

## Acceptance Criteria
No greenfield replacement may be proposed where a compatible implementation exists without an explicit migration/reconciliation decision.

## Phase 1 Deliverable
A machine-readable Brownfield Coverage Registry and a human-readable architecture reconciliation report.
