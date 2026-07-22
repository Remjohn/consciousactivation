---
tech_spec_id: "TS-CMF-130"
title: "Post-Render Self-Review and Media QA Gate"
story_id: "13.11"
story_title: "Post-Render Self-Review and Media QA Gate"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.11"
pipeline_stage: "post-render qa and approval blocking"
entry_object: "RenderedAssetReviewRequest"
exit_object: "PostRenderReviewReceipt"
validation_contract: "media technical QA, delivery promise check, source lineage, brand context, caption/audio, primitive/doctrine, approval blocker"
required_receipt: "PostRenderReviewReceipt"
runtime_target: "Python / Pydantic v2 / render workflow / media probe / image critic / approval gate / review workbench"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-130: Post-Render Self-Review and Media QA Gate

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | QA, rejection, and sonic mandates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact mandate. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.11. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | Existing deterministic render precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Review workbench dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-129-pre-compose-delivery-promise-and-slideshow-risk-gate.md` | Delivery promise dependency. |
| `THE CMF STUDIO/src/ccp_studio/workflows/render_workflow.py` | Existing render workflow owner. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Existing render metadata owner. |
| `THE CMF STUDIO/src/ccp_studio/services/image_critic_service.py` | Existing visual QA/eval owner. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Existing blocker owner. |
| `THE CMF STUDIO/src/ccp_studio/services/review_state_service.py` | Existing review read-model owner. |
| `OpenMontage AGENT_GUIDE.md` | Reference pattern for post-render ffprobe/frame/audio/subtitle review. |

## 2. Overview

Every rendered asset must review itself before an operator can approve it. This spec adds a post-render QA gate that inspects technical media validity, delivery promise fidelity, source lineage, brand context, captions, audio, human cutouts, overlays, platform profile, primitive/doctrine compliance, and final package readiness.

The QA service checks duration, resolution, frame rate, codec, file size, black frames, frozen frames, broken overlays, off-canvas text, caption presence, caption timing, audio silence, clipping, loudness, music ducking, human cutout alignment, render artifacts, brand watermark/logo rules, platform profile compatibility, source lineage, Brand Context Version, Expression Moment binding, primitive triad evidence, doctrine eval receipts, consent compatibility, and composition family rules.

Failures map to repair commands: rerender captions, adjust crop, replace asset, repair audio mix, regenerate layer mask, rerun runtime binding, replace footage, re-evaluate primitive triad, or escalate to human review. A rendered file cannot enter final approval, publishing intent, memory admission, or package sequencing until QA passes or receives explicit waiver where allowed.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-130-001 | `RenderedAssetReviewRequest` | Bundles rendered file, render contract, pre-compose receipt, source refs, platform profile, and eval requirements. |
| DEP-CMF-130-002 | `MediaProbeResult` | Technical media inspection result for video/audio/image. |
| DEP-CMF-130-003 | `DeliveryPromiseQAResult` | Compares final render against pre-compose delivery promise and runtime lock. |
| DEP-CMF-130-004 | `PostRenderRepairCommand` | Actionable repair command for failed QA dimension. |
| DEP-CMF-130-005 | `PostRenderReviewReceipt` | Receipt proving QA scores, blockers, repair commands, waivers, and final eligibility. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/deterministic_rendering.py` | Add rendered asset review request, media probe result, QA dimensions, repair command, and receipt models. |
| `src/ccp_studio/workflows/render_workflow.py` | Run post-render QA immediately after render completion. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Collect technical metadata and render hashes. |
| `src/ccp_studio/services/image_critic_service.py` | Evaluate visual issues, text overlap, frame artifacts, and brand fit. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Validate primitive/doctrine receipts and composition family compliance. |
| `src/ccp_studio/services/approval_gate_service.py` | Block final approval/publishing on QA failure. |
| `src/ccp_studio/services/review_state_service.py` | Surface QA read model and repair commands. |
| `src/ccp_studio/api/v1/renders.py` | Add post-render review and repair endpoints. |
| `POST /api/v1/renders/{render_id}/qa`, `POST /api/v1/renders/{render_id}/repair`, `GET /api/v1/renders/{render_id}/qa` | Exact API routes for rendered asset QA, repair command routing, and inspection. |
| Postgres tables: `post_render_review_receipts`, `media_probe_results`, `media_qa_findings`, `render_repair_commands` | Durable storage for technical QA, visual/audio findings, blockers, and repair decisions. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-FBK-001` | Actionable Rejection | QA failures return exact repair command. |
| `EXP-SOC-001` | Verifiable Artifact | QA receipts store rendered file hash, probe results, and approval eligibility. |
| `EXP-TRS-004` | Cinematic Meaning | Final render must preserve promised composition family and source meaning. |
| `EXP-TRS-003` | Sonic Prestige | Audio loudness, clipping, silence, ducking, and caption timing are checked. |
| `EXP-PRG-001` | Inline Routing SLA | QA runs before final approval/publishing/memory admission. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Delivery promise QA compares final render against planned format. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Final approval, publishing, and package sequencing require QA receipt. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | QA failures produce repair commands. |
| Phase4-M06: Sonic Prestige Rule | Phase 4 Story 6.1 | `EXP-TRS-003` | Audio and captions fail when silence, clipping, loudness, or timing is wrong. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | QA receipt stores file hash and probe evidence. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| QA runs automatically after render. | Operators review evidence, not raw hope. |
| Technical and doctrine QA are separate dimensions. | A file can be technically valid and still creatively/ethically wrong. |
| Repair commands are structured. | Enables automated repair loops and clear human decisions. |
| QA gates final approval and publishing. | Prevents broken media from leaving the factory. |

## 4. Implementation Plan

1. Add post-render QA contracts.
2. Add media probe integration in render workflow for video/audio/image outputs.
3. Add frame sampling, black/frozen frame checks, text bounds, overlay integrity, caption timing, audio loudness, silence, clipping, and platform profile checks.
4. Add delivery promise comparison against pre-compose receipt, runtime lock, SceneSpec, source refs, and primitive/doctrine receipts.
5. Add repair command generation.
6. Add approval gate blockers for QA failure.
7. Add review workbench read model with preview, QA dimensions, blockers, and repair actions.
8. Add tests for each technical and CMF-specific QA dimension.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class MediaProbeResult(BaseModel):
    schema_version: Literal["cmf.media_probe_result.v1"]
    duration_seconds: float | None = None
    width: int | None = None
    height: int | None = None
    frame_rate: float | None = None
    codec: str | None = None
    file_size_bytes: int
    black_frame_count: int = 0
    frozen_frame_segments: list[str] = Field(default_factory=list)
    audio_loudness_lufs: float | None = None
    audio_clipping_detected: bool = False


class PostRenderRepairCommand(BaseModel):
    repair_code: str
    target_ref: str
    reason: str
    command: str
    auto_repair_allowed: bool


class PostRenderReviewReceipt(BaseModel):
    schema_version: Literal["cmf.post_render_review_receipt.v1"]
    receipt_id: str
    rendered_asset_id: str
    rendered_file_sha256: str
    media_probe: MediaProbeResult
    verdict: Literal["pass", "warning", "blocked", "waiver_required"]
    qa_scores: dict[str, float]
    repair_commands: list[PostRenderRepairCommand] = Field(default_factory=list)
    final_approval_eligible: bool
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Legacy rendered files can be imported as historical assets but must run QA before final approval, publishing intent, memory admission, or package sequencing. If media probe dependencies are unavailable, the gate returns `qa_unavailable` and blocks public approval rather than treating lack of evidence as a pass.

Warnings may proceed to operator review. Blockers require repair or explicit waiver where policy permits. Consent, source-lineage, and severe technical failures are not waiverable for public production.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T130-01 | Contracts | Add review request, media probe, QA result, repair command, receipt. |
| T130-02 | Render Workflow | Run QA after render completion. |
| T130-03 | Media Probe | Implement technical checks and frame/audio sampling. |
| T130-04 | Doctrine QA | Compare final render to delivery promise and primitive/doctrine receipts. |
| T130-05 | Approval Gates | Block final approval and publishing on failed QA. |
| T130-06 | Review UI | Surface QA evidence and repair commands. |
| T130-07 | Tests | Add technical, doctrine, blocker, waiver, and replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC130-01 | Every rendered asset produces post-render review receipt before final approval. | Operator approves MP4 with no QA receipt. | Phase4-M03; approval gate test. |
| AC130-02 | Technical QA detects black frames, frozen frames, broken overlays, off-canvas text, and bad media metadata. | Final render has clipped captions but passes. | Phase4-M05; media probe fixtures. |
| AC130-03 | Audio/caption QA detects silence, clipping, loudness, ducking, and caption timing failures. | Voice is silent for half the clip but marked approved. | Phase4-M06; audio fixture. |
| AC130-04 | Final render is compared to delivery promise and runtime lock. | Runtime lock says Remotion reaction UI, final file is static slideshow. | Phase4-M02; delivery promise QA test. |
| AC130-05 | Repair commands are structured and actionable. | QA says "visual issue" with no repair target. | Phase4-M05; repair command test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-043` | Render precedent | Technical render metadata. |
| `TS-CMF-092` | Review workbench | Surface QA evidence. |
| `TS-CMF-129` | Pre-compose gate | Delivery promise baseline. |
| `render_workflow.py` | Existing workflow | Run QA. |
| `image_critic_service.py` | Existing service | Visual QA. |
| `approval_gate_service.py` | Existing service | Block final approval. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Probe results, repair commands, and receipts validate. |
| Media tests | Black frame, frozen frame, wrong resolution, bad codec, and file size fixtures. |
| Visual tests | Off-canvas text, broken overlay, bad cutout, watermark/brand mismatch. |
| Audio tests | Silence, clipping, loudness, ducking, and caption timing. |
| Gate tests | Final approval and publishing block without pass or waiver. |
| Receipt tests | QA receipt replays file hash, probe results, scores, repairs, and eligibility. |
