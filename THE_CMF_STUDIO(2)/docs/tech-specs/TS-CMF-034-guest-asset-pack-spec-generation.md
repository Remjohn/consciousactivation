---
tech_spec_id: "TS-CMF-034"
title: "Guest Asset Pack Spec Generation"
story_id: "6.6"
story_title: "Guest Asset Pack Spec Generation"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-6-6-guest-asset-pack-spec-generation.md"
fr_ids:
  - "FR-CMF-06.06"
pipeline_stage: "8"
entry_object: "route receipts and offer"
exit_object: "AssetPackageSpec"
validation_contract: "source sufficiency and commercial guardrail"
required_receipt: "package spec receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-034: Guest Asset Pack Spec Generation

**Status:** Ready for Development  
**Story:** `6.6 - Guest Asset Pack Spec Generation`  
**Implementation Boundary:** Trial Guest Asset Pack spec generation, source sufficiency gaps, commercial guardrails, package item lineage, and Complete Editing Session request readiness.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-6-6-guest-asset-pack-spec-generation.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-06.06 authority and pack traceability rules. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Pricing guardrail and trial Guest Asset Pack deliverable standard. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Guest Asset Pack standard, compilation logic, reaction seeds, and handoff object. |
| `THE CMF STUDIO/CCP Archetype System Migration Proposition.docx.md` | Pack compilation through schemas. |
| `docs/architecture.md` | Stage 8 AssetPackageService and no-newsletter format rule. |
| `docs/cmf-studio-pipeline-map.md` | Routing and package planning stage. |
| `docs/migration/legacy-inventory.md` | Archetype prompts and creative subsystems migration context. |

## 2. Overview

Implement `AssetPackageSpec` for trial Guest Asset Packs. When source supports it, the package targets 4 videos, 2 carousels, 2 meme visuals, 2 poll visuals, and 2-3 reaction seeds. Quantity pressure must never fabricate source material. Unsupported or insufficient items become explicit gaps, not invented assets.

Customer-facing content charge language for trial packs is limited to `$29/week`. The package spec consumes accepted route receipts and prepares item-level Complete Editing Session requests with source expression, route, registry, Brand Context requirement, evaluation state, and production readiness.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.06 | Generate Asset Package Specs for trial Guest Asset Packs: 4 videos, 2 carousels, 2 meme visuals, 2 poll visuals, and 2-3 reaction seeds when source supports them. | Package schema, source sufficiency guard, gap handling, trial commercial language, package receipt, and editing-session request readiness. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 8 - Asset package planning |
| Entry Object | route receipts and offer |
| Exit Object | `AssetPackageSpec` |
| Validation Contract | source sufficiency and commercial guardrail |
| Required Receipt | package spec receipt |

### Legacy Intelligence Mapping

- V9.1 pack logic defines target asset classes and reaction seed storage.
- Archetype migration proposition requires pack compilation through schemas rather than random format choice.
- Commercial policy allows only documented trial and monthly content-charge language.

## 4. Implementation Plan

1. Add contracts for `AssetPackageSpec`, `AssetPackageItem`, `PackageGap`, `ReactionSeed`, and `PackageSpecReceipt`.
2. Implement `AssetPackageService` that consumes accepted route receipts and trial entitlement state.
3. Enforce pack target counts as goals only when source supports them.
4. Mark source-sufficiency gaps with required evidence and reason.
5. Attach route receipt, expression moment, registry refs, Brand Context requirement, evaluation state, and production readiness to each item.
6. Emit package spec receipt and downstream Complete Editing Session request candidates.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class PackageItemType(str, Enum):
    SHORT_VIDEO = "short_video"
    CAROUSEL = "carousel"
    MEME_VISUAL = "meme_visual"
    POLL_VISUAL = "poll_visual"
    REACTION_SEED = "reaction_seed"


class PackageItemStatus(str, Enum):
    READY_FOR_EDITING_SESSION = "ready_for_editing_session"
    SOURCE_GAP = "source_gap"
    REVIEW_REQUIRED = "review_required"


class AssetPackageItem(BaseModel):
    package_item_id: str
    item_type: PackageItemType
    expression_moment_id: str | None = None
    asset_route_receipt_id: str | None = None
    registry_refs: list[str] = []
    brand_context_required: bool = True
    evaluation_state: str
    production_readiness: PackageItemStatus
    source_gap_id: str | None = None


class PackageGap(BaseModel):
    package_gap_id: str
    target_item_type: PackageItemType
    reason: str
    missing_source_requirement: str
    route_attempt_receipt_ids: list[str] = []


class AssetPackageSpec(BaseModel):
    asset_package_spec_id: str
    expression_session_id: str
    brand_id: str
    offer_code: str
    customer_facing_price_label: str
    items: list[AssetPackageItem]
    gaps: list[PackageGap] = []
    package_spec_receipt_id: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `GenerateTrialGuestAssetPackSpecCommand`, `EvaluatePackageSourceSufficiencyCommand`, `RecordPackageGapCommand`, `ApproveAssetPackageSpecCommand`, `PrepareEditingSessionRequestsCommand` |
| Events | `AssetPackageSpecGenerated`, `PackageSourceGapRecorded`, `AssetPackageSpecApproved`, `EditingSessionRequestsPrepared` |
| Workflow | `CompleteExpressionSessionWorkflow.stage8_generate_asset_package_spec` |
| Receipt | `PackageSpecReceipt` with route receipt IDs, item/gap counts, offer code, price label, reviewer, and readiness status |

## 7. Backward Compatibility and Migration Fallback

Legacy pack examples and archetype prompts are compilation references only. Asset package items must reference migrated registry routes and approved Expression Moments. If a route registry is missing, create a gap or review-required item; do not create a synthetic deliverable.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Pack target count vs. truth | Counts are targets when source supports them. Gaps are explicit. | Package spec lists items and source gaps separately. |
| Commercial clarity vs. hidden tiers | Trial label is `$29/week`; no other customer-facing trial content tier appears. | Package receipt records offer code and price label. |
| Multi-format output vs. random selection | Items come from accepted route receipts and registries. | Each item has route receipt and registry refs. |

## 9. Tasks

- Add package contracts and tables.
- Implement source sufficiency evaluator.
- Implement trial pack generation service.
- Add package gap recording.
- Add package approval and editing-session request preparation.
- Add tests for price label, target counts, gaps, and route lineage.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Pack targets 4 videos, 2 carousels, 2 meme visuals, 2 poll visuals, 2-3 reaction seeds where supported. | Pack forces missing video from weak source. |
| AC2 | Unsupported source creates gap. | Gap is hidden and item is fabricated. |
| AC3 | Each item maps to moment, route, registry, brand context, evaluation, readiness. | Item lacks expression moment ID. |
| AC4 | Trial pack language uses `$29/week`. | Spec renders another customer-facing content tier. |
| AC5 | Approved package prepares editing session requests with lineage. | Editing request lacks route state. |

## 11. Dependencies

- TS-CMF-006 commercial entitlements.
- TS-CMF-033 route receipts.
- TS-CMF-021 locked Brand Context versions for downstream production.
- TS-CMF-032 approved Expression Moments.

## 12. Testing Strategy


Unit tests:

- Unit tests for package item/gap schema and target item classes.
- Commercial guardrail tests for `$29/week` trial label.
- Source sufficiency tests for gap creation.
- Route lineage tests for every package item.
- Integration tests preparing Complete Editing Session requests.

Integration tests:

- Workflow test from `route receipts and offer` to `AssetPackageSpec` through pipeline stage `8`.
- Command Bus test proving `package spec receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for package item counts, gaps by type, source sufficiency failures, and approval latency.
- Logs include package spec ID, route receipts, offer code, price label, and readiness state.
- Recovery: regenerate package spec after new moments/routes are approved.
- Rollback: supersede package spec and cancel unstarted editing-session requests.

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
| Tech Spec ID | TS-CMF-034 |
| Story | 6.6 |
| Requirement Trace | FR-CMF-06.06 |
| Pipeline Trace | Stage 8, route receipts and offer to AssetPackageSpec |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No fabricated pack items, no unsupported content tiers, no random format choice |

