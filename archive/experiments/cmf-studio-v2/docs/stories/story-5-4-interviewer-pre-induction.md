---
story_id: "5.4"
story_title: "Interviewer Pre-Induction"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-05.04"
pipeline_stage: "4"
entry_object: "session plan"
exit_object: "`PreInductionPlan`"
validation_contract: "anti-centroid and manipulation gate"
required_receipt: "pre-induction receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 5.4: Interviewer Pre-Induction

**Epic:** 5 - Interview Intelligence and Narrative State Induction
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-05.04 |
| Canonical Pipeline Stage | 4 |
| Entry Object | session plan |
| Exit Object | `PreInductionPlan` |
| Validation Contract | anti-centroid and manipulation gate |
| Required Receipt | pre-induction receipt |
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

As an Operator, I want to run interviewer pre-induction before the session, so that I can guide the guest into authentic expression without scripting or manipulation.

**Acceptance Criteria:**

- Given a session plan exists, when pre-induction opens, then the Operator sees authentic curiosity prompts, emotional bridges, questions to avoid, guest-specific resonance, and opening state.
- Given a proposed question would produce a safe centroid answer, when the pre-session gate evaluates it, then the system flags the risk and recommends a collision-bearing route.
- Given the Operator edits a question, when it is saved, then the system preserves the source evidence and induction rationale.
- Given a prompt crosses into manipulation or scripted performance, when review runs, then it is blocked or marked for rewrite.
- Given pre-induction completes, when the session starts, then live guidance references the approved plan without replacing the Operator's judgment.

**Technical Notes:** Implement `InterviewerResonanceContext`, `PreInductionPlan`, and PWA Interview Intelligence Studio state. The output feeds Live Interview Mode.

**Legacy and Primitive Mapping:** V9 activation/articulation doctrine, TTT transition grammar, RSCS. Active families: PRS, PSY, SAF, HUM.

**Prerequisites:** Stories 5.1 through 5.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
