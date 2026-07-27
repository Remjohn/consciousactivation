"""Composition lineage repositories for TS-CMF-038."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.composition import (
    CompositionAnalysis,
    CompositionJob,
    CompositionPlate,
    CompositionReceipt,
    DownstreamCompositionEdit,
    FinalTextPlan,
    IdeogramProviderReceipt,
)


@dataclass
class InMemoryCompositionRepository:
    composition_jobs: dict[UUID, CompositionJob] = field(default_factory=dict)
    final_text_plans: dict[UUID, FinalTextPlan] = field(default_factory=dict)
    provider_receipts: dict[UUID, IdeogramProviderReceipt] = field(default_factory=dict)
    analyses: dict[UUID, CompositionAnalysis] = field(default_factory=dict)
    plates: dict[UUID, CompositionPlate] = field(default_factory=dict)
    downstream_edits: dict[UUID, DownstreamCompositionEdit] = field(default_factory=dict)
    receipts: dict[UUID, CompositionReceipt] = field(default_factory=dict)

    def put_composition_job(self, job: CompositionJob) -> CompositionJob:
        self.composition_jobs[job.composition_job_id] = job
        return job

    def put_final_text_plan(self, plan: FinalTextPlan) -> FinalTextPlan:
        self.final_text_plans[plan.final_text_plan_id] = plan
        return plan

    def put_provider_receipt(self, receipt: IdeogramProviderReceipt) -> IdeogramProviderReceipt:
        self.provider_receipts[receipt.provider_receipt_id] = receipt
        return receipt

    def put_analysis(self, analysis: CompositionAnalysis) -> CompositionAnalysis:
        self.analyses[analysis.composition_analysis_id] = analysis
        return analysis

    def put_plate(self, plate: CompositionPlate) -> CompositionPlate:
        self.plates[plate.composition_plate_id] = plate
        return plate

    def put_downstream_edit(self, edit: DownstreamCompositionEdit) -> DownstreamCompositionEdit:
        self.downstream_edits[edit.downstream_composition_edit_id] = edit
        return edit

    def put_receipt(self, receipt: CompositionReceipt) -> CompositionReceipt:
        self.receipts[receipt.composition_receipt_id] = receipt
        return receipt
