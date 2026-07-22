---
tech_spec_id: "TS-CMF-143"
title: "Operator Auth, Scope, Permission, and Contract Version Gates"
story_id: "15.8"
story_title: "Protect Every Operator Surface With Scope and Version Gates"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-01"
  - "FR-CMF-02"
  - "FR-CMF-03"
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "auth, scope selection, permission enforcement, consent gates, and generated contract compatibility"
entry_object: "OperatorSession, BrandGuestScopeState, GeneratedContractVersion"
exit_object: "OperatorAccessDecision, ScopeGateReceipt, ContractVersionGateReceipt"
validation_contract: "authenticated actor, role permissions, brand/guest scope, consent state, commercial policy, contract version compatibility"
required_receipt: "ScopeGateReceipt"
runtime_target: "FastAPI auth dependency / React scope provider / Telegram auth / Command Bus policy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-143: Operator Auth, Scope, Permission, and Contract Version Gates

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture.md` | Defines auth provider open question, RBAC, consent, command boundary, and Telegram initData validation. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-004-organization-and-brand-workspace-lifecycle.md` | Workspace lifecycle dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-005-role-based-production-permissions.md` | Role permission dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-008-versioned-consent-records.md` | Consent dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-010-consent-blockers-across-workflows.md` | Consent blocker dependency. |
| `THE CMF STUDIO/src/ccp_studio/contracts/operator_ui.py` | Existing `BrandGuestScopeState`, `UiCommandEnvelope`, and shell contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/command_bus.py` | Existing validation path includes auth, role permission, brand scope, object existence, transition, consent, quotas, and confirmations. |
| `THE CMF STUDIO/src/ccp_studio/services/role_policy.py` | Role command handler owner. |
| `THE CMF STUDIO/src/ccp_studio/services/consent_service.py` | Consent state service owner. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/webhooks/telegram.py` | Telegram auth/initData precedent. |

## 2. Overview

CMF Studio will handle multiple brand workspaces, guests, interview assets, source media, likeness rights, approval states, and publishing decisions. The operator UI and Telegram surface therefore need strict gates: who is acting, under which role, for which organization, brand, guest, object, contract version, and consent state.

This spec defines shared access decisions for PWA, Telegram, command console, Pi-originated proposals, and API clients. It does not choose a final auth provider; it defines the CMF boundary that any provider must satisfy. The backend must return explicit `OperatorAccessDecision` and `ScopeGateReceipt` objects. The frontend must not render commandable controls until scope and contract version are current.

The user has emphasized guest workspace isolation repeatedly. This spec makes that isolation enforceable.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-143-001 | `OperatorSession` | Authenticated actor, roles, organization, and session metadata. |
| DEP-CMF-143-002 | `OperatorAccessDecision` | Allow/block decision for route, object, or command. |
| DEP-CMF-143-003 | `ScopeGateReceipt` | Receipt proving scope validation. |
| DEP-CMF-143-004 | `ContractVersionGateReceipt` | Receipt proving frontend/backend contract compatibility. |
| DEP-CMF-143-005 | `ConsentAccessGate` | Blocks actions requiring consent, likeness, or voice rights. |
| DEP-CMF-143-006 | `CommercialAccessGate` | Blocks unsupported offer/publishing paths. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `services/command_bus.py` | Reuse validation path but expose preflight access decision for UI. |
| `services/role_policy.py` | Provide command and route permission checks. |
| `services/consent_service.py` | Provide consent and likeness blocker checks. |
| `api/v1/operator_ui.py` | Add scope preflight endpoint. |
| `operator-web` | Use scope gate before rendering commandable controls. |
| `api/v1/webhooks/telegram.py` | Apply same scope/access decision to Telegram surface actions. |

### ADR-05 Primitive Implementation

Primitive/eval gates do not replace auth or consent. They are additional blockers after access is allowed. Access gate must pass before primitive/eval actions are visible.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase1-M05 Deterministic Override | Stale contract or object version blocks actions. |
| Phase4-M04 Frictionless Block | Scope/permission block explains required role, consent, or route. |
| Phase5-M01 Verifiable Artifact | Scope gate and contract version gate emit receipts. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-01 | Organization, brand workspace, role, and commercial permissions enforced. |
| FR-CMF-02 | Consent, source, likeness, and voice governance enforced before action. |
| FR-CMF-03 | Generated contract version is a startup and command gate. |
| FR-CMF-09 | Review/approval permissions and evidence gates are enforced. |
| FR-CMF-10 | Operations and recovery actions remain scoped and auditable. |

## 5. Canonical Pipeline Stage Trace

Every pipeline stage uses the same scope gate. More sensitive stages add stricter policy:

| Stage | Special Gate |
|---|---|
| Recording | Consent and source artifact readiness. |
| Voice/likeness | Likeness, voice DNA, and consent state. |
| Review/approval | Reviewer role and evidence sufficiency. |
| Publishing | Publishing intent, commercial policy, and approval receipt. |
| Memory | Memory admission authority and correction/quarantine state. |

## 6. Greenfield Integration and Legacy Migration Context

Old repo auth assumptions must not be imported. CMF may preserve permission ideas only after mapping them to `RolePermission`, `CommandPermission`, and `OperatorAccessDecision`.

## 7. Architecture Component Map

| Component | Owner | Responsibility |
|---|---|---|
| `AuthDependency` | API | Resolve `OperatorSession`. |
| `AccessGateService` | Backend | Route/object/command preflight decisions. |
| `ScopeGateService` | Backend | Validate organization, brand, guest, object version. |
| `ContractVersionGate` | Backend/frontend | Block incompatible generated consumers. |
| `ScopeProvider` | Frontend | Store active scope and gate commandable UI. |
| `TelegramScopeGate` | Backend | Apply same access logic to Telegram actions. |

## 8. Implementation Plan

1. Add `OperatorSession`, `OperatorAccessDecision`, `ScopeGateReceipt`, and `ContractVersionGateReceipt` contracts.
2. Add `AccessGateService.preflight_route()` and `preflight_command()`.
3. Add `/api/v1/operator-ui/scope/preflight`.
4. Add contract version header: request `X-CMF-Contract-Version`, response current required version.
5. Add frontend scope provider that loads shell, loads active brand/guest scope, and blocks command controls until access decision passes.
6. Add Telegram scope gate for quick actions and Mini App requests.
7. Add Command Bus integration so preflight and submit share policy logic.
8. Add tests for wrong guest, wrong role, stale contract, missing consent, and suspended workspace.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class OperatorSession(BaseModel):
    schema_version: Literal["cmf.operator_session.v1"] = "cmf.operator_session.v1"
    operator_user_id: UUID
    organization_id: UUID
    role_keys: list[str] = Field(min_length=1)
    auth_provider: str = Field(min_length=1)
    session_expires_at: datetime | None = None

class OperatorAccessDecision(BaseModel):
    schema_version: Literal["cmf.operator_access_decision.v1"] = "cmf.operator_access_decision.v1"
    decision_id: UUID
    allowed: bool
    operator_user_id: UUID
    organization_id: UUID
    brand_workspace_id: UUID | None = None
    guest_id: UUID | None = None
    active_object_type: str | None = None
    active_object_id: UUID | None = None
    route_key: str | None = None
    command_type: str | None = None
    blocker_codes: list[str] = Field(default_factory=list)
    required_actions: list[str] = Field(default_factory=list)

class ScopeGateReceipt(BaseModel):
    schema_version: Literal["cmf.scope_gate_receipt.v1"] = "cmf.scope_gate_receipt.v1"
    receipt_id: UUID
    access_decision_id: UUID
    object_version_checked: str | None = None
    contract_version_checked: str | None = None
    gate_status: Literal["passed", "blocked", "stale", "contract_mismatch"]
    created_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `OperatorAccessDecision` | Required for command preflight. |
| `ScopeGateReceipt` | Required when action is blocked or submitted. |
| `ContractVersionGateReceipt` | Required on frontend startup and command submit. |
| `operator.scope.blocked` | Event when scope gate fails. |
| `operator.contract_version.blocked` | Event when frontend/backend contracts drift. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

No intelligence service may override access gates. If an agent or JIT skill proposes a command, it inherits the actor and stage access policy.

## 12. Provider, Renderer, Projection, or Worker Boundaries

Workers and providers receive scoped job contracts only after access and command validation. They never evaluate user permissions themselves.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Operators need speed across guests; scope mistakes are catastrophic. |
| Failure Scenario | Operator commands a Claude revision while Adele is active. |
| Resolution Demand | Scope gate blocks object mismatch before command submit. |
| Downstream Proof | Scope gate receipt records object, guest, workspace, and decision. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC143-01 | Commandable UI is hidden or disabled until scope gate passes. | Button submits before shell state loads. | Phase4-M04 |
| AC143-02 | Wrong guest/object relation blocks command. | Adele command targets Claude asset id. | Phase1-M05 |
| AC143-03 | Missing consent blocks likeness/voice/publishing actions. | Voice-DNA boost requested with no consent. | Phase4-M04 |
| AC143-04 | Contract version mismatch blocks startup or command submit. | UI sends outdated envelope schema. | Phase1-M05 |
| AC143-05 | Telegram actions use same access service. | Telegram approves object outside operator role. | Phase5-M01 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-004 | Workspace lifecycle. |
| TS-CMF-005 | Role permissions. |
| TS-CMF-008 | Consent records. |
| TS-CMF-010 | Consent blockers. |
| TS-CMF-136 | Operator web API client. |
| TS-CMF-137 | Production app composition. |
| TS-CMF-141 | Telegram integration. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Unit | Access decision blocks wrong role, wrong guest, and stale version. |
| Unit | Contract version gate blocks mismatch. |
| Integration | UI preflight and Command Bus submit share same decision logic. |
| Telegram | Quick action blocked for wrong scope or expired session. |
| Negative | Suspended workspace blocks all production actions. |

## 17. Observability, Recovery, and Rollback

1. Log blocked access decisions with safe reason codes.
2. Do not log sensitive source text in auth logs.
3. Allow operator to switch scope and retry after read-model refresh.
4. Roll back a broken contract build by serving previous generated contract version only if backend supports it.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-143 |
| Protocol | CMF/ERA3 18-section spec |
| Guest workspace isolation | Required |
| Auth provider agnostic | Yes |
| Contract version gate | Required |
| Status | ready-for-development |
