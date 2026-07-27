---
story_id: "2.3"
story_title: "Consent Blockers Across Workflows"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-02.03"
pipeline_stage: "all gated stages"
entry_object: "consent-sensitive command"
exit_object: "blocked or allowed state"
validation_contract: "current consent compatibility"
required_receipt: "consent blocker receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 2.3: Consent Blockers Across Workflows

**Epic:** 2 - Consent, Source, Likeness, and Voice Safety
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-02.03 |
| Canonical Pipeline Stage | all gated stages |
| Entry Object | consent-sensitive command |
| Exit Object | blocked or allowed state |
| Validation Contract | current consent compatibility |
| Required Receipt | consent blocker receipt |
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

As a Reviewer, I want incompatible consent to block processing, rendering, memory, review, and publishing, so that unsafe work cannot slip through another surface.

**Acceptance Criteria:**

- Given a consent scope does not allow provider processing, when a provider job command is submitted, then it fails with `CONSENT_SCOPE_BLOCKED`.
- Given likeness reuse is revoked, when an Operator attempts to re-render a scene using that likeness, then the command is blocked and all affected pending jobs are flagged.
- Given publication consent is missing, when Publishing Intent is drafted, then the draft is blocked before external scheduling.
- Given a memory admission candidate references sensitive source without compatible consent, when admission is reviewed, then approval is unavailable and quarantine is offered.
- Given consent changes after an asset was approved, when future reuse is requested, then the system reevaluates the current consent version rather than trusting historical approval.

**Technical Notes:** Consent policy must be called by provider jobs, render commands, memory admission, review commands, and publishing commands. Add tests for revoked consent in each boundary.

**Legacy and Primitive Mapping:** Consent doctrine, receipt chain, governance gates. Active families: SAF, FBK.

**Prerequisites:** Stories 2.1 and 2.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
