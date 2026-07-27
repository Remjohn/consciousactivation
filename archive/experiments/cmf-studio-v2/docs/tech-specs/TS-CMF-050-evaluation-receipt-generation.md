---
tech_spec_id: "TS-CMF-050"
title: "Evaluation Receipt Generation"
story_id: "9.1"
story_title: "Evaluation Receipt Generation"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-9-1-evaluation-receipt-generation.md"
fr_ids:
  - "FR-CMF-09.01"
pipeline_stage: "13"
entry_object: "render/package ready for review"
exit_object: "EvaluationReceipt"
validation_contract: "category thresholds and evidence"
required_receipt: "evaluation receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / DSPy / evaluation workflow"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-050: Evaluation Receipt Generation

**Status:** Ready for Development  
**Story:** `9.1 - Evaluation Receipt Generation`  
**Implementation Boundary:** EvaluationReceipt, evaluator category contracts, evidence pointers, hard-failure policy, revision-linked immutable receipts, and approval blockers emitted from failed evaluation.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-9-1-evaluation-receipt-generation.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-09.01 authority and evaluation category list. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Evaluation, human approval, CBAR, and legacy intelligence doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Evaluation layer, threshold, hard-fail, and EvaluationReceipt contract source. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, 64-state acting library, PaperCut avatar rig, micro-semiotic anchors, and 2.5D PaperCut animation doctrine. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Ideogram 4 composition contract, acting-reference retrieval, PaperCut style constitution, layer extraction, and deterministic 2D animation doctrine. |
| `docs/architecture.md` | Evaluation core objects, publishing rule, and stage constraints. |
| `docs/cmf-studio-pipeline-map.md` | Stage 13 evaluation and review trace. |
| `docs/migration/legacy-inventory.md` | CBAR gate packs, receipt chain, anti-draft calibration, and SDA/SFL failure corpora. |
| `reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Legacy truth to evaluation content compiler chain. |

## 2. Overview

Evaluation begins whenever a doctrine-governed production object is ready to advance, not only when a render output or asset package is ready for review. It creates immutable receipts for interview briefs, interview asset contracts, Brand Genesis sessions, Brand Context locks, 64-state acting libraries, PaperCut rigs, rig manifests, animation plans, render outputs, and asset packages.

The category set includes source truth, doctrine alignment, CCF orchestration lineage, primitive registry fidelity, Context Premise integrity, Narrative State Induction integrity, anchor contract integrity, Brand Genesis completeness, acting-library coverage, PaperCut rig integrity, micro-semiotic integrity, animation readiness, asset-generation policy, archetype fit, expression depth, identity consistency, likeness, composition, style, motion restraint, platform fit, negative space, micro-semiotic anchors, routeability, evaluation-target coverage, and publishing readiness.

Scores are calibration aids, not final authority. Each receipt must carry evidence, evaluator version, threshold profile, hard failures, warnings, object lineage, and a decision recommendation. Any hard failure becomes an approval blocker for Story 9.4.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-09.01 | Generate evaluation receipts for truth, fit, depth, identity, likeness, composition, style, motion, platform, negative space, micro-semiotic anchors, routeability, and publishing readiness. | Evaluation category contracts, evidence validation, immutable receipts, hard-failure policy, rerun supersession, and approval-blocker handoff. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 13 - Evaluation, review, revision, approval |
| Entry Object | render/package ready for review |
| Exit Object | `EvaluationReceipt` |
| Validation Contract | category thresholds and evidence |
| Required Receipt | evaluation receipt |

### Legacy Intelligence Mapping

- ImageCritic, SemanticCritic, and VoiceContinuityCritic become category-specific evaluator contracts.
- CBAR gate packs become hard-failure and adversarial evaluation prompts.
- Anti-draft calibration and SDA/SFL failure corpora become fixtures and contrastive evals.
- Active primitive families FBK, SAF, VSG, VOC, IDN, AUD, VOI, ACT, NEG, RIG, MOT, and MSA inform feedback clarity, safety, visual/sonic guidance, voice continuity, identity, audience resonance, acting performance, Negative Space, rig integrity, motion restraint, and micro-semiotic scoring.
- Brand Genesis cannot lock without explicit consent, source media QC, business intelligence, Tribe Soul, Character Lexicon, Voice DNA/Negative Space, visual constitution, identity pack, acting-library plan, PaperCut rig plan, micro-semiotic anchor library, and a Genesis Clearance Certificate.
- The 64-state acting library cannot lock without the complete 8 x 8 emotional-performance matrix, provider receipts, per-cell metadata, QC scores, human review grid, Negative Space update path, and lock receipt.
- The PaperCut rig cannot lock without approved acting library lineage, required avatar assets, layer decomposition, hidden-region repair evidence, canonical rig manifest, editor independence, preview tests, motion constitution, PaperCut style constitution, Ideogram 4 composition JSON structure, micro-semiotic anchor refs, and rig lock receipt.

## 4. Implementation Plan

1. Define `EvaluationCategory`, `EvaluationScore`, `EvidencePointer`, `HardFailure`, `EvaluationReceipt`, and `EvaluationThresholdProfile`.
2. Define `DoctrineEvalDefinition`, `DoctrineEvidenceRequirement`, `PrimitiveEvalObligation`, `DoctrineEvalTargetInput`, and `DoctrineEvalSelection`.
3. Register canonical doctrine evals for Interview Brief / Interview Asset Contract, Brand Genesis / Brand Context, 64-State Acting Library, and PaperCut Rig / 2D Animation.
4. Implement category evaluator adapters with DSPy signatures where reasoning is required and deterministic checks where hashes, dimensions, consent, lineage, manifest coverage, preview tests, or provider receipts are sufficient.
5. Validate that every score and hard failure cites evidence.
6. Persist immutable receipts and link reruns to prior receipts after revision.
7. Emit approval blockers for hard failures and invalid receipts.
8. Expose evaluation receipts to the review read model without granting approval authority to evaluator output.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field


class EvaluationCategory(str, Enum):
    SOURCE_TRUTH = "source_truth"
    DOCTRINE_ALIGNMENT = "doctrine_alignment"
    CCF_ORCHESTRATION_LINEAGE = "ccf_orchestration_lineage"
    PRIMITIVE_REGISTRY_FIDELITY = "primitive_registry_fidelity"
    CONTEXT_PREMISE_INTEGRITY = "context_premise_integrity"
    NARRATIVE_INDUCTION_INTEGRITY = "narrative_induction_integrity"
    ANCHOR_CONTRACT_INTEGRITY = "anchor_contract_integrity"
    BRAND_GENESIS_COMPLETENESS = "brand_genesis_completeness"
    ACTING_LIBRARY_COVERAGE = "acting_library_coverage"
    PAPERCUT_RIG_INTEGRITY = "papercut_rig_integrity"
    MICRO_SEMIOTIC_INTEGRITY = "micro_semiotic_integrity"
    ANIMATION_READINESS = "animation_readiness"
    ASSET_GENERATION_POLICY = "asset_generation_policy"
    ARCHETYPE_FIT = "archetype_fit"
    EXPRESSION_DEPTH = "expression_depth"
    IDENTITY_CONSISTENCY = "identity_consistency"
    LIKENESS = "likeness"
    COMPOSITION = "composition"
    STYLE = "style"
    MOTION_RESTRAINT = "motion_restraint"
    PLATFORM_FIT = "platform_fit"
    NEGATIVE_SPACE = "negative_space"
    MICRO_SEMIOTIC_ANCHORS = "micro_semiotic_anchors"
    ROUTEABILITY = "routeability"
    EVALUATION_TARGET_COVERAGE = "evaluation_target_coverage"
    PUBLISHING_READINESS = "publishing_readiness"


class EvidencePointer(BaseModel):
    source_type: str
    source_id: str
    start_ms: int | None = None
    end_ms: int | None = None
    transcript_segment_id: str | None = None
    claim_scope: Literal["supports", "contradicts", "contextualizes"]
    note: str | None = None


class EvaluationScore(BaseModel):
    category: EvaluationCategory
    score: float = Field(ge=0, le=1)
    threshold: float = Field(ge=0, le=1)
    passed: bool
    evidence: list[EvidencePointer]
    evaluator_version: str


class HardFailure(BaseModel):
    category: EvaluationCategory
    code: str
    message: str
    evidence: list[EvidencePointer]
    approval_blocker_code: str


class EvaluationReceipt(BaseModel):
    schema_version: Literal["cmf.evaluation_receipt.v1"]
    evaluation_receipt_id: str
    object_type: Literal[
        "interview_brief",
        "interview_asset_contract",
        "context_premise",
        "matrix_brief",
        "skill_output",
        "expression_moment",
        "brand_genesis_session",
        "brand_context_version",
        "acting_library",
        "acting_reference",
        "papercut_rig",
        "rig_manifest",
        "animation_plan",
        "render_output",
        "asset_package",
        "scene_output",
    ]
    object_id: str
    previous_receipt_id: str | None = None
    threshold_profile_id: str
    scores: list[EvaluationScore]
    hard_failures: list[HardFailure]
    warnings: list[str]
    decision: Literal["passes_for_human_review", "needs_revision", "blocked"]
    created_at: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `GenerateEvaluationReceiptCommand`, `RunEvaluationCategoryCommand`, `ValidateEvaluationEvidenceCommand`, `RecordEvaluationReceiptCommand`, `BlockApprovalFromEvaluationCommand`, `SupersedeEvaluationReceiptCommand` |
| Events | `EvaluationStarted`, `EvaluationCategoryScored`, `EvaluationEvidenceValidated`, `EvaluationReceiptCreated`, `ApprovalBlockedFromEvaluation`, `EvaluationReceiptSuperseded` |
| Workflow | `EvaluationWorkflow.stage13_generate_receipts` |
| Receipt | `EvaluationReceipt` with object refs, category scores, hard failures, warnings, evaluator versions, evidence pointers, and previous receipt link |

## 6.1 Canonical Doctrine Eval Definitions

| Eval ID | Target objects | Required source doctrine | Blocking evidence routes |
|---|---|---|---|
| `EVL-DOCTRINE-IAC-001` | `interview_brief`, `interview_asset_contract`, `skill_output` | CCP V9, V9.1, Claude deck, Matrix of Edging, CCF/primitive lineage | CRAL/SCRE signal, audience conversation, Context Premise, trigger map, interviewer resonance, Matrix of Edging, primitive registry, First-Line Anchors, Depth Anchor, landing targets, repair followups, route target, hard negative |
| `EVL-DOCTRINE-BGN-001` | `brand_genesis_session`, `brand_context_version`, `skill_output` | Brand Genesis V3, greenfield context, domain contracts, implementation gates, creative pipeline | client intake, consent, source media QC, business intelligence, Tribe Soul, Character Lexicon, Voice DNA/Negative Space, visual constitution, identity pack, acting-library plan, PaperCut rig plan, micro-semiotic library, clearance certificate |
| `EVL-DOCTRINE-ACT-064-001` | `acting_library`, `acting_reference`, `brand_context_version` | Brand Genesis V3, greenfield context, domain contracts, implementation gates, creative pipeline | identity pack, human approval before generation, 64-state matrix, provider receipts, cell metadata, auto-QC scores, human review grid, Negative Space updates, lock receipt |
| `EVL-DOCTRINE-PPR-RIG-001` | `papercut_rig`, `rig_manifest`, `animation_plan` | Brand Genesis V3, creative pipeline, greenfield context, domain contracts, implementation gates | approved acting library, required avatar assets, layer decomposition, hidden-region repair, rig manifest, editor independence, preview tests, motion constitution, PaperCut style constitution, composition JSON, micro-semiotic anchor refs, rig lock receipt |

## 7. Backward Compatibility and Migration Fallback

Legacy evaluator rubrics and gate packs are reference intelligence, fixtures, and eval targets. They cannot approve, publish, or mutate production state. If a legacy rubric cannot be converted with evidence requirements, it remains a reference-only artifact until a migration receipt validates the conversion.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast production vs. truthful review | Evaluation must run before approval and every hard failure must block approval. | Approval policy reads hard failures from immutable receipts. |
| Scores vs. human authority | Scores guide review but cannot approve by themselves. | Approval requires ReviewDecision and ApprovalEvent from Story 9.3. |
| Legacy critic value vs. opaque judgment | Legacy critic logic must cite evidence and evaluator version. | Receipt validation fails when any category lacks evidence. |

## 9. Tasks

- Add evaluation contracts and persistence.
- Implement evaluator category registry and threshold profiles.
- Implement DSPy evaluator adapters and deterministic validators.
- Add evidence validation policy.
- Add immutable receipt writer and rerun supersession.
- Add approval-blocker handoff for hard failures.
- Add review read-model query for receipts.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Required evaluation categories produce receipts for review-ready render/package. | Render enters review with no source truth or identity receipt. |
| AC2 | Category hard-fail blocks approval. | Identity hard-fail still allows approval. |
| AC3 | Source truth evidence opens source artifact, transcript segment, timestamp, route, evaluator version. | Receipt says "source OK" with no source pointer. |
| AC4 | Receipt without evidence is invalid. | Evaluator score is saved with empty evidence. |
| AC5 | Rerun after revision links to prior immutable receipt. | New evaluation overwrites the old one. |

## 11. Dependencies

- TS-CMF-001 command spine.
- TS-CMF-002 pipeline stage records.
- TS-CMF-010 consent blockers.
- TS-CMF-011 Voice-DNA Boost eligibility.
- TS-CMF-037 RenderContract compilation.
- TS-CMF-043 deterministic render output.
- TS-CMF-047 audio, caption, timeline, and mix assembly.

## 12. Testing Strategy


Unit tests:

- Unit tests for evaluation category schema and threshold validation.
- Unit tests for evidence pointer requirements.
- Integration tests from render output to evaluation receipt.
- Hard-failure tests proving approval blocker emission.
- Rerun tests proving old receipts remain immutable.
- Fixture/eval tests against migrated CBAR, anti-draft, and SDA/SFL failure corpora.

Integration tests:

- Workflow test from `render/package ready for review` to `EvaluationReceipt` through pipeline stage `13`.
- Command Bus test proving `evaluation receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for evaluations started, category passes, hard failures, invalid evidence, and reruns.
- Logs include object ID, evaluation receipt ID, threshold profile, evaluator version, category, and blocker code.
- Recovery reruns evaluation after revised object hash changes.
- Rollback does not delete receipts; it supersedes invalid evaluation receipts and blocks dependent approvals until refreshed.

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
| Tech Spec ID | TS-CMF-050 |
| Story | 9.1 |
| Requirement Trace | FR-CMF-09.01 |
| Pipeline Trace | Stage 13, render/package ready for review to EvaluationReceipt |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No model-only approval, no receipt without evidence, no mutable evaluation history |

