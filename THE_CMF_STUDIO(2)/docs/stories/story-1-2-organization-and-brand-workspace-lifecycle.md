---
story_id: "1.2"
story_title: "Organization and Brand Workspace Lifecycle"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-01.01"
  - "FR-CMF-01.03"
pipeline_stage: "1"
entry_object: "organization / brand request"
exit_object: "`BrandWorkspace` lifecycle event"
validation_contract: "owner/admin role and brand scope"
required_receipt: "workspace receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 1.2: Organization and Brand Workspace Lifecycle

**Epic:** 1 - Governed Workspace and Production Spine
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-01.01, FR-CMF-01.03 |
| Canonical Pipeline Stage | 1 |
| Entry Object | organization / brand request |
| Exit Object | `BrandWorkspace` lifecycle event |
| Validation Contract | owner/admin role and brand scope |
| Required Receipt | workspace receipt |
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

As an Owner or Admin, I want to create, suspend, archive, restore, and inspect organizations and brand workspaces, so that each client brand has an isolated production context.

**Acceptance Criteria:**

- Given an Owner creates a brand workspace, when the command succeeds, then `organizations`, `brand_workspaces`, initial role assignment, default retention policy, and domain event are created in one transaction.
- Given an Admin suspends a brand workspace, when an Operator tries to start new production work in that brand, then mutating commands are blocked while read-only audit access remains available to permitted roles.
- Given a workspace is archived, when recovery is requested, then restoration requires an Owner/Admin command and writes an audit receipt.
- Given a workspace is inspected, when the UI renders, then the dashboard shows status, active roles, entitlement state, recent commands, open blockers, and production health.
- Given Brand A is active, when a user queries Brand B objects without permission, then no Brand B object ID, title, asset preview, memory, or provider job is returned.

**Technical Notes:** Use `/api/v1/organizations` and `/api/v1/brands`; enforce RLS or equivalent repository checks; expose lifecycle events `BrandWorkspaceCreated`, `BrandWorkspaceSuspended`, `BrandWorkspaceArchived`, `BrandWorkspaceRestored`.

**Legacy and Primitive Mapping:** Adapts legacy tenant isolation doctrine to Python-first repository enforcement. Active families: SAF, PER, BUS.

**Prerequisites:** Story 1.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
