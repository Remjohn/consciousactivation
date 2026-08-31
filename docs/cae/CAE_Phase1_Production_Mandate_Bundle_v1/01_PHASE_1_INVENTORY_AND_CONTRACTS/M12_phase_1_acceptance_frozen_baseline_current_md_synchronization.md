# M12 — Phase 1 Acceptance + Frozen Baseline + CURRENT.md Synchronization

Status: PROPOSED — OPERATOR-RATIFICATION-REQUIRED
Phase: 1 — Inventory and Contracts

## 1. Decision / Objective
Freeze Phase 1 truth: consolidate evidence, create machine-readable baseline snapshot, update control state and synchronize CURRENT.md from verified evidence. This is the Phase 2 handoff authority.

## 2. Mandatory reading
Baseline: `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
M12-specific: M1–M11 evidence; baseline snapshot schema; PRD maintenance rule; program-control.


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
Generate baseline snapshot/fingerprints, synchronize CURRENT.md, record open decisions and exact commit.

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
All 12 mandates have evidence/commit; inventory/contracts/gaps exist; CURRENT.md matches reality; operator explicitly accepts or blocks Phase 2.

## 6. Stop conditions
STOP if there is an authority conflict, undefined write owner, pressure to create a canonical duplicate,
lane collapse, Skill nesting, inability to prove completion, stale/missing mandatory authority source,
or any material contradiction between the mandate and live repository.

## 7. Operator gate
The operator accepts the evidence or records a blocker/correction. No next mandate is implicit.

## 8. Scope exclusion
No broad runtime implementation. Phase 1 defines and proves the handoff required for later runtime work.

## 9. Gemini execution
Execute ONLY M12. Do not begin another mandate. After the evidence report and operator decision request, STOP.
