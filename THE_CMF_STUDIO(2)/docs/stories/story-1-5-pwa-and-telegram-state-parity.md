---
story_id: "1.5"
story_title: "PWA and Telegram State Parity"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-01.03"
  - "FR-CMF-01.07"
pipeline_stage: "1 / 13"
entry_object: "PWA or Telegram action"
exit_object: "canonical command result"
validation_contract: "same state and role validation"
required_receipt: "command receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 1.5: PWA and Telegram State Parity

**Epic:** 1 - Governed Workspace and Production Spine
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-01.03, FR-CMF-01.07 |
| Canonical Pipeline Stage | 1 / 13 |
| Entry Object | PWA or Telegram action |
| Exit Object | canonical command result |
| Validation Contract | same state and role validation |
| Required Receipt | command receipt |
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

As an Operator, I want PWA Control Tower and Telegram actions to operate on the same governed object state, so that mobile approvals and notifications cannot fork production reality.

**Acceptance Criteria:**

- Given an object is visible in PWA, when a Telegram notification deep-links to it, then the Telegram payload references the same object ID, brand ID, state, and required command.
- Given a Telegram quick action is submitted, when FastAPI receives it, then it validates Telegram authentication, role, brand scope, idempotency, object state, and receipt writer availability.
- Given a PWA action and Telegram action target the same object, when one succeeds first, then the second sees the updated canonical state and cannot overwrite it blindly.
- Given Telegram cannot show enough evidence for a complex decision, when the user attempts approval, then the bot deep-links to the PWA review surface instead of allowing blind approval.
- Given a state change occurs in PWA, when Telegram renders a follow-up notification, then it reflects the latest canonical state.

**Technical Notes:** Use `/api/v1/webhooks/telegram`, generated TS contracts, command idempotency, and event-driven notifications. Telegram Bot and Mini App are leaf surfaces only.

**Legacy and Primitive Mapping:** Legacy Telegram/Mini App patterns are reference only; state belongs to Python backend. Active families: FRC, FBK, SAF.

**Prerequisites:** Stories 1.1 through 1.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
