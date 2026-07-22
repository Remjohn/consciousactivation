---
story_id: "11.8"
story_title: "ADK and Agents CLI Adapter Export Drift Gate"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.07"
  - "PRD-CMF-02.04"
pipeline_stage: "adapter/export overlay"
entry_object: "approved agent role spec"
exit_object: "generated ADK/Agents CLI adapter"
validation_contract: "generated-only adapter and drift gate"
required_receipt: "adapter export receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.8: ADK and Agents CLI Adapter Export Drift Gate

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Story Definition

As an Architect, I want Google ADK and Agents CLI adapters generated from CMF contracts, so that external agent runtimes help deployment without becoming the source of truth.

**Acceptance Criteria:**

- Given an AgentRoleSpec is approved, when ADK export runs, then the generated adapter includes name, description, tools, sub-agents, callbacks, and handoff hints derived from CMF contracts.
- Given a generated adapter is edited by hand, when drift check runs, then the adapter is marked non-canonical and export must be regenerated.
- Given an ADK callback maps to a CMF Hook, when exported, then the hook remains governed by CMF lifecycle and receipt rules.
- Given an ADK tool maps to a CMF ToolCapabilitySpec, when exported, then it cannot bypass Pydantic input/output or Command Bus mutation rules.
- Given Agents CLI deployment scaffolding is generated, when reviewed, then it cites the originating CMF role spec and readiness receipt.

**Technical Notes:** Add adapter export records, generated file hashes, drift checks, ADK/Agents CLI metadata, and read-only generated adapter folders.

**Legacy and Primitive Mapping:** Learns from Google agent config discipline without replacing BMAD, Pydantic contracts, Pi harness rules, or CMF receipt authority. Active families: SAF, BUS.

**Prerequisites:** Stories 11.1 through 11.7.

## Tech Spec Handoff Requirements

- Define generated adapter outputs, hash receipts, drift checks, and adapter export review.
- Include tests that hand-authored adapter changes are detected and that generated adapters cannot become product requirement authority.
