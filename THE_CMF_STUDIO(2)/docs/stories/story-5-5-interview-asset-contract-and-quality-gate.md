---
story_id: "5.5"
story_title: "Interview Asset Contract and Quality Gate"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-05.05"
  - "FR-CMF-05.06"
  - "FR-CMF-05.07"
pipeline_stage: "4"
entry_object: "preparation artifacts"
exit_object: "`InterviewAssetContract`, deck"
validation_contract: "routeability and expression/archetype separation"
required_receipt: "contract compilation receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 5.5: Interview Asset Contract and Quality Gate

**Epic:** 5 - Interview Intelligence and Narrative State Induction
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-05.05, FR-CMF-05.06, FR-CMF-05.07 |
| Canonical Pipeline Stage | 4 |
| Entry Object | preparation artifacts |
| Exit Object | `InterviewAssetContract`, deck |
| Validation Contract | routeability and expression/archetype separation |
| Required Receipt | contract compilation receipt |
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

As an Operator, I want Interview Asset Contracts with target expression state, archetype route, asset derivative, edge product, anchors, repair followups, CMF route, and evaluation logic, so that the session has routeable production intent without becoming a script.

**Acceptance Criteria:**

- Given approved interview preparation artifacts exist, when an Interview Asset Contract is compiled, then each content-intended question includes target expression state, target archetype, asset derivative, edge product, first-line anchor, depth anchor, repair followups, CMF route, and evaluation logic.
- Given an expression state is confused with an output archetype, when the quality gate runs, then the contract is rejected with a correction note.
- Given a contract lacks saturation context, collision strength, specificity, or routeability, when evaluation runs, then it cannot be approved for session use.
- Given the Operator approves a contract, when the Complete Expression Session is created, then the contract ID is bound to the session.
- Given a later extraction uses the contract, when Expression Moments are reviewed, then induction context is visible.

**Technical Notes:** Implement `InterviewAssetContract`, `InterviewDeck`, `InterviewPlanEvaluationReceipt`, and `InterviewAssetContractCompiled` event.

**Legacy and Primitive Mapping:** V9.1 Interview Asset Contract doctrine, Archetype Migration Proposition, RSCS 4 laws. Active families: STR, TRG, PSY, FBK.

**Prerequisites:** Stories 5.1 through 5.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
