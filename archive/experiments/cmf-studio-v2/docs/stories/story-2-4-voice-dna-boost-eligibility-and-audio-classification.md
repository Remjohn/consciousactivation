---
story_id: "2.4"
story_title: "Voice-DNA Boost Eligibility and Audio Classification"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-02.05"
  - "FR-CMF-02.06"
pipeline_stage: "12 / 13"
entry_object: "voice repair request"
exit_object: "`VoiceBoostEligibilityReport`, audio manifest"
validation_contract: "repair hierarchy and claim restrictions"
required_receipt: "voice eligibility receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 2.4: Voice-DNA Boost Eligibility and Audio Classification

**Epic:** 2 - Consent, Source, Likeness, and Voice Safety
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-02.05, FR-CMF-02.06 |
| Canonical Pipeline Stage | 12 / 13 |
| Entry Object | voice repair request |
| Exit Object | `VoiceBoostEligibilityReport`, audio manifest |
| Validation Contract | repair hierarchy and claim restrictions |
| Required Receipt | voice eligibility receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Make consent, source truth, likeness, file provenance, and voice eligibility product-level blockers before recording, extraction, rendering, review, memory, and publishing.

**Covers:** FR-CMF-02.01 through FR-CMF-02.07.

**User Value:** Guests and clients keep authority over permission boundaries; Operators and Reviewers know exactly when work is allowed, blocked, or requires repair.

**Technical Context:** `/api/v1/consent`, consent record versions, source artifact storage, recording configuration, voice eligibility policy, review gates, render manifests, error code `CONSENT_SCOPE_BLOCKED`.

**CBAR Failure Scenario:** If consent is a checkbox instead of a state machine, then a revoked likeness can still leak into a render, memory, or publishing job. Consent therefore becomes an execution gate across the whole chain.

## Story Definition

As a Reviewer, I want Voice-DNA Boost to be allowed only as a documented structural repair exception, so that synthetic voice never becomes the primary voice of truth.

**Acceptance Criteria:**

- Given a SemanticCritic finds a structural gap, when Voice-DNA Boost is requested, then the system first checks recut, verbatim fragment search, prior approved quote, and human pickup request availability.
- Given synthetic bridge voice is eligible, when the command succeeds, then the receipt proves explicit consent, source evidence, visual covering, duration cap, repair hierarchy, and claim restrictions.
- Given synthetic bridge audio is included in a render, when the manifest is produced, then it distinguishes source voice, repaired source voice, synthetic bridge voice, interviewer voice, generated audio, SFX, and music.
- Given a requested synthetic bridge would carry a primary claim, decisive confession, or sensitive assertion, when eligibility runs, then the request is rejected.
- Given Voice DNA evaluation fails, when review opens, then the Reviewer sees the evidence and cannot approve the bridge.

**Technical Notes:** Implement `VoiceDnaBoostEligibility`, `AudioSourceType`, `AudioMixManifest`, `CalibrationReport`, and `AntiDraftCalibrationProgram` integration.

**Legacy and Primitive Mapping:** Legacy `voice_dna_models.py`, `anti_draft_calibrator.py`, SFL failure corpus. Active families: VOC, SAF, FBK.

**Prerequisites:** Stories 2.1 through 2.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
