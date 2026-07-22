---
tech_spec_id: "TS-CMF-047"
title: "Audio, Caption, Timeline, and Mix Assembly"
story_id: "8.6"
story_title: "Audio, Caption, Timeline, and Mix Assembly"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-6-audio-caption-timeline-and-mix-assembly.md"
fr_ids:
  - "FR-CMF-08.06"
pipeline_stage: "12"
entry_object: "audio/caption/timeline plan"
exit_object: "manifests and final mix"
validation_contract: "voice/caption/timing validation"
required_receipt: "sonic/timeline receipt"
runtime_target: "Python / Pydantic v2 / audio services / caption service / renderer manifests"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-047: Audio, Caption, Timeline, and Mix Assembly

**Status:** Ready for Development  
**Story:** `8.6 - Audio, Caption, Timeline, and Mix Assembly`  
**Implementation Boundary:** Source/interviewer/restored/synthetic/SFX/music/final audio components, caption manifests, timeline manifests, ducking decisions, final mix, and sonic/timeline receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-6-audio-caption-timeline-and-mix-assembly.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.06 authority and no-opaque-artifact rule. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | LavaSR/MOSS-TTS, Voice-DNA Boost limits, audio continuity risks. |
| `docs/architecture.md` | Audio/caption/timeline manifests and Voice-DNA rules. |
| `docs/cmf-studio-pipeline-map.md` | Rendering sub-workflow and sonic receipt. |
| `docs/migration/legacy-inventory.md` | Legacy audio engine, caption engine, timeline generator, SFL failure corpus. |

## 2. Overview

Implement auditable sonic and timeline assembly. Source audio, interviewer audio, restored audio, synthetic bridge audio, SFX, music, captions, and final mix must be separate timeline components with source/role classification and validation. Synthetic bridge voice follows Voice-DNA Boost eligibility, duration, visual-covering, and provenance constraints.

Caption and timeline decisions are not styling afterthoughts. They are part of render reproducibility and review.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.06 | Separate source audio, interviewer audio, restored audio, synthetic bridge audio, SFX, music, captions, and final mix into auditable timeline components. | `AudioMixManifest`, `CaptionManifest`, `TimelineManifest`, component roles, ducking metadata, Voice-DNA Boost guard, and sonic/timeline receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 12 - Rendering and assembly |
| Entry Object | audio/caption/timeline plan |
| Exit Object | manifests and final mix |
| Validation Contract | voice/caption/timing validation |
| Required Receipt | sonic/timeline receipt |

### Legacy Intelligence Mapping

- Legacy audio engine informs ducking/separation math fixtures.
- Caption engine and timeline generator inform manifest shape.
- SFL failure corpus informs audio/caption continuity evals.

## 4. Implementation Plan

1. Extend `AudioMixManifest`, `CaptionManifest`, and `TimelineManifest` contracts with source roles, timing, styling, platform variants, and hashes.
2. Implement audio component classifier and ducking decision records.
3. Validate captions against source timing and platform constraints.
4. Enforce Voice-DNA Boost policy before synthetic bridge use.
5. Write `SonicTimelineReceipt` and attach to RenderOutput/EvaluationReceipt.
6. Expose review view for timeline, audio, caption, and mix lineage.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel


class AudioComponentRole(str, Enum):
    SOURCE_GUEST = "source_guest"
    INTERVIEWER = "interviewer"
    RESTORED_SOURCE = "restored_source"
    SYNTHETIC_BRIDGE = "synthetic_bridge"
    SFX = "sfx"
    MUSIC = "music"
    FINAL_MIX = "final_mix"


class AudioTimelineComponent(BaseModel):
    component_id: str
    role: AudioComponentRole
    source_artifact_id: str | None = None
    provider_receipt_id: str | None = None
    start_ms: int
    end_ms: int
    gain_db: float | None = None
    ducking_rule_id: str | None = None
    content_hash: str


class CaptionManifest(BaseModel):
    caption_manifest_id: str
    platform_variant: str
    caption_segments: list[dict]
    style_constraints: dict
    text_source_refs: list[str]
    manifest_hash: str


class SonicTimelineReceipt(BaseModel):
    sonic_timeline_receipt_id: str
    audio_mix_manifest_id: str
    caption_manifest_id: str | None = None
    timeline_manifest_id: str
    validation_summary: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileAudioMixManifestCommand`, `CompileCaptionManifestCommand`, `CompileTimelineManifestCommand`, `EvaluateAudioDuckingCommand`, `ValidateVoiceBridgePolicyCommand`, `WriteSonicTimelineReceiptCommand` |
| Events | `AudioMixManifestCompiled`, `CaptionManifestCompiled`, `TimelineManifestCompiled`, `AudioDuckingEvaluated`, `VoiceBridgePolicyValidated`, `SonicTimelineReceiptWritten` |
| Workflow | `RenderWorkflow.stage12_audio_caption_timeline_assembly` |
| Receipt | `SonicTimelineReceipt` with audio/caption/timeline hashes, ducking decisions, policy validation, and final mix refs |

## 7. Backward Compatibility and Migration Fallback

Legacy audio/caption/timeline code becomes fixtures and reference ports. Production manifests are Python-first contracts. If a legacy audio operation cannot emit component roles and hashes, it cannot be used in final assembly.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Smooth audio vs. truth | Source, restored, synthetic, SFX, music are distinct roles. | Review shows role-specific timeline components. |
| Voice repair vs. authenticity | Synthetic bridge requires Epic 2 eligibility and constraints. | Receipt stores policy validation. |
| Caption clarity vs. timing truth | Caption timing validates against source/timeline. | Caption conflicts block render or revision. |

## 9. Tasks

- Add/extend audio/caption/timeline contracts.
- Implement component classifier and ducking records.
- Add Voice-DNA Boost gate integration.
- Add caption timing validation.
- Add review read model.
- Add legacy fixture tests.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Audio mix classifies source, interviewer, restored, synthetic, SFX, music, final mix. | Synthetic bridge is indistinguishable from source. |
| AC2 | Caption manifest includes timing, text source, style, platform. | Captions saved as final text only. |
| AC3 | Ducking math and affected segments are recorded. | Music volume changes with no receipt. |
| AC4 | Synthetic bridge follows Epic 2 restrictions. | Synthetic primary claim is rendered. |
| AC5 | Review exposes timeline/audio/caption/mix lineage. | Reviewer hears final mix only. |

## 11. Dependencies

- TS-CMF-011 Voice-DNA Boost eligibility.
- TS-CMF-039 assembly plans.
- TS-CMF-043 deterministic rendering.
- TS-CMF-044 LavaSR/MOSS-TTS adapters.

## 12. Testing Strategy


Unit tests:

- Unit tests for audio component roles and hashes.
- Ducking math fixture tests from legacy audio engine.
- Caption timing conflict tests.
- Voice bridge policy tests.
- Review read model tests.

Integration tests:

- Workflow test from `audio/caption/timeline plan` to `manifests and final mix` through pipeline stage `12`.
- Command Bus test proving `sonic/timeline receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for audio policy blocks, caption conflicts, ducking failures, final mix failures, and synthetic bridge usage.
- Logs include manifest IDs, component roles, source refs, and receipt ID.
- Recovery: rebuild mix/timeline with corrected components.
- Rollback: supersede sonic receipt and invalidate dependent render/evaluation outputs.

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
| Tech Spec ID | TS-CMF-047 |
| Story | 8.6 |
| Requirement Trace | FR-CMF-08.06 |
| Pipeline Trace | Stage 12, audio/caption/timeline plan to manifests/final mix |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No opaque final mix, no synthetic/source confusion, no caption timing bypass |

