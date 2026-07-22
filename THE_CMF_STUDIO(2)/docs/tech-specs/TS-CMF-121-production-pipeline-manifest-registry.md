---
tech_spec_id: "TS-CMF-121"
title: "CMF Production Pipeline Manifest Registry"
story_id: "13.2"
story_title: "CMF Production Pipeline Manifest Registry"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.02"
pipeline_stage: "cross-stage production orchestration"
entry_object: "ProductionPipelineManifestDraft"
exit_object: "ProductionPipelineManifestSnapshot"
validation_contract: "pipeline manifest schema, CMF object spine, consent, source truth, primitive gates, receipt chain"
required_receipt: "ProductionPipelineManifestActivationReceipt"
runtime_target: "Python / Pydantic v2 / registry service / durable workflow / Operations Board"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-121: CMF Production Pipeline Manifest Registry

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section format and backend mapping requirements. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for pipeline and routing behavior. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact mandate for activated manifests. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.02. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Interview Brief V2, Expression Ingredient Inventory, and ContentSequenceProgram dependencies. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md` | Command spine and receipt discipline. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime and transcript timing dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md` | Sequence-to-composition handoff dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/orchestration.py` | Existing orchestration owner to extend. |
| `THE CMF STUDIO/src/ccp_studio/workflows/orchestration_run.py` | Existing workflow run shape. |
| `THE CMF STUDIO/src/ccp_studio/services/command_bus.py` | Existing command dispatch owner. |
| `THE CMF STUDIO/src/ccp_studio/services/registry_service.py` | Registry owner for active snapshots. |
| `OpenMontage docs/ARCHITECTURE.md` | Reference pattern for declarative pipeline manifests. |
| `OpenMontage AGENT_GUIDE.md` | Reference pattern for rule-zero stage execution. |

## 2. Overview

OpenMontage proves the usefulness of declarative pipeline manifests. CMF must adopt the pattern with stricter ownership: a manifest is not a generic video workflow; it is a typed production route bound to the CMF object spine.

Each manifest declares stage order, stage owner, stage director skill contract, entry object, exit object, required tools, fallback tools, human approval policy, review focus, success criteria, eval targets, receipt obligations, and downstream composition targets. A valid CMF manifest must explicitly bind to organization, brand workspace, consent state, Brand Context Version, Interview Brief V2, Complete Expression Session, Expression Moment, route, Asset Package Spec, ContentSequenceProgram, SceneSpec, or render contract according to stage.

Manifests are activated snapshots, not loose YAML files. Pi, DSPy programs, agents, provider adapters, renderers, and review workbench surfaces must resolve the active snapshot through the registry service before execution. Draft manifests are editable planning artifacts; snapshots are immutable runtime authority.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-121-001 | `ProductionPipelineManifestDraft` | Editable authoring object for a pipeline profile. |
| DEP-CMF-121-002 | `ProductionPipelineStageSpec` | Stage contract with entry/exit objects, owner, tools, skill, evals, approvals, receipts, and blockers. |
| DEP-CMF-121-003 | `ProductionPipelineManifestSnapshot` | Immutable activated manifest used by runtime and replay. |
| DEP-CMF-121-004 | `StageObjectContinuityGate` | Validates that each stage consumes the prior stage's typed output or an explicit upstream dependency. |
| DEP-CMF-121-005 | `ProductionPipelineManifestActivationReceipt` | Receipt proving schema, object-spine, consent, primitive, CBAR, and approval checks. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/orchestration.py` | Add manifest draft, stage spec, snapshot, continuity gate, and activation receipt contracts. |
| `src/ccp_studio/services/orchestration.py` | Resolve active manifest snapshots before starting production runs. |
| `src/ccp_studio/workflows/orchestration_run.py` | Bind workflow runs to manifest snapshot ID and stage spec IDs. |
| `src/ccp_studio/services/command_bus.py` | Require command metadata to include manifest snapshot and current stage. |
| `src/ccp_studio/services/registry_service.py` | Store active manifest snapshots and registry read models. |
| `src/ccp_studio/services/approval_gate_service.py` | Block activation on missing consent, source truth, human review policy, or primitive gates. |
| `src/ccp_studio/api/v1/orchestration.py` | Add manifest draft, validate, activate, deactivate, and inspect endpoints. |
| `POST /api/v1/orchestration/manifests`, `POST /api/v1/orchestration/manifests/{manifest_id}/validate`, `POST /api/v1/orchestration/manifests/{manifest_id}/activate`, `GET /api/v1/orchestration/manifests/{manifest_id}` | Exact API routes for manifest lifecycle. |
| `src/ccp_studio/repositories/orchestration.py` | Persist drafts, snapshots, stage specs, and activation receipts. |
| Postgres tables: `production_pipeline_manifest_drafts`, `production_pipeline_manifest_snapshots`, `pipeline_stage_specs`, `pipeline_manifest_activation_receipts` | Durable storage for manifest lifecycle, active snapshots, stage contracts, and receipts. |
| `THE CMF STUDIO/registries/pipelines/` | New manifest registry namespace. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-SOC-001` | Verifiable Artifact Rule | Active manifests are versioned, hash-backed artifacts with receipt obligations. |
| `EXP-PRG-001` | Inline Routing SLA | Runtime stage routing must resolve from active snapshot, not local drafts. |
| `EXP-FBK-001` | Actionable Rejection Rule | Manifest validation failures name exact missing stage, object, gate, or receipt. |
| `EXP-TRS-004` | Cinematic Meaning Rule | Pipeline paths cannot flatten story, source truth, or composition meaning. |
| `EXP-FRC-006` | Frictionless Block Rule | Blockers give operators repair commands without allowing unsafe bypass. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Activation blocks missing consent, Brand Context, source truth, primitive evals, and approvals. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Runtime resolves stage owner, skill, and tools from the snapshot. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Validation failures include failing stage ID and repair command. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Activated manifests write receipt-chain rows and store snapshot hashes. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Runtime uses snapshots only. | Prevents draft changes from mutating active production runs. |
| Stage specs declare both object contracts and receipts. | Keeps agent work tied to CMF state and audit trail. |
| Manifest activation is approval-gated. | Prevents hidden bypass of source, consent, primitive, and review obligations. |
| Manifest registry is brand-aware but not brand-owned. | One manifest profile can be reused while each run remains brand-scoped. |

## 4. Implementation Plan

1. Add Pydantic contracts for manifest drafts, stage specs, snapshots, validation reports, and activation receipts.
2. Create `pipeline_manifest_registry_service.py` or extend `orchestration.py` with manifest registration and snapshot resolution.
3. Add validation gates for stage order, object continuity, required receipts, consent requirements, source truth requirements, primitive/eval requirements, and approval policies.
4. Add registry namespace `registries/pipelines/` with canonical CMF manifest profiles for interview-first production, existing-interview production, carousel, SuperVisual, PaperCut, and reaction editing.
5. Add endpoints for authoring, validation, activation, deactivation, and read-model inspection.
6. Modify workflow run creation to require an active manifest snapshot ID.
7. Modify command metadata to include manifest snapshot ID, stage ID, and stage receipt obligation.
8. Add Operations Board read model for active manifests, stage state, blockers, and runtime consumers.
9. Emit activation receipt after all gates pass.
10. Add pytest fixtures proving invalid manifests cannot activate.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class ProductionPipelineStageSpec(BaseModel):
    schema_version: Literal["cmf.pipeline_stage_spec.v1"]
    stage_id: str
    stage_order: int
    stage_name: str
    owner_kind: Literal["agent", "sub_agent", "service", "dspy_program", "human_queue"]
    owner_ref: str
    stage_director_skill_ref: str | None = None
    entry_object_type: str
    exit_object_type: str
    required_tool_refs: list[str] = Field(default_factory=list)
    fallback_tool_refs: list[str] = Field(default_factory=list)
    required_eval_target_ids: list[str]
    required_receipt_type: str
    human_approval_policy: Literal["required", "waiver_allowed", "not_required"]
    blocker_codes: list[str] = Field(default_factory=list)


class ProductionPipelineManifestSnapshot(BaseModel):
    schema_version: Literal["cmf.pipeline_manifest_snapshot.v1"]
    manifest_snapshot_id: str
    manifest_family: str
    version: int
    compatible_asset_formats: list[str]
    entry_object_type: str
    exit_object_type: str
    stage_specs: list[ProductionPipelineStageSpec]
    required_brand_context_state: str
    required_consent_scopes: list[str]
    forbidden_bypasses: list[str]
    snapshot_sha256: str


class ProductionPipelineManifestActivationReceipt(BaseModel):
    schema_version: Literal["cmf.pipeline_manifest_activation_receipt.v1"]
    receipt_id: str
    manifest_snapshot_id: str
    validation_verdict: Literal["pass", "blocked"]
    continuity_passed: bool
    consent_gate_passed: bool
    primitive_gate_passed: bool
    cbar_gate_passed: bool
    blocker_codes: list[str] = Field(default_factory=list)
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing workflow services can continue to execute current hardcoded paths until a manifest profile is activated for that workflow family. Once a workflow family has an active manifest snapshot, all new runs for that family must use the snapshot. Legacy runs remain replayable with their previous orchestration records but cannot be edited as if they had manifest coverage.

If manifest resolution fails during run creation, the system must block the run and return available active snapshots or a repair command to activate a profile. It must not fall back to loose YAML, hidden prompts, or hand-coded stage order.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T121-01 | Contracts | Add manifest, stage spec, validation, and activation receipt models. |
| T121-02 | Registry | Add `registries/pipelines/` and seed manifest profiles. |
| T121-03 | Services | Implement validation and snapshot activation. |
| T121-04 | Workflow | Bind production runs and commands to manifest snapshots. |
| T121-05 | API | Add author, validate, activate, deactivate, inspect endpoints. |
| T121-06 | Review UI | Add manifest read model to Operations Board. |
| T121-07 | Tests | Add invalid continuity, missing gate, draft access, and snapshot replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC121-01 | Active manifest stages have entry/exit object continuity. | Asset stage expects `SceneSpec` but previous stage emits free text. | Phase4-M03; continuity gate test. |
| AC121-02 | Manifest activation blocks missing consent, source truth, Brand Context, primitive evals, or approval policy. | Pipeline renders from raw upload with no consent stage. | Phase4-M01; activation blocker fixture. |
| AC121-03 | Runtime uses active snapshot, not draft files. | Pi reads a local YAML draft directly. | Phase4-M03; runtime resolver test. |
| AC121-04 | Every stage declares receipt type and eval target obligations. | Render stage has no post-render receipt requirement. | Phase5-M01; schema validation test. |
| AC121-05 | Manifest failures include actionable repair commands. | Operator sees "invalid manifest" with no stage ID or fix. | Phase4-M05; blocker payload test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-001` | Command spine | Commands must carry manifest and stage metadata. |
| `TS-CMF-080` | Composition runtime | Downstream composition stages must bind to runtime contracts. |
| `TS-CMF-118` | Sequence handoff | ContentSequenceProgram stages must feed composition stages. |
| `orchestration.py` | Existing service | Extend instead of bypassing. |
| `registry_service.py` | Existing service | Use for snapshot lookup. |
| `approval_gate_service.py` | Existing service | Use for activation blockers. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Stage specs reject missing owner, object type, receipt, approval policy, and eval target. |
| Continuity tests | Invalid stage input/output chains block activation. |
| Gate tests | Missing consent, source truth, primitive, or approval stage blocks activation. |
| Runtime tests | Workflow run creation requires active snapshot ID. |
| Receipt tests | Activation receipt contains snapshot hash and gate verdicts. |
| Replay tests | Past runs resolve their historical manifest snapshot even after newer versions activate. |
