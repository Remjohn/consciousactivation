---
tech_spec_id: "TS-CMF-065"
title: "HookSpec and ExtensionSpec Lifecycle Contracts"
story_id: "11.4"
story_title: "Hook and Extension Lifecycle Contracts"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-4-hook-and-extension-lifecycle-contracts.md"
fr_ids:
  - "PRD-CMF-10.03"
  - "PRD-CMF-10.04"
module_requirement_ids:
  - "PRD-CMF-10.03"
  - "PRD-CMF-10.04"
pipeline_stage: "all gated stages"
entry_object: "lifecycle boundary and integration request"
exit_object: "`HookSpec`, `ExtensionSpec`"
validation_contract: "no canonical-state bypass and lifecycle contract"
required_receipt: "hook/extension receipt"
runtime_target: "Python / Pydantic v2 / Agent Gateway / Command Bus / provider extensions"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-065: HookSpec and ExtensionSpec Lifecycle Contracts

**Status:** Ready for Development  
**Story:** `11.4 - Hook and Extension Lifecycle Contracts`  
**Implementation Boundary:** HookSpec, ExtensionSpec, lifecycle triggers, mounting rules, callback mapping, no-canonical-authority checks, and hook/extension receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-4-hook-and-extension-lifecycle-contracts.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | Hook and Extension product definitions. |
| `docs/cmf-studio-agent-factory-architecture.md` | Hook lifecycle and extension vocabulary. |
| `docs/cmf-studio-agent-intelligence-contract.md` | Runtime spine and gateway constraints. |
| `docs/architecture.md` | Command Bus, provider adapter, publishing, and canonical state boundaries. |
| `docs/migration/legacy-inventory.md` | Legacy gates, callbacks, and provider integration lineage. |

## 2. Overview

Hooks are deterministic lifecycle checks around stages, models, tools, workflows, provider jobs, review, publishing, and memory admission. Extensions are bounded integration packages behind contracts, such as Publer, Telegram, Remotion, Motion Canvas, ComfyUI worker, provider adapters, research connectors, or Neo4j projection.

Hooks and extensions enforce or expose capability; they do not own canonical truth. This spec prevents hidden authority by making lifecycle boundaries, trigger conditions, allowed checks, mutation restrictions, credentials boundaries, tool exposure, and receipts explicit.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.03 | Hooks run before/after lifecycle boundaries and enforce gates. | HookSpec, lifecycle enums, trigger conditions, receipts. |
| PRD-CMF-10.04 | Extensions expose bounded integrations behind contracts and cannot own canonical truth. | ExtensionSpec, mounting rules, no-canonical-authority checks. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | all gated stages |
| Entry Object | lifecycle boundary and integration request |
| Exit Object | `HookSpec`, `ExtensionSpec` |
| Validation Contract | no canonical-state bypass and lifecycle contract |
| Required Receipt | hook/extension receipt |

## 4. Implementation Plan

1. Define `LifecycleBoundary`, `HookSpec`, `ExtensionSpec`, `HookExecutionReceipt`, and `ExtensionMountReceipt`.
2. Add lifecycle boundary enum: before/after stage, model, tool, workflow, command, provider, review, publish, memory admission.
3. Add deterministic-only hook rule; hooks cannot perform creative synthesis.
4. Add extension mounting rules with credential boundary and canonical-state restriction.
5. Register core hooks: consent gate, brand-scope gate, registry conflict gate, approval gate, memory admission gate.
6. Register core extensions: Publer, Telegram, provider adapters, renderers, Neo4j projection.
7. Add gateway enforcement so hooks/extensions cannot mutate outside Command Bus or approved workflow.
8. Emit receipts.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class LifecycleBoundary(str, Enum):
    before_stage = "before_stage"
    after_stage = "after_stage"
    before_tool = "before_tool"
    after_tool = "after_tool"
    before_provider_job = "before_provider_job"
    after_provider_job = "after_provider_job"
    before_review = "before_review"
    before_publishing = "before_publishing"
    before_memory_admission = "before_memory_admission"


class HookSpec(BaseModel):
    schema_version: Literal["cmf.hook_spec.v1"]
    hook_spec_id: UUID
    entity_code: str
    lifecycle_boundary: LifecycleBoundary
    trigger_condition: str
    allowed_checks: list[str]
    blocked_mutations: list[str]
    emitted_receipt_type: str
    failure_behavior: Literal["block", "warn", "handoff"]


class ExtensionSpec(BaseModel):
    schema_version: Literal["cmf.extension_spec.v1"]
    extension_spec_id: UUID
    entity_code: str
    integration_scope: str
    exposed_tool_refs: list[str]
    credential_boundary_ref: str | None
    canonical_state_authority: Literal["none"]
    required_receipt_types: list[str]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterHookSpecCommand`, `RegisterExtensionSpecCommand`, `MountExtensionCommand`, `RunHookCommand`, `RecordHookReceiptCommand` |
| Events | `HookSpecRegistered`, `ExtensionSpecRegistered`, `ExtensionMounted`, `HookBlockedAction`, `HookApprovedAction` |
| Workflow | `AgentFactoryWorkflow.lifecycle_contract_mounting` |
| Receipt | `HookExecutionReceipt`, `ExtensionMountReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy callback, provider, and publishing behaviors must be converted into HookSpec or ExtensionSpec records. If a legacy integration assumes it owns state, it must be blocked or wrapped so CMF canonical state remains in PostgreSQL/Command Bus.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Lifecycle enforcement vs. hidden control | Hooks declare deterministic checks and blocked mutations. | Hook receipt shows decision and evidence. |
| Integration usefulness vs. external authority | Extensions expose tools but own no canonical state. | ExtensionSpec `canonical_state_authority` is `none`. |
| ADK callbacks vs. CMF gates | Callback-like behavior maps to CMF HookSpec. | Generated adapter links back to HookSpec. |

## 9. Tasks

- Add HookSpec and ExtensionSpec contracts.
- Add lifecycle enums.
- Implement registry and mounting services.
- Add gateway enforcement.
- Seed core hooks/extensions.
- Add tests and receipts.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Hook declares lifecycle, trigger, checks, blocked mutations, receipt, failure behavior. | Hook runs arbitrary prompt before publishing. |
| AC2 | Extension declares tools, credential boundary, scope, restrictions, receipts. | Publer adapter owns approval state. |
| AC3 | Creative reasoning hook is blocked. | Approval hook rewrites captions creatively. |
| AC4 | `PUB-PUBLERX-EX` cannot own canonical truth. | Publer status overwrites asset approval. |
| AC5 | `REV-APPGATE-HK` blocks publishing when blockers exist. | Publication proceeds despite missing lineage. |

## 11. Dependencies

- TS-CMF-001, TS-CMF-010, TS-CMF-042, TS-CMF-053, TS-CMF-054, TS-CMF-062, TS-CMF-063.

## 12. Testing Strategy

Unit tests:

- HookSpec validation and deterministic-only rule.
- ExtensionSpec canonical authority restriction.
- Lifecycle trigger matching.

Integration tests:

- Approval gate hook blocks publication.
- Publer extension schedules only approved PublishingIntent.
- Consent hook blocks provider job.

Eval and recovery tests:

- Hook failure creates blocker receipt.
- Extension mount rollback disables tools and preserves receipts.

## 13. Observability, Recovery, and Rollback

- Metrics: hook executions, blocks, extension tool calls, mount failures.
- Logs include lifecycle boundary, entity code, active object, decision, receipt ID.
- Rollback disables hook/extension version and preserves mount history.

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
| Tech Spec ID | TS-CMF-065 |
| Story | 11.4 |
| Requirement Trace | PRD-CMF-10.03, PRD-CMF-10.04 |
| Pipeline Trace | all gated stages, lifecycle boundary to HookSpec/ExtensionSpec |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No creative hooks, no extension canonical truth, no bypass of Command Bus |
