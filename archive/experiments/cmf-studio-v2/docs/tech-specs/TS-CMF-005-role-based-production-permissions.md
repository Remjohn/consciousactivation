---
tech_spec_id: "TS-CMF-005"
title: "Role-Based Production Permissions"
story_id: "1.3"
story_title: "Role-Based Production Permissions"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-1-3-role-based-production-permissions.md"
fr_ids:
  - "FR-CMF-01.02"
pipeline_stage: "1"
entry_object: "user and role request"
exit_object: "RoleAssignment"
validation_contract: "permission policy"
required_receipt: "role assignment receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / PostgreSQL"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-005: Role-Based Production Permissions

**Status:** Ready for Development  
**Story:** `1.3 - Role-Based Production Permissions`  
**Implementation Boundary:** Role assignment contracts, permission policy, command authorization, revocation enforcement, and role assignment receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for Operator, Reviewer, Migration Steward, Publishing Approver, and internal production roles. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-01.02 source authority and PWA/Telegram permission parity requirements. |
| `docs/architecture.md` | Architecture source for auth/RBAC, Command Bus validation, route boundaries, and Telegram initData verification. |
| `docs/cmf-studio-pipeline-map.md` | Stage 1 role segregation and Agent Gateway role-contract guidance. |
| `docs/migration/legacy-inventory.md` | ERA3 permission discipline and legacy spec governance as read-only doctrine. |
| `docs/stories/story-1-3-role-based-production-permissions.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md` | Command authorization dependency. |
| `docs/tech-specs/TS-CMF-004-organization-and-brand-workspace-lifecycle.md` | Organization and brand scope dependency. |

## 2. Overview

### Problem Statement

CMF STUDIO includes Owners, Admins, Operators, Reviewers, Migration Stewards, Production Stewards, Publishing Approvers, and Commercial Administrators. If roles are informal labels, Telegram quick actions and PWA workflows can approve publishing, modify commercial state, migrate legacy intelligence, or trigger production without the right authority.

### Solution

Implement role-based production permissions as Pydantic contracts and Command Bus validation policy. Every command derives permissions from active role assignment, organization scope, brand scope, command type, object state, and surface context. Revocation is immediate. PWA and Telegram use the same backend role checks.

### Scope

In scope:

- `RoleAssignment`, `PermissionPolicy`, `CommandPermission`, and `PermissionDecision` contracts.
- Assign, revoke, inspect, and evaluate role commands.
- Permission checks in Command Bus validation.
- Role matrix tests for allowed and blocked commands.
- Migration Steward approval receipt fields for source hash, target contract, fixture target, eval target, reviewer, and receipt.
- Shared PWA/Telegram role evaluation.

Out of scope:

- External identity provider selection.
- UI role management screens.
- Public customer role model beyond internal CMF production roles.
- Legacy runtime coupling auth implementation.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-01.02 | Owners/Admins can assign role-based permissions for Operators, Reviewers, Migration Stewards, Production Stewards, Publishing Approvers, and Commercial Administrators. | `RoleAssignment`, `PermissionPolicy`, command authorization checks, revocation handling, and role assignment receipts. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `1 - Workspace and commercial setup` |
| Entry Object | User and role request |
| Exit Object | `RoleAssignment` |
| Allowed Actors / Services | Owner, Admin, AuthService, RolePolicyService, Command Bus |
| Validation Contract | Permission policy |
| Required Receipt | Role assignment receipt |
| Forbidden Shortcut | Surface-specific role logic, cached role after revocation, publishing approval without Publishing Approver role |

### Legacy Intelligence Mapping

The Legacy Inventory informs permission discipline and spec governance but no legacy auth code is imported. Role policy is implemented in Python and referenced by Command Bus validation. Role names are product roles, not model personas. Pi and DSPy may operate as service actors only through assigned service permissions and allowed handoff packets.

Target modules:

- `ccp_studio.contracts.roles`
- `ccp_studio.contracts.permissions`
- `ccp_studio.services.role_policy`
- `ccp_studio.repositories.role_assignments`
- `ccp_studio.api.v1.auth`
- `ccp_studio.api.v1.roles`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `RoleAssignment` | Scoped role grant for actor, organization, and optional brand. |
| `PermissionPolicy` | Maps role, command type, object state, and surface to allow/deny. |
| `CommandPermission` | Atomic permission claim checked by Command Bus. |
| `PermissionDecision` | Deterministic authorization result with reason and evidence. |
| `RoleAssignmentReceipt` | Receipt for assignment, revocation, and migration approval actions. |

## 4. Implementation Plan

### Workstream A: Role Contracts

Define role keys and assignments for Owner, Admin, Operator, Reviewer, Migration Steward, Production Steward, Publishing Approver, Commercial Administrator, and service actors.

### Workstream B: Permission Policy

Implement a permission policy service that receives actor, command type, organization, brand, object state, and source surface. It returns an allow/deny decision with a stable code.

### Workstream C: Command Bus Integration

Install the permission policy as the role permission step in TS-CMF-001 validation. Re-check permissions on every command, including Telegram quick actions and replayed attempts.

### Workstream D: Revocation and Cache Safety

Role revocation must invalidate short-lived permission caches. Any cache may optimize reads but cannot allow stale permissions after revocation.

### Workstream E: Migration Steward Receipt Fields

When Migration Stewards approve migrated registry entries, record reviewer, source hash, target contract, fixture target, eval target, and receipt.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class RoleKey(str, Enum):
    owner = "owner"
    admin = "admin"
    operator = "operator"
    reviewer = "reviewer"
    migration_steward = "migration_steward"
    production_steward = "production_steward"
    publishing_approver = "publishing_approver"
    commercial_administrator = "commercial_administrator"
    service_actor = "service_actor"


class RoleAssignmentStatus(str, Enum):
    active = "active"
    revoked = "revoked"
    expired = "expired"


class RoleAssignment(BaseModel):
    schema_version: Literal["cmf.role_assignment.v1"]
    role_assignment_id: UUID
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID | None = None
    role_key: RoleKey
    status: RoleAssignmentStatus
    assigned_by_actor_id: UUID
    assigned_at: datetime
    revoked_at: datetime | None = None


class CommandPermission(BaseModel):
    schema_version: Literal["cmf.command_permission.v1"]
    permission_key: str
    command_type: str
    allowed_roles: list[RoleKey]
    requires_brand_scope: bool = True
    allowed_surfaces: list[str] = Field(default_factory=list)


class PermissionDecision(BaseModel):
    schema_version: Literal["cmf.permission_decision.v1"]
    actor_id: UUID
    command_type: str
    organization_id: UUID
    brand_id: UUID | None
    allowed: bool
    decision_code: str
    matched_role_assignment_ids: list[UUID] = Field(default_factory=list)
    decided_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `AssignRoleCommand`, `RevokeRoleCommand`, `InspectRoleAssignmentsCommand`, `EvaluateCommandPermissionCommand` |
| Events | `RoleAssigned`, `RoleRevoked`, `PermissionDenied`, `MigrationRegistryEntryApproved` |
| Workflows | Role assignment transaction workflow, revocation propagation workflow |
| Receipts | `RoleAssignmentReceipt`, `PermissionDecisionReceipt`, migration approval receipt |

## 7. Backward Compatibility and Migration Fallback

Legacy role assumptions become test fixtures only. If a migrated workflow lacks a role mapping, it defaults to denied until mapped.

Fallback behavior:

- Missing role returns `PERMISSION_DENIED`.
- Revoked role returns `ROLE_REVOKED`.
- Publishing approval without role returns `PUBLISHING_APPROVER_REQUIRED`.
- Migration approval missing source hash or target contract returns `MIGRATION_RECEIPT_INCOMPLETE`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Fast internal production wants broad access; CMF safety requires least-privilege actions tied to product responsibilities. |
| UX / Ops Failure Scenario | A Reviewer approves public publishing from Telegram or a Migration Steward promotes legacy material without eval target evidence. |
| Resolution Demand | Role policy takes precedence. Every command is authorized from current role assignments, organization scope, brand scope, and command type. |
| Downstream Proof | Tests must prove each role has at least one allowed and one blocked command, revocation is immediate, and PWA/Telegram decisions are identical. |

## 9. Tasks

- Define role and permission contracts.
- Add `role_assignments` migration and repository.
- Implement permission policy service.
- Integrate role validation into Command Bus.
- Add revocation propagation and cache invalidation.
- Add migration approval receipt fields.
- Add role matrix fixtures and tests.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | User command permissions derive from active role assignment, organization scope, and brand scope. | Actor with org-level role can mutate a brand they are not scoped to. |
| AC2 | Operator publishing approval fails with `PERMISSION_DENIED`. | Operator publishes publicly without Publishing Approver role. |
| AC3 | Migration Steward approval records reviewer, source hash, target contract, fixture target, eval target, and receipt. | Migration ledger entry is approved with no eval target. |
| AC4 | Telegram quick action uses the same role checks as PWA. | Telegram allows a rejected PWA action. |
| AC5 | Revoked role denies previously valid action immediately. | Cached permission permits action after revocation. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-004 Organization and Brand Workspace Lifecycle
- Auth service boundary
- Audit receipt writer

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- SQLAlchemy v2

## 12. Testing Strategy

Unit tests:

- Role assignment schema.
- Permission decision rules.
- Role revocation.
- Migration approval receipt completeness.

Integration tests:

- Assign role and allow expected command.
- Deny blocked command per role.
- Telegram and PWA permission parity.
- Revoke role and deny repeated command.

Safety tests:

- Publishing approval requires Publishing Approver.
- Commercial policy updates require Commercial Administrator.
- Service actors cannot exceed assigned service permissions.

## 13. Observability, Recovery, and Rollback

- Logs include `actor_id`, `role_assignment_id`, `organization_id`, `brand_id`, `command_type`, and decision code.
- Metrics track permission denied, role assigned, role revoked, stale permission prevented, and migration approval receipts.
- Rollback uses role revocation or compensating assignment commands.
- Recovery can rebuild permission audit view from role assignment events.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-01.02 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - ERA3 permission discipline mapped to Python policy and receipts |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python role policy, Pi as service actor only |
| TypeScript Boundary | PWA/Telegram consume generated role decisions only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

