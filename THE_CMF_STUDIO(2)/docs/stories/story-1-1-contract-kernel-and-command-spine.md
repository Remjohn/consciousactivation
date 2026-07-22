---
story_id: "1.1"
story_title: "Contract Kernel and Command Spine"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-01.03"
  - "FR-CMF-01.06"
pipeline_stage: "1 / cross-cutting"
entry_object: "command request"
exit_object: "command log, event, audit receipt"
validation_contract: "command envelope and brand scope"
required_receipt: "audit receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 1.1: Contract Kernel and Command Spine

**Epic:** 1 - Governed Workspace and Production Spine
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-01.03, FR-CMF-01.06 |
| Canonical Pipeline Stage | 1 / cross-cutting |
| Entry Object | command request |
| Exit Object | command log, event, audit receipt |
| Validation Contract | command envelope and brand scope |
| Required Receipt | audit receipt |
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

As an Owner, I want every production action to enter through a typed command spine, so that CMF STUDIO can govern state consistently before creative workflows begin.

**Acceptance Criteria:**

- Given a state-changing request reaches FastAPI, when it is accepted, then it is wrapped in a Pydantic command with `command_id`, `command_type`, `organization_id`, `brand_id`, `actor_id`, `idempotency_key`, `payload`, and `requested_at`.
- Given a command is processed, when validation runs, then it follows schema version, authentication, role permission, organization and brand scope, object existence, state transition, consent policy, cost/quota policy, idempotency, provider policy when relevant, confirmation, and receipt-writer checks.
- Given a command succeeds, when persistence completes, then the system writes `command_log`, a domain event, and an audit receipt with correlation ID.
- Given the same idempotency key is submitted again, when the command is replayed, then the system returns the prior command result without duplicating side effects.
- Given a command lacks brand scope, when validation runs, then it fails with `BRAND_SCOPE_VIOLATION`.

**Technical Notes:** Implement base command contracts under `ccp_studio/contracts`, Command Bus handlers under `ccp_studio/api/commands`, repository enforcement for `organization_id` and `brand_id`, and generated TypeScript contract output for PWA and Telegram consumers.

**Legacy and Primitive Mapping:** Legacy receipt-chain references inform audit receipt fields. Active families: SAF, BUS, FBK.

**Prerequisites:** None.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
