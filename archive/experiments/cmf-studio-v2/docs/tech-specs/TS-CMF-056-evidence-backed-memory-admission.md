---
tech_spec_id: "TS-CMF-056"
title: "Evidence-Backed Memory Admission"
story_id: "10.1"
story_title: "Evidence-Backed Memory Admission"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-10-1-evidence-backed-memory-admission.md"
fr_ids:
  - "FR-CMF-10.01"
pipeline_stage: "14"
entry_object: "approved event or rejected pattern"
exit_object: "MemoryAdmission"
validation_contract: "evidence and consent compatibility"
required_receipt: "memory admission receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / DSPy / memory admission workflow"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-056: Evidence-Backed Memory Admission

**Status:** Ready for Development  
**Story:** `10.1 - Evidence-Backed Memory Admission`  
**Implementation Boundary:** MemoryAdmissionCandidate, MemoryEvent, Brand Memory, Interviewer Memory, Route Memory, rejected-pattern memory, publishing-performance memory, evidence policy, consent compatibility, and memory admission receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-10-1-evidence-backed-memory-admission.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-10.01 authority and memory admission scope. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Evidence-backed memory, benchmark memory, and projection doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Memory admission rules and Postgres/Neo4j boundary. |
| `docs/architecture.md` | Memory core objects, memory rule, and event model. |
| `docs/cmf-studio-pipeline-map.md` | Stage 14 memory and projection trace. |
| `docs/migration/legacy-inventory.md` | Receipt chain and legacy memory references. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Reality-contact gate and anti-genericity filter. |

## 2. Overview

CMF STUDIO learns only from evidence. Memory candidates can be proposed from approved assets, approved routes, rejected candidates, publishing outcomes, review decisions, and operational receipts, but they enter durable memory only after evidence, provenance, confidence, scope, consent compatibility, and admission policy pass.

Memory is not lore. Every future JIT compiler, route selector, interviewer prep module, or evaluation program that uses memory must cite the memory event ID and evidence references that made the memory admissible.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-10.01 | Admit Brand Memory, Interviewer Memory, Route Memory, anchor memory, archetype survival memory, rejected-pattern memory, and publishing-performance memory only with evidence, source references, provenance, and admission receipts. | Memory candidate contracts, evidence policy, consent compatibility, admission commands, memory event, and citation requirements for downstream compilers. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 14 - Publishing, memory, and projection |
| Entry Object | approved event or rejected pattern |
| Exit Object | `MemoryAdmission` |
| Validation Contract | evidence and consent compatibility |
| Required Receipt | memory admission receipt |

### Legacy Intelligence Mapping

- Brand Memory, Interviewer Memory, Route Memory, and rejected-pattern memory become typed memory event families.
- RSCS reality-contact checks prevent generic or inferred lore from entering memory.
- Receipt-chain doctrine becomes mandatory provenance and citation.
- Active primitive families FBK, SAF, and PER govern feedback clarity, safety, and memory pacing.

## 4. Implementation Plan

1. Define `MemoryAdmissionCandidate`, `MemoryEvidenceRef`, `MemoryEvent`, `MemoryAdmissionReceipt`, `MemoryScope`, and memory event type enums.
2. Implement proposal from approved assets, routes, rejections, publishing outcomes, review decisions, and performance receipts.
3. Validate evidence refs, provenance, consent compatibility, confidence, memory scope, and downstream usage constraints.
4. Persist approved memory as append-only events.
5. Reject or quarantine candidates that lack evidence or violate consent.
6. Add downstream citation guard so JIT compilers must cite memory event ID and evidence refs when using memory.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field


class MemoryEventType(str, Enum):
    BRAND = "brand"
    INTERVIEWER = "interviewer"
    ROUTE = "route"
    ANCHOR = "anchor"
    ARCHETYPE_SURVIVAL = "archetype_survival"
    REJECTED_PATTERN = "rejected_pattern"
    PUBLISHING_PERFORMANCE = "publishing_performance"


class MemoryEvidenceRef(BaseModel):
    source_type: str
    source_id: str
    evidence_uri: str | None = None
    transcript_segment_id: str | None = None
    receipt_id: str | None = None
    claim_scope: Literal["supports", "contradicts", "contextualizes"]


class MemoryAdmissionCandidate(BaseModel):
    schema_version: Literal["cmf.memory_admission_candidate.v1"]
    candidate_id: str
    memory_type: MemoryEventType
    proposed_from_event_id: str
    proposed_statement: str
    evidence_refs: list[MemoryEvidenceRef]
    confidence: float = Field(ge=0, le=1)
    scope: Literal["brand", "guest", "session", "route", "interviewer", "global_fixture"]
    consent_record_version_id: str
    provenance_summary: str


class MemoryEvent(BaseModel):
    schema_version: Literal["cmf.memory_event.v1"]
    memory_event_id: str
    candidate_id: str
    memory_type: MemoryEventType
    status: Literal["approved", "rejected", "quarantined"]
    approved_by: str | None = None
    evidence_refs: list[MemoryEvidenceRef]
    created_at: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `ProposeMemoryAdmissionCommand`, `ValidateMemoryEvidenceCommand`, `ValidateMemoryConsentCommand`, `ApproveMemoryAdmissionCommand`, `RejectMemoryAdmissionCommand`, `QuarantineMemoryCandidateCommand`, `RecordMemoryUsageCitationCommand` |
| Events | `MemoryAdmissionProposed`, `MemoryEvidenceValidated`, `MemoryConsentValidated`, `MemoryAdmissionApproved`, `MemoryAdmissionRejected`, `MemoryCandidateQuarantined`, `MemoryUsageCited` |
| Workflow | `MemoryAdmissionWorkflow.stage14_admit_evidence_memory` |
| Receipt | `MemoryAdmissionReceipt` with candidate ID, memory event ID, source refs, provenance, confidence, consent compatibility, scope, reviewer/policy result, and downstream citation rule |

## 7. Backward Compatibility and Migration Fallback

Legacy memory and benchmark artifacts are reference sources until they pass the admission policy. Existing legacy memory that cannot cite source evidence remains quarantined or fixture-only. Vector similarity may suggest candidates, but it cannot admit memory without evidence and consent compatibility.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Learning speed vs. invented lore | Memory admission requires evidence, provenance, confidence, and consent compatibility. | Candidate without evidence is rejected. |
| Useful pattern vs. stale truth | Memory must carry scope and later governance status. | Story 10.2 can expire, correct, reverse, or quarantine memory. |
| Compiler convenience vs. source accountability | JIT compilers must cite memory event and evidence. | SkillInvocationRecord includes memory citations. |

## 9. Tasks

- Add memory admission contracts and tables.
- Implement memory candidate proposal service.
- Add evidence and consent validators.
- Add admission approval/rejection/quarantine commands.
- Add memory event writer.
- Add downstream memory citation guard.
- Add review surface read model for memory candidates.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Candidate includes source refs, provenance, confidence, consent compatibility, route, and evidence. | Memory says "this brand likes bold claims" with no source. |
| AC2 | Candidate lacking evidence is rejected. | Inferred brand lore enters memory. |
| AC3 | Consent-incompatible candidate is blocked or quarantined. | Revoked source becomes future memory. |
| AC4 | Approved candidate writes `MemoryAdmissionApproved` and receipt. | Memory row appears with no event. |
| AC5 | JIT compiler cites memory event ID and evidence refs. | Compiler uses memory as hidden prompt context. |

## 11. Dependencies

- TS-CMF-001 command spine.
- TS-CMF-002 pipeline stage records.
- TS-CMF-015 JIT Skill compilers.
- TS-CMF-035 rejected-candidate memory.
- TS-CMF-050 evaluation receipts.
- TS-CMF-054 Publishing Intent and Publer adapter.

## 12. Testing Strategy


Unit tests:

- Unit tests for memory candidate, evidence ref, and memory event schemas.
- Policy tests for evidence required, confidence bounds, scope, and consent compatibility.
- Integration tests from approval/publishing/rejection events to memory admission.
- Negative tests for source-free candidate rejection.
- Compiler citation tests proving memory event and evidence are required.

Integration tests:

- Workflow test from `approved event or rejected pattern` to `MemoryAdmission` through pipeline stage `14`.
- Command Bus test proving `memory admission receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for memory candidates proposed, approved, rejected, quarantined, and cited.
- Logs include candidate ID, memory event ID, source event ID, consent version, confidence, scope, and policy result.
- Recovery can re-run admission policy after missing evidence or consent repair.
- Rollback creates governance events in Story 10.2; approved memory events remain append-only.

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
| Tech Spec ID | TS-CMF-056 |
| Story | 10.1 |
| Requirement Trace | FR-CMF-10.01 |
| Pipeline Trace | Stage 14, approved event/rejected pattern to MemoryAdmission |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No ungrounded lore, no memory without evidence, no hidden compiler memory |
