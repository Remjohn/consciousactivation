---
tech_spec_id: "TS-CMF-028"
title: "CRAL, Context Premise, Emotional DNA, and Root-Down Induction"
story_id: "5.6"
story_title: "CRAL, Context Premise, Emotional DNA, and Root-Down Induction"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-5-6-cral-context-premise-emotional-dna-and-root-down-induction.md"
fr_ids:
  - "FR-CMF-05.08"
pipeline_stage: "3 / 4"
entry_object: "CRAL/context/DNA evidence"
exit_object: "InductionRationale"
validation_contract: "supported psychology and root-down evidence"
required_receipt: "induction rationale receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-028: CRAL, Context Premise, Emotional DNA, and Root-Down Induction

**Status:** Ready for Development  
**Story:** `5.6 - CRAL, Context Premise, Emotional DNA, and Root-Down Induction`  
**Implementation Boundary:** CRAL findings, Audience Deep Trigger Map, Emotional DNA, Voice DNA, root-down rationale, unsupported psychology gate, and induction rationale receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-5-6-cral-context-premise-emotional-dna-and-root-down-induction.md` | Story source and acceptance criteria. |
| `docs/epics.md` | Epic 5 FR-CMF-05.08 coverage and prerequisites. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-05.08 authority and anti-pattern rules. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | CRAL/SCRE, Context Premise, Emotional DNA, Voice DNA, and root-down doctrine. |
| `docs/architecture.md` | CRAL rule, root-down expression rule, and core object list. |
| `docs/cmf-studio-pipeline-map.md` | Stage 3/4 research and interview-intelligence trace. |
| `docs/migration/legacy-inventory.md` | CRAL engines, identity architecture, Voice DNA services, anti-draft calibrator, and primitive inventory. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Narrative State Induction definition and anti-centroid source. |
| `THE CMF STUDIO/Matrix of Edging.md` | Matrix pressure selection and candidate survival doctrine. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Evaluation and anti-genericity laws. |

## 2. Overview

Implement the rationale layer that explains why each interview move exists before source capture. `InductionRationale` must connect CRAL/SCRE signals, Context Premise, Audience Deep Trigger Map, Emotional DNA, Voice DNA, Matrix position, target expression state, and intended asset extraction outcome.

The root-down rule is non-negotiable: Emotional DNA is the root system for Voice DNA. The system must distinguish what the guest believes, how they construct expression, and the emotional path through which activation becomes language. If evidence is insufficient, the rationale must be partial and low-certainty, never falsely authoritative.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-05.08 | Use CRAL/SCRE research, Context Premise, Audience Deep Trigger Map, Emotional DNA, Voice DNA, and root-down induction logic to explain why each interview move is made before source capture. | CRAL findings, DNA profiles, induction rationale schema, evidence support gate, explanation UI, and rationale receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 3 / 4 - Research and interview intelligence |
| Entry Object | CRAL/context/DNA evidence |
| Exit Object | `InductionRationale` |
| Validation Contract | supported psychology and root-down evidence |
| Required Receipt | induction rationale receipt |

### Legacy Intelligence Mapping

- CRAL/SCRE seven JIT moments: Relevant, Believable, Undeniable, Resonant, Surprising, Irrefutable, Relatable.
- Context Premise stores trigger depth, hermeneutical gap, moral-emotional vector, coping trajectory, and match logic.
- Emotional DNA and Voice DNA legacy assets inform contracts and fixtures but must become typed greenfield objects.
- Anti-draft calibrator and Voice DNA services inform evaluation of generic voice imitation and negative-space drift.

## 4. Implementation Plan

1. Add or extend contracts for `CRALFinding`, `AudienceDeepTriggerMap`, `EmotionalDNAProfile`, `VoiceDNAProfile`, `InductionRationale`, and `InductionRationaleReceipt`.
2. Implement DSPy programs: `CRALResearchCompiler`, `AudienceDeepTriggerMapCompiler`, `EmotionalDNAExtractor`, `VoiceDNAProfileCompiler`, and `InductionRationaleCompiler`.
3. Add supported-psychology validator that requires evidence IDs, source role, confidence, limitation, and rationale mode for every claim.
4. Add partial-mode behavior for insufficient CRAL, Context Premise, Emotional DNA, or Voice DNA evidence.
5. Attach rationale IDs to pre-induction questions and Interview Asset Contracts.
6. Expose rationale inspection in Interview Intelligence Studio.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class CRALMoment(str, Enum):
    RELEVANT = "relevant"
    BELIEVABLE = "believable"
    UNDENIABLE = "undeniable"
    RESONANT = "resonant"
    SURPRISING = "surprising"
    IRREFUTABLE = "irrefutable"
    RELATABLE = "relatable"


class RationaleMode(str, Enum):
    FULL_DEPTH = "full_depth"
    PARTIAL = "partial"
    SHALLOW_SUPPORTED = "shallow_supported"
    BLOCKED_UNSUPPORTED = "blocked_unsupported"


class CRALFinding(BaseModel):
    cral_finding_id: str
    moment: CRALMoment
    signal: str
    evidence_ids: list[str] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    contradiction_notes: list[str] = []


class EmotionalDNAProfile(BaseModel):
    emotional_dna_profile_id: str
    guest_id: str
    belief_content: list[str]
    emotional_path: list[str]
    suppression_markers: list[str]
    escalation_triggers: list[str]
    evidence_ids: list[str]
    limitation: str | None = None


class VoiceDNAProfile(BaseModel):
    voice_dna_profile_id: str
    guest_id: str
    construction_mechanics: list[str]
    negative_space: list[str]
    normative_expression_targets: list[str]
    calibration_receipt_ids: list[str] = []
    emotional_dna_profile_id: str | None = None


class InductionRationale(BaseModel):
    rationale_id: str
    planned_move_id: str
    cral_finding_ids: list[str]
    context_premise_id: str
    trigger_map_id: str
    emotional_dna_profile_id: str | None = None
    voice_dna_profile_id: str | None = None
    matrix_brief_id: str
    matrix_edge_product_id: str | None = None
    target_expression_state: list[str]
    intended_extraction_outcome: list[str]
    rationale_mode: RationaleMode
    support_limitations: list[str] = []
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileCRALFindingsCommand`, `CompileAudienceDeepTriggerMapCommand`, `ExtractEmotionalDNACommand`, `CompileVoiceDNAProfileCommand`, `CompileInductionRationaleCommand`, `BlockUnsupportedPsychologyCommand` |
| Events | `CRALFindingsCompiled`, `AudienceDeepTriggerMapCompiled`, `EmotionalDNAExtracted`, `VoiceDNAProfileCompiled`, `InductionRationaleCompiled`, `UnsupportedPsychologyBlocked` |
| Workflow | `InterviewPreparationWorkflow.stage3_4_compile_induction_rationale` |
| Receipt | `InductionRationaleReceipt` with evidence IDs, rationale mode, compiler versions, blocked claims, and downstream bindings |

Every rationale must bind to at least one planned move, pre-induction question, or Interview Asset Contract. Orphan rationales are invalid.

## 7. Backward Compatibility and Migration Fallback

Legacy Voice DNA and anti-draft modules can provide schema/eval guidance and fixtures. Production profiles must be generated as CMF STUDIO typed records with evidence, consent compatibility where applicable, and calibration receipts.

If Emotional DNA or Voice DNA evidence is absent, the system uses partial rationale mode and prevents claims that imply full psychological certainty.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Deep induction vs. unsupported psychology | Rationale mode and support limitations are mandatory. | UI shows partial/blocked rationale instead of confident claims. |
| Voice DNA vs. imitation | Voice profile references construction mechanics and negative space, not surface tone mimicry. | Anti-draft and calibration receipts attach to downstream drafting/extraction. |
| Context Premise vs. persona summary | Trigger map fields are required for interview move explanation. | Planned move shows hermeneutical gap, moral-emotional vector, and match logic when available. |

## 9. Tasks

- Add contracts and persistence models for CRAL, DNA profiles, and induction rationales.
- Implement DSPy compilers and validation wrappers.
- Add evidence support validator and unsupported psychology blocker.
- Add partial-mode behavior and UI inspection models.
- Attach rationale IDs to pre-induction and Interview Asset Contract outputs.
- Add fixtures from legacy CRAL, Voice DNA, anti-draft, Matrix, and RSCS sources.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | CRAL roles are preserved when evidence is promoted. | CRAL finding stored as generic "insight." |
| AC2 | Audience Deep Trigger Map includes depth, gaps, vectors, coping, focus when available, confidence, and gaps. | Context output is only a target persona paragraph. |
| AC3 | Emotional DNA/Voice DNA distinguish belief, construction, emotional path, negative space, suppression, triggers, and targets. | Profile imitates tone with no emotional root. |
| AC4 | Operator can inspect rationale for each move. | Question appears with no CRAL/context/DNA explanation. |
| AC5 | Insufficient evidence creates partial/shallow mode and blocks certainty. | Plan claims a deep trauma pattern with no source support. |

## 11. Dependencies

- TS-CMF-023 through TS-CMF-027.
- TS-CMF-011 Voice-DNA Boost eligibility and audio classification.
- TS-CMF-015 JIT skill compiler saturation and contrast.
- TS-CMF-017 intentional orchestration migration contracts.
- TS-CMF-008 consent records where source material includes likeness/voice/private guest data.

## 12. Testing Strategy


Unit tests:

- Unit tests for CRAL moment enum, rationale mode, and support limitation fields.
- Compiler tests for partial-mode behavior when evidence is incomplete.
- Validator tests for unsupported psychology, tone imitation, missing trigger map, and missing evidence IDs.
- Workflow tests proving rationale IDs attach to pre-induction questions and Interview Asset Contracts.
- Evaluation tests comparing generic prompt rationale against CRAL/context/DNA grounded rationale.

Integration tests:

- Workflow test from `CRAL/context/DNA evidence` to `InductionRationale` through pipeline stage `3 / 4`.
- Command Bus test proving `induction rationale receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for rationale mode distribution, blocked unsupported psychology, missing DNA evidence, and rationale inspection usage.
- Logs include compiler versions, evidence hashes, rationale IDs, and downstream binding IDs.
- Recovery: enrich evidence, rerun CRAL/context/DNA compilers, and create a new rationale version.
- Rollback: supersede rationale and invalidate dependent draft plans/contracts while preserving completed-session lineage.

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
| Tech Spec ID | TS-CMF-028 |
| Story | 5.6 |
| Requirement Trace | FR-CMF-05.08 |
| Pipeline Trace | Stages 3 / 4, CRAL/context/DNA evidence to InductionRationale |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No unsupported psychology, no tone imitation, no persona collapse, no legacy runtime coupling |

