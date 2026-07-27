---
tech_spec_id: "TS-CMF-008"
title: "Versioned Consent Records"
story_id: "2.1"
story_title: "Versioned Consent Records"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-2-1-versioned-consent-records.md"
fr_ids:
  - "FR-CMF-02.01"
pipeline_stage: "1 / 13 / 14"
entry_object: "consent request"
exit_object: "ConsentRecordVersion"
validation_contract: "consent scope model"
required_receipt: "consent receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / PostgreSQL / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-008: Versioned Consent Records

**Status:** Ready for Development  
**Story:** `2.1 - Versioned Consent Records`  
**Implementation Boundary:** Immutable consent versions, consent scope policy, consent receipts, current-consent resolver, and pending-work quarantine hooks.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for consent, source, likeness, provider processing, synthetic voice, retention, and public publishing boundaries. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-02.01 source authority and consent-as-runtime-gate doctrine. |
| `docs/architecture.md` | Architecture authority for `ConsentRecordVersion`, Command Bus consent policy, receipt storage, and consent evaluation before provider jobs, memory, and publishing. |
| `docs/cmf-studio-pipeline-map.md` | Stage 1, 13, and 14 consent trace. |
| `docs/migration/legacy-inventory.md` | Legacy receipt-chain and Voice DNA governance as read-only migration context. |
| `docs/stories/story-2-1-versioned-consent-records.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md` | Command Bus and audit receipt dependency. |
| `docs/tech-specs/TS-CMF-004-organization-and-brand-workspace-lifecycle.md` | Organization and brand scope dependency. |

## 2. Overview

### Problem Statement

CMF STUDIO cannot treat consent as a single checkbox because a guest or client may allow recording but disallow likeness reuse, derivative generation, provider processing, synthetic voice, reuse, retention, or publication. Consent can also narrow, expire, or be revoked after assets have already moved through production. If the system trusts historical approvals or stale consent, a revoked likeness or voice permission can leak into rendering, memory, or publishing.

### Solution

Implement immutable `ConsentRecordVersion` records with explicit scopes. All consequential commands resolve the current active consent version before execution. New versions never overwrite old versions. Expiry and revocation block future processing and mark affected pending work for quarantine or review. Consent receipts are written under the brand receipt path and linked to command, actor, organization, brand, guest/client, scope, and evidence.

### Scope

In scope:

- Versioned consent contracts for recording, storage, likeness, derivative generation, provider processing, synthetic voice eligibility, reuse, retention, and publication.
- Consent grant, narrow, expire, revoke, inspect, and compatibility-check commands.
- Consent policy integration into Command Bus validation.
- Pending provider job and workflow quarantine hooks after narrowing, expiry, or revocation.
- Review display model for active version, scope compatibility, source evidence, and revocation risk.

Out of scope:

- Legal agreement text generation.
- External e-signature provider integration.
- UI copy and visual design.
- Legacy runtime coupling to old consent or receipt code.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-02.01 | Guests/clients can provide, version, narrow, expire, and revoke consent for recording, source storage, likeness use, derivative generation, provider processing, synthetic voice eligibility, reuse, retention, and publication. | `ConsentRecordVersion`, `ConsentScope`, `ConsentPolicy`, `ConsentCompatibilityResult`, `ConsentReceipt`, Command Bus policy step, and quarantine hooks. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `1 - Workspace, commercial, consent, and source intake`; `13 - Review and approval`; `14 - Publishing, memory, projection` |
| Entry Object | Consent request |
| Exit Object | `ConsentRecordVersion` |
| Allowed Actors / Services | Guest/client, Owner/Admin, Operator, ConsentPolicyService, Command Bus, ReviewService, recovery job |
| Validation Contract | Consent scope model and active-version compatibility |
| Required Receipt | Consent receipt |
| Forbidden Shortcut | Mutable consent rows, stale consent approval, provider/render/memory/publishing commands without current consent resolution |

### Legacy Intelligence Mapping

Legacy receipt-chain and Brand Genesis consent doctrine inform field shape and review expectations, but production implementation is new Python/Pydantic code. Consent is not a prompt instruction. It is a typed policy gate called by command validation and workflows. TypeScript surfaces consume generated consent view models only.

Target modules:

- `ccp_studio.contracts.consent`
- `ccp_studio.domain.policies.consent_policy`
- `ccp_studio.services.consent_service`
- `ccp_studio.repositories.consent_record_versions`
- `ccp_studio.api.v1.consent`
- `ccp_studio.workflows.consent_change_quarantine`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `ConsentRecordVersion` | Immutable consent version with scope flags, effective time, expiry, revocation state, and evidence references. |
| `ConsentScope` | Fine-grained permission fields for recording, storage, likeness, derivatives, providers, voice, reuse, retention, and publication. |
| `ConsentPolicy` | Resolves whether a command is compatible with current consent. |
| `ConsentCompatibilityResult` | Allow/block result with scope name and evidence. |
| `ConsentReceipt` | Auditable receipt for grant, narrowing, expiry, revocation, and compatibility checks. |
| `ConsentChangeImpact` | List of affected pending jobs, assets, memory candidates, and publishing intents. |

## 4. Implementation Plan

### Workstream A: Contracts

Define consent scope, version status, consent record, compatibility result, receipt, and impact report Pydantic models.

### Workstream B: Persistence

Add `consent_record_versions` and `consent_receipts`. Existing versions are append-only. Current active version is derived by effective timestamps, status, and latest version number.

### Workstream C: Command Handlers

Implement `GrantConsentCommand`, `NarrowConsentCommand`, `ExpireConsentCommand`, `RevokeConsentCommand`, `InspectConsentCommand`, and `EvaluateConsentCompatibilityCommand`.

### Workstream D: Policy Integration

Install `ConsentPolicy` as the consent step in Command Bus validation. The policy receives command type, target object, source refs, organization, brand, guest/client, and required scopes.

### Workstream E: Impact and Quarantine

When consent narrows, expires, or is revoked, identify pending provider jobs, renders, memory admissions, review items, and publishing intents that require quarantine or review.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ConsentVersionStatus(str, Enum):
    active = "active"
    narrowed = "narrowed"
    expired = "expired"
    revoked = "revoked"


class ConsentScope(BaseModel):
    recording_allowed: bool
    source_storage_allowed: bool
    likeness_use_allowed: bool
    derivative_generation_allowed: bool
    provider_processing_allowed: bool
    synthetic_voice_eligible: bool
    reuse_allowed: bool
    retention_allowed: bool
    publication_allowed: bool


class ConsentRecordVersion(BaseModel):
    schema_version: Literal["cmf.consent_record_version.v1"]
    consent_record_version_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    version_number: int
    status: ConsentVersionStatus
    scope: ConsentScope
    effective_at: datetime
    expires_at: datetime | None = None
    replaces_version_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    created_by_actor_id: UUID
    created_at: datetime


class ConsentCompatibilityResult(BaseModel):
    schema_version: Literal["cmf.consent_compatibility_result.v1"]
    consent_record_version_id: UUID
    command_type: str
    allowed: bool
    blocked_scope: str | None = None
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `GrantConsentCommand`, `NarrowConsentCommand`, `ExpireConsentCommand`, `RevokeConsentCommand`, `InspectConsentCommand`, `EvaluateConsentCompatibilityCommand` |
| Events | `ConsentRecordVersioned`, `ConsentNarrowed`, `ConsentExpired`, `ConsentRevoked`, `ConsentCompatibilityEvaluated`, `PendingWorkMarkedForConsentReview` |
| Workflows | Consent change impact workflow, pending job quarantine workflow |
| Receipts | `ConsentReceipt`, `ConsentBlockerReceipt`, `AuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy consent doctrine becomes fixtures and policy examples only. Existing imported source assets without explicit consent version are blocked from new processing until a consent record is created or an approved exception receipt exists.

Fallback behavior:

- Missing current consent returns `CONSENT_RECORD_REQUIRED`.
- Expired consent returns `CONSENT_EXPIRED`.
- Revoked consent returns `CONSENT_REVOKED`.
- Scope mismatch returns `CONSENT_SCOPE_BLOCKED`.
- Ambiguous guest/client identity returns `CONSENT_SUBJECT_AMBIGUOUS`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Production wants to keep using approved assets; guest/client authority requires current consent to override historical convenience. |
| UX / Ops Failure Scenario | A render or memory update uses a likeness after the active consent version has been narrowed or revoked. |
| Resolution Demand | Current consent version takes precedence. Every consent-sensitive command must resolve active consent before execution and write a receipt. |
| Downstream Proof | Tests must prove narrowing preserves old versions, expiry blocks future commands, revocation quarantines pending work, and review surfaces display scope compatibility. |

## 9. Tasks

- Define consent contracts.
- Add append-only consent migrations and repositories.
- Implement consent command handlers.
- Integrate `ConsentPolicy` into Command Bus.
- Add receipt writing under `brands/{brand_id}/receipts/`.
- Add consent change impact workflow.
- Add review display model.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Consent grant creates immutable version with all required scopes. | Consent saved as one mutable boolean. |
| AC2 | Narrowing creates a new active version and preserves old version auditability. | Prior version is overwritten. |
| AC3 | Expired consent blocks render or memory command and names expired scope. | Render continues after publication scope expiry. |
| AC4 | Revocation blocks future processing and marks pending provider work for quarantine or review. | Queued provider job runs after revocation. |
| AC5 | Review view shows active version, scope compatibility, source evidence, and revocation risk. | Reviewer sees "consent ok" with no scope detail. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-002 Orchestration records
- TS-CMF-004 Workspace lifecycle
- TS-CMF-007 PWA/Telegram parity

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- Object storage

## 12. Testing Strategy

Unit tests:

- Consent scope validation.
- Current version resolution.
- Scope compatibility matrix.
- Consent receipt schema.

Integration tests:

- Grant, narrow, expire, revoke lifecycle.
- Expired consent blocks render command.
- Revoked consent quarantines pending provider job.
- Review view returns consent evidence.

Safety tests:

- Provider, render, memory, review, and publishing commands cannot bypass consent policy.
- Direct mutation of consent version status is blocked outside Command Bus.

## 13. Observability, Recovery, and Rollback

- Logs include `consent_record_version_id`, `guest_or_client_id`, `organization_id`, `brand_id`, `command_id`, and blocked scope.
- Metrics track scope blocks, revocations, expiries, pending-work quarantine, and consent review load.
- Rollback is a new consent version, never mutation of prior versions.
- Recovery rebuilds active consent state from append-only versions.

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
| Requirement Trace | FR-CMF-02.01 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Receipt-chain and Voice DNA governance used as read-only doctrine |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python policy gate in Command Bus; Pi cannot bypass consent |
| TypeScript Boundary | Generated consent view consumers only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

