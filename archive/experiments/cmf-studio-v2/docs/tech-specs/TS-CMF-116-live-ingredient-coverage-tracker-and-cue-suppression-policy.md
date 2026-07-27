---
tech_spec_id: "TS-CMF-116"
title: "Live Ingredient Coverage Tracker and Cue Suppression Policy"
story_id: "12.3"
story_title: "Live Ingredient Coverage"
epic_id: 12
epic_title: "Conscious Sequencing and Expression Acquisition"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP Conscious Sequencing and Expression Acquisition Engine V1 bundle"
pipeline_stage: "6 / 7"
entry_object: "Approved InterviewBriefV2, active InterviewAssetContractV2, Complete Expression Session stream, live transcript ticks, interviewer state"
exit_object: "LiveIngredientCoverageState, LiveCueDecisionReceipt, IngredientGapDetected events, pickup recommendations"
validation_contract: "coverage tracking, state integrity, cue timing, suppression, interviewer confirmation, source event receipts"
required_receipt: "LiveCueDecisionReceipt"
runtime_target: "Python / Pydantic v2 / Complete Expression Session workflow / PWA live view / Telegram quick cues"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-116: Live Ingredient Coverage Tracker and Cue Suppression Policy

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for live pipeline gating and actionable blocks. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 CBAR mandates for inline capture and verifiable artifacts. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | Phase 4 adversarial audit trail. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` | Phase 5 adversarial audit trail. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Product owner for FR-CMF-12.03. |
| `THE CMF STUDIO/CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/ccp_conscious_sequence_engine_v1/00_AGENT_START_HERE.md` | Forbids turning coverage into an interrogation checklist. |
| `.../01_MASTER_SPEC.md` | Live coverage policy and procurement-to-session relation. |
| `.../02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Live coverage state, requirement states, events, invariants. |
| `.../03_RUNTIME_WORKFLOWS.md` | Live session workflow. |
| `.../05_EVALUATION_GOVERNANCE_AND_LEARNING.md` | Live coverage gates. |
| `.../models/sequence_engine_models.py` | `CoverageItem`, `LiveCue`, and `LiveIngredientCoverageState`. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-029-complete-expression-session-creation.md` | Complete Expression Session dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-031-anchor-hit-and-expression-moment-candidate-detection.md` | Anchor hit and live source signal dependency. |
| `src/ccp_studio/services/expression_session_service.py` | Current session readiness/start/pause/resume/close workflow. |

## 2. Overview

This spec adds state-aware live ingredient coverage during the Complete Expression Session. The system tracks whether planned ingredients are being captured, estimates provisional quality, proposes interviewer cues only when appropriate, and suppresses cues when they would violate guest state, safety, or interview flow.

The tracker is an assistant to the interviewer, not a checklist controller. It must never force the guest to follow the final viewer-state sequence, and it must never interrupt an emotional peak to satisfy an asset recipe.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-116-001 | `CoverageItem` | Tracks one planned ingredient requirement during the session. |
| DEP-CMF-116-002 | `LiveCue` | Proposed, shown, suppressed, accepted, ignored, or expired cue. |
| DEP-CMF-116-003 | `LiveIngredientCoverageState` | Session-level coverage state bound to Interview Brief V2 and active contract. |
| DEP-CMF-116-004 | `LiveCueDecisionReceipt` | Receipt proving cue decision, suppression reason, source tick, and operator/interviewer state. |
| DEP-CMF-116-005 | `LiveCoverageReadModel` | Calm operator read model for PWA and Telegram quick review. |

### Existing Backend Integration

| Python Owner | Database Table(s) | API Route(s) | Migration / Backfill Behavior |
|---|---|---|---|
| `src/ccp_studio/services/live_ingredient_coverage_service.py` | `live_ingredient_coverage_states`, `live_coverage_items` | `POST /api/cmf/expression-sessions/{id}/coverage/start`, `GET /api/cmf/expression-sessions/{id}/coverage` | New live-state tables keyed by expression session. |
| `src/ccp_studio/services/live_cue_policy_service.py` | `live_cues`, `live_cue_decisions` | `POST /api/cmf/expression-sessions/{id}/coverage/tick`, `POST /api/cmf/expression-sessions/{id}/coverage/cues/{cue_id}/decision` | New cue event tables; no historical backfill. |
| `src/ccp_studio/services/expression_session_service.py` | `expression_sessions` | existing session start/pause/close routes | Extends session lifecycle with coverage start only after approved brief. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | `receipt_chain`, `approval_blockers` | shared receipt writer | Writes cue decision receipts and suppression blockers. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PER-003` | Phase4-M01 | Live cue display requires state review and source tick evidence. |
| `EXP-FRC-006` | Phase4-M04 | Suppressed or blocked cues must produce a next action, not a static wall. |
| `EXP-FBK-001` | Phase4-M05 | Cue rejection must state exact suppression reason and ingredient role. |
| `EXP-PRG-001` | Phase4-M03 and Phase5-M04 | Cue decisions must happen inline during the session. |
| `EXP-SOC-001` | Phase5-M01 | Cue decisions write verifiable receipt-chain artifacts. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Cue display is blocked unless current interview state and source tick are valid. |
| Phase4-M04: Frictionless Block Rule | Phase 4 Story 4.1 | `EXP-FRC-006` | Suppressed cues return alternative actions: wait, pickup, substitute, or waive. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Suppression receipts name exact ingredient role and suppression reason. |
| Phase5-M04: Inline Capture Hook | Phase 5 Story 2.2 | `EXP-PRG-001` | Accepted cues are executable inline and cannot schedule deferred context switches. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Cue decisions write receipt-chain rows. |

### Receipt Chain Guard

| Receipt | Table | Action | Idempotency Key | Required Hashes |
|---|---|---|---|---|
| `LiveCueDecisionReceipt` | `receipt_chain` | `live_cue_decision.recorded` | `expression_session_id + cue_id + proposed_at_tick` | live state hash, cue payload hash, source event hash |

### Coverage Objects

| Object | Purpose |
|---|---|
| `CoverageItem` | Tracks one ingredient requirement, role, status, provisional quality, source segment hint, and notes. |
| `LiveCue` | Represents a proposed, suppressed, accepted, or ignored cue. |
| `LiveIngredientCoverageState` | Stores session-level state, active contract, current interview state, emotional peak flag, coverage items, cues, and tick. |

### Requirement Statuses

```text
planned
targeted
partial
captured
quality_passed
missing
substituted
pickup_requested
waived
```

### Cue Suppression Rules

A cue must be suppressed when any of these are true:

| Suppression Reason | Required Behavior |
|---|---|
| `emotional_peak_active` | Do not interrupt. Continue passive coverage tracking. |
| `guest_boundary_signal` | Suppress and require interviewer confirmation before any adjacent follow-up. |
| `sensitive_followup_unconfirmed` | Suppress until interviewer explicitly opts in. |
| `state_mismatch` | Suppress if the cue would jump the guest into a different interview-state sequence prematurely. |
| `redundant_cue` | Suppress repeated prompts for an already captured or substituted ingredient. |
| `stronger_unexpected_ingredient` | Suppress planned cue and log possible substitution. |
| `timebox_risk` | Suppress low-priority cue when it would endanger mandatory coverage. |
| `checklist_pressure` | Suppress if cues accumulate into interrogation behavior. |

### Cue Rate Limits and Cooldowns

| Rule | Limit |
|---|---|
| Maximum visible cues per interview-state step | 2 cues unless interviewer explicitly unlocks more. |
| Minimum interval between visible cues | 180 seconds or 12 speaker turns, whichever comes first. |
| Sensitive follow-up cooldown | One accepted sensitive cue locks adjacent sensitive cues for 8 speaker turns. |
| Emotional peak cooldown | No cues during peak and no cues for 90 seconds after peak resolves. |
| Repeated ingredient role cooldown | Same ingredient role cannot be cued twice unless quality remains below 0.45 and interviewer requests repair. |
| Checklist pressure pause | If 3 cues are suppressed for checklist pressure, cue stream enters passive-only mode until interviewer resets. |

### Gate Thresholds

| Gate ID | Threshold | Hard Fail | Consequence |
|---|---:|---|---|
| `live_cue_state_safe` | 1.00 | Yes | Cue cannot be shown. |
| `active_contract_bound` | 1.00 | Yes | Coverage tracker enters passive-only mode. |
| `ingredient_role_known` | 1.00 | Yes | Cue cannot be proposed. |
| `interviewer_confirmation_required` | 1.00 | Yes | Sensitive cue hidden until accepted. |
| `coverage_quantity_estimate` | 0.70 | No | Creates warning, not interruption. |
| `coverage_quality_estimate` | 0.65 | No | Creates provisional repair/pickup recommendation. |
| `guest_comfort_state` | 0.85 | Yes | Cue suppressed and session flag raised. |
| `checklist_pressure_score` | 0.20 maximum | Yes | Cue stream paused. |

### Gate Verdict Semantics

| Verdict | Rule | Receipt Behavior |
|---|---|---|
| `PASS` | Cue is state-safe, rate-safe, and source-supported. | Show cue and write receipt when decided. |
| `PROVISIONAL` | Cue is useful but non-mandatory, low urgency, or near cooldown boundary. | Hold cue for interviewer review; do not auto-display. |
| `FAIL` | Cue misses safety, quality, or redundancy checks. | Suppress cue and write actionable suppression receipt. |
| `BLOCKED` | Session lacks approved brief, active contract, or valid source tick. | Enter passive-only coverage mode. |

## 4. Implementation Plan

1. Add `src/ccp_studio/services/live_ingredient_coverage_service.py`.
2. Add coverage state creation when a Complete Expression Session starts from an approved Interview Brief V2.
3. Subscribe to live transcript ticks, anchor hits, speaker turns, silence/pause markers, and manual interviewer events.
4. Update coverage items with provisional status and quality estimates.
5. Run cue proposal logic only after state and suppression checks.
6. Add cue decision lifecycle: proposed, suppressed, accepted, ignored, expired.
7. Emit receipts for every accepted, ignored, or suppressed cue.
8. Add PWA live panel that shows coverage as calm status, not as a task checklist.
9. Add Telegram quick cue channel with strict rate limits and suppression.
10. Export final coverage state to post-session Expression Ingredient Inventory and gap planning.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class LiveCueDecisionReceipt(BaseModel):
    schema_version: Literal["cmf.live_cue_decision_receipt.v1"]
    receipt_id: str
    expression_session_id: str
    interview_brief_id: str
    active_contract_id: str | None = None
    cue_id: str
    cue_type: str
    ingredient_role: str | None = None
    proposed_at_tick: int = Field(ge=0)
    decision: Literal["shown", "accepted", "ignored", "suppressed", "expired"]
    suppression_reason: str | None = None
    current_interview_state: str
    emotional_peak_active: bool
    operator_or_interviewer_id: str | None = None
    state_safe: bool
    source_event_refs: list[str]


class LiveCoverageReadModel(BaseModel):
    schema_version: Literal["cmf.live_coverage_read_model.v1"]
    expression_session_id: str
    current_interview_state: str
    mandatory_total: int
    mandatory_captured_or_quality_passed: int
    optional_total: int
    optional_captured_or_quality_passed: int
    suppressed_cue_count: int
    pickup_recommendation_count: int
    calm_summary: str
```

## 6. Workflow

```text
session_started
-> load_approved_interview_brief_v2
-> create_live_coverage_state
-> ingest_transcript_tick
-> detect_possible_ingredient
-> update_coverage_item
-> evaluate_interview_state
-> run_cue_suppression_policy
-> propose_or_suppress_cue
-> interviewer_accepts_or_ignores
-> receipt_written
-> final_coverage_state_exported
```

## 7. API, Service, and Event Contracts

| Contract | Shape |
|---|---|
| `POST /api/cmf/expression-sessions/{id}/coverage/start` | Creates coverage state from approved brief. |
| `POST /api/cmf/expression-sessions/{id}/coverage/tick` | Updates coverage from live transcript/event tick. |
| `POST /api/cmf/expression-sessions/{id}/coverage/cues/{cue_id}/decision` | Records accepted, ignored, or suppressed cue. |
| `GET /api/cmf/expression-sessions/{id}/coverage` | Returns calm operator read model. |

Events:

```text
LiveCoverageStateCreated
CoverageItemUpdated
LiveCueProposed
LiveCueSuppressed
LiveCueAccepted
IngredientGapDetected
PickupRequested
```

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate / Test Evidence |
|---|---|---|---|
| AC1 | Coverage state cannot start without an approved Interview Brief V2 or retrospective adapter receipt. | Coverage starts from a draft brief and produces cues during a live interview. | Phase4-M01, `EXP-PER-003`; coverage start test. |
| AC2 | Cue proposal is blocked during emotional peaks, unsafe guest states, and cooldown windows. | The tracker interrupts a vulnerable memory moment to request a mechanism follow-up. | Phase4-M04, `EXP-FRC-006`; suppression policy test. |
| AC3 | Sensitive cues require interviewer confirmation and write cue decision receipts. | A sensitive follow-up appears directly to the interviewer without confirmation or receipt row. | Phase5-M01, `EXP-SOC-001`; receipt persistence test. |
| AC4 | Coverage estimates remain provisional and cannot override human judgment. | A provisional score marks a required ingredient as final-approved without post-session review. | Phase4-M05, `EXP-FBK-001`; state transition test. |
| AC5 | Unexpected high-value ingredients can substitute planned ingredients only with source evidence and receipt. | The tracker marks a substitution without a source tick or operator-visible rationale. | Phase5-M01, `EXP-SOC-001`; substitution receipt test. |
| AC6 | The UI never presents ingredient coverage as a coercive checklist. | The PWA shows a red task list that pushes the interviewer to ask every missing item immediately. | Phase4-M04, `EXP-FRC-006`; UI read-model test. |

## 9. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| State-machine tests | Coverage only starts from approved session context. |
| Suppression tests | Emotional peak, safety, redundant, and checklist-pressure cues are blocked. |
| Cue receipt tests | Every decision emits receipt with source tick refs. |
| Quality estimate tests | Provisional scores never mark final approval. |
| Unexpected ingredient tests | Substitution creates explicit event and downstream review flag. |
| UI read-model tests | Calm summary avoids checklist language and shows blockers clearly. |

## 10. Doctrine-Driven Test Harness Binding

The harness must evaluate:

```text
live_cue_state_safe
guest_dignity_preserved
checklist_pressure_below_threshold
coverage_signal_source_supported
interviewer_authority_preserved
pickup_recommendation_grounded
```

Hard failures block cue display and create live approval blockers.

## Spec Audit Receipt

| Check | Status |
|---|---|
| Does not flatten interview-state and viewer-state sequencing | Pass |
| Does not force the guest into an asset checklist | Pass |
| Attaches to Complete Expression Session instead of inventing a parallel session runtime | Pass |
| Preserves human interviewer authority | Pass |
| Emits receipts for cue decisions and suppression | Pass |
