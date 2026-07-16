# CMF Atomic Harness Builder Next — Sharded PRD Package V1.2 Aligned Overlay

**Status:** `draft_for_review`  
**Version:** `0.2.0-draft`  
**Created:** 2026-07-13

This package converts the completed 33-question Grill-me product-constitution session and the approved Builder Workflow Runtime delta into a BMAD-informed, CMF-governed sharded PRD.

## Package facts

- **33** locked product decisions
- **18** behavioral feature shards
- **210** globally stable Functional Requirements
- **53** cross-cutting Non-Functional Requirements
- **14** operator and downstream user journeys
- **5** canonical format categories
- **3** explicit compilation targets
- **22** binding anti-goals

## Start here

1. [`sources/CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_CONSTITUTION_V1_1.md`](sources/CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_CONSTITUTION_V1_1.md) — highest-order Activative and visual doctrine
2. [`docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md`](docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md) — binding Builder V1.2 amendment
3. [`governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`](governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml) — executable authority order
4. [`prd/index.md`](prd/index.md) — sharded PRD index
5. [`prd/PRD_COMBINED.md`](prd/PRD_COMBINED.md) — single-file reading view
6. [`governance/REQUIREMENTS_REGISTRY.yaml`](governance/REQUIREMENTS_REGISTRY.yaml) — machine-readable FR/NFR registry
7. [`docs/contracts/CONTRACT_REGISTRY.yaml`](docs/contracts/CONTRACT_REGISTRY.yaml) — V1.2 Builder-owned contract catalog
8. [`validation/PRD_VALIDATION_REPORT.md`](validation/PRD_VALIDATION_REPORT.md) — package validation result

## Documentation boundary

The main PRD defines **what the product must do and what success means**. Technical choices and detailed mechanisms are captured as Architecture handoff or addendum material. Epics and Stories are intentionally not authored yet; BMAD-style planning begins only after approved Architecture and, for the Control Tower, a UX contract.

## Rebuild and validate

```bash
python scripts/rebuild_combined_prd.py
python scripts/validate_prd_package.py
```

The generated validation reports are authoritative only for this package version and file set.
