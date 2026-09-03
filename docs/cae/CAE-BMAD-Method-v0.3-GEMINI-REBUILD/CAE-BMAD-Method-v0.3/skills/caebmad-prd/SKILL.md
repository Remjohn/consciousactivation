---
name: caebmad-prd
description: Skill for authoring and validating modular PRD modules with source lineage traceability and functional requirements.
version: 0.3.0-rebuild
agent: cae-prd-agent
---

# Skill: caebmad-prd

## 1. Purpose & Invocation
The `caebmad-prd` skill enables the `cae-prd-agent` and `cae-documentation-analyst` to author, validate, and index modular PRD modules following the CCP modular PRD tradition.

## 2. Invocation Preconditions
1. Product Reconstruction Record (`docs/cae-bmad/01_reconstruction/PRODUCT_RECONSTRUCTION.md`) is available.
2. 216-source research library is loaded and accessible.
3. PRD module schema (`schemas/prd_module.schema.json`) is available.

## 3. Execution Logic
1. **Pillar Selection:** Identify which of the 5 capability pillars this PRD module addresses.
2. **Source Lineage Binding:** Attach `SRC-xxx` references from the 216-source library with fidelity status tags.
3. **FR Authoring:** Write atomic, testable functional requirements (`FR-xxx`) with concrete acceptance criteria.
4. **Schema Validation:** Validate the module against `schemas/prd_module.schema.json`.
5. **Index Update:** Update the PRD index at `docs/cae-bmad/03_product/PRD_INDEX.md`.

## 4. Output Contract
- Individual PRD module file at `docs/cae-bmad/03_product/modules/PRD-xxx.md`
- Updated PRD index
- FR entries for the central Functional Requirements matrix
