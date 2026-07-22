---
tech_spec_id: "TS-CMF-015"
title: "JIT Skill Compiler Saturation and Contrast"
story_id: "3.3"
story_title: "JIT Skill Compiler Saturation and Contrast"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-3-3-jit-skill-compiler-saturation-and-contrast.md"
fr_ids:
  - "FR-CMF-03.04"
  - "FR-CMF-03.05"
pipeline_stage: "3 / 4 / 6 / 7"
entry_object: "saturation context"
exit_object: "SkillInvocationRecord and proposals"
validation_contract: "grounded context and anti-draft gate"
required_receipt: "skill invocation receipt"
runtime_target: "Python / Pydantic v2 / DSPy / JIT skill compilers / eval receipts"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-015: JIT Skill Compiler Saturation and Contrast

**Status:** Ready for Development  
**Story:** `3.3 - JIT Skill Compiler Saturation and Contrast`  
**Implementation Boundary:** JIT skill compiler contracts, saturation context bundles, contrastive prompt layers, anti-draft calibration, evidence refs, evaluation scores, and skill invocation receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for JIT skill compilers, two-level extraction, narrative induction, contrastive prompting, and anti-draft layers. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-03.04 and FR-CMF-03.05 source authority. |
| `docs/architecture.md` | Architecture authority for DSPy program registry, JIT compiler rule, saturation context, and SkillInvocationRecord. |
| `docs/cmf-studio-pipeline-map.md` | Stages 3, 4, 6, and 7 trace for research, induction, extraction, and routing. |
| `docs/migration/legacy-inventory.md` | Legacy skill modules, anti-draft calibrator, Voice DNA, and narrative intelligence as read-only source. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Narrative State Induction, Three-Context Engine, First-Line Anchors, Depth Anchors, and Interview Asset Contract doctrine. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Every question as Interview Asset Contract, asset derivatives, route targets, landing eval targets, and repair followups. |
| `docs/stories/story-3-3-jit-skill-compiler-saturation-and-contrast.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-014-registry-conversion-fixtures-and-evals.md` | Registry, fixture, and eval dependency. |

## 2. Overview

### Problem Statement

Generic few-shot prompting cannot preserve CMF's narrative induction and expression extraction depth. The system needs migrated JIT skill compilers that operate on saturation context: source docs, transcript segments, guest dossier, audience reality, brand context, primitive candidates, prior evaluations, and failure corpora. Without required context and contrast, compiler outputs can become generic scripts that incorrectly influence extraction or routing.

### Solution

Implement JIT skill compilers as DSPy-backed, Pydantic-typed programs that receive a `SaturationContextBundle`, produce proposals plus contrast candidates, run anti-draft calibration, cite evidence, and write `SkillInvocationRecord`. A compiler output cannot influence extraction, induction, routing, or evaluation unless it passes grounded context and anti-draft gates.

### Scope

In scope:

- `JITSkillCompiler`, `DSPyProgramSpec`, `SaturationContextBundle`, `ContrastivePromptLayer`, `CompilerCandidateSet`, `AntiDraftCalibrationReport`, and `SkillInvocationRecord`.
- `ConsciousInterviewBriefSkillOutput` and Interview Asset Contract candidates that rebuild CCF signal intelligence through Guest Truth, Interviewer Resonance, Audience Reality, Context Premise, Matrix pressure, expression-state induction, anchors, repair followups, landing evaluation, and route targets.
- Live guest extraction support vs transcript/source extraction classification.
- Evidence refs, input hashes, DSPy program version, output schema, eval score, reviewer state.
- Blocking ungrounded outputs from influencing routing or extraction.

Out of scope:

- Specific extractor internals for each future route.
- UI prompt editing.
- Legacy runtime coupling prompt runtime.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-03.04 | Operators and agents use migrated JIT skill compilers for extraction, drafting, contrast, anti-draft, Voice DNA, induction, routing, and evaluation. | Typed `JITSkillCompiler`, DSPy program specs, compiler registry, candidate sets, calibration reports, and invocation receipts. |
| FR-CMF-03.05 | JIT compilers operate on grounded saturation context. | `SaturationContextBundle`, required context validation, evidence refs, input hashes, anti-draft gate, and rejection of uncited outputs. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `3 - Research and context engineering`; `4 - Interview intelligence`; `6 - Post-session extraction`; `7 - Routing and package planning` |
| Entry Object | Saturation context |
| Exit Object | `SkillInvocationRecord` and proposals |
| Allowed Actors / Services | Operator, Pi Orchestrator, DSPy Program Registry, JITSkillCompilerService, EvaluationService |
| Validation Contract | Grounded context and anti-draft gate |
| Required Receipt | Skill invocation receipt |
| Forbidden Shortcut | Compiler output without evidence refs, generic few-shot script, hidden prompt stack, compiler mutating canonical state |

### Legacy Intelligence Mapping

Legacy skill modules, anti-draft calibrator, narrative intelligence, RSCS saturation/collision/compression/evaluation, CBAR, Voice DNA, and primitive systems become typed compilers, fixtures, and evals. DSPy owns reasoning. Canonical state mutation remains Command Bus only.

Target modules:

- `ccp_studio.contracts.skills`
- `ccp_studio.contracts.dspy_programs`
- `ccp_studio.services.jit_skill_compiler_service`
- `ccp_studio.dspy_programs.jit_skill_compilers`
- `ccp_studio.dspy_programs.anti_draft_calibration_program`
- `ccp_studio.repositories.skill_invocation_records`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `SaturationContextBundle` | Source docs, transcript segments, guest dossier, audience reality, Context Premise, Audience Deep Trigger Map, Interviewer Resonance Context, Matrix brief, CRAL findings, audience conversations, brand context, primitive candidates, prior evaluations, failure corpus. |
| `JITSkillCompiler` | Typed compiler definition and allowed use cases. |
| `DSPyProgramSpec` | DSPy signature, input model, output model, optimizer artifact, eval threshold, and version. |
| `ContrastivePromptLayer` | Contrast generation and anti-centroid pressure. |
| `AntiDraftCalibrationReport` | Detects generic, uncited, or style-drift outputs. |
| `SkillInvocationRecord` | Records invocation evidence, versions, scores, and reviewer state. |

## 4. Implementation Plan

### Workstream A: Contracts

Define skill compiler, saturation bundle, compiler candidate, contrast layer, calibration report, and invocation record contracts.

### Workstream B: Required Context Validation

Require context fields based on compiler type and stage. Extraction compilers require transcript/source refs. Induction compilers require guest/audience context and live support classification.

### Workstream C: DSPy Program Registry

Register compilers as DSPy program specs with Pydantic input/output models, fixture sets, eval thresholds, and versioned optimizer artifacts where applicable.

### Workstream D: Anti-Draft and Contrast

Every candidate set includes contrast candidates, anti-draft calibration, evidence refs, and confidence. Uncited candidates cannot influence downstream routing or extraction.

### Workstream E: Receipts and State Boundary

Write `SkillInvocationRecord`; do not let DSPy compilers mutate canonical objects directly.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SkillUseMode(str, Enum):
    live_guest_induction = "live_guest_induction"
    conscious_interview_brief = "conscious_interview_brief"
    interview_engineering = "interview_engineering"
    narrative_induction = "narrative_induction"
    transcript_extraction = "transcript_extraction"
    source_expression_contrast = "source_expression_contrast"
    routing_support = "routing_support"
    evaluation_support = "evaluation_support"
    voice_dna_support = "voice_dna_support"
    scene_prompt_support_after_route = "scene_prompt_support_after_route"


class SaturationContextBundle(BaseModel):
    schema_version: Literal["cmf.saturation_context_bundle.v1"]
    source_doc_refs: list[str] = Field(default_factory=list)
    transcript_segment_refs: list[str] = Field(default_factory=list)
    guest_dossier_id: UUID | None = None
    audience_reality_brief_id: UUID | None = None
    context_premise_id: UUID | None = None
    audience_deep_trigger_map_id: UUID | None = None
    interviewer_resonance_context_id: UUID | None = None
    matrix_brief_id: UUID | None = None
    brand_context_version_id: UUID | None = None
    cral_finding_refs: list[str] = Field(default_factory=list)
    audience_conversation_refs: list[str] = Field(default_factory=list)
    primitive_candidate_ids: list[UUID] = Field(default_factory=list)
    invariant_field_refs: list[str] = Field(default_factory=list)
    coalition_signature_refs: list[str] = Field(default_factory=list)
    edge_product_refs: list[str] = Field(default_factory=list)
    ccf_orchestration_refs: list[str] = Field(default_factory=list)
    prior_evaluation_receipt_ids: list[UUID] = Field(default_factory=list)
    failure_corpus_refs: list[str] = Field(default_factory=list)


class ConsciousInterviewBriefQuestion(BaseModel):
    schema_version: Literal["cmf.conscious_interview_brief_question.v1"]
    question_id: UUID
    main_question: str
    source_pressure_refs: list[str]
    context_premise_ref: UUID
    matrix_brief_ref: UUID
    interviewer_resonance_context_ref: UUID
    primitive_candidate_ids: list[UUID]
    invariant_refs: list[str] = Field(default_factory=list)
    target_expression_states: list[str]
    route_target: dict[str, Any]
    edge_product_refs: list[str] = Field(default_factory=list)
    first_line_anchors: dict[str, str]
    depth_anchor: str
    expected_source_material: list[str]
    clip_start_rule: Literal["start_at_selected_first_line_anchor"]
    depth_eval_rule: Literal["answer_must_contain_specific_cost_or_tension"]
    landing_eval_targets: list[str]
    repair_followups: dict[str, str]
    intended_guest_reaction: str
    intended_extraction_outcome: str
    anti_centroid_check: str


class ConsciousInterviewBriefSkillOutput(BaseModel):
    schema_version: Literal["cmf.conscious_interview_brief_skill_output.v1"]
    interview_brief_skill_output_id: UUID
    question_contracts: list[ConsciousInterviewBriefQuestion]
    ccf_reverse_engineering_chain: list[str]
    required_skill_invocation_receipt_id: UUID | None = None


class DSPyProgramSpec(BaseModel):
    schema_version: Literal["cmf.dspy_program_spec.v1"]
    dspy_program_spec_id: UUID
    program_key: str
    input_model: str
    output_model: str
    version: str
    fixture_set_ids: list[UUID]
    evaluation_target_ids: list[UUID]
    eval_threshold: float | None = None


class SkillInvocationRecord(BaseModel):
    schema_version: Literal["cmf.skill_invocation_record.v1"]
    skill_invocation_id: UUID
    skill_key: str
    use_mode: SkillUseMode
    dspy_program_spec_id: UUID
    registry_snapshot_id: UUID
    input_hashes: list[str]
    output_schema: str
    evidence_refs: list[str]
    eval_score: float | None = None
    reviewer_state: str | None = None
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `InvokeJITSkillCompilerCommand`, `ValidateSaturationContextCommand`, `RecordContrastiveLayerCommand`, `RunAntiDraftCalibrationCommand`, `WriteSkillInvocationReceiptCommand` |
| Events | `JITSkillCompilerInvoked`, `SaturationContextValidated`, `AntiDraftCalibrationCompleted`, `SkillOutputRejected`, `SkillInvocationRecorded` |
| Workflows | JIT skill invocation workflow, anti-draft calibration workflow, reviewer escalation workflow |
| Receipts | `SkillInvocationReceipt`, `EvaluationReceipt`, `FailureReceipt`, `HumanHandoffRequest` |

## 7. Backward Compatibility and Migration Fallback

Legacy prompt modules cannot run as hidden prompts. If they are not migrated into a compiler spec with fixtures and evals, they remain source doctrine. Uncited outputs are rejected.

Fallback behavior:

- Missing context returns `SATURATION_CONTEXT_INCOMPLETE`.
- Conscious interview brief mode requires CRAL refs, audience conversation refs, Context Premise, Audience Deep Trigger Map, Matrix brief, primitive candidates, CCF orchestration refs, prior eval receipts, and hard negatives.
- Missing evidence refs returns `SKILL_OUTPUT_UNGROUNDED`.
- Missing eval target returns `SKILL_EVAL_TARGET_REQUIRED`.
- `scene_prompt_support_after_route` without approved `ExpressionMoment`, route receipt, and `CompleteEditingSession` returns `SCENE_PROMPT_SUPPORT_PRE_ROUTE_BLOCKED`.
- Anti-draft failure returns `ANTI_DRAFT_GATE_FAILED`.
- Direct state mutation attempt returns `SKILL_STATE_MUTATION_FORBIDDEN`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Fast generation wants lightweight prompts; CMF intelligence requires saturated, contrastive, evidence-backed compiler outputs. |
| UX / Ops Failure Scenario | A generic draft or interview question influences routing because it sounds plausible but cites no CRAL signal, audience conversation, Context Premise, Matrix pressure, primitive, or failure-context evidence. |
| Resolution Demand | Saturation context and anti-draft gates take precedence. Compiler outputs cannot influence production unless grounded, contrasted, evaluated, and receipted. |
| Downstream Proof | Tests must prove missing context rejects output, live induction differs from transcript extraction, and invocation records include versions, hashes, eval scores, and evidence. |

## 9. Tasks

- Define JIT skill contracts.
- Implement saturation context validation.
- Implement DSPy program spec registry hooks.
- Implement contrast and anti-draft report contracts.
- Implement skill invocation workflow.
- Add rejection path for ungrounded outputs.
- Add tests and eval fixtures.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Compiler input includes relevant source docs, transcript, guest, audience, brand, primitives, eval history, and failure corpus. | Compiler runs on a one-line prompt. |
| AC2 | Results include contrast candidates, anti-draft calibration, evidence refs, and confidence. | Output contains only a polished final paragraph. |
| AC3 | Output without saturation citations cannot influence routing or extraction. | Route candidate is accepted with no source refs. |
| AC4 | Narrative induction guidance distinguishes live guest support from transcript/source extraction. | Live interview prompt is reused as transcript extractor. |
| AC5 | Stored receipt includes DSPy version, input hashes, output schema, eval score, and reviewer state when required. | Invocation saved with no program version. |
| AC6 | `interview_engineering`, `narrative_induction`, and `source_expression_contrast` are first-class use modes with saturation checks, not aliases to generic script writing. | Interview brief generation is implemented as a hidden few-shot social script prompt. |
| AC7 | `scene_prompt_support_after_route` requires an approved `ExpressionMoment`, route receipt, and `CompleteEditingSession`. | Scene prompt generation runs from research notes before route approval. |

## 11. Dependencies

Internal:

- TS-CMF-002 Orchestration records
- TS-CMF-014 Registry conversion
- TS-CMF-016 Greenfield gates
- Source/consent specs from Epic 2

External:

- Pydantic v2
- DSPy
- PostgreSQL
- Evaluation runner

## 12. Testing Strategy

Unit tests:

- Required saturation fields by skill mode.
- Explicit use-mode validation for `interview_engineering`, `narrative_induction`, `source_expression_contrast`, and `scene_prompt_support_after_route`.
- Anti-draft report validation.
- Skill invocation record schema.
- DSPy program spec validation.

Integration tests:

- Invoke extraction skill with complete context.
- Reject missing transcript evidence.
- Run anti-draft calibration failure.
- Store invocation receipt with hashes and score.
- Verify compiler cannot mutate canonical state.
- Reject `scene_prompt_support_after_route` when approved expression, route receipt, or complete editing session proof is missing.

Safety tests:

- Hidden prompt stack blocked.
- Unapproved skill cannot run.
- JIT compiler output cannot bypass reviewer state where required.

## 13. Observability, Recovery, and Rollback

- Logs include `skill_invocation_id`, `skill_key`, `program_version`, `registry_snapshot_id`, `eval_score`, and rejected reason.
- Metrics track invocations, anti-draft failures, ungrounded outputs, reviewer escalations, and eval threshold failures.
- Recovery can rerun compiler from saved input hashes and registry snapshot.
- Rollback deactivates compiler version and preserves invocation records.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-03.04, FR-CMF-03.05 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Skill modules and anti-draft systems mapped to DSPy/Pydantic compiler contracts |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | DSPy reasoning with Python contracts and Pi handoff receipts |
| TypeScript Boundary | No prompt or compiler authority in UI |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

