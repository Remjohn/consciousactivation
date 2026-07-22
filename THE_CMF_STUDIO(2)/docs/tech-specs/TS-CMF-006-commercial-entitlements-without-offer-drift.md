---
tech_spec_id: "TS-CMF-006"
title: "Commercial Entitlements Without Offer Drift"
story_id: "1.4"
story_title: "Commercial Entitlements Without Offer Drift"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-1-4-commercial-entitlements-without-offer-drift.md"
fr_ids:
  - "FR-CMF-01.04"
  - "FR-CMF-01.05"
pipeline_stage: "1 / 8"
entry_object: "entitlement request"
exit_object: "CommercialPolicy, cost receipt"
validation_contract: "$29/week or $99/month guardrail"
required_receipt: "commercial receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / PostgreSQL"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-006: Commercial Entitlements Without Offer Drift

**Status:** Ready for Development  
**Story:** `1.4 - Commercial Entitlements Without Offer Drift`  
**Implementation Boundary:** Public offer guardrails, internal entitlement policy, quota/cost policy, usage ledger, cost receipts, and production command commercial validation.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Commercial authority for `$29/week` trial Guest Asset Packs, `$99/month` Monthly Asset Engine, and valid content formats. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-01.04 and FR-CMF-01.05 source authority plus no-extra-tier rules. |
| `docs/architecture.md` | Architecture source for commercial objects, cost policy, Command Bus validation, and provider-cost boundaries. |
| `docs/cmf-studio-pipeline-map.md` | Stage 1 commercial setup and Stage 8 package production trace. |
| `docs/migration/legacy-inventory.md` | Legacy read-only doctrine and legacy runtime coupling forbidden. |
| `docs/stories/story-1-4-commercial-entitlements-without-offer-drift.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md` | Commercial validation enters through Command Bus. |
| `docs/tech-specs/TS-CMF-004-organization-and-brand-workspace-lifecycle.md` | Brand workspace scope dependency. |
| `docs/tech-specs/TS-CMF-005-role-based-production-permissions.md` | Commercial Administrator permission dependency. |

## 2. Overview

### Problem Statement

CMF STUDIO needs internal controls for usage, provider budgets, trial expiration, retention, render volume, Publer profiles, and cost exposure. Those controls must not become customer-facing pricing drift. The product has only two customer-facing content charges: `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine.

### Solution

Implement commercial entitlements as a strict public offer layer plus internal policy layer. Public copy can only render the two documented offers. Internal `CommercialPolicy`, `QuotaPolicy`, `CostPolicy`, `UsageLedgerEntry`, and `CostReceipt` objects govern operations without inventing tiers, credits, newsletters, or hidden packages. Commercial validation is a Command Bus step before production jobs start.

### Scope

In scope:

- Public offer enum limited to `trial_guest_asset_pack` and `monthly_asset_engine`.
- Internal entitlement, quota, usage, cost, retention, trial, and provider budget policy.
- Commercial validation in Command Bus.
- Cost receipts for production-relevant jobs.
- Entitlement expiration/suspension blocking new production commands.
- Guardrails proving lineage, consent, review, approval, and valid format requirements are never reduced by entitlement type.

Out of scope:

- Payment processor implementation.
- Public marketing page copy.
- Extra customer-facing content packages.
- Newsletters.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-01.04 | The system enforces only `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine as customer-facing content charges. | `PublicContentOffer` enum, billing-copy guard, offer validation tests, and blocked unknown public offer keys. |
| FR-CMF-01.05 | Internal entitlement, quota, cost, retention, trial, and usage policies apply without exposing extra customer-facing content tiers. | `CommercialPolicy`, `QuotaPolicy`, `CostPolicy`, `UsageLedgerEntry`, and `CostReceipt` behind Command Bus validation. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `1 - Workspace and commercial setup`; `8 - Asset package specification` |
| Entry Object | Entitlement request |
| Exit Object | `CommercialPolicy`, cost receipt |
| Allowed Actors / Services | Commercial Administrator, CommercialPolicyService, Command Bus, UsageLedgerService |
| Validation Contract | `$29/week` or `$99/month` public offer guardrail plus internal quota/cost policy |
| Required Receipt | Commercial receipt |
| Forbidden Shortcut | Extra public pricing tiers, credit bundles, unsupported editorial packages, entitlement-based removal of consent/lineage/review requirements |

### Legacy Intelligence Mapping

Commercial scope comes from the Product Brief and PRD. Legacy billing or package language is not imported. Internal policy can be rich, but customer-facing offer language remains constrained.

Target modules:

- `ccp_studio.contracts.commercial`
- `ccp_studio.domain.policies.commercial_policy`
- `ccp_studio.services.commercial_policy_service`
- `ccp_studio.services.usage_ledger_service`
- `ccp_studio.repositories.commercial_entitlements`
- `ccp_studio.repositories.usage_ledger`
- `ccp_studio.api.v1.commercial`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `PublicContentOffer` | Two allowed customer-facing content charges only. |
| `CommercialEntitlement` | Brand-scoped access state for trial or monthly production. |
| `CommercialPolicy` | Internal rule pack for entitlement status, trial expiry, retention, and usage. |
| `QuotaPolicy` | Internal limits for work volume or provider usage. |
| `CostPolicy` | Internal provider budget and cost exposure guard. |
| `UsageLedgerEntry` | Durable record of charged or measured usage. |
| `CostReceipt` | Audit receipt for production cost decisions. |

## 4. Implementation Plan

### Workstream A: Commercial Contracts

Define public offer, entitlement status, commercial policy, quota policy, cost policy, usage ledger, and cost receipt contracts.

### Workstream B: Public Copy Guard

Create a small renderer/validator for customer-facing commercial language. It rejects any public content offer outside the two documented offers.

### Workstream C: Command Bus Commercial Validation

Install commercial validation before expensive production work, provider jobs, render jobs, asset package generation, and publishing-related operations.

### Workstream D: Usage and Cost Receipts

Record usage ledger entries and cost receipts for provider work, render jobs, storage, and production packages. Internal costs must not alter public package language.

### Workstream E: Entitlement State Transitions

Support active, expired, suspended, and cancelled entitlements with clear production blocking behavior and receipts.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class PublicContentOffer(str, Enum):
    trial_guest_asset_pack = "trial_guest_asset_pack"
    monthly_asset_engine = "monthly_asset_engine"


class EntitlementStatus(str, Enum):
    active = "active"
    expired = "expired"
    suspended = "suspended"
    cancelled = "cancelled"


class CommercialEntitlement(BaseModel):
    schema_version: Literal["cmf.commercial_entitlement.v1"]
    commercial_entitlement_id: UUID
    organization_id: UUID
    brand_id: UUID
    public_offer: PublicContentOffer
    status: EntitlementStatus
    starts_at: datetime
    ends_at: datetime | None = None


class QuotaPolicy(BaseModel):
    schema_version: Literal["cmf.quota_policy.v1"]
    quota_policy_id: UUID
    entitlement_id: UUID
    max_provider_jobs_per_period: int | None = None
    max_render_minutes_per_period: int | None = None
    max_storage_gb: int | None = None


class CostPolicy(BaseModel):
    schema_version: Literal["cmf.cost_policy.v1"]
    cost_policy_id: UUID
    entitlement_id: UUID
    provider_budget_cents_per_period: int | None = None
    requires_manual_override_above_cents: int | None = None


class CostReceipt(BaseModel):
    schema_version: Literal["cmf.cost_receipt.v1"]
    cost_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    command_id: UUID
    entitlement_id: UUID
    policy_decision: str
    estimated_cost_cents: int | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `CreateCommercialEntitlementCommand`, `UpdateCommercialEntitlementCommand`, `EvaluateCommercialPolicyCommand`, `RecordUsageCommand`, `BlockProductionForCommercialStatusCommand` |
| Events | `CommercialEntitlementCreated`, `CommercialEntitlementUpdated`, `CommercialPolicyEvaluated`, `UsageRecorded`, `ProductionBlockedByCommercialPolicy` |
| Workflows | Commercial entitlement workflow, usage ledger workflow, provider cost guard workflow |
| Receipts | `CommercialReceipt`, `CostReceipt`, `AuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy package names are not imported. Unknown historical package labels can be mapped to internal notes only and must not render publicly.

Fallback behavior:

- Unknown public offer returns `PUBLIC_OFFER_NOT_ALLOWED`.
- Extra tier label returns `PUBLIC_OFFER_DRIFT_BLOCKED`.
- Expired entitlement blocks new production with `COMMERCIAL_ENTITLEMENT_EXPIRED`.
- Suspended entitlement blocks new production with `COMMERCIAL_ENTITLEMENT_SUSPENDED`.
- Quota exceeded blocks or requests manual override according to policy.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Operations need detailed quotas and cost controls; customer-facing packaging must remain simple and truthful. |
| UX / Ops Failure Scenario | Internal provider budget logic leaks into the UI as new tiers, credits, or reduced-quality packages. |
| Resolution Demand | Public offer guardrail takes precedence. Internal policy governs operations but cannot create public offer drift or remove required lineage, consent, review, and approval. |
| Downstream Proof | Tests must reject unknown public offers, enforce only two rendered offers, block expired entitlements, and prove trial/monthly work still requires full production receipts. |

## 9. Tasks

- Define commercial contracts.
- Add commercial entitlement, quota, cost, and usage ledger migrations.
- Implement public offer guard.
- Implement commercial validation service.
- Integrate commercial validation into Command Bus.
- Add cost receipt writer.
- Add tests for pricing guardrails and entitlement blocking.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Customer-facing copy renders only `$29/week` trial Guest Asset Pack or `$99/month` Monthly Asset Engine. | UI renders unsupported tier labels, credit bundle, or unsupported package. |
| AC2 | Internal quota limits are enforced without exposing extra public tiers. | Render limit appears as a public "lite plan." |
| AC3 | Trial Guest Asset Pack follows documented format without reducing lineage, review, or consent requirements. | Trial work skips source lineage to save cost. |
| AC4 | Monthly Asset Engine still requires source lineage, evaluation receipts, human approval, and valid format registry entries. | Monthly work bypasses approval because entitlement is active. |
| AC5 | Expired or suspended entitlement blocks new production with commercial receipt. | New provider job starts after entitlement expiration. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-004 Workspace lifecycle
- TS-CMF-005 Role permissions
- Asset Package Spec from later Epic 6
- Provider policy and cost receipts from later provider specs

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- SQLAlchemy v2

## 12. Testing Strategy

Unit tests:

- Public offer enum rejects unknown offers.
- Billing copy guard.
- Entitlement status decision.
- Cost policy threshold.
- Usage ledger entry validation.

Integration tests:

- Commercial Admin creates entitlement.
- Expired entitlement blocks production command.
- Quota exceeded blocks or requires manual override.
- Trial and monthly entitlements still require lineage/review/approval receipts.

Safety tests:

- Search rendered public copy fixtures for forbidden tier labels.
- Ensure no commercial policy bypass for provider job commands.
- Ensure newsletters are not a CMF deliverable.

## 13. Observability, Recovery, and Rollback

- Logs include `commercial_entitlement_id`, `public_offer`, `policy_decision`, `command_id`, `organization_id`, and `brand_id`.
- Metrics track entitlement status, blocked production, quota decisions, cost receipts, and offer drift blocks.
- Rollback uses compensating entitlement commands.
- Recovery can rebuild usage and cost views from command events and cost receipts.

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
| Requirement Trace | FR-CMF-01.04, FR-CMF-01.05 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Read-only only; commercial authority comes from Product Brief and PRD |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python commercial policy in Command Bus |
| TypeScript Boundary | UI renders generated allowed offers only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

