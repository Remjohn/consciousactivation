---
tech_spec_id: "TS-CMF-123"
title: "Capability Tool Registry and Provider Menu"
story_id: "13.4"
story_title: "Capability Tool Registry and Provider Menu"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.04"
pipeline_stage: "provider and tool capability planning"
entry_object: "CapabilityRegistryQuery"
exit_object: "ProviderMenuSnapshot"
validation_contract: "capability schema, credential boundary, consent requirements, cost/resource profile, fallback options, receipt chain"
required_receipt: "ProviderMenuSnapshotReceipt"
runtime_target: "Python / Pydantic v2 / provider registry / Operations Board / Pi Harness"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-123: Capability Tool Registry and Provider Menu

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 mandates for routing, blockers, and provider behavior. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.04. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-042-provider-capability-registry-and-job-receipts.md` | Existing provider capability precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-045-self-hosted-comfyui-docker-gpu-worker.md` | ComfyUI GPU worker dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime capability dependency. |
| `THE CMF STUDIO/src/ccp_studio/contracts/provider_jobs.py` | Existing provider job contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Existing provider operations owner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_request_builder.py` | Existing request-building owner. |
| `THE CMF STUDIO/src/ccp_studio/services/comfy_gpu_worker_service.py` | Existing self-hosted GPU worker owner. |
| `THE CMF STUDIO/src/ccp_studio/services/operations_board_service.py` | Existing operations read-model owner. |
| `OpenMontage docs/ARCHITECTURE.md` | Reference pattern for tool registry. |
| `OpenMontage docs/PROVIDERS.md` | Reference pattern for provider menu and setup status. |

## 2. Overview

CMF needs a capability registry and provider menu that answers a simple operator question before production starts: what can this factory actually do right now, with which tools, under which constraints, at what cost and quality risk?

This spec adapts OpenMontage's tool registry and provider menu into CMF's provider, renderer, research, editing, evaluation, and publishing boundaries. Each capability record states name, family, provider, runtime type, stability, dependencies, credential boundary, input schema, output schema, fallback options, resource profile, cost estimator, retry policy, consent requirements, brand-scope behavior, linked skills, and eval requirements.

The provider menu summarizes configured, unavailable, blocked, and degraded capabilities for operators and Pi before expensive work begins. It covers image generation, video generation, layer extraction, segmentation, background removal, transcription, captions, TTS, music, SFX, research, visual research, Remotion, Motion Canvas, HyperFrames, FFmpeg, ComfyUI, Skia, rough notation, publishing, and evaluation workers.

CMF must not hardcode provider availability in prompts or specs. Runtime consumers query this registry.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-123-001 | `CapabilityToolRecord` | Typed registry entry for a provider, service, runtime, evaluator, renderer, or adapter capability. |
| DEP-CMF-123-002 | `ProviderMenuSnapshot` | Operator-facing snapshot of available, unavailable, blocked, degraded, and credential-required capabilities. |
| DEP-CMF-123-003 | `CapabilityAvailabilityGate` | Validates credentials, runtime health, consent, license, GPU status, and dependency readiness. |
| DEP-CMF-123-004 | `ProviderMenuSnapshotReceipt` | Hash-backed proof of capability state used during planning. |
| DEP-CMF-123-005 | `CapabilityFallbackPolicy` | Defines allowed fallback tools and forbidden fallback substitutions. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/provider_jobs.py` | Add capability records, menu snapshots, fallback policy, and capability availability gate models. |
| `src/ccp_studio/services/provider_operations_service.py` | Own registry loading, provider menu generation, and health status aggregation. |
| `src/ccp_studio/services/provider_request_builder.py` | Query capability records before building provider requests. |
| `src/ccp_studio/services/comfy_gpu_worker_service.py` | Report ComfyUI worker GPU status, queue state, and model availability. |
| `src/ccp_studio/services/operations_board_service.py` | Surface provider menu snapshots and blockers. |
| `src/ccp_studio/api/v1/provider_jobs.py` | Add capability registry and provider menu endpoints. |
| `POST /api/v1/provider-jobs/capabilities`, `POST /api/v1/provider-jobs/provider-menu/snapshot`, `GET /api/v1/provider-jobs/provider-menu/{snapshot_id}` | Exact API routes for capability registration and menu inspection. |
| `src/ccp_studio/repositories/provider_jobs.py` | Persist capability snapshots and receipts. |
| Postgres tables: `provider_capabilities`, `provider_menu_snapshots`, `provider_availability_checks`, `provider_operation_receipts` | Durable storage for provider capability inventory, active menus, availability evidence, and receipts. |
| `THE CMF STUDIO/registries/providers/` | New provider capability registry namespace. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PRG-001` | Inline Routing SLA | Runtime resolves capability state through registry before execution. |
| `EXP-FBK-001` | Actionable Rejection | Missing credentials, unavailable GPU, or blocked consent returns exact repair action. |
| `EXP-SOC-001` | Verifiable Artifact | Menu snapshot is a receipt-backed artifact for audit replay. |
| `EXP-FRC-006` | Frictionless Block | Provider blocks must offer safe next route or explain no fallback. |
| `EXP-TRS-004` | Cinematic Meaning | Provider menu must reveal quality tradeoffs that could flatten format meaning. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Production planning cannot select capabilities without availability and consent checks. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Pi and workflows query provider menu snapshot inline. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Unavailable capabilities return missing credential, runtime, license, or consent reason. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Provider menu snapshots write receipts and can be replayed. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Capability records are provider-neutral. | Allows Ideogram, GPT Image 2, Flux 2 Klein 9b, Qwen layered, SAM3, ComfyUI, Remotion, and FFmpeg to share governance. |
| Menu snapshots are generated per brand/run context. | Consent, credentials, budget, and package state vary by context. |
| Fallback policy is explicit. | Prevents silent downgrade from motion video to static slideshow. |
| Operations Board is the canonical operator surface. | The operator must see capability and blocker state before spend. |

## 4. Implementation Plan

1. Add capability and provider menu contracts to `provider_jobs.py` or a dedicated `provider_capabilities.py`.
2. Seed `registries/providers/provider_capabilities.v1.json` with CMF's known providers and runtimes.
3. Extend `provider_operations_service.py` to load registry, check runtime health, check credentials, check consent, estimate resource profile, and create snapshots.
4. Add provider menu endpoint returning configured, unavailable, blocked, degraded, and credential-required capabilities.
5. Connect `provider_request_builder.py` to reject provider requests not present in the active menu snapshot.
6. Connect ComfyUI worker status, GPU model availability, queue depth, and VRAM class to capability status.
7. Add Operations Board read model with provider family filters and repair commands.
8. Emit `ProviderMenuSnapshotReceipt` for production planning.
9. Add tests for missing credentials, unavailable GPU worker, consent block, fallback policy, and snapshot replay.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class CapabilityToolRecord(BaseModel):
    schema_version: Literal["cmf.capability_tool_record.v1"]
    capability_id: str
    name: str
    capability_family: Literal[
        "research", "transcription", "image_generation", "video_generation",
        "layer_extraction", "segmentation", "rendering", "audio",
        "evaluation", "publishing", "storage"
    ]
    provider: str
    runtime_type: Literal["local", "self_hosted_gpu", "cloud_api", "browser", "deterministic_service"]
    input_schema_ref: str
    output_schema_ref: str
    credential_boundary: str
    consent_requirements: list[str]
    fallback_capability_ids: list[str] = Field(default_factory=list)
    resource_profile: dict[str, str | int | float]
    eval_target_ids: list[str] = Field(default_factory=list)


class ProviderMenuSnapshot(BaseModel):
    schema_version: Literal["cmf.provider_menu_snapshot.v1"]
    snapshot_id: str
    organization_id: str
    brand_id: str
    pipeline_run_id: str | None = None
    available_capability_ids: list[str]
    unavailable_capability_ids: list[str]
    blocked_capability_ids: list[str]
    degraded_capability_ids: list[str]
    blocker_reasons: dict[str, str]
    snapshot_sha256: str
```

## 6. Backward Compatibility Fallback

Existing provider jobs can continue using current provider job contracts. New production planning routes must create a provider menu snapshot before selecting providers. If no capability registry exists for a legacy provider, it may be marked `legacy_unregistered` for audit visibility, but new jobs cannot use it until a capability record is added.

If snapshot generation fails, planning blocks and returns missing registry, credential, runtime, consent, or health status repairs. It must not guess provider availability from environment variables or prompt instructions.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T123-01 | Contracts | Add capability record, snapshot, availability gate, and fallback policy. |
| T123-02 | Registry | Seed provider capabilities registry. |
| T123-03 | Services | Implement provider menu generator and health aggregation. |
| T123-04 | API | Add provider capability and menu endpoints. |
| T123-05 | Operations Board | Add provider menu read model. |
| T123-06 | Provider Requests | Enforce snapshot gating before request creation. |
| T123-07 | Tests | Add capability availability, fallback, consent, and replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC123-01 | Every provider request references an available capability in the active menu snapshot. | Provider request calls Qwen layered without a capability record. | Phase4-M03; request builder test. |
| AC123-02 | Missing credentials or GPU runtime returns a blocker with repair command. | ComfyUI job fails later because GPU status was never checked. | Phase4-M05; availability gate fixture. |
| AC123-03 | Consent and license requirements are visible in provider menu state. | Stock footage capability shows available despite missing commercial license. | Phase4-M01; consent/license test. |
| AC123-04 | Fallbacks are explicit and cannot change output meaning silently. | Motion Canvas unavailable, system silently switches to static image. | Phase4-M05; fallback policy test. |
| AC123-05 | Provider menu snapshot writes receipt for replay. | Operator cannot reconstruct what was available at planning time. | Phase5-M01; receipt replay test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-042` | Provider precedent | Extend capability registry and receipt patterns. |
| `TS-CMF-045` | ComfyUI worker | Worker status feeds capability menu. |
| `provider_operations_service.py` | Existing service | Own menu generation. |
| `provider_request_builder.py` | Existing service | Enforce capability availability. |
| `operations_board_service.py` | Existing service | Surface menu and blockers. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Registry tests | Capability registry loads and rejects duplicate IDs or missing schemas. |
| Availability tests | Missing credentials, offline ComfyUI, unavailable model, or consent block sets correct state. |
| Request tests | Provider request builder rejects unavailable or unregistered capabilities. |
| Fallback tests | Fallbacks preserve output family and require approval when quality changes. |
| Receipt tests | Snapshot receipt reconstructs available, unavailable, blocked, and degraded capabilities. |
| UI read-model tests | Operations Board receives capability groups, blockers, and repair commands. |
