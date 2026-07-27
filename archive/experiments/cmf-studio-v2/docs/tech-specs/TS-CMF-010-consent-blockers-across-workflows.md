---
tech_spec_id: "TS-CMF-010"
title: "Consent Blockers Across Workflows"
story_id: "2.3"
story_title: "Consent Blockers Across Workflows"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-2-3-consent-blockers-across-workflows.md"
fr_ids:
  - "FR-CMF-02.03"
pipeline_stage: "all gated stages"
entry_object: "consent-sensitive command"
exit_object: "blocked or allowed state"
validation_contract: "current consent compatibility"
required_receipt: "consent blocker receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / durable workflows"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-010: Consent Blockers Across Workflows

**Status:** Ready for Development  
**Story:** `2.3 - Consent Blockers Across Workflows`  
**Implementation Boundary:** Cross-workflow consent blocker policy for provider jobs, renders, memory admission, review, publishing intent, and future reuse.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for consent as a hard operational boundary. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-02.03 source authority and NFR16 consent policy boundary. |
| `docs/architecture.md` | Architecture source for Command Bus consent checks, workflow quarantine, provider jobs, memory admission, and publishing intent. |
| `docs/cmf-studio-pipeline-map.md` | Cross-stage trace for consent-sensitive stages. |
| `docs/migration/legacy-inventory.md` | Legacy governance gates and receipt chain as read-only references. |
| `docs/stories/story-2-3-consent-blockers-across-workflows.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-008-versioned-consent-records.md` | Consent version dependency. |
| `docs/tech-specs/TS-CMF-009-recording-setup-and-source-artifact-gate.md` | Source artifact dependency. |

## 2. Overview

### Problem Statement

Consent rules are only reliable if every consent-sensitive workflow calls them. A correct consent record is not enough if provider jobs, render commands, memory admission, review, or publishing intent can bypass the current version. Future reuse is especially risky because historical approval may no longer match current consent.

### Solution

Implement a cross-workflow `ConsentBlockerPolicy` that maps command types and workflow stages to required consent scopes. The policy runs inside Command Bus validation and durable workflows before external provider processing, likeness reuse, render, memory admission, review approval, publishing intent, and Publer scheduling. Blocks create `ConsentBlockerReceipt` and offer quarantine or repair actions where appropriate.

### Scope

In scope:

- Consent-sensitive command registry.
- Required-scope mapping for provider, render, memory, review, publishing, future reuse, and voice repair commands.
- `ConsentBlockerReceipt` and affected pending job flagging.
- Current consent re-evaluation for future reuse.
- Tests across every gated boundary.

Out of scope:

- New consent scope creation beyond TS-CMF-008.
- Provider-specific job execution.
- Full memory admission implementation.
- Full publishing adapter implementation.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-02.03 | System blocks processing, provider jobs, renders, memory, review, and publishing when consent is incompatible. | `ConsentBlockerPolicy`, consent-sensitive command registry, current consent compatibility checks, blocker receipts, and quarantine hooks. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | All gated stages, especially provider jobs, rendering, review, memory, and publishing |
| Entry Object | Consent-sensitive command |
| Exit Object | Blocked or allowed state |
| Allowed Actors / Services | Command Bus, ConsentPolicyService, ProviderJobWorkflow, RenderWorkflow, ReviewService, MemoryAdmissionService, PublishingWorkflow |
| Validation Contract | Current consent compatibility |
| Required Receipt | Consent blocker receipt or consent compatibility receipt |
| Forbidden Shortcut | Historical approval treated as current consent, provider/render/memory/publishing actions without consent policy call |

### Legacy Intelligence Mapping

Legacy governance gates become fixtures and tests, not runtime imports. This spec makes consent a system-wide dependency, which prevents later specs from defining local consent logic. All future provider, renderer, memory, and publishing specs must cite this blocker policy.

Target modules:

- `ccp_studio.domain.policies.consent_blocker_policy`
- `ccp_studio.contracts.consent_blockers`
- `ccp_studio.services.consent_guard`
- `ccp_studio.workflows.consent_sensitive_workflows`
- `ccp_studio.repositories.consent_blocker_receipts`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `ConsentSensitiveCommand` | Registry entry mapping command type to required consent scopes. |
| `ConsentBlockerPolicy` | Evaluates current consent before consent-sensitive commands. |
| `ConsentBlockerReceipt` | Durable proof of blocked action, scope, object, evidence, and repair options. |
| `AffectedPendingWork` | Pending provider jobs, renders, memory candidates, or publishing intents requiring quarantine/review. |
| `ConsentRepairOption` | Quarantine, remove claim, remove likeness, request updated consent, or human review. |

## 4. Implementation Plan

### Workstream A: Command Registry

Define consent-sensitive command categories and required scopes for provider processing, likeness reuse, render, memory admission, review approval, publishing intent, Publer scheduling, and voice repair.

### Workstream B: Policy Service

Implement `ConsentBlockerPolicy.evaluate(command, object_ref, consent_version)` returning allow/block and required repair options.

### Workstream C: Workflow Integration

Install blockers at Command Bus validation and durable workflow boundaries. Workflows must re-check after long waits or before external side effects.

### Workstream D: Receipts and Quarantine

Write blocker receipts and flag pending work affected by scope changes.

### Workstream E: Future Reuse

For any reuse command, evaluate current consent version rather than original approval state.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ConsentRepairAction(str, Enum):
    quarantine = "quarantine"
    request_updated_consent = "request_updated_consent"
    remove_likeness = "remove_likeness"
    remove_claim = "remove_claim"
    human_review = "human_review"


class ConsentSensitiveCommand(BaseModel):
    schema_version: Literal["cmf.consent_sensitive_command.v1"]
    command_type: str
    required_scopes: list[str]
    applies_to_stages: list[str]
    external_side_effect: bool = False


class ConsentBlockerReceipt(BaseModel):
    schema_version: Literal["cmf.consent_blocker_receipt.v1"]
    consent_blocker_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    command_id: UUID
    object_type: str
    object_id: UUID
    consent_record_version_id: UUID | None
    blocked_scope: str
    decision_code: str
    repair_actions: list[ConsentRepairAction]
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `EvaluateConsentSensitiveCommand`, `BlockForConsentScopeCommand`, `FlagAffectedPendingWorkCommand`, `RequestConsentRepairCommand` |
| Events | `ConsentSensitiveCommandBlocked`, `AffectedPendingWorkFlagged`, `ConsentRepairRequested`, `ConsentSensitiveCommandAllowed` |
| Workflows | Consent guard workflow, pending work quarantine workflow |
| Receipts | `ConsentBlockerReceipt`, `FailureReceipt`, `HumanHandoffRequest` |

## 7. Backward Compatibility and Migration Fallback

Any legacy workflow that performs provider processing, rendering, memory, publishing, or voice repair must be wrapped by this policy before production use. If scope mapping is missing, default to blocked.

Fallback behavior:

- Missing scope mapping returns `CONSENT_SCOPE_MAPPING_REQUIRED`.
- Provider processing not allowed returns `CONSENT_SCOPE_BLOCKED`.
- Likeness revoked returns `LIKENESS_REUSE_BLOCKED`.
- Publication missing returns `PUBLICATION_CONSENT_REQUIRED`.
- Memory scope mismatch returns `MEMORY_ADMISSION_CONSENT_BLOCKED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Each workflow wants local autonomy; consent must remain a global runtime blocker. |
| UX / Ops Failure Scenario | A publishing workflow trusts an old approval after consent was narrowed, or a provider job runs after provider processing was revoked. |
| Resolution Demand | Current consent compatibility takes precedence over workflow convenience and historical approvals. |
| Downstream Proof | Tests must prove provider, render, memory, review, publishing, and future reuse commands block when consent is incompatible. |

## 9. Tasks

- Define consent-sensitive command registry.
- Implement blocker policy.
- Integrate with Command Bus and durable workflows.
- Add blocker receipt repository.
- Add pending work flagging.
- Add future reuse current-consent check.
- Add tests for every gated boundary.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Provider job fails with `CONSENT_SCOPE_BLOCKED` when provider processing is not allowed. | External provider receives source after provider scope revoked. |
| AC2 | Likeness reuse revocation blocks re-render and flags pending jobs. | Scene re-renders using revoked likeness. |
| AC3 | Missing publication consent blocks Publishing Intent before scheduling. | Publer scheduling starts with no publication scope. |
| AC4 | Memory admission incompatible with sensitive source cannot be approved and offers quarantine. | Sensitive quote becomes memory without consent. |
| AC5 | Future reuse evaluates current consent version, not historical approval. | Old approval permits reuse after narrowing. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-002 Orchestration records
- TS-CMF-008 Consent records
- TS-CMF-009 Source artifact gate

External:

- FastAPI
- Pydantic v2
- Durable workflow runtime
- PostgreSQL

## 12. Testing Strategy

Unit tests:

- Required-scope registry.
- Blocker policy decisions.
- Repair action selection.
- Blocker receipt schema.

Integration tests:

- Provider command blocked.
- Render command blocked for revoked likeness.
- Publishing intent blocked.
- Memory admission blocked.
- Future reuse re-checks active consent.

Safety tests:

- Consent-sensitive workflows default to blocked when mapping missing.
- Durable workflow re-checks consent before external side effect.

## 13. Observability, Recovery, and Rollback

- Logs include `consent_blocker_receipt_id`, `command_type`, `blocked_scope`, `object_id`, `organization_id`, and `brand_id`.
- Metrics track blocked command type, scope, pending work flags, and repair outcomes.
- Recovery can re-run impact analysis after consent changes.
- Rollback uses updated consent version or compensating command, not manual override.

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
| Requirement Trace | FR-CMF-02.03 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Governance gates mapped to Python blocker policy and receipts |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python consent guard; Pi cannot bypass current consent |
| TypeScript Boundary | Surfaces only show decisions and repair options |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

