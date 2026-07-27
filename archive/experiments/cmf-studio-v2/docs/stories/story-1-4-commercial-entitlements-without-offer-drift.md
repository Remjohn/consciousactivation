---
story_id: "1.4"
story_title: "Commercial Entitlements Without Offer Drift"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-01.04"
  - "FR-CMF-01.05"
pipeline_stage: "1 / 8"
entry_object: "entitlement request"
exit_object: "`CommercialPolicy`, cost receipt"
validation_contract: "`$29/week` or `$99/month` guardrail"
required_receipt: "commercial receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 1.4: Commercial Entitlements Without Offer Drift

**Epic:** 1 - Governed Workspace and Production Spine
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-01.04, FR-CMF-01.05 |
| Canonical Pipeline Stage | 1 / 8 |
| Entry Object | entitlement request |
| Exit Object | `CommercialPolicy`, cost receipt |
| Validation Contract | `$29/week` or `$99/month` guardrail |
| Required Receipt | commercial receipt |
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

As a commercial administrator, I want CMF STUDIO to expose only the two documented content charges while still enforcing internal usage and cost controls, so that customer-facing packaging stays simple and truthful.

**Acceptance Criteria:**

- Given a customer-facing price is rendered, when the billing or entitlement layer prepares copy, then the only public content offers are `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine.
- Given an internal cost quota is applied, when an Operator queues renders, then the system enforces internal usage limits without exposing extra public content tiers.
- Given a trial Guest Asset Pack entitlement is active, when an Asset Package Spec is generated, then it follows the documented Guest Asset Pack format and does not silently reduce lineage, review, or consent requirements.
- Given a Monthly Asset Engine entitlement is active, when production work is requested, then the system still requires source lineage, evaluation receipts, human approval, and valid format registry entries.
- Given commercial entitlement is expired or suspended, when a new production job is requested, then the command is blocked with a receipt stating the commercial policy condition.

**Technical Notes:** Implement `CommercialEntitlement`, `CommercialPolicy`, cost receipts, and entitlement checks in Command Bus validation. Keep billing copy separate from internal provider-cost accounting.

**Legacy and Primitive Mapping:** Product Brief commercial scope and PRD commercial rules. Active families: BUS, SAF, PER.

**Prerequisites:** Stories 1.1 through 1.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
