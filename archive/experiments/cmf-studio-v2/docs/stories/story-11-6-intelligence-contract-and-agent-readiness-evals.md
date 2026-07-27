---
story_id: "11.6"
story_title: "Intelligence Contract and Agent Readiness Evals"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.06"
pipeline_stage: "agent-factory overlay"
entry_object: "agent intelligence profile"
exit_object: "`AgentReadinessEval`"
validation_contract: "standards, primitives, tools, memory, evals, receipts, blocked actions"
required_receipt: "readiness eval receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.6: Intelligence Contract and Agent Readiness Evals

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Story Definition

As an Owner, I want every intelligence entity evaluated before activation, so that standards, primitives, rules, tools, memory, skills, and receipts govern its behavior.

**Acceptance Criteria:**

- Given an AgentRoleSpec is submitted, when readiness eval runs, then it checks constitutions, standards, primitives, deterministic rules, protocols, tools, memory access, skills, evals, receipts, and blocked actions.
- Given an Agent lacks primitive obligations for a quality-critical task, when readiness eval runs, then activation is blocked or revision-required.
- Given memory access is broader than the active object allows, when readiness eval runs, then activation is blocked.
- Given eval obligations are missing, when an Agent handles review, routing, extraction, or rendering, then readiness eval fails.
- Given readiness passes, when the Agent activates, then the versioned readiness receipt is linked to its role spec.

**Technical Notes:** Add `AgentReadinessEval`, readiness receipts, primitive obligation checks, memory policy checks, and review UI.

**Legacy and Primitive Mapping:** Makes primitives the production quality standard for agent behavior, not just output scoring. Active families: SAF, FBK, PER, BUS.

**Prerequisites:** Stories 3.2, 9.1, 10.1, 11.2.

## Tech Spec Handoff Requirements

- Define readiness eval target selection, primitive obligations, memory policy checks, pass/fail states, and receipts.
- Include eval fixtures for missing primitives, overbroad memory, missing blocked actions, and missing receipt obligations.
