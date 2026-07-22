---
tech_spec_id: "TS-CMF-045"
title: "Self-Hosted ComfyUI Docker GPU Worker"
story_id: "8.4"
story_title: "Self-Hosted ComfyUI Docker GPU Worker"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-4-self-hosted-comfyui-docker-gpu-worker.md"
fr_ids:
  - "FR-CMF-08.04"
pipeline_stage: "11"
entry_object: "ComfyUI queued job"
exit_object: "worker output and cost report"
validation_contract: "approved template and GPU policy"
required_receipt: "GPU worker receipt"
runtime_target: "Python / durable workflows / self-hosted ComfyUI Docker / AWS or Google Cloud GPU"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-045: Self-Hosted ComfyUI Docker GPU Worker

**Status:** Ready for Development  
**Story:** `8.4 - Self-Hosted ComfyUI Docker GPU Worker`  
**Implementation Boundary:** Batch-first self-hosted ComfyUI Docker worker on AWS or Google Cloud 24GB/32GB VRAM, approved workflow validation, queue/checkpoint/upload/cost/shutdown policy, and GPU worker receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-4-self-hosted-comfyui-docker-gpu-worker.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.04 authority and batch GPU worker requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Self-hosted Docker GPU worker and approved template rule. |
| `docs/architecture.md` | ComfyUI worker rule, provider capability record, recovery table. |
| `docs/cmf-studio-pipeline-map.md` | GPU execution provider role and stage 11 trace. |
| `docs/migration/legacy-inventory.md` | ComfyUI templates and CMF engine references. |

## 2. Overview

Implement ComfyUI execution as a self-hosted Docker GPU worker. Workers run approved hashed workflow templates with typed parameters, checkpoint per asset, upload outputs, write receipts, report cost/performance, and shut down when the queue drains. Runtime agents may request approved templates; they may not mutate arbitrary workflow graphs in production.

The worker is a provider behind capability records. It cannot write canonical business state directly.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.04 | Run batch-first GPU worker behavior for self-hosted ComfyUI Docker worker, including queued execution, checkpointing, upload, receipt writing, cost reporting, and shutdown. | `GpuWorkerJob`, queue, checkpoint, approved template validation, cloud/GPU metadata, output upload, cost report, and worker receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 11 - Asset research and provider jobs |
| Entry Object | ComfyUI queued job |
| Exit Object | worker output and cost report |
| Validation Contract | approved template and GPU policy |
| Required Receipt | GPU worker receipt |

### Legacy Intelligence Mapping

- Legacy ComfyUI JSON templates are migrated worker assets, not mutable runtime graphs.
- CMF engine references inform fixtures and evals.
- Batch GPU behavior follows PRD/NFR cost and checkpoint constraints.

## 4. Implementation Plan

1. Add contracts for `GpuWorkerJob`, `ComfyWorkflowExecution`, `WorkerCheckpoint`, `GpuCostReport`, and `GpuWorkerReceipt`.
2. Validate workflow template hash and active worker asset before queueing.
3. Record cloud provider, GPU tier, Docker image digest, queue state, workflow hash, input assets, and job IDs at startup.
4. Checkpoint each completed output, upload artifacts, and persist progress.
5. Requeue incomplete work after interruption.
6. Shut down worker and write final cost report when queue drains.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel


class GpuWorkerStatus(str, Enum):
    QUEUED = "queued"
    STARTING = "starting"
    RUNNING = "running"
    DRAINING = "draining"
    SHUTDOWN = "shutdown"
    FAILED = "failed"


class GpuWorkerJob(BaseModel):
    gpu_worker_job_id: str
    provider_job_id: str
    cloud_provider: str
    gpu_tier: str
    docker_image_digest: str
    workflow_asset_id: str
    workflow_hash: str
    input_artifact_hashes: list[str]
    queue_position: int | None = None
    status: GpuWorkerStatus


class WorkerCheckpoint(BaseModel):
    checkpoint_id: str
    gpu_worker_job_id: str
    output_artifact_uri: str
    output_artifact_hash: str
    completed_step: str
    cost_so_far: float | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `QueueComfyGpuWorkerJobCommand`, `StartGpuWorkerCommand`, `RecordWorkerCheckpointCommand`, `UploadWorkerOutputCommand`, `RequeueIncompleteGpuJobCommand`, `ShutdownGpuWorkerCommand`, `BlockUnapprovedComfyWorkflowCommand` |
| Events | `ComfyGpuWorkerJobQueued`, `GpuWorkerStarted`, `WorkerCheckpointRecorded`, `WorkerOutputUploaded`, `IncompleteGpuJobRequeued`, `GpuWorkerShutdown`, `UnapprovedComfyWorkflowBlocked` |
| Workflow | `ProviderJobWorkflow.stage11_comfy_gpu_worker` |
| Receipt | `GpuWorkerReceipt` with cloud/GPU/Docker metadata, workflow asset/hash, inputs, outputs, checkpoints, cost, status, and shutdown state |

## 7. Backward Compatibility and Migration Fallback

Legacy ComfyUI templates must pass worker-asset migration before use. Unapproved or modified workflow graphs are blocked. Production worker execution uses typed parameters and approved asset hashes only.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| GPU power vs. cost control | Worker starts for queued batches and shuts down when drained. | Cost report and shutdown event written. |
| Template flexibility vs. governance | Only approved hashed workflow assets execute. | Receipt stores workflow asset ID/hash. |
| Interruption vs. lost work | Checkpoints preserve completed outputs. | Recovery requeues only incomplete work. |

## 9. Tasks

- Add GPU worker contracts and persistence.
- Implement worker queue and lifecycle commands.
- Add approved workflow validation.
- Add checkpoint/upload/cost reporting.
- Add recovery for interrupted workers.
- Add tests for unapproved template block and checkpoint resume.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Worker start records GPU tier, cloud, Docker, queue, workflow hash, inputs, job IDs. | Worker starts with no image digest. |
| AC2 | Output checkpoint uploads artifact and receipt/progress. | Completed asset lost after interruption. |
| AC3 | Queue drain shuts down worker and reports cost. | GPU instance remains idle indefinitely. |
| AC4 | Interrupted worker preserves outputs and requeues incomplete jobs. | All jobs restart from zero. |
| AC5 | Unapproved template is blocked. | Runtime graph mutation executes. |

## 11. Dependencies

- TS-CMF-042 provider capability registry.
- TS-CMF-044 generative provider adapters.
- TS-CMF-046 ComfyUI worker asset migration.
- TS-CMF-048 recovery semantics when generated.

## 12. Testing Strategy


Unit tests:

- Unit tests for worker job/checkpoint schemas.
- Lifecycle tests for queue/start/checkpoint/upload/shutdown.
- Unapproved workflow hash tests.
- Interruption recovery tests.
- Cost report tests.

Integration tests:

- Workflow test from `ComfyUI queued job` to `worker output and cost report` through pipeline stage `11`.
- Command Bus test proving `GPU worker receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for worker startup time, GPU utilization, queue depth, job duration, cost, checkpoint count, and shutdown success.
- Logs include worker job ID, provider job ID, Docker digest, workflow hash, output hashes, and cost.
- Recovery: requeue incomplete jobs from checkpoint.
- Rollback: mark worker job failed/cancelled and preserve uploaded outputs/receipts.

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
| Tech Spec ID | TS-CMF-045 |
| Story | 8.4 |
| Requirement Trace | FR-CMF-08.04 |
| Pipeline Trace | Stage 11, ComfyUI queued job to worker output/cost report |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No hidden external execution route, no arbitrary workflow mutation, no idle default GPU posture |

