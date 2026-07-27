---
tech_spec_id: "TS-CMF-012"
title: "Consent and Source Review Surface"
story_id: "2.5"
story_title: "Consent and Source Review Surface"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-2-5-consent-and-source-review-surface.md"
fr_ids:
  - "FR-CMF-02.04"
  - "FR-CMF-02.07"
pipeline_stage: "13"
entry_object: "asset under review"
exit_object: "approval-ready evidence view"
validation_contract: "source and consent completeness"
required_receipt: "review evidence receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / generated TypeScript / PWA / Telegram deep links"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-012: Consent and Source Review Surface

**Status:** Ready for Development  
**Story:** `2.5 - Consent and Source Review Surface`  
**Implementation Boundary:** Review evidence API, consent/source read model, approval blocking, approval event source refs, and PWA/Telegram evidence-depth routing.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for Operator/Reviewer evidence review and source truth. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-02.04 and FR-CMF-02.07 source authority. |
| `docs/architecture.md` | Architecture source for ReviewService, approval events, evaluation receipts, source artifacts, transcript revisions, and PWA/Telegram surfaces. |
| `docs/cmf-studio-pipeline-map.md` | Stage 13 review and approval trace. |
| `docs/migration/legacy-inventory.md` | Legacy evaluation receipt doctrine and receipt chain as read-only context. |
| `docs/stories/story-2-5-consent-and-source-review-surface.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-007-pwa-and-telegram-state-parity.md` | PWA/Telegram deep-link dependency. |
| `docs/tech-specs/TS-CMF-008-versioned-consent-records.md` | Consent view dependency. |
| `docs/tech-specs/TS-CMF-009-recording-setup-and-source-artifact-gate.md` | Source artifact dependency. |
| `docs/tech-specs/TS-CMF-011-voice-dna-boost-eligibility-and-audio-classification.md` | Audio/voice evidence dependency. |

## 2. Overview

### Problem Statement

Reviewers cannot approve truth-sensitive media from a pretty preview alone. Approval must expose consent lineage, source artifact, transcript revision, timestamp references, claim references, voice classification, and file provenance. Telegram is useful for quick decisions, but complex evidence must deep-link to PWA rather than allowing blind approval.

### Solution

Implement a consent and source review read model plus approval gate. The ReviewService builds an `ApprovalEvidenceView` from consent versions, source artifacts, transcript revisions, evaluation receipts, audio manifests, and approval history. Approval is blocked when source references, consent compatibility, or claim evidence are incomplete. Approved commands write `ApprovalEventRecorded` plus audit receipt with consent and source references.

### Scope

In scope:

- Review evidence API over consent, source artifacts, transcript revisions, evaluation receipts, audio classification, and claim refs.
- Approval blocker for missing source reference, consent incompatibility, provenance gaps, and failed voice eligibility.
- Append-only transcript/source revision display.
- Approval event and audit receipt source refs.
- Telegram deep-link behavior when evidence is too complex.

Out of scope:

- Full visual UI implementation.
- Evaluation model internals.
- Publishing adapter implementation.
- New consent or source ingestion commands.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-02.04 | System preserves source artifacts, transcript revisions, timestamps, claim references, and file provenance. | `ApprovalEvidenceView`, `SourceReference`, transcript revision history, source hashes, and file provenance display. |
| FR-CMF-02.07 | Reviewers inspect consent lineage and source truth before approving assets, publishing intent, memory admission, or voice repair. | Review gate, approval blocker policy, evidence-depth routing, `ReviewEvidenceReceipt`, and source-linked `ApprovalEventRecorded`. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `13 - Evaluation, review, revision, approval` |
| Entry Object | Asset under review |
| Exit Object | Approval-ready evidence view |
| Allowed Actors / Services | Reviewer, Operator, ReviewService, EvaluationService, PWA, Telegram Bot/Mini App |
| Validation Contract | Source and consent completeness |
| Required Receipt | Review evidence receipt |
| Forbidden Shortcut | Approval without source refs, blind Telegram approval for complex evidence, approval event without consent/source references |

### Legacy Intelligence Mapping

Legacy evaluation receipt and receipt-chain doctrine informs the evidence surface, but production logic lives in Python. PWA and Telegram consume generated read models and submit commands through the Command Bus. Telegram may accelerate low-risk review only when evidence sufficiency passes.

Target modules:

- `ccp_studio.contracts.review_evidence`
- `ccp_studio.services.review_evidence_service`
- `ccp_studio.domain.policies.approval_evidence_policy`
- `ccp_studio.repositories.review_read_models`
- `ccp_studio.api.v1.review`
- `ccp_studio.contract_generation.typescript`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `ApprovalEvidenceView` | Reviewer-facing evidence bundle for consent, source, transcript, claims, voice, provenance, and blockers. |
| `SourceReference` | Timestamped source link for claim or asset segment. |
| `TranscriptRevisionSummary` | Append-only transcript revision and source hash history. |
| `ApprovalBlocker` | Structured blocker that prevents approval until repaired. |
| `ReviewEvidenceReceipt` | Receipt proving the evidence view was generated and checked. |
| `ApprovalEventRecorded` | Approval event carrying consent and source references. |

## 4. Implementation Plan

### Workstream A: Review Evidence Contracts

Define evidence view, source reference, transcript summary, blocker, receipt, and approval event reference contracts.

### Workstream B: Evidence Read Model

Build a read model joining consent record versions, recording artifacts, source artifacts, transcript revisions, evaluation receipts, voice/audio manifests, and prior approvals.

### Workstream C: Approval Blocker Policy

Block approval when claim lacks source ref, consent incompatible, provenance missing, voice classification missing, voice eligibility failed, or evaluation receipt missing.

### Workstream D: Approval Event Writer

Write `ApprovalEventRecorded` and audit receipt with consent and source references.

### Workstream E: PWA/Telegram Routing

If evidence complexity exceeds Telegram sufficiency threshold, return a PWA deep link using TS-CMF-007.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ApprovalBlockerCode(str, Enum):
    missing_source_reference = "missing_source_reference"
    consent_incompatible = "consent_incompatible"
    provenance_missing = "provenance_missing"
    voice_classification_missing = "voice_classification_missing"
    voice_eligibility_failed = "voice_eligibility_failed"
    evaluation_receipt_missing = "evaluation_receipt_missing"
    pwa_review_required = "pwa_review_required"


class SourceReference(BaseModel):
    schema_version: Literal["cmf.source_reference.v1"]
    source_reference_id: UUID
    source_artifact_id: UUID
    transcript_revision_id: UUID | None = None
    start_seconds: float | None = None
    end_seconds: float | None = None
    claim_ref: str | None = None


class ApprovalBlocker(BaseModel):
    schema_version: Literal["cmf.approval_blocker.v1"]
    blocker_code: ApprovalBlockerCode
    message: str
    evidence_refs: list[str] = Field(default_factory=list)
    repair_action: str


class ApprovalEvidenceView(BaseModel):
    schema_version: Literal["cmf.approval_evidence_view.v1"]
    approval_evidence_view_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str
    object_id: UUID
    consent_record_version_id: UUID
    source_references: list[SourceReference]
    transcript_revision_ids: list[UUID]
    evaluation_receipt_ids: list[UUID]
    audio_mix_manifest_id: UUID | None = None
    file_provenance_refs: list[str] = Field(default_factory=list)
    blockers: list[ApprovalBlocker] = Field(default_factory=list)
    generated_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `GenerateApprovalEvidenceViewCommand`, `EvaluateApprovalEvidenceCommand`, `ApproveWithEvidenceCommand`, `RejectForMissingEvidenceCommand`, `DeepLinkToPWAReviewCommand` |
| Events | `ApprovalEvidenceViewGenerated`, `ApprovalBlockedForEvidence`, `ApprovalEventRecorded`, `ReviewEvidenceReceiptWritten` |
| Workflows | Review evidence workflow, approval workflow, Telegram-to-PWA review workflow |
| Receipts | `ReviewEvidenceReceipt`, `ApprovalReceipt`, `AuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy evaluation receipt doctrine becomes test fixtures. Historical assets without source references cannot be approved for new publication, memory admission, or voice repair until evidence is repaired.

Fallback behavior:

- Missing source ref returns `SOURCE_REFERENCE_REQUIRED`.
- Missing consent compatibility returns `CONSENT_REVIEW_REQUIRED`.
- Missing provenance returns `SOURCE_PROVENANCE_REQUIRED`.
- Too complex for Telegram returns `PWA_REVIEW_REQUIRED`.
- Approval without evidence receipt returns `REVIEW_EVIDENCE_RECEIPT_REQUIRED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Review should be fast; truth-sensitive approval requires evidence depth. |
| UX / Ops Failure Scenario | A Reviewer approves a strong-looking asset without seeing that the core claim lacks a timestamped source reference. |
| Resolution Demand | Evidence-backed approval takes precedence. Review surfaces must show source and consent truth, and Telegram must deep-link to PWA when evidence is too complex. |
| Downstream Proof | Tests must prove missing source refs block approval, transcript history is append-only, approval receipts include evidence, and Telegram deep-links for complex review. |

## 9. Tasks

- Define review evidence contracts.
- Build evidence read model.
- Implement approval blocker policy.
- Implement approval event writer with consent/source refs.
- Add PWA deep-link routing.
- Add tests for source refs, transcript revisions, consent compatibility, and Telegram complexity threshold.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Review surface shows consent version, source artifact, transcript revision, timestamp refs, claim refs, voice classification, and file provenance. | Review shows only final render preview. |
| AC2 | Claim without source reference blocks approval until repaired or removed. | Unsupported claim is approved. |
| AC3 | Multiple source revisions display append-only transcript revisions and hashes. | Reviewer sees only latest transcript text. |
| AC4 | Approval event and audit receipt include consent and source references. | Approval event has no evidence refs. |
| AC5 | Complex evidence attempted from Telegram deep-links to PWA. | Telegram allows blind approval from short preview. |

## 11. Dependencies

Internal:

- TS-CMF-007 PWA/Telegram parity
- TS-CMF-008 Consent records
- TS-CMF-009 Source artifact gate
- TS-CMF-010 Consent blockers
- TS-CMF-011 Voice/audio classification
- Evaluation receipts from Epic 9

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- Generated TypeScript consumers

## 12. Testing Strategy

Unit tests:

- Evidence view schema.
- Approval blocker generation.
- Source reference validation.
- Telegram complexity threshold.

Integration tests:

- Generate evidence view for asset.
- Block approval for missing source ref.
- Show transcript revision history.
- Approve with evidence and write receipt.
- Telegram action deep-links to PWA when evidence is complex.

Safety tests:

- Approval command cannot bypass evidence receipt.
- Review read model never returns cross-brand source artifacts.
- Approval event must include consent and source refs.

## 13. Observability, Recovery, and Rollback

- Logs include `approval_evidence_view_id`, `object_id`, `consent_record_version_id`, `blocker_code`, `organization_id`, and `brand_id`.
- Metrics track approval blockers, evidence view generation, PWA deep links, repaired evidence, and approval receipt latency.
- Recovery can regenerate evidence views from immutable sources, transcript revisions, and receipts.
- Rollback uses revision or rejection commands; approval records remain append-only.

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
| Requirement Trace | FR-CMF-02.04, FR-CMF-02.07 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Evaluation receipt and receipt-chain doctrine mapped to evidence read model |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python review policy; Telegram/PWA are generated consumers |
| TypeScript Boundary | No domain authority in UI |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

