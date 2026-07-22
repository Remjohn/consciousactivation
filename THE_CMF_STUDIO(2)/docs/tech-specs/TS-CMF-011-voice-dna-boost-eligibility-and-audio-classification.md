---
tech_spec_id: "TS-CMF-011"
title: "Voice-DNA Boost Eligibility and Audio Classification"
story_id: "2.4"
story_title: "Voice-DNA Boost Eligibility and Audio Classification"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-2-4-voice-dna-boost-eligibility-and-audio-classification.md"
fr_ids:
  - "FR-CMF-02.05"
  - "FR-CMF-02.06"
pipeline_stage: "12 / 13"
entry_object: "voice repair request"
exit_object: "VoiceBoostEligibilityReport, audio manifest"
validation_contract: "repair hierarchy and claim restrictions"
required_receipt: "voice eligibility receipt"
runtime_target: "Python / Pydantic v2 / DSPy / MOSS-TTS adapter / LavaSR adapter / render manifest"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-011: Voice-DNA Boost Eligibility and Audio Classification

**Status:** Ready for Development  
**Story:** `2.4 - Voice-DNA Boost Eligibility and Audio Classification`  
**Implementation Boundary:** Voice-DNA Boost eligibility, repair hierarchy proof, audio source classification, voice continuity evaluation, and voice eligibility receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Voice-DNA Boost hierarchy, MOSS-TTS/LavaSR provider intent, duration caps, visual covering, and claim restrictions. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-02.05 and FR-CMF-02.06 source authority. |
| `docs/architecture.md` | Architecture source for VoiceBoostEligibilityReport, VoiceBridgeManifest, synthetic voice policy, and human review. |
| `docs/cmf-studio-pipeline-map.md` | Stage 12 and 13 trace for rendering, evaluation, and review. |
| `docs/migration/legacy-inventory.md` | Legacy `voice_dna_models.py`, `anti_draft_calibrator.py`, SFL failure corpus, and audio engine references as migration context. |
| `docs/stories/story-2-4-voice-dna-boost-eligibility-and-audio-classification.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-008-versioned-consent-records.md` | Explicit synthetic voice consent dependency. |
| `docs/tech-specs/TS-CMF-010-consent-blockers-across-workflows.md` | Consent blocker dependency. |

## 2. Overview

### Problem Statement

Voice-DNA Boost can repair awkward transitions and structural gaps, but it is dangerous if treated as a normal rewriting layer. Synthetic voice must never become the guest's primary voice of truth or carry decisive claims. The audio manifest must also distinguish source, repaired source, synthetic bridge, interviewer, generated audio, SFX, and music so reviewers can understand exactly what they are approving.

### Solution

Implement Voice-DNA Boost as a narrow structural repair exception. The eligibility workflow must prove the repair hierarchy has been exhausted: recut existing source, verbatim fragment search, prior approved quote, and human pickup request availability. Only then can synthetic bridge voice be requested, and only with explicit consent, source evidence, visual covering, duration cap, evaluation receipts, claim restrictions, and human approval. Audio outputs are classified in an `AudioMixManifest`.

### Scope

In scope:

- `VoiceBoostEligibilityReport`, `AudioSourceType`, `AudioSegmentClassification`, `AudioMixManifest`, `VoiceBridgeManifest`, and `VoiceEligibilityReceipt`.
- Repair hierarchy proof.
- Duration cap: `min(7 seconds, 15% of final video duration)`.
- Claim restrictions blocking primary claims, decisive confessions, medical/legal/financial advice, and decisive emotional truth.
- Integration points for SemanticCritic, VoiceContinuityCritic, AntiDraftCalibrationProgram, MOSS-TTS, and LavaSR.
- Review failure behavior when Voice DNA evaluation fails.

Out of scope:

- Implementing MOSS-TTS or LavaSR internals.
- Full render assembly.
- Voice clone model training implementation.
- External legal agreement management.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-02.05 | System evaluates Voice-DNA Boost eligibility against consent, evidence, hierarchy, and restrictions. | `VoiceBoostEligibilityReport`, repair hierarchy proof, consent compatibility, duration cap, claim restriction classifier, and voice eligibility receipt. |
| FR-CMF-02.06 | System distinguishes source, repaired source, synthetic bridge, interviewer, and generated audio. | `AudioSourceType`, segment classifications, `AudioMixManifest`, `VoiceBridgeManifest`, and review display model. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `12 - Rendering and assembly`; `13 - Evaluation, review, revision, approval` |
| Entry Object | Voice repair request |
| Exit Object | `VoiceBoostEligibilityReport`, audio manifest |
| Allowed Actors / Services | Reviewer, Operator, SemanticCritic, VoiceContinuityCritic, AudioService, MOSS-TTS adapter, LavaSR adapter |
| Validation Contract | Repair hierarchy, explicit consent, source evidence, visual covering, duration cap, claim restrictions, evaluation receipts |
| Required Receipt | Voice eligibility receipt |
| Forbidden Shortcut | Synthetic voice as convenience rewrite, synthetic bridge carrying primary claims, unclassified audio segments, approval after Voice DNA evaluation failure |

### Legacy Intelligence Mapping

Legacy Voice DNA schemas, anti-draft calibration, SFL failure corpus, and audio engine references are migration sources for contracts, fixtures, and evals. They are not runtime imports. DSPy may evaluate semantic gap, voice continuity, and claim restriction, but Command Bus and ReviewService decide eligibility state from typed reports and receipts.

Target modules:

- `ccp_studio.contracts.voice`
- `ccp_studio.contracts.audio`
- `ccp_studio.services.voice_boost_eligibility`
- `ccp_studio.services.audio_classification`
- `ccp_studio.dspy_programs.voice_continuity_critic`
- `ccp_studio.dspy_programs.anti_draft_calibration_program`
- `ccp_studio.providers.moss_tts`
- `ccp_studio.providers.lavasr`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `VoiceBoostEligibilityReport` | Eligibility verdict and evidence for structural repair exception. |
| `RepairHierarchyProof` | Evidence that recut, verbatim fragment, prior approved quote, and human pickup were unavailable or insufficient. |
| `VoiceBridgeManifest` | Synthetic bridge details, provider metadata, cap compliance, visual covering, and restriction results. |
| `AudioMixManifest` | Full classification of source, repaired source, synthetic bridge, interviewer, generated audio, SFX, and music. |
| `CalibrationReport` | Voice continuity and anti-draft evaluation evidence. |
| `VoiceEligibilityReceipt` | Immutable approval/block receipt. |

## 4. Implementation Plan

### Workstream A: Contracts

Define voice eligibility, repair hierarchy, bridge manifest, audio classification, calibration report, and receipt contracts.

### Workstream B: Repair Hierarchy

Implement checks for recut existing source, verbatim fragment search, prior approved quote, and human pickup request. Synthetic bridge is unavailable until the hierarchy is exhausted.

### Workstream C: Consent and Claim Policy

Require explicit synthetic voice consent and block restricted claim categories. Use source references and evaluation receipts as evidence.

### Workstream D: Audio Classification

Produce `AudioMixManifest` for every rendered asset with segment-level audio type and provenance.

### Workstream E: Provider Adapter Boundary

MOSS-TTS and LavaSR are behind provider adapters. They cannot create canonical approval state. They return provider receipts and artifacts only.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class AudioSourceType(str, Enum):
    source_voice = "source_voice"
    repaired_source_voice = "repaired_source_voice"
    synthetic_bridge_voice = "synthetic_bridge_voice"
    interviewer_voice = "interviewer_voice"
    generated_audio = "generated_audio"
    sfx = "sfx"
    music = "music"


class VoiceEligibilityStatus(str, Enum):
    eligible = "eligible"
    blocked = "blocked"
    review_required = "review_required"


class RepairHierarchyProof(BaseModel):
    schema_version: Literal["cmf.repair_hierarchy_proof.v1"]
    recut_checked: bool
    verbatim_fragment_search_checked: bool
    prior_approved_quote_checked: bool
    human_pickup_request_checked: bool
    evidence_refs: list[str] = Field(default_factory=list)


class VoiceBoostEligibilityReport(BaseModel):
    schema_version: Literal["cmf.voice_boost_eligibility_report.v1"]
    voice_boost_eligibility_report_id: UUID
    organization_id: UUID
    brand_id: UUID
    render_output_id: UUID
    status: VoiceEligibilityStatus
    consent_record_version_id: UUID
    repair_hierarchy: RepairHierarchyProof
    max_duration_seconds: float
    requested_duration_seconds: float
    visual_covering_required: bool
    claim_restriction_passed: bool
    evaluation_receipt_ids: list[UUID]
    blocker_codes: list[str] = Field(default_factory=list)


class AudioSegmentClassification(BaseModel):
    schema_version: Literal["cmf.audio_segment_classification.v1"]
    segment_id: UUID
    source_type: AudioSourceType
    start_seconds: float
    end_seconds: float
    source_ref: str
    provider_receipt_id: UUID | None = None


class AudioMixManifest(BaseModel):
    schema_version: Literal["cmf.audio_mix_manifest.v1"]
    audio_mix_manifest_id: UUID
    render_output_id: UUID
    segments: list[AudioSegmentClassification]
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `RequestVoiceBoostEligibilityCommand`, `RecordRepairHierarchyProofCommand`, `ClassifyAudioSegmentsCommand`, `CreateVoiceBridgeManifestCommand`, `RejectVoiceBoostCommand` |
| Events | `VoiceBoostEligibilityEvaluated`, `VoiceBridgeManifestCreated`, `AudioMixManifestCreated`, `VoiceBoostBlocked`, `VoiceEligibilityReceiptWritten` |
| Workflows | Voice boost eligibility workflow, audio classification workflow, voice review workflow |
| Receipts | `VoiceEligibilityReceipt`, `ProviderReceipt`, `EvaluationReceipt`, `ApprovalEvent` |

## 7. Backward Compatibility and Migration Fallback

Legacy Voice DNA models and audio engines are fixtures, schemas, and eval targets. If a historical audio asset lacks classification, it cannot be used for approval, publishing, memory, or voice repair until classified.

Fallback behavior:

- Missing synthetic voice consent returns `SYNTHETIC_VOICE_CONSENT_REQUIRED`.
- Repair hierarchy not exhausted returns `VOICE_REPAIR_HIERARCHY_INCOMPLETE`.
- Duration cap exceeded returns `VOICE_BRIDGE_DURATION_CAP_EXCEEDED`.
- Restricted claim returns `VOICE_BRIDGE_CLAIM_RESTRICTED`.
- Missing visual covering returns `VOICE_BRIDGE_VISUAL_COVERING_REQUIRED`.
- Failed Voice DNA evaluation returns `VOICE_DNA_EVALUATION_FAILED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Voice repair can improve continuity; synthetic voice can also erase source truth and guest agency. |
| UX / Ops Failure Scenario | A synthetic bridge carries the guest's decisive claim because it is smoother than the available source. |
| Resolution Demand | Source truth and repair hierarchy take precedence. Voice-DNA Boost is allowed only as a documented structural bridge with explicit constraints and review. |
| Downstream Proof | Tests must prove hierarchy exhaustion, duration cap, claim restrictions, visual covering, audio classification, and review blocking on failed evaluation. |

## 9. Tasks

- Define voice and audio contracts.
- Implement repair hierarchy proof.
- Implement claim restriction policy.
- Integrate consent compatibility.
- Implement audio segment classification.
- Add MOSS-TTS and LavaSR adapter boundaries.
- Add voice eligibility receipts.
- Add review blocking behavior.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Voice-DNA Boost checks recut, verbatim fragment, prior approved quote, and human pickup first. | Synthetic bridge is generated before source search. |
| AC2 | Eligible bridge receipt proves consent, evidence, visual covering, duration cap, hierarchy, and claim restrictions. | Receipt lacks visual covering proof. |
| AC3 | Audio manifest distinguishes all audio source types. | Synthetic bridge appears as normal source voice. |
| AC4 | Primary claim, decisive confession, or sensitive assertion is rejected. | Synthetic voice delivers the core claim of the asset. |
| AC5 | Failed Voice DNA evaluation blocks approval. | Reviewer can approve bridge after evaluation failure. |

## 11. Dependencies

Internal:

- TS-CMF-008 Consent records
- TS-CMF-010 Consent blockers
- Source artifact gate
- Evaluation and Review specs from Epic 9
- Rendering specs from Epic 8

External:

- Pydantic v2
- DSPy
- MOSS-TTS adapter
- LavaSR adapter
- Object storage

## 12. Testing Strategy

Unit tests:

- Duration cap calculation.
- Claim restriction classifier outputs.
- Repair hierarchy proof validation.
- Audio segment classification schema.

Integration tests:

- Eligible voice bridge writes report and receipt.
- Ineligible bridge rejected for missing hierarchy.
- Restricted claim rejected.
- Failed voice evaluation blocks review.
- Audio manifest persists provider receipt links.

Safety tests:

- Synthetic bridge cannot be approved without explicit consent.
- MOSS-TTS adapter cannot write approval state.
- Audio classification required before publishing.

## 13. Observability, Recovery, and Rollback

- Logs include `voice_boost_eligibility_report_id`, `render_output_id`, `duration`, `claim_restriction_passed`, and consent version.
- Metrics track eligibility requested, blocked reasons, approved bridges, evaluation failures, and cap violations.
- Recovery can regenerate audio classification from stored manifests and provider receipts.
- Rollback removes or supersedes bridge via render revision command, never silent audio replacement.

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
| Requirement Trace | FR-CMF-02.05, FR-CMF-02.06 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Voice DNA, anti-draft, and audio engine references mapped to contracts, fixtures, and evals |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python eligibility policy, DSPy critics, provider adapters behind receipts |
| TypeScript Boundary | Review surfaces consume manifests only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

