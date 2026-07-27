---
tech_spec_id: "TS-CMF-131"
title: "Budget, Cost, and Resource Governance"
story_id: "13.12"
story_title: "Budget, Cost, and Resource Governance"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.12"
pipeline_stage: "provider spend, GPU worker, budget, and usage governance"
entry_object: "CostReservationRequest"
exit_object: "CostGovernanceReceipt"
validation_contract: "estimate, reserve, execute, reconcile, package policy, retry policy, provider usage, GPU resource state"
required_receipt: "CostGovernanceReceipt"
runtime_target: "Python / Pydantic v2 / usage ledger / provider operations / commercial policy / Operations Board"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-131: Budget, Cost, and Resource Governance

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Provider/resource blockers and routing mandates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact and paywall/offer constraints. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.12. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-006-commercial-entitlements-without-offer-drift.md` | Commercial entitlement dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-042-provider-capability-registry-and-job-receipts.md` | Provider job receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-045-self-hosted-comfyui-docker-gpu-worker.md` | GPU worker cost dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-123-capability-tool-registry-and-provider-menu.md` | Provider capability state dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/usage_ledger_service.py` | Existing usage ledger owner. |
| `THE CMF STUDIO/src/ccp_studio/services/commercial_policy_service.py` | Existing commercial policy owner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Provider usage owner. |
| `THE CMF STUDIO/src/ccp_studio/services/comfy_gpu_worker_service.py` | GPU runtime owner. |
| `OpenMontage docs/PROVIDERS.md` | Reference pattern for estimate, reserve, reconcile cost lifecycle. |

## 2. Overview

CMF uses multiple expensive providers and self-hosted GPU resources. Without explicit cost governance, the factory can become operationally unpredictable even when creative quality is high. This spec adapts OpenMontage's estimate, reserve, execute, and reconcile lifecycle into CMF's provider and worker governance.

Before provider jobs, GPU workers, render batches, music generation, video generation, image generation, TTS, stock retrieval, or paid API calls execute, the system estimates cost, checks package policy, reserves budget, and raises approval thresholds when needed. After execution, it reconciles actual spend, provider-reported usage, output hashes, retry count, worker time, GPU tier, and cost variance.

Budget rules are brand-scoped and package-aware: $99/month guest packs, $29/week trial guest packs, experimental renders, failed jobs, and operator-approved retries must be visible separately. The system supports `observe`, `warn`, and `cap` modes. Public production should block surprise spend.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-131-001 | `CostReservationRequest` | Request to estimate and reserve cost before provider/GPU work. |
| DEP-CMF-131-002 | `CostEstimate` | Estimate by provider, capability, GPU tier, duration, retry policy, and package context. |
| DEP-CMF-131-003 | `BudgetReservation` | Holds approved amount, mode, expiry, and policy refs. |
| DEP-CMF-131-004 | `CostReconciliationRecord` | Actual spend, usage, variance, retries, output hashes, and worker time. |
| DEP-CMF-131-005 | `CostGovernanceReceipt` | Receipt linking selection, reservation, execution, reconciliation, and blockers. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/commercial.py` | Add cost estimate, reservation, reconciliation, and receipt models. |
| `src/ccp_studio/services/usage_ledger_service.py` | Own estimate/reserve/reconcile ledger entries. |
| `src/ccp_studio/services/commercial_policy_service.py` | Enforce package, trial, monthly, experimental, retry, and cap policies. |
| `src/ccp_studio/services/provider_operations_service.py` | Attach provider usage and job receipt data. |
| `src/ccp_studio/services/comfy_gpu_worker_service.py` | Report GPU worker time, tier, queue, and cost class. |
| `src/ccp_studio/api/v1/commercial.py` | Add budget policy, reserve, reconcile, and inspect endpoints. |
| `POST /api/v1/commercial/budget/estimate`, `POST /api/v1/commercial/budget/reserve`, `POST /api/v1/commercial/budget/reconcile`, `GET /api/v1/commercial/budget/{workspace_id}` | Exact API routes for budget estimate, reservation, reconciliation, and workspace spend inspection. |
| `src/ccp_studio/repositories/usage_ledger.py` | Persist reservations, actual usage, variance, and receipts. |
| Postgres tables: `budget_reservations`, `provider_cost_ledger_entries`, `gpu_worker_usage_entries`, `budget_reconciliation_receipts`, `package_entitlement_states` | Durable storage for costs, package limits, reservations, actuals, and reconciliation evidence. |
| `src/ccp_studio/services/operations_board_service.py` | Surface brand/package spend and blockers. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-FBK-001` | Actionable Rejection | Budget blocks name cost, threshold, package, and repair options. |
| `EXP-SOC-001` | Verifiable Artifact | Estimate, reservation, usage, and reconciliation are receipt-backed. |
| `EXP-FRC-002` | 1-Tap Paywall / Friction | Trial/monthly package states must be explicit and not surprise users/operators. |
| `EXP-PRG-001` | Inline Routing SLA | Cost check runs before provider job creation. |
| `EXP-FRC-006` | Frictionless Block | Cap/warn/observe modes give clear next actions. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Provider job creation requires cost reservation where applicable. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Budget blockers include amount, policy, threshold, and repair route. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Cost receipts link estimate, reservation, execution, and reconciliation. |
| Phase5-M05: 1-Tap Paywall Rule | Phase 5 Story 3.1 | `EXP-FRC-002` | Package entitlements and trial/monthly limits are visible before spend. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Cost governance happens before provider job creation. | Prevents surprise spend. |
| Reconciliation is required after execution. | Estimates alone are not operational truth. |
| Budget is brand/package scoped. | Trial packs and monthly packs have different constraints. |
| Failed jobs and retries are visible. | Helps diagnose provider reliability and cost variance. |

## 4. Implementation Plan

1. Add cost estimate, reservation, reconciliation, and receipt contracts.
2. Extend commercial policy with package-aware budget modes for $99/month and $29/week trial guest packs.
3. Add estimate and reserve flow before provider job, render batch, GPU worker, or paid API execution.
4. Capture provider-reported usage, GPU worker duration, retry count, output hashes, and actual cost.
5. Reconcile actual spend against reservation and create variance record.
6. Add approval thresholds for cap/warn modes.
7. Add Operations Board budget read model by brand, package, provider, capability, and run.
8. Add tests for estimate/reserve/reconcile, budget caps, retries, failed jobs, and package visibility.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class CostEstimate(BaseModel):
    schema_version: Literal["cmf.cost_estimate.v1"]
    estimate_id: str
    organization_id: str
    brand_id: str
    package_type: Literal["monthly_guest_pack", "trial_guest_pack", "experimental", "internal"]
    capability_request_id: str
    provider_capability_id: str
    estimated_cost_usd: float = Field(ge=0)
    confidence: Literal["low", "medium", "high"]
    assumptions: list[str] = Field(default_factory=list)


class BudgetReservation(BaseModel):
    schema_version: Literal["cmf.budget_reservation.v1"]
    reservation_id: str
    estimate_id: str
    mode: Literal["observe", "warn", "cap"]
    approved_amount_usd: float = Field(ge=0)
    approval_required: bool
    expires_at: str


class CostGovernanceReceipt(BaseModel):
    schema_version: Literal["cmf.cost_governance_receipt.v1"]
    receipt_id: str
    reservation_id: str
    provider_job_id: str | None = None
    estimated_cost_usd: float
    actual_cost_usd: float | None = None
    variance_usd: float | None = None
    retry_count: int = 0
    output_hashes: dict[str, str] = Field(default_factory=dict)
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing completed provider jobs can be imported into the usage ledger as historical usage if data exists. New paid or GPU-backed jobs must create cost reservations before execution. If pricing data is unknown, the system enters `warn` or `cap` mode depending on policy and requires operator approval before execution.

If reconciliation cannot determine actual cost, the job is marked `cost_reconciliation_pending` and cannot be used to update package profitability metrics until resolved.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T131-01 | Contracts | Add estimate, reservation, reconciliation, receipt. |
| T131-02 | Commercial Policy | Encode monthly/trial package cost policy. |
| T131-03 | Usage Ledger | Implement estimate/reserve/reconcile lifecycle. |
| T131-04 | Provider Ops | Attach provider usage and retry data. |
| T131-05 | GPU Worker | Report worker duration/tier/cost class. |
| T131-06 | Operations Board | Add cost and budget read model. |
| T131-07 | Tests | Add reservation, cap, retry, failed-job, and reconciliation tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC131-01 | Paid/GPU provider jobs require estimate and reservation before execution. | ComfyUI GPU job starts with no cost reservation. | Phase4-M03; provider job gate test. |
| AC131-02 | Budget blockers name amount, policy, package, and repair route. | Operator sees "budget exceeded" with no details. | Phase4-M05; blocker payload test. |
| AC131-03 | Actual usage reconciles against reservation after execution. | Provider reports usage but ledger remains estimate-only. | Phase5-M01; reconciliation test. |
| AC131-04 | Monthly and trial guest packs expose separate spend. | Trial pack spend is mixed with monthly production. | Phase5-M05; package ledger test. |
| AC131-05 | Failed jobs and retries remain visible. | Failed provider calls disappear from cost reports. | Phase5-M01; retry/failure test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-006` | Commercial entitlements | Package policy source. |
| `TS-CMF-042` | Provider receipts | Provider usage linkage. |
| `TS-CMF-045` | GPU worker | Worker resource data. |
| `TS-CMF-123` | Provider menu | Capability state and cost classes. |
| `usage_ledger_service.py` | Existing service | Extend. |
| `commercial_policy_service.py` | Existing service | Enforce. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Cost estimate, reservation, reconciliation, and receipt validate. |
| Reservation tests | Provider jobs cannot start without applicable reservation. |
| Policy tests | Trial/monthly/experimental/internal package rules are distinct. |
| Reconciliation tests | Actual spend, variance, retries, and output hashes are recorded. |
| Blocker tests | Cap/warn/observe modes produce correct operator actions. |
| Read-model tests | Operations Board shows brand/package spend, variance, and pending reconciliation. |
