from __future__ import annotations

from ccp_studio.contracts.provider_adapters import (
    ProviderExecutionRequest,
    ProviderExecutionStatus,
    ProviderJobReceipt,
)
from ccp_studio.providers.registry import ProviderAdapterRegistry


class ProviderOrchestrationService:
    def __init__(self, registry: ProviderAdapterRegistry | None = None):
        self.registry = registry or ProviderAdapterRegistry()

    def run(self, request: ProviderExecutionRequest) -> ProviderJobReceipt:
        adapter = self.registry.get(request.provider_id)
        preflight = adapter.validate(request)
        if not preflight.pass_status:
            return ProviderJobReceipt(
                request_id=request.provider_execution_request_id,
                provider_id=request.provider_id,
                provider_capability_id=request.provider_capability_id,
                provider_request_id="not_submitted",
                status=ProviderExecutionStatus.PREFLIGHT_FAILED,
                output_assets=[],
                route_production_spec_id=request.route_production_spec_id,
                provider_job_blueprint_id=request.provider_job_blueprint_id,
                primary_style_route_id=request.primary_style_route_id,
                frame_profile=request.frame_profile,
                composition_role=request.composition_role,
            )

        adapter.estimate(request)
        submission = adapter.submit(request)
        poll = adapter.poll(request, submission)
        outputs = adapter.download_outputs(request, poll)
        return adapter.normalize(request, submission, poll, outputs)
