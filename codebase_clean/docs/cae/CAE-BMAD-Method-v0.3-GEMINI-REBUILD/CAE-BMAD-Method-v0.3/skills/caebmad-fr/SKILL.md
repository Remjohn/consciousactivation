---
name: caebmad-fr
description: Skill for compiling and validating the central Functional Requirements matrix with traceability from sources through PRD modules to acceptance tests.
version: 0.3.0-rebuild
agent: cae-prd-agent
---

# Skill: caebmad-fr

## 1. Purpose & Invocation
The `caebmad-fr` skill compiles, validates, and maintains the central Functional Requirements (FR) matrix that traces every product requirement from source lineage through PRD modules to concrete acceptance criteria.

## 2. Invocation Preconditions
1. At least one PRD module exists with `functional_requirements` entries.
2. Product Reconstruction Record is available for upstream traceability.
3. PRD module schema is loaded for validation.

## 3. Execution Logic
1. **FR Collection:** Scan all PRD modules under `docs/cae-bmad/03_product/modules/` and extract FR entries.
2. **Deduplication:** Detect duplicate FR IDs and conflicting descriptions across modules.
3. **Traceability Verification:** Ensure every FR links to at least one source (`SRC-xxx`) and at least one acceptance criterion.
4. **Testability Audit:** Reject FRs where `testable` is not `true` or acceptance criteria are vague.
5. **Matrix Emission:** Generate `docs/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md`.

## 4. Output Contract
- Central FR matrix at `docs/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md`
- FR deduplication and conflict report
