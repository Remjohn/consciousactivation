---
tech_spec_id: "TS-CMF-031"
title: "Anchor Hit and Expression Moment Candidate Detection"
story_id: "6.3"
story_title: "Anchor Hit and Expression Moment Candidate Detection"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-6-3-anchor-hit-and-expression-moment-candidate-detection.md"
fr_ids:
  - "FR-CMF-06.03"
pipeline_stage: "6"
entry_object: "aligned transcript/source"
exit_object: "candidate Expression Moments"
validation_contract: "source truth and JIT skill validation"
required_receipt: "extraction receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-031: Anchor Hit and Expression Moment Candidate Detection

**Status:** Ready for Development  
**Story:** `6.3 - Anchor Hit and Expression Moment Candidate Detection`  
**Implementation Boundary:** Timestamped anchor-hit detection, emotional/source cues, Expression Moment candidates, JIT skill compiler participation, source-truth validation, and extraction receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-6-3-anchor-hit-and-expression-moment-candidate-detection.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-06.03 authority and dual-layer extraction requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Dual extraction, JIT skill compiler, anti-draft, and narrative induction source authority. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | First-Line Anchor, Depth Anchor, and Expression Moment induction doctrine. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression capture and route candidate doctrine. |
| `docs/architecture.md` | Post-session extraction workflow and JIT compiler integration. |
| `docs/cmf-studio-pipeline-map.md` | Stage 6 extraction sub-workflow and Pi orchestration example. |
| `docs/migration/legacy-inventory.md` | JIT skill modules, 96 archetype prompts, anti-draft calibrator, and primitives. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Saturation, collision, and anti-generic extraction filters. |

## 2. Overview

Implement extraction that begins from aligned source truth and approved interview contracts. The system detects anchor hits, emotional shifts, transcript segments, source timestamps, gesture/voice cues when available, and candidate `ExpressionMoment` records. Candidates are not approved outputs. They must carry source references, induction context, route rationale, confidence, and extraction receipt.

JIT skill compilers may participate as context-specific extraction lenses. They must return saturation context, contrast output, anti-draft calibration, and typed invocation receipts.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.03 | Detect anchor hits, emotional shifts, transcript segments, source timestamps, gesture or voice cues when available, and candidate Expression Moments. | `TimestampedAnchorHit`, `ExpressionMomentCandidate`, extraction DSPy programs, JIT skill receipts, and source-truth gate. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 6 - Post-session extraction |
| Entry Object | aligned transcript/source |
| Exit Object | candidate Expression Moments |
| Validation Contract | source truth and JIT skill validation |
| Required Receipt | extraction receipt |

### Legacy Intelligence Mapping

- V9/V9.1 anchor doctrine tells the extractor why clean starts and depth anchors matter.
- Legacy JIT skill compilers provide extraction and contrastive prompting logic after migration into DSPy/Pydantic contracts.
- Anti-draft calibration prevents generic rewriting of source expression.

## 4. Implementation Plan

1. Add contracts for `TimestampedAnchorHit`, `ExpressionMomentCandidate`, `SourceCue`, `ExtractionRun`, and `ExtractionReceipt`.
2. Implement `PostSessionExtractionAgent` DSPy programs for anchor hit detection, emotional shift detection, quote/story beat candidates, primitive activation, and route rationale.
3. Integrate migrated JIT skill compilers through `SkillInvocationRecord` and typed outputs.
4. Block automatic approval. Candidates enter reviewer queue with reason codes.
5. Preserve accepted artifacts and receipts across retries.
6. Expose `/api/v1/expression-moments/candidates`.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class CandidateStatus(str, Enum):
    NEEDS_REVIEW = "needs_review"
    REJECTED_UNSUPPORTED = "rejected_unsupported"
    READY_FOR_REVIEW = "ready_for_review"


class TimestampedAnchorHit(BaseModel):
    anchor_hit_id: str
    expression_session_id: str
    interview_asset_contract_id: str
    anchor_type: str
    transcript_segment_ids: list[str]
    source_artifact_id: str
    start_ms: int
    end_ms: int
    confidence: float = Field(ge=0, le=1)


class ExpressionMomentCandidate(BaseModel):
    candidate_id: str
    expression_session_id: str
    transcript_revision_id: str
    source_artifact_id: str
    timestamp_start_ms: int
    timestamp_end_ms: int
    transcript_segment_ids: list[str] = Field(min_length=1)
    source_quote: str
    induction_context_ids: list[str]
    anchor_hit_ids: list[str] = []
    emotional_shift_evidence: list[str] = []
    primitive_candidate_ids: list[str] = []
    route_rationale: str
    confidence: float = Field(ge=0, le=1)
    status: CandidateStatus
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `DetectTimestampedAnchorHitsCommand`, `RunExpressionExtractionCommand`, `InvokeJITExtractionSkillCommand`, `RejectUnsupportedCandidateCommand`, `QueueExpressionMomentCandidateForReviewCommand` |
| Events | `TimestampedAnchorHitDetected`, `ExpressionExtractionStarted`, `JITExtractionSkillInvoked`, `ExpressionMomentCandidateCreated`, `ExpressionMomentCandidateRejected`, `ExtractionReceiptWritten` |
| Workflow | `CompleteExpressionSessionWorkflow.stage6_extract_candidates` |
| Receipt | `ExtractionReceipt` with selected transcript revision, source artifact hashes, skill invocation IDs, candidate IDs, and evaluator results |

## 7. Backward Compatibility and Migration Fallback

Legacy JIT skill modules are compiled into DSPy programs and fixtures before use. If a skill module has not been migrated, it cannot participate in production extraction. The extractor may run generic source-truth candidate detection, but must mark route rationale as low-confidence when skill coverage is absent.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Clip hunting vs. dual-layer extraction | Candidates include induction context and contract IDs, not just transcript highlights. | Review surface shows source plus upstream contract/rationale. |
| Emotional labeling vs. evidence | Emotional shifts require transcript/source evidence. | Candidate contains evidence refs or remains needs-review. |
| JIT power vs. hidden prompt stack | Skill invocations emit receipts and typed outputs. | Extraction receipt links every skill contribution. |

## 9. Tasks

- Add extraction contracts and persistence.
- Implement anchor hit and candidate detection DSPy programs.
- Integrate JIT skill invocation records.
- Add source-truth and anti-genericity evaluator.
- Add candidate review queue API.
- Add retry behavior preserving accepted artifacts.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Candidate includes timestamp, transcript, source, induction context, anchor hit, route rationale, confidence. | Candidate only contains quote text. |
| AC2 | Emotional shift cites evidence. | Candidate labels "vulnerable" with no transcript/source support. |
| AC3 | Unsupported candidate is rejected or review-only. | Candidate lacking source support becomes approved. |
| AC4 | JIT compiler returns saturation, contrast, anti-draft output, and receipt. | Skill emits opaque text only. |
| AC5 | Retry preserves prior accepted receipts. | Rerun deletes accepted candidates. |

## 11. Dependencies

- TS-CMF-015 JIT skill compiler.
- TS-CMF-027 Interview Asset Contract.
- TS-CMF-029 session creation.
- TS-CMF-030 ingestion/alignment.
- TS-CMF-028 induction rationale.

## 12. Testing Strategy


Unit tests:

- Unit tests for timestamp ranges, anchor hit confidence, and candidate schema.
- DSPy tests for extracting candidates from aligned transcript fixtures.
- JIT receipt tests for migrated skill participation.
- Retry tests proving accepted artifacts are preserved.
- Evaluator tests for unsupported emotional labels and generic clip candidates.

Integration tests:

- Workflow test from `aligned transcript/source` to `candidate Expression Moments` through pipeline stage `6`.
- Command Bus test proving `extraction receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for candidates per session, anchor hit rate, rejected unsupported candidates, skill invocations, and retry count.
- Logs include extraction run ID, source artifact hash, transcript revision, and skill invocation IDs.
- Recovery: rerun extraction with same selected transcript revision and append new candidates.
- Rollback: mark candidate rejected/superseded; do not delete source or receipts.

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
| Tech Spec ID | TS-CMF-031 |
| Story | 6.3 |
| Requirement Trace | FR-CMF-06.03 |
| Pipeline Trace | Stage 6, aligned transcript/source to candidate Expression Moments |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No clip-only extraction, no opaque JIT prompt stack, no unsupported emotional certainty |
