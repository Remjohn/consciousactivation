---
tech_spec_id: "TS-CMF-128"
title: "Render Runtime Selection and Locking"
story_id: "13.9"
story_title: "Render Runtime Selection and Locking"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.09"
pipeline_stage: "composition runtime and render route governance"
entry_object: "RenderRuntimeSelectionRequest"
exit_object: "RenderRuntimeLockReceipt"
validation_contract: "runtime capability, format fit, transcript timing, composition family, provider availability, approval lock, drift detection"
required_receipt: "RenderRuntimeLockReceipt"
runtime_target: "Python / Pydantic v2 / deterministic rendering / Remotion / Motion Canvas / HyperFrames / FFmpeg / ComfyUI / Skia"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-128: Render Runtime Selection and Locking

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Runtime routing, cinematic meaning, and rejection mandates. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.09. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | Existing deterministic render runtime precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime and transcript timing dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-094-headless-2d-frame-renderer-and-avatar-export-worker.md` | 2D character frame renderer dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md` | Skia still render dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Existing deterministic render owner. |
| `THE CMF STUDIO/src/ccp_studio/workflows/render_workflow.py` | Existing render workflow owner. |
| `THE CMF STUDIO/src/ccp_studio/services/composition_service.py` | Composition planning owner. |
| `THE CMF STUDIO/src/ccp_studio/services/scene_spec_compiler.py` | SceneSpec owner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Provider capability owner. |
| `OpenMontage AGENT_GUIDE.md` | Reference rule that runtime choice must be locked and not silently swapped. |

## 2. Overview

CMF must select render runtime as a production decision, not an implementation afterthought. The system must expose the available routes for each composition plan: Remotion, Motion Canvas, HyperFrames, FFmpeg, ComfyUI worker, video generation provider, Skia, headless 2D renderer, or hybrid assembly.

Each route has a different fit. Remotion is strongest for transcript-timed social video and UI overlays. Motion Canvas is strong for precise 2D and explanatory motion. HyperFrames or browser animation can support HTML/GSAP-style kinetic scenes. FFmpeg is strong for deterministic cuts, muxing, and final assembly. ComfyUI and video generation workers create or transform media plates. Skia is deterministic for still outputs. A high-motion Conscious Reactions clip must not degrade into a static slideshow, and a PaperCut explainer must not become flat corporate animation.

Once approved, the selected runtime is written into the render contract, composition handoff, edit decisions, provider receipts, and workspace checkpoint. Silent swaps are forbidden. Runtime drift creates a blocker.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-128-001 | `RenderRuntimeSelectionRequest` | Request tied to format target, SceneSpec, ContentSequenceProgram, transcript timing, assets, and provider menu. |
| DEP-CMF-128-002 | `RenderRuntimeCandidate` | Runtime option with fit score, capability status, quality risks, cost, and constraints. |
| DEP-CMF-128-003 | `RenderRuntimeDecision` | Selected runtime, rejected runtimes, approval requirement, and fallback policy. |
| DEP-CMF-128-004 | `RenderRuntimeLock` | Immutable lock binding runtime to render contract and composition handoff. |
| DEP-CMF-128-005 | `RenderRuntimeLockReceipt` | Receipt proving approved runtime, candidate analysis, and drift detection baseline. |
| DEP-CMF-128-006 | `RenderRuntimeDriftBlocker` | Blocker emitted when approved and executed runtime diverge. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/deterministic_rendering.py` | Add runtime selection request, candidate, decision, lock, drift blocker, and receipt models. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Own runtime candidate scoring, lock creation, and drift check. |
| `src/ccp_studio/workflows/render_workflow.py` | Require runtime lock before render job starts. |
| `src/ccp_studio/services/composition_service.py` | Request runtime selection from composition handoff and SceneSpec. |
| `src/ccp_studio/services/provider_operations_service.py` | Provide runtime capability status from provider menu. |
| `src/ccp_studio/api/v1/renders.py` | Add runtime select, lock, inspect, and drift-check endpoints. |
| `POST /api/v1/renders/runtime/select`, `POST /api/v1/renders/runtime/lock`, `POST /api/v1/renders/runtime/{lock_id}/drift-check`, `GET /api/v1/renders/runtime/{lock_id}` | Exact API routes for runtime selection, locking, and drift inspection. |
| `src/ccp_studio/repositories/deterministic_rendering.py` | Persist runtime locks and receipts. |
| Postgres tables: `render_runtime_candidates`, `render_runtime_selection_receipts`, `render_runtime_locks`, `runtime_drift_events` | Durable storage for runtime scoring, locks, drift evidence, and replayable receipts. |
| `src/ccp_studio/services/review_state_service.py` | Surface runtime decision and fallback risks. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-TRS-004` | Cinematic Meaning | Runtime must fit format feel and composition function. |
| `EXP-PRG-001` | Inline Routing SLA | Runtime resolves before rendering, not during execution. |
| `EXP-FBK-001` | Actionable Rejection | Runtime unavailable or drift returns exact alternative and impact. |
| `EXP-SOC-001` | Verifiable Artifact | Runtime lock is receipt-backed and replayable. |
| `EXP-FRC-006` | Frictionless Block | Fallbacks require approval when quality or format meaning changes. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Candidate scoring blocks runtime choices that flatten the format. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Render workflow requires runtime lock before job start. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Unavailable runtime or drift returns alternatives and quality impact. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Runtime lock and drift baseline write receipts. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Runtime choice is an approval-gated lock. | Prevents silent downgrade and protects operator expectation. |
| Candidate scoring uses composition family and transcript timing. | Runtime fit depends on the actual asset, not general preference. |
| Drift detection compares approved and executed runtime. | Catches accidental implementation swaps. |
| Fallbacks carry quality impact. | Operators can approve informed tradeoffs. |

## 4. Implementation Plan

1. Add render runtime selection contracts.
2. Add runtime capability records under TS-CMF-123 provider menu.
3. Implement candidate scoring for format target, composition family, transcript timing, motion needs, asset state, cost, runtime availability, and primitive fit.
4. Add runtime lock creation with approval status and fallback policy.
5. Require runtime lock in render workflow before job creation.
6. Write runtime refs into render contract, composition handoff, edit decisions, provider receipts, and workspace checkpoint.
7. Add drift check comparing approved runtime and executed runtime.
8. Surface runtime candidates, lock, and fallback risks in review workbench.
9. Add tests for candidate selection, lock, drift, and fallback approval.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class RenderRuntimeCandidate(BaseModel):
    schema_version: Literal["cmf.render_runtime_candidate.v1"]
    runtime_id: str
    runtime_kind: Literal["remotion", "motion_canvas", "hyperframes", "ffmpeg", "comfyui", "video_generation", "skia", "headless_2d", "hybrid"]
    fit_score: float = Field(ge=0, le=1)
    capability_status: Literal["available", "degraded", "blocked", "unavailable"]
    best_for: list[str]
    quality_risks: list[str] = Field(default_factory=list)
    cost_estimate_usd: float | None = None


class RenderRuntimeLock(BaseModel):
    schema_version: Literal["cmf.render_runtime_lock.v1"]
    runtime_lock_id: str
    selection_request_id: str
    selected_runtime_id: str
    approved_by: str
    composition_handoff_id: str
    render_contract_id: str
    fallback_runtime_ids: list[str] = Field(default_factory=list)
    lock_sha256: str


class RenderRuntimeLockReceipt(BaseModel):
    schema_version: Literal["cmf.render_runtime_lock_receipt.v1"]
    receipt_id: str
    runtime_lock_id: str
    candidate_runtime_ids: list[str]
    rejected_reasons: dict[str, str]
    drift_baseline_sha256: str
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing deterministic rendering paths can keep operating for legacy render jobs. New production render jobs require a runtime lock. If the best runtime is unavailable, the system returns a blocker with alternatives and quality impact. Fallback execution requires operator approval when the fallback changes motion, timing precision, composition family, or output quality.

If the system cannot determine runtime fit, it must block for review rather than defaulting to FFmpeg, static images, or a generic renderer.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T128-01 | Contracts | Add runtime request, candidate, decision, lock, blocker, receipt. |
| T128-02 | Provider Menu | Register render runtime capability states. |
| T128-03 | Services | Implement candidate scoring and lock creation. |
| T128-04 | Render Workflow | Require runtime lock before render job. |
| T128-05 | Drift Detection | Compare approved and executed runtime. |
| T128-06 | Review UI | Surface candidates, lock, fallback, and risks. |
| T128-07 | Tests | Add runtime fit, lock, fallback, and drift tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC128-01 | Runtime candidates are scored against format, composition family, timing, assets, and availability. | PaperCut explainer defaults to FFmpeg with no motion capability check. | Phase4-M02; runtime scoring test. |
| AC128-02 | Render workflow requires an approved runtime lock. | Render job starts with no selected runtime. | Phase4-M03; workflow gate test. |
| AC128-03 | Silent runtime swaps are blocked. | Approved Remotion route executes as static FFmpeg slideshow. | Phase4-M05; drift detection test. |
| AC128-04 | Fallbacks include quality impact and approval requirement. | Motion Canvas unavailable, system uses still-image route silently. | Phase4-M05; fallback approval test. |
| AC128-05 | Runtime lock receipt is replayable. | Operator cannot reconstruct why runtime was selected. | Phase5-M01; receipt replay test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-043` | Render precedent | Extend deterministic render routes. |
| `TS-CMF-080` | Composition runtime | Runtime selection consumes composition binding. |
| `TS-CMF-123` | Provider menu | Runtime availability comes from capability state. |
| `deterministic_rendering_service.py` | Existing service | Extend. |
| `render_workflow.py` | Existing workflow | Require lock. |
| `composition_service.py` | Existing service | Request selection. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Runtime candidates, locks, drift blockers, and receipts validate. |
| Scoring tests | Format-specific fixtures select expected runtime families. |
| Workflow tests | Render job creation fails without runtime lock. |
| Drift tests | Executed runtime mismatch blocks final approval. |
| Fallback tests | Quality-impact fallback requires approval. |
| Receipt tests | Runtime lock receipt replays candidates, rejected reasons, chosen runtime, and baseline hash. |
