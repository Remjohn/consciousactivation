# CMF TS-120..132 ERA3 Protocol Revision Receipt

Date: 2026-06-25
Status: revised and protocol-checked for implementation specification readiness

## Scope

This receipt records the full ERA3 protocol rewrite of TS-CMF-120 through TS-CMF-132, covering the CMF-native OpenMontage-inspired production orchestration adapter layer. The revision upgrades the earlier architectural-reference spec set into implementation-grade CMF/ERA3 specs with explicit backend ownership, primitive gates, CBAR mandates, schemas, fallback behavior, acceptance failure examples, dependencies, and testing strategies.

## Protocol Sources Read

| Source | Use |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section tech spec structure, existing-backend mapping, CBAR mandate enforcement, primitive gates, and testability requirements. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md` | Current ERA3-compatible spec model for sequence programs, composition handoff, and acceptance criteria. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Current ERA3-compatible model for visual rendering, provider routing, primitive gates, and deterministic output receipts. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Feature requirement source for FR-CMF-13.01 through FR-CMF-13.13. |

## Revised Tech Specs

| Requirement | Revised Spec |
|---|---|
| FR-CMF-13.01 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-120-openmontage-reference-adapter-governance.md` |
| FR-CMF-13.02 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-121-production-pipeline-manifest-registry.md` |
| FR-CMF-13.03 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-122-stage-director-skill-contract-binding.md` |
| FR-CMF-13.04 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-123-capability-tool-registry-and-provider-menu.md` |
| FR-CMF-13.05 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-124-scored-provider-selector-and-capability-router.md` |
| FR-CMF-13.06 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-125-brand-scoped-project-workspace-and-checkpoint-runtime.md` |
| FR-CMF-13.07 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-126-reference-video-and-existing-footage-intake-adapter.md` |
| FR-CMF-13.08 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-127-real-footage-corpus-and-source-media-retrieval-adapter.md` |
| FR-CMF-13.09 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-128-render-runtime-selection-and-locking.md` |
| FR-CMF-13.10 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-129-pre-compose-delivery-promise-and-slideshow-risk-gate.md` |
| FR-CMF-13.11 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-130-post-render-self-review-and-media-qa-gate.md` |
| FR-CMF-13.12 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-131-budget-cost-and-resource-governance.md` |
| FR-CMF-13.13 | `THE CMF STUDIO/docs/tech-specs/TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` |

## Revision Actions

| Area | Repair Applied |
|---|---|
| ERA3 section structure | All 13 specs now use the mandatory 10-section shape: Files Read, Overview, Context for Development, Implementation Plan, Primary Output Schema, Backward Compatibility Fallback, Tasks, Acceptance Criteria, Dependencies, and Testing Strategy. |
| Context for Development | Each spec now includes Architecture Traceability, Existing Backend Integration, ADR-05 Primitives, CBAR Mandate Enforcement, and Technical Decisions. |
| Backend ownership | Each spec names concrete CMF service owners, registry locations, probable database tables, API routes, and test files instead of describing abstract architecture only. |
| Legacy/source traceability | Each spec now explicitly names the canonical CMF source documents: Greenfield Python/DSPy/Pi runtime, domain contracts/state machines, CCP V9, CCP V9.1, Brand Genesis V3, Creative Pipeline V2, and `PROJECT_STRUCTURE.md`. |
| API and persistence specificity | Each Existing Backend Integration table now includes exact `/api/v1/` route targets and exact Postgres table targets. |
| Schemas | Each spec now defines a primary Pydantic-style output contract with stable IDs, foreign-key relationships, verdict fields, receipt fields, and blocking semantics. |
| Acceptance criteria | Acceptance criteria now include failure examples and CBAR / test evidence columns so violations are auditable before implementation. |
| Primitive compliance | Specs require at least three relevant primitive or doctrine gates where the stage materially affects composition quality, source grounding, brand fit, delivery fidelity, or approval readiness. |
| Open-source boundary | TS-CMF-120 explicitly blocks unapproved AGPL runtime imports and routes OpenMontage patterns through CMF-native adapters only. |
| Operator workflow | Specs bind approvals, waivers, checkpoints, review read models, provider menus, budget evidence, render locks, and QA receipts to the current CMF operator pipeline. |

## Validation Evidence

| Check | Command / Evidence | Result |
|---|---|---|
| Target spec count | `rg --files "THE CMF STUDIO\\docs\\tech-specs" | rg "TS-CMF-12[0-9]|TS-CMF-13[0-2]"` | 13 target specs present. |
| Mandatory section protocol | PowerShell section scan for all 10 ERA3 headings plus backend, primitive, CBAR, failure example, and test-evidence markers | `CHECKED_FILES=13` |
| Forbidden drift terms | `rg -n -i -g "TS-CMF-12*.md" -g "TS-CMF-13*.md" "newsletter|mvp|flux/kontext|running" "THE CMF STUDIO\\docs\\tech-specs"` | No matches. |
| Provider naming correction | `rg -n -g "TS-CMF-12*.md" -g "TS-CMF-13*.md" "GPT Image" "THE CMF STUDIO\\docs\\tech-specs"` | Matches only `GPT Image 2`, paired with Ideogram 4, Flux 2 Klein 9b, Qwen layered, SAM3, ComfyUI, Remotion, and FFmpeg where relevant. |
| Source trace and persistence scan | PowerShell section scan includes `CCP V9`, `CCP V9.1`, `CCP_CMF_Brand_Genesis`, `CCP_Creative_Pipeline_Architecture`, `PROJECT_STRUCTURE`, `Postgres tables:`, and `/api/v1/`. | `CHECKED_FILES=13` |
| Spec depth | `Get-Content ... | Measure-Object -Line` on each revised spec | Each file is 174-190 lines after the audit revision. |

## Build Readiness Result

The revised TS-CMF-120 through TS-CMF-132 set is ready to enter implementation planning. It should be treated as an adapter layer on top of existing CMF services, not as a replacement runtime. Implementation should begin with registries and read models before workflow automation: OpenMontage reference decisions, pipeline manifests, stage director contracts, capability provider menu, scored provider selector, workspace checkpoints, source intake, source retrieval, render runtime locking, promise gates, QA gates, budget governance, and approval protocol.

## Residual Risk

These are specification artifacts only. No Python implementation tests were run in this receipt because the task was to rewrite the specs, not to build the services. Implementation should create or extend the test files named in each spec before accepting runtime behavior as complete.
