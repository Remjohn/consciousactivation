---
tech_spec_id: "TS-CMF-003"
title: "Python/DSPy/Pi BMad Spec Workflow"
story_id: "3.5"
story_title: "Python/DSPy/Pi BMad Spec Workflow"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-3-5-python-dspy-pi-bmad-spec-workflow.md"
fr_ids:
  - "FR-CMF-03.07"
pipeline_stage: "spec-governance overlay"
entry_object: "epic/story/spec request"
exit_object: "SpecAuditReceipt"
validation_contract: "files-read, FR trace, pipeline trace, CBAR"
required_receipt: "spec audit receipt"
runtime_target: "Python / Pydantic v2 / DSPy / Pi / durable workflows"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-003: Python/DSPy/Pi BMad Spec Workflow

**Status:** Ready for Development  
**Story:** `3.5 - Python/DSPy/Pi BMad Spec Workflow`  
**Implementation Boundary:** Spec compiler workflow, source-read receipts, requirement trace, pipeline trace, CBAR checks, and spec audit receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for full-system scope, interview-first workflow, legacy intelligence, and Python/DSPy/Pi runtime posture. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-03.07 and PRD authority for spec governance. |
| `docs/architecture.md` | Architecture source for `TechSpecCompilerWorkflow`, `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, `CBARCheck`, and `SpecAuditReceipt`. |
| `docs/cmf-studio-pipeline-map.md` | Pipeline trace authority for spec-governance overlay. |
| `docs/migration/legacy-inventory.md` | Legacy BMAD/ERA3 workflow migration targets and legacy-runtime-coupling prohibition. |
| `docs/stories/story-3-5-python-dspy-pi-bmad-spec-workflow.md` | Story acceptance criteria and handoff requirements. |
| `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Legacy tech-spec 10-section protocol to preserve. |
| `docs/architecture/april_updates/PROMPT_Spec_Build.md` | Legacy build executor discipline for spec decomposition, gates, receipts, and verification. |
| `docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Legacy five-lens audit approach adapted to CMF. |
| `docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning_Epics_Stories.md` | CBAR anti-decay mechanism for generated specs. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Signal distillation quality filter for project-specific evidence. |

## 2. Overview

### Problem Statement

The legacy BMAD and ERA3 writing workflows are valuable because they enforce files-read discipline, FR traceability, CBAR checks, and acceptance criteria rigor. They also contain old stack assumptions and can decay into generic implementation prose if they are copied into CMF unchanged. CMF needs a spec workflow that preserves the intentional orchestration discipline while making Python, Pydantic, DSPy, Pi, durable workflows, and greenfield migration the default target.

### Solution

Implement `TechSpecCompilerWorkflow`: a governed, Python-first workflow that opens from an approved story, records every required source in `FilesReadReceipt`, compiles `RequirementTrace` and `PipelineStageTrace`, uses DSPy programs for spec drafting and auditing, applies CBAR and RSCS checks, and closes with `SpecAuditReceipt` status of accepted, revision requested, or blocked.

### Scope

In scope:

- Pydantic contracts for spec workflow state, source packets, file-read receipts, requirement trace, pipeline trace, CBAR checks, and audit receipts.
- DSPy programs for epic/story compilation, tech-spec drafting, requirement trace compilation, and CBAR audit.
- Pi orchestration boundary for reading sources, invoking compilers, and requesting human approval.
- Rules that replace old "Existing Backend Integration" with "Greenfield Integration and Legacy Migration Context".
- Tests that block specs missing FR trace, pipeline trace, files-read receipts, CBAR, or Python/DSPy/Pi alignment.

Out of scope:

- Product decisions outside approved PRD, architecture, epics, and stories.
- Automatic implementation of code from specs.
- Legacy runtime coupling to old BMAD/ERA3 scripts.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-03.07 | The system can run PRD, epic/story, architecture, and tech-spec workflows using legacy BMAD/ERA3 discipline updated for Python, Pydantic, DSPy, Pi, and CMF greenfield rules. | `TechSpecCompilerWorkflow`, `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, `CBARCheck`, `SpecAuditReceipt`, and greenfield migration lint rules. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | Spec-governance overlay |
| Entry Object | Epic, story, architecture decision, or spec request |
| Exit Object | `SpecAuditReceipt` |
| Allowed Actors / Services | PM Agent, Architect Agent, Tech Writer Agent, Pi Orchestrator, DSPy compiler, human approver |
| Validation Contract | Files-read receipt, FR trace, pipeline trace, CBAR, RSCS, Python/DSPy/Pi alignment |
| Required Receipt | Spec audit receipt |
| Forbidden Shortcut | Writing implementation specs without reading source docs, missing legacy inventory, missing pipeline trace, old-stack assumptions, generic acceptance criteria |

### Legacy Intelligence Mapping

Legacy workflow files are migrated as doctrine and compiler targets:

- `ERA3_Epic_and_Story_Writing_Protocol` maps to `SpecWritingProtocol` and `EpicStoryCompiler`.
- `ERA3_Tech_Spec_Writing_Protocol` maps to `TechSpecWorkflow` and `TechSpecCompiler`.
- `PROMPT_Spec_Audit` maps to `TechSpecAuditor`.
- CBAR materials map to `CBARAuditor` and `CBARCheck`.
- RSCS methodology maps to a quality filter requiring evidence-rich, project-specific outputs.

No legacy workflow file is imported into runtime. The Python implementation stores the protocol as typed policy, fixture, or compiler prompt asset with versioned hashes.

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `SpecWritingProtocol` | Versioned policy object for PRD, architecture, epic/story, and tech-spec writing rules. |
| `TechSpecWorkflow` | Durable state record for a spec-writing run. |
| `TechSpecSourcePacket` | Declares required source documents and feature-specific dependencies. |
| `FilesReadReceipt` | Evidence record that each required source was loaded before drafting. |
| `RequirementTrace` | Links spec sections to FR-CMF IDs and story acceptance criteria. |
| `PipelineStageTrace` | Links spec to stage, entry object, exit object, allowed actor/service, validation contract, and receipt. |
| `CBARCheck` | Records tension, failure scenario, resolution demand, and downstream proof. |
| `SpecAuditReceipt` | Accepted, revision-requested, or blocked verdict with evidence. |

### Technical Decisions

- The spec workflow is itself a canonical orchestration run from TS-CMF-002.
- DSPy compilers produce drafts, traces, and audits, but acceptance requires receipts.
- Pi can orchestrate reading, compilation, and audit tasks, but cannot self-approve a spec.
- Every generated tech spec must state how it integrates with greenfield contracts, commands, events, workflows, DSPy programs, JIT skills, provider boundaries, renderer boundaries, projection boundaries, tests, and recovery.
- Old-stack references must be rewritten or blocked.

## 4. Implementation Plan

### Workstream A: Spec Governance Contracts

Define Pydantic contracts for protocol version, source packets, files-read receipts, requirement trace, pipeline trace, CBAR checks, audit receipts, and spec workflow state.

### Workstream B: Source Resolution and Files Read Receipts

Implement a source resolver that derives required files from story frontmatter, PRD references, architecture references, pipeline map, Legacy Inventory, and feature-specific source docs. The compiler cannot draft until required `FilesReadReceipt` records exist.

### Workstream C: DSPy Compiler Programs

Implement:

- `EpicStoryCompiler`
- `TechSpecCompiler`
- `RequirementTraceCompiler`
- `PipelineStageTraceCompiler`
- `CBARAuditor`
- `TechSpecAuditor`

Each program must receive typed source packets and return Pydantic outputs with evidence references.

### Workstream D: Audit and Block Rules

Add validators for:

- Missing files-read receipt.
- Missing FR-CMF trace.
- Missing pipeline trace.
- Missing CBAR tension or downstream proof.
- Missing greenfield migration context.
- Old-stack runtime assumptions.
- Legacy runtime coupling.
- TypeScript treated as domain authority.
- Pi/DSPy/Telegram/provider/renderer/Neo4j bypass of Command Bus.

### Workstream E: Spec Artifact Writer

Write accepted spec artifacts to `docs/tech-specs` with stable IDs, frontmatter, section headings, and source trace tables. Revision-requested and blocked specs must write audit receipts without overwriting accepted specs.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SpecAuditStatus(str, Enum):
    accepted = "accepted"
    revision_requested = "revision_requested"
    blocked = "blocked"


class SourceFileRef(BaseModel):
    path: str
    required: bool
    source_role: str
    content_hash: str | None = None


class FilesReadReceipt(BaseModel):
    schema_version: Literal["cmf.files_read_receipt.v1"]
    receipt_id: UUID
    workflow_id: UUID
    file_ref: SourceFileRef
    read_at: datetime
    reader_actor_id: UUID
    evidence_summary: str


class RequirementTrace(BaseModel):
    schema_version: Literal["cmf.requirement_trace.v1"]
    trace_id: UUID
    workflow_id: UUID
    fr_id: str
    story_id: str
    spec_sections: list[str]
    acceptance_criteria_refs: list[str]
    enforcement_mechanism: str


class PipelineStageTrace(BaseModel):
    schema_version: Literal["cmf.pipeline_stage_trace.v1"]
    trace_id: UUID
    workflow_id: UUID
    pipeline_stage: str
    entry_object: str
    exit_object: str
    allowed_actor_or_service: str
    validation_contract: str
    required_receipt: str


class CBARCheck(BaseModel):
    schema_version: Literal["cmf.cbar_check.v1"]
    cbar_check_id: UUID
    workflow_id: UUID
    primitive_tension: str
    failure_scenario: str
    resolution_demand: str
    downstream_proof: str
    test_or_receipt_refs: list[str]


class SpecAuditReceipt(BaseModel):
    schema_version: Literal["cmf.spec_audit_receipt.v1"]
    spec_audit_receipt_id: UUID
    workflow_id: UUID
    spec_id: str
    status: SpecAuditStatus
    files_read_receipt_ids: list[UUID]
    requirement_trace_ids: list[UUID]
    pipeline_trace_ids: list[UUID]
    cbar_check_ids: list[UUID]
    findings: list[str] = Field(default_factory=list)
    written_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `OpenTechSpecWorkflowCommand`, `RecordFilesReadReceiptCommand`, `CompileRequirementTraceCommand`, `CompilePipelineStageTraceCommand`, `RunCBARCheckCommand`, `WriteSpecAuditReceiptCommand` |
| Events | `TechSpecWorkflowOpened`, `FilesReadReceiptRecorded`, `RequirementTraceCompiled`, `PipelineStageTraceCompiled`, `CBARCheckCompleted`, `SpecAuditReceiptCreated` |
| Workflows | `TechSpecCompilerWorkflow`, `SpecAuditWorkflow`, `SpecRevisionWorkflow` |
| DSPy Programs | `TechSpecCompiler`, `TechSpecAuditor`, `RequirementTraceCompiler`, `PipelineStageTraceCompiler`, `CBARAuditor` |
| Receipts | `FilesReadReceipt`, `SpecAuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy workflow files remain source doctrine and fixtures. The workflow must not call old scripts as runtime authorities. Existing spec documents may be imported as source examples, but every new CMF tech spec must pass the greenfield audit.

Fallback behavior:

- Missing required file read blocks with `FILES_READ_INCOMPLETE`.
- Missing FR trace blocks with `REQUIREMENT_TRACE_MISSING`.
- Missing pipeline trace blocks with `PIPELINE_TRACE_MISSING`.
- Missing CBAR blocks with `CBAR_CHECK_MISSING`.
- Old-stack target blocks with `GREENFIELD_ALIGNMENT_FAILED`.
- Legacy runtime coupling blocks with `LEGACY_RUNTIME_IMPORT_FORBIDDEN`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Legacy BMAD/ERA3 workflows are valuable, but copying them unchanged preserves stale stack assumptions; rewriting from scratch risks losing their discipline. |
| UX / Ops Failure Scenario | A spec writer creates confident generic requirements that omit Legacy Inventory, pipeline stages, CBAR, source evidence, and Python/DSPy/Pi boundaries. Implementation then builds a plausible but wrong subsystem. |
| Resolution Demand | Preserve the workflow shell as typed policy, source receipts, trace records, CBAR checks, and audit receipts, while replacing old backend assumptions with greenfield migration context. |
| Downstream Proof | Tests must block specs missing required sources, FR trace, pipeline trace, CBAR proof, legacy inventory reference, or Python/DSPy/Pi alignment. |

## 9. Tasks

- Define spec governance Pydantic contracts.
- Add persistence for spec workflows, source packets, files-read receipts, traces, CBAR checks, and audit receipts.
- Implement `TechSpecCompilerWorkflow` through TS-CMF-002 orchestration records.
- Implement source resolver from story frontmatter and canonical documentation.
- Implement DSPy compilers and auditors with typed outputs.
- Add greenfield migration lint rules.
- Add spec artifact writer for `docs/tech-specs`.
- Add human approval hook for accepted specs.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Workflow opens only from approved epic/story and creates `TechSpecWorkflow`. | Spec is drafted from a free-form user prompt with no story link. |
| AC2 | Compiler records files-read receipts for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, story, and feature docs. | Spec references CMF rendering but never reads the Legacy Inventory or pipeline map. |
| AC3 | Spec includes `RequirementTrace` and `PipelineStageTrace`. | Spec lists implementation tasks but no FR-CMF IDs or stage entry/exit objects. |
| AC4 | "Existing Backend Integration" is replaced with "Greenfield Integration and Legacy Migration Context". | Spec says to extend an old Fastify/Supabase route as canonical runtime. |
| AC5 | Old-stack assumptions are blocked. | Spec makes TypeScript the source of truth for domain contracts. |
| AC6 | CBAR includes tension, failure scenario, resolution demand, and downstream proof. | CBAR section says "be careful with quality" but names no conflict or proof. |
| AC7 | RSCS requires project-specific evidence. | Spec uses generic phrases like "improve user engagement" without CMF source trace. |
| AC8 | Workflow closes with `SpecAuditReceipt`. | A spec file is created with no accepted/revision/blocked receipt. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-002 Orchestration records
- `docs/epics.md`
- `docs/stories`
- PRD and architecture source documents
- Legacy Inventory
- Pipeline map

External:

- Pydantic v2
- DSPy
- Durable workflow runtime
- Python markdown parser selected by architecture

## 12. Testing Strategy

Unit tests:

- Source packet resolution from story frontmatter.
- Files-read receipt requiredness.
- Requirement trace schema validation.
- Pipeline trace schema validation.
- CBAR check completeness.
- Greenfield lint rules.

Integration tests:

- Run `TechSpecCompilerWorkflow` for Story 1.1 and produce accepted audit receipt.
- Block a spec with missing Legacy Inventory.
- Block a spec with no pipeline stage trace.
- Request revision for a spec with weak acceptance criteria.
- Block old-stack assumptions.

Safety tests:

- Legacy runtime coupling fails.
- TypeScript domain authority fails.
- Spec allowing Command Bus bypass fails.
- Spec treating Neo4j as canonical truth fails.

## 13. Observability, Recovery, and Rollback

- Logs include `workflow_id`, `spec_id`, `story_id`, `fr_ids`, `pipeline_stage`, and `audit_status`.
- Metrics track accepted specs, revision requests, blocked specs, missing-source failures, and greenfield-alignment failures.
- Recovery resumes from last recorded source receipt or trace.
- Revision preserves prior audit receipt and writes a new receipt after correction.
- Blocked specs are not deleted; they remain evidence for why the workflow stopped.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-03.07 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - BMAD/ERA3 protocols mapped to Python contracts, DSPy programs, and audit receipts |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Native target of workflow |
| TypeScript Boundary | No TypeScript spec authority |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |


