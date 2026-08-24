# FR-CA-01-011 — Agent Query Governance and Authorized Semantic Functions

## Requirement
Agents SHOULD operate through authorized semantic retrieval/query functions instead of unrestricted database exploration for mission-critical tasks.

## Pattern
`Intent → Schema Linking → Relevant Entities/Relations → Subproblem Decomposition → Query/Retrieval Plan → Execute → Validate → Typed Error → Repair`

## Required Characteristics
- narrow purpose
- typed inputs/outputs
- owner
- authority scope
- validator
- error taxonomy
- audit/receipt behavior

## Examples
`get_active_audience_tensions`, `find_guest_audience_resonances`, `find_eligible_primitives`, `generate_coalition_candidates`, `get_previous_coalition_outcomes`.
