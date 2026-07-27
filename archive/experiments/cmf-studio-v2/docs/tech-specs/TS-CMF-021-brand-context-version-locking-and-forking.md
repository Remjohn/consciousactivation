---
tech_spec_id: "TS-CMF-021"
title: "Brand Context Version Locking and Forking"
story_id: "4.4"
story_title: "Brand Context Version Locking and Forking"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-4-4-brand-context-version-locking-and-forking.md"
fr_ids:
  - "FR-CMF-04.06"
  - "FR-CMF-04.07"
pipeline_stage: "2"
entry_object: "approved genesis assets"
exit_object: "locked/forked BrandContextVersion"
validation_contract: "review and version immutability"
required_receipt: "genesis clearance receipt"
runtime_target: "Python / Pydantic v2 / immutable versioning / object storage / event outbox"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-021: Brand Context Version Locking and Forking

**Status:** Ready for Development  
**Story:** `4.4 - Brand Context Version Locking and Forking`  
**Implementation Boundary:** Immutable Brand Context Versions, Genesis Clearance Certificates, version hashes, fork workflow, and historical render lineage.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Immutable BrandContextVersion object and fork-on-change doctrine. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-04.06 and FR-CMF-04.07 source authority. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Context Version schema, lock process, app screens, lifecycle, and evaluation doctrine. |
| `docs/architecture.md` | Architecture authority for immutable Brand Context Versions, GenesisClearanceCertificate, object storage, and downstream references. |
| `docs/cmf-studio-pipeline-map.md` | Stage 2 Brand Genesis trace and production lock boundaries. |
| `docs/migration/legacy-inventory.md` | Legacy CMF visual/sonic doctrine as source context. |
| `docs/stories/story-4-4-brand-context-version-locking-and-forking.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-018-brand-genesis-intake-and-session-creation.md` | Session dependency. |
| `docs/tech-specs/TS-CMF-019-64-state-acting-library.md` | Acting library dependency. |
| `docs/tech-specs/TS-CMF-020-paper-cut-rig-and-creative-libraries.md` | Rig and creative library dependency. |

## 2. Overview

### Problem Statement

If Brand Context can be edited in place, historical outputs lose their creative truth. A render made with Brand Context v1 must always resolve to that exact identity substrate, even if the Operator later changes props, motion rules, anchors, or visual identity.

### Solution

Implement immutable locked `BrandContextVersion` records. Locking requires approved genesis assets and writes a `GenesisClearanceCertificate`. Any core identity or creative-rule change forks a new version. Downstream SceneSpecs, RenderContracts, provider jobs, evaluation receipts, and reviews store the version ID and hash they used.

### Scope

In scope:

- `BrandContextVersion`, `GenesisClearanceCertificate`, `BrandContextVersionHash`, `BrandContextForkRequest`, and `BrandContextLineageRef`.
- Lock workflow after required genesis assets pass review.
- Fork workflow for approved changes.
- Historical context resolution.
- Blocking stale or cross-brand version selection.

Out of scope:

- Production SceneSpec gate details. Covered by TS-CMF-022.
- New creative asset generation. Covered by TS-CMF-019 and TS-CMF-020.
- Manual UI details.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-04.06 | System forks Brand Context Versions for approved changes while preserving historical outputs against their original locked context. | Immutable `BrandContextVersion`, fork command, parent version reference, version hash, and historical lineage refs. |
| FR-CMF-04.07 | System prevents production jobs using unapproved, unlocked, stale, or cross-brand identity assets. | Lock state validation, GenesisClearanceCertificate, brand scope guard, stale/superseded policy, and downstream gate. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `2 - Brand Genesis` |
| Entry Object | Approved genesis assets |
| Exit Object | Locked or forked `BrandContextVersion` |
| Allowed Actors / Services | Operator, BrandGenesisWorkflow, ReviewService, BrandContextService, Command Bus |
| Validation Contract | Review and version immutability |
| Required Receipt | Genesis clearance receipt |
| Forbidden Shortcut | In-place mutation of locked context, production reference to draft context, cross-brand context selection |

### Legacy Intelligence Mapping

Brand Genesis V3 versioning doctrine is source authority. The implementation uses Python contracts and database immutability rules. Legacy or generated assets must enter through approved genesis asset records with hashes and receipts.

Target modules:

- `ccp_studio.contracts.brand_context`
- `ccp_studio.services.brand_context_service`
- `ccp_studio.workflows.brand_context_lock`
- `ccp_studio.repositories.brand_context_versions`
- `ccp_studio.repositories.genesis_clearance_certificates`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `BrandContextVersion` | Immutable creative truth bundle for a brand. |
| `GenesisClearanceCertificate` | Lock proof for acting library, rig, props, anchors, motion, SFX, platform profiles, and evaluation receipts. |
| `BrandContextForkRequest` | Approved change request that creates a child version. |
| `BrandContextLineageRef` | Version ID/hash reference stored downstream. |
| `BrandContextVersionHash` | Integrity hash over included locked assets and policy refs. |

## 4. Implementation Plan

### Workstream A: Contracts

Define version, clearance certificate, hash, fork request, and lineage ref contracts.

### Workstream B: Lock Workflow

Require all required genesis assets to be approved and evaluated before lock. Write certificate and lock event.

### Workstream C: Immutability Enforcement

Add repository and database rules preventing mutation after lock.

### Workstream D: Fork Workflow

Core changes create a forked version with parent reference, approved change reason, and fresh evaluation requirements.

### Workstream E: Historical Resolution

Expose exact locked version lookup for old renders, SceneSpecs, and review views.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class BrandContextStatus(str, Enum):
    draft = "draft"
    locked = "locked"
    superseded = "superseded"
    archived = "archived"


class GenesisClearanceCertificate(BaseModel):
    schema_version: Literal["cmf.genesis_clearance_certificate.v1"]
    genesis_clearance_certificate_id: UUID
    brand_context_version_id: UUID
    acting_library_version_id: UUID
    rig_manifest_id: UUID
    creative_library_receipt_ids: list[UUID]
    evaluation_receipt_ids: list[UUID]
    approved_by_actor_id: UUID
    issued_at: datetime


class BrandContextVersion(BaseModel):
    schema_version: Literal["cmf.brand_context_version.v1"]
    brand_context_version_id: UUID
    organization_id: UUID
    brand_id: UUID
    parent_brand_context_version_id: UUID | None = None
    status: BrandContextStatus
    version_hash: str
    acting_library_version_id: UUID
    rig_manifest_id: UUID
    prop_library_version_id: UUID | None = None
    micro_semiotic_anchor_library_version_id: UUID | None = None
    motion_recipe_library_version_id: UUID | None = None
    sfx_library_version_id: UUID | None = None
    platform_profile_version_id: UUID | None = None
    clearance_certificate_id: UUID | None = None
    locked_at: datetime | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `CreateBrandContextDraftCommand`, `LockBrandContextVersionCommand`, `ForkBrandContextVersionCommand`, `ResolveBrandContextLineageCommand`, `BlockStaleBrandContextCommand` |
| Events | `BrandContextVersionDrafted`, `GenesisClearanceCertificateIssued`, `BrandContextVersionLocked`, `BrandContextVersionForked`, `BrandContextVersionSuperseded` |
| Workflows | Brand context lock workflow, fork workflow, lineage resolution workflow |
| Receipts | `GenesisClearanceReceipt`, `BrandContextForkReceipt`, `BrandContextGateReceipt` |

## 7. Backward Compatibility and Migration Fallback

Historical outputs are never rewritten to a newer context. Legacy Brand Context-like assets must be ledgered, evaluated, and locked into a version before use.

Fallback behavior:

- Missing clearance certificate returns `GENESIS_CLEARANCE_REQUIRED`.
- Draft context returns `BRAND_CONTEXT_NOT_LOCKED`.
- In-place mutation returns `BRAND_CONTEXT_IMMUTABLE`.
- Cross-brand context returns `BRAND_SCOPE_VIOLATION`.
- Superseded context in new production returns `BRAND_CONTEXT_SUPERSEDED_REVIEW_REQUIRED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Operators need to improve the brand over time; historical outputs need immutable creative truth. |
| UX / Ops Failure Scenario | A prop change silently alters old render lineage, making evaluation and memory untrustworthy. |
| Resolution Demand | Version immutability takes precedence. Any approved change forks a new Brand Context Version, and old outputs keep their original version. |
| Downstream Proof | Tests must prove locked versions cannot mutate, forks retain parent refs, old renders resolve original version, and stale/cross-brand versions block production. |

## 9. Tasks

- Define Brand Context contracts.
- Add persistence and immutability constraints.
- Implement lock command and clearance certificate.
- Implement fork command.
- Implement lineage lookup.
- Add stale/cross-brand gates.
- Add tests for immutable lock and forks.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Lock writes `GenesisClearanceCertificate` after all assets pass review. | Brand context locks with failed rig preview. |
| AC2 | Production can select only assets approved within locked version. | SceneSpec selects draft anchor. |
| AC3 | Core visual identity change creates fork instead of mutating old version. | Prop is edited inside v1. |
| AC4 | Old render resolves exact locked version used at render time. | Old render points to latest context. |
| AC5 | Stale or cross-brand version blocks SceneSpec compilation. | Brand A job uses Brand B context. |

## 11. Dependencies

Internal:

- TS-CMF-018 Brand Genesis session
- TS-CMF-019 Acting library
- TS-CMF-020 Creative libraries
- TS-CMF-010 Consent blockers

External:

- Pydantic v2
- PostgreSQL
- Object storage
- Event outbox

## 12. Testing Strategy

Unit tests:

- Version hash calculation.
- Clearance certificate requiredness.
- Immutable status behavior.
- Fork parent reference.

Integration tests:

- Lock approved context.
- Block lock with missing asset.
- Fork context.
- Resolve old render lineage.
- Block stale/cross-brand selection.

Safety tests:

- Database/repository prevents locked context mutation.
- SceneSpec cannot reference draft context.
- Provider job includes version ID and hash.

## 13. Observability, Recovery, and Rollback

- Logs include `brand_context_version_id`, `version_hash`, `parent_id`, status, and clearance certificate.
- Metrics track locks, forks, stale blocks, cross-brand blocks, and immutability violations.
- Recovery rebuilds context index from lock/fork events.
- Rollback forks a replacement or supersedes a version; it never edits locked versions.

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
| Requirement Trace | FR-CMF-04.06, FR-CMF-04.07 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Brand Genesis V3 versioning doctrine as source |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python immutable version contracts; Pi cannot mutate locked context |
| TypeScript Boundary | UI consumes lineage/read models only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

