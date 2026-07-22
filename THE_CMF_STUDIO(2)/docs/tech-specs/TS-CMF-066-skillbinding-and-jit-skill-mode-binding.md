---
tech_spec_id: "TS-CMF-066"
title: "SkillBinding and JIT Skill Mode Binding"
story_id: "11.5"
story_title: "Skill Bindings and JIT Compiler Modes"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-5-skill-bindings-and-jit-compiler-modes.md"
fr_ids:
  - "PRD-CMF-10.05"
module_requirement_ids:
  - "PRD-CMF-10.05"
pipeline_stage: "stages 3-8 and 13"
entry_object: "agent role and skill need"
exit_object: "`SkillBinding`, JIT compiler mode binding"
validation_contract: "stable-vs-JIT distinction and invocation record requirement"
required_receipt: "skill binding receipt"
runtime_target: "Python / Pydantic v2 / DSPy / JIT Skill Compiler"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-066: SkillBinding and JIT Skill Mode Binding

**Status:** Ready for Development  
**Story:** `11.5 - Skill Bindings and JIT Compiler Modes`  
**Implementation Boundary:** Stable skill binding, JIT skill compiler mode binding, allowed use modes, invocation requirements, activation gates, and skill binding receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-5-skill-bindings-and-jit-compiler-modes.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | Skills and JIT Skills product authority. |
| `docs/cmf-studio-skill-system-contract.md` | Stable vs JIT skill distinction. |
| `docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | Existing JIT compiler contracts and invocation records. |
| `src/ccp_studio/contracts/skills.py` | Existing skill invocation contracts. |
| `docs/migration/legacy-inventory.md` | Legacy JIT modules and skill compiler source context. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Saturation and anti-genericity quality filter. |

## 2. Overview

CMF Studio has two skill families. Stable operational skills are repeatable procedures such as registry lookup, source review, blocker inspection, or command proposal. JIT Skill Compilers are saturation-bound specialist compilers for interview briefs, narrative induction, contrast questions, expression extraction, route support, and evaluation support.

This spec binds skills to agents without collapsing them into hidden prompts. JIT usage requires saturation context, registry snapshot, compiler fingerprint, contrastive prompt layer, critic result, synthesis result, and `SkillInvocationRecord`.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.05 | Skills and JIT Skills are reusable capabilities; JIT skills produce invocation records. | SkillBinding, StableSkillBinding, JITSkillModeBinding, invocation requirements, receipts. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | stages 3-8 and 13 |
| Entry Object | agent role and skill need |
| Exit Object | `SkillBinding`, JIT compiler mode binding |
| Validation Contract | stable-vs-JIT distinction and invocation record requirement |
| Required Receipt | skill binding receipt |

## 4. Implementation Plan

1. Define `SkillBinding`, `StableSkillBinding`, `JITSkillModeBinding`, and `SkillBindingReceipt`.
2. Reuse existing `SkillUseMode`, `JITSkillCompiler`, `SaturationContextBundle`, and `SkillInvocationRecord`.
3. Add allowed stage and agent role compatibility checks.
4. Require JIT bindings to specify output schema, DSPy program spec, eval target, and invocation evidence.
5. Block generic few-shot-only skills from activation.
6. Migrate `SkillUseMode` to include `interview_engineering`, `narrative_induction`, `source_expression_contrast`, and `scene_prompt_support_after_route` as first-class values. The `scene_prompt_support_after_route` mode must be blocked unless an approved `ExpressionMoment`, route receipt, and `CompleteEditingSession` exist.
7. Add service/API methods for binding, activation, and inspection.
8. Emit receipts.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SkillBindingType(str, Enum):
    stable = "stable"
    jit = "jit"


class SkillUseMode(str, Enum):
    live_guest_induction = "live_guest_induction"
    interview_engineering = "interview_engineering"
    narrative_induction = "narrative_induction"
    transcript_extraction = "transcript_extraction"
    source_expression_contrast = "source_expression_contrast"
    routing_support = "routing_support"
    evaluation_support = "evaluation_support"
    voice_dna_support = "voice_dna_support"
    scene_prompt_support_after_route = "scene_prompt_support_after_route"


class SkillBinding(BaseModel):
    schema_version: Literal["cmf.skill_binding.v1"]
    skill_binding_id: UUID
    skill_entity_code: str
    binding_type: SkillBindingType
    agent_role_ref: str
    allowed_stage_refs: list[str]
    allowed_use_modes: list[SkillUseMode]
    skill_manifest_ref: str | None = None
    jit_compiler_ref: str | None = None
    required_invocation_record: bool
    output_schema_ref: str
    evaluation_target_refs: list[str]
    active: bool


class SkillBindingReceipt(BaseModel):
    schema_version: Literal["cmf.skill_binding_receipt.v1"]
    receipt_id: UUID
    skill_binding_id: UUID
    decision_code: Literal["accepted", "blocked", "updated"]
    evidence_refs: list[str]
    failure_reasons: list[str] = []
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `BindStableSkillCommand`, `BindJITSkillModeCommand`, `ActivateSkillBindingCommand`, `BlockSkillBindingCommand` |
| Events | `SkillBindingCreated`, `SkillBindingActivated`, `SkillBindingBlocked`, `SkillBindingUsed` |
| Workflow | `AgentFactoryWorkflow.skill_binding_activation` |
| Receipt | `SkillBindingReceipt`, plus existing `SkillInvocationRecord` and `SkillInvocationReceipt` for JIT use |

## 7. Backward Compatibility and Migration Fallback

Legacy JIT modules become source doctrine, fixtures, evals, stable skills, or JIT compilers. Script-writing or visual-prompt skills are not discarded, but current north-star bindings must support interview briefs, induction, extraction, route reasoning, and eval support. Generic few-shot prompt snippets remain blocked.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Stable skills vs. JIT compilers | Bind them differently and validate invocation requirements. | SkillBinding type and receipt. |
| Legacy scripts vs. interview-first north star | JIT modes prioritize interview brief, induction, extraction, route, and eval support. | Allowed use modes and eval targets. |
| Hidden prompts vs. auditable intelligence | JIT use requires SkillInvocationRecord. | Invocation record linked to agent and stage. |

## 9. Tasks

- Add SkillBinding contracts.
- Extend allowed use modes for interview brief and induction if needed.
- Add binding service.
- Add activation gates.
- Add API/read model.
- Add tests and receipts.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Stable skill references versioned manifest and procedure. | Stable skill is a loose instruction paragraph. |
| AC2 | JIT binding requires saturation, registry snapshot, compiler fingerprint, contrast, critic, synthesis, invocation record. | JIT compiler emits candidates without source context. |
| AC3 | Interview engineering JIT supports explicit `interview_engineering`, `narrative_induction`, `source_expression_contrast`, extraction, route, or eval use modes. | JIT only writes generic social scripts or hides interview brief generation under a generic prompt mode. |
| AC4 | Generic few-shot skill activation is blocked. | Prompt snippet becomes production skill. |
| AC5 | `EXT-JITCOMP-AG` outputs retain source context and eval state. | Routing consumes untraceable extraction candidates. |
| AC6 | `scene_prompt_support_after_route` is unavailable until an approved Expression Moment, route receipt, and Complete Editing Session exist. | A visual prompt compiler runs before source expression and routing are approved. |

## 11. Dependencies

- TS-CMF-015, TS-CMF-023 through TS-CMF-035, TS-CMF-050, TS-CMF-062, TS-CMF-063.

## 12. Testing Strategy

Unit tests:

- Stable vs JIT binding validation.
- Missing invocation requirement rejection.
- Generic few-shot-only rejection.
- Explicit validation for `interview_engineering`, `narrative_induction`, `source_expression_contrast`, and `scene_prompt_support_after_route` use modes.

Integration tests:

- Agent invokes JIT skill and creates SkillInvocationRecord.
- Route consumes JIT output only with eval state.
- Interview brief compiler binding uses saturation bundle.

Eval and recovery tests:

- Anti-draft calibration fixtures.
- Failed skill invocation remains receipt-backed and does not affect routing.

## 13. Observability, Recovery, and Rollback

- Metrics: skill bindings, JIT invocations, blocked generic skills, eval failures.
- Logs include skill code, agent code, use mode, compiler fingerprint, registry snapshot.
- Rollback deactivates binding and preserves invocation records.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-066 |
| Story | 11.5 |
| Requirement Trace | PRD-CMF-10.05 |
| Pipeline Trace | stages 3-8 and 13, agent skill need to SkillBinding |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No hidden prompts, no generic few-shot skill activation, no JIT output without invocation record |
