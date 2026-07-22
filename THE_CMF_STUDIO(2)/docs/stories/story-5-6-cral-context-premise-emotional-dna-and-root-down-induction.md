---
story_id: "5.6"
story_title: "CRAL, Context Premise, Emotional DNA, and Root-Down Induction"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-05.08"
pipeline_stage: "3 / 4"
entry_object: "CRAL/context/DNA evidence"
exit_object: "`InductionRationale`"
validation_contract: "supported psychology and root-down evidence"
required_receipt: "induction rationale receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 5.6: CRAL, Context Premise, Emotional DNA, and Root-Down Induction

**Epic:** 5 - Interview Intelligence and Narrative State Induction
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-05.08 |
| Canonical Pipeline Stage | 3 / 4 |
| Entry Object | CRAL/context/DNA evidence |
| Exit Object | `InductionRationale` |
| Validation Contract | supported psychology and root-down evidence |
| Required Receipt | induction rationale receipt |
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

As an Operator, I want each planned interview move to expose the CRAL signal, Context Premise, Emotional DNA or Voice DNA rationale, and intended extraction outcome, so that Narrative State Induction is intentional rather than a polished question list.

**Acceptance Criteria:**

- Given CRAL/SCRE research is available, when a Research Field is promoted into interview preparation, then the system preserves the relevant, believable, undeniable, resonant, surprising, irrefutable, and relatable signal roles that support the planned session.
- Given audience evidence is sufficient, when Context Premise compilation runs, then it emits an Audience Deep Trigger Map with depth mode, hermeneutical gaps, moral-emotional vectors, coping trajectory, regulatory focus when available, confidence, and gaps.
- Given guest or coach source material is available, when Emotional DNA and Voice DNA extraction runs, then the output distinguishes belief content, construction mechanics, emotional path, negative space, suppression markers, escalation triggers, and normative expression targets.
- Given a proposed interview move is displayed, when the Operator inspects it, then the system shows CRAL evidence, Context Premise link, Emotional DNA or Voice DNA rationale when available, Matrix of Edging position, target expression state, and intended asset extraction outcome.
- Given the system lacks enough evidence for an Emotional DNA or full-depth Context Premise claim, when it compiles the plan, then it marks the rationale as partial, uses the appropriate shallow mode, and prevents unsupported psychological certainty.

**Technical Notes:** Implement or extend `CRALFinding`, `ContextPremise`, `AudienceDeepTriggerMap`, `EmotionalDNAProfile`, `VoiceDNAProfile`, `InductionRationale`, and DSPy programs for CRAL research, Context Premise, Emotional DNA extraction, Voice DNA compilation, and interview move explanation.

**Legacy and Primitive Mapping:** Sovereign CRAL, Context Premise Engine proposals, CSIP v3 Voice/Emotional DNA, Voice DNA Framework, Matrix of Edging, PRD-02 CCF, PRD-08 primitives. Active families: PSY, STR, TRG, VOC, PRS, SAF.

**Prerequisites:** Stories 5.1 through 5.5 and Story 3.6.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
