---
tech_spec_id: "TS-CMF-049"
title: "SVRE, Aurore, and Asset Research Engine Routing"
story_id: "8.8"
story_title: "SVRE, Aurore, and Asset Research Engine Routing"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-8-svre-aurore-and-asset-research-engine-routing.md"
fr_ids:
  - "FR-CMF-08.08"
pipeline_stage: "11"
entry_object: "VisualResearchQuery"
exit_object: "AssetResearchManifest, ImageResolutionMap"
validation_contract: "license/provenance/asset-roll gate"
required_receipt: "asset research receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / DSPy / provider adapters / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-049: SVRE, Aurore, and Asset Research Engine Routing

**Status:** Ready for Development  
**Story:** `8.8 - SVRE, Aurore, and Asset Research Engine Routing`  
**Implementation Boundary:** VisualResearchQuery, VisualCandidate, AssetResearchManifest, ImageResolutionMap, LicensingDecision, asset-roll routing, SVRE/Aurore migration, and asset research receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-8-svre-aurore-and-asset-research-engine-routing.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.08 authority and SVRE/Aurore constraints. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | SVRE/Aurore, asset engines, licensing, and asset-roll doctrine. |
| `docs/architecture.md` | Visual and asset research rule and core objects. |
| `docs/cmf-studio-pipeline-map.md` | Stage 10/11 asset research provider sub-workflow. |
| `docs/migration/legacy-inventory.md` | Sovereign Visual Research Engine, Aurore, asset hunting, and CMF asset engine references. |

## 2. Overview

Migrate SVRE/Aurore-style visual research into governed CMF STUDIO contracts. Visual research starts from a SceneSpec and asset-roll intent, then retrieves or proposes visual candidates with emotional mode, symbolic role, contradiction value, cultural proximity, source quality, brand alignment, licensing, provenance, and direct-use/composition-reference state.

The asset research engine is not a background reference. It produces typed manifests, scoring receipts, license decisions, selected/rejected reasons, and downstream render route links.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.08 | Migrate and adapt SVRE/Aurore and legacy asset-research logic into governed VisualResearchQuery, AssetResearchManifest, ImageResolutionMap, licensing, scoring, and candidate-selection contracts. | Research query, candidate scoring, licensing decision, usable/reference state, manifest, image resolution map, and receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 11 - Asset research and provider jobs |
| Entry Object | `VisualResearchQuery` |
| Exit Object | `AssetResearchManifest`, `ImageResolutionMap` |
| Validation Contract | license/provenance/asset-roll gate |
| Required Receipt | asset research receipt |

### Legacy Intelligence Mapping

- SVRE/Aurore concepts map into Pydantic query/candidate/scoring/licensing objects.
- SearXNG-style categories, source search, T-Score-like scoring, known-person validity, licensing tiers, source win-rate logic, and visual candidate ranking become fixtures/evals and typed fields.
- Superseded execution services are context only; current provider adapters perform execution.

## 4. Implementation Plan

1. Add contracts for `VisualResearchQuery`, `VisualCandidate`, `VisualCandidateScore`, `LicensingDecision`, `AssetResearchManifest`, and `ImageResolutionMap`.
2. Implement `AssetResearchService` with DSPy scoring and provider/search adapter boundaries.
3. Validate source URL/reference, license tier, provenance, brand alignment, known-person validity when relevant, and asset-roll fit.
4. Distinguish direct-use assets from composition-reference-only assets.
5. Attach manifest and image resolution map to RenderContract and AssetRollPlan.
6. Write asset research receipt with selected and rejected candidate reasons.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class CandidateUseMode(str, Enum):
    DIRECT_USE = "direct_use"
    COMPOSITION_REFERENCE_ONLY = "composition_reference_only"
    BLOCKED = "blocked"


class VisualResearchQuery(BaseModel):
    visual_research_query_id: str
    scene_spec_id: str
    asset_roll_role: str
    emotional_state: str
    symbolic_role: str
    contradiction_value: str | None = None
    brand_alignment_constraints: list[str]
    source_constraints: list[str]
    licensing_requirements: list[str]


class VisualCandidate(BaseModel):
    visual_candidate_id: str
    query_id: str
    source_url_or_ref: str
    candidate_uri: str | None = None
    provenance_summary: str
    use_mode: CandidateUseMode
    license_decision_id: str
    score_id: str


class VisualCandidateScore(BaseModel):
    score_id: str
    emotional_mode_match: float = Field(ge=0, le=1)
    cultural_proximity: float = Field(ge=0, le=1)
    symbolic_role_fit: float = Field(ge=0, le=1)
    authenticity: float = Field(ge=0, le=1)
    source_quality: float = Field(ge=0, le=1)
    brand_alignment: float = Field(ge=0, le=1)
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CreateVisualResearchQueryCommand`, `RunAssetResearchCommand`, `ScoreVisualCandidateCommand`, `RecordLicensingDecisionCommand`, `SelectVisualCandidateCommand`, `WriteAssetResearchManifestCommand` |
| Events | `VisualResearchQueryCreated`, `AssetResearchRunCompleted`, `VisualCandidateScored`, `LicensingDecisionRecorded`, `VisualCandidateSelected`, `AssetResearchManifestWritten` |
| Workflow | `ProviderJobWorkflow.stage11_asset_research` |
| Receipt | `AssetResearchReceipt` with query ID, candidate set, scores, license decisions, selected/rejected reasons, manifest ID, and image resolution map ID |

## 7. Backward Compatibility and Migration Fallback

SVRE/Aurore legacy logic becomes scoring fixtures, adapter specs, and eval targets. It cannot call old execution services as live dependencies. If a candidate lacks license/provenance, it is blocked or composition-reference-only according to policy.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Visual richness vs. rights/provenance | License/provenance gate required before selection. | Manifest stores license decision and source ref. |
| Found asset vs. brand truth | Candidate scoring includes brand alignment and asset-roll role. | RenderContract links selected candidate and use mode. |
| Legacy engine value vs. provider drift | SVRE/Aurore logic migrates into contracts/evals. | Receipt lists scoring fields and adapter route. |

## 9. Tasks

- Add visual research contracts and persistence.
- Implement asset research service and scoring program.
- Add license/provenance validator.
- Add direct-use/reference-only routing.
- Add manifest and image map writer.
- Add render/asset-roll integration.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Query includes scene, roll, emotion, symbolic role, contradiction, brand, source, license. | Query is just keywords. |
| AC2 | Candidates scored across emotional, cultural, symbolic, authenticity, source, brand fit. | Candidate selected because it "looks cool." |
| AC3 | Unlicensed candidate cannot direct-use. | Found image enters final render with no license. |
| AC4 | Superseded execution logic is adapted to current providers. | Legacy asset engine is called directly. |
| AC5 | Manifest/map links selected candidate, alternatives, scores, license, source, render route. | Render uses asset with no selected/rejected reason. |

## 11. Dependencies

- TS-CMF-041 scene intelligence and asset-roll plan.
- TS-CMF-042 provider capability registry.
- TS-CMF-044 generative provider adapters.
- TS-CMF-046 worker asset migration.

## 12. Testing Strategy


Unit tests:

- Unit tests for query/candidate/score/license schemas.
- Scoring tests with known-person validity and cultural proximity fixtures.
- License/provenance block tests.
- Direct-use/reference-only routing tests.
- RenderContract integration tests.

Integration tests:

- Workflow test from `VisualResearchQuery` to `AssetResearchManifest, ImageResolutionMap` through pipeline stage `11`.
- Command Bus test proving `asset research receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for research queries, candidates scored, license blocks, selected/rejected candidates, and reference-only selections.
- Logs include query ID, candidate ID, source ref, score ID, license decision, and manifest ID.
- Recovery: rerun research with revised constraints or license requirements.
- Rollback: supersede manifest and invalidate dependent asset selections/render drafts.

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
| Tech Spec ID | TS-CMF-049 |
| Story | 8.8 |
| Requirement Trace | FR-CMF-08.08 |
| Pipeline Trace | Stage 11, VisualResearchQuery to AssetResearchManifest/ImageResolutionMap |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No old execution-service calls, no unlicensed direct use, no asset research as vague inspiration |

