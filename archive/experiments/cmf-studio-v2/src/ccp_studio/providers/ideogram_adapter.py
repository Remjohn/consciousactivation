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
    ProviderSubmissionReceipt,
    ProviderTransportMode,
)
from ccp_studio.providers.base import BaseProviderAdapter
from ccp_studio.providers.provider_http import ProviderHttpClient
from ccp_studio.providers.provider_storage import ProviderOutputStorage


class IdeogramAdapter(BaseProviderAdapter):
    provider_id = ProviderId.IDEOGRAM
    capability_ids = [
        ProviderCapabilityId.IMAGE_GENERATE,
        ProviderCapabilityId.IMAGE_REMIX,
        ProviderCapabilityId.IMAGE_DESCRIBE,
        ProviderCapabilityId.IMAGE_INPAINT,
        ProviderCapabilityId.IMAGE_UPSCALE,
        ProviderCapabilityId.BACKGROUND_REMOVE,
    ]

    def __init__(self, config: ProviderAdapterConfig | None = None, http: ProviderHttpClient | None = None, storage: ProviderOutputStorage | None = None):
        super().__init__(
            config
            or ProviderAdapterConfig(
                provider_id=ProviderId.IDEOGRAM,
                enabled=False,
                transport_mode=ProviderTransportMode.HTTP,
                base_url="https://api.ideogram.ai",
                model_name="ideogram",
                credential_ref=ProviderCredentialRef(provider_id=ProviderId.IDEOGRAM, env_var_name="IDEOGRAM_API_KEY"),
                extra={"generate_path": "/generate"},
            )
        )
        self.http = http or ProviderHttpClient()
        self.storage = storage or ProviderOutputStorage()

    def map_frame_profile_to_aspect_ratio(self, frame_profile: str) -> str:
        if frame_profile.startswith("9:16"):
            return "ASPECT_9_16"
        if frame_profile.startswith("4:5"):
            return "ASPECT_4_5"
        if frame_profile.startswith("16:9"):
            return "ASPECT_16_9"
        return "ASPECT_1_1"

    def build_payload(self, request: ProviderExecutionRequest) -> dict:
        return {
            "image_request": {
                "prompt": request.prompt_contract.primary_prompt,
                "aspect_ratio": self.map_frame_profile_to_aspect_ratio(request.frame_profile),
                "model": self.config.model_name,
            }
        }

    def submit(self, request: ProviderExecutionRequest) -> ProviderSubmissionReceipt:
        payload = self.build_payload(request)
        api_key = os.getenv(self.config.credential_ref.env_var_name) if self.config.credential_ref else None
        headers = {"Api-Key": api_key} if api_key else {}
        path = self.config.extra.get("generate_path", "/generate")
        response = self.http.post_json(
            url=f"{self.config.base_url}{path}",
            payload=payload,
            headers=headers,
            timeout=request.timeout_seconds,
        )
        provider_request_id = response.get("request_id") or response.get("id") or f"ideogram_{request.provider_execution_request_id}"
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
            status=ProviderExecutionStatus.SUCCEEDED,
            raw_response_redacted={"sync_or_external_poll": True},
        )

    def download_outputs(self, request: ProviderExecutionRequest, poll: ProviderPollReceipt) -> list[ProviderOutputAsset]:
        return []
