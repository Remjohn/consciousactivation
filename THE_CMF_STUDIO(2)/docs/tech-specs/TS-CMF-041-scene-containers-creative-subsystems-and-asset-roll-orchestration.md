---
tech_spec_id: "TS-CMF-041"
title: "Scene Containers, Creative Subsystems, and Asset Roll Orchestration"
story_id: "7.6"
story_title: "Scene Containers, Creative Subsystems, and Asset Roll Orchestration"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-7-6-scene-containers-creative-subsystems-and-asset-roll-orchestration.md"
fr_ids:
  - "FR-CMF-07.09"
pipeline_stage: "9 / 10"
entry_object: "scene intent"
exit_object: "scene container/component/subsystem/asset-roll plan"
validation_contract: "CMF scene orchestration gate"
required_receipt: "scene intelligence receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / DSPy / registry services"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-041: Scene Containers, Creative Subsystems, and Asset Roll Orchestration

**Status:** Ready for Development  
**Story:** `7.6 - Scene Containers, Creative Subsystems, and Asset Roll Orchestration`  
**Implementation Boundary:** Scene container plans, scene component selections, creative subsystem gate decisions, A/B/C/D/E-roll asset role planning, scene intelligence receipts, and reconstruction links.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-7-6-scene-containers-creative-subsystems-and-asset-roll-orchestration.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-07.09 authority and scene orchestration acceptance criteria. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | CMF intentional orchestration, scene containers/components/subsystems, and asset engines. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | CMF creative harness, SceneSpec, composition, layers, and render branches. |
| `docs/architecture.md` | Scene intelligence rule and asset roll rule. |
| `docs/cmf-studio-pipeline-map.md` | Scene, composition, and asset sub-workflow. |
| `docs/migration/legacy-inventory.md` | 34 Creative Subsystems, CMF references, scene intelligence, asset hunting, and registry migration. |

## 2. Overview

Implement scene intelligence so a SceneSpec can explain the perceptual and narrative job it performs. The system must select a biological arc container before selecting a cinematic component; then it records creative subsystem gate decisions and A/B/C/D/E-roll asset roles with narrative, emotional, explanatory, authentic, or cultural function.

This spec preserves the intentional orchestration of legacy CMF modules. Scene containers, components, creative subsystems, and asset rolls are not decorative labels. They explain why the scene exists, what role each visual/audio asset plays, and how the scene can be reconstructed or revised later.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.09 | Preserve CMF scene-container, scene-component, creative-subsystem, and asset-roll decisions inside SceneSpec and Complete Editing Session lineage. | `SceneContainerPlan`, `SceneComponentSelection`, `CreativeSubsystemDecision`, `AssetRollPlan`, scene intelligence validator, and receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 9 / 10 - SceneSpec and composition planning |
| Entry Object | scene intent |
| Exit Object | scene container/component/subsystem/asset-roll plan |
| Validation Contract | CMF scene orchestration gate |
| Required Receipt | scene intelligence receipt |

### Legacy Intelligence Mapping

- CMF Master Scene Intelligence, Creative Subsystems, Scene Containers, Scene Components, and Conscious Asset Strategy Guide are priority legacy orchestration sources.
- Asset rolls are intentional roles: A-Roll narrative/emotional anchor, B-Roll cinematic/emotional layer, C-Roll visual explanation layer, D-Roll authentic lived-reality layer, E-Roll cultural/status/pattern-interrupt layer.
- Migrated registries are required before production decisions can reference old subsystem names.

## 4. Implementation Plan

1. Add contracts for `SceneContainerPlan`, `SceneComponentSelection`, `CreativeSubsystemDecision`, `AssetRollPlan`, `AssetRollItem`, and `SceneIntelligenceReceipt`.
2. Implement `SceneIntelligenceService` that consumes source expression, route, SceneSpec intent, Brand Context Version, and migrated scene registries.
3. Require biological arc container selection before component selection.
4. Record constraints satisfied/violated for each component.
5. Record creative subsystem gate decisions when relevant.
6. Attach asset roll plan to SceneSpec, CompositionJob, assembly manifests, and reconstruction audit view.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class BiologicalArcContainer(str, Enum):
    HOOK = "hook"
    SETUP = "setup"
    CHALLENGE = "challenge"
    TURNING_POINT = "turning_point"
    RESOLUTION = "resolution"
    VISION = "vision"


class AssetRollRole(str, Enum):
    A_ROLL = "a_roll"
    B_ROLL = "b_roll"
    C_ROLL = "c_roll"
    D_ROLL = "d_roll"
    E_ROLL = "e_roll"


class SceneContainerPlan(BaseModel):
    scene_container_plan_id: str
    scene_spec_id: str
    container: BiologicalArcContainer
    source_expression_moment_id: str
    selection_rationale: str
    constraints: list[str]


class SceneComponentSelection(BaseModel):
    scene_component_selection_id: str
    scene_container_plan_id: str
    component_registry_ref: str
    valid_for_container: bool
    satisfied_constraints: list[str]
    violated_constraints: list[str] = []


class CreativeSubsystemDecision(BaseModel):
    creative_subsystem_decision_id: str
    subsystem_registry_ref: str
    decision: str
    rationale: str
    evidence_refs: list[str]


class AssetRollItem(BaseModel):
    asset_roll_item_id: str
    role: AssetRollRole
    asset_ref: str | None = None
    function: str
    source_or_license_state: str
    rationale: str


class AssetRollPlan(BaseModel):
    asset_roll_plan_id: str
    scene_spec_id: str
    items: list[AssetRollItem] = Field(min_length=1)
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `SelectSceneContainerCommand`, `SelectSceneComponentCommand`, `EvaluateCreativeSubsystemGatesCommand`, `CompileAssetRollPlanCommand`, `ValidateSceneOrchestrationCommand`, `WriteSceneIntelligenceReceiptCommand` |
| Events | `SceneContainerSelected`, `SceneComponentSelected`, `CreativeSubsystemGatesEvaluated`, `AssetRollPlanCompiled`, `SceneOrchestrationValidated`, `SceneIntelligenceReceiptWritten` |
| Workflow | `CompleteEditingSessionWorkflow.stage9_10_scene_intelligence` |
| Receipt | `SceneIntelligenceReceipt` with container, component, subsystem decisions, asset roll roles, registry versions, evidence refs, and validation result |

## 7. Backward Compatibility and Migration Fallback

Legacy scene containers/components/subsystems must be migrated into registries before production use. If a registry ref is missing, the compiler can mark a decision as unresolved for review, but cannot use it as an approved production decision.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Visual style vs. narrative job | Container selection precedes component selection. | SceneSpec shows container rationale and component fit. |
| Legacy subsystem richness vs. prompt sprawl | Subsystem gates are typed registry decisions. | Scene intelligence receipt lists gate refs and decisions. |
| Asset abundance vs. function | Every A/B/C/D/E-roll item has a role and rationale. | Assembly plan carries asset roll function and source/license state. |

## 9. Tasks

- Add scene intelligence contracts and persistence.
- Implement registry-backed SceneIntelligenceService.
- Add container-before-component validator.
- Add creative subsystem gate evaluator.
- Add asset roll planner and validation.
- Add audit view integration.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Scene selects biological arc container before cinematic component. | Component chosen with no HOOK/SETUP/etc. context. |
| AC2 | Component records validity and constraints. | Scene uses visual effect with no reason. |
| AC3 | Relevant subsystem gates are recorded. | First-frame imprint or silence container is implicit only. |
| AC4 | Asset roll items carry function and source/license status. | B-roll is just a stock URL. |
| AC5 | Reconstruction resolves source, route, container, component, gates, asset rolls, sonic plan, CompositionJob, manifests, approvals. | Reviewer cannot explain why scene feels this way. |

## 11. Dependencies

- TS-CMF-017 intentional orchestration migration.
- TS-CMF-037 SceneSpec compilation.
- TS-CMF-038 CompositionJob lineage.
- TS-CMF-039 assembly plans.
- TS-CMF-014 registry conversion.

## 12. Testing Strategy


Unit tests:

- Unit tests for scene container/component/subsystem/asset roll contracts.
- Registry validation tests for migrated scene intelligence refs.
- Validator tests requiring container before component.
- Asset roll tests for role/function/source-license completeness.
- Reconstruction tests proving scene intelligence fields appear in audit view.

Integration tests:

- Workflow test from `scene intent` to `scene container/component/subsystem/asset-roll plan` through pipeline stage `9 / 10`.
- Command Bus test proving `scene intelligence receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for unresolved registry refs, invalid component/container pairs, subsystem gate failures, asset roll gaps, and audit reconstruction misses.
- Logs include SceneSpec ID, registry bundle version, container, component, subsystem refs, and asset roll plan ID.
- Recovery: re-run scene intelligence with migrated registry refs or revised SceneSpec intent.
- Rollback: supersede scene intelligence receipt and invalidate dependent composition/assembly drafts.

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
| Tech Spec ID | TS-CMF-041 |
| Story | 7.6 |
| Requirement Trace | FR-CMF-07.09 |
| Pipeline Trace | Stages 9 / 10, scene intent to scene container/component/subsystem/asset-roll plan |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No decorative-only scene labels, no unmigrated registry production use, no asset bucket without function |

