---
tech_spec_id: "TS-CMF-037"
title: "SceneSpec, Creative State, and Render Contract Compilation"
story_id: "7.2"
story_title: "SceneSpec, Creative State, and Render Contract Compilation"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-7-2-scenespec-creative-state-and-render-contract-compilation.md"
fr_ids:
  - "FR-CMF-07.02"
pipeline_stage: "9"
entry_object: "editing session"
exit_object: "SceneSpec, CreativeState, RenderContract"
validation_contract: "asset/variant/revision validation"
required_receipt: "SceneSpec receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-037: SceneSpec, Creative State, and Render Contract Compilation

**Status:** Ready for Development  
**Story:** `7.2 - SceneSpec, Creative State, and Render Contract Compilation`  
**Implementation Boundary:** SceneSpec compilation, Creative State initialization, Render Contract compilation, asset selection, platform variants, evaluation requirements, revision policy, and SceneSpec receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-7-2-scenespec-creative-state-and-render-contract-compilation.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-07.02 authority and tech-spec required contracts. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative State, SceneSpec, RenderContract, and render routing doctrine. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | SceneSpec and render contract as reproducibility requirements. |
| `docs/architecture.md` | Core object list, Stage 9, and renderer props rule. |
| `docs/cmf-studio-pipeline-map.md` | Complete Editing Session and SceneSpec sub-workflow. |
| `docs/migration/legacy-inventory.md` | CMF engine references, creative subsystems, and render manifest references. |

## 2. Overview

Compile `SceneSpec`, `CreativeState`, and `RenderContract` from a Complete Editing Session. The compiler must include asset selections, renderer route options, evaluation requirements, platform variants, and revision policy. Selected assets must come from the locked Brand Context Version or approved source/provider outputs.

The Creative State is the evolving state object for the job. Every stage reads and writes to it so the workflow does not fracture into unrelated prompts, files, or provider outputs.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.02 | Compile SceneSpecs, Creative State, Render Contracts, asset selections, renderer routes, evaluation requirements, platform variants, and revision policies. | Pydantic contracts, compiler commands, asset/variant/revision validation, receipt, and workflow guard. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 9 - Complete Editing Session |
| Entry Object | editing session |
| Exit Object | `SceneSpec`, `CreativeState`, `RenderContract` |
| Validation Contract | asset/variant/revision validation |
| Required Receipt | SceneSpec receipt |

### Legacy Intelligence Mapping

- Creative Pipeline V2 defines SceneSpec as the core creative source of truth.
- Creative State prevents fragmented prompts/files/model outputs.
- Legacy CMF engine manifests inform render contract and receipt fields.

## 4. Implementation Plan

1. Add contracts for `SceneSpec`, `CreativeState`, `RenderContract`, `AssetSelection`, `PlatformVariant`, `EvaluationRequirement`, and `RevisionPolicy`.
2. Implement `SceneSpecCompiler` DSPy/Pydantic pipeline.
3. Validate selected assets against locked Brand Context Version and approved source lineage.
4. Validate platform variants for captions, aspect ratio, negative space, and text plan.
5. Require revision policy before provider or renderer jobs are queued.
6. Emit `SceneSpecCompiled` and `SceneSpecReceipt`.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class CreativeStateStage(str, Enum):
    CREATED = "created"
    SCENE_SPEC_VALIDATED = "scene_spec_validated"
    COMPOSITION_REQUESTED = "composition_requested"
    RENDER_CONTRACT_READY = "render_contract_ready"
    EVALUATED = "evaluated"


class SceneSubjectSpec(BaseModel):
    identity_asset_ref: str
    emotion: str
    gesture: str
    position: str
    text_space: str | None = None


class SceneSpec(BaseModel):
    scene_spec_id: str
    complete_editing_session_id: str
    format: str
    aspect_ratio: str
    duration_seconds: float
    content_type: str
    visual_style: str
    platform_targets: list[str]
    message_role: str
    emotional_intent: str
    subject: SceneSubjectSpec
    composition_requirements: dict
    negative_constraints: dict
    source_expression_moment_id: str
    asset_route_receipt_id: str
    brand_context_version_id: str


class RenderContract(BaseModel):
    render_contract_id: str
    scene_spec_id: str
    renderer_route: str
    platform_variants: list[str]
    selected_asset_ids: list[str]
    evaluation_requirement_ids: list[str]
    revision_policy_id: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileSceneSpecCommand`, `InitializeCreativeStateCommand`, `CompileRenderContractCommand`, `ValidateSceneAssetsCommand`, `ValidatePlatformVariantsCommand`, `BlockProviderQueueWithoutRevisionPolicyCommand` |
| Events | `SceneSpecCompiled`, `CreativeStateInitialized`, `RenderContractCompiled`, `SceneAssetsValidated`, `PlatformVariantsValidated`, `SceneSpecCompilationBlocked` |
| Workflow | `CompleteEditingSessionWorkflow.stage9_compile_scene_spec` |
| Receipt | `SceneSpecReceipt` with session ID, source expression, route, Brand Context Version, input hashes, selected asset hashes, platform variants, and revision policy |

## 7. Backward Compatibility and Migration Fallback

Legacy scene specs and render manifests inform fixtures and contract fields only. Renderer props must originate from Pydantic contracts, not hand-authored TypeScript or hidden template strings.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Creative freedom vs. brand lock | Selected assets validate against locked Brand Context Version. | SceneSpecReceipt stores asset hashes and context hash. |
| Platform fit vs. visual drift | Platform variant constraints are explicit in RenderContract. | Renderer receives aspect/text/caption constraints from contract. |
| Provider speed vs. revision audit | Revision policy required before queue. | Provider jobs include revision policy ID. |

## 9. Tasks

- Add SceneSpec, CreativeState, RenderContract, and supporting contracts.
- Implement compiler and validators.
- Add receipt writer.
- Add command handlers and API endpoints.
- Add blocked state for missing revision policy.
- Add contract tests for renderer props generation.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Compilation emits SceneSpec, CreativeState, RenderContract, assets, variants, eval requirements, revision policy. | Render starts from only a prompt and route label. |
| AC2 | Unapproved brand assets fail validation. | Draft prop from another context is selected. |
| AC3 | Caption/negative-space constraints are explicit. | Vertical variant has no text-space rule. |
| AC4 | Missing revision policy blocks provider queue. | Provider job runs with no revision boundary. |
| AC5 | Receipt references source, route, brand context, input hashes. | SceneSpec cannot trace to source moment. |

## 11. Dependencies

- TS-CMF-036 Complete Editing Session creation.
- TS-CMF-021 Brand Context version lock.
- TS-CMF-020 creative libraries.
- TS-CMF-033 route receipts.
- TS-CMF-034 package specs.

## 12. Testing Strategy


Unit tests:

- Unit tests for SceneSpec/CreativeState/RenderContract schemas.
- Compiler tests from fixture editing sessions.
- Brand Context asset validation tests.
- Platform variant constraint tests.
- Workflow blocker tests for missing revision policy.

Integration tests:

- Workflow test from `editing session` to `SceneSpec, CreativeState, RenderContract` through pipeline stage `9`.
- Command Bus test proving `SceneSpec receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for SceneSpec compile success, asset validation failures, variant failures, and missing revision-policy blocks.
- Logs include session ID, SceneSpec ID, render contract ID, brand context hash, and selected asset hashes.
- Recovery: recompile SceneSpec with corrected assets or variants.
- Rollback: supersede SceneSpec and invalidate dependent composition/render jobs.

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
| Tech Spec ID | TS-CMF-037 |
| Story | 7.2 |
| Requirement Trace | FR-CMF-07.02 |
| Pipeline Trace | Stage 9, editing session to SceneSpec/CreativeState/RenderContract |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No prompt-only render contract, no unapproved brand assets, no hidden renderer props |

