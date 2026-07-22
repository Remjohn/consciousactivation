---
story_id: "3.4"
story_title: "Legacy Import, Hidden Prompt, and Template Gates"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-03.06"
pipeline_stage: "0 / all stages"
entry_object: "import/template/spec reference"
exit_object: "blocked or approved reference"
validation_contract: "greenfield rule and template hash"
required_receipt: "gate failure or approval receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 3.4: Legacy Import, Hidden Prompt, and Template Gates

**Epic:** 3 - Legacy Intelligence and JIT Skill Governance
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-03.06 |
| Canonical Pipeline Stage | 0 / all stages |
| Entry Object | import/template/spec reference |
| Exit Object | blocked or approved reference |
| Validation Contract | greenfield rule and template hash |
| Required Receipt | gate failure or approval receipt |
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

As an Architect or reviewer, I want build and workflow gates to reject direct legacy imports, hidden prompt stacks, duplicate registries, and unapproved provider templates, so that the greenfield runtime stays clean.

**Acceptance Criteria:**

- Given production code imports a legacy runtime module directly, when CI runs, then the build fails with `LEGACY_IMPORT_BLOCKED` and points to the migration ledger target.
- Given an agent tries to use an unapproved prompt stack, when the workflow gate runs, then the action is blocked until the prompt is migrated into a typed compiler or registry.
- Given duplicate registry truths exist, when activation is requested, then the system requires conflict resolution before either entry can influence production.
- Given a ComfyUI template lacks approved hash or compatibility notes, when a worker job references it, then the provider route is blocked.
- Given a TypeScript-first assumption appears in a tech spec or story, when review runs, then it is flagged unless it is a permitted leaf runtime.

**Technical Notes:** Add static import checks, registry conflict checks, provider template hash checks, and spec-review checks. Store failures as evaluation receipts and migration review events.

**Legacy and Primitive Mapping:** Legacy Inventory greenfield rule; ERA3/PROMPT audit protocols. Active families: SAF, BUS.

**Prerequisites:** Stories 3.1 through 3.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
