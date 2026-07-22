---
tech_spec_id: "TS-CMF-018"
title: "Brand Genesis Intake and Session Creation"
story_id: "4.1"
story_title: "Brand Genesis Intake and Session Creation"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-4-1-brand-genesis-intake-and-session-creation.md"
fr_ids:
  - "FR-CMF-04.01"
pipeline_stage: "2"
entry_object: "brand intake and consent"
exit_object: "BrandGenesisSession"
validation_contract: "source/consent completeness"
required_receipt: "genesis start receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / durable workflows / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-018: Brand Genesis Intake and Session Creation

**Status:** Ready for Development  
**Story:** `4.1 - Brand Genesis Intake and Session Creation`  
**Implementation Boundary:** Brand Genesis session creation, intake contracts, consent/source validation, brand-scoped storage, and genesis start receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for Brand Genesis as upfront locked creative substrate. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-04.01 source authority. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis Session, Brand Context Version, intake, likeness consent, source photo, identity summary, and control tower doctrine. |
| `docs/architecture.md` | Architecture authority for BrandGenesisWorkflow, BrandContextVersion, consent/source gates, and object storage. |
| `docs/cmf-studio-pipeline-map.md` | Stage 2 Brand Genesis trace. |
| `docs/migration/legacy-inventory.md` | Visual/sonic doctrine, Voice DNA references, and legacy-runtime-coupling context. |
| `docs/stories/story-4-1-brand-genesis-intake-and-session-creation.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-008-versioned-consent-records.md` | Consent dependency. |
| `docs/tech-specs/TS-CMF-009-recording-setup-and-source-artifact-gate.md` | Source artifact dependency. |

## 2. Overview

### Problem Statement

Brand Genesis manufactures the reusable creative universe before production begins. If the system starts generation from incomplete intake, missing likeness consent, weak source media, or vague preferences, later SceneSpecs and render jobs will reinvent the brand clip by clip.

### Solution

Implement `BrandGenesisSession` as the stage-2 entrypoint. The session captures brand notes, audience, offer, forbidden tone, visual preferences, Voice DNA references, source media, negative-space inputs, and consent compatibility. Generation cannot start until source and consent completeness pass and a genesis start receipt is written.

### Scope

In scope:

- `BrandGenesisSession`, `BrandSourceInput`, `VoiceDnaReference`, `VisualConstitutionInput`, `NegativeSpaceInput`, and `GenesisStartReceipt`.
- Consent compatibility before likeness or source use.
- Brand-scoped object storage under `brands/{brand_id}/brand-genesis/`.
- Missing evidence reports instead of fabricated brand constitution.
- Cross-brand access blocking.

Out of scope:

- Acting library generation. Covered by TS-CMF-019.
- Rig and creative libraries. Covered by TS-CMF-020.
- Brand Context locking. Covered by TS-CMF-021.
- UI design details.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-04.01 | Operators run Brand Genesis from intake, consent, sources, brand notes, audience, offer, forbidden tone, visual preferences, Voice DNA, visual constitution, and negative-space inputs. | `BrandGenesisSession`, required intake validation, consent/source checks, brand-scoped storage, and genesis start receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `2 - Brand Genesis` |
| Entry Object | Brand intake and consent |
| Exit Object | `BrandGenesisSession` |
| Allowed Actors / Services | Operator, BrandGenesisWorkflow, ConsentPolicyService, SourceIngestionService, VoiceDNA reference resolver |
| Validation Contract | Source and consent completeness |
| Required Receipt | Genesis start receipt |
| Forbidden Shortcut | Generating brand assets without consent, source media, negative-space inputs, or brand scope |

### Legacy Intelligence Mapping

Brand Genesis V3 and legacy visual/sonic doctrine are source materials, not runtime imports. Voice DNA references must point to migrated contracts or approved reference records. The session belongs to the Python workflow and writes typed events and receipts.

Target modules:

- `ccp_studio.contracts.brand_genesis`
- `ccp_studio.contracts.brand_context`
- `ccp_studio.services.brand_genesis_service`
- `ccp_studio.workflows.brand_genesis`
- `ccp_studio.repositories.brand_genesis_sessions`
- `ccp_studio.api.v1.brand_genesis`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `BrandGenesisSession` | Stateful workflow object for a brand's creative-universe manufacturing run. |
| `BrandSourceInput` | Source media, photo/video refs, hashes, consent links, and quality status. |
| `VoiceDnaReference` | Approved Voice DNA or calibration reference, never raw prompt text. |
| `VisualConstitutionInput` | Visual preferences, style constraints, paper-cut direction, composition preferences. |
| `NegativeSpaceInput` | Forbidden tone, forbidden visual motifs, avoided claims, and style boundaries. |
| `GenesisStartReceipt` | Proof that session started with required evidence. |

## 4. Implementation Plan

### Workstream A: Contracts

Define intake, source, Voice DNA, visual constitution, negative-space, session status, and receipt models.

### Workstream B: Session Command

Implement `CreateBrandGenesisSessionCommand` through Command Bus with role, brand scope, consent, source, and receipt validation.

### Workstream C: Intake Completeness

Create missing evidence report for incomplete intake. Do not synthesize missing brand constitution fields.

### Workstream D: Storage and Scope

Store genesis artifacts under brand-scoped paths and deny cross-brand query or reuse.

### Workstream E: Workflow Start

Open `BrandGenesisWorkflow` only after start receipt is written.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class BrandGenesisSessionStatus(str, Enum):
    draft = "draft"
    ready = "ready"
    blocked = "blocked"
    running = "running"
    completed = "completed"


class BrandSourceInput(BaseModel):
    schema_version: Literal["cmf.brand_source_input.v1"]
    source_artifact_ids: list[UUID]
    consent_record_version_id: UUID
    source_quality_receipt_ids: list[UUID] = Field(default_factory=list)


class BrandGenesisSession(BaseModel):
    schema_version: Literal["cmf.brand_genesis_session.v1"]
    brand_genesis_session_id: UUID
    organization_id: UUID
    brand_id: UUID
    status: BrandGenesisSessionStatus
    brand_notes: str
    audience_summary: str
    offer_summary: str
    forbidden_tone: list[str]
    visual_preferences: list[str]
    voice_dna_reference_ids: list[UUID] = Field(default_factory=list)
    source_inputs: list[BrandSourceInput]
    negative_space_inputs: list[str]
    created_by_actor_id: UUID
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `CreateBrandGenesisSessionCommand`, `ValidateBrandGenesisIntakeCommand`, `StartBrandGenesisWorkflowCommand`, `BlockBrandGenesisForConsentCommand` |
| Events | `BrandGenesisSessionCreated`, `BrandGenesisIntakeValidated`, `BrandGenesisStartBlocked`, `BrandGenesisWorkflowStarted` |
| Workflows | `BrandGenesisWorkflow` start workflow |
| Receipts | `GenesisStartReceipt`, `ConsentBlockerReceipt`, `AuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy Brand Genesis and visual constitution documents are doctrine. Any source media or Voice DNA record must be migrated into approved contracts before the session can use it.

Fallback behavior:

- Missing consent returns `CONSENT_SCOPE_BLOCKED`.
- Missing intake returns `BRAND_GENESIS_INTAKE_INCOMPLETE`.
- Missing source returns `BRAND_SOURCE_REQUIRED`.
- Cross-brand query returns `BRAND_SCOPE_VIOLATION`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Operators want immediate visual generation; Brand Genesis requires grounded creative truth before asset production. |
| UX / Ops Failure Scenario | The system fabricates a brand constitution from vague notes and later locks identity assets that do not match the client. |
| Resolution Demand | Intake completeness and consent/source truth take precedence. Generation cannot start without required evidence and receipt. |
| Downstream Proof | Tests must block missing consent, incomplete intake, and cross-brand reuse, and prove start receipt is written before workflow execution. |

## 9. Tasks

- Define Brand Genesis intake contracts.
- Add session persistence.
- Implement intake completeness validator.
- Integrate consent/source checks.
- Implement start command and workflow opening.
- Add brand-scoped storage rules.
- Add tests for missing evidence and cross-brand blocking.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Session records notes, audience, offer, forbidden tone, visual preferences, Voice DNA refs, source media, negative-space inputs, and consent compatibility. | Session created with brand name only. |
| AC2 | Source media without consent blocks start. | Likeness generation starts from unconsented photo. |
| AC3 | Incomplete intake shows missing evidence. | System invents visual constitution from generic defaults. |
| AC4 | Passing intake writes `BrandGenesisSession` and receipt. | Workflow starts with no genesis start receipt. |
| AC5 | Session cannot be queried or reused across brand boundaries. | Brand B selects Brand A genesis source. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-004 Workspace lifecycle
- TS-CMF-008 Consent records
- TS-CMF-009 Source artifact gate
- TS-CMF-013 Migration ledger

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- Object storage
- Durable workflow runtime

## 12. Testing Strategy

Unit tests:

- Intake required field validation.
- Source/consent compatibility.
- Negative-space input validation.
- Brand scope validation.

Integration tests:

- Create valid Brand Genesis session.
- Block missing consent.
- Block incomplete intake.
- Start workflow and write receipt.
- Deny cross-brand session query.

Safety tests:

- Pi cannot start Brand Genesis without command receipt.
- Legacy Voice DNA reference must be migrated before use.
- Source artifacts must be brand-scoped.

## 13. Observability, Recovery, and Rollback

- Logs include `brand_genesis_session_id`, `organization_id`, `brand_id`, `consent_record_version_id`, and blocker codes.
- Metrics track session starts, missing evidence blocks, consent blocks, and cross-brand access blocks.
- Recovery resumes from last workflow receipt.
- Rollback cancels draft/running session by command; historical receipts remain.

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
| Requirement Trace | FR-CMF-04.01 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Brand Genesis V3 and visual/sonic doctrine as source only |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python workflow with Pi via typed commands |
| TypeScript Boundary | Generated UI consumers only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

