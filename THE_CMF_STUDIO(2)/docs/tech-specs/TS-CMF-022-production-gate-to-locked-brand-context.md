---
tech_spec_id: "TS-CMF-022"
title: "Production Gate to Locked Brand Context"
story_id: "4.5"
story_title: "Production Gate to Locked Brand Context"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-4-5-production-gate-to-locked-brand-context.md"
fr_ids:
  - "FR-CMF-04.07"
pipeline_stage: "9 / 10"
entry_object: "production job request"
exit_object: "allowed or blocked SceneSpec compile"
validation_contract: "locked brand context"
required_receipt: "brand context gate receipt"
runtime_target: "Python / Pydantic v2 / CompleteEditingSessionWorkflow / SceneSpecCompiler / provider receipts"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-022: Production Gate to Locked Brand Context

**Status:** Ready for Development  
**Story:** `4.5 - Production Gate to Locked Brand Context`  
**Implementation Boundary:** Complete Editing Session brand-context gate, SceneSpec asset selection validation, provider receipt lineage, and review context lineage view.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority that render jobs only accept locked Brand Context version hash. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-04.07 source authority and downstream context gate requirements. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Complete Editing Session, active Brand Context, render board, and locked context doctrine. |
| `docs/architecture.md` | Architecture authority for CompleteEditingSessionWorkflow, SceneSpecCompiler, provider receipts, and review lineage. |
| `docs/cmf-studio-pipeline-map.md` | Stage 9 and 10 production gate trace. |
| `docs/migration/legacy-inventory.md` | Legacy CMF lineage doctrine as source context. |
| `docs/stories/story-4-5-production-gate-to-locked-brand-context.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-021-brand-context-version-locking-and-forking.md` | Brand Context lock/fork dependency. |

## 2. Overview

### Problem Statement

Brand Genesis only protects production if every production job is forced to use an approved, locked, brand-scoped context. SceneSpecs, provider jobs, and review surfaces must prove which Brand Context Version and asset hashes shaped the render.

### Solution

Implement a production gate in CompleteEditingSessionWorkflow, SceneSpec compilation, provider request construction, and review context lineage. A production job fails if Brand Context is missing, unlocked, stale without explicit decision, or cross-brand. Every selected acting reference, prop, anchor, motion recipe, SFX asset, caption rule, and visual constraint must belong to the locked version.

### Scope

In scope:

- `BrandContextGateResult`, `SceneSpecBrandContextBinding`, `SelectedBrandAssetRef`, and `BrandContextLineageView`.
- Complete Editing Session creation gate.
- SceneSpec selection validation.
- Superseded-context revision decision.
- Provider receipt inclusion of Brand Context ID and selected asset hashes.
- Reviewer lineage view.

Out of scope:

- Full SceneSpec content model.
- Provider adapter execution internals.
- Full review UI design.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-04.07 | System prevents production jobs from using unapproved, unlocked, stale, or cross-brand identity assets. | Brand Context gate, SceneSpec selection validation, provider receipt lineage, superseded-context decision, and review lineage view. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `9 - Complete Editing Session`; `10 - Scene planning and composition control` |
| Entry Object | Production job request |
| Exit Object | Allowed or blocked SceneSpec compile |
| Allowed Actors / Services | Production Steward, CompleteEditingSessionWorkflow, SceneSpecCompiler, ProviderRouteService, ReviewService |
| Validation Contract | Locked Brand Context |
| Required Receipt | Brand context gate receipt |
| Forbidden Shortcut | SceneSpec without locked context, selected asset outside version, provider job without context ID/hash, blind stale-version revision |

### Legacy Intelligence Mapping

Legacy CMF lineage doctrine and Brand Genesis V3 production rules inform this gate. Production must retrieve and compose from the approved Brand Context; it must not reinvent the brand or use provider outputs as new identity truth.

Target modules:

- `ccp_studio.contracts.brand_context_gate`
- `ccp_studio.services.brand_context_gate_service`
- `ccp_studio.workflows.complete_editing_session`
- `ccp_studio.services.scene_spec_compiler`
- `ccp_studio.services.provider_request_builder`
- `ccp_studio.services.review_lineage_service`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `BrandContextGateResult` | Allow/block state with version/hash and blocker reason. |
| `SceneSpecBrandContextBinding` | SceneSpec reference to locked context and selected assets. |
| `SelectedBrandAssetRef` | Acting reference, prop, anchor, motion, SFX, caption rule, or visual constraint selected from locked context. |
| `SupersededContextDecision` | Preserve original context or fork into new approved context for revisions. |
| `BrandContextLineageView` | Reviewer-facing view of locked creative universe behind render. |

## 4. Implementation Plan

### Workstream A: Gate Contracts

Define gate result, context binding, selected asset ref, superseded decision, and lineage view contracts.

### Workstream B: Complete Editing Session Gate

Block session creation when Brand Context Version is missing, unlocked, cross-brand, or stale without explicit decision.

### Workstream C: SceneSpec Selection Validation

Validate that selected acting references, props, anchors, motion recipes, SFX, caption rules, and constraints belong to the locked version.

### Workstream D: Provider Receipt Lineage

Provider request builder must include Brand Context Version ID, version hash, and selected asset hashes.

### Workstream E: Review Lineage View

ReviewService exposes the locked creative universe behind any render.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class BrandContextGateStatus(str, Enum):
    allowed = "allowed"
    blocked = "blocked"
    decision_required = "decision_required"


class SelectedBrandAssetRef(BaseModel):
    schema_version: Literal["cmf.selected_brand_asset_ref.v1"]
    asset_type: str
    asset_id: UUID
    asset_hash: str
    brand_context_version_id: UUID


class BrandContextGateResult(BaseModel):
    schema_version: Literal["cmf.brand_context_gate_result.v1"]
    brand_context_gate_result_id: UUID
    organization_id: UUID
    brand_id: UUID
    requested_brand_context_version_id: UUID | None
    status: BrandContextGateStatus
    decision_code: str
    selected_asset_refs: list[SelectedBrandAssetRef] = Field(default_factory=list)


class SceneSpecBrandContextBinding(BaseModel):
    schema_version: Literal["cmf.scene_spec_brand_context_binding.v1"]
    scene_spec_id: UUID
    brand_context_version_id: UUID
    brand_context_version_hash: str
    selected_asset_refs: list[SelectedBrandAssetRef]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `ValidateProductionBrandContextCommand`, `BindSceneSpecToBrandContextCommand`, `SelectBrandAssetCommand`, `RecordSupersededContextDecisionCommand`, `GenerateBrandContextLineageViewCommand` |
| Events | `BrandContextGatePassed`, `BrandContextGateBlocked`, `SceneSpecBoundToBrandContext`, `ProviderRequestBoundToBrandContext`, `BrandContextLineageViewed` |
| Workflows | Complete Editing Session gate workflow, SceneSpec compile workflow, provider request construction workflow |
| Receipts | `BrandContextGateReceipt`, `ProviderReceipt`, `ReviewEvidenceReceipt` |

## 7. Backward Compatibility and Migration Fallback

Any production job created before Brand Context gate enforcement cannot move to rendering until rebound to a locked context or blocked for repair. Legacy CMF assets can be selected only if included in a locked Brand Context Version.

Fallback behavior:

- Missing context returns `BRAND_CONTEXT_REQUIRED`.
- Unlocked context returns `BRAND_CONTEXT_NOT_LOCKED`.
- Asset outside version returns `BRAND_ASSET_NOT_IN_CONTEXT`.
- Superseded context returns `BRAND_CONTEXT_DECISION_REQUIRED`.
- Provider receipt missing context returns `PROVIDER_BRAND_CONTEXT_LINEAGE_REQUIRED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Production wants flexible asset selection; brand consistency requires strict retrieval from locked context. |
| UX / Ops Failure Scenario | A provider job uses a fresh prop or acting reference outside the locked context, causing style drift that reviewers cannot trace. |
| Resolution Demand | Locked Brand Context gate takes precedence. Every SceneSpec and provider request must carry version and selected asset hashes. |
| Downstream Proof | Tests must prove missing/unlocked/cross-brand context fails, selected assets must belong to version, provider receipts include version/hash, and reviewers can open lineage. |

## 9. Tasks

- Define gate contracts.
- Implement Complete Editing Session gate.
- Implement SceneSpec selection validation.
- Add superseded-context decision command.
- Add provider request binding.
- Add review lineage view.
- Add tests for context and asset selection blockers.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Complete Editing Session fails when Brand Context Version is missing or unlocked. | Session starts with draft context. |
| AC2 | SceneSpec selections all belong to locked version. | SceneSpec selects anchor outside context. |
| AC3 | Revision of old scene asks preserve original or fork into new context. | Revision silently uses latest context. |
| AC4 | Provider receipts include Brand Context Version ID and selected asset hashes. | Provider receipt has prompt only. |
| AC5 | Reviewer can inspect locked creative universe behind render. | Review shows final asset with no context lineage. |

## 11. Dependencies

Internal:

- TS-CMF-021 Brand Context locking/forking
- TS-CMF-019 Acting library
- TS-CMF-020 Creative libraries
- TS-CMF-002 Orchestration records

External:

- Pydantic v2
- PostgreSQL
- Provider adapters
- Review service

## 12. Testing Strategy

Unit tests:

- Gate status decisions.
- Selected asset membership.
- Superseded-context decision.
- Provider receipt required fields.

Integration tests:

- Block missing context.
- Block unlocked context.
- Bind SceneSpec to context.
- Build provider request with context lineage.
- Generate review lineage view.

Safety tests:

- Cross-brand context fails.
- Provider job cannot run without context ID/hash.
- SceneSpec compiler cannot create identity assets outside context.

## 13. Observability, Recovery, and Rollback

- Logs include `brand_context_version_id`, `scene_spec_id`, `provider_job_id`, selected asset hashes, and gate decision.
- Metrics track allowed gates, blocked gates, stale decisions, provider lineage failures, and review lineage opens.
- Recovery can revalidate SceneSpec against stored Brand Context Version.
- Rollback uses revision/fork command; it does not mutate context references.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-04.07 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - CMF lineage doctrine and Brand Genesis V3 as source |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python gate in workflow; Pi cannot bypass locked context |
| TypeScript Boundary | Review/UI consume lineage contracts only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

