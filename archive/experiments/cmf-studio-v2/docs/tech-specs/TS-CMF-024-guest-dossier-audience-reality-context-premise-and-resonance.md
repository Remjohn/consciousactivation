---
tech_spec_id: "TS-CMF-024"
title: "Guest Dossier, Audience Reality, Context Premise, and Resonance"
story_id: "5.2"
story_title: "Guest Dossier, Audience Reality, Context Premise, and Resonance"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-5-2-guest-dossier-audience-reality-context-premise-and-resonance.md"
fr_ids:
  - "FR-CMF-05.02"
pipeline_stage: "3"
entry_object: "approved research"
exit_object: "dossier, audience brief, Context Premise"
validation_contract: "evidence and inference validation"
required_receipt: "context compilation receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-024: Guest Dossier, Audience Reality, Context Premise, and Resonance

**Status:** Ready for Development  
**Story:** `5.2 - Guest Dossier, Audience Reality, Context Premise, and Resonance`  
**Implementation Boundary:** DSPy compilers and typed records for guest truth, audience reality, context premise, audience trigger structure, and interviewer resonance.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-5-2-guest-dossier-audience-reality-context-premise-and-resonance.md` | Story source, acceptance criteria, pipeline trace, and handoff requirements. |
| `docs/epics.md` | Epic 5 FR and story sequencing. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-05.02 authority and anti-pattern prevention. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Dual extraction, Context Premise, Emotional DNA, Voice DNA, and interview-first product doctrine. |
| `docs/architecture.md` | Stage 3 objects and DSPy compiler list. |
| `docs/cmf-studio-pipeline-map.md` | Research and context engineering workflow. |
| `docs/migration/legacy-inventory.md` | Narrative intelligence, archetype prompts, cognitive primitives, and Voice DNA references. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Narrative State Induction definition and source context. |
| `THE CMF STUDIO/Matrix of Edging.md` | Research field to pressure selection doctrine. |

## 2. Overview

Implement the context compilation layer that turns approved evidence into `GuestDossier`, `AudienceRealityBrief`, `ContextPremise`, `AudienceDeepTriggerMap`, and `InterviewerResonanceContext`. These objects establish the guest truth, audience pressure field, and Operator resonance before Matrix of Edging and Interview Asset Contract compilation.

The system must separate sourced facts from inferences. Context Premise must not collapse into a generic persona summary; it must preserve trigger depth, hermeneutical gaps, moral-emotional vectors, coping trajectory, and audience/guest or audience/coach matching logic when evidence supports it.

For CMF Studio, Context Premise is also the bridge between audience conversations and interview question design. It should register recurring comments, objections, search questions, social debates, comment-section language, and lived audience friction as evidence-backed pressure. If it does not change what the Interview Brief asks, it is not operationally useful.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-05.02 | The system can compile Guest Dossiers, Audience Reality Briefs, Context Premises, and Interviewer Resonance Contexts for a planned session. | DSPy compilers, typed output objects, evidence/inference validation, context receipt, and review gates. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 3 - Research and context engineering |
| Entry Object | approved research |
| Exit Object | dossier, audience brief, Context Premise |
| Validation Contract | evidence and inference validation |
| Required Receipt | context compilation receipt |

### Legacy Intelligence Mapping

- V9 defines research, interviewer resonance, audience reality, and Matrix of Edging as Narrative State Induction inputs.
- Legacy archetype prompts and narrative intelligence inform compiler fixtures and evaluation examples.
- Context Premise and Audience Deep Trigger Map are typed greenfield objects, not persona blurbs.
- Voice/Emotional DNA references inform resonance fields when source evidence exists.

## 4. Implementation Plan

1. Add contracts for `GuestDossier`, `AudienceRealityBrief`, `ContextPremise`, `AudienceDeepTriggerMap`, and `InterviewerResonanceContext`.
2. Add DSPy programs: `GuestDossierCompiler`, `AudienceRealityBriefCompiler`, `ContextPremiseCompiler`, `AudienceDeepTriggerMapCompiler`, and `InterviewerResonanceCompiler`.
3. Implement compiler input packet containing approved evidence IDs, research receipt IDs, guest profile hints, audience scope, brand context, and operator notes.
4. Add evidence/inference validation that rejects unsupported claims, overconfident psychology, and persona-summary collapse.
5. Persist compiler outputs with source hashes, confidence, reviewer state, and context compilation receipt.
6. Expose review endpoints in `/api/v1/interviews/preparation`.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ContextOutputStatus(str, Enum):
    DRAFT = "draft"
    EVIDENCE_REVIEW_REQUIRED = "evidence_review_required"
    APPROVED = "approved"
    REJECTED = "rejected"


class EvidenceBackedInference(BaseModel):
    inference_id: str
    statement: str
    evidence_ids: list[str] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    limitation: str | None = None


class GuestDossier(BaseModel):
    guest_dossier_id: str
    brand_id: str
    guest_id: str
    research_field_id: str
    identity_facts: list[EvidenceBackedInference]
    narrative_history: list[EvidenceBackedInference]
    likely_expression_constraints: list[EvidenceBackedInference]
    research_gaps: list[str]
    status: ContextOutputStatus


class AudienceDeepTriggerMap(BaseModel):
    trigger_map_id: str
    depth_mode: str
    hermeneutical_gaps: list[EvidenceBackedInference]
    moral_emotional_vectors: list[EvidenceBackedInference]
    coping_trajectory: list[EvidenceBackedInference]
    audience_guest_matches: list[EvidenceBackedInference]


class ContextPremise(BaseModel):
    context_premise_id: str
    audience_reality_brief_id: str
    trigger_map_id: str
    premise: str
    question_implications: list[str]
    audience_conversation_refs: list[str] = []
    trigger_match_summary: str | None = None
    unsupported_inference_flags: list[str] = []
    status: ContextOutputStatus


class InterviewerResonanceContext(BaseModel):
    resonance_context_id: str
    operator_id: str
    authentic_curiosity: list[str]
    emotional_bridges: list[str]
    questions_to_avoid: list[str]
    opening_state: str
    evidence_ids: list[str]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileGuestDossierCommand`, `CompileAudienceRealityBriefCommand`, `CompileContextPremiseCommand`, `CompileInterviewerResonanceCommand`, `ApproveContextArtifactCommand`, `RejectUnsupportedContextInferenceCommand` |
| Events | `GuestDossierCompiled`, `AudienceRealityBriefCompiled`, `ContextPremiseCompiled`, `InterviewerResonanceCompiled`, `ContextArtifactApproved`, `ContextInferenceRejected` |
| Workflow | `InterviewPreparationWorkflow.stage3_compile_context` |
| Receipt | `ContextCompilationReceipt` with compiler version, input evidence IDs, source hashes, output IDs, evaluator results, and reviewer state |

DSPy predictions must be validated into Pydantic objects before persistence. Rejected inferences remain visible for audit but cannot feed Matrix or contract compilation.

## 7. Backward Compatibility and Migration Fallback

Legacy prompts and research files are used as fixture and evaluation material only. If a legacy archetype prompt suggests a context structure, the system stores the migrated structure in a typed registry or DSPy program spec before use.

If evidence is insufficient for full-depth Context Premise, compile a shallow context with explicit gaps rather than inventing psychological certainty.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Deep context vs. overconfident inference | Every inference carries evidence IDs, confidence, and limitations. | Interview plan review shows source links and unsupported-inference flags. |
| Audience reality vs. persona flattening | Context Premise stores trigger structure and audience/guest match logic. | Matrix compiler consumes trigger map fields, not generic persona text. |
| Audience conversation vs. abstract research | Audience comments, objections, social debates, and search questions must feed question implications. | Conscious Interview Brief Skill cannot compile questions without audience conversation refs. |
| Operator resonance vs. scripted interview | Resonance context gives authentic bridges and avoid-lists without replacing Operator judgment. | Pre-induction uses resonance as guidance with edit trail. |

## 9. Tasks

- Add Pydantic/SQLAlchemy models for guest dossier, audience reality, trigger map, context premise, and resonance context.
- Implement DSPy compiler modules and registry metadata.
- Add evidence/inference evaluator with source ID, confidence, and limitation checks.
- Add review commands for approving/rejecting artifacts.
- Add API read models for Interview Intelligence Studio.
- Add tests and fixtures using legacy V9/Matrix/CRAL examples.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Compilers produce typed artifacts with source references and confidence. | A Guest Dossier contains unsourced identity claims. |
| AC2 | Context Premise connects guest truth to audience reality. | Context Premise is a generic audience persona paragraph. |
| AC3 | Resonance context includes curiosity, bridges, avoid-list, and opening state. | Pre-induction opens with only generated questions. |
| AC4 | Unsupported inference is flagged for revision. | Psychological claim is approved without evidence. |
| AC5 | Approved artifact IDs become saturation context for contracts. | Interview Asset Contract compiler lacks context artifact refs. |

## 11. Dependencies

- TS-CMF-023 approved ResearchField and ResearchEvidence.
- TS-CMF-013 through TS-CMF-017 legacy inventory and orchestration migration.
- TS-CMF-004 brand workspace and scope.
- TS-CMF-005 operator permissions.
- TS-CMF-002 stage execution records.

## 12. Testing Strategy


Unit tests:

- Unit tests for inference evidence requirements and confidence bounds.
- DSPy contract tests proving predictions validate into Pydantic models.
- Evaluation tests for persona collapse, unsupported psychology, and missing limitations.
- Workflow tests proving approved output IDs feed Matrix and contract compilers.
- Security tests for brand-scoped evidence and context objects.
- Golden fixture tests from V9/Matrix material.

Integration tests:

- Workflow test from `approved research` to `dossier, audience brief, Context Premise` through pipeline stage `3`.
- Command Bus test proving `context compilation receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Log compiler version, input hash, output hash, evaluator result, and review decision.
- Metrics for unsupported-inference failures, context approval latency, shallow-mode outputs, and rejected persona summaries.
- Recovery: revise context artifact by creating a new version linked to the same evidence packet.
- Rollback: supersede approved artifact and invalidate dependent draft Matrix briefs and contract outputs.

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
| Tech Spec ID | TS-CMF-024 |
| Story | 5.2 |
| Requirement Trace | FR-CMF-05.02 |
| Pipeline Trace | Stage 3, approved research to dossier/audience/context artifacts |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No newsletters, no persona collapse, no unsupported psychological certainty, no legacy runtime coupling |

