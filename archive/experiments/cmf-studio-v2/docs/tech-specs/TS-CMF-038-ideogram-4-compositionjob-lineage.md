---
tech_spec_id: "TS-CMF-038"
title: "Ideogram 4 CompositionJob Lineage"
story_id: "7.3"
story_title: "Ideogram 4 CompositionJob Lineage"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-7-3-ideogram-4-compositionjob-lineage.md"
fr_ids:
  - "FR-CMF-07.03"
  - "FR-CMF-07.04"
pipeline_stage: "10"
entry_object: "SceneSpec and Ideogram route"
exit_object: "CompositionJob, plate, analysis"
validation_contract: "text-space and identity boundary"
required_receipt: "composition receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / provider adapters / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-038: Ideogram 4 CompositionJob Lineage

**Status:** Ready for Development  
**Story:** `7.3 - Ideogram 4 CompositionJob Lineage`  
**Implementation Boundary:** Ideogram 4 CompositionJob JSON, prompt hash, constraints, composition plate URI/hash, composition analysis, provider metadata, downstream edit references, final text plan, and composition receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-7-3-ideogram-4-compositionjob-lineage.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-07.03 and FR-CMF-07.04 authority. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Ideogram 4 CompositionJob and scene reproducibility doctrine. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Ideogram role, non-role, input/output contract, and acceptance criteria. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Ideogram as Composition Director and text-layout guidance. |
| `docs/architecture.md` | AD-011 and first-class lineage rule. |
| `docs/cmf-studio-pipeline-map.md` | Stage 10 composition-control sub-workflow. |
| `docs/migration/legacy-inventory.md` | Legacy scene reproducibility, CMF beat-fingerprint, manifest lineage, and asset engine references. |

## 2. Overview

Implement Ideogram 4 as a first-class composition-control provider. It produces composition plates and composition analysis. It is not the final identity renderer and not the canonical final text layer. The structured `CompositionJob` JSON is a key lineage artifact and must be preserved with prompt hash, constraints, output requirements, provider metadata, plate URI/hash, downstream edit references, selected brand layers, final text plan, and approval/evaluation state.

If a plate contains final-looking text or identity drift, the system restricts it to background/composition use, rejects it, or sends it to repair. Final production text is rendered downstream from the approved text plan.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.03 | Preserve Ideogram 4 CompositionJob JSON, prompt hash, plate URI, analysis, provider metadata, downstream edits, selected brand layers, final text plan, evaluation receipts, and approval state. | `CompositionJob`, `CompositionAnalysis`, lineage links, storage, provider receipt, and composition receipt. |
| FR-CMF-07.04 | Treat Ideogram 4 as Composition Director, not final identity renderer or final text authority. | Identity/text boundary validator, restricted-use state, repair/reject handling, and final text plan requirement. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 10 - Scene planning and composition control |
| Entry Object | SceneSpec and Ideogram route |
| Exit Object | `CompositionJob`, plate, analysis |
| Validation Contract | text-space and identity boundary |
| Required Receipt | composition receipt |

### Legacy Intelligence Mapping

- Creative Pipeline V2 defines Ideogram as composition-control engine.
- Brand Genesis V3 clarifies Ideogram designs text layout while final text remains downstream.
- Legacy CMF beat-fingerprint lineage and Ideogram JSON lineage must both be retained.

## 4. Implementation Plan

1. Add contracts for `CompositionJob`, `CompositionConstraints`, `CompositionOutputRequirements`, `CompositionPlate`, `CompositionAnalysis`, `CompositionUsageState`, and `CompositionReceipt`.
2. Implement Ideogram provider adapter behind provider capability records.
3. Compile prompts from SceneSpec and constraints; store prompt hash before provider call.
4. Store plate in object storage and persist output hash, provider metadata, and analysis.
5. Validate text-space, identity boundary, layerability, style, visual flow, and final-text restriction.
6. Link downstream edit jobs and final text-rendering plan to the originating CompositionJob.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel


class CompositionUsageState(str, Enum):
    APPROVED_COMPOSITION_PLATE = "approved_composition_plate"
    BACKGROUND_ONLY = "background_only"
    REPAIR_REQUIRED = "repair_required"
    REJECTED = "rejected"


class CompositionConstraints(BaseModel):
    aspect_ratio: str
    subject_position: str
    text_area: str
    visual_flow: str
    style: str
    micro_semiotic_anchor_ids: list[str] = []


class CompositionJob(BaseModel):
    composition_job_id: str
    complete_editing_session_id: str
    scene_spec_id: str
    provider: str = "ideogram_4"
    purpose: str = "composition_plate"
    compiled_prompt: str
    prompt_hash: str
    constraints: CompositionConstraints
    output_requirements: dict
    provider_correlation_id: str | None = None


class CompositionPlate(BaseModel):
    composition_plate_id: str
    composition_job_id: str
    plate_uri: str
    plate_hash: str
    provider_receipt_id: str
    analysis: dict
    usage_state: CompositionUsageState
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileCompositionJobCommand`, `SubmitIdeogramCompositionJobCommand`, `RecordCompositionPlateCommand`, `EvaluateCompositionBoundaryCommand`, `RestrictCompositionPlateUseCommand`, `LinkDownstreamCompositionEditCommand` |
| Events | `CompositionJobCompiled`, `IdeogramCompositionSubmitted`, `CompositionPlateRecorded`, `CompositionBoundaryEvaluated`, `CompositionPlateUseRestricted`, `DownstreamCompositionEditLinked` |
| Workflow | `CompleteEditingSessionWorkflow.stage10_composition_control` |
| Receipt | `CompositionReceipt` with CompositionJob JSON hash, prompt hash, plate URI/hash, provider receipt, analysis, usage state, and downstream link IDs |

## 7. Backward Compatibility and Migration Fallback

Older composition prompts can become compiler fixtures. Production jobs must use the structured `CompositionJob` contract. A flattened plate without CompositionJob JSON is invalid lineage and cannot enter final render.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Beautiful plate vs. brand truth | Identity boundary validator prevents final identity reliance. | Plate state is background-only, repair, rejected, or approved composition plate. |
| AI text convenience vs. editable final text | Final text plan is stored and rendered downstream. | RenderContract references final text plan, not baked provider text. |
| Composition speed vs. reproducibility | Prompt hash, JSON, provider receipt, plate hash, analysis preserved. | Audit view reconstructs full composition lineage. |

## 9. Tasks

- Add CompositionJob and plate contracts.
- Implement Ideogram adapter and prompt compiler.
- Add object storage path and hash persistence.
- Add composition boundary evaluator.
- Add downstream edit/final text lineage.
- Add tests for text-space, identity drift, and lineage completeness.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Submit stores CompositionJob JSON, prompt hash, constraints, provider metadata, correlation ID. | Provider call stores only output URL. |
| AC2 | Plate stores URI, hash, analysis, provider receipt. | Plate is saved without analysis. |
| AC3 | Final-looking text or identity drift is restricted, rejected, or repaired. | Plate becomes final output with baked text. |
| AC4 | Downstream edits reference originating CompositionJob. | Identity repair cannot trace composition source. |
| AC5 | Audit shows job, hash, plate, analysis, downstream edits, final text plan. | Reviewer sees only thumbnail. |

## 11. Dependencies

- TS-CMF-037 SceneSpec and RenderContract.
- TS-CMF-022 locked Brand Context gate.
- Provider capability records from architecture.
- TS-CMF-020 creative libraries and micro-semiotic anchors.

## 12. Testing Strategy


Unit tests:

- Unit tests for CompositionJob constraints and output requirements.
- Adapter contract tests with mocked provider responses.
- Boundary evaluator tests for missing text space, identity drift, baked text, layerability failure, and style drift.
- Lineage tests proving downstream edit references CompositionJob.
- Storage tests for prompt hash and plate hash.

Integration tests:

- Workflow test from `SceneSpec and Ideogram route` to `CompositionJob, plate, analysis` through pipeline stage `10`.
- Command Bus test proving `composition receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for composition submissions, boundary failures, restricted plates, repair requests, and provider errors.
- Logs include CompositionJob ID, provider correlation ID, prompt hash, plate hash, and usage state.
- Recovery: retry with stricter constraints or route to repair.
- Rollback: mark plate rejected/restricted and invalidate dependent draft edit/render jobs.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-038 |
| Story | 7.3 |
| Requirement Trace | FR-CMF-07.03, FR-CMF-07.04 |
| Pipeline Trace | Stage 10, SceneSpec/Ideogram route to CompositionJob/plate/analysis |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No final identity from Ideogram, no final text authority, no output-URL-only lineage |
