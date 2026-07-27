"""Deterministic Publer adapter for TS-CMF-054 tests and local workflows."""

from __future__ import annotations

from uuid import uuid5, NAMESPACE_URL

from ccp_studio.contracts.publishing import PublerJobStatus, PublishingIntent


class PublerAdapter:
    provider_name = "publer"

    def submit_confirmed_intent(self, intent: PublishingIntent, *, idempotency_key: str) -> dict[str, str]:
        external_job_id = str(uuid5(NAMESPACE_URL, f"publer:{intent.publishing_intent_id}:{idempotency_key}"))
        return {
            "external_job_id": external_job_id,
            "status": PublerJobStatus.scheduled.value,
            "provider_name": self.provider_name,
        }

