---
tech_spec_id: "TS-CMF-019"
title: "64-State Acting Library"
story_id: "4.2"
story_title: "64-State Acting Library"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-4-2-64-state-acting-library.md"
fr_ids:
  - "FR-CMF-04.02"
  - "FR-CMF-04.05"
pipeline_stage: "2"
entry_object: "brand source and generation request"
exit_object: "acting library version"
validation_contract: "likeness/gesture/style gate"
required_receipt: "acting library receipt"
runtime_target: "Python / Pydantic v2 / provider adapters / ImageCritic / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-019: 64-State Acting Library

**Status:** Ready for Development  
**Story:** `4.2 - 64-State Acting Library`  
**Implementation Boundary:** Acting library generation, 8x8 state metadata, provider receipts, ImageCritic evaluation, repair/reject/approve flow, and locked acting library versions.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | 64-state acting library, ImageCritic scoring, and Brand Context lock doctrine. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-04.02 and FR-CMF-04.05 source authority. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Emotional/gesture families, 8x8 matrix, acting reference metadata, generation strategy, and lock rules. |
| `docs/architecture.md` | Architecture source for acting library, evaluation receipts, provider boundaries, and immutable versions. |
| `docs/cmf-studio-pipeline-map.md` | Stage 2 Brand Genesis trace. |
| `docs/migration/legacy-inventory.md` | Legacy visual doctrine and Voice DNA context. |
| `docs/stories/story-4-2-64-state-acting-library.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-018-brand-genesis-intake-and-session-creation.md` | Brand Genesis session dependency. |

## 2. Overview

### Problem Statement

Without a locked acting library, every scene asks a generative provider to rediscover the client's face, body language, hands, and emotional range. This creates identity drift, hand failures, inconsistent style, and unusable gestures.

### Solution

Implement a versioned 64-state acting library. Each reference is assigned an emotional family and gesture family, linked to source inputs and provider receipts, evaluated for likeness, gesture clarity, hand quality, style adherence, negative space, and production usability, and then rejected, repaired, replaced, approved, or locked as part of an immutable library version.

### Scope

In scope:

- `ActingLibraryVersion`, `ActingReference`, `ActingStateCell`, `ActingReferenceEvaluation`, and `ActingLibraryReceipt`.
- 8 emotional families x 8 gesture/body-language families.
- Provider receipt linkage and source input linkage.
- ImageCritic/evaluation receipts and human review states.
- Blocking unapproved references from SceneSpec compilation.

Out of scope:

- Provider-specific image generation internals.
- Paper-cut rig decomposition. Covered by TS-CMF-020.
- Final production SceneSpec compilation. Covered by later production specs.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-04.02 | Operators generate, evaluate, repair, reject, approve, and lock a 64-state acting library across emotional and gesture families. | Acting library version, acting reference state machine, provider receipts, repair/reject/approve commands, and lock receipt. |
| FR-CMF-04.05 | System scores references for likeness, gesture clarity, hand quality, paper texture, style adherence, negative space, and usability. | `ActingReferenceEvaluation`, ImageCritic result, human review state, and evaluation receipts. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `2 - Brand Genesis` |
| Entry Object | Brand source and generation request |
| Exit Object | Acting library version |
| Allowed Actors / Services | Operator, BrandGenesisWorkflow, ProviderAdapter, ImageCritic, EvaluationService |
| Validation Contract | Likeness, gesture, hand, style, negative-space, and usability gate |
| Required Receipt | Acting library receipt |
| Forbidden Shortcut | Using unapproved reference, mutating locked library version, treating provider output as approved identity |

### Legacy Intelligence Mapping

Brand Genesis V3 defines the acting matrix and metadata. Provider outputs and legacy visual doctrine are only inputs to the new Python contracts. ImageCritic acts as an evaluation layer, not final authority; human approval is required for lock.

Target modules:

- `ccp_studio.contracts.acting_library`
- `ccp_studio.services.acting_library_service`
- `ccp_studio.services.image_critic_service`
- `ccp_studio.workflows.brand_genesis`
- `ccp_studio.repositories.acting_references`
- `ccp_studio.repositories.acting_library_versions`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `ActingStateCell` | Emotional family and gesture family grid coordinate. |
| `ActingReference` | Generated or repaired image reference with source/provider/eval state. |
| `ActingReferenceEvaluation` | Likeness, gesture, hands, paper texture, style, negative-space, and usability scores. |
| `ActingLibraryVersion` | Immutable set of approved acting references. |
| `ActingLibraryReceipt` | Generation, repair, approval, rejection, or lock receipt. |

## 4. Implementation Plan

### Workstream A: Contracts

Define acting matrix, reference, evaluation, library version, review state, and receipt contracts.

### Workstream B: Generation and Provider Linkage

Create provider job requests through approved adapters and store provider receipts with each reference.

### Workstream C: Evaluation

Run ImageCritic/evaluation and store score vectors and failure instructions.

### Workstream D: Review State Machine

Allow reject, repair, replace, approve, and lock commands. Locked references are immutable.

### Workstream E: SceneSpec Guard

Expose approved-only selection validation to SceneSpec compilers.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ActingReferenceStatus(str, Enum):
    generated = "generated"
    repair_requested = "repair_requested"
    rejected = "rejected"
    approved = "approved"
    locked = "locked"


class ActingStateCell(BaseModel):
    schema_version: Literal["cmf.acting_state_cell.v1"]
    emotional_family: str
    gesture_family: str
    matrix_row: int
    matrix_column: int


class ActingReferenceEvaluation(BaseModel):
    schema_version: Literal["cmf.acting_reference_evaluation.v1"]
    evaluation_receipt_id: UUID
    likeness_score: float
    gesture_clarity_score: float
    hand_quality_score: float
    paper_texture_score: float
    style_adherence_score: float
    negative_space_score: float
    production_usability_score: float
    failure_notes: list[str] = Field(default_factory=list)


class ActingReference(BaseModel):
    schema_version: Literal["cmf.acting_reference.v1"]
    acting_reference_id: UUID
    brand_id: UUID
    state_cell: ActingStateCell
    source_artifact_ids: list[UUID]
    provider_receipt_id: UUID
    artifact_uri: str
    content_hash: str
    status: ActingReferenceStatus
    latest_evaluation: ActingReferenceEvaluation | None = None


class ActingLibraryVersion(BaseModel):
    schema_version: Literal["cmf.acting_library_version.v1"]
    acting_library_version_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    version_hash: str
    acting_reference_ids: list[UUID]
    locked: bool
    locked_at: datetime | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `GenerateActingReferenceGridCommand`, `EvaluateActingReferenceCommand`, `RejectActingReferenceCommand`, `RepairActingReferenceCommand`, `ApproveActingReferenceCommand`, `LockActingLibraryVersionCommand` |
| Events | `ActingReferenceGenerated`, `ActingReferenceEvaluated`, `ActingReferenceRejected`, `ActingReferenceApproved`, `ActingLibraryVersionLocked` |
| Workflows | Acting library generation workflow, repair workflow, approval workflow |
| Receipts | `ActingLibraryReceipt`, `ProviderReceipt`, `EvaluationReceipt`, `ApprovalReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy 64-state doctrine is source context. Any old image assets must be ledgered, hashed, evaluated, and approved before use.

Fallback behavior:

- Missing provider receipt returns `PROVIDER_RECEIPT_REQUIRED`.
- Failed likeness/gesture/style gate returns `ACTING_REFERENCE_EVALUATION_FAILED`.
- Unapproved reference returns `ACTING_REFERENCE_NOT_APPROVED`.
- Locked version mutation returns `ACTING_LIBRARY_VERSION_IMMUTABLE`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Generative speed wants instant scene-specific poses; brand stability requires a reviewed acting library first. |
| UX / Ops Failure Scenario | A scene uses a new provider-generated pose with weak likeness or broken hands because no approved reference existed. |
| Resolution Demand | Acting library gate takes precedence. Production may only use approved references from locked versions. |
| Downstream Proof | Tests must prove failed evaluations block approval, locked versions are immutable, unapproved references cannot compile into SceneSpec, and historical outputs retain original version. |

## 9. Tasks

- Define acting library contracts.
- Implement 8x8 matrix generation requests.
- Link provider receipts and source inputs.
- Implement ImageCritic/evaluation storage.
- Implement review state machine.
- Implement lock command.
- Add SceneSpec selection guard.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Each reference includes emotional family, gesture family, sources, provider receipt, and evaluation state. | Image file saved without grid metadata. |
| AC2 | Failed reference can be rejected, repaired, or replaced. | Broken hand reference auto-approves. |
| AC3 | Approved references become immutable in locked library version. | Locked reference image is overwritten. |
| AC4 | Unapproved reference blocks SceneSpec compilation. | SceneSpec selects generated-but-unreviewed pose. |
| AC5 | Evaluation changes after lock do not rewrite historical outputs. | Old render points to newly repaired reference. |

## 11. Dependencies

Internal:

- TS-CMF-018 Brand Genesis session
- TS-CMF-010 Consent blockers
- TS-CMF-013 Migration ledger
- TS-CMF-014 Registry/eval targets

External:

- Pydantic v2
- Object storage
- Provider adapters
- ImageCritic/evaluation service

## 12. Testing Strategy

Unit tests:

- Acting state cell validation.
- Evaluation threshold behavior.
- Lock immutability.
- Provider receipt requiredness.

Integration tests:

- Generate grid and store references.
- Evaluate reference and block failed approval.
- Repair and approve reference.
- Lock acting library version.
- Block SceneSpec selection of unapproved reference.

Safety tests:

- Provider output cannot skip evaluation.
- Cross-brand reference selection fails.
- Locked library cannot be mutated.

## 13. Observability, Recovery, and Rollback

- Logs include `acting_reference_id`, `acting_library_version_id`, `provider_receipt_id`, scores, and status.
- Metrics track generated, failed, repaired, approved, rejected, and locked references.
- Recovery resumes from provider receipts and stored artifacts.
- Rollback forks a new version; it never mutates locked version.

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
| Requirement Trace | FR-CMF-04.02, FR-CMF-04.05 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Brand Genesis V3 acting-library doctrine as source |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python state machine and provider/eval receipts |
| TypeScript Boundary | Review grid consumes generated contracts only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

