"""Provider operation repositories for TS-CMF-042."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.provider_jobs import (
    ProviderCapabilityRecord,
    ProviderDomainEvent,
    ProviderJob,
    ProviderReceipt,
    ProviderRequest,
    ProviderResponse,
    ProviderWebhookEnvelope,
)


@dataclass
class InMemoryProviderOperationsRepository:
    capabilities: dict[str, ProviderCapabilityRecord] = field(default_factory=dict)
    requests: dict[UUID, ProviderRequest] = field(default_factory=dict)
    jobs: dict[UUID, ProviderJob] = field(default_factory=dict)
    responses: dict[UUID, ProviderResponse] = field(default_factory=dict)
    receipts: dict[UUID, ProviderReceipt] = field(default_factory=dict)
    webhooks: dict[UUID, ProviderWebhookEnvelope] = field(default_factory=dict)
    domain_events: list[ProviderDomainEvent] = field(default_factory=list)
    idempotency_index: dict[tuple[UUID, UUID, str], UUID] = field(default_factory=dict)
    webhook_idempotency_index: dict[str, UUID] = field(default_factory=dict)
    job_by_provider_correlation_id: dict[str, UUID] = field(default_factory=dict)

    def put_capability(self, capability: ProviderCapabilityRecord) -> ProviderCapabilityRecord:
        self.capabilities[capability.provider_capability_id] = capability
        return capability

    def put_request(self, request: ProviderRequest) -> ProviderRequest:
        self.requests[request.provider_request_id] = request
        return request

    def put_job(self, job: ProviderJob) -> ProviderJob:
        self.jobs[job.provider_job_id] = job
        if job.provider_correlation_id:
            self.job_by_provider_correlation_id[job.provider_correlation_id] = job.provider_job_id
        return job

    def put_response(self, response: ProviderResponse) -> ProviderResponse:
        self.responses[response.provider_response_id] = response
        self.job_by_provider_correlation_id[response.provider_correlation_id] = response.provider_job_id
        return response

    def put_receipt(self, receipt: ProviderReceipt) -> ProviderReceipt:
        self.receipts[receipt.provider_receipt_id] = receipt
        return receipt

    def put_webhook(self, envelope: ProviderWebhookEnvelope) -> ProviderWebhookEnvelope:
        self.webhooks[envelope.provider_webhook_id] = envelope
        return envelope

    def append_event(self, event: ProviderDomainEvent) -> ProviderDomainEvent:
        self.domain_events.append(event)
        return event

    def remember_idempotency(self, request: ProviderRequest, provider_job_id: UUID) -> None:
        self.idempotency_index[(request.organization_id, request.brand_id, request.idempotency_key)] = provider_job_id

    def job_for_idempotency(self, organization_id: UUID, brand_id: UUID, idempotency_key: str) -> ProviderJob | None:
        job_id = self.idempotency_index.get((organization_id, brand_id, idempotency_key))
        return self.jobs.get(job_id) if job_id else None

    def receipt_for_job(self, provider_job_id: UUID) -> ProviderReceipt | None:
        return next((item for item in self.receipts.values() if item.provider_job_id == provider_job_id), None)

    def latest_response_for_job(self, provider_job_id: UUID) -> ProviderResponse | None:
        responses = [item for item in self.responses.values() if item.provider_job_id == provider_job_id]
        if not responses:
            return None
        return sorted(responses, key=lambda item: item.received_at)[-1]
