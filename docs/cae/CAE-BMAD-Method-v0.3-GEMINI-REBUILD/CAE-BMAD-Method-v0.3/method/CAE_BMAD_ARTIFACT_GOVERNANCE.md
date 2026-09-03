# CAE-BMAD Artifact Governance

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL POLICY  
**Authority:** CAE Rebuild Program / Operator Mandate M01  
**Scope:** Lifecycle, schema requirements, versioning, mutation rules, and promotion standards for all CAE-BMAD method artifacts.

---

## 1. The 15 Governed Artifact Families

Every CAE-BMAD execution operates on a strict set of 15 artifact families:

| # | Artifact Family | Standard Path | Schema / Structure Standard | Primary Author Agent |
|---|---|---|---|---|
| 01 | Research Corpus | `.caebmad/research/CAE_RESEARCH_LIBRARY.yaml` | `schemas/research_source.schema.json` | `cae-product-reconstructor` |
| 02 | Product Reconstruction | `docs/cae-bmad/01_reconstruction/PRODUCT_RECONSTRUCTION.md` | `templates/product_reconstruction.md` | `cae-product-reconstructor` |
| 03 | Operating Level Assessment | `docs/cae-bmad/02_investigation/OPERATING_LEVEL_ASSESSMENT.md` | `templates/operating_level_assessment.md` | `cae-documentation-analyst` |
| 04 | Decision Ledger / Grill | `docs/cae-bmad/00_governance/DECISION_LEDGER.md` | `schemas/decision_ledger.schema.json` | `cae-method-orchestrator` |
| 05 | Product Brief | `docs/cae-bmad/03_product/PRODUCT_BRIEF.md` | `templates/product_brief.md` | `cae-product-brief-agent` |
| 06 | PRD Index | `docs/cae-bmad/03_product/PRD_INDEX.md` | `templates/prd_index.md` | `cae-prd-agent` |
| 07 | PRD Modules | `docs/cae-bmad/03_product/modules/PRD-*.md` | `templates/prd_module.md` | `cae-prd-agent` |
| 08 | Functional Requirements (FR) | `docs/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md` | `templates/fr_matrix.md` | `cae-prd-agent` |
| 09 | Architecture Specification | `docs/cae-bmad/04_architecture/ARCHITECTURE.md` | `templates/architecture.md` | `cae-architecture-agent` |
| 10 | Epics Matrix | `docs/cae-bmad/05_planning/EPICS.md` | `templates/epics.md` | `cae-delivery-agent` |
| 11 | Stories Matrix | `docs/cae-bmad/05_planning/STORIES.md` | `templates/stories.md` | `cae-delivery-agent` |
| 12 | UI/UX Specification | `docs/cae-bmad/06_ui_ux/UI_UX_SPECIFICATION.md` | `templates/ui_ux.md` | `cae-ux-agent` |
| 13 | Brownfield Reality Map | `docs/cae-bmad/07_brownfield/BROWNFIELD_REALITY_MAP.md` | `templates/brownfield_reality_map.md` | `cae-brownfield-auditor` |
| 14 | Implementation / Handoff | `docs/cae-bmad/08_handoff/IMPLEMENTATION_HANDOFF.md` | `templates/implementation_handoff.md` | `cae-method-orchestrator` |
| 15 | Review & Promotion Gate | `docs/cae-bmad/09_review/REVIEW_AND_GATE_RECORD.md` | `templates/review_record.md` | `cae-adversarial-reviewer` |

---

## 2. Artifact Header Standard

Every markdown artifact produced by the method must begin with a standardized metadata frontmatter:

```yaml
---
artifact_id: string (e.g. CAE-ART-PRD-001)
artifact_family: string (e.g. prd_modules)
title: string
version: string (semantic versioning, e.g. 1.0.0)
status: enum [DRAFT, GRILL_PENDING, IN_REVIEW, APPROVED, SUPERSEDED]
primary_agent: string (agent ID)
operating_level: string (operating level name)
source_provenance:
  - source_id: string
    relevance: integer
    authority_class: enum [CURRENT, HISTORICAL, TRANSCRIPT, REFERENCE]
upstream_dependencies:
  - artifact_id: string
created_at: ISO8601 string
updated_at: ISO8601 string
---
```

---

## 3. Mutation and Versioning Invariants

1. **Immutability of Approved Milestones:** Once an artifact is promoted to `APPROVED` via an operator gate, it becomes immutable for that version slice. Any subsequent changes require incrementing the minor/patch version and generating a change rationale delta.
2. **Preservation of Contradictions:** If an artifact uncovers a conflict between two authoritative sources, it must not resolve the contradiction by guessing. It must tag the conflicting claims as `CONTRADICTED` and record a pending issue in the Decision Ledger.
3. **Traceability Links:** All artifact references must use relative file links (e.g. `[PRD Index](../03_product/PRD_INDEX.md)`) that validate under automated reference checks.
