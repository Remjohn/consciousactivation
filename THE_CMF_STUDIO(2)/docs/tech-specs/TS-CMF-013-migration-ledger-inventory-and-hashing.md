---
tech_spec_id: "TS-CMF-013"
title: "Migration Ledger Inventory and Hashing"
story_id: "3.1"
story_title: "Migration Ledger Inventory and Hashing"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-3-1-migration-ledger-inventory-and-hashing.md"
fr_ids:
  - "FR-CMF-03.01"
  - "FR-CMF-03.08"
pipeline_stage: "0"
entry_object: "legacy source path"
exit_object: "MigrationLedgerEntry"
validation_contract: "hash and migration target"
required_receipt: "migration receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / PostgreSQL / content hashing"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-013: Migration Ledger Inventory and Hashing

**Status:** Ready for Development  
**Story:** `3.1 - Migration Ledger Inventory and Hashing`  
**Implementation Boundary:** Legacy asset inventory, content hashes, migration ledger entries, migration target mapping, review status, and migration receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for the 1686-file Legacy Inventory, Greenfield Rule, and migration target fields. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-03.01 and FR-CMF-03.08 source authority. |
| `docs/architecture.md` | Architecture authority for legacy migration objects, legacy-coupling ban, and migration workflow. |
| `docs/cmf-studio-pipeline-map.md` | Stage 0 legacy inventory and migration trace. |
| `docs/migration/legacy-inventory.md` | Primary source for migration ledger fields, high-value module inventory, and legacy-runtime-coupling prohibition. |
| `docs/stories/story-3-1-migration-ledger-inventory-and-hashing.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md` | Command and receipt dependency. |
| `docs/tech-specs/TS-CMF-002-pipeline-stage-orchestration-records.md` | Stage execution dependency. |

## 2. Overview

### Problem Statement

CMF STUDIO must preserve valuable legacy intelligence without inheriting runtime fragmentation. If a legacy asset is reused without source path, hash, owner, defects, target package, contract target, fixture target, eval target, and reviewer, agents can cite stale doctrine or import old code without provenance.

### Solution

Implement a migration ledger that records every retained legacy asset as an immutable, reviewable, hash-backed entry. Migration Stewards classify source paths, assign canonicality confidence, define target Python/Pydantic/DSPy/fixture/eval destinations, and write migration receipts. Hash drift triggers review rather than silent canonical updates.

### Scope

In scope:

- `LegacyAssetInventoryItem`, `MigrationLedgerEntry`, `MigrationTargetMap`, `MigrationReviewState`, and `MigrationReceipt`.
- Content hashing for legacy assets.
- Ledger commands for propose, map, approve, block, refresh hash, and inspect.
- Hash-change detection and review flagging.
- Blocked asset references with approved reason and replacement target.

Out of scope:

- Actual registry conversion. Covered by TS-CMF-014.
- JIT compiler execution. Covered by TS-CMF-015.
- CI import scanning. Covered by TS-CMF-016.
- Direct mutation of the legacy repository.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-03.01 | Migration Stewards inventory, classify, hash, map, convert, validate, approve, deprecate, or block legacy assets. | Ledger commands, content hashes, classification fields, target mapping, review states, block reasons, and migration receipts. |
| FR-CMF-03.08 | Every migrated registry/compiler has Pydantic target, DSPy target when applicable, fixture, eval, reviewer, defects, and status. | `MigrationTargetMap`, required field validation, reviewer status, defect notes, and activation preconditions. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `0 - Legacy inventory and migration` |
| Entry Object | Legacy source path |
| Exit Object | `MigrationLedgerEntry` |
| Allowed Actors / Services | Migration Steward, Architecture Reviewer, MigrationWorkflow, Command Bus |
| Validation Contract | Content hash, classification, target map, reviewer, and migration status |
| Required Receipt | Migration receipt |
| Forbidden Shortcut | Reusing legacy asset without ledger entry, silent hash update, legacy runtime coupling, targetless migration |

### Legacy Intelligence Mapping

The Legacy Inventory is the primary source. It states that legacy files serve as read-only registry, doctrine, fixture, example, provider-code source, or worker asset source. Legacy code is never coupled into production runtime as-is. This spec creates the runtime record that lets later agents know what a legacy asset is allowed to become.

Target modules:

- `ccp_studio.contracts.legacy`
- `ccp_studio.services.migration_service`
- `ccp_studio.workflows.migration_workflow`
- `ccp_studio.repositories.legacy_inventory_items`
- `ccp_studio.repositories.migration_ledger_entries`
- `ccp_studio.api.v1.legacy_migration`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `LegacyAssetInventoryItem` | Source path, type, registry family, owner, language, canonicality, mechanics, defects, and hash. |
| `MigrationTargetMap` | Target Python package, Pydantic contract, DSPy program, TypeScript leaf target if any, fixture, eval, and reviewer. |
| `MigrationLedgerEntry` | Lifecycle record for migration status and approved disposition. |
| `MigrationReceipt` | Receipt for propose, map, approve, block, or hash-review actions. |
| `HashReviewFlag` | Review signal when source hash changes. |

## 4. Implementation Plan

### Workstream A: Contracts

Define inventory item, migration target, status, hash review, block reason, and receipt contracts.

### Workstream B: Persistence

Add `legacy_inventory_items`, `migration_ledger_entries`, `migration_target_maps`, and `migration_receipts`.

### Workstream C: Hashing and Refresh

Implement deterministic content hashing and refresh jobs. A changed hash creates `HashReviewFlag` and blocks activation until reviewed.

### Workstream D: Ledger Commands

Implement propose, map, approve, block, deprecate, inspect, and refresh commands through the Command Bus.

### Workstream E: Reference Resolution

When an agent references a blocked or deprecated asset, return the approved reason and replacement target when available.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class LegacyAssetStatus(str, Enum):
    proposed = "proposed"
    mapped = "mapped"
    approved = "approved"
    blocked = "blocked"
    deprecated = "deprecated"
    needs_hash_review = "needs_hash_review"


class LegacyDisposition(str, Enum):
    doctrine = "doctrine"
    registry = "registry"
    fixture = "fixture"
    eval_target = "eval_target"
    reference_implementation = "reference_implementation"
    worker_asset = "worker_asset"
    deprecated_runtime = "deprecated_runtime"


class MigrationTargetMap(BaseModel):
    schema_version: Literal["cmf.migration_target_map.v1"]
    target_python_package: str | None = None
    pydantic_contract_target: str | None = None
    dspy_program_target: str | None = None
    typescript_leaf_target: str | None = None
    fixture_target: str | None = None
    eval_target: str | None = None
    reviewer_actor_id: UUID | None = None


class MigrationLedgerEntry(BaseModel):
    schema_version: Literal["cmf.migration_ledger_entry.v1"]
    migration_ledger_entry_id: UUID
    source_path: str
    legacy_type: str
    registry_family: str | None = None
    canonicality_confidence: float
    source_owner: str
    runtime_language: str | None = None
    valuable_mechanics: list[str]
    known_defects: list[str] = Field(default_factory=list)
    content_hash: str
    disposition: LegacyDisposition
    target_map: MigrationTargetMap
    status: LegacyAssetStatus
    created_at: datetime
    updated_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `ProposeLegacyAssetCommand`, `MapLegacyAssetCommand`, `ApproveLegacyAssetCommand`, `BlockLegacyAssetCommand`, `RefreshLegacyAssetHashCommand`, `InspectMigrationLedgerCommand` |
| Events | `LegacyAssetProposed`, `MigrationTargetMapped`, `LegacyAssetApproved`, `LegacyAssetBlocked`, `LegacyAssetHashChanged`, `MigrationReceiptWritten` |
| Workflows | `MigrationWorkflow`, hash refresh workflow, blocked reference resolution workflow |
| Receipts | `MigrationReceipt`, `HashReviewReceipt`, `BlockedReferenceReceipt` |

## 7. Backward Compatibility and Migration Fallback

No legacy runtime compatibility path exists. Legacy items without ledger entries are unknown and cannot be activated. Hash changes do not auto-update canonical source.

Fallback behavior:

- Missing ledger entry returns `LEGACY_ASSET_NOT_LEDGERED`.
- Missing content hash returns `LEGACY_CONTENT_HASH_REQUIRED`.
- Missing migration target returns `MIGRATION_TARGET_REQUIRED`.
- Hash drift returns `LEGACY_HASH_REVIEW_REQUIRED`.
- Blocked asset reference returns `LEGACY_ASSET_BLOCKED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Reuse legacy intelligence quickly; preserve provenance and avoid inheriting runtime disorder. |
| UX / Ops Failure Scenario | An agent cites an old prompt or module with no hash, target, reviewer, or replacement path, producing untraceable production behavior. |
| Resolution Demand | Migration ledger authority takes precedence. No legacy asset influences production until inventoried, hashed, mapped, reviewed, and receipted. |
| Downstream Proof | Tests must prove target fields are required, hash drift blocks activation, blocked assets return reason/replacement, and ledger changes write receipts. |

## 9. Tasks

- Define legacy migration contracts.
- Add ledger persistence.
- Implement content hashing.
- Implement migration commands.
- Add hash refresh workflow.
- Add blocked asset reference resolver.
- Add tests for required target fields and hash drift.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Ledger entry records source path, type, family, confidence, owner, language, mechanics, defects, hash, and status. | Entry only stores filename and notes. |
| AC2 | Target map includes Python package, Pydantic target, DSPy target where applicable, TypeScript leaf target if any, fixture, eval, and reviewer. | Archetype prompt has no eval target. |
| AC3 | Hash change flags asset for review. | Hash silently updates and stays approved. |
| AC4 | Blocked asset returns reason and replacement target. | Agent receives raw blocked prompt text. |
| AC5 | Approved ledger changes write migration receipt. | Status changes with no receipt. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-002 Orchestration records
- TS-CMF-003 Spec governance workflow
- TS-CMF-004 Workspace lifecycle

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- Hashing library from Python standard library

## 12. Testing Strategy

Unit tests:

- Ledger schema required fields.
- Hash generation and comparison.
- Target map validation.
- Blocked reference resolution.

Integration tests:

- Propose asset, map target, approve, write receipt.
- Change hash and require review.
- Block asset and resolve replacement.
- Inspect ledger by source path.

Safety tests:

- Asset cannot activate without ledger entry.
- Asset cannot activate without target map.
- Approved status cannot be set without reviewer and receipt.

## 13. Observability, Recovery, and Rollback

- Logs include `migration_ledger_entry_id`, `source_path`, `content_hash`, `status`, and reviewer.
- Metrics track proposed, mapped, approved, blocked, deprecated, and hash-review assets.
- Recovery rebuilds active migration index from ledger entries and receipts.
- Rollback marks a new ledger status and writes receipt; prior entries remain auditable.

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
| Requirement Trace | FR-CMF-03.01, FR-CMF-03.08 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Primary authority for fields and Greenfield Rule |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python ledger with Pydantic targets and Pi through commands |
| TypeScript Boundary | Leaf target only when permitted |
| Legacy Runtime Coupling | Forbidden by design |
| Verdict | Accepted for implementation |

