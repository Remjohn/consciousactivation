# CAE-BMAD Product Artifact Pipeline Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M09  
**Scope:** Multi-agent production pipeline, dependency sequencing, handoff schemas, and quality gates for core product artifacts (Product Brief, PRD Index, Modular PRDs, Functional Requirements, Architecture, UI/UX, Epics, Stories).

---

## 1. Multi-Agent Production Pipeline Overview

The Product Artifact Pipeline converts raw research corpus synthesis and operator intent into fully specified, delivery-ready engineering artifacts.

```text
Level 01: PRODUCT / INTENT        [cae-product-brief-agent]  → PRODUCT_BRIEF.md
         ↕
Level 02: DOCUMENTATION           [cae-prd-agent]            → PRD_INDEX.md, modules/PRD-*.md, FUNCTIONAL_REQUIREMENTS.md
         ↕
Level 02/07: ARCHITECTURE         [cae-architecture-agent]   → ARCHITECTURE.md
         ↕
Level 01/07: UI / UX              [cae-ux-agent]             → UI_UX_SPECIFICATION.md
         ↕
Level 03: PLAN                    [cae-delivery-agent]       → EPICS.md, STORIES.md
         ↕
Level ALL: REVIEW                 [cae-adversarial-reviewer] → Cross-artifact integrity audit
```

---

## 2. Core Artifact Standards & Invariants

1. **Product Brief (`docs/cae-bmad/03_product/PRODUCT_BRIEF.md`):**
   - Synthesizes product vision, target audience, 5 capability pillars, non-goals, and success metrics.
   - Bound to `schemas/product_brief.schema.json`.

2. **Modular PRDs & FR Matrix (`docs/cae-bmad/03_product/`):**
   - 5 modular PRD specifications with source lineage (`SRC-xxx`) and atomic testable functional requirements (`FR-xxx`).
   - Bound to `schemas/prd_module.schema.json`.

3. **Technical Architecture (`docs/cae-bmad/04_architecture/ARCHITECTURE.md`):**
   - Defines core subsystems, typed interface boundaries, event buses, protocol choices, and brownfield integration strategy.
   - Bound to `schemas/architecture_spec.schema.json`.

4. **UI/UX Specification (`docs/cae-bmad/06_ui_ux/UI_UX_SPECIFICATION.md`):**
   - Details operator studio views, interaction flows, responsive error modals, and Atomic Harness visual syntax tokens.
   - Bound to `schemas/ui_ux_spec.schema.json`.

5. **Epics & Stories Backlog (`docs/cae-bmad/05_planning/`):**
   - Actionable user stories with concrete acceptance criteria tied to functional requirements.
   - Bound to `schemas/epic_story.schema.json`.

---

## 3. Handoff Integrity Gates

- **Gate A (Brief → PRD):** PRD modules cannot be authored until Product Brief establishes non-goals.
- **Gate B (PRD → Architecture):** Technical architecture must address all functional requirements in the FR matrix.
- **Gate C (Architecture → Epics):** Epics must cite subsystem boundaries and interface schemas.
- **Gate D (UI/UX → Stories):** Frontend stories must trace to operator views and Atomic Harness design tokens.
