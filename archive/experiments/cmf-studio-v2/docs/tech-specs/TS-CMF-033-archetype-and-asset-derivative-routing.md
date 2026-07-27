---
tech_spec_id: "TS-CMF-033"
title: "Archetype and Asset Derivative Routing"
story_id: "6.5"
story_title: "Archetype and Asset Derivative Routing"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-6-5-archetype-and-asset-derivative-routing.md"
fr_ids:
  - "FR-CMF-06.05"
  - "FR-CMF-06.07"
pipeline_stage: "7"
entry_object: "approved Expression Moment"
exit_object: "AssetRouteReceipt"
validation_contract: "registry route and source support"
required_receipt: "routing receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-033: Archetype and Asset Derivative Routing

**Status:** Ready for Development  
**Story:** `6.5 - Archetype and Asset Derivative Routing`  
**Implementation Boundary:** Route selection through migrated registries, source-support validation, unsupported-format rejection, route receipts, and route lineage into package specs.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-6-5-archetype-and-asset-derivative-routing.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-06.05 and FR-CMF-06.07 authority. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Archetype Contract Registry chain and unsupported-format guard. |
| `THE CMF STUDIO/CCP Archetype System Migration Proposition.docx.md` | Five registry architecture and schema decomposition. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Valid format set and explicit newsletter exclusion. |
| `docs/architecture.md` | Stage 7 RoutingService and registry route constraint. |
| `docs/cmf-studio-pipeline-map.md` | Routing and package planning sub-workflow. |
| `docs/migration/legacy-inventory.md` | 96 archetype prompts and 34 creative subsystems as migration sources. |

## 2. Overview

Implement routing from approved Expression Moments through active migrated registries: Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode. Routing cannot use generic social format categories or unsupported outputs. If source expression does not support a requested route, the route is rejected rather than fabricated.

Every accepted or rejected route writes an `AssetRouteReceipt` containing expression moment ID, registry versions, route rationale, evidence, route-fit score, and failure alternatives.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.05 | Route approved Expression Moments through Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode registries. | `ArchetypeRoute`, registry query service, route selection program, and route receipt. |
| FR-CMF-06.07 | Reject unsupported formats and never treat newsletters as CMF deliverables. | Unsupported-format guard, registry-only validation, and rejection receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 7 - Archetype and asset routing |
| Entry Object | approved Expression Moment |
| Exit Object | `AssetRouteReceipt` |
| Validation Contract | registry route and source support |
| Required Receipt | routing receipt |

### Legacy Intelligence Mapping

- Old monolithic prompts become modular schemas, not direct generation prompts.
- The five registries define meaning, packaging, meme mechanism, reaction format, and physical render route separately.
- Creative subsystem intelligence can inform route constraints only after registry migration.

## 4. Implementation Plan

1. Add contracts for `ArchetypeRoute`, `RouteSelectionCandidate`, `UnsupportedFormatRejection`, and `AssetRouteReceipt`.
2. Implement `RoutingService` and `RouteSelectionProgram` with registry version inputs.
3. Validate that expression moment is approved, not held, and source-supported for each route.
4. Reject unsupported formats with typed receipt and human-readable reason.
5. Persist accepted and rejected route attempts for downstream package planning and future evals.
6. Expose `/api/v1/expression-moments/{id}/routes`.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class RouteDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED_SOURCE_UNSUPPORTED = "rejected_source_unsupported"
    REJECTED_UNSUPPORTED_FORMAT = "rejected_unsupported_format"
    REVIEW_REQUIRED = "review_required"


class RegistryRouteRefs(BaseModel):
    core_content_archetype_ref: str
    asset_derivative_ref: str | None = None
    meme_mechanism_ref: str | None = None
    reaction_archetype_ref: str | None = None
    cmf_render_mode_ref: str
    registry_bundle_version: str


class ArchetypeRoute(BaseModel):
    archetype_route_id: str
    expression_moment_id: str
    route_refs: RegistryRouteRefs
    source_support_evidence: list[str] = Field(min_length=1)
    route_rationale: str
    route_fit_score: float = Field(ge=0, le=1)
    failure_alternatives: list[str] = []
    decision: RouteDecision


class AssetRouteReceipt(BaseModel):
    asset_route_receipt_id: str
    expression_moment_id: str
    accepted_route_ids: list[str]
    rejected_route_ids: list[str]
    registry_bundle_version: str
    evaluator_summary: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RouteExpressionMomentCommand`, `RejectUnsupportedFormatCommand`, `RejectUnsupportedSourceRouteCommand`, `ApproveArchetypeRouteCommand`, `WriteAssetRouteReceiptCommand` |
| Events | `ExpressionMomentRoutingStarted`, `ArchetypeRouteSelected`, `AssetRouteRejected`, `UnsupportedFormatRejected`, `AssetRouteReceiptWritten` |
| Workflow | `CompleteExpressionSessionWorkflow.stage7_route_expression_moments` |
| Receipt | `AssetRouteReceipt` with expression moment ID, registry refs, route scores, accepted/rejected route IDs, and evaluator state |

## 7. Backward Compatibility and Migration Fallback

Legacy archetype prompts and creative subsystems must be migrated into registries before routing can reference them. A route request for an unmigrated or inactive registry entry receives a rejection receipt.

Unsupported deliverables are rejected with a typed reason and can become negative evidence, but they cannot become package items.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Format ambition vs. source support | Route requires source evidence and route-fit score. | Package item references accepted route receipt. |
| Legacy prompt value vs. monolith risk | Route uses modular registry refs only. | Receipt stores registry bundle version. |
| Customer request vs. valid CMF format | Unsupported formats are blocked. | Rejection receipt exists and package spec excludes item. |

## 9. Tasks

- Add route contracts and persistence.
- Implement registry query service and active bundle validation.
- Implement route selection DSPy program.
- Add unsupported-format guard.
- Add route receipt writer.
- Add tests for accepted, unsupported, and source-insufficient routes.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Routing evaluates only active migrated registry entries. | Route references raw old prompt filename. |
| AC2 | Receipt includes moment ID, route ID, registry versions, evidence, rationale, failures. | Route exists with no registry version. |
| AC3 | Source-insufficient route is rejected. | Weak quote becomes fabricated explainer. |
| AC4 | Unsupported format is blocked. | Non-CMF deliverable becomes package item. |
| AC5 | Route lineage remains attached to package planning. | AssetPackageSpec item lacks route receipt ID. |

## 11. Dependencies

- TS-CMF-014 registry conversion.
- TS-CMF-016 hidden prompt/template gates.
- TS-CMF-027 Interview Asset Contract routes.
- TS-CMF-032 approved Expression Moments.

## 12. Testing Strategy


Unit tests:

- Unit tests for registry refs, route decisions, and receipt schema.
- Registry validation tests for inactive/unmigrated refs.
- DSPy route selection tests with approved Expression Moment fixtures.
- Unsupported-format tests, including explicit newsletter rejection.
- Package planning integration tests.

Integration tests:

- Workflow test from `approved Expression Moment` to `AssetRouteReceipt` through pipeline stage `7`.
- Command Bus test proving `routing receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for route accepted/rejected counts, unsupported format attempts, route-fit score distribution, and registry bundle usage.
- Logs include expression moment ID, registry bundle, route candidate IDs, and evaluator summary.
- Recovery: reroute with newer registry bundle or richer moment evidence.
- Rollback: supersede route receipt and invalidate dependent draft package items.

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
| Tech Spec ID | TS-CMF-033 |
| Story | 6.5 |
| Requirement Trace | FR-CMF-06.05, FR-CMF-06.07 |
| Pipeline Trace | Stage 7, approved Expression Moment to AssetRouteReceipt |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No generic social format routing, no unsupported deliverables, no monolithic legacy prompt execution |

