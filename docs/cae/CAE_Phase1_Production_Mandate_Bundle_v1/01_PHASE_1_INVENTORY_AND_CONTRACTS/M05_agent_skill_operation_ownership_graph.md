# M05 — Agent / Skill / Operation Ownership Graph

Status: PROPOSED — OPERATOR-RATIFICATION-REQUIRED
Phase: 1 — Inventory and Contracts

## 1. Decision / Objective
Map reasoning capabilities to deterministic Operations, Agents, Teams, Sub-agents and Skills while preserving passive/flat Skills and four Authority Lanes.

## 2. Mandatory reading
Baseline: `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
M5-specific: Skill Constitution; builder skill packages; ProgrammedModelRegistry; workflow role taxonomy; delegation.


    ## Constitutional constraints
    - Read the entire baseline authority set and mandate-specific references before action.
    - Preserve CAE canonical ontology, Workspace scope, authority, typed operations, state and receipts.
    - Preserve Hunter / Analyst / Composer / Commander separation.
    - Preserve passive, flat Canonical Skills; no Skill-to-Skill invocation.
    - Pi is a runtime substrate; Eve is a package composition reference; neither creates CAE authority.
    - Do not create a parallel state, receipt, Program, Skill, Harness or knowledge authority.
    - No mass service→agent conversion.
    - No deletion/merge based only on naming similarity.


## 3. Allowed work
Produce capability→lane→agent/team→skill→operation→artifact graph and identify unexecuted intelligence.

## 4. Required verification
- Record exact repository commit.
- Report every file/directory actually read.
- Inspect exact symbols/callers for current behavior.
- Run focused tests and relevant aggregate verification.
- Capture runtime evidence where applicable.
- Distinguish pre-existing failures from new failures.
- Record artifacts/receipts where applicable.
- Record exact commit SHA.

## 5. Acceptance criteria
Every identified reasoning capability has an owner; no Skill nesting; no lane collapse.

## 6. Stop conditions
STOP if there is an authority conflict, undefined write owner, pressure to create a canonical duplicate,
lane collapse, Skill nesting, inability to prove completion, stale/missing mandatory authority source,
or any material contradiction between the mandate and live repository.

## 7. Operator gate
The operator accepts the evidence or records a blocker/correction. No next mandate is implicit.

## 8. Scope exclusion
No broad runtime implementation. Phase 1 defines and proves the handoff required for later runtime work.

## 9. Gemini execution
Execute ONLY M05. Do not begin another mandate. After the evidence report and operator decision request, STOP.
