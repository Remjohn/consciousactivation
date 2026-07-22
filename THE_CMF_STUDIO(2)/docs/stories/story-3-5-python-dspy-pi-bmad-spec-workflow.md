---
story_id: "3.5"
story_title: "Python/DSPy/Pi BMad Spec Workflow"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-03.07"
pipeline_stage: "spec-governance overlay"
entry_object: "epic/story/spec request"
exit_object: "`SpecAuditReceipt`"
validation_contract: "files-read, FR trace, pipeline trace, CBAR"
required_receipt: "spec audit receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 3.5: Python/DSPy/Pi BMad Spec Workflow

**Epic:** 3 - Legacy Intelligence and JIT Skill Governance
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-03.07 |
| Canonical Pipeline Stage | spec-governance overlay |
| Entry Object | epic/story/spec request |
| Exit Object | `SpecAuditReceipt` |
| Validation Contract | files-read, FR trace, pipeline trace, CBAR |
| Required Receipt | spec audit receipt |
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

As a PM, Architect, or Tech Writer agent, I want the legacy BMAD and ERA3 writing workflows adapted to Python, Pydantic, DSPy, Pi, CBAR, and CMF greenfield constraints, so that PRDs, epics, architecture, stories, and tech specs stay implementation-grounded.

**Acceptance Criteria:**

- Given a tech spec workflow starts, when the `TechSpecCompilerWorkflow` opens, then it must link to an approved epic/story and create a `TechSpecWorkflow` record.
- Given source context is gathered, when the compiler runs, then it records `FilesReadReceipt` entries for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, and feature-specific CMF/CCF source docs.
- Given traceability is compiled, when validation runs, then the spec includes `RequirementTrace` entries for FR-CMF IDs and `PipelineStageTrace` entries naming stage, entry object, exit object, validation contract, receipt, and allowed actor/service.
- Given implementation context is drafted, when the spec is produced, then the old "Existing Backend Integration" section is replaced with "Greenfield Integration and Legacy Migration Context" listing Pydantic contracts, commands, events, services, durable workflows, DSPy programs, JIT skills, legacy source paths, provider boundaries, renderer boundaries, projection boundaries, and tests.
- Given a spec references the old stack incorrectly, when audit runs, then it is blocked until updated for Python-first Harness, Pydantic contracts, DSPy programs, Pi orchestration, durable workflows, and TypeScript leaf boundaries.
- Given CBAR is applied, when audit runs, then the spec must include tension, failure scenario, resolution demand, and downstream proof tied to tests or receipts.
- Given RSCS is applied, when a recommendation or story detail is included, then it must require project-specific context to verify.
- Given audit completes, when the workflow closes, then it writes a `SpecAuditReceipt` with accepted, revision_requested, or blocked status.

**Technical Notes:** Model `SpecWritingProtocol`, `TechSpecWorkflow`, `TechSpecSourcePacket`, `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, `CBARCheck`, `SpecAuditReceipt`, `EpicStoryCompiler`, `TechSpecCompiler`, `TechSpecAuditor`, `RequirementTraceCompiler`, and `CBARAuditor`. Tests live under `tests/spec_governance`.

**Legacy and Primitive Mapping:** ERA3 Epic and Story Writing Protocol, ERA3 Tech Spec Writing Protocol, PROMPT_Spec_Build, PROMPT_Spec_Audit, CBAR story adaptation. Active families: STR, SAF, FBK.

**Prerequisites:** Stories 3.1 through 3.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
