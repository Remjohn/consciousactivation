---
tech_spec_id: "TS-CMF-057"
title: "Memory Review, Correction, Expiry, and Quarantine"
story_id: "10.2"
story_title: "Memory Review, Correction, Expiry, and Quarantine"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-10-2-memory-review-correction-expiry-and-quarantine.md"
fr_ids:
  - "FR-CMF-10.02"
pipeline_stage: "14"
entry_object: "memory event"
exit_object: "corrected/expired/quarantined memory"
validation_contract: "provenance and reversal gate"
required_receipt: "memory governance receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / PWA / memory governance workflow"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-057: Memory Review, Correction, Expiry, and Quarantine

**Status:** Ready for Development  
**Story:** `10.2 - Memory Review, Correction, Expiry, and Quarantine`  
**Implementation Boundary:** MemoryReviewState, MemoryGovernanceAction, correction/reversal/expiry/quarantine commands, downstream usage blocking, and memory governance receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-10-2-memory-review-correction-expiry-and-quarantine.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-10.02 authority and memory governance actions. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Brand/interviewer memory and benchmark-memory doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Memory admission and downstream retrieval constraints. |
| `docs/architecture.md` | Memory events, recovery, and canonical event rules. |
| `docs/cmf-studio-pipeline-map.md` | Stage 14 memory governance trace. |
| `docs/migration/legacy-inventory.md` | Receipt chain and memory governance references. |
| `docs/tech-specs/TS-CMF-056-evidence-backed-memory-admission.md` | Memory admission dependency. |

## 2. Overview

Memory must remain inspectable and reversible. Operators can correct, reverse, expire, or quarantine memory admissions that become wrong, stale, sensitive, unsupported, or consent-incompatible. These actions supersede memory usage without mutating historical memory events.

Future compilers, route selectors, and interview prep modules must respect governance state before using memory. Expired memory can remain historical evidence, while quarantined or reversed memory is blocked from active use.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-10.02 | Operators can inspect, correct, reverse, expire, or quarantine memory admissions that are wrong, stale, sensitive, unsupported, or consent-incompatible. | Memory review state, governance actions, append-only supersession events, downstream usage guard, and governance receipts. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 14 - Publishing, memory, and projection |
| Entry Object | memory event |
| Exit Object | corrected/expired/quarantined memory |
| Validation Contract | provenance and reversal gate |
| Required Receipt | memory governance receipt |

### Legacy Intelligence Mapping

- Product Brief memory doctrine becomes reviewable governance state, not hidden context.
- Receipt-chain mechanics become append-only correction and quarantine receipts.
- Active primitive families SAF, FBK, and PER govern safety, clear repair feedback, and timing of memory expiry.

## 4. Implementation Plan

1. Define `MemoryReviewState`, `MemoryGovernanceAction`, `MemoryGovernanceEvent`, `MemoryUsagePolicy`, and `MemoryGovernanceReceipt`.
2. Build memory review read model with evidence, source refs, route, confidence, consent state, created event, downstream usage, and governance history.
3. Implement correction, reversal, expiry, and quarantine commands.
4. Enforce append-only governance events; never mutate the original memory event.
5. Add downstream memory usage guard for compilers and routes.
6. Add projection update event so relationship projection reflects governance state.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class MemoryGovernanceActionType(str, Enum):
    CORRECT = "correct"
    REVERSE = "reverse"
    EXPIRE = "expire"
    QUARANTINE = "quarantine"
    RELEASE_FROM_QUARANTINE = "release_from_quarantine"


class MemoryReviewState(BaseModel):
    schema_version: Literal["cmf.memory_review_state.v1"]
    memory_event_id: str
    evidence_refs: list[str]
    source_refs: list[str]
    route_refs: list[str]
    confidence: float
    consent_compatible: bool
    downstream_usage_refs: list[str]
    governance_status: Literal["active", "corrected", "reversed", "expired", "quarantined"]


class MemoryGovernanceAction(BaseModel):
    action_id: str
    memory_event_id: str
    action_type: MemoryGovernanceActionType
    reason: str
    evidence_refs: list[str]
    requested_by_user_id: str


class MemoryGovernanceEvent(BaseModel):
    event_id: str
    action_id: str
    memory_event_id: str
    resulting_status: str
    superseding_memory_event_id: str | None = None
    created_at: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `BuildMemoryReviewStateCommand`, `CorrectMemoryCommand`, `ReverseMemoryCommand`, `ExpireMemoryCommand`, `QuarantineMemoryCommand`, `ReleaseMemoryFromQuarantineCommand`, `ValidateMemoryUsageCommand` |
| Events | `MemoryReviewStateBuilt`, `MemoryCorrected`, `MemoryReversed`, `MemoryExpired`, `MemoryQuarantined`, `MemoryReleasedFromQuarantine`, `MemoryUsageBlocked` |
| Workflow | `MemoryAdmissionWorkflow.stage14_govern_memory` |
| Receipt | `MemoryGovernanceReceipt` with action, reason, actor, evidence refs, prior status, resulting status, and downstream usage effect |

## 7. Backward Compatibility and Migration Fallback

Legacy memory entries without governance history must be imported as candidates or quarantined references. If a memory entry cannot prove provenance, it cannot become active. Downstream users must treat historical memory as evidence only when active status allows it.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Useful learning vs. stale or wrong memory | Operators can expire, correct, reverse, or quarantine memory through append-only events. | Future compiler use reads governance status first. |
| Historical truth vs. active guidance | Original memory remains visible but superseded status controls usage. | Review state displays created event and governance history. |
| Sensitivity vs. operational speed | Quarantine blocks downstream use until resolved. | Memory usage guard rejects quarantined memory. |

## 9. Tasks

- Add memory governance contracts.
- Build memory review read model.
- Implement correction, reversal, expiry, quarantine, and release commands.
- Add downstream usage guard.
- Add projection event for governance status.
- Add PWA memory review surface.
- Add governance receipt writer.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Review surface shows evidence, source refs, route, confidence, consent, event, and usage. | Memory row shows only a sentence. |
| AC2 | Correction writes superseding event without mutating history. | Original memory text is overwritten. |
| AC3 | Expired memory is blocked from active compiler use. | Stale memory still shapes interview prep. |
| AC4 | Quarantined memory blocks downstream use until resolved. | Sensitive memory remains retrievable by route compiler. |
| AC5 | Reversal is respected in future routes. | Reversed route memory still boosts the same route. |

## 11. Dependencies

- TS-CMF-010 consent blockers.
- TS-CMF-015 JIT Skill compilers.
- TS-CMF-056 evidence-backed memory admission.
- TS-CMF-058 Neo4j projection.

## 12. Testing Strategy


Unit tests:

- Unit tests for governance actions and review state schema.
- Integration tests for correction, reversal, expiry, and quarantine commands.
- Downstream compiler tests proving inactive memory is blocked.
- Projection tests proving governance state updates.
- Consent-change tests that quarantine incompatible memory.

Integration tests:

- Workflow test from `memory event` to `corrected/expired/quarantined memory` through pipeline stage `14`.
- Command Bus test proving `memory governance receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for memory corrections, reversals, expiries, quarantines, releases, and blocked usages.
- Logs include memory event ID, governance action ID, actor, resulting status, and usage refs.
- Recovery rebuilds active memory view from append-only memory and governance events.
- Rollback is another governance event; history is not deleted.

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
| Tech Spec ID | TS-CMF-057 |
| Story | 10.2 |
| Requirement Trace | FR-CMF-10.02 |
| Pipeline Trace | Stage 14, memory event to corrected/expired/quarantined memory |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No mutable memory history, no active use of quarantined memory, no unsupported memory |
