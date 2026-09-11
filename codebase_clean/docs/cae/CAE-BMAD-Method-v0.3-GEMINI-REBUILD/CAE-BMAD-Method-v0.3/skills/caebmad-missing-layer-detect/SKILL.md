---
name: caebmad-missing-layer-detect
description: Discovers, catalogs, and ranks missing layers, partial implementations, and execution gaps into the Missing Implementation Register.
version: 0.3.0-rebuild
agent: cae-brownfield-auditor
---

# Skill: caebmad-missing-layer-detect

## 1. Purpose & Invocation
The `caebmad-missing-layer-detect` skill enables the `cae-brownfield-auditor` to construct and maintain the formal Missing Implementation Register.

## 2. Invocation Preconditions
1. Brownfield Reconciliation Report generated.
2. Operating level assessments and code forensics available.
3. Schema `schemas/missing_implementation_register.schema.json` loaded.

## 3. Execution Logic
1. **Gap Identification:** Extract all `MISSING_LAYER` and `PARTIAL_IMPLEMENTATION` items.
2. **Severity & Blocker Assessment:** Classify each gap by severity (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) and blocking flag.
3. **Remediation Plan Formulation:** Provide actionable steps to implement missing code surfaces.
4. **Deliverable Emission:** Assemble `docs/cae-bmad/07_brownfield/MISSING_IMPLEMENTATION_REGISTER.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/MISSING_IMPLEMENTATION_REGISTER.json`
- `docs/cae-bmad/07_brownfield/MISSING_IMPLEMENTATION_REGISTER.md`
