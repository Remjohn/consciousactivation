---
tech_spec_id: "TS-CMF-119"
title: "Sequence Eval Gates, Package Sequencing, and Learning"
story_id: "12.6"
story_title: "Sequence Eval and Package Learning"
epic_id: 12
epic_title: "Conscious Sequencing and Expression Acquisition"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP Conscious Sequencing and Expression Acquisition Engine V1 bundle"
pipeline_stage: "11 / 12 / 13"
entry_object: "Frozen ContentSequenceProgram, composition previews, package asset candidates, evaluation receipts, operator revisions, publish telemetry"
exit_object: "SequenceEvaluationReceipt, PackageSequenceProgram, learning recommendations, registry update proposals, approval blockers"
validation_contract: "sequence gates, ethical hard gates, package relationship progression, learning receipts, immutable historical records"
required_receipt: "SequenceEvaluationReceipt"
runtime_target: "Python / Pydantic v2 / eval registry / approval blockers / PWA review / publishing read model"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-119: Sequence Eval Gates, Package Sequencing, and Learning

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for rejection, framing, and pipeline gates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 CBAR mandates for verifiable artifacts and earned package progression. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | Phase 4 adversarial audit trail. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` | Phase 5 adversarial audit trail. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Product owner for FR-CMF-12.06. |
| `THE CMF STUDIO/CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/ccp_conscious_sequence_engine_v1/01_MASTER_SPEC.md` | Sequence evaluation dimensions, package sequencing, and learning loop. |
| `.../02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | `PackageSequenceProgram`, `SequenceEvaluationReceipt`, states, and events. |
| `.../03_RUNTIME_WORKFLOWS.md` | Evaluation, approval, publish, and learning workflow. |
| `.../04_REGISTRIES_AND_FORMAT_ADAPTERS.md` | Sequence Eval Gate Registry. |
| `.../05_EVALUATION_GOVERNANCE_AND_LEARNING.md` | Gate definitions, ethical hard gates, operator commands. |
| `.../models/sequence_engine_models.py` | `PackageAssetRef`, `PackageSequenceProgram`, `SequenceStageScore`, `SequenceEvaluationReceipt`. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-034-guest-asset-pack-spec-generation.md` | Guest Asset Pack dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md` | Standard evaluation receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-053-approval-blockers.md` | Approval blocker dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Doctrine and primitive eval coverage dependency. |

## 2. Overview

This spec evaluates frozen sequence programs, blocks manipulative or ungrounded content, orders multiple assets into package/series programs, and turns performance plus operator revisions into learning recommendations. It is the quality and memory layer for sequencing.

Learning may propose registry updates, threshold adjustments, compiler examples, and package sequencing heuristics. It must not mutate published programs, retroactively change receipts, or silently rewrite doctrine and primitive standards.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-119-001 | `SequenceStageScore` | Per-viewer-state score with dimensions and notes. |
| DEP-CMF-119-002 | `SequenceEvaluationReceipt` | Evaluation receipt for one frozen sequence program. |
| DEP-CMF-119-003 | `PackageAssetRef` | Ordered asset reference in a package sequence. |
| DEP-CMF-119-004 | `PackageSequenceProgram` | Package/series ordering program. |
| DEP-CMF-119-005 | `SequenceLearningSignal` | Evidence-backed learning signal from eval, revision, telemetry, or manual note. |
| DEP-CMF-119-006 | `SequenceRegistryRecommendation` | Draft-only recommendation for registry change. |
| DEP-CMF-119-007 | `PackageSequenceApprovalReceipt` | Receipt for package approval and schedule readiness. |

### Existing Backend Integration

| Python Owner | Database Table(s) | API Route(s) | Migration / Backfill Behavior |
|---|---|---|---|
| `src/ccp_studio/services/sequence_evaluation_service.py` | `sequence_evaluation_receipts`, `sequence_stage_scores` | `POST /api/cmf/sequence-programs/{id}/evaluate` | New tables linked to `content_sequence_programs`. |
| `src/ccp_studio/services/package_sequence_program_service.py` | `package_sequence_programs`, `package_sequence_assets` | `POST /api/cmf/package-sequences`, `POST /api/cmf/package-sequences/{id}/approve` | New package tables; does not mutate Guest Asset Pack specs. |
| `src/ccp_studio/services/sequence_learning_service.py` | `sequence_learning_signals`, `sequence_registry_recommendations` | `POST /api/cmf/sequence-learning/signals`, `POST /api/cmf/sequence-learning/recommendations` | New learning tables; recommendations are draft-only until registry revision approval. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | `receipt_chain`, `evaluation_receipts`, `approval_blockers` | shared receipt writer | Writes eval and package approval receipts. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-FBK-001` | Phase4-M05 | Sequence failures return exact beat, score, and revision command. |
| `EXP-PRG-004` | Phase4-M07 | Package learning and future value must preserve positive long-loop framing. |
| `EXP-SOC-001` | Phase5-M01 | Sequence receipts and package approvals are verifiable artifacts. |
| `EXP-TRG-005` | Phase5-M02 | Package escalation requires earned prior signal, not premature ask. |
| `EXP-PRG-001` | Phase5-M04 | Package and learning actions must remain inline and reviewable. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Sequence eval failures name exact beat, loop, score, and revision command. |
| Phase4-M07: Long Loop Framing Rule | Phase 4 Story 7.1 | `EXP-PRG-004` | Package sequencing preserves future value and does not frame low-performing assets as downgrades. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Evaluation, package approval, and learning recommendations are hash-backed receipt artifacts. |
| Phase5-M02: Earned Escalation Rule | Phase 5 Story 1.2 | `EXP-TRG-005` | Package sequence cannot trigger participation/CTA assets before recognition or trust assets earn it. |
| Phase5-M04: Inline Capture Hook | Phase 5 Story 2.2 | `EXP-PRG-001` | Operator revision and package approval remain inline in review workbench. |

### Receipt Chain Guard

| Receipt | Table | Action | Idempotency Key | Required Hashes |
|---|---|---|---|---|
| `SequenceEvaluationReceipt` | `receipt_chain` | `sequence_evaluation.completed` | `sequence_program_id + sequence_program_sha256` | program hash, eval profile hash, stage score hash |
| `PackageSequenceApprovalReceipt` | `receipt_chain` | `package_sequence.approved` | `package_sequence_program_id + category_promise` | package program hash, asset order hash, score hash |
| `SequenceRegistryRecommendation` | `receipt_chain` | `sequence_learning.recommendation_created` | `recommendation_id + target_registry_id + target_item_id` | learning signal hashes, proposed change hash |

### Sequence Gates

| Gate | What It Checks |
|---|---|
| Perceptual entry | Distinctive, brand-consistent, immediately legible for format. |
| Relevant open question | Clear, audience-relevant, source-supported, specific enough to evaluate. |
| Active prediction | Progressive disclosure narrows understanding without deceptive head fake. |
| Truthful payoff | Loop closes with non-trivial, source-grounded answer. |
| Human affinity | Authentic human cue, Voice DNA, Negative Space, no manufactured vulnerability. |
| Expected future value | Package/series promise is coherent, differentiated, and repeated without monotony. |

### Ethical Hard Gates

Reject sequences that use:

```text
false open loops
fabricated conflict
unclosed promised answers
misleading transcript rearrangement
trauma sensationalization
fabricated urgency
synthetic guest claims
clickbait that violates payoff contract
```

### Package Sequencing Goals

| Goal | Required Behavior |
|---|---|
| Recognition | Repeated signature worldview, visual DNA, and premise continuity without monotony. |
| Trust | Alternates proof, vulnerability, clarity, and useful teaching. |
| Category ownership | Builds a coherent category promise across assets. |
| Participation | Places polls, reactions, comments, and mirror questions at the right moments. |
| Future value | Gives audience reason to expect the next asset without false urgency. |

### Gate Thresholds

| Gate ID | Threshold | Hard Fail | Consequence |
|---|---:|---|---|
| `source_grounding_score` | 1.00 | Yes | Sequence rejected. |
| `loop_closure_score` | 0.95 | Yes | Sequence rejected or must revise. |
| `voice_dna_score` | 0.85 | Yes | Operator revision required. |
| `negative_space_score` | 0.85 | Yes | Operator revision required. |
| `doctrine_alignment_score` | 0.95 | Yes | Sequence rejected. |
| `confusion_penalty` | 0.20 maximum | Yes | Sequence must revise. |
| `manipulation_risk` | 0.10 maximum | Yes | Sequence rejected. |
| `package_relationship_progression` | 0.75 | No | Package needs review. |
| `package_format_diversity` | 0.70 | No | Package needs review. |

### Gate Verdict Semantics

| Verdict | Rule | Receipt Behavior |
|---|---|---|
| `PASS` | All hard sequence gates pass and package soft gates meet threshold. | Write eval/package receipt and allow publish/schedule. |
| `PROVISIONAL` | Only non-hard package gates are below threshold. | Require operator review before schedule. |
| `FAIL` | Repairable sequence or package gate fails. | Write blocker and require revision command. |
| `BLOCKED` | Ethical hard gate, synthetic guest claim, manipulation risk, or source grounding hard gate fails. | Stop publish handoff. |

### Registry Promotion Governance

Learning cannot mutate active registries. Promotion uses this state machine:

```text
learning_signal_recorded
-> recommendation_draft
-> operator_review
-> compatibility_tests_passed
-> registry_revision_receipt_written
-> registry_snapshot_candidate
-> activated_by_TS_CMF_114
```

Rules:

- `SequenceLearningSignal.safe_to_promote` is advisory only.
- `SequenceRegistryRecommendation.status == approved` does not activate behavior.
- Active behavior changes require a new `SequenceRegistrySnapshot` through TS-CMF-114.
- Historical `ContentSequenceProgram`, `SequenceEvaluationReceipt`, and `PackageSequenceProgram` rows are never rewritten by learning.

## 4. Implementation Plan

1. Add `src/ccp_studio/services/sequence_evaluation_service.py`.
2. Add `src/ccp_studio/services/package_sequence_program_service.py`.
3. Add DSPy program `SequenceEvaluator` and deterministic hard-gate validators.
4. Extend the standard `EvaluationReceipt` service with `SequenceEvaluationReceipt` wrappers.
5. Add package compiler that orders approved asset candidates by relationship role, format diversity, category promise, and future value.
6. Add operator commands from bundle governance: `REPLACE_INGREDIENT`, `REORDER_BEATS`, `CHANGE_SEQUENCE_PATTERN`, `CLOSE_LOOP_EARLIER`, `REMOVE_FALSE_TENSION`, `REDUCE_EMOTIONAL_AMPLITUDE`, `CHANGE_AFFINITY_CUE`, `CHANGE_FUTURE_VALUE_SIGNAL`, `REQUEST_PICKUP`, `WAIVE_INGREDIENT_REQUIREMENT`.
7. Add package approval workflow: draft, asset_candidates_bound, diversity_evaluated, schedule_proposed, operator_approved, scheduled, active, completed, learned.
8. Add learning service that stores recommendations without mutating historical receipts.
9. Add PWA package board and sequence eval read model.
10. Add regression tests for ethical hard gates and package learning.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class SequenceLearningSignal(BaseModel):
    schema_version: Literal["cmf.sequence_learning_signal.v1"]
    signal_id: str
    sequence_program_id: str
    package_sequence_program_id: str | None = None
    source: Literal["operator_revision", "eval_failure", "publish_telemetry", "manual_note"]
    signal_type: str
    affected_pattern_id: str | None = None
    affected_format_adapter_id: str | None = None
    recommendation: str
    evidence_refs: list[str]
    safe_to_promote: bool = False


class SequenceRegistryRecommendation(BaseModel):
    schema_version: Literal["cmf.sequence_registry_recommendation.v1"]
    recommendation_id: str
    target_registry_id: str
    target_item_id: str
    proposed_change_type: Literal["threshold", "example", "anti_pattern", "rule", "adapter_mapping"]
    rationale: str
    learning_signal_ids: list[str]
    requires_operator_approval: bool = True
    status: Literal["draft", "approved", "rejected", "implemented"] = "draft"


class PackageSequenceApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.package_sequence_approval_receipt.v1"]
    receipt_id: str
    package_sequence_program_id: str
    brand_context_version_id: str
    package_type: str
    category_promise: str
    asset_refs: list[str]
    relationship_progression_score: float = Field(ge=0, le=1)
    diversity_score: float = Field(ge=0, le=1)
    future_value_score: float = Field(ge=0, le=1)
    blocker_codes: list[str] = Field(default_factory=list)
    operator_status: Literal["approved", "needs_revision", "rejected"]
```

The canonical `SequenceEvaluationReceipt` and `PackageSequenceProgram` must preserve the bundle schema fields and also link to standard CMF `EvaluationReceipt` and approval blocker records.

## 6. Workflow

```text
frozen_content_sequence_program
-> auto_eval_sequence_gates
-> ethical_hard_gate_check
-> operator_review
-> revise_or_approve
-> bind_asset_to_package_candidate
-> compile_package_sequence_program
-> evaluate_package_progression
-> operator_approve_schedule
-> publish
-> learn_from_receipts_and_telemetry
-> propose_registry_recommendations
```

Package state:

```text
draft
-> asset_candidates_bound
-> diversity_evaluated
-> schedule_proposed
-> operator_approved
-> scheduled
-> active
-> completed
-> learned
```

## 7. API, Service, and Event Contracts

| Contract | Shape |
|---|---|
| `POST /api/cmf/sequence-programs/{id}/evaluate` | Emits `SequenceEvaluationReceipt`. |
| `POST /api/cmf/sequence-programs/{id}/revision-command` | Applies typed sequence revision command. |
| `POST /api/cmf/package-sequences` | Creates package sequence program from approved asset candidates. |
| `POST /api/cmf/package-sequences/{id}/evaluate` | Runs relationship progression and diversity evals. |
| `POST /api/cmf/package-sequences/{id}/approve` | Operator approves schedule proposal. |
| `POST /api/cmf/sequence-learning/signals` | Records learning signal. |
| `POST /api/cmf/sequence-learning/recommendations` | Creates registry recommendation draft. |

Events:

```text
SequenceEvaluationCompleted
SequenceApprovalBlocked
SequenceRevisionCommandApplied
PackageSequenceProgramCompiled
PackageSequenceScheduled
PackageSequenceCompleted
SequenceLearningSignalRecorded
SequenceRegistryRecommendationCreated
```

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate / Test Evidence |
|---|---|---|---|
| AC1 | Every frozen sequence program receives `SequenceEvaluationReceipt` before render or publish approval. | A video renders from a frozen program with no sequence eval receipt. | Phase5-M01, `EXP-SOC-001`; publish gate test. |
| AC2 | Ethical hard gate failures block publish and require revision or rejection. | A sequence uses fabricated conflict for a stronger hook and still publishes. | Phase4-M05, `EXP-FBK-001`; ethical hard gate test. |
| AC3 | Package sequencing evaluates relationship progression, format diversity, category promise, participation, and future value. | A package repeats five high-energy polls without proof, trust, or future-value progression. | Phase4-M07, `EXP-PRG-004`; package progression test. |
| AC4 | Operator commands create a new program version or explicit waiver receipt. | Operator reorders beats in place and the original receipt remains unchanged. | Phase5-M01, `EXP-SOC-001`; revision immutability test. |
| AC5 | Learning signals cannot mutate published programs, historical receipts, or active registries. | A publish telemetry win automatically changes the active sequence pattern registry. | Phase5-M01, `EXP-SOC-001`; registry governance test. |
| AC6 | Package CTA or participation assets require earned recognition or trust signals earlier in the package. | The first package asset asks viewers to participate before any context or payoff. | Phase5-M02, `EXP-TRG-005`; earned escalation test. |
| AC7 | PWA review shows sequence scores, hard failures, package order, asset roles, and next required action. | Operator sees only an overall score and cannot identify the failing beat. | Phase4-M05, `EXP-FBK-001`; review read-model test. |

## 9. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Eval gate tests | All six sequence gates and ethical hard gates pass/fail deterministically. |
| Receipt tests | Sequence receipt links to program hash and standard EvaluationReceipt. |
| Revision tests | Each operator command creates a new version or waiver receipt. |
| Package tests | Asset order, diversity requirements, and category promise are validated. |
| Learning tests | Learning recommendations cannot auto-activate. |
| Negative tests | False loops, fabricated conflict, and synthetic guest claims block publish. |

## 10. Doctrine-Driven Test Harness Binding

The harness must evaluate:

```text
sequence_loop_closure
source_grounding
voice_dna
negative_space
doctrine_alignment
confusion_penalty
manipulation_risk
package_relationship_progression
future_value_continuity
```

Hard failures create approval blockers and stop publish handoff.

## Spec Audit Receipt

| Check | Status |
|---|---|
| Uses standard evaluation and approval blocker architecture | Pass |
| Makes package-level future value explicit | Pass |
| Blocks manipulative sequence patterns and false payoff | Pass |
| Allows learning without mutating immutable history | Pass |
| Closes the sequencing loop from program to publish to registry recommendation | Pass |
