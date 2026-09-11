# Scope and Non-Goals

## In scope

- Repository-level inventory of code, tests, migrations, schemas, runtime surfaces, control-state artifacts, skills, mandates, Tech Specs, PRD surfaces, and current program-status records.
- Verification of claims that materially affect “where we stand now.”
- Reconciliation of authority and implementation status.
- Identification of stale, superseded, duplicate-looking, or conflicting artifacts.
- Synchronization of `docs/PRD/CURRENT.md` from verified evidence.
- Final independent verification and operator-ready handoff for the next program.

## Explicitly out of scope

- Implementing runtime convergence.
- Refactoring unrelated code.
- Deleting “legacy” files without an operator decision.
- Changing canonical object definitions because they are inconvenient.
- Introducing new architecture to solve a discovered gap.
- Fixing every discovered defect. Defects are recorded and routed.
- Re-running expensive external systems unless required to verify a material current-state claim.

## Smallest useful operation

The program is successful when it produces a trustworthy current-state ledger and a synchronized PRD, even if significant portions of the system remain incomplete.
