---
tech_spec_id: "TS-CMF-124"
title: "Scored Provider Selector and Capability Router"
story_id: "13.5"
story_title: "Scored Provider Selector and Capability Router"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.05"
pipeline_stage: "provider selection and capability routing"
entry_object: "CapabilityRequest"
exit_object: "ProviderSelectionReceipt"
validation_contract: "provider scoring, consent compatibility, budget, brand fit, source lineage, reproducibility, primitive/eval compatibility"
required_receipt: "ProviderSelectionReceipt"
runtime_target: "Python / Pydantic v2 / provider operations / capability router / Operations Board"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-124: Scored Provider Selector and Capability Router

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Provider routing and actionable rejection mandates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact requirement for provider decisions. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.05. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-042-provider-capability-registry-and-job-receipts.md` | Existing provider job receipt precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-044-generative-provider-adapters.md` | Generative provider adapter dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-123-capability-tool-registry-and-provider-menu.md` | Active provider menu dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Existing provider operation owner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_request_builder.py` | Existing provider request builder. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Existing blocker owner. |
| `THE CMF STUDIO/src/ccp_studio/services/doctrine_evaluation_service.py` | Doctrine/primitive compatibility owner. |
| `OpenMontage docs/PROVIDERS.md` | Reference pattern for provider scoring and selection. |

## 2. Overview

This spec implements the scored provider selector and capability router for CMF. OpenMontage scores providers for task fit, quality, control, reliability, cost efficiency, latency, and continuity. CMF must extend that model with consent compatibility, brand fit, source-lineage support, reproducibility, primitive/eval compatibility, package budget, and doctrine fit.

Every provider decision must be receipt-backed. The selector receives a typed `CapabilityRequest`, reads the active `ProviderMenuSnapshot`, scores candidate capabilities, applies hard gates, selects the provider, records rejected options, estimates cost, sets fallback policy, and emits `ProviderSelectionReceipt`.

Operator preference is allowed, but it cannot override consent, budget caps, capability status, source-lineage requirements, or route doctrine. The selector covers Ideogram 4, GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, ComfyUI workers, LavaSR, TTS, music, stock footage, Remotion, Motion Canvas, HyperFrames, FFmpeg, Skia, caption engines, and evaluation workers through one governance model.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-124-001 | `CapabilityRequest` | Typed request for a provider capability tied to source, brand, format, budget, and eval requirements. |
| DEP-CMF-124-002 | `ProviderCandidateScore` | Scorecard across task fit, quality, control, reliability, cost, latency, continuity, consent, brand, lineage, reproducibility, and primitive fit. |
| DEP-CMF-124-003 | `ProviderSelectionPolicy` | Registry-configured weights, hard gates, fallback rules, and operator override boundaries. |
| DEP-CMF-124-004 | `ProviderSelectionReceipt` | Immutable proof of candidates, scores, chosen provider, rejected options, cost estimate, and required evals. |
| DEP-CMF-124-005 | `CapabilityRouteDecision` | Selected route from capability family to provider job, deterministic service, render runtime, or human queue. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/provider_jobs.py` | Add capability request, candidate score, selection policy, route decision, and receipt models. |
| `src/ccp_studio/services/provider_operations_service.py` | Own candidate scoring and selection. |
| `src/ccp_studio/services/provider_request_builder.py` | Consume route decisions to create provider jobs. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Provide primitive/eval compatibility signals. |
| `src/ccp_studio/services/approval_gate_service.py` | Block operator preference if hard gates fail. |
| `src/ccp_studio/api/v1/provider_jobs.py` | Add capability route and selection endpoints. |
| `POST /api/v1/provider-jobs/capability-route`, `POST /api/v1/provider-jobs/provider-selection`, `GET /api/v1/provider-jobs/provider-selection/{receipt_id}` | Exact API routes for scored routing and selection receipt inspection. |
| `src/ccp_studio/repositories/provider_jobs.py` | Persist selection receipts and scorecards. |
| Postgres tables: `capability_requests`, `provider_candidate_scores`, `provider_selection_receipts`, `provider_route_decisions` | Durable storage for route requests, scorecards, chosen providers, and replayable decisions. |
| `THE CMF STUDIO/registries/providers/provider_selection_policy.v1.json` | New score weight and hard gate registry. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PRG-001` | Inline Routing SLA | Provider route resolves before job creation. |
| `EXP-FBK-001` | Actionable Rejection | Rejected providers include score and hard-gate reason. |
| `EXP-SOC-001` | Verifiable Artifact | Selection receipt records all candidates and chosen route. |
| `EXP-TRS-004` | Cinematic Meaning | Provider choice must preserve format meaning and visual/sonic quality. |
| `EXP-FRC-006` | Frictionless Block | Failed selection gives alternatives, waiver path, or "no safe route". |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Hard gates block consent, budget, lineage, and doctrine violations. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Capability route is resolved before provider request creation. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Receipt names rejected candidates and exact reasons. |
| Phase4-M06: Sonic Prestige Rule | Phase 4 Story 6.1 | `EXP-TRS-003` | Audio providers must meet voice, music, loudness, and mix requirements. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Selection receipt is stored and replayable. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Separate provider menu from provider selector. | Menu answers what is available; selector decides what should be used. |
| Score weights live in registry. | Enables quality tuning without prompt drift. |
| Hard gates override operator preference. | Protects consent, source truth, budget, and doctrine. |
| Receipts store rejected providers. | Supports audit, learning, and quality improvement. |

## 4. Implementation Plan

1. Add selector contracts to provider job contracts.
2. Create `provider_selection_policy.v1.json` with weights and hard gates per capability family.
3. Implement `score_provider_candidates()` in `provider_operations_service.py`.
4. Add hard-gate checks for consent, budget, package policy, source lineage, reproducibility, capability status, brand fit, and primitive/eval compatibility.
5. Add operator preference handling that can bias score but cannot override hard gates.
6. Emit `ProviderSelectionReceipt`.
7. Connect route decision to `provider_request_builder.py`.
8. Add Operations Board read model showing candidates, scores, selected provider, rejected options, cost, and fallback.
9. Add tests for scoring, hard gates, overrides, fallback, and receipt replay.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class CapabilityRequest(BaseModel):
    schema_version: Literal["cmf.capability_request.v1"]
    request_id: str
    provider_menu_snapshot_id: str
    organization_id: str
    brand_id: str
    capability_family: str
    asset_format: str
    source_object_refs: list[str]
    required_output_schema_ref: str
    budget_ceiling_usd: float | None = None
    operator_preference_provider: str | None = None
    required_eval_target_ids: list[str] = Field(default_factory=list)


class ProviderCandidateScore(BaseModel):
    provider_capability_id: str
    total_score: float = Field(ge=0, le=1)
    dimensions: dict[str, float]
    hard_gate_status: Literal["pass", "blocked"]
    hard_gate_reasons: list[str] = Field(default_factory=list)


class ProviderSelectionReceipt(BaseModel):
    schema_version: Literal["cmf.provider_selection_receipt.v1"]
    receipt_id: str
    request_id: str
    chosen_capability_id: str
    candidate_scores: list[ProviderCandidateScore]
    rejected_capability_ids: list[str]
    cost_estimate_usd: float | None = None
    fallback_capability_ids: list[str] = Field(default_factory=list)
    required_eval_target_ids: list[str]
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing provider jobs may continue if already queued or completed. New provider jobs must reference a provider selection receipt once this selector is active. Legacy direct provider calls can be marked `legacy_direct_route` in receipts during migration, but production workflows cannot create new direct calls without a capability request and route decision.

If no safe provider passes hard gates, the selector returns `blocked` with alternatives: adjust budget, add credentials, choose a lower-risk format, request human override where allowed, or defer the asset. It must not select the "least bad" provider when hard gates fail.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T124-01 | Contracts | Add capability request, candidate score, selection policy, route decision, receipt. |
| T124-02 | Registry | Add provider selection policy weights and hard gates. |
| T124-03 | Services | Implement scoring and hard-gate selection. |
| T124-04 | Provider Requests | Require selection receipt before job creation. |
| T124-05 | Approval Gates | Block unsafe operator preferences. |
| T124-06 | Operations Board | Add candidate score and route read model. |
| T124-07 | Tests | Add scoring, hard gate, override, fallback, and replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC124-01 | Selector scores all available candidates using registry weights. | Only the operator's preferred provider is considered. | Phase4-M03; scoring test. |
| AC124-02 | Consent, budget, lineage, capability, and doctrine hard gates override preference. | Operator chooses a stock provider without commercial rights. | Phase4-M01; hard gate test. |
| AC124-03 | Rejected providers include score and reason. | Receipt only stores chosen provider. | Phase4-M05; receipt schema test. |
| AC124-04 | Provider request builder requires selection receipt. | Provider job is created from a prompt directly. | Phase4-M03; request-builder test. |
| AC124-05 | Audio providers satisfy sonic requirements when selected for voice/music/mix. | TTS route selected without voice quality or loudness eval. | Phase4-M06; audio route test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-123` | Provider menu | Must provide active capability candidates. |
| `TS-CMF-042` | Provider receipt precedent | Extend rather than duplicate. |
| `TS-CMF-044` | Generative adapters | Candidate provider families must align. |
| `provider_operations_service.py` | Existing service | Own selector. |
| `provider_request_builder.py` | Existing service | Consume route decision. |
| `doctrine_evaluation_service.py` | Existing service | Provide primitive/eval compatibility. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Scoring tests | Each dimension affects total score according to registry weights. |
| Hard gate tests | Consent, budget, lineage, reproducibility, and doctrine failures block selection. |
| Override tests | Operator preference can bias eligible candidates but cannot pass blocked candidates. |
| Request tests | Provider jobs require selection receipt. |
| Receipt tests | Candidate scores, rejected options, chosen provider, cost, fallback, and evals are replayable. |
| Regression tests | Known routes for Ideogram, Qwen layered, ComfyUI, Remotion, Motion Canvas, FFmpeg, and Skia select expected providers under fixtures. |
