---
tech_spec_id: "TS-CMF-069"
title: "ADK and Agents CLI Adapter Export and Drift Gate"
story_id: "11.8"
story_title: "ADK and Agents CLI Adapter Export Drift Gate"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-8-adk-agents-cli-adapter-export-and-drift-gate.md"
fr_ids:
  - "PRD-CMF-10.07"
  - "PRD-CMF-02.04"
module_requirement_ids:
  - "PRD-CMF-10.07"
  - "PRD-CMF-02.04"
pipeline_stage: "adapter/export overlay"
entry_object: "approved agent role spec"
exit_object: "generated ADK/Agents CLI adapter"
validation_contract: "generated-only adapter and drift gate"
required_receipt: "adapter export receipt"
runtime_target: "Python / Pydantic v2 / generated ADK adapters / Agents CLI scaffolds"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-069: ADK and Agents CLI Adapter Export and Drift Gate

**Status:** Ready for Development  
**Story:** `11.8 - ADK and Agents CLI Adapter Export Drift Gate`  
**Implementation Boundary:** Generated ADK/Agents CLI adapters from CMF contracts, export records, generated file hashes, drift checks, adapter receipts, and source-of-truth enforcement.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-8-adk-agents-cli-adapter-export-and-drift-gate.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | Google Agents CLI and BMAD compatibility authority. |
| `docs/cmf-studio-agent-factory-architecture.md` | ADK/Agents CLI adaptation decisions. |
| `docs/cmf-studio-agent-intelligence-contract.md` | Runtime source-of-truth boundaries. |
| `docs/cmf-studio-agent-factory-registry.md` | Persona and role registry source for generated adapters. |
| `docs/architecture.md` | Runtime boundary: Python/Pydantic/DSPy/Pi source of truth. |
| `docs/migration/legacy-inventory.md` | BMAD/ERA3 workflow source and legacy agentic patterns. |

## 2. Overview

Google ADK and Agents CLI can help express deployable agents, sub-agents, tools, callbacks, and graph workflows. They must not become CMF source of truth. CMF generates adapters from `AgentRoleSpec`, `SubAgentRoleSpec`, `HookSpec`, `ExtensionSpec`, `ToolCapabilitySpec`, and readiness receipts.

This spec creates generated adapter exports and a drift gate. If generated files are hand-edited, they are marked non-canonical and must be regenerated.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.07 | Google agent descriptions can help, while BMAD/ERA3 and CMF contracts remain authority. | Generated adapter export, hashes, drift gate. |
| PRD-CMF-02.04 | Pi harness rules remain source of orchestration authority. | Adapter export references CMF role specs and gateway tools. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | adapter/export overlay |
| Entry Object | approved agent role spec |
| Exit Object | generated ADK/Agents CLI adapter |
| Validation Contract | generated-only adapter and drift gate |
| Required Receipt | adapter export receipt |

## 4. Implementation Plan

1. Define `AdapterExportTarget`, `AgentAdapterExport`, `GeneratedAdapterFile`, `AdapterDriftFinding`, and `AdapterExportReceipt`.
2. Implement export from active `AgentRoleSpec` and accepted readiness receipt.
3. Generate ADK-compatible config descriptions, tool declarations, sub-agent references, callback mappings, and handoff hints.
4. Generate Agents CLI scaffolding metadata where useful.
5. Store generated file hashes.
6. Add drift check comparing current generated files to expected hashes.
7. Block hand-authored adapter drift from becoming canonical.
8. Add CI/static guard and API/read model.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class AdapterExportTarget(str, Enum):
    google_adk = "google_adk"
    agents_cli = "agents_cli"


class GeneratedAdapterFile(BaseModel):
    path: str
    content_hash: str
    source_spec_refs: list[str]


class AgentAdapterExport(BaseModel):
    schema_version: Literal["cmf.agent_adapter_export.v1"]
    adapter_export_id: UUID
    target: AdapterExportTarget
    agent_role_spec_id: UUID
    readiness_eval_id: UUID
    generated_files: list[GeneratedAdapterFile]
    export_status: Literal["generated", "drift_detected", "superseded"]


class AdapterDriftFinding(BaseModel):
    schema_version: Literal["cmf.adapter_drift_finding.v1"]
    finding_id: UUID
    adapter_export_id: UUID
    path: str
    expected_hash: str
    observed_hash: str
    decision_code: Literal["regenerate_required"]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `ExportAgentAdapterCommand`, `RunAdapterDriftCheckCommand`, `RegenerateAgentAdapterCommand`, `RecordAdapterExportReceiptCommand` |
| Events | `AgentAdapterExported`, `AdapterDriftDetected`, `AgentAdapterRegenerated`, `AdapterExportSuperseded` |
| Workflow | `AgentFactoryWorkflow.adapter_export_and_drift_gate` |
| Receipt | `AdapterExportReceipt` with target, role spec, readiness eval, generated hashes, drift status |

## 7. Backward Compatibility and Migration Fallback

Hand-authored ADK or Agents CLI configs may be imported only as reference examples. Runtime export must be generated from CMF contracts. Drifted generated files are not patched manually; they are regenerated from source specs.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| External agent runtime convenience vs. CMF authority | ADK/Agents CLI adapters are generated artifacts only. | Adapter export receipt links to AgentRoleSpec and readiness eval. |
| Hand edits vs. contract drift | Hash drift creates regenerate-required finding. | Drift finding blocks canonical use. |
| Callback/tool mapping vs. bypass risk | ADK callbacks and tools map to HookSpec and ToolCapabilitySpec. | Export includes source spec refs. |

## 9. Tasks

- Add adapter export contracts.
- Add export generator.
- Add hash storage and drift checker.
- Add CI/static guard.
- Add API/read model.
- Add tests.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Exported adapter derives name, description, tools, sub-agents, callbacks, handoff hints from CMF contracts. | Adapter contains hand-authored tool not in ToolCapabilitySpec. |
| AC2 | Hand-edited generated adapter is marked non-canonical. | Manual edit silently changes agent behavior. |
| AC3 | ADK callback maps to HookSpec. | Callback bypasses consent hook. |
| AC4 | ADK tool maps to ToolCapabilitySpec and cannot bypass Pydantic/Command Bus. | ADK tool writes canonical state directly. |
| AC5 | Agents CLI scaffold cites originating role spec and readiness receipt. | Deployment scaffold has no CMF source refs. |

## 11. Dependencies

- TS-CMF-063 through TS-CMF-068.
- Existing spec governance and static guard patterns.

## 12. Testing Strategy

Unit tests:

- Export schema generation from AgentRoleSpec.
- Generated hash creation and drift finding.
- Missing readiness eval blocks export.

Integration tests:

- Export ADK adapter for a seeded agent role.
- Hand-edit generated file and verify drift gate fails.
- Tool/callback refs map to ToolCapabilitySpec and HookSpec.

Eval and recovery tests:

- Regeneration supersedes drifted export and writes receipt.
- CI/static guard detects drift before merge.

## 13. Observability, Recovery, and Rollback

- Metrics: adapter exports, drift findings, regenerations, blocked exports.
- Logs include export target, role spec, readiness eval, file hash, drift status.
- Rollback marks export superseded and removes it from deployment candidates.

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
| Tech Spec ID | TS-CMF-069 |
| Story | 11.8 |
| Requirement Trace | PRD-CMF-10.07, PRD-CMF-02.04 |
| Pipeline Trace | adapter/export overlay, approved AgentRoleSpec to generated adapter |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No hand-authored adapter authority, no ADK tool bypass, no export without readiness receipt |
