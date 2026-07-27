---
tech_spec_id: "TS-CMF-115"
title: "Interview Brief V2 Procurement, Sequence Hypotheses, and Expression Acquisition Plan"
story_id: "12.2"
story_title: "Interview Brief V2 Procurement"
epic_id: 12
epic_title: "Conscious Sequencing and Expression Acquisition"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP Conscious Sequencing and Expression Acquisition Engine V1 bundle"
pipeline_stage: "4 / 5 / 6"
entry_object: "SaturationContextBundle, Brand Context, Guest Dossier, Audience Reality Brief, Context Premises, Matrix of Edging, asset portfolio intent"
exit_object: "InterviewBriefV2, SequenceHypothesis list, ExpressionAcquisitionPlan, InterviewAssetContractV2 drafts, procurement readiness receipt"
validation_contract: "source saturation, sequence hypothesis coverage, acquisition role coverage, state-aware interview flow, safety constraints, operator approval"
required_receipt: "InterviewBriefV2ProcurementReceipt"
runtime_target: "Python / Pydantic v2 / DSPy / JIT Skill Compiler / Pi harness / PWA review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-115: Interview Brief V2 Procurement, Sequence Hypotheses, and Expression Acquisition Plan

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for intelligence-gated pipeline work. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 CBAR mandates for verifiable artifacts and earned progression. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | Phase 4 adversarial audit trail. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` | Phase 5 adversarial audit trail. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Product owner for FR-CMF-12.02. |
| `THE CMF STUDIO/CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/ccp_conscious_sequence_engine_v1/00_AGENT_START_HERE.md` | Boot order, runtime authority, interview-state versus viewer-state distinction. |
| `.../01_MASTER_SPEC.md` | Interview Brief V2, Asset Portfolio Intent, Sequence Hypotheses, Expression Acquisition Plan, Interview Asset Contract V2. |
| `.../02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Brief, requirement, and asset-contract states. |
| `.../03_RUNTIME_WORKFLOWS.md` | Pre-interview compiler workflow. |
| `.../05_EVALUATION_GOVERNANCE_AND_LEARNING.md` | Research and procurement readiness gates. |
| `.../models/sequence_engine_models.py` | Pydantic fields for `InterviewBriefV2`, `SequenceHypothesis`, `ExpressionAcquisitionPlan`, and `InterviewAssetContractV2`. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | JIT compiler and saturation context dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-027-interview-asset-contract-and-quality-gate.md` | Current Interview Asset Contract boundary. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-029-complete-expression-session-creation.md` | Downstream Complete Expression Session boundary. |
| `src/ccp_studio/contracts/skills.py` | Existing skill modes and saturation context fields for conscious interview brief and interview engineering. |
| `src/ccp_studio/services/jit_skill_compiler_service.py` | Existing invocation, anti-draft, evidence, and receipt enforcement. |

## 2. Overview

This spec upgrades the Conscious Interview Brief from a question document into a procurement contract. Interview Brief V2 must declare what asset portfolio CMF intends to produce, which viewer-state sequence hypotheses those assets require, which expression ingredients must be acquired, which acquisition instruments will be used, and which Interview Asset Contracts will guide the live session.

The brief does not force the guest into the final content sequence. It creates an interview-state sequence that protects safety and emergence while still making sure the factory has the right ingredients for later content programs.

The first monthly artifact remains the Interview Brief. If no interview exists, CMF may enter from existing transcript and footage, but the same sequence and ingredient contracts still apply as retrospective procurement/evidence contracts.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-115-001 | `AssetPortfolioIntent` | Declares target formats, asset derivatives, and exploratory/mandatory status. |
| DEP-CMF-115-002 | `SequenceHypothesis` | Defines provisional viewer-state recipe and promised payoff. |
| DEP-CMF-115-003 | `IngredientRequirement` | Defines one required ingredient role, source preference, substitutes, and minimum quality. |
| DEP-CMF-115-004 | `ExpressionAcquisitionPlan` | Deduplicates ingredient requirements and binds acquisition instruments. |
| DEP-CMF-115-005 | `InterviewBriefV2` | Canonical procurement brief for monthly interview planning. |
| DEP-CMF-115-006 | `InterviewAssetContractV2` | Contract bridge into Complete Expression Session. |
| DEP-CMF-115-007 | `InterviewBriefV2ProcurementReceipt` | Approval receipt for procurement readiness. |
| DEP-CMF-115-008 | `InterviewBriefV2ReadModel` | Operator-facing read model for review and readiness. |

### Existing Backend Integration

| Python Owner | Database Table(s) | API Route(s) | Migration / Backfill Behavior |
|---|---|---|---|
| `src/ccp_studio/contracts/conscious_sequencing.py` | n/a | n/a | Adds DEP-CMF-115 contract models. |
| `src/ccp_studio/services/interview_brief_v2_service.py` | `interview_briefs_v2`, `sequence_hypotheses`, `expression_acquisition_plans` | `POST /api/cmf/interview-briefs-v2`, `POST /api/cmf/interview-briefs-v2/{id}/approve` | New migration; legacy Conscious Interview Briefs require adapter receipt. |
| `src/ccp_studio/services/jit_skill_compiler_service.py` | `skill_invocation_receipts`, `receipt_chain` | compiler-internal | Extends allowed outputs for DEP-CMF-115 objects. |
| `src/ccp_studio/services/interview_asset_contract_v2_service.py` | `interview_asset_contracts_v2` | `POST /api/cmf/interview-briefs-v2/{id}/compile-contracts` | New table extends current IAC; does not mutate legacy IAC rows. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | `receipt_chain`, `evaluation_receipts`, `approval_blockers` | shared receipt writer | Writes `InterviewBriefV2ProcurementReceipt`. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PER-003` | Phase4-M01 | Operator must review procurement gaps before a session can activate. |
| `EXP-PRG-001` | Phase4-M03 | Compiler and coverage simulation must return readiness inline, not as a delayed batch. |
| `EXP-FRC-006` | Phase4-M04 | Blocked procurement must produce immediate repair actions, not a static failure. |
| `EXP-FBK-001` | Phase4-M05 | Every rejected question, ingredient, or contract must name the exact failing source. |
| `EXP-SOC-001` | Phase5-M01 | Approved Interview Brief V2 is a verifiable artifact with hashes and receipt-chain row. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Live session activation is locked until procurement readiness is approved. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Brief compilation returns readiness and blockers inline for the operator. |
| Phase4-M04: Frictionless Block Rule | Phase 4 Story 4.1 | `EXP-FRC-006` | Missing ingredient/instrument blockers return typed repair actions. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Rejections identify exact requirement, source gap, and repair follow-up. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Approved Interview Brief V2 writes hashes and receipt-chain proof. |

### Receipt Chain Guard

| Receipt | Table | Action | Idempotency Key | Required Hashes |
|---|---|---|---|---|
| `InterviewBriefV2ProcurementReceipt` | `receipt_chain` | `interview_brief_v2.approved` | `interview_brief_id + asset_portfolio_intent_hash` | brief JSON hash, asset intent hash, sequence hypothesis hashes, contract hashes |

### Compiler Responsibilities

| Compiler | Skill Use Mode | Output |
|---|---|---|
| `AssetPortfolioPlanner` | `conscious_interview_brief` / `interview_engineering` | `AssetPortfolioIntent` with canonical target formats and derivative slots. |
| `SequenceHypothesisCompiler` | `interview_engineering` | Candidate `SequenceHypothesis[]` for target archetypes and formats. |
| `IngredientRequirementCompiler` | `interview_engineering` | Deduplicated `ExpressionAcquisitionPlan`. |
| `InterviewAssetContractV2Compiler` | `conscious_interview_brief` | Source-backed `InterviewAssetContractV2[]`. |
| `CoverageSimulationEvaluator` | `evaluation_support` | Procurement readiness gaps and blocker list. |

### Interview Brief V2 Contents

| Object | Required Meaning |
|---|---|
| `research_context` | Immutable refs to Brand Context, Guest Dossier, Audience Reality, Context Premises, Interviewer Resonance, Matrix of Edging, CRAL findings, and audience evidence. |
| `asset_portfolio_intent` | Declares intended asset routes, formats, package logic, and exploratory/mandatory status. |
| `sequence_hypotheses` | Viewer-state recipes that may later become clips, carousels, single images, polls, reactions, or package assets. |
| `expression_acquisition_plan` | Ingredient requirements, shared groups, visual requests, research tasks, fallbacks, pickup policy. |
| `interview_state_sequence` | Guest-facing state progression through safety, memory, vulnerability, authority, teaching, humor, and invitation. |
| `live_coverage_policy` | Rules for tracking ingredient coverage without checklist coercion. |

### Interview Asset Contract V2 Relationship

`InterviewAssetContractV2` extends the current Interview Asset Contract from `TS-CMF-027`. It must add ingredient procurement and sequence hypothesis fields while preserving current quality gates, consent, route, and source-boundary rules.

| Current Contract Concern | V2 Addition |
|---|---|
| Target expression state | `target_expression_states` and interview-state sequence relation. |
| Anchor / question | `main_question`, `first_line_anchors`, `depth_anchor`, repair followups. |
| Route target | `sequence_hypothesis_ids`, target archetype, asset derivatives, format targets. |
| Quality gate | `coverage_success_rule`, mandatory roles, minimum ingredient count. |
| Safety | `safety_constraints` and sensitive follow-up confirmation. |

### Gate Thresholds

| Gate ID | Threshold | Hard Fail | Consequence |
|---|---:|---|---|
| `brand_context_pinned` | 1.00 | Yes | Brief cannot leave draft. |
| `research_context_saturation` | 0.90 | Yes | Sequence hypothesis compilation blocked. |
| `context_premise_source_support` | 0.90 | Yes | Acquisition plan blocked. |
| `matrix_reviewed` | 1.00 | Yes | Brief cannot enter operator review. |
| `asset_portfolio_declared` | 1.00 | Yes | Ingredient compiler blocked. |
| `sequence_hypothesis_coverage` | 0.85 | No | Provisional blocker; operator can approve exploratory status. |
| `required_ingredient_coverage` | 1.00 | Yes | Interview Asset Contract V2 approval blocked. |
| `acquisition_instrument_coverage` | 1.00 | Yes | Required roles without instruments or approved non-interview sources are blocked. |
| `safety_territory_declared` | 1.00 | Yes | Live session activation blocked. |
| `anti_draft_quality` | 0.85 | Yes | JIT compiler output rejected. |

### Gate Verdict Semantics

| Verdict | Rule | Receipt Behavior |
|---|---|---|
| `PASS` | Gate meets threshold and no hard blocker exists. | Write readiness receipt and allow next state. |
| `PROVISIONAL` | Non-hard gate is within 0.08 below threshold or exploratory status is declared. | Write receipt with operator review required. |
| `FAIL` | Threshold fails or source refs are missing. | Write actionable blocker and keep brief in current state. |
| `BLOCKED` | Brand Context, doctrine, Matrix, or safety territory is missing. | Stop session activation until revised brief is approved. |

## 4. Implementation Plan

1. Add `InterviewBriefV2` contracts to `src/ccp_studio/contracts/conscious_sequencing.py`.
2. Add `src/ccp_studio/services/interview_brief_v2_service.py` for state transitions, validation, receipts, and read models.
3. Extend JIT skill compiler allowed outputs for `AssetPortfolioIntent`, `SequenceHypothesis[]`, `ExpressionAcquisitionPlan`, and `InterviewAssetContractV2[]`.
4. Add DSPy signatures for the five compiler programs listed above.
5. Extend `SaturationContextBundle` validation so Interview Brief V2 requires source refs for Brand Context, CRAL findings, audience conversations, Context Premises, Matrix, interviewer resonance, primitive candidates, invariant fields, and route intent.
6. Add migration adapter from current Conscious Interview Brief output to Interview Brief V2.
7. Add procurement readiness eval that returns blockers and typed repair recommendations.
8. Add PWA review surface for asset portfolio intent, sequence hypotheses, ingredient requirements, question instruments, and safety constraints.
9. Emit `InterviewBriefV2ProcurementReceipt` on approval and every revision.
10. Make Complete Expression Session creation consume only approved Interview Brief V2 or an approved legacy-to-v2 adapter receipt.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class InterviewBriefV2ProcurementReceipt(BaseModel):
    schema_version: Literal["cmf.interview_brief_v2_procurement_receipt.v1"]
    receipt_id: str
    interview_brief_id: str
    brand_context_version_id: str
    doctrine_bundle_id: str
    saturation_context_refs: list[str]
    asset_portfolio_intent_hash: str
    sequence_hypothesis_ids: list[str]
    ingredient_requirement_ids: list[str]
    interview_asset_contract_ids: list[str]
    procurement_readiness_score: float = Field(ge=0, le=1)
    safety_constraints: list[str]
    blocker_codes: list[str] = Field(default_factory=list)
    operator_status: Literal["approved", "needs_revision", "rejected"]


class InterviewBriefV2ReadModel(BaseModel):
    schema_version: Literal["cmf.interview_brief_v2_read_model.v1"]
    interview_brief_id: str
    status: str
    target_asset_routes: list[str]
    sequence_hypothesis_count: int
    mandatory_requirement_count: int
    covered_requirement_count: int
    safety_constraint_count: int
    next_operator_action: str | None = None
```

The canonical `InterviewBriefV2`, `SequenceHypothesis`, `ExpressionAcquisitionPlan`, and `InterviewAssetContractV2` field definitions must remain schema-compatible with the bundle models unless CMF adds explicit migration fields.

## 6. Workflow

```text
load_brand_and_doctrine
-> load_research_context
-> compile_asset_portfolio_intent
-> compile_sequence_hypotheses
-> compile_expression_acquisition_plan
-> compile_interview_asset_contract_v2
-> simulate_live_coverage
-> operator_review
-> approved_interview_brief_v2
-> complete_expression_session_ready
```

State transitions:

```text
draft
-> research_complete
-> sequence_hypotheses_compiled
-> acquisition_plan_ready
-> operator_review
-> approved
-> active_session
-> superseded
```

## 7. API, Service, and Event Contracts

| Contract | Shape |
|---|---|
| `POST /api/cmf/interview-briefs-v2` | Creates a draft brief from saturation context. |
| `POST /api/cmf/interview-briefs-v2/{id}/compile-asset-portfolio` | Runs `AssetPortfolioPlanner`. |
| `POST /api/cmf/interview-briefs-v2/{id}/compile-sequence-hypotheses` | Runs `SequenceHypothesisCompiler`. |
| `POST /api/cmf/interview-briefs-v2/{id}/compile-acquisition-plan` | Runs `IngredientRequirementCompiler`. |
| `POST /api/cmf/interview-briefs-v2/{id}/compile-contracts` | Runs `InterviewAssetContractV2Compiler`. |
| `POST /api/cmf/interview-briefs-v2/{id}/approve` | Operator approval with receipt. |

Events:

```text
InterviewBriefV2Created
SequenceHypothesisCreated
IngredientRequirementAdded
InterviewAssetContractV2Drafted
InterviewBriefV2ProcurementEvaluated
InterviewBriefV2Approved
```

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate / Test Evidence |
|---|---|---|---|
| AC1 | Interview Brief V2 cannot be approved without pinned Brand Context, doctrine bundle, research context, Context Premise, Matrix of Edging, and asset portfolio intent. | A brief compiles questions from a guest bio but lacks Context Premise or Matrix refs and still activates a session. | Phase4-M01, `EXP-PER-003`; readiness gate test. |
| AC2 | Every mandatory target asset has a sequence hypothesis or explicit exploratory status. | A Guest Asset Pack requires a reaction clip but no sequence hypothesis or exploratory waiver exists. | Phase4-M05, `EXP-FBK-001`; blocker names target asset. |
| AC3 | Every required ingredient has an acquisition instrument, approved source, fallback, or pickup path. | `hidden_mechanism` is mandatory, but no question or source path exists and the brief is approved. | Phase4-M04, `EXP-FRC-006`; repair action test. |
| AC4 | Existing Interview Asset Contract rules remain enforced through V2 adapter. | A V2 contract bypasses consent, source-boundary, or route quality gates from TS-CMF-027. | Phase5-M01, `EXP-SOC-001`; adapter compatibility test. |
| AC5 | Live session activation is blocked until `InterviewBriefV2ProcurementReceipt.operator_status == approved`. | The Complete Expression Session starts from a draft brief. | Phase4-M01, `EXP-PER-003`; session activation test. |
| AC6 | Operator revisions create new receipt versions and never mutate approved history. | An approved brief is edited in place after operator approval. | Phase5-M01, `EXP-SOC-001`; receipt immutability test. |

## 9. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Compiler contract tests | DSPy/JIT outputs validate against Pydantic models. |
| Saturation negative tests | Missing Brand Context, Matrix, Context Premise, or CRAL refs block output. |
| Procurement gap tests | Required ingredient without instrument/source creates blocker. |
| Safety tests | Sensitive follow-ups require declared safety constraints. |
| State-machine tests | Invalid transition from draft to approved is blocked. |
| Legacy adapter tests | Existing Conscious Interview Brief can migrate only with explicit adapter receipt. |

## 10. Doctrine-Driven Test Harness Binding

The harness must evaluate:

```text
research_readiness
procurement_readiness
context_premise_source_support
asset_portfolio_intent_declared
ingredient_requirement_coverage
acquisition_instrument_coverage
interview_state_sequence_integrity
```

Hard failures become approval blockers visible in PWA and Telegram review.

## Spec Audit Receipt

| Check | Status |
|---|---|
| Preserves Interview Brief as the first monthly artifact | Pass |
| Uses JIT/DSPy for compilation but stable services for state, receipts, and approval | Pass |
| Extends current Interview Asset Contract rather than replacing it | Pass |
| Separates guest interview journey from final viewer sequence | Pass |
| Blocks generic, unsourced, or checklist-style interview generation | Pass |
