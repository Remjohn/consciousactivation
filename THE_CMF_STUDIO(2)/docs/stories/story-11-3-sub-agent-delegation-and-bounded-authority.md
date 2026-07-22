---
story_id: "11.3"
story_title: "Sub-Agent Delegation and Bounded Authority"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.02"
  - "PRD-CMF-02.03"
  - "PRD-CMF-02.05"
pipeline_stage: "agent-factory overlay"
entry_object: "parent agent and specialist task"
exit_object: "`SubAgentRoleSpec` binding"
validation_contract: "bounded authority and parent-stage compatibility"
required_receipt: "sub-agent binding receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.3: Sub-Agent Delegation and Bounded Authority

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Story Definition

As an Agent owner, I want sub-agents to have bounded specialist contracts, so that narrow expertise can help without expanding authority beyond the parent stage.

**Acceptance Criteria:**

- Given a Sub-Agent is bound to an Agent, when saved, then it must include parent agent, invocation conditions, input contract, output contract, blocked actions, proof obligation, and receipt.
- Given a SubAgentRoleSpec is invoked, when execution starts, then it must cite parent `AgentRoleSpec`, parent orchestration run, parent stage plan, bounded input model, and expected output model.
- Given a Sub-Agent tries to mutate canonical state directly, when the gateway checks authority, then the action is blocked.
- Given a Sub-Agent needs a tool, when validation runs, then the tool must be listed in the sub-agent spec and compatible with the parent stage validation contract.
- Given a Sub-Agent output is used downstream, when the handoff packet is created, then it includes source evidence, parent stage, and sub-agent receipt.
- Given a Sub-Agent result should change production state, when the result is accepted, then the parent Agent must route it through the normal command, workflow, review, or evaluation path.
- Given `RES-EVDCRIT-SA` critiques evidence, when its output is consumed by `RES-CTXPRMS-AG`, then the Context Premise receipt cites the critique.
- Given `SCN-CMPDIRC-SA` analyzes an Ideogram plate, when render proceeds, then its output cannot override final text or identity authority.

**Technical Notes:** Add `SubAgentRoleSpec`, parent compatibility checks, bounded input/output models, sub-agent tool subset validation, sub-agent receipts, and handoff packet integration.

**Legacy and Primitive Mapping:** Protects specialized legacy lenses such as evidence critic, anti-centroid critic, visual candidate scorer, and composition inspector from becoming uncontrolled agents. Active families: SAF, FBK, VSG.

**Prerequisites:** Stories 1.6, 11.1, 11.2.

## Tech Spec Handoff Requirements

- Include `RequirementTrace` for PRD-CMF-10.02 and PRD-CMF-02.05.
- Define sub-agent invocation, parent binding, bounded I/O contracts, tool subset validation, authority checks, and receipt models.
- Include tests that sub-agents cannot bypass parent authority or mutate canonical state directly.
