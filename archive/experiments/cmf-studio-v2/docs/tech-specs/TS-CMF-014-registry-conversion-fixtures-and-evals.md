---
tech_spec_id: "TS-CMF-014"
title: "Registry Conversion, Fixtures, and Evals"
story_id: "3.2"
story_title: "Registry Conversion, Fixtures, and Evals"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-3-2-registry-conversion-fixtures-and-evals.md"
fr_ids:
  - "FR-CMF-03.02"
  - "FR-CMF-03.03"
  - "FR-CMF-03.08"
pipeline_stage: "0"
entry_object: "approved legacy asset"
exit_object: "registry, fixture, eval target"
validation_contract: "schema/eval activation gate"
required_receipt: "registry activation receipt"
runtime_target: "Python / Pydantic v2 / DSPy / tests fixtures / tests evals"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-014: Registry Conversion, Fixtures, and Evals

**Status:** Ready for Development  
**Story:** `3.2 - Registry Conversion, Fixtures, and Evals`  
**Implementation Boundary:** Migrated registries, fixture sets, evaluation targets, activation gate, registry conflict checks, and activation receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for primitives, SDA/SFL, archetypes, creative subsystems, CBAR, TTT, Voice DNA, fixtures, and eval gates. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-03.02, FR-CMF-03.03, and FR-CMF-03.08 source authority. |
| `docs/architecture.md` | Architecture authority for registries, DSPy program specs, fixture sets, evaluation targets, and activation gates. |
| `docs/cmf-studio-pipeline-map.md` | Stage 0 migration and registry activation trace. |
| `docs/migration/legacy-inventory.md` | Legacy source families and migration targets. |
| `docs/stories/story-3-2-registry-conversion-fixtures-and-evals.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-013-migration-ledger-inventory-and-hashing.md` | Ledger and target map dependency. |

## 2. Overview

### Problem Statement

The old system contains valuable archetype prompts, cognitive primitives, SDA/SFL registries, CBAR gates, TTT profiles, creative subsystem rules, Voice DNA logic, and CMF references. If these are copied as prompts or notes, production loses schema validation, examples, counterexamples, failure cases, and eval coverage. If CMF engine references are treated as live production code without approval, the greenfield runtime inherits old defects.

### Solution

Convert approved legacy assets into typed Pydantic registry entries, fixture sets, and evaluation targets. A registry entry cannot activate until it has source hash, examples, counterexamples, required schema fields, failure cases where relevant, eval target, reviewer, and activation receipt.

### Scope

In scope:

- `RegistryEntry`, `RegistryFamily`, `FixtureSet`, `EvaluationTarget`, `RegistryActivationReceipt`, and conflict checks.
- Conversion patterns for archetypes, cognitive primitives, SDA/SFL, CBAR gates, TTT profiles, creative subsystems, Voice DNA, and CMF reference behavior.
- Golden examples and failure corpora as fixtures.
- Eval coverage gate before activation.

Out of scope:

- Runtime execution of JIT compilers. Covered by TS-CMF-015.
- Direct provider jobs and worker assets. Covered in later provider specs.
- Manual editing of legacy source files.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-03.02 | System migrates archetypes, primitives, SDA/SFL, Voice DNA, CBAR, TTT, subsystems, and CMF references. | `RegistryEntry`, family-specific schemas, source hashes, target mappings, reviewer state, and activation receipts. |
| FR-CMF-03.03 | System preserves golden examples and failure corpora as fixtures. | `FixtureSet`, fixture paths, source examples, counterexamples, failure cases, and eval references. |
| FR-CMF-03.08 | Every migrated registry/compiler has targets, fixtures, evals, reviewer, defects, and status. | Activation gate requires target map, fixture, eval target, known defects, reviewer, and status. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `0 - Legacy inventory and migration` |
| Entry Object | Approved legacy asset |
| Exit Object | Registry entry, fixture set, eval target |
| Allowed Actors / Services | Migration Steward, RegistryService, EvaluationService, Architecture Reviewer |
| Validation Contract | Schema validation and eval activation gate |
| Required Receipt | Registry activation receipt |
| Forbidden Shortcut | Prompt-only registry, active registry without eval coverage, CMF reference behavior treated as production code without approval |

### Legacy Intelligence Mapping

This spec operationalizes the Legacy Inventory counts: 244 cognitive primitives, 44 SDA/SFL files, 96 archetype prompts, 34 creative subsystems, CBAR gate packs, TTT profiles, Voice DNA assets, and CMF references. Every migrated item is either a typed registry, fixture, eval target, reference behavior, or blocked asset.

Target modules:

- `ccp_studio.contracts.registry`
- `ccp_studio.contracts.fixtures`
- `ccp_studio.contracts.evaluation_targets`
- `ccp_studio.services.registry_service`
- `ccp_studio.services.fixture_service`
- `ccp_studio.services.evaluation_target_service`
- `ccp_studio.api.v1.registries`
- `tests/fixtures`
- `tests/evals`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `RegistryEntry` | Typed activated or draft entry for a registry family. |
| `RegistryFamily` | Archetype, primitive, SDA, SFL, CBAR, TTT, Voice DNA, creative subsystem, CMF reference behavior. |
| `FixtureSet` | Golden examples, counterexamples, hard negatives, and failure corpora. |
| `EvaluationTarget` | Test or eval target that must pass before activation. |
| `RegistryActivationReceipt` | Proof that schema, fixtures, evals, reviewer, and source hash passed. |
| `RegistryConflict` | Duplicate or overlapping truth requiring resolution. |

## 4. Implementation Plan

### Workstream A: Registry Contracts

Define common registry envelope and family-specific payload hooks.

### Workstream B: Fixture Contracts

Define fixture sets for golden examples, counterexamples, failure corpora, and hard negatives.

### Workstream C: Eval Target Contracts

Define evaluation target metadata, thresholds, and required test locations.

### Workstream D: Conversion Commands

Implement conversion commands from approved ledger entries into draft registry entries, fixture sets, and eval targets.

### Workstream E: Activation Gate

Activation validates schema, source hash, examples, counterexamples, failure cases, target map, eval coverage, conflict status, and reviewer approval.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class RegistryFamily(str, Enum):
    archetype = "archetype"
    cognitive_primitive = "cognitive_primitive"
    sda = "sda"
    sfl = "sfl"
    cbar_gate = "cbar_gate"
    ttt_profile = "ttt_profile"
    voice_dna = "voice_dna"
    creative_subsystem = "creative_subsystem"
    cmf_reference_behavior = "cmf_reference_behavior"


class RegistryStatus(str, Enum):
    draft = "draft"
    active = "active"
    blocked = "blocked"
    deprecated = "deprecated"


class FixtureSet(BaseModel):
    schema_version: Literal["cmf.fixture_set.v1"]
    fixture_set_id: UUID
    migration_ledger_entry_id: UUID
    fixture_path: str
    golden_examples: list[str] = Field(default_factory=list)
    counterexamples: list[str] = Field(default_factory=list)
    failure_cases: list[str] = Field(default_factory=list)
    content_hash: str


class EvaluationTarget(BaseModel):
    schema_version: Literal["cmf.evaluation_target.v1"]
    evaluation_target_id: UUID
    target_path: str
    threshold: float | None = None
    required: bool = True


class RegistryEntry(BaseModel):
    schema_version: Literal["cmf.registry_entry.v1"]
    registry_entry_id: UUID
    registry_family: RegistryFamily
    migration_ledger_entry_id: UUID
    source_hash: str
    payload: dict[str, Any]
    fixture_set_ids: list[UUID]
    evaluation_target_ids: list[UUID]
    known_defects: list[str] = Field(default_factory=list)
    reviewer_actor_id: UUID
    status: RegistryStatus
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `ConvertLegacyAssetToRegistryCommand`, `CreateFixtureSetCommand`, `CreateEvaluationTargetCommand`, `ActivateRegistryEntryCommand`, `BlockRegistryEntryCommand`, `ResolveRegistryConflictCommand` |
| Events | `RegistryEntryDrafted`, `FixtureSetCreated`, `EvaluationTargetCreated`, `RegistryActivationBlocked`, `RegistryEntryActivated`, `RegistryConflictDetected` |
| Workflows | Registry conversion workflow, registry activation workflow, conflict resolution workflow |
| Receipts | `RegistryActivationReceipt`, `RegistryBlockReceipt`, `EvaluationCoverageReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy registry-like files are not activated as-is. If a legacy file cannot be converted into schema, fixtures, and eval target, it remains doctrine/reference only or blocked.

Fallback behavior:

- Missing fixture returns `FIXTURE_SET_REQUIRED`.
- Missing eval target returns `EVALUATION_TARGET_REQUIRED`.
- Schema failure returns `REGISTRY_SCHEMA_INVALID`.
- Duplicate truth returns `REGISTRY_CONFLICT_REQUIRES_REVIEW`.
- CMF engine reference not approved as code returns `REFERENCE_BEHAVIOR_ONLY`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Legacy prompts and registries carry deep intelligence; untyped activation creates prompt drift and duplicate truths. |
| UX / Ops Failure Scenario | An archetype route is activated from a prompt with no counterexamples, causing extraction to force weak moments into confident routes. |
| Resolution Demand | Schema and eval activation take precedence. No migrated registry influences production without typed entry, fixtures, eval target, and reviewer receipt. |
| Downstream Proof | Tests must prove missing eval blocks activation, primitives require examples/failure cases, and CMF references remain fixtures unless approved as code. |

## 9. Tasks

- Define registry, fixture, and eval contracts.
- Add persistence for migrated registry entries, fixture sets, and evaluation targets.
- Implement conversion workflow.
- Implement activation gate.
- Implement conflict detection.
- Add fixture/eval directory conventions.
- Add tests for every required legacy family.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Approved archetype prompt converts to typed registry entry with examples, counterexamples, source hash, route constraints, and eval target. | Archetype stored as raw prompt only. |
| AC2 | Cognitive primitive activation requires schema, examples, failure cases, and family. | Primitive activates with no hard negatives. |
| AC3 | SDA/SFL fixtures support downstream extraction, audio, compression, and evaluation tests. | SFL profile has no audio eval fixture. |
| AC4 | CMF engine reference not approved as production code is reference behavior or fixture only. | Old engine module is imported directly. |
| AC5 | Registry entry lacking eval coverage is blocked. | Registry activates with no test target. |

## 11. Dependencies

Internal:

- TS-CMF-013 Migration ledger
- TS-CMF-016 Greenfield gates
- Evaluation service from Epic 9
- JIT compiler spec TS-CMF-015

External:

- Pydantic v2
- PostgreSQL
- pytest or selected eval runner
- DSPy where applicable

## 12. Testing Strategy

Unit tests:

- Registry schema validation per family.
- Fixture set validation.
- Eval target requiredness.
- Conflict detection.

Integration tests:

- Convert archetype prompt.
- Convert primitive.
- Convert SDA/SFL fixture set.
- Block entry without eval target.
- Activate entry with receipt.

Safety tests:

- Raw prompt cannot become active registry.
- CMF reference behavior cannot be imported as code unless separately approved.
- Duplicate registry truth blocks activation.

## 13. Observability, Recovery, and Rollback

- Logs include `registry_entry_id`, `registry_family`, `source_hash`, `fixture_set_id`, `evaluation_target_id`, and status.
- Metrics track draft, active, blocked, deprecated, conflict, and eval-failure counts.
- Recovery rebuilds active registry bundle from activation receipts.
- Rollback deprecates an active registry entry and activates a replacement via receipt.

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
| Requirement Trace | FR-CMF-03.02, FR-CMF-03.03, FR-CMF-03.08 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Legacy families mapped to typed registry, fixtures, and evals |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Pydantic registry, DSPy eval targets where applicable |
| TypeScript Boundary | Generated consumers only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

