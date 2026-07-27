---
story_id: "5.1"
story_title: "Research Fields and Evidence Capture"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-05.01"
pipeline_stage: "3"
entry_object: "research evidence"
exit_object: "`ResearchField`, `ResearchEvidence`"
validation_contract: "provenance/freshness gate"
required_receipt: "research evidence receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 5.1: Research Fields and Evidence Capture

**Epic:** 5 - Interview Intelligence and Narrative State Induction
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-05.01 |
| Canonical Pipeline Stage | 3 |
| Entry Object | research evidence |
| Exit Object | `ResearchField`, `ResearchEvidence` |
| Validation Contract | provenance/freshness gate |
| Required Receipt | research evidence receipt |
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

As an Operator, I want to create Research Fields with evidence, citations, claims, confidence, temporal sensitivity, provenance, and gaps, so that interview preparation has reality contact.

**Acceptance Criteria:**

- Given an Operator creates a Research Field, when evidence is added, then each item records claim, source, citation, confidence, temporal sensitivity, provenance, and research gap status.
- Given a claim is temporally sensitive, when it is reused in an interview plan, then the system marks it for freshness verification.
- Given evidence lacks provenance, when it is saved, then it remains draft and cannot support an Interview Asset Contract.
- Given a Research Field is brand-scoped, when another brand is active, then evidence cannot leak across brands.
- Given research is approved for use, when the workflow compiles downstream artifacts, then evidence IDs are retained.

**Technical Notes:** Implement `ResearchField`, `ResearchEvidence`, source provenance contracts, and `/api/v1/research` commands.

**Legacy and Primitive Mapping:** RSCS Law 1 saturation before compression, CRAL/Visual Research references. Active families: STR, SAF.

**Prerequisites:** Epics 1 through 4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
