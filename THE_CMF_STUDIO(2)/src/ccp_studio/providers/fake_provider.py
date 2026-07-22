"""Fake provider adapter for TS-CMF-042 provider operation tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.provider_jobs import (
    ProviderCapabilityRecord,
    ProviderJob,
    ProviderJobStatus,
    ProviderRequest,
    ProviderResponse,
    provider_hash,
)


@dataclass
class FakeProviderAdapter:
    provider_name: str = "fake_provider"
    response_status: ProviderJobStatus = ProviderJobStatus.succeeded
    output_count: int = 1
    failure_code: str | None = None
    submissions: list[ProviderJob] = field(default_factory=list)

    def submit(
        self,
        *,
        request: ProviderRequest,
        capability: ProviderCapabilityRecord,
        job: ProviderJob,
    ) -> ProviderResponse:
        self.submissions.append(job)
        output_hashes = []
        if self.response_status == ProviderJobStatus.succeeded:
            output_hashes = [
                provider_hash(
                    {
                        "provider_job_id": job.provider_job_id,
                        "provider_capability_id": capability.provider_capability_id,
                        "output_index": index,
                    }
                )
                for index in range(self.output_count)
            ]
        return ProviderResponse(
            schema_version="cmf.provider_response.v1",
            provider_response_id=uuid4(),
            provider_job_id=job.provider_job_id,
            provider_correlation_id=f"{capability.provider_name}:{uuid4()}",
            status=self.response_status,
            output_artifact_hashes=output_hashes,
            cost_amount=float(request.parameters.get("estimated_cost_amount", 0.0)),
            failure_code=self.failure_code,
            response_metadata={
                "provider_name": capability.provider_name,
                "capability_name": capability.capability_name,
                "model_or_workflow_version": capability.model_or_workflow_version,
            },
            received_at=utc_now(),
        )
