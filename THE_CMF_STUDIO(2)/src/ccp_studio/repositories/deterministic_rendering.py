"""Deterministic rendering repositories for TS-CMF-043."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.deterministic_rendering import (
    DeterministicRenderJob,
    RendererPropsBundle,
    RendererRouteDecision,
    RenderOutput,
    RenderReceipt,
)


@dataclass
class InMemoryDeterministicRenderRepository:
    route_decisions: dict[UUID, RendererRouteDecision] = field(default_factory=dict)
    props_bundles: dict[UUID, RendererPropsBundle] = field(default_factory=dict)
    jobs: dict[UUID, DeterministicRenderJob] = field(default_factory=dict)
    outputs: dict[UUID, RenderOutput] = field(default_factory=dict)
    receipts: dict[UUID, RenderReceipt] = field(default_factory=dict)
    idempotency_index: dict[str, UUID] = field(default_factory=dict)

    def put_route_decision(self, decision: RendererRouteDecision) -> RendererRouteDecision:
        self.route_decisions[decision.renderer_route_decision_id] = decision
        return decision

    def put_props_bundle(self, bundle: RendererPropsBundle) -> RendererPropsBundle:
        self.props_bundles[bundle.renderer_props_bundle_id] = bundle
        return bundle

    def put_job(self, job: DeterministicRenderJob) -> DeterministicRenderJob:
        self.jobs[job.deterministic_render_job_id] = job
        self.idempotency_index[job.idempotency_key] = job.deterministic_render_job_id
        return job

    def put_output(self, output: RenderOutput) -> RenderOutput:
        self.outputs[output.render_output_id] = output
        return output

    def put_receipt(self, receipt: RenderReceipt) -> RenderReceipt:
        self.receipts[receipt.render_receipt_id] = receipt
        return receipt

    def job_for_idempotency(self, idempotency_key: str) -> DeterministicRenderJob | None:
        job_id = self.idempotency_index.get(idempotency_key)
        return self.jobs.get(job_id) if job_id else None

    def output_for_props_bundle(self, renderer_props_bundle_id: UUID) -> RenderOutput | None:
        return next((item for item in self.outputs.values() if self.jobs[item.deterministic_render_job_id].renderer_props_bundle_id == renderer_props_bundle_id), None)
