---
tech_spec_id: "TS-CMF-122"
title: "Stage Director Skill Contract Binding"
story_id: "13.3"
story_title: "Stage Director Skill Contract Binding"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.03"
pipeline_stage: "agent and skill orchestration"
entry_object: "StageDirectorSkillDraft"
exit_object: "StageSkillInvocationReceipt"
validation_contract: "typed skill contract, allowed scope, source artifacts, output schema, review blockers, receipt chain"
required_receipt: "StageSkillInvocationReceipt"
runtime_target: "Python / Pydantic v2 / AgentRoleSpec / SKILL contracts / DSPy / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-122: Stage Director Skill Contract Binding

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory format and CBAR requirements. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 mandates for routing, rejection, and intelligence-gated execution. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_10_Agents_SubAgents_Hooks_Extensions_Skills.md` | Agent, sub-agent, hook, extension, and skill definitions. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.03. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | JIT skill compiler precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-081-agent-definition-runtime-architecture-and-registry.md` | Agent runtime architecture dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-121-production-pipeline-manifest-registry.md` | Stage manifest dependency. |
| `THE CMF STUDIO/src/ccp_studio/contracts/skills.py` | Existing skill contracts. |
| `THE CMF STUDIO/src/ccp_studio/repositories/skill_invocation_records.py` | Existing invocation persistence. |
| `THE CMF STUDIO/src/ccp_studio/services/jit_skill_compiler_service.py` | Existing JIT skill service to preserve and extend. |
| `THE CMF STUDIO/src/ccp_studio/services/agent_factory_service.py` | Existing agent factory owner. |
| `THE CMF STUDIO/src/ccp_studio/services/command_bus.py` | Invocation command dispatch owner. |
| `OpenMontage AGENT_GUIDE.md` | Reference pattern for stage director skills and agent operating rules. |

## 2. Overview

OpenMontage uses readable director skills to guide stage execution. CMF needs the readability but not untyped prompt authority. This spec converts stage director instructions into `StageDirectorSkillSpec` contracts that agents, sub-agents, DSPy programs, deterministic services, and human queues can invoke through the Command Bus.

A stage director skill is not a free prompt and cannot mutate canonical state directly. It declares pipeline stage, active object scope, required context bundle, required primitives, approved tools, source artifacts, output schema, review criteria, blocker types, and receipt type. Every invocation writes a `StageSkillInvocationReceipt` with skill version, input object hashes, agent or service identity, requested tool calls, outputs, review state, blockers, and downstream command refs.

The spec also preserves the distinction Emilio emphasized: stable operational skills are not the same as JIT skills. JIT skills remain specialized compilers for interview engineering, narrative induction, expression extraction, contrastive prompting, visual prompt shaping, and eval interpretation. Stage director skills may call JIT skills only through typed contracts.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-122-001 | `StageDirectorSkillSpec` | Typed contract for stage operating instructions and boundaries. |
| DEP-CMF-122-002 | `StageSkillContextBundle` | Source-grounded context packet with object hashes, primitives, doctrines, and allowed memory. |
| DEP-CMF-122-003 | `StageSkillInvocationCommand` | Command Bus object for invoking a stage skill. |
| DEP-CMF-122-004 | `StageSkillOutputEnvelope` | Typed output with canonical object proposals, blockers, and review notes. |
| DEP-CMF-122-005 | `StageSkillInvocationReceipt` | Receipt proving skill identity, scope, inputs, tools, outputs, and review state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/skills.py` | Add stage director skill spec, context bundle, invocation command, output envelope, and receipt models. |
| `src/ccp_studio/services/jit_skill_compiler_service.py` | Expose JIT skill outputs as typed dependencies, not hidden prompt text. |
| `src/ccp_studio/services/agent_factory_service.py` | Bind AgentRoleSpec/Agent runtime permissions to allowed stage skills. |
| `src/ccp_studio/services/command_bus.py` | Dispatch stage skill invocation commands and record command refs. |
| `src/ccp_studio/repositories/skill_invocation_records.py` | Persist invocation receipts and output envelopes. |
| `src/ccp_studio/services/approval_gate_service.py` | Block skills with undocumented behavior, missing source refs, or scope expansion. |
| `src/ccp_studio/api/v1/roles.py` | Add read endpoints for skill binding to agents and sub-agents. |
| `POST /api/v1/roles/stage-skills`, `POST /api/v1/roles/stage-skills/{skill_id}/invoke`, `GET /api/v1/roles/stage-skills/{skill_id}` | Exact API routes for skill registration, invocation, and inspection. |
| Postgres tables: `stage_director_skill_specs`, `stage_skill_invocation_receipts`, `skill_output_envelopes`, `approval_blockers` | Durable storage for registered skill contracts, invocations, outputs, and blocked calls. |
| `THE CMF STUDIO/registries/skills/` | New registry namespace for stable stage director skill specs. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PER-003` | Intelligence-Gated Intercept | Skill invocation must use scoped context and cannot invent missing intelligence. |
| `EXP-PRG-001` | Inline Routing SLA | Skill routing resolves through manifest and AgentRoleSpec before execution. |
| `EXP-FBK-001` | Actionable Rejection | Skill blockers name missing scope, input, primitive, output schema, or approval. |
| `EXP-SOC-001` | Verifiable Artifact | Every invocation is hash-backed and replayable. |
| `EXP-FRC-006` | Frictionless Block | Skill failures return next command, not vague failure prose. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Skill cannot run without a complete scoped context bundle. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Manifest stage resolves the skill spec and allowed tools before invocation. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Invocation failures return blocker code and repair command. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Invocation receipt stores input/output hashes and review result. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Stage skills cannot mutate canonical objects directly. | Keeps canonical writes behind services, gates, and receipts. |
| JIT skills are callable dependencies, not stage directors by default. | Preserves specialized extraction and narrative induction compilers. |
| Skill text is versioned and hash-backed. | Prevents hidden prompt drift. |
| Invocation receipts include agent/service identity. | Makes responsibility auditable across agents and sub-agents. |

## 4. Implementation Plan

1. Extend `contracts/skills.py` with stage director skill contracts and invocation receipts.
2. Add skill registry loader for stable stage director skill specs under `registries/skills/`.
3. Add command handler for `StageSkillInvocationCommand`.
4. Connect manifest stage specs from TS-CMF-121 to stage skill refs and allowed tool refs.
5. Bind AgentRoleSpec permissions to allowed stage skills and object scopes.
6. Add gate that blocks hidden prompt text, missing output schema, missing source artifacts, and scope expansion.
7. Add typed bridge for JIT skill compiler outputs when stage skills call extraction, narrative induction, or interview engineering skills.
8. Add review read model showing invoked skill, object scope, blockers, outputs, and downstream actions.
9. Emit invocation receipts for every run.
10. Add tests for scope, schema, hidden prompt, JIT bridge, and replay behavior.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class StageDirectorSkillSpec(BaseModel):
    schema_version: Literal["cmf.stage_director_skill.v1"]
    skill_id: str
    skill_name: str
    skill_kind: Literal["stable_operational", "jit_compiler", "reviewer", "human_queue"]
    version: str
    pipeline_stage_id: str
    allowed_object_scope: list[str]
    required_context_refs: list[str]
    required_primitive_ids: list[str]
    allowed_tool_refs: list[str] = Field(default_factory=list)
    output_schema_ref: str
    blocker_types: list[str]
    receipt_type: str
    skill_body_sha256: str


class StageSkillInvocationReceipt(BaseModel):
    schema_version: Literal["cmf.stage_skill_invocation_receipt.v1"]
    receipt_id: str
    skill_id: str
    skill_version: str
    manifest_snapshot_id: str
    stage_id: str
    invoker_id: str
    input_object_hashes: dict[str, str]
    tool_call_refs: list[str] = Field(default_factory=list)
    output_envelope_hash: str
    review_status: Literal["accepted", "needs_revision", "blocked"]
    blocker_codes: list[str] = Field(default_factory=list)
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing JIT skill compiler behavior continues for current interview engineering and extraction tasks until stage director specs consume it through typed bridges. Existing agents may continue using current role policies, but any new production pipeline stage defined by TS-CMF-121 must invoke only registered stage director skills.

If a stage skill is missing, hidden, or unversioned, the workflow blocks at stage dispatch and returns a repair command: register skill, attach output schema, bind allowed scope, or assign a human queue. It must not fall back to untracked prompt text.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T122-01 | Contracts | Add stage skill spec, context bundle, command, output envelope, receipt. |
| T122-02 | Registry | Add `registries/skills/` loader and seed specs. |
| T122-03 | Command Bus | Add stage skill invocation handler. |
| T122-04 | Agents | Bind AgentRoleSpec to stage skills and scopes. |
| T122-05 | JIT Skills | Add typed bridge from JIT compiler outputs to stage output envelopes. |
| T122-06 | Review UI | Add invocation read model and blocker surface. |
| T122-07 | Tests | Add schema, scope, hidden prompt, JIT bridge, and replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC122-01 | Every stage skill has allowed object scope, output schema, source refs, and receipt type. | Skill contains prose instructions but no typed output schema. | Phase4-M01; skill schema test. |
| AC122-02 | Stage skills cannot expand authority beyond manifest stage contract. | Visual research skill writes final approval status. | Phase4-M03; scope gate test. |
| AC122-03 | Hidden prompt text blocks production use. | Agent invokes an undocumented local prompt file. | Phase4-M05; hidden prompt gate test. |
| AC122-04 | JIT skills produce typed outputs when called by stage director skills. | Narrative induction returns unstructured text only. | Phase4-M01; JIT bridge test. |
| AC122-05 | Every invocation writes a receipt with input/output hashes and review state. | Invocation completes with no skill version or output hash. | Phase5-M01; receipt replay test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-015` | JIT skill compiler | Must be preserved and bridged. |
| `TS-CMF-081` | Agent architecture | AgentRoleSpec must govern skill access. |
| `TS-CMF-121` | Manifest registry | Stage specs identify skill refs. |
| `contracts/skills.py` | Existing contracts | Extend. |
| `skill_invocation_records.py` | Existing repository | Extend. |
| `command_bus.py` | Existing service | Use for invocation. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Stage skill specs reject missing scope, schema, source artifacts, primitive refs, and receipt type. |
| Permission tests | Agents cannot invoke stage skills outside AgentRoleSpec or manifest scope. |
| Hidden prompt tests | Unregistered prompt text blocks production invocation. |
| JIT bridge tests | JIT compiler outputs are converted to typed envelopes with hashes. |
| Receipt tests | Invocation receipt stores skill version, input hashes, output hash, tool refs, and review status. |
| Replay tests | Replaying an invocation resolves the same skill version and context hashes. |
