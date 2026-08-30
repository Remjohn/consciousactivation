# CAE Gemini Execution Protocol — Current-State Reconciliation

This bundle inherits the repository's authoritative Gemini execution skill:

`docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`

and the mandate authoring protocol:

`docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`

Do not treat this file as a replacement for either source. It is a bundle-local index and execution reminder.

## Required sequence

`LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE WITHIN FILE BOUNDARY → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → REQUEST OPERATOR DECISION → STOP`

## Critical rule for this program

This is a read-heavy, evidence-first operation. The current PRD, control-state records, mandates, Tech Specs, receipts, and status reports are evidence sources with different authority levels; none becomes authoritative merely because it exists.

Gemini must:

- read the selected mandate completely;
- read every mandatory reference;
- inspect current repository reality before making implementation claims;
- separate `FACT`, `HYPOTHESIS`, and `DECISION REQUIRED`;
- preserve conflicts instead of silently resolving them;
- reuse existing status surfaces instead of creating competing control planes;
- update only the scope authorized by the mandate;
- record exact repository revision and verification context;
- stop at the mandate's stated boundary.

## One-at-a-time execution

Run one mandate per Gemini session. Do not authorize the entire bundle at once. CA-CSR-02 requires CA-CSR-01's accepted evidence base; CA-CSR-03 requires CA-CSR-02 acceptance; CA-CSR-04 requires the synchronized PRD.

## No runtime-convergence creep

The repository may reveal a tempting implementation opportunity. Record it as `NEXT_RUNTIME_CONVERGENCE` or `BLOCKED`, but do not implement it under this program.
