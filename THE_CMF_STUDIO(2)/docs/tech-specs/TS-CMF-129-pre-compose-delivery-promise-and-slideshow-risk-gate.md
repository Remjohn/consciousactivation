---
tech_spec_id: "TS-CMF-129"
title: "Pre-Compose Delivery Promise and Slideshow Risk Gate"
story_id: "13.10"
story_title: "Pre-Compose Delivery Promise and Slideshow Risk Gate"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.10"
pipeline_stage: "composition validation before rendering"
entry_object: "PreComposeValidationRequest"
exit_object: "PreComposeValidationReceipt"
validation_contract: "delivery promise, format fit, motion adequacy, primitive triad, doctrine gates, timing map, runtime route, asset readiness"
required_receipt: "PreComposeValidationReceipt"
runtime_target: "Python / Pydantic v2 / composition service / doctrine evals / approval blockers / review workbench"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-129: Pre-Compose Delivery Promise and Slideshow Risk Gate

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Cinematic meaning, routing, rejection, and sonic mandates. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.10. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` | Four canonical video format obligations. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime and transcript timing dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Composition eval and approval dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md` | Sequence handoff dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-128-render-runtime-selection-and-locking.md` | Runtime lock dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/composition_service.py` | Existing composition planning owner. |
| `THE CMF STUDIO/src/ccp_studio/services/scene_spec_compiler.py` | SceneSpec owner. |
| `THE CMF STUDIO/src/ccp_studio/services/doctrine_evaluation_service.py` | Doctrine/primitive evaluation owner. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Blocker owner. |
| `OpenMontage AGENT_GUIDE.md` | Reference pattern for pre-compose delivery promise checks. |

## 2. Overview

CMF must validate whether an approved composition plan can actually deliver its promise before rendering starts. This prevents a cinematic story from becoming a still slideshow, a reaction clip from showing UI unrelated to the transcript, a PaperCut explainer from missing layer materiality, or an educational sequence from using decorative motion with no concept mapping.

The pre-compose gate validates SceneSpec, ContentSequenceProgram, CompositionRuntimeBinding, render runtime lock, selected assets, caption plan, music/SFX plan, timing map, provider jobs, primitive triad receipts, doctrine evals, and operator approvals. It returns `pass`, `warning`, `blocked`, or `waiver_required`.

Slideshow risk is a first-class signal. The gate scores repetition, decorative visuals, weak motion, unsupported cinematic claims, typography overreliance, missing source footage, missing concept-motion mapping, stale reaction UI, weak primitive triad, and absence of human/emotional evidence. Rendering cannot start until hard blockers are repaired or a human waiver is recorded where allowed.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-129-001 | `DeliveryPromiseContract` | Declares promised format, emotional/teaching/reaction function, motion needs, evidence needs, and payoff. |
| DEP-CMF-129-002 | `PreComposeValidationRequest` | Bundles SceneSpec, sequence, runtime lock, assets, captions, audio, provider jobs, and eval receipts. |
| DEP-CMF-129-003 | `SlideshowRiskScore` | Scores static/repetitive/unsupported composition risk. |
| DEP-CMF-129-004 | `PreComposeBlocker` | Exact blocking issue with repair command and waiver policy. |
| DEP-CMF-129-005 | `PreComposeValidationReceipt` | Receipt proving gate inputs, verdict, risk scores, blockers, waivers, and approval state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/composition.py` | Add delivery promise, pre-compose request, risk score, blocker, and receipt models. |
| `src/ccp_studio/services/composition_service.py` | Own pre-compose validation orchestration. |
| `src/ccp_studio/services/scene_spec_compiler.py` | Provide SceneSpec fields and composition family constraints. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Evaluate primitive triad, doctrine, and format-specific gates. |
| `src/ccp_studio/services/approval_gate_service.py` | Block render job creation when pre-compose fails. |
| `src/ccp_studio/workflows/render_workflow.py` | Require pre-compose receipt before render job. |
| `src/ccp_studio/api/v1/compositions.py` | Add pre-compose validate and repair-plan endpoints. |
| `POST /api/v1/compositions/pre-compose/validate`, `POST /api/v1/compositions/pre-compose/{receipt_id}/repair-plan`, `GET /api/v1/compositions/pre-compose/{receipt_id}` | Exact API routes for pre-compose gate, repair plan, and inspection. |
| `src/ccp_studio/services/review_state_service.py` | Surface delivery promise, risk, blockers, and waiver options. |
| Postgres tables: `precompose_validation_receipts`, `precompose_blockers`, `slideshow_risk_scores`, `composition_delivery_promises` | Durable storage for pre-render validation, blocker evidence, risk scores, and declared composition promises. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-TRS-004` | Cinematic Meaning | Planned composition must preserve story/teaching/reaction meaning. |
| `EXP-FBK-001` | Actionable Rejection | Failures return exact scene, beat, asset, timing, or primitive repair command. |
| `EXP-PRG-001` | Inline Routing SLA | Gate runs before render workflow, not after render failure. |
| `EXP-SOC-001` | Verifiable Artifact | Receipt stores risk scores, blockers, input hashes, and waiver state. |
| `EXP-TRS-003` | Sonic Prestige | Audio/caption/music plan must match promised asset quality. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Blocks format promises that cannot be fulfilled by planned scene, motion, and assets. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Render workflow requires pre-compose receipt. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Blockers identify exact scene/beat/asset/timing repair. |
| Phase4-M06: Sonic Prestige Rule | Phase 4 Story 6.1 | `EXP-TRS-003` | Blocks missing or low-quality audio/caption plan when format requires it. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Receipt records validation state and waiver evidence. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Pre-compose blocks before render. | Prevents wasted provider spend and poor outputs. |
| Slideshow risk is explicit and scored. | Directly addresses the recurring failure mode of static outputs. |
| Waivers are possible only when policy allows. | Keeps operator control without hiding risk. |
| Risk is format-specific. | Cinematic, PaperCut, Living Commentary, and Conscious Reactions have different failure modes. |

## 4. Implementation Plan

1. Add delivery promise, validation request, slideshow risk, blocker, and receipt contracts.
2. Implement pre-compose validator in `composition_service.py`.
3. Add format-specific rules for Cinematic Story Commentary, Educational/PaperCut, Living Commentary Reactions, Conscious Reactions Editing, carousel, and SuperVisuals.
4. Validate asset readiness, timing map, captions, audio plan, runtime lock, provider jobs, primitive triads, doctrine receipts, and operator approvals.
5. Compute slideshow risk scores and hard failures.
6. Connect approval gate to block render job creation without pass or approved waiver.
7. Add repair commands and review read model.
8. Add tests for static slideshow risk, reaction UI mismatch, PaperCut materiality, cinematic pacing, missing concept-motion mapping, and waiver policy.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class SlideshowRiskScore(BaseModel):
    schema_version: Literal["cmf.slideshow_risk_score.v1"]
    static_asset_ratio: float = Field(ge=0, le=1)
    repetition_score: float = Field(ge=0, le=1)
    decorative_visual_score: float = Field(ge=0, le=1)
    motion_adequacy_score: float = Field(ge=0, le=1)
    source_evidence_score: float = Field(ge=0, le=1)
    primitive_triad_score: float = Field(ge=0, le=1)
    overall_risk: Literal["low", "medium", "high", "blocked"]


class PreComposeBlocker(BaseModel):
    blocker_code: str
    stage_ref: str
    scene_ref: str | None = None
    beat_ref: str | None = None
    reason: str
    repair_command: str
    waiver_policy: Literal["not_allowed", "human_approval_required", "warning_only"]


class PreComposeValidationReceipt(BaseModel):
    schema_version: Literal["cmf.pre_compose_validation_receipt.v1"]
    receipt_id: str
    validation_request_id: str
    verdict: Literal["pass", "warning", "blocked", "waiver_required"]
    slideshow_risk: SlideshowRiskScore
    blockers: list[PreComposeBlocker] = Field(default_factory=list)
    input_hashes: dict[str, str]
    waiver_receipt_id: str | None = None
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Legacy render jobs already completed remain historical records. New render jobs require a pre-compose validation receipt. If a workflow lacks enough structured data to validate, the gate returns `blocked_missing_contracts` and requires the upstream SceneSpec, sequence program, runtime lock, or asset manifest to be repaired.

If a low-risk warning exists, rendering may proceed with warning receipt. High-risk or blocked conditions cannot proceed without repair or explicit waiver where policy allows.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T129-01 | Contracts | Add delivery promise, validation request, risk score, blocker, receipt. |
| T129-02 | Composition Service | Implement validator and risk scoring. |
| T129-03 | Doctrine Eval | Bind primitive triad and format-specific doctrine checks. |
| T129-04 | Render Workflow | Require pass or approved waiver before render job. |
| T129-05 | Review UI | Show delivery promise, risk, blockers, and repair commands. |
| T129-06 | Fixtures | Add four-video-format and still-output risk fixtures. |
| T129-07 | Tests | Add blocker, waiver, slideshow risk, and receipt tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC129-01 | Render workflow blocks without pre-compose receipt. | Render job starts from SceneSpec alone. | Phase4-M03; workflow gate test. |
| AC129-02 | Slideshow risk blocks high-risk motion-led videos. | Conscious Reactions clip renders with mostly static image cards. | Phase4-M02; slideshow risk fixture. |
| AC129-03 | Blockers identify exact scene, beat, asset, timing, or primitive repair. | Operator sees "composition weak" with no fix. | Phase4-M05; blocker payload test. |
| AC129-04 | PaperCut and 2D explainer scenes require layer materiality and concept-motion mapping. | PaperCut explainer has flat text over stock image. | Phase4-M02; explainer fixture. |
| AC129-05 | Audio/caption plan is validated when format requires it. | Cinematic story has captions but no audio mix plan. | Phase4-M06; sonic plan test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-078` | Format doctrine | Four video format requirements. |
| `TS-CMF-080` | Composition binding | Provides runtime/timing contracts. |
| `TS-CMF-118` | Sequence program | Provides semantic beat order. |
| `TS-CMF-128` | Runtime lock | Required before pre-compose pass. |
| `composition_service.py` | Existing service | Own validator. |
| `approval_gate_service.py` | Existing service | Block render. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Validation request, risk score, blocker, and receipt validate. |
| Format fixtures | Cinematic, PaperCut, Living Commentary, Conscious Reactions, carousel, and SuperVisual fixtures. |
| Slideshow tests | Static ratio, repetition, decorative visuals, and weak motion produce risk scores. |
| Blocker tests | Missing asset, timing, primitive, runtime, caption, or audio plan returns repair command. |
| Waiver tests | Waiver-required and not-allowed states enforce approval policy. |
| Receipt tests | Receipt replays input hashes, verdict, blockers, and waiver evidence. |
