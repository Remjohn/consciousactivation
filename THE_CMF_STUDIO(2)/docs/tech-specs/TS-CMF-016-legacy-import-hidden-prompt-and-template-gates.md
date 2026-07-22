---
tech_spec_id: "TS-CMF-016"
title: "Legacy Import, Hidden Prompt, and Template Gates"
story_id: "3.4"
story_title: "Legacy Import, Hidden Prompt, and Template Gates"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-3-4-legacy-import-hidden-prompt-and-template-gates.md"
fr_ids:
  - "FR-CMF-03.06"
pipeline_stage: "0 / all stages"
entry_object: "import/template/spec reference"
exit_object: "blocked or approved reference"
validation_contract: "greenfield rule and template hash"
required_receipt: "gate failure or approval receipt"
runtime_target: "Python / CI checks / registry validation / provider template hash gates / spec audit"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-016: Legacy Import, Hidden Prompt, and Template Gates

**Status:** Ready for Development  
**Story:** `3.4 - Legacy Import, Hidden Prompt, and Template Gates`  
**Implementation Boundary:** CI import blockers, hidden prompt gates, registry conflict checks, provider template hash checks, and spec review checks.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Greenfield Rule, legacy runtime coupling is forbidden, no hidden shell dependencies, and no duplicated TypeScript domain logic. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-03.06 source authority and NFR46/NFR47 boundaries. |
| `docs/architecture.md` | Architecture authority for legacy import ban, registry validation, worker asset constraints, and spec audit rules. |
| `docs/cmf-studio-pipeline-map.md` | Stage 0 and all-stage gate trace. |
| `docs/migration/legacy-inventory.md` | Greenfield Rule and legacy asset classifications. |
| `docs/stories/story-3-4-legacy-import-hidden-prompt-and-template-gates.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-013-migration-ledger-inventory-and-hashing.md` | Ledger target lookup dependency. |
| `docs/tech-specs/TS-CMF-014-registry-conversion-fixtures-and-evals.md` | Registry conflict dependency. |
| `docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | Hidden prompt/JIT compiler dependency. |

## 2. Overview

### Problem Statement

The fastest way to lose the greenfield architecture is to import old runtime modules, run hidden prompt stacks, activate duplicate registry truths, reference unapproved provider templates, or write specs with old stack assumptions. These shortcuts can appear useful while quietly reintroducing fragmentation, untyped state, and prompt drift.

### Solution

Implement gates across CI, workflow execution, registry activation, provider template routing, and spec review. Legacy runtime coupling imports fail CI with ledger target guidance. Hidden prompts are blocked unless migrated into typed compilers or registries. Duplicate registry truth requires resolution. Provider templates require approved hash and compatibility notes. Specs are flagged when they assign domain authority to an old or wrong runtime boundary.

### Scope

In scope:

- Static import scanner for production packages.
- Hidden prompt and unapproved template gate.
- Registry conflict activation gate.
- Provider template hash and compatibility gate.
- Tech spec/story review gate for runtime-boundary drift.
- Gate receipts and evaluation receipts for failures and approvals.

Out of scope:

- Full provider adapter execution.
- Full worker asset migration. Later provider specs will implement worker execution.
- Runtime security scanning beyond legacy/import/template boundaries.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-03.06 | System rejects legacy runtime couplings, stale TypeScript-first assumptions, hidden prompts, duplicate registries, and unapproved templates. | CI import scanner, hidden prompt gate, registry conflict gate, provider template hash gate, and spec audit check. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `0 - Legacy inventory and migration`; all production stages where a legacy reference, prompt, registry, or template is used |
| Entry Object | Import, template, prompt, registry, or spec reference |
| Exit Object | Blocked or approved reference |
| Allowed Actors / Services | CI, MigrationWorkflow, RegistryService, ProviderRouteService, TechSpecAuditor, Architecture Reviewer |
| Validation Contract | Greenfield Rule, ledger target, registry conflict state, template hash, and permitted runtime boundary |
| Required Receipt | Gate failure or approval receipt |
| Forbidden Shortcut | Legacy runtime coupling, hidden prompt stack, duplicate registry truth, unapproved ComfyUI template, TypeScript domain authority |

### Legacy Intelligence Mapping

The Legacy Inventory explicitly allows legacy assets as read-only doctrine, fixtures, examples, provider-code source, reference implementations, and approved worker assets. This spec turns that rule into executable gates.

Target modules:

- `ccp_studio.gates.legacy_import_gate`
- `ccp_studio.gates.hidden_prompt_gate`
- `ccp_studio.gates.registry_conflict_gate`
- `ccp_studio.gates.provider_template_gate`
- `ccp_studio.gates.spec_runtime_boundary_gate`
- `tests/evals/greenfield_gate_test.py`
- `tests/spec_governance/runtime_boundary_test.py`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `LegacyImportViolation` | Legacy runtime coupling with source path and migration target. |
| `HiddenPromptViolation` | Prompt stack not migrated into typed registry/compiler. |
| `RegistryConflictViolation` | Duplicate or overlapping active truths. |
| `ProviderTemplateApproval` | Approved template hash, compatibility notes, required inputs, outputs, defects, and eval target. |
| `RuntimeBoundaryFinding` | Spec/story finding for wrong runtime authority. |
| `GateReceipt` | Block or approve result with evidence and repair path. |

## 4. Implementation Plan

### Workstream A: Import Scanner

Scan production Python packages for legacy runtime coupling references. When found, fail with `LEGACY_IMPORT_BLOCKED` and lookup migration ledger target.

### Workstream B: Hidden Prompt Gate

Require all production prompts to be represented as typed registry entries, JIT skill compilers, or DSPy program specs with hashes and eval targets.

### Workstream C: Registry Conflict Gate

Block activation when duplicate registry truths exist until reviewer resolves authority.

### Workstream D: Provider Template Gate

Require approved template hash, compatibility notes, required inputs, output contracts, known defects, and eval target before worker route can use a provider template.

### Workstream E: Spec Runtime Boundary Gate

Scan tech specs and stories for runtime-boundary drift and flag violations in `SpecAuditReceipt`.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class GateViolationType(str, Enum):
    legacy_import = "legacy_import"
    hidden_prompt = "hidden_prompt"
    registry_conflict = "registry_conflict"
    provider_template_hash = "provider_template_hash"
    runtime_boundary = "runtime_boundary"


class GateStatus(str, Enum):
    approved = "approved"
    blocked = "blocked"
    revision_required = "revision_required"


class GateReceipt(BaseModel):
    schema_version: Literal["cmf.gate_receipt.v1"]
    gate_receipt_id: UUID
    violation_type: GateViolationType
    status: GateStatus
    object_ref: str
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)
    repair_target: str | None = None
    written_at: datetime


class ProviderTemplateApproval(BaseModel):
    schema_version: Literal["cmf.provider_template_approval.v1"]
    provider_template_approval_id: UUID
    template_key: str
    content_hash: str
    compatibility_notes: str
    required_inputs: list[str]
    output_contract: str
    known_defects: list[str] = Field(default_factory=list)
    evaluation_target_id: UUID
    approved_by_actor_id: UUID
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `RunLegacyImportGateCommand`, `ValidatePromptStackCommand`, `ValidateRegistryConflictCommand`, `ValidateProviderTemplateCommand`, `RunSpecRuntimeBoundaryGateCommand` |
| Events | `LegacyImportBlocked`, `HiddenPromptBlocked`, `RegistryConflictBlocked`, `ProviderTemplateBlocked`, `RuntimeBoundaryFindingRecorded`, `GateReceiptWritten` |
| Workflows | Greenfield gate workflow, provider template approval workflow, spec audit gate workflow |
| Receipts | `GateReceipt`, `EvaluationReceipt`, `SpecAuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

There is no direct runtime fallback. Legacy code can appear as source path, fixture, reference behavior, worker asset if approved, or migration source only.

Fallback behavior:

- Direct import returns `LEGACY_IMPORT_BLOCKED`.
- Hidden prompt returns `PROMPT_STACK_NOT_MIGRATED`.
- Duplicate registry returns `REGISTRY_CONFLICT_REQUIRES_REVIEW`.
- Missing template hash returns `PROVIDER_TEMPLATE_HASH_REQUIRED`.
- Wrong runtime authority returns `RUNTIME_BOUNDARY_DRIFT`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Implementation speed wants shortcuts; greenfield integrity requires explicit migration and typed activation. |
| UX / Ops Failure Scenario | A developer imports old runtime code or a worker runs an unapproved ComfyUI template, causing hidden dependencies and unreproducible outputs. |
| Resolution Demand | Greenfield gate authority takes precedence. Every legacy import, prompt, registry, template, and spec boundary must be approved or blocked with receipt. |
| Downstream Proof | Tests must fail direct imports, hidden prompts, duplicate registries, missing template hashes, and runtime-boundary drift in specs. |

## 9. Tasks

- Implement import scanner.
- Implement hidden prompt gate.
- Implement registry conflict gate.
- Implement provider template hash gate.
- Implement spec runtime-boundary gate.
- Add gate receipts.
- Add CI/eval tests.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Direct production import from legacy runtime fails with ledger target. | Production package imports old CMF engine module. |
| AC2 | Unapproved prompt stack is blocked until migrated into typed compiler or registry. | Agent runs a raw prompt file from legacy folder. |
| AC3 | Duplicate registry truths require conflict resolution before activation. | Two route definitions both claim canonical authority. |
| AC4 | Provider template without approved hash or compatibility notes is blocked. | Worker runs ComfyUI JSON from unapproved path. |
| AC5 | Tech spec/story runtime-boundary drift is flagged unless the runtime is a permitted leaf. | Spec makes UI code define domain contracts. |

## 11. Dependencies

Internal:

- TS-CMF-003 Spec workflow
- TS-CMF-013 Migration ledger
- TS-CMF-014 Registry conversion
- TS-CMF-015 JIT skill compiler

External:

- CI runner
- Pydantic v2
- pytest or selected eval runner

## 12. Testing Strategy

Unit tests:

- Import scanner path matching.
- Hidden prompt detection.
- Provider template approval schema.
- Runtime-boundary finding generation.

Integration tests:

- CI fails on legacy import.
- Prompt stack blocked until registry migration.
- Duplicate registry conflict blocks activation.
- Provider template route blocks missing hash.
- Spec audit flags runtime-boundary drift.

Safety tests:

- Gate checks cannot be disabled by normal workflow command.
- Approved exception requires explicit reviewer and receipt.
- Worker route cannot execute unapproved template.

## 13. Observability, Recovery, and Rollback

- Logs include `gate_receipt_id`, violation type, object ref, decision code, and repair target.
- Metrics track violations by type, blocked builds, blocked worker routes, and spec audit findings.
- Recovery reruns gates after repair.
- Rollback revokes approval by new gate receipt; prior approvals remain auditable.

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
| Requirement Trace | FR-CMF-03.06 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Greenfield Rule enforced as CI/workflow/spec gates |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python gates and spec governance with Pi unable to bypass |
| TypeScript Boundary | Leaf-only runtime enforced |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

