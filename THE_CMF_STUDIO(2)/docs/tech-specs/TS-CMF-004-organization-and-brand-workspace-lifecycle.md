---
tech_spec_id: "TS-CMF-004"
title: "Organization and Brand Workspace Lifecycle"
story_id: "1.2"
story_title: "Organization and Brand Workspace Lifecycle"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-1-2-organization-and-brand-workspace-lifecycle.md"
fr_ids:
  - "FR-CMF-01.01"
  - "FR-CMF-01.03"
pipeline_stage: "1"
entry_object: "organization / brand request"
exit_object: "BrandWorkspace lifecycle event"
validation_contract: "owner/admin role and brand scope"
required_receipt: "workspace receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / PostgreSQL RLS"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-004: Organization and Brand Workspace Lifecycle

**Status:** Ready for Development  
**Story:** `1.2 - Organization and Brand Workspace Lifecycle`  
**Implementation Boundary:** Organization records, brand workspace lifecycle state, active brand context, workspace receipts, workspace inspection APIs, and tenant isolation enforcement.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for multi-brand production, PWA/Telegram operations, and full-system scope. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-01.01 and FR-CMF-01.03 source authority. |
| `docs/architecture.md` | Architecture authority for tenancy, PostgreSQL canonical state, RLS, Command Bus, object storage paths, and receipt requirements. |
| `docs/cmf-studio-pipeline-map.md` | Stage 1 workspace and commercial setup trace. |
| `docs/migration/legacy-inventory.md` | Legacy tenant isolation doctrine and legacy-runtime-coupling migration boundary. |
| `docs/stories/story-1-2-organization-and-brand-workspace-lifecycle.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md` | Command mutation and audit receipt dependency. |
| `docs/tech-specs/TS-CMF-002-pipeline-stage-orchestration-records.md` | Orchestration and stage receipt dependency. |

## 2. Overview

### Problem Statement

CMF STUDIO operates across multiple client brands, each with transcripts, identity assets, provider jobs, render outputs, approvals, publishing state, memory, and cost records. If organization and brand workspace lifecycle state is treated as generic CRUD, suspended or archived workspaces can still receive production commands, and cross-brand queries can leak object IDs, asset previews, memory, or provider job state.

### Solution

Implement a brand-scoped workspace lifecycle service. Owners and Admins create, suspend, archive, restore, and inspect organizations and brand workspaces through typed commands. Workspace state is enforced by PostgreSQL RLS or equivalent repository predicates, Command Bus validation, object storage path policy, and inspection APIs that never return cross-brand data.

### Scope

In scope:

- `Organization`, `BrandWorkspace`, `ActiveBrandContext`, `WorkspaceLifecyclePolicy`, and `WorkspaceReceipt` contracts.
- Commands for create, suspend, archive, restore, inspect, and switch active brand context.
- One transaction for organization, brand workspace, initial role assignment, default retention policy, lifecycle event, and receipt creation.
- Workspace status enforcement in Command Bus validation.
- Read-only audit access for suspended or archived workspaces when permitted.
- Workspace inspection snapshot for status, roles, entitlement state, recent commands, blockers, and production health.

Out of scope:

- Billing provider integration.
- Brand Genesis identity manufacturing.
- UI implementation details for the dashboard.
- Legacy runtime coupling tenant code import.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-01.01 | Owners/Admins can create, suspend, archive, restore, and inspect organization and brand workspaces with isolated production context. | Workspace lifecycle commands, state transition policy, lifecycle events, inspection snapshots, RLS/repository predicates, and workspace receipts. |
| FR-CMF-01.03 | Operators explicitly switch active brand context, and every command/query/receipt/upload/render/memory admission binds to it. | `ActiveBrandContext`, brand-scoped query guard, command validation, object storage path policy, and no cross-brand query leakage. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `1 - Workspace and commercial setup` |
| Entry Object | Organization or brand request |
| Exit Object | `BrandWorkspace` lifecycle event |
| Allowed Actors / Services | Owner, Admin, WorkspaceService, Command Bus, recovery job for restore flows |
| Validation Contract | Owner/Admin role, active organization, brand scope, lifecycle state, receipt writer readiness |
| Required Receipt | Workspace receipt |
| Forbidden Shortcut | Direct brand workspace status edits, cross-brand object inspection, production commands against suspended or archived workspaces |

### Legacy Intelligence Mapping

The Legacy Inventory preserves tenant-isolation doctrine but does not provide runtime code. The old `coach_id` isolation pattern becomes organization and brand-workspace scoping across commands, events, storage paths, provider jobs, render contracts, evaluation receipts, Neo4j projection nodes, memory updates, and audit logs.

Target modules:

- `ccp_studio.contracts.tenancy`
- `ccp_studio.contracts.workspace_lifecycle`
- `ccp_studio.services.workspace_service`
- `ccp_studio.domain.policies.workspace_lifecycle_policy`
- `ccp_studio.repositories.organizations`
- `ccp_studio.repositories.brand_workspaces`
- `ccp_studio.api.v1.organizations`
- `ccp_studio.api.v1.brands`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `Organization` | Tenant owner boundary for brands, users, roles, and commercial state. |
| `BrandWorkspace` | Production boundary for brand-specific assets, sessions, commands, receipts, memory, provider jobs, and projections. |
| `WorkspaceLifecyclePolicy` | Valid status transitions and command allowances. |
| `ActiveBrandContext` | Actor-selected brand context for command and query binding. |
| `WorkspaceInspectionSnapshot` | Read model for dashboard status, roles, entitlements, blockers, and health. |
| `WorkspaceReceipt` | Lifecycle audit receipt. |

## 4. Implementation Plan

### Workstream A: Contracts

Define Pydantic contracts for organizations, brand workspaces, lifecycle status, active brand context, inspection snapshots, and workspace receipts.

### Workstream B: Persistence and Isolation

Add `organizations`, `brand_workspaces`, `active_brand_contexts`, and default retention policy records. Apply PostgreSQL RLS where available and repository-level predicates everywhere. Object storage paths must include `brands/{brand_id}/...` and content hashes.

### Workstream C: Lifecycle Commands

Implement typed command handlers behind TS-CMF-001:

- `CreateOrganizationCommand`
- `CreateBrandWorkspaceCommand`
- `SuspendBrandWorkspaceCommand`
- `ArchiveBrandWorkspaceCommand`
- `RestoreBrandWorkspaceCommand`
- `SwitchActiveBrandContextCommand`
- `InspectBrandWorkspaceCommand`

### Workstream D: Inspection Read Model

Build a read model that shows workspace status, active roles, entitlement state, recent commands, open blockers, production health, and last receipts without exposing cross-brand objects.

### Workstream E: Recovery and Restore

Restoration requires Owner/Admin command, lifecycle policy validation, and workspace receipt. Recovery jobs cannot restore by direct table edit.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class WorkspaceStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    archived = "archived"
    restoring = "restoring"


class Organization(BaseModel):
    schema_version: Literal["cmf.organization.v1"]
    organization_id: UUID
    name: str
    status: WorkspaceStatus
    created_at: datetime
    updated_at: datetime


class BrandWorkspace(BaseModel):
    schema_version: Literal["cmf.brand_workspace.v1"]
    brand_id: UUID
    organization_id: UUID
    display_name: str
    status: WorkspaceStatus
    default_retention_policy_id: UUID
    created_at: datetime
    updated_at: datetime


class ActiveBrandContext(BaseModel):
    schema_version: Literal["cmf.active_brand_context.v1"]
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    selected_at: datetime
    source_surface: str


class WorkspaceInspectionSnapshot(BaseModel):
    schema_version: Literal["cmf.workspace_inspection_snapshot.v1"]
    organization_id: UUID
    brand_id: UUID
    status: WorkspaceStatus
    active_role_count: int
    entitlement_state: str
    recent_command_ids: list[UUID] = Field(default_factory=list)
    open_blockers: list[str] = Field(default_factory=list)
    production_health: str
    last_receipt_id: UUID | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `CreateOrganizationCommand`, `CreateBrandWorkspaceCommand`, `SuspendBrandWorkspaceCommand`, `ArchiveBrandWorkspaceCommand`, `RestoreBrandWorkspaceCommand`, `SwitchActiveBrandContextCommand`, `InspectBrandWorkspaceCommand` |
| Events | `OrganizationCreated`, `BrandWorkspaceCreated`, `BrandWorkspaceSuspended`, `BrandWorkspaceArchived`, `BrandWorkspaceRestored`, `ActiveBrandContextSwitched` |
| Workflows | Workspace lifecycle transaction workflow, restore workflow |
| Receipts | `WorkspaceReceipt`, `AuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

No legacy tenancy code is imported. Legacy tenant semantics become fixtures and tests. If RLS is not available in a test profile, repository predicates remain mandatory.

Fallback behavior:

- Suspended workspace blocks new mutating production commands with `WORKSPACE_SUSPENDED`.
- Archived workspace blocks new production commands with `WORKSPACE_ARCHIVED`.
- Unauthorized cross-brand query returns an empty result or `NOT_FOUND`, never foreign object metadata.
- Restore without Owner/Admin role fails with `PERMISSION_DENIED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Fast setup wants generic workspace CRUD; CMF safety requires lifecycle status to govern every downstream production action. |
| UX / Ops Failure Scenario | A suspended brand still receives a render job, or a user sees Brand B previews while Brand A is active. |
| Resolution Demand | Workspace lifecycle authority takes precedence. Every command and query binds to organization, brand, role, and lifecycle state. |
| Downstream Proof | Tests must prove suspended/archived workspaces block mutation, restore requires receipt, active brand switching binds future commands, and cross-brand queries leak nothing. |

## 9. Tasks

- Define tenancy and lifecycle Pydantic contracts.
- Add organization and brand workspace migrations.
- Add lifecycle policy and state transition checks.
- Implement command handlers through TS-CMF-001.
- Implement active brand context switching.
- Implement workspace inspection snapshot.
- Add repository predicates and RLS policy checks.
- Add workspace lifecycle receipts.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Brand creation writes organization, brand workspace, initial role assignment, retention policy, domain event, and receipt in one transaction. | Brand workspace exists without initial role assignment. |
| AC2 | Suspended workspace blocks new mutating production work while preserving permitted read-only audit access. | Operator starts a render in suspended brand. |
| AC3 | Archived workspace restoration requires Owner/Admin command and audit receipt. | Support script flips status from archived to active. |
| AC4 | Inspection dashboard returns status, roles, entitlement state, recent commands, blockers, and production health. | Dashboard shows status only and hides blockers. |
| AC5 | Cross-brand query returns no Brand B object ID, title, preview, memory, or provider job to unauthorized users. | Brand A user sees Brand B thumbnail in search results. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-002 Orchestration records
- Role policy from TS-CMF-005
- Commercial policy from TS-CMF-006
- Pydantic contract generation

External:

- FastAPI
- Pydantic v2
- PostgreSQL with RLS where available
- SQLAlchemy v2

## 12. Testing Strategy

Unit tests:

- Workspace lifecycle transition table.
- Active brand context validation.
- Repository predicates include organization and brand scope.
- Workspace receipt schema.

Integration tests:

- Create brand workspace transaction.
- Suspend workspace and reject production command.
- Archive and restore with Owner/Admin command.
- Inspect workspace snapshot.
- Unauthorized cross-brand query returns no data.

Safety tests:

- Static route scan for direct lifecycle status edits.
- Object storage path guard includes brand ID.
- Recovery restore path goes through Command Bus.

## 13. Observability, Recovery, and Rollback

- Logs include `organization_id`, `brand_id`, `workspace_status`, `command_id`, and `correlation_id`.
- Metrics track workspace creation, suspension, archive, restore, failed cross-brand access, and blocked production commands.
- Rollback uses compensating lifecycle commands.
- Restore preserves old receipts and writes a new restore receipt.

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
| Requirement Trace | FR-CMF-01.01, FR-CMF-01.03 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Tenant isolation doctrine mapped to organization and brand workspace scope |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python contracts and Command Bus enforcement |
| TypeScript Boundary | PWA consumes workspace state only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

