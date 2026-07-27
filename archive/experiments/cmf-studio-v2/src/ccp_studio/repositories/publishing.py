"""Publishing repositories for TS-CMF-054."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.publishing import (
    PublerJob,
    PublishingDomainEvent,
    PublishingIntent,
    PublishingOutcome,
    PublishingReceipt,
)


@dataclass
class InMemoryPublishingRepository:
    intents: dict[UUID, PublishingIntent] = field(default_factory=dict)
    publer_jobs: dict[UUID, PublerJob] = field(default_factory=dict)
    outcomes: dict[UUID, PublishingOutcome] = field(default_factory=dict)
    receipts: dict[UUID, PublishingReceipt] = field(default_factory=dict)
    events: list[PublishingDomainEvent] = field(default_factory=list)
    submit_idempotency_index: dict[str, UUID] = field(default_factory=dict)
    webhook_idempotency_index: dict[str, UUID] = field(default_factory=dict)
    memory_admission_proposals: list[UUID] = field(default_factory=list)

    def put_intent(self, intent: PublishingIntent) -> PublishingIntent:
        self.intents[intent.publishing_intent_id] = intent
        return intent

    def put_publer_job(self, job: PublerJob) -> PublerJob:
        self.publer_jobs[job.publer_job_id] = job
        self.submit_idempotency_index[job.idempotency_key] = job.publer_job_id
        return job

    def put_outcome(self, outcome: PublishingOutcome, *, webhook_idempotency_key: str | None = None) -> PublishingOutcome:
        self.outcomes[outcome.publishing_outcome_id] = outcome
        if webhook_idempotency_key:
            self.webhook_idempotency_index[webhook_idempotency_key] = outcome.publishing_outcome_id
        return outcome

    def put_receipt(self, receipt: PublishingReceipt) -> PublishingReceipt:
        self.receipts[receipt.publishing_receipt_id] = receipt
        return receipt

    def append_event(self, event: PublishingDomainEvent) -> PublishingDomainEvent:
        self.events.append(event)
        return event

