---
tech_spec_id: "TS-CMF-035"
title: "Rejected Candidate and Coalition-Fatality Memory"
story_id: "6.7"
story_title: "Rejected Candidate and Coalition-Fatality Memory"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-6-7-rejected-candidate-and-coalition-fatality-memory.md"
fr_ids:
  - "FR-CMF-06.08"
pipeline_stage: "6 / 7 / 14"
entry_object: "rejected candidate/route"
exit_object: "failure corpus or memory candidate"
validation_contract: "consent and non-truth admission gate"
required_receipt: "rejection receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / eval fixtures"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-035: Rejected Candidate and Coalition-Fatality Memory

**Status:** Ready for Development  
**Story:** `6.7 - Rejected Candidate and Coalition-Fatality Memory`  
**Implementation Boundary:** Rejected candidate records, rejected route records, coalition-fatality evidence, consent quarantine, negative evidence for compilers, and memory-admission handoff without truth admission.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-6-7-rejected-candidate-and-coalition-fatality-memory.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-06.08 authority and memory caution. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Matrix coalition fatality and learning doctrine. |
| `THE CMF STUDIO/Matrix of Edging.md` | Benchmark law and coalition survival/fatality concepts. |
| `docs/architecture.md` | Memory admission, rejected-route candidates, and Neo4j projection boundary. |
| `docs/cmf-studio-pipeline-map.md` | Stage 6/7/14 rejected-pattern and learning loop. |
| `docs/migration/legacy-inventory.md` | SFL failure corpus, CBAR, RSCS, and receipt chain references. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Anti-generic evaluation and failure evidence. |

## 2. Overview

Implement a governed way to preserve failed extraction and routing evidence without admitting it as truth. Rejected candidates, rejected routes, and coalition-fatality records help future JIT compilers and routing evals avoid repeated mistakes, but they cannot be treated as approved moments, memory facts, or production routes.

Sensitive or consent-incompatible rejected material must be blocked or quarantined. Future compilers may cite rejection evidence only as negative evidence with receipt lineage.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.08 | Preserve failed candidates, rejected routes, and coalition-fatality evidence for future improvement without admitting them as truth. | Rejection records, consent quarantine, negative evidence interface, memory candidate handoff, and rejection receipts. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 6 / 7 / 14 - Extraction, routing, memory/projection |
| Entry Object | rejected candidate/route |
| Exit Object | failure corpus or memory candidate |
| Validation Contract | consent and non-truth admission gate |
| Required Receipt | rejection receipt |

### Legacy Intelligence Mapping

- Matrix benchmark law requires learning from coalition geometries and fatality patterns.
- SFL failure corpus informs failure-record fixtures.
- CBAR and RSCS define why generic or unsupported outputs should become negative evidence.
- Memory admission remains governed by Epic 10; this spec only prepares candidates.

## 4. Implementation Plan

1. Add contracts for `RejectedExpressionCandidate`, `RejectedRouteAttempt`, `CoalitionFatalityRecord`, `NegativeEvidenceRef`, and `RejectionReceipt`.
2. Implement command handlers for storing rejection, quarantining sensitive material, and exposing negative evidence to compilers.
3. Add consent compatibility check before preserving rejected source spans.
4. Prevent rejected records from becoming approved memory without Epic 10 memory admission.
5. Attach rejected route/candidate IDs to future compiler/evaluator reports when used as negative evidence.
6. Prepare failure corpus exports for evals only when consent permits.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class RejectionCategory(str, Enum):
    SOURCE_UNSUPPORTED = "source_unsupported"
    ROUTE_FIT_FAILED = "route_fit_failed"
    BOUNDARY_BAD = "boundary_bad"
    GENERIC_OR_CENTROID = "generic_or_centroid"
    SENSITIVITY_OR_CONSENT = "sensitivity_or_consent"
    COALITION_FATALITY = "coalition_fatality"


class RejectedExpressionCandidate(BaseModel):
    rejected_candidate_id: str
    candidate_id: str
    expression_session_id: str
    category: RejectionCategory
    reason: str
    source_reference_ids: list[str]
    reviewer_id: str | None = None
    consent_compatible: bool
    quarantined: bool = False
    created_at: datetime


class RejectedRouteAttempt(BaseModel):
    rejected_route_attempt_id: str
    expression_moment_id: str | None = None
    route_refs: list[str]
    category: RejectionCategory
    source_gap: str | None = None
    route_fit_score: float | None = None
    usable_as_negative_evidence: bool


class CoalitionFatalityRecord(BaseModel):
    coalition_fatality_id: str
    matrix_brief_id: str | None = None
    primitive_candidate_ids: list[str]
    edge_product_id: str | None = None
    failure_observation: str
    downstream_stage: str
    rejection_receipt_id: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RecordRejectedExpressionCandidateCommand`, `RecordRejectedRouteAttemptCommand`, `RecordCoalitionFatalityCommand`, `QuarantineRejectedMaterialCommand`, `ReferenceNegativeEvidenceCommand`, `ProposeMemoryAdmissionFromRejectionCommand` |
| Events | `RejectedExpressionCandidateRecorded`, `RejectedRouteAttemptRecorded`, `CoalitionFatalityRecorded`, `RejectedMaterialQuarantined`, `NegativeEvidenceReferenced`, `MemoryAdmissionCandidateProposed` |
| Workflow | `CompleteExpressionSessionWorkflow.stage6_7_record_rejections` and `MemoryAdmissionWorkflow.stage14_review_candidate` |
| Receipt | `RejectionReceipt` with source refs, consent state, category, reviewer, negative-evidence eligibility, and quarantine state |

## 7. Backward Compatibility and Migration Fallback

Legacy failure corpus concepts can seed typed categories and eval fixtures. New rejected records must be generated through CMF STUDIO workflows with consent and source references. Neo4j may project these relationships later but cannot be canonical state.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Learning from failure vs. admitting false truth | Rejections are negative evidence only unless memory gates approve later. | Compiler reports cite rejection receipt as negative evidence. |
| Failure corpus value vs. consent risk | Sensitive rejected material is quarantined or blocked. | Rejection receipt records consent compatibility. |
| Coalition ambition vs. real survival | Coalition fatality captures where a Matrix hypothesis died. | Future Matrix evals can cite fatality without treating it as approved content. |

## 9. Tasks

- Add rejection/fatality contracts and tables.
- Implement consent/non-truth admission gate.
- Add commands for rejected candidates, route attempts, and fatality records.
- Add negative evidence interface for JIT compilers and route evaluators.
- Add memory admission proposal handoff guarded by Epic 10 policy.
- Add failure corpus export with consent filters.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Rejection stores reason, evidence, reviewer, route attempt, category. | Candidate disappears after rejection. |
| AC2 | Source-insufficient route becomes negative evidence. | Same unsupported route keeps recurring without record. |
| AC3 | Sensitive/consent-incompatible material is blocked or quarantined. | Rejected private confession becomes eval fixture. |
| AC4 | Future compiler cites rejection and cannot treat it as truth. | Rejected route is reused as approved memory. |
| AC5 | Memory proposal requires explicit memory gate later. | Rejection auto-enters Brand Memory. |

## 11. Dependencies

- TS-CMF-008 and TS-CMF-010 consent governance.
- TS-CMF-031 candidate detection.
- TS-CMF-032 moment review.
- TS-CMF-033 routing.
- Epic 10 memory admission specs when generated.

## 12. Testing Strategy


Unit tests:

- Unit tests for rejection categories and quarantine flags.
- Command tests for candidate/route/fatality records.
- Consent tests blocking or quarantining sensitive rejected material.
- Compiler integration tests using negative evidence refs.
- Memory handoff tests ensuring no auto-admission.

Integration tests:

- Workflow test from `rejected candidate/route` to `failure corpus or memory candidate` through pipeline stage `6 / 7 / 14`.
- Command Bus test proving `rejection receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for rejection categories, quarantines, coalition fatality count, negative-evidence references, and memory proposals.
- Logs include rejection receipt, source refs, consent version, reviewer, and downstream references.
- Recovery: update rejection metadata through superseding receipt if consent or reviewer decision changes.
- Rollback: remove negative-evidence eligibility while preserving immutable rejection history.

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
| Tech Spec ID | TS-CMF-035 |
| Story | 6.7 |
| Requirement Trace | FR-CMF-06.08 |
| Pipeline Trace | Stages 6 / 7 / 14, rejected candidate/route to failure corpus or memory candidate |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No rejected truth admission, no consent bypass, no canonical Neo4j state |

