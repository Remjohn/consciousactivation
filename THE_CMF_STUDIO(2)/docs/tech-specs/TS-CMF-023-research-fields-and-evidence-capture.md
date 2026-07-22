---
tech_spec_id: "TS-CMF-023"
title: "Research Fields and Evidence Capture"
story_id: "5.1"
story_title: "Research Fields and Evidence Capture"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-5-1-research-fields-and-evidence-capture.md"
fr_ids:
  - "FR-CMF-05.01"
pipeline_stage: "3"
entry_object: "research evidence"
exit_object: "ResearchField, ResearchEvidence"
validation_contract: "provenance/freshness gate"
required_receipt: "research evidence receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-023: Research Fields and Evidence Capture

**Status:** Ready for Development  
**Story:** `5.1 - Research Fields and Evidence Capture`  
**Implementation Boundary:** Research field creation, evidence capture, citation/provenance validation, freshness markers, evidence receipt generation, and downstream saturation inputs.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-5-1-research-fields-and-evidence-capture.md` | Story source, acceptance criteria, pipeline trace, and handoff requirements. |
| `docs/epics.md` | Epic 5 sequencing, FR coverage, and stage trace. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-05.01 authority and anti-generic interview rules. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Interview-first moat, dual extraction doctrine, and legacy orchestration targets. |
| `docs/architecture.md` | `InterviewPreparationWorkflow`, core research objects, CRAL rule, and persistence boundaries. |
| `docs/cmf-studio-pipeline-map.md` | Stage 3 research and context engineering sub-workflow. |
| `docs/migration/legacy-inventory.md` | Legacy primitives, CRAL research engines, narrative intelligence, and Voice DNA references. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Saturation, collision, compression, and evaluation quality filter. |
| `THE CMF STUDIO/Matrix of Edging.md` | Research field to broad signal doctrine. |

## 2. Overview

Implement `ResearchField` and `ResearchEvidence` as the first typed saturation layer for interview preparation. The system must capture claims, citations, provenance, confidence, temporal sensitivity, contradiction notes, and research gaps before downstream compilers produce Guest Dossiers, Context Premises, Matrix of Edging briefs, or Interview Asset Contracts.

This spec prevents the interview plan from beginning as a generic prompt. The Operator and agents start from a brand-scoped evidence workspace with explicit source truth, freshness obligations, and receipts that can be carried into every induction and extraction decision.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-05.01 | Operators can create Research Fields with evidence, citations, claims, confidence, temporal sensitivity, source provenance, and research gaps. | Research field/evidence contracts, provenance gate, freshness markers, approval state, and research evidence receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 3 - Research and context engineering |
| Entry Object | research evidence |
| Exit Object | `ResearchField`, `ResearchEvidence` |
| Validation Contract | provenance/freshness gate |
| Required Receipt | research evidence receipt |

### Legacy Intelligence Mapping

- CRAL/SCRE source discipline informs evidence role labels and contradiction notes.
- The 244 primitive assets inform primitive-family hints without becoming runtime imports.
- RSCS Law 1 requires saturation before compression; evidence that lacks provenance cannot support interview contracts.
- Legacy research engines are read-only intelligence. The greenfield source of truth is Pydantic/SQLAlchemy in the Python core.

## 4. Implementation Plan

1. Add `ccp_studio.contracts.research` Pydantic models for research fields, evidence, claims, citations, source roles, freshness policy, and receipts.
2. Add SQLAlchemy tables for `research_fields`, `research_evidence`, `research_evidence_citations`, and `research_evidence_receipts`.
3. Expose Command Bus commands through `/api/v1/research` for field creation, evidence attachment, provenance validation, approval, stale marking, and evidence freezing.
4. Add `InterviewPreparationWorkflow` activities for evidence validation and research snapshot freezing.
5. Emit `ResearchEvidenceReceipt` on approval and attach evidence IDs to downstream compiler inputs.
6. Add review UI contracts for the PWA and Telegram Mini App to show evidence status, freshness risk, and blocked downstream use.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class ResearchEvidenceStatus(str, Enum):
    DRAFT = "draft"
    PROVENANCE_READY = "provenance_ready"
    APPROVED_FOR_USE = "approved_for_use"
    STALE_REVIEW_REQUIRED = "stale_review_required"
    REJECTED = "rejected"


class SourceRole(str, Enum):
    PRIMARY_SOURCE = "primary_source"
    PUBLIC_CONTEXT = "public_context"
    AUDIENCE_SIGNAL = "audience_signal"
    CRAL_SIGNAL = "cral_signal"
    OPERATOR_NOTE = "operator_note"
    INFERENCE = "inference"


class EvidenceCitation(BaseModel):
    citation_id: str
    uri: HttpUrl | None = None
    title: str
    retrieved_at: datetime
    quoted_span_ref: str | None = None
    source_hash: str | None = None


class ResearchEvidence(BaseModel):
    evidence_id: str
    research_field_id: str
    brand_id: str
    claim: str
    source_role: SourceRole
    citations: list[EvidenceCitation] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    temporal_sensitivity: str
    freshness_due_at: datetime | None = None
    provenance_summary: str
    contradiction_notes: list[str] = []
    research_gap: bool = False
    primitive_family_hints: list[str] = []
    status: ResearchEvidenceStatus


class ResearchField(BaseModel):
    research_field_id: str
    brand_id: str
    guest_id: str | None = None
    objective: str
    source_scope: list[str]
    evidence_ids: list[str] = []
    approved_evidence_ids: list[str] = []
    created_by_user_id: str
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CreateResearchFieldCommand`, `AttachResearchEvidenceCommand`, `ValidateEvidenceProvenanceCommand`, `ApproveResearchEvidenceCommand`, `MarkEvidenceStaleCommand`, `FreezeResearchSnapshotCommand` |
| Events | `ResearchFieldCreated`, `ResearchEvidenceAttached`, `ResearchEvidenceValidated`, `ResearchEvidenceApproved`, `ResearchEvidenceStale`, `ResearchSnapshotFrozen` |
| Workflow | `InterviewPreparationWorkflow.stage3_collect_research_evidence` |
| Receipt | `ResearchEvidenceReceipt` with field ID, evidence IDs, citation hashes, freshness policy, validator, and timestamp |

All mutations pass through Command Bus. DSPy programs may propose evidence summaries, source roles, or contradiction notes, but they cannot approve evidence without the provenance gate.

## 7. Backward Compatibility and Migration Fallback

Legacy CRAL, research, primitive, and narrative-intelligence modules remain read-only. Migrated fixtures may seed test cases, primitive-family labels, and CRAL role examples. Production evidence must be newly stored as typed CMF STUDIO records with source hashes and brand scope.

If a legacy source lacks a stable citation or hash, create a `ResearchGap` marker instead of silently promoting the claim. Downstream compilers can consume gaps as uncertainty, not as facts.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast interview prep vs. reality contact | Evidence can be drafted quickly, but cannot support contracts until provenance and freshness pass. | Interview Asset Contracts include approved evidence IDs and receipt IDs. |
| CRAL intelligence vs. unsupported inference | CRAL labels are allowed only when tied to source discipline and confidence. | Context compilers expose source role, contradiction, and research gap fields. |
| Brand reuse vs. evidence leakage | Evidence is brand-scoped and cannot cross active brand context. | Command handler rejects cross-brand evidence references. |

## 9. Tasks

- Add Pydantic contracts and SQLAlchemy models for research fields, evidence, citations, freshness, and receipts.
- Add command handlers and FastAPI routes under `/api/v1/research`.
- Add workflow activities for provenance validation, stale evidence marking, and snapshot freezing.
- Add evaluator checks for missing citation, expired temporal claim, unsupported inference, and cross-brand access.
- Add PWA/Telegram query contracts for evidence status and blocked downstream use.
- Add fixture set from legacy CRAL examples and RSCS saturation tests.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Evidence records claim, source, citation, confidence, temporal sensitivity, provenance, and gap status. | A claim is saved with no citation or source role. |
| AC2 | Temporal claims are marked for freshness review when reused. | A dated claim supports a contract after freshness expiry. |
| AC3 | Evidence without provenance remains draft. | Draft evidence appears in an Interview Asset Contract input. |
| AC4 | Brand scope prevents evidence leakage. | Brand B can reference Brand A evidence ID. |
| AC5 | Approved evidence IDs are retained downstream. | Guest Dossier output cannot trace back to evidence IDs. |

## 11. Dependencies

- TS-CMF-001 Command Bus and mutation contract.
- TS-CMF-002 pipeline stage execution records.
- TS-CMF-004 brand workspace lifecycle.
- TS-CMF-005 role permissions.
- TS-CMF-008 consent and source governance where research references guest-provided material.
- TS-CMF-013 through TS-CMF-017 for legacy migration, primitive fixtures, and intentional orchestration records.

## 12. Testing Strategy


Unit tests:

- Unit tests for Pydantic validation of citations, confidence bounds, source role, and freshness policy.
- Command handler tests for create, attach, validate, approve, stale, and freeze paths.
- Security tests for cross-brand evidence reference rejection.
- Workflow tests proving frozen research snapshot IDs persist into downstream compiler inputs.
- Evaluation tests using RSCS: generic evidence without saturation must fail.
- Legacy fixture tests proving CRAL examples are converted into typed test data, not production imports.

Integration tests:

- Workflow test from `research evidence` to `ResearchField, ResearchEvidence` through pipeline stage `3`.
- Command Bus test proving `research evidence receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Log every evidence mutation with `orchestration_run_id`, command ID, user ID, brand ID, and evidence ID.
- Emit metrics for draft evidence count, approved evidence count, stale evidence count, provenance failures, and cross-brand rejections.
- Recovery path: stale or rejected evidence can be corrected through a new command that creates a new evidence revision; prior receipts remain immutable.
- Rollback path: removing evidence from downstream use creates a superseding receipt and invalidates dependent draft compiler outputs.

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
| Tech Spec ID | TS-CMF-023 |
| Story | 5.1 |
| Requirement Trace | FR-CMF-05.01 |
| Pipeline Trace | Stage 3, research evidence to ResearchField/ResearchEvidence |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No newsletters, no partial-product scoping, no legacy runtime coupling, no unsupported customer-facing tiers |

