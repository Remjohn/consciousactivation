---
tech_spec_id: "TS-CMF-105"
title: "Single Image Eval, Review, and Golden Fixture Runtime"
story_id: "7.27F"
story_title: "Single Image Quality Gates and Review"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-099 decomposition after audit"
pipeline_stage: "12 / 13"
entry_object: "SingleImageSceneSpecV2, SkiaRenderReceipt, SingleImageRegistryBundle"
exit_object: "SingleImageEvaluationReceiptV2, SingleImageReviewReadModel, SingleImageProductionRecord"
validation_contract: "rubric threshold, hard failures, primitive compliance, source fidelity, brand consistency, operator blockers, golden fixtures, approval receipt"
required_receipt: "SingleImageEvaluationReceiptV2"
runtime_target: "Python / Eval Registry / PWA Review / Telegram Quick Review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-105: Single Image Eval, Review, and Golden Fixture Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Umbrella eval/review requirements. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md` | Render receipt dependency. |
| `THE CMF STUDIO/registries/evals/composition/single_image_eval_rubrics.v2.json` | Global and family-specific eval rubrics. |
| `THE CMF STUDIO/registries/composition/evidence/single_image_examples.v2.json` | Golden routing examples. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Operator review workbench dependency. |

## 2. Overview

This spec owns the final quality gates for single-image outputs. It prevents attractive but incorrect visuals from passing as complete work. Evaluation must check hard failures, primitives, source fidelity, brand consistency, composition hierarchy, legibility, and platform fit before operator approval.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-105-001 | `SkiaRenderReceipt` | Supplies output hashes and scene spec proof. |
| DEP-CMF-105-002 | `single_image_eval_rubrics.v2.json` | Supplies thresholds, hard failures, and profiles. |
| DEP-CMF-105-003 | `SingleImageEvaluationReceiptV2` | Stores scores, hard failures, repairs, and approval blockers. |
| DEP-CMF-105-004 | `SingleImageReviewReadModel` | Exposes source, candidate, render, eval, repair, and approval evidence. |
| DEP-CMF-105-005 | `SingleImageProductionRecord` | Final audit record. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Runs primitive and doctrine checks. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | Persists single-image eval receipts. |
| `src/ccp_studio/services/approval_gate_service.py` | Blocks approval on hard failures. |
| `src/ccp_studio/services/review_workbench_service.py` | Exposes PWA/Telegram read model. |

### ADR-05 Primitives

Eval must verify role coverage, not only count primitive refs. A scene with three primitives all describing aesthetics fails because it lacks meaning and delivery roles.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase3-M02 Per-Slide Feedback | Review shows scores, blockers, repairs, source evidence, and alternatives. |
| Phase4-M01 Intelligence-Gated Intercept | Eval blocks missing primitive, source, or brand evidence. |
| Phase4-M05 Actionable Rejection | Every failure returns repair action. |
| Phase5-M01 Verifiable Artifact | Production record binds input, route, scene, render, eval, and approval. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Visual eval cannot approve. | Human operator approval remains required. |
| Golden fixtures cover all families. | Prevents SuperVisuals from being tested only as quote cards. |
| Hard failures override aggregate score. | Source or identity violations cannot be averaged away. |

## 4. Implementation Plan

1. Add single-image eval runner.
2. Load family-specific eval profile.
3. Run hard-fail checks.
4. Run primitive role coverage check.
5. Run source fidelity checks for quotes, stats, screenshots, and identity assets.
6. Generate suggested repairs.
7. Project review read model.
8. Block approval until operator resolves or rejects.
9. Add golden fixtures for all eight families and all included examples.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SingleImageReviewReadModel(BaseModel):
    schema_version: Literal["cmf.single_image_review_read_model.v1"]
    review_id: UUID
    content_asset_code: str
    selected_composition_id: str
    candidate_summary: list[dict]
    source_evidence_refs: list[str]
    render_preview_uri: str
    eval_receipt_id: UUID
    hard_failures: list[str] = Field(default_factory=list)
    suggested_repairs: list[dict] = Field(default_factory=list)
    approval_blocked: bool
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Eval profile missing | Block with `SINGLE_IMAGE_EVAL_PROFILE_UNKNOWN`. |
| Hard failure present | Block approval regardless of score. |
| Review read model incomplete | Block with `SINGLE_IMAGE_REVIEW_EVIDENCE_INCOMPLETE`. |
| Operator approval missing | Block publishing intent. |

## 7. Tasks

| Task | Requirement |
|---|---|
| T105-01 | Add eval runner and receipt service integration. |
| T105-02 | Add review read model. |
| T105-03 | Add approval blocker integration. |
| T105-04 | Add golden fixtures for all eight families and five example routes. |
| T105-05 | Add negative fixtures for hard failures and missing review evidence. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR |
|---|---|---|---|
| AC105-01 | Hard failures block approval regardless of score. | Identity mismatch passes because composition is attractive. | Phase4-M05 |
| AC105-02 | Review shows source, route, candidates, render, eval, and repairs. | Operator sees only a thumbnail. | Phase3-M02 |
| AC105-03 | Fixtures cover all eight composition families. | Only quote cards are tested. | Phase5-M01 |
| AC105-04 | Production record binds every required receipt. | Published asset cannot prove registry or render hash. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Render binding | `TS-CMF-104` |
| Eval receipts | `TS-CMF-050` |
| Approval blockers | `TS-CMF-053` |
| Operator workbench | `TS-CMF-092` |

## 10. Testing Strategy

- Global rubric threshold tests.
- Hard-failure override tests.
- Primitive role coverage tests.
- Source fidelity tests.
- PWA and Telegram review read model parity tests.
- Golden fixtures for assertion, documentary, comparison, cartoon moral, cartoon framework, conceptual metaphor, sports collage, promo live.
