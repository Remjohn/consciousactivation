---
tech_spec_id: "TS-CMF-092"
title: "Composition Eval Fixtures and Operator Approval Workbench"
story_id: "9.10"
story_title: "Composition Eval and Approval Workbench"
epic_id: 9
epic_title: "Evaluation, Review, Approval, Publishing, and Memory"
status: "ready-for-development"
created_at: "2026-06-24"
updated_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition and protocol repair"
pipeline_stage: "10 / 11 / 12 / 13"
entry_object: "CompositionRuntimeBinding, RendererPreview, FrameSequenceManifest, EvaluationReceipt"
exit_object: "CompositionEvalSuiteRun, OperatorApprovalDecision, ApprovalBlocker, ReviewReadModel"
validation_contract: "doctrine eval, primitive triad, route feel, golden fixtures, visual/semantic/source approval"
required_receipt: "CompositionOperatorApprovalReceipt"
runtime_target: "Python / Pydantic v2 / eval harness / PWA read model / Telegram quick review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-092: Composition Eval Fixtures and Operator Approval Workbench

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines mandatory spec sections, CBAR enforcement, and acceptance criteria structure. |
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Identifies missing visual eval harness, operator workbench, and protocol-level acceptance gates. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Requires evidence-rich review, approval blockers, evaluation receipts, reconstruction, and traceability. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Establishes doctrine-driven eval harness and primitive coverage obligations. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Defines primitive triad requirements, hard failure codes, route primitives, and applicable target objects. |
| `THE CMF STUDIO/registries/evals/doctrine/cmf_papercut_rig_doctrine_eval.v1.json` | Defines paper-cut rig doctrine eval, threshold, hard failures, and required evidence routes. |
| `THE CMF STUDIO/src/ccp_studio/contracts/doctrine_evals.py` | Existing doctrine eval contract family. |
| `THE CMF STUDIO/src/ccp_studio/services/doctrine_evaluation_service.py` | Existing service owner for doctrine scoring and failure behavior. |
| `THE CMF STUDIO/src/ccp_studio/contracts/doctrine_tests.py` | Existing doctrine test harness contract family. |
| `THE CMF STUDIO/src/ccp_studio/services/doctrine_test_harness.py` | Existing service owner for doctrine test execution. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Composition runtime objects under review. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Renderer previews, props, and output manifests under review. |

## 2. Overview

The Composition Eval and Approval Workbench is the visible quality gate for CMF scenes, templates, and rendered previews. It must prove that an output is not generic slop, not disconnected from the interview, not missing Brand Genesis, not breaking doctrine, and not bypassing the primitive standards Emilio built.

The workbench has two responsibilities:

1. Run doctrine and primitive evals on production targets.
2. Show operators enough evidence to approve, repair, or block the composition.

This includes visual previews, source transcript refs, Brand Context refs, template family, asset code, renderer props hash, primitive triad, doctrine scores, hard blockers, and repair instructions.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-092-001 | `EvalTargetSelection` | Selects exact object under review: SceneSpec, CompositionJob, runtime binding, preview, frame sequence, or render output. |
| DEP-CMF-092-002 | `EvaluationReceipt` | Records eval family, score, threshold, evidence refs, and blockers. |
| DEP-CMF-092-003 | `CompositionPrimitiveTriadEval` | Enforces minimum three primitives and required role coverage. |
| DEP-CMF-092-004 | `DoctrineEvalSuiteRun` | Runs doctrine family checks including paper-cut rig and composition route feel. |
| DEP-CMF-092-005 | `ApprovalBlocker` | Converts hard failures into operator-visible repair blockers. |
| DEP-CMF-092-006 | `ReviewReadModel` | Provides evidence-rich UI state for PWA and Telegram review. |
| DEP-CMF-092-007 | `CompositionOperatorApprovalReceipt` | Records approval, rejection, repair, or escalation decision. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `doctrine_evals.py` | Add composition eval target and receipt refs where missing. |
| `doctrine_evaluation_service.py` | Execute primitive and doctrine evals against selected targets. |
| `doctrine_tests.py` | Register positive and negative fixture suites. |
| `doctrine_test_harness.py` | Run fixtures in CI and local audit mode. |
| `composition.py` | Provide target objects, source refs, route, template, and asset refs. |
| `deterministic_rendering.py` | Provide props hashes, preview refs, frame sequence refs, and render output refs. |
| `approval blockers specs` | Connect hard failures to workflow blocking and repair commands. |

### ADR-05 Primitives

The workbench MUST make primitive validation visible, not hidden in logs.

Required display:

| Display Field | Requirement |
|---|---|
| `minimum_validated_primitives` | Must show count and pass/fail status. |
| `required_roles` | Must show meaning transform, delivery shape, and format material coverage. |
| `primitive_evidence_refs` | Must link each primitive to source, composition, or visual evidence. |
| `route_primitive_set` | Must show route-specific allowed primitive set. |
| `hard_failure_codes` | Must show exact primitive failure code if blocked. |

Applicable hard failures include `COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET`, `COMPOSITION_PRIMITIVE_ROLE_COVERAGE_MISSING`, `COMPOSITION_GENERIC_PREMIUM_SOCIAL_SLOP`, `COMPOSITION_ROUTE_FEEL_COLLAPSED`, and `COMPOSITION_DOCTRINE_CONFLICT`.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Approval is blocked until eval target, source lineage, Brand Context, and primitive triad pass. |
| Phase4-M02 Cinematic Meaning | Workbench displays the declared meaning job of beats, visuals, and motion. |
| Phase4-M04 Frictionless Block | Operators can review and repair, but cannot approve blocked outputs. |
| Phase4-M05 Actionable Rejection | Every blocker includes failed rule, object ref, evidence ref, and repair command. |
| Phase5-M01 Verifiable Artifact | Approval receipt records target hashes, eval receipt refs, and operator decision. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Use eval target selection before running suites. | Prevents vague evals against "the scene" without object precision. |
| Keep negative fixtures mandatory. | CMF must prove it catches cheap or generic outputs. |
| Treat approval blockers as product objects. | Operators need repair workflow, not a passive score. |
| Use the same read model for PWA and Telegram. | Review parity matters across desktop and quick review. |
| Store eval receipts before approval. | Approval must be traceable, reconstructable, and auditable. |

## 4. Implementation Plan

1. Add `EvalTargetSelection`, `CompositionEvalSuiteRun`, `ApprovalBlocker`, `ReviewReadModel`, and `CompositionOperatorApprovalReceipt` contracts.
2. Register composition eval suites for source lineage, Brand Genesis substrate, primitive triad, route feel, visual quality, identity/consent, micro-semiotic integrity, paper-cut doctrine, renderer compatibility, and timing.
3. Add golden positive fixtures for all four canonical video formats.
4. Add mandatory negative fixtures for no Expression Moment, no locked Brand Context, no rig, no primitive triad, route feel collapse, flat paper-cut image, unsafe open-source component, and preview/final drift.
5. Implement eval target selection API and run command.
6. Build review read model with visual preview, source refs, primitive triad, doctrine score, blocker list, and repair commands.
7. Connect approval blockers to render/publish gates.
8. Add CI command that runs eval fixtures before build acceptance.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class EvalTargetSelection(BaseModel):
    schema_version: Literal["cmf.eval_target_selection.v1"]
    target_selection_id: UUID
    workspace_id: UUID
    target_type: Literal[
        "scene_spec",
        "composition_job",
        "composition_runtime_binding",
        "paper_cut_runtime_manifest",
        "renderer_props_manifest",
        "frame_sequence_manifest",
        "renderer_preview",
        "render_output",
    ]
    target_id: UUID
    target_hash: str
    required_eval_family_refs: list[str]


class ApprovalBlocker(BaseModel):
    schema_version: Literal["cmf.approval_blocker.v1"]
    blocker_id: UUID
    blocker_code: str
    severity: Literal["hard", "repair_required", "warning"]
    failed_rule_ref: str
    failed_object_ref: str
    evidence_ref: str | None = None
    repair_command_ref: str | None = None
    operator_message: str


class CompositionEvalSuiteRun(BaseModel):
    schema_version: Literal["cmf.composition_eval_suite_run.v1"]
    suite_run_id: UUID
    target_selection_id: UUID
    eval_receipt_refs: list[str]
    primitive_eval_receipt_ref: str
    doctrine_eval_receipt_refs: list[str]
    blockers: list[ApprovalBlocker]
    decision: Literal["pass", "blocked", "needs_repair"]


class ReviewReadModel(BaseModel):
    schema_version: Literal["cmf.review_read_model.v1"]
    review_id: UUID
    workspace_id: UUID
    complete_editing_session_id: UUID
    target_selection_id: UUID
    visual_preview_ref: str
    source_quote_ref: str
    transcript_segment_refs: list[str]
    brand_context_ref: str
    asset_code: str
    route_code: str
    format_code: str
    primitive_role_map: dict[str, list[str]]
    eval_receipt_refs: list[str]
    blockers: list[ApprovalBlocker]
    available_decisions: list[Literal["approve", "request_repair", "reject", "escalate"]]


class CompositionOperatorApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.composition_operator_approval_receipt.v1"]
    receipt_id: UUID
    review_id: UUID
    operator_id: UUID
    decision: Literal["approved", "repair_requested", "rejected", "escalated"]
    target_hash: str
    eval_receipt_refs: list[str]
    blocker_codes: list[str]
    approved_for_render: bool
    approved_for_publish: bool
```

## 6. Backward Compatibility Fallback

Existing review screens may display preview artifacts, but they cannot approve outputs unless this workbench has a valid eval suite run and approval receipt. During migration, a manual operator note may accompany a repair request, but it cannot override hard blockers.

| Condition | Fallback |
|---|---|
| Eval target missing | Block with `EVAL_TARGET_SELECTION_REQUIRED`. |
| Primitive registry unavailable | Block approval with `PRIMITIVE_REGISTRY_UNAVAILABLE`. |
| Visual preview unavailable | Permit data-only inspection but block approval with `VISUAL_PREVIEW_REQUIRED`. |
| Telegram quick review lacks full evidence | Allow repair request only, not final approval. |
| Legacy output has no target hash | Block with `APPROVAL_TARGET_HASH_MISSING`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T092-01 | Add eval target, suite run, blocker, read model, and approval receipt contracts. |
| T092-02 | Register composition eval families and required target types. |
| T092-03 | Implement eval target selection and eval run command. |
| T092-04 | Implement primitive triad visibility and blocker mapping. |
| T092-05 | Implement doctrine score visibility and paper-cut hard failure handling. |
| T092-06 | Build PWA review read model and UI route. |
| T092-07 | Build Telegram quick review read model with limited decisions. |
| T092-08 | Add golden positive fixtures for four canonical formats. |
| T092-09 | Add negative fixtures proving generic, ungrounded, and doctrine-breaking outputs fail. |
| T092-10 | Wire hard blockers into render, approval, and publishing gates. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC092-01 | Approval cannot happen without an explicit eval target selection. | Operator approves an unnamed preview image. | Phase4-M01 |
| AC092-02 | Workbench displays primitive count, roles, evidence, and failure codes. | UI shows "good style" but no primitive IDs. | Phase4-M01 |
| AC092-03 | Negative fixtures catch flat paper-cut, missing rig, missing source, and route-feel collapse. | Generic premium social poster passes as `SV-EDU`. | Phase4-M04 |
| AC092-04 | Hard blockers disable approval but allow repair request. | Operator approves a render with `COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET`. | Phase4-M04 |
| AC092-05 | Every blocker includes failed rule, object ref, evidence ref, and repair command when available. | Workbench says "doctrine failed" with no repair path. | Phase4-M05 |
| AC092-06 | Approval receipt includes target hash and eval receipt refs. | Later audit cannot prove what was approved. | Phase5-M01 |
| AC092-07 | PWA and Telegram review use the same read model constraints. | Telegram approves output missing evidence available in PWA. | Phase5-M01 |
| AC092-08 | Render and publish workflows reject unapproved or blocked targets. | Publish intent can be created for a blocked composition. | Phase4-M01 |

## 9. Dependencies

| Dependency | Owner Spec |
|---|---|
| Doctrine test harness | `TS-CMF-077` |
| Four video format runtime | `TS-CMF-078` |
| Route-specific visual feel | `TS-CMF-079` |
| Composition runtime binding | `TS-CMF-080` |
| Template family registry | `TS-CMF-081` |
| Beat map compiler | `TS-CMF-084` |
| Paper-cut runtime | `TS-CMF-086` |
| Renderer prop compiler | `TS-CMF-090` |
| Headless frame renderer | `TS-CMF-094` |
| Approval blockers | `TS-CMF-053` |
| Evidence review surface | `TS-CMF-051`, `TS-CMF-055` |

## 10. Testing Strategy

| Test | Required Evidence |
|---|---|
| Contract tests | Eval target, suite run, blocker, read model, and approval receipt schemas. |
| Registry tests | Primitive triad and paper-cut doctrine eval registries load and validate required targets. |
| Positive fixture tests | Four canonical video formats pass when source, brand, primitives, doctrine, timing, and preview evidence are valid. |
| Negative fixture tests | Missing source, missing Brand Context, flat paper-cut, no rig, no primitive triad, generic route feel, and preview/final drift fail. |
| UI tests | Workbench displays visual preview, source quote, primitive triad, doctrine score, blockers, and decisions. |
| Telegram tests | Quick review cannot approve when required evidence is hidden or missing. |
| Gate tests | Render and publish commands refuse targets without approved receipt. |
| Regression tests | Existing doctrine evaluation and deterministic rendering tests remain passing. |

