---
tech_spec_id: "TS-CMF-083"
title: "Expression Lineage and Interview Asset Contract Binding"
story_id: "7.13"
story_title: "Expression Lineage Binding"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition"
pipeline_stage: "8 / 9 / 10"
entry_object: "InterviewAssetContract and ExpressionMoment"
exit_object: "ExpressionLineageBindingReceipt"
validation_contract: "CES, IAC, expression moment, anchors, route, primitive coalition, eval targets"
required_receipt: "ExpressionLineageBindingReceipt"
runtime_target: "Python / Pydantic v2 / DSPy extraction outputs / repository services"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-083: Expression Lineage and Interview Asset Contract Binding

## 1. Purpose

Bind every composition to the interview intelligence that made it possible. The composition runtime must know which Interview Asset Contract produced the answer, how the answer was extracted, why it routes to a template, and what eval targets define success.

## 2. Required Lineage

Every binding must include:

- Complete Expression Session;
- Interview Asset Contract;
- selected question;
- First-Line Anchor options and selected anchor hit;
- Depth Anchor;
- expression states;
- source transcript segment;
- Expression Moment;
- Matrix of Edging brief;
- edge product;
- primitive coalition;
- core archetype;
- asset derivative;
- CMF route;
- four-video slot when applicable;
- reaction seed when applicable;
- eval requirements.

## 3. Primary Contract

```python
class ExpressionLineageBindingReceipt(BaseModel):
    schema_version: Literal["cmf.expression_lineage_binding_receipt.v1"]
    receipt_id: UUID
    complete_expression_session_id: UUID
    interview_asset_contract_id: UUID
    expression_moment_id: UUID
    source_question_id: UUID
    transcript_segment_ids: list[UUID]
    first_line_anchor_hit_id: UUID | None
    depth_anchor_ref: str | None
    target_expression_states: list[str]
    core_archetype: str
    asset_derivative: str
    cmf_route: str
    four_video_slot_code: str | None
    edge_product: str
    primitive_coalition_refs: list[str]
    eval_target_refs: list[str]
    blocker_codes: list[str]
    decision: Literal["bound", "blocked", "candidate_only"]
```

## 4. Binding Rules

- No composition from a visual idea alone.
- No four-video slot fill without source-supported Expression Moment.
- No reaction template without reaction seed, reaction candidate, or interview interaction evidence.
- No Challenger proof card without source support.
- No Cinematic Story without story/witness/backstory source.
- No Educational Explainer without teaching/concept/framework source.

## 5. Commands and Receipts

| Type | Names |
|---|---|
| Commands | `BindExpressionLineageCommand`, `ValidateInterviewAssetContractRouteCommand`, `RecordExpressionLineageBindingReceiptCommand` |
| Events | `ExpressionLineageBound`, `ExpressionLineageBlocked`, `ExpressionLineageMarkedCandidateOnly` |
| Receipt | `ExpressionLineageBindingReceipt` |

## 6. Blockers

| Blocker | Trigger |
|---|---|
| `COMPLETE_EXPRESSION_SESSION_MISSING` | No upstream session. |
| `INTERVIEW_ASSET_CONTRACT_MISSING` | Question is not represented as contract. |
| `EXPRESSION_MOMENT_MISSING` | No approved source moment. |
| `ANCHOR_BOUNDARY_MISSING` | Clip start cannot be explained. |
| `ARCHETYPE_ROUTE_MISSING` | No core archetype or derivative. |
| `PRIMITIVE_COALITION_MISSING` | No primitive evidence for source force. |
| `REACTION_SEED_REQUIRED` | Reaction format lacks reaction seed or human interaction source. |

## 7. Acceptance Criteria

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Every runtime composition has expression lineage receipt. | Template built from a screenshot prompt. |
| AC2 | Four-video slot assignment is source-supported. | System fabricates SV-RRC because quota requires it. |
| AC3 | Route selection includes edge and primitive rationale. | Route is "looks good for reels." |
| AC4 | Reaction seed is stored for reaction-based routes. | Poll video has no stored reaction question. |

## 8. Testing

- IAC-to-expression binding tests.
- Missing source blockers.
- Four-slot source support tests.
- Reaction seed requirement tests.
- Route mismatch negative fixtures.

