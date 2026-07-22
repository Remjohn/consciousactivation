"""ComfyUI GPU worker repositories for TS-CMF-045."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.comfy_gpu_worker import (
    ComfyWorkflowAsset,
    ComfyWorkflowExecution,
    GpuCostReport,
    GpuWorkerJob,
    GpuWorkerReceipt,
    WorkerCheckpoint,
)


@dataclass
class InMemoryComfyGpuWorkerRepository:
    workflow_assets: dict[UUID, ComfyWorkflowAsset] = field(default_factory=dict)
    jobs: dict[UUID, GpuWorkerJob] = field(default_factory=dict)
    executions: dict[UUID, ComfyWorkflowExecution] = field(default_factory=dict)
    checkpoints: dict[UUID, WorkerCheckpoint] = field(default_factory=dict)
    cost_reports: dict[UUID, GpuCostReport] = field(default_factory=dict)
    receipts: dict[UUID, GpuWorkerReceipt] = field(default_factory=dict)

    def put_workflow_asset(self, asset: ComfyWorkflowAsset) -> ComfyWorkflowAsset:
        self.workflow_assets[asset.workflow_asset_id] = asset
        return asset

    def put_job(self, job: GpuWorkerJob) -> GpuWorkerJob:
        self.jobs[job.gpu_worker_job_id] = job
        return job

    def put_execution(self, execution: ComfyWorkflowExecution) -> ComfyWorkflowExecution:
        self.executions[execution.comfy_workflow_execution_id] = execution
        return execution

    def put_checkpoint(self, checkpoint: WorkerCheckpoint) -> WorkerCheckpoint:
        self.checkpoints[checkpoint.checkpoint_id] = checkpoint
        return checkpoint

    def put_cost_report(self, report: GpuCostReport) -> GpuCostReport:
        self.cost_reports[report.gpu_cost_report_id] = report
        return report

    def put_receipt(self, receipt: GpuWorkerReceipt) -> GpuWorkerReceipt:
        self.receipts[receipt.gpu_worker_receipt_id] = receipt
        return receipt
