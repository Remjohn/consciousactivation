# CMF PRD-13 / TS-120..132 OpenMontage Adapter Spec Receipt

Date: 2026-06-25
Status: created and validation-passed for specification readiness

## Scope

This receipt records the CMF-native adaptation of OpenMontage architecture patterns into PRD-CMF-13 and 13 operational tech specs.

## Reference Sources

| Source | Use |
|---|---|
| `https://github.com/calesthio/OpenMontage` | Overall reference repository. |
| OpenMontage `README.md` | Pipeline list, production flow, provider scoring, QA, budget, real-footage path. |
| OpenMontage `AGENT_GUIDE.md` | Rule Zero, provider menu, stage directors, runtime locking, checkpoints, approval protocol. |
| OpenMontage `docs/ARCHITECTURE.md` | Tool registry, pipeline manifests, checkpoint system, artifact schemas, render runtimes. |
| OpenMontage `docs/PROVIDERS.md` | Provider families, local/cloud routes, cost/setup categories. |
| `THE CMF STUDIO/docs/architecture.md` | CMF Python/Pydantic, Command Bus, provider, workflow, receipt, renderer boundaries. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` | Open-source governance boundary. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime, transcript timing, primitive, and brand binding. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md` | ContentSequenceProgram and composition handoff dependency. |

## Created PRD Module

| File | Notes |
|---|---|
| `docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Adds 13 feature requirements, each validated at 160-200 words, and maps them to TS-CMF-120 through TS-CMF-132. |
| `docs/prd/modules/PRD_INDEX.md` | Registers PRD-CMF-13 and FR-CMF-13.01 through FR-CMF-13.13. |

## Created Tech Specs

| Requirement | Tech Spec |
|---|---|
| FR-CMF-13.01 | `TS-CMF-120-openmontage-reference-adapter-governance.md` |
| FR-CMF-13.02 | `TS-CMF-121-production-pipeline-manifest-registry.md` |
| FR-CMF-13.03 | `TS-CMF-122-stage-director-skill-contract-binding.md` |
| FR-CMF-13.04 | `TS-CMF-123-capability-tool-registry-and-provider-menu.md` |
| FR-CMF-13.05 | `TS-CMF-124-scored-provider-selector-and-capability-router.md` |
| FR-CMF-13.06 | `TS-CMF-125-brand-scoped-project-workspace-and-checkpoint-runtime.md` |
| FR-CMF-13.07 | `TS-CMF-126-reference-video-and-existing-footage-intake-adapter.md` |
| FR-CMF-13.08 | `TS-CMF-127-real-footage-corpus-and-source-media-retrieval-adapter.md` |
| FR-CMF-13.09 | `TS-CMF-128-render-runtime-selection-and-locking.md` |
| FR-CMF-13.10 | `TS-CMF-129-pre-compose-delivery-promise-and-slideshow-risk-gate.md` |
| FR-CMF-13.11 | `TS-CMF-130-post-render-self-review-and-media-qa-gate.md` |
| FR-CMF-13.12 | `TS-CMF-131-budget-cost-and-resource-governance.md` |
| FR-CMF-13.13 | `TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` |

## Validation Evidence

| Check | Result |
|---|---|
| FR-CMF-13.01 through FR-CMF-13.13 word count | All 13 feature requirements are within 160-200 words. |
| Tech spec count | 13 files created for TS-CMF-120 through TS-CMF-132. |
| Required sections | All 13 tech specs include Files Read, Overview, Architecture Traceability, Existing Backend Integration, ADR-05 Primitives, CBAR Mandate Enforcement, Acceptance Criteria, and Forbidden Drift Check. |
| PRD index routing | PRD-CMF-13 and all 13 FR routes are registered in `PRD_INDEX.md`. |
| Primitive/CBAR coverage | New specs bind to `EXP-SOC-001`, `EXP-FBK-001`, `EXP-PRG-001`, `EXP-FRC-006`, `EXP-TRS-004`, and Phase4/Phase5 mandates where relevant. |

## Implementation Boundary

These specs operationalize OpenMontage as an architectural reference only. They do not approve copying AGPLv3 code, importing OpenMontage runtime modules, or replacing CMF's Command Bus, Pydantic contracts, provider receipts, primitive evals, review gates, or Brand Context authority.

