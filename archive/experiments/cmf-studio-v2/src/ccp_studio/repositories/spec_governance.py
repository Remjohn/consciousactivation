"""In-memory spec-governance repositories for TS-CMF-003."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.spec_governance import (
    CBARCheck,
    FilesReadReceipt,
    PipelineStageTrace,
    RequirementTrace,
    SpecAuditReceipt,
    TechSpecSourcePacket,
    TechSpecWorkflow,
)


@dataclass
class InMemorySpecGovernanceRepository:
    workflows: dict[UUID, TechSpecWorkflow] = field(default_factory=dict)
    source_packets: dict[UUID, TechSpecSourcePacket] = field(default_factory=dict)
    files_read_receipts: dict[UUID, FilesReadReceipt] = field(default_factory=dict)
    requirement_traces: dict[UUID, RequirementTrace] = field(default_factory=dict)
    pipeline_traces: dict[UUID, PipelineStageTrace] = field(default_factory=dict)
    cbar_checks: dict[UUID, CBARCheck] = field(default_factory=dict)
    audit_receipts: dict[UUID, SpecAuditReceipt] = field(default_factory=dict)

    def save_workflow(self, workflow: TechSpecWorkflow) -> TechSpecWorkflow:
        self.workflows[workflow.workflow_id] = workflow
        return workflow

    def get_workflow(self, workflow_id: UUID) -> TechSpecWorkflow | None:
        return self.workflows.get(workflow_id)

    def save_source_packet(self, packet: TechSpecSourcePacket) -> TechSpecSourcePacket:
        self.source_packets[packet.source_packet_id] = packet
        return packet

    def latest_source_packet_for_workflow(self, workflow_id: UUID) -> TechSpecSourcePacket | None:
        packets = [
            packet
            for packet in self.source_packets.values()
            if packet.workflow_id == workflow_id
        ]
        if not packets:
            return None
        return max(packets, key=lambda item: item.created_at)

    def save_files_read_receipt(self, receipt: FilesReadReceipt) -> FilesReadReceipt:
        self.files_read_receipts[receipt.receipt_id] = receipt
        return receipt

    def files_read_for_workflow(self, workflow_id: UUID) -> list[FilesReadReceipt]:
        return [
            receipt
            for receipt in self.files_read_receipts.values()
            if receipt.workflow_id == workflow_id
        ]

    def save_requirement_trace(self, trace: RequirementTrace) -> RequirementTrace:
        self.requirement_traces[trace.trace_id] = trace
        return trace

    def requirement_traces_for_workflow(self, workflow_id: UUID) -> list[RequirementTrace]:
        return [
            trace
            for trace in self.requirement_traces.values()
            if trace.workflow_id == workflow_id
        ]

    def save_pipeline_trace(self, trace: PipelineStageTrace) -> PipelineStageTrace:
        self.pipeline_traces[trace.trace_id] = trace
        return trace

    def pipeline_traces_for_workflow(self, workflow_id: UUID) -> list[PipelineStageTrace]:
        return [
            trace
            for trace in self.pipeline_traces.values()
            if trace.workflow_id == workflow_id
        ]

    def save_cbar_check(self, check: CBARCheck) -> CBARCheck:
        self.cbar_checks[check.cbar_check_id] = check
        return check

    def cbar_checks_for_workflow(self, workflow_id: UUID) -> list[CBARCheck]:
        return [
            check
            for check in self.cbar_checks.values()
            if check.workflow_id == workflow_id
        ]

    def save_audit_receipt(self, receipt: SpecAuditReceipt) -> SpecAuditReceipt:
        self.audit_receipts[receipt.spec_audit_receipt_id] = receipt
        return receipt
