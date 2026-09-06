# Wave 05 / 06 Gate Governance Bridge: Mandates CA-M040 and CA-M041

This bridge document references the completed, execution-ready gate governance mandates covering Canon Question 40:

1. **`CA-M040` (Real Human Gate Milestones & Fail-Closed Execution Suspension):**
   - File: [`../CAE_MANDATE_BUNDLE_WAVE_05/10_CA_MANDATE_040.md`](file:///d:/Work/consciousactivation/docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/10_CA_MANDATE_040.md)
   - Canonical Question: `Q40`
   - Primary Invariant: `INV-GATE-001` (`FR-040`)
   - Scope: Eliminates mock auto-approvals, halts execution at declared gates fail-closed, releases worker leases, transitions lifecycle to `AWAITING_APPROVAL`.

2. **`CA-M041` (Reactive Gate Resumption, Commander Approval Receipts & Rejection Routing):**
   - File: [`../CAE_MANDATE_BUNDLE_WAVE_05/11_CA_MANDATE_041.md`](file:///d:/Work/consciousactivation/docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/11_CA_MANDATE_041.md)
   - Canonical Question: `Q40` / Bridge to `Q41`
   - Primary Invariant: `INV-GATE-002` / `INV-AUTH-001` (`FR-040`, `FR-025`)
   - Scope: Implements `approve_program` with `AuthorityLane.COMMANDER` validation, signed `AuthorizationDecisionReceipt` generation, and reactive `RESUME` signals; implements `reject_program` with typed `RejectionDispositionRoute` rewinds without evidence destruction.

These two mandates complete the prerequisite dependency chain (`Q34–Q40`) required by Wave 06 Mandate `CA-M042` (Atomic CAS State Transitions in SQLite).
