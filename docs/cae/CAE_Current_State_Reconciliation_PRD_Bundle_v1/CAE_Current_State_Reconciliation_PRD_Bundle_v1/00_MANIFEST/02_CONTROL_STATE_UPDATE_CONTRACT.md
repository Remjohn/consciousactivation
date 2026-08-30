# Control-State Update Contract

This program must reuse the repository's current program-control surfaces. It must not create a parallel control plane merely to report its own work.

## Required updates by phase

### CA-CSR-01
Record the exact repository revision, evidence packet path, completion state, limitations, and operator decision reference.

### CA-CSR-02
Record the accepted current-state ledger/report, reconciliation verdict, unresolved conflicts, and operator acceptance.

### CA-CSR-03
Record the PRD revision/diff, synchronized sections, evidence source, and operator authorization for final verification.

### CA-CSR-04
Record final verdict, repository revision verified, independent checks, limitations, and the operator's decision about whether a separate runtime-convergence program may begin.

If the existing repository control-state schema cannot represent one of these transitions, classify the mismatch as `SCHEMA_ERROR` or `AUTHORITY_ERROR` and stop rather than inventing a new global status model.
