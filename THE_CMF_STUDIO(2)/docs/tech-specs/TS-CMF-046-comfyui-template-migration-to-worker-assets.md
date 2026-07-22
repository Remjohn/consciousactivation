---
tech_spec_id: "TS-CMF-046"
title: "ComfyUI Template Migration to Worker Assets"
story_id: "8.5"
story_title: "ComfyUI Template Migration to Worker Assets"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-5-comfyui-template-migration-to-worker-assets.md"
fr_ids:
  - "FR-CMF-08.05"
pipeline_stage: "0 / 11"
entry_object: "ComfyUI template"
exit_object: "worker asset"
validation_contract: "hash, compatibility, eval target"
required_receipt: "template migration receipt"
runtime_target: "Python / migration workflow / object storage / self-hosted ComfyUI Docker worker"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-046: ComfyUI Template Migration to Worker Assets

**Status:** Ready for Development  
**Story:** `8.5 - ComfyUI Template Migration to Worker Assets`  
**Implementation Boundary:** ComfyUI JSON template migration, worker asset records, hashes, compatibility notes, typed inputs, output contracts, known defects, eval targets, activation state, and migration receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-5-comfyui-template-migration-to-worker-assets.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.05 authority and legacy migration constraints. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Worker asset/reference port doctrine. |
| `docs/architecture.md` | ComfyUI worker rule and migration validation. |
| `docs/cmf-studio-pipeline-map.md` | Stage 0/11 migration-to-worker boundary. |
| `docs/migration/legacy-inventory.md` | Legacy ComfyUI template inventory and CMF engine references. |

## 2. Overview

Migrate approved ComfyUI JSON templates into governed worker assets. A worker asset stores source path, content hash, required inputs, output contract, compatibility notes, known defects, eval target, reviewer, active state, and activation receipt. ComfyUI worker execution can only reference active worker assets by ID and hash.

Template migration is not legacy runtime coupling. It is an explicit conversion into a current worker asset with typed parameters and evaluation gates.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.05 | Migrate approved ComfyUI JSON templates into worker assets with hashes, compatibility notes, required inputs, output contracts, known defects, and eval targets. | `ComfyWorkflowAsset`, migration command, validation, activation state, compatibility/eval metadata, and template migration receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 0 / 11 - Legacy migration and provider jobs |
| Entry Object | ComfyUI template |
| Exit Object | worker asset |
| Validation Contract | hash, compatibility, eval target |
| Required Receipt | template migration receipt |

### Legacy Intelligence Mapping

- Legacy ComfyUI templates are valuable worker assets only after migration.
- Known defects and eval targets must be retained so worker execution can be tested and repaired.
- Template hashes become part of GPU worker receipts.

## 4. Implementation Plan

1. Add contracts for `ComfyWorkflowAsset`, `ComfyWorkflowInputContract`, `ComfyWorkflowOutputContract`, `TemplateCompatibilityNote`, and `TemplateMigrationReceipt`.
2. Add migration command from Legacy Inventory entry to worker asset.
3. Validate JSON hash, required inputs, output contract, known defects, eval target, and reviewer.
4. Store active assets under `worker-assets/comfyui-workflows`.
5. Block worker execution for inactive or revalidated-required templates.
6. Include template hash in every GPU worker/provider receipt.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class WorkerAssetStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    REVALIDATION_REQUIRED = "revalidation_required"
    REJECTED = "rejected"


class ComfyWorkflowInputContract(BaseModel):
    input_name: str
    input_type: str
    required: bool = True
    validation_rule: str | None = None


class ComfyWorkflowAsset(BaseModel):
    comfy_workflow_asset_id: str
    legacy_source_path: str
    content_hash: str
    storage_uri: str
    required_inputs: list[ComfyWorkflowInputContract] = Field(min_length=1)
    output_contract: str
    compatibility_notes: list[str]
    known_defects: list[str] = []
    eval_target: str
    reviewer_id: str
    status: WorkerAssetStatus
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `MigrateComfyTemplateToWorkerAssetCommand`, `ValidateComfyWorkflowInputsCommand`, `ActivateComfyWorkflowAssetCommand`, `DeactivateComfyWorkflowAssetCommand`, `RequireComfyWorkflowRevalidationCommand` |
| Events | `ComfyTemplateMigrationStarted`, `ComfyWorkflowAssetValidated`, `ComfyWorkflowAssetActivated`, `ComfyWorkflowAssetDeactivated`, `ComfyWorkflowRevalidationRequired` |
| Workflow | `MigrationWorkflow.stage0_comfy_template_to_worker_asset` |
| Receipt | `TemplateMigrationReceipt` with source path, content hash, storage URI, input/output contract, defects, eval target, reviewer, and activation state |

## 7. Backward Compatibility and Migration Fallback

Templates can be copied only into worker assets with hashes and contracts. If a template requires ambiguous inputs or has no eval target, it remains inactive until repaired.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Legacy value vs. runtime disorder | Template becomes typed worker asset before use. | GPU receipt stores worker asset ID/hash. |
| Template convenience vs. safety | Required inputs and eval target are mandatory. | Queue validator blocks missing inputs. |
| Output contract drift vs. reproducibility | Output contract changes require revalidation. | Inactive/revalidation state blocks execution. |

## 9. Tasks

- Add worker asset contracts and tables.
- Implement migration and validation commands.
- Add storage convention for workflow assets.
- Add activation/revalidation state.
- Add GPU worker validation integration.
- Add tests for hash, required inputs, output contract, and eval target.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Worker asset stores source path, hash, inputs, output contract, compatibility, defects, eval, reviewer. | Template activated with no output contract. |
| AC2 | Typed inputs checked before queueing. | Worker runs with missing source image. |
| AC3 | Output contract change blocks old template or requires revalidation. | Old template runs after schema change. |
| AC4 | Failed eval remains inactive. | Template activates despite failing eval. |
| AC5 | Render receipt includes template hash. | GPU output cannot trace workflow JSON. |

## 11. Dependencies

- TS-CMF-013 migration ledger.
- TS-CMF-014 registry conversion and evals.
- TS-CMF-045 ComfyUI Docker GPU worker.
- TS-CMF-042 provider capability registry.

## 12. Testing Strategy


Unit tests:

- Unit tests for worker asset schema.
- Migration tests from sample legacy templates.
- Input contract validation tests.
- Revalidation tests on output contract change.
- GPU worker integration tests for template hash receipt.

Integration tests:

- Workflow test from `ComfyUI template` to `worker asset` through pipeline stage `0 / 11`.
- Command Bus test proving `template migration receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for migrated templates, active templates, revalidation blocks, eval failures, and worker asset usage.
- Logs include legacy path, asset ID, content hash, eval target, and reviewer.
- Recovery: repair input/output contract and re-run migration validation.
- Rollback: deactivate worker asset and block future queueing.

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
| Tech Spec ID | TS-CMF-046 |
| Story | 8.5 |
| Requirement Trace | FR-CMF-08.05 |
| Pipeline Trace | Stage 0 / 11, ComfyUI template to worker asset |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No legacy runtime coupling, no unhashable worker template, no eval-less activation |

