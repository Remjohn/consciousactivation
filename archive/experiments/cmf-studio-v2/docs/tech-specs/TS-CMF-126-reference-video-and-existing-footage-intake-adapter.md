---
tech_spec_id: "TS-CMF-126"
title: "Reference Video and Existing Footage Intake Adapter"
story_id: "13.7"
story_title: "Reference Video and Existing Footage Intake Adapter"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.07"
pipeline_stage: "source/reference intake and provenance"
entry_object: "ReferenceMediaIntakeCommand"
exit_object: "ReferenceVideoAnalysisReceipt or SourceFootageInspectionReceipt"
validation_contract: "media classification, consent, source lineage, copyright risk, transcript alignment, composition inspiration boundary"
required_receipt: "ReferenceVideoAnalysisReceipt"
runtime_target: "Python / Pydantic v2 / source ingestion / visual research / media inspection / review workbench"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-126: Reference Video and Existing Footage Intake Adapter

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Source, routing, and rejection mandates. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.07. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-009-recording-setup-and-source-artifact-gate.md` | Source artifact gate dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-030-source-ingestion-transcript-alignment-and-provenance.md` | Source ingestion and provenance dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition reference handoff dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/source_ingestion.py` | Existing source ingestion owner. |
| `THE CMF STUDIO/src/ccp_studio/services/source_provenance_service.py` | Existing provenance owner. |
| `THE CMF STUDIO/src/ccp_studio/services/source_quality.py` | Existing media/source quality owner. |
| `THE CMF STUDIO/src/ccp_studio/services/visual_research_service.py` | Existing visual research owner. |
| `THE CMF STUDIO/src/ccp_studio/services/consent_guard.py` | Consent gate owner. |
| `THE CMF STUDIO/src/ccp_studio/services/review_state_service.py` | Review read-model owner. |
| `OpenMontage README.md` | Reference pattern for starting from topic/reference video. |

## 2. Overview

Operators will often bring references: YouTube videos, Reels, Shorts, downloaded clips, existing interviews, competitor videos, or raw guest footage. CMF must classify these inputs correctly before any downstream use. A reference video is not automatically source truth. A source interview is not merely inspiration. A competitor clip is not an asset to copy.

This spec creates the intake adapter that classifies media as `inspiration_reference`, `source_footage`, `existing_interview`, `brand_owned_broll`, `competitor_reference`, `prohibited_unlicensed`, or `unknown_requires_review`. For inspiration, it extracts composition lessons such as pacing, hook, scene structure, motion grammar, subtitle behavior, framing, visual hierarchy, and emotional logic without copying protected expression. For source footage, it runs consent, media inspection, transcription, diarization, scene detection, frame sampling, and provenance capture.

The output is a receipt that downstream systems can trust. Reference analysis can guide composition. Source inspection can feed expression extraction and editing. Copyright risk and consent gaps become explicit blockers.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-126-001 | `ReferenceMediaIntakeCommand` | Typed command for URL/file/reference/source media intake. |
| DEP-CMF-126-002 | `ReferenceMediaClassification` | Classification and risk model for inspiration vs source vs prohibited media. |
| DEP-CMF-126-003 | `ReferenceCompositionAnalysis` | Extracts composition lessons without copying protected creative expression. |
| DEP-CMF-126-004 | `SourceFootageInspection` | Media inspection, consent status, transcription, diarization, scene sampling, and provenance. |
| DEP-CMF-126-005 | `ReferenceVideoAnalysisReceipt` | Receipt for inspiration/reference analysis. |
| DEP-CMF-126-006 | `SourceFootageInspectionReceipt` | Receipt for source footage usable in extraction or editing. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/source.py` | Add reference media command, classification, composition analysis, source inspection, and receipt models. |
| `src/ccp_studio/services/source_ingestion.py` | Add media classification and branch to reference vs source workflows. |
| `src/ccp_studio/services/source_provenance_service.py` | Store URL/file hashes, provenance, license notes, and media lineage. |
| `src/ccp_studio/services/source_quality.py` | Inspect duration, resolution, audio, frame quality, and transcription readiness. |
| `src/ccp_studio/services/visual_research_service.py` | Extract visual grammar and composition lessons for inspiration references. |
| `src/ccp_studio/services/consent_guard.py` | Block source-footage use without consent scope. |
| `src/ccp_studio/services/review_state_service.py` | Surface classification, risk, and permitted downstream use. |
| `src/ccp_studio/api/v1/source.py` | Add media intake, classify, inspect, and receipt endpoints. |
| `POST /api/v1/source/media-intake`, `POST /api/v1/source/media-intake/{record_id}/classify`, `POST /api/v1/source/media-intake/{record_id}/inspect`, `GET /api/v1/source/media-intake/{record_id}` | Exact API routes for reference/source intake lifecycle. |
| `src/ccp_studio/repositories/source_artifacts.py` | Persist source/reference records and receipts. |
| Postgres tables: `reference_media_intake_records`, `source_media_classifications`, `reference_composition_analyses`, `source_media_inspection_receipts`, `source_provenance_records` | Durable storage for media classification, inspection, composition lessons, and provenance. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PER-003` | Intelligence-Gated Intercept | Downstream use depends on correct classification and consent state. |
| `EXP-FBK-001` | Actionable Rejection | Copyright, consent, or classification gaps return exact blocker. |
| `EXP-SOC-001` | Verifiable Artifact | Classification and inspection receipts include source hashes and provenance. |
| `EXP-TRS-004` | Cinematic Meaning | Reference analysis extracts function and feeling, not carbon copies. |
| `EXP-FRC-006` | Frictionless Block | Unknown risk routes to review instead of unsafe use. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Media cannot feed extraction/editing until classification and consent pass. |
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Inspiration analysis captures composition logic without copying expression. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Risk blockers name consent, license, provenance, or classification issue. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Intake and inspection produce hash-backed receipts. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Separate inspiration from source truth. | Prevents reference videos from becoming unapproved source claims. |
| Capture composition function, not copyable expression. | Supports learning from references while reducing copyright risk. |
| Unknown media requires human review. | Avoids unsafe automated classification. |
| Source footage uses stricter consent and provenance gates. | Guest-owned editing must be auditable. |

## 4. Implementation Plan

1. Add source contracts for intake command, classification, composition analysis, source inspection, and receipts.
2. Extend source ingestion with URL/file intake and classification.
3. Add media inspection using existing source quality hooks: duration, resolution, codec, audio, frame samples, transcript readiness.
4. Add consent gate for source-footage and existing-interview branches.
5. Add visual research extraction for inspiration references: pacing, hook structure, subtitle behavior, framing, motion grammar, hierarchy, emotional logic.
6. Add copyright/license risk fields and review blockers.
7. Persist provenance, hashes, and classification receipts.
8. Surface risk and allowed downstream use in review state.
9. Add tests for classification, consent, reference/source separation, copyright risk, and receipt replay.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class ReferenceMediaClassification(BaseModel):
    schema_version: Literal["cmf.reference_media_classification.v1"]
    classification_id: str
    media_ref: str
    media_kind: Literal[
        "inspiration_reference", "source_footage", "existing_interview",
        "brand_owned_broll", "competitor_reference",
        "prohibited_unlicensed", "unknown_requires_review"
    ]
    consent_status: Literal["not_required", "present", "missing", "requires_review"]
    copyright_risk: Literal["low", "medium", "high", "blocked", "unknown"]
    allowed_downstream_uses: list[str]
    blocker_codes: list[str] = Field(default_factory=list)


class ReferenceCompositionAnalysis(BaseModel):
    schema_version: Literal["cmf.reference_composition_analysis.v1"]
    analysis_id: str
    classification_id: str
    hook_pattern: str | None = None
    pacing_notes: list[str] = Field(default_factory=list)
    framing_patterns: list[str] = Field(default_factory=list)
    subtitle_behavior: list[str] = Field(default_factory=list)
    motion_grammar: list[str] = Field(default_factory=list)
    emotional_logic: list[str] = Field(default_factory=list)
    prohibited_copy_elements: list[str] = Field(default_factory=list)


class ReferenceVideoAnalysisReceipt(BaseModel):
    schema_version: Literal["cmf.reference_video_analysis_receipt.v1"]
    receipt_id: str
    classification_id: str
    analysis_id: str | None = None
    source_hashes: dict[str, str]
    allowed_downstream_uses: list[str]
    blocker_codes: list[str] = Field(default_factory=list)
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing source ingestion continues for already approved uploaded source artifacts. New reference URLs or files must pass through this classification adapter before downstream use. If classification is unavailable, media is marked `unknown_requires_review` and cannot feed extraction, editing, rendering, or asset generation until reviewed.

The fallback for a blocked reference is not to use it secretly; it is to record the reference as prohibited, extract no assets, and return safer alternatives such as "use as verbal inspiration only", "replace with licensed footage", or "request consent".

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T126-01 | Contracts | Add intake, classification, reference analysis, source inspection, receipts. |
| T126-02 | Source Ingestion | Implement media classification branch. |
| T126-03 | Provenance | Store URL/file hashes, metadata, and allowed uses. |
| T126-04 | Visual Research | Extract composition lessons for reference media. |
| T126-05 | Consent | Block source branch without consent scope. |
| T126-06 | Review UI | Show classification, risk, and downstream permissions. |
| T126-07 | Tests | Add media classification, consent, copyright risk, and replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC126-01 | Intake classifies media before downstream use. | Competitor video is treated as editable source footage. | Phase4-M01; classification test. |
| AC126-02 | Source footage requires consent and provenance before extraction/editing. | Existing interview transcript is processed without consent state. | Phase4-M01; consent gate test. |
| AC126-03 | Inspiration analysis extracts composition function, not copyable assets. | System copies a competitor's exact graphic layout. | Phase4-M02; prohibited-copy test. |
| AC126-04 | Copyright and license risks become explicit blockers. | Unlicensed clip is stored as direct-use B-roll. | Phase4-M05; risk blocker test. |
| AC126-05 | Receipts include source hashes and allowed downstream uses. | Operator cannot tell whether a reference can be rendered. | Phase5-M01; receipt replay test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-009` | Source artifact gate | Must enforce source validity. |
| `TS-CMF-030` | Ingestion/provenance | Must be extended. |
| `TS-CMF-080` | Composition binding | Receives reference lessons only when allowed. |
| `source_ingestion.py` | Existing service | Extend. |
| `visual_research_service.py` | Existing service | Extend. |
| `consent_guard.py` | Existing service | Reuse. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Classification tests | URL/local media resolves to correct media kind and allowed uses. |
| Consent tests | Source footage and existing interview branches block without consent. |
| Copyright tests | High-risk or blocked media cannot become direct-use assets. |
| Analysis tests | Inspiration analysis emits composition lessons and prohibited copy elements. |
| Receipt tests | Classification and reference analysis receipts replay from hashes and metadata. |
| Review tests | Review state exposes classification, risk, blockers, and allowed downstream use. |
