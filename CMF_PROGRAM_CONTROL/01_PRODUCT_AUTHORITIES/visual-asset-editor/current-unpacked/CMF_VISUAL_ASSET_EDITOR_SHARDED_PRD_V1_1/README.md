# CMF Visual Asset Editor — Sharded PRD Package V1.1

**Status:** `draft_for_review`  
**Version:** `0.2.0-draft`  
**Created:** 2026-07-13

This package converts the completed 28-question Grill-me product planning session into a BMAD-informed, CMF-governed sharded Product Requirements Document for the independently versioned CMF Visual Asset Editor.

## Package facts

- **28** locked product decisions
- **22** behavioral feature shards
- **176** globally stable Functional Requirements
- **70** cross-cutting Non-Functional Requirements
- **16** user and system journeys
- **8** canonical asset families
- **6** selectable Budget Programs
- **1** production reference path: Format 02 — Minimal Coach Theatre

## Constitutional amendment

The binding [`VAE V1.1 Activative Visual Contract Amendment`](amendments/VAE_V1_1_ACTIVATIVE_VISUAL_CONTRACT_AMENDMENT.md) expands the Visual Asset Demand and evaluation system so the editor receives constitution-complete visual intelligence rather than reconstructing it from a generic prompt.

## Start here

1. [`prd/index.md`](prd/index.md) — sharded PRD index
2. [`prd/PRD_COMBINED.md`](prd/PRD_COMBINED.md) — combined reading view
3. [`governance/DECISION_REGISTER.md`](governance/DECISION_REGISTER.md) — all 28 decisions
4. [`governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`](governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml) — frozen upstream architecture
5. [`governance/REQUIREMENTS_REGISTRY.yaml`](governance/REQUIREMENTS_REGISTRY.yaml) — machine-readable FR/NFR registry
6. [`reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/README.md`](reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/README.md) — Release 1 reference path
7. [`validation/PRD_VALIDATION_REPORT.md`](validation/PRD_VALIDATION_REPORT.md) — mechanical validation
8. [`handoff/ARCHITECTURE_HANDOFF.md`](handoff/ARCHITECTURE_HANDOFF.md) — authorized next phase

## Documentation boundary

The PRD specifies **what the product must do, what it must preserve, and how success is measured**. It does not finalize technical implementation, cloud vendor, database, orchestration framework, API transport, or ComfyUI node topology. Those choices belong to Architecture and feature technical specifications.

The approved PRD authorizes Architecture work only. Implementation requires the formal Visual Asset Editor Implementation Authorization Gate.

## Rebuild and validate

```bash
python scripts/rebuild_combined_prd.py
python scripts/validate_prd_package.py
```
