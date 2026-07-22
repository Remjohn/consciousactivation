from __future__ import annotations

import os

from ccp_studio.contracts.provider_adapters import (
    ProviderAdapterConfig,
    ProviderCapabilityId,
    ProviderCredentialRef,
    ProviderExecutionRequest,
    ProviderExecutionStatus,
    ProviderId,
    ProviderOutputAsset,
    ProviderPollReceipt,
    ProviderPreflightReport,
    ProviderSubmissionReceipt,
    ProviderTransportMode,
    ProviderErrorCode,
)
from ccp_studio.providers.base import BaseProviderAdapter
from ccp_studio.providers.provider_http import ProviderHttpClient
from ccp_studio.providers.provider_storage import ProviderOutputStorage


class BFLFluxAdapter(BaseProviderAdapter):
    provider_id = ProviderId.BFL_FLUX
    capability_ids = [
        ProviderCapabilityId.IMAGE_GENERATE,
        ProviderCapabilityId.IMAGE_EDIT,
        ProviderCapabilityId.IMAGE_REFERENCE_EDIT,
        ProviderCapabilityId.IMAGE_OUTPAINT,
        ProviderCapabilityId.IMAGE_REPAIR,
    ]

    def __init__(self, config: ProviderAdapterConfig | None = None, http: ProviderHttpClient | None = None, storage: ProviderOutputStorage | None = None):
        super().__init__(
            config
            or ProviderAdapterConfig(
                provider_id=ProviderId.BFL_FLUX,
                enabled=False,
                transport_mode=ProviderTransportMode.HTTP,
                base_url="https://api.bfl.ai",
                model_name="flux",
                credential_ref=ProviderCredentialRef(provider_id=ProviderId.BFL_FLUX, env_var_name="BFL_API_KEY"),
                max_reference_images=10,
                extra={"generate_path": "/v1/flux"},
            )
        )
        self.http = http or ProviderHttpClient()
        self.storage = storage or ProviderOutputStorage()

    def validate(self, request: ProviderExecutionRequest) -> ProviderPreflightReport:
        report = super().validate(request)
        if len(request.reference_assets) > self.config.max_reference_images:
            report.missing_requirements.append("reference_assets_within_provider_limit")
            report.blocker_codes.append(ProviderErrorCode.UNSUPPORTED_INPUT_ASSET)
            report.pass_status = False
        return report

    def build_payload(self, request: ProviderExecutionRequest) -> dict:
        return {
            "model": self.config.model_name,
            "prompt": request.prompt_contract.primary_prompt,
            "reference_images": [asset.uri for asset in request.reference_assets if asset.uri],
            "metadata": {
                "frame_profile": request.frame_profile,
                "composition_role": request.composition_role,
                "style_route": request.primary_style_route_id,
            },
        }

    def submit(self, request: ProviderExecutionRequest) -> ProviderSubmissionReceipt:
        payload = self.build_payload(request)
        api_key = os.getenv(self.config.credential_ref.env_var_name) if self.config.credential_ref else None
        headers = {"x-key": api_key} if api_key else {}
        path = self.config.extra.get("generate_path", "/v1/flux")
        response = self.http.post_json(
            url=f"{self.config.base_url}{path}",
            payload=payload,
            headers=headers,
            timeout=request.timeout_seconds,
        )
        provider_request_id = response.get("id") or response.get("request_id") or f"bfl_{request.provider_execution_request_id}"
        return ProviderSubmissionReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_request_id=provider_request_id,
            request_payload_hash=self._payload_hash(payload),
            idempotency_key=request.idempotency_key,
            raw_response_redacted={"response_keys": sorted(response.keys())},
        )

    def poll(self, request: ProviderExecutionRequest, submission: ProviderSubmissionReceipt) -> ProviderPollReceipt:
        return ProviderPollReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_request_id=submission.provider_request_id,
            status=ProviderExecutionStatus.RUNNING,
            raw_response_redacted={"async": True},
        )

    def download_outputs(self, request: ProviderExecutionRequest, poll: ProviderPollReceipt) -> list[ProviderOutputAsset]:
        return []
