---
tech_spec_id: "TS-CMF-120"
title: "OpenMontage Reference Adapter Governance"
story_id: "13.1"
story_title: "OpenMontage Reference Adapter Governance"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.01"
pipeline_stage: "cross-stage integration governance"
entry_object: "OpenSourceReferenceCandidate"
exit_object: "IntegrationAdapterDecisionReceipt"
validation_contract: "license, source hash, reference-only boundary, CMF ownership, doctrine compatibility, receipt chain"
required_receipt: "IntegrationAdapterDecisionReceipt"
runtime_target: "Python / Pydantic v2 / registry service / evaluation receipts / Operations Board"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-120: OpenMontage Reference Adapter Governance

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec protocol, existing backend mapping, ADR-05, CBAR, failure examples, and testing discipline. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for orchestration, routing, rejection, and cinematic meaning. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 mandate for verifiable artifact handling. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product requirement owner for FR-CMF-13.01. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` | Existing governance boundary for open-source references. |
| `THE CMF STUDIO/docs/architecture.md` | Current CMF architecture: Command Bus, Pydantic contracts, receipt chain, provider governance, review states. |
| `THE CMF STUDIO/src/ccp_studio/services/spec_governance.py` | Existing spec governance service to extend. |
| `THE CMF STUDIO/src/ccp_studio/services/registry_service.py` | Existing registry access service for integration candidate records. |
| `THE CMF STUDIO/src/ccp_studio/services/evaluation_receipt_service.py` | Existing receipt writer for adapter decision evidence. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Existing blocker service for license, architecture, and guest-data boundary failures. |
| `OpenMontage README.md` | Reference pattern: agentic video production pipeline and stage flow. |
| `OpenMontage AGENT_GUIDE.md` | Reference pattern: agent operating contract, rule zero, runtime lock, provider menu, checkpoints. |
| `OpenMontage docs/ARCHITECTURE.md` | Reference pattern: pipeline manifests, tools, schemas, project workspaces, checkpoints. |
| `OpenMontage docs/PROVIDERS.md` | Reference pattern: provider categories, capabilities, setup state, cost model. |

## 2. Overview

CMF may use OpenMontage as an architectural reference, but OpenMontage must not become production authority. This spec creates a CMF-native governance layer for external architecture references so that inspiration becomes typed adapter decisions, not copied code, vague prompts, or unreviewed production dependencies.

The service registers reference repositories, fetched document hashes, licenses, candidate patterns, prohibited uses, evaluation results, approval decisions, and downstream owner specs. For OpenMontage, the first accepted patterns are conceptual: pipeline manifests, stage director skills, tool registry, provider menu, provider scoring, project workspaces, checkpoints, runtime locking, pre-compose QA, post-render QA, and budget governance.

The service must block direct AGPLv3 code import, vendored runtime dependency, production execution on guest data, and any spec that says "use OpenMontage" without a CMF-owned adapter contract and decision receipt. The goal is not to diminish the reference. The goal is to protect CMF's interview-first object spine, doctrine gates, primitive evaluation, consent boundaries, provider receipts, and operator approval.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-120-001 | `OpenSourceReferenceCandidate` | Records repository URL, license, fetched document hashes, candidate patterns, and reference status. |
| DEP-CMF-120-002 | `ReferencePatternDecision` | Maps each adopted, blocked, lab-only, or reference-only pattern to a CMF owner spec and prohibited uses. |
| DEP-CMF-120-003 | `LicenseCompatibilityGate` | Blocks direct import, production dependency use, or copied implementation until legal and architecture review approve. |
| DEP-CMF-120-004 | `IntegrationAdapterDecisionReceipt` | Immutable receipt proving the decision, evidence, risk, owner, and downstream activation state. |
| DEP-CMF-120-005 | `ReferenceBoundaryViolation` | Blocker emitted when code, prompt, spec, or provider route crosses the approved boundary. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/registry.py` | Add Pydantic contracts for integration candidates, pattern decisions, license gates, and boundary violations. |
| `src/ccp_studio/services/spec_governance.py` | Add checks that specs referencing external repositories include approved `IntegrationAdapterDecisionReceipt` refs. |
| `src/ccp_studio/services/registry_service.py` | Store and query reference candidate and pattern decision registries. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | Emit hash-backed adapter decision receipts and license compatibility receipts. |
| `src/ccp_studio/services/approval_gate_service.py` | Add blockers for AGPL import, guest-data execution, missing owner spec, and unsupported pattern activation. |
| `src/ccp_studio/api/v1/registries.py` | Add endpoints for registration, evaluation, approval, blocking, and read-model retrieval. |
| `POST /api/v1/registries/integration-candidates`, `POST /api/v1/registries/reference-pattern-decisions`, `GET /api/v1/registries/integration-candidates/{candidate_id}` | Exact API routes for reference registration, decision recording, and inspection. |
| `src/ccp_studio/repositories/registry_entries.py` | Persist candidates and decisions using existing registry persistence conventions. |
| Postgres tables: `integration_reference_candidates`, `reference_pattern_decisions`, `integration_adapter_decision_receipts`, `approval_blockers` | Durable storage for source refs, pattern decisions, approval blockers, and replayable receipts. |
| `THE CMF STUDIO/registries/integrations/` | New registry namespace for `open_source_reference_patterns.v1.json`. |
| `THE CMF STUDIO/tests/cmf_studio/` | Add integration-governance tests using current pytest pattern. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-SOC-001` | Verifiable Artifact Rule | Every adopted pattern must have source, hash, decision receipt, and owner spec. |
| `EXP-FBK-001` | Actionable Rejection Rule | Rejections name exact license, architecture, data, or doctrine failure with next action. |
| `EXP-PRG-001` | Inline Routing SLA | Approved patterns route to a CMF owner spec and registry entry before activation. |
| `EXP-FRC-006` | Frictionless Block Rule | Blockers offer safe alternatives: reference-only, lab-only, adapter review, or full block. |
| `EXP-TRS-004` | Cinematic Meaning Rule | External patterns cannot flatten CMF's interview-first source truth or composition doctrine. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | External references cannot influence production until evaluated and approved. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Decision must identify owner spec, registry path, implementation boundary, and eval target. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Every blocked pattern returns reason, evidence, risk class, and allowed next action. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Every decision writes a hash-backed receipt and can be replayed from source evidence. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Treat OpenMontage as reference evidence, not runtime authority. | Avoids license drift and protects CMF's Python/Pydantic object spine. |
| Store fetched document hashes. | Enables repeatable audits when external repositories change. |
| Require owner specs for approved patterns. | Prevents "inspired by" from becoming hidden architecture. |
| Block guest-data execution in `reference_only` or `lab_only` status. | Preserves consent, privacy, and production lineage. |
| Use existing registry and receipt services first. | Keeps this as an extension, not a parallel governance system. |

## 4. Implementation Plan

1. Add integration candidate and decision contracts to `src/ccp_studio/contracts/registry.py` or a dedicated `contracts/integrations.py` if the registry file becomes too large.
2. Add `integration_adapter_governance_service.py` to register source references, hash fetched docs, extract candidate patterns, and evaluate boundary risk.
3. Add registry persistence through `registry_entries.py` with deterministic keys: `integration_candidate:{repo_slug}:{version}` and `reference_pattern:{candidate_id}:{pattern_id}`.
4. Add license compatibility gate to `approval_gate_service.py`.
5. Add spec-governance lint that rejects references to OpenMontage or other OSS repos without decision receipt refs.
6. Add endpoints under `api/v1/registries.py` for registration, evaluation, approval, blocking, and read-model inspection.
7. Add `registries/integrations/open_source_reference_patterns.v1.json` with OpenMontage candidate pattern IDs and statuses.
8. Add Operations Board read model showing adopted patterns, blocked patterns, license state, owner specs, and next actions.
9. Emit `IntegrationAdapterDecisionReceipt` on every approve, block, or status change.
10. Add pytest fixtures for AGPL block, reference-only data boundary, owner-spec requirement, and replay hash integrity.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


class OpenSourceReferenceCandidate(BaseModel):
    schema_version: Literal["cmf.integration_candidate.v1"]
    candidate_id: str
    repo_name: str
    repo_url: HttpUrl
    license_id: str
    fetched_document_hashes: dict[str, str]
    candidate_pattern_ids: list[str]
    registered_by: str
    registered_at: str


class ReferencePatternDecision(BaseModel):
    schema_version: Literal["cmf.reference_pattern_decision.v1"]
    decision_id: str
    candidate_id: str
    pattern_id: str
    pattern_name: str
    status: Literal["reference_only", "adapter_now", "lab_only", "blocked"]
    cmf_owner_spec_id: str | None = None
    prohibited_uses: list[str] = Field(default_factory=list)
    required_eval_target_ids: list[str] = Field(default_factory=list)
    rationale: str
    evidence_hashes: dict[str, str]


class IntegrationAdapterDecisionReceipt(BaseModel):
    schema_version: Literal["cmf.integration_adapter_decision_receipt.v1"]
    receipt_id: str
    decision_id: str
    candidate_id: str
    license_gate_verdict: Literal["pass", "review_required", "blocked"]
    architecture_gate_verdict: Literal["pass", "review_required", "blocked"]
    guest_data_boundary: Literal["production_allowed", "lab_only", "reference_only", "blocked"]
    approved_by: str | None = None
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing specs and code that do not reference external repositories continue to operate unchanged. Existing provider, rendering, and review services keep their current behavior until an approved adapter decision activates a new pattern. If OpenMontage source evidence is unavailable, the system can keep a manually registered reference candidate in `reference_only` status, but it cannot activate downstream implementation tasks, provider behavior, or runtime dependencies.

Fallback must never silently downgrade governance. If a decision receipt is missing, the system blocks the spec or implementation route and gives the operator a repair command: register source, add hash evidence, map owner spec, or mark blocked.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T120-01 | Contracts | Add integration candidate, pattern decision, license gate, and receipt models. |
| T120-02 | Services | Implement governance evaluation and status transition service. |
| T120-03 | Registry | Create integration reference registry namespace and OpenMontage seed records. |
| T120-04 | API | Add register, evaluate, approve, block, and inspect endpoints. |
| T120-05 | Gates | Add license, data-boundary, and owner-spec blockers. |
| T120-06 | Review UI | Add Operations Board panel for reference decisions. |
| T120-07 | Tests | Add governance fixtures and failure tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC120-01 | OpenMontage cannot be cited by production specs without a registered candidate and decision receipt. | A spec says "use OpenMontage tool registry" but has no receipt ref. | Phase5-M01; spec-governance lint test. |
| AC120-02 | AGPLv3 direct code import is blocked unless legal and architecture review approve. | OpenMontage code is copied into `src/ccp_studio` as a utility. | Phase4-M01; dependency/import scanner fixture. |
| AC120-03 | Every adopted pattern maps to a CMF owner spec and output contract. | Provider menu pattern is approved with no CMF provider contract owner. | Phase4-M03; pattern decision schema test. |
| AC120-04 | `reference_only` and `lab_only` patterns cannot execute on guest data. | A lab script processes a real guest interview upload. | Phase4-M05; guest-data boundary test. |
| AC120-05 | Blocked patterns return actionable next steps. | Operator sees "license issue" with no repair path. | Phase4-M05; blocker payload assertion. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-076` | Upstream governance | Must be read and extended, not duplicated. |
| `spec_governance.py` | Existing service | Extend with external-reference lint checks. |
| `registry_service.py` | Existing service | Reuse for reference pattern registry. |
| `evaluation_receipt_service.py` | Existing service | Reuse for decision receipts. |
| `approval_gate_service.py` | Existing service | Reuse for blocker emission. |
| OpenMontage docs | External reference | Hash and register; do not execute as runtime. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Candidate, decision, license gate, and receipt schemas validate and reject missing evidence. |
| Registry tests | OpenMontage seed record loads with deterministic hashes and pattern IDs. |
| Spec lint tests | Specs referencing external repos fail without approved decision receipt. |
| Boundary tests | `reference_only` and `lab_only` statuses block guest-data execution. |
| License tests | AGPL direct-import attempts create blockers. |
| Receipt replay tests | Decision receipt can be reconstructed from candidate, pattern decision, evidence hashes, and approval state. |
