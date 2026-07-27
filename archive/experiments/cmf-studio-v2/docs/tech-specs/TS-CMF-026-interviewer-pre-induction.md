---
tech_spec_id: "TS-CMF-026"
title: "Interviewer Pre-Induction"
story_id: "5.4"
story_title: "Interviewer Pre-Induction"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-5-4-interviewer-pre-induction.md"
fr_ids:
  - "FR-CMF-05.04"
pipeline_stage: "4"
entry_object: "session plan"
exit_object: "PreInductionPlan"
validation_contract: "anti-centroid and manipulation gate"
required_receipt: "pre-induction receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy / PWA"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-026: Interviewer Pre-Induction

**Status:** Ready for Development  
**Story:** `5.4 - Interviewer Pre-Induction`  
**Implementation Boundary:** Pre-session Operator guidance, authentic curiosity prompts, emotional bridges, avoid-lists, opening state, anti-centroid checks, and manipulation safety gate.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-5-4-interviewer-pre-induction.md` | Story source, acceptance criteria, and handoff requirements. |
| `docs/epics.md` | Epic 5 sequencing and FR coverage. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-05.04 authority and anti-pattern rules. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Human activation protocol and Operator role. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Narrative State Induction as structured facilitation, not scripting. |
| `THE CMF STUDIO/Claude Ntahuga Interview Deck — V4.docx.md` | First-Line Anchor and Depth Anchor operating protocol. |
| `docs/architecture.md` | InterviewPreparationWorkflow and induction rules. |
| `docs/cmf-studio-pipeline-map.md` | Interview intelligence sub-workflow. |
| `docs/migration/legacy-inventory.md` | TTT, cognitive primitives, and narrative intelligence references. |

## 2. Overview

Implement `PreInductionPlan` as the Operator-facing preparation layer before live capture. The plan gives authentic curiosity prompts, emotional bridges, questions to avoid, guest-specific resonance, opening state, Matrix pressure, and safety warnings. It must help the Operator guide a real human into clearer expression without scripting, manipulation, or replacing the Operator's judgment.

The plan becomes the bridge between research/context intelligence and Live Interview Mode. It must be editable, evidence-backed, and preserved as a receipt before the Complete Expression Session starts.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-05.04 | Operators can run interviewer pre-induction to refine authentic curiosity, emotional bridges, questions to avoid, guest-specific resonance, and opening state. | `PreInductionPlan`, resonance context, anti-centroid gate, manipulation gate, Operator edit trail, and pre-induction receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 4 - Interview intelligence and induction planning |
| Entry Object | session plan |
| Exit Object | `PreInductionPlan` |
| Validation Contract | anti-centroid and manipulation gate |
| Required Receipt | pre-induction receipt |

### Legacy Intelligence Mapping

- V9 defines Narrative State Induction as structured facilitation preserving authentic human speech.
- TTT transition grammar informs opening state and state-transition warnings.
- First-Line Anchors and Depth Anchors are preparation affordances, not scripts.
- Primitive families PRS, PSY, SAF, HUM inform evaluation and UI review language.

## 4. Implementation Plan

1. Add contracts for `PreInductionPlan`, `PreInductionQuestion`, `InductionBridge`, `QuestionAvoidanceRule`, `OperatorEdit`, and `PreInductionReceipt`.
2. Implement `CompilePreInductionPlanCommand` from approved dossier, context, resonance, Matrix brief, and draft session plan.
3. Implement evaluator for centroid risk, manipulation risk, missing evidence, unsupported emotional claim, and routeability weakness.
4. Expose plan review/edit surface in Interview Intelligence Studio.
5. Preserve Operator edits with source evidence and induction rationale.
6. Bind approved pre-induction receipt to Live Interview Mode startup.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class InductionRiskLevel(str, Enum):
    LOW = "low"
    REVIEW = "review"
    BLOCKED = "blocked"


class QuestionAvoidanceRule(BaseModel):
    rule_id: str
    reason: str
    evidence_ids: list[str]
    safer_route: str


class InductionBridge(BaseModel):
    bridge_id: str
    emotional_bridge: str
    guest_specific_resonance: str
    matrix_edge_product_id: str | None = None
    evidence_ids: list[str]


class PreInductionQuestion(BaseModel):
    question_id: str
    natural_question: str
    authentic_curiosity: str
    first_line_anchor_options: list[str] = []
    depth_anchor: str | None = None
    centroid_risk: InductionRiskLevel
    manipulation_risk: InductionRiskLevel
    rationale_id: str | None = None


class PreInductionPlan(BaseModel):
    pre_induction_plan_id: str
    brand_id: str
    guest_id: str
    operator_id: str
    context_premise_id: str
    matrix_brief_id: str
    opening_state: str
    bridges: list[InductionBridge]
    questions_to_avoid: list[QuestionAvoidanceRule]
    planned_questions: list[PreInductionQuestion]
    operator_edit_ids: list[str] = []
    approved_at: datetime | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompilePreInductionPlanCommand`, `EvaluatePreInductionPlanCommand`, `EditPreInductionQuestionCommand`, `BlockManipulativePromptCommand`, `ApprovePreInductionPlanCommand` |
| Events | `PreInductionPlanCompiled`, `PreInductionPlanEvaluated`, `PreInductionQuestionEdited`, `PreInductionPromptBlocked`, `PreInductionPlanApproved` |
| Workflow | `InterviewPreparationWorkflow.stage4_pre_induction` |
| Receipt | `PreInductionReceipt` with context IDs, Matrix ID, risk scores, edit trail, approval state, and Live Interview Mode binding |

Live Interview Mode can read the approved plan, but cannot mutate it. Late changes create a new plan version and receipt.

## 7. Backward Compatibility and Migration Fallback

Legacy TTT and interview deck examples can seed guidance patterns and evaluator fixtures. They are not copied as hard-coded prompts. If the plan lacks enough guest-specific evidence, the system must surface a shallow/low-certainty mode rather than generating intimate psychological guidance.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Helpful guidance vs. scripting | Plan offers bridges, anchors, and avoid-lists; Operator retains live judgment. | Live session receipt records plan reference and Operator choices. |
| Emotional depth vs. manipulation | Manipulation gate blocks coercive or scripted performance prompts. | Block event includes reason and safer route. |
| Anti-centroid pressure vs. truth preservation | System recommends collision-bearing routes without forcing the guest's landing. | Follow-up guidance keeps "answer may land elsewhere" state. |

## 9. Tasks

- Add pre-induction contracts and persistence tables.
- Implement compile/evaluate/edit/approve command handlers.
- Add PWA Interview Intelligence Studio review state.
- Add risk evaluator for centroid, manipulation, unsupported claim, and routeability weakness.
- Add Live Interview Mode read binding for approved plan.
- Add fixtures from V9, Claude deck, Matrix, and TTT references.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Operator sees curiosity prompts, bridges, avoid-list, resonance, and opening state. | Pre-induction screen only shows question text. |
| AC2 | Centroid-safe question is flagged with better route. | Generic question passes with no warning. |
| AC3 | Operator edits preserve evidence and rationale. | Edited question loses source links. |
| AC4 | Manipulative or scripted prompt is blocked or marked for rewrite. | System tells guest what to feel or perform. |
| AC5 | Approved plan feeds session start without replacing judgment. | Live mode auto-advances scripted answers. |

## 11. Dependencies

- TS-CMF-023 research evidence.
- TS-CMF-024 context and resonance compilation.
- TS-CMF-025 Matrix of Edging brief.
- TS-CMF-002 stage execution records.
- TS-CMF-005 role permissions.

## 12. Testing Strategy


Unit tests:

- Unit tests for plan schema, risk states, and edit trail immutability.
- Evaluator tests for generic question, manipulation, unsupported psychology, and missing source rationale.
- Workflow tests for plan approval and Live Interview Mode binding.
- UI contract tests for review/edit/approve states.
- Fixture tests from Claude deck protocol: main question, first-line anchors, depth anchor, follow-ups.

Integration tests:

- Workflow test from `session plan` to `PreInductionPlan` through pipeline stage `4`.
- Command Bus test proving `pre-induction receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for centroid risk, manipulation blocks, edit count, approval latency, and live plan usage.
- Audit log for every Operator edit and evaluator decision.
- Recovery: blocked prompt can be revised by Operator or recompiled with richer Matrix/context input.
- Rollback: supersede approved plan and require new receipt before session start.

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
| Tech Spec ID | TS-CMF-026 |
| Story | 5.4 |
| Requirement Trace | FR-CMF-05.04 |
| Pipeline Trace | Stage 4, session plan to PreInductionPlan |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No scripting, no manipulation, no generic question plan, no legacy runtime coupling |

