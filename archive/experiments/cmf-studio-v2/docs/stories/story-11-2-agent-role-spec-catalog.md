---
story_id: "11.2"
story_title: "Agent Role Spec Catalog"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.01"
  - "PRD-CMF-02.03"
  - "PRD-CMF-02.05"
pipeline_stage: "agent-factory overlay"
entry_object: "department and production responsibility"
exit_object: "`AgentRoleSpec` catalog"
validation_contract: "goal, active object, tool, memory, eval, receipt completeness"
required_receipt: "agent role spec receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.2: Agent Role Spec Catalog

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| Module Requirement IDs | PRD-CMF-10.01, PRD-CMF-02.03, PRD-CMF-02.05 |
| Canonical Pipeline Stage | agent-factory overlay |
| Entry Object | department and production responsibility |
| Exit Object | `AgentRoleSpec` catalog |
| Validation Contract | goal, active object, tool, memory, eval, receipt completeness |
| Required Receipt | agent role spec receipt |
| Source PRD Module | `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` |
| Source Agent Registry | `docs/cmf-studio-agent-factory-registry.md` |

## Epic Context

**Epic Goal:** Create accountable agent role contracts rather than loose prompt personas.

**CBAR Failure Scenario:** If an agent has a name but no active object, tool boundary, memory policy, or receipt obligation, it can act outside the pipeline. The resolution is `AgentRoleSpec` completeness and readiness gating.

## Story Definition

As a Builder, I want each Agent to have an `AgentRoleSpec`, so that the system knows its goal, responsibility, active objects, tools, memory, skills, evals, blocked actions, and receipts.

**Acceptance Criteria:**

- Given an Agent is added to the Factory, when saved, then it must include persona code, display name, department, goal, fit rationale, entry objects, exit objects, allowed tools, skills, sub-agent bindings, hooks, evals, memory policy, blocked actions, and receipt obligations.
- Given an AgentRoleSpec is activated, when runtime invocation is requested, then it must resolve through `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentActionRequest`, and `PiAgentGateway`.
- Given an Agent implementation is a DSPy program, deterministic service, ADK adapter, workflow activity, provider worker, or human queue, when it runs, then it must still bind to the same `AgentRoleSpec` and receipt obligations.
- Given an Agent lacks active object scope, when activation is requested, then activation is blocked.
- Given an Agent has tool access without a permission and receipt obligation, when readiness eval runs, then it fails.
- Given an Agent tries to write canonical state outside the Command Bus or approved workflow command, when gateway or static guard runs, then the action is blocked.
- Given an Agent owns a pipeline stage, when inspected, then the UI and docs show the stage, entry object, exit object, validation contract, and required receipt.
- Given `ORC-PIORCHS-AG` is active, when it proposes work, then it acts only through the Agent Gateway and Command Bus.

**Technical Notes:** Add `AgentRoleSpec`, `DepartmentSpec`, activation state, readiness eval link, generated adapter hash, repository/service methods, validation gates, runtime invocation checks, and seed records from the persona registry.

**Legacy and Primitive Mapping:** Applies BMAD/ERA3 discipline to runtime agents instead of document-only personas. Active families: SAF, BUS.

**Prerequisites:** Story 11.1.

## Tech Spec Handoff Requirements

- Include source receipts for PRD-CMF-10, Agent Factory registry, Intelligence Contract, architecture, pipeline map, and this story.
- Define `AgentRoleSpec`, `DepartmentSpec`, role registry service, activation checks, runtime invocation path, adapter binding fields, receipt models, and tests.
- Include gateway and Command Bus boundary tests for `ORC-PIORCHS-AG`.
