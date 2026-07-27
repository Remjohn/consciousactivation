---
tech_spec_id: "TS-CMF-027"
title: "Interview Asset Contract and Quality Gate"
story_id: "5.5"
story_title: "Interview Asset Contract and Quality Gate"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-5-5-interview-asset-contract-and-quality-gate.md"
fr_ids:
  - "FR-CMF-05.05"
  - "FR-CMF-05.06"
  - "FR-CMF-05.07"
pipeline_stage: "4"
entry_object: "preparation artifacts"
exit_object: "InterviewAssetContract, deck"
validation_contract: "routeability and expression/archetype separation"
required_receipt: "contract compilation receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-027: Interview Asset Contract and Quality Gate

**Status:** Ready for Development  
**Story:** `5.5 - Interview Asset Contract and Quality Gate`  
**Implementation Boundary:** Interview Asset Contract compiler, Interview Deck contract set, expression-state vs archetype separation, routeability gate, anchor/follow-up fields, and contract compilation receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-5-5-interview-asset-contract-and-quality-gate.md` | Story source and acceptance criteria. |
| `docs/epics.md` | Epic 5 FR coverage and dependencies. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-05.05 through FR-CMF-05.07 authority. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Interview Asset Contract as upstream production infrastructure. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview Asset Contract atomic unit and Narrative State Induction. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Interview Deck as Asset Contract and schema fields. |
| `THE CMF STUDIO/Claude Ntahuga Interview Deck — V4.docx.md` | Practical deck structure with target archetype, derivative, state, anchors, and follow-ups. |
| `docs/architecture.md` | Induction rule, compiler registry, and contract lifecycle. |
| `docs/cmf-studio-pipeline-map.md` | Stage 4 interview intelligence sub-workflow. |
| `docs/migration/legacy-inventory.md` | Archetype prompts, primitives, and narrative intelligence migration targets. |

## 2. Overview

Implement `InterviewAssetContract` as the atomic upstream production object. In CMF STUDIO, a content-intended interview question is not merely a prompt. It is a typed contract carrying target expression state, target archetype, asset derivative, edge product, first-line anchors, depth anchor, repair followups, CMF route, expected source material, clip rules, and evaluation logic.

The quality gate must explicitly distinguish expression states from output archetypes. Expression states guide induction. Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode registries define output structure and route options.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-05.05 | Compile Interview Asset Contracts with target expression state, target archetype, asset derivative, edge product, anchors, repair followups, CMF route, and evaluation logic. | Contract schema, compiler, deck object, anchor/follow-up fields, and receipt. |
| FR-CMF-05.06 | Distinguish expression states from archetypes. | Separate enum/reference fields and quality gate rejection when confused. |
| FR-CMF-05.07 | Evaluate interview plans for saturation, collision strength, anti-centroid risk, specificity, and routeability. | `InterviewPlanEvaluationReceipt` and routeability gate. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 4 - Interview intelligence and induction planning |
| Entry Object | preparation artifacts |
| Exit Object | `InterviewAssetContract`, deck |
| Validation Contract | routeability and expression/archetype separation |
| Required Receipt | contract compilation receipt |

### Legacy Intelligence Mapping

- V9/V9.1 define the contract object and anchor doctrine.
- Claude Interview Deck demonstrates how target archetype, asset derivatives, states, edge product, CMF routes, anchors, and follow-ups combine.
- Archetype migration docs define valid output structure registries.
- Matrix and primitive outputs remain traceable through contract fields.

## 4. Implementation Plan

1. Add contracts for `InterviewAssetContract`, `InterviewDeck`, `FirstLineAnchorSet`, `DepthAnchor`, `RepairFollowups`, `ContractRouteTarget`, and `InterviewPlanEvaluationReceipt`.
2. Implement `InterviewAssetContractCompiler` and `InterviewDeckCompiler` with required inputs: research snapshot, context artifacts, Matrix brief, pre-induction plan, brand context, and registry versions.
3. Add quality gate for saturation, collision strength, anti-centroid risk, specificity, routeability, expression/archetype separation, and supported content format.
4. Persist contract/deck versions and bind approved contract IDs to Complete Expression Session creation.
5. Expose review endpoints and Operator approval workflow.
6. Emit `InterviewAssetContractCompiled` and `InterviewDeckApproved` events.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class ExpressionState(str, Enum):
    CINEMATIC = "cinematic"
    VULNERABILITY = "vulnerability"
    AUTHORITY = "authority"
    MEANING = "meaning"
    INVITATION = "invitation"


class FirstLineAnchorSet(BaseModel):
    cinematic: str | None = None
    emotional: str | None = None
    reels_hook: str | None = None


class RepairFollowups(BaseModel):
    too_historical: str
    too_abstract: str
    too_flat: str
    not_clip_ready: str


class ContractRouteTarget(BaseModel):
    core_archetype_ref: str
    asset_derivative_refs: list[str]
    meme_mechanism_refs: list[str] = []
    reaction_archetype_refs: list[str] = []
    cmf_render_mode_refs: list[str]


class InterviewAssetContract(BaseModel):
    contract_id: str
    brand_id: str
    guest_id: str
    question_id: str
    main_question: str
    target_expression_states: list[ExpressionState] = Field(min_length=1)
    route_target: ContractRouteTarget
    edge_product_id: str
    first_line_anchors: FirstLineAnchorSet
    depth_anchor: str
    expected_source_material: list[str]
    clip_start_rule: str
    depth_eval_rule: str
    landing_eval_targets: list[str]
    repair_followups: RepairFollowups
    evidence_ids: list[str]
    matrix_brief_id: str
    induction_rationale_ids: list[str] = []


class InterviewDeck(BaseModel):
    interview_deck_id: str
    brand_id: str
    guest_id: str
    contract_ids: list[str] = Field(min_length=1)
    evaluation_receipt_id: str
    approved_for_session: bool = False
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileInterviewAssetContractCommand`, `CompileInterviewDeckCommand`, `EvaluateInterviewPlanCommand`, `RejectExpressionArchetypeConfusionCommand`, `ApproveInterviewDeckCommand`, `BindDeckToExpressionSessionCommand` |
| Events | `InterviewAssetContractCompiled`, `InterviewPlanEvaluated`, `InterviewDeckCompiled`, `InterviewDeckRejected`, `InterviewDeckApproved`, `InterviewDeckBoundToSession` |
| Workflow | `InterviewPreparationWorkflow.stage4_compile_asset_contracts` |
| Receipt | `ContractCompilationReceipt` with input artifact IDs, registry versions, route targets, evaluation scores, and approval state |

## 7. Backward Compatibility and Migration Fallback

Legacy archetype prompts are deconstructed into registry-backed route targets and DSPy compiler fixtures. A legacy prompt family cannot be referenced by a production contract unless it has a migrated registry ID and validation receipt.

If routeability fails, the contract is not approved for session use. The system can return to Matrix selection or context saturation rather than inventing unsupported routes.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Production intent vs. scripting | Contract defines route/eval intent while allowing the guest to answer authentically. | Complete Expression Session stores contract ID and actual answer outcome. |
| Expression state vs. output archetype | Schema separates induction state from route target registries. | Quality gate rejects confused or missing route fields. |
| Route ambition vs. source truth | Contract cannot approve without saturation, collision, specificity, and evidence. | Evaluation receipt travels into extraction review. |

## 9. Tasks

- Add contracts and persistence for Interview Asset Contract and Interview Deck.
- Implement DSPy contract/deck compilers.
- Add route registry validation for archetype, derivative, meme, reaction, and CMF render mode refs.
- Add quality gate and receipt writer.
- Add review/approval endpoints and UI contracts.
- Add binding to Complete Expression Session creation.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Each question includes expression state, route, derivative, edge, anchors, followups, CMF route, and evaluation logic. | Question only contains text and a hook label. |
| AC2 | Expression/archetype confusion is rejected. | `vulnerability` is used as an output archetype. |
| AC3 | Weak saturation/collision/specificity/routeability blocks approval. | Generic contract is approved with no evidence IDs. |
| AC4 | Approved contract binds to Complete Expression Session. | Session starts with no deck or contract IDs. |
| AC5 | Extraction review shows induction context. | Expression Moment cannot show its originating contract. |

## 11. Dependencies

- TS-CMF-023 through TS-CMF-026.
- TS-CMF-014 registry conversion and evals.
- TS-CMF-015 JIT skill compilers.
- TS-CMF-017 intentional orchestration contracts.
- TS-CMF-002 stage execution records.

## 12. Testing Strategy


Unit tests:

- Unit tests for contract schema and required route fields.
- Quality gate tests for expression/archetype confusion, weak routeability, missing evidence, generic text, and unsupported format.
- DSPy compiler tests with V9/V9.1 and Claude deck fixtures.
- Workflow tests binding approved deck to a Complete Expression Session.
- Registry validation tests against migrated archetype and asset derivative registries.

Integration tests:

- Workflow test from `preparation artifacts` to `InterviewAssetContract, deck` through pipeline stage `4`.
- Command Bus test proving `contract compilation receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for contract approval rate, routeability failures, expression/archetype confusion, unsupported registry refs, and session binding failures.
- Audit log compiler input hashes, registry versions, and reviewer decisions.
- Recovery: revise rejected contracts by updating Matrix/context/route targets.
- Rollback: supersede approved deck and block session start until a new receipt exists.

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
| Tech Spec ID | TS-CMF-027 |
| Story | 5.5 |
| Requirement Trace | FR-CMF-05.05, FR-CMF-05.06, FR-CMF-05.07 |
| Pipeline Trace | Stage 4, preparation artifacts to InterviewAssetContract/deck |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No newsletters, no expression/archetype collapse, no unsupported route targets, no scripting |

