---
story_id: "5.3"
story_title: "Matrix of Edging Brief"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-05.03"
  - "FR-CMF-05.07"
pipeline_stage: "3 / 4"
entry_object: "dossier and audience reality"
exit_object: "`MatrixOfEdgingBrief`"
validation_contract: "collision and specificity gate"
required_receipt: "Matrix receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 5.3: Matrix of Edging Brief

**Epic:** 5 - Interview Intelligence and Narrative State Induction
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-05.03, FR-CMF-05.07 |
| Canonical Pipeline Stage | 3 / 4 |
| Entry Object | dossier and audience reality |
| Exit Object | `MatrixOfEdgingBrief` |
| Validation Contract | collision and specificity gate |
| Required Receipt | Matrix receipt |
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

As an Operator, I want a Matrix of Edging brief that names primary signals, tension sites, primitive candidates, coalition signatures, edge products, and likely failure points, so that the interview plan is shaped by collisions rather than bland prompts.

**Acceptance Criteria:**

- Given Guest Dossier and Audience Reality Brief exist, when Matrix of Edging compilation runs, then it produces research pass, provocation pass, authentication pass, primitive pass, coalition pass, edge pass, routing pass, and benchmark pass outputs.
- Given a tension site is proposed, when it lacks source evidence, then it is marked speculative and cannot anchor a question.
- Given a likely failure point is detected, when the Operator reviews the plan, then the system shows how to avoid centroid-safe answers.
- Given primitive candidates are attached, when routing later runs, then they remain traceable to the brief.
- Given the Matrix output is too generic, when RSCS evaluation runs, then it fails specificity and must be regenerated.

**Technical Notes:** Implement `MatrixOfEdgingBrief` and DSPy program with RSCS evaluation. Preserve input artifact hashes and output receipt.

**Legacy and Primitive Mapping:** Matrix of Edging, RSCS Law 2 collision, cognitive primitives. Active families: TRG, PSY, HUM, PER.

**Prerequisites:** Stories 5.1 and 5.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
