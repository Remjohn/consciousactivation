---
story_id: "11.7"
story_title: "Pi Harness Tool Registry and Department Runtime"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.08"
  - "PRD-CMF-02.04"
  - "PRD-CMF-02.05"
pipeline_stage: "all stages"
entry_object: "Pi action and tool need"
exit_object: "`ToolCapabilitySpec`, department runtime registry"
validation_contract: "Pydantic I/O, role scope, idempotency, receipt obligation"
required_receipt: "tool registration receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.7: Pi Harness Tool Registry and Department Runtime

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Story Definition

As Pi Orchestrator, I need explicit tools registered per department, so that I can coordinate the Factory without relying on built-in or hidden capabilities.

**Acceptance Criteria:**

- Given a tool is registered, when Pi requests it, then the tool must expose Pydantic input/output, department scope, allowed stages, role policy, idempotency rule, receipt obligation, and failure behavior.
- Given Pi requests a tool outside the active stage or role, when the Agent Gateway evaluates the request, then it is blocked.
- Given a department has no registered tool for a required action, when Pi reaches that stage, then it creates a human handoff or blocker rather than inventing a tool.
- Given a tool mutates state, when executed, then the mutation goes through the Command Bus and writes a receipt.
- Given a provider or renderer tool is called, when it returns, then provider metadata, cost, retry state, and output hashes are preserved.

**Technical Notes:** Add `ToolCapabilitySpec`, department runtime registry, tool gateway checks, and Pi action validation.

**Legacy and Primitive Mapping:** Implements the correction that Pi has no built-in CMF production tools; every capability must be built, scoped, and receipt-backed. Active families: SAF, BUS, FRC.

**Prerequisites:** Stories 1.1, 1.6, 8.1, 11.2.

## Tech Spec Handoff Requirements

- Define tool capability model, department runtime registry, gateway enforcement, idempotency, receipt obligations, and missing-tool handoff behavior.
- Include tests that Pi cannot invent tools or bypass Command Bus mutations.
