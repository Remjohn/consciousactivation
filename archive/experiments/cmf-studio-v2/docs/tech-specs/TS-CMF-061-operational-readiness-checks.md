---
tech_spec_id: "TS-CMF-061"
title: "Operational Readiness Checks"
story_id: "10.6"
story_title: "Operational Readiness Checks"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-10-6-operational-readiness-checks.md"
fr_ids:
  - "FR-CMF-10.07"
pipeline_stage: "release readiness overlay"
entry_object: "system fixtures and production chain"
exit_object: "readiness report"
validation_contract: "full brand-cycle and rebuild gates"
required_receipt: "readiness receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / operations checks / CI-ready fixtures"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-061: Operational Readiness Checks

**Status:** Ready for Development  
**Story:** `10.6 - Operational Readiness Checks`  
**Implementation Boundary:** ReadinessCheckRun, restore drills, provider outage simulation, GPU worker shutdown check, memory rebuild, Neo4j projection rebuild, complete brand-cycle check, readiness report, and readiness receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-10-6-operational-readiness-checks.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-10.07 authority and readiness scope. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Final human acceptance, provider outage fallback, restore drill, and projection readiness doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Operational tasks and exit gate source. |
| `docs/architecture.md` | Failure taxonomy, release validation checklist, and readiness targets. |
| `docs/cmf-studio-pipeline-map.md` | Full pipeline and operations recovery trace. |
| `docs/migration/legacy-inventory.md` | Legacy spec/build protocols and readiness references. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Reality-contact evaluation gate for readiness reports. |

## 2. Overview

Operational readiness proves CMF STUDIO can run the full documented system under production pressure. Checks cover restore drills, provider outage handling, GPU worker shutdown, memory rebuild, Neo4j projection rebuild, and one complete brand cycle from Brand Genesis through publishing intent, memory, operations, and projection health.

Readiness checks are executable fixtures and reports, not slideware. They must prove canonical state, object storage references, receipts, projection rebuild ability, recovery actions, spend alerts, and operator completion without manual database edits.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-10.07 | Run operational readiness checks for restore drills, provider outage handling, GPU worker shutdown, memory rebuild, Neo4j projection rebuild, and one complete brand cycle without manual database edits. | Readiness check run, drill contracts, full brand-cycle fixture, rebuild gates, outage simulation, receipt validation, and readiness report. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | release readiness overlay |
| Entry Object | system fixtures and production chain |
| Exit Object | readiness report |
| Validation Contract | full brand-cycle and rebuild gates |
| Required Receipt | readiness receipt |

### Legacy Intelligence Mapping

- Greenfield release gates become executable readiness checks.
- Legacy spec/build protocols inform source trace, CBAR, and proof requirements.
- RSCS reality-contact gate prevents readiness reports from becoming generic assurance language.
- Active primitive families SAF, BUS, and FBK govern safety, operational viability, and clear failure feedback.

## 4. Implementation Plan

1. Define `ReadinessCheckRun`, `ReadinessCheckResult`, `RestoreDrillReport`, `ProviderOutageSimulation`, `GpuWorkerShutdownCheck`, `MemoryRebuildCheck`, `ProjectionRebuildCheck`, `CompleteBrandCycleCheck`, and `ReadinessReceipt`.
2. Implement command to run the complete readiness suite and individual checks.
3. Validate restore of canonical state, object storage refs, receipts, and projection rebuild.
4. Simulate provider outage and prove recovery preserves completed artifacts and avoids duplicate effects.
5. Drain GPU worker queue and verify shutdown status and final costs.
6. Replay memory events and projection events.
7. Execute full brand-cycle fixture without manual database edits.
8. Emit readiness report with pass/fail, evidence refs, blockers, and required fixes.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class ReadinessCheckType(str, Enum):
    RESTORE_DRILL = "restore_drill"
    PROVIDER_OUTAGE = "provider_outage"
    GPU_WORKER_SHUTDOWN = "gpu_worker_shutdown"
    MEMORY_REBUILD = "memory_rebuild"
    PROJECTION_REBUILD = "projection_rebuild"
    COMPLETE_BRAND_CYCLE = "complete_brand_cycle"


class ReadinessCheckResult(BaseModel):
    check_type: ReadinessCheckType
    passed: bool
    evidence_refs: list[str]
    blocker_codes: list[str]
    required_fixes: list[str]


class ReadinessCheckRun(BaseModel):
    schema_version: Literal["cmf.readiness_check_run.v1"]
    readiness_run_id: str
    triggered_by_user_id: str
    fixture_pack_id: str
    results: list[ReadinessCheckResult]
    overall_status: Literal["passed", "failed", "blocked"]
    created_at: str


class ReadinessReceipt(BaseModel):
    receipt_id: str
    readiness_run_id: str
    canonical_state_verified: bool
    object_storage_verified: bool
    receipts_verified: bool
    projection_rebuild_verified: bool
    manual_database_edits_detected: bool
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RunOperationalReadinessSuiteCommand`, `RunRestoreDrillCommand`, `SimulateProviderOutageCommand`, `RunGpuWorkerShutdownCheckCommand`, `RunMemoryRebuildCheckCommand`, `RunProjectionRebuildCheckCommand`, `RunCompleteBrandCycleCheckCommand`, `RecordReadinessReceiptCommand` |
| Events | `OperationalReadinessSuiteStarted`, `RestoreDrillCompleted`, `ProviderOutageSimulationCompleted`, `GpuWorkerShutdownCheckCompleted`, `MemoryRebuildCheckCompleted`, `ProjectionRebuildCheckCompleted`, `CompleteBrandCycleCheckCompleted`, `ReadinessReceiptRecorded` |
| Workflow | `OperationsWorkflow.release_readiness_overlay` |
| Receipt | `ReadinessReceipt` with run ID, fixture pack, evidence refs, check results, blockers, required fixes, and manual-edit detection |

## 7. Backward Compatibility and Migration Fallback

Legacy release and acceptance checklists become executable checks or evidence references. If a check cannot be automated yet, it must produce a human handoff with evidence refs and cannot be marked passed. Manual database edits fail the readiness suite.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Confidence vs. real operability | Readiness must execute drills and full brand cycle, not assert readiness. | ReadinessReceipt stores evidence refs and pass/fail per check. |
| Provider outage vs. duplicate effects | Outage drill must prove recovery preserves artifacts and blocks duplicates. | Provider outage result includes recovery receipt refs. |
| Projection and memory complexity vs. rebuildability | Memory and projection rebuild checks are mandatory. | Rebuild results validate counts and governance state. |

## 9. Tasks

- Add readiness contracts and fixture pack metadata.
- Implement readiness suite command.
- Implement restore drill.
- Implement provider outage simulation.
- Implement GPU worker shutdown check.
- Implement memory rebuild check.
- Implement projection rebuild check.
- Implement complete brand-cycle fixture.
- Add readiness report and receipt writer.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Restore drill verifies canonical state, object storage, receipts, and projection rebuild. | Backup restores tables but loses receipt links. |
| AC2 | Provider outage simulation preserves completed artifacts and avoids duplicate side effects. | Outage recovery reposts or bills twice. |
| AC3 | GPU worker shutdown records drain, final status, and cost. | GPU worker stops with no cost receipt. |
| AC4 | Memory rebuild preserves approved, expired, reversed, and quarantined states. | Rebuild reactivates reversed memory. |
| AC5 | Full brand cycle completes without manual database edits. | Operator needs a developer to patch state mid-run. |

## 11. Dependencies

- TS-CMF-001 through TS-CMF-060.
- Full story file set under `docs/stories`.
- Provider, renderer, publishing, memory, projection, and operations fixtures.

## 12. Testing Strategy


Unit tests:

- Unit tests for readiness schemas and result aggregation.
- Fixture tests for restore, outage, GPU shutdown, memory rebuild, projection rebuild, and full brand-cycle checks.
- Integration test executing one complete brand cycle.
- Failure tests for missing receipts, object storage refs, duplicate side effects, and manual edit detection.
- Regression tests that all readiness checks produce evidence refs.

Integration tests:

- Workflow test from `system fixtures and production chain` to `readiness report` through pipeline stage `release readiness overlay`.
- Command Bus test proving `readiness receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for readiness runs, check pass/fail, run duration, blockers, required fixes, and manual-edit detections.
- Logs include readiness run ID, fixture pack ID, check type, evidence refs, and blocker codes.
- Recovery re-runs failed checks after fixes and links new receipts to prior readiness run.
- Rollback marks readiness run superseded; it does not delete failed readiness evidence.

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
| Tech Spec ID | TS-CMF-061 |
| Story | 10.6 |
| Requirement Trace | FR-CMF-10.07 |
| Pipeline Trace | Release readiness overlay, system fixtures and production chain to readiness report |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No paper-only readiness, no manual database edits, no missing full brand-cycle proof |
