---
name: caebmad-brownfield-reconciliation
description: Audits the delta between product/architecture claims and codebase ground truth, generating the Brownfield Reconciliation Report.
version: 0.3.0-rebuild
agent: cae-brownfield-auditor
---

# Skill: caebmad-brownfield-reconciliation

## 1. Purpose & Invocation
The `caebmad-brownfield-reconciliation` skill enables the `cae-brownfield-auditor` to evaluate planned subsystems against physical code across Levels 01–13.

## 2. Invocation Preconditions
1. Architecture and PRD specifications available.
2. Repository, Application, and Data maps loaded.
3. Schema `schemas/brownfield_reconciliation.schema.json` loaded.

## 3. Execution Logic
1. **Delta Comparison:** Compare each subsystem against physical filesystem existence.
2. **Fidelity Classification:** Assign `VERIFIED_COMPLETE`, `PARTIAL_IMPLEMENTATION`, `MISSING_LAYER`, or `CONTRADICTED`.
3. **Quarantine Strategy Formulation:** Define non-destructive isolation policies for legacy paths.
4. **Deliverable Emission:** Assemble `docs/cae-bmad/07_brownfield/BROWNFIELD_RECONCILIATION_REPORT.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/BROWNFIELD_RECONCILIATION_REPORT.json`
- `docs/cae-bmad/07_brownfield/BROWNFIELD_RECONCILIATION_REPORT.md`
