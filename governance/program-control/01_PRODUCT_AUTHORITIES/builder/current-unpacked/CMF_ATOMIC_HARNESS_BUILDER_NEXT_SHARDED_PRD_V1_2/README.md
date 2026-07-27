# CMF Atomic Harness Builder Next — Sharded PRD Package V1.2

**Status:** `draft_for_review`  
**Version:** `0.3.0-draft`  
**Created:** 2026-07-13

This package converts the completed 33-question Grill-me session, the approved Builder Workflow Runtime delta, and the binding Activative Intelligence constitutional alignment into a CMF-governed sharded PRD.

## Package facts

- **33** locked product decisions
- **18** behavioral feature shards
- **210** globally stable Functional Requirements
- **53** cross-cutting Non-Functional Requirements
- **14** operator and downstream user journeys
- **5** canonical format categories
- **3** explicit compilation targets
- **22** binding anti-goals

## Constitutional amendment

The binding [`Builder V1.2 Constitutional Alignment Amendment`](amendments/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md) adds the Conversational Activation / Human Expression category and restores the complete runtime semantic chain while preserving the validated Builder architecture.

## Start here

1. [`prd/index.md`](prd/index.md) — sharded PRD index
2. [`prd/PRD_COMBINED.md`](prd/PRD_COMBINED.md) — single-file reading view
3. [`governance/DECISION_REGISTER.md`](governance/DECISION_REGISTER.md) — all 33 decisions
4. [`governance/REQUIREMENTS_REGISTRY.yaml`](governance/REQUIREMENTS_REGISTRY.yaml) — machine-readable FR/NFR registry
5. [`governance/TRACEABILITY_MATRIX.csv`](governance/TRACEABILITY_MATRIX.csv) — requirements, decisions, journeys, and features
6. [`validation/PRD_VALIDATION_REPORT.md`](validation/PRD_VALIDATION_REPORT.md) — package validation result
7. [`handoff/ARCHITECTURE_HANDOFF.md`](handoff/ARCHITECTURE_HANDOFF.md) — required next phase

## Documentation boundary

The main PRD defines **what the product must do and what success means**. Technical choices and detailed mechanisms are captured as Architecture handoff or addendum material. Epics and Stories are intentionally not authored yet; BMAD-style planning begins only after approved Architecture and, for the Control Tower, a UX contract.

## Rebuild and validate

```bash
python scripts/rebuild_combined_prd.py
python scripts/validate_prd_package.py
```

The generated validation reports are authoritative only for this package version and file set.
