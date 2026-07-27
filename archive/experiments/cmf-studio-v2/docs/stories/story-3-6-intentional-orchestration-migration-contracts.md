---
story_id: "3.6"
story_title: "Intentional Orchestration Migration Contracts"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-03.09"
pipeline_stage: "0"
entry_object: "orchestration-bearing module"
exit_object: "`LegacyOrchestrationIntentRecord`"
validation_contract: "organism layer and proof obligations"
required_receipt: "orchestration intent receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 3.6: Intentional Orchestration Migration Contracts

**Epic:** 3 - Legacy Intelligence and JIT Skill Governance
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-03.09 |
| Canonical Pipeline Stage | 0 |
| Entry Object | orchestration-bearing module |
| Exit Object | `LegacyOrchestrationIntentRecord` |
| Validation Contract | organism layer and proof obligations |
| Required Receipt | orchestration intent receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Preserve the high-value legacy intelligence and its intentional orchestration logic as typed, evaluated, Python-first assets while blocking direct legacy runtime dependency and stale stack assumptions.

**Covers:** FR-CMF-03.01 through FR-CMF-03.09.

**User Value:** Migration Stewards and AI agents can recover the depth of CCP/CMF intelligence while production remains clean, typed, testable, and greenfield.

**Technical Context:** `/api/v1/legacy-migration`, `/api/v1/registries`, MigrationWorkflow, `legacy_inventory_items`, `migration_ledger_entries`, `legacy_orchestration_intent_records`, `migrated_registry_entries`, `fixture_sets`, `evaluation_targets`, DSPy programs, CI import gate.

**CBAR Failure Scenario:** If legacy intelligence is flattened into prompts, CMF loses its edge. If legacy runtime is imported directly, the greenfield architecture inherits fragmentation. The resolution is typed migration plus explicit compiler/eval targets.

## Story Definition

As a Migration Steward, I want every orchestration-bearing legacy module to preserve why it exists and how it coordinates the system, so that CCF/CMF intelligence does not get flattened into disconnected prompts or feature labels.

**Acceptance Criteria:**

- Given a legacy CCF or CMF module is marked for migration, when the Steward creates its migration record, then the record must include product purpose, organism layer, upstream inputs, emitted packets, downstream consumers, required gates, failure modes, and proof obligations.
- Given a migrated module claims to support CRAL, Context Premise, Emotional DNA, Voice DNA, primitive coalitions, SVRE, scene containers, creative subsystems, or asset roles, when activation is requested, then it must cite the source document and expose a typed contract or registry target.
- Given a module is only summarized as style advice, vibes, or a prompt snippet, when activation is requested, then it is blocked until its orchestration role is made explicit.
- Given two legacy modules claim overlapping authority, when migration review runs, then the Steward must resolve whether each belongs to DNA/truth, RNA/transcription, force, delivery, variation, phenotype, evaluation, or outer learning.
- Given the orchestration intent passes review, when a downstream story or tech spec references the module, then it can cite the `LegacyOrchestrationIntentRecord` and inherit its gates.

**Technical Notes:** Add `LegacyOrchestrationIntentRecord` with organism layer enum, input/output packet references, gate references, downstream artifact references, failure modes, source links, and reviewer status. MigrationWorkflow activation requires this record for orchestration-bearing modules.

**Legacy and Primitive Mapping:** PRD-02 CCF, PRD-03 CMF, PRD-08 Conscious Primitives, CCP Biological Orchestration Model, CSIP v3, CRAL, SVRE, CMF Master Scene Intelligence. Active families: STR, PSY, VSG, VOC, SAF, FBK.

**Prerequisites:** Stories 3.1 through 3.5.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
