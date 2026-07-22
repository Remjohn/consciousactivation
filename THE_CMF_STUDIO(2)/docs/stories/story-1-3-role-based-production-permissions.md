---
story_id: "1.3"
story_title: "Role-Based Production Permissions"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-01.02"
pipeline_stage: "1"
entry_object: "user and role request"
exit_object: "`RoleAssignment`"
validation_contract: "permission policy"
required_receipt: "role assignment receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 1.3: Role-Based Production Permissions

**Epic:** 1 - Governed Workspace and Production Spine
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-01.02 |
| Canonical Pipeline Stage | 1 |
| Entry Object | user and role request |
| Exit Object | `RoleAssignment` |
| Validation Contract | permission policy |
| Required Receipt | role assignment receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Create the governed product spine that lets the CMF team operate multiple brands, roles, commands, commercial entitlements, receipts, and PWA/Telegram surfaces over the same canonical state.

**Covers:** FR-CMF-01.01 through FR-CMF-01.07.

**User Value:** Owners, Admins, Operators, and commercial administrators can run production without cross-brand leakage, pricing drift, or separate state machines.

**Technical Context:** `contracts/tenancy.py`, `contracts/commercial.py`, `/api/v1/organizations`, `/api/v1/brands`, `/api/v1/auth`, Command Bus, `organizations`, `brand_workspaces`, `role_assignments`, `commercial_entitlements`, `command_log`, `domain_events`, `audit_receipts`.

**CBAR Failure Scenario:** If the system treats workspace setup as generic CRUD, then Telegram actions, provider jobs, memory, and publishing can mutate the wrong brand or expose the wrong offer. The story set therefore locks brand scope and command receipts before creative workflows begin.

## Story Definition

As an Owner or Admin, I want role assignments for Operators, Reviewers, Migration Stewards, Production Stewards, Publishing Approvers, and commercial administrators, so that each actor can only perform the work they are trusted to perform.

**Acceptance Criteria:**

- Given a user receives a role assignment, when they authenticate, then their command permissions are derived from active role assignment, organization scope, and brand scope.
- Given an Operator attempts a Publishing Approval command without the required role, when validation runs, then the command is rejected with `PERMISSION_DENIED`.
- Given a Migration Steward accesses the migration ledger, when they approve a migrated registry entry, then the system records reviewer, source hash, target contract, fixture target, eval target, and receipt.
- Given a Reviewer acts through Telegram, when the quick action reaches FastAPI, then the same role checks apply as PWA.
- Given a role is revoked, when a user repeats a previously valid action, then the action is denied immediately.

**Technical Notes:** Model `RoleAssignment`, `PermissionPolicy`, and command permissions as Pydantic contracts; use repository joins against `role_assignments`; test every role against at least one allowed and one blocked command.

**Legacy and Primitive Mapping:** ERA3 spec discipline requires permission checks in downstream tech specs. Active families: SAF, PER.

**Prerequisites:** Stories 1.1 and 1.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
