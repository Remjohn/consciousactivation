---
story_id: "11.1"
story_title: "Persona Code Registry and Validation"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.00"
pipeline_stage: "agent-factory overlay"
entry_object: "department and entity naming request"
exit_object: "persona code registry"
validation_contract: "`DDD-XXXXXXX-TT` code validation"
required_receipt: "persona registry receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.1: Persona Code Registry and Validation

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| Module Requirement IDs | PRD-CMF-10.00 |
| Canonical Pipeline Stage | agent-factory overlay |
| Entry Object | department and entity naming request |
| Exit Object | persona code registry |
| Validation Contract | `DDD-XXXXXXX-TT` code validation |
| Required Receipt | persona registry receipt |
| Source PRD Module | `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` |
| Source Agent Registry | `docs/cmf-studio-agent-factory-registry.md` |
| Source Intelligence Contract | `docs/cmf-studio-agent-intelligence-contract.md` |

## Epic Context

**Epic Goal:** Create the traceable Agent Factory layer that names every agent, sub-agent, hook, extension, skill, registry, and eval with a compact persona code, binds each entity to a production responsibility, and prevents agents from becoming loose prompt personas.

**User Value:** Operators and builders can tell exactly what each intelligence entity serves, which department owns it, what it can do, what it cannot do, and which receipt proves its work.

**CBAR Failure Scenario:** If agents are named poetically but not operationally, the Factory becomes impossible to audit. The resolution is a strict `DDD-XXXXXXX-TT` persona code and registry validation.

## Story Definition

As an Operator-builder, I want every Factory entity to use a compact persona code, so that logs, receipts, UI filters, specs, and agent configs reveal exactly what the entity serves.

**Acceptance Criteria:**

- Given an agent, sub-agent, hook, extension, skill, registry, or eval is registered, when its code is validated, then it must match `DDD-XXXXXXX-TT`.
- Given the middle segment is not exactly seven characters, when registration runs, then the entity is rejected.
- Given the type segment is not a known two-character entity type, when registration runs, then the entity is rejected.
- Given a code uses only a poetic persona name and not a service role, when review runs, then the reviewer must request a service-revealing code.
- Given `RES-VISRSCH-AG` is registered, when the registry renders it, then it resolves to Visual Research Agent / Aurore and its service scope.

**Technical Notes:** Implement persona code schema, department code enum, entity type enum, uniqueness check, and registry validation.

**Legacy and Primitive Mapping:** Preserves intentional orchestration traceability from old CCF/CMF modules. Active families: SAF, BUS, FBK.

**Prerequisites:** Stories 1.1, 1.6, 3.6.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for the PRD, PRD-CMF-10, architecture, pipeline map, Agent Factory registry, this story file, and Legacy Inventory.
- Include `RequirementTrace` for PRD-CMF-10.00.
- Include `PipelineStageTrace` for the agent-factory overlay stage.
- Define Pydantic models, validation rules, seed data, tests, receipts, and UI/read-model requirements.
- Include CBAR proof that persona codes prevent untraceable prompt-persona drift.
