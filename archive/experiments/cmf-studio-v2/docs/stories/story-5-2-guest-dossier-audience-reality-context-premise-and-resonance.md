---
story_id: "5.2"
story_title: "Guest Dossier, Audience Reality, Context Premise, and Resonance"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-05.02"
pipeline_stage: "3"
entry_object: "approved research"
exit_object: "dossier, audience brief, Context Premise"
validation_contract: "evidence and inference validation"
required_receipt: "context compilation receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 5.2: Guest Dossier, Audience Reality, Context Premise, and Resonance

**Epic:** 5 - Interview Intelligence and Narrative State Induction
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-05.02 |
| Canonical Pipeline Stage | 3 |
| Entry Object | approved research |
| Exit Object | dossier, audience brief, Context Premise |
| Validation Contract | evidence and inference validation |
| Required Receipt | context compilation receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Help Operators prepare interviews that activate real expression before capture, then encode that preparation as typed Interview Asset Contracts.

**Covers:** FR-CMF-05.01 through FR-CMF-05.08.

**User Value:** Operators stop asking generic questions and start guiding guests into authentic, source-backed, routeable expression.

**Technical Context:** `/api/v1/research`, `/api/v1/interviews`, InterviewPreparationWorkflow, `research_fields`, `research_evidence`, `cral_findings`, `guest_dossiers`, `audience_reality_briefs`, `context_premises`, `audience_deep_trigger_maps`, `emotional_dna_profiles`, `voice_dna_profiles`, `interviewer_resonance_contexts`, `matrix_of_edging_briefs`, `interview_asset_contracts`, DSPy compilers.

**CBAR Failure Scenario:** If the interview plan is generated from a generic prompt, the guest gives centroid-safe answers and the backend can only clip mediocrity. Research saturation and narrative induction must precede extraction.

## Story Definition

As an Operator, I want the system to compile a Guest Dossier, Audience Reality Brief, Context Premise, and Interviewer Resonance Context, so that the session is prepared around the guest's truth and audience collision points.

**Acceptance Criteria:**

- Given approved Research Evidence exists, when compilation runs, then the system produces typed artifacts with source references and confidence.
- Given the Audience Reality Brief includes audience fears, desires, misconceptions, and language, when Context Premise is compiled, then it connects guest truth to audience reality.
- Given Interviewer Resonance Context is compiled, when the Operator reviews it, then it includes authentic curiosity, emotional bridges, questions to avoid, and opening state.
- Given a compilation output contains unsupported inference, when evaluation runs, then it is flagged for revision.
- Given artifacts are approved, when Interview Asset Contracts are compiled, then their IDs are included as saturation context.

**Technical Notes:** Implement DSPy compilers for `GuestDossierCompiler`, `AudienceRealityBriefCompiler`, `ContextPremiseCompiler`, and `InterviewerResonanceCompiler`.

**Legacy and Primitive Mapping:** V9 Interview-First Expression Engine, Matrix of Edging, Claude Interview Deck. Active families: PSY, STR, PRS, SAF.

**Prerequisites:** Story 5.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
